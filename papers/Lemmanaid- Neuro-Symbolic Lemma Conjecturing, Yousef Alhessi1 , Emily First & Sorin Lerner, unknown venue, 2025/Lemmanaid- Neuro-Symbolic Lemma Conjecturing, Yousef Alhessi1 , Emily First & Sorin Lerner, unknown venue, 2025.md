                                                         Lemmanaid: Neuro-Symbolic Lemma Conjecturing
                                                                     Yousef Alhessi1 , Emily First & Sorin Lerner
                                                                    Department of Computer Science and Engineering
                                                                       University of California, San Diego, USA
                                                                   {yalhessi,emfirst, lerner}@ucsd.edu

                                         Sólrún Halla Einarsdóttir1 , George Granberry, Moa Johansson & Nicholas Smallbone
                                                             Department of Computer Science and Engineering
                                                       Chalmers University of Technology & University of Gothenburg
                                                          Abstract           Gothenburg, Sweden
                                                    {slrn,georgegr,moa.johansson,nicsma}@chalmers.se
                                                                             1
                                                                               Joint first authorship
                                            Mathematicians and computer scientists are in-
arXiv:2504.04942v6 [cs.AI] 2 Jun 2026




                                                                                                                 Formalization                       Lemmanaid
                                            creasingly leveraging proof assistants to for-
                                                                                                                       theory x       Functions,   Neural Engine
                                            malize and check complex proofs, a task that                                               context
                                                                                                                       datatype a
                                            demands substantial expertise. Can we lower
                                                                                                                       function f
                                            the bar by automating the conjecturing of help-                            function g                           Templates
                                            ful, interesting and novel lemmas? We present                              lemma l1                    Symbolic Engine
                                            the first neuro-symbolic lemma conjecturing                                lemma l2


                                            tool, L EMMANAID, designed to discover con-
                                                                                                                                    Conjectures
                                            jectures by drawing analogies between math-
                                            ematical theories. L EMMANAID uses a fine-
                                                                                                            Figure 1: High-level overview of L EMMANAID.
                                            tuned LLM to generate lemma templates that
                                            describe the shape of a lemma, and symbolic                  Tao, 2023). However, formalizing mathematics in a
                                            methods to fill in the details. We compare L EM -            proof assistant is a non-trivial task. This in turn has
                                            MANAID against the same LLM fine-tuned to                    sparked research in areas where large language models
                                            generate lemmas directly, as well as a fully                 might be of assistance, primarily in autoformalization
                                            symbolic conjecturing method. On test sets                   (Wang et al., 2018; Szegedy, 2020; Wu et al., 2022) and
                                            from Isabelle’s HOL library and Archive of For-              formal proof synthesis (Polu and Sutskever, 2020; Jiang
                                            mal Proofs (AFP), L EMMANAID consistently                    et al., 2022, 2023; First et al., 2023). In these settings,
                                            outperforms both neural and symbolic meth-                   the LLM and proof assistant complement each other:
                                            ods. Using DeepSeek-coder-6.7B as a backend,                 LLMs can provide a more flexible and powerful proof
                                            L EMMANAID discovers 50% (HOL) and 29%                       search while hallucinations in proofs are caught by the
                                            (AFP) of the gold standard lemmas, increas-                  proof assistant and easily discarded.
                                            ing to 55% and 35% when ensembling prompt-                      We address a different challenge, conjecturing: learn-
                                            ing strategies. In a case study on Octonions,                ing to construct new, interesting, and useful lemmas.
                                            L EMMANAID discovers 79% of the gold stan-                   This is an important and long standing challenge in AI
                                            dard lemmas, compared to 62% for neural-only                 for mathematical reasoning (Lenat, 1976; Fajtlowicz,
                                            and 23% for the state of the art symbolic tool.              1988; Ireland and Bundy, 1996; Colton, 2002), yet it
                                            Furthermore, in a targeted comparison, L EM -                remains an underexplored area (Yang et al., 2025). Auto-
                                            MANAID discovers more gold standard lem-
                                                                                                         matically discovered lemmas can both aid a human user
                                            mas than both Claude Opus 4.5 and GPT-5.2.                   working on a mathematical formalization and strengthen
                                            Our results show that L EMMANAID can conjec-                 automated theorem provers. General conjecturing must
                                            ture a significant number of interesting lemmas              work across a broad range of theories, spanning com-
                                            across complex formalizations in mathematics                 puter science, logic and mathematics. However, stan-
                                            and computer science.                                        dard benchmarks for formal mathematical reasoning
                                                                                                         have been derived from high school and undergradu-
                                        1   Introduction
                                                                                                         ate level mathematics competitions and standard text-
                                        Proof assistants like Lean (de Moura et al., 2015) and Is-       books, like miniF2F (Zheng et al., 2022), PutnamBench
                                        abelle (Nipkow et al., 2002) are becoming increasingly           (Tsoukalas et al., 2024) and ProofNet (Azerbayev et al.,
                                        important among research mathematicians who want                 2023). We move beyond these limited domains by lever-
                                        intricate proofs verified for guaranteed correctness. Fol-       aging real formalizations by researchers in both mathe-
                                        lowing the formalization of Kepler’s conjecture (Hales           matics and computer science.
                                        et al., 2017), there have been several projects formal-             In this work we introduce L EMMANAID: a novel
                                        izing recent results in research mathematics (Scholtze,          neuro-symbolic approach and tool for general lemma
                                        2020; Commelin and Topaz, 2024; Gowers et al., 2023;             conjecturing across a broad range of mathematical the-


                                                                                                     1
ories. L EMMANAID combines LLMs’ generalization                      HOL library1 and its Archive of Formal Proofs (AFP)2 .
capabilities with symbolic tools to generate lemmas by
a process of analogy. The LLM suggests generic tem-                  Contributions We show that the L EMMANAID ap-
plates describing learned families of analogous lemmas,              proach compares favorably to the results achievable
which are then instantiated to concrete theorems sym-                using purely neural or purely symbolic conjecturing.
bolically (Figure 1). Previous work has shown that such              The main contributions of our work are:
families of analogous lemmas indeed occur in proof                       • L EMMANAID, the first neuro-symbolic lemma con-
assistant libraries (Einarsdóttir et al., 2022; Heras et al.,             jecturing approach that uses an LLM to suggest
2013).                                                                     templates and a symbolic engine to instantiate tem-
   Existing conjecturing approaches rely on either a neu-                  plates as candidate lemmas.
ral or a symbolic engine. Neural methods may gener-
ate lemmas that are repetitive, redundant or trivial, or                 • A broad evaluation of L EMMANAID on the Isabelle
hallucinate symbols that are undefined in the formal-                      proof assistant’s HOL and AFP libraries. This goes
ization (Urban and Jakubův, 2020; Rabe et al., 2021;                      beyond evaluations of prior tools that have focused
Johansson and Smallbone, 2023). Scaling the model is                       on specific mathematical domains.
a commonly attempted remedy, albeit computationally
expensive and most effective in domains where back-                      • A comparison to an existing symbolic method,
ground libraries have already been formalized, such as                     QuickSpec, and to neural LLM-based lemma con-
the theories needed for math olympiad problems (Zheng                      jecturing models we create, showing that L EM -
et al., 2022). Symbolic methods, on the other hand, can                    MANAID outperforms these methods and is com-
be designed and programmed to avoid repetition and                         plementary.
redundancy. Prior symbolic tools (Smallbone et al.,
                                                                         • A comparison to instruction-tuned commercial
2017; Einarsdóttir et al., 2021; Singher and Itzhaky,
                                                                           LLMs on very recent entries in the AFP, show-
2021) have been used to successfully discover lemmas
                                                                           ing that L EMMANAID outperforms these models
needed in automated (co-)inductive provers (Johansson
                                                                           with smaller local models and token usage.
et al., 2014; Einarsdóttir et al., 2018, 2024; Kurashige
et al., 2024) over (co-)recursive datatypes. However,                2    Related Work
symbolic tools are limited in the shape, size and domain
of lemmas they can generate, and scale poorly to large               Proof Assistants and Autoformalization Proof As-
inputs sets. L EMMANAID addresses these shortcom-                    sistants (Nipkow et al., 2002; de Moura et al., 2015) can
ings in its novel neuro-symbolic lemma conjecturing                  check proofs in mathematics and computer science for
approach. The LLM suggests appropriate analogous                     correctness. A user must formalize their theory by trans-
lemma-patterns likely to be relevant for the theory at               lating it into the format language of the proof assistant
hand. The symbolic engine ensures correctness and nov-               and then interact with the system to construct a proof
elty, while keeping the search space manageable. In this             with calls to tactics, each executing and checking a part
way, we leverage the best of both neural and symbolic                of the proof. Tools like Sledgehammer (Blanchette et al.,
methods. As far as we are aware, this is the first work              2011) can automate many simpler proofs.
focusing on neuro-symbolic lemma conjecturing.                          Formalization remains difficult, driving research in
   L EMMANAID is a bottom-up conjecturing tool. Auto-                autoformalization: translating definitions, theorems and
mated conjecturing broadly follows two main method-                  lemmas written in natural language to the formal lan-
ologies (Johansson, 2019): top-down and bottom-up.                   guage of a proof assistant (Wang et al., 2018; Szegedy,
Top-down methods find relevant lemmas for a spe-                     2020; Wu et al., 2022). Autoformalization on realistic
cific proof attempt (Ireland and Bundy, 1996; Heras                  definitions is still a challenge for LLMs (Zhang et al.,
et al., 2013), with recent work in test-time reinforce-              2025). L EMMANAID serves as an excellent comple-
ment learning producing custom curricula to train spe-               ment: autoformalized definitions can be passed to L EM -
cialized neural provers (Dong and Ma, 2025; Hubert                   MANAID to generate a richer initial formalization.
et al., 2025; Chen et al., 2025). Success is measured
by increased proof success rate (of original proofs). In             Proof Synthesis Even with definitions and statements
contrast, bottom-up methods like L EMMANAID find                     formalized, constructing the required proofs from var-
interesting lemmas from a set of definitions, without                ious tactics is non-trivial, even with the help of tools
any predefined top-level goal (Lenat, 1976; McCasland                like Sledgehammer. This has motivated work on various
et al., 2017; Urban and Jakubův, 2020; Johansson and                LLM-driven methods for synthesizing proof scripts for
Smallbone, 2023). Evaluating bottom-up methods re-                   proof assistants such as Isabelle or Lean, either step by
quires defining a notion of conjecture interestingness,              step, whole proofs at once, or via proof sketches (Polu
typically using human-written formalizations as a gold-              and Sutskever, 2020; Wang et al., 2024; Ren et al., 2025;
standard (Montano-Rivas et al., 2012; Smallbone et al.,              Hubert et al., 2025; Chen et al., 2025; Wang et al., 2025;
2017; Einarsdóttir et al., 2018; Urban and Jakubův,                  1
                                                                         https://isabelle.in.tum.de/dist/
2020). Thus, we evaluate L EMMANAID by its coverage                  library/HOL/index.html
                                                                       2
of unseen test-set lemmas within a subset of Isabelle’s                  https://www.isa-afp.org


                                                                 2
Lin et al., 2025; Jiang et al., 2022; First et al., 2023;         called sketching has also been applied in the domain of
Jiang et al., 2023). Retrieval augmentation has been              program synthesis (Solar-Lezama, 2009). In the above
used to complement tactic search by fetching suitable             works, templates have typically been provided by the
lemmas and similar proofs from existing libraries (Yang           human user. Nye et al. (2019) used a neural network
et al., 2023; Thakur et al., 2024; Thompson et al., 2025),        to propose program sketches which were then filled in
with Kumarappan et al. (2025) also targeting continuous           by a symbolic program synthesizer, thus sharing some
learning on growing libraries. While our work does not            features with our work.
focus on producing proofs, we see it as an excellent
complement for future integration with systems like the           3         The L EMMANAID Approach
above.
                                                                  We have implemented a tool, L EMMANAID, for
Neural Conjecturing and Reinforcement Learning                    template-based conjecturing in Isabelle/HOL. We en-
Recent top-down conjecturing methods have success-                vision a user working on a new mathematical formal-
fully been used in test time reinforcement learning as a          ization; having defined some functions, types and other
means to generate additional data with the aim of cre-            concepts, and perhaps a few theorems about these. This
ating a curriculum for training a neural prover (Dong             collection of definitions, which we refer to as a (partial)
and Ma, 2025; Hubert et al., 2025; Chen et al., 2025),            theory, serves as input to the conjecturing system. L EM -
which has contributed to gold medal performances on               MANAID then outputs conjectures that are likely to be
International Math Olympiad problems (Hubert et al.,              useful in this context, allowing the user to make progress
2025; Chen et al., 2025). Here, conjectures are typi-             in their formalization, or better understand the behavior
cally variants of some given seed statement of interest.          of the theory they have defined so far. This happens
L EMMANAID, on the other hand, uses a bottom-up con-              in two stages: First (neural part), the partial theory is
jecturing approach and targets a different use-case. It           given as input to an LLM which outputs templates likely
aims to make novel suggestions directly from definitions,         to be relevant. Second (symbolic part), L EMMANAID
interesting to a human doing a formalization, rather than         searches over possible instantiations of those templates
generating variants of a given statement.                         in the current theory, to produce concrete conjectures.
   Other methods combining neural conjecturing and                See Figure 2 for an overview.
reinforcement learning have demonstrated success in                  We make all code, experimental scripts, data, and
specific domains , such as inductive proofs about synthe-         models publicly available online3 . See Appendix B
sized programs that generate integer sequences (Gau-              for details about computing resources and replication
thier and Urban, 2025). LEGO-prover attempts to intro-            parameters used in our evaluation.
duce intermediate proof statements as reusable lemmas
for other problems in the same domain (Wang et al.,               3.1       L EMMANAID’s Symbolic Engine
2024). Minimo treats conjecturing as a reinforcement              Template Language A template is an abstraction of
learning game in simple propositional logic, arithmetic,          a mathematical statement with most of the concrete
and group theory, with well-formed conjectures gener-             operators replaced by schematic variables called holes.
ated neurally via constrained decoding (Poesia et al.,            The template captures the overall structure of a state-
2024). Fermat combines symbolic rules and reinforce-              ment, with the intention that a template represents a
ment learning to form conjectures in elementary num-              family of analogous lemmas. Basic logical operators,
ber theory and on finite fields (Tsoukalas et al., 2025),         such as equality and quantifiers, are part of the template
and is evaluated against a gold-standard set of con-              to retain this high-level structure 4 . We simply imple-
jectures while simultaneously developing an interest-             ment templates using the standard internal term type
ingness function over conjectures. In contrast, L EM -            in Isabelle/HOL (Wenzel et al., 2026). As an example,
MANAID targets the broad range of theories from re-               consider the following lemmas about the Octonionic
search in computer science and mathematics represented            product and sum functions from the Isabelle ATP for-
in proof assistant libraries, and aims to avoid domain            malization about the octonions, an eight-dimensional
specific learning by generating generic templates as an           extension of complex numbers (Koutsoukou-Argyraki,
intermediate step.                                                2018):
Templates for Synthesizing Conjectures Follow-                    lemma octo product noncommutative:
ing the observation that many mathematical theories               ¬(∀x y :: octo.(x ∗ y = y ∗ x))
share analogical lemmas of similar shapes, Buchberger             lemma octo distrib left:
et al. (2006) first proposed to use templates as human-           a ∗ (b + c) = a ∗ b + a ∗ c for a b c :: octo
provided guidance in mathematical theory exploration,
by conjecturing interesting lemmas by analogy to known            lemma octo assoc plus:
shapes. This has been implemented in a range of sym-              a + (b + c) = (a + b) + c for a b c :: octo
bolic lemma conjecturing systems, including some tar-                   3
                                                                       https://anonymous.4open.science/r/
geting Isabelle/HOL (Montano-Rivas et al., 2012; Heras            lemmanaid-emnlp
et al., 2013; McCasland et al., 2017; Einarsdóttir et al.,          4
                                                                       See Appendix A for details about the standard logic sym-
2021; Nagashima et al., 2023). A similar technique                bols included in our template language.


                                                              3
        Formalization                                                Lemmanaid                                                            Evaluation
        theory x                                 Neural Engine                                 Symbolic Engine                              Gold-standard
                                                                                                                                            match?
         datatype a
                             Functions,                                                                                                     Counter-example
                                                                          Templates                                   Conjectures
         function f           context                                                                                                       found?
         function g
                                                                                                                                            Provable?



          Gold-standard lemma             [Symbols: *, +]                                                       1. x1*(x2+x3) = (x1*x2)+(x1*x3)
             octo_distrib_left:           [Types of *, +]        ?H1 x1 (?H2 x2 x3) = ?H2(?H1x1x2)(?H1 x1 x3)
                                                                                                                2. x1+(x2* x3) = (x1+x2)*(x1+x3)
       "a * (b + c) = a * b + a * c"       [Defs of *, +]



Figure 2: Overview showing how L EMMANAID conjectures lemmas and how we evaluated generated conjectures.

  If we abstract away the function symbols operating                                       L EMMANAID’s symbolic engine takes as input a tem-
on octonions, and rename the variables according to                                     plate and a list of function names. It then searches over
our template abstraction method, we obtain the three                                    the possible instantiations of the holes in the template
templates:
                                                                                        using the given functions (note that unlike holes the vari-
               ¬(∀ y0 y1 . ?H1 y0 y1 = ?H1 y1 y0 )                           (1)        ables are fixed at instantiation, and not replaced by any
                                                                                        further terms). Each indexed hole is replaced by one of
 ?H1 x1 (?H2 x2 x3 ) = ?H2 (?H1 x1 x2 ) (?H1 x1 x3 ) (2)                                the given function symbols while ensuring that the re-
         ?H1 x1 (?H1 x2 x3 ) = ?H1 (?H1 x1 x2 ) x3                           (3)        sulting candidate lemma is well typed. This may lead to
                                                                                        a number of different candidate lemmas being produced.
 Note how the function symbols ∗ and + operating
                                                                                        This instantiation task can be viewed as a constraint
on octonions have been replaced by the holes ?H1
                                                                                        satisfaction problem (CSP): holes are variables whose
and ?H2 , and the variables a, b, c, x, y standardized to
                                                                                        domains are function symbols, while type signatures of
y0 , y1 , x1 , x2 , x3 . Note that logical symbols, such as
                                                                                        symbols and arities of holes impose constraints on valid
negation ¬, universal quantifier ∀ and equals sign =
                                                                                        instantiations. We use standard forward checking (Har-
remain in the template structure. Technically, templates
                                                                                        alick and Elliott, 1980) to efficiently prune the search
are implemented as instances of Isabelle/HOL’s term
                                                                                        space.
datatype5 .
   Our template language represents analogous lemma                                        Revisiting our example, consider again template 3
statements, that have been abstracted and normalized in                                 (associativity). Suppose we give this template to L EM -
                                                                                        MANAID’s symbolic engine, along with the functions +
the following way: Function symbols are replaced with
a hole, represented as ?Hk where k is a positive integer                                (addition), − (subtraction), sin, cos and ˆ (exponentia-
label. Note that the type of the hole is also an abstraction                            tion) for real numbers, and the functions len (the length
of the type of the original symbol, with concrete types                                 of a list), rev (reversing a list) and @ (concatenate two
replaced by type variables. In our examples, the holes in                               lists). In the hole-filling step, it will come up with the
the templates above have types that match any function                                  following candidates:
with two arguments. Each occurrence of a particular
                                                                                                        (x1 + x2 ) + x3 = x1 + (x2 + x3 )
function symbol is replaced by the same hole label, even
in the case of polymorphic functions where different                                                   (x1 @ x2 ) @ x3 = x1 @ (x2 @ x3 )
occurrences of the symbol may have different types.                                                     (x1 − x2 ) − x3 = x1 − (x2 − x3 )
Variables are renamed to xk (or yk in the case of bound                                                                              x
                                                                                                                                   x 3
variables), where k is a non-negative integer label, and                                                         (xx1 2 )x3 = x1 2
their types set to match those of the corresponding holes.
                                                                                        Note how sin, cos, len, and rev cannot be used to fill
Template Instantiation We can instantiate or fill the                                   the hole ?H1 , since ?H1 is applied to two arguments and
holes in a template by any operator with a matching                                     therefore requires a binary operator. Also note that only
type. For instance, template 1 can be instantiated us-                                  the instantiations with + and @ result in valid lemmas,
ing any binary operator, such as subtraction on real                                    while the other two conjectures are false. The user can
numbers or concatenation on lists, to obtain a new con-                                 for instance apply Isabelle’s counterexample checker to
jecture. If the operator indeed is non-commutative,                                     easily identify these.
we obtain a correct lemma analogous to the lemma
octo product noncommutative. In this way, templates                                     3.2      L EMMANAID’s Neural Engine
are generalizations of lemma statements: each template                                  L EMMANAID’s neural engine uses a fine-tuned LLM
matches many different lemmas that may apply in dif-                                    to suggest templates given a theory context, which are
ferent theories.                                                                        then passed to L EMMANAID’s symbolic engine (§3.1).
   5
     See section 2.2 of the Isabelle/Isar Implementa-                                   For fine-tuning, we create labeled training data (input-
tion Manual https://isabelle.in.tum.de/dist/                                            output pairs) following §3.1: we extract the template
Isabelle2025/doc/implementation.pdf                                                     of each lemma appearing in a corpus of human-written


                                                                                    4
theory files, and use a string representation of the tem-        3.4       Dataset
plate as the desired output. For each output template, its
                                                                 We train and evaluate L EMMANAID on mathematical
corresponding input is the list of symbols appearing in
                                                                 libraries from the Isabelle proof assistant. First, the
the body of the original lemma, as well as contextual in-
                                                                 Isabelle/HOL library, which contains formalizations
formation about the symbols. For a given symbol, both
                                                                 based on higher order logic for a range of mathematics
its type and any known associated definition convey in-
                                                                 (e.g. number theory, analysis, algebra, set theory). Sec-
formation about how the symbol can be used. Although
                                                                 ond, we also use the Isabelle Archive of Formal Proofs
definitions provide more complete descriptions of sym-
                                                                 (AFP), which is a large collection of formalizations
bols, types are more succinct and they often provide
                                                                 from the research community including mathematics,
sufficient information to form well-typed templates and
                                                                 computer science and logic. At the time of writing, the
lemmas. Section 4.2 evaluates the effectiveness of types
                                                                 AFP includes about 285,200 lemmas in close to 900
and definitions as inputs. Revisiting the examples about
                                                                 theories. We extract templates for the lemmas in the
octonions, the lemma octo distrib left would result in
                                                                 above libraries as described in §3.1. In total, this results
the data-point of the shape:
                                                                 in a dataset of 62,816 data-points from the HOL library
  Input: [Symbols: ∗, +][Types of ∗, +][Defs of ∗, +]            and 210,898 data-points from the AFP6 .
  Output: ?H1 x1 (?H2 x2 x3 ) =                       (4)
                 ?H2 (?H1 x1 x2 ) (?H1 x1 x3 )
                                                                 4         Evaluation of L EMMANAID

To obtain the list of symbols present in a given lemma,          We set out to answer the following research questions:
we first construct a theory file with low-level ML code
                                                                 RQ1 How does our neuro-symbolic approach, L EM -
to interact with Isabelle/Isar top-level and retrieve the
                                                                     MANAID , compare with neural approaches and
lemma. To extract the symbols, we recursively iterate
                                                                     existing symbolic approaches?
over applications in the term storing any encountered
constants, using Isabelle-client (Shminke, 2022). The
                                                                 RQ2 How does different contextual information (such
list of symbols and their information is the minimal
                                                                     as types and definitions) impact performance?
context necessary to recover a given lemma. However,
additional context, such as relevant existing lemmas,
                                                                 RQ3 What characterizes the conjectures L EMMANAID
may further guide the conjecturing process and is an
                                                                     is able to generate (how many can be proved/have
interesting direction for future work.
                                                                     counter examples)?
3.3   Direct Neural Conjecturing
                                                                 4.1       Experimental Setup
While L EMMANAID employs a neural engine to gener-
ate templates and a symbolic engine to instantiate those         Models and Inference We evaluate three instances of
templates into lemmas, there is another approach one             L EMMANAID using DeepSeek-coder-1.3B, DeepSeek-
can take, which is to use a neural engine to directly            coder-6.7B and Llama-3.2-1B as neural backends.
generate lemmas. To create such a baseline, we adapt             These models are selected as representatives of open-
L EMMANAID’s neural engine, by instead fine-tuning it            weight base models performant on code-related tasks.
on tuples of the form (symbols, context, lemma) instead          One benefit of using smaller models in L EMMANAID
of a template. Revisiting the running example again, the         is that it supports a more realistic setup for actual users
lemma octo distrib left now results in a data-point of           wanting to use a conjecturing tool and run it locally
the shape:                                                       on their machine. See Appendix B for details about
                                                                 computing resources and replication parameters. At in-
  Input: [Symbols: ∗, +][Types of ∗, +][Defs of ∗, +]            ference time, we experiment with both greedy decoding
  Output: a * (b + c) = a * b + a * c                 (5)        and beam search (size 4), plus a combination of the two.

   Two possible string representations of the lemma in           Baselines There are no existing neural-based tools or
the output are: (1) the lemma command as appearing in            models for Isabelle to compare against so we train our
the source code of the theory file (what a human would           own neural baselines (Section 3.3), to directly suggest
write), and (2) a string representation of the internal          lemma. These are denoted by “neural” in tables in the
lemma object within the proving engine. We noticed               evaluation. QuickSpec is the state-of-the-art symbolic
early in our experimentation that an LLM is almost               tool for lemma conjecturing (Smallbone et al., 2017).
never able to predict the lemma command as it is less            QuickSpec is limited to generating equational lemmas as
structured than the lemma object, and so we use the              its conjecturing algorithm is based around enumerative
lemma object representation. While there is some nov-            synthesis of terms and the construction of equivalence
elty in predicting lemma objects directly as opposed to          classes via automated testing.
lemma commands, the main purpose of doing direct neu-                  6
                                                                     Some theories could not be processed by the batch method
ral lemma conjecturing is to create a suitable baseline          we used, due to technical issues with theory imports. Hence,
for our experiments.                                             our dataset does not cover everything from the AFP.


                                                             5
Benchmarks We derive our datasets from the Is-                     similarly parse the predicted and gold templates and
abelle/HOL library and the Archive of Formal Proofs                compare their Isabelle term representations. The metric
(recall §3.4) and create multiple train/validation/test sets       is therefore stricter than proving equivalence: predic-
from these libraries. We create two training sets: HOL-            tions that are merely logically equivalent after rewriting
train (57,576 datapoints containing only data from files           or other reasoning can still be counted as misses.
in the HOL library) and HOL+AFP-train (adding AFP
                                                                   Inference budget Note that the purely neural model
projects published before 2024, resulting in 249,098
                                                                   and L EMMANAID are given the same neural GPU-
datapoints). We also create two disjoint test sets: HOL-
                                                                   inference budget per task. The neural models attempt to
test (4,740 datapoints) and AFP-test (18,975 datapoints
                                                                   generate lemmas directly while L EMMANAID generates
from projects published in 2024). We note that while
                                                                   templates. L EMMANAID is then allowed an additional
HOL-train and HOL-test share style and are about re-
                                                                   (symbolic) CPU-budget of max 60s per task to search
lated topics, the data from the AFP tend to differ greatly
                                                                   for instantiations of the templates. L EMMANAID and
in topic, content, and style, why we expect AFP-test
                                                                   the neural conjecturing model are also given the same
to be more difficult. We fine-tune our LLMs on the
                                                                   input prompt, containing information about the symbols
respective training sets and evaluate on both test sets to
                                                                   occurring in the relevant gold-standard target lemma
evaluate: in-context performance (HOL-train + HOL-
                                                                   (see Eq. 4 in 3.2 and Eq. 5 in 3.3). These symbols are
test); the effect of adding more diverse training data
                                                                   also used as the function name inputs to L EMMANAID’s
(HOL+AFP-train + HOL-test); and finally the out-of-
                                                                   symbolic engine.
distribution performance (HOL-train/HOL+AFP-train
+ AFP-test). Evaluation on AFP-test also mitigates the
                                                                   4.2   RQ1–2: Discovery of Gold Standard Lemmas
risk of test data leakage for the fully neural baseline
models7 , as their publicly reported pretraining cutoff            To evaluate L EMMANAID and compare it against neural-
dates are in 2023, before the AFP-test projects were               only baselines and symbolic methods, we train L EM -
published.                                                         MANAID ’s neural model and the baseline models on
   For comparison with the symbolic tool Quick-                    either HOL-train or HOL+AFP-train, obtain multiple
Spec, we separately test on the Octonions                          variants, and evaluate them across different test sets
project (Koutsoukou-Argyraki, 2018) from the                       (Table 1). For each model, we compare the results ob-
AFP, which contains 350 lemmas, and leave it out of all            tained when various contextual information is included
training sets. We choose the Octonion formalization as             in the input: definitions, type information, or both (as
it consists of equational lemmas, which is the domain              described in 3.2). Note that adding only the definitions,
QuickSpec supports.                                                but not types, led to worse performance in initial exper-
                                                                   iments with DeepSeek 1.3B, so was not attempted for
Evaluation Metric A successful conjecturing system
                                                                   the other LLMs. For each model, we get 5 predictions:
ought to produce lemmas that are interesting and useful
                                                                   1 using greedy decoding, and 4 using beam search (with
in some sense. Note that what is interesting and useful
                                                                   beam size of 4). We break down the results for each
is very much context dependent on for example existing
                                                                   decoding method in Appendix C.
definitions, lemmas and theorems, available tactics and
                                                                      We see that L EMMANAID outperforms the respective
potential different downstream tasks. Hence, there is
                                                                   neural baselines on all test sets, with the best model (us-
non-trivial to define a metric that will be relevant across
                                                                   ing DeepSeek 6.7B and HOL+AFP training) reaching
any formalization in Isabelle. As a proxy, we therefore
                                                                   50.2% on HOL-test and 28.6% on AFP-test. For the
choose to evaluate against gold-standard lemmas written
                                                                   smaller 1B models, the DeepSeek backend appears to
by humans in Isabelle, so they ought to align with what
                                                                   consistently outperform Llama-3.2. We also see that
the human expert author thought was interesting and
                                                                   neural methods are somewhat complementary to L EM -
useful, and thus worth including in the formalization in
                                                                   MANAID: taken as an ensemble they discover even more
the first place.
                                                                   lemmas, 58.6% on HOL-test and 42.7% on AFP-test
   In each evaluation task, there is one gold-standard
                                                                   (using DeepSeek 6.7B and HOL+AFP training). The
lemma. The method being assessed generates a set of
                                                                   inclusion of type information is greatly beneficial to
suggested lemmas, and is considered successful if the
                                                                   both L EMMANAID and the neural baseline method. We
gold-standard lemma is among these. Our matching
                                                                   see that in some cases the success rate is higher when
criterion is based on Isabelle’s internal representation
                                                                   only type information is included and definitions are
of terms. For lemma-object predictions, we parse both
                                                                   excluded, while in others including both is beneficial,
the gold-standard lemma and each suggested lemma in
                                                                   although the differences are relatively small. We see
Isabelle, in the source theory context, and compare their
                                                                   that on AFP-test, the performance drops for all variants
internal term representations. This accepts harmless pre-
                                                                   compared to their results on HOL-test. This is unsur-
sentational differences such as alpha-renamed variables
                                                                   prising, as the lemmas in AFP projects are more diverse
and eta-contracted forms. For template predictions, we
                                                                   than those in HOL. Also, the input to the LLMs may
   7
     Recall that L EMMANAID’s neural module produce tem-           not always include enough contextual information for
plates rather than lemmas, and as the templates were created       retrieving definitions in AFP theories requiring long-
by us they are not present in prior training data.                 distance dependencies, though we always account for


                                                               6
Table 1: Percentage of gold-standard lemmas discovered for L EMMANAID and a neural version. We include results
for the symbolic QuickSpec tool only on Octonions which is in its scope. Results are for 5 predictions (greedy
decoding & beam search with beam size 4). Note that due to limited computational resources and poor results using
DeepSeek 1.3B, we did not further explore the prompting technique with only definitions for the other models.

                                                HOL-train                              HOL+AFP-train
                                   HOL-test     AFP-Test Octonions             HOL-test AFP-Test Octonions
      DeepSeek-coder-1.3B
      L EMMANAID (types + defs)    39.5%        20.3%           57.4%          41.8%        28.2%         66.9%
      L EMMANAID (types)           37.6%        19.7%           58.3%          35.7%        27.4%         56.0%
      L EMMANAID (defs)            33.2%        7.3%            54.6%          35.6%        13.0%         61.4%
      Neural (types + defs)        30.5%        11.9%           34.0%          30.9%        18.6%         46.0%
      Neural (types)               33.4%        12.9%           42.9%          30.1%        15.0%         48.0%
      Neural (defs)                30.5%        6.2%            41.4%          26.1%        7.8%          45.1%
      L EMMANAID Combined          48.0%        26.4%           67.7%          49.8%        35.9%         75.7%
      Neural Combined              42.6%        17.8%           53.1%          39.4%        23.7%         59.1%
      Combined                     53.3%        28.5%           70.9%          53.1%        38.7%         79.4%
      DeepSeek-coder-6.7B
      L EMMANAID (types + defs)    46.5%        26.3%           68.0%          50.2%        27.9%         76.6%
      L EMMANAID (types)           43.3%        22.5%           67.1%          44.5%        28.6%         78.9%
      Neural (types + defs)        42.3%        19.7%           53.1%          29.7%        25.1%         62.3%
      Neural (types)               38.6%        19.0%           51.4%          38.5%        25.2%         53.1%
      L EMMANAID Combined          52.2%        29.4%           76.0%          55.1%        34.8%         83.1%
      Neural Combined              46.8%        23.5%           59.4%          44.1%        31.6%         65.7%
      Combined                     57.2%        32.1%           79.7%          58.6%        42.7%         84.9%
      Llama-3.2-1B
      L EMMANAID (types + defs)    31.7%        17.7%           57.4%          28.6%        19.3%         60.6%
      L EMMANAID (types)           34.1%        15.0%           59.7%          35.0%        27.2%         65.1%
      Neural (types + defs)        23.1%        6.2%            40.6%          19.2%        12.9%         32.3%
      Neural (types)               22.8%        8.8%            42.3%          17.7%        12.2%         32.6%
      L EMMANAID Combined          39.3%        21.1%           62.6%          38.5%        30.4%         67.4%
      Neural Combined              28.9%        11.1%           48.6%          24.7%        17.7%         45.1%
      Combined                     42.9%        22.6%           64.0%          41.2%        32.9%         68.6%
      QuickSpec                    —            —               22.8%          —            —             22.8%


HOL as a dependency.                                           Applicability to Realistic Formalizations Appendix
   For Octonions, L EMMANAID models (best reach-               D shows a breakdown per projects/theories in HOL-test
ing 78.9%) outperform their respective neural base-            and AFP-test, with the number of test lemmas from
lines (62.3%) while both greatly outperform QuickSpec          each and the success rate of the best-performing L EM -
(reaching just 22.8%). Similar to other datasets, an en-       MANAID and neural ensembles with DeepSeek 6.7B.
semble of L EMMANAID and neural models provides a              We note that L EMMANAID performs better on almost
significant improvement, with overall lemma success            every test theory in the test sets. We also list the topic of
rate up to 84.9%. Not shown in Table 1 is that Quick-          the different AFP formalizations in our test set, showing
Spec generates several thousand lemmas, giving it an           that they range over a variety of different topics from
extremely poor precision of less than 1%. This is be-          Computer Science, Mathematics and Logic. The results
cause it has limited heuristics for judging which lemmas       confirm that L EMMANAID’s approach to conjecturing
are interesting, and only skips lemmas that are logical        by analogy successfully produces interesting lemmas
consequences of existing lemmas. It also skips several         across a wide range of real world formalizations.
useful and simple lemmas, such as inner e1 x = Im 1 x,         Generated Conjectures We take a closer look at
as they are considered trivial consequences of other           the full set of conjectures generated by the best-
lemmas. This is further discussed in Appendix H.               performing instance of L EMMANAID (DeepSeek 6.7B
                                                               and HOL+AFP training), under greedy decoding. We
4.3    RQ3: Analysis of Generated Conjectures                  separate the generated conjectures into three main cate-
                                                               gories (true, false and unresolved) using the Sledgeham-
In §4.2, we counted the number of gold standard lemmas         mer tool for automated proofs (Blanchette et al., 2011),
discovered. Here, we break down these results further.         and counter-example finding tools Nitpick (Blanchette


                                                           7
Table 2: Gold-standard lemma discovery rates on the commercial LLM benchmark. Fine-tuned models use five
predictions per task: one greedy prediction and four beam-search predictions, and the types+defs prompting strategy.
Commercial LLMs also use five predictions per task: one greedy prediction and four temperature-1 samples.

                                Template                                                      Lemma-object
Model                                        Octonions AFP-2026          Model                             Octonions AFP-2026
L EMMANAID DeepSeek-coder-1.3B                66.9%       30.9%          Neural DeepSeek-coder-1.3B           44.0%        25.2%
L EMMANAID DeepSeek-coder-6.7B                76.6%       41.7%          Neural DeepSeek-coder-6.7B           61.7%        38.1%
L EMMANAID Llama-3.2-1B                       46.9%       28.1%          Neural Llama-3.2-1B                  54.6%        23.0%
Claude Opus 4.5                               47.1%       19.4%          Claude Opus 4.5                      46.3%        34.5%
GPT-5.2                                       50.0%       15.8%          GPT-5.2                              45.4%        25.2%


and Nipkow, 2010) and Quickcheck (Bulwahn, 2012).                   of training data leakage.
True conjectures consist of 1) the gold-standard lem-                  While the setup is different between instruction fine-
mas, and 2) other conjectures proved by Sledgehammer.               tuned commercial models and the auto regressive fine-
False conjectures are those for which we can find a                 tuned models in the previous section, we attempt to
counter-examples. Unresolved conjectures are those                  compare them under as similar conditions as possible.
that can neither be proved by Sledgehammer, nor have                We used five few-shot examples per problem, both for
a counter-example.                                                  template generation and for direct conjecture genera-
   For HOL-test (4,740 gold-standard lemmas), L EM -                tion. Relevant examples are selected from our AFP-
MANAID generates 7,628 conjectures. Table 3 shows                   train dataset to reflect a reasonably fair comparison.
a breakdown of these conjectures: 1,356 are true state-             Details of this selection as well as the prompts to the
ments which don’t match the gold-standard lemmas,                   LLMs are in Appendix G. The success rates for the com-
and 2,749 are unresolved conjectures which require fur-             mercial models are also calculated based on the top-5
ther non-trivial reasoning. Appendix F contains some                predictions. Note however that the commercial models
examples of these, and Appendix E additional statistics.            consume considerably more compute and tokens: for
                                                                    comparison the inputs for template prediction for the
        Table 3: Generated conjectures for HOL-test.                fine-tuned models are about 325 token per query, while
                                                                    for the commercial models it is about 1700 tokens. The
          Category                    Size                          results are summarised in Table 2.
          Gold-standard               1721 (22.6%)
          Other True Statements       1356 (17.8%)                  6   Conclusion
          False Conjectures           1802 (23.6%)
                                                                    L EMMANAID is a novel neuro-symbolic bottom-up con-
          Unresolved Conjectures      2749 (36.0%)
                                                                    jecturing tool for the Isabelle proof assistant. L EM -
          Total                       7628
                                                                    MANAID works by (neurally) learning analogical fam-
                                                                    ilies of conjectures, represented as templates which
5       Comparison with Commercial LLMs                             are symbolically instantiated in new theories. This ap-
A common question arising is whether a commercial                   proach is efficient at discovering lemmas in formaliza-
closed-source LLM would have been able to perform the               tions across a wide range of topics from Isabelle’s HOL
conjecturing task as well or better without any additional          and AFP libraries. L EMMANAID outperforms fine-tuned
fine tuning:                                                        neural baselines, symbolic tools and, on a test set in-
   RQ4: How does large commercial instruction fine-                 cluding recent formalizations, also commercial models
tuned models perform both as backends for L EM -                    Claude Opus 4.5 and GPT-5.2. We demonstrate that
MANAID, and on the direct conjecturing task?                        by fine-tuning smaller models on the simpler task of
As a complement to our results using auto-regressive                template generation, good results are achievable with a
fine-tuned models above, we therefore also evaluate                 modest amount of compute.
Claude Opus 4.5 and GPT-5.2 with few-shot learning.                    The best-performing L EMMANAID backend
For economic reasons, this evaluation is conducted on               (deepseek-6.7b), discovers 50% of gold standard
a limited test set: our running example of Octonions,               lemmas for HOL-test, 29% for AFP-test and 41% on
as well as two formalizations added to Isabelle’s AFP               AFP-2026. Ensembling different prompting strategies
in 2026 involving the common list datatype: Swap Dis-               further improves results, showing that the different
tance (Eberl, 2026b), and Linear Orders as Rankings                 approaches discover slightly different conjectures.
(Eberl, 2026a). The training cut-offs for both Claude                  This work is a first step toward demonstrating the
Opus 4.5 and GPT-5.2 are in 2025, so using two very                 usability of neuro-symbolic analogical conjecturing for
recent formalizations ought to minimize8 the probability
                                                                    course have been on the internet prior to 2026, so we cannot
    8
        Development versions of these formalizations might of       fully guarantee there was no leakage.


                                                                8
proof assistants on a realistic selection of theories from       References
real formalizations in computer science, mathematics,
                                                                 Zhangir Azerbayev, Bartosz Piotrowski, Hailey
and logic, going beyond benchmark theories from high-              Schoelkopf, Edward W. Ayers, Dragomir Radev, and
school and undergraduate mathematics competitions.                 Jeremy Avigad. 2023. ProofNet: Autoformalizing
                                                                   and formally proving undergraduate-level mathemat-
Limitations                                                        ics. Preprint, arXiv:2302.12433.

Due to limitations in computational resources, we have           Jasmin Christian Blanchette, Sascha Böhme, and
evaluated the Lemmanaid framework with smaller LLM                 Lawrence C. Paulson. 2011. Extending Sledgeham-
backends, ranging between 1B to 6.7B, for two dif-                 mer with SMT solvers. Journal of Automated Rea-
                                                                   soning, 51:109 – 128.
ferent model families, DeepSeek and Llama 3. Each
instance of Lemmanaid requires fine-tuning both the              Jasmin Christian Blanchette and Tobias Nipkow. 2010.
template-generation model, and a direct neural conjec-             Nitpick: A counterexample generator for higher-
turing model. This in turn, was done for two (or three)            order logic based on a relational model finder. In
different prompting strategies (see e.g. table 1), includ-         International conference on interactive theorem prov-
ing either both type and function definitions, or only             ing, pages 131–146. Springer.
one of them. Further prompting experiments, and wider            Bruno Buchberger, Adrian Craciun, Tudor Jebelean,
beam searches were beyond the scope of our compu-                  Laura Kovács, Temur Kutsia, Koji Nakagawa, Flo-
tational budget. Furthermore, for the largest model                rina Piroi, Nikolaj Popov, Judit Robu, Markus
(Deepseek-coder-6.7b) we suspect additional compu-                 Rosenkranz, and Wolfgang Windsteiger. 2006. Theo-
tational resources might have revealed slightly better             rema: Towards computer-aided mathematical theory
hyper-parameter settings, which with additional fine-              exploration. Journal of Applied Logic, 4:470–504.
tuning could have improved those results further.                Lukas Bulwahn. 2012. The new Quickcheck for Is-
   We have evaluated L EMMANAID by comparing it to                 abelle: Random, exhaustive and symbolic testing
gold-standard human written lemmas from Isabelle for-              under one roof. In International Conference on Cer-
malizations, motivated by the assumption that human                tified Programs and Proofs, pages 92–108. Springer.
domain experts have a good idea of what is interesting           Luoxin Chen, Jinming Gu, Liankai Huang, Wenhao
and useful in each different formalization. Evaluating             Huang, Zhicheng Jiang, Allan Jie, Xiaoran Jin, Xing
whether the conjectures are actually useful for other,             Jin, Chenggang Li, Kaijing Ma, Cheng Ren, Jiawei
yet unknown, downstream tasks was not the goal of                  Shen, Wenlei Shi, Tong Sun, He Sun, Jiahui Wang,
the evaluation, nor the question we aimed to answer in             Siran Wang, Zhihong Wang, Chenrui Wei, and 17
this paper. Assessing the usefulness of a tool like L EM -         others. 2025. Seed-prover: Deep and broad rea-
MANAID for human users working on real formalization               soning for automated theorem proving. Preprint,
tasks would indeed be a very interesting follow-up study           arXiv:2507.23726.
warranting a paper in its own right, but is beyond the           Simon Colton. 2002. The HR program for theorem gen-
scope of the current paper.                                        eration. In Automated Deduction—CADE-18, pages
   As described in §4.3, proofs of the conjectures gen-            285–289, Berlin, Heidelberg. Springer Berlin Heidel-
erated by L EMMANAID have only been attempted by                   berg.
the fully automated tactic Sledgehammer. While power-            Johan Commelin and Adam Topaz. 2024. Abstraction
ful, any conjectures requiring a more specialized tactic-          boundaries and spec driven development in pure math-
based proof remain open. In this paper, our focus was              ematics. Bull. Amer. Math. Soc., 61.
a comparison across a wide range of formalizations
against their gold-standard lemmas, and we leave deeper          Leonardo de Moura, Soonho Kong, Jeremy Avigad,
analysis and interactive proof attempts of open conjec-            Floris van Doorn, and Jakob von Raumer. 2015. The
                                                                   Lean theorem prover (system description). In Auto-
tures in each theory as future work.
                                                                   mated Deduction - CADE-25, pages 378–388, Cham.
   We conducted a smaller evaluation of using commer-              Springer International Publishing.
cial high-powered LLMs as backends for L EMMANAID
as well as for direct conjecturing. We limited this evalu-       Kefan Dong and Tengyu Ma. 2025. STP: Self-play
ation to a smaller set for two reasons: First, we wanted           LLM theorem provers with iterative conjecturing and
to at least minimize the amount of test-data leakage by            proving. In Forty-second International Conference
                                                                   on Machine Learning.
choosing formalizations entered into the Isabelle AFP
after the training cut-off dates of the LLMs. Secondly,          Manuel Eberl. 2026a. Linear orders as rankings.
we needed to keep to a limited budget. While we at-               Archive of Formal Proofs. https://isa-afp.
tempt to conduct the comparative experiments under as             org/entries/Rankings.html, Formal proof
similar conditions as possible, we once again emphasize           development.
that there are inherent differences in the models consid-        Manuel Eberl. 2026b. Swap distance. Archive
ering computational resources and cost, training, and             of Formal Proofs. https://isa-afp.org/
input prompt token usage.                                         entries/Swap_Distance.html,        Formal
                                                                  proof development.


                                                             9
Sólrún Halla Einarsdóttir, Márton Hajdu, Moa Johans-         Andrew Ireland and Alan Bundy. 1996. Productive use
   son, Nicholas Smallbone, and Martin Suda. 2024.                 of failure in inductive proof. Journal of Automated
   Lemma discovery and strategies for automated in-                Reasoning, 16:79–111.
   duction. In Automated Reasoning, pages 214–232,
   Cham. Springer Nature Switzerland.                            Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski,
                                                                   Konrad Czechowski, Tomasz Odrzygóźdź, Piotr
Sólrún Halla Einarsdóttir, Moa Johansson, and Jo-               Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022. Thor:
   hannes Åman Pohjola. 2018. Into the infinite - theory          Wielding hammers to integrate language models and
   exploration for coinduction. In Proceedings of AISC             automated theorem provers. In Advances in Neural
   2018, pages 70–86.                                              Information Processing Systems.

Sólrún Halla Einarsdóttir, Moa Johansson, and Nicholas        Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou,
   Smallbone. 2022. LOL: A library of lemma templates              Timothee Lacroix, Jiacheng Liu, Wenda Li, Mateja
   for data-driven conjecturing. In Work-in-progress pa-           Jamnik, Guillaume Lample, and Yuhuai Wu. 2023.
   pers presented at the 15th Conference on Intelligent            Draft, sketch, and prove: Guiding formal theorem
   Computer Mathematics (CICM 2022) Informal Pro-                  provers with informal proofs. In The Eleventh Inter-
   ceedings, page 22.                                              national Conference on Learning Representations.
                                                                 Moa Johansson. 2019. Lemma discovery for induction.
Sólrún Halla Einarsdóttir, Nicholas Smallbone, and Moa
                                                                  In Intelligent Computer Mathematics, pages 125–139,
   Johansson. 2021. Template-based theory exploration:
                                                                  Cham. Springer International Publishing.
   Discovering properties of functional programs by test-
   ing. In Proceedings of the 32nd Symposium on Imple-           Moa Johansson, Dan Rosén, Nicholas Smallbone, and
   mentation and Application of Functional Languages,             Koen Claessen. 2014. Hipster: Integrating theory
   IFL ’20, page 67–78, New York, NY, USA. Associa-               exploration in a proof assistant. In Proceedings of
   tion for Computing Machinery.                                  CICM, pages 108–122. Springer.
S. Fajtlowicz. 1988. On conjectures of Graffiti. Discrete        Moa Johansson and Nicholas Smallbone. 2023. Explor-
   Math., 72(13):113–118.                                         ing mathematical conjecturing with large language
                                                                  models. In 17th International Workshop on Neural-
Emily First, Markus Rabe, Talia Ringer, and Yuriy                 Symbolic Learning and Reasoning, NeSy 2023.
 Brun. 2023. Baldur: Whole-Proof Generation and
 Repair with Large Language Models. In Proceed-                  Angeliki Koutsoukou-Argyraki. 2018. Octonions.
 ings of the 31st ACM Joint European Software En-                 Archive of Formal Proofs. https://isa-afp.
 gineering Conference and Symposium on the Foun-                   org/entries/Octonions.html,          Formal
 dations of Software Engineering, ESEC/FSE 2023,                   proof development.
 page 1229–1241, New York, NY, USA. Association
 for Computing Machinery.                                        Adarsh Kumarappan, Mo Tiwari, Peiyang Song,
                                                                   Robert Joseph George, Chaowei Xiao, and Anima
Thibault Gauthier and Josef Urban. 2025. Learning                 Anandkumar. 2025. Leanagent: Lifelong learning for
  conjecturing from scratch. In Automated Deduction -              formal theorem proving. In The Thirteenth Interna-
  CADE-30.                                                         tional Conference on Learning Representations.

W. T. Gowers, Ben Green, Freddie Manners, and Ter-               Cole Kurashige, Ruyi Ji, Aditya Giridharan, Mark Bar-
  ence Tao. 2023. On a conjecture of Marton. Preprint,             bone, Daniel Noor, Shachar Itzhaky, Ranjit Jhala,
  arXiv:2311.05762.                                                and Nadia Polikarpova. 2024. CCLemma: E-graph
                                                                   guided lemma discovery for inductive equational
Thomas Hales, Mark Adams, Gertrud Bauer, Tat Dat                   proofs. Proc. ACM Program. Lang., 8(ICFP).
  Dand, John Harrison, Le Troung Hoan, Cezary
                                                                 Douglas B. Lenat. 1976. AM, an artificial intelligence
  Kaliszyk, Victor Magron, Sean McLaughlin,
                                                                   approach to discovery in mathematics as heuristic
  Tat Thanf Nguyen, and et al. 2017. A formal proof
                                                                   search. Ph.D. thesis, Stanford University.
  of the Kepler conjecture. Forum of Mathematics, Pi,
  5:e2.                                                          Yong Lin, Shange Tang, Bohan Lyu, Jiayun Wu,
                                                                   Hongzhou Lin, Kaiyu Yang, Jia Li, Mengzhou
Robert M Haralick and Gordon L Elliott. 1980. Increas-             Xia, Danqi Chen, Sanjeev Arora, and Chi Jin.
  ing tree search efficiency for constraint satisfaction           2025. Goedel-prover: A frontier model for open-
  problems. Artificial intelligence, 14(3):263–313.                source automated theorem proving.     Preprint,
                                                                   arXiv:2502.07640.
Jonathan Heras, Ekaterina Komendantskaya, Moa Jo-
  hansson, and Ewen Maclean. 2013. Proof-pattern                 Daniel Matichuk, Toby Murray, and Makarius Wenzel.
  recognition and lemma discovery in ACL2. In Pro-                 2016. Eisbach: A proof method language for Isabelle.
  ceedings of LPAR.                                                J. Autom. Reason., 56(3):261–282.
T. Hubert, R. Mehta, and L. et al. Sartran. 2025.                R. L. McCasland, A. Bundy, and P. F. Smith. 2017.
  Olympiad-level formal mathematical reasoning with                MATHsAiD: Automated mathematical theory explo-
  reinforcement learning. Nature.                                  ration. Applied Intelligence.


                                                            10
Omar Montano-Rivas, Roy McCasland, Lucas Dixon,                 Christian Szegedy. 2020. A promising path towards
 and Alan Bundy. 2012. Scheme-based theorem dis-                  autoformalization and general artificial intelligence.
 covery and concept invention. Expert systems with                In Intelligent Computer Mathematics, pages 3–20,
 applications, 39(2):1637–1646.                                   Cham. Springer International Publishing.

Yutaka Nagashima, Zijin Xu, Ningli Wang, Daniel Se-             Terrence Tao. 2023. Formalizing the proof of pfr in
  bastian Goc, and James Bang. 2023. Template-                    lean4 using blueprint: a short tour.
  based conjecturing for automated induction in Is-
                                                                Amitayush Thakur, George Tsoukalas, Yeming Wen,
  abelle/HOL. In Fundamentals of Software Engineer-
                                                                 Jimmy Xin, and Swarat Chaudhuri. 2024. An in-
  ing, pages 112–125, Cham. Springer Nature Switzer-
                                                                 context learning agent for formal theorem-proving.
  land.
                                                                 In First Conference on Language Modeling.
Tobias Nipkow, Markus Wenzel, and Lawrence C. Paul-             Kyle Thompson, Nuno Saavedra, Pedro Carrott, Kevin
  son. 2002. Isabelle/HOL: a proof assistant for higher-          Fisher, Alex Sanchez-Stern, Yuriy Brun, João F.
  order logic. Springer-Verlag, Berlin, Heidelberg.               Ferreira, Sorin Lerner, and Emily First. 2025.
                                                                  Rango: Adaptive retrieval-augmented proving for
Maxwell Nye, Luke Hewitt, Joshua Tenenbaum, and                   automated software verification. In Proceedings of
 Armando Solar-Lezama. 2019. Learning to infer pro-               the IEEE/ACM 47th International Conference on Soft-
 gram sketches. In Proceedings of the 36th Interna-               ware Engineering, ICSE ’25, page 347–359. IEEE
 tional Conference on Machine Learning, volume 97                 Press.
 of PMLR, pages 4861–4870.
                                                                George Tsoukalas, Jasper Lee, John Jennings, Jimmy
Gabriel Poesia, David Broman, Nick Haber, and Noah                Xin, Michelle Ding, Michael Jennings, Amitayush
  Goodman. 2024. Learning formal mathematics from                 Thakur, and Swarat Chaudhuri. 2024. Putnam-
  intrinsic motivation. In The Thirty-eighth Annual               Bench: Evaluating neural theorem-provers on
  Conference on Neural Information Processing Sys-                the putnam mathematical competition. Preprint,
  tems.                                                           arXiv:2407.11214.
Stanislas Polu and Ilya Sutskever. 2020. Generative             George Tsoukalas, Rahul Saha, Amitayush Thakur, Sab-
  language modeling for automated theorem proving.                rina Reguyal, and Swarat Chaudhuri. 2025. Learning
  Preprint, arXiv:2009.03393.                                     interestingness in automated mathematical theory for-
                                                                  mation. In The Thirty-ninth Annual Conference on
Markus N. Rabe, Dennis Lee, Kshitij Bansal, and Chris-            Neural Information Processing Systems.
 tian Szegedy. 2021. Mathematical reasoning via
 self-supervised skip-tree training. In Proceedings             Josef Urban and Jan Jakubův. 2020. First neural conjec-
 of ICLR.                                                         turing datasets and experiments. In Proceedings of
                                                                  CICM.
Z. Z. Ren, Zhihong Shao, Junxiao Song, Huajian Xin,
  Haocheng Wang, Wanjia Zhao, Liyue Zhang, Zhe Fu,              Haiming Wang, Mert Unsal, Xiaohan Lin, Mantas
  Qihao Zhu, Dejian Yang, Z. F. Wu, Zhibin Gou, Shi-              Baksys, Junqi Liu, Marco Dos Santos, Flood Sung,
  rong Ma, Hongxuan Tang, Yuxuan Liu, Wenjun Gao,                 Marina Vinyes, Zhenzhe Ying, Zekai Zhu, Jianqiao
  Daya Guo, and Chong Ruan. 2025. DeepSeek-Prover-                Lu, Hugues de Saxcé, Bolton Bailey, Chendong Song,
  V2: Advancing formal mathematical reasoning via                 Chenjun Xiao, Dehao Zhang, Ebony Zhang, Freder-
  reinforcement learning for subgoal decomposition.               ick Pu, Han Zhu, and 21 others. 2025. Kimina-Prover
  Preprint, arXiv:2504.21801.                                     preview: Towards large formal reasoning models with
                                                                  reinforcement learning. Preprint, arXiv:2504.11354.
Peter Scholtze. 2020. Liquid tensor experiment.                 Haiming Wang, Huajian Xin, Chuanyang Zheng,
Boris Shminke. 2022. Python client for Isabelle server.           Zhengying Liu, Qingxing Cao, Yinya Huang, Jing
  Preprint, arXiv:2212.11173.                                     Xiong, Han Shi, Enze Xie, Jian Yin, Zhenguo Li, and
                                                                  Xiaodan Liang. 2024. LEGO-prover: Neural theorem
Eytan Singher and Shachar Itzhaky. 2021. Theory explo-            proving with growing libraries. In The Twelfth Inter-
  ration powered by deductive synthesis. In Computer              national Conference on Learning Representations.
  Aided Verification, pages 125–148, Cham. Springer             Qingxiang Wang, Cezary Kaliszyk, and Josef Urban.
  International Publishing.                                       2018. First experiments with neural translation of
                                                                  informal to formal mathematics. In Intelligent Com-
Nicholas Smallbone, Moa Johansson, Koen Claessen,
                                                                  puter Mathematics, pages 255–270, Cham. Springer
  and Maximilian Algehed. 2017. Quick specifications
                                                                  International Publishing.
  for the busy programmer. Journal of Functional Pro-
  gramming, 27.                                                 Makarius Wenzel, Stefan Berghofer, Florian Haftmann,
                                                                 and Larry Paulson. 2026. The Isabelle/Isar imple-
Armando Solar-Lezama. 2009. The sketching approach               mentation manual.
  to program synthesis. In Proceedings of the 7th Asian
  Symposium on Programming Languages and Systems,               Yuhuai Wu, Albert Qiaochu Jiang, Wenda Li,
  APLAS ’09, page 4–13, Berlin, Heidelberg. Springer-             Markus Norman Rabe, Charles E Staats, Mateja Jam-
  Verlag.                                                         nik, and Christian Szegedy. 2022. Autoformalization


                                                           11
    with large language models. In Advances in Neural                  • Inequality symbols: less, greater, less or
    Information Processing Systems.                                      equal, greater or equal Defined in ”Or-
                                                                         derings.ord class.less eq”        and      ”Order-
Kaiyu Yang, Gabriel Poesia, Jingxuan He, Wenda Li,                       ings.ord class.less” (greater and greater eq
  Kristin E. Lauter, Swarat Chaudhuri, and Dawn Song.
                                                                         are defined in terms of less and less eq and are
  2025. Position: Formal mathematical reasoning—a
  new frontier in AI. In Forty-second International                      translated in the term structure so we don’t expect
  Conference on Machine Learning Position Paper                          them to appear in templates).
 Track.
                                                                   Implementation details of the exact symbols and how
Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chala-                  to extract them are available in our anonymous code
  mala, Peiyang Song, Shixing Yu, Saad Godil, Ryan                 repository.
  Prenger, and Anima Anandkumar. 2023. LeanDojo:
  theorem proving with retrieval-augmented language                B     Computing Resources and Details for
  models. In Proceedings of the 37th International                       Replication
  Conference on Neural Information Processing Sys-
  tems, NIPS ’23, Red Hook, NY, USA. Curran Asso-                  We run the majority of our training and evaluation on 8
  ciates Inc.                                                      NVIDIA RTX 2080 Ti (11GB VRAM). The Deepseek
                                                                   6.7B models are trained and evaluated on 4 NVIDIA
Lan Zhang, Marco Valentino, and Andre Freitas. 2025.               Tesla A40s, each with 48GB of VRAM. We use 8-bit
  Autoformalization in the wild: Assessing LLMs on
                                                                   quantization when loading models for both fine-tuning
  real-world mathematical definitions. In Proceed-
  ings of the 2025 Conference on Empirical Methods                 and inference. We train models with DistributedData-
  in Natural Language Processing, pages 1720–1738,                 Parallel (DDP) for 12 epochs and 8e − 4 learning rate.
  Suzhou, China. Association for Computational Lin-                We use a maximum sequence length of 1024 with 200
  guistics.                                                        tokens reserved for the output. We use an effective batch
                                                                   size 16.
Kunhao Zheng, Jesse Michael Han, and Stanislas Polu.
  2022. miniF2F: a cross-system benchmark for for-                 C     Results found using greedy decoding vs
  mal olympiad-level mathematics. In International
  Conference on Learning Representations.
                                                                         beam search
                                                                   We break down the results from Table 1 in Table 4 to
A       Template language and symbols                              show the performance of different decoding strategies.
                                                                   The results in Table 4 are for greedy decoding and beam
Templates are implemented as instances of Is-
                                                                   search. Greedy decoding selects the token with the high-
abelle/HOL’s term datatype9 . While theory-specific
                                                                   est probability at each generation step. Beam search
symbols are replaced by holes, general logical symbols
                                                                   obtains multiple high-probability predictions for a given
remain in the template to not make it overly abstract
                                                                   model. We see that beam search helps to improve results
and obscuring the analogies we wish to uncover. The
                                                                   for both L EMMANAID and the neural baseline ensem-
symbols that are part of the template language and not
                                                                   bles. However, L EMMANAID is still performant in a
abstracted away are:
                                                                   greedy setting, showing that the approach can achieve
    • All constants whose names begin with ‘HOL.’                  good results with a smaller inference budget.
      These are the functions defined in Isabelle/sr-
      c/HOL/HOL.thy including equality, True, False,               D     Breakdown of Results per Theory
      Not, All and Ex (quantifiers), conjunction and dis-          D.1    HOL-test
      junction.
                                                                   For the lemmas included in our test set HOL-test, Ta-
    • All constants whose names begin with ‘Pure.’                 ble 5 shows the number of test lemmas from each ses-
      Basic logical constructs including implication               sion and the lemma success rates (in percentages) of
      (Pure.imp), Pure.all, Pure.eq, defined in Isabelle/s-        L EMMANAID, neural-only lemma prediction, and their
      rc/Pure/logic.ML                                             combination. The results shown are the ensembles of
                                                                   the different variants of L EMMANAID and the neural
    • Bounded quantifiers for sets (these are rendered the         baselines, trained on HOL+AFP-train using DeepSeek-
      same as the regular quantifiers defined in HOL).             coder-6.7b. We created a file-wise split of the HOL
                                                                   library.
    • Set membership.                                                 For the 29 different sessions, we see that the L EM -
                                                                   MANAID ensemble outperforms the neural ensemble on
    • Pairs/Cartesian products as defined in sr-                   25 of them, while the neural ensemble performs better
      c/HOL/Product Type.                                          in one case, and in the remaining three both methods
    9
     See section 2.2 of the Isabelle/Isar Implementa-              get the same rate of accurate predictions (0% in two
tion Manual https://isabelle.in.tum.de/dist/                       of the three). On average the success rate of the L EM -
Isabelle2025/doc/implementation.pdf                                MANAID ensemble is 10.34% higher than that of the


                                                              12
Table 4: Breakdown of Table 1 by decoding strategy. Top: greedy decoding. Bottom: beam search with beam size 4.

                                                         HOL-train                      HOL+AFP-train
                  Method                      HOL-test   AFP-Test Octonions      HOL-test AFP-Test Octonions
                  DeepSeek-coder-1.3B
                  L EMMANAID (types + defs)   28.7%      14.7%       47.1%       29.1%    20.0%     54.0%
                  L EMMANAID (types)          27.3%      15.1%       50.0%       24.4%    19.9%     42.9%
                  L EMMANAID (defs)           23.8%      4.8%        45.1%       24.3%    8.1%      53.1%
                  Neural (types + defs)       23.5%      8.8%        30.0%       26.1%    15.4%     39.7%
                  Neural (types)              20.5%      9.8%        29.4%       24.1%    11.6%     42.9%
                  Neural (defs)               22.8%      3.9%        31.4%       20.8%    5.2%      36.9%
                  L EMMANAID Combined         37.3%      21.0%       58.3%       37.5%    27.3%     61.7%
                  Neural Combined             32.6%      13.7%       44.9%       33.5%    19.7%     51.1%
Greedy decoding




                  Combined                    42.9%      23.5%       62.0%       43.3%    31.0%     66.6%
                  DeepSeek-coder-6.7B
                  L EMMANAID (types + defs)   34.9%      19.8%       60.9%       36.6%    4.7%      62.6%
                  L EMMANAID (types)          31.6%      18.2%       55.7%       31.2%    7.3%      57.7%
                  Neural (types + defs)       30.9%      14.2%       46.9%       16.2%    3.5%      33.7%
                  Neural (types)              29.2%      14.6%       42.9%       8.8%     18.9%     48.0%
                  L EMMANAID Combined         40.5%      23.3%       66.3%       42.4%    10.2%     70.0%
                  Neural Combined             36.0%      18.7%       50.9%       18.0%    20.1%     53.7%
                  Combined                    45.8%      26.7%       70.3%       44.4%    23.2%     74.9%
                  Llama-3.2-1B
                  L EMMANAID (types + defs)   16.3%      9.8%        44.0%       17.1%    12.3%       46.0%
                  L EMMANAID (types)          17.9%      9.9%        44.0%       19.4%    15.2%       49.7%
                  Neural (types + defs)       12.0%      3.6%        23.4%       9.9%     5.6%        12.9%
                  Neural (types)              11.6%      4.4%        23.1%       11.1%    7.1%        20.6%
                  L EMMANAID Combined         23.3%      13.8%       52.0%       24.5%    19.1%       54.3%
                  Neural Combined             17.0%      6.2%        33.4%       15.7%    9.9%        26.9%
                  Combined                    27.6%      15.3%       54.3%       27.9%    21.2%       57.1%
                                                         HOL-train                      HOL+AFP-train
                  Method                      HOL-test   AFP-Test    Octonions   HOL-test AFP-Test Octonions
                  DeepSeek-coder-1.3B
                  L EMMANAID (types + defs)   37.6%      19.1%       52.6%       40.0%    26.6%     63.7%
                  L EMMANAID (types)          35.8%      18.1%       49.7%       33.5%    25.9%     52.9%
                  L EMMANAID (defs)           31.8%      6.8%        49.1%       33.5%    12.3%     58.3%
                  Neural (types + defs)       29.3%      11.5%       31.7%       27.9%    16.7%     45.4%
                  Neural (types)              33.0%      12.5%       42.3%       28.0%    14.1%     44.9%
                  Neural (defs)               30.2%      6.2%        41.4%       24.0%    7.3%      41.7%
                  L EMMANAID Combined         46.8%      25.5%       66.0%       48.2%    34.4%     74.6%
                  Neural Combined             42.1%      17.3%       52.9%       37.3%    22.2%     57.4%
                  Combined                    52.6%      27.9%       69.4%       51.7%    37.2%     79.1%
 Beam search




                  DeepSeek-coder-6.7B
                  L EMMANAID (types + defs)   46.4%      26.2%       68.0%       50.1%    27.8%     76.6%
                  L EMMANAID (types)          43.2%      16.9%       66.9%       36.2%    28.4%     78.3%
                  Neural (types + defs)       42.3%      19.7%       53.1%       22.3%    25.0%     62.3%
                  Neural (types)              38.4%      18.9%       51.1%       38.4%    24.9%     53.1%
                  L EMMANAID Combined         52.1%      28.9%       76.0%       54.2%    34.7%     83.1%
                  Neural Combined             46.8%      23.5%       59.4%       43.2%    31.4%     65.7%
                  Combined                    57.1%      31.9%       79.7%       57.9%    42.5%     84.9%
                  Llama-3.2-1B
                  L EMMANAID (types + defs)   31.3%      17.4%       57.4%       27.3%    17.6%     58.9%
                  L EMMANAID (types)          33.7%      13.6%       59.7%       34.2%    26.8%     64.9%
                  Neural (types + defs)       22.6%      5.4%        40.0%       18.8%    12.5%     32.0%
                  Neural (types)              22.3%      8.5%        42.0%       15.7%    11.1%     27.4%
                  L EMMANAID Combined         38.8%      20.5%       62.6%       37.6%    29.5%     66.6%
                  Neural Combined             28.3%      10.5%       48.0%       23.4%    16.8%     43.4%
                  Combined                    42.1%      21.9%       64.0%       40.1%    32.0%     68.3%
                  QuickSpec                   —          —           22.8%       —        —         22.8%



                                                             13
                          Table 5: Results for the different sessions of the HOL library.


                     HOL session              Lemmas       L EMMANAID          Neural    Combined
                     Algebra                        49              73.47%    67.35%        81.63%
                     Analysis                     1009              41.72%    28.84%        44.80%
                     Auth                          350              61.71%    60.00%        64.29%
                     Bali                          346              40.46%    21.10%        41.62%
                     Cardinals                      93              46.24%    34.41%        46.24%
                     Computational Algebra          50              66.00%    62.00%        66.00%
                     Data Structures                91              74.73%    70.33%        76.92%
                     Datatype Examples             145              53.10%    23.45%        55.17%
                     Decision Procs                240              58.75%    47.08%        60.42%
                     Eisbach                        23               0.00%     0.00%         0.00%
                     ex                             75              41.33%    37.33%        42.67%
                     Hoare                          15              80.00%    66.67%        80.00%
                     HOLCF                          93              61.29%    47.31%        63.44%
                     IMP                           284              89.08%    88.73%        95.07%
                     Imperative HOL                 61              40.98%    27.87%        45.90%
                     IMPP                           26              50.00%    26.92%        53.85%
                     IOA                            20              45.00%    35.00%        50.00%
                     Lattice                        55              61.82%    54.55%        69.09%
                     Library                      1054              54.74%    39.47%        58.25%
                     Matrix LP                      25              24.00%    20.00%        24.00%
                     Metis Examples                  1               0.00%     0.00%         0.00%
                     MicroJava                     178              47.75%    34.27%        51.12%
                     Nominal                       302              81.79%    61.26%        84.44%
                     Nonstandard Analysis           36              75.00%    72.22%        80.56%
                     Number Theory                  47              61.70%    61.70%        72.52%
                     Quotient Examples              18              55.56%    38.89%        55.56%
                     Proofs                          6              33.33%    16.67%        33.33%
                     TLA                             7              57.14%    28.57%        57.14%
                     UNITY                          41              14.63%    19.51%        24.39%


neural ensemble. Their combined success rate is on              ble performs better for two, and in the remaining 6 cases
average 3.00% higher than that of the L EMMANAID                the performance is equally good (0% in five out of six
ensemble, showing that the approaches are somewhat              cases). Note that most of the projects with a success
complementary but mostly overlapping.                           rate of 0% contain a small number of target lemmas
   A clear outlier is the Eisbach session where both            (less than 10), with the outlier being the Actuarial Math-
methods are completely unsuccessful, this is because            ematics formalization. In this case, the syntax used in
the lemmas in that set are all simple example lemmas            the formalization meant that none of the predicted lem-
used to demonstrate the use of the Eisbach proof method         mas were considered syntactically equivalent, however
language (Matichuk et al., 2016). These examples 10             a more thorough evaluation would have shown some of
only contain basic logic symbols which we discard from          them to be semantically equivalent to the target lemmas.
our input symbol set, so our models don’t have any input        On average the L EMMANAID ensemble has a 7.18%
to base their predictions on.                                   better performance than the neural one. Their combined
                                                                success rate is on average 3.52% higher than the one for
D.2   AFP-test                                                  the L EMMANAID ensemble.
For the formalizations included in our test set AFP-
test, Table 6 shows the formalization topic chosen by
                                                                E    Additional Test Set Statistics
the project authors, the number of gold-standard lem-
mas from each project and the lemma success rates (in
                                                                Statistics on HOL-test, AFP-test, and Octonions, and
percentages) of L EMMANAID, neural-only lemma pre-
                                                                the successes of L EMMANAID and neural baselines on
diction, and their combination. The results shown are
                                                                each dataset are shown in Table 7. We count the num-
the ensembles of the different variants of L EMMANAID
                                                                ber of lemmas in each test set (Lemmas), how many of
and the neural baselines, trained on HOL+AFP-train
                                                                them are equational (Eq), and look into the length (in
using DeepSeek-coder-6.7b.
                                                                characters) of lemmas and their templates as well as the
   We can see that out of the 27 tested formalization
                                                                number of different symbols that appear. L EMMANAID
projects, the L EMMANAID ensemble outperforms the
                                                                and neural models here are trained on HOL-train and
neural ensemble on 19 of them, while the neural ensem-
                                                                use greedy decoding, using DeepSeek-coder-6.7b for
  10
     https://isabelle.in.tum.de/library/                        both the neural prediction and the neural engine of L EM -
HOL/HOL-Eisbach/Examples.html                                   MANAID.


                                                           14
                    Table 6: Information about the different formalization projects in AFP-test.


        AFP entry               Topic(s)                    Lemmas        L EMMANAID      Neural    Combined
        ConcurrentHOL           CS/Concurrency                   481           39.71%     28.27%       43.24%
        Sumcheck                CS/Security                       62           67.74%     62.90%       74.19%
        Protocol                CS/Algorithms
        Broadcast Psi           CS/Concurrency                   145           82.07%     69.66%       85.52%
        AutoCorres2             CS/PL                           12721          34.72%     22.48%       37.86%
                                CS/Semantics & reasoning
                                Tools
        Substitutions           Logic/Rewriting                  55            50.91%     21.82%       52.73%
        Lambda-Free
        Doob Convergence        Math/Prob. theory                 2             0.00%      0.00%        0.00%
        Orient Rewrite          Logic/Rewriting                  148           60.14%     42.57%       62.16%
        Rule Undecidable
        Uncertainty             Math/Physics                      3              0.00%     0.00%        0.00%
        Principle
        Derandomization         CS/Algorithms                    15             40.00%    40.00%       40.00%
        with Conditional
        Expectations
        Verified QBF            CS/Algorithms                    171           53.80%     43.86%       57.31%
        Solving                 Logic/General logic
        IMP                     CS/PL                            50            40.00%     38.00%       42.00%
        Noninterference         CS/Security
        Actuarial               Math/Games & econ.               168             0.00%     0.00%        0.00%
        Mathematics
        LL(1) Parser            CS/Algorithms                    205            38.05%    46.83%       55.61%
        Generator               CS/PL
        Schönhage-Strassen     CS/ALgorithms                    128           41.41%     26.56%       43.75%
        Multiplication          Math/Algebra
        Isabelle DOF            CS/Semantics & reasoning         41            53.66%     34.15%       53.66%
        Interval Analysis       Math/Analysis                   694            55.19%     46.83%       58.50%
        MFOTL Checker           CS/Data mgmt systems            2081           14.22%     24.89%       30.71 %
                                CS/Algorithms
                                Logic/General logic
        Decomposition of        Math/Algebra                      1              0.00%     0.00%        0.00%
        totally ordered hoops
        Approximate Model       CS/Algorithms                    112           32.14%     17.86%       34.82%
        Counting
        Wieferich-Kempner       Math/Number theory                8              0.00%     0.00%        0.00%
        Theorem
        PNT with                Math/Number theory               155           35.48%     25.81%       40.00%
        Remainder
        Continued Fractions     Math/Analysis                    428           37.62%     35.75%       43.69%
        CondNormReasHOL         Logic/Phil. aspects               34           11.76%      5.88%       11.76%
                                Logic/General logic
        Region Quadtrees        CS/Data structures               182           41.76%     34.07%       46.15%
        Karatsuba               CS/Algorithms                    431           50.58%     32.25%       55.22%
        Pick’s Theorem          Math/Geometry                    334           19.46%     14.37%       22.46%
        Kummer Congruence       Math/Number theory               120           34.17%     25.83%       38.33%


F   Examples of Generated Conjectures                           the first lemma is identical to the gold-standard lemma
                                                                totient imp prime and the second one doesn’t match
The analysis presented in section 4.3 divides the set of        any formalized lemmas.
conjectures generated by L EMMANAID into true, false,
                                                                lemma “totient x1 = x1 − 1 =⇒ 0 < x1 =⇒
and undecided conjectures. Here, we present some
                                                                prime x1 ”
examples of conjectures in each category.
                                                                lemma “1 ≤ x1 =⇒ 1 ≤ totient x1 ”
True Statements If Sledgehammer succeeds in find-
ing a proof of a given conjecture, it’s considered a            False Statements Conjectures for which Nitpick or
true statement. True statements included both gold-             Quickcheck can find a counter-example are considered
standard lemmas formalized by experts and other other           false statements. For the conjecture below, Quickcheck
true statements not previously formalized. The follow-          finds a counter-example when x1 = 2.
ing two conjectures were discovered by L EMMANAID:              lemma “2 ≤ x1 =⇒ even (totient x1 )”


                                                           15
Table 7: Number of lemmas in each test set, and how many were discovered by L EMMANAID and the corresponding
neural method (using DeepSeek-6.7b and greedy decoding), including how many were equational. The table also
shows information about template and lemma lengths (number of characters) and the number of different symbols
appearing.

                                           Template Length                          Lemma Length             # Symbols
               Lemmas     Eq
                                  Min    25%   Med    75%        Max     Min   25%     Med   75%    Max     Mean    Max
HOL-test       4740       2242    9      49    82     127        9014    7     57      91    150    10454   4.2     100
L EMMANAID     1643       885     11     37    55     85         300     10    45      69    100    368     3.3     15
Neural         1407       750     11     37    55     85         433     11    45      68    98     390     3.3     15
AFP-test       18975      13202   7      39    63     130        10492   7     58      80    141    7530    4.1     31
L EMMANAID     3712       2989    7      25    31     45         220     12    39      55    73     286     2.8     14
Neural         2111       1526    7      23    33     45         184     10    36      52    71     253     2.8     12
Octonions      350        262     17     29    49     75         688     11    33      55    79     391     3.8     21
L EMMANAID     212        152     17     23    43     67         121     11    29      47    65     133     2.7     11
Neural         164        105     19     23    49     67         269     15    25      47    66     279     2.7     11.0



Unresolved Conjectures L EMMANAID generates a                    <definitions for example>
number of conjectures which can’t be automatically cat-          ###output
egorized. This is expected due to the incompleteness             <gold output for example>###end
of the automated reasoning tools we use. These conjec-           ... repeated for five in-context
tures require further complex reasoning to decide if that            examples ...
are true or false. One example of such an unresolved
conjecture generated by L EMMANAID is the monotonic-             ### Now predict
ity of Euler’s function. Nitpick and Quickcheck fail to          ###symbols
                                                                 <query symbol table>
find a counterexample such as x1 = 21, x2 = 22.                  ###defs
lemma “x1 ≤ x2 =⇒ totient x1 ≤ totient x2 ”                      <query definitions>
                                                                 ###output
G     Comparison with Commercial LLMs                             For template prediction, the instruction is:
      Details
                                                                 You are predicting Isabelle/HOL lemma
G.1   Evaluation Sets                                                templates for the Lemmanaid task.
We evaluate commercial models on Octonions and on
                                                                 You will be given a context block
two fresh 2026 AFP entries, Rankings and Swap Dis-                   describing the symbols (with type
tance. The Octonions benchmark is identical to the one               signatures) and definitions
used for evaluating RQ1-2, and it contains 350 data-                 available, then asked to produce a
points. The Rankings and Swap Distance benchmark                     template -- an abstracted Isabelle
                                                                     proof goal where concrete operators
contains 139 datapoints extracted from three source
                                                                     are replaced by placeholders (?H1, ?
theories in an AFP snapshot from 2026-04-26, using                   H2, ...) and bound variables by x_1,
Isabelle2025-2. For each datapoint, the extracted record              x_2, ....
contains the gold-standard lemma object, its abstracted
template, and the symbol, type, and definition informa-          The symbol table determines the
                                                                     placeholder inventory exactly. If
tion used to construct model inputs.
                                                                     there are N listed symbols, your
                                                                     output must use exactly the
G.2   Prompt Format                                                  placeholders ?H1 through ?HN. Every
Each prompt contains an instruction, five in-context ex-             one of ?H1, ?H2, ..., ?HN must
amples, and a final query. Each example provides the                 appear at least once in the final
                                                                     template. No other ?H placeholders
available symbols, relevant definitions, and the desired
                                                                     may appear.
output. The query has the same symbol and definition
fields but leaves the output blank for the model to com-         Below are worked examples from the same
plete.                                                               theory. Then a new context. Output
   The full prompt has the following form:                           ONLY the template followed by ‘###
                                                                     end‘. No prose, no markdown fences.
<task instruction>
                                                                  For direct lemma-object prediction, the instruction is:
### Example <i>
###symbols                                                       You are predicting Isabelle/HOL lemma
<symbol table for example>                                           statements for the Lemmanaid task.
###defs


                                                            16
You will be given a context block                                Figure 3: Output from QuickSpec on Octonions for
    describing the symbols (with type                            multiplication and inverse.
    signatures) and definitions
    available, then asked to produce the
     lemma statement -- a concrete
                                                                   == Functions ==
    Isabelle proof goal using the named                            (*) :: It -> It -> It
    operators from the symbol table and                              1 :: It
    schematic variables (?x, ?y, ...).                             == Laws ==
                                                                     1. x * 1 = x
The symbol table determines the required                             2. 1 * x = x
                                                                     3. (x * x) * y = x * (x * y)
     operator inventory exactly. Every                               4. (x * y) * x = x * (y * x)
    listed symbol must be used at least                              5. (x * y) * y = x * (y * y)
                                                                     6. x * (y * (x * y)) = (x * y) * (x * y)
    once in the final lemma statement,                               7. x * (y * (y * x)) = (x * y) * (y * x)
    either by name or by its standard                                8. x * (y * (y * y)) = (x * y) * (y * y)
    Isabelle notation when appropriate.                              9. x * ((y * z) * x) = (x * y) * (z * x)
                                                                    10. (x * (y * x)) * z = x * (y * (x * z))
    Do not use operators that are not                               11. ((x * y) * z) * y = x * (y * (z * y))
    listed in the symbol table, except
                                                                   == Functions ==
    built-in logical syntax and                                    inv :: It -> It
    schematic variables.
                                                                   == Laws ==
                                                                    12. inv 1 = 1
Below are worked examples from the same                             13. inv (inv x) = x
    theory. Then a new context. Output                              14. x * inv x = 1
                                                                    15. inv x * inv y = inv (y * x)
    ONLY the lemma statement followed by                            16. inv x * (x * y) = y
     ‘###end‘. No prose, no                                         17. x * (y * inv x) = (x * y) * inv x
                                                                    18. (inv x * y) * x = inv x * (y * x)
markdown fences.

G.3   In-context Examples
The prompt generator supports several strategies for             more QuickSpec suffers from combinatorial blowup and
selecting in-context examples. The results reported in           generating uninteresting lemmas.
Table 2 use nearest-example selection. The examples                 In the complex numbers, the functions Re, Im : C →
are drawn from a fixed AFP-train pool to simulate a              R extract the real and imaginary parts of a number
realistic conjecturing setting. Nearestness is measured          respectively. In the octonions, there are eight anal-
by overlap in the Isabelle symbols appearing in the task:        ogous functions Re, Im1 . . . Im7 : O → R. When
for a query with symbol set Q, each candidate example            we added these functions, QuickSpec generated 775
with symbol set S is scored by Jaccard overlap, |Q∩S|
                                                 |Q∪S| .         laws, the vast majority extremely uninteresting for a
                                                                 human. An example of a typical generated law is
H Partial QuickSpec output on Octonions                          Re(x + Im2 y × z) = Re(x + y × Im2 z).
As reported in the main text, QuickSpec generated close             Corresponding to the complex number i there are
to 10,000 lemmas on the Octonions example, so we do              seven octonions e1 . . . e7 which (together with 1) act
not include the full output here. However, we include            as unit numbers. Unfortunately when we add these
the output on a small subset of the Octonions theory to          as constants then QuickSpec starts to generate many
illustrate some of the problems.                                 thousands of irrelevant lemmas. Examples include:
   QuickSpec takes as input a list of function and con-
                                                                       (e5 − e4 ) × (e1 + e4 ) = (1 + e1 ) × (e4 − e1 )
stant symbols out of which it will build the terms. We
started by giving it the functions (with ×, inverse and          and
1). As the inverse of 0 is not defined, we had to in-
struct QuickSpec to only test using non-zero Octonions,            e4 × (Im1 x × Im2 y) = Im7 (Im1 x × (y × e4 ))
a limitation not shared by L EMMANAID. For the same
reason we could not give it the constant symbol 0 or the         The problem is that QuickSpec does not attempt to judge
functions + and −, which would allow it to construct             which lemmas are relevant to a human user.
a zero octonion. The output of QuickSpec is shown in
Figure 3. So far the number of lemmas is manageable
and 9 of the 18 are found in the AFP theory, giving a
precision of 50%.
   Then we ran QuickSpec again, adding the extra func-
tions +, 0, inner product (·) and norm, but removing
the inverse operation (as discussed above). The results
are still reasonable but, especially with the inner prod-
uct function, most of the lemmas are uninteresting, not
found in the AFP theory, and generated only because
they happen to be true (see Figures 4 and 5). In general,
it seems that the more function symbols there are, the


                                                            17
Figure 4: Output from QuickSpec on Octonions with +,
0, inner product (·)


  == Functions ==
  (*) :: It -> It -> It
    0 :: It
    1 :: It

  == Laws ==
    1. x * 0 = 0
    2. x * 1 = x
    3. 0 * x = 0
    4. 1 * x = x
    5. (x * x) * y = x * (x * y)
    6. (x * y) * x = x * (y * x)
    7. (x * y) * y = x * (y * y)
    8. x * (y * (x * y)) = (x * y) * (x * y)
    9. x * (y * (y * x)) = (x * y) * (y * x)
   10. x * (y * (y * y)) = (x * y) * (y * y)
   11. x * ((y * z) * x) = (x * y) * (z * x)
   12. (x * (y * x)) * z = x * (y * (x * z))
   13. ((x * y) * z) * y = x * (y * (z * y))

  == Functions ==
  (+) :: It -> It -> It

  == Laws ==
   14. x + y = y + x
   15. x + 0 = x
   16. (x + x) * y = x * (y + y)
   17. (x + y) + z = x + (y + z)
   18. x * (y + 1) = x + (x * y)
   19. (x + 1) * y = y + (x * y)
   20. (x + x) * (x * y) = (x * x) * (y + y)                Figure 5: Continued output from Figure 4, Octonions
   21. (x + x) * (y * x) = (x * y) * (x + x)
   22. (x + x) * (y * y) = (x * y) * (y + y)
                                                            with +, 0, inner product (·) and norm
   23. (x * y) + (x * z) = x * (y + z)
   24. (x * y) + (z * y) = (x + z) * y
   25. (x + 1) * (x + x) = (x + x) * (x + 1)
   26. x * (y * (x + y)) = (x * y) * (x + y)
                                                              == Functions ==
   27. x * (y + (y * x)) = (x * y) * (x + 1)
                                                              norm :: It -> It
   28. x * (y + (y * y)) = (x * y) * (y + 1)
   29. (x * (x + y)) * y = x * ((x + y) * y)
                                                              == Laws ==
   30. ((x + y) * x) * y = (x + y) * (x * y)
                                                               75. norm 0 = 0
   31. (x + (x * x)) * y = (x + 1) * (x * y)
                                                               76. norm 1 = 1
   32. (x + (y * x)) * y = (y + 1) * (x * y)
                                                               77. norm x = x · x
   33. (x + (x + x)) * y = x * (y + (y + y))
                                                               78. norm (x + (x * x)) = norm (x + norm x)
                                                               79. (x · y) * (z · 1) = z · (x · y)
  == Functions ==
                                                               80. (x · y) · (z · 1) = z · (x · y)
  (·) :: It -> It -> It
                                                               81. norm (norm x + (y * z)) = norm (norm x + (z * y))
                                                               82. (norm x + norm y) * z = z * (norm x + norm y)
  == Laws ==
                                                               83. x · (y * (z · 1)) = z · (x · y)
   34. x · y = y · x
                                                               84. (x * (y · 1)) · z = y · (x · z)
   35. x · 0 = 0
                                                               85. norm x * (1 + norm y) = norm x + norm (x * y)
   36. 1 · 1 = 1
                                                               86. norm x · (1 + norm y) = norm x + norm (x * y)
   37. (x · y) * z = z * (x · y)
                                                               87. norm (x * (x + norm x)) = norm (norm x * (x + 1))
   38. x · (y * x) = x · (x * y)
   39. x · (y + y) = y · (x + x)
   40. x · (y · y) = y · (x * y)
   41. x · (y · 1) = y · (x · 1)
   42. 1 · (x * y) = 1 · (y * x)
   43. 1 · (x · y) = x · y
   44. 1 · (x + 1) = 1 + (x · 1)
   45. (x · y) + (x · z) = x · (y + z)
   46. (x * y) · (x * z) = (x · x) * (y · z)
   47. (x * y) · (z * y) = (x · z) * (y · y)
   48. (x * y) · (y + x) = (y * x) · (y + x)
   49. (x * y) · (z · w) = (y * x) · (z · w)
   50. (x · y) · (z · w) = (x · y) * (z · w)
   51. (x + x) * (x · 1) = (x * x) + (x · x)
   52. (x · y) * (z · 1) = z · (x · y)
   53. (x * y) · (y + 1) = (y * x) · (y + 1)
   54. (x · y) · (z · 1) = z · (x · y)
   55. (1 + 1) · (1 + 1) = (1 + 1) * (1 + 1)
   56. x * (y * (z · w)) = (x * y) * (z · w)
   57. (x * (y · z)) * w = (x * w) * (y · z)
   58. (x + (y · z)) * x = x * (x + (y · z))
   59. x · (y * (z * x)) = (y * z) · (x · x)
   60. x · (y * (z · w)) = (x · y) * (z · w)
   61. x · ((x * y) * z) = (y * z) · (x · x)
   62. x · ((y * x) * z) = x · (y * (x * z))
   63. x · ((x + y) * y) = x · (y * (x + y))
   64. x · (y + (z * x)) = x · (y + (x * z))
   65. x · (y + (x · x)) = x · (y + (x * x))
   66. x · (y + (x · y)) = (x + 1) · (x · y)
   67. x · (y + (y · y)) = y · (x + (x * y))
   68. x · (y · (z * y)) = z · (y · (x * y))
   69. x · (y · (z · w)) = y · (x · (z · w))
   70. x · (y + (y + y)) = y · (x + (x + x))
   71. x · (y * (z · 1)) = z · (x · y)
   72. 1 · ((x * y) * z) = 1 · (x * (y * z))
   73. (x * (y · 1)) · z = y · (x · z)
   74. x · (y + (y · 1)) = y · (x + (x · 1))




                                                       18
