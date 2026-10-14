                                           Compositional Safety Verification with Max-SMT
                                            Marc Brockschmidt ∗ , Daniel Larraz † , Albert Oliveras † , Enric Rodrı́guez-Carbonell † and Albert Rubio †
                                                                                          ∗ Microsoft Research, Cambridge
                                                                                       † Universitat Politècnica de Catalunya




                                           Abstract—We present an automated compositional program        our approach is Max-SMT solving. Max-SMT solvers can
                                        verification technique for safety properties based on conditionaldeal with hard and soft constraints, where hard constraints are
                                        inductive invariants. For a given program part (e.g., a single
arXiv:1507.03851v3 [cs.LO] 3 Aug 2015




                                                                                                         mandatory, and soft constraints are those that we would like to
                                        loop) and a postcondition ϕ, we show how to, using a Max-SMT
                                                                                                         hold, but are not required to. Hard constraints express what is
                                        solver, an inductive invariant together with a precondition can be
                                        synthesized so that the precondition ensures the validity of the needed for the soundness of our analysis, while soft ones favor
                                        invariant and that the invariant implies ϕ. From this, we build  the solutions that are more useful for our technique. More
                                        a bottom-up program verification framework that propagates       precisely, we use Max-SMT to iteratively infer conditional
                                        preconditions of small program parts as postconditions for       inductive invariants1 , which prove the validity of a property,
                                        preceding program parts. The method recovers from failures
                                        to prove the validity of a precondition, using the obtained      given that a precondition holds. Hence, if the precondition
                                                                                                         holds, the program is proved safe. Otherwise, thanks to a
                                        intermediate results to restrict the search space for further proof
                                        attempts.                                                        novel program transformation technique we call narrowing2 ,
                                           As only small program parts need to be handled at a time,     we exploit the failing conditional invariants to focus on what
                                        our method is scalable and distributable. The derived conditions is missing in the safety proof of the program. Then new
                                        can be viewed as implicit contracts between different parts of
                                        the program, and thus enable an incremental program analysis.    conditional invariants are sought, and the process is repeated
                                                                                                         until the safety proof is finally completed. Based on this, we
                                                                                                         introduce a new bottom-up program analysis procedure that
                                                               I. I NTRODUCTION                          infers conditional invariants in a goal-directed manner, starting
                                           To have impact on everyday software development, a ver- from a property that we wish to prove for the program. Our
                                        ification engine needs to be able to process the millions of approach makes distributing analysis tasks as simple as in
                                        lines of code often encountered in mature software projects. other bottom-up analyses, but also enjoys the precision of
                                        At the same time, the analysis should be repeated every CEGAR-based provers.
                                        time developers commit a change, and should report feed-
                                        back in the course of minutes, so that fixes can be applied                    II. I LLUSTRATION OF THE M ETHOD
                                        promptly. Consequently, a central theme in recent research
                                        on automated program verification has been scalability. As          In this section, we illustrate the core concepts of our
                                        a natural solution to this problem, compositional program        approach    by using some small examples. We will give the
                                        analyses [1]–[3] have been proposed. They analyze program        formal   definition  of the used methods in Sect. IV.
                                        parts (semi-)independently and then combine the results to          We handle programs by considering one strongly connected
                                        obtain a whole-program proof.                                    component      (SCC) C of the control-flow graph at a time,
                                           For this, a compositional analysis has to predict likely      together   with  the sequential parts of the program leading to C,
                                        intermediate assertions that allow us to break whole-program     either  from  initial states or other SCCs.
                                        reasoning into many instances of local reasoning. This strat-       Instead  of  program    invariants, for each SCC we synthesize
                                        egy simplifies the individual reasoning steps and allows dis-    conditional   inductive  invariants.  These are inductive properties
                                        tributing the analysis [4]. The disadvantage of compositional    such   that they   may    not always    hold whenever the SCC is
                                        analyses has traditionally been their precision: local analyses  reached,   but  once  they  hold, then   they are always satisfied.
                                        must blindly choose the intermediate assertions. While in some        a)   Conditional    Inductive  Invariants:
                                                                                                                                                              while i > 0 do
                                        domains (e.g. heap) some heuristics have been found [2], effec- As an example, consider the program snip-               x := x + 5;
                                        tive strategies for guessing and/or refining useful intermediate pet in Fig. 1, where we do not assume any              i := i − 1;
                                        assertions or summaries in arithmetic domains remains an knowledge about the rest of the program.                     done
                                        open problem.                                                    To prove the assertion, we need an induc-
                                                                                                                                                              assert(x ≥ 0);
                                           In this paper we introduce a new method for predicting and tive property Q for the loop such that                      Fig. 1.
                                        refining intermediate arithmetic assertions for compositional Q together with the negation of the loop
                                        reasoning about sequential programs. A key component in
                                                                                                                 1 This concept was previously introduced with the name “quasi-invariant”

                                          This work has been supported by Spanish MINECO under the grant      in [5] in the different context of proving program non-termination.
                                        TIN2013-45732-C4-3-P (project DAMAS) and the FPI grant BES-2011-         2 This narrowing is inspired by the narrowing in term rewrite systems, and
                                        044621 (Larraz).                                                      is unrelated to the notion with the same name used in abstract interpretation.
condition i > 0 implies the assertion. Using our constraint-                                     III. P RELIMINARIES
solving based method CondSafe (cf. Sect. IV-A), we find                1) SAT, Max-SAT, and Max-SMT: Let P be a fixed set of
Q1 = x + 5 · i ≥ 0. The property Q1 can be seen as a               propositional variables. For p ∈ P, p and ¬p are literals. A
precondition at the loop entry for the validity of the assertion.  clause is a disjunction of literals l1 ∨· · ·∨ln . A (CNF) proposi-
                                                                   tional formula is a conjunction of clauses C1 ∧ · · · ∧ Cm . The
       b) Combining Conditional Inductive Invariants: Once
                                                                   problem of propositional satisfiability (SAT) is to determine
we have found a conditional inductive invariant for an SCC,
                                                                   whether a propositional formula is satisfiable. An extension
we use the generated preconditions as postconditions for its
                                                                   of SAT is satisfiability modulo theories (SMT) [6], where
preceding SCCs in the program.
                                                                   satisfiability of a formula with literals from a given background
                        As an example, assume that the loop theory is checked. We will use the theory of quantifier-free
  while j > 0 do
                     from Fig. 1 is directly preceded by the integer (non-)linear arithmetic, where literals are inequalities
     j := j − 1;
                     loop in Fig. 2. We now use the pre- of linear (resp. polynomial) arithmetic expressions.
     i := i + 1;
                     condition Q1 we obtained earlier as in-           Another extension of SAT is Max-SAT [6], which general-
  done
                     put to our conditional invariant synthesis izes SAT to finding an assignment such that the number of
       Fig. 2.       method, similarly to the assertion in Fig. 1. satisfied clauses in a given formula F is maximized. Finally,
Thus, we now look for an inductive property Q2 that, together Max-SMT combines Max-SAT and SMT. A (weighted partial)
with ¬(j > 0), implies Q1 . In this case we obtain the Max-SMT problem is a formula of the form H1 ∧ . . . ∧ Hn ∧
conditional invariant Q2 = j ≥ 0 ∧ x + 5 · (i + j) ≥ 0 for [S1 , ω1 ] ∧ . . . ∧ [Sm , ωm ], where the hard clauses Hi and the
the loop. As with Q1 , now we can see Q2 as a precondition soft clauses Sj (with weight ωj ) are disjunctions of literals
at the loop entry, and propagate Q2 up to the preceding SCCs over a background theory, and the aim is to find a model of
in the program.                                                    the hard clauses that maximizes the sum of the weights of the
                                                                   satisfied soft clauses.
       c) Recovering from Failures: When we cannot prove               2) Programs and States: We make heavy use of the
that a precondition always holds, we try to recover and find program structure and hence represent programs as graphs.
an alternative precondition. In this process, we make use of For this, we fix a set of (integer) program variables V =
the results obtained so far, and narrow the program using {v , . . . , v } and denote by F (V) the formulas consisting of
                                                                       1        n
our intermediate results. As an example, consider the loop conjunctions of linear inequalities over the variables V. Let L
in Fig. 3.                                                         be the set of program locations, which contains a canonical
   We again apply our method                                       start location ℓ0 . Program transitions T are tuples (ℓ, τ, ℓ′ ),
                                          while unknown() do where ℓ and ℓ′ ∈ L represent the pre- and post-location re-
CondSafe to find a conditional in-
                                             assert(x 6= y);       spectively, and τ ∈ F (V ∪ V ′ ) describes its transition relation.
variant for this loop which, together
                                             x := x + 1;           Here V ′ = {v1′ , . . . , vn′ } are the post-variables, i.e., the values
with the loop condition, implies the
                                             y := y + 1;           of the variables after the transition.3 A transition is initial if
assertion in the loop body. As it
                                          done                     its source location is ℓ0 . A program is a set of transitions. We
can only synthesize conjunctions of
linear inequalities, it produces the              Fig. 3.          view a program P = (L, T ) as a directed graph (the control-
conditional invariant Q3 = x > y for the loop. However, flow graph, CFG), in which edges are the transitions T and
                                                                                                      4
assume that the precondition Q3 could not be proven to always nodes are the locations L.
hold in the context of our example. In that case, we use               A state s = (ℓ, v) consists of a location ℓ ∈ L and a
the obtained information to narrow the program and look for valuation v : V → Z. A state (ℓ, v) is initial if ℓ = ℓ0 .
another precondition.                                              We denote an evaluation step with transition t = (ℓ, τ, ℓ′ )
                                          if ¬(x > y) then         by (ℓ, v) →t (ℓ′ , v ′ ), where the valuations v, v ′ satisfy the
   Intuitively, our program narrow-                                formula τ of t. We use →P if we do not care about the
                                             while ¬(x > y) do
ing reflects that states represented                               executed transition, and →∗P to denote the transitive-reflexive
                                                assert(x 6= y);
by the conditional invariant found                                 closure of →P . We say that a state s is reachable if there
                                                x := x + 1;
earlier are already proven to be safe.                             exists an initial state s0 such that s0 →∗P s.
                                                y := y + 1;
Hence, we only need to consider                                        3) Safety and Invariants: An assertion (t, ϕ) is a pair of a
                                             done
states for which the negation of the                               transition t ∈ T and a formula ϕ ∈ F (V). A program P is
                                          fi
conditional invariant holds, i.e., we                              safe for the assertion (t, ϕ) if for every evaluation (ℓ0 , v 0 ) →∗P
can add its negation as an assump-                Fig. 4.
                                                                   ◦ →t (ℓ, v), we have that v |= ϕ holds.5 Note that proving
tion to the program. In our example, this yields the modified that a formula ϕ always holds at a location ℓ can be handled
version of Fig. 3 displayed in Fig. 4. Another call to CondSafe
then yields the conditional invariant Q′3 = x < y for the             3 For ϕ ∈ F (V), ϕ′ ∈ F (V ′ ) is the version of ϕ using primed variables.
                                                                      4 Since we label transitions only with conjunctions of linear inequalities,
loop. This means that we can ensure the validity of the
assertion if before the conditional statement we satisfy that disjunctive conditions are represented using several transitions with the same
                                                                   pre- and post-location. Thus, P is actually a multigraph.
¬(x > y) ⇒ x < y, or equivalently, x 6= y. In general, this           5 Here, →∗ ◦ → denotes arbitrary program evaluations that end with an
                                                                                       t
                                                                                P
narrowing allows us to find (some) disjunctive invariants.         evaluation step using t.
in this setting by adding an extra location ℓ∗ and an extra                Conditional safety is “transitive” in the sense that if a set
transition t∗ = (ℓ, true, ℓ∗ ) and checking safety for (t∗ , ϕ).       of transitions E = {te1 , . . . , tf                    6
                                                                                                          m } dominates t, and for all i =
   We call a map I : L → F (V) a program invariant (or                 1, . . . , m we have P is (tei , ϕ
                                                                                                        ei )-conditionally safe for (t, ϕ) and
often just invariant) if for all reachable states (ℓ, v), we have      P is safe for (tei , ϕ
                                                                                            ei ), then P is also safe for (t, ϕ). In what
v |= I(ℓ) holds. An important class of program invariants              follows we exploit this observation to prove program safety
are inductive invariants. An invariant I is inductive if the           by means of conditional safety.
following conditions hold:                                                 A program component C of a program P is an SCC of
                                                                       the control-flow graph, and its entry transitions (or entries)
   Initiation:                                     ⊤ |= I(ℓ0 )
                                                                       EC are those transitions t = (ℓ, τ, ℓ′ ) such that t 6∈ C but
   Consecution:         For (ℓ, τ, ℓ′ ) ∈ P: I(ℓ) ∧ τ |= I(ℓ′ )′
                                                                       ℓ′ appears in C. By considering each component as a single
    4) Constraint Solving for Verification: Inductive invariants node, we can obtain from P a DAG of SCCs, whose edges
can be generated using a constraint-based approach [7], [8]. are the entry transitions. Our technique analyzes components
The idea is to consider templates for candidate invariant independently, and communicates the results of these analyses
properties, such as (conjunctions of) linear inequalities. These to other components along entry transitions.
templates contain both the program variables V as well as                  Given a component C and an assertion (t, ϕ) such that
template variables V T , whose values have to be determined t 6∈ C but the source node of t appears in C, we call t an
to ensure the required properties. To this end, the conditions exit transition of C. For such exit transitions, we compute a
on inductive invariants are expressed by means of constraints sufficient condition ψt̃ for each entry transition t̃ ∈ EC such
of the form ∃ V T .∀ V . . . .. Any solution to these constraints that C ∪ {t} is (t̃, ψt̃ )-conditionally safe for (t, ϕ). Then we
then yields an invariant. In the case of linear arithmetic, Farkas’ continue reasoning backwards following the DAG and try to
Lemma [9] is often used to handle the quantifier alternation in prove that P is safe for each (t̃, ψt̃ ). If we succeed, following
the generated constraints. Intuitively, it allows one to transform the argument above we will have proved P safe for (t, ϕ).
∃∀ problems encountered in invariant synthesis into ∃ prob-                In the following, we first discuss how to prove conditional
lems. In the general case, an SMT problem over non-linear safety of single program components in Sect. IV-A, and then
arithmetic is obtained, for which effective SMT solvers exist present the algorithm that combines these local analyses to
[10], [11]. By assigning weights to the different conditions, construct a global safety proof in Sect. IV-B.
invariant generation can be cast as an optimization problem in
                                                                       A. Synthesizing Local Conditions
the Max-SMT framework [5], [12].
                                                                           Here we restrict ourselves to a program component C and
                       IV. P ROVING S AFETY                            its  entry transitions EC , and assume we are given an assertion
                                                                       (texit , ϕ), where texit = (ℓ̃exit , τexit , ℓexit ) is an exit transition
    Most automated techniques for proving program safety of C (i.e., texit 6∈ C and ℓ̃exit appears in C). We show
iteratively construct inductive program invariants as over- how a precondition (t, ψ) for (texit , ϕ) can be obtained for
approximations of the reachable state space. Starting from each t ∈ EC . Here we only consider the case of ϕ being a
the known set of initial states, a process to discover more single clause (i.e., a disjunction of literals); if ϕ is in CNF,
reachable states and refine the approximation is iterated, until each conjunct is handled separately. The preconditions on the
it finally reaches a fixed point (i.e., the invariant is inductive) entry transitions will be determined by a conditional inductive
and is strong enough to imply program safety. However, this invariant, which like a standard invariant is inductive, but not
requires taking the whole program into account, which is necessarily initiated in all program runs. Indeed, this initiation
sometimes infeasible or undesirable in practice.                       condition is what we will extract as precondition and propagate
     In contrast to this, our method starts with the known unsafe backwards to preceding program components in the DAG.
states, and iteratively constructs an under-approximation of the
set of safe states, with the goal of showing that all initial states Definition 2 (Conditional Inductive Invariant). We say a map
are contained in that set. For this, we introduce the notion of Q : L → F (V) is a conditional (inductive) invariant for a
                                                                                                                                 ′  ′
conditional safety. Intuitively, when proving that a program is program (component) P if for all (ℓ, v) →P (ℓ , v ), we have
                                                                                               ′          ′
(t̃, ϕ̃)-conditionally safe for the assertion (t, ϕ) we consider v |= Q(ℓ) implies v |= Q(ℓ ).
evaluations starting after a →t̃ (ℓ̃, ṽ) step, where ṽ satisfies ϕ̃,     Conditional invariants are convenient tools to express con-
instead of evaluations starting at an initial state. In particular, ditions for safety proving, allowing reasoning in the style of
a program that is (t0 , ⊤)-conditionally safe for (t, ϕ) for all “if the condition for Q holds, then the assertion (t, ϕ) holds”.
initial transitions t0 is (unconditionally) safe for (t, ϕ).
Definition 1 (Conditional safety). Let P be a program, t, t̃ Example 1. Consider the program snippet in Fig. 5. A con-
transitions and ϕ, ϕ̃ ∈ F (V). The program P is (t̃, ϕ̃)- ditional inductive invariant supporting safety of this program
conditionally safe for the assertion (t, ϕ) if for any evaluation part is Q5 (ℓ1 ) ≡ x + 5 · i ≥ 50, Q5 (ℓ2 ) ≡ x ≥ 50. In fact, any
that contains → (ℓ̃, ṽ) →∗ (ℓ̄, v̄) → (ℓ, v), we have ṽ |= ϕ̃ conditional invariant Qm (ℓ1 ) ≡ x+m·i ≥ 50 with 0 ≤ m ≤ 5
                  t̃          P            t
implies that v |= ϕ. In that case we say that the assertion                 6 We say a set of transitions E dominates transition t if every path in the
(t̃, ϕ̃) is a precondition for the postcondition (t, ϕ).                  CFG from ℓ0 that contains t must also contain some t̃ ∈ E.
       ...                                                                           Algorithm 1 Proc. CondSafe computing conditional invariant
       while i > 0 do                             ℓ1                                 Input: component C, entry transitions EC , assertion (texit , ϕ)
          x := x + 5;                    i≤0                  i>0                        s.t. texit is an exit transition of C and ϕ is a clause
xxxxxx                                 ∧ x′ = x             ∧ x′ = x + 5
          i := i − 1;                                                                Output: None | Q, where Q maps locations in C to conjunc-
       done                            ∧ i′ = i             ∧ i′ = i − 1                 tions of inequations
       assert(x ≥ 50)                             ℓ2                                  1: k ← 1
                        xxxxxxxx
                                                                                      2: repeat
            Fig. 5. Source code of program snippet and its CFG.                       3:      construct formula Fk from C, EC and (texit , ϕ)
                                                                                      4:      σ ← Max-SMT-solver(Fk )
                                                                                      5:      if σ is a model then
would be a conditional inductive invariant that, together with                        6:          Q ← {ℓ 7→ σ(Iℓ,k ) | ℓ in C} return Q
the negation of the loop condition i ≤ 0, implies x ≥ 50.
                                                                                      7:      k ←k+1
                                                                                      8: until k > MAX CONJUNCTS return None
   We use a Max-SMT-based constraint-solving approach to
generate conditional inductive invariants. Unlike in [5], to
use information about the initialization of variables before a
                                                                                     templates Iℓ,k with the values found for the template variables
program component, we take into account the entry transitions
                                                                                     in the model σ, obtaining a conditional invariant Q. When we
EC . The precondition for each entry transition is the conditional
                                                                                     obtain a result, for every entry transition t = (ℓ, τ, ℓ′ ) ∈ EC
invariant that has been synthesized at its target location.
                                                                                     the conditional invariant Q(ℓ′ ) is a precondition that implies
   To find conditional invariants, we construct a constraint
                                                                                     safety for the assertion (texit , ϕ). The following theorem states
system. For each location ℓ in C we create a template
                                                                                     the correctness of this procedure.
Iℓ,k (V) ≡ ∧1≤j≤k Iℓ,j,k (V) which is a conjunction
                                                  P         of k linear
inequations7 of the form Iℓ,j,k (V) ≡ iℓ,j + v∈V iℓ,j,v · v ≤ 0,                     Theorem 1. Let C be a component, EC its entry transitions,
where the iℓ,j , iℓ,j,v are fresh variables from the set of                          and (texit , ϕ) an assertion with texit an exit transition of C and
template variables V T . We then transform the conditions for a                      ϕ a clause. If the procedure call CondSafe(C, EC , (texit , ϕ))
conditional invariant proving safety for the assertion (texit , ϕ)                   returns Q =  6 None, then Q is a conditional inductive invariant
to the constraints in Fig. 6. Here, e.g., Iℓ′′ ,k refers to the variant              for C and P is (t, Q(ℓ′ ))-conditionally safe for (texit , ϕ) for
of Iℓ′ ,k using primed versions of the program variables V, but                      all t = (ℓ, τ, ℓ′ ) ∈ EC .
unprimed template variables V T .
                                                                                     Proof. All proofs can be found in Appendix A.
   In the overall constraint system, we mark the Conse-
cution and Safety constraints as hard requirements. Thus,                            B. Propagating Local Conditions
any solution to these constraints is a conditional inductive                            In this section, we explain how to use the local procedure
invariant implying our assertion. However, as we mark the                            CondSafe to prove safety of a full program. To this end we now
Initiation constraints as soft, the found conditional invariants                     consider the full DAG of program components. As outlined
may depend on preconditions not implied by the direct context                        above, the idea is to start from the assertion provided by
of the considered component. On the other hand, the Max-                             the user, call the procedure CondSafe to obtain preconditions
SMT solver prefers solutions that require fewer preconditions.                       for the entry transitions of the corresponding component, and
Overall, we create the following Max-SMT formula                                     then use these preconditions as assertions for preceding com-
    def ^           ^                                 ^                             ponents, continuing recursively. If eventually for each initial
Fk =        Ct,k ∧       It,j,k ∨ ¬ pIt,j,k ∧ Sk ∧         [pIt,j,k , ωI ],
                                                                                     transition the transition relation implies the corresponding
        t∈C       t∈EC ,1≤j≤k                           t∈EC ,1≤j≤k
                                                                                     preconditions, then safety has been proven. If we fail to
where the pIt,j,k are propositional variables which are true                         prove safety for certain assertions, we backtrack, trying further
if the Initiation condition It,j,k is satisfied, and ωI is the                       possible preconditions and conditional invariants.
corresponding weight. 8 We use Fk in our procedure CondSafe                             The key to the precision of our approach is our treatment
in Algo. 1.                                                                          of failed proof attempts. When the procedure CondSafe finds
   In CondSafe, we iteratively try “larger” templates of more                        a conditional invariant Q for C, but proving (t, Q(ℓ′ )) as a
conjuncts of linear inequations until we either give up (in our                      postcondition of the preceding component fails for some t =
implementation, MAX CONJUNCTS is 3) or finally find a                                (ℓ, τ, ℓ′ ) ∈ EC , we use Q to narrow our program representation
conditional invariant. Note, however, that here we are only                          and filter out evaluations that are already known to be safe.
trying to prove safety for one clause at a time, which reduces                          As outlined above, in our proof process we treat each
the number of required conjuncts as compared to dealing with                         clause of the conjunction Q(ℓ′ ) separately, and pass each
a whole CNF in a single step. If the Max-SMT solver is                               one as its own assertion to preceding program components,
able to find a model for Fk , then we instantiate our invariant                      allowing for a fine-grained program-narrowing technique. By
  7 In our overall algorithm, k is initially 1 and increased in case of failures.    construction of Q, evaluations that satisfy all literals of Q(ℓ′ )
  8 Farkas’ Lemma is applied locally to the subformulas C
                                                             t,k , It,j,k and Sk ,
                                                                                     after executing t = (ℓ, τ, ℓ′ ) ∈ EC are safe. Thus, among the
and weights are added on the resulting constraints over the template variables.      evaluations that use t, we only need to consider those where
                                                                                            def
                     Initiation:       For t = (ℓ, τ, ℓ′ ) ∈ EC , 1 ≤ j ≤ k: It,j,k          =                     τ    ⇒ Iℓ′′ ,j,k
                                                                                            def
                     Consecution:      For t = (ℓ, τ, ℓ′ ) ∈ C:                     Ct,k     =              Iℓ,k ∧ τ    ⇒ Iℓ′′ ,k
                                                                                            def
                     Safety:           For texit = (ℓ̃exit , τexit , ℓexit ):       Sk       =     Iℓ̃exit ,k ∧ τexit   ⇒ ϕ′

                                                Fig. 6. Constraints used in CondSafe(C, EC , (texit , ϕ))


Algorithm 2 Procedure CheckSafe for proving a program safe                      Theorem 2. Let P be a program, C a component and
for an assertion                                                                EC its entries. Given an assertion (texit , ϕ) such that
Input: Program P, a component C, entries EC , assertion                         texit is an exit transition of C and ϕ is a clause, if
    (texit , ϕ) s.t. texit is an exit transition of C and ϕ a clause            CheckSafe(P, C, EC , (texit , ϕ)) = Safe, then P is safe for
Output: Safe | Maybe                                                            (texit , ϕ).
 1: let (ℓexit , τexit , ℓ′exit ) = texit
 2: if (τexit ⇒ ϕ′ ) then return Safe                                           Example 2. We demonstrate CheckSafe on the program
 3: else if ℓexit = ℓ0 then return Maybe                                        displayed on Fig. 7, called P in the following, which is an
                                                                                extended version of the example from Fig. 3.
 4: Q ← CondSafe(C, EC , (texit , ϕ))
                                                                                   We want to prove the assertion (t5 , x 6= y). Hence we make
 5: if Q = None then return Maybe
                                                                                a first call CheckSafe(P, {t4 }, {t3 }, (t5 , x 6= y)): the non-
 6: for all t = (ℓ, τ, ℓ′ ) ∈ EC , L ∈ Q(ℓ′ ) do
                                                                                trivial SCC containing ℓ2 is {t4 } and its entry transitions
 7:     C˜ ← component(ℓ, P)                                                    are {t3 }. Hence, we call CondSafe({t4 }, {t3 }, (t5 , x 6= y))
 8:     EC̃ ← entries(C,      ˜ P)
                                                                                and the resulting conditional invariant for ℓ2 is either x < y
 9:     res[t, L] ← CheckSafe(P, C,       ˜ E , (t, L))
                                             C̃                                 or y < x. Let us assume it is y < x. In the next step,
10: if ∀t = (ℓ, τ, ℓ′ ) ∈ EC , L ∈ Q(ℓ′ ) . res[t, L] = Safe then               we propagate this to the predecessor SCC {t2 }, and call
11: return Safe                                                                 CheckSafe(P, {t2 }, {t1 }, (t3 , y < x)).
12: else                        ^                                                  In turn, this leads to calling CondSafe({t2 }, {t1 }, (t3 , y <
13:     ÊC ← {(ℓ, τ ∧ ¬(              L′ ), ℓ′ ) | t = (ℓ, τ, ℓ′ ) ∈ EC }      x)) to our synthesis subprocedure. No conditional invariant
                              L∈Q(ℓ′ )
                           res[t,L]=Maybe
                                                                                supporting this assertion can be found, and hence None is
14:     Cˆ ← {(ℓ, τ ∧ ¬Q(ℓ′ )′ ∧ ¬Q(ℓ), ℓ′ ) | (ℓ, τ, ℓ′ ) ∈ C}                 returned by CondSafe, and consequently Maybe is returned
15: return CheckSafe(P, Ĉ, ÊC , (texit , ϕ))
                                                                                by CheckSafe. Hence, we return to the original SCC {t4 }
                                                                                and its entry {t3 }, and then by narrowing we obtain two new
                                                                                transitions:

at least one literal in Q(ℓ′ ) does not hold. Hence, we narrow          t′4 = (ℓ2 , x′ = x + 1 ∧ y′ = y + 1 ∧ ¬(y < x), ℓ2 ),
each entry transition by conjoining it with the negation of the         t′3 = (ℓ1 , x < 0 ∧ x′ = x ∧ y′ = y ∧ ¬(y < x), ℓ2 ).
conjunction of all literals for which we could not prove safety
                                                                 Using these, we call CheckSafe(P, {t′4 }, {t′3 }, (t5 , x 6= y)). The
(see line 13 in Algo. 2). Note that if there is more than one
                                                                 next call to CondSafe then yields the conditional invariant
literal in this conjunction, then the negation is a disjunction,
                                                                 x < y at ℓ2 , which is in turn propagated backwards with the
which in our program model implies splitting transitions.
                                                                 call CheckSafe(P, {t2 }, {t1 }, (t′3 , x < y)). This then yields a
   We can narrow program components similarly. For a tran-
                                                                 conditional invariant x < y at ℓ1 , which is finally propagated
sition t = (ℓ, τ, ℓ′ ) ∈ C, we know that if either Q(ℓ) or
     ′ ′                                                         back in the call CheckSafe(P, {}, {}, (t1, x < y)), which
Q(ℓ ) holds in an evaluation passing through t, the program
                                                                 directly returns Safe.
is safe. Thus, we narrow the program by replacing τ by                                                                             ℓ0
τ ∧ ¬ Q(ℓ) ∧ ¬ Q(ℓ′ )′ (see line 14 in Algo. 2).                 C. Improving Performance                            t1 : x < y
   This narrowing allows us to generate disjunctive conditional     The basic method CheckSafe                           ∧ x′ = x
invariants, where each result of CondSafe is one disjunct. Note can be extended in several ways                          ∧ y′ = y
that not all disjunctive invariants can be discovered like this, to improve performance. We now t2 : x′ ≥ 0
as each intermediate result needs to be inductive using the present a number of techniques                  ∧x = x− 1              ℓ1
                                                                                                            ∧ y′ = y
disjuncts found so far. However, this is the pattern observed that are useful to reduce the run-
                                                                                                                   t3 : x < 0
in phase-change algorithms [13].                                 time of the algorithm and dis-                        ∧ x′ = x
   Our overall safety proving procedure CheckSafe is shown tribute the required work. Note                             ∧ y′ = y
in Algo. 2. The helper procedures component and entries are that none of these techniques influ-
                                                                                                          t4 : x′ = x + 1          ℓ2
used to find the program component for a given location and ences the precision of the overall              ∧ y′ = y + 1
the entry transitions for a component. The result of CheckSafe framework.
                                                                                                                            t5 : ⊤
is either Maybe when the proof failed, or Safe if it succeeded.       a) Using conditional invari-
In the latter case, we have managed to create a chain of ants to disable transitions: When                                         ℓ3
conditional invariants that imply that (texit , ϕ) always holds. proving an assertion, it is often
                                                                                                                                      Fig. 7.
necessary to find invariants that show the unfeasibility of the solver simultaneously. Secondly, at a higher level, the
some transition, which allows disabling it. In our framework, recursive calls of CheckSafe (line 9 in Algo. 2) are parallelized.
the required invariants can be conditional as well. Therefore, Note that, since narrowing and the “learning” optimizations
CheckSafe must be called recursively to prove that the con- described above are considered only locally, they can be
ditional invariant is indeed invariant. In our implementation, handled as asynchronous updates to the program kept in each
we generate constraints such that every solution provides worker, and do not require synchronization operations. Hence,
conditional invariants either implying the postcondition or distributing the analysis onto several worker processes, in the
disabling some transition. By imposing different weights, we style of Bolt [4], would be possible as well.
make the Max-SMT solver prefer solutions that imply the                 Other directions for parallelization, which have not been im-
postcondition.                                                       plemented yet, are to return different conditional invariants in
      b) Handling unsuccessful proof attempts: One important parallel when the Max-SMT problem in procedure CondSafe
aspect is that the presented algorithm does not learn facts has several solutions. Moreover, based on experimental obser-
about the reachable state space, and so duplicates work when vations that successful safety proofs have a short successful
assertions appear several times. To alleviate this for unsuccess- path in the tree of proof attempts, we are also interested in
ful recursive invocations of CheckSafe, we introduce a simple exploring a look-ahead strategy: after calling CondSafe in
memoization technique to avoid repeating such calls. So when CheckSafe, we could make recursive calls of CheckSafe on
CheckSafe(P, C, EC , (t, ϕ)) = Maybe, we store this result, some processes while others are already applying narrowing.
and use it for all later calls of CheckSafe(P, C, EC , (t, ϕ)). This       e) Iterative proving: Finally, one could store the condi-
strategy is valid as the return value Maybe indicates that our tional invariants generated during a successful proof, which
method cannot prove the assertion (t, ϕ) at all, meaning that are hence invariants, so that they can be re-used in later runs.
later proof attempts will fail as well. In our implementation, E.g., if a single component is modified, one can reprocess it
this memoization of unsuccessful attempts is local to the and compute a new precondition that ensures its postcondition.
initial call to CheckSafe. The rationale is that, when proving If this precondition is implied by the previously computed
unrelated properties, it is likely that few calls are shared and invariant, the program is safe and nothing else needs to
that the book-keeping does not pay off.                              be done. Otherwise, one can proceed with the preceding
      c) Handling successful proof attempts: When a re- components, and produce respective new preconditions in a
cursive call yields a successful result, we can strengthen recursive way. Only when proving safety with the previously
the program with the proven invariant. Remember that computed invariants in this way fails, the whole program
CheckSafe(P, C, EC , (t, ϕ)) = Safe means that whenever needs to be reprocessed again. This technique has not been
the transition t is used in any evaluation, ϕ holds in the implemented yet, as our prototype is still in a preliminary
succeeding state. Thus, we can add this knowledge explicitly state.
and change the transition in the original program. In practice,
this strengthening is applied only if the first call to CheckSafe                          V. R ELATED W ORK
was successful, i.e, no narrowing was applied. The reason               Safety proving is an active area of research. In the recent
is that, if the transition relation of t was obtained through past, techniques based on variations of counterexample guided
repeated narrowing, in general one needs to split transitions, abstraction refinement have dominated [14]–[23]. These meth-
and it is not correct to just add ϕ′ to t. Namely, assume ods prove safety by repeatedly unfolding the program relation
that to = (ℓ, τo , ℓ′ ) is the original (unnarrowed) version of using a symbolic representation of program states, starting in
a transition t = (ℓ, τ, ℓ′ ) ∈ EC . As t is an entry transition the initial states. This process generates an over-approximation
of C, we have τ = τo ∧ ¬ψ1′ ∧ . . . ∧ ¬ψm     ′
                                                 by construction, of the set of reachable states, where the coarseness of
where ψi is the additional constraint we added in the i-th the approximation is a consequence of the used symbolic
narrowing of component entries. Thus what we proved is that representation. Whenever a state in the over-approximation
ψ1′ ∨. . .∨ψm′
               ∨ϕ′ always holds after using transition to . So we violates the safety condition, either a true counterexample
should replace to in the program with a transition labeled with was found and is reported, or the approximation is refined
τo ∧ (ψ1′ ∨ . . . ∨ ψm′
                        ∨ ϕ′ ). As we cannot handle disjunctions (using techniques such as predicate abstraction [24] or Craig
natively, this implies replacing to by m + 1 new transitions.        interpolation [25]). When further unwinding does not change
   Note that this program modification approach, unlike mem- the symbolic representation, all reachable states have been
oization, makes the gained information available to the Max- found and the procedure terminates. This can be understood as
SMT solver when searching for a conditional invariant. A a “top-down” (“forward”) approach (starting from the initial
similar strategy can be used to strengthen the transitions in states), whereas our method is “bottom-up” (“backwards”), i.e.
the considered component C.                                          starting from the assertions.
      d) Parallelizing & distributing the analysis: Our analysis        Techniques based on Abstract Interpretation [26] have had
can easily be parallelized. We have implemented this at two substantial success in the industrial setting. There, an abstract
stages. First, at the level of the procedure CondSafe, we try at interpreter is instantiated by an abstract domain whose ele-
the same time different numbers of template conjuncts (lines ments are used to over-approximate sets of program states. The
3-6 in Algo. 1), which requires calling several instances of interpreter then evaluates the program on the chosen abstract
domain, discovering reachable states. A widening operator,           directly from [27], where it is reported that the experiments
combining two given over-approximations to a more general            were performed on an Intel i5 2.6 GHz CPU with 8 Gb of
one representing both, is employed to guarantee termination          memory. For the sake of a fair comparison, we have run the
of the analysis when handling loops.                                 other tools on a 4-core machine with the same specification,
   “Bottom-up” safety proving with preconditions found by            using the same timeout of 200 seconds. Tab. I summarizes
abduction has been investigated in [27]. This work is closest        the results, reporting the number of successful proofs, failed
to ours in its overall approach, but uses fundamentally dif-         proofs, and timeouts (TO), together with the respective total
ferent techniques to find preconditions. Instead of applying         runtimes. Both versions of VeryMax are competitive, and our
Max-SMT, the approach uses an abduction engine based                 parallel version was two times faster than our sequential one
on maximal universal subsets and quantifier elimination in           on four cores. As a reference, on these examples VeryMax-
Presburger arithmetic. Moreover, it does not have an equivalent      Seq needed 2.8 overall calls (recursive or after narrowings) on
to our narrowing to exploit failed proof attempts. In a similar      average, with a maximum of 16. The number of narrowings
vein, [28] uses straight-line weakest precondition computation       was approximately 1, with a maximum of 13. Our memoiza-
and backwards-reasoning to infer loop invariants supporting          tion technique making use of already failed proof attempts was
validity of an assertion. To enforce a generalization towards        employed in about one third of the cases.
inductive invariants, a heuristic syntax-based method is used.          In our second benchmark set (which we will refer to as
   Automatically constructing program proofs from indepen-           NR-BENCHS) we have used integer abstractions of 217
dently obtained subproofs has been an active area of research        numerical algorithms from [46]. For each procedure and for
in the recent past. Splitting proofs along syntactic boundaries      each array access in it, we have created two safety problems
(e.g., handling procedures separately) has been explored in [1],     with one assertion each, expressing that the index is within
[2], [4], [29]. For each such unit, a summary of its behavior        bounds. In some few cases the soundness of array accesses in
is computed, i.e., an expression that connects certain (classes      the original program depends on properties of floating-point
of) inputs to outputs. Depending on the employed analyzers,          variables, which are abstracted away. So in the corresponding
these summaries encode under- and over-approximations of             abstraction some assertions may not hold. Altogether, the
reachable states [1] or changes to the heap using separation         resulting benchmark suite consists of 6452 problems, of up
logic’s frame rule [2]. Finally, [4] discusses how such compo-       to 284 lines of C code. Due to the size of this set, and to give
sitional analyses can leverage cloud computing environments          more room to exploit parallelism (both tools with which we
to parallelize and scale up program proofs.                          compare on these benchmarks, CPAchecker and SeaHorn,
                                                                     make use of several cores), we performed the experiments with
          VI. I MPLEMENTATION AND E VALUATION                        a more powerful machine, namely, an 8-core Intel i7 3.4 GHz
    We have implemented the algorithms from Sect. IV-A and           CPU with 16 GB of memory. The time limit is 300 seconds.
Sect. IV-B in our early prototype VeryMax, using the Max-               The results can be seen in Tab. II. On these instances,
SMT solver for non-linear arithmetic [30] in the Barcel-             VeryMax is able to prove more assertions than any of the
ogic [31] system. We evaluated a sequential (VeryMax-Seq)            other tools, while being about as fast as SeaHorn, and
and a parallel (VeryMax-Par) variant on two benchmark sets.          significantly faster than CPAchecker. Note that many exam-
    The first set (which we will call HOLA-BENCHS) are the           ples are solved very quickly in the sequential solver already,
46 programs from the evaluation of safety provers in [27]            and thus do not profit from our parallelization. VeryMax
(which were collected from a variety of sources, among others,       is at an early stage of development, and is hence not yet
[13], [32]–[42], the NECLA Static Analysis Benchmarks, etc.).        fully tuned. For example, a number of program slicing tech-
The programs are relatively small (they have between 17 and          niques have not been implemented yet, which would be
71 lines of code, and between 1 and 4 nested or consecutive          very useful for handling larger programs. Thus, we expect
loops), but expose a number of “hard” problems for analyzers.        that further development will improve the tool performance
All of them are safe.                                                significantly. The benchmarks and our tool can be found at
    On this first benchmark set we compare with three systems.       http://www.cs.upc.edu/∼albert/VeryMax.html.
The first two were leading tools in the Software Verifica-                                     VII. C ONCLUSION
tion Competition 2015 [43]: CPAchecker9 [44], which was
the overall winner and in particular won the gold medal                     We have presented a novel approach to compositional safety
                                                                          verification. Our main contribution is a proof framework that
in the “Control Flow and Integer Variables” category, and
SeaHorn [45], which got the silver medal, and also won refines intermediate results produced by a Max-SMT-based
the “Simple” category. We also compare with HOLA [27], precondition synthesis procedure. In contrast to most earlier
an abduction-based backwards reasoning tool. Unfortunately, work, we proceed bottom-up to compute summaries of code
we were not able to obtain an executable for HOLA. For that are guaranteed to be relevant for the proof.
this reason we have taken the experimental data for this tool               We plan to further extend VeryMax to cover more pro-
                                                                          gram features and include standard optimizations (e.g., slicing
   9 We ran CPAchecker with two different configurations, predicateAnaly- and constraint propagation with simple abstract domains). It
sis and sv-comp15.                                                        currently handles procedure calls by inlining, and does not
                                   Tool                            Safe      Σs  Fail   Σs  TO    Total s
                                   CPAchecker sv-comp15             33  2424.41    3  61.28  10  4489.73
                                   CPAchecker predicateAnalysis     25   503.05   11  19.72  10  2271.12
                                   SeaHorn                          32      7.95  13  3.477   1   211.56
                                   HOLA                             43    23.53    0      0   3   623.53
                                   VeryMax-Seq                      44   293.14    2  50.69   0   343.83
                                   VeryMax-Par                      45   138.40    1  12.81   0   151.21
                                                                     TABLE I
                                             E XPERIMENTAL RESULTS ON HOLA-BENCHS BENCHMARK SET.

                   Tool                                 Safe       Σs    Unsafe     Σs  Fail      Σs                       TO        Total s
                   CPAchecker sv-comp15                 5570 614803.98     251  6188.30 326  28749.78                      305    735336.82
                   CPAchecker predicateAnalysis         5928  23417.15     170   495.13 234   9105.69                      120     64652.29
                   SeaHorn                              6077   4276.21     233   135.25  80    529.09                       62     24167.11
                   VeryMax-Seq                          6105   5940.88        0       0 326  26739.30                       21     38980.80
                   VeryMax-Par                          6106   4789.73        0       0 346  18878.42                        0     23668.15
                                                                     TABLE II
                                               E XPERIMENTAL RESULTS ON NR-BENCHS BENCHMARK SET.


support recursive functions yet. However, they can be handled                     [17] K. L. McMillan, “Lazy abstraction with interpolants,” in CAV, 2006.
by introducing templates for function pre/postconditions.                         [18] A. Podelski and A. Rybalchenko, “ARMC: The logical choice for
                                                                                       software model checking with abstraction refinement,” in PADL, 2007.
   In the future, we are interested in experimenting with alter-                  [19] A. R. Bradley, “SAT-based model checking without unrolling,” in
native precondition synthesis methods (e.g., abduction-based                           VMCAI, 2011.
ones). We also want to combine our method with a Max-SMT-                         [20] S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko,
                                                                                       “Synthesizing software verifiers from proof rules,” in PLDI, 2012.
based termination proving method [12] and extend it to exis-                      [21] A. Albarghouthi, A. Gurfinkel, and M. Chechik, “Whale: an
tential properties such as reachability and non-termination [5].                       interpolation-based algorithm for inter-procedural verification,” in VM-
We expect to combine all of these techniques in an alternating                         CAI, 2012.
                                                                                  [22] A. Cimatti and A. Griggio, “Software model checking via IC3,” in CAV,
procedure [1] that tries to prove properties at the same time as                       2012.
their duals, and which uses partial proofs to narrow the state                    [23] K. Hoder and N. Bjørner, “Generalized property directed reachability,”
space that remains to be considered. Eventually, these methods                         in SAT, 2014.
                                                                                  [24] C. Flanagan and S. Qadeer, “Predicate abstraction for software verifica-
could be combined to verify arbitrary temporal properties.                             tion,” in POPL, 2002.
In another direction, we want to consider more expressive                         [25] K. L. McMillan, “Craig interpolation and reachability analysis,” in SAS,
theories to model program features such as arrays or the heap.                         2003.
                                                                                  [26] P. Cousot and R. Cousot, “Abstract interpretation: A unified lattice model
                              R EFERENCES                                              for static analysis of programs by construction or approximation of
                                                                                       fixpoints,” in POPL, 1977.
 [1] P. Godefroid, A. V. Nori, S. K. Rajamani, and S. Tetali, “Compositional      [27] I. Dillig, T. Dillig, B. Li, and K. L. McMillan, “Inductive invariant
     may-must program analysis: unleashing the power of alternation,” in               generation via abductive inference,” in OOPSLA, 2013.
     POPL, 2009.                                                                  [28] C. S. Pasareanu and W. Visser, “Verification of Java programs using
 [2] C. Calcagno, D. Distefano, P. O’Hearn, and H. Yang, “Compositional                symbolic execution and invariant generation,” in SPIN, 2004.
     shape analysis by means of bi-abduction,” JACM, vol. 58, no. 6, 2011.        [29] G. Yorsh, E. Yahav, and S. Chandra, “Generating precise and concise
 [3] B. Li, I. Dillig, T. Dillig, K. L. McMillan, and M. Sagiv, “Synthesis of          procedure summaries,” in POPL, 2008.
     circular compositional program proofs via abduction,” in TACAS, 2013.        [30] D. Larraz, A. Oliveras, E. Rodrı́guez-Carbonell, and A. Rubio, “Minimal-
 [4] A. Albarghouthi, R. Kumar, A. V. Nori, and S. K. Rajamani, “Paralleliz-           model-guided approaches to solving polynomial constraints and exten-
     ing top-down interprocedural analyses,” in PLDI, 2012.                            sions,” in SAT, 2014.
 [5] D. Larraz, K. Nimkar, A. Oliveras, E. Rodrı́guez-Carbonell, and A. Ru-       [31] M. Bofill, R. Nieuwenhuis, A. Oliveras, E. Rodrı́guez-Carbonell, and
     bio, “Proving non-termination using Max-SMT,” in CAV, 2014.                       A. Rubio, “The barcelogic SMT solver,” in CAV, 2008.
 [6] A. Biere, M. J. H. Heule, H. van Maaren, and T. Walsh, Eds., Handbook        [32] A. Gupta and A. Rybalchenko, “InvGen: An efficient invariant genera-
     of Satisfiability. IOS Press, 2009.                                               tor,” in CAV, 2009.
 [7] M. Colón, S. Sankaranarayanan, and H. Sipma, “Linear Invariant Gen-         [33] S. Gulwani, S. Srivastava, and R. Venkatesan, “Program analysis as
     eration Using Non-linear Constraint Solving,” in CAV, 2003.                       constraint solving,” in PLDI, 2008.
 [8] A. R. Bradley, Z. Manna, and H. B. Sipma, “Linear ranking with               [34] D. Beyer, T. A. Henzinger, R. Majumdar, and A. Rybalchenko, “Path
     reachability,” in CAV, 2005.                                                      invariants,” in PLDI, 2007.
 [9] A. Schrijver, Theory of Linear and Integer Programming. Wiley, 1998.         [35] B. S. Gulavani, S. Chakraborty, A. V. Nori, and S. K. Rajamani,
[10] C. Borralleras, S. Lucas, A. Oliveras, E. Rodrı́guez-Carbonell, and               “Automatically refining abstract interpretations,” in TACAS, 2008.
     A. Rubio, “SAT Modulo Linear Arithmetic for Solving Polynomial               [36] A. R. Bradley and Z. Manna, “Property-directed incremental invariant
     Constraints,” JAR, vol. 48, no. 1, 2012.                                          generation,” Formal Asp. Comput., vol. 20, no. 4-5, 2008.
[11] D. Jovanovic and L. M. de Moura, “Solving non-linear arithmetic,” in         [37] A. Miné, “The octagon abstract domain,” Higher-Order and Symbolic
     IJCAR, 2012.                                                                      Computation, vol. 19, no. 1, 2006.
[12] D. Larraz, A. Oliveras, E. Rodrı́guez-Carbonell, and A. Rubio, “Proving      [38] R. Jhala and K. L. McMillan, “A practical and complete approach to
     termination of imperative programs using Max-SMT,” in FMCAD, 2013.                predicate refinement,” in TACAS, 2006.
[13] R. Sharma, I. Dillig, T. Dillig, and A. Aiken, “Simplifying loop invariant   [39] R. Sharma, A. V. Nori, and A. Aiken, “Interpolants as classifiers,” in
     generation using splitter predicates,” in CAV, 2011.                              CAV, 2012.
[14] T. Ball and S. K. Rajamani, “The SLAM toolkit,” in CAV, 2001.                [40] B. S. Gulavani, T. A. Henzinger, Y. Kannan, A. V. Nori, and S. K.
[15] T. A. Henzinger, R. Jhala, R. Majumdar, and G. Sutre, “Software                   Rajamani, “SYNERGY: a new algorithm for property checking,” in FSE,
     verification with BLAST,” in SPIN, 2003.                                          2006.
[16] E. M. Clarke, D. Kroening, N. Sharygina, and K. Yorav, “SATABS:              [41] B. S. Gulavani and S. K. Rajamani, “Counterexample driven refinement
     SAT-based predicate abstraction for ANSI-C,” in TACAS, 2005.                      for abstract interpretation,” in TACAS, 2006.
                                                                        is safe for (tm−1 , Q(ℓm )). By construction of Q and Thm. 1,
[42] I. Dillig, T. Dillig, and A. Aiken, “Automated error diagnosis using
     abductive inference,” in PLDI, 2012.                               this then implies that the program is safe for (texit , ϕ).
[43] D. Beyer, “Software verification and verifiable witnesses - (report on
     SV-COMP 2015),” in TACAS, 2015.                                       The second case is returning the result of CheckSafe on the
[44] D. Beyer and M. E. Keremoglu, “CPAchecker: A tool for configurable narrowed program in lines 19 and 20. For this, we need to
     software verification,” in CAV, 2011.                              prove that our program narrowing is indeed correct. Assume
[45] T. Kahsai, J. A. Navas, A. Gurfinkel, and A. Komuravelli, “The SeaHorn
     verification framework,” in CAV, 2015.                             now that the considered evaluation is unsafe, i.e., that v n 6|= ϕ.
[46] W. H. Press, S. A. Teukolsky, W. T. Vetterling, and B. P. Flannery,We will show that our narrowing preserves unsafe evaluations.
     Numerical Recipes in C++ (2Nd Ed.): The Art of Scientific Computing.
                                                                        Then, as the recursive call of CheckSafe (with recursion depth
     New York, NY, USA: Cambridge University Press, 2002.
                                                                        u − 1) is correct by our induction hypothesis, we can conclude
                            A PPENDIX A                                 that  Safe is only returned if there are no unsafe evaluations.
                                P ROOFS                                    We   first consider the narrowing V ÊC . By our induction hy-
                                                                        pothesis, we know that v m |= ( L∈Q(ℓm ),res[tm−1 ,L]=Safe L′ )
Proof of Thm. 1. That Q is a conditional inductive invariant holds. Now assume that the narrowed version of t
                                                                                                                                     m−1 is
follows directly from the structure of the generated constraints, not enabled anymore because of the added condition. Then
which are (modulo renaming) also discussed in [8].                                     V
                                                                        v m 6|= V¬( L∈Q(ℓm ),res[tm−1 ,L]=Maybe L′ ) holds, and thus
   We prove the claim about conditional safety by contradic- v |=                                ′
                                                                          m          L∈Q(ℓm ) L . But then, our evaluation is safe (by
tion via induction over the length of evaluations. Assume that the same argument                as in the proof of Thm. 1), contradicting
there is an unsafe execution                                            our assumption that the considered evaluation is unsafe. Thus,
          (ℓ1 , v 1 ) →t1 (ℓ2 , v 2 ) →t2 . . . →tn (ℓn , v n )         unsafe evaluations are not broken by our narrowing of entry
                                                                        transitions.
of length n ∈ N>1 such that t1 ∈ EC ∪ C (i.e., ℓ2 is always                Similarly, we now consider the narrowing C.       ˆ We consider
a location in C), tn = texit , v 2 |= Q(ℓ2 ) and v n 6|= ϕ. We an evaluation step (ℓw , v w ) →tw (ℓw+1 , v w+1 ) with tw ∈ C.             ˆ
will show that no such evaluation can exist, implying our If the narrowed version t̂w ∈ C of tw cannot be used, ˆ
proposition as the special case t1 ∈ EC .                               then either v w |= Q(ℓw ) or v w+1 |= Q(ℓw+1 ) holds, and
   As the component graph is a DAG, t1 ∈ EC ∪ C and texit is again, by an argument similar to the proof of Thm. 1, this
an exit transition of C, we have ti ∈ C for all 1 < i < n.              contradicts the assumption that our evaluation is unsafe. Thus,
   We first consider the case n = 2 (n = 1 would be the unsafe evaluations are preserved by narrowing of the program
case where t1 is both an entry and exit transition, and thus component.
infeasible). Let t2 = (ℓ1 , τ2 , ℓ2 ). Then, v 2 |= Q(ℓ2 ) ≡ σ(Iℓ2 ,k )
by choice and definition, and σ(Iℓ2 ,k ) ∧ τ2 ⇒ ϕ′ by constraint                                     A PPENDIX B
Sk . Thus, no unsafe evaluation of length 2 is possible.                  C HOICE OF W EIGHTS IN THE M AX -SMT F ORMULATION

   We now assume n > 2 and that the proposition has been                   In VeryMax, all weights for the initiation conditions are
proven for evaluations of length n − 1. Let t2 = (ℓ2 , τ2 , ℓ3 ).       currently   the same. Choosing different weights would bias the
For length n, we have that the valuations v 2 , v 3 satisfy τ2 ,        solver  towards   satisfying certain initiation conditions. Weights
and v 2 |= Q(ℓ2 ) ≡ σ(Iℓ2 ,k ). These are the premises of our           play  a  crucial role  in VeryMax to favor invariants that imply
consecution constraint Ct2 ,k ≡ Iℓ2 ,k ∧ τ2 ⇒ Iℓ3 ,k , and thus         postconditions    over  ones that disable transitions (cf. Sect. IV-
v 3 |= σ(Iℓ3 ,k ) ≡ Q(ℓ3 ). Hence, we instead have to consider          C-a).   The   chosen   MaxSMT     framework also allows adding
the evaluation of length n − 1 starting in (ℓ2 , v 2 ), which by        other  techniques   with   lower weights,  e.g. the techniques from
our hypothesis is infeasible.                                           [5] that  strengthen   single program   transitions  during the anal-
                                                                        ysis.
Proof of Thm. 2. We prove the proposition by induction over
the number u of recursive calls of CheckSafe.
   In the base case u = 0, we have that τexit ⇒ ϕ′ , i.e.,
the condition to prove is always a consequence of using the
transition texit , and the claim trivially holds.
   Let now u > 0, and we assume that the proposition has
been shown for all calls of CheckSafe that return Safe and
need at most u − 1 recursive calls of CheckSafe.
   We now consider a program evaluation
  (ℓ0 , v 0 ) →t0 . . . →tm−1 (ℓm , v m ) →tm . . . →tn (ℓn , v n )
with tm−1 ∈ EC and tn = texit .
   First, we consider the case that CheckSafe returns Safe
in line 11, where all preconditions are satisfied for all entry
transitions. By the condition ∀L ∈ Q(ℓm ). res[tm−1 , L] =
Safe and our induction hypothesis, we know that the program
