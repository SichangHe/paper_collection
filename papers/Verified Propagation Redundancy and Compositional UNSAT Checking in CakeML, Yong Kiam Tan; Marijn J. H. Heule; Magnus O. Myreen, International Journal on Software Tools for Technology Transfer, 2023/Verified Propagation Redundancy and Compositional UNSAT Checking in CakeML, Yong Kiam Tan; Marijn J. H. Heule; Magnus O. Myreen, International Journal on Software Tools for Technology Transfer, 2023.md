International Journal on Software Tools for Technology Transfer (2023) 25:167-184
https://doi.org/10.1007/s10009-022-00690-y

  GENERAL

  Special Issue: TACAS 2021


Veriﬁed Propagation Redundancy and Compositional UNSAT
Checking in CakeML
Yong Kiam Tan · Marijn J. H. Heule · Magnus O. Myreen


Accepted: 4 November 2022 / Published online: 27 February 2023
© The Author(s) 2023




Abstract Modern SAT solvers can emit independently-                         proof formats; cake_lpr’s strong correctness guarantees
checkable proof certiﬁcates to validate their results. The                  are obtained without signiﬁcant sacriﬁce in its performance;
state-of-the-art proof system that allows for compact proof                 and the compositional proof format enables scalable parallel
certiﬁcates is propagation redundancy (PR). However, the                    proof checking for large proofs.
only existing method to validate proofs in this system with a
formally veriﬁed tool requires a transformation to a weaker                 Keywords linear propagation redundancy · binary code
proof system, which can result in a signiﬁcant blowup in                    extraction · compositional proof checking
the size of the proof and increased proof validation time.
This article describes the ﬁrst approach to formally verify
PR proofs on a succinct representation. We present (i) a                    1 Introduction
new Linear PR (LPR) proof format, (ii) an extension of the
                                                                            Given a formula of propositional logic, the task of a SAT
DPR-trim tool to eﬃciently convert PR proofs into LPR
                                                                            solver is to decide whether there exists an assignment that
format, and (iii) cake_lpr, a veriﬁed LPR proof checker
                                                                            satisﬁes the formula. Such a satisfying assignment, if found
developed in CakeML. We also enhance these tools with
                                                                            by a SAT solver, is easily veriﬁable by independent checkers
(iv) a new compositional proof format designed to enable
                                                                            and so one does not need to trust the inner workings of the
separate (parallel) proof checking. The LPR format is back-
                                                                            solver. The situation with unsatisfiable formulas, i.e., where
wards compatible with the existing LRAT format, but extends
                                                                            no satisfying assignment exists, is not as straightforward.
LRAT with support for the addition of PR clauses. More-
                                                                            Here, SAT solvers must produce an unsatisfiability proof
over, cake_lpr is veriﬁed using CakeML’s binary code
                                                                            (also called a refutation) for the input formula. Ideally, the
extraction toolchain, which yields correctness guarantees
                                                                            proof system and corresponding proof format for such proofs
for its machine code (binary) implementation. This further
                                                                            should be suﬃciently expressive, allowing SAT solvers to
distinguishes our clausal proof checker from existing check-
                                                                            eﬃciently produce proofs that correspond to the SAT solving
ers because unveriﬁed extraction and compilation tools are
                                                                            techniques they use at runtime. At the same time, the resulting
removed from its trusted computing base. We experimen-
                                                                            proofs ought to be eﬃciently checkable by independent and
tally show that: LPR provides eﬃciency gains over existing
                                                                            trustworthy tools.
                                                                               The de facto standard proof system for propositional
The ﬁrst author was supported by A*STAR, Singapore, the second
author was supported by the National Science Foundation (NSF)               unsatisﬁability proofs is Resolution Asymmetric Tautology
under grant CCF-2010951, and the third author was supported by the          (RAT) [31]. The associated DRAT format [55] combines
Swedish Foundation for Strategic Research, Sweden. This work was            clause addition based on RAT steps and clause deletion.
also supported by NSF award number ACI-1445606 at the Pittsburgh
                                                                            Independent checking tools can validate proofs in the DRAT
Supercomputing Center (PSC).
                                                                            format; they have been used to check the results of the SAT
Yong Kiam Tan and Marijn J. H. Heule                                        competitions since 2014 [55] and in industry [20]. Enriching
Computer Science Department, Carnegie Mellon University,
Pittsburgh, USA
                                                                            DRAT proofs with hints is the main technique for develop-
E-mail: yongkiat@cs.cmu.edu                                                 ing eﬃcient veriﬁed proof checkers, e.g., existing veriﬁed
E-mail: marijn@cmu.edu                                                      checkers use the enriched proof formats LRAT [10] and
Magnus O. Myreen (B)                                                        GRAT [39].
Chalmers University of Technology, Gothenburg, Sweden                          A recently proposed proof system, called Propagation
E-mail: myreen@chalmers.se                                                  Redundancy (PR) [28], generalizes RAT. There exist short

                                                                                                                                123
168                                                                                                          Yong Kiam Tan et al.


PR proofs without new variables for many problems that           extensions in cake_lpr to support the compositional proof
are hard for resolution, such as pigeonhole formulas, Tseitin    format. The new correctness result for cake_lpr allows
problems, and mutilated chessboard problems [26]. Due to         users to exploit veriﬁed compositional proof checking by
the absence of new variables it is easier to ﬁnd PR proofs       running parallel instances of the tool to check very large
automatically [27], and it is considered unlikely that there     unsatisﬁability proofs, such as those typically found in SAT-
exist short RAT proofs for these problems that do not intro-     solver aided proofs of mathematical results [23, 29, 35]. In
duce new variables nor reuse eliminated variables [28]. Such     particular, we explain how compositional proofs can be con-
PR proofs can be checked directly [28], or they can ﬁrst         veniently generated from the cube-and-conquer [22] SAT
be transformed into DRAT proofs or even Extended Res-            solving technique that is naturally parallelizable. Together
olution proofs by introducing new variables [25, 34]. In         with our veriﬁed checker, this enables a fully parallel pipeline
theory, the blowup is small, i.e., polynomial-sized. How-        for SAT solving, proof generation, and veriﬁed proof check-
ever, in practice, the transformed proofs can be signiﬁcantly    ing. To the best of our knowledge, this is the ﬁrst veriﬁcation
more expensive to validate compared to the original PR           result for a proof checker that formally accounts for multiple,
proofs [28].                                                     separate executions of the checker.
    A natural question arises: why should proof checkers be          Section 3 shows how PR proofs are enriched to obtain LPR
trusted to correctly check proofs if we do not likewise trust    proofs and presents the corresponding LPR proof checking
SAT solvers to correctly determine satisﬁability? One answer     algorithm (Contributions (i) & (ii)). Existing LRAT proof
is that proof checkers are much easier to implement so their     checkers can be extended in a clean and minimal way to
code can be carefully audited. Another answer is that the        support LPR proofs. Section 4 introduces the compositional
algorithms underlying proof checkers have been formally          proof format which extends an underlying clausal proof for-
verified in a proof assistant [10, 20, 39]. However, to get      mat with support for separate proof checking (Contribution
executable code for these veriﬁed checkers, some additional      (iv)). Section 5 explains the implementation of our proof
unveriﬁed steps are still required. Although unlikely, each of   checker in CakeML, as well as the correctness guarantees and
these steps can introduce bugs in the resulting executable:      high-level veriﬁcation strategy behind the proofs (Contribu-
(a) the algorithms are extracted by unveriﬁed code gener-        tions (iii) & (v)). Section 6 benchmarks our proof checker
ation tools into source code for a programming language;         against existing implementations. A summary comparison of
(b) unveriﬁed parsing, ﬁle I/O, and command-line inter-          the new proof checker against existing veriﬁed proof checkers
face code is added; (c) the combined code is compiled by         is in Table 1.
unveriﬁed compilers to executable machine code.
    The contributions of this article are: (i) a new Lin-
ear PR (henceforth LPR) proof format that enriches PR            2 Background
proofs with hints and is backwards compatible with the
                                                                 This section provides background on CakeML and its related
LRAT format, (ii) an extension of the existing DPR-trim
                                                                 tools. It also recalls the standard problem format and clausal
tool [28] to eﬃciently convert PR proofs into LPR for-
                                                                 proof systems used by SAT solvers.
mat, and (iii) cake_lpr, an eﬃcient veriﬁed LPR proof
checker with correctness guarantees, including for steps
                                                                 2.1 HOL4 and CakeML
(a)–(c) enumerated above. The cake_lpr tool was used to
validate the unsatisﬁability proofs for the 2020 SAT Com-        HOL4 is a proof assistant implementing classical higher-
petition because of its strong trust story combined with easy    order logic [51] and CakeML [45] is a programming
compilation and usage. Moreover, the stronger PR proof sys-      language with syntax and semantics formally deﬁned in
tem could be supported in future competitions. The tool is       HOL4. Tools for developing veriﬁed CakeML software are
publicly available at: https://github.com/tanyongkiam/cake_      used to ﬁll the veriﬁcation gaps in the correspondingly
lpr                                                              enumerated items in Section 1:
    This article extends our conference version [53] with:       (a) Two tools are used to produce (or extract) veriﬁed
(iv) a new compositional proof format consisting of a top-           CakeML source code in HOL4:
level summary proof whose proof steps can be separately
justiﬁed by respective underlying proofs and (v) veriﬁed




123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                                       169


Table 1 A comparison of SAT proof checkers that have been veriﬁed in various proof assistants [10, 20, 39]. Green background (cells with +)
indicates, in our view, desirable properties, e.g., LPR is based on a stronger proof system than LRAT and GRAT, while red backgrounds (cells with
×) indicate less desirable properties. Yellow backgrounds (cells with −) are also undesirable but to a lesser extent.

                  Property          ACL2 checker [20]       Coq checker [10]        GRATchk [39]        cake_lpr
               Proof System
                                    − LRAT                  − LRAT                  − GRAT              + LPR
                (Section 3)
              Executable Code           Directly                Unveriﬁed               Unveriﬁed           Binary Code
                                    −                       ×                       ×                   +
                (Section 5)             Executed                Extraction              Extraction          Extraction
              Checking Speed
                                    + Fast                  × Slow                  + Very Fast         + Fast (Parallelizable)
                (Section 6)




      – the CakeML proof-producing translator [46] auto-                         The input for propositional SAT solvers is a formula 𝐹
        matically synthesizes veriﬁed source code from pure                  in conjunctive normal form (CNF) over the set of variables
        algorithmic speciﬁcations;                                           𝑥1 , . . . , 𝑥 𝑛 . Here, CNF means that 𝐹 consists of an outer
                                                                                                          𝑚
      – the CakeML characteristic formula (CF) frame-                        logical conjunction 𝐹 ≡ 𝑖=1       𝐶𝑖 , where each clause 𝐶𝑖 is a
        work [19] provides a separation logic which can                      disjunction over some of the literals 𝐶𝑖 ≡ 𝑙 𝑖1 ∨ 𝑙 𝑖2 , · · · ∨ 𝑙 𝑖𝑘 ;
        be used to manually verify (more eﬃcient) imper-                     in general, each clause can contain a diﬀerent number of
        ative code for performance-critical parts of the proof               literals. Formulas in CNF can be represented directly as sets
        checker.                                                             of clauses and clauses as sets of literals. The empty clause is
(b) CakeML provides a foreign function interface (FFI)                       denoted ⊥.
    and a corresponding formal FFI model [15]. These are                         An assignment 𝛼 assigns boolean values (true or false) to
    used to verify system call interactions, e.g., ﬁle I/O                   each variable; 𝛼 can be partial, i.e., it only assigns values to
    and command-line interfaces, under carefully speciﬁed                    some of the variables. Like formulas and clauses, a (partial)
    assumptions on the system environment.                                   assignment 𝛼 can be represented as a set of literals such
(c) Most importantly, CakeML has a compiler that is ver-                     that 𝑙 ∈ 𝛼 iﬀ 𝛼 assigns 𝑙 to true. For consistency, 𝛼 may
    ified [54] to preserve the semantics of source CakeML                    contain at most one of each literal 𝑙 or its negation. The
    programs down to their compiled machine-code imple-                      negation of an assignment, denoted 𝛼, assigns the negation
    mentations. Hence, all guarantees obtained from the                      of all literals in 𝛼 to true. An assignment 𝛼 satisfies a clause
    preceding steps can be carried down to the level of                      𝐶 iﬀ their set intersection is nonempty. Additionally, we
    machine code with proofs.                                                deﬁne 𝐶 | 𝛼 =  if 𝛼 satisﬁes 𝐶; otherwise, 𝐶 | 𝛼 denotes the
                                                                             result of removing from 𝐶 all the literals falsiﬁed by 𝛼, i.e.,
   The combination of these tools enables binary code                        𝐶 | 𝛼 = 𝐶 \ 𝛼. For a formula 𝐹, we deﬁne 𝐹 | 𝛼 = {𝐶 | 𝛼 | 𝐶 ∈
extraction [36] where veriﬁed machine code is extracted                      𝐹 and 𝐶 | 𝛼 ≠ }. Intuitively, 𝐹 | 𝛼 contains the remaining
directly in HOL4. Several CakeML programs have been                          simpliﬁed clauses in formula 𝐹 after committing to the partial
veriﬁed using these tools, including: certiﬁcate checkers                    assignment 𝛼.
for ﬂoating-point error bounds [6] and vote counting [18],                       The task of a SAT solver is to determine whether 𝐹
an OpenTheory article checker [1], and the bootstrapped                      is satisfiable, i.e., whether there exists a (possibly partial)
CakeML compiler [54]. Other toolchains can be used to                        assignment 𝛼 such that 𝐹 | 𝛼 is empty. Any satisfying assign-
build veriﬁed checkers, e.g., Œuf provides a similar binary                  ment can be used as certiﬁcate of satisﬁability. Formulas
code extraction toolchain in the Coq proof assistant [44]; the               without a satisfying assignment are unsatisfiable. Certify-
Veriﬁed Software Toolchain [9] provides a program logic for                  ing unsatisﬁability is more diﬃcult and typically uses a
a subset of C which can be compiled with the veriﬁed com-                    clausal proof system [28]. The idea behind these proof sys-
piler CompCert [40]; and the Isabelle Reﬁnement framework                    tems is brieﬂy recalled next, using the key concept of clause
can produce veriﬁed LLVM implementations [37, 38].                           redundancy.


2.2 SAT Problems and Clausal Proofs                                          Deﬁnition 1 A clause 𝐶 is redundant with respect to formula
Fix a set of boolean variables 𝑥1 , . . . , 𝑥 𝑛 , where the nega-            𝐹 iﬀ 𝐹 ∧ 𝐶 and 𝐹 are both satisﬁable or both unsatisﬁable,
tion of variable 𝑥𝑖 is denoted 𝑥 𝑖 , and the negation of 𝑥 𝑖 is              i.e., they are satisﬁability equivalent.
identiﬁed with 𝑥𝑖 . Variables and their negations are called
literals and are denoted using 𝑙.

                                                                                                                                        123
170                                                                                                                 Yong Kiam Tan et al.


   A clause 𝐶 that is redundant for 𝐹 can be added to 𝐹 with-      various other notions of clause redundancy, including the
out changing its satisﬁability. Clausal proof systems work by      de facto standard Resolution Asymmetric Tautology (RAT)
successively adding redundant clauses to 𝐹 until the empty         proof system (see [28, Theorem 2]) that is able to compactly
clause ⊥ is added. Such a sequence of additions is illustrated     express all current techniques used in state-of-the-art SAT
below:                                                             solvers [31]. There is ongoing research towards integrating
                                                                   PR in SAT solvers [27, 28]. For example, PR-based prepro-
                                                                   cessing has been shown to improve solver performance on
        + redundant 𝐶1    + redundant 𝐶2                           SAT competition benchmarks [49].
               
       𝐹 =⇒ 𝐹 ∧ 𝐶1 =⇒ 𝐹 ∧ 𝐶1 ∧ 𝐶2                                     In practice, clausal proof formats also support clause
                                                                   deletions to speed up proof validation, especially for proof
                     ..
                      .                                            checking steps that need to iterate over the entire formula,
                                                                   e.g., 𝐹 | 𝛼 1 𝐹 | 𝜔 for Def. 2. Hence, unsatisﬁability proofs
                              =⇒ 𝐹 ∧ 𝐶1 ∧ 𝐶2 ∧ · · · ∧ ⊥
                                                               for formula 𝐹 are modeled as sequences 𝐼1 , . . . , 𝐼 𝑛 of instruc-
                          + redundant ⊥                            tions that either add or delete a clause; an addition instruction
                                                                   is a triple a, 𝐶, 𝜔 , where 𝐶 is a clause and 𝜔 is a (possi-
    Satisﬁability is preserved along each =⇒ step because          bly empty) witnessing assignment; a deletion instruction is
of clause redundancy, e.g., satisﬁability of 𝐹 implies sat-        a pair d, 𝐶 where 𝐶 is a clause. The sequence 𝐼1 , . . . , 𝐼 𝑛
isﬁability of 𝐹 ∧ 𝐶1 . Since the ﬁnal formula containing ⊥         gives rise to formulas 𝐹1 , . . . , 𝐹𝑛 with 𝐹0 = 𝐹, where 𝐹 𝑗
is unsatisﬁable, the sequence of redundant clause addition         is the accumulated formula, i.e., a (multi)set of clauses,
steps 𝐶1 , 𝐶2 , . . . , ⊥ corresponds to a proof of unsatisﬁa-     up to the 𝑗-th instruction computed recursively according
bility for 𝐹. Deciding clause redundancy is as hard as             to (1).
solving the SAT problem itself because ⊥ is always redun-                     
dant for unsatisﬁable formulas. The diﬀerence between                             𝐹 𝑗−1 ∪ {𝐶 𝑗 }   if 𝐼 𝑗 is of the form a, 𝐶 𝑗 , 𝜔
clausal proof systems is how the redundancy of a (pro-                 𝐹𝑗 =                                                           (1)
                                                                                  𝐹 𝑗−1 \ {𝐶 𝑗 }   if 𝐼 𝑗 is of the form d, 𝐶 𝑗
posed) redundant clause 𝐶 is eﬃciently certiﬁed at each proof
step.                                                                 A PR proof of unsatisﬁability is valid if the last instruction
    Many syntactic notions of redundancy are based on unit         adds the empty clause 𝐼 𝑛 = a, ⊥, ∅ , and, for all addition
propagation. A unit clause is a clause with only one literal.      instructions 𝐼 𝑗 = a, 𝐶 𝑗 , 𝜔 𝑗 , it holds that 𝐶 𝑗 is PR with
The result of applying the unit clause rule to a formula 𝐹 is      respect to 𝐹 𝑗−1 using witness 𝜔 𝑗 . In case an empty witness
the formula 𝐹 | 𝑙 where (𝑙) is a unit clause in 𝐹. The iterated    is provided for 𝐼 𝑗 , then 𝐹 𝑗−1 1 𝐶 𝑗 should hold.
application of the unit clause rule to a formula 𝐹 until no unit
clauses are left is called unit propagation. If unit propagation
on 𝐹 yields the empty clause ⊥, denoted by 𝐹 1 ⊥, we say           3 Linear Propagation Redundancy
that 𝐹 implies ⊥ by unit propagation. The notion of implied
by unit propagation is also used for regular clauses as follows:   This section describes a new clausal proof format called
                                                                  Linear Propagation Redundancy (LPR) which is designed
𝐹 1 𝐶 iﬀ 𝐹 ∧ ¬𝐶 1 ⊥ with ¬𝐶 = 𝑙 ∈𝐶 (𝑙). Observe that
¬𝐶 can be viewed as a partial assignment that assigns the          to enable eﬃcient validation of PR clauses using a (veri-
literals 𝑙, for 𝑙 ∈ 𝐶, to true. For a formula 𝐺, 𝐹 1 𝐺 iﬀ          ﬁed) proof checker. It also presents our enhancements to the
𝐹 1 𝐶 for all 𝐶 ∈ 𝐺. The main clausal proof system used            DPR-trim tool1 to eﬃciently add hints to PR proofs, thereby
in this article is based on propagation redundant clauses,         turning them into LPR proofs. Throughout the section, we
which are deﬁned as follows.                                       emphasize how LPR can be viewed as a clean and minimal
                                                                   extension of the existing LRAT proof format, which thereby
Deﬁnition 2 Let 𝐹 be a formula, 𝐶 a nonempty clause, and           enables its straightforward implementation in existing LRAT
𝛼 the smallest assignment that falsiﬁes 𝐶. Then, 𝐶 is prop-        tools.
agation redundant (PR) with respect to 𝐹 if there exists an           The most commonly used proof format for SAT solvers is
assignment 𝜔 which satisﬁes 𝐶 and such that 𝐹 | 𝛼 1 𝐹 | 𝜔.         DRAT, which combines deletion with RAT redundancy [55].
    Intuitively, a PR clause 𝐶 is redundant because any satis-     DRAT proofs are easy for SAT solvers to emit and top-tier
fying assignment for 𝐹 that does not already satisfy 𝐶 can be      SAT solvers support it, but they have some disadvantages
modiﬁed to a satisfying assignment for 𝐹 ∧ 𝐶 by updating its
literals assigned to true according to the (partial) witnessing
assignment 𝜔 (see [28, Theorem 1] for more details). Prop-
                                                                     1 LPR hint addition is now part of the public GitHub version of
agation redundancy is eﬃciently checkable in polynomial            DPR-trim using the command-line option -L at: https://github.com/
time using the witnessing assignment 𝜔 and PR generalizes          marijnheule/dpr-trim.


123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                               171


                                                                   literal in 𝜔 ∩ 𝛼 is removed as well as any literal in 𝜔 that is
                                                                   implied by unit propagation from 𝐹 | 𝛼. The shrinking was
                                                                   shown to be correct [28], but has not been implemented so
                                                                   far. We observed that the witnesses in the PR proofs produced
                                                                   by SaDiCaL [27] can be substantially compressed using this
                                                                   method.
                                                                       Fig. 2 (left) shows an example formula in the standard
                                                                   DIMACS problem format. The DIMACS format includes a
                                                                   header line starting with “p cnf ” followed by the number
                                                                   of variables and the number of clauses. The non-comment
                                                                   lines (not starting with “c ”) represent clauses, and they
Fig. 1 The grammar for the LPR format. Additions compared to the   end with “0”. Positive integers denote positive literals, while
LRAT grammar [10] are highlighted in bold.                         negative integers denote negative literals. By convention (fol-
                                                                   lowing LRAT), the clauses are implicitly indexed according
for veriﬁed proof checking. In particular, checking whether a      to their order of appearance in the ﬁle, starting from index
clause is RAT requires a signiﬁcant amount of proof search to      1. Fig. 2 (right) shows a corresponding proof in LPR for-
ﬁnd the unit clauses necessary for showing the implied-by-         mat.2 Deletion lines in LPR are formatted identically to
unit-propagation 1 property. This complicates veriﬁcation          LRAT [10] (not shown here). For clause addition lines, the
of the proof checking algorithm and slows down the resulting       LPR format only diﬀers from LRAT in case the clause to
veriﬁed proof checkers. The idea behind the Linear RAT             be added has PR but not RAT redundancy. A clause addi-
(LRAT) [10, 20] and GRAT [39] formats is to include these          tion line in LPR format consists of three parts. The ﬁrst
unit clauses as hints so that veriﬁed proof checkers can follow    part is the ﬁrst integer on the line, which denotes the index
the hints directly without the need for proof search. The          of the new clause. The second part exactly matches the PR
LPR format lifts this idea to allow fast validation of the PR      proof format [28]. It consists of the redundant clause and
property as follows.                                               its witness; the ﬁrst group of literals is the clause while the
    An assignment 𝜔 reduces a clause 𝐶 if 𝐶 | 𝜔 ⊂ 𝐶 and            (potentially empty) witness starts from the second occur-
𝐶 | 𝜔 ≠ . To check the PR property 𝐹 | 𝛼 1 𝐹 | 𝜔, it suf-         rence of the ﬁrst literal of the clause until the ﬁrst 0 that
ﬁces to check, for each clause 𝐶 ∈ 𝐹 reduced by 𝜔, that            separates the unit clause hints. The third part (after the ﬁrst
𝐹 | 𝛼 1 𝐶 | 𝜔. In practice, a smaller 𝜔 yields a cheaper PR        0) are the unit clause hints, which exactly matches the LRAT
check. The LPR format extends the PR format by adding, for         format [10].
each clause reduced by the witness, a list of all unit clause          The checking algorithm for LPR, shown in Fig. 3, overlaps
hints required for showing the implied-by-unit-propagation         signiﬁcantly with that for LRAT (see [10, Algorithm 1]). The
property. Additionally, in order to point to clauses, the LPR      only diﬀerences are in Steps 4 and 5.1. In Step 4, the witness
format includes an index for each clause at the beginning          is used (if present) instead of always using the ﬁrst literal in
of each line. The grammar of the LPR format is shown               𝐶 𝑗 . In Step 5.1, clauses are skipped if they are satisﬁed by the
in Fig. 1.                                                         witness. Notice that a clause can only be both reduced and
    The DPR-trim tool [28, Sect. 6] is built on top of             satisﬁed by a witness if the witness consists of at least two
DRAT-trim and facilitates veriﬁcation of DPR proofs, a             literals, while in the LRAT format witnesses always consist
generalization of DRAT proofs with PR clause addition.             of exactly one literal. Note also that the algorithm does not
If a clause addition step includes a witnessing assignment         check whether 𝐶 𝑗 | 𝜔 = , which is a requirement for PR.
𝜔, then the PR redundancy check is performed. Otherwise            This omission is allowed because the ﬁrst literal in 𝜔 in the
DPR-trim falls back on the RAT check from the DRAT-trim            LPR (and PR) format is syntactically the same as the ﬁrst
code base. Deletion steps are not validated. DPR-trim has          literal in 𝐶 𝑗 .
similar features compared to DRAT-trim, including back-
ward checking, extraction of unsatisﬁable cores, and proof
optimization.                                                        2 The 12 line PR proof in Fig. 2 (right) can be converted to a longer
    Our extension to DPR-trim enriches input PR proofs by          264 line RAT proof using earlier techniques [27] (not shown for brevity);
                                                                   to the best of our knowledge, there are no known short RAT proofs for
ﬁnding and adding all required unit clause hints to produce        these problems that do not introduce new variables nor reuse eliminated
LPR proofs. Most of the changes generalize the code to             variables [28].
produce LRAT proofs in DRAT-trim. The main PR-speciﬁc
optimization shrinks the witness 𝜔 where possible: every




                                                                                                                               123
172                                                                                                                              Yong Kiam Tan et al.




Fig. 2 (Left) Clauses of an unsatisﬁable pigeonhole formula (4 pigeons, 3 holes) in the DIMACS format used by SAT solvers. The ﬁrst 4 clauses
encode that each pigeon belongs to at least one hole, e.g., the variable 1 (resp. 4, 7, 10) is set to true iﬀ pigeon A (resp. B, C, D) is in the ﬁrst
hole; the latter 18 clauses encode that no two pigeons share the same hole, e.g., the clause -1 -4 encodes that pigeons A and B do not share the
ﬁrst hole. (Right) The LPR refutation consisting of clause-witness pairs and unit clause hints. The ﬁrst bold integer in each line is the clause index
while other bold integers are the unit clause hints. Dropping the bold integers yields a proof in the PR format. Redundant spaces have been added
to improve readability.




                                                                             of compositional proofs in propositional logic have been
                                                                             discussed in earlier work [24]; here, we deﬁne a format for
                                                                             compositional proofs and present a proof checking frame-
                                                                             work for the entire toolchain. Intuitively, the format consists
                                                                             of a top-level summary proof and a set of underlying proofs
                                                                             which are used to justify the top-level proof steps, see Fig. 4
                                                                             for an illustration (explained below). The underlying proofs
                                                                             can be checked separately and in parallel to speed up proof
                                                                             checking. Section 4.1 presents the proof format and its proof
                                                                             checking algorithm. Section 4.2 explains our technique for
                                                                             generating compositional proofs from the cube-and-conquer
                                                                             SAT solving technique [22].

                                                                             4.1 Compositional Proof Checking
                                                                             Compositional proofs are modeled using instruction
                                                                             sequences 𝐼1 , . . . , 𝐼 𝑛 similar to clausal proofs (Section 2.2)
                                                                             except addition instructions are of the form a, 𝐶 , i.e., they
                                                                             do not carry witnesses. The accumulated formulas 𝐹 𝑗 are
                                                                             deﬁned according to equation 1.
                                                                                 The key idea behind compositional proof checking is
                                                                             to justify a range of instructions simultaneously using an
                                                                             underlying clausal proof, see Fig. 4. More precisely, given
                                                                             a pair of indices (𝑖, 𝑗), with 𝑖 ≤ 𝑗, the algorithm checks
Fig. 3 Algorithm to check a single clause addition step in the LPR           that satisﬁability of the accumulated formula 𝐹𝑖 implies sat-
format. The bold parts show the additions compared to LRAT proof
                                                                             isﬁability of the accumulated formula 𝐹 𝑗 . By transitivity
checking [10].
                                                                             of satisﬁability implication, this means that a proof with 𝑛
                                                                             instructions can be checked by separately checking 𝑘 ranges
                                                                             (𝑖0 , 𝑖 1 ), (𝑖 1 , 𝑖 2 ), . . . , (𝑖 𝑘−1 , 𝑖 𝑘 ) for some choice of indices
4 Compositional Proofs                                                       0 = 𝑖 0 ≤ 𝑖 1 ≤ 𝑖 2 ≤ · · · ≤ 𝑖 𝑘 = 𝑛. If all 𝑘 checks succeed,
This section presents a new compositional proof format for                   then satisﬁability of 𝐹 implies satisﬁability of 𝐹𝑛 and, in
unsatisﬁability proof checking, motivated by the need to                     particular, if 𝐹𝑛 also contains ⊥ then the input formula 𝐹
check very large unsatisﬁability proofs behind SAT-solver                    is unsatisﬁable. Satisﬁability implication for each pair 𝐹𝑖 ,
aided proofs of mathematical results [23, 29, 35]. The rules                 𝐹 𝑗 is checked using an underlying clausal proof and its

123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                                              173




Fig. 4 Illustration of a compositional proof: the top-level proof is a sequence of instructions 𝐼1 , . . . , 𝐼𝑛 that can add or delete clauses; the indexes
𝑖0 , . . . , 𝑖𝑘 divide the top-level proof steps into ranges; and the boxes indicate underlying clausal proofs which are separately checked (indicated
by ) using instances of appropriate proof checkers, e.g., cake_lpr.




                                                                                Fig. 6 The grammar for the DRAT format [55], re-used for compo-
                                                                                sitional proofs. Each 𝑙𝑖𝑛𝑒 represents either addition (no preﬁx) or
                                                                                deletion (preﬁxed by “d”) of a clause.


                                                                                   To enable re-use of existing parsing tools, compositional
Fig. 5 Compositional proof checking algorithm for range (𝑖, 𝑗) based            proofs are syntactically represented using the DRAT for-
on an underlying clausal proof format.                                          mat [55], recalled in Fig. 6. Clauses are implicitly numbered
                                                                                according to their order of addition, continuing from the last
                                                                                (implicit) index of the corresponding DIMACS CNF. For
corresponding proof checker. A formal description of the                        example, starting from a DIMACS ﬁle with 5 clauses (indices
algorithm for checking range (𝑖, 𝑗) is in Fig. 5. By design,                    1–5), the ﬁrst added clause in the compositional proof has
there is signiﬁcant ﬂexibility in how the underlying proofs                     index 6, the second has index 7, and so on. Deletion steps
can be checked:                                                                 are ignored for the purposes of indexing.
 – The indexes 𝑖0 , 𝑖 1 , . . . , 𝑖 𝑘 can be chosen arbitrarily by
                                                                                4.2 Compositional Proof Generation
   tools, as long as they cover all steps of the top-level proof
   with 𝑖0 = 0, 𝑖 𝑘 = 𝑛.                                                        Compositional proofs can be generated particularly conve-
 – Diﬀerent clausal proof formats and corresponding proof                       niently from cube-and-conquer SAT proofs [22]. Given an
   checkers can be used for each underlying proof.                              input formula 𝐹, the basic idea behind cube-and-conquer is to
 – The underlying proofs can be checked separately, in any                      partition 𝐹 into a set of subformulas 𝐹 ∧𝐺 1 , 𝐹 ∧𝐺 2 , . . . , 𝐹 ∧
   order, and in parallel by running multiple instances of                      𝐺 𝑛 , and to solve each subproblem separately. Here, each
   proof checkers on several machines.                                          𝐺 𝑖 = 𝑙 1 ∧ 𝑙 2 ∧ · · · ∧ 𝑙 𝑗 is a cube, i.e., a conjunction of literals,
                                                                                                                               𝑛
                                                                                such that the disjunction of cubes 𝑖=1               𝐺 𝑖 is a tautology.

                                                                                                                                              123
174                                                                                                                      Yong Kiam Tan et al.




Fig. 7 Compositional proof used for the cube-and-conquer parallel SAT solving strategy. The boxes correspond to underlying proofs generated
by DRAT-trim for each cube which can be checked using cake_lpr or other LRAT tools [10]. In practice, the cubes 𝐺𝑖 used in the top-level proof
steps can be simpliﬁed to core subsets 𝐻𝑖 ⊆ 𝐺𝑖 obtained from incremental SAT solving.


Thus, if every subproblem 𝐹 ∧ 𝐺 𝑖 is unsatisﬁable, then 𝐹 is
unsatisﬁable.
    The compositional unsatisﬁability proof for 𝐹 under cube-
and-conquer is shown in Fig. 7, analogous to Fig. 4. Here,
the top-level proof is the sequence of 𝑛 additions of negated
cubes ¬𝐺 𝑖 (which are clauses), followed by addition of the
empty clause. The ﬁrst 𝑛 underlying proofs justify unsatisﬁ-
ability of 𝐹 under each cube, while the last proof shows that
the cube-and-conquer strategy correctly partitions the space
of assignments.
    The top-level proof steps can be simpliﬁed while gener-
ating the underlying clausal proofs for each step. In practice,
each subproblem 𝐹 ∧ 𝐺 𝑖 is tackled using incremental SAT
solvers that support solving 𝐹 under assumptions (or partial
assignments) 𝐺 𝑖 . Such assumptions are typically provided
either via iCNF ﬁles [56] or via the solver API; an exam-
ple formula with three cubes expressed in iCNF (DIMACS                   Fig. 8 (Left) Incremental CNF ﬁles for the pigeonhole formula
ﬁles extended with assumptions) is shown in Fig. 8. If the               from Fig. 2 split using three cubes (assumptions are speciﬁed using
formula 𝐹 is found to be unsatisﬁable under assumptions                  a ... 0 lines). (Middle) Generated DRAT proofs for each incremental
𝐺 𝑖 , incremental solvers can further compute a subset of the            CNF; the last line in each proof is ¬𝐻𝑖 . (Right) The top-level com-
                                                                         positional proof for the pigeonhole formula in Fig. 2 built from ¬𝐻𝑖 .
cube 𝐻𝑖 ⊆ 𝐺 𝑖 that was involved in determining unsatisﬁabil-
ity [13]. The negation ¬𝐻𝑖 can be used in the compositional
proof in place of ¬𝐺 𝑖 , e.g., the topmost cube in Fig. 8 has
a proof with 𝐻𝑖 ⊂ 𝐺 𝑖 . Since existing solvers with incre-
mental support can only log proofs in the DRAT format,                   𝐹 ∧ ¬𝐻1 ∧ · · · ∧ ¬𝐻𝑖−1 , which may help to simplify the
we modiﬁed DRAT-trim to convert such partial proofs into                 LRAT proof.
LRAT proofs that end with the addition of clause ¬𝐻𝑖 . In                   The ﬁnal line in compositional unsatisﬁability proofs is
addition, when generating the LRAT proof for ¬𝐻𝑖 , the                   the addition of the empty clause. In most use cases, there
compositional proof checking algorithm Fig. 5 allows us                  exists a short justiﬁcation of the empty clause using the added
to assume all previously added clauses, i.e., starting with              clauses in the compositional proof, e.g., the conjunction of
                                                                         preceding clauses in the compositional proof is typically

123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                     175


unsatisﬁable (in our case, by construction). Thus, a SAT           is NO, the input CNF could still be unsatisﬁable, but the
solver can be used on that formula to produce the justiﬁcation     input LPR proof is not valid according to the algorithm
of the empty clause in the appropriate clausal proof format.       in Fig. 3.
Alternatively, if the compositional proof was constructed             Step 3 uses imperative features in the CakeML
using more complicated cube-and-conquer strategies [22],           source language, e.g., (byte) arrays and exceptions,
then the underlying tree structure used to generate the cubes      to improve code performance; these optimizations are
can be used to guide the resolution steps for obtaining the        detailed further in Section 5.3. This step also adds
empty clause.                                                      user interface features like parsing and ﬁle I/O so
                                                                   that the input CNF formula is read (and parsed)
                                                                   from a ﬁle, and the results are printed on the stan-
5 CakeML Proof Checking                                            dard output and error streams. The veriﬁcation of
                                                                   this step uses CakeML’s proof-producing translator [46]
This section explains the implementation and veriﬁcation
                                                                   and characteristic formula framework [19] to prove
of cake_lpr, our veriﬁed CakeML LPR proof checker.
                                                                   the correctness of the source code implementation of
Section 5.1 focuses on the high-level veriﬁcation strat-
                                                                   cake_lpr; this code is subsequently compiled with the
egy which we used to reduce the veriﬁcation task to
                                                                   veriﬁed CakeML compiler [54]. Composing the correct-
mostly routine low-level proofs (details of the latter are
                                                                   ness theorem for source cake_lpr with CakeML’s compiler
omitted). Section 5.2 explains the main veriﬁed theorems
                                                                   correctness theorem yields the corresponding correctness
for the proof checker. Section 5.3 highlights some of
                                                                   theorem for the cake_lpr binary.
the veriﬁed performance optimizations used in the proof
                                                                      At the point of writing, the veriﬁed cake_lpr binary can
checker.
                                                                   be invoked from the command-line in ﬁve ways, each with
                                                                   associated soundness proofs (Section 5.2):
5.1 Implementation and Veriﬁcation Strategy
                                                                   1. cake_lpr <DIMACS>
The development of cake_lpr proceeds in three reﬁnement
                                                                      Parses the input ﬁle in DIMACS format and prints the
steps, where each step progressively produces a more con-
                                                                      parsed formula.
crete and performant implementation of the proof checker.
                                                                   2. cake_lpr <DIMACS> <LPR>
These reﬁnements are visualized in the three columns
                                                                      Runs LPR proof checking on the parsed formula.
of Fig. 9 for LPR proof checking. A similar veriﬁcation
                                                                   3. cake_lpr <DIMACS1> <LPR> <DIMACS2>
process was used to add support for compositional proof
                                                                      Runs LPR transformation checking on the parsed for-
checking.
                                                                      mulas, i.e., DIMACS1 is checked to imply DIMACS2
    Step 1 formalizes the deﬁnition of CNF formulas and their
                                                                      (satisﬁability-wise) using the LPR proof [10].
unsatisﬁability, as well as the PR proof system described
                                                                   4. cake_lpr <DIMACS> <COMP> i-j <LPR>
in Section 2.2. The inputs and outputs to the proof system
                                                                      Runs compositional proof checking on the parsed for-
are abstract and not tied to any concrete representation at this
                                                                      mula and compositional proof COMP for the range i–j
step. For example, input variables are drawn from an arbitrary
                                                                      and underlying LPR proof LPR.
type 𝛼, while clauses and CNFs are represented using sets.
                                                                   5. cake_lpr <DIMACS> <COMP> -check <OUTPUT>
The correctness of the PR proof system is proved in this step,
                                                                      Checks the combined result of several compositional
i.e., we show that a valid PR proof implies unsatisﬁability of
                                                                      proof checker executions (see below).
the input CNF. The proof essentially follows [28, Theorem
1].                                                                   Recall from Section 4.1 that cake_lpr needs to be exe-
    Step 2 implements a purely functional version of the           cuted (with option 4) for a set of ranges covering the lines of
LPR proof checking algorithm from Fig. 3. Here, the inputs         the compositional (top-level) proof COMP and we expect users
and outputs are given concrete representations with com-           to exploit this compositionality by running separate instances
putable datatypes, e.g., literals are integers (similar to         of cake_lpr in parallel on several machines. Accordingly,
DIMACS), clauses are lists of integers, and CNFs are               an important correctness caveat for compositional proof
lists of clauses. These concrete representations lift natu-        checking is that users correctly set up separate executions
rally to the abstract, set-based representation from Step          for their respective systems.
1. The output is a YES or NO answer according to the                  Option 5 is designed to add a simple layer of protection
algorithm from Fig. 3. The correctness theorem for Step            against user error when setting up separate (or parallel) exe-
2 shows that LPR proof checking correctly reﬁnes the               cutions. In particular, cake_lpr outputs the following string
PR proof system, i.e., if it outputs YES, then there exists        for each successful run of option 4, where md5 takes the MD5
a valid PR proof for the input (lifted) CNF; by Step 1,            hash of the input ﬁles:
this implies that the CNF is unsatisﬁable. If the output              s VERIFIED RANGE md5(DIMACS) md5(COMP) i-j

                                                                                                                       123
176                                                                                                                         Yong Kiam Tan et al.




Fig. 9 The three step reﬁnement used in the development of cake_lpr.




   The MD5 hash is chosen for convenience because it is                  Finally, lines (5) (in black) list the output behaviors of
available on most machines, so users can, e.g., manually               cake_lpr for each command-line option.3
compare md5 hashes of their input DIMACS and proof ﬁles                1. When cake_lpr is given one command-line argument
to check that the correct ﬁles were used on all machines.                 (length cl = 2)4, it attempts to read and parse the ﬁle before
By concatenating these outputs into an output ﬁle OUTPUT                  printing (if successful) the parsed formula to standard
and executing cake_lpr with option 5, cake_lpr can be                     output. The DIMACS parser (parse_dimacs) is proved to
used to check that the output ﬁle contains the correct hashes             be left inverse to the DIMACS printer (print_dimacs) as
and that the speciﬁed ranges appropriately cover the entire               follows:
compositional proof. Our implementation checks range cov-
                                                                              every wf_clause fml ⇒
erage (e.g., that ranges 0–2, 4–8, 2–4, 8–12 can be strung
                                                                             parse_dimacs ( print_dimacs fml) = Some fml
together to check range 0–12) by reusing a veriﬁed reacha-
bility checking function originally developed for a veriﬁed               This says that for any well-formed formula fml, printing
compiler optimization in the CakeML compiler [32].                        that formula into DIMACS format then parsing it yields
                                                                          the formula back. All parsed formulas are proved to be
5.2 Correctness Theorems                                                  well-formed (not shown here).
                                                                       2. If two arguments are given (length cl = 3), then if the
The main correctness theorem for cake_lpr in HOL4 is                      string “s VERIFIED UNSAT\n” is printed onto standard
shown in Fig. 10. The ﬁrst line (2) (in red) summarizes rou-              output, cake_lpr was provided with a ﬁle (in its ﬁrst
tine assumptions for compiled CakeML programs that use                    argument), and the ﬁle parses in DIMACS format to a
its basis library. Brieﬂy, it assumes that the command-line               formula fml whose lifted representation (interp fml) is
cl and ﬁle system fs models are well-formed and the com-                  unsatisﬁable.
piled code is placed in (and executed from) code memory                3–5. The speciﬁcations for the remaining cases have a
of a machine state ms according to CakeML’s x64 machine                   similar ﬂavor and are omitted here for brevity.
model mc.
                                                                          The correctness theorem for cake_lpr’s compositional
    The ﬁrst guarantee (3) (in blue) is that the machine-
                                                                       proof checking is shown in Fig. 11. The deﬁnition check_suc-
code implementation always terminates normally according
                                                                       cessful_par characterizes a successful set of runs of cake_lpr
to CakeML’s x64 machine-code semantics. Notably, this
                                                                       using command line options 4 and 5 on input strings fmlstr
means the binary never crashes and it may emit some I/O
                                                                       and pfstr. The lines in red (6) say that there is a list of
events when run; however, it possibly terminates with an out-
                                                                       output strings outs such that every entry of this list is pro-
of-memory error (extend_with_resource_limit) if the CakeML
                                                                       duced from the standard output of an execution of cake_lpr
runtime runs out of stack or heap space [54]. The second
                                                                       with command-line option 4 (with appropriate setup of each
guarantee (4) (in green) states that the only observable change
to the ﬁlesystem after executing cake_lpr are some strings                3 These lines feature HOL4 deﬁnitions for interacting with the
printed on standard output out and standard error err. To              ﬁlesystem fs, e.g., inFS_fname fs s says the string s is a valid ﬁle-
                                                                       name in fs, all_lines fs s returns the ﬁle contents as a list of strings (per
minimize user confusion, cake_lpr is designed to print all             line), and file_content fs s returns the ﬁle content as a raw string.
error messages to standard error and only success messages                4 By convention, the default (zeroth) command-line argument is
on standard output.                                                    always the name of the executable.


123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                         177




Fig. 10 The end-to-end correctness theorem for the CakeML LPR proof checker. The cases for command-line options 1 and 2 are shown here
(other cases are elided with . . . for brevity).




Fig. 11 The correctness theorem for compositional proof checking.




machine’s ﬁlesystem and command-line arguments).5 The                         The theorems in Figures 10 and 11 have a trusted com-
lines in blue (7) say that outs is successfully checked by                 puting base (TCB) where the CakeML compiler itself is not
an execution of cake_lpr with command-line option 5 and                    present. The TCB does, however, still include CakeML’s
the corresponding success string (concat [. . . ]) is printed to           model of the foreign function interface and assumed seman-
standard output. Using this deﬁnition, the correctness theo-               tics for the targeted hardware platform. CakeML’s TCB is
rem (8) says that on a successful set of runs, satisﬁability of            discussed in detail in prior publications [36, 42].
the formula fml parsed from fmlstr implies satisﬁability of the
ﬁnal formula run_proof fml pf obtained by running all lines
of the parsed proof pf on fml, i.e., if fml is 𝐹0 and pf has 𝑛
                                                                           5.3 Veriﬁed Optimizations
instructions, then run_proof fml pf computes the accumulated
formula 𝐹𝑛 as deﬁned in Section 4.1.                                       To minimize veriﬁcation eﬀort, CakeML’s imperative fea-
                                                                           tures are only used for the most performance-critical steps
                                                                           of cake_lpr. Our design decisions are based on empirical
                                                                           observations about the LPR proof checking algorithm. These
  5 In practice, this models users concatenating the outputs of multiple   are explained below with reference to speciﬁc steps in the
cake_lpr executions into a single ﬁle.                                     algorithm outlined in Fig. 3.

                                                                                                                            123
178                                                                                                                    Yong Kiam Tan et al.


5.3.1 Array-based representations                                   𝐹 𝑗 to be checked against the hashtable for 𝐺 in near-constant
                                                                    time.
In practice, many LPR proof steps do not require the full
strength of a PR (or RAT) clause. Hence, a large part of proof
checking time is spent in the Step 3 loop of the algorithm          5.3.4 Buﬀered I/O streams
(reverse unit propagation) and it is important to compute the
main loop bottleneck, 𝐶𝑖 | 𝛼 in Step 3.1, as eﬃciently as pos-      Proof ﬁles generated by SAT solvers can be large, e.g.,
sible. Here, CakeML’s native byte arrays are used to maintain       ranging from 300 MB to 4 GB for the second benchmark
a compact bitset-like representation of the assignment 𝛼, so        suite in Section 6. These ﬁles are streamed into memory line
that 𝐶𝑖 | 𝛼 can be computed in one pass over 𝐶𝑖 with constant       by line because each proof step depends only on informa-
time bitset lookup for each literal in 𝐶𝑖 .                         tion contained in its corresponding line in the ﬁle. This
   For proof steps requiring the full strength of PR clauses,       streaming interaction is optimized using CakeML’s veri-
Step 5 loops over all undeleted clauses in the formula. For-        ﬁed buﬀered I/O library [41] which maintains an internal
mulas are represented as an array of clauses6 together with         buﬀer of yet-to-be-read bytes from the read-only proof ﬁle to
a lazily updated list that tracks all indices of the array con-     batch and minimize the number of expensive ﬁlesystem I/O
taining undeleted clauses. This enables both constant-time          calls.
lookup of clauses throughout the algorithm and fast itera-
tion over the undeleted clauses for Step 5. Deletion in the         5.3.5 Producing MD5 hashes
index list is done in (amortized) constant time by remov-
ing a deleted index only when the index is looked up in             As part of this work, we veriﬁed a CakeML library for
Step 5.1.                                                           computing the MD5 hash of an input stream which is con-
   Additionally, for each literal, the smallest clause index        nected with the buﬀered I/O library to eﬃciently compute
where that literal occurs (if any) is lazily tracked in a lookup    hashes for the compositional proof checking command-line
array; for a given witness 𝜔, all clauses occurring at indices      options 4 and 5 in Section 5.1. The veriﬁcation shows that
below the index of any literal in 𝜔 can be skipped in Step          our imperative implementation of MD5 hashing matches
5.1.                                                                its functional speciﬁcation. In particular, since the MD5
                                                                    hash is provided solely for user convenience, we do not
                                                                    prove any formal cryptographic properties of the hashing
5.3.2 Proof checking exceptions                                     function.
There are several steps in the proof checking algorithm that
can fail (report NO) if the input proof is invalid, e.g., in Step
3.3. In a purely functional implementation, results are rep-
                                                                    6 Benchmarks
resented with an option: None indicating a failure and Some
res indicating success with result res. While conceptually          This section compares the CakeML LPR proof checker
simple, this means that common case (successful) interme-           against other veriﬁed checkers on two benchmark suites
diate results are always boxed within a Some constructor and        (Sections 6.1 and 6.2) and a RAT microbenchmark (Sec-
then immediately unboxed with pattern matching to be used           tion 6.3). It also evaluates the compositional proof format on
again. In cake_lpr, failures instead raise exceptions which         unsatisﬁability proofs of Erdős discrepancy properties [35]
are directly handled at the top level. Thus, successful results     (Section 6.4). The ﬁrst suite is a collection of problems
can be passed directly, i.e., as res, without any boxing. Sup-      with PR proofs generated by the satisfaction-driven clause
port for verifying the use of exceptions is a unique feature of     learning (SDCL) solver SaDiCaL [27]; the second suite con-
CakeML’s CF framework [19].                                         sists of unsatisﬁable problems from the SAT Race 2019
                                                                    competition.7 The RAT microbenchmark consists of proofs
                                                                    for large mutilated chessboards generated by a BDD-based
5.3.3 Hashtables
                                                                    SAT solver [8]. The unsatisﬁability proofs for the Erdős
For compositional proof checking (Fig. 5), it is important to       discrepancy properties are generated by cube-and-conquer
check the inclusion of clauses 𝐹 𝑗 ⊆ 𝐺 eﬃciently since both         (see Section 4.2). Raw timing data used to produce the ﬁg-
formulas can contain a large number of clauses. To achieve          ures and tables in this section is available from the cake_lpr
this, the formula 𝐺 (in the array-based representation) is          repository.
converted into CakeML’s veriﬁed hashtable library using a
simple rolling hash for clauses. This allows every clause in
                                                                      7 The suites are available at http://fmv.jku.at/sadical/ and http://sat-
                                                                    race-2019.ciirc.cvut.cz/ respectively. Note that cake_lpr was also used
  6 Deleted clauses are no longer referenced by the array and are   to validate proofs for the 2020 SAT Competition (results not reported
automatically freed by CakeML’s garbage collector.                  here).


123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                            179


   The CakeML checker is labeled cake_lpr (default                    (summing SaDiCaL, pr2drat, GRATgen and GRATchk
4GB heap and stack space), while the other proof check-               times) is much slower than the LRAT toolchains (sum-
ers used are labeled acl2-lrat (veriﬁed in ACL2 [20]),                ming SaDiCaL, pr2drat, DRAT-trim and fastest LRAT
coq-lrat (veriﬁed in Coq [10]), and GRATchk (veriﬁed                  checking times). This is in contrast to the SAT Race
in Isabelle/HOL [39]) respectively. All experiments were              2019 benchmarks below (see Fig. 12), where we observed
ran on identical nodes with Intel Xeon E5-2695 v3 CPUs                the opposite relationship. We believe that the diﬀer-
(35M cache, 2.30GHz) and 128GB RAM; more speciﬁc                      ence in checking speed is due to the various checkers
conﬁguration options for each benchmark suite are reported            having diﬀerent optimizations for checking the expen-
below.                                                                sive RAT proof steps produced by conversion from PR
                                                                      proofs.
6.1 SaDiCaL PR Benchmarks
                                                                      6.2 SAT Race 2019 Benchmarks
The SaDiCaL solver produces PR proofs for hard SAT prob-
lems in its benchmark suite [27] and it is experimentally             We further benchmarked the veriﬁed checkers on a suite of
much faster than a plain DRAT-based CDCL solver on                    102 unsatisﬁable problems from the SAT Race 2019 com-
those problems [27, Section 7]. The PR proofs are directly            petition.9 For all problems, DRAT proofs were generated
checked by cake_lpr after conversion into LPR format with             using the state-of-the-art SAT solver CaDiCaL before con-
DPR-trim. For all other checkers, the PR proofs were ﬁrst             version into the LRAT or GRAT formats. Proofs generated
converted to DRAT format using pr2drat (as in an earlier              by CaDiCaL on this suite rarely require RAT (or PR) steps,
approach [27]), and then into LRAT and GRAT formats using             so the checkers are stress-tested on their implementation of
the DRAT-trim and GRATgen8 tools respectively. All tools              ﬁle I/O, parsing, and reverse unit propagation based on the
were ran with a timeout of 10000 seconds and all timings are          annotated hints (Step 3.1 from Fig. 3); cake_lpr is the only
reported in seconds (to one d.p.). Results are summarized in          tool with a formally veriﬁed implementation of the former
Tables 2 and 3.                                                       two steps. All tools were ran with the SAT competition solver
   All benchmarks were successfully solved by SaDiCaL                 timeout of 5000 seconds.
except mchess19 which exceeded the time limit. For the                   A summary of the results is given in Table 4, where
remaining benchmarks, generating and checking LPR proofs              all proofs generated by CaDiCaL were checked by at least
required a comparable (1–2.5x) amount of time to solving              one veriﬁed checker. The acl2-lrat checker fails with a
the problems, except mchess, for which LPR generation                 parse error on one problem even though none of the other
and checking is much faster than solving the problems                 checkers reported such an error; GRATgen aborted on two
(Table 2). Unsurprisingly, direct checking of LPR proofs              problems for an unknown reason. Plots comparing LRAT
is much faster than the circuitous route of converting into           proof checking time and overall proof generation and check-
DRAT and then into either LRAT or GRAT (Table 3).                     ing time (LRAT and GRAT) are shown in Fig. 12. From
Unlike LPR, checking PR proofs via the LRAT route is                  Fig. 12 (top), the relative order of LRAT checking speeds
5–60x slower than solving those problems; this is a sig-              remains the same as Table 3, where cake_lpr is on aver-
niﬁcant drawback to using the route in practice for certifying        age 1.2x slower than acl2-lrat, although cake_lpr is
solver results. Compared to an unveriﬁed C implementa-                faster on 28 benchmarks. From Fig. 12 (bottom), both LRAT
tion of LPR proof checking, cake_lpr is approximately                 toolchains are slower than the GRAT toolchain (average 3.5x
an order of magnitude slower on these benchmarks; a                   slower for cake_lpr and 3.4x for acl2-lrat). Part of this
detailed comparison against unveriﬁed proof checking is               speedup for the GRAT toolchain comes from GRATgen which
in Section 6.3.                                                       can be run in parallel (with 8 threads). This suggests that
   The backwards compatibility of cake_lpr is also shown              adding native support for GRAT-based input to cake_lpr
in Table 3, where it is used to check the generated LRAT              or adding LRAT support to GRATgen could be worthwhile
proofs. Among the LRAT checkers, acl2-lrat is fastest,                future extensions.
followed by cake_lpr (LRAT checking), and coq-lrat.
Although cake_lpr (LRAT checking) is on average 1.3x
slower than acl2-lrat, it scales better on the mchess
problems and is actually much faster than acl2-lrat on
mchess18. We also observed that the GRAT toolchain


                                                                        9 There are 117 problems from the competition which are known
  8 The GRATgen tool supports parallel proof generation and was ran   to be unsatisﬁable; CaDiCaL proved unsatisﬁability for 102 problems
with 8 threads.                                                       within the 5000 seconds timeout.


                                                                                                                             123
180                                                                                                                           Yong Kiam Tan et al.


Table 2 Timings for PR benchmarks with conversion into LPR format. The “Total (LPR)” column sums the generation and checking times. The
timing for mchess19 is omitted because SaDiCaL timed out; timings for the Urquhart U.-s3-* benchmarks are omitted because they took a
negligible amount of time (< 1.0s total).

  Problem        SaDiCaL        DPR-trim        cake_lpr         Total      Problem       SaDiCaL       DPR-trim        cake_lpr         Total
                                                   (LPR)        (LPR)                                                      (LPR)        (LPR)
  hole20               1.0               0.5             0.7       2.2      U.-s4-b1             0.7           0.6               0.3       1.6
  hole30               6.9               2.4             6.1      15.4      U.-s4-b2             0.3           0.4               0.2       0.8
  hole40              31.3              10.0            25.1      66.3      U.-s4-b3             0.4           0.4               0.2       1.0
  hole50             101.7              35.5            87.9     225.1      U.-s4-b4             0.3           0.5               0.3       1.1
  mchess15            18.5               1.1             2.1      21.7      U.-s5-b1             2.5           0.9               1.3       4.7
  mchess16            21.7               1.2             2.1      25.0      U.-s5-b2             1.2           0.6               0.7       2.4
  mchess17            34.8               1.6             3.4      39.8      U.-s5-b3             3.2           1.5               2.0       6.8
  mchess18            59.8               2.3             5.2      67.2      U.-s5-b4             5.5           1.5               3.2      10.1


Table 3 Timings for PR benchmarks, ﬁrst converted to DRAT and subsequently converted into LRAT and GRAT formats. The “Total (LRAT)”
and “Total (GRAT)” columns sum the fastest generation and checking times for the LRAT and GRAT formats respectively. The “Total (LPR)”
column (in bold, fastest total time) is reproduced from Table 2 for ease of comparison. Fail(T) indicates a timeout. Timings for the mchess19 and
U.-s3-* benchmarks are omitted as in Table 2.

                                           cake_lpr                                                            Total       Total         Total
Prob.        pr2drat        DRAT-trim                     acl2-lrat      coq-lrat     GRATgen    GRATchk
                                             (LRAT)                                                           (LPR)      (LRAT)        (GRAT)
hole20             0.8            4.4            18.5             7.9        966.7        4.6        18.2        2.2           14.2       24.6
hole30             6.8           61.4           180.4           105.9       Fail(T)      24.5       647.9       15.4          181.0      686.1
hole40            32.4          460.0          1039.5           711.8       Fail(T)     101.3      Fail(T)      66.3         1235.5          -
hole50           108.6         2663.0          4697.4          3292.2       Fail(T)     337.2      Fail(T)     225.1         6165.5          -
mchess15           7.7           48.2            49.3            36.2       Fail(T)      48.4      2023.1       21.7          110.6     2097.7
mchess16           9.0           62.0            59.8            53.2       Fail(T)      55.2      2903.8       25.0          145.9     2989.6
mchess17          14.5          105.0            97.3            88.5       Fail(T)      86.1      7050.9       39.8          242.7     7186.3
mchess18          25.1          195.0           152.7           296.8       Fail(T)     135.9      Fail(T)      67.2          432.5          -
U.-s4-b1           0.5            2.5             3.6             3.3        135.7        3.6        44.8        1.6            7.0       49.7
U.-s4-b2           0.2            0.8             1.4             1.0         23.2        1.7          8.2       0.8            2.3       10.4
U.-s4-b3           0.3            1.3             2.0             1.5         49.2        2.4        16.2        1.0            3.5       19.3
U.-s4-b4           0.3            1.1             1.8             1.4         38.3        2.0        10.3        1.1            3.1       12.9
U.-s5-b1           4.2           13.6            16.7            12.5       3048.7       17.4       933.2        4.7           32.8      957.3
U.-s5-b2           1.7            5.6             7.3             5.5        614.7        7.7       189.6        2.4           13.9      200.2
U.-s5-b3           5.0           18.4            26.3            22.2       8750.5       21.1      2316.3        6.8           48.8     2345.6
U.-s5-b4          11.3           34.2            36.9            30.1       Fail(T)      40.6      Fail(T)      10.1           81.0          -


Table 4 A summary of the SAT Race 2019 benchmark results on 102 unsatisﬁability proofs generated by CaDiCaL. The N/A row counts problems
that timed out or failed in an earlier step of the respective toolchains.

                   Status            DRAT-trim          acl2-lrat        cake_lpr     coq-lrat     GRATgen      GRATchk
                   Success                      97              96             97           36          100            100
                   Timeout                       5               0              0           61            0              0
                   Other Failures                0               1              0            0            2              0
                   N/A                           0               5              5            5            0              2



6.3 Mutilated Chessboard RAT Microbenchmarks                                 results for lrat-check, an unverified LRAT proof checker
                                                                             implemented in C.
The following microbenchmark suite tests the LRAT check-
                                                                                The results in Table 5 show the impact of cake_lpr’s
ers on large mutilated chessboard problems (up to 100 by
                                                                             RAT optimizations (Section 5.3). Notably, cake_lpr scales
100) solved by pgbdd, a BDD-based SAT solver [8]. Unlike
                                                                             essentially linearly in the size of the proofs (up to ≈ 10
the previous benchmark suites, LRAT proofs are emitted
                                                                             million proof steps). As a result, cake_lpr is signiﬁcantly
directly by the solver so additional DRAT-trim conversion
                                                                             faster than acl2-lrat and coq-lrat on these RAT-heavy
is not needed. All tools were ran with a timeout of 10000
                                                                             proofs and it comes within a 5x factor of the unveriﬁed
seconds and all timings are reported in seconds (to one
                                                                             lrat-check tool.
d.p.). For additional scaling comparison, we also report


123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                                 181




Fig. 12 (Left) SAT Race 2019 proofs checked within a given (per instance) time limit for the LRAT proof checkers. (Right) SAT Race 2019 proofs
generated and checked within a given (per instance) time limit for the LRAT and GRAT toolchains.



Table 5 Timings for the RAT microbenchmark. The number of proof steps and ﬁle size of the proofs (in MB) are shown in the last two columns.
Fail(T) indicates a timeout.

                Problem          pgbdd       lrat-check        cake_lpr       acl2-lrat       coq-lrat       LRAT Steps     File Size
                mchess20            3.9                0.5             0.5          19.6         3405.2           125752           5
                mchess40           47.5                1.0             3.5         453.4         Fail(T)          769287          36
                mchess60          311.7                2.7            10.6        4885.2         Fail(T)         2300522         114
                mchess80         1164.1                4.8            22.6        Fail(T)        Fail(T)         5089457         259
                mchess100        3599.0                9.3            44.2        Fail(T)        Fail(T)         9506092         499



6.4 Erdős Discrepancy Properties                                              Table 6 Timings (wall-clock) for the EDP benchmark. Speedup is
                                                                              calculated relative to 1 thread.
The Erdős Discrepancy Problem (EDP) asks if, for every 𝐶 >
0 and inﬁnite ±1 sequence (𝑥1 , 𝑥2 , 𝑥3 , . . . ), there exists 𝑘, 𝑑                           Threads       cake_lpr      Speedup
                  𝑘
such that | 𝑖=1       𝑥𝑖·𝑑 | > 𝐶. Konev and Lisitsa [35] provided                                  1             3871.7          -
a SAT-solver aided proof of the EDP in the case 𝐶 = 2. We                                          2             1985.4        2.0
demonstrate the parallel scalability of compositional proof                                        4              998.2        3.9
                                                                                                   8              517.4        7.5
checking (Section 4) using cake_lpr’s compositional proof                                         16              273.2       14.2
checking option on a cube-and-conquer proof generated by                                          32              136.4       28.4
iGlucose, a version of Glucose 3.0 with support for iCNF                                          64               76.5       50.6
ﬁles, and the technique reported in Section 4.2. The technique                                    128              60.2       64.3
yields a 5226 line compositional top-level proof where each
line is justiﬁed by an underlying LRAT proof, see Fig. 8. The
underlying proofs consist of 20 million clause addition lines
in total and they vary widely in size, ranging from 88 bytes                  LRAT proofs dominate the overall proof checking time at
to 110 MB.                                                                    high levels of parallelism. A more advanced parallelization
    Proof steps are allocated evenly to parallel threads by their             scheme, e.g., with a scheduler, could further improve proof
index. For example, with two threads, the ﬁrst thread would                   checking performance.
check all odd-numbered proof steps by sequentially running
instances of cake_lpr to check the underlying proofs for
ranges (𝑖 0 , 𝑖 1 ), (𝑖 2 , 𝑖 3 ), . . . , while the second thread checks
all even-numbered proof steps for ranges (𝑖1 , 𝑖 2 ), (𝑖 3 , 𝑖 4 ), . . . ,   7 Related Work
and similarly for more parallel threads. Results are summa-                   Verified Proof Checking. There are several RAT-based
rized in Table 6 with wall-clock execution times reported                     veriﬁed proof checkers, in ACL2 [20], Coq [10], and
in seconds and relative speedup against a single thread. All                  Isabelle/HOL [39]; these veriﬁed checkers all use an unver-
values are rounded to one decimal place.                                      iﬁed preprocessing tool to add proof hints to DRAT proofs,
    The speedup is nearly linear for lower number of threads                  either DRAT-trim or GRATgen. Alternative preprocessing
(1–32) but drops oﬀ at 64 and 128 threads. This is likely                     tools are available, e.g., based on the recently proposed FRAT
due to the unbalanced nature of proof sizes, where large                      format [4]. The DRAT format is itself an extension of the

                                                                                                                                        123
182                                                                                                                  Yong Kiam Tan et al.


DRUP format [21]; the Coq checker is based on a predeces-         Our proof checker opens up the possibility of using a ver-
sor veriﬁed checker for the GRIT [11] format. The ACL2            iﬁed checker to help check and debug the implementation
checker can be eﬃciently and directly executed (without           of these new techniques. It also gives future SAT compe-
extraction) using imperative primitives native to the ACL2        titions the option of providing PR as the default (veriﬁed)
kernel [20]. However, the implementation of these features        proof system for participating solvers. Another interesting
in ACL2 itself must be trusted to trust the proof checking        direction is to add cake_lpr support for other proof for-
results [50], hence the yellow background in Table 1. SMT-        mats [5, 39]. In particular, this would allow users to build
Coq [2, 14] is another certiﬁcate-based checker for SAT and       compositional proofs that utilize diﬀerent underlying proof
SMT problems in Coq. Its resolution-based proof certiﬁcates       formats for separate parts of the proof.
can be checked natively using native computation extensions
of the Coq kernel.                                                Acknowledgements We thank the anonymous reviewers for their help-
   Veriﬁed checkers are available for other logics, such as       ful feedback on this article, as well as Jasmin Blanchette and the
the Veriﬁed TESC Veriﬁer for ﬁrst-order logic [3], Pastèque       TACAS’21 anonymous reviewers for their helpful feedback on the ear-
                                                                  lier conference version. We also thank Peter Lammich for help with
for the practical algebraic calculus [33], and various checkers   GRATgen and Stefan O’Rear for help with proﬁling CakeML programs.
for higher-order logics (and type theories) underlying proof
assistants [1, 47, 52].                                           Funding Open access funding provided by Chalmers University of
                                                                  Technology.
Applications. SAT solving is a key technology underlying
many software and hardware veriﬁcation domains [7, 30].
Certifying SAT results adds a layer of trust and is clearly a     Declarations
worthwhile endeavor. Solver-aided proofs of mathematical
                                                                  Conﬂict of interest The authors declare that they have no conﬂict of
results [23, 29, 35] are particularly interesting and challeng-   interest.
ing to certify because these often feature complicated SAT
encodings, custom (hand-crafted) proof steps, and enormous        Open Access This article is licensed under a Creative Commons
resulting proofs [29]. Our cake_lpr checker is designed to        Attribution 4.0 International License, which permits use, sharing, adap-
                                                                  tation, distribution and reproduction in any medium or format, as long
handle the latter two challenges eﬀectively. For the ﬁrst chal-   as you give appropriate credit to the original author(s) and the source,
lenge, the SAT encoding of mathematical problems can also         provide a link to the Creative Commons licence, and indicate if changes
be veriﬁed within proof assistants. This was done for the         were made. The images or other third party material in this article are
Boolean Pythagorean Triples problem building on the Coq           included in the article’s Creative Commons licence, unless indicated
                                                                  otherwise in a credit line to the material. If material is not included in
proof checker [12].                                               the article’s Creative Commons licence and your intended use is not
                                                                  permitted by statutory regulation or exceeds the permitted use, you will
Verified SAT Solving. An alternative to proof checking is to
                                                                  need to obtain permission directly from the copyright holder. To view a
verify the SAT solvers [16, 17, 43, 48]. This is a signiﬁcant     copy of this licence, visit http://creativecommons.org/licenses/by/4.0/.
undertaking but it would allow the pipeline of generating
and checking proofs to be entirely bypassed. Furthermore,
such veriﬁcation eﬀorts can yield new insights about key
invariants underlying SAT solving techniques compared to          References
prior pen-and-paper presentations, e.g., the 2WL invari-           1. Abrahamsson, O.: A veriﬁed proof checker for higher-order logic.
ant [17]. However, the performance of veriﬁed SAT solvers             J. Log. Algebraic Methods Program. 112, 100530 (2020). https://
are not yet competitive with modern (unveriﬁed) SAT solving           doi.org/10.1016/j.jlamp.2020.100530
                                                                   2. Armand, M., Faure, G., Grégoire, B., Keller, C., Théry, L., Werner,
technology [16, 17].                                                  B.: A modular integration of SAT/SMT solvers to Coq through
                                                                      proof witnesses. In: Jouannaud, J., Shao, Z. (eds.) CPP, LNCS,
                                                                      vol. 7086, pp. 135–150. Springer (2011). https://doi.org/10.1007/
                                                                      978-3-642-25379-9_12
8 Conclusion                                                       3. Baek, S.: A formally veriﬁed checker for ﬁrst-order proofs. In:
                                                                      Cohen, L., Kaliszyk, C. (eds.) ITP, LIPIcs, vol. 193, pp. 6:1–6:13.
This work presents the LPR proof format for veriﬁed check-            Schloss Dagstuhl - Leibniz-Zentrum für Informatik (2021). https://
ing of PR proofs and a compositional proof format for                 doi.org/10.4230/LIPIcs.ITP.2021.6
                                                                   4. Baek, S., Carneiro, M., Heule, M.J.H.: A ﬂexible proof format
separate (parallel) proof checking. It also demonstrates
                                                                      for SAT solver-elaborator communication. Log. Methods Comput.
the feasibility of using binary code extraction to verify             Sci. (2022). https://doi.org/10.46298/lmcs-18(2:3)2022
cake_lpr, a performant proof checker supporting both for-          5. Barnett, L.A., Biere, A.: Non-clausal redundancy properties. In:
mats down to its machine-code implementation. Given the               Platzer, A., Sutcliﬀe, G. (eds.) CADE, LNCS, vol. 12699, pp. 252–
                                                                      272. Springer (2021). https://doi.org/10.1007/978-3-030-79876-
strength of the PR proof system, there is ongoing research
                                                                      5_15
into the design of satisfaction-driven clause learning tech-       6. Becker, H., Zyuzin, N., Monat, R., Darulova, E., Myreen, M.O.,
niques [27, 28, 49] for SAT solvers based on PR clauses.              Fox, A.C.J.: A veriﬁed certiﬁcate checker for ﬁnite-precision


123
Veriﬁed Propagation Redundancy and Compositional UNSAT Checking in CakeML                                                                       183


    error bounds in Coq and HOL4. In: Bjørner, N., Gurﬁnkel, A.            23. Heule, M.J.H.: Schur number ﬁve. In: McIlraith, S.A., Weinberger,
    (eds.) FMCAD, pp. 1–10. IEEE (2018). https://doi.org/10.23919/             K.Q. (eds.) AAAI, pp. 6598–6606. AAAI Press (2018)
    FMCAD.2018.8603019                                                     24. Heule, M.J.H., Biere, A.: Compositional propositional proofs. In:
 7. Biere, A., Cimatti, A., Clarke, E.M., Zhu, Y.: Symbolic model              Davis, M., Fehnker, A., McIver, A., Voronkov, A. (eds.) LPAR,
    checking without BDDs. In: Cleaveland, R. (ed.) TACAS, LNCS,               LNCS, vol. 9450, pp. 444–459. Springer (2015). https://doi.org/
    vol. 1579, pp. 193–207. Springer (1999). https://doi.org/10.1007/          10.1007/978-3-662-48899-7_31
    3-540-49059-0_14                                                       25. Heule, M.J.H., Biere, A.: What a diﬀerence a variable makes. In:
 8. Bryant, R.E., Heule, M.J.H.: Generating extended resolution proofs         Beyer, D., Huisman, M. (eds.) TACAS, LNCS, vol. 10806, pp. 75–
    with a BDD-based SAT solver. In: Groote, J.F., Larsen, K.G. (eds.)         92. Springer (2018). https://doi.org/10.1007/978-3-319-89963-3_
    TACAS, LNCS, vol. 12651, pp. 76–93. Springer (2021). https://              5
    doi.org/10.1007/978-3-030-72016-2_5                                    26. Heule, M.J.H., Kiesl, B., Biere, A.: Clausal proofs of mutilated
 9. Cao, Q., Beringer, L., Gruetter, S., Dodds, J., Appel, A.W.: VST-          chessboards. In: Badger, J.M., Rozier, K.Y. (eds.) NFM, LNCS,
    Floyd: a separation logic tool to verify correctness of C programs.        vol. 11460, pp. 204–210. Springer (2019). https://doi.org/10.1007/
    J. Autom. Reason. 61(1–4), 367–422 (2018). https://doi.org/10.             978-3-030-20652-9_13
    1007/s10817-018-9457-5                                                 27. Heule, M.J.H., Kiesl, B., Biere, A.: Encoding redundancy for
10. Cruz-Filipe, L., Heule, M.J.H., Hunt Jr., W.A., Kaufmann, M.,              satisfaction-driven clause learning. In: Vojnar, T., Zhang, L. (eds.)
    Schneider-Kamp, P.: Eﬃcient certiﬁed RAT veriﬁcation. In:                  TACAS, LNCS, vol. 11427, pp. 41–58. Springer (2019). https://
    de Moura, L. (ed.) CADE, LNCS, vol. 10395, pp. 220–236.                    doi.org/10.1007/978-3-030-17462-0_3
    Springer (2017). https://doi.org/10.1007/978-3-319-63046-5_14          28. Heule, M.J.H., Kiesl, B., Biere, A.: Strong extension-free proof
11. Cruz-Filipe, L., Marques-Silva, J., Schneider-Kamp, P.: Eﬃcient            systems. J. Autom. Reason. 64(3), 533–554 (2020). https://doi.
    certiﬁed resolution proof checking. In: Legay, A., Margaria, T.            org/10.1007/s10817-019-09516-0
    (eds.) TACAS, LNCS, vol. 10205, pp. 118–135 (2017). https://doi.       29. Heule, M.J.H., Kullmann, O., Marek, V.W.: Solving and verifying
    org/10.1007/978-3-662-54577-5_7                                            the boolean Pythagorean triples problem via cube-and-conquer. In:
12. Cruz-Filipe, L., Marques-Silva, J., Schneider-Kamp, P.: Formally           Creignou, N., Berre, D.L., (eds.) SAT, LNCS, vol. 9710, pp. 228–
    verifying the solution to the Boolean Pythagorean triples problem.         245. Springer (2016). https://doi.org/10.1007/978-3-319-40970-
    J. Autom. Reason. 63(3), 695–722 (2019). https://doi.org/10.1007/          2_15
    s10817-018-9490-4                                                      30. Jackson, D., Schechter, I., Shlyakhter, I.: Alcoa: the Alloy con-
13. Eén, N., Sörensson, N.: An extensible SAT-solver. In: Giunchiglia,         straint analyzer. In: Ghezzi, C., Jazayeri, M., Wolf, A.L. (eds.)
    E., Tacchella, A. (eds.) SAT, LNCS, vol. 2919, pp. 502–518.                ICSE, pp. 730–733. ACM (2000). https://doi.org/10.1145/337180.
    Springer (2003). https://doi.org/10.1007/978-3-540-24605-3_37              337616
14. Ekici, B., Mebsout, A., Tinelli, C., Keller, C., Katz, G., Reynolds,   31. Järvisalo, M., Heule, M., Biere, A.: Inprocessing rules. In: Gram-
    A., Barrett, C.W.: SMTCoq: a plug-in for integrating SMT solvers           lich, B., Miller, D., Sattler, U. (eds.) IJCAR, LNCS, vol. 7364,
    into Coq. In: Majumdar, R., Kuncak, V. (eds.) CAV, LNCS, vol.              pp. 355–370. Springer (2012). https://doi.org/10.1007/978-3-642-
    10427, pp. 126–133. Springer (2017). https://doi.org/10.1007/978-          31365-3_28
    3-319-63390-9_7                                                        32. Kanabar, H.: Implementing and verifying a compiler optimisa-
15. Férée, H., Pohjola, J.Å., Kumar, R., Owens, S., Myreen, M.O., Ho,          tion for CakeML (2018). https://hrutvik.co.uk/assets/pdf/Hrutvik_
    S.: Program veriﬁcation in the presence of I/O - semantics, veriﬁed        Kanabar_dissertation.pdf. Computer Science Tripos, Part II Dis-
    library routines, and veriﬁed applications. In: Piskac, R., Rümmer,        sertation. University of Cambridge, UK
    P. (eds.) VSTTE, LNCS, vol. 11294, pp. 88–111. Springer (2018).        33. Kaufmann, D., Fleury, M., Biere, A.: The proof checkers Pacheck
    https://doi.org/10.1007/978-3-030-03592-1_6                                and Pastèque for the practical algebraic calculus. In: FMCAD, pp.
16. Fleury, M.: Optimizing a veriﬁed SAT solver. In: Badger, J.M.,             264–269. IEEE (2020). https://doi.org/10.34727/2020/isbn.978-3-
    Rozier, K.Y. (eds.) NFM, LNCS, vol. 11460, pp. 148–165. Springer           85448-042-6_34
    (2019). https://doi.org/10.1007/978-3-030-20652-9_10                   34. Kiesl, B., Rebola-Pardo, A., Heule, M.J.H.: Extended resolution
17. Fleury, M., Blanchette, J.C., Lammich, P.: A veriﬁed SAT solver            simulates DRAT. In: Galmiche, D., Schulz, S., Sebastiani, R. (eds.)
    with watched literals using Imperative HOL. In: Andronick, J.,             IJCAR, LNCS, vol. 10900, pp. 516–531. Springer (2018). https://
    Felty, A.P. (eds.) CPP, pp. 158–171. ACM (2018). https://doi.org/          doi.org/10.1007/978-3-319-94205-6_34
    10.1145/3167080                                                        35. Konev, B., Lisitsa, A.: Computer-aided proof of Erdős discrepancy
18. Ghale, M.K., Pattinson, D., Kumar, R., Norrish, M.: Veriﬁed cer-           properties. Artif. Intell. 224, 103–118 (2015). https://doi.org/10.
    tiﬁcate checking for counting votes. In: Piskac, R., Rümmer, P.            1016/j.artint.2015.03.004
    (eds.) VSTTE, LNCS, vol. 11294, pp. 69–87. Springer (2018).            36. Kumar, R., Mullen, E., Tatlock, Z., Myreen, M.O.: Software ver-
    https://doi.org/10.1007/978-3-030-03592-1_5                                iﬁcation with ITPs should use binary code extraction to reduce
19. Guéneau, A., Myreen, M.O., Kumar, R., Norrish, M.: Veriﬁed                 the TCB - (short paper). In: Avigad, J., Mahboubi, A. (eds.) ITP,
    characteristic formulae for CakeML. In: Yang, H. (ed.) ESOP,               LNCS, vol. 10895, pp. 362–369. Springer (2018). https://doi.org/
    LNCS, vol. 10201, pp. 584–610. Springer (2017). https://doi.org/           10.1007/978-3-319-94821-8_21
    10.1007/978-3-662-54434-1_22                                           37. Lammich, P.: Generating veriﬁed LLVM from Isabelle/HOL. In:
20. Heule, M., Hunt Jr., W.A., Kaufmann, M., Wetzler, N.: Eﬃcient,             Harrison, J., O’Leary, J., Tolmach, A. (eds.) ITP, LIPIcs, vol.
    veriﬁed checking of propositional proofs. In: Ayala-Rincón, M.,            141, pp. 22:1–22:19. Schloss Dagstuhl - Leibniz-Zentrum für
    Muñoz, C.A. (eds.) ITP, LNCS, vol. 10499, pp. 269–284. Springer            Informatik (2019). https://doi.org/10.4230/LIPIcs.ITP.2019.22
    (2017). https://doi.org/10.1007/978-3-319-66107-0_18                   38. Lammich, P.: Reﬁnement to Imperative HOL. J. Autom. Rea-
21. Heule, M., Hunt Jr., W.A., Wetzler, N.: Trimming while checking            son. 62(4), 481–503 (2019). https://doi.org/10.1007/s10817-017-
    clausal proofs. In: FMCAD, pp. 181–188. IEEE (2013). https://              9437-1
    doi.org/10.1109/FMCAD.2013.6679408                                     39. Lammich, P.: Eﬃcient veriﬁed (UN)SAT certiﬁcate checking. J.
22. Heule, M., Kullmann, O., Wieringa, S., Biere, A.: Cube and con-            Autom. Reason. 64(3), 513–532 (2020). https://doi.org/10.1007/
    quer: Guiding CDCL SAT solvers by lookaheads. In: Eder, K.,                s10817-019-09525-z
    Lourenço, J., Shehory, O. (eds.) HVC, LNCS, vol. 7261, pp. 50–         40. Leroy, X.: Formal veriﬁcation of a realistic compiler. Commun.
    65. Springer (2011). https://doi.org/10.1007/978-3-642-34188-5_            ACM 52(7), 107–115 (2009). https://doi.org/10.1145/1538788.
    8                                                                          1538814


                                                                                                                                       123
184                                                                                                                          Yong Kiam Tan et al.


41. Lind, J., Mihajlovic, N., Myreen, M.O.: Veriﬁed hash map and           50. Slind, K.: Trusted extensions of interactive theorem provers:
    buﬀered I/O libraries for CakeML. In: Trends in Functional                 Workshop summary (2010). https://www.cs.utexas.edu/users/
    Programming (TFP) (2021). Accepted for presentation                        kaufmann/itp-trusted-extensions-aug-2010/summary/summary.
42. Lööw, A., Kumar, R., Tan, Y.K., Myreen, M.O., Norrish, M.,                 pdf. [Online; accessed 7-September-2021]
    Abrahamsson, O., Fox, A.C.J.: Veriﬁed compilation on a ver-            51. Slind, K., Norrish, M.: A brief overview of HOL4. In: Mohamed,
    iﬁed processor. In: McKinley, K.S., Fisher, K. (eds.) PLDI,                O.A., Muñoz, C.A., Tahar, S. (eds.) TPHOLs, LNCS, vol. 5170,
    pp. 1041–1053. ACM (2019). https://doi.org/10.1145/3314221.                pp. 28–32. Springer (2008). https://doi.org/10.1007/978-3-540-
    3314622                                                                    71067-7_6
43. Maric, F.: Formal veriﬁcation of a modern SAT solver by shallow        52. Sozeau, M., Boulier, S., Forster, Y., Tabareau, N., Winterhalter,
    embedding into Isabelle/HOL. Theor. Comput. Sci. 411(50), 4333–            T.: Coq Coq correct! Veriﬁcation of type checking and erasure for
    4356 (2010). https://doi.org/10.1016/j.tcs.2010.09.014                     Coq. Coq. Proc. ACM Program. Lang. 4(POPL), 8:1-8:28 (2020).
44. Mullen, E., Pernsteiner, S., Wilcox, J.R., Tatlock, Z., Grossman,          https://doi.org/10.1145/3371076
    D.: Œuf: minimizing the Coq extraction TCB. In: Andronick, J.,         53. Tan, Y.K., Heule, M.J.H., Myreen, M.O.: cake_lpr: Veriﬁed prop-
    Felty, A.P. (eds.) CPP, pp. 172–185. ACM (2018). https://doi.org/          agation redundancy checking in CakeML. In: Groote, J.F., Larsen,
    10.1145/3167089                                                            K.G. (eds.) TACAS, LNCS, vol. 12652, pp. 223–241. Springer
45. Myreen, M.O.: The CakeML project’s quest for ever stronger cor-            (2021). https://doi.org/10.1007/978-3-030-72013-1_12
    rectness theorems (invited paper). In: Cohen, L., Kaliszyk, C.         54. Tan, Y.K., Myreen, M.O., Kumar, R., Fox, A.C.J., Owens, S.,
    (eds.) ITP, LIPIcs, vol. 193, pp. 1:1–1:10. Schloss Dagstuhl -             Norrish, M.: The veriﬁed CakeML compiler backend. J. Funct. Pro-
    Leibniz-Zentrum für Informatik (2021). https://doi.org/10.4230/            gram. 29, e2 (2019). https://doi.org/10.1017/S0956796818000229
    LIPIcs.ITP.2021.1                                                      55. Wetzler, N., Heule, M., Hunt Jr., W.A.: DRAT-trim: Eﬃcient check-
46. Myreen, M.O., Owens, S.: Proof-producing translation of higher-            ing and trimming using expressive clausal proofs. In: Sinz, C., Egly,
    order logic into pure and stateful ML. J. Funct. Program. 24(2–3),         U. (eds.) SAT, LNCS, vol. 8561, pp. 422–429. Springer (2014).
    284–315 (2014). https://doi.org/10.1017/S0956796813000282                  https://doi.org/10.1007/978-3-319-09284-3_31
47. Nipkow, T., Roßkopf, S.: Isabelle’s metalogic: Formalization and       56. Wieringa, S., Niemenmaa, M., Heljanko, K.: Tarmo: A framework
    proof checker. In: Platzer, A., Sutcliﬀe, G. (eds.) CADE, LNCS,            for parallelized bounded model checking. In: Brim, L., van de Pol,
    vol. 12699, pp. 93–110. Springer (2021). https://doi.org/10.1007/          J. (eds.) PDMC, EPTCS, vol. 14, pp. 62–76 (2009). https://doi.org/
    978-3-030-79876-5_6                                                        10.4204/EPTCS.14.5
48. Oe, D., Stump, A., Oliver, C., Clancy, K.: versat: A veriﬁed mod-
    ern SAT solver. In: Kuncak, V., Rybalchenko, A. (eds.) VMCAI,
                                                                               Publisher’s Note Springer Nature remains neutral with regard
    LNCS, vol. 7148, pp. 363–378. Springer (2012). https://doi.org/
    10.1007/978-3-642-27940-9_24                                               to jurisdictional claims in published maps and institutional
49. Reeves, J.E., Heule, M.J.H., Bryant, R.E.: Preprocessing of propa-         aﬃliations.
    gation redundant clauses. In: Blanchette, J., Kovács, L., Pattinson,
    D. (eds.) IJCAR, LNCS, vol. 13385, pp. 106–124. Springer (2022).
    https://doi.org/10.1007/978-3-031-10769-6_8




123
