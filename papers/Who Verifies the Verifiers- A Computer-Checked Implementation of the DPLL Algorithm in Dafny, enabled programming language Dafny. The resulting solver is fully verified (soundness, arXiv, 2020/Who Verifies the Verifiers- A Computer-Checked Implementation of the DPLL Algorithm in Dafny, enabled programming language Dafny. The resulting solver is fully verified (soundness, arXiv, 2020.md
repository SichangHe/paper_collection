                                                  WHO VERIFIES THE VERIFIERS? A COMPUTER-CHECKED
                                                  IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY ∗

                                                                        CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ

                                               Alexandru Ioan Cuza University, Ias, i
arXiv:2007.10842v1 [cs.LO] 19 Jul 2020




                                               e-mail address: cezar.andrici@gmail.com

                                               Alexandru Ioan Cuza University, Ias, i
                                               e-mail address: stefan.ciobaca@info.uaic.ro


                                                     Abstract. We build a SAT solver implementing the DPLL algorithm in the verification-
                                                     enabled programming language Dafny. The resulting solver is fully verified (soundness,
                                                     completeness and termination are computer checked). We benchmark our Dafny solver and
                                                     we show that it is just as efficient as an equivalent DPLL solver implemented in C# and
                                                     roughly two times less efficient than an equivalent solver written in C++. We conclude
                                                     that auto-active verification is a promising approach to increasing trust in SAT solvers, as
                                                     it combines a good trade-off between execution speed and degree of trustworthiness of the
                                                     final product.




                                                                                       1. Introduction
                                         Modern high-performance SAT solvers quickly solve large satisfiability instances that occur
                                         in practice. If the instance is satisfiable, then the SAT solver can provide a witness in the
                                         form of a satisfying truth assignment, which can be checked independently.
                                              If the instance is unsatisfiable, the situation is less clear. Brummayer and others [BLB10]
                                         have shown using fuzz testing that in 2010 many state-of-the-art SAT solvers contained bugs,
                                         including soundness bugs. Since 2016, in order to mitigate this issue, the annual SAT com-
                                         petition requires solvers competing in the main track to output UNSAT certificates [BHJ17];
                                         these certificates are independently checked in order to ensure soundness.
                                              These certificates could be exponentially large and the SAT solver might not even be able
                                         to output them due to various resource constraints. The implementation of the SAT solver
                                         should then be trusted not to contain bugs. However, typical high-performance SAT solvers
                                         contain data structures and algorithms complex enough to allow for subtle programming
                                         errors.
                                              To handle these potential issues, we propose a verified SAT solver using the Dafny
                                         system [Lei13]. Dafny is a high-level imperative language with support for object oriented
                                         features. It features methods with preconditions, postconditions and invariants, which are
                                            Key words and phrases: DPLL, Dafny, formal verification, auto-active verification, satisfiability solving.
                                           ∗
                                            This is an extended version of a paper [AC19] presented at the Working Formal Methods Symposium
                                         2019.


                                         Preprint submitted to                                                          ©    Cezar-Constantin Andrici and S, tefan Ciobâcă
                                         Logical Methods in Computer Science                                            CC    Creative Commons
2                    CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




checked at compilation time by relying on the Z3 SMT solver [dMB08]. If a postcondition
cannot be established (either due to a timeout or due to the fact that it does not hold),
compilation fails. Therefore, we can place a high degree of trust in a program verified using
the Dafny system.
     A modern high-performance SAT solver implements a backtracking search for a satisfying
assignment. The search space is pruned by using several algorithmic tricks: (1) unit
propagation; (2) fast data structures (e.g., to identify unit clauses); (3) variable ordering
heuristics; (4) back-jumping; (5) conflict analysis; (6) clause learning; (7) restart strategy.
In addition, careful engineering of the implementation is required for high performance.
     The first three items are usually referred to as the DPLL algorithm [DP60, DLL62],
and all items together are the core of the state-of-the-art CDCL algorithm [MS99, BS97].
We have implemented and verified in Dafny the first three items, constituting the DPLL
algorithm, and we leave the other items for future work. We implement the MOMS variable
ordering heuristic [HV95]. We note that our Dafny solver is computer checked for soundness,
completeness and termination. We assume that the input is already in CNF form. The
parser, which reads a file in the well-known DIMACS format, is also written in Dafny and
hence verified against, e.g., out of bounds errors. However, there is no specification for the
parser.
     Our work is part of the larger trend towards producing more trustworthy software
artifacts, ranging among certified compilers [Ler09], system software [HP10, HHL+ 14, BFK16,
ZBPB17], or logic [BFLW18]. The main conceptual difference to previous work on verified
or certified SAT solvers is that we propose to check directly the imperative algorithm using
deductive verification, instead of, e.g., verifying functional code and relying on a refinement
mechanism to extract imperative code, which could hurt performance.
     Structure. In Section 2, we briefly go over the DPLL algorithm, as presented in the
literature. In Section 3, we present our verified implementation in Dafny of the algorithm.
We start by presenting the main data structures and their invariants (Section 3.1). We
continue with the operations supported by the data structures in Section 3.2. Finally, in
Section 3.3, we present the implementation of the core DPLL algorithm, together with the
verified guarantees that it provides. In Section 4, we benchmark the performance of our
solver. In Section 5, we discuss related work. We conclude in Section 6. We also discuss the
main challenge in verifying our implementation of DPLL, along with some methodological
tricks that we have used to make the verification effort tractable.
     Contributions. We present the first (to our knowledge) assertional proof of the DPLL
algorithm. The implementation is competitive in running time with an equivalent C++
solver.
     Comparison with the workshop version. This paper is a revised extended version of our
previous work [AC19] published in EPTCS. We feature an improved presentation, additional
explanations and a benchmark of the performance of our solver. In addition, the solver
improvements over the workshop version are:
(1) The new implementation features machine integers, which improve performance ap-
     proximately 10 times in our tests. Going to machine integers from unbounded integers
     requires proving upper bounds on indices throughout the code.
(2) The new implementation features mutable data structures for identifying unit clauses.
     Our previous approach used Dafny sequences (seq), which are immutable and cause
     a performance drawback because they are updated frequently. The new mutable data
        A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                       3




    structures make the solver significantly faster, but they are more difficult to reason
    about and verify.
(3) We implement and verify the MOMS variable ordering heuristic.
(4) We also improve the methodology of our verification approach and in particular we
    significantly reduce verification time. By carefully specifying invariants and separating
    concerns in the implementation, the verification time is now approximately 13 minutes
    for the entire project.
       In contrast, in our previous implementation, one method (setLiteral) took approxi-
    mately 10 minutes to verify on its own (the entire project used to take about 2 hours to
    verify in its entirety).
(5) We benchmark our Dafny implementation against similar DPLL implementations written
    in C# and C++ and we show it is competitive in terms of performance.


               2. The Davis-Putnam-Logemann-Loveland Algorithm
The DPLL procedure is an optimization of backtracking search. The main improvement
is called unit propagation. A unit clause has the property that its literals are all false in
the current assignment, except one, which has no value yet. If this literal would be set to
false, the clause would not be satisfied; therefore, the literal must necessarily be true for the
entire formula to be true. This process of identifying unit clauses and setting the unknown
literal to true is called unit propagation.
Example 2.1. We consider a formula with 7 variables and 5 clauses:
          (x1 ∨ x2 ∨ x3 )∧ (¬x1 ∨ ¬x2 )∧ (x2 ∨ ¬x3 )∧ (x2 ∨ x4 ∨ x5 )∧ (x5 ∨ x6 ∨ x7 )
The formula is satisfiable, as witnessed by the truth assignment (true, false, false, true, true,
false, true).
    Algorithm 2.2 describes the DPLL procedure [GKSS08] that we implement and verify,
presented slightly differently in order to match our implementation more closely:
Algorithm 2.2. Function DPLL-recursive(F , tau)
       input : A CNF formula F and an partial assignment tau
       output : SAT/UNSAT, depending on where there exists an assignment extending
             tau that satisfies F
       while ∃ unit clause ∈ F do
           ` ← the unset literal from the unit clause
       tau ← tau[` := true]
       if F contains the empty clause then return UNSAT ;
       if F has no clauses left then
           Output tau
        return SAT
       ` ← some unset literal
       if DPLL-recursive(F, tau[` := true]) = SAT then return SAT;
       return DPLL-recursive(F, tau[` := false])
     We describe how the algorithm works on this example: first, the algorithm chooses the
literal x1 and sets it to true (arbitrarily; if true would not work out, then the algorithm
would backtrack here and try false). At the next step, it finds that the second clause is
unit and sets ¬x2 to true, which makes the third clause unit, so ¬x3 is set to true. After
4                    CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




unit propagation, the next clause not yet satisfied is the fourth one, and the first unset
literal is x4 . At the branching step, x4 is assigned to true. Furthermore, only one clause is
not satisfied yet, and the next decision is to choose x5 and set it to true, which makes the
formula satisfied, even if x6 and x7 are not set yet.
     Next, we recall some well-known terminology in SAT solvers. Choosing and assigning
an unset literal to true or false is called a branching step or a decision. Every time the
algorithm makes a decision, the decision level is incremented by one and some more literals
are assigned to true or false by unit propagation.
     The trace of assignments is split into layers, one layer per decision. Multiple literals
can be set at the same decision level (the decision literal, and the literals assigned by
unit propagation). Every time the algorithm backtracks it must revert an entire layer
of assignments. A possible assignments trace corresponding to Example 2.1 is shown in
Figure 1.

              Example formula:            Example assignments trace:
              1) x1 ∨ x2 ∨ x3             (x1 , true), (x2 , f alse), (x3 , f alse)
              2) ¬x1 ∨ ¬x2                (x4 , true)
              3) x2 ∨ ¬x3                 (x5 , true)
              4) x2 ∨ x4 ∨ x5
              5) x5 ∨ x6 ∨ x7


Figure 1: Assignments trace representation for Example 2.1 divided into layers. The first
          layer corresponds to setting the decision variable x1 to true, followed by unit
          propagation, which sets x2 and x3 . This trace occurs just before the algorithm
          stops with an answer of SAT, after setting the decision variables x4 and x5 to true.



             3. A Verified Implementation of the DPLL Algorithm
In this section, we present the main ingredients of our verified solver. The full source code,
along with instruction on how to compile it and reproduce our benchmarks, can be found at
                 https://github.com/andricicezar/sat-solver-dafny-v2.

3.1. Data Structures. We first discuss the data structures for representing the formula,
for quickly identifying unit clauses and for recalling the current truth assignment.

3.1.1. Representing the CNF formula. The main class in our Dafny development is Formula,
which extends DataStructures (Figure 2). This class is instantiated with the number
of propositional variables (variablesCount) and with the clauses of the formula to be
checked for satisfiability. Propositional variables are represented by values between 0 and
variablesCount−1, positive literals are represented by values between 1 and variablesCount,
and negative integers between −1 and −variablesCount represent negative literals. Variables
and literals are represented by values of type Int32.t, which we define to model machine
integers and which is extracted to int.
        A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                       5




trait DataStructures {
    var variablesCount : Int32 . t ;
    var clauses : seq < seq < Int32 .t > >;
    var decisionLevel : Int32 . t ;
...
    var traceVariable : array < Int32 .t >;
    var traceValue : array < bool >;
    var traceDLStart : array < Int32 .t >;
    var traceDLEnd : array < Int32 .t >;
    ghost var assignmentsTrace : set <( Int32 .t , bool ) >;
...
    var truthAssignment : array < Int32 .t >;
    var trueLiteralsCount : array < Int32 .t >;
    var falseLiteralsCount : array < Int32 .t >;
    var positiveLiteralsToClauses : array < seq < Int32 .t > >;
    var negativeLiteralsToClauses : array < seq < Int32 .t > >;
}


Figure 2: The    most    important     fields             in     our    data   structures   (file
          solver/data structures.dfy).

     Clauses are sequences of literals and the entire formula is represented by a sequence
of clauses (var clauses : seq< seq<Int32.t> >). Using sequences for clause (sequences
are immutable in Dafny) has no significant performance impact, since they are set at the
beginning once and never changed.

3.1.2. Representing the current assignment and the assignments trace. The member variable
decisionLevel recalls the current decision level, which has an initial value of −1. The
assignments trace is represented at computation time by using the arrays traceVariable,
traceValue, traceDLStart and traceDLEnd and at verification time also by the ghost con-
struct assignmentsTrace (see Figure 2).
     The arrays traceVariable and traceValue have the same actual length. They recall,
in order, all variables that have been set so far, together with their value. The arrays
traceDLStart and traceDLEnd recall at what index in traceVariable and traceValue each
decision layer starts and ends, respectively.
     The ghost construct assignmentsTrace recalls the same information as a set of (variable,
value) pairs. This set is used for the convenience of specifying some of the methods and it
only lives at verification time; it is erased before running time and therefore it entails no
performance penalty.
     Note that traceVariable, traceValue, traceDLStart and traceDLEnd are arrays, and
they are extracted to C# as such. Therefore, lookups and updates in these arrays take
constant time. The link between the ghost construct assignmentsTrace and its impera-
tive counterparts (traceVariable, traceValue, traceDLStart and traceDLEnd) is computer
checked as the following class invariant:
 ( decisionLevel ≥ 0 =⇒ (
    (∀ i • 0 ≤ i < traceDLEnd [ decisionLevel ] =⇒
      ( traceVariable [ i ] , traceValue [ i ]) in assignmentsTrace )
    ∧
    (∀ x • x in assignmentsTrace =⇒ (
6                         CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




        ∃ i • 0 ≤ i < traceDLEnd [ decisionLevel ] ∧
          ( traceVariable [ i ] , traceValue [ i ]) = x ))))

     The array truthAssignment is indexed from 0 to variablesCount − 1 and it recalls the
current truth assignment. The value truthAssignment[v] is −1 if the propositional variable
v is unset, 0 if v is false, and 1 if v is true. At the beginning, it is initialized to −1 at all
indices. The following class invariant describing the expected link between the assignments
trace and the current truth assignment is computer checked:
    truthAssignment . Length = variablesCount ∧
    (∀ i • 0 ≤ i < variablesCount =⇒ -1 ≤ truthAssignment [ i ] ≤ 1) ∧
    (∀ i • 0 ≤ i < variablesCount ∧ truthAssignment [ i ] 6= -1 =⇒
      (i , truthAssignment [ i ]) in assignmentsTrace ) ∧
    (∀ i • 0 ≤ i < variablesCount ∧ truthAssignment [ i ] = -1 =⇒
      (i , false ) ∈
                   6 assignmentsTrace ∧ (i , true ) ∈
                                                    6 assignmentsTrace )

      Note that the invariant makes use of the ghost construct assignmentsTrace for brevity.

3.1.3. Quickly identifying unit clauses. The array trueLiteralsCount (falseLiteralsCount)
is used to recall how many literals in each clause are currently true (resp. false). They are
indexed from 0 to |clauses| − 1. The value trueLiteralsCount[i] denotes the number of
literals set to true in clauses[i] and falseLiteralsCount[i] the number of false literals in
clauses[i]. These are used to quickly identify which clauses are satisfied, which clauses are
unit or which clauses are false. For example, to check whether clauses[i] is satisfied, we
simply evaluate trueLiteralsCount[i] > 0. The following class invariant involving these
arrays is computer checked:
    | trueLiteralsCount | = | clauses | ∧
    ∀ i • 0 ≤ i < | clauses | =⇒
       0 ≤ trueLiteralsCount [ i ] = countTrueLiterals ( truthAssignment , clauses [ i ])

and analougously for falseLiteralsCount. Note that countTrueLiterals is a function (not
a method, hence it is used for specification only) that actually computes the number of true
literals by walking through all literals in the respective clause.
     In order to quickly update trueLiteralsCount and falseLiteralsCount when a new
literal is (un)set, we use positiveLiteralsToClauses and negativeLiteralsToClauses.
These are arrays indexed from 0 to variablesCount − 1. The first array contains the indices
of the clauses in which a given variable occurs. The second array contains the indices of
the clauses in which the negation of the given variable occurs. They provably satisfy the
following invariant:
    | positiveLiteralsToClauses | = variablesCount ∧ (
       ∀ variable • 0 ≤ variable < | positiveLiteralsToClauses | =⇒
         ghost var s := positiveLiteralsToClauses [ variable ];
         ...
         (∀ clauseIndex • clauseIndex in s =⇒ variable +1 in clauses [ clauseIndex ]) ∧
         (∀ clauseIndex • 0 ≤ clauseIndex < | clauses | ∧ clauseIndex ∈
                                                                      6 s =⇒
             variable +1 ∈
                         6 clauses [ clauseIndex ]))

(analogously for negativeLiteralsToClauses).
    To represent class invariants, Dafny encourages a methodology of defining a class
predicate valid. In our development, valid consists of the conjunction of the above
invariants, plus several other lower-level predicates that we omit for brevity. The predicate
        A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                        7




valid is used as a precondition and postcondition for all class methods, and therefore plays
the role of a class invariant. This way, it is guaranteed that the data structures are consistent.

3.2. Verified Operations over the Data Structures. From the initial (valid) state, we
allow one of these four actions:
(1) increase the decision level,
(2) set a variable,
(3) set a literal and perform unit propagation, and
(4) revert the assignments done on the last decision level.
     Each of the actions is implemented as a method and we show that these four methods
preserve the data structure invariants above.

3.2.1. The Method increaseDecisionLevel. This method increments the decision level by
one and creates a new layer. The method guarantees that the new state is valid, and nothing
else changes. Its signature and its specification are:
  method increaseDecisionLevel ()
    requires validVariablesCount ();
    requires validAssignmentTrace ();
    requires decisionLevel < variablesCount - 1;
    requires decisionLevel ≥ 0 =⇒
      traceDLStart [ decisionLevel ] < traceDLEnd [ decisionLevel ];

    modifies ‘ decisionLevel , traceDLStart , traceDLEnd ;

    ensures decisionLevel = old ( decisionLevel ) + 1;
    ensures validAssignmentTrace ();
    ensures traceDLStart [ decisionLevel ] = traceDLEnd [ decisionLevel ];
    ensures getDecisionLevel ( decisionLevel ) = {};
    ensures ∀ i • 0 ≤ i < decisionLevel =⇒
      old ( getDecisionLevel ( i )) = getDecisionLevel ( i );

    The predicates validVariablesCount and validAssignmentTrace are used as conjuncts
in the class invariant. The function getDecisionLevel returns all assignments at a given
decision level as a set.

3.2.2. The Method setVariable. This method takes a variable that is not yet set and it
updates is value. Because the trace of assignments and truthAssignment are changed,
trueLiteralsCount and falseLiteralsCount have to be updated. We use the arrays
positiveLiteralsToClauses and negativeLiteralsToClauses to efficiently update them,
and prove that the clauses that are not mentioned in these arrays are not impacted. The
signature of setVariable and its specification are:
  method setVariable ( variable : Int32 .t , value : bool )
    requires valid ();
    requires validVariable ( variable );
    requires truthAssignment [ variable ] = -1;
    requires 0 ≤ decisionLevel ;

    modifies truthAssignment , traceVariable , traceValue ,
             traceDLEnd , ‘ assignmentsTrace , trueLiteralsCount ,
             falseLiteralsCount ;
8                         CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




      ensures   valid ();
      ensures   traceDLStart [ decisionLevel ] < traceDLEnd [ decisionLevel ];
      ensures   traceVariable [ traceDLEnd [ decisionLevel ] -1] = variable ;
      ensures   traceValue [ traceDLEnd [ decisionLevel ] -1] = value ;

      // post conditions that ensure that only a position of the arrays
      // has been updated .
      ensures value = false =⇒ old ( truthAssignment [..])[ variable := 0]
        = truthAssignment [..];
      ensures value = true =⇒ old ( truthAssignment [..])[ variable := 1]
        = truthAssignment [..];
      ensures ∀ i • 0 ≤ i < variablesCount ∧ i 6= decisionLevel =⇒
        traceDLEnd [ i ] = old ( traceDLEnd [ i ]);
      ensures ∀ i • 0 ≤ i < variablesCount ∧ i 6= old ( traceDLEnd [ decisionLevel ]) =⇒
        traceVariable [ i ] = old ( traceVariable [ i ]) ∧ traceValue [ i ] = old ( traceValue [ i ]);
      ensures ∀ x • 0 ≤ x < old ( traceDLEnd [ decisionLevel ]) =⇒
        traceVariable [ x ] = old ( traceVariable [ x ]);

      ensures ∀ i • 0 ≤ i < decisionLevel =⇒
        old ( getDecisionLevel ( i )) = getDecisionLevel ( i );

      ensures assignmentsTrace = old ( assignmentsTrace ) + { ( variable , value ) };

      ensures countUnsetVariables ( truthAssignment [..]) + 1 =
        old ( countUnsetVariables ( truthAssignment [..]));



3.2.3. The Method setLiteral. This method uses setVariable as a primitive, so the pre-
conditions and postconditions are similar. The main difference is that after it makes the
first update, it also performs unit propagation, possibly recursively. This means that it calls
setLiteral again with new values. So, at the end of a call, truthAssignment might change
at several positions. To prove termination, we use as a variant the number of unset variables,
which provably decreases at every recursive step. Its signature and its specification are:
    method setLiteral ( literal : Int32 .t , value : bool )
      requires valid ();
      requires validLiteral ( literal );
      requires getLiteralValue ( truthAssignment [..] , literal ) = -1;
      requires 0 ≤ decisionLevel ;

      modifies truthAssignment , trueLiteralsCount ,
               falseLiteralsCount , traceDLEnd , traceValue ,
               traceVariable , ‘ assignmentsTrace ;

      ensures valid ();
      ensures traceDLStart [ decisionLevel ] < traceDLEnd [ decisionLevel ];
      ensures ∀ x • 0 ≤ x < old ( traceDLEnd [ decisionLevel ]) =⇒
        traceVariable [ x ] = old ( traceVariable [ x ]);
      ensures assignmentsTrace = old ( assignmentsTrace ) +
        getDecisionLevel ( decisionLevel );
      ensures ∀ i • 0 ≤ i < decisionLevel =⇒
        old ( getDecisionLevel ( i )) = getDecisionLevel ( i );
      ensures countUnsetVariables ( truthAssignment [..]) <
        old ( countUnsetVariables ( truthAssignment [..]));
       A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                     9




   ensures (
      ghost var ( variable , val ) := convertLVtoVI ( literal , value );
      isSatisfiableExtend ( old ( truthAssignment [..])[ variable as int := val ]) ⇐⇒
              isSatisfiableExtend ( truthAssignment [..])
   );

   decreases countUnsetVariables ( truthAssignment [..]) , 0;

     In the code above, the function getLiteralValue(tau, `) returns the value of the literal
` in the truth assignment tau. Note that the variable truthAssignment is an array, while
truthAssignment[..] converts the array to a sequence. The sequence (immutable) is used
to represent truth assignments at specification level.

3.2.4. The Method revertLastDecisionLevel. This method reverts the assignments from
in the last layer by changing the value of the respective literals to −1. The proof of this
method requires several helper proofs that confirm that the data structures are updated
correctly. To quickly update trueLiteralsCount and falseLiteralsCount, we again use
the two arrays positiveLiteralsToClauses and negativeLiteralsToClauses. As part of
postcondition, we prove that the literals not on the last decision level remain unchanged:
 method revertLastDecisionLevel ()
   requires valid ();
   requires 0 ≤ decisionLevel ;

   modifies ‘ assignmentsTrace , ‘ decisionLevel , truthAssignment , trueLiteralsCount ,
            falseLiteralsCount , traceDLEnd ;

   ensures decisionLevel = old ( decisionLevel ) - 1;
   ensures assignmentsTrace = old ( assignmentsTrace ) -
     old ( getDecisionLevel ( decisionLevel ));
   ensures valid ();
   ensures ∀ i • 0 ≤ i ≤ decisionLevel =⇒
     old ( getDecisionLevel ( i )) = getDecisionLevel ( i );
   ensures decisionLevel > -1 =⇒
     traceDLStart [ decisionLevel ] < traceDLEnd [ decisionLevel ];



3.3. Proof of Functional Correctness for the Main Algorithm. The entry point
called to solve the SAT instance is solve:
 method solve () returns ( result : SAT_UNSAT )
   requires formula . valid ();
   requires formula . decisionLevel > -1 =⇒
     formula . traceDLStart [ formula . decisionLevel ] <
       formula . traceDLEnd [ formula . decisionLevel ];

   modifies formula . truthAssignment , formula . traceVariable , formula . traceValue ,
            formula . traceDLStart , formula . traceDLEnd , formula ‘ decisionLevel ,
            formula ‘ assignmentsTrace , formula . trueLiteralsCount ,
            formula . falseLiteralsCount ;

   ensures formula . valid ();
   ensures old ( formula . decisionLevel ) = formula . decisionLevel ;
   ensures old ( formula . assignmentsTrace ) = formula . assignmentsTrace ;
   ensures ∀ i • 0 ≤ i ≤ formula . decisionLevel =⇒
10                         CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




         old ( formula . getDecisionLevel (i )) = formula . getDecisionLevel ( i );
       ensures formula . decisionLevel > -1 =⇒
         formula . traceDLStart [ formula . decisionLevel ] <
           formula . traceDLEnd [ formula . decisionLevel ];

       ensures result . SAT ? =⇒ formula . validValuesTruthAssignment ( result . tau );
       ensures formula . countUnsetVariables ( formula . truthAssignment [..]) =
         formula . countUnsetVariables ( old ( formula . truthAssignment [..]));

       ensures result . SAT ? =⇒
         formula . isSatisfiableExtend ( formula . truthAssignment [..]);
       ensures result . UNSAT ? =⇒
         ¬formula . isSatisfiableExtend ( formula . truthAssignment [..]);

       decreases formula . countUnsetVariables ( formula . truthAssignment [..]) , 1;

     It implements the DPLL-procedure given in Algorithm 2.2 using recursion. However, for
efficiency, the data structures are kept in the instance of a class instead of being passed as
arguments. The most important postconditions stating the functional correctness are: if it
returns SAT then the current truthAssignment can be extended to satisfy the formula, and
if returns UNSAT it means that no truth assignment extending the current truthAssignment
satisfies it. We use the predicate isSatisfiableExtend(tau, clauses), which tests whether
there exists a complete assignment that extends the partial truth assignment tau and that
satisfies the formula.
     We also show as a postcondition that solve ends in the same state as where it starts.
This means that we chose to undo the changes even if we find a solution. Otherwise, the
preconditions and postconditions for solve would need to change accordingly and become
more verbose and less elegant. For simplicity, we chose to revert to the initial state every
time.
     A flowchart that shows graphically the main flow of the solve method, together with
the most important statements that hold after each line, is presented in Figure 3.
     Once a literal is chosen, the updates to the data structures are delegated to the step
method. This removes some duplication in the code, but it also makes the verification take
less time. The preconditions and postconditions of step are the same as in solve, but taking
into account that step additionally takes as arguments a literal and a desired value for this
literal. The method step calls setLiteral to set the literal and perform unit propagation,
and then calls solve recursively:
     method step ( literal : Int32 .t , value : bool ) returns ( result : SAT_UNSAT )
       requires formula . valid ();
       requires formula . decisionLevel < formula . variablesCount - 1;
       requires formula . decisionLevel > -1 =⇒
         formula . traceDLStart [ formula . decisionLevel ] <
           formula . traceDLEnd [ formula . decisionLevel ];
       requires ¬formula . hasEmptyClause ();
       requires ¬formula . isEmpty ();
       requires formula . validLiteral ( literal );
       requires formula . getLiteralValue ( formula . truthAssignment [..] , literal ) = -1;

       modifies formula . truthAssignment , formula . traceVariable , formula . traceValue ,
                formula . traceDLStart , formula . traceDLEnd , formula ‘ decisionLevel ,
                formula ‘ assignmentsTrace , formula . trueLiteralsCount ,
                formula . falseLiteralsCount ;
        A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                              11




        solve()

     does the for-
    mula have an               Yes
    empty clause?                              ∃i • 0 ≤ i < |clauses| ∧ falseLiteralsCount[i] =
                                               |clause[i]| =⇒!isSatisfiableExtend(tau)
          No                 UNSAT
                                               1) ∀i • 0 ≤ i < |clauses| =⇒ falseLiteralsCount[i] <
                                               literalsCount[i];
  is formula empty?            Yes
                                               ∀i • 0 ≤ i < |clauses| =⇒ trueLiteralsCount[i] > 0
          No                  SAT
                                               2) (○
                                                   1 ∧∃i • 0 ≤ i < |clauses| =⇒ trueLiteralCount[i] =
                                               0) =⇒ ∃` • getLiteralValue(tau, `) = −1
 ` ← chooseLiteral()
                                               3) ○
                                                  2 ∧getLiteralValue(tau, `) = −1

   r ← step(`, true)                           calls solve recursively
                                               4) ○
                                                  3 ∧old(state) = state

      is r SAT?                Yes
                                               ○4 ∧isSatisfiableExtend(tau[` := true]) =⇒
                                               isSatisfiableExtend(tau)
          No                  SAT
                                               ○
                                               4 ∧¬isSatisfiableExtend(tau[` := true])

 return step(`, f alse)                        calls solve recursively


Figure 3: Flowchart of method solve. For simplicity, when the initial state is reached, we
          use the notation state = old(state).


   ensures formula . valid ();
   ensures old ( formula . decisionLevel ) = formula . decisionLevel ;
   ensures old ( formula . assignmentsTrace ) = formula . assignmentsTrace ;
   ensures ∀ i • 0 ≤ i ≤ formula . decisionLevel =⇒
     old ( formula . getDecisionLevel ( i )) = formula . getDecisionLevel ( i );
   ensures formula . decisionLevel > -1 =⇒
     formula . traceDLStart [ formula . decisionLevel ] <
       formula . traceDLEnd [ formula . decisionLevel ];

   ensures result . SAT ? =⇒ formula . validValuesTruthAssignment ( result . tau );
   ensures result . SAT ? =⇒ (
     var ( variable , val ) := formula . convertLVtoVI ( literal , value );
     formula . isSatisfiableExtend ( formula . truthAssignment [..][ variable := val ]));

   ensures result . UNSAT ? =⇒ (
     var ( variable , val ) := formula . convertLVtoVI ( literal , value );
     ¬formula . isSatisfiableExtend ( formula . truthAssignment [..][ variable := val ]));

   ensures formula . countUnsetVariables ( formula . truthAssignment [..]) =
     formula . countUnsetVariables ( old ( formula . truthAssignment [..]));
12                          CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




         decreases formula . countUnsetVariables ( formula . truthAssignment [..]) , 0;



                                             4. Benchmarks
Dafny code can be extracted to C#, and then compiled and executed as regular C# code.
In this section, we present the results obtained by benchmarking the C# code extracted
from our verified solver (we refer to this code as the Dafny solver) to see how it performs
against other solvers.
     Benchmark used. For benchmarking, we use some of the tests in SATLIB - Benchmark
Problems1. We select the sets uf100, uuf100 up to uf200, uuf200. These sets of SAT
problems all contain instances in 3-CNF, with uf denoting satisfiable instances and uuf
denoting unsatisfiable instances. The numbers in the names (e.g., 100, 200) denote the
number of propositional variables. The number of clauses in each set is chosen such that the
problems sit at the satisfiability threshold [CA96]. We choose these sets of SAT instances
because they are small enough for DPLL to solve in reasonable time, but big enough so that
the search dominates the execution time (and not, e.g., reading the input).
     Benchmarking methodology. We run the tests using the benchmarking framework
BenchExec [BLW19], a solution that reliably measures and limits resource usage of the
benchmarked tool2. We used BenchExec to limit resource usage to set the following for
each run: time limit to 5000s, memory limit to 1024 MB, CPU core limit to 1. We used
a Intel Core i7-9700K CPU @ 3.60GHz machine (cores: 4, threads: 8, frequency: 4900
MHz, Turbo Boost: enabled; RAM: 8290 MB, Operating System Linux-5.3.0-40-generic-
x86 64-with-Ubuntu-18.04-bionic, Dafny 2.3.0.10506, Mono JIT compiler 6.8.0.105, G++
7.5.0).
     Benchmark 1. We first check whether the extracted code has any added overhead
compared to a implementation written directly in C#. For this purpose, we write in C# a
solver implementing the same algorithm and data structures as the Dafny solver.
     We find that there is a negligible overhead coming from the method we use to read files
in Dafny, and not from the extraction process itself. In our results, the reading and parsing
of the input file in Dafny takes at least twice as long as in C#. On small inputs, the C#
solver therefore outperforms the Dafny solver. On larger inputs, the performance is the
same.
     Benchmark 2. The language C# is not popular in SAT solving, with C++ being
the language of choice because of performance. Therefore, we implement the same DPLL
algorithm directly in C++. We benchmark our verified Dafny solver against the C++
implementation. The results show that the (unverified) C++ solver is approximately twice
as fast on large tests as our verified Dafny solver.
     Benchmark 3. To put the performance of our verified Dafny solver into context, we also
benchmark against the solver MiniSat 3 (with the default settings). As MiniSat implements
the full CDCL algorithm, which can be exponentially faster than DPLL, it outperforms
our solver significantly. However, the correctness guarantee offered by our verified solver is
higher than the unverified C code of MiniSat.
     1
       https://www.cs.ubc.ca/∼hoos/SATLIB/benchm.html
     2
       https://github.com/sosy-lab/benchexec
     3
       http://minisat.se/
       A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                           13




    In Table 1, we summarize the running times of all solvers on the respective sets of tests.
We report the average running time, the standard deviation and the sum over all running
times for SAT instances in each particular set of tests.
                  Dafny SAT Solver      C# DPLL Solver C++ DPLL Solver MiniSat v2.2.0
                   avg    sd     sum     avg    sd     sum avg       sd    sum avg sd sum
          uf100 0.07 0.02       72.72 0.05 0.02       55.75 0.02 0.01 21.73 0.00 0.00 2.70
         uuf100 0.13 0.03 130.58 0.11 0.03 111.65 0.04 0.01 49.94 0.00 0.00 4.03
          uf150 1.29 1.30 129.24 1.22 1.26 122.22 0.63 0.66 63.54 0.00 0.00 0.84
         uuf150 3.48 1.56 348.44 3.34 1.51 334.52 1.76 0.79 176.18 0.01 0.00 1.87
          uf175 6.90 6.90 690.60 6.88 6.87 688.59 3.50 3.50 350.75 0.02 0.02 2.58
         uuf175 21.66 10.60 2166.94 21.80 10.67 2180.41 10.77 5.25 1077.03 0.05 0.02 5.13
          uf200 43.22 39.99 4322.50 47.07 43.69 4707.89 21.92 20.35 2192.21 0.06 0.05 6.48
         uuf200 110.64 48.33 10953.40 120.07 52.64 11887.17 55.98 22.55 5542.17 0.18 0.08 17.82

Table 1: The CPU time required to solve each set of instances by each SAT Solver in seconds.
         The first three solvers are implemented by us.

    Figures 4 and 5 present the running times (log scale) of all four solvers mentioned above
on all SAT instances in the uf200 and uuf200 sets, respectively. The running times are
sorted by the time it takes for the Dafny solver to finish.




Figure 4: CPU time on each instance in the set uf200 (all instances are satisfiable in this
          set). The Dafny solver and the C# solver are essentially indistinguishable. The
          C++ solver is approximately twice as fast. MiniSAT is much faster, since it
          implements the full CDCL algorithm.

     We conclude that our verified Dafny solver is competitive with an equivalent implemen-
tation in C++ (it is only two times slower), but the correctness guarantee offered by our
verified solver makes it significantly more trustworthy.

                                        5. Related Work
The SAT solver versat [OSOC12] was implemented and verified in the Guru programming
language using dependent types. As our solver, it also implements efficient data structures.
14                    CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




Figure 5: CPU time on each instance in the set uuf200 (all instances are unsatisfiable in
          this set). The Dafny solver and the C# solver are essentially indistinguishable.
          The C++ solver is approximately twice as fast. MiniSAT is much faster, since it
          implements the full CDCL algorithm.

However, it relies on a translation to C where data structures are implemented imperatively
by using reference counting and a statically enforced read/write discipline. Unlike our
approach, the solver is only verified to be sound: if it produces an UNSAT answer, then the
input formula truly is unsatisfiable. However, termination and completeness (if the solver
produces SAT, then the formula truly is satisfiable) are not verified. Another small difference
is the verification guarantee: versat is verified to output UNSAT only if a resolution proof of
the empty clause exists, while in our approach we use a semantic criterion: our solver always
terminates and produces UNSAT only if there is no satisfying model of the input formula.
Of course, in the case of propositional logic these criteria are equivalent and therefore this
difference is mostly a matter of implementation. Unlike our solver, some checks are not proved
statically and must be checked dynamically, so they could be a source of incompleteness. An
advantage of versat over our approach is that is implements more optimizations, like conflict
analysis and clause learning, which enable it to be more competitive in terms of running
time. Blanchette and others [BFLW18] present a certified SAT solving framework verified
in the Isabelle/HOL proof assistant. The proof effort is part of the Isabelle Formalization
of Logic project. The framework is based on refinement: at the highest level sit several
calculi like CDCL and DPLL, which are formally proved. Depending on the strategy, the
calculi are also shown to be terminating. The calculi are shown to be refined by a functional
program. Finally, at the lowest level is an imperative implementation in Standard ML,
which is shown to be a refinement of the functional implementation. Emphasis is also
placed on meta-theoretical consideration. The final solver can still two orders of magnitude
slower than a state-of-the-art C solver and therefore additional optimizations [Fle19] are
desirable. In contrast, in our own work we do not investigate any meta-theoretical properties
of the DPLL/CDCL frameworks; we simply concentrate on obtaining a verified SAT solver.
We investigate to what extent directly proving the imperative algorithm is possible in
an auto-active manner. A key challenge is that the verification of Dafny code may take
a lot of time in certain cases and we have to optimize our code for verification time as
       A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                        15




well. Another SAT solver verified in Isabelle/HOL, is by Marić [Mar09]. In contrast to
previous formalization, the verification methodology is not based on refinement. Instead,
the Hoare triples associated to the solver pseudo-code are verified in Isabelle/HOL. In
subsequent work [MJ11], Marić and Janičić prove in Isabelle the functional correctness of a
SAT solver represented as an abstract transition system. Another formalization of a SAT
solver (extended with linear arithmetic) is by Lescuyer [Les11], who verifies a DPLL-based
decision procedure for propositional logic in Coq and exposes it as a reflexive tactic. Finally,
a decision procedure based on DPLL is also verified by Shankar and Vaucher [SV11] in the
PVS system. For the proof, they rely on subtyping and dependent types. Berger et al. have
used the Minlog proof assistant to extract a certified SAT solver [BLFS15]. For these last
approaches, performance considerations seem to be secondary.

                           6. Conclusion and Further Work
We have developed a formally verified implementation of the DPLL algorithm in the Dafny
programming language. Our implementation is competitive in terms of execution time, but
it is also trustworthy: all specifications are computer checked by the Dafny system. Other
approaches to SAT solvers that rely on type checkers [BFLW18] are arguably even more
trustworthy, since they are verified by a software system satisfying the de Bruijn criterion.
However, we believe that our approach can strike a good balance between efficiency and
trustworthiness of the final product.
     Our implementation incorporates data structures to quickly identify unit clauses and
perform unit propagation. The formalization consists of around 3088 lines of Dafny code,
including the parser. The code was written by the first author in approximately one year
and a half of part time work. The author also learned Dafny during that time. The ratio
between lines of proof and lines of code is approximately 4/1. Table 2 contains a summary
of our verified solver in numbers.
 Lines of code    3088 (without whitespace)                    Preconditions             420
 Classes          4 (and 1 trait)                              Postconditions            181
 Methods          33                                           Invariants                173
                  approx. 13 minutes (entire project)          Variants                  44
 Verification
                  most expensive: SATSolver.solve              Predicates                37
 time
                       (approx. 175s)                          Functions                 20
                  more than 60s:                               Ghost variables           24
                       6 methods/lemmas                        Lemmas                    42
                  between 10s and 60s:                         Assertions                169
                       2 methods/lemmas
 Ratio specifica- 2488 lines of specification/proofs to        reads annotations         41
 tion/code        600 lines of code                            modifies annotations      26

                  Table 2: Various statistics for our verified DPLL solver.

     In addition to coming up with the right invariants, the main challenge in the development
of the verified solver is the large amount of time required by the Dafny system to discharge
the verification conditions. In order to minimize this verification time, we develop and use
the following development/verification methodology:
16                   CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




(1) Avoid nested loops in methods. Nested loops usually require duplicating invariants,
     which decreases elegance and increases verification time.
        An example of applying this tip is the revertLastDecisionLevel method (in the file
     solver/formula.dfy), whose purpose is to backtrack to the previous decision level. The
     code of the method is currently very simple: it calls removeLastVariable repeatedly in a
     while loop. However, because it is so simple, it is tempting to inline removeLastVariable
    – this would lead to a significant increase in verification time.
(2) In the same spirit, avoid multiple quantifications in specifications.
        We have found it useful, whenever having a specification of the form forall x ::
     forall y :: P(x, y), to try to extract the subformula forall y :: P(x, y) as a
     separate predicate of x. This helps in two distinct ways: it forces the programmer to
     name the subformula, thereby clearing their thought process and making their intention
     more clear, and it enables the Z3 pattern-based quantifier instantiation to perform
     better [Mos09].
(3) Use very small methods. We find that it is better to extract as a method even code that
     is only a few lines of code long. In a usual programming language, such methods would
     be inlined (by the programmer). In our development, it is not unusual for such methods
     (with very few lines of code) to require many more helper annotations (invariants, helper
     assertions, etc.) and take significant time to verify.
(4) Use minimal modifies clauses in methods and reads clauses in functions. In particular,
     we make extensive use of the less well-known backtick operator in Dafny.
(5) During development, use Dafny to verify only the lemma/method currently being worked
     on. Run Dafny on the entire project at the end. To force Dafny to check only one
     method, we use the -proc command line switch.
(6) Finally, we have found that using the rather nice Z3 axiom profiler [BMS19] to optimize
     verification time does not scale well to projects the size of our solver.
      Our project shows that it is possible to obtain a fully verified SAT solver written in
assertional style, solver that is competitive in terms of running time with similar solvers
written in non-verifiable languages. However, our experience with the verified implementation
of the solver is that it currently takes significant effort and expertise to achieve this. We
consider that three directions of action for the development of Dafny (and other similar
auto-active verification tools) would be beneficial in order to improve this situation:
(1) Improve verification time of individual methods/lemmas,
(2) Make failures of verification obligations to check more explainable, and
(3) Devise a method better than asserts to guide the verifier manually.
      As future work, we would like to verify an implementation of the full CDCL algorithm,
thereby obtaining a verified solver that is competitive against state-of-the-art SAT solvers.
In order to upgrade to a competitive CDCL solver, we need to modify the algorithm to
implement a back-jumping and clause learning strategy, but also implement the two watched
literals data structure [GKSS08], which becomes more important for performance when the
number of clauses grows.

                                   Acknowledgments
This work was supported by a grant of the Alexandru Ioan Cuza University of Iaşi, within
the Research Grants program UAIC Grant, code GI-UAIC-2018-07.
         A COMPUTER-CHECKED IMPLEMENTATION OF THE DPLL ALGORITHM IN DAFNY                                 17




                                              References
[AC19]    Cezar-Constantin Andrici and Ştefan Ciobâcă. Verifying the DPLL algorithm in Dafny. In Mircea
          Marin and Adrian Crăciun, editors, Proceedings Third Symposium on Working Formal Methods,
          Timişoara, Romania, 3-5 September 2019, volume 303 of Electronic Proceedings in Theoretical
          Computer Science, pages 3–15. Open Publishing Association, 2019.
[BFK16] Karthikeyan Bhargavan, Cédric Fournet, and Markulf Kohlweiss. miTLS: Verifying protocol
          implementations against real-world attacks. IEEE Secur. Priv., 14(6):18–25, 2016.
[BFLW18] Jasmin Christian Blanchette, Mathias Fleury, Peter Lammich, and Christoph Weidenbach. A
          verified SAT solver framework with learn, forget, restart, and incrementality. J. Autom. Reasoning,
          61(1-4):333–365, 2018.
[BHJ17] Tomás Balyo, Marijn J. H. Heule, and Matti Järvisalo. SAT competition 2016: Recent develop-
          ments. In Proceedings of the Thirty-First AAAI Conference on Artificial Intelligence, February
          4-9, 2017, San Francisco, California, USA., pages 5061–5063, 2017.
[BLB10] Robert Brummayer, Florian Lonsing, and Armin Biere. Automated testing and debugging of
          SAT and QBF solvers. In Theory and Applications of Satisfiability Testing - SAT 2010, 13th
          International Conference, SAT 2010, Edinburgh, UK, July 11-14, 2010. Proceedings, pages 44–57,
          2010.
[BLFS15] Ulrich Berger, Andrew Lawrence, Fredrik Nordvall Forsberg, and Monika Seisenberger. Extracting
          verified decision procedures: DPLL and resolution. Log. Methods Comput. Sci., 11(1), 2015.
[BLW19] Dirk Beyer, Stefan Löwe, and Philipp Wendler. Reliable benchmarking: requirements and solutions.
          STTT, 21(1):1–29, 2019.
[BMS19] Nils Becker, Peter Müller, and Alexander J. Summers. The axiom profiler: Understanding and
          debugging SMT quantifier instantiations. In Tomás Vojnar and Lijun Zhang, editors, Tools and
          Algorithms for the Construction and Analysis of Systems - 25th International Conference, TACAS
          2019, Held as Part of the European Joint Conferences on Theory and Practice of Software, ETAPS
          2019, Prague, Czech Republic, April 6-11, 2019, Proceedings, Part I, volume 11427 of Lecture
          Notes in Computer Science, pages 99–116. Springer, 2019.
[BS97]    Roberto J. Bayardo Jr. and Robert Schrag. Using CSP look-back techniques to solve real-world
          SAT instances. In Benjamin Kuipers and Bonnie L. Webber, editors, Proceedings of the Fourteenth
          National Conference on Artificial Intelligence and Ninth Innovative Applications of Artificial
          Intelligence Conference, AAAI 97, IAAI 97, July 27-31, 1997, Providence, Rhode Island, USA,
          pages 203–208. AAAI Press / The MIT Press, 1997.
[CA96]    James M. Crawford and Larry D. Auton. Experimental results on the crossover point in random
          3-SAT. Artif. Intell., 81(1-2):31–57, 1996.
[DLL62] Martin Davis, George Logemann, and Donald W. Loveland. A machine program for theorem-
          proving. Commun. ACM, 5(7):394–397, 1962.
[dMB08] Leonardo Mendonça de Moura and Nikolaj Bjørner. Z3: an efficient SMT solver. In C. R.
          Ramakrishnan and Jakob Rehof, editors, Tools and Algorithms for the Construction and Analysis
          of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint European
          Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-
          April 6, 2008. Proceedings, volume 4963 of Lecture Notes in Computer Science, pages 337–340.
          Springer, 2008.
[DP60]    Martin Davis and Hilary Putnam. A computing procedure for quantification theory. J. ACM,
          7(3):201–215, 1960.
[Fle19]   Mathias Fleury. Optimizing a verified SAT solver. In NASA Formal Methods - 11th International
          Symposium, NFM 2019, Houston, TX, USA, May 7-9, 2019, Proceedings, pages 148–165, 2019.
[GKSS08] Carla P. Gomes, Henry A. Kautz, Ashish Sabharwal, and Bart Selman. Satisfiability solvers. In
          Handbook of Knowledge Representation, pages 89–134. Elsevier, 2008.
[HHL+ 14] Chris Hawblitzel, Jon Howell, Jacob R. Lorch, Arjun Narayan, Bryan Parno, Danfeng Zhang,
          and Brian Zill. Ironclad apps: End-to-end security via automated full-system verification. In 11th
          USENIX Symposium on Operating Systems Design and Implementation, OSDI ’14, Broomfield,
          CO, USA, October 6-8, 2014., pages 165–181, 2014.
[HP10]    Chris Hawblitzel and Erez Petrank. Automated verification of practical garbage collectors. Log.
          Methods Comput. Sci., 6(3), 2010.
18                       CEZAR-CONSTANTIN ANDRICI AND S, TEFAN CIOBÂCĂ




[HV95]   John N. Hooker and V. Vinay. Branching rules for satisfiability. J. Autom. Reasoning, 15(3):359–
         383, 1995.
[Lei13]  K. Rustan M. Leino. Developing verified programs with Dafny. In 35th International Conference
         on Software Engineering, ICSE ’13, San Francisco, CA, USA, May 18-26, 2013, pages 1488–1490,
         2013.
[Ler09]  Xavier Leroy. A formally verified compiler back-end. J. Autom. Reasoning, 43(4):363–446, 2009.
[Les11]  Stephane Lescuyer. Formalizing and Implementing a Reflexive Tactic for Automated Deduction in
         Coq. Theses, Université Paris Sud - Paris XI, January 2011.
[Mar09]  Filip Marić. Formalization and implementation of modern SAT solvers. J. Autom. Reasoning,
         43(1):81–119, 2009.
[MJ11]   Filip Marić and Predrag Janičić. Formalization of abstract state transition systems for SAT. Log.
         Methods Comput. Sci., 7(3), 2011.
[Mos09]  Michal Moskal. Programming with triggers. In Proceedings of the 7th International Workshop on
         Satisfiability Modulo Theories, SMT ’09, page 2029, New York, NY, USA, 2009. Association for
         Computing Machinery.
[MS99]   João P. Marques Silva and Karem A. Sakallah. GRASP: A search algorithm for propositional
         satisfiability. IEEE Trans. Computers, 48(5):506–521, 1999.
[OSOC12] Duckki Oe, Aaron Stump, Corey Oliver, and Kevin Clancy. versat: A verified modern SAT solver.
         In Verification, Model Checking, and Abstract Interpretation - 13th International Conference,
         VMCAI 2012, Philadelphia, PA, USA, January 22-24, 2012. Proceedings, pages 363–378, 2012.
[SV11]   Natarajan Shankar and Marc Vaucher. The mechanical verification of a DPLL-based satisfiability
         solver. Electr. Notes Theor. Comput. Sci., 269:3–17, 2011.
[ZBPB17] Jean Karim Zinzindohoué, Karthikeyan Bhargavan, Jonathan Protzenko, and Benjamin Beur-
         douche. HACL*: A verified modern cryptographic library. In Bhavani M. Thuraisingham, David
         Evans, Tal Malkin, and Dongyan Xu, editors, Proceedings of the 2017 ACM SIGSAC Conference
         on Computer and Communications Security, CCS 2017, Dallas, TX, USA, October 30 - November
         03, 2017, pages 1789–1806. ACM, 2017.




                                              This work is licensed under the Creative Commons Attribution License. To view a copy of
                                              this license, visit https://creativecommons.org/licenses/by/4.0/ or send a letter to Creative
                                              Commons, 171 Second St, Suite 300, San Francisco, CA 94105, USA, or Eisenacher Strasse
                                              2, 10777 Berlin, Germany
