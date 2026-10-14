                                                  CT L∗ Verification and Synthesis using
                                                        Existential Horn Clauses

                                                              Mishel Carelli      and Orna Grumberg
arXiv:2408.11502v1 [cs.LO] 21 Aug 2024




                                                               Technion - Israel Institute of Technology



                                               Abstract. This work proposes a novel approach for automatic verifi-
                                               cation and synthesis of infinite-state reactive programs with respect to
                                               CT L∗ specifications, based on translation to Existential Horn Clauses
                                               (EHCs).
                                               CT L∗ is a powerful temporal logic, which subsumes the temporal log-
                                               ics LTL and CTL, both widely used in specification, verification, and
                                               synthesis of complex systems.
                                               EHCs with its solver E-HSF, is an extension of Constrained Horn
                                               Clauses, which includes existential quantification as well as the power
                                               of handling well-foundedness.
                                               We develop the translation system Trans, which given a verification prob-
                                               lem consisting of a program P and a specification φ, builds a set of EHCs
                                               which is satisfiable iff P satisfies φ. We also develop a synthesis algorithm
                                               that given a program with holes in conditions and assignments, fills the
                                               holes so that the synthesized program satisfies the given CT L∗ specifi-
                                               cation.
                                               We prove that our verification and synthesis algorithms are both sound
                                               and relative complete. Finally, we present case studies to demonstrate
                                               the applicability of our algorithms for CT L∗ verification and synthesis.


                                         1   Introduction

                                         This work proposes a novel approach for automatic verification and synthesis of
                                         reactive infinite-state programs with respect to CT L∗ specifications, based on
                                         translation to Existential Horn Clauses (EHC).
                                             CTL∗ is a powerful temporal logic, which subsumes the temporal logics LTL
                                         and CTL, both widely used in specification, verification, and synthesis of complex
                                         systems in industry and in academic research. In addition to specifying the
                                         behavior of a system over time, CTL∗ is capable of describing the system’s
                                         branching structure.
                                             Constrained Horn Clauses (CHCs) is a fragment of first-order logic which
                                         has been recently highly successful in automated verification of infinite-state
                                         programs with respect to safety properties [6,5]. CHCs include uninterpreted
                                         predicates that represent, for instance, loop invariants within the checked pro-
                                         gram. CHCs are accompanied with powerful solvers that can determine their
                                         satisfiability. That is, they can find an appropriate interpretation for the unin-
                                         terpreted predicates, so that the CHCs are satisfied. Given a verification problem
consisting of a program and a safety property, the problem can be translated to
a set of CHCs, which is satisfiable iff the program satisfies the property.
    While being successful in proving safety properties, CHCs lack the power of
proving properties such as termination and general liveness or branching tem-
poral properties. For the former, a notion of well-foundedness is needed. For the
latter, an existential quantifier is needed for choosing one of several branches.
    Existential Horn Clauses (EHCs) with their solver E-HSF [3], is an extension
of CHCs, which include existential quantification as well as the power of handling
well-foundedness.
    Our work is built on two pillars. One, is the seminal paper by Kesten and
Pnueli [14], which establishes a compositional approach to deductive verification
of First-Order CT L∗ . The other is the EHC logic with its solver E-HSF [3]
applicable to linear programs, which together provides a strong formal setting
for verification problems that can be determined by EHC satisfiability.
    The compositional approach to CT L∗ in [14] provides proof rules for basic
(assertional) state formulas of the form Qc, where Q is a path quantifier and
c is an assertion. Formulas including temporal operators are reduced to the
basic form by applying rules for successive eliminations of temporal operators.
The reductions involve building program-like (testers) structures that are later
composed with each other and with the verified program.
    Our work adopts the idea of transforming a specification to basic state for-
mulas while eliminating temporal operators. However, it takes a significantly
different approach. We develop a translation system Trans, which given a veri-
fication problem consisting of a program P and a specification φ, builds a set
of EHCs which is satisfiable iff P satisfies φ. Trans consists of 8 translation
rules. The first replaces each basic subformula in φ with a boolean variable. The
second replaces non-fair path quantifiers Q with fair path quantifiers Qf . The
next three rules eliminate temporal path subformulas of the form N ext (Xc),
Globally (Gx), and U ntil (c1 U c2 ), using fresh boolean variables and fresh un-
interpreted predicates. Additional constraints require that the program satisfies
the appropriate temporal property.
    It should be noted, that our programs include fairness conditions that restrict
the paths under consideration. This is because, the elimination of both Globally
and U ntil require such conditions. Moreover, handling fairness as part of the
program and not as part of a specification is much more efficient. Typically, the
program is large and the specification is relatively small. However, specifications
describing program fairness might be of size of the program.
    The sixth and seventh translation rules in Trans deviate the most from [14].
Rule 6 handles the verification of Af c, i.e., along every fair path, assertion c
holds. For that purpose, the translation imposes the requirement that if a path
does not satisfy c, then it is not fair. Well-foundedness is needed for proving this
fact. Rule 7 handles Ef c, i.e., for every initial state there is a fair path starting
at it. Here we need both well-foundedness and an existential quantification, both
supplied by EHCs. In our translation rules we also use negations and disjunctions
that are not allowed by CHCs, but are expressible by EHCs.

                                          2
    We prove that our translation Trans is sound and relative complete.
    Next, we turn to exploiting our approach for synthesis. We are given a partial
program, in which some of the conditions (e.g. in while loops) and assignments
are missing (holes). We are also given a CT L∗ specification. Our goal is to
synthesize a “filling” to the holes, so that the synthesized program satisfies the
CT L∗ specification.
    We obtain this by first filling each hole with an uninterpreted predicate.
Additional constraints are added to guarantee that predicates associated with a
condition or an assignment indeed behave accordingly. Finally, we build EHCs
to describe the new program and send it to the EHC solver, which will return
interpreted predicates to serve as hole fillings. Here again we prove the soundness
and relative completeness of our approach.
    Finally, we present case studies to demonstrate the applicability of our algo-
rithms for CT L∗ verification and synthesis.

Related work Several works [1,4] exploit the approach presented in [14] to
perform CTL+FO verification via EHC-solving. We significantly extend their
result to perform full CT L∗ verification. We also show that EHCs can be further
exploited for CT L∗ synthesis.
    In [2], EHCs are used to solve reachability, safety and LTL games on infinite
graphs. This tool can perform CT L∗ verification, since CT L∗ can be expressed
through µ-calculus [10], µ-calculus verification can be performed through parity-
games [18], which are a special case of LTL games. However, the translation of
CT L∗ to µ-calculus is doubly exponential [10]. As a result, a direct model check-
ing of CT L∗ according to our approach is more efficient than first translating
and then solving the resulting LTL game.
    In [20], condition synthesis is performed, given a program with holes in con-
ditions and specifications as assertions in the code. The program behaviors are
modeled “backwards” using CHCs. The CHC solver infers conditions so that
the synthesized program satisfies the assertions. In our work we synthesize both
conditions and assignments with respect to full CT L∗ . Program behaviors are
modeled “forward”. However, we use EHCs rather than the more standard mod-
eling via CHCs to model the problem.
    Many works use synthesis to fill holes in partial program. Sketch [21,13]
synthesizes programs to satisfy input-output specifications. In template-based
synthesis [22] the specification is in the form of assertions in the code. Overview
on synthesis and on synthesis of reactive programs can be found in [12] and [11].
Condition synthesis can also be used to repair programs [25,17,26,20].
    Termination has been proved in [9]. Several works are able to synthesize finite-
state full systems for propositional CTL∗ specifications. [16] translates proposi-
tional CTL∗ formulas to hesitant alternating automata. [15] proposes bounded
synthesis for CTL∗ . The paper bounds the number of states in the synthesized
system to some k. The bound is increased if no such system exists. Clearly, such
an algorithm is complete only if the goal of the synthesis is a finite-state system.
Moreover, it cannot determine unrealizability. [7] shows how to apply CTL∗ syn-

                                         3
thesis via LTL synthesis. Both logics are propositional. It exploits translation to
a hesitant automaton, which is then sent to an SMT solver.
    In contrast, our work handles First-Order CTL∗ specifications. It can syn-
thesize infinite-state systems and can determine unrealizability. However, we are
given as input a partial (sketch-like) program, from which we synthesize a full
program.
    Another type of Horn-like clauses, very similar to EHCs, called pfwCSP, has
been introduced in [24]. pfwCSP does not allow existential quantification in the
heads of clauses but allows disjunctions and can require that an uninterpreted
predicate behaves like a function. Instead of disjunctively well-founded clauses,
pfwCSP can require well-foundedness.
    The authors of [24] present a fully automated CEGIS-based method for solv-
ing pfwCSP and implement it for the theory of quantifier-free linear arithmetic.
Furthermore, the authors describe how relational verification concerning different
relational verification problems, including k-safety, co-termination, termination-
sensitive non-interference, and generalized non-interference for infinite-state pro-
grams, can be performed using pfwCSP.
    The authors conjecture that EHCs and pfwCSP are inter-reducible.
    In future work, our rules can be redesigned to reduce CT L∗ verification to
pfwCSP satisfiability by replacing the only occurrence of the existential quanti-
fier in rule 7 with a Skolem function using a functional predicate and substituting
disjunctive well-foundedness with well-foundedness.
    Another use of pfwCSP is presented in [23]. The authors define a first-order
fixpoint logic with background theories called µCLP and reduce the validity
checking of µCLP to pfwCSP solving. Moreover, they present a modular primal-
dual method that improves the solving of the pfwCSP, generated for µCLP
formulas.
    The authors mention that several problems, such as LTL, CTL, and even full
µ-calculus model checking, can be encoded using µCLP for infinite-state systems
in a sound and complete manner. Similar techniques were used in [24] to perform
µ-calculus verification in a sound but incomplete way.
    Another sound but incomplete procedure for CT L∗ verification of infinite-
state systems has been presented in [8].


2     Preliminaries

2.1   Forall-exists Horn-like clauses (EHC)

Let T be a first-order theory over signature Σ. Then, Forall-exists Horn-like
clauses, also called Existential Horn Clauses (EHCs), are first-order formulas of
two types: implications and dwf -clauses.

 1. Implications are formulas with uninterpreted predicates of the form:

          c(v0 ) ∧ q1 (v1 ) ∧ · · · ∧ qn (vn ) → ∃w : b(w0 ) ∧ p1 (w1 ) ∧ . . . pm (wm )

                                             4
    where q1 , . . . , qn , p1 , . . . , pm are uninterpreted predicate symbols, not in-
    cluded in Σ; v0 . . . vn , w0 , . . . , wm are tuples of variables, not necessarily dis-
    joint; c and b are quantifier-free
                                    Sm          formulas from T over variables v0 and w0 ,
    respectively, and w ⊆ i=0 wi .
    The left-hand side of the clause is called the body of the clause and the
    right-hand side is called the head.
 2. Disjunctively well-founded clauses or dwf -clauses are of the form:

                                             dwf (q)
    where q(v, v ′ ) is an uninterpreted predicate of arity 2n for some n ∈ N.

The semantics of EHCs Let I be an interpretation, defined over a domain
E. I associates with each uninterpreted predicate of arity k a k-ary relation over
E. Given a formula φ, I(φ) is the formula obtained by replacing each occurrence
of an uninterpreted predicate p with its interpretation, I(p). We say that clause
f (u) = body(u) → head(u) is satisfied under I, if I(body(u)) |=T I(head(u)).
    To define the semantics of dwf -clauses we need the notion of a disjunctively
well-founded relation.
Definition 1. A relation r(v, v ′ ) over a set X is well-founded if there is no
infinite sequence of elements in X, x1 , x2 , . . . such that for every i: r(xi , xi+1 ).
A relation r(v, v ′ ) is disjunctively well-founded if it is included in a finite union
of well-founded relations. Formally, r(v, v ′ ) → r1 (v, v ′ ) ∨ · · · ∨ rl (v, v ′ ) for some
well-founded relations r1 , . . . , rl .
An interpretation I satisfies dwf (q) for a predicate q of arity 2n, if I(q) is a
disjunctively well-founded relation over the set E n .
     Note that, our notion of satisfiability is semantic, referring only to the do-
main over which the interpretation I is defined, ignoring the syntax over which
relations associated with uninterpreted predicates are expressed.
     Theorem 1 from [19] can be reformulated as follows: A relation is well-founded
if its transitive closure is disjunctively well-founded. We refer to this formulation
when we use this theorem in our work.
Expressing disjunction and negation with EHC For our purposes, we
need to express a disjunction in the heads of EHC clauses. A clause of the form
body → head1 ∨ head2 is equivalent to the following three forall-exists Horn-like
clauses, using a new boolean variable a:
          body → ∃a : head(a); head(0) → head1 ; head(1) → head2

    Given a predicate p(v), we define a predicate q(v) such that q(v) ≡ ¬p(v)
using the following two clauses:
                      p(v) ∧ q(v) → ⊥; ⊤ → p(v) ∨ q(v)

If both of them are satisfied, then q(v) ≡ ¬p(v).
    From now on, we use disjunctions and negations as part of the forall-exists
Horn-like clauses, implying that we express them as described above.

                                              5
2.2       CT L∗ verification
In this section we present the verification problems that we solve.
Program Let us fix a first-order theory T . We view a program as a transition
system with fairness conditions. A program P consists of a tuple of program
variables v, and two formulas next(v, v ′ ) and init(v), describing the transition
relation and the set of initial states, respectively. In addition, it includes a finite
set J of assertions in T , describing the set of fairness conditions.
     The states of P are the valuations of v. A path of P is a sequence of states
s1 , s2 , . . ., such that si , si+1 |=T next(v, v ′ ) for every i. An infinite path s1 , s2 , . . .
is fair if for every φ ∈ J we have si |=T φ for infinitely many i’s. If J = ∅ then
every infinite path is fair. Note that the transition relation is not required to be
total. Nevertheless, only infinite sequences of states are considered as program
paths in the semantics of CT L∗ defined later.
Syntax and semantics of CT L∗ We define the syntax of CT L∗ formulas
in negation normal form (NNF), where negations are applied only to atomic
assertions. Let c range over assertions in T . State formulas φ and path formulas
ψ can be defined by the following grammar.
                           φ := c|φ ∧ φ|φ ∨ φ|Eψ|Aψ|Ef ψ|Af ψ
                             ψ := φ|Gψ|Xψ|ψU ψ|ψ ∧ ψ|ψ ∨ ψ
      ∗
CT L is the set of state formulas defined by this grammar.
    We use Q to denote a non-fair quantifier (A or E), ranging over all infinite
program paths. Qf denotes a fair quantifier (Af or Ef ), ranging only over fair
paths.
    A CT L∗ state formula of the form Qψ or Qf ψ is called basic, if ψ does not
contain path quantifiers.
    Let P be a program, s range over the states of P , and π range over the paths
of P . We use π i to denote the suffix of π, starting at the i’th state.
    The semantics of CT L∗ is defined with respect to a program P , where boolean
and temporal operators have their usual semantics: π |= Xψ iff ψ holds on π 1 ;
π |= Gψ iff ψ holds on every suffix of π; π |= ψ1 U ψ2 iff ψ2 eventually holds on
a suffix π j of π and ψ1 holds in all preceding suffixes.
 P, s |= c iff s |=T c
 P, s |= Eψ iff there exists an infinite path π starting at s such that P, π |= ψ
 P, s |= Aψ iff for every infinite path π starting at s: P, π |= ψ
 P, s |= Ef ψ iff there exists a fair path π starting at s such that P, π |= ψ
 P, s |= Af ψ iff for every fair path π starting at s: P, π |= ψ
 P, π |= φ iff s is the first state of π and P, s |= φ


The CT L∗ verification problem We say that P satisfies a CT L∗ formula φ,
denoted P |= φ, if φ holds in every initial state of P . That is, for every state s
of P : init(s) → P, s |= φ.

                                                 6
    We view the verification problem as the tuple (v, init(v), next(v, v ′ ), J, φ),
where the first four elements are the parameters of the program and the last one
is the CT L∗ state formula that the program must satisfy.


3   Reduction of CT L∗ verification problem to EHC
    satisfiability
Our goal is to generate a set of EHCs for a given verification problem, such that
the set of EHCs is satisfiable iff the program meets the specification.
    We denote the desired set of EHCs as Clauses(v, init(v), next(v, v ′ ), J, φ)
and define it recursively on the structure of φ. We prove that this recursive
definition is always sound (Theorem 2) and relatively complete (Theorem 3).
    Below, we present our translation system Trans, which consists of eight rules,
and explain the intuition behind them.
    We use the notation φ1 (φ2 ) to describe a formula φ1 that contains one or
more occurrences of a state subformula φ2 . φ1 (γ) then stands for the formula φ1
in which every occurrence of φ2 is replaced by the state formula γ.
    Denote D = (v, init(v), next(v, v ′ ), J). Recall that if D |= φ then for all s,
init(s) → φ.

 1. Consider the CT L∗ state formula φ2 (φ1 ) with a basic state subformula φ1
    and let aux be a fresh uninterpreted predicate of arity |v|, then

                                Clauses(D, φ2 (φ1 )) =

         = Clauses(v, aux(v), next(v, v ′ ), J, φ1 ) ∪ Clauses(D, φ2 (aux)(v)).
    Explanation of Rule 1: The fresh predicate aux represents an underap-
    proximation of the set of states in which φ1 is satisfied. Since our formu-
    las are in NNF, where negations are applied only to atomic assertions, we
    can conclude that φ2 (aux(v)) is an underapproximation of φ2 (φ1 ). Thus, by
    init(v) → φ2 (aux) we also have init(v) → φ2 (φ1 ).
 2. Let Qφ be a CT L∗ basic state formula, where Q is a non-fair path quantifier
    (E or A). Let Qf be the fair version of Q (Ef or Af , respectively), then

             Clauses(D, Qφ) = Clauses(v, init(v), next(v, v ′ ), ∅, Qf φ).

    Explanation of Rule 2: Since the only path quantifier in Qφ is non-fair,
    it does not depend on the fairness conditions. Hence, we can eliminate those
    conditions from the program and replace Q with its fair version.
 3. Let c be an assertion in T . Suppose we have the CT L∗ basic state formula
    Qf φ(Xc). Let xX be a new boolean variable, then

                               Clauses(D, Af φ(Xc)) =

       = Clauses(v ∪ {xX }, init(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J, Af φ(xX )).

                                          7
  In the case of an existential path quantifier we also need a fresh uninterpreted
  predicate aux of arity |v| + 1:

             Clauses(D, Ef φ(Xc)) = {init(v) → ∃xX : aux(v, xX )}∪

    ∪ Clauses(v ∪ {xX }, aux(v, xX ), next(v, v ′ ) ∧ (xX = c(v ′ )), J, Ef φ(xX )).
  Explanation of Rule 3: The new variable xX represents the value of c(v)
  in the next state of the path. This is achieved through the new constraint
  added to next(v, v ′ ). Hence, we can replace Xc by xX in the verified formula.
  For the existential quantifier Ef , we add a new auxiliary predicate aux over
  (v, xX ) that, if initially holds for a certain value of xX , it is guaranteed that
  Ef φ(xX ) holds as well. The additional clause init(v) → ∃xX : aux(v, xX ),
  when interpreted together with the rest of the clauses, guarantees that for
  every initial state there is a value of xX , such that aux(v, xX ) initially holds.
  The reason why we need this auxiliary predicate is that we do not know the
  value of xX in the beginning of the path. For example, if φ(Xc) = F Xc, then
  a path that satisfies this formula may or may not have Xc in the first state.
  Therefore, we want to express that we can consider paths with any initial
  value of xX . The second set of clauses guarantees that if initially aux(v, xX )
  holds for some value xX , then Ff φ(xX ) holds as well.
  The same approach is applied in rules 4 and 5 with the existential quantifier.
4. Let c be an assertion in T . Suppose we have the CT L∗ basic state formula
   Qf φ(Gc). Let xG be a new boolean variable, then

                               Clauses(D, Af φ(Gc)) =

  = Clauses(v∪{xG }, init(v), next(v, v ′ )∧(xG = (c(v)∧x′G )), J∪{xG ∨¬c(v)}, Af φ(xG )).
  In the case of an existential path quantifier, similarly to Rule 3, we also need
  a fresh uninterpreted predicate aux of arity |v| + 1:

             Clauses(D, Ef φ(Gc)) = {init(v) → ∃xG : aux(v, xG )}∪

  Clauses(v∪{xG }, aux(v, xG ), next(v, v ′ )∧(xG = c(v)∧x′G ), J∪{xG ∨¬c(v)}, Ef φ(xG ))
  Explanation of Rule 4: If the new variable xG is true in some state, then
  the new condition added to the transition relation ensures that c(v) and xG
  are true in every consecutive state. Thus, xG represents the value of Gc along
  the path. The new fairness condition ensures that if for every state of the
  path c(v) is true, then xG must be true infinitely often along this path.
5. Let c1 and c2 be assertions in T . Suppose we have the CT L∗ basic state
   formula Qf φ(c1 U c2 ). Let xU be a new boolean variable, then

              Clauses(D, Af φ(c1 U c2 )) = Clauses(v ∪ {xU }, init(v),

     next(v, v ′ ) ∧ (xU = c2 (v) ∨ (c1 (v) ∧ x′U )), J ∪ {¬xU ∨ c2 (v)}, Af φ(xU )).

                                          8
   In the case of an existential path quantifier, similarly to Rule 3, we need a
   fresh uninterpreted predicate aux of arity |v| + 1:

                                   Clauses(D, Ef φ(c1 U c2 )) =

   = Clauses(v ∪ {xU }, aux(v, xU ), next(v, v ′ ) ∧ (xU = (c2 (v) ∨ (c1 (v) ∧ x′U ))),
           J ∪ {¬xU ∨ c2 (v)}, Ef φ(xU )) ∪ {init(v) → ∃xU : aux(v, xU )}.
   Explanation of Rule 5: The new variable xU represents the value of c1 U c2
   along the path. The new condition added to the transition relation defines
   U recursively. The new fairness condition ensures that if for every state of
   the path xU holds, then c2 (v) must hold infinitely often along this path.
6. Let c be an assertion in T . Suppose we have a basic CT L∗ state formula
   Af c. Let p be a fresh uninterpreted predicate of arity |v| and let r, t be fresh
   uninterpreted predicates of arity 2|v|. Let v0 , . . . , v|J| be |J| + 1 copies of the
   set of program variables v. Suppose J 6= ∅, then,

    Clauses(D, Af c) = {init(v) ∧ ¬c(v) → p(v), next(v, v ′ ) ∧ p(v) → p(v ′ ),

                           ^
                           |J|
                p(v0 ) ∧         (t(vi−1 , vi ) ∧ Ji (vi )) → r(v0 , v|J| ), dwf (r),
                           i=1

              next(v, v ′ ) → t(v, v ′ ), t(v, v ′ ) ∧ next(v ′ , v ′′ ) → t(v, v ′′ )},
   where Ji is the i-th element of J.
   If J = ∅, then,


    Clauses(D, Af c) = {init(v) ∧ ¬c(v) → p(v), next(v, v ′ ) ∧ p(v) → p(v ′ ),

                             p(v) ∧ t(v, v ′ ) → r(v, v ′ ), dwf (r),
              next(v, v ′ ) → t(v, v ′ ), t(v, v ′ ) ∧ next(v ′ , v ′′ ) → t(v, v ′′ )}

   Explanation of Rule 6: The new predicate p(v) represents states that
   are reachable from initial states that do not satisfy c(v). The predicate t
   represents the transitive closure of the transition relation next. The predicate
   r(v, v ′ ) represents a pair of states from p that can be connected by a path
   that satisfies every fairness constraint at least once.
   In order to verify that the program satisfies Af c we need to prove that
   every initial state either satisfies c(v) or there is no fair path starting in
   that state. The latter is guaranteed by showing that r(v, v ′ ) is well-founded,
   which implies that not all fairness conditions hold infinitely often.
   If J = ∅, then every infinite path is fair, since the program does not have
   any fairness constraints. Hence, we want to avoid infinite paths that start in
   initial states that do not satisfy c. In that case, we set r(v, v ′ ) to represent
   pairs of states from p that can be connected by a path. Since r is disjunctively
   well-founded, there is no infinite path from a state that satisfies p.


                                                 9
 7. Let c be an assertion in T and let Ef c be a basic CT L∗ state formula. Let
    q1 , . . . , q|J| be fresh uninterpreted predicates of arity |v| and r1 , . . . , r|J| be
    fresh uninterpreted predicates of arity 2|v|. Suppose J 6= ∅. Then,
                     Clauses(D, Ef c) = {init(v) → c(v) ∧ q1 (v)} ∪
     ∪ {qi (v) → ∃v ′ : next(v, v ′ ) ∧ ((Ji (v) ∧ q(i%|J|)+1 (v ′ )) ∨ (ri (v, v ′ ) ∧ qi (v ′ ))),
                    dwf (ri ), ri (v, v ′ ) ∧ ri (v ′ , v ′′ ) → ri (v, v ′′ ) | i ≤ |J|},
    where Ji is the i-th element of J. i%|J| is the remainder of i modulo |J|.
    If J = ∅, let q be a fresh predicate of arity |v|, then
    Clauses(D, Ef c) = {init(v) → c(v) ∧ q(v), q(v) → ∃v ′ : next(v, v ′ ) ∧ q(v ′ )}

    Explanation of Rule 7: In order to verify that the program satisfies Ef c
    we need to prove that every initial state s0 satisfies c(v) and there is a fair
    path starting at s0 .
    The clauses dwf (ri ), ri (v, v ′ ) ∧ ri (v ′ , v ′′ ) → ri (v, v ′′ ) ensure that ri is a
    disjunctively well-founded and transitive relation. Hence, it is well-founded.
    ri (v, v ′ ) means that v ′ is closer to a state that satisfies Ji than v. Since ri is
    well-founded it takes only finitely many steps to get to a state that satisfies
    Ji .
    The new predicate qi represents the states from which it is possible to get to
    a state s that satisfies Ji . In addition, there is a transition from s to a state
    satisfying qj for j = (i%|J|) + 1, meaning that eventually, Jj holds too.
    We use (i%|J|) + 1 instead of i + 1 to emphasize that when a state that
    satisfies J|J| is found, we continue to look for a state that satisfies J1 , so
    every Ji will be satisfied infinitely many times along the path.
    If J = ∅, then every infinite path is a fair path. Hence, we just prove that
    every initial state satisfies c(v) and is the start of an infinite path. Predicate
    q represents the set of states, that lie on an infinite path.
 8. Let c be an assertion in T . Suppose we have the CT L∗ state formula c, then

                 Clauses(v, init(v), next(v, v ′ ), J, c) = {init(v) → c(v)}.
Remark 1. Applying Trans to a verification problem may result in a non-unique
set of clauses. This may occur when the specification is a basic state formula that
contains more than one path subformula. For example, Ef (Xc1 ∨ Gc2 ). In such
cases, these subformulas can be eliminated (using rules 3 and 4) in any order.
As the soundness and relative completeness theorems prove, all sets produced
by Trans correctly represent the given verification problem.
    Unless otherwise stated, Clauses(v, init(v), next(v, v ′ ), J, φ) will refer to any
set of clauses that may be produced by Trans.
    For every verification problem, Trans terminates, since every rule calls proce-
dure Clauses for a problem with a smaller verification formula, except of rule 2,
which can be called only once for every non-fair path quantifier in the specifica-
tion formula.

                                                  10
Theorem 1 (complexity). Let (D, φ) be a verification problem, with a pro-
gram of size m, with k fairness conditions, and a specification formula of size n.
Then Trans produces a set Clauses(D, φ) consisting of O(n(n + k)) clauses with
a total size of O(n(n + k)(n + m)).


3.1   Soundness

Theorem 2 (soundness).
    For every set Clauses(v, init(v), next(v, v ′ ), J, φ) of clauses produced by
Trans, if the set is satisfiable, then the program D = (v, init(v), next(v, v ′ ), J)
satisfies φ.

Proof. We prove the theorem by induction on the size of the formula φ. Recall
that by definition, CTL∗ formulas are state formulas. As such, they are true in
a program D if all initial states of D satisfy the formula. That is, init(v) → φ.
We will use this fact in the proof.
Base: Rule 8 forms the basis of the induction. For an assertion c in T ,
Clauses(D, c) = {init(v) → c(v)}. If this set of clauses is satisfiable then, by
definition of CTL∗ satisfiability, D |= c.
Induction step:
Rule 1:
Assume a set of clauses Clauses(D, φ2 (φ1 )) is satisfiable by an interpretation I.
Then, I satisfies Clauses(v, aux(v), next(v, v ′ ), J, φ1 ) and by the induction hy-
pothesis, (v, I(aux)(v), next(v, v ′ ), J) |= φ1 . Thus, I(aux)(v) → φ1 . Also, I sat-
isfies Clauses(D, φ2 (aux)(v)) and by the induction hypothesis D |= φ2 (I(aux)).
Since φ2 is in Negation Normal Form (NNF), replacing all occurrences of I(aux)
in φ2 with φ1 results in a formula that is also true in D. We thus conclude that
D |= φ2 (φ1 ), as required.
   We present here the proof of Rule 4 (Universal and Existential cases). The
proofs of Rules 3, 5 are presented in the Appendix A.2.
Rule 4, Universal:
Suppose D = (v, init(v), next(v, v ′ ), J) does not satisfy Af φ(Gc). Then there is
a fair path π = s1 , s2 , . . . such that D, s1 |= init(v) and D, π 6|= φ(Gc).
    Consider the path πG = s′1 , s′2 , . . . of the program DG = (v ∪
{xG }, init(v), next(v, v ′ )∧(xG = c(v)∧x′G ), J ∪{xG ∨¬c(v)}), where s′i (v) = si (v)
and s′i (xG ) = true iff for every j ≥ i : s′j |= c(v). Note that, once xG is set to
true on πG , c(v) is set to true. Moreover, they both remain true forever from
that point on.
    πG is a fair path of DG since the fairness conditions of D do not depend on
xG . The additional fairness condition of DG holds as well, since if c(v) holds from
a certain point on along πG then xG holds from that point on. Thus, xG ∨ ¬c(v)
holds infinitely often along πG .
    Also DG , πG 6|= φ(xG ), since xG is true on the same locations of path πG as
the locations of π where Gc is true.

                                          11
    Hence, DG does not satisfy Af φ(xG ). By the induction hypothesis, every set
of clauses produced by Trans for Clauses(DG, Af φ(xG )) is unsatisfiable. Since
Clauses(D, Af φ(Gc)) = Clauses(DG, Af φ(xG )), this implies that every set of
clauses produced by Trans for Clauses(D, Af φ(Gc)) is unsatisfiable, as required.
Rule 4, Existential:
Suppose a set Clauses(v, init(v), next(v, v ′ ), J, Ef φ(Gc)) is satisfied by inter-
pretation I. Denote DG = (v ∪ {xG }, I(aux)(v, xG ), next(v, v ′ ) ∧ (xG = c(v) ∧
x′G ), J ∪ {xG ∨ ¬c(v)}). Then, by Rule 4, Clauses(DG , Ef φ(xG )) is also satisfied
by I. By the induction hypothesis DG |= Ef φ(xG ).
     Let s be a state of D = (v, init(v), next(v, v ′ ), J), such that D, s |= init(v).
Since the clause {init(v) → ∃xG : aux(v, xG )} is satisfied by interpretation
I, then there is a state sG of DG such that sG (v) = s(v) and DG , sG |=
I(aux)(v, xG ). Moreover, there is a fair path πG = sG , s′2 , s′3 , . . . of DG such
that DG , πG |= φ(xG ). Consider the path of D defined by π = s, s2 , s3 . . . , where
si (v) is the restriction of s′i to the variables from v. Then D, π |= φ(Gc). This is
because xG is true on the same places of the path πG as the places of π where
Gc is true. Moreover, π is a fair path. Thus, D satisfies Ef φ(Gc).
Rule 6:
Denote D = (v, init(v), next(v, v ′ ), J). Suppose by way of contradiction that a
set Clauses(D, Af c) is satisfied by an interpretation I but the program D does
not satisfy the formula Af c. Then, there is a fair path π = s0 , s1 , s2 , . . . , such
that D, s0 |= init(v) and D, π 6|= c.
    By the clauses init(v) ∧ ¬c(v) → I(p)(v), next(v, v ′ ) ∧ I(p)(v) → I(p)(v ′ )
we know that for every i : si |= I(p)(v).
    Since π is fair, each Jj holds infinitely often along π. Moreover, there is an
infinite increasing sequence of indexes 0 < i1 < i2 < i3 <, . . . , such that for
every k : sik |= Jk%|J|+1 .
                                   V|J|
    By the clause I(p)(v0 ) ∧ i=1 (I(t)(vi−1 , vi ) ∧ Ji (vi )) → I(r)(v0 , v|J| ) we
get that sin1 |J| , sin2 |J| |= I(r)(v, v ′ ) for every pair of natural numbers n1 , n2 ,
provided n1 < n2 . Thus, I(r), which is disjunctive well-founded, contains an
infinite transitive chain, but this is impossible due to Theorem 1 from [19]. A
contradiction.
Rule 7:
Suppose a set of clauses Clauses(D, Ef c) is satisfied by interpretation I.
    In order to prove that D satisfies Ef c we need to show that every state that
satisfies init(v) also satisfies c(v) and is a start of a fair path.
    Suppose for some state s of D, s |= init(v), then by clause init(v) → c(v) ∧
I(q1 )(v) we have s |= c(v) and s |= I(q1 )(v).
    By clauses {dwf (I(ri )), I(ri )(v, v ′ ) ∧ I(ri )(v ′ , v ′′ ) → I(ri )(v, v ′′ ) | i ≤ |J|}
we know that for every i ≤ |J|, relation I(ri ) is disjunctively well-founded and
transitive, hence it is a well-founded relation by Theorem 1 from [19].
    For every i ≤ |J|, by clause I(qi )(v) → ∃v ′ : next(v, v ′ ) ∧ ((Ji (v ′ ) ∧
I(q(i%|J|)+1 )(v ′ )) ∨ (I(ri )(v, v ′ ) ∧ I(qi )(v ′ ))) and the fact that I(ri ) is a well-
founded relation we can conclude that for every state t of D if t |= I(qi )(v) then

                                               12
there is a path in D from t to some state t′ such that t′ |= Ji (v) and there is a
transition from t′ to some state t′′ such that t′′ |= I(q(i%|J|)+1 )(v).
   Thus, there is a fair path, that starts in s.                                 ⊓
                                                                                 ⊔

3.2   Relative completeness
Next we show that Trans is relative complete. That is, if a verification problem
holds, i.e., the program meets its specification, then every set of clauses, produced
by Trans for that problem, is satisfied by some interpretation of the uninterpreted
predicates. However, this interpretation might not be expressible by a first-order
formula in our logic.

Theorem 3 (relative completeness). If D = (v, init(v), next(v, v ′ ), J) sat-
isfies φ then every set produced by Trans for Clauses(D, φ) is satisfiable by some
interpretation of the uninterpreted predicates.

Proof. We prove the theorem by induction on the size of the verified formula.
Base:
Rule 8: For assertion c in T , if D |= c then Clauses(D, c) = {init(v) → c(v)}
is satisfiable by definition of CTL∗ semantics.
Induction step:
Rule 1:
Assume D |= φ2 (φ1 ). For the uninterpreted predicate aux, we choose as inter-
pretation the predicate I(aux), which is true in exactly those states where φ1 is
true. Then, (v, I(aux)(v), next(v, v ′ ), J) meets φ1 and (v, init(v), next(v, v ′ ), J)
meets φ2 (I(aux)). By the induction hypothesis, the corresponding sets of clauses
are satisfiable. Consequently, Clauses(D, φ1 (φ2 )) is satisfiable.
In the rest of the proof we omit some details of the induction steps. The full
proof appears in the Appendix A.3.
Rule 3, Universal:
If D = (v, init(v), next(v, v ′ ), J) meets Af φ(Xc), then DX = (v ∪
{xX }, init(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J) meets Af φ(xX ). This is because
for every fair path of DX , the formula xX is true in exactly the same places
where Xc is true on the corresponding path of D. By the induction hypothesis,
every set of clauses produced by Trans for Clauses(DX , Af φ(xX )) is satisfiable.
Consequently, every set of clauses produced by Trans for Clauses(D, Af φ(Xc))
is satisfiable, as required.

Rule 6:
Suppose the program D = (v, init(v), next(v, v ′ ), J) satisfies Af c. Recall that,
D |= Af c implies that every initial state of D either satisfies c or has no fair
path starting in it. We define an interpretation I as follows:
 – s |= I(p)(v) iff there is no fair path starting at s.
 – s, s′ |= I(t)(v, v ′ ) iff there is a path from s to s′ .

                                           13
 – s, s′ |= I(r)(v, v ′ ) iff s |= I(p)(v), s′ |= J|J| (v ′ ) and there is a path from s
   to s′ which visits a state satisfying J1 , then a state satisfying J2 and so on
   until it ends in s′ that satisfies J|J| .
Rule 7:
Suppose the program D = (v, init(v), next(v, v ′ ), J) satisfies Ef c. This means
that every initial state s of D satisfies c, and, in addition, s is the start of a fair
path. We say that a state s of D is fair if there is a fair path starting at s. We
define the interpretation I as follows. For every i ∈ {1, . . . , |J|}:

 – s |= I(qi )(v) iff s is a fair state.
 – s, s′ |= I(ri )(v, v ′ ) iff s′ is a fair state and s satisfies Ji or s′ is the successor
   of s on the shortest path π leading from s to a fair state s′′ satisfying Ji . ⊓       ⊔


4    Case study 1: CT L∗ verification of a robot system
                                             Suppose we are given a system with
                                         three robots placed on rational points of
                                         a two-dimensional plane. A user makes
l1 : while ( t r u e ) {                 an ongoing interaction with the system
l2 :     r o bo t_ id := ∗ ;             by sending commands. The system pro-
l3 :     a := ∗ ;                        cesses the commands and moves the
l4 :     b := ∗ ;                        robots accordingly.
l5 :     i f ( r o bo t_ id == 1 ) {         We wish to verify two properties. The
l6 :             x1 := x1 + 2a + b ;     first property states that the three robots
         }                               are never located in the same position
l7 :     i f ( r o bo t_ id == 2 ) {     at the same time. The second property
l8 :             x2 := x2 + a + b ;      states that for each pair of robots, the
l9 :             y2 := y2 − 2a − 2b ;    user can manipulate the robots in such a
         }                               way that this pair meets infinitely often.
l10 :    i f ( r o bo t_ id == 3 ) {         Program R, presented in Figure 1, de-
l11 :            x3 := x3 + a + b ;      scribes the interaction between the user
l12 :            y3 := y3 − a − b ;      and the system. Program R consists of a
         }                               while-loop. At the beginning of each iter-
      }                                  ation, three variables robot_id, a and b
                                         are assigned non-deterministically. These
                                         are the inputs from the user. Variable
       Fig. 1: Robots program R
                                         robot_id represents the identification of
                                         the robot that the user wishes to move.
                                         Variables a and b represent the moving
instruction, given by the user to the selected robot.
     Variables xi and yi represent the current position of robot i on the plane.
     If the user chooses robot i, then the system changes its position according
to the linear transformation defined for robot i, based on a and b. For each
robot, a different linear transformation is being used. For example, for robot 2
the transformation is (a + b, −2a − 2b).

                                            14
   Let us denote the set of variables of R (including the variable pc) as v and
the transition relation of R as next(v, v ′ ). The initial positions of the robots are
given by the initial condition: init(v) = (x1 = y1 = x2 = y2 = x3 = 0)∧(y3 = 2).
The property we wish to verify is given by the CT L∗ formula φ.
φ = AG(saf e(v)) ∧ EG(F meet1,2 (v)) ∧ EG(F meet2,3 (v)) ∧ EG(F meet1,3 (v)),
where the formula saf e(v) states that the three robots are not all in the same
position on the plane. Formula meeti,j (v) states that robot i and robot j are in
the same position1 .
   The first conjunct of φ ensures that the three robots are never in the same
position at the same time. The second conjunct ensures that for every pair of
robots, there is a path along which they meet infinitely often.
   Next, we demonstrate how to generate the set of EHCs for the verification
problem of R |= φ, using Trans.
   We first need to use rule 1 four times, one for each basic state subformula.
As the result, we get the following
      Clauses(R, φ) = Clauses(v, aux1 (v), next(v, v ′ ), ∅, AG(saf e(v))) ∪ . . .
             · · · ∪ Clauses(v, aux4 (v), next(v, v ′ ), ∅, EG(F meet2,3 (v)))∪
                 ∪Clauses(R, aux1 (v) ∧ aux2 (v) ∧ aux3 (v) ∧ aux4 (v))
The first set of clauses requires that in every state where aux1 (v) is true, sub-
formula AG(saf e(v)) is satisfied. Similar requirements are presented in the next
three sets. The last set guarantees that in the initial states of R all four auxi
predicates are satisfied.
    To deal with the first set we can use rule 2 to turn A to Af and then rule 4
to eliminate the temporal operator. This results in
Clauses(v∪{xG }, aux1 (v), next(v, v ′ )∧(xG = saf e(v)∧x′G ), {xG ∨¬saf e(v)}, Af xG ).
    Finally, we use rule 6 to get the explicit set of clauses. In the Appendix A.4
we explain why the resulting set of clauses is satisfiable.
    For the second, third and fourth sets, the generation of clauses is similar. We
present here only the fourth set of clauses.
    Rewrite the formula to replace F with U : EG(F meet2,3 (v)) =
EG(T rueU meet2,3 (v)). Next, apply rule 2 to turn E to Ef . Then apply rule 5
to eliminate the temporal operator U . This results in the following set of clauses.
                Clauses(v, aux4 (v), next(v, v ′ ), ∅, EG(F meet2,3 (v))) =
        = {aux4 (v) → ∃xU : aux5 (v, xU )} ∪ Clauses(v ∪ {xG }, aux5 (v, xU ),
      next(v, v ′ ) ∧ (xU = (meet2,3 (v) ∨ x′U )), {¬xU ∨ meet2,3 (v)}, EG(XU )).
As the last two steps, we apply rule 4 to eliminate the temporal operator G and
rule 7 to get the explicit set of clauses.
More details are given in the Appendix A.4.
1
    saf e(v) = (x1 6= x2 ) ∨ (x1 6= x3 ) ∨ (x2 6= x3 ) ∨ (y1 6= y2 ) ∨ (y1 6= y3 ) ∨ (y2 6= y3 ) and
    meeti,j (v) = (xi = xj ) ∧ (yi = yj ).


                                                 15
5     CT L∗ synthesis from partial programs
In this section, we investigate the problem of CT L∗ synthesis from partial pro-
grams, which include holes of two types – condition holes and assignment holes.
    As in the previous part, a program is presented as a transition system with
fairness conditions. Additionally, we have the variable pc, ranging over program
locations. The set of program variables is now presented as v = {pc} ∪ vr , where
vr is the set of all program variables except pc.
    A partial program is a pair hP, Hi, where P is a program and H is a finite
set of holes in P . There are two types of holes.
    A condition hole is a triple of locations hl, lt , lf i – the first element represents
the location where we would like to insert a condition. If this condition is satisfied
by a certain state at location l, then the synthesized program moves from location
l to location lt , otherwise, it moves to location lf .
    An assignment hole is a pair of locations hl, l′ i. In this case, we want to
synthesize an assignment in the form of a relation α(vr , vr′ ) over pairs of states
such that the synthesized program moves from location l to location l′ , assigning
variables according to α.
    A resolving function for a partial program hP, Hi is a function Ψ that maps
every condition hole to a subset of E |vr | , and every assignment hole to a subset
of E |vr | × E |vr | 2 , such that for every assignment hole hl, l′ i the following holds:
                                      ∀vr ∃vr′ : Ψ (hl, l′ i)(vr , vr′ )
.
   The constraint above characterizes a non-deterministic multiple assignment.
Using constraints to characterize the assignment holes gives us flexibility in
the synthesis. For example, we could alternatively require that the assignment
changes exactly one variable, while all others preserve their previous value.
   For a partial program hP, Hi and a resolving function Ψ the synthesized
program is a program PΨ = hv, init(v), nextΨ (v, v ′ ), J i, where
                      _
    nextΨ (v, v ′ ) =       (pc = l ∧ pc′ = lt ∧ Ψ (hl, lt , lf i)(vr ) ∧ vr′ = vr )∨
                          hl,lt ,lf i∈H
                 _
                             (pc = l ∧ pc′ = lf ∧ ¬Ψ (hl, lt , lf i)(vr ) ∧ vr′ = vr )∨
             hl,lt ,lf i∈H
                 _
                          (pc = l ∧ pc′ = l′ ∧ Ψ (hl, l′ i)(vr , vr′ )) ∨ next(v, v ′ ).
              hl,l′ i∈H

So basically PΨ is P with the holes filled according to Ψ .
    The CT L∗ synthesis problem is given a partial program hP, Hi and a
CT L∗ formula φ. A solution to the CT L∗ synthesis problem is a resolving func-
tion Ψ , such that the synthesized program PΨ satisfies φ. If such a resolving
function exists we say that the problem is realizable. Otherwise, the problem is
unrealizable.
2
    Recall that E is the domain over which interpretations are defined.


                                                     16
5.1      Reduction of CT L∗ synthesis to EHC satisfiability
Our goal is to generate a set of EHCs for a given synthesis problem, such that
the set of EHCs is satisfiable if and only if there is a solution to the synthesis
problem, exactly as we did for the verification problem.
     Actually, the verification problem is a special case of the synthesis problem,
so it is not surprising that we use an extension of our approach to CT L∗ ver-
ification to perform CT L∗ synthesis. The main idea of our algorithm is to fill
holes with uninterpreted predicates, apply our reduction for CT L∗ verification
and add some additional clauses to the resulted set of EHCs, in order to set
some constraints on uninterpreted predicates in holes.
     Formally, for a given synthesis problem consisting of a partial program hP, Hi
and a CT L∗ formula φ, we define the set of uninterpreted predicates U as follows:
U := {ucl(vr )|hl, lt , lf i ∈ H} ∪ {ual (vr , vr′ )|hl, l′ i ∈ H}.
     Basically, U contains a predicate over vr for every condition hole and a pred-
icate over vr , vr′ for every assignment hole.
     Intuitively, ucl and ¬ucl represent the sets of states from which the program
moves from l to lt and lf , respectively.
     The predicate ual intuitively represents the set of pairs of states s, s′ (with
locations l and l′ ), such that the program moves from s to s′ . We need to require
that for every state s in l there exists a state s′ in l′ , such that the program
moves from s to s′ . For that purpose, we introduce the following set of clauses
∆a (P, H) := {⊤ → ∃vr′ : ual (vr , vr′ ) | hl, l′ i ∈ H}.
     Let us define the program PU , which is the program P with holes filled with
uninterpreted predicates. Formally PU = hv, init(v), nextU (v, v ′ ), Ji, where
                                         _
    nextU (v, v ′ ) = next(v, v ′ ) ∨             (pc = l ∧ pc′ = lt ∧ ucl (vr ) ∧ vr′ = vr )∨
                                         hl,lt ,lf i∈H

        _                                                      _
∨                   (pc = l∧pc′ = lf ∧¬ucl (vr )∧vr′ = vr )∨           (pc = l∧pc′ = l′ ∧ual (vr , vr′ ))3 .
    hl,lt ,lf i∈H                                          hl,l′ i∈H

Finally, the desired set of clauses is ∆(P, H, φ) := ∆a (P, H) ∪ Clauses(PU , φ).

Theorem 4 (soundness). Suppose for a given CT L∗ synthesis problem
hP, H, φi, a set of clauses ∆(P, H, φ) produced by Trans is satisfiable by interpre-
tation I. Let Ψ be a resolving function for hP, Hi defined by:
    For every condition hole hl, lt , lf i ∈ H, Ψ (hl, lt , lf i)(vr ) = I(ucl )(vr ).
    For every assertion hole hl, l′ i ∈ H, Ψ (hl, l′ i)(vr , vr′ ) = I(ual )(vr , vr′ ).
Then PΨ satisfies φ.

Theorem 5 (Relative completeness). Given a realizable CT L∗ synthesis
problem hP, H, φi, then every set of clauses ∆(P, H, φ) produced by Trans is sat-
isfiable.

The proofs appear in the Appendix A.5.
3
    Recall that we can express the negation of a predicate using EHCs. See Section 2.1


                                                     17
6    Case study 2: Synthesizing a bank-client interaction

Suppose we would like to write a program that will determine the rules for an
ongoing interaction between a client and a bank. The goal is to define a process
that is satisfactory for both the client and the bank. Specifically, we would like
to complete the given sketch on Figure 2(a) according to a given specification
written as a CT L∗ formula (see below).
    The interaction between the client and the bank is an ongoing iterative pro-
cess, defined over the variables req (for request), bal (for balance), exp (for
expenses) and pro (for profit). At each iteration the client may request to ap-
ply either a withdrawal (in which case req ≥ 0) or a deposit (where req < 0)
to his account. bal represents the balance (amount of money) in the client’s ac-
count. exp represents the accumulative withdrawals made by the client up to this
iteration, and pro holds the profit accumulated by the bank up to this iteration.
    Initially, bal = exp = pro = 0.
    According to the sketch in Figure 2(a), after an unspecified check on line lc ,
on line l3 the client’s balance is updated according to req. Then the computation
is split to the case where request is a deposit (line la1 ) or a withdrawal (line l5 ).
In both cases the associated assignments are unspecified, but in the latter case,
exp is updated according to the current withdrawal. Finally, on line l6 the bank’s
profit is updated, decreasing it by $0.1, regardless of the action that has been
applied. This is because the bank has to transfer a fee of $0.1 to the central bank
on each transaction it makes.
    The CTL∗ specification formula φ is given as follows:

     φ = A(G(exp < 1000) ∨ F G(pro > 50)) ∧ EF ((exp ≥ 100) ∧ pro < 7).

    The first conjunct of φ requires that for every path either exp is always less
than $1000 or from some moment on, pro is greater than $50 forever. It assures
that if the amount of money withdrew by the client is sufficiently large, then pro
is also large.
    The second conjunct assures that the client can withdraw at least $100 from
his account, while not paying the bank more than $7.
    The entire φ ensures that the interaction between the client and the bank,
performed according to the synthesized program, is acceptable for the bank (first
conjunct) and for the client (second conjunct).
    Note that the first conjunct also implies that the fees of $0.1 transferred from
the bank to the central bank (line l6 ), are collected from the client. Otherwise,
the bank would not be able to maintain pro > 50, as it might lose profit on
client’s actions.
    The set of variables of B is v = {pc, req, bal, exp, pro}, the transition relation
is next(v, v ′ ) and the initial condition is init(v) = (bal = exp = pro = 0). The
set of holes is H = {lc , la1 , la2 }. We use Trans to generate the set of clauses
∆(B, H, φ) for the synthesis problem hB, H, φi.

                                          18
   The set of uninterpreted predicates is U = {uclc (vr ), uala (vr , vr′ ), uala (vr , vr′ )}.
                                                               1                 2
The program BU = hv, init(v), nextU (v), ∅i, where

                     nextU (v, v ′ ) = (pc = lc ∧ pc′ = l3 ∧ uclc (vr ) ∧ vr′ = vr )∨

                            ∨(pc = lc ∧ pc′ = l2 ∧ ¬uclc (vr ) ∧ vr′ = vr )∨
∨(pc = la1 ∧pc′ = l6 ∧uala1 (vr , vr′ ))∨(pc = la2 ∧pc′ = l6 ∧uala2 (vr , vr′ ))∨next(v, v ′ ).
By definition, ∆(B, H, φ) = ∆a (B, H) ∪ Clauses(BU , φ). Since we have two
assignment hole, ∆a (PT , H) = {⊤ → ∃vr′ : uala (vr , vr′ ), ⊤ → ∃vr′ : uala (vr , vr′ )}.
                                               1                            2
The holes can be filled as presented in Figure 2(b), resulting in program BS .


    l1 : while ( t r u e ) {                       l1 : while ( t r u e ) {
    l2 : r e q := ∗ ;                              l2 : r e q := ∗ ;
    lc : i f ( ?c ) {                              lc : i f ( b a l−r e q >= 0 . 1 ) {
    l3 :       b a l := b a l−r e q ;              l3 :       b a l := b a l−r e q ;
    l4 :       i f ( req < 0) {                    l4 :       i f ( req < 0) {
    la1 :           ?a1 ;                          la1 :            b a l := b a l − 0 . 1 ;
                                                                    pro := pro + 0 . 1 ;
                    } else {                                  } else {
    l5 :               exp := exp+r e q ;          l5 :             exp := exp+r e q ;
    la2 :              ?a2 ;                       la2 :            b a l := b a l −0.1 −0.06 r e q ;
                                                                    pro := pro +0.1+0.06 r e q ;
                    }                                         }
    l6 :            pro := pro − 0 . 1 ;           l6 :       pro := pro − 0 . 1 ;
                }                                         }
            }                                           }

            (a) Partial program B                         (b) Synthesized program BS
                           Fig. 2: Synthesizing bank-client interaction


    The synthesized condition on line lc assures that the client has enough money
to pay for his request and for the cost of transaction, $0.1, so that the bank would
not lose its profit.
    On lines la1 and la2 of BS the bank collects $0.1 from the client’s account.
Additionally, on line la2 the bank collects 6% of req, thus pro is at least 6% of
exp and it never decreases. The first conjunct of φ is then satisfied.
    To see that the second conjunct holds, consider a scenario in which the client
deposits $110 and then withdraws $100. After this transaction exp = $100 and
pro = $6. Hence, the second conjunct of φ is satisfied. Theorem 5 now guarantees
that the set ∆(B, H, φ) is satisfiable.


7     Conclusion
In this work, we exploit the power of EHCs for the verification and synthesis of
infinite-state programs with respect to CT L∗ specification. The algorithms are
both sound and relative complete. The relative completeness is based on semantic

                                                   19
interpretation that might not be expressible in a specific syntax. However, this
is the most general way to describe the desired interpretation. For synthesis,
for instance, when we conclude that the synthesis problem is unrealizable, then
indeed no suitable solution exists, regardless of the syntax.
    Our translation is independent of the solver or the underlying theory. If, in
the future, a new EHC solver for any theory is designed, it can be combined
with our translation system to perform CT L∗ verification and partial synthesis.




                                       20
References

 1. Beyene, T.A., Brockschmidt, M., Rybalchenko, A.: CTL+FO verification as con-
    straint solving (2014)
 2. Beyene, T.A., Chaudhuri, S., Popeea, C., Rybalchenko, A.: A constraint-based
    approach to solving games on infinite graphs. In: Jagannathan, S., Sewell, P.
    (eds.) The 41st Annual ACM SIGPLAN-SIGACT Symposium on Principles
    of Programming Languages, POPL ’14, San Diego, CA, USA, January 20-
    21, 2014. pp. 221–234. ACM (2014). https://doi.org/10.1145/2535838.2535860,
    https://doi.org/10.1145/2535838.2535860
 3. Beyene, T.A., Popeea, C., Rybalchenko, A.: Solving existentially quantified horn
    clauses. In: Sharygina, N., Veith, H. (eds.) Computer Aided Verification. pp. 869–
    882. Springer Berlin Heidelberg, Berlin, Heidelberg (2013)
 4. Beyene, T.A., Popeea, C., Rybalchenko, A.: Efficient CTL verification via horn
    constraints solving. In: Gallagher, J.P., Rümmer, P. (eds.) Proceedings 3rd Work-
    shop on Horn Clauses for Verification and Synthesis, HCVS@ETAPS 2016, Eind-
    hoven, The Netherlands, 3rd April 2016. EPTCS, vol. 219, pp. 1–14 (2016).
    https://doi.org/10.4204/EPTCS.219.1, https://doi.org/10.4204/EPTCS.219.1
 5. Bjørner, N., Gurfinkel, A., McMillan, K., Rybalchenko, A.: Horn Clause Solvers for
    Program Verification, pp. 24–51. Springer International Publishing, Cham (2015)
 6. Bjørner, N.S., McMillan, K.L., Rybalchenko, A.: On solving universally quan-
    tified horn clauses. In: Logozzo, F., Fähndrich, M. (eds.) Static Analy-
    sis - 20th International Symposium, SAS 2013, Seattle, WA, USA, June
    20-22, 2013. Proceedings. Lecture Notes in Computer Science, vol. 7935,
    pp. 105–125. Springer (2013). https://doi.org/10.1007/978-3-642-38856-9_8,
    https://doi.org/10.1007/978-3-642-38856-9_8
 7. Bloem, R., Schewe, S., Khalimov, A.: CTL* synthesis via LTL synthesis. Elec-
    tronic Proceedings in Theoretical Computer Science 260, 4–22 (Nov 2017).
    https://doi.org/10.4204/eptcs.260.4, http://dx.doi.org/10.4204/EPTCS.260.4
 8. Cook, B., Khlaaf, H., Piterman, N.: On automation of CTL* verification for
    infinite-state systems. In: Kroening, D., Păsăreanu, C.S. (eds.) Computer Aided
    Verification. pp. 13–29. Springer International Publishing, Cham (2015)
 9. Cook, B., Podelski, A., Rybalchenko, A.: Terminator: Beyond safety. In: Ball, T.,
    Jones, R.B. (eds.) Computer Aided Verification. pp. 415–418. Springer Berlin Hei-
    delberg, Berlin, Heidelberg (2006)
10. Dam, M.: CTL∗ and ECTL∗ as fragments of the modal µ-
    calculus.     Theoretical    Computer       Science    126(1),     77–96    (1994).
    https://doi.org/https://doi.org/10.1016/0304-3975(94)90269-0,
    https://www.sciencedirect.com/science/article/pii/0304397594902690
11. Finkbeiner, B.: Synthesis of reactive systems, pp. 72–98 (04 2016).
    https://doi.org/10.3233/978-1-61499-627-9-72
12. Gulwani, S., Polozov, O., Singh, R.: Program synthesis. Founda-
    tions and Trends® in Programming Languages 4(1-2), 1–119 (2017).
    https://doi.org/10.1561/2500000010, http://dx.doi.org/10.1561/2500000010
13. Guo, D., Svyatkovskiy, A., Yin, J., Duan, N., Brockschmidt, M., Allamanis, M.:
    Learning to complete code with sketches (2022)
14. Kesten, Y., Pnueli, A.: A compositional approach to CTL* ver-
    ification. Theoretical Computer Science 331, 397–428 (02 2005).
    https://doi.org/10.1016/j.tcs.2004.09.023


                                          21
15. Khalimov, A., Bloem, R.: Bounded synthesis for Streett, Rabin, and CTL*.
    In: Majumdar, R., Kuncak, V. (eds.) Computer Aided Verification - 29th In-
    ternational Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017,
    Proceedings, Part II. Lecture Notes in Computer Science, vol. 10427,
    pp. 333–352. Springer (2017). https://doi.org/10.1007/978-3-319-63390-9_18,
    https://doi.org/10.1007/978-3-319-63390-9_18
16. Kupferman,        O.,    Vardi,     M.Y.,       Wolper,     P.:    An     automata-
    theoretic     approach    to    branching-time      model    checking.    J.    ACM
    47(2),         312–360       (2000).         https://doi.org/10.1145/333979.333987,
    https://doi.org/10.1145/333979.333987
17. Long, F., Rinard, M.: Staged program repair with condition synthesis. pp. 166–178
    (08 2015). https://doi.org/10.1145/2786805.2786811
18. Niwiński, D., Walukiewicz, I.: Games for the µ-calculus. Theoretical Computer
    Science 163(1-2), 99–116 (1996)
19. Podelski, A., Rybalchenko, A.: Transition invariants. In: Proceedings of the 19th
    Annual IEEE Symposium on Logic in Computer Science, 2004. pp. 32–41 (2004).
    https://doi.org/10.1109/LICS.2004.1319598
20. Rothenberg, B.C., Grumberg, O., Vizel, Y., Singher, E.: Condition synthesis real-
    izability via constrained horn clauses. In: Rozier, K.Y., Chaudhuri, S. (eds.) NASA
    Formal Methods. pp. 380–396. Springer Nature Switzerland, Cham (2023)
21. Solar-Lezama, A., Tancau, L., Bodik, R., Seshia, S., Saraswat, V.: Com-
    binatorial sketching for finite programs. SIGARCH Comput. Archit.
    News 34(5), 404–415 (oct 2006). https://doi.org/10.1145/1168919.1168907,
    https://doi.org/10.1145/1168919.1168907
22. Srivastava, S., Gulwani, S., Foster, J.S.: Template-based program verification and
    program synthesis. International Journal on Software Tools for Technology Transfer
    15(5), 497–518 (January 2012)
23. Unno, H., Terauchi, T., Gu, Y., Koskinen, E.: Modular primal-dual fixpoint logic
    solving for temporal verification. Proc. ACM Program. Lang. 7(POPL) (jan 2023).
    https://doi.org/10.1145/3571265, https://doi.org/10.1145/3571265
24. Unno, H., Terauchi, T., Koskinen, E.: Constraint-based relational verification. In:
    Silva, A., Leino, K.R.M. (eds.) Computer Aided Verification. pp. 742–766. Springer
    International Publishing, Cham (2021)
25. Xiong, Y., Wang, J., Yan, R., Zhang, J., Han, S., Huang, G., Zhang, L.:
    Precise condition synthesis for program repair. In: 2017 IEEE/ACM 39th In-
    ternational Conference on Software Engineering (ICSE). pp. 416–426 (2017).
    https://doi.org/10.1109/ICSE.2017.45
26. Xuan, J., Martinez, M., DeMarco, F., Clement, M., Marcote, S.L.,
    Durieux, T., Le Berre, D., Monperrus, M.: Nopol: Automatic repair
    of conditional statement bugs in java programs. IEEE Trans. Softw.
    Eng. 43(1), 34–55 (jan 2017). https://doi.org/10.1109/TSE.2016.2560811,
    https://doi.org/10.1109/TSE.2016.2560811




                                          22
A     Appendix

A.1    Proof of complexity theorem

Theorem 6 (complexity). Let (D, φ) be a verification problem, with a pro-
gram of size m, with k fairness conditions, and a specification formula of size
n. Then Trans produces a set Clauses(v, init(v), next(v, v ′ ), J, φ) consisting of
O(n(n + k)) clauses with a total size of O(n(n + k)(n + m)).

Proof. At first, we prove that in the case when φ is a basic state formula, the
number of clauses and the overall size are O(n + k) and O((n + k)(n + m))
respectively. At the end of the generation process Trans applies rule 6 or rule 7.
Rule 6 produces constant number of clauses, rule 7 produces O(k) clauses and
in both cases overall size is O(n + mk).
    Before the last step Trans applies rules 3, 4 and 5, replacing assertions inside
the formula with boolean variables and extending the set of fairness conditions
(by one element on each step) and transition relation (linearly from the size
of the replaced assertion). Hence, by the last step of the algorithm, the sizes
of the set of fairness constraints and the program are O(n + k) and O(n + m)
respectively, hence the number of the clauses in the resulting set and the overall
size are O(n + k) and O((n + k)(n + m)). Also, during the implication of rules 3,
4 and 5 Trans may produce one clause per step of the size m, hence not more
than n clauses with overall size n(n + m).
    Rule 2 makes a recursive call of Clauses for the problem of the same size,
hence the bounds are preserved.
    To deal with the case of non-basic specification formula φ we need to examine
Rule 1. It takes a state basic subformula of the specification formula of the size l
and makes two recursive calls. One for the problem with sizes of the parameters
m, n − l, k and one for the problem with sizes of the parameters m, l, k and with
the basic state specification formula. Eventually, after numerous implications of
rule 1 Trans reduces our problem to not more than n subproblems with the same
sizes of program and the set of fairness constraints and smaller specification
state formulas. Hence, Trans produces O(n(n + k)) clauses with the overall size
O(n(n + k)(n + m)).                                                                ⊓
                                                                                   ⊔


A.2    Full proof of soundness theorem

Theorem 7 (soundness).
   For      every     set        of     clauses     produced       by    Trans    for
Clauses(v, init(v), next(v, v ′ ), J, φ), if the set is satisfiable then the program
D = (v, init(v), next(v, v ′ ), J) satisfies φ.

Proof. We prove the theorem by induction on the size of the formula φ. Recall
that by definition, CTL∗ formulas are state formulas. As such, they are true in
a program D if all initial states of D satisfy the formula. That is, init(v) → φ.
We will use this fact in the proof.

                                         23
Base: Rule 8 forms the basis of the induction. For an assertion c in T ,
Clauses(D, c) = {init(v) → c(v)}. If this set of clauses is satisfiable then, by
definition of CTL∗ satisfiability, D |= c.
Induction step:
Rule 1:
Assume a set of clauses Clauses(D, φ2 (φ1 )) is satisfiable by an interpretation I.
Then, I satisfies Clauses(v, aux(v), next(v, v ′ ), J, φ1 ) and by the induction hy-
pothesis, (v, I(aux)(v), next(v, v ′ ), J) |= φ1 . Thus, I(aux)(v) → φ1 . Also, I sat-
isfies Clauses(D, φ2 (aux)(v)) and by the induction hypothesis D |= φ2 (I(aux)).
Since φ2 is in Negation Normal Form (NNF), replacing all occurrences of I(aux)
in φ2 with φ1 results in a formula that is also true in D. We thus conclude that
D |= φ2 (φ1 ), as required.
Rule 2:
Since the formula Qφ does not depend on the fairness conditions,
(v, init(v), next(v, v ′ ), J) |= Qφ iff (v, init(v), next(v, v ′ ), ∅) |= Qf φ.
    Assume by way of contradiction that a set of clauses produced
by Trans for Clauses(v, init(v), next(v, v ′ ), J, Qφ) is satisfiable but
(v, init(v), next(v, v ′ ), J) 6|= Qφ. Then (v, init(v), next(v, v ′ ), ∅) 6|= Qf φ.
By the induction hypothesis, since we consider Qf φ to be smaller than Qφ, ev-
ery set of clauses produced by Trans for Clauses(v, init(v), next(v, v ′ ), ∅, Qf φ) is
unsatisfiable. Recall that Rule 2 defines Clauses(v, init(v), next(v, v ′ ), J, Qφ) =
Clauses(v, init(v), next(v, v ′ ), ∅, Qf φ). Consequently, every set of clauses
produced by Trans for Clauses(v, init(v), next(v, v ′ ), J, Qφ) is unsatisfiable as
well. A contradiction.
We partition the proof for each of the rules 3, 4 and 5 into two cases – universal
and existential quantifiers.
Rule 3, Universal:
We prove here that if D = (v, init(v), next(v, v ′ ), J) does not satisfy
Af φ(Xc) then for every set of clauses, produced by Trans for Clauses(v ∪
{xX }, init(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J, Af φ(xX )), the set is unsatisfiable.
     Suppose D does not satisfy Af φ(Xc). Then there is a fair path π = s1 , s2 , . . .
such that D, s1 |= init(v) and D, π 6|= φ(Xc).
     Consider the path πX = s′1 , s′2 , . . . of the program DX = (v ∪
{xX }, init(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J), where s′i (v) = si (v) and s′i (xX ) =
si+1 (c(v)). πX is a fair path of DX , since the fairness conditions of D and
DX are identical and defined only over v (and not over xX ). In addition,
DX , πX 6|= φ(xX ), since xX and Xc are true on exactly the same locations
of the paths πX and π, respectively.
     Hence, DX does not satisfy Af φ(xX ). By the induction hypothesis, for every
set of clauses produced by Trans for Clauses(v∪{xX }, init(v), next(v, v ′ )∧(xX =
c(v ′ )), J, Af φ(xX )), the set is unsatisfiable, as required.
Rule 3, Existential:
Denote D     =    (v, init(v), next(v, v ′ ), J).     Suppose     a    set   of   clauses

                                           24
Clauses(D, Ef φ(Xc)) = Clauses(v ∪ {xX }, aux(v, xX ), next(v, v ′ ) ∧ (xX =
c(v ′ )), J, Ef φ(xX )) ∪ {init(v) → ∃xX : aux(v, xX )} is satisfied by interpreta-
tion I.
     Denote DX = (v ∪ {xX }, I(aux)(v, xX ), next(v, v ′ ) ∧ (xX = c(v ′ )), J). By the
induction hypothesis, DX |= Ef φ(xX ).
     Let s be a state of D such that D, s |= init(v). Since the clause init(v) →
∃xX : I(aux)(v, xX ) is true, there is a state sX of DX , such that sX (v) = s(v)
and DX , sX |= I(aux)(v, xX ). Thus, there is a fair path πX = sX , sX               X
                                                                                2 , s3 , . . .
of DX such that DX , πX |= φ(xX ). Consider the path of D defined as π =
s, s2 , s3 , . . . , where each si is the restriction of sX
                                                          i to the variables from v. Then
D, π |= φ(Xc). This is because xX and Xc are true on exactly the same locations
of the paths πX and π, respectively. We conclude that D |= Ef φ(Xc).

Rule 4, Universal:
Suppose D = (v, init(v), next(v, v ′ ), J) does not satisfy Af φ(Gc). Then there is
a fair path π = s1 , s2 , . . . such that D, s1 |= init(v) and D, π 6|= φ(Gc).
    Consider the path πG = s′1 , s′2 , . . . of the program DG = (v ∪
{xG }, init(v), next(v, v ′ )∧(xG = c(v)∧x′G ), J ∪{xG ∨¬c(v)}), where s′i (v) = si (v)
and s′i (xG ) = true iff for every j ≥ i : s′j |= c(v). Note that, once xG is set to
true on πG , c(v) is set to true. Moreover, they both remain true forever from
that point on.
    πG is a fair path of DG since the fairness conditions of D do not depend on
xG . The additional fairness condition of DG holds as well, since if c(v) holds from
a certain point on along πG then xG holds from that point on. Thus, xG ∨ ¬c(v)
holds infinitely often along πG .
    Also DG , πG 6|= φ(xG ), since xG is true on the same locations of path πG as
the locations of π where Gc is true.
    Hence, DG does not satisfy Af φ(xG ). By the induction hypothesis, every set
of clauses produced by Trans for Clauses(DG , Af φ(xX )) is unsatisfiable. Since
Closes(D, Af φ(Gc)) = Clauses(DG , Af φ(xX )), this implies that every set of
clauses produced by Trans for Closes(D, Af φ(Gc)) is unsatisfiable, as required.

Rule 4, Existential:
Suppose a set Clauses(v, init(v), next(v, v ′ ), J, Ef φ(Gc)) is satisfied by inter-
pretation I. Denote DG = (v ∪ {xG }, I(aux)(v, xG ), next(v, v ′ ) ∧ (xG = c(v) ∧
x′G ), J ∪ {xG ∨ ¬c(v)}). Then, by Rule 4, Clauses(DG , Ef φ(xG )) is also satisfied
by I. By the induction hypothesis DG |= Ef φ(xG ).
     Let s be a state of D = (v, init(v), next(v, v ′ ), J), such that D, s |= init(v).
Since the clause {init(v) → ∃xG : aux(v, xG )} is satisfied by interpretation
I, then there is a state sG of DG such that sG (v) = s(v) and DG , sG |=
I(aux)(v, xG ). Moreover, there is a fair path πG = sG , s′2 , s′3 , . . . of DG such
that DG , πG |= φ(xG ). Consider the path of D defined by π = s, s2 , s3 . . . , where
si (v) is a restriction of s′i to the variables from v. Then D, π |= φ(Gc). This is
because xG is true on the same places of the path πG as the places of π where
Gc is true. Moreover, π is a fair path. Thus, D satisfies Ef φ(Gc).

                                             25
Rule 5, Universal:
Suppose D = (v, init(v), next(v, v ′ ), J) does not satisfy Af φ(c1 U c2 ), then there
is a fair path π = s1 , s2 , . . . , such that D, s1 |= init(v) and D, π 6|= φ(c1 U c2 ).
      Consider the path πU = s′1 , s′2 , . . . of the program DU = (v ∪
{xU }, init(v), next(v, v ′ ) ∧ (xU = c2 (v) ∨ (c1 (v) ∧ x′U )), J ∪ {¬xU ∨ c2 (v)}), where
s′i (v) = si (v) and s′i (xU ) = true iff π i satisfies c1 U c2 . πU is a fair path of DU
since the fairness conditions from D do not depend on the evaluation of xU . Fur-
ther, if xU is true from a certain point on along πU , then c2 must hold infinitely
often. Thus, πU satisfies the additional fairness condition as well.
      Also DU , πU 6|= φ(xU ), since xU is true on the same places of the path πU as
the places of π where c1 U c2 is true.
      Hence DU does not satisfy Af φ(xU ). By the induction hypothesis, every
clause produced by Trans for Clauses(v∪{xU }, init(v), next(v, v ′ )∧(xU = c2 (v)∨
(c1 (v) ∧ x′U )), J ∪ {¬xU ∨ c2 (x)}, Af φ(xU )) is unsatisfiable, as required.
Rule 5, Existential:
Suppose a set Clauses(v, init(v), next(v, v ′ ), J, Ef φ(c1U c2)) is satisfied by in-
terpretation I.
   Denote DU = (v ∪ {xU }, init(v), next(v, v ′ ) ∧ (xU = c2 (v) ∨ (c1 (v) ∧ x′U )), J ∪
{¬xU ∨ c2 (x)}). By the induction hypothesis DU |= Ef φ(xU ).
   Let s be a state of D = (v, init(v), next(v, v ′ ), J), such that D, s |= init(v).
Since the clause {init(v) → ∃xX : aux(v, xG )} is satisfied by interpretation
I, then there is a state sU of DU such that sU (v) = s(v) and DU , sU |=
I(aux)(v, xU ). Moreover, there is a fair path πU = sU , s′2 , s′3 , . . . of DU such
that DU , πU |= φ(xU ). Consider the path of D defined by π = s, s2 , s3 , . . . ,
where si is the restriction of s′i to the variables from v.
   Then D, π |= φ(c1 U c2 ) since xU is true on the same places of path πU as the
places of π where c1 U c2 is true. Hence, D satisfies Ef φ(c1 U c2 ).
Rule 6:
Denote D = (v, init(v), next(v, v ′ ), J). Suppose by way of contradiction that a
set Clauses(D, Af c) is satisfied by an interpretation I but the program D does
not satisfy the formula Af c. Then, there is a fair path π = s0 , s1 , s2 , . . . , such
that D, s0 |= init(v) and D, π 6|= c.
    By the clauses init(v) ∧ ¬c(v) → I(p)(v), next(v, v ′ ) ∧ I(p)(v) → I(p)(v ′ ) we
know that for every i : si |= I(p)(v).
    Since π is fair, each Jj holds infinitely often along π. Moreover, there is an
infinite increasing sequence of indexes 0 < i1 < i2 < i3 <, . . . , such that for
every k : sik |= Jk%|J|+1 .
                                      V|J|
    By the clause I(p)(v0 ) ∧ i=1 (I(t)(vi−1 , vi ) ∧ Ji (vi )) → I(r)(v0 , v|J| ) we get
that sin1 |J| , sin2 |J| |= r(v, v ′ ) for every pair of natural numbers n1 , n2 , provided
n1 < n2 . Thus, I(r), which is disjunctive well-founded, contains an infinite tran-
sitive chain, but that is impossible due to Theorem 1 from [19]. A contradiction.
Rule 7:
Suppose a set of clauses Clauses(v, init(v), next(v, v ′ ), J, Ef c) is satisfied by
interpretation I.

                                            26
    Denote D = (v, init(v), next(v, v ′ ), J). In order to prove that D satisfies Ef c
we need to show that every state that satisfies init(v) also satisfies c(v) and is a
start of a fair path.
    Suppose for some state s of D, s |= init(v), then by clause init(v) → c(v) ∧
I(q1 )(v) we have s |= c(v) and s |= I(q1 )(v).
    By clauses {dwf (I(ri )), I(ri )(v, v ′ ) ∧ I(ri )(v ′ , v ′′ ) → I(ri )(v ′ , v ′′ ) | i ≤ |J|}
we know that for every i ≤ |J|, relation I(ri ) is disjunctively well-founded and
transitive, hence it is a well-founded relation by Theorem 1 from [19].
    For every i ≤ |J|, by clause I(qi )(v) → ∃v ′ : next(v, v ′ ) ∧ ((Ji (v ′ ) ∧
I(q(i%|J|)+1 )(v ′ )) ∨ (I(ri )(v, v ′ ) ∧ I(qi )(v ′ ))) and the fact that I(ri ) is a well-
founded relation we can conclude that for every state t of D if t |= I(qi )(v) then
there is a path in D from t to some state t′ such that t′ |= Ji (v) and there is a
transition from t′ to some state t′′ such that t′′ |= I(q(i%|J|)+1 )(v).
    Thus, there is a fair path, that starts in s.                                                 ⊓
                                                                                                  ⊔


A.3     Full proof of relative completeness

Next we show that Trans is relative complete. Relative completeness means that
if a verification problem holds, that is, the program meets the specification, then
every set of clauses, produced by Trans for that problem, must be satisfied by
some interpretation of the uninterpreted predicates. However, this interpretation
is not necessarily expressible by a first-order formula in our logic.

Theorem 8 (relative completeness). If D = (v, init(v), next(v, v ′ ), J) satis-
fies φ then every set produced by Trans for Clauses(D, φ) is satisfiable by some
interpretation of the uninterpreted predicate symbols.

Proof. We prove the theorem by induction on the size of the verified formula.
Base: Rule 8 forms the basis of the induction. For assertion c in T , if D |=
c then Clauses(D, c) = {init(v) → c(v)} is satisfiable by definition of CTL∗
satisfiability.
Induction step:
Rule 1:
Assume D |= φ2 (φ1 ). For the uninterpreted predicate aux, we choose as inter-
pretation the predicate I(aux), which is true in exactly those states where φ1 is
true. Then, (v, I(aux)(v), next(v, v ′ ), J) meets φ1 and (v, init(v), next(v, v ′ ), J)
meets φ2 (I(aux)). By the induction hypothesis, the corresponding sets of clauses
are satisfiable. Consequently, Clauses(D, φ1 (φ2 )) is satisfiable.
Rule 2:
Since this verification problem does not depend on the fairness conditions, the
following holds: (v, init(v), next(v, v ′ ), J) |= Qφ iff (v, init(v), next(v, v ′ ), ∅) |=
Qφ iff (v, init(v), next(v, v ′ ), ∅) |= Qf φ. By the induction hypothesis (since
we consider Qf φ to be smaller than Qφ), every set of clauses produced by
Trans for Clauses(v, init(v), next(v, v ′ ), ∅, Qf φ) is satisfiable. The same holds
for Clauses(v, init(v), next(v, v ′ ), J , Qφ), since by Rule 2 is identical.

                                                27
We partition the proof for each of the rules 3, 4 and 5 into two cases – universal
and existential quantifiers.
Rule 3, Universal:
If D = (v, init(v), next(v, v ′ ), J) meets Af φ(Xc), then DX = (v ∪
{xX }, init(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J) meets Af φ(xX ). This is because
for every fair path of DX , the formula xX is true in the exact the same places
where Xc is true on the corresponding path of D. By the induction hypothesis,
every set of clauses produced by Trans for Clauses(DX , Af φ(xX )) is satisfiable.
Consequently, every set of clauses produced by Trans for Clauses(D, Af φ(Xc))
is satisfiable, as required.
Rule 3, Existential:
Assume D = (v, init(v), next(v, v ′ ), J) satisfies Ef φ(Xc). We need to prove that
every set of clauses produce by Trans for Clauses(D, Ef φ(Xc)) = Clauses(v ∪
{xX }, aux(v, xX ), next(v, v ′ ) ∧ (xX = c(v ′ )), J, Ef φ(xX )) ∪ {init(v) → ∃xX :
aux(v, xX )} is satisfiable.
    For DX = (v ∪ {xX }, I(aux)(v), next(v, v ′ ) ∧ (xX = c(v ′ )), J), we choose
the predicate I(aux), which is true in exactly those states of DX that satisfy
Ef φ(xX ).
    Clearly, DX satisfies Ef φ(xX ). By the induction hypothesis, every set of
clauses produced by Trans for Clauses(DX , Ef φ(xX )) is satisfiable.
    For every fair path of DX , the variable xX is true in exactly the same places
where Xc is true on the corresponding fair path of D.
    Hence, init(v) → ∃xX I(aux)(v, xX ), because if s |= init(v) is true for some
state s of D, then there is a fair path π, starting at s that satisfies φ(Xc).
Hence, if Xc is true on π, then s |= I(aux)(v, 1) and if Xc is false on π then
s |= I(aux)(v, 0).
    Thus, for every set of clauses produced by Trans for Clauses(v ∪
{xX }, aux(v, xX ), next(v, v ′ ) ∧ (xX = c(v ′ )), J, Ef φ(xX )) ∪ {init(v) → ∃xX :
aux(v, xX )}, we defined an interpretation that satisfy this set.
The two cases for rules 4 and 5 can be proved similarly to Rule 3 and are omitted.
Rule 6:
Suppose the program D = (v, init(v), next(v, v ′ ), J) satisfies Af c. Recall that,
D |= Af c implies that every initial state of D either satisfies c or has no fair
path starting in it. We define an interpretation I as follows:
 – s |= I(p)(v) iff there is no fair path starting at s.
 – s, s′ |= I(t)(v, v ′ ) iff there is a path from s to s′ .
 – s, s′ |= I(r)(v, v ′ ) if s |= I(p)(v), s′ |= J|J| (v ′ ) and there is a path from s
   to s′ which visits a state satisfying J1 , then a state satisfying J2 and so on
   until it ends in s′ that satisfies J|J| .
For every set of state s, s′ , s′′ , s0 , . . . , s|J| of D, we check that all clauses defined
by Rule 6 are satisfied by I.
 – s |= init(v) ∧ ¬c(v) → I(p)(v), because if an initial state does not satisfy c,
   then there is no fair path that starts in it. This is because D satisfies Af c.

                                             28
 – s, s′ |= next(v, v ′ ) ∧ I(p)(v) → I(p)(v ′ ), because if there is no fair path that
   starts in s and there is a transition from s to s′ , then there is no fair path
   that starts in s′ .             V
 – s0 , . . . , s|J| |= I(p)(v0 ) ∧ |J|
                                    i=1 (t(vi−1 , vi ) ∧ Ji (vi )) → I(r)(v0 , v|J| ) by defini-
   tion of I(r).
 – s, s′ |= next(v, v) → I(t)(v, v ′ ) and s, s′ , s′′ |= next(v, v ′ ) ∧ I(t)(v ′ , v ′′ ) →
   I(t)(v, v ′′ ), since I(t) is the transitive closure of next.
 – Relation I(r) is well-founded, since if there was an infinite chain of I(r),
   then this chain would represent a fair path on states satisfying I(p). But
   such states cannot occur on fair paths. Hence dwf (I(r)).
This concludes the proof of relative completeness for Rule 6.
Rule 7:
Suppose the program D = (v, init(v), next(v, v ′ ), J) satisfies Ef c. This means
that every initial state s of D satisfies c, and, in addition, s is the start of a fair
path. We say that a state s of D is fair if there is a fair path starting at s. We
define the interpretation I as follows. For every i ∈ {1, . . . , |J|}:

 – s |= I(qi )(v) iff s is a fair state.
 – s, s′ |= I(ri )(v, v ′ ) iff s′ is a fair state and s satisfies Ji or s′ is the successor
   of s on the shortest path π leading from s to a fair state s′′ satisfying Ji .

For every two states s, s′ in D, we check that the clauses defined by Rule 7 are
satisfied by I.
 – s |= init(v) → c(v) ∧ I(q1 )(v) since for every initial state s, c(v) holds in s
   and there is a fair path starting at s. That is, s is fair.
 – s |= I(qi )(v) → ∃v ′ : next(v, v ′ ) ∧ ((Ji (v) ∧ I(q(i%|J|)+1 )(v ′ )) ∨ (I(ri )(v, v ′ ) ∧
   I(qi )(v ′ ))). This is because if s |= I(qi )(v), then s is a fair state. On a fair
   path every Jj holds infinitely often. Thus, either Ji (v) holds in s or there is
   a shortest path π from s to a fair state where Ji holds.
   In the first case we define s′ as the successor of s on a fair path. In the
   second case we define s′ as the successor of s on π. Hence, we either have
   s |= Ji (v) and s′ |= I(q(i%|J|)+1 )(v ′ ) (this is because fair states satisfy all qj )
   or s′ |= I(qi )(v) and s, s′ |= I(ri )(v, v ′ ).
 – s |= I(ri )(v, v ′ ) ∧ I(ri )(v ′ , v ′′ ) → I(ri )(v, v ′′ ), since the relation is transitive
   by definition.
 – I(ri ) is a well-founded relation because if on each step we move to a state,
   which is closer along the shortest path to a state satisfying (Ji ∧ q(i%|J|)+1 ),
   we will eventually get to such a state. Hence dwf (I(ri )).
This concludes the proof of relative completeness for Rule 7.                                   ⊓
                                                                                                ⊔

A.4    Case study 1: CTL∗ verification of user-robots system
Let us demonstrate how we generate the set of EHCs for the verification problem
of R |= φ using Trans.

                                               29
   We need to use rule 1 four times, one for each basic state subformula. As the
result, we get the following


       Clauses(R, φ) = Clauses(v, aux1 (v), next(v, v ′ ), ∅, AG(saf e(v)))∪

              ∪Clauses(v, aux2 (v), next(v, v ′ ), ∅, EG(F meet1,2 (v)))∪
              ∪Clauses(v, aux3 (v), next(v, v ′ ), ∅, EG(F meet1,3 (v)))∪
              ∪Clauses(v, aux4 (v), next(v, v ′ ), ∅, EG(F meet2,3 (v)))∪
                ∪Clauses(R, aux1 (v) ∧ aux2 (v) ∧ aux3 (v) ∧ aux4 (v))
    The first set requires that in every state where aux1 (v) is true, subformula
AG(saf e(v)) is satisfied. Similar requirements are presented in the next three
sets. The last set guarantees that in the initial states of R all four auxi predicates
are satisfied.
    To deal with the first set we can use rule 2 to turn A to Af and then rule 4
to eliminate the temporal operator. Finally, we get the following result.

                  Clauses(v, aux1 (v), next(v, v ′ ), ∅, AG(saf e(v))) =

        = Clauses(v ∪ {xG }, aux1 (v), next(v, v ′ ) ∧ (xG = saf e(v) ∧ x′G ),

                                   {xG ∨ ¬saf e(v)}, Af xG ).
   Now we need to use rule 6 to get the explicit set of clauses.


Clauses(v∪{xG }, aux1 (v), next(v, v ′ )∧(xG = saf e(v)∧x′G ), {xG ∨¬saf e(v)}, Af xG ) =

= {aux1 (v)∧¬xG → p(v, xG ), next(v, v ′ )∧(xG = saf e(v)∧x′G )∧p(v, xG ) → p(v ′ , x′G ),
         p(v, xG ) ∧ t(v, xG , v ′ , x′G ) ∧ (x′G ∨ ¬saf e(v ′ )) → r(v, xG , v ′ , x′G ),
          dwf (r), next(v, v ′ ) ∧ (xG = saf e(v) ∧ x′G ) → t(v, xG , v ′ , x′G ),
   t(v, xG , v ′ , x′G ) ∧ next(v ′ , v ′′ ) ∧ (x′G = saf e(v ′ ) ∧ x′′G ) → t(v, xG , v ′′ , x′′G )}.
    The resulting set of clauses guarantees that aux1 (v) is evaluated in such a
way that from every state in which aux1 (v) is true, the user cannot direct three
robots to the same point at the same time (since saf e(V ) holds).
    Next, we explain informally why the set of clauses above is satisfiable. Sup-
pose from a state s the user can apply a sequence of moves so that eventually
all three robots arrive at position (x; y). Hence y = s(y1 ), since the second co-
ordination of robot 1 cannot be changed. For the second and third robots the
sums 2x2 + y2 and x3 + y3 cannot be changed. Hence

                          2x + s(y1 ) = 2x + y = 2s(x2 ) + s(y2 ),

                               x = (2s(x2 ) + s(y2 ) − s(y1 ))/2

                                                  30
and from the condition for the last robot, we need to have (2s(x2 ) + s(y2 ) −
s(y1 ))/2 + s(y1 ) = s(x3 ) + s(y3 ). By these equations, we can conclude that
aux1 (v) can be evaluated as
                           ((2x2 + y2 + y1 )/2) 6= x3 + y3
and init(v) implies this condition.
    For the second, third and fourth sets the generation of clauses in similar. We
will look only at the fourth set.
    Let us rewrite the formula to replace F with U .
                    EG(F meet2,3 (v)) = EG(T rueU meet2,3 (v))
First, we need to apply rule 2 to turn E to Ef . Then we need to apply rule 5 to
eliminate the temporal operator U .
           Clauses(v, aux4 (v), next(v, v ′ ), ∅, EG(T rueU meet2,3(v))) =
                        = {aux4 (v) → ∃xU : aux5 (v, xU )}∪
      ∪Clauses(v ∪ {xG }, aux5 (v, xU ), next(v, v ′ ) ∧ (xU = meet2,3 (v) ∨ x′U ,
                           {¬xU ∨ meet2,3 (v)}, EG(XU ))
   As the last two steps, we need to apply rule 4 to eliminate the temporal
operator G and rule 7 to get the explicit set of clauses.

A.5    Soundness and completeness of CT L∗ synthesis
Theorem 9 (soundness). Suppose for a given CT L∗ synthesis problem
hP, H, φi, a set of clauses ∆(P, H, φ) produced by Trans is satisfiable by interpre-
tation I. Let Ψ be a resolving function for hP, Hi defined by:
    For every condition hole hl, lt , lf i ∈ H, Ψ (hl, lt , lf i)(vr ) = I(ucl )(vr ).
    For every assertion hole hl, l′ i ∈ H, Ψ (hl, l′ i)(vr , vr′ ) = I(ual )(vr , vr′ ).
Then PΨ satisfies φ.
Proof. First, we check that Ψ is a resolving function. That is, for every assign-
ment hole hl, l′ i ∈ H, the formula ∀vr ∃vr′ : Ψ (hl, l′ i)(vr , vr′ ) is true. But this
follows from the fact that interpretation I satisfies clauses ∆a (P, H).
    Next, we partition I to I1 and I2 , where I1 is a restriction of I to the set of
predicates U and I2 is restricted to the predicates not in U .
    We denote by I1 (nextU ) the formula nextU , in which every predicate ucl or
  a
ul is interpreted according to I1 . Note that, by definition of nextU , nextΨ and
Ψ , we get I1 (nextU )(v, v ′ ) = nextΨ (v, v ′ ). Similarly, we denote by I1 (PU ) the
program PU , in which the transition relation nextU is replaced by its interpreted
version I1 (nextU ). Note that, I1 (PU ) = PΨ .
    Applying I1 to the predicates inside Clauses(PU , φ) we get
          I1 (Clauses(PU , φ)) = Clauses(I1 (PU ), φ) = Clauses(PΨ , φ).
Since the set Clauses(PU , φ) is satisfied by interpretation I and I = I1 ∪I2 , then
Clauses(PΨ , φ) = I1 (Clauses(PU , φ)) is satisfied by I2 . Thus, by Theorem 2 the
program PΨ satisfies φ, as required.                                               ⊓
                                                                                   ⊔

                                          31
Theorem 10 (Relative completeness). Given a realizable CT L∗ synthe-
sis problem hP, H, φi, then every set of clauses ∆(P, H, φ) produced by Trans is
satisfiable.

Proof. Suppose hP, H, φi is realizable by resolving function Ψ .
As before, we partition the satisfying interpretation I that we would like to define
into two interpretations, I1 and I2 , where the first interprets the predicates from
U and the second interprets the rest. We define interpretation I1 on U as follows:
    For every condition hole hl, lt , lf i ∈ H, I1 (ucl )(vr ) := Ψ (hl, lt , lf i)(vr ).
    For every assertion hole hl, l′ i ∈ H, I1 (ual )(vr , vr′ ) := Ψ (hl, l′ i)(vr , vr′ ).
    We adopt the notations of I1 (nextU ), I1 (PU ) and I1 (Clauses(PU , φ)) from
the proof of Lemma 4. Note that, I1 (nextU )(v, v ′ ) = nextΨ (v, v ′ ), hence PΨ =
I1 (PU ). Thus, by Theorem 3 the set Clauses(PΨ , φ) = Clauses(I1 (PU ), φ) =
I1 (Clauses(PU , φ)) is satisfiable by some interpretation I2 , since PΨ satisfies φ.
Hence, I := I1 ∪ I2 is a satisfying interpretation for Clauses(PU , φ).
    Since the formula ∀vr ∃vr′ : Ψ (hl, l′ i)(vr , vr′ ) is true, then ∆a (P, H) is satisfied
by I1 , and therefore also by I. Thus, ∆(P, H, φ) is satisfied by I.                        ⊓
                                                                                            ⊔




                                             32
