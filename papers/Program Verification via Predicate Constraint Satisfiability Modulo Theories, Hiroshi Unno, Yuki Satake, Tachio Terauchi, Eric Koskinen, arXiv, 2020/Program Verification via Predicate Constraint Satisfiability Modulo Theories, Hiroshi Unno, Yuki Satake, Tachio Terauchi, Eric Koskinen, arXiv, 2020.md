                                        Program Verification via Predicate Constraint Satisfiability
                                        Modulo Theories
                                        HIROSHI UNNO, University of Tsukuba, Japan and RIKEN AIP, Japan
                                        YUKI SATAKE, University of Tsukuba, Japan
arXiv:2007.03656v1 [cs.PL] 7 Jul 2020




                                        TACHIO TERAUCHI, Waseda University, Japan
                                        ERIC KOSKINEN, Stevens Institute of Technology, USA
                                        This paper presents a verification framework based on a new class of predicate Constraint Satisfaction Problems
                                        called pCSP⇓λ where constraints are represented as clauses modulo first-order theories over function variables
                                        and predicate variables that may represent well-founded predicates. The verification framework generalizes
                                        an existing one based on Constrained Horn Clauses (CHCs) to arbitrary clauses, function variables, and
                                        well-foundedness constraints. While it is known that the satisfiability of CHCs and the validity of queries
                                        for Constrained Logic Programs (CLP) are inter-reducible, we show that, thanks to the added expressiveness,
                                        pCSP⇓λ is expressive enough to express µCLP queries. µCLP itself is a new extension of CLP that we propose in
                                        this paper. It extends CLP with arbitrarily nested inductive and co-inductive predicates and is equi-expressive
                                        as first-order fixpoint logic. We show that µCLP can naturally encode a wide variety of verification problems
                                        including but not limited to termination/non-termination verification and even full modal mu-calculus model
                                        checking of programs written in various languages. To establish our verification framework, we present (1)
                                        a sound and complete reduction algorithm from µCLP to pCSP⇓λ and (2) a constraint solving method for
                                        pCSP⇓λ based on stratified CounterExample-Guided Inductive Synthesis (CEGIS) of (co-)inductive invariants,
                                        ranking functions, and Skolem functions witnessing existential quantifiers. Stratified CEGIS combines CEGIS
                                        with stratified families of templates to achieve relative completeness and faster and stable convergence of
                                        CEGIS by avoiding the overfitting problem. We have implemented the proposed framework and obtained
                                        promising results on diverse verification problems that are beyond the scope of the previous verification
                                        frameworks based on CHCs.

                                        1   INTRODUCTION
                                        In the formal verification community, a class of predicate constraints called Constrained Horn
                                        Clauses (CHCs) [Bjørner et al. 2015] has been widely adopted as a “common intermediate language”
                                        for uniformly expressing verification problems for various programming paradigms, such as func-
                                        tional and object-oriented languages. Example uses of the CHCs framework include safety property
                                        verification [Grebenshchikov et al. 2012; Gurfinkel et al. 2015; Kahsai et al. 2016] and refinement
                                        type inference [Jhala et al. 2011; Kobayashi et al. 2011; Terauchi 2010; Unno and Kobayashi 2009;
                                        Zhu et al. 2015]. The wide applicability of CHCs is due in no small part to its expressiveness: it is
                                        known that the satisfiability of CHCs and the validity of queries for Constrained Logic Programs
                                        (CLP) [Jaffar and Maher 1994] are inter-reducible. The separation of constraint generation and
                                        solving has facilitated the rapid development of constraint generation tools such as RCaml [Unno
                                        and Kobayashi 2009], SeaHorn [Gurfinkel et al. 2015], and JayHorn [Kahsai et al. 2016] as well as
                                        efficient constraint solving tools such as SPACER [Komuravelli et al. 2014], Eldarica [Hojjat and
                                        Rümmer 2018], and HoIce [Champion et al. 2018].
                                           In this paper we show that the same phenomenon—separating constraint generation from
                                        solving—can empower a wider class of verification problems. To this end, we generalize CHCs
                                        and introduce a new class of predicate Constraint Satisfaction Problems called pCSP⇓λ where
                                        constraints are arbitrary (i.e., possibly non-Horn) clauses modulo first-order theories over function

                                        Authors’ addresses: Hiroshi Unno, University of Tsukuba, Japan , RIKEN AIP, Japan, uhiro@cs.tsukuba.ac.jp; Yuki Satake,
                                        University of Tsukuba, Japan, satake@logic.cs.tsukuba.ac.jp; Tachio Terauchi, Waseda University, Japan, terauchi@waseda.jp;
                                        Eric Koskinen, Stevens Institute of Technology, USA, eric.koskinen@stevens.edu.
2                                                  Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


variables and (possibly well-founded) predicate variables. We then show that pCSP⇓λ can encode
a wider range of verification problems including but not limited to termination/non-termination
verification and even linear-time & branching-time temporal verification (full modal mu-calculus
model checking) of programs written in various languages. All these become possible due to
the increased expressiveness: we show that pCSP⇓λ can express queries for a new extension of
CLP, denoted µCLP, that has arbitrarily nested inductive and co-inductive predicates. µCLP can
naturally encode the above classes of verification problems and subsumes first-order fixpoint
logics (which have recently been applied to temporal verification of imperative and functional
programs [Kobayashi et al. 2019; Nanjo et al. 2018]).
   The first part of this paper is a sound and complete reduction algorithm from µCLP to pCSP⇓λ .
The algorithm generalizes the recently proposed deductive system for the validity of first-order
fixpoint logic [Nanjo et al. 2018] to µCLP. It obtains a collection C of clause constraints that
have placeholder function variables Tλ , Uλ , . . . and predicate variables P, Q, . . ., including some for
well-founded relations R ⇓ , S ⇓ , . . . (see Section 4 for the definition).
   Next, we give a constraint solving method for pCSP⇓λ based on stratified CounterExample-
Guided Inductive Synthesis (CEGIS) of (co-)inductive invariants, ranking functions, and Skolem
functions witnessing existential quantifiers. Stratified CEGIS combines CEGIS [Solar-Lezama et al.
2006] with stratified families of templates [Jhala and McMillan 2006; Terauchi and Unno 2015]
to achieve relative completeness, a theoretical guarantee of convergence, and a faster and stable
convergence by avoiding the overfitting problem of expressive templates to counterexamples [Padhi
et al. 2019]. The constraint solving method naturally generalizes a number of previous techniques
developed for CHCs solving and invariant/ranking function synthesis to the new class pCSP⇓λ . It
proceeds with an iterative algorithm that attempts to discover appropriate functions/predicates or
counterexamples to the given pCSP⇓λ C. Each iteration consists of a synthesis phase that attempts
to guess the function/predicate variables (represented as a function/predicate substitution over
the stratified families of templates) and a validation phase that determines whether the guess was
valid. The validation is done by substituting the guess to C and using an SMT solver to determine
whether C is satisfiable. When the substituion yields a satisfiable C we conclude the µCLP queries
to be valid. Meanwhile, iterations maintain example instances of C from failed attempts by previous
candidates and if these examples become unsatisfiable, we conclude the queries to be invalid.
   We have implemented the above framework. The implementation supports various widely used
background theories: Booleans, linear integer and rational arithmetic. We have applied our tool to
a diverse collection of verification problems (modal mu-calculus, CTL*, CTL, LTL, termination, and
safety) and obtained promising results. The benchmark problems used for experiments go beyond
the capabilities of the existing related tools (such as CHCs solvers and program verification tools).
   The rest of the paper is organized as follows. Section 2 gives a brief overview with some examples.
Section 3 defines µCLP and discusses its expressiveness and applications. Section 4 defines pCSP⇓λ
and Section 5 formalizes the reduction from µCLP. We present our constraint solving method
for pCSP⇓λ based on stratified CEGIS in Section 6. Section 7 reports on the implementation and
experimental evaluation of the presented framework. We discuss related work in Section 8 and
conclude with a remark on future work in Section 9.



2   OVERVIEW
We now highlight the contributions of our work through a series of representative examples that
we will return to later in the paper.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                          3


2.1    Modeling language µCLP: Generalizing CLP.
Our first contribution is µCLP. It generalizes CLP to allow describing a wider range of verification
problems. Let us consider the termination verification problem of the following program obtained
from the benchmark set of the FuncTion tool [Urban 2013; Urban and Miné 2014], which is available
from its web interface1 :
while (x1 >= 0 && x2 >= 0) {
  if (nondet()) { while (x2 <= 10 && nondet()) { x2 = x2 + 1; }
                  x1 = x1 - 1; }
  x2 = x2 - 1; }
where nondet() returns a non-deterministic Boolean value. This program is always terminating
for any external integer inputs x1,x2 and any internal Boolean non-deterministic choices.2
   The termination verification problem for the program can be modularly encoded as the following
µCLP Pterm using both least and greatest fixpoints in the style of extended refinement type systems
[Nanjo et al. 2018; Unno et al. 2017a]:
            Query :      ∀x 1 , x 2 : int. I (x 1 , x 2 )
                         
                         
                                                      ¬(x 1 ≥ 0 ∧ x 2 ≥ 0) ∨
                                                           J (x 2 ) ∧
                         
                            I (x 1 , x 2 )    =µ ©
                         
                         
                                                                2 : int. NP(x 2 , x 2 ) ∨ I (x 1 − 1, x 2 − 1)) ∧ ®
                         
                         
                                                          (∀x   ′                  ′                   ′         ª
                                                      ­
                                                       « I (x 1 , x 2 − 1)
                         
                         
         Program :                                                                                                ¬
                            J  (x   )         =      ¬(x   2 ≤ 10) ∨ J (x 2 + 1)
                         
                                                 µ
                         
                                 2
                                                            ¬(x 2 ≤ 10) ∧ x 2′ = x 2 ∨
                         
                                                                                                            
                          NP(x 2 , x 2′ ) =ν ¬
                         
                         
                                                            x 2 ≤ 10 ∧ (¬NP(x 2 + 1, x 2′ ) ∨ x 2′ = x 2 )
                         
                         
                         
Here, J is an inductive predicate defined as the least fixpoint of the function F (J ) = λx 2 . ¬(x 2 ≤
10) ∨ J (x 2 + 1) over predicates (indicated by µ in =µ ). Likewise, I is also an inductive predicate and is
defined as a least fixpoint. By contrast, NP is a co-inductive predicate defined as the greatest fixpoint
of the function G(NP) = λ(x 2 , x 2′ ). ¬(¬(x 2 ≤ 10) ∧ x 2′ = x 2 ∨ x 2 ≤ 10 ∧ (¬NP(x 2 + 1, x 2′ ) ∨ x 2′ = x 2 )).
Intuitively, I (x 1 , x 2 ) and J (x 2 ) characterize the weakest pre-conditions for the termination of the
outer and the inner loops, respectively; Note that the inner loop always terminates (regardless
of non-deterministic choices) if and only if ¬(x 2 ≤ 10) eventually holds after a finite number of
iterations of incrementing x 2 , which is here enforced by the least-fixpoint definition of J . NP(x 2 , x 2′ )
denotes the complement of the following inductive predicate P(x 2 , x 2′ ) which characterizes the
strongest post-condition of the inner loop:
                 P(x 2 , x 2′ ) =µ ¬(x 2 ≤ 10) ∧ x 2′ = x 2 ∨ x 2 ≤ 10 ∧ (P(x 2 + 1, x 2′ ) ∨ x 2′ = x 2 ).
In the definition of I , NP(x 2 , x 2′ ) is used to bind x 2′ to a possible value of the program variable x2
upon the termination of the inner loop, encapsulating the internal behavior of the inner loop. Thus,
the query formula is valid if and only if the program is always terminating for all initial integer
valuations of x1 and x2 and for all internal non-deterministic choices. Though we could encode the
termination verification problem using only least fixpoints by regarding the given program as a
single monolithic transition system, this example demonstrates an advantage of the use of µCLP
for modularly and naturally encoding verification problems.
   To demonstrate another advantage of µCLP, let us now consider verifying non-termination for
the same program. Thanks to the expressiveness of µCLP, this can be encoded as the following

1 https://www.di.ens.fr/~urban/FuncTion.html
2 Note that the termination is witnessed by, for example, the lexicographic order of x1,x2.
4                                                   Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


µCLP Pnterm , which is simply the De Morgan dual of Pterm :


        Query :   ∃x 1 , x 2 : int. NI (x 1 , x 2 )
                  
                  
                                            x1 ≥ 0 ∧ x2 ≥ 0 ∧
                                                 NJ(x 2 ) ∨
                  
                   NI (x 1 , x 2 ) =ν ©­ (∃x ′ : int. P(x 2 , x ′ ) ∧ NI (x 1 − 1, x ′ − 1)) ∨ ª®
                  
                  
                  
                  
                  
      Program :                                      2              2                2
                                            «   NI (x 1 , x 2 − 1)                              ¬
                                     =ν x 2 ≤ 10 ∧ NJ(x 2 + 1)
                  
                     NJ(x 2 )
                  
                  
                  
                   P(x 2 , x ′ ) =µ ¬(x 2 ≤ 10) ∧ x ′ = x 2 ∨ x 2 ≤ 10 ∧ (P(x 2 + 1, x ′ ) ∨ x ′ = x 2 )
                  
                  
                               2                                2                            2    2



Intuitively, NI (x 1 , x 2 ) and NJ(x 2 ) respectively characterize the weakest pre-conditions for the non-
termination of the outer and the inner loops, which generalize the recurrent sets [Gupta et al. 2008]
whose inhabitant witnesses the non-termination of the given program, for the purpose of modular
encoding. Recall that P(x 2 , x 2′ ) characterizes the strongest post-condition of the inner loop.
   Our validity checker MuVal for µCLP tries to solve the primary Pterm and the dual Pnterm in
parallel. The primal-dual approach turns out to be particularly useful for branching-time temporal
verification where we found either the primary or the dual is often easier to solve than the other
(cf. Section 7).
   As we show in Section 3.3 and Appendix A, µCLP is expressive enough to naturally encode a
diverse class of program verification problems.

      • Linear-time temporal verification of labeled transition systems. Section 3.3 explains a re-
        duction from (ω-)regular model checking where the specifications are given as Büchi word
        automata (which strictly subsume LTL).
      • Bisimulation and bisimilarity verification between labeled transition systems (Appendix A.1).
      • Infinite state, infinite duration games. Safety games, reachability games and so-called LTL
        games (Appendix A.2).

Also, it immediately follows from existing results that µCLP can encode:

      • Linear-time temporal verification of functional programs [Kobayashi et al. 2019; Nanjo et al.
        2018].
      • Branching-time temporal verification. A reduction algorithm from modal mu-calculus model
        checking of imperative programs is shown in [Kobayashi et al. 2019].

2.2    Intermediate representation pCSP⇓λ .
µCLP is a very expressive language, and existing verification intermediate representations such as
Constrained Horn Clauses (CHCs) [Bjørner et al. 2015] are not powerful enough to capture the full
class of µCLP. We therefore introduce a new verification intermediate representation: a class of
predicate Constraint Satisfaction Problems denoted pCSP⇓λ . pCSP⇓λ is a generalization of CHCs to
arbitrary clauses, function variables, and well-foundedness constraints over predicate variables.
   We will present a sound and complete reduction from µCLP validity to pCSP⇓λ satisfiability in
Section 5. It is inspired by a recently proposed deductive system for first-order fixpoint logic [Nanjo
et al. 2018] that eliminates least and greatest fixpoints by over- and under-approximations via
(co-)inductive invariants and well-founded relations, and eliminates quantifiers by Skolemization.
For the termination verification problem Pterm , our reduction gives the following set of clauses
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                        5


whose term variables are implicitly universally quantified:
 
 
  I (x 1 , x 2 ),                                                                                                          (1) 
                                                                                                                                
                                                                                                                                
 
 
                       ¬(x
                         1 ≥ 0 ∧ x 2 ≥ 0) ′∨
                                                                                                                                
                                                                                                                                
                                                                                                                                
          ,               J (x 2 ) ∧ (NP(x 2 , x 2 ) ∨ I (x 1 − 1, x 2′ − 1) ∧ I ⇓ (x 1 , x 2 , x 1 − 1, x 2′ − 1)) ∧ ,
                                                                                                                              
   I (x     x   )  ⇒                                                                                                        (2) 
 
                                                                                                                               
       1     2                                                                                                                 
                          I (x 1 , x 2 − 1) ∧ I ⇓ (x 1 , x 2 , x 1 , x 2 − 1)
 
                                                                                                                               
                                                                                                                                

   J (x   )  ⇒     ¬(x   ≤  10) ∨ J (x 2 + 1) ∧ J⇓ (x 2 , x 2 + 1),                                                         (3) 
 
                                                                                                                               
 
       2              2                                                                                                        
                                                                                                                                
                              ¬(x 2 ≤ 10) ∧ x 2′ = x 2 ∨
 
                                                                                                                             
                                                                                                                                
  NP(x 2 , x 2 ) ⇒ ¬ x 2 ≤ 10 ∧ (¬NP(x 2 + 1, x ′ ) ∨ x ′ , x 2 )
 
 
                 ′                                                                                                             
                                                                                                                            (4) 
                                                                                                                                
                                                                                                                                
                                                                     2      2                                                  
Here I , J , and NP are predicate variables that represent an under-approximation of the (co-)inductive
predicates I , J , and NP, respectively. I ⇓ and J⇓ are well-founded predicate variables that are required
to represent a well-founded relation and used here to enforce a bounded unfolding of the inductive
predicates I and J , respectively; Note here that, in the third clause, J⇓ (x 2 , x 2 + 1) requires that the
formal argument x 2 of J and the actual argument x 2 + 1 of the recursive call to J are related by
a well-founded relation. Similarly, I ⇓ (x 1 , x 2 , x 1 − 1, x 2′ − 1) and I ⇓ (x 1 , x 2 , x 1 , x 2 − 1) in the second
clause require that the pair (x 1 , x 2 ) of the formal arguments and the pairs of the actual arguments
of the two recursive calls are respectively related by a well-founded relation. This transformation of
inductive predicates generalizes binary reachability analysis that has been studied for termination
verification of imperative [Cook et al. 2006; Podelski and Rybalchenko 2004b] and functional
programs [Kuwahara et al. 2014]. The obtained pCSP⇓λ is satisfiable: our satisfiability checker
PCSat for pCSP⇓λ reports the following satisfying predicate assignment:
          I (x 1 , x 2 ) 7→ ⊤,         J (x 2 ) 7→ x 2 ≥ 0, NP(x 1 , x 2 ) 7→ ⊥
 I ⇓ (x 1 , x 2 , x 1 , x 2 ) 7→ x 1 ≥ 0 ∧ x 1 + x 2 ≥ 0 ∧ (x 1 > x 1′ ∨ x 1 ≥ x 1′ ∧ x 1 + x 2 > x 1′ + x 2′ )
                    ′ ′

            J⇓ (x 2 , x 2′ ) 7→ x 2 ≥ 0 ∧ x 2′ ≥ 0 ∧ max(22 − x 2 , x 2 ) ≥ 0 ∧ max(22 − x 2 , x 2 ) > max(22 − x 2′ , x 2′ )
Here, max(t 1 , t 2 ) represents the maximum of integer terms t 1 and t 2 , I ⇓ and J⇓ represent the well-
founded relations respectively induced by the lexicographic ranking function λ(x 1 , x 2 ).(x 1 , x 1 + x 2 )
and the piecewise-defined ranking function λx 2 ≥ 0. max(22 − x 2 , x 2 ).
  For the non-termination verification problem Pnterm , our reduction gives the following pCSP⇓λ :
        
        
         NI (S λ ,Tλ ),                                                                                            (1) 
                                                                                                                        
                                                                                                                        
        
        
        
                               x1 ≥ 0 ∧ x2 ≥ 0 ∧                                                                       
                                                                                                                        
                                                                                                                        
                                                                                                                        
                                  NJ(x 2 ) ∨                                                                           
         NI (x 1 , x 2 ) ⇒ ©­ (P(x 2 , Uλ (x 1 , x 2 )) ∧ NI (x 1 − 1, Uλ (x 1 , x 2 ) − 1)) ∨ ª® ,
                                                                                                                       
                                                                                                                    (2) 
        
                                                                                                                       
        
                                                                                                                       
                                                                                                                        
                                                                                                                        
                               « NI (x 1 , x 2 − 1)                                                    ¬               
                                 10 ∧ NJ(x 2 + 1),
                                                                                                                       
          NJ(x     )  ⇒   x    ≤                                                                                    (3) 
        
                                                                                                                       
        
                2          2                                                                                           
                                                                                                                        
                                ¬(x 2 ≤ 10) ∧ x 2′ = x 2 ∨
        
                                                                                                                     
                                                                                                                        
         P(x 2 , x 2 ) ⇒
                     ′
                                                                                                                       
                                                                                                                   (4) 
                                x 2 ≤ 10 ∧ (P(x 2 + 1, x 2′ ) ∧ P⇓ (x 2 , x 2′ , x 2 + 1, x 2′ ) ∨ x 2′ = x 2 )
                                                                                                                       
                                                                                                                        
                                                                                                                       
Here NI , NJ, and P are predicate variables that represent an under-approximation of the (co-
)inductive predicates NI , NJ, and P, respectively. P⇓ is a well-founded predicate variable used here
to enforce a bounded unfolding of P. S λ , Tλ , and Uλ are function variables that represent total
functions to be synthesized and used here to Skolemize the existential quantification of the term
variables x 1 , x 2 in the query and x 2′ in the body of NJ, respectively.3 Not surprisingly, this pCSP⇓λ
is unsatisfiable.

3 Note that we regard S
                          λ , Tλ as integer variables that represent integer functions of the arity 0.
6                                                          Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


2.3    CounterExample-Guided Inductive Synthesis
Our reduction from µCLP to pCSP⇓λ may generate constraints that go beyond the class of CHCs.
We thus present a new constraint solving method that can handle the general class of constraints,
which is formally defined in Section 4 and here explained informally using the following example
pCSP⇓λ :
                           n ≥ 0 ⇒ X (n),                                     (1) 
                          
                                                                                  
                     C ≜ X (x) ⇒ (Y (x) ∧ X (x + 1)),
                                                                                  
                                                                                   
                                                                               (2)
                           Y (y) ⇒ (y = 0 ∨ Y (y − 1) ∧ Y⇓ (y, y − 1))
                          
                                                                               (3) 
                                                                                   
                                                                                  
Our constraint solving method is based on a CounterExample Guided Inductive Synthesis (CEGIS)
approach to finding a solution of the given constraint set C, i.e., a predicate substitution for X , Y , Y⇓
that satisfies all the three formulas in C and the well-foundedness condition of Y⇓ . Our method is
designed as a general constraint solving schema and this paper presents an instantiation of the
schema based on template-based synthesis [Garg et al. 2014; Sharma et al. 2013b]. This section
is mostly dedicated to informally reviewing well-known CEGIS with template-based synthesis
in order to make the paper self-contained. Detailed exposition, in particular, our extensions with
stratified families of function/predicate templates and unsat-core-based template refinement, are
given in Section 6).
   Our method first prepares predicate templates TX , TY , TY⇓ , with unknown parameters to be
inferred, respectively for the predicate variables X , Y , Y⇓ to restrict the solution space to be
explored. For example, let us here use the templates:4
                              TX ≜ λx .a · x + b ≥ 0,            TY ≜ λy.c · y + d ≥ 0,
                              TY⇓ ≜ λ(z, z ′).d · z + e ≥ 0 ∧ d · z + e > d · z ′ + e.
Here, a, b, c, d, e are unknown parameters of the predicate templates. Note that the form of the
predicate template TY⇓ for Y⇓ guarantees that Y⇓ is a well-founded relation for any valuation of d, e:
the function λz. d · z + e represents an affine ranking function whose return value strictly decreases,
when the input changes from z to z ′. These templates are geared to the background theory, but
other templates could be used for other theories.
    Our constraint solving schema then iteratively accumulates examples E of the constraints in C by
instantiating term variables to concrete values in a counterexample guided manner and enumerates
candidate solutions using E until a genuine solution for C is obtained. More specifically, at each
iteration i, our schema consists of two phases: Synthesis Phase asks a synthesizer to obtain a
candidate solution σ (i) that satisfies the set of examples E (i) and Validation Phase checks whether
σ (i) is a genuine solution of C. If it is the case, our schema returns σ (i) as a solution and otherwise
repeats with E (i+1) obtained from E (i) by adding new examples that are not satisfied by σ (i) .
    We now illustrate this procedure, using the running example. There will be four iterations, each
with two phases.
  First iteration. In the first iteration, we have no examples of the constraints yet, so we start with
examples E (1) = ∅. The template-based synthesizer, using e.g. an SMT solver, may generate any
candidate solution such as:
                                 σ (1) ≜ θ (1) ({X 7→ TX , Y 7→ TY , Y⇓ 7→ TY⇓ }),
                                  θ (1) ≜ {a 7→ 0, b 7→ 0, c 7→ 0, d 7→ 0, e 7→ 0}
4 Our stratified template families further support templates of more general shapes: disjunctions of conjunctions of atomic

formulas for ordinary predicate variables, well-founded relation templates induced by lexicographic piecewise-defined
affine ranking for well-founded predicate variables, and piecewise-defined affine function templates for function variables.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                      7


where θ (1) is a substitution of values for template parameters. We next use this parameter assignment,
substituting it back into the templates. In this example, substituting a 7→ 0 and b 7→ 0 into TX ,
yields λx .0 + 0 ≥ 0, or λx .⊤. We similarly obtain TY = λy.⊤ but obtain TY⇓ = λ(z, z ′).⊥. Together,
we have
                                   σ (1) ≡ {X 7→ λx .⊤, Y 7→ λy.⊤, Y⇓ 7→ λ(z, z ′).⊥}.
  We now enter the second phase of the first iteration: we need to check whether σ (1) is a genuine
solution of C. We substitute σ (1) back into C and for Eqn. 3, to obtain
                             σ (1) (Y )(y) ⇒ (y = 0 ∨ σ (1) (Y )(y − 1) ∧ σ (1) (Y⇓ )(y, y − 1)).
Using an SMT solver, we can find that this is not valid and, thus, the constraint is not satisfied.
An SMT solver may, for example, generate a model y 7→ 1, which gives us an example Y (1) ⇒
Y (0) ∧ Y⇓ (1, 0) of C that is not satisfied by σ (1) . This provides us with a new example E (2) of C that
is not satisfied by σ (1) :
                                                E (2) ≜ {Y (1) ⇒ Y (0) ∧ Y⇓ (1, 0)}.
  Remaining iterations 2, 3, and 4. The next iterations proceed similarly, and yield the following
solutions and examples:
                     σ (2) ≡ {X 7→ λx .⊤, Y 7→ λy.⊤, Y⇓ 7→ λ(z, z ′).z ≥ 0 ∧ z > z ′ }
                    E (3) = E (2) ∪ {Y (−1) ⇒ Y (−2) ∧ Y⇓ (−1, −2)}
                     σ (3) ≡ {X 7→ λx .⊤, Y 7→ λy.y ≥ 0, Y⇓ 7→ λ(z, z ′).z ≥ 0 ∧ z > z ′ }
                    E (4) = E (3) ∪ {X (−1) ⇒ (Y (−1) ∧ X (0))}
                     σ (4) ≡ {X 7→ λx .x ≥ 0, Y 7→ λy.y ≥ 0, Y⇓ 7→ λ(z, z ′).z ≥ 0 ∧ z > z ′ }
From iteration 3, we have refined Y , requiring that it constrains y to be positive. This constraint
eliminates the issue that arose from parameters to Y⇓ being negative. Iteration 4 similarly teaches us
that x must be positive. In the final iteration’s second phase, we find that σ (4) is a genuine solution
of C and exit the procedure.

3     EXTENDED CONSTRAINT LOGIC PROGRAMS µCLP
This section defines the syntax and the semantics of the extension µCLP of constraint logic programs
CLP [Jaffar and Maher 1994] with arbitrarily nested inductive and co-inductive predicates. We also
discuss its application to temporal verification.

3.1    Syntax
Let T be a (possibly many-sorted) first-order theory with the signature Σ. The syntax of T -formulas
and T -terms is:
    (formulas) ϕ ::= X (t 1 , . . . , t ar(X ) ) | p(t 1 , . . . , t ar(p) ) | ¬ϕ | ϕ 1 ∨ ϕ 2 | ϕ 1 ∧ ϕ 2 | ∃x : s.ϕ | ∀x : s.ϕ
        (terms) t ::= x | F (t 1 , . . . , t ar(F ) ) | f (t 1 , . . . , t ar(f ) )
Here, the meta-variables x, X , and F respectively range over term, predicate, and function variables.
The meta-variables p and f respectively denote predicate and function symbols of the signature
Σ. We use s as a meta-variable ranging over sorts of the signature Σ. We write • for the sort of
propositions and s 1 → s 2 for the sort of functions from s 1 to s 2 . We henceforth regard a predicate
variable as a function variable whose return sort is •. We write ar(o) and sort(o) respectively for the
arity and the sort of a syntactic element o. A function f represents a constant if ar(f ) = 0. We write
8                                                         Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


ftv(ϕ), fpv(ϕ), and ffv(ϕ) respectively for the set of free term, predicate, and function variables that
occur in ϕ. Note that fpv(ϕ) ⊆ ffv(ϕ) always holds. We write xe for a sequence of term variables, |e  x|
for the length of xe, and ϵ for the empty sequence. We often abbreviate ¬ϕ 1 ∨ ϕ 2 as ϕ 1 ⇒ ϕ 2 . We
henceforth consider only well-sorted formulas and terms.
   A µCLP P over the theory T is a sequence of mutually (co-)recursive equations of the form:5
                                         x 1 ) =α 1 ϕ 1 ); . . . ; (Xm (e
                                   (X 1 (e                              x m ) =α m ϕ m )
Here, α i ∈ {µ, ν } and for any i, j ∈ {1, . . . , m}, X i may occur only positively in ϕ j . An equation
   x ) =µ ϕ that satisfies ffv(ϕ) ⊆ {X } represents the inductive predicate µX (e
X (e                                                                                   x ). ϕ defined as the
least fixpoint of the function F (X ) = λe    x .ϕ over predicates. Similarly, X (e x ) =ν ϕ that satisfies
ffv(ϕ) ⊆ {X } represents the co-inductive predicate ν X (e    x ). ϕ defined as the greatest fixpoint of F .
Note here that F is monotonic because the bound predicate variable X occurs only positively in
the body ϕ. In cases where ffv(ϕ) ⊆ {X } does not hold, more sophisticated semantic treatment is
required. We formalize this point later in Section 3.2. We define dom(P) = {X 1 , . . . , Xm }. A query for
a µCLP P is defined as a T -formula ϕ. The De Morgan dual ¬P of a µCLP P = (X i (e           x i ) =α ϕ i )m
                                                                                                           i=1 is
              ¬  x i ) =¬α σ (¬ϕ i ))i=1 where σ ≜ {X 1 7→ ¬X 1 , . . . Xm 7→ ¬Xm }, ¬µ ≜ ν , and ¬ν ≜ µ.
defined by (X i (e                   m                           ¬                ¬


   Remark 1. Note that quantifiers over recursively enumerable (r.e.) domains (e.g., integers) can
be eliminated in µCLP; We can encode ∃x : int.ϕ and ∀x : int.ϕ with the bound integer variable x
respectively as E(0) and A(0) using the following inductive and co-inductive predicates E and A:
                 E(x) =µ ϕ ∨ [−x/x]ϕ ∨ E(x + 1)                 A(x) =ν ϕ ∧ [−x/x]ϕ ∧ A(x + 1)
Intuitively, E and A are required to hold for some and for all integer x, respectively. This encoding
strategy, however, cannot apply to non r.e. domains like real numbers and is not useful in practice even
for r.e. domains like rational numbers that have no simple way to enumerate all its elements. This is
the reason why we apply Skolemization via function variables instead in our reduction algorithm to
pCSP⇓λ (see Section 5 for details).                                                                    ■

3.2   Semantics
This section formalizes the denotational semantics of µCLP. Let A = (D, Σ, I ) be the structure
of the background first-order theory T . Here, D is the universe, Σ is the signature, and I is the
interpretation function for the predicate and function symbols in Σ. We write Ds for the set of
values in D of the sort s. In particular, We define D• ≜ {⊤, ⊥} for the sort • of propositions. For a
sequence es = s 1 , . . . , sm of sorts with m ≥ 0, we write Des for the sequence Ds1 , . . . , Dsm . We define
D(es →s) ≜ Des → Ds . We assume that I (p) ∈ Des → D• if sort(p) = e        s → •, and I (f ) ∈ Des → Ds if
sort(f ) = e
           s → s. We introduce the partially ordered sets (D(es →•) , ⊑(es →•) ) by defining
          ⊑• ≜ {(⊤, ⊤), (⊥, ⊤), (⊥, ⊥)},                  ⊑(es →•) ≜ {(f , д) | ∀e
                                                                                 v ∈ Des .f (e
                                                                                             v ) ⊑• G(e
                                                                                                      v )}.
The least upper bound ⊔(es →•) and the greatest lower bound ⊓(es →•) operators with respect to ⊑(es →•)
are then defined as follows:
        ⊤ ⊓• ⊤      ≜     ⊤       ⊤ ⊓• ⊥      ≜    ⊥        ⊥ ⊓• ⊤       ≜      ⊥       ⊥ ⊓• ⊥     ≜    ⊥
        ⊤ ⊔• ⊤      ≜     ⊤       ⊤ ⊔• ⊥      ≜    ⊤        ⊥ ⊔• ⊤       ≜      ⊤       ⊥ ⊔• ⊥     ≜    ⊥
         f ⊓(es →•) д   ≜      v ∈ Des . f (e
                              λe            v ) ⊓• д(e
                                                     v)          f ⊔(es →•) д       ≜    v ∈ Des . f (e
                                                                                        λe            v ) ⊔• д(e
                                                                                                               v)
Note that (Des →• , ⊑es →• ) forms a complete lattice. The least and greatest elements of Des →• are
 x . ⊥ and λe
λe          x . ⊤ respectively.
5 If we fix T to integer arithmetic, µCLP coincides Mu-Arithmetic, a fixpoint logic with integer arithmetic studied in

[Bradfield 1999; Lubarsky 1993] and reformalized as hierarchical equation systems (HES) in [Kobayashi et al. 2019].
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                            9


  Given a T -formula ϕ and an interpretation ρ of free term and function/predicate variables in ϕ,
we write JϕK(ρ) for the truth value of ϕ which is defined as follows:


                d
  J∀x : s.ϕK(ρ) Ã• { JϕK(ρ {x 7→ v}) | v ∈ Ds }
                     ≜                                                    JX (et )K(ρ)   ≜     ρ(X )(Je t K(ρ))
  J∃x : s.ϕK(ρ) ( • { JϕK(ρ {x 7→ v}) | v ∈ Ds }
                     ≜                                                         t )K(ρ)
                                                                            Jp(e         ≜     I (p)(Je
                                                                                                      t K(ρ))
      J¬ϕK(ρ) ≜   ⊤ (JϕK(ρ) = ⊥)                                      Jϕ 1 ∧ ϕ 2 K(ρ)    ≜     Jϕ 1 K(ρ) ⊓• Jϕ 2 K(ρ)
                  ⊥ (JϕK(ρ) = ⊤)                                      Jϕ 1 ∨ ϕ 2 K(ρ)    ≜     Jϕ 1 K(ρ) ⊔• Jϕ 2 K(ρ)
  JxK(ρ) ≜ ρ(x)    JF (e
                       t )K(ρ) ≜ ρ(F )(Je t K(ρ))                     Jf (e
                                                                          t )K(ρ) ≜      I (f )(Jet K(ρ))


Here, we assume that ρ(x) ∈ Dsort(x ) , ρ(X ) ∈ Des → D• if sort(X ) = e
                                                                       s → •, and ρ(F ) ∈ Des → Ds
if sort(X ) = e
              s → s. We write ρ |= ϕ if and only if JϕK(ρ ′) = ⊤ holds for any extension ρ ′ of ρ for
the term and function/predicate variables in (ftv(ϕ) ∪ ffv(ϕ)) \ dom(ρ), where dom(ρ) represents
the domain of ρ. We say the given formula ϕ is valid and write |= ϕ if and only if ∅ |= ϕ holds.
   Given a µCLP P and an interpretation ρ of free term and function/predicate variables in P, we
write [[P]](ρ) for the predicate interpretation for dom(P) induced by P which is defined by:


                    JϵK(ρ)       ≜∅
         x ) =α ϕ); PK(ρ)
    J(X (e                             x ) =α ϕK P (ρ) ⊎ [[P]](ρ ⊎ [[X (e
                                 ≜ JX (e                                x ) =α ϕ]] P (ρ))
                             n                                                             o
                                            )
        x ) =α ϕK P (ρ)
    JX (e                   ≜ X 7→ FPsort(X
                                     α        λq.λe
                                                  v .JϕK ρ{X →
                                                             7 q, x
                                                                  e →
                                                                    7 v
                                                                      e } ⊎ JPK (ρ{X →
                                                                                     7 q})



where dom(ρ) ∩ dom(P) = ∅ and the fixpoint operator FPesα→• (•) is defined by:


                              FPesµ→• (F ) ≜
                                               d
                                          s →•) { q ∈ De
                                         (e             s →• | F (q) ⊑(es →•) q }
                                s →•    Ã
                              FPν (F ) ≜ (es →•) { q ∈ Des →• | q ⊑(es →•) F (q) }
                                e




We write P |= ϕ if and only if JPK(∅) |= ϕ holds.


  Example 3.1. Let us consider µCLP Pν µ ≜ (X =ν X ∧ Y ); (Y =µ X ∨ Y ) and µCLP Pµν ≜ (Y =µ
X ∨ Y ); (X =ν X ∧ Y ). Note that the semantics of Pν µ and Pµν are different as shown below,
though the definition of Pν µ and Pµν only differ in the order of the equations:


         JPν µ K(∅) = JX =ν X ∧ Y K(Y =µ X ∨Y ) (∅) ⊎ JY =µ X ∨ Y Kϵ (JX =ν X ∧ Y K(Y =µ X ∨Y ) (∅))
                     = ρ ν µ ⊎ JY =µ X ∨ Y Kϵ (ρ ν µ )
                     = {X 7→ ⊤} ⊎ JY =µ X ∨ Y Kϵ ({X 7→ ⊤})
                     = {X 7→ ⊤, Y 7→ ⊤}
10                                                     Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


where

           ρ ν µ = X 7→ FPν• λq.JX ∧ Y K({X 7→ q} ⊎ JY =µ X ∨ Y K({X 7→ q}))
                                                                            

                 = X 7→ • { q ∈ D• | q ⊑• JX ∧ Y K({X 7→ q} ⊎ JY =µ X ∨ Y K({X 7→ q})) }
                       Ã
                                                                 µ
                 = X 7→ • { q ∈ D• | q ⊑• JX ∧ Y K({X 7→ q} ⊎ ρ q ) }
                       Ã

                 = X 7→ • { q ∈ D• | q ⊑• JX ∧ Y K({X 7→ q, Y 7→ q}) }
                       Ã

                = {X 7→ ⊤}
                  n                                              o
              µ
             ρq =  Y 7→ FP•µ λq ′ .JX ∨ Y K({X 7→ q, Y 7→ q ′ })
                = {Y 7→ q}
      JPµν K(∅) = JY =µ X ∨ Y K(X =ν X ∧Y ) (∅) ⊎ JX =ν X ∧ Y Kϵ (JY =µ X ∨ Y K(X =ν X ∧Y ) (∅))
                = {Y 7→ ⊥} ⊎ JX =ν X ∧ Y Kϵ ({Y 7→ ⊥})
                = {X 7→ ⊥, Y 7→ ⊥}

                                                                                                                  ■

  Definition 3.2. A validity checking problem (ϕ, P) of a query ϕ for a µCLP P is that of deciding
P |= ϕ, which we will also write |= (ϕ, P).

   Remark 2. The validity of µCLP (ϕ 0 , ((X 1 (e      x 1 ) =α 1 ϕ 1 ); · · · ; (Xm (e
                                                                                      xm ) =αm ϕm ))) has an equiva-
lent CLP validity if all the following conditions are met: (1) α i = ν for all i = 1, . . . , m, (2) X 1 , . . . , Xm
occur only positively in ϕ 0 , and (3) universal (resp. existential) quantifiers occur only positively (resp.
negatively) in ϕ i ’s. We henceforth call this fragment of µCLP, validity-reducible. Similarly, the inva-
lidity of µCLP has an equivalent CLP validity if: (1) α i = µ for all i = 1, . . . , m, (2) X 1 , . . . , Xm occur
only positively in ϕ 0 , (3a) ϕ i ’s only free variables are xei , and (3b) universal (resp. existential) quantifiers
occur only negatively (resp. positively) in ϕ i ’s. We call this µCLP fragment, invalidity-reducible.               ■

3.3    Application to Temporal Property Verification
We now demonstrate the expressiveness of µCLP by showing that it can encode temporal property
verification. In recent years, a wide variety of techniques and tools have emerged for verifying
temporal properties of programs. Here are some examples. In the setting of infinite-state imperative
programs, there have been works that prove CTL properties [Beyene et al. 2013; Cook et al. 2011,
2013], LTL properties [Cook and Koskinen 2011; Dietsch et al. 2015], and others such as CTL∗
properties [Cook et al. 2015]. For infinite-state higher-order programs, [Murase et al. 2016] and
[Koskinen and Terauchi 2014] respectively present automata-theoretic and type-based approaches
to verification of ω-regular properties (that subsume LTL). As already mentioned, there are re-
cent proposals of reductions from temporal program verification to validity checking in fixpoint
logic [Kobayashi et al. 2019, 2018; Nanjo et al. 2018; Watanabe et al. 2019]. Our validity checking
method for µCLP can be combined with their reductions to yield an automated temporal verification
method for infinite-state imperative and functional programs that can solve classes of verification
problems beyond the reach of the existing verification tools.
   As an exemplary instance of such a reduction, we next formalize the reduction from linear
temporal property verification of infinite-state systems to µCLP. First, we review the notion of
labeled transition system (LTS). A LTS is a triple M = (S,T , L) where S ⊆ D n is the the set of states,
L is the finite set of labels, T ⊆ S × L × S is the transition relation. (Note that S may be infinite and
therefore we allow infinite-state systems.) For M = (S,T , L), we often write S M for S, TM for T , and
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                        11

                          ℓ
L M for L. We write s →     − M s ′ when (s, ℓ, s ′) ∈ TM . We omit the subscript M when it is clear from the
context.
     We now review the notion of a Büchi automaton. A (non-deterministic) Büchi automaton A is a
tuple (Q, L, δ, q init , F ) where Q is the finite set of states (unrelated to the states of the LTS), L is the
finite set of labels, δ ⊆ Q × L × Q is the transition relation, q init ∈ Q is the starting state, and F ⊆ Q
is the set of final states. For q ∈ Q and ℓ ∈ L, we write δ (q, ℓ) for the set {q ′ ∈ Q | (q, ℓ, q ′) ∈ δ }. An
infinite word ℓ0 ℓ1 · · · ∈ Lω is accepted by A if and only if there exists an infinite sequence of states
q 0 , q 1 , . . . such that q 0 = q init , qi+1 ∈ δ (qi , ℓ) for all i ≥ 0, and some state in F occurs infinitely
often.
     We consider the temporal property verification problem in which we are given a LTS M, a
predicate ϕ init (e   x ) on states of the LTS, and a Büchi automaton A such that the label set of A is
L M . Recall that we allow a LTS to be infinite-state.) The goal of the verification is to decide if for
any (infinite) execution of M from a state satisfying ϕ init (e          x ), the infinite sequence of labels of the
execution is accepted by A. That is, the goal is to verify whether the given LTS satisfies the linear
temporal property specified by the given Büchi automaton. The problem can be expressed in µCLP
by defining the mutually-recursive least-and-greatest fixpoint predicates LVq,α (e                   x ) for each q ∈ Q
and α ∈ {µ, ν }:
                                              Û              ℓ           Ü
                             LVq,α (ex ) =α        y .⟨e
                                                  ∀e   x⟩ → − ⟨ey⟩ ⇒            LVq ′,α (q ′ ) (e
                                                                                                y ).
                                          ℓ ∈L                      q ′ ∈δ (q, ℓ)

Here, α(q) = ν if q ∈ F and α(q) = µ otherwise. Then, the LTS satisfies the temporal property if
and only if ϕ init (e
                    x ) ⇒ LVqinit ,ν (e
                                      x ) is valid. The correctness of the construction follows from the
fact that LVq,_ (e
                 x ) represents the set of states from which the labels along the execution of the LTS
is accepted by A when A is run from the state q. Note that the occurrence of a predicate in the
body of the recursive definition becomes the LV_, µ variant when no state in F is visited in the
corresponding execution step. This ensures that there must be a path in which a state from F is
visited infinitely often.

4   PREDICATE CONSTRAINT SATISFACTION PROBLEMS pCSP⇓λ
We now describe a new verification intermediate representation, that generalizes CHCs, and serves
as an intermediary for automating µCLP validity queries. Specifically, we formalize the class pCSP⇓λ
of predicate constraint satisfaction problems. We use φ as a meta-variable ranging over T -formulas
(cf. Section 3) without quantifiers and predicate variables (but possibly with non-predicate function
variables whose return sort is not •). First, we define a pCSP C (without function variables and
well-founded predicate variables) to be a finite set of clauses of the form
                                         ℓ
                                                    !   m
                                                                       !
                                        Ü              Ü
                                   φ∨      X i (e
                                                ti ) ∨      ¬X i (e
                                                                  ti )
                                                 i=1           i=ℓ+1

where 0 ≤ ℓ ≤ m and ffv(φ) = ∅.
   We write ftv(c) and ftv(C) for the set of free term variables that occur in c and C, respectively.
We regard the variables in ftv(c) as implicitly universally quantified. We write fpv(C) (resp. ffv(C))
for the set of free predicate (resp. function) variables that occur in C. A pCSP C is called CHCs
if ℓ ≤ 1 for all clauses c ∈ C, and co-CHCs if m ≤ ℓ + 1 for all c ∈ C. A pCSP C is called linear
CHCs (or linear co-CHCs) if C is both CHCs and co-CHCs. A function/predicate substitution σ is a
finite map from non-predicate function variables F to closed functions of the form λx 1 , . . . , x ar(F ) .t
and predicate variables X to closed predicates of the form λx 1 , . . . , x ar(X ) .φ. We write σ (C) for
the application of σ to C and dom(σ ) for the domain of σ . We call σ a syntactic solution for C if
12                                                  Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen

                          Ó
ffv(C) ⊆ dom(σ ) and |= σ (C). Similarly, Ó
                                          we call a function/predicate interpretation ρ a semantic
solution for C if ffv(C) ⊆ dom(ρ) and ρ |= C.
   We next extend pCSP to pCSP⇓λ by adding function variables and well-foundedness constraints.
A pCSP⇓λ (C, R) consists of
     • a finite set C of pCSP-clauses over function/predicate variables without necessarily satisfying
       the pCSP-restriction ffv(φ) = ∅ of the φ-part of each clause and
     • a set R of well-founded predicate variables that are required to represent well-founded
       relations.
We write ρ |= WF(X ) if the interpretation ρ(X ) of the predicate variable X is well-founded, that
is, sort(X ) = (e
                s ,e                         s of sorts and there is no infinite sequence ve1 , ve2 , . . .
                   s ) → • for some sequence e
of sequences vei of values of the sorts e             vi , vei+1 ) ∈ ρ(X ) for all i ≥ 1. We call a func-
                                         s such that (e
tion/predicate interpretation ρ a semantic solution for (C, R) if ρ is a semantic solution of C and
ρ |= WF(X ) for all X ∈ R. The notion of syntactic solution can be similarly generalized to pCSP⇓λ .
   Definition 4.1 (Satisfiability of pCSP⇓λ ). The predicate satisfiability problem of a pCSP⇓λ (C, R)
is that of deciding whether it has a semantic solution.
   It is well known that the satisfiability of CHCs and the validity of CLP are inter-reducible. In
Section 5, we will show a sound and complete reduction from the validity of µCLP to the satisfiability
of pCSP⇓λ . The reduction is of practical importance because the latter problem is often easier to
address: we may find a certificate of the satisfiability instead of exhaustively checking all possible
cases.

5    REDUCTION ALGORITHM FROM µCLP TO pCSP⇓λ
This section defines our reduction algorithm from the given µCLP validity problem (ϕ, P) (cf. Defi-
nition 3.2) to a pCSP⇓λ satisfiability problem (C, R) (cf. Definition 4.1). We assume without loss of
generality that the (co-)inductive predicates X ∈ dom(P) occur only positively in the query ϕ: we
can always transform the given query into this form by replacing each negative occurrence of X in
ϕ with ¬X ¬ where the predicate X ¬ is defined by the De Morgan dual ¬P.
   Our reduction consists of three steps: The first step, elim∃ , Skolemizes positive occurrences
of existential quantifiers and negative occurrences of universal quantifiers by introducing fresh
function variables. The second step, elimµ , replaces inductive predicates defined by µ-equations
with co-inductive predicates defined by ν-equations with guards (i.e., well-foundedness constraints)
for co-recursion added to preserve the semantics. The third step, elimν , further eliminates co-
inductive predicates by replacing them with uninterpreted predicates represented as fresh predicate
variables. Formally, the reduction algorithm is:
                               let (ϕ µ , Pµ ) = elim∃ (ϕ, P) in
             reduct(ϕ, P) ≜
                               let (ϕ ν , Pν , R) = elimµ (ϕ µ , Pµ , ∅) in (elimν (ϕ ν , Pν ), R)
Here, the µCLP (ϕ µ , Pµ ) is obtained from (ϕ, P) by eliminating existential quantifiers with fresh
function variables as stated above. The definition of elimν (ϕ, P) is given as:
                                     elimν (ϕ, ϵ) ≜ cnf(ϕ)
                                     x ) =ν ϕ ′)) ≜ elimν (ϕ, P) ∪ cnf(X (e
                    elimν (ϕ, P; (X (e                                    x ) ⇒ ϕ ′)

where ϕ is the formula obtained from ϕ by replacing each occurrence of a predicate X ∈ dom(P)
                                             an under-approximation of X . cnf(ϕ) converts ϕ into
with the predicate variable X that representsÓ
its prenex and conjunctive normal form ∀e x . C and returns the set C of clauses. The most tricky
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                 13


part of the algorithm, namely, elimµ (ϕ, P, R), is defined by:
                   x i ) =ν ϕ i )m
   elimµ (ϕ, (X i (e             i=1 , R) ≜ (ϕ, (X i (e
                                                      x i ) =ν ϕ i )m
                                                                    i=1 , R)                                        (base)
   elimµ (ϕ, P; (X (e x ) =µ ϕ ); (X i (e
                                  ′
                                        x i ) =ν ϕ i )m
                                                      i=1 , R) ≜                                               (recursive)
                                 x ) =ν σX (ϕ )); (X i (bi , xe, xei ) =ν σi (ϕ i ))m
                                                 ′
                                                                                    i=1 , R ∪ X ⇓
                                                                                             
      elimµ (σ0 (ϕ), σ0 (P); (X (e                                                                        )
                  y .X i (⊥, ve, ye) | i = 1, . . . , m }
   σ0 ≜ { X i 7→ λe
                  y .X (e           x , ye) ∪ { X i 7→ λe y .X i (⊤, xe, ye) | i = 1, . . . , m }
         
   σX ≜ X 7→ λe         y ) ∧ X ⇓ (e
                 y .X (e                    x , ye)) ∪ { X j 7→ λe y .X j (bi , xe, ye) | j = 1, . . . , m }
        
   σi ≜ X 7→ λe        y ) ∧ (bi ⇒ X ⇓ (e
The third argument of elimµ accumulates generated fresh well-founded predicate variables. The base
case of elimµ (ϕ, P, R) just returns the converted ν -only µCLP (ϕ, P) that contains well-founded
predicate variables in R. In the recursive step, for the definition X (e                     x ) =µ ϕ ′ of the right-most
inductive (i.e., µ) predicate X in the input µCLP, we generate a fresh well-founded predicate
variable X ⇓ and use it as the guard for each co-recursion in the converted co-inductive definition
X (ex ) =ν σX (ϕ ′): we use the substitution σX to replace each call X (e                   t ) in the body ϕ ′ of X with
X (t ) ∧ X ⇓ (e
    e          x , t ) that checks that the formal arguments xe of X and the actual arguments e
                  e                                                                                                t of the
co-recursion are related by the well-founded relation represented by X ⇓ . At the same time, we
extend the formal arguments of each co-inductive (i.e., ν ) predicate X i in the right-hand side of
the equation for X with arguments xe of the same sort as the formal arguments of X and a Boolean
argument bi , where we assume that the formal arguments xei of X i are α-renamed to avoid a name
conflict between xei and xe, bi . The extended formal arguments xe of X i are used to receive the actual
arguments previously passed to a call to the inductive predicate X and are related by X ⇓ , in the
converted definition of X i , with the actual arguments passed to each indirect recursive call to X in
X i .6 Dummy values are passed as xe when no such previous call to X exists and the extended Boolean
formal argument bi of X i indicates whether there indeed is such a call to X and its actual arguments
are passed as xe to X i (bi = ⊤) or the dummy values are passed as xe to X i (bi = ⊥). In fact, we use the
substitution σ0 to replace each call X i (e     t ) in the query ϕ and the definition of the predicates P in the
left-hand side of the equation for X with X i (⊥, ve, e          t ) for some sequence ve of dummy values of the
same sorts as the formal arguments xe of X . For the definition X (e              x ) =µ ϕ ′, we use the substitution σX
to replace each call X i (t ) in X with X i (⊤, xe, t ). For the definition X j (e
                              e                         e                                x j ) =ν ϕ j of each co-inductive
predicate X j in the right-hand side of the equation for X , we use σ j to replace each call X i (e                t ) in X j
with X i (b j , xe, e
                    t ) and each call X (e
                                         t ) with X (et ) ∧ (b j ⇒ X ⇓ (e x ,e
                                                                             t )) that checks that if xe are not dummy
(i.e., b j = ⊤), the actual arguments of a previous call to X passed around to X j as its extended
formal arguments xe are related by X ⇓ with the actual arguments e                    t of the indirect recursive call to
X . In the resulting µCLP, the generated well-founded predicate variables occur only positively.
   Example 5.1. Let us consider the µCLP (ϕ, P) where ϕ ≜ ∀x .X (x) ∧ Y (x) and
                             P ≜ (X (x) =µ Y (x − 1)); (Y (y) =µ y ≤ 0 ∨ X (y − 1))
We obtain elim∃ (ϕ, P) = (ϕ, P) and
             elimµ (ϕ, P, ∅) = elimµ (ϕ, (X (x) =µ Y (x − 1)); (Y (y) =ν y ≤ 0 ∨ X (y − 1)), ∅)
                                    ∀x .X (x) ∧ Y (⊥, 0, x),
                                  ­ (X (x) =ν Y (⊤, x, x − 1));
                                  ©                                                             ª
                                 =­
                                                                                                ®
                                  ­ (Y (b, x, y) =  y ≤    ∨ X (y −    ∧ (b ⇒ X   (x, y −
                                                                                                ®
                                                 ν      0          1)          ⇓         1))), ®
                                  « X⇓                                                          ¬
6 This transformation is similar in spirit to binary reachability analysis [Cook et al. 2006; Kuwahara et al. 2014; Podelski and

Rybalchenko 2004b] for termination verification.
14                                                   Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


Here, in the first step of the transformation, the inductive definition of Y is simply replaced by the
co-inductive definition because the body of Y has no recursive call to Y . The indirect recursive
call to X in Y is properly handled in the second step by adding the formal arguments b and x to
Y . Note also that in the call Y (⊥, 0, x) in the query, 0 is used as a dummy value for the extended
formal argument x of Y .
    We thus get pCSP reduct(ϕ, P) = (C, X ⇓ ) where
                                             
                                                                                               
                  X (x), Y (⊥, 0, x), ¬X (x) ∨ Y (⊤, x, x − 1),
        C ≜
                  ¬Y (b, x, y) ∨ y ≤ 0 ∨ X (y − 1), ¬Y (b, x, y) ∨ y ≤ 0 ∨ ¬b ∨ X ⇓ (x, y − 1))
                                                                                                                ■
  Remark 3. In the implementation of reduct(ϕ, P) in our µCLP validity checker MuVal, unnecessary
arguments addition is suppressed. For example, from the µCLP (ϕ, P) where
               ϕ ≜ ∀x .X (x)
             P ≜ (X (x) =µ Y (x − 1)); (Y (y) =µ Z (y − 1)); (Z (z) =µ z ≤ 0 ∨ X (z − 1))
                                         
reduct(ϕ, P) generates the pCSP (C, X ⇓ ) where
          X (x), X (x) ⇒ Y (⊤, x, x − 1), Y (b1 , x, y) ⇒ Z (b1 , x, ⊤, y, y − 1),
                                                                                                         
   C≜
          Z (b1 , x, b2 , y, z) ⇒ z ≤ 0 ∨ X (z − 1), Z (b1 , x, b2 , y, z) ∧ b1 ⇒ z ≤ 0 ∨ X ⇓ (x, z − 1))
By contrast, MuVal gets a simpler but equi-satisfiable pCSP (C ′, X ⇓ ) where
                                                                           
                                                                                               
                           X (x), X (x) ⇒ Y (x, x − 1), Y (x, y) ⇒ Z (x, y − 1),
             C′ ≜
                           Z (x, z) ⇒ z ≤ 0 ∨ X (z − 1), Z (x, z) ⇒ z ≤ 0 ∨ X ⇓ (x, z − 1))
Note that the query ϕ calls X , X calls Y , Y calls Z , and Z recursively calls X . Thus, if we start from the
query, Z is always passed the actual argument of the previous call to X and, therefore, b1 is always ⊤
and so unneeded. Likewise, b2 is also always ⊤ and unneeded.                                                 ■
     We now show the following soundness and the completeness of the reduction algorithm.
     Theorem 5.2. reduct(ϕ, P) has a semantic solution if and only if |= (ϕ, P).
   This follows from the lemmas for each steps of reduct(ϕ, P): The following lemma for the
first-step elim∃ (ϕ, P) follows immediately from the well-known soundness and completeness of
Skolemization for first-order logic.
  Lemma 5.3. |= (ϕ, P) if and only if there is an interpretation ρ for the function variables introduced
by the Skolemization such that ρ |= elim∃ (ϕ, P).
   The following lemma for the third-step elimν (ϕ, P) follows from the maximality of the greatest
fixpoints (i.e., co-induction principle) (see e.g., Corollary 1 in [Unno et al. 2017b] for a formal related
discussion of least fixpoints that occur in negative positions).
  Lemma 5.4. Let ρ be any interpretation of ffv(ϕ, P). elimν (ϕ, P) has a semantic solution that
extends ρ if and only if ρ |= (ϕ, P).
     We finally show the soundness and completeness of the second-step elimµ (ϕ, P).
  Lemma 5.5. Suppose that elimµ (ϕ, P) = (ϕ ′, P ′, R). We then have |= (ϕ, P) if and only if there is
an interpretation ρ of R such that ρ |= WF(X ) for all X ∈ R and ρ |= (ϕ ′, P ′).
     This can be shown as a corollary of the following lemma.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                            15


    Lemma 5.6. ρ |= (ϕ, P; (X (e  x ) =µ ϕ ′); (X i (ex i ) =ν ϕ i )mi=1 ) if and only if there is an interpretation
ρ ′ of X  ⇓ such  that ρ ′ |= WF(X ⇓ ) and ρ ⊎  ρ ′  |=    (σ 0 (ϕ), σ            x ) =ν σX (ϕ ′)); (X i (bi , xe, xei ) =ν
                                                                       0 (P); (X (e
          m
σi (ϕ i ))i=1 ) where
                      y .X i (⊥, ve, ye) | i = 1, . . . , m }
       σ0 ≜ { X i 7→ λe
                     y .X (e           x , ye) ∪ { X i 7→ λe  y .X i (⊤, xe, ye) | i = 1, . . . , m }
            
       σX ≜ X 7→ λe        y ) ∧ X ⇓ (e
                     y .X (e                   x , ye)) ∪ { X j 7→ λe   y .X j (bi , xe, ye) | j = 1, . . . , m }
            
        σi ≜ X 7→ λe       y ) ∧ (bi ⇒ X ⇓ (e
   Remark 4. Let (ϕ, P) be a µCLP. If (ϕ, P) is validity-reducible (recall Remark 2), reduct(ϕ, P)
always generates co-CHCs. Similarly, if (ϕ, P) is invalidity-reducible, reduct(ϕ, ¬(P)) always gen-
erates co-CHCs. Note also that the satisfiability of the co-CHCs C can be further reduced to that of
the CHCs C ¬ , obtained from C by replacing, each literal of the form X (e t ) with ¬X ¬ (e
                                                                                          t ) and ¬X (e
                                                                                                      t)
        ¬
with X (e                            ¬
          t ) for X ∈ fpv(C), where X is a fresh predicate variable that represents the negation of X .
Thus we can use off-the-shelf CHC solvers to discharge the validity-reducible and invalidity-reducible
fragments of µCLP. Our constraint solving method described in the next section can handle the full
classes of pCSP⇓λ and µCLP (via the reduction).                                                       ■

6   CONSTRAINT SOLVING METHOD FOR pCSP⇓λ
This section describes our CEGIS-based method for finding a (syntactic) solution—in other words,
(co-)inductive invariants, ranking functions, and witnesses for existential quantifiers—of the given
pCSP⇓λ (C, R). Our method iteratively accumulates example instances of C, which are defined to
be pCSP⇓λ -clauses without term variables obtained from C by instantiating ftv(C), from which a
sequence of candidate solutions for C is generated by using a synthesizer S (whose details are
deferred to Section 6.2), until a genuine solution or a counterexample (i.e., unsatisfiable example
instances) is found. We write E (i) for the set of example instances accumulated before the iteration
i. Starting from E (1) = ∅, for each iteration i ≥ 1, our method performs the following:
   (1) Synthesis Phase: We check whether the set of instances (E (i) , R) is unsatisfiable. If so, we
       return E (i) as a counter example to the input pCSP⇓λ (C, R). Otherwise, we let the synthesizer
       S find a syntactic solution σ (i) (with dom(σ (i) ) = ffv(C)) of the instances (E (i) , R), which
       will be used as a candidate solution for (C, R).
   (2) Validation Phase: We check whether σ (i) is a genuine solution to (C, R) by using an off-
       the-shelf SMT solver. If so, we return σ (i) as the solution. Otherwise, for each clause c ∈ C
       unsatisfied by σ (i) , we obtain a counterexample, that is, a term substitution θ c such that
       dom(θ c ) = ftv(c) and ̸ |= θ c (σ (i) (c)). We then update the example set by adding a new example
       instance for each unsatisfied clause (i.e., E (i+1) = E (i) ∪ { θ c (c) | c ∈ C∧ ̸ |= σ (i) (c) }), and
       proceed to the next iteration with E (i+1) .
   Remark 5. In our pCSP⇓λ satisfiability checker PCSat (Section 7), we implemented a third phase
that we call the resolution phase for accelerating the convergence of the CEGIS loop. There, we first
apply unit propagation repeatedly to the example instances E to obtain the set E + of positive examples
               v ) and the set E − of negative examples of the form ¬X (e
of the form X (e                                                         v ). We then repeatedly apply
resolution principle to the clauses in the original pCSP⇓λ C and the clauses in E + ∪ E − to obtain new
positive/negative examples (without containing term variables), which are then added to E.
   In general, the above CEGIS procedure may diverge, which is inevitable due to the undecidability
of pCSP⇓λ . But it satisfies the so called progress property: any counterexample and candidate solution
found in an iteration are never generated again in succeeding iterations. Furthermore, if we carefully
design a synthesizer S as discussed in Section 6.2 by incorporating our idea of stratified CEGIS, we
can show the relative completeness in the sense of [Jhala and McMillan 2006; Terauchi and Unno
16                                                       Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


2015]: if the given pCSP⇓λ (C, R) has a syntactic solution expressible in the stratified families of
templates, a solution of the pCSP⇓λ is eventually found by the procedure.
   The rest of this section discusses the details of the synthesis phase. Section 6.1 discusses how to
check the unsatisfiability of example instances (E, R). Section 6.2 discusses the synthesis based on
stratified template families and unsat-core-based template refinement. For simplicity, we focus on
the theory of quantifier-free linear integer arithmetic (QFLIA) in the description of the synthesis
phase. Designing stratified template families for richer theories such as arrays, algebraic data types,
and heaps is actually non-trivial and will be discussed as a future work in Section 9.

6.1     Unsatisfiability Checking of Example Instances
If R = ∅, the unsatisfiability of the given example instances (E, R) can be decided by an off-the-shelf
SAT solver (if (ffv(E) \ fpv(E)) = ∅) or SMT solver (otherwise) because E is a finite set of clauses
not containing term variables. Otherwise, we use the following (CDCL-like) iterative algorithm
staring from E0 = E: For each iteration i ≥ 0, we first check whether (Ei , ∅) is unsatisfiable. If so,
then we conclude that (E, R) is unsatisfiable. Otherwise, we obtain a satisfying assignment σ for
Ei . Then, for each X ∈ R, we consider the graph comprising the edges { (e   v 1 , ve2 ) | |= σ (X (e
                                                                                                    v 1 , ve2 )) }
and enumerate its simple cycles (e.g., by using the algorithm of [Johnson 1975]). Note that such
cycles would be counterexamples to the well-foundedness constraint X . If no such cycles exist, we
conclude that (E, R) is satisfiable. Otherwise, we let Ei+1 be Ei but with the following new learnt
clauses added:
            v 1 , ve2 ) ∨ · · · ∨ ¬X (e
      • ¬X (e                         vm−1 , vem ) for each simple cycle ve1 , . . . , vem = ve1 of each X ∈ R.
We then proceed to the next iteration with Ei+1 .
  It is worth mentioning here that if R = ∅ and the original pCSP (C, R) is unsatisfiable, there
always exists an unsatisfiable finite set E of example instances of C. However, there is, in general,
no such finite witness of the unsatifiability if R , ∅. This fact also supports an advantage of our
primal-dual approach to verification based on µCLP.

6.2     Function/Predicate Synthesis with Stratified Families of Templates
We do a template-based search for a solution of the given example instances to be returned as a
candidate solution of the input pCSP⇓λ (C, R). Templates can effectively restrict the solution space
to explore and be made to satisfy the well-foundedness constraints at the same time. There however
is a trade-off between expressiveness and generalizability. With less expressive templates like
intervals, we may miss actual solutions. By contrast, with very expressive templates like polyhedra,
there could be many solutions, and a solution thus returned is liable to overfitting and therefore is
of low generalizability. That is, the solution is likely too specific to be a solution of (C, R). [Padhi
et al. 2019] discusses a similar overfitting problem in the context of grammar-based synthesis.
   Our remedy to the problem is to use stratified families of predicate templates that have been used
in prior work to guarantee the convergence of counterexample-guided refinement iterations [Jhala
and McMillan 2006; Terauchi and Unno 2015]. Initially, we assign each predicate variable a less
expressive template and gradually refine it in a counterexample-guided manner: we try to find a
solution expressible in the current templates and if no solution is found, we generate and analyze
an unsat core of the constraint over the unknown parameters of the templates to identify the
parameters of the families of templates that are necessary to be updated.

6.2.1 Stratified Families of Templates. We have designed three stratified families of templates re-
spectively for (1) ordinary predicates, (2) (non-predicate) functions, and (3) well-founded predicates.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                17


  (1) For ordinary predicates X ∈ (fpv(C) \ R), the stratified family of templates TX• (nd, nc, ac, ad)
      and its accompanying constraint ϕ X• (nd, nc, ac, ad) are defined as:
                                                                               Íar(X )
         TX• (nd, nc, ac, ad) ≜ λ(x 1 , . . . , x ar(X ) ). i=1  j=1 c i, j,0 + k =1 c i, j,k · x k ≥ 0
                                                           Ônd Ónc
                                 Ónd Ónc Íar(X )
         ϕ X• (nd, nc, ac, ad) ≜    i=1     j=1 k =1 |c i, j,k | ≤ ac ∧ |c i, j,0 | ≤ ad
      Here, c i, j,k ’s are fresh unknown parameters to be inferred. Note that the parameter nd (resp.
      nc) is the number of disjuncts (resp. conjuncts) and the parameter ac is the upper bound of
      the sum of the absolute value of coefficients c i, j,k (k > 0) of the variables. The parameter ad
      is the upper bound of the absolute value of constant term c i, j,0 .
  (2) For (non-predicate) functions F ∈ (ffv(C)\fpv(C)), we define the stratified family of templates
      TFλ (nd, nc, dc, dd, ec, ed) and its accompanying constraint ϕ Fλ (nd, nc, dc, dd, ec, ed) as:
           TFλ (nd, nc, dc, dd, ec, ed)        ≜      x ).t 1 (e
                                                    λ(e        x)
                                                     Ónd Íar(X )−1
                                                        i=1 j=1       |c i, j | ≤ ec ∧ |c i,0 | ≤ ed ∧
           ϕ Fλ (nd, nc, ec, ed, dc, dd)       ≜     Ónd−1 Ó      nc Íar(X )−1 ′
                                                        i=1       j=1 k =1       |c i, j,k | ≤ dc ∧ |c i,′ j,0 | ≤ dd
         where
   t nd (e
         x ) ≜ e nd (e
                     x ),                         ti (e
                                                      x)       ≜    ITE(D i (e x ), ei (e          x )) (for 1 ≤ i < nd),
                                                                                        x ), ti+1 (e
                        Íar(X )−1                                                     Íar(X )−1 ′
         x ) ≜ c i,0 + j=1        c i, j · x j , D i (e               j=1 c i, j,0 + k =1
                                                                    Ónc ′
     ei (e                                            x)       ≜                                   c i, j,k · x k ≥ 0.
      Here, c i, j ’s and c i,′ j,k ’s are fresh unknown parameters to be inferred. TFλ characterizes a
      piecewise-defined affine function with discriminators D 1 , . . . , D nd−1 and branch expressions
      e 1 , . . . , e nd . The parameter nc is the number of conjuncts in each discriminator. The parameters
      dc, dd, ec, ed are the upper bounds similar to ac, ad for TX• . Note that for any substitution θ
      for the unknown parameters in TFλ , θ (TFλ ) represents a total function.
  (3) For well-founded predicates X ∈ R, the stratified family of templatesTX⇓ (nl, np, nc, rc, rd, dc, dd)
      and its accompanying constraint ϕ X⇓ (nl, np, nc, rc, rd, dc, dd) are defined as:
                                                           Ó Ó                           
                                                              nl   np
                                                                         r i, j (e
                                                                                 x ) ≥  0    ∧
                                                           Ói=1 Ôj=1                 Ó Ô                           
        ⇓                                                          np                                   np
     TX (nl, np, nc, rc, rd, dc, dd) ≜ λ(e        x , ye).    nl
                                                              i=1   j=1 D i, j (e  x) ∧         nl
                                                                                                i=1     j=1 D i, j (e
                                                                                                                    y) ∧
                                                           Ô                                                   
                                                              nl
                                                                           ,                              ,
                                                                                     Ói−1
                                                              i=1 GT i (e
                                                                        x    y
                                                                             e  )  ∧   ℓ=1  GEQ      ℓ (e
                                                                                                        x   y
                                                                                                            e )
                                                 Ónl Ónp Íar(X )
                                                           j=1 k =1   |c i, j,k  | ≤ rc  ∧  |c i, j,0 | ≤ rd ∧
     ϕ X⇓ (nl, np, nc, rc, rd, dc, dd) ≜            i=1
                                                 Ónl Ónp      Ónc Íar(X ) ′                                 ′
                                                    i=1    j=1 k =1 l =1 |c i, j,k,l | ≤ dc ∧ |c i, j,k,0 | ≤ dd

       where
                                   Ônp                       Ónp
                     x , ye)                                                                     x ) > r i,k (e
                                                                                                                 
               GT i (e           ≜     j=1  D i, j (e
                                                    x ) ≥ 0 ∧ k=1 D i,k (e     y ) ≥ 0 ⇒ r i, j (e            y)
                                   Ônp                       Ónp
                     x , ye)
                                                                                                                 
              GEQi (e            ≜     j=1 D i, j (ex ) ≥ 0 ∧ k=1 D i,k (e     y ) ≥ 0 ⇒ r i, j (e
                                                                                                 x ) ≥ r i,k (e
                                                                                                              y)
                                                         Íar(X )/2 ′
                                       k =1 c i, j,k,0 + l =1
                                   Ónc ′
                 D i, j (e
                         x)      ≜                                c i, j,k,l · xl ≥ 0
                                               Íar(X )/2
                    r i, j (e
                            x)   ≜ c i, j,0 + k =1 c i, j,k · x k

       Here, c i, j,k ’s and c i,′ j,k,l ’s are fresh unknown parameters to be inferred. TX⇓ represents the
       well-founded relation induced by the nl-lexicographic np-piecewise-defined affine ranking
       function where r i, j are the affine ranking function template for the j-th region specified by
       the discriminator D i, j of the i-th lexicographic component. The parameters rc, rd, dc, dd are
       the upper bounds similar to ac, ad for TX• . The first conjunct of TX⇓ asserts that the return
       value of all the affine ranking functions is non-negative and the second conjunct asserts
18                                                         Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


       that the discriminators cover all the reachable states. Note that discriminators can overlap
       and for such an overlapping region, the maximum return value of the ranking functions
       is used. In the third conjunct, GT i (e x , ye) (resp. GEQi (e
                                                                    x , ye)) means that the return value of
       the piecewise-defined affine ranking function of i-th lexicographic component strictly (resp.
       non-strictly) decreases from xe to ye. It follows that for any substitution θ for the unknown
       parameters in TX⇓ , θ (TX⇓ ) represents a well-founded relation.
 6.2.2 Template-based Synthesis. For each function variable F , let ty(F ) = • if F is ordinary predicate,
 ty(F ) = λ if it is (non-predicate) function, and ty(F ) = ⇓ if it is well-founded predicate. Let
pe ∈ Zn where n is the number of parameters summed across all templates, and let TFα (e                              p ) and
ϕ αF (e
      p ) (for α ∈ {•, λ, ⇓}) project the corresponding parameters. Each pe ∈ Zn induces a solution
                                                                                              ty(F )
 space Je  p K ≜ {T (e p )[θ ] | θ |= Con(e       p )} where T (e
                                                                p )[θ ] ≜ {F 7→ θ (TF (e             p )) | F ∈ ffv(C)} and
               Ó            ty(F )
 Con(e p ) ≜ F ∈ffv(C) ϕ F (e      p ).
    Let pe1 ≤ pe2 be the point-wise ordering. Note that Je            p K is a finite set for any pe ∈ Zn , and pe1 ≤ pe2
 implies Je   p1 K ⊆ Jep2 K. We start the CEGIS process with some small initial parameters pe(0) (i.e.,
 the parameters will be maintained as a global state of the CEGIS process). At each iteration, we
 try to find a candidate solution to the given examples (E, R) in Je                    p (i) K where pe(i) are the current
 parameters. This is done by using an off-the-shelf SMT solver for QFLIA to find θ satisfying
       p (i) )[θ ](E) ∧ θ (Con(e  p (i) )). If such θ is found, we return T (e   p (i) )[θ ] as the candidate solution for
 Ó
    T (e
 the outer CEGIS process. Otherwise, we update the parameters to some pe(i+1) > pe(i) such that
  p (i+1) K contains a solution for (E, R). Here, we do the update in a fair manner, that is, in any
 Je
 infinite series of updates pe(0) , pe(1) , . . . , every parameter is updated infinitely often (the details are
 deferred to below). Because of the progress property of our CEGIS procedure (cf. Section 6) and
 the fact that every Je    p K is finite, this ensures that every parameter is updated infinitely often in an
 infinite series of CEGIS iterations. We thus obtain the following property.

   Theorem 6.1. Our CEGIS-procedure based on stratified families of templates is relatively complete:
                        p K such that σ is a syntactic solution of the given pCSP⇓λ (C, R), a syntactic
if there is pe and σ ∈ Je
             ′
solution σ of (C, R), which could be different from σ , is eventually found by the procedure.

                                                                                           p (i) )[θ ](E)∧
                                                                                      Ó
6.2.3 Updating Template Parameters via Unsat Cores. In above, when the constraint T (e
θ (Con(e (i)
        p )) has no solution (and thus Je   (i)
                                           p K has no solution to the examples), we analyze the unsat
core of the constraint to obtain the parameters that have caused the failure. Note here that there
could be a dependency between function/predicate variables and in such a case our unsat core
analysis enumerates all the involved function/predicate variables and we obtain the parameters of
the templates for all of them. We then increment these parameters in a fair manner, by limiting the
maximum differences between different parameters to some finite threshold, and repeatedly solve
the resulting constraint until a solution is found.

7    EVALUATION
To evaluate the presented verification framework, we have implemented:
     • PCSat, a satisfiability checking tool for pCSP⇓λ based on stratified CEGIS.
     • MuVal, a validity checking tool for µCLP based on the reduction algorithm presented in
       Section 5 and the satisfiability checker PCSat.
PCSat supports the theory of Booleans and the quantifier-free theory of linear inequalities over
integers/rationals. The tools are implemented in OCaml, using Z3 [de Moura and Bjørner 2008]
and MiniSat [Eén and Sörensson 2004] as the backend SMT and SAT solvers, respectively.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                     19


  We compare PCSat with the state-of-the-art SyGuS (syntax-guided synthesis) solver LoopIn-
vGen [Padhi et al. 2019] which is the winner of the Inv Track of SyGuS-Comp 2018. We also compare
with the state-of-the-art CHCs solvers HoIce [Champion et al. 2018] and SPACER [Gurfinkel et al.
2015]. We run the tools on the following benchmark sets:
  (a) SyGuS-Comp 2018 (Invariant Synthesis Track).
  (b) CHC-COMP 2019 (LIA-nonlin Track) for CHCs over the theory of QFLIA.
We remark that the SyGuS benchmarks only contain linear CHCs with each constraint set containing
only a single predicate variable. To compare, we have selected non-linear instances from CHC-
COMP.
   We have also tested MuVal on the benchmark sets below encoded as µCLP and compared the
results with Mu2CHC [Kobayashi et al. 2019], which is a recently proposed tool for solving fixpoint
logic constraints:
 (c1) The standard benchmark set for CTL verification (small) [Cook and Koskinen 2013].
 (c2) The standard benchmark set for CTL verification (industrial) [Cook and Koskinen 2013].
  (d) The benchmark set of Mu-Arithmetic (i.e., µCLP restricted to integer arithmetic) [Kobayashi
      et al. 2019] which consists of some properties of integer arithmetic encoded in Mu-Arithmetic
      (Problems 1–6), linear-time temporal properties of first-order functional programs encoded
      by a translation in [Kobayashi et al. 2019] (Problems 7–22), branching-time temporal proper-
      ties (some are only expressible in CTL* or modal-µ) of imperative programs encoded by a
      translation similar to one in [Watanabe et al. 2019] (Problems 23–28).
  (e) The termination verification benchmark set for FuncTion.7
All experiments have been conducted on 3.1GHz Intel Xeon Platinum 8000 CPU and 32 GiB RAM
with the time limit of 300 seconds.
   The experimental results except (b) are summarized in Figure 1. The cactus plot (left) compares
the results of PCSat on (a) with those of HoIce, SPACER, and LoopInvGen. For the number of
solved instances, PCSat obtained comparable results with LoopInvGen [Padhi et al. 2019]: PCSat
(denoted “Stratified”) solved 113 SAT and 8 UNSAT instances while LoopInvGen solved 116 SAT
and 5 UNSAT instances. PCSat obtained better results than the highly-tuned CHCs solvers HoIce
(109 SAT, 9 UNSAT, and 2 wrong answers) and SPACER (101 SAT and 9 UNSAT). PCSat however
is often slower compared to the other mature tools. This is partly because PCSat does not use
incremental SMT solving across CEGIS iterations and therefore becomes significantly slower as the
number of example instances grows. This inefficiency caused PCSat to obtain suboptimal results on
(b) the CHC-COMP benchmarks: PCSat solved 97 SAT and 55 UNSAT instances while HoIce solved
123 SAT and 79 UNSAT, and SPACER solved 147 SAT and 117 UNSAT instances. From our analysis
of the failed runs, we found that PCSat often failed to solve CHCs containing multiple Boolean
variables. This is because the current version of PCSat naively generates 2n -copies of templates
over integer variables for each Boolean valuation where n is the number of Boolean variables in
CHCs. We plan to design improved families of templates for Boolean variables. Though it is rather
out of the scope of this paper, we believe this dramatically improves the experiment results because
most benchmarks from (b) have multiple Boolean variables. Also, we found that PCSat is general
but not well-tuned for proving the unsatisfiability when applied to the subclass CHCs of pCSP⇓λ .
We could exploit the restricted (i.e. Horn) form of constraints for efficiently finding a resolution
derivation of the contradiction via SLD-resolution.
   The cactus plot (left) also shows the trade-off between expressiveness and generalizability of
templates. Interval, Octagon, Octahedron, and Polyhedron are PCSat restricted to use respective
7 https://www.di.ens.fr/~urban/FuncTion.html
20                                                                 Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen



                    250                                                                                                   Timeout (300 sec)


                                 Stratified
                                 Interval
                                 Octagon                                                  100
                    200          Octahedron
      Time in seconds




                                 Polyhedron
                                 LoopInvGen
                    150          Hoice                                                     10

                                 Spacer




                                                                                 Mu2CHC
                    100                                                                     1




                        50
                                                                                           0.1



                        0
                             0       20       40   60   80   100     120                  0.01

                                   Benchmarks passed (of 127)                                    0.01   0.1   1
                                                                                                                  MuVal
                                                                                                                            10                100




Fig. 1. Experimental results of PCSat on the benchmarks from SyGuS-Comp 2018 (Inv Track) com-
pared with LoopInvGen, HoIce, SPACER (left) and MuVal on various µCLP benchmarks compared with
Mu2CHC [Kobayashi et al. 2019] (right)



fixed predicate templates, and the plot shows that they obtained significantly worse results compared
to PCSat with stratified families of templates. Also note that the results with the Polyhedron and
the Interval templates are even worse than those of the Octahedron and the Octagon templates.
We believe that these results show that the Polyhedron templates suffer from the overfitting
problem [Padhi et al. 2019] due to their high expressiveness, while the Interval templates suffer
from their low expressiveness.
   The scatter plot (right) in Figure 1 compares the results of MuVal on (c1), (c2), (d), and (e) with
those of Mu2CHC: MuVal solved 76 VALID and 72 INVALID instances (out of 159 instances) and
Mu2CHC solved 74 VALID and 74 INVALID instances. MuVal failed to solve 5 temporal verification
benchmarks from (c2) and (d) that were solved by Mu2CHC. We believe that this is because the
highly-tuned invariant synthesis engine (i.e., SPACER and HoIce) used in Mu2CHC worked better
for the benchmarks. By contrast Mu2CHC failed to solve 5 termination verification benchmarks
that were solved by MuVal, which require synthesis of piecewise-defined and/or lexicographic
affine ranking functions. We believe that this shows a limitation of the Mu2CHC approach that
separately synthesize termination arguments and inductive invariants, and cannot quickly feedback
a failure of invariant synthesis to ranking function synthesis.

8    RELATED WORK
The class of problems pCSP⇓λ that we have introduced in this paper is closely related to existentially-
quantified Horn clauses (E-CHCs) introduced in [Beyene et al. 2013]. We conjecture that pCSP⇓λ and
E-CHCs are inter-reducible, though it is not trivial to fill the gap, without changing the background
theory, between our well-foundedness and their disjunctive well-foundedness constraints and our
function variables and their existentially-quantified heads. We believe inter-reducibility is often a
desirable feature: even though DFAs and regular expressions are inter-reducible, each format has
its own benefits. In our case, for instance, having the direct support for general disjunctions in
pCSP can be advantageous compared to encoding them indirectly by existentials in E-CHCs. In
particular, general disjunctions can be handled by PCSat without any additional twist, and can be
used to completely encode branching-time temporal properties verification problems of imperative
programs with finitely-bounded non-determinism, for which existential quantifications in E-CHCs
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                          21


and function variables in pCSP⇓λ are probably overkill. Also, the class of pCSP without function
variables and well-founded predicates is closed under negation like in µCLP (cf. Remark 4). Besides
the logical beauty, the property is also useful in practice: we can mechanically compute the De
Morgal dual of the given CHCs and check the satisfiability of the primary and dual CHCs in parallel
or cooperatively. Also, it is well known that well-founded relations used in pCSP⇓λ and disjunctively
well-founded relations used in E-CHCs are both complete for termination (see [Podelski and
Rybalchenko 2004b]) but have different benefits. To solve E-CHCs, [Beyene et al. 2013] proposes
a method called E-HSF which reduces the given E-CHCs to (ordinary) CHCs by synthesizing
candidate witnesses for existentially quantified variables iteratively in a counterexample-guided
manner. The generated CHCs are then solved (possibly itself via a counterexample-guided iteration)
by an off-the-shelf CHCs solver. By contrast, our method, while also based on counterexample-
guided iteration, reduces the problem to quantifier-free SMT solving by simultaneously synthesizing
candidate invariants, well-founded relations, and quantifier witnesses. We believe that there are two
advantages to our approach. One is that the simultaneous synthesis facilitates finding candidates
that depend amongst each other, for instance, well-founded relations that depend on quantifier
witnesses, by sharing useful information via faster feedbacks from synthesis failures. Another
advantage is that pCSP⇓λ can directly express non-Horn clauses whereas handling such clauses in
E-CHCs would incur introducing additional existential quantifiers.
   An extension of CLP called co-Constraint Logic Programs (co-CLP) with mixed inductive and
co-inductive predicates has been proposed in [Saeedloei and Gupta 2012]. Unlike our µCLP,
co-CLP does not support mutually recursive inductive and co-inductive predicates which are
necessary to directly express modal-µ temporal verification problems. Also related to our µCLP
is Mu-Arithmetic [Bradfield 1999; Lubarsky 1993] which is a first-order fixpoint logic of integer
arithmetic. It has recently been applied to temporal property verification in [Kobayashi et al. 2019]
where they present a method called Mu2CHC for checking the validity of formulas expressed in
the logic.8 Mu2CHC works by reducing the problem to (ordinary) CHCs. This is done by conserva-
tively approximating fixpoints by asserting some (symbolic) bound on their unfolding depths. The
resulting CHCs are then solved by an off-the-shelf CHCs solver. By contrast, our MuVal reduces
the problem to pCSP⇓λ and therefore has the advantages of simultaneous synthesis remarked
above.9 In fact, this difference resulted in the better results of MuVal on the termination verification
benchmark set that requires synthesis of lexicographc and/or piecewise-defined ranking functions
(recall discussion in Section 7). And, the completeness of the reduction to pCSP⇓λ allows MuVal to
conclude the invalidity of the original µCLP from the unsatisfiability of the reduced pCSP⇓λ unlike
Mu2CHC. Also, Mu2CHC is specialized to integer arithmetic, for example, relying on that particu-
lar domain to encode existential quantifiers as fixpoints, as explained in Remark 1. Generalizing
their method to other theories (such as the theory of reals) may require non-trivial extensions.
By contrast, MuVal is designed for the full class of µCLP which can be seen as a generalization
of Mu-Arithmetic to arbitrary first-order theories. However, we remark that both Mu2CHC and
E-HSF have an advantage over our approach in that they can utilize highly-tuned off-the-shelf
CHCs solvers. Indeed, for this reason, we have noticed that our approach is often less efficient than
theirs on (ordinary) CHCs instances.
   Our pCSP⇓λ solving technique generalizes a number of previous techniques developed for
CHCs solving and invariant/ranking function discovery. Most closely related to our work are the
data-driven approaches to solving subclasses of CHCs based on CEGIS [Solar-Lezama et al. 2006]
combined with template-based synthesis via SMT solver [Garg et al. 2014; Sharma et al. 2013b],

8 Technically, their method works on hierarchical equation systems (HES) which is a reformulation of Mu-Arithmetic.
9 In fact, Mu2CHC has no feedback from CHCs solving to fixpoints approximation.
22                                               Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


greedy set covering with logic minimization [Padhi et al. 2016; Sharma et al. 2013a], decision
tree learning [Champion et al. 2018; Ezudheen et al. 2018; Garg et al. 2016; Krishna et al. 2015;
Zhu et al. 2018], and grammar-based synthesis [Fedyukovich et al. 2018; Padhi et al. 2019]. Our
stratified CEGIS adopts the idea of stratified families of templates [Jhala and McMillan 2006;
Terauchi and Unno 2015]. Our approach is similar in spirit to [Padhi et al. 2019] but they use
a stratified family of grammars instead and also do not use unsat cores for updating grammars.
The idea presented in [Fedyukovich et al. 2018] of extracting grammars for enumerating ranking
functions and recurrent sets and our idea of stratifying templates are orthogonal and could be
better together. Besides the data-driven approach, various CHCs solving approaches have been
proposed: counterexample-guided abstraction refinement and Craig interpolation [Hojjat and
Rümmer 2018; Unno and Kobayashi 2009], generalized property directed reachability [Hoder and
Bjørner 2012; Komuravelli et al. 2014], constraint specialization [Angelis et al. 2014; Kafle et al.
2016], and inductive theorem proving [Unno et al. 2017b]. A number of existing techniques for
program verification can be applied straightforwardly to invariant synthesis for linear CHCs and
ranking function synthesis. Some use templates for invariants [Colón et al. 2003; Sankaranarayanan
et al. 2004] and ranking functions [Leike and Heizmann 2014] but many of them involve costly
non-linear constraint solving. RankFinder [Podelski and Rybalchenko 2004a] synthesizes linear
ranking functions via linear constraint solving. However, none of the above methods can be used
to solve the full class of pCSP⇓λ .

9    CONCLUSION
We have introduced the class µCLP of constraint logic programs with arbitrarily nested inductive
and co-inductive predicates and the class pCSP⇓λ of predicate constraint satisfaction problems
that generalizes CHCs with arbitrary clauses, function variables, and well-foundedness constraints.
We have then established a program verification framework based on µCLP by showing that (1)
µCLP can naturally encode various classes of verification problems, (2) the validity of µCLP can
be reduced to the satisfiability of pCSP⇓λ , and (3) existing CHCs solving and invariants/ranking
function synthesis techniques can be adopted to pCSP⇓λ solving and further improved with the
idea of stratified CEGIS for simultaneously achieving relative completeness (Theorem 6.1) and
practical effectiveness (Figure 1, left).
   Though we presented a sound and complete reduction from µCLP to pCSP⇓λ and the classes
of CHCs and co-CHCs correspond to fragments of µCLP as discussed in Remark 4, any µCLP is
reduced to the satisfiability of a co-CHCs⇓λ that is a strict syntactic fragment of pCSP⇓λ and recent
semantic results based on the recursion theory [Tsukada 2020] imply that the full class of pCSP⇓λ is
strictly more expressive than µCLP, meaning that the full class of pCSP⇓λ is not necessary for the
validity of µCLP. It would thus be interesting to investigate the potential of the full class of pCSP⇓λ
in practice and to find some (non-syntactic) restriction that would capture the full class of µCLP.
   To further widen the applicability of our framework, we plan to extend our tools MuVal and
PCSat to support other first-order theories beyond LIA/LRA such as arrays, algebraic data types
(ADTs), and heaps [Duck et al. 2013]. As far as the semantics of µCLP is concerned, there is no
issue with the background theory being incomplete (i.e., undecidable). However, the constraint
solving method may require non-trivial extensions to support the above theories because it involves
designing appropriate stratified families of templates. For example, certificates (i.e., invariants,
ranking functions, witnesses for quantifiers) over arrays often require quantifiers, and those over
heaps and ADTs often require inductive predicates. Future work also includes extensions of the
framework to higher-order predicates and probabilities. The former extension is useful for precisely
analyzing higher-order recursive functions (cf. HoCHC [Burn et al. 2018] and HFL(Z) [Kobayashi
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                23


et al. 2018; Watanabe et al. 2019]). The latter extension is for reasoning about programs and systems
that exhibit uncertain or probabilistic behaviors (cf. PCHC [Albarghouthi 2017]).

REFERENCES
Aws Albarghouthi. 2017. Probabilistic Horn Clause Verification. In SAS ’17. Springer, 1–22.
Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2014. VeriMAP: A tool for verifying
    programs through transformations. In TACAS ’14. Springer, 568–574.
Tewodros Beyene, Swarat Chaudhuri, Corneliu Popeea, and Andrey Rybalchenko. 2014. A Constraint-based Approach to
    Solving Games on Infinite Graphs. In POPL ’14 (San Diego, California, USA). ACM, 221–233.
Tewodros A. Beyene, Corneliu Popeea, and Andrey Rybalchenko. 2013. Solving Existentially Quantified Horn Clauses. In
    CAV ’13 (LNCS), Vol. 8044. Springer, 869–882.
Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. 2015. Horn Clause Solvers for Program
    Verification. In Fields of Logic and Computation II: Essays Dedicated to Yuri Gurevich on the Occasion of His 75th Birthday
    (LNCS), Vol. 9300. Springer, 24–51.
Marijke H. L. Bodlaender, Cor A. J. Hurkens, Vincent J. J. Kusters, Frank Staals, Gerhard J. Woeginger, and Hans Zantema.
    2012. Cinderella versus the Wicked Stepmother. In IFIP TCS. 57–71.
Julian C. Bradfield. 1999. Fixpoint Alternation and the Game Quantifier. In CSL ’99 (LNCS), Vol. 1683. Springer, 350–361.
J. Richard Buchi and Lawrence H. Landweber. 1969. Solving Sequential Conditions by Finite-State Strategies. Trans. Amer.
    Math. Soc. 138 (1969), 295–311.
Toby Cathcart Burn, C.-H. Luke Ong, and Steven J. Ramsay. 2018. Higher-order constrained horn clauses for verification.
    PACMPL 2, POPL (2018), 11:1–11:28.
Adrien Champion, Tomoya Chiba, Naoki Kobayashi, and Ryosuke Sato. 2018. ICE-Based Refinement Type Discovery for
    Higher-Order Functional Programs. In TACAS ’18 (LNCS), Vol. 10805. Springer, 365–384.
Michael A. Colón, Sriram Sankaranarayanan, and Henny B. Sipma. 2003. Linear Invariant Generation Using Non-linear
    Constraint Solving. In CAV ’03 (Chennai, India) (LNCS), Vol. 2725. Springer, 420–432.
Byron Cook, Heidy Khlaaf, and Nir Piterman. 2015. On Automation of CTL* Verification for Infinite-State Systems. In CAV
    ’15. Springer, 13–29.
Byron Cook and Eric Koskinen. 2011. Making Prophecies with Decision Predicates. In POPL ’11 (Austin, Texas, USA). ACM,
    399–410.
Byron Cook and Eric Koskinen. 2013. Reasoning About Nondeterminism in Programs. In PLDI ’13 (Seattle, Washington,
    USA). ACM, 219–230.
Byron Cook, Eric Koskinen, and Moshe Vardi. 2011. Temporal Property Verification As a Program Analysis Task. In CAV ’11
    (Snowbird, UT). Springer, 333–348.
Byron Cook, Andreas Podelski, and Andrey Rybalchenko. 2006. Termination proofs for systems code. In PLDI ’06. ACM,
    415–426.
Byron Cook, Abigail See, and Florian Zuleger. 2013. Ramsey vs. Lexicographic Termination Proving. In TACAS ’13 (LNCS),
    Vol. 7795. Springer, 47–61.
Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In TACAS ’08 (Budapest, Hungary, March29 –
    April 6) (LNCS), Vol. 4963. Springer, 337–340.
Daniel Dietsch, Matthias Heizmann, Vincent Langenfeld, and Andreas Podelski. 2015. Fairness Modulo Theory: A New
    Approach to LTL Software Model Checking. In CAV ’15. Springer, 49–66.
Gregory J. Duck, Joxan Jaffar, and Nicolas C. H. Koh. 2013. Constraint-Based Program Reasoning with Heaps and Separation.
    In CP ’13. Springer, 282–298.
Niklas Eén and Niklas Sörensson. 2004. An Extensible SAT-solver. In SAT ’04. Springer, 502–518.
P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg, and P. Madhusudan. 2018. Horn-ICE Learning for Synthesizing
    Invariants and Contracts. Proc. ACM Program. Lang. 2, OOPSLA, Article 131 (Oct. 2018), 25 pages.
Azadeh Farzan and Zachary Kincaid. 2017. Strategy Synthesis for Linear Arithmetic Games. Proc. ACM Program. Lang. 2,
    POPL, Article 61 (Dec. 2017), 30 pages.
Grigory Fedyukovich, Yueling Zhang, and Aarti Gupta. 2018. Syntax-Guided Termination Analysis. In CAV ’18 (LNCS),
    Vol. 10981. Springer, 124–143.
Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. 2014. ICE: A Robust Framework for Learning Invariants.
    In CAV ’14. Springer, 69–87.
Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. 2016. Learning Invariants Using Decision Trees and Implication
    Counterexamples. In POPL ’16 (St. Petersburg, FL, USA). ACM, 499–512.
Erich Grädel, Wolfgang Thomas, and Thomas Wilke (Eds.). 2002. Automata, Logics, and Infinite Games: A Guide to Current
    Research. LNCS, Vol. 2500. Springer.
24                                                        Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. 2012. Synthesizing Software Verifiers
   from Proof Rules. In PLDI ’12 (Beijing, China). ACM, 405–416.
Ashutosh Gupta, Thomas A. Henzinger, Rupak Majumdar, Andrey Rybalchenko, and Ru-Gang Xu. 2008. Proving non-
   termination. In POPL ’08 (San Francisco, California, USA). ACM, 147–158.
Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. 2015. The SeaHorn Verification Framework.
   In CAV ’15. Springer, 343–361.
Kryštof Hoder and Nikolaj Bjørner. 2012. Generalized Property Directed Reachability. In SAT ’12 (Trento, Italy). Springer,
   157–171.
Hossein Hojjat and Philipp Rümmer. 2018. The Eldarica Horn Solver. In FMCAD ’18. IEEE.
Antonius J.C. Hurkens, Cor A.J. Hurkens, and Gerhard J. Woeginger. 2011. How Cinderella won the bucket game (and lived
   happily ever after). Mathematics Magazine 84, 4 (2011), 278–283.
Joxan Jaffar and Michael J. Maher. 1994. Constraint logic programming: a survey. The Journal of Logic Programming 19
   (1994), 503 – 581.
Ranjit Jhala, Rupak Majumdar, and Andrey Rybalchenko. 2011. HMC: verifying functional programs using abstract
   interpreters. In CAV ’11 (Snowbird, UT) (LNCS), Vol. 6806. Springer, 470–485.
Ranjit Jhala and Kenneth L. McMillan. 2006. A Practical and Complete Approach to Predicate Refinement. In TACAS ’06
   (LNCS), Vol. 3920. Springer, 459–473.
Donald B. Johnson. 1975. Finding All the Elementary Circuits of a Directed Graph. SIAM J. Comput. 4 (1975), 77–84.
Bishoksan Kafle, John P Gallagher, and José F Morales. 2016. RAHFT: A tool for verifying Horn clauses using abstract
   interpretation and finite tree automata. In CAV ’16. Springer, 261–268.
Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Martin Schäf. 2016. JayHorn: A Framework for Verifying Java
   programs. In CAV ’16, Vol. 9779. Springer, 352–358.
Naoki Kobayashi, Takeshi Nishikawa, Atsushi Igarashi, and Hiroshi Unno. 2019. Temporal Verification of Programs via
   First-Order Fixpoint Logic. In SAS ’19. Springer, 413–436.
Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2011. Predicate abstraction and CEGAR for higher-order model checking.
   In PLDI ’11 (San Jose, California, USA). ACM, 222–233.
Naoki Kobayashi, Takeshi Tsukada, and Keiichi Watanabe. 2018. Higher-Order Program Verification via HFL Model Checking.
   In ESOP ’18. Springer, 711–738.
Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2014. SMT-Based Model Checking for Recursive Programs. In CAV
   ’14 (LNCS), Vol. 8559. Springer, 17–34.
Eric Koskinen and Tachio Terauchi. 2014. Local Temporal Reasoning. In CSL-LICS ’14 (Vienna, Austria). ACM, Article 59,
   10 pages.
Siddharth Krishna, Christian Puhrsch, and Thomas Wies. 2015. Learning Invariants using Decision Trees. CoRR
   abs/1501.04725 (2015). arXiv:1501.04725 http://arxiv.org/abs/1501.04725
Takuya Kuwahara, Tachio Terauchi, Hiroshi Unno, and Naoki Kobayashi. 2014. Automatic Termination Verification for
   Higher-Order Functional Programs. In ESOP ’14 (LNCS), Vol. 8410. Springer, 392–411.
Jan Leike and Matthias Heizmann. 2014. Ranking Templates for Linear Loops. In TACAS ’14 (LNCS), Vol. 8413. Springer,
   172–186.
Robert S. Lubarsky. 1993. µ-Definable Sets of Integers. Journal of Symbolic Logic 58, 1 (1993), 291–313.
Akihiro Murase, Tachio Terauchi, Naoki Kobayashi, Ryosuke Sato, and Hiroshi Unno. 2016. Temporal Verification of
   Higher-order Functional Programs. In POPL ’16 (St. Petersburg, FL, USA). ACM, 57–68.
Yoji Nanjo, Hiroshi Unno, Eric Koskinen, and Tachio Terauchi. 2018. A Fixpoint Logic and Dependent Effects for Temporal
   Property Verification. In LICS ’18. ACM, 759–768.
Saswat Padhi, Todd D. Millstein, Aditya V. Nori, and Rahul Sharma. 2019. Overfitting in Synthesis: Theory and Practice. In
   CAV ’19 (LNCS), Vol. 11561. Springer, 315–334.
Saswat Padhi, Rahul Sharma, and Todd D. Millstein. 2016. Data-Driven Precondition Inference with Learned Features. In
   PLDI ’16. 42–56.
Amir Pnueli and Roni Rosner. 1989. On the Synthesis of a Reactive Module. In POPL ’89. 179–190.
Andreas Podelski and Andrey Rybalchenko. 2004a. A Complete Method for the Synthesis of Linear Ranking Functions. In
   VMCAI ’04 (LNCS), Vol. 2937. Springer, 239–251.
Andreas Podelski and Andrey Rybalchenko. 2004b. Transition Invariants. In LICS ’04. IEEE, 32–41.
Neda Saeedloei and Gopal Gupta. 2012. Coinductive Constraint Logic Programming. In FLOPS ’12. Springer, 243–259.
Davide Sangiorgi. 2011. Introduction to Bisimulation and Coinduction. Cambridge University Press.
Sriram Sankaranarayanan, Henny B. Sipma, and Zohar Manna. 2004. Non-linear loop invariant generation using Gröbner
   bases. In POPL ’04 (Venice, Italy). ACM, 318–329.
Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, Percy Liang, and Aditya V. Nori. 2013b. A data driven
   approach for algebraic loop invariants. In ESOP ’13 (Rome, Italy) (LNCS), Vol. 7792. Springer, 574–592.
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                           25


Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, and Aditya V. Nori. 2013a. Verification as Learning Geometric
   Concepts. In SAS ’13. Springer, 388–411.
Armando Solar-Lezama, Liviu Tancau, Rastislav Bodik, Sanjit Seshia, and Vijay Saraswat. 2006. Combinatorial Sketching
   for Finite Programs. In ASPLOS XII (San Jose, California, USA). ACM, 404–415.
Tachio Terauchi. 2010. Dependent types from counterexamples. In POPL ’10 (Madrid, Spain). ACM, 119–130.
Tachio Terauchi and Hiroshi Unno. 2015. Relaxed Stratification: A New Approach to Practical Complete Predicate Refinement.
   In ESOP ’15 (LNCS), Vol. 9032. Springer, 610–633.
Wolfgang Thomas. 1995. On the Synthesis of Strategies in Infinite Games. In STACS ’95. 1–13.
Takeshi Tsukada. 2020. On Computability of Logical Approaches to Branching-Time Property Verification of Programs. In
   LICS’20 (To appear).
Hiroshi Unno and Naoki Kobayashi. 2009. Dependent Type Inference with Interpolants. In PPDP ’09 (Coimbra, Portugal).
   ACM, 277–288.
Hiroshi Unno, Yuki Satake, and Tachio Terauchi. 2017a. Relatively Complete Refinement Type System for Verification of
   Higher-order Non-deterministic Programs. Proc. ACM Program. Lang. 2, POPL, Article 12 (Dec. 2017), 29 pages.
Hiroshi Unno, Sho Torii, and Hiroki Sakamoto. 2017b. Automating Induction for Solving Horn Clauses. In CAV ’17. Springer,
   571–591.
Caterina Urban. 2013. The Abstract Domain of Segmented Ranking Functions. In SAS ’13. Springer, 43–62.
Caterina Urban and Antoine Miné. 2014. An Abstract Domain to Infer Ordinal-Valued Ranking Functions. In ESOP ’14.
   Springer, 412–431.
Keiichi Watanabe, Takeshi Tsukada, Hiroki Oshikawa, and Naoki Kobayashi. 2019. Reduction from Branching-Time Property
   Verification of Higher-Order Programs to HFL Validity Checking. In PEPM ’19. ACM.
He Zhu, Stephen Magill, and Suresh Jagannathan. 2018. A Data-driven CHC Solver. In PLDI ’18 (Philadelphia, PA, USA).
   ACM, 707–721.
He Zhu, Aditya V. Nori, and Suresh Jagannathan. 2015. Learning Refinement Types. In ICFP ’15 (Vancouver, BC, Canada).
   ACM, 400–411.


A     EXPRESSING VERIFICATION PROBLEMS IN µCLP
We now consider a variety of verification problems, showing that each of them can be expressed
as validity in µCLP. Specifically, we discuss applications of µCLP to bisimulation and bisimilarity
verification in Appendix A.1 and infinite state and infinite duration two player game solving in
Appendix A.2.

A.1    Bisimulation and Bisimilarity Verification
Bisimulation and bisimilarity are a prototypical application of greatest fixpoint and co-induction in
computer science [Sangiorgi 2011]. We show that the notions and various problems thereof can be
naturally expressed in our framework.
  Given two LTS M 1 and M 2 with L = L M1 = L M2 , the bisimilarity relation BisimM1, M2 between M 1
and M 2 can be defined in µCLP as follows:

                        x 1 , xe2 ) =ν
           BisimM1, M2 (e
                                        ℓ                      ℓ
                               y1 .⟨e                 y2 .⟨e                             y1 , ye2 )
                Ó
                   ℓ ∈L ∀e          x1⟩ →
                                        − M1 ⟨e
                                              y1 ⟩ ⇒ ∃e    x2⟩ →
                                                               − M2 ⟨e
                                                                     y2 ⟩ ∧ BisimM1, M2 (e
                                           ℓ                           ℓ
                               y2 .⟨e
                             ∧∀e    x2⟩ →
                                        − M2 ⟨e       y1 .⟨e
                                              y2 ⟩ ⇒ ∃e    x1⟩ →
                                                               − M1 ⟨e                   y1 , ye2 )
                                                                     y1 ⟩ ∧ BisimM1, M2 (e

Note that the equation defines BisimM1, M2 (e  x 1 , xe2 ) as a greatest fixpoint. A basic problem of in-
terest in bisimulation is deciding whether two (concrete) states, say n       e1 ∈ S M1 and ne2 ∈ S M2 , are
bisimilar. This is expressed in our logic by the formula BisimM1, M2 (e       n1, n
                                                                                  e2 ). More generally, we
may be interested in knowing if every pair of states xe1 ∈ S M1 and xe2 ∈ S M2 satisfying ϕ(e       x 1 , xe2 )
are bisimilar, where ϕ is some property on pairs of states. This can be expressed by the formula
  x 1 , xe2 ) ⇒ BisimM1, M2 (e
ϕ(e                          x 1 , xe2 ).
   Such queries are instances of checking if a formula is a lower-bound of a greatest fixpoint formula,
and can be solved by our constraint solving method described in Sections 5 and 6. As we shall show
26                                                                      Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


there, our technique for solving such a constraint corresponds to the well-known technique of
proof by co-induction.
   While co-induction can be used to prove lower-bounds of greatest fixpoints, a different, new
technique is required to prove their upper-bounds. For instance, suppose that we wish to check
if all bisimilar pairs of states satisfy a certain property, say ψ . The query can be expressed in our
logic by: BisimM1, M2 (ex 1 , xe2 ) ⇒ ψ (e
                                         x 1 , xe2 ). Solving such greatest-fixpoint upper-bound queries are
beyond the scope of previous methods. Nonetheless, our method is able to solve them by use of
well-founded relations as we show in Sections 5 and 6.
   Next, we instantiate the above with a concrete instance. Let us consider a concrete LTS M with
labels L M = {+, −}, states S M = Z2 , and the following transition relation:
                                                             +
                                                          → ⟨x + 1, y⟩ if x + 1 ≤ y
                                                   ⟨x, y⟩ −
                                                          −
                                                   ⟨x, y⟩ −
                                                          → ⟨x − 1, y⟩ if x − 1 ≥ y
Let us consider BisimM, M , that is, we consider the bisimulation relating two states of the same
system M. We may then check if two states, for instance (0, 1) ∈ S M and (1, 2) ∈ S M , are bisimilar by
proving if BisimM, M (0, 1, 1, 2) is true. In this case, our method is able to do the proof by synthesizing
the co-inductive invariant BisimM, M (x 1 , y1 , x 2 , y2 ) ≜ x 1 = 0 ∧ x 2 = 1 ∧ x 3 = 1 ∧ x 4 = 2 ∨ x 1 =
1 ∧ x 2 = 1 ∧ x 3 = 2 ∧ x 4 = 2. Our method can also prove a more general property that any
states of M such that y − x is the same are bisimilar, by synthesizing the co-inductive invariant
BisimM, M (x 1 , y1 , x 2 , y2 ) ≜ y1 − x 1 = y2 − x 2 .
    Next, suppose that we wish to prove that every pair of bisimilar states (x 1 , y1 ) ∈ S M and
(x 2 , y2 ) ∈ S M satisfies y1 − x 1 = y2 − x 2 . That is, every bisimilar states of M have equal direction
and distance from x to y. The query can be expressed in our logic by the following formula:
                                         BisimM, M (x 1 , y1 , x 2 , y2 ) ⇒ y1 − x 1 = y2 − x 2
which is equivalent to
                                         y1 − x 1 , y2 − x 2 ⇒ Bisim¬M, M (x 1 , y1 , x 2 , y2 )
where Bisim¬M, M is the de Morgan dual of BisimM, M defined by:
                           x 1 , xe2 ) =µ
             Bisim¬M1, M2 (e
                                           ℓ                       ℓ
                                  y1 .⟨e                  y2 .⟨e                              y1 , ye2 ))
                                                                         y2 ⟩ ⇒ Bisim¬M1, M2 (e
                   Ô
                      ℓ ∈L ∃e          x1⟩ →
                                           − M1 ⟨e
                                                 y1 ⟩ ∧ (∀e    x2⟩ →
                                                                   − M2 ⟨e
                                                    ℓ                                  ℓ
                                     y2 .⟨e
                                   ∨∃e    x2⟩ →
                                              − M2 ⟨e        y1 .⟨e
                                                    y2 ⟩ ∧ (∀e    x1⟩ →
                                                                      − M1 ⟨e                   y1 , ye2 ))
                                                                            y1 ⟩ ⇒ BisimM1, M2 (e
As remarked above, such a “property checking” query on greatest fixpoints can be, as a result,
handled by our method by using well-founded relations. Here, our method synthesizes the in-
ductive invariant Bisim¬M, M (x 1 , y1 , x 2 , y2 ) ≜ y1 − x 1 , y2 − x 2 and the well-founded relation
Bisim¬M, M ⇓ (x 1 , y1 , x 2 , y2 , x 1′ , y1′ , x 2′ , y2′ ) ≜ r (x 1 , y1 , x 2 , y2 ) > r (x 1′ , y1′ , x 2′ , y2′ ) where r (x 1 , y1 , x 2 , y2 ) =
(y_1-x_1) + (y_2-x_2).

A.2      Infinite State and Infinite Duration Games Solving
Two-player turn-based infinite-duration games are games in which two players take turns in moving
a token along the edges of a graph. A player wins if the (infinite) sequence of nodes visited by the
token satisfies a certain condition. Classically, the games are played over a finite graph representing
the state transition diagram of a finite-state transition system, and there is a rich body of work
relating such games to the verification and synthesis of finite state systems [Grädel et al. 2002]. For
instance, in the synthesis of reactive systems [Buchi and Landweber 1969; Pnueli and Rosner 1989;
Thomas 1995], a game with two players, Sys and Env, is considered over a graph with edges from
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                27


one player’s node to the other player’s node. The edges from Sys’s nodes describe the possible
(one-step) execution choices of the system to be synthesized and those from Env’s nodes describe
the possible external inputs to the system. The goal of Sys is to satisfy the given specification (given,
e.g., by a temporal logic formula) whereas the goal of Env is to violate it. The desired system is
realizable if and only if Sys has a winning strategy.
   Recently, the line of work has been extended to infinite-state systems with which one can express
the verification and synthesis problems for infinite-state systems [Beyene et al. 2014; Farzan and
Kincaid 2017]. We show that our framework is expressive enough to express such infinite-state
infinite-duration games. Following the literature [Beyene et al. 2014; Farzan and Kincaid 2017], we
consider three classes of games: Safety games, Reachability games, and LTL games.10
   Each game is played over a graph formed by a LTS. Specifically, we consider a LTS of the form
M = (S,T , L A ∪ L E ) where L A ∩ L E = ∅, that is, the labels are partitioned into L A and L E . For each
                                                ℓ
ℓ ∈ L E (resp. ℓ ∈ L A ), a transition s →
                                         − s ′ denotes E player’s (resp. A player’s) move from node s to
                           E                A                                                                           ℓ
node s ′. We write s →              → s ′) when there exists ℓ ∈ L E (resp. ℓ ∈ L A ) such that s →
                     − s ′ (resp. s −                                                             − s ′.
Below, we describe each class of games and our encoding of them in µCLP. For simplicity, we
assume that each game starts with A’s turn.

A.2.1 Safety games. In a safety game, we are given predicates ϕ init (e     x ) and ϕ safe (e
                                                                                            x ). The E player
wins the game if only states satisfying ϕ safe (e
                                                x ) are visited along any sequence of plays starting from
any state satisfying ϕ init (e
                             x ). The game can be expressed in µCLP by defining the greatest fixpoint
predicate SG(ex ) as follows:
                                                     A                                   E
                    x ) =ν ϕ safe (e
                 SG(e                     y .⟨e
                                   x ) ∧ ∀e   x⟩ −
                                                 → ⟨e
                                                    y ⟩ ⇒ ϕ safe (e      z .⟨e
                                                                  y ) ∧ ∃e   y⟩ →
                                                                                − ⟨e
                                                                                   z ⟩ ∧ SG(e
                                                                                            z ).

Then, E has a winning strategy if and only if ϕ init (e x ) ⇒ SG(e  x ) is valid. The correctness of the
encoding can be readily seen by observing that SG(e  x ) describes exactly the set of states from which
E can force the plays to stay in the states satisfying ϕ safe (e
                                                               x ).

A.2.2 Reachability games. In a reachability game, we are given predicates ϕ init (e          x ) and ϕ reach (e
                                                                                                              x ).
The E player wins the game if for any play starting from a state satisfying ϕ init (e  x ), a state satisfying
ϕ reach (e
         x ) is eventually visited. As clear from the definition, reachability games are the dual of safety
games. That is, a safety game with the objective ϕ safe (e       x ) is won by E if and only if A wins the
reachability game with the objective ϕ reach (e  x ) = ¬ϕ safe (e
                                                                x ) on the same graph but with the players’
edge sets swapped. The game can be expressed in µCLP by defining the least fixpoint predicate
RG(e x ) as follows:
                                                     A                                       E
                   x ) =µ ϕ reach (e
                RG(e                      y .⟨e
                                   x ) ∨ ∀e   x⟩ −
                                                 → ⟨e
                                                    y ⟩ ⇒ ϕ reach (e      z .⟨e
                                                                   y ) ∨ ∃e   y⟩ →
                                                                                 − ⟨e
                                                                                    z ⟩ ∧ RG(e
                                                                                             z ).

Then, E has a winning strategy if and only if ϕ init (e  x ) ⇒ RG(e x ) is valid. The correctness of the
encoding can be readily seen by observing that RG(e   x ) describes exactly the set of states from which
E can force the plays to eventually reach a state satisfying ϕ reach (ex ).
   Our µCLP formulations of safety games and reachability games show a striking resemblance,
reflecting the inherent duality of the two classes of games. This is in contrast to their formulations
in existentially-quantified Horn clauses [Beyene et al. 2014, 2013] that used rather different encodings
for the two classes.

10 “LTL games” is a misnomer as the games actually go beyond LTL properties. [Farzan and Kincaid 2017] also considers

another class of games called Satisfiability games which is only finite duration and therefore is omitted from our discussion.
28                                                         Hiroshi Unno, Yuki Satake, Tachio Terauchi, and Eric Koskinen


A.2.3 LTL games. In a LTL game, we are given a predicate ϕ init (e       x ) and a Büchi automaton A such
that the label set of A is L E ∪ L A (cf. Section 3.3 for the definition of Büchi automaton). The E player
wins the game if for any play starting from a state satisfying ϕ init (e  x ), the infinite sequence of labels
of the play is accepted by A. The game can be expressed in µCLP by defining the mutually-recursive
least-and-greatest fixpoint predicates LGq,α (e     x ) for each q ∈ Q and α ∈ {µ, ν }:
                        Û               ℓ             Ü                 Ü                         ℓ′
              x ) =α
       LGq,α (e                   y .⟨e
                                 ∀e   x⟩ →
                                         − ⟨e
                                            y⟩ ⇒                                         z .⟨e
                                                                                        ∃e   y ⟩ −→ ⟨e
                                                                                                     z ⟩ ∧ LGq ′′,α (q ′,q ′′ ) (e
                                                                                                                                 z ).
                        ℓ ∈L A                     q ′ ∈δ (q, ℓ)        ℓ′ ∈L E
                                                                   q ′′ ∈δ (q ′, ℓ′ )

Here, α(q 1 , q 2 ) = ν if q 1 ∈ F or q 2 ∈ F , and α(q 1 , q 2 ) = µ otherwise. Then, E has a winning strategy
if and only if ϕ init (e x ) ⇒ LGqinit ,ν (e
                                           x ) is valid. The correctness of the construction follows from an
argument similar to that of the linear temporal property verification reduction shown in Section 3.3.
   Here is an example of a simple LTL game for the property GF(restore). The game consists
of a single integer variable x whose value is initially 0. The LTS is defined with the label sets
L E = {restore, incr, decr} and L A = {break, skip}, and the transition relation is shown in the left
column below:
                   restore
        • ⟨x⟩ −−−−−→ ⟨x ′⟩ if x = x ′ = 0
                incr
        • ⟨x⟩ −−−→ ⟨x ′⟩ if x ′ = x + 1.                                                        restore               ∗
                decr                                                                                      restore
        • ⟨x⟩ −−−→ ⟨x ′⟩ if x ′ = x − 1.                                                        / q0 t              4 q1
                break
        • ⟨x⟩ −−−−→ ⟨x ′⟩ if x = 0 and x ′ , 0.                                                             ∗
                skip
        • ⟨x⟩ −−−→ ⟨x ′⟩ if x = x ′.
A Büchi automaton expressing the property GF(restore) is shown in the right column.
   The winning strategy is obvious: whenever player A breaks away from q 0 by randomly assigning
to x, E must either incr or decr to get x back to 0 and then restore. Following the encoding of LGq,α
above, it is straight forward to define this game in µCLP. The encoding will be as follows:

               LGq,α (x) =α (∀x ′ . (x = 0 ∧ x ′ , 0) ⇒ ϕ(x ′)) ∧ (∀x ′ . x ′ = x ⇒ ϕ(x ′))
                           ∃x ′′ .x ′′ = x ′ − 1 ∧ LGq , µ (x ′′)
                       Ô                              1
               ϕ(x ) =      ∃x ′′ .x ′′ = x ′ + 1 ∧ LGq1, µ (x ′′)
                          
                          
                  ′
                           ∃x ′′ .x ′′ = x ′ = 0 ∧ LGq ,ν (x ′′)
                          
                                                      0


where q ∈ {q 0 , q 1 } and α ∈ {µ, ν }. The universally quantified actions pertain to the A player
performing a break or skip action. The existentially quantified actions pertain to the E player
performing a decr, incr, or restore action.

A.2.4 Cinderella-Stepmother game. As a concrete example of the three classes of games, let us
consider the Cinderella-Stepmother game [Bodlaender et al. 2012; Hurkens et al. 2011], which is
also used as examples in [Beyene et al. 2014; Farzan and Kincaid 2017]. The game comprises five
buckets of water arranged in a circle. Each bucket can hold some constant c amount of water. The
two players, Cinderella and Stepmother, take turns emptying and filling the buckets. In each of her
turns, Stepmother brings 1 unit of additional water and distributes it among the five buckets. In
turn, Cinderella chooses two adjacent buckets and empties them. Cinderella wins if none of the
buckets ever overflow. It is known that Cinderella has a winning strategy exactly when c > 2. For
instance, when c < 1, it is easy to see that Stepmother wins in one round by pouring the entire
additional water to a single bucket. Also, when c ≥ 3, it is easy to see that Cinderella can win by
adopting the round-robin strategy whereby she goes around the circle and in each round empties
two buckets that are adjacent to the buckets that were emptied in the previous round. However, as
Program Verification via Predicate Constraint Satisfiability Modulo Theories                                                   29


                                         ∗            sm,cd             sm,cd                 ∗

                                                                           u   sm,cd
                                                                                                  
                                     /           ∗    /                  /                5
                                                                                    ∗
                                                 A1                               A2

                           Fig. 2. Büchi automata for Cinderella-Stepmother LTL games.


remarked in [Beyene et al. 2014; Farzan and Kincaid 2017], synthesizing a winning strategy (for
Cinderella or Stepmother) when 1 ≤ c < 3 is non-trivial.
   We formalize the game in our framework. The state space of the game is S = Q5≥0 where Q ≥0 is
the set of non-negative rational numbers. Each (b0 , b1 , b2 , b3 , b4 ) ∈ S represents the state of the five
buckets with bi being the amount of water in the i-th bucket. The set of labels for Stepmother is
L SM = {ov, sm} where ov indicates that a bucket is overflowing after Stepmother has made the
move. The set of labels for Cinderella is the singleton set L CD = {cd}. Let us write [0, 4] for the set
{0, 1, 2, 3, 4}. The transition relation is defined by:
                                 sm
    • (b0 , b1 , b2 , b3 , b4 ) −−→ (b0′ , b1′ , b2′ , b3′ , b4′ ) if 1 + i ∈[0,4] bi = i ∈[0,4] bi′ and bi ≤ bi′ ≤ c for each
                                                                         Í             Í
       i ∈ [0, 4].
                                 ov
    • (b0 , b1 , b2 , b3 , b4 ) −→ (b0′ , b1′ , b2′ , b3′ , b4′ ) if 1 + i ∈[0,4] bi = i ∈[0,4] bi′, bi ≤ bi′ for each i ∈ [0, 4],
                                                                         Í             Í
        and there exists i ∈ [0, 4] such that bi′ > c.
                               cd
     • (b0 , b1 , b2 , b3 , b4 ) −→ (b0′ , b1′ , b2′ , b3′ , b4′ ) if there exists i ∈ [0, 4] such that bi′ = b(i+1)%5
                                                                                                               ′       = 0 and
         b j = b j′ for each j ∈ [0, 4] \ {i, (i + 1)%5}.
The set of initial states is described by ϕ init (b0 , b1 , b2 , b3 , b4 ) ≜ i ∈[0,4] bi = 0, that is, the buckets
                                                                                         Ó
are initially all empty.
    For Cinderella, the game can be formalized                        Óas a safety game where L E = L CD , L A = L SM , and
the safety objective is ϕ safe (b0 , b1 , b2 , b3 , b4 ) ≜ i ∈[0,4] bi ≤ c. Dually, for Stepmother, the game can
be formalized as a reachability game where L E = L SM , L A = L CD , and the reachability objective is
ϕ reach (b0 , b1 , b2 , b3 , b4 ) ≜ ¬ϕ safe (b0 , b1 , b2 , b3 , b4 ) = i ∈[0,4] bi > c.
                                                                          Ô
    As in [Beyene et al. 2014], let us also consider variants of the game with LTL objectives. For
instance, consider the Büchi automata A1 and A2 shown in Fig. 2. A1 corresponds to the LTL formula
FG(¬ov). That is, it accepts exactly the plays in which overflows happen only finitely often. By
contrast, A2 corresponds to the LTL formula GF(¬ov) and it accepts exactly the plays in which
buckets are in a non-overflowing state infinitely often. As also remarked in [Beyene et al. 2014], the
automata are examples of weakened objectives for Cinderella which may allow her to win the game
more often. Using A1 or A2 as the objective Büchi automaton and letting L E = L CD and L A = L SM ,
our framework is able to model the weakened variants as LTL games.
