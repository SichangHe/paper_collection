                                          Are LLMs Rigorous Logical Reasoners? Empowering Natural Language
                                            Proof Generation by Stepwise Decoding with Contrastive Learning

                                                                 Ying Su1 , Mingwen Liu2 , Zhijiang Guo3,4
                                               South China University of Technology1 , Likelihood Lab2 , HKUST(GZ)3 , HKUST4
                                              yingsu@scut.edu.cn, maxwell@alphafuture.cn, zhijiangguo@hkust-gz.edu.cn



                                                               Abstract                          of their explanations (Xu et al., 2023). Utiliz-
                                             Logical reasoning is a pivotal component in         ing prompting methods such as in-context learn-
                                             the field of artificial intelligence. Proof plan-   ing (Brown et al., 2020) and chain-of-thought (Wei
arXiv:2311.06736v3 [cs.CL] 30 Oct 2025




                                             ning, particularly in contexts requiring the val-   et al., 2022), LLMs have shown promising re-
                                             idation of explanation accuracy, continues to       sults across various deductive reasoning tasks in
                                             present challenges. The recent advancement          question-answering formats (Weston et al., 2015;
                                             of large language models (LLMs) has led to          Tafjord et al., 2021; Saparov and He, 2022; Han
                                             significant progress in natural language proof
                                                                                                 et al., 2022). These approaches decompose the
                                             planning, evolving from one-stage generators
                                             to more complex three-stage systems that in-        final task goal by guiding the LLMs through inter-
                                             clude additional searchers or verifiers. While      mediate reasoning steps in a carefully constructed
                                             these assisted methods improve the quality of       context. However, providing correct explanations,
                                             generated results, they also introduce increased    which covers completeness, redundancy, correct-
                                             search efforts and computational costs. Fur-        ness (Xu et al., 2023), emerges as a more daunting
                                             thermore, the generative process itself remains     challenge. This is particularly evident in tasks that
                                             underexplored. In this study, we propose a          involve generating reasoning chains from premises
                                             stepwise decoding approach augmented by con-
                                                                                                 leading to a conclusion, known as proof genera-
                                             trastive learning to address two common errors
                                             encountered during the LLM generator’s decod-       tion (Clark et al., 2020; Dalvi et al., 2021). Unfor-
                                             ing process. We fine-tune the language model        tunately, LLMs often fall short in creating concise
                                             using both vanilla and enhanced hard negatives      and exact proof trees, commonly producing super-
                                             to mitigate these decoding errors. Empirical re-    fluous or imprecise intermediate steps.
                                             sults demonstrate the effectiveness of our strat-
                                                                                                    Previous studies have utilized LLMs to gener-
                                             egy. Additionally, our further analysis reveals
                                             that even larger LLMs still struggle to generate
                                                                                                 ate proof trees, employing a range of techniques
                                             rigorous logical chains.                            from holistic approaches (Qu et al., 2022) to in-
                                                                                                 cremental steps (Tafjord et al., 2021; Sanyal et al.,
                                         1   Introduction                                        2022). Recent methods increasingly rely on post-
                                         Logical reasoning underpins the comprehension           processing to enhance the quality of generated re-
                                         of human cognition and intelligence in ma-              sults, introducing verification- and search-based
                                         chines (Goel et al., 2017). Large Language Models       systems (Hong et al., 2022; Yang et al., 2022).
                                         (LLMs) like GPT (Brown et al., 2020; Ouyang             However, as the methods become more complex,
                                         et al., 2022) and PaLM (Chowdhery et al., 2022;         there is a corresponding increase in search efforts
                                         Anil et al., 2023) have pioneered using natu-           and computational costs. Conversely, there has
                                         ral language as a platform for logical reasoning,       been insufficient focus on refining the generative
                                         complementing the traditional use of formal lan-        process itself. Current models exhibit proficiency
                                         guages (Kazemi et al., 2022; Creswell et al., 2022).    in selecting relevant premises but struggle to de-
                                         The incorporation of natural language broadens          duce intermediary conclusions, highlighting a defi-
                                         the scope of logical reasoning by allowing flexible     ciency in their understanding of semantic nuances
                                         querying and tapping into the extensive implicit        during stepwise deductive reasoning.
                                         knowledge encapsulated within LLMs.                        Addressing this issue, we introduce a novel strat-
                                            In examining the capacity of LLMs for logical        egy dubbed ConDec (Contrastive learning based
                                         reasoning, it is crucial to consider not only the ac-   stepwise Decoding), designed to enhance the gen-
                                         curacy of their answers but also the correctness        erative aspect of LLMs for deductive reasoning
    Method                                  Stepwise     Stepwise     Direction Search Verifier Human-authored   Stage
                                            Generation   Correction                             Benchmark
    EntailmentWriter (Dalvi et al., 2021)   ✗            ✗            →        ✗       ✗       ✓                 1
    IRGR (Ribeiro et al., 2022)             ✓            ✗            →        ✓       ✗       ✓                 2
    SCSearch (Bostrom et al., 2022)         ✓            ✗            →        ✓       ✗       ✗                 2
    MetGen (Hong et al., 2022)              ✓            ✗            both     ✓       ✗       ✓                 2
    ADGV (Sprague et al., 2022)             ✓            ✗            both     ✓       ✓       ✓                 3
    NLProofs (Yang et al., 2022)            ✓            ✗            →        ✓       ✓       ✓                 3
    ConDec                                  ✓            ✓            →        ✗       ✗       ✓                 1

Table 1: Comparison of methods over natural language proof generation. Stepwise Correction means that if stepwise
generation is enhanced in training. Stage calculates if the method contains generation, verification, and search.

tasks. ConDec leverages carefully constructed hard                the form of natural language to alleviate the repre-
negatives – outputs that are deceivingly similar                  sentation challenge with formal language (Musen
in form yet differ semantically – to refine genera-               and Van der Lei, 1988).
tion precision. These hard negatives can be sim-                     Among the logical reasoning over natural lan-
ple sequence alterations or products of an intricate              guage (Yang et al., 2023), deductive reasoning
sampling and reasoning process, aided by an ex-                   covers aspects including hypothesis classification,
ternal reasoner and checker. Intuitively, the hard                proof generation, proof generation with incomplete
negatives are designed to solve decoding errors an-               information, and implication enumeration. Sev-
alyzed in (Dalvi et al., 2021): repetition and invalid            eral tasks have been proposed to evaluate these
entailment. Finetuning with these hard negatives                  reasoning abilities. Specifically, hypothesis clas-
notably advances the LLMs’ proficiency in interme-                sification is conducted over RuleTaker with trans-
diate step and conclusion generation, culminating                 formers (Clark et al., 2020). Proof generation pro-
in overall improved proof accuracy. The main con-                 viding rationals along with the predicted answer
tributions of this study are threefold:                           for emulating formal reasoning is further proposed
                                                                  to increase the explanability (Saha et al., 2020).
     • We introduce ConDec, a stepwise decoding                   ProofWriter (Tafjord et al., 2021) produces a de-
       with contrastive learning strategy that en-                ductive chain of reasoning over proof generation
       hances stepwise generative quality in proof                and implication enumeration with an iterative gen-
       generation tasks, and devise an automatic                  erating style. To enhance the chain of reasoning for
       method for hard negative generation involving              multi-step premises, EntailmentWriter tests trans-
       a reasoner and a checker;                                  formers’ explainability in the form of entailment
                                                                  trees over EntailmentBank (Dalvi et al., 2021).
     • We conduct an extensive empirical analysis
       on the Entailment benchmark, demonstrating                 2.2     Proof Generation
       the effectiveness of the proposed method;
                                                                  Methods for finetuning language models for proof
     • We reveal that LLMs even equipped with                     generation vary in the proof direction, infer-
       chain-of-thought strategies still struggle to              ence with or without hypothesis, and whether
       perform rigorous logical reasoning in natural              search or verification is involved. One line of re-
       language proof generation tasks.                           search is inference without a hypothesis available.
                                                                  FaiRR (Sanyal et al., 2022) breaks proof gener-
2      Related Work                                               ation into three steps: rule selection, fact selec-
                                                                  tion, and knowledge composition. MetGen (Hong
2.1      Logical Reasoning with Natural Language                  et al., 2022) iteratively generates the entailment
Logical reasoning is an important ability to re-                  tree by conducting a single-step entailment with
alize human-level cognition and intelligence in                   separate modules and a reasoning controller. SC-
AI (Nunes, 2012). Early research of logical rea-                  Search (Bostrom et al., 2022) decomposes the de-
soning uses formal language to represent knowl-                   ductive reasoning task into separate steps coor-
edge and conducts symbolic reasoning (Muggleton                   dinated by a search procedure, producing a tree
and De Raedt, 1994). Recent research uses pre-                    of intermediate conclusions that faithfully reflects
trained language models for logical reasoning in                  the system’s reasoning process. ADGV (Sprague
        Task Description
                                         Input                                                                              Output
                      The sun will be the star that appears the                                                              ℎ: the sun will be the star that
        Hypothesis 𝒉: brightest to the earth;
                                                                                        Proof tree (𝐓):                       appears the brightest to the
                                                                                                                                         earth
                         sent1: the sun is the star that is closest
                         to earth                                                                        int2: as the stars become
                                                                                                                                                 sent1: the sun is the star that
                         sent2: the four planets farthest from the                                      closer, the light of the stars
                                                                                                                                                      is closest to earth
                         sun are made of gas                                                                will appear brighter
         Facts 𝑪:        sent3: far means great in distance
                         sent4: furthest / farthest means greatest                                                          sent11: as a source of light
                                                                                                  int1: stars are a
                         / most / highest in distance                                                                      becomes closer, the light will
                         sent5: to be in the sun means to be in                                    source of light
                                                                                                                                 appear brighter
                         the sunlight
                         sent6: appear is similar to apparent
                         sent7: brightness means amount of light                       sent13: a source of                 sent16: a star
                                              ……                                     something produces light              produces light


      Stepwise Decoding with Contrastive Learning (ConDec)
                                                                                                                      Stepwise output 𝐬𝐭𝐞𝐩𝟐 :
       I𝐧𝐩𝐮𝐭 𝒙 𝐟𝐨𝐫 𝟐𝐧𝐝 𝐬𝐭𝐞𝐩 𝐠𝐞𝐧𝐞𝐫𝐚𝐭𝐢𝐨𝐧:
                                                                                                                      int1 & sent11 -> int2: as the stars become
      $hypothesis$=the sun will be the
      star that appears the brightest to
                                                    Encoder                          Decoder                          closer, the light of the stars will appear brighter;

      the earth;
                                                                                                                      Vanilla hard negative 𝐬𝐭𝐞𝐩𝟐 :
      $facts$=sent1: the sun is the star              𝐌                                       𝐇
      that is closest to earth sent2: the
      four …;                                                     Projection layer                                    int1 & sent11 -> int2: as a source of light
      $partial_proof$=sent13 & sent16                                                                                 becomes closer , the light will appear brighter;
      -> int1: stars are a source of light
                                                       𝐳!                                                             Enhanced hard negative 𝐬𝐭𝐞𝐩𝟐:
                                                                                         "!
                                                                                         𝐙                            sent11 & sent1 -> int2: the sun will be the star
                                                          𝐳"                     "!
                                                                                 𝐙                                    that appear the brightest to the earth;



Figure 1: Architecture of the stepwise decoding with contrastive learning over hard negatives. The hard negatives
are constructed by vanilla and enhanced strategies. Vanilla strategy means simple conclusion substitution. The
enhanced strategy uses a reasoner and a checker to generate hard negatives.

et al., 2022) proposes to abductively infer a premise                                     a subset of the facts {senti } ∈ C, denoting leaf
given another premise and a conclusion, as well                                           nodes on the tree T . U = {int1 , int2 , ..., intm }
as to search over two fingers interleaving deduc-                                         denotes the intermediate nodes on the tree. The
tive (forward-chaining) and abductive (backward-                                          intermediate nodes are deduced during the reason-
chaining) inferences.                                                                     ing process. Each intermediate node represents an
   Another line of work is with the hypothesis avail-                                     intermediate conclusion. The intermediate nodes
able. IBR (Qu et al., 2022) enhances the inter-                                           are internal tree nodes. On top of the tree, h is the
pretability of reasoning procedures by predicting                                         root node as well as the final conclusion needs to
nodes and edges in the proof tree iteratively back-                                       be proved.
ward from the question, as well as increasing ef-                                            The structure of the tree is denoted by reason-
ficiency and accuracy by simplifying the interme-                                         ing steps S = {step1 , step2 , ..., stept }. Each in-
diate process of reasoning. IRGR (Ribeiro et al.,                                         ternal tree node corresponds to a reasoning step
2022) explains a given hypothesis by iteratively                                          stepi ∈ S with intj ∈ U as the conclusion and
searching for suitable premises, constructing a sin-                                      its children as premises, i.e., sent1 & int1 → int2 ,
gle entailment step at a time. NLProofs (Yang et al.,                                     representing that intermediate node int2 is the con-
2022) trains an independent verifier to check the                                         clusion of leaf node sent1 and intermediate node
validity of the proof steps to improve decoding ac-                                       int1 . The premise of a reasoning step can be from
curacy. Our work follows this line and we focus                                           leaf nodes or intermediate nodes. Under the step-
on stepwise decoding correction on the generator                                          wise generation setting, intermediate nodes and
itself. A comparison of our method with other ap-                                         proof steps up to the current step are added to given
proaches with LLMs is presented in Table 1.                                               facts as input to generate new intermediate nodes
                                                                                          for the next step.
3   Problem Formulation
                                                                                          4       Approach
Following the task definition in Yang et al. (2022),
the proof generation task is to derive a proof tree T                                     4.1        Stepwise Decoding with Contrastive
given a hypothesis h and a set of supporting facts                                                   Learning
C = {sent1 , sent2 , ..., sentn }. The proof tree T                                       With stepwise training, subtrees are sampled on the
is represented as a tuple T = (h, Ĉ, U, S). Ĉ is                                        original entire proof graph. The decoding goal can
be the intermediate node or the final hypothesis of                  between the pair of source sequence and target se-
the subtree, depending on the sampling strategy. As                  quence while minimizing the similarity between
analyzed in (Dalvi et al., 2021), there are decoding                 the negative pairs as follows:
errors leading to inaccurate proof step generation,
                                                                                   N                             (i)   (i)
finally leading to entire proof generation failure.                                X             exp(sim(zx , zs )/τ )
                                                                     Lcont (θ) =         log P                         (i)   (k)
                                                                                                                                     ,
An overview is presented in Figure 1.                                                         (k)  exp(sim(zx , zs )/τ )
                                                                                   i=1       zs ∈S
   To address the problem, we adopt a contrastive                                                                    (6)
learning technique to improve the stepwise decod-                    where S is the set of negative samples in the same
ing quality. Learning with contrasting positive and                  batch and τ is the temperature parameter.
negative pairs can improve the generalization abil-
ity of conditional text generations (Lee et al., 2020;               4.2   Training with Hard Negative
An et al., 2022). Inspired by this, we construct neg-                Though stepwise generation improves over a single-
ative decoding samples to improve the reasoning                      shot generation (training over the entire proof tree
ability of the generator.                                            and the decoding goal is a hypothesis), it still has
   The goal of the generator is to output a                          typical errors (Dalvi et al., 2021): 1) repetition(the
                                    (i)
stepwise reasoning step stepj with tokens                            entailed conclusion simply repeats one of the input
  (i)     (i)    (i)                                                 sentences); 2) invalid entailment(the entailed con-
(s̃1 , s̃2 , ..., s̃L ) with length L conditioned on the
                                    (i) (i)                          clusion does not follow from input sentences). To
input text sequence x(i) = (x̃1 , x̃2 , ...). The in-
                                                                     improve the decoding quality, we design two types
put text sequence is a concatenation of contexts
                                                                     of hard negatives for these errors and finetune the
from hypothesis h, facts C, and previous steps
        (i)           (i)                                            model with these hard negatives.
{step1 , ..., stepj−1 }. i is the index of instances in                                                         (i)
                                                                        The hard negative sequence stepj is con-
a batch. The finetuning loss is to maximize the con-
                                                                     structed based on the gold proof step sequence
ditional log-likelihood log pθ (stepj |x) for a given                     (i)
                                   (i) N                             stepj . With the hard negative sequences, the de-
N observations {(x(i) , stepj )i=1 } as follows:                     coding loss becomes:
                        N
                                                  (i)
                        X
          LM LE (θ) =         log pθ (stepj |x(i) ),          (1)     Lcont−hard (θ) =
                        i=1                                           N                              (i)   (i)
                                                                      X                  exp(sim(zx , zs )/τ )
                                                                           log P                            (i) (i)
                                                                                                                          ,
                                 L
          (i)    (i)
                                 Y          (i)     (i)               i=1           (k) S (i)
                                                                                   zs ∈S {z̄s }
                                                                                                exp(sim(z   x  , zs )/τ )
  pθ (s̃1 , ..., s̃L |x(i) ) =         pθ (s̃l |s̃<l , x(i) ), (2)
                                                                                                                        (7)
                                 l=1                                         (i)
                                                                     where z̄s is the projected hidden state of hard
                                                                     negatives. The final loss for finetuning is:
    (i)         (i)
  hl = g(s̃l−1 , M(i) ; θ), M(i) = f (x(i) ; θ), (3)
                                                                                L = LM LE + αLcont−hard ,                      (8)
where f, g denote the encoder and the decoder
                                                                     α is a weighted parameter.
respectively. M(i) is the concatenation of the
hidden representations of the source tokens x(i) .                   4.2.1 Vanilla Hard Negative
H(i) is the concatenation of the hidden states                       Vanilla hard negatives are constructed based on sub-
  (i)       (i)
[h1 , ..., hL ] at the decoder output.                               stitution, which mimics the form of gold stepwise
   With a linear projection layer, the hidden states                 proofs, to address the repetition error. we randomly
M(i) and H(i) of the encoder and decoder are                         select one of the premises in a proof step stepj
mapped onto the latent embedding space:                              and replace the conclusion with its context. For
                                                                     example in Figure 1, the vanilla hard negative is
  z(i)
   x = AvgPool(ReLU(Wproj M
                                  (i)
                                      + bproj )),                    constructed by replacing the gold standard conclu-
                                               (4)                   sion with the context of input node sent11.
   (i)                            (i)
  zs = AvgPool(ReLU(Wproj H + bproj )).
                                               (5)                   4.2.2 Enhanced Hard Negative
The semantic similarity sim between them can be                      To increase the entailment quality over stepwise
calculated by distance with a dot or cosine func-                    proofs, we also propose to construct enhanced hard
tion. A contrastive loss maximizes the similarity                    negatives by exploring unseen proof steps with a
                      int1: stars are a                                                              int2: as the stars become closer, the
                       source of light                                                               light of the stars will appear brighter

                                                                                                                             sent11: as a source of light
          sent13: a source of                 sent16: a star                                    int1: stars are a           becomes closer, the light will
        something produces light              produces light                                     source of light                  appear brighter

                      1st step generation                                                            2nd step generation(Stepwise output 𝐬𝐭𝐞𝐩𝟐 )

    premise                                                                          int2: stars are close to a source of light
   sampling

  int1: stars are a       sent3: far means great in                              int1: stars are a                       sent3: far means
   source of light                 distance                                       source of light                        great in distance
                                                                                                                                                                0.144
                                                               Reasoner                                                                               Checker

                         sent11: as a source of light                                    int2: the sun will be the star that                                    0.968
 sent1: the sun is
                          becomes closer, the light                                      appear the brightest to the earth
  the star that is
 closest to earth           will appear brighter
                                                                                 sent1: the sun is                  sent11: as a source of light
                                                                                  the star that is                   becomes closer, the light
                                                                                 closest to earth                      will appear brighter

                                                        2nd step generation(Enhanced hard negative 𝐬𝐭𝐞𝐩𝟐 )


Figure 2: Enhanced hard negative construction is implemented by exploring the unseen combination of premises,
inferencing with the reasoner, and filtering with a score from the checker.

reasoner and a checker. The reasoner is first trained                                where the score is calculated with a sigmoid func-
with proof steps stepj ∈ S in natural language                                       tion after hidden layers γ.
and then utilized to generate a conclusion given an
unseen combination of premises in the supporting                                     5        Experiment
facts C.                                                                             5.1        Dataset
   Given proof step stepj , the premises and con-
                                                                                    EntailmentBank (Dalvi et al., 2021): Entailment
clusion in natural language are denoted as set
                                                                                    trees are made up of individual and multi-premise
{p1 , p2 , ...} and c. The premises are concatenated
                                                                                    textual entailment steps. EntailmentBank contains
as input and the conclusion is output for training
                                                                                    1,840 multi-step entailment trees for accompanying
the reasoner.
                                                                                    QA pairs. For the proof generation task, only the
                                                                                    hypothesis H and context set C are used as inputs.
             LM LE (ϕ) = log pϕ (c|p1 , p2 , ...),                         (9)
                                                                                    Each proof tree T contains an average of 6.6 nodes
After training, the reasoner can generate a conclu-                                 and 2.7 entailment steps. Train/Validation/Test
sion given an unseen combination of premises. The                                   splits are 1,313/187/340 respectively. Entailment-
premise combinations are first sampled from sup-                                    Bank consists of three tasks as follows:
porting fact set. The sampled premises {ps1 , ps2 , ...}                            (1) Task 1 (no-distractor): C consists of exactly
and generated conclusion cs constructs an en-                                       the leaf nodes of the ground truth proof tree;
hanced hard negative step. Details are presented                                    (2) Task 2 (distractor): C consists of 15-20 dis-
in Figure 2. In the example, for premises int1 and                                  tractor sentences besides the leaf nodes on the
sent11 in gold proof, randomly sample one premise                                   ground truth proof tree;
to substitute one of them and use the reasoner to                                   (3) Task 3 (full-corpus): C is a large corpus of
generate a new conclusion given the recombined                                      12K sentences derived from WorldTree V2 (Xie
premises.                                                                           et al., 2020), requiring the model to retrieve rele-
                                                                                    vant supporting facts from the corpus. For each
   To improve the quality of the hard negatives
                                                                                    hypothesis, 25 supporting facts are retrieved. Fol-
generated from the reasoner, we further adopt the
                                                                                    lowing Dalvi et al. (2021), we evaluate the zero-
checker Vera (Liu et al., 2023) to score the hard
                                                                                    shot performance of the model from Task 2.
negatives and filter those with low scores. Vera is
finetuned over T5-11B with commonsense datasets.                                     5.2        Evaluation
The score from the checker indicates the extent of
                                                                                     Following Dalvi et al. (2021), we use the official
the reasonableness of the deductive commonsense
                                                                                     tools1 to evaluate the generated entailment tree
knowledge generated by the reasoner:
                                                                                     T = (h, L, E, S) with the golden entailment tree
       score = sigmoid([ps1 , ps2 , ..., cs ]; γ),                        (10)            1
                                                                                              https://github.com/allenai/entailment_bank
  Reasoner    Enhanced Negative    Filtered Negative      neptune orbits the sun in the solar system, the hard
              Task 1   Task 2      Task 1 Task 2          negatives substitute conclusion neptune orbits the
      8,819
              47,386 104,665       16,371 21,948          sun in the solar system with the context of sent11
                                                          or sent24. The temperature τ is set as 0.05 and α
Table 2: Distribution of samples from training data,      is 0.1. The learning rate of the stepwise decoding
constructed enhanced hard negatives and filtered hard
                                                          stage is the same as finetuning with original proof
negatives on Task 1 and Task 2. In filtering, threshold
score is 0.9.                                             trees. The MLE loss and contrastive loss are
                                                          alternatively trained for 10 epochs based on the
T ∗ = (h, L∗ , E ∗ , S ∗ ). These metrics evaluate the    finetuned generator with MLE loss only.
correctness along 4 dimensions:
(1) Leaves (F1, AllCorrect): F1 measures the pre-         Enhanced Hard Negatives. We use Flan-T5-
cision of leaf nodes of T comparing to gold tree          Large as an additional reasoner to generate unseen
T ∗ . ALLCorrect=1 if F1=1, and ALLCorrect=1 if           proof steps based on labeled proof trees as hard
F1<1.                                                     negatives. To train the reasoner, details of data
(2) Steps (F1, AllCorrect): F1 measures the preci-        collection are presented in Appendix A.1. The rea-
sion of proof steps structurally correctness. Each        soner is trained for 30 epochs with a learning rate
step contains an internal node u ∈ T ∗ (aligned to        of 1e-4. We further apply Vera (Liu et al., 2023)
v ∈ T ). The predicted step is correct if u and v are     to filter unreasonable generated proof steps. De-
perfectly aligned. For each tree, ALLCorrect=1 if         tails of stepwise proofs sampled for reasoner and
F1=1 otherwise 0.                                         enhanced new negatives filtered by the checker are
(3) Intermediates (F1, AllCorrect): For the inter-        presented in Table 2. To increase diversity, en-
nal node u ∈ T ∗ (aligned to v ∈ T ), the interme-        hanced hard negatives and vanilla hard negatives
diate conclusion is correct if the BLEURT (Sellam         are jointly sampled for training.
et al., 2020) score between u and v is greater than
0.28 (Dalvi et al., 2021). F1 and AllCorrect from
                                                          6     Result Analysis
all intermediate conclusions in T ∗ and T are calcu-      6.1    Main Results
lated. ALLCorrect=1 if F1=1 otherwise 0.
                                                          The main results are presented in Table 3. By ana-
(4) Overall (AllCorrect): The metric evaluates
                                                          lyzing the results, we can find that:
whether leaves, steps, and intermediates are all
                                                          Stepwise correction matters. Stepwise generation
correct, AllCorret = 1 if and only if all the leaves,
                                                          methods (MetGen, NLProofs, ConDec) outperform
steps, and intermediates are all correct.
                                                          single-shot training (EntailmentWriter), even for
5.3    Implementation Details                             EntailmentWriter with a much larger parameter
                                                          size (11B). When comparing ConDec with three-
The optimizer is set as Adam (Kingma and Ba,              stage generation methods MetGen and NLProofs,
2014) for all the training. The average running           ConDec achieves comparable or even better perfor-
time is 18 hours for Task 1 and 24 hours for Task 2.      mance on Task 2 and Task 3. This shows that con-
Experiments are conducted on A800.                        trastive decoding with hard negatives can improve
                                                          language models’ reasoning ability, demonstrating
Generator. We use Flan-T5-Large as the gen-               our methods’ effectiveness. While our research fo-
erator. Flan-T5-Large is a finetuned version of           cuses on the generator, combining our method with
T5-Large (Raffel et al., 2020) over a collection of       theirs may still improve the final accuracy and it is
FLAN instructions (Chung et al., 2022; Longpre            worth exploring.
et al., 2023). The generator is trained for 500           Enhanced hard negatives facilitate reasoning.
epochs on Task1 and 600 epochs on Task2. The              With enhanced hard negatives, we can find that the
learning rate for the first-stage generator is 1e-4       ability of proof planning over three tasks is all im-
and 5e-5 for Task 1 and Task 2 respectively.              proved. Unlike vanilla negative construction, the
                                                          enhanced hard negatives contain harder or more
ConDec. The vanilla hard negatives are con-               accurate conclusions given premises. Detailed eval-
structed by substituting the conclusion in the gold       uation of enhanced hard negatives is in Appendix
proof step with a randomly selected premise node          A.1. It further improves the training coverage over
context. For example, for sent11 & sent24 -> int:         reasoning steps, thus leading to better performance
                                                         Leaves                   Steps          Intermediates          Overall
           Task                Method
                                                  F1       AllCorrect      F1      AllCorrect   F1 AllCorrect          AllCorrect
          Task 1           EntailmentWriter       98.7        86.2         50.5      37.7       67.6     36.2             33.5
      (no-distractor)   EntailmentWriter (11B)    99.0        89.4         51.5      38.2       71.2     38.5             35.3
                               MetGen∗           100.0       100.0         57.7      41.9       70.8     39.2             36.5
                              NLProofs∗          97.8        90.1          55.6      42.3       72.4     40.6             38.9
                                ConDec           99.9         98.2         55.7      42.1       72.3     38.9             36.2
                               ConDec⋆           99.9         98.2         57.3      43.2       72.9     41.5             37.9
         Task 2            EntailmentWriter      84.3         35.6         35.5      22.9       61.8     28.5             20.9
       (distractor)     EntailmentWriter (11B)   89.1         48.8         41.4      27.7       66.2     31.5             25.6
                               MetGen∗           82.7         46.1         41.3      29.6       61.4     32.4             27.7
                              NLProofs∗          90.3         58.8         47.2      34.4       70.2     37.8             33.3
                                ConDec           91.0         59.1         50.2      36.5       70.3     38.2             34.1
                               ConDec⋆           91.1         60.6         50.7      37.4       70.7     38.2             34.7
         Task 3            EntailmentWriter      35.7         2.9           6.1       2.4       33.4      7.7             2.4
      (full-corpus)     EntailmentWriter (11B)   39.9         3.8           7.4       2.9       35.9      7.1             2.9
                               MetGen∗           34.8         8.7           9.8       8.6       36.6     20.4             8.6
                              NLProofs∗          43.2         8.2          11.2       6.9       42.9     17.3             6.9
                                ConDec           43.3         8.2          11.1       6.5       43.4     18.0             6.5
                               ConDec⋆           44.7         9.4          11.7       7.1       42.3     17.7             7.1

Table 3: Main results on EntailmentBank with finetuning method. Methods with ∗ are three-stage. ConDec denotes
finetuning with vanilla hard negatives and ConDec⋆ denotes finetuning with combination of vanilla and enhanced
hard negatives. Best results are boldface and second-best results are underlined.

over proof planning.                                                  Method        Stage                       Time(s)    Improvement
ConDec is more efficient with distractors. Specif-                    ConDec        generator                    294               -
                                                                      NLProofs      generator+search             430             31.6%
ically, contrastive learning with hard negatives
                                                                      NLProofs      generator+search+verify      544             46.0%
achieves obvious performance gain over Task 2
and Task 3 while deteriorating the performance on                    Table 4: Computation time comparison(percentage re-
Task 1. For Task 2 and Task 3, there are distractor                  duction). Time denotes the inference time. NLProofs
premises or full-corpus, which increases the chal-                   requires additional search and verification for predic-
lenges for rigorous reasoning. For Task 1, there is                  tion.
no distractor. Adding hard negatives deviates the
                                                                     6.3     Ablation Study
generator from generating correct steps instead of
intermediate nodes.                                                  Results of the ablation study on Task 2 test split are
Predicting intermediate node is still challenging.                   presented in Table 5.
ConDec achieves the best performance mostly over                     Backbone model. The results indicate that
leave or step accuracy. The contrastive loss helps                   LLaMA-3.2-1B fails to adequately differentiate be-
the generator discriminate between premises and                      tween input premises and output reasoning proof
finds semantically correlated premises to deduce a                   steps. As a decoder model focused on next-word
conclusion. However, deductive reasoning is still                    prediction, LLaMA simply predicts proof steps as
challenging as the improvement over intermediates                    the next sentence following the premises. With
is not as obvious as that on leaves or steps.                        stepwise training, the presence of intermediate or
                                                                     hypothesis nodes can confuse the model regarding
                                                                     when to stop generating output, as a subtree with
6.2   Computational Cost Analysis
                                                                     an intermediate node is a subsequence of the en-
ConDec’s design can reduce the inference cost with                   tire tree that includes the hypothesis node. This
a one-stage process during inference as shown in                     is why LLaMA tends to produce shorter outputs
Table 4. We provide a concrete comparison using                      when trained in a stepwise manner.
the validation set for Task 2, with the same model                      Moreover, the results for LLaMA are signifi-
size (Flan-T5-Large), on an A800 GPU. It clearly                     cantly lower than those for Flan-T5-Large, despite
shows that ConDec can significantly improve time                     the latter’s smaller size. Natural proof generation is
efficiency compared to two and three-stage meth-                     fundamentally a sequence-to-sequence task. Distin-
ods (NLProofs).                                                      guishing between input and output is crucial, as the
                                                           Leaves                  Steps             Intermediates        Overall
                      Method
                                                    F1      AllCorrect       F1     AllCorrect      F1 AllCorrect        AllCorrect
    LLaMA-3.2-1B (1.2B, w/o stepwise)               19.5         5.3        6.4          2.9       13.9          5.3           2.7
    LLaMA-3.2-1B (1.2B, stepwise)                   15.6         3.5        4.1          3.2        9.9          5.0           3.2
    Flan-T5-Large (0.8B, stepwise)                  90.7         58.8       49.2      36.2         69.6          36.8      33.5
    + contrastive loss                              90.9         60.3       49.5      35.9         69.4          37.1      32.4
    + contrastive loss, vanilla hard                91.0         59.1       50.2      36.5         70.3          38.2      34.1
    + contrastive loss, vanilla and enhanced hard   91.1         60.6       50.7      37.4         70.7          38.2      34.7
    Flan-T5-XL (3B, stepwise)                       90.9         57.1       50.2      36.5         68.8          35.9      33.8

                          Table 5: Ablation study results on EntailmentBank test set in Task 2.

                                        Leaves                          Steps                     Intermediates          Overall
             Method
                                F1          AllCorrect      F1              AllCorrect     F1            AllCorrect     AllCorrect
    ConDec⋆                     92.4         63.1           55.3            45.5           72.8           43.9          41.2
    GPT3 (5-shot)               64.2         15.3           17.6            12.3           53.6           22.3          12.3
    GPT3.5-turbo (5-shot)       61.9         9.0            16.9            4.3            51.9           15.1          3.74
    GPT4 (5-shot)               78.1         32.6           30.2            22.5           63.9           30.8          21.9
    GPT4 (SI)                   79.1         30.0           24.3            14.0           65.4           32.1          13.9
    GPT4 (CoT)                  79.0         33.7           30.9            22.5           64.7           31.6          22.5
    GPT4o-mini (5-shot)         63.1         18.2           20.0            13.9           54.5           24.1          13.9
    o1-mini (5-shot)            72.5         27.3           28.6            13.9           50.9           18.7          11.8
    o1-preview (5-shot)         84.0         43.3           38.7            28.0           67.8           33.7          21.9

Table 6: Results on EntailmentBank validation set in Task 2 with finetuning and prompting methods. GPT3.5 is
GPT3.5-turbo-0613. GPT4 is GPT4-0613. GPT4o-mini is gpt-4o-mini-2024-07-18. o1-mini is o1-mini-2024-09-12.
o1-preview is o1-preview-2024-09-12.


encoder-decoder architecture of Flan-T5 processes                      Based on it, Select-inference(SI)(Creswell et al.,
different texts. A case study comparing LLaMA                          2022) is a two-stage COT that decomposes each
and Flan-T5 is presented in the Appendix A.6.                          reasoning step into a premise selection stage and
Model size. For the model size, we also try Flan-                      a conclusion inference state. Details of the CoT is
T5-XL (3B). Stepwise training over Flan-T5-Large                       illustrated in Appendix A.2.2.
provides a strong baseline. Though much larger                            As shown in Table 6. Comparing different
in model size, Flan-T5-XL achieves similar per-                        LLMs, GPT4 generally outperforms GPT3 and
formance over the metrics. It shows that proof                         GPT3.5-turbo on all the metrics. One detailed
planning requires a higher level of understanding                      case study of GPT3.5-turbo and GPT4 with k-shot
of deductive reasoning over multi-hops.                                prompting results is in Appendix A.2.1. It shows
Negative sample. ConDec without hard negatives                         that the GPT3.5-turbo tends to generate more irrel-
improves the leave accuracy while decreasing the                       evant and inaccurate steps with simple imitation of
step accuracy, leading to a slight drop in the overall                 premises during inferencing new conclusions. In
performance. Adding vanilla or enhanced hard neg-                      contrast, GPT4 conducts deductive reasoning and
atives can generally improve over all the metrics.                     generates correct conclusions based on premises.
                                                                       When accompanied by CoT, GPT4 achieves bet-
7     Analysis of Closed-Source LLMs                                   ter performance than the vanilla prompt. While
In-context learning (ICL; Brown et al. 2020) and                       with SI, GPT4 makes more mistakes in the premise
CoT (Wei et al., 2022) have been widely used in                        selection stage.
various reasoning tasks (Patel et al., 2021; Cobbe                        Our ConDec⋆ outperforms all closed-source
et al., 2021; Fu et al., 2022; Xiong et al., 2023).                    LLMs in all metrics. Although recent LLMs such
We apply 5-shot prompting and CoT to evaluate                          as o1-mini and o1-preview show improvements
how LLMs perform on the proof generation task.                         in several metrics compared to their predecessors
The vanilla prompt method simply adopts a k-shot                       (GPT-3.5-turbo and GPT-4), a substantial perfor-
in-context learning strategy. The CoT decomposes                       mance gap remains when compared to finetuning-
the reasoning process into step-by-step generation.                    based methods. Through stepwise training with
curated datasets, these language models can better           Paul Barham, Hyung Won Chung, Charles Sutton,
capture the correlations between premises.                   Sebastian Gehrmann, et al. 2022. Palm: Scaling
                                                             language modeling with pathways. arXiv preprint
8   Conclusion                                               arXiv:2204.02311.
                                                           Hyung Won Chung, Le Hou, Shayne Longpre, Bar-
Logical reasoning is both challenging and funda-             ret Zoph, Yi Tay, William Fedus, Eric Li, Xuezhi
mental in artificial intelligence. Proof generation          Wang, Mostafa Dehghani, Siddhartha Brahma, et al.
serves as a measure of the explanatory capabilities          2022. Scaling instruction-finetuned language models.
of large language models in the context of logical           arXiv preprint arXiv:2210.11416.
reasoning. To enhance stepwise deductive reason-           Peter Clark, Oyvind Tafjord, and Kyle Richardson. 2020.
ing, we propose a decoding strategy augmented by             Transformers as soft reasoners over language. In
contrastive learning. The carefully designed hard            Proceedings of the Twenty-Ninth International Joint
                                                             Conference on Artificial Intelligence, IJCAI 2020,
negatives address the typical errors encountered
                                                             pages 3882–3890. ijcai.org.
during the decoding process. The experimental re-
sults across standard benchmarks demonstrate the           Karl Cobbe, Vineet Kosaraju, Mohammad Bavarian,
                                                             Mark Chen, Heewoo Jun, Lukasz Kaiser, Matthias
effectiveness of our method. Additionally, our anal-
                                                             Plappert, Jerry Tworek, Jacob Hilton, Reiichiro
ysis of larger LLMs reveals that they continue to            Nakano, et al. 2021. Training verifiers to solve math
struggle with proof planning tasks.                          word problems. arXiv preprint arXiv:2110.14168.

Limitations                                                Antonia Creswell, Murray Shanahan, and Irina Higgins.
                                                             2022. Selection-inference: Exploiting large language
From the analysis of the paper, natural proof plan-          models for interpretable logical reasoning. arXiv
                                                             preprint arXiv:2205.09712.
ning ability is still a challenging topic in evaluating
LLMs’ deductive reasoning ability. The current cu-         Bhavana Dalvi, Peter Jansen, Oyvind Tafjord, Zhengnan
rated human-annotated dataset in our experiments             Xie, Hannah Smith, Leighanna Pipatanangkura, and
                                                             Peter Clark. 2021. Explaining answers with entail-
is of limited size to improve LLMs’ deductive rea-
                                                             ment trees. In Proceedings of the 2021 Conference
soning ability. Knowledge from related corpora               on Empirical Methods in Natural Language Process-
such as cause and effect, logic reasoning can be fur-        ing, pages 7358–7370.
ther applied to improve the proof generation ability
                                                           Yao Fu, Hao Peng, Ashish Sabharwal, Peter Clark,
with pre-training or transfer learning.                      and Tushar Khot. 2022. Complexity-based prompt-
                                                             ing for multi-step reasoning.    arXiv preprint
                                                             arXiv:2210.00720.
References
                                                           Vinod Goel, Gorka Navarrete, Ira A Noveck, and
Chenxin An, Jiangtao Feng, Kai Lv, Lingpeng Kong,            Jérôme Prado. 2017. The reasoning brain: the in-
  Xipeng Qiu, and Xuanjing Huang. 2022. Cont: Con-           terplay between cognitive neuroscience and theories
  trastive neural text generation. Advances in Neural        of reasoning.
  Information Processing Systems, 35:2197–2210.
                                                           Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting
Rohan Anil, Andrew M Dai, Orhan Firat, Melvin John-          Qi, Martin Riddell, Luke Benson, Lucy Sun, Eka-
  son, Dmitry Lepikhin, Alexandre Passos, Siamak             terina Zubova, Yujie Qiao, Matthew Burtell, et al.
  Shakeri, Emanuel Taropa, Paige Bailey, Zhifeng             2022. Folio: Natural language reasoning with first-
  Chen, et al. 2023. Palm 2 technical report. arXiv          order logic. arXiv preprint arXiv:2209.00840.
  preprint arXiv:2305.10403.
                                                           Ruixin Hong, Hongming Zhang, Xintong Yu, and
Kaj Bostrom, Zayne Sprague, Swarat Chaudhuri, and            Changshui Zhang. 2022. METGEN: A module-
  Greg Durrett. 2022. Natural language deduction             based entailment tree generation framework for an-
  through search over statement compositions. In Find-       swer explanation. In Findings of the Association
  ings of the Association for Computational Linguistics:     for Computational Linguistics: NAACL 2022, pages
  EMNLP 2022, pages 4871–4883.                               1887–1905, Seattle, United States. Association for
                                                             Computational Linguistics.
Tom Brown, Benjamin Mann, Nick Ryder, Melanie
  Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind       Seyed Mehran Kazemi, Najoung Kim, Deepti Bhatia,
  Neelakantan, Pranav Shyam, Girish Sastry, Amanda           Xin Xu, and Deepak Ramachandran. 2022. Lam-
  Askell, et al. 2020. Language models are few-shot          bada: Backward chaining for automated reasoning in
  learners. Advances in neural information processing        natural language. arXiv preprint arXiv:2212.13894.
  systems, 33:1877–1901.
                                                           Diederik P Kingma and Jimmy Ba. 2014. Adam: A
Aakanksha Chowdhery, Sharan Narang, Jacob Devlin,            method for stochastic optimization. arXiv preprint
  Maarten Bosma, Gaurav Mishra, Adam Roberts,                arXiv:1412.6980.
Seanie Lee, Dong Bok Lee, and Sung Ju Hwang. 2020.          Danilo Neves Ribeiro, Shen Wang, Xiaofei Ma, Rui
  Contrastive learning with adversarial perturbations         Dong, Xiaokai Wei, Henghui Zhu, Xinchi Chen,
  for conditional text generation. In International Con-      Peng Xu, Zhiheng Huang, Andrew Arnold, et al.
  ference on Learning Representations.                        2022. Entailment tree explanations via iterative
                                                              retrieval-generation reasoner. In Findings of the Asso-
Jiacheng Liu, Wenya Wang, Dianzhuo Wang, Noah A               ciation for Computational Linguistics: NAACL 2022,
   Smith, Yejin Choi, and Hannaneh Hajishirzi. 2023.          pages 465–475.
   Vera: A general-purpose plausibility estimation
   model for commonsense statements. arXiv preprint         Stephen Robertson, Hugo Zaragoza, et al. 2009. The
   arXiv:2305.03695.                                           probabilistic relevance framework: Bm25 and be-
                                                              yond. Foundations and Trends® in Information Re-
Tengxiao Liu, Qipeng Guo, Xiangkun Hu, Yue Zhang,              trieval, 3(4):333–389.
  Xipeng Qiu, and Zheng Zhang. 2022. Rlet: A rein-
  forcement learning based approach for explainable         Swarnadeep Saha, Sayan Ghosh, Shashank Srivastava,
  qa with entailment trees. In Proceedings of the 2022        and Mohit Bansal. 2020. Prover: Proof generation
  Conference on Empirical Methods in Natural Lan-             for interpretable reasoning over rules. In Proceedings
  guage Processing, pages 7177–7189.                          of the 2020 Conference on Empirical Methods in
                                                              Natural Language Processing (EMNLP), pages 122–
Shayne Longpre, Le Hou, Tu Vu, Albert Webson,                 136.
  Hyung Won Chung, Yi Tay, Denny Zhou, Quoc V
  Le, Barret Zoph, Jason Wei, et al. 2023. The flan         Soumya Sanyal, Harman Singh, and Xiang Ren. 2022.
  collection: Designing data and methods for effective        FaiRR: Faithful and robust deductive reasoning over
  instruction tuning. arXiv preprint arXiv:2301.13688.        natural language. In Proceedings of the 60th Annual
                                                              Meeting of the Association for Computational Lin-
Stephen Muggleton and Luc De Raedt. 1994. Induc-              guistics (Volume 1: Long Papers), pages 1075–1093,
   tive logic programming: Theory and methods. The            Dublin, Ireland. Association for Computational Lin-
  Journal of Logic Programming, 19:629–679.                   guistics.

Mark A Musen and Johan Van der Lei. 1988. Of brit-          Abulhair Saparov and He He. 2022. Language models
 tleness and bottlenecks: Challenges in the creation          are greedy reasoners: A systematic formal analysis of
 of pattern-recognition and expert-system models. In          chain-of-thought. arXiv preprint arXiv:2210.01240.
 Machine intelligence and pattern recognition, vol-
 ume 7, pages 335–352. Elsevier.                            Thibault Sellam, Dipanjan Das, and Ankur Parikh. 2020.
                                                              Bleurt: Learning robust metrics for text generation.
Terezinha Nunes. 2012. Logical reasoning and learning.        In Proceedings of the 58th Annual Meeting of the As-
  pages 2066–2069.                                            sociation for Computational Linguistics, pages 7881–
                                                              7892.
Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida,
  Carroll Wainwright, Pamela Mishkin, Chong Zhang,          Zayne Sprague, Kaj Bostrom, Swarat Chaudhuri, and
  Sandhini Agarwal, Katarina Slama, Alex Ray, et al.          Greg Durrett. 2022. Natural language deduction with
  2022. Training language models to follow instruc-           incomplete information. In Proceedings of the 2022
  tions with human feedback. Advances in Neural               Conference on Empirical Methods in Natural Lan-
  Information Processing Systems, 35:27730–27744.             guage Processing, pages 8230–8258.

Arkil Patel, Satwik Bhattamishra, and Navin Goyal.          Oyvind Tafjord, Bhavana Dalvi, and Peter Clark. 2021.
  2021.      Are nlp models really able to solve              Proofwriter: Generating implications, proofs, and
  simple math word problems?        arXiv preprint            abductive statements over natural language. In Find-
  arXiv:2103.07191.                                           ings of the Association for Computational Linguistics:
                                                              ACL-IJCNLP 2021, pages 3621–3634.
Hanhao Qu, Yu Cao, Jun Gao, Liang Ding, and Ruifeng
  Xu. 2022. Interpretable proof generation via itera-       Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten
  tive backward reasoning. In Proceedings of the 2022          Bosma, Brian Ichter, Fei Xia, Ed H. Chi, Quoc V. Le,
  Conference of the North American Chapter of the              and Denny Zhou. 2022. Chain-of-thought prompt-
  Association for Computational Linguistics: Human             ing elicits reasoning in large language models. In
  Language Technologies, pages 2968–2981, Seattle,             NeurIPS.
  United States. Association for Computational Lin-
  guistics.                                                 Jason Weston, Antoine Bordes, Sumit Chopra, Alexan-
                                                               der M Rush, Bart Van Merriënboer, Armand Joulin,
Colin Raffel, Noam Shazeer, Adam Roberts, Katherine            and Tomas Mikolov. 2015. Towards ai-complete
  Lee, Sharan Narang, Michael Matena, Yanqi Zhou,              question answering: A set of prerequisite toy tasks.
  Wei Li, and Peter J Liu. 2020. Exploring the limits          arXiv preprint arXiv:1502.05698.
  of transfer learning with a unified text-to-text trans-
  former. The Journal of Machine Learning Research,         Zhengnan Xie, Sebastian Thiem, Jaycie Martin, Eliz-
  21(1):5485–5551.                                            abeth Wainwright, Steven Marmorstein, and Peter
  Jansen. 2020. Worldtree v2: A corpus of science-
  domain structured explanations and inference pat-
  terns supporting multi-hop inference. In Proceedings
  of the Twelfth Language Resources and Evaluation
  Conference, pages 5456–5473.
Jiong Xiong, Zixuan Li, Chuanyang Zheng, Zhijiang
   Guo, Yichun Yin, Enze Xie, Zhicheng Yang, Qingx-
   ing Cao, Haiming Wang, Xiongwei Han, Jing Tang,
   Chengming Li, and Xiaodan Liang. 2023. Dq-lore:
   Dual queries with low rank approximation re-ranking
   for in-context learning. ArXiv, abs/2310.02954.
Fangzhi Xu, Qika Lin, Jiawei Han, Tianzhe Zhao, Jun
  Liu, and Erik Cambria. 2023. Are large language
  models really good logical reasoners? a comprehen-
  sive evaluation from deductive, inductive and abduc-
  tive views. arXiv preprint arXiv:2306.09841.
Kaiyu Yang, Jia Deng, and Danqi Chen. 2022. Gen-
  erating natural language proofs with verifier-guided
  search. In Proceedings of the 2022 Conference on
  Empirical Methods in Natural Language Processing,
  pages 89–105.

Zonglin Yang, Xinya Du, Rui Mao, Jinjie Ni, and Erik
  Cambria. 2023. Logical reasoning over natural lan-
  guage as knowledge representation: A survey. arXiv
  preprint arXiv:2303.12023.
          Threshold score     Accuracy(%)                  A.3   Baseline Details
                 0.7                36                     MetGen and NLProofs are three-stage methods.
                 0.8                50                     MetGen divides single-step entailment into basic
                 0.9                60                     logical operations. It reasons in both forward
                                                           deductive and backward abductive steps. A
Table 7: Human check accuracy on enhanced hard nega-       controller finally selects promising steps among
tives from reasoner and checker with different threshold   the reasoning results. NLProofs uses a trained
scores.                                                    verifier to guide the search process of proof
                                                           generation. The verifier scores the generation
                                                           expansion steps and finally, a proof tree is selected
A     Appendix                                             according to the scores.
A.1     Details of Enhanced Hard Negatives
Training data of the reasoner is basically all the         A.4   Discussion with RLET
proof steps in the training set. Each proof step           RLET(Liu et al., 2022) is trained using cumulative
is converted into the form of natural language: 1)         signals across the entire entailment tree, marking
premises are concatenated with conjunction “and”;          the first introduction of reinforcement learning into
2) premises and conclusion are linked with “Be-            the entailment tree generation task. It employs a
cause” and “Therefore”. The reasoner is trained            one-stage generation method that does not involve
with 8,819 proof steps for both Task 1 and Task 2.         search or verification. RLET flexibly assigns re-
   For each proof step stepj , substitute one premise      wards to each generated step and utilizes the overall
from the the supporting fact set C except the ones         cumulative reward to optimize training based on
in current proof step. Recombined proof premises           the full trajectory. In contrast, our approach and
{ps1 , ps2 , ...} are converted into natural language      previous methods (as listed in Table 1) rely on exact
form and used as input to the reasoner. The rea-           matches of gold steps as training signals.
soner generates a new conclusion cs based on the              In Task 3, the retrieved supporting facts may con-
                                           (i)             tain noise and are longer than those in Task 1 and
premises, forming a hard negative stepj .
                                         (i)               Task 2. RLET’s focus on long-path proof training
    The constructed hard negative stepj is then fil-
                                                           provides it with an advantage over our method (and
tered by the checker with a threshold score. To
                                                           previous methods listed in Table 1) in this task.
determine the threshold score, three PhD students
                                                           However, since the supporting facts are sourced
from the CSE department are assigned with the
                                                           from a relevant corpus, they may deviate from the
task to check the quality of 100 randomly selected
                                                           training setting, particularly under zero-shot per-
constructed hard negatives. Each hard negative is
                                                           formance conditions. As a result, RLET’s perfor-
first judged by Vera. The score from Vera indi-
                                                           mance is significantly lower than that of previous
cates the reasonableness of the hard negative. By
                                                           methods in Task 1 and Task 2.
filtering the score with a threshold, we choose the
constructed negatives with high quality for further
training. The result of human checking over the fil-
tered negatives is shown in the table 7. We find that
with a threshold score of 0.9, 60% of the filtered
hard negatives are reasonable.

A.2     Prompting Methods
A.2.1    Case study for prompting
Result case from GPT3.5-turbo and GPT4 on Task2
dev split with vanilla prompts is shown in Table 8.

A.2.2    Template for prompting
Prompting template for GPT4 with CoT is in Table
9.
Hypothesis: new york state has the least sunlight during december
Context:
sent1: precipitation is a kind of weather
sent2: daylight hours means time during which there is daylight
sent3: state means form
sent4: water is in the liquid state , called liquid water , for temperatures between 273 / 32 / 0 and 373 /
212 / 100 k / f / c
sent5: united states is located in the northern hemisphere
...
sent9: when the seasons change from summer to fall / from summer to winter , the amount of daylight
will decrease
...
sent14: new york / new york state is a state located in the united states of america
sent15: winter has the least sunlight
...
sent22: the earth being tilted on its rotating axis causes seasons
sent23: december is during the winter in the northern hemisphere
...
Gold Proof: sent14 & sent5 -> int1: new york state is located in the northern hemisphere; int1 & sent23
-> int2: december is during the winter for new york state; int2 & sent15 -> hypothesis;
GPT3.5-turbo: sent23 & sent22 -> int1: December is during the winter in the northern hemisphere;
int1 & sent9 -> int2: the amount of daylight will decrease during December; int2 & sent15 -> int3:
December has the least sunlight; int3 & sent14 -> hypothesis;
GPT4: sent14 & sent5 -> int1: New York state is located in the northern hemisphere; int1 & sent23 ->
int2: December is during the winter in New York state; int2 & sent15 -> hypothesis;

                    Table 8: Case study of vanilla prompt with GPT3.5-turbo and GPT4.




Hypothesis: if a fossil of a bird cannot be identified then that kind of bird is probably extinct.
Context:
sent1: identifying is similar to determining.
sent2: if a fossil is of an organism that cannot be identified then that organism is probably extinct.
sent3: discovering something usually requires seeing that something.
sent4: a dinosaur is a kind of extinct animal.
sent5: fossils can be used as evidence for the ancient environment.
sent6: dead means not alive.
...
sent25: fossils can be used to study the history of organisms and environments on earth

Reasoning step by step and finally output the proof:
From sent13 & sent24, we can infer that a bird is a kind of organism (int1);
From int1 & sent2, we can infer that if a fossil of a bird cannot be identified then that kind of bird is
probably extinct (hypothesis);
Proof: sent13 & sent24 -> int1: a bird is a kind of organism; int1 & sent2 -> hypothesis;

               Table 9: Prompting template of stepwise proof generation for GPT4 with COT.
A.5   Selection of Enhanced Hard Negatives
Besides randomly selecting premises to construct
enhanced hard negatives, we also select according
to the top similarity score calculated with BM25
(Robertson et al., 2009). Results are presented in
Table 10. The results show that similar distracted
premises do not contribute to intermediate node
accuracy as much as random premises do. This is
because randomly selected premises can introduce
more diversity for the constructed hard negatives.

A.6   Case Study
We present a case study comparing the genera-
tion capabilities of LLaMA 3.2-1B and Flan-T5-
Large to illustrate the differences between encoder-
decoder and decoder-only LLMs, as shown in Ta-
ble 11. The table indicates that LLaMA (without
stepwise training) generates longer proofs because
it is trained with complete proof chains. In con-
trast,LLaMA (with stepwise training) typically pro-
duces one-step proofs that conclude with either a
"hypothesis" or an "intermediate node," reflecting
the fact that both are endpoints in the sequences
used for stepwise training. Flan-T5-Large (with
stepwise training) strikes a balance between gener-
ating long and short proof chains due to its encoder-
decoder architecture. However, it still faces chal-
lenges in accurately selecting premises.
                                  Leaves               Steps          Intermediates    Overall
                  Method
                            F1     AllCorrect   F1      AllCorrect   F1 AllCorrect    AllCorrect
                  Random   91.0       60.6      50.7      37.4       70.7   38.2        34.7
                  BM25     90.8       60.3      50.3      36.8       68.8   37.9        34.7

   Table 10: Ablation study of enhanced hard negative construction on EntailmentBank test set on Task 2.




Hypothesis: as the distance of the star to earth decreases, the star will appear brighter.
Context:
sent1: a star produces light and heat
sent2: far is the opposite of close
sent3: as the distance from an object increases , the force of gravity on that object will decrease
sent4: brightness means amount of light
sent5: if two or more things are in a relationship then those things impact each other
sent6: feature is synonymous with characteristic
...
sent25: moving away from the source increases the distance

Gold Proof: sent1 & sent13 -> int1: a star is a source of light; int1 & sent21 & sent23 -> hypothesis;
LLaMA-3.1-1B(w/o stepwise): sent13 & sent1 -> int1: stars are a source of light; int1 & sent21 -> int2:
as the distance of a star to earth decreases, the star will appear brighter; int2 & sent7 -> hypothesis;
LLaMA-3.1-1B(stepwise): sent21 & sent3 -> hypothesis;
Flan-T5-Large(stepwise): sent1 & sent13 -> int1: a star is a source of light and produces light; sent17 &
int1 & sent21 -> hypothesis;

                                 Table 11: Case study of LLaMA and Flan-T5.
