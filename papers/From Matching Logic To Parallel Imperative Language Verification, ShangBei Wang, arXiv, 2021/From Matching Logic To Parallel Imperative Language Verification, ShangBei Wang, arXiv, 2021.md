                                         1   From Matching Logic To Parallel Imperative
                                         2   Language Verification
                                         3   ShangBei Wang
                                         4   Nanjing University of Aeronautics and Astronautics, Nanjing, China
                                         5   wangshangbei123@nuaa.edu.cn

                                         6         Abstract
                                         7   Program verification is to develop the program’s proof system, and to prove the proof system
                                         8   soundness with respect to a trusted operational semantics of the program. However, many practical
                                         9   program verifiers are not based on operational semantics and can’t seriously validate the program.
                                        10   Matching logic is proposed to make program verification based on operational semantics. In this
                                        11   paper, following Grigore Roşu et al’s work, we consider matching logic for parallel imperative
                                        12   language(PIMP). According to our investigation, this paper is the first study on matching logic for
                                        13   PIMP. In our matching logic, we redefine "interference-free" to character parallel rule and prove the
arXiv:2102.04011v1 [cs.LO] 8 Feb 2021




                                        14   soundness of matching logic to the operational semantics of PIMP. We also link PIMP’s operational
                                        15   semantics and PIMP’s verification formally by constructing a matching logic verifier for PIMP which
                                        16   executes rewriting logic semantics symbolically on configuration patterns and is sound and complete
                                        17   to matching logic for PIMP. That is our matching logic verifier for PIMP is sound to the operational
                                        18   semantics of PIMP. Finally, we also verify the matching logic verifier through an example which is a
                                        19   standard problem in parallel programming.


                                        20   Keywords and phrases Matching Logic, Operational Semantics, Program Verification, Parallel
                                        21   Language


                                        22    1     Introduction

                                        23   Operational semantics[1][7][23] is called “transition semantics” whose basic idea is to use a
                                        24   sequence γ0 → γ1 → γi → · · · of configurations to formalize the execution of a program. γi is
                                        25   either a terminal configuration or a nonterminal configuration. The development of semantics
                                        26   engineering frameworks K[17][18], Ott[29] and PLT-Redex[3] make it very easy to define the
                                        27   operational semantics of a programming language. Consequently, the operational semantics
                                        28   of C[4][5], Java[10], Python[12], CAML[36], JavaScript[8][25] have been proposed. The
                                        29   advantages of operational semantics such as easy to define and understand, being executable
                                        30   and being tested, make it suitable as trusted reference model for language. The ideal program
                                        31   verification should use such operational semantics, unchanged, to produce proof certificates.
                                        32   However, program verification rarely use operational semantics directly, because the proof
                                        33   based on operational semantics directly involve the corresponding transition system, which is
                                        34   generally considered low-level. Hoare[31][34] and dynamic logic[9] are typically used because
                                        35   their reasoning seems higher level. However, the set of abstract proof rules to define language
                                        36   semantics in Hoare and dynamic logic are hard to understand and trust. The essence of
                                        37   program verification is to develop a program’s proof system, and to prove the proof system
                                        38   sound with respect to a trusted operational semantics of the program. However, instead of
                                        39   being based on a formal semantics, many practical program verifiers[6][28][32][33] convert
                                        40   the target program language to an intermediate validation language or simply implement
                                        41   ad-hoc verification condition. If a program verification is not based on the formal semantics
                                        42   of the program, the program verification does not seriously validate the program and the
                                        43   result can’t be trusted.
                                        44   Matching logic[13] is proposed to make program verification based on operational semantics.
                                        45   To reason about program, we first need to define program configurations. Matching logic
42:2        From Matching Logic To Parallel Imperative Language Verification


       46   configuration patterns consist of variables, symbols in signature, first-order logical connectives
       47   and existential quantifiers. For example ∃z(o =<x := x ∗ y>k <x 7→ x, y 7→ z, ρ>env <m>mem
       48   ∧x 6= 0) is matching logic configuration pattern where o is a distinguished variable of sort Cfg
       49   and <· · ·>k holds code fragment and<· · ·>env <· · ·>mem holds program state and x 6= 0 is
       50   the constraint, an arbitrary first-order logical formula. There are two reasons why matching
       51   logic is particularly suitable for program reasoning:

       52      By matching logic configuration patterns, we can get access to any detail in the program
       53      and hide irrelevant details using existential quantization;

       54      Both the operational semantics and reachability properties of a program can be described
       55      as matching logic rules between configuration patterns.
       56   Like Hoare logic, correctness pair ∃X(o =<c>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <
       57   ρ0 >env <m0 >mem ∧ϕ0 ) in matching logic relates configuration before the execution of c to
       58   configuration after it’s execution. Correctness pair should not be viewed as an independent
       59   object but as the result of a proof outline which carries intermediate proof information.
       60   Matching logic has a lot of achievements[16][20][19][14][15][35] in sequential imperative
       61   language (IMP). In [19], Grigore Roşu et al presented matching logic proof system of IMP
       62   and proved the soundness of the matching logic proof system w.r.t. the operational semantics
       63   of IMP. However, when multiple processes execute in parallel, the results are complex and
       64   difficult to handle because the execution order of actions in different processes is unpredictable.
       65   A number of proof systems of PIMP have been proposed, such as temporal logic[30] and
       66   Hoare logic of parallel program [37]. Unfortunately, according to our investigation, there is
       67   no research on matching logic proof system for PIMP.
       68   In this paper, following Grigore Roşu et al’s work[19], we consider matching logic for PIMP,
       69   which include parallelism in matching logic proof system of IMP. Matching logic for PIMP
       70   provides a simple and understandable way to deal with parallelism. More importantly, it
       71   is intuitive and suitable as a basis for a reliable proof outline. In [37], the definition of
       72   "interference-free" is key in characterizing parallel rule. However, this definition can’t be
       73   used directly in matching logic. We had to redefine it so that it could be used in matching
       74   logic. Rewriting logic is the theoretical basis of K, Ott and PLT-Redex. we use rewriting
       75   logic semantics[24][26][27] to give operational semantics of PIMP and define the operational
       76   semantics of PIMP as a rewrite theory. We also try to link PIMP’s operational semantics
       77   and PIMP’s verification formally. First, we prove the soundness of matching logic with
       78   respect to operational semantics of PIMP, and then matching logic verifier for PIMP is given
       79   which execute rewriting logic semantics symbolically on configuration patterns and is sound
       80   and complete for matching logic system of PIMP. Figure 1 shows the relationship among
       81   operational semantics, matching logic and matching logic verifier.
       82     The paper is organized as follows. The next section presents PIMP, a parallel imperative
       83   language with PAR and AWAIT operations to describing cooperation between processes-
       84   synchronization, mutual exclusion; with Env operation to describing a process is executed
       85   in an arbitrary "state", that is, in parallel with other processes. In addition, we define
       86   operational semantics of PIMP by rewriting logic and prove several useful properties. Section
       87   3 introduces matching logic proof system for PIMP and prove the soundness of matching
       88   logic with respect to operational semantics of PIMP. Section 4 gives the matching logic
       89   verifier for PIMP and shows that it is sound and complete for matching logic proof system
       90   for PIMP. That is the matching logic verifier for PIMP is sound to the operational semantics
       91   of PIMP. We also verify the matching logic verifier through an example which is a standard
       92   problem in parallel programming.
      ShangBei Wang                                                                                                  42:3




           Figure 1 Relationship among operational semantics, matching logic and matching logic verifier



93     2      Operational semantics of PIMP

94    In this section, we introduce a simple parallel imperative language(PIMP) by adding await
95    operation, parallel operation and array operations to the IMP[19]. The operational semantics
96    of PIMP is defined as a rewrite logic theory (ΣPIMP , EPIMP , RPIMP )[11]. Figure 2 shows the
97    complete rewrite theory. The signature ΣPIMP consists of the PIMP’s syntax and the syntax
98    of configurations. The configurations of PIMP have the form <· · ·>k <· · ·>env <· · ·>mem ,
99    containing: a computation, an environment and a memory. The Env sort is a partial mapping
100   and has the form x1 7→ i1 , x2 7→ i2 , · · · , xn 7→ in with · representing the empty environment.
101   Like Env sort, the Mem sort is also a partial map structure but from positive naturals to
102   integers. The C sort is computation and · is empty computation with its usual properties
103   : · ; c = c and · kc = c = ck ·. await b then cc computation acts as a flexible but primitive
104   tool for mutual exclusion. Only when the condition b is true, the process can execute
105   await b then cc, otherwise, the process is blocked. The computation cc is an indivisible
106   action. During its execution, other processes are blocked. Hence, it is very desirable to not
107   contain k, while and await computations in CC sort. A := Array(e1 , e2 , · · · , en ) evaluates
108   e1 , e2 , · · · , en to i1 , i2 , · · · , in , allocates a contiguous space with size n and starting address
109   as positive integer p in memory, writes values i1 , i2 , · · · , in in order in that space and assigns
110   p to A. x := A[e] evaluates e to positive integer p, evaluates A to positive integer q and
111   assigns to x the value at location p + q in memory (p + q must be allocated). A[e1 ] := e2
112   evaluates e1 to positive integer p, A to positive integer q and e2 to value i, writes i to location
113   p + q in memory (p + q must be allocated).
114     The EPIMP contains equations which define bags, sequences and maps. We do not list
115   these equations explicitly in Figure 2 because our main goal is to give PIMP an operational
116   semantics in the rewriting logic framework. The semantic rules[2] are the core of a rewrite
117   semantics, and usually each language construct has at least one semantic rule. +, −, ∗, ÷, mod
118   constructs are reduced to the domain +Int , −Int , ∗Int , ÷Int , modInt when its arguments become
119   integers and the =, 6=, <, > constructs are reduced to the domain =Bool , 6=Bool , <Bool , >Bool
120   when its arguments become integers. PAR1 and PAR2 semantic rules use non-determinism
121   to simulate parallelism, but they are defined in such a way that the results are equivalent
122   to those which would be obtained using true parallelism. ARRAY semantic rule chose
123   some arbitrary positive integer p such that (p 7→ [ρ(e)], m) is a well-formed map and
124   update the environment and the memory accordingly where p 7→ [ρ(e)] is a shorthand for
125   p 7→ ρ(e1 ), p + 1 7→ ρ(e2 ), · · · , p + n − 1 7→ ρ(en ) and e ∈ Seq −,− [E] and ρ(e) ∈ Seq −,− [Int].
126   It has been suggested[21][22] that a computation should be thought of as being executed
42:4   From Matching Logic To Parallel Imperative Language Verification



        Rewrite Theory Of PIMP

        Abstract Syntax:

        E ::= 0 | 1 | 2 | · · · | Var | −E | E1 + E2 | E1 − E2 | E1 ∗ E2 | E1 ÷ E2 | E1 mod E2
        B ::= true | f alse | E1 = E2 | E1 6= E2 | E1 < E2 | E1 > E2

        CC ::= Var := E | if (B) CC1 else CC2 | CC1 ; CC2 | Var := Array(Seq −,− [E]) |
        Var[E1 ] := E2 | Var1 := Var2 [E] | skip
        C ::= Var := E | if (B) C1 else C2 | C1 ; C2 | while B do C | C1 k C2 | await B then CC |
        skip | Var := Array(Seq −,− [E]) | Var[E1 ] := E2 | Var1 := Var2 [E]
        Configurtation:
        Cfg ::=<C>k <Env>env <Mem>mem

        Env ::= Map−,−
                   .   [Var, Int]

        Mem ::= Map−,−
                   .   [Nat + , Int]
        Semantic Rules:
                                           ·
        SKIP:                                  P
                <skip>k <ρ>env <m>mem −
                                      →<·>k <ρ>env <m>mem
                                               P
                                      →<c01>k <ρ0>env <m0>mem
                  <c1>k <ρ>env <m>mem −
        SEQ:                                   P
                                         →<c01 ; c2>k <ρ0>env <m0>mem
                <c1 ; c2>k <ρ>env <m>mem −
                                                           ·
        ASGN1:                                         P
                  <x := e>k <ρ>env <m>mem −
                                          →<·>k <ρ[ρ(e)/x]>env <m>mem
                                                                               ·
        ASGN2:                                                 P
                  <x := A[e]>k <ρ>env <m>mem −
                                             →<·>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem
                                                                                   ·
        ASGN3:                                                     P
                  <A[e1 ] := e2>k <ρ>env <m>mem −
                                                →<·>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem
                                                                               ·
        ARRAY:                                                             P
                   <A := Array(e)>k <ρ>env <m>mem −
                                                  →<·>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem
                                       ρ(b) is true
        IF1:                                                       P
               <if (b) c1 else c2>k <ρ>env <m>mem −
                                                  →<c1>k <ρ>env <m>mem
                                       ρ(b) is f alse
        IF2:                                                       P
               <if (b) c1 else c2>k <ρ>env <m>mem −
                                                  →<c2>k <ρ>env <m>mem
                                                           ρ(b) is true
        WHILE1:                                                        P
                    <while b do c>k <ρ>env <m>mem −
                                                  →<c; while b do c>k <ρ>env <m>mem
                                           ρ(b) is f alse
        WHILE2:                                                        P
                    <while b do c>k <ρ>env <m>mem −
                                                  →<·>k <ρ>env <m>mem
                                                                           P ∗
                                                    → <·>k <ρ0>env <m0>mem
                  ρ(b) is true, <cc>k <ρ>env <m>mem −
        AWAIT:                                                             P
                                                    →<·>k <ρ0>env <m0>mem
                   <await b then cc>k <ρ>env <m>mem −
                                                   P
                                        →<c01>k <ρ0>env <m0>mem
                    <c1>k <ρ>env <m>mem −
        PAR1                                       P
                                         →<c01 k c2>k <ρ0>env <m0>mem
                <c1 k c2>k <ρ>env <m>mem −
                                                   P
                                        →<c02>k <ρ0>env <m0>mem
                    <c2>k <ρ>env <m>mem −
        PAR2                                       P
                                         →<c1 k c02>k <ρ0>env <m0>mem
                <c1 k c2>k <ρ>env <m>mem −
                                       ·
        ENV                            E
                                  →<c>k <ρ0>env <m0>mem
               <c>k <ρ>env <m>mem −


          Figure 2 Rewrite Theory Of PIMP
      ShangBei Wang                                                                                         42:5


127   in an arbitrary "state", that is, in parallel with other computations. Therefore, there
                                                                  P
128   are two types of semantic rules, < c >k < ρ >env < m >mem − →< c0 >k < ρ0 >env < m0 >mem
129   represents update of the environment ρ to ρ0 and memory m to m0 because c is executed;
                             E
130   <c>k <ρ>env <m>mem −   →<c>k <ρ0>env <m0>mem represents update of the environment ρ to
131   ρ and memory m to m0 because other computation is executed which is in parallel with c.
       0

132   We can now formally define the operational semantics of PIMP as a rewrite logic theory.

133   I Definition 1. Let PIMP denotes the rewriting logic theory (ΣPIMP , EPIMP , RPIMP ) in Figure
                                             L                  L                                  L ∗
134   2, L = P or L = E, PIMP |= t −  → t0 indicates that t −
                                                            → t0 can be derived. PIMP |= t −
                                                                                           → t0
                                L 0
135   indicates that the rule t −
                                → t can be derived in zero or more steps.

136   Computation k is well-terminated iff it is equal to an integer value or to "·". Let PIMPo be the
                                        o             o
137   algebraic specification (ΣPIMP , EPIMP ) where EPIMP  ⊆ EPIMP contains equations defining bags,
138   sequences and maps. Let T be the initial PIMPo algebra. Terms <k>k <ρ>env <m>mem
                                   o

139   in T o of sort Cfg are called concrete configurations. If k is well-terminated, concrete
140   configurations <k>k <ρ>env <m>mem are called final configurations.

141   I Definition 2. An execution of concrete configuration <k0 >k <ρ0 >env <m0 >mem is any
                                                                                  L
142   finite or infinite sequence of the form: σ ≡<k0 >k <ρ0 >env <m0 >mem −      →<k1 >k <ρ1 >env <
                 L      L                            L                                       L
143   m1 >mem −  → ··· −→<ki >k <ρi >env <mi >mem −  →<ki+1 >k <ρi+1 >env <mi+1 >mem −       → · · · . If
144   the sequence is finite and there exits j ∈ Int, for all j 0 ≥ j, <kj 0 >k <ρj 0 >env <mj 0 >mem is
145   final configuration, we call σ terminable, otherwise, σ no terminable.

      For example c1 ≡ x := 3; if (x > 0) x := x + 1 else x := x − 1 and c2 ≡ await x > 0 then x :=
      10, then a terminable execution of <c1 kc2>k <x 7→ 0>env <·>mem is :
                                                                       P
                                     <c1 kc2>k <x 7→ 0>env <·>mem −
                                                                  →
                                                                                                     P
       <if (x > 0)x := x + 1 else x := x − 1k await x > 0 then x := 10>k <x 7→ 3>env <·>mem −
                                                                                            →
                                                                                        P
                   <if (x > 0) x := x + 1 else x := x − 1k·>k <x 7→ 10>env <·>mem −
                                                                                  →
                                                            P
                   <x := x + 1>k <x 7→ 10>env <·>mem −
                                                     →<·>k <x 7→ 11>env <·>mem
      which can be broken down into two terminable executions:
                                     P
       <c1>k <x 7→ 0>env <·>mem −
                                →<if (x > 0)x := x + 1 else x := x − 1>k <x 7→ 3>env <·>mem
                    E                                                                    P
                   −
                   →<if (x > 0)x := x + 1 else x := x − 1>k <x 7→ 10>env <·>mem −
                                                                                →
                                                            P
                   <x := x + 1>k <x 7→ 10>env <·>mem −
                                                     →<·>k <x 7→ 11>env <·>mem
      and
                                         E                             P
        <c2>k <x 7→ 0>env <·>mem −
                                 →<c2>k <x 7→ 3>env <·>mem −
                                                           →<·>k <x 7→ 10>env <·>mem
                        E                               E
                        −
                        →<·>k <x 7→ 10>env <·>mem −
                                                  →<·>k <x 7→ 11>env <·>mem
146



147   I Proposition 3. For any c1 , c2 ∈ C , if σ is an execution of concrete configuration <
148   c1 kc2>k <ρ>env <m>mem and σ is terminable, then σ can be broken down into two terminable
149   executions σ1 , σ2 , which are executions of concrete configurations <c1>k <ρ>env <m>mem
150   and <c2>k <ρ>env <m>mem respectively.
42:6         From Matching Logic To Parallel Imperative Language Verification


             Proof. Suppose
                                                          L                                L     L
                     σ ≡<c10 kc20>k <ρ0>env <m0>mem −
                                                    →<c11 kc21>k <ρ1>env <m1>mem −
                                                                                 → ··· −
                                                                                       →
                                                      L         L
                        <c1i kc2i>k <ρi>env <mi>mem −
                                                    → ··· −
                                                          →<c1n kc2n>k <ρn>env <mn>mem
             where c10 = c1 and c20 = c2 and ρ0 = ρ and m0 = m.
                                                                        L
             For 1 ≤ i ≤ n, <c1(i−1) kc2(i−1) >k <ρi−1 >env <mi−1 >mem −→<c1i kc2i >k <ρi >env <mi >mem ,
             if L = P , there are two ways in which the inference is done.
             Case1: By PAR1 rule,
                                                                    P
                              <c1(i−1)>k <ρi−1>env <mi−1>mem −
                                                             →<c1i>k <ρi>env <mi>mem
                                                                    P
                    <c1(i−1) kc2(i−1)>k <ρi−1>env <mi−1>mem −
                                                            →<c1i k c2(i−1)>k <ρi>env <mi>mem

             Set
                                                                    P
                              <c1(i−1)>k <ρi−1>env <mi−1>mem −
                                                             →<c1i>k <ρi>env <mi>mem
                                                                E
                          <c2(i−1)>k <ρi−1>env <mi−1>mem −
                                                         →<c2(i−1)>k <ρi>env <mi>mem
             Case2: By PAR2 rule,
                                                                    P
                              <c2(i−1)>k <ρi−1>env <mi−1>mem −
                                                             →<c2i>k <ρi>env <mi>mem
                                                                    P
                    <c1(i−1) kc2(i−1)>k <ρi−1>env <mi−1>mem −
                                                            →<c1(i−1) k c2i>k <ρi>env <mi>mem

             Set
                                                                E
                          <c1(i−1)>k <ρi−1>env <mi−1>mem −
                                                         →<c1(i−1)>k <ρi>env <mi>mem
                                                                    P
                              <c2(i−1)>k <ρi−1>env <mi−1>mem −
                                                             →<c2i>k <ρi>env <mi>mem
             If L = E, set
                                                                E
                          <c1(i−1)>k <ρi−1>env <mi−1>mem −
                                                         →<c1(i−1)>k <ρi>env <mi>mem
                                                                E
                          <c2(i−1)>k <ρi−1>env <mi−1>mem −
                                                         →<c2(i−1)>k <ρi>env <mi>mem
       151   Hence, σ can be broken down into two terminable executions σ1 , σ2 , which are executions of
       152   concrete configurations <c1>k <ρ>env <m>mem and <c2>k <ρ>env <m>mem respectively. J
                                                          L n
       153                                      → <c01 >k <ρ0 >env <m0 >mem , then <c1 ; c2 >k <
             I Lemma 4. If <c1 >k <ρ>env <m>mem −
                               L n
       154                → <c01 ; c2>k <ρ0>env <m0>mem , n ∈ Int.
             ρ>env <m>mem −

             Proof. Suppose
                                                    L n
                                                  → <c01>k <ρ0>env <m0>mem , n ∈ Int
                              <c1>k <ρ>env <m>mem −

             If n = 0, then
                                                              L 0
                                     <c1>k <ρ>env <m>mem −
                                                         → <c1>k <ρ>env <m>mem
             Obviously,
                                                              L 0
                                <c1 ; c2>k <ρ>env <m>mem −
                                                         → <c1 ; c2>k <ρ>env <m>mem
             If n 6= 0, we prove by induction on the length of execution path, that is induction on n.

                                           L                            L n−1
                                       →<c001 >k <ρ00>env <m00>mem −
                   <c1>k <ρ>env <m>mem −                           →            <c01>k <ρ0>env <m0>mem
      ShangBei Wang                                                                                   42:7


      By the induction hypothesis of
                                                  L n−1
                       <c001 >k <ρ00>env <m00>mem −
                                                  →         <c01>k <ρ0>env <m0>mem

      we conclude
                                                  L n−1
                    <c001 ; c2>k <ρ00>env <m00>mem −
                                                   →        <c01 ; c2>k <ρ0>env <m0>mem
                                       L
                                  →<c001 >k <ρ00>env <m00>mem is P , then SEQ rule implies
      If L in <c1>k <ρ>env <m>mem −
                                                  L
                                               →<c001 ; c2>k <ρ00>env <m00>mem
                      <c1 ; c2>k <ρ>env <m>mem −
                                       L
                                  →<c001 >k <ρ00>env <m00>mem is E, then c001 = c1 and
      If L in <c1>k <ρ>env <m>mem −
                                                  L
                                               →<c001 ; c2>k <ρ00>env <m00>mem
                      <c1 ; c2>k <ρ>env <m>mem −
                                            L n
155                                   → <c01 ; c2>k <ρ0>env <m0>mem .
      Hence, <c1 ; c2>k <ρ>env <m>mem −                                                          J
                                                        L ∗
156   I Proposition 5. <c1 ; c2 >k <ρ>env <m>mem −   → <·>k <ρ0 >env <m0 >mem for some final
157   configuration < · >k < ρ0 >env < m0 >mem iff there exits some final configuration < · >k <
                                                                   L ∗
158   ρ00 >env < m00 >mem such that < c1 >k < ρ >env < m >mem −
                                                              → < · >k < ρ00 >env < m00 >mem and
                                L ∗
159   <c2>k <ρ00>env <m00>mem −
                              → <·>k <ρ0>env <m0>mem .

      Proof. (⇐)
      If there exit some final configuration <·>k <ρ00>env <m00>mem such that
                                                  L ∗
                                              → <·>k <ρ00>env <m00>mem
                          <c1>k <ρ>env <m>mem −

      and
                                                      L ∗
                         <c2>k <ρ00>env <m00>mem −
                                                 → <·>k <ρ0>env <m0>mem
      Since < · >k < ρ00 >env < m00 >mem is final configuration, there exits n ∈ Int such that
                               L n
      <c1>k <ρ>env <m>mem −    → <·>k <ρ00>env <m00>mem . By Lemma 1, we conclude
                                                   L n
                                                → <c2>k <ρ00>env <m00>mem
                       <c1 ; c2>k <ρ>env <m>mem −
                                            L ∗
                                      → <·>k <ρ0>env <m0>mem .
      Hence, <c1 ; c2>k <ρ>env <m>mem −
      (⇒) Suppose
                                 E ∗                                 P       L ∗
      <c1 ; c2>k <ρ>env <m>mem −
                               → <c1 ; c2>k <ρ1>env <m1>mem −     → <·>k <ρ0>env <m0>mem
                                                            → ··· −

      our goal is to find <·>k <ρ00>env <m00>mem which satisfy the property. we prove by structural
      induction on c1 .
      Case1: c1 ≡ x := e, by SEQ and ASGN1 rules,
                                                  P
                 <x := e; c2>k <ρ1>env <m1>mem −
                                               →<c2>k <ρ1 [ρ1 (e)/x]>env <m1>mem
                                           L ∗
                                       → <·>k <ρ0>env <m0>mem
                                       −
      Set ρ00 = ρ1 [ρ1 (e)/x] and m00 = m1 .
      Case2: c1 ≡ x := A[e], by SEQ and ASGN2 rules,
                                                                         P
                                <x := A[e]; c2>k <ρ1>env <m1>mem −
                                                                 →
42:8   From Matching Logic To Parallel Imperative Language Verification


                                                                         L ∗
                                                                → <·>k <ρ0>env <m0>mem
              <c2>k <ρ1 [m1 (ρ1 (A) +Int ρ1 (e))/x]>env <m1>mem −
       Set ρ00 = ρ1 [m1 (ρ1 (A) +Int ρ1 (e))/x] and m00 = m1 .
       Case3: c1 ≡ A[e1 ] := e2 , by SEQ and ASGN3 rules,
                                                                                P
                                 <A[e1 ] := e2 ; c2>k <ρ1>env <m1>mem −
                                                                      →
                                                                          L ∗
                                                                    → <·>k <ρ0>env <m0>mem
            <c2>k <ρ1>env <m1 [ρ1 (e2 )/(ρ1 (A) +Int ρ1 (e1 ))]>mem −
       Set ρ00 = ρ1 and m00 = m1 [ρ1 (e2 )/(ρ1 (A) +Int ρ1 (e1 ))].
       Case4: c1 ≡ A := Array(e), by SEQ and ARRAY rules,
                                                     P
         <A := Array(e); c2>k <ρ1>env <m1>mem −
                                              →<c2>k <ρ1 [p/A]>env <p 7→ [ρ1 (e)], m1>mem
                                         L ∗
                                        → <·>k <ρ0>env <m0>mem
                                        −
       Set ρ00 = ρ1 [p/A] and m00 = p 7→ [ρ1 (e)], m1 .
       Case5: c1 ≡ if (b) c3 else c4 . If ρ1 (b) is true, then by IF1 and SEQ rules,
                                                               P                       L ∗
              <if (b) c3 else c4 ; c2>k <ρ1>env <m1>mem −
                                                        →<c3 ; c2>k <ρ1>env <m1>mem −
                                                                                    →

                                          <·>k <ρ0>env <m0>mem
       Since c3 is substructure of c1 , by the induction of
                                                          L ∗
                                                    → <·>k <ρ0>env <m0>mem
                         <c3 ; c2>k <ρ1>env <m1>mem −

       there exits some final configuration <·>k <ρ2>env <m2>mem such that
                                                        L ∗
                          <c3>k <ρ1>env <m1>mem −
                                                → <·>k <ρ2>env <m2>mem
                                                         L ∗
                                                 → <·>k <ρ0>env <m0>mem
                           <c2>k <ρ2>env <m2>mem −
       Set ρ00 = ρ2 and m00 = m2 .
       If ρ1 (b) is false, then by IF2 and SEQ rules,
                                                               P                       L ∗
              <if (b) c3 else c4 ; c2>k <ρ1>env <m1>mem −
                                                        →<c4 ; c2>k <ρ1>env <m1>mem −
                                                                                    →

                                          <·>k <ρ0>env <m0>mem
       Since c4 is substructure of c1 , by the induction of
                                                          L ∗
                                                    → <·>k <ρ0>env <m0>mem
                         <c4 ; c2>k <ρ1>env <m1>mem −

       there exits some final configuration <·>k <ρ2>env <m2>mem such that
                                                        L ∗
                          <c4>k <ρ1>env <m1>mem −
                                                → <·>k <ρ2>env <m2>mem
                                                         L ∗
                                                 → <·>k <ρ0>env <m0>mem
                           <c2>k <ρ2>env <m2>mem −
       Set ρ00 = ρ2 and m00 = m2 .
       Case6: c1 ≡ while b do c3 . Since <·>k <ρ0>env <m0>mem is final configuration, there exits
       n ∈ Int such that
                                                                   L n
                                                         → <·>k <ρ0>env <m0>mem
                     <while b do c3 ; c2>k <ρ>env <m>mem −
ShangBei Wang                                                                                   42:9


We prove the property by well-founded induction on n for any ρ and m. If ρ1 (b) is true, by
WHILE1 and SEQ rule,
                                             P
   <while b do c3 ; c2>k <ρ1>env <m1>mem −
                                         →<c3 ; while b do c3 ; c2>k <ρ1>env <m1>mem
                                 L n1
                                 → <·>k <ρ0>env <m0>mem
                                 −
with n1 < n. Since c3 is substructure of c1 , by the induction of
                                                              L n1
                                                      → <·>k <ρ0>env <m0>mem
           <c3 ; while b do c3 ; c2>k <ρ1>env <m1>mem −

there exits some final configuration <·>k <ρ2>env <m2>mem such that
                                                 L ∗
                   <c3>k <ρ1>env <m1>mem −
                                         → <·>k <ρ2>env <m2>mem
                                                             L n2
                                                  → <·>k <ρ0>env <m0>mem
            <while b do c3 ; c2>k <ρ2>env <m2>mem −
with n2 < n. By the inner induction hypothesis (n2 < n), there exits some final configuration
<·>k <ρ3>env <m3>mem such that
                                                        L ∗
              <while b do c3>k <ρ2>env <m2>mem −
                                               → <·>k <ρ3>env <m3>mem
                                                 L ∗
                                          → <·>k <ρ0>env <m0>mem
                    <c2>k <ρ3>env <m3>mem −
Set ρ00 = ρ3 and m00 = m3 .
If ρ1 (b) is false, then by WHILE2 and SEQ rule,
                                         P                           L n1
<while b do c3 ; c2>k <ρ1>env <m1>mem −                      → <·>k <ρ0>env <m0>mem
                                      →<c2>k <ρ1>env <m1>mem −

Set ρ00 = ρ1 and m00 = m1 .
Case7: c1 ≡ await b then cc. <·>k <ρ0 >env <m0 >mem is final configuration, there exits
ρ1 , m1 such that ρ1 (b) is true, then by SEQ and AWAIT rules,
                                                         P                      L ∗
         <await b then cc; c2>k <ρ1>env <m1>mem −
                                                →<c2>k <ρ2>env <m2>mem −
                                                                       →

                                   <·>k <ρ0>env <m0>mem
                                  P ∗
where <cc>k <ρ1>env <m1>mem −      → <·>k <ρ2>env <m2>mem . Set ρ00 = ρ2 and m00 = m2 .
Case8: c1 ≡ c3 ; c4 . Since c3 is substructure of c1 , by the induction of
                                                       L ∗
                                                  → <·>k <ρ0>env <m0>mem
                 <c3 ; (c4 ; c2 )>k <ρ>env <m>mem −

there exits some final configuration <·>k <ρ2>env <m2>mem such that
                                              L ∗
                     <c3>k <ρ>env <m>mem −
                                         → <·>k <ρ2>env <m2>mem
                                                  L ∗
                                             → <·>k <ρ0>env <m0>mem
                  <c4 ; c2>k <ρ2>env <m2>mem −
Since c4 is substructure of c1 , by the induction of
                                                  L ∗
                                             → <·>k <ρ0>env <m0>mem
                  <c4 ; c2>k <ρ2>env <m2>mem −

there exits some final configuration <·>k <ρ3>env <m3>mem such that
                                                 L ∗
                   <c4>k <ρ2>env <m2>mem −
                                         → <·>k <ρ3>env <m3>mem
42:10   From Matching Logic To Parallel Imperative Language Verification


                                                            L ∗
                                                   → <·>k <ρ0>env <m0>mem
                             <c2>k <ρ3>env <m3>mem −
        Set ρ00 = ρ3 and m00 = m3 .
                                                                                              P
        Case9: c1 ≡ c3 k c4 . According to the rule used in <(c3 k c4 ); c2>k <ρ1>env <m1>mem −
                                                                                              → γ,
        there are two cases:
        Case9.1: By SEQ and PAR1 rules,
                                                        P                                          L ∗
                                                  →<(c03 k c4 ); c2>k <ρ2>env <m2>mem −
                <(c3 k c4 ); c2>k <ρ1>env <m1>mem −                                   →

                                              <·>k <ρ0>env <m0>mem
        If c3 6= ((while b do c5 ); c6 ) k c7 , then c03 k c4 is substructure of c1 , by the induction of
                                                                  L ∗
                        <(c03 k c4 ); c2>k <ρ2>env <m2>mem −
                                                           → <·>k <ρ0>env <m0>mem

        there exits some final configuration <·>k <ρ3>env <m3>mem such that
                                                              L ∗
                          <(c03 k c4 )>k <ρ2>env <m2>mem −
                                                         → <·>k <ρ3>env <m3>mem
                                                            L ∗
                                                   → <·>k <ρ0>env <m0>mem
                             <c2>k <ρ3>env <m3>mem −
        Set ρ00 = ρ3 and m00 = m3 .
        If c3 = ((while b do c5 ); c6 ) k c7 , then c03 = ((c5 ; while b do c5 ); c6 ) k c7 and ρ2 = ρ1 and
        m2 = m1 . Since <·>k <ρ0>env <m0>mem is final configuration, there exits <(c3 k c04 ); c2>k <
        ρ3>env <m3>mem such that c04 is substructure of c4 and
                                                        L ∗                                        L ∗
                <(c03 k c4 ); c2>k <ρ2>env <m2>mem −
                                                   → <(c3 k c04 ); c2>k <ρ3>env <m3>mem −
                                                                                        →

                                              <·>k <ρ0>env <m0>mem
        By the induction of
                                                                  L ∗
                        <(c3 k c04 ); c2>k <ρ3>env <m3>mem −
                                                           → <·>k <ρ0>env <m0>mem

        there exits some final configuration <·>k <ρ4>env <m4>mem such that
                                                              L ∗
                          <(c3 k c04 )>k <ρ3>env <m3>mem −
                                                         → <·>k <ρ4>env <m4>mem
                                                            L ∗
                                                   → <·>k <ρ0>env <m0>mem
                             <c2>k <ρ4>env <m4>mem −
        Set ρ00 = ρ4 and m00 = m4 .
        Case9.2: By SEQ and PAR2 rules,
                                                        P                                          L ∗
                                                  →<(c3 k c04 ); c2>k <ρ2>env <m2>mem −
                <(c3 k c4 ); c2>k <ρ1>env <m1>mem −                                   →

                                              <·>k <ρ0>env <m0>mem
        If c4 6= ((while b do c5 ); c6 ) k c7 , then c3 k c04 is substructure of c1 , by the induction of
                                                                  L ∗
                        <(c3 k c04 ); c2>k <ρ2>env <m2>mem −
                                                           → <·>k <ρ0>env <m0>mem

        there exits some final configuration <·>k <ρ3>env <m3>mem such that
                                                              L ∗
                          <(c3 k c04 )>k <ρ2>env <m2>mem −
                                                         → <·>k <ρ3>env <m3>mem
      ShangBei Wang                                                                                         42:11


                                                       L ∗
                                                 → <·>k <ρ0>env <m0>mem
                           <c2>k <ρ3>env <m3>mem −
      Set ρ00 = ρ3 and m00 = m3 .
      If c4 = ((while b do c5 ); c6 ) k c7 , then c04 = ((c5 ; while b do c5 ); c6 ) k c7 and ρ2 = ρ1 and
      m2 = m1 . Since <·>k <ρ0>env <m0>mem is final configuration, there exits <(c03 k c4 ); c2>k <
      ρ3>env <m3>mem such that c03 is substructure of c3 and
                                                    L ∗                                      L ∗
             <(c3 k c04 ); c2>k <ρ2>env <m2>mem −
                                                → <(c03 k c4 ); c2>k <ρ3>env <m3>mem −
                                                                                     →

                                          <·>k <ρ0>env <m0>mem
      By the induction of
                                                             L ∗
                      <(c03 k c4 ); c2>k <ρ3>env <m3>mem −
                                                         → <·>k <ρ0>env <m0>mem

      there exits some final configuration <·>k <ρ4>env <m4>mem such that
                                                          L ∗
                       <(c3 k c04 )>k <ρ3>env <m3>mem −
                                                      → <·>k <ρ4>env <m4>mem
                                                       L ∗
                                                 → <·>k <ρ0>env <m0>mem
                           <c2>k <ρ4>env <m4>mem −
      Set ρ00 = ρ4 and m00 = m4 .
      Case10: c1 ≡ skip, by SEQ and SKIP rules
                                          P                            L ∗
           <skip; c2>k <ρ>env <m>mem −                    → <·>k <ρ0>env <m0>mem
                                     →<c2>k <ρ>env <m>mem −

160   Set ρ00 = ρ and m00 = m.                                                                         J

161    3      Matching logic for PIMP
162   In matching logic, one can’t quantify program variables because they are syntactic constants
163   rather than logical variables. Suppose SVar is an infinite set of logical or semantic variables,
164   and it also contain a special variable named "o" of sort Cfg which serves as a place holder in
165   the matching logic pattern.

166   I Definition 6. [19]Matching logic patterns, are FOL= forumlae ∃X((o = c) ∧ ϕ), where:
167   X ⊂ SVar is the set of bound variables; c is the pattern structure and is a term of sort Cfg;
168   ϕ is the constraint, an arbitrary FOL= formula.

      Let T is the initial model of PIMP and SVar o = SVar ∪ {o}. Valuation (γ, τ ) : SVar o → T
      includes a concrete configuration γ and a map τ : SVar → T . (γ, τ ) |= ∃X((o = c) ∧ ϕ)
      iff there exists θτ : SVar → T with θτ SVar/X = τ SVar/X such that γ = θτ (c) and
      θτ |= ϕ. Let Γ, Γ0 are matching logic patterns, Γ ⇓ Γ0 is called matching logic correctness
      pair. Informally matching logic correctness pair ∃X(o =< c >k < ρ >env < m >mem ∧ϕ) ⇓
      ∃X(o =< · >k < ρ0 >env < m0 >mem ∧ϕ0 ) means: for any valuation (γ, τ ) : SVar o → T , if
      (γ, τ ) |= ∃X(o =<c>k <ρ>env <m>mem ∧ϕ) before execution of γ, then (γ 0 , τ ) |= ∃X(o =<
      · >k < ρ0 >env < m0 >mem ∧ϕ0 ) after execution of γ, where PIMP |= γ →∗ γ 0 and γ 0 is a
      final configuration. We introduce syntax shorthand notations for configuration pattern and
      correctness pair:
                                <c>k <ρ>env <m>mem <X>bnd <ϕ>f orm
      instead of
                                   ∃X((o =<c>k <ρ>env <m>mem ) ∧ ϕ)
42:12   From Matching Logic To Parallel Imperative Language Verification



         Matching logic proof system of PIMP

         M-SKIP:
                                       ·
         ∃X(o =<skip>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ)

         M-ASGN1:
                                            ·
         ∃X(o =<x := e>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ[ρ(e)/x]>env <m>mem ∧ϕ)

         M-ASGN2:
                                                   ·
         ∃X(o =<x := A[e]>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ[m(ρ(A)+Int ρ(e))/x]>env <m>mem ∧ϕ)

         M-ASGN3:
                                                       ·
         ∃X(o =<A[e1 ] := e2>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ>env <m[ρ(e2 )/(ρ(A)+Int ρ(e1 ))]>mem ∧ϕ)

         M-ARRAY:
                                                    ·
         ∃X(o =<A :=Array(e)>k <ρ>env<m>mem ∧ϕ)⇓ ∃(X ∪{p})(o =<·>k<ρ[p/A]>env<p 7→ [ρ(e)], m>mem ∧ϕ)

         M-SEQ:
          ∃X1 (o =<c1>k <ρ1>env <m1>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ2>env <m2>mem ∧ϕ2 )
          ∃X2 (o =<c2>k <ρ2>env <m2>mem ∧ϕ2 ) ⇓ ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 )
         ∃X1 (o =<c1 ; c2>k <ρ1>env <m1>mem ∧ϕ1 ) ⇓ ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 )

         M-IF:
         ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
         ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is f alse)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
           ∃X1 (o =<if (b)c1 else c2>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

         M-CONS:
         |= Γ ⇒ Γ1 , Γ1 ⇓ Γ01 , |= Γ01 ⇒ Γ0
                      Γ ⇓ Γ0

         M-CASE:
         |= Γ ⇒ Γ1 ∨ Γ2 , Γ1 ⇓ Γ0 , Γ2 ⇓ Γ0
                     Γ ⇓ Γ0

         M-AWAIT:
         ∃X1 (o =<cc>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
          ∃X1 (o =<await b then cc>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

         M-WHILE:
              ∃X(o =<c>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is true)) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ)
         ∃X(o =<while b do c>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is f alse))

         M-PAR:
         ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 )
         ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ2 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ02 )
         c1 , c2 are interference-free
         ∃X1 (o =<c1 k c2>k <ρ>env <m>mem ∧ϕ1 ∧ ϕ2 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 ∧ ϕ02 )



          Figure 3 Matching logic proof system of PIMP
      ShangBei Wang                                                                                       42:13


      and

              <ρ>env <m>mem <X>bnd <ϕ>f orm c <ρ0>env <m0>mem <X 0>bnd <ϕ0>f orm

      instead of

               ∃X(o =<c>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X 0 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

169   we call <ρ>env <m>mem <X >bnd <ϕ>f orm and <ρ0 >env <m0 >mem <X 0 >bnd <ϕ0 >f orm
170   assertions. Figure 3 gives the matching logic proof system for PIMP. Notice that M-PAR
171   rule in Figure 3 says that as long as c1 , c2 don’t interfere with each other, the effect of
172   executing c1 and c2 in parallel is the same as executing c1 and c2 separately. The easiest
173   way to get "interference-free" is not to allow shared variables, but this is too restrictive to
174   handle the synchronization of producer and consumer which is a standard problem in parallel
175   programming literature.
176   Suppose <ρ1>env <m1>mem <X1>bnd <ϕ1>f orm c1 <ρ01>env <m01>mem <X10 >bnd <ϕ01>f orm
177   , set pre(c1 ) =<ρ1>env <m1>mem <X1>bnd <ϕ1>f orm and post(c1 ) =<ρ01>env <m01>mem <
178   X10 >bnd <ϕ01>f orm , we now define "interference-free".

179   I Definition 7. Given a proof outline of pre(c1 ) c1 post(c1 ) and a computation k with
180   pre(k) k post(k), we say that k don’t interfere with c1 if the following two conditions hold:
181   1. For any concrete configuration γ, if (γ, τ ) |=<k>k pre(k) and (γ, τ ) |=<k>k post(c1 ) and
182      γ →∗ γ 0 and γ 0 is a final configuration, then (γ 0 , τ ) |=<·>k post(c1 );
183   2. Let c01 is any sub computation within c1 but not within any await, for any concrete
184      configuration γ, if (γ, τ ) |=<k>k pre(k) and (γ, τ ) |=<k>k pre(c01 ) and γ →∗ γ 0 and γ 0 is
185      a final configuration, then (γ 0 , τ ) |=<·>k pre(c01 ).

186   I Definition 8. Given proof outlines of pre(c1 ) c1 post(c1 ) and pre(c2 ) c2 post(c2 ), we say
187   that c1 , c2 are "interference-free" if the following two conditions hold:
188    1. Let c01 be an await or := sub computation (which don’t appear in an await) of c1 , then c01
189       don’t interfere with c2 ;
190    2. Let c02 be an await or := sub computation (which don’t appear in an await) of c2 , then c02
191       don’t interfere with c1 .

192   I Definition 9. Given a proof outline of pre(c) c post(c) and any concrete configura-
193   tion γ0 with (γ0 , τ ) |=< c >k pre(c), there are infinite number of terminable executions
                 L       L       L      L         L        L
194   σ = γ0 −   → γ1 −  → ··· − → γi − → γi+1 −  → ··· − → γn because of ENV rule. For any
          L
195   γi −→ γi+1 , 0 ≤ i < n, if L = E, it means other computation c0 which is in parallel
196   with c updates environment and memory. Let S represents a set of computations executed in
197   parallel with c. A terminable execution σ is called actual execution if c0 , c are "interference-
198   free" for any c0 ∈ S.
199

200   We now formally give the proof that matching logic is soundness to the operational semantics
201   of PIMP. Let’s make the assumption that the original PIMP program don’t contain variables
202   in SVar.
                                                            L      L      L     L        L      L
203   I Theorem 10. For any actual execution σ = γ0 −            → γ1 − → ··· −
                                                                              → γi −
                                                                                   → γi+1 −
                                                                                          → ··· −
                                                                                                → γn ,
204   if (γ0 , τ ) |= Γ and Γ ⇓ Γ0 is derivable, then (γn , τ ) |= Γ0 .

      Proof. We prove by the induction on the depth of inference of Γ ⇓ Γ0 . We consider the
      different ways in which the last step of the inference is done:
42:14   From Matching Logic To Parallel Imperative Language Verification


        Case1: By M-ASGN1 rule
                                               ·
            ∃X(o =<x := e>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ[ρ(e)/x]>env <m>mem ∧ϕ)
        Γ ≡ ∃X(o =<x := e>k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X(o =<·>k <ρ[ρ(e)/x]>env <
        m>mem ∧ϕ). Suppose there exists θτ : SVar → T with θτ SVar/X = τ SVar/X such that
        γ0 =<x := e>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                           L       L       L       L       L       L
                 <x := e>k <θτ (ρ)>env <θτ (m)>mem −
                                                   → γ1 −
                                                        → ··· −
                                                              → γi −
                                                                   → γi+1 −
                                                                          → ··· −
                                                                                → γn
                                                   P
        If <x := e>k <θτ (ρ)>env <θτ (m)>mem −
                                             → γ1 , by ASGN1 rule,

                                 γ1 =<·>k <θτ (ρ)[θτ (ρ)(e)/x]>env <θτ (m)>mem

        and
                                                                   E       E       E       E       E
                 <·>k <θτ (ρ)[θτ (ρ)(e)/x]>env <θτ (m)>mem −
                                                           → ··· −
                                                                 → γi −
                                                                      → γi+1 −
                                                                             → ··· −
                                                                                   → γn

        Due to θτ |= ϕ, (γ1 , τ ) |= Γ0 . Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 ,
                                                                   E
        2 ≤ i ≤ n. If <x := e>k <θτ (ρ)>env <θτ (m)>mem −          → γ1 , since σ is an actual execution,
                                                                       E      E      P         E        E
        (γ1 , τ ) |= Γ and there exits j (1 < j ≤ n − 1) such that γ1 −→ ··· −→ γj − → γj+1 −  → ··· −  → γn
        with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1SVar/X = τSVar/X
        such that γj =<x := e>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. By ASGN1 rule, we
        conclude γj+1 =<·>k <θτ1 (ρj )[θτ1 (ρj )(e)/x]>env <θτ1 (mj )>mem . Due to θτ1 |= ϕ, (γj+1 , τ ) |= Γ0 .
        Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 , j + 1 ≤ i ≤ n.
        Case2: By M-ASGN2 rule
                                                  ·
        ∃X(o =<x :=A[e]>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ[m(ρ(A)+Int ρ(e))/x]>env <m>mem∧ϕ)
        Γ ≡ ∃X(o =<x := A[e]>k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X(o =<·>k <ρ[m(ρ(A) +Int
        ρ(e))/x]>env <m>mem ∧ϕ). Suppose there exists θτ : SVar → T with θτ SVar/X = τSVar/X
        such that γ0 =<x := A[e]>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                               L       L       L       L       L       L
               <x := A[e]>k <θτ (ρ)>env <θτ (m)>mem −
                                                    → γ1 −
                                                         → ··· −
                                                               → γi −
                                                                    → γi+1 −
                                                                           → ··· −
                                                                                 → γn
                                                       P
        If <x := A[e]>k <θτ (ρ)>env <θτ (m)>mem −
                                                → γ1 , by ASGN2 rule,

                     γ1 =<·>k <θτ (ρ)[θτ (m)(θτ (ρ)(A) +Int θτ (ρ)(e))/x]>env <θτ (m)>mem

        and
                                                                                           E       E
                <·>k <θτ (ρ)[θτ (m)(θτ (ρ)(A) +Int θτ (ρ)(e))/x]>env <θτ (m)>mem −
                                                                                 → ··· −
                                                                                       → γn

        Due to θτ |= ϕ, (γ1 , τ ) |= Γ0 . Since σ is actual execution, we conclude (γi , τ ) |= Γ0 , 2 ≤ i ≤ n.
                                                       E
        If <x := A[e]>k <θτ (ρ)>env <θτ (m)>mem −      → γ1 , since σ is actual execution, (γ1 , τ ) |= Γ and
        there exits j (1 < j ≤ n − 1) such that
                                          E       E        P           E       E
                                      γ1 −
                                         → ··· −
                                               → γj −
                                                    → γj+1 −
                                                           → ··· −
                                                                 → γn

        with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1SVar/X = τSVar/X
        such that γj =<x := A[e]>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. By ASGN2 rule, we
        conclude

                 γj+1 =<·>k <θτ1 (ρj )[θτ1 (mj )(θτ1 (ρj )(A) +Int θτ1 (ρj )(e))/x]>env <θτ1 (mj )>mem
ShangBei Wang                                                                                                  42:15


Due to θτ1 |= ϕ, (γj+1 , τ ) |= Γ0 . Since σ is actual execution, we conclude (γi , τ ) |= Γ0 ,
j + 1 ≤ i ≤ n.
Case3: By M-ASGN3 rule
                                           ·
∃X(o=<A[e1] := e2>k <ρ>env <m>mem∧ϕ) ⇓ ∃X(o=<·>k <ρ>env <m[ρ(e2)/(ρ(A)+Int ρ(e1))]>mem∧ϕ)

Γ ≡ ∃X(o =< A[e1 ] := e2 >k < ρ >env < m >mem ∧ϕ) and Γ0 ≡ ∃X(o =< · >k < ρ >env <
m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem ∧ϕ). Suppose there exists θτ : SVar → T with θτ SVar/X =
τSVar/X such that γ0 =<A[e1 ] := e2>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                       L       L       L       L           L       L
       <A[e1 ] := e2>k <θτ (ρ)>env <θτ (m)>mem −
                                               → γ1 −
                                                    → ··· −
                                                          → γi −
                                                               → γi+1 −
                                                                      → ··· −
                                                                            → γn
                                                  P
If <A[e1 ] := e2>k <θτ (ρ)>env <θτ (m)>mem −
                                           → γ1 , by ASGN3 rule,

            γ1 =<·>k <θτ (ρ)>env <θτ (m)[θτ (ρ)(e2 )/(θτ (ρ)(A) +Int θτ (ρ)(e1 ))]>mem

and
                                                                                           E       E
       <·>k <θτ (ρ)>env <θτ (m)[θτ (ρ)(e2 )/(θτ (ρ)(A) +Int θτ (ρ)(e1 ))]>mem −
                                                                              → ··· −
                                                                                    → γn

Due to θτ |= ϕ, (γ1 , τ ) |= Γ0 . Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 ,
                                                          E
2 ≤ i ≤ n. If <A[e1 ] := e2>k <θτ (ρ)>env <θτ (m)>mem −   → γ1 , since σ is an actual execution,
(γ1 , τ ) |= Γ and there exits j (1 < j ≤ n − 1) such that
                                   E       E       P           E       E
                               γ1 −
                                  → ··· −
                                        → γj −
                                             → γj+1 −
                                                    → ··· −
                                                          → γn

with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1SVar/X = τSVar/X
such that γj =<A[e1 ] := e2>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. By ASGN3 rule, we
conclude

        γj+1 =<·>k <θτ1 (ρj )>env <θτ1 (mj )[θτ1 (ρj )(e2 )/(θτ1 (ρj )(A) +Int θτ1 (ρj )(e1 ))]>mem

Due to θτ1 |= ϕ, (γj+1 , τ ) |= Γ0 . Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 ,
j + 1 ≤ i ≤ n.
Case4: By M-ARRAY rule
                                            ·
∃X(o=<A:=Array(e)>k <ρ>env <m>mem ∧ϕ) ⇓ ∃(X ∪{p})(o=<·>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem∧ϕ)

Γ ≡ ∃X(o =< A := Array(e) >k < ρ >env < m >mem ∧ϕ) and Γ0 ≡ ∃(X ∪ {p})(o =<
· >k < ρ[p/A] >env < p 7→ [ρ(e)], m >mem ∧ϕ). Suppose there exists θτ : SVar → T with
θτ SVar/X = τ SVar/X such that γ0 =< A := Array(e) >k < θτ (ρ) >env < θτ (m) >mem and
θτ |= ϕ and
                                                           L       L       L       L           L       L
      <A := Array(e)>k <θτ (ρ)>env <θτ (m)>mem −
                                               → γ1 −
                                                    → ··· −
                                                          → γi −
                                                               → γi+1 −
                                                                      → ··· −
                                                                            → γn
                                                       P
If <A := Array(e)>k <θτ (ρ)>env <θτ (m)>mem −
                                            → γ1 , by ARRAY rule,

                 γ1 =<·>k <θτ (ρ)[θτ (p)/A]>env <θτ (p) 7→ [θτ (ρ)(e)], θτ (m)>mem

and
                                                                       E       E       E           E       E
<·>k <θτ (ρ)[θτ (p)/A]>env <θτ (p) 7→ [θτ (ρ)(e)], θτ (m)>mem −
                                                              → ··· −
                                                                    → γi −
                                                                         → γi+1 −
                                                                                → ··· −
                                                                                      → γn
42:16     From Matching Logic To Parallel Imperative Language Verification


          Set θτ1 SVar/(X∪{p}) = τ SVar/(X∪{p}) and θτ1 X = θτ X and θτ1 p = τ p . Due to θτ |= ϕ,
          θτ1 |= ϕ and (γ1 , τ ) |= Γ0 . Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 , 2 ≤ i ≤ n.
                                                                    E
          If < A := Array(e) >k < θτ (ρ) >env < θτ (m) >mem −       → γ1 , since σ is an actual execution,
          (γ1 , τ ) |= Γ and there exits j (1 < j ≤ n − 1) such that

                                            E       E      P          E         E
                                        γ1 −
                                           → ··· −
                                                 → γj −
                                                      → γj+1 −
                                                             → ··· −
                                                                   → γn

          with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ2 : SVar → T with θτ2SVar/X = τSVar/X
          such that γj =<A := Array(e)>k <θτ2 (ρj )>env <θτ2 (mj )>mem and θτ2 |= ϕ. By ARRAY rule,
          we conclude

                       γj+1 =<·>k <θτ2 (ρj )[θτ2 (p)/A]>env <θτ2 (p) 7→ [θτ2 (ρj )(e)], θτ2 (mj )>mem

    205   Set θτ3SVar/(X∪{p}) = τSVar/(X∪{p}) and θτ3X = θτ2X and θτ3p = τp . Due to θτ2 |= ϕ, θτ3 |= ϕ
    206   and (γj+1 , τ ) |= Γ0 . Since σ is an actual execution, we conclude (γi , τ ) |= Γ0 , j + 1 ≤ i ≤ n.
    207   Case5: By M-SEQ rule

    208       ∃X1 (o =<c1>k <ρ1>env <m1>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ2>env <m2>mem ∧ϕ2 )
    209       ∃X2 (o =<c2>k <ρ2>env <m2>mem ∧ϕ2 ) ⇓ ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 )
    210
    211
              ∃X1 (o =<c1 ; c2>k <ρ1>env <m1>mem ∧ϕ1 ) ⇓ ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 )

          Γ ≡ ∃X1 (o =< c1 ; c2 >k < ρ1 >env < m1 >mem ∧ϕ1 ) and Γ0 ≡ ∃X3 (o =< · >k < ρ3 >env <
          m3>mem ∧ϕ3 ). Suppose there exists θτ : SVar → T with θτ SVar/X1 = τSVar/X1 such that
          γ0 =<c1 ; c2>k <θτ (ρ1 )>env <θτ (m1 )>mem and θτ |= ϕ1 and

                                                           L      L        L        L     L       L
                    <c1 ; c2>k <θτ (ρ)>env <θτ (m)>mem −
                                                       → γ1 −
                                                            → ··· −
                                                                  → γi −
                                                                       → γi+1 −
                                                                              → ··· −
                                                                                    → γn

          Proposition 5 implies there exits some final configuration <·>k <ρ0>env <m0>mem such that

                                                                  L ∗
                                                             → <·>k <ρ0>env <m0>mem
                           <c1>k <θτ (ρ1 )>env <θτ (m1 )>mem −

          and
                                                                          L ∗
                                           <c2>k <ρ0>env <m0>mem −
                                                                 → γn

          By the induction hypothesis of

                ∃X1 (o =<c1>k <ρ1>env <m1>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ2>env <m2>mem ∧ϕ2 )

          we conclude (<·>k <ρ0>env <m0>mem , τ ) |= ∃X2 (o =<·>k <ρ2>env <m2>mem ∧ϕ2 ). Since c2
          is ground, (<c2>k <ρ0>env <m0>mem , τ ) |= ∃X2 (o =<c2>k <ρ2>env <m2>mem ∧ϕ2 ). By the
          induction hypothesis of

                ∃X2 (o =<c2>k <ρ2>env <m2>mem ∧ϕ2 ) ⇓ ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 )

    212   we conclude (γn , τ ) |= ∃X3 (o =<·>k <ρ3>env <m3>mem ∧ϕ3 ).
    213   Case6: By M-IF rule

    214       ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
    215       ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is f alse)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
    217
    216       ∃X1 (o =<if (b)c1 else c2>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
ShangBei Wang                                                                                        42:17


Γ ≡ ∃X1 (o =<if (b)c1 else c2 >k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X2 (o =<·>k <ρ0 >env <
m0>mem ∧ϕ0 ). Suppose there exists θτ : SVar → T with θτ SVar/X1 = τSVar/X1 such that
γ0 =<if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                      L       L       L   L     L      L
    <if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem −
                                                → γ1 −
                                                     → ··· −
                                                           → γi −
                                                                → γi+1 −
                                                                       → ··· −
                                                                             → γn
                                                  P
If <if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem −
                                               → γ1 , we distinguish two cases according to
whether θτ (ρ)(b) is true or not.
Case6.1: θτ (ρ)(b) is true; by IF1 rule,
                                                  P                                    L ∗
   <if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem −
                                               →<c1>k <θτ (ρ)>env <θτ (m)>mem −
                                                                              → γn

By the induction hypothesis of

  ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

we conclude (γn , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 ).
Case6.2: θτ (ρ)(b) is false; by IF2 rule,
                                                  P                                    L ∗
   <if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem −
                                               →<c2>k <θτ (ρ)>env <θτ (m)>mem −
                                                                              → γn

By the induction hypothesis of

 ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is f alse)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

we conclude (γn , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 ).
                                               E
If <if (b)c1 else c2>k <θτ (ρ)>env <θτ (m)>mem −
                                               → γ1 , since σ is an actual execution, (γ1 , τ ) |=
Γ and there exits j (1 < j ≤ n − 1) such that
                                E      E      P           E       E
                            γ1 −
                               → ··· −
                                     → γj −
                                          → γj+1 −
                                                 → ··· −
                                                       → γn

with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1SVar/X1 = τSVar/X1
such that γj =<if (b)c1 else c2>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. We also distinguish
two cases according to whether θτ1 (ρj )(b) is true or not.
Case6.3: θτ1 (ρj )(b) is true; by IF1 rule,
                                                  P                                        L ∗
 <if (b)c1 else c2>k <θτ1 (ρj )>env <θτ1 (mj )>mem −
                                                   →<c1>k <θτ1 (ρj )>env <θτ1 (mj )>mem −
                                                                                        → γn

Since if (b)c1 else c2 is ground,

(<c1>k <θτ1 (ρj )>env <θτ1 (mj )>mem , τ ) |= ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true))

By the induction hypothesis of

  ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

we conclude (γn , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 ).
Case6.4: θτ1 (ρj )(b) is false; by IF2 rule,
                                                  P                                        L ∗
 <if (b)c1 else c2>k <θτ1 (ρj )>env <θτ1 (mj )>mem −
                                                   →<c2>k <θτ1 (ρj )>env <θτ1 (mj )>mem −
                                                                                        → γn

Since if (b)c1 else c2 is ground,

 (<c2>k <θτ1 (ρj )>env <θτ1 (mj )>mem , τ ) |= ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is f alse))
42:18   From Matching Logic To Parallel Imperative Language Verification


        By the induction hypothesis of

          ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is f alse)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

        we conclude (γn , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 ).
        Case7: By M-CONS rule

                                           |= Γ ⇒ Γ1 , Γ1 ⇓ Γ01 , |= Γ01 ⇒ Γ0
                                                        Γ ⇓ Γ0
                                           L       L       L       L           L       L
        Suppose (γ0 , τ ) |= Γ and γ0 − → γ1 −→ ··· −→ γi −→ γi+1 −  → ··· −→ γn . Due to |= Γ ⇒ Γ1 ,
        (γ0 , τ ) |= Γ1 . By the induction hypothesis of Γ1 ⇓ Γ01 , we conclude (γn , τ ) |= Γ01 . Due to
        |= Γ01 ⇒ Γ0 , (γn , τ ) |= Γ0 .
        Case8: By M-CASE rule

                                           |= Γ ⇒ Γ1 ∨ Γ2 , Γ1 ⇓ Γ0 , Γ2 ⇓ Γ0
                                                       Γ ⇓ Γ0
                                       L       L       L       L           L       L
        Suppose (γ0 , τ ) |= Γ and γ0 −     → γ1 −→ ··· −  → γi − → γi+1 −→ ··· −
                                                                                → γn . Due to |= Γ ⇒ Γ1 ∨ Γ2 ,
        (γ0 , τ ) |= Γ1 or (γ0 , τ ) |= Γ2 . If (γ0 , τ ) |= Γ1 , by the induction hypothesis of Γ1 ⇓ Γ0 , we
        conclude (γn , τ ) |= Γ0 . If (γ0 , τ ) |= Γ2 , by the induction hypothesis of Γ2 ⇓ Γ0 , we conclude
        (γn , τ ) |= Γ0 . Thus, (γn , τ ) |= Γ0 .
        Case9: By M-AWAIT rule

          ∃X1 (o =<cc>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
           ∃X1 (o =<await b then cc>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

        Γ ≡ ∃X1 (o =<await b then cc>k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X2 (o =<·>k <ρ0 >env <
        m0>mem ∧ϕ0 ). Suppose there exists θτ : SVar → T with θτ SVar/X1 = τSVar/X1 such that
        γ0 =<await b then cc>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                                   L       L       L       L   L     L
            <await b then cc>k <θτ (ρ)>env <θτ (m)>mem −
                                                       → γ1 −
                                                            → ··· −
                                                                  → γi −
                                                                       → γi+1 −
                                                                              → ··· −
                                                                                    → γn
                                                               P
        If <await b then cc>k <θτ (ρ)>env <θτ (m)>mem −
                                                      → γ1 , by AWAIT rule, we conclude γ1 is a
                                                                                               L ∗
        final configuration and θτ (ρ)(b) is true and <cc>k <θτ (ρ)>env <θτ (m)>mem −
                                                                                    → γ1 . By the
        induction hypothesis of

          ∃X1 (o =<cc>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )

        we conclude (γ1 , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 ). Since σ is an actual execution,
        (γi , τ ) |= Γ0 , 2 ≤ i ≤ n.
                                                        E
        If <await b then cc>k <θτ (ρ)>env <θτ (m)>mem − → γ1 , since σ is an actual execution, there
        exits j (1 < j ≤ n − 1) such that
                                           E       E       P           E       E
                                      γ1 −
                                         → ··· −
                                               → γj −
                                                    → γj+1 −
                                                           → ··· −
                                                                 → γn

        with (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1SVar/X1 = τSVar/X1
        such that γj =<await b then cc>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. By AWAIT rule,
        we conclude γj+1 is a final configuration and θτ1 (ρj )(b) is true and <cc>k <θτ1 (ρj )>env <
                       L ∗
        θτ1 (mj )>mem −
                      → γj+1 . By the induction hypothesis of

        ∃X1 (o =<cc>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ0 )
ShangBei Wang                                                                                       42:19


we conclude (γj+1 , τ ) |= ∃X2 (o =< · >k < ρ0 >env < m0 >mem ∧ϕ0 ). Since σ is an actual
execution, (γi , τ ) |= Γ0 , j + 1 ≤ i ≤ n.
Case10: By M-WHILE rule
     ∃X(o =<c>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is true)) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ)
∃X(o =<while b do c>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ∧(ρ(b) is f alse))

Γ ≡ ∃X(o =<while b do c>k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X(o =<·>k <ρ>env <m>mem
∧ϕ ∧ (ρ(b) is f alse)). Suppose there exists θτ : SVar → T with θτ SVar/X = τSVar/X such
that γ0 =<while b do c>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                                 L n
                      <while b do c>k <θτ (ρ)>env <θτ (m)>mem −
                                                              → γn

We prove by well-founded induction on n that

               (γn , τ ) |= ∃X(o =<·>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is f alse))

There exit n1 , n2 such that
                                          E n1                                    P     L n2
                                        → <while b do c>k <ρ0>env <m0>mem −
<while b do c>k <θτ (ρ)>env <θτ (m)>mem −                                 → γ0 −
                                                                               →               γn

with n1 + n2 + 1 = n.
If ρ0 (b) is true, by WHILE1 rule, γ 0 =<c; while b do c>k <ρ0>env <m0>mem and
                                                               L n2
                        <c; while b do c>k <ρ0>env <m0>mem −
                                                           →          γn

Proposition 5 implies there exits some final configuration <·>k <ρ00>env <m00>mem such that
                                             L ∗
                    <c>k <ρ0>env <m0>mem −
                                         → <·>k <ρ00>env <m00>mem

and
                                                              L n3
                        <while b do c>k <ρ00>env <m00>mem −
                                                          →           γn
with n3 < n2 . Since σ is an actual execution, (<while b do c>k <ρ0>env <m0>mem , τ ) |= Γ.
Since while b do c is ground and ρ0 (b) is true,

      (<c>k <ρ0>env <m0>mem , τ ) |= ∃X(o =<c>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is true))

By the induction hypothesis of

 ∃X(o =<c>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is true)) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ)

we conclude (<·>k <ρ00 >env <m00 >mem , τ ) |= ∃X(o =<·>k <ρ>env <m>mem ∧ϕ). Since
while b do c is ground,

 (<while b do c>k <ρ00>env <m00>mem , τ ) |= ∃X(o =<while b do c>k <ρ>env <m>mem ∧ϕ)

By the inner induction hypothesis (n3 < n), we conclude

               (γn , τ ) |= ∃X(o =<·>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is f alse))

If ρ0 (b) is false, by WHILE2 rule, γ 0 =<·>k <ρ0>env <m0>mem . Since σ is an actual execution,
(<while b do c>k <ρ0>env <m0>mem , τ ) |= Γ. Since while b do c is ground and ρ0 (b) is false,

      (<·>k <ρ0>env <m0>mem , τ ) |= ∃X(o =<·>k <ρ>env <m>mem ∧ϕ ∧ (ρ(b) is f alse))
42:20     From Matching Logic To Parallel Imperative Language Verification


    218   Since σ is an actual execution, (γn , τ ) |= Γ0 .
    219   Case11: By M-PAR rule

    220      ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 )
    221      ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ2 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ02 )
    222
    223
             ∃X1 (o =<c1 k c2>k <ρ>env <m>mem ∧ϕ1 ∧ϕ2 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 ∧ϕ02 )

          where c1 , c2 are interference-free. Γ ≡ ∃X1 (o =<c1 k c2>k <ρ>env <m>mem ∧ϕ1 ∧ ϕ2 ) and
          Γ0 ≡ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 ∧ ϕ02 ). Suppose there exists θτ : SVar → T with
          θτ SVar/X1 = τSVar/X1 such that γ0 =<c1 k c2>k <θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ1 ∧ ϕ2
          and
                                                              L       L       L           L   L       L
                     <c1 k c2>k <θτ (ρ)>env <θτ (m)>mem −
                                                        → γ1 −
                                                             → ··· −
                                                                   → γi −
                                                                        → γi+1 −
                                                                               → ··· −
                                                                                     → γn

          Set γi =<c1i k c2i>k <ρi>env <mi>mem , 0 ≤ i ≤ n and c10 = c1 and c20 = c2 and ρ0 = θτ (ρ)
          and m0 = θτ (m). Proposition 3 implies
                                            L   L      L          L       L           L
                                       γ0 −
                                          → γ1 −
                                               → ··· −
                                                     → γi −
                                                          → γi+1 −
                                                                 → ··· −
                                                                       → γn

          can be broken down into two terminable executions
                                        L       L     L           L           L           L
                                   γ10 −
                                       → γ11 −
                                             → ··· −
                                                   → γ1i −
                                                         → γ1(i+1) −
                                                                   → ··· −
                                                                         → γ1n

          and
                                        L       L     L           L           L           L
                                   γ20 −
                                       → γ21 −
                                             → ··· −
                                                   → γ2i −
                                                         → γ2(i+1) −
                                                                   → ··· −
                                                                         → γ2n
    224   where γ1i =<c1i>k <ρi>env <mi>mem and γ2i =<c2i>k <ρi>env <mi>mem , 0 ≤ i < n.
                               L        L       L      L              L           L               L       L   L
    225   B Claim 11.      γ10 −
                               → γ11 −
                                     → ··· −
                                           → γ1i −
                                                 → γ1(i+1) −
                                                           → ··· −
                                                                 → γ1n and γ20 −
                                                                               → γ21 −
                                                                                     → ··· −
                                                                                           →
                L          L       L
    226   γ2i −
              → γ2(i+1) −
                        → ··· −
                              → γ2n are actual executions.

    227   Proof. First, since σ is an actual execution and c1 is substructure of c1 k c2 , c0 , c1 are
    228   "interference-free" where c0 ∈ S and S represents a set of computations executed in parallel
                                                                                  L     L     L     L
    229   with c1 k c2 . Second, c1 , c2 are also "interference-free". Thus, γ10 −→ γ11 −
                                                                                        → ··· −
                                                                                              → γ1i −
                                                                                                    →
                 L       L                                              L       L     L     L       L
    230   γ1i+1 −→ ··· −→ γ1n is an actual execution. Similarly, γ20 −  → γ21 −→ ··· −→ γ2i −
                                                                                            → γ2i+1 −
                                                                                                    →
               L
    231   ··· −
              → γ2n is also an actual execution.                                                     C

          By the induction hypothesis of

                    ∃X1 (o =<c1>k <ρ>env <m>mem ∧ϕ1 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 )

          we conclude (γ1n , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ01 ).
          By the induction hypothesis of

                    ∃X1 (o =<c2>k <ρ>env <m>mem ∧ϕ2 ) ⇓ ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ02 )

          we conclude (γ2n , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ∧ϕ02 ).
          Since γ1n = γ2n = γn , there exits θτ1 : SVar → T with θτ1 SVar/X2 = τ SVar/X2 such
          that γ1n = γ2n =<·>k <θτ1 (ρ0 )>env <θτ1 (m0 )>mem and θτ1 |= ϕ01 and θτ1 |= ϕ02 . Therefor,
          (γn , τ ) |= ∃X2 (o =<·>k <ρ0>env <m0>mem ϕ01 ∧ ϕ02 ).
          Case12: By M-SKIP rule
                                                   ·
                     ∃X(o =<skip>k <ρ>env <m>mem ∧ϕ) ⇓ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ)
      ShangBei Wang                                                                                          42:21


      Γ ≡ ∃X(o =<skip>k <ρ>env <m>mem ∧ϕ) and Γ0 ≡ ∃X(o =<·>k <ρ>env <m>mem ∧ϕ).
      Suppose there exists θτ : SVar → T with θτ SVar/X = τSVar/X such that γ0 =<skip>k <
      θτ (ρ)>env <θτ (m)>mem and θτ |= ϕ and
                                                     L      L      L     L        L       L
                <skip>k <θτ (ρ)>env <θτ (m)>mem −
                                                → γ1 −
                                                     → ··· −
                                                           → γi −
                                                                → γi+1 −
                                                                       → ··· −
                                                                             → γn
                                             P
      If <skip>k <θτ (ρ)>env <θτ (m)>mem −→ γ1 , by SKIP rule, γ1 =<·>k <θτ (ρ)>env <θτ (m)>mem
      and
                                                  E     E      E      E       E
                   <·>k <θτ (ρ)>env <θτ (m)>mem − → ··· −
                                                        → γi − → γi+1 −
                                                                      → ··· − → γn
232   Since θτ |= ϕ, (γ1 , τ ) |= Γ0 . Since σ is an actual execution, (γi , τ ) |= Γ0 , 2 ≤ i ≤ n.
                                                   E
233   If < skip >k < θτ (ρ) >env < θτ (m) >mem −   → γ1 , since σ is an actual execution, (γ1 , τ ) |= Γ
                                                              E      E        P           E      E
234   and there exits j (1 < j ≤ n − 1) such that γ1 −        → ··· −→ γj −   → γj+1 −    → ··· −→ γn with
235   (γi , τ ) |= Γ, 1 ≤ i ≤ j. Suppose there exists θτ1 : SVar → T with θτ1 SVar/X = τ SVar/X
236   such that γj =<skip>k <θτ1 (ρj )>env <θτ1 (mj )>mem and θτ1 |= ϕ. By SKIP rule, we conclude
237   γj+1 =<·>k <θτ1 (ρj )>env <θτ1 (mj )>mem . Due to θτ1 |= ϕ, (γj+1 , τ ) |= Γ0 . Since σ is an actual
238   execution, (γi , τ ) |= Γ0 , j + 1 ≤ i ≤ n.                                                       J

239    4     Matching logic verifier for PIMP
      Intuitively, the matching logic verifier for PIMP is to execute rewriting logic semantics
      symbolically on configuration patterns that we define in section 3. Figure 7 shows matching
      logic verifier for PIMP. First, we add patternItem sort as algebraic infrastructure for pattern.
      Compared to Cfg sort, two new sub cells are added, one to hold the bound variables set
      and the other to hold the constraints. Secondly, we add program annotations. assert ass
      acts as program annotation and can be inserted at any place in the computation. Sort Ass
      don’t include the <· · ·>k because the purpose of program annotation is to describe the state
      of the program. We also add Top sort to wrap a set of patterns such as <Γ1 , Γ2 , · · · , Γn>
      and each Γi is a pattern with program annotation. Final, we introduce semantic rules.
      V-NULL and V-FALSE rules are used to dissolve pattern. A pattern Γi is considered verified
      either when it translate into <·>k <ρ>env <m>mem <X >bnd <ϕ>f orm , meaning that all
      the program annotations have been validated, or when it is found that constraint yield
      false. <Γ1 , Γ2 , · · · , Γn > is emptied means that the program is fully verified. V-ASSERT
      rule replaces pattern’s ass2 with ass1 , which is particularly important when ass1 is a loop
      invariant. V-IF rule divides the current pattern into two patterns, corresponding to the
      two cases that the assumption about b is true or false. V-WHILE rule assumes that ass1
      of the current pattern is invariant and generates two branches. In one branch, ρ(b) is true
      indicating the invariant holds, and in the other branch, ρ(b) is false ignoring the computation
      of current pattern. In V-AWAIT rule, cc is also executed as an indivisible action. In
      V-PARALLEL rule, result(_) : PatternItem → Ass is a function. In later chapters, we
      abbreviate result(<c>k <ρ>env <m>mem <X>bnd <ϕ>f orm ) as result(c, ρ, m, X, ϕ). If
      <<c1>k <ρ>env <m>mem <X>bnd <ϕ1>f orm>→∗ <<·>k <ρ0>env <m0>mem <X 0>bnd <ϕ01>f orm>
      <<c2>k <ρ>env <m>mem <X>bnd <ϕ1>f orm>→∗ <<·>k <ρ0>env <m0>mem <X 0>bnd <ϕ02>f orm>
      then
                      result(c1 , ρ, m, X, ϕ1 ) =<ρ0>env <m0>mem <X 0>bnd <ϕ01>f orm
                      result(c2 , ρ, m, X, ϕ2 ) =<ρ0>env <m0>mem <X 0>bnd <ϕ02>f orm
      result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 ) =<ρ0>env <m0>mem <X 0>bnd <ϕ01 ∧ ϕ02>f orm
240
42:22   From Matching Logic To Parallel Imperative Language Verification



         Matching logic verifier for PIMP
         Abstract Syntax:
         the same as Rewrite Theory Of PIMP, but adding: C ::= · · · | assert ass
         Configurtation:
         the same as Rewrite Theory Of PIMP, but adding:
         PatternItem ::=<C>k |<Env>env |<Mem>mem |<F orm>f orm |<Set−,−    ·   [SV ar]>bnd
         Pattern ::=< Bag −,−
                           .   [PatternItem] >
         Ass ::=< Env >env <Mem>mem < Set·−,− [SV ar] >bnd < F orm >f orm
         Top ::=< Set −,−
                      .   [pattern] >
         Semantic Rules:
         V-NULL:
                             ·
         <<·>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→<·>
         V-FALSE:
                                   ·
         <<c1 ; c2>k <ρ>env <m>mem <X>bnd <f alse>f orm>→<·>
         V-SKIP:
                                                  ·
         <<skip; c>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→<<c>k <ρ>env <m>mem <X>bnd <ϕ>f orm>
         V-ASSERT:
                |=<c>k ass2 ⇒<c>k ass1
         <<assert ass1 ; c>k ass2>→<<c>k ass1>
         V-ASGN1:
                                                     ·
         <<x := e; c>k <ρ>env <m>mem <X>bnd <ϕ>form>→<<c>k <ρ[ρ(e)/x]>env <m>mem <X>bnd <ϕ>form>
         V-ASGN2:
                                         ·
         <<x := A[e]; c>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→
         <<c>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm>
         V-ASGN3:
                                           ·
         <<A[e1 ] := e2 ; c>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→
         <<c>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm>
         V-ARRAY:
                                      ·
         <<A := Array(e); c>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→
         <<c>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm>
         V-IF:
                                             ·
         <<(if(b)c1 else c2 ); c3>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→
         <<c1 ; c3>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm ,
         <c2 ; c3>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm >
         V-WHILE:
                                                        ·
         <<(while b do c1 ); c2>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→
         <<c1 ; assert (<ρ>env <m>mem <X>bnd<ϕ>form )>k <ρ>env <m>mem <X>bnd<ϕ∧(ρ(b) is true)>form ,
         <c2>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm >
         V-AWAIT:
                                         ·
         <<await b then cc; c2>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→
         <<cc; c2>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm>
         V-PAR:
                                            c1 , c2 are interference-free
         <<(c1 k c2 ); c3>k <ρ>env <m>mem <X>bnd<ϕ1 ∧ ϕ2>f orm>→
         <<c1 ; assert(result(c1 , ρ, m, X, ϕ1 ))>k <ρ>env <m>mem <X>bnd<ϕ1>f orm ,
         <c2 ; assert(result(c2 , ρ, m, X, ϕ2 ))>k <ρ>env <m>mem <X>bnd<ϕ2>f orm ,
         <<c3>k result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 ) >



           Figure 4 Matching logic verifier for PIMP
      ShangBei Wang                                                                                          42:23


241   I Theorem 12. Given an annotated computation k ∈ C, k ∈ C is the computation obtained
242   by removing all assert ass from k, the following holds:
243   1. If <<k; assert asspost >k asspre >→∗ <·>, then <k>k asspre ⇓<·>k asspost is derivable
244       from matching logic;
245   2. If < k1 >k asspre ⇓< · >k asspost is derivable from matching logic, then there is an
246       annotated computation k2 such that k2 = k1 and <<k2 ; assert asspost >k asspre>→∗ <·>.

      Proof. Suppose Γ ≡<<k; assert asspost >k asspre > and Γ →∗ <·>. The original pattern Γ
      iterative rewrite it to <Γ1 , Γ2 , · · · , Γn >. Since rewrite logic allows parallel rewriting, we
      require Γ1 , Γ2 , · · · , Γn parallel rewriting. Therefor, we get a rewrite tree with Γ as root node
      and · as leaf nodes. Notice that Γi (0 < i < n + 1) is also a subtree which implies Γi →∗ <·>.
      We prove conclusion 1 by induction on the depth of the rewrite tree. According to the
      rewriting rule adopted in the first step of Γ →∗ <·>, we distinguish different cases:
      Case1: By V-FALSE rule

                   <<c; assert asspost>k <ρ>env <m>mem <X>bnd <f alse>f orm>→<·>

      |=<c>k <ρ>env <m>mem <X >bnd <f alse>f orm ⇒<·>k asspost is tautology. Since <·>k
      asspost ⇓< · >k asspost , < c >k < ρ >env < m >mem < X >bnd < f alse >f orm ⇓< · >k asspost is
      derivable from matching logic by M-CONS rule.
      Case2: By V-ASGN1 rule

                   <<x := e; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→

               <<k 0 ; assert asspost>k <ρ[ρ(e)/x]>env <m>mem <X>bnd <ϕ>f orm>→∗ <·>
      By the induction hypothesis of

               <<k 0 ; assert asspost>k <ρ[ρ(e)/x]>env <m>mem <X>bnd <ϕ>f orm>→∗ <·>

      we conclude <k 0 >k <ρ[ρ(e)/x]>env <m>mem <X >bnd <ϕ>f orm ⇓<·>k asspost . M-ASGN1
      rule implies

      <x := e>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k <ρ[ρ(e)/x]>env <m>mem <X>bnd <ϕ>f orm

      Since x := e; k 0 = x := e; k 0 , by M-SEQ rule, we conclude

                     <x := e; k 0>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost

      is derivable from matching logic.
      Case3: By V-ASGN2 rule

                 <<x := A[e]; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→

        <<k 0 ; assert asspost>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm>→∗ <·>
      By the induction hypothesis of

        <<k 0 ; assert asspost>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm>→∗ <·>

      we conclude

             <k 0>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost
42:24   From Matching Logic To Parallel Imperative Language Verification


        M-ASGN2 rule implies

                               <x := A[e]>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓

                        <·>k <ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm
        Since x := A[e]; k 0 = x := A[e]; k 0 , by M-SEQ rule, we conclude

                      <x := A[e]; k 0>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost

        is derivable from matching logic.
        Case4: By V-ASGN3 rule

                  <<A[e1 ] := e2 ; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→

        <<k 0 ; assert asspost>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm>→∗ <·>
        By the induction hypothesis of

        <<k 0 ; assert asspost>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm>→∗ <·>

        we conclude

              <k 0>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm ⇓<·>k asspost

        M-ASGN3 rule implies

                             <A[e1 ] := e2>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓

                      <·>k <ρ>env <m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm
        Since A[e1 ] := e2 ; k 0 = A[e1 ] := e2 ; k 0 , by M-SEQ rule, we conclude

                    <<A[e1 ] := e2 ; k 0>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost

        is derivable from matching logic.
        Case5: By V-ARRAY rule

                <<A := Array(e); k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→

         <<k 0 ; assert asspost>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm>→∗ <·>
        By the induction hypothesis of

         <<k 0 ; assert asspost>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm>→∗ <·>

        we conclude

               <k 0>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm>⇓<·>k asspost

        M-ARRAY rule implies

                            <A := Array(e)>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓

                        <·>k <ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm
        Since A := Array(e); k 0 = A := Array(e); k 0 , by M-SEQ rule, we conclude

                   <A := Array(e); k 0>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost
ShangBei Wang                                                                               42:25


is derivable from matching logic.
Case6: By V-IF rule

        <<(if(b)c1 else c2 ); k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→

      <<c1 ; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ,
  <c2 ; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm >→∗ <·>
Let Γ1 ≡<k>k <ρ1>env <m1>mem <X1>bnd <ϕ1>f orm and Γ2 ≡<k>k <ρ2>env <m2>mem <
X2>bnd <ϕ2>f orm , Γ1 ∇Γ2 is a new pattern:

<k>k <ρ>env <m>mem <X1 ∪X2 ∪ρ∪m>bnd <(ϕ1 ∧ρ = ρ1 ∧m = m1 )∨(ϕ2 ∧ρ = ρ2 ∧m = m2 )>f orm

Obviously, |= Γ1 ∇Γ2 ⇔ Γ1 ∨ Γ2 . By the induction hypothesis of

  <<c1 ; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>→∗ <·>

we conclude

        <c1 ; k 0>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost

and

       <c2 ; k 0>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k asspost

by the induction hypothesis of

  <<c2 ; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm>→∗ <·>

there must have appropriate ass1 and ass2 such that

          <c1>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k ass1

and
                                 <k 0>k ass1 ⇓<·>k asspost
and
          <c2>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k ass2
and
                                 <k 0>k ass2 ⇓<·>k asspost
Suppose ass1 ≡<ρ1 >env <m1 >mem <X1 >bnd <ϕ1 >f orm and ass2 ≡<ρ2 >env <m2 >mem <
X2>bnd <ϕ2>f orm ,

ass1 ∇ass2 ≡<ρ>env <X1 ∪X2 ∪ρ∪m>bnd <(ϕ1 ∧ρ = ρ1 ∧m = m1 )∨(ϕ2 ∧ρ = ρ2 ∧m = m2 )>f orm

Since |=<k 0>k ass1 ∇ass2 ⇔ (<k 0>k ass1 ) ∨ (<k 0>k ass2 ) and <k 0>k ass1 ⇓<·>k asspost
and <k 0>k ass2 ⇓<·>k asspost , M-CASE rule implies

                             <k 0>k ass1 ∇ass2 ⇓<·>k asspost

Since |=<·>k ass1 ∇ass2 ⇔ (<·>k ass1 ) ∨ (<·>k ass2 ) and |=<·>k ass1 ⇒ (<·>k ass1 ) ∨ (<
·>k ass2 ) and

          <c1>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k ass1
42:26   From Matching Logic To Parallel Imperative Language Verification


        applying M-CONS rule, we conclude

               <c1>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k ass1 ∇ass2

        Since |=<·>k ass1 ∇ass2 ⇔ (<·>k ass1 ) ∨ (<·>k ass2 ) and |=<·>k ass2 ⇒ (<·>k ass1 ) ∨ (<
        ·>k ass2 ) and

                  <c2>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k ass2

        by M-CONS rule, we conclude

               <c2>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k ass1 ∇ass2

        M-IF rule implies

                  <if (b)c1 else c2>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k ass1 ∇ass2

        Applying M-SEQ rule, we conclude

                 <(if (b)c1 else c2 ); k 0>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost

        is derivable from matching logic.
        Case7: By V-WHILE rule

                <<(while b do c); k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→

        <<c; assert(<ρ>env <m>mem <X>bnd<ϕ>form )>k <ρ>env <m>mem <X>bnd<ϕ∧(ρ(b) is true)>form ,
            <k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm >→∗ <·>
        By the induction hypothesis of

        <<c; assert(<ρ>env <m>mem <X>bnd<ϕ>form )>k <ρ>env <m>mem <X>bnd<ϕ∧(ρ(b) is true)>form>

                                                →∗ <·>
        we conclude

        <c>k <ρ>env <m>mem <X>bnd<ϕ∧(ρ(b) is true)>f orm ⇓<·>k <ρ>env <m>mem <X>bnd<ϕ>f orm

        M-WHILE rule implies

                            <while b do c>k <ρ>env <m>mem <X>bnd<ϕ>f orm ⇓

                        <·>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm
        By the induction hypothesis of

            <<k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm>→∗ <·>

        we conclude

                <k 0>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is f alse)>f orm>⇓<·>k asspost

        By M-SEQ rule, we conclude

                   <while b do c; k 0>k <ρ>env <m>mem <X>bnd<ϕ>f orm ⇓<·>k asspost
ShangBei Wang                                                                                  42:27


is derivable from matching logic.
Case8: By V-AWAIT rule

       <<await b then cc; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ>f orm>→

   <<cc; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm>→∗ <·>
By the induction hypothesis of

   <<cc; k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm>→∗ <·>

we conclude

        <cc; k 0>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost

There exits some appropriate ass1 such that

           <cc>k <ρ>env <m>mem <X>bnd<ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k ass1

and
                                   <k 0>k ass1 ⇓<·>k asspost
M-AWAIT rule implies

              <await b then cc>k <ρ>env <m>mem <X>bnd<ϕ>f orm ⇓<·>k ass1

By M-SEQ rule, we conclude

          <await b then cc; k 0>k <ρ>env <m>mem <X>bnd<ϕ>f orm ⇓<·>k asspost

is derivable from matching logic.
Case9: By V-PAR rule

        <<(c1 k c2 ); k 0 ; assert asspost>k <ρ>env <m>mem <X>bnd<ϕ1 ∧ ϕ2>f orm>→

        <<c1 ; assert result(c1 , ρ, m, X, ϕ1 )>k <ρ>env <m>mem <X>bnd<ϕ1>f orm ,

         <c2 ; assert result(c2 , ρ, m, X, ϕ2 )>k <ρ>env <m>mem <X>bnd<ϕ2>f orm ,

       <k 0 ; assert asspost>k result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 ) >→∗ <·>
By the induction hypothesis of

       <<c1 assert result(c1 , ρ, m, X, ϕ1 )>k <ρ>env <m>mem <X>bnd<ϕ1>f orm>→∗

                             <<·>k result(c1 , ρ, m, X, ϕ1 )>→∗ <·>
we conclude

          <c1>k <ρ>env <m>mem <X>bnd<ϕ1>f orm>⇓<·>k result(c1 , ρ, m, X, ϕ1 )

where result(c1 , ρ, m, X, ϕ1 ) =<ρ0>env <m0>mem <X 0>bnd<ϕ01>f orm .
Similarly, we conclude

          <c2>k <ρ>env <m>mem <X>bnd<ϕ2>f orm>⇓<·>k result(c2 , ρ, m, X, ϕ2 )
42:28   From Matching Logic To Parallel Imperative Language Verification


        where result(c2 , ρ, m, X, ϕ2 ) =<ρ0>env <m0>mem <X 0>bnd<ϕ02>f orm .
        Since c1 , c2 are interference-free, M-PAR rule implies

                           <c1 k c2>k <ρ>env <m>mem <X>bnd<ϕ1 ∧ ϕ2>f orm>⇓

                             <·>k result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 )
        By the induction hypothesis of

               <<k 0 ; assert asspost>k result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 )>→∗ <·>

        we conclude

                    <k 0>k result(c1 , ρ, m, X, ϕ1 ) ∩ result(c2 , ρ, m, X, ϕ2 ) ⇓<·>k asspost

        By M-SEQ rule, we conclude

                  <(c1 k c2 ); k 0>k <ρ>env <m>mem <X>bnd<ϕ1 ∧ ϕ2>f orm>⇓<·>k asspost

        is derivable from matching logic.
        Case10: By V-SKIP rule

                 <<skip; k 0 ; assert asspost>k ass1>→<<k 0 ; assert asspost>k ass1>→∗ <·>

        By the induction hypothesis of

                                     <<k 0 ; assert asspost>k ass1>→∗ <·>

        we conclude < k 0 >k ass1 ⇓< · >k asspost . Since < skip >k ass1 ⇓< · >k ass1 and
        skip; k 0 = skip; k 0 , by M-SEQ rule, we conclude < skip; k 0 >k ass1 ⇓< · >k asspost is de-
        rivable from matching logic.
        We annotate the program with assertions which are the pre-condition and post-condition
        of the corresponding code segment in the matching logic, and then verify the annotated
        program. Let ~ be a mapping from matching logic rules to annotated programs.
        If πskip ≡<skip>k ass ⇓<·>k ass, then ~(πskip ) = assert ass; skip; assert ass;
        If πasgn1 ≡< x := e >k asspre ⇓< · >k asspost , then ~(πasgn1 ) = assert asspre ; x :=
        e; assert asspost ;
        If πasgn2 ≡< x := A[e] >k asspre ⇓< · >k asspost , then ~(πasgn2 ) = assert asspre ; x :=
        A[e]; assert asspost ;
        If πasgn3 ≡<A[e1 ] := e2 >k asspre ⇓<·>k asspost , then ~(πasgn3 ) = assert asspre ; A[e1 ] :=
        e2 ; assert asspost ;
        If πarray ≡<A := Array(e)>k asspre ⇓<·>k asspost , then

                          ~(πarray ) = assert asspre ; A := Array(e); assert asspost

        If πseq ≡<c1 ; c2>k asspre ⇓<·>k asspost , then

                            ~(πseq ) = assert asspre ; ~(πc1 ); ~(πc2 ); assert asspost

        where πc1 ≡<c1>k asspre ⇓<·>k ass1 and πc2 ≡<c2>k ass1 ⇓<·>k asspost for appropriate
        ass1 ;
        If πif ≡<if (b) c1 else c2>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost , then

        ~(πif ) = assert(<ρ>env <m>mem <X>bnd <ϕ>f orm ); (if (b) ~(πif1 ) else ~(πif2 )); assert asspost
ShangBei Wang                                                                                   42:29


where πif1 ≡<c1 >k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost and
πif2 ≡<c2>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k asspost ;
If πwhile ≡<while b do c>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost , then

~(πwhile ) = assert(<ρ>env <m>mem <X>bnd <ϕ>f orm ); (while b do ~(πbody )); assert asspost

where πbody ≡<c>k <ρ>env <m>mem <X >bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k <ρ>env <
m>mem <X>bnd <ϕ>f orm ;
If πawait ≡<await b then cc>k <ρ>env <m>mem <X>bnd <ϕ>f orm ⇓<·>k asspost , then

   ~(πawait ) = assert(<ρ>env <X>bnd <ϕ>f orm ); (await b then ~(πbody )); assert asspost

where πbody ≡<cc>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost ;
If πpar ≡<c1 k c2>k <ρ>env <m>mem <X1>bnd <ϕ1 ∧ ϕ2>f orm ⇓<·>k asspost , then

~(πpar ) = assert(<ρ>env <m>mem <X1>bnd <ϕ1 ∧ϕ2>f orm ); (~(πc1 ) k ~(πc2 )); assert asspost

where πc1 ≡<c1>k <ρ>env <m>mem <X1>bnd <ϕ1>f orm ⇓<·>k <ρ0>env <m0>mem <X2>bnd <
ϕ01 >f orm and πc2 ≡<c2 >k <ρ>env <m>mem <X1 >bnd <ϕ2 >f orm ⇓<·>k <ρ0 >env <m0 >mem <
X2>bnd <ϕ02>f orm .
For any <c>k asspre ⇓<·>k asspost , say πc , ~(πc ) = c. All we need to do is that

                                <<~(πc )>k asspre>→∗ <·>

We prove by structural induction on πc :
Case1: πc ≡<x := e>k asspre ⇓<·>k asspost and ~(πc ) ≡ assert asspre ; x := e; assert asspost
where asspre ≡<ρ>env <m>mem <X>bnd <ϕ>f orm and asspost ≡<ρ[ρ(e)/x]>env <m>mem <
X>bnd <ϕ>f orm .
By V-ASSERT and V-ASGN1 rules,

  <<assert asspre ; x := e; assert asspost>k asspre>→<<x := e; assert asspost>k asspre>

                              →<<assert asspost>k asspost>
By V-ASSERT rule again, we conclude

                      <<assert asspost>k asspost>→<<·>k asspost>

The V-NULL rule implies <<·>k asspost>→<·>.
Case2: πc ≡< x := A[e] >k asspre ⇓< · >k asspost and ~(πc ) ≡ assert asspre ; x :=
A[e]; assert asspost where asspre ≡< ρ >env < m >mem < X >bnd < ϕ >f orm and asspost ≡<
ρ[m(ρ(A) +Int ρ(e))/x]>env <m>mem <X>bnd <ϕ>f orm .
By V-ASSERT and V-ASGN2 rules,

<<assert asspre ; x := A[e]; assert asspost>k asspre>→<<x := A[e]; assert asspost>k asspre>

                              →<<assert asspost>k asspost>
By V-ASSERT and V-NULL rules,

                   <<assert asspost>k asspost>→<<·>k asspost>→<·>

Case3: πc ≡<A[e1 ] := e2 >k asspre ⇓<·>k asspost and ~(πc ) ≡ assert asspre ; A[e1 ] :=
e2 ; assert asspost where asspre ≡<ρ>env <m>mem <X>bnd <ϕ>f orm and asspost ≡<ρ>env <
42:30   From Matching Logic To Parallel Imperative Language Verification


        m[ρ(e2 )/(ρ(A) +Int ρ(e1 ))]>mem <X>bnd <ϕ>f orm .
        By V-ASSERT and V-ASGN3 rules,

                          <<assert asspre ; A[e1 ] := e2 ; assert asspost>k asspre>→

                  <<A[e1 ] := e2 ; assert asspost>k asspre>→<<assert asspost>k asspost>
        By V-ASSERT and V-NULL rules,

                            <<assert asspost>k asspost>→<<·>k asspost>→<·>

        Case4: πc ≡<A := Array(e)>k asspre ⇓<·>k asspost and ~(πc ) ≡ assert asspre ; A :=
        Array(e); assert asspost where asspre ≡<ρ>env <m>mem <X>bnd <ϕ>f orm and asspost ≡<
        ρ[p/A]>env <p 7→ [ρ(e)], m>mem <X ∪ {p}>bnd <ϕ>f orm .
        By V-ASSERT and V-ARRAY rules,

                        <<assert asspre ; A := Array(e); assert asspost>k asspre>→

                <<A := Array(e); assert asspost>k asspre>→<<assert asspost>k asspost>
        By V-ASSERT and V-NULL rules,

                            <<assert asspost>k asspost>→<<·>k asspost>→<·>

        Case5: πc ≡<c1 ; c2>k asspre ⇓<·>k asspost and ~(πc ) ≡ assert asspre ; ~(πc1 ); ~(πc2 );
        assert asspost where πc1 ≡<c1 >k asspre ⇓<·>k ass1 and πc2 ≡<c2 >k ass1 ⇓<·>k asspost
        for appropriate ass1 .
        By V-ASSERT rule

                        <<assert asspre ; ~(πc1 ); ~(πc2 ); assert asspost>k asspre>→

                                 <<~(πc1 ); ~(πc2 ); assert asspost>k asspre>
        By the induction hypothesis of πc1 , we conclude

                                    <<~(πc1 )>k asspre>→∗ <<·>k ass1>

        which implies

              <<~(πc1 ); ~(πc2 ); assert asspost>k asspre>→∗ <<~(πc2 ); assert asspost>k ass1>

        By the induction hypothesis of πc2 , we conclude

                                    <<~(πc2 )>k ass1>→∗ <<·>k asspost>

        which implies

                     <<~(πc2 ); assert asspost>k ass1>→∗ <<assert asspost>k asspost>

        Applying V-ASSERT rule and V-NULL rule, we conclude

                            <<assert asspost>k asspost>→<<·>k asspost>→<·>

        Case6: πc ≡<if (b) c1 else c2 >k <ρ>env <m>mem <X >bnd <ϕ>f orm ⇓<·>k asspost and
        ~(πc ) ≡ assert(<ρ>env <m>mem <X>bnd <ϕ>f orm ); (if (b) ~(πif1 ) else ~(πif2 )); assert asspost
        where πif1 ≡<c1 >k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost and
ShangBei Wang                                                                                 42:31


πif2 ≡<c2>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm ⇓<·>k asspost .
By V-ASSERT and V-IF rules,

<<assert(<ρ>env <m>mem <X>bnd <ϕ>f orm ); (if (b) ~(πif1 ) else ~(πif2 )); assert asspost>k

                            <ρ>env <m>mem <X>bnd <ϕ>f orm>→
   <<(if (b) ~(πif1 ) else ~(πif2 )); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→
     <<~(πif1 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ,
     <~(πif2 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm >
By the induction hypothesis of πif1 , we conclude

    <<~(πif1 )>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>→∗ <<·>k asspsot>

which implies

      <<~(πif1 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>

                               →∗ <<assert asspost>k asspsot>
By the induction hypothesis of πif2 , we conclude

   <<~(πif2 )>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm>→∗ <<·>k asspsot>

which implies

     <<~(πif2 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm>

                               →∗ <<assert asspost>k asspsot>
Therefor,

     <<~(πif1 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ,

     <~(πif2 ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm >
                 →∗ <<assert asspost>k aaspost , <assert asspost>k aaspost >
Applying V-ASSERT rule and V-NULL rule, we conclude

                <<assert asspost>k aaspost , <assert asspost>k aaspost >→<·>

Case7: πc ≡< while b do c >k < ρ >env < m >mem < X >bnd < ϕ >f orm ⇓< · >k asspost and
~(πc ) ≡ assert(<ρ>env <m>mem <X >bnd <ϕ>f orm ); (while b do ~(πbody )); assert asspost
where πbody ≡<c>k <ρ>env <m>mem <X >bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k <ρ>env <
m>mem <X>bnd <ϕ>f orm and aaspost ≡<ρ>env <m>mem <X>bnd <ϕ∧(ρ(b) is f alse)>f orm .
By V-ASSERT and V-WHILE rules,

<<assert(<ρ>env <m>mem <X>bnd <ϕ>f orm ); (while b do ~(πbody )); assert asspost>k <ρ>env

                               <m>mem <X>bnd <ϕ>f orm>→
     <<(while b do ~(πbody )); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ>f orm>→
   <<~(πbody ); assert(<ρ>env <m>mem <X>bnd <ϕ>f orm )>k <ρ>env <m>mem <X>bnd
42:32   From Matching Logic To Parallel Imperative Language Verification


        <ϕ∧(ρ(b) is true)>f orm , <assert asspost>k <ρ>env <m>mem <X>bnd <ϕ∧(ρ(b) is f alse)>f orm >
        By the induction hypothesis of πbody , we conclude

                     <<~(πbody )>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>

                              →∗ <<·>k <ρ>env <m>mem <X>bnd <ϕ>f orm>
        which implies
                                <<~(πbody ); assert(<ρ>env <m>mem <X>bnd
                     <ϕ>form )>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>form>→∗
           <<assert(<ρ>env <m>mem <X>bnd <ϕ>f orm )>k <ρ>env <m>mem <X>bnd <ϕ>f orm>
        By V-ASSERT and V-NULL rules

           <<assert(<ρ>env <m>mem <X>bnd <ϕ>f orm )>k <ρ>env <m>mem <X>bnd <ϕ>f orm ,

              <assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is f alse)>f orm >→∗ <·>
        Case8: πc ≡<await b then cc>k <ρ>env <m>mem <X >bnd <ϕ>f orm ⇓<·>k asspost and
        ~(πc ) ≡ assert(<ρ>env <X >bnd <ϕ>f orm ); (await b then ~(πbody )); assert asspost where
        πbody ≡<cc>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm ⇓<·>k asspost .
        By V-ASSERT and V-AWAIT rules,

          <<assert(<ρ>env <X>bnd <ϕ>f orm ); (await b then ~(πbody )); assert asspost>k <ρ>env

                                     <m>mem <X>bnd <ϕ>f orm>→∗
              <<~(πbody ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>form>
        By the induction hypothesis of πbody , we conclude

           <<~(πbody )>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>→∗ <<·>k aaspsot>

        Therefor,

           <<~(πbody ); assert asspost>k <ρ>env <m>mem <X>bnd <ϕ ∧ (ρ(b) is true)>f orm>→∗

                                       <<assert asspost>k aaspsot>
        By V-ASSERT and V-NULL rules

                           <<assert asspost>k aaspsot>→<<·>k aaspsot>→<·>

        Case9: πc ≡< c1 k c2 >k < ρ >env < m >mem < X1 >bnd < ϕ1 ∧ ϕ2 >f orm ⇓< · >k asspost and
        ~(πc ) ≡ assert(<ρ>env <m>mem <X1>bnd <ϕ1 ∧ ϕ2>f orm ); (~(πc1 ) k ~(πc2 )); assert asspost
        where πc1 ≡<c1>k <ρ>env <m>mem <X1>bnd <ϕ1>f orm ⇓<·>k <ρ0>env <m0>mem <X2>bnd <
        ϕ01 >f orm and πc2 ≡<c2 >k <ρ>env <m>mem <X1 >bnd <ϕ2 >f orm ⇓<·>k <ρ0 >env <m0 >mem <
        X2>bnd <ϕ02>f orm and aaspost ≡<ρ0>env <m0>mem <X2>bnd <ϕ01 ∧ ϕ02>f orm
        By V-ASSERT and V-PAR rules,

        <<assert(<ρ>env <m>mem <X1>bnd <ϕ1 ∧ϕ2>f orm ); (~(πc1 ) k ~(πc2 )); assert asspost>k <ρ>env

        <m>mem <X1>bnd <ϕ1 ∧ ϕ2>f orm>→<<(~(πc1 ) k ~(πc2 )); assert asspost>k <ρ>env <m>mem
              <X1>bnd <ϕ1 ∧ ϕ2>f orm>→<<~(πc1 )>k <ρ>env <m>mem <X1>bnd <ϕ1>f orm ,
      ShangBei Wang                                                                                      42:33


                             <~(πc2 )>k <ρ>env <m>mem <X1>bnd <ϕ2>f orm ,
             <assert asspost>k result(~(πc1 ), ρ, m, X1 , ϕ1 ) ∩ result(~(πc2 ), ρ, m, X1 , ϕ2 ) >
      By the induction hypothesis of πc1 , we conclude

                          <<~(πc1 )>k <ρ>env <m>mem <X1>bnd <ϕ1>f orm>→∗

                              <<·>k <ρ0>env <m0>mem <X2>bnd <ϕ01>f orm>
      which implies

                  result(~(πc1 ), ρ, m, X1 , ϕ1 ) =<ρ0>env <m0>mem <X2>bnd <ϕ01>f orm>

      By the induction hypothesis of πc2 , we conclude

                          <<~(πc2 )>k <ρ>env <m>mem <X1>bnd <ϕ2>f orm>→∗

                              <<·>k <ρ0>env <m0>mem <X2>bnd <ϕ02>f orm>
      which implies

                  result(~(πc2 ), ρ, m, X1 , ϕ2 ) =<ρ0>env <m0>mem <X2>bnd <ϕ02>f orm>

      Therefor,
                            <<~(πc1 )>k <ρ>env <m>mem <X1>bnd <ϕ1>f orm ,
                            <~(πc2 )>k <ρ>env <m>mem <X1>bnd <ϕ2>f orm >,
           <assert asspost>k result(~(πc1 ), ρ, m, X1 , ϕ1 ) ∩ result(~(πc2 ), ρ, m, X1 , ϕ2 ) >→∗
              <<·>, <·>, <assert asspost>k <ρ0>env <m0>mem <X2>bnd <ϕ01 ∧ ϕ02>f orm >
      By V-ASSERT and V-NULL rules, we conclude

           <<·>, <·>, <assert asspost>k <ρ0>env <m0>mem <X2>bnd <ϕ01 ∧ ϕ02>f orm >→∗ <·>

      Case10: πc ≡<skip>k ass ⇓<·>k ass and ~(πc ) ≡ assert ass; skip; assert ass.
      By V-ASSERT ,V-SKIP and V-NULL rules ,

      <<assert ass; skip; assert ass>k ass>→<<skip; assert ass>k ass>→<<assert ass>k ass>

                                            →<<·>k ass>→<·>
247                                                                                                  J

248    5     Application Example
249   Let’s take a standard problem in parallel programming as an example. The producer
250   process provides products (e.g. values) to the consumer process. Because the speed of
251   producer process is different from that of consumer, it is profitable to set up a buffer
252   between producer and consumer. But the storage is limited, the buffer can only store
253   N products. Figure 5 uses this solution to copy values of array A[1 : M ] into array
254   B[1 : M ]. Figure 6 gives proof outlines of the producer process and Figure 7 gives proof
255   outlines of the consumer process. The yellow text is the code, the rest are assertions.
256   <ρ>env <m>mem <X>bnd <ϕ>f orm c <ρ0 >env <m0 >mem <X 0 >bnd <ϕ0 >f orm implies the
257   existence of a proof of the corresponding correctness pair, using the rules in Figure 3. Two
42:34     From Matching Logic To Parallel Imperative Language Verification


           Comment:
           C ≡ the shared buffer of size N ;
           in ≡ number of elements added to the buffer;
           out ≡ number of elements removed from the buffer;
           in − out ≡ the total number of elements in the buffer, those are in order : C [out mod N ], · · · ,
           C [(out + in − out − 1) mod N ]

           Begin:
           in := 0; out := 0; i := 1; j := 1;
           producer:
                      while i < M + 1 do
                             x := A[i];
                             await in − out < N then skip;
                             C[in mod N ] := x;
                             in := in + 1;
                             i := i + 1;
           k
           consumer:
                      while j < M + 1 do
                             await in − out > 0 then skip;
                             y := C[out mod N ];
                             out := out + 1;
                             B[j] := y;
                             j := j + 1;
           End

             Figure 5 Producer and Consumer


    258   consecutive assertions denote a use of the rule of M-CONS.
    259     First of all, let’s show that producer and consumer are "interference-free". The only
    260   operation in consumer process that might invalidate the producer process’s assertions is
    261   out := out + 1. The assertions of the producer which may be possibly invalidated are:

    262      6. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p],
    263      b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ x = pi
    264         ∧ in − out < N>f orm
    265      7. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p],
    266      b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1
    267
    268
                ∧ in − out < N ∧ kin mod N = pi>f orm

    269   Suppose γ is a concrete configuration and

    270      γ |=<out := out + 1>k <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b,
    271      C 7→ c, ρ>env <a 7→ [p], b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1
    273
    272         ∧ i < M + 1 ∧ x = pi ∧ in − out < N>f orm

    274   and

    275      γ |=<out := out + 1>k <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b,
    276      C 7→ c, ρ>env <a 7→ [p], b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1
    278
    277         ∧ i < M + 1 ∧ in − out < N ∧ kin mod N = pi>f orm
ShangBei Wang                                                                                                     42:35



 1. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ>f orm

 in := 0; out := 0; i := 1; j := 1;

 2. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1>f orm

 producer:
              while i < M + 1 do

 3. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1>f orm

                      x := A[i];

 4. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ pi , y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1>f orm

 5. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ x = pi>f orm

                      await in − out < N then skip;

 6. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ x = pi ∧ in − out < N
 >f orm

                      C[in mod N ] := x;

 7. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ in − out < N ∧
 kin mod N = pi>f orm

                      in := in + 1;

 8. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in ∧ i < M + 1>f orm

                      i := i + 1;

 9. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1>f orm

 10. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i = M + 1>f orm

 where ϕ = (k(n−1) mod N = pn , out < n < in + 1) ∧ (0 ≤ in − out ≤ N ) ∧ (1 ≤ i ≤ M + 1)∧
 (1 ≤ j ≤ M + 1) and p = p0 , p1 , p2 , · · · , pM and a 7→ [p] = a 7→ p0 , a + 1 7→ p1 , · · · , a + M 7→ pM
 and pn ∈ Int, 0 < n < M + 1


   Figure 6 Proof outlines of Producer
42:36   From Matching Logic To Parallel Imperative Language Verification



         1. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ>f orm

         in := 0; out := 0; i := 1; j := 1;

         2. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1>f orm

         consumer:

                      while j < M + 1 do

         3. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1>f orm

                              await in − out > 0 then skip;

         4. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1 ∧ in − out > 0>f orm

                              y := C[out mod N ];

         5. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ kout mod N , A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p],
         b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1 ∧ in − out > 0
         >f orm

         6. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1 ∧ in − out > 0∧
         y = pj >f orm

                              out := out + 1;

         7. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out ∧ j < M + 1 ∧ y = pj >f orm

                              B[j] := y;

         8. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out ∧ j < M + 1 ∧ qj = pj >f orm

                              j := j + 1;

         9. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1>f orm

         10. <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
         c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j = M + 1>f orm

         where ϕ = (k(n−1) mod N = pn , out < n < in + 1) ∧ (0 ≤ in − out ≤ N ) ∧ (1 ≤ i ≤ M + 1)∧
         (1 ≤ j ≤ M + 1) and φ = qn = pn , 0 < n < j and p = p0 , p1 , p2 , · · · , pM and a 7→ [p] = a 7→ p0 ,
         a + 1 7→ p1 , · · · , a + M 7→ pM and pn ∈ Int, 0 < n < M + 1


           Figure 7 Proof outlines of Consumer
      ShangBei Wang                                                                                                 42:37


279   and

280       γ |=<out := out + 1>k <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b,
281       C 7→ c, ρ>env <a 7→ [p], b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ
282
283
            ∧ j = out + 1 ∧ j < M + 1 ∧ in − out > 0 ∧ y = pj >f orm

284   Then there exit inint , outint , iint , jint , xint , yint , q int , k int such that

285       γ =<out := out + 1>k <in 7→ inint , out 7→ outint , i 7→ iint , j 7→ jint , x 7→ xint , y 7→ yint ,
286
287
          A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q int ], c 7→ [k int ], m>mem

288   and iint = inint + 1 and iint < M + 1 and xint = piint and inint − outint < N and
289   kinint mod N = piint and jint = outint + 1 and jint < M + 1 and inint − outint > 0 and
290   yint = pjint and k(n−1) mod N = pn , outint < n < inint + 1 and 0 ≤ inint − outint ≤ N and
291   1 ≤ iint ≤ M + 1 and 1 ≤ jint ≤ M + 1 and qn = pn , 0 < n < jint .
292   By ASGN1 rule, we get

293       γ 0 =<·>k <in 7→ inint , out 7→ outint + 1, i 7→ iint , j 7→ jint , x 7→ xint , y 7→ yint , A 7→ a,
294
295
          B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q int ], c 7→ [k int ], m>mem

296   Set in = inint , out = outint + 1, i = iint , j = jint , x = xint , y = yint , q = q int , k = k int , then

297       γ 0 |=<·>k <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env
298         <a 7→ [p], b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1
300
299         ∧ x = pi ∧ in − out < N>f orm

301   and

302       γ 0 |=<·>k <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env
303         <a 7→ [p], b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1
305
304         ∧ in − out < N ∧ kin mod N = pi>f orm

306   Thus, the consumer does not interfere with the producer; Similarly, the producer does not
307   interfere with the consumer. The proof outlines of producer k consumer is:

308         <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p],
309       b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ j = out + 1 ∧ i = in + 1>f orm
310                                                producer k consumer;
311         <in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p],
312       b 7→ [q], c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ i = M + 1 ∧ j = M + 1∧
313
314
          j = out + 1 ∧ i = in + 1>f orm

315   Secondary, let us illustrate our verifier on Producer-Consumer. Figure 8 shows the validation
316   process starting with Γstart ≡<<in := 0; out := 0; i := 1; j := 1; assert ass1 ; (producer k
317   consumer); assert asspost >k asspre >. < Γstart >→∗ < · > means Producer-Consumer is
318   validated.
42:38   From Matching Logic To Parallel Imperative Language Verification



         < Γstart >→∗ < Γ1 >→< Γ2 >→< Γ3 , Γ4 , Γ5 >→∗ < Γ6 , Γ7 , Γ8 , Γ9 , Γ5 >→< Γ10 , Γ7 , Γ11 , Γ9 , Γ5 >→
         < Γ12 , Γ7 , Γ13 , Γ9 , Γ5 >→< Γ14 , Γ7 , Γ15 , Γ9 , Γ5 >→< Γ16 , Γ7 , Γ17 , Γ9 , Γ5 >→< Γ18 , Γ7 , Γ19 , Γ9 , Γ5 >→
         < Γ20 , Γ7 , Γ21 , Γ9 , Γ5 >→< Γ22 , Γ7 , Γ23 , Γ9 , Γ5 >→∗ < · >

         producer ≡ assert assp1 ; while i < M + 1 do (x := A[i]; await in − out < N then skip;
         C[in mod N ] := x; in := in + 1; i := i + 1; )

         consumer ≡ assert assc1 ; while j < M + 1 do (await in − out > 0 then skip; y := C[out mod N ];
         out := out + 1; B[j] := y; j := j + 1; )

         Γstart ≡<<in := 0; out := 0; i := 1; j := 1; assert ass1 ; (producer k consumer); assert asspost>k
         asspre >

         Γ1 ≡<<assert ass1 ; (producer k consumer); assert asspost>k ass0 >

         Γ2 ≡<<producer k consumer; assert asspost>k ass1 >

         Γ3 ≡<<producer; assert result(<producer>k assp1 )>k assp1 >

         Γ4 ≡<<consumer; assert result(<consumer>k assc1 )>k assc1 >

         Γ5 ≡<<assert asspost>k result(<producer>k assp1 ) ∩ result(<consumer>k assc1 ) >

         Γ6 ≡<<(x := A[i]; await in − out < N then skip; C[in mod N ] := x; in := in + 1; i := i + 1);
         assert assp1>k assp2 >

         Γ7 ≡<<assert result(<producer>k assp1 )>k assp3 >

         Γ8 ≡<<(await in − out > 0 then skip; y := C[out mod N ]; out := out + 1; B[j] := y; j := j + 1);
         assert assc1>k assc2 >

         Γ9 ≡<<assert result(<consumer>k assc1 )>k assc3 >

         Γ10 ≡<<(await in − out < N then skip; C[in mod N ] := x; in := in + 1; i := i + 1); assert assp1>k
         assp4 >

         Γ11 ≡<<(skip; y := C[out mod N ]; out := out + 1; B[j] := y; j := j + 1); assert assc1>k assc4 >

         Γ12 ≡<<(skip; C[in mod N ] := x; in := in + 1; i := i + 1); assert assp1>k assp5 >

         Γ13 ≡<<(y := C[out mod N ]; out := out + 1; B[j] := y; j := j + 1); assert assc1>k assc4 >

         Γ14 ≡<<(C[in mod N ] := x; in := in + 1; i := i + 1); assert assp1>k assp5 >

         Γ15 ≡<<(out := out + 1; B[j] := y; j := j + 1); assert assc1>k assc5 >

         Γ16 ≡<<(in := in + 1; i := i + 1); assert assp1>k assp6 >

         Γ17 ≡<<(B[j] := y; j := j + 1); assert assc1>k assc6 >

         Γ18 ≡<<i := i + 1; assert assp1>k assp7 >

         Γ19 ≡<<j := j + 1; assert assc1>k assc7 >

         Γ20 ≡<<assert assp1>k assp8 >

         Γ21 ≡<<assert assc1>k assc8 >

         Γ22 ≡<<·>k assp1 >
ShangBei Wang                                                                                                        42:39



 Γ23 ≡<<·>k assc1 >

 asspre ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ>f orm

 asspost ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out+1 ∧ i = in+1>form

 ass0 ≡<in 7→ 0, out 7→ 0, i 7→ 1, j 7→ 1, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ i = in + 1 ∧ i = 1 ∧ j = out + 1 ∧ j = 1>f orm

 ass1 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ i = in + 1 ∧ j = out + 1>f orm

 assp1 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1>f orm

 assc1 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1>f orm

 assp2 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1>f orm

 assc2 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1>f orm

 assp3 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i = M + 1>f orm

 assc3 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j = M + 1>f orm

 assp4 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ x = pi>f orm

 assc4 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1 ∧ in − out > 0>f orm

 assp5 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1 ∧ x = pi ∧ in − out < N>f orm

 assc5 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out+1 ∧ j < M +1 ∧ in−out > 0 ∧ y = pj >f orm

 assp6 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in+1 ∧ i <M +1 ∧ in−out <N ∧ kin mod N = pi>f orm

 assc6 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out ∧ j < M + 1 ∧ y = pj >f orm

 assp7 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
 c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in ∧ i < M + 1>f orm
42:40     From Matching Logic To Parallel Imperative Language Verification



           assc7 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
           c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out ∧ j < M + 1 ∧ qj = pj >f orm

           assp8 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
           c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ i = in + 1 ∧ i < M + 1>f orm

           assc8 ≡<in 7→ in, out 7→ out, i 7→ i, j 7→ j, x 7→ x, y 7→ y, A 7→ a, B 7→ b, C 7→ c, ρ>env <a 7→ [p], b 7→ [q],
           c 7→ [k], m>mem <in, out, i, j, x, y, q, k>bnd <ϕ ∧ φ ∧ j = out + 1 ∧ j < M + 1>f orm

           where ϕ = (k(n−1) mod N = pn , out < n < in + 1) ∧ (0 ≤ in − out ≤ N ) ∧ (1 ≤ i ≤ M + 1)∧
           (1 ≤ j ≤ M + 1) and φ = qn = pn , 0 < n < j and p = p0 , p1 , p2 , · · · , pM and a 7→ [p] = a 7→ p0 ,
           a + 1 7→ p1 , · · · , a + M 7→ pM and pn ∈ Int, 0 < n < M + 1


               Figure 8 Verification of Producer-Consumer


    319    6      Conclusion and Future Work
    320   In this paper, following Grigore Roşu et al’s work, we consider matching logic for PIMP.
    321   In our matching logic, we redefine "interference-free" to character parallel rule and prove
    322   the soundness of matching logic to the operational semantics of PIMP. We also link PIMP’s
    323   operational semantics and PIMP’s verification formally by constructing a matching logic
    324   verifier for PIMP which executes rewriting logic semantics symbolically on configuration
    325   patterns and is sound and complete to matching logic for PIMP. That is our matching logic
    326   verifier for PIMP is sound to the operational semantics of PIMP. The state-of-the-art in
    327   mechanical program verification is to develop and prove its proof system soundness to a
    328   trusted operational semantics. So far, we have achieved this goal in theory. Finally, we also
    329   verify the matching logic verifier through an example which is a standard problem in parallel
    330   programming.
    331   Matching logic for PIMP requires c1 , c2 is "interference-free". Our further work is to generalize
    332   our results in this paper so that they dono’t depend on “interference-free". In theory, match-
    333   ing logic verifier meets the state-of-the-art in mechanical program verification. Unfortunately,
    334   there is no practical executable matching logic verifier in this paper. Although it needs huge
    335   effort to implement the executable matching logic verifier, this is another work we need to
    336   do further.
    337




    338          References
    339    1     Klin. Bartek. Bialgebras for structural operational semantics: An introduction. Theoretical
    340          Computer Science, 412(38):5043–5069, 2011. doi:10.1016/j.tcs.2011.03.023.
    341    2     Reynolds J. C. Theories of programming languages. Cambridge University Press, 2009.
    342    3     Klein. Casey, Clements. John, and Dimoulas. Christos et al. Run your research: on the
    343          effectiveness of lightweight mechanization. ACM SIGPLAN Notices, 47(1):285–296, 2012.
    344          doi:10.1145/2103621.2103691.
    345    4     Hathhorn. Chris, Ellison. Chucky, and Roşu. Grigore. Defining the undefinedness of c. In
    346          Proceedings of the 36th ACM SIGPLAN Conference on Programming Language Design and
    347          Implementation, pages 336–345, 2015. doi:10.1145/2737924.2737979.
    348    5     Ellison. Chucky and Roşu. Grigore. An executable formal semantics of c with applications.
    349          ACM SIGPLAN Notices, 47(1):533–544, 2012. doi:10.1145/2103621.2103719.
      ShangBei Wang                                                                                        42:41


350    6   Calcagno. Cristiano, Distefano. Dino, and Jérémy et al Dubreil. Moving fast with soft-
351        ware verification. In NASA Formal Methods Symposium, pages 3–11, 2015. doi:10.1007/
352        978-3-319-17524-9_1.
353    7   Plotkin G. D. A structural approach to operational semantics. 1981.
354    8   Park. Daejun, Stefănescu. Andrei, and Roşu. Grigore. Kjs: A complete formal semantics of
355        javascript. In Proceedings of the 36th ACM SIGPLAN Conference on Programming Language
356        Design and Implementation, pages 346–356, 2015. doi:10.1145/2737924.2737991.
357    9   Harel. David. Dynamic logic. In Handbook of philosophical logic, pages 497–604. 1984.
358        doi:10.1007/978-94-009-6259-0_10.
359   10   Bogdanas. Denis and Roşu. Grigore. K-java: a complete semantics of java. In Proceedings
360        of the 42nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
361        Languages, pages 445–456, 2015. doi:10.1145/2676726.2676982.
362   11   Şerbănuţă T. Florin, Roşu. Grigore, and Meseguer. José. A rewriting logic approach to
363        operational semantics. Information and Computation, 207(2):305–340, 2009. doi:10.1016/j.
364        ic.2008.03.026.
365   12   Politz J. Gibbs, Martinez. Alejandro, and Milano. Matthew et al. Python: the full monty.
366        ACM SIGPLAN Notices, 48(10):217–232, 2013. doi:10.1145/2544173.2509536.
367   13   Roşu. Grigore. Matching logic. arXiv preprint arXiv:1705.06312, 2017. doi:1705.06312.
368   14   Roşu. Grigore and Stefanescu. Andrei. Matching logic: a new program verification approach
369        (nier track). In 2011 33rd International Conference on Software Engineering (ICSE), pages
370        868–871, 2011. doi:10.1145/1985793.1985928.
371   15   Roşu. Grigore and Stefanescu. Andrei. Checking reachability using matching logic. In
372        Proceedings of the ACM international conference on Object oriented programming systems
373        languages and applications, pages 555–574, 2012. doi:10.1145/2384616.2384656.
374   16   Roşu. Grigore, Ellison. Chucky, and Schulte. Wolfram. Matching logic: An alternative
375        to hoare/floyd logic. In International Conference on Algebraic Methodology and Software
376        Technology, pages 142–162, 2010. doi:10.1007/978-3-642-17796-5_9.
377   17   Roşu. Grigore and Şerbǎnuţǎ T. Florin. An overview of the k semantic framework. The Journal
378        of Logic and Algebraic Programming, 79(6):397–434, 2010. doi:10.1016/j.jlap.2010.03.012.
379   18   Roşu. Grigore and Şerbǎnuţǎ T. Florin. K overview and simple case study. Electronic Notes
380        in Theoretical Computer Science, 304:3–56, 2014. doi:10.1016/j.entcs.2014.05.002.
381   19   Roşu. Grigore, Ellison C. M, and Schulte. Wolfram. From rewriting logic executable semantics
382        to matching logic program verification. Technical report, 2009.
383   20   Roşu. Grigore and Ştefănescu. Andrei. From hoare logic to matching logic reachabil-
384        ity. In International Symposium on Formal Methods, pages 387–402, 2012. doi:10.1007/
385        978-3-642-32759-9_32.
386   21   Barringer. Howard, Kuiper. Ruurd, and Pnueli. Amir. Now you may compose temporal logic
387        specifications. In Proceedings of the sixteenth annual ACM symposium on Theory of computing,
388        pages 51–63, 1984. doi:10.1145/800057.808665.
389   22   Abrahamson. Karl. Modal logic of concurrent nondeterministic programs. In Semantics of
390        concurrent computation, pages 21–33. Springer, 1979.
391   23   Aceto. Luca, Fokkink. Wan, and Verhoef. Chris. Structural operational semantics. In Handbook
392        of process algebra, pages 197–292. 2001. doi:10.1016/B978-044482830-9/50021-7.
393   24   Narciso Martí-Oliet and José Meseguer. Rewriting logic as a logical and semantic framework.
394        In Handbook of Philosophical Logic, pages 1–87. 2002. doi:10.1007/978-94-017-0464-9_1.
395   25   Bodin. Martin, Charguéraud. Arthur, and Filaretti. Daniele et al. A trusted mechanised
396        javascript specification. ACM SIGPLAN Notices, 49(1):87–100, 2014. doi:10.1145/2578855.
397        2535876.
398   26   José Meseguer. Conditional rewriting logic as a unified model of concurrency. Theoretical
399        computer science, 96(1):73–155, 1992. doi:10.1016/0304-3975(92)90182-F.
400   27   José Meseguer. Twenty years of rewriting logic. The Journal of Logic and Algebraic Program-
401        ming, 81(7-8):721–781, 2012. doi:10.1016/j.jlap.2012.06.003.
42:42     From Matching Logic To Parallel Imperative Language Verification


    402   28   Bjørner. Nikolaj, Gurfinkel. Arie, and McMillan. Ken et al. Horn clause solvers for
    403        program verification. In Fields of Logic and Computation II, pages 24–51. 2015. doi:
    404        10.1007/978-3-319-23534-9_2.
    405   29   Sewell. Peter, Nardelli F. Zappa, and Owens. Scott et al. Ott: Effective tool support for
    406        the working semanticist. Journal of functional programming, 20(1):71, 2010. doi:10.1017/
    407        S0956796809990293.
    408   30   Amir Pnueli. The temporal logic of programs. foundations of computer science, pages 46–57,
    409        1977.
    410   31   Apt K. R and Olderog E. R. Fifty years of hoare’s logic. Formal Aspects of Computing,
    411        31(6):751–807, 2019. doi:10.1007/s00165-019-00501-3.
    412   32   Domenica D. R, Siddharth R. S, and Duggal. Chanderpreet et al. Method, system, and
    413        computer program product for customer-level data verification, November 24 2015. US Patent
    414        9,195,985.
    415   33   Sasse. Ralf and José Meseguer. Java+ itp: A verification tool based on hoare logic and
    416        algebraic semantics. Electronic Notes in Theoretical Computer Science, 176(4):29–46, 2007.
    417        doi:10.1016/j.entcs.2007.06.006.
    418   34   Hoare C. A. Richard. An axiomatic basis for computer programming. Communications of the
    419        ACM, 12(10):576–580, 1969. doi:10.1145/363235.363259.
    420   35   Grigore Roşu and Chen. Xiaohong. Matching logic: the foundation of the k framework
    421        (invited talk). In Proceedings of the 9th ACM SIGPLAN International Conference on Certified
    422        Programs and Proofs, pages 1–1, 2020. doi:10.1145/3372885.3378574.
    423   36   Owens. Scott. A sound semantics for ocaml light. In European Symposium on Programming,
    424        pages 1–15, 2008. doi:10.1007/978-3-540-78739-6_1.
    425   37   Owicki. Susan and Gries. David. An axiomatic proof technique for parallel programs i. Acta
    426        Inf., 6(4):319–340, 1976. doi:10.1007/BF00268134.
