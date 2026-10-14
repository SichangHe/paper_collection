                                                  Polynomial invariants by linear algebra

                                                    Steven de Oliveira1, Saddek Bensalem2 , Virgile Prevosto1
                                                         1
                                                              CEA, LIST, Software Reliability and Security Lab
                                                             {steven.deoliveira,virgile.prevosto}@cea.fr
                                                                      2
                                                                        Université Grenoble Alpes
                                                                       saddek.bensalem@imag.fr
arXiv:1611.07726v1 [cs.LO] 23 Nov 2016




                                               Abstract. We present in this paper a new technique for generating poly-
                                               nomial invariants, divided in two independent parts : a procedure that
                                               reduces polynomial assignments composed loops analysis to linear loops
                                               under certain hypotheses and a procedure for generating inductive in-
                                               variants for linear loops. Both of these techniques have a polynomial
                                               complexity for a bounded number of variables and we guarantee the
                                               completeness of the technique for a bounded degree which we success-
                                               fully implemented for C programs verification.



                                         1    Introduction
                                         When dealing with computer programming, anyone should be aware of the un-
                                         derlying behavior of the whole code, especially when it comes to life-critical
                                         projects composed of million of lines of code [10]. Manual code review cannot
                                         scale to the size of actual embedded programs. Testing allows to detect many
                                         vulnerabilities but it is never enough to certify their total absence. Indeed, the
                                         cost of generating and executing sufficient test cases to meet the most stringent
                                         coverage criteria [4] that are expected for critical software becomes quickly pro-
                                         hibitive as the size of the code under test grows. Alternatively, formal methods
                                         techniques based on abstraction allow us to prove the absence of error.
                                             However, since a program can, at least in theory, have an infinite number of
                                         different behaviors, the verification problem is undecidable and these techniques
                                         either lose precision (emitting false alarms) and/or require manual input. One of
                                         the main issue of such approach is the analysis of loops, considered as a major
                                         research problem since the 70s [2]. Program verification based on Floyd-Hoare’s
                                         inductive assertion [9] and CEGAR-like techniques [7] for model-checking uses
                                         loop invariants in order to reduce the problem to an acyclic graph analysis [3]
                                         instead of unrolling or accelerating loops [11]. Thus, a lot or research nowadays
                                         is focused on the automatic inference of loop invariants [16,21].
                                             We present in this paper a new technique for generating polynomial invari-
                                         ants, divided in two independent parts : a linearization procedure that reduces
                                         the analysis of solvable loops, defined in [21], to the analysis of linear loops ; an
                                         inductive invariant generation procedure for linear loops. Those two techniques
                                         are totally independent from each other, we aim to present in this article their
                                         composition in order to find polynomial invariants for polynomial loops. We also
add an extension of this composition allowing to treat loops with complex be-
haviors that induces the presence of complex numbers in our calculation. The
linearization algorithm has been inspired by a compiler optimisation technique
called operator strength reduction [8]. Our invariant generation is completely in-
dependent from the initial state of the loop studied and outputs parametrized
invariants, which is very effective on programs using a loop multiple times and
loops for which we have no knowledge of the initial state. In addition to being
complete for a certain class of polynomial relations, the invariant generation
technique has the advantage to be faster than the already existing one for such
loops as it relies on polynomial complexity linear algebra algorithms.
    Furthermore, a tool implementing this method has been developped in the
Frama-C framework for C programs verification [14] as a new plug-in called
Pilat (standing for Polynomial Invariants by Linear Algebra Tool). We then
compared our performances with Aligator [16] and Fastind [5], two invariant
generators working on similar kinds of loops. First experiments over a represen-
tative benchmark exposed great improvements in term of computation time.


Outline. The rest of this paper is structured as follows. Section 2 introduces
the theoretical concepts used all along the article and the kind of programs we
focus on. Section 3 presents the application of our technique on a simple example.
Section 4.1 presents the linearization step for simplifying the loop, reducing
the problem to the study of affine loops. Section 4.2 presents our contribution
for generating all polynomial invariants of affine loops. Section 4.3 extends the
method with the treatment of invariants containing non-rational expressions.
Finally, section 5 compares Pilat to Aligator and Fastind. .


State of the art. Several methods have been proposed to generate invariants
for kinds of loops that are similar to the ones we address in this paper. In partic-
ular, the weakest precondition calculus of polynomial properties in [19] is based
on the computation of the affine transformation kernel done by the program.
This method is based on the computation of the kernel of the affine transfor-
mation described by the program. More than requiring the whole program to
be affine, this method relies on the fact that once in the program there exists
a non-invertible assignment, otherwise the kernel is empty. This assumption is
valuable in practice, as a constant initialization is non- invertible, so the re-
sults may appear at the end of a whole-program analysis and highly depend on
the initial state of the program. On the other hand, our method can generate
parametrized invariants, computable without any knowledge of the initial state
of a loop, making it more amenable to modular verification.
    From a constant propagation technique in [18] to a complete invariant gen-
eration in [21], Gröbner bases have proven to be an effective way to handle
polynomial invariant generation. Such approaches have been successfully imple-
mented in the tool Aligator [16]. This tool generates all polynomial invariants
of any degree from a succession of p-solvable polynomial mappings in very few
steps. It relies on the iterative computation of Gröbner bases of some polynomial
ideals, which is a complicated problem proven to be EXPSPACE-complete [17].
    Attempts to get rid of Gröbner bases as in [5] using abstract interpreta-
tion with a constant-based instead of a iterative-based technique accelerates the
computation of invariants by generating abstract loop invariants. However, this
technique is incomplete and misses some invariants. The method we propose
here is complete for a particular set of loops defined in [21] in the sense that it
finds all polynomial relations P of a given degree verifying P (X) = 0 at every
step of the loop, and has a polynomial complexity in the degree of the invariants
seeked for a given number of variables.


2     Preliminaries
Mathematical background. Given a field K, Kn is the vector space of di-
mension n composed by vectors with n coefficients in K. Given a family of vector
Φ ⊂ Kn , V ect(Φ) is the vector space generated by Φ. Elements of Kn are de-
noted x = (x1 , ..., xn )t a column vector. Mn (K) is the set of matrices of size
n ∗ n and K[X] is the set of polynomials using variables with coefficients in K.
We note K the algebraic closure of K, K = {x|∃P ∈ K[X], P (x) = 0}. We will
use h., .i the linear algebra standard notation, hx, yi = x · y t , with · the standard
dot product. The kernel of a matrix A ∈ Mn (K), denoted ker(A), is the vector
space defined as ker(A) = {x|x ∈ Kn , A.x = 0}. Every matrix of Mn (K) admits
a finite set of eigenvalues λ ∈ K and their associated eigenspaces Eλ , defined as
Eλ = ker(A − λId), where Id is the identity matrix and Eλ 6= {0}. Let E be a
K vector space, F ⊂ E a sub vector space of E and x an element of F . A vector
y is orthogonal to x if hx, yi = 0. We denote F ⊥ the set of vectors orthogonal to
every element of F .

Programming model. We use a basic programming language whose syntax
is given in figure 1. V ar is a set of variables that can be used by a program,
and which is supposed to have a total order. Variables take value in a field K.
A program state is then a partial mapping V ar ⇀ K. Any given program only
uses a finite number n of variables. Thus, program states can be represented as a
vector X = (x1 , ..., xn )t . In addition, we will note X ′ = (x′1 , ..., x′n )t the program
state after an assignment. Finally, we assume that for all programs, there exists
xn+1 = x′n+1 = 1 a constant variable always equal to 1.
    The i OR i instruction refers to a non-deterministic condition.
    Each i will be refered to as one of the bodies of the loop.
    Multiple variables assignments occur simultaneously within a single instruc-
tion. We say that an instruction is affine when it is an assignment for which
the right values are affine. If not, we divide instructions in two categories with
respect to the following definition, from [21]

Definition 1 Let g ∈ Q[X]m be a polynomial mapping. g is solvable if there
exists a partition of X into subvectors of variables x = w1 ⊎ ... ⊎ wk such that
     i ::= i ; i                                        exp ::=       cst ∈ K
         | (x1 ,..,xn ):=(exp1 ,...,expn )                          | x ∈ V ar
         | i OR i                                                   | exp + exp
         | while (∗) do i done                                      | exp ∗ exp



                                   Fig. 1: Code syntax


∀j, 1 6 j 6 k we have

                          gwj (x) = Mj wjT + Pj (w1 , ..., wj−1 )

   with (Mi )16i6k a matrix family and (Pi )16i6k a family of polynomial map-
ping.

   An instruction is solvable if the associated assignment is a solvable polynomial
mapping. Otherwise, it is unsolvable. Our technique focuses on loops containing
only solvable instructions, thus it is not possible to generate invariants for nested
loops. It is however possible to find an invariant for a loop containing no inner
loop even if it is itself inside a loop, that’s why we allow the construction.


3    Overview of our approach
Steps of the generation. In order to explain our method we will take the
following running example, for which we want to compute all invariants of degree
3:
 while ( ∗ ) do
    ( x , y ) := ( x + y ∗y , y + 1 )
 done
Our method is based on two distinct parts :

 1. reduction of the polynomial loop to a linear loop;
 2. linear invariant generation from the linearized loop.

    We want to find a linear mapping f that simulates the behavior of the poly-
nomial mapping P (x, y) = (x + y 2 , y + 1). To achieve this, we will express the
value of every monomial of degree 2 or more using brand new variables. Here,
the problem comes from the y 2 monomial. In [19], it is described how to con-
sider the evolution of higher degree monomials as affine applications of lower or
equal degree monomials when the variables involved in those monomials evolve
affinely. We extend this method to express monomials transformations of the
loop by affine transformations, reducing the problem to a simpler loop analysis.
For example here, y ′ = y + 1 is an affine assignment, so there exists an affine
representation of y2 = y 2 , which is y2′ = y2 + 2.y + 1. Assuming the initial y2
is correct, we are sure to express the value of y 2 with the variable y2 . Also, if
we want to find invariants of degree 3, we will need to express all monomials
of degree 3, i.e. xy and y3 the same way. (monomials containing xi with i > 2
are irrelevant as their expression require the expression of degree 4 monomials).
Applying this method to P gives us the linear mapping f (x, y, y2 , xy, y3 , 1) =
(x + y2 , y + 1, y2 + 2.y + 1, xy + x + y2 + y3 , y3 + 3.y2 + 3.y + 1, 1), with 1 the
constant variable mentioned in the previous section.
    Now comes the second part of the algorithm, the invariant generation. Infor-
mally, an invariant for a loop is a formula that

 1. is valid at the beginning of the loop ;
 2. stays valid after every loop step.

    We are interested in finding semi-invariants complying only with the second
criterion such that they can be expressed as a linear equation over X, containing
the assignment’s original variables and the new ones generated by the lineariza-
tion procedure. In this setting, a formula satisfying the second criterion is then
a vector of coefficients ϕ such that

                              hϕ, Xi = 0 ⇒ hϕ, f (X)i = 0                                (1)

By linear algebra, the following is always true

                                hϕ, f (X)i = hf ∗ (ϕ), Xi                                (2)

where f ∗ is the dual of f . If ϕ happens to be an eigenvector of f ∗ (i.e. there
exists λ such that f ∗ (ϕ) = λϕ), the equation (1) becomes

                         hϕ, Xi = 0 ⇒ hf ∗ (ϕ), Xi = 0 by (2)
                         hϕ, Xi = 0 ⇒ hλ.ϕ, Xi = 0
                         hϕ, Xi = 0 ⇒ λ. hϕ, Xi = 0

which is always true. We just need to transpose the matrix representing f to
compute f ∗ . It returns f ∗ (x, y, y2 , y3 , 1) = (x, y + y2 + y3 , x + y2 + 3.y3 , y3 , y +
y2 + y3 + 1, y + y2 + y3 + 1). f ∗ only admits the eigenvalue 1. The eigenspace of f ∗
associated to 1 is generated by two independants vectors, e1 = (−6, 1, −3, 2, 0)t
and e2 = (0, 0, 0, 0, 1)t. Eventually, we get the formula Fk1,k2 = (k1 .(−6.x + y −
3.y2 + 2.y3 ) + k2 .1 = 0) as invariant, with k1 , k2 ∈ Q. By writing k = − kk12 and
replacing 1 with 1, we can rewrite it with only one parameter, Fk = (−6.x +
y − 3.y2 + 2y3 = k). In this case, information on the initial state of the loop
allows to fix the value of the parameter k. For example if the loop starts with
(x = 0, y = 0), then −6.x + y − 3.y 2 + 2.y 3 = 0, and F0 is an invariant. The
next section will show how the work done on our example can be generalized on
any (solvable) loop. In particular, section 4.1 will deal with the linearization of
polynomial assignments. Then we will see in section 4.2 that the eigenspace of
the application actually represents all the possible invariants of f and that we
can always reduce them to find a formula with only one parameter.
Extension of the basic method. The application’s eigenvector may not
always be rational. For example, applying the previous technique on a mapping  √
such as f (x, y) = (y, 2.x) will give us invariants with coefficients involving 2.
Dealing with irrational and/or complex values raises some issues in our current
implementation setting. Therefore, we propose in section 4.3 a solution to stick
with rational numbers. Eventually, we treat the case when a condition occur in
loops in section 4.4.


4      Automated generation of loop invariants
4.1        Strength reduction of polynomial loops
Lowerization. Let P be a program containing a single loop with a single solv-
able assignment X := g(X). In order to reduce the invariant generation problem
for solvable polynomial loops to the one for affine loops, we need to find a linear
mapping f that perfectly matches g. As shown in figure 2, the first loop L1 is



    L1 :
    while ( ∗ ) do
     ( x , y , z ) := ( x + 1 , y + 2 , z + x ∗ y )
    done
    L2 :
    xy = x ∗ y
    while ( ∗ ) do
      ( x , y , xy , z ) := ( x + 1 , y + 2 , xy + 2 x + y + 2 , z + xy )
    done


            Fig. 2: Polynomial and affine loop having the same behavior


polynomial but there exists a similar affine loop, namely L2, computing the same
vector of values plus and thanks to an extra variable xy.

Definition 2 Let g be a polynomial mapping of degree d using m variables.
g is linearizable if there exists a linear mapping f such that X ′ = g(X) ⇒
(X ′ , P (X ′ )) = f (X, P (X)), where P : Qm → Qn is a polynomial of degree d.

    By considering polynomials as entries of the application, we are able to con-
sider the evolution of the polynomial value instead of recomputing it for every
loop step. This is the case in the previous example, where the computation of
xy as x ∗ y is made once at the beginning of the loop. Afterwards, its evolution
depends linearly of itself, x and y. Similarly, if we want to consider y n for some
n ≥ 2, we would just need to express the evolution of y n by a linear combination
of itself and lower degree monomials, which could themselves be expressed as lin-
ear combinations of lower degree monomials, until we reach an affine application.
We call this process the polynomial mappings lowerization or linearization.

Remark. This example and our running example have the good property to
be linearizable. However, this property is not true for all polynomials loops.
Consider for example the mapping f (x) = x2 . Trying to express x2 as a linear
variable will force us to consider the monomials x4 , x8 and so on. Thus, we need
to restrain our study to mappings that do not polynomially transform a variable
itself. This class of polynomials corresponds to solvable polynomial mappings,
defined in Definition 1.

Property 1 For every solvable polynomial mapping g, g is linearizable.

    For example, let g(x, y) = (x + y 2 , y + 1). g is linearized by f (x, y, y2 ) =
(x + y2 , y + 1, y2 + 2y + 1). Indeed with (x′ , y ′ ) = g(x, y), we have (x′ , y ′ , y ′2 ) =
f (x, y, y 2 )

Linearization Algorithm. The algorithm is divided in two parts : the solv-
ability verification of the mapping and, if successful, the linearization process.
The solvability verification consists in finding an appropriate partitioning of the
variables that respects the solvable constraint. It is nothing more than check-
ing that a variable v cannot be in a polynomial (i.e. non linear) assignment of
another variable that itself depend on v. This check can be reduced to verify-
ing the acyclicity of a graph, which can be computed e.g. by Tarjan’s [22] or
Johnson’s [12] algorithms.
    The linearization process then consists in considering all monomials as new
variables, then finding their linear evolution by replacing each of their variables
by the transformation made by the initial application. This may create new
monomials, for which we similarly create new variables until all necessary mono-
mials have been mapped to a variable. Since we tested the solvability of the loop,
the variable creation process will eventually stop. Indeed, if this was not the case,
this would mean that a variable x transitively depends on xd with d > 1.

Elevation. We saw how to transform a polynomial application into a linear
mapping by adding extra variables representing the successive products and
powers of every variable. This information can be useful in order to generate
invariants but in fact, most of the time, this is not enough. In our running
example of section 2, g(x, y) = (x + y 2 , y + 1), the degree of the mapping is 2 but
there exists no invariant of degree 2 for this loop. In order to deal with higher-
degree invariants, we need not just to linearize g, we also have to add more
variables to our study. As we can represent monomials of variables of a solvable
mapping as linear applications, we can extend the method to generate higher
degree monomials such as y 3 for example : we elevate g to a higher degree. The
process of elevation is described in [19] as a way to express polynomial relations
on a linear program.
Property 2 Every solvable polynomial mapping g using n variables is lineariz-
able by a linear mapping f using at most n+d    d   new variables, where d is the
degree of P , the polynomial linearizing g as in definition 2.

Note. The complexity of the transformation is polynomial for d or n fixed.
The lowerization algorithm can be used as shown above by adding variables
computing the high degree monomials we want to linearize. Moreover, n+d
                                                                               
                                                                             d   is an
upper bound and in practice, we usually need much less variables. For instance,
in our running example, we don’t need to consider x.y 2 . Indeed, if we tried to
linearize this monomial, we would end up with x.y 2 = x.y 2 +x.y+x+y 4 +2y 3 +y 2 ,
a polynomial of degree 4. Detecting that a monomial m is relevant or not can be
done by computing the degree of its transformation. For example, the assignment
of x is a degree 2 polynomial, so x2 associated transformation will be of degree 4.
Here, there is actually only two interesting monomials of degree 3, which are xy
and y 3 . Though those variables will be useless for the linearized mapping, they
are still easily computable: y3′ = y3 +3.y2 +3.y +1 and xy = xy +x+y2 +y3 . This
limits the necessary variables to only 6 (x, y, y2 , y3 , xy, 1) instead of 52 = 10.
This upper bound in only reached for affine transformations when searching for
polynomial invariants, as all possible monomials need to be treated.

4.2    Invariant generation
The transformation described previously doesn’t linearize a whole program, but
only a loop. Polynomial assignments must be performed before the loop starts
to initialize the new monomials. The method we present only focuses on the loop
behavior itself, allowing any kind of operation outside of the loop.

Eigenspace. Loop invariants are logical formulas satisfied at every step of a
loop. We can characterize them with two criteria : they have to hold at the
beginning of the loop (initialization criterion) and if they hold at one step, then
they hold at the next step (heredity criterion). Our technique is based on the
discovery of linear combinations of variables that are equal to 0 and satisfying
the heredity criterion. For example, the loop of section 3 admits the formula
−6.x + y − 3.y2 + 2y3 = k as a good invariant candidate. Indeed, if we set
k in accordance with the values of the variables at the beginning of the loop,
then this formula will be true for any step of the loop. We call such formulas
semi-invariants.

Definition 3 Let ϕ : Kn 7→ K and f : Kn 7→ Kn two linear mappings. ϕ is a
semi-invariant for f iff ∀X, ϕ(X) = 0 ⇒ ϕ(f (X)) = 0.

Definition 4 Let ϕ : Kn 7→ K, f : Kn 7→ Kn and X ∈ Kn . ϕ is an invariant
for f with initial state X iff ϕ(X) = 0 and ϕ is a semi-invariant for f .

   The key point of our technique relies on the fact that if there exists λ, f ∗ (ϕ) =
λϕ, then we know that ϕ is a semi-invariant. Indeed, we can rewrite definition 3
by hϕ, xi = 0 ⇒ hϕ, f (x)i = 0. By linear algebra, we have hϕ, f (x)i = hf ∗ (ϕ), xi,
with f ∗ the dual of f . If ∃λ, f ∗ (ϕ) = λϕ, then we can deduce that hϕ, xi = 0 ⇒
λ hϕ, xi = 0. This formula is always true, thus we know that ϕ is a semi-invariant.
Such ϕ are commonly called eigenvectors of f ∗ . We will not adress the problem
of computing the eigenvectors of an application as this problem have been widely
studied (in [20] for example).
    Recall our running example g(x, y) = (x + y 2 , y + 1), linearized by the appli-
cation f (x, y, y2 , xy, y3 , 1) = (x + y2 , y + 1, y2 + 2y + 1, xy + x + y2 + y3 , y3 + 3y2 +
3y + 1, 1). f ∗ admits e1 = (−6, 1, −3, 0, 2, 0)t and e2 = (0, 0, 0, 0, 0, 1)t as eigen-
vectors associated to the eigenvalue λ = 1. It means that if hk1 .e1 + k2 e2 , xi = 0,
then

                    hk1 .e1 + k2 e2 , f (X)i = hf ∗ (k1 .e1 + k2 e2 ), Xi
                                             = hλ(k1 .e1 + k2 e2 ), Xi
                                             =0

In other words, hk1 .e1 + k2 e2 , Xi = 0 is a semi-invariant. Then, by expanding
it, we can find that −6.x + y − 3.y2 + 2y3 = k, with k = − kk12 is a semi-invariant.
In terms of the original variables, we have thus −6.x + y − 3.y 2 + 2y 3 = k.
    Being an eigenvector of f ∗ does not just guarantee a formula to be a semi-
invariant of a loop transformed by f . This is also a necessary condition.

Theorem 1 ϕ : Kn 7→ K is a semi-invariant if and only if ∃λ ∈ K, ∃ϕ ∈ Eλ ,
where Eλ = ker(f ∗ − λId).

    It is now clear that the set of invariants is exactly the union of all eigenspaces
of f ∗ , i.e. a vector space union (which is not a vectorial space itself). An element
ϕ of Eλ of basis {e1 , ...en } is a linear combination of e1 , ..., en :
                                             n
                                             X
                                       ϕ=           ki ei
                                             k =1

The parameters ki can be chosen with respect to the initial state of the loop.

Expression of eigenvectors as invariants. More than a syntactic sugar, the
variable 1 brings interesting properties over the kind of invariants we generate
for an application f . The vector e1 such that he1 , Xi = 1 is always an eigenvector
associated to the eigenvalue 1. Indeed, by definition f (1) = 1, hence f ∗ (e1 ) = e1 .
For example, let’s take the mapping f (x, y, xy, 1) = (2x, 12 y + 1, xy + 2x, 1). This
mapping admits 3 eigenvalues : 2, 21 and 1. There exists two eigenvectors for the
eigenvalue 1 : (−2, 0, 1, 0) and (0, 0, 0, 1) = e1 . We have then the semi-invariant
k1 .(−2x+xy)+k2 = 0, or −2x+xy = −k         k1 . This implies that the two parameters
                                              2


k1 and k2 can be reduced to only one paramter k = −k        k1 , which simplifies a lot
                                                              2


the equation by providing a way to compute the parameter at the initial state if
we know it. For our example, −k   k1 would be −2xinit + xinit .yinit , where xinit and
                                    2


yinit are the initial values of x and y. More generally, each eigenvector associated
to 1 gives us an invariant ϕ that can be rewritten as ϕ(X) = k, where k is inferred
from the initial value of the loop variables.
     We can generalize this observation to eigenvectors associated to any eigen-
value. To illustrate this category, let us take as example f (x, y, z) = (2x, 2y, 2z).
Eigenvectors associated to 2 are e1 = (1, 0, 0), e2 = (0, 1, 0) and e3 = (0, 0, 1),
thus k1 x + k2 y + k3 z = 0 is a semi invariant, for any k1 , k2 and k3 satisfying
the formula for the initial condition of the loop. However, if we try to set e.g.
k1 = k2 = 1, using x + y + kz = 0 as semi invariant, we won’t be able to find a
proper invariant when yinit or xinit 6= 0 and zinit = 0. Thus, in order to keep the
genericity of our formulas, we cannot afford to simplify the invariant as easily
as we can do for invariants associated to the eigenvalue 1. Namely for every ei ,
we have to test whether hei , Xinit i = 0. For each ei for which this is the case,
hei , Xi = 0 is itself an invariant if hei , Xinit i = 0. However, if there exists an
i such that hei , Xinit i 6= 0, then we can simplify the problem. For example, we
                                                                                 +k2 yinit
assume that zinit 6= 0. Then k1 xinit +k2 yinit +k3 zinit = 0 ⇔ k1 xinitzinit              = −k3 .
                                           k1 xinit +k2 yinit
We know then that k1 x + k2 y =                  zinit        z is a semi-invariant. By writing
                       +k2 yinit
g(k1 , k2 ) = k1 xinitzinit      , we have
     
       x = g(1, 0)z
       y = g(0, 1)z
     As g is a linear application, these two invariants implies that ∀k1 , k2 , k1 x +
k2 y = g(k1 , k2 )z is a semi-invariant.
                                                                    n
                                                                    P
Property 3 Let F a semi-invariant expressed as F =                        ki ei .
                                                                    i=0
    If he0 , Xinit i 6= 0, then we have that
       n
       ^                   hei , Xinit i
           (hei , Xi = −                 he0 , Xi) is an invariant ⇔ hF , Xinit i = 0
       i=1
                           he0 , Xinit i

   We are now able to use pairs of eigenvectors to express invariants by knowing
the initial condition.

Algorithm. As we are restricting our study to solvable loops, that we know
can be replaced without loss of generality by linear loops, we assume the input
of this algorithm is a family of linear mappings. We can easily compose them via
their matrix representation. We end up with a new matrix A. Computing the dual
of A is computing the matrix AT . Then, eigenvectors of AT can be computed by
many algorithms in the linear algebra literature [20]. As the eigenvalue problem is
known to be polynomial, our invariant generation algorithm is also polynomial.

4.3     Extension of the method
 Let A ∈ Mn (Q). In the general case, A admits irrational and complex eigenval-
ues and eigenvectors, which end up generating irrational or complex invariants.
We cannot accept such representation for a further analysis of the input pro-
gram because of the future use of these invariants, by SMT solvers for example
which hardly deal with non-rational numbers. For example, let us take the   √ func-
tion f (x,
         √ y) =   (y, 2x). This mapping   admits  two   eigenvalues : λx =    2 and
λy = −√ 2. In this example, the  √  previous  method    would output  the invariants
k.(x + 2y) = 0 and k ′ .(x − 2y) = 0. With x and y integers or rationals,
this would be possible iff k = k ′ = 0. However, by considering the variable xy
the invariant generation procedure outputs the invariant k.(xy) = 0, which is
possible if x or y equals 0. This raises the issue of finding a product of variables
that will give us a rational invariant. We aim to treat the problem at its source
: the algebraic character of the matrix eigenvalues. A value x is algebraic in Q
if there exists a polynomial P in Q[X] such that P (x) = 0. Assuming we have a
geometric relation between the complex eigenvalues λi (i.e. a product q of eigen-
values that is rational), we will build a monomial m as a product of variables xi
associated to λi such that the presence of this monomial induces the presence
of a rational eigenvalue, namely q. Moreover, a rational eigenvalue of a matrix
is always associated to a rational eigenvector. Indeed, the kernel of a rational
matrix is always a Q-vectorial space. If λ ∈ Q is an eigenvalue of A, then A−λ.Id
is a rational matrix and its kernel is not empty.

Definition 5 Let A ∈ Mn (Q) . We denote Ψd (A) the elevation matrix such that
∀X = (x1 , ..., xn ) ∈ Qn , Ψd (A).p(X) = p(A.X), with p ∈ (Q[X]k ) a polynomial
associating X to all possible monomials of degree d or lower.
                                       
                                     ab
For example, if we have A =               as a transformation for X = (x, y), and
                                     cd
x ≺ y, we have as transformation for the variables (x2 , xy, y 2 , x, y) the matrix
                                      2
                                            2ab b2 0 0
                                                         
                                        a
                                      ac ad + bc bd 0 0 
                                      2
                                            2cd d2 0 0 
                                                         
                                     c
                            Ψ2 (A) =                    
                                     0      0     0 a b
                                        0    0     0 cd

Property 4 Let A ∈ Md (Q), Λ(M ) the eigenvalue set of a matrix M and d an
integer. Then for any product p of d or less elements of Λ(A), p ∈ Λ(Ψd (A)).

We can generalize this property for more variables. After working with two
variables, we get a new matrix with new variables that we can combine similarly,
and so on. Thanks to this property, if we have a multiplicative relation between
eigenvalues we are able to create home-made variables in the elevated application
whose presence implies the presence of rational eigenvalues.
    Though we could brute-force the search of rational products of irrational
eigenvalues in order to find all possibilities of variable products that have rational
eigenvalues, we could search for algebraic relations, i.e. multiplicative relations
between algebraic values. This subject is treated in [13] and we will not focus
on it. However, we can guarantee that there exists at least one monomial having
a rational eigenvalue. Indeed, it is known that the product of all eigenvalues of
a rational matrix is equal to its determinant. As the determinant of a rational
matrix is always rational, we know that the product of all variables infers the
presence of the determinant of the matrix as eigenvalue of the elevated matrix.
Coming back to the previous example, we have the algebraic relation λx .λy = −2.
If we consider the evolution of xy, we have (xy ′ ) = 2xy. Note that the eigenvalue
associated
          to xy is  2 and not −2. Indeed, we know that A = P −1 JP , with
            1 −1
    P = √          √
              2− 2
    and J an upper-triangular matrix, which means the    √ eigenvalues
                                                                    √    of A are on
the diagonal of J. xy in the base of J would be (x + 2y)(x − 2y) = x2 − 2y 2 ,
and we have well λ2x − 2λ2y = −2.
    Finally, by knowing that λ2x = 2, λ2y = 2 and λx λy = −2, we will consider the
variables x2 , y 2 and xy in our analysis of f . We can deduce new semi-invariants
from these variables : k1 (xy) + k2 (2x2 + y 2 ) = 0 with the eigenvectors associated
to 2 and k.(y 2 − 2x2 ) = 0 with the eigenvector associated to −2.

4.4    Multiple loops
 In this short section, we present our method to treat non-deterministic loops,
i.e. loops with non-deterministic conditions. At the beginning of each iteration,
the loop can choose randomly between all its bodies. This representation is
equivalent to the definition in section 2.

Definition 6 Let F = {Ai }16i6n a family of matrices and Inv(F ) the set of
invariants of a loop whose different bodies can be encoded by elements of F .
                                  Vn
   Inv(F ) = {ϕ|∀X, ϕ.X = 0 ⇒         ϕ.Ai .X = 0}
                                   i=1

Property 5 Let F = {Ai }16i6n a family of matrices.
                                          n
                                          \
                              Inv(F ) =         Inv(Ai )
                                          i=1

    As the set of invariants of a single-body loop are a vectorial spaces union, its
intersection with another set of invariants is also a vector space union. Although
we do not consider the condition used by the program to choose the correct body,
we still can discover useful invariants. Let us consider the following example,
taken from [21], that computes the product of x and y in variable z :
 while ( ∗ ) do
    ( x , y , z ) := ( 2 x , ( y −1)/2 , x + z )
    OR
    ( x , y , z ) := ( 2 x , y / 2 , z )
 done
   We have to deal with two applications : f1 (x, y, z) = (2x, (y − 1)/2, x + z)
and f2 (x, y, z) = (2x, y/2, z). The elevation to the degree 2 of f1 and f2 returns
applications having both 10 eigenvectors. For simplicity, we focus on invariants
associated to the eigenvalue 1.
   f1∗ has 4 eigenvectors {ei }i∈[1,4] as-    f2∗ also has 4 eigenvectors {e′i }i∈[1,4]
sociated to 1 such that                    associated to 1 such that

 – he1 , Xi = −x + xy                          – he′1 , Xi = xy
 – he2 , Xi = x + z                            – he′2 , Xi = z
 – he3 , Xi = xz + x2 + z 2                    – he′3 , Xi = z 2
 – he4 , Xi = 1                                – he′4 , Xi = 1

    First, we notice that e4 = e′4 . Then, we can see that he1 + e2 , Xi = xy + z =
he1 + e′2 , Xi. Thus, e1 + e2 = e′1 + e′2 . Eventually, we find that e1 + e2 + k.e4 ∈
  ′

(V ect({ei }i∈[1,4] ) ∩ V ect({e′i }i∈[1,4] )). That’s why (he1 + e2 + k.e4 , Xi = 0) is a
semi-invariant for both f1 and f2 , hence for the whole loop. Replacing hk.e4 , Xi
by k = −k ′ and he1 + e2 , Xi by xy + z gives us xy + z = k ′ .


Algorithm. The intersection of two vector spaces corresponds to the vectors
that both vector spaces have in common. It means that such elements can be
expressed by elements of the base of each vector space. Let B1 and B2 the bases of
the two vector spaces. If e ∈ Vect{B1 } and e ∈ Vect{B2 }, then e ∈ ker{(B1 B2 )}.
To compute the intersection of a vector space union, we just have to compute
the kernels of each combination of vector space in the union.


5     Implementation and experimentation
In order to test our method, we implemented an invariant generator as a plu-
gin of Frama-C [14], a framework for the verification of C programs written in
OCaml. Tests have been made on a Dell Precision M4800 with 16GB RAM and
8 cores. Time does not include parsing time of the code, but only the invariant
computation from the Frama-C representation of the program to the formulas.
Moreover, our tool doesn’t implement the extension of our method and may out-
put irrational invariants or fail on complex eigenvalues. Benchmark is available
at [6]. The second column of the table 1 represents the number of variables used
in the program. The third column represents the invariant degree used for Pilat
and Fastind. The last three columns are the computation time of the tools in
ms. O.O.T. represents an aborted ten minutes computation and – indicates that
no invariant is found.
    All the tested functions are examples for which the presence of a polynomial
invariant is compulsory for their verification. The choice of high degree for some
functions is motivated by our will to show the efficiency of our tool to find high
degree invariants as choosing a higher degree induces computing a bigger set of
relations. In the other cases, degree is choosen for its usefulness.
    For example in figure 3 we were interested in finding the invariant x + qy = k
for eucli_div. That’s why we set the degree to 2. Let X be the vector of variables
(x, y, q, xq, xy, qy, y2 , x2 , q2 , 1). The matrix A representing the loop in figure 3
has only one eigenvalue : 1. There exist 4 eigenvectors {ei }i∈[1;4] associated to 1
       Table 1: Performance results with our implementation Pilat

                     Program                          Time (in ms)

         Name          Var     Degree Aligator [15] Fastind [5] Pilat

          divbin        5       2                80             6     2.5
            hard        6       2                89            13       2
       mannadiv         5       2                27             6       2
            sqrt        4       2                33             5     1.5
         djikstra       5       2               279            31       4
        euclidex2       8       2             1759             10       6
           lcm2         6       2               175             6       3
         prodbin        5       2               100             6     2.5
           prod4        6       2            13900              –       8
         fermat2        5       2                30             9       2
          knuth         9       3        O.O.T.               347     192
       eucli_div        3       2                13             6       2
         cohencu        5       2                90             5       2
       read_writ        6       2                82             –      12
          illinois      4       2        O.O.T.                 –       8
            mesi        4       2               620             –       4
           moesi        5       2        O.O.T.                 –       8
        petter_4        2       10           19000             37       3
        petter_5        2       10       O.O.T.                37       2
        petter_6        2       10       O.O.T.                37       2




       Input : degree = 2                       Frama-C output :


 int eucl i _di v ( int x , int y ){       int eucl i _di v ( int x , int y ){
   int q = 0 ;                               int q = 0 ;
   while ( x > y ) {                         int k = x + y∗q ;
     x = x−y ;                               // i n v a r i a n t x + y ∗ q = k ;
     q ++;                                   while ( x > y ) {
   }                                           x = x−y ;
   return q ;                                  q ++;
 }                                           }
                                             return q ;
                                           }


Fig. 3: Euclidean division C loop and generation of its associated invariants.
            4                
            P
in A, so          ki ei , X       = 0 is a semi-invariant. One of these eigenvectors, let’s
            i=1
say e1 , correspond to the constant variable, i.e. e1 .X = 1 = 1, thus we have
   4
             
  P
     ki ei , X = −k1 as invariant. In our case, he2 , Xi = y, he3 , Xi = x + yq and
 i=2
he4 , Xi = y2 . We can remove (y = k) and (y2 = k) that are evident because y
does not change inside the loop. The remaining invariant is x + yq = k.


6      Conclusion and future work
We presented a simple and effective method to generate non-trivial invariants.
One of its great advantages is to only rely on linear algebra theory, and generate
modular invariants. Still our method has some issues that we are currently in-
vestigating. First, it is incomplete for integers : invariants we generate are only
correct for rationals. Perhaps surprisingly, this issue does not come from the in-
variant generation, but from the linearization procedure which badly takes into
account the division. For example in C, the operation x′ = x2 with x uneven
returns x−1
          2 . This behavior is not taken into account by the elevation, which can
freely multiply this x by a variable y with y ′ = 2y. This returns the assignment
xy ′ = xy which is false if x is odd. Next, we do not treat interleaving loops as
we cannot yet compose invariants with our generation technique. The tool has
been successfully implemented as an independent tool of Frama-C.
    Our next step is to use those invariants with the Frama-C tools Value (a
static value analyser) and WP (a weakest precondition calculus API) to ap-
ply a CEGAR-loop on counter-examples generated by CaFE, a temporal logic
model checker based on [1]. Also, we want the next version of the tool to handle
irrational eigenvalues as decribed in section 4.3.


References
 1. R. Alur, K. Etessami, and P. Madhusudan. A temporal logic of nested calls and
    returns. In TACAS 2004, pages 467–481, 2004.
 2. S. K. Basu and J. Misra. Proving loop programs. IEEE Trans. Software Eng.,
    1(1):76–86, 1975.
 3. D. Beyer, T. A. Henzinger, R. Majumdar, and A. Rybalchenko. Path invariants.
    In ACM SIGPLAN 2007 Conference on Programming Language Design and Im-
    plementation, pages 300–309, 2007.
 4. B. Botella, M. Delahaye, S. H. T. Ha, N. Kosmatov, P. Mouy, M. Roger, and
    N. Williams. Automating structural testing of C programs: Experience with
    PathCrawler. In 4th International Workshop on Automation of Software Test,
    AST 2009, pages 70–78, 2009.
 5. D. Cachera, T. P. Jensen, A. Jobin, and F. Kirchner. Inference of polynomial
    invariants for imperative programs: A farewell to Gröbner bases. Sci. Comput.
    Program., 93:89–109, 2014.
 6. E.       Carbonell.                 Polynomial       invariant     generation.
    http://www.cs.upc.edu/~erodri/webpage/polynomial_invariants/list.html.
 7. E. M. Clarke, O. Grumberg, S. Jha, Y. Lu, and H. Veith. Counterexample-guided
    abstraction refinement. In CAV 2000, pages 154–169, 2000.
 8. K. D. Cooper, L. T. Simpson, and C. A. Vick. Operator strength reduction. ACM
    Trans. Program. Lang. Syst., 23(5):603–625, 2001.
 9. C. A. R. Hoare. An axiomatic basis for computer programming. Commun. ACM,
    12(10):576–580, 1969.
10. C. A. R. Hoare. The verifying compiler: A grand challenge for computing research.
    J. ACM, 50(1):63–69, 2003.
11. H. Hojjat, R. Iosif, F. Konecný, V. Kuncak, and P. Rümmer. Accelerating inter-
    polants. In ATVA 2012, pages 187–202, 2012.
12. D. B. Johnson. Finding all the elementary circuits of a directed graph. SIAM
    Journal on Computing, 4(1), 1975.
13. M. Kauers and B. Zimmermann. Computing the algebraic relations of C-finite
    sequences and multisequences. J. Symb. Comput., 43(11):787–803, 2008.
14. F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski. Frama-C:
    A software analysis perspective. Formal Aspects of Computing, 27(3), 2015.
15. L. Kovács. Aligator: A mathematica package for invariant generation (system
    description). In Automated Reasoning, 4th International Joint Conference, IJCAR
    2008, pages 275–282, 2008.
16. L. Kovács. A complete invariant generation approach for P-solvable loops. In
    Perspectives of Systems Informatics, 7th International Andrei Ershov Memorial
    Conference, PSI 2009, pages 242–256, 2009.
17. E. Mayr. Membership in polynomial ideals over Q is exponential space complete.
    Springer, 1989.
18. M. Müller-Olm and H. Seidl. Polynomial constants are decidable. In Static Anal-
    ysis, 9th International Symposium, SAS 2002, pages 4–19, 2002.
19. M. Müller-Olm and H. Seidl. Precise interprocedural analysis through linear alge-
    bra. In POPL 2004, pages 330–341, 2004.
20. V. Y. Pan and Z. Q. Chen. The complexity of the matrix eigenproblem. In
    Proceedings of the Thirty-First Annual ACM Symposium on Theory of Computing,
    May 1-4, 1999, Atlanta, Georgia, USA, pages 507–516, 1999.
21. E. Rodríguez-Carbonell and D. Kapur. Generating all polynomial invariants in
    simple loops. J. Symb. Comput., 42(4):443–476, 2007.
22. R. E. Tarjan. Depth-first search and linear graph algorithms. SIAM journal on
    computing, 1(2), 1972.
7    Appendix
Linearization theorem. The following justifies the linearization theorem of
section 4.1
Property 1 For every solvable polynomial mapping g, g is linearizable.
Proof. Let g ∈ Q[x]m be a solvable polynomial mapping. There exists a partition
of variables x = w1 ∪ ... ∪ wk such that

                          gwj (x) = Mj wjT + Pj (w1 , ..., wj−1 )
  We proceed by induction on the size k of the partition on the variables of g.
We can state that :
 • If k = 1, x = w1 , then gw1 (x) = M1 w1T + P1 , where P1 is a constant. Then
   it is clear that gw1 is an affine transformation.
 • Assume we can compute a linear application f from g such that (g(x), P (g(x))) =
   f (x, P (x)) if there exists a partition of k sets of variable satisfying the solv-
   able hypothesis. Let h be a solvable polynomial mapping for which there
   exists a partition of x into k + 1 subvectors of variables x = w1 ⊎ ... ⊎
   wk+1 , wi ∩ wj = ∅ if i 6= j. By induction hypothesis, we can linearize hwi for
   1 6 i 6 k. Now, the key point is to find a way to linearize
                                          T
                        hwk+1 (x) = Mk+1 wk+1 + Pk+1 (w1 , ..., wk )
    First, let’s note that no variable of wk+1 have been used in any other hi . Let
          n
             viλi a product of variables in (w1 ∪ ... ∪ wk ). It can appear in P as v d ,
         Q
    v=
         i=0
    where d in an integer. We know, by induction hypothesis, that the evolution
    of vi following the h transformation can be expressed as a linear application
    f with the help of extra variables.
    Lemma 1 Let g : Kn 7→ Kn a linear application. There exists a linear
    application f : Km 7→ Km with m > n such that for all k ∈ N and P ∈
    (K[X])m−n , X ′ = g k (X) ⇒ (X ′ , P (X ′ )) = f k (X, P (X))
    Proof. First, let’s prove it for n = 2 and P (x, y) = (x.y, x2 , y 2 ). Let g(x, y) =
    (ax + bx y, ay x + by y). Then, (x.y)′ = ax .ay x2 + (ax .by + ay .bx )x.y + bx .by .y 2 ,
    which is a linear combination of x2 , y 2 and xy. Similarly, (x2 )′ and (y 2 )′ can
    be expressed as linear combinations of x2 , y 2 and x.y.
    Next, if the degree of the polynomial is 1, one just need to take f = g.
    To generalize this proof for all degrees polynomials, let’s assume that for
    d ∈ N , the lemma is true with P of degree d. To express a polynomial of
    degree d + 1, one need to express all monomials md+1 of degree d + 1, which
    is the product of a variable x and a monomial md of degree d. By hypothesis,
    the monomial of degree d is expressible in g as a linear combination of lower
    or equal degree monomials. Considering md as a variable of g, the variable
    for which we seek a linear representation is the product of the two variables
    x and md , a case which has been treated before. 
    We can then use Lemma 1 to linearize all monomials of elements of w1 , ..., wk
    occuring in P . In the end, we can write h as a linear application over the
    initial variables and the auxiliary variables introduced by the linearization.
    

Complexity. The following justifies the complexity theorem of elevation in
section 4.1
Property 2 Every solvable polynomial mapping g using n variables is lineariz-
able by a linear mapping f using at most n+d    d     new variables, where d is the
degree of P , the polynomial linearizing g as in definition 2.

Proof. This property comes from [19]. n+d
                                               
                                            d     is the total number of variables
needed to express all monomials products of n variables of degree lower or equal
to d.

Invariants set. The following justifies the completude of the invariant gener-
ation procedure in section 4.2
Theorem 1 ϕ : Kn 7→ K is a semi-invariant if and only if ∃λ ∈ K, ∃ϕ ∈ Eλ ,
where Eλ = ker(f ∗ − λId).

Proof. This comes from a well known linear algebra result :
Lemma 2 Let K be a field, E be a K*vectorial space, F a sub-K vectorial space
of E and f : E → E a linear application.
f (F ) ⊂ F ⇔ f ∗ (F ⊥ ) ⊂ F ⊥

Proof. By linear algebra, we have < f (x), x′ >=< x, f ∗ (x′ ) >. Let x ∈ F, x′ ∈
F ⊥ . If f (F ) ⊂ F , then < f (x), x′ >= 0, so < x, f ∗ (x′ ) >= 0.
    As we have f ∗ (F ⊥ ) ⊂ F ⊥ , we conclude by seeing (F ⊥ )⊥ = F and (f ∗ )∗ = f .


     Let V ect(X) the vectorial space generated by X. Let ϕ a semi-invariant, so
(ϕ.x = 0 ⇒ ϕ(f (x)) = 0). This means that V ect(ϕ)⊥ is stable by f , so by
property 2, (V ect(ϕ)⊥ )⊥ = V ect(ϕ) is stable by f ∗ . As ϕ ∈ V ect(ϕ), we have
f ∗ (ϕ) = k ∗ ϕ.
     

Constant deplacement. The following justifies the operation of preserving
the equivalency of two invariants by moving constants in section 4.2.
                                                                n
                                                                P
Property 3 Let F a semi-invariant expressed as F =                   ki ei .
                                                               i=0
   If he0 , Xinit i 6= 0, then we have that
      n
      ^                   hei , Xinit i
          (hei , Xi = −                 he0 , Xi) is an invariant ⇔ hF , Xinit i = 0
      i=1
                          he0 , Xinit i
Proof.                      n                      
                            P
    hF , Xinit i = 0 ⇔              ki ei , Xinit       = −k0 he0 , Xinit i
                            i=1
                           n
                           P
                       ⇔         ki hei , Xinit i = −k0 he0 , Xinit i
                           i=1
                            P
                            n
                                 ki hei ,Xinit i
                       ⇔ i=1he0 ,Xinit i           = −k0
                                P
                                n
                                    ci .hei ,Xinit i
                                                                            hei ,Xinit i
    Let g(c1 , ..., cn ) = − i=1he0 ,Xinit i           . We have g(ui ) = − he0 ,Xinit i
                                                                                         We note that
g is linear, thus :
                                                                 n
                                                                 P
    hF , Xinit i = 0 ⇔ g(k1 , ..., kn ) he0 , Xinit i =                ki hei , Xinit i
                                                                 i=1
                            n
                            V                  hei ,Xinit i
                       ⇒         (hei , Xi = − he0 ,Xinit i
                                                            he0 , Xi)
                           i=1
    by setting ki = 1 and kj = 0 for all j 6= i.
    Now to prove that this transformation does not make us lose precision, we
will construct F with the n equations.
       n
       V
    If   (hei , Xi = g(ui ) he0 , Xi), then as g is a linear application we have that
       i=1

                            n
                            X
                                    ki hei , Xi = g(k1 , ..., kn ) he0 , Xi
                            i=1

    We conclude by setting k0 to −g(k1 , ..., kn )
    

Extension of the method. The following justifies the theorema of construc-
tion of rational eigenvalue in section 4.3.

Property 4 Let A ∈ Md (Q), Λ(M ) the eigenvalue set of a matrix M and d an
integer. Then for any product p of d or less elements of Λ(A), p ∈ Λ(Ψd (A)).

Proof. First of all, we will prove some simple properties about Ψd .

Lemma 3

 1. Ψk (A.B) = Ψk (A).Ψk (B)
 2. Ψk (A−1 ) = Ψk (A)−1

Proof. 1. Ψk (A).Ψk (B)p(X) = Ψk (A).p(B.X) = p(A.B.X) = Ψk (A.B)p(X)
 2. Ψk (A−1 ).Ψk (A).p(X) = p(A.A−1 X) = p(X) so Ψk (A−1 ).Ψk (A) = Id.
    

   To deal with this, let’s consider J the Jordan normal form of A. As we are
working with C, which is an algebraically closed field, A is similar to J (ie.
∃P.A = P −1 JP ), with
                                                         
            J1 0 ... 0                     λk 1 ... 0
          . . . . ..                                    . 
                                          0 . . . . . . .. 
                                         
         0 . . . 
    J = .                   , and Jk =  . . .
                                                         
          .. . . . . . . 0              .. . . . . 1 
                                                            

             0 ... 0 Jk                    0 ... 0 λk
    As A = P −1 JP, Ψk (A) = Ψk (P )−1 .Ψk (J)Ψk (P ), so Ψk (A) is similar to Ψk (J).
This means that they have the same set of eigenvalues. The transformation of a
variable x by J can be either of the form λ.x, either λ.x+ y, with λ an eigenvalue
of J and y another variable. Another interesting information from the jordan
normal form is that this variable y does not depend on x. To understand the
proof, let’s see what happens for d = 2 and n = 2.              
                ′                                           λ b
    If λ and λ are eigenvalues of A, then J =                      with b = 0 or 1 . So
                                                            0 λ′
           2          ′ ′2
                                 
             λ 2λλ λ 0 0
           0 λλ′ bλ′ 0 0 
                          ′2
                                
Ψ2 (J) =  0 0 λ 0 0 .
                                 
           0 0 0 λ b
              0 0 0 0 λ′
    Ψ2 (J) is upper triangular, so its eigenvalues are on the diagonal : λ, λ′ , λ2 , λλ′
and λ′2
    The proof for any number of variables and any degree is similar. We just
need to analyse the elevation of the Jordan normal form of A.
Definition 7 Let f a linear application. We define a dependency order ≺f on
V ar a total order such that for all x ∈ V ar, f (X) restricted to x depends only
on a linear combination of variables V for which ∀y ∈ V, y f x. We also say
that f respects ≺f .
The idea behind this is that an upper-triangular matrix J induces such an order
: the last element xn only depend on himself, the previous element xn−1 depends
on himself and xn , so xn ≺A xn−1 , etc.. We note that for any triangular matrix,
the diagonal coefficients are the eigenvalues of the said matrix and of all similar
matrix.
    In other words, if for the ith variable of an application, the line of its matrix
is composed of i − 1 zeros then λ at the ith position, then its eigenvalue is λ.
    We define ≺J as an order that J respects. By choosing a right order for
monomials of p, we will show that Ψk (J) is upper-triangular. We will take the
graded lexicographic order ≺gJ with respect to ≺J , i.e. the order such that :
 – if x ≺J y two variables, then x ≺gJ y ;
 – if m1 ≺gJ m2 , then for any monomial m3 , m1 .m3 ≺gJ m2 .m3 .
   If x ≺gJ y then by definition x ≺J y. Moreover, m1 ≺gJ m2 ⇔ (m1 does not
appear in the expression of m2 ), then let m3 any monomial. We can clearly see
that m1 .m3 does not appear in the expression of m2 .m3 . Thus :
Lemma 4 Let J an upper triangular matrix, ≺J be a dependency order respected
bu J. Then for any k ∈ N, ≺gJ can be a dependency order for Ψk (J).
    By our construction of the linearization process of 4.1, we can state that for
all x, y, z ∈ V ar, if x ≺J y J z, then y i z j ≺gJ xi+j is impossible for all i, j as x
does not depend on y or z, but the contrary is false. Thus :
Lemma 5 Let f a linear application, ≺f a dependency order on f , x, y ∈ V ar.
Let M ond (x, y) the set of variables representing monomials of degree lower or
equal to d depending on x and y. Then z ≺f x ≺f y ⇒ v ∈ M ond (x, y), z d gf v.
      In other words, in a triangular matrix M representing x, y, z and its mono-
mials, if x and y are over z and M respects ≺gM , then xi .y j will always be over
z k , for every i, j, k with k 6 i + j.
      Let x, y, z, t variables such that x′ = λx .x + jz z, and y ′ = λy .y + jt t where jz
and jt = 0 or 1. Then the matrix Ψk (J) will set xi .y j to (λx .x+jz z)i (λy .y +jt t)j .
      Eventually, when one develop xi .y j , there is :
 • 0 for monomial variables of strictly higher degree ;
 • 0 for monomial variables
                         ′   ′
                                containing t such that t ≺ x ≺ y by lemma 5 ;
 • 0 for monomials xi .y j with i′ + j ′ = d and i′ > i ;
 • a coefficient λix .λjy for the variable xi .y j , which will be on the diagonal of
   Ψk (J).
   The third point is true because if x ≺J y, then xi y j ≺gJ xi−1 y j+1 and ≺gJ is
a dependency order for Ψk (J) 4.
   Ψk (J) will be upper-triangular itself by respecting ≺gJ .
   

Multiple loop. The following justifies the multiple loop proposition of sec-
tion 4.3
Property 5 Let F = {Ai }16i6n a family of matrices.
                                             n
                                             \
                                 Inv(F ) =         Inv(Ai )
                                             i=1

Proof.
Lemma 6
   Let F = {Ai }16i6m , G = {Bi }16i6n two matrix families. Then Inv(F ∪G) =
Inv(F ) ∩ Inv(G)
Proof. As we have ((p ⇒ q) ∧ (p ⇒ r)) ⇔ (p ⇒ (q ∧ r)),

                                                         m
                                                         V
                                     (ϕ.X = 0 ⇒              ϕ.Ai .X = 0)
  Inv(F ) ∩ Inv(G) = {ϕ|∀X,                          i=1                    }
                                                      n
                                                      V
                                  ∧ (ϕ.X = 0 ⇒               ϕ.Bi .X = 0)
                                                     i=1
                                                   m
                                                   ^                     n
                                                                         ^
                       = {ϕ|∀X, ϕ.X = 0 ⇒ (              ϕ.Ai .X = 0 ∧          ϕ.Bi .X = 0)}
                                                   i=1                   i=1
                       = Inv(F ∩ G)
   

   By recurrence over the size n of a family F , if n equals 1 it is true. If it is
true for a certain n, then Inv(F ∪ {A}) = Inv(F ) ∩ Inv({A}) by the previous
lemma.
   
