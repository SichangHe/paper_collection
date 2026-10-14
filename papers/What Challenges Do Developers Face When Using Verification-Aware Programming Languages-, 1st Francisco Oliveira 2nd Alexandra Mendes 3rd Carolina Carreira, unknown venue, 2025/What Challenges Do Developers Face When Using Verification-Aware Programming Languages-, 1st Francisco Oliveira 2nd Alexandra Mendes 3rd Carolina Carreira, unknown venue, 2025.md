                                         What Challenges Do Developers Face When Using
                                           Verification-Aware Programming Languages?
                                              1st Francisco Oliveira                   2nd Alexandra Mendes                             3rd Carolina Carreira
                                              Faculty of Engineering           INESC TEC, Faculty of Engineering,                   Carnegie Mellon University
                                                University of Porto                    University of Porto                      INESC-ID & IST, University of Lisbon
                                                 Porto, Portugal                        Porto, Portugal                                  Lisbon, Portugal



                                           Abstract—Software reliability is critical in ensuring that the         Despite their importance, the adoption of VA languages is
                                        digital systems we depend on function correctly. In software           still low. The reason usually attributed to this is the level of
                                        development, increasing software reliability often involves testing.
arXiv:2506.23696v2 [cs.SE] 7 Sep 2025




                                                                                                               expertise required from the developers and challenges that they
                                        However, for complex and critical systems, developers can use
                                        Design by Contract (DbC) methods to define precise specifications      often face when trying to prove a program correct. Previous
                                        that software components must satisfy. Verification-Aware (VA)         work identifies some challenges when using these tools, such
                                        programming languages support DbC and formal verification              as the lack of counter-examples [47], lack of clarity of the
                                        at compile-time or run-time, offering stronger correctness guar-       error messages [42], and a general difficulty in understanding
                                        antees than traditional testing. However, despite the strong           why proofs fail [24]. However, to the best of our knowledge,
                                        guarantees provided by VA languages, their adoption remains
                                        limited. In this study, we investigate the barriers to adopting VA     no previous studies have been made to systematically collect
                                        languages by analyzing developer discussions on public forums          the challenges and struggles that VA language developers face.
                                        using topic modeling techniques. We complement this analysis              In this paper, we aim to identify challenges usually encoun-
                                        with a developer survey to better understand the practical             tered when using VA languages with the aim of supporting VA
                                        challenges associated with VA languages. Our findings reveal           language, verifier, and IDE designers to improve the developer
                                        key obstacles to adoption, including steep learning curves and
                                        usability issues. Based on these insights, we identify actionable      experience and, hopefully contribute to a wider adoption.
                                        recommendations to improve the usability and accessibility of VA          We conducted a literature review to identify challenges in
                                        languages. Our findings suggest that simplifying tool interfaces,      the use of VA languages that are documented in the literature
                                        providing better educational materials, and improving integra-         and used topic modeling, in particular Latent Dirichlet Alloca-
                                        tion with everyday development environments could improve the          tion (LDA) [9], to extract challenges from developer posts on
                                        usability and adoption of these languages. Our work provides
                                        actionable insights for improving the usability of VA languages        Stack Overflow. This was followed by a user study to validate
                                        and making verification tools more accessible.                         the identified challenges and improvements that can be made
                                           Index Terms—Formal verification, Verification-Aware pro-            to VA languages to improve adoption and user experience.
                                        gramming languages, Software reliability, Usability, Topic mod-           We address the following research questions:
                                        eling, Developer survey, Programming languages                               RQ1: What challenges do verification-aware language
                                                                                                               practitioners face?
                                                               I. I NTRODUCTION                                      RQ2: What is the context of the first contact with
                                           In today’s world, software is integral to almost every aspect       verification-aware languages?
                                        of our lives, from personal communication and entertainment                  RQ3: What improvements can be made to existing tools
                                        to critical systems like air traffic control and IoT devices. As       to overcome those challenges?
                                        software becomes increasingly prevalent, ensuring its reliabil-        Contributions. The main contributions of this work are:
                                        ity is essential. The importance of reliability is even greater            • A collection of challenges that affect VA language devel-
                                        when considering critical applications where failures can be                 opers, obtained through a literature review and the anal-
                                        life-threatening and cause extensive damage [38], such as                    ysis of 1,420 questions from Stack Overflow, validated
                                        financial damage and risk users’ privacy.                                    and complemented by a user study with 31 practitioners.
                                           Verification-aware (VA) languages and systems, such as                  • An overview of practitioners’ first contact with VA lan-
                                        Dafny [34], VCC [13], Why3 [20], and Verus [32], go be-                      guages.
                                        yond traditional programming languages by integrating formal               • A collection of suggested improvements, validated by
                                        verification capabilities directly into the development process.             beginner and experienced VA language practitioners, that
                                        These languages enable the verification of program correctness               can inform language, verifier, and IDE designers.
                                        against user-defined specifications or contracts, using formal
                                        methods to mathematically prove that a program adheres to                                   II. S TUDY D ESIGN
                                        its specification. This built-in verification makes it possible to       We used a three-step approach as shown in Figure 1. In
                                        detect bugs early in the development cycle, offering a higher          Step 1, we performed a literature review to understand the
                                        degree of assurance about software correctness and safety.             context in which practitioners apply VA languages and the
                Literature Review                                   Q&A Topic Modeling                                  User Study


                 Database                                                                                 1420       Recruitment
                  search                                                                                Questions


                1024 papers                                                                                            13 Experts              Quantitative Analysis
                                                                      LDA topic modeling          Pre-processing          +
                                                                                                                           +
                                                                                                                       18 Beginners             Qualitative Analysis
                 Duplicate           Manual           Final                           Human-in-the-loop:
                 Removal            Screening        Analysis                  manual assignment semantic labels
                    723                600              9                                                            Validation of challenges and improvements
                                                                                                                                                          RQ1    RQ3

                              Developer challenges                         Topic-based challenge taxonomy                             Context of usage
                                                            RQ1                                                RQ1                                               RQ2




                                                        Fig. 1. Overview of the three-step research methodology.



challenges that arise from their use. Step 2 consisted of                                  the previously identified ones. We only accepted articles with
topic modeling, in particular using Latent Dirichlet Allocation                            ten or fewer years because, considering we are trying to
(LDA) [9], to extract challenges from developer posts on Stack                             understand developer practices and challenges, older articles
Overflow. Finally, Step 3 consisted of a user-study to validate                            could contain issues already addressed or outdated. We also
the challenges collected in the previous two steps, to explore                             included in the query the set of VA languages identified in
first contexts of users’ contact with these languages, and to                              Section II-A. The resulting query is as follows:
explore potential improvements. Steps 1, 2, and 3 contribute                                      ( "theorem proving" OR "theorem proof"
to answering RQ1. Step 3 contributes to answering questions                                        OR "deductive verification" OR "deductive methods"
                                                                                                   OR "formal verification" OR "formal specification"
RQ2 and RQ3.                                                                                       OR "contract programming" OR "design by contract"
                                                                                                   OR "programming by contract" OR "Bandera" OR "Dafny"
A. Verification-Aware Languages Considered                                                         OR "Escher C Verifier" OR "Eiffel" OR "Frama-C"
                                                                                                   OR "Java PathFinder" OR "JML" OR "mbeddr" OR "Spec#"
   We consider as VA programming languages those that                                              OR "Spark Ada" OR "VeriFast" OR "VCC" OR "Whiley"
                                                                                                   OR "Why3" )
natively support constructs for automated program verification,                                   AND industr*
such as pre-conditions, post-conditions, and invariants. For                                      AND ( challeng* OR issue* OR drawback? OR constraint?
                                                                                                        OR limitation? OR obstacle? OR difficult* )
our search queries, we defined a set of VA languages to be
considered, which resulted from a search of Verifiable Pro-                                   The query only searches in the field Abstract because it is
gramming Languages used in industry taken from the Formal                                  the field that all databases support. The queries were conducted
Methods Europe Industry Committee’s website,1 consulted                                    on 26/12/2023, resulting in 1024 articles. After 729 duplicates
on 20/11/2023. The languages that did not comply with our                                  were removed, 600 articles were screened.
definition of VA languages were removed.                                                      The following exclusion criteria were applied. These aim
   Following a three-person analysis of the technologies                                   to include the maximum number of relevant articles. When
listed, we arrived at the following set: Bandera [14],                                     in doubt, the full-text screening was applied. Title Screening:
Dafny [34], Escher C Verifier [19], Eiffel [36], Frama-C [15],                             1) the title is not related to formal verification (or derived
Java PathFinder [26], JML [33], mbeddr [49], Spec# [7],                                    terms) — e.g. “Solidification Principle in Large Vertical Steel
Spark Ada [6], VeriFast [28], VCC [13], Whiley [39], and                                   Casting Under the EMS Effect”; 2) the title mentions formal
Why3 [20]. Although KeY [2] was considered a VA language,                                  verification tools that are not VA languages — e.g. Alloy,
it was later removed as it introduced significant noise due to                             SysML. Abstract Screening: 1) the term formal methods or
the name’s generality, including, e.g., results from security.                             related is used in contexts not related to our research —
                                                                                           e.g. formal verification of startup models; 2) the tools or
B. Literature Review
                                                                                           formal verification methods mentioned are related to the area
   To understand from existing work what challenges are faced                              of software engineering, but the application area is not aligned
by practitioners when using VA languages, we performed a                                   with the our research — formal verification of system models.
literature review. Next, we present all the steps followed.                                Full-Text Screening: 1) the article does not mention any
   We queried the ACM Digital Library, IEEE Xplore, Scopus,                                challenges; 2) the challenges are not related to the application
and Web of Science. The research query was developed                                       of VA languages (e.g., the article talks about the challenges
following an iterative methodology. Firstly, we identified the                             of integrating Dafny with Solidity).
following relevant articles that we would like to find with                                   After this process, nine of the 600 articles were considered
our research query: [27], [37], [42], [47], [50]. Then, we                                 relevant and were analyzed (see III-A), highlighting a signifi-
developed an initial search query based on keywords from                                   cant research gap and reinforcing the relevance of this study.
the collected articles. The resulting query was then tailored
                                                                                           C. Stack Overflow Q&A Study
to find as many articles as possible, while also containing
                                                                                             This section details how we extract challenges from de-
 1 https://fme-industry.github.io/                                                         veloper posts on Stack Overflow, a widely used Q&A plat-
form where developers from diverse backgrounds openly dis-           snippets and tags (similar to [21] and [5]). With that in mind,
cuss real-world programming problems at scale, making it             we built four pre-processing pipelines, with each pipeline
a rich and authentic source for empirical studies [1], [3],          combining a subset of the following nine steps.
[4], [8], [18], [25], [40]. However, manually analyzing the          Pre-processing steps. Based on prior research, we considered
vast amounts of data available in these sources may become           the following nine pre-processing steps:
infeasible, particularly as the dataset size increases. Therefore,       •    remove code: Removes all tags and code snippets from
we use topic modeling, a popular analytical tool for evaluating            the body of a given question, wrapping it into a div tag,
data, as an approach to identify groups of similar words,                  and then performing a depth-first search into its children,
or topics, within the text [48]. One of the most popular                   removing all code and pre tags. Only the inner text of the
algorithms for topic modeling is Latent Dirichlet Allocation               other tags, such as anchor, strong, paragraph, etc, and
(LDA) [9], an unsupervised machine learning algorithm that                 text that is directly a child of a given tag is kept. The
models automatically extracted topics in corpora. It is based              resulting text is then trimmed and joined with a white
on the idea that each document is a mixture of topics, and each            space. Based on [8], [4], [25], [3], [18], and [40].
topic is a mixture of words. LDA aims to discover how much               •    gensim preprocessing: Performs common pre-
of each topic is in each document and how much of each word                processing tasks using the functions strip numeric,
belongs to a particular topic. The algorithm outputs probability           strip multiple whitespaces, and strip punctuation from
distributions that quantify the proportion of each topic within            the Gensim5 library. This step removes digits from the
a document and the association of each word with a given                   initial string and multiple consecutive white spaces,
topic [45]. Several previous studies have used unsupervised                leaving just one separating the words. Finally, it strips
machine learning, in particular LDA, for categorizing forum                all the punctuation from the input string. Based on [4],
posts [1], [3], [4], [8], [18], [25], [40].                                [25], [3], [18], and [40].
   Our forum post analysis with topic modeling follows prior             •    lemmatize body: Starts by tokenizing the input string
work and involves four steps: a) collecting Stack Overflow                 using NLTK’s word tokenize function. After tokenizing,
data on VA languages, b) pre-processing (cleaning, stop-word               we apply stemming using NLTK’s WordNet lemmatizer.
removal, stemming/lemmatization), c) training an LDA model,                This lemmatizer needs to receive the part of speech of
and d) labeling tags based on associated words and topics.                 each word. Since identifying specific parts of speech is
      a) Data Collection: Three popular Stack Overflow post                out of the scope of our work, we decided to consider
datasets are: SO official data dumps [21], SOTorrent [5], and              every word as a verb since we found that verbs and plural
SE Data Explorer.2 The first is distributed as a very large                nouns were transformed into their stems. Based on [25].
XML file, which we found difficult to process; the second                •    remove stop words: Filters out stop words using the
is not updated since 2020; and the third is available through              NLTK stop words corpus (e.g., a, an, the, of, and). This
a human-centered interface, making it difficult to automate                is an approach used by [25], [1], and [40].
data collection. Therefore, we used the official Stack Exchange          •    transform bigrams: Takes a list of words and returns a
API3 as, similarly to SE Data Explorer, it provides the newest             list of bigrams using NLTK bigrams function. This step
data at the time of querying, but in a computer-friendly format.           was also used by [1], although the authors used Gensim
   We identified the tags we would use to query the API                    to build the bigrams.
endpoint and settled with a variation of a list of VA languages          •    make lower case: Transforms all words into their low-
presented in Section II-A. From our observations of the Stack              ercase version.
Overflow tag list,4 only hyphenated tags are supported, so               •    remove handpicked: Removes words that, after exam-
“Escher C Verifier”, “Java PathFinder”, and “Spark Ada” had                ination, we considered as not adding value to the trained
to be transformed to accommodate this requirement. In the                  model — e.g., also, always, etc, like (full list available
final mapping between VA language names and the tag names,                 in the supplementary material). Based on [3] and [40].
“Escher C Verifier”, “Java PathFinder”, and “Spark Ada”                  •    remove uncommon: Removes words with less than
became “escher”, “pathfinder”, and “spark-ada”, respectively.              three uses since these words can not form patterns.
   Moreover, we decided only to query the /questions endpoint            •    remove small: Removes words with less than two
because we are looking for challenges commonly found in                    characters since we considered that words with that size
questions but not in the answers and comments.                             could not express meaningful value.
   We ended up with 1420 questions, most of which were about
                                                                     Pre-processing pipelines. After collecting the data, we pro-
Dafny and Frama-C. The distribution of questions was Dafny:
                                                                     cess the questions using the four pre-processing pipelines
530, Frama C: 474, Eiffel: 289, Spark Ada: 55, Why3: 52,
                                                                     listed below, developed as a combination of the nine steps
JML: 44, and Spec#: 16.
                                                                     listed previously. All the pipelines are based on [25] because
      b) Data Pre-processing: Since we gathered data from
                                                                     they lemmatize the words before removing the stop words.
the Stack Exchange API, the question bodies contain code
                                                                       1) baseline: This pipeline is the simplest and produces
  2 https://data.stackexchange.com/
                                                                           a list of individual words. The exact sequence of the
  3 https://api.stackexchange.com/
  4 https://stackoverflow.com/tags                                     5 https://radimrehurek.com/gensim/
      steps is:     remove code →         gensim preprocessing       be quickly calculated. We also analyzed the logarithm of the
      →       lemmatize body →          make lower case         →    perplexity, which measures how likely an outside observer is
         remove stop words.                                          to predict the values drawn from a model. The values used are
  2) baseline bigram: Create bigrams from the list of words          the output of the function log perplexity7 in Gensim.
      resulting from the baseline pipeline. Based on the work            We trained a model for each combination of pre-processing
      by [1]. The steps are: baseline → transform bigrams.           pipelines and hyperparameters. The performance of each com-
  3) rem words baseline: Similar to the regular baseline             bination (pipeline × combination of hyperparameters × 4
      pipeline but incorporates the innovation of [3] and [40] of    models) was assessed by calculating the average coherence and
      removing domain-specific words as well as an additional        perplexity scores, as well as their standard deviations across
      removal of words with less than three uses — since these       the four models. This allowed to identify configurations that
      words can not possibly form patterns — and less than two       were not only high-performing but also consistent. Configura-
      characters — since we considered that words with that          tions with high standard deviations were considered unstable.
      size could not express meaningful value. The sequence is:      Taking into consideration LDA’s non-deterministic nature, this
      baseline→ remove handpicked → remove uncommon                  strategy allows us to detect if a score is exceptionally good
      → remove small.                                                or if the hyperparameters are able to make LDA consistently
  4) rem words bigram: Based on the rem words baseline               output good models.
      but, similarly to baseline bigram, ends with a step that           The baseline and baseline bigram pipelines resulted in con-
      transforms the resulting list of words in a list of bigrams.   figurations with significantly high standard deviations in coher-
      Steps: rem words baseline → transform bigrams.                 ence, indicating instability. The rem words baseline pipeline
      c) Model Training: To configure the LDA algorithm,             showed better overall performance and, unlike baseline, it re-
several parameters, known as hyperparameters, must be set:           moved words that were not helpful for identifying challenges.
the number of topics (K); the number of iterations (i.e.,            The rem words bigram pipeline generally showed higher
optimization steps); the number of passes over the training          degradation in coherence compared to rem words baseline.
corpus; to what extent questions mix topics (α) — a high value       Based on this initial analysis, the rem words baseline was
means that questions cover a wide range of topics; and to            chosen. A configuration with 16 topics within this pipeline
what extent questions mix words (β) — a high value means             was initially selected for further consideration.
that topics are likely to contain a broad range of words, rather         As further explained in II-C0d, questions with low proba-
than being focused on a small, specific set of terms.                bility of belonging to a topic were discarded and open card
   Each of the four pre-processing pipelines presented in the        sorting [46] was performed based on the top 30 words and
previous subsection was tested against each combination of           top 20 documents for each topic. Looking at the composition
the following hyperparameters: K ranging from 2 to 40 in             of the topics, we obtained 209 unique questions from the 320
steps of 2 to capture all identified challenges, and from 500        that were assigned to the 16 topics. Most questions appeared
to 3000 in steps of 500 to align with prior work; we also tried      only once, indicating diverse topics.
50 iterations, the Gensim default. We set the number of passes           After applying open card sorting to the clustered questions,
at 1 (Gensim default) and 5 (as per [25]). For β, we tested          we obtained the tag distribution depicted in Figure 2. The most
0.1, 0.01, and None (Gensim default), while α followed the           frequent tag is the not-suited tag with 79 questions, meaning
common formulation α = 50/K from prior studies [3], [4].             that around 38% of questions were considered inadequate
Final Model. We select the final model configuration through         to answer RQ1. Of the 16 resulting topics, in 15, the most
an evaluation across multiple training runs and criteria, which,     frequent tag was not-suited, indicating that the topics are not
due to space limitations, we briefly detail below. More details      representative of any challenge.
can be found in the supplementary material.6                             To overcome this issue, we decided to filter out these ques-
   This process began with an initial training run using the         tions and run the training in a dataset without the 79 inadequate
full dataset of collected Stack Overflow questions. This run         questions. A second training run was then done using the
aimed to evaluate the performance of different pre-processing        filtered dataset. Again, we applied the four pre-processing
pipelines and model configurations. This produced: 4 model           pipelines and explored various hyperparameter configurations
runs, one for each pipeline; 840 model configurations resulting      and used the same evaluation metrics as in the first training
from the combination of LDA hyperparameters; and 3360                run. Similar performance patterns to those obtained in the first
models, four for each configuration. To account for the non-         training run were observed across the pipelines, with base-
deterministic nature of the LDA algorithm, we trained four           line, baseline bigram, and rem words bigram showing high
models for each combination of the hyperparameters.                  errors. The rem words baseline pipeline again demonstrated
   Model performance was evaluated using two primary met-            consistent performance for configurations filtered by lowest
rics: topic coherence (CU M ass ) [41] and perplexity score          error. Considering the similar performance, we again chose
(logarithm of perplexity) [9]. We decided to use CU M ass to         the rem words baseline pipeline to pick the best configuration
evaluate our models since it is a standard metric that can
                                                                       7 https://radimrehurek.com/gensim/models/ldamodel.html#gensim.models.
  6 https://figshare.com/s/bc220b6c300b46c97d89                      ldamodel.LdaModel.log perplexity [last access 31st August 2024]
                                     Fig. 2. Frequency of each tag (initial training)                             probabilities greater than the random assignment.
                                  80 79                                                                              After filtering the questions with low probabilities, we
                                  75                                                                              sorted them and performed open card sorting [46] based
                                  70
                                  65                                                                              on the top 30 words and top 20 documents for each topic.
                                  60                                                                              The labeling for each topic was discussed among the team
                                  55
            Number of Questions



                                  50                                                                              members until a consensus was reached.
                                  45                                                                                 For the final chosen model configuration, which had eight
                                  40       36
                                  35                                                                              topics, the labeling process involved analyzing the frequency
                                  30          27                                                                  and distribution of the tags that were created during the open
                                  25
                                  20             19                                                               card sorting process.
                                  15                14 14 13
                                                             11 10 10 10                                             For Topic 0, even though the most common tag is not-suited,
                                  10                                     8 8
                                   5                                         5 3 3 3                              the label Memory Model Understanding was assigned, influ-
                                                                                     2 2 1
                                   0
                                                                                                                  enced by the second most common tag, heap-understanding.
            heandi roof-owleited
         co und -und-beh atege
        lac figuerstaerstaavio y
            kin rat nd nd ur
                g-d ion -fa ing
                   da umeardsres



                 ur- ve t-deriant
                                   n
                 rfo ili ste g
                       fny nt hip
                    loo logi emo n
                                   r




                        - - ry

                             em tic
                                ory
                             c- ry




      flo arrframmancy-iss cy
             ng -re c-m iss s
                -po la e ue

                         a-m me r
          ha ontra-invaerro




                      adarith orde
          ati ay a- e- ue
               ap ng str dg




                           -m atio



                    inc rifi sig
              pe sab nsi r-bu



                     int tive mo
                     r t n
                                                                                                                  Topic 1 was labeled Language Understanding, driven by
                    oc -h ilu
            rst p kn su




                             e
        de ture- not-




                           c
                         o
                        p




                                                                                                                  the frequency of the lack-feature-knowledge and understand-
                  u
                  c
               ea




             vio




                                                                                                                  behaviour tags, and the occurrences of logic-error, loop-
           k-f




           n
     lac




      be
                   un




                                                                                 Tag Names                        invariant, understand-failures, and lacking-documentation.
                                                                                                                  Topic 2 was labeled Not Suited because no clear relationship
                                                                                                                  between the clustered questions was found. Topic 3 was la-
                                      Fig. 3. Frequency of each tag (second training)                             beled Environment Setup as most of the questions are related
                             30
                                        28                                                                        to to the configuration-hardship tag. Topics 4 and 5 were
                                             26
                                                  25                                                              labeled Non Relevant as no clear relationships were found
                             25
                                                                                                                  between the top question label. Topics 6 and 7 were labeled
                             20                                                                                   Proof Elaboration, because both contain many questions re-
       Number of Questions




                                                                                                                  garding the label proof-strategy and some questions regarding
                                                       15 15
                             15                                14                                                 loop-invariant. These labeled topics were then used to identify
                                                                    10
                                                                                                                  broader categories of challenges, which are presented in the
                             10                                          9                                        Section III-B.
                                                                             8
                                                                                  7 7
                                                                                        5 5 5
                                  5                                                                               D. User Study
                                                                                                3 3
                                                                                                      2
                                                                                                          1 1 1
                                  0                                                                                  To better understand the challenges faced by VA language
                                                                                                                  users and assess the relevance of the issues identified in our
         lacheapcont -behrdsh s
      unconfinderre-knstratited
            rst ra nd le y
                  din n-h ilu e


                    oc rst esig r
                       um an n
                    loo logi tatiog



       beating rfor a-c-m-issuug




                                 ory
            kin -un rac av ip



                   da -in c-er n
                      fny va ror
                  us ver emant



             arr ur-int-ari e-issory

                     ad tive-tencc
       flo p fram bilit fier-bory
           ha -p ma e es

                 ay co thm ue

                         a-m or y
                             emder
                g-d de t-d iou
                      g a re




                       la is ti
         de gu sta ow eg
               an tio -fa dg




                           en din




                   -re ns e
             vio oin nc m
                          -m ri
             u atu oof- t-su




                                                                                                                  prior qualitative analysis, we conducted an online survey study.
                           y
               e r o




                           i
            k-f p n




                        p

                     a




                                                                                                                  We designed the study to capture both quantitative and qualita-
                e




                                                                                                                  tive feedback, drawing on the experiences of participants with
        lac




                                                                             Tag Names                            different levels of familiarity with VA languages. We provide
                                                                                                                  the full protocol in the supplementary material.
                                                                                                                     1) Survey Design: We start the survey with a section about
and model. We chose the configuration with eight topics                                                           background information, where we ask about familiarity with
because it resulted in a number of topics that allowed for the                                                    VA languages and years of experience. We also ask about
identification of challenges consistent with prior literature, as                                                 participants’ initial contact with VA languages and how they
discussed in Section III-A. Looking at the topics, we observe                                                     learned to program with them. We then attempt to validate
these are composed of 160 questions, from which 145 are                                                           the answers to RQ1. We use matrix-style questions with a 5-
unique. This indicates that this model is diverse.                                                                point Likert scale to ask questions about challenges related
   After performing open card sorting, we end up with the tag                                                     to Proof Elaboration and Environment Setup. We also ask
distribution shown in Figure 3. Despite being the most popular                                                    participants about a subset of language-agnostic challenges
tag, the not-suited questions only comprise 19% of the overall                                                    identified in Section III-B and language-specific challenges
questions against the 38% obtained in the initial training run.                                                   with Dafny and Frama-C. We only showed these sections
Based on our analysis, we decided that this model was suited                                                      to participants who mentioned having experience with these
for naming and challenge identification.                                                                          languages. This part of the survey mainly targets Dafny and
      d) Topic Labelling: This process involved analyzing the                                                     Frama-C practitioners because over 70% of the questions
chosen model configuration’s output. Questions were filtered,                                                     found in Stack Overflow were related to these specific lan-
discarding those where the probability of belonging to a topic                                                    guages and some challenges are language dependent.
was less than n1 (where n is the number of topics). The                                                              We ask two open-ended questions about additional chal-
reasoning for this was that n1 is the probability of randomly                                                     lenges not identified in the previous parts of the study and
assigning a document to a given topic, thus we only accepted                                                      suggestions for improving the adoption of VA languages.
Then, we use a matrix-style closed-ended question to ask about
the suggestions we developed a priori. We asked open-ended                                     TABLE I
                                                                         OVERVIEW OF PARTICIPANT DEMOGRAPHICS AND EXPERIENCE
questions before the closed-ended to prevent bias and allow
the participants to think more freely without being conditioned                                       Beginners   Experienced   Total (%)
by the options they had already seen.
                                                                    Gender
   2) Recruitment: Our sample had a total of 31 participants.       Male                                    14            11       80.6%
We recruited participants using our social media, professional      Female                                   4             1       16.1%
network, and snowball sampling. We began by distributing            Prefer not to say                        –             1        3.2%
the survey to 15 students of the 2023/2024 edition of the           Age
                                                                    18–24 years                             15             1       51.6%
Formal Methods for Critical Systems course, an optional first-      25–34 years                              3             2       16.1%
year Master’s level course from the Faculty of Engineering,         35–44 years                              –             7       22.6%
University of Porto. Using Proxycurl,8 we gathered 28 profiles      45–64 years                              –             3        9.7%
of LinkedIn users from the US with software and formal              Highest Education Achieved
verification skills, contacted 16 industry professionals from our   Some college, no degree                  2             –        6.5%
                                                                    Associate’s or technical degree          –             1        3.2%
professional network, and 26 Dafny contributors on GitHub,          Bachelor’s degree                       14             1       48.4%
whose contact information was public. Additionally, we shared       Graduate/professional degree             2            11       41.9%
our survey on social media through X.9 We used snowball             Race
sampling by asking our contacts to distribute the survey to         Asian                                    1             1        6.5%
relevant members of their professional and student networks.        Black                                    4             –       12.9%
                                                                    White                                   12             8       64.5%
We also distributed the survey through Frama-C’s mailing list.      Prefer not to say                        1             4       16.1%
We divide participants by years of experience: more than three
                                                                    Currently Employed in CS
are considered experienced, all others are beginners.               Yes                                      7            13       64.5%
   All participants were over 18 years old and provided in-         No                                       9             –       29.0%
                                                                    No, but have been in the past            2             –        6.5%
formed consent after reviewing a form with the study’s pur-
pose, procedures, and their rights. Participants were informed      Formal CS Education
                                                                    Yes                                     18            11       93.5%
that they were not required to participate and could withdraw       No                                       –             2        6.5%
at any time without penalty. No personal or identifiable data
                                                                    Total Participants                      18            13       100%
were collected.
   Sample. Most of our sample identify as male and are
employed in the computing field with formal education. Most
experienced participants have some graduate or professional         initial coder designed the first version of the codebooks that
degree, while most beginners only have a bachelor’s degree.         both coders used. This first codebook was developed with
See Table I for complete demographic information.                   prior knowledge of the types of challenges identified in an
   3) Quantitative Analysis: For our quantitative data, we use      earlier portion of the study. After completing the first pass, the
the Mann-Whitney U test to check whether the data from              codebook was refined, and the coders met to discuss the added
two groups, beginners and experienced, differ significantly. We     and modified codes. Following these updates, both coders
chose a non-parametric test because our data does not follow        independently applied the revised codebooks to the dataset
a normal distribution. We use a Friedman test to compare            in a second round of coding. After this, the coders met to
answers to statements within the same group. If the Friedman        resolve discrepancies in their coding and reached a consensus.
test is significant (p < 0.05), we then use the Wilcoxon signed-    The process resulted in two finalized codebooks: one for
rank test to make pairwise comparisons of each statement            suggested improvements, consisting of 13 codes, and another
and understand which particular statements are significantly        for challenges, consisting of 14 codes. Each participant’s
different from the others. Finally, we analyze the frequency        response could have up to 5 different codes.
of each response to understand if the participants encountered
the challenge. To analyze Likert scale data, we remove the Not          III. W HAT CHALLENGES DO V ERIFICATION -AWARE
Sure responses from the statistical test, assuming that these                LANGUAGE PRACTITIONERS FACE ? (RQ1)
were due to the participant not understanding the statement.
                                                                    A. Findings from Literature Review
   4) Qualitative Analysis: Most of our survey consisted of
closed-ended questions. However, we asked two open-ended               From the existing literature, we identified several chal-
questions about challenges and possible solutions to chal-          lenges, such as: behavior dependent on previous executions,
lenges. We used deductive and inductive coding to analyze           which include challenges related to the verification of prop-
the qualitative data derived from these questions. Two coders       erties where the behavior is influenced by previous execu-
did two independent rounds of coding. In the first round, the       tions [17], [23]; behaviour inconsistency, as verification suc-
                                                                    cess changes depending on the solver [47]; cost of applying VA
  8 https://nubela.co/proxycurl/                                    languages [50]; feedback quality, which includes the lack of
  9 https://x.com/                                                  counter-examples by some tools [47], the lack of clarity of the
error messages [42], and a general difficulty in understanding       to dependency installation, which were identified in four
why proofs fail [24]; handling boolean values, i.e. challenges       questions. It includes challenges related to missing dependen-
related to verifying properties about boolean values [16], [23];     cies, incompatible dependency versions, and dependencies not
imprecise specifications [23], [30]; increasing the scale of ver-    being found. The other two classes of challenges are related
ification, which includes challenges related to the integration      to unsupported use cases and missing installation instructions.
of multiple verified functions [30], the scaling of verification     These challenges are represented by one question each.
time [16], the difficulty of tracking and maintaining anno-                c) Memory Model Understanding: The challenges in
tations [16], [27], and general claims about scalability [37];       this topic are language-specific, as we observed that languages
integration with hardware, including difficulties related to the     where the user manually manipulates the memory, like C, have
verification of functions that interact with hardware, often         different challenges than garbage-collected ones, like Dafny.
resulting in side effects [17]; integration with other tools [27];      We identified three challenges among Dafny programmers,
lack of features to support verifying some behaviors [30], [43];     all related to the modifies clause. The modifies clause specifies
lack of verified APIs [27]; lacking support for specific tasks,      the set of memory locations that a method, iterator, or loop
such as lack of support for floating-point arithmetic [27], [37],    body may modify [35].
concurrent software [27], and reflection [27] verification; loop        The first challenge is related to the user applying a modifies
invariant discovery [24], [42]; need for automation, which           clause to a given memory location, holding a reference to an
includes the need for automation so that deductive verification      object within the scope of a method, but only changing the
can be widespread [37]; insufficient [27], [42], [47] and costly     properties of the given object inside a loop. Dafny assumes that
[27], [50] support and documentation; switching costs, which         the loop might change the object to which the memory location
includes authors that considered the lack of interoperability        is pointing, thus making verification based on the previously
between tools and the cost to switch them an obstacle for            set object properties impossible. The programmer must create
the adoption of VA languages [50]; and type conversions,             an invariant saying that the memory location always points to
including challenges related to the verification of implicit [23]    the same object.
or heterogeneous [16] type conversions.                                 The second challenge is related to programmers not under-
                                                                     standing which variables are affected by the modifies clause,
B. Findings from Stack Overflow Q&A Study                            identified in two questions. In both, we see that the authors
   In this section, we group the identified challenges by the        fail to acknowledge what is the right target of the modifies
four topics identified in II-C0d. Due to space restrictions, full    clause when the target property is a memory location to an
details can be found in the supplementary material.                  object: one author is missing a modifies this clause; the other
      a) Proof Elaboration: The challenges in this class are         tries to modify a property of the class while using modifies
related to the programming paradigm, so these are language           this instead of including modifies this.property name.
agnostic. The first challenge is related to creating a proof            In another question, we observed a similar challenge, but
strategy. In many questions, authors could not even start            the clause the author is using is the reads clause. The reads
the proof, not knowing what proof strategy to choose. This           clause marks all the heap memory locations the function is
challenge was observed in nine questions.                            allowed to read [35].
   The second challenge is related to completing a proof.                  d) Language Understanding: Similarly to the previous
In contrast with the previous challenge, these authors could         topic, most of the challenges in this topic are related to features
start to design a proof strategy that then proved impractical        that are language-specific, related to Dafny, and to the Frama-
in verifying the properties of the code. This challenge was          C WP Plugin, which uses ACSL as an annotation language.
observed in three questions.                                            For Dafny, in one of the questions, the author seemed to
   The third challenge is related to authors who chose a non-        lack knowledge about partial functions. The second ques-
ideal strategy to prove the properties of the code; for example,     tion is about the fuel attribute in Dafny using an example
choosing a proof by induction when a proof by contradiction          function. Another question concerns an author that fails to
would be easier. This was observed in one question.                  understand the error message provided by the verifier about
   The fourth challenge concerns identifying and expressing          a type definition. Upon further inspection, we considered
the necessary loop invariants to verify loops. This challenge        the message self-explanatory for developers who knew about
was observed in five questions.                                      subset types and witnesses. In the final question, the author
   The fifth challenge, observed in one question, is related to      fails to acknowledge what constructs are opaque. In Dafny,
the fourth and concerns identifying and expressing a valid           when a construct is opaque, the verifier does not introspect it
decrease clause that proves that loops or recursion functions        to derive pre-conditions and post-conditions — the developer
terminate. This challenge was observed in one question.              must define the contract. In this specific case, the developer
   The sixth challenge concerns not being able to gather             forgot the constructor’s post-condition.
feedback, i.e., whether the contracts are respected due to the          Regarding the Frama-C questions, in one of the questions,
verifier timing out. This was observed in two questions.             the author is trying to use a feature defined in the ACSL
      b) Environment Setup: The challenges in this topic             Reference Manual but not implemented by the Frama-C WP
are language agnostic. The first class of challenges is related      Plugin. In another, the author wants to prove that, given
the same arguments, the function always returns the same                                        TABLE II
values using ACSL. The accepted answer claims that this                             P ROOF E LABORATION C HALLENGES
is impossible in ACSL. In the third question, the author is         ID      Challenge Description
trying to use a C11 specification feature not implemented by        P E1    Difficulty designing proof strategies accepted by the validator.
the Frama-C pre-processor at the time of writing. In the final      P E2    Difficulty completing designed proof strategies.
                                                                    P E3    Tendency to choose non-ideal proof strategies.
Frama-C question, the accepted answer claims that the author        P E4    Inability to identify necessary loop invariants.
fails to acknowledge the need for loop assigns in the presented     P E5    Inability to express necessary loop invariants.
loops. The question has some loop assigns expressions and           P E6    Inability to identify clauses proving termination.
                                                                    P E7    Inability to express clauses proving termination.
was edited 8 hours after creation, presumably to add them.
   The following questions are considered language agnostic.
In the first, the author wants to prove a lemma in Dafny.          and expressing (P E5 ) loop invariants and termination clauses
The original code of the author causes an internal error in        (P E6 and P E7 ) does not seem to be a problem for most.
Dafny 4.7.0. According to the accepted answer, an assertion              b) Environment Setup Challenges: While we do not
was missing to make the verifier accept the proof. Because         see a significant difference between beginners and experts,
the need for the assertion is probably tied to the internal        most developers did not encounter dependency conflicts when
verification mechanism, we considered that the proof elicits       installing verification tools with 67.7% agreeing this is not a
a lack of language understanding, namely, the underlying           problem. Similarly, the challenge of finding the correct version
verification mechanisms. In the second question, the author        of a verification tool compatible with a preferred IDE was not
is trying to understand the translation of mapping WhyML           common (77.4% did not consider this a challenge).
code into the SMT encoding to understand how the proofs                  c) Feature Knowledge Challenges: We do not see a
for ACSL annotated programs are provided. This question is         significant difference among experienced users. However, most
not a challenge but introduces a need for understanding the        developers, particularly beginners, struggled to understand
underlying verification mechanisms. The last question contains     how their high-level code is translated to the underlying SMT
a simple syntax error where the author does not use the correct    code, while more experienced developers felt confident in this
syntax to write comments in ACSL.                                  area. When it came to translating proofs from other mediums
                                                                   (e.g., paper) to the VA language, most developers did not
C. Findings from User Study                                        report significant difficulties. Experienced developers showed
      a) Proof Elaboration Challenges: In this section, we         relatively higher agreement with this challenge than beginners.
validate seven challenges related to Proof Elaboration. Of the           d) Dafny Challenges: Most participants did not face
seven challenges, presented in Table II, only P E7 , which         significant issues understanding the “modifies” and “reads”
addresses difficulties in expressing the necessary clause to       clauses or distinguishing between opaque and non-opaque
prove loop/recursion termination, had a significant p-value        statements. However, some developers still struggled with ex-
(p = 0.02666), this means that P E7 is the only PE challenge       pressing the immutability of variables, and many participants
significantly worse for beginners than experienced users. All      were unfamiliar with critical concepts like the fuel attribute,
other challenges had a non-significant p-value (p > 0.05) when     partial functions for reasoning about high-order functions, and
comparing beginners and experienced users.                         using witnesses to prove the non-emptiness of type definitions.
   To assess differences between the seven conditions across all         e) Frama-C WP Plugin Challenges: None of these
participants, we conducted a Friedman test. The results indi-      challenges had a significant p-value (p < 0.05) when com-
cate a significant difference between the conditions, chi2 (6) =   paring beginners and experienced users. Most developers felt
27.79, p = 0.0001. To assess these differences, we conducted       confident in their understanding of the different memory mod-
pairwise comparisons with a Wilcoxon signed-rank test with         els and their ability to choose the correct model for proving
Bonferroni correction (see Table III). The results indicate that   code properties and in selecting variables for “loop assigns”
there were significant differences between P E1 and P E7           statements. Some developers also identified missing features
(p = 0.023) and between P E2 and P E7 (p = 0.032). No              in Frama-C’s C specifications and noted that certain features
other comparisons reached statistical significance after the       available in other plugins were absent in the WP Plugin.
Bonferroni correction (all p > 0.05). This means that P E7 , the         f) Additional Challenges: The most frequently reported
challenge of expressing loop/recursion termination clauses, is     challenges were “Tool Performance Issues” and “Poor Er-
a significantly less important problem than P E1 — designing       ror Messages and Feedback,” each mentioned seven times.
proof strategies — and P E2 — completing proof strategies.         “Complex Language Features and Low-Level Operations” was
   Our results show that most developers struggled with de-        reported six times, followed by “Specification and Annotation
signing proof strategies (P E1 , 64.5%). The challenge related     Challenges” with five occurrences. Both “Understanding Ver-
to difficulty completing proof strategies (P E2 ) was more split   ifier Capabilities” and “Learning Curve” were identified four
with 48.4% agreeing that this is an issue for them and 22.6%       times each. Additional challenges included “Mindset Shift,”
disagreeing. When it comes to searching for the right proof        “Scalability and Large Project Integration,” and “IDE Inte-
strategies (P E3 ), we saw a similar split with 48.4% agreeing     gration,” each reported twice. The following challenges were
and 22.6% disagreeing it is a challenge. Identifying (P E4 )       identified once each: “Lack of Documentation,” “Conflicts
                                                             TABLE III
  PAIRWISE W ILCOXON SIGNED - RANK TEST RESULTS WITH B ONFERRONI CORRECTION FOR MULTIPLE COMPARISONS . *S IGNIFICANT AT ADJUSTED
                                                         p − value < 0.05.

                          P E1       P E2           P E3           P E4            P E5           P E6            P E7
                  P E1       -     95.5, 1.000   144.0, 1.000   172.5, 0.237    150.5, 0.093   207.5, 0.172    263.5, 0.023*
                  P E2       -          -         80.5, 1.000   143.5, 1.000    139.0, 0.368   169.0, 0.336    189.5, 0.032*
                  P E3       -          -              -        178.5, 1.000    148.5, 0.611   205.5, 0.811     184.5, 0.058
                  P E4       -          -              -              -          26.5, 1.000    60.0, 1.000      86.0, 1.000
                  P E5       -          -              -              -               -        104.5, 1.000      88.0, 1.000
                  P E6       -          -              -              -               -              -           49.5, 1.000
                  P E7       -          -              -              -               -              -                -



with Performance Optimization,” “Proof Stability,” “Transla-                                        TABLE IV
tion of Algorithms,” and “Lack of Proof Automation.”                        C HARACTERIZATION OF PARTICIPANTS BASED ON THE CONTEXT IN
                                                                          WHICH THEY FIRST LEARNED ABOUT VERIFICATION - AWARE LANGUAGES .


   RQ1: VA language practitioners most commonly face                             Context                                       Frequency
   challenges in designing and completing proof strate-                          Optional University Course                           22
   gies. The only challenge different between beginners                          Work Context                                         15
                                                                                 Online Discussions                                    3
   and experienced users was proving loop/recursion ter-                         Mandatory University Course                           2
   mination, though this issue was uncommon and signif-                          With university and enterprise colleagues             1
   icantly less important than the challenges of designing                       Self-learning                                         1
                                                                                 Was bored in high school                              1
   and completing proof strategies. Language-specific se-
   mantics (e.g., frame specifications, termination clauses)
   appeared on Stack Overflow but were not confirmed as
   challenges in our user study. While environment setup               participants learn about VA languages as a choice of education
   is less problematic, feature knowledge challenges were              or career path. Table IV summarizes the results.
   confirmed, with beginners struggling more with SMT                     When it comes to their experience programming with VA
   translation, and experienced developers with translating            languages, their responses were consistent with their first con-
   proofs to the VA language. We identified fourteen new               tact. Most participants reported learning how to program in a
   challenges, the most reported ones being “Tool Perfor-              university course (22 participants, 71%) and being self-taught
   mance Issues”, “Poor Error Messages and Feedback”,                  (14 participants, 45%). When considering only experienced
   “Complex Language Features and Low-Level Opera-                     users, 11 participants (85%) are self-taught and 10 participants
   tions”, and “Specification and Annotation Challenges”.              (77%) learned in a work context.
                                                                          These results suggest that beginners usually first encounter
                                                                       VA languages at university, while experienced developers
IV. W HAT IS THE CONTEXT OF THE FIRST CONTACT WITH                     do so in professional settings and increasingly through self-
      V ERIFICATION -AWARE LANGUAGES ? (RQ2)                           teaching. These insights highlight the need for differentiated
                                                                       learning resources: universities should integrate VA languages
   To understand the educational and professional pathways             into curricula for early exposure, while practitioners could
that lead individuals to work with VA languages, we asked              benefit from self-guided resources and community support.
all participants two questions, one about where they first
learned about VA languages and another about where they                      RQ2: The context of the first contact with VA lan-
learned to program with VA languages. In our sample, we                      guages seems to vary by experience level. Most begin-
have 18 beginners and 13 experienced programmers. Most                       ners first encounter VA language in university courses,
beginners had their first contact and learned VA languages                   while most experienced programmers are introduced
in an optional university course (16 participants, 89%), with                to VA languages in a work context. Moreover, as
the exception of two participants who had their first contact                users gain experience, self-teaching emerges as a key
in a work context. On the other hand, most experienced                       mechanism through which they acquire knowledge.
developers had contact with VA languages in a work context
(12 participants, 92%). Overall, the most frequent response
for both groups was a university course (77%) and work                      V. W HAT IMPROVEMENTS CAN BE MADE TO EXISTING
context (48%). Three participants mentioned online discus-                   TOOLS TO OVERCOME THOSE CHALLENGES ? (RQ3)
sions, one mentioned “university and enterprise colleagues”               The user survey combined closed and open-ended questions.
(P17), another reported “self-learning” (P18), and finally, one        The closed questions aimed to validate the following specific
participant said their first encounter was due to being “bored in      proposals derived from our earlier analysis: 1) Create user-
high school” (P28). From our observation, it seems that most           readable counter-examples to complement error messages.
                          TABLE V                                                  languages effectively. For example, one beginner developer,
  C ODEBOOK WITH CODE FREQUENCY FOR THE PROPOSED SOLUTIONS                         P28, noted the need for “more documentation on coming
                       SUGGESTED BY PARTICIPANTS
                                                                                   up with invariants”. Four participants mentioned improved
          #    Code                                                                usability, and three better education. When facing errors,
          5    Better Documentation and Learning Materials
                                                                                   two beginners and one experienced developer mentioned that
          4    Integration with Mainstream Languages and Tools                     better debugging would help them understand why the veri-
          4    Improved Usability                                                  fication fails. P23 mentioned directly that “To be really useful
          3    Better Error Messages and Feedback
          3    Improved Automation
                                                                                   in practice, a verification-aware language needs to be familiar,
          3    Increased Awareness and Education                                   easy to write proofs in, predictable in terms of what can
          3    Better Debugging and Profiling Tools                                be verified, well-integrated with common tools, interoperable
          3    Industry Demand and Investment
          2    Easier Installation and Better Tool Support
                                                                                   with other languages, and able to generate efficient code.”
          2    Use of Common Specification Methodologies                           (P23). This aligns with the broader theme of integration with
          2    Skepticism about Practical Use                                      mainstream languages, mentioned by four participants.
          2    Reusable Blocks
          1    Exposing Internal Proof State
                                                                                      Another suggestion by two participants is related to
                                                                                   reusable blocks, P19 proposed that tools should “provide
                                                                                   more automation to help ‘easy tasks’, so the program-
From our analysis, counter-examples do not always seem                             mer/prover can focus on complex tasks”, and P26, mentioned
helpful and their use was even discouraged in some cases;                          directly they would like to see “reusable bricks for com-
2) Develop official tutorials on common verification exercises                     mon verification patterns“. Three participants advocated for
(e.g., Fibonacci sequence, greatest common divisor). Neither                       increased investment in verification tools, suggesting that
Dafny nor Frama-C provides guided tutorials on their official                      funding and institutional support are necessary for widespread
pages; 3) Implement a search feature in the documentation.                         adoption. While the majority of participants maintained a
Neither Dafny nor Frama-C include a search feature, and                            positive outlook, skepticism regarding practical adoption was
Frama-C’s documentation is only available in PDF format.                           expressed by two participants. For instance, P13 remarked,
Dafny’s online documentation lacks a persistent table of con-                      “verification is expensive, and tends not to produce immediate
tents, unlike popular tools like Jest,10 and Pytest;11 4) Expand                   value, something which corporate doesn’t like very much.”
the themes covered in the documentation based on the gaps
identified in our analysis; and 5) Promote VA languages in                            RQ3: Our findings point to four key improvements for
mandatory courses, as these languages often appear only in                            addressing challenges in VA languages: better debug-
optional courses, unlike testing, which is frequently taught.                         ging tools; richer educational resources like tutorials
   The open-ended responses complemented these results with                           and improved documentation; greater automation of
additional, user-driven suggestions not previously captured. In                       routine verification tasks; and tighter integration with
this subsection, we present both the quantitative results and the                     mainstream development tools.
qualitative themes that emerged from participants’ feedback.
Closed-ended Questions. The first improvement addresses the                                            VI. R ELATED W ORK
inclusion of user-readable counter-examples that could allow
                                                                                      To the best of our knowledge, this is the first work to
users to “debug” the proofs. Most participants (83.9%) agreed
                                                                                   address challenges faced by developers using VA languages.
on its importance. The suggestion to improve tutorials with
                                                                                   In this section, we focus on related work on analysis and
common projects was also well-received by the majority of
                                                                                   topic modeling of developer discussions, and on studies on
participants (64.5%). Improving documentation search mech-
                                                                                   challenges faced when using different programming languages.
anisms saw a notable divide, with beginners (66.7%) placing
                                                                                   Developer Discussion Analysis and Topic Modeling. Prior
more emphasis on this improvement than experienced devel-
                                                                                   studies have applied topic modeling to analyse developer
opers (15.4%), and this difference was statistically significant
                                                                                   discussions on platforms like Stack Overflow and GitHub,
(p = 0.02822). Expanding documentation themes received
                                                                                   focusing on areas different from VA languages [10]. Barua
mixed responses, with 41.9% considering it very important.
                                                                                   et al. [8] analysed posts from a Stack Overflow data dump to
Finally, including VA languages in undergraduate programs
                                                                                   understand the main general discussion topics on the platform.
was considered highly impactful by most participants (50.1%).
                                                                                   Bagherzadeh and Khatchadourian [4] used the official Stack
Open-ended Questions. We identified 13 categories of im-
                                                                                   Overflow data dump to study the topics of questions about
provement for VA languages (see Table V). The most fre-
                                                                                   big data. Han et al. [25] studied what issues deep learning
quently mentioned area was improvements in documentation
                                                                                   framework practitioners discuss, gathering data from Stack
and learning materials, suggested by five participants. These
                                                                                   Overflow and GitHub. Abdellatif et al. [1] used the official
requests included better tutorials, guides, and documentation to
                                                                                   Stack Overflow data dump to identify the topics chatbot devel-
assist both newcomers and experienced developers in using VA
                                                                                   opers were asking about. They analysed heuristics to discover
  10 https://jestjs.io/docs/getting-started [last access 16th July 2024]           relevant tags, using only post titles for training data, claiming
  11 https://docs.pytest.org/en/8.2.x/contents.html [last access 16th July 2024]   it was representative and reduced noise. El aoun et al. [18]
investigated challenges in quantum software engineering using      (e.g., frame specifications and proof termination clauses, were
data from GitHub and the Stack Exchange Data Explorer (for         identified in Stack Overflow, but not confirmed as challenges),
Stack Overflow). Al Alamin et al. [3] conducted an empirical       points to the importance of empirical user studies, as research
study of developer discussions on low-code software develop-       based solely on online discussions may not fully capture the
ment challenges. Peruma et al. [40] used the SOTorrent dataset     real experience of practitioners (or vice-versa).
to study the topics around Software Refactoring being asked           This work can pave the way for future research on chal-
by developers. These studies demonstrate a well-established        lenges and improvements, while also offering valuable insights
methodology for using topic modeling, primarily on online          to guide the design and/or enhancement of VA languages to
forum data, to study developer discussions across various          support broader adoption. Future work includes expanding
software engineering areas. Our work builds on these studies       the dataset with further sources and carry out a large-size
and applies them to the specific context of VA languages.          user study. In addition, newly identified challenges should
Programming Language Challenges. Other studies have                be ranked based on relevance, in order to direct development
examined the challenges developers face when using program-        towards support that can have a greater impact.
ming languages, suggesting that even experienced developers        Threats to Validity. For topic modeling, using question bodies
struggle to learn new programming languages [44]. Ko et            provides more context but also introduces noise from off-topic
al. [31] identified six learning barriers in programming sys-      discussions, error messages, and troubleshooting attempts,
tems, which include understanding, design, use, and informa-       which may obscure the actual challenges. We mitigated this
tion barriers. These barriers align closely with the challenges    by reviewing both topic keywords and question bodies during
reported by VA language users in our study, such as difficulty     classification. Additionally, Stack Overflow may lack sufficient
interpreting tool feedback and expressing proof strategies.        coverage for some tools, limiting the generalizability of our
Other studies focused on particular languages. For instance,       results. Our mapping between languages and questions may
Zhu et al. [51] focused on Rust. They analyzed 15,000 Stack        also have missed relevant posts, reducing completeness. In the
Overflow posts and surveyed 101 Rust developers to find that       survey, the number of participants limited the ability to detect
Rust safety features impose a steep learning curve and that        differences between experience levels. Also, the translation
compiler messages often lack actionable information. This is       of challenges into affirmations may have lost important con-
in line with other work that identified onboarding and usability   text, affecting participants’ understanding. We mitigated this
issues as barriers to the adoption of languages [22], [29].        by providing open-ended questions where participants could
Chakraborty et al. [11] examined the support ecosystem for         provide their opinions.
newer languages such as Go, Swift, and Rust by analyzing
both Stack Overflow and GitHub data. They identified gaps in                              ACKNOWLEDGMENTS
documentation, which often drove developers to rely on com-           Alexandra Mendes was supported by an Amazon Research
munity Q&A sites. Finally, Christakis and Bird [12] studied        Award, Fall 2024. Carolina Carreira was financed by National
developer expectations regarding program analysis tools by         Funds through the FCT - Fundação para a Ciência e a Tecnolo-
surveying engineers at Microsoft. They found that high false-      gia, I.P. (Portuguese Foundation for Science and Technology)
positive rates, poor tool integration, and unclear feedback were   within the project VeriFixer, with reference 2023.15557.PEX
the main reasons developers rejected static analysis tools in      (DOI: 10.54499/2023.15557.PEX), and by funding from FCT
practice. These findings echo the feedback-related problems        under grant PRT/BD/153739/2021. We thank João F. Ferreira
reported by VA language users in our study and suggest that        for his valuable comments on this work.
if tools fail to align with developers’ workflows or generate
opaque error messages, they are unlikely to be adopted.                                         R EFERENCES
                                                                    [1] Ahmad Abdellatif, Diego Costa, Khaled Badran, Rabe Abdalkareem,
                     VII. C ONCLUSION                                   and Emad Shihab. Challenges in Chatbot Development: A Study of
                                                                        Stack Overflow Posts. In MSR’20, pages 174–185. ACM, 2020.
   This work analyzes the challenges developers face with VA        [2] Wolfgang Ahrendt, Bernhard Beckert, Richard Bubel, Reiner Hähnle,
languages, incorporating feedback from both beginners and               Peter H Schmitt, and Mattias Ulbrich. Deductive software verification
experienced users. We trained an ML model on 1,420 ques-                - the KeY book. Lecture notes in computer science, 10001, 2016.
                                                                    [3] Md Abdullah Al Alamin, Sanjay Malakar, Gias Uddin, Sadia Afroz,
tions, with 145 analyzed post-clustering. From this, 24 distinct        Tameem Bin Haider, and Anindya Iqbal. An empirical study of
challenges were identified and rated by 31 study participants.          developer discussions on low-code software development challenges. In
Additionally, five improvement suggestions were evaluated,              2021 IEEE/ACM 18th MSR, pages 46–57, 2021.
                                                                    [4] Mehdi Bagherzadeh and Raffi Khatchadourian. Going big: a large-scale
and 12 more were uncovered via open-ended responses.                    study on what big data developers ask. In Proceedings of the 2019
   Our findings suggest that VA language adoption is primarily          27th ACM Joint Meeting on European Software Engineering Conference
blocked by lack of documentation, and usability and ecosystem           and Symposium on the Foundations of Software Engineering, ESEC/FSE
                                                                        2019, pages 432–442, New York, NY, USA, August 2019. ACM.
limitations, highlighting key areas for improvement. For exam-      [5] Sebastian Baltes, Lorik Dumani, Christoph Treude, and Stephan Diehl.
ple, a challenge across all experience levels lies in designing         Sotorrent: reconstructing and analyzing the evolution of stack overflow
and completing proof strategies, underscoring the need for              posts. In MSR, MSR ’18, page 319–330, New York, NY, USA, 2018.
                                                                        Association for Computing Machinery.
better tool support and guidance. Additionally, the mismatch        [6] John Barnes. SPARK: The Proven Approach to High Integrity Software.
found between online discussions and reported challenges                Altran Praxis, 2012.
 [7] Mike Barnett, K Rustan M Leino, and Wolfram Schulte. The spec#                     fast verifier for c and java. In NASA formal methods symposium, pages
     programming system: An overview. In International Workshop on                      41–55. Springer, 2011.
     Construction and Analysis of Safe, Secure, and Interoperable Smart            [29] Brittany Johnson, Yoonki Song, Emerson Murphy-Hill, and Robert
     Devices, pages 49–69. Springer, 2004.                                              Bowdidge. Why don’t software developers use static analysis tools to
 [8] Anton Barua, Stephen W. Thomas, and Ahmed E. Hassan. What are                      find bugs? In 2013 35th ICSE, pages 672–681. IEEE, 2013.
     developers talking about? An analysis of topics and trends in Stack           [30] Alexander Knüppel, Thomas Thüm, Carsten Pardylla, and Ina Schaefer.
     Overflow. Empirical Software Engineering, 19(3):619–654, June 2014.                Experience Report on Formally Verifying Parts of OpenJDK’s API with
 [9] David M. Blei, Andrew Y. Ng, and Michael I. Jordan. Latent Dirichlet               KeY. Electronic Proceedings in Theoretical Computer Science, 284:53–
     Allocation. Journal of Machine Learning Research, 3:993–1022, 2003.                70, 2018. Publisher: Open Publishing Association.
[10] Carolina Carreira, Nuno Saavedra, Alexandra Mendes, and João F               [31] Amy J Ko, Brad A Myers, and Htet Htet Aung. Six learning barriers
     Ferreira. From “Worse is Better” to better: Lessons from a mixed                   in end-user programming systems. In 2004 IEEE Symposium on Visual
     methods study of ansible’s challenges. arXiv preprint arXiv:2504.08678,            Languages-Human Centric Computing, pages 199–206. IEEE, 2004.
     2025.                                                                         [32] Andrea Lattuada, Travis Hance, Jay Bosamiya, Matthias Brun, Chanhee
[11] Partha Chakraborty, Rifat Shahriyar, Anindya Iqbal, and Gias Uddin.                Cho, Hayley LeBlanc, Pranav Srinivasan, Reto Achermann, Tej Chajed,
     How do developers discuss and support new programming languages in                 Chris Hawblitzel, Jon Howell, Jay Lorch, Oded Padon, and Bryan Parno.
     technical Q&A site? An empirical study of Go, Swift, and Rust in Stack             Verus: A practical foundation for systems verification. In SOSP, pages
     Overflow. Information and Software Technology, 137:106603, 2021.                   438–454, November 2024.
[12] Maria Christakis and Christian Bird. What developers want and need            [33] Gary T Leavens, Albert L Baker, and Clyde Ruby. Preliminary design
     from program analysis: an empirical study. In 31st IEEE/ACM Int. Conf.             of JML: A behavioral interface specification language for Java. ACM
     on Automated Software Engineering, pages 332–343, 2016.                            SIGSOFT Software Engineering Notes, 31(3):1–38, 2006.
[13] Ernie Cohen, Markus Dahlweid, Mark Hillebrand, Dirk Leinenbach,               [34] K Rustan M Leino. Dafny: An automatic program verifier for functional
     Michał Moskal, Thomas Santen, Wolfram Schulte, and Stephan Tobies.                 correctness. In International conference on logic for programming
     VCC: A practical system for verifying concurrent C. In Theorem Proving             artificial intelligence and reasoning, pages 348–370. Springer, 2010.
     in Higher Order Logics, pages 23–42. Springer, 2009.                          [35] K. Rustan M. Leino, David R. Cok, and Dafny contributors. Dafny
[14] James C Corbett, Matthew B Dwyer, John Hatcliff, Shawn Laubach,                    Reference Manual, 2024. [Online]; accessed 06th January 2025.
     Corina S Păsăreanu, Robby, and Hongjun Zheng. Bandera: Extracting           [36] Bertrand Meyer. The Eiffel programming language. http://www. eiffel.
     finite-state models from java source code. In 22nd ICSE, pages 439–448,            com, 1992.
     2000.                                                                         [37] Mattias Nyberg, Dilian Gurov, Christian Lidström, Andreas Rasmus-
[15] Pascal Cuoq, Florent Kirchner, Nikolai Kosmatov, Virgile Prevosto,                 son, and Jonas Westman. Formal verification in automotive industry:
     Julien Signoles, and Boris Yakobowski. Frama-c: A software analysis                Enablers and obstacles. Lecture Notes in Computer Science (including
     perspective. pages 233–247, 2012.                                                  subseries Lecture Notes in Artificial Intelligence and Lecture Notes in
[16] Adel Djoudi, Martin Hána, and Nikolai Kosmatov. Formal Verification               Bioinformatics), 11247 LNCS:139 – 158, 2018.
     of a JavaCard Virtual Machine with Frama-C. In Formal Methods, pages          [38] David L. Parnas, A. John van Schouwen, and Shu Po Kwan. Evaluation
     427–444. Springer International Publishing, 2021.                                  of safety-critical software. Commun. ACM, 33(6):636–648, 1990.
[17] Frank Dordowsky. An experimental Study using ACSL and Frama-                  [39] David J Pearce and Lindsay Groves. Whiley: a platform for research in
     C to formulate and verify Low-Level Requirements from a DO-178C                    software verification. In SLE’13, pages 238–248. Springer, 2013.
     compliant Avionics Project. Electronic Proceedings in Theoretical             [40] Anthony Peruma, Steven Simmons, Eman Abdullah AlOmar, Chris-
     Computer Science, 187:28–41, 2015.                                                 tian D. Newman, Mohamed Wiem Mkaouer, and Ali Ouni. How do
[18] Mohamed Raed El aoun, Heng Li, Foutse Khomh, and Moses Openja.                     I refactor this? An empirical study on refactoring trends and topics in
     Understanding quantum software engineering challenges an empirical                 Stack Overflow. Empirical Software Engineering, 27(1), January 2022.
     study on stack exchange forums and github issues. In 2021 IEEE                [41] Michael Röder, Andreas Both, and Alexander Hinneburg. Exploring
     ICSME, pages 343–354, 2021.                                                        the Space of Topic Coherence Measures. In Proc. of WSDM’15, pages
[19] Escher Technologies. Escher C verifier (ECV). https://web.archive.org/             399–408. ACM, 2015.
     web/20250115124219/https://eschertech.com/products/ecv.php, 2017.             [42] Marc Schoolderman, Sjaak Smetsers, and Marko Van Eekelen. Is
     Accessed via Internet Archive on January 15, 2025.                                 Deductive Program Verification Mature Enough to be Taught to Software
[20] Jean-Christophe Filliâtre and Andrei Paskevich. Why3—where pro-                   Engineers? In Proceedings of the 8th Computer Science Education
     grams meet provers. In Programming Languages and Systems: 22nd                     Research Conference, pages 50–57. ACM, 2019.
     European Symposium on Programming 2013, pages 125–128, 2013.                  [43] Yuvaraj Selvaraj, Wolfgang Ahrendt, and Martin Fabian. Verification
[21] David Fullerton. Stack Exchange Creative Commons data now hosted                   of Decision Making Software in an Autonomous Vehicle: An Industrial
     by the Internet Archive, 2014. [Online]; accessed 03 June 2024.                    Case Study. In Formal Methods for Industrial Critical Systems: 24th
[22] Kelsey R Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and                     International Conference, pages 143–159. Springer-Verlag, 2019.
     Michelle L Mazurek. Benefits and drawbacks of adopting a secure               [44] Nischal Shrestha, Colton Botta, Titus Barik, and Chris Parnin. Here we
     programming language: Rust as a case study. In 17th Symposium on                   go again: Why is it difficult for developers to learn another programming
     Usable Privacy and Security, pages 597–616, 2021.                                  language? In ICSE, pages 691–701, 2020.
[23] Dilian Gurov, Christian Lidström, Mattias Nyberg, and Jonas Westman.         [45] Julia Silge and David Robinson. Text Mining with R: A Tidy Approach,
     Deductive Functional Verification of Safety-Critical Embedded C-Code:              2024. [Online]; accessed 30 May 2024.
     An Experience Report. In Laure Petrucci, Cristina Seceleanu, and Ana          [46] Donna Spencer. Card Sorting: Designing Usable Categories. Rosenfeld
     Cavalcanti, editors, Critical Systems: Formal Methods and Automated                Media, 2009.
     Verification, pages 3–18. Springer International Publishing, 2017.            [47] Vassil Todorov, Frederic Boulanger, and Safouan Taha. Formal verifi-
[24] Matthias Güdemann. Online Teaching of Verification of C Programs in               cation of automotive embedded software. In 6th Conference on Formal
     Applied Computer Science. In João F. Ferreira, Alexandra Mendes, and              Methods in Software Engineering (FormaliSE ’18), page 84 – 87, 2018.
     Claudio Menghi, editors, Formal Methods Teaching, 2021.                       [48] Ike Vayansky and Sathish AP Kumar. A review of topic modeling
[25] Junxiao Han, Emad Shihab, Zhiyuan Wan, Shuiguang Deng, and Xin                     methods. Information Systems, 94:101582, 2020.
     Xia. What do Programmers Discuss about Deep Learning Frameworks.              [49] Markus Voelter, Daniel Ratiu, Bernhard Schaetz, and Bernd Kolb.
     Empirical Software Engineering, 25(4):2694–2747, July 2020.                        mbeddr: an extensible c-based programming language and ide for
[26] Klaus Havelund and Thomas Pressburger. Model checking java pro-                    embedded systems. In Proc. of SPLASH’12, pages 121–140, 2012.
     grams using java pathfinder. International Journal on Software Tools          [50] Neil White, Stuart Matthews, and Roderick Chapman. Formal verifi-
     for Technology Transfer, 2:366–381, 2000.                                          cation: Will the seedling ever flower? Philosophical Transactions of
[27] Reiner Hähnle and Marieke Huisman. Deductive software verification:               the Royal Society A: Mathematical, Physical and Engineering Sciences,
     From pen-and-paper proofs to industrial tools. Lecture Notes in Com-               375(2104), 2017.
     puter Science (including subseries Lecture Notes in Artificial Intelligence   [51] Shuofei Zhu, Ziyi Zhang, Boqin Qin, Aiping Xiong, and Linhai Song.
     and Lecture Notes in Bioinformatics), 10000:345 – 373, 2019.                       Learning and programming challenges of Rust: A mixed-methods study.
[28] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem             In ICSE, pages 1269–1281, 2022.
     Penninckx, and Frank Piessens. Verifast: A powerful, sound, predictable,
