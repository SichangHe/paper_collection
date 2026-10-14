                                                     CoqPyt: Proof Navigation in Python in the Era of LLMs
                                                           Pedro Carrott∗                             Nuno Saavedra∗                               Kyle Thompson
                                                  pedro.carrott@imperial.ac.uk                  nuno.saavedra@tecnico.ulisboa.pt               r7thompson@ucsd.edu
                                                    Imperial College London                    INESC-ID/IST, University of Lisbon         University of California San Diego
                                                          London, UK                                    Lisbon, Portugal                           San Diego, USA

                                                            Sorin Lerner                               João F. Ferreira                               Emily First
                                                     lerner@cs.ucsd.edu                                joao@joaoff.com                            emfirst@ucsd.edu
                                              University of California San Diego               INESC-ID/IST, University of Lisbon         University of California San Diego
                                                       San Diego, USA                                   Lisbon, Portugal                           San Diego, USA
arXiv:2405.04282v1 [cs.SE] 7 May 2024




                                        ABSTRACT                                                                  task is automated proof repair [20], which is necessary to perform
                                        Proof assistants enable users to develop machine-checked proofs           when specifications or dependencies change and result in broken
                                        regarding software-related properties. Unfortunately, the interac-        proofs. To train these neural models and implement proof search,
                                        tive nature of these proof assistants imposes most of the proof           sufficient programmatic support is thus required for collecting
                                        burden on the user, making formal verification a complex, and             training examples and driving the theorem prover.
                                        time-consuming endeavor. Recent automation techniques based on               In this paper, our target proof assistant is Coq due to its popu-
                                        neural methods address this issue, but require good programmatic          larity for building verified software systems. Existing tools, such
                                        support for collecting data and interacting with proof assistants.        as Coq Serapy [22] and PyCoq [9], provide programmatic support
                                        This paper presents CoqPyt, a Python tool for interacting with            for interacting with Coq in Python, and all current neural theorem
                                        the Coq proof assistant. CoqPyt improves on other Coq-related             provers for Coq utilize them. These tools implement Python bind-
                                        tools by providing novel features, such as the extraction of rich         ings for Coq SerAPI [7], which is a library for machine-to-machine
                                        premise data. We expect our work to aid development of tools and          interaction with Coq. However, with the announcement that Coq
                                        techniques, especially LLM-based, designed for proof synthesis and        SerAPI will be deprecated and replaced with Coq LSP [26], a lan-
                                        repair. A video describing and demonstrating CoqPyt is available          guage server for Coq, the need arises for a new tool to continue
                                        at: https://youtu.be/fk74o0rePM8.                                         supporting existing features. Fortunately, this also creates a great
                                                                                                                  opportunity to support new features that prior tools did not.
                                        CCS CONCEPTS                                                                 In the emerging era of large language models (LLMs), additional
                                                                                                                  functionality is desirable in tools for interfacing with Coq in Python
                                        • Software and its engineering → Software notations and
                                                                                                                  in order to promote LLM-based approaches for Coq proof synthesis
                                        tools; Development frameworks and environments.
                                                                                                                  and repair. Namely, the ability to collect rich contextual data is not
                                        KEYWORDS                                                                  supported by any of the existing programmatic tools for control-
                                                                                                                  ling Coq. LLM-based neural theorem provers for Lean and Isabelle
                                        Coq, Data extraction, Theorem proving, Retrieval augmentation             proof assistants rely on retrieval augmentation, wherein they re-
                                                                                                                  trieve premises, such as lemmas and definitions, that are relevant
                                        1    INTRODUCTION                                                         to the proof goal, and condition the next tactic generation on those
                                        Formal software verification is an incredibly effective method for        premises [17, 29]. For the approach to be effective, they collect fine-
                                        developing high quality software, as it ensures that a software pro-      grained annotations of which premises are used in proofs as well
                                        gram adheres to a predefined formal specification. For example,           as which premises are accessible from a proof. However, existing
                                        a study compared industrial standard compilers (e.g., GCC and             tools for Coq do not collect that type of premise data.
                                        LLVM) to CompCert, a C compiler verified using the Coq proof                 We introduce CoqPyt, a tool that enables interaction with Coq
                                        assistant [25], and CompCert was the only one for which no bugs           in Python using Coq LSP as the backend. CoqPyt continues to
                                        were found [30]. Unfortunately, even though formal software veri-         support existing capabilities essential to training data collection
                                        fication provides valuable guarantees, its development is still too       and proof search, but goes beyond state-of-the-art tools for Coq by
                                        costly. CompCert took 100,000 lines of Coq code and 6 person-             supporting the ability to collect rich contextual data, among other
                                        years to formally verify [13]. For this reason, it is important to find   novel features. Our tool supports the newest versions of Coq (8.17
                                        methods that decrease the cost of formal verification.                    to 8.19), which will facilitate mining software repositories for new,
                                           One recent approach to address this is the use of neural methods       enriched training and evaluation data. We foresee that our work will
                                        to automate proof synthesis. Neural theorem provers, given a partial      help promote future research into neural proof synthesis and repair
                                        proof and the proof state, use neural networks to predict the next        for Coq, especially as LLM capabilities continue to evolve. CoqPyt
                                        likely proof steps. A proof assistant is then used to evaluate the        is open-source and available at: https://github.com/sr-lab/coqpyt.
                                        candidate proof steps, returning either new proof states or errors.
                                        Neural theorem provers iterate on this procedure, performing proof        2   COQPYT
                                        search to traverse the space of possible proofs. A complementary
                                                                                                                  CoqPyt is a Python tool that enables developers and researchers to
                                        ∗ Both authors contributed equally to this research.                      interact programmatically with Coq. It also allows users to extract
                                                                                                                                                                                                                                             Carrott et al.


                  CoqChange                           CoqFile                           FileContext                         Term                      ProofTerm                              ProofFile                                 ProofChange
                                           steps : List[Step]                     terms : Map[String, Term]   1   * step : Step          *    * steps : List[ProofStep]   *   1 proofs : List[ProofTerm]
                                                                          1   1
                                           context : FileContext                  update(terms) : None               type : TermType             context : List[Term]           open_proofs : List[ProofTerm]
                                           is_valid : Bool                                                                                                                      current_goals : Optional[GoalAnswer]
                                                                                                                            1            *                1                     in_proof : Bool
                                           exec(nsteps) : List[Step]
     CoqAdd                   CoqDelete                                                                                     1                             *                                                              ProofAppend                 ProofPop
                                           add_step(index, text) : None
                                           delete_step(index) : None                                                        Step                       ProofStep                append_step(proof, text) : None
index : Integer
                         index : Integer   change_steps(changes) : None                                                                                                         pop_step(proof) : None                 text : String
text : String                                                             1                                       * text : String             * goal : GoalAnswer
                                           save_vo() : None                                                                                                                     change_proof(proof, changes) : None
                                                                                                                     ast : RangedSpan            context : List[Term]




   Figure 1: UML diagram for a simplified view of the domain of CoqPyt. The selected attributes and methods are all public.


textual and structural information from Coq files. We now describe                                                                         A CoqFile object provides an exec method which allows users
the structure and main functionalities of CoqPyt, providing an                                                                          to take an arbirary number of forward and backward steps through
illustrative example on how to interact with the tool.                                                                                  the file. The method returns a list of Steps corresponding to the
                                                                                                                                        steps that were executed or backtracked during the call. Each step
2.1           The Coq Proof Assistant                                                                                                   contains its textual representation in the file and the AST contents.
Coq provides an interactive environment with a rich type system                                                                            Given that steps may be term definitions, a FileContext object
suitable for theorem proving. A theorem in Coq is a type definition,                                                                    is kept within the CoqFile, indexing by name all terms that have
which can be proven by constructing a proof term with the stated                                                                        been defined until the last executed step. Any term defined inside
theorem type. Since writing a proof term directly is difficult, Coq                                                                     a module has its name prefixed by the module path. Although
allows users to write a proof script consisting of a sequence of high-                                                                  notations are nameless terms, these are also stored in the context,
level tactics (e.g., induction or reflexivity). Each tactic guides Coq in                                                               indexed by the string pattern used to define them. For each defined
a search for the desired proof term, refining the state until no new                                                                    term, a Term object is created containing its corresponding step, as
obligations hold. After a tactic application, Coq displays the current                                                                  well as its term type. This type depends on whether the term is a
proof state, which includes the goals to prove and the local context.                                                                   theorem, a notation, a tactic or any other definable Coq construct.
When executed, a complete proof script generates the proof term.

2.2           Coq Language Server Protocol                                                                                              2.4        Proof Navigation
To interact with Coq files, we use Coq LSP [26], a language server                                                                      With CoqPyt, it is also possible to track the proof state throughout
that provides Coq-related features. Coq LSP was developed to re-                                                                        the file. A CoqFile can be instantiated through the ProofFile
place Coq SerAPI [7], a well-known tool in the Coq community                                                                            subclass, which allows users to manage the file’s proof context.
that implements a protocol for interacting specifically with Coq                                                                        As steps are taken, one can enter (or leave) proof mode, which
files. Unlike Coq SerAPI, Coq LSP follows a standardized protocol                                                                       will activate (or deactivate) the in_proof boolean flag. If there are
for interacting with text documents known as Language Server                                                                            any on-going goals, these can be accessed via the current_goals
Protocol (LSP) [16]. LSP servers, such as Coq LSP, provide useful                                                                       attribute. Goals are represented as a GoalAnswer object, which
language features, such as auto complete. Client applications, such                                                                     mimics the structure of goals in the Coq LSP response [26].
as IDEs, can use these features by running their own LSP client.                                                                            In addition to allowing users to manage a file’s proof context,
    Besides the usual LSP features, Coq LSP provides Coq-specific                                                                       ProofFile instances also fetch all of the file’s imported terms. Thus,
functionality, namely requesting the proof state at any given point                                                                     a ProofFile captures terms in a file and in its dependencies. In
of a Coq file. Coq LSP also allows users to request the abstract                                                                        practice, the ProofFile context is initialized by instantiating a
syntax tree (AST) of the entire document, which corresponds to                                                                          CoqFile for each library imported by the file and extracting the
a list of steps in the file, each with its own AST representation. A                                                                    context of each library to the new ProofFile instance. Since cre-
step can be a term definition (e.g., definitions and theorems) or a                                                                     ating a ProofFile requires instantiating multiple CoqFiles, it is
proof step (e.g., mid-proof tactic application), determined by the AST                                                                  more expensive to create a ProofFile than a CoqFile.
contents of each step. For erroneous Coq files, Coq LSP is able to                                                                          A ProofFile holds information about all proofs found in the
ignore erroneous steps and evaluate the remaining steps of the file,                                                                    file until the last executed step. Proofs with open goals are kept in
allowing any subsequent non-erroneous steps to define new terms.                                                                        the open_proofs attribute. Multiple open proofs occur in files with
Coq LSP also enables project-wise imports by saving compiled .vo                                                                        nested proofs, as we need to open inner proofs before closing outer
files, which may also benefit from this error-ignoring approach,                                                                        proofs. Each proof is a ProofTerm, a Term with a context attribute,
given that valid files may still import terms from invalid files.                                                                       listing all terms found in the current context used to define the
                                                                                                                                        proof term. This contextual information is valuable for neural-based
2.3           Interaction with Coq Files                                                                                                models and is not accessible from prior Coq-related tools.
CoqPyt implements a client for Coq LSP providing the interface                                                                              A ProofTerm also contains an ordered list of ProofSteps, corre-
shown in Figure 1. This client implementation is encapsulated                                                                           sponding to all steps taken until the proof is closed (or until the last
within CoqFile, a class that abstracts the state of an actual Coq file,                                                                 executed step if the proof is open). The ProofStep class enables a
hiding the interaction with Coq LSP. For instance, the is_valid                                                                         mapping from each proof step to the intermediate proof goals it
boolean flag indicates if the underlying Coq file is valid and the                                                                      attempts to solve or simplify. A ProofStep is thus constructed by
save_vo method allows the user to compile the file.                                                                                     augmenting the respective Step with the intermediate proof goals
CoqPyt: Proof Navigation in Python in the Era of LLMs


  1   Require Import List .                                                    1   with ProofFile (" test .v") as pf :
  2   Lemma rev_append : forall {a} ( l1 l2 : list a) ,                        2     pf . exec ( len ( pf . steps ))
  3     rev ( l1 ++ l2 ) = rev l2 ++ rev l1 .                                  3     print ( pf . context )
  4   Proof .                                                                  4     for proof in pf . proofs :
  5   intros a l1 l2 . induction l1 ; intros .                                 5        for step in proof . steps :
  6     - simpl . rewrite app_nil_r . reflexivity .                            6           print ( step . text , step . ast , step . context , step . goals )
  7     - simpl . rewrite IHl1 .
  8   Admitted .
                                                                                         Listing 2: Proof data available with CoqPyt.
 Listing 1: Example Coq file test.v with a property of rev.
                                                                               1   incorrect = [" reflexivity ." , "\ nQed ."]
                                                                               2   correct = [" rewrite app_assoc ."] + incorrect
before that step is taken. Similarly to ProofTerm, a ProofStep also            3   with ProofFile (" test .v") as pf :
                                                                               4       pf . exec ( len ( pf . steps ))
has a context attribute listing the terms used in the step.                    5       unproven = pf . unproven_proofs [0]
                                                                               6       for attempt in [ incorrect , correct ]:
2.5      Proof Modification                                                    7
                                                                               8
                                                                                             changes = [ ProofPop () ] # Admitted
                                                                                             for s in attempt :
CoqPyt allows steps to be added to or deleted from the file. Allowing          9                   changes . append ( ProofAppend (s))
                                                                            10               try :
such modifications on Coq files yields an interface well suited for         11                     pf . change_proof ( unproven , changes )
proof development. Invalid changes, such as adding inexisting tac-          12                     print (" Proof succeeded !")
tics, may lead to explicit errors or undefined behaviour, depending         13                     break
                                                                            14               except InvalidChangeException :
on the nature of the error. For erroneous modifications, the file will      15                     print (" Proof attempt not valid .")
revert to its original state, ignoring the requested changes.                                Listing 3: Proof attempts with CoqPyt.
   Through the add_step method, it is possible to define terms,
introduce theorems and apply tactics to solve proof obligations.
Conversely, delete_step enables the removal of steps, such as
added tactics which do not alter the proof goals as intended. Both         of the proof rev_append (line 5). We then delete the “Admitted.”
methods allow editing in arbitrary parts of the file: delete_step          step from the proof of rev_append (line 7) and add the steps asso-
requires an index i to delete the ith step in the file; add_step           ciated with our new proof attempt (line 9). When we attempt to
requires the index of the step which precedes the new step. To add         add the erroneous steps from the proof attempt incorrect (line
a new step, its textual representation must also be provided.              11), an error is returned and test.v will remain in its original state.
   Modifications may also be batched as transactions. A sequence of        In turn, when the valid steps from the proof attempt correct are
CoqChanges can be provided to the change_steps method, which               added (line 11), the changes are applied to test.v.
will perform all modifications. A CoqChange can be either a CoqAdd
or a CoqDelete, which serve as data wrappers for the parameters of         3       RELATED WORK
add_step and delete_step, respectively. During the transaction,            Most neural theorem provers for Coq use either Coq Serapy [22, 24],
intermediate invalid states are allowed as long as the final state is      PyCoq [2], or a custom Python class [4, 5, 23, 28] to create training
valid. For example, it is possible to add a Qed before adding the actual   examples and perform proof search. The neural theorem prover
proof steps, which cannot be done through successive add_step              GamePad [8] instead modifies Coq itself to record intermediate
calls. To directly modify a proof, ProofFile provides the methods          proof states. The CoqGym benchmark dataset [28], collected using
append_step and pop_step for single step modifications, as well            a Python class, is the state-of-the-art benchmark for Coq. However,
as a change_proof method for a transaction of ProofChanges.                it was collected in 2019 and has only been updated to support
                                                                           versions 8.10 and 8.12 of Coq, while the newest version is 8.19.
2.6      Use Cases                                                         CoqPyt will render neural theorem provers useful for new Coq
The features that CoqPyt offers are particularly useful for proof          developments since it can be used for mining software repositories
search and learning-based tasks, such as neural theorem proving. To        for newer Coq training data and for evaluation.
get a sense of CoqPyt’s interface for collecting data and conducting          LeanDojo [29] and PISA [10] are learning environments for Lean
proof search, consider the file test.v in Listing 1, where we have         and Isabelle, allowing for data extraction and proof search inter-
a Coq file that defines a property about reversing a list. Listing 2       action. The neural theorem provers that use these environments
shows how we can leverage CoqPyt to collect data from the file             are LLM-based and use retrieval augmentation [11, 17, 29]. CoqPyt
shown in Listing 1. We can see which terms are available to the            would enable retrieval augmented LLM approaches in Coq.
file via the pf.context attribute (line 3). For example, all the terms        Pretrained LLMs have been shown to have quantitative reasoning
from the imported package List.v are available to the proofs in            capabilities [3, 18, 27], especially when they undergo continued
the file. Likewise, we show how to retrieve information from each          training on math data [1, 14]. To synthesize proofs, they can be
proof step in the file via the ProofStep attributes (line 6).              fine-tuned on proof data [6, 10, 29], few-shot prompted [1, 12, 31],
    Developing neural-based theorem provers requires the ability to        or even zero-shot prompted [24, 29]. However, the question of test
attempt possibly erroneous proofs during proof search. For example,        leakage arises in any evaluation that uses pretrained LLMs. CoqPyt
suppose we wanted to complete the proof rev_append from List-              will allow for data collection after the pretraining cutoff date.
ing 1. Listing 3 shows how we can use the change_proof method                 During proof development, proof engineers are constantly per-
to conduct proof attempts. We first obtain the ProofTerm object            forming proof repair [21]. The first work in automating this task
                                                                                                                                                                          Carrott et al.


               Table 1: Evaluation of CoqPyt’s performance on CompCert. PCC stands for Pearson correlation coefficient.

                               Count                                                                      Execution time (s)
                                                                                   Add step                  Delete step          Change steps (Add)       Change steps (Delete)
    Metric/Feature
                      Proofs           Steps       Load file   Execute file   Beginning   On pointer     Beginning   On pointer   Beginning   On pointer   Beginning     On pointer

    𝜇 (𝜎 2 )         32.3 (48.1)   609.6 (828.1)   6.6 (7.3)    31.2 (63.8)   1.1 (1.8)   0.9 (1.5)      1.0 (1.7)   0.9 (1.6)    1.5 (2.7)   1.0 (1.7)    1.1 (1.8)     0.8 (1.5)
    𝑥˜                  12.0          258.0           3.9           9.6          0.4         0.3            0.3         0.3          0.5         0.3          0.4           0.3
    PCC (steps)           -            1.00          0.59          0.72         0.90        0.92           0.94        0.92         0.87        0.92         0.90          0.91


Table 2: Feature comparison between CoqPyt and similar                                     we performed the modification in the beginning of the file and
tools (✓full support, ∼ partial support, ✗ no support).                                    at the current point of execution, after executing the whole file.
                                                                                           We performed each case 5 times for each feature. This approach is
         Feature                        CoqPyt     Coq LSP     Coq Serapy                  driven by the understanding that the number of required operations
         Get proof state                  ✓           ✓             ✓                      for these features increases as the distance to the point of execution
         Check file validity              ✓           ✓             ✓                      rises. To evaluate change_steps, we performed a single addition
         Execute/Modify steps            ✓/✓         ∼/✗           ✓/∼
         Extract step context             ✓           ✗             ✗                      or deletion to make it simpler to compare to the other features. The
         Track modules/terms/proofs     ✓/✓/✓       ✗/✓/✗         ✓/✗/∼                    results for file execution are dependent on a cache that saves our
                                                                                           loading of Coq libraries. As more libraries were cached, the time to
                                                                                           execute the files decreased. By calculating the Pearson correlation
uses symbolic tools for automated proof repair in Coq [20], and has                        coefficient, we conclude that the execution time for all features is
since been applied to other proof systems [15]. Baldur is the first                        positively correlated to the number of steps in a file. A replication
work to use neural methods (in particular, LLMs) to repair proofs,                         package is available at: https://zenodo.org/records/10292580.
but as part of its proof synthesis approach [6]. With the creation of
a large-scale dataset of proof repair instances [19], the creation of                      5       CONCLUSION
LLM methods to automate real-world proof repairs is forthcoming.                           We developed CoqPyt, a Python tool for interacting with Coq. It of-
                                                                                           fers valuable features previously unavailable in similar Coq-related
4      EVALUATION                                                                          tools, namely per-step context extraction and arbitrary file and
   Feature Evaluation. Table 2 compares the features of CoqPyt                             proof modification. CoqPyt does not yet explore the full potential
to similar tools. When compared to Coq LSP, CoqPyt supports a                              of context extraction, as it does not consider a small subset of Coq’s
more extensive range of features by using the data supplied by                             rich environment (e.g., module types and section-local constructs)
Coq LSP and constructing additional components of Coq program                              nor does it fetch context recursively, i.e., for each term in a step con-
logic upon it. For instance, Coq LSP provides partial support for                          text we ignore the context of the term itself. Nonetheless, we have
operating with steps by enabling retrieval of the proof state at any                       shown that CoqPyt provides rich features and reasonable execution
position of the file. However, it lacks implementation for navigating                      times, enabling an expressive interaction style with Coq. These con-
backward or forward from a specific step, which is provided by                             tributions are expected to ease the automation of machine-checked
CoqPyt. Compared to Coq Serapy, CoqPyt offers complete support                             proof synthesis and repair in the emerging era of LLMs.
for an additional four features: (1) modifying steps – while Coq
Serapy supports the addition or deletion of steps at the current                           ACKNOWLEDGEMENTS
point of execution, it does not offer the capability to add or delete                      This work was partially funded by NSF, National Science Founda-
steps at arbitrary positions within the file; (2) extract step context –                   tion grants CCF-1955457 and CCF-2220892, and by FCT, Fundação
Coq Serapy does not collect the terms used in each step; (3) track                         para a Ciência e a Tecnologia, under grant BD/04736/2023 and
terms – Coq Serapy does not retain a record of the terms defined up                        project UIDB/50021/2020 (DOI:10.54499/UIDB/50021/2020).
to the current execution point; (4) track proofs – even though Coq
Serapy supports commands such as navigating to the next proof, it                          REFERENCES
does not maintain a record of all the proofs already defined in a file.                      [1]       Zhangir Azerbayev, Hailey Schoelkopf, Keiran Paster, Marco Dos Santos,
                                                                                                       Stephen McAleer, Albert Q. Jiang, Jia Deng, Stella Biderman, and Sean Welleck.
    Performance Evaluation. To evaluate CoqPyt’s performance, we                                       2023. Llemma: An Open Language Model For Mathematics. (2023). arXiv: 2310
                                                                                                       .10631.
used the project CompCert [13] since it is a popular project with                            [2]       Lasse Blaauwbroek, Josef Urban, and Herman Geuvers. 2020. The Tactician.
over 1,700 stars on GitHub and 259 Coq files with considerable                                         In Intelligent Computer Mathematics (CICM 2020). Christoph Benzmüller and
                                                                                                       Bruce Miller, (Eds.) Springer, Cham, 271–277. doi: 10.1007/978-3-030-53518-6
complexity. We ran the experiments inside a Docker container on                                        _17.
an Intel Xeon Silver 4210R CPU @ 2.40GHz. Table 1 summarizes                                 [3]       Aakanksha Chowdhery et al. 2022. PaLM: Scaling Language Modeling with
our results. CoqPyt was able to run on 193 files, 58 files contained                                   Pathways. CoRR, abs/2204.02311. arXiv: 2204.02311. doi: 10.48550/arXiv.2204.0
                                                                                                       2311.
Coq-related errors, 6 files generated out-of-memory errors, and 2                            [4]       Emily First and Yuriy Brun. 2022. Diversity-driven automated formal verifica-
files crashed for unknown reasons. The column Count describes                                          tion. In Proceedings of the 44th International Conference on Software Engineering
metrics for the number of steps and proofs of CompCert. We ran                                         (ICSE ’22). Association for Computing Machinery, Pittsburgh, Pennsylvania,
                                                                                                       (May 2022), 749–761. doi: 10.1145/3510003.3510138.
all the features in each Coq file. For features that modify steps,
CoqPyt: Proof Navigation in Python in the Era of LLMs


 [5]   Emily First, Yuriy Brun, and Arjun Guha. 2020. TacTok: semantics-aware proof       [19]   Tom Reichel, R Henderson, Andrew Touchet, Andrew Gardner, and Talia Ringer.
       synthesis. Proceedings of the ACM on Programming Languages, 4, OOPSLA,                    2023. Proof repair infrastructure for supervised models: Building a large proof
       Article 231, (Nov. 2020), 31 pages. doi: 10.1145/3428299.                                 repair dataset. In 14th International Conference on Interactive Theorem Proving
 [6]   Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun. 2023. Baldur: Whole-              (ITP 2023). Schloss-Dagstuhl-Leibniz Zentrum für Informatik. doi: 10 . 4230
       Proof Generation and Repair with Large Language Models. In Proceedings of                 /LIPIcs.ITP.2023.26.
       the 31st ACM Joint European Software Engineering Conference and Symposium          [20]   Talia Ringer. 2021. Proof Repair. Ph.D. Dissertation. University of Washington.
       on the Foundations of Software Engineering (ESEC/FSE 2023). Association for        [21]   Talia Ringer, Alex Sanchez-Stern, Dan Grossman, and Sorin Lerner. 2020.
       Computing Machinery, San Francisco, CA, USA, (Nov. 2023), 1229–1241. doi:                 REPLica: REPL instrumentation for Coq analysis. In Proceedings of the 9th
       10.1145/3611643.3616243.                                                                  ACM SIGPLAN International Conference on Certified Programs and Proofs (CPP
 [7]   Emilio Jesús Gallego Arias. 2016. SerAPI: Machine-Friendly, Data-Centric Seri-            2020). Association for Computing Machinery, New Orleans, LA, USA, (Jan.
       alization for Coq. Tech. rep. MINES ParisTech, (Oct. 2016). https://hal-mines-p           2020), 99–113. doi: 10.1145/3372885.3373823.
       aristech.archives-ouvertes.fr/hal-01384408.                                        [22]   Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin Lerner. 2020.
 [8]   Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever. 2019.                     Generating correctness proofs with neural networks. In Proceedings of the 4th
       GamePad: A Learning Environment for Theorem Proving. In ICLR. https://ope                 ACM SIGPLAN International Workshop on Machine Learning and Programming
       nreview.net/forum?id=r1xwKoR9Y7.                                                          Languages (MAPL 2020). Association for Computing Machinery, London, UK,
 [9]   IBM. 2021. pycoq. https://github.com/IBM/pycoq. (2021).                                   1–10. doi: 10.1145/3394450.3397466.
[10]   Albert Q. Jiang, Wenda Li, Jesse Michael Han, and Yuhuai Wu. 2021. LISA:           [23]   Alex Sanchez-Stern, Emily First, Timothy Zhou, Zhanna Kaufman, Yuriy Brun,
       Language models of ISAbelle proofs. 6th Conference on Artificial Intelligence             and Talia Ringer. 2023. Passport: Improving Automated Formal Verification
       and Theorem Proving, (Sept. 2021).                                                        Using Identifiers. ACM Transactions on Programming Languages and Systems,
[11]   Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski,                     45, 2, Article 12, (June 2023), 30 pages. doi: 10.1145/3593374.
       Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu, and Mateja Jamnik. 2022. Thor:          [24]   Amitayush Thakur, Yeming Wen, and Swarat Chaudhuri. 2023. A Language-
       Wielding Hammers to Integrate Language Models and Automated Theorem                       Agent Approach to Formal Theorem-Proving. (2023). arXiv: 2310.04353.
       Provers. In Advances in Neural Information Processing Systems (NeurIPS 2022).      [25]   The Coq Development Team. 2024. Coq – Release 8.19.1. https://coq.inria.fr.
       Vol. 35. Curran Associates, Inc., 8360–8373.                                              (2024).
[12]   Albert Qiaochu Jiang, Sean Welleck, Jin Peng Zhou, Timothee Lacroix, Jiacheng      [26]   The Coq LSP Development Team. 2024. Coq LSP – Release 0.1.8. https://github
       Liu, Wenda Li, Mateja Jamnik, Guillaume Lample, and Yuhuai Wu. 2023. Draft,               .com/ejgallego/coq-lsp. (2024).
       Sketch, and Prove: Guiding Formal Theorem Provers with Informal Proofs. In         [27]   Hugo Touvron et al. 2023. Llama 2: Open Foundation and Fine-Tuned Chat
       The Eleventh International Conference on Learning Representations. https://open           Models. (2023). arXiv: 2307.09288.
       review.net/forum?id=SMa9EAovKMC.                                                   [28]   Kaiyu Yang and Jia Deng. 2019. Learning to prove theorems via interacting
[13]   Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer, Markus                   with proof assistants. In Proceedings of the 36th International Conference on
       Pister, and Christian Ferdinand. 2016. CompCert - A Formally Verified Opti-               Machine Learning. Vol. 97. PMLR, (June 2019), 6984–6994.
       mizing Compiler. In ERTS 2016: Embedded Real Time Software and Systems, 8th        [29]   Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song, Shixing Yu,
       European Congress. SEE. Toulouse, France, (Jan. 2016). https://inria.hal.science          Saad Godil, Ryan Prenger, and Anima Anandkumar. 2023. LeanDojo: Theorem
       /hal-01238879.                                                                            Proving with Retrieval-Augmented Language Models. In Advances in Neural
[14]   Aitor Lewkowycz et al. 2022. Solving Quantitative Reasoning Problems with                 Information Processing Systems (NeurIPS 2023). Vol. 36. Curran Associates, Inc.,
       Language Models. CoRR, abs/2206.14858. doi: 10.48550/arXiv.2206.14858.                    21573–21612.
[15]   Paolo Masci and Aaron Dutle. 2022. Proof Mate: An Interactive Proof Helper         [30]   Xuejun Yang, Yang Chen, Eric Eide, and John Regehr. 2011. Finding and un-
       for PVS (Tool Paper). In NASA Formal Methods Symposium. Springer, 809–815.                derstanding bugs in C compilers. In Proceedings of the 32nd ACM SIGPLAN
[16]   Microsoft. 2023. Language Server Protocol. https://microsoft.github.io/langua             Conference on Programming Language Design and Implementation (PLDI ’11).
       ge-server-protocol. (2023).                                                               Association for Computing Machinery, San Jose, California, USA, (June 2011),
[17]   Maciej Mikuła, Szymon Antoniak, Szymon Tworkowski, Albert Qiaochu Jiang,                  283–294. doi: 10.1145/1993498.1993532.
       Jin Peng Zhou, Christian Szegedy, Łukasz Kuciński, Piotr Miłoś, and Yuhuai Wu.     [31]   Shizhuo Dylan Zhang, Talia Ringer, and Emily First. 2023. Getting More out of
       2023. Magnushammer: A Transformer-based Approach to Premise Selection.                    Large Language Models for Proofs. 8th Conference on Artificial Intelligence and
       (2023). arXiv: 2303.04488.                                                                Theorem Proving, (Sept. 2023). arXiv: 2305.04369.
[18]   OpenAI. 2023. GPT-4 Technical Report. (2023). arXiv: 2303.08774.
