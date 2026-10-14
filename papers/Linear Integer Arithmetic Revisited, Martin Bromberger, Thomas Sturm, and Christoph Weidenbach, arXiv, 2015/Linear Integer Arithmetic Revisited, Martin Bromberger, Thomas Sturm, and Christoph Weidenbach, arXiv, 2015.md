                                                    Linear Integer Arithmetic Revisited

                                                Martin Bromberger, Thomas Sturm, and Christoph Weidenbach

                                                    Max Planck Institute for Informatics, Saarbrücken, Germany
                                                          {mbromber,sturm,weidenb}@mpi-inf.mpg.de
arXiv:1503.02948v3 [cs.LO] 23 Oct 2020




                                               Abstract. We consider feasibility of linear integer programs in the con-
                                               text of verification systems such as SMT solvers or theorem provers. Al-
                                               though satisfiability of linear integer programs is decidable, many state-
                                               of-the-art solvers neglect termination in favor of efficiency. It is challeng-
                                               ing to design a solver that is both terminating and practically efficient.
                                               Recent work by Jovanović and de Moura constitutes an important step
                                               into this direction. Their algorithm CUTSAT is sound, but does not ter-
                                               minate, in general. In this paper we extend their CUTSAT algorithm by
                                               refined inference rules, a new type of conflicting core, and a dedicated rule
                                               application strategy. This leads to our algorithm CUTSAT++, which
                                               guarantees termination.


                                         Keywords: Linear arithmetic, SMT, SAT, DPLL, Linear programming, Integer
                                         arithmetic


                                         1   Introduction

                                         Historically, feasibility of linear integer problems is a classical problem, which has
                                         been addressed and thoroughly investigated by at least two independent research
                                         lines: (i) integer and mixed real integer linear programming for optimization [16],
                                         (ii) first-order quantifier elimination and decision procedures for Presburger
                                         Arithmetic and corresponding complexity results [20,5,10,18,7,8,21,2,3,11,12,22,17].
                                         We are interested in feasibility of linear integer problems, which we call simply
                                         problems, in the context of the combination of theories, as they occur, e.g., in the
                                         context of SMT solving or theorem proving. From this perspective, both these
                                         research lines address problems that are too general for our purposes: with the
                                         former, the optimization aspects go considerably beyond pure feasibility. The
                                         latter considers arbitrary Boolean combinations of constraints and quantifier
                                         alternation or even parametric problems.
                                             Consequently, the SMT community has developed several interesting ap-
                                         proaches on their own [6,13,1].These solvers typically neglect termination and
                                         completeness in favour of efficiency. More precisely, these approaches are based
                                         on a branch-and-bound strategy, where the rational relaxation of an integer prob-
                                         lem is used to cut off and branch on integer solutions. Together with the known
                                         a priori integer bounds [19] for a problem this yields a terminating and complete
                                         algorithm. However, these bounds are so large that for many practical problems

                                                                                     1
the resulting branch-and-bound search space cannot be explored in reasonable
time. Hence, the a priori bounds are not integrated in the implementations of
the approaches.
    On these grounds, the recent work by Jovanović and de Moura [14,15], al-
though itself not terminating, constitutes an important step towards an algo-
rithm that is both efficient and terminating. The termination does no longer
rely on bounds that are a priori exponentially large in the occurring parameters.
Instead, it relies on structural properties of the problem, which are explored by
their CUTSAT algorithm. The price for this result is an algorithm that is by
far more complicated than the above-mentioned branch-and-bound approach. In
particular, it has to consider divisibility constraints in addition to inequalities.
    Our interest in an algorithm for integer constraints originates from a pos-
sible combination with superposition, e.g., see [9]. In the superposition context
integer constraints are part of the first-order clauses. Variables in constraints
are typically unguarded, so that an efficient decision procedure for this case is a
prerequisite for an efficient combined procedure.
    Our contribution is an extension and refinement of the CUTSAT algorithm,
which we call CUTSAT++. In contrast to CUTSAT, our CUTSAT++ generally
terminates. The basic idea of both algorithms is to reduce a problem contain-
ing unguarded integer variables to a problem containing only guarded variables.
These unguarded variables are not eliminated. Instead, one explores the un-
guarded variables by adding constraints on smaller variables to the problem, with
respect to a strict total ordering where all unguarded variables are larger than all
guarded variables. After adding sufficiently many constraints, feasibility of the
problem only depends on guarded variables. Then a CDCL style algorithm tests
for feasibility by employing exhaustive propagation. The most sophisticated part
is to turn an unguarded variable into a guarded variable. Quantifier elimination
techniques, such as Cooper elimination [5], do so by removing the unguarded vari-
able. In case of Cooper elimination, the price to pay is an exponentially growing
Boolean structure and exponentially growing coefficients (see Section 3). Since
integer linear programming is NP-complete, all algorithms known today can not
prevent such a kind of behavior, in general. Since Cooper elimination does not
care about the concrete structure of a given problem, the exponential behavior
is almost guaranteed. The idea of both CUTSAT and CUTSAT++ is therefore
to simulate a lazy variation of Cooper elimination. This leaves space for model
assumptions and simplification rules in order for the algorithm to adapt to the
specific structure of a problem and hence to systematically avoid certain cases
of the worst-case exponential behavior observed with Cooper elimination.
    This paper is and extended version of [4]. It is organized as follows. After
fixing some notation in Section 2, we present three examples for problems where
CUTSAT diverges. The divergence of CUTSAT can be fixed by respective refine-
ments on the original CUTSAT rules. However, in a fourth example the combina-
tion of our refinements results in a frozen state. Our conclusion is that CUTSAT
lacks, in addition to our rule refinements, a third type of conflicting cores, which
we call diophantine conflicting core. Theorem 5 in Section 3 actually implies that

                                         2
any procedure that is based on what we call weak Cooper elimination needs to
consider this type of conflicting core for completeness. In Sections 4-5, we refine
the inference rules for the elimination of unguarded variables on the basis of our
results from Section 3 and show their soundness, completeness, and termination.
We finally give conclusions and point at possible directions for future research.


2    Motivation

We use variables x, y, z, k, possibly with indices. Furthermore, we use integer
constants a, b, c, d, e, l, v, u, linear polynomials p, q, r, s, and constraints I, J
possibly with indices. As input problems, we consider finite sets of constraints C
corresponding to and sometimes used as conjunction over their elements. Each
constraint I is either an inequality an xn + . . . + a1 x1 + c ≤ 0 or a divisibility
constraint d | an xn + . . . + a1 x1 + c. We denote coeff(I, xi ) = ai ∈ Z. vars(C)
denotes the set of variables occurring in C. We sometimes write C(x) in order
to emphasise that x ∈ vars(C(x)). A problem C is satisfiable if ∃X : C holds,
where X = vars(C). For true we denote ⊤ and for false we denote ⊥. Since
d | cx + s ≡ d | −cx − s, we may assume that c > 0 for all d | cx + s ∈ C.
A variable x is guarded in a problem C if C contains constraints of the form
x − ux ≤ 0 and −x + lx ≤ 0. Otherwise, x is unguarded in C. Note that guarded
variables are bounded as defined in [15] but not vice versa. A constraint is guarded
if it contains only guarded variables. Otherwise, it is unguarded.
     Our algorithm CUTSAT++ aims at deciding whether or not a given problem
C is satisfiable. It either ends in the state unsat, or in a state hυ, sati where υ is
a satisfiable assignment for C. In order to reach one of those two final states, the
algorithm produces lower bounds x ≥ b and upper bounds x ≤ b for the variables
in C. The produced bounds are stored in a sequence M = [[γ1 , . . . , γn ]], which
describes a partial model. The empty sequence is denoted by [[]]. We use [[M, γ]]
and [[M1 , M2 ]] to denote the concatenation of a bound γ at the end of M , and
M2 at the end of M1 , respectively.
     By lower(x, M ) = b and upper(x, M ) = b we denote the value b of the
greatest lower bound x ≥ b and the least upper bound x ≤ b for a variable x
in M , respectively [15]. If there is no lower (upper) bound for x in M , then
lower(x, M ) = −∞ (upper(x, M ) = ∞). The definitions of upper and lower are
extended to polynomials as done in [15].
     A state in CUTSAT++ is of the form S = hM, Ci or S = hM, Ci ⊢ I, or
is one of the two final states hυ, sati, unsat [15]. The initial-state for a problem
C is h[[]], Ci. For a state S = hM, Ci(⊢ I), inequality p ≤ 0 is a conflict if
lower(p, M ) > 0. For a state S = hM, Ci(⊢ I), divisibility constraint d | ax + p
is a conflict if all variables in p are fixed, and d ∤ ab + lower(p, M ) for all b with
lower(x, M ) ≤ b ≤ upper(x, M ). In a state S = hM, Ci ⊢ I, the constraint I is
always a conflict.
     The partial model M of a state hM, Ci(⊢ I) is complete if all variables x in
C are fixed, in the sense that upper(x, M ) = lower(x, M ). In this case, we define
υ[M ] as the assignment that assigns to every variable x the value lower(x, M ).

                                          3
With val(p, M ) = lower(p, M ) we denote the value assigned to a fixed polynomial
p, i.e., val(p, M ) is only defined if all variables occurring in p are fixed in M . A
state is frozen if it is not a final state and no rule is applicable.
   Our CUTSAT++ algorithm is defined as a transition system consisting of
the following rules:



Decide                                   
                                             upper(x, M ) 6= +∞,
hM, Ci =⇒CS h[[M, x ≥ b]], Ci       if
                                             lower(x, M ) < b = upper(x, M )
                                         
                                             lower(x, M ) 6= −∞,
hM, Ci =⇒CS h[[M, x ≤ b]], Ci       if
                                             lower(x, M ) = b < upper(x, M )
Propagate                              
                                       
                                        J ∈ C is an inequality,
                                       
                                        coeff(J, x) < 0,
                                       
hM, Ci =⇒CS h[[M, x ≥I b]], Ci      if   improves(J, x, M ),
                                       
                                       
                                       
                                        b = bound(J, x, M ),
                                       
                                         I = tight(J, x, M )
                                       
                                       
                                        J ∈ C is an inequality,
                                       
                                        coeff(J, x) > 0,
                                       
hM, Ci =⇒CS h[[M, x ≤I b]], Ci      if   improves(J, x, M ),
                                       
                                       
                                       
                                        b = bound(J, x, M ),
                                       
                                         I = tight(J, x, M )
Propagate-Div                          
                                       
                                        D = (d | ax + p) ∈ C, val(p, M ) = k,
                                       
                                         b = lower(x, M ), d ∤ ab + k,
hM, Ci =⇒CS h[[M, x ≥I c]], Ci      if
                                       
                                        c = bound(D, x, M ), c ≤ upper(x, M ),
                                       
                                         I = div-derive(D, x, M )
                                       
                                       
                                        D = (d | ax + p) ∈ C, val(p, M ) = k,
                                       
                                         b = upper(x, M ), d ∤ ab + k,
hM, Ci =⇒CS h[[M, x ≤I c]], Ci      if
                                       
                                        c = bound(D, x, M ), c ≥ lower(x, M ),
                                       
                                         I = div-derive(D, x, M )
Conflict
hM, Ci =⇒CS hM, Ci ⊢ p ≤ 0          if p ≤ 0 ∈ C, lower(p, M ) > 0
Conflict-Div                           
                                       
                                         J = (d | ax + p) ∈ C, val(p, M ) = k,
                                       
                                          b = lower(x, M ), d ∤ ab + k,
hM, Ci =⇒CS hM, Ci ⊢ I              if
                                       
                                         bound(J, x, M ) > upper(x, M ),
                                       
                                          I = div-derive(J, x, M )
                                       
                                       
                                         J = (d | ax + p) ∈ C, val(p, M ) = k,
                                       
                                          b = upper(x, M ), d ∤ ab + k,
hM, Ci =⇒CS hM, Ci ⊢ I              if
                                       
                                         bound(J, x, M ) < lower(x, M ),
                                       
                                          I = div-derive(J, x, M )


                                             4
Unsat-Div                                   
                                                d | a1 x1 + . . . + an xn + c ∈ C,
hM, Ci         =⇒CS unsat              if
                                                gcd(d, a1 , . . . , an ) ∤ c
Sat
hM, Ci         =⇒CS hυ[M ], sati       if υ[M ] satisfies C
Forget
hM, C ∪ {J}i =⇒CS hM, Ci               if C ⊢Z J, and J 6∈ C
Slack-Intro                               
                                          
                                           hM, Ci is stuck,
                                          
                                           x is stuck,
                                          
hM, Ci         =⇒CS hM, C ∪ Cs i       if   xS is the slack-variable,
                                          
                                            Cs = {−xS ≤ 0, x − xS ≤ 0,
                                          
                                          
                                          
                                          
                                                    −x − xS ≤ 0}




Resolve
h[[M, γ]], Ci ⊢ I     =⇒CS hM, Ci ⊢ resolve(γ, I)           if γ is an implied bound
Skip-Decision                                                    
                                                                     γ is a decided bound,
h[[M, γ]], Ci ⊢ p ≤ 0 =⇒CS hM, Ci ⊢ p ≤ 0                   if
                                                                     lower(p, M ) > 0
Unsat
hM, Ci ⊢ b ≤ 0        =⇒CS unsat                            if b > 0
Backjump                                                       
                                                               
                                                                γ is a decided bound,
                                                               
                                                                coeff(J, x) < 0,
                                                               
h[[M, γ, M ′ ]], Ci ⊢ J =⇒CS h[[M, x ≥I b]], Ci             if   improves(J, x, M ),
                                                               
                                                               
                                                               
                                                                I = tight(J, x, M ),
                                                               
                                                                 b = bound(J, x, M )
                                                               
                                                                γ is a decided bound,
                                                               
                                                               
                                                                coeff(J, x) > 0,
                                                               
h[[M, γ, M ′ ]], Ci ⊢ J =⇒CS h[[M, x ≤I b]], Ci             if   improves(J, x, M ),
                                                               
                                                               
                                                               
                                                                I = tight(J, x, M ),
                                                               
                                                                 b = bound(J, x, M )
Learn
hM, Ci ⊢ I            =⇒CS hM, C ∪ {I}i ⊢ I                 if I 6∈ C

                                            5
Solve-Div-Left                          
                                         divisibility constraints I1 , I2 ∈ C,
                                        
                                        
                                        
                                        
                                         x is top in I1 and I2 ,
                                        
                                         x is unguarded,
                                        
hM, Ci =⇒CS hM, C ′ i                if   all other vars. in I1 , I2 are fixed,
                                          (I1′ , I2′ ) = div-solve(x, I1 , I2 ),
                                        
                                        
                                        
                                        
                                          C ′ = C \ {I1 , I2 } ∪ {I1′ , I2′ },
                                        
                                        
                                        
                                        
                                         ′
                                          I2 is not a conflict
Solve-Div-Right                         
                                        
                                         divisibility constraints I1 , I2 ∈ C,
                                        
                                        
                                        
                                         x is top in I1 and I2 ,
                                        
                                        
                                        
                                         x is unguarded,
                                        
                                         all other vars. in I1 , I2 are fixed,
                                        
hM, Ci =⇒CS hM ′ , C ′ i             if   (I1′ , I2′ ) = div-solve(x, I1 , I2 ),
                                          C ′ = C \ {I1 , I2 } ∪ {I1′ , I2′ },
                                        
                                        
                                        
                                        
                                          I2′ is a conflict,
                                        
                                        
                                        
                                        
                                          y = top(I2′ ),
                                        
                                        
                                        
                                        
                                         ′
                                          M = prefix(M, y)
Resolve-Cooper                          
                                        
                                         (x, C ′ ) is a conflicting core,
                                        
                                        
                                        
                                         x is unguarded,
                                         all z ≺ x are fixed and C ′ ⊆ C,
                                        
                                        
hM, Ci =⇒CS hM ′ , C ∪ Rk ∪ Rc i     if   if J ∈ C is a conflict, then top(J) 6≺ x,
                                          cooper(x, C ′ ) = (Rk , Rc ),
                                        
                                        
                                        
                                        
                                        
                                        
                                        
                                         y = minI∈Rc {top(I)},
                                         ′
                                          M = prefix(M, y)

CUTSAT [15] includes all of the rules of CUTSAT++ except for the rules Solve-
Div-Left, Solve-Div-Right, and Resolve-Cooper, which are explained in more
detail in Section 4.
    Via applications of the rule Decide, CUTSAT++ adds decided bounds x ≤ b
or x ≥ b to the sequence M in search-state S [15]. A decided bound gener-
ally assigns a variable x to lower(x, M ) or upper(x, M ). Via applications of the
propagation rules, CUTSAT++ adds propagated bounds x ≥I b or x ≤I b to the
sequence M , where I is a generated constraint propagating the bound. To this
end the function bound(J, x, M ) computes the strictest bound value b and the
function tight(J, x, M ) computes the corresponding justification I for constraint
J under the partial model M [15]. For an inequality J, bound(J, x, M ) is defined
as follows:                                l               m
                                                 lower(p,M)
                                          
                                          
                                            −        a       if a > 0,
             bound(ax + p ≤ 0, x, M ) =        j            k
                                          
                                           − lower(p,M) if a < 0.
                                          
                                                   a

Whenever a > 0, J propagates only upper bounds for x. Whenever a < 0, J prop-
agates only lower bounds for x. For a divisibility constraint D, bound(D, x, M )

                                        6
is defined as follows:                            
                                        d⌈ ab+k
                                              d ⌉−k
                                      
                                      
                                              a      if b = lower(x, M ),
                                      
         bound(d | ax + p, x, M ) =      ab+k    
                                      
                                      
                                        d⌊ d ⌋−k
                                      
                                            a      if b = upper(x, M ),

where a > 0, d > 0, all variables in p are fixed, and lower(p) = k. Whenever
we choose b = lower(x, M ) in the above function, D propagates a lower bound.
Whenever we choose b = upper(x, M ) in the above function, D propagates an
upper bound. The bound value bound(D, x, M ) for divisibility constraint D is
computed in such a way that CUTSAT++ never skips a satisfiable solution for
D:

Lemma 1. Let D = d | ax + p be a divisibility constraint with a > 0. Let hM, Ci
be a state where the polynomial p is fixed. Let bound(d | ax + p, x, M ) denote
a lower bound value. (1) Then it holds for all e ∈ {lower(x, M ), . . . , bound(d |
ax + p, x, M ) − 1} that d ∤ ae + lower(p, M ). Otherwise, bound(d | ax + p, x, M )
denotes an upper bound value: (2) Then it holds for all e ∈ {bound(d | ax +
p, x, M, ≤) + 1, . . . , upper(x, M )} that d ∤ ae + lower(p, M ).

Proof. We only prove the case that bound(d | ax + p, x, M ) denotes a lower
bound. The proof for the second case is analogous. Assume for a contradiction
that there exists an e ∈ {lower(x, M ), . . . , bound(d | ax + p, x, M ) − 1} such that
                                                                                     
                                                                                ae+k
d | ae + lower(p,           l Since d m| ae + lower(p, M ), it holds that
              ae+kM ) holds.                                                     d    =
ae+k          d ⌈     ⌉ −k       d ae+k
                                        −k
  d    and         d
                    a        =       d
                                      a    = e. Since lower(x, M ) ≤ e, it holds that
l                 m         
  a lower(x,M)+k
          d         ≤ ae+k d  . Thence,
                                            ab+k       ae+k           
                                            d⌈ d ⌉−k         d⌈ d ⌉−k
           bound(d | ax + p, x, M, ≥) =          a      ≤         a        = e.
Therefore, e ∈/ {lower(x, M ), . . . , bound(d | ax + p, x, M ) − 1}, which contradicts
our initial assumption.

    The rules of the CUTSAT++ calculus are restricted in such a way that
M stays consistent, i.e. lower(x, M ) ≤ upper(x, M ) for all variables x ∈ X.
CUTSAT++ also propagates only bounds that are more strict than the current
bound for the variable x, e.g., CUTSAT++ only propagates lower bound x ≥ b
if b > lower(x, M ). This behaviour is expressed by the following predicate for
inequalities J = ax +p ≤ 0:
                         lower(x, M ) < bound(J, x, M ) ≤ upper(x, M ) , if a < 0,
improves(J, x, M ) =
                         lower(x, M ) ≤ bound(J, x, M ) < upper(x, M ) , if a > 0.
    The justifications annotated to the propagated bounds are necessary for a
CDCL-like conflict resolution. In CDCL, boolean resolution is used to combine
the current conflict C ∨ l with a clause used for unit propagation C ′ ∨ l̄ to receive
a new conflict C ∨C ′ without literals l or ¯l. For CUTSAT++ the function resolve
fulfils a similar purpose:

                                           7
                                              
                                                   |a|q + |c|p ≤ 0 , if a · c < 0,
       resolve(x ⊲⊳cx+q≤0 b, ax + p ≤ 0) =
                                                   ax + p ≤ 0      , otherwise .
Whenever J = ax + p ≤ 0 is a conflict in state h[[M, γ]], Ci ⊢ J, where C ⊢Z J
and γ = x ⊲⊳cx+q≤0 b, J ′ = resolve(x ⊲⊳cx+q≤0 b, ax + p ≤ 0) is also a conflict in
state hM, Ci ⊢ J ′ and C ⊢Z J ′ [15]. The function resolve only results in a new
conflict because CUTSAT++ requires that the justification I of bound x ⊲⊳I b,
with ⊲⊳ ∈ {≤, ≥}, in state hM, Ci(⊢ J) fulfils the following conditions: Firstly, I
is an inequality and C ⊢Z I. Secondly, if ⊲⊳ = ≤, then coeff(I, x) = 1. If ⊲⊳ = ≥,
then coeff(I, x) = −1. Finally, bound(I, x, M ) ⊲⊳ b, i.e. the justification I implies
at least a bound as strong as x ⊲⊳I b.
    The function tight(J, x, M ) = I defined by the set of rules in Figure 1 cal-
culates a justification I in variable x for the bound x ⊲⊳I b propagated from
inequality J = ±ax + p ≤ 0, where b = bound(J, x, M ). A state in this rule
system is a pair
                                   hM ′ , ±ax + as ⊕ ri,
where a > 0, s and r are polynomials, and M ′ is a prefix of the initial M , i.e.
M = [[M ′ , M ′′ ]]. The initial state for tight(±ax + p ≤ 0, x, M ) is hM, ±ax ⊕ pi.
The first goal is to produce an inequality where all coefficients are divisible by
a = coeff(J, x). To this end, we apply the rules (Fig. 1) until the polynomial on
the right side of ⊕ becomes empty. In this case, all coefficients are divisible by
a = coeff(J, x) and we derive the justification I with the final rule Round.
    The function div-derive(D, x, M ) calculates a justification I in variable x for
the bound x ⊲⊳I b propagated from the divisibility constraint D = d | ax + p,
where b = bound(D, x, M ). The justification computed by div-derive is derived
from a set of inequalities describing the propagated bound value. For instance,
let us look at the lower bound value:            ab+k        
                                                  d⌈ d ⌉−k
                           bound(D, x, M ) =           a        ,
where D = d | ax + p, a > 0, d > 0, p is fixed, k = lower(p, M ), and
b = lower(x, M ). The sub-term c = ab+k      d    is equal to the bound value com-
putable from the diophantine representation dz = ax + p of the divisibility
constraint D:                                                   
                   bound(−dz + ax + p ≤ 0, z, M ) = ab+k     d     .
Notice that z is a variable not occurring in the problem, and only introduced
for the above calculation. The fitting tightly propagating inequality for the sub-
terms are abbreviated with
                         div-part(D, x, M ):
                           tight(−dz + ax + p ≤ 0, x, M ) , if b = lower(x, M ),
   div-part(D, x, M ) =
                           tight(dz − ax − p ≤ 0, x, M ) , if b = upper(x, M ).
For div-part, we forbid tight to apply the Consume rule to the variables x and
z. The restriction to Consume guarantees that the inequality ±z + r ≤ 0 =
div-part(D, x, M ) does not contain x. Given I2 = −z+r ≤ 0 = div-part(D, x, M )
and I1 = dz − ax − p ≤ 0, we use resolve(x ≥I2 c, I1 ) = −ax + dr − p ≤ 0 = I3
to receive the inequality that computes the complete       lower bound:
                                   l                m  d ab+k −k 
                                     d lower(r,M)−k         ⌈ d ⌉
               bound(I3 , x, M ) =           a        ≥        a     .
Finally, we compute the tightly propagating inequality for a divisibility con-

                                          8
Consume
   hM, ±ax + as ⊕ aky + ri             =⇒tight hM, ±ax + as + aky ⊕ ri,
where x 6= y.
Resolve-Implied
   h[[M, γ]], ±ax + as ⊕ pi            =⇒tight hM, ±ax + as ⊕ qi,
where γ is a propagated bound and q ≤ 0 = resolve(γ, p ≤ 0).
Decide-Lower
   h[[M, y ≥ b]], ±ax + as ⊕ cy + ri   =⇒tight hM, ±ax + as + aky ⊕ r + (ak − c)qi,
                                                  c
where y ≤I b in M , with I = y + q ≤ 0, and k =     a
                                                      .
Decide-Lower-Neg
   h[[M, y ≥ b]], ±ax + as ⊕ cy + ri   =⇒tight hM, ±ax + as ⊕ cq + ri,
where y ≤I b in M , with I = y − q ≤ 0, and c < 0.
Decide-Upper
   h[[M, y ≤ b]], ±ax + as ⊕ cy + ri   =⇒tight hM, ±ax + as + aky ⊕ r + (c − ak)qi,
                                                    c
where y ≥I b in M , with I = −y + q ≤ 0, and k =     a
                                                       .
Decide-Upper-Pos
   h[[M, y ≤ b]], ±ax + as ⊕ cy + ri   =⇒tight hM, ±ax + as ⊕ cq + ri,
where y ≥I b in M , with I = −y + q ≤ 0, and c > 0.
Round (and terminate)
                                                            
                                                            b
   hM, ±ax + as ⊕ bi                   =⇒tight ± x + s +       ≤0
                                                            a


        Fig. 1. Rule system that derives tightly propagating inequalities [15]



straint D = d | ax + p withthe function
                                          div-derive(D, x, M ):
                           
                                    b  = lower(x, M ),
                              ′
                           
                            I   if   I 2 = −z  + r ≤ 0 = div-part(D, x, M, ),
                            3
                                    ′
                                      I
                                     3   = tight(−ax  + dr − p ≤ 0, x, M ),
    div-derive(D, x, M ) =
                           
                                    b  = upper(x, M  ),
                             I ′ if
                           
                           
                                     I2 = z + r ≤ 0 = div-part(D, x, M ),
                            3
                                    ′
                                      I3 = tight(ax + dr + p ≤ 0, x, M ).
    The rule Slack-Intro is necessary to prevent a special type of frozen state
called stuck state. A variable x is called stuck in state S = hM, Ci if M contains
no bounds for x and there is no inequality I = ax + p ≤ 0 ∈ C that propagates
a bound for x [15]. Variables x with a constraint of the form ±x − b ≤ 0 ∈
C are never stuck, as CUTSAT++ is able to propagate at least one bound
for x, i.e., either x ≥ −b or x ≤ b. A state S is a stuck state if all unfixed
variables x are stuck and if the rules Sat, Unsat-Div, Conflict, and Conflict-Div
are not applicable [15]. In a stuck state, Slack-Intro is applicable and one of the
previously stuck variables x is turned unstuck by the constraints added to the

                                           9
problem. As recommended in [15], CUTSAT++ uses the same slack variable for
all Slack-Intro applications.
    We are now going to discuss three examples where CUTSAT diverges. The
first one shows that, CUTSAT can apply Conflict and Conflict-Div infinitely
often to constraints containing unguarded variables.
Example 1. Let
  C := {−x ≤ 0, −y ≤ 0, −z ≤ 0, z ≤ 0, z + 1 ≤ 0, 1 − x + y ≤ 0, x − y ≤ 0}
        | {z } | {z } | {z } | {z } | {z } |            {z    } | {z }
              Ix       Iy       Iz1     Iz2        Iz3         J1            J2
be a problem. Let Si = hMi , Ci for i ∈ N be a series of states with:
                  M0 := [[x ≥Ix 0, y ≥Iy 0, z ≥Iz1 0, z ≤Iz2 0]],
                  Mi+1 := [[Mi , x ≥J1 i + 1, y ≥J2 i + 1]].
Let the variable order be given by z ≺ y ≺ x. CUTSAT with a two-layered
strategy [15] has diverging runs starting in state S0′ = h[[]], Ci. Let CUTSAT
traverse the states S0′ , S0 , S1 , S2 , . . . in the following fashion: CUTSAT reaches
state S0 from state S0′ after propagating the constraints Ix , Iy , Iz1 , and Iz2 .
CUTSAT reaches state Si+1 from state Si after:
 – fixing x to i with a Decision γdx := x ≤ i; Mi1 := [[Mi , γdx ]] and Si1 := hMi1 , Ci
 – applying Conflict to Constraint J1 because lower(1 − x + y, Mi1 ) > 0; Mi2 :=
   Mi1 and Si2 := hMi2 , Ci ⊢ J1
 – undoing the decided bound γdx by applying Backjump because the predicate
   improves(J1 , x, Mi , ≥) evaluates to true. The result is the exchange of γdx
   with the bound γ x = x ≥J1 i + 1; Mi3 := [[Mi , γ x ]] and Si3 := hMi3 , Ci
 – fixing y to i with a Decision γdy := y ≤ i; Mi4 := [[Mi3 , γdy ]] and Si4 := hMi4 , Ci
 – applying Conflict to Constraint J2 because lower(x − y, Mi4 ) > 0; Mi5 := Mi4
   and Si5 := hMi5 , Ci ⊢ J1
 – undoing the decided bound γdy by applying Backjump because the predicate
   improves(J2 , y, Mi3 , ≥) evaluates to true. The result is the exchange of γdy
   with the bound γ y = y ≥J2 i + 1; Mi6 := [[Mi3 , γ y ]] and Si+1 = Si6 := hMi6 , Ci
Since {Iz1 , Iz3 } is a conflicting core, the variable z is the minimal conflicting vari-
able in the states Si , Si1 , and Si4 . Since Iz1 and Iz2 bound z, the conflicting core
is also guarded. Therefore, Resolve-Cooper as defined in [15] is not applicable,
which in turn implies that Conflict is applicable.
     A straightforward fix to example 1 is to limit the application of the Con-
flict and Conflict-Div rules to guarded constraints. Our second example shows,
that CUTSAT can still diverge by infinitely many applications of the Solve-Div
rule [15].
Example 2. Let di be the sequence with d0 = 2 and dk+1 := dk 2 for k ∈ N, let
C0 = {4 | 2x + 2y, 2 | x + z} be a problem, and let S0 = h[[]], C0 i be the initial
CUTSAT state. Let the variable order be given by x ≺ y ≺ z. Then CUTSAT
has divergent runs S0 =⇒CS S1 =⇒CS S2 =⇒CS . . .. For instance, let CUTSAT
apply the Solve-Div rule whenever applicable. By an inductive argument, Solve-
Div is applicable in every state Sn = h[[]], Cn i, and the constraint set Cn has the
following form:

                                              10
                     
                 {2dn | dn x + dn y, dn | d2n y − d2n z} if n is odd,
              Cn =
                 {2dn | dn x + dn y, dn | d2n x + d2n z} if n is even.
Therefore, CUTSAT applies Solve-Div infinitely often and diverges.
    A straightforward fix to example 2 is to limit the application of Solve-Div
to maximal variables in the variable order ≺. Our third example shows, that
CUTSAT can apply Conflict and Conflict-Div [15] infinitely often. The exam-
ple 3 differs from example 1 in that the conflicting core contains also unguarded
variables.
Example 3. Let
   C := {−x ≤ 0, −y ≤ 0, −z ≤ 0, z ≤ 0, 1 − x + y + z ≤ 0, x − y − z ≤ 0}}
         | {z } | {z } | {z } | {z } |         {z       } |      {z    }
               Ix        Iy      Iz1    Iz2           J1                J2
be a problem. Let Si = hMi , Ci for i ∈ N be a series of states with:
                      M0 := [[x ≥Ix 0, y ≥Iy 0, z ≥Iz1 0, z ≤Iz2 0]],
                      Mi+1 := [[Mi , x ≥J1 i + 1, y ≥J2 i + 1]].
Let the variable order be given by z ≺ x ≺ y. CUTSAT has diverging runs
starting in state S0′ = h[[]], Ci. For instance, let CUTSAT traverse the states S0′ ,
S0 , S1 , S2 , . . . in the following fashion: CUTSAT reaches state S0 from state
S0′ after propagating the constraints Ix , Iy , Iz2 and Iz2 . CUTSAT reaches state
Si+1 from state Si after:
 – fixing x to i and y to i with Decisions γdx := x ≤ i and γdy := y ≤ i;
   Mi1 := [[Mi , γdx , γdy ]] and Si1 := hMi1 , Ci
 – applying Conflict to Constraint J1 because lower(1 − x + y + z, Mi1 ) > 0;
   Mi2 := Mi1 and Si2 := hMi2 , Ci ⊢ J1
 – undoing the decided bounds γdy and γdx by applying first Skip-Decision and
   then Backjump. The result is the sequence Mi3 := [[Mi , γ x ]] and the state
   Si3 := hMi3 , Ci, where γ x = x ≥J1 i + 1;
 – fixing y to i and x to i + 1 with Decisions γdy := y ≤ i and γdx := y ≤ i + 1;
   Mi4 := [[Mi3 , γdy , γdx ]] and Si4 := hMi4 , Ci
 – applying Conflict to Constraint J2 because lower(x − y − z, Mi4 ) > 0; Mi5 :=
   Mi4 and Si5 := hMi5 , Ci ⊢ J1
 – undoing the decided bounds γdx and γdy by applying first Skip-Decision and
   then Backjump. The result is the sequence Mi6 := [[Mi3 , γ y ]] and the state
   Si+1 = Si6 := hMi6 , Ci, where γ y = y ≥J2 i + 1.
Notice that the conflicting core {J1 , J2 } in states Si1 and Si4 is bounded in [15],
which admits the application of Conflict.
    For example 3, applying the fix suggested for example 1 results in a frozen
state. Here, a straightforward fix is to change the definition of conflicting cores
to cover only those cores where the conflicting variable is the maximal variable.1
    The fixes for our examples suggested above are restrictions of CUTSAT which
have the consequence that Conflict(-Div) cannot be applied to unguarded con-
straints, Solve-Div is only applicable for the elimination of the maximal variable,
1
    The restrictions to maximal variables in the definition of the conflicting core and
    to the Solve-Div rule were both confirmed as missing but necessary in a private
    communication with Jovanović.


                                           11
and the conflicting variable x is the maximal variable in the associated conflict-
ing core C ′ . However, our next and final example shows that these restrictions
lead to frozen states.
Example 4. Let CUTSAT include restrictions to maximal variables in the defini-
tion of conflicting cores, and in the Solve-Div rule as described above. Let there
be additional restrictions in CUTSAT to the rules Conflict and Conflict-Div such
that these rules are only applicable to conflict constraints I where I contains no
unguarded variable. Let
                   C := {−x ≤ 0, x − 1 ≤ 0, −y ≤ 0, 6 | 4y + x}
                           | {z } | {z } | {z } | {z }
                           Ix1       Ix2        Iy       J
be a problem. Let M := [[x ≥Ix1 0, x ≤Ix2 1, y ≥Iy 0, x ≥ 1, y ≤ 0]] be a bound se-
quence. Let the variable order be given by x ≺ y. CUTSAT has a run starting in
state S0′ = h[[]], Ci that ends in the frozen state S = hM, Ci. Let CUTSAT prop-
agate Ix1 , Ix2 , Iy , and fix x to 1 and y to 0 with two Decisions. Through these
Decisions, the constraint J is a conflict. Since y is unguarded, CUTSAT can-
not apply the rule Conflict-Div. Furthermore, [15] has defined conflicting cores
as either interval or divisibility conflicting cores. The state S contains neither
an interval or a divisibility conflicting core. Therefore, CUTSAT cannot apply
the rule Resolve-Cooper. The remaining rules are also not applicable because
all variables are fixed and there is only one divisibility constraint. Without the
before introduced restrictions to the rules Conflict(-Div), Solve-Div, CUTSAT
diverges on the example.


3   Weak Cooper Elimination
In order to fix the frozen state of Example 4 in the previous section, we are going
to introduce in Section 4 a new conflicting core, which we call diophantine con-
flicting core. For understanding diophantine conflicting cores, as well as further
modifications to be made, it is helpful to understand the connection between
CUTSAT and a variant of Cooper’s quantifier elimination procedure [5].
    The original Cooper elimination takes a variable x, a problem C(x), and
produces a disjunction of problems, equivalent to ∃x h: C(x):              i
                    W                   W         W
     ∃x : C(x) ≡         C−∞ (k) ∨                       a | p + k ∧ C p+k
                                                                         a     ,
                0≤k<m             −ax+p≤0∈C 0≤k<a·m
where a > 0, m = lcm{d ∈ Z : (d | ax + p) ∈ C}. If there exists no constraint
of the form −ax + p ≤ 0 ∈ C, then C−∞ (x) = {(d | ax + p) ∈ C} . Otherwise,
C−∞ (x) = ⊥. One application of Cooper elimination results in a disjunction
of quadratically many problems out of a single problem. Iteration causes an
exponential increase in the coefficients due to the multiplication with a because
division is not part of the language.
    Weak Cooper elimination is a variant of Cooper elimination that is very help-
ful to understand problems around CUTSAT. The idea is, instead of building
a disjunction over all potential solutions for x, to add additional guarded vari-
ables and constraints without x that guarantee the existence of a solution for
x. We assume here that C(x) contains only one divisibility constraint for x. If

                                           12
not, exhaustive application of div-solve to divisibility constraints for x removes
all constraints except one: div-solve(x, d1 | a1 x + p1 , d2 | a2 x + p2 ) = (d1 d2 |
dx + c1 d2 p1 + c2 d1 p2 , d | −a1 p2 + a2 p1 ), where d = gcd(a1 d2 , a2 d1 ), and c1 and
c2 are integers such that c1 a1 d2 + c2 a2 d1 = d [5,15]. Now weak Cooper elimina-
tion takes a variable x, a problem C(x) and produces a new problem by replacing
∃x : C(x) with:                                                                
                                                                        S
         ∃K : {I ∈ C(x) : coeff(I, x) = 0} ∪ {gcd(c, d) | s} ∪              Rk ,
                                                                     k∈K
where d | cx + s ∈ C(x), k ∈ K is a newly introduced variable for every pair of
constraints −ax + p ≤ 0 ∈ C(x) and bx − q ≤ 0 ∈ C(x),
    Rk = {−k ≤ 0, k − m ≤ 0, bp − aq + bk ≤ 0, a | k + p, ad | cp + as + ck}
                                                                           
                                                                         ad
is a resolvent for the same inequalities [15], where m := lcm a, gcd(ad,c)      − 1.
Note that there is still an existential quantifier ∃K but all variables k ∈ K are
guarded by their respective Rk .
    Let ν be a satisfiable assignment for the formula after one weak Cooper
elimination step on C(x). Then we compute a strictest lower bound x ≥ lx and
a strictest upper bound x ≤ ux from C(x) for the variable x under the assignment
ν. We now argue that there is a value vx for x such that x ≥ lx , x ≤ ux , and
d | cvx + s are satisfied. Whenever lx 6= −∞ and ux 6= ∞, the bounds x ≥ lx ,
x ≤ ux are given by respective constraints of the form −ax + p ≤ 0 ∈ C(x)
and bx − q ≤ 0 ∈ C(x) such that lx = ⌈ ν(p)                      ν(q)
                                               a ⌉ and ux = ⌊ b ⌋. In this case
                                     ν(k+p)
the extension of ν with ν(x) =          a   satisfies C(x) because the constraint
a | k + p ∈ Rk guarantees that ν(x) ∈ Z, the constraint bp − aq + bk ≤ 0 ∈ Rk
guarantees that lx ≤ ν(x) ≤ ux , and the constraint ad | cp + as + ck ∈ Rk
guarantees that ν satisfies d | cx + s ∈ C(x). Whenever lx = −∞ (ux = ∞) we
extend ν by an arbitrary small (large) value for x that satisfies d | cx + s ∈ C(x).
There exist arbitrarily small (large) solutions for x and d | cx + ν(s) because
gcd(c, d) | s is satisfied by ν.
    The advantage of weak Cooper elimination compared to Cooper elimination
is that the output is again one conjunctive problem in contrast to a disjunction
of problems. Our CUTSAT++ performs weak Cooper elimination not in one
step but subsequently adds to the states the constraints from the Rk as well as
the divisibility constraint gcd(c, d) | s with respect to a strict ordering on the
unguarded variables.
    The following equivalence, for which we have just outlined the proof, states
the correctness of weak Cooper elimination:
                                                                              
                                                                         S
   ∃x : C(x) ≡ ∃K : {I ∈ C(x) : coeff(I, x) = 0} ∪ {gcd(c, d) | s} ∪         Rk .
                                                                            k∈K
    The extra divisibility constraint gcd(c, d) | s in weak Cooper elimination is
necessary whenever the problem C(x) has no constraint of the form −ax + p ≤
0 ∈ C(x) or bx − q ≤ 0 ∈ C(x). For example, let C(x) = {y − 1 ≤ 0, −y + 1 ≤
0, 6 | 2x+y} be a problem and x be the unguarded variable we want to eliminate.
As there are no inequalities containing x, weak Cooper elimination without the
extra divisibility constraint returns C ′ = {y − 1 ≤ 0, −y + 1 ≤ 0}. While C ′ has

                                           13
a satisfiable assignment ν(y) = 1, C(x) has not since 2x + 1 is never divisible by
2 or 6.
    Note that for any Rk introduced by weak Cooper elimination we can also
show the following Lemma:


Lemma 2. Let k be a new variable. Let a, b, c > 0. Then,
                 (∃x : {−ax + p ≤ 0, bx − q ≤ 0, d | cx + s})
  ≡ (∃k : {−k ≤ 0, k − m ≤ 0, bp − aq + bk ≤ 0, a | k + p, ad | cp + as + ck}).

Proof. See [15] pp. 101-102 Lemma 4.

    That means satisfiability of the respective Rk guarantees a solution for the
triple of constraints it is derived from. An analogous Lemma holds for the divis-
ibility constraint gcd(c, d) | s introduced by weak Cooper elimination:

Lemma 3. (∃x : d | cx + s) ≡ gcd(c, d) | s.

Proof. We equivalently rewrite the two divisibility constraints into diophantine
equations, viz. ∃y : dy − cx = s, and ∃k : gcd(c, d)k = s for d | cx + s, and
gcd(c, d) | s, respectively. We choose d′ , c′ ∈ Z such that d′ · gcd(c, d) = d and
c′ · gcd(c, d) = c. Assume that ν is a variable assignment such that dν(y) −
cν(x) = ν(s) and therefore also d | cν(x) + ν(s). Thence ν(s) = dν(y) − cν(x) =
gcd(c, d) · (d′ ν(y) − c′ ν(x)). After extending ν with ν(k) = (d′ ν(y) − c′ ν(x)), ν
satisfies gcd(c, d)k = s.
     Assume, that ν is a variable assignment such that gcd(c, d)ν(k) = ν(s) holds
and therefore also gcd(c, d) | ν(s). By Beźout’s Lemma there exist a′ , b′ ∈ Z,
such that a′ d − b′ c = gcd(c, d). Thence a′ dν(k) − b′ cν(k) = (a′ d − b′ c)ν(k) =
gcd(c, d)ν(k) = ν(s). After extending ν with ν(y) = a′ ν(k) and ν(x) = b′ ν(k)
the assignment ν satisfies dy − cx = s.

    That means satisfiability of gcd(c, d) | s guarantees a solution for the divisi-
bility constraint d | cx + s. The rule Resolve-Cooper (Fig. 3) in our CUTSAT++
exploits these properties by generating the Rk and constraint gcd(c, d) | s in the
form of strong resolvents in a lazy way. Furthermore, it is not necessary for the
divisibility constraints to be a priori reduced to one, as done for weak Cooper
elimination. Instead, the rules Solve-Div-Left and Solve-Div-Right (Fig. 3) per-
form lazy reduction.
    The solution set for variable x, assignment ν, and problem C(x), is the set
of values S ⊆ Z such that v ∈ S if C(v) is satisfied by ν. The solution set Sd of
a divisibility constraint d | cx + s, variable x, and assignment ν is either empty
or unbounded from above and below.

Lemma 4. Let ν be an assignment for all variables except x. Let Sd be the
solution set for variable x, assignment ν, and constraint d | cx + s. Then,
              Sd = ∅ or Sd = {v0 + ev ′ : e ∈ Z} for some v0 , v ′ ∈ Z.

                                         14
Proof. In case Sd 6= ∅, there exists a value v0 ∈ Sd such that d | cv0 + ν(s). We
first prove that there exists a v ′ ∈ Z such that d | c(v0 + ev ′ ) + ν(s) for all e ∈ Z
and therefore v0 + ev ′ ∈ Sd . We choose v ′ , e′ ∈ Z such that c = e′ gcd(c, d) and
d = v ′ gcd(c, d). Then we deduce for any e ∈ Z:
                   d | c(v0 + ev ′ ) + ν(s) ≡ d | cv0 + ν(s) + cev ′ ≡
                         d | cv0 + ν(s) + de′ v ′ ≡ d | cv0 + ν(s)
    It remains to show that for every vk ∈ Sd there exists an e ∈ Z such that
v0 +ev ′ = vk . As Sd is the solution set we know that d | cv0 +ν(s) and d | cvk +ν(s)
are true. Thence d | c(v0 − vk ) ≡ d | cv0 + ν(s) − (cvk + ν(s)). As d = v ′ gcd(c, d),
the term c(v0 − vk ) is only divisible by d if v0 − vk is divisible by v ′ . Therefore,
∃e ∈ Z : v0 − vk = ev ′ .
    This property allows us to choose an arbitrary small or large solution for x
to satisfies d | cx + ν(s) in the correctness proof of weak Cooper Elimination. As
mentioned in the outline of the proof, the ability to choose arbitrary small and
large solutions for x is necessary when C(x) contains no constraints of the form
−ax + p ≤ 0 or bx − q ≤ 0.

Theorem 5.                                                                   
                                                                         S
   ∃x : C(x) ≡ ∃K :     {I ∈ C(x) : coeff(I, x) = 0} ∪ {gcd(c, d) | s} ∪   Rk
                                                                            k∈K

Proof. First, we partition the problem C(x) as follows:
    Cl = {−ax + p ≤ 0 ∈ C(x) : a > 0}, Cu = {bx − q ≤ 0 ∈ C(x) : b > 0},
    Id = d | cx + s ∈ C(x),             Cr = {I ∈ C(x) : coeff(I, x) = 0}.
By Lemma 2, it holds for all −ax + p ≤ 0, bx − q ≤ 0 ∈ C(x) with a, b > 0 that:
           (∃x : C(x)) → (∃x : {−ax + p ≤ 0, bx − q ≤ 0, d | cx + s})
  → (∃k : {−k ≤ 0, k − m ≤ 0, bp − aq + bk ≤ 0, a | k + p, ad | cp + as + ck}).
          |                              {z                                 }
                                               Rk
By Lemma 3, it holds that: (∃x : C(x)) → (∃x : d | cx + s) → gcd(c, d) | s. As
Cr ⊆ C(x) it also holds that: (∃x : C(x)) → Cr . As all new variables k ∈ K
appear only in one resolvent
                            Rk , the above implications prove           
                                                                    S
  ∃x : C(x) → ∃K : {I ∈ C(x) : coeff(I, x) = 0} ∪ {gcd(c, d) | s} ∪   Rk .
                                                                           k∈K
    Assume, vice versa, that ν is a satisfiable assignment for the formula after
one step of weak Cooper elimination. Then it is easy to deduce the following
facts:

              n solution set for x, ν,oand Il = −ax + p ≤ 0 ∈ C(x) with a > 0.
 – Let Sl be the
   Then Sl = ⌈ ν(p)       ν(p)
                   a ⌉, ⌈ a ⌉ + 1, . . . .
 – Let Su be then solution set for x, ν,o and Iu = bx − q ≤ 0 ∈ C(x) with b > 0.
   Then Su = . . . , ⌊ ν(q)       ν(q)
                        b ⌋ − 1, ⌊ b ⌋ .
                                                                          T
   Let SI be the solution set for x, ν, and Cl ∪ Cu . Then SI = Il ∈Cl Sl ∩
 – T
    Iu ∈Cu Su .
 – Let the set SI be bounded from n      below, i.e., SI = {l, l o
                                                                 + 1, . . .} or SI =
                                           ′
                                           )
    {l, . . . , u}. Then l = maxI∈Cl ⌈ ν(p           ′     ′
                                        a′ ⌉ : I = −a x + p ≤ 0 .


                                          15
                               n above, i.e., SI = {. . o
 – Let the set SI be bounded from                       . , u − 1, u} or SI =
   {l, . . . , u}. Then u = minI∈Cu ⌊ ν(q)       ′      ′
                                       b ⌋:I = b x−q ≤ 0 .
 – By Lemma 3, d | cx + ν(s) is satisfiable because gcd(c, d) | s is contained
   in the result formula of weak Cooper elimination. By Lemma 4, the set of
   solutions for x, ν, and d | cx + s has the form Sd = {v0 + v ′ µ : v ′ ∈ Z}.
 – The solution set S for x, ν, and C ′ is S = Sd ∩ SI .
Next, we do a case distinction on the structure of C(x):
 – Let Cl = ∅, then SI is unbounded from below. We choose a small enough
   v ∈ Sd , i.e., small enough v ′ ∈ Z such that v = v0 +v ′ µ. Then the assignment
   x 7→ v and y 7→ ν(y) (if y 6= x) satisfies C ′ .
 – Let Cu = ∅, then SI is unbounded from above. We choose a large enough
   v ∈ Sd , i.e., large enough v ′ ∈ Z such that v = v0 + v ′ µ. Then the assignment
   x 7→ v and y 7→ ν(y) for all y 6= x satisfies C ′ .
 – Let |Cl |, |Cu | > 0. We select Il = −ax
                                         n +′ p ≤ 0 such that            o
                                            ν(p )
                      ⌈ ν(p)
                          a  ⌉ = max                        ′
                                     I∈Cl ⌈ a′ ⌉ : I = −a x + p ≤ 0
                                                                   ′

   and Iu = bx − q ≤ 0 such that          n                            o
                                             ν(q′ )
                       ⌊ ν(q)                             ′      ′
                           b ⌋ = minI∈Cu ⌊ b′ ⌋ : I = b x − q ≤ 0 .
   The resolvent for the two constraints Il and Iu is
       Rk = {−k ≤ 0, k − m ≤ 0, bp − aq + bk ≤ 0, a | k + p, ad | cp + as + ck}.
   We will now show that ν(p+k)    a   is in the set of solutions S of C(x). All of
   the remaining deductions stem from the evaluation of the resolvent under
   ν. Since a | ν(p + k), ν(p+k)  a     ∈ Z. Furthermore,
                                                 n            since oν(p+k)
                                                                        a   ∈ Z and
    ν(bp − aq + bk) ≤ 0, ν(p+k)  a     ∈ SI = ⌈ ν(p)             ν(q)
                                                   a ⌉, . . . , ⌊ b ⌋ . Finally, since
               ad | ν(cp + as + ck) = ad | acν(x) + aν(s) = d | cν(x) + ν(s),
    ν(p+k)
       a    ∈   Sd . We choose the assignment ν ′ with x 7→ ν(p+k)  a   and y 7→ ν(y)
    for all y 6= x. Hence, ν ′ satisfies C ′ .


    We stated that weak Cooper elimination can only be applied to those prob-
lems where C(x) contains one divisibility constraint d | ax + p in x. To expand
weak Cooper elimination to any set of constraints C ′ (x) we briefly explained
how to exhaustively apply div-solve to eliminate all but one constraint d | ax + p
in x. The algorithm CombDivs(x, C) (Fig. 2) is a more detailed version of this
procedure.
Lemma 6. Let C ′ (x) be a set of LIA constraints. Let C(x) be the output of
CombDivs(x, C ′ (x)). Then C(x) ≡ C ′ (x).
Proof. Follows directly from the proof of equivalence [15] of the div-solve trans-
formation.
    Since the output C(x) of CombDivs(x, C ′ (x)) is equivalent to C ′ (x) and fulfils
the conditions of weak Cooper elimination, we conclude the following equivalence
for the output of weak Cooper elimination applied to C(x):

                                         16
    Algorithm 1: CombDivs(x, C ′ (x))
   Input : The variable x and a set of LIA constraints C ′ (x)
   Output : A set of LIA constraints C(x) such that C(x) ≡ C ′ (x) and there
               exists one divisibility constraint d | cx + s ∈ C(x) such that c > 0
                           ′
 1 Cd := {d | cx + s ∈ C (x) : c > 0}
              ′
 2 C(x) := C (x) \ Cd ;
 3 if (Cd = ∅) then
 4     return C(x) ∪ {1 | x} ;
 5 while (|Cd | > 1) do
 6     Select d1 | a1 x + p1 , d2 | a2 x + p2 ∈ Cd ;
 7     Cd := Cd \ {d1 | a1 x + p1 , d2 | a2 x + p2 };
 8     d = gcd(a1 d2 , a2 d1 ) ;
 9     Choose c1 and c2 such that c1 a1 d2 + c2 a2 d1 = d;
10     Cd := Cd ∪ {d1 d2 | dx + c1 d2 p1 + c2 d1 p2 } ;
11     C(x) := C(x) ∪ {d | −a1 p2 + a2 p1 };
12 end
13 return C(x) ∪ Cd ;


Fig. 2. An algorithm that combines constraints Cd = {d | cx + s ∈ C ′ (x) : c > 0} until
only one divisibility constraint in x remains

                                                                                         
          ′
                                                                               S
    ∃x : C (x) ≡ ∃K :       {I ∈ C(x) : coeff(I, x) = 0} ∪ {gcd(c, d) | s} ∪         Rk
                                                                               k∈K



4     Strong Conflict Resolution Revisited

Weak Cooper elimination is capable of exploring all unguarded variables to even-
tually create a problem where feasibility only depends on guarded variables. It
is simulated in a lazy manner through an additional set of CUTSAT++ rules
(Fig. 3). Instead of eliminating all unguarded variables before the application
of CUTSAT++, the rules perform the same intermediate steps as weak Cooper
elimination, viz. the combination of divisibility constraints via div-solve and
the construction of resolvents, to resolve and block conflicts in unguarded con-
straints. As a result, CUTSAT++ can avoid some of the intermediate steps of
weak Cooper elimination. Furthermore, CUTSAT++ is not required to apply the
intermediate steps of weak Cooper elimination one variable at a time. The lazy
approach of CUTSAT++ does not eliminate unguarded variables. In the worst
case CUTSAT++ has to perform all of weak Cooper elimination’s intermediate
steps. Then a strategy (Def. 13) guarantees that CUTSAT++ recognizes that
all unguarded conflict constraints have been blocked by guarded constraints.
    The eventual result is the complete algorithm CUTSAT++, which is a com-
bination of the rules Resolve-Cooper, Solve-Div-Left, Solve-Div-Right (Fig. 3),
a strictly-two-layered strategy (Def. 13), and the CUTSAT rules: Propagate,
Propagate-Div, Decide, Conflict, Conflict-Div, Sat, Unsat-Div, Forget, Slack-
Intro, Resolve, Skip-Decision, Backjump, Unsat, and Learn [15].

                                            17
     The advantage of the lazy approach is that CUTSAT++ might find a sat-
isfiable assignment or detect unsatisfiability without encountering and resolving
a large number of unguarded conflicts. This means the number of divisibility
constraint combinations and introduced resolvents might be much smaller in the
lazy approach of CUTSAT++ than during the elimination with weak Cooper
elimination.
     In order to simulate weak Cooper elimination, CUTSAT++ uses a total order
≺ over all variables such that y ≺ x for all guarded variables y and unguarded
variables x [15]. While the order needs to be fixed for all unguarded variables, the
ordering among the guarded variables can be dynamically changed. In relation
to weak Cooper elimination, the order ≺ describes the elimination order for the
unguarded variables, viz. xi ≺ xj if xj is eliminated before xi . A variable x is
called maximal in a constraint I if x is contained in I and all other variables in
I are smaller with respect to ≺. The maximal variable in I is also called its top
variable (x = top(I)).

Definition 7. Let S = hM, Ci be a state, C ′ ⊆ C, x the top variable in C ′ and
let all other variables in C ′ be fixed. The pair (x, C ′ ) is a conflicting core if it is
of one of the following three forms
(1) C ′ = {−ax + p ≤ 0, bx − q ≤ 0}, and the lower bound from −ax + p ≤ 0
contradicts the upper bound from bx − q ≤ 0, i.e., bound(−ax + p ≤ 0, x, M ) >
bound(bx − q ≤ 0, x, M )[15]; in this case (x, C ′ ) is called an interval conflicting
core and its strong resolvent is ({−k ≤ 0, k − a + 1 ≤ 0}, {bp − aq + bk ≤ 0, a |
k + p}) [15]
(2) C ′ = {−ax + p ≤ 0, bx − q ≤ 0, d | cx + s}, and bl = bound(−ax + p ≤
0, x, M ), bu = bound(bx − q ≤ 0, x, M ), bl ≤ bu and for all bd ∈ [bl , bu ] we have
d ∤ cbd + lower(s, M )[15]; in this case (x, C ′ ) is called a divisibility conflicting
core and its strong resolvent is ({−k ≤ 0, k − m ≤ 0}, {bp − aq + bk ≤ 0, a |
k + p, ad | cp + as + ck}) [15]
(3) C ′ = {d | cx + s}, and for all bd ∈ Z we have d ∤ cbd + lower(s, M ); in this
case (x, C ′ ) is called a diophantine conflicting core and its strong resolvent is
(∅, {gcd(c, d) | s}).                                                      
                                                               ad
In the first two cases k is a fresh variable and m = lcm a, gcd(ad,c) − 1.

    We refer to the respective strong resolvents for a conflicting core (x, C ′ ) by
the function cooper(x, C ′ ) which returns a pair (Rk , Rc ) as defined above. Note
that the newly introduced variable k is guarded by the constraints in Rk . If there
is a conflicting core (x, C ′ ) in state S, then x is called a conflicting variable. A
potential conflicting core is a pair (x, C ′ ) if there exists a state S where (x, C ′ )
is a conflicting core.
    Next we define a semantic generalization of strong resolvents. Since the strong
resolvents generated out of conflicting cores will be further processed by CUT-
SAT++, we must guarantee that any set of constraints implying the feasibility of
the conflicting core constraints prevents a second application of Resolve-Cooper
to the same conflicting core. All strong resolvents of Definition 7 are also strong
resolvents in the sense of the below definition (see also end of Section 3).

                                           18
Definition 8. A set of constraints R is a strong resolvent for the pair (x, C ′ )
if it holds that R → ∃x : C ′ and for all J ∈ R : top(J) ≺ x.
Lemma 9. Let C ′ ⊆ C. Let cooper(x, C ′ ) = (Rk , Rc ). Let R = Rk ∪ Rc . Then
∃k : C ∪ R ≡ C. Furthermore, R is a strong resolvent for (x, C ′ ).
Proof. Follows directly from the Lemmas 2 and 3. The interval conflicting core
is the only new case. However, cooper(x, {−ax + p ≤ 0, bx − q ≤ 0}) is equivalent
to cooper(x, {−ax + p ≤ 0, bx − q ≤ 0, 1 | x}). By Lemmas 2 and 3, R → ∃x : C ′ .
Finally, since k is the minimal element of ≺ and all other variables in R appear
in C ′ , where x is maximal, it holds that J ∈ R : top(J) ≺ x.
    The rule Resolve-Cooper (Fig. 3) requires that the conflicting variable x of
the conflicting core (x, C ′ ) is the top-variable in the constraints of C ′ . This sim-
ulates a setting where all variables y with x ≺ y are already eliminated. We
restrict Resolve-Cooper to unguarded constraints, because weak Cooper elimi-
nation modifies only unguarded constraints.
Lemma 10. Let S = hM, Ci be a CUTSAT++ state. Let C ′ ⊆ C and x be
an unguarded variable. Let R, R ⊆ C, be a strong resolvent for (x, C ′ ). Then
Resolve-Cooper is not applicable to (x, C ′ ).
Proof. Assume for contradiction that D = (x, C ′ ) is a conflicting core, R ∈ C
is a strong resolvent for D in state S and Resolve-Cooper is applicable to D in
state S. Resolve-Cooper requires that all variables y ≺ x are fixed (Fig. 3). This
holds especially for all variables in R (Def. 8). Due to the restriction that every
conflict J ∈ C has top(J) 6≺ top(I) in Resolve-Cooper, there is no conflict in
R. Furthermore, since all variables y ≺ x are fixed, R is satisfied by the partial
assignment defined by M . By Def. 7, all conflicting cores have no satisfiable
solution for x under partial model M . However, by Def. 8, R satisfiable implies
that there exists an x such that C ′ is satisfiable under M . This contradicts the
assumption that (x, C ′ ) is a conflicting core!
    For the resolvent R to block Resolve-Cooper from being applied to the
conflicting core (x, C ′ ), CUTSAT++ has to detect all conflicts in R. Detect-
ing all conflicts in R is only possible if CUTSAT++ fixes all variables y with
y ≺ x and if Resolve-Cooper is only applicable if there exists no conflict I with
top(I) ≺ x. Therefore, the remaining restrictions of Resolve-Cooper justify the
above Lemma. If we add strong resolvents again and again, then CUTSAT++
will reach a state after which every encounter of a conflicting core guarantees
a conflict in a guarded constraint. From this point forward CUTSAT++ won’t
apply Resolve-Cooper anymore. The remaining guarded conflicts are resolved
with the rules Conflict and Conflict-Div [15].
    The rules Solve-Div-Left and Solve-Div-Right (Fig. 3) combine divisibility
constraints as it is done a priori to weak Cooper elimination. In these rules we
restrict the application of div-solve(x, I1 , I2 ) to constraints where x is the top
variable and where all variables y in I1 and I2 , with y 6= x, are fixed. The ordering
restriction simulates the order of elimination, i.e., we apply div-solve(x, I1 , I2 )

                                          19
in a setting where all variables y with x ≺ y appear to be eliminated in I1
and I2 . Otherwise, divergence would be possible (see example 2). Requiring
smaller variables to be fixed prevents the accidental generation of a conflict for
an unguarded variable xi by div-solve(x, I1 , I2 ).
   Thanks to an eager top-level propagating strategy, defined below, any un-
guarded conflict in CUTSAT++ is either resolved with Solve-Div-Right (Fig. 3)
or CUTSAT++ constructs a conflicting core that is resolved with Resolve-
Cooper. Both cases may require multiple applications of the Solve-Div-Left rule
(Fig. 3). We define the following further restrictions on the CUTSAT++ rules
that will eventually generate the above described behavior.

Definition 11. Let ⊲⊳ ∈ {≤, ≥}. We call a strategy for CUTSAT++ eager top-
level propagating if we restrict propagations and decisions for every state hM, Ci
in the following way:

1. Let x be an unguarded variable. Then we only allow to propagate bounds
   x ⊲⊳ bound(I, x, M ) if x is the top variable in I. Furthermore, if I is a
   divisibility constraint d | ax + p, then we only propagate d | ax + p if:
   (a) Either lower(x, M ) 6= −∞ and upper(x, M ) 6= ∞
   (b) Or if gcd(a, d) | lower(p, M ), and d | ax + p is the only divisibility con-
       straint in C with x as top variable.
2. Let x be an unguarded variable. Then we only allow decisions γ = x ⊲⊳ b if:
   (a) For every constraint I ∈ C with x = top(I) all occurring variables y 6= x
       are fixed
   (b) There exists no I ∈ C where x = top(I) and I is a conflict in [[M, γ]]
   (c) Either lower(x, M ) 6= −∞ and upper(x, M ) 6= ∞ or there exists at most
       one divisibility constraint in C with x as top variable.

    An eager top-level propagating strategy has two advantages. First, the strat-
egy dictates an order of influence over the variables, i.e., a bound for unguarded
variable x is only influenced by previously propagated bounds for variable y with
y ≺ x. Furthermore, the strategy makes only decisions for unguarded variable x
when all constraints with x = top(I) are fixed and satisfied by the decision. This
means any conflict I ∈ C with x = top(I) is impossible as long as the decision for
x remains on the bound sequence. For the same purpose, i.e., avoiding conflicts
I where x = top(I) is fixed by a decision, CUTSAT++ backjumps in the rules
Resolve-Cooper and Solve-Div-Right to a state where this is not the case. To
avoid frozen states resulting from the eager top-level propagating strategy, the
slack variable xS has to be the smallest unguarded variable in ≺. Otherwise, the
constraints x − xS ≤ 0, −x − xS ≤ 0 introduced by Slack-Intro cannot be used
to propagate bounds for variable x, and x would remain stuck.

Definition 12. A strategy is reasonable if Propagate applied to constraints of
the form ±x − b ≤ 0 has the highest priority over all rules and the Forget Rule
is applied only finitely often [15].

                                       20
Solve-Div-Left                          
                                        
                                         divisibility constraints I1 , I2 ∈ C,
                                         x is top in I1 and I2 ,
                                        
                                        
                                        
                                         x is unguarded,
                                        
                                        
hM, Ci =⇒CS hM, C ′ i                if   all other vars. in I1 , I2 are fixed,
                                          (I1′ , I2′ ) = div-solve(x, I1 , I2 ),
                                        
                                        
                                        
                                        
                                          C ′ = C \ {I1 , I2 } ∪ {I1′ , I2′ },
                                        
                                        
                                        
                                        
                                         ′
                                          I2 is not a conflict
Solve-Div-Right                         
                                        
                                         divisibility constraints I1 , I2 ∈ C,
                                         x is top in I1 and I2 ,
                                        
                                        
                                        
                                        
                                        
                                        
                                         x is unguarded,
                                         all other vars. in I1 , I2 are fixed,
                                        
                                        
hM, Ci =⇒CS hM ′ , C ′ i             if   (I1′ , I2′ ) = div-solve(x, I1 , I2 ),
                                          C ′ = C \ {I1 , I2 } ∪ {I1′ , I2′ },
                                        
                                        
                                        
                                        
                                          I2′ is a conflict
                                        
                                        
                                        
                                        
                                         y = top(I2′ )
                                        
                                        
                                        
                                         ′
                                          M = prefix(M, y)
Resolve-Cooper
                                          (x, C ′ ) is a conflicting core,
                                        
                                        
                                        
                                        
                                        
                                        
                                         x is unguarded,
                                         all z ≺ x are fixed and C ′ ⊆ C,
                                        
                                        
hM, Ci =⇒CS hM ′ , C ∪ Rk ∪ Rc i     if   if J ∈ C is a conflict, then top(J) 6≺ x,
                                          cooper(x,      C ′ ) = (Rk , Rc ),
                                        
                                        
                                        
                                        
                                          y = minI∈Rc {top(I)},
                                        
                                        
                                        
                                        
                                         ′
                                          M = prefix(M, y)

In the above rules, M ′ = prefix(M, y) defines the largest prefix of M that contains only
decided bounds for variables x with x ≺ y.

                      Fig. 3. Our strong conflict resolution rules



Definition 13. A strategy is strictly-two-layered if:
(1) it is reasonable, (2) it is eager top-level propagating (Def. 11), (3) the Forget,
Conflict, Conflict-Div rules only apply to guarded constraints, (4) Forget cannot
be applied to a divisibility constraint or a constraint contained in a strong resol-
vent, and (5) only guarded constraints are used to propagate guarded variables.


   A strictly-two-layered strategy is the final restriction to CUTSAT++. With
the condition 13-(3) it partitions conflict resolution into two layers: Every un-
guarded conflict is handled with the rules Resolve-Cooper, Solve-Div-Left, and
Solve-Div-Right (Fig. 3), every guarded conflict with the rules Conflict(-Div).
The conditions 13-(1) and 13-(5) make the guarded variables independent from
the unguarded variables. The conditions 13-(2) and 13-(4) give a guarantee that
the rules Resolve-Cooper, Solve-Div-Left, and Solve-Div-Right are applied at
most finitely often. We assume for the remainder of the paper that all runs of
CUTSAT++ follow a strictly-two-layered strategy.

                                           21
5     Termination and Completeness
The CUTSAT++ rules are Propagate, Propagate-Div, Decide, Conflict, Conflict-
Div, Sat, Unsat-Div, Forget, Slack-Intro, Resolve, Skip-Decision, Backjump, Un-
sat, and Learn from [15], as well as Resolve-Cooper, Solve-Div-Left, and Solve-
Div-Right (Fig. 3). Before we prove termination and completeness for CUT-
SAT++, we have to prove another property over strong resolvents. We have
proven in Section 4 that Resolve-Cooper applied to conflicting core (x, C ′ ) adds
a strong resolvent R, which blocks another application of Resolve-Cooper to
(x, C ′ ). However, CUTSAT++ is able to remove constraints from R with the
rules Solve-Div-Left and Solve-Div-Right. This removes the original conflict-
ing core R from our state. Nonetheless, CUTSAT++ is still unable to apply
Resolve-Cooper to conflicting core (x, C ′ ) because the rules Solve-Div-Left and
Solve-Div-Right guarantee that a new strong resolvent R′ for conflicting core
(x, C ′ ) is introduced:

Lemma 14. Let S = hM, Ci be a state reachable by CUTSAT++ from the
initial state h[[]], C0 i and let S ′ = hM ′ , C ′ i be a state reachable by CUTSAT++
from S. Let C contain a strong resolvent R for (x, C ′′ ). Then C ′ contains also
a strong resolvent R′ for (x, C ′′ ).

Proof. Assume for a contradiction that S contains a strong resolvent R for
(x, C ′′ ) and S ′ contains no strong resolvent R′ ∈ C ′ for (x, C ′′ ). W.l.o.g. we as-
sume that S ′ is the first state after S where R * C ′ . By Def. 13.(4), CUTSAT++
with a strictly-two-layered strategy cannot remove constraints from a strong re-
solvent R except with the rules Solve-Div-Right and Solve-Div-Left. Through
the equivalence proven for div-solve(x, I1 , I2 ) in [15], we know that there exist
I1′ , I2′ ∈ C ′ such that {I1′ , I2′ } ≡ {I1 , I2 } and R ⊆ C ′ \ {I1′ , I2′ } ∪ {I1 , I2 }. Thus
R′ = R \ {I1 , I2 } ∪ {I1′ , I2′ } is a strong resolvent of (x, C ′′ ) such that
                                       R′ → R → ∃x : C ′′ .
Furthermore, R is a subset of C ′ , which contradicts our initial assumption!
                    ′


    Together with Lemma 10 this property implies that Resolve-Cooper is applied
at most once to every conflicting core encountered by CUTSAT++. This is
essential for our termination proof.

5.1    Proof for Termination
For the termination proof of CUTSAT++, we consider a (possibly infinite) se-
quence of rule applications h[[]], C0 i = S0 =⇒CS S1 =⇒CS . . . on a problem C0 ,
following the strictly-two-layered strategy.
    First, this sequence reaches a state Ss (s ∈ N+  0 ) after a finite derivation of
rule applications S0 =⇒CS . . . =⇒CS Ss such that there is no further application
of the rules Slack-Intro and Forget after state Ss :

Lemma 15. Let h[[]], C0 i = S0 =⇒CS S1 =⇒CS . . . be a sequence of rule applica-
tions applied to a problem C0 , following the strictly-two-layered strategy. Then

                                               22
the sequence reaches a state Ss (s ∈ N+  0 ) after at most finitely many rule ap-
plications S0 =⇒CS . . . =⇒CS Ss such that there is no further application of the
rules Slack-Intro and Forget after state Ss .

Proof. Such a state Ss exists for two reasons: Firstly, the strictly-propagating-
strategy employed by CUTSAT++ is also reasonable. The reasonable strategy
explicitly forbids infinite applications of the rule Forget. Secondly, the Slack-Intro
rule is applicable only to stuck variables and only once to each stuck variable.
Only the initial set of variables can be stuck because all variables x introduced
during the considered derivation are introduced with at least one constraint
x − b ≤ 0 that allows at least one propagation for the variable. Therefore, the
rules Slack-Intro and Forget are at most finitely often applicable.
     Next, the sequence reaches a state Sw (w ≥ s) after a finite derivation of
rule applications Ss =⇒CS . . . =⇒CS Sw such that there is no further applica-
tion of the rules Resolve-Cooper, Solve-Div-Left or Solve-Div-Right after state
Sw : The rules Resolve-Cooper, Solve-Div-Left, Solve-Div-Right, and Slack-Intro
are applicable only to unguarded constraints. Through the strictly-two-layered
strategy they are also the only rules producing unguarded constraints. There-
fore, they form a closed loop with respect to unguarded constraints, which we
use in our termination proof. We have shown in the previous paragraph that
Ss =⇒CS . . . =⇒CS Sw contains no application of the rule Slack-Intro. By Lemma
10, an application of Resolve-Cooper to the conflicting core (x, C ′ ) prevents any
further applications of Resolve-Cooper to the same core. By Def. 7, the con-
straints learned through an application of Resolve-Cooper contain only variables
y such that y ≺ x. Therefore, an application of Resolve-Cooper blocks a con-
flicting core (x, C ′ ) and introduces potential conflicting cores only for smaller
variables than x. This strict decrease in the conflicting variables guarantees that
we encounter only finitely many conflicting cores in unguarded variables. There-
fore, Resolve-Cooper is at most finitely often applicable. An analogous argument
applies to the rules Solve-Div-Left and Solve-Div-Right. Thus the rules Resolve-
Cooper, Solve-Div-Left and Solve-Div-Right are at most finitely often applicable.

Lemma 16. Let h[[]], C0 i = S0 =⇒CS S1 =⇒CS . . . be a sequence of rule applica-
tions applied to a problem C0 , following the strictly-two-layered strategy. Then
the sequence reaches a state Sw after finitely many rule applications S0 =⇒CS
. . . =⇒CS Sw such that there is no further application of the rules Resolve-Cooper,
Solve-Div-Left, and Solve-Div-Right after state Sw .

Proof. By Lemma 15, we assume w.l.o.g. that the sequence continues from a
state Ss such that Ss is reached by the sequence after at most finitely many
rule applications S0 =⇒CS . . . =⇒CS Ss , and there is no further application
of the rules Slack-Intro and Forget after state Ss . Let x1 ≺ . . . ≺ xn be the
order of variables for all unguarded variables xi . We consider a weight vector
that strictly decreases after every call to Resolve-Cooper, Solve-Div-Left and
Solve-Div-Right. For this weight vector, we define cores(xi , C) as the set of po-
tential conflicting cores in the problem C with conflicting variable xi . Its subset

                                         23
woSR(xi , C) ⊆ cores(xi , C) is defined so it contains all its potential conflicting
cores without a strong resolvent R ⊆ C. It is easy to see that | cores(xi , C)| ≤ 2|C|
and therefore both functions define finite sets. Now we define the weight vector
weightc (S) for every state S = hM, Ci(⊢ I):
weightc (S) = (| cores(xn , C)|, | woSR(xn , C)|, . . . , | cores(x1 , C)|, | woSR(x1 , C)|)
By Definition 13, Conflict(-Div) is only applicable to guarded constraints and
guarded variables are only propagated through guarded constraints. Therefore,
the conflict I in a state hM, Ci ⊢ I stays always guarded, even after an ap-
plication of the Resolve rule, and Learn is only applicable to guarded con-
straints. Therefore, Resolve-Cooper, Solve-Div-Left, and Solve-Div-Right are
the only rules learning potentially unguarded constraints and thereby the only
rules that can increase | cores(xi , C)| and | woSR(xi , C)| between two subsequent
states Si =⇒CS Si+1 . After all other transitions Si =⇒CS Si+1 , it holds that
weightc (Si ) ≥lex weightc (Si+1 ). Whenever CUTSAT++ applies Solve-Div-Left,
Solve-Div-Right or Resolve-Cooper, the weight vector strictly decreases, i.e.,
weightc (S ′ ) >lex weightc (S):
 1. By Lemma 10, an application of Resolve-Cooper to conflicting core (xi , C ∗ )
    implies that there is no strong resolvent R′ ⊆ C ′ for (xi , C ∗ ). By Lemma 9,
    the new problem C = C ′ ∪ R contains a strong resolvent R for (xi , C ∗ ).
    Therefore, | woSR(xi , C)| < | woSR(xi , C ′ )|. By Definition 8, it holds for
    all y ∈ vars(R) that y ≺ x. Thence, Resolve-Cooper has not introduced
    new potential conflicting cores (xj , C ∗∗ ) with j ≥ i and | cores(xj , C)| ≤
    | cores(xj , C ′ )| for all j ≥ i. By Lemma 14, | woSR(xj , C)| ≤ | woSR(xj , C ′ )|
    for all j > i. Therefore, the weight decreases after an application of Resolve-
    Cooper, i.e., weightc (S ′ ) >lex weightc (S).
 2. Let Solve-Div-Left (Solve-Div-Right) be applied to the pair of divisibility
    constraints (I1 , I2 ) such that top(I1 ) = xi and div-solve(xi , I1 , I2 ) = (I1′ , I2′ ).
    The new constraint set is C = C ′ \ {I1 , I2 } ∪ {I1′ , I2′ }. The number of
    potential conflicting cores containing the same divisibility constraint I =
    d | ax + p ∈ C ′′ in problem Ĉ ⊎ {I} is the same for all divisibility con-
    straints with top(I) = x. This means, removing I1 and replacing it with
    I1′ doesn’t increase the number of cores, i.e., | cores(xi , C ′ \ {I1 } ∪ {I1′ })| =
    | cores(xi , C ′ )|. However, since I2 ∈ cores(xi , C ′ ) and we replace I2 with I2′
    where top(I2′ ) ≺ xi , we will decrease the number of conflicting cores in xi .
    It is easy to see, that we do not introduce any new conflicting cores for xj
    with j > i. Thus | cores(xj , C)| = | cores(xj , C ′ )|. Finally, Lemma 14 implies
    that | woSR(xj , C)| ≤ | woSR(xj , C ′ )| for j > i. Therefore, weightc (C ′ ) >lex
    weightc (C).
We deduce that the weightc vector monotonically decreases if we continue from
the before mentioned state Ss . Since > is a well-founded order, the lexicographic
order >lex is also well-founded. The minimum of the weight order is (. . . , 0, . . .).
As >lex is well-founded, there exists no way to decrease the weight weightc (Cs )
without reaching the minimum (. . . , 0, . . .) after finitely many applications of the
rules Solve-Div-Left, Solve-Div-Right, or Resolve-Cooper. Finally, the weightc
vector cannot decrease below (. . . , 0, . . .) so CUTSAT++ is not able to apply

                                              24
Solve-Div-Left, Solve-Div-Right, or Resolve-Cooper after we reach a state S with
weightc (S) = (. . . , 0, . . .). We conclude that the rules Solve-Div-Left, Solve-Div-
Right, and Resolve-Cooper are at most finitely often applicable.

    Next, the sequence reaches a state Sb (b ≥ w) after a finite derivation of rule
applications Sw =⇒CS . . . =⇒CS Sb such that for every guarded variable x the
bounds remain invariant, i.e., lower(x, Mb ) = lower(x, Mj ) and upper(x, Mb ) =
upper(x, Mj ) for every state Sj = hMj , Cj i(⊢ Ij ) after Sb = hMb , Cb i(⊢ Ib ) (j ≥
b): The strictly-two-layered strategy guarantees that only bounds of guarded
variables influence the propagation of further bounds for guarded variables. Any
rule application involving unguarded variables does not influence the bounds
for guarded variables. A proof for the termination of the solely guarded case
was already provided in [15]. At this point we know that the sequence after Sb
contains no further propagations, decisions, or conflict analysis for the guarded
variables.

Lemma 17. Let h[[]], C0 i = S0 =⇒CS S1 =⇒CS . . . be a sequence of rule applica-
tions applied to a problem C0 , following the strictly-two-layered strategy. Then
the sequence reaches a state Sb after finitely many rule applications S0 =⇒CS
. . . =⇒CS Sb such that such that for every guarded variable x the bounds remain
invariant.

Proof. This proof is based on the termination proof for CUTSAT on finite prob-
lems, i.e., problems without unguarded variables [15]. It uses a weight function
that strictly decreases whenever CUTSAT++ changes a bound for a guarded
variable and otherwise stays the same. By Lemmas 15 and 16, we assume w.l.o.g.
that the sequence continues from a state Sw such that Sw is reached by the se-
quence after at most finitely many rule applications S0 =⇒CS . . . =⇒CS Sw ,
and there is no further application of the rules Slack-Intro, Forget, Resolve-
Cooper, Solve-Div-Left, and Solve-Div-Right after state Sw . The levelB of a
state S = hM, Ci is the number of decisions for guarded variables in M . The
maximal prefix of M containing only j decisions for guarded variables is denoted
by B-subseqj (M ) = Mj the j-th guarded subsequence. Since CUTSAT++ is rel-
evant, it prefers to propagate simple constraints. This allows us to assume w.l.o.g.
that M0 contains both a lower and upper bound for all guarded variables x. The
guarded weight of the j-th     P levelB is defined by the function wB (Mj ):
                     wB (Mj ) = x is guarded (upper(x, M ) − lower(x, M )) .
The guarded weight of a state is the vector:
          weightB (hM, Ci) = hwB (B-subseq0 (M )), · · · , wB (B-subseqn (M ))i,
where n is the number of guarded variables. We order the two weightB -vectors
of two subsequent search-states with the well-founded lexicographic order >lex
based on the well-founded order >. It is easy to see that the minimum of weightB
is (. . . , 0, . . .) and that any change to a bound of a guarded variable changes
the guarded weight weightB . Furthermore, by the definition of the strictly-two-
layered strategy, we see that we only propagate guarded variables with guarded
constraints. Thus the strategy also implies that the conflict rules, Conflict,

                                          25
Conflict-Div, Backjump, Resolve, Skip-Decision, Unsat, and Learn, only han-
dle guarded constraints. Given the proof for Theorem 2 in [15], we see that
every application of Propagate, Propagate-Div and Decide applied to a guarded
variable decreases weightB strictly. We see in the same proof [15] that weightB
strictly decreases between one application of Conflict(-Div) and Backjump as
long as the conflict rules handle only guarded constraints - as is the case for
CUTSAT++. Since the bound sequence M is finite, the conflict rules are at most
|M | times applicable between one application of Conflict(-Div), and Backjump
or Unsat. The remaining rules, Propagate, Propagate-Div and Decide applied
to unguarded variables, have no influence on weightB or the bounds of guarded
variables. Since the guarded weight weightB cannot decrease below (. . . , 0, . . .),
we conclude that CUTSAT++ is not able to change the bounds for guarded
variables infinitely often.
    Next, the sequence reaches a state Su (u ≥ b) after a finite derivation of
rule applications Sb =⇒CS . . . =⇒CS Su such that also for every unguarded
variable x the bounds remain invariant, i.e. lower(x, Mb ) = lower(x, Mj ) and
upper(x, Mb ) = upper(x, Mj ) for every state Sj = hMj , Cj i(⊢ Ij ) after Su =
hMu , Cb i(⊢ Iu ) (j ≥ u). After Sb , CUTSAT++ propagates and decides only
unguarded variables or ends with an application of Sat or Unsat(-Div). CUT-
SAT++ employs the strictly-two-layered strategy which is also an eager top-level
propagating strategy. The latter induces a strict order of propagation over the
unguarded variables through the top-variable restriction for propagating con-
straints. Therefore, any bound for unguarded variable x is influenced only by
bounds for variables y ≺ x. This strict variable order guarantees that unguarded
variables are propagated and decided only finitely often.
Lemma 18. Let h[[]], C0 i = S0 =⇒CS S1 =⇒CS . . . be a sequence of rule applica-
tions applied to a problem C0 , following the strictly-two-layered strategy. Then
the sequence reaches a state Su after finitely many rule applications S0 =⇒CS
. . . =⇒CS Su such that for every unguarded variable x the bounds remain invari-
ant.
Proof. By Lemmas 15, 16, and 17, we assume w.l.o.g. that the sequence continues
from a state Sb = hMb , Cb i(⊢ Ib ) such that Sb is reached by the sequence after
at most finitely many rule applications S0 =⇒CS . . . =⇒CS Sb and only the rules
Sat, Unsat-Div, Propagate, Propagate-Div, and Decide are applied after Sb ,
whereas the last three only for unguarded variables. Assume for a contradiction
that there exists an infinite CUTSAT++ run starting in Sb . Since there is only a
finite number of unguarded variables and no rule to undo a decision, the Decide
rule is applied at most finitely often. Furthermore, any application of Sat or
Unsat-Div ends a run making it finite. This allows us to assume w.l.o.g. that
there is no application to the rules Sat, Unsat-Div, and Decide in the infinite
run starting in the state Sb .
    Since there are at most finitely many variables in state Sb , and no rule to
introduce further variables after Sb , there exists a smallest unguarded variable x
that is propagated infinitely often. We assume w.l.o.g. that the run starting in Sb

                                         26
propagates only variables y bigger than or equal to x. Therefore, the bounds of all
smaller variables y, remain invariant in all subsequent states Sj = hMj , Cj i(⊢ Ij )
of Sb , i.e., lower(y, Mj ) = lower(y, Mb ) and upper(y, Mj ) = upper(y, Mb ). Since
there exists no applicable rule that changes the constraint set, we notice that the
constraint set Cb also remains invariant for all states after Sb . Thus we find all
constraints C ∗ used to propagate x in the set Cb . Since CUTSAT++ is eager top-
level propagating, any constraint I ∈ C ∗ has x as their top variable. This leads
us to the deduction, that bound(I, x, Mj ) = bound(I, x, Mb ) for all subsequent
states Sj = hMj , Cj i and inequalities I ∈ C ∗ . Since the bounds defined by the
inequalities in C ∗ remain invariant after state Sb , CUTSAT++ propagates x at
most finitely often with inequalities.
    Therefore, there only exists an infinite CUTSAT++ run if x is propagated in-
finitely often with Propagate-Div. This allows us to assume w.l.o.g. that the run
starting in Sb propagates x only with Propagate-Div. Next, we deduce that vari-
able x stays unbounded in the remaining states of the derivation sequence. Other-
wise there exists a finite set x ∈ {lx , . . . , ux } bounding x, therefore allowing only
finitely many propagations. In the case that x stays unbounded, the definition of
the eager top-level propagating strategy states that Propagate-Div is only appli-
cable to x if Id = d | ax+p ∈ C ∗ is the only divisibility constraint in Cb with x as
their top variable. Furthermore, we know, because of Definition 11 and Lemma 3,
that there must exist v ∈ Z such that d | av + lower(p, Mk ) is satisfied. Now if
we consider Lemma 1 and the conditions c = bound(D, x, M ), c ≤ upper(x, M )
and c = bound(D, x, M ), c ≥ lower(x, M ) of the Propagate-Div rule, then we see
that Propagate-Div propagates x at most finitely often. More specifically, if the
lower bound of x is lower(x, Mb ) = lx 6= −∞ then Propagate-Div propagates for
x at most v −lx lower bounds. If the upper bound of x is upper(x, Mb ) = ux 6= ∞
then Propagate-Div propagates for x at most ux − v upper bounds. This contra-
dicts the assumption that x is the smallest variable propagated infinitely often,
which in turn contradicts our initial assumption!

   After state Su , only the rules Sat, Unsat, and Unsat-Div are applicable,
which lead to a final state. Hence, the sequence S0 =⇒CS S1 =⇒CS . . . is finite.
We conclude that CUTSAT++ always terminates:

Theorem 19. If CUTSAT++ starts from an initial state h[[]], C0 i, then there is
no infinite derivation sequence.

Proof. By Lemmas 15, 16, 17, and 18, CUTSAT++ reaches a state Su after
which only the rules Sat, Unsat, and Unsat-Div are applicable, which lead to a
final state. Therefore, CUTSAT++ does not diverge.


5.2   Frozen States

Our CUTSAT++ algorithm never reaches a frozen state. Let x be the smallest
unfixed variable with respect to ≺. Whenever x is guarded we can propagate
a constraint ±x − b ≤ 0 ∈ C and then fix x by introducing a decision. If we

                                           27
cannot propagate any bound for x, then x is unguarded and stuck, and there-
fore Slack-Intro is applicable. If we cannot fix x by introducing a decision, then
x is unguarded and there is a conflict constraint. Guarded conflict constraints
are resolved via the Conflict(-Div) rules. Unguarded conflict constraints are re-
solved via the strong conflict resolution rules. Unless a final state is reached
CUTSAT++ has always a rule applicable.
    The proof outlined above works because CUTSAT++ encounters only un-
guarded conflict constraints that are either the result of multiple contradicting
divisibility constraints resolvable by Solve-Div-Left and Solve-Div-Right, or ex-
pressible via a conflicting core. Since conflicting cores are only defined over con-
straints and propagated bounds, we have to guarantee that CUTSAT++ never
encounters an unguarded conflict constraint I where x = top(I) is fixed with a
Decision. We express this property with the following invariant fulfilled by every
state visited by CUTSAT++:

Definition 20. A state S = hM, Ci(⊢ I) is called eager top-level propagated if
for all unguarded variables x, all decisions γ = x ⊲⊳ b in M = [[M ′ , γ, M ′′ ]], and
all constraints J ∈ C with top(J) = x: (1) all other variables contained in J are
fixed in M ′ and (2) J is no conflict in S.

Lemma 21. If S ′ is an eager top-level propagated state (Def. 20), then any
successor state S = hM, Ci(⊢ I) reachable by CUTSAT++ is eager top-level
propagated.

Proof. Let S ′ be an eager top-level propagated state and S its successor, i.e.,
S ′ =⇒CS S. We prove this Lemma with a case distinction on the rule leading to
the above transition:
 1. Let the applied rule be Propagate(-Div). Then S ′ = hM ′ , C ′ i and S =
    h[[M ′ , x ⊲⊳J b]], C ′ i. Let J ′ ∈ C ′ be the constraint used for propagation, i.e.,
    J ′ fulfils the properties improves(J ′ , x, M ′ ), bound(J ′ , x, M ′ ) = b and J =
    tight(J ′ , x, M ′ ) (or J = div-derive(J ′ , x, M ′ )). Let the unguarded variable
    y be fixed by a decided bound γ, i.e., M ′ = [[M ′′ , γ, M ′′′ ]]. Let I ∈ C ′ be
    a constraint with top(I) = y. Since S ′ is eager top-level propagated, all
    variables in I are fixed in M ′ and M ′′ . The variable x is not fixed in M ′ ,
    because the predicate improves(J ′ , x, M ′ ) must be true for Propagate(-Div)
    to be applicable. Therefore, x is not contained in I (or top(I) = y ≺ x) and
    I is still no conflict in S. Furthermore, all variables in I are still fixed in
    [[M ′ , x ⊲⊳J b]]. We conclude that S is eager top-level propagated.
 2. Let the applied rule be Decide. Then S ′ = hM ′ , C ′ i and S = h[[M ′ , x ⊲⊳
    b]], C ′ i. We will use the eager top-level propagating strategy (Def. 11) to prove
    that S is an eager top-level propagated successor state. We consider all un-
    guarded variables y decided in S ′ by a decided bound γ. Let I ∈ C ′ be a con-
    straint with top(I) = y. The bound γ is part of M ′ , i.e., M ′ = [[M ′′ , γ, M ′′′ ]].
    As S ′ is eager top-level propagated, all other variables contained in I are
    fixed in M ′ and M ′′ . Since lower(x, M ′ ) < upper(x, M ′ ) is a condition of the
    Decide rule, the variable x is not fixed in M ′ . Therefore, x is not contained in

                                            28
    I (top(I) = y ≺ x), and I is still no conflict in S. Furthermore, all variables
    in I are still fixed in [[M ′ , x ⊲⊳J b]]. Next, we prove that the newly decided
    variable x does not violate that S is eager top-level propagated. Considering
    Def. 11.2(a) we see that Def. 20.1 is fulfilled. Similarly, Def. 11.2(b) enforces
    Def. 20.2. We conclude that S is eager top-level propagated.
 3. Let the applied rule be Unsat(-Div) or Sat. Then the successor state S is
    neither a search- or conflict-state. The Lemma is thereby trivially fulfilled.
 4. Let the applied rule be Forget. Then S ′ = hM ′ , C ′ ∪ {J}i and S = hM ′ , C ′ i.
    Therefore, any conflict I ∈ C ′ and any decision in S is also contained in S ′ .
    We conclude that S is eager top-level propagated.
 5. Let the applied rule be Slack-Intro. Then S ′ = hM ′ , C ′ i, x is a stuck variable
    in S ′ and S = hM ′ , C ′ ∪ {−xS ≤ 0, x − xS ≤ 0, −x − xS ≤ 0}i. Either Slack-
    Intro was applied before and −xS ≤ 0 ∈ C ′ or xS has upper(xS , M ) = ∞,
    and −xS ≤ 0 is not a conflict in S. Since x was stuck in S ′ , it is unfixed,
    and the top variable in the new constraints {x − xS ≤ 0, −x − xS ≤ 0}. We
    conclude that S is eager top-level propagated.
 6. Let the applied rule be Resolve-Cooper. Then S ′ = hM ′ , C ′ i and S =
    hM, C ′ ∪Rc ∪Rk i. Notice that M = prefix(M ′ , y) with y = minI∈Rc {top(I)}.
    Therefore, M is the prefix of M ′ without decisions in variables greater or
    equal to y. Since y  x for all I ∈ R and x = top(I), we deduce that any
    I ∈ R that is a conflict has no decision for its top variable x in S. Since M
    is a prefix of M ′ , every conflict I ∈ C ′ appearing in state S also appears in
    state S ′ . Now it is easy to see that S is eager top-level propagated because
    S ′ was eager top-level propagated.
 7. Let the applied rule be Solve-Div-Right. Then S ′ = hM ′ , C ′ ∪ {I1 , I2 }i and
    S = hM, C ′ ∪ {I1′ , I2′ }i. We notice that M = prefix(M ′ , y) with y = top(I2′ ).
    Therefore, M is the prefix of M ′ without decisions in variables greater or
    equal to y, which includes especially the variable x = top(I1 ). We deduce
    that neither the top variable of I1′ or I2′ is fixed by a decision. Since M is a
    prefix of M ′ , every conflict I ∈ C ′ appearing in state S also appears in state
    S ′ . Now it is easy to see that S is eager top-level propagated because S ′ was
    eager top-level propagated.
 8. Let the applied rule be Solve-Div-Left. Then S ′ = hM ′ , C ′ ∪ {I1 , I2 }i and
    S = hM ′ , C ′ ∪ {I1′ , I2′ }i. Since the bound sequence is the same in both states,
    every conflict I ∈ C ′ appearing in state S also appears in state S ′ . By
    the definition of the Solve-Div-Left rule, I2′ is no conflict in state S. Note
    that div-solve is an equivalence preserving transformation. Thus if I1′ were a
    conflict in S, and top(I1′ ) = x fixed by a Decision, then I1 or I2 is a conflict
    in S ′ . Therefore, I1′ is no conflict or top(I1′ ) = x is not decided by a Decision.
    Now it is easy to see that S is eager top-level propagated because S ′ was
    eager top-level propagated.
 9. Let the applied rule be Conflict or Conflict-Div. Then S ′ = hM ′ , C ′ i and
    S = hM ′ , C ′ i ⊢ I. It is easy to see that S is eager top-level propagated
    because S ′ is eager top-level propagated.
10. Let the applied rule be Resolve or Skip-Decision. Then S ′ = h[[M, γ]], C ′ i ⊢ J ′
    and S = hM, C ′ i ⊢ J. Since M is a prefix of M ′ , every conflict I ∈ C ′

                                           29
    appearing in state S also appears in state S ′ . Now it is easy to see that S is
    eager top-level propagated because S ′ was eager top-level propagated.
11. Let the applied rule be Learn. Then S ′ = h[[M ′ , γ]], C ′ i ⊢ I and S = hM ′ , C ′ ∪
    Ii ⊢ I. Since CUTSAT++ uses a two-layered strategy (Def. 13), I is a
    guarded constraint. Now it is easy to see that S is eager top-level propagated
    because S ′ was eager top-level propagated.
12. Let the applied rule be Backjump. Then S ′ = h[[M ′ , γ, M ′′ ]], C ′ i ⊢ I and
    S = h[[M ′ , γ ′ ]], C ′ i. Since CUTSAT++ uses a two-layered strategy (Def. 13),
    I is a guarded constraint. Now it is easy to see that S is eager top-level
    propagated because S ′ was eager top-level propagated.


    Since the initial state h[[]], C0 i fulfils the eager top-level propagated proper-
ties trivially, it is clear that CUTSAT++ produces only eager top-level states,
except for the final states. The eager top-level propagated property is so im-
portant, because it allows us to show that CUTSAT++ resolves any conflict I
it encounters. In case the conflict is a guarded constraint this is done with the
conflict rules. Otherwise, the conflict I is an unguarded constraint and CUT-
SAT++ simulates weak Cooper elimination with the strong conflict resolution
rules. First, we use Solve-Div-Left to simulate Phase I. This either ends with a
call to Solve-Div-Right resolving the conflict or CUTSAT++ finds a conflicting
core. Then the conflicting core is resolved with the rules Resolve-Cooper.

Lemma 22. Let S = hM, Ci be a state reachable by CUTSAT++. Let I ∈ C be
a conflict in state S. Then state S is not frozen.

Proof. Assume for a contradiction that state S is frozen. W.l.o.g. we assume that
x = top(I) is the smallest variable in our order that is top variable in a conflict
I ′ ∈ C. If x is a guarded variable then Conflict or Conflict-Div is applicable,
which contradicts our initial assumption! Therefore, x is an unguarded variable.
Furthermore, all variables y smaller than x are fixed. Otherwise, we deduce for
the smallest unfixed variable y that either
 – y is stuck and Slack-Intro is applicable
 – Propagate is applicable to a constraint I ′ where top(I ′ ) = y
 – C contains at least two divisibility constraints I1 , I2 that have y as their top
   variable and Solve-Div-Left or Solve-Div-Right is applicable
 – S contains a diophantine conflicting core (y, Id ) and Resolve-Cooper is ap-
   plicable
 – Decision is applicable to y because all conditions in Def. 11.2 are fulfilled
Since S is eager top-level propagated and I is a conflict with top variable x, we
know that state S contains no decision for x (Def. 20 and Lemma 21). W.l.o.g.
we assume that C contains at most one divisibility constraint Id with x as
its top variable. Otherwise, Solve-Div-Left or Solve-Div-Right are applicable,
which contradicts our initial assumption! Let x ≥ bl be the strictest lower bound
bl = bound(x, Il , M, ≥) for an inequality Il ∈ C with top variable x or −∞ if

                                           30
there is no inequality propagating a lower bound. Let x ≤ bu be the strictest
upper bound bu = bound(x, Iu , M, ≤) for an inequality Iu ∈ C with top variable
x or ∞ if there is no inequality propagating an upper bound. Since the strictly-
two-layered strategy forbids the application of Forget to unguarded constraints,
CUTSAT++ never removes an unguarded inequality. Furthermore, any bound
x ⊲⊳ b propagated from a divisibility constraint requires another bound x ⊲⊳ b′
propagated from an inequality. We deduce that bu 6= ∞ if upper(x, M ) 6= ∞ and
bl 6= −∞ if lower(x, M ) 6= −∞. Next, we do a case distinction on whether the
bounds bu and bl are finite:
 – Let bu = ∞ and bl = −∞. Then it holds for all inequalities ax + p ≤ 0 that
   lower(ax + p) = −∞. Thus I is no inequality. A divisibility constraint is only
   a conflict if lower(x, M ) 6= −∞ and upper(x, M ) 6= ∞. This contradicts the
   assumption that I is a conflict.
 – Let bu = ∞ and bl ∈ Z. Then it holds for all inequalities ax + p ≤ 0 with
   a < 0 that lower(ax + p) = −∞. Thus I is no inequality. A divisibility
   constraint is only a conflict if lower(x, M ) 6= −∞ and upper(x, M ) 6= ∞.
   This contradicts the assumption that I is a conflict.
 – Let bl = −∞ and bu ∈ Z. Then it holds for all inequalities ax + p ≤ 0
   with a > 0 that lower(ax + p) = −∞. Thus I is no inequality. A divisibility
   constraint is only a conflict if lower(x, M ) 6= −∞ and upper(x, M ) 6= ∞.
   This contradicts the assumption that I is a conflict.
 – Let bu < bl . Then (x, {Il , Iu }) is a conflicting core, and Resolve-Cooper is
   applicable. This contradicts the assumption that no rule is applicable.
 – Let {bl , . . . , bu } 6= ∅. Then I is not an inequality. If (x, {Il , Iu , Id }) is a con-
   flicting core, then Resolve-Cooper is applicable contradicting our initial as-
   sumption. Therefore, there exists a solution bd ∈ {bl , . . . , bu } for x satisfying
   Id . Let D be the set of divisibility constraints used to propagate a bound for x
   in M . All constraints D′ ⊆ D not contained in C, i.e., D′ = D \ C = D \ {Id }
   were eliminated with div-solve. It is easy to see that there exists a set of con-
   straints D∗ = D∗∗ ∪ {Id } contained in C that implies satisfiability of D:
                                       D∗ = D∗∗ ∪ {Id } → D,
   and D∗∗ contains only variables y smaller than x (Proof the same as for
   Lemma 14). In state S, the set of divisibility constraints D∗ is fixed, and
   satisfied under the partial assignment of M . Otherwise S would contain
   a conflict I ′ ∈ D∗ ⊆ C with top(I ′ ) ≺ x. This implies that the solution
   bd ∈ {bl , . . . , bu } for x that satisfies Id in M , also satisfies D ∪ {Id }. Further-
   more, all propagated constraints are satisfied if x is set to bd :
                                  lower(x, M ) ≤ bd ≤ upper(x, M ).
   This contradicts the assumption that there exists a conflict I with top(I) =
   x.


   The remainder of the proof follows directly the proof outline from above:
Theorem 23. Let S = hM, Ci be a state reachable by CUTSAT++. Then S is
not frozen.

                                             31
Proof. Assume for a contradiction that S = hM, Ci is a frozen state. It is easy
to see that CUTSAT++ can propagate at least two bounds for every guarded
variable and afterwards use a Decision to fix them. Therefore, we assume that
all guarded variables are fixed. By Lemma 22, there is no conflict in state S.
Since there is no conflict, at least one variable is unfixed or rule Sat [15] would
be applicable. Therefore, there must exist a smallest unfixed and unguarded
variable x. With the Slack-Intro-rules CUTSAT++ introduces for all variables
at least one lower or upper bound. Therefore, there exists a violation to the
conditions in Def. 11.2 or Decide would be applicable to x. Since x is the smallest
unfixed variable, condition Def. 11.2(a) holds. Def. 11.2(c) is also easy to satisfy
by applications of Solve-Div-Left or Solve-Div-Right. Therefore, Def. 11.2(b) is
violated. This implies that there exists a constraint I ∈ C that is a conflict
in S ′ = h[[M, γ]], Ci, where γ is a decision in x and x = top(I). However, by
Lemma 22, it is not possible that I ∈ C is a conflict in S or S would not be
frozen. Finally, I is a conflict only in S ′ and not S if Propagate(-Div) is applicable
to I. With Solve-Div-Left and Solve-Div-Right it is relatively easy to fulfil the
conditions for Def. 11.1 and therefore Propagate(-Div) is applicable. We conclude
that CUTSAT++ has always one applicable rule, which is a contradiction to our
assumption!


5.3   Proof for Completeness

All CUTSAT++ rules are sound, i.e., if hMi , Ci i(⊢ Ii ) =⇒CS hMj , Cj i(⊢ Ij ) then
any satisfiable assignment υ for Cj is a satisfiable assignment also for Ci . The
rule Resolve-Cooper is sound because of the Lemmas 2 and 3. The soundness
of Solve-Div-Left and Solve-Div-Right follows from the fact that div-solve is an
equivalence preserving transformation. The soundness proofs for all other rules
are either trivial or given in [15].
    Summarizing, CUTSAT++ is terminating, sound, and never reaches a frozen
state. This in combination with obvious properties of the rules Sat, Unsat, and
Unsat-Div implies completeness:

Theorem 24. If CUTSAT++ starts from an initial state h[[]], C0 i then it ei-
ther terminates in the unsat state and C0 is unsatisfiable, or it terminates with
hυ, sati where υ is a satisfiable assignment for C0 .

Proof. By Theorem 19, CUTSAT++ is terminating. By [15], and the Lemmas
2 and 3, CUTSAT++ is sound. By Theorem 23, CUTSAT++ never reaches a
frozen state. Since CUTSAT++ is terminating and never reaches a frozen state,
every application of CUTSAT++ ends via the rules Sat, Unsat, or Unsat-Div in
one of the final states. The rule Sat is only applicable in a state hM, Ci where
υ[M ] satisfies C and because of soundness also C0 . The rules Unsat and Unsat-
Div are only applicable to states hM, Ci(⊢ I) where the constraint set C contains
a trivially unsatisfiable constraint. In this case, it follows from the soundness of
the CUTSAT++ rules that C0 is unsatisfiable.

                                          32
6    Conclusion and Future Work

The starting point of our work was an implementation of CUTSAT [15] as a
theory solver for hierarchic superposition [9]. In that course, we observed diver-
gence for some of our problems. The analysis of those divergences led to the
development of the CUTSAT++ algorithm presented in this paper, which is
a substantial extension of CUTSAT by means of the weak Cooper elimination
describe in Section 3.
   As a next step, we plan to develop a prototypical implementation of CUT-
SAT++, to test its efficiency on benchmark problems. Depending on the out-
come, we consider integrating CUTSAT++ as a theory solver for hierarchic
superposition modulo linear integer arithmetic [9].
   Finally, we point at some possible improvements of CUTSAT++. We see
great potential in the development of constraint reduction techniques from (weak)
Cooper elimination [5]. For practical applicability such reduction techniques
might be crucial. The choice of the variable order ≺ has considerable impact
on the efficiency of CUTSAT++. It might be possibly to derive suitable or-
ders via the analysis of the problem structure. We might benefit from results
and experiences of research in quantifier elimination with variable elimination
orders.


References

 1. Clark Barrett, Robert Nieuwenhuis, Albert Oliveras, and Cesare Tinelli. Splitting
    on demand in sat modulo theories. In Miki Hermann and Andrei Voronkov, ed-
    itors, Logic for Programming, Artificial Intelligence, and Reasoning, volume 4246
    of Lecture Notes in Computer Science, pages 512–526. Springer Berlin Heidelberg,
    2006.
 2. Leonard Berman. Precise bounds for Presburger arithmetic and the reals with
    addition. In 18th Annual Symposium on Foundations of Computer Science (FOCS
    1977), 31 October–2 November, Providence, RI, USA, pages 95–99. IEEE, 1977.
 3. Leonard Berman. The complexity of logical theories. Theoretical Computer Sci-
    ence, 11(1):71 – 77, 1980.
 4. Martin Bromberger, Thomas Sturm, and Christoph Weidenbach. Linear integer
    arithmetic revisited. In Amy P. Felty and Aart Middeldorp, editors, Automated
    Deduction - CADE-25 - 25th International Conference on Automated Deduction,
    Berlin, Germany, August 1-7, 2015, Proceedings, volume 9195 of Lecture Notes in
    Computer Science, pages 623–637. Springer, 2015.
 5. D. C. Cooper. Theorem proving in arithmetic without multiplication. In Bernhard
    Meltzer and Donald Michie, editors, Proceedings of the Seventh Annual Machine
    Intelligence Workshop, Edinburgh, 1971, volume 7 of Machine Intelligence, pages
    91–99. Edinburgh University Press, 1972.
 6. Isil Dillig, Thomas Dillig, and Alex Aiken. Cuts from proofs: A complete and
    practical technique for solving linear inequalities over integers. In Ahmed Bouajjani
    and Oded Maler, editors, Computer Aided Verification, volume 5643 of Lecture
    Notes in Computer Science, pages 233–247. Springer Berlin Heidelberg, 2009.


                                           33
 7. Jeanne Ferrante and Charles W. Rackoff. A decision procedure for the first order
    theory of real addition with order. SIAM Journal on Computing, 4(1):69–76, March
    1975.
 8. Jeanne Ferrante and Charles W. Rackoff. The Computational Complexity of Logical
    Theories, volume 718 of LNM. Springer, 1979.
 9. Arnaud Fietzke and Christoph Weidenbach. Superposition as a decision procedure
    for timed automata. Mathematics in Computer Science, 6(4):409–425, 2012.
10. M. J. Fischer and M. Rabin. Super-exponential complexity of Presburger arith-
    metic. SIAM-AMS Proceedings, 7:27–41, 1974.
11. Martin Fürer. The complexity of presburger arithmetic with bounded quantifier
    alternation depth. Theoretical Computer Science, 18(1):105 – 111, 1982.
12. Erich Grädel. The complexity of subclasses of logical theories. PhD thesis, Univer-
    sität Basel, 1987.
13. Alberto Griggio. A practical approach to satisability modulo linear integer arith-
    metic. JSAT, 8(1/2):1–27, 2012.
14. Dejan Jovanović and Leonardo de Moura. Cutting to the chase solving linear
    integer arithmetic. In Automated Deduction - CADE-23 - 23rd International Con-
    ference on Automated Deduction, Wroclaw, Poland, July 31 - August 5, 2011.
    Proceedings, volume 6803 of Lecture Notes in Computer Science, pages 338–353.
    Springer, 2011.
15. Dejan Jovanović and Leonardo de Moura. Cutting to the chase. Journal of Auto-
    mated Reasoning, 51(1):79–108, 2013.
16. Michael Jünger, Thomas M. Liebling, Denis Naddef, George L. Nemhauser,
    William R. Pulleyblank, Gerhard Reinelt, Giovanni Rinaldi, and Laurence A.
    Wolsey, editors. 50 Years of Integer Programming 1958-2008. Springer, 2010.
17. Aless Lasaruk and Thomas Sturm. Weak quantifier elimination for the full linear
    theory of the integers. A uniform generalization of Presburger arithmetic. Ap-
    plicable Algebra in Engineering, Communication and Computing, 18(6):545–574,
    December 2007.
                           2pn
18. Derek C. Oppen. A 22       upper bound on the complexity of Presburger arithmetic.
    J. Comput. Syst. Sci., 16(3):323–332, 1978.
19. Christos H. Papadimitriou. On the complexity of integer programming. J. ACM,
    28(4):765–768, October 1981.
20. Mojzesz Presburger. Über die Vollständigkeit eines gewissen Systems der Arith-
    metik ganzer Zahlen, in welchem die Addition als einzige Operation hervortritt.
    In Comptes Rendus du premier congres de Mathematiciens des Pays Slaves, pages
    92–101, Warsaw, Poland, 1929.
21. Joachim von zur Gathen and Malte Sieveking. A bound on solutions of linear
    integer equalities and inequalities. Proceedings of the AMS, 72:155–158, 1978.
22. Volker Weispfenning. The complexity of almost linear diophantine problems. Jour-
    nal of Symbolic Computation, 10(5):395–403, November 1990.




                                          34
