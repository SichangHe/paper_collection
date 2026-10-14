                                             Towards LLM-based Generation of Human-Readable Proofs in
                                                          Polynomial Formal Verification
                                                                                        (Invited Paper)


                                                                               Rolf Drechsler[0000−0002−9872−1740]

                                                                         University of Bremen/DFKI, Bremen, Germany
                                                                                   drechsler@uni-bremen.de
                                                                                 http://www.rolfdrechsler.de
arXiv:2505.23311v1 [cs.LO] 29 May 2025




                                               Abstract. Verification is one of the central tasks in circuit and system design. While simulation and
                                               emulation are widely used, complete correctness can only be ensured based on formal proof techniques.
                                               But these approaches often have very high run time and memory requirements. Recently, Polynomial
                                               Formal Verification (PFV) has been introduced showing that for many instances of practical relevance
                                               upper bounds on needed resources can be given. But proofs have to be provided that are human-
                                               readable.
                                               Here, we study how modern approaches from Artificial Intelligence (AI) based on Large Language
                                               Models (LLMs) can be used to generate proofs that later on can be validated based on reasoning
                                               engines. Examples are given that show how LLMs can interact with proof engines, and directions for
                                               future work are outlined.

                                               Keywords: Polynomial Formal Verification · LLM · Proof Generation.


                                         1   Introduction
                                         With the ever-increasing complexity of modern circuits and systems, ensuring the functional correctness is
                                         a highly relevant task. Classical approaches based on simulation and emulation are not sufficient due to
                                         their limited resulting coverage in the verification task. Only formal proof techniques can guarantee that
                                         the systems operate 100% correct. But the underlying methods, like BDDs, SAT or SMT, are known to be
                                         computationally very expensive (see e.g. [1,2]).
                                             A possible solution to this dilemma is Polynomial Formal Verification (PFV) [3,4]: For specific classes
                                         of circuits, like adders and multipliers, implementations are identified together with a corresponding proof
                                         engine such that efficient upper bounds on run time and memory requirement can be ensured. This requires
                                         first a theoretical analysis and a formal proof followed by an efficient implementation. By this, fast adder
                                         designs with more than one thousand bits could be completely verified based on BDDs in a few CPU seconds.
                                             While PFV itself is very powerful, so far, its lacks automation of the proof process. Recently in [5,6]
                                         approaches have been proposed for the automatic generation of human-readable proofs. These are based on
                                         a search on the underlying graphs of BDDs.
                                             In this paper, we propose to enhance the proof generation process by techniques from Artificial Intelligence
                                         (AI), namely Large Language Models (LLMs). These have been studied in various applications in circuit
                                         design and have also recently been investigated in the context of verification [8]. We show some examples
                                         for generation of human-readable proofs. Due to the power of today’s LLMs – in the following ChatGPT 4o
                                         is used – easily understandable text can be created. But due to the hallucinations in the AI tool, finally the
                                         correctness has to be proven. We show some examples to discuss the consequences for future work.


                                         2   Examples
                                         One of the simplest but also in this context often used proof technique is induction. This is also the technique
                                         applied in [5,6] for BDDs.
                                            In the following, it is briefly described how LLMs can be used, while the detailed questions and answers
                                         are reported in Section 4 Appendix. The corresponding question/prompt is given by Qx: followed by the
                                         answer A:.
2      R. Drechsler

Induction proof: Not surprisingly, the basic of mathematical induction can be easily summarized (see Q1),
   where the induction step is given from n to n + 1.
f2 = x1 x2 + x3 x4 + · · · + x2n−1 x2n : In a next step, induction is applied to function f2 . Here, it is im-
   portant to do the induction step not only for a single but for two variables. This is also suggested by
   the tool (see Q2). This can be expected, since this function is very well known and well-studied in the
   BDD community. Already in the original paper by Bryant, where BDDs have been introduced in its often
   used ordered and reduced form, this function has been discussed [9]. This is due to the fact that it has
   the interesting property that the BDD size varies from linear to exponential dependent on the chosen
   variable ordering.
f3 = x1 x2 x3 + x4 x5 x6 + · · · + xn−2 xn−1 xn : A slight extension is to move from two to three variables
   per monomial. This function is quite similar to f2 but now requires to group three variables in the base
   case and the induction step. Also here, LLMs work well (see Q3).
Totally symmetric functions: For totally symmetric functions (see Q4) it is known that BDDs only
   require a quadratic number of nodes, i.e. O(n2 ) [9]. The BDDs only grow by one node per level in the
   worst case, i.e. one node in the first level, two in the second, etc. For many symmetric functions, like
   AND and OR, the final number is much smaller. In this case, the LLM correctly gives the core idea.
Of course, in all cases a formal proof that should be tool assisted is required. But this can easily be linked
to the graph-based techniques from [5,6].
    To show that some of the discussions require a deeper understanding, we finally consider the multiplier
function, where it can be formally proven that the BDD size is exponential independent of the chosen variable
ordering [7]. Since the Q&A is longer in this case, only the core parts are reported:
    Q: Can you also proof by induction that BDDs for the multiplication functions are polynomially
    bounded?
This generates the answer:
    A: This is a great and subtle question. The short answer is:
    No — we cannot, in general, prove by induction that BDDs for binary multiplication functions are
    polynomially bounded in size. In fact, in the worst case, Binary Decision Diagrams (BDDs) for
    multiplication functions can have exponential size.
    Let’s examine this carefully.
    ...
    Summary
    Multiplication functions (e.g., A × B) are not guaranteed to have polynomial-size BDDs.
    There is no general inductive proof that BDDs for multiplication are polynomially bounded.
    In fact, under most variable orderings, BDDs for multiplication require exponential space.
Most variables is not correct, since it can be proven that it holds for all. A next question/prompt is send to
clarify this.
    Q: But many cases does not mean all, right? can you give me a case where you can avoid the
    exponential blow-up.
As a result, you get:
    A: ... Case: Careful variable ordering
    For full multiplication A × B (both n bits), variable ordering matters greatly.
    A poor ordering like:
    a0 , b0 , a1 , b1 , a2 , b2 , . . .
    leads to exponential size.
    But a better ordering is:
    a0 , a1 , . . . , an−1 , b0 , b1 , . . . , bn−1
    or the reverse:
    b0 , b1 , . . . , bn−1 , a0 , a1 , . . . , an−1
    This allows the BDD package to exploit sharing and avoid recomputation of intermediate partial
    products.
    Empirically (see Bryant 1986 and follow-ups), this ordering can significantly reduce BDD size —
    sometimes making it polynomial in practice for moderate n.
                                         Towards LLM-based Generation of Human-Readable Proofs in PFV                 3

From a complexity analysis point of view the last sentence is not correct, while the core message is clear: for
a small number of variables the program might terminate within the given resources.


3    Conclusions and Future Work
LLMs are a very powerful tool in the context of text generation. This also holds for generation of human-
readable proofs. But the correctness has to be checked by some formal tools. This has already been observed
in various applications leading to approaches for explanation models (see e.g. [10,11,12,13]).
    While the suggestions for proofs — at least for induction — are promising, a formal approach has to be
applied. This can either be based on identifying patterns as suggested in [5,6] or on some explanation that
is based on logical reasoning. Further interesting aspects to study are:
 1. While the current induction proofs are for well-studied problems, however the same principles are also
    applicable to modern data structures (see e.g. [14]). Hence, LLMs can potentially benefit there as well.
 2. The LLMs have used the prior works as reference while reasoning about the proofs in some cases. However,
    with the availability of Retrieval Augmented Generation (RAG), ongoing tailored proofs can be fed to
    the LLMs to build complex proofs that are human-readable.
 3. Currently, even with simple prompts the reasoning capabilities of LLMs have shown potential. Using
    techniques like chain of thought reasoning and feedback from the formal tool can further aid the LLMs
    in proof generation.
For PFV a linking of formal tools with the LLM is a promising direction for future work.

Acknowledgments. This work was supported by the German Research Foundation (DFG) within the Reinhart
Koselleck Project PolyVer (DR 287/36-1 - project number 431649366) and the Research Training Group GRK 2972
CAUSE (project number 513623283).


References
 1. Drechsler, R.: Advanced Formal Verification. Kluwer Academic Publishers, 2004.
 2. Drechsler, R.: Formal System Verification: State-of the-Art and Future Trends. Springer, 2017
 3. Drechsler, R.: PolyAdd: Polynomial Formal Verification of Adder Circuits. 24th IEEE International Symposium
    on Design and Diagnostics of Electronic Circuits and Systems (2021)
 4. Drechsler, R., Mahzoon, A.: Polynomial Formal Verification: Ensuring Correctness under Resource Constraints.
    International Conference on Computer Aided Design (2022)
 5. Drechsler, R., Schnieber, M.: Next-Generation Automatic Human-Readable Proofs Enabling Polynomial Formal
    Verification. International Conference on Formal Methods and Models for System Design (2023)
 6. Schnieber, M., Drechsler, R.: Automated polynomial formal verification using generalized binary decision diagram
    patterns. Philosophical Transactions of the Royal Society A (2025)
 7. Bryant, R,: On the complexity of VLSI implementations and graph representations of Boolean functions with
    application to integer multiplication, IEEE Transactions on Computers, vol. 40, no. 2, pp. 205-213 (1991)
 8. Qayyum, K., Ahmadi-Pour, S., Jha, C., Hassan, M., Drechsler, R.: LLMs for Hardware Verification: Frameworks,
    Techniques, and Future Directions. IEEE Asian Test Symposium (2024)
 9. Bryant, R.: Graph-Based Algorithms for Boolean Function Manipulation, IEEE Transactions on Computers, vol.
    C-35, no. 8, pp. 677-691 (1986)
10. Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., Zhou, D.: Chain-of-thought
    prompting elicits reasoning in large language models. 36th International Conference on Neural Information Pro-
    cessing Systems (2022)
11. Fey, G., Fränzle, M., Drechsler, R.: Self-Explanation in Systems of Systems. IEEE 30th International Require-
    ments Engineering Conference Workshops (2022)
12. Yao, S., Yu, D., Zhao, J., Shafran, I., Griffiths, T., Cao, Y., Narasimhan, K.: Tree of thoughts: deliberate problem
    solving with large language models. 37th International Conference on Neural Information Processing Systems
    (2023)
13. Liu, T., Xu, W., Huang, W., Zeng, Y., Wang, J., Wang, X., Yang, H., Li, J.: Logic-of-Thought: Injecting Logic
    into Contexts for Full Reasoning in Large Language Models. Conference of the Nations of the Americas Chapter
    of the Association for Computational Linguistics: Human Language Technologies (2025)
14. Drechsler, R., Plump, C., Schnieber, M.: The Future is Hybrid: Next Generation Data Structures for Formal
    Verification, Asian Test Symposium (2024)
     4         R. Drechsler

     4      Appendix
     Q1: How can I perform an induction proof for binary decision diagrams?
     A: To perform an induction proof involving Binary Decision Diagrams (BDDs), you typically use mathe-
     matical induction on a structural property (e.g., number of variables or size of the BDD). Here’s a generic
     outline:
Step 1: Base Case: Prove the property holds for a trivial BDD, such as one with 0 or 1 variable.
Step 2: Inductive Hypothesis: Assume the property holds for all BDDs with up to n variables.
Step 3: Inductive Step: Prove it holds for n + 1 variables. Use the fact that BDDs for n + 1 variables can be
        split at the root into two BDDs with at most n variables each (Then/Else branches). Apply the inductive
        hypothesis.
           You might use this to prove correctness, size bounds, or structural properties of BDDs.

     Q2: How does this work for the function f = x1 x2 + x3 x4 + · · · + x2n−1 x2n ?
                         Pn
     A: Consider fn = i=1 x2i−1 x2i . Each term is a 2-variable AND. With a fixed variable ordering x1 < x2 <
     · · · < x2n , the BDD can be constructed incrementally.

     Inductive Structure:
         – Base Case (n = 1): f1 = x1 x2 , BDD has 3 internal nodes.
         – Inductive Hypothesis: BDD for fk has size ≤ 3k + 1.
         – Inductive Step: Add x2k+1 x2k+2 . New BDD adds 3 nodes. Total becomes 3(k + 1) + 1.
           Thus, the size is linear in n.

     Q3: How does it work for f = x1 x2 x3 + x4 x5 x6 + · · · + xn−2 xn−1 xn ?
                                   Pk
     A: Let n = 3k, and define fk = i=1 x3i−2 x3i−1 x3i .

     Inductive Strategy:
         – Base Case: f1 = x1 x2 x3 , BDD has 3 internal nodes.
         – Inductive Step: Add new term x3k+1 x3k+2 x3k+3 , which adds 4 nodes (including the OR node).

     Conclusion:
     The BDD size grows linearly in k. So for n = 3k, the BDD size is O(n).

     Q4: Can you also prove by induction that BDDs for totally symmetric functions are
     polynomially bounded?
     A: Yes. Let fn be a totally symmetric Boolean function: it depends only on the Hamming weight of its input.
     We’ll show the size of its BDD is O(n2 ).

     Inductive Argument:
         – Base Case (n = 1): BDD size is constant.
         – Inductive Hypothesis: Assume fn has a BDD with size ≤ Cn2 .
         – Inductive Step: Construct BDD for fn+1 . At each level i, track how many ones have been seen (0 ≤ k ≤ i).
           Each level has i + 1 nodes.

     Node Count:
                                             n
                                            X             (n + 1)(n + 2)
                                                (i + 1) =                = O(n2 )
                                            i=0
                                                                2
