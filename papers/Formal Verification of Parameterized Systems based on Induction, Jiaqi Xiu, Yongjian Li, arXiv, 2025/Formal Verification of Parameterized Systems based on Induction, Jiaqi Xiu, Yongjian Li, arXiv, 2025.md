                                         Formal Verification of Parameterized Systems based
                                                             on Induction
                                                                      1st Jiaqi Xiu                                                  2nd Yongjian Li†
                                                          Key Laboratory of System Software                                 Key Laboratory of System Software
                                                 Institute of Software, Chinese Academy of Sciences                Institute of Software, Chinese Academy of Sciences
                                                                    Beijing, China                                                    Beijing, China
                                                                    xiujq@ios.ac.cn                                                  lyj238@ios.ac.cn
arXiv:2503.18030v1 [cs.LO] 23 Mar 2025




                                            Abstract—Parameterized systems play a crucial role in the            number of processors has made the parallelism of caches an
                                         computer field, and their security is of great significance. Formal     important means of enhancing system performance [3]–[6].
                                         verification of parameterized protocols is especially challenging       Distributed protocols are core technologies for ensuring correct
                                         due to its “parameterized” feature, which brings complexity and
                                         undecidability. Existing automated parameterized verification           and efficient data exchange and coordination among multiple
                                         methods have limitations, such as facing difficulties in automat-       computing nodes. With the rapid development of technologies
                                         ically deriving parameterized invariants constrained by mixed           such as cloud computing and big data, the application sce-
                                         Forall and Exists quantifiers, or having challenges in completing       narios of distributed systems have become more extensive,
                                         the parameterized verification of large and complex protocols.          playing important roles in file systems, high-performance
                                         This paper proposes a formal verification framework for param-
                                         eterized systems based on induction, named wiseParaverifier. It         computing, and database systems [7]–[9].
                                         starts from small concretizations of protocols, analyzes inductive         In these parameterized systems, security is a primary
                                         counterexamples, and constructs counterexample formulas to              consideration, especially in systems involving sensitive data
                                         guide the entire process of parameterized verification. It also         processing, network communication, and multi-user environ-
                                         presents a heuristic Generalize method to quickly find auxiliary        ments. Therefore, the formal verification of parameterized
                                         invariants, a method for promoting complex mixed quantifiers
                                         and merging parameterized invariants, and uses symmetric re-            protocols, namely parameterized verification, has attracted
                                         duction ideas to accelerate the verification process. Experimental      extensive attention from both academia and industry [10].
                                         results show that wiseParaverifier can successfully complete            The key in verifying parameterized protocols lies in finding
                                         automatic inductive verification on 7 cache coherence protocols         a set of auxiliary invariants that, together with the security
                                         and 10 distributed protocols. It has strong verification capabilities   properties, can form inductive invariants, thereby completing
                                         and migration capabilities, and can provide concise and readable
                                         verification results, which is helpful for learners to understand       the parameterized verification.
                                         protocol behaviors.                                                        The challenge in the inductive proof of parameterized sys-
                                            Index Terms—Formal verification, Inductive verification, Pa-         tems is that although it is relatively straightforward to identify
                                         rameterized systems,Cache coherence protocols, distributed pro-         inductive invariants for certain small scale concretizations of
                                         tocols.                                                                 the system, it does not imply that these invariants will retain
                                                                                                                 their inductive characteristics when applied to larger scale
                                                                I. I NTRODUCTION                                 system concretizations. To address this issue, researchers have
                                            Parameterized systems play a crucial role in the com-                proposed many methods to automate this process. The first
                                         puter field, modeling parameterized systems leads to the                type, inductive verification starting from small concretizations
                                         formation of parameterized protocols. The parameters within             [11]–[15], but may face the state space explosion problem,
                                         these systems typically represent system configurations or              has high requirements for model checkers, and struggles to
                                         environmental conditions, such as variables that can affect             generalize complex invariants withmixed Forall and Exists
                                         system behavior, including the number of processes, resource            quantifiers. The second type, using data-driven techniques
                                         limitations, the number of users, or network nodes. Common              to directly construct parameterized auxiliary invariants [16]–
                                         types of parameterized protocols include cache coherence                [18], has a large enumeration volume, is prone to explosion
                                         protocols, distributed protocols, security protocols, and net-          of enumeration in complex protocol verification, and the
                                         work communication protocols, which are widely applied in               auxiliary invariants found are less concise and less readable.
                                         areas such as hardware design verification and multi-hreaded            Futhermore, most current automated verification tools can only
                                         programs [1], [2].                                                      handle single type parameterized protocols.
                                            In modern computer architectures, cache coherence pro-                  Limited by the scale and the diversity of protocols, devel-
                                         tocols are key technologies for ensuring the consistency of             oping a general and efficient automated parameterized verifi-
                                         cached data in multi-core or multi-processor systems. With the          cation system has emerged as an urgent issue that demands
                                         development of computer hardware technology, the increasing             immediate resolution. In response to this problem, this paper
conducts idepth research. Starting from small examples, we          time monitoring and learning methods to generate effective
proposed a counter example guided inductive verification            invariant expressions through dynamic program analysis. Yao
method. The main contributions of this paper are as follows:        et al. [16], [17] used data-driven methods and Ivy [21] for
  1) A formal verification framework wiseParaverifier for           auxiliary verification to directly construct and filter parame-
     parameterized systems based on induction is proposed.          terized invariants. This approach is fast for verifying simple
     It begins with small concretizations of protocols, deeply      distributed protocols and can infer complex invariants with
     analyzes inductive counter examples, and presents a            mixed Forall/Exists quantifiers based on invariant templates,
     method for constructing counter example formulas.              automating the verification of several Paxos variants [17].Ivy
  2) A heuristic Generalize method for quickly finding aux-         is a successful automatic reasoning framework for inductive
     iliary invariants is proposed. The proposed method con-        properties in recent years. However, since it is unable to
     structs heuristic information based on variable analysis       automatically derive the inductive invariants of protocols,
     of pre-invariants, enabling rapid identification of the        subsequent automation work only uses it as an auxiliary
     candidate invariants set where the target auxiliary in-        verification tool in the inductive relation proof stage.
     variant lies. By combining incremental and decremental            These methods have an advantage in quantifier general-
     strategies, redundant terms are further eliminated to          ization since they avoid parameterizing invariants from con-
     obtain the most concise description of the auxiliary           cretizations to parameterized forms. However, their verifica-
     invariant.                                                     tion speed is often limited by heuristic information such as
  3) A method for promoting complex mixed quantifiers               invariant templates.
     guided by type saturation and a theory for merging                                      III. M ETHOD
     parameterized invariants are proposed. Aiming at the
     difficulty of accurately deriving Forall/Exists quanti-           As shown in Fig. 1, wiseParaverifier is an inductive formal
     fier mixed constraints, this proposed method achieves          verification method for parameterized systems that can au-
     fast and accurate inference of complex descriptions of         tomatically and efficiently search for and construct auxiliary
     Forall/Exists mixed quantifiers in parameterized invari-       invariants for the target safety properties of parameterized
     ants through fine grained grouping and expansion.              protocols, and complete inductive proofs of the protocols.
                                                                    The verification process consists of two stages: analyzing
                     II. R ELATED W ORK                             and constructing specific auxiliary invariants (invFinder), and
A. Verification Starting from Small Concretizations                 generalizing and proving parameterized inductive invariants
   Researchers observed that inductive invariants often remain      (Verifier).
relatively stable as protocol parameters increase. Lv et al.        A. invFinder
[11] combined implicit invariants with the CMP method
                                                                       In this stage, the system will automatically analyze inductive
to use small protocol concretizations as reference instances
                                                                    counterexamples and construct specific auxiliary invariants for
for computing auxiliary invariants. L-CMP [19] designed
                                                                    the input protocols. The auxiliary invariant determination is
an automated parameterized verification framework based on
                                                                    designed as a Client-Server architecture, where the server side
association rule learning, which automatically learns auxil-
                                                                    encapsulates Murphi [22], NuSMV and NuSMV-BMC [23]
iary invariants from small concretizations of parameterized
                                                                    services. This stage has the following steps:
systems, abstracts them, and performs verification. In the
                                                                       1) Obtaining Minimum Concretizations of Transition Rules
verification of distributed protocols, I4 [20] was the first work
                                                                    and Safety Properties: Since wiseParaverifier uses inductive
to automatically construct inductive invariants and complete
                                                                    verification starting from small concretizations, the selection
parameterized verification. IC3PO [13], [15] also starts with
                                                                    of initial sizes for protocols directly affects the efficiency of
invariants from small protocol concretizations and generalizes
                                                                    all inductive verification processes. The principles for selecting
the inductive verification relationships of small concretizations
                                                                    protocol concretization sizes are as follows:
to parameterized systems. SWISS [14] iteratively strengthens
inductive invariants by adding invariants constructed from             1) Concretization begins with the parameters in the in-
small concretizations until they are sufficient to prove param-            variant. First determine the minimum concretization
eterized protocols.                                                        based on the parameters required by the invariant, then
   These methods starting from small concretizations have                  determine the minimum concretization of the rules based
achieved success in verifying cache coherence and distributed              on the parameter relationships between invariants and
protocols. However, they struggle to verify both types of                  rules.
protocols effectively.                                                 2) The concrete protocol must be sufficient to simulate the
                                                                           same or symmetric transition behaviors as the protocol
B. Verification via Direct Construction of Parameterized Aux-              under any parameters.
iliary Invariants                                                      3) Among concretizations satisfying the above conditions,
  Unlike methods starting from small concretizations, these                select the smallest concretization N.
approaches directly construct parameterized auxiliary invari-          Assuming both invariant F and rule R contain only type1
ants at the parameterized level. LIDO [18] combines run-            variables, we denotes the actual parameter count required by
                                                        Fig. 1. Workflow of wiseParaverifier



F as m, and the actual parameter count required by R as k.                    •  guard(R) represents the values of all relevant variables
For simplicity, type1 in F can be instantiated as 1, 2, · · · , m,               in the guard part of transition rule R at state s.
                                                                                                    ′
and type1 in R can be instantiated according to permutations                  • asgn2Form(act(R )) represents the assignments to all
of 1, 2, · · · , n. Although theoretically n can take multiple                   relevant variables in the action part a of transition rule
values, to simplify the verification process and avoid duplicate                 R′ at state s′ .
concretizations, this section only considers the minimum n                    • assumptions(R, F ) represents variables appearing in in-
satisfying the above relationships. Examples of instantiation                    variant F but not in the action part a of transition rule
for different m, k, and n values include:                                        R. All variables var′ in assumptions(R, F ) are assigned
  1) If m = 2 and k = 1, type1 in F can be concretized                           values equal to var, implying variables unchanged by rule
     as [1, 2]. For R, possible type1 concretizations are                        execution do not directly affect state s′ .
                                                                                     ′                                                ′
     [1], [2], [3]. The first two represent cases where F and                 • ¬F indicates the invariant will not hold at state s , i.e.,

     R share the same concretization, while [3] represents all                   the system reaches a counterexample.
     cases where F and R have different concretization. The                   According to Hoare logic, if s ⊨ F , then s ⊨ preCond(F, a)
     minimum n selected in this example would be 3.                        when s′ is reachable via rule R. If a does not modify any
  2) If m = 2and k = 2, type1 in F is still concretized                    variables in F (s ↔ preCond(F, a)), then F ′ trivially holds
     as [1, 2]. For R, possible type1 concretizations include              after rule execution, meaning no inductive counterexample can
     [1, 2], [1, 3], [2, 1], [2, 3], [3, 1], [3, 2], [3, 4]. Here n = 4,   occur. wiseParaverifier automatically filters out such invalid
     but not all combinations are used due to symmetries or                indOblg formulas.
     redundant meanings. For example, [2, 3] and [2, 4] both                  For each indOblg formula, wiseParaverifier creates a Z3
     represent cases where the first parameter in R matches                solver instance and adds constraints. Solvability is determined
     the second parameter in F , while the second parameter                as follows:
     in R does not appear in F .                                              1) If unsolvable, indOblg(R, F ) has no solution, meaning
   2) Constructing, Filtering, and Solving Counterexample                         ⟨R, F ⟩ does not form a CTI.
Formulas: To satisfy the inductive property of invariants, for                2) If solvable, indOblg(R, F ) has solutions consisting of
any transition rule R leading from state s to s′ , the invariant                  variable value equations eq. In this case, (R, F ) forms
must hold in both s and s′ . If not, the inductive continuity of                  a CTI. The solver returns the first valid solution, which
the invariant is violated. From a counterexample perspective,                     wiseParaverifier uses to construct candidate invariants
the counterexample formula indOblg is constructed as follows:                     by negating the conjunction of eq in s. The constructed
                                                                                  auxiliary invariants follow the pattern in Eq. (2), where
           indOblg(R, F) ≡ guard(R)∧                                              N is the protocol concretization and W is the number
                            asgn2Form(act(R′ ))∧                    (1)           of clause equations.
                            assumptions(R, F ) ∧ ¬F ′                                                   W
                                                                                                        ^
                                                                                               ΩN = ¬       fk , fk = eqi ∨ ¬eqi        (2)
  Where:                                                                                                k
   3) Heuristic Search Method for Auxiliary Invariants: While                    As shown in Fig. 2, F1 represents pre-invariants known
indOblg formulas provide insights into inductive counterex-                   or previously derived by the wiseParaverifier system, while
amples, candidate invariants directly constructed from their                  Sol2 is the solution set of counterexamples for the candidate
solutions are often too complex. wiseParaverifier proposes                    invariant being solved. The equation terms in F1 and Sol2
an efficient heuristic Generalize strategy to filter irrelevant               form sets eq1 and eq2 respectively. Typically, there exists a
variables and construct concise auxiliary invariants.                         subset of identical equation terms join between eq1 and eq2 .
   Empirical analysis indicates that new auxiliary invariants                 This join set serves as heuristic guidance for constructing the
often relate to the ¬F ′ terms in indOblg. As shown in Fig. 2,                minimal auxiliary invariant from Sol2 . Meanwhile, the unique
the heuristic Generalize algorithm uses variable information                  equation terms dif f in Sol2 are incrementally added to the
from previous invariants as guidance to rapidly identify rele-                join set as subsets to form candidate invariant subsets. The
vant terms.                                                                   notation dif f n in Fig. 2 denotes permutations of selecting
                                                                              n equation terms from the dif f set. When the external
                                                                              model checker determines that a candidate invariant subset
                                                                              join + dif f n contains the correct protocol invariant, it is
                                                                              considered the target auxiliary invariant derived from Sol2 ,
                                                                              and the computation of join + dif f n+1 stops.
                                                                                 However, the above determination process does not en-
                                                                              compass the full candidate invariants determination process
                                                                              involved in the heuristic Generalize algorithm. This is because
                                                                              although the invariant information set join provides heuristic
                                                                              guidance during the Generalize process, not all equation terms
Fig. 2. Illustration of the Core Idea of the Heuristic Generalize Algorithm   in join are effective. Nevertheless, the remaining candidates
                                                                              are already very close to the target auxiliary invariant. At
Algorithm 1        simplifyAuxInv                                             this point, combining with the two auxiliary invariant search
 1: Inputs: The indOblg set returned by the Z3 solver: solution.
                                                                              algorithms described in Algo. 1 allows for the rapid elimina-
 2: Ouputs: Whether solution successfully constructs the auxiliary invari-    tion of remaining irrelevant terms.In Algo. 1, the functions
    ant. Returns its auxiliary invariant auxInv if success.                   simplifyAuxInvdecreasingly and simplifyAuxInvincreasingly
 3: – simplif yAuxInvdecreasingly: Iteratively remove irrelevant terms
    from the largest initial candidate.
                                                                              represent the Decreasing strategy and the Increasing strategy
 4: – simplif yAuxInvincreasingly: Iteratively add valid terms to the         respectively, and each of them has its own advantages in
    smallest initial candidate.                                               different scenarios.
 5: function simplif yAuxInvdecreasingly(solution)
 6:     canInv ← turnSM V f orm(solution)                                        The process of the Generalize heuristic algorithm is shown
 7:     passCheck ← callN uSM V (canInv)                                      in Algo. 2. This algorithm can be divided into four stages:
 8:     if passCheck then
 9:         auxInv ← canInv                                                      1) Heuristic search for the candidate invariants set con-
10:         if solution.length > 1 then                                              taining the target auxiliary invariant (Lines 13-17 of
11:             for subS ∈ getSublist(solution, solution.length − 1) do              Algo. 2).
12:                 if simplif yAuxInvdecreasingly[0] then
13:                     break                                                    2) Final determination of the target auxiliary invariant by
14:                 end if                                                           combining with Algo. 1 (Lines 18-21 of Algo. 2).
15:             end for                                                          3) Adding constraints to accelerate counterexample solving
16:         end if
17:         return T rue, auxInv                                                     and invariant search (Lines 24-25 of Algo. 2). wisePa-
18:     end if                                                                       raverifier adds constraints to the Z3 solver after each
19:     return F alse, N one                                                         auxiliary invariant is solved to speed up subsequent
20: end function
21: function simplif yAuxInvincreasingly(solution)                                   processes.
22:     for n ∈ solution.length do                                               4) A fallback non-heuristic Generalize method (Lines 30-
23:         for subS ∈ getSublist(solution, n) do                                    32 and 3-11 of Algo. 2) to ensure verification rigor for
24:             auxInv ← turnSM V f orm(solution)
25:             passCheck ← callN uSM V (auxInv)                                     potential invariants not found by the heuristic approach,
26:             if passCheck then                                                    using the simplifyAuxInv algorithm described in Algo. 1
27:                 return T rue, auxInv
28:             end if                                                        B. Verifier
29:         end for
30:     end for                                                               C. Parameterization and Merging of Auxiliary Invariant Con-
31:     return F alse, N one
32: end function                                                              cretizations
                                                                                 The auxiliary invariants obtained by invFinder need to be
   Based on this, we proposes an efficient heuristic Generalize               parameterized in the Verifier stage to complete the parameter-
algorithm. Its core idea is to leverage variable information                  ized verification. The difficulty in this stage lies in determining
from pre-invariants as heuristic guidance to rapidly determine                the correct quantifier constraints that should be added to
the variable terms of subsequent auxiliary invariants.                        each parameter type after generalizing the specific invariants.
wiseParaverifier employs Ivy for automatic inductive verifi-                      Parameter types with this saturation range will be de-
cation, thus the results of parameterization in the described                     scribed using Forall quantifiers in Ω’s parameterization.
Verifier stage are all in Ivy format.                                        2) When γ(t) = 1 (i.e., #(Ω, t) = C(t)), all concretiza-
                                                                                  tions of type t in P (N ) must participate in clause
Algorithm 2 Generalization                                                        Ω. The direct relationship between #(Ω, t) and C(t)
 1: Inputs: Z3 solver SmtSolver, and its returned indOblg solution set            cannot be determined immediately, as the correctness of
    solution.
 2: Ouputs: target concise auxiliary invariant auxInv.                            the concrete invariant may depend on specific permuta-
 3: function regular generalize(solution, SmtSolver)                              tions of the current parameter concretize scale. Directly
 4:    auxInv ← simplif yAuxInv(solution)                                         generalizing to larger scales (N > C(s)) may violate
 5:    if auxInv ̸= N one ∧ isLegal(auxInv) then
 6:        addSM T Assertions(auxInv, SmtSolver)                                  original constraints.Due to potential behavioral changes
 7:    else                                                                       during concretization scaling, the correctness of clause
 8:        auxInv ← N one                                                         Ω is reverified on P (N + 1), leading to two further
 9:    end if
10:    return auxInv                                                              generalization cases:
11: end function                                                                     a) If Ω still holds, indicating symmetric behavior
12: function heuristic generalize(join, dif f, solution, SmtSolver)
13:    if join ̸= N one then                                                             and invariants before/after scaling, type t in the
14:         for n ∈ dif f.length do                                                      parameterized clause Ω uses Forall quantifiers as
15:             for subS ∈ getsublist(dif f, n) do                                       in Case 1.
16:                 canInv ← turnSM V f orm(subS ∪ join)
17:                 passCheck ← callN uSM V (canIN v)                                b) If Ω does not hold, the new concretization break the
18:                 if passCheck then                                                    small concretization constraints, requiring Exists
19:                     auxInv ← simplif yAuxInv(canInv)                                 quantifiers to limit the scope. However, analysis of
20:                     break
21:                 end if                                                               numerous protocol concretizations shows that even
22:             end for                                                                  in this scenario, t may be partially constrained by
23:         end for                                                                      Forall quantifier, while the other part is constrained
24:         if auxInv ̸= N one ∧ isLegal(auxInv) then
25:             addSM T Assertions(auxInv, SmtSolver)                                    by the Exists quantifier.
26:         else                                                             Therefore, it is necessary to perform more fine-
27:             auxInv ← N one
28:         end if
                                                                         grained quantifier parameterization grouping for all specific
29:    end if                                                            t1 , t2 · · · tn of type t. Treating t1 , t2 · · · tn as minimal group-
30:    if join is N one ∨ auxInv is N one then                           ings of type t, the extended invariant for each grouping g
31:         auxInv ← regular generalize(solution, SmtSolver)
32:    end if
                                                                         is constructed for the concretization P (N + 1) using the
33:    return auxInv                                                     following formula:
34: end function
                                                                                          Ω′g = Ω g N 7→ g N +1 , Ω′ = Ω′g ∧ Ω
                                                                                                                
                                                                                                                                             (4)
   Hybrid Quantifier Generalization Based on Type Sat-                      The extension principle of g N 7→ g N +1 in Eq. (4) is to
uration The proposed method developed a parameterized                    supplement all possible parameter concretizations of the types
invariant quantifier deriving method based on parameter type             involved in the group g within g N +1 , as shown in Eq. (5).
saturation characteristics, which can rapidly and accurately
infer complex Forall and Exists quantifier descriptions in                                                       N^
                                                                                                                  t +1

parameterized invariants.                                                                      g N 7→ g N +1 =           gi                 (5)
   In this method, C(t) = nt is defined as the concrete size                                                       i
of parameter type t in protocol P (N ), and #(Ω, t) represents              The pattern of the clause Ω before extension is expressed
the number of constant concretizations of parameter type t               in Eq. (2), while the extended clause Ω′ follows the form in
appearing in clause Ω. Based on this, the type saturation γ(t)           Eq. (6).
of parameter type t is defined as follows:                                                                           !
                                                                                                    W       N^
                                                                                                             t +1
                                   #(Ω, t)                                                  ′
                                                                                          Ω =¬
                                                                                                    ^
                                                                                                       fk ∧       gi              (6)
                          γ(t) =                                  (3)
                                    C(t)                                                                k          i
   The type saturation γ(t) ranges from (0, 1]. Based on                   Introducing the existential quantifier Exists to transform
whether γ(t) = 1, the generalization cases can be divided                Eq. (6) further yields an equivalent formula description ex-
into the following two scenarios:                                        pressed in Eq. (7).
   1) When γ(t) ̸= 1 (i.e., #(Ω, t) < C(t)), all concretiza-                                                                  !
                                                                                                                    W
      tions of type t in P (N ) do not fully participate in clause                                                  ^
      Ω. Increasing C(t) in P (N ) does not affect #(Ω, t),                         Ω′ = ∃i : t1 , t2 , ..tNt +1 .¬   fk ∧ gi      (7)
                                                                                                                       k
      meaning the occurrence of type t in Ω is independent
                                                                                                    ′
      of its concrete size. Even concretizing type t to larger             If P (N + 1) ⊭ Ω , it indicates that the behavior of
      values only produces symmetrically equivalent clauses              grouping g can be preserved in the extended concretization,
      to small concretizations.                                          and the constraints derived from small concretizations can be
applied to the extended one. The concretized tg represented by         1) Pure Forall-quantified types: Allow free permutations.
this grouping will be described using Forall quantifiers after         2) Pure Existential-quantified types: Permutations are re-
parameterization. Conversely, if P (N + 1) ⊨ Ω′ , it means                stricted to maintain correctness.
the grouping g depends on specific concretized descriptions,           3) Hybrid types: Combine Forall and Existential quanti-
and the constraints from small - scale concretizations can-               fiers.
not be directly applied to the extended concretization. The
                                                                    Algo. 3 distinguishes these cases to efficiently generate sym-
concretized tg represented by this grouping will be described
                                                                    metric invariants while preserving logical correctness.
using Exists quantifiers after parameterization. Notably, when
multiple extended groupings of type t satisfy P (N + 1) ⊨ Ω′ ,
the parameterized concretized tg of each grouping will be           Algorithm 3 getSymmetryInvs: Symmetric Invariant Gen-
connected by ∨.                                                     eration Algorithm
                                                                     1: Inputs: oriInv: auxiliary invariant get by Generalization
   Parameterized Invariant Merging The principle for                 2: Ouputs: symmInvs: All symmetric invariants of oriInv
merging and streamlining parameterized invariants is as fol-         3: –Analyze variable/type concretization distributions and filter existential
lows: If the variable types and equation terms described by             types
                                                                     4: S ← P arse(oriInv)
the Forall quantifier in the clauses are exactly the same, and       5: (D, V ) ← AnalyzeV ariables(S)
the variable types described by the Exists quantifier are the        6: E ← F ilterExistentialT ypes(D, V )
same, then merging can be considered. Denote the merged              7: –Generate permutations based on quantifier patterns
                                                                     8: R = ×[P ermute(V [t])|t ∈   / E] // Forall quantified types only
parameterized invariant as ϕ. wiseParaverifier can perform the       9: E P = ×[P ermute(ExistV ars(V [t]))| ∈ E] // Existential parts
merging of parameterized invariants in the following scenarios:         of hybrid types
   1) Simple Equivalence Merging. Some different auxiliary          10: F P = ×[P ermute(F orallV ars(V [t]))|t ∈ E] // Forall parts of
                                                                        hybrid types
      invariant concretizations may parameterize to identical       11: –Generate symmetric invariants through permutation combinations
      parameterized invariants via Hybrid Quantifier Gener-         12: for r ∈ R do
      alization Based on Type Saturation. For such invariant        13:     for e ∈ E P do
                                                                    14:         for f ∈ FP do
      groups, retaining one representative as ϕ suffices.           15:             S r = ApplyCombination(S, r)
   2) Implication Merging. When a group of parameterized            16:             S e = ApplyCombination(S r, e) ∧ S r
      invariants satisfies the implication relationship defined     17:             S f inal = ApplyF orallP erm(S e, f ) ∧ Se
                                                                    18:             symmInvs ← SymmInvs ∧ Assemble(S f inal)
      in Eq. (8), select ϕ = φ k:                                   19:         end for
                                    n
                                    ^                               20:     end for
                            φ k⇒       φ i                   (8)    21: end for
                                                                    22: return symmInvs
                                    i=1
  3) Constraint Strengthening Merging. When invariant com-
     binations share identical term structures and quantifier          Since a single counterexample may generate multiple aux-
     patterns, a new stronger single constraint  ϕ can replace      iliary invariants, many of which are equivalent or symmetric,
                                       Vn
     the original multiple constraints i=1 ϕi . The strength-       the Generalize process risks becoming trapped in redundant
                                                      Vn
     ened invariant ϕ and the multiple constraints i=1 ϕi           invariant construction. To address this, symmetry reduction can
     must satisfy the relationship in Eq. (9) with the original     be applied during Generalize to avoid generating equivalent or
     invariants:                                                    symmetric invariants.
                       ^n              n
                                       ^
                  ϕ⇒       φi and          φi ⇏ ϕ           (9)     Algorithm 4 addSM T Assertions: SMT Acceleration Algo-
                        i=1               i=1                       rithm
   1) Symmetry Reduction Principles: Although the heuristic           Inputs: auxInv: The auxiliary invariant that have completed the Gener-
Generalize algorithm saves significant computational overhead         alize process.
                                                                      Inputs: SmtSolver: The current instance of the Z3 solver.
for constructing auxiliary invariants , including solver solving      symmInvs ← getSymmetryInvs(auxInv)
and external model checking tool calls, protocols with high           for subI ∈ auxInv ∪ symmInvs do
complexity (e.g., Flash protocol) may still trap wiseParaverifier         SmtSolver.add(turnSM T Assertion(subI))
                                                                      end for
in state space explosion.
   To address this challenge, we apply symmetry reduction
principles from model checking to the auxiliary invariants             Specifically, after the Generalize algorithm constructs
solving phase of wiseParaverifier. Parameterized protocols          an auxiliary invariant auxInv, all its symmetric counter-
contain abundant symmetric system structures and states, lead-      parts symmInvs are precomputed. The combined constraint
ing to symmetric relationships in auxiliary invariants derived      auxInv ∧ symmInvs is then added to the Z3 solver as a new
from protocol CTIs. These symmetries introduce redundant            assertion to block future generation of symmetric invariants.
computational costs during verification.                               Finally, Algo. 4 incorporates all symmetric invariants and
   Algo. 3 demonstrates how to construct all symmetric in-          the original invariant into the Z3 solver during the Generalize
variants for an auxiliary invariant. After generalization, the      process. This algorithm corresponds to the implementation of
concretetized types may fall into three categories:                 lines 6 and 25 in the Generalization procedure.
                                                               TABLE I
                              AUTOMATIC PARAMETERIZED I NDUCTIVE V ERIFICATION R ESULTS OF WISE PARAVERIFIER

                                            Automated Verification Completion Time (s)               Final Number of Parameterized Invariants
                  Protocols
                                        wiseParaverifier   Paraverifier   DuoAI      IC3PO      wiseParaverifier   Paraverifier   DuoAI      IC3PO
              MutualExNodata                  1.46             1.98         1.01      1.82             4                5           14          5
                 MutualEx                     2.96             3.37         2.49      3.16             6                6           16          6
               MutualEx M2                   17.12             error       28.10      26.94            13              error        32          12
               GermanNodata                  19.14            21.76       535.80       fail            39               40          892       fail
                  German                     49.20            57.67         fail       fail            55               58          fail      fail
                FlashNodata                  329.91           342.17        fail       fail            95              152          fail      fail
                    Flash                    585.68           589.23        fail       fail           135              162          fail      fail
             Decentralized lock               4.66             error        9.38      5.98             15              error        16          4
                Lock server                   0.24             error        1.31      2.60             1               error         1          2
             Multi lock server                2.55             error        1.94      11.05            11              error        12          9
              Ricart-Agrawala                 0.43             error        0.90      2.40             2               error         6          3
                   Shard                      3.13             error        1.98      5.43             13              error        15          7
            Two phase commit                  4.23             6.18         2.12      5.29             10               10           7          11
          Client server ae(Exists)*           3.28             error        2.50      3.32             2               error         4          2
        Client server db ae(Exists)*          6.83             error        4.12       fail            8               error         7        fail
         Toy consensus epr(Exists)*           4.97             error        3.92      3.61             4               error         4          3
           Consensus epr(Exists)*             43.10            error      28.88     1248.26           16              error         7           8
                      1. error: After modeling the protocol according to the method’s requirements, the compilation process failed.
            2. fail: After inputting and modeling the protocol according to the method’s requirements, the verification cannot be completed.
            3. (Exists)*: The protocol verification process involves parameterized types requiring the use of Forall/Exists hybrid quantifiers.



                         IV. E XPERIMENT                                              Flash protocol automatically, albeit requiring signifi-
                                                                                      cantly more auxiliary invariants than wiseParaverifier.
   We quantitative analysis the automated parameterized in-
                                                                                      However, Paraverifier failed to verify MutualEx M2 and
ductive verification capabilities of wiseParaverifier across 17
                                                                                      all distributed protocols in the validation set due to its
classic protocols, including 7 cache coherence protocols and
                                                                                      inability to handle high-dimensional array variables and
10 distributed protocols, with 4 distributed protocols requiring
                                                                                      infer Forall/Exists hybrid quantifiers.
complex Forall/Exists hybrid quantifiers to describe parameter-
                                                                                   2) DuoAI, the first work to automate Paxos and several
ized auxiliary invariants. All experiments were conducted on
                                                                                      of its variants (excluding vertical Paxos), showed robust
an 18 cores Intel(R) Gold 6254 CPU @ 3.10GHz. Notably, the
                                                                                      inductive verification capabilities. Table I reveals that
Server side typically only needed to run once, with relevant
                                                                                      DuoAI achieved marginally faster average verification
information of executed protocols recorded in its context.
                                                                                      times than wiseParaverifier on distributed protocols.
A. Comparative Study                                                                  However, this difference was negligible due to the small
                                                                                      state spaces and invariant candidate enumerations of
   This work selects recent state-of-the-art approaches: Par-                         these protocols. For cache coherence protocols with
averifier, DuoAI, and IC3PO as benchmarks for comparing                               richer variable types and more rules, such as German
the verification capabilities of wiseParaverifier. Tab. I presents                    and Flash, DuoAI not only incurred significantly longer
a detailed comparison between wiseParaverifier and these                              runtimes and generated more invariants but also suffered
advanced methods in terms of automated verification com-                              from candidate invariant enumeration space explosion
pletion time and number of parameterized invariants required                          during verification.
to achieve verification.                                                           3) IC3PO performed well on distributed protocols but
   The qualitative results presented in Tab. I demonstrate that                       struggled with cache coherence protocols, verifying
the wiseParaverifier excels in the inductive verification of the                      only 3 simple cases (the worst among the three base-
automated protocol:                                                                   lines). It also exhibited limited ability to infer complex
   1) Paraverifier demonstrated strong performance in auto-                           Forall/Exists hybrid quantifiers, completing verification
       mated inductive verification of cache coherence proto-                         for 3 out of 4 distributed protocols requiring such
       cols, successfully verifying 6 out of the 7 protocols                          quantifiers. On the Consensus protocol, IC3PO’s runtime
       in this work with completion times comparable to                               lagged significantly behind wiseParaverifier and DuoAI.
       wiseParaverifier. Notably, it was the only state-of-the-                       Despite these limitations, IC3PO produced relatively
       art method in Tab. I capable of verifying the complex
                                                                  TABLE II
                   C OMPARISON E XPERIMENTAL R ESULTS OF D IFFERENT G ENERALIZE A LGORITHMS AND T HEIR U SAGE S TRATEGIES

                                                   Simple Generalize Algorithm                                                 Heuristic Generalize Algorithm
                Protocols             Increasingly Strategy Only   Decreasingly Strategy Only    Auxiliary Utilizing Increasingly Strategy     Auxiliary Utilizing Decreasingly Strategy
                                      Time (s)    call NuSMV       Time (s)      call NuSMV      Time (s)            call NuSMV                Time (s)            call NuSMV
            MutualExNodata              2.18           22            2.2             22            1.46                   22                     1.46                   22
                MutualEx                4.09           55           4.21             44            3.89                   46                     2.96                   40
              MutualEx M2              83.77           227          85.02           227            20.9                  266                    17.12                  226
             GermanNoData              32.45           477          39.45           356           19.14                  297                     19.1                  272
                 German                92.12          1319          97.27           1145          61.74                  703                    49.20                  630
               FlashNodata               /              /             /              /           1669.69                 1818                   329.91                 674
                  Flash                  /              /             /              /              /                      /                    585.68                 965
           Decentralized lock           7.03           120          7.05            109            5.03                   75                     4.66                   60
               Lock server              0.25            4           0.24             4             0.34                    8                     0.25                   5
            Multi lock server           6.01           66           6.73             57            6.73                   57                     2.55                   50
             Ricart-Agrawala            0.44            8           0.43             8             0.54                   10                     0.54                   10
                  Shard                 3.85           66           3.86             65            3.19                   52                     3.13                   52
           Two phase commit             7.88           248          11.42           187            5.66                  119                     4.23                   80
        Client server ae(Exists)*       8.46           159          9.31             89            9.31                   72                     3.28                   45
       Client server db ae(Exists)*    11.68           210          13.58           175           11.33                  154                     6.83                  125
       Toy consensus epr(Exists)*      12.71           121          12.08            97            6.04                   89                     4.97                   88
         Consensus epr(Exists)*       183.23          2909         180.96           2093          72.48                  869                    43.10                  753
                             /: The verification runtime has exceeded 24 hours, and the search for new counterexamples has not ceased.



       concise verification results for most successfully verified                              discovery, deemed unable to complete automated parameter-
       protocols.                                                                               ized verification under the corresponding algorithm strategy
   In summary, wiseParaverifier demonstrates superior com-                                      combination.
prehensive verification capabilities, particularly in complex                                      The comparative results in Tab. II reveal the following
cache coherence protocols characterized by numerous rules,                                      performance trends for the 17 protocols across 4 Generalize
rich variable types, and large reachable state spaces, as well                                  algorithms and strategies:
as distributed protocols involving high-dimensional array vari-                                    1) The Heuristic Generalize Algorithm combined with the
ables and intricate Forall/Exists hybrid quantifier inference.                                        Decreasingly Strategy achieved the best performance,
                                                                                                      attaining the shortest verification time and least NuSMV
B. Ablation Study
                                                                                                      invocations for 15 out of 17 protocols. Its verification
   The designed Generalize algorithm is to construct the                                              times for the remaining two protocols (Lock server and
most concise auxiliary invariants from the solution set of the                                        Ricart-Agrawala) differed from the shortest by only
counterexample formula indOblg. To improve the efficiency                                             0.01s and 0.11s, respectively. Notably, this configuration
of Generalize, we introduces the join and dif f sets in the                                           was the only one capable of completing automated
developed method, proposes a Generalize algorithm based                                               parameterized verification for all 17 protocols.
on heuristic information, and uses the Decreasingly strategy                                       2) The Heuristic Generalize Algorithm with the Increas-
and the Increasingly strategy as auxiliary algorithms for the                                         ingly Strategy performed well, achieving the shortest
heuristic Generalize algorithm.                                                                       verification times for 2 protocols. It successfully verified
   To validate the effectiveness of the Heuristic Generalize                                          16 protocols, with the sole failure being the industrial-
Algorithm proposed in this section, Tab. II presents compara-                                         grade cache coherence protocol Flash, which features
tive experimental results for the 17 protocols in the validation                                      complex specifications, rich variable types, and an ex-
set, detailing the automated verification completion time (in                                         cessively large reachable state space. Verification times
seconds) and number of external model checker invocations                                             for other protocols (except FlashNodata) were compara-
(NuSMV is used in the table) when wiseParaverifier employs                                            ble to the shortest recorded times.
different Generalize algorithms combined with auxiliary strate-                                    3) The simple Generalize Algorithm with the Increasingly
gies during parameterized protocol verification.                                                      Strategy achieved verification times close to the best
   As shown in Tab. II, red text highlights the shortest pa-                                          for small protocols (MutualExNodata, Lock server),
rameterized verification time for each protocol across all 4                                          but incurred significantly longer runtimes for complex
Generalize algorithms and strategies, while light green text                                          protocols (German, Consensus epr). This configuration
indicates the shortest time achieved using the simple Gener-                                          verified 15 protocols but failed to handle large-scale pro-
alize algorithm with different strategy configurations. The “/”                                       tocols Flash and FlashNodata. Additionally, it required
symbol denotes protocols where verification runtime exceeded                                          significantly more NuSMV invocations than the other
86,400 seconds (24 hours) without halting counterexample                                              three configurations.
   4) The simple Generalize Algorithm with the Decreasingly                        [6] M. Kunjir, B. Fain, K. Munagala, and S. Babu, “Robus: fair cache
       Strategy achieved the shortest times for 2 small, simple                        allocation for data-parallel workloads,” in Proceedings of the 2017 ACM
                                                                                       International Conference on Management of Data, 2017, pp. 219–234.
       protocols (Lock server and Ricart-Agrawala), with neg-                      [7] S. Ghemawat, H. Gobioff, and S.-T. Leung, “The google file system,”
       ligible differences in runtime and NuSMV invocations                            in Proceedings of the nineteenth ACM symposium on Operating systems
       compared to other strategies. It verified 15 protocols but                      principles, 2003, pp. 29–43.
                                                                                   [8] F. Chang, J. Dean, S. Ghemawat, W. C. Hsieh, D. A. Wallach, M. Bur-
       failed to handle Flash and FlashNodata, similar to the                          rows, T. Chandra, A. Fikes, and R. E. Gruber, “Bigtable: A distributed
       previous simple algorithm configuration.                                        storage system for structured data,” ACM Transactions on Computer
                                                                                       Systems (TOCS), vol. 26, no. 2, pp. 1–26, 2008.
   The heuristic Generalize Algorithm efficiently constructs                       [9] J. Dean and S. Ghemawat, “Mapreduce: simplified data processing on
minimal auxiliary invariants from counterexample solutions,                            large clusters,” Communications of the ACM, vol. 51, no. 1, pp. 107–113,
accelerating parameterized protocol verification in wisePar-                           2008.
                                                                                  [10] K. R. Apt and D. Kozen, “Limits for automatic verification of finite-
averifier with fewer external model checker calls while han-                           state concurrent systems,” Inf. Process. Lett., vol. 22, no. 6, pp. 307–309,
dling industrial-grade protocols. The Decreasingly Strategy                            1986.
is optimal for heuristic generalization because its pre-pruned                    [11] Y. Lv, H. Lin, and H. Pan, “Computing invariants for parameter
                                                                                       abstraction,” in 2007 5th IEEE/ACM International Conference on Formal
invariant set (join ∧ dif f n ) typically requires only 1-2 redun-                     Methods and Models for Codesign (MEMOCODE 2007). IEEE, 2007,
dant term removals. Light green highlights shortest verification                       pp. 29–38.
times for simple Generalize Algorithm configurations where                        [12] Y. Li, K. Duan, Y. Lv, J. Pang, and S. Cai, “A novel approach to
                                                                                       parameterized verification of cache coherence protocols,” in 2016 IEEE
the Increasingly Strategy outperforms Decreasingly, though                             34th International Conference on Computer Design (ICCD). IEEE,
Decreasingly reduces NuSMV invocations, its complex invari-                            2016, pp. 560–567.
ants cause longer verification, whereas Increasingly’s simpler,                   [13] A. Goel and K. Sakallah, “Towards an automatic proof of lamport’s
                                                                                       paxos,” in # PLACEHOLDER PARENT METADATA VALUE#, 2021,
shorter invariants offset higher invocation counts with faster                         pp. 112–122.
checks.                                                                           [14] T. Hance, M. Heule, R. Martins, and B. Parno, “Finding invariants
                                                                                       of distributed systems: It’s a small (enough) world after all,” in 18th
                            V. C ONCLUSION                                             USENIX symposium on networked systems design and implementation
                                                                                       (NSDI 21), 2021, pp. 115–131.
   In this paper, an inductive formal verification method wiseP-                  [15] A. Goel and K. Sakallah, “On symmetry and quantification: A new
araverifier was proposed for parameterized systems that can                            approach to verify distributed protocols,” in NASA Formal Methods
automatically and efficiently search for and construct auxiliary                       Symposium. Springer, 2021, pp. 131–150.
                                                                                  [16] J. Yao, R. Tao, R. Gu, J. Nieh, S. Jana, and G. Ryan, “{DistAI}:{Data-
invariants, and complete complete the inference of parame-                             Driven} automated invariant learning for distributed protocols,” in 15th
terized invariants and the proof of inductive relationships. By                        USENIX symposium on operating systems design and implementation
utilizing a heuristic Generalize method, wiseParaverifier could                        (OSDI 21), 2021, pp. 405–421.
                                                                                  [17] J. Yao, R. Tao, R. Gu, and J. Nieh, “{DuoAI}: Fast, automated inference
rapidly find auxiliary invariants. Furthermore, A method for                           of inductive invariants for verifying distributed protocols,” in 16th
promoting complex mixed quantifiers guided by type satura-                             USENIX Symposium on Operating Systems Design and Implementation
tion and a theory for merging parameterized invariants are                             (OSDI 22), 2022, pp. 485–501.
                                                                                  [18] Y. Xia, D. Sur, A. S. Pingle, J. V. Deshmukh, M. Raghothaman,
designed, mainly aiming at the difficulty of accurately infer-                         and S. Ravi, “Discovering likely invariants for distributed systems
ring Forall/Exists quantifier mixed constraints. The proposed                          through runtime monitoring and learning,” in International Conference
wiseParaverifier demonstrated robust automated parameterized                           on Verification, Model Checking, and Abstract Interpretation. Springer,
                                                                                       2025, pp. 3–25.
inductive verification capabilities and strong transferability                    [19] J. Cao, Y. Li, and J. Pang, “L-cmp: An automatic learning-based
through multiple experimental groups, which include 7 cache                            parameterized verification tool,” in Proceedings of the 33rd ACM/IEEE
coherence protocols and 10 distributed protocols.                                      International Conference on Automated Software Engineering, 2018, pp.
                                                                                       892–895.
                                                                                  [20] E. A. Emerson and V. Kahlon, “Exact and efficient verification of
                         ACKNOWLEDGMENT                                                parameterized cache coherence protocols,” in Advanced Research Work-
  This research did not receive any specific grant from funding                        ing Conference on Correct Hardware Design and Verification Methods.
                                                                                       Springer, 2003, pp. 247–262.
agencies in the public, commercial, or not-for-profit sectors.                    [21] C. Hawblitzel, J. Howell, M. Kapritsos, J. R. Lorch, B. Parno, M. L.
                                                                                       Roberts, S. Setty, and B. Zill, “Ironfleet: proving practical distributed
                              R EFERENCES                                              systems correct,” in Proceedings of the 25th Symposium on Operating
 [1] P. A. Abdulla, G. Delzanno, and A. Rezine, “Parameterized verification            Systems Principles, 2015, pp. 1–17.
     of infinite-state processes with global conditions,” in Computer Aided       [22] D. L. Dill, “The mur ϕ verification system,” in Computer Aided
     Verification: 19th International Conference, CAV 2007, Berlin, Germany,           Verification: 8th International Conference, CAV’96 New Brunswick, NJ,
     July 3-7, 2007. Proceedings 19. Springer, 2007, pp. 145–157.                      USA, July 31–August 3, 1996 Proceedings 8. Springer, 1996, pp. 390–
 [2] P. A. Abdulla and G. Delzanno, “Parameterized verification,” Interna-             393.
     tional Journal on Software Tools for Technology Transfer, vol. 18, pp.       [23] A. Cimatti, E. Clarke, E. Giunchiglia, F. Giunchiglia, M. Pistore,
     469–473, 2016.                                                                    M. Roveri, R. Sebastiani, and A. Tacchella, “Nusmv 2: An opensource
 [3] D. Fujiki, S. Mahlke, and R. Das, “Duality cache for data parallel                tool for symbolic model checking,” in Computer Aided Verification: 14th
     acceleration,” in Proceedings of the 46th International Symposium on              International Conference, CAV 2002 Copenhagen, Denmark, July 27–31,
     Computer Architecture, 2019, pp. 397–410.                                         2002 Proceedings 14. Springer, 2002, pp. 359–364.
 [4] O. Mallayev, B. Anvarjonov, and M. Aziz, “Cache problems in parallel
     computational processes,” Annals of the Romanian Society for Cell
     Biology, vol. 25, no. 3, pp. 8924–8934, 2021.
 [5] M. Eshel, R. L. Haskin, D. Hildebrand, M. Naik, F. B. Schmuck, and
     R. Tewari, “Panache: A parallel file system cache for global file access.”
     in FAST, vol. 10, 2010, pp. 1–14.
