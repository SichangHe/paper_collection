                                                                  When Regression Verification Meets CEGAR
                                                                Fei He                                    Qianshan Yu                                            Liming Cai
                                                  School of Software, Tsinghua                   School of Software, Tsinghua                        School of Software, Tsinghua
                                                           University                                     University                                          University
                                                     Haidian, Beijing, China                        Haidian, Beijing, China                             Haidian, Beijing, China
                                                     hefei@tsinghua.edu.cn                        yuqianshan@foxmail.com                               limingcai0101@yeah.net

                                         ABSTRACT                                                                     Model checking [16] is one of the most successful techniques in
                                         Software systems evolve throughout their life cycles. Many revi-          formal verification. However, it is still very time-consuming. Verify-
                                         sions are produced over time. Model checking each revision of the         ing every revision of the software is impractical. Inspired by the re-
                                         software is impractical. Regression verification suggests reusing         gression testing [20, 31], researchers in formal verification commu-
arXiv:1806.04829v1 [cs.SE] 13 Jun 2018




                                         intermediate results from the previous verification runs.                 nity propose the technique of regression verification [2, 10, 11, 19].
                                            This paper proposes a fully automatic regression verification          Taking into consideration that many intermediate results are pro-
                                         technique in the context of CEGAR. Procedure summaries, which             duced during the verification, and computing these results is costly,
                                         describe the input/output behaviors of a procedure, are proposed          regression verification aims to make use of these intermediate re-
                                         as the intermediate results to be reused. Procedure summaries are         sults in the verification of new program revisions.
                                         reasonably small to store, technically easy to process, and do not           Different intermediate results have been proposed for reuse, in-
                                         require much extra computation effort to be reused. Reusing proce-        cluding abstract precisions, state-space graph, constraint solver
                                         dure summaries saves much analysis effort on the corresponding            solutions, and interpolation-based procedure summaries. Beyer
                                         procedures. By combining regression verification and CEGAR, we            et al. [10] proposed to record the final abstract precision in the
                                         propose a technique that is able to reuse procedure summaries             previous verification run, and reuse it in the current verification.
                                         across different abstract precisions and different program revisions.     Henzinger et al. [23] proposed to reuse state-space graph for in-
                                            We performed extensive experiments on a large number of in-            cremental checking of temporal safety properties. Visser et al. [35]
                                         dustrial programs (534 revisions of 89 Linux kernel device drivers).      noticed the important role of constraint solving in software verifi-
                                         The results show that our approach can significantly improve the          cation, and proposed to reuse the constraints solving results. Sery
                                         performance of regression verification.                                   et al. [32] proposed to reuse the interpolation-based procedure
                                                                                                                   summaries in incremental upgrade checking.
                                         CCS CONCEPTS                                                                 This paper proposes to use state-based procedure summaries
                                                                                                                   as the intermediate verification results. A state-based procedure
                                         • Software and its engineering → Formal software verifica-                summary is a pair of input and output states, describing the ob-
                                         tion;                                                                     servable behaviors of the procedure. Remark that the state-based
                                                                                                                   procedure summaries is a different type of intermediate results to
                                         KEYWORDS                                                                  the interpolation-based summaries 1 . In the following, unless oth-
                                         Regression verification, software verification, procedure summary,        erwise specified, by procedure summary we mean the state-based
                                         counterexample-guided abstraction refinement                              summary.
                                                                                                                      The state-based procedure summaries can be automatically gen-
                                         ACM Reference Format:                                                     erated by most of the interprocedural analysis techniques [30, 33].
                                         Fei He, Qianshan Yu, and Liming Cai. 2018. When Regression Verification
                                                                                                                   Generating these procedure summaries does not need much ad-
                                         Meets CEGAR. In Proceedings of ACM Conference, Washington, DC, USA,
                                                                                                                   ditional computation effort. Recall that a state-based procedure
                                         July 2017 (Conference’17), 11 pages.
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn                                   summary is a pair of input and output states. They are efficient
                                                                                                                   to store, easy to process, and do not require much extra computa-
                                                                                                                   tion effort before they can be reused. More importantly, reusing
                                                                                                                   state-based procedure summaries avoids re-analysis of the same
                                         1    INTRODUCTION                                                         procedures, and thus significantly reduces the verification effort
                                         Along with the widespread use of software in our daily life, there is     for the next revision. State-based procedure summaries, therefore,
                                         a growing concern for software reliability. At the same time, mar-        are a good choice for reusing in regression verification.
                                         ket pressure demands quick product introductions. The software               We consider regression verification in the context of counter-
                                         companies are required to introduce new features to their software        example guided abstraction refinement (CEGAR) [15]. Techniques
                                         products in shorter release cycles. Since errors may be introduced        for representing, processing and reusing state-based procedure
                                         with new features, each revision of these software products needs         summaries need be adapted to the CEGAR framework (see Sec-
                                         be formally verified.                                                     tion 4 and 5). A lazy counterexample analysis technqiue is further
                                                                                                                   proposed to address the effectiveness issure of summary reuse (see
                                                                                                                   Section 6). To the best of our knowledge, we are the first to consider
                                         Conference’17, July 2017, Washington, DC, USA
                                         2018. ACM ISBN 978-x-xxxx-xxxx-x/YY/MM. . . $15.00
                                         https://doi.org/10.1145/nnnnnnn.nnnnnnn                                   1 Their differences will be discussed in Section 8.
Conference’17, July 2017, Washington, DC, USA                                                            Fei He, Qianshan Yu, and Liming Cai


the reuse of state-based procedure summaries in the context of                 Counterexample-guided abstraction refinement [15] provides a
CEGAR. Considering that CEGAR is a widely-adopted technique in             framework for automatically finding proper precisions. Starting
software verification [4, 6, 9, 13, 22], our approach can be applied       from an initial abstract precision, it iteratively checks if the cor-
to most state-of-the-art software verifiers.                               responding abstract model satisfies the desired property. If the
    We implemented our approach on top of CPAchecker[9], and               property is satisfied, it must also hold on the concrete model, the
performed extensive experiments on a large set of industrial pro-          algorithm terminates and reports “safe”. Otherwise, the checker
grams. Up to 534 revisions of 89 Linux kernel device drivers are           returns a path on the abstract model that falsifies the desired prop-
used in experiments. Experimental results show very promising              erty. The algorithm then checks if the returned path is valid on the
performance of our approach. In comparison to the standalone ver-          concrete model or not. If it is, the algorithm finds a real bug, it thus
ification, our summary reuse technique saves 31.4% of verification         terminates and reports “unsafe”. Otherwise, the precision is too
time. We also test the impact of summary reduction and lazy coun-          coarse, and needs be refined with the counterexample. Then the
terexample analysis to regression verification. Results show that          above process repeats, until either “safe” or “unsafe” is reported.
these two techniques can significantly improve the performance of              The abstract precision is not necessary to be the same throughout
regression verification.                                                   the program [24]. To simplify the discussion, we assume in this
    The main technical contributions of this paper are summarized          paper that the abstract precisions are defined at the procedure level,
as follows:                                                                i.e., each procedure is associated with an unique abstract precision.
     • We identify the value of state-based summaries as interme-          Note that this is not a limitation of our approach, which can be
        diate results to be reused in regression verification.             applied to other settings of abstract precisions.
     • We propose a fully automatic regression verification tech-
        nique in the context of counterexample-guided abstraction
        refinement, with which procedure summaries can be effi-            2.2    Software Verification
        ciently reused across different abstract precisions and differ-    Model checking and program analysis are two major approaches
        ent program revisions.                                             for software verification. Comparing these two techniques, model
     • The counterexample analysis is nontrivial in the context            checking is more precise with fewer false positives produced, while
        of regression verification and CEGAR. We propose a lazy            program analysis is comparatively more efficient and can be applied
        analysis technique to improve the effectiveness of summary         to more programs. An increasing tendency to software verification
        reuse.                                                             is to integrate these two techniques together [8], to get a good
     • We implemented our approach in the software verification            balance between accuracy and efficiency.
        tool CPAchecker. Experimental results show promising per-              Control flow automata (CFA) are adopted in many software ver-
        formance of our approach.                                          ification techniques (for example, BLAST and CPAchecker) for
    The remainder of this paper is organized as follows. Section 2 in-     representing programs. Let X , L and Op be the sets of variables,
troduces necessary backgrounds. Section 3 illustrates our approach         locations and operations in a program P, respectively. The CFA of
by a toy example. Section 4 presents techniques for representing           P consists of the set L of locations and the set G ⊆ L × Op × L
and processing summaries in the context of CEGAR. Section 5                of control flow edges. A state of P is a pair (l, u), where l ∈ L is a
presents our regression verification framework. Section 6 exhibits         program location and u is a valuation to X .
the lazy counterexample analysis technique. Section 7 reports eval-            Predicate abstraction is a popular abstraction technique for soft-
uation results on our approach. Section 8 discusses related work           ware verification. The abstract precision λ is a set of predicates. All
and Section 9 concludes this paper.                                        predicates are defined over the program variables. This analysis
                                                                           tracks values of predicates in λ on each abstract state. Formally,
2 BACKGROUND                                                               an abstract state for predicate analysis is a pair (l, s) where l is a
2.1 Abstraction and Refinement                                             program location and s an abstract valuation that assigns Boolean
                                                                           values to all predicates in λ. In the remainder of the paper, we also
Abstraction plays a central role in software verification. Abstrac-        call s an abstract data state. There exists other abstract domains,
tion omits details of the system behaviors, resulting in a simpler         like interval abstraction, octagon abstraction, etc. Our technique
model. We call the model before and after abstraction the concrete         can easily be extended to these abstract domains.
and abstract model, respectively. An abstraction is conservative [16]          Interprocedural analysis deals with programs with multiple pro-
if it does not omit any behavior of the concrete model. Conserva-          cedures. A simple way for interprocedural analysis is to inline a
tive abstraction guarantees that the properties (more precisely, the       copy of the callee procedure at each of its callsites. The inlining
ACT L∗ properties [16]) established on the abstract system also hold       technique is, however, very expensive and may lead to context ex-
on the concrete system. The reverse, however, is not guaranteed: if        plosion for recursive procedures. Another interprocedural analysis
the abstract model falsifies the property, the concrete model does         technqiue is by use of procedure summaries [30, 33]. A procedure
not necessarily falsify this property, too.                                summary (or shortly, a summary) describes the input/output be-
    The abstract precision [10] (for short, precision) defines the level   haviors of a procedure. This technique plugs summaries in at each
of abstraction of an abstract model. The precision must be at a            callsite of the procedure. With this technique, we avoid reanalyzing
proper level. A too-coarse precision may fail to verify the property,      the procedure body at each of its call sites, the efficiency is thus
a too-fine precision, however, may lead to state space explosion.          improved.
Finding a proper precision appears to require ingenuity.
When Regression Verification Meets CEGAR                                                         Conference’17, July 2017, Washington, DC, USA

                main(){                                                                          main() {
                    …                                                                                …
                1: if (flag) {                                                                   1: if (flag)
                2:      y = inc(x, flag);                                                        2:      y = inc(x, flag);
                3:      if (y <= x) ERROR;                                                           else
                    } else {                                                                     3:      x = inc(y, flag);
                4:      z = inc(x, flag);                                                        4: if (x > y) ERROR;
                5:      if (z >= x) ERROR;                                                           …
                    }                                                                            }
                    …
                }                                                                         Figure 2: The updated main procedure

                inc(int a, int sign){
                    int rv;                                                   Summary reuse across different invocations has already been
                6: if (sign)                                               supported by existing interprocedural analysis techniques [30, 33].
                7:     rv = a + 1;                                         A summary cache is maintained to keep all procedure summaries
                    else                                                   generated so far. In case of a procedure invocation, the verifier
                8:     rv = a – 1;                                         attempts to seek in the cache for a summary that meets the current
                9: return rv;                                              input state. Only when no applicable summary exists in the cache,
                }                                                          do we need to analyze the procedure.

                 Figure 1: An example program                              3.2     Reuse Across Programs
                                                                           Consider now the original program evolves to a new version, where
3     A MOTIVATING EXAMPLE                                                 the main procedure changes, while the inc procedure does not. The
                                                                           updated main procedure is shown in Fig. 2. Apparently, this new
Figure 1 shows a simple program we designed to illustrate the basic
                                                                           program must be re-verified to guarantee its correctness. Tradi-
process of summary reuse in the context of CEGAR. This program
                                                                           tional interprocedural techniques [30, 33] verify this new program
consists of two procedures: main and inc. The inc procedure takes
                                                                           from scratch, which apparently is not an efficient way.
two input parameters: a and siдn, and outputs either a +1 (if siдn! =
                                                                              Note that there are many commonalities between two consecu-
0), or a − 1 (if siдn = 0). The inc procedure is invoked twice in the
                                                                           tive revisions. The summaries generated for the older revision have
main procedure. We want to verify that the “ERROR” statements
                                                                           many possibilities to be reused in the regression verification. These
(at line 3 and 5) are not reachable in any execution of this program.
                                                                           summaries contain important information about the verification.
    Assume the current abstract precision for the inc procedure
                                                                           Reusing them can significantly reduce the consequent verification
contains two predicates, i.e., sign = 0 and rv > a. Only values of
                                                                           effort.
these two predicates need be tracked in the predicate analysis of
                                                                              Considering the example, since the inc procedure remains the
the inc procedure. At the first call (at line 2) to the inc procedure,
                                                                           same in the new revision, the previously generated summaries (1)
f laд , 0, and thus the predicate sign = 0 is false. The invoked inc
                                                                           and (2) can be applied to the verification of the new revision. At line
procedure therefore takes the true branch (line 7), and at the return
                                                                           2 of the new main procedure, without entering the inc procedure,
point the predicate rv > a holds. One summary is concluded after
                                                                           we can directly get that y > x by applying (1) 2 . Similarly, at line 3,
this procedure call, written
                                                                           we get that ¬(x > y) by applying (2). In either case, the condition
                ⟨¬(sign = 0), ¬(sign = 0) ∧ rv > a⟩,                (1)    y < x does not hold, we thus conclude the new program is safe.
meaning that if the input state of the inc procedure satisfies the         Remark that in the above regression verification, we need not to
left formula (called the input condition), the output state of the         look into the body of the inc procedure.
inc procedure must satisfy the right formula (called the output               There are some issues that must be addressed for reusing sum-
condition). Similarly, at the second call (line 4) to the inc procedure,   maries across different program versions:
the invoked inc procedure takes another branch and concludes                    • Abstraction issue: Note that the regression verification in-
                                                                                   volves a new round of CEGAR. Abstract precision changes
                  ⟨sign = 0, sign = 0 ∧ ¬(rv > a)⟩.                 (2)
                                                                                   among different iterations of CEGAR. Summaries generated
Above two formulas summarize the input/output behaviors of the                     in the previous verification run may not be applicable to the
inc procedure at the given abstract level.                                         current verification. Reconsidering the above example, if the
   For more information on the summary generation of interproce-                   current abstract precision does not contain the predicates
dural analysis, please refer to [21, 37].                                          rv > a and rv < a, the summaries (1) and (2) can not be
                                                                                   applied.
3.1    Reuse Across Invocations                                                 • Counterexample issue: In the framework of CEGAR, each
If there is another call to the inc procedure in the remainder of the              time the verifier returns a counterexample, one needs to
program, without entering the procedure’s body, we can immedi-                     check if this counterexample corresponds to a real path or
ately determine its output state by testing ¬(sign = 0) on its input       2 Assume the predicates y > x and x > y are included in the abstract precision of the
state.                                                                     new main procedure.
Conference’17, July 2017, Washington, DC, USA                                                              Fei He, Qianshan Yu, and Liming Cai


       not. To validate a counterexample, the involved procedure            In the worst case, the number of satisfiability checkings are up to
       calls need be expanded to the inner paths in the correspond-         the total number of summaries in the cache.
       ing procedures. This task is nontrivial and may lead the
       summary reuse much less useful for regression verification           4.2    Summary Representation
       (see Section 6). A smarter counterexample analysis technique
                                                                            Note that a large number of satisfiability checking is required to
       is in demand.
                                                                            find an applicable summary. To improve the efficiency of summary
                                                                            retrieval, we use ordered binary decision diagrams (OBDDs) to
4    ABSTRACT SUMMARIES                                                     represent procedure summaries.
To adapt to CEGAR, the summary definition needs to be extended                 OBDD is a compact and canonical representation of Boolean
with the abstract precision. In this section, we first introduce the        functions. If two Boolean functions are equivalent, their OBDDs
definition of abstract procedure summaries, then discuss their rep-         must be isomorphic. The canonicality of OBDD leads to a very
resentations, and finally propose an optimization technique for             efficient algorithm for checking equivalence of two Boolean func-
summary reduction.                                                          tions [12]. Moreover, many modern OBDD packages (for example,
                                                                            the CUDD package [34]) realizes the shared OBDD technique, with
4.1 Definitions                                                             which the equivalence checking of two Boolean functions can be
Let p be a predicate, a predicate literal of p is either p or ¬p. Recall    finished in constant time [34].
that an abstract precision λ is a set of predicates. An abstract data          For each procedure summary, two OBDDs that represents ϕ in
state is a valuation to all predicates in λ. An abstract data state can     and ϕout , respectively, are stored. Construction of these two OBDDs
be represented as a complete conjunction of predicate literals, such        may take some time. However, it is worthwhile, since these OBDDs
that each predicate in λ occurs in the conjunction in either positive       may later be tested many times during the verification. With the
or negtive form. In contrast, a partial conjunction of predicate            OBDD representation, each test requires only a constant time.
literals represents a set of abstract data states.
    Considering the motivating example, assume the current abstract         4.3    Summary Reduction
precision consists of two predicates, i.e., sign = 0 and rv > a.
                                                                            A procedure summary may contain redundant information. This
Positive and negative forms of these two predicates are all predicate
                                                                            redundant information is useless, and may decrease the hit rate of
literals. The formula “sign = 0 ∧ ¬(rv > a)” is a full conjunction
                                                                            the summary cache. In the following, we discuss how to remove
of predicate literals in the precision, representing an abstract data
                                                                            redundant information from summaries.
state. The formula “sign = 0” is a partial conjunction of predicate
                                                                               A number of variables are accessed in the body of a procedure,
literals, representing a set of abstract data states (the predicate
                                                                            including formal parameters, local variables and global variables.
rv > a can be either true or false).
                                                                            Let Vf be the set of all variables accessed by the procedure f . A
  Definition 4.1. A summary of a procedure f with respect to an             predicate is relevant to f if it contains at least one variable in Vf . A
abstract precision λ is a pair ⟨ϕ in , ϕout ⟩, where ϕ in and ϕout are      predicate is irrelevant to f , if all variables occurred in the predicate
conjunctions of predicate literals in λ, representing the input and         are irrelevant to the procedure. For example, a and siдn are formal
output conditions of f , respectively.                                      parameters, and rv is a local variable of the inc procedure, thus the
                                                                            predicates sign = 0, rv > a are both relevant, while the predicates
    A summary ⟨ϕ in , ϕout ⟩ indicates that if the input state of f sat-    flag = 0 and x > 0 are not.
isfies ϕ in , its output state must satisfy ϕout . In our implementation,      The irrelevant predicates have nothing to do with the procedure,
we require ϕ in to be a complete conjunction of predicate literals          and can be safely removed from this procedure’s summaries. Recall
and ϕout a “partial” one. This is accordant with the process of intra-      that each summary is associated with an abstract precision. To
procedural analysis [9], since from a single abstract state, there          reduce a summary, the corresponding abstract precision needs
usually can be more than one reachable abstract states at the exit          also be reduced. Let ⟨ϕ in , ϕout ⟩ be a summary with respect to an
point of the procedure.                                                     abstract precision λ. Recall that λ is a set of predicates; ϕ in and ϕout
    All procedure summaries are kept in a summary cache. During             can be considered as two sets of predicate literals. The summary
the program analysis, if a procedure call statement is encountered,         reduction proceeds as follows: identifies and removes all irrelevant
the verifier seeks in the cache for a proper summary. Let the called        predicates in and from λ; then removes all occurrences of these
procedure be f , the current abstract precision be λ, and the cur-          irrelevant predicates in both ϕ in and ϕout .
rent abstract data state be s. A summary of f is applicable to this            Note that the above summary reduction procedure is not com-
procedure call, if                                                          plete. It cannot guarantee removing all redundant information. For
    (1) it is with the same abstract precision λ, and                       a more powerful method, one may refer to the method of quanti-
    (2) its input condition ϕ in is satisfied by s.                         fiers elimination. However, our technique is much more efficient
If there exists an applicable summary, the cache returns ϕout of            than that of quantifiers elimination. Summary reduction is just an
the summary to the verifier. Otherwise, it returns “NULL”. In the           optimization, we are more interested in efficiency here.
latter case, the verifier needs to conduct a heavy intra-procedural            Note that at each callsite of a procedure, the current abstract
analysis to compute the output.                                             precision and the current input state need also be reduced. Then
    Note that testing if the input condition ϕ in of a summary is sat-      with these reduced abstract precision and reduced input state, the
isfied by the current abstract state requires a satisfiability checking.    verifier look applicable summaries up in the cache.
When Regression Verification Meets CEGAR                                                      Conference’17, July 2017, Washington, DC, USA


                   dump                     load                               1: inc(int,int)
                                                                                  {
                                                                                    …
                                                                               2:   (assert (= sign 0))
Program 𝑃𝑘                  Summary file              Program 𝑃𝑘+1             3:   (assert (> rv a))
                                                                                    {
                                                                               4:     (assert(not (= sign 0)))
Figure 3: Summary reuse across different program versions                      5:     (assert(and (not (= sign 0)) (> rv a )))
                                                                                    }
                                                                                    {
  Consider the program example in Fig. 1, assume the abstract                  6:     (assert(= sign 0))
                                                                               7:     (assert(and (= sign 0) (not (> rv a))))
precision of the inc procedure is {y > 0, siдn = 0, rv > a}, a                      }
possible summary of the procedure is                                                …
                                                                                  }
       ⟨y > 0 ∧ ¬(siдn = 0), y > 0 ∧ ¬(siдn = 0) ∧ rv > a⟩.          (3)
Assume the inc procedure is called again at a subsequent position,                 Figure 4: A summary example in text format
and assume the input state at that callsite is ¬(y > 0) ∧ ¬(sign =
0). Apparently, the input condition of (3) is not satisfied by this
input state. However, if we look into this summary, we find that
the predicate y > 0 is indeed irrelative to the inc procedure. By             Due to program changes, not all summaries of the old program
removing this predicate, we get a reduced summary                          can be reused in the current verification. Let P and P ′ be two ver-
                                                                           sions of a program. Let f be a procedure in P, and f ′ its updated
               ⟨¬(siдn = 0), ¬(siдn = 0) ∧ rv > a⟩.                        version in P ′ . Procedure summaries of f can be reused in the regres-
                                                                           sion verification, if and only if f and f ′ are semantically equivalent.
This reduced summary is now applicable to the second invocation.
                                                                              However, checking semantic equivalence of each procedure is
Removing irrelevant predicates can thus improve the hit rate of
                                                                           very time-consuming. We choose to perform syntactic checking
summaries .                                                                                                                               ′
                                                                           instead. More specially, we syntactically compare P and P to find
                                                                           a set τP of syntactically unchanged procedures. Note that a proce-
5   SUMMARY REUSE FOR REGRESSION                                           dure may call other procedures in its body. If the callee procedure
    VERIFICATION                                                           changes, even the caller procedure remains syntactically the same,
Summaries convey important information about the verification.             its semantics changes. We thus find a subset τP∗ of τP , such that
To reuse summaries in regression verification, we need to dump all         for any procedure f ∈ τP∗ , all its callee procedures are also in τP∗ .
summaries to an external file, called the summary file, after each         Note that this is a recursive definition. Then we have the following
verification run; and load the previously-generated summaries from         lemma.
the summary file to initialize the current summary cache, before
a regression verification starts (Fig. 3). In this way, the important         Lemma 5.1. For any procedure in τP∗ , its two versions in P and P ′
information stored in the procedure summaries is shared across             are semantically equivalent.
different program versions.
                                                                              Compared to semantic equivalence checking, our syntactic check-
5.1 Summary Dumping                                                        ing is less precise. There may exist procedures that are semantically
                                                                           equivalent but syntactically different. Summaries of such proce-
Summary dumping is quite simple. When a verification finishes,
                                                                           dures will be abandoned by our technique. Note that our syntactic
the verifier dumps all entries of the summary cache to an external
                                                                           checking is much more efficient. We indeed trade the maximal
file. Remark that this operation is performed in the end of the
                                                                           reuseability for efficiency.
verification, and does not intervene to the verification process.
                                                                              We use the set τP∗ to filter summaries in the process of summary
    We define a simple text-based format for the summary file. A
                                                                           loading. Only summaries that belong to some procedure of τP∗ are
fragment of the summary file for the program example is shown
                                                                           kept, and all others are directly abandoned. According to Lemma 5.1,
in Fig. 4, where the first line declares these summaries belong to
                                                                           all kept summaries belong to semantically equivalent procedures,
the inc procedure. Note that a procedure identifier consists of its
                                                                           and can be safely reused in the regression verification. Remark that
name and its type signature. Summaries of a procedure are grouped
                                                                           the computation of τP∗ and loading summaries can be realized as
by abstract precisions. Lines 2 to 3 of Fig. 4 declare an abstract
                                                                           a preprocessing step of the regression verification, and does not
precision, while lines 4 to 5, and 6 to 7 declare two summaries with
                                                                           intervene to the real verification process.
respect to this precision. The format for declaring predicates and
formulas follows the SMT-LIB standard [3].
                                                                           6   LAZY COUNTEREXAMPLE ANALYSIS FOR
5.2 Summary Loading                                                            REGRESSION VERIFICATION
Before the regression verification starts, we load the previously-         In the context of regression verification and CEGAR, the coun-
generated summaries from the summary file and then reuse them              terexample analysis is nontrivial. We explain in the following the
in the current verification.                                               problem and then present our solution.
Conference’17, July 2017, Washington, DC, USA                                                                         Fei He, Qianshan Yu, and Liming Cai

                                            main_new()                                                    main_new()

                                                    0                                                                 0

                                                …                                                            …
                                                    1                                                                 1      sign=flag          inc()
                                     [flag!=0]                                                      [flag!=0]                   a=x
                                                                                                                                                  6
                                                                                                         2                          [sign!=0]
                                            2

                         y = inc(x, flag)                                                                                                  7

                                            4                                                            4                       rv=a+1

                             [x>y]                                                          [x>y]
                                                                                                                                           9
                                                                                                                             y=rv
                                                                                                 Err
                                   Err




                     Figure 5: A counterexample                                          Figure 6: The expanded counterexample

                                                                             д = (li , opi , li+1 ). In other words, a CFA path represents a syntactical
6.1    The Problem                                                           walk through the CFA. A counterexample is a CFA path that ends
If the property cannot be verified with the current abstract precision,      at the error location ler r .
the verifier returns a counterexample. We need to check if this                 A path may contain procedure call operations. Replacing the pro-
counterexample corresponds to a real bug or not.                             cedure call operation with the corresponding intra-procedural path
    Fig. 5 shows a counterexample path, obtained by regression               is called an expansion. In the following, we assume all procedure
verification of the updated main procedure in Fig. 2. Each node on           call operations, except of holes, have already been expanded. For
the path represents an abstract state. Recall that an abstract state         example, the expansion of the counterexample in Fig. 5 is shown in
consists of a program location and an abstract data state. In the            Fig. 6. We call a path holeless if it contains no hole.
figure, only the program locations are labeled, whereas the abstract            Define the strongest post-condition operator SP as follows: for a
data states, for simplicity reason, are skipped.                             formula φ and an operation op (op is not a hole), SPop (φ) represents
    Note that there is a procedure call between l 2 and l 4 in the coun-     the set of data states that are reachable from any of the states
terexample. To validate this counterexample, the intra-procedural            that satisfy φ after the execution of op. The concrete semantics of a
path of the inc procedure needs be restored. Let s 2 and s 4 be the cor-     holeless path is the successive applications of the SP operator to
responding abstract data states at l 2 and l 4 , respectively. Assume in     operations of π , i.e., SP π (φ) = SPopn (. . . (SPop0 (φ) . . . ).
the verification step, the abstract data state s 4 is computed by intra-
                                                                                Definition 6.2. A holeless path π that starts from the abstract
procedural analysis on the inc procedure. After the intra-procedural
                                                                             state (l, s) is feasible if SP π (s) is satisfiable.
analysis, the reached states from s 2 of the inc procedure are com-
puted and cached in memory (for example, in the CPAchecker [9]).                Let H be the set of holes on the path π . These holes split π into
Now in the counterexample analysis step, with this reached set, the          |H | + 1 path segments. Each of these segments is a holeless path.
intra-procedural path of inc from s 2 to s 4 can be easily restored.         The concrete semantics of π is defined as the conjunction of the
    Assume in the verification step, the output state of the inc proce-      concrete semantics of these segments.
dure at s 2 is obtained from a cached summary that was generated                Theorem 6.3. Let π be a path with holes H , and Π the set of
in the previous verification. Then in the counterexample analysis,           segments of π split by H ,
there is no information for the reached set of the inc procedure,
                                                                                (1) if any segment in Π is infeasible, π is infeasible; and
We have to rely on the costly intra-procedural analysis to build
                                                                                (2) if all segments in Π are feasible, π is, however, not necessary
the inner path in inc from s 2 to s 4 . That is to say, the saved intra-
                                                                                    to be feasible.
procedural analysis gets back in the counterexample analysis. The
benefits of summary reuse are thus annulled to some extent by the               For the latter case, if all segments of π are feasible, we call the
counterexample analysis.                                                     path π is separately feasible. The above theorem states that the
                                                                             separately feasibility cannot prove the feasibility of the whole path.
  Definition 6.1. A procedure call operation is called a hole if the         This is obvious since the concrete semantics of holes are not taken
corresponding reached set of this procedure is not available.                into consideration in the separately feasibility.
                                                                                Consider the counterexample in Fig. 5, assume the procedure
6.2    Our Solution                                                          call operation at l 2 is a hole. It splits the path into two segments, i.e.
Let P be a program. An abstract path π is an alternating sequence                                               ...          [f l aд!=0]
of abstract states and operations, i.e.,                                                   σ1 = (l 0 , s 0 ) −−→ (l 1 , s 1 ) −−−−−−−−→ (s 2 , s 2 ),
                          op0               op1         opn−1                                                   [x >y]
          π = (l 0 , s 0 ) −−−→ (l 1 , s 1 ) −−−→ . . . −−−−−→ (ln , sn ).                 σ2 = (l 4 , s 4 ) −−−−−→ (ler r , ser r ).
The path π is called a CFA path if l 0 is the entry location of the          This counterexample is infeasible if either SP σ1 (true) or SP σ2 (s 4 ) is
program, and for each i with 0 ≤ i < n there exists a CFA edge               unsatisfiable.
When Regression Verification Meets CEGAR                                                     Conference’17, July 2017, Washington, DC, USA


   Our lazy analysis algorithm is shown in Alg. 1. The basic idea is to   are extracted from the “SystemsDeviceDriversLinux64ReachSafety”
expand holes only when needed. In this way, we avoid unnecessary          category of the 6nd International Competition on Software Veri-
hole expansions. The main body of the algorithm is a while loop.          fication (SV-COMP’17) [5]. We choose programs according to the
In the beginning of each iteration of the loop, the algorithm checks      following two criteria: (1) the lines of code is no less than 1000, and
whether the current path is holeless (isHoleless(π )) or not, and         (2) at least one refinement is required for verifying this program
whether the current path is infeasible (isInfeasible(π )) or not. If      using CPAchecker. In this way, we omit the trivial programs and
both checks returns f alse, the loop continues by expanding one           those that CEGAR is not needed. Moreover, we limit our selection
hole in π . Otherwise, the current path π must be either infeasible       to drivers from Linux 3.4 kernel and with the mutex lock/unlock
or holeless. For the former case, the algorithm returns π ; and for       specifications [10].
the latter case, it returns “unsafe”.                                        We use a higher-order mutation tool MiLu [26] to generate new
                                                                          revisions of these drivers. Up to 5 new revisions are randomly gen-
    Input: A finite abstract path π                                       erated for each device driver. Counting up the initial revision, there
    Output: The expanded path of π if it is infeasible; or “unsafe”       are 6 revisions for each driver. In total, we prepared a benchmark
               if it corresponds to a real path.                          set with 534 revisions of 89 device drivers.
    while ¬(isHoleless(π ) ∨ isInfeasible(π )) do                            For each device driver, the initial revision is verified from scratch.
         let h be a hole in π ;                                           Each mutated revision corresponds to a regression verification task.
         π ← expandHole(π , h);                                           Verification tasks are performed in an incremental way. Procedure
    end                                                                   summaries of the former revision are reused in the next revision.
    if isInfeasible(π ) then return π ;                                   In total, there are 534 verification tasks, among which 445 are
                                                                          regression verification tasks.
    else return unsafe ;
                                                                             All experiments are performed on a machine with a 3.6GHz 8
                      Algorithm 1: lazyAnalysis(π )
                                                                          Core CPU and 16GB RAM. We use Ubuntu 16.04 (64-bit) with Linux
                                                                          4.13 and jdk1.8.0. We use the predicateAnalysis-bam configuration
   A brute-force approach for counterexample analysis is to directly      for CPAchecker. Each verification run is limited to 90 seconds of
expand all holes of the counterexample, and then check its feasibility.   run time, 11GB of Java heap size and 4 CPU cores.
Compared to our lazy approach, the brute-force approach needs
only one feasibility checking. However, our approach is still more
beneficial. Firstly, with our lazy approach, the computational efforts    7.1    Overall Results
for unnecessary hole expansions (which in many cases are time-            We compare the performance of regression verification with and
consuming) are saved. Secondly and more importantly, the returned         without summary reuse in this experiment. For simplicity, in the
path by our approach is often much shorter than the fully expanded        following, we refer to our approach as summary reuse, and the
one. Note that the refinement is a heavy step in CEGAR. With a            approach without summary reuse as standalone.
shorter counterexample, the computation efforts for the refinement            Experimental results are listed in Table 1. We restrict this table
(for example, the interpolation-based refinement [28]) can often be       to the 35 best and 5 worst cases out of the total of 89 device drivers
significantly reduced.                                                    (sorted by the Speedup column). The first column (Device Driver)
   Our lazy analysis algorithm can be easily adapted to the exist-        lists the device drivers’ names. The second column (Rst) shows
ing CEGAR framework (for example, CPAchecker [9]). When the               the verification results, where the first and the second number
verifier in the existing framework returns a counterexample, our          indicate the amount of “safe” and “unsafe” results, respectively. The
algorithm is applied to check if this counterexample is spurious          third column (Loc) shows the lines of code for the initial version of
or not. In case of spurious counterexample, our algorithm returns         each device driver. The fourth column (T1st ) lists the verification
a (partially) expanded path, and gives it to an existing refiner in       time for the first version of each device driver. Recall that this is
the framework. The returned path by our algorithm may contain             not a regression verification task. T1st gives us information on the
holes. Treating these holes as value assignments, these paths can be      complexity of verifying each device driver.
directly processed by most of the existing refinement techniques,             The following two column assemblies report the experimental
for example, the interpolation-based refinement [28].                     results of standalone and summary reuse, respectively. For each
                                                                          approach, we report the total verification time (TT ot al ), the ver-
7    EXPERIMENTAL EVALUATION                                              ification time on the refinement step (TRef ) and the number of
We implemented our regression verification technique on top of            refinements (#Ref ). All results about time are expressed in seconds.
CPAchecker [9]. CPAchecker provides a configurable framework              Note that the verification time on all steps of CEGAR, and the time
for software verification. Predicate abstraction and counterexample       for processing and accessing procedure summaries are all counted
guided abstraction refinement are supported in CPAchecker. We             in TT ot al . For summary reuse approach, we also report the maximal
need to add supports for summary dumping, summary loading and             size of summary files (MaxFSize) among all revisions of each device
lazy counterexample analysis.                                             driver. The file size is expressed in Kilobyte. The last column shows
   To evaluate the effectiveness and efficiency of our summary            the time speedup of summary reuse over standalone. Recall that
reuse technique to the regression verification, we perform exten-         there are 5 mutated revisions for each device driver. Each row in
sive experiments on a large set of industrial programs. We take           the table sums up results of all regression verification tasks of the
device drivers from Linux kernel as the benchmark. All drivers            corresponding driver. The last (Total) row sums up results of all
Conference’17, July 2017, Washington, DC, USA                                                                 Fei He, Qianshan Yu, and Liming Cai


rows in the table (except for the MaxFSize column that takes the                                  10
maximal value).
   From Table 1, we observed that summary reuse outperforms
standalone in most of cases. More specially, among all 89 drivers,
summary reuse wins in 72 drivers. Our approach is a little bit slower
for 17 drivers. Looking at the 5 worst cases, their first-version




                                                                                 With Reduction
verification time are all less than 0.5 seconds. It is understandable
that on trivial verification tasks, our summary reuse approach may                                 1
not get the best performance. In total, the standalone approach
finishes all 445 regression verification tasks in 670.4 seconds, while
our summary reuse approach finishes in 460.2 seconds. The overall
time speedup of our approach is 31.4%.
   Comparing the numbers of refinements (# Ref ) required by sum-
mary reuse and standalone for each device driver, there is no obvious
pattern. Recall that with our approach the counterexample is ana-                                 0.1
lyzed in a lazy fashion. The path given to a refiner may not be as                                      0.1          1                  10
same as that using the standalone approach. Hence, the whole re-                                              Without Reduction
finement process may differ. However, if we look at the refinement
time (TRef ), we find that our approach is noticeably superior to stan-   Figure 7: Compare the total time of summary reuse with-
dalone. Using our approach, the total refinement time is decreased        /without summary reduction
from 97.4 to 42.7 seconds (about 56%). These results evidence the
effectiveness of our lazy counterexample analysis technique.
   Let us look at the MaxFSize column. The maximal size of sum-           of CEGAR. All results are presented in scatter diagrams, where each
mary files among all device drivers is 774.0KB (for most drivers,         point represents a single revision of a device driver. The X and Y
less than 500KB). The added overhead by our approach in storage           axes indicate the performance with and without lazy counterexam-
is acceptable.                                                            ple analysis , respectively. Both X and Y axes are logarithmic. Again,
                                                                          a point above the reference line indicates a case of performance
7.2 Impact of Summary Reduction                                           improvement.
The second experiment tests the impact of summary reduction to                On the whole, among all 445 regression verification tasks, lazy
our regression verification technique. We compare the performance         counterexample analysis shows a noticeably speedup (> 5%) in 312
of our approach with and without the summary reduction.                   cases for total verification time and in 376 cases for refinement time.
   The results are plotted in Fig. 7, where each point represents a       It is also observed that this technique yields shorter counterexample
regression verification task, with the X and Y axes representing the      paths for the majority (430 out of 445) of cases. These results con-
regression verification time using our approach with and without          form to our algorithmic analysis in Section 6. With the lazy analysis
summary reduction, respectively. There are totally 445 points in the      technique, the counterexample needs not be fully expanded. And a
figure. Timeout cases (exceeding 90 seconds) are projected to the         shorter counterexample can usually reduce the refinement efforts.
corresponding axis. Note that both X and Y axes are logarithmic.
Points below the reference line of y = x indicate a speedup case          8   RELATED WORK
with the summary reduction.                                               Regression verification was investigated mainly in two directions,
   We observe in Fig. 7 that the performance of our approach is           the verification of differences, and the reuse of previously computed
indeed improved by summary reduction. Among all 445 points,               results.
92 points are near to the reference line, indicating a comparable
                                                                             Verification of Differences. In this line of research, one attempts
performance (−5% ˜ 5%) with summary reduction; 341 points (in-
                                                                          to establish the correctness of the new program by proving its
cluding 73 timeout cases) are noticeably below the reference line,
                                                                          (conditional) equivalence to an old and verified program.
indicating a speedup of over 5%; only 12 points are noticeably above
                                                                             Many techniques have been proposed in this line of research.
the reference line, indicating a slow down of over 5%.
                                                                          Golden et al. [19] proposed an technique for proving conditional
                                                                          equivalence of two programs by abstraction and decomposition of
7.3 Impact of Lazy Counterexample Analysis                                procedures. Backes et al. [2] proposed to distinguish the program
The third experiment tests the impact of lazy counterexample anal-        behaviors that are impacted by the changes. Only the impacted
ysis to our regression verification technique. Various results, in-       program behaviors needed to be considered during the regression
cluding the verification time, refinement time and counterexample         verification. Beyer et al. [7] proposed the conditional model check-
length are used to evaluate the lazy counterexample analysis .            ing, which outputs a condition such that the program satisfies the
   These results are presented at Fig 8, where Fig 8(a), Fig 8(b)         specification under this condition. Böhme et al. [11] proposed a
and Fig 8(c) show results on verification time, refinement time and       partition-based regression verification technique. Instead of prov-
counterexample length, respectively. Note that the counterexample         ing the absence of regression errors for the complete input space,
length is the summation length of counterexamples in all iterations       this approach continuously verifies the input space in a gradual
When Regression Verification Meets CEGAR                                                                 Conference’17, July 2017, Washington, DC, USA

                                                    Table 1: Overall experimental results

                               Run set                              Standalone                            Summary Reuse

         Device Driver                Rst       Loc     T1st   TRef       TT ot al        #Ref   TRef     TT ot al   #Ref   MaxFSize   Speedup
         mtd-docprobe                 5/0      3145      3.2     1.7         15.3           55     0.3        1.9       5      194.3     87.5%
         block-paride-frpw            5/0      8044     21.7    33.6       102.5            95     7.0       40.1      40      774.0     60.8%
         media-mt2266                 5/0      4853      5.1     1.6         25.2           40     0.9       10.8      35      126.3     57.0%
         usb-dwc3-pci                 5/0      2784      1.2     0.7          5.7           20     0.2        2.7      10       55.2     52.0%
         media-max2165                5/0      5423      4.5     3.0         22.4           50     1.1       10.9      40      201.1     51.2%
         gpio-74x164                  5/0      3054      1.4     0.9          6.5           20     0.3        3.3      15       88.5     49.8%
         usb-otg-nop-xceiv            5/0      2075      1.4     1.0          7.4           25     0.3        3.7      15       71.3     49.7%
         input-ad714x-spi             5/0      3875      1.0     0.6          4.8           20     0.2        2.5      10       80.7     48.3%
         media-mc44s803               5/0      4624      2.4     1.0         12.0           50     0.6        6.3      25      132.9     47.9%
         rtc-ds3234                   5/0      3916      1.9     1.1          9.6           20     0.5        5.1      20       83.3     46.6%
         hwmon-max1111                5/0      2986      1.4     1.0          6.8           20     0.4        3.7      15       85.3     45.2%
         mfd-wl1273-core              5/0      3665      1.3     0.6          6.5           10     0.3        3.6      10      133.5     44.3%
         addac-adt7316-spi            4/1      2890      2.0     1.1          8.4           17     0.5        4.7      23       69.7     44.1%
         pci-ioapic                   5/0      3678      1.4     0.8          6.8           30     0.3        3.9      15       40.7     43.1%
         input-adxl34x-spi            5/0      3666      1.6     0.9          7.9           35     0.4        4.6      25       72.6     42.2%
         comedi-adl_pci7432           5/0      2720      2.0     0.9         10.3           30     0.5        6.0      23      118.5     41.8%
         meter-ade7854-i2c            5/0      3805      0.7     0.6          3.6           10     0.2        2.1      10      170.4     41.3%
         media-gspca_pac207           5/0      5668      3.2     1.2         16.1           55     0.8        9.5      45      153.5     40.8%
         rtc-max6902                  5/0      3855      1.7     1.1          8.7           20     0.6        5.3      20       78.1     38.8%
         dds-ad9910                   5/0      3609      1.6     1.1          8.3           30     0.5        5.3      14      140.8     36.4%
         gpio-mc33880                 5/0      2953      1.3     0.8          6.6           20     0.4        4.2      15       78.0     36.1%
         rtc-m41t94                   5/0      4242      2.1     1.1         10.2           20     0.7        6.6      20      111.8     35.9%
         parport_cs                   5/0      4510      2.0     0.9          9.9           35     0.6        6.4      25       94.4     35.6%
         touchscreen-ad7879           5/0      3778      2.0     1.1          9.7           40     0.6        6.2      25       77.9     35.5%
         rtc-stk17ta8                 5/0      4220      3.3     1.5         16.8           74     1.0       10.9      70      238.3     35.2%
         mtd_pagetest                 5/0      4723      1.3     0.3          6.9           15     0.4        4.6      15       36.1     34.3%
         misc-bmp085                  5/0      3675      1.4     1.0          7.6           15     0.6        5.2      18      154.7     31.1%
         hid-kensington               5/0      2305      0.8     0.6          4.2           20     0.2        2.9      15       33.1     30.9%
         mtd_subpagetest              5/0      4483      1.3     0.3          6.4           15     0.4        4.5      15      268.2     30.5%
         hid-ezkey                    5/0      2429      1.1     0.7          5.9           29     0.3        4.2      20       45.6     28.3%
         staging-zram                 5/0      8115      0.7     0.5          3.2            5     0.2        2.3       5      418.1     27.3%
         comedi-adl_pci7230           5/0      2661      2.1     0.9         10.4           25     0.7        7.6      24      111.4     27.1%
         dds-ad9951                   1/4      3088      1.6     0.9          6.0           18     0.5        4.4      13       82.0     25.7%
         misc-ti_dac7512              5/0      2623      0.4     0.4          2.2           10     0.2        1.7      10       47.3     24.3%
         usb-ums-usbat                5/0      9025      0.8     0.2          3.6           10     0.2        2.8      10      469.1     23.8%
                            ..                                                       ..                                         ..
                             .                                                        .                                          .
         Device Driver                Rst      Loc      T1st   TRef       TT ot al        #Ref   TRef     TT ot al   #Ref   MaxFSize   Speedup
         net-phy-realtek              3/2     3528       0.4     0.4          2.3            8     0.3        2.6       8       23.0     -13.8%
         x86-mxm-wmi                  4/1     2903       0.4     0.2          2.0           10     0.2        2.3      10       27.2     -17.2%
         net-phy-vitesse              5/0     3704       0.5     0.4          2.5           10     0.2        2.9      10       32.0     -18.8%
         w1_smem                      5/0     1072       0.3     0.3          2.0           15     0.2        2.5      15       18.4     -27.8%
         kfifo_buf                    5/0     1928       0.2     0.1          0.8            5     0.1        1.6       5       57.6    -105.2%
         Total                     418/27   342427     137.0    97.4       670.4          2175    42.7     460.2     1813      774.0      31.4%


manner. Felsing et al. [18] reduced the equivalence proving of two                 Reuse of Intermediate Results. In this line of research, one studies
related imperative integer programs to Horn constraints over unin-              the reuse of previously-generated results to the current verification.
terpreted predicates, and then solved the constraints using an SMT              A variety of information have been proposed for reuse.
solver. Moreover, Chaki et al. [14] studied the regression verification            Some researchers[23, 27, 36] proposed to keep the reached state
for multi-threaded programs,                                                    space and reuse them in the further verification runs. The rationale
                                                                                of these techniques is that state spaces of consecutive versions
Conference’17, July 2017, Washington, DC, USA                                                                                                                     Fei He, Qianshan Yu, and Liming Cai


                     10.0                                                             1.0                                                                       1000




                                                                                                                                           With Lazy Analysis
With Lazy Analysis




                                                                 With Lazy Analysis
                      1.0                                                             0.1                                                                       100




                      0.1                                                             0.0                                                                        10
                            0.1             1.0           10.0                              0.0               0.1                  1.0                                 10              100          1000
                                  Without Lazy Analysis                                           Without Lazy Analysis                                                     Without Lazy Analysis
                                     (a) Time                                                     (b) Refinement Time                                                   (c) Counterexample length


                              Figure 8: Compare the performance of summary reuse with and without lazy counterexample analysis


tend to be similar. However, recording and reusing reached state                                               test suite that can be used to revalidate the software as it evolves.
space may be costly, and these techniques may not be applicable to                                             Different from our approach, this technique is respect to regres-
large-scale programs.                                                                                          sion testing. The verification technique is used there, as an aid, to
   Visser et al.[35] noticed the importance of constraint solving for                                          validate dynamic properties (or invariants). In contrast, we aim
symbolic execution. They proposed to cache and reuse the results                                               to providing a new regression verification technique via reusing
of constraint solving. This approach was further improved in [1, 25]                                           procedure summaries.
from different aspects. This group of techniques are orthogonal
to our approach. These techniques can be applied to enhance our                                                9    CONCLUSION
approach.
                                                                                                               We proposed in this paper a fully automatic regression verifica-
   Beyer et al.[10] proposed to use abstract precisions as the in-
                                                                                                               tion technique in the context of CEGAR. Procedure summaries are
termediate results. An abstract precision defines the level of ab-
                                                                                                               reused across different abstract precisions and different program
straction, which conveys important information on the current
                                                                                                               revisions. We elaborated techniques for representing, processing
verification. They proposed to record the final abstract precision,
                                                                                                               and reusing procedure summaries. A summary reduction technique
and to reuse it as the initial abstract precision of the current verifi-
                                                                                                               was also proposed to improve the hit rate of summary cache. A lazy
cation. With this technique, the number of refinements can often
                                                                                                               counterexample analysis algorithm was further proposed to reduce
be reduced. Note that the precision reuse and our summary reuse
                                                                                                               the unnecessary path expansion efforts. Experimental results show
are orthogonal to each other. It is possible to combine these two
                                                                                                               promising performance of our technique.
reuse techniques together.
                                                                                                                  In the future, we are planning to investigate other kinds of inter-
   The most relevant work to ours is [17, 32], where an regression
                                                                                                               mediate results that can be reused in regression verification.
verification technique by means of interpolation-based procedure
summaries was proposed. However, the definition of procedure
summaries is different in that paper. A procedure summary in [32]                                              REFERENCES
is an over-approximation of all behaviors of the procedure. In con-                                             [1] Andrea Aquino, Francesco A Bianchi, Meixian Chen, Giovanni Denaro, and
                                                                                                                    Mauro Pezzè. 2015. Reusing constraint proofs in program analysis. In Proceedings
trast, a procedure summary in our paper is a pair of input and                                                      of the 2015 International Symposium on Software Testing and Analysis. ACM,
output states, representing a set of visited paths of the procedure.                                                305–315.
                                                                                                                [2] John Backes, Suzette Person, Neha Rungta, and Oksana Tkachuk. 2013. Regression
Our definition of summaries is consistent to the classical interpro-                                                verification using impact summaries. In Model Checking Software. Springer, 99–
cedural analysis techniques [30, 33], which has been realized in                                                    116.
most of the modern software verifiers (for example, CPAchecker).                                                [3] Clark Barrett, Aaron Stump, Cesare Tinelli, and others. 2010. The SMT-LIB stan-
                                                                                                                    dard: Version 2.0. In Proceedings of the 8th International Workshop on Satisfiability
Our summaries can be automatically generated by these interpro-                                                     Modulo Theories (Edinburgh, England), Vol. 13. 14.
cedural analysis techniques, without any additional computation                                                 [4] Dirk Beyer. 2016. Reliable and reproducible competition results with BenchExec
effort. In contrast, the interpolation-based summaries in [32] must                                                 and witnesses (Report on SV-COMP 2016). In International Conference on Tools
                                                                                                                    and Algorithms for the Construction and Analysis of Systems. Springer, 887–904.
be computed by an additional process, which in some cases maybe                                                 [5] Dirk Beyer. 2017. Software Verification with Validation of Results (Report on
quite time-consuming. On the other hand, the technique in [32] is                                                   SV-COMP 2017). In International Conference on Tools and Algorithms for the
                                                                                                                    Construction and Analysis of Systems. Springer, 331–349.
based on bounded model checking, while ours is developed in the                                                 [6] Dirk Beyer, Thomas A Henzinger, Ranjit Jhala, and Rupak Majumdar. 2007. The
context of CEGAR.                                                                                                   software model checker BLAST. International Journal on Software Tools for
   Pastore et al. [29] proposed a method to validate that an already                                                Technology Transfer 9, 5-6 (2007), 505–525.
                                                                                                                [7] Dirk Beyer, Thomas A Henzinger, M Erkan Keremoglu, and Philipp Wendler.
tested code has not been broken by an upgrade. It maintains a                                                       2012. Conditional model checking: a technique to pass information between
When Regression Verification Meets CEGAR                                                                          Conference’17, July 2017, Washington, DC, USA


     verifiers. In Proceedings of the ACM SIGSOFT 20th International Symposium on           [33] Micha Sharir and Amir Pnueli. 1978. Two approaches to interprocedural data
     the Foundations of Software Engineering. ACM, 57.                                           flow analysis. New York University. Courant Institute of Mathematical Sciences.
 [8] Dirk Beyer, Thomas A Henzinger, and Grégory Théoduloz. 2007. Configurable                   ComputerScience Department.
     software verification: Concretizing the convergence of model checking and pro-         [34] Fabio Somenzi. 2004. CUDD: CU decision diagram package-release 2.4. 0. Uni-
     gram analysis. In CAV, Vol. 7. Springer, 504–518.                                           versity of Colorado at Boulder (2004).
 [9] Dirk Beyer and M Erkan Keremoglu. 2011. CPAchecker: A tool for configurable            [35] Willem Visser, Jaco Geldenhuys, and Matthew B Dwyer. 2012. Green: reducing,
     software verification. In Computer Aided Verification. Springer, 184–190.                   reusing and recycling constraints in program analysis. In Proceedings of the ACM
[10] Dirk Beyer, Stefan Löwe, Evgeny Novikov, Andreas Stahlbauer, and Philipp                    SIGSOFT 20th International Symposium on the Foundations of Software Engineering.
     Wendler. 2013. Precision reuse for efficient regression verification. In Proceedings        ACM, 58.
     of the 2013 9th Joint Meeting on Foundations of Software Engineering. ACM, 389–        [36] Guowei Yang, Matthew B Dwyer, and Gregg Rothermel. 2009. Regression model
     399.                                                                                        checking. In Software Maintenance, 2009. ICSM 2009. IEEE International Conference
[11] Marcel Böhme, Bruno C d S Oliveira, and Abhik Roychoudhury. 2013. Partition-                on. IEEE, 115–124.
     based regression verification. In Proceedings of the 2013 International Conference     [37] Greta Yorsh, Eran Yahav, and Satish Chandra. 2008. Generating Precise and
     on Software Engineering. IEEE Press, 302–311.                                               Concise Procedure Summaries. In Proceedings of the 35th Annual ACM SIGPLAN-
[12] Randal E Bryant. 1986. Graph-based algorithms for boolean function manipula-                SIGACT Symposium on Principles of Programming Languages (POPL ’08). ACM,
     tion. Computers, IEEE Transactions on 100, 8 (1986), 677–691.                               New York, NY, USA, 221–234. DOI:http://dx.doi.org/10.1145/1328438.1328467
[13] Montgomery Carter, Shaobo He, Jonathan Whitaker, Zvonimir Rakamarić, and
     Michael Emmi. 2016. SMACK Software Verification Toolchain. In Proceedings
     of the 38th IEEE/ACM International Conference on Software Engineering (ICSE)
     Companion, Willem Visser and Laurie Williams (Eds.). ACM, 589–592.
[14] Sagar Chaki, Arie Gurfinkel, and Ofer Strichman. 2012. Regression verifica-
     tion for multi-threaded programs. In Verification, model checking, and abstract
     interpretation. Springer, 119–135.
[15] Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2000.
     Counterexample-guided abstraction refinement. In Computer aided verification.
     Springer, 154–169.
[16] Edmund M Clarke, Orna Grumberg, and Doron Peled. 1999. Model Checking.
     MIT press.
[17] Grigory Fedyukovich, O. Sery, and Natasha Sharygina. 2013. eVolCheck: In-
     cremental Upgrade Checker for C. In 19th International Conference on Tools
     and Algorithms for the Construction and Analysis of Systems (TACAS). Springer,
     Springer.
[18] Dennis Felsing, Sarah Grebing, Vladimir Klebanov, Philipp Rümmer, and Mattias
     Ulbrich. 2014. Automating regression verification. In Proceedings of the 29th
     ACM/IEEE international conference on Automated software engineering. ACM,
     349–360.
[19] Benny Godlin and Ofer Strichman. 2009. Regression verification. In Proceedings
     of the 46th Annual Design Automation Conference. ACM, 466–471.
[20] Todd L Graves, Mary Jean Harrold, Jung-Min Kim, Adam Porter, and Gregg
     Rothermel. 2001. An empirical study of regression test selection techniques.
     ACM Transactions on Software Engineering and Methodology (TOSEM) 10, 2 (2001),
     184–208.
[21] Sumit Gulwani and Ashish Tiwari. 2007. Computing procedure summaries for
     interprocedural analysis. In European Symposium on Programming. Springer,
     253–267.
[22] Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2013. Software
     model checking for people who love automata. In International Conference on
     Computer Aided Verification. Springer, 36–52.
[23] Thomas A Henzinger, Ranjit Jhala, Rupak Majumdar, and Marco AA Sanvido.
     2003. Extreme model checking. In Verification: Theory and Practice. Springer,
     332–358.
[24] Thomas A Henzinger, Ranjit Jhala, Rupak Majumdar, and Grégoire Sutre. 2002.
     Lazy abstraction. ACM SIGPLAN Notices 37, 1 (2002), 58–70.
[25] Xiangyang Jia, Carlo Ghezzi, and Shi Ying. 2015. Enhancing Reuse of Constraint
     Solutions to Improve Symbolic Execution. arXiv preprint arXiv:1501.07174 (2015).
[26] Yue Jia and Mark Harman. 2008. MILU: A customizable, runtime-optimized
     higher order mutation testing tool for the full C language. In Practice and Research
     Techniques, 2008. TAIC PART’08. Testing: Academic & Industrial Conference. IEEE,
     94–98.
[27] Steven Lauterburg, Ahmed Sobeih, Darko Marinov, and Mahesh Viswanathan.
     2008. Incremental state-space exploration for programs with dynamically allo-
     cated data. In Proceedings of the 30th international conference on Software engi-
     neering. ACM, 291–300.
[28] Kenneth L McMillan. 2006. Lazy abstraction with interpolants. In International
     Conference on Computer Aided Verification. Springer, 123–136.
[29] Fabrizio Pastore, Leonardo Mariani, Antti EJ Hyvärinen, Grigory Fedyukovich,
     Natasha Sharygina, Stephan Sehestedt, and Ali Muhammad. 2014. Verification-
     aided regression testing. In Proceedings of the 2014 International Symposium on
     Software Testing and Analysis. ACM, 37–48.
[30] Thomas Reps, Susan Horwitz, and Mooly Sagiv. 1995. Precise interprocedural
     dataflow analysis via graph reachability. In Proceedings of the 22nd ACM SIGPLAN-
     SIGACT symposium on Principles of programming languages. ACM, 49–61.
[31] Gregg Rothermel and Mary Jean Harrold. 1996. Analyzing regression test selec-
     tion techniques. Software Engineering, IEEE Transactions on 22, 8 (1996), 529–551.
[32] Ondrej Sery, Grigory Fedyukovich, and Natasha Sharygina. 2012. Incremental
     upgrade checking by means of interpolation-based function summaries. In Formal
     Methods in Computer-Aided Design (FMCAD), 2012. IEEE, 114–121.
