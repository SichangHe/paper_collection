                                          ROOSTERIZE: Suggesting Lemma Names for Coq
                                            Verification Projects Using Deep Learning
                                                                    Pengyu Nie∗ , Karl Palmskog† , Junyi Jessy Li∗ , Milos Gligoric∗
                                                              pynie@utexas.edu, palmskog@kth.se, jessy@austin.utexas.edu, gligoric@utexas.edu
                                           ∗ The University of Texas at Austin, Austin, TX, USA      † KTH Royal Institute of Technology, Stockholm, Sweden



                                           Abstract—Naming conventions are an important concern in             by rule-based tools, specification of rules is tedious and often
                                        large verification projects using proof assistants, such as Coq.       incomplete. Moreover, most large Coq projects use mutually
                                        In particular, lemma names are used by proof engineers to              incompatible lemma naming schemes.
arXiv:2103.01346v2 [cs.PL] 3 May 2021




                                        effectively understand and modify Coq code. However, providing
                                        accurate and informative lemma names is a complex task,                   We present ROOSTERIZE, a toolchain which automatically
                                        which is currently often carried out manually. Even when               suggests Coq lemma names. ROOSTERIZE learns naming
                                        lemma naming is automated using rule-based tools, generated            conventions by leveraging neural networks trained on existing
                                        names may fail to adhere to important conventions not specified        Coq code. The deep learning and suggestion processes use
                                        explicitly. We demonstrate a toolchain, dubbed ROOSTERIZE,             multiple representations of lemma statements, including syntax
                                        which automatically suggests lemma names in Coq projects.
                                        ROOSTERIZE leverages a neural network model trained on                 trees and Coq kernel trees (also called elaborated terms) [7].
                                        existing Coq code, thus avoiding manual specification of naming        In essence, ROOSTERIZE consists of (1) a set of components
                                        conventions. To allow proof engineers to conveniently access           written in OCaml that interact with Coq or directly process
                                        suggestions from ROOSTERIZE during Coq project development,            information extracted from Coq, and (2) a set of components
                                        we integrated the toolchain into the popular Visual Studio Code        written in Python that perform name learning and generation.
                                        editor. Our evaluation shows that ROOSTERIZE substantially
                                        outperforms strong baselines for suggesting lemma names and            The first set of components is based on the SerAPI library [8]
                                        is useful in practice. The demo video for ROOSTERIZE can be            for serialization of Coq data, while the second set of compo-
                                        viewed at: https://youtu.be/HZ5ac7Q14rc.                               nents is based on the PyTorch deep learning framework [9]
                                           Index Terms—Coq, lemma names, neural networks                       and the OpenNMT library [10].
                                                                                                                  The core of ROOSTERIZE is command-line based. Although
                                                              I. I NTRODUCTION                                 valuable, this does not provide a convenient interface for proof
                                           In large software projects with many contributors, names            engineers as they are stating and proving new Coq lemmas.
                                        of methods and classes are important for code comprehen-               Hence, we integrated the toolchain into Visual Studio Code
                                        sion and modification. Open source projects often document             (VSCode) [11], a popular editor for Coq source code.
                                        their naming conventions carefully, impose them on proposed               We evaluated an earlier version of ROOSTERIZE using a
                                        contributions, and willingly accept naming fixes [1].                  corpus derived from the MathComp family of Coq projects,
                                           The Coq proof assistant [2] is increasingly used to de-             finding that the toolchain significantly outperforms strong
                                        velop trustworthy software systems, e.g., compilers [3] and            baselines on automatic metrics [7]. Moreover, we found
                                        distributed systems [4]. As such verification projects grow            encouraging results in a qualitative case study where the
                                        in scope and size, naming conventions become an important              maintainer of a medium-sized Coq project manually evaluated
                                        concern. In particular, proof engineers use lemma names to             over 150 name suggestions generated by ROOSTERIZE.
                                        effectively understand and modify code [5].                               The earlier toolchain version provided few conveniences
                                           In contrast to method names in Java-like languages, which           beyond basic name suggestions via the command line, and
                                        tend to use camel case and regular English words (e.g.,                did not include any editor integration. In addition to the novel
                                        openServerConnection), Coq lemma names often mix                       integration with VSCode, the toolchain version presented here
                                        camel case and underscores with heavily abbreviated termi-             provides a significantly more automated installation process
                                        nology from logic and advanced mathematics, which makes                and supports system-level configuration of Coq project and
                                        the naming task more difficult. For example, in the Math-              name suggestion parameters, making it suitable for wider use
                                        ematical Components (MathComp) Coq library, the lemma                  by proof engineers.
                                        name extprod_mulgA is used to express “associativity of                   Our code, documentation, and pre-trained models are pub-
                                        multiplication operations in external product groups”, i.e., a         licly available on GitHub:
                                        property of abstract algebra. This meaning is obtained by first        https://github.com/EngineeringSoftware/roosterize.
                                        decomposing the name into extprod, mul, g, and A, and
                                        then consulting the MathComp naming conventions [6].                             II. T ECHNIQUE AND I MPLEMENTATION
                                           Currently, documentation and enforcement of lemma nam-                 In this section, we explain the workflow of the ROOSTERIZE
                                        ing conventions in Coq projects is largely a manual process.           toolchain, and then briefly describe our neural network model
                                        While some aspects of naming conventions can be captured               for lemma name generation.



                                                                                                           1
      3                                                                                  learn a deep semantic representation of a given lemma
      SubTok                  Coq source/compiled files
                                                                                         statement from its tokens, syntax tree, and kernel tree. The
      4                                                                                  model can be configured to use any combination of the three
    MISeq2Seq                      1
                                  ser{comp,tok,name}
                                                                                         encoders. The decoder is another RNN that generates the
                                                             SerAPI        Coq
      PyTorch                                                                            descriptive lemma name based on the input deep semantic
                                                                                         representation. We equipped the decoder RNN with attention
                            lemma names
     2                                                                                   mechanism [14] and copy mechanism [15] to improve the
    DataMiner
                                                                                         generation accuracy.
                        syntax and terms                                                    All the inputs and the output are sequences of sub-tokens;
                                                                                         the sub-tokens of inputs are obtained using a sub-tokenizer,
           Fig. 1: Low-level workflow of ROOSTERIZE.                                     and the sub-tokens of the output are concatenated to form the
                                                                                         generated lemma name. We implemented the sub-tokenizer
      lemma statement
                              ···                                                        based on the conventions outlined by MathComp develop-
                                                           lemma name
       L     1    L     2            .
                                                                                         ers [6] (e.g., the lemma name extprod mulgA should be sub-
                                                   mg        eq       nerode hEOSi
      chopped syntax tree                                                                tokenized to extprod, , mul, g, and A). Because syntax and
                              ···
                                                                                         kernel trees can be large, we implemented chopping heuristics
       (     (    ( CLocalAssum      )             hBOSi
      chopped kernel tree
                                            fully
                                          connected
                                                                                         to remove the parts irrelevant for generating lemma names
                              ···           layer          DECODER                       before feeding them to the encoders. Our heuristics essentially:
       (    Prod char   (            )                                                   (1) replace the fully qualified name sub-trees with only the
             ENCODERS                                                                    last component of the name; (2) remove the line number
Fig. 2: Neural architecture of lemma name generation model                               information from sub-trees; (3) extract the singletons, i.e., non-
in ROOSTERIZE, exemplified for the name mg_eq_nerode.                                    leaf nodes that have only one child.

                                                                                                           III. T OOL I NSTALLATION
A. Toolchain Workflow
                                                                                            ROOSTERIZE currently supports macOS and Linux-based
   Fig. 1 illustrates the low-level workflow of the ROOS -                               operating systems. The first installation step is to download
TERIZE toolchain. (1) We use the SerAPI library [8] for
                                                                                         the ROOSTERIZE repository:
extracting data from Coq files, using three programs: sertok
                                                                                         $ git clone \
for extracting tokens, sercomp for extracting the syntax                                    https://github.com/EngineeringSoftware/roosterize
trees, and sername for extracting kernel trees. Syntax trees                             $ cd roosterize && git checkout v1.1.0+8.10.2
are Coq’s internal representations of source code elements,
including lemmas, during the parsing phase. Kernel trees                                 Required software and libraries. ROOSTERIZE depends on
are Coq’s internal representations of statements and func-                               two sets of software and libraries: (1) OCaml, Coq, and
tions during proof checking, and contain rich information                                SerAPI; (2) PyTorch and other Python libraries.
relevant for lemma naming. (2) DataMiner orchestrates                                      To install OCaml (4.07.1), Coq (8.10.2) and SerAPI (0.7.1),
these programs to obtain all lemmas in the given Coq files                               we recommend using the OCaml-based package-management
and their names, lemma statements, and syntax and kernel                                 system OPAM [16] version 2.0.7 or later:
trees. (3) SubTok sub-tokenizes the inputs for the neural                                $ opam switch create roosterize 4.07.1
network model. (4) MISeq2Seq is the multi-input neural                                   $ opam switch roosterize && eval $(opam env)
                                                                                         $ opam update
network model for lemma name generation (Section II-B). The                              $ opam pin add coq 8.10.2
model is implemented in the popular deep learning framework                              $ opam pin add coq-serapi 8.10.0+0.7.1
PyTorch [9], and is based on the OpenNMT library [10].                                      To install PyTorch and other Python libraries, we recom-
   Users interact with ROOSTERIZE by using its command-                                  mend using the package-management system Conda [17]. The
line interface or the VSCode extension. We use the Language                              installation script may be different depending on the operating
Server Protocol (LSP) [12] to connect the server (the core                               system and whether to use GPU or not. For example, on Linux,
of ROOSTERIZE including data extraction scripts and the                                  to use CPU only:
lemma name generation model) with the client (the VSCode
                                                                                         $ conda env create --name roosterize \
extension). This simplifies future integration with other editors                                           --file conda-envs/cpu.yml
that also support LSP, e.g., Emacs.                                                      $ conda activate roosterize

B. Neural Network Model for Generating Lemma Names                                         After installing these required software and libraries, users
   We consider lemma name generation with an encoder-                                    can use ROOSTERIZE via its command-line interface.
decoder mindset, and use sequence-to-sequence (SEQ 2 SEQ)                                VSCode extension. The ROOSTERIZE VSCode extension can
neural architectures specifically designed for transduction                              be installed easily from VSCode marketplace: launch “VS
tasks [13]. Fig. 2 illustrates the architecture of our model [7].                        Code Quick Open” (Ctrl+P), paste the following command:
The encoders are Recurrent Neural Networks (RNNs) that ext install EngineeringSoftware.roosterize-vscode



                                                                                     2
                                                                      compile the project before suggesting lemma names. ROOST-
                                                                      ERIZE can suggest lemma names for one Coq file at a time.
                                                                      For example, running the following commands downloads the
                                                                      Coq project FCSL PCM at Git revision eef4503, prepares a
                                                                      .roosterizerc configuration file, and suggests lemma names
                                                                      for the finmap.v file in the project:
                                                                      $ git clone \
                                                                         https://github.com/imdea-software/fcsl-pcm
Fig. 3: Screenshot of using ROOSTERIZE from command line.             $ git checkout eef4503
                                                                      $ echo "compile_cmd: make -j8" > ./.roosterizerc
                                                                      $ roosterize suggest_naming \
                                                                                   --file=$PWD/finmap/finmap.v

                                                                         In the last command, ROOSTERIZE uses SerAPI to parse
                                                                      finmap.v and extracts all lemmas, then uses the lemma names
                                                                      suggestion model to generate top k (default k = 5) likely
                                                                      lemma names for each lemma, and then compares the gener-
                                                                      ated lemma names with the original lemma names, and finally
                                                                      prints a report to suggest potential lemma names changes.
                                                                      Fig. 3 shows the top part of the report generated for finmap.v
                                                                      (full report available at: https://tinyurl.com/yy6l8fbq).
                                                                      B. VSCode
                                                                         Users should first open the Coq files they want to analyze.
                                                                      The steps to obtain the lemma names suggestions for them are:
                                                                      (1) open “Command Palettes” (Ctrl+Shift+P), and (2) choose
                                                                      “Roosterize: Suggest Naming (for all .v files)”. After ROOS -
                                                                      TERIZE produces the suggestions, the lemma names that do
  Fig. 4: Screenshot of using ROOSTERIZE from VSCode.                 not conform to the conventions are underlined, and users can
                                                                      hover the mouse pointer over that underlined name to view
  Then, users should configure the path to ROOSTERIZE ex-             ROOSTERIZE’s suggestion in a tooltip. Users can also view all
ecutable file (./bin/roosterize) using the following steps:           suggestions in the “Problems” tab. Fig. 4 shows a screenshot
open “Settings” (Ctrl+,), search for the entry “ROOSTERIZE:           of this step.
Bin Path”, and fill in the path to ROOSTERIZE executable file.                                V. E VALUATION
                      IV. T OOL U SAGE                                A. Quantitative

   In this section, we describe the way our tool can be invoked       Coq projects under study. We selected four large Coq
from command line and from VSCode.                                    projects from the MathComp family: math-comp, finmap,
                                                                      fourcolor, and odd-order. The projects have a total of 164k
A. Command Line                                                       lines of code, 187 files, and 11,266 lemmas. More information
                                                                      of these projects can be found in our corpus [19] (“Tier 1”
  After installation, users can launch ROOSTERIZE via the
                                                                      part). Following standard deep learning practice, we randomly
executable file ./bin/roosterize (in short, roosterize).
                                                                      split the projects’ files into training, validation, and testing sets
We focus on the main usage of ROOSTERIZE—suggesting
                                                                      which contain 80%, 10%, 10% of the files, which is 8,861,
lemma names for Coq projects. For other usages, e.g., training
                                                                      1,085, 1,320 lemmas, respectively; the lemmas from a same
models, users can refer to the help included in ROOSTERIZE:
                                                                      file are assigned to only one of the sets.
$ roosterize --help
                                                                      Results. We trained various configurations of our model. In
  Users should first obtain a model, e.g., by downloading             this paper, we focus on five configurations that use different in-
a pre-trained model. The following command downloads the              puts: Stmt+ChopKnlTree+ChopSynTree, Stmt+ChopKnlTree,
model we pre-trained on our MathComp corpus [7]:                      Stmt+ChopSynTree, ChopKnlTree+ChopSynTree, and only
                                                                      Stmt (where Stmt = lemma statement, ChopSynTree =
$ roosterize download_global_model
                                                                      chopped syntax tree, ChopKnlTree = chopped kernel tree).
   Applying ROOSTERIZE to a Coq project requires (1) a                We also compare our model with a retrieval-based baseline.
  CoqProject file in the project root directory in the format            We evaluate each model by applying it on the testing set and
used by the coq makefile tool [18], and (2) that the project          measure the average similarity between the generated names
source code has been compiled. If a user specified the compila-       and the expected names (as written by developers), using four
tion command in the .roosterizerc configuration file at the           automatic metrics: BLEU [20], fragment accuracy [7], top-1
root directory of the project, ROOSTERIZE will automatically          accuracy, and top-5 accuracy.



                                                                  3
          TABLE I: Results of ROOSTERIZE Models.                        suggests names that appear in the training data. ROOSTERIZE
                                                                        uses novel neural network models pre-trained on existing Coq
  Model                          BLEU    Frag.Acc.   Top1    Top5
                                                                        code to generate lemma names. Our quantitative evaluation
  Stmt+ChopKnlTree+ChopSynTree    45.4      22.2%    7.5%   16.5%
  Stmt+ChopKnlTree                47.2      24.9%    9.6%   18.0%
                                                                        showed that ROOSTERIZE outperforms several strong base-
  Stmt+ChopSynTree                37.7      18.1%    6.1%   10.6%       lines, and our qualitative evaluation demonstrated the quality
  ChopKnlTree+ChopSynTree         45.4      22.9%    7.6%   15.3%
  Stmt                            38.9      19.4%    6.9%   11.6%
                                                                        of generated lemma names. We believe ROOSTERIZE can be
  Retrieval-based                 28.3      10.0%    0.2%    0.3%
                                                                        especially useful to proof engineers in large Coq projects
                                                                        to ensure that lemma names follow prevailing conventions.
                                                                        Through our integration of ROOSTERIZE with the VSCode
                                                                        editor, naming suggestions can be continually provided as Coq
   Table I shows the results. We observed that Stmt                     code is added and revised.
+ChopKnlTree achieved the best performance and substan-
tially outperforms the retrieval-based baseline. This shows                                      ACKNOWLEDGMENTS
the importance of using Coq’s internal structures. Lemma                  We thank Cyril Cohen, Emilio Jesús Gallego Arias, Anton
statement and syntax tree do not work well together primarily           Trunov, and the anonymous reviewers for their comments
because the two representations contain mostly the same in-             and feedback. This work was partially supported by the US
formation. We performed extensive ablation studies to confirm           National Science Foundation under Grant No. CCF-1652517
the effectiveness of the other parts of the model (Section 6.2          and the University of Texas at Austin Continuing Fellowship.
of our IJCAR’20 paper [7]), including the chopping heuristics
and the attention and copy mechanisms. We also performed                                              R EFERENCES
a generalization study which confirms that ROOSTERIZE can                [1] M. Allamanis, E. T. Barr, C. Bird, and C. Sutton, “Learning natural
perform well on a new project with little additional training                coding conventions,” in FSE, 2014.
                                                                         [2] Coq Development Team, “The Coq proof assistant, version 8.10.0,”
(Appendix D.3 of our IJCAR’20 paper [7]).                                    Oct. 2019. [Online]. Available: https://zenodo.org/record/3476303
                                                                         [3] X. Leroy, “Formal verification of a realistic compiler,” Commun. ACM,
B. Qualitative                                                               vol. 52, no. 7, 2009.
                                                                         [4] I. Sergey, J. R. Wilcox, and Z. Tatlock, “Programming and proving with
   We carried out a qualitative case study using ROOSTERIZE                  distributed protocols,” PACMPL, vol. 2, no. POPL, 2018.
by applying it to the FCSL PCM Coq project, which comprises              [5] D. Aspinall and C. Kaliszyk, “What’s in a theorem name?” in ITP, 2016.
690 lemmas. 36 suggestions (5%) exactly matched the exist-               [6] C. Cohen and A. Trunov, “Contribution guide for the Mathematical
                                                                             Components library,” 2018, last accessed 2020-11-20. [Online].
ing lemma names. We then asked the project maintainer to                     Available: https://github.com/math-comp/math-comp/blob/mathcomp-1.
comment on the remaining suggestions. The maintainer found                   9.0/CONTRIBUTING.md
that 20% of the suggested names he inspected were of good                [7] P. Nie, K. Palmskog, J. J. Li, and M. Gligoric, “Deep generation of Coq
                                                                             lemma names using elaborated terms,” in IJCAR, 2020.
quality, out of which more than half were of high quality.               [8] E. J. Gallego Arias, “SerAPI: Machine-friendly, data-centric seri-
Considering that the analysis was of top-1 suggestions, we                   alization for Coq,” MINES ParisTech, Tech. Rep., 2016, https://
find these results encouraging.                                              hal-mines-paristech.archives-ouvertes.fr/hal-01384408.
                                                                         [9] A. Paszke, S. Gross, S. Chintala, G. Chanan, E. Yang, Z. DeVito,
             VI. L IMITATIONS AND F UTURE W ORK                              Z. Lin, A. Desmaison, L. Antiga, and A. Lerer, “Automatic
                                                                             differentiation in PyTorch,” in Autodiff Workshop, 2017. [Online].
   Due to limitations in the protocol that VSCode uses to                    Available: https://openreview.net/forum?id=BJJsrmfCZ
communicate with Coq, our VSCode extension cannot obtain                [10] G. Klein, Y. Kim, Y. Deng, J. Senellart, and A. M. Rush, “OpenNMT:
                                                                             Open-source toolkit for neural machine translation,” in ACL Demo, 2017.
name suggestions for a lemma in real time as it is being edited,        [11] Microsoft, “Visual Studio Code Website,” 2020, last accessed 2020-11-
i.e., by monitoring changes to the Coq source file and proof                 20. [Online]. Available: https://code.visualstudio.com
state. However, our toolchain can support this mode of use              [12] Microsoft, “Language Server Protocol Website,” 2020, last
                                                                             accessed 2020-11-19. [Online]. Available: https://microsoft.github.
once protocol limitations are lifted.                                        io/language-server-protocol/
   The quality of lemma name suggestions is highly dependent            [13] I. Sutskever, O. Vinyals, and Q. V. Le, “Sequence to sequence learning
on the quality of the pre-trained neural networks, and building              with neural networks,” in NeurIPS, 2014.
                                                                        [14] T. Luong, H. Pham, and C. D. Manning, “Effective approaches to
a model requires careful curation of Coq training data. While                attention-based neural machine translation,” in EMNLP, 2015.
we have constructed such a high-quality dataset based on the            [15] A. See, P. J. Liu, and C. D. Manning, “Get to the point: Summarization
MathComp family of projects, additional datasets must be                     with pointer-generator networks,” in ACL, 2017.
                                                                        [16] OPAM Development Team, “OCaml Package Manager,” 2020, last
curated to suggest names that follow conventions other than                  accessed 2020-11-19. [Online]. Available: https://opam.ocaml.org
those for MathComp.                                                     [17] Anaconda, Inc., “Miniconda - Conda documentation,” 2020, last
                                                                             accessed 2020-11-19. [Online]. Available: https://docs.conda.io/en/
                       VII. C ONCLUSION                                      latest/miniconda.html
                                                                        [18] Coq Development Team, “Building a Coq project,” 2019, last
   We presented ROOSTERIZE, a toolchain for suggesting                       accessed 2020-11-20. [Online]. Available: https://coq.inria.fr/distrib/V8.
lemma names in Coq verification projects. Nearly all related                 10.2/refman/practical-tools/utilities.html
work addresses fundamentally different name generation tasks            [19] P. Nie, K. Palmskog, J. J. Li, and M. Gligoric, “MathComp Corpus
                                                                             of Coq Code,” 2020, last accessed 2020-11-20. [Online]. Available:
in conventional languages such as Java [1]. An exception is                  https://github.com/EngineeringSoftware/math-comp-corpus
Aspinall and Kaliszyk [5], who learn naming from a corpus for           [20] K. Papineni, S. Roukos, T. Ward, and W. Zhu, “BLEU: A method for
the HOL Light proof assistant; however, their technique only                 automatic evaluation of machine translation,” in ACL, 2002.




                                                                    4
