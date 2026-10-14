                                                                                                                                                  format(ip.strip())


                                                                                                                                                                                                                      Bad ex
                                                                                                                         Example
                                                                                                                                                                                                              x = analysis.ge
                                                                                                                 x = analysis.get(ip, None)                                        ✓ Good (No error)          if not x:
                                                                                                                 if not x:                                                                                      print ("PANIC
                                                                                                                   print ("PANIC! No {}".                                                                        "No {}".form
                                                                                                                     format(ip.strip())
                                                                                                                                               e.g. code analyzer, compiler
                                                                                                                                                                                   ✘ Bad (Error!)
                                                                                                                                                                                                             Error!




                                                                                                                        Bad example                                                 Good example
                                                            Break-It-Fix-It: Unsupervised Learning for Program Repair
                                                                                                                 x = analysis.get(ip, None)                                     x = analysis.get(ip, None)
                                                                                                                 if not x:                                                      if not x:
                                                                                                                   print ("PANIC! No {}".                                         print ("PANIC! No {}".      x = analysis.ge
                                                                                                                     format(ip.strip())                                             format(ip.strip()))       if not x:
                                                                                                                                                                                                                print ("PANIC
                                                                                                               Error!                                                         No error — fixed!                  "No {}".form

                                                                                                           1                         1                                                                       No error — fixe
                                                                                      Michihiro Yasunaga       Percy Liang


                                                                                                                                               Unlabeled Data
                                                                     Abstract
                                                 We consider repair tasks: given a critic (e.g.,                                              x = analysis.get(ip, None)
                                                                                                                                              if not x:
                                                 compiler) that assesses the quality of an input, the                                           print ("PANIC! No {}".
                                                                                                                                                  format(ip.strip())
arXiv:2106.06600v2 [cs.LG] 22 Jun 2021




                                                 goal is to train a fixer that converts a bad example
                                                 (e.g., code with syntax errors) into a good one (e.g.,
                                                 code with no syntax errors). Existing works create
                                                 training data consisting of (bad, good) pairs by                        Example
                                                 corrupting good examples using heuristics (e.g.,                x = analysis.get(ip, None)                                        ✓ Good (No error)
                                                                                                                 if not x:
                                                 dropping tokens). However, fixers trained on this                 print ("PANIC! No {}".
                                                                                                                     format(ip.strip())                                            ✘ Bad (Error!)
                                                                                                                                               e.g. code analyzer, compiler
                                                 synthetically-generated data do not extrapolate
                                                 well to the real distribution of bad inputs. To bridge
                                                 this gap, we propose a new training approach,
                                                 Break-It-Fix-It (BIFI), which has two key ideas:
                                                                                                                        Bad example                                                 Good example
                                                 (i) we use the critic to check a fixer’s output on
                                                                                                                 x = analysis.get(ip, None)                                     x = analysis.get(ip, None)
                                                 real bad inputs and add good (fixed) outputs to                 if not x:                                                      if not x:
                                                                                                                   print ("PANIC! No {}".                                         print ("PANIC! No {}".
                                                 the training data, and (ii) we train a breaker to                   format(ip.strip())                                             format(ip.strip()))

                                                 generate realistic bad code from good code. Based             Error!                                                         No error — fixed!
                                                 on these ideas, we iteratively update the breaker
                                                 and the fixer while using them in conjunction to              Figure 1. Problem setup. We are given an unlabeled data (code
                                                 generate more paired data. We evaluate BIFI on                snippets) and a critic (e.g., code analyzer, compiler) that assesses
                                                 two code repair datasets: GitHub-Python, a new                the quality of an input (e.g., bad if the code has errors; good if no
                                                 dataset we introduce where the goal is to repair              error). Our task is to learn a fixer that can actually repair a bad
                                                 Python code with AST parse errors; and DeepFix,               example into a good one (e.g., fixing errors in the bad code).
                                                 where the goal is to repair C code with compiler
                                                 errors. BIFI outperforms state-of-the-art methods,
                                                                                                               instances of this general setting include molecular design (Jin
                                                 obtaining 90.5% repair accuracy on GitHub-
                                                                                                               et al., 2019) which aims to improve the chemical properties
                                                 Python (+28.5%) and 71.7% on DeepFix (+5.6%).
                                                                                                               (e.g., drug-likeness) of molecules given a property evaluator,
                                                 Notably, BIFI does not require any labeled data;
                                                                                                               and essay editing (Taghipour & Ng, 2016) which aims to
                                                 we hope it will be a strong starting point for
                                                                                                               improve a writing given a grade. How to automatically
                                                 unsupervised learning of various repair tasks.
                                                                                                               learn a fixer given a critic (we term critic2fixer) remains an
                                                                                                               important research problem in machine learning.
                                         1. Introduction
                                                                                                               In this work, we focus on the domain of code repair. Learning
                                         In many domains, one has access to a critic that assesses the         a fixer is challenging because manual labeling of paired data,
                                         quality of an input, but what is desired is a more constructive       e.g., hbroken code, fixed codei, is costly. To this end, we con-
                                         fixer that actually improves bad inputs. For instance, in             sider learning from unlabeled data. Specifically, as illustrated
                                         programming, while a code analyzer and compiler can tell              in Figure 1, we are given (a) a critic (code analyzer or com-
                                         if a given code has errors, programmers need to repair the            piler) that assesses the quality of an input—bad if the code has
                                         errors in the bad code. Development of an automatic code              errors; good if it has no errors—, and (b) unlabeled data—
                                         fixer is thus a key to enhancing programming productivity             unpaired set of good code and bad code, e.g., from GitHub.
                                         (Seo et al., 2014) and is an active area of research (Mesbah          Our goal is to learn a fixer that repairs bad code into good
                                         et al., 2019; Ding et al., 2020; Dinella et al., 2020). Other         code. Previous works in code repair apply random or heuris-
                                             1                                                                 tic perturbations to good code (e.g., dropping tokens) and
                                             Stanford University, Stanford, CA. Correspondence to:
                                         Michihiro Yasunaga <myasu@cs.stanford.edu>.                           prepare synthetic paired data hperturbed code, good codei to
                                                                                                               train a fixer (Pu et al., 2016; Gupta et al., 2017; Ahmed et al.,
                                         Proceedings of the 38 th International Conference on Machine          2018; Hajipour et al., 2019; Yasunaga & Liang, 2020). How-
                                         Learning, PMLR 139, 2021. Copyright 2021 by the author(s).            ever, such synthetically generated bad examples do not match
   msg = ("invalid type!"
 <IN>                                    msg = ("invalid type!"
                                       <IN>                                    msg = ("invalid type!"                                               Real                                          Synthetic
     "not in %s" % types)                    "not in %s" % types)   a            "not in %s" % types)
   raise Exception(msg)<DE>              <IN>raise Exception(msg)<DE><DE>      raise Exception(msg)<DE>
 else: pass                            else: pass                            else: pass                           print ("PANIC! No {}".             print ("PANIC! No {}".                       print ("PANIC! No {}".
                                                                                                                     format(ip.strip()))    i           format(ip.strip())                 i         format ip.strip()))
                                                    (Human Error)                    (Synthetic Error)
                                                                                                                                                                          (Human Errors)                     (Synthetic Errors)
                                                           Break-It-Fix-It: Unsupervised Learning for Program Repair
                                                                                                                                                    Real                                          Synthetic
                                                      Distribution Mismatch                               a source-to-target
                                                                                                              def validate(type):       model to
                                                                                                                                               def reconstruct
                                                                                                                                                   validate(type):     the targets   (e.g., the
                                                                                                                                                                                def validate(type):
                                                                                                                if type not in types:
                                                                                                               <IN>                              if type not in types:
                                                                                                                                                     <IN>                         if type not in types:
                                                                                                                                                                                                  <IN>

                                                                                                          bad-sidemsg = and    good-side
                                                                                                                        ("invalid
                                                                                                                      <IN>         type!"
                                                                                                                    "not in %s" % types)
                                                                                                                                            in   our
                                                                                                                                                   msg =repair
                                                                                                                                                         ("invalid task
                                                                                                                                                            <IN>   type!" can be msg
                                                                                                                                                     "not in %s" % types)
                                                                                                                                                                                   viewed
                                                                                                                                                                                      = ("invalidas
                                                                                                                                                                                                  type!"
                                                                                                                                                                                    "not in %s" % types)
                                                                                                                                                                                       a




                                     Real                                   Synthetic                     the source       and    target).
                                                                                                                  raise Exception(msg)
                                                                                                                else: pass
                                                                                                                                     <DE>
                                                                                                                                           BIFI     differs     from
                                                                                                                                                     raise Exception(msg)
                                                                                                                                                 else: pass
                                                                                                                                                                   <IN>
                                                                                                                                                                          backtranslation        in
                                                                                                                                                                                  raise Exception(msg)
                                                                                                                                                                                       <DE><DE>

                                                                                                                                                                                else: pass
                                                                                                                                                                                                                         <DE>




                                                                                                          two ways: it uses the critic to verify(Human        if theErrors)
                                                                                                                                                                       generated examples
 print ("PANIC! No {}".              print ("PANIC! No {}".                 print ("PANIC! No {}".                                                                                     (Synthetic Errors)
    format(ip.strip()))          i      format(ip.strip())              i      format ip.strip()))        are actually fixed or broken (step 1 and 3), and it trains the
                                                                                                          fixer on real bad examples in addition to examples generated
                                                    (Human Error)                   (Synthetic Error)     by the breaker (step 4), which improves the correctness and
                                                                                                          distributional match of generated paired data.
                                     Real                                   Synthetic
 def validate(type):                 def validate(type):                    def validate(type):           We evaluate our proposed approach on two code repair
 <I>if type not in types:            <I>if type not in types:               <I>iftype not in types:
    <I>msg = ("invalid type!"           <I>msg = ("invalid type!"             msg = ("invalid type!"      datasets:
         "not in %s" % types)                 "not in %s" % types)  a           "not in %s" % types)
       raise Exception(msg)<D>             <I>raise Exception(msg)<D><D>      raise Exception(msg)<D>
    else: pass                          else: pass                          else: pass
                                                                                                           • GitHub-Python: We collected a new dataset of 3M
                                                    (Human Error)                   (Synthetic Error)        Python code snippets from github.com. The task is to
                                                                                                             repair errors caught by the Python AST parser. We set
Figure 2. Challenge of learning a fixer from unlabeled data. Ex-
                                                                                                             the initial fixer to be an encoder-decoder Transformer
isting works randomly perturb good examples into bad examples
and learn to recover. However, such synthetically generated bad
                                                                                                             (Vaswani et al., 2017) trained on random perturbations.
examples do not match the distribution of real bad examples. For                                           • DeepFix (Gupta et al., 2017): The task is to repair
instance, synthetic perturbations may drop parentheses arbitrar-                                             compiler errors in C code submitted by students in an
ily from code (top right), but real human-written bad code misses                                            introductory programming course. We set the initial fixer
parentheses more often in a nested context (top center). In a more ex-                                       to be the existing best system, DrRepair (Yasunaga &
treme case at bottom, to generate the human error (center) from the                                          Liang, 2020), which was trained on manually-designed
corrected code (left), a pair of indent and dedent tokens need to be in-                                     heuristic perturbations.
serted accordingly, which random perturbations generate with very
small probability. Note that indentation is meaningful in Python: in                                      Our approach (BIFI) outperforms the initial fixers, obtaining
the tokenized Python code, each hIi token means indenting the line                                        90.5% repair accuracy on GitHub-Python (+28.5% absolute)
by one unit, each hDi means dedenting the next line by one unit.                                          and 71.7% repair accuracy on DeepFix (+5.6% absolute),
                                                                                                          attaining a new state-of-the-art. BIFI also improves on
                                                                                                          backtranslation by 10%. Further, we qualitatively show
the distribution of real bad examples. For instance, as shown                                             how the fixer and breaker adapt towards more realistic
in Figure 2, synthetic perturbations may drop parentheses                                                 distributions of code through the BIFI algorithm (§4.3).
arbitrarily from code, generating errors that rarely happen in
real programming (Figure 2 top right; synthetic errors); in                                               2. Problem statement
contrast, real human-written code misses parentheses more
often in a nested context (Figure 2 top center; human errors).                                            Figure 1 illustrates our problem setup, critic2fixer. The
As we will show in §4, this distribution mismatch between                                                 system is given unlabeled data D (code snippets) and a critic
synthetic data and real data results in low performance.                                                  c (code analyzer or compiler) that returns whether an input
                                                                                                          is good or bad: e.g., for a code snippet x ∈ D,
To bridge this gap, we propose Break-It-Fix-It (BIFI), a new                                                                     
method to learn a fixer from unlabeled data and a critic (Fig-                                                                     0 if x has errors,
                                                                                                                        c(x) =                                     (1)
ure 3). BIFI is based on two core insights: (i) we can use the                                                                     1 if x has no error.
critic to check a fixer’s output on real bad examples and add                                             Using the critic c, examples in D can be classified into bad
good outputs to the training data, and (ii) we train a breaker to                                         ones Dbad = {x | x ∈ D, c(x) = 0} and good ones Dgood = {y |
generate realistic bad examples from good examples. Specif-                                               y ∈ D, c(y) = 1}. Our task is to learn a fixer f that maps a bad
ically, given an initial fixer trained on synthetic paired data                                           example x ∈ Dbad into a good example f (x) such that it is
hsynthetic bad, goodi, BIFI improves the fixer and breaker si-                                            close1 to x and c(f (x)) = 1. The evaluation metric is the fixer
multaneously through rounds of data generation and training:                                              f ’s repair accuracy on a held-out set of bad examples, Dbad(test)
                                                                                                                                                                             ,
(1) apply the fixer to real bad examples and keep fixed outputs
                                                                                                                                                           (test)
to obtain real paired data, (2) use the resulting data to train the                                                                             |{x | x ∈ Dbad    , c(f (x)) = 1}|
breaker, (3) use the learned breaker to generate code errors                                                                 RepairAcc =                                    (test)
                                                                                                                                                                                                         .         (2)
                                                                                                                                                                          |Dbad    |
and obtain more paired data, and (4) train the fixer on the
newly-generated paired data in (1) and (3). Intuitively, this
cycle trains the fixer on increasingly more real or realistically
                                                                                                          3. Approach
generated bad code, adapting the fixer from the initial syn-                                              The major challenge of learning a fixer is that we need to learn
thetic distributions towards real distributions of code errors.                                           from unpaired data, i.e., Dbad and Dgood do not form hbroken,
The BIFI algorithm is related to backtranslation in unsuper-                                                  1
                                                                                                               We constrain the edit distance as described in §4.1. We acknowl-
vised machine translation (Lample et al., 2018a), which uses                                              edge that while we want f (x) to be semantics-preserving, it is non-
a target-to-source model to generate noisy sources and trains                                             trivial to ensure this automatically, so we rely on the edit distance.
       for name in listdir(path)
       if isfile(join(path,name)))   i
                                         (4) Finetune fk          for name in listdir(path)
                                                                  if isfile(join(path,name)))
                                                                                                    for name in listdir(path)
                                                                                                    if isfile(join(path,name))    i
                                                                                                                                                             for name in listdir(path)
                                                                                                                                                             if isfile(join(path,name)))




                                                                                                                                      (4) Finetune fk


                                                        Break-It-Fix-It: Unsupervised Learning for Program Repair

  § 3.1 Initialization — Round 0                                                                § 3.4 FixerOnly — Round k (=1,2, …)

                                         (1)    Synthetic                                                                             (1) Apply fk-1
    Synthetic bad code                         Perturbation    Good code                          Bad code                                Keep if fixed    Fixed code
    def iterFiles path):                                       def iterFiles(path):               def compute_loss(self):                                  def compute_loss(self):
      return (name                                               return (name                       loss = self.cost(self.preds                              loss = self.cost(self.preds,
       for name in listdir(path)         (2)     Train b0         for name in listdir(path)          self.target,
                                                                                                     self.length).sum()
                                                                                                                                      (2) Train fk            self.target,
                                                                                                                                                              self.length).sum()
       if isfile(join(path,name)))                                if isfile(join(path,name)))


                                                 Train f0


  § 3.3 ref. Backtranslation — Round k (=1,2, …)                                                § 3.2 Break-It-Fix-It (BIFI) — Round k (=1,2, …)
                                                                                                                                      (1) Apply fk-1
    Bad code                             (1) Apply fk-1        Fixed? code                        Bad code                                Keep if fixed    Fixed code
    def compute_loss(self):                                    def compute_loss(self):            def compute_loss(self):                                  def compute_loss(self):
      loss = self.cost(self.preds                                loss = self.cost(self.preds=       loss = self.cost(self.preds                              loss = self.cost(self.preds,
       self.target,
       self.length).sum()
                                         (2) Train bk             self.target,
                                                                  self.length).sum()
                                                                                                     self.target,
                                                                                                     self.length).sum()
                                                                                                                                      (2) Train bk            self.target,
                                                                                                                                                              self.length).sum()




    Broken? code                         (3) Apply bk          Good code                          Broken code                         (3) Apply bk         Good code
    def iterFile(path): return                                 def iterFiles(path):               def iterFiles(path):
                                                                                                                                          Keep if broken   def iterFiles(path):
    (name                                                        return (name                       return (name                                             return (name
       for name in listdir(path)
       if isfile(join(path,name)))   i
                                         (4) Train fk             for name in listdir(path)
                                                                  if isfile(join(path,name)))
                                                                                                     for name in listdir(path)
                                                                                                     if isfile(join(path,name))   i
                                                                                                                                                              for name in listdir(path)
                                                                                                                                                              if isfile(join(path,name)))




                                                                                                                                      (4) Train fk


Figure 3. Overview of our approach. We train the initial fixer on synthetically prepared data as in prior works (top left). In our approach,
BIFI (bottom right), we apply the initial fixer to the real bad examples and add fixed outputs (verified by the critic) to our training data
(Step 1), train a breaker on the resulting paired data (Step 2), use the breaker to generate (intuitively more realistic) code errors (Step 3), and
train the fixer again on the newly-generated paired data (Step 4). We iterate this cycle, improving the fixer and the breaker simultaneously.
Top right: a version of BIFI without the breaker (FixerOnly). Bottom left: comparison of BIFI to backtranslation. The main difference
is that BIFI uses the critic to verify that the fixer produces good code and the breaker produces bad code (annotated with magenta font).

fixedi pairs. Prior works in code repair apply random or                                        resulting paired data—as this data consists of real code errors,
heuristic perturbations to good examples (e.g., dropping to-                                    intuitively, the breaker learns to generate realistic code errors;
kens) and prepare a synthetic paired data hperturbed code,                                      (3) we apply the breaker to the good examples; (4) we finally
good codei to train a fixer (Gupta et al., 2017; Ahmed et al.,                                  train the fixer on the newly-generated paired data in (1) and
2018; Yasunaga & Liang, 2020). However, such syntheti-                                          (3). We iterate this cycle to improve the fixer and the breaker
cally generated bad examples do not match the distribution of                                   simultaneously in the process. The intuition is that a better
real bad examples. For instance, as Figure 2 (top) shows, syn-                                  fixer and breaker will be able to generate more realistic paired
thetic perturbations may drop parentheses arbitrarily from                                      data, which in turn helps to train a better fixer and breaker.
code, generating errors that are rare in real programs; in
                                                                                                Below, we describe the initialization step in §3.1, our main
contrast, real human-written code misses parentheses often
                                                                                                algorithm BIFI in §3.2, and discuss two baselines of BIFI:
in a nested context (e.g., 10x more than non-nested in our
                                                                                                backtranslation (§3.3) and FixerOnly (version of BIFI
collected dataset GitHub-Python). In a more extreme case
                                                                                                without the breaker; §3.4).
(Figure 2 bottom), to make the real human error (center) from
the corrected code (left), multiple tokens (in this case, a pair                                3.1. Initialization
of indent and dedent) need to be inserted or dropped accord-
ingly, which random perturbations would generate with ex-                                       Given unlabeled data D = (Dbad ,Dgood ), we first prepare a
tremely low probability. This distribution mismatch between                                     synthetic paired data Psynthetic by perturbing good examples:
synthetic data and real data results in low performance (§4).                                                  Psynthetic = {(bsynthetic (y), y) | y ∈ Dgood },                             (3)
To address this challenge, we propose Break-It-Fix-It (BIFI),                                   where bsynthetic denotes a pre-defined procedure that corrupts
an approach that adapts the fixer automatically towards real                                    code. For instance, we will experiment with two choices of
distributions of bad examples. Concretely, we first start                                       bsynthetic : (i) random noising, which randomly drops/inserts
from the synthetic paired data hsynthetic bad, goodi and                                        /replaces tokens in code, and (ii) heuristic noising designed
train an initial fixer as in prior works (see Figure 3 top left;                                in Yasunaga & Liang (2020), which aims to generate
initialization). We then perform the following cycle (see                                       common programming errors such as typo, punctuation and
Figure 3 bottom right): (1) we apply the initial fixer to the real                              type errors. More details are described in §4.1.
bad examples and use the critic to assess if the fixer’s output is
good—if good, we keep the pair; (2) we train a breaker on the                                   We then train the initial fixer f0 and breaker b0 on the
                                     Break-It-Fix-It: Unsupervised Learning for Program Repair

synthetic paired data:                                             in each round k, backtranslation performs the following:
                               good→bad                                             (f )
               b0 = T RAIN                (Psynthetic )     (4)                   Pk = {(x, fk−1 (x)) | x ∈ Dbad }              (10)
               f0 = T RAINbad→good (Psynthetic )            (5)                     bk = T RAIN      good→bad     (f )
                                                                                                                (Pk )           (11)
               good→bad                                                            (b)
where T RAIN            (P) denotes training an encoder-                          Pk = {(bk (y), y) | y ∈ Dgood }               (12)
decoder model that maps good-side examples to bad-side                                                     (b)
examples in a paired data P, and T RAINbad→good (P) does                           fk = T RAINbad→good (Pk ).                   (13)
the reverse. Note that f0 here corresponds to the fixer learned    BIFI differs in two aspects. First, as our task has a critic, BIFI
in prior works (e.g., Gupta et al. (2017); Yasunaga & Liang        uses the critic to verify the outputs of the fixer and breaker,
(2020)). We call this initialization step our round 0.             and only keep examples whose outputs are actually fixed
                                                                   (Eq 6 red part) and whose outputs are broken (Eq 8 red
3.2. Break-It-Fix-It (BIFI)
                                                                   part) to generate paired data. In contrast, backtranslation
BIFI aims to improve the fixer and breaker simultaneously          does not verify the generated paired data in Eq 10, 12. This
through rounds of data generation and training: (1) use            may blindly include non-fixed code as good-side examples
a fixer to create data for a breaker, (2) train a breaker, (3)     (consequently, the breaker might learn to output erroneous
use a breaker to create data for a fixer, and (4) train a fixer.   code) and non-broken code as bad-side examples, leading
Concretely, after the initialization step, BIFI performs the       to noisy training data (e.g., Figure 3 bottom left). Secondly,
following in each round k = 1,2,...,K:                             while backtranslation trains the fixer only on examples
      (f )
                                                                   predicted by the breaker (Eq 13), BIFI trains the fixer on the
   Pk = {(x, fk−1 (x)) | x ∈ Dbad , c(fk−1 (x)) = 1}        (6)                            (f )
                                                                   real bad examples (Pk in Eq 9) in addition to examples
                    good→bad     (f )                              generated by the breaker, which improves the correctness
      bk = T RAIN              (Pk )                        (7)
     (b)                                                           and distributional match of training data. We will show in our
    Pk = {(bk (y), y) | y ∈ Dgood , c(bk (y)) = 0}          (8)    ablation study (§4.3.3) that both of these two components
                             (f )
     fk = T RAINbad→good (Pk ∪ Pk ).
                                       (b)
                                                            (9)    improve the learning of a fixer and breaker. In essence, BIFI
                                                                   is an augmentation of backtranslation with a critic.
For convenience, we call the original examples in Dbad real
bad examples. Here Eq 6 applies the current fixer fk−1 to the      3.4. Version of BIFI without breaker: FixerOnly
real bad examples in Dbad , and keeps outputs that are actually
fixed (verified by the critic c; red part). This way, we can ob-   The benefit of BIFI is to enable training the fixer on real bad
                          (f )                                     examples and bad examples generated by a learned breaker.
tain new paired data Pk that is based on real bad examples.        We consider a version (FixerOnly) that trains the fixer simply
Eq 7 then trains the breaker bk (fine-tunes from the previous      on the real bad examples (prepared in Eq 6) but not the bad
                                            (f )
breaker bk−1 ) on this new paired data Pk so that intuitively      examples generated by the breaker (Eq 8). Specifically,
it can learn to generate realistic bad examples. Next, Eq 8 ap-    FixerOnly does the following in each round k:
plies the breaker bk to the good examples in Dgood , and keeps            (f )
outputs that are actually broken (verified by the critic c; red       Pk = {(x, fk−1 (x)) | x ∈ Dbad , c(fk−1 (x)) = 1}         (14)
                                                (b)
part). This provides an extra paired data Pk that is based on              fk = T RAIN   bad→good     (f )
                                                                                                    (Pk ).                      (15)
bad examples generated by the learned breaker. Finally, Eq
9 trains the fixer fk (fine-tunes from the previous fixer fk−1 )   FixerOnly can also be viewed as self-training (Lee, 2013)
           (f )       (b)                                          with the difference that we only add fixer outputs verified by
on both Pk and Pk , so that the fixer sees real and breaker-
                                                                   the critic to the training data. We will show in §4.3.1 that
generated bad examples. Over time, this cycle adapts the
                                                                   FixerOnly is especially useful when the amount of available
fixer and breaker towards the distribution of real examples.
                                                                   bad examples |Dbad | is big, but the gain is smaller compared
Figure 3 (bottom right) provides an illustration of BIFI.
                                                                   to BIFI when |Dbad | is small, because BIFI can use the breaker
3.3. Comparison with Backtranslation                               to generate additional paired data for training the fixer (Eq 8).

The BIFI algorithm is related to backtranslation (Lample           4. Experiments
et al., 2018b) in unsupervised machine translation. One may
view the bad-side and good-side in our setup as two source/tar-    We evaluate our approach on two code repair datasets: a
get languages in machine translation. Backtranslation uses a       common benchmark DeepFix2 (Gupta et al., 2017), and
target-to-source model to generate noisy sources and trains a      GitHub-Python, a bigger dataset we collect in this paper.
source-to-target model to reconstruct the targets. Specifically,
                                                                   4.1. Dataset and setup
                                                                   We first describe the detail and experimental setup for
                                                                   GitHub-Python and DeepFix.
                                                                      2
                                                                          https://bitbucket.org/iiscseal/deepfix
                                     Break-It-Fix-It: Unsupervised Learning for Program Repair

                                        Test accuracy                   (Vaswani et al., 2017) with 4 layers, 8 attention heads, and hid-
 Method                             Unbalanced Indentation Invalid      den states of size 256. The model parameters are optimized
                            Total   Parentheses  Error     Syntax       by Adam (Kingma & Ba, 2015), with batch size of 27,000 to-
 Initial   Round-0         62.0%     87.7%       39.4%       70.5%      kens, learning rate 0.001, and gradient clipping 1.0 (Pascanu
           Round-1         86.8%     93.3%       79.5%       90.9%      et al., 2013), on one GPU (GTX Titan X). For generation, we
 FixerOnly                                                              use beam search with beam size 10, and keep predictions with
           Round-2         88.6%     92.4%       83.7%       92.0%
           Round-1         88.0%     94.1%       81.3%       91.6%      Levenshtein edit-distance less than 5 tokens from the input.
 BIFI
           Round-2         90.5%     94.2%       85.9%       93.5%
                                                                        To train the initial fixer f0 , we use random perturbations for
Table 1. Repair accuracy on the GitHub-Python test set. The             the corruption procedure bsynthetic (Eq 3), which drops, inserts,
initial fixer is trained on synthetic bad code. Our proposed method     or replaces 1–3 tokens in code with uniform distribution. We
(BIFI) enables the fixer to be fine-tuned on real bad code and bad      apply bsynthetic 8 times to each of the 2.6M good code snippets
code generated by the learned breaker. The result shows that BIFI       to prepare the initial training data Psynthetic . We holdout 1%
outperforms the initial fixer by a large margin.                        of Psynthetic as our dev set, which we use to perform early
                                                                        stopping. We then run the BIFI algorithm for K = 2 rounds.
    Method                                       Test accuracy
    DeepFix (Gupta et al., 2017)                     33.4%
                                                                        4.1.2. DeepFix
    RLAssist (Gupta et al., 2019)                    26.6%              Dataset. DeepFix (Gupta et al., 2017) contains C code sub-
    SampleFix (Hajipour et al., 2019)                45.3%              mitted by students in an introductory programming course, of
    DrRepair (Yasunaga & Liang, 2020)                66.1%
                                                                        which 37K snippets are good (no compiler error) and 7K are
    Our Initial        Round-0 (= DrRepair)          66.1%              bad (have compiler errors). Each code snippet has 25 lines on
                       Round-1                       68.6%              average. Within the 7K bad examples, we take 20% as a held-
    Our FixerOnly
                       Round-2                       70.5%              out test set. We make the remaining 80% available for BIFI.
                       Round-1                       70.8%              The goal is to learn a fixer that repairs compiler errors. Repair
    Our BIFI
                       Round-2                       71.7%              is successful if the output code has no compiler errors. The
Table 2. Repair accuracy on the DeepFix test set. We define our         evaluation metric is the fixer’s repair accuracy on the test set.
initial fixer (Round 0) to be the existing best system DrRepair. Note   BIFI implementation details. We define the initial fixer
that DrRepair’s training procedure coincides with the initialization    f0 as DrRepair (Yasunaga & Liang, 2020) (the existing best
step of our BIFI algorithm, with heuristic perturbations used in Eq     system on DeepFix), which is an encoder-decoder model
3. We then apply BIFI on top of it for Round 1, 2. BIFI outperforms     trained in a procedure that corresponds exactly to the initial-
DrRepair, achieving a new state-of-the-art.                             ization step of BIFI (§3.1). Specifically, to train DrRepair,
                                                                        Yasunaga & Liang (2020) design heuristic perturbations for
4.1.1. Github-Python                                                    the corruption procedure bsynthetic , which mimics common
                                                                        code errors beginner and experienced programmers make
Dataset. To obtain an unlabeled dataset of code, we col-                (e.g., typos, punctuation, keyword and type errors). We
lected Python3 files from GitHub public repositories.3 We               use the same training / dev data prepared and released by
then tokenize each code file using the builtin Python tok-              the authors to train the initial fixer. We then run the BIFI
enizer, and keep code snippets of length 10–128 tokens, re-             algorithm for K = 2 rounds. Our fixer and breaker have the
sulting in 3M code snippets. As the critic c, we use the Python         same model architecture as DrRepair. At test time, following
AST parser,4 which catches unbalanced parentheses, inden-               the original DrRepair, we repeatedly apply the fixer while
tation errors, and other syntax errors. Concretely, we define           the code still has errors, up to a maximum of 5 times.
c(x) = 1 (good) if the AST parser returns no errors for input
code x, and c(x) = 0 (bad) otherwise. Using this critic, we ob-         4.2. Main results
tain 38K snippets of bad code and 3M snippets of good code.
From the 38K bad examples, we holdout 15K as the final test             We study the fixer’s repair accuracy on GitHub-Python
set, and make the remaining 23K bad examples available for              and DeepFix. Here “round k accuracy” means the repair
BIFI. Our goal is to learn a fixer that repairs AST parse errors.       accuracy of the fixer learned in round k, i.e., fk .
We define that the fixer’s repair is successful if the output code      GitHub-Python.          Table 1 shows the test results on
has no AST parse errors and has Levenshtein edit-distance               GitHub-Python. We show the overall repair accuracy
(Levenshtein, 1966) less than 5 tokens from the input code.             (“Total”) as well as the breakdown over the error categories
The evaluation metric is the fixer’s repair accuracy on the test        in the Python AST parser (table right). The initial fixer f0
set, i.e., the heldout 15K examples of real bad code.                   (“Initial”) is trained on randomly perturbed, synthetic bad
BIFI implementation details. For the architecture of the                code. Our proposed method (BIFI) enables the initial fixer to
fixer and breaker, we use the encoder-decoder Transformer               be further trained on real bad code and bad code generated by
                                                                        the learned breaker, which outperforms the initial fixer signif-
   3
       https:github.com                                                 icantly: +28.5% in overall repair accuracy, and consistently
   4
       https://docs.python.org/3/library/ast.html
                                                                                                    self.length).sum()                            k            self.length).sum()                          self.length).sum(
      def sanitize(x,start,end):       def sanitize(x,start,end):        def sanitize(x,start,end):
      <I>if x >= start and x < end:    <I>if x >= start and x < end:     <I>if x >= start and x < end:
         err = 0                          <I>err = 0                        <I>err = 0
         <I>return err, x<D>                 <I>return err, x<D>               return err, x<D> Broken?                           (3) Apply bk              Good                                     Broken
         else:                               else:                          else:
         <I>err = 1                          <I>err = 1                     <I>err = 1           def iterFile(path): return                                 def iterFiles(path):                     def iterFiles(path):
            return err, x                       return err, x                  return err, x     (name                                                        return (name                             return (name
                                                                                 for name in listdir(path)
                                                  Break-It-Fix-It: Unsupervised Learning
                                                                                 if isfile(join(path,name)))
                                                                                                             Finetune fk
                                                                                              for Program(4)Repair            i
                                                                                                                                                               for name in listdir(path)
                                                                                                                                                               if isfile(join(path,name)))
                                                                                                                                                                                                        for name in listd
                                                                                                                                                                                                        if isfile(join(pa



                                                       Test accuracy
  Method                               Bad            Bad       Bad      ref. Synthetic             def del_record(self, desc):    def del_record(self, desc):    def del_record(self, desc):
       def sanitize(x,r1,r2):      def sanitize(x,r1,r2):      def sanitize(x,r1,r2):                 record = self.find_one(desc)   record = self.find_one(desc)   record = self.find_one(desc)
       <I>if x >= r1 and x < r2:
                                       100%          50%
                                   <I>if x >= r1 and x < r2:
                                                                 10%          bad only
                                                               <I>if x >= r1 and x < r2:              records = self.find(desc)      records = self.find(desc)      records = self.find(desc)
          err = 0                     <I>err = 0                  <I>err = 0
                                                                                                      if [record] != records:        if [record] != records:        if [record] != records:
  Initial <I>return Round-0           62.0%         62.0%      62.0%           62.0%                      raise ValueError(              raise ValueError,              raise ValueError(
                    err, x<D>            <I>return err, x<D>         return err, x<D>
                                                                                                                                                        a




                                                                                                            "duplicate {}".format(         "duplicate {}".format(         "duplicate {}".format(
          else:                          else:                    else:                                        str(desc)))                    str(desc))                     str(desc))
  FixerOnly
          <I>err = 1
                    Round-2           88.6%
                                         <I>err = 1
                                                    84.7%      78.5%
                                                                  <I>err = 1
                                                                               62.7%                                                                                                         a




                                                                                                      if  record:
                                                                                                    def sanitize(x,start,end):       if  record:
                                                                                                                                         def sanitize(x,start,end): if  record:
                                                                                                                                                                              def sanitize(x,start,end):
  BIFI return Round-2err, x           90.5% return err, x
                                                    89.0%      86.7% return err, x
                                                                               63.3%                <I>if
                                                                                                         self.remove(record)
                                                                                                          x >= start and x < end:
                                                                                                                                        self.remove(record)
                                                                                                                                    <I>if x >= start and x < end:
                                                                                                                                                                       self.remove(record)
                                                                                                                                                                     <I>if x >= start and x < end:

                 Error!                      Error!                No error — fixed!                  err = 0                          <I>err = 0                       <I>err = 0
                                                                                                      <I>return err, x<D>                 <I>return err, x<D>              return
Table 3. Analysis varying the amount of (real) bad code on                                          Figure
                                                                                                      else:
                                                                                                              4. Example      of breaker      outputs.
                                                                                                                                          else:
                                                                                                                                                          Given  good   code
                                                                                                                                                                        else:
                                                                                                                                                                                onerr,
                                                                                                                                                                                   the x<D>
GitHub-Python. “Bad 100%” is our original setting (with 23K                                         left, we   sampled
                                                                                                      <I>err = 1          two  outputs    made    by
                                                                                                                                          <I>err = 1   the breaker learned    in
                                                                                                                                                                        <I>err = 1BIFI
real bad examples available for BIFI) and “Bad 50%” means only                                      roundreturn  err, x We observe thatreturn
                                                                                                             1 (right).                              err, x places high probability
                                                                                                                                              the breaker                  return err, x

50% of them (11.5K) are made available. “Synthetic bad only”                                        on errors seen in real bad code (i.e., obsolete usage of raise,
means keeping training the fixer on synthetic bad examples. The                                     unbalanced parentheses in nested context).
result shows that (i) even when the amount of real bad examples
is small (e.g., “Bad 10%”), they are still useful, allowing FixerOnly                                                                                                                                def del_record(sel
                                                                                                    def sanitize(x,r1,r2):          def sanitize(x,r1,r2):         def sanitize(x,r1,r2):              record = self.fi
/BIFI to perform better than using synthetic data alone; (ii) when                                                                                                                                     records = self.f
                                                                                                    <I>if x >= r1 and x < r2:       <I>if x >= r1 and x < r2:      <I>if x >= r1 and x < r2:
the amount of real bad examples is small, BIFI exceeds FixerOnly                                       err = 0                         <I>err = 0                     <I>err = 0
                                                                                                                                                                                                       if [record] != r
                                                                                                                                                                                                          raise ValueEr
                                                                                                       <I>return err, x<D>                <I>return err, x<D>            return err, x<D>
by a larger margin, highlighting the usefulness of the bad examples                                                                                                                                         "duplicate
                                                                                                       else:                              else:                       else:                                    str(desc
generated by the learned breaker.                                                                      <I>err = 1                         <I>err = 1                  <I>err = 1                       if record:
                                                                                                          return err, x                      return err, x               return err, x                   self.remove(re
           Method                                           Test accuracy
                                                                                                               Error!                        Error!                     No error — fixed!
           Initial                    Round-0                   62.0%
                                                                                                    Figure 5. Example of fixer outputs. Given the bad code on the left
           BIFI (ours)                Round-2                   90.5%                               (with an indentation error), the initial fixer (center) attempts to fix it
            – real bad                Round-2                   84.6%                               by inserting an indent token (hIi) to line 3, but fails to adjust (delete)
            – critic                  Round-2                   84.0%                               the indent token on the next line. The initial fixer commonly makes
                                                                                                    this mistake due to the distribution mismatch between real errors and
            – both
                             Round-2                            80.1%                               synthetic perturbations on which the initial fixer was trained (see
           (backtranslation)
                                                                                                    §4.3.4). After one round of BIFI, the fixer in round 1 (right) learns
Table 4. Performance comparison with backtranslation on                                             to insert and delete the correct pair of indent tokens, fixing the error.
GitHub-Python. Backtranslation is equivalent to removing two
components from BIFI: (i) using the critic to verify fix / break
attempts (“critic”) and (ii) training the fixer on real bad examples                                boosts repair accuracy without additional manual effort.
in addition to examples generated by the breaker (“real bad”). The
result suggests that both of these components improve the learning
                                                                                                    4.3. Analysis
of a fixer, and consequently BIFI outperforms backtranslation.                                      We now analyze the key insights of BIFI. As the main prop-
                                                                                                    erties of BIFI are to (i) add real bad examples to the training
across all error categories. This result suggests that even if                                      data if the critic accepts the fixer’s output (the FixerOnly
we start from a very simple initial fixer trained with random                                       version), and to (ii) train the breaker to generate realistic bad
perturbations, BIFI can automatically turn it into a usable                                         examples (BIFI), we analyze their effects in §4.3.1 and §4.3.2.
fixer with high repair accuracy—90.5% accuracy on real bad                                          We also compare with backtranslation in §4.3.3. We then
code. We also experimented with continuing training the                                             analyze how our fixer adapts towards real code distributions
initial fixer f0 with synthetic perturbations only, for the same                                    through quantitative and qualitative studies (§4.3.4).
rounds of BIFI (hence, controlling the amount of training
                                                                                                    4.3.1. Effect of real bad examples
data seen by the fixer); however, this did not provide an
improvement, suggesting that there is a performance ceiling                                         FixerOnly enables training the fixer on real bad examples
if we only train on synthetic data.                                                                 (but does not use the bad examples generated by the breaker).
                                                                                                    As Table 1 and 2 show, FixerOnly outperforms the initial fixer
DeepFix. Table 2 shows the test results on DeepFix, along
                                                                                                    by a large margin, e.g., +27% on GitHub-Python. This result
with prior works. Here we use the existing best system
                                                                                                    highlights the importance of training on real bad examples.
DrRepair as our initial fixer (“Initial”). BIFI outperforms
the initial fixer by a substantial margin (+5.6% absolute                                           We further analyze the effect of varying the amount of real
over DrRepair), attaining a new state-of-the-art accuracy                                           bad examples, shown in Table 3. Here, “Bad 100%” is
of 71.7%. It is notable that DrRepair was trained with                                              our original setting (with 23K real bad examples available
manually-designed heuristic perturbations, where the                                                for BIFI and FixerOnly) and “Bad 50%” means only 50%
authors (Yasunaga & Liang, 2020) mimicked various code                                              of them (11.5K) are made available. “Synthetic bad only”
errors beginner and experienced programmers make (e.g.,                                             means keeping training the fixer on synthetic bad examples
typos, punctuation and type errors). Nevertheless, our result                                       only. We find that while the repair accuracy drops as we
suggests that there is still room for improving the adaptation                                      decrease the amount of available real bad examples, a small
to a more realistic distribution of coding errors, and BIFI                                         amount of real bad examples (e.g., “Bad 10%”) is still useful,
                                                  Break-It-Fix-It: Unsupervised Learning for Program Repair

                                                                                      Initial                FixerOnly                      BIFI
        Code error category                                            #Examples
                                                                                   Round-0 Acc.   Round-1 Acc.    Round-2 Acc.   Round-1 Acc.   Round-2 Acc.
        Total                                                             15055       62.0%          86.8%               92.4%      88.0%          90.5%
        Unbalanced Parentheses                                             3999       87.7%          93.3%               92.4%      94.1%          94.2%
          Unclosed left parenthesis (not nested)                            226       92.5%          94.6%               94.6%      94.7%          94.4%
          Unclosed left parenthesis (nested)                               3014       85.8%          92.8%               91.7%      93.8%          93.8%
          Redundant right parenthesis                                       759       93.8%          95.3%               94.7%      95.4%          95.7%
        Indentation Error                                                  6307       39.4%          79.5%               83.7%      81.3%          85.9%
          Expected indent                                                  4311       46.4%          81.2%               84.1%      82.0%          85.3%
          Unexpected indent                                                1966       24.6%          76.8%               83.8%      80.9%          88.4%
        Invalid Syntax                                                     4749       70.5%          90.9%               92.0%      91.6%          93.5%
          Missing colon                                                     663       98.3%          97.3%               97.4%      98.2%          98.0%
          Missing comma (single-line list/tuple/dict)                       694       95.4%          98.1%               97.4%      98.4%          98.3%
          Missing comma (multi-line list/tuple/dict)                        451       88.9%          92.5%               92.0%      94.5%          94.9%
          Missing newline                                                    52       84.6%          86.5%               88.5%      86.5%          88.5%
          Missing parenthesis pair                                          634       82.5%          85.0%               86.4%      87.1%          88.3%
          Redundant comma                                                   152       73.7%          84.2%               91.4%      84.9%          92.1%
          Redundant parenthesis pair                                        698       13.8%          80.7%               86.1%      80.1%          89.4%
          Invalid use of comma                                             1138       61.3%          98.8%               99.1%      98.7%          99.4%
             (e.g., “raise OSError, "msg"” → “raise OSError("msg")”)
          Other                                                             267       60.7%          66.3%               64.4%      67.4%          66.7%

Table 5. Code error categories in GitHub-Python, and repair accuracy. Due to the mismatch between real errors and synthetic perturba-
tions used for training, the initial fixer has lower accuracy on “nested” than “not nested” for “unbalanced parentheses” errors, but it catches up
in BIFI round 1, 2. Similarly, the initial fixer’s repair accuracy is very low for “redundant parenthesis pair” and “indentation error”, but it im-
proves significantly in round 1, 2. This result illustrates the effect of BIFI adapting the fixer towards real errors. See §4.3.4 for more analysis.

making FixerOnly perform better than using synthetic data                                     a large margin (+10% absolute on GitHub-Python).
alone (i.e., 78.5% vs 62.7%).
                                                                                              4.3.4. How does the fixer adapt?
4.3.2. Effect of bad examples generated by breaker
                                                                                              We take a closer look at how our fixer performs and adapts
Recall that BIFI trains the fixer on both real bad examples                                   towards the real distribution of bad code. Table 5 shows
and bad examples generated by the learned breaker. As                                         fine-grained categories of code errors seen in GitHub-Python,
Table 1 and 2 show, BIFI consistently provides an extra boost                                 and their repair accuracy.
over FixerOnly, suggesting that the use of breaker outputs
                                                                                              In this categorization, we observe two examples of dis-
improves the fixer. Moreover, another benefit of the breaker
                                                                                              tribution mismatch between the real errors and synthetic
is that one can sample many bad examples from the breaker
                                                                                              perturbations: (i) random perturbations can generate this
to augment real bad examples, if their amount is limited.
                                                                                              category of errors with high probability but with a wrong
In Table 3 we find that BIFI is especially stronger than
                                                                                              “sub-distribution” within it (e.g., can generate “unbalanced
FixerOnly when the amount of available real bad examples
                                                                                              parentheses” or “missing comma” errors but do not match
is small (e.g., “Bad 10%”).
                                                                                              the low-level distribution of real bad code, such as errors
Figure 4 shows sample outputs made by the learned breaker                                     occurring more often in nested parentheses or in a multi-line
b1 given the good code on the left. We observe that the                                       list/tuple/dict; recall the Figure 2 top example); (ii) random
breaker places high probability on errors seen in real bad                                    perturbations can only generate this category of errors with
code, i.e., obsolete usage of raise in Python3 (center) and                                   very small probability (e.g., “redundant parenthesis pair” and
unbalanced parentheses in nested context (right). Compared                                    “indentation error”, for which an exact pair of parentheses
to random perturbations that arbitrarily drop/insert tokens,                                  or indents/dedents need to be dropped or inserted; recall
the learned breaker improves the coverage and efficiency of                                   the Figure 2 bottom example). For (i), the result shows that
the training data for the fixer.                                                              the initial fixer trained with random perturbations has lower
                                                                                              accuracy on “nested” than “not nested” for “unbalanced
4.3.3. Comparison with backtranslation                                                        parentheses” errors, and on “multi-line” than “single-line”
Table 4 compares our method (BIFI) with backtranslation.                                      for “missing comma” errors; but the performance catches
As discussed in §3.3, backtranslation is equivalent to                                        up in round 1, 2, suggesting the effect of BIFI for addressing
removing two components from BIFI: (i) using the critic                                       the low-level distribution mismatch. For (ii), the result
to verify fix/break attempts in data generation (“critic” in                                  shows that the initial fixer’s repair accuracy is very low for
Table) and (ii) training the fixer on real bad examples besides                               “redundant parenthesis pair” and “indentation error”, but it
examples generated by the breaker (“real bad”). We find that                                  achieves significantly higher performance in round 1, 2 (e.g.,
removing each component from BIFI hurts the performance                                       39%→85% for indentation errors). A possible explanation
(e.g., 90%→84%), which suggests that both components                                          is that as BIFI iteratively adds the successfully repaired cases
are important to improve the quality of training data. With                                   to training, the fixer adapts to up-weight this category of
these two innovations, BIFI outperforms backtranslation by                                    error fixing, leading to improved accuracy.
                                  Break-It-Fix-It: Unsupervised Learning for Program Repair

Figure 5 provides examples of fixer outputs. Given the             than real data. In our repair task, unpaired real data (code
bad code on the left (with an indentation error), the initial      snippets on GitHub) is available but paired real data is costly
fixer (center) attempts to fix it by inserting an indent token     to obtain. Hence we considered adaptation from synthetic
(hIi) to line 3 but fails to adjust (delete) the indent token on   paired data to real paired data. Within domain adaptation, our
the following line. The initial fixer commonly makes this          task is also related to the setting where unlabeled data in the
mistake for indentation errors, due to the mismatch between        test domain is available (Sun & Saenko, 2016; Hoffman et al.,
real errors and synthetic perturbations discussed above.           2018; Sun et al., 2020) (in our case, real bad code). The dif-
After one round of BIFI, the fixer (Figure 5 right) learns to      ference is that as our outputs are structured, we have a critic
insert and delete the correct pair of indents, fixing the error.   to check if the fixer’s output on the unlabeled data is correct.
                                                                   Leveraging this property, BIFI takes the correct outputs to cre-
5. Related work and discussion                                     ate training data in the test domain (Eq 6); and trains a breaker
                                                                   to generate more data that simulates the test domain (Eq 8).
Learning to repair code. Several works learn to repair
code from labeled datasets of source code edits made by            Data augmentation. Data augmentation aims to generate
programmers, e.g., error resolution records (Just et al., 2014;    extra training data. A common approach is to increase the
Chen et al., 2019; Mesbah et al., 2019; Bader et al., 2019;        source side data, for instance by adding modifications or
Tarlow et al., 2020; Ding et al., 2020). As labeled data is        sampling from generative models (Hannun et al., 2014; Jia &
costly to prepare, various works study learning code fixers        Liang, 2016; Krizhevsky et al., 2017; Antoniou et al., 2017;
from unlabeled or synthetic data (Pu et al., 2016; Parihar         Yasunaga et al., 2018; Yu et al., 2018a; Lee et al., 2019;
et al., 2017; Ahmed et al., 2018; Pradel & Sen, 2018; Wang         Berthelot et al., 2019; Xie et al., 2020). Several works also
et al., 2018; Vasic et al., 2019; Gupta et al., 2019; Hajipour     study target side augmentation, which keeps multiple (valid)
et al., 2019; Hellendoorn et al., 2020). In particular, Gupta      target predictions made by a model and adds to training.
et al. (2017) is an early work that randomly perturbs good         This is commonly used in structured generation problems
code to prepare a synthetic paired data and trains a seq2seq       such as semantic parsing, program synthesis and molecule
neural network model as a fixer. Yasunaga & Liang (2020)           generation (Liang et al., 2013; Berant et al., 2013; Guu et al.,
improve on it by designing heuristic perturbations that mimic      2017; Min et al., 2019; Zhong et al., 2020; Yang et al., 2020).
common errors made by programmers. Different from the              While our method also augments training data, it differs
above work, our method (BIFI) adapts a naive fixer trained         in two aspects: 1) we use the fixer and breaker to augment
with synthetic errors towards real errors without manual,          both the source and target sides; 2) our goal is not only to
domain-specific effort. For a more comprehensive review of         increase the amount of training data, but also to adapt to the
automatic code repair, we refer readers to Monperrus (2020).       distribution of interest (real bad examples).
Denoising autoencoding. Denoising autoencoding (Vin-               Self-training. Self-training (Lee, 2013; McClosky et al.,
cent et al., 2008) trains a model that recovers original data      2006; Kumar et al., 2020; Xie et al., 2021) applies a trained
from randomly corrupted versions, and is widely used as            model to unlabeled data, obtains predicted targets (pseudo-
an effective self-supervised representation learning and pre-      labels), and uses them as extra training examples. Similarly,
training strategy, e.g., in computer vision (Erhan et al., 2010)   co-training (Blum & Mitchell, 1998) and tri-training (Zhou
and natural language processing (NLP) (Lewis et al. (2020),        & Li, 2005) train multiple models and add predicted targets
which randomly drops / replaces tokens in a sentence and           on which these models agree. Our method also applies
learns to recover). Our initial fixer trained with random per-     trained models (breaker and fixer) to unlabeled data to
turbations is a denoising autoencoder. Crucially, instead          generate targets, with a difference that we use the critic to
of using it purely for representation learning, we show that       verify the predictions and only keep correct ones.
through the BIFI algorithm, one can turn the vanilla denoising
                                                                   Unsupervised machine translation (MT). Unsupervised
autoencoder into a usable fixer that repairs real-world bad ex-
                                                                   MT learns translators from unpaired corpora (Artetxe et al.,
amples with high accuracy. On a related note, Lee et al. (2019)
                                                                   2018a;b; Lachaux et al., 2020). Backtranslation (Sennrich
adapt a denoising autoencoder into an autocomplete system.
                                                                   et al., 2016; Lample et al., 2018a;b) is a common approach
Domain adaptation. Domain adaptation aims to address               that uses the target-to-source model to generate noisy sources
the mismatch in data distribution between training and test        and then trains the source-to-target model to reconstruct the
domains (Daume III & Marcu, 2006; Quionero-Candela et al.,         targets (also related to cycle-consistency (Zhu et al., 2017;
2009; Koh et al., 2021). Such domain shifts typically occur        Hoffman et al., 2018) and style transfer (Shen et al., 2017;
across related but different datasets (Torralba & Efros, 2011;     Yang et al., 2018; Zhang et al., 2019)). One may view the
Fang et al., 2013; Venkateswara et al., 2017; Yu et al., 2018b;    “bad-side” and “good-side” in our repair task as two source/
2019; Peng et al., 2019; Kamath et al., 2020), as well as from     target languages in MT and apply backtranslation. The main
synthetic data to real data (including sim2real) (Wang et al.,     difference is that the repair task has a critic, which motivated
2015; Ganin & Lempitsky, 2015; Richter et al., 2016; Peng          our BIFI algorithm: BIFI (i) uses the critic to verify if the
et al., 2018; Hellendoorn et al., 2019; Xu et al., 2020; Belle-    generated examples are actually fixed or broken (Eq 6,
mare et al., 2020), as synthetic data can be easier to obtain      8), and (ii) trains the fixer on real bad examples besides
                                 Break-It-Fix-It: Unsupervised Learning for Program Repair

examples generated by the breaker (Eq 9). We found these         Bellemare, M. G., Candido, S., Castro, P. S., Gong, J.,
techniques improve the correctness of the generated training       Machado, M. C., Moitra, S., Ponda, S. S., and Wang, Z.
data (§4.3.3). While we focused on code repair in this work,       Autonomous navigation of stratospheric balloons using
we hope that BIFI can be applied to unsupervised MT and            reinforcement learning. Nature, 588, 2020.
style transfer by introducing a human-based or learned critic.
                                                                 Berant, J., Chou, A., Frostig, R., and Liang, P. Semantic
6. Conclusion                                                      parsing on freebase from question-answer pairs. In
                                                                   Empirical Methods in Natural Language Processing
We considered the problem of learning a fixer from unpaired        (EMNLP), 2013.
data and a critic (code analyzer or compiler), and proposed a
new approach, Break-It-Fix-It (BIFI). The idea of BIFI is to     Berthelot, D., Carlini, N., Goodfellow, I., Papernot, N.,
train a breaker and use the critic to amass more realistic and     Oliver, A., and Raffel, C. A. Mixmatch: A holistic
correct paired data for training the fixer. Using two code re-     approach to semi-supervised learning. In Advances in
pair datasets (GitHub-Python and DeepFix), we showed how           Neural Information Processing Systems (NeurIPS), 2019.
BIFI adapts baseline fixers towards realistic distributions
of code errors, achieving improved repair performance. We        Blum, A. and Mitchell, T. Combining labeled and unlabeled
note that BIFI is not about simply collecting more training        data with co-training. In Conference on computational
data, but rather turning raw unlabeled data into usable paired     learning theory, 1998.
data with the help of a critic. This is a potentially powerful
                                                                 Chen, Z., Kommrusch, S. J., Tufano, M., Pouchet, L.-N.,
and general framework applicable to many areas such as
                                                                   Poshyvanyk, D., and Monperrus, M.           Sequencer:
molecular design, text editing, and machine translation.
                                                                   Sequence-to-sequence learning for end-to-end program
                                                                   repair. IEEE Transactions on Software Engineering, 2019.
Acknowledgments
We thank Michael Xie, members of the Stanford P-Lambda,          Daume III, H. and Marcu, D. Domain adaptation for
SNAP and NLP groups, as well as our anonymous reviewers            statistical classifiers. Journal of artificial Intelligence
for valuable feedback. This work was supported in part by          research, 2006.
Funai Foundation Fellowship and NSF CAREER Award                 Dinella, E., Dai, H., Li, Z., Naik, M., Song, L., and Wang,
IIS-1552635.                                                       K. Hoppity: Learning graph transformations to detect
                                                                   and fix bugs in programs. In International Conference
Reproducibility                                                    on Learning Representations (ICLR), 2020.
Code and data are available at https://github.com/
                                                                 Ding, Y., Ray, B., Devanbu, P., and Hellendoorn, V. J.
michiyasunaga/bifi. Experiments are available at
                                                                   Patching as translation: the data and the metaphor. In
https://worksheets.codalab.org/worksheets/
                                                                   Automated Software Engineering (ASE), 2020.
0xfddb2ef01a9f4dc0b5d974a5a97174be.
                                                                 Erhan, D., Courville, A., Bengio, Y., and Vincent, P. Why
References                                                         does unsupervised pre-training help deep learning?
Ahmed, U. Z., Kumar, P., Karkare, A., Kar, P., and Gulwani,        In Artificial Intelligence and Statistics (AISTATS), pp.
  S. Compilation error repair: for the student programs,           201–208, 2010.
  from the student programs. In International Conference
                                                                 Fang, C., Xu, Y., and Rockmore, D. N. Unbiased metric
  on Software Engineering (ICSE), pp. 78–87, 2018.
                                                                   learning: On the utilization of multiple datasets and web
Antoniou, A., Storkey, A., and Edwards, H. Data augmen-            images for softening bias. In International Conference
  tation generative adversarial networks. arXiv preprint           on Computer Vision (ICCV), 2013.
  arXiv:1711.04340, 2017.
                                                                 Ganin, Y. and Lempitsky, V. Unsupervised domain adap-
Artetxe, M., Labaka, G., and Agirre, E. Unsupervised statisti-     tation by backpropagation. In International Conference
  cal machine translation. arXiv preprint arXiv:1809.01272,        on Machine Learning (ICML), 2015.
  2018a.
                                                                 Gupta, R., Pal, S., Kanade, A., and Shevade, S. K. Deepfix:
Artetxe, M., Labaka, G., Agirre, E., and Cho, K. Unsu-             Fixing common C language errors by deep learning. In
  pervised neural machine translation. In International           Association for the Advancement of Artificial Intelligence
  Conference on Learning Representations (ICLR), 2018b.           (AAAI), 2017.

Bader, J., Scott, A., Pradel, M., and Chandra, S. Getafix:       Gupta, R., Kanade, A., and Shevade, S. Deep reinforcement
  Learning to fix bugs automatically. Proceedings of the           learning for programming language correction. In
  ACM on Programming Languages, 3(OOPSLA):1–27,                   Association for the Advancement of Artificial Intelligence
  2019.                                                           (AAAI), 2019.
                                  Break-It-Fix-It: Unsupervised Learning for Program Repair

Guu, K., Pasupat, P., Liu, E. Z., and Liang, P. From               Kumar, A., Ma, T., and Liang, P. Understanding self-
  language to programs: Bridging reinforcement learning              training for gradual domain adaptation. In International
  and maximum marginal likelihood. In Association for               Conference on Machine Learning (ICML), 2020.
 Computational Linguistics (ACL), 2017.
                                                                   Lachaux, M.-A., Roziere, B., Chanussot, L., and Lample,
Hajipour, H., Bhattacharya, A., and Fritz, M. Samplefix:             G. Unsupervised translation of programming languages.
  Learning to correct programs by sampling diverse fixes.            In Advances in Neural Information Processing Systems
  arXiv preprint arXiv:1906.10502, 2019.                             (NeurIPS), 2020.

Hannun, A., Case, C., Casper, J., Catanzaro, B., Diamos, G.,       Lample, G., Conneau, A., Denoyer, L., and Ranzato, M.
  Elsen, E., Prenger, R., Satheesh, S., Sengupta, S., Coates,        Unsupervised machine translation using monolingual
  A., et al. Deep speech: Scaling up end-to-end speech               corpora only. In International Conference on Learning
  recognition. arXiv preprint arXiv:1412.5567, 2014.                 Representations (ICLR), 2018a.

Hellendoorn, V. J., Proksch, S., Gall, H. C., and Bacchelli, A.    Lample, G., Ott, M., Conneau, A., Denoyer, L., and Ranzato,
  When code completion fails: A case study on real-world             M. Phrase-based & neural unsupervised machine
  completions. In International Conference on Software               translation. In Empirical Methods in Natural Language
  Engineering (ICSE), 2019.                                          Processing (EMNLP), 2018b.

Hellendoorn, V. J., Sutton, C., Singh, R., Maniatis, P., and       Lee, D.-H. Pseudo-label: The simple and efficient semi-
  Bieber, D. Global relational models of source code. In             supervised learning method for deep neural networks. In
  International Conference on Learning Representations               Workshop on challenges in representation learning, Inter-
 (ICLR), 2020.                                                       national Conference on Machine Learning (ICML), 2013.

Hoffman, J., Tzeng, E., Park, T., Zhu, J.-Y., Isola, P., Saenko,   Lee, M., Hashimoto, T. B., and Liang, P. Learning
  K., Efros, A., and Darrell, T. Cycada: Cycle-consistent ad-        autocomplete systems as a communication game. In
  versarial domain adaptation. In International Conference           Advances in Neural Information Processing Systems
  on Machine Learning (ICML), 2018.                                  (NeurIPS) Workshop on Emergent Communication, 2019.
                                                                   Levenshtein, V. I. Binary codes capable of correcting
Jia, R. and Liang, P. Data recombination for neural semantic
                                                                     deletions, insertions, and reversals. In Soviet physics
   parsing. In Association for Computational Linguistics
                                                                     doklady, 1966.
   (ACL), 2016.
                                                                   Lewis, M., Liu, Y., Goyal, N., Ghazvininejad, M., Mohamed,
Jin, W., Yang, K., Barzilay, R., and Jaakkola, T. Learning           A., Levy, O., Stoyanov, V., and Zettlemoyer, L. Bart:
   multimodal graph-to-graph translation for molecular               Denoising sequence-to-sequence pre-training for natural
   optimization. In International Conference on Learning             language generation, translation, and comprehension. In
   Representations (ICLR), 2019.                                     Association for Computational Linguistics (ACL), 2020.
Just, R., Jalali, D., and Ernst, M. D. Defects4j: A database       Liang, P., Jordan, M. I., and Klein, D. Learning dependency-
  of existing faults to enable controlled testing studies for        based compositional semantics.              Computational
  java programs. In Proceedings of the 2014 International            Linguistics, 2013.
  Symposium on Software Testing and Analysis, pp.
  437–440, 2014.                                                   McClosky, D., Charniak, E., and Johnson, M. Effective
                                                                    self-training for parsing. In North American Association
Kamath, A., Jia, R., and Liang, P. Selective question               for Computational Linguistics (NAACL), 2006.
  answering under domain shift. In Association for
  Computational Linguistics (ACL), 2020.                           Mesbah, A., Rice, A., Johnston, E., Glorioso, N., and
                                                                    Aftandilian, E. Deepdelta: learning to repair compilation
Kingma, D. and Ba, J. Adam: A method for stochastic                 errors. In Proceedings of the 2019 27th ACM Joint Meet-
  optimization. In International Conference on Learning             ing on European Software Engineering Conference and
  Representations (ICLR), 2015.                                     Symposium on the Foundations of Software Engineering,
                                                                    pp. 925–936, 2019.
Koh, P. W., Sagawa, S., Marklund, H., Xie, S. M., Zhang,
  M., Balsubramani, A., Hu, W., Yasunaga, M., Phillips,            Min, S., Chen, D., Hajishirzi, H., and Zettlemoyer, L. A
  R. L., Beery, S., et al. Wilds: A benchmark of in-the-wild        discrete hard em approach for weakly supervised question
  distribution shifts. In International Conference on               answering. In Empirical Methods in Natural Language
  Machine Learning (ICML), 2021.                                    Processing (EMNLP), 2019.
Krizhevsky, A., Sutskever, I., and Hinton, G. E. Imagenet          Monperrus, M. The living review on automated program
  classification with deep convolutional neural networks.           repair. Technical Report hal-01956501. HAL/archives-
  Communications of the ACM, 2017.                                  ouvertes.fr., 2020.
                                  Break-It-Fix-It: Unsupervised Learning for Program Repair

Parihar, S., Dadachanji, Z., Praveen Kumar Singh, R. D.,           Taghipour, K. and Ng, H. T. A neural approach to automated
  Karkare, A., and Bhattacharya, A. Automatic grading                essay scoring. In Empirical Methods in Natural Language
  and feedback using program repair for introductory                 Processing (EMNLP), 2016.
  programming courses. In ACM Conference on Innovation
  and Technology in Computer Science Education, 2017.              Tarlow, D., Moitra, S., Rice, A., Chen, Z., Manzagol, P.-A.,
                                                                     Sutton, C., and Aftandilian, E. Learning to fix build errors
Pascanu, R., Mikolov, T., and Bengio, Y. On the difficulty of        with graph2diff neural networks. In Proceedings of the
  training recurrent neural networks. In International confer-       IEEE/ACM 42nd International Conference on Software
  ence on machine learning (ICML), pp. 1310–1318, 2013.              Engineering Workshops, pp. 19–20, 2020.

Peng, X., Usman, B., Kaushik, N., Wang, D., Hoffman, J.,           Torralba, A. and Efros, A. A. Unbiased look at dataset bias. In
  and Saenko, K. Visda: A synthetic-to-real benchmark for            Computer Vision and Pattern Recognition (CVPR), 2011.
  visual domain adaptation. In Computer Vision and Pattern         Vasic, M., Kanade, A., Maniatis, P., Bieber, D., and Singh,
  Recognition (CVPR), 2018.                                          R. Neural program repair by jointly learning to localize
                                                                     and repair. In International Conference on Learning
Peng, X., Bai, Q., Xia, X., Huang, Z., Saenko, K., and Wang,
                                                                     Representations (ICLR), 2019.
  B. Moment matching for multi-source domain adaptation.
  In International Conference on Computer Vision (ICCV),           Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones,
  2019.                                                              L., Gomez, A. N., Kaiser, L., and Polosukhin, I. Attention
                                                                     is all you need. In Advances in Neural Information
Pradel, M. and Sen, K. Deepbugs: A learning approach to              Processing Systems (NeurIPS), 2017.
  name-based bug detection. Proceedings of the ACM on
  Programming Languages, 2(OOPSLA):1–25, 2018.                     Venkateswara, H., Eusebio, J., Chakraborty, S., and
                                                                     Panchanathan, S. Deep hashing network for unsupervised
Pu, Y., Narasimhan, K., Solar-Lezama, A., and Barzilay, R.           domain adaptation. In Computer Vision and Pattern
  sk p: a neural program corrector for moocs. In Companion           Recognition (CVPR), pp. 5018–5027, 2017.
  Proceedings of the 2016 ACM SIGPLAN International
  Conference on Systems, Programming, Languages and                Vincent, P., Larochelle, H., Bengio, Y., , and Manzagol, P.-A.
  Applications: Software for Humanity, pp. 39–40, 2016.              Extracting and composing robust features with denoising
                                                                     autoencoders. In International Conference on Machine
Quionero-Candela, J., Sugiyama, M., Schwaighofer, A., and            Learning (ICML), 2008.
  Lawrence, N. D. Dataset shift in machine learning. The
  MIT Press, 2009.                                                 Wang, K., Singh, R., and Su, Z. Dynamic neural program
                                                                    embeddings for program repair.       In International
Richter, S. R., Vineet, V., Roth, S., and Koltun, V. Playing        Conference on Learning Representations (ICLR), 2018.
  for data: Ground truth from computer games. In European
                                                                   Wang, Y., Berant, J., and Liang, P. Building a semantic parser
  conference on computer vision, 2016.
                                                                    overnight. In Association for Computational Linguistics
Sennrich, R., Haddow, B., and Birch, A. Improving neural            (ACL), 2015.
  machine translation models with monolingual data. In             Xie, Q., Dai, Z., Hovy, E., Luong, M.-T., and Le, Q. V.
  Association for Computational Linguistics (ACL), 2016.             Unsupervised data augmentation for consistency training.
                                                                     In Advances in Neural Information Processing Systems
Seo, H., Sadowski, C., Elbaum, S., Aftandilian, E., and
                                                                     (NeurIPS), 2020.
  Bowdidge, R. Programmers’ build errors: A case study
  at google. In International Conference on Software               Xie, S. M., Kumar, A., Jones, R., Khani, F., Ma, T., and
  Engineering (ICSE), 2014.                                          Liang, P. In-n-out: Pre-training and self-training using
                                                                     auxiliary information for out-of-distribution robustness.
Shen, T., Lei, T., Barzilay, R., and Jaakkola, T. Style transfer     In International Conference on Learning Representations
  from non-parallel text by cross-alignment. In Advances in          (ICLR), 2021.
  Neural Information Processing Systems (NeurIPS), 2017.
                                                                   Xu, S., Semnani, S. J., Campagna, G., and Lam, M. S.
Sun, B. and Saenko, K. Deep coral: Correlation alignment            Autoqa: From databases to qa semantic parsers with only
  for deep domain adaptation. In European Conference on              synthetic training data. In Empirical Methods in Natural
  Computer Vision (ECCV), 2016.                                     Language Processing (EMNLP), 2020.
Sun, Y., Wang, X., Liu, Z., Miller, J., Efros, A. A., and          Yang, K., Jin, W., Swanson, K., Barzilay, R., and Jaakkola, T.
  Hardt, M. Test-time training for out-of-distribution               Improving molecular design by stochastic iterative target
  generalization. In International Conference on Machine             augmentation. In International Conference on Machine
  Learning (ICML), 2020.                                             Learning (ICML), 2020.
                                 Break-It-Fix-It: Unsupervised Learning for Program Repair

Yang, Z., Hu, Z., Dyer, C., Xing, E. P., and Berg-Kirkpatrick,
  T. Unsupervised text style transfer using language models
  as discriminators. In Advances in Neural Information
  Processing Systems (NeurIPS), 2018.
Yasunaga, M. and Liang, P. Graph-based, self-supervised
  program repair from diagnostic feedback. In International
  Conference on Machine Learning (ICML), 2020.
Yasunaga, M., Kasai, J., and Radev, D. Robust multilingual
  part-of-speech tagging via adversarial training. In North
  American Association for Computational Linguistics
  (NAACL), 2018.
Yu, T., Yasunaga, M., Yang, K., Zhang, R., Wang, D., Li, Z.,
  and Radev, D. Syntaxsqlnet: Syntax tree networks for com-
  plex and cross-domaintext-to-sql task. In Empirical Meth-
  ods in Natural Language Processing (EMNLP), 2018a.
Yu, T., Zhang, R., Yang, K., Yasunaga, M., Wang, D.,
  Li, Z., Ma, J., Li, I., Yao, Q., Roman, S., et al. Spider:
  A large-scale human-labeled dataset for complex and
  cross-domain semantic parsing and text-to-sql task. In
  Empirical Methods in Natural Language Processing
  (EMNLP), 2018b.
Yu, T., Zhang, R., Yasunaga, M., Tan, Y. C., Lin, X. V.,
  Li, S., Er, H., Li, I., Pang, B., Chen, T., et al. Sparc:
  Cross-domain semantic parsing in context. In Association
  for Computational Linguistics (ACL), 2019.
Zhang, Z., Ren, S., Liu, S., Wang, J., Chen, P., Li, M.,
  Zhou, M., and Chen, E. Style transfer as unsupervised
  machine translation. In Association for the Advancement
  of Artificial Intelligence (AAAI), 2019.
Zhong, V., Lewis, M., Wang, S. I., and Zettlemoyer, L.
  Grounded adaptation for zero-shot executable semantic
  parsing. In Empirical Methods in Natural Language
  Processing (EMNLP), 2020.
Zhou, Z.-H. and Li, M. Tri-training: Exploiting unlabeled
  data using three classifiers. IEEE Transactions on
  knowledge and Data Engineering, 2005.
Zhu, J.-Y., Park, T., Isola, P., and Efros, A. A. Unpaired
  image-to-image translation using cycle-consistent
  adversarial networks. In International Conference on
  Computer Vision (ICCV), 2017.
