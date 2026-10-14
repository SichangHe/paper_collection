                                         Chapter 20
                                         Verification of Provers and Solvers

                                         René Thiemann


                                         Second readers: Frédéric Blanqui and Peter Lammich




                                         Abstract Automatic deduction tools such as automatic theorem provers, SAT (sat-
                                         isfiability) solvers, SMT (satisfiability modulo theories) solvers, and termination
arXiv:2607.25793v1 [cs.LO] 28 Jul 2026




                                         analyzers can be connected to proof assistants using various approaches, notably
                                         by certification and verification. This chapter reviews and compares the approaches
                                         available, and mentions several successful applications.




                                         20.1 Introduction

                                         In this chapter, we review the connection between proof assistants and automatic
                                         deduction tools such as automatic theorem provers, SAT (satisfiability) solvers,
                                         SMT (satisfiability modulo theories) solvers, and termination analyzers. We will
                                         see how the reliability of automated tools is increased with the help of proof assis-
                                         tants. Moreover, we will see that proof assistants can be useful when extending or
                                         modifying those inference rules that form the basis of the deduction tool (e.g., the
                                         rules of CDCL, DPLL(T ), or the superposition calculus). There is also the impor-
                                         tant possibility of using deduction tools to improve automation in proof assistants,
                                         which was already covered in Chapter 8.
                                            Although concrete domains such as SAT, SMT, and termination analysis are men-
                                         tioned, we do not assume any domain knowledge in these areas, but try to stay at a
                                         general level. Still, we will use a running example in a concrete domain. To be more
                                         precise, we consider a termination technique from first-order term rewriting that is
                                         also used in first-order theorem provers, namely, the lexicographic path ordering
                                         (LPO) [20] and the recursive path ordering with status (RPO) [16] where the latter
                                         ordering combines LPO and the recursive path ordering without status [15].

                                         René Thiemann
                                         University of Innsbruck, Innsbruck, Austria, e-mail: rene.thiemann@uibk.ac.at


                                                                                                                            1
2                                                                                           René Thiemann

Definition 20.1. Let Σ be a signature of first-order terms, and > be a strongly nor-
malizing order on Σ, called precedence. Then the LPO induced by the precedence >
is defined as a binary relation ≻ on terms via the following three inference rules:

                                            si ≻ t ∨ s i = t
                                       f (s1 , . . . , si , . . . , sn ) ≻ t                        (sub)
                       f >g           ∀ j ∈ {1, . . . , m}. f (s1 , . . . , sn ) ≻ t j
                                    f (s1 , . . . , sn ) ≻ g(t1 , . . . , tm )                     (prec)
                     si ≻ ti        ∀ j ∈ {i + 1, . . . , n}. f (s1 , . . . , sn ) ≻ t j
                          f (s1 , . . . , sn ) ≻ f (s1 , . . . , si−1 , ti , . . . , tn )           (lex)

   RPO extends LPO by a status where for every symbol one can choose whether
the arguments should be compared lexicographically as in (lex) or via a multiset
comparison. We omit a precise definition of RPO and further term rewriting related
notions, since they are not important for understanding this chapter. The interested
reader is referred to a textbook [4] for details.
   The following theorems are what make these orderings useful.
Theorem 20.2. LPO and RPO are reduction orders.
Theorem 20.3. Let ≻ be a reduction order. Whenever ℓ ≻ r for all rules ℓ → r of a
term rewrite system R, then R is terminating.



20.2 Certification

Certification is an approach to validate results from unreliable sources, such as
highly optimized automated deduction tools. These tools may depend on other un-
verified tools. Consider a termination prover that searches for suitable precedences
of LPO with the help of an SMT solver for integer arithmetic,1 which itself re-
lies on a C library for arbitrary precision integers. We only assume that the tools
generate some certificate in addition to the Boolean answer such as “the input is ter-
minating.”2 Such a certificate usually consists of a proof sketch (which techniques
or inference rules are applied in which order), in combination with auxiliary infor-
mations how the techniques are applied or parameterized. Certificates can be quite
verbose, but also sparse; for example, a certificate might only mention that a certain
decision procedure is applicable, without giving any further details.
    The advantage of certification (checking the result) over verification (fully veri-
fying the automated tool) is that the former is often simpler. For example, searching
1 A precedence can be synthesized by assigning natural numbers to each symbol, and then f > g is

defined via a comparison of the numbers of f and g.
2 These kinds of tools are called certifying algorithms or certifying computations by some au-

thors [2]. Here, we instead use the notion of certification exclusively for the process or algorithm
that checks a certificate, and not for the certificate-producing tools.
20 Verification of Provers and Solvers                                                      3

                                                     0=0
                                                                (sub)
               n=n                ack > s      ack(s(n), 0) ≻ 0
                       (sub)                                          (prec)
              s(n) ≻ n                     ack(s(n), 0) ≻ s(0)
                                                                             (lex)
                                ack(s(n), 0) ≻ ack(n, s(0))

Fig. 20.1 Inference tree for ack(s(n), 0) ≻ ack(n, s(0))



a suitable precedence for an LPO or RPO termination proof is NP-complete [23],
whereas checking an LPO or RPO proof with given precedence is usually simple:
polynomial time implementations of textbook definitions of LPO and RPO can eas-
ily be obtained by using memoization.3
Example 20.4. Consider the following encoding of the Ackermann–Péter function
as a term rewrite system over the signature Σ = {ack, s, 0}.

                                 ack(0, m) → s(m)
                               ack(s(n), 0) → ack(n, s(0))
                          ack(s(n), s(m)) → ack(n, ack(s(n), m))

A basic certificate of termination is “LPO with precedence ack > s.” An extended
certificate might additionally contain inference trees for each rule, e.g., the tree in
Figure 20.1 for the second rule.
  For certifying proofs that are generated by deduction tools there are two essential
questions.
(A) Are the applied techniques sound?
    For Example 20.4, this corresponds to the question whether we believe that The-
    orems 20.2 and 20.3 are indeed provable theorems. For other kinds of proofs, we
    might want to know whether the inference rules of CDCL are sound, whether a
    given superposition calculus is sound, etc.
(B) Are the techniques applied correctly?
    In Example 20.4, we have to ensure that the specified precedence is strongly
    normalizing and we need to check that ℓ ≻ r is satisfied for each rule ℓ → r of
    the rewrite system. Again, similar questions arise for other kinds of proofs.
   In the following, we will discuss four different ways to perform certification.




3 Note that the complexity of checking RPO constraints for a given precedence depends on

the exact definition of RPO. For certain extensions of RPO, already constraint checking is NP-
complete [32].
4                                                                        René Thiemann

20.2.1 Manual Certification

Clearly, humans can answer both questions (A) and (B) for Example 20.4: regarding
(A), the proofs can be found in the original paper or in a textbook on rewriting, and
these proofs can be checked manually; similarly, it is quite easy to verify manually
that the inference tree in Figure 20.1 is correct. We leave it as an exercise to the
reader to figure out suitable inference trees for the other two rules. Strong normal-
ization of the precedence of the example is obvious.
   The problem with manual certification is that it is error-prone and inefficient and
does not scale. In particular, answering question (B) without computer support is
often feasible only for toy examples.



20.2.2 Trusted Checker

A better solution to question (B) is by automating this task. The idea is the use
of a trusted checker, a program which takes certificates such as the one in Ex-
ample 20.4 as input, and then validates whether all techniques within that proof
have been applied correctly. Examples of such checkers have been used in various
competitions—e.g., DRAT-trim [34] was used as a checker in the SAT competition,
and CPAchecker [6] is a checker for SV-COMP.
   The obvious question at this point is why the checkers should be trusted. In other
words, what kind of additional guarantee do we get by using these checkers instead
of just relying upon the deduction tools? On the positive side, these checkers are
usually less complex programs compared with full deduction tools, since they only
have to check existing proofs instead of generating proofs, and therefore are less
likely to contain bugs. Moreover, since often the checkers are independent of the
deduction tools, using such a checker can increase the level of trust, since then two
independent systems agree upon the same proof.



20.2.3 Certification with Proof Assistants via Proof Script
       Generation

To increase the level of trust even further, we want to profit from the high reliability
of proof assistants with their small trusted code base (Section 1.6). Moreover, using
proof assistants not only we can increase the reliability with respect to question (B),
but we can also improve it with respect to question (A), namely, by formally verify-
ing the theorems.
   We illustrate a workflow for validating both questions with the help of a proof
assistant by applying it on Example 20.4. The idea is to develop a library, generate a
20 Verification of Provers and Solvers                                                 5

    Operation          File         Example Content

                                    definition rewrite-relation R = ...
1. Formalization     Library
                                    theorem 20.2: SN > –> red-order (LPO >)

                      Input         ack(0,m) -> m; ...
   Deduction
   Tool
                     Property       Terminating
                    Certificate     LPO(precedence: ack > s)

   2. Script
   Generator
                   Script with      definition ack-trs = ...
                   property +       lemma SN (rewrite-relation ack-trs)
                   proof            apply (theorem 20.3 where ≻ = LPO)
                                    ...
   3. Proof
   Checking

Fig. 20.2 Certification Workflow with Proof Assistants and proof script Generation



proof script for each example certificate, and then run the proof assistants to check
the scripts, as shown in Figure 20.2.
   Let us illustrate all three steps in some more detail.
 1. We need to develop a library that formalizes several domain-specific notions
    and theorems. In the LPO example, this library will contain notions such as
    strong normalization and term rewriting, the LPO might be formally defined
    as inductive predicate, and LPO properties such as Theorem 20.2 are available
    as formal theorems. However, the library does not include any particular in-
    puts and certificates; for example, it contains neither the rewrite system nor the
    precedence of Example 20.4.
 2. We need to develop a proof script generator: its task is to transform a given in-
    put certificate into a proof script for the proof assistant. This script contains two
    essential parts: the definition of the property of interest and the formal proof
    of this property. For Example 20.4, the first part will contain the formal defi-
    nition of the Ackermann–Péter system and the statement that it is terminating.
    The second part will be a formal proof of this statement, obtained by encod-
    ing the proof of the certificate into a script. This script may rely on everything
    that is provided by the proof assistant, the notions and theorems from the for-
    mal library of Step 1, as well as on tactics that have been tailor-made for the
    certification task.
 3. Finally, checking the proof is possible: a user must validate that the correct
    property has been defined in the first part, and then verifying the proof of the
    property is achieved by running the proof assistant.
6                                                                                    René Thiemann

   For the formal definition of the property, there are several design decisions re-
quired. For example, for the Ackermann–Péter system one could first define a new
datatype for the given signature (with constructors ack, s, 0) or just encode the three
symbols by strings. The first approach has the advantage that the proof assistant’s
type checker can ensure that no garbage terms such as ack(0, nil) can occur, at the
cost of having to create a symbol type for every input. Similarly, one can use invari-
ants or dependent types to ensure that all terms respect the arities of the symbols,
forbidding an input term such as ack(s).
   After having defined the property, we need a way to certify ℓ ≻ r for all rules
of the rewrite system, where we mention three alternatives. First, when given the
extended certificate described in Example 20.4, the proof script generator can easily
transform the inference tree into a proof script where each inference rule is trans-
lated into the corresponding introduction rule of the formal version of LPO. Second,
when only the basic certificate is available, the generator might reconstruct the infer-
ence tree for each rewrite rule with the help of some unverified algorithm, and then
translate the tree as in the first case; of course, adding extra information into the
certificate can also be done by an unverified preprocessor that runs before the proof
script generator. Alternatively, the proof script generator may just invoke some tailor
made tactic, that internally reconstructs the inference trees and additionally applies
the corresponding introduction rules. Third, one can perform a deep embedding4
and implement a verified algorithm within the proof assistant, which either ensures
ℓ ≻ r for a given precedence or outputs some error message. Then the proof script
generator only needs to invoke that algorithm and check that the result is not an
error.
   All of these three options can also be used to check complex combined proofs,
e.g., a termination proof consisting of several different termination techniques.
   Overall, certification with proof script generation has the advantage that it signif-
icantly decreases the trusted code base and in particular covers both questions (A)
and (B). One disadvantage in comparison with the usage of trusted checkers as in
Section 20.2.2 is a reduced execution speed: proof script generation in combina-
tion with running the proof assistant is usually much slower than just executing the
trusted checker. This might be a significant problem when it comes to checking
proofs which require many computations.



20.2.4 Certification with Proof Assistants via External Certification

A solution to the problem of reduced execution speed of the proof script approach
is available if the proof scripts are always of a very specific shape, namely, they
just consist of the invocation of some verified algorithm. In this case, the algorithm
provides a sufficient criterion for the desired property. Here, the certificate is mainly
used to guide the verified algorithm, e.g., which techniques should be applied, and
4 Modeling properties and proofs can be done using either a deep embedding or a shallow embed-

ding. We do not explain these concepts here, but just refer to Section 5.6.1 for further details.
20 Verification of Provers and Solvers                                                  7

      Operation           File           Example Content

                                         definition rewrite-relation R = ...
   1. Formalization     Library
                                         theorem 20.2: SN > –> red-order (LPO >)

   2. Formalization     Verified         definition SN-checker R C = ...
                        Checker          lemma SN-checker R C = Accepted –>
                                             SN (rewrite-relation R)
                       Executable        ...
                       Checker           export SN-checker ... to executable code

                         Input           ack(0,m) -> m; ...
      Deduction
      Tool
                        Property         Terminating
                       Certificate       LPO(precedence: ack > s)

      3. Proof
      Checking

Fig. 20.3 External certification workflow



how are these parameterized. Given such a verified algorithm, certification is pos-
sible outside the proof assistant, which gives an alternative workflow to Steps 1–3
mentioned in Section 20.2.3: external certification, shown in Figure 20.3.
1′ . Same as 1.
2′ . For each supported property P and certificate C, provide a verified algorithm
     that is a sufficient condition for the property: whenever the algorithm on input I
     and C does not complain, then P I holds. Export the verified algorithms into
     some executable program.
 ′
3 . Run the program on inputs and certificates. Here some wrapper can be used to
     select the suitable verified algorithm depending on the property P that needs to
     be verified.
   Clearly, external certification is faster than the previous approach: running a pro-
gram is much faster than first starting a proof assistant and then letting it check a
proof script. For instance, in experiments about termination proof certification the
certifier based on external certification was 50 times faster than its competitors that
have been using proof scripts [33]. As a consequence, more certificates can be han-
dled in reasonable time. This is in particular the case if the certification task requires
many computations.
   Note that it is not necessarily advantageous or always possible to provide helpful
details about computations in the certificate. For example, for checking safety proofs
via tree automata (a PSPACE-hard problem), one has to check a certain property
for all state-substitutions. Here, listing these state-substitutions in the certificate is
not advantageous at all: one has to generate all state-substitutions in a verified way
8                                                                          René Thiemann

in order to satisfy the criterion that ensures safety; consequently, comparing the
generated substitutions with the ones in the certificate just poses some extra work;
finally, certificates with an explicit list of substitutions would be much more bulky
and are thus more tedious to generate.
   Hence, for some kinds of proofs, efficiency of the verified algorithms becomes
a critical factor. In these cases, the integration of optimizations into the verified
algorithms becomes essential. This integration is often done using a refinement ap-
proach; that is, first an abstract algorithm is proved correct, and then it is refined to
an executable one where efficient data structures and algorithms are used to imple-
ment the abstract operations.
   Besides improved efficiency, external certification has one further advantage in
comparison with proof script generation: it is less brittle in the face of changes in
the proof assistant. The proof assistant only needs to be integrated statically for
Steps 1′ and 2′ . By contrast, such changes might also require modifications of the
proof script generator in Step 2 and required adaptations only become visible when
running it on example certificates.
   However, external certification also has two disadvantages compared with proof
script generation. First, some design decisions, which have been discussed before,
are no longer available; for example, we cannot create a datatype for the signature
that is used in a certificate, and also a shallow embedding is not possible anymore,
since the verified algorithm runs outside the proof assistant. The second disadvan-
tage is that external certification has a larger trusted code base. For instance, external
certification invokes the code generator of a proof assistant and an external compiler,
and both of these tools might not be formally verified. We refer to Section 5.6 for
further details on code generation.



Summary on Certification

To conclude, we mention several successful examples of certification using proof
assistants as it was described in Sections 20.2.3 and 20.2.4.
    • Coccinelle is a library on rewriting for the Rocq Prover (formerly known as
      Coq), and CiME3 contains a corresponding proof script generator [11,12]. Their
      approach uses a mixture of shallow and deep embedding and supports several
      termination techniques for term rewriting.
    • CoLoR is another Rocq libary on rewriting, and initially Rainbow was used
      as the corresponding proof script generator [9, 21]. In contrast to Coccinelle/
      CiME3, most of the formalization is using a deep embedding, so that later on
      external certification of termination proofs became available, and the develop-
      ment of Rainbow was stopped.
    • IsaFoR is the Isabelle Formalization of Rewriting [33]. From the outset, it was
      designed for external certification. Besides termination proofs of rewrite sys-
20 Verification of Provers and Solvers                                                   9

    tems, it also supports confluence proofs, complexity proofs, completion proofs,
    and proofs about tree automata and integer transition systems.
  • The developers of the three certifiers above have agreed on a standard certifica-
    tion format, CPF [29]. This format is currently used in the annual termination
    competition (termCOMP) and confluence competition (CoCo) to validate re-
    sults of competing certificate-producing tools.
  • Certifiers for SAT have been verified in various proof assistants [13, 24, 30].
    Here, the interesting part is of course checking unsatisfiability proofs. All cited
    certifiers expect their input in the DRAT format [18], a format that is easy to
    produce for tools and that has been used in recent SAT competitions. Since ef-
    ficiency is crucial for checking unsatisfiability proofs, all approaches are based
    on external certification. Moreover, preprocessing of the DRAT certificates is
    done by unverified algorithms, e.g., by adding extra information to speed up
    unit propagation in the verified algorithms.
  • Timbuk is a collection of tools that use tree automata completion to verify
    higher-order functional programs or cryptographic protocols. To increase relia-
    bility of the unverified Timbuk, a verified certifier for tree automata completion
    has been developed in Rocq [10]. Since checking the properties of tree automata
    involve heavy computations, the verified checker uses external certification.




20.3 Extensions of the Inference Systems

When running certifiers on certificates of deduction tools, it might happen that some
certificates are rejected. This in particular happens when a fixed combination of
technique, certifier, and deduction tool is tested for the first time, e.g., directly after
a new technique has been added to the certificate format, or when some tool added
certificate generation for the first time.
    There are at least four different reasons for rejected certificates.
    First, there might be some misunderstanding or imprecision in the certificate for-
mat. For example, should the indices of subterms si of inference rule (sub) be started
from 1 (as usual in papers) or from 0 (as usual in implementations)? Such problems
will result in many rejected certificates and are therefore easy to detect. Moreover,
they can be repaired easily, e.g., by making the specification of the certification for-
mat more precise. Afterward, one just has to adjust either the parser of the certifier
or the certificate generation part of the deduction tool. Here, a close collaboration
between the developers of the certifier and the deduction tool is definitely helpful,
where ideally the certificate format is codeveloped right from the start.
    Second, there might be a bug in the parser of the certifier or in the certificate
generating part of the deduction tool. Problems of this kind are very similar to the
first one: they are usually detected immediately and are easy to repair.
    Third, a certificate might contain an invalid proof, so certification reveals a real
bug in the deduction tool. In this situation, the bug can be repaired in the tool, possi-
10                                                                                                 René Thiemann

bly turning an unsound tool into a sound one. We briefly mention three examples of
these bugs. All of them remained unnoticed for some years and got revealed as soon
as certification of the effected techniques became available. The first bug caused
wrong nontermination answers, i.e., the tool “disproved termination” for some ter-
minating rewrite systems. The simple reason was that some of the applied tech-
niques in the tool ignored the evaluation strategy of the rewrite systems [28]. The
second bug resulted in wrong termination proofs [31]. Here the reason was a mis-
take in the implementation of some inference system for manipulating first-order
formulas. Finally, we mention bugs in tools for complexity analysis that have been
detected with the help of certification [3].
   Fourth, a certificate might contain proof steps that, despite being valid in prin-
ciple, are rejected by the certifier. The reason might be that the certifier uses only
a sufficient criterion to ensure validity of a certain proof step, or that the deduction
tool uses an extended set of inference rules in its implementation that deviates from
what is described in a corresponding paper, and hence also from what is checked
with respect to the formal statements. In both cases, an easy solution is to integrate
an option into the deduction tool so that users can restrict the reasoning engine of
the tool in a way that it solely uses approximations and inference rules that are
supported by the certifier. Such a restriction will usually come with a decrease in
power. The alternative is to make the certifier more powerful, e.g., by adding the
new inference rules to the formal definition.
   As an example, consider an extension of LPO by a new inference rule that sup-
ports least elements where it is allowed to compare a variable x against a constant
c that has least precedence. To this end, we can define a new nonstrict LPO order
≿ satisfying ≻ ⊆ ≿ and including rule (least), and modify the existing rule (lex). In
this way, rules such as f(x, s(y), z) → f(0, y, x) can be proved terminating by LPO.

                                                   ∀d. d ≥ c
                                                     x≿c                                                      (least)
  ∀ j ∈ {1, . . . , i − 1}. s j ≿ t j          si ≻ ti          ∀ j ∈ {i + 1, . . . , n}. f (s1 , . . . , sn ) ≻ t j
                                        f (s1 , . . . , sn ) ≻ f (t1 , . . . , tn )
                                                                                                                (lex′ )

   The advantage of having a formal proof at this point is that one can easily spot
where the proofs of the properties of LPO need adjustments. By contrast, doing a
rigorous proof checking manually on paper would at least be tedious, so it might
just be sketched, and errors might remain hidden. For example, while the above
extension of LPO is sound, the very same extension of RPO is unsound, since then
a crucial property of a reduction order is no longer satisfied [32].
   Knuth–Bendix orderings compatible with associativity and commutativity, called
AC-KBO, provide another example that an extension or a modification of a set of
inference rules is error-prone when done manually. There are several variants of
AC-KBO available [22, 27, 35], for which contradictory properties are stated in var-
ious papers: for example, one paper states that a particular variant is flawed, and a
later paper claims that there is no flaw in that variant, but instead one only needs
20 Verification of Provers and Solvers                                               11

an alternative proof. More details on the conflicting results on AC-KBO are given
by Yamada et al. [35], and at least their variant of AC-KBO has been verified in
Isabelle/HOL [25], so that the issue is finally settled via formal verification.
   Another success story is part of IsaFoL, the Isabelle Formalization of Logic [7],
that aims at developing formal theories about logics, proof systems, and automatic
provers. It contains a formal soundness and completeness proof [26] of a first-order
prover as it is presented in the Handbook of Automated Reasoning [5]. Besides the
intrinsic merits of verifying a prover, it is now possible to safely explore or modify
the underlying inference rules of the calculus (“hack without fear” as an anonymous
reviewer wrote [7]), since the proof assistant will rigorously check all proofs again
and point to those properties which break or need adjustments in their proofs.



20.4 Verified Deduction Tools

We saw in Section 20.2 that certification can be used to validate the output of de-
duction tools. Such a validation is no longer required if the deduction tool itself has
been fully verified. However, it is more work to develop a verified tool than a veri-
fied certifier. One of the reasons is that deduction tools are more efficiency critical
than checkers, since the former tools have to search for a proof. Consequently, they
usually contain more optimizations, which then all need to be formally verified. To
this end, often one can reuse commonly used algorithms and data structures (e.g.,
tree-based dictionaries, sorting algorithms) since verified implementations are al-
ready contained in libraries of proof assistants. A problem occurs if the deduction
tool to be verified crucially relies upon an imperative algorithm with mutable states.
In that case the verification and modeling task might become more complicated, in
particular if the default modeling language of the proof assistant is purely functional.
    A successful example for a verified deduction tool is the IsaSAT solver of Fleury
et al. [8] that has been developed as part of IsaFoL. It starts with a high-level
description of the algorithm in the form of inference rules which are both ab-
stract and non-deterministic. At this point many design decisions are still open and
implementation-dependent optimizations are not yet included, in particular since
these are not expressible on the abstract level. Afterward, an executable and deter-
ministic verified implementation is developed from the inference rules by a series
of refinement steps. One of the refinements is the inclusion of two watched literals
to speed up unit propagation and conflict detection. Interestingly, during the formal
proof development it was detected that the stated (paper) invariant for two watched
literals needed adjustments. A fixed invariant is now available in the formal proof
as well as in its textual description [8, Section 6].
    It should be said that at the time of writing, the combination of a highly optimized
deduction tool with a certifier run afterward is usually more efficient than a fully
verified deduction tool, despite the overhead in the certified approach where the
proof is processed twice. This was the approach taken by Lammich for his highly
optimized unsatisfiability certificate checker [24]. However, the fully verified tool
12                                                                              René Thiemann

might have stronger formal guarantees (e.g., being a decision procedure), whereas
in the certified approach the deduction tool may contain bugs and therefore might
produce uncertifiable proofs.
   Last but not least, proof assistants themselves are also deduction tools and are
therefore subject to verification. The work on the verification of Rocq and its un-
derlying metalogic have already been mentioned in Section 18.3.2. As further ex-
amples, we briefly mention work on verifying HOL Light [1, 17] and work on
Milawa [14], a verified proof assistant that is modeled after ACL2. Furthermore,
also certification is possible: proof assistants itself can export their internally gen-
erated proofs as a certificate, which can then be independently checked, e.g., by
Dedukti [19].



20.5 Conclusion

We have seen how deduction tools can profit from the usage of proof assistants. Ver-
ified certifiers detected several bugs in implementations of deduction tools, where
some of these bugs have not been noticed for years. Moreover, certifiers are suc-
cessfully applied in competitions of deduction tools, where they are used to validate
a large amount of automatically generated proofs.
    Core techniques that are implemented in deduction tools have been formally ver-
ified, resulting in two further benefits. On the one hand, faulty proofs in published
papers could be revealed and repaired. On the other hand, extensions of these tech-
niques can safely be investigated with the help of a proof assistant: “hack without
fear.”
    Finally, we also mentioned the development of verified deduction tools. Here,
the cost of verification is usually much higher than for certifiers, but it can be done.
Although the unverified tools usually outperform the verified tools, recently it was
shown that the situation might change: the verified solver IsaSAT won in the EDA-
Challenge 2021 against its unverified competitors. It will be interesting to see future
developments of verified solvers, in particular also those that target more complex
properties than SAT.



References

 1. Abrahamsson, O., Myreen, M.O., Kumar, R., Sewell, T.: Candle: A verified implementation
    of HOL light. In: J. Andronick, L. de Moura (eds.) ITP 2022, LIPIcs, vol. 237, pp. 3:1–3:17.
    Schloss Dagstuhl – Leibniz-Zentrum für Informatik (2022). URL
    https://doi.org/10.4230/LIPIcs.ITP.2022.3
 2. Alkassar, E., Böhme, S., Mehlhorn, K., Rizkallah, C.: A framework for the verification of
    certifying computations. J. Autom. Reason. 52(3), 241–273 (2014). URL
    https://doi.org/10.1007/s10817-013-9289-2
 3. Avanzini, M., Sternagel, C., Thiemann, R.: Certification of complexity proofs using CeTA.
    In: M. Fernández (ed.) RTA 2015, LIPIcs, vol. 36, pp. 23–39. Schloss Dagstuhl –
20 Verification of Provers and Solvers                                                         13

    Leibniz-Zentrum für Informatik (2015). URL
    https://doi.org/10.4230/LIPIcs.RTA.2015.23
 4. Baader, F., Nipkow, T.: Term Rewriting and All That. Cambridge University Press (1998).
    URL https://doi.org/10.1017/CBO9781139172752
 5. Bachmair, L., Ganzinger, H.: Resolution theorem proving. In: J.A. Robinson, A. Voronkov
    (eds.) Handbook of Automated Reasoning, vol. I, pp. 19–99. Elsevier and MIT Press (2001).
    URL https://doi.org/10.1016/b978-044450813-3/50004-7
 6. Beyer, D., Keremoglu, M.E.: CPAchecker: A tool for configurable software verification. In:
    G. Gopalakrishnan, S. Qadeer (eds.) CAV 2011, LNCS, vol. 6806, pp. 184–190. Springer
    (2011). URL https://doi.org/10.1007/978-3-642-22110-1_16
 7. Blanchette, J.C.: Formalizing the metatheory of logical calculi and automatic provers in
    Isabelle/HOL (invited talk). In: A. Mahboubi, M.O. Myreen (eds.) CPP 2019, pp. 1–13.
    ACM (2019). URL https://doi.org/10.1145/3293880.3294087
 8. Blanchette, J.C., Fleury, M., Lammich, P., Weidenbach, C.: A verified SAT solver framework
    with learn, forget, restart, and incrementality. J. Autom. Reason. 61(1–4), 333–365 (2018).
    URL https://doi.org/10.1007/s10817-018-9455-7
 9. Blanqui, F., Koprowski, A.: CoLoR: A Coq library on well-founded rewrite relations and its
    application to the automated verification of termination certificates. Math. Struct. Comput.
    Sci. 21(4), 827–859 (2011). URL https://doi.org/10.1017/S0960129511000120
10. Boyer, B., Genet, T., Jensen, T.P.: Certifying a tree automata completion checker. In:
    A. Armando, P. Baumgartner, G. Dowek (eds.) IJCAR 2008, LNCS, vol. 5195, pp. 523–538.
    Springer (2008). URL https://doi.org/10.1007/978-3-540-71070-7_43
11. Contejean, E., Courtieu, P., Forest, J., Pons, O., Urbain, X.: Certification of automated
    termination proofs. In: B. Konev, F. Wolter (eds.) FroCoS 2007, LNCS, vol. 4720, pp.
    148–162. Springer (2007). URL https://doi.org/10.1007/978-3-540-74621-8_10
12. Contejean, E., Courtieu, P., Forest, J., Pons, O., Urbain, X.: Automated certified proofs with
    CiME3. In: M. Schmidt-Schauß (ed.) RTA 2011, LIPIcs, vol. 10, pp. 21–30. Schloss
    Dagstuhl – Leibniz-Zentrum fuer Informatik (2011). URL
    https://doi.org/10.4230/LIPIcs.RTA.2011.21
13. Cruz-Filipe, L., Heule, M.J.H., Jr., W.A.H., Kaufmann, M., Schneider-Kamp, P.: Efficient
    certified RAT verification. In: L. de Moura (ed.) CADE 26, LNCS, vol. 10395, pp. 220–236.
    Springer (2017). URL https://doi.org/10.1007/978-3-319-63046-5_14
14. Davis, J., Myreen, M.O.: The reflective Milawa theorem prover is sound (down to the
    machine code that runs it). J. Autom. Reason. 55(2), 117–183 (2015). URL
    https://doi.org/10.1007/s10817-015-9324-6
15. Dershowitz, N.: Orderings for term-rewriting systems. Theor. Comput. Sci. 17, 279–301
    (1982). URL https://doi.org/10.1016/0304-3975(82)90026-3
16. Dershowitz, N.: Termination of rewriting. J. Symb. Comput. 3(1/2), 69–116 (1987). URL
    https://doi.org/10.1016/S0747-7171(87)80022-6
17. Harrison, J.: Towards self-verification of HOL Light. In: U. Furbach, N. Shankar (eds.)
    IJCAR 2006, LNCS, vol. 4130, pp. 177–191. Springer (2006). URL
    https://doi.org/10.1007/11814771_17
18. Heule, M.J.H.: The DRAT format and DRAT-trim checker (2016). URL
    http://arxiv.org/abs/1610.06229
19. Hondet, G., Blanqui, F.: The new rewriting engine of Dedukti (system description). In: Z.M.
    Ariola (ed.) FSCD 2020, LIPIcs, vol. 167, pp. 35:1–35:16. Schloss Dagstuhl –
    Leibniz-Zentrum für Informatik (2020). URL
    https://doi.org/10.4230/LIPIcs.FSCD.2020.35
20. Kamin, S., Lévy, J.J.: Two generalizations of the recursive path ordering. Tech. rep.,
    University of Illinois at Urbana-Champaign (1980)
21. Koprowski, A.: Coq formalization of the higher-order recursive path ordering. Appl. Algebra
    Eng. Commun. Comput. 20(5–6), 379–425 (2009). URL
    https://doi.org/10.1007/s00200-009-0105-5
14                                                                               René Thiemann

22. Korovin, K., Voronkov, A.: An AC-compatible Knuth-Bendix order. In: F. Baader (ed.)
    CADE-19, LNCS, vol. 2741, pp. 47–59. Springer (2003). URL
    https://doi.org/10.1007/978-3-540-45085-6_5
23. Krishnamoorthy, M.S., Narendran, P.: On recursive path ordering. Theor. Comput. Sci. 40,
    323–328 (1985). URL https://doi.org/10.1016/0304-3975(85)90175-6
24. Lammich, P.: Efficient verified (UN)SAT certificate checking. J. Autom. Reason. 64(3),
    513–532 (2020). URL https://doi.org/10.1007/s10817-019-09525-z
25. Lochmann, A., Sternagel, C.: Certified ACKBO. In: A. Mahboubi, M.O. Myreen (eds.) CPP
    2019, pp. 144–151. ACM (2019). URL https://doi.org/10.1145/3293880.3294099
26. Schlichtkrull, A., Blanchette, J.C., Traytel, D., Waldmann, U.: Formalizing Bachmair and
    Ganzinger’s ordered resolution prover. In: D. Galmiche, S. Schulz, R. Sebastiani (eds.)
    IJCAR 2018, LNCS, vol. 10900, pp. 89–107. Springer (2018). URL
    https://doi.org/10.1007/978-3-319-94205-6_7
27. Steinbach, J.: AC-termination of rewrite systems: A modified Knuth-Bendix ordering. In:
    H. Kirchner, W. Wechler (eds.) ALP ’90, LNCS, vol. 463, pp. 372–386. Springer (1990).
    URL https://doi.org/10.1007/3-540-53162-9_52
28. Sternagel, C., Thiemann, R.: Certification of nontermination proofs. In: L. Beringer, A.P.
    Felty (eds.) ITP 2012, LNCS, vol. 7406, pp. 266–282. Springer (2012). URL
    https://doi.org/10.1007/978-3-642-32347-8_18
29. Sternagel, C., Thiemann, R.: The certification problem format. In: C. Benzmüller, B.W.
    Paleo (eds.) UITP 2014, EPTCS, vol. 167, pp. 61–72 (2014). URL
    https://doi.org/10.4204/EPTCS.167.8
30. Tan, Y.K., Heule, M.J.H., Myreen, M.O.: cake_lpr: Verified propagation redundancy
    checking in CakeML. In: J.F. Groote, K.G. Larsen (eds.) TACAS 2021, Part II, LNCS, vol.
    12652, pp. 223–241. Springer (2021). URL
    https://doi.org/10.1007/978-3-030-72013-1_12
31. Thiemann, R.: Formalizing bounded increase. In: S. Blazy, C. Paulin-Mohring, D. Pichardie
    (eds.) ITP 2013, LNCS, vol. 7998, pp. 245–260. Springer (2013). URL
    https://doi.org/10.1007/978-3-642-39634-2_19
32. Thiemann, R., Allais, G., Nagele, J.: On the formalization of termination techniques based on
    multiset orderings. In: A. Tiwari (ed.) RTA 2012, LIPIcs, vol. 15, pp. 339–354. Schloss
    Dagstuhl – Leibniz-Zentrum fuer Informatik (2012). URL
    https://doi.org/10.4230/LIPIcs.RTA.2012.339
33. Thiemann, R., Sternagel, C.: Certification of termination proofs using CeTA. In:
    S. Berghofer, T. Nipkow, C. Urban, M. Wenzel (eds.) TPHOLs 2009, LNCS, vol. 5674, pp.
    452–468. Springer (2009). URL https://doi.org/10.1007/978-3-642-03359-9_31
34. Wetzler, N., Heule, M., Jr., W.A.H.: DRAT-trim: Efficient checking and trimming using
    expressive clausal proofs. In: C. Sinz, U. Egly (eds.) SAT 2014, LNCS, vol. 8561, pp.
    422–429. Springer (2014). URL https://doi.org/10.1007/978-3-319-09284-3_31
35. Yamada, A., Winkler, S., Hirokawa, N., Middeldorp, A.: AC-KBO revisited. Theory Pract.
    Log. Program. 16(2), 163–188 (2016). URL
    https://doi.org/10.1017/S1471068415000083
