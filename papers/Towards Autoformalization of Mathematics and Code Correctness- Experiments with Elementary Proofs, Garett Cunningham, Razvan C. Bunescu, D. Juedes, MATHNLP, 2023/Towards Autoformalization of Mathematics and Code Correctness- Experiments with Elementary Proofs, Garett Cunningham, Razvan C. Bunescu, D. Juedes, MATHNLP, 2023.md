                                             Towards Autoformalization of Mathematics and Code Correctness:
                                                          Experiments with Elementary Proofs
                                              Garett Cunningham                   Razvan C. Bunescu                      David Juedes
                                                School of EECS               Department of Computer Science             School of EECS
                                                Ohio University                     UNC Charlotte                       Ohio University
                                               Athens, OH 45701                   Charlotte, NC 28223                  Athens, OH 45701
                                              gc974517@ohio.edu                razvan.bunescu@uncc.edu                 juedes@ohio.edu


                                                              Abstract                         the reader—proofs must be convincing to and com-
                                                                                               prehensible by mathematicians. For the third point,
                                            The ever-growing complexity of mathemati-          he notes that, “Most mathematicians and philoso-
                                            cal proofs makes their manual verification by      phers believe that any acceptable proof can be for-
                                            mathematicians very cognitively demanding.         malized. We can always find an appropriate formal
arXiv:2301.02195v1 [cs.CL] 5 Jan 2023




                                            Autoformalization seeks to address this by
                                                                                               language and theory in which the informal proof
                                            translating proofs written in natural language
                                            into a formal representation that is computer-     can be embedded and ‘filled out’ into a rigorous
                                            verifiable via interactive theorem provers. In     formal proof.” For most mathematicians, this third
                                            this paper, we introduce a semantic parsing ap-    part is crucial for ensuring that subtle, but fatal,
                                            proach, based on the Universal Transformer         errors in logic do not exist in mathematical proof.
                                            architecture, that translates elementary math-        Great progress has been made since the 1970’s
                                            ematical proofs into an equivalent formaliza-
                                                                                               in fully formalizing significant mathematical re-
                                            tion in the language of the Coq interactive the-
                                            orem prover. The same architecture is also         sults. For instance, the Feit-Thompson Theorem
                                            trained to translate simple imperative code dec-   (Gonthier et al., 2013; Gonthier, 2013) and the Four
                                            orated with Hoare triples into formally veri-      Color Theorem (Gonthier, 2008) have been for-
                                            fiable proofs of correctness in Coq. Exper-        mally verified using the proof assistant Coq (Bertot
                                            iments on a limited domain of artificial and       and Castéran, 2013), and the Kepler Conjecture
                                            human-written proofs show that the models          (Hales, 2005; Hales et al., 2017) has been formally
                                            generalize well to intermediate lengths not
                                                                                               verified using the proof assistants Isabelle and HOL
                                            seen during training and variations in natural
                                            language.                                          Light (Nipkow et al., 2002). Moreover, proof assis-
                                                                                               tants have demonstrated immense utility for soft-
                                                                                               ware verification, such as the full certification of a
                                        1   Introduction
                                                                                               C compiler (Leroy, 2009). Proofs demonstrating
                                        To the uninitiated, the notion of mathematical proof   the correct behavior of code share a similar struc-
                                        represents simply an argument written by people        ture to proofs in pure mathematics, where systems
                                        to convince others of mathematical truth. How-         like Hoare logic replace standard first-order logic.
                                        ever, in a real sense, mathematical proof must have    Thus, Tymoczko’s criteria for mathematical proof
                                        formal underpinnings that go beyond the written        can be extended to the verification of programs.
                                        argument. Arguments that lack such underpinnings       For many experts, LaTeX provides an excellent
                                        might have fatal errors or even logical inconsisten-   tool for satisfying the first two criteria. In addition,
                                        cies (see, for example, Russell’s Paradox (Irvine      carefully written LaTeX (Higham, 2020) provides
                                        and Deutsch, 2021)). Nevertheless, mathematical        a rich structure for establishing the third criterion.
                                        arguments written in natural language are the norm        The vast majority of modern mathematics is ex-
                                        and they have great value.                             pressed using natural language (NL), with the over-
                                           In Tymoczko (1979)’s well-known paper that dis-     whelming majority typeset in LaTeX. Fully for-
                                        cusses a somewhat controversial (at the time) proof    malizing mathematics using proof assistants is still
                                        of the Four Color Theorem (Appel and Haken,            a difficult and time consuming task. This paper
                                        1977; Appel et al., 1977), he explores “what is a      takes some preliminary steps toward bridging this
                                        mathematical proof?” He posits that all mathemati-     gap by exploring how modern machine learning
                                        cal proofs must be (i) convincing, (ii) surveyable,    techniques can be used to convert carefully writ-
                                        and (iii) formalizable. The first two points are for   ten LaTeX into equivalent, and formally verified
mathematics in Coq, a process referred to as auto-         represented in Coq. This work focuses on the proof
formalization in the literature (Szegedy, 2020).           assistant Coq (Bertot and Castéran, 2013) because
   Wang et al. (2018, 2020) explored the similar           (a) there is a rich set of mathematical libraries that
task of translating mathematical statements from           have been developed for it, (b) it has been used
LaTeX into Mizar, using LSTM-based models with             successfully to reason about significant computa-
attention. To generate aligned LaTeX-Mizar pairs,          tion artifacts, such as the ComperCert C compiler
they use a tool (Bancerek, 2006) that translates           (Leroy, 2009)), and (c) it benefits from a rich set of
top-level Mizar statements into artificial LaTeX           training material for the proof assistant related to
sentences, a task that is facilitated by the fact that     software verification (Pierce et al., 2010).
Mizar is human readable and similar in length with            Each class of examples demonstrates features
the corresponding LaTeX version. Carman (2021)             necessary for the successful autoformalization of
evaluated the competency of LSTMs toward for-              mathematical theorems and proofs. For example,
malizing a restricted set of artificially generated the-   POWERS and COMPOSITES examples may define
orems about simple arithmetic expressions, report-         useful terminology to make the theorems shorter,
ing reasonable success over expression lengths seen        e.g. proving that 4 is a square, or conversely they
during training. More recently, Wu et al. (2022)           may state theorems directly without any prelim-
evaluated Codex and PaLM on a significantly more           inary definitions, e.g. proving ∃n. n2 = 4. As
limited, but human-written set of theorems in alge-        shown in Figures 3 and 4, this corresponds in Coq
bra and number theory.                                     to aliasing propositions using the Definition key-
   In contrast to prior work, we address the auto-         word. Additionally, the examples in the dataset
formalization of both theorems and their proofs,           provide a stress test of the copying mechanism de-
and extend the scope to proofs of code correctness.        scribed in Section 3.1, testing its ability to learn
We use a number of manually written mathemati-             the correct order and number of terms to include
cal statements to abstract a complex grammar that          in mathematical expressions, as well as their place-
is then used to generate a dataset of substantially        ment in theorems and proofs, in a way that general-
longer and more diverse mathematical theorems              izes to arbitrary tokens in mathematical language.
and proofs. We develop an architecture based
                                                              For each of the four classes of theorems and
on the Universal Transformer (Dehghani et al.,
                                                           proofs, we manually created a few examples our-
2018) and adapt a copying mechanism (Gu et al.,
                                                           selves in order to guide the construction of a com-
2016) to handle arbitrary numbers and variable
                                                           plex grammar that is then used to generate a dataset
names at test time. The models are evaluated exten-
                                                           of substantially longer and more diverse mathemat-
sively on their ability to systematically generalize
                                                           ical theorems and proofs. Each dataset is generated
to statement lengths not seen during training, for
                                                           using its corresponding grammar in an identical
which we report sequence-level accuracy as well
                                                           way. First, a random seed is sampled that controls
as a semantic-level accuracy calculated by combin-
                                                           the overall structure of the theorem, proof, and
ing sequence-level accuracy for the theorem and
                                                           definition, if any. Then, the skeleton structure of
running Coq to determine if the generated proof
                                                           the proof is completed with phrases that are sam-
is correct. Code and data are made available at
                                                           pled from a separate context-free grammar. The
https://github.com/gc974517/autoformalization.
                                                           coarse control of the skeleton structure allows the
                                                           construction of examples with interesting features
2   Dataset of Theorems and Proofs                         like sublemmas, forward or backward proof direc-
We create two independent datasets of mathemat-            tion, coreference, or additional conditions for the
ical statements that overall correspond to four            theorem, among others.
classes of theorems and proofs: the first dataset con-        Many of the difficulties in formalizing mathe-
tains three classes of arithmetic statements (EVEN -       matical statements from NL into Coq stem from
ODD , COMPOSITES , and POWERS ), described in              the wide variability in the level of detail of mathe-
detail in Section 2.1, and the second dataset contain-     matical proofs, and the frequent mismatch between
ing statements about code correctness via Hoare            what is considered an acceptable inference step in
logic (POLY), described in detail in Section 2.2.          NL proofs vs. an inference step in Coq. Further-
In each example, the input theorem-proof pair is           more, there may be multiple Coq proofs for any
given in LaTeX, whereas the formalized output is           given theorem, at different levels of granularity. We
                  LaTeX Input Sequence                                           LaTeX Input Sequence

 Theorem. 28M + 308 is even.                                   Theorem. 450 + a · 192 + j · 462 is guaranteed to be
                                                               even for any natural terms j, and a.
 Proof. We know the summation between even numbers
 in N will be an even number. Observe that 308 is known        Proof. It can be justified that 192 · a + j · 462 is trivially
 to be even. Additionally, note that the pair M × 28 is        even. Note that 192a is an even number in N because
 trivially even. This is true because the coefficient 28 is    multiplying between an even integer with an arbitrary
 even.                                                         number in N is guaranteed to be even. Likewise, 462j
                                                               is trivially an even number in N. The claim is proven as
                  Coq Output Sequence                          a consequence of the fact that the sum of even numbers
                                                               with an even number will be in itself an even number.
 Require Import Arith.                                         Therefore, our theorem holds.
 Theorem M28_308:
   forall M : nat, Nat.even(28 * M + 308) = true.                                Coq Output Sequence
 Proof.
   intros.                                                     Require Import Arith.
   repeat rewrite Nat.even_add.                                Theorem a450_192j_450_even:
   assert (H1: Nat.even 308 = true).                             forall j a : nat,
   { auto. }                                                     Nat.even (192 * a + 462 * j + 450) = true.
   assert (H2: Nat.even 28 = true).                            Proof.
   { auto. }                                                     intros.
   assert (H3: Nat.even (28 * M) = true).                        rewrite Nat.even_add.
   { rewrite Nat.even_mul.                                       assert (H1: Nat.even (192 * a) = true).
     rewrite H2.                                                 { rewrite Nat.even_mul.
     auto. }                                                       auto. }
   rewrite H1.                                                   assert (H2: Nat.even (462 * j) = true).
   rewrite H3.                                                   { rewrite Nat.even_mul.
   auto.                                                           auto. }
 Qed.                                                            assert (H3: Nat.even
                                                                   (192 * a + 462 * j) = true).
Figure 1: Generated example from the EVEN - ODD set.             { repeat rewrite Nat.even_add.
                                                                   rewrite H1.
                                                                   rewrite H2.
                                                                   auto. }
address this ambiguity by requiring the structure of             rewrite H3.
the Coq proof to match the overall structure of the              auto.
                                                               Qed.
NL proof. This is achieved by quasi-synchronously
generating the LaTeX and Coq versions of mathe-               Figure 2: Instance of sublemma use in the EVEN - ODD
matical statements, while still allowing for some             dataset. The proof that the sum of non-constant terms is
simple re-orderings in order to improve general-              even (assertion H3) is given before proving the theorem.
ization performance, e.g. swapping arguments of
commutative operations.
   In total, the grammar-based method for gen-                whole expression. Proofs make use of this fact
erating examples can theoretically produce over               with varying rigor based on our manually designed
283 million unique arithmetic examples and over               grammar, an example of which is shown by Figure
491,000 unique code examples, before consider-                1. The Coq program is generated concurrently with
ing variations in phrasing by sampling from the               the paired LaTeX example. The example shown in
context-free grammar.                                         Figure 2 illustrates the generation and use of prior
                                                              facts to prove an implicit sublemma, in both the
2.1   Arithmetic Statements                                   natural language and matching Coq version.
We generated three classes of mathematical state-                Examples of theorems and proofs for POWERS
ments, i.e. theorem-proof pairs:                              and COMPOSITES share a similar structure in both
   • EVEN - ODD: an expression is even or odd.                their LaTeX and Coq forms, as shown in Figures 3
                                                              and 4, respectively. The theorems assert the ex-
   • COMPOSITES: a number is composite.
                                                              istence of a natural number such that a defining
   • POWERS: a number is an integer power of n.               property holds and their proofs are constructive,
EVEN - ODD examples contain arithmetic expres-                with the distinction that examples for composites
sions of n variables with even coefficients that are          prove factorization into n factors.
summed with a constant term, meaning that the                   For both training and testing, we generate 5,000
parity of this constant determines the parity of the          even-odd, 5,000 composites, and 2,000 powers ex-
                 LaTeX Input Sequence                      respectively. This is done in order to evaluate the
 Definition. We define that w ∈ N is a composite natural   model’s ability to generalize to unseen arithmetic
 number if taking some R, Q ∈ N we have Q, R ≥ 2 and       expression lengths and numbers of factors.
 Q × R = w.
 Theorem. 35 is a composite whole number.                  2.1.1    Handwritten Examples
 Proof. Remember that a composite natural number is the    We also created a small collection of 45 human-
 multiplication between Q and R such that Q and R ≥ 2.     written LaTeX theorem-proof pairs to evaluate per-
 Allow R = 7, Q = 5. We justify the result is valid as
 35 = Q · R.                                               formance on examples outside of our manually
                                                           generated grammar. These are distinct from the
                 Coq Output Sequence
                                                           original manually written examples that were used
 Require Import Lia.
                                                           to guide the development of the generative gram-
 Definition composite                                      mar. There are 15 examples for each type of proof
   (w : nat) :=                                            from the arithmetic set, using the same vocabulary
     exists R Q : nat,
     (Q >= 2) /\ (R >= 2)                                  with a number of unseen grammatical structures.
     /\ (Q * R = w).
 Theorem w_composite:                                      2.2     Code Correctness Statements
   composite 35.
 Proof.                                                    We create a dataset of correctness proofs about
   unfold composite.                                       short programs written in the imperative program-
   exists 7.
   exists 5.                                               ming language Imp (Pierce et al., 2018), which we
   lia.                                                    call POLY. The programs represent various algo-
 Qed.                                                      rithms for evaluating a polynomial, and their proofs
                                                           of correctness verify that the programs correctly
     Figure 3: Generated COMPOSITES example.
                                                           model the polynomial as a mathematical function.
                                                           Proofs are conducted as either fully decorated pro-
                 LaTeX Input Sequence
                                                           grams or as sequences of Hoare triples with natural
 Definition. We say o is a square whenever there exists    language justifying steps in between. An example
 some whole number Z such that Z ≥ 2 and o = Z 2 .         is shown in Figure 5.
 Theorem. o = 64 is a square.                                 For both training and testing data, we generate
 Proof. Let Z = 8. Observe that 64 = 82 . Also notice      5,000 examples. We train on programs containing
 Z = 8 is more than or equal to 2. This yields 64 is a     2, 3, 5, 7, 9, and 11 lines, then test on programs con-
 square whole number.
                                                           taining from 2 up to 14 lines to evaluate the model’s
                 Coq Output Sequence                       ability to generalize to novel program lengths.

 Require Import Lia.                                       3     Semantic Parsing Architecture
 Definition square
   (o : nat) :=
     exists Z : nat,
                                                           To formalize LaTeX statements into Coq, we de-
     (Z >= 2) /\ (o = Z^2).                                veloped an encoder-decoder architecture based on
 Theorem square_64:                                        the Universal Transformer (Dehghani et al., 2018).
   square 64.
 Proof.                                                    Similar to Csordás et al. (2021), we do so by adding
   unfold square.                                          recursive passes into the encoder and decoder of
   exists 8.                                               a base Transformer (Vaswani et al., 2017), thus
   assert (H1: 8 >= 2).
   { lia. }                                                making the model analogous to a Universal Trans-
   repeat split.                                           former without adaptive computation time (ACT).
   apply H1.                                               Further, we introduce a copying mechanism and
 Qed.
                                                           support for out-of-vocabulary mathematical terms.
 Figure 4: Generated example from the POWERS set.
                                                           3.1     Copying Mechanism
                                                           Mathematical language contains features uncom-
amples. We train on values of n ∈ {2, 3, 5, 7, 9}          mon or non-existent in natural language, such as
and test on values n ∈ {2, 3, . . . , 12}, where n rep-    numbers, variables, and carefully defined terminol-
resents the number of variables in the arithmetic          ogy. In order to address the use of general math-
expression, the number of factors, or the power,           ematical jargon, these tokens are replaced in the
               LaTeX Input Sequence                                    Coq Output Sequence

  Theorem. Consider the following series of               Require Import String.
  commands such that                                      From PLF Require Import Imp.
                                                          From PLF Require Import Hoare.
  S := 3;                                                 Theorem poly_code_correct:
  S := 3 + S * Z;                                           forall y : nat,
  S := 1 + S * Z                                            {{ Z = y }}
                                                            S := 3;
  Allow Z = y, for any natural number y, ahead              S := 3 + S * Z;
                                                            S := 1 + S * Z
  of running this code then S = 3 × y 2 + 3 × y + 1         {{ S = 3 * y ^ 2 + 3 * y + 1 }}.
  after the set of instructions has executed.             Proof.
                                                            intros.
  Proof. By application of usual Hoare logic:               apply hoare_seq with
                                                              (Q := (
                                   {Z = y}                      (Z = y /\ S = 3)
                                                              )%assertion).
                                     S := 3;                apply hoare_seq with
                                                              (Q := (
                         {Z = y ∧ S = 3}                        (Z = y /\ S = 3 * y + 3)
                            S := 3 + S * Z;                   )%assertion).
                                                            apply hoare_seq with
                {Z = y ∧ S = 3 × y + 3}                       (Q := (
                                                                (Z = y /\ S = 3 * y^2 + 3 * y + 1)
                             S := 1 + S * Z                   )%assertion).
                            2
     {Z = y ∧ S = 3 × y + 3 × y + 1}                        all: eapply hoare_consequence_pre;
                                                            try (apply hoare_asgn || assn_auto'').
                                                          Qed.
  Hence, this program is shown to be correct.

   Figure 5: Generated POLY example: [Left] the Hoare logic proof; [Right] the code correctness proof in Coq.


LaTeX input with generic forms denoting their us-         beddings need to be trained and the model is forced
age, such as <var1> up to <varN> for variables,           to utilize contextual information in order to appro-
which effectively ensures generalization to vari-         priately copy tokens into the Coq output. In this
able renaming (Ferreira et al., 2022), <nat1> up to       way, the model has the ability to generalize to un-
<natN> for numbers, or <def> for definitions, cou-        seen numbers or variable and definition names.
pled with the use of a copying mechanism adapted             The original CopyNet (Gu et al., 2016) used an
from Gu et al. (2016). Note that a different generic      encoder-decoder architecture with a copying mech-
token is introduced for each unique numerical con-        anism to calculate the probabilities of generating
stant or variable literal in the theorem and its proof,   in-vocabulary tokens vs. copying tokens from the
and the corresponding generic token is used in            input sequence to the output. Our autoformaliza-
the Coq version. For example, considering the             tion task guarantees mutual exclusivity between
hLaTeX, Coqi pair in Figure 3, <nat1>, <nat2>,            generating (g) and copying (c) tokens, which al-
<nat3>, and <nat4> would be used to replace the           lows using a simplified formula for calculating the
constants 2, 35, 7, and 5 respectively, everywhere in     probability of producing a token yt at time step t.
the LaTeX and Coq statements. Similarly, <var1>,          Letting Vc denote the Coq vocabulary, X denote
<var2>, and <var3> were used to replace variable          the input sequence of LaTeX tokens, and X denote
literals w, R, and Q. This is in contrast to using        the collection of unique tokens in X, we calculate
just two generic tokens <nat> and <var> every-            the probability of producing yt as:
where, which would make all numbers coreferent
                                                                                1 ψg (yt )
                                                                   
and all variables coreferent. Preliminary experi-                                                                yt ∈ Vc
                                                                   p(yt , g) = Z e        ,
                                                                   
                                                                   
ments validated the utility of encoding these dis-                               t
                                                          p(yt ) =              1     X
tinctions while maintaining the correct coreference                p(yt , c) =                         eψc (xj ) , yt ∈ X
                                                                   
                                                                               Zt
in both LaTeX and Coq statements.                                                       xj ∈X:xj =yt

                                                                        X                     X
  Overall, by using generic tokens for numbers,           where Zt =            eψg (yt ) +           eψc (xj ) . The scor-
variables, and definitions, only a limited set of em-                  yt ∈Vc                 xj ∈X
ing functions are given by ψg (yt ) = vy>t Wo st and                   EVEN - ODD    COMPOSITES       POLY
                                                                  n    Seq    Sem     Seq      Sem     Both
                            
ψc (xj ) = tanh h>   j W   c st , where vyt is a one-
                                                                  2    99.6   99.8   76.7      97.6   100.0
hot encoding of yt , hj is the hidden encoder state
                                                                  3    99.4   99.6   64.6      94.2   100.0
for the input token xj , st is the decoder state at step
                                                                  4    99.4   99.4   56.1      93.9    82.1
t, and Wo and Wc are learnable parameters.
                                                                  5    99.2   99.6   54.9      94.4    99.2
3.2    Encoder-Decoder Architecture                               6    98.8   98.8   57.1      94.3    45.1
                                                                  7    99.1   99.5   58.5      93.4    96.5
We diverge from the standard Transformer archi-                   8    93.8   94.0   53.5      88.3    15.7
tecture in a few crucial ways:                                    9    98.6   98.6   53.7      93.7    98.2
    • Probabilities are calculated via p(yt ) above.              10    7.0    7.0    1.2       1.6    35.6
                                                                  11    0.0    0.0    0.0       0.0    93.5
    • Absolute positional encodings are removed.
                                                                 12+    0.0    0.0    0.0       0.0     0.0
    • Self-attention uses relative positional repre-
      sentations as in Shaw et al. (2018).                        POWERS      Seq = 100.0      Sem = 100
    • Stacks of N encoder/decoder blocks have T
      recurrent passes.                                    Table 1: Sequence-level (Seq) and semantic-level
                                                           (Sem) accuracy (%) on test examples, split by expres-
All other aspects of the model remain unchanged            sion length, with the exception of POWERS.
from the original Transformer. We emphasize rel-
ative positional information over absolute in our
model architecture. Preliminary evaluations on the         using the natural language version as a guide.
EVEN - ODD dataset showed that Transformer mod-              All experiments were performed on one NVIDIA
els that use absolute positional encodings obtain          RTX-A6000 GPU with 48GB of memory.
0% sequence-level accuracy on expression lengths
that are not seen at training time. Removing re-           4.1    Arithmetic Statements
liance on absolute position resolves this type of
                                                           We evaluate a Transformer model on the full data
systematic generalization. The use of relative posi-
                                                           combining EVEN - ODD + COMPOSITES + POWERS
tional encodings for the Transformer-based models
                                                           and using both the theorem and its proof in each
was thus essential for achieving stronger systematic
                                                           sequence. We tune a model with embedding and
generalization, which also agrees with the findings
                                                           state sizes of 32, a feed forward width of 256, 4
of Csordás et al. (2021) on other NLP tasks.
                                                           encoder and decoder blocks with 4 recurrent passes,
                                                           4 attention heads, and a clipping value of 2 for self-
4     Experimental Evaluations
                                                           attention. We trained this model over minibatches
To evaluate the performance of trained models, we          of size 20, optimized with Adam using β1 = 0.9,
ran two primary experiments: first on the collection       β2 = 0.98, ε = 1e − 9, and an initial√learning rate
of arithmetic examples, then on the collection of          of 0.001, annealed by a factor of 1/ 10 based on
code correctness examples. All models are eval-            training loss plateaus with a patience of 5 epochs.
uated in terms of sequence-level accuracy, where              The results in Table 1 show that the model gener-
an example is considered correctly processed only          alizes well to the intermediate lengths of {4, 6, 8},
if the generated Coq sequence for both the theo-           with a small number of correctly translated exam-
rem and its proof perfectly matches token by to-           ples longer than the maximum of 9 used in training.
ken the ground truth sequence. We also report              Otherwise, the model fails to generalize to longer
semantic-level accuracy, for which the generated           unseen lengths, which is not surprising, given that
Coq theorem needs to attains a perfect sequence-           Transformer models are known to fail dramatically
level accuracy and the Coq engine verifies that the        at systematic generalization on longer inputs for
generated Coq proof truly proves the generated             various NLP tasks (Csordás et al., 2021), or to in-
Coq theorm, regardless of whether it matches the           cur substantial decrease in accuracy for longer sym-
ground truth version of the proof. This empha-             bolic integration problems (Welleck et al., 2022).
sizes that the model was able to capture the general       Switching to semantic-level evaluation leads to a
meaning of the natural language proof by correctly         significant increase in accuracy for COMPOSITES,
translating the theorem and successfully proving it        with a more modest increase for EVEN - ODD.
4.2   Code Correctness Statements                          like MATH (Hendrycks et al., 2021) may serve to
                                                           alleviate the problems caused by the scarcity of
We extend our scope to include data representing
                                                           aligned natural and formal mathematics data.
proofs of program correctness using the language
of Hoare logic. We train a separate model with             5   Concluding Remarks
the same embedding and state sizes, feed forward
width, and learning rates as in Section 4.1. Depth         As we have seen, it is feasible to train machine
is increased to 8 encoder and decoder blocks with 8        learning models to perform autoformalization over
recurrent passes, 8 attention heads, and a clipping        very restricted domains of math and code correct-
value of 8. The model is trained over minibatches          ness proofs. These models show capability to sys-
of size 1 with Adam, with a patience of 3 epochs.          tematically generalize to new expression lengths
   The POLY results shown in Table 1 demonstrate           and program sizes. Moreover, these models were
that the model is able to generalize to program line       able to translate previously unseen hand written
counts of {4, 6, 8, 10} unseen during training with        natural language examples, albeit with lower ac-
diminishing returns as the program length grows,           curacy. We are hopeful that this approach can be
eventually failing to generalize for lengths longer        applied to autoformalization of a larger segment of
than the maximum seen in training. We observe              mathematics and code verification.
that increasing the depth of the model significantly          As mentioned by Szegedy (2020), "Autoformal-
improved generalization. A model with identi-              ization is not just a challenge: successful autofor-
cal hyperparameters to the arithmetic experiment           malization would represent a breakthrough for gen-
yielded less then half the sequence-level accuracy         eral AI with significant implications in various do-
for intermediate program lengths. Therefore, fur-          mains." We see an especially significant impact in
ther increasing the depth of the model could push          education, where integration of autoformalization
performance closer to optimal generalization to in-        into proof assistants for introductory mathematics
termediate lengths at the cost of significantly more       and software verification courses would enable the
computing resources. Additionally, POLY exam-              detection of missing steps or misconceptions in
ples are far less prone to non-fatal token swapping        students’ proofs.
errors. We observe that semantic-level accuracy is
identical to sequence-level, as all copying errors
compromised the validity of the proof. Therefore,          References
accuracies are shown as one column (Both).                 K. Appel and W. Haken. 1977. Every planar map is
                                                             four colorable, part I: discharging. Illinois Journal
4.3   Handwritten Examples                                   of Mathematics, 21(3):429 – 490.

We also evaluate the semantic-level accuracy of            K. Appel, W. Haken, and J. Koch. 1977. Every planar
                                                             map is four colorable. II: Reducibility. Ill. J. Math.,
the trained models on the collection of 45 human-
                                                             21:491–567.
written LaTeX theorem-proof pairs. This is done
by manually verifying that the generated Coq the-          Grzegorz Bancerek. 2006. Automatic translation in
orem corresponds to the LaTeX version and that               formalized mathematics. Mechanized Mathematics
                                                             and Its Applications, 5(2):19–31.
the subsequent proof is correct according to the
Coq interpreter. The fully trained model achieved          Yves Bertot and Pierre Castéran. 2013. Interactive the-
53.3% for both EVEN - ODD and COMPOSITES, and                orem proving and program development: Coq’Art:
73.3% for POWERS.                                            the calculus of inductive constructions. Springer
                                                             Science & Business Media.
   Mistakes in almost all cases are confined to the
mishandling of out-of-vocabulary tokens, such as           Benjamin Andrew Carman. 2021. Translating LaTeX
mis-copying a variable within a definition or the            to Coq: A Recurrent Neural Network Approach to
                                                             Formalizing Natural Language Proofs. Ph.D. thesis,
omission of an assertion in the proof tied to a term.
                                                             Ohio University.
The model otherwise generated syntactically sound
Coq code. Mistakes strongly correlate with exam-           Róbert Csordás, Kazuki Irie, and Juergen Schmidhu-
ples that deviate significantly from the grammatical         ber. 2021. The devil is in the detail: Simple tricks
                                                             improve systematic generalization of transformers.
structure of the artificial data. Thus, pre-trained lan-     In Proceedings of the 2021 Conference on Empiri-
guage models as evaluated by Wu et al. (2022) or             cal Methods in Natural Language Processing, pages
pre-training new models on mathematical corpora              619–634.
Mostafa Dehghani, Stephan Gouws, Oriol Vinyals,           Tobias Nipkow, Lawrence C Paulson, and Markus
 Jakob Uszkoreit, and Łukasz Kaiser. 2018. Univer-          Wenzel. 2002. Isabelle/HOL: a proof assistant for
 sal transformers. arXiv preprint arXiv:1807.03819.         higher-order logic, volume 2283. Springer Science
                                                            & Business Media.
Deborah Ferreira, Mokanarangan Thayaparan, Marco
  Valentino, Julia Rozanova, and Andre Freitas. 2022.     Benjamin C Pierce, Chris Casinghino, Marco
  To be or not to be an Integer? Encoding Variables for     Gaboardi, Michael Greenberg, Cătălin Hriţcu,
  Mathematical Text. In Findings of the Association         Vilhelm Sjöberg, and Brent Yorgey. 2010. Software
  for Computational Linguistics: ACL 2022, pages            foundations. Webpage: http://www. cis. upenn.
  938–948, Dublin, Ireland. Association for Compu-          edu/bcpierce/sf/current/index. html.
  tational Linguistics.
G. Gonthier. 2013. Engineering mathematics: The odd       Benjamin C. Pierce, Arthur Azevedo de Amorim, Chris
  order theorem proof. In Conference Record of the          Casinghino, Marco Gaboardi, Michael Greenberg,
  Annual ACM Symposium on Principles of Program-            Cǎtǎlin Hriţcu, Vilhelm Sjöberg, Andrew Tolmach,
  ming Languages, pages 1–2. Cited By 12.                   and Brent Yorgey. 2018. Programming Language
                                                            Foundations. Software Foundations series, volume
Georges Gonthier. 2008. Formal proof – the four-color       2. Electronic textbook. Version 5.5. http://www.
  theorem. Notices of the AMS, 55(11):1382–1393.            cis.upenn.edu/~bcpierce/sf.

Georges Gonthier, Andrea Asperti, Jeremy Avi-             Peter Shaw, Jakob Uszkoreit, and Ashish Vaswani.
  gad, Yves Bertot, Cyril Cohen, François Garil-            2018. Self-attention with relative position represen-
  lot, Stéphane Le Roux, Assia Mahboubi, Russell            tations. In Proceedings of the 2018 Conference of
  O’Connor, Sidi Ould Biha, Ioana Pasca, Laurence           the North American Chapter of the Association for
  Rideau, Alexey Solovyev, Enrico Tassi, and Lau-           Computational Linguistics: Human Language Tech-
  rent Théry. 2013. A machine-checked proof of the          nologies, Volume 2 (Short Papers), pages 464–468,
  odd order theorem. In Interactive Theorem Proving,        New Orleans, Louisiana. Association for Computa-
  pages 163–179, Berlin, Heidelberg. Springer Berlin        tional Linguistics.
  Heidelberg.
                                                          Christian Szegedy. 2020. A promising path towards
Jiatao Gu, Zhengdong Lu, Hang Li, and Victor OK             autoformalization and general artificial intelligence.
   Li. 2016. Incorporating copying mechanism in             In Intelligent Computer Mathematics. CICM 2020.
   sequence-to-sequence learning. In Proceedings of         Lecture Notes in Computer Science, volume 12236,
   the 54th Annual Meeting of the Association for Com-      pages 3–20. Springer.
   putational Linguistics (Volume 1: Long Papers),
   pages 1631–1640.                                       Thomas Tymoczko. 1979. The four-color problem and
Thomas Hales, Mark Adams, Gertrud Bauer, Tat Dat            its philosophical significance. Journal of Philoso-
  Dang, John Harrison, Le Truong Hoang, Cezary              phy, 76(2):57–83.
  Kaliszyk, Victor Magron, Sean McLaughlin,
  Tat Thang Nguyen, and et al. 2017. A formal proof       Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob
  of the Kepler conjecture. Forum of Mathematics, Pi,       Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz
  5:e2.                                                     Kaiser, and Illia Polosukhin. 2017. Attention is all
                                                            you need. Advances in Neural Information Process-
Thomas C. Hales. 2005. A proof of the Kepler conjec-        ing Systems, 30:5998–6008.
  ture. Ann. Math. (2), 162(3):1065–1185.
                                                          Qingxiang Wang, Chad Brown, Cezary Kaliszyk, and
Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul          Josef Urban. 2020. Exploration of neural machine
  Arora, Steven Basart, Eric Tang, Dawn Song, and           translation in autoformalization of mathematics in
  Jacob Steinhardt. 2021. Measuring mathematical            Mizar. In Proceedings of the 9th ACM SIGPLAN
  problem solving with the math dataset. NeurIPS.           International Conference on Certified Programs and
                                                            Proofs, CPP 2020, page 85–98, New York, NY, USA.
Nicholas J. Higham. 2020. Handbook of Writing for           Association for Computing Machinery.
  the Mathematical Sciences, third edition. Society
  for Industrial and Applied Mathematics, Philadel-
                                                          Qingxiang Wang, Cezary Kaliszyk, and Josef Urban.
  phia, PA, USA.
                                                            2018. First experiments with neural translation of
Andrew David Irvine and Harry Deutsch. 2021. Rus-           informal to formal mathematics. In Intelligent Com-
  sell’s Paradox. In Edward N. Zalta, editor, The Stan-     puter Mathematics, pages 255–270, Cham. Springer
  ford Encyclopedia of Philosophy, Spring 2021 edi-         International Publishing.
  tion. Metaphysics Research Lab, Stanford Univer-
  sity.                                                   Sean Welleck, Peter West, Jize Cao, and Yejin Choi.
                                                            2022. Symbolic Brittleness in Sequence Models:
Xavier Leroy. 2009. Formal verification of a realistic      On Systematic Generalization in Symbolic Mathe-
  compiler. Communications of the ACM, 52(7):107–           matics. Proceedings of the AAAI Conference on Ar-
  115.                                                      tificial Intelligence, 36(8):8629–8637. Number: 8.
Yuhuai Wu, Albert Q Jiang, Wenda Li, Markus N
  Rabe, Charles Staats, Mateja Jamnik, and Christian
  Szegedy. 2022. Autoformalization with large lan-
  guage models. arXiv preprint arXiv:2205.12615.
