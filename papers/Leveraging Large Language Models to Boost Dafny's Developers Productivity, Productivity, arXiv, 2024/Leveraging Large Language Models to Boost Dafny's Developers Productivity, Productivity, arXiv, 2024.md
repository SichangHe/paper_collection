                                        Leveraging Large Language Models to Boost Dafny’s Developers
                                                               Productivity
                                                        Álvaro Silva                               Alexandra Mendes                                   João F. Ferreira
                                                   Independent Researcher                  HASLab / INESC TEC & Faculty of               INESC-ID & IST, University of Lisbon
                                                       Porto, Portugal                      Engineering, University of Porto                      Lisbon, Portugal
                                                   amfpsilva@hotmail.com                            Porto, Portugal                               joao@joaoff.com
                                                                                             alexandra@archimendes.com
                                        ABSTRACT                                                                of the program, are available and enable verification alongside code
                                        This research idea paper proposes leveraging Large Language Mod-        development. One such language is Dafny [21].
arXiv:2401.00963v1 [cs.SE] 1 Jan 2024




                                        els (LLMs) to enhance the productivity of Dafny developers. Al-             Dafny is celebrated for its advanced deductive verification sup-
                                        though the use of verification-aware languages, such as Dafny, has      port that offers a sophisticated backend, encompassing a compiler
                                        increased considerably in the last decade, these are still not widely   capable of producing executable binaries and a verifier tasked with
                                        adopted. Often the cost of using such languages is too high, due to     meticulously validating code conformity to specified requirements.
                                        the level of expertise required from the developers and challenges      While Dafny stands as a state-of-the-art tool in software verifica-
                                        that they often face when trying to prove a program correct. Even       tion, its application demands a profound grasp of concepts often
                                        though Dafny automates a lot of the verification process, sometimes     encountered exclusively during the formalization of specifications,
                                        there are steps that are too complex for Dafny to perform on its        which is not commonplace in conventional programming languages.
                                        own. One such case is that of missing lemmas, i.e. Dafny is unable      This complexity can hinder software development productivity in
                                        to prove a result without being given further help in the form of a     Dafny. In addition, and although Dafny has considerable adoption
                                        theorem that can assist it in the proof of the step.                    in industry (e.g. at Amazon Web Services1 and at Consensys [5–7]),
                                           In this paper, we describe preliminary work on a new Dafny plu-      it is not widely used, most likely due to the cost in effort, time, and,
                                        gin that leverages LLMs to assist developers by generating sugges-      as stated above, the need for expert knowledge when using Dafny.
                                        tions for relevant lemmas that Dafny is unable to discover and use.         Large Language Models (LLMs) have recently demonstrated ex-
                                        Moreover, for the lemmas that cannot be proved automatically, the       traordinary capabilities, exhibiting proficiency in diverse tasks such
                                        plugin also attempts to provide accompanying calculational proofs.      as engaging in conversations, retrieving and summarizing exten-
                                        We also discuss ideas for future work by describing a research          sive information, and even generating and explaining text and code
                                        agenda on using LLMs to increase the adoption of verification-          [2]. Their utility is further underscored by their application as code
                                        aware languages in general, by increasing developers productivity       suggestion tools, exemplified by GitHub Copilot [28].
                                        and by reducing the level of expertise required for crafting formal         In this research idea paper, we describe how we plan to explore
                                        specifications and proving program properties.                          LLMs’ capabilities to boost Dafny’s developers productivity and
                                                                                                                to support its wider adoption. First, we describe some of the chal-
                                                                                                                lenges identified in the use of Dafny and how we intend to address
                                        CCS CONCEPTS
                                                                                                                them. Second, we showcase preliminary work on prompting GPT-
                                        • Software and its engineering → Software notations and                 4 [2, 4] to support the automated inference of lemmas and their
                                        tools; Software verification and validation.                            proofs. Finally, we discuss implications of these results, challenges
                                                                                                                in using these tools within the context of Dafny, and the next steps
                                        KEYWORDS                                                                of our research agenda. Our proposed solution encompasses the
                                        Verification-Aware Languages, Dafny, Large Language Models, Gen-        integration of the proposed features into the Dafny plugin for VS
                                        erative AI, Software Productivity, Software Verification, Lemma         Code, seamlessly integrating the presented ideas to assist develop-
                                        Inference, Proof Inference, Automated Program Repair, Code Sum-         ers in using Dafny to write specifications and their corresponding
                                        marization                                                              implementations.
                                                                                                                    Our overarching goal is to enhance the accessibility of Dafny for
                                                                                                                new users and cultivate increased autonomy and productivity in
                                        1   INTRODUCTION                                                        Dafny’s use.
                                        As software is becoming increasingly pervasive in our daily lives, it
                                                                                                                2    SYNERGIES BETWEEN DAFNY AND LLMS
                                        is more important than ever to ensure that it does not contain bugs.
                                        Particularly in critical systems, software testing is not enough as
                                                                                                                LLMs and Dafny verification capabilities can complement each
                                        stronger assurances are needed. These assurances can be achieved
                                                                                                                other, as LLMs are inherently creative but not always reliable, whilst
                                        through software verification, which mathematically ensures that
                                                                                                                Dafny’s verification engine acts as a stringent gatekeeper, ensuring
                                        software behaves exactly as intended, with respect to a formal spec-
                                                                                                                that artifacts generated by LLMs undergo a rigorous verification
                                        ification. Several verification-aware programming languages and
                                                                                                                process. This interplay makes their combination promising.
                                        systems, where logical constructs such as pre and postconditions,
                                        invariants, and assertions provide assurances about the correctness     1 https://github.com/aws/aws-encryption-sdk-dafny
                                                                                                   Álvaro Silva, Alexandra Mendes, and João F. Ferreira


   There are several challenges that Dafny users face when using         2.3    Automated Repair
the language. An important challenge is the common case that             Most programmers make mistakes when writing code. Automated
non-trivial Dafny developments entail substantial effort in writing      Program Repair (APR) can help with this by supporting develop-
lemmas and proofs. For example, in Cassez’s verification of the          ers with automatic fix of software bugs. There are several existing
Incremental Merkle Tree Algorithm [5], almost 90% of the lines of        works that successfully applied LLMs for automated program re-
code are proofs and function definitions used in the proofs. More-       pair [19, 29, 40, 41]. However, as far as we are aware, there are
over, an experience report on using Dafny at the VerifyThis 2021         no previous developments on APR for Dafny leveraging LLMs. In
verification competition shows that the interpretability of Dafny’s      addition, in the context of Dafny, when a bug is detected, i.e. the
error messages is challenging as these are often not informative [9].    program fails to verify, the issue can be due to an incorrect spec-
   In this section, we describe four challenges that we intend to        ification or an incorrect implementation. Although most current
tackle using LLMs.                                                       research assumes that the specification is correct, focusing on re-
                                                                         pairing the implementation, it is known that many issues with
                                                                         software stem from incorrect specifications [24]. Previous work
2.1    Predicate and Lemma Inference
                                                                         on specification repair in Dafny relies on Daikon [8] for dynamic
Even though Dafny automates a lot of the verification process,           invariant inference which is then used for generating weakening
sometimes there are steps that are too complex for Dafny to perform      and strengthening candidate fixes (and their combination) [1].
on its own. One such case is that of missing lemmas, i.e. Dafny is           We are not aware of any work on Dafny’s specification or pro-
unable to prove a result without being given further help in the         gram repair using LLMs. Our goal is to explore existing approaches
form of a theorem that can assist it in the proof of the step. The       that use LLMs for automated repair and adapt/improve them to be
challenge lies not only in proving the lemmas and theorems but           used for Dafny. We also intend to tackle proof repair and to do so
also in determining the specifications of lemmas and predicates          in at least two contexts: when the code changes and existing proofs
capable of solving the problem at hand.                                  become invalid and when the user or the LLM suggest a proof that
   Various approaches have been explored in the literature to ad-        does not verify. We will follow a continuous feedback loop between
dress these challenges across a diverse range of verification tools.     LLMs and the Dafny’s verifier, where the LLM produces proofs or
For instance, infering inductive invariants in TLA+ [34], inference of   fixes to proofs and, should these not verify, the feedback produced
lemmas in Coq [33, 35] and in symbolic-Heap separation logic [37].       by Dafny is fed into the LLM to produce another suggestion.
   Our objective is to address lemma inference and general predicate
inference using LLMs. Our approach involves using prompting to
infer lemmas and predicates, and fine-tuning LLMs to infer them,         2.4    Summarization and Natural Language Specs
particularly if the zero-shot or few-shot learning approaches yield      Code summarization, the task of generating summaries that accu-
unsatisfactory results. Section 3 provides an illustrative example of    rately describe the functionalities of the code, can reduce develop-
lemma inference using prompting and GPT-4 [2].                           ers’ efforts in interpreting the goals of a program or snippet of code.
                                                                         In the context of Dafny, code summarization can also potentially
                                                                         help with understanding the intentions set out in specifications.
2.2    Proof Inference                                                   Further, as detailed above, Dafny’s error messages can be challeng-
Dafny supports calculational proofs (aka verified calculations),         ing to understand; code summarization has the potential to enhance
which are proofs by stepwise formula manipulation. As pointed            error messages with further information about the error and about
out by Leino and Polikarpova [23], calculational proofs are praised      what is the mismatch between the specifications and the code. As
for their rigor, readability, and elegance. Indeed, it has been shown    developers spend around 58% percent of their time on program
that calculational proofs can greatly improve on traditional verbose     comprehension activities [42], features that assist them in code
proofs in natural language [10–12].                                      comprehension seem valuable to enhance their productivity.
   Writing calculational proofs is challenging and any method that          We intend to explore LLMs’ capabilities in code summarization
can help infer these proofs or steps of these proofs can boost Dafny’s   to enhance error messages in Dafny, to provide explanations of
developers productivity. Moreover, proof inference can complement        specs/code, and also complement and update specs/code comments
the lemma inference described in subsection 2.1, as when lemmas          which are helpful in code understanding activities. Previous works
are added to the code, it is often the case that a proof needs to be     have shown the enormous potential of LLMs in code summarization
provided by the user. LLMs can assist in this process by providing       tasks [16, 20, 39]. Another feature that we intend to explore is
the full proof or by giving hints to the user regarding the proof        the use of LLMs to support the translation of natural language
steps. This also applies to lemmas inferred by the LLM, as proofs        specifications into Dafny, assisting developers in this task that
will also need to be provided. In addition, even though Dafny can        requires knowledge that is not commonplace.
often prove the lemmas on its own, it has been shown that, even in
those cases, adding proof steps that are not absolutely necessary
can reduce considerably the verification time [5].                       3     PRELIMINARY EXPERIMENTS
   To infer proofs, we plan to use models fine-tuned on proof data,      This section describes preliminary experiments on using LLMs to
but we will also explore few-shot prompted and even zero-shot            infer lemmas and calculational proofs. In particular we used the
prompted approaches. Section 3 provides an illustrative example of       latest version of GPT-4 Turbo, gpt-4-1106-preview, trained on data
few-shot prompted proof generation.                                      up to April 2023, enabling support for contexts with 128,000 tokens.
Leveraging Large Language Models to Boost Dafny’s Developers Productivity


method CoincidenceCount(a: array<int>,                                      You are a software expert specializing in formal methods
                        b: array<int>)                                      using the Dafny programming language. You receive the
 returns (c: nat)                                                           following program where a loop invariant could not be
 requires forall i,j ::                                                     proven. The verifier error message is inside // VERIFIER
   0<=i<j<a.Length ==> a[i]<=a[j]                                           ERROR ... //. Your task is to create lemmas and insert
 requires forall i,j ::                                                     them into the code to facilitate verification.
   0<=i<j<b.Length ==> b[i]<=b[j]                                                             (b) Prompt used to generate lemmas.
 ensures c == |multiset(a[..]) * multiset(b[..])| {
 c := 0;                                                                    lemma LemmaIntersectionAfterIncrease_m
 var m, n := 0, 0;                                                            (a: array<int>, b: array<int>, m: nat, n: nat)
 while m < a.Length &&                                                      requires 0 <= m < a.Length && 0 <= n <= b.Length
       n < b.Length                                                         requires forall i,j :: 0<=i<j<a.Length ==> a[i]<=a[j]
 invariant 0 <= m <= a.Length && 0 <= n <= b.Length                         requires forall i,j :: 0<=i<j<b.Length ==> b[i]<=b[j]
 // Fails to prove the following invariant                                  ensures |multiset(a[m..]) * multiset(b[n..])| ==
 invariant c + |multiset(a[m..]) * multiset(b[n..])|                                |multiset(a[m+1..]) * multiset(b[n..])|
           == |multiset(a[..]) * multiset(b[..])|
 decreases a.Length - m + b.Length - n {                                    lemma LemmaIntersectionAfterIncrease_n
  if {                                                                        (a: array<int>, b: array<int>, m: nat, n: nat)
   case a[m] == b[n] => {                                                   requires 0 <= m <= a.Length && 0 <= n < b.Length
    /* Suggested by GPT-4: */                                               requires forall i,j :: 0<=i<j<a.Length ==> a[i]<=a[j]
    LemmaIntersectionAfterIncrease_mn(a, b, m, n);                          requires forall i,j :: 0<=i<j<b.Length ==> b[i]<=b[j]
    c, m, n := c + 1, m + 1, n + 1;}                                        ensures |multiset(a[m..]) * multiset(b[n..])| ==
   case a[m] < b[n] => {                                                            |multiset(a[m..]) * multiset(b[n+1..])|
    /* Suggested by GPT-4: */
    LemmaIntersectionAfterIncrease_m(a, b, m, n);                           lemma LemmaIntersectionAfterIncrease_mn
    m := m + 1;}                                                              (a: array<int>, b: array<int>, m: nat, n: nat)
   case b[n] < a[m] => {                                                    requires 0 <= m < a.Length && 0 <= n < b.Length
    /* Suggested by GPT-4: */                                               requires forall i,j :: 0<=i<j<a.Length ==> a[i]<=a[j]
    LemmaIntersectionAfterIncrease_m(a, b, m, n);                           requires forall i,j :: 0<=i<j<b.Length ==> b[i]<=b[j]
    n := n + 1; }}}}                                                        //ensures |multiset(a[m..]) * multiset(b[n..])| ==
                                                                                      |multiset(a[m+1..]) * multiset(b[n+1..])|
(a) Method that computes how many elements two sorted arrays
                                                                            ensures |multiset(a[m..]) * multiset(b[n..])| ==
have in common. The second invariant cannot be verified automati-
cally. GPT-4 extends the code with calls to lemmas that enable the
                                                                                    |multiset(a[m+1..]) * multiset(b[n+1..])| + 1
verification.                                                               (c) Lemmas generated by GPT-4. The commented assertion in gray
                                                                            had to be replaced with the assertion in blue.

                                      Figure 1: GPT-4 suggests lemmas to complete method verification.


3.1     Lemma Inference                                                     in Figure 1b2 . GPT-4 inferred the lemmas shown in Figure 1c and
We use an example taken from Leino’s book [22] and shown in                 placed them in the code as shown in Figure 1a (in blue). Only a small
Figure 1a. Given two sorted arrays, the method CoincidenceCount             correction was required to make the program verify using these
computes how many elements they have in common. The postcondi-              lemmas as axioms (highlighted in blue). However, note that these
tion is expressed in terms of multisets (note that * denotes multiset       lemmas cannot be proved since they require more information in the
intersection and the vertical-bar brackets denote the cardinality of        precondition (e.g. to prove LemmaIntersectionAfterIncrease_mn,
a multiset). Since the two arrays are sorted, the algorithm can be          it is required to add a[m] == b[n] as a precondition; similar anno-
efficiently implemented using two indices (m and n) to keep track           tations are needed for the other lemmas).
of how many elements of a and b have been processed. Dafny’s
verifier is able to prove the method postcondition from the loop            3.2     Proof Inference
invariants. However, it cannot automatically prove the second in-           Our experiments with prompt engineering to infer proofs for the
variant (identified by the red comment), because it is not able to          three lemmas shown in Figure 1c were not as successful. In general,
automatically prove relevant properties about multisets. The typical        there were many syntactic errors and we had to provide many
approach to solve this is to annotate the program with lemmas that          examples of proofs to generate plausible solutions. The best result
provide enough information for the proof to be completed.
   To determine whether GPT-4 can assist us by inferring useful             2 The code used was the one shown in black, with the additional comment above the
lemmas, we used the code shown in Figure 1a and the prompt shown            invariant that cannot be proved: // VERIFIER_ERROR loop invariant violation.
                                                                            This invariant could not be proved to be maintained by the loop //.
                                                                                                                  Álvaro Silva, Alexandra Mendes, and João F. Ferreira


type pos = x | 1 <= x witness 1                                                        annotations. The main idea is to reduce correctness checking to a
                                                                                       problem of consistency checking. However, the reduction from cor-
ghost predicate IsFactor(p: pos, x: pos) {                                             rectness to consistency is not mathematically complete. Our goals
  exists q :: p * q == x }                                                             are different and more fine-grained: we aim to prove correctness
                                                                                       and to contribute with features that continuously focus on parts of
ghost function Factors(x: pos): set<pos> {                                             the program, not necessarily the program as a whole, to enhance
  set p: pos | p <= x && IsFactor(p, x) }                                              developers productivity in achieving program correctness.
                                                                                          Regarding lemma inference, we are not aware of any work fo-
lemma Factor0(p: pos, y: pos, x: pos)                                                  cused on Dafny nor work that uses LLMs, but there have been
    requires exists a :: x == p*a                                                      efforts to synthesize lemmas for Coq [33, 35], and for symbolic-
    requires exists b :: y == p*b                                                      Heap separation logic [37]. AdtInd automates proofs by induction
    ensures IsFactor(p, y + x) {                                                       over algebraic data types, where lemmas are synthesized by term
   /* Proof Suggested by GPT-4: */                                                     enumeration guided by user-specified templates [45].
    var a: pos := x / p; // Witness for x == p*a                                          Recent work on neural methods to automate proof synthesis
    var b: pos := y / p; // Witness for y == p*b                                       is related to our goals of inferring calculational proofs. Given
                                                                                       a partial proof and the proof state, neural theorem provers use
       calc {                                                                          neural networks to predict the next likely proof steps, which are
           p * (a + b);                                                                then evaluated by a proof assistant to return new proof states or
           == { arithmetic }                                                           errors. Several neural theorem provers have been proposed for
           p * a + p * b;                                                              Coq [3, 13, 14, 17, 31, 32, 38, 43], for Lean [44] and Isabelle [18, 27].
           == { definition of a and b }                                                Baldur uses LLMs to repair proofs as part of its proof synthesis ap-
           x + y; }}                                                                   proach [15]. Finally, regarding computer support for calculational
                                                                                       proofs, there have been efforts to create structure editors that also
    Figure 2: GPT-4-generated proof for lemma Factor0.                                 support verified calculations [25, 26] but none using LLMs.

                                                                                       5   CONCLUSION
we obtained was when we asked to prove one of the lemmas, but
                                                                                       The lemma inference experiment yielded promising results, demon-
gave a complete proof of one of the other similar lemmas.
                                                                                       strating GPT-4’s ability to infer lemmas with minor errors. However,
   To test whether GPT-4 would be able to help Dafny developers
                                                                                       throughout the experiments, several responses contained syntax
when they need to prove less domain-specific results, we also at-
                                                                                       errors that proved challenging to rectify through reprompting. The
tempted to infer proofs for statements that are more widely known.
                                                                                       program struggled to complete lemma proofs or correct minor
An example is shown in Figure 2, where a proof for the lemma
                                                                                       errors in lemma specifications.
Factor0 was generated by GPT-4. The lemma is a version of a
                                                                                          On the other hand, the proof inference experiment revealed that
basic property of number theory: 𝑝 is a factor of any linear com-
                                                                                       only through a meticulously crafted prompt with rich examples
bination 𝑝 ∗ 𝑎 + 𝑝 ∗ 𝑏. The predicate is a variation of the lemmas
                                                                                       could GPT-4 successfully complete the proofs. This underscores the
required to prove correctness of Euclid’s algorithm as implemented
                                                                                       need for improved LLMs that reduce the need for extensive manual
in Dafny’s integration tests.3
                                                                                       prompt curation.
   The best attempt by GPT-4 to prove the lemma is shown in blue
                                                                                          In order to achieve these improvements, our next steps will focus
in Figure 2. To achieve this, we designed a prompt incorporating ex-
                                                                                       on prompting engineering and fine-tuning models with well-crafted
tensive Dafny code and examples; in particular we provided all the
                                                                                       datasets containing relevant Dafny code, with a specific emphasis
contents of the integration test file for calculations.4 Even though
                                                                                       on lemma inference, proof inference, and suggestions that only
the hints are correct and make sense, they are not accepted by
                                                                                       contain correct syntax.
Dafny. Nevertheless, once we comment them, the proof is accepted.
                                                                                          In terms of dataset creation, we plan to contribute to and extend
Moreover, in the version of Dafny that we used, 4.3.0, we had to
                                                                                       CloverBench [36], the dataset used by Clover. At the time of writing,
change the variable definitions to:
                                                                                       CloverBench contains only 60 small CS textbook examples. Many
               var a :| x == p*a; var b :| y == p*b;                                   more, and more complex, examples will be required to ensure the
                                                                                       practicality of our ideas. Moreover, we plan to create additional and
4    RELATED WORK                                                                      specialized datasets for specific tasks; for example, we intend to
                                                                                       create a Dafny dataset akin to Reichel et al.’s dataset for Coq [30],
Clover [36] is the only work that we are aware of on using LLMs
                                                                                       to assist developers in proof repair.
in the context of Dafny. Clover consists on using a checker that
                                                                                          Finally, to increase the adoption of our ideas, we started their
performs consistency checks among code, docstrings, and formal
                                                                                       integration into Dafny’s VSCode plugin.
3 Permalink:                              https://github.com/dafny-lang/dafny/blob/
eae8fc97aabc13ea665b486060e831188628d42b/Source/IntegrationTests/TestFiles/
LitTests/LitTest/dafny4/gcd.dfy. See also: https://leino.science/papers/krml279.html
4 Permalink:                              https://github.com/dafny-lang/dafny/blob/
eae8fc97aabc13ea665b486060e831188628d42b/Source/IntegrationTests/TestFiles/
LitTests/LitTest/dafny2/Calculations.dfy
Leveraging Large Language Models to Boost Dafny’s Developers Productivity


REFERENCES                                                                                    [25] Alexandra Mendes, Roland Backhouse, and João F. Ferreira. 2014. Structure
 [1] Alexandre Abreu, Nuno Macedo, and Alexandra Mendes. 2023. Exploring Auto-                     editing of handwritten mathematics: Improving the computer support for the
     matic Specification Repair in Dafny Programs. In 2023 38th IEEE/ACM Interna-                  calculational method. In Proceedings of the Ninth ACM International Conference
     tional Conference on Automated Software Engineering Workshops (ASEW). 105–112.                on Interactive Tabletops and Surfaces. 139–148.
     https://doi.org/10.1109/ASEW60602.2023.00019                                             [26] Alexandra Mendes and João F. Ferreira. 2018. Towards Verified Handwritten
 [2] Open AI. 2023. GPT-4 Technical report. arXiv preprint arXiv:2303.08774 (2023).                Calculational Proofs: (Short Paper). In Interactive Theorem Proving: 9th Interna-
 [3] Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. The Tactician. In                   tional Conference, ITP 2018, Held as Part of the Federated Logic Conference, FloC
     Intelligent Computer Mathematics. 271–277.                                                    2018, Oxford, UK, July 9-12, 2018, Proceedings 9. Springer, 432–440.
 [4] Sébastien Bubeck, Varun Chandrasekaran, Ronen Eldan, Johannes Gehrke, Eric               [27] Maciej Mikuła, Szymon Antoniak, Szymon Tworkowski, Albert Qiaochu Jiang,
     Horvitz, Ece Kamar, Peter Lee, Yin Tat Lee, Yuanzhi Li, Scott Lundberg, et al.                Jin Peng Zhou, Christian Szegedy, Łukasz Kuciński, Piotr Miłoś, and Yuhuai Wu.
     2023. Sparks of artificial general intelligence: Early experiments with gpt-4.                2023. Magnushammer: A Transformer-based Approach to Premise Selection.
     arXiv preprint arXiv:2303.12712 (2023).                                                       arXiv:2303.04488
 [5] Franck Cassez. 2021. Verification of the incremental Merkle tree algorithm               [28] Nhan Nguyen and Sarah Nadi. 2022. An empirical evaluation of GitHub copilot’s
     with Dafny. In 24th International Symposium on Formal Methods (FM) (LNCS,                     code suggestions. In Proceedings of the 19th International Conference on Mining
     Vol. 13047). Springer, 445–462.                                                               Software Repositories. 1–5.
 [6] Franck Cassez, Joanne Fuller, Milad K Ghale, David J Pearce, and Horacio MA              [29] Julian Aron Prenner, Hlib Babii, and Romain Robbes. 2022. Can OpenAI’s Codex
     Quiles. 2023. Formal and Executable Semantics of the Ethereum Virtual Machine                 Fix Bugs? An Evaluation on QuixBugs. In Proceedings of the Third International
     in Dafny. In International Symposium on Formal Methods. Springer, 571–583.                    Workshop on Automated Program Repair (Pittsburgh, Pennsylvania) (APR ’22).
 [7] Franck Cassez, Joanne Fuller, and Horacio Mijail Antón Quiles. 2022. Deductive                Association for Computing Machinery, New York, NY, USA, 69–75. https:
     verification of smart contracts with Dafny. In International Conference on Formal             //doi.org/10.1145/3524459.3527351
     Methods for Industrial Critical Systems. Springer, 50–66.                                [30] Tom Reichel, R Henderson, Andrew Touchet, Andrew Gardner, and Talia Ringer.
 [8] Michael D Ernst, Jeff H Perkins, Philip J Guo, Stephen McCamant, Carlos Pacheco,              2023. Proof repair infrastructure for supervised models: Building a large proof
     Matthew S Tschantz, and Chen Xiao. 2007. The Daikon system for dynamic                        repair dataset. In 14th International Conference on Interactive Theorem Proving
     detection of likely invariants. Sci. Comput. Program. 69, 1-3 (2007), 35–45.                  (ITP 2023). Schloss-Dagstuhl-Leibniz Zentrum für Informatik.
 [9] Marie Farrell, Conor Reynolds, and Rosemary Monahan. 2021. Using dafny to                [31] Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner. 2020.
     solve the VerifyThis 2021 challenges. In Proceedings of the 23rd ACM International            Generating correctness proofs with neural networks. In Proceedings of the 4th
     Workshop on Formal Techniques for Java-like Programs. 32–38.                                  ACM SIGPLAN International Workshop on Machine Learning and Programming
[10] João F. Ferreira, Alexandra Mendes, Roland Backhouse, and Luís S Barbosa. 2009.               Languages. 1–10.
     Which mathematics for the information society?. In Teaching Formal Methods:              [32] Alex Sanchez-Stern, Emily First, Timothy Zhou, Zhanna Kaufman, Yuriy Brun,
     Second International Conference, TFM 2009, Eindhoven, The Netherlands, November               and Talia Ringer. 2023. Passport: Improving Automated Formal Verification
     2-6, 2009. Proceedings 2. Springer, 39–56.                                                    Using Identifiers. ACM TOPLAS 45, 2, Article 12 (June 2023), 12:1-12:30 pages.
[11] João F. Ferreira, Alexandra Mendes, Alcino Cunha, Carlos Baquero, and Paulo                   https://doi.org/10.1145/3593374
     Silva. 2011. Logic training through algorithmic problem solving. In Tools for            [33] John Sarracino, Tobias Kappé, Ryan Doenges, and Greg Morrisett. [n. d.].
     Teaching Logic: Third International Congress, TICTTL 2011, Salamanca, Spain,                  Metaprogramming for Practical and Extensible SMT-Powered Coq Proof Au-
     June 1-4, 2011. Proceedings. Springer, 62–69.                                                 tomation. ([n. d.]).
[12] João F. Ferreira and Alexandra Mendes. 2009. Students’ feedback on teaching              [34] William Schultz, Ian Dardik, and Stavros Tripakis. 2022. Plain and Simple
     mathematics through the calculational method. In 2009 39th IEEE Frontiers in                  Inductive Invariant Inference for Distributed Protocols in TLA+. In 2022 Formal
     Education Conference. IEEE, 1–6.                                                              Methods in Computer-Aided Design (FMCAD). IEEE, 273–283.
[13] Emily First and Yuriy Brun. 2022. Diversity-Driven Automated Formal Verifi-              [35] Aishwarya Sivaraman, Alex Sanchez-Stern, Bretton Chen, Sorin Lerner, and Todd
     cation. In ICSE (22–27). Pittsburgh, PA, USA, 749–761. https://doi.org/10.1145/               Millstein. 2022. Data-driven lemma synthesis for interactive proofs. Proceedings
     3510003.3510138                                                                               of the ACM on Programming Languages 6, OOPSLA2 (2022), 505–531.
[14] Emily First, Yuriy Brun, and Arjun Guha. 2020. TacTok: Semantics-Aware Proof             [36] Chuyue Sun, Ying Sheng, Oded Padon, and Clark Barrett. 2023. Clover: Closed-
     Synthesis. PACMPL OOPSLA 4 (November 2020), 231:1–231:31. https://doi.org/                    Loop Verifiable Code Generation. arXiv preprint arXiv:2310.17807 (2023).
     10.1145/3428299                                                                          [37] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan Chin. 2017.
[15] Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-                  Automated lemma synthesis in symbolic-heap separation logic. Proceedings of
     Proof Generation and Repair with Large Language Models. In Proceedings of the                 the ACM on Programming Languages 2, POPL (2017), 1–29.
     31st ACM Joint European Software Engineering Conference and Symposium on                 [38] Amitayush Thakur, Yeming Wen, and Swarat Chaudhuri. 2023. A Language-
     the Foundations of Software Engineering (, San Francisco, CA, USA,) (ESEC/FSE                 Agent Approach to Formal Theorem-Proving. arXiv:2310.04353
     2023). Association for Computing Machinery, New York, NY, USA, 1229–1241.                [39] Ruyun Wang, Hanwen Zhang, Guoliang Lu, Lei Lyu, and Chen Lyu. 2020. Fret:
     https://doi.org/10.1145/3611643.3616243                                                       Functional Reinforced Transformer With BERT for Code Summarization. IEEE
[16] Shuzheng Gao, Cuiyun Gao, Yulan He, Jichuan Zeng, Lunyiu Nie, Xin Xia, and                    Access 8 (2020), 135591–135604. https://doi.org/10.1109/ACCESS.2020.3011744
     Michael Lyu. 2023. Code Structure–Guided Transformer for Source Code Sum-                [40] Chunqiu Steven Xia, Yuxiang Wei, and Lingming Zhang. 2023. Automated
     marization. ACM Trans. Softw. Eng. Methodol. 32, 1, Article 23 (feb 2023), 32 pages.          Program Repair in the Era of Large Pre-Trained Language Models. In Proceedings
     https://doi.org/10.1145/3522674                                                               of the 45th International Conference on Software Engineering (Melbourne, Victoria,
[17] Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever. 2019. GamePad:                Australia) (ICSE ’23). IEEE Press, 1482–1494. https://doi.org/10.1109/ICSE48619.
     A Learning Environment for Theorem Proving. In ICLR. https://openreview.net/                  2023.00129
     forum?id=r1xwKoR9Y7                                                                      [41] Chunqiu Steven Xia and Lingming Zhang. 2022. Less Training, More Repairing
[18] Albert Jiang, Konrad Czechowski, Mateja Jamnik, Piotr Milos, Szymon                           Please: Revisiting Automated Program Repair via Zero-Shot Learning. In Pro-
     Tworkowski, Wenda Li, and Yuhuai Tony Wu. 2022. Thor: Wielding Hammers                        ceedings of the 30th ACM Joint European Software Engineering Conference and
     to Integrate Language Models and Automated Theorem Provers. In NeurIPS.                       Symposium on the Foundations of Software Engineering (, Singapore, Singapore,)
[19] Matthew Jin, Syed Shahriar, Michele Tufano, Xin Shi, Shuai Lu, Neel Sundaresan,               (ESEC/FSE 2022). Association for Computing Machinery, New York, NY, USA,
     and Alexey Svyatkovskiy. 2023. Inferfix: End-to-end program repair with llms.                 959–971. https://doi.org/10.1145/3540250.3549101
     arXiv preprint arXiv:2303.07263 (2023).                                                  [42] Xin Xia, Lingfeng Bao, David Lo, Zhenchang Xing, Ahmed E. Hassan, and Shan-
[20] Junaed Younus Khan and Gias Uddin. 2023. Automatic Code Documentation                         ping Li. 2018. Measuring Program Comprehension: A Large-Scale Field Study
     Generation Using GPT-3. In Proceedings of the 37th IEEE/ACM International                     with Professionals. IEEE Transactions on Software Engineering 44, 10 (2018),
     Conference on Automated Software Engineering (Rochester, MI, USA) (ASE ’22).                  951–976. https://doi.org/10.1109/TSE.2017.2734091
     Association for Computing Machinery, New York, NY, USA, Article 174, 6 pages.            [43] Kaiyu Yang and Jia Deng. 2019. Learning to prove theorems via interacting with
     https://doi.org/10.1145/3551349.3559548                                                       proof assistants. In ICML. 6984–6994.
[21] K Rustan M Leino. 2010. Dafny: An automatic program verifier for functional cor-         [44] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu,
     rectness. In International conference on logic for programming artificial intelligence        Saad Godil, Ryan Prenger, and Anima Anandkumar. 2023. LeanDojo: Theorem
     and reasoning. Springer, 348–370.                                                             Proving with Retrieval-Augmented Language Models. In Neural Information
[22] K Rustan M Leino. 2023. Program Proofs. MIT Press.                                            Processing Systems (NeurIPS).
[23] K Rustan M Leino and Nadia Polikarpova. 2013. Verified calculations. In Working          [45] Weikun Yang, Grigory Fedyukovich, and Aarti Gupta. 2019. Lemma synthesis
     Conference on Verified Software: Theories, Tools, and Experiments. Springer, 170–             for automating induction over algebraic data types. In Principles and Practice of
     190.                                                                                          Constraint Programming: 25th International Conference, CP 2019, Stamford, CT,
[24] Nancy Leveson. 2020. Are you sure your software will not kill anyone? Commun.                 USA, September 30–October 4, 2019, Proceedings 25. Springer, 600–617.
     ACM 63, 2 (2020), 25–28.
