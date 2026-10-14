                                                                2023 IEEE/ACM 45rd International Conference on Software Engineering (ICSE)



                                             Impact of Code Language Models on Automated
                                                            Program Repair
                                                      Nan Jiang                        Kevin Liu                   Thibaud Lutellier                    Lin Tan
                                                   Purdue University            Lynbrook High School              University of Alberta            Purdue University
                                                West Lafayette, USA                San Jose, USA                    Alberta, Canada              West Lafayette, USA
                                                jiang719@purdue.edu            kevin.bx.liu@gmail.com             lutellie@ualberta.ca            lintan@purdue.edu



                                            Abstract—Automated program repair (APR) aims to help                 Although DL-based APR techniques are one of the most
arXiv:2302.05020v3 [cs.SE] 16 Apr 2023




                                         developers improve software reliability by generating patches for    effective, these tools fail to fix a large portion of bugs.
                                         buggy programs. Although many code language models (CLM)             In addition, existing DL-based APR tools typically have to
                                         are developed and effective in many software tasks such as code
                                         completion, there has been little comprehensive, in-depth work       generate hundreds to thousands of candidate patches and take
                                         to evaluate CLMs’ fixing capabilities and to fine-tune CLMs for      hours to validate these patches to fix enough bugs [6], [7],
                                         the APR task.                                                        [9], [10]. Recent work shows that 93% of developers are only
                                            Firstly, this work is the first to evaluate ten CLMs on four      willing to review up to ten patches and 63% of developers
                                         APR benchmarks, which shows that surprisingly, the best CLM,         expect APR tools to respond within one hour [22]. Thus, there
                                         as is, fixes 72% more bugs than the state-of-the-art deep-learning
                                         (DL)-based APR techniques. Secondly, one of the four APR             is a gap for DL-based APR research to be used in practice [22].
                                         benchmarks was created by us in this paper to avoid data                In addition to DL-based APR models, code language models
                                         leaking for a fair evaluation. Thirdly, it is the first work to      (CLMs) [23], [24] have shown their promises for fixing bugs,
                                         fine-tune CLMs with APR training data, which shows that fine-        given the demonstrated effectiveness of language models [25]–
                                         tuning brings 31%–1,267% improvement to CLMs and enables             [34] in natural language domains. Different from DL-based
                                         them to fix 46%–164% more bugs than existing DL-based APR
                                         techniques. Fourthly, this work studies the impact of buggy lines,   APR models that use an APR-specific design and are trained
                                         showing that CLMs, as is, cannot make good use of the buggy          with labeled APR training sets (typically pairs of buggy and
                                         lines to fix bugs, yet fine-tuned CLMs could potentially over-rely   fixed code), CLMs are trained with huge-sized unlabeled code
                                         on buggy lines. Lastly, this work analyzes the size, time, and       corpora (e.g., programs) for general code language modeling
                                         memory efficiency of different CLMs.                                 tasks, e.g., next token prediction [35], [36].
                                            This work shows promising directions for the APR domain,
                                         such as fine-tuning CLMs with APR-specific designs, and also            Despite the success of CLMs in many domains [23], [24],
                                         raises awareness of fair and comprehensive evaluations of CLMs       [35], [37], [38], there has been little comprehensive, in-depth
                                         and calls for more transparent reporting of open-source reposi-      work analyzing and comparing CLMs’ fixing capabilities
                                         tories used in the pre-training data to address the data leaking     in the APR domain with those of existing DL-based APR
                                         problem.                                                             techniques that are specially designed to fix bugs. Thus, it
                                            Index Terms—Automated Program Repair, Code Language
                                         Model, Fine-Tuning, Deep Learning
                                                                                                              is an interesting and important research question to ask: do
                                                                                                              code language models bring improvement to automated
                                                                                                              program repair and how?
                                                               I. I NTRODUCTION                               A. Evaluation of CLMs on APR Benchmarks
                                         Automated program repair (APR) [1]–[3] helps developers im-          Existing techniques [23], [24], [37], [38] evaluate CLMs’
                                         prove software reliability by generating patches automatically       fixing capabilities mostly on the benchmark provided by
                                         to repair software defects. Many deep learning (DL)-based            CodeXGLUE [39], which is abstracted code (e.g., VAR1 <
                                         APR techniques [4]–[13] adapt DL models to take a buggy              VAR2.length()) instead of real-world code (e.g., charno <
                                         software program as input and generate a patched program.            sourceExcerpt.length()). But understanding and gener-
                                         A typical DL-based APR technique builds a neural network             ating concrete variable and function names is a mandatory and
                                         model from a training set, which are pairs of buggy code and         challenging step to fix bugs [6], [7], [9], [10]. In addition, they
                                         the corresponding fixed code. Then these models are evaluated        report BLEU scores (which measure the similarity between
                                         on a test set, which are also pairs of the buggy and fixed code      generated patched code and the developer patch) instead of
                                         that is disjoint from the training set. With the strong learn-       validating the correctness of the generated patches. They
                                         ing capability of DL models, these techniques learn diverse          cannot do so, because CodeXGLUE [39] also contains no full
                                         patterns of transforming buggy programs to patched programs          project context or test cases. But many patches with a good
                                         from large code corpora, and many [7], [9], [10] outperform          BLEU score are incorrect patches. Thus, we need to use an
                                         traditional template-based [14], [15], heuristic-based [16]–[18]     APR benchmark with realistic, real-world bugs and test cases
                                         and constraint-based [19]–[21] APR techniques.                       to evaluate the true effectiveness of CLMs in fixing bugs.

                                         xxxxx © 2023 IEEE.
                                         DOI xxxxx
   While we can and will use real-world APR bench-                   (time efficiency), and how the memory footprint changes
marks such as Defects4J v1.2 [40], Defects4J v2.0 [40],              (memory efficiency) of the ten different-sized CLMs.
and QuixBugs [41], to evaluate the fixing capabilities of
CLMs [42], there is a challenge that the training data of these      D. Contributions
CLMs may contain the bugs or fixes in these APR benchmarks,          To sum up, this paper makes the following contributions:
since these CLMs use public repositories such as all GitHub          (1) A new APR benchmark, HumanEval-Java, that no existing
repositories by a certain date [23], [24], [35], [37], [38]. While   CLMs have seen during pre-training, to ensure the fairness of
data leaking is a threat to all CLM-related papers, not just this    evaluation.
paper, this threat is less of a concern for APR compared to
other domains [43], [44], since CLMs do not see the pairs            (2) A study of ten CLMs (of four architectures, i.e., PLBART,
of buggy code and their fixed code during training, and their        CodeT5, CodeGen, and InCoder) and four state-of-the-art DL-
training data often contains at most the buggy code or the fixed     based APR techniques (i.e., CURE, RewardRepair, Recoder,
code, but not both. We address this data-leaking challenge by        and KNOD) on four APR benchmarks (i.e., Defects4J v1.2,
manually creating a new evaluation benchmark HumanEval-              Defects4J v2.0, QuixBugs and our new HumanEval-Java):
Java that has not been seen by any of the evaluated CLMs                • Finding 1: CLMs, even without fine-tuning, have com-

during training.                                                          petitive fixing capabilities. To our surprise, the best CLM,
   In this work, we evaluate ten code language models of                  as is, fixes 72% more bugs than the state-of-the-art DL-
four types (PLBART [23], CodeT5 [24], CodeGen [35], and                   based APR techniques.
InCoder [45]) on four benchmarks (Defects4J v1.2 [40], De-              • Finding 2: While buggy lines (code lines that need to be

fects4J v2.0 [40], QuixBugs [41] and HumanEval-Java). We                  modified) are useful to guide fixing, CLMs fail to make
run developer-written test cases to validate the correctness of           good use of them and fix fewer bugs when the buggy
generated patches to evaluate and compare the ten CLMs.                   lines are explicitly given.
                                                                     (3) The first fine-tuning experiment of ten CLMs with APR
B. Fine-tuning CLMs for the APR Task                                 training data, and a study of fine-tuning’s impact (and its
CLMs are often trained for general tasks (e.g., next token           training data size) on CLMs for APR:
prediction) on a large corpus. This training is referred to as          • Finding 3: Fine-tuning improves CLMs’ fixing capabil-
pre-training. Fine-tuning is a common technique to train a                 ities by 31%–1,267%, and fine-tuned CLMs outperform
pre-trained CLM with data from a downstream task, e.g., code               DL-based APR techniques significantly, by 46%–164%.
summarization or code translation, when one wants to apply a            • Finding 4: Although fine-tuning helps, it sometimes
general pre-trained CLM to a specific downstream task [23],                makes CLMs over-rely on the buggy lines, and thus fail
[24], [35], [37], [38]. Fine-tuning is typically very effective to         to fix some bugs that can be fixed without fine-tuning.
tailor a general pre-trained CLM for a downstream task [25],            • Finding 5: CodeT5 and CodeGen models achieve the best
[30]–[32], [46]. Yet, none of the CLMs have been fine-tuned                fixing capabilities after being fine-tuned with 10,000 APR
for the APR task with real-world, non-abstracted APR training              training instances, and fine-tuning with more APR data
data.                                                                      makes them fix fewer (reduced by 8%–19%). InCoder
   To study how fine-tuning may enhance or hurt CLMs on                    model fixes the most bugs after being fine-tuned with
APR, we fine-tune ten CLMs with APR training data used                     50,000 training instances, and more fine-tuning data also
by DL-based APR techniques. We also study the impact of                    makes it fix fewer (reduced by 9%).
the size of the fine-tuning data. Typically the more training        (4) A study of the size, time and memory efficiency of CLMs
data, the more effective the resulting models are up to a            (i.e., PLBART, CodeT5, CodeGen and InCoder).
certain point, when one trains a DL model from scratch [26],
                                                                         • Finding 6: CodeT5 and InCoder models have the best
[27], [46], [47]. And DL-based APR tools also fix more bugs
when they are trained with more data [10]. We will study if                 size efficiency, suggesting developing larger CodeT5 or
fine-tuning with more data improves the fixing capabilities of              InCoder models is the most promising. Besides, CodeT5,
CLMs for APR [47], [48].                                                    PLBART, and InCoder models are better choices given
                                                                            limited resources, as they have better time and memory
C. Fixing Capability versus Cost                                            efficiency than CodeGen models.

As the size (i.e., number of parameters) of CLMs grows               (5) Implications for future work (Section VII).
exponentially in recent years [34], the cost of applying such                       II. C ODE L ANGUAGE M ODELS
large models (e.g., time and memory cost) also grows dra-
matically. Although larger CLMs may fix more bugs, the               A. CLM Architectures
trade-off between fixing capability and cost of applying such        Code language models can be categorized into three groups:
large models is important. Thus, we study as the model sizes         encoder-only models, decoder-only models, and encoder-
change, how the fixing capabilities change (size efficiency),        decoder models. Regardless of groups, most existing code
how the average time required to generate patches changes            language models are built with a Transformer [49] architecture
as it has the best learning capability and the greatest scalabil-                 (2) Masked Span Prediction is the task of training a language
ity [25]–[27], [30]–[32], [46], [49].                                             model to predict the masked code snippet in the input code.
   Encoder-only models include CodeBERT [37] and Graph-                           Figure 1 shows a simple Java function that returns the sum of
CodeBERT [38], which only have a bidirectional transformer                        two integers, where some parts of the function are masked by
encoder [49] with attention mechanism [49] to learn vectorized                    placeholders <MASK0> and <MASK1>. The language model is
embedding of the input code sequence. As they only have                           trained to predict that <MASK0> should be int and <MASK1>
encoders, these models are most suitable for downstream tasks                     should be x + y.
that require no generation, such as code representation (i.e.,                    (2) Masked Identifier Prediction is the task of predicting
embedding the input code) and code clone detection [37].                          identifier names in the given code. For example, all three iden-
   Decoder-only models include CodeGen [35], InCoder [45],                        tifiers (add, x, and y) are masked by placeholders (<MASK0>,
and Codex [36], which only have an autoregressive trans-                          <MASK1>, and <MASK2>), and a code language model is
former decoder [49] to learn to generate code sequences.                          trained to predict their correct name.
Different from encoder-only models that calculate embedding
                                                                                  (3) Deleted Span Prediction is the task that given code
for input code, decoder-only models are most suitable for
                                                                                  with some parts deleted (e.g., int and + y are deleted), the
downstream tasks such as open-ending code generation [36],
                                                                                  language model is trained to generate the completed code.
i.e., generating code based on input prompts, where a prompt
could be natural language text describing the functionality,                      (4) Identifier Tagging is the task of predicting whether each
the signature of a function, or the first few lines of code in a                  token in the code is an identifier or not. For example, add is
function.                                                                         an identifier while int is not. Thus the predicted label of add
   Finally, encoder-decoder models include PLBART [23]                            is 1 and that of int is 0.
and CodeT5 [24], which have both a bidirectional trans-                           (5) Biomodel Dual Generation is the task of training a lan-
former encoder and an autoregressive transformer decode.                          guage model that transforms code between different languages,
The encoder is trained to calculate the embedding of input                        e.g., from a natural language description to Java code, from
code and the decoder is trained to generate code. Thus,                           Java code to natural language text, or from Java code to Python
encoder-decoder models are more flexible to suit both non-                        code, etc.
generation (e.g., code classification) [23] and generation (e.g.,
code summarization) [24] downstream tasks.                                                        III. E XPERIMENTAL D ESIGN
                                                                                  Figure 2 shows the overview of our experimental design. We
                         (1) Next Token Prediction
Input: int add ( int x , int y ) { return                                         apply ten CLMs and three state-of-the-art DL-based APR
Output: int add ( int x , int y ) { return x
Input: int add ( int x , int y ) { return x                                       techniques on four bug benchmarks—three widely-used and
Output: int add ( int x , int y ) { return x +
                         (2) Masked Span Prediction
                                                                                  one new benchmark that we designed to address the data-
Input: int add ( int x , <MASK0> y ) { return <MASK1> ; }                         leaking challenge—to generate patches. We study and compare
Output: <MASK0> int <MASK1> x + y
                         (3) Masked Identifier Prediction                         the fixing capabilities of the CLMs and the DL-based APR
Input: int <MASK0> ( int <MASK1> , int <MASK2> ) { return <MASK1> + <MASK2> ; }
Output: <MASK0> add <MASK1> x <MASK2> y
                                                                                  techniques (RQ1). Then we fine-tune these CLMs with APR
                         (4) Deleted Span Prediction                              training datasets of different sizes, and study the patches
Input: int add ( int x , y) { return x ; }
Output: int add ( int x , int y ) { return x + y ; }                              generated by fine-tuned CLMs to show the impact of training
                         (5) Identifier Tagging                                   data size on fine-tuning (RQ2). Finally, by comparing patches
Input: int add ( int x , int y ) { return x + y ; }
Output: 0   1 0 0 1 0 0 1 0 0         0   1 0 1 0 0                               generated by differently sized code language models, we study
                         (6) Biomodel Dual Generation
Input: int add ( int x , int y ) { return x + y ; }
                                                                                  the size, time, and memory efficiency of different CLMs
Output: add two integers.
Input: add two integers.
                                                                                  (RQ3).
Output: int add ( int x , int y ) { return x + y ; }
                                                                                     We focus on Java single-hunk bugs, as the best DL-based
Fig. 1: Common pre-training tasks with examples that are used                     APR techniques are all specially designed for Java single-hunk
by existing CLMs.                                                                 bugs (i.e., the buggy code is continuous lines of code) [7], [9],
                                                                                  [10]. This enables us to explore how CLMs are different from
                                                                                  DL-based APR techniques in fixing the same types of bugs.
B. Common Pre-training Tasks
An important design difference among code language models                         A. Three Existing Bug Benchmarks
is the tasks used in pre-training. Figure 1 shows several                         We select real-world bug benchmarks widely used in the APR
common pre-training tasks used by existing code language                          domain, including Defects4J v1.2 [40], Defects4J v2.0 [40],
models.                                                                           and QuixBugs [41]. Defects4J v1.2 is the most widely used
(1) Next Token Prediction is the task that given a piece                          version of the Defects4J benchmark that contains 393 bugs,
of incomplete code, the language model is trained to predict                      among which 130 are single-hunk bugs. Defects4J v2.0 is
the following token, e.g., given int add(int x, int y){                           the latest version of the Defects4J benchmark that contains
return, the next token should be x. This process, if done iter-                   444 additional bugs, among which 108 are single-hunk bugs.
atively, trains language models to generate complete programs                     Both Defects4J v1.2 and Defects4J v2.0 are collected from
from the beginning to the end.                                                    famous Java projects such as “Google Closure compiler”
                                                                                                                     PLBART            CodeT5     CodeGen          InCoder
                  DL-based APR Techniques                                         RQ1:
                                             Patch Generation              Fixing Capabilities
                                                                                                                   base (140M)     small (60M)       350M                1B
                                                                           (Comparison with       Models          large (400M)     base (220M)          2B               6B
                                                                 Patched    APR Techniques)                                       large (770M)          6B
                                                                Programs
                                                                                                  Data Source    StackOverflow   CodeSearchNet    THEPILE     StackOverflow
                   Code Language Models                                                                               BigQuery        BigQuery    BigQuery    GitHub/GitLab
                                             Patch Generation                    RQ2:                       NL         79.0GB                 -      1.1TB          57.0GB
                                                                               Impact of          Raw Size
                                                                 Patched
                                                                                                            PL        576.0GB                 -    436.3GB         159.0GB
                                                                              Fine-tuning
 Bug Benchmarks                                                 Programs                                    NL            47M               5M            -                -
                                                                                                  Instances
                              Fine-Tuning                                                                   PL           680M               8M            -                -
                  Fine-tuned Code Language                                                                  NL            6.7B                -     354.7B                 -
                           Models
                                                                                                  Tokens
                                             Patch Generation
                                                                                                            PL           64.4B                -     150.8B                 -
                                                                                 RQ3:
                                                                            Size, Time and
                                                                 Patched
                                                                Programs
                                                                           Memory Efficiency     TABLE I: Ten CLMs of four architectures that we study in
                                                                                                 this work. NL refers to natural language, while PL refers
             Fig. 2: Overview of experimental design.                                            to programming language. “Raw Size” refers to the size of
                                                                                                 collected pre-training data, “Instances” refers to the number
and “Apache commons-math”. QuixBugs is a benchmark that                                          of pre-training data fed to the models, and “Tokens” is the
contains 40 bugs regarding famous algorithms like “quick sort”                                   total number of NL or PL tokens in the pre-training data. “-”
and “merge sort”.                                                                                means the corresponding number is not reported.
B. New HumanEval-Java Benchmark to Avoid Data Leaking                                            designs. Thus, encoder-only models such as CodeBERT [37]
Defects4J v1.2, Defects4J v2.0, and QuixBugs are widely used                                     or GraphCodeBERT [38] are excluded. They need either an
by DL-based APR techniques. However, applying CLMs only                                          extra decoder or careful designs of input format to be applied
on them might be problematic, as CLMs may have seen these                                        to generate patches, and (3) the pre-trained language model is
benchmarks in their pre-training data. By checking Code-                                         publicly accessible (e.g., Codex [36] is excluded as its model
SearchNet [50] and BigQuery1 , which are the data sources                                        is not released and cannot be fine-tuned). As a result, we select
of common CLMs, we find that four repositories used by                                           four types of code language models, which are PLBART [23],
the Defects4J benchmark are also in CodeSearchNet, and the                                       CodeT5 [24], CodeGen [35], and InCoder [45].
whole Defects4J repository is included by BigQuery. Thus, it
is very likely that existing APR benchmarks are seen by CLMs                                     PLBART: These models follow BART’s [32] encoder-decoder
during pre-training.                                                                             architecture (Section II-A), and are pre-trained on masked span
                                                                                                 prediction and deleted span prediction (Section II-B).
   To overcome this threat, we create a new bug benchmark
from HumanEval [36], named HumanEval-Java. HumanEval                                                The pre-training dataset of PLBART comes from BigQuery
is a dataset manually created to address the threat that CLMs                                    and StackOverflow, which contains 47M natural language
may have seen test datasets available online. Yet, it is created                                 instances and 680M programming language instances. The
for evaluating code generation task [36] and is written in                                       programming language data consist of 470M Java instances
Python. We manually convert the Python programs in Hu-                                           (69%) and 210M Python instances (31%). Thus, it performs
manEval and their test cases into Java programs and Junit                                        better on Java and Python code than other programming
test cases, and then inject bugs in the correct Java programs                                    languages [23].
to create an APR benchmark. HumanEval-Java contains 164                                             The developers released two PLBART models of different
(single-hunk) Java bugs, varying from simple bugs like in-                                       sizes, referred to as PLBART-base (140M parameters) and
correct operator usage to complex logical bugs that require                                      PLBART-large (400M parameters), both of which are pre-
modification of several lines of code to fix. Since HumanEval-                                   trained with the same data and pre-training tasks. We include
Java is converted from HumanEval and the bugs are manually                                       both models in this work.
injected, none of the CLMs would have seen it before. Thus,                                      CodeT5: The CodeT5 models follow T5’s [46] encoder-
it is the fairest benchmark to compare CLMs with DL-based                                        decoder architectures (Section II-A), and are pre-trained on
APR tools.                                                                                       several code-specified tasks, including masked span prediction,
C. Studied Code Language Models                                                                  identifier tagging, masked identifier prediction, and bimodal
                                                                                                 dual generation (Section II-B).
Table I lists the ten CLMs evaluated in this paper. We select
                                                                                                    The pre-training dataset comes from CodeSearchNet [50]
CLMs to study based on the following requirements: (1) the
                                                                                                 (an open-sourced code corpus containing 4291 projects col-
language model is trained on a large enough code corpus (e.g.,
                                                                                                 lected from GitHub), and also C and CSharp programs
we exclude T5 [46] and GPT-2 [26], which are natural lan-
                                                                                                 collected via BigQuery, which contains around 5M natural
guage models, and we exclude GPT-Neo [29] and GPT-J [28],
                                                                                                 language instances and 8M programming language instances.
which are trained on the THEPILE dataset [51], of which
                                                                                                 The programming language data consists of 22% JavaScript,
90% are English text), (2) the language model can be applied
                                                                                                 18% Java, 13% Python, 13% CSharp, 12% C, 11% PHP, 8%
to APR without any modification to its architecture or extra
                                                                                                 Go and 2% Ruby languages.
  1 https://console.cloud.google.com/marketplace/details/github/github-                             Developers released three CodeT5 models of different sizes,
repos?pli=1                                                                                      referred to as CodeT5-small (60M parameters), CodeT5-base
                       PLBART Prompt (w/o buggy line)                                      PLBART Prompt (w/ buggy line)
 Input:                                                             Input:
 public ValueMarker(double value, Paint paint, Stroke stroke,...    public ValueMarker(double value, Paint paint, Stroke stroke,...
     <mask>                                                             // buggy line: super(paint, stroke, paint, stroke, alpha);
     this.value = value;}                                               <mask>
                                                                        this.value = value;}
 Expected Output:                                                   Expected Output:
 public ValueMarker(double value, Paint paint, Stroke stroke,...    public ValueMarker(double value, Paint paint, Stroke stroke,...
     super(paint, stroke, outlinePaint, outlineStroke, alpha);          super(paint, stroke, outlinePaint, outlineStroke, alpha);
     this.value = value;}                                               this.value = value;}
                        CodeT5 Prompt (w/o buggy line)                                     CodeT5 Prompt (w/ buggy line)
 Input:                                                             Input:
 public ValueMarker(double value, Paint paint, Stroke stroke,...    public ValueMarker(double value, Paint paint, Stroke stroke,...
     <extra_id_0>                                                       // buggy line: super(paint, stroke, paint, stroke, alpha);
     this.value = value;}                                               <extra_id_0>
                                                                        this.value = value;}
 Expected Output:                                                   Expected Output:
     super(paint, stroke, outlinePaint, outlineStroke, alpha);          super(paint, stroke, outlinePaint, outlineStroke, alpha);
                       CodeGen Prompt (w/o buggy line)                                     CodeGen Prompt (w/ buggy line)
 Input:                                                             Input:
 public ValueMarker(double value, Paint paint, Stroke stroke,...    public ValueMarker(double value, Paint paint, Stroke stroke,...
                                                                        // buggy line: super(paint, stroke, paint, stroke, alpha);
 Expected Output:                                                   Expected Output:
     super(paint, stroke, outlinePaint, outlineStroke, alpha);          super(paint, stroke, outlinePaint, outlineStroke, alpha);
     this.value = value;}                                               this.value = value;}
                        InCoder Prompt (w/o buggy line)                                    InCoder Prompt (w/ buggy line)
 Input:                                                             Input:
 public ValueMarker(double value, Paint paint, Stroke stroke,...    public ValueMarker(double value, Paint paint, Stroke stroke,...
     <mask>                                                             // buggy line: super(paint, stroke, paint, stroke, alpha);
     this.value = value;}                                               <mask>
                                                                        this.value = value;}
 Expected Output:                                                   Expected Output:
     super(paint, stroke, outlinePaint, outlineStroke, alpha);          super(paint, stroke, outlinePaint, outlineStroke, alpha);
     this.value = value;}                                               this.value = value;}


  Fig. 3: Prompts used for applying CLMs on the APR task, using Chart-20 in Defects4J v1.2 benchmark as an example.

(220M parameters), and CodeT5-large (770M parameters).               D. Applying Code Language Models
We include all three models in this work.                            To answer RQ1, we apply the pre-trained CLMs without any
CodeGen: The CodeGen models follow a decoder-only ar-                fine-tuning to study their fixing capabilities learned from pre-
chitecture (Section II-A) and are pre-trained on the next            training tasks. We carefully check their papers and documen-
token prediction task (Section II-B). The developers re-             tation to ensure we set them up correctly.
leased 12 CodeGen models: CodeGen-350M/2B/6B/16B-                       To set up a fair comparison, we apply each code language
NL/Multi/Mono [35]. The “350M/2B/6B/16B” in the name                 model with two different prompts, i.e., the input to a CLM.
refers to the number of parameters, while “NL/Multi/Mono”            The first prompt does not contain the buggy lines (but the bug
specifies different training datasets. Specifically, “NL” denotes    location is still known), which is the natural (default) way of
that the model is only pre-trained on THEPILE [51] dataset           applying these CLMs according to their documentation. The
(mostly English text). “Multi” means that the model is also          second prompt gives the buggy lines as lines of comments,
pre-trained on data collected via BigQuery, which includes           to ensure CLMs have the same information as DL-based
30% Java, 21% C++, 17% C, 16% Python, 8% JavaScript and              APR techniques, which require buggy lines and surrounding
8% Go languages. “Mono” specifies that the model is also             functions to fix bugs. Figure 3 shows the prompts for different
pre-trained on a huge Python corpus collected from GitHub.           CLMs.
                                                                        • To apply PLBART models without providing the buggy
   As we focus on fixing Java bugs in this paper, and the
16B model is too large to run on our machines, we only                     lines, the whole buggy function is provided, with
study the CodeGen-350M/2B/6B-Multi models, referred to as                  the buggy lines masked by a placeholder (specifically,
CodeGen-350M, CodeGen-2B, and CodeGen-6B to simplify                       <mask> for PLBART). The models are expected to
the names.                                                                 output the whole patched function. To validate the correct-
                                                                           ness, the test cases are executed on the output function.
InCoder: The InCoder models follow XGLM [52]’s decoder-                 • To apply CodeT5 models without the buggy lines, the
only architecture (Section II-A) and are also pre-trained on the           input format is the same as PLBART, but the placeholder
masked span prediction task (Section II-B).                                used to mask the buggy line is <extra_id_0>. CodeT5
   The pre-training data of InCoder comes from open-sourced                models are expected to generate the patched lines. Since
projects on GitHub and GitLab, and StackOverflow posts,                    CodeT5 models do not have to generate the whole func-
which consists of 159 GB of code data (33% Python, 26%                     tion, it is supposed to be easier for CodeT5 to generate the
JavaScript, 10% C/C++, 8% HTML, 4% Java, etc.) and 57                      correct patch. To validate the correctness of the patch, we
GB of text data (the number of instances and tokens is not                 replace the buggy lines with CodeT5’s output to form the
reported). The pre-training data is deduplicated and filtered to           patched program, on which developer-written test cases
guarantee high quality.                                                    are executed.
   Developers released two InCoder models of different sizes,           • To apply CodeGen models without the buggy lines, the
referred to as InCoder-1B (1B parameters) and InCoder-6B                   input is the function before the buggy lines. The models
(6B parameters), both of which are included in this work.                  are expected to complete the function by generating the
                             Fine-tuning Prompt                     F. Baseline DL-based APR Techniques
Input:
public ValueMarker(double value, Paint paint, Stroke stroke,...
    // buggy line: super(paint, stroke, paint, stroke, alpha);      To compare CLMs with APR tools, we select the four best
    this.value = value;}
Expected Output:
                                                                    open-sourced DL-based APR techniques, namely CURE [7],
    super(paint, stroke, outlinePaint, outlineStroke, alpha);       RewardRepair [9], Recoder [10], and KNOD [11]. Other APR
                                                                    techniques either fix fewer bugs [4]–[6], [14], [15] or are un-
Fig. 4: Prompt used for fine-tuning CLMs with Chart-20
                                                                    available [54], and we need to select open-sourced techniques
in Defects4J v1.2 benchmark as an example.
                                                                    to apply them to our new benchmark HumanEval-Java. These
    patched line and the remainder of the function after the        APR techniques all have encoder-decoder architecture, but also
    buggy lines. To validate the correctness, we append the         have APR-specific designs.
    output to the input to form a complete function, on which          CURE implements its encoder and decoder with convolu-
    the test cases are executed. CodeGen models do not know         tional networks [55], and applies a small code GPT [7], [25]
    the code snippet after the buggy lines (thus, they have less    to learn code syntax (but it is only pre-trained on 4M Java
    information when fixing bugs), which is due to the design       functions), and designs a code-aware search strategy to exclude
    of CodeGen.                                                     invalid identifiers during patch generation [7].
  • To apply InCoder models without the buggy line, the                RewardRepair is implemented with transformer architecture
    input is the same as PLBART. The models are expected            and is the most similar to CLMs regarding architectures. It
    to output the patched line as well as the code after            also considers patch execution information (compilability and
    the patched line. To validate the correctness, we append        correctness) in the calculation of loss function during training,
    the output to the code before the buggy line to form a          which makes the model learn to generate compilable and
    complete function and run the test cases. Compared with         correct patches [9].
    CodeGen models, InCoder models have the code snippet               Recoder has a novel architecture to generate edits to modify
    after the buggy lines when generating patches, which is         the abstract syntax tree (AST) to patched AST [10]. Generat-
    the advantage of the design of InCoder models (i.e., using      ing at the AST level enables it to generate more syntactically
    masked span prediction as a pre-training task).                 correct patches, and generating edits enables it to fix bugs with
  • To apply these CLMs models with buggy lines as part             fewer decoding steps.
    of the prompts, the buggy lines are provided as lines of           KNOD is a recent DL-based APR technique that uses
    comments before the location of the buggy lines.                graph-transformer [56] and a novel three-stage tree decoder
                                                                    to generate patched ASTs. It also uses domain-knowledge
E. Fine-tuning Code Language Models                                 distillation [57] to help the model learn code syntaxes and
                                                                    semantics.
To answer RQ2, we conduct the first experiment to fine-tune
ten CLMs for the APR task. Since the APR training data are          G. Patch Generation and Validation
pairs of buggy code and fixed code, we provide the buggy
code as part of the prompts to CLMs so that they can learn to       For all experiments, we let each tool (CLMs, fine-tuned CLMs,
generate fixed code given buggy code (Figure 4). Similar to         or DL-based APR techniques) generate ten candidate patches
RQ1, to make the comparison among fine-tuned code language          for each bug and run the developer-written test cases on
models fair, we use the same prompt, i.e., input to the models,     the patched program. The first patched program that passes
for all language models. We fine-tune the CLMs to directly          all the test cases is considered a plausible patch. And we
output the patched lines, the same as the output of DL-based        finally manually check the correctness of plausible patches
APR techniques.                                                     to distinguish correct patches (which should be identical or
   For the training data for fine-tuning, we use the APR            semantically equivalent to developer-written patches).
data shared in previous work [10], which is collected from
                                                                                  IV. RQ1: F IXING C APABILITIES
commits of open-sourced GitHub Java projects, and treat each
single-hunk fix as a separate instance, which contains 143,666      Table II shows the fixing capabilities of the ten CLMs and
instances in total. The dataset is randomly split into a training   three state-of-the-art DL-based APR techniques on four bug
dataset with 129,300 instances and a validation dataset with        benchmarks, including our new HumanEval-Java. We report
14,366 instances to tune the hyper-parameters (e.g., number         the number of correct patches within the top ten patches
of training epochs).                                                generated by each technique since recent work shows that 93%
   For all the CLMs, we apply the same setting for fine-            of developers are only willing to review up to ten patches [22].
tuning. Specifically, the batch size is one (due to our hardware    The results of CLMs are obtained and reported without feeding
constraints). We use the Adam optimizer [53] with a learning        buggy lines, as CLMs fix more bugs without buggy lines
rate of 1e−5 to update the model weights. CLMs are only fine-       information (analyzed in Section IV-B).
tuned for one epoch over the APR dataset, as they converge
fast on the validation dataset. We set a fixed random seed          A. Comparison between CLMs and DL-based APR Techniques
when fine-tuning different models to minimize variance for a        Table II shows that different types of CLMs perform signifi-
consistent, fair comparison.                                        cantly differently when applied to APR without fine-tuning. In
   Benchmarks       #Bugs     PLBART               CodeT5             CodeGen                                     InCoder         DL-based APR Techniques
                             base large    small    base  large   350M    2B  6B                                 1B    6B      CURE  Reward   Recoder   KNOD
   Defects4J v1.2      130     13    13       1        0      1       4   11  11                                 10    16         6       20       24      20
   Defects4J v2.0      108      9     8       2        4      1       3    4   8                                 10    15         6        8       11      13
   QuixBugs             40     11    12       3        0      3       7   15  16                                 14    15         5        7        6      10
   HumanEval-Java      164     39    52       3        5      6      30   49  46                                 40    59        18       22       11      18
   Total               442     72    85       9        9     11      44   79  81                                 74 105          35       57       52      61

TABLE II: Number of correct fixes generated by the ten CLMs (without fine-tuning), and four DL-based APR techniques.
Reward denotes RewardRepair.

general, PLBART models, CodeGen models (except CodeGen-              deletes return, which even makes the function uncompilable,
350M), and InCoder models fix more bugs than APR tools               Recoder’s patch replaces a with b, and KNOD’s patch replaces
in the four APR benchmarks combined (Row ‘Total’), while             b with a.
CodeT5 models fix the fewest. Specifically, InCoder-6B fixes
                                                                      Finding 1: CLMs have competitive fixing capabilities
the most number (105) of bugs, which is 72% more than the
                                                                      even without fine-tuning. PLBART, CodeGen, and InCoder
best DL-based APR technique, KNOD. The second best is
                                                                      models fix more bugs and generate more compilable
PLBART-large, which fixes 85 bugs and is 39% more than
                                                                      patches than state-of-the-art DL-based APR techniques,
KNOD. The poor result of CodeT5 models might be due to
                                                                      while CodeT5 models, as an exception, generate poor
that it is pre-trained for significantly different tasks [24], in-
                                                                      patches before fine-tuning.
cluding code-to-code generation, code-to-identifier-tag predic-
tion, and code-to-natural-language generation. Thus, without         B. Impact of Buggy Lines
fine-tuning them for the APR task, CodeT5 models cannot
generate reasonable code or correct patches.


                                                                           Compilation Rate on Each Bug
                                                                                                      1.0
   Figure 5 shows the distributions of the compilation rate of
                                                                                                      0.8
patches generated for bugs in all benchmarks by each model.
                                                                                                      0.6
CodeGen models generate the most compilable patches, with
an average compilation rate of 73% and a median of 97%.                                               0.4
PLBART and InCoder models also generate much more com-                                                0.2
pilable patches than DL-based APR techniques. DL-based                                                0.0
                                                                                                            PLBART CodeT5 CodeGen InCoder CURE Reward Recoder KNOD
APR techniques are only able to generate 44%–62% com-
pilable patches on average.                                          Fig. 5: Distributions of compilation rates of the ten patches
   CLMs and DL-based APR techniques have different fixing            generated for each bug from all four benchmarks.
capabilities on different benchmarks. Specifically, DL-based
APR techniques have better fixing capabilities than CLMs on
                                                                      public double getPct(Object v) {
Defects4J v1.2. Figure 6(a) shows an example (Math-75) in             -    return getCumPct((Comparable<?>) v);              Buggy line
                                                                      +    return getPct((Comparable<?>) v);                 APR tools' patch
Defects4J v1.2 that all three DL-based APR techniques fix but         +    return (double ) v ;                              PLBART's patch
all ten CLMs fail to fix. This bug has little context. Without        +    if (v instanceof Number)                          CodeGen's patch
                                                                      +         return ((Number) v).doubleValue();
enough context, although CLMs can generate reasonable code,           +    else if (v instanceof Boolean)
                                                                      +         return ((Boolean) v).booleanValue()? 1.0 : 0.0;
they fail to generate the correct fix. Regardless of providing the    +    else if (v instanceof String)
                                                                      +         return Double.parseDouble((String) v);
buggy line return getCumPct((Comparable<?>) v); to                    +    else return 0.0;
                                                                      +    Number n = (Number) v;                            InCoder's patch
the CLMs or not, all CLMs fail to fix this bug. As shown              +    return n.doubleValue() * 100.0;
later in Section IV-B, CLMs without fine-tuning make poor             }

use of the buggy lines. In contrast, APR tools are designed to       (a) Math-75 bug in Defects4J v1.2 that DL-based APR techniques fix but CLMs
leverage the buggy line information and thus fix this bug.           do not.
   In contrast, on QuixBugs and HumanEval-Java benchmarks,            public static int gcd(int a, int b) {
PLBART, CodeGen and InCoder models show much better fix-                   if (b == 0) return a;
                                                                      -    else return gcd(a % b, b);                                                Buggy Line
ing capabilities than APR tools. Figure 6 (b) shows an example        +    else return gcd(b, a % b);                                                CLMs' patch
                                                                      +    else return gcd(a, b);                                                    CURE's patch
(GCD) in QuixBugs that PLBART, CodeGen and InCoder                    +    gcd(a % b, b);                                                            RewardRepair's patch
                                                                      +    else return gcd(b % b, b);                                                Recoder's patch
models can fix but APR tools cannot. Although CLMs do                 +    else return gcd(a % b, a);                                                KNOD's patch
not see the buggy line else return gcd(a % b, b);, they               }

have learned from natural language text or code corpus that
                                                                      (b) GCD in QuixBugs that CLMs fix but DL-based APR techniques do not.
gcd stands for greatest common divisor, and can complete the
function correctly. By contrast, APR tools rely on the buggy         Fig. 6: Examples of bugs on which CLMs and DL-based APR
line a lot when generating candidate patches. Their patches          tools perform differently.
look like applying simple edit operations on the buggy line
without considering code syntax and semantics carefully. i.e.,       Table III shows the number of correct fixes over four bench-
CURE’s patch replaces a % b with a, RewardRepair’s patch             marks generated by CLMs when buggy lines are given. For
                                  PLBART                          CodeT5                         CodeGen                    InCoder
                               base    large            small       base  large        350M         2B         6B        1B         6B
                             36 (-36) 62 (-23)          5 (-4)     2 (-7) 4 (-7)      28 (-16)    58 (-21)   73 (-8)   61 (-13)  99 (-6)

TABLE III: Number of correct fixes generated by CLMs with buggy lines provided. Numbers in () are the reduction compared
to those without buggy lines.

public static Integer next_smallest(int[] lst) {
+    Set<Integer> numbers = new HashSet<Integer>();
                                                                        Although CLMs fix fewer bugs when buggy lines are
                                                      CLMs' patch w/o buggy line
     for (Integer n : lst)
         numbers.add(n);
                                                                     given, they fix some unique bugs with the help of buggy
     Integer[] no_duplicate = numbers.toArray(new Integer[] {});
public static Integer next_smallest(int[] lst) {
                                                                     lines. Figure 7(b) shows such an example, Chart-8, from
     // buggy line: List<Integer> numbers = new ArrayList<Integer>();Defects4J v1.2. Without the buggy line, CLMs’ patches are
+    if (lst == null) return null;                    PLBART's patch w/ buggy line
     for (Integer n : lst)                                           incorrect for this bug as they do not have enough context
         numbers.add(n);
     Integer[] no_duplicate = numbers.toArray(new Integer[] {});     to generate the correct patch. When the buggy line is given,
(a) PLBART generates incorrect patch for NEXT SMALLEST in HumanEval- they all can generate the correct patch this(time, zone,
Java with the buggy line given.                                      Local.getDefault());.
public static String flip_case(String string) {
     ...
                                                                                         Finding 2: Although buggy lines enable CLMs to fix some
     for (int i = 0; i < char_list.length; i += 1) {
         char c = char_list[i];
                                                                                         bugs, CLMs fail to make good use of the buggy lines.
         if (Character.isLowerCase(c)) {                                                 CLMs generate fewer compilable patches and fix fewer
+            char_list[i]=Character.toUpperCase(c); CLM's patch w/o buggy line
 public static String flip_case(String string) {                                         bugs overall when buggy lines are given.
      ...
      for (int i = 0; i < char_list.length; i += 1) {
          char c = char_list[i];
          if (Character.isLowerCase(c)) {
              // buggy line: char_list[i]=Character.toLowerCase(c);
                                                                                                        V. RQ2: I MPACT OF F INE - TUNING
 +                                                    CodeGen's patch w/ buggy line
 +            char_list[i]=Character.toLowerCase(c); InCoder's patch w/ buggy line      A. Fixing Capabilities of Fine-tuned CLMs
(b) CodeGen and InCoder generate incorrect patches for FLIP CASE in                     Table IV shows the number of correct fixes generated by
HumanEval-Java with the buggy line given.                                               the ten CLMs after fine-tuning. Overall, all CLMs fix more
public Week(Date time, TimeZone zone) {
                                                                                        bugs after fine-tuning, with a 31%–1,267% improvement.
+    super(time, zone);                             PLBART's patch w/o buggy line       As a result, fine-tuned CLMs consistently outperform DL-
+    this.time = time; this.zone = zone;            CodeGen's patch w/o buggy line
+    super(); this.time = time; this.zone = zone;   InCoder's patch w/o buggy line      based APR techniques over four benchmarks. The best model,
}
public Week(Date time, TimeZone zone) {                                                 InCoder-6B, fixes 100 (164%) more bugs than the best DL-
     // buggy line: this(time, RegularTimePeriod.DEFAULT_TIME_ZONE,
     // buggy line:      Locale.getDefault());                                          based APR technique.
+    this(time, zone, Locale.getDefault());         CLM's patch w/ buggy line
}                                                                                          Regarding the impact of fine-tuning, CodeT5 models gain
  (c) CLMs fix Chart-8 in Defects4J v1.2 only with the buggy line given.                the most improvement (889%–1,267%) and PLBART models
                                                                                        gain the least improvement (31%). Although multi-task pre-
Fig. 7: Bug examples on which CLMs perform differently                                  training [24] makes CodeT5 models generate poor code before
when buggy lines are given versus not given.                                            fine-tuning, they indeed learn general programming language
                                                                                        knowledge from pre-training, which helps CodeT5 models
example, “36 (-36)” shows that PLBART-base fixes 36 bugs                                learn great fixing capability from fine-tuning. For PLBART
with buggy lines provided as input, while PLBART-base fixes                             models, a surprising result is that the PLBART-large model
72 bugs without buggy lines. To our surprise, all CLMs                                  fixes four fewer bugs on the HumanEval-Java benchmark after
consistently fix 6%–78% fewer bugs when buggy lines are                                 fine-tuning, which we tried to explain in Section V-B.
given.
   To understand the reason, Figure 7(a) shows an example,                               Finding 3: Fine-tuning with APR data improves all ten
bug NEXT SMALLEST from HumanEval-Java, for which                                         CLMs’ fixing capabilities, and fine-tuned CLMs fix sig-
CLMs generate the correct patch without having the buggy                                 nificantly 100 (164%) more bugs than the state-of-the-art
line. This shows the models understand no_duplicate in                                   DL-based APR techniques on the four benchmarks.
the context and thus initializes numbers as a HashSet.
Yet, when the buggy line List<Integer> numbers = new                                    B. Pre-trained versus Fine-tuned CLMs
ArrayList<Integer>(); is given, PLBART fails to fix it                                  Figure 8(a) shows an example that all the CLMs can fix
anymore, generating an uncompilable patch where numbers is                              only after fine-tuning. Without fine-tuning, CodeT5 models
undeclared. Figure 7(b) shows another example, FLIP CASE                                generate incorrect patches that are irrelevant to the buggy
from HumanEval-Java, that CodeGen and InCoder generate                                  line, PLBART and CodeGen models generate patches that are
incorrect patches when the buggy lines are given. CodeGen’s                             equivalent to the buggy lines, and InCoder models delete the
patch deletes the whole buggy line and InCoder’s patch simply                           buggy line. This supports our Finding 2 that CLMs fail to
repeats the buggy line, which shows that CLMs are confused                              utilize the buggy line information well (CLMs also fail to fix
by the buggy lines, and try to follow the given buggy code                              this bug without the buggy lines). Yet, after fine-tuning, all
instead of generating the correct code. This is explainable as                          CLMs learn to make use of the buggy lines to generate the
CLMs are not pre-trained to utilize the buggy lines.                                    correct patches.
 Benchmarks           #Bugs          PLBART                        CodeT5                                                 CodeGen                      InCoder                DL-based APR Techniques
                                     base large           small       base          large    350M                             2B          6B           1B         6B         CURE Reward Recoder KNOD
 Defects4J v1.2          130     25 (12) 29 (16)        19 (18)     30 (30)    33 (32)      23 (19)                         32 (21)   38 (27)      27 (17)    41 (25)            6        20          24       20
 Defects4J v2.0          108      13 (4) 17 (9)         15 (13)     17 (13)    19 (18)      20 (17)                         23 (19)   23 (15)      24 (14)    28 (13)            6         8          11       13
 QuixBugs                 40      15 (4) 17 (5)         14 (11)     15 (15)    19 (16)      18 (11)                          18 (3)    18 (2)       18 (4)     22 (7)            5         7           6       10
 HumanEval-Java          164      41 (2) 48 (-4)        41 (38)     54 (49)    54 (48)      52 (22)                          53 (4)    52 (6)      64 (24)    70 (11)           18        22          11       18
 Total                   442     94 (22) 111 (26)       89 (80) 116 (107) 125(114)          96 (69) 126 (47) 131 (50)                             133 (59)   161 (56)           35        57          52       61

TABLE IV: Number of correct fixes generated by the ten fine-tuned CLMs and four DL-based APR techniques. Numbers in
() are the improvement gained by fine-tuning. Reward stands for RewardRepair.

public static String next_palindrome(int[] digit_list) {
     ArrayList<Integer> otherwise = new ArrayList<Integer>();                                                                                           71              73           76
     otherwise.add(1);                                                                                                   70                                             64                             70
     // buggy line: otherwise.addAll(                                                                                                                   61              59           59
                                                                                                                         60 54 (w/)




                                                                                               Number of Correct Fixes
     // buggy line:    Collections.nCopies(digit_list.length, 0));
                                                                                                                                            51                                       52                54
                                                    PLBART's patch w/o fine-tuning                                                                      51                                               52
+    otherwise.addAll(Arrays.asList(digit_list));
                                                                                                                         50 47 (w/)
+    otherwise = new ArrayList<Integer>();          CodeT5's patch w/o fine-tuning                                                          48                          42           49                48
+
+
     for (int i = 0; i < digit_list.length; i++){
         otherwise.add(digit_list[i]);
                                                    CodeGen's patch w/o fine-tuning
                                                                                                                         40 38 (w/)
                                                                                                                                                        32
+
+
     }
                                                    InCoder's patch w/o fine-tuning
                                                                                                                         30                 27
                                                                                                                                            22                                                   InCoder
+    otherwise.addAll(                              Fine-tuned CLMs' patch                                               20
+        Collections.nCopies(digit_list.length-1, 0));                                                                                                                                           CodeGen
                                                                                                                         10                                                                      CodeT5
 (a) NEXT PALINDROME in QuixBugs that CLMs only fix w/ fine-tuning.                                                                                                                              PLBART
                                                                                                                          0      1 (w/)
public SORT_NUMBERS(String numbers) {                                                                                    0 (no fine-tuning) 100        1000            10K           50K       129K (full dataset)
     HashMap<String, Integer> value_map = new HashMap<String, Integer>()                                                                             Size of Fine-tuning Data
     {{ put("zero", 0); put("one", 1); put("two", 2);... }}
     ArrayList<String> number_array = new ArrayList<String(
         Arrays.asList(numbers.split(" ")));                                                  Fig. 9: Number of correct fixes for HumanEval-Java generated
+    Collections.sort(number_array,                   CLMs' patch w/o fine-tuning
+        (a, b) -> value_map.get(a).compareTo(value_map.get(b)));
                                                                                              by CLMs that are fine-tuned with different-sized APR data.
public SORT_NUMBERS(String numbers) {                                                         (w/) stands for applying CLMs (not fine-tuned) with feeding
     ...
     ArrayList<String> number_array = new ArrayList<String(                                   buggy lines.
         Arrays.asList(numbers.split(" ")));
     // buggy line: Collections.sort(number_array);
+    Arrays.sort(number_array);                       Fine-tuned PLBART's patch               C. Impact of Fine-tuning Data Size
+    Collections.sort(number_array, new String[0]);   Fine-tuned CodeGen's patch
+    number_array.sort();                             Fine-tuned InCoder's patch
+    Collections.sort(number_array);                                   Figure 9 shows the number of correct fixes that CLMs gen-
                                                      CURE and Recoder's patch
+    Collections.sort(number_array.trim());           RewardRepair's patch
+    Collections.odd_count(number_array);             KNOD's patch
                                                                       erate on the HumanEval-Java benchmark when they are fine-
                                                                       tuned with different-sized APR data. CodeT5-large gains a
(b) SORT NUMBERS in HumanEval-Java that CLMs only fix w/o fine-tuning.
                                                                       great improvement after being fine-tuned with only 100 APR
Fig. 8: Examples of bugs on which CLMs perform differently training instances and reaches its best fixing capability (59)
after fine-tuning.                                                     after being fine-tuned with 10,000 instances. CodeGen-6B also
                                                                       fixes the most number of bugs after being fine-tuned with
    Figure 8 (b) shows an opposite example that CLMs can 10,000 instances. Both models share a common pattern that if
fix only without fine-tuning. PLBART, CodeGen and InCoder the fine-tuning data increases from 10,000 to the full dataset
models fix this bug without fine-tuning and without the (129,000), they start to fix fewer bugs.
buggy line provided, which shows that they understand that                InCoder-6B fixes fewer bugs after being fine-tuned with 100
number_array is an array of numbers written in English, APR training instances (51), but its fixing capability keeps
and should be sorted according to their numerical values increasing and reaches the best (76) after being fine-tuned with
(stored in value_map). This reveals CLMs’ strong capabilities 50,000 instances.
of understanding code semantics. Yet, after fine-tuning, they             PLBART-large shows a different pattern that its fixing capa-
all generate incorrect patches. It is surprising that the fine- bility keeps a relatively stable growth as the fine-tuning data
tuned CLMs make a similar mistake as the DL-based APR increases. Yet, the fine-tuned PLBART-large model always
techniques (which also fail to fix this bug) that their patches fixes fewer bugs than the pre-trained PLBART-large (i.e.,
rely on the buggy line too much, failing to figure out the target without fine-tuning) without the buggy lines given.
functionality from the context.
                                                                         Finding 5: CodeT5, CodeGen, and InCoder models reach
  Finding 4: Fine-tuning with APR data enables CLMs to                   the best fixing capabilities after being fine-tuned with
  better leverage buggy lines to fix more bugs. Yet, it also             10,000 and 50,000 APR instances, yet too much fine-
  makes CLMs share a common shortcoming of DL-based                      tuning data makes them fix fewer bugs. The best fine-tuned
  APR techniques that they miss some bugs if they over-rely              PLBART model still fails to outperform the pre-trained
  on the buggy lines. Overall, fine-tuned CLMs have the best             PLBART models.
  fixing capabilities.
                                                                                                                           VI. RQ3: S IZE , T IME , AND M EMORY E FFICIENCY
                                                                                              Figure 10 (a) shows the number of correct fixes that the
                                                                                              ten fine-tuned CLMs generate as the CLMs’ number of
                                             (a) Size Efficiency                                         (b) Time Efficiency                                             (c) Memory Efficiency
                 160                                                            6B                                     6B                                                                                    6B
                 140                                           1B                                      1B                                                                              1B
                                                       large                   6B                                                                                                     large
                 120                   base large                      2B                     large base large                  2B 6B                                    baselarge            2B        6B
#Correct Fixes




                 100
                        small       base       350M                                        base small          350M                                       small base     350M
                  80                                                        InCoder
                  60      KNOD
                           Reward                                           CodeGen                    Reward                KNOD                         KNOD Reward
                          Recoder                                           CodeT5                                                          Recoder          Recoder
                  40        CURE                                            PLBART                                              CURE                              CURE
                       50     100      200      400     800     1600   3200 6400 (M) 0.5        1       2         4         8          16        32 (s)   0.5        1      2         4       8    16         32 (GB)
                                           Number of Parameters                                     Generation Time Per Correct Fix                                             GPU Memory

                                                                            Fig. 10: Size, time and memory efficiency of CLMs.

 parameters grows. Larger models with more parameters con-                                                            niques. Thus, it is promising to build future APR techniques
 sistently exhibit better fixing capability than smaller models.                                                      based on CLMs instead of training from scratch.
 Fine-tuned CodeT5 and InCoder models always fix the most                                                                Yet, the fine-tuning applied in this work is straightforward
 number of bugs compared with other models that have a                                                                and simple. Existing DL-based APR techniques have APR-
 similar number of parameters, i.e., CodeT5 and InCoder are                                                           specific designs, such as code-syntax guided beam search [7],
 the most size-efficient. Fine-tuned PLBART models have the                                                           leveraging AST structural information [10], and learning exe-
 second-best size efficiency, and CodeGen models are the least                                                        cution information [9], which existing CLMs do not have yet.
 size-efficient. The result suggests that pre-training and fine-                                                      Incorporating syntax and structural information or test cases
 tuning larger CodeT5 or InCoder models are promising, which                                                          execution information into fine-tuning may further improve the
 remains as future work since we already evaluated the largest                                                        fixing capabilities of CLMs.
 models released.                                                                                                     Addressing over-reliance on buggy lines: Fine-tuned CLMs
    In addition to size efficiency, we study CLMs’ time effi-                                                         share a common shortcoming with existing DL-based APR
 ciency. Figure 10 (b) shows the GPU time in seconds that each                                                        techniques, which is the over-reliance on buggy lines. It might
 CLM takes to generate a correct fix. PLBART models have                                                              be caused by model biases to favor small changes to fix
 the best time efficiency in generating patches, taking 0.70–                                                         bugs and that fixes to most bugs in the training set are small
 0.89 seconds on average to generate a correct patch. CodeGen                                                         changes [7]. Yet, this makes fixing bugs that require larger
 models, although fixing more bugs than PLBART models,                                                                modifications to the buggy lines extra challenging. Possible
 are the least time-efficient and require 3.64–13.88 seconds on                                                       solutions include balancing different bugs in the fine-tuning
 average to generate a correct patch.                                                                                 APR dataset, or developing separate models especially for
    Memory requirement, or memory efficiency, is also an                                                              bugs requiring big modifications.
 important consideration for practical usage. Figure 10 (c)
 shows the requirement of GPU memory (in GB) to apply                                                                 B. Larger CodeT5 and InCoder Models
 each CLM on the four benchmarks. The CodeGen-6B and                                                                  Our Finding 6 shows that CodeT5 and InCoder models have
 InCoder-6B models require 19.84–24.81GB GPU memory to                                                                better size efficiency. Thus, pre-training and fine-tuning larger-
 run, which is significantly more than other CLMs. In contrast,                                                       sized CodeT5 and InCoder models is a promising direction to
 the other CLMs can easily fit into a single card with standard                                                       fix more bugs.
 8GB or 12GB memory. Overall, CodeT5 and InCoder models
 always fix more bugs than PLBART and CodeGen given the                                                               C. Fair and Comprehensive Evaluation
 same memory limitations.                                                                                             Improving benchmarks: Good benchmarks are crucial for
    We also include the size, time and memory efficiency of                                                           evaluating and comparing CLMs. This work releases a new
 Dl-based APR techniques in figure 10. All CLMs fix more                                                              benchmark HumanEval-Java that is not only more realistic
 bugs than DL-based APR techniques given the same number                                                              than the code-refinement dataset in CodeXGLUE for the APR
 of parameters, time, and memory.                                                                                     task, but also not included in CLMs’ pre-training data. Yet,
                                                                                                                      HumanEval-Java contains mostly small programs. An APR
         Finding 6: CodeT5 and InCoder models show the best                                                           benchmark that consists of larger buggy programs (and also
         size efficiency, thus it is more promising to develop larger                                                 not seen by CLMs) is still needed.
         CodeT5 and InCoder models than the others. PLBART,
                                                                                                                      Avoiding benchmark leaking in pre-training: CLMs rely on
         CodeT5 and InCoder models all have better time efficiency
                                                                                                                      enormous code corpora to pre-train, which brings a threat that
         and memory efficiency than CodeGen models, and thus are
                                                                                                                      existing APR benchmarks such as Defects4J may be (partially)
         better choices given limited resources.
                                                                                                                      included in their pre-training datasets. It is impractical to limit
                            VII. I MPLICATIONS AND F UTURE W ORK                                                      the pre-training dataset of CLMs, as data is a crucial part and
                                                                                                                      contribution of techniques. But we call for clearer reporting
 A. Fine-tuning CLMs for APR                                                                                          and documentation of open-source repositories used in the pre-
 Improving fine-tuning: Fine-tuned CLMs have much better                                                              training data of future CLM work to address the benchmark
 fixing capabilities than state-of-the-art DL-based APR tech-                                                         leaking problem.
Evaluating size, time, and memory efficiency: In addition                   discussed in Section I-A,(1) their performance is reported
to the overall fixing capabilities, size efficiency shows which             by BLEU score [58], which could be misleading and dif-
type of model is more promising to develop with larger sizes.               ferent from real-world benchmarks such as Defects4J [40].
Time and memory efficiency show which models perform the                    As the BLEU score only measures the similarity between
best given limited resources. To make more comprehensive                    the generated function with the correct function, and since
evaluations of CLMs in future work, size, time, and memory                  no test cases are executed, the reported score cannot really
efficiency should also be evaluated and reported.                           tell how many bugs can be correctly fixed by these code
                                                                            language models. And (2) they do not study the characteristics
       VIII. T HREATS TO VALIDITY AND L IMITATIONS                          of the programs generated by CLMs, nor study the impact
One threat to the evaluation of all CLM papers [23], [24], [35]             of feeding buggy lines, and (3) they do not compare CLMs’
is that the training data of these CLMs may contain the bugs                fixing capabilities with DL-based APR tools. Thus, our work
or fixes in the four APR benchmarks since these CLMs use                    is different by providing a comprehensive, in-depth study of
public repositories such as all GitHub repositories by a certain            the fixing capabilities of ten CLMs, with more details about
date [23], [24], [35]. This threat exists for all CLM-related               the impact of buggy lines, fine-tuning data size and their size,
papers, not just this paper. But this threat is less of a concern           time, and memory efficiency.
since CLMs do not see the pair of bugs and their fixed code
                                                                            B. Automated Program Repair
during training, and their training data often contains at most
the buggy code or the fixed code, but not both. We mitigate                 Many template- [14], [15], heuristic- [16]–[18], constraint-
this threat by using an evaluation benchmark HumanEval-Java                 [19]–[21], and DL-based APR techniques [4]–[6], [8] have
that has not been seen by any of the CLMs during training.                  been developed and evaluated on Defects4J and QuixBugs
   We exclude the state-of-the-art code language model                      benchmarks. None of these papers is fully built on large pre-
Codex [36] from the results section because Codex is a black                trained CLMs, and they all fix fewer bugs than the three DL-
box, and one cannot fine-tune it. Fine-tuning Codex remains                 based APR techniques studied in this work. Other DL-based
future work if Codex releases fine-tuning APIs in the future.               techniques fix compilation bugs and syntax issues [59]–[61]
We did apply Codex without fine-tuning on the four APR                      instead of runtime bugs. Thus, the novelty, conclusion, and
benchmarks. Codex correctly fixes 41 bugs from Defects4J                    implications of this work are not affected.
v1.2, 27 bugs from Defects4J v2.0, 34 bugs from QuixBugs,                                         X. C ONCLUSION
and 71 bugs from HumanEval-Java (173 in total). While Codex
                                                                            This paper studies the impact that CLMs bring to the APR
seems highly effective, it is particularly susceptible to the data-
                                                                            domain. We apply ten CLMs with and without fine-tuning on
leaking threat, because Codex models keep updating with the
                                                                            four APR benchmarks, including a new benchmark created
latest open-source data and potential user input2 . Making a
                                                                            in this work. Experiments show CLMs’ competitive fixing
solid and fair evaluation of Codex remains an important and
                                                                            capabilities, with the best CLM fixing 72% more bugs than
challenging future work.
                                                                            the state-of-the-art DL-based APR techniques. Fine-tuning
   Another threat lies in the evaluation of patch correctness.              also significantly improves CLMs, enabling CLMs to fix
Instead of using automated metrics such as BLEU [58] and                    31%–1,267% more bugs and outperform the best DL-based
CodeBLEU [39], we manually check if the patches pass the                    APR technique by 46%–164%. Thus, this paper shows that
test cases are semantically equivalent to the developer patches,            developing APR techniques based on CLMs, bringing APR-
which could be subjective. Yet, our experiments show BLEU                   specific designs into the fine-tuning process of CLMs, and
and CodeBLUE are indeed misleading in comparing APR                         addressing the over-reliance on buggy lines are promising
techniques. The CodeBLUE score of RewardRepair’s patches                    future directions to explore. In addition, this work also calls
on the HumanEval-Java benchmark is 36.76, higher than the                   for awareness of fair and comprehensive evaluation of CLMs,
fine-tuned CodeT5 model (33.47), but it fixes 19 fewer bugs.                including avoidance of data leaking and reporting of size, time,
We suspect this is because CLMs generate patches with more                  and memory efficiency.
diversity, and thus better automated metrics are needed.
                                                                                              XI. DATA AVAILABILITY
                        IX. R ELATED W ORK
                                                                            Our replication package, including (1) the new APR bench-
A. Language Models on Code Refinement                                       mark HumanEval-Java, (2) the generated patches for all four
CLMs, including CodeBERT, GraphCodeBERT, PLBART,                            benchmarks by all CLMs, (3) the fine-tuned CLM models, and
and CodeT5 [24], have been studied for code refinement.                     (4) the source code for reproduction are available at [62].
These models are fine-tuned on the code refinement dataset                                      ACKNOWLEDGMENT
offered by CodeXGLUE [39], where the input to the model
                                                                            We thank the reviewers for their insightful comments and
is an abstracted buggy function, and the models are trained
                                                                            suggestions. This work is partially supported by a J.P. Morgan
to generate the patched correct function. However, as we
                                                                            AI Faculty Research Award. Any opinions, findings, and
  2 https://help.openai.com/en/articles/5722486-how-your-data-is-used-to-   conclusions in this paper are those of the authors only and
improve-model-performance                                                   do not necessarily reflect the views of our sponsors.
                              R EFERENCES                                        [19] Y. Xiong, J. Wang, R. Yan, J. Zhang, S. Han, G. Huang, and L. Zhang,
                                                                                      “Precise condition synthesis for program repair,” in 2017 IEEE/ACM
 [1] M. Monperrus, “The living review on automated program repair,” 2020.             39th International Conference on Software Engineering (ICSE), 2017,
 [2] C. L. Goues, M. Pradel, and A. Roychoudhury, “Automated program                  pp. 416–426.
     repair,” Commun. ACM, vol. 62, no. 12, pp. 56–65, 2019. [Online].           [20] J. Xuan, M. Martinez, F. Demarco, M. Clement, S. R. L. Marcote,
     Available: https://doi.org/10.1145/3318162                                       T. Durieux, D. L. Berre, and M. Monperrus, “Nopol: Automatic
 [3] M. Monperrus, “Automatic software repair: A bibliography,” ACM                   repair of conditional statement bugs in java programs,” IEEE Trans.
     Comput. Surv., vol. 51, no. 1, pp. 17:1–17:24, 2018. [Online]. Available:        Software Eng., vol. 43, no. 1, pp. 34–55, 2017. [Online]. Available:
     https://doi.org/10.1145/3105906                                                  https://doi.org/10.1109/TSE.2016.2560811
 [4] Z. Chen, S. Kommrusch, M. Tufano, L.-N. Pouchet, D. Poshyvanyk,             [21] M. Martinez and M. Monperrus, “Ultra-large repair search space
     and M. Monperrus, “SequenceR: Sequence-to-Sequence Learning for                  with automatically mined templates: The cardumen mode of astor,” in
     End-to-End Program Repair,” TSE, 2019.                                           Search-Based Software Engineering - 10th International Symposium,
 [5] Y. Li, S. Wang, and T. N. Nguyen, “DLFix: Context-Based Code                     SSBSE 2018, Montpellier, France, September 8-9, 2018, Proceedings,
     Transformation Learning for Automated Program Repair,” in ICSE.                  ser. Lecture Notes in Computer Science, T. E. Colanzi and P. McMinn,
     ACM, 2020, p. 602–614.                                                           Eds., vol. 11036. Springer, 2018, pp. 65–86. [Online]. Available:
 [6] T. Lutellier, H. V. Pham, L. Pang, Y. Li, M. Wei, and L. Tan, “CoCoNuT:          https://doi.org/10.1007/978-3-319-99241-9 3
     Combining Context-Aware Neural Translation Models Using Ensemble            [22] Y. Noller, R. Shariffdeen, X. Gao, and A. Roychoudhury, “Trust
     for Program Repair,” in ISSTA. ACM, 2020, p. 101–114.                            enhancement issues in program repair,” in Proceedings of the 44th
 [7] N. Jiang, T. Lutellier, and L. Tan, “Cure: Code-aware neural machine             International Conference on Software Engineering, ser. ICSE ’22.
     translation for automatic program repair,” in 2021 IEEE/ACM 43rd                 New York, NY, USA: Association for Computing Machinery, 2022,
     International Conference on Software Engineering (ICSE), 2021, pp.               p. 2228–2240. [Online]. Available: https://doi.org/10.1145/3510003.
     1161–1173.                                                                       3510040
 [8] S. Chakraborty, Y. Ding, M. Allamanis, and B. Ray, “Codit: Code             [23] W. Ahmad, S. Chakraborty, B. Ray, and K.-W. Chang, “Unified pre-
     editing with tree-based neural models,” IEEE Transactions on Software            training for program understanding and generation,” in Proceedings of
     Engineering, vol. 48, no. 4, pp. 1385–1399, 2022.                                the 2021 Conference of the North American Chapter of the Association
                                                                                      for Computational Linguistics: Human Language Technologies. Online:
 [9] H. Ye, M. Martinez, and M. Monperrus, “Neural program repair with
                                                                                      Association for Computational Linguistics, Jun. 2021, pp. 2655–2668.
     execution-based backpropagation,” in Proceedings of the International
                                                                                      [Online]. Available: https://aclanthology.org/2021.naacl-main.211
     Conference on Software Engineering, 2022. [Online]. Available:
     http://arxiv.org/pdf/2105.04123                                             [24] W. Yue, W. Weishi, J. Shafiq, and C. H. Steven, “Codet5: Identifier-aware
[10] Q. Zhu, Z. Sun, Y.-a. Xiao, W. Zhang, K. Yuan, Y. Xiong,                         unified pre-trained encoder-decoder models for code understanding
     and L. Zhang, “A syntax-guided edit decoder for neural program                   and generation,” in Proceedings of the 2021 Conference on Empirical
     repair,” in Proceedings of the 29th ACM Joint Meeting on European                Methods in Natural Language Processing, EMNLP 2021, 2021.
     Software Engineering Conference and Symposium on the Foundations            [25] A. Radford, K. Narasimhan, T. Salimans, and I. Sutskever, “Improving
     of Software Engineering. New York, NY, USA: Association                          language understanding by generative pre-training,” 2018.
     for Computing Machinery, 2021, p. 341–353. [Online]. Available:             [26] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever,
     https://doi.org/10.1145/3468264.3468544                                          “Language models are unsupervised multitask learners,” 2019.
[11] N. Jiang, T. Lutellier, Y. Lou, L. Tan, D. Goldwasser, and X. Zhang,        [27] T. B. Brown, B. Mann, N. Ryder, M. Subbiah, J. Kaplan, P. Dhariwal,
     “Knod: Domain knowledge distilled tree decoder for automated program             A. Neelakantan, P. Shyam, G. Sastry, A. Askell, S. Agarwal,
     repair,” in Proceedings of the International Conference on Software              A. Herbert-Voss, G. Krueger, T. Henighan, R. Child, A. Ramesh,
     Engineering, 2023.                                                               D. M. Ziegler, J. Wu, C. Winter, C. Hesse, M. Chen, E. Sigler,
[12] Z. Chen, S. Kommrusch, and M. Monperrus, “Neural transfer                        M. Litwin, S. Gray, B. Chess, J. Clark, C. Berner, S. McCandlish,
     learning for repairing security vulnerabilities in c code,” IEEE                 A. Radford, I. Sutskever, and D. Amodei, “Language models are few-
     Transactions on Software Engineering, 2022. [Online]. Available:                 shot learners,” CoRR, vol. abs/2005.14165, 2020. [Online]. Available:
     http://arxiv.org/pdf/2104.08308                                                  https://arxiv.org/abs/2005.14165
[13] H. Ye, M. Martinez, X. Luo, T. Zhang, and M. Monperrus, “Selfapr:           [28] B. Wang and A. Komatsuzaki, “GPT-J-6B: A 6 Billion Parameter
     Self-supervised program repair with test execution diagnostics,” in              Autoregressive Language Model,” May 2021.
     Proceedings of ASE, 2022. [Online]. Available: http://arxiv.org/pdf/        [29] S. Black, G. Leo, P. Wang, C. Leahy, and S. Biderman, “GPT-Neo:
     2203.12755                                                                       Large Scale Autoregressive Language Modeling with Mesh-Tensorflow,”
[14] J. Jiang, Y. Xiong, H. Zhang, Q. Gao, and X. Chen, “Shaping program              Mar. 2021. [Online]. Available: https://doi.org/10.5281/zenodo.5297715
     repair space with existing patches and similar code,” in Proceedings of     [30] J. Devlin, M. Chang, K. Lee, and K. Toutanova, “BERT: pre-training
     the 27th ACM SIGSOFT International Symposium on Software Testing                 of deep bidirectional transformers for language understanding,” CoRR,
     and Analysis, ser. ISSTA 2018. New York, NY, USA: Association                    vol. abs/1810.04805, 2018. [Online]. Available: http://arxiv.org/abs/
     for Computing Machinery, 2018, p. 298–309. [Online]. Available:                  1810.04805
     https://doi.org/10.1145/3213846.3213871                                     [31] Y. Liu, M. Ott, N. Goyal, J. Du, M. Joshi, D. Chen, O. Levy,
[15] K. Liu, A. Koyuncu, D. Kim, and T. F. Bissyandé, “TBar: Revisiting              M. Lewis, L. Zettlemoyer, and V. Stoyanov, “Roberta: A robustly
     Template-Based Automated Program Repair,” in ISSTA. ACM, 2019.                   optimized BERT pretraining approach,” CoRR, vol. abs/1907.11692,
[16] Y. Yuan and W. Banzhaf, “ARJA: automated repair of java programs                 2019. [Online]. Available: http://arxiv.org/abs/1907.11692
     via multi-objective genetic programming,” IEEE Trans. Software              [32] M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy,
     Eng., vol. 46, no. 10, pp. 1040–1067, 2020. [Online]. Available:                 V. Stoyanov, and L. Zettlemoyer, “BART: denoising sequence-to-
     https://doi.org/10.1109/TSE.2018.2874648                                         sequence pre-training for natural language generation, translation, and
[17] M. Wen, J. Chen, R. Wu, D. Hao, and S. Cheung, “Context-aware                    comprehension,” CoRR, vol. abs/1910.13461, 2019. [Online]. Available:
     patch generation for better automated program repair,” in Proceedings            http://arxiv.org/abs/1910.13461
     of the 40th International Conference on Software Engineering, ICSE          [33] J. Zhang, H. Zhang, C. Xia, and L. Sun, “Graph-bert: Only attention is
     2018, Gothenburg, Sweden, May 27 - June 03, 2018, M. Chaudron,                   needed for learning graph representations,” CoRR, vol. abs/2001.05140,
     I. Crnkovic, M. Chechik, and M. Harman, Eds. ACM, 2018, pp.                      2020. [Online]. Available: https://arxiv.org/abs/2001.05140
     1–11. [Online]. Available: https://doi.org/10.1145/3180155.3180233          [34] S. Smith, M. Patwary, B. Norick, P. LeGresley, S. Rajbhandari,
[18] R. K. Saha, Y. Lyu, H. Yoshida, and M. R. Prasad, “ELIXIR:                       J. Casper, Z. Liu, S. Prabhumoye, G. Zerveas, V. Korthikanti, E. Zheng,
     effective object oriented program repair,” in Proceedings of the                 R. Child, R. Y. Aminabadi, J. Bernauer, X. Song, M. Shoeybi, Y. He,
     32nd IEEE/ACM International Conference on Automated Software                     M. Houston, S. Tiwary, and B. Catanzaro, “Using deepspeed and
     Engineering, ASE 2017, Urbana, IL, USA, October 30 - November                    megatron to train megatron-turing NLG 530b, A large-scale generative
     03, 2017, G. Rosu, M. D. Penta, and T. N. Nguyen, Eds.                           language model,” CoRR, vol. abs/2201.11990, 2022. [Online]. Available:
     IEEE Computer Society, 2017, pp. 648–659. [Online]. Available:                   https://arxiv.org/abs/2201.11990
     https://doi.org/10.1109/ASE.2017.8115675                                    [35] E. Nijkamp, B. Pang, H. Hayashi, L. Tu, H. Wang, Y. Zhou, S. Savarese,
     and C. Xiong, “A conversational paradigm for program synthesis,” arXiv            modeling,” CoRR, vol. abs/2101.00027, 2021. [Online]. Available:
     preprint, 2022.                                                                   https://arxiv.org/abs/2101.00027
[36] M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. de Oliveira Pinto,                [52] X. V. Lin, T. Mihaylov, M. Artetxe, T. Wang, S. Chen, D. Simig,
     J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, A. Ray,                  M. Ott, N. Goyal, S. Bhosale, J. Du, R. Pasunuru, S. Shleifer,
     R. Puri, G. Krueger, M. Petrov, H. Khlaaf, G. Sastry, P. Mishkin,                 P. S. Koura, V. Chaudhary, B. O’Horo, J. Wang, L. Zettlemoyer,
     B. Chan, S. Gray, N. Ryder, M. Pavlov, A. Power, L. Kaiser,                       Z. Kozareva, M. T. Diab, V. Stoyanov, and X. Li, “Few-shot learning
     M. Bavarian, C. Winter, P. Tillet, F. P. Such, D. Cummings,                       with multilingual language models,” CoRR, vol. abs/2112.10668, 2021.
     M. Plappert, F. Chantzis, E. Barnes, A. Herbert-Voss, W. H. Guss,                 [Online]. Available: https://arxiv.org/abs/2112.10668
     A. Nichol, A. Paino, N. Tezak, J. Tang, I. Babuschkin, S. Balaji, S. Jain,   [53] T. Wolf, L. Debut, V. Sanh, J. Chaumond, C. Delangue, A. Moi,
     W. Saunders, C. Hesse, A. N. Carr, J. Leike, J. Achiam, V. Misra,                 P. Cistac, T. Rault, R. Louf, M. Funtowicz, J. Davison, S. Shleifer,
     E. Morikawa, A. Radford, M. Knight, M. Brundage, M. Murati,                       P. von Platen, C. Ma, Y. Jernite, J. Plu, C. Xu, T. L. Scao, S. Gugger,
     K. Mayer, P. Welinder, B. McGrew, D. Amodei, S. McCandlish,                       M. Drame, Q. Lhoest, and A. M. Rush, “Transformers: State-of-
     I. Sutskever, and W. Zaremba, “Evaluating large language models                   the-art natural language processing,” in Proceedings of the 2020
     trained on code,” CoRR, vol. abs/2107.03374, 2021. [Online]. Available:           Conference on Empirical Methods in Natural Language Processing:
     https://arxiv.org/abs/2107.03374                                                  System Demonstrations. Online: Association for Computational
[37] Z. Feng, D. Guo, D. Tang, N. Duan, X. Feng, M. Gong, L. Shou,                     Linguistics, Oct. 2020, pp. 38–45. [Online]. Available: https:
     B. Qin, T. Liu, D. Jiang, and M. Zhou, “Codebert: A pre-trained model             //www.aclweb.org/anthology/2020.emnlp-demos.6
     for programming and natural languages,” CoRR, vol. abs/2002.08155,           [54] C. S. Xia and L. Zhang, “Less training, more repairing please: Revisiting
     2020. [Online]. Available: https://arxiv.org/abs/2002.08155                       automated program repair via zero-shot learning,” in Proceedings of
[38] D. Guo, S. Ren, S. Lu, Z. Feng, D. Tang, S. Liu, L. Zhou,                         the 30th ACM Joint European Software Engineering Conference
     N. Duan, A. Svyatkovskiy, S. Fu, M. Tufano, S. K. Deng,                           and Symposium on the Foundations of Software Engineering,
     C. B. Clement, D. Drain, N. Sundaresan, J. Yin, D. Jiang, and                     ser. ESEC/FSE 2022. New York, NY, USA: Association for
     M. Zhou, “Graphcodebert: Pre-training code representations with                   Computing Machinery, 2022, p. 959–971. [Online]. Available: https:
     data flow,” CoRR, vol. abs/2009.08366, 2020. [Online]. Available:                 //doi.org/10.1145/3540250.3549101
     https://arxiv.org/abs/2009.08366                                             [55] M. Ott, S. Edunov, A. Baevski, A. Fan, S. Gross, N. Ng, D. Grangier,
[39] S. Lu, D. Guo, S. Ren, J. Huang, A. Svyatkovskiy, A. Blanco, C. B.                and M. Auli, “fairseq: A fast, extensible toolkit for sequence modeling,”
     Clement, D. Drain, D. Jiang, D. Tang, G. Li, L. Zhou, L. Shou, L. Zhou,           in Proceedings of NAACL-HLT 2019: Demonstrations, 2019.
     M. Tufano, M. Gong, M. Zhou, N. Duan, N. Sundaresan, S. K. Deng,             [56] V. P. Dwivedi and X. Bresson, “A generalization of transformer
     S. Fu, and S. Liu, “Codexglue: A machine learning benchmark dataset               networks to graphs,” CoRR, vol. abs/2012.09699, 2020. [Online].
     for code understanding and generation,” CoRR, vol. abs/2102.04664,                Available: https://arxiv.org/abs/2012.09699
     2021.                                                                        [57] Z. Hu, X. Ma, Z. Liu, E. Hovy, and E. Xing, “Harnessing deep neural
[40] R. Just, D. Jalali, and M. D. Ernst, “Defects4J: A Database of Existing           networks with logic rules,” in Proceedings of the 54th Annual Meeting of
     Faults to Enable Controlled Testing Studies for Java Programs,” in                the Association for Computational Linguistics (Volume 1: Long Papers).
     ISSTA, 2014, pp. 437–440.                                                         Berlin, Germany: Association for Computational Linguistics, Aug. 2016,
                                                                                       pp. 2410–2420. [Online]. Available: https://aclanthology.org/P16-1228
[41] D. Lin, J. Koppel, A. Chen, and A. Solar-Lezama, “QuixBugs: A
                                                                                  [58] C.-Y. Lin and F. J. Och, “ORANGE: a method for evaluating automatic
     Multi-Lingual Program Repair Benchmark Set Based on the Quixey
                                                                                       evaluation metrics for machine translation,” in COLING 2004:
     Challenge,” in SPLASH, 2017, p. 55–56.
                                                                                       Proceedings of the 20th International Conference on Computational
[42] J. A. Prenner, H. Babii, and R. Robbes, “Can openai’s codex fix bugs?:            Linguistics. Geneva, Switzerland: COLING, aug 23–aug 27 2004, pp.
     An evaluation on quixbugs,” in 2022 IEEE/ACM International Workshop               501–507. [Online]. Available: https://aclanthology.org/C04-1072
     on Automated Program Repair (APR), 2022, pp. 69–75.                          [59] A. Mesbah, A. Rice, E. Johnston, N. Glorioso, and E. Aftandilian,
[43] B. Barz and J. Denzler, “Do we train on test data? purging cifar of               “DeepDelta: Learning to Repair Compilation Errors,” in ESEC/FSE.
     near-duplicates,” Journal of Imaging, vol. 6, no. 6, p. 41, 2020.                 ACM, 2019, pp. 925–936.
[44] M. Tan, L. Tan, S. Dara, and C. Mayeux, “Online defect prediction            [60] R. Gupta, S. Pal, A. Kanade, and S. Shevade, “Deepfix: Fixing Common
     for imbalanced data,” in 2015 IEEE/ACM 37th IEEE International                    C Language Errors by Deep Learning,” in AAAI, 2017, pp. 1345–1351.
     Conference on Software Engineering, vol. 2. IEEE, 2015, pp. 99–108.          [61] E. A. Santos, J. C. Campbell, A. Hindle, and J. N. Amaral, “Finding
[45] D. Fried, A. Aghajanyan, J. Lin, S. Wang, E. Wallace, F. Shi, R. Zhong,           and Correcting Syntax Errors Using Recurrent Neural Networks,” PeerJ
     W.-t. Yih, L. Zettlemoyer, and M. Lewis, “Incoder: A generative                   PrePrints, vol. 5, p. e3123v1, 2017.
     model for code infilling and synthesis,” 2022. [Online]. Available:          [62] “Replication package of this work,” 2022. [Online]. Available:
     https://arxiv.org/abs/2204.05999                                                  https://github.com/lin-tan/clm
[46] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena,
     Y. Zhou, W. Li, and P. J. Liu, “Exploring the limits of transfer learning
     with a unified text-to-text transformer,” CoRR, vol. abs/1910.10683,
     2019. [Online]. Available: http://arxiv.org/abs/1910.10683
[47] E.-S. A. Lee, S. Thillainathan, S. Nayak, S. Ranathunga, D. I. Adelani,
     R. Su, and A. D. McCarthy, “Pre-trained multilingual sequence-to-
     sequence models: A hope for low-resource language translation?” 2022.
     [Online]. Available: https://arxiv.org/abs/2203.08850
[48] H. Mehrafarin, S. Rajaee, and M. T. Pilehvar, “On the importance of data
     size in probing fine-tuned models,” in Findings of the Association for
     Computational Linguistics: ACL 2022. Dublin, Ireland: Association
     for Computational Linguistics, May 2022, pp. 228–238. [Online].
     Available: https://aclanthology.org/2022.findings-acl.20
[49] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones,
     A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all
     you need,” CoRR, vol. abs/1706.03762, 2017. [Online]. Available:
     http://arxiv.org/abs/1706.03762
[50] H. Husain, H. Wu, T. Gazit, M. Allamanis, and M. Brockschmidt,
     “Codesearchnet challenge: Evaluating the state of semantic code
     search,” CoRR, vol. abs/1909.09436, 2019. [Online]. Available:
     http://arxiv.org/abs/1909.09436
[51] L. Gao, S. Biderman, S. Black, L. Golding, T. Hoppe, C. Foster,
     J. Phang, H. He, A. Thite, N. Nabeshima, S. Presser, and
     C. Leahy, “The pile: An 800gb dataset of diverse text for language
