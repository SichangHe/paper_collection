                                         Understanding and Improving Automated Proof Synthesis for
                                         Interactive Theorem Provers
                                         Manqing Zhanga,1 , Yunwei Donga,∗ , Lingru Zhoub , Bingxu Xiaoa and Yepang Liuc,d
                                         a School of Software, Northwestern Polytechnical University, Xi’an, China
                                         b School of Computer Science and Ningbo Institute, Northwestern Polytechnical University, Xi’an, China
                                         c Research Institute of Trustworthy Autonomous Systems, Southern University of Science and Technology, Shenzhen, China
                                         d Department of Computer Science and Engineering, Southern University of Science and Technology, Shenzhen, China



                                         ARTICLE INFO                                         ABSTRACT
                                         Keywords:                                            Formal verification using interactive theorem provers ensures high-quality software. However, writing
                                         Proof Script Synthesis                               proof scripts for interactive theorem provers is labor-intensive and requires deep expertise. Recent
arXiv:2604.24354v1 [cs.LO] 27 Apr 2026




                                         Formal Software Verification                         studies have leveraged deep learning to automate theorem proving by learning from manually written
                                         Deep Learning                                        proof corpora. Nevertheless, these techniques still achieve limited success rates in proof synthesis.
                                         Expert Proof Pattern                                 This paper investigates the theorems that current proof synthesis techniques are unable to prove and
                                                                                              analyzes their characteristics. Through an in-depth analysis of the proven theorems, proof scripts, and
                                                                                              the proof search process, we identify the limitations of existing tools and summarize the key factors
                                                                                              influencing proof success rates. Our research provides valuable insights for the future optimization of
                                                                                              automated proof tools. Based on our empirical study, we discover that tactic selections conforming
                                                                                              to human expert proof patterns are more likely to lead to successful proofs. Inspired by this finding,
                                                                                              we propose a pattern-guided tactic search (PGTS) method to heuristically enhance the search process
                                                                                              of existing proof synthesis tools. Our evaluation experiments demonstrate that PGTS improves the
                                                                                              number of theorems proved by existing proof synthesis tools by an average of 8.05%, while also
                                                                                              achieving an average 20% increase in previously unproven theorems. Furthermore, PGTS enhances
                                                                                              the capability of proof synthesis tools to prove complex theorems and generates more concise proof
                                                                                              scripts.



                                         1. Introduction                                                                neural networks, which learn to generate tactics by training
                                                                                                                        on large-scale corpora of proof step data. These methods
                                             Ensuring the reliability of complex software systems re-                   treat proof synthesis as a machine translation problem. A
                                         mains a fundamental challenge in software engineering [1],                     model encodes the current proof step state and decodes it
                                         especially given their increasing complexity and critical                      into the next appropriate tactic. By iteratively predicting
                                         role in modern applications [2, 3, 4]. Traditional testing                     and applying tactics for every proof step state, the system
                                         methods often fail to provide complete assurances of soft-
                                                                                                                        incrementally constructs a complete formal proof through
                                         ware correctness, particularly for edge cases and complex
                                                                                                                        proof search.
                                         interactions. In this context, interactive theorem provers                         However, their performance remains consistently lim-
                                         (ITPs) offers a robust alternative, utilizing formal methods to                ited in real-world theorem proving applications. To investi-
                                         ensure that software systems meet their specifications. ITPs                   gate the performance bottlenecks of existing proof synthe-
                                         have been successfully applied to verify many large-scale                      sis tools, this paper conducts an in-depth analysis of the
                                         and complex software systems, such as the seL4 operating
                                                                                                                        characteristics of theorems that these tools fail to prove.
                                         system microkernel [5] and the CompCert compiler [6].
                                                                                                                        Specifically, as shown in Figure 1, we examine the features
                                             In ITPs, users construct formal proofs by writing proof                    of unprovable theorems from three dimensions: the theo-
                                         scripts, consisting of proof tactics sequences. Each tactic                    rems themselves, the proof scripts, and the proof search
                                         represents a small, logical proof step that advances the proof                 process. Our findings indicate that current proof synthesis
                                         toward completion. However, writing these tactics manu-                        tools face significant challenges when dealing with complex
                                         ally is often a knowledge and labor-intensive task [7]. For
                                                                                                                        theorems, especially those involving higher-order logic or
                                         instance, the seL4 team invested over 20 person-years and
                                                                                                                        intricate logical-mathematical symbols. Proof success rates
                                         wrote over 33K lines of proof scripts to verify a microker-                    are notably lower for theorems that include logical operators
                                         nel [8]. Similarly, the CompCert verified compiler project                     (∧, ∨, ¬). Moreover, performance drops substantially when
                                         required 6 person-years of effort, resulting in 175 Coq files                  the proof process requires the introduction of intermediate
                                         and approximately 100K lines of proof script [9, 10]. To                       lemmas. We also observe that proof tactics aligned with
                                         alleviate the high cost of manual proof development, re-
                                                                                                                        commonly used human expert reasoning patterns are more
                                         cent research has explored automated proof synthesis using                     likely to succeed in proof search.
                                             ∗ Corresponding author                                                         Inspired by this study, we propose a pattern-guided tactic
                                                 yunweidong@nwpu.edu.cn (Y. Dong)                                       search (PGTS) algorithm that heuristically steers the proof
                                              ORCID (s): 0000-0001-9882-9121 (Y. Dong)                                  search process. As illustrated in Figure 1, our study begins
                                             1 This work was done when the first author was a visiting scholar at

                                         Southern University of Science and Technology.


                                         M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                          Page 1 of 17
                                                 Journal of Systems and Software

                              Theorems          §7 Evaluation       1 Theorem trace_outputs_backup :
                        RQ1   Complex
                                                Effectiveness       2   forall e, trace_outputs [(backup, e)] = 0.
                                                                    3 Proof.
                                Proof             Capability
                        RQ2                                         4   intros.
                                Scripts
                                                   Quality          5   simpl in |- *.
                                Search                              6   auto.
                        RQ3    Progress            §6 PGTS          7 Qed.

Proof Synthesis Tools     Empirical Study    PGTS and Evaluation        Figure 2: An example of proof script in Verdi project

           Figure 1: Overall Workflow of the Study
                                                                          and generates more concise proof scripts, thereby ad-
                                                                          vancing the efficiency and effectiveness of automated
with an empirical investigation into the limitations of exist-            proof synthesis.
ing tools, followed by the design and evaluation of PGTS.
This algorithm is a simple yet effective plug-and-play mod-             The remainder of this paper is organized as follows.
ule that integrates seamlessly with existing proof synthesis        Section 2 presents the background of this study. Section 3
tools. This idea is also motivated by our observation of exist-     describes the experimental setup and methodology of our
ing proof synthesis tool architectures: they typically generate     empirical investigation. Section 4 reports the results and
tactics for individual proof steps in isolation, overlooking the    findings for each of our research questions. Section 5 dis-
correlations and dependencies between tactics across differ-        cusses the implications of these findings in detail. Section 6
ent steps within a proof. Specifically, we utilize a sequential     introduces a new method inspired by the findings. Sec-
pattern mining algorithm to identify high-frequency proof           tion 7 presents the experimental evaluation of our proposed
patterns between proof steps in a proof corpus. These pat-          method. Section 8 discusses limitations and threats to the
terns capture common relationships between proof steps that         validity of our study. Section 9 reviews related work. Finally,
reflect human expert reasoning conventions. By templating           Section 10 concludes the paper.
these mined patterns, PGTS reranks the candidate tactics
produced by proof synthesis tools, prioritizing those that
align with the identified patterns. This approach enables the       2. Background
proof search to more closely follow human-like reasoning                This section provides a brief introduction to interactive
trajectories. Experimental results on the CoqGym bench-             theorem provers, as well as the workflow of proof synthesis
mark show that PGTS increases the number of theorems                tools.
successfully proven by proof synthesis tools by an average of
8.05%. On average, it proves 20% more previously unproven           2.1. Interactive Theorem Provers
theorems. In addition, PGTS is able to handle more complex              ITPs are powerful tools widely used in foundational
theorems while generating more concise proofs. All data             verification tasks, providing a rigorous and structured frame-
from the empirical study, the source code and the evaluation        work for constructing formal proofs. These systems en-
results have been released for replication [11].                    able users to define both data and program specifications
    This paper makes the following contributions:                   alongside corresponding proof goals, offering a controlled
                                                                    environment in which proofs can be developed interactively.
   • To the best of our knowledge, we conduct the first                 In ITPs, the proof process is driven by a sequence of
     systematic study on the effectiveness of automated             user-issued commands known as tactics. These tactics serve
     proof synthesis tools. We highlight key limitations of         as the fundamental building blocks of interaction, allowing
     existing techniques and distill the factors influencing        users to structure and guide proofs in a modular and pro-
     proof success rates.                                           grammable way. Tactics may range from low-level primi-
                                                                    tives, such as simplification, case analysis, or induction, to
   • Inspired by our empirical findings, we propose PGTS,
                                                                    higher-level compositions that encapsulate more complex
     which leverages human expert proof expertise to
                                                                    strategies. During proof development, tactics operate by
     heuristically enhance proof search. As a lightweight
                                                                    manipulating the current proof context and transforming
     and plug-and-play approach, PGTS can be seamlessly
                                                                    the original goal into a sequence of simpler subgoals. This
     integrated into the search processes of existing proof
                                                                    process continues iteratively until all subgoals are reduced to
     synthesis tools, significantly improving their perfor-
                                                                    axioms or previously proven theorems. While users provide
     mance.
                                                                    strategic direction by applying tactics, the system is respon-
   • Our experimental evaluation demonstrates that PGTS             sible for checking the logical validity of each transformation
     significantly enhances the performance of proof syn-           and offering feedback at every step. In this way, ITPs ensure
     thesis tools, achieving an average increase of 8.05%           that all intermediate proof states remain sound under the
     in successfully proven theorems. Additionally, PGTS            formal rules of logic.
     improves the capability to prove complex theorems                  Figure 2 presents an example proof script from the Verdi
                                                                    project, which is concerned with the formal verification of

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                    Page 2 of 17
                                                   Journal of Systems and Software

                                                                    𝑙𝑜𝑐𝑎𝑙 𝑐𝑜𝑛𝑡𝑒𝑥𝑡 of 𝑎𝑠𝑠𝑢𝑚𝑝𝑡𝑖𝑜𝑛𝑠, and 𝑒𝑛𝑣𝑖𝑟𝑜𝑛𝑚𝑒𝑛𝑡 of proven
   intros.                  intros.
                            simpl in |- *.
                                                                    facts, is passed back to the tool for further prediction. This
   simpl in |- *.
                            auto.                                   iterative process continues with the tool generating tactics
          Proof State       updated scripts      ➊ apply h.         and the ITP returning updated proof states until there are
                                                                    no more subgoals. At that point, the tool appends Qed to
           input                                                    complete the script. If a predefined time or step limit is
                                                 ➋ simpl.
                            generate tactics                        reached without completing the proof, the search process is
             Model
                              (beam size 5)                         terminated.
                                                 ➌ auto.
 If compiles, proof state is not
 duplicate, and subgoals still exist,                               3. Empirical Study Methodology
 update proof state and scripts                  ➍ intros.
                                                                       This section describes the experimental setup used in
                                                                    our empirical study, as well as the research questions it
                                                 ➎ trivial.
                                try one by one                      addresses, including the motivation and approach.
                     ITP
Figure 3: An example workflow of step-by-step proof search          3.1. Experimental Setup
and tactic selection                                                3.1.1. Selection of Proof Synthesis Tools
                                                                        In this study, we selected six state-of-the-art (SOTA)
                                                                    proof synthesis tools, including five based on deep learning
distributed systems. The script defines a theorem named             and one based on a large language model. Below, we briefly
trace_outputs_backup, which asserts that any event emitted          summarize the key characteristics of each tool:
solely by the backup node does not contribute to the system’s           ASTactic [12]: ASTactic employs a standard encoder-
observable output. To establish the correctness of this theo-       decoder architecture that represents proof states as abstract
rem, the user interacts with the ITPs by applying a sequence        syntax trees (ASTs). It generates syntactically valid proof
of tactics that incrementally construct the proof. As shown         steps by learning from tree-structured input representations.
in the Figure 2, the proof begins with the keyword Proof                Tac [13]: Tac learns to predict proof steps based on
and concludes with Qed, delineating the start and end of the        the current proof state and the most frequently used Coq
proof process. The intermediate lines (lines 4-6) represent         tactics from existing partial proof scripts. It excludes custom
the specific tactics applied at each step of the derivation. In     tactics and ambiguous parameters to reduce learning noise
this case, the script consists of three proof steps, employing      associated with tactic names.
the tactics intros, simpl, and auto, respectively. These tactics        Tok [13]: Tok extends Tac by modeling the proof state
serve to introduce variables, simplify the goal, and automat-       together with the full token sequence from prior proof
ically discharge the proof based on the context and available       scripts, omitting only punctuation marks. This allows for
lemmas.                                                             finer-grained learning of proof construction patterns.
    In summary, ITPs support a collaborative, step-by-step              Passport [14]: Passport builds upon the Tok framework
construction of formal proofs through the use of tactics. This      by additionally encoding identifier information—such as
interactive workflow allows users to tackle complex veri-           variable and hypothesis names—into the input representa-
fication tasks in a modular and verifiable manner, making           tion, enhancing the model’s awareness of local proof context.
ITPs indispensable tools for applications that demand high              Proverbot9001 [15]: Proverbot9001 decomposes the
assurance and mathematical rigor.                                   proof step prediction task into two stages: tactic prediction
                                                                    and parameter prediction. The final proof step is synthesized
2.2. Proof Synthesis Tools                                          by integrating the outputs of these two components.
    Figure 3 illustrates the workflow of a proof synthesis tool         PALM [16]: PALM adopts a two-stage synthesis pipeline.
performing proof search in an interactive theorem prover            First, it leverages ChatGPT to generate an initial complete
(ITP). To reduce human effort in ITPs, such tools aim to            proof script. This script is then interactively executed in
automate the construction of proof scripts for given theorems       Coq until an error is encountered, at which point a repair
by mimicking the human proof-writing process. Initially, the        mechanism is triggered to correct the script from the failure
proof state contains only the goal, which is the statement of       location onward.
the theorem. The tool encodes this initial state and generates
candidate tactics intended to manipulate the state.                 3.1.2. Dataset
    In the Figure 3, the model predicts five tactics for the            We use the CoqGym benchmark [12] as the test set for
current proof state. These tactics are sequentially attempted       our empirical study. CoqGym is a comprehensive and widely
by the ITP. The first tactic, apply h, fails due to a contextual    adopted dataset for evaluating proof synthesis tools, con-
error. The second, simpl, is syntactically valid but makes          taining 13,137 theorems from 27 open-source Coq projects
no progress, as it reproduces the same proof state. The             on GitHub. We set up the original CoqGym environment
third, auto, successfully advances the proof by producing           and successfully compiled all 27 projects using Coq 8.9.0.
an updated proof state. As a result, auto is appended to the        It is worth noting that previous evaluations of Tac, Tok,
proof script, and the updated state, which includes 𝑠𝑢𝑏𝑔𝑜𝑎𝑙𝑠,       and Passport were conducted on only 26 projects, as these

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                    Page 3 of 17
                                                Journal of Systems and Software

tools failed to run on the coq-library-undecidability project       when dealing with specific types of theorems. Understand-
due to internal Coq errors. In contrast, our experiments            ing how these theorem characteristics specifically affect tool
successfully executed all tools across the complete set of 27       performance can provide valuable guidance for optimizing
projects.                                                           the design of proof synthesis tools.
    Due to version compatibility issues, Proverbot9001 and              Approach: To address RQ1, we systematically inves-
PALM could not be executed in the original CoqGym en-               tigated the characteristics of theorems to understand their
vironment, as both tools only support newer versions of             impact on proof success rates. Specifically, we analyzed
Coq. To overcome this limitation, we reached out to the             theorem complexity through two key dimensions: (1) the
authors of these tools to determine whether they had eval-          classification of theorems as first-order or higher-order, and
uated subsets of the CoqGym benchmark using compatible              (2) the number of logical-mathematical symbols within each
versions of Coq. The authors of Proverbot9001 provided              theorem.
results obtained on a newer Coq version, covering 11,998                For the first dimension, we employed CoqHammer to
theorems across 27 projects. Similarly, PALM was evaluated          attempt proofs for the given theorems. Theorems success-
on 26 projects within a subset of CoqGym, with results              fully proven by CoqHammer were classified as first-order,
publicly available on GitHub. To ensure a fair comparison           leveraging CoqHammer’s capability to translate Coq goals
across all six tools, we took the intersection of their evalu-      into first-order logic. Theorems for which proof attempts
ation sets, resulting in a common subset of 24 projects and         failed were categorized as higher-order. This classification
8,879 theorems. This dataset was used to evaluate RQ1 and           provides a robust framework for distinguishing theorem
RQ2, which focus on understanding the limitations of proof          types and analyzing their relationship with proof success
synthesis tools from two perspectives: the characteristics of       rates in automated theorem proving.
the theorems themselves and human-written proof scripts.                For the second dimension, we quantified theorem com-
For RQ3, which investigates the characteristics of the proof        plexity by counting the occurrences of five types of logical-
search process itself, such as the number of proof steps,           mathematical symbols: equivalence operators, implication
branching behavior, and search depth, we required detailed          operators, quantifiers, logical operators, and inequality op-
search trace data. However, such data was not available             erators. A higher count of these symbols indicated greater
for Proverbot9001 and PALM. Therefore, we conducted an              theorem complexity. This quantitative approach enabled us
empirical analysis of the proof search process using only the       to systematically explore how the presence and frequency of
remaining four tools that provide sufficient dynamic search         logical-mathematical symbols influence proof success rates.
information.                                                        By integrating the analysis of theorem type and symbolic
                                                                    complexity with proof outcomes, our study offers nuanced
3.1.3. Environment                                                  insights into the structural and symbolic factors that shape
    Evaluating the performance of theorem proving is com-           the challenges of automated theorem proving, highlighting
putationally expensive, but the workload is highly paralleliz-      the limitations of current tools and informing strategies for
able, allowing the evaluations to be executed in arbitrary          improving their effectiveness.
order. For experiments that could be executed on CoqGym,
we parallelized the evaluation of all theorems by partitioning      3.2.2. RQ2: Which characteristics of proof scripts
them according to project files and running them on a high-                 make them harder to prove with existing proof
performance computing (HPC) server. The HPC environ-                        synthesis tools?
ment was managed using the Slurm workload manager.                       Motivation: The structure and composition of proof
The server was equipped with dual AMD 7285H 32-core                 scripts play a pivotal role in formal proof construction.
processors (totaling 64 cores), 256 GB of DDR4 memory,              A well-structured theorem script enhances readability and
and a base clock frequency of 2.5 GHz.                              maintainability and significantly impacts the proof process’s
                                                                    efficiency. Studying the structural characteristics of theo-
3.2. Research Questions                                             rem scripts can reveal critical bottlenecks in the proof pro-
3.2.1. RQ1: Which characteristics of theorems make                  cess, such as redundant tactic invocations, suboptimal proof
       them harder to prove with existing proof                     strategies, or ineffective lemma decomposition. Identifying
       synthesis tools?                                             these bottlenecks provides valuable insights into how proofs
    Motivation: The structure and characteristics of the-           can be streamlined, potentially reducing the time and com-
orems (such as complexity, logical relationships) play a            putational resources required for verification.
crucial role in the success rate of proof synthesis tools.               Approach: To study RQ2, we summarized the charac-
Simple theorems may only require basic logical reasoning,           teristics of proof scripts to investigate their relationship with
whereas more complex theorems often involve challenging             proof success rates. Specifically, our analysis focused on two
features such as recursive structures, higher-order logic, or       key aspects:
dependent types. By analyzing the relationship between the               1) Lemma Usage: We identified a distinctive feature
characteristics of theorems and the performance of tools,           within proof scripts—the use of lemmas. To explore the
we can identify the limitations of existing proof synthesis         impact of lemma introduction on proof success rates, we ex-
tools. This analysis also helps pinpoint their weaknesses           tracted proof scripts that invoked previously defined lemmas


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                      Page 4 of 17
                                                Journal of Systems and Software

during the proof process. This allows us to analyze whether         calculated the average number of tactic attempts per proof
existing proof synthesis tools struggle more with proofs that       step. This metric corresponds to the average number of child
require the introduction of auxiliary lemmas.                       nodes for each parent node at every level of the proof search
    2) Proof Pattern: Proof patterns in proof scripts refer to      tree, offering insights into the search process’s efficiency and
the recurring relationships between tactics within a proof          branching behavior.
sequence. These patterns capture the underlying logical rea-            Additionally, we identified three distinct types of tactics
soning connections between proof steps and reflect the typ-         encountered during the search process:
ical strategies used in human-driven proofs. We used the                1) Error tactics: These tactics are directly rejected by the
PrefixSpan [17, 18] sequential pattern mining algorithm to          interactive theorem prover, resulting in an error message due
identify frequent patterns in proof strategies. These patterns      to semantic invalidity.
were then classified by two authors of the paper based on               2) Stagnation tactics: These tactics are accepted by the
their intended purpose in proofs. The inter-annotator agree-        interactive theorem prover but generate proof subgoals that
ment, measured by Cohen’s Kappa coefficient, reached 0.90,          are redundant, duplicating previously proven goals and fail-
indicating excellent consistency. Following discussions to          ing to advance the proof.
resolve classification discrepancies, we ultimately catego-             3) Progress tactics: These tactics successfully advance
rized the proof patterns into six distinct types: Introduc-         the proof by transforming the current goal into new, non-
tion, Simplification, Application, Rewriting, Automation,           redundant subgoals.
and Analysis. Subsequently, we conducted statistical anal-              To examine whether alignment with human expert proof
yses to determine the prevalence rates of these six proof           patterns contributes to improved proof success, we con-
patterns.                                                           ducted a detailed analysis of the proportion of human-like
    This experimental design aims to provide a compre-              tactics within each of the three identified tactic types. We
hensive understanding of how structural characteristics of          traverse the proof search tree and examine the relationships
proof scripts, such as lemma usage and pattern, influence the       between parent and child nodes. For each node, we de-
success of proof synthesis tools. By examining these factors,       termine whether it conforms to a proof pattern. Using the
we aim to identify patterns and insights that can guide the         previously defined three types of nodes, we then compute the
development of more effective proof automation strategies.          proportion of pattern-conforming nodes within each type.
                                                                    This investigation aims to assess the potential of human-
3.2.3. RQ3: How does the search process in existing                 guided heuristics in distinguishing effective proof strate-
        proof synthesis tools affect proof synthesis?               gies from unproductive or erroneous ones, thereby offering
    Motivation: Existing proof synthesis tools predomi-             insights into how human expert reasoning models might
nantly adopt an approach that synthesizes individual proof          be leveraged to enhance the efficiency and reliability of
steps sequentially and constructs complete proofs through           automated proof search.
iterative search. To achieve a more comprehensive evalu-
ation of these tools, it is essential to conduct an in-depth
analysis of their search mechanisms. Specifically, examining        4. Study Results and Analysis
key elements of the search process, such as the number of               This section presents the detailed results of our empirical
proof attempts during the search and the types of proofs            study, providing an analysis of the limitations of existing
generated, can provide valuable insights. The number of             proof synthesis tools from multiple perspectives.
attempts reflects the efficiency of the tool’s search strategy,
while the diversity and nature of the generated proofs reveal       4.1. Results for RQ1
the tool’s capability to explore the proof space effectively.           RQ1: Which characteristics of theorems make them
Analyzing these factors can help identify bottlenecks in the        harder to prove with existing proof synthesis tools?
search process and uncover patterns that contribute to suc-             To answer RQ1, we conduct a comprehensive analysis of
cessful proof synthesis. This research provides a foundation        performance bottlenecks in proof synthesis tools across two
for understanding the limitations of current tools and guiding      key dimensions: theorem types and complexity levels. Fig-
the development of more efficient and robust proof synthesis        ure 4 presents a Sankey diagram illustrating the distribution
methodologies.                                                      of theorem types proven by different proof synthesis tools. In
    Approach: To study RQ3, we modified the code of four            the Sankey diagram, the left side represents different proof
proof synthesis tools and reran their experiments to record         synthesis tools, while the right side represents the types of
detailed information about the proof search process. This           theorems. The flow from a synthesis tool to a theorem type
included capturing the tactics used during the search, their        indicates the proportion of theorems of each type among all
corresponding tactic types, and other relevant metadata.            theorems successfully proven by that tool. From the flow
Each proof’s search process was ultimately represented by           patterns in the diagram, we observe that the majority of the
exploring a proof search tree, which provided a structured          proof attempts by existing tools are concentrated in the first-
view of the tool’s behavior during proof synthesis.                 order logic (FOL) block. This indicates that current tools
    To analyze the relationship between the proof search            are predominantly capable of proving first-order theorems,
process’s characteristics and the tools’ success rates, we          while higher-order theorems remain a significant challenge.


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                     Page 5 of 17
                                                Journal of Systems and Software
                                                                                                              ASTactic                                                             Tac                                                               Tok
    Specifically, Tok exhibits the weakest performance on                                1.0
                                                                                                         Pearson r = -0.3744
                                                                                                                                                            1.0
                                                                                                                                                                            Pearson r = -0.3213
                                                                                                                                                                                                                              1.0
                                                                                                                                                                                                                                              Pearson r = -0.3418

higher-order theorems, with only 15.3% of its successfully                               0.8                                                                0.8                                                               0.8




                                                                    Proof Success Rate




                                                                                                                                       Proof Success Rate




                                                                                                                                                                                                         Proof Success Rate
proven theorems classified as higher-order. Although PALM                                0.6                                                                0.6                                                               0.6

achieves a relatively higher proportion of higher-order the-                             0.4                                                                0.4                                                               0.4


orem proofs (38.6%), the majority of the theorems it proves                              0.2

                                                                                         0.0
                                                                                                                                                            0.2                                                               0.2

                                                                                                                                                            0.0                                                               0.0
are still within the first-order domain. Further analysis of                                   0.0     2.5    5.0     7.5 10.0 12.5 15.0                          0.0     2.5    5.0    7.5 10.0 12.5 15.0                          0.0     2.5    5.0    7.5 10.0 12.5 15.0

PALM’s algorithm reveals that its success in proving a                                                        Passport
                                                                                                         Pearson r = -0.3182
                                                                                                                                                                              Proverbot9001
                                                                                                                                                                            Pearson r = -0.4406
                                                                                                                                                                                                                                                    PALM
                                                                                                                                                                                                                                              Pearson r = -0.2901
                                                                                         1.0                                                                1.0                                                               1.0
large number of theorems can be attributed to its repeated                               0.8                                                                0.8                                                               0.8




                                                                    Proof Success Rate




                                                                                                                                       Proof Success Rate




                                                                                                                                                                                                         Proof Success Rate
invocation of CoqHammer during the proof synthesis pro-                                  0.6                                                                0.6                                                               0.6

cess. Since CoqHammer primarily leverages first-order au-                                0.4                                                                0.4                                                               0.4

tomated reasoning techniques, this suggests that PALM’s                                  0.2                                                                0.2
                                                                                                                                                                                                                              0.2
                                                                                         0.0                                                                0.0
performance is still largely dependent on first-order logic                                    0.0     2.5    5.0     7.5 10.0 12.5 15.0                          0.0     2.5    5.0    7.5 10.0 12.5 15.0
                                                                                                                                                                                                                              0.0
                                                                                                                                                                                                                                    0.0     2.5    5.0    7.5 10.0 12.5 15.0
capabilities.
                                                                    Figure 5: Impact of Logical-Mathematical Symbol Count on
                                                                    Proof Success Rates of Proof Synthesis Tools



                                                                        Figure 6 illustrates the proof success rates of theorems
                                                                    involving different types of logical-mathematical symbols.
                                                                    Notably, theorems containing quantifiers (e.g., ∀, ∃) exhibit
                                                                    the highest proof success rate across all evaluated synthesis
                                                                    tools. In contrast, theorems involving implication operators
                                                                    (→) and logical connectives (∧, ∨, ¬) demonstrate relatively
                                                                    lower success rates. In particular, the presence of logical
                                                                    operators such as conjunction, disjunction, and negation
                                                                    appears to pose the greatest challenge, resulting in the lowest
                                                                    success rates among all categories. This suggests that the
                                                                    complexity introduced by logical connectives may hinder
Figure 4: The proportion of theorem types proven by proof           the performance of current automated proof synthesis tech-
synthesis tools                                                     niques, possibly due to the increased reasoning steps and
                                                                    non-linear dependencies required to handle such structures.
    Figure 5 illustrates the relationship between the num-
                                                                                                                    ASTactic                                                            Tac                                                               Tok
ber of Logical-Mathematical Symbols in theorems and the                                    0.5                                                                0.5                                                              0.5

proof success rate. The regression lines indicate that as                                  0.4                                                                0.4                                                              0.4
                                                                          Success Rate




                                                                                           0.3                                                                0.3                                                              0.3
the number of Logical-Mathematical Symbols increases,                                      0.2                                                                0.2                                                              0.2
the proof success rates of all proof synthesis tools exhibit                               0.1                                                                0.1                                                              0.1
                                                                                           0.0                                                                0.0                                                              0.0
a consistent decline. This trend may be attributed to the
                                                                                                       e
                                                                                                               on

                                                                                                                                 er

                                                                                                                                   l

                                                                                                                                 ty




                                                                                                                                                                          e
                                                                                                                                                                                  on

                                                                                                                                                                                                   er

                                                                                                                                                                                                     l

                                                                                                                                                                                                   ty




                                                                                                                                                                                                                                            e
                                                                                                                                                                                                                                                    on

                                                                                                                                                                                                                                                                     er

                                                                                                                                                                                                                                                                       l

                                                                                                                                                                                                                                                                     ty
                                                                                                                              ica




                                                                                                                                                                                                ica




                                                                                                                                                                                                                                                                  ica
                                                                                                     nc




                                                                                                                                                                        nc




                                                                                                                                                                                                                                          nc
                                                                                                                             ali




                                                                                                                                                                                               ali




                                                                                                                                                                                                                                                                 ali
                                                                                                                            tifi




                                                                                                                                                                                              tifi




                                                                                                                                                                                                                                                                tifi
                                                                                                                ti




                                                                                                                                                                                   ti




                                                                                                                                                                                                                                                     ti
increasing complexity and abstraction introduced by a higher
                                                                                                                          log




                                                                                                                                                                                            log




                                                                                                                                                                                                                                                              log
                                                                                                  ale




                                                                                                                                                                     ale




                                                                                                                                                                                                                                      ale
                                                                                                             ca




                                                                                                                                                                                ca




                                                                                                                                                                                                                                                  ca
                                                                                                                          qu




                                                                                                                                                                                            qu




                                                                                                                                                                                                                                                              qu
                                                                                                                    an




                                                                                                                                                                                       an




                                                                                                                                                                                                                                                         an
                                                                                                         pli




                                                                                                                                                                            pli




                                                                                                                                                                                                                                              pli
                                                                                                 uiv




                                                                                                                                                                    uiv




                                                                                                                                                                                                                                     uiv
                                                                                                                      ine




                                                                                                                                                                                        ine




                                                                                                                                                                                                                                                          ine
                                                                                                                qu




                                                                                                                                                                                   qu




                                                                                                                                                                                                                                                     qu
                                                                                                       im




                                                                                                                                                                          im




                                                                                                                                                                                                                                            im
                                                                                               eq




                                                                                                                                                                  eq




                                                                                                                                                                                                                                    eq




                                                                                                                    Passport                                                    Proverbot9001                                                             PALM
density of symbols, which poses greater challenges for auto-                               0.5                                                                0.5                                                              0.5
                                                                                           0.4                                                                0.4                                                              0.4
mated reasoning and proof construction. Among the tools
                                                                          Success Rate




                                                                                           0.3                                                                0.3                                                              0.3
evaluated, PALM demonstrates the highest stability, with                                   0.2                                                                0.2                                                              0.2

a Pearson correlation coefficient closest to 0, suggesting                                 0.1                                                                0.1                                                              0.1
                                                                                           0.0                                                                0.0                                                              0.0
minimal sensitivity to the increasing number of Logical-
                                                                                                    pli e
                                                                                                  qu n
                                                                                                             er

                                                                                                               l

                                                                                                             ty




                                                                                                                                                                       pli e
                                                                                                                                                                     qu on
                                                                                                                                                                                er

                                                                                                                                                                                  l

                                                                                                                                                                                ty




                                                                                                                                                                                                                                        pli e
                                                                                                                                                                                                                                      qu n
                                                                                                                                                                                                                                                 er

                                                                                                                                                                                                                                                   l

                                                                                                                                                                                                                                                 ty
                                                                                                           ica




                                                                                                                                                                              ica




                                                                                                                                                                                                                                               ica
                                                                                                          nc




                                                                                                                                                                             nc




                                                                                                                                                                                                                                              nc
                                                                                                          tio




                                                                                                                                                                                                                                              tio
                                                                                                         ali




                                                                                                                                                                            ali




                                                                                                                                                                                                                                             ali
                                                                                                        tifi




                                                                                                                                                                           tifi




                                                                                                                                                                                                                                            tifi
                                                                                                                                                                             ti
                                                                                                      log




                                                                                                                                                                         log




                                                                                                                                                                                                                                          log
                                                                                                      ale




                                                                                                                                                                         ale




                                                                                                                                                                                                                                          ale
                                                                                                       ca




                                                                                                                                                                          ca




                                                                                                                                                                                                                                           ca
                                                                                                      qu




                                                                                                                                                                         qu




                                                                                                                                                                                                                                          qu




Mathematical Symbols. Conversely, Proverbot9001 exhibits
                                                                                                     an




                                                                                                                                                                        an




                                                                                                                                                                                                                                         an
                                                                                                 uiv




                                                                                                                                                                    uiv




                                                                                                                                                                                                                                      uiv
                                                                                                  ine




                                                                                                                                                                     ine




                                                                                                                                                                                                                                      ine
                                                                                                       im




                                                                                                                                                                          im




                                                                                                                                                                                                                                            im
                                                                                               eq




                                                                                                                                                                  eq




                                                                                                                                                                                                                                    eq




the lowest stability, with a Pearson correlation coefficient        Figure 6: Proof Success Rates of Theorems by Logical-
approaching -1, indicating a strong negative correlation and        Mathematical Symbol Type
significant vulnerability to the increasing complexity asso-
ciated with a higher symbol count.

  Finding 1: Proof synthesis tools exhibit significant per-                              Finding 2: Theorems with quantifiers (e.g., ∀, ∃) have
  formance bottlenecks as theorem complexity increases.                                  the highest proof success rates across synthesis tools,
  Most tools, including PALM and Tok, perform well                                       while those with implication operators (→) and logi-
  on first-order logic theorems but struggle with higher-                                cal operators (∧, ∨, ¬) show lower success rates, with
  order theorems and those containing a greater number                                   logical connectives posing the greatest challenge due to
  of logical-mathematical symbols.                                                       increased reasoning complexity.




M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                                                                                                                                  Page 6 of 17
                                                                   Journal of Systems and Software

4.2. Results for RQ2                                                                suggesting that these techniques pose greater challenges for
    RQ2: Which characteristics of proof scripts make                                automated tools. This disparity may stem from the inherent
them harder to prove with existing proof synthesis tools?                           complexity of applying rewriting rules and configuring au-
    Figure 7 presents a comparative analysis of proof success                       tomation tactics, which often require a deeper understanding
rates between scenarios involving the introduction of auxil-                        of context-specific transformations and a careful selection of
iary lemmas and those without such additional components.                           parameters or hint databases.
The empirical data clearly demonstrates a consistent pattern
across all proof synthesis tools: the success rates are signif-                                     0.5
                                                                                                          ASTactic
                                                                                                                      0.5
                                                                                                                                 Tac
                                                                                                                                              0.5
                                                                                                                                                        Tok
icantly lower in cases requiring auxiliary lemmas compared                                          0.4               0.4                     0.4




                                                                                     Success Rate
to those that can be completed without lemma introduction.                                          0.3               0.3                     0.3
                                                                                                    0.2               0.2                     0.2
This systematic discrepancy suggests that the incorporation                                         0.1               0.1                     0.1
of auxiliary lemmas introduces substantial challenges for                                           0.0               0.0                     0.0

automated proof synthesis. Several underlying factors may




                                                                                            pli on
                                                                                          ap ation

                                                                                              rew on
                                                                                          au riting

                                                                                               an n
                                                                                                        sis




                                                                                                                         pli on
                                                                                                                       ap ation

                                                                                                                           rew on
                                                                                                                       au riting

                                                                                                                            an n
                                                                                                                                     sis




                                                                                                                                                 pli on
                                                                                                                                               ap ation

                                                                                                                                                   rew on
                                                                                                                                               au riting

                                                                                                                                                    an n
                                                                                                                                                             sis
                                                                                                        o




                                                                                                                                     o




                                                                                                                                                             o
                                                                                        sim ucti


                                                                                                      ti


                                                                                                    ati




                                                                                                                     sim ucti


                                                                                                                                   ti


                                                                                                                                 ati




                                                                                                                                             sim ucti


                                                                                                                                                           ti


                                                                                                                                                         ati
                                                                                                   aly




                                                                                                                                aly




                                                                                                                                                        aly
                                                                                                   ca




                                                                                                                                ca




                                                                                                                                                        ca
                                                                                                fic




                                                                                              tom




                                                                                                                             fic




                                                                                                                           tom




                                                                                                                                                     fic




                                                                                                                                                   tom
                                                                                               pli




                                                                                                                            pli




                                                                                                                                                    pli
                                                                                             rod




                                                                                                                          rod




                                                                                                                                                  rod
                                                                                         int




                                                                                                                      int




                                                                                                                                              int
contribute to this phenomenon: (1) the process of identify-                                         0.5
                                                                                                          Passport
                                                                                                                      0.5
                                                                                                                             Proverbot9001
                                                                                                                                              0.5
                                                                                                                                                       PALM

ing and formulating appropriate auxiliary lemmas requires                                           0.4               0.4                     0.4




                                                                                     Success Rate
                                                                                                    0.3               0.3                     0.3
higher-level mathematical insight that current automated                                            0.2               0.2                     0.2
systems may lack; (2) the introduction of additional lemmas                                         0.1               0.1                     0.1

increases the complexity of the proof structure, potentially                                        0.0               0.0                     0.0




                                                                                            pli on
                                                                                          ap ation

                                                                                              rew on
                                                                                          au riting

                                                                                               an n
                                                                                                        sis




                                                                                                                         pli on
                                                                                                                       ap ation

                                                                                                                           rew on
                                                                                                                       au riting

                                                                                                                            an n
                                                                                                                                     sis




                                                                                                                                                 pli on
                                                                                                                                               ap ation

                                                                                                                                                   rew on
                                                                                                                                               au riting

                                                                                                                                                    an n
                                                                                                                                                             sis
creating more opportunities for logical inconsistencies or




                                                                                                        o




                                                                                                                                     o




                                                                                                                                                             o
                                                                                        sim ucti


                                                                                                      ti


                                                                                                    ati




                                                                                                                     sim ucti


                                                                                                                                   ti


                                                                                                                                 ati




                                                                                                                                             sim ucti


                                                                                                                                                           ti


                                                                                                                                                         ati
                                                                                                   aly




                                                                                                                                aly




                                                                                                                                                        aly
                                                                                                   ca




                                                                                                                                ca




                                                                                                                                                        ca
                                                                                                fic




                                                                                              tom




                                                                                                                             fic




                                                                                                                           tom




                                                                                                                                                     fic




                                                                                                                                                   tom
                                                                                               pli




                                                                                                                            pli




                                                                                                                                                    pli
                                                                                             rod




                                                                                                                          rod




                                                                                                                                                  rod
                                                                                         int




                                                                                                                      int




                                                                                                                                              int
implementation errors; (3) the need for auxiliary lemmas
often indicates that the original problem is inherently more                        Figure 8: Comparison of Proof Success Rates by Human Expert
                                                                                    Proof Patterns
complex, which naturally leads to lower success rates.


                               1.0                                 Include Lemma
                                                                         True                 Finding 4: Proof synthesis tools perform best on intro-
                                                                         False                duction and analysis patterns, but exhibit lower success
                               0.8                                                            rates on rewriting and automation, reflecting difficulties
Theorem Proving Success Rate




                                                                                              in managing context-sensitive transformations and tac-
                               0.6                                                            tic configuration.


                               0.4                                                  4.3. Results for RQ3
                                                                                         RQ3: How does the search process in existing proof
                                                                                    synthesis tools affect proof synthesis?
                               0.2
                                                                                         To address RQ3, we conducted an in-depth investigation
                                                                                    into the characteristics of tactic usage during the proof
                               0.0                                                  search process. Specifically, we analyzed the relationship
                                                                                    between search depth and the number of tactic attempts
                                      tic


                                            c



                                                 k



                                                       ort




                                                                         LM
                                                                   01
                                            Ta



                                                 To
                                        c




                                                                  t90
                                                      ssp




                                                                        PA




                                                                                    required to make progress in the proof. As shown in Figure 9,
                                     Ta




                                                               rbo
                                     AS




                                                      Pa



                                                              ve




                                                                                    a significantly larger number of tactics are attempted during
                                                             Pro




                                                                                    the initial stages of proof search, indicating that identifying a
Figure 7: Comparative Analysis of Proof Success Rates With                          viable direction early in the proof is particularly challenging.
and Without Auxiliary Lemma Introduction
                                                                                    As the proof progresses to greater depths, the number of
                                                                                    required tactic attempts tends to decrease, suggesting that
                                                                                    once a productive path is found, the search becomes more
                Finding 3: Automated proof synthesis tools exhibit                  focused and efficient.
                significantly lower success rates on theorems requiring                  Moreover, our analysis reveals a clear distinction be-
                auxiliary lemmas, highlighting their limitations in han-            tween successful and failed proofs: theorems that ultimately
                dling structurally complex or insight-intensive proofs.             fail to be proven consistently require a much higher number
                                                                                    of tactic attempts throughout the search process. A closer
    Figure 8 illustrates the proof success rates associated                         inspection suggests that this is due to the model’s tendency
with different human expert proof patterns observed in the                          to assign high probabilities to tactics that either lead to errors
proof scripts. Among the various patterns, the "Introduc-                           or result in redundant proof states. As a consequence, the
tion" and "Analysis" patterns exhibit the highest success                           search must explore a larger number of low-ranked tactics to
rates, indicating that current proof synthesis tools are more                       find one that successfully advances the proof. This behavior
effective when dealing with goal decomposition and case                             highlights a key limitation of current tactic prediction mod-
analysis tasks. In contrast, patterns such as "Rewriting"                           els: while they may be syntactically confident, their semantic
and "Automation" show comparatively lower success rates,                            alignment with proof progress is often weak, especially in

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                                    Page 7 of 17
                                                                    Journal of Systems and Software

                                          Successful Proof Search                                             Failed Proof Search
                        20
Avg. Tactics per Step

                        15
    (a) ASTactic




                        10

                         5
                          1
                          2
                          3
                          4
                          5
                          6
                          7
                          8
                          9
                         10
                         11
                         12
                         13
                         14
                         15
                         16
                         17
                         18
                         19
                         20
                         21
                         22
                         23
                         24
                         25
                         26
                         27
                         28
                         29
                         30
                         31
                         32
                         33
                         34
                         35
                         36
                         37
                         38
                         39
                         40
                         41
                         42
                         43
                         44
                         45
                         46
                         47
                         48
                         49
                         50



                                                                                        1
                                                                                        2
                                                                                        3
                                                                                        4
                                                                                        5
                                                                                        6
                                                                                        7
                                                                                        8
                                                                                        9
                                                                                       10
                                                                                       11
                                                                                       12
                                                                                       13
                                                                                       14
                                                                                       15
                                                                                       16
                                                                                       17
                                                                                       18
                                                                                       19
                                                                                       20
                                                                                       21
                                                                                       22
                                                                                       23
                                                                                       24
                                                                                       25
                                                                                       26
                                                                                       27
                                                                                       28
                                                                                       29
                                                                                       30
                                                                                       31
                                                                                       32
                                                                                       33
                                                                                       34
                                                                                       35
                                                                                       36
                                                                                       37
                                                                                       38
                                                                                       39
                                                                                       40
                                                                                       41
                                                                                       42
                                                                                       43
                                                                                       44
                                                                                       45
                                                                                       46
                                                                                       47
                                                                                       48
                                                                                       49
                                                                                       50
                                          Successful Proof Search                                             Failed Proof Search
                        20
Avg. Tactics per Step




                        15
       (b) Tac




                        10

                         5
                          1
                          2
                          3
                          4
                          5
                          6
                          7
                          8
                          9
                         10
                         11
                         12
                         13
                         14
                         15
                         16
                         17
                         18
                         19
                         20
                         21
                         22
                         23
                         24
                         25
                         26
                         27
                         28
                         29
                         30
                         31
                         32
                         33
                         34
                         35
                         36
                         37
                         38
                         39
                         40
                         41
                         42
                         43
                         44
                         45
                         46
                         47
                         48
                         49
                         50



                                                                                        1
                                                                                        2
                                                                                        3
                                                                                        4
                                                                                        5
                                                                                        6
                                                                                        7
                                                                                        8
                                                                                        9
                                                                                       10
                                                                                       11
                                                                                       12
                                                                                       13
                                                                                       14
                                                                                       15
                                                                                       16
                                                                                       17
                                                                                       18
                                                                                       19
                                                                                       20
                                                                                       21
                                                                                       22
                                                                                       23
                                                                                       24
                                                                                       25
                                                                                       26
                                                                                       27
                                                                                       28
                                                                                       29
                                                                                       30
                                                                                       31
                                                                                       32
                                                                                       33
                                                                                       34
                                                                                       35
                                                                                       36
                                                                                       37
                                                                                       38
                                                                                       39
                                                                                       40
                                                                                       41
                                                                                       42
                                                                                       43
                                                                                       44
                                                                                       45
                                                                                       46
                                                                                       47
                                                                                       48
                                                                                       49
                                                                                       50
                                          Successful Proof Search                                             Failed Proof Search
                        20
Avg. Tactics per Step




                        15
       (c) Tok




                        10

                         5
                          1
                          2
                          3
                          4
                          5
                          6
                          7
                          8
                          9
                         10
                         11
                         12
                         13
                         14
                         15
                         16
                         17
                         18
                         19
                         20
                         21
                         22
                         23
                         24
                         25
                         26
                         27
                         28
                         29
                         30
                         31
                         32
                         33
                         34
                         35
                         36
                         37
                         38
                         39
                         40
                         41
                         42
                         43
                         44
                         45
                         46
                         47
                         48
                         49
                         50



                                                                                        1
                                                                                        2
                                                                                        3
                                                                                        4
                                                                                        5
                                                                                        6
                                                                                        7
                                                                                        8
                                                                                        9
                                                                                       10
                                                                                       11
                                                                                       12
                                                                                       13
                                                                                       14
                                                                                       15
                                                                                       16
                                                                                       17
                                                                                       18
                                                                                       19
                                                                                       20
                                                                                       21
                                                                                       22
                                                                                       23
                                                                                       24
                                                                                       25
                                                                                       26
                                                                                       27
                                                                                       28
                                                                                       29
                                                                                       30
                                                                                       31
                                                                                       32
                                                                                       33
                                                                                       34
                                                                                       35
                                                                                       36
                                                                                       37
                                                                                       38
                                                                                       39
                                                                                       40
                                                                                       41
                                                                                       42
                                                                                       43
                                                                                       44
                                                                                       45
                                                                                       46
                                                                                       47
                                                                                       48
                                                                                       49
                                                                                       50
                                          Successful Proof Search                                             Failed Proof Search
                        20
Avg. Tactics per Step




                        15
    (d) Passport




                        10

                         5
                          1
                          2
                          3
                          4
                          5
                          6
                          7
                          8
                          9
                         10
                         11
                         12
                         13
                         14
                         15
                         16
                         17
                         18
                         19
                         20
                         21
                         22
                         23
                         24
                         25
                         26
                         27
                         28
                         29
                         30
                         31
                         32
                         33
                         34
                         35
                         36
                         37
                         38
                         39
                         40
                         41
                         42
                         43
                         44
                         45
                         46
                         47
                         48
                         49
                         50



                                                                                        1
                                                                                        2
                                                                                        3
                                                                                        4
                                                                                        5
                                                                                        6
                                                                                        7
                                                                                        8
                                                                                        9
                                                                                       10
                                                                                       11
                                                                                       12
                                                                                       13
                                                                                       14
                                                                                       15
                                                                                       16
                                                                                       17
                                                                                       18
                                                                                       19
                                                                                       20
                                                                                       21
                                                                                       22
                                                                                       23
                                                                                       24
                                                                                       25
                                                                                       26
                                                                                       27
                                                                                       28
                                                                                       29
                                                                                       30
                                                                                       31
                                                                                       32
                                                                                       33
                                                                                       34
                                                                                       35
                                                                                       36
                                                                                       37
                                                                                       38
                                                                                       39
                                                                                       40
                                                                                       41
                                                                                       42
                                                                                       43
                                                                                       44
                                                                                       45
                                                                                       46
                                                                                       47
                                                                                       48
                                                                                       49
                                                                                       50
                                                Proof Depth                                                       Proof Depth

                    Figure 9: Relationship Between Proof Search Depth and Number of Tactic Attempts for Successful and Failed Theorems



  complex or ambiguous proof states. These findings suggest                          human expert proof patterns strongly correlates with the
  that improving the accuracy and utility of tactic ranking,                         syntactic and semantic validity of tactics in automated proof
  particularly in the early stages of proof search, is essential                     search.
  for enhancing proof synthesis performance.
                                                                                       Finding 6: Tactics that advance proofs in automated
             Finding 5: Failed proof search involves significantly                     proof search show the highest alignment with human ex-
             more tactic attempts, largely due to the model’s overcon-                 pert proof patterns, followed by those causing redundant
             fidence in tactics that lead to errors or redundant states,               states, while error-inducing tactics exhibit the lowest
             highlighting the need for more semantically informed                      alignment, indicating a strong correlation between hu-
             tactic ranking.                                                           man expert proof pattern alignment and tactic validity.

      Figure 10 presents the proportion of tactics attempted
  during the proof search process that align with human expert                       5. Implications
  proof patterns. Our analysis reveals that the proportion of                            This section discusses the implications derived from our
  tactics conforming to human expert proof patterns is sig-                          findings (Findings 1–6). We outline several insights that
  nificantly higher among those that successfully advance the                        could inspire improvements for future proof synthesis tools.
  proof compared to tactics that fail or result in redundant
  states. Specifically, tactics that advance the proof exhibit                       5.1. Design Implications for Automated Proof
  the highest alignment with human expert proof patterns,                                 Synthesis Tools
  followed by those leading to redundant states, while tactics                           Automated proof synthesis tools must be capable of
  resulting in errors show the lowest alignment. Notably, both                       handling varying levels of theorem complexity and logical
  tactics that advance the proof and those leading to redundant                      structure. Our study reveals several performance bottle-
  states interact with the interactive theorem prover without                        necks, highlighting the need for improvements in both tool
  triggering errors. These results indicate that alignment with                      architecture and tactic selection mechanisms. Based on these

  M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                  Page 8 of 17
                                                                                                          Journal of Systems and Software

                                                   $ 6 7 D F W L F                                  7 D F                  involving quantifiers (e.g., ∀, ∃) tend to have higher proof
                                                                                                                       success rates, whereas those involving implication (→) and
                                                                                                                       logical connectives such as conjunction (∧), disjunction (∨),
  3 U R S R U W L R Q



                                                                                                                           and negation (¬) show significantly reduced performance
                            
                                                                                                                           (Finding 2). In particular, the presence of logical connectives
                            
                                                                                                                           creates nonlinear dependency relationships and branched
                                                                                                                       structures, which existing tools typically cannot handle ef-
                                                                                                                           ficiently. This limitation indicates a fundamental representa-
                                     U R U




                                                                          V



                                                                                U R U




                                                                                                                     V
                                                         R Q




                                                                                                    R Q
                                                                      U H V




                                                                                                                 U H V
                                                                                                                           tional shortcoming in current logical encoding methods.
                                                   D W L




                                                                                              D W L
                                    ( U




                                                                               ( U
                                                                   R J




                                                                                                              R J
                                                 J Q




                                                                                            J Q
                                                                  3 U




                                                                                                             3 U
                                              6 W D




                                                                                         6 W D
                                                                                                                                Symbolic representation learning aims to encode the
                                                         7 R N                                3 D V V S R U W              logical structure, symbolic relationships, and semantic roles
                            
                                                                                                                           of theorem components into vector or graph representations
                                                                                                                       that can guide tactic prediction. When this representation is
  3 U R S R U W L R Q




                                                                                                                       insufficient, tools may struggle to capture the complex in-
                                                                                                                       teractions among symbols. This often leads to performance
                            
                                                                                                                           degradation, especially in the presence of implication and
                                                                                                                           connectives. Existing methods may over-rely on syntactic
                                                                                                                           patterns while overlooking deeper semantic roles. To over-
                                     U R U




                                                                          V



                                                                                U R U




                                                                                                                     V
                                                       R Q




                                                                                                  R Q
                                                                      U H V




                                                                                                                 U H V
                                                   D W L




                                                                                              D W L
                                    ( U




                                                                               ( U
                                                                   R J




                                                                                                              R J
                                                 J Q




                                                                                            J Q




                                                                                                                           come this challenge, future tools could incorporate seman-
                                                                  3 U




                                                                                                             3 U
                                              6 W D




                                                                                         6 W D




                                                                                                                           tically enriched embeddings. For example, the implication
Figure 10: Correlation of Human Expert Proof Pattern Align-                                                                symbol (→) could be labeled as a “hypothesis introduction”
ment with Tactic Effectiveness in Proof Search                                                                             trigger, indicating its role in conditional reasoning. Such se-
                                                                                                                           mantic labeling helps the model distinguish between syntac-
                                                                                                                           tic forms that require different proof strategies. Additionally,
findings, we present a set of suggestions for enhancing future                                                             the low success rate for implication-heavy theorems may
proof synthesis tools.                                                                                                     stem from the model’s inability to learn how implication
    An effective direction for future proof synthesis tools                                                                interacts with other symbols. As a simple example, the
is the joint prediction of tactics and theorem types, en-                                                                  frequent co-occurrence of ∀ and → often corresponds to
abling more context-aware and accurate proof generation.                                                                   inductive or assumption-based proofs. Learning such inter-
We observe a notable decline in the performance of existing                                                                action patterns can guide the model toward more suitable
synthesis tools as theorem complexity increases (Finding                                                                   tactic choices in complex proof scenarios.
1). Although many SOTA tools (e.g., PALM and Tok)                                                                               Current proof synthesis tools should incorporate lemma
achieve high success rates on first-order logic theorems,                                                                  suggestion mechanisms as an essential component of their
their performance degrades significantly when faced with                                                                   architecture. Our analysis reveals that many theorems re-
higher-order logic or theorems involving dense symbolic                                                                    quire the introduction of intermediate lemmas to complete
mathematical structures. This indicates that current tools                                                                 a successful proof. However, most existing systems lack the
struggle to perform effective tactic prediction for complex                                                                ability to identify or exploit such auxiliary lemmas, resulting
theorems.                                                                                                                  in significantly lower success rates on theorems that inher-
    To overcome this limitation in Finding 1, one promis-                                                                  ently depend on intermediate reasoning steps (Finding 3). To
ing approach involves classifying proof tactics and labeling                                                               overcome this limitation, future tools should include ded-
those that are typically used either individually or in com-                                                               icated lemma discovery modules capable of automatically
bination in the proofs of complex theorems. For example,                                                                   detecting when a particular proof state cannot be resolved
in Coq, complex proofs often involve tactics such as in-                                                                   by local tactics alone and instead requires the formulation
duction, inversion, apply, and rewrite, frequently combined                                                                of a supporting lemma. This involves not only recognizing
with auxiliary lemmas and structured proof planning. Based                                                                 the need for a lemma but also retrieving or generating a
on this observation, future synthesis tools could incorporate                                                              relevant lemma that can bridge the current proof gap. For
explicit complexity-awareness mechanisms. For instance,                                                                    example, in Coq, proving the associativity of list concatena-
the tool could begin by classifying the input theorem ac-                                                                  tion often requires the application of previously established
cording to its structural and symbolic complexity, and then                                                                lemmas about the identity element or the generalization
dynamically adjust its tactic generation strategy accordingly.                                                             of the induction hypothesis. These steps typically demand
Furthermore, a multi-task learning-based tactic synthesizer                                                                human expert insight or multi-step reasoning, which most
could be trained to jointly predict both the next tactic and the                                                           current synthesis tools are not equipped to handle effec-
complexity category of the current proof subgoal.                                                                          tively. By integrating a lemma suggestion module, proof
    Future proof synthesis tools may require more fine-                                                                    synthesis systems can more efficiently resolve intermediate
grained symbolic and semantic representation capabilities.                                                                 proof states that would otherwise hinder progress. Such
Further analysis reveals that not all logical symbols con-                                                                 mechanisms are especially critical for theorems that require
tribute equally to proof difficulty. For instance, theorems                                                                auxiliary insights, structural decomposition, or multi-hop


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                                                            Page 9 of 17
                                                 Journal of Systems and Software

reasoning. A well-designed lemma suggestion module has              common human expert proof patterns, whereas tactics lead-
the potential to substantially improve performance in these         ing to redundant states or errors tend to exhibit lower align-
more challenging cases, thereby narrowing the gap between           ment (Finding 6). This strong correlation suggests that con-
automated and human-driven theorem proving.                         sistency with human proof strategies can serve as a powerful
     Proof search strategies should be tailored according to        inductive bias when training proof synthesis models. Future
the type of tactic pattern. Our analysis reveals that the tactic    proof synthesis tools may leverage annotated human expert
category used significantly impacts the automated proofs’           proof traces, employ imitation learning from expert tactic
success rate. In particular, introduction and analytic tactics      sequences, or incorporate preference modeling based on
yield higher success rates, while rewriting and automation-         human interaction logs. Additionally, prioritizing tactics that
related tactics often underperform (Finding 4). This sug-           align with human expert proof patterns during proof search
gests that certain tactics, especially those requiring context-     may further facilitate the synthesis of complete proof scripts.
sensitive transformations or fine-grained configuration, pose       These approaches not only enhance the quality of tactic
greater challenges for existing automated proof synthesis           selection but also improve the interpretability of the proof
tools. To enhance the robustness of proof automation across         process and its adaptability to user feedback.
diverse tactic patterns, future tools may benefit from pattern-
aware adjustments during proof search. This could involve
dynamically selecting or prioritizing tactic sequences based        6. Automated Proof Synthesis via PGTS
on the recognized tactic type. For example, when the tools               Existing proof synthesis tools typically generate tactics
detect that a low-performing tactic category (e.g., rewriting)      for individual proof steps without considering the logical
is likely needed, it could trigger selective tactic expansion,      reasoning relationships between them. However, human ex-
exploring multiple variants or alternatives more exhaus-            pert reasoning patterns that reflect the dependencies and
tively. Additionally, constraint-based filtering mechanisms         logical progression between proof steps are often crucial to
could be introduced to suppress low-confidence tactic ap-           constructing coherent proofs. According to RQ3, proofs that
plications, especially in cases where the model’s prediction        align with human-written patterns tend to be more successful
confidence does not meet a predefined threshold. Such ap-           in the search process. This finding inspires us to consider
proaches can reduce the search space and improve reliability        whether guiding proof search with such patterns can im-
by avoiding unproductive or misleading proof paths.                 prove success rates. To explore this, we investigate pattern-
                                                                    guided tactical search strategies to enhance existing depth-
5.2. Learning Implications for Human-Guided                         first search methods. Specifically, we first extract common
     Proof Strategies                                               proof patterns from a large-scale corpus of human-written
    While tool-level improvements are essential, a deeper           proofs and formalize these patterns into reusable templates.
integration of human-like reasoning patterns offers a com-          In this way, we integrate the mined human expert proof
plementary path forward. Our findings demonstrate that              patterns into the proof search process, providing heuristic
alignment with expert proof behavior significantly correlates       guidance to steer the search more effectively.
with tactic validity and overall proof success, suggesting new
directions for training and designing synthesis strategies.         6.1. Mining Proof Pattern
    Proof synthesis tools should incorporate human expert               To obtain human-written proof patterns, we follow the
involvement or more advanced proof strategies to address            methodology outlined in RQ2 for extracting proof patterns.
model uncertainty. Our analysis reveals that proof failures         First, we convert 57,719 human-written proof scripts from
are often associated with an increased number of tactic at-         the CoqGym training set into sequential data. In this step,
tempts, particularly when the model overconfidently selects         each tactic in a proof script is treated as an individual item
tactics that lead to incorrect or redundant goals (Finding          in a sequence, and the tactics are recorded in the order
5). This suggests that proof synthesis models exhibit high          they are executed. Furthermore, we normalize the tactic
probabilistic uncertainty from the outset in cases where            sequences by unifying tactic parameters (i.e., simplifying
they eventually fail. To handle such uncertainty, greater           parameterized tactics into their parameter-free forms) and
human interaction should be incorporated when the model’s           handling compound tactics (i.e., decomposing tactic chains
predicted tactic distributions are highly uncertain. Alter-         separated by semicolons, such as intros; simpl; auto, into
natively, retrieval-augmented methods can be employed to            individual items). Through this preprocessing, we obtain
improve the accuracy of tactic prediction by providing rel-         standardized sequences of proof tactics.
evant contextual information from existing proofs. These                Next, we apply the PrefixSpan sequential pattern min-
approaches can help reduce failure rates, improve the robust-       ing algorithm to extract human-written proof patterns. We
ness of automated proof synthesis, and allow the system to          follow a common practice in setting the pattern mining
better leverage human intuition and domain expertise.               threshold. Specifically, we extract patterns that appear with
    Human-written proof patterns can guide both training            a frequency greater than 1% in the dataset [19]. Since proof
and proof search processes. We observe that tactics which           scripts typically consist of a series of ordered tactics and
successfully advance a proof are more likely to align with          exhibit temporal or event sequences characteristics, the Pre-
                                                                    fixSpan algorithm is well-suited for this task. PrefixSpan


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                   Page 10 of 17
                                                  Journal of Systems and Software

focuses on mining frequent subsequences by recursively pro-          These pattern-matching tactics are sorted in descending
jecting the sequence database to discover patterns, thereby          order of their frequency in the pattern database. Second, any
avoiding generating an excessive number of candidate se-             tactics that do not match a known pattern are sorted by the
quences. Since the PrefixSpan algorithm mines all frequent           original neural network confidence scores. The re-ranked list
subsequences, it may include non-contiguous patterns with            combines both subsets, prioritizing pattern-aligned tactics
large spans. Therefore, to ensure that the mined patterns are        while still considering the model’s statistical predictions.
strictly contiguous, we apply a filtering step to retain only            The proof search continues by sequentially trying the re-
strictly contiguous patterns.                                        ordered tactics with the interactive theorem prover. If a tactic
                                                                     successfully leads to proof completion, meaning no subgoals
6.2. Pattern-Guided Tactic Search                                    remain, the proof is considered successful, and the system
     The proof synthesis tool is designed to generate can-           returns the accumulated proof sequence (Lines 12–15). The
didate tactics for advancing each proof step. It employs             process is terminated and reported as unsuccessful if the
a step-by-step search strategy to construct complete proof           proof search exceeds a predefined maximum number of
sequences. The proof search can be modeled as a tree search,         tactic attempts or a time threshold (Lines 16-17). We follow
where each node represents a candidate tactic generated by           the settings used in prior work by imposing a maximum
the automated synthesis tool, and a path from the root to            time limit of 600 seconds and restricting the total number
a leaf corresponds to a potential complete proof sequence.           of tactic applications to 300. These constraints ensure a fair
This search process is formally described in Algorithm 1,            comparison with existing approaches and prevent the search
which integrates neural predictions with mined human ex-             process from running indefinitely.
pert proof patterns to guide and prioritize tactic application
during proof construction.
     Specifically, The proof process begins with an initial          7. Evaluation
goal derived from the theorem to be proven. At this point,               Our evaluation answers three research questions:
a neural network is used to generate the top-k candidate
tactics that most likely apply to the current goal (Line 3).            • RQ4 (Effectiveness): Does PGTS enhance the effec-
The value of k for the top-k candidate tactics is set to 20,              tiveness of theorem proving?
following the default configuration used in prior work. Since           • RQ5 (Capability): Does PGTS enhance the ability of
the initial goal has no associated parent tactic, it cannot               proof synthesis tools to generate complex theorems?
be matched against any binary tactic transition patterns
mined from human proofs (Lines 32-34). Consequently, the                • RQ6 (Quality): Does PGTS improve the quality of
candidate tactics are attempted strictly in descending order              proof generation?
of the probabilities output by the neural network.
     The system attempts to apply each tactic in the top-k           7.1. Evaluation Setup
list using the interactive theorem prover (Lines 10-11). If          7.1.1. Benchmark
the application of a tactic results in an error or if the new             Dataset. We use CoqGym, a widely adopted benchmark
proof goal it generates has already been seen (Lines 16-18),         for evaluating theorem-proving synthesis tools. The Coq-
the system skips to the next tactic in the list. When a tactic       Gym benchmark consists of 124 open-source Coq projects.
successfully advances the proof by producing a new, unseen           Its training set includes 57,719 theorems from 97 projects,
proof goal, it is added to the proof sequence and recorded as        while the test set contains 13,137 theorems from 27 projects.
the parent tactic for future pattern matching (Lines 22–26).         We extract common human-written proof patterns from the
It is important to note that if none of the top-k candidate          proof sequences in the training set and evaluate their effec-
tactics generated for a given goal successfully advance the          tiveness on the test set.
proof, the system performs backtracking (Lines 6-9). In this              Base model. Our goal is to develop a general proof
case, it returns to the preceding proof goal and resumes             search optimization method. We selected four proof syn-
the search by attempting the remaining, previously untried           thesis tools, ASTactic, Tac, Tok, and Passport, as baseline
tactics associated with the parent node. This mechanism              models. All of these utilize a DFS proof search strategy.
ensures that the search does not terminate prematurely and           Additionally, to better evaluate the effectiveness of our pro-
can explore alternative proof paths when an initially chosen         posed approach, we implemented Restricted Pattern-Guided
tactic sequence fails.                                               Tactic Search (RPGTS), a variant of PGTS that prioritizes
     The new proof goal then undergoes the same process:             only parameterized tactics that match predefined patterns.
the neural network predicts a new set of top-k tactics. This
time, however, our Pattern-Guided Tactic Search (PGTS)               7.1.2. Evaluation Metrics
algorithm re-ranks the neural network outputs based on                   For RQ4, we use Total Added Value and Unique Added
frequent tactic transition patterns previously mined from            Value to evaluate the extent to which PGTS enhances the
human-written proofs (Lines 35-37). PGTS reorders the                proof capabilities of existing proof synthesis tools. The
candidate tactics in two stages. First, it identifies tactics that   detailed definitions of these two metrics are provided below.
match a known binary pattern with the current parent tactic.             Total Added Value: This metric shows how much better
                                                                     tool A performs compared to tool B by calculating the

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                     Page 11 of 17
                                                Journal of Systems and Software

 Algorithm 1: PGTS: Pattern-Guided Tactic Search
   Input: Initial goal 𝐺, Pattern frequency table 𝑃 , Neural network predictor 𝑁𝑁, Top-𝑘 = 20
   Output: Proof sequence or "No proof found"
 1 Function ProofSearch(𝐺, 𝑃 , 𝑁𝑁):
 2    𝑃 𝑟𝑜𝑜𝑓 ← [] ;                                                                                  // Proof sequence
 3    𝑆𝑡𝑎𝑐𝑘 ← push_sorted(𝑃 𝐺𝑇 𝑆(𝐺, null, 𝑃 , 𝑁𝑁)) ;                   // Push init top-k tactics, top-1 at stack top
 4    𝑆𝑒𝑒𝑛 ← {𝐺} ;                                                                  // Seen goals to detect repetition
 5    while 𝑆𝑡𝑎𝑐𝑘 ≠ [[]] do
 6        if 𝑆𝑡𝑎𝑐𝑘[−1] = [] then
 7             𝑆𝑡𝑎𝑐𝑘.pop(), 𝑃 𝑟𝑜𝑜𝑓 .pop(), 𝑈 𝑛𝑑𝑜() ;                                                      // Backtrack
 8             continue
 9        end
10        𝑇 𝑎𝑐𝑡𝑖𝑐 ← 𝑆𝑡𝑎𝑐𝑘[−1].pop() ;                                              // get tactic to apply current goal
11        (𝑅𝑒𝑠𝑢𝑙𝑡, 𝐺) ← 𝐴𝑝𝑝𝑙𝑦𝑇 𝑎𝑐𝑡𝑖𝑐(𝑇 𝑎𝑐𝑡𝑖𝑐, 𝐺) ;                                 // prove result and next proof goal
12        if 𝑅𝑒𝑠𝑢𝑙𝑡 = "SUCCESS" then
13             𝑃 𝑟𝑜𝑜𝑓 ← 𝑃 𝑟𝑜𝑜𝑓 ∪ {𝑇 𝑎𝑐𝑡𝑖𝑐} ;                                          // Add tactic to proof sequences
14             return 𝑃 𝑟𝑜𝑜𝑓 ;                                                                          // Proof found
15        end
16        else if 𝑅𝑒𝑠𝑢𝑙𝑡 = "MAX_NUM_TACTICS_REACHED" or 𝑅𝑒𝑠𝑢𝑙𝑡 = "MAX_TIME_REACHED" then
17             return "No proof found" ;                                                     // Fail if limits reached
18        end
19        else if 𝑅𝑒𝑠𝑢𝑙𝑡 = "ERROR" or 𝐺 ∈ 𝑆𝑒𝑒𝑛 then
20             continue ;                                                            // Skip if error or goal repeated
21        end
22        else if 𝑅𝑒𝑠𝑢𝑙𝑡 = "PROVING" then
23             𝑃 𝑟𝑜𝑜𝑓 ← 𝑃 𝑟𝑜𝑜𝑓 ∪ {𝑇 𝑎𝑐𝑡𝑖𝑐} ;                                                             // Add tactic
24             𝑆𝑒𝑒𝑛.add(𝐺) ;                                                                      // Mark goal as seen
25             𝑆𝑡𝑎𝑐𝑘.push(𝑃 𝐺𝑇 𝑆(𝐺, 𝑇 𝑎𝑐𝑡𝑖𝑐, 𝑃 , 𝑁𝑁)) ;                        // Push new tactics for next proof goal
26        end
27    end
28    return "No proof found" ;                                                                     // Proof not found
29 end
30 Function PGTS(𝐺, 𝑃 𝑎𝑟𝑒𝑛𝑡𝑇 𝑎𝑐𝑡𝑖𝑐, 𝑃 , 𝑁𝑁):
31    𝑇 ← 𝑁𝑁(𝐺) ;                                                        // Top-𝑘 tactics predicted by neural network
32    if 𝑃 𝑎𝑟𝑒𝑛𝑡𝑇 𝑎𝑐𝑡𝑖𝑐 is null then
33        return 𝑇 ;                                                      // Return NN predictions if no prior tactic
34    end
35    𝑇𝑝𝑎𝑡𝑡𝑒𝑟𝑛 ← {𝑡 ∈ 𝑇 ∣ (𝑃 𝑎𝑟𝑒𝑛𝑡𝑇 𝑎𝑐𝑡𝑖𝑐, 𝑡) ∈ 𝑃 } ;                                      // Pattern-matching tactics
36    𝑇𝑟𝑒𝑠𝑡 ← 𝑇 ⧵ 𝑇𝑝𝑎𝑡𝑡𝑒𝑟𝑛 ;                                                                      // Remaining tactics
37    return 𝑆𝑜𝑟𝑡𝐵𝑦𝑃 𝑎𝑡𝑡𝑒𝑟𝑛(𝑇𝑝𝑎𝑡𝑡𝑒𝑟𝑛 , 𝑃 ) ∪ 𝑆𝑜𝑟𝑡𝐵𝑦𝑁𝑁(𝑇𝑟𝑒𝑠𝑡 ) ;        // Sort pattern-matching tactics by frequency,
           others by NN probability
38   end


extra theorems A proves (total theorems by A minus total            higher-order logic. For RQ6, we assess the enhancement in
theorems by B) divided by the total theorems B proves. It           the quality of generated proofs by calculating the average
indicates the overall percentage improvement of A over B in         number of proof steps in the synthesized scripts. Since
proving theorems.                                                   variations in the number and complexity of theorems may
    Unique Added Value: This metric measures the specific           introduce bias into the average proof length, we introduce
advantage of tool A over tool B by determining the number           an additional metric: the average reduction in proof steps
of theorems only A proves (not proven by B) divided by the          compared to human-written proofs. This metric reflects the
total theorems B proves. It reflects the percentage of new          conciseness of the synthesized scripts and provides a more
theorems A adds relative to B’s performance.                        detailed perspective on proof quality.
    For RQ5, we evaluate the improvement in the ability of
proof synthesis tools to handle complex theorems by mea-
suring the proportion of newly proven theorems that involve

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                               Page 12 of 17
                                                                           Journal of Systems and Software

7.2. RQ4: Effectiveness                                                                     Table 1
     Figure 11 illustrates the number of theorems proved by                                 Unique Added Value of PGTS and RPGTS Compared to
all studied baselines using the original depth-first search                                 Original DFS Proof Search Across Theorem-Proving Tools
(DFS), our proposed Pattern-Guided Tactic Search (PGTS),
                                                                                                                      RPGTS               PGTS
and a variant, RPGTS. The results show that incorporating                                    Base Model DFS
                                                                                                                 Unique Added Value Unique Added Value
human-written proof patterns into the search process as a
heuristic significantly enhances the theorem-proving capa-                                   ASTactic     1595         50 (3.13%)        240 (15.05%)
bilities of automated proof synthesis tools. Notably, guiding                                Tac          1343         68 (5.06%)        327 (24.35%)
                                                                                             Tok          1407         94 (6.68%)        329 (23.38%)
all tactics with patterns, as in PGTS, outperforms guiding
                                                                                             Passport     1430         82 (5.73%)        246 (17.20%)
only parameterized tactics, as in RPGTS. Specifically, PGTS
improves the ASTactic tool by 5.64% (90 additional theo-                                     Average         -         74 (5.15%)        286 (20.00%)
rems), Tac by 12.14% (163 additional theorems), Tok by
9.24% (130 additional theorems), and Passport by 5.17%                                      Table 2
(74 additional theorems), achieving an average performance                                  Proportion of Higher-Order Logic in New Proven Theorems by
improvement of 8.05% across proof synthesis tools.                                          PGTS

                    1800                                                                       Base Model         DFS        new Theorems     Increase
                                                                                   DFS
                                                                                   RPGTS       ASTactic          19.44%         29.17%        50.05%
                                  1685                                             PGTS        Tac               18.76%         32.72%        74.41%
                                                                                               Tok               16.84%         38.91%        131.00%
                               1614                                                            Passport          20.42%         37.80%        85.11%
                    1600   1595
# Theorems Proven




                                                                                               Average             -                -          85.14%
                                                                    1537
                                                   1506                              1504
                                                                                 1467
                                                              1446
                                                          1407
                                                                             1430           theorems by effectively leveraging comprehensive pattern
                    1400                                                                    guidance, outperforming both DFS and the more limited
                                         13431358                                           RPGTS approach.

                                                                                              Answer to RQ4: PGTS improves the performance of
                                                                                              proof synthesis tools by increasing the number of suc-
                    1200
                             ASTactic        Tac              Tok              Passport       cessfully proven theorems by an average of 8.05%. On
                                                                                              average, it proves 20% more theorems that were previ-
Figure 11: Number of Theorems Proved by Baseline Tools                                        ously unprovable by the baseline tools.
Using DFS, PGTS, and RPGTS

                                                                                            7.3. RQ5: Capability
    Following the evaluation methodology of previous the-                                       Table 2 presents the proportion of higher-order logic in
orem proving tools, we also investigated whether incorpo-                                   the newly proven theorems by PGTS, indicating that PGTS
rating pattern-guided search enhances the ability of proof                                  proves a greater number of new theorems involving higher-
synthesis tools to prove new theorems. Table 1 presents the                                 order logic. The results show that across all four proof
unique added value of our proposed pattern-guided approach                                  synthesis tools, PGTS consistently proves a higher percent-
(PGTS) and a variant method (RPGTS) compared to the                                         age of new theorems involving higher-order logic compared
original DFS proof search. Consistent with the total added                                  to the original DFS search. Specifically, for ASTactic, the
value results, employing pattern-guided proof search signif-                                proportion of higher-order logic new theorems increases
icantly enhances the ability of theorem-proving synthesis                                   from 19.44% under DFS to 29.17% with PGTS, marking a
tools to prove new theorems. Guiding all tactics with pat-                                  50.05% relative increase. Tac exhibits an even more signif-
terns, as in PGTS, substantially outperforms guiding only                                   icant improvement, with the proportion rising from 18.76%
parameterized tactics, as in RPGTS. Specifically, PGTS                                      to 32.72%, reflecting a 74.41% increase. Similarly, Tok sees
proves 240 theorems that the original ASTactic fails to prove,                              a substantial increase from 16.84% under DFS to 38.91%
yielding a unique added value of 15.05%. For Tac, PGTS                                      with PGTS, achieving a remarkable 131.00% relative gain.
proves 327 additional new theorems, achieving a unique                                      Passport also demonstrates a strong improvement, with the
added value of 24.35%. For Tok, it proves 329 new theorems,                                 proportion increasing from 20.42% to 37.80%, representing
with a unique added value of 23.38%, and for Passport,                                      an 85.11% increase. On average, PGTS leads to an 85.14%
it proves 246 new theorems, resulting in a unique added                                     increase in the proportion of proven theorems that involve
value of 17.20%. Overall, PGTS proves an average of 286                                     higher-order logic across all tools. These findings indicate
theorems that prior tools fail to address, with an average                                  that PGTS is particularly effective in addressing complex
unique added value of 20.00%. These results underscore                                      theorems that require higher-order reasoning, significantly
PGTS’s superior ability to uncover previously unprovable                                    enhancing the capability of automated proof synthesis tools.

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                           Page 13 of 17
                                                   Journal of Systems and Software

                                                                     across four proof synthesis tools, with darker heatmap colors
   Answer for RQ5: PGTS significantly enhances the
                                                                     indicating a smaller proof length compared to manually
   ability of various proof synthesis tools to prove new
                                                                     written proofs. Our analysis reveals that the average step
   theorems involving higher-order logic, with an average
                                                                     length reduction for current proof synthesis tools is con-
   increase of 85.14%.
                                                                     sistently negative. This suggests that the proof sequences
                                                                     generated by these tools are generally longer than their
7.4. RQ6: Quality                                                    manually written counterparts. Furthermore, our proposed
     Figure 12 presents a heatmap illustrating the average           PGTS search method demonstrates a notable improvement
proof length generated by different proof search strate-             over the original DFS search method, achieving a greater
gies across four foundational proof synthesis tools. In the          reduction in proof sequence length. For instance, PGTS
heatmap, darker colors indicate shorter proof sequences,             reduces proof lengths by an average of 20.82% (0.97 tactics
signifying higher-quality proofs. The experimental results           steps) more than DFS across the four tools, highlighting its
demonstrate that our proposed PGTS tool significantly im-            superior performance in producing more concise proofs.
proves proof synthesis by reducing proof lengths in most
cases. Specifically, PGTS achieves an average proof length
reduction of 15.12% in Tac, 14.03% in Tok, and 18.95%
in Passport compared to the baseline DFS strategy. For                                                                             3.2
                                                                                   -3.10        -3.02           -3.06




                                                                        ASTactic
instance, in Passport, PGTS generates proofs with an average
length of 6.20 tactics, outperforming DFS (7.65 tactics) and
RPGTS (6.67 tactics), thereby demonstrating a notable im-                                                                          3.6
provement. However, on ASTactic, PGTS produces slightly                            -4.90        -4.41           -3.61

                                                                        Tac
longer proof sequences than the initial DFS search strategy
employed by the tool. Nonetheless, its variant, RPGTS,
                                                                     Tool
                                                                                                                                   4.0
still generates shorter proofs than DFS. This suggests that
pattern-guided proof search remains effective, as it leverages                     -4.06        -3.58           -3.01
                                                                        Tok



structural regularities in proof synthesis to guide the search                                                                     4.4
toward more efficient proof sequences.
                                                                                   -5.07        -4.11           -3.56              4.8
                                                                        Passport




                                                               7.6
              5.89          5.84            5.97                                   DFS          RPGTS           PGTS
   ASTactic




                                                                                               Method
                                                               7.2
                                                                     Figure 13: The Average Reduction in Proof Steps by Four
                                                                     Proof Synthesis Tools Using Different Proof Search Methods
              7.54          7.06            6.40
   Tac




                                                                     Compared to Human-Written Proofs
                                                               6.8
Tool




              6.70          6.29            5.76                        Answer for RQ6: PGTS significantly reduces proof
   Tok




                                                               6.4      lengths compared to DFS, achieving an average reduc-
                                                                        tion of 20.82% across proof synthesis tools.

              7.65          6.67            6.20               6.0
   Passport




                                                                     8. Discussion
              DFS          RPGTS            PGTS                        This section discusses several potential limitations of our
                           Method
                                                                     approach PGTS, as well as threats to its validity.
Figure 12: The Average Proof Sequence Length of Four Proof
Synthesis Tools Using Different Proof Search Methods                 8.1. Limitations
                                                                         While our proposed PGTS significantly improves the
                                                                     capability of existing proof synthesis tools in handling com-
    Since different proof synthesis tools address distinct           plex theorems and generating more concise proof scripts, we
theorems, the average proof length may be influenced by the          observed a notable increase in the number of tactic attempts
complexity of the theorems involved. To address this, we             during the proof search process. Figure 14 illustrates the
also evaluated the quality of proof sequences generated by           number of tactics attempted at each proof step when using
these tools by measuring the difference between the proof se-        the original DFS-based search compared to our pattern-
quence length produced by the tools and the length of manu-          guided approaches, RPGTS and PGTS. Interestingly, PGTS
ally written proof sequences. Figure 3 presents the reduction        tends to attempt slightly more tactics per step than DFS.
in proof step length achieved by different search methods

M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                       Page 14 of 17
                                                                   Journal of Systems and Software

                                                                                    extracted patterns are restricted to strictly contiguous se-
                                  20                                      Method
                                                                                    quences of tactics.
Avg. Tactics Attempted Per Step
                                                                            DFS
                                                                            RPGTS       External Validity. Threats to external validity arise
                                                                            PGTS
                                  15                                                from the generalizability of both our empirical study and
                                                                                    the experimental results of the PGTS approach. Although
                                                                                    we evaluated six state-of-the-art proof synthesis tools, all
                                  10
                                                                                    of them are specifically designed for the Coq interactive
                                                                                    theorem prover. This Coq-specific focus may limit the ap-
                                   5                                                plicability of our findings to other proof assistants. How-
                                                                                    ever, our empirical results demonstrate a consistent pat-
                                   0                                                tern of behavior across all six tools, suggesting that the
                                       ASTactic   Tac   Tok   Passport              observed phenomena may reflect broader characteristics of
                                                                                    current proof synthesis methods. Furthermore, the fact that
Figure 14: Average Number of Tactic Attempts per Proof Step                         our PGTS approach enhances the proof capabilities of all
under Different Search Strategies
                                                                                    evaluated tools provides additional evidence supporting its
                                                                                    generalizability beyond any single tool.

     To understand this phenomenon, we conducted a deeper
analysis. The primary cause lies in the pattern-matching                            9. Related Works
mechanism: tactics that align with human-like proof patterns                        9.1. Neural Theorem Proving
are prioritized during the search. However, our current de-                              Neural theorem proving integrates neural language mod-
sign considers only the category of a tactic, without vali-                         els with formal proof assistants, leveraging large-scale cor-
dating the correctness of its parameters before attempting                          pora of existing proofs to train the system to generate proof
it. As a result, many tactics that superficially match the                          tactics automatically. Yang et al. [12] employed a deep
desired pattern but have incorrect parameters are explored                          learning-based model to generate abstract syntax trees for
first, leading to an increase in tactic attempts.                                   tactic sequences, demonstrating the potential of neural net-
     Despite this limitation, guiding the proof search with                         works in generating tactics for interactive theorem provers.
human-like patterns still significantly improves the effec-                         First et al. [13] further integrated partially written proof
tiveness of proof synthesis. Prioritizing tactics that align                        scripts with proof state modeling, enhancing the success rate
with common proof strategies helps the search process re-                           of automatically generated tactics for interactive theorem
main more focused and increases the likelihood of finding                           proving. Sanchez-Stern et al. [14] enhanced the capabilities
successful proofs, even if some additional tactic attempts                          of existing proof synthesis tools by incorporating identifier
are required. However, it is important to note that directly                        encoding. Furthermore, First et al. [20] demonstrated that
filtering tactics based on parameter validity remains highly                        the proof success rate can be significantly improved by
challenging. Verifying whether a tactic’s parameters are                            combining multiple complementary machine learning-based
correct typically requires interaction with the underlying                          tactic generation models.
ITPs, as static analysis alone is insufficient to determine                              With the advancement of large model technology, some
parameter correctness in most cases. Such interactions intro-                       research [21, 16, 22] has explored the integration of large
duce considerable computational overhead and would funda-                           models with symbolic-based first-order theorem provers,
mentally change the lightweight nature of the current search                        such as Hammer [23, 24, 25], for proof generation. First
framework. Consequently, it is difficult to filter out invalid                      et al. [26] achieved promising results by fine-tuning large
tactics prior to their execution. PGTS, therefore, strikes a                        models for the generation and repair of proofs. Yang et
practical balance by guiding search using tactic categories                         al. [27] proposed a retrieval-augmented method for selecting
informed by human-like patterns without engaging in expen-                          premises from extensive mathematical libraries to facilitate
sive parameter validation. Future improvements may explore                          proof synthesis.
lightweight heuristic approximations or predictive models to
estimate parameter correctness without fully relying on ITPs                        9.2. Empirical Study on Code-related Tasks
interactions, though this remains an open challenge.                                    The advancement of deep learning technologies has led
                                                                                    to the emergence of numerous techniques tailored to code-
8.2. Threats to Validity                                                            related tasks. These include empirical evaluation of vulner-
     Internal Validity. Threat to internal validity lies in                         ability detection tools, code summarization, and other soft-
the potential bias during tactic pattern identification. PGTS                       ware engineering applications. Existing empirical studies
relies on tactic patterns derived from empirical data, and                          can be categorized into two types: one explores the impact
any inaccuracies in the extraction process may impact its                           of dataset quality on model performance, while the other
generalizability. To mitigate this risk, we applied a sequen-                       focuses on the capability boundaries of models for specific
tial pattern mining algorithm to extract tactic patterns from                       tasks. Liu et al. [28] found that removing noise from the
manually written proof scripts. To ensure consistency, the                          commit message dataset significantly degraded the model’s


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                  Page 15 of 17
                                                  Journal of Systems and Software

performance. Wu et al. [29] found that correcting mislabeled         References
security bug reports improved the performance of the clas-            [1] Francisco Henrique Ferreira, Elisa Yumi Nakagawa, and Ro-
sification model. Chakraborty et al. [30] demonstrated that               drigo Pereira dos Santos. Reliability in software-intensive systems:
state-of-the-art deep learning-based techniques experienced               challenges, solutions, and future perspectives. In 2021 47th Euromi-
a performance drop of more than 50% in real-world vulnera-                cro Conference on Software Engineering and Advanced Applications
bility prediction scenarios. Tian et al. [31] indicated that the          (SEAA), pages 54–61. IEEE, 2021.
                                                                      [2] Francisco Henrique Cerdeira Ferreira, Elisa Yumi Nakagawa, and
dataset for the commit message generation task has issues
                                                                          Rodrigo Pereira dos Santos. Towards an understanding of reliability
with message quality and defined what constitutes good                    of software-intensive systems-of-systems. Information and Software
commit quality. Unlike the aforementioned tasks, the proof                Technology, 158:107186, 2023.
script synthesis dataset is of high quality, as it is derived from    [3] Michael R Lyu. Software reliability engineering: A roadmap. In
real runtime proof information and evaluated on theorems                  Future of Software Engineering (FOSE’07), pages 153–170. IEEE,
                                                                          2007.
from real-world projects.
                                                                      [4] PK Kapur, Hoang Pham, Anshu Gupta, PC Jha, et al. Software
     Peng et al.[32] conducted a systematic study on the                  reliability assessment with OR applications, volume 364. Springer,
performance of methods for the API recommendation task.                   2011.
Dong et al.[33] examined the frequent patterns in commit              [5] Gerwin Klein, Kevin Elphinstone, Gernot Heiser, June Andronick,
messages generated by models. Steenhoek et al. [34] in-                   David Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,
                                                                          Rafal Kolanski, Michael Norrish, et al. sel4: Formal verification of
vestigated the types of program vulnerabilities that deep
                                                                          an os kernel. In Proceedings of the ACM SIGOPS 22nd symposium
learning models may find challenging to handle. Zhang et                  on Operating systems principles, pages 207–220, 2009.
al.[35] studied the types of commit messages generated                [6] Xavier Leroy. Formal verification of a realistic compiler. Communi-
and demonstrated that current methods can only generate                   cations of the ACM, 52(7):107–115, 2009.
commit message subjects rather than message bodies. Ni                [7] Mark Staples, Ross Jeffery, June Andronick, Toby Murray, Gerwin
                                                                          Klein, and Rafal Kolanski. Productivity for proof engineering.
et al.[36] investigated seven research questions on vulner-
                                                                          In Proceedings of the 8th ACM/IEEE International Symposium on
ability detection models across multiple dimensions, in-                  Empirical Software Engineering and Measurement, pages 1–4, 2014.
cluding model capability, interpretability, stability, usability,     [8] Qiao Zhang, Danyang Zhuo, and James Wilcox. A survey of formal
and cost-effectiveness. Similar to these works, this paper                verification approaches for practical systems.
explores proof synthesis tools’ capability boundaries. We             [9] Xavier Leroy, Sandrine Blazy, Daniel Kästner, Bernhard Schommer,
                                                                          Markus Pister, and Christian Ferdinand. Compcert-a formally verified
analyze the limitations of these tools from three perspec-
                                                                          optimizing compiler. In ERTS 2016: Embedded Real Time Software
tives: the theorem itself, proof scripts, and proof search. Fur-          and Systems, 8th European Congress, 2016.
thermore, based on our observations, we propose a pattern-           [10] Gilles Barthe, Sandrine Blazy, Benjamin Grégoire, Rémi Hutin, Vin-
guided tactic search method to optimize existing tools, sig-              cent Laporte, David Pichardie, and Alix Trieu. Formal verification of
nificantly improving proof performance.                                   a constant-time preserving c compiler. Proceedings of the ACM on
                                                                          Programming Languages, 4(POPL):1–30, 2019.
                                                                     [11] Manqing Zhang, Lingru Zhou, Bingxu Xiao, Yunwei Dong, and
                                                                          Yepang Liu. Replication package for “understanding and improving
10. Conclusion                                                            automated proof synthesis for interactive theorem provers”. https:
    In this paper, we explored the limitations of current proof           //github.com/zmqgeek/PGTS, 2025.
synthesis tools based on deep learning within ITPs environ-          [12] Kaiyu Yang and Jia Deng. Learning to prove theorems via interacting
                                                                          with proof assistants. In International Conference on Machine
ments. We observed that tactics aligned with human expert
                                                                          Learning, pages 6984–6994. PMLR, 2019.
proof patterns are more likely to be those that successfully         [13] Emily First, Yuriy Brun, and Arjun Guha. Tactok: Semantics-
advance the proof during the search process. This finding                 aware proof synthesis. Proceedings of the ACM on Programming
motivated the development of our PGTS approach, which                     Languages, 4(OOPSLA):1–31, 2020.
integrates pattern-awareness into the proof search process of        [14] Alex Sanchez-Stern, Emily First, Timothy Zhou, Zhanna Kaufman,
                                                                          Yuriy Brun, and Talia Ringer. Passport: Improving automated formal
existing proof synthesis tools. PGTS heuristically prioritizes
                                                                          verification using identifiers. ACM Transactions on Programming
tactics that match human expert proof patterns, resulting in              Languages and Systems, 45(2):1–30, 2023.
more efficient and focused proof search. Evaluation results          [15] Alex Sanchez-Stern, Yousef Alhessi, Lawrence Saul, and Sorin
demonstrate that PGTS significantly enhances existing proof               Lerner. Generating correctness proofs with neural networks. In
synthesis tools, increasing the average theorem-proving rate              Proceedings of the 4th ACM SIGPLAN International Workshop on
                                                                          Machine Learning and Programming Languages, pages 1–10, 2020.
by 8.05%. Moreover, PGTS proves to be especially effective
                                                                     [16] Minghai Lu, Benjamin Delaware, and Tianyi Zhang. Proof au-
in handling complex theorems and generating more concise                  tomation with large language models. In Proceedings of the 39th
proof sequences, suggesting its potential as a general im-                IEEE/ACM International Conference on Automated Software Engi-
provement framework for a wide range of ITPs.                             neering, pages 1509–1520, 2024.
                                                                     [17] Jiawei Han, Jian Pei, Behzad Mortazavi-Asl, Helen Pinto, Qiming
                                                                          Chen, Umeshwar Dayal, and Meichun Hsu. Prefixspan: Mining
Acknowledgment                                                            sequential patterns efficiently by prefix-projected pattern growth. In
                                                                          proceedings of the 17th international conference on data engineering,
   This work was supported by the Major Program of the                    pages 215–224. IEEE Piscataway, NJ, USA, 2001.
National Natural Science Foundation of China (Grant Nos.             [18] Jian Pei, Jiawei Han, Behzad Mortazavi-Asl, Jianyong Wang, Helen
62192733 and 62192730), the General Program of National                   Pinto, Qiming Chen, Umeshwar Dayal, and Mei-Chun Hsu. Mining
Natural Science Foundation of China No.62372219.                          sequential patterns by pattern-growth: The prefixspan approach. IEEE
                                                                          Transactions on knowledge and data engineering, 16(11):1424–1440,


M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                             Page 16 of 17
                                                          Journal of Systems and Software

     2004.                                                                          A critical review and directions for future work. IEEE Transactions
[19] Fabíola SF Pereira. Mining comparative sentences from social media             on Software Engineering, 50(4):816–835, 2024.
     text. In Workshop on interactions between data mining and natural         [36] Chao Ni, Liyu Shen, Xiaodan Xu, Xin Yin, and Shaohua Wang.
     language processing (DMNLP) co-located with European conference                Learning-based models for vulnerability detection: An extensive
     on machine learning and principles and practice of knowledge discov-           study. arXiv preprint arXiv:2408.07526, 2024.
     ery in databases (ECML/PKDD), pages 41–48, 2015.
[20] Emily First and Yuriy Brun. Diversity-driven automated formal
     verification. In Proceedings of the 44th International Conference on
     Software Engineering, pages 749–761, 2022.
[21] Saketh Ram Kasibatla, Arpan Agarwal, Yuriy Brun, Sorin Lerner,
     Talia Ringer, and Emily First. Cobblestone: Iterative automation for
     formal verification. arXiv preprint arXiv:2410.19940, 2024.
[22] Albert Qiaochu Jiang, Wenda Li, Szymon Tworkowski, Konrad
     Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu, and
     Mateja Jamnik. Thor: Wielding hammers to integrate language mod-
     els and automated theorem provers. Advances in Neural Information
     Processing Systems, 35:8360–8373, 2022.
[23] Lawrence C Paulsson and Jasmin C Blanchette. Three years of ex-
     perience with sledgehammer, a practical link between automatic and
     interactive theorem provers. In Proceedings of the 8th International
     Workshop on the Implementation of Logics (IWIL-2010), Yogyakarta,
     Indonesia. EPiC, volume 2, 2012.
[24] Cezary Kaliszyk and Josef Urban. Learning-assisted automated
     reasoning with flyspeck. Journal of Automated Reasoning, 53:173–
     213, 2014.
[25] Łukasz Czajka and Cezary Kaliszyk. Hammer for coq: Automation
     for dependent type theory. Journal of automated reasoning, 61:423–
     453, 2018.
[26] Emily First, Markus N Rabe, Talia Ringer, and Yuriy Brun. Baldur:
     Whole-proof generation and repair with large language models. In
     Proceedings of the 31st ACM Joint European Software Engineering
     Conference and Symposium on the Foundations of Software Engineer-
     ing, pages 1229–1241, 2023.
[27] Kaiyu Yang, Aidan Swope, Alex Gu, Rahul Chalamala, Peiyang Song,
     Shixing Yu, Saad Godil, Ryan J Prenger, and Animashree Anandku-
     mar. Leandojo: Theorem proving with retrieval-augmented language
     models. Advances in Neural Information Processing Systems, 36:
     21573–21612, 2023.
[28] Zhongxin Liu, Xin Xia, Ahmed E Hassan, David Lo, Zhenchang
     Xing, and Xinyu Wang. Neural-machine-translation-based commit
     message generation: how far are we? In Proceedings of the 33rd
     ACM/IEEE international conference on automated software engi-
     neering, pages 373–384, 2018.
[29] Xiaoxue Wu, Wei Zheng, Xin Xia, and David Lo. Data quality
     matters: A case study on data label correctness for security bug report
     prediction. IEEE Transactions on Software Engineering, 48(7):2541–
     2556, 2021.
[30] Saikat Chakraborty, Rahul Krishna, Yangruibo Ding, and Baishakhi
     Ray. Deep learning based vulnerability detection: Are we there yet?
     IEEE Transactions on Software Engineering, 48(9):3280–3296, 2021.
[31] Yingchen Tian, Yuxia Zhang, Klaas-Jan Stol, Lin Jiang, and Hui
     Liu. What makes a good commit message? In Proceedings of the
     44th International Conference on Software Engineering, pages 2389–
     2401, 2022.
[32] Yun Peng, Shuqing Li, Wenwei Gu, Yichen Li, Wenxuan Wang,
     Cuiyun Gao, and Michael R Lyu. Revisiting, benchmarking and
     exploring api recommendation: How far are we? IEEE Transactions
     on Software Engineering, 49(4):1876–1897, 2022.
[33] Jinhao Dong, Yiling Lou, Dan Hao, and Lin Tan. Revisiting learning-
     based commit message generation. In 2023 IEEE/ACM 45th Interna-
     tional Conference on Software Engineering (ICSE), pages 794–805.
     IEEE, 2023.
[34] Benjamin Steenhoek, Md Mahbubur Rahman, Richard Jiles, and Wei
     Le. An empirical study of deep learning models for vulnerability
     detection. In 2023 IEEE/ACM 45th International Conference on
     Software Engineering (ICSE), pages 2237–2248. IEEE, 2023.
[35] Yuxia Zhang, Zhiqing Qiu, Klaas-Jan Stol, Wenhui Zhu, Jiaxin Zhu,
     Yingchen Tian, and Hui Liu. Automatic commit message generation:



M. Zhang, L. Zhou, B. Xiao et al.: Preprint submitted to Elsevier                                                                     Page 17 of 17
