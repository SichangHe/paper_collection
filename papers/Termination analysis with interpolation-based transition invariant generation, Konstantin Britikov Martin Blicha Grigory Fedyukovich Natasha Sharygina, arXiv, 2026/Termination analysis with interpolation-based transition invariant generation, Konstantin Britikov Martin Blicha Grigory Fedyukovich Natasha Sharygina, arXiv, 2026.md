                                                 Termination analysis with interpolation-based
                                                        transition invariant generation
                                              Konstantin Britikov                   Martin Blicha                   Grigory Fedyukovich                 Natasha Sharygina
                                                 USI, Switzerland           Argot Collective, Switzerland             FSU, United States                   USI, Switzerland



                                           Abstract—Termination and nontermination of infinite-state          focused (non)termination problems, which guide the analysis
                                        systems are complementary problems that, despite their close          of the whole transition system. Solving these problems helps
                                        connection, are typically addressed by separate techniques. The       to extend the transition invariant candidate and enables an
                                        core idea of this paper is to connect termination and nontermi-
                                        nation analysis, enabling the two to share intermediate results       efficient nontermination analysis of complex problems.
                                        and guide one another. We present a new termination analysis             We implemented our new technique in the G OLEM Con-
                                        approach based on the generation of well-founded transition in-       strained Horn Clause solver [26]. We evaluated it on the
                                        variants. It leverages Craig interpolation for transition invariant   Integer Transition Systems benchmarks from the Termination
                                        generation, capturing the structural reasons for termination. The
                                                                                                              Competition [27]. Our tool solved a large number of termi-
                                        proposed technique extends safety-based nontermination analy-
                                        sis, enabling it to prove both termination and nontermination         nating instances and demonstrated significant improvement for
arXiv:2608.08857v1 [cs.LO] 9 Aug 2026




                                        within a unified framework. We implemented our approach               nontermination analysis, compared to the classical SNA. The
                                        in the G OLEM verification framework and evaluated it on              comparison with the winners of the Termination Competi-
                                        benchmarks from the Termination Competition (TermComp).               tion 20251 —KOAT, L OAT [28], and T2 [18]— shows that
                                        Empirical results demonstrate that combining termination and
                                                                                                              our approach is competitive with the state-of-the-art tools and
                                        nontermination is beneficial and yields performance comparable
                                        to state-of-the-art tools.                                            can solve unique instances, including those that were never
                                                                                                              solved by any tool before.
                                                              I. I NTRODUCTION                                   Overall, the contributions of this paper are as follows:
                                            Termination analysis of infinite-state systems is a funda-        (1) a novel interpolation-based method for the generation of
                                        mental problem in formal methods. Proving termination and             disjunctively well-founded transition invariants, (2) a unified
                                        nontermination is undecidable [1], yet there exist many tech-         termination/nontermination analysis procedure that utilises the
                                        niques that succeed on a large class of real-world problems.          intermediate results of (non)termination analysis for self-
                                        Modern techniques treat termination and nontermination as             guidance and (3) its implementation and successful evaluation.
                                        separate problems, since each has a different proof procedure.
                                        The existence of a ranking function by e.g. [2]–[11] witnesses                                 II. P RELIMINARIES
                                        termination by providing a measure that strictly decreases
                                        along every transition. Alternatively, fixpoint computation,             This section introduces the definitions and formalisms used
                                        e.g. [12], and disjunctively well-founded transition invari-          in the paper. Logical formulas in our approach are defined over
                                        ants [13]–[16] have been proposed for termination analysis.           the theory of Linear Integer Arithmetic (LIA). We use X, X ′
                                        Nontermination techniques are predominantly based on the              to denote sets of variables (unprimed and primed), where X is
                                        detection of recurrent sets — sets of states from which               a set of state variables, and X ′ = {x′ |x ∈ X} is a set of next
                                        execution cannot escape [8], [10], [17]–[20]. There also exist        state variables. If a formula contains variables over multiple
                                        alternative approaches based on Hoare-style reasoning [21],           states, we use superscript notation, e.g., X (0) , . . . , X (n) .
                                        safety proving [22], [23], representing infinite runs as sums            The formula defined over X is a state formula, and a
                                        of geometric series [24], or synthesis of negative exact loop         formula over X ∪ X ′ is a transition formula. State formulas
                                        bounds [11].                                                          encode a set of states, and transition formulas define binary
                                                                                                                                                                 ′
                                            In this work, we present a unified framework for proving          relations over the states. We V use Id(X, X ) to denote the
                                        both termination and nontermination. This framework extends           identity transition formula x∈X x = x′ .
                                        the safety-based nontermination analysis [22] (SNA), enabling            A transition system is defined as TS = ⟨Init, Tr , X⟩,
                                        it to prove termination. The extension is a novel interpolation-      where Init is a formula encoding the initial states of the
                                        based method for generating disjunctively well-founded tran-          system, Tr is a transition formula, encoding the transition
                                        sition invariants for termination analysis. The proposed ap-          relation, and X is the set of system variables. With respect
                                        proach uses terminating transition traces constructed by SNA,         to transition system, a transition trace is a formula encod-
                                        overapproximating them with a Craig interpolation [25]. The           ing multiple consecutive transitions: Tr n (X (0) , . . . , X (n) ) =
                                        interpolant is processed into a transition invariant candidate,       Tr (X (0) , X (1) )∧· · ·∧Tr (X (n−1) , X (n) ). A safety problem is
                                        which is used to prove termination. Additionally, based on the
                                        transition invariant candidate, the algorithm creates smaller,          1 https://termination-portal.org/wiki/Termination Competition 2025.
P = ⟨Init, Tr , Bad, X⟩, where Bad is a formula representing                                                                START
states that violate the safety property.
                                                                                                       P = <Init, Tr, Sink, X>                                                          BlockTerm
   Safety verification amounts to determining whether there
                                                                                                       <SAFE, Inv>                      <UNSAFE, Trn>                 Construct states
exists a transition trace that reaches a Bad state from                                                                  Safety check
                                                                                                                             of P
                                                                                                                                                                    reachable after i and
                                                                                                                                                                       i+1 transitions
some initial state. If TS is safe, then there exists an in-                                                                               i = n-1

                                                                                                                                                                      Si, Si+1
ductive invariant Inv(X) such that (1) ∀X.Init(X) →                                          No
                                                                                                    Inv is a
                                                                                  UNKNOWN
Inv(X), (2) ∀X, X ′ .Inv(X) ∧ Tr (X, X ′ ) → Inv(X ′ ),                                           Recurrent set
                                                                                                                                                                Is SAT     Si(X) /\

and (3) ∀X.Inv(X) → ¬Bad(X). We use S AFETY-                                                   Yes                 Updated P
                                                                                                                                        Tr = Tr /\ ¬Si+1(X')             Tr(X,X') /\
                                                                                                                                                                          ¬Si+1(X')
                                                                                                                                                                                            i = i -1


C HECK (P ) to denote a safety verification procedure that                                   NONTERMINATING
                                                                                                                                                                        Is
returns a tuple ⟨SAFE, Inv(X)⟩ if TS is safe (Inv(X)                                                                                                                  UNSAT


is an inductive invariant). If TS is unsafe it returns                                                                                                          YES                         NO
⟨UNSAFE, Tr n (X (0) , . . . , X (n) )⟩, s.t. ∃X (0) , . . . , X (n)2 .                                                                 Init = Init /\ ¬S0(X)               i=0




       Init(X (0) ) ∧ Tr n (X (0) , . . . , X (n) ) ∧ Bad(X (n) )
                                                                                  Figure 1. Execution flow of Safety-based Nontermination analysis, cf. [22]
  A transition system is called nonterminating if there exists
an initial state from which it is possible to take any number
of transitions, meaning ∃X.Init(X) such that:                                        Given two formulas A and B where A ∧ B is unsatisfiable,
                       (1)            (n)     n          (1)            (n)       a Craig interpolant [25] for A and B is a formula I, where:
       ∀n ∈ N.∃X             ,...,X         .Tr (X, X          ,...,X         )
                                                                                  (1) A → I; (2) I ∧ B is unsatisfiable; and (3) I only contains
Definition 1 (Recurrent Set). For a Transition System                             the symbols, common to both A and B. Craig interpolants are
⟨Init, Tr , X⟩, a formula N (X) is a recurrent set if: (1)                        widely used as overapproximations. We write I TP(A, B) for
∀X.N (X) → ∃X ′ .Tr (X, X ′ ) ∧ N (X ′ ), (2) ∃X.N (X) ∧                          the computation of a Craig interpolant.
Init(X).
                                                                                  A. Proving Nontermination via Safety
   Transition System is nonterminating if there exists a re-
current set. Intuitively, every state in a recurrent set has a                      Many techniques reduce termination and nontermination
successor that also lies in the recurrent set, and the recurrent                  analysis to safety verification. One notable approach is the
set contains some of the initial states.                                          reduction of nontermination to safety, which constructs recur-
   A TS is called terminating if for every initial state it                       rent sets via inductive invariants [22]. It was introduced in the
enables only a finite number of transitions. Transition System                    context of proving nontermination of programs with loops, and
⟨Init, Tr , X⟩ terminates, if ∀X.Init(X) the following holds:                     can be extended to transition systems.

      ∃n ∈ N.¬∃X (1) , . . . , X (n) .Tr n (X, X (1) , . . . , X (n) )            Definition 5 (Sink states). For a Transition System
                                                                                  ⟨Init, Tr , X⟩, a state s is a sink state, if ¬∃s′ .Tr (s, s′ ). We
Definition 2 (Transition invariant). For a Transition Sys-                        use Sink (X) to denote the formula encoding all sink states in
tem ⟨Init, Tr , X⟩, TrInv (X, X ′ ) is a transition invariant                     the transition system: ∀X.Sink (X) ↔ ¬∃X ′ .Tr (X, X ′ )
if: ∀X, X ′ .R(X) ∧ Tr + (X, X ′ ) → TrInv (X, X ′ ), where
Tr + (X, X ′ ) is the transitive closure of Tr (X, X ′ ) and R(X)                    Algorithm 1 for Safety-based Nontermination analysis
is a formula encoding all states reachable in TS .                                (SNA) takes a safety problem P = ⟨Init, Tr , Sink , X⟩,
                                                                                  where sink states are constructed from TS using quantifier
Definition 3 (Well-founded Relation). A binary relation W ⊆                       elimination (QE): Sink (X) = ¬QE(∃X ′ .Tr (X, X ′ )). As an
D × D over a domain D is well-founded if there exists no                          output, it returns NONTERM if the system is nonterminating,
infinite descending chain:                                                        and UNKNOWN, if the algorithm cannot conclude the anal-
          ∄ d0 , d1 , d2 , · · · ∈ D. ∀i ∈ N. (di , di+1 ) ∈ W                    ysis. Figure 1 illustrates the execution flow of Safety-based
                                                                                  Nontermination.
   A relation W (X, X ′ ) can be proven to be well-
                                                                                     SNA iteratively solves increasingly refined safety problems
founded by synthesizing a ranking function f (X), such that
                                                                                  until the given sink states are proven unreachable. In every
∀X, X ′ .W (X, X ′ ) → f (X) > f (X ′ ) [2].
                                                                                  iteration, if there exists a trace reaching sink states (line 3),
   Termination can be proven using transition invariants [29]. If
                                                                                  B LOCK T ERM (Algorithm 2) refines the safety problem P
a transition invariant is a finite union of well-founded relations
                                                                                  by blocking the states that deterministically lead to the sink
(for example, if each relation admits a ranking function), then
                                                                                  states, updating the safety problem. B LOCK T ERM is described
the transition system terminates.
                                                                                  in detail below. When the original sink states are no longer
Definition 4 (Disjunctively well-founded relation). A relation                    reachable, SNA checks if the computed inductive invariant
               Sn
K(X, X ′ ) = i=0 Wi (X, X ′ ) is called disjunctively well-                       Inv (X) is a recurrent set (line 6). This amounts to deciding
founded if every relation Wi (X, X ′ ) is well-founded.                           satisfiability of the following formula:
  2 It is a shorthand notation for ∃X (0) , . . . , ∃X (n)                                                Inv (X) ∧ ¬∃X ′ .Tr (X, X ′ ).
 Algorithm 1: Safety-based Nontermination Analysis                         1∨x′ = x−2)∧x ̸= 0. The sink states are Sink (X) ≜ x = 0,
 (SNA), cf. [22]                                                           and the initial safety problem is P = ⟨Init, Tr , Sink , x⟩. This
  Input : Safety problem P = ⟨Init, Tr , Sink , X⟩                         TS is nonterminating, since x infinitely decreases.
  Output: NONTERM | UNKNOWN                                                   The execution of Algorithm 1 updates the initial states and
1 while ⊤ do                                                               the transition relation in two iterations of the algorithm, via
2   ⟨res, ϕ = Tr n or Inv ⟩ ← S AFETY C HECK(P )                           B LOCK T ERM: Init(X) ← x ̸= 0, and Tr (X, X ′ ) ←
3   if res = UNSAFE then
4       P ← B LOCK T ERM(P, ϕ)                                             Tr (X, X ′ ) ∧ x′ ̸= 0. The safety check of the updated problem
5   else                                                                   concludes SAFE, with Inv(X) ≜ x ̸= 0. Inv(X) is a
6       if ∀X.ϕ(X) → ∃X ′ .Tr (X, X ′ ) then                               recurrent set, and algorithm returns NONTERM.
7          return NONTERM                                                     Motivation for transition invariant-based termination anal-
8       return UNKNOWN                                                     ysis. Consider a small modification (replacing x ̸= 0 with
                                                                           x > 0): Tr (X, X ′ ) ≜ (x′ = x − 1 ∨ x′ = x − 2) ∧ x > 0.
                                                                           This renders TS terminating since x is strictly positive and
 Algorithm 2: B LOCK T ERM (P, Tr n ), cf. [22]
                                                                           decreases every step. However, Algorithm 1 cannot detect
   Input : Safety problem P = ⟨Init, Tr , Sink , X⟩,                       termination by design, and it would return UNKNOWN.
               terminating trace Tr n (X (0) , . . . , X (n) ) =
               Tr (X (0) , X (1) ) ∧ · · · ∧ Tr (X (n−1) , X (n) )
                                                                              Let us examine the execution of Algorithm 1 on this
   Output: Refined safety problem P ′                                      example. First, using B LOCK T ERM, it blocks initial states
   Data : S0 , . . . , Sn - formulas which encode states within            that instantly terminate: Init(X)          ←       x > 0. In the
               trace reachable in 0, ..., n transitions                    second iteration, S AFETY C HECK (P ) returns UNSAFE with
 1 i ← n−1
                                                                           a trace Tr 1 (X (0) , X (1) ) satisfying ∃X (0) , X (1) .Init(X (0) ) ∧
 2 while i > 0 do
                                                                           Tr 1 (X (0) , X (1) ) ∧ Sink (X (1) ). Our key insight is to gen-
 3    Si+1 (X) ← QE(∃X (0) , . . . , X (i) , X (i+2) , . . . , X (n) .
                                                                           eralise such terminating traces into a formula describing an
        Init(X (0) ) ∧ Tr n ∧ Sink (X (n) ))[X (i+1) 7→ X]
 4    Si (X) ← QE(∃X (0) , . . . , X (i−1) , X (i+1) , . . . , X (n) .     entire class of terminating behaviours. If this generalisation
        Init(X (0) ) ∧ Tr n ∧ Sink (X (n) ))[X (i) 7→ X]                   yields a disjunctively well-founded transition invariant over
 5    if SAT ? Si (X) ∧ Tr (X, X ′ ) ∧ ¬Si+1 (X ′ ) then                   all reachable states, it witnesses termination. Particularly,
 6        Tr ′ (X, X ′ ) ← Tr (X, X ′ ) ∧ ¬Si+1 (X ′ )                     TrInv (X, X ′ ) ≜ x′ < x ∧ x > 0 is a well-founded transi-
 7        return ⟨Init, Tr ′ , Sink , X⟩                                   tion invariant that proves the termination of TS . Section III
 8    i←i−1
        ′    (0)                                                           presents the algorithm that automates this generalisation via
 9 Init (X       ) ← Init(X (0) ) ∧
                                                                           Craig interpolation.
     ¬QE(∃X (1) , . . . , X (n) .Init(X (0) ) ∧ Tr n ∧ Sink (X (n) ))
                   ′
10 return ⟨Init , Tr , Sink , X⟩
                                                                           III. T ERMINATION A NALYSIS VIA I NTERPOLATION - BASED
                                                                                     T RANSITION I NVARIANT G ENERATION
                                                                              We present a new termination analysis approach that lever-
If Inv (X) is a recurrent set, then the transition system is               ages safety verification to generate a well-founded transition
nonterminating. Otherwise, SNA returns UNKNOWN.                            invariant via interpolation. At each iteration, our procedure
   The B LOCK T ERM procedure takes as input a safety prob-                constructs a trace from the initial states to a sink state. A
lem P and a trace formula Tr n (X (0) , . . . , X (n) ) such that          candidate well-founded transition invariant is then constructed
Init(X (0) )∧Tr n (X (0) , . . . , X (n) )∧Sink (X (n) ) is satisfiable.   based on the overapproximation of the terminating trace.
The algorithm iteratively analyses the trace from the last                 If the candidate is valid for all reachable states (meaning
transition backwards. Using QE, Algorithm 2 computes Si                    it is a transition invariant), termination is concluded. The
and Si+1 , encoding the states that are reachable after i and              interpolation-based approach enables efficient generation of a
i+1 transitions from Init (lines 3, 4). Then, at line 5 it checks          transition invariant guided by the termination conditions.
if Si (X) ∧ Tr (X, X ′ ) ∧ ¬Si+1 (X ′ ) is satisfiable.Intuitively,
with this query, the algorithm checks if it is possible to take            A. Interpolation-based Generation of Well-Founded Transition
an alternative transition at step i, one that does not lead to             Invariants
the sink states. If it is possible, the algorithm blocks the states           The core of our approach is T R I NV G EN, a procedure
deterministically leading to the sink states by excluding them             for the automated interpolation-based generation of well-
from the transition relation (line 6). If the whole trace is               founded transition invariants. Given a transition system and
deterministic (it is not possible to take an alternative transition        a terminating trace, it constructs a disjunctively well-founded
along the trace), B LOCK T ERM blocks the subset of initial                approximation of the trace. If the resulting formula constitutes
states deterministically leading to sink (line 9).                         a transition invariant over all reachable states, it witnesses
                                                                           termination.
Lemma 1. If Algorithm 1 returns NONTERM, then the
                                                                              The procedure consists of five steps: (1) Computing NT n ,
transition system is nonterminating, cf. [22].
                                                                           the formula encoding states from which non-sink states can
Example 1. Consider a transition system TS = ⟨Init, Tr , X⟩                be reached within n transitions. NT n is used to construct
with X = {x}, Init(X) ≜ ⊤, and Tr (X, X ′ ) ≜ (x′ = x −                    the interpolant. The negation of NT n encodes the states
                   Transition Invariant Generation                                                   all variables from the formula except for X (0) . Construction
                                        DNFize interpolant
                                                               Construct TrInv(x,x'),
                                                                 preserving well-
                                                                                                     of NT n enables the overapproximation of the trace.
                 Construct states,                              founded disjuncts
   START        nonterminating in
               n transitions: NTn(x)
                                                                                        <TrInv, C>
                                                                                                     Example 2. Consider TS = ⟨Init, Tr , X⟩ with Init ≜ x > 0,
                                                               Construct states C(x),
                                       Overapproximate the
                                       Trn via interpolation
                                                                where TrInv is valid
                                                                transition invariant
                                                                                                     Tr (X, X ′ ) ≜ (x′ = x − 1 ∨ x′ = x − 2) ∧ (x > 0 ∨ x < −10),
                                                                                                     X ≜ {x}. The sink states are Sink (X) ≜ x ≤ 0 ∧ x ≥ −10.
                                                                                                     For n = 1, quantifier elimination yields NT 1 (X) = x >
Figure 2. Execution Flow of Interpolation-based Transition Invariant Gener-
                                                                                                     1 ∧ x < −10: states from which ¬Sink is reachable in one
ation                                                                                                transition.
                                                                                                       Step 2: Interpolation (line 2). The following formula is
 Algorithm 3: T R I NV G EN(P, Tr n , TrInv ).
                                                                                                     unsatisfiable by construction since any state that satisfies
  Input : Safety problem P = ⟨Init, Tr , Sink , X⟩, transition                                       ¬NT n must reach Sink within at most n steps:
             trace Tr n (X (0) , X (1) , . . . , X (n) ), candidate
             transition invariant TrInv (X, X ′ )                                                        ¬NT n (X (0) ) ∧ Tr n (X (0) , . . . , X (n) ) ∧ ¬Sink (X (n) )
  Output: Updated transition invariant TrInv (X, X ′ ) and
             formula C(X) encoding states covered by                                                    This allows us to compute a Craig interpolant that over-
             transition invariant                                                                    approximates the trace Tr n . Crucially, the usage of the sink
       n    (0)
1 NT (X         ) ← QE(∃X (1) , . . . , X (n) .                                                      states for the interpolant construction allows the interpolant to
    Tr (X , X (1) , . . . , X (n) ) ∧ ¬Sink (X (n) ))
        n   (0)
                                                                                                     capture the reason why the particular trace is terminating.
              ′
2 itp(X, X ) ←
                                                                                                        Step 3: DNF underapproximation (line 3). For a transition
    I TP(Tr n (X, . . . , X ′ ), ¬NT n (X) ∧ ¬Sink (X ′ ))
              ′
3 Cs(X, X ) ← T O DNF(itp)
                                                                                                     invariant to witness termination, it must be disjunctively well-
                                                                                                     founded: every disjunct must encode a well-founded relation.
                          W
4 TrInv ← TrInv ∨            i {di ∈ Cs | ∃ ranking function f (X)}
                                         ′      ′′            ′
5 C(X) ← Sink(X) ∨ ¬QE(∃X , X . Tr (X, X ) ∧                                                         Converting the interpolant to DNF would simplify the well-
      Id(X ′ , X ′′ ) ∨ TrInv (X ′ , X ′′ ) ∧ ¬TrInv (X, X ′′ ))
                                           
                                                                                                     foundedness check for separate disjuncts. However, complete
6 return ⟨TrInv , C⟩
                                                                                                     DNF conversion can cause an exponential blowup in formula
                                                                                                     size and take a significant amount of time. Moreover, even a
                                                                                                     complete DNF is not guaranteed to yield a transition invariant.
from which Sink is guaranteed to be reached in at most                                                  Instead, our algorithm follows a lazy approach: it constructs
n transitions. (2) Constructing an over-approximation of the                                         an under-approximating DNF formula on demand. Specifi-
terminating trace via interpolation. The usage of sink states                                        cally, the algorithm constructs disjuncts as follows: (1) the
allows the interpolant to capture the reason for termination. (3)                                    SMT solver produces a model that satisfies itp; (2) the literals
Converting the interpolant into an underapproximating DNF                                            satisfied by this model are extracted and conjoined to form a
formula. This enables efficient ranking function synthesis for                                       single disjunct; (3) this disjunct is blocked from itp and the
each disjunct. (4) Filtering disjuncts, preserving only disjuncts                                    process repeats until some m disjuncts are constructed. The
that encode well-founded relations. These disjuncts are used to                                      result is a formula:
construct a candidate transition invariant. Only well-founded                                                                              m
                                                                                                                                           _
relations are preserved, as transition invariant needs to be                                                                Cs(X, X ′ ) ≜     di
disjunctively well-founded to witness termination. (5) Com-                                                                                  i=0
puting the formula C(X), encoding states for which candidate                                         where each di is a conjunction, and Cs(X, X ′ ) → itp(X, X ′ ).
transition invariant is valid. Transition invariant needs to be                                      This approach significantly reduces formula size and speeds up
valid only over the reachable states to conclude termination.                                        both the DNF construction and subsequent well-foundedness
Therefore, if all reachable states satisfy C(X), then TS is                                          check, while preserving correctness: in the worst case, Cs fails
terminating. The overall flow of the procedure is illustrated in                                     to be a transition invariant, but this is also possible even with
Figure 2 and described in Algorithm 3.                                                               a complete DNF conversion.
   Algorithm 3 takes as input a safety problem P = ⟨Init, Tr ,                                          Step 4: Filtering Well-Founded Disjuncts (line 4). For each
Sink , X⟩, a transition trace Tr n (X (0) , X (1) , . . . , X (n) ), and a                           disjunct d(X, X ′ ) ∈ Cs(X, X ′ ), the algorithm checks if
transition invariant formula TrInv (X, X ′ ). It returns a tuple of                                  d(X, X ′ ) encodes a well-founded relation. Our technique syn-
formulas ⟨TrInv , C⟩, where TrInv (X, X ′ ) is a disjunctively                                       thesizes linear ranking functions automatically following [2]
well-founded transition invariant candidate, and C(X) is a                                           for checking the existence of a ranking function. The dis-
formula encoding the states for which TrInv is a valid                                               juncts admitting a ranking function are preserved, the rest are
transition invariant. It proceeds in the following steps:                                            discarded. The resulting formula is disjoined with the input
   Step 1: Computing NT n (line 1). NT n (X) encodes all                                             candidate transition invariant TrInv .
states from which a non-sink state is reachable within n transi-                                        Step 5: Synthesis of the states for which transition invariant
tions. The following property defines it: ∀X (0) .NT n (X (0) ) ↔                                    is valid (line 5). If TrInv is a transition invariant over all
                                                                                                     reachable states, then TS terminates, since every disjunct
   ∃X (1) , . . . , X (n) .Tr n (X (0) , . . . , X (n) ) ∧ ¬Sink (X (n) )
                                                                                                     encodes a well-founded relation. To verify this, the procedure
  NT n is constructed with quantifier elimination, eliminating                                       computes the formula C(X) encoding the states over which
TrInv is a valid transition invariant (including sink states, as                                               START
any candidate invariant is valid over Sink ).
                                                                                          P = <Init, Tr, Sink, X>           Transition Invariant-based Termination
Definition 6 (Coverage formula). Given a transition system                                <SAFE, Inv>                      <UNSAFE, Trn>      Transition
                                                                                                            Safety check
TS = ⟨Init, Tr , X⟩ and a formula TrInv (X, X ′ ), a formula                                                    of P
                                                                                                                                               Invariant
                                                                                                                                              Generation
C(X) is called coverage, if the following holds ∀X, X ′ , X ′′ :                                                                                    <TrInv, C>
                                                                                No                      Updated P
                                         ′                 ′                           Inv is a
                      C(X) ∧ Tr (X, X ) →TrInv (X, X )              UNKNOWN          Recurrent set
                                                                                                                                            <SAFE, *>
                     ′              ′   ′′                 ′′                                                                                               Safety check
   C(X) ∧ Tr (X, X ) ∧ TrInv (X , X ) →TrInv (X, X )                              Yes
                                                                                                                            TERMINATING                  of <Init, Tr, ¬C, X>


That is, TrInv is a transition invariant over states that satisfy               NONTERMINATING
                                                                                                           P = BlockTerm
                                                                                                                                           <UNSAFE, *>

C(X).
    Similarly to NT n , C(X) is constructed by applying quan-
tifier elimination, negating the states for which TrInv is not a    Figure 3. Execution Flow of Interpolation-based Transition Invariant Gener-
transition invariant. It is a coverage formula by construction.     ation (New components are placed in a grey block, lines 5,6,8).

Example 3. Continuing Example 2, suppose the procedure
constructs an interpolant itp(X, X ′ ) ≜ x′ < x ∧ (x > 0 ∨          Therefore the base case holds.
x < −10). Afterwards, algorithm would construct DNF form:             Inductive step: Assume R(X) ∧ Tr n (X, . . . , X ′ ) →
(x′ < x ∧ x > 0) ∨ (x′ < x ∧ x < −10), and since the second         TrInv (X, X ′ ) for some n ≥ 1. Let Tr n+1 (X, X ′′ ) hold, so
disjunct is not well founded, it would be dropped, resulting        there ∃X, X ′ , . . . , X ′′ .R(X)∧Tr (X, X ′ )∧Tr n (X ′ , . . . , X ′′ ).
in TrInv (X, X ′ ) ≜ x′ < x ∧ x > 0. Quantifier elimination at      Since R(X) is a formula encoding all reachable states: R(X)∧
line 5 then returns C(X) ≜ (x ≥ −10 ∧ x ≤ 0) ∨ x > 0.               Tr (X, X ′ ) ∧ Tr n (X ′ , . . . , X ′′ ) → R(X) ∧ Tr (X, X ′ ) ∧
   Note. If ¬C(X) is unreachable, then TrInv (X, X ′ ) is a         R(X ′ )∧Tr n (X ′ , . . . , X ′′ ). Since R(X)∧Tr n (X, . . . , X ′ ) →
disjunctively well-founded transition invariant over all reach-     TrInv (X, X ′ ), then trivially R(X) ∧ Tr (X, X ′ ) ∧ R(X ′ ) ∧
able states, and witnesses termination of the transition sys-       Tr n (X ′ , . . . , X ′′ ) → R(X) ∧ Tr (X, X ′ ) ∧ TrInv (X ′ , X ′′ ).
tem. For illustration, the transition invariant in Example 3        Now, due to the fact that R(X) → C(X), the following holds:
is sufficient to prove termination since the states satisfying      R(X) ∧ Tr (X, X ′ ) ∧ TrInv (X ′ , X ′′ ) → C(X) ∧ Tr (X, X ′ ) ∧
¬C(X) ≜ x < −10 cannot be reached within TS .                       TrInv (X ′ , X ′′ ). By the lemma hypothesis:

Lemma 2. Let TS = ⟨Init, Tr , X⟩ be a transition system               C(X) ∧ Tr (X, X ′ ) ∧ TrInv (X ′ , X ′′ ) → TrInv (X, X ′′ ).
and let C(X) be a formula such that ¬C(X) is unreachable
in TS . If TrInv (X, X ′ ) is a finite disjunction of formulas        Therefore, through the chain of implications, we have:
encoding well-founded relations and satisfies ∀X, X ′ , X ′′ :                 R(X) ∧ Tr n+1 (X, X ′ ) → TrInv (X, X ′ ).
                      C(X) ∧ Tr (X, X ′ ) →TrInv (X, X ′ )
                                                                      Thus TrInv is a disjunctively well-founded transition in-
   C(X) ∧ Tr (X, X ) ∧ TrInv (X ′ , X ′′ ) →TrInv (X, X ′′ )
                     ′
                                                                    variant over all reachable states, and TS is terminating.
then TS is terminating.
                                                                    B. Interpolation-based Termination Analysis
Proof. We show that TrInv is a disjunctively well-founded
                                                                       This subsection presents the full termination analysis pro-
transition invariant over the reachable states of TS , from
                                                                    cedure using the interpolation-based transition invariant gen-
which termination follows by [29].
                                                                    eration. It integrates T R I NV G EN into the main loop of Algo-
   Disjunctive well-foundedness.     By construction, for each
                         W                                          rithm 1. At each iteration, instead of only blocking terminating
disjunct di of TrInv = i di there exists a ranking function.
                                                                    states, the algorithm also constructs a transition invariant
Therefore, every disjunct is a logical encoding of well-founded
                                                                    candidate. The overall flow is shown in Figure 3.
relation [2]. Hence TrInv is disjunctively well-founded.
                                                                       The Algorithm 4 takes as input a safety problem P =
   Transition invariant. We show that ∀X, X ′ . R(X) ∧
                                                                    ⟨Init, Tr , Sink , X⟩, where Init and Tr encode the initial
Tr + (X, X ′ ) → TrInv (X, X ′ ), where R(X) denotes the
                                                                    states and transition relation, Sink is the formula encoding
reachable states of TS , by induction on the number of steps
                                                                    sink states, and X is the set of variables over which the
n in Tr + (X, X ′ ).
                                                                    transition system is defined. As an output, the algorithm
   Base case (n = 1): It is needed to prove that:
                                                                    returns NONTERM if TS is nonterminating, TERM if it
            R(X) ∧ Tr (X, X ′ ) → TrInv (X, X ′ )                   is terminating, and UNKNOWN if the procedure cannot
                                                                    determine the final result. The procedure maintains a candi-
Since ¬C(X) is unreachable, R(X) → C(X), and therefore
                                                                    date transition invariant TrInv (X, X ′ ). During the execution,
R(X) ∧ Tr (X, X ′ ) → C(X) ∧ Tr (X, X ′ ).
                                                                    TrInv is extended with new disjuncts, which are generated by
  The following assumption holds by the lemma statement:
                                                                    the T R I NV G EN procedure, and encode well-founded relations.
            C(X) ∧ Tr (X, X ′ ) → TrInv (X, X ′ ).                  Changes to the original SNA are at lines 5, 6, and 8.
 Algorithm 4: Interpolation-based Transition Invariant              safety check for ⟨Init, Tr , ¬C, X⟩ returns UNSAFE, since
 Generation for Proving and Disproving Termination.                 states with u < 10 are reachable from Init. B LOCK T ERM
   Input : Safety problem P = ⟨Init, Tr , Sink , X⟩                 then blocks the states that are guaranteed to reach sink:
   Output: TERM | NONTERM | UNKNOWN                                 Tr (X, X ′ ) ← Tr (X, X ′ ) ∧ x′ > 0.
   Data : TrInv - formula that encodes transition invariant            The algorithm calls S AFETY C HECK(P ), which returns
 1 TrInv ← ⊥
                                                                    SAFE with inductive invariant Inv (X) ≜ x > 0. However,
 2 while ⊤ do
 3   ⟨res, ϕ = Tr n or Inv ⟩ ← S AFETY C HECK(P )                   Inv is not a recurrent set, so Algorithm 4 returns U NKNOWN.
 4   if res = UNSAFE then                                              The root cause why the algorithm cannot prove termination
 5       ⟨TrInv , C⟩ ← T R I NV G EN(P, ϕ, TrInv )                  is that TrInv does not cover states with u < 10. It captures
 6       ⟨res ′ , ⟩ ← S AFETY C HECK(⟨Init, Tr , ¬C, X⟩)            why the system terminates when u = 10, but not the global
 7       if res ′ = UNSAFE then P ← B LOCK T ERM(P, ϕ)              argument: u grows until at most u = 10, after which x de-
 8       else return TERM
 9   else
                                                                    creases monotonically. A complete termination proof requires
10       if ∀X.ϕ(X) → ∃X ′ .Tr (X, X ′ ) ∧ ϕ(X ′ ) then             a second disjunct covering the u < 10 region. In Section IV,
11           return NONTERM                                         we present an extension that focuses on the state space for
12       return UNKNOWN                                             which the transition invariant candidate is not valid, aiming to
                                                                    extend the transition invariant.
                                                                    C. Correctness
   Every iteration of Algorithm 4, similarly to the Algorithm 1,
begins with the safety check at line 3. The algorithm handles         This subsection proves the soundness of the introduced
two possible cases:                                                 approach. We first prove that when the algorithm returns
     a) UNSAFE: A terminating trace Tr n exists. The al-            TERM, the transition system is terminating, and then we prove
gorithm calls T R I NV G EN to extend TrInv and compute the         the correctness for the nontermination.
coverage formula C(X) (line 5). Then, it checks if ¬C(X)            Lemma 3. If Algorithm 4 returns TERM, then the transition
is reachable from the initial states (line 6). If ¬C(X) is          system ⟨Init, Tr , X⟩ is terminating.
reachable, the algorithm refines the safety problem by block-
ing the states that deterministically lead to termination via       Proof. TERM is returned only at line 8. It means that there
B LOCK T ERM, and the loop continues. Otherwise, TrInv is a         exists a transition invariant TrInv which is valid over states
transition invariant over all reachable states, and the algorithm   C(X), and ¬C(X) is unreachable from the initial states.
concludes termination.                                              The safety problem is updated iteratively, blocking the states
                                                                    that deterministically lead to termination, so in the end the
     b) SAFE: No sink state is reachable, and there exists                        ′   ′                          ′
an inductive invariant Inv (X). If Inv (X) is a recurrent set,      Vm= ⟨Init , Tr , Sink ′, X⟩, where Init
                                                                    P
                                                                                                             ′
                                                                                                                   (X)
                                                                                                                     Vl = Init(X) ′
                                                                                                                                      ∧
the system is nonterminating. Otherwise, the algorithm returns         i=0 ¬S i (X)  and  Tr    =  Tr  (X, X   )   ∧   j=0 ¬Sj (X   )  .
UNKNOWN as the analysis is inconclusive.                            According to Lemma 2, transition system ⟨Init ′ , Tr ′ , X⟩ is
                                                                    terminating, since TrInv is a disjunctively well-founded tran-
Example 4. Consider TS from Example 2 with Init ≜ x > 0,            sition invariant over all reachable
                                                                                                    Wm states.
Tr ≜ (x′ = x−1∨x′ = x−2)∧(x > 0∨x < −10), X ≜ {x}.
                                                                                                                         Wl
                                                                        Since the states satisfying i=0 Si (X) and j=0 Sj (X ′ )
Preprocessing computes Sink ≜ x ≤ 0 ∧ x ≥ −10. Then, the            deterministically lead to the termination, every trace of
algorithm is called with P = ⟨Init, Tr , Sink , X⟩.                 ⟨Init, Tr , X⟩ either follows Tr ′ or passes through a blocked
   The safety check detects a trace Tr 1 reaching Sink .            state, which leads to termination. Hence ⟨Init, Tr , X⟩ is
T R I NV G EN produces a transition invariant candidate             terminating.
TrInv (X, X ′ ) ≜ x′ < x ∧ x > 0 and the formula
C(X) ≜ (x ≤ 0 ∧ x ≥ −10) ∨ x > 0. The safety check                  Lemma 4. If Algorithm 4 returns NONTERM, then the
for ⟨Init, Tr , ¬C(X), X⟩ returns SAFE, and the algorithm           transition system ⟨Init, Tr , X⟩ is nonterminating.
concludes that the transition system is terminating.                Proof. The proof of this lemma follows directly from
   Limitation of the approach. Consider a different TS , with       Lemma 1, as the nontermination analysis in Algorithm 4
X = {x, u}, Init(X) ≜ u < 10 ∧ x > 0, and Tr (X, X ′ ) ≜            follows exactly the same process as Algorithm 1.
((x′ = x − 1 ∧ u′ = u) ∨ (x′ = x + 1 ∧ u′ = u + 1 ∧ u <
10)) ∧ x > 0. Intuitively, each transition either decrements x         IV. E XTENDED I NTERPOLATION - BASED T RANSITION
(and keeps u unchanged), or increments both x and u until           I NVARIANT G ENERATION FOR P ROVING AND D ISPROVING
u < 10. Once u = 10, only the decrementing transition is                                 T ERMINATION
possible, and x decreases monotonically to zero. Hence TS is           Algorithm 4 is already capable of proving termination effi-
terminating. The sink states are Sink (X) ≜ x ≤ 0.                  ciently through the construction of transition invariants. This
   The Algorithm 4 detects a trace Tr 1 (X (0) , X (1) ) reach-     section describes an extension of the algorithm that aims to
ing Sink states. T R I NV G EN constructs transition invariant:     improve interaction between termination and nontermination
TrInv (X, X ′ ) ≜ x′ < x ∧ x > 0. The coverage formula              analyses. Additionally, we present further extensions to the
is computed as: C(X) ≜ x ≤ 0 ∨ (x > 0 ∧ u = 10). The                original SNA algorithm that improve overall performance.
                                                          START
                                                                                                                              Algorithm 5: Extended Interpolation-based Transition
                                      P = <Init, Tr, Sink, X>
                                                                                                                              Invariant Generation for Proving and Disproving Ter-
          P = Prs.pop()                                                                         P = Prs.pop()
                                                                                                                              mination.
 Prs.push(<Init, Tr,
                                    <SAFE, Inv>                  <UNSAFE, Trn>
                                                                                     Transition
                                                                                                                                Input : Safety problem P
     Sink', X>)                                       Safety check
                                                          of P
                                                                                      Invariant                                 Output: TERM | NONTERM
                                                                                     Generation

                                                                                 <TrInv, C>
                                                                                                                                Data : TrInv - candidate transition invariant, Prs - stack
   No                                                           P = Prs.pop()                            Prs.push(<Sm, Tr,
                                                        No                                                   Sink, X>)                    of safety problems
                   Is SAT                     Is UNSAT               <SAFE, *>                                                1 TrInv ← ⊥
     Inv is a                                                                        Safety check
                            Init(X) /\ Tr(X,X')        Prs is empty?
   Recurrent set                                                                  of <Init, Tr, ¬C, X>                        2 Prs ← [P ]
                                                                                                          Construct states    3 while ⊤ do
  Yes                                                   Yes                                              Sm not covered by
                                                                           <UNSAFE, *>
                                                                                                               TrInv          4   P ′ ≡ ⟨Init, Tr , Sink , X⟩ ← Prs.pop()
NONTERMINATING                                      TERMINATING                       Prs.push(                               5   ⟨res, ϕ⟩ ← S AFETY C HECK(P ′ )
                                                                                     BlockTerm)
                                                                                                                              6   if res = UNSAFE then
                                                                                                                              7       ⟨TrInv , C⟩ ← T R I NV G EN(P ′ , ϕ, TrInv )
                                                                                                                              8       ⟨res ′ , ϕ′ ⟩ ← S AFETY C HECK(⟨Init, Tr , ¬C, X⟩)
Figure 4. Extended Interpolation-based Termination Analysis (new compo-                                                       9       if ⟨res ′ , ϕ′ ⟩ = ⟨UNSAFE, Tr m ⟩ then
nents are highlighted in dark orange and dark blue colors).                                                                  10          Prs.push(B LOCK T ERM(P ′ , ϕ))
                                                                                                                             11          Sm (X) ← QE(∃X (0) , . . . , X (m−1) .Init(X (0) ) ∧
                                                                                                                                           ϕ′ (X (0) , . . . , X (m) ) ∧ ¬C(X (m) ))[X (m) 7→ X]
The high-level flow of the extended algorithm can be seen                                                                    12          Prs.push(⟨Sm , Tr , C, X⟩)
in Figure 4.                                                                                                                 13       else
                                                                                                                             14          if Prs = ∅ then return TERM
A. Analysis of States for which Transition Invariant is not                                                                  15          else continue
Valid                                                                                                                        16   else
                                                                                                                             17       if ∀X.ϕ(X) → ∃X ′ .Tr (X, X ′ ) ∧ ϕ(X ′ ) then
                                                                                                                             18          return NONTERM
   A transition invariant candidate can be used to guide the                                                                 19       if UNSAT? Init(X) ∧ Tr (X, X ′ ) then
termination analysis. Particularly, Algorithm 4 constructs the                                                               20          if Prs = ∅ then return TERM
formula C(X) encoding states for which the transition invari-                                                                21          else continue
ant is valid. If ¬C(X) is reachable, there exist states for which                                                            22       Sink ′ (X) ← ¬QE(∃X ′ .Tr (X, X ′ ))
                                                                                                                             23       Prs.push(⟨Init, Tr , Sink ′ , X⟩)
the transition invariant is not valid, and which potentially can
lead to nontermination. The intuition is to compute the reach-
able states Sm within ¬C(X) (which corresponds to line 11
of Algorithm 5). Then, it is possible to run (non)termination                                                                   If ¬C is not reachable, TrInv proves termination of the
check for these particular states within TS (line 12).                                                                       currently analyzed TS (the last TS popped from the stack),
   In the case of termination, the algorithm produces a wit-                                                                 and the number of remaining subproblems decreases. If the
ness transition invariant that extends the transition invariant                                                              stack is empty, Algorithm 5 returns TERM. The algorithm
of the original system, making it valid for more states. If                                                                  incorporates two further extensions.
nontermination is proved for Sm , then the original TS is also                                                                  Simple termination check (line 19). When the safety check
nonterminating, since Sm is reachable from the initial states.                                                               returns SAFE and ϕ(X) is not a recurrent set, the algorithm
                                                                                                                             additionally checks whether it is possible to take a transition
B. Overall Algorithm                                                                                                         from the initial states by querying:
    Algorithm 5 extends Algorithm 4 to enable more efficient
                                                                                                                                                    Init(X) ∧ Tr (X, X ′ )
(non)termination analysis. First, in addition to maintaining the
transition invariant, the algorithm maintains a stack of safety                                                              If this formula is unsatisfiable, then no transition can be taken
problems to be analyzed: Prs (line 2). At each iteration, the                                                                from the initial states (or all transitions are blocked, meaning
algorithm pops a safety problem from the stack and analyzes                                                                  all reachable states deterministically lead to termination), and
it. The stack allows the algorithm to focus on (non)termination                                                              the system is trivially terminating.
analysis of particular reachable states within TS . The original                                                                Refinement of Sink states (lines 22, 23). When ϕ(X) is
safety problem always remains in the Prs stack.                                                                              not a recurrent set, this is often because B LOCK T ERM has
    The postprocessing phase of transition invariant construc-                                                               eliminated all transitions leading to Sink . This means that the
tion is the main change to Algorithm 4. When ¬C is reachable,                                                                produced ϕ contains sink states due to the updated Tr . New
the extended algorithm performs three actions: (1) it pushes                                                                 formula encoding sink states is computed as:
the B LOCK T ERM-refined problem (line 10); (2) it computes
a formula encoding reachable states, for which transition                                                                                  Sink ′ (X) = ¬QE(∃X ′ .Tr ′ (X, X ′ ))
invariant candidate is not valid (line 11); and (3) it pushes a
                                                                                                                                Formula Sink ′ replaces Sink in the safety problem, enabling
new subproblem to analyze for termination (line 12), with Sm
                                                                                                                             the analysis to proceed instead of returning UNKNOWN.
as the initial states. This allows the algorithm to concentrate on
proving termination or nontermination of particular reachable                                                                Lemma 5. If Algorithm 5 returns TERM, then the original
states.                                                                                                                      transition system ⟨Init, Tr , X⟩ is terminating.
Proof. TERM is returned at line 14 or line 19. As in                                                     Table I
Algorithm 4, to return TERM, the termination conditions                             C OMPARISON OF I TP T IG + WITH SNA AND I TP T IG .
need to be satisfied for the transition   system ⟨Init ′ , Tr ′ , X⟩,      Algorithm      Total   Terminating      Nonterminating      Uniquely
where Init (X) = Init(X) ∧ i ¬Si (X), and Tr ′ (X, X ′ ) =
            ′                    V
                                                                               SNA         343         0                343               7
                              Wm                Wl                           I TP T IG     521        186               335               7
Tr (X, X ′ ) ∧ j ¬Sj (X ′ ). i=0 Si (X) and j=0 Sj (X ′ ) are
              V
                                                                            I TP T IG +    761        320               441              240
the states that deterministically lead to termination.
   Case 1. If TERM is returned at line 14, then the termination
                                                                                                         Table II
proof follows directly from Lemma 3. This is the case, since                   C OMPARISON OF I TP T IG + WITH STATE - OF - THE - ART TOOLS .
the original safety problem is preserved in the stack, so if
Prs = ∅, the original safety problem is terminating.                       Algorithm      Total   Terminating      Nonterminating      Uniquely
                                                                              L OAT        525         0                525               48
   Case 2. If TERM is returned at line 19, then formula                       KOAT         562        562                0                26
Init ′ (X) ∧ Tr ′ (X, X ′ ) is unsatisfiable, so no transition is               T2        1002        572               430               40
reachable from Init ′ . Thus, all feasible transitions in the               I TP T IG +    761        320               441                8
original transition system lead to deterministically terminating
states, and the transition system is terminating.
                                                                           The benchmark suite of Integer Transition Systems was
Lemma 6. If Algorithm 5 returns NONTERM, then the                       taken from the Termination Competition [27]. Overall, there
original transition system ⟨Init, Tr , X⟩ is nonterminating.            are 1222 benchmarks (538 nonterminating, 665 terminating,
Proof. NONTERM is returned at line 18, where ϕ(X) is a                  and 19 unknown). We excluded 42 trivially terminating bench-
recurrent set for the currently considered TS ⟨Init ′ , Tr ′ , X⟩.      marks from the evaluation (termination of which can be
By Lemma 1, there exists a recurrent set in the transition              detected by trivial syntactic checks), which are solved by
system ⟨Init ′ , Tr ′ , X⟩, and since Tr ′ (X, X ′ ) → Tr (X, X ′ )     all tools. The evaluation was executed with the 120 seconds
and Init ′ is reachable from Init (or it is Init), this recurrent       timeout (the increase of the timeout does not significantly
set witnesses nontermination of TS .                                    influence the evaluation).
                                                                           Table I gives the experimental results for I TP T IG +, SNA,
           V. I MPLEMENTATION AND E VALUATION                           and I TP T IG. It confirms that I TP T IG + consistently outper-
  This section presents the implementation details and exper-           forms both SNA and I TP T IG for terminating and nonterminat-
imental evaluation of our approach.                                     ing instances, solving 240 instances solved by neither SNA nor
                                                                        I TP T IG. We attribute this to I TP T IG +’s generation of focused
A. Implementation                                                       sub-problems, which allows the analysis to concentrate on
   We implemented the prototypes of Algorithms 1, 4, and                specific reachable states. This benefits recurrent set detection
5 inside of G OLEM; we refer to these implementations as                by focusing the analysis on specific states not covered by
SNA, I TP T IG, and I TP T IG +. G OLEM was chosen because              the transition invariant. It also benefits termination proving by
it supports multiple different safety verification procedures,          extending the transition invariant with additional disjuncts that
such as Property-Directed Reachability [30] (PDR), Transition           cover different regions of the reachable state space. In answer
Power Abstraction [31] (TPA), and Interpolation-based Model             to RQ1, the combination of termination and nontermination
Checking [32]. Additionally, we used quantifier elimination,            reasoning in I TP T IG + significantly outperforms either individ-
already implemented in G OLEM. For SMT queries and inter-               ual approach in isolation.
polation, our implementation uses the O PEN SMT solver [33],               Interestingly, I TP T IG + behaves differently depending on the
[34]. O PEN SMT is integrated within G OLEM and provides                underlying safety verification engine: with TPA it solved 761
native support for interpolation.                                       instances and with PDR – 755. That said, it solved 24 (resp.
                                                                        18) benchmarks uniquely with TPA (resp. PDR).
B. Evaluation
                                                                           Figure 5 shows a scatter plot comparing I TP T IG +
   We compared I TP T IG + against SNA and I TP T IG to evaluate        against state-of-the-art termination analyzers, where each axis
the effect of combining termination and nontermination analy-           represents the solving time in seconds for a given tool. Orange
ses. Additionally, we evaluated I TP T IG + against several state-      squares denote nonterminating instances; blue crosses denote
of-the-art tools: L OAT [28] (version eacb74b), KOAT [28]               terminating instances. Points above the diagonal indicate
(version 41cb681), T2 [18] (version 10f1373). The evaluation            instances where I TP T IG + is faster than the competitor.
focused on termination analysis of Integer Transition Systems.          I TP T IG + solves 761 benchmarks, with T2 solving 1002,
Experiments were conducted on Ubuntu 20.04 machine with                 KOAT 562, and L OAT 525 instances, the full comparison can
an AMD EPYC 7452 32-core processor and 8x32 GiB RAM.                    be seen in Table II. As shown in Figure 5, I TP T IG +, despite
Our evaluation addressed the following research questions:              being a prototype implementation, is competitive with state-
   • RQ1: How does extending SNA with the termination                   of-the-art termination analyzers. Among all compared tools,
     procedure affect verification performance?                         I TP T IG + uniquely solves eight instances. Notably, two of
   • RQ2: How does I TP T IG + perform compared to state-of-            these — juLinkedListCreateAddAll.jar-obl-11
     the-art tools?                                                     and      juLinkedListCreateAddAllAt.jar-obl-17
                              Figure 5. Comparison of I TP T IG + with KOAT, L OAT and T2 (runtime in seconds).



have never been solved in the Termination Competition.                  to guide transition invariant synthesis with respect to the actual
I TP T IG + found recurrent sets and proved nontermination              termination conditions, producing property-directed invariants.
for them. In answer to RQ2, I TP T IG + is competitive with                                    VII. C ONCLUSION
state-of-the-art tools and solves instances not solved by any
tool in the Termination Competition.                                       We have presented an interpolation-based approach to tran-
                                                                        sition invariant generation for proving and disproving termi-
                    VI. R ELATED W ORK                                  nation of infinite-state systems. The approach extends safety-
                                                                        based nontermination analysis with a termination proving ca-
   Recent years have seen significant advances in automated             pability, unifying the two within a single framework. Our key
techniques for both termination and nontermination analysis.            insight is to exploit terminating traces produced by the SNA
   Nontermination. Nontermination analysis is typically cen-            as a source of structural information, using Craig interpolation
tered on the construction of recurrent sets — sets of states from       to construct well-founded transition invariants guided by the
which execution cannot escape [10], [17]–[20], [22]. These              termination conditions. The interaction between termination
techniques range from template-based synthesis to safety-               and nontermination reasoning is central to our technique:
check-based recurrent set construction, the latter of which             transition invariants focus the nontermination analysis on not
our approach directly extends [22]. An alternative approach             covered states, while SNA provides terminating traces that
detects nontermination by identifying lasso-shaped executions           drive invariant generation. Grounding the approach in safety
— finite paths leading to a cycle — via bounded model check-            verification provides a robust foundation, enabling efficient
ing [23]. Leike and Heizmann [24] use geometric nontermina-             checking of both termination and nontermination via existing
tion witnesses: finite representations of infinite executions via       safety solvers. We proved the soundness of the algorithm and
sums of geometric series. Unlike the approaches above, which            conducted an extensive experimental evaluation. The results
treat nontermination in isolation, our technique is integrated          demonstrate the benefit of combining termination and nonter-
with termination analysis within a unified framework, so that           mination analysis, and show that our approach achieves com-
intermediate results guide one another.                                 petitive performance against state-of-the-art tools, including
   Termination. The most widely studied approach to ter-                the unique solution of instances never solved by any tool in
mination analysis is the synthesis of ranking functions [2]–            the Termination Competition.
[4], [6], [7], [9]–[11]. State-of-the-art techniques focus on              Acknowledgements. This work was supported in part by
the construction of multiphase or lexicographic ranking func-           SNSF grant No. 200021-236601. We thank Marek Jankola and
tions [4], [10], which significantly broaden the class of pro-          Dirk Beyer for fruitful discussions on termination analysis.
grams for which termination can be proved. However, the
                                                                                                    R EFERENCES
complexity of a transition system can make ranking function
synthesis infeasible. With fixpoint computation, [12] reduces            [1] M. Braverman, “Termination of integer linear programs,” in Computer
                                                                             Aided Verification, 18th International Conference, CAV 2006, Seattle,
termination and nontermination to the validity of a first-                   WA, USA, August 17-20, 2006, Proceedings, ser. Lecture Notes in
order fixpoint formula. Disjunctively well-founded transition                Computer Science, T. Ball and R. B. Jones, Eds. Springer, 2006, pp.
invariants [15], [16], [29], [35] enable over-approximating the              372–385. [Online]. Available: https://doi.org/10.1007/11817963 34
                                                                         [2] A. Podelski and A. Rybalchenko, “A complete method for the
behavior of the transition system. The central challenge there               synthesis of linear ranking functions,” in Verification, Model
is the generation of the transition invariant itself: existing               Checking, and Abstract Interpretation, 5th International Conference,
techniques rely either on template-based generation [16] or on               VMCAI 2004, Venice, Italy, January 11-13, 2004, Proceedings,
                                                                             ser. Lecture Notes in Computer Science, B. Steffen and
the direct construction of a ranking relation from a particular              G. Levi, Eds. Springer, 2004, pp. 239–251. [Online]. Available:
trace [35]. In contrast, our approach uses Craig interpolation               https://doi.org/10.1007/978-3-540-24622-0 20
 [3] S. Kura, H. Unno, and I. Hasuo, “Decision tree learning in cegis-                  Notes in Computer Science, T. Touili, B. Cook, and P. B.
     based termination analysis,” in Computer Aided Verification - 33rd                 Jackson, Eds. Springer, 2010, pp. 89–103. [Online]. Available:
     International Conference, CAV 2021, Virtual Event, July 20-23, 2021,               https://doi.org/10.1007/978-3-642-14295-6 9
     Proceedings, Part II, ser. Lecture Notes in Computer Science, A. Silva        [16] A. Tsitovich, N. Sharygina, C. M. Wintersteiger, and D. Kroening,
     and K. R. M. Leino, Eds. Springer, 2021, pp. 75–98. [Online].                      “Loop summarization and termination analysis,” in Tools and
     Available: https://doi.org/10.1007/978-3-030-81688-9 4                             Algorithms for the Construction and Analysis of Systems - 17th
 [4] A. M. Ben-Amram and S. Genaim, “Ranking functions for linear-                      International Conference, TACAS 2011, Held as Part of the Joint
     constraint loops,” J. ACM, vol. 61, no. 4, pp. 26:1–26:55, 2014.                   European Conferences on Theory and Practice of Software, ETAPS
     [Online]. Available: https://doi.org/10.1145/2629488                               2011, Saarbrücken, Germany, March 26-April 3, 2011. Proceedings,
 [5] M. Heizmann, J. Hoenicke, and A. Podelski, “Termination analysis                   ser. Lecture Notes in Computer Science, P. A. Abdulla and
     by learning terminating programs,” in Computer Aided Verification                  K. R. M. Leino, Eds. Springer, 2011, pp. 81–95. [Online]. Available:
     - 26th International Conference, CAV 2014, Held as Part of the                     https://doi.org/10.1007/978-3-642-19835-9 9
     Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 18-22, 2014.          [17] F. Frohn and J. Giesl, “Proving non-termination and lower runtime
     Proceedings, ser. Lecture Notes in Computer Science, A. Biere and                  bounds with loat (system description),” in Automated Reasoning
     R. Bloem, Eds. Springer, 2014, pp. 797–813. [Online]. Available:                   - 11th International Joint Conference, IJCAR 2022, Haifa, Israel,
     https://doi.org/10.1007/978-3-319-08867-9 53                                       August 8-10, 2022, Proceedings, ser. Lecture Notes in Computer
 [6] J. Giesl, C. Aschermann, M. Brockschmidt, F. Emmes, F. Frohn,                      Science, J. Blanchette, L. Kovács, and D. Pattinson, Eds., vol.
     C. Fuhs, J. Hensel, C. Otto, M. Plücker, P. Schneider-Kamp,                       13385. Springer, 2022, pp. 712–722. [Online]. Available: https:
     T. Ströder, S. Swiderski, and R. Thiemann, “Analyzing program                     //doi.org/10.1007/978-3-031-10769-6 41
     termination and complexity automatically with aprove,” J. Autom.              [18] M. Brockschmidt, B. Cook, S. Ishtiaq, H. Khlaaf, and N. Piterman,
     Reason., vol. 58, no. 1, pp. 3–31, 2017. [Online]. Available:                      “T2: temporal property verification,” in Tools and Algorithms for the
     https://doi.org/10.1007/s10817-016-9388-y                                          Construction and Analysis of Systems - 22nd International Conference,
 [7] Y. Sarita, A. Singh, S. Gomber, G. Singh, and M. Vishwanathan,                     TACAS 2016, Held as Part of the European Joint Conferences on Theory
     “Efficient ranking function-based termination analysis via bidirectional           and Practice of Software, ETAPS 2016, Eindhoven, The Netherlands,
     decompositional search,” in Programming Languages and Systems                      April 2-8, 2016, Proceedings, ser. Lecture Notes in Computer Science,
     - 35th European Symposium on Programming, ESOP 2026, Held                          M. Chechik and J. Raskin, Eds. Springer, 2016, pp. 387–393. [Online].
     as Part of the International Joint Conferences on Theory and                       Available: https://doi.org/10.1007/978-3-662-49674-9 22
     Practice of Software, ETAPS 2026, Turin, Italy, April 11-16, 2026,            [19] M. Brockschmidt, T. Ströder, C. Otto, and J. Giesl, “Automated detection
     Proceedings, Part II, ser. Lecture Notes in Computer Science,                      of non-termination and nullpointerexceptions for java bytecode,” in
     R. Krebbers, Ed. Springer, 2026, pp. 181–209. [Online]. Available:                 Formal Verification of Object-Oriented Software - International
     https://doi.org/10.1007/978-3-032-22723-2 7                                        Conference, FoVeOOS 2011, Turin, Italy, October 5-7, 2011, Revised
 [8] A. M. Ben-Amram, J. J. Doménech, and S. Genaim, “Multiphase-linear                Selected Papers, ser. Lecture Notes in Computer Science, B. Beckert,
     ranking functions and their relation to recurrent sets,” in Static Analysis        F. Damiani, and D. Gurov, Eds. Springer, 2011, pp. 123–141. [Online].
     - 26th International Symposium, SAS 2019, Porto, Portugal, October                 Available: https://doi.org/10.1007/978-3-642-31762-0 9
     8-11, 2019, Proceedings, ser. Lecture Notes in Computer Science,
                                                                                   [20] D. Larraz, K. Nimkar, A. Oliveras, E. Rodrı́guez-Carbonell, and
     B. E. Chang, Ed. Springer, 2019, pp. 459–480. [Online]. Available:
                                                                                        A. Rubio, “Proving non-termination using max-smt,” in Computer
     https://doi.org/10.1007/978-3-030-32304-2 22
                                                                                        Aided Verification - 26th International Conference, CAV 2014, Held as
 [9] C. Urban, A. Gurfinkel, and T. Kahsai, “Synthesizing ranking functions
                                                                                        Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July
     from bits and pieces,” in Tools and Algorithms for the Construction
                                                                                        18-22, 2014. Proceedings, ser. Lecture Notes in Computer Science,
     and Analysis of Systems - 22nd International Conference, TACAS
                                                                                        A. Biere and R. Bloem, Eds. Springer, 2014, pp. 779–796. [Online].
     2016, Held as Part of the European Joint Conferences on Theory
                                                                                        Available: https://doi.org/10.1007/978-3-319-08867-9 52
     and Practice of Software, ETAPS 2016, Eindhoven, The Netherlands,
     April 2-8, 2016, Proceedings, ser. Lecture Notes in Computer Science,         [21] T. C. Le, S. Qin, and W. Chin, “Termination and non-termination
     M. Chechik and J. Raskin, Eds. Springer, 2016, pp. 54–70. [Online].                specification inference,” in Proceedings of the 36th ACM SIGPLAN
     Available: https://doi.org/10.1007/978-3-662-49674-9 4                             Conference on Programming Language Design and Implementation,
[10] G. Fedyukovich, Y. Zhang, and A. Gupta, “Syntax-guided termination                 Portland, OR, USA, June 15-17, 2015, D. Grove and S. M.
     analysis,” in Computer Aided Verification - 30th International                     Blackburn, Eds. ACM, 2015, pp. 489–498. [Online]. Available:
     Conference, CAV 2018, Held as Part of the Federated Logic                          https://doi.org/10.1145/2737924.2737993
     Conference, FloC 2018, Oxford, UK, July 14-17, 2018, Proceedings,             [22] H. Y. Chen, B. Cook, C. Fuhs, K. Nimkar, and P. W. O’Hearn,
     Part I, ser. Lecture Notes in Computer Science, H. Chockler and                    “Proving nontermination via safety,” in Tools and Algorithms for the
     G. Weissenbacher, Eds. Springer, 2018, pp. 124–143. [Online].                      Construction and Analysis of Systems - 20th International Conference,
     Available: https://doi.org/10.1007/978-3-319-96145-3 7                             TACAS 2014, Held as Part of the European Joint Conferences on
[11] D. Riley and G. Fedyukovich, “Exact loop bound analysis,” Proc. ACM                Theory and Practice of Software, ETAPS 2014, Grenoble, France, April
     Program. Lang., vol. 9, no. PLDI, pp. 1814–1837, 2025. [Online].                   5-13, 2014. Proceedings, ser. Lecture Notes in Computer Science,
     Available: https://doi.org/10.1145/3729323                                         E. Ábrahám and K. Havelund, Eds. Springer, 2014, pp. 156–171.
[12] H. Unno, T. Terauchi, Y. Gu, and E. Koskinen, “Modular primal-dual                 [Online]. Available: https://doi.org/10.1007/978-3-642-54862-8 11
     fixpoint logic solving for temporal verification,” Proc. ACM Program.         [23] A. Biere, C. Artho, and V. Schuppan, “Liveness checking as safety
     Lang., vol. 7, no. POPL, pp. 2111–2140, 2023. [Online]. Available:                 checking,” in 7th International ERCIM Workshop in Formal Methods
     https://doi.org/10.1145/3571265                                                    for Industrial Critical Systems, FMICS 2002, ICALP 2002 Satellite
[13] D. Beyer, M. Jankola, and M. Lingsch-Rosenfeld, “Tran-                             Workshop, Málaga, Spain, July 12-13, 2002, ser. Electronic Notes
     sition invariants revisited: Termination witnesses and their                       in Theoretical Computer Science, R. Cleaveland and H. Garavel,
     validation,”     in    Proc.    CAV.      Springer,     2026.     [Online].        Eds., no. 2. Elsevier, 2002, pp. 160–177. [Online]. Available:
     Available: https://www.sosy-lab.org/research/pub/2026-CAV.Transition               https://doi.org/10.1016/S1571-0661(04)80410-9
     Invariants Revisited Termination Witnesses and Their Validation.pdf           [24] J. Leike and M. Heizmann, “Geometric nontermination arguments,” in
[14] B. Cook, A. Podelski, and A. Rybalchenko, “Termination proofs                      Tools and Algorithms for the Construction and Analysis of Systems
     for systems code,” in Proceedings of the ACM SIGPLAN 2006                          - 24th International Conference, TACAS 2018, Held as Part of the
     Conference on Programming Language Design and Implementation,                      European Joint Conferences on Theory and Practice of Software,
     Ottawa, Ontario, Canada, June 11-14, 2006, M. I. Schwartzbach                      ETAPS 2018, Thessaloniki, Greece, April 14-20, 2018, Proceedings,
     and T. Ball, Eds. ACM, 2006, pp. 415–426. [Online]. Available:                     Part II, ser. Lecture Notes in Computer Science, D. Beyer and
     https://doi.org/10.1145/1133981.1134029                                            M. Huisman, Eds. Springer, 2018, pp. 266–283. [Online]. Available:
[15] D. Kroening, N. Sharygina, A. Tsitovich, and C. M. Wintersteiger,                  https://doi.org/10.1007/978-3-319-89963-3 16
     “Termination analysis with compositional transition invariants,” in           [25] W. Craig, “Three uses of the Herbrand-Gentzen theorem in relating
     Computer Aided Verification, 22nd International Conference, CAV                    model theory and proof theory,” The Journal of Symbolic Logic, vol. 22,
     2010, Edinburgh, UK, July 15-19, 2010. Proceedings, ser. Lecture                   no. 3, pp. 269–285, 1957.
[26] M. Blicha, K. Britikov, and N. Sharygina, “The golem horn solver,”
     in Computer Aided Verification - 35th International Conference,
     CAV 2023, Paris, France, July 17-22, 2023, Proceedings, Part II,
     ser. Lecture Notes in Computer Science, C. Enea and A. Lal,
     Eds., vol. 13965. Springer, 2023, pp. 209–223. [Online]. Available:
     https://doi.org/10.1007/978-3-031-37703-7 10
[27] J. Giesl, F. Mesnard, A. Rubio, R. Thiemann, and J. Waldmann,
     “Termination competition (termcomp 2015),” in Automated Deduction
     - CADE-25 - 25th International Conference on Automated Deduction,
     Berlin, Germany, August 1-7, 2015, Proceedings, ser. Lecture
     Notes in Computer Science, A. P. Felty and A. Middeldorp,
     Eds. Springer, 2015, pp. 105–108. [Online]. Available: https:
     //doi.org/10.1007/978-3-319-21401-6 6
[28] N. Lommen and J. Giesl, “Aprove (koat + loat),” in Tools and Algo-
     rithms for the Construction and Analysis of Systems, A. Gurfinkel and
     M. Heule, Eds. Cham: Springer Nature Switzerland, 2025, pp. 205–211.
[29] A. Podelski and A. Rybalchenko, “Transition invariants,” in 19th IEEE
     Symposium on Logic in Computer Science (LICS 2004), 14-17 July
     2004, Turku, Finland, Proceedings. IEEE Computer Society, 2004, pp.
     32–41. [Online]. Available: https://doi.org/10.1109/LICS.2004.1319598
[30] A. R. Bradley and Z. Manna, “Property-directed incremental invariant
     generation,” Formal Aspects Comput., vol. 20, no. 4-5, pp. 379–405,
     2008. [Online]. Available: https://doi.org/10.1007/s00165-008-0080-9
[31] M. Blicha, G. Fedyukovich, A. E. J. Hyvärinen, and N. Sharygina,
     “Transition power abstractions for deep counterexample detection,”
     in Tools and Algorithms for the Construction and Analysis of
     Systems - 28th International Conference, TACAS 2022, ser. Lecture
     Notes in Computer Science, D. Fisman and G. Rosu, Eds.,
     vol. 13243. Springer, 2022, pp. 524–542. [Online]. Available:
     https://doi.org/10.1007/978-3-030-99524-9 29
[32] K. L. McMillan, “Interpolation and sat-based model checking,” in
     Computer Aided Verification, 15th International Conference, CAV
     2003, Boulder, CO, USA, July 8-12, 2003, Proceedings, ser. Lecture
     Notes in Computer Science, W. A. H. Jr. and F. Somenzi,
     Eds., vol. 2725. Springer, 2003, pp. 1–13. [Online]. Available:
     https://doi.org/10.1007/978-3-540-45069-6 1
[33] A. E. J. Hyvärinen, M. Marescotti, L. Alt, and N. Sharygina,
     “Opensmt2: An SMT solver for multi-core and cloud computing,”
     in Theory and Applications of Satisfiability Testing - SAT 2016 -
     19th International Conference, Bordeaux, France, July 5-8, 2016,
     Proceedings, ser. Lecture Notes in Computer Science, N. Creignou and
     D. L. Berre, Eds., vol. 9710. Springer, 2016, pp. 547–553. [Online].
     Available: https://doi.org/10.1007/978-3-319-40970-2 35
[34] R. Bruttomesso, E. Pek, N. Sharygina, and A. Tsitovich, “The opensmt
     solver,” in Tools and Algorithms for the Construction and Analysis
     of Systems, 16th International Conference, TACAS 2010, Held as
     Part of the Joint European Conferences on Theory and Practice
     of Software, ETAPS 2010, Paphos, Cyprus, March 20-28, 2010.
     Proceedings, ser. Lecture Notes in Computer Science, J. Esparza and
     R. Majumdar, Eds. Springer, 2010, pp. 150–153. [Online]. Available:
     https://doi.org/10.1007/978-3-642-12002-2 12
[35] B. Cook, A. Podelski, and A. Rybalchenko, “Abstraction refinement
     for termination,” in Static Analysis, 12th International Symposium,
     SAS 2005, London, UK, September 7-9, 2005, Proceedings, ser.
     Lecture Notes in Computer Science, C. Hankin and I. Siveroni,
     Eds. Springer, 2005, pp. 87–101. [Online]. Available: https:
     //doi.org/10.1007/11547662 8
