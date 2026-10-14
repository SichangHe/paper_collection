                                                   A New Approach Towards Autoformalization


                                                                Nilay Patel                                   Rahul Saha
                                                     Department of Computer Science                   rsaha@alumni.princeton.edu
                                                    University of California, Santa Cruz
                                                             nilay@ucsc.edu

                                                                                     Jeffrey Flanigan
arXiv:2310.07957v3 [cs.CL] 9 Jul 2024




                                                                             Department of Computer Science
                                                                            University of California, Santa Cruz
                                                                                  jmflanig@ucsc.edu



                                                                                         Abstract

                                                    Verifying mathematical proofs is difficult [15], but can be automated with the
                                                    assistance of a computer. Autoformalization is the task of automatically translating
                                                    natural language mathematics into a formal language that can be verified by a
                                                    program. This is a challenging task, and especially for higher-level mathematics
                                                    found in research papers. Research paper mathematics requires large amounts of
                                                    background and context. In this paper, we propose an avenue towards tackling
                                                    autoformalization for research-level mathematics, by breaking the task into easier
                                                    and more approachable subtasks: unlinked formalization (formalization with un-
                                                    linked definitions and theorems), entity linking (linking to the proper theorems and
                                                    definitions), and finally adjusting types so it passes the type checker. In addition, we
                                                    present arXiv2Formal,1 a benchmark dataset for unlinked formalization consisting
                                                    of 50 theorems formalized for the Lean theorem prover [8] sampled from papers
                                                    on arXiv.org.


                                        1       Introduction
                                        Mathematics is a notoriously difficult, and introducing even one false theorem can invalidate all
                                        follow-up work. Discounting the time it takes to prove results, it often takes many months or years
                                        to verify the result and have it accepted by the community. Still, mistakes can be made and even
                                        seemingly simple ones can be difficult to find. One famous example is a mistake in knot theory which
                                        went uncorrected for nearly 100 years.2
                                        Using proof assistants to verify proofs is effective, but requires the mathematics to be written
                                        in a formal language as opposed to the natural language humans use. Formalizing natural lan-
                                        guage mathematics has a high barrier to entry, even for mathematicians, and remains difficult and
                                        time-consuming once learned. To mitigate these high costs, research in automatic formalization
                                        (autoformalization) and automatic theorem proving has been increasingly popular in recent years
                                        [21, 24, 22, 10, 3, 13, 23, 1], in part due to major advances in natural language processing (NLP)
                                        such as the introduction of large language models (LLMs) [4]. A high-quality autoformalization tool
                                        would alleviate many downsides of theorem provers while maintaining their benefits.
                                        However, there are still many challenges faced in the development of such an autoformalization
                                        tool, such as the intrinsic difficulty of the domain and severe lack of high-quality data. Previous
                                            1
                                                https://github.com/jlab-nlp/arxiv2formal
                                            2
                                                https://mathoverflow.net/a/9059


                                        Preprint. Under review.
work [3, 23, 24, 12, 9] introduce datasets for this and other related tasks, but these works either are
not parallel corpora needed for building a supervised model, or focus on "easier" domains, such as
olympiad-style or undergraduate mathematics.3 While a useful stepping stone, they are far removed
from "real world" mathematics which requires far more context and background material for theorems.
One attempt at this task was Formal Abstracts [1], a project intending to formalize the main theorem
of papers from arXiv, but progress on this project has ceased, which we speculate is partly due to the
monumental challenge straight formalization of high-level mathematics poses (see § 2).
Another looming issue with previous approaches to autoformalization is scalability. Much of the
difficulty in formalization comes from the necessity for the foundations of the theory to be general
and broadly applicable. Formalization for well-understood areas of mathematics can take years to
develop; some areas of undergraduate mathematics remain incomplete [16]. Even a single theorem in
high-level mathematics can take years to properly formalize [5].4 Current work on autoformalization
assumes that definitions and types are decided ahead of time by annotators, which is burdensome and
potentially inhibitory to large-scale annotation projects.
To tackle higher-level mathematics, we propose breaking the task of autoformalization down into
easier subtasks to better leverage the powerful tools from NLP. Furthermore, we release a beta version
of arXiv2Formal, a benchmark dataset for the first subtask, with 50 examples (and growing). For
this work, we use Lean 3 [8], but a similar technique could be adapted for others. We also plan to
release a version of the dataset in Lean 4.
At a high level, our subtasks to autoformalization are as follows:

      1. Formalize Theorems (Unlinked): Translate natural language theorem statements into
         syntactically correct but not necessarily semantically valid Lean. In this intermediate step,
         we allow references to variables, functions, or other theorems which don’t yet exist.
      2. Formalize Definitions (Unlinked): Translate definitions of functions, variables, etc. from a
         paper into a "library" which can be referenced by theorems. These definitions should be
         recursively constructed using a base library (e.g., Lean’s mathlib [16]).
      3. Entity Linking: Link referenced names to the definitions in the library from step 2. Since
         steps 1 and 2 generate names automatically, this step is necessary to resolve coreferences.
      4. Adjust Types: Postprocess the generated translations with the assistance of the Lean type
         checker to ensure types are aligned. This also may involve adjusting type signatures to add
         arguments to definitions which, in text, don’t appear to need any, but are necessary in a
         formal setting.

Note that theorem proving poses its own (separate) challenges compared to theorem formalization.
For this work, we focus on the previous four tasks and leave theorem proving for future work.
The rest of the paper is organized as follows. First, we discuss some related work (§ 2), then we
describe our proposed approach and reasoning (§ 3), and finally we provide a benchmark dataset for
the first subtask (§ 4).

2   Related Work
Several papers have been published recently in autoformalization and theorem proving [9, 12, 3, 24,
13, 11], but current research on autoformalization is limited by a small amount of high-quality data.
Of note, miniF2F [24] contains 488 formalized olympiad problems in Lean and three other languages.
Codex [6] and other LLMs have been effective in autoformalization for this dataset, achieving over
25% exact translation accuracy [22].
ProofNet [3] is another dataset consisting of 371 formal/informal undergraduate math problems in
Lean 3. In addition to the dataset, the authors also describe two techniques which improve LLM
autoformalization and theorem proving performance, prompt retrieval and distilled backtranslation.
Other work with applying LLMs to autoformalization [22, 10, 2] have shown promising results. The
    3
      These domains are still unsolved and are by no means easy, but pose fewer challenges than higher-level
mathematics.
    4
      It took a team over 1.5 years to formalize the prove a single theorem in the Liquid Tensor Experiment
[5, 19, 7].


                                                     2
Figure 1: An example of our proposed autoformalization process, starting from LaTeX theorems
(top left red) and definition (top right red) and ending with formalized Lean code (bottom). In step 1
(top left), despite lacking context for the set X, the definitions of flubs and glibs, and the function f ,
we are still able to make a plausible translation which we can fill in later. In step 2 (top right), we
formalize definitions and determine the correct types of objects. Note that the translations are still not
correct, since the type of X hasn’t been applied to the other definitions or theorems yet. In step 3
(bottom), we fix this by linking the referenced name X with the generated type X, and we also align
the names of other mismatched functions.


authors of ProofNet also released an LLM pretrained on the proof-pile [3], a large corpus of math
theorems and proofs, which may further improve performance of autoformalization with LLMs.
Interestingly, an error analysis from [22] showed that a majority of the autoformalization errors on
the minif2f dataset were due to an inability to link natural language and formal definitions. In our
proposed task, this failure case would be handled by the linking in step 3, which should significantly
improve overall performance.

3   Our Approach to Autoformalization
We propose to break autoformalization into four subtasks, each of which are easier than the original
task.

      1. Formalize Theorems (Unlinked). Previous work [22] has shown promising results in the
         use of LLMs for autoformalization. A major problem, however, is high-level mathematics
         often requires a large amount of context even for short theorems. To simply the problem,
         we propose separating the tasks of (1) translating theorems to a formal language with
         placeholder names and (2) linking the placeholders to the actual definitions. See Figure 1
         for an example.
      2. Formalize Definitions (Unlinked). Similar to theorems, definitions often require prior
         context and thus need to be constructed iteratively. However, even without context, we can
         use the same approach as above and formalize the definition with placeholder names.
      3. Link Entities. Unlinked formalization in steps 1 and 2 result in list of theorems and
         definitions, but the identifiers are not necessarily aligned. For example, a theorem may
         reference a vector space, but mathlib does not define vector spaces, and instead uses a
         module over a field. The reference to a vector space needs to be linked to mathlib’s module
         definition. While still challenging, entity linking and coreference resolution is a well-studied
         field in NLP, and we plan to adapt and leverage prior work for this task.
      4. Adjust Types. This last step is a catch-all for any processing that requires the assistance
         of the Lean type system, such as correcting type misalignment. In practice, what this step
         entails is dependent on the output of the previous three steps. As an example, if a theorem
         references a vector space without specifying the field, but we linked it to mathlib’s module


                                                    3
         definition, which requires a specified field, we would need to add the field argument to
         correct the types.


4     Benchmark Dataset: arXiv2Formal

To facilitate progress towards subtask 1, we release a benchmark dataset of 50 theorems in LaTeX
and Lean 3 sampled from a random subset of mathematics papers from arXiv.org. On average,
our natural language theorems consisted of 140 tokens compared to 113 tokens for the formalized
versions. Currently, arXiv2Formal is a beta release and will be updated regularly as more examples
are annotated. For examples, see Appendix A.
We construct the dataset in a semi-automated manner. We formalize the theorems first automatically
via prompting GPT-3.5 turbo [17] and manually correcting any mistakes in the automatic translation.
As more translations are completed, we use them to improve the quality of future translations by
selecting them as examples for the prompt. We observe that the amount of human correction work
lessens as the dataset becomes larger because the prompts become better (Table 1).


                                                     Model       BLEU ↑     TER ↓     TrueSkill ↑
                                                     GPT-3.5     17.2       140.5     10.9
                                                     +ICL 1      31.9       93.4      25.4
                                                     +ICL 5      37.5       85.7      28.0,
                                                     +ICL 10     41.7       83.9      33.1

                                                  Table 1: Performance of GPT-3.5 turbo (16k) on
                                                  arXiv2Formal with varying number of examples
                                                  for in-context learning (ICL). Adding just a few ex-
                                                  amples to show the model the expected format sig-
                                                  nificantly improves BLEU score, showing promis-
Figure 2: Distribution of topics of formalized    ing results for this subtask.
theorems in arXiv2Formal.


Evaluation We evaluate using common NLP automatic metrics such as BLEU [18] and Translation
Error Rate (TER) [20], as well as human evaluations. In a small-scale experiment of 10 examples, we
compared model outputs with varying BLEU and Translation Error Rate (TER) scores, and found that
an increase in these scores strongly correlates with better human evaluation of the output (R = .99).
For the future, we suggest evaluation with automatic metrics combined with a human evaluation.


4.1   Experiments with GPT-3.5

We experimented with unlinked-autoformalization for arXiv2Formal using GPT-3.5 [17]. GPT-3.5
likely contains training data from mathlib, and without any prompting, it formalizes statements in
a very similar way to theorems found there. With few-shot in-context learning, performance on
arXiv2Formal increased noticeably (Table 1).
GPT-3.5 was highly effective in assisting our formalization. However, the naive method we used for
these baseline results made several mistakes. One common mistake is that GPT often attempts to
guess the type of referenced objects based on insufficient context. While it was sometimes correct
(e.g., seeing familiar vocabulary and LaTeX formatting, it guesses that V is a vector space), it
hallucinates regularly and mistypes in most cases. In our proposed autoformalization approach, these
errors will be fixed later when more context is available to adjust types in step 4.
One of the more difficult cases which GPT struggled to handle is multipart theorems. In many cases,
each part requires different or mutually exclusive conditions which makes formalizing it as a single
theorem awkward and unwieldy. A much more natural approach is to split the theorem into multiple
parts, though this introduces another challenge of automatic theorem splitting.


                                                 4
5   Conclusion
Previous work in autoformalization largely focuses on "easier" domains such as olympiad or un-
dergraduate math. Higher-level mathematics requires far more background and context for each
theorem and thus requires a new approach. We propose breaking the task down autoformalization
into four more manageable subtasks: (1) formalizing theorems (unlinked), (2) formalizing definitions
(unlinked), (3) linking identifiers and references, and (4) adjusting types. While still difficult, each
subtask is much easier to tackle in isolation than the full task and allows for cheaper data collection.
We hope to stimulate research along this path, and provide arXiv2Formal, a dataset of 50 machine-
assisted human-annotated LaTeX/Lean 3 theorems as a benchmark for subtask 1. We welcome any
contributions to future versions of this dataset.

References
 [1] Formal abstracts. {MSWindowsNT}KernelDescription.
 [2] Ayush Agrawal, Siddhartha Gadgil, Navin Goyal, Ashvni Narayanan, and Anand Tadipatri.
     Towards a mathematics formalisation assistant using large language models. (arXiv:2211.07524),
     Nov 2022. URL http://arxiv.org/abs/2211.07524. arXiv:2211.07524 [cs].
 [3] Zhangir Azerbayev, Bartosz Piotrowski, and Jeremy Avigad. Proofnet: A benchmark for
     autoformalizing and formally proving undergraduate-level mathematics problems. NeurIPS
     2022.
 [4] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal,
     Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel
     Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M.
     Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz
     Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec
     Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners, 2020.
 [5] Davide Castelvecchi et al. Mathematicians welcome computer-assisted proof in ‘grand unifica-
     tion’theory. Nature, 595(7865):18–19, 2021.
 [6] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Pondé de Oliveira Pinto, Jared
     Kaplan, Harrison Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul
     Puri, Gretchen Krueger, Michael Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke
     Chan, Scott Gray, Nick Ryder, Mikhail Pavlov, Alethea Power, Lukasz Kaiser, Mohammad
     Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such, Dave Cummings, Matthias
     Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen Guss, Alex
     Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain,
     William Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Joshua Achiam, Vedant
     Misra, Evan Morikawa, Alec Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie
     Mayer, Peter Welinder, Bob McGrew, Dario Amodei, Sam McCandlish, Ilya Sutskever, and
     Wojciech Zaremba. Evaluating large language models trained on code. CoRR, abs/2107.03374,
     2021. URL https://arxiv.org/abs/2107.03374.
 [7] Mathlib Community. Completion of the liquid tensor experiment, Jul 2022. URL https:
     //leanprover-community.github.io/blog/posts/lte-final/.
 [8] Leonardo Mendonça de Moura, Soonho Kong, Jeremy Avigad, Floris van Doorn, and Jakob
     von Raumer. The lean theorem prover (system description). In CADE, 2015. URL https:
     //api.semanticscholar.org/CorpusID:232990.
 [9] Chelsea Edmonds. Hypergraphs. Archive of Formal Proofs, September 2023. ISSN 2150-914x.
     https://isa-afp.org/entries/Hypergraph_Basics.html, Formal proof development.
[10] Siddhartha Gadgil, Anand Rao Tadipatri, Ayush Agrawal, Ashvni Narayanan, and Navin Goyal.
     Towards automating formalisation of theorem statements using large language models.
[11] Jesse Michael Han, Jason Rute, Yuhuai Wu, Edward W. Ayers, and Stanislas Polu. Proof artifact
     co-training for theorem proving with language models. (arXiv:2102.06203), Mar 2022. URL
     http://arxiv.org/abs/2102.06203. arXiv:2102.06203 [cs].


                                                   5
[12] Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn
     Song, and Jacob Steinhardt. Measuring mathematical problem solving with the math dataset.
     arXiv preprint arXiv: 2103.03874, 2021.
[13] Albert Q. Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik,
     Timothée Lacroix, Yuhuai Wu, and Guillaume Lample. Draft, sketch, and prove: Guiding
     formal theorem provers with informal proofs. (arXiv:2210.12283), Feb 2023. URL http:
     //arxiv.org/abs/2210.12283. arXiv:2210.12283 [cs].
[14] Laura Luzzi, Stefano Marmi, Hitoshi Nakada, and Rie Natsui. Generalized brjuno functions
     associated to α-continued fractions. arXiv preprint arXiv: Arxiv-0705.1690, 2007.
[15] Dana Mackenzie. The poincaré conjecture–proved. Science, 314(5807):1848–1849, 2006. doi:
     10.1126/science.314.5807.1848. URL https://www.science.org/doi/abs/10.1126/
     science.314.5807.1848.
[16] The mathlib Community. The lean mathematical library. In Proceedings of the 9th ACM
     SIGPLAN International Conference on Certified Programs and Proofs, CPP 2020, page 367–381,
     New York, NY, USA, 2020. Association for Computing Machinery. ISBN 9781450370974. doi:
     10.1145/3372885.3373824. URL https://doi.org/10.1145/3372885.3373824.
[17] OpenAI. Chatgpt, 2020. URL https://www.openai.com/research/chatgpt.
[18] Kishore Papineni, Salim Roukos, Todd Ward, and Wei-Jing Zhu. Bleu: a method for automatic
     evaluation of machine translation. In Proceedings of the 40th Annual Meeting of the Association
     for Computational Linguistics, pages 311–318, Philadelphia, Pennsylvania, USA, July 2002.
     Association for Computational Linguistics. doi: 10.3115/1073083.1073135. URL https:
     //aclanthology.org/P02-1040.
[19] Peter Scholze. Liquid tensor experiment, Dec 2020. URL https://xenaproject.
     wordpress.com/2020/12/05/liquid-tensor-experiment/.
[20] Matthew Snover, Bonnie Dorr, Rich Schwartz, Linnea Micciulla, and John Makhoul. A study
     of translation edit rate with targeted human annotation. In Proceedings of the 7th Conference of
     the Association for Machine Translation in the Americas: Technical Papers, pages 223–231,
     Cambridge, Massachusetts, USA, August 8-12 2006. Association for Machine Translation in
     the Americas. URL https://aclanthology.org/2006.amta-papers.25.
[21] Christian Szegedy, editor. A Promising Path Towards Autoformalization and General Artificial
     Intelligence, 2020.
[22] Yuhuai Wu, Albert Q. Jiang, Wenda Li, Markus N. Rabe, Charles Staats, Mateja Jamnik, and
     Christian Szegedy. Autoformalization with large language models. (arXiv:2205.12615), May
     2022. URL http://arxiv.org/abs/2205.12615. arXiv:2205.12615 [cs].
[23] Kaiyu Yang, Aidan M. Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu, Saad
     Godil, Ryan Prenger, and Anima Anandkumar. Leandojo: Theorem proving with retrieval-
     augmented language models. arXiv preprint arXiv: 2306.15626, 2023.
[24] Kunhao Zheng, Jesse Michael Han, and Stanislas Polu. Minif2f: a cross-system benchmark for
     formal olympiad-level mathematics. arXiv preprint arXiv:2109.00110, 2021.




                                                 6
A    Appendix: Dataset Examples


     Natural Language        Lemma. For any irrational number x, x is a Brjuno number
                             if and only if x and −x are semi-Brjuno numbers.

                              lemma theorem_two
                                ( x : R) ( hx : ¬ is_rational x ) :
     Formalized (Human)         is_brjuno x ↔
                                ( is_semi_brjuno x ∧ is_semi_brjuno ( - x ))
                                := sorry

                              lemma theorem_two
                                ( x : irrational_number ) :
     Formalized (GPT-3.5)       is_brjuno_number x ↔
                                ( is _se mi_brj uno_n umber x ∧
                                  i s_ semi_b rjuno _numbe r ( - x ))
                                := sorry


Figure 3: An example pair from an arXiv paper ([14]) from the benchmark dataset and its formalized
versions. Note that we don’t know the definitions of semi-Brjuno and Brjuno, but we are still able to
formalize the theorem with placeholders.




                                                 7
     Natural Language          Lemma. Let G be a finitely generated group with finite generating
                               set S and the associated word length metric. Then the following are
                               equivalent:
                                     1. G is amenable;
                                     2. For any ε > 0, there exists a function f ∈ ℓ2 (G)1,+ such
                                        that ∥f − s · f ∥2 ≤ ε for any s ∈ S and supp(f ) is
                                        finite.

     Formalized (Human)
                               lemma p rop_hu lanic ki_rei ter
                                 ( G : Type *) [ group G ]
                                 ( S : finset G )
                                 ( hS : fi nite_g enera ting_s et S )
                                 ( word_length : word_length_on G S ) :
                                 amenable G ↔
                                    (∀ (ε : R) ( hε : ε > 0) ,
                                      ∃ ( f : G → R) ( hf : f ∈ l2 G)
                                        ( hf_pos : ∀ ( g : G ) , g ̸= 1 → f g > 0) ,
                                        (∀ ( s : G ) , s ∈ S →
                                           ∥f - (λ ( g : G ) , f ( s ∗ g ))∥2 ≤ ε)
                                           ∧ ( set . finite ( function . support f )))
                                 := sorry


     Formalized (GPT-3.5)
                               lemma p rop_hu lanic ki_rei ter
                                 ( G : Type *) [ group G ]
                                 ( S : finset G )
                                 ( hS : fi nite_g enera ting_s et S )
                                 ( word_length : word_length_on G S ) :
                                 ( amenable G ) ↔
                                    (∀ (ε : R) ( hε : ε > 0) ,
                                      ∃ ( f : G → C) ( hf : f ∈ l2_1_plus G )
                                        ( hf_pos : ∀ ( g : G ) , g ̸= 1 → f g > 0) ,
                                        (∀ ( s : S ) ,
                                           norm_l2 (f -( s * f )) ≤ ε)
                                           ∧ ( finite_support f ))
                                 := sorry




Figure 4: An example pair from an arXiv paper ([14]) from the benchmark dataset and its formalized
versions. In this more complicated case, GPT is still able to correctly translate several pieces of the
theorem. One mistake is the fact that f should have a range of C rather than R, but this is a mistake
that will be corrected in stage 4 (entity linking). The use of ∥ . . . ∥2 instead of our preferred norm_l2
is due to the prevalence of this notation in the pretraining corpus.




                                                    8
