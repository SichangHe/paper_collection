                                                                CTL+FO Verification as Constraint Solving

                                                         Tewodros A. Beyene                                 Marc Brockschmidt                     Andrey Rybalchenko
                                                          Technische Universität                               Microsoft Research                    Microsoft Research
                                                           München, Germany                                     Cambridge, UK                         Cambridge, UK
arXiv:1406.3988v3 [cs.LO] 21 Jun 2014




                                        ABSTRACT                                                                             (where for all possible secret input values, the output should
                                        Expressing program correctness often requires relating pro-                          be the same). The logic CTL+FO offers a natural specifi-
                                        gram data throughout (different branches of) an execution.                           cation mechanism for such properties, allowing to freely mix
                                        Such properties can be represented using CTL+FO, a logic                             temporal and first-order quantification. First-order quantifi-
                                        that allows mixing temporal and first-order quantification.                          cation makes it possible to specify variables dependent on
                                        Verifying that a program satisfies a CTL+FO property is a                            the current system state, and temporal quantifiers allow to
                                        challenging problem that requires both temporal and data                             relate this data to system states reached at a later point.
                                        reasoning. Temporal quantifiers require discovery of invari-                            While CTL+FO and similar logics have been identified as
                                        ants and ranking functions, while first-order quantifiers de-                        a specification language before, no fully automatic method
                                        mand instantiation techniques. In this paper, we present                             to check CTL+FO properties on infinite-state systems was
                                        a constraint-based method for proving CTL+FO proper-                                 developed. Hence, the current state of the art is to either
                                        ties automatically. Our method makes the interplay be-                               produce verification tools specific to small subclasses of prop-
                                        tween the temporal and first-order quantification explicit in                        erties, or using error-prone program modifications that ex-
                                        a constraint encoding that combines recursion and existen-                           plicitly introduce and initialize ghost variables, which are
                                        tial quantification. By integrating this constraint encoding                         then used in (standard) CTL specifications.
                                        with an off-the-shelf solver we obtain an automatic verifier                            In this paper, we present a fully automatic procedure to
                                        for CTL+FO.                                                                          transform a CTL+FO verification problem into a system
                                                                                                                             of existentially quantified recursive Horn clauses. Such sys-
                                                                                                                             tems can be solved by leveraging recent advances in con-
                                        Categories and Subject Descriptors                                                   straint solving [3], allowing to blend first-order and tempo-
                                        D.2.4 [Software Engineering]: Software/Program Verifi-                               ral reasoning. Our method benefits from the simplicity of
                                        cation; F.3.1 [Logics and Meanings of Programs]: Spec-                               the proposed proof rule and the ability to leverage on-going
                                        ifying and Verifying and Reasoning about Programs                                    advances in Horn constraint solving.

                                        General Terms                                                                        Related Work.
                                                                                                                                Verification of CTL+FO and its decidability and com-
                                        Verification, Theory                                                                 plexity have been studied (under various names) in the past.
                                                                                                                             Bohn et al. [5] presented the first model-checking algorithm.
                                        Keywords                                                                             Predicates partitioning a possibly infinite state space are
                                                                                                                             deduced syntactically from the checked property, and rep-
                                        Model Checking, Software Verification, Temporal Logic
                                                                                                                             resented symbolically by propositional variables. This al-
                                                                                                                             lows to leverage the efficiency of standard BDD-based model
                                        1.     INTRODUCTION                                                                  checking techniques, but the algorithm fails when the needed
                                           In specifying the correct behaviour of systems, relating                          partition of the state space is not syntactically derivable
                                        data at various stages of a computation is often crucial. Ex-                        from the property.
                                        amples include program termination [7] (where the value of                              Working on finite-state systems, Hallé et al. [10], Patthak
                                        a rank function should be decreasing over time), correctness                         et al. [15] and Rensink [16] discuss a number of different
                                        of reactive systems [13] (where each incoming request should                         techniques for quantified CTL formulas. In these works, the
                                        be handled in a certain timeframe), and information flow [11]                        finiteness of the data domain is exploited to instantiate quan-
                                                                                                                             tified variables, thus reducing the model checking problem
                                                                                                                             for quantified CTL to standard CTL model checking.
                                                                                                                                Hodkinson et al. [13] study the decidability of CTL+FO
                                        Permission to make digital or hard copies of all or part of this work for            and some fragments on infinite state systems. They show the
                                        personal or classroom use is granted without fee provided that copies are            general undecidability of the problem, but also identify cer-
                                        not made or distributed for profit or commercial advantage and that copies           tain decidable fragments. Most notably, they show that by
                                        bear this notice and the full citation on the first page. To copy otherwise, to
                                        republish, to post on servers or to redistribute to lists, requires prior specific
                                                                                                                             restricting first order quantifiers to state formulas and only
                                        permission and/or a fee.                                                             applying temporal quantifiers to formulas with at most one
                                        SPIN ’14, July 21Ű23, 2014, San Jose, CA, USA                                       free variable, a decidable fragment can be obtained. Finally,
                                        Copyright 2014 ACM 978-1-4503-2452-6/14/07 ...$15.00.
Da Costa et al. [8] study the complexity of checking prop-               ables. The refinement loop collects a global constraint that
erties over propositional Kripke structures, also providing              declaratively determines which witnesses can be chosen. The
an overview of related decidability and complexity results.              chosen witnesses are used to replace existential quantifica-
In temporal epistemic logic, Belardinelli et al. [1] show that           tion, and then the resulting universally quantified clauses
checking FO-CTLK on a certain subclass of infinite systems               are passed to a solver over decidable theories, e.g., HSF [9]
can be reduced to finite systems. In contrast, our method                or µZ [12]. Such a solver either finds a solution, i.e., a model
directly deals with quantification over infinite domains.                for uninterpreted relations constrained by the clauses, or re-
                                                                         turns a counterexample, which is a resolution tree (or DAG)
2.    PRELIMINARIES                                                      representing a contradiction. Ehsf turns the counterexam-
                                                                         ple into an additional constraint on the set of witness can-
Programs.                                                                didates, and continues with the next iteration of the refine-
   We model programs as transition systems. A program P                  ment loop.
consists of a tuple of program variables v, an initial condition            For the existential clause above, Ehsf introduces a wit-
init(v), and a transition relation next (v, v ′ ). A state is a val-     ness/Skolem relation sk over variables x and y, i.e., x ≥
uation of v. A computation π is a maximal sequence of states             0 ∧ sk (x, y) → x ≥ y ∧ rank (x, y). In addition, since for each
s1 , s2 , . . . such that init(s1 ) and for each pair of consecutive     x such that x ≥ 0 holds we need a value y, we require that
states (s, s′ ) we have next (s, s′ ). The set of computations of        such x is in the domain of the Skolem relation using an ad-
P starting in s is denoted by ΠP (s).                                    ditional clause x ≥ 0 → ∃y : sk (x, y). In the Ehsf approach,
                                                                         the search space of a Skolem relation sk (x, y) is restricted by
CTL+FO Syntax and Semantics.
                                                                         a template function Templ(sk )(x, y). To conclude this ex-
  The following definitions are standard, see e.g. [5, 14].
                                                                         ample, we note that one possible solution returned by Ehsf
  Let T be a first order theory and |=T denote its satis-
                                                                         is the Skolem relation sk (x, y) = (y ≤ x − 1).
faction relation that we use to describe sets and relations
over program states. Let c range over assertions in T and x
range over variables. A CTL+FO formula ϕ is defined by                   3. CONSTRAINT GENERATION
the following grammar using the notion of a path formula φ.                 In this section we present our algorithm Gen for gen-
                                                                         erating constraints that characterize the satisfaction of a
      ϕ ::= ∀x : ϕ | ∃x : ϕ | c | ϕ ∧ ϕ | ϕ ∨ ϕ | A φ | E φ              CTL+FO formula. We also consider its complexity and
      φ ::= Xϕ | Gϕ | ϕU ϕ                                               correctness and present an example.
                                                                            See Figure 1. Gen performs a top-down, recursive de-
As usual, we define F ϕ = (trueU ϕ). The satisfaction rela-              scent through the syntax tree of the given CTL+FO for-
tion P |= ϕ holds if and only if for each s such that init(s)            mula. It introduces auxiliary predicates and generates a se-
we have P, s |= ϕ. We define P, s |= ϕ as follows using an               quence of implication and well-foundedness constraints over
auxiliary satisfaction relation P, π |= φ. Note that d ranges            these predicates. We use “,” to represent the concatenation
over values from the corresponding domain.                               operator on sequences of constraints. At each level of recur-
P, s |= ∀x : ϕ iff for all d holds P, s |= ϕ[d/x]                        sion, Gen takes as input a CTL+FO formula ϕ0 , a tuple
                                                                         of variables v0 that are considered to be in scope and define
P, s |= ∃x : ϕ iff exists d such that P, s |= ϕ[d/x]
                                                                         a state, assertions init(v0 ) and next (v0 , v0′ ) that describe a
P, s |= c       iff s |=T c                                              set of states and a transition relation, respectively. We as-
P, s |= ϕ1 ∧ ϕ2 iff P, s |= ϕ1 and P, s |= ϕ2                            sume that variables bound by first-order quantifiers in ϕ0
P, s |= ϕ1 ∨ ϕ2 iff P, s |= ϕ1 or P, s |= ϕ2                             do not shadow other variables. To generate constraints for
                                                                         checking if P = (v, init(v), next (v, v ′ )) satisfies ϕ we exe-
P, s |= A φ     iff for all π ∈ ΠP (s) holds P, π |= φ                   cute Gen(ϕ, v, init(v), next (v, v ′ )).
P, s |= E φ     iff exists π ∈ ΠP (s) such that P, π |= φ
P, π |= Xϕ      iff π = s1 , s2 , . . . and P, s2 |= ϕ                   Handling First-Order Quantification.
P, π |= Gϕ      iff π = s1 , s2 , . . . for all i ≥ 1 holds P, si |= ϕ      When ϕ0 is obtained from some ϕ1 by universally quan-
                                                                         tifying over x, we directly descend into ϕ1 after adding
P, π |= ϕ1 U ϕ2 iff π = s1 , s2 , . . . and exists j ≥ 1 such that       x to the scope. Hence, the recursive call to Gen uses
                    P, sj |= ϕ2 and P, si |= ϕ1 for 1 ≤ i ≤ j            v1 = (v0 , x). Since init(v0 ) defines a set of states over
                                                                         v1 in which x ranges over arbitrary values, the application
Quantified Horn Constraints.                                             Gen(ϕ1 , v1 , init(v0 ), . . . ) implicitly requires that ϕ1 holds
  Our method uses the Ehsf [3] solver for forall-exists Horn             for arbitrary x. Since the value of x is arbitrary but fixed
constraints and well-foundedness. We omit the syntax and                 within ϕ1 , we require that the transition relation considered
semantics of constraints solved by Ehsf, see [3] for details.            by the recursive calls does not modify x and thus extend
Instead, we consider an example:                                         next to next (v0 , v0′ ) ∧ x′ = x in the last argument.
                                                                            When ϕ0 is obtained from some ϕ1 by existentially quan-
       x ≥ 0 → ∃y : x ≥ y ∧ rank (x, y),           wf (rank ).
                                                                         tifying over x, we use an auxiliary predicate aux that implic-
These constraints are an assertion over the interpretation of            itly serves as witness for x. A first constraint connects the
the “query symbol” rank (the predicate wf is not a query                 set of states init(v0 ) on which ϕ0 needs to hold with aux (v1 ),
symbol, but requires well-foundedness). A solution maps                  which describes the states on which ϕ1 needs to hold. We
query symbols into constraints. The example has a solution               require that for every state s allowed by init(v0 ), a choice
that maps rank (x, y) to the constraint (x ≥ 0 ∧ y ≤ x − 1).             of x exists such that the extension of s with x is allowed by
  Ehsf resolves clauses like the above using a CEGAR                     aux (v1 ). Then, the recursive call Gen(ϕ1 , v1 , aux (v1 ), . . . )
scheme to discover witnesses for existentially quantified vari-          generates constraints that keep track of satisfaction of ϕ1 on
                                                                      able in general. In practice however, the used solver often
  Gen(ϕ0 , v0 , init(v0 ), next (v0 , v0′ )) =                        succeeds in finding a solution (cf. Sect. 4). We formalize
   match ϕ0 with                                                      the correctness of Gen in the following theorem.
    | ∀x : ϕ1 ⇒                                                          Theorem 1. For a given program P with init(v) and
      let v1 = (v0 , x) in                                            next (v, v ′ ) over v and a CTL+FO formula ϕ the application
      Gen(ϕ1 , v1 , init(v0 ), next (v0 , v0′ ) ∧ x′ = x)             Gen(ϕ, v, init(v), next (v, v ′ )) computes a constraint that is
    | ∃x : ϕ1 ⇒                                                       satisfiable if and only if P |= ϕ.
      let v1 = (v0 , x) in                                               Proof. (sketch) We omit the full proof here for
      let aux = fresh symbol of arity |v1 | in                        space reasons. We proceed by structural induction, as
      init(v0 ) → ∃x : aux (v1 ),                                     the constraint generation of the algorithm Gen. For-
      Gen(ϕ1 , v1 , aux (v1 ), next (v0 , v0′ ) ∧ x′ = x)             mally, we prove that the constraints generated by
                                                                      Gen(ϕ0 , v0 , init(v0 ), next (v0 , v0′ )) have a solution if and only
    |c⇒                                                               if the program P = (v0 , init(v0 ), next (v0 , v0′ )) satisfies ϕ0 .
      init(v0 ) → c                                                   The base case, i.e., ϕ0 is an assertion c from our background
    | EF ϕ1 ⇒                                                         theory T , is trivial.
      let inv , aux = fresh symbols of arity |v0 | in                    As example for an induction step, we consider ϕ0 = ∃x :
      let rank = fresh symbol of arity |v0 | + |v0 | in               ϕ1 . To prove soundness, we assume that the generated con-
                                                                      straints have a solution. For the predicate aux , this solution
      init(v0 ) → inv (v0 ),
                                                                      is a relation Saux that satisfies all constraints generated for
      inv(v0 ) ∧ ¬aux (v0 ) → ∃v0′ : next (v0 , v0′ ) ∧ inv (v0′ )    aux . For each s with init(s), we choose xs such that (s, xs ) ∈
                                         ∧ rank (v0 , v0′ ),          Saux . As we require init(v0 ) → ∃x : aux (v0 , x), this element
      wf (rank ),                                                     is well-defined. We now apply the induction hypothesis for
      Gen(ϕ1 , v0 , aux (v0 ), next (v0 , v0′ ))                      P ′ = ((v0 , x), aux (v0 , x), next (v0 , v0′ )∧x′ = x) and ϕ1 . Then
                                                                      for all s with init(s), we have P ′ , (s, xs ) |= ϕ1 , and as P ′ is
Figure 1:    Constraint generation rules for FO                       not changing x by construction, also P ′ , (s, xs ) |= ϕ1 [xs /x].
quantification, assertions, and existential/eventually                From this, P, s |= ϕ0 directly follows.
quantification.                                                          For completeness, we proceed analogously. If P, ϕ0 |=
                                                                      holds, then a suitable instantiation xs of x can be chosen for
                                                                      each s with init(s), and thus we can construct a solution for
arbitrary x allowed by aux (v1 ). Thus, aux (v1 ) serves as a         aux (v0 , x) from init(v0 ).
restriction of the choices allowed for x.
                                                                      Example.
Handling Temporal Quantification.                                       We illustrate Gen (see Figure 1) on a simple example. We
   We use a deductive proof system for CTL [14] and con-              consider a property that the value stored in a register v can
sider its proof rules from the perspective of constraint gen-         grow without bound on some computation.
eration.
   When ϕ0 is a background theory assertion, i.e., does not                                 ∀x : v = x → EF (v > x)
use path quantification, Gen produces a constraint that re-
quires ϕ0 to hold on every initial state.                             This property can be useful for providing evidence that a
   When ϕ0 requires that there is a path on which ϕ1 even-            program is actually vulnerable to a denial of service attack.
tually holds, then Gen uses an auxiliary predicate aux (v0 )          Let init(v) and next (v, v ′ ) describe a program over a single
to describe those states in which ϕ1 holds. Gen applies               variable v.
a combination of inductive reasoning together with well-                We apply Gen on the property and the program and ob-
foundedness to show that aux (v0 ) is eventually reached from         tain the following application trace (here, we treat → as
the initial states. The induction hypothesis is represented           expected, as its left-hand side is a background theory atom).
as inv (v0 ) and is required to hold for every initial state and
                                                                       Gen(∀x : v = x → EF (v > x),v,         init(v),    next(v, v′ ))
when aux (v0 ) is not reached yet. Then, the well-foundedness
                                                                       Gen(v = x → EF (v > x),         (v, x),init(v),    next(v, v′ ) ∧ x′ = x)
condition wf , which requires that it is not possible to come
back into the induction hypothesis forever, ensures that               Gen(v = x → aux (v, x),         (v, x),init(v),    next(v, v′ ) ∧ x′ = x)
eventually we reach a “base case” in which aux (v0 ) holds.            Gen(EF (v > x),                 (v, x),aux (v, x),next(v, v′ ) ∧ x′ = x)
Hence, eventually ϕ1 holds on some computations. Note
that the induction hypothesis inv (v0 ), the well-founded rela-       This trace yields the following constraints.
tion rank (v0 , v0′ ), and the predicate aux (v0 ) are left for the   init(v) → (v = x → aux (v))
solver to be discovered.
   See [2] for the remaining rules that describe the full set of      aux (v) → inv (v, x)
CTL temporal quantifiers.                                             inv (v, x) ∧ ¬(v > x) → ∃v ′ , x′ : next (v, x, v ′ , x′ ) ∧ x′ = x
                                                                                                          ∧ inv (v ′, x′ ) ∧ rank (v, x, v ′, x′ )
Complexity and Correctness.                                           wf (rank )
  Gen performs a single top-down descent through the syn-
tax tree of the given CTL+FO formula ϕ. The run time and              Note that there exists an interpretation of aux , inv , and rank
the size of the generated constraints is linear in the size of ϕ.     that satisfies these constraints if and only if the program
Finding a solution for the generated constraints is undecid-          satisfies the property.
4.   EVALUATION                                           Table 1: Evaluation of CTLFO on examples from [6].
   In this section we present CTLFO, a CTL+FO verifica-                Property φ            |=CTL+FO φ |=CTL+FO ¬φ
tion engine. CTLFO implements the procedure Gen and                                         Res. Time Res. Time
applies Ehsf [3] to solve resulting clauses.              P1 ∃x : AG(a = x → AF (r = 1)) X         1.0   ×    0.1
                                                              AG(∃x : a = x → AF (r = 1)) X        0.9   ×    0.1
                                                          P2 ∃x : EF (a = x ∧ EG(r 6= 5)) X        0.9   ×    0.2
                                                              EF (∃x : a = x ∧ EG(r 6= 5)) X       0.6   ×    0.2
                                                          P3 ∃x : AG(a = x → EF (r = 1)) X         1.1   ×    0.1
                                                              AG(∃x : a = x → EF (r = 1)) X        1.0   ×    0.1
                                                          P4 ∃x : EF (a = x ∧ AG(r 6= 1)) X        1.8   ×    0.4
                                                              EF (∃x : a = x ∧ AG(r 6= 1)) X       0.9   ×    0.4
                                                          P5 ∃x : AG(s = x → AF (u = x)) X         7.0   ×    0.1
                                                              AG(∃x : s = x → AF (u = x)) X        7.2   ×    0.1
                                                          P6 ∃x : EF (s = x ∧ EG(u 6= x)) X        1.8   ×    2.2
                                                              EF (∃x : s = x ∧ EG(u 6= x)) X       1.1   ×    2.1
                                                          P7 ∃x : AG(s = x → EF (u = x)) X         3.1   ×    0.2
                                                              AG(∃x : s = x → EF (u = x)) X        6.5   ×    0.1
                                                          P8 ∃x : EF (s = x ∧ AG(u 6= x)) X        14.3  ×    1.8
                                                              EF (∃x : s = x ∧ AG(u 6= x)) X       13.9  ×    1.8
                                                          P9 ∃x : AG(a = x → AF (r = 1)) X        118.7  ×    17.3
                                                              AG(∃x : a = x → AF (r = 1)) X        82.3  ×    1.4
                                                          P10 ∀x : EF (a = x ∧ EG(r 6= 1)) T/O      -    ×    3.5
                                                              EF (∀x : a = x ∧ EG(r 6= 1)) T/O      -    ×    3.5
                                                          P11 ∃x : AG(a = x → EF (r = 1)) X       126.8  ×    3.6
                                                              AG(∃x : a = x → EF (r = 1)) X       140.3  ×    0.2
                                                          P12 ∀x : EF (a = x ∧ AG(r 6= 1)) X      146.7  ×    3.2
                                                              EF (∀x : a = x ∧ AG(r 6= 1)) X      161.7  ×    0.2
                                                          P13∃x : AF (io = x) ∨ AF (ret = x) X    576.8  ×    0.3
                                                          P14∃x : EG(io 6= x) ∧ EG(ret 6= x) X     15.1  ×    48.1
                                                          P15∃x : EF (io = x) ∧ EF (ret = x) X    166.4  ×    1.9
                                                          P16∃x : AG(io 6= x) ∨ AG(ret 6= x) X     3.4 T/O     -

                                                             We run CTLFO on the examples OS frag.1, . . . , OS
                                                          frag.4 from industrial code from [6, Figure 7]. Each ex-
                                                          ample consists of a program and a CTL property to be
                                                          proven. We have modified the given properties to lift the
                                                          CTL formula to CTL+FO. As example, consider the prop-
                                                          erty AG(a = 1 → AF (r = 1)). One modified property to
                                                          check could be ∃x : AG(a = x → AF (r = 1)), and an-
                                                          other one is AG(∃x : (a = x → AF (r = 1))). By doing
                                                          similar satisfiability-preserving transformations of the prop-
                                                          erties for all the example programs, we get a set programs
                                                          whose properties are specified in CTL+FO as shown in Ta-
                                                          ble 1. For each pair of a program and CTL+FO property φ,
                                                          we generated two verification tasks: proving φ and proving
                                                          ¬φ. While the existence of a proof for a property φ implies
                                                          that ¬φ is violated by the same program, we consider both
                                                          properties to show the correctness of our tool.
                                                             We report the results in Table 1. X (resp. ×) marks
                                                          cases where CTLFO was able to prove (resp. disprove) a
                                                          CTL+FO property. T/O marks the cases where CTLFO
                                                          could not find a solution or a counter-example in 600 sec-
                                                          onds.
                                                             CTLFO is able to find proofs for all the correct pro-
                                                          grams except for P10 and counter-examples for all incorrect
                                                          programs except for P16. Currently, CTLFO models the
                                                          control flow symbolically using a program counter variable,
                                                          which we believe is the most likely reason for the solving pro-
                                                          cedure to time out. Efficient treatment of control flow along
                                                          the lines of explicit analysis as performed in the CPAchecker
                                                          framework could lead to significant improvements for deal-
                                                          ing with programs with large control-flow graphs [4]. An exe-
                                                          cutable of CTLFO, together with a more verbose evaluation,
                                                          can be found at https://www7.in.tum.de/~beyene/ctlfo/.
                                                             For cases where the property contains nested path quan-
                                                          tifiers and the outer temporal quantifier is F or U , our im-
plementation may generate non-Horn clauses following the         [16] A. Rensink. Model checking quantified computation
proof system from [14]. While a general algorithm for solv-           tree logic. In CONCUR, 2006.
ing non-Horn clauses is beyond the scope of this paper, we
used a simple heuristic to seed solutions for queries appear-
ing under the negation operator.


5.   CONCLUSION
   This paper presented an automated method for proving
program properties written in the temporal logic CTL+FO,
which combines universal and existential quantification over
time and data. Our approach relies on a constraint genera-
tion algorithm that follows the formula structure to produce
constraints in the form of Horn constraints with forall/exists
quantifier alternation. The obtained constraints can be
solved using an off-the-shelf constraint solver, thus result-
ing in an automatic verifier.


6.   REFERENCES
 [1] F. Belardinelli, A. Lomuscio, and F. Patrizi. An
     abstraction technique for the verification of
     artifact-centric systems. In KR, 2012.
 [2] T. Beyene, M. Brockschmidt, and A. Rybalchenko.
     CTL+FO verification as constraint solving. CoRR,
     abs/1406.3988, 2014.
 [3] T. Beyene, C. Popeea, and A. Rybalchenko. Solving
     existentially quantified Horn clauses. In CAV, 2013.
 [4] D. Beyer and S. Löwe. Explicit-state software model
     checking based on CEGAR and interpolation. In
     FASE, 2013.
 [5] J. Bohn, W. Damm, O. Grumberg, H. Hungar, and
     K. Laster. First-order-CTL model checking. In
     FSTTCS, 1998.
 [6] B. Cook and E. Koskinen. Reasoning about
     nondeterminism in programs. In PLDI, 2013.
 [7] B. Cook, A. Podelski, and A. Rybalchenko.
     Termination proofs for systems code. In PLDI, 2006.
 [8] A. Da Costa, F. Laroussinie, and N. Markey.
     Quantified CTL: expressiveness and model checking.
     In CONCUR, 2012.
 [9] S. Grebenshchikov, N. P. Lopes, C. Popeea, and
     A. Rybalchenko. Synthesizing software verifiers from
     proof rules. In PLDI, 2012.
[10] S. Hallé, R. Villemaire, O. Cherkaoui, and
     B. Ghandour. Model checking data-aware workflow
     properties with CTL-FO+ . In EDOC, 2007.
[11] J. Heusser and P. Malacaria. Quantifying information
     leaks in software. In ASAC, 2010.
[12] K. Hoder, N. Bjørner, and L. M. de Moura. µZ - an
     efficient engine for fixed points with constraints. In
     CAV, 2011.
[13] I. Hodkinson, F. Wolter, and M. Zakharyaschev.
     Decidable and undecidable fragments of first-order
     branching temporal logics. In LICS, 2002.
[14] Y. Kesten and A. Pnueli. A compositional approach to
     CTL∗ verification. Theor. Comput. Sci.,
     331(2-3):397–428, 2005.
[15] A. C. Patthak, I. Bhattacharya, A. Dasgupta,
     P. Dasgupta, and P. Chakrabarti. Quantified
     computation tree logic. Information processing letters,
     82(3):123–129, 2002.
APPENDIX
A.   REMAINING RULES
  In this section we present the remaining rules of Gen,
which deal with the complete set of temporal quantifiers.
See Figure 2.


     | A Xϕ1 ⇒
       let aux = fresh symbol of arity |v0 | in
       init(v0 ) → ∃v0′ : next (v0 , v0′ ),
       init(v0 ) ∧ next (v0 , v0′ ) → aux (v0′ ),
       Gen(ϕ1 , v0 , aux (v0 ), next (v0 , v0′ ))
     | E Xϕ1 ⇒
       let aux = fresh symbol of arity |v0 | in
       init(v0 ) → ∃v0′ : next (v0 , v0′ ) ∧ aux (v0′ ),
       Gen(ϕ1 , v0 , aux (v0 ), next (v0 , v0′ ))
     | A Gϕ1 ⇒
       let inv = fresh symbol of arity |v0 | in
       init(v0 ) → inv (v0 ),
       inv (v0 ) ∧ next (v0 , v0′ ) → inv (v0′ ),
       Gen(ϕ1 , v0 , inv (v0 ), next (v0 , v0′ ))
     | E Gϕ1 ⇒
       let inv = fresh symbol of arity |v0 | in
       init(v0 ) → inv (v0 ),
       inv (v0 ) ∧ next (v0 , v0′ ) → ∃v0′ : next (v0 , v0′ ) ∧ inv (v0′ ),
       Gen(ϕ1 , v0 , inv (v0 ), next (v0 , v0′ ))
     | A (ϕ1 U ϕ2 ) ⇒
       let inv , aux 1 , aux 2 = fresh symbols of arity |v0 | in
       let rank = fresh symbol of arity |v0 | + |v0 | in
       init(v0 ) → inv (v0 ),
       inv (v0 ) ∧ ¬aux 2 (v0 ) → aux 1 (v0 ) ∧ ∃v0′ : next (v0 , v0′ ),
       inv (v0 ) ∧ ¬aux 2 (v0 ) ∧ next (v0 , v0′ ) → inv (v0′ ) ∧ rank (v0 , v0′ ),
       wf (rank ),
       Gen(ϕ1 , v0 , aux 1 (v0 ), next (v0 , v0′ )), Gen(ϕ2 , v0 , aux 2 (v0 ), next (v0 , v0′ ))
     | E (ϕ1 U ϕ2 ) ⇒
       let inv , aux 1 , aux 2 = fresh symbols of arity |v0 | in
       let rank = fresh symbol of arity |v0 | + |v0 | in
       init(v0 ) → inv (v0 ),
       inv (v0 ) ∧ ¬aux 2 (v0 ) → aux 1 (v0 ) ∧ ∃v0′ : next (v0 , v0′ ) ∧ inv (v0′ ) ∧ rank (v0 , v0′ ),
       wf (rank ),
       Gen(ϕ1 , v0 , aux 1 (v0 ), next (v0 , v0′ )), Gen(ϕ2 , v0 , aux 2 (v0 ), next (v0 , v0′ ))
     | (A/E) F ϕ1 ⇒ Gen(v0 , init(v0 ), next (v0 , v0′ ), (A/E) (trueU ϕ1 ))
     | ϕ1 ∧ / ∨ ϕ2 ⇒
       let aux 1 , aux 2 = fresh symbols of arity |v0 | in
       init(v0 ) → aux 1 (v0 ) ∧ / ∨ aux 2 (v0 ),
       Gen(ϕ1 , v0 , aux 1 (v0 ), next (v0 , v0′ )), Gen(ϕ2 , v0 , aux 2 (v0 ), next (v0 , v0′ ))

                               Figure 2: Remaining rules of constraint generation algorithm Gen.
