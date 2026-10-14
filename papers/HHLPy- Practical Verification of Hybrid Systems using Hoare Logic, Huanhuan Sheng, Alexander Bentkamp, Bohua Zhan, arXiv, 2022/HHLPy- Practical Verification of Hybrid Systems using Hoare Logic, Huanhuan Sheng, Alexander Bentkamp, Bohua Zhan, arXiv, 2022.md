                                                HHLPy: Practical Verification of Hybrid Systems
                                                              using Hoare Logic

                                                           Huanhuan Sheng1,2 , Alexander Bentkamp1 , and Bohua Zhan1,2

                                           FM                                                                                         FM
                                                      1
                                                          State Key Laboratory of Computer Science, Institute of Software, Chinese
                                         Artifact                           Academy of Sciences, Beijing, China                    Artifact
                                         Evaluation                                                                                Evaluation
arXiv:2210.17163v2 [cs.LO] 21 Feb 2023




                                                                          {shenghh,bentkamp,bzhan}@ios.ac.cn
                                                                2
                                                                  University of Chinese Academy of Sciences, Beijing, China
                                         Available                                                                                     Reproducible



                                                          Abstract. We present a tool for verification of hybrid systems expressed
                                                          in the sequential fragment of HCSP (Hybrid Communicating Sequential
                                                          Processes). The tool permits annotating HCSP programs with pre- and
                                                          postconditions, invariants, and proof rules for reasoning about ordinary
                                                          differential equations. Verification conditions are generated from the an-
                                                          notations following the rules of a Hoare logic for hybrid systems. We
                                                          designed labeling and highlighting mechanisms to distinguish and visu-
                                                          alize different verification conditions. The tool is implemented in Python
                                                          and has a web-based user interface. We evaluated the effectiveness of the
                                                          tool on translations of Simulink/Stateflow models and on KeYmaera X
                                                          benchmarks.

                                                          Keywords: Hybrid systems · Hoare logic · Formal verification.


                                               1      Introduction
                                               Hybrid systems refer to systems that have both continuous and discrete be-
                                               haviors. They occur in diverse areas of science and engineering, ranging from
                                               transportation and spaceflight, to robots and medical devices. Hence, verifying
                                               that hybrid systems meet certain specifications is an important problem. Apart
                                               from methods such as monitoring and model checking, theorem proving is one
                                               of the major approaches to verifying hybrid systems.
                                                   There is a substantial amount of previous work on verification of hybrid
                                               systems based on theorem proving. One major framework is Platzer’s differ-
                                               ential dynamic logic (dL) [23, 25], and the associated KeYmaera/KeYmaera X
                                               prover [9, 26]. Recently, a Hoare logic has been introduced for dL and imple-
                                               mented within the Isabelle proof assistant [21]. We review these works in detail
                                               in Section 8 of this paper.
                                                   Another approach is to model hybrid systems using HCSP (Hybrid CSP)
                                               [13, 35], an extension of CSP (Communicating Sequential Processes) to include
                                               continuous evolution. Its semantics of continuous evolution is deterministic, so it
                                               can be used naturally for capturing Simulink/Stateflow models. A hybrid Hoare
                                               logic has been developed for HCSP, and is implemented in Isabelle [30]. However,
                                               practical application of the tool is complicated by its steep learning curve. To use
2        H. Sheng, A. Bentkamp et al.

this tool, the user need to be familiar with the Isabelle proof assistant, as well as
manually applying a set of Hoare logic rules which are themselves very complex.
This is in stark contrast to KeYmaera X, which allows users to verify hybrid
programs by choosing menu actions and offers highly specialized automation.
    This paper introduces HHLPy3 , a tool for verification of the sequential part
of HCSP with a friendly graphical user interface. Compared to [30], we simplify
the Hoare logic rules, and add more rules for reasoning about the behavior of
differential equations. These latter rules are closely related to that in dL, but due
to the semantic differences of HCSP, we adapted some of the rules and proved
our rules to be sound (Section 3).
    Our Hoare logic rules are in a sufficiently simple form that automatic verifi-
cation condition generation is possible. We design such a procedure to compute
verification conditions (VCs) from a given annotated HCSP program (Section 4).
We express VCs as a set of conditions, splitting up VCs that are conjunctions
as much as possible. We use labels to distinguish between different VCs, so that
users can choose solvers (currently either Z3 [19] or Wolfram Engine [31]) for
each VC individually and such choices are maintained through minor changes
on the code (Section 5).
    To visualize to the user where each VC originates from, a highlighting mech-
anism highlights the set of code fragments in the annotated program that con-
tributed to generating the VC (Section 6).
    We implemented the tool using Python and JavaScript and evaluated it on
Simulink/Stateflow models and on KeYmaera X benchmarks (Section 7). We
translated two Simulink/Stateflow models using the toolchain developed by Zou
et al. [36,37] and verified them in our tool. Due to differences in the semantics of
dL and HCSP, we translated each KeYmaera X benchmark by hand, trying to
maintain semantic equivalence as much as possible. In this way, we succeeded to
use our tool to solve most of the verification problems in the basic and nonlinear
KeYmaera X benchmarks.

2     Preliminaries
In this section, we present the sequential fragment of HCSP, with an informal
explanation of its semantics. We further give an overview of the existing toolchain
on translation of Simulink/Stateflow models into HCSP.

2.1    Sequential fragment of HCSP
Hybrid CSP (HCSP), introduced in [13, 35], is an extension of Hoare’s Com-
municating Sequential Processes to include continuous evolution. It can model
communicating processes running in parallel, where each process may have both
continuous and discrete behavior. In this paper, we focus on the sequential frag-
ment of HCSP, consisting of the following commands:
    S, T ::= skip | x := e | x := ∗ (B) | S; T | if B then S else T | S ++ T | S∗
             | hẋ = e & Di
3
    The tool is available at https://github.com/bzhan/mars/tree/master/hhlpy
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic        3

The program state is a mapping from variables to reals. skip leaves the state
unchanged. x := e assigns the value of expression e to variable x. x := ∗ (B) is
nondeterministic assignment of some value satisfying condition B to x. S; T and
if B then S else T are regular sequential composition and conditional. S ++ T
is a nondeterministic choice between S and T . S∗ runs S a nondeterministic
number of times (including zero).
    The ordinary differential equation (ODE) command hẋ = e & Di specifies
continuous evolution in HCSP. It makes the vector of variables x evolve accord-
ing to ODE ẋ = e until the domain D becomes false. If D is false from the start,
the ODE is skipped. In contrast to dL, where continuous evolution may stop at
any point within the specified domain, in HCSP it always deterministically con-
tinues up to the boundary. In this paper, we assume D is given by a polynomial
inequality of the form p(x) < 0, so it represents an open set in Rn .
    We assume in this paper that all expressions appearing in an HCSP program
(as well as in annotations to be discussed later) are polynomials, and hence
continuity conditions are trivially satisfied.
    For a formal treatment of semantics of HCSP (including communication and
parallel composition), we refer to Zhan et al. [33, Chapter 6].

2.2   Translation from Simulink/Stateflow
The HCSP language is located at the center of a toolchain that also includes
translation from Simulink/Stateflow models, simulation and code generation [2].
The original translation algorithms from Simulink [37] and Stateflow [36] pro-
duce HCSP programs that involve communication between parallel processes.
However, more recent methods by Xu et al. [32] and Guo et al. [11] produce
sequential HCSP programs. We use these translation methods for verification of
Simulink/Stateflow models in Section 7.


3     Proof Rules of Hoare Logic for Hybrid Systems
In this section, we present the Hoare logic that forms the basis of our verification
tool. The Hoare triple for partial correctness, written as {P }c{Q}, means starting
from a state satisfying assertion P , any terminating execution of c reaches a state
satisfying assertion Q. The Hoare rules for ordinary commands (except ODEs)
are standard and are presented in the Appendix A.
    Hence, we focus on the Hoare rules for ODEs. These rules are mostly adapted
from rules for dL, as given in [25,28]. Due to the difference in semantics between
HCSP and dL, several of the rules take on different forms. We do not aim to
present a minimal set of rules, instead providing users a wide range of choices.

3.1   Proof rules based on invariants
In order to state proof rules based on invariants of ODEs, we require an addi-
tional kind of judgments, called invariant triples.
4       H. Sheng, A. Bentkamp et al.

Definition 1 (Invariant Triple). Let P and Q be predicates on the variables
of an ODE ẋ = e. Let γ : [0, T ] → Rn be a solution of the ODE such that
γ(t) satisfies P for all t ∈ [0, T ] and such that γ(0) satisfies Q. If for all such
solutions γ, γ(t) satisfies Q for all t ∈ [0, T ], then we say that Q is an invariant
of ODE ẋ = e under domain P , written as

                                  JP Khẋ = eiJQK

Differential Weakening The differential weakening rule (dW) reduces a Hoare
triple goal to an invariant triple, incorporating the domain condition.

                      JDKhẋ = eiJIK ∂D ∧ I → Q
                                                      dW
                  {(D → I) ∧ (¬D → Q)}hẋ = e & Di{Q}

Here, D is the closure of D, and ∂D is the boundary set of D. Note that the rule
is in the form that allows us to derive a precondition from any postcondition.
The precondition (D → I)∧(¬D → Q) corresponds to the two cases for the state
before ODE: if the state satisfies domain D, then it should satisfy the invariant.
Otherwise it should satisfy the postcondition Q directly. Two special cases of
the rule, for I set to true and false, provide further intuition. They correspond
to cases where no invariant is needed, and where the starting state is known to
satisfy ¬D.
            ∂D → Q
                             dWT                                          dWF
     {¬D → Q}hẋ = e & Di{Q}                 {¬D ∧ Q}hẋ = e & Di{Q}

Proof (of the (dW) rule). Given starting state x, we divide into two cases based
on whether x satisfies domain D. If x satisfies D, then there exists a solution
γ : [0, T ] → Rn , such that γ(t) satisfies D for t ∈ [0, T ) and γ(T ) satisfies ¬D,
and we wish to show that γ(T ) satisfies Q. By the continuity of γ, we get that
γ(t) satisfies D for t ∈ [0, T ]. Moreover, since D → I holds in the precondition,
we get that γ(0) satisfies I as well. Then from JDKhẋ = eiJIK, we get that γ(t)
satisfies I for t ∈ [0, T ]. From ∂D ∧ I → Q and the fact that γ(T ) satisfies I and
∂D, we get that γ(T ) satisfies Q, as desired.
    If x does not satisfy D, then the ODE is not executed, and we wish to show
that x satisfies Q. Since ¬D → Q holds in the precondition, we get that x
satisfies Q, as desired.

Differential Invariant The differential invariant rule (dI) is essentially the
same as that in dL. It concludes invariants from computation of Lie derivatives.

                                  P → f˙ = 0
                                                  dI=
                              JP Khẋ = eiJf = 0K

Here f˙ denotes the Lie derivative of f under the differential equation ẋ = e.
The corresponding rules for inequality and disequality are as follows, where <
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic        5

denotes either > or ≥.

                    P → f˙ ≥ 0                 P → f˙ = 0
                                    dI<                         dI6=
                JP Khẋ = eiJf < 0K        JP Khẋ = eiJf 6= 0K

Differential Cut The differential cut rule (dC) inserts an intermediate invari-
ant to be proved, and afterwards permits the use of this invariant to show further
invariants. In contrast to dL, it is not possible to record previously proved in-
variants as conjuncts in the domain of ODE commands. Instead we place them
in the premise of the invariant triple. Indeed this is the primary motivation for
introducing the concept of invariant triples.

                   JP Khẋ = eiJQ1 K JP ∧ Q1 Khẋ = eiJQ2 K
                                                            dC
                             JP Khẋ = eiJQ1 ∧ Q2 K

    The (dC) rule can be used multiple times to show conjunction of more than
two invariants. For example, if we wish to show three invariants Q1 , Q2 , Q3
in that order, first apply the (dC) rule with Q1 and Q2 to obtain JP Khẋ =
eiJQ1 ∧ Q2 K, then apply the (dC) rule again to obtain the conclusion.
Differential Ghost The differential ghost rule (dG) adds new variables satis-
fying some differential equations to help prove the Hoare triple of the original
differential equations.

                 JDKhẋ = e, ẏ = f (x, y)iJIK ∂D ∧ I → Q
                                                          dG
                {(D → ∃y. I) ∧ (¬D → Q)}hẋ = e & Di{Q}

Here, y are fresh variables that do not occur in hẋ = e & Di or Q, and f (x, y)
satisfies the Lipschitz condition.
Barrier Certificate The barrier certificate rule (bc) concludes invariants from
the definition of barrier certificate.

                              P ∧ f = 0 → f˙ > 0
                                                  bc
                              JP Khẋ = eiJf < 0K

Darboux The Darboux rule (dbx) exploits properties of Darboux invariants,
which are inspired by Darboux polynomials. Darboux equality and inequality
rules are as follows.

                 P → f˙ = gf                  P → f˙ ≥ gf
                                  dbx=                         dbx<
              JP Khẋ = eiJf = 0K          JP Khẋ = eiJf < 0K

3.2   Solution Rule
The solution rule offers another way to conclude Hoare triples directly, inde-
pendent of using the (dW) or (dG) rule followed by proving invariants. In the
rule below, e is linear in x, and u(t, x) is the unique solution to the differential
6       H. Sheng, A. Bentkamp et al.

equation ẋ = e with symbolic initial value x (that is, du(t,x)
                                                           dt   = e(u(t, x)) and
u(0, x) = x). Let P 0 (x) denote the following predicate on the starting state x:
          ∀t > 0. (∀0 ≤ τ < t. D(u(τ, x))) ∧ ¬D(u(t, x)) → Q(u(t, x)).
The solution rule for Hoare triples (sln) is:
                                                                    sln
                   {(D → P 0 ) ∧ (¬D → Q)}hẋ = e & Di{Q}


4    Verification Condition Generation
The VC generation procedure operates on annotated sequential HCSP programs.
For ODEs, there are two kinds of annotations: ghost variable (gvar) and invariant
annotations (ode inv):
                           gvar ::= ghost z (ż = f (x, z))
                        ode inv ::= [I] | [I] {dbx g} | [I] {bc}

Here, ‘ghost z (ż = f (x, z))’ denotes a ghost variable z following the ODE
ż = f (x, z), where f must be linear in z to ensure global Lipschitz condition. The
annotation [I] denotes showing invariant I using the (dI) rule. The annotation
[I] {dbx g} denotes showing an invariant using the (dbx) rule, with g being the
optional cofactor. The annotation [I] {bc} denotes using the (bc) rule.
    The syntax for annotated sequential HCSP programs is:
      S, T ::= skip | x := e | x := ∗(B) | S; T | if B then S else T |
               S ++ T | S ∗ invariant [I1 ] . . . [In ] |
               hẋ = e & Di invariant gvar1 . . . gvark , ode inv1 . . . ode invn |
               hẋ = e & Di solution
The only addition to the syntax of HCSP is that each loop is followed by a
list of invariants I1 , . . . , In , and each ODE is either followed by a list of ghost
variable declarations and a list of invariant annotations, each of which specify
an invariant to be proved using one of (dI), (dbx), or (bc) rules, or followed by
the annotation “solution” to indicate that the (sln) rule is to be used.
    To generate the necessary VCs for a given Hoare triple, we devised a proce-
dure using weakest preconditions [3, 4]. To be able to refer to preconditions and
VCs individually, we consider sets of conditions instead of composing predicates
by ∧.
    Given a Hoare triple {P1 ∧ · · · ∧ Pm }S{Q1 ∧ · · · ∧ Qn } to verify, we define the
set of all VCs to be
 VC({P1 ∧ · · · ∧ Pm }S{Q1 ∧ · · · ∧ Qn }) =
  {P1 ∧ · · · ∧ Pm → R | R ∈ pre(S, {Q1 , . . . , Qn })} ∪                            (pre)
  {P̃1 ∧ · · · ∧ P̃m̃ → R | R ∈ vc(S, {Q1 , . . . , Qn })}                             (vc)

where P̃1 , . . . , P̃m̃ is the subset of the preconditions P1 , . . . , Pm whose variables
are never reassigned in S, and the functions pre and vc are defined below.
          HHLPy: Practical Verification of Hybrid Systems using Hoare Logic                    7

    Given an annotated program S and a set {Q1 , . . . , Qn } of postconditions,
we denote the set of derived preconditions as pre(S, {Q1 , . . . , Qn }), defined as
follows.

pre(S, {Q1 , . . . , Qn }) = pre(S, Q1 ) ∪ · · · ∪ pre(S, Qn )                 (pre-multi)
pre(skip, Q) = Q                                                                 (pre-skip)
pre(x := e, Q) = Q[e/x]                                                         (pre-assn)
pre(S; T , Q) = pre(S, pre(T , Q))                                                (pre-seq)
pre(if B1 then S1 else · · · if Bn−1 then Sn−1 else Sn , Q) =
  {¬(B1 ∨ · · · ∨ Bi−1 ) ∧ Bi → P | P ∈ pre(Si , Q), 1 ≤ i ≤ n − 1} ∪               (pre-if)
  {¬(B1 ∨ · · · ∨ Bn−1 ) → P | P ∈ pre(Sn , Q)}                                  (pre-else)
pre(S1 ++ · · · ++ Sn , Q) = pre(S1 , Q) ∪ · · · ∪ pre(Sn , Q)                (pre-choice)
pre(x := ∗ (B), Q) = B[y/x] → Q[y/x] for a fresh variable y                    (pre-nassn)
pre(S ∗ invariant [I1 ] . . . [In ], Q) = {Ij | 1 ≤ j ≤ n}                      (pre-loop)
pre(hẋ = e & Di invariant gvar1 . . . gvark , ode inv1 . . . ode invn , Q) =
  Pskip ∪ Pinit
pre(hẋ = e & Di solution) = Pskip ∪ Psln

where

 Pskip = {¬D → Q}                                                             (pre-dWG-skip)
 Pinit = {D → ∃z1 , . . . , zk . I1 ∧ · · · ∧ In } if k > 0                      (pre-dG-init)
 Pinit = {D → Ij , | 1 ≤ j ≤ n} otherwise                                       (pre-dW-init)
 Psln = {D → (∀t > 0. (∀0 ≤ τ < t. D(u(τ, x))) ∧
          ¬D(u(t, x)) → Q(u(t, x)))}                                                  (pre-sln)

where z1 , . . . , zk are the ghost variables provided in gvar1 . . . gvark , and I1 , . . . , In
are the invariants provided in ode inv1 , . . . , ode invn . If the user chooses the (sln)
rule, we verify that e is linear in x and compute the unique solution u(τ, x) to
the ODE with symbolic initial value x.
    Given an annotated program S and a set {Q1 . . . , Qn } of postconditions, we
denote the set of internal VCs as vc(S, {Q1 , . . . , Qn }), defined as follows.

vc(S, {Q1 , . . . , Qn }) = vc(S, Q1 ) ∪ · · · ∪ vc(S, Qn )                     (vc-multi)
vc(skip, Q) = ∅                                                                   (vc-skip)
vc(x := e, Q) = ∅                                                                (vc-assn)
vc(S; T , Q) = vc(S, pre(T , Q)) ∪ vc(T , Q)                                       (vc-seq)
vc(if B1 then S1 else if · · · else if Bn−1 then Sn−1 else Sn , Q) =
  vc(S1 , Q) ∪ · · · ∪ vc(Sn , Q)                                                   (vc-ite)
vc(S1 ++ · · · ++ Sn , Q) = vc(S1 , Q) ∪ · · · ∪ vc(Sn , Q)                    (vc-choice)
vc(x := ∗ (B), Q) = ∅                                                           (vc-nassn)
vc(S ∗ invariant [I1 ] . . . [In ], Q) =
  vc(S, {I1 , . . . , In }) ∪                                              (vc-loop-body)
  {(I1 ∧ · · · ∧ In ) → Q} ∪                                                (vc-loop-exit)
  {(I1 ∧ · · · ∧ In ) → P | P ∈ pre(S, {I1 , . . . , In })}            (vc-loop-maintain)
vc(hẋ = e & Di invariant gvar1 . . . gvarm , ode inv1 . . . ode invn , Q) = Cexec ∪ CdC
vc(hẋ = e & Di solution, Q) = ∅
8         H. Sheng, A. Bentkamp et al.

where we set Cexec = ∅ if the only invariant is false, or else

    Cexec = {I1 ∧ · · · ∧ In ∧ ∂D → Q}                                 (vc-dWG-exec)
    CdC = {I1 ∧ · · · ∧ Ij−1 → R | R ∈ vc(hẋ = e & Di, ode invj , Q),
                                   1 ≤ j ≤ n}                                (vc-dC)

Here, I1 , . . . , In are the invariants provided in ode inv1 , . . . , ode invn . If no in-
variants are specified, we set a single invariant I1 = true by default. We write
vc(hẋ = e & Di, ode invj , Q) for the VC generated from annotation ode invj ,
defined as follows.
    vc(hẋ = e & Di, [true], Q) = ∅                                              (vc-true)
    vc(hẋ = e & Di, [false], Q) = ∅                                            (vc-false)
    vc(hẋ = e & Di, [f = 0], Q) = {D → f˙ = 0}                                   (vc-dI1)
    vc(hẋ = e & Di, [f < 0], Q) = {D → f˙ ≥ 0}                                   (vc-dI2)
    vc(hẋ = e & Di, [f 6= 0], Q) = {D → f˙ = 0}                                  (vc-dI3)
    vc(hẋ = e & Di, [f = 0] {dbx g}, Q) = {D → f˙ = gf }                       (vc-dbx1)
    vc(hẋ = e & Di, [f < 0] {dbx g}, Q) = {D → f˙ ≥ gf }                       (vc-dbx2)
    vc(hẋ = e & Di, [f < 0] {bc}, Q) = {D ∧ f = 0 → f˙ > 0}                       (vc-bc)

All Lie derivatives are computed with respect to ẋ = e and the equations given
in gvar1 . . . gvarm . For the (dbx) rule, if no cofactor g is provided, we attempt
to compute the cofactor automatically. Specifically, in the case of an equality
invariant, this reduces to simplifying f˙/f into polynomial form. In the case of
an inequality invariant, we attempt to find a polynomial quotient of f˙ and f
with a non-negative remainder.
Theorem 1. A Hoare triple {P1 ∧ · · · ∧ Pm }T {Q1 ∧ · · · ∧ Qn } holds if all con-
ditions in VC({P1 ∧ · · · ∧ Pm }T {Q1 ∧ · · · ∧ Qn }) hold.
Proof. We give the full proof in Appendix B. In short, we proceed by structural
induction on T . The difficult case is when T is an ODE. If the ODE is annotated
to use the solution rule, we use the VC stemming from the precondition (pre-
sln). Otherwise, we employ the (dG) rule or the (dW) rule depending on if ghost
variables are specified. The VCs stemming from (pre-dWG-skip) and (pre-dW-init)
or (pre-dG-init) show that the rule (dW) or (dG) is applicable. The condition (vc-
dWG-exec) discharges the right premise of the (dW) or (dG) rule.
     For the left premise JDKhẋ = e, ẏ = f (x, y)iJI1 ∧ · · · ∧ Ik K, (without y if
using the (dW) rule), we repeatedly apply the (dC) rule to isolate each invariant
Ii . For each step JD ∧ I1 ∧ · · · ∧ Ii−1 Khẋ = e, ẏ = f (x, y)iJIi K, depending on the
rule specified in the annotation, we apply the (dI) rule, (dbx) rule or (bc) rule,
using the corresponding VCs as premises.                                                t
                                                                                        u


5      Labels
VCs generated by the procedure in Section 4 will be proved using Z3 or Wolfram
Engine. In this section, we introduce a labeling mechanism to store which solver
          HHLPy: Practical Verification of Hybrid Systems using Hoare Logic        9

is used for each VC, in a way that is robust to minor modifications of the program
or its annotations.
    As indicated in Section 4, the generation of a VC starts from a postcondition
or invariant and proceeds bottom up through the program. We call the post-
condition or invariant at the beginning of this process the conclusion assertion
of the VC. We associate each VC to its conclusion assertion. Labels are used to
distinguish between multiple VCs from the same conclusion assertion. They can
arise for the following reasons:

 – Loop and ODE invariants produce VCs for showing that they initially hold
   and for showing that they are maintained by the loop or ODE.
 – If-then-else and nondeterministic choice produce multiple preconditions, at
   least one for each branch.4
 – Each ODE produces preconditions for both the case when the domain D
   holds initially, and for when D does not hold.

   A label consists of two parts: a category label and a branch label. The cat-
egory label is either empty or one of “init”, “maintain”, “init all”. The branch
label is a list, separated by “.”, of either “skip”, “exec”, or n(b) where n is a
positive integer and b is a branch label itself. We write n instead of n() when
the inner branch label is empty.


Category Labels Category labels use “init” (“init all”) and “maintain” to
distinguish between VCs with loop or ODE invariants as conclusion assertions.
For loops, the VCs for showing the invariant holds initially are labeled “init”,
and the VCs that result from showing the invariant is maintained by the loop
are labeled “maintain” (when there are nested loops or ODEs in the loop body,
multiple VCs are computed in the loop body, this applies only to those with the
invariant as conclusion assertion).
    For an ODE, the VC coming from (pre-dW-init) (resp. (pre-dG-init)) are la-
beled “init” (resp. “init all”). The VCs coming from (vc-dC), for showing each
invariant is maintained during evolution, are labeled “maintain”.
    The category label is empty in all other cases.


Branch Labels Branch labels help to distinguish VCs generated by executing
different branches of programs.
    The positive integer n handles branches created by ‘if B then S1 else S2 ’ or
‘S1 ++ S2 ’. Each value of n (starting from 1) corresponds to one branch. Sequence
labels b.b are used for sequences of such commands. For example, the branches for
‘S1 ++ S2 ; S3 ++ S4 ’ have labels 1.1, 1.2, 2.1 and 2.2. Nested labels n(b) are used
for nested commands. For example, the branches for if B then S1 ++ S2 else S3
have labels 1(1), 1(2) and 2, corresponding to S1 , S2 and S3 , respectively.
4
    A large program consisting of multiple if-then-else commands can lead to an unde-
    sired blow up of the number of VCs. For example, a program constructed by ten
    if-then-else commands as sequential components results in more than 210 VCs.
10     H. Sheng, A. Bentkamp et al.

   The labels “skip” and “exec” are used for branches of the ODE. The branch
where the initial state does not satisfy domain D is labeled “skip”. The other
branch, where the ODE is executed, is labeled “exec”. They come from applying
the rules (vc-dWG-skip) and (vc-dWG-exec), respectively.

Example 1. This example illustrates assignments, nondeterministic choice, and
loops.
                       {x ≤ 0}
                          x := −x;
                          (x := x + 1 ++ x := x + 2)∗
                             invariant [x ≥ 0];
                          x := x + 1
                       {x ≥ 1}
The computation starts at postcondition x ≥ 1. Applying (pre-assn) and (vc-
loop-exit), we get the VC x ≥ 0 → x + 1 ≥ 1. Applying (pre-loop), the loop’s
precondition is x ≥ 0. The whole program’s precondition is −x ≥ 0 by applying
(pre-assn) again. The loop body yields the preconditions x + 1 ≥ 0 and x + 2 ≥ 0
by (pre-choice) and (pre-assn). Then we get x ≥ 0 → x + 1 ≥ 0 and x ≥ 0 →
x + 2 ≥ 0 by applying (vc-loop-maintain). The overall VCs and their labels are:

                       VC       Conclusion Assertion   Label
                 x ≤ 0 → −x ≥ 0     x ≥ 0 (inv)         init
                x≥0→x+1≥1          x ≥ 1 (post)          
                x≥0→x+1≥0           x ≥ 0 (inv)      maintain 1
                x≥0→x+2≥0           x ≥ 0 (inv)      maintain 2

With conclusion assertions and labels, we can store the solver (default Z3) for
each VC and reuse the solver despite of minor modifications of code. For example,
if we choose Wolfram Engine to prove x ≤ 0 → −x ≥ 0, “init: wolfram” will
be annotated after the invariant x ≥ 0. If we then change the second line from
x := −x into x := −2 ∗ x, resulting in a different VC x ≤ 0 → −2 ∗ x ≥ 0, the
solver of the VC is still Wolfram Engine.
Example 2. This example illustrates non-deterministic assignments and ODEs
(#4 of KeYmaera X’s basic benchmarks):

                   {x ≥ 0}
                     x := x + 1; t := ∗ (t ≥ 0);
                     hṫ = −1, ẋ = 2 & t > 0i invariant [x ≥ 1]
                   {x ≥ 1}

The computation of pre starts at postcondition x ≥ 1. By (pre-dWG-skip) and
(pre-dW-init), the ODE’s preconditions are ¬t > 0 → x ≥ 1 and t > 0 →
x ≥ 1. By (pre-nassn) and (pre-assn), the whole program’s preconditions are
t1 ≥ 0 → t1 > 0 → x ≥ 1 and t1 ≥ 0 → ¬t1 > 0 → x + 1 ≥ 1. The VCs
x ≥ 1 ∧ t = 0 → x ≥ 1 and t ≥ 0 → 2 ≥ 0 come from (vc-dWG-exec) and
(vc-dI2), respectively. The overall list of VCs is:
        HHLPy: Practical Verification of Hybrid Systems using Hoare Logic       11

                        VC                  Conclusion Assertion Label
        x ≥ 0 → t1 ≥ 0 → t1 > 0 → x + 1 ≥ 1     x ≥ 1 (inv)       init
       x ≥ 0 → t1 ≥ 0 → ¬t1 > 0 → x + 1 ≥ 1    x ≥ 1 (post)       skip
               x≥1∧t=0→x≥1                     x ≥ 1 (post)      exec
                   t≥0→2≥0                      x ≥ 1 (inv)     maintain


Example 3. Finally, we consider an example with multiple ghost variables (#18
of KeYmaera X’s basic benchmarks):

                {x ≥ 0}
                  t := ∗ (t ≥ 0); hẋ = x, ṫ = −1 & t > 0i
                  invariant ghost y (ẏ = −y) ghost z (ż = z/2)
                     [xy ≥ 0] [yz 2 = 1]
                {x ≥ 0}

                         VC                         Conclusion Assertion Label
  x ≥ 0 → t1 ≥ 0 → t1 > 0 → ∃y z. xy ≥ 0 ∧ yz 2 = 1      invariants      init all
         x ≥ 0 → t1 ≥ 0 → ¬t1 > 0 → x ≥ 0              x ≥ 0 (post)        skip
          xy ≥ 0 ∧ yz 2 = 1 ∧ t = 0 → x ≥ 0            x ≥ 0 (post)       exec
             t ≥ 0 → x · (−y) + xy ≥ 0                 xy ≥ 0 (inv)     maintain
 xy ≥ 0 → t ≥ 0 → yz(z/2) + (y(z/2) + (−y)z)z = 0      yz 2 = 1 (inv)   maintain

The first VC comes from (pre-dG-init). The remaining VCs are similar to Exam-
ple 2, except that there is one VC for maintaining each invariant. When verifying
the second invariant, the (dC) rule allows us to assume the first invariant.


6   Highlighting

In this section, we explain the highlighting mechanism we devised to help the user
understand how each VC is derived from the program. Essentially, when the user
hovers over a VC, we highlight all parts of the program that contribute to the
computation of the VC, including commands, assertions and domain constraints.
    We highlight any assertion that contributes to the VC. In particular, invari-
ants of an ODE that are already proved will be highlighted when proving the
next invariant because they are added as assumptions in (vc-dC). Preconditions
whose variables are never reassigned will be highlighted because they are added
as assumptions in (vc).
    Domain constraints of ODEs will be highlighted if they are used in the VC
(e.g. the domain constraint D in the VC generated by (vc-dWG-exec)).
    Atomic commands are highlighted if they are traversed during VC generation.
ODE commands are highlighted for VCs computed by (vc-dC) or (pre-sln). For if-
then-else and nondeterministic choice, only the branch that is actually traversed
during VC generation will be considered for highlighting.
    Fig. 1 and 2 show the highlighting for some the VCs from Examples 1 and 2.
12      H. Sheng, A. Bentkamp et al.

       {x ≤ 0}                                 {x ≤ 0}
         x := −x;                                x := −x;
         (x := x + 1 ++ x := x + 2)∗             (x := x + 1 ++ x := x + 2)∗
            invariant [x ≥ 0];                      invariant [x ≥ 0];
         x := x + 1                              x := x + 1
       {x ≥ 1}                                 {x ≥ 1}

          (a) VC labeled ‘init’           (b) VC for the postcondition (no label)

       {x ≤ 0}                                 {x ≤ 0}
         x := −x;                                x := −x;
         (x := x + 1 ++ x := x + 2)∗             (x := x + 1 ++ x := x + 2)∗
            invariant [x ≥ 0];                      invariant [x ≥ 0];
         x := x + 1                              x := x + 1
       {x ≥ 1}                                 {x ≥ 1}

       (c) VC labeled ‘maintain 1’             (d) VC labeled ‘maintain 2’

               Fig. 1: Highlighting for the four VCs in Example 1

       {x ≥ 0}                                  {x ≥ 0}
         x := x + 1; t := ∗(t ≥ 0);               x := x + 1; t := ∗(t ≥ 0);
         hṫ = −1, ẋ = 2 & t > 0i                hṫ = −1, ẋ = 2 & t > 0i
             invariant [x ≥ 1]                        invariant [x ≥ 1]
       {x ≥ 1}                                  {x ≥ 1}

          (a) VC labeled ‘skip’                 (b) VC labeled ‘maintain’

           Fig. 2: Highlighting for the two of the VCs in Example 2


7     Implementation and Evaluation

In this section, we present the implementation of HHLPy and evaluate it on
Simulink/Stateflow models and on KeYmaera X benchmarks. All verified exam-
ples are available online, coming with the tool.


7.1   Implementation

Fig. 3 shows the architecture of the tool. The user inputs HCSP programs and
annotations in the editor (the HCSP programs can also come from translation of
Simulink/Stateflow models). The core HHLPy engine then parses the input and
generates VCs. The user interface displays the VCs and allows users to choose
a solver for each VC. The solver will be invoked, with the results displayed to
the user interface. The backend of HHLPy is implemented in Python, and the
graphical user interface is implemented using JavaScript. A screenshot of the
user interface is shown in Fig. 4.
        HHLPy: Practical Verification of Hybrid Systems using Hoare Logic     13




                         Fig. 3: Architecture of HHLPy




Fig. 4: Screenshot of user interface. The left panel (1) shows a list of example
files. The middle panel (2) is the editor area, where user can edit the program
and add annotations either directly as text or by clicking on buttons. The right
panel (3) shows the VCs. When hovering over each VC, the relevant part of the
code is highlighted.


7.2   Evaluation on Simulink/Stateflow Models
To illustrate the use of our tool as part of an existing toolchain to verify cor-
rectness of Simulink/Stateflow models, we show two example models, one from
Simulink and one from Stateflow.

Cruise Control System The first example is a cruise control system of an
automotive vehicle [14]. The system stabilizes the speed of a vehicle around
some desired speed (15 m/s in our case) using a PI controller. The PI controller
adjusts the control force according to the difference between actual speed and
desired speed as well as its integral. The vehicle follows its physical dynamics.
The Simulink models are presented in Appendix C.
    We first applied the approach by Xu et al. [32] to translate the Simulink
models into an HCSP program. In the program, the controller and vehicle dy-
namics are combined into a single ODE. Given the initial speed v = 14 and
initial integral value I = 700 of the controller, which are close to the stable
point (v = 15, I = 750), we want to verify that the speed remains in the interval
[13.5, 16.5].
     14       H. Sheng, A. Bentkamp et al.

         To verify the Hoare triple, we annotated the ODE and loop with the invariant
     1.3 ∗ (I − 750)2 − 198 ∗ (I − 750) ∗ (v − 15) + 12192 ∗ (v − 15)2 ≤ 5542, and used
     (dI) rule to prove the ODE invariant. The invariant was derived following the
     standard theory for analyzing linear dynamical systems. The annotated HCSP
     program is illustrated below. The tool generated seven VCs, and Z3 can prove
     all of them.
1    pre [v == 14][I == 700];
2
3    t := 0;
4     tick := 0;
5    tt := 0;
6
7    {
8      {tt dot = 1, I dot = (15 − v) ∗ 40, v dot = ((15 − v) ∗ 600 + I − v ∗ 50) ∗ 0.001 & tt < 1}
9          invariant [1.3∗(I−750)ˆ2 − 198 ∗ (I−750)∗(v−15)+12192∗(v−15)ˆ2<=5542];
10     t := t + tt;
11      tick := tick + 1;
12     tt := 0;
13   }∗
14     invariant [1.3∗(I−750)ˆ2 − 198 ∗ (I−750)∗(v−15)+12192∗(v−15)ˆ2<=5542];
15   post [v >= 13.5][v <= 16.5];




     Sawtooth Wave The sawtooth wave is a Stateflow model generating a signal
     that alternates between increasing from 0 to 1 and decreasing from 1 to 0. It
     illustrates functionality in Stateflow such as hierarchical states and specifying
     ODEs in a state. The Stateflow model is presented in Appendix C. The signal
     x follows the ODE ẋ = y, with y switching between 1 and −1 per unit time. We
     want to verify that every time y switches, x is still between 0 and 1.
         We translated the Stateflow model into an HCSP program with the approach
     by Guo et al. [11] (code shown in Appendix C). To verify the program, the loop
     is annotated with four invariants (mostly having to do with the relationship
     between Stateflow locations and value of variable x), and the ODE is annotated
     with “solution”. A total of 62 VCs are generated and proved to be true by Z3.


     7.3     Evaluation on Benchmarks from KeYmaera X

     We also evaluated our tool on the basic and nonlinear benchmarks5 from KeY-
     maera X. We first translated the examples from dL to HCSP manually, trying
     to maintain semantic equivalence as much as possible. Due to the differences be-
     tween dL and HCSP, some examples can not be translated into HCSP programs.
     We annotated the programs with invariants and proof rules, mostly following the
     existing proofs in KeYmaera X.
         Given the annotations, HHLPy can verify 50 out of 60 examples in the basic
     benchmarks. In comparison, KeYmaera X solves 58 examples in the scripted
     mode (with detailed proof scripts), and 55 examples in the hints mode (with
     invariants annotated in the model) [17]. Of the ten unsolved examples, we are
     5
          The benchmarks are available at             https://github.com/LS-Lab/KeYmaeraX-
          projects/tree/master/benchmarks
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic        15

unable to translate eight of them to HCSP due to use of dL-specific constructs;
one is non-polynomial; and the last one makes use of invariants containing old
versions of variables. For the nonlinear benchmarks, HHLPy can verify 103 out
of 141 examples (compared to 108 in the scripted mode and 95 in the hints mode
for KeYmaera X [17]). Most of the unsolved ones are because we are unable to
find the invariants or their VCs cannot be proved in reasonable time by Z3 or
Wolfram Engine. Specifically, HHLPy can verify 9 examples which KeYmaera X
cannot verify in hints mode, while KeYmaera X can verify one example in hints
mode that HHLPy cannot verify. For this one example, we have not found the
invariants or specific rules, while KeYmaera X verifies it using a general ODE
rule.
    In the 153 examples solvable by HHLPy, the user only needs to add annota-
tions including loop/ODE invariants and ODE rules; just a couple of annotations
are needed per problem. For some problems, it is necessary to switch the backend
solver from the default Z3 to Wolfram Engine. After this, HHLPy can finish the
proof automatically. These experiments show that our tool can be used to solve
a wide range of examples from existing benchmarks with little manual effort.
Moreover, from the evaluation on the benchmarks we note that there are some
VCs that Z3 can solve but Wolfram Engine cannot, and vice versa, showing
the two solvers have complementary advantages. Generally speaking, Z3 han-
dles complex boolean structures better, while Wolfram Engine has advantages
in expressions containing many decimal numbers.


8   Related Work

Differential dynamic logic (dL) [23, 25] models hybrid systems by extending dy-
namic logic with continuous evolution. Reasoning rules about continuous evo-
lution include differential invariants, differential weakening, differential cut, and
differential ghosts. The rules are stated in the form of a uniform substitution
calculus [24], and they are complete [28]. Differential dynamic logic has been im-
plemented in KeYmaera [26] and KeYmaera X [9], whose user interfaces display
current subgoals in sequent calculus form and allow users to point and click to
construct proofs. The Bellerophon language allows users to perform proofs using
a tactic language [8]. The KeYmaera X tool produces proofs that can be inde-
pendently checked in Isabelle and Coq [1]. Liebrenz et al. developed a method
to translate Simulink models to dL and to verify them in KeYmaera X [16].
    Huerta y Munive and Struth represented dL programs using Kleene algebras,
and built verification components for hybrid systems in Isabelle/HOL [21, 22].
Foster et al. proposed Hoare logic rules and refinement calculi for hybrid pro-
grams [7] and extended the verification components in Isabelle/HOL [6], e.g.,
with syntax translation to obtain more user-friendly modeling and specifica-
tion languages and with proof automation using Eisbach. Huerta y Munive and
Struth also described formalization of solutions to affine and linear systems of
ODEs, with applications to verifying correctness of such systems [20].
16     H. Sheng, A. Bentkamp et al.

    Both of the above series of works focused on hybrid programs modeled using
dL. As discussed in Section 2 and 3, the semantics of continuous evolution is
different from that in dL; hence the proof rules need to be adapted, resulting
in particular to significant changes to differential weakening and differential cut
rules. In addition, compared to KeYmaera X in scripted mode, HHLPy can fin-
ish the verification automatically once programs are annotated with loop/ODE
invariants and ODE rules. Compared to KeYmaera X in hints mode, HHLPy
shows the VCs that cannot be proved, and highlights the set of code fragments
that contribute to generating the VCs, which help users to debug programs and
annotations.
    Goncharov and Neves introduced the HybCore language for hybrid compu-
tation [10]. Similarly to HCSP, HybCore defines deterministic semantics for do-
main constraints of ODE. The connection with Moggi’s work on computational
effects [18] potentially aids reasoning and verification in HybCore. However,
concrete verification methods remain future work.
    Compared to the previous version of hybrid Hoare logic [30], we focus only on
the sequential fragment of HCSP, resulting in much simpler rules that permits
automatic VC generation. On the other hand, we consider a full set of reasoning
rules for ODEs in parallel with dL, rather than only the invariant rule in [30].
    The design of our tool is similar to many other (semi-)automatic program
verification tools, such as Dafny [15], VeriFast [12], and Why3 [5], in that an-
notations are inserted into the program code. Our work differs from these tools
firstly in being able to handle hybrid programs. Moreover, we designed detailed
labeling and highlighting mechanisms to improve robustness of the annotations
and help visualization. These improvements are not limited to hybrid programs,
and can potentially be incorporated into other program verification tools as well.


9    Conclusion

We presented HHLPy, a tool for verification of hybrid programs written in the
sequential fragment of HCSP. The backend of the tool implements a Hoare logic
that includes rules for reasoning about continuous evolution adapted from dL.
We also designed labeling and highlighting mechanisms to improve user interac-
tion. We demonstrated the capabilities of the tool on HCSP programs translated
from Simulink/Stateflow models and on KeYmaera X benchmarks.
    We leave extension of the deduction system to handle communication, inter-
rupts, and parallel composition to future work. On the side of implementation
and applications, we intend to further extend the tool to be able to handle
non-polynomial ODEs and invariants and permit interactive proofs of VCs.

Acknowledgments. This work is supported by the National Natural Science Foun-
dation of China under grant No. 62032024, 62002351, and a Chinese Academy of
Sciences President’s International Fellowship for Postdoctoral Researchers under
grant No. 2021PT0015.
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic            17

References
 1. Bohrer, R., Rahli, V., Vukotic, I., Völp, M., Platzer, A.: Formally verified differ-
    ential dynamic logic. In: Bertot, Y., Vafeiadis, V. (eds.) Conference on Certified
    Programs and Proofs (CPP 2017). pp. 208–221. ACM (2017)
 2. Chen, M., Han, X., Tang, T., Wang, S., Yang, M., Zhan, N., Zhao, H., Zou, L.:
    MARS: A toolchain for modelling, analysis and verification of hybrid systems.
    In: Hinchey, M.G., Bowen, J.P., Olderog, E. (eds.) Provably Correct Systems, pp.
    39–58. NASA Monographs in Systems and Software Engineering, Springer (2017)
 3. Dijkstra, E.W.: Guarded commands, nondeterminacy and formal derivation of pro-
    grams. Commun. ACM 18(8), 453–457 (1975)
 4. Dijkstra, E.W.: A Discipline of Programming. Prentice-Hall (1976)
 5. Filliâtre, J., Paskevich, A.: Why3 - where programs meet provers. In: Felleisen, M.,
    Gardner, P. (eds.) European Symposium on Programming, (ESOP 2013). LNCS,
    vol. 7792, pp. 125–128. Springer (2013)
 6. Foster, S., Huerta y Munive, J.J., Gleirscher, M., Struth, G.: Hybrid systems veri-
    fication with Isabelle/HOL: Simpler syntax, better models, faster proofs. In: Huis-
    man, M., Pasareanu, C.S., Zhan, N. (eds.) Formal Methods (FM 2021). LNCS, vol.
    13047, pp. 367–386. Springer (2021)
 7. Foster, S., Huerta y Munive, J.J., Struth, G.: Differential Hoare logics and refine-
    ment calculi for hybrid systems with Isabelle/HOL. In: Fahrenberg, U., Jipsen, P.,
    Winter, M. (eds.) Relational and Algebraic Methods in Computer Science (RAM-
    iCS 2020). LNCS, vol. 12062, pp. 169–186. Springer (2020)
 8. Fulton, N., Mitsch, S., Bohrer, R., Platzer, A.: Bellerophon: Tactical theorem prov-
    ing for hybrid systems. In: Ayala-Rincón, M., Muñoz, C.A. (eds.) Interactive The-
    orem Proving (ITP 2017). LNCS, vol. 10499, pp. 207–224. Springer (2017)
 9. Fulton, N., Mitsch, S., Quesel, J., Völp, M., Platzer, A.: KeYmaera X: an axiomatic
    tactical theorem prover for hybrid systems. In: Felty, A.P., Middeldorp, A. (eds.)
    Conference on Automated Deduction (CADE-25). LNCS, vol. 9195, pp. 527–538.
    Springer (2015)
10. Goncharov, S., Neves, R.: An adequate while-language for hybrid computation. In:
    Komendantskaya, E. (ed.) International Symposium on Principles and Practice of
    Programming Languages (PPDP 2019). pp. 11:1–11:15. ACM (2019)
11. Guo, P., Zhan, B., Xu, X., Wang, S., Sun, W.: Translating a large subset of State-
    flow to hybrid CSP with code optimization. J. Syst. Archit. 130, 102665 (2022)
12. Jacobs, B., Smans, J., Philippaerts, P., Vogels, F., Penninckx, W., Piessens, F.:
    VeriFast: A powerful, sound, predictable, fast verifier for C and Java. In: Bobaru,
    M.G., Havelund, K., Holzmann, G.J., Joshi, R. (eds.) NASA Formal Methods
    (NFM 2011). LNCS, vol. 6617, pp. 41–55. Springer (2011)
13. Jifeng, H.: From CSP to Hybrid Systems, p. 171–189. Prentice Hall International
    (UK) Ltd., GBR (1994)
14. Kekatos, N.: Verifying a cruise control system using Simulink and SpaceEx. CoRR
    abs/2101.00102 (2021)
15. Leino, K.R.M.: Dafny: An automatic program verifier for functional correctness. In:
    Clarke, E.M., Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence,
    and Reasoning (LPAR-16). LNCS, vol. 6355, pp. 348–370. Springer (2010)
16. Liebrenz, T., Herber, P., Glesner, S.: Deductive verification of hybrid control sys-
    tems modeled in Simulink with KeYmaera X. In: Sun, J., Sun, M. (eds.) Inter-
    national Conference on Formal Engineering Methods (ICFEM 2018). LNCS, vol.
    11232, pp. 89–105. Springer (2018)
18      H. Sheng, A. Bentkamp et al.

17. Mitsch, S., Jin, X., Zhan, B., Wang, S., Zhan, N.: ARCH-COMP21 category report:
    Hybrid systems theorem proving. In: Frehse, G., Althoff, M. (eds.) International
    Workshop on Applied Verification of Continuous and Hybrid Systems (ARCH21).
    EPiC Series in Computing, vol. 80, pp. 120–132. EasyChair (2021)
18. Moggi, E.: Notions of computation and monads. Inf. Comput. 93(1), 55–92 (1991)
19. de Moura, L.M., Bjørner, N.S.: Z3: an efficient SMT solver. In: Ramakrishnan,
    C.R., Rehof, J. (eds.) Tools and Algorithms for the Construction and Analysis of
    Systems (TACAS 2008). LNCS, vol. 4963, pp. 337–340. Springer (2008)
20. Huerta y Munive, J.J.: Affine systems of ODEs in Isabelle/HOL for hybrid-program
    verification. In: de Boer, F.S., Cerone, A. (eds.) Software Engineering and Formal
    Methods (SEFM 2020). LNCS, vol. 12310, pp. 77–92. Springer (2020)
21. Huerta y Munive, J.J., Struth, G.: Verifying hybrid systems with modal Kleene
    algebra. In: Desharnais, J., Guttmann, W., Joosten, S. (eds.) Relational and Al-
    gebraic Methods in Computer Science (RAMiCS 2018). LNCS, vol. 11194, pp.
    225–243. Springer (2018)
22. Huerta y Munive, J.J., Struth, G.: Predicate transformer semantics for hybrid
    systems. J. Autom. Reason. 66(1), 93–139 (2022)
23. Platzer, A.: Differential dynamic logic for hybrid systems. J. Autom. Reason. 41(2),
    143–189 (2008)
24. Platzer, A.: A complete uniform substitution calculus for differential dynamic logic.
    J. Autom. Reason. 59(2), 219–265 (2017)
25. Platzer, A.: Logical Foundations of Cyber-Physical Systems. Springer (2018)
26. Platzer, A., Quesel, J.: KeYmaera: A hybrid theorem prover for hybrid systems
    (system description). In: Armando, A., Baumgartner, P., Dowek, G. (eds.) Interna-
    tional Joint Conference on Automated Reasoning (IJCAR 2008). LNCS, vol. 5195,
    pp. 171–178. Springer (2008)
27. Platzer, A., Tan, Y.K.: Differential equation axiomatization: The impressive power
    of differential ghosts. In: Dawar, A., Grädel, E. (eds.) Logic in Computer Science
    (LICS 2018). pp. 819–828. ACM (2018)
28. Platzer, A., Tan, Y.K.: Differential equation invariance axiomatization. J. ACM
    67(1), 6:1–6:66 (2020)
29. Prajna, S., Jadbabaie, A., Pappas, G.J.: A framework for worst-case and stochastic
    safety verification using barrier certificates. IEEE Trans. Autom. Control. 52(8),
    1415–1428 (2007)
30. Wang, S., Zhan, N., Zou, L.: An improved HHL prover: An interactive theorem
    prover for hybrid systems. In: Butler, M.J., Conchon, S., Zaı̈di, F. (eds.) Formal
    Methods and Software Engineering (ICFEM 2015). LNCS, vol. 9407, pp. 382–399.
    Springer (2015)
31. Wolfram Research, Inc.: Wolfram Engine, Version 13.1, https://www.wolfram.com/
    engine, Champaign, IL, 2022
32. Xu, X., Zhan, B., Wang, S., Talpin, J.P., Zhan, N.: A denotational semantics of
    Simulink with higher-order UTP. J. Log. Algebraic Methods Program. p. 100809
33. Zhan, N., Wang, S., Zhao, H.: Formal Verification of Simulink/Stateflow Diagrams.
    Springer (2017)
34. Zhao, H., Zeng, X., Chen, T., Liu, Z., Woodcock, J.: Learning safe neural network
    controllers with barrier certificates. Formal Aspects Comput. 33(3), 437–455 (2021)
35. Zhou, C., Wang, J., Ravn, A.P.: A formal description of hybrid systems. In: Hy-
    brid Systems III: Verification and Control, Proceedings of the DIMACS/SYCON
    Workshop on Verification and Control of Hybrid Systems. pp. 511–530 (1995)
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic                19

36. Zou, L., Zhan, N., Wang, S., Fränzle, M.: Formal verification of Simulink/Stateflow
    diagrams. In: Finkbeiner, B., Pu, G., Zhang, L. (eds.) Automated Technology for
    Verification and Analysis (ATVA 2015). LNCS, vol. 9364, pp. 464–481. Springer
    (2015)
37. Zou, L., Zhan, N., Wang, S., Fränzle, M., Qin, S.: Verifying Simulink diagrams
    via a Hybrid Hoare Logic prover. In: Ernst, R., Sokolsky, O. (eds.) International
    Conference on Embedded Software, (EMSOFT 2013). pp. 9:1–9:10. IEEE (2013)


A     More on the Proof Rules
In this section, we provide more details on the proof rules.

A.1    Proof Rules for Other Commands
The proof rules for commands other than the ODE are given in Fig. 5.


                                                           {P1 }c1 {Q} {P2 }c2 {Q}
                skip                           assign                                   ichoice
 {P }skip{P }            {P [e/x]}x := e{P }                   {P1 ∧ P2 }c1 ++ c2 {Q}
                                                               {P }c1 {Q} {Q}c2 {R}
                                        nondet-assign                                   seq
    {B[y/x] → Q[y/x]}x := ∗(B){Q}                                   {P }c1 ; c2 {R}
                                {P1 }c1 {Q} {P2 }c2 {Q}
                                                                            ite
                 {(B → P1 ) ∧ (¬B → P2 )}if B then c1 else c2 {Q}
                 {I}c{I}              P0 → P    {P }c{Q} Q → Q0
                             loop                                       conseq
                {I}c ∗ {I}                      {P 0 }c{Q0 }


                  Fig. 5: Hoare rules for the non-ODE commands




A.2    Example for the (dW) Rule
We give some examples of applying the (dW) rule with different invariants, such
as the trivial invariants true and false or the non-trivial invariant x − y = 1.
Example 4. In this example, the precondition guarantees that the ODE starts
inside the domain D. The Hoare triple is:
                             {x < 5}hẋ = 1 & x < 5i{x = 5}
As the boundary of domain D implies the postcondition, no invariant is needed
(set I = true by default). From the postcondition x = 5, we obtain precondition
¬x < 5 → x = 5 and VC x = 5 → x = 5. So the VCs are:
                               x < 5 → ¬x < 5 → x = 5
                                    x=5→x=5
20      H. Sheng, A. Bentkamp et al.

Example 5. In this example, the precondition guarantees that the ODE starts
outside the domain D. The Hoare triple is:

                         {x > 10}hẋ = 1 & x < 5i{x > 8}

Here we set invariant to be false. From the postcondition x > 8, we obtain
precondition ¬x < 5 ∧ x > 8 and no VCs from the ODE. The overall VCs are:
                             x > 10 → ¬x < 5 ∧ x > 8

Example 6. Now consider a case where the starting position may or may not lie
within the domain D. The Hoare triple is:

                     {x < 6}hẋ = 1 & x < 5i{x ≥ 5 ∧ x < 6}

No invariant is needed (I = true is set by default). From the postcondition, we
obtain the precondition ¬x < 5 → x ≥ 5 ∧ x < 6, and the VC x = 5 → x ≥
5 ∧ x < 6. So the overall VCs are:
                         x < 6 → ¬x < 5 → x ≥ 5 ∧ x < 6
                              x=5→x≥5∧x<6
Example 7. Now we consider an example where a non-trivial invariant must be
introduced. The Hoare triple is:

                  {x = 0 ∧ y = 0}hẋ = 1, ẏ = 1 & x < 5i{y = 5}

We set the invariant to be x − y = 0, requiring to show

                         Jx ≤ 5Khẋ = 1, ẏ = 1iJx − y = 0K

We get the VC x = 5 ∧ x − y = 0 → y = 5 and the precondition (x < 5 →
x − y = 0) ∧ (¬x < 5 → y = 5).

A.3    Example and Proof for the (dI) Rule
We give an example showing the use of the (dI) rule.
Example 8 (Example 7 continued). In this example, we continue with the invari-
ant triple we get:

                         Jx ≤ 5Khẋ = 1, ẏ = 1iJx − y = 0K
    The Lie derivative of x − y is ẋ − ẏ = 1 − 1 = 0. So the premise of the (dI)
rule is x ≤ 5 → 0 = 0.
Proof (of the (dI) rule). We consider each of the rules in turn.
Rule dI= Consider a solution γ : [0, T ] → Rn of the ODE, satisfying the condi-
   tion that γ(t) satisfies P for all t ∈ [0, T ]. Then, the derivative of f (γ(t)) is
   0 for all t ∈ [0, T ]. This shows that f (γ(t)) is constant within this interval.
   If furthermore f (γ(0)) = 0, then we get f (γ(T )) = 0, as desired.
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic         21

Rule dI< Similar to before, except now the derivative of f (γ(t)) is greater than
   or equal to 0 for all t ∈ [0, T ], so f (γ(t)) is a non-decreasing function of t
   within this interval. If furthermore f (γ(0)) < 0, then we get f (γ(T )) < 0,
   as desired.
Rule dI6= Similar to before, we get that the derivative of f (γ(t)) is 0 for all t ∈
   [0, T ]. This shows that f (γ(t)) is constant within this interval. If furthermore
   f (γ(0)) 6= 0, then we get f (γ(T )) 6= 0, as desired.


A.4    Example and Proof for the (dC) Rule

Example 9. In this example, we insert an intermediate invariant to help prove
the final invariant. The invariant triple is:

                       Jy ≤ 1Khẋ = y, ẏ = 1iJy > 0 ∧ x > 0K

Using the (dC) rule, the two premises are:

                           Jy ≤ 1Khẋ = y, ẏ = 1iJy > 0K

                       Jy ≤ 1 ∧ y > 0Khẋ = y, ẏ = 1iJx > 0K
Both the two premises can be proved by using the (dI) rule.

Proof (of the (dC) rule). Consider a solution γ : [0, T ] → Rn of the ODE,
satisfying the condition that γ(t) satisfies P for all t ∈ [0, T ], and γ(0) satisfies
Q1 ∧ Q2 . We wish to show γ(t) satisfies Q1 ∧ Q2 for all t ∈ [0, T ]. By the first
premise, we get γ(t) satisfies Q1 for all t ∈ [0, T ]. Then by the second premise,
γ(t) satisfies Q1 ∧ Q2 for all t ∈ [0, T ].


A.5    Example and Proof for the (dG) Rule

Example 10. In this example, the Hoare triple is:

                  {x > 0 ∧ t = 0}hẋ = x, ṫ = 1 & t < 10i{x > 0}

Using the (dG) rule, we introduce a ghost variable y with the differential equation
ẏ = − y2 and set the invariant for the new differential equations to be xy 2 = 1.
Then the new goal is:
                                            y
                     Jt < 10Khẋ = x, ẏ = − , ṫ = 1iJxy 2 = 1K
                                            2
We get the VC t = 10 ∧ xy 2 = 1 → x > 0 and the precondition (t < 10 →
∃y.xy 2 = 1) ∧ (¬t < 10 → x > 0).

Proof (of the (dG) rule). Given starting state x0 , we distinguish two cases based
on whether x0 satisfies D.
22      H. Sheng, A. Bentkamp et al.

 1. If x0 satisfies D, then there exists a solution γ : [0, T ] → Rn of the ODE
    hẋ = ei with initial condition x(0) = x0 , such that γ(t) satisfies D for
    t ∈ [0, T ) and γ(T ) satisfies ¬D. We wish to show that γ(T ) satisfies Q. Since
    D → ∃y.I holds in the precondition and x0 satisfies D, using r to denote a
    witness of y, we get that (x0 , r) satisfies I. With f (x, y) satisfying Lipschitz
    condition, let ψ : [0, T ] → R denote the solution of ODE hẏ = f (x, y)i
    with initial value r. Given that y are fresh variables and do not limit the
    duration of the solutions of x, we get that (γ, ψ) is the solution of the ODE
    hẋ = e, ẏ = f (x, y)i with initial condition (x0 , r). Then from JDKhẋ =
    e, ẏ = f (x, y)iJIK, we get that (γ(t), ψ(t)) satisfies I for t ∈ [0, T ]. From
    ∂D ∧ I → Q and (γ(T ), ψ(T )) satisfies I and ∂D, we get that (γ(T ), ψ(T ))
    satisfies Q. Since y does not occur in Q, we get that γ(T ) satisfies Q, as
    desired.
 2. If x0 does not satisfy D, the proof is similar to the one for the (dW) rule.


A.6    Example and Proof for the Barrier Certificate Rule

Example 11. In this example, we use the (bc) rule to prove the following invari-
ant triple:
                       Jt ≤ 10Khẋ = x3 + x4 iJx3 > 5K
Then the premise of the (bc) rule is

                        t ≤ 10 ∧ x3 = 5 → 3x2 (x3 + x4 ) > 0

Proof (of the (bc) rule). The proof is by contradiction. Consider a solution γ :
[0, T ] → Rn of the ODE, satisfying the condition that γ(t) satisfies P for all
t ∈ [0, T ], and γ(0) satisfies f ≥ 0. Assume there exists t0 ∈ [0, T ] such that
f (γ(t0 )) < 0. According to the proof of strict barrier certificate [29] in [34], we
get that there exists tsup ∈ [0, t0 ) satisfying f (γ(tsup )) = 0 and the Lie derivative
of f at tsup is non-positive. However, according to the premise, f˙ > 0 when f = 0,
which leads to a contradiction. Therefore, there cannot exist t0 ∈ [0, T ] such that
f (γ(t0 )) < 0, i.e. for all t ∈ [0, T ], f (γ(t0 )) ≥ 0.
    The proof is similar when considering the case where the invariant is f > 0.


A.7    Example and Proof for the Darboux Rule

Example 12. In this example, we use the (dbx= ) rule. The invariant triple is:

              Jt ≤ 1Khẋ = 5x2 + 3x, ż = 5zx + 3z, ṫ = 1iJx + z = 0K

Then, using the (dbx= ) rule with g = 5x + 3, we obtain the following premise of
the (dbx= ) rule:

                 t ≤ 1 → 5x2 + 3x + 5zx + 3z = (5x + 3)(x + z)
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic              23

Example 13. In this example, we use (dbx< ) rule. The invariant triple is:

                          Jt ≤ 1Khẋ = −x + 1, ṫ = 1iJx > 0K

Then, by using the (dbx< ) rule with which g = −1, we obtain the following
premise of the (dbx< ) rule:

                                 t ≤ 1 → −x + 1 ≥ −x

Proof (of Darboux rule). We consider each rule in turn.

Rule (dbx= ) Consider a solution γ : [0, T ] → Rn to the ODE, satisfying the
   condition that γ(t) satisfies P for all t ∈ [0, T ], and γ(0) satisfies f = 0.
   We wish to show that f (γ(t)) = 0 for all t ∈ [0, T ]. According to [27], given
   f˙ = gf , f = 0 stays invariant along the (analytic) solution to the ODE.
   Therefore, γ(t) satisfies f = 0 for all t ∈ [0, T ].
Rule (dbx< ) This rule can be derived by (dI), (dC), (dG) rule according to [27].

A.8    Example and Proof for the Solution Rule
Example 14. We illustrate rule (sln) with the following example:

                   {x = 0 ∧ y = 0}hẋ = 1, ẏ = x & x < 2i{y = 2}

The solution u(τ, x0 , y0 ) is given by (τ +x0 , 21 τ 2 +x0 t+y0 ). Hence D(u(τ, x0 , y0 ))
is τ + x0 < 2, and P 0 (x) is
                                                                1 2
       ∀t > 0. (∀0 ≤ τ < t. τ + x < 2) ∧ ¬(t + x < 2) →           t + xt + y = 2
                                                                2
The two premises ∀0 ≤ τ < t. τ + x < 2 and ¬(t + x < 2) of the implication are
together equivalent to t + x = 2. Hence, under the assumption of x < 2 (so that
t > 0 ∧ t + x = 2 has a unique solution), the predicate P 0 reduces to
                             1
                               (2 − x)2 + x(2 − x) + y = 2
                             2
So the precondition we derive from the solution rule is (x < 2 → 12 (2 − x)2 +
x(2 − x) + y = 2) ∧ (¬x < 2 → y = 2). Since x = 0 ∧ y = 0 implies this condition,
we prove the Hoare triple.

Proof (of solution rule). Given starting state x0 , we distinguish two cases based
on whether x0 satisfies domain D.
 1. If x0 satisfies D, then there exists a solution γ : [0, T ] → Rn of the ODE
    ẋ = e with initial state x0 , such that γ(τ ) satisfies D for τ ∈ [0, T ) and
    γ(T ) satisfies ¬D, and we wish to show that γ(T ) satisfies Q. Since D → P 0
    holds in the precondition, we get that x0 satisfies P 0 :

           ∀t > 0. (∀0 ≤ τ < t. D(u(τ, x0 ))) ∧ ¬D(u(t, x0 )) → Q(u(t, x0 )).
24       H. Sheng, A. Bentkamp et al.

     Then let t = T. We get:

                ∀0 ≤ τ < T. D(u(τ, x0 )) ∧ ¬D(u(T, x0 )) → Q(u(T, x0 )).

     Next, since u is the unique solution to the differential equation ẋ = e, we
     get that γ(τ ) = u(τ, x0 ) for all 0 ≤ τ ≤ T . Then we get:

                      ∀0 ≤ τ < T. D(γ(τ )) ∧ ¬D(γ(T )) → Q(γ(T )).

    From the fact that γ(τ ) satisfies D for τ ∈ [0, T ) and γ(T ) satisfies ¬D, we
    get γ(T ) satisfies Q, as desired.
 2. If x does not satisfy D, then the ODE is not executed, and we wish to show
    that x satisfies Q. Since ¬D → Q holds in the precondition, x satisfies Q,
    as desired.


B     Proof of Soundness of the Verification Condition
      Generation

Theorem 1. A Hoare triple {P1 ∧· · ·∧Pm }T {Q1 ∧· · ·∧Qn } holds if all conditions
in VC({P1 ∧ · · · ∧ Pm }T {Q1 ∧ · · · ∧ Qn }) hold.

Proof. We proceed by structural induction on T . We assume an initial state in
which P1 , . . . , Pm hold. We must show that after executing T on this state, if T
terminates, Q1 , . . . , Qn hold.
    The predicates P̃1 , . . . , P̃m̃ in (vc) are the subset of the preconditions P1 , . . . ,
Pm whose variables are never reassigned in T . They hold in the initial state by
assumption and since their variables never change, they hold in all states in the
course of the program T . Thus, for the purposes of this proof, we can assume
that P̃1 , . . . , P̃m0 always hold. Therefore, we can also assume that the elements
of vc(T , {Q1 , . . . , Qn }) always hold.
    If T is any command except loop or ODE, the correctness of the Hoare triple
is easy to see using the induction hypotheses and the VCs emerging via (pre) from
(pre-skip), (pre-assn), (pre-seq), (pre-if), (pre-else), (pre-choice), and (pre-nassn).
    If T is a loop S∗ with invariants I1 , . . . , In , we proceed as follows. Since
pre(T , Q1 , . . . , Qn ) = {I1 , . . . In } by (pre-loop), we have P1 ∧ · · · ∧ Pm → Ii ∈
VC({P1 , . . . , Pm }T {Q1 , . . . , Qn }) (pre) for each Ii . Thus, all Ii hold in the initial
state. The induction hypothesis for S, in conjunction with (vc-loop-body) and
(vc-loop-maintain), imply {I1 , . . . , In }S{I1 , . . . , In }. Hence, the Ii not only hold
in the initial state, but still after executing S arbitrarily often. Finally, by (vc-
loop-exit), Q1 , . . . , Qn hold in the final state.
    If T is a an ODE hẋ = e & Di with invariants I1 , . . . , Ik , we proceed as
follows.
    If the ODE is annotated to use the solution rule, we apply it using the VC
stemming from the precondition (pre-sln), and we are done.
    Otherwise, invariants have been specified, or the default invariant I1 = true
has been set. If additionally ghost variables are specified, we employ the (dG)
         HHLPy: Practical Verification of Hybrid Systems using Hoare Logic               25

rule; if no ghost variables are specified we employ the (dW) rule. The VCs stem-
ming from (pre-dWG-skip) and (pre-dW-init) or (pre-dG-init) show that the rule
(dW) or (dG) is applicable to our desired Hoare triple {P1 , . . . , Pm }T {Q1 , . . . , Qn }.
The condition (vc-dWG-exec) discharges the right premise of the (dW) or (dG)
rule. It remains the left premise

                       JDKhẋ = e, ẏ = f (x, y)iJI1 ∧ · · · ∧ Ik K

(possibly without y in the case of the (dW) rule)
   Next, we repeatedly apply the (dC) rule to isolate each invariant Ii . Then it
remains to show

                    JD ∧ I1 ∧ · · · ∧ Ii−1 Khẋ = e, ẏ = f (x, y)iJIi K

    We distinguish the different rules that could be in the annotation:

 – If the user did not specify a rule and Ii is either true or false, what we need
   to show is obvious because true and false are always invariants.
 – dI: We apply the (dI) rule. Its premise is justified by (vc-dI1), (vc-dI2), or
   (vc-dI3).
 – dbx: We apply the (dbx) rule. Its premise is justified by (vc-dbx1) or (vc-
   dbx2).
 – bc: We apply the (bc) rule. Its premise is justified by (vc-bc).              t
                                                                                 u


C     Simulink/Stateflow Models

C.1    Model for the Cruise Control System Example

Simulink models for the cruise control system are shown in Fig. 6, 7, and 8.




                 Fig. 6: Simulink Model of Cruise Control System.
26   H. Sheng, A. Bentkamp et al.




               Fig. 7: Simulink Model of Vehicle Dynamics.




                 Fig. 8: Simulink Model of PI Controller.




                Fig. 9: Stateflow Model of Sawtooth Wave.
                HHLPy: Practical Verification of Hybrid Systems using Hoare Logic   27

     C.2      Model and Code for the Sawtooth Wave Example

     The Stateflow model of the sawtooth wave example is shown in Fig. 9.
         Fig. 10 shows the HCSP code that is automatically translated from the State-
     flow diagram for the sawtooth example, together with annotations of pre- and
     postconditions, invariants, and ODE proof rules used to verify the property that
     x remains in the interval [0, 1] for this model.


1    pre [true ];
2
3      Chart All A := 1;
4      Chart All B := 2;
5      Chart All := 0;
6      x := 1;
7      Chart st := Chart All;
8      t := 1;
9      Chart All st := Chart All A;
10     y := 1;
11
12     {
13       Chart ret := 0;
14        if (Chart All st == Chart All A) {
15          Chart All A done := 0;
16          if (t >= 1) {
17            t := 0;
18            if (Chart All st == Chart All A) {
19              Chart All st := Chart All B;
20              y := −1;
21              Chart All A done := 1;
22            }
23          }
24          Chart ret := Chart All A done;
25       } else if (Chart All st == Chart All B) {
26          Chart All B done := 0;
27          if (t >= 1) {
28            t := 0;
29            if (Chart All st == Chart All B) {
30              Chart All st := Chart All A;
31              y := 1;
32              Chart All B done := 1;
33            }
34          }
35          Chart ret := Chart All B done;
36       }
37          {x dot = y, t dot = 1 & t < 1} solution;
38     }∗
39     invariant [Chart All st == Chart All A −> x == 1]
40                [ Chart All st == Chart All B −> x == 0]
41                [ Chart All st == Chart All A || Chart All st == Chart All B]
42                [ t == 1];
43
44   post [x >= 0][x <= 1];



     Fig. 10: HCSP code translated from the Stateflow diagram for the sawtooth
     example, with annotations.
