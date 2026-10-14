                                                       MintHint: Automated Synthesis of Repair Hints

                                                 Shalini Kaleeswaran Varun Tulsian Aditya Kanade                                                     Alessandro Orso
                                                                          Indian Institute of Science                                       Georgia Institute of Technology
                                                     {shalinik,varuntulsian,kanade}@csa.iisc.ernet.in                                            orso@cc.gatech.edu




                                        ABSTRACT                                                                   65   char esc(char ∗s, int ∗i) {
arXiv:1306.1286v2 [cs.SE] 16 Sep 2013




                                                                                                                   66      char result;
                                           Being able to automatically repair programs is at the same time         67      if (s[∗i] != ESCAPE)
                                        a very compelling vision and an extremely challenging task. In             68          result = s[∗i];
                                        this paper, we present MintHint, a novel technique for program re-         69      else
                                                                                                                   70          if (s[∗i] == ENDSTR) // Localization rank 3
                                        pair that is a departure from most of today’s approaches. Instead          71              result = ESCAPE;
                                        of trying to fully automate program repair, which is often an un-          72          else {
                                        achievable goal, MintHint performs statistical correlation analysis        73             ∗i = ∗i + 1; // Localization rank 4
                                                                                                                   74             if (s[∗i] == ’n’)
                                        to identify expressions that are likely to occur in the repaired code      75                 result = NEWLINE;
                                        and generates, using pattern-matching based synthesis, repair hints        76             else
                                        from these expressions. Intuitively, these hints suggest how to rec-       77                 if (s[∗i] == ’t’) // Localization rank 2
                                                                                                                   78                     result = TAB;
                                        tify a faulty statement and help developers find a complete, actual        79                 else
                                        repair. MintHint can address a variety of common faults, including         80                     result = s[∗i]; // Localization rank 1
                                        incorrect, spurious, and even missing expressions.                         81             }
                                           We also present an empirical evaluation of MintHint that con-           82      return result;
                                                                                                                   83   }
                                        sists of two main parts. The first part is a user study that shows that,
                                        when debugging, developers’ productivity can improve manyfold              Figure 1: Function esc from program replace (version 23),
                                        with the use of repair hints—compared to having only traditional           which contains a faulty statement at line 70. The ones shown
                                        fault localization information. The second part consists of applying       are the line numbers of function esc in the actual code.
                                        MintHint to several faults of a widely used Unix utility program to           To address these limitations of existing techniques, in this paper
                                        further assess the effectiveness of the approach. Our results show         we propose MintHint, a novel, semi-automated approach to pro-
                                        that MintHint performs well even in situations, seen frequently in         gram repair. MintHint is a departure from most of today’s program
                                        practice, where (1) the repair space searched does not contain the         repair techniques as it does not try to find a complete repair, which
                                        exact repair, and (2) the operational specification obtained from the      we have observed to be an unachievable goal in many, if not most,
                                        test cases for repair is incomplete or even imprecise—which can be         cases due to technical and practical reasons. Instead, MintHint
                                        challenging for approaches aiming at fully automated repair.               aims to generate repair hints that suggest how to rectify a faulty
                                                                                                                   statement and help developers find a complete, actual repair.
                                        1    Introduction                                                             As an example, consider function esc from a faulty version of
                                           Debugging is an expensive activity that can be responsible for          program replace [19], shown in Figure 1. Function esc takes as
                                        a significant part of the cost of software maintenance [39]. It is         input a string and an index into the string and checks whether the
                                        therefore not surprising that researchers and practitioners alike have     character at the index is a special character (such as a newline or a
                                        invested a great deal of effort in developing techniques that can im-      tab). If so, it returns a program-specific constant that represents the
                                        prove the efficiency and effectiveness of debugging (e.g., [3, 6, 7,       special character. The fault is at line 70, where the branch predicate
                                        11, 15, 25, 29, 31, 32, 34, 35, 42]). In particular, in recent years,      should be s[*i+1] == ENDSTR, but an incorrect array index, *i, is
                                        there has been a growing interest in automated program repair tech-        used instead. Given this faulty program and a set of test cases for
                                        niques (e.g., [6, 11, 29, 31, 32, 35]). Although these techniques          the program that trigger the fault (i.e., at least one test in the set
                                        have been shown to be effective, they suffer from one or more of           fails due to this fault), MintHint would produce the following hint:
                                        the following limitations. First, some techniques rely on the ex-
                                        istence of a specification for the program being debugged, which                  Replace s[*i] == ENDSTR by s[*i+1] == ENDSTR
                                        is rarely the case in practice. Second, techniques that do not rely        Developers would use this hint as guidance while modifying the
                                        on specifications tend to “overfit” the repair to the set of existing      original code to arrive at a repair. In this specific example, de-
                                        test cases, which is likely to affect the general validity of the re-      velopers would simply make the suggested change and obtain the
                                        pair. Third, because they are looking for a complete repair, most          repaired version. In the more general case, as we will show in Sec-
                                        existing techniques must perform a search over a repair space that         tion 4, hints are not necessarily complete repairs, but rather sugges-
                                        is large enough to include the (unknown) repair. For non-trivial re-       tions on how to generate such repairs.
                                        pairs, this can make the technique either ineffective (if the bound           In the common case in which more than one statement is sus-
                                        on the repair space used by the tool is too small) or too expensive        pected to be faulty, MintHint would algorithmically generate re-
                                        to be used in practice (if the bound used/required is too large).          pair hints for all of them. It would then rank the generated hints to
                                                                                                                   help developers prioritize their efforts.
   To generate hints, MintHint operates in four steps. The first                Nature of hint   Targeted fault
step identifies potentially faulty statements by leveraging an exist-           Insert           Missing expressions
ing fault localization technique that requires only a test suite (e.g.,         Replace          Incorrect operator, constant, variable, etc.
[1, 20, 25]). The subsequent steps are performed for each of the                Remove           Spurious expressions
identified statements. The second step derives a state transformer,             Retain           Eliminating false positives
that is, a function that (1) is defined for all program states that reach       Compound         One or more occurrences of above
the faulty statement in the given test suite and (2) produces the                     Table 1: Nature of hints and targeted faults.
right output state for each of them. This step leverages dynamic
symbolic execution techniques (e.g., [4]). The third step explores          in both the phases, in the experimental phase, with hints, they were
a repair space and tries to identify and rank, through a statistical        completed over 5 times faster.
correlation analysis [8, 27], expressions in the space that are likely         In addition to the user study, we also performed a case study us-
to occur in the repaired statement, using the state transformer de-         ing a commonly used Unix utility, namely, the stream editor sed.
rived in the second step. (To the best of our knowledge, this paper         We considered 6 faulty versions of sed. On one of them sym-
is the first one to apply this form of statistical reasoning to pro-        bolic execution timed out and hence it was not subjected to hint
grams.) Finally, the fourth step of the approach synthesizes repair         generation. On 3 of the remaining 5 faulty versions, MintHint
hints by pattern matching [41] the expressions computed in the pre-         provided hints that immediately lead to repair. In one additional
vious step with those in the faulty statement. Together these steps         case, the hints when applied to the program, resulted in a partial
result in a sophisticated technique that suitably combines symbolic,        repair in which all passing tests continued to pass but several fail-
statistical, and syntactic reasoning to help in program repair.             ing tests started passing. Further, MintHint was able to synthesize
                                                                            useful hints even in the many cases across the user study and the
   MintHint synthesizes five types of hints that suggest (1) inser-
                                                                            case study in which (1) the repair space considered did not con-
tion, (2) replacement, (3) removal, or (4) retention of expressions,
                                                                            tain the repaired version of the faulty expression, or (2) the state
and (5) combinations of these. As shown in Table 1, these hints are
                                                                            transformer contained imperfect data.
applicable to many types of common faults, ranging from incorrect
                                                                               In summary, the main contributions of this paper are:
or spurious expressions to missing expressions, to combinations of
                                                                                • The definition of a novel technique for program repair, called
these. Moreover, MintHint can handle faults in a variety of pro-
                                                                                   MintHint, that combines symbolic, statistical, and syntac-
gram constructs, such as assignments, conditionals, switch state-
                                                                                   tic reasoning and overcomes some of the main limitations of
ments, loop headers, return statements, and statements with ternary
                                                                                   existing techniques by focusing on generating repair hints,
expressions. The main restriction, for the technique presented in
                                                                                   rather than complete repairs.
this paper, is that the fault has to involve a single statement and, in
the case of an assignment, it must be on the right-hand side (RHS)              • An implementation of MintHint that can perform automated
expression. However, we believe that MintHint can be extended to                   synthesis of repair hints for C programs.
address other situations, e.g., where the left-hand side variable in            • A user study that evaluates the effect of repair hints on de-
an assignment is faulty or the fault spans multiple statements.                    velopers’ productivity. This is one of the few user studies
                                                                                   performed in the area of program repair and debugging in
   MintHint overcomes the main limitations of existing techniques
                                                                                   general.
that we listed earlier in the following ways. First, it does not rely
on a formal specification; it instead derives an operational specifi-           • A further evaluation of MintHint’s effectiveness on a case
cation (i.e., a state transformer) from the test cases available. Sec-             study involving several faulty versions of a Unix utility.
ond, approaches that aim at deriving complete repair, typically use
equality with the state transformer (or an analogous entity) as a           2    Overview
criterion for selecting a candidate repair (e.g., [29, 31]). The sta-
                                                                              Figure 2 provides a high-level view of MintHint. As the figure
tistical correlation used in MintHint is a more relaxed and robust
                                                                            shows, MintHint takes as input a faulty program and a test suite—
notion than equality and can thus be more effective in identifying
                                                                            where at least one test case triggers the fault in the program, and
which expressions are likely to be part of the repaired code; this al-
                                                                            thus fails—and produces a list of repair hints in four steps. We
lows MintHint to generate more general repairs and to be effective
                                                                            now describe these four steps using the example we discussed in
in the presence of incomplete or even imperfect (i.e., noisy) data.
                                                                            the Introduction, shown in Figure 1.
Third, since MintHint looks for building blocks of repair (rather
than the complete repair itself) and then combines them algorithmi-         Step 1: Fault localization. This is a preliminary step, whose
cally to generate compound hints, it can generate useful actionable         goal is to provide the hint generation algorithm with a list of possi-
hints even when exploring an incomplete repair space.                       bly faulty statements to be repaired. To compute this list, MintHint
   To evaluate MintHint, we developed a prototype tool that im-             can leverage any existing fault localization approach. In our current
plements our approach for C programs and performed a user study             implementation, we use the Ochiai approach as implemented in the
using programs from the Siemens benchmark [19]. Specifically, the           Zoltar tool [20], which uses the test suite and performs spectra-
study consisted of two phases: control and experimental. In both            based fault localization. For our example, the localization tool out-
phases, a user was provided a single repair task along with fault           puts a ranked list of suspicious statements: 80, 77, 70, 73, 502, and
localization information and a test suite. In the experimental phase,       so on. In its subsequent steps, MintHint runs the hint generation
in addition, repair hints generated by MintHint were supplied. The          algorithm on each statement in the fault localization list indepen-
tasks given to a user in the two phases were independent. In all 10         dently, up to a given threshold. In the following discussion, we use
users were involved in the study. Without repair hints, only 6 of           line 70 to illustrate the remaining steps of MintHint.
them completed their task within 2h. With repair hints, all users           Step 2: Derivation of state transformers. The next step
could complete their task within the same time limit. For example,          towards repair is to infer the specification of what would be the
the fault described in Figure 1 was part of the user study but with-        correct statement at line 70. To do so, in the absence of an actual
out hints the user could not repair it within 2h, whereas with hints        specification, MintHint uses the test suite provided for the pro-
another user repaired it easily. Moreover, for the tasks completed          gram to infer an operational specification for the statement in the
            Program              Test suite




                                                                         MintHint
                                                                    State                        Ranked                            Repair
                                 Program                        transformer                    expressions                          hints




                                              Derivation of                      Ranking of                  Synthesis of                       Developers
                    Fault
                 localization              state transformers                   expressions                  repair hints

                                                     Figure 2: High-level view of the MintHint approach.


   Input state       Output state      Values of expressions over input state                                Rank     Expression             Likelihood
    s        *i        branch0         s[*i] ==     s[*i] ==         s[*i+1] ==                                  1    s[*i+1] == ENDSTR        0.62
                                       s[*i+1]     ENDSTR            ENDSTR                                      2    s[*i+1] <= ENDSTR        0.62
                                                                                                                      ...
"@%&a"       0           false           false        false             false
                                                                                                                 7    s[*i+1] != ENDSTR        0.62
 "@n@"       0           false           false        false             false
                                                                                                                      ...
 "@n@"       2            true           false        false              true
                                                                                                                23    s[1] == ENDSTR           0.43
"%@@"        1           false           true         false             false
                                                                                                                      ...
  "V@"       1            true           false        false              true
                                                                                                               488    s[*i] == ENDSTR            0
Table 2: An example state transformer and values of some ex-                                                          ...
pressions over the input states.                                                              Table 3: A partial list of expressions ranked by the likelihood
                                                                                              of occurrence in the repaired RHS.
form of a state transformer. Informally, this state transformer is
a function that, given an input state (i.e., valuation to variables)
at the (potentially) faulty statement, produces an output state that                               Rank      Statement      Hint                          Score
would make every test in the test suite pass, including the failing                                 1           70          Replace s[*i] == ENDSTR       1
ones. For passing tests, state transformers can be easily computed                                                          with s[*i+1] == ENDSTR
by simply observing input and output states during the execution                                    2           70          Replace s[*i] == ENDSTR       1
                                                                                                                            with s[1] == ENDSTR
of the tests. For failing tests, as we discuss in detail in Section 3.1,                            3           70          Insert s[*i+1] <= ENDSTR      1
MintHint computes state transformers using dynamic symbolic ex-                                                             and Remove s[*i] == ENDSTR
ecution and constraint solving [4]. Let us illustrate this step using                               4          77           Retain the statement          1
the statement at line 70. Because the statement is a conditional                                    5          80           Retain the statement          1
statement, MintHint uses a fresh boolean variable, say branch0 , to                                 6          502          Retain the statement          1
represent the outcome of the branch predicate. That is, the state-                                  7          70           Insert s[*i+1] != ENDSTR      0.62
ment is transformed into an assignment branch0 = s[*i] == END-                                          Table 4: Repair hints synthesized by MintHint.
STR, in which the fault is on the RHS, and the branch predicate
becomes the variable branch0 . Table 2 shows some entries in the                              tions between the values of the candidate expressions and the ex-
state transformer of the statement: (1) the string array s and index                          pected value of branch0 at line 70. For some expressions from
expression *i in the input state and (2) the LHS variable branch0                             the repair space and the faulty RHS itself, Table 2 gives the values
in the output state. The values of all variables except branch0 re-                           over the input states. ENDSTR is the null character indicating end-
main unchanged between a pair of input/output states, and hence                               of-string. As can be seen, the values of s[*i+1] == ENDSTR are
are not shown again. The value of branch0 in the first row is ob-                             highly correlated with the expected values of branch0 but the same
tained from a passing test by concrete execution and the remaining                            is not true for the other expressions. Table 3 shows some expres-
are obtained from failing tests by symbolic execution. These are                              sions in the repair space ranked by decreasing value of likelihood.
the values that branch0 is expected to take in the repaired version,                          Step 4: Synthesis of repair hints. After producing a ranked
on the respective input states.                                                               list of expressions, MintHint analyzes this list to synthesize an ac-
                                                                                              tionable list of repair hints. MintHint generates two types of hints:
Step 3: Ranking of expressions. The goal of this step is to                                   simple and compound. A simple hint is a single program trans-
identify syntactic building blocks (i.e., expressions) for construct-                         formation, whereas a compound hint is a set of program transfor-
ing an RHS expression compliant with the computed state trans-                                mations. For our example, the hints synthesized by MintHint for
former. To do so, MintHint searches the solution space, called                                some of the statements identified by the fault localization tool are
the repair space, for expressions whose values over the input state                           given in Table 4. Note that MintHint may generate more than one
of the state transformer are statistically correlated with the corre-                         hint for the same statement (e.g., statement 70 in Table 4). We now
sponding output values produced by the state transformer. More                                explain how MintHint generates such hints.
precisely, MintHint interprets correlation coefficients, which rep-
resent the numerical measure of the strength of a statistical corre-                          For simple hints, MintHint iteratively selects expressions from the
lation [8, 27], as the likelihood of the expression to occur in the                           repair space of each statement individually such that (1) their likeli-
repaired RHS. For our example, MintHint would compute correla-                                hood values are above a threshold and (2) the statistical correlation
among themselves is low. That is, they form a set of expressions            Algorithm 1: Algorithm MintHint
such that any one expression in the set is likely to appear in the           Input: Program P , test suite T , the number of faulty stmts k, the
repaired RHS. In our example, MintHint would select s[*i+1] !=                      bound on the size of exps in the repair space m
ENDSTR and s[1] == ENDSTR. We discuss the algorithm for                      Output: Ranked list of repair hints for the faulty statements
selection of expressions in detail in Section 3.2.                         1 begin
                                                                           2   SF ← localize_faults(P, T, k) // Localize faults
   After selecting these expressions, MintHint pattern matches [41]
                                                                           3   Hints ← ∅ // Initialize the set of hints
each of the selected expressions with the faulty RHS. Based on the         4   foreach F ∈ SF do
edit distance between an expression and the subexpressions in the                // Derive the state transformer
faulty RHS, MintHint determines the nature of the hint to be gen-          5     Let F be of the form x := e
erated for the expression. If the edit distance is less than or equal      6     f ← st_trans(P, F, T )
to a threshold chosen heuristically (2 in our current formulation),        7     Let f be represented as an array [(σ1 , σ10 ), . . . , (σn , σn
                                                                                                                                               0 )]
                                                                                 // Enumerate expressions in repair space
MintHint suggests the replacement of the matching expression in
                                                                           8     S ← subexps(e)
the faulty RHS. Otherwise, if the edit distance is greater than the        9     V ← vars_in_scope(P, F ); E ← enum_exps(G, V, m)
threshold, it suggests an insertion. Expression s[1] == ENDSTR,                  // Generate the data
for example, is at edit distance 2 from the faulty RHS’s expression       10     D(x) ← [σ10 (x), . . . , σn
                                                                                                           0 (x)]

s[*i] == ENDSTR, so MintHint synthesizes a replace hint for the           11     foreach e0 ∈ S ∪ E do D(e0 ) ← [σ1 (e0 ), . . . , σn (e0 )]
RHS (position 2 in Table 4). The edit distance for s[*i+1] != END-               // Synthesize hints
                                                                          12     Hints ← Hints ∪ MintSimpleHints(F, D, S, E)
STR, conversely, is greater than 2, and MintHint synthesizes an
                                                                          13     Hints ← Hints ∪ MintCompoundHints(F, D, S, E)
insert hint for this expression (position 7 in Table 4).                  14   end
   If the edit distance of an expression selected through likelihood      15   return sort(Hints)
value is zero, that is, the expression already occurs as a subexpres-     16 end
sion in the faulty RHS, MintHint deems the RHS’s subexpression
as unlikely to be faulty and generates a retain hint for it. In our ex-   sets is singleton in this case. In general, however, the sets would
ample, this happens for lines 80, 77, and 502 (positions 5, 4, and        contain more than one expression (e.g., see task 10 in Section 4.1).
6, respectively). In all three cases, MintHint finds that the existing       After computing a set of expressions that may occur together in
RHS is the most likely expression to appear in the repaired version       a repair, MintHint synthesizes actual compound hint using the edit
and hence synthesizes the retain hints for the statements. In fact,       distance of each expression in the set with the faulty RHS. For the
there is no way to repair the fault through simple modifications of       first set in our example, {s[*i+1] == ENDSTR}, MintHint gen-
these statements. We can say that retain hints can help developers        erates the replace hint at position 1 in Table 4. For the second
localize a fault by eliminating some spurious statements (i.e., false     set, {s[*i+1] <= ENDSTR}, it generates the hint at position 3 in
positives) returned by the fault localization tool.                       Table 4, which has two constituent hints: an insert hint for the ex-
   MintHint ranks hints based on their score. Intuitively, the score      pression in the set together with a remove hint. MintHint adds the
indicates the confidence in the applicability of the hint and is de-      remove hint because, in this compound hint, there is no constituent
rived from the likelihood values of the expressions involved. In the      hint which suggests retention or replacement of the faulty RHS.
case of a replace hint, the score is the maximum of the likelihood           To compute the score for a compound hint, MintHint computes
of the expression being used for replacement and one minus the            the maximum of the scores of the constituent hints. After com-
likelihood of the expression being replaced. For the replace hint at      puting all hints and their scores, MintHint reports the hints to the
position 2 in Table 4, for instance, the score is max(0.43, 1 − 0),       developer, ordered by score (as in Table 4).
where 0 is the likelihood value of the faulty RHS which is being
replaced (see Table 3). For insert and retain hints, the score is the     After getting the hints produced by MintHint, developers can man-
likelihood of the expression being inserted or retained (e.g., 0.62       ually apply the hints by modifying the potential faulty statement
for the insert hint at position 7 in Table 4). For a remove hint, it is   according to the hints. For example, in the case of a replace hint,
one minus the likelihood of the expression being removed.                 developers will have to replace a subexpression with a suggested
                                                                          one. For a remove hint, developer will have to remove the subex-
Whereas simple hints can address faults that can be repaired through      pression in the hint. They will also have to suitably remove the
a single syntactic transformation, compound hints can help re-            operator(s) around the subexpression, or guess another expression
pair more complex faults—faults that require more than one pro-           to fill the hole, so as to obtain a well-formed resulting expression.
gram transformation to be repaired or more refined pattern match-         Similarly, for an insert hint, developers will have to combine the
ing. Further, if the repair space contains only building blocks of        subexpression in the hint with the existing expression and select an
the repaired RHS, but not the repaired RHS itself, then compound          appropriate operator and place for insertion.
hints—obtained by algorithmically combining the building blocks—
bring the repair hints closer to the actual repair.                       3     Algorithm
   MintHint synthesizes compound hints by first computing sets of            The MintHint algorithm is presented in Algorithm 1. As we
expressions such that (1) within each set, the likelihood values of       discussed in the previous section, the input to the algorithm is a
the expressions are above a threshold and (2) all expressions in the      program P and a test suite T such that the program fails on at
repair space which are likely to appear in the repaired RHS together      least one of the tests in T . MintHint also takes a threshold k on
are included in the same set. This computation uses a variant of          the number of faulty statements to be considered for repair and a
correlation coefficients, called partial correlation coefficients, and    bound m on the size of the expressions in the repair space.
a more refined pattern matching. We differ the detailed discussion           The first step of MintHint (line 2) is to use the test suite to per-
on this to Sections 3.1 and 3.2. In our example, MintHint would           form fault localization, as indicated by the function localize_faults.
compute two such sets: {s[*i+1] == ENDSTR} and {s[*i+1] <=                All statements in the fault localization list SF are then processed
ENDSTR}. The selection criterion used here successfully identi-           in a loop (starting at line 4). Function st_trans at line 6 computes
fies the required expression s[*i+1] == ENDSTR. Each of these             the state transformer for a faulty statement F . Sets S and E, com-
puted at lines 8 and 9, contain the subexpressions of the faulty RHS            concretely using the so computed value for x (instead of the orig-
and the extra expressions that should be considered when search-                inal value of the RHS e). The input/output states at F in this con-
ing for repairs. The function D maps expressions from the repair                crete execution give the mapping f for the failing test. MintHint
space and the LHS variable to their values according to the state               also handles the cases where the faulty statement is executed more
transformer (similar to the column values in Table 2). Two sep-                 than once in a passing or failing test.
arate algorithms, MintSimpleHints and MintCompoundHints are                        Symbolic execution may fail to obtain a value for x that results in
used for synthesizing simple and compound hints. Finally, the hints             the correct output. If all failing tests of F still fail during symbolic
across all statements are sorted by their scores (line 15).                     execution (i.e., the program fails irrespective of F ), it is possible
   In the following discussion, for simplicity, we consider statement           that F may not be the faulty statement. In such cases, MintHint
F to be of the form x := e. A conditional statement can be rewrit-              generates a “retain the statement” hint. MintHint also sets time-
ten in this form similar to the transformation of line 70 in Section 2.         out for symbolic execution and if the symbolic execution times out
MintHint can handle cases in which the potentially faulty state-                on every failing test within the timeout threshold then MintHint
ment is a loop header of the form for(init, cond, upd), where init              discards the statement and does not generate any hints.
initializes the loop counter(s), cond is the loop termination condi-               In its subsequent phases, MintHint treats the computed state
tion, and upd is the update of the loop counter(s). In these cases,             transformer f for each potentially faulty statement F as an opera-
the fault could be in any of these three components, so MintHint                tional specification for the repair, thus eliminating the need to have
spawns three different tasks—one each for init, cond, and upd.                  a formal specification.
MintHint treats an assignment with a ternary RHS expression as a                3.1.3     Ranking of Expressions
conditional statement in which the fault is in the branch predicate
                                                                                   Using the state transformer f as a specification for statement F ,
or in one of the assignments in the branches. MintHint can handle
                                                                                MintHint ranks expressions in the repair space of F according to
other constructs, such as switch or return, in analogous ways.
                                                                                their likelihood of occurring on the RHS of the repaired version of
   We now present the different steps of the algorithm (summarized
                                                                                F . The repair space to be searched over can be obtained in several
above) in detail by discussing how MintHint goes (1) from the pro-
                                                                                ways, such as by enumerating expressions over variables in scope
gram’s test suite to expressions that may help repair the fault and
                                                                                or mining expressions that occur elsewhere in the program (simi-
(2) from these expressions to actual repair hints.
                                                                                lar to what is done in [29]). Presently, MintHint uses the former
3.1     From Tests to Likelihood of Expressions                                 approach. More precisely, function vars_in_scope, in Algorithm 1,
   This first part of the MintHint algorithm is based on symbolic               computes the set V of variables in scope at F . Then, function
and statistical analysis and is performed in several phases. We                 enum_exps enumerates the expressions of size up to m (a user-
discuss each of these phases separately.                                        defined threshold) over V according to the grammar of expressions
3.1.1     Fault Localization                                                    in the programming language in which P is implemented. Let E
   Function localize_faults leverages an existing fault localization            be the set of these expressions.
technique to compute a set SF of potentially faulty statements. Any                MintHint also includes in the repair space the set of subexpres-
fault localization technique that requires only the program P and a             sions of e, the RHS expression, including e itself. It does so be-
test suite T can be used here (e.g., [1, 20, 25]). These techniques,            cause it evaluates whether they are likely to be faulty or not inde-
called spectra-based techniques, gather runtime data on the execu-              pendent of the fault localization results. This set, which we call S,
tion of passing and failing tests and use data clustering techniques            is computed by function subexps (line 8). The repair space is thus
to rank statements by their likelihood of being faulty.                         defined as E ∪ S.
   Given this ranked list, MintHint analyzes the top k statements in               We recall that a program state σ is a mapping from variables
the list, where k is a threshold set by the user that can be increased          to values. This mapping can be extended naturally to expressions.
progressively, if necessary. We recall that, analogously to other               In particular, if e ≡ e0 op e00 then σ(e) = JopK(σ(e0 ), σ(e00 )).
existing repair approaches (e.g., [29, 31]), MintHint currently as-             Let D(x) = [σ10 (x), . . . , σn0 (x)] be the values of the LHS variable
sumes that faults can be repaired by changing a single statement.               x over the output states defined by state transformer f (line 10).
Therefore, MintHint synthesizes repair hints for each statement F               Similarly, for an expression e0 in the repair space, let D(e0 ) =
in SF , the set of potentially faulty statements, independently.                [σ1 (e0 ), . . . , σn (e0 )] be the values of the expression e0 over the in-
                                                                                put states defined by f (line 11).
3.1.2     Derivation of State Transformers
                                                                                   Given the data D(x) and D(e0 ), MintHint’s goal is to find whether
   For each potentially faulty statement F , function st_trans de-
                                                                                x and e0 are related with each other, that is, whether a change of
rives a state transformer f that, when substituted to F , makes the
                                                                                value in one is accompanied by a change of value in the other. Be-
program produce the correct output for each test in T . f is a func-
                                                                                cause D(x) contains the expected (correct), rather than current (er-
tion from program states to program states, where a program state
                                                                                roneous), values of x for the failing tests, the faulty RHS and its
σ is a mapping from the variables in scope at the faulty statement to
                                                                                faulty subexpressions should not be highly related with x. There-
appropriately typed values. More formally, in Algorithm 1 f is an
                                                                                fore, the expressions that are highly related with x will be treated
array of pairs of input/output states: f = [(σ1 , σ10 ), . . . , (σn , σn0 )]
                                                                                as building blocks for the repair. Of course, just because the fault
(line 7). Notationally, an unprimed state is an input state (at F ),
                                                                                localization tool marks a statement as potentially faulty, it does not
and a primed state is the corresponding output state.
                                                                                mean that the statement is actually faulty. The statistical analysis
   Function f is defined for states that can be witnessed at F , given          performed by MintHint is discriminative enough so that, for a spu-
the inputs in T . Tests in T that do not execute F are ignored when             riously marked statement (i.e., a false positive), the existing RHS
computing state transformers. For each passing test traversing F ,              expression e itself may appear as highly related to x.
MintHint runs the program and collects the input/output states at
F . Conversely, for failing tests that traverse F , MintHint (1) makes          Statistical Correlation. In statistics, the problem of finding
the LHS variable x symbolic, (2) uses a symbolic execution algo-                whether two variables are related with each other is called sta-
rithm with constraint solving to obtain a value of x that makes the             tistical correlation. A correlation coefficient is a numerical mea-
program produce the correct output, and (3) reruns the program                  sure of the strength of the correlation between two statistical vari-
ables [8, 27]. In our context, a statistical variable is either the LHS       Algorithm 2: Algorithm MintSimpleHints
variable x or an expression e0 . The (absolute) value of a correla-            Input: The faulty statement F ≡ x := e, a mapping D from
tion coefficient ranges over [0, 1]. A correlation coefficient value                  expressions to data, the set S of subexpressions of the faulty
close to 0 indicates that the variables are statistically uncorrelated,               RHS, the set E of enumerated expressions
whereas values close to 1 indicate strong correlation.                         Output: A set of simple hints
                                                                             1 begin
   There are a number of correlation coefficients that are used for
                                                                             2   R ← S ∪ E; SH ← ∅; L ← ∅
identifying different types of correlations between variables (e.g.,
                                                                             3   while true do
linear or monotonic correlations). In its current form, MintHint                   // Select the most likely expression
uses the Spearman coefficient [8]. This coefficient can be applied           4     e0 ← argmaxe00 ∈R likelihood(e00 ); R ← R \ {e0 }
to any data domain for which there is a ranking function r that can                // Exit loop if likelihood below threshold
map the values in the data domain to a totally-ordered set. The co-          5     if likelihood(e0 ) ≤ δ then break
efficient is defined even if the data domains of the two variables are             // Ensure that e’ is not subsumed by L
different. MintHint presently computes coefficients over three data          6     if p_likelihood(e0 , L) ≥ β then
domains: Booleans, integers, and ASCII encoding of characters. In            7         L ← L ∪ {e0 }
                                                                                       // Synthesize a simple hint using e’
general, there can be multiple variables in the system. We may               8         (e00 , dist) ← MinEdit(e0 , S)
want to compute the strength of the correlation between a pair of            9         SH ← SH ∪ GenHint(e0 , e00 , dist)
variables by eliminating the effect of a subset {c1 , . . . , cm } of the   10     end
other variables. This set is called a controlling set. The Spearman         11   end
partial correlation coefficient is a variant of Spearman coefficient             // Remove-hints for unlikely expressions
between a pair of variables with respect to a controlling set.              12   foreach e0 ∈ S for which there is no retain/replace hint do
                                                                            13     SH ← SH ∪ {(Line(F ), Remove e0 , 1 − likelihood(e0 ))}
Example I. As an example of how correlation coefficients can be             14   end
applied for reasoning about program constructs, consider a dataset          15   return SH
generated by the assignment y := i + j ∗ k − 10 over integer vari-          16 end

ables i ∈ [1, 2], j ∈ [1, . . . , 5], and k ∈ [1, . . . , 25]. The Spear-
man coefficient between the values of the (non-linear) subexpres-           are computed wrt values of y from Example I. MintHint would
sion j ∗ k and the values of the variable y is 0.9997. Clearly, the         then use this information and apply pattern matching to generate a
high coefficient value conforms to the fact that the term j ∗ k is,         “Replace j/k by j ∗ k” hint. This technique is discussed next.
numerically, a dominant term on the RHS. Conversely, i has a very
small range and is not a dominant term on the RHS, so its coef-
                                                                            3.2      From Likelihood of Expressions to Hints
                                                                               In this second part, we discuss how MintHint utilizes the likeli-
ficient is only 0.0230. Nevertheless, i is still a contributing term
                                                                            hood values of expressions computed in the first part of the algo-
on the RHS. We can use partial correlation to assess the correlation
                                                                            rithm to synthesize hints. Intuitively, MintHint synthesizes hints
between y and i by eliminating the effect of j ∗ k. In this example,
                                                                            by performing syntactic pattern matching between the expressions
the value of the partial correlation between y and i, with j ∗ k as
                                                                            that are likely to occur in the repaired RHS and the subexpressions
the controlling set, is 0.9116.
                                                                            of the faulty RHS, using different patterns to address different types
Complexity. The complexity of computing the Spearman coeffi-                of possible faults. Formally, a repair hint h for a statement F is a
cient between datasets of size n is O(n log n). The complexity              triple (`, t, s) comprising the line number ` of statement F , a tex-
of computation of the Spearman partial coefficient is O(n3 ), for n         tual hint t, and the hint’s score s. The keywords in the textual hint,
larger than m where m is the size of the controlling set.                   shown in bold font, have their usual English meaning.
Likelihood and Ranking of Expressions. The MintHint al-                     3.2.1      Simple Hints
gorithm is based on the hypothesis that an expression e0 is likely              MintSimpleHints (see Algorithm 2) synthesizes a set SH of sim-
to occur on the RHS in the repaired version of F iff it is highly-          ple hints given a faulty statement F , a dataset D obtained from F ’s
correlated with x on the dataset obtained from the state transformer        state transformer, subexpressions S of the faulty RHS, and extra ex-
which gives the expected, correct values of x even for the failing          pressions E over which to search. The algorithm also makes use of
tests. Based on this hypothesis, MintHint computes two measures             two thresholds δ and β, used respectively, for selecting expressions
for expressions: likelihood and partial likelihood.                         by likelihood and for checking partial likelihood of a candidate ex-
   The likelihood of an expression e0 to occur in the repaired RHS,         pression given the already selected expressions.
denoted by likelihood(e0 ), is the absolute value of the Spearman               MintSimpleHints initializes the repair space R to S ∪ E, the
coefficient between e0 and x over the datasets D(e0 ) and D(x)              set of simple hints SH and the set of likely expression L to the
(obtained at lines 10 and 11). Given a set L of expressions, the            empty set (line 2). It then executes the loop starting at line 3 until
partial likelihood of e0 to occur in the repaired RHS along with the        the likelihood of expressions drops below the threshold δ (line 5).
expressions in L, denoted by p_likelihood(e0 , L), is the absolute          Within this loop, an expression e0 ∈ R with the highest likelihood
value of the Spearman partial correlation coefficient of D(e0 ) and         is selected and removed from R (line 4). If the partial likelihood of
D(x) with {D(e00 ) | e00 ∈ L} as the data of the controlling set L.         e0 with L as the controlling set is above the threshold β (line 6) then
                                                                            it is added to L. This check ensures that e0 has sufficient statistical
Example II. Consider a faulty version y := i + j/k − 10 of the              correlation with x (the LHS) after taking out the effect of L, that is,
statement from Example I, where an incorrect operator / is used in          e0 is not subsumed by L. In the example in Section 2, once s[*i+1]
place of ∗. Through symbolic execution, MintHint would compute              != ENDSTR is added to L, all expressions until s[1] == ENDSTR
the expected values of y which would be close, if not identical, to         (ranked 23) have partial correlation below the threshold β = 0.1.
the values that y would take in the repaired program. With this                 Now, MintSimpleHints generates a simple hint for e0 . To do
data, the expression j ∗ k would get likelihood value of 0.9997. On         so, it first invokes function MinEdit, which identifies the expres-
the other hand, the faulty subexpression j/k would get a likelihood         sion e00 from S with minimal edit distance [41] from e0 (line 8).
value of 0.2109. For the sake of this example, these coefficients           Let dist be the minimal edit distance. Then, the algorithm invokes
function GenHint, which synthesizes a simple hint based on the                              Program          LOC     #Tasks
                                                                                            print_tokens2    570       2
value of dist (line 9). If dist is below a given threshold, it gen-
                                                                                            replace          564       4
erates hint “Replace e00 by e0 ”. Conversely, if dist is above such                         tcas             173       4
threshold, it generates hint “Insert e0 ”. For the former, the score
of the hint is set to the maximum between the likelihood of e0 and                          Table 5: Description of tasks.
the unlikelihood of e00 (i.e., 1 − likelihood(e00 )). For the latter,     each other and hence are permitted to conflict.) Finally, analogous
the score is simply the likelihood of e0 . In the current formulation,    to the loop at line 12 in Algorithm 2, MintCompoundHints gen-
MintHint uses threshold of 2 over the edit distance. This seems           erates remove hints for the subexpressions of the faulty RHS for
to capture errors resulting from incorrect operator, constant, vari-      whom there is no retain or replace hint synthesized earlier.
able, array index, and so on. Increasing the threshold may generate          There could be multiple simple hints that suggest retention of
spurious replace hints and reducing it would produce two separate         different subexpressions of the RHS. In these cases, these hints are
hints, respectively insert and remove, for e0 and e00 .                   clustered into one single compound hint. The score of a compound
   If dist = 0 (i.e., e0 already belongs to S), the algorithm gen-        hint is the maximum of the scores of the constituent hints.
erates hint “Retain e0 ” and assigns to the hint a score equal to
likelihood(e0 ). A special case of this is when e0 is exactly the same    4     Evaluation
as the RHS expression for which the algorithm generates a “retain            To assess the effectiveness of our approach, we implemented
the statement” hint. Finally, for the expressions that appear in the      MintHint to synthesize repair hints for C programs and performed
faulty RHS but not in set L, it generates remove hints in the loop at     an empirical evaluation. Our implementation uses Zoltar [20] for
line 12, where function Line returns the line number of a statement.      fault localization, KLEE [4] for dynamic symbolic execution with
The score of a “Remove e0 ” hint is 1 − likelihood(e0 ).                  constraint solving, and Matlab1 for statistical analysis.
3.2.2    Compound Hints                                                      Our evaluation consists of two parts. We performed a user study
   Function MintCompoundHints, called in Algorithm 1 at line 13,          to evaluate whether MintHint improves developers’ productivity.
computes compound hints using the same inputs as MintSimpleHints.         The user study is augmented with the application of hints on a case
Due to space constraints, we do not typeset MintCompoundHints             study. We investigate the following research questions:
and simply explain the key similarities and differences between              RQ1: Usefulness of hints — Can MintHint produce useful hints,
MintCompoundHints and Algorithm 2. Similar to Algorithm 2,                enabling developers to repair programs more effectively?
it iteratively computes the set of likely expressions. However, it           RQ2: Robustness — How does MintHint perform when the re-
uses p_likelihood(e00 , L) in place of likelihood(e00 ) at line 4 and     pair space is incomplete (i.e., does not contain the repaired version
the branch predicate at line 6 is replaced with true. The value           of the faulty expression) and is supplied imprecise data?
of partial likelihood gives the measure of the likelihood of e00 to          RQ3: Performance and scalability — How does MintHint scale
appear in the repaired RHS along with the expressions in L. As            to large programs, state transformers, and repair spaces?
a consequence, the expressions that get added to the set L are all        4.1     User Study
those expressions which can occur together in the repaired RHS. In
contrast, the expression selected at line 4 in Algorithm 2 is selected
                                                                          Experimental Setup. We performed fault localization on the
                                                                          programs from the Siemens suite [19]. The Siemens suite consists
only based on its individual likelihood.
                                                                          of a few programs with multiple faulty versions for each of them.
   In general, MintCompoundHints can generate more than one
                                                                          Table 5 lists the programs and the number of faulty versions that
set of likely expressions. More specifically, if multiple expres-
                                                                          were selected as tasks. In all, 10 tasks were selected. In the user
sions have the highest partial correlation coefficient (at line 4) in
                                                                          study, each user was required to work on two independent tasks. To
the first iteration of the loop, then the algorithm would partition
                                                                          keep each task manageable within 2h, for each task, only the top 5
them into three sets based on their edit distance from the faulty
                                                                          statements identified by Zoltar as potentially faulty were presented
RHS and its subexpressions: (1) equal to zero, (2) less than equal to
                                                                          to the users. For each of the chosen tasks, the actual faulty state-
2, and (3) more than 2. It initializes three sets of likely expressions
                                                                          ment belonged to this list. The tasks represent a diverse collection
by selecting one expression from each of the partitions above (if
                                                                          of faults (see Table 6). For each program and candidate faulty state-
not empty). It then proceeds independently to select other expres-
                                                                          ment, the state transformers were obtained for failing tests through
sions to add to each of them. (Conversely, when generating simple
                                                                          symbolic execution with the timeout of 5m per test. In one of the
hints, for multiple expressions with the highest correlation coeffi-
                                                                          tasks, symbolic execution of many failing tests timed out. Conse-
cient, MintSimpleHints selects one expression at random without
                                                                          quently, the data from the passing tests was seen to bias the results.
partitioning them by edit distance.) For example, in Section 2, the
                                                                          Therefore, for that task, only half of the passing tests were used.
expression s[*i+1] == ENDSTR is the only expression, among the
                                                                             Of the 10 users who participated in our study, 8 were working
seven expressions with the highest likelihood, which is at edit dis-
                                                                          professionals and 2 were graduate students (with prior industry ex-
tance less than equal to 2.
                                                                          perience) – none affiliated with our research group. Of these, 8
   For each expression in the set L, MintCompoundHints gener-             stated that they had moderate to high expertise with C program-
ates a hint with the pattern matching logic used at line 9 in Algo-       ming/debugging with everyone having at least 1 year of experience
rithm 2. We call each of these hints, a constituent hint, of the com-     in C programming. For each task, the input/output specifications
pound hint. We say that a pair of constituent hints of a compound         of methods, and meaning of variables and named constants were
hint conflict if they refer to either the same or overlapping subex-      presented as comments in the source code. In addition, each user
pressions of the faulty RHS. Two subexpressions of the faulty RHS         was provided a test suite of 10 passing tests and was given 15m to
overlap if their subtrees in the AST of the faulty RHS have some          study the program before starting with program repair.
common node(s). Overlapping subexpressions can be identified by              There were two phases of the user study. In the control phase, the
a simple walk over the AST. In order to ensure that no conflicting        users were given the fault localization information and test suite.
hints are generated, MintHint removes a subexpression and all ex-         In the experimental phase, in addition, they were given the repair
pressions that overlap with it from the repair space as soon as the
                                                                          1
subexpression is added to set L. (Simple hints are independent of             http://www.mathworks.com/products/matlab/
   Task    Program-Version       Nature of fault          Type of the most useful hint    Rank of the most    #Total hints     #Stmts with only
                                                                                            useful hint                      “Retain the stmt” hints
    1      print_tokens2-v6      Incorrect array index    Remove                                 10               31                   –
    2      replace-v7            Superfluous expression   Compound (Remove + others)             4                13                   1
    3      print_tokens2-v7      Superfluous expression   Compound (Remove + others)             4                8                    –
    4      replace-v18           Missing expression       Compound (Insert + others)             1                3                    1
    5      replace-v23           Incorrect array index    Replace                                1                6                    3
    6      tcas-v28              Incorrect operator       Replace                                6                26                   –
    7      replace-v8            Missing expression       Compound (Retain + others)             1                6                    2
    8      tcas-v2               Incorrect constant       Replace                                7                13                   1
    9      tcas-v1               Incorrect operator       Replace                                2                11                   3
    10     tcas-v12              Incorrect operator       Compound (Retain + others)             11               14                   –
Table 6: Description of faults in the user study and of useful hints identified by the users: The tasks that could not be finished in the
control phase (without hints) are underlined. All the tasks were completed in the experimental phase (with hints).

                                   Control phase   Experimental phase           hints for all statements presented to the user for that task. Note
                                  (without hints)       (with hints)
                                                                                that MintHint may produce multiple hints for a faulty statement.
                           Quantitative Analysis
Successful localization         8/10              10/10         (+2 )           The most useful hints were all in top 10 except for one case. The
Successful repair               6/10              10/10         (+4 )           last column in Table 6 gives the number of statements for which
Avg. time to repair             91m + 4 timeouts 29m (no timeouts)              only a “retain the statement” hint was generated. These are the
Avg. speedup (excl. timeouts) NA                  5.8x                          statements that are classified by MintHint as unlikely to be faulty.
           Qualitative Analysis (Ratings given by the users)                    Across the 10 tasks and 50 statements in the fault localization lists,
                                Easy: 2           Easy: 6       (+4 )           40 statements are likely to be false positives (10 are true positive,
Difficulty of localization      Moderate: 6       Moderate: 3
                                                                                i.e., definitely faulty). Out of these, 11 statements (more than 25%)
                                Difficult: 2      Difficult: 1
                                Easy: 3           Easy: 7       (+4 )           are eliminated by MintHint. This contributes greatly to ease of
Difficulty of repair            Moderate: 5       Moderate: 1                   localization. We believe that there is no obvious way to rectify
                                Difficult: 2      Difficult: 2                  these statements. In fact, no user in the study (even in the control
                 Table 7: Results of the user study.                            phase) came up with a repair for any of these statements.
                                                                                   For 6 tasks (tasks 2–6 and 9), the most useful hint had the precise
                                                    Yes             No          information required to repair the fault. For task 10, the faulty RHS
  Incompleteness of repair space                    5               5           was of the form exp1 || exp2 and the compound hint suggested
  Noise in state transformers obtained from tests   7 (max. 27%)    3           that both exp1 and exp2 be retained but did not say the same for
Table 8: Count of tasks in the user study wrt incompleteness of                 the entire RHS. The user therefore suspected that the operator was
the repair space and noise in state transformers.                               incorrect and correctly replaced it with &&. For task 1, the hint
                                                                                suggested only removal of the incorrect expression. The user had
hints. Each user worked on a single task in a phase and was given               to come up with the substitute expression. In task 7, the hint did
2h to complete the task. A task was considered to be complete if the            not suggest the expression to be inserted. The user mentioned that
repaired program passed all the tests. The users chose the programs             the hints helped mainly in localizing the fault. This is possible
for the control phase by drawing lots. We had mapped each task in               because MintHint eliminates 2 other statements in this case (see
the control phase to a task in the experimental phase with the objec-           the last column for task 7 in Table 6). In the case of task 8, the
tive of avoiding a user working on the same task or another version             replace hint did not suggest the required (named) constant to be
of the same program in both phases. A presentation was made to                  used. Nevertheless, the user observed that after substituting the new
them to explain the meaning of different types of repair hints. The             expression suggested in the hint, many failing tests started passing
users were provided Linux based machines with a debugger, text                  and subsequently inferred the right constant manually. Of these,
editors and IDEs, and the standard command line utilities.                      tasks 5, 8, 9, and 10 were not completed in the control phase.
(RQ1) Usefulness of hints. Table 7 summarizes the results of                       The number of total hints per task given in Table 6 depends on
the user study. In the control phase (without hints), out of 10 tasks,          the following factors: (1) The thresholds on correlation coefficients
the users could localize the faults to the actual faulty statement in           which determine how many expressions end up in the set of likely
8 cases but only managed to repair the programs in 6 cases. On                  expressions, thereby, also affect the number of hints. Across all
the contrary, in the experimental phase (with hints), the users could           tasks, the thresholds on correlation coefficient and partial correla-
perform localization and repair in all the 10 cases. Further, the aver-         tion coefficient for generation of simple hints were 0.4 and 0.1 re-
age time taken to repair a fault was 91m in the control phase (excl.            spectively. For compound hints, it was 0.6. (2) If the symbolic exe-
the 4 timeouts), whereas it was 29m in the experimental phase. The              cution times out on all failing tests for a statement then the hint gen-
average speedup obtained with the use of hints, for the 6 tasks that            eration algorithm is not run for that statement (see Section 3.1.2).
were completed in both the phases, was equal to 5.8x. The users                    Though the study is not large enough to measure the difference
were asked to rate the difficulty level of fault localization and repair        with statistical significance, the results suggest that repair hints can
for their tasks as easy, moderate, or difficult. The ratings, for the           contribute significantly in improving developers’ productivity and
same set of tasks, differ across the two phases. Notably, with the              even the feasibility of repair (within limited time).
hints, 4 more tasks were rated by the users as easy. These qualita-
tive ratings corroborate the quantitative results presented above.              (RQ2) Robustness. In practice, it is difficult to estimate the
   The users uniformly mentioned that the hints were useful and                 syntactic space to search for a complete repair. In our experiments,
were asked to indicate the hint that was most useful to them. The               for each statement, apart from the subexpressions of the potentially
ranks of the most useful hints in Table 6 are over the entire list of           faulty expression, expressions of size up to 4 (over the variables in
                                       #Exprs in repair space              Task Version-                      Type of      Rank of #Total #Stmts with
                                   (#Columns of the data matrix)                Fault    Nature of fault      useful        useful hints “Retain stmt”
       Size of state               Upto 5k Upto 10k > 10k                                                     hint           hint          hint only
       transformer     Upto 1k      < 1m        < 1m       < 1m
      (#Rows of the    Upto 10k     < 1m        < 5m       < 5m             1   v2-f1    Incorrect operator Replace        1      11        10
      data matrix)      > 10k       < 1m        < 5m       ≈ 1h             2   v3-f4    Incorrect constant –               –     11         3
                                                                            3   v3-f6    Incorrect constant Replace        1      10         9
Table 9: Performance and scalability chart: Tasks from the                  4   v5-f1    Incorrect operator Replace       13      13        12
user study belong to all cells except cell at position (3, 2). Tasks        5   v6-f1    Incorrect operators Compound      2       4         –
from the case study (Section 4.2) belong to the shaded cells.               6   v6-f2          Symbolic execution times out with 15m threshold

scope at the statement) were added to the repair space. The size             Table 10: Description of faults and hints in the case study.
of an expression is the number of nodes in its abstract syntax tree
(AST). For expressions involving arrays, an occurrence of an array                                                              Yes              No
with the index expression is counted as size 1 and the index ex-             Incompleteness of repair space                     1                4
pressions themselves can go up to size 4. We call a repair space             Noise in state transformers obtained from tests    4 (max. 97%)     1
complete only if the repaired version of the expression belongs to         Table 11: Count of tasks in the case study wrt incompleteness
it. For example, in task 10, the repaired expression exp1 && exp2          of the repair space and noise in state transformers.
was not in the repair space.
    MintHint derives state transformers for failing tests by symbolic      the SIR repository [12]. sed is a reasonably large program with
execution. In some cases, the derived constraints may have mul-            over 14K LOC and 250 functions. The SIR repository consists of
tiple satisfying assignments but not all of them can be observed           several versions of sed seeded with different faults. We performed
in the execution of the repaired version of the program. The con-          fault localization on them using Zoltar. Table 10 lists the versions
straint solver may pick any one of them. For passing tests, the state      and fault-IDs of the programs that were selected as tasks. In all,
transformer is obtained by concrete execution. Even though the test        6 tasks were selected. The top 15 statements identified by Zoltar
passes, the value generated by the faulty expression may not be ob-        as potentially faulty were considered for repair. For each of the
served in the repaired version. These situations make the resulting        chosen tasks, the actual faulty statement belonged to this list. For
data, which is used as a specification, imperfect (noisy) and may in       each version and candidate faulty statement, the state transform-
general invalidate the applicability of a repair.                          ers were obtained for failing tests through symbolic execution with
    Table 8 gives the count of tasks which had noise in the state trans-   the timeout of 5m per test for the first three tasks and 15m for the
formers and where the repair space was incomplete. This informa-           remaining. In the sixth task, symbolic execution timed out for all
tion is provided only for the actual faulty statement. To estimate         failing tests and hence it was not subjected to further analysis.
the amount of noise in the data, we first obtain the noise-free state      (RQ1) Usefulness of hints. For each of the tasks, Table 10
transformer of the (known) repaired version independently by con-          shows the nature of the fault and the type of the most useful hint.
crete execution over the test suite. An entry in the state transformer     For tasks 1, 3, and 4, a replace hint synthesized by MintHint when
obtained over the faulty version is classified as noisy if it does not     applied, immediately lead to success on both passing and failing
belong to the noise-free state transformer. There were 7 tasks with        tests. Task 5 consists of two faults in the same statement. A com-
noisy data with the maximum of 27% noise in one of them and                pound hint suggested removal of two subexpressions and retention
there were 5 tasks where the actual repaired expression did not be-        of the non-faulty subexpression. We removed the subexpressions
long to the repair space. Nevertheless, the successful completion of       identified by MintHint for removal and obtained well-formed ex-
the tasks in the user study indicates that useful hints could be syn-      pressions by removing operators around them. This change how-
thesized even in these challenging cases. The key reasons for this         ever lead to only a partial repair since MintHint did not generate
are (1) the use of statistical correlation which is robust in presence     the expressions that should be used for replacing the faulty ones.
of noise and (2) the ability of MintHint to synthesize compound            With this change, all the previously passing tests continued to pass
hints from building blocks. In particular, the repair spaces were in-      and several previously failing tests too started to pass. In task 2,
complete for tasks 2–4, 7, and 10, and as Table 6 shows, in each of        MintHint did not produce any useful hint for the faulty statement
these cases, the most useful hint was a compound hint.                     (due to excessive noise, as discussed below).
(RQ3) Performance and scalability. The complexity of sta-                     Interestingly, MintHint generated only “retain the statement”
tistical correlation computation dominates the cost of hint genera-        hints for many statements identified by Zoltar. Across the 5 tasks
tion (see Section 3.1.3 for discussion on its complexity). It works        and 75 statements in the fault localization lists, 70 statements are
on a two-dimentional matrix where the number of rows is equal to           likely to be false positives (5 are true positive, i.e., definitely faulty).
the size of the state transformer (the number of input/output pairs)       Out of these, 34 statements (more than 45%) are eliminated by
and the number of columns is equal to the number of expressions in         MintHint. In fact, in tasks 1, 3, and 4, retain were the only other
the repair space. Table 9 gives the performance and scalability chart      type of hints apart from the replace hint required for program repair.
summarizing all runs of the hint generation algorithm for all tasks        We studied the faulty statements which had only the retain hints but
and faulty statements in the user study. Despite the large datasets,       could not identify a way to change them to repair the faults.
the hint generation algorithm scales well. Zoltar took slightly over          This study gives preliminary evidence that MintHint can be ap-
2m on an average for fault localization. Except for a few state-           plied to large programs with not so accurate fault localization lists.
ments, KLEE ran to completion on all the failing tests within 5m
(the timeout set by us). The timings are measured on a desktop             (RQ2) Robustness. Repair spaces were constructed in a man-
with Intel i5 CPU@3.20 GHz and 4GB RAM.                                    ner similar to the user study and with the same bound on expression
                                                                           sizes. As shown in Table 11, the repair space searched by MintHint
4.2     A Case Study                                                       contained the repaired version of the faulty RHS in all but one case.
Experimental Setup. We applied MintHint on a commonly                      The data obtained for the failing tests however contained noise in
used Unix utility program, the stream editor sed obtained from             all cases except one. Our approach for estimating the amount of
noise is explained in Section 4.1. In one case (task 2), the noise         the quality of repair hints. It is however important to note that the
was 97% and MintHint could not produce any useful hint.                    tasks and test suites we used were also used in numerous previous
                                                                           papers in the area (e.g., [26, 31, 43]). Nevertheless, the number
(RQ3) Performance and scalability. In Table 9, the shaded                  of tasks considered is small, so our findings may not generalize to
cells denote the time taken by MintHint for statistical correlation        other programs or faults. We plan to perform an additional exten-
analysis and hint generation for the tasks in the case study. No           sive empirical evaluation to confirm our current results.
task took more than 5m for these steps. Fault localization finished
within 1m on an average for these tasks. While symbolic execution          5    Related work
completed within 5m on most failing tests for the first three tasks it
required 15m for most cases for tasks 4 and 5. However, even with             Early work by Arcuri [2], later extended by Le Goues and col-
15m threshold, it timed out for all failing tests and all potentially      leagues [29], proposes the use of genetic programming to automat-
faulty statements for the sixth task.                                      ically generate repairs that make failing test cases pass and do not
                                                                           break any passing test case. Debroy and Wong propose a similar
4.3     Limitations and Threats to Validity                                approach, but based on the use of mutation [10].
   One of the main limitations of our approach is its reliance on             Other approaches rely on the use of program specifications to
symbolic execution for deriving state transformers, which is a com-        repair the code. Pei and colleagues propose an approach for find-
plex and expensive technique. However, these techniques are be-            ing program repairs given program contracts [32, 40]. Jobstmann,
coming increasingly efficient, and many of their practical limita-         Griesmayer, and Bloem use a game theoretical approach for identi-
tions are being addressed (e.g., [13, 36]). Moreover, as we discuss        fying repairs that satisfy a linear-temporal-logic specification of the
in Section 6, we plan to investigate alternative, less expensive ways      program to be repaired [24]. Gopinath, Malik, and Khurshid’s ap-
to build state transformers. Further, it is technically difficult to ob-   proach builds a SAT formula that encodes the constraints imposed
tain only those values which can be observed in the repaired pro-          by the specification on the program behavior and, if the formula is
gram through symbolic execution. This makes the state transform-           satisfiable, derives a repair from the SAT solution [14]. Konighofer
ers noisy. Due to the statistical reasoning applied in MintHint, it        and Bloem present a template-based approach that, given a faulty
produced useful hints even in presence of noise in many cases. The         program and a specification, performs a symbolic analysis of pro-
so-called measurement errors leading to noisy data are common in           gram inputs and template parameters to generate a repair [28]. He
other application domains as well and a large body of work, com-           and Gupta propose a technique that computes the weakest precon-
monly called outlier detection, exists to deal with them (see [5] for      ditions along a failing trace and compares the computed condi-
a survey). We plan to investigate applications of these techniques         tions with functions’ pre- and post-conditions to find and correct
to further improve tolerance of MintHint to noise.                         faults [18]. Logozzo and Ball’s approach generates verified pro-
   Like every empirical evaluation, ours too has potential threats to      gram repairs from failed verification checks of programs that have
validity. Threats to internal validity for the user study include selec-   developer-supplied modular specifications [30].
tion bias where the users working on the same task in control and
                                                                              Yet other approaches leverage the existing test suite to infer spec-
experimental phases may have different expertise and testing bias
                                                                           ifications and generate repairs accordingly. PACHIKA [9] models a
where activities before the study may affect the outcome. Only two
                                                                           program’s behavior for passing and failing test cases and generates
users had indicated low expertise with C programming, to prevent
                                                                           a repair based on the differences between these models of correct
selection bias, we paired them in such a way that their tasks were
                                                                           and incorrect behavior. In a recent paper, Nguyen and colleagues
interchanged in the two phases. Other users picked their tasks ran-
                                                                           propose the SemFix approach that combines angelic debugging [6]
domly. To mitigate testing bias, we ensured that no user worked on
                                                                           and program synthesis [22] to automatically identify program re-
the same task or two faults of the same program, in the two phases
                                                                           pairs [31]. BugFix [21] shares with our approach the idea of pro-
of the user study. Further, we only made a presentation about the
                                                                           viding developers with “bug-fix suggestions”, rather than actual re-
meaning of repair hints to them and did not provide any hands-on
                                                                           pairs. Unlike our approach, however, BugFix generates suggestions
tutorial. There may be faults in our implementation that might have
                                                                           using a machine-learning approach based on knowledge acquired
affected our results. To address this threat, we manually checked
                                                                           from previous bug repairs.
many of our results and did not encounter any error.
                                                                              Finally, some approaches perform program repair in specific do-
   Threats to external validity arise because our results may not
                                                                           mains, such as repairs for data structures [11], web application re-
generalize to other group of developers (in the case of user study)
                                                                           pairs [35], and repairs targeted at security vulnerabilities [33] or
and program repair tasks. In the user study, we ensured that the
                                                                           concurrency faults [23].
users did not have any prior experience with the programs used as
repair tasks. While this ensures a level playing field, it leaves out
users who might have better familiarity with the programs. The
                                                                           6    Conclusions and Future Work
tasks in the user study were not hand-picked. We applied a well-              We presented MintHint, a novel technique for semi-automated
defined criterion for their selection. The programs in Siemens suite       program repair. The key novelty of our approach is that it combines
were sorted by the rank of the actual faulty statement in the respec-      symbolic, statistical, and syntactic reasoning to synthesize repair
tive localization lists. Within each rank, the program-fault names         hints, given only the faulty program and a test suite. Our evaluation
were then sorted in the lexicographic order and finally, the first two     of MintHint provides initial but strong evidence that our approach
tasks at each fault localization rank were selected. Similarly, the        is effective. An interesting direction for future work is the inves-
tasks in the case study, involving sed, consist of all tasks from the      tigation of how repair hints could be used to further automate the
SIR repository [12] with only a single faulty statement such that the      program-repair process. For example, we envision that hints could
statement occurs within top 15 statements returned by a third-party        be used to inform program synthesis (e.g., [16, 17, 22]) or sketching
fault localization tool, Zoltar. A few tasks could not be included         (e.g., [37, 38]). In the future, we will extend our technique so that
because of limitations of the symbolic execution tool. The perfor-         it can handle the more challenging case of faults involving multiple
mance of MintHint is a function of the test suite also. It will take a     statements. Finally, in order to improve performance of MintHint,
much larger evaluation to ascertain how the quality of tests affects       we plan to investigate (1) alternative, more efficient techniques for
building operational specifications and (2) outlier detection mech-   [22] S. Jha, S. Gulwani, S. A. Seshia, and A. Tiwari. Oracle-guided
anisms to further improve tolerance of MintHint to noise.                  Component-based Program Synthesis. In ICSE, pages 215–
                                                                           224, 2010.
References                                                            [23] G. Jin, W. Zhang, D. Deng, B. Liblit, and S. Lu. Automated
                                                                           Concurrency-bug Fixing. In OSDI, pages 221–236, 2012.
                                                                      [24] B. Jobstmann, A. Griesmayer, and R. Bloem. Program Repair
 [1] R. Abreu, P. Zoeteweij, and A. J. C. v. Gemund. An Evalu-
                                                                           as a Game. In CAV, pages 287–294, 2005.
     ation of Similarity Coefficients for Software Fault Localiza-
                                                                      [25] J. A. Jones, M. J. Harrold, and J. Stasko. Visualization of
     tion. In PRDC, pages 39–46, 2006.
                                                                           test information to assist fault localization. In ICSE, pages
 [2] A. Arcuri. On the Automation of Fixing Software Bugs. In
                                                                           467–477, 2002.
     ICSE Companion, pages 1003–1006, 2008.
                                                                      [26] M. Jose and R. Majumdar. Cause clue clauses: error localiza-
 [3] T. Ball, M. Naik, and S. K. Rajamani. From Symptom
                                                                           tion using maximum satisfiability. In PLDI, pages 437–446,
     to Cause: Localizing Errors in Counterexample Traces. In
                                                                           2011.
     POPL, pages 97–105, 2003.
                                                                      [27] M. Kendall and J. Gibbons. Rank correlation methods. A
 [4] C. Cadar, D. Dunbar, and D. R. Engler. KLEE: Unassisted and
                                                                           Charles Griffin Book. E. Arnold, 1990.
     Automatic Generation of High-Coverage Tests for Complex
                                                                      [28] R. Konighofer and R. Bloem. Automated Error Localization
     Systems Programs. In OSDI, pages 209–224, 2008.
                                                                           and Correction for Imperative Programs. In FMCAD, pages
 [5] V. Chandola, A. Banerjee, and V. Kumar. Outlier detection:
                                                                           91–100, 2011.
     A survey. ACM Computing Surveys, 2007.
                                                                      [29] C. Le Goues, T. Nguyen, S. Forrest, and W. Weimer. Genprog:
 [6] S. Chandra, E. Torlak, S. Barman, and R. Bodik. Angelic
                                                                           A Generic Method for Automatic Software Repair. IEEE
     debugging. In ICSE, pages 121–130, 2011.
                                                                           Trans. on Software Engineering, pages 54 –72, 2012.
 [7] H. Cleve and A. Zeller. Locating causes of program failures.
                                                                      [30] F. Logozzo and T. Ball. Modular and Verified Automatic Pro-
     In ICSE, pages 342–351, 2005.
                                                                           gram Repair. In OOPSLA, pages 133–146, 2012.
 [8] H. Cramér. Mathematical Methods of Statistics. Princeton
                                                                      [31] H. D. Nguyen, D. Qi, A. Roychoudhury, and S. Chandra.
     Landmarks in Mathematics and Physics. Princeton University
                                                                           SemFix: Program Repair via Semantic Analysis. In ICSE,
     Press, 1945.
                                                                           2013.
 [9] V. Dallmeier, A. Zeller, and B. Meyer. Generating fixes from
                                                                      [32] Y. Pei, Y. Wei, C. A. Furia, M. Nordio, and B. Meyer. Code-
     object behavior anomalies. In ASE, pages 550–554, 2009.
                                                                           based Automated Program Fixing. In ASE, pages 392–395,
[10] V. Debroy and W. E. Wong. Using Mutation to Automatically
                                                                           2011.
     Suggest Fixes for Faulty Programs. In ICST, pages 65–74,
                                                                      [33] J. H. Perkins, S. Kim, S. Larsen, S. Amarasinghe, J. Bachrach,
     2010.
                                                                           M. Carbin, C. Pacheco, F. Sherwood, S. Sidiroglou, G. Sulli-
[11] B. Demsky, M. D. Ernst, P. J. Guo, S. McCamant, J. H.
                                                                           van, W.-F. Wong, Y. Zibin, M. D. Ernst, and M. Rinard. Au-
     Perkins, and M. Rinard. Inference and Enforcement of Dta
                                                                           tomatically Patching Errors in Deployed Software. In SOSP,
     Structure Consistency Specifications. In ISSTA, pages 233–
                                                                           pages 87–102, 2009.
     244, 2006.
                                                                      [34] M. Renieris and S. P. Reiss. Fault localization with nearest
[12] H. Do, S. G. Elbaum, and G. Rothermel. Supporting con-
                                                                           neighbor queries. In ASE, pages 30–39, 2003.
     trolled experimentation with testing techniques: An infras-
                                                                      [35] H. Samimi, M. Schäfer, S. Artzi, T. Millstein, F. Tip, and
     tructure and its potential impact. Empirical Software Engi-
                                                                           L. Hendren. Automated Repair of HTML Generation Er-
     neering: An International Journal, 10(4):405–435, 2005.
                                                                           rors in PHP Applications using String Constraint Solving. In
[13] P. Godefroid, A. V. Nori, S. K. Rajamani, and S. D. Tetali.
                                                                           ICSE, pages 277–287, 2012.
     Compositional may-must program analysis: Unleashing the
                                                                      [36] N. Sinha, N. Singhania, S. Chandra, and M. Sridharan. Alter-
     power of alternation. In ACM Sigplan Notices, volume 45,
                                                                           nate and learn: Finding witnesses without looking all over. In
     pages 43–56, 2010.
                                                                           CAV, pages 599–615, 2012.
[14] D. Gopinath, M. Z. Malik, and S. Khurshid. Specification-
                                                                      [37] A. Solar-Lezama, R. Rabbah, R. Bodík, and K. Ebcioğlu.
     based program repair using sat. In TACAS, pages 173–188,
                                                                           Programming by Sketching for Bit-streaming Programs. In
     2011.
                                                                           PLDI, pages 281–294, 2005.
[15] A. Groce, D. Kroening, and F. Lerda. Understanding Coun-
                                                                      [38] A. Solar-Lezama, L. Tancau, R. Bodík, S. A. Seshia, and V. A.
     terexamples with Explain. In CAV, pages 453–456, 2004.
                                                                           Saraswat. Combinatorial sketching for finite programs. In
[16] S. Gulwani. Automating String Processing in Spreadsheets
                                                                           ASPLOS, pages 404–415, 2006.
     using Input-Output Examples. In PLDI, pages 317–330,
                                                                      [39] I. Vessey. Expertise in Debugging Computer Programs. Inter-
     2011.
                                                                           national Journal of Man-Machine Studies: A process analy-
[17] S. Gulwani, V. A. Korthikanti, and A. Tiwari. Synthesizing
                                                                           sis, pages 459–494, 1985.
     Geometry Constructions. In PLDI, pages 50–61, 2011.
                                                                      [40] Y. Wei, Y. Pei, C. A. Furia, L. S. Silva, S. Buchholz, B. Meyer,
[18] H. He and N. Gupta. Automated debugging using path-based
                                                                           and A. Zeller. Automated Fixing of Programs with Contracts.
     weakest preconditions. In FASE, pages 267–280, 2004.
                                                                           In ISSTA, pages 61–72, 2010.
[19] M. Hutchins, H. Foster, T. Goradia, and T. Ostrand. Experi-
                                                                      [41] K. Zhang, R. Statman, and D. Shasha. On the editing dis-
     ments of the effectiveness of dataflow- and control flow-based
                                                                           tance between unordered labeled trees. Inf. Process. Lett.,
     test adequacy criteria. In ICSE, pages 191–200, 1994.
                                                                           42(3):133–139, 1992.
[20] T. Janssen, R. Abreu, and A. J. C. van Gemund. Zoltar: A
                                                                      [42] X. Zhang, N. Gupta, and R. Gupta. Locating Faults through
     toolset for automatic fault localization. In ASE, pages 662–
                                                                           Automated Predicate Switching. In ICSE, pages 272–281,
     664. IEEE Computer Society, 2009.
                                                                           2006.
[21] D. Jeffrey, M. Feng, N. Gupta, and R. Gupta. Bugfix: A
                                                                      [43] X. Zhang, N. Gupta, and R. Gupta. Locating faults through
     Learning-based Tool to assist Developers in Fixing Bugs. In
                                                                           automated predicate switching. In ICSE 2006, pages 272–
     ICPC, pages 70–79, 2009.
281, 2006.
