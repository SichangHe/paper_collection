                                          A Proof-of-Concept for Explainable Disease Diagnosis
                                                   Using Large Language Models and
                                                       Answer Set Programming
                                                                         IOANNA GEMOU AND EVANGELOS LAMPROU
arXiv:2512.23932v1 [cs.AI] 30 Dec 2025




                                                 Abstract. Accurate disease prediction is vital for timely intervention, effective treatment, and
                                                 reducing medical complications. While symbolic AI has been applied in healthcare, its adoption
                                                 remains limited due to the effort required for constructing high-quality knowledge bases. This work
                                                 introduces McCoy, a framework that combines Large Language Models (LLMs) with Answer Set
                                                 Programming (ASP) to overcome this barrier. McCoy orchestrates an LLM to translate medical
                                                 literature into ASP code, combines it with patient data, and processes it using an ASP solver to
                                                 arrive at the final diagnosis. This integration yields a robust, interpretable prediction framework that
                                                 leverages the strengths of both paradigms. Preliminary results show McCoy has strong performance
                                                 on small-scale disease diagnosis tasks.


                                                                                         1. Introduction
                                            Getting an accurate diagnosis quickly can make all the difference in patient outcomes, but building
                                         automated systems that practitioners can trust is still a major challenge [1]. Symbolic AI, and in
                                         particular Answer Set Programming (ASP), provides clear logical reasoning [2, 3] and has seen
                                         success in the medical domain [4]. However, its adoption has been limited because constructing and
                                         maintaining large, domain-specific knowledge bases is very labor-intensive. On the other hand, Large
                                         Language Models (LLMs) have shown strong results on tasks such as medical question answering
                                         and clinical note summarization [5, 6, 7], but their tendency to produce inconsistent or opaque
                                         outputs makes them risky for clinical use [8, 9, 10].
                                            There is an acute need for clinical support systems that are both interpretable and widely
                                         applicable. McCoy takes a step in that direction by combining the strengths of LLMs and ASP.
                                         Instead of requiring experts to hand-craft large knowledge bases, McCoy automatically converts
                                         medical literature into ASP rules. These rules are then enriched with patient symptoms and clinical
                                         indicators, and passed through an ASP solver to produce diagnostic suggestions together with
                                         logical justifications. On public datasets, McCoy reaches 95–100% predictive accuracy on selected
                                         diseases, while giving transparent explanations for each diagnosis.
                                            The paper begins with background on LLMs and ASP (section 2), then details the McCoy
                                         framework (section 4), evaluates the approach on patient data (section 5), and concludes with a
                                         discussion of limitations and future directions (section 6).

                                                                                          2. Background
                                         Large Language Models. LLMs are advanced computational systems designed to understand
                                         and generate human language [11]. These models can produce text that closely mirrors human
                                         linguistic patterns and have emergent reasoning capabilities [12]. Recent models such as GPT-
                                         5 [13] have been trained on massive corpora spanning diverse domains, enabling them to acquire
                                         broad, cross-disciplinary knowledge. To give an intuition of the way they operate, LLMs are

                                            Originally submitted as part of a university research competition on 1st June 2023. Both authors were students at
                                         the University of Patras, Greece, at the time.
                                                                                                    1
2                             IOANNA GEMOU AND EVANGELOS LAMPROU


deep neural networks that have converged to transformer networks [14], which are trained using
self-supervised learning [15]. During training, these models refine an internal representation that
enables them to analyze and understand the relationships between words, phrases, and sentences. By
capturing patterns and structures in the training data, they can then be probed to generate coherent
and relevant responses based on given prompts. The term “large” often refers to models with a
large number of parameters (often in the billions) that allow these models to build high-quality
representations of language. At a very basic level, an LLM is able to predict the next word (referred
to as a token) based on its preceding context.
   LLMs have demonstrated strong performance across a variety of natural language tasks, includ-
ing question answering [16], summarization [17], dialogue generation [18], and program synthesis
[19]. In specialized domains such as biomedicine, domain-adapted LLMs have been employed for
clinical decision support [6] and biomedical knowledge retrieval [20]. Among their capabilities,
LLMs excel at transforming text from one representation to another [14, 21]. This characteristic is
particularly relevant to the present work, which focuses on the effective encoding of medical literature.

Challenges in applying LLMs. However, LLMs are not without errors [22, 23]. They can
occasionally produce incorrect or nonsensical responses [24]. There have been efforts to mitigate
these issues through data preprocessing techniques and fine-tuning [25]. Ongoing research seeks to
improve the factual accuracy, safety, and interpretability of these models, enabling their deployment
in high-stakes environments [26]. This work specifically tackles this issue by grounding LLM outputs
on real medical knowledge, and having an ASP solver provide further validation and explainability.

Answer Set Programming. Answer Set Programming (ASP) [27] is a declarative problem-solving
paradigm rooted in logic programming and non-monotonic reasoning [2]. The formal semantics of
stable models and the foundational ASP language were first introduced by Gelfond and Lifschitz
[28]. These are implemented in a family of languages commonly known as AnsProlog [29].
   The central idea of ASP is to represent a problem declaratively using logical rules, facts, and
constraints. These elements collectively form a program that describes the conditions any solution
must satisfy. Given a valid program, an ASP solver processes it to compute one or more stable
models (also known as answer sets), each of which corresponds to a solution that satisfies all the
given rules and constraints.
   In traditional programming, transitioning from a problem to a solution requires the programmer’s
thorough understanding of the given problem, followed by the creation of a program that will take
as input an instance of the problem, and produce output which will then be interpreted as the
solution. In ASP, the process of deriving solutions from a problem specification typically follows
a sequence of well-defined steps [30], as illustrated in fig. 1. First, the problem is modeled using
the ASP language. Next, a grounder (e.g., gringo [31]) transforms the program into a set of basic
rules and facts. Finally, a solver (e.g., clasp [32]) computes the stable models (answer sets), which
correspond to the solutions of the original problem.
   Several solvers for ASP have been developed, with some seeing industrial adoption [33, 31]. This
work uses the Clingo ASP system, which integrates the gringo grounder [31] and the clasp solver
[32] into a single pipeline. The Clingo system also offers a powerful Python API, enabling integration
into other applications.

                                         3. Related work
ASP for disease diagnosis. ASP has been used in the past to represent and reason over medical
knowledge in a declarative, logic-based manner. Early work applied ASP to biomedical ontologies and
structured databases to answer complex diagnostic and pharmacological queries with interpretable
logical justifications [34]. In the clinical domain, ASP is especially effective for encoding medical
rules and patient-specific data, enabling precise and explainable decision-making [4]
                  A POC FOR EXPLAINABLE DISEASE DIAGNOSIS USING LLMS & ASP                          3



              Problem                                                      Solution


                   Modeling                                        Interpreting
                                            Solving
                                             Grounding
              Program          Grounder                   Solver        Stable Models


       Figure 1. Solving a problem with ASP. A problem is first modeled as a program,
       then transformed into ground rules by a grounder. A solver computes the stable
       models, which are interpreted as solutions.


   Two common strategies illustrate the role of ASP in medical reasoning. The first is rule-based
representation, where medical knowledge is expressed as logical statements that capture relationships
among symptoms, diseases, treatments, and patient data. For instance, a rule might specify that if
a patient exhibits certain symptoms, this supports or excludes the presence of particular diseases.
The second is knowledge base construction, where facts, rules, and constraints are combined into
structured repositories that consistently model diagnostic criteria, symptom–disease associations,
and therapeutic protocols in an extensible way. This work builds on these foundations and works
towards closing the gap with fully automated knowledge-base construction.

Integrating LLMs with ASP. There has been work that explores the synergy between LLMs
and ASP for enhanced diagnostic reasoning. These hybrid approaches aim to combine the language
understanding of LLMs with the precision and explainability of symbolic reasoning. A YAML-based
interface has been proposed to guide LLMs in extracting structured facts from natural language,
which are then processed by ASP for logical inference [35]. Other work uses ASP to validate and
trace misleading or inconsistent outputs from LLMs in medical contexts [36]. Another work leverages
smaller-sized LLMs and uses fine-turning to enhance their performance in generating valid ASP
programs [37]. These works share several of the same insights and motivations as McCoy.


                                        4. Methodology
Architecture. Figure 2 illustrates McCoy’s architecture, which transforms unstructured medical
text into a structured knowledge base. The process begins with the collection of medical literature
relevant to the diseases or conditions of interest. A carefully designed prompt is then used to guide
an LLM in translating this literature into ASP code, which is incorporated into a growing knowledge
base. This knowledge base is further enriched with patient-specific information such as symptoms
and examination results. An ASP solver subsequently reasons over the combined knowledge base
and produces a set of plausible diagnoses.
Prompt Construction. While Large Language Models exhibit strong instruction-following capa-
bilities, their reliability in high-stakes domains remains limited [38]. To improve robustness, a wide
range of prompting strategies are employed by McCoy [39, 40]. In McCoy, carefully designed
prompts are employed to guide the model in translating medical literature. This involves a careful
and accurate description of the desired output format, and specific instructions on the kind of
information to encode within it. Figure 3 represents an example of a poorly constructed prompt
that fails to yield satisfactory results, and fig. 4 shows the prompt that McCoy ultimately uses to
convert medical text into ASP code.
4                                     IOANNA GEMOU AND EVANGELOS LAMPROU



    Prompt
    “Convert the following
    medical literature into
    ASP code..”                                  ASP             Knowledge             ASP
                                 LLM                                                           Diagnosis
                                               Program             Base               Solver

          Medical             Patient Data
         Literature


              Figure 2. McCoy overview. The diagnostic process begins by transforming
              medical literature into an ASP program using a LLM. An ASP solver then executes
              the program and produces a final diagnosis based on each patient’s data.


    !
         Prompt: Medical Text...
         The paragraph above lists common symptoms of pneumonia. Write a clingo script that diagnoses
         pneumonia based on these symptoms.

    LLM Output

         symptom(cough).
         symptom(cough_with_mucus).
         symptom(chest_pain).
         symptom(headache).
         ...

         diagnosis(pneumonia) :- symptom(cough),
                                 symptom(chest_pain),
                                 symptom(headache),
                                 symptom(arthralgia),
                                 ...


              Figure 3. A prompt that does not yield satisfactory results. The LLM output does
              not decompose the disease diagnosis into discrete rules.


Logical Program Construction. The knowledge base is initialized with a set of symptoms and
medical indicators represented as:
(1)                               symptom(s). s ∈ {cough, chest pain, rash, . . . }
(2)                                indicator(i). i ∈ {low MCV, high TIBC, . . . }
Let S denote the set of symptoms and I the set of indicators. A patient exhibiting a specific
symptom or testing positive for an indicator is represented as:
(3)                                               has(x). x ∈ S ∪ I
        Logical rules used for inferring diagnoses follow this general form:
(4)                                  diagnosis(d1 ) ←− has(x1 ) ∧ has(x2 ) ∧ . . .
(5)                                  diagnosis(d1 ) ←− has(x1 ) ∧ has(x3 ) ∧ . . .
(6)                                  diagnosis(d2 ) ←− has(x3 ) ∧ has(x4 ) ∧ . . .
                      A POC FOR EXPLAINABLE DISEASE DIAGNOSIS USING LLMS & ASP                      5


 !
       Prompt: Medical Text...
       The paragraph above lists common symptoms of pneumonia. Write a clingo script that diagnoses
       pneumonia based on these symptoms. In the diagnosis rule, use a structure like:
       diagnosis(pneumonia) :- has(symptom(x)), has(symptom(y)) ...
       Include alternative diagnoses that share overlapping symptoms with pneumonia. Add rules that
       link one symptom to another (e.g., symptom propagation or dependency).

 LLM Output
      symptom(cough).
      symptom(cough_with_mucus).
      ...


      linked_symptom(cough_with_mucus, wheezing).
      linked_symptom(cough_with_mucus, shortness_of_breath).

      ...

      has(symptom(Symptom2)) :- has(symptom(Symptom1)),
                    linked_symptom(Symptom1, Symptom2).


      diagnosis(pneumonia) :- has(symptom(cough)),
                              has(symptom(cough_with_mucus)),
      ...

      diagnosis(pneumonia) :- has(symptom(cough_with_mucus)),
                              has(symptom(chest_pain)),
      ...


            Figure 4. An effective prompt that produces accurate and well-structured output.
            The LLM output is structured into multiple rules that aid explainability and can
            result in partial diagnoses.


   Correlations between certain symptoms are also encoded in the knowledge base. For example,
clinical observations have reported links between skin conditions and headaches [41]. In some cases,
the presence of one symptom may lead to the appearance of another. Such relationships are captured
using rules of the form:

(7)              has(symptom(S2)) ←− has(symptom(S1)) ∧ linked symptom(S1, S2).

     Example entries for such relationships include:

(8)                            linked symptom(grunting, chest retractions).
(9)                        linked symptom(nasal f laring, chest retractions).

  Since patients may not exhibit all known symptoms, McCoy must support reasoning under
partial information. To allow flexible reasoning, a choice rule introduces possible symptoms into the
knowledge base when patient data is incomplete:

(10)                               {add(symptom(S)) : symptom(S)}.
6                             IOANNA GEMOU AND EVANGELOS LAMPROU




            l :punish ←− drive, drunk                                 d       k     r
           m :punish ←− resist
           e :prison ←− punish                                            l        m
           d :drive
           k :drunk
                                                                          e         e
(13)       r :resist
                                                                Figure 5. Causal graph of
                                                                logic program in eq. (13).

    The following integrity constraint imposes at least one diagnosis:
(11)                                    ⊥ ←−∼ diagnosis( )
  Finally, the solver minimizes assumptions by penalizing added symptoms, favoring diagnoses
based on known patient information:
(12)                            #minimize{1, S : add(symptom(S))}
  This formulation guarantees that at least one diagnosis is produced, relying as much as possible
on available clinical data rather than hypothetical assumptions.

Diagnostic Explainability. Symbolic AI offers a significant advantage over sub-symbolic methods
in terms of explainability. In symbolic systems, the relationships between facts and conclusions are
explicitly defined, enabling transparent reasoning. Thus, it possible to associate logical propositions
with their justifications [42]. For example, the logic program shown in eq. (13) is accompanied by
a causal graph shown in fig. 5, which illustrates the connections between rules and their inferred
outcomes. This structure supports the interpretability of conclusions derived by a symbolic logic
solver. The tool xclingo [43] enables the visualization of justifications for results produced by the
clingo solver. It does so by incorporating a trace that corresponds to the rules of the logic program.
McCoy leverages this produce such a trace, which can then help identify the reasoning path, as
well as potential flaws in McCoy’s knowledge base and reasoning process.

                                              5. Results
   Evaluation was conducted using a publicly available dataset.1 Each record’s list of symptoms
serves as input. The knowledge base—comprising ASP rules automatically derived from medical
literature—infers potential diagnoses. A prediction is considered correct when the disease inferred
by the ASP solver matches the actual diagnosis listed in the dataset.

         Table 1. Accuracy of the framework on selected diseases. The size column indicates
         the number of logical terms in the disease-specific ASP program.

                                   Diseases        Size Accuracy
                                   Chickenpox       66      95%
                                   Pneumonia        75      100%
                                   Common Cold      44      100%

    1https://www.kaggle.com/datasets/itachi9604/disease-symptom-description-dataset
                  A POC FOR EXPLAINABLE DISEASE DIAGNOSIS USING LLMS & ASP                         7


   High accuracy is achieved when the knowledge base includes a sufficiently rich set of logical
rules. In addition to accurate predictions, McCoy offers explainability and visualizes the reasoning
process behind each diagnosis (an example is shown in listing 1).
    *
    | __ diagnosis ( chickenpox )
         | __ has ( symptom ( itching ) )
         | __ has ( symptom ( fatigue ) )
         | __ has ( symptom ( lethargy ) )
              | __ has ( symptom ( fatigue ) )
              | __ linked_symptom ( fatigue , lethargy )
         | __ has ( symptom ( high_fever ) )
              | __ has ( symptom ( mild_fever ) )
                    | __ has ( symptom ( loss_of_appetite ) )
                    | __ linked_symptom ( loss_of_appetite , mild_fever )
              | __ linked_symptom ( mild_fever , high_fever )
         | __ has ( symptom ( loss_of_appetite ) )
         | __ has ( symptom ( mild_fever ) )
              | __ has ( symptom ( loss_of_appetite ) )
              | __ linked_symptom ( loss_of_appetite , mild_fever )
         | __ has ( symptom ( swelled_lymph_nodes ) )
       Listing 1. Excerpt from the explanation tree for the chickenpox diagnosis. The
       structure illustrates the reasoning path based on symptom associations (slightly
       modified for clarity).
   Listing 1 shows an excerpt from the explanation tree generated for a patient diagnosed with
chickenpox. The tree visualizes the reasoning steps performed by the ASP solver to reach this
conclusion. At the root, McCoy infers diagnosis(chickenpox) based on the presence of multiple
symptoms such as itching, fatigue, lethargy, and high fever. Each symptom is further justified
through observed inputs or inferred relationships. For example, lethargy is supported by repeated
instances of fatigue and the known association linked symptom(fatigue, lethargy). Similarly,
high fever is explained via the intermediate symptom mild fever, which itself is supported by
loss of appetite. These explanations demonstrate how McCoy combines direct observations and
transitive symptom relationships encoded in the knowledge base to construct a transparent and
explainable diagnostic path.

                                         6. Conclusion
   This paper presents McCoy, a framework for disease prediction using LLMs and ASP. The
system uses LLMs to extract knowledge from medical texts and translate it into ASP rules, which
then drive predictions and provide interpretable explanations. The architecture, prompt design, and
rule structuring in the knowledge base are described. Experiments show that McCoy can predict
diseases accurately while keeping the reasoning process transparent.
   Future work will focus on scaling this process across more sources, formalizing the pipeline to
enable auditability and pluggability, and further experimentation in augmenting each step with
additional guardrails, possibly including fine-tuning.
8                                IOANNA GEMOU AND EVANGELOS LAMPROU


                                                 References
 [1] Retno Aulia Vinarti. Knowledge Representation for Infectious Disease Risk Prediction System: A Literature
     Review. Procedia Computer Science, 161:821–825, 2019.
 [2] Gerhard Brewka, Thomas Eiter, and Miroslaw Truszczyński. Answer set programming at a glance. Commun. ACM,
     54(12):92–103, December 2011.
 [3] Michael Gelfond and Yulia Kahl. Knowledge Representation, Reasoning, and the Design of Intelligent Agents:
     The Answer-Set Programming Approach. Cambridge University Press, 2014.
 [4] Mario Alviano, Riccardo Bertolucci, Valeria Cardellini, Carmine Dodaro, Giuseppe Galatà, Muhammad Kashif
     Khan, Nicola Leone, Marco Maratea, Francesco Ricca, and Marco Schouten. Answer Set Programming in
     Healthcare: Extended Overview. IPS-RCRA@ AI* IA, 2020.
 [5] K. Singhal, Shekoofeh Azizi, Tao Tu, Said Mahdavi, Jason Wei, Hyung Won Chung, Nathan Scales, Ajay Kumar
     Tanwani, Heather J. Cole-Lewis, Stephen J. Pfohl, P A Payne, Martin G. Seneviratne, Paul Gamble, Chris Kelly,
     Nathaneal Scharli, Aakanksha Chowdhery, P. A. Mansfield, Blaise Agüera y Arcas, Dale R. Webster, Greg S.
     Corrado, Yossi Matias, Katherine Hui-Ling Chou, Juraj Gottweis, Nenad Tomaev, Yun Liu, Alvin Rajkomar,
     Joëlle K. Barral, Christopher Semturs, Alan Karthikesalingam, and Vivek Natarajan. Large language models
     encode clinical knowledge. Nature, 620:172–180, 2022.
 [6] Karan Singhal, Tao Tu, Juraj Gottweis, Rory Sayres, Ellery Wulczyn, Le Hou, Kevin Clark, Stephen Pfohl,
     Heather Cole-Lewis, Darlene Neal, Mike Schaekermann, Amy Wang, Mohamed Amin, Sami Lachgar, Philip
     Mansfield, Sushant Prakash, Bradley Green, Ewa Dominowska, Blaise Aguera y Arcas, Nenad Tomasev, Yun
     Liu, Renee Wong, Christopher Semturs, S. Sara Mahdavi, Joelle Barral, Dale Webster, Greg S. Corrado, Yossi
     Matias, Shekoofeh Azizi, Alan Karthikesalingam, and Vivek Natarajan. Towards Expert-Level Medical Question
     Answering with Large Language Models, 2023.
 [7] Yanxin Zheng, Wensheng Gan, Zefeng Chen, Zhenlian Qi, Qian Liang, and Philip S. Yu. Large Language Models
     for Medicine: A Survey, 2024.
 [8] Manar Aljohani, Jun Hou, Sindhura Kommu, and Xuan Wang. A Comprehensive Survey on the Trustworthiness
     of Large Language Models in Healthcare, 2025.
 [9] Cynthia Rudin. Stop Explaining Black Box Machine Learning Models for High Stakes Decisions and Use
     Interpretable Models Instead, 2019.
[10] Rishi Bommasani, Drew A. Hudson, Ehsan Adeli, Russ Altman, Simran Arora, Sydney von Arx, Michael S.
     Bernstein, Jeannette Bohg, Antoine Bosselut, Emma Brunskill, Erik Brynjolfsson, Shyamal Buch, Dallas Card,
     Rodrigo Castellon, Niladri Chatterji, Annie Chen, Kathleen Creel, Jared Quincy Davis, Dora Demszky, Chris
     Donahue, Moussa Doumbouya, Esin Durmus, Stefano Ermon, John Etchemendy, Kawin Ethayarajh, Li Fei-Fei,
     Chelsea Finn, Trevor Gale, Lauren Gillespie, Karan Goel, Noah Goodman, Shelby Grossman, Neel Guha,
     Tatsunori Hashimoto, Peter Henderson, John Hewitt, Daniel E. Ho, Jenny Hong, Kyle Hsu, Jing Huang, Thomas
     Icard, Saahil Jain, Dan Jurafsky, Pratyusha Kalluri, Siddharth Karamcheti, Geoff Keeling, Fereshte Khani, Omar
     Khattab, Pang Wei Koh, Mark Krass, Ranjay Krishna, Rohith Kuditipudi, Ananya Kumar, Faisal Ladhak, Mina
     Lee, Tony Lee, Jure Leskovec, Isabelle Levent, Xiang Lisa Li, Xuechen Li, Tengyu Ma, Ali Malik, Christopher D.
     Manning, Suvir Mirchandani, Eric Mitchell, Zanele Munyikwa, Suraj Nair, Avanika Narayan, Deepak Narayanan,
     Ben Newman, Allen Nie, Juan Carlos Niebles, Hamed Nilforoshan, Julian Nyarko, Giray Ogut, Laurel Orr,
     Isabel Papadimitriou, Joon Sung Park, Chris Piech, Eva Portelance, Christopher Potts, Aditi Raghunathan, Rob
     Reich, Hongyu Ren, Frieda Rong, Yusuf Roohani, Camilo Ruiz, Jack Ryan, Christopher Ré, Dorsa Sadigh, Shiori
     Sagawa, Keshav Santhanam, Andy Shih, Krishnan Srinivasan, Alex Tamkin, Rohan Taori, Armin W. Thomas,
     Florian Tramèr, Rose E. Wang, William Wang, Bohan Wu, Jiajun Wu, Yuhuai Wu, Sang Michael Xie, Michihiro
     Yasunaga, Jiaxuan You, Matei Zaharia, Michael Zhang, Tianyi Zhang, Xikun Zhang, Yuhui Zhang, Lucia Zheng,
     Kaitlyn Zhou, and Percy Liang. On the Opportunities and Risks of Foundation Models, 2021.
[11] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou, Yingqian Min, Beichen Zhang,
     Junjie Zhang, Zican Dong, Yifan Du, Chen Yang, Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren,
     Yifan Li, Xinyu Tang, Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. A Survey of Large Language
     Models, 2023.
[12] Bhargavi Paranjape, Scott Lundberg, Sameer Singh, Hannaneh Hajishirzi, Luke Zettlemoyer, and Marco Tulio
     Ribeiro. ART: Automatic multi-step reasoning and tool-use for large language models, 2023.
[13] OpenAI. GPT-5, 2025.
[14] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, L ukasz Kaiser,
     and Illia Polosukhin. Attention is All you Need. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus,
     S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems, volume 30.
     Curran Associates, Inc., 2017.
                     A POC FOR EXPLAINABLE DISEASE DIAGNOSIS USING LLMS & ASP                                       9


[15] Jie Gui, Tuo Chen, Jing Zhang, Qiong Cao, Zhenan Sun, Hao Luo, and Dacheng Tao. A survey on self-supervised
     learning: Algorithms, applications, and future trends. IEEE Trans. Pattern Anal. Mach. Intell., 46(12):9052–9071,
     December 2024.
[16] Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind
     Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen
     Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel Ziegler, Jeffrey Wu, Clemens Winter, Chris
     Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner,
     Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language Models are Few-Shot Learners.
     In H. Larochelle, M. Ranzato, R. Hadsell, M.F. Balcan, and H. Lin, editors, Advances in Neural Information
     Processing Systems, volume 33, pages 1877–1901. Curran Associates, Inc., 2020.
[17] Jingqing Zhang, Yao Zhao, Mohammad Saleh, and Peter Liu. PEGASUS: Pre-training with Extracted Gap-
     sentences for Abstractive Summarization. In Hal Daumé III and Aarti Singh, editors, Proceedings of the 37th
     International Conference on Machine Learning, volume 119 of Proceedings of Machine Learning Research, pages
     11328–11339. PMLR, 13–18 Jul 2020.
[18] Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng, Alicia
     Jin, Taylor Bos, Leslie Baker, Yu Du, YaGuang Li, Hongrae Lee, Huaixiu Steven Zheng, Amin Ghafouri, Marcelo
     Menegali, Yanping Huang, Maxim Krikun, Dmitry Lepikhin, James Qin, Dehao Chen, Yuanzhong Xu, Zhifeng
     Chen, Adam Roberts, Maarten Bosma, Vincent Zhao, Yanqi Zhou, Chung-Ching Chang, Igor Krivokon, Will
     Rusch, Marc Pickett, Pranesh Srinivasan, Laichee Man, Kathleen Meier-Hellstern, Meredith Ringel Morris,
     Tulsee Doshi, Renelito Delos Santos, Toju Duke, Johnny Soraker, Ben Zevenbergen, Vinodkumar Prabhakaran,
     Mark Diaz, Ben Hutchinson, Kristen Olson, Alejandra Molina, Erin Hoffman-John, Josh Lee, Lora Aroyo, Ravi
     Rajakumar, Alena Butryna, Matthew Lamm, Viktoriya Kuzmina, Joe Fenton, Aaron Cohen, Rachel Bernstein,
     Ray Kurzweil, Blaise Aguera-Arcas, Claire Cui, Marian Croak, Ed Chi, and Quoc Le. LaMDA: Language Models
     for Dialog Applications, 2022.
[19] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde de Oliveira Pinto, Jared Kaplan, Harri
     Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, Alex Ray, Raul Puri, Gretchen Krueger, Michael
     Petrov, Heidy Khlaaf, Girish Sastry, Pamela Mishkin, Brooke Chan, Scott Gray, Nick Ryder, Mikhail Pavlov,
     Alethea Power, Lukasz Kaiser, Mohammad Bavarian, Clemens Winter, Philippe Tillet, Felipe Petroski Such,
     Dave Cummings, Matthias Plappert, Fotios Chantzis, Elizabeth Barnes, Ariel Herbert-Voss, William Hebgen
     Guss, Alex Nichol, Alex Paino, Nikolas Tezak, Jie Tang, Igor Babuschkin, Suchir Balaji, Shantanu Jain, William
     Saunders, Christopher Hesse, Andrew N. Carr, Jan Leike, Josh Achiam, Vedant Misra, Evan Morikawa, Alec
     Radford, Matthew Knight, Miles Brundage, Mira Murati, Katie Mayer, Peter Welinder, Bob McGrew, Dario
     Amodei, Sam McCandlish, Ilya Sutskever, and Wojciech Zaremba. Evaluating Large Language Models Trained
     on Code, 2021.
[20] Renqian Luo, Liai Sun, Yingce Xia, Tao Qin, Sheng Zhang, Hoifung Poon, and Tie-Yan Liu. BioGPT: generative
     pre-trained transformer for biomedical text generation and mining. Briefings in Bioinformatics, 23(6), September
     2022.
[21] Bohang Li, Gaozhe Jiang, Ningxin Li, and Chaoda Song. Research on large-scale structured and unstructured data
     processing based on large language model. In Proceedings of the International Conference on Machine Learning,
     Pattern Recognition and Automation Engineering, MLPRAE ’24, page 111–116, New York, NY, USA, 2024.
     Association for Computing Machinery.
[22] Harsh Raj, Domenic Rosati, and Subhabrata Majumdar. Measuring Reliability of Large Language Models through
     Semantic Consistency, 2023.
[23] Laura Eline Ruis, Akbir Khan, Stella Biderman, Sara Hooker, Tim Rocktäschel, and Edward Grefenstette. Large
     language models are not zero-shot communicators, 2023.
[24] Lei Huang, Weijiang Yu, Weitao Ma, Weihong Zhong, Zhangyin Feng, Haotian Wang, Qianglong Chen, Weihua
     Peng, Xiaocheng Feng, Bing Qin, and Ting Liu. A survey on hallucination in large language models: Principles,
     taxonomy, challenges, and open questions. ACM Trans. Inf. Syst., 43(2), January 2025.
[25] Jesse Dodge, Maarten Sap, Ana Marasović, William Agnew, Gabriel Ilharco, Dirk Groeneveld, Margaret Mitchell,
     and Matt Gardner. Documenting Large Webtext Corpora: A Case Study on the Colossal Clean Crawled Corpus,
     2021.
[26] Deep Ganguli, Liane Lovitt, Jackson Kernion, Amanda Askell, Yuntao Bai, Saurav Kadavath, Ben Mann,
     Ethan Perez, Nicholas Schiefer, Kamal Ndousse, Andy Jones, Sam Bowman, Anna Chen, Tom Conerly, Nova
     DasSarma, Dawn Drain, Nelson Elhage, Sheer El-Showk, Stanislav Fort, Zac Hatfield-Dodds, Tom Henighan,
     Danny Hernandez, Tristan Hume, Josh Jacobson, Scott Johnston, Shauna Kravec, Catherine Olsson, Sam Ringer,
     Eli Tran-Johnson, Dario Amodei, Tom Brown, Nicholas Joseph, Sam McCandlish, Chris Olah, Jared Kaplan, and
     Jack Clark. Red Teaming Language Models to Reduce Harms: Methods, Scaling Behaviors, and Lessons Learned,
     2022.
10                               IOANNA GEMOU AND EVANGELOS LAMPROU


[27] Thomas Eiter, Giovambattista Ianni, and Thomas Krennwallner. Answer Set Programming: A Primer. volume
     5689, pages 40–110, 01 2009.
[28] Michael Gelfond and Vladimir Lifschitz. The Stable Model Semantics for Logic Programming. In Robert Kowalski,
     Bowen, and Kenneth, editors, Proceedings of International Logic Programming Conference and Symposium,
     pages 1070–1080. MIT Press, 1988.
[29] Michael Gelfond. Representing Knowledge in A-Prolog. In Computational Logic: Logic Programming and Beyond,
     pages 413–451. Springer Berlin Heidelberg, 2002.
[30] Martin Gebser, Roland Kaminski, Benjamin Kaufmann, and Torsten Schaub. Answer Set Solving in Practice.
     Springer International Publishing, 2013.
[31] Martin Gebser, Roland Kaminski, Benjamin Kaufmann, and Torsten Schaub. Clingo = ASP + Control: Prelimi-
     nary Report, 2014.
[32] Steffen Hölldobler and Lukas Schweizer. Answer set programming and CLASP: A tutorial. volume 1145, 04 2014.
[33] Boming Xia, Xiaozhen Ye, and Adnan Abuassba. Recent Research on AI in Games. pages 505–510, 06 2020.
[34] Esra Erdem, Yelda Erdem, Halit Erdogan, and Umut Oztok. Finding Answers and Generating Explanations
     for Complex Biomedical Queries. Proceedings of the AAAI Conference on Artificial Intelligence, 25(1):785–790,
     August 2011.
[35] Mario Alviano and Luca Grillo. Answer Set Programming and Large Language Models Interaction with YAML:
     Preliminary Report. In Proceedings of the 39th Italian Conference on Computational Logic (CILC 2024), volume
     3733 of CEUR Workshop Proceedings. CEUR-WS.org, 2024.
[36] Quang-Anh Nguyen, Thu-Trang Pham, Thi-Hai-yen Vuong, Giang Trinh, and Nguyen Thanh. Detecting Misleading
     Information with LLMs and Explainable ASP. pages 1327–1334, 01 2025.
[37] Erica Coppolillo, Francesco Calimeri, Giuseppe Manco, Simona Perri, and Francesco Ricca. LLASP: Fine-tuning
     Large Language Models for Answer Set Programming, 2024.
[38] Samuel R. Bowman. Eight Things to Know about Large Language Models, 2023.
[39] Pengfei Liu, Weizhe Yuan, Jinlan Fu, Zhengbao Jiang, Hiroaki Hayashi, and Graham Neubig. Pre-train, Prompt,
     and Predict: A Systematic Survey of Prompting Methods in Natural Language Processing, 2021.
[40] Prompt Engineering Guide. https://www.promptingguide.ai. [Accessed 27-May-2023].
[41] Migraine.com Editorial Team. Migraine Hives Symptoms. https://migraine.com/migraine-symptoms/hives.
     Accessed on May 30, 2023.
[42] Pedro Cabalar, Jorge Fandinno, and Michael Fink. Causal Graph Justifications of Logic Programs, 2014.
[43] Pedro Cabalar, Jorge Fandinno, and Brais Muñiz. A System for Explainable Answer Set Programming.
     Electronic Proceedings in Theoretical Computer Science, 325:124–136, sep 2020.
