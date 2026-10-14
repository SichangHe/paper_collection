                                         Verification and Validation of Convex Optimization Algorithms
                                                          for Model Predictive Control

                                                                                     Raphael Cohen∗ and Eric Feron †
                                                           Georgia Institute of Technology, School of Aerospace Engineering, Atlanta, GA 30332

                                                                                            Pierre-Loïc Garoche‡
                                                                          Onera – The French Aerospace Lab, Toulouse, 31000 France
arXiv:2005.12588v1 [cs.CL] 26 May 2020




                                                         Advanced embedded algorithms are growing in complexity and they are an essential contrib-
                                                     utor to the growth of autonomy in many areas. However, the promise held by these algorithms
                                                     cannot be kept without proper attention to the considerably stronger design constraints that
                                                     arise when the applications of interest, such as aerospace systems, are safety-critical. Formal
                                                     verification is the process of proving or disproving the "correctness" of an algorithm with re-
                                                     spect to a certain mathematical description of it by means of a computer. This article discusses
                                                     the formal verification of the Ellipsoid method, a convex optimization algorithm, and its code
                                                     implementation as it applies to receding horizon control. Options for encoding code properties
                                                     and their proofs are detailed. The applicability and limitations of those code properties and
                                                     proofs are presented as well. Finally, floating-point errors are taken into account in a numerical
                                                     analysis of the Ellipsoid algorithm. Modifications to the algorithm are presented which can be
                                                     used to control its numerical stability.


                                                                                                         Nomenclature

                                         R            =   The set of all real numbers.
                                         F            =   Set of floating-point numbers.
                                         R+           =   The set of all positive real numbers.
                                         R∗+          =   The set of all strictly positive real numbers.
                                         Rn           =   The set of real vectors of length n.
                                         Rm×n         =   The set of real matrices of size m × n.
                                         k Ak F       =   Frobenius norm of a matrix A.
                                         k Ak         =   Two norm of a matrix A.
                                         k xk         =   Two norm of a vector x.
                                         Bn           =   n-dimensional unit Euclidean ball. Bn = {z ∈ Rn : kzk ≤ 1}.
                                         Br (x)       =   Ball of radius r centered on x. Br (x) = {z ∈ Rn : kz − xk ≤ r }.
                                         Ell(B, c)    =   Ellipsoid set defined by: Ell(B, c) = {Bu + c : u ∈ Bn }.
                                         fl()         =   Floating-point rounding of a given real number.
                                         H            =   Model Predictive Control Horizon.
                                         k(A)         =   Condition number of a matrix A.
                                         N            =   Number of iterations.
                                         u            =   Plant Input.
                                         u            =   Collection of input vectors to horizon: u = [u1 . . . u H−1 ].
                                         Vol()        =   Volume of a given set.
                                         X            =   Original Decision Vector for an Optimization problem.
                                         x            =   Plant State Vector.
                                         x            =   Collection of state vectors to horizon: x = [x1 . . . x H ].
                                         Xf           =   Feasible set of an optimization problem.
                                         X           =   Epsilon optimal set of an optimization problem.
                                            ∗ Ph.D. Student, School of Aerospace Engineering, raphael.cohen@gatech.edu.
                                            † Professor of Aerospace Engineering, School of Aerospace Engineering, feron@gatech.edu.
                                            ‡ Research Scientist, Onera, pierre-loic.garoche@onera.fr.
Z          =   Projected Decision Vector for an Optimization problem.
γ          =   Upper bound of Reduction Ratio.
θ          =   Elevation Angle in Radians for the three degrees of freedom Helicopter.
λ          =   Ellipsoids Widening Coefficient.
σmax (A)   =   Largest singular value of a matrix A.
σmin (A)   =   Smallest singular value of a matrix A.
φ          =   Travel Angle in Radians for the three degrees of freedom Helicopter.
ψ          =   Pitch Angle in Radians for the three degrees of freedom Helicopter.


                                                  I. Introduction
Formal verification of optimization algorithms used online within control systems is the sole focus of this research.
Recently, such algorithms have been used online with great success for the guidance of safety-critical applications,
including, autonomous cars [1] and reusable rockets [2]. The latter case has resulted in technology demonstrations
such as the landings of SpaceX’s Falcon 9 [3] and BlueOrigin’s New Shepard. Thus, algorithms solving optimization
problems are already used online, have been embedded on board, and yet still lack the level of qualification required
by civil aircraft or manned rocket flight. Automatic code generation for solving convex optimization problems has
already been done [4, 5], but does not include the use of formal methods. Likewise, work within the field of model
predictive control already exists where numerical properties of algorithms are being evaluated [6]. Nevertheless, this
work is only valid for Quadratic Programming (See Section II) and using fixed-point arithmetic. As well, no formal
verification is performed. On the other hand, some contributions have been made concerning formal verification of
control systems [7–10], but they mainly focus on formal verification and code generation for linear control systems.
Research has also been made toward the verification of numerical optimization algorithms [11, 12], yet it remains
purely theoretical and no proof was obtained using formal verification tools. Contributions on formal verification of
optimization algorithms have already been made [13], but this work focuses on a single optimization problem, where
closed-loop behaviors are not being addressed, which does not meet the level of guarantees needed for receding horizon
controllers. As well, the formal proof was not complete and no numerical analysis was presented.
The need for enhanced safety and better performance is currently pushing for the introduction of advanced numerical
methods into the next generation of cyber-physical systems. While most of the algorithms described in this article have
been established for a long time, their online use within embedded systems is relatively new and introduces issues that
have to be addressed. Among these methods, this study focuses on numerical optimization algorithms.
The following scientific contributions are presented:
    • axiomatization of optimization problems and formalization of algorithm proof (Ellipsoid method) as code
       annotation
    • extraction of guarantees of convergence for sequential optimization problems, representing closed-loop management
    • modification of the original algorithm to account for floating-point errors
    • generation of C code implementations via credible autocoders of receding horizon controllers along with ANSI/ISO
       C Specification Language (ACSL) annotations
The choice of ellipsoid method here seems unconventional as current state of art solvers typically use some variant of
the interior-point method. However it has been shown in [13] that guaranteeing the numerical accuracy of second-order
methods are very challenging. This paper is a first attempt at providing methods and tools to formally verify convex
optimization code for solving online receding-horizon control problems. The article is structured as follows: Section II
presents backgrounds for convex optimization, model predictive control, and axiomatic semantics using Hoare triples.
Section III focuses on the axiomatization of second-order cone programs and the formal verification of the Ellipsoid
Method. Furthermore, the closed-loop management and the online aspect of the developed algorithm is discussed in
Section IV. A modified version of the original Ellipsoid Method used to control floating-point errors, is presented in
Section V. A floating-point analysis of the ellipsoid method is presented in Section VI, while Section VII presents how
this framework can be automated and applied to a system, the three degrees of freedom (DOF) Helicopter. Finally,
Section VIII concludes this article.




                                                           2
                                                   II. Preliminaries

A. Second-Order Cone Programming
Optimization algorithms solve a constrained optimization problem, defined by an objective function and a set of
constraints to be satisfied:
                                        min      fo (x)
                                                                                                            (1)
                                         s.t.    fi (x) ≤ bi for i ∈ [1, m]

This problem searches for x ∈ Rn , the optimization variable, minimizing fo ∈ Rn → R, the objective function, while
satisfying constraints fi ∈ Rn → R, with associated bounds bi . An element of Rn is feasible when it satisfies all the
constraints fi . An optimal point is defined by the element having the smallest cost value among all feasible points. An
optimization algorithm computes an exact or approximated estimate of the optimal cost value, together with one or more
feasible points achieving this value. A subclass of these problems that can be efficiently solved are convex optimization
problems. In these cases, the functions fo and fi are required to be convex [4], with one of the consequences being
that a local minimizer is also a global minimizer. Furthermore, when the constraints are linear the problem is either
called a Linear Program (LP) if the cost is also linear or called a Quadratic Program (QP) if the cost is quadratic.
Optimization problems where both the cost and the constraints are quadratic are called Quadratically Constrained
Quadratic Program (QCQP). Semi-Definite Programs (SDP) represent problems that have constraints which can be
formulated as a Linear Matrix Inequality (LMI). Here, only a specific subset of convex optimization problems are
presented in details: Second-Order Cone Programs (SOCPs). For x ∈ Rn , a SOCP in standard form can be written as:

                                       min       fT x
                                         s.t.  k Ai x + bi k 2 ≤ ciT x + di for i ∈ [1 , m]                               (2)
                                 With: f ∈ Rn, Ai ∈ Rni ×n, bi ∈ Rni , ci ∈ Rn, di ∈ R.

A classification of the most common convex optimization problems is
presented in Fig. 1. Frequently, optimization problems that are used
online for control systems can be formulated as a SOCP. Furthermore,
extensions to SDPs are possible with little additional work. The
algorithm used and the proof are still valid for any convex problem.


B. Model Predictive Control (MPC)
Model predictive control (also known as receding horizon control) is
an optimal control strategy based on numerical optimization. In this Figure 1 Classification of Some Convex Op-
technique, a discrete-time dynamical model of the system is being timization Problems
used to predict potential future trajectories. As well, a cost function, that depends on the future control inputs and states,
is being considered over the receding prediction horizon H, with the objective being to minimize this cost. At each time
t, a convex optimization problem is being solved and the corresponding input is sent to the system. A time step later, the
exact same process occurs and is repeated until a final time. We refer the reader to [14, 15] for more details on MPC.

C. Axiomatic Semantics and Hoare Logic
Semantics of programs express their behavior. Using axiomatic semantics, the program’s semantics can be defined in an
incomplete way, as a set of projective statements, i.e., observations. This idea was formalized by [16] and then [17] as a
way to specify the expected behavior of a program through pre- and post-conditions.
Hoare Logic. A piece of code C is axiomatically described by a pair of formulas (P, Q) such that when P holds before
executing C, then Q should be valid after its execution. This pair acts as a contract for the function and (P, C, Q) is called
a Hoare triple. In most uses, P and Q are expressed in first order formulas over the variables of the program. Depending
on the level of precision of these annotations, the behavior can be fully or partially specified. In our case we are
interested in specifying, at code level, algorithm specific properties such as the algorithm convergence or preservation of
feasibility for intermediate iterates. Software analyzers, such as the Frama-C platform [18], provide means to annotate
source code with these contracts, and tools to reason about these formal specifications. For the C language, ACSL [19]
(ANSI C Specification Language) can be used to write source comments.



                                                              3
Figure 2 shows an example of a function contract expressed in ACSL.             ACSL + C
The “ensures” keyword expresses all the properties that will be true
after the execution of the function, assuming that all the properties listed 1 /*@
                                                                             2    @ requires -2 <= x <= 2;
within the “requires” keywords were true before the execution (similar       3    @ ensures \result == x*x;
to a Hoare triple). As well, it is possible to annotate and check the        4    @ ensures 0 <= \result <= 4;
                                                                             5    @ assigns \nothing ;
part of the memory assigned by a function using the keyword “assigns”.       6 */
                                                                             7 double square ( double x){
In the case shown in Fig. 2, the function is not assigning anything          8    return x*x;
during its execution, and therefore no global variable were changed.         9 }

Throughout this article, the verification is performed using the software
analyzer Frama-C and the SMT solver (Satisfiability Modulo Theories)
Alt-Ergo [20], via the Weakest Precondition (WP) plug-in. The role of          Figure 2 ACSL Function Contract
the WP plug-in is to implement a weakest precondition calculus for ACSL annotations present at code level. For each
annotation, the WP plug-in generates proof obligations (mathematical first-order logic formulas) that are then submitted
to Alt-Ergo. Further information about the WP plug-in can be found in [21].


              III. Formal Verification of an Ellipsoid Method C code Implementation
Our goal is to build a framework that is capable of compiling the high-level requirements of online MPC solvers into
ACSL augmented C code which can then be automatically verified using existing formal methods tools for C programs
such as Frama-C and Alt-ergo. The MPC solver shall take a parameterized SOCP problem as inputs and always outputs
a solution that is both feasible and epsilon-optimal within a predefined number of iterations.
This kind of requirement has never been formalized before. Hence it also has never been verified by the state of art
automatic formal methods techniques and it is not really possible to do so without going into some manual proofs. To
formalize these high-level requirements, one has to:
    • formalize in ACSL the low-level types, such as vectors and matrices
    • formalize in ACSL second-order cone problems
    • formalize the solver (from algorithm and input problem to the generated C code)
    • formalize the properties of the ellipsoid method in a way such that they can be expressed as axiomatic semantic of
       the C program (ACSL types, axioms, functions to express feasability and optimality).
For example, mathematical types from linear algebra can be defined axiomatically. The input problem and solver choice
is automatically transformed into a C program. The high-level properties (feasability and optimality) of the chosen solver
together with the input problem are compiled into an ACSL form (expressing the axiomatics semantics of the generated
C program), and then inserted into the C program as comments. The various artifacts (ACSL types, functions, predicates,
axioms, lemmas, theorems), that were manually written to support the compilation of the high-level requirements (HLR)
into C+ACSL and its automatic verification, are packaged into libraries. Examples of these artifacts include types like
matrix, vector, optim, predicates like “isFeasible” and functions such as “twoNorm”, etc.


A. Semantics of an Optimization Problem
The first work to be done is the formal definition of an optimization problem. In order to do so, new mathematical types,
objects, axioms and theorems are created. Our goal is to axiomatize optimization problems with enough properties
allowing us to state all the needed optimization-level properties at code level. Let us consider the second-order cone
program, described in Eq. (2).
Encoding an SOCP. In order to fully describe an SOCP, we use the variables:

                         A1          b1          cT           d1 
                         .           .           .1           .                             h             i
         f ∈ R , A =  ..  , b =  ..  , C =  ..  , d =  ..  and also the vector m = n1 . . . nm .
                n
                         Am          bm         cT            dm 
                                                 m            
The vector m is used to collect the sizes of the vectors Ai · x + bi . Furthermore, if i=1     ni = 0, then the SOCP (2) is an
                                                                                         Ím
LP. Using ACSL, a new type and a high level function are defined, providing the possibility to create objects of the type
“optim”. Figure 3 represents an extract of the ACSL optimization theory. First, a new ACSL theory is created using the
keyword “axiomatic”. The keyword “logic” is used to define a new function and its signature. Information about the part
of memory used by a function is provided using the keyword “reads”. Figure 3 presents the definition of 2 functions. The
function socp_o f _size_2_6_0 is used to instantiate objects representing an optimization problem of appropriate sizes.


                                                              4
The function constraints returns a vector collecting the values          ACSL
of all the constraint functions for a given problem and point.
When applying a method to solve an actual optimization problem,        1 /*@
                                                                       2 axiomatic OptimSOCP {
many concepts are crucial. The work here is to highlight the           3 type optim ;
                                                                       4 logic optim socp_of_size_2_6_0 (
parts of the HLR that need to be formalized (via axiomatization)       5     matrix A, vector b, matrix C,
and packaged into a library to support the automatic compilation       6     vector d, vector f, int* m)
                                                                       7     reads m [0..5];
of the HLR into ACSL augmented C code. The concepts of                 8 logic vector constraints ( optim OPT ,
feasibility and optimality are being axiomatized. For this,            9     vector x);
                                                                      10 */
given a second-order cone program, an axiomatic definition is
given for the vector constraint, the gradient of a constraint, the
cost, optimal point (making the assumption that it exists and is         Figure 3 ACSL Optim Type Definition
unique), etc. For instance, Fig. 4 illustrates the axiomatization
of a constraint calculation and the feasibility predicate definition.
For the constraint calculation, two axioms are defined representing two different cases: The case where the constraint is
linear and the case where it is not. The predicate shown in Fig. 4 defines that a point is feasible if all the components
of its constraint vector are negative. When instantiating an object of type vector or matrix, the size of the considered

                    ACSL
                1 /*@
                2    axiom constraint_linear_axiom :
                3      \forall optim OPT , vector x, integer i;
                4        getm(OPT )[i] == 0 ==>
                5          constraint (OPT , x, i) ==
                6            -scalarProduct ( getci(OPT ,i),x, size_n (OPT ))- getdi(OPT ,i);
                7    axiom constraint_socp_axiom :
                8      \forall optim OPT , vector x, integer i;
                9        getm(OPT )[i] != 0 ==>
               10          constraint (OPT , x, i) ==
               11            twoNorm ( vector_affine ( getAi(OPT ,i),x, getbi(OPT ,i))) -
               12            scalarProduct ( getci (OPT ,i),x, size_n (OPT ))- getdi (OPT ,i);
               13    ...
               14    predicate
               15      isFeasible ( optim OPT , vector x) = isNegative ( constraints (OPT ,x));
               16 */




                                   Figure 4    ACSL Feasible Predicate Definition

object needs to be known since it is hard-coded in the ACSL axiomatization. This is not an issue since at this time (post
parsing), all the sizes of the variables used are already defined. The objects sizes only depend on the plant’s order and
the horizon. Thus, as long as the order of the plant and the horizon do not change dynamically, the variables sizes can
be predicted. Also, working with predefined and hard-coded size objects will help the analyzers proving the goals.
B. The Ellipsoid Method
Despite its modest efficiency with respect to interior point methods, the Ellipsoid Method [22–24] benefits from concrete
proof elements and could be considered a viable option for critical embedded systems where safety is more important
than performance. This section presents a way to annotate a C code implementation of the Ellipsoid Method. Before
recalling the main steps of the algorithm, some mathematical preliminaries are presented.
Ellipsoids in Rn . An ellipsoid can be characterized as an affine transformation of an Euclidean Ball. Before defining
an Ellipsoid set, the definition of an Euclidean ball is first recalled.
Definition 1 (Euclidean ball) Let n ∈ N, Vn denotes the unit                       n
                                                              Euclidean ball in R . Vol(Vn ) represents
                                                                                                        its volume. As
well, BR (x) is defined as the ball of radius R centered on x i.e {z ∈ Rn : (z − x)T (z − x) ≤ R} .

Definition 2 (Ellipsoid Sets) Let c ∈ Rn and B ∈ Rn×n , be a non-singular matrix (det(B) , 0). The Ellipsoid Ell(B, c)
is the set :
                                          Ell(B, c) = {Bu + c : uT u ≤ 1}                                         (3)
Definition 3 (Volume of Ellipsoids) Let Ell(B, c) be an ellipsoid set in Rn . V ol(Ell(B, c)) denotes its volume and is
defined as :
                                        Vol(Ell(B, c)) = |det(B)| · Vol(Vn )                                        (4)


                                                           5
Algorithm. The main steps of the algorithm detailed in [23–25] are now presented. In the following, Ek = Ell(Bk , ck )
denotes the ellipsoid computed by the algorithm at the k th iteration.

Ellipsoid cut. The algorithm starts with an ellipsoid containing the feasible set X, and therefore the optimal point x ∗ .
An iteration consists of transforming the current ellipsoid Ek into a smaller volume ellipsoid Ek+1 that also contains x ∗ .
Given an ellipsoid Ek of center ck , the objective is to find a hyperplane containing ck that cuts Ek in half, such that
one half is known not to contain x ∗ . Finding such a hyperplane is called the oracle separation step, cf. [24]. Within
the SOCP setting, this cutting hyperplane is obtained by taking the gradient of either a violated constraint or the cost
function. Then, the ellipsoid Ek+1 is defined by the minimal volume ellipsoid containing the half ellipsoid Êk that is
known to contain x ∗ . The Fig. 5a and 5b illustrate such ellipsoids cuts.




                      (a) Ellipsoid Cut                                     (b) Ellipsoid Cut In a LP Setting

                                          Figure 5   Ellipsoids Cut Illustration


Ellipsoid transformation. From the oracle separation step, a separating hyperplane, e, that cuts Ek in half with the
guarantee that x ∗ is localized in Êk has been computed. The following step is the Ellipsoid transformation. Using this
hyperplane e, one can update the ellipsoid Ek to its next iterate Ek+1 according to Eqs. (5),(6) and (7). In addition to
that, an upper bound, γ, of the ratio of Vol(Ek+1 ) to Vol(Ek ) is known.

                                            ck+1 = ck − 1/(n + 1) · Bk p ,                                              (5)
                                                                          
                                             n             n         n
                                   Bk+1 = √       Bk +         −√            (Bk p)pT                                   (6)
                                             2
                                            n −1         n + 1       2
                                                                    n −1
                                                         q
with:                                          p = Bk e/ eT Bk BkT e.
                                                     T
                                                                                                                        (7)

Termination. The search points are the successive centers of the ellipsoids. Throughout the execution of the algorithm,
the best point so far, x̂ is being stored in memory. A point x is better than a point y if it is feasible and has a smaller
cost. When the program reaches the number of iteration needed, the best point so far, x̂, which is known to be feasible
and -optimal, is returned by the algorithm. A volume related property is now stated, at the origin of the algorithm
convergence, followed by the main theorem of the method. Both properties can be found in [24, 26].
Property 1 [Reduction ratio.] Let k ≥ 0, by construction:
                                      Vol(Ek+1 ) ≤ exp{−1/(2 · (n + 1))} · Vol(Ek )                                     (8)
Please find below the the proof of this property.
Proof 1 Let us put the update formula (6) into the form:
                                            Bk+1 = αBk + β(Bk p)pT
              √                            √
With: α = n/ n2 − 1 and β = n/(n + 1) − n/ n2 − 1. Let us now take the determinant of both sides.
                                                                                           β 
         det(Bk+1 ) = det Bk · αIn + βppT = det Bk det αIn + βppT = det Bk α n det In + ppT
                                                                                 
                                                                                                 α


                                                             6
Using Sylvester’s determinant identity: det(In + AB) = det(Im + BA) ∀A ∈ Rn×m, B ∈ Rm×n , the determinant on the
right side of the equality can be put into the form:
                                                                     β    
                                          det(Bk+1 ) = α n det Bk · 1 + kpk
                                                                       α
But, from Eg. (7), one can see that kpk = 1. Therefore:

                                Vol(Ek+1 ) | det(Bk+1 )|           β        −1 
                                          =              = αn · 1 +    ≤ exp
                                 Vol(Ek )    | det(Bk )|            α         2(n + 1)
                                                                                                                     
Necessary Geometric Characteristics. In order to know the
number of steps required for the algorithm to return an -optimal
solution, three scalars and a point xc ∈ Rn are needed:
    • a radius R such that
                             X f ⊂ BR (xc )                   (9)

   • a scalar r such that there exists a point x̄ such that
                             Br ( x̄) ⊂ X f                 (10)

   • and another scalar V such that
                     max fo − min fo ≤ V .                       (11)
                      x ∈X f        x ∈X f

Figure 6 illustrates the scalars R and r. The Feasible set
(assumed to be bounded) is shown in green. The main result Figure 6 Included and Including Balls for the
can be stated as:                                          feasible set of linear constraints (shown in green)

Theorem 1 Assuming that X is bounded, non-empty and that scalars R, r and V satisfying Eqs. (9), (10) and (11) are
known. Then, for all  ∈ R∗+ , the algorithm, using N iterations, will return x̂, satisfying:
                                               fo ( x̂) ≤ fo (x ∗ ) +  and x̂ ∈ X
With N = 2n(n + 1) log    RV
                             
                          r     , n being the dimension of the optimization problem.
This result, when applied to LP, is the first proof of the polynomial solvability of linear programs. This proof can be
found in [24, 26].
C. ACSL Theory                                                   ACSL
This section would be to describe all the manually
written ACSL artifacts to support the automatic for-         1 /*@ axiomatic LinAlg {
                                                             2    type vector ;
malization and then verification of the HLR. Indeed,         3    type matrix ;
the software analyzer takes as an input the annotated        4    logic vector vec_of_16_scalar ( double * x)
                                                             5      reads x [0..15];
C code plus ACSL theories that define new abstract           6    logic vector vec_of_36_scalar ( double * x)
                                                             7      reads x [0..35];
types, functions, as well as axioms, lemmas and              8    ...
theorems. The lemmas and theorems need to be                 9    logic vector vector_add ( vector A, vector B);
                                                            10    axiom vector_add_length :
proven but the axioms are taken to be true. For the         11      \forall vector x, y;
SMT solver, properties within C code as annotations         12        vector_length (x) == vector_length (y) ==>
                                                            13        vector_length ( vector_add (x,y)) ==
are usually harder to prove than lemmas within an           14          vector_length (x);
                                                            15    axiom vector_add_select :
ACSL theory. On top on checking the mathematical            16      \forall vector x, y, integer i;
correctness of an ACSL annotation, the SMT solver           17        vector_length (x) == vector_length (y) ==>
                                                            18        0 <= i < vector_length (x) ==>
needs to check the soundness of the code itself (e.g.,      19        vector_select ( vector_add (x,y),i) ==
memory allocation, function calls, ACSL contracts           20
                                                            21    ...
                                                                      vector_select (x,i)+ vector_select (y,i);
on the function called, etc). Thus, the approach            22 }
                                                            23 */
chosen here is to develop as much as possible the
ACSL theories to express and prove the main results
used by the algorithm. That way, the Hoare triples at
                                                                        Figure 7     ACSL Linear Algebra Theory
code level are only an instantiation of those lemmas
and are relatively simple to prove.

                                                                 7
Linear Algebra Based ACSL Theory. In this ACSL theory, new abstract types for vectors and matrices are defined.
Functions allowing the instantiation of those types of objects are also defined. As well, all of the well-known operations
have also been axiomatized, such as vector-scalar multiplication, scalar product, norm etc. This ACSL theory is
automatically generated during the autocoding process of the project and all the sizes of the vectors and matrices are
known. Thus, within this theory, only functions that will create objects, from a C code pointer, of appropriate sizes (as
illustrated in Fig. 7) are being defined. ACSL code is printed in green and its keywords in red. The C code keywords are
printed in blue and the actual C code is printed in black. Using the keyword “type”, two new abstract types, matrix and
vector are being defined. Furthermore, the ACSL constructors for those types and the axiomatization of vector addition
is shown in Fig. 7. The first axiom states that the length of the addition of two vectors, of same length is equal to this
same length. The second axiom states that the elements of the addition of two vectors is the addition of the elements of
the two separate vectors. Figure 7 shows a partial sample of the autocoded ACSL linear algebra theory.
Optimization and Ellipsoid Method Based ACSL Theory. The axiomatization of optimization problems has already
been briefly discussed in Section III.A. Additionally, work has been dedicated to axiomatize the calculation of the vector
constraint, feasibility, epsilon-optimality, etc. As well,
                                                                ACSL
Ellipsoids and related properties are formally defined,
such as those presented in Fig. 8. Figure 8 presents          1 # include " axiom_linalg .h"
the definition of another theory called “Ellipsoid” and       2 /*@ axiomatic Ellipsoid {
                                                              3    type ellipsoid ;
within it, it shows the creation of a new abstract type       4    logic ellipsoid Ell( matrix P, vector x);
“ellipsoid” and the definition of the functions “Ell” and     5    logic boolean inEllipsoid ( ellipsoid E,
                                                              6         vector z);
“inEllipsoid”. The function “Ell” returns the Ellipsoid       7    ...
                                                              8 }
formed by the matrix P and vector x as defined in             9 */
Eq. (3). The function “inEllipsoid” returns true if the
vector z is in the Ellipsoid E and returns false otherwise.
As it was explained earlier, Theorem 1 was translated                  Figure 8 Ellipsoid Type Definition
to ACSL and auto generated as ACSL lemmas. All the
autocoded lemmas are proven using the software analyzer Frama-C and the SMT solver Alt-Ergo. One of the autocoded
lemmas can be found in Fig. 9 and can be expressed using common mathematical notations as:
                          Assuming: 0 < /V < 1 ; 0 <  ; ∀x, y ∈ X, fo (x) − fo (y) ≤ V ;
        ∀z ∈ R , z < Ell(P, x), =⇒ xbest is better than z and Vol(Ell(P, x)) < X /V
               n
                                                                                         Then: xbest is  − optimal.
A formal definition is also given for a point x being better than another point y. The set X /V represents the set obtained
by shrinking the feasible set X f by a factor /V centered on the optimal point x ∗ . Further details about this set can be
found in [24].

        ACSL Lemma
    1 /*@
    2  lemma epsilon_solution_lemma :
    3     \forall optim OPT , real r,V,epsilon , matrix P, vector x, x_best ;
    4        (0 < epsilon /V < 1) ==> 0 < r ==> 0 < V ==> 0 < epsilon ==>
    5      size_n (OPT) > 0 ==>
    6      ( \forall vector x1 , x2; isFeasible (OPT , x1) ==> isFeasible (OPT , x2) ==>
    7        cost(OPT ,x1) - cost(OPT ,x2) <= V ) ==>
    8      ( \forall vector z; ! inEllipsoid (Ell(P,x), z) ==> isBetter (OPT , z, x_best ) ) ==>
    9      ( \exists vector x; include ( tomyset (Ell( mat_mult_scalar ( ident ( size_n (OPT )),r), x)) ,
   10                feasible_set (OPT )) ) ==>
   11       volume ( tomyset (Ell(P,x))) < pow( epsilon /V*r, size_n (OPT )) ==>
   12       isEpsilonSolution (OPT , x_best , epsilon );
   13 */




                                      Figure 9    Ellipsoid Method Main Lemma


D. Annotating C Code
Details are now given about how the C code is annotated and the type of Hoare triples used. For this, a specific technique
was adopted. Every C code function is implemented in a separated file. That way, for every function, a corresponding C
code body (.c) file and header file (.h) are automatically generated. The body file contains the implementation of the


                                                             8
function along with annotations and loop invari-                  C Code + ACSL
ants. The header file contains the declaration of the
function with its ACSL contract. The first kind of            1 # ifndef getNorm_2_lib
                                                              2 # define getNorm_2_lib
Hoare triples and function contracts added to the             3 # include " axiom_linalg .h"

code were to check basic mathematical operations.             4 # include " my_sqrt .h"
                                                              5 # include " scalarProduct_2 .h"
Figure 10 shows an ACSL contract relative to the              6 /*@

C code function computing the 2-norm of a vector              7    @ requires \valid (Ain +(0..1));
                                                              8    @ ensures \result ==
of a size two. The ACSL contract specifies that the           9         twoNorm ( vec_of_2_scalar (Ain ));
variable returned is positive and equal to the 2-norm        10    @ ensures \result >= 0;
                                                             11    @ assigns \nothing ;
of the vector of size two described by the input             12    @ behavior Ain_non_null :
pointer. Using the keywords “behavior”, “disjoint”           13      @ assumes nonnull ( vec_of_2_scalar (Ain ));
                                                             14      @ ensures \result > 0;
and “complete” one can specify the different scenar-         15    @ behavior Ain_null :
                                                             16      @ assumes ! nonnull ( vec_of_2_scalar (Ain ));
ios possible and treat them separately. Furthermore,         17      @ ensures \result == 0;
it is proved that the result is always positive or null,     18    @ complete behaviors Ain_non_null , Ain_null ;
                                                             19    @ disjoint behaviors Ain_non_null , Ain_null ;
and assuming the corresponding input vector not              20 */
equal to zero, the output is strictly greater than zero.     21 double getNorm_2 ( double *Ain );
                                                             22 # endif
This last property becomes important when one
must prove there are no divisions by zero (normal-
izing vectors). The implementation of the function                    Figure 10    getNorm_2 Header C Code File
is presented in Fig. 11. Once all the C functions
implementing elementary mathematical operations
have been annotated and proven, the next step con-                        C Code + ACSL
sists of annotating the higher level C functions such                 1 # include " getNorm_2 .h"
as constraint and gradient calculations, matrix and                   2 double getNorm_2 ( double *Ain) {
                                                                      3    double sum;
vector updates, etc. Please find in Fig. 12 as an                     4    sum = scalarProduct_2 (Ain , Ain );
example, the annotated C function for the function                    5    return my_sqrt (sum ); }
“getp” that computes the vector p as described in
Eq. (7), needed to perform the ellipsoid update. In
                                                                       Figure 11   getNorm_2 Body C Code File

      C Code + ACSL
  1  # include "getp.h"
  2  void getp () {
   3    double norm;
   4    double norm_inv ;
   5    getTranspose ();
   6    /*@ assert mat_of_2x2_scalar (& temp_matrix [0])==
   7      transpose ( mat_of_2x2_scalar (& P_minus [0])); */
   8    changeAxis ();
   9    /*@ assert vec_of_2_scalar (& temp2 [0]) == mat_mult_vector (
  10      mat_of_2x2_scalar (& temp_matrix [0]) , vec_of_2_scalar (& grad [0])); */
  11    /*@ assert vec_of_2_scalar (& temp2 [0]) == mat_mult_vector ( transpose (
  12      mat_of_2x2_scalar (& P_minus [0]) ), vec_of_2_scalar (& grad [0])); */
  13    norm = getNorm_2 ( temp2 );
  14    /*@ assert 1/ norm == 1/ twoNorm ( mat_mult_vector (
  15      transpose ( mat_of_2x2_scalar (& P_minus [0]) ), vec_of_2_scalar (& grad [0]))); */
  16    /*@ assert vec_of_2_scalar (& temp2 [0]) == mat_mult_vector ( transpose (
  17      mat_of_2x2_scalar (& P_minus [0])) , vec_of_2_scalar (& grad [0])); */
  18    norm_inv = 1.0 / (norm );
  19    scaleAxis ( norm_inv );
  20    /*@ assert 1/ norm == 1/ twoNorm ( mat_mult_vector ( transpose (
  21      mat_of_2x2_scalar (& P_minus [0])) , vec_of_2_scalar (& grad [0]))); */
  22    /*@ assert vec_of_2_scalar (& temp2 [0]) == mat_mult_vector ( transpose (
  23      mat_of_2x2_scalar (& P_minus [0])) , vec_of_2_scalar (& grad [0])); */
  24    /*@ assert vec_of_2_scalar (&p [0])== vec_mult_scalar ( vec_of_2_scalar (& temp2 [0]) ,1/ norm ); */
  25 }




                                           Figure 12       getp.c Body C Code File

Fig. 12 one can note the presence of several function calls followed by ACSL annotations, encoding the corresponding
specifications. The first function call refers to the function “getTranspose” which computes the transpose of the matrix
“P_minus” and stores it into the variable “temp_matrix”. The function “changeAxis” multiplies the matrix “temp_matrix”


                                                                  9
by the vector “grad” and stores the result into the vector “temp2”. The current state of the memory is specified at each
line of code using ACSL annotations. Then, after computing the norm and scaling the vector “temp2”, the annotations
specify that the resulting vector stored in the variable p has indeed been calculated as stated in Eq. (7).


                                    IV. Sequential Optimization Problems
In this section, convergence guarantees are provided for a class of optimization problems used online. For this, an
optimization problem with parameterized constraints and cost will be considered. This section concerns the study of
how this parameter affects the optimization problem at each iteration and how to find the condition that the parameter
needs to satisfy in order to prove convergence for every point along the trajectory.
First, the study focuses on the special case of linear constraints. Following this, another section will be dedicated to
SOCP constraints.


A. Parameterized Linear Constraints
The objective is to solve in real-time the optimization problem described in Eq. (12). The vector X ∈ Rn x denotes the
decision vector.
                                                  minimize fo (X)
                                                       X                                                          (12)
                                                  subject to AX ≤ b
The initialization of this optimization problem is done using Eq. (13), where S is a full rank matrix. Usually, S represents
a selector matrix and is of the form: [I p O p×(n x −p) ]. A selector matrix is a matrix that selects one or more component
from X. If S is a selector matrix then SX returns certain components of X. In that case it is obviously full rank. xo
denotes the input of the controller and it is written x̂o to account for the fact that xo changes from one optimization
problem to another.
                                                            SX = x̂o                                                    (13)
One can decompose and separate the equality and inequality constraints hidden behind the matrix A and vector b. That
way, Eq. (12) can be written as:
                                                minimize fo (X)
                                                      X
                                                subject to     Aeq X = beq                                               (14)
                                                               Aineq X ≤ bineq
                                                               SX = x̂o
The idea here is to project all the equality constraints in order to eliminate them while keeping track of the variable
parameter, x̂o . There exist matrices M, A1 and A2 such that for all vectors X satisfying the equality constraints of the
problem defined by Eq. (14), there exists a vector Z such that:
                                                   X = A1 beq + A2 x̂o + M Z                                             (15)
Equation (15) is a direct implication that the set of solutions of a linear systemis an affine set. In this same equation, M
is a matrix formed by an orthonormal basis of the null space of the matrix Aeq and d denotes the total number of
                                                                                     S
equality constraints (number of rows of Aeq + number of rows of S). The vector Z then belongs to Rnz with nz = nx − d.
Thus, the original optimization problem described by Eq. (12) is equivalent to the projected problem:

                                           minimize       fo (A1 beq + A2 x̂o + M Z)
                                               Z                                                                         (16)
                                           subject to     Af Z ≤ bo + Q x̂o

With:                     Af = Aineq M ;     bo = bineq − Aineq A1 beq        and      Q = −Aineq A2 .                   (17)
More details and references about equality constraints elimination can be found in [4]. Using the Ellipsoid Method
online to solve this optimization problem requires the computation of geometric characteristics on the feasible set of this
parametric optimization problem for every possible xo . For that reason, for now, let us assume: k xo k 2 ≤ ro .
The parameterized polyhedral set below Px̂o is defined as:
                                            Px̂o = {z ∈ Rnz : Af z ≤ bo + Q x̂o }                                        (18)
Having this collection of polyhedral sets, the goal is to compute ball radii that will tell us about the volume of the
feasible set that would be true for every xo . The operator ν(.) returns for a matrix A the vector ν(A) whose coordinates


                                                              10
are the 2-norm of the rows of A. Thus, a way of computing those geometric characteristics is to consider the two extreme
polyhedral sets below:
                                        Pmin = {z ∈ Rnz : Af z ≤ bo − ro ν(Q)},                                      (19)
                                        Pmax = {z ∈ Rnz : Af z ≤ bo + ro ν(Q)}.                                      (20)
In order to give an example of this concept, please find
in Fig. 13 an illustration of such polyhedral sets (the
illustrated sets have no physical meaning and do not
represent any MPC problem). The two extreme polyhedral
sets are drawn with solid lines and the actual feasible
polyhedral sets are drawn using dotted lines. The values
used are:

     −1     1             1         1
     1      1             1         2
                                     
     1     −0.5
                            1
                                      1
Af =  0           , ν(Q) =     , b   = 1.5 and ro = 0.5.
                                        
                                    o
             1             1
                            
                                        
     −1     0            1         0.5                        Figure 13    Pmax and Pmin Polyhedral Sets
                                      
     0
            −1           1
                             
                                        0.5
                                         

Fact 1 [Extreme Polyhedral Sets]
                                  ∀xo ∈ Rn s.t. k xo k 2 ≤ ro , Pmin ⊂ Px̂o ⊂ Pmax .

Proof 2 Take xo such that k xo k 2 ≤ ro .
First, using the Cauchy-Schwarz inequality, one can write:
                         |(Qxo )(i)| = |row(Q, i)T xo | ≤ krow(Q, i)k 2 k xo k 2 ≤ ν(Q)(i)ro ∀i                      (21)
                                           =⇒ −ν(Q)ro ≤ Qxo ≤ ν(Q)ro .
Then, if x ∈ Pmin , one can conclude that Af x ≤ bo − ro ν(Q). Using the inequality above, it is clear that it implies
x ∈ Pxo . Similarly, assuming that x ∈ Pxo and using the inequality below, it is clear that x ∈ Pmax .              

Next, one needs to find three scalars r, R and V such that:

                                            ∃ z¯1 such that B( z¯1, r) ⊂ Pmin ,                                      (22)
                                        ∃ z¯2 such that Pmax ⊂ B( z¯2, R) ,                                          (23)
                                   V ≥ max fo (z) − min fo (z) , ∀ k x̂o k ≤ ro .                                    (24)
                                        z ∈Px̂ o        z ∈Px̂ o

For the first scalar, r, one can compute a numerical value by running an off-line optimization problem finding the largest
ball inside Pmin . If no solution can be found, the value of ro needs to be decreased, and the process is repeated until
acceptable values for ro and r are found. Further information about finding the largest ball in a polytope can be found
in [4].
As a consequence of equality constraint elimination, and seen in Eq. (15), the relation between the original decision
vector X and the projected vector Z can be written as:
                                                            " #
                                                             beq
                                                  X = Aproj       + M Z.                                              (25)
                                                             x̂o

The decision vector X can now be decomposed into two parts, x and u. The part u is bounded due to constraints in the
original optimization problem (described by Eq. (12)). If no constraints on u were originally present, one can construct
bounds on the projected vector Z to make the problem bounded and simpler to analyze. The point here being that from
bounded variables within the vector X, one can infer bounds on the projected vector Z. There is no need to have original




                                                              11
bounds specifically on the collection of future inputs. Rewriting Eq. (25) yields:
                                          " # "            #" # " #
                                            x      A11 A12 beq         M1
                                               =                   +        Z.                                       (26)
                                           u       A21 A22 x̂o         M2

Following this, one can conclude:
                                              Z = M2−1 u − A21 beq − A22 x̂o .
                                                                            
                                                                                                                     (27)
Therefore assuming again that k x̂o k ≤ ro , one can compute a value of R such that:

                                    kZ k ≤ M2−1 kuk + A21 beq + k A22 k ro = R.
                                                                              
                                                                                                                     (28)

On the other hand, from the physical meaning of the variables and the constraints of the optimization problem, one can
construct bounds in which the variables should live, and therefore find a lower bound for V.
With the values R and r, one can now guarantee the convergence of a family of optimization problems parameterized by
xo .
Theorem 2 [MPC Ellipsoid Method Convergence]
The problem given by Eq. (14) is run in an online fashion in order to implement receding horizon control.
Using the Ellipsoid Method and initializing the first Ellipsoid by B( z¯2, R), the method will find an -solution using N
iterations for all x̂o such that k x̂o k ≤ ro , with:
                                                                        RV
                                                      N = 2n(n + 1) log
                                                                         r 
with the variables z¯2 , r, R and V satisfying the Eqs. (22), (23) and (24). The variable n denotes the dimension of the
parameterized optimization problem.

Proof 3 . Let us assume, the problem given by Eq. (14) is run online. For each iteration, the input parameter xo
is assumed to satisfy k xo k ≤ ro . Xf denotes the feasible set of the current optimization problem to solve. That way,
Eq. (22) is satisfied. Thus, by definition of r, we know that:
                                           ∃ z¯1 such that B( z¯1, r) ⊂ Pmin ⊂ X f .
Similarly, because it is assumed that R satisfies Eq. (23), the following property holds:
                                               ∃ z¯2 such that X f ⊂ B( z¯1, r).
As well, the scalar V satisfies Eq. (11). Finally, One can conclude that the returned point will indeed be -optimal using
N iterations thanks to Theorem 1.                                                                                       

Linear Programs: In the case of Linear Programs, the method developed is identical and having a linear cost, the scalar
V is easily found by running the two optimization problems below.

                   minimize      cT (A1 beq + A2 x̂o + M z)        maximize        cT (A1 beq + A2 xo + M z)
                       x̂ o ,z                                        x o ,z
                                 Af z ≤ bo + Q x̂o                                 Af z ≤ bo + Qxo
                                 k x̂o k 2 ≤ ro                                    k xo k 2 ≤ ro

B. Second-Order Conic Constraints
In the last section, the fact that only linear constraints was present was used to find the radius r. Therefore, in this
section we aim to give ways of computing these constants for second-order constraints. Consider that one wants to solve
a model predictive control optimization problem given by Eq. (29).

                                  minimize      fo (X)
                                       X
                                                k Ai X + bi k 2 ≤ ciT X + di , i = 1 . . . m                         (29)
                                                Aeq X = beq
                                                SX = x̂o

We assume that no equality constraints are hidden in the second-order constraints (if not, a very simple analysis will
confirm this and one can extract those equality constraints and put it into the couple (Aeq, beq ) from equation (29)).


                                                              12
Performing again an equality constraint elimination, we end up with an equivalent optimization problem, of smaller
dimension, that contains no equality constraint. We want to find the radius of the biggest ball inside the feasible set
of this latter problem. Unfortunately, second-order constraints are still present and finding the largest balls inside
second-order cones is not an easy task. For this, we use the equivalence of norms in finite dimensions, noting that k·k 1
and k·k ∞ are linear, to perform a linear relaxation on the second-order constraints and end up with a polyhedral set as
the feasible set. For instance, the problem described by Eq. (30) represents a linear relaxation of the original problem
stated in Eq. (29) after having eliminated the equality constraints.
                                                0
                                 minimize     fo (Z)
                                      X
                                              √      0    0            0       0                                           (30)
                                                n Ai Z + bi        ≤ ciT Z + di , i = 1 . . . m
                                                              ∞

Thus, by finding the largest ball inside the resulting feasible set (which is a polyhedral set), a ball is finally found inside
the original second-order cone.

                                       V. Bounding the Condition Number
The use of the Ellipsoid Method was justified by arguing that it represents a trade off between performance and safety.
As well, it also attracted our attention for its numerical properties. Although at first, the Ellipsoid Method appears to be
numerically stable, finding a priori bounds on the program’s variables is challenging. The worst case occurred when the
separating hyperplane has the same direction at each iteration. In this case, the condition number of the successive
ellipsoids increases exponentially, and so do the program’s variables. This worst case is very unlikely to happen in
practice. Nevertheless, a mathematical way to get around this case is needed, along with a way to compute a priori
bounds on the variables before the execution of the program. In this section, a method for controlling the condition
number of the successive ellipsoids and a way to compute those bounds by adding a correcting step in the original
algorithm is presented. This section also includes how the formal proof of the corresponding software is modified to
support the correctness of the resulting modified ellipsoid algorithm.


A. Bounding the Singular Values of the Successive Ellipsoids
When updating Bi by the usual formulas√of the ellipsoid algorithm (Eq. (6)), Bi evolves according to Bi+1 = Bi Di , where
Di has n − 1 singular values equal to n/ n2 − 1, and has one singular value equal to n/(n + 1). It follows that at a single
step the largest and the smallest singular values of Bi can change by a factor from [1/2, 2]. The objective is to prove that
one can modify the algorithm to bound the singular values of the matrix Bi throughout the execution of the program.
Minimum Half Axis: First, we claim that if σmin (Bi ) is less than than r/V then the algorithm has already found an
-solution. Note that the scalar  is the desired precision and the scalars r and V are defined in Section III. Please find
below a proof of this statement.
Proof 4 Let us assume σmin (B) < r/V. In this case, Ei is contained in the strip between two parallel hyperplanes, the
width of the strip being less than 2 · r/V and consequently Ei does not contain X = θ X f + (1 − θ)x∗ , where x∗ is the
minimizer of fo and θ = /V (because X contains a ball of radius r/V). Consequently, there exists z ∈ X f such that
y = θz + (1 − θ)x∗ ∈ X but < Ei , implying by the standard argument (developed in [24]) that the best value f + of f
processed so far for feasible solutions satisfies f + ≤ f (y) ≤ f (x∗ ) + θ f (z − x∗ ) which implies that f + ≤ f (x∗ ) + . We
can thus stop the algorithm and return the current best point found (feasible and smallest cost).                              
Maximum Half Axis: We argue now that one can modify the original ellipsoid algorithm         √ in order to bound the value of
the maximum singular value of Bi . When the largest singular value of B√    i is less than 2R n + 1, we carry out a step as in
the basic ellipsoid method. When this singular value is greater than 2R n + 1, a corrective step is applied to Bi , which
transforms Ei into Ei+ . Under this corrective step, Ei+ is a localizer along with Ei , specifically Ei ∩ X f ⊂ Ei+ ∩ X f , and
additionally:
     (a) The volume of Ei+ is at most γ (upper bound of reduction ratio from Eq. (8)) times the volume of Ei ;
                                                          √
     (b) The largest singular value of Bi+ is at most 2R n + 1.
                                                                                          √
The corrective step is described as follows. First, define σ = σmax (Bk ) > 2R n + 1 and let ei be a unit vector
corresponding to the singular direction. We then consider:
                                                            √                  √
                                             p                                           
                                   G = diag n/(n + 1), n + 1/σ, . . . , n + 1/σ .


                                                              13
This case is concluded by performing the update:
                                       Bi+1 = Bi · G and ci+1 = ci − (eTi ci ) · ei .                                   (31)
Please find in Fig. 14 an illustration of this corrective step. The ellipsoid Ei shown in Fig. 14 appears to have a condition
number too high due to its large semi-major axis. The correction step as detailed previously has been performed and the
corrected ellipsoid Ei+ is shown with dotted line. As one can see, the volume as been decreased and the area of interest
Ei ∩ X f (dotted area) still lies within the ellipsoid Ei+ . Hence, one can conclude that throughout the execution of the
code:
                                       1 r     r                               √            √
                        σmin (Bi ) ≥         =        and σmax (Bi ) ≤ 2 × 2R n + 1 = 4R n + 1.
                                       2V       2V

B. Corresponding Condition Number
From the definition of the condition number, one can
write:
       k(B) = kBk · B−1 = σmax (B)/σmin (B).

Thus, by bounding the singular values of B, a bound on
its condition number can be constructed. The factors 1/2
and 2 that could affect the singular values of B at each
iteration are also taken into account to get:
                     √           √
               2 2R n + 1     8R n + 1
                          !            !
       k(B) ≤     ·         =
              1/2   r/V        r/V
and                              √
              kBk = σmax (B) ≤ 4R n + 1.
                                                               Figure 14 Corrective step for Ellipsoid Ei according to
                                                               Eq. (31). The feasible set X f is illustrated as the unit
C. Corresponding norm on c                                     ball.
At each iteration it is known that the optimal point belongs
to the current ellipsoid. Thus:
                          k x ∗ − ck k = kBk uk ≤ kBk k · kuk ≤ kBk k ,        for some u ∈ B1 (0).
Finally,
                                                kck k ≤ R + k xc k + kBk k .

D. Consequences on the Code
In this section, we explain how to implement this correcting step and give the tools to verify it. In order to detect an
ellipsoid with large semi-major axis, the largest singular value σmax of the current matrix Bk needs to be computed.
However, performing a singular value decomposition would be far too expensive and slow (this decomposition being
performed at each iteration). The Frobenius norm, defined in Def. 4, which is a well-known upper bound on the
maximum singular value, is computed instead.
Definition 4 The Frobenius norm of a matrix A ∈ Rn×n is:
                                                          v
                                                          u
                                                          tÕ  n Õn
                                                k Ak F =           ai,2 j
                                                                i=1 j=1

The Frobenius norm of a vector has been axiomatized by setting it equal to the vector 2-norm of the “vectorized” matrix.
A matrix is “vectorized” by concatenating all its rows in a single vector. In the case of an overly large semi-major axis,
the direction e in which this axis lies is needed as well. Therefore, the power iteration algorithm is performed in order to
compute this information.


                                       VI. Floating-Point Considerations
Standard notation is used for rounding error analysis [27–29], fl() being the result of the expression within the parenthesis
rounded to the nearest floating-point number. The relative rounding error unit is written u and eta denotes the underflow


                                                               14
unit. For IEEE 754 double precision (binary64) we have u= 2−53 and eta= 2−1074 .
This section presents an analysis targeting the numerical properties of the ellipsoid algorithm. Contributions already have
been made concerning finite-precision calculations within the ellipsoid method [26]. However, this work only shows
that it is possible to compute approximate solutions without giving exact bounds, and is only for Linear Programming
(LP). Also, the analysis performed considers abstract finite-precision numbers and the actual machine floating-point
types are not mentioned. Thanks to the analysis performed in this section, using the IEEE standard for floating-point
arithmetic and knowing exactly how the errors are being propagated, it is possible to check a posteriori the correctness
of the analysis using static analyzers [30, 31].
A. Preliminaries
Within this algorithm, we focus our attention on the update formulas (5), (6) and (7), allowing us to update the current
ellipsoid into the next one. In order to propagate the errors due to rounding through the code, we state now a useful
theorem dealing with matrix perturbations and inverses.
Theorem 3 [32][Matrix perturbations and Inverse] Let A be a non-singular matrix of Rn×n and ∆A a small perturbation
of A. Then,
                                       (A + ∆A)−1 − A−1             k∆Ak
                                                             ≤ k(A)                                            (32)
                                               A−1                   k Ak

B. Norms and Bounds
To successfully perform the algorithm’s numerical stability analysis, we need to know how “big” the variables can
grow within the execution of the algorithm. Indeed, for a given computer instruction, the errors due to floating-point
arithmetic are usually proportional to the variables values. As it was explained in Section V, we slightly modified the
ellipsoid algorithm to keep the condition numbers of the ellipsoid iterates under control. Therefore, implementing this
corrected algorithm, we can use the following results:
                                                             √
                                             kpk = BT e / eT BBT e = 1,                                            (33)
                                                              √
                                                   kBk ≤ 4R n + 1,                                                 (34)
                                                            √
                                               k(B) ≤ (8RV n + 1)/(r),                                            (35)
                                                      kck ≤ R + k xc k + kBk ,                                            (36)
where n, R, r, V, xc and  are the variables described in Section III.

C. Problem Formulation and Results
In order to take into account the uncertainties on the variables due to floating-point rounding, the algorithm is modified
to make it more robust. Those uncertainties are first evaluated and a coefficient λ is then computed. This coefficient
represents how much the ellipsoid Ek is being widened at each iteration (see Fig. 15). Let us assume we have B ∈ Fn×n ,
p ∈ Fn , c ∈ Fn . We want to find λ ≥ 1 ∈ R such that:
                                                                          
                                             Ell B, c ⊂ Ell λ · fl(B), fl(c) .                                       (37)


Before evaluating any of those rounding errors, Lemma
1 is stated, which gives a sufficient condition for the
coefficient λ to have Ell λ · fl(B), fl(c) covering Ell(B, c).
If the calculations of B and c were perfect, using Lemma
1, λ = 1 would be a solution; no correction is indeed
necessary.
Lemma 1 [Widening - Sufficient Condition]                         Figure 15 Ellipsoid Widening
                      −1          −1                                                   
                fl B B + fl B           · kc − fl(c)k ≤ λ =⇒ Ell B, c ⊂ Ell λ · fl(B), fl(c) .


                                               −1               −1
Proof 5 The starting hypothesis is: fl B             B + fl B          · kc − fl(c)k ≤ λ. Using the fact that the two norm is a
consistent norm, we have:


                                                                 15
                                  −1                −1                         −1                             −1
           ∀ u ∈ B1 (0) , fl B          Bu ≤ fl B          B   and       fl B            c − fl(c)       ≤ fl B          · kc − fl(c)k .
Therefore using these properties and the assumed starting property, we have:
                                                   −1           −1          
                               ∀ u ∈ B1 (0) , fl B Bu + fl B        · c − fl(c) ≤ λ.
Then, using the triangle Inequality (k x + yk ≤ k xk + k yk), we finally have:
                                                         −1                
                                    ∀ u ∈ B1 (0) , fl B     · Bu + c − fl(c) ≤ λ.
Reformulating the second part of the above statement (we are assuming that λ > 0):
                                                                            −1          
                    ∀ u1 ∈ B1 (0) , z = Bu1 + c → ∃ u2 ∈ B1 (0) , λ · fl(B)     · z − fl(c) = u2 .
Using the definition of Ellipsoids described in Eq. (3), one can write the equivalent statement:
                                                                         −1          
                              ∀ z ∈ Ell(B, c), ∃ u2 ∈ B1 (0) , λ · fl(B)     · z − fl(c) = u2 .
Rearranging the equation implies:
                                    ∀ z ∈ Ell(B, c), ∃ u2 ∈ B1 (0) , z = λ · fl(B)u2 + fl(c).
Again, this is equivalent to:                                                       
                                           ∀ z ∈ Ell(B, c) → z ∈ Ell λ · fl(B), fl(c) .
which is the desired property:                                              
                                                Ell B, c ⊂ Ell λ · fl(B), fl(c) .

                                                                                                                                             
The floating-point errors ∆B , ∆B−1 and ∆c are defined as:
                          ∆B = fl(B) − B , ∆c = fl(c) − c , ∆B−1 = (fl(B))−1 − (B)−1 .                                                     (38)
For now, it is assumed that after performing the floating-point analysis, E B and E c have been found such that:
                          |(∆B )i, j | ≤ E B   ∀i, j ∈ [1, n],       and         |(∆c )i | ≤ E c         ∀i ∈ [1, n].
From Lemma 1, one can see that the calculation of a widening coefficient λ highly depends on the accuracy of the
matrix fl(B)−1 . Therefore, E B−1 is also needed such that: |(∆B−1 )i, j | ≤ E B−1 ∀i, j ∈ [1, n].
The quantity (B)−1 is not used explicitly in the algorithm and its floating-point error could not be evaluated by numerically
analyzing the method. Instead, perturbation matrix theory [32] and Theorem 3 will be used, which gives a lower bound
on E B−1 given E B , the norm of B and its condition number. The result is stated as follows.
Lemma 2 [Widening - Analytical Sufficient Condition]
            k(B) √      √
                                                         
                                             k(B)                                             
         1+        n · n · k(B)E B + E c +        nE B E c ≤ λ =⇒ Ell B, c ⊂ Ell λ · fl(B), fl(c) .
            kBk                              kBk

Proof 6 To prove this lemma, k∆B−1 k is first evaluated. Using Eq. (32):

                                                               B−1         k 2 (B)
                                          k∆B−1 k ≤ k(B)           k∆B k =         k∆B k .
                                                               kBk         kBk 2
                                                                     2
But, k∆B k ≤ k∆B k F ≤ nE B , which implies: k∆B−1 k ≤ k (B)2 nE B . The three constants I, J and K are now defined:
                                                         kB k
          −1               −1
I = fl B B , J = fl B           and K = kc − fl(c)k.
The next step consists of computing an upper bound for each of those constants.
                                                                                 k 2 (B)
                           I = kIn + ∆B−1 Bk =⇒ I ≤ kIn k + k∆B−1 k kBk = 1 +            nE B,
                                                                                  kBk
                                                           k(B)        k(B)      
                                   J ≤ (B)−1 + k∆B−1 k =         · 1+        nE B ,
                                                            kBk         kBk
                                                         √
                                                     K ≤ nE c .
So, if


                                                                   16
                          k(B) √      √
                                                                     
                                                         k(B)
                     1+          n · n · k(B)E B + E c +      nE B E c ≤ λ =⇒ I + J · K ≤ λ,
                          kBk                            kBk
then                                             −1               −1
                                         fl B          B + fl B          · kc − fl(c)k ≤ λ.

Using the result of Lemma 1, one can conclude on the inclusion property (37).                                           

Thus, due to Lemma 2, following the floating-point analysis of the algorithm, a coefficient λ such that Eq. (37) is valid
can now be computed. After finding such a λ, using over-approximation schemes, we consider how the algorithm’s
convergence changes. Because the method’s proof lies with the fact that the final ellipsoid has a small enough volume,
this correction has an impact on the guaranteed number of iterations. Lemma 3 addresses those issues.
Lemma 3 [Convergent Widening Coefficient] Let n ∈ N, n ≥ 2.
The algorithm implementing the widened ellipsoids, with coefficient λ converges if:
                                             λ < exp 1/(n(n + 1)) .
                                                                    
                                                                                                                      (39)
In that case, if N denotes the original number of iteration needed, the algorithm implementing the widened ellipsoids
will require:
                                       Nλ = N/ 1 − n(n + 1) · log(λ) iterations
                                                                     
                                                                                                                 (40)


Proof 7 We recall that the Ellipsoid algorithm implementing the widened ellipsoids, with coefficient λ converges if:
                                      Vol λ · Ell(Bk+1, ck+1 ) < Vol Ell(Bk , ck ) .
                                                                                  
When using the Ellipsoid algorithm update process (with or without condition number correction), we have:
                                       Vol Ell(Bk+1, ck+1 ) ≤ γ · Vol Ell(Bk , ck )
                                                                                   
With γ = exp(−1/(2(n + 1))), and Eq. (4), we know that:
                                 Vol Ell(λ · Bk+1, ck+1 ) = λ n/2 · Vol Ell(Bk+1, ck+1 )
                                                                                        
Therefore, the algorithm implementing the widened ellipsoids, with widening coefficient λ will converge if:
                            λ n/2 · γ < 1 which is equivalent to λ < exp 1/(n(n + 1))
                                                                                           
                                                                                                                    
Proof 8 The second statement of Lemma 3 is now proved, which shows how to compute the updated number of
iterations for the algorithm implementing widened ellipsoids. We introduce Bk+10   = λBk+1 . Therefore using Eq. (4), and
Vol(Ek+1 ) = λ · Vol(Ek+1 ) , we get:
       0        n/2
                                                 0 )
                                          Vol(Ek+1            0 )
                                                        Vol(Ek+1  Vol(Ek+1 )
                                   γλ =               =                      = λ n/2 · γ.
                                           Vol(Ek )     Vol(Ek+1 ) Vol(Ek )
To end up at the final step with an ellipsoid of the same volume, we need: Vol(Eo ) · γλNλ = Vol(Eo ) · γ N . Which implies
                                           Nλ log(γ) + n/2 · log(λ) = N log(γ).
                                                                    

Replacing γ by its value, using property 1 from Section III.B:
                                                               
                                  Nλ n/2 · log(λ) − 1/(2(n + 1)) = −N/(2(n + 1))
And thus, we arrive at the formula:             Nλ = N/{1 − n(n + 1) log(λ)}.                                           


D. Computing E B and E c
This section introduces the evaluation of the floating-point errors taking place when performing the update formulas (5)
and (6) (represented by E c and E B ). For this, numerical properties for basic operations appearing in the algorithm are
first presented.
Rounding of a Real. Let z ∈ R, z̃ = fl(z) = z + δ + η with |δ| < u and |η| < eta/2
Product and Addition of Floating-Points. Let a, b ∈ F.
                            fl(a + b) = (a + b)(1 + 1 )                        with |1 | < u
                    fl(a × b) = (a × b)(1 + 2 ) + η2     with |2 | < u, |η2 | < eta and 2 · η2 = 0
Reals-Floats Product. Let z ∈ R and a ∈ F, |fl fl(z) · a − z · a| ≤ |z||a| · u + |a| · 2u(1 + u)
                                                           




                                                                  17
Scalar Product. Let a, b ∈ Fn . We define, ha, bi =                                  =
                                                             Ín                          Ín
                                                              i=1 ai bi and |a, b|         i=1 |ai bi |. We have then:
                                               |flha, bi − ha, bi| ≤ An |a, b| + Γn
                                   With:     An = n · u/(1 − n · u) and Γn = A2n · eta/u

Rounding Error on c. Knowing how the errors are being propagated through elementary transformations, the goal is
to compute the error for a transformation similar to the vector c’s update. For each component of c, we have:
                                                             
                                        ci = ci − 1/{n + 1} · hRowi (B), pi.
Therefore, the operation performed, in floating-point arithmetic is:
                            fl c + fl fl(z) · flha, bi    with: a, b ∈ Fn, c ∈ F and z ∈ R.
                                                       
                                                                                                                           (41)
Using this and neglecting all terms in eta and powers
                                                     of u greater than two, we get:
                                       E c ≤ u · 16n2 + 16n + 3 · kBk + kck .
                                                                 
                                                                                                                           (42)

Error on B. Similarly, for each component of B, the operation below is performed:
                                             Bi, j = α · Bi, j + β · hRowi (B), pi · p j .
In floating-point arithmetic, this last equation can be put into form:
                                                                                       
                                                                                        
                                        fl fl fl(z1 ) · d + fl fl(z2 ) · fl flha, bi · c .
Similarly, propagating the errors using elementary transformations implies that:
                                                                                                  !
                                                        n /{1 − nu} + 2 | β| + n + 2|α| + 1 .
                                                         2                 
                                    E B ≤ u · kBk ·                                                                        (43)



                                VII. Automatic Code Generation and Examples

A. Credible Autocoding
Credible autocoding, is a process by which an implementation of a certain input model in a given programming language is
being generated along with formally verifiable evidence that the output source code correctly implements the input model.
The goal of the work presented in this article is to automatically generate, formally verifiable C code implementations of
a given receding horizon controller. Thus, an autocoder that we call a “Credible Autocoder” (see Fig. 16 ) has been
built that generates an ACSL annotated C code implementation of a given MPC controller. This autocoder takes as an
input a formulation of a MPC controller written by the user in a text file. Once the output code is generated, it can
be checked using the software analyzer Frama-c and the plugin WP. If the verification terminates positively, the code
correctly implements the wanted receding horizon control. The controller can then be compiled and the binary file
embedded in a feedback control loop. The specification and the requirements are automatically generated from the
input text file written by the user. The verification taking place in this work is applied to one high-level requirement (of
the MPC solver). The other high-level requirements such as those involving control-related issues are not examined.
Nevertheless, given that the input text file is written in
a high-level language, specifically designed for MPC
formulations, it is relatively simple to read. The use of
autocoders for automated MPC code generation makes
the formulation easier to check and add traceability to the
algorithms.


B. Example: the three degree-of-freedom helicopter
The three degree-of-freedom (3 DOF) helicopter shown
in Fig. 17 was used to illustrate the framework developed
in this article. The vector state of the system collects the 3
axis angles and rates and it is denoted by x = [θ ψ φ θÛ ψÛ φ].
                                                            Û
The inputs are the voltages of the front and back DC motors.                   Figure 17      Quanser – 3 DOF Helicopter


                                                                  18
                                    Figure 16    Credible Autocoding Framework


Further information about the 3 DOF helicopter can be found in [33]. Given an inner feedback controller and a
discretization step of T = 0.5 sec, the resulting system is a stable linear system. The problem we are trying to solve is a
landing of the 3 DOF helicopter. Starting with an angle of 25 deg in elevation, 15 deg in travel (see Fig. 17 for axis) and
all the other states being zero, the objective is to design a controller that can drive the system back to the origin while
avoiding the ground. The ground is the area below θ = 0. Thus, the constraint for enforcing ground avoidance is a
formula on the elevation and the pitch angles and can be formulated as: h sin(θ) ± d sin(φ) >= 0. By linearizing this
constraint over small angles, one can obtain linear inequalities of the form: Aobs x ≤ bobs . We want to implement the
following MPC controller.
                                               ÕH
                                   minimize          k xk k
                                   X=[x,u]
                                              k=1
                                             xk+1 = Axk + Buk , k = 1..H − 1                                          (44)
                                             kuk k ≤ 60 , k = 1..H − 1
                                             0 ≤ xk (1) and Aobs xk ≤ bobs , k = 2..H
                                             x1 = x̂o
Assuming that k x̂o k ≤ 27, we found, using the method developed in Section IV a radius 8.0612 (running an off-line
optimization problem that finds the largest ball inside Pmin ). Similarly, R = 322, was obtained using Eq. (28). From the
problem formulation, one can see that the norms of the successive x’s along the trajectory constructed are supposed to
be minimized. Given a starting point, an upper bound on the objective function over the feasible set can be computed.
The objective function is maximal when xo has the largest norm, and when the system stays at this point throughout the
trajectory. The constant V can therefore be computed as:
                                        V = H · k xo k ≤ H · 27 = 6 × 27 = 162.                                       (45)
Following those calculations, a number of step of N = 5528 is found. In order to control floating-point errors, a widening
coefficient λ can be constructed. Performing the steps described in Section VI, using double precision floating-points
and an accuracy of  = 0.25 result in:
                                               λ = 1.000695409372118.
As it was explained in Section VI, the ellispoid widening increased the number of iterations needed for the convergence
to Nλ = 6817. The simulation was ran on a Intel Core i5-3450 CPU @ 3.10GHz × 4 processor and the running time
was approximately 0.2 sec for a single point. The results of the simulation can be found in Fig. 18a and 18b. Figure 18a
presents the closed-loop response for the state vector x and Fig. 18b shows the lowest altitude point with time for
the same simulation. The text file presented in Fig. 19 has been used to generate the C code in order to perform the
simulation. The whole simulation was executed using the autocoded C code and a Simulink model. The full autocoder




                                                            19
source code, input file (Fig. 19), Simulink model and a user guide for the autocoder can be found online∗ .




                 (a) State Vector versus time                                    (b) Lowest Altitude versus time

                                                Figure 18     Simulation Data



                     Input File to the Autocoder
                 1  Input
                 2  xo (6)
                  3 Output
                  4 u(: ,1)
                  5 Constants
                  6 H = 6; M = H -1; l = 90; r = 40;
                  7 A = [0.7101      0.0000   -0.0000     0.2331    0.0000      0.0000;
                  8        0.0000    0.2105     0.4023    0.0000    0.0977      0.7390;
                  9      -0.0000    -0.1272     0.9846   -0.0000   -0.0134      0.4733;
                 10      -0.8721     0.0000   -0.0000     0.0724    0.0000      0.0000;
                 11      -0.0000    -2.0777     0.7830    0.0000   -0.2674      1.6711;
                 12      -0.0000    -0.4224   -0.1072    -0.0000   -0.0618      0.8109];
                 13 B = [0.2899      0.0000;     -0.0000   -0.4023; 0.0000      0.0154;
                 14        0.8721    0.0000;      0.0000   -0.7830; 0.0000      0.1072];
                 15 Aobs = [-l    -r 0 0 0 0; -l r 0 0 0 0]; bosbt = [0;0];
                 16 Variables
                 17 x(6,H) u(2,M)
                 18 Minimize
                 19 sum( || x(:,k) || , k = 1..H )
                 20 SubjectTo
                 21 constraint1 : x(: ,1) = xo;
                 22 constraint2 : x(:,k+1) = A*x(:,k) + B*u(:,k)    ,k=1..H -1;
                 23 constraint3 : -30 <= u(1,k)                     ,k=1..H -1;
                 24 constraint4 : u(1,k) <= 30                      ,k=1..H -1;
                 25 constraint5 : -30 <= u(2,k)                     ,k=1..H -1;
                 26 constraint6 : u(2,k) <= 30                      ,k=1..H -1;
                 27 constraint8 :   0 <= x(1,k)                     ,k=2..H;
                 28 constraint9 : -40 <= x(2,k)                     ,k=2..H;
                 29 constraint10 : x(2,k) <= 40                     ,k=2..H;
                 30 constraint11 : Aobs*x(:, k) <= bosbt            ,k=2..H;
                 31 Information
                 32 r = 8.06; R = 322; V = 162; eps = 0.25; lambda = 1.000695409372118;




                       Figure 19     3 DOF Helicopter Landing Problem: Autocoder Input File

   ∗ The source code for the autocoder is available at: https://cavale.enseeiht.fr/quanser_mpc/




                                                               20
                                                      VIII. Conclusion
In this article, we presented a formal framework for the automatic generation and verification of optimization code for
solving second-order cone programs. We focused on the ellipsoid method due to its good numerical characteristics. We
built a framework capable of compiling the high-level requirements of online receding horizon solvers into C code
programs which can then be automatically verified using existing formal methods tools. The credible autocoding
framework developed is targeting a certain type of convex optimization problems and the high-level requirements
formalized are appropriately chosen. However, if additional high-level requirements are needed, some manual
formalization are needed. Although high-level requirements formalization can be complex, the struggle during this task
is to formalize the low-level mathematical types and predicates needed. Hence, this task being already done, the same
mathematical foundations can be used and the formalization of additional high-level requirements within the credible
autocoder is highly simplified.
A numerical analysis of the method has been presented, showing how to propagate the errors due to floating-point
calculations through the operations performed by the program. A modified version of the algorithm was presented,
allowing us to compute “reasonable” a priori bounds on floating-points errors. However, the numerical analysis
performed remains for now purely manual. Its correctness depends on the exactitude of equations obtained manually
and no verification tools was used for this part. Future work shall include the use of formal methods to validate the
numerical analysis.


                                                     Acknowledgments
This work was partially supported by projects ANR ASTRID VORACE, ANR FEANICSES ANR-17-CE25-0018, and
NSF CPS SORTIES under grant 1446758. The authors would also like to thank Pierre Roux from ONERA for reviewing
this work, and Arkadi Nemirovski for sharing how the Ellipsoid method can be modified to keep the ellipsoid’s condition
number bounded.


                                                          References
 [1] Jerez, J. L., Goulart, P. J., Richter, S., Constantinides, G. A., Kerrigan, E. C., and Morari, M., “Embedded Online Optimization
     for Model Predictive Control at Megahertz Rates,” IEEE Trans. Automat. Contr., Vol. 59, No. 12, 2014, pp. 3238–3251.
     doi:10.1109/TAC.2014.2351991, URL http://dx.doi.org/10.1109/TAC.2014.2351991.
 [2] Açikmese, B., III, J. M. C., and Blackmore, L., “Lossless Convexification of Nonconvex Control Bound and Pointing Constraints
     of the Soft Landing Optimal Control Problem,” IEEE Trans. Contr. Sys. Techn., Vol. 21, No. 6, 2013, pp. 2104–2113.
     doi:10.1109/TCST.2012.2237346, URL http://dx.doi.org/10.1109/TCST.2012.2237346.
 [3] Blackmore, L., The Bridge, Liveright New York, 2016. URL https://www.nae.edu/File.aspx?id=164381.
 [4] Boyd, S., and Vandenberghe, L., Convex optimization, Cambridge University Press, New York, NY, USA, 2004.
 [5] Mattingley, J., and Boyd, S., “CVXGEN: A code generator for embedded convex optimization,” Optimization and Engineering,
     Vol. 13, No. 1, 2012, pp. 1–27.
 [6] Patrinos, P., Guiggiani, A., and Bemporad, A., “A dual gradient-projection algorithm for model predictive control in fixed-point
     arithmetic,” Automatica, Vol. 55, 2015, pp. 226–235.
 [7] Feron, E., “From Control Systems to Control Software,” Control Systems, IEEE, Vol. 30, No. 6, 2010, pp. 50 –71. doi:
     10.1109/MCS.2010.938196.
 [8] Champion, A., Delmas, R., Dierkes, M., Garoche, P.-L., Jobredeaux, R., and Roux, P., “Formal methods for the analysis of
     critical control systems models: Combining non-linear and linear analyses,” International Workshop on Formal Methods for
     Industrial Critical Systems, Springer, 2013, pp. 1–16.
 [9] Herencia-Zapana, H., Jobredeaux, R., Owre, S., Garoche, P.-L., Feron, E., Perez, G., and Ascariz, P., “PVS linear algebra
     libraries for verification of control software algorithms in C/ACSL,” NASA Formal Methods Symposium, Springer, 2012, pp.
     147–161.
[10] Roux, P., Jobredeaux, R., Garoche, P.-L., and Féron, É., “A generic ellipsoid abstract domain for linear time invariant systems,”
     Proceedings of the 15th ACM international conference on Hybrid Systems: Computation and Control, ACM, 2012, pp. 105–114.
[11] Wang, T., Jobredeaux, R., Pantel, M., Garoche, P.-L., Feron, E., and Henrion, D., “Credible autocoding of convex optimization
     algorithms,” Optimization and Engineering, Vol. 17, No. 4, 2016, pp. 781–812.
[12] Wei, H., “Numerical stability in linear programming and semidefinite programming,” 2006.
[13] Cohen, R., Davy, G., Feron, E., and Garoche, P.-L., “Formal Verification for Embedded Implementation of Convex Optimization
     Algorithms,” IFAC-PapersOnLine, Vol. 50, No. 1, 2017, pp. 5867–5874.
[14] Blackmore, L., Acikmese, B., and Scharf, D. P., “Minimum-landing-error powered-descent guidance for Mars landing using
     convex optimization,” Journal of guidance, control, and dynamics, Vol. 33, No. 4, 2010, pp. 1161–1171.



                                                                 21
[15] Borrelli, F., Falcone, P., Keviczky, T., Asgari, J., and Hrovat, D., “MPC-based approach to active steering for autonomous
     vehicle systems,” International Journal of Vehicle Autonomous Systems, Vol. 3, No. 2, 2005, pp. 265–291.
[16] Floyd, R. W., “Assigning Meanings to Programs,” Proceedings of Symposium on Applied Mathematics, Vol. 19, 1967, pp.
     19–32.
[17] Hoare, C. A. R., “An axiomatic basis for computer programming,” Commun. ACM, Vol. 12, 1969, pp. 576–580.
[18] Cuoq, P., Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J., and Yakobowski, B., “Frama-C: a software analysis perspective,”
     Springer, 2012, pp. 233–247.
[19] Baudin, P., Filliâtre, J.-C., Marché, C., Monate, B., Moy, Y., and Prevosto, V., “ACSL: ANSI/ISO C Specification Language.
     Version 1.11.” http://frama-c.com/download/acsl.pdf, 2016.
[20] Conchon, S., Contejean, E., and Iguernelala, M., “Canonized Rewriting and Ground AC Completion Modulo Shostak Theories :
     Design and Implementation,” Logical Methods in Computer Science, Vol. 8, No. 3, 2012.
[21] Frama-C, 2019. URL https://frama-c.com/wp.html.
[22] Grötschel, M., Lovász, L., and Schrijver, A., “The ellipsoid method and its consequences in combinatorial optimization,”
     Combinatorica, Vol. 1, No. 2, 1981, pp. 169–197.
[23] Bland, R. G., Goldfarb, D., and Todd, M. J., “The ellipsoid method: A survey,” Operations research, Vol. 29, No. 6, 1981, pp.
     1039–1091.
[24] Nemirovski, A., Introduction to Linear Optimization, Lecture notes, Georgia Institute of Technology, 2012.
[25] Boyd, S. P., and Barratt, C. H., Linear controller design: limits of performance, Prentice Hall Englewood Cliffs, NJ, 1991.
[26] Khachiyan, L. G., “Polynomial algorithms in linear programming,” USSR Computational Mathematics and Mathematical
     Physics, Vol. 20, No. 1, 1980, pp. 53–72.
[27] Rump, S. M., “Verification of positive definiteness,” BIT Numerical Mathematics, Vol. 46, No. 2, 2006, pp. 433–452.
[28] Rump, S. M., “Error estimation of floating-point summation and dot product,” BIT Numerical Mathematics, Vol. 52, No. 1,
     2012, pp. 201–220.
[29] Roux, P., Jobredeaux, R., and Garoche, P., “Closed loop analysis of control command software,” Proceedings of the 18th
     International Conference on Hybrid Systems: Computation and Control, HSCC’15, Seattle, WA, USA, April 14-16, 2015, 2015,
     pp. 108–117. doi:10.1145/2728606.2728623, URL http://doi.acm.org/10.1145/2728606.2728623.
[30] Goubault, E., and Putot, S., Static Analysis of Finite Precision Computations, Springer Berlin Heidelberg, Berlin, Heidelberg,
     2011, pp. 232–247. doi:10.1007/978-3-642-18275-4_17, URL https://doi.org/10.1007/978-3-642-18275-4_17.
[31] Putot, S., Goubault, E., and Martel, M., Static Analysis-Based Validation of Floating-Point Computations, Springer Berlin
     Heidelberg, Berlin, Heidelberg, 2004, pp. 306–313. doi:10.1007/978-3-540-24738-8_18, URL https://doi.org/10.1007/
     978-3-540-24738-8_18.
[32] El Ghaoui, L., “Inversion error, condition number, and approximate inverse of structured matrices,” Linear Algebra and its
     Applications, Vol. 342, No. 1–3, 2002.
[33] Quanser, “3-DOF Helicopter Reference Manual,” , n.d. URL https://www.lehigh.edu/~inconsy/lab/frames/
     experiments/QUANSER-3DOFHelicopter_Reference_Manual.pdf.




                                                                 22
