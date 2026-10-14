          An Immune System Inspired Approach to
              Automated Program Verification
                                                              Soumya Banerjee



  Abstract — An immune system inspired Artificial Immune                   An AIS algorithm is proposed to carry out the machine-
System (AIS) algorithm is presented, and is used for the                   learning task of predicting invariant shape from an instance
purposes of automated program verification. Relevant
                                                                           of a program. No distinction is made between a B cell and its
immunological concepts are discussed and the field of AIS is
briefly reviewed. It is proposed to use this AIS algorithm for a           receptor, known as an antibody (Ab), so that every element
specific automated program verification task: that of predicting           of our artificial immune system will be generically called an
shape of program invariants. It is shown that the algorithm                Ab.
correctly predicts program invariant shape for a variety of
benchmarked programs.
                                                                                          II. CLONAL SELECTION THEORY
  Index Terms — Artificial Immune System, Evolutionary
Computing, Program Invariant, Automatic Program                               Any molecule that can be recognized by the adaptive
Verification, Shape of Invariant.                                          immune system is known as an antigen (Ag). When an
                                                                           animal is exposed to an Ag, some subpopulation of its bone-
                      I. INTRODUCTION                                      marrow-derived cells (B cells) responds by producing
      VER the last few years, there has been an ever-                      antibodies (Ab’s). Ab’s are molecules attached primarily to
O     increasing interest in the area of artificial immune
      systems (AIS) and their applications [1]–[6]. AIS uses
                                                                           the surface of B cells whose aim is to recognize and bind to
                                                                           Ag’s. Each B cell secretes a single type of Ab, which is
ideas gleaned from immunology in order to develop adaptive                 relatively specific for the Ag. By binding to these Ab’s and
systems capable of performing a wide range of tasks in                     with a second signal from accessory cells, such as the T-
various areas of research.                                                 helper cell, the Ag stimulates the B cell to proliferate
   In this paper, I review the clonal selection concept,                   (divide) and mature into terminal (nondividing) Ab secreting
together with the affinity maturation process, and state how               cells, called plasma cells. The process of cell division
these biological principles can lead to the development of                 (mitosis) generates a clone, i.e., a cell or set of cells that are
useful computational tools [7]. The algorithm proposed to be               the progenies of a single cell.
used focuses on a systemic view of the immune system and                      B cells, in addition to proliferating and differentiating into
does not take into account cell–cell interactions. I do not                plasma cells, can differentiate into long-lived B memory
model any biological phenomenon, but propose how some                      cells. Memory cells circulate through the blood, lymph, and
basic immune principles can help us to not only better                     tissues and, when exposed to a second antigenic stimulus,
understand the immune system itself, but also to solve a                   commence to differentiate into plasma cells capable of
problem in program verification: that of finding a program                 producing high-affinity Ab’s, preselected for the specific Ag
invariant.                                                                 that had stimulated the primary response. The main features
   An invariant of a program is a mathematical formula that                of the clonal selection theory [10], [11] that will be reviewed
captures the semantics of the program [8] and is used in                   in this paper are:
automatic program verification. The shape of an invariant is                  1) proliferation and differentiation on stimulation of cells
its approximate polynomial representation. Once the shape                     with Ag’s;
of the invariant is predicted, deterministic techniques can be                2) generation of new random genetic changes, expressed
used to generate the exact form of the invariant [9]. Hence,                  subsequently as diverse Ab patterns, by a form of
the prediction of invariant shape is of paramount importance                  accelerated somatic mutation (a process called affinity
for program verification.                                                     maturation);

                                                                             A.     Reinforcement Learning and Immune Memory
                                                                              Learning in the immune system involves raising the
  Manuscript received May 15th, 2009.
                                                                           relative population size and affinity of those lymphocytes
                                                                           that have proven themselves to be valuable by having
   S.B. Author is with the Department of Computer Science, University of   recognized a given Ag. In the use of the clonal selection
New Mexico, Albuquerque, NM - 87106, USA. (Phone - 505-277-3122,
Fax - 505-277-6927, E-mail: soumya@cs.unm.edu)                             theory for the solution of practical problems, I do not intend
                                                                           to maintain a large number of candidate solutions, but to
keep a small set of best individuals. A clone will be created       As a summary, immune learning and memory are
temporarily and those progeny with low affinity will be           acquired through [19]:
discarded. The purpose is to solve the problem using a              1) repeated exposure to an Ag;
minimal amount of resources. Hence, I seek high-quality and         2) affinity maturation of the receptor molecules;
parsimonious solutions.                                             3) low-grade chronic infection;
   In the normal course of the immune system evolution, an          4) cross-reactivity.
organism would be expected to encounter a given Ag
repeatedly during its lifetime. The initial exposure to an Ag
                                                                   B. Affinity Maturation
that stimulates an adaptive immune response is handled by a
small number of low-affinity B cells, each producing an Ab          In an immune response, the repertoire of Ag-activated B
type of different affinity. The effectiveness of the immune       cells is diversified basically by two mechanisms:
response to secondary encounters is enhanced considerably            1) hypermutation and 2) receptor editing [20]–[23].
by the presence of memory cells associated with the first            Ab’s present in a memory response have, on average, a
infection, capable of producing high-affinity Ab’s just after     higher affinity than those of the early primary response. This
subsequent encounters. Rather than “starting from scratch”        phenomenon is referred to as the maturation of the immune
every time, such a strategy ensures that both the speed and       response. This maturation requires the Ag-binding sites of
accuracy of the immune response becomes successively              the Ab molecules to be structurally different from those
higher after each infection.                                      present in the primary response.
   This is an intrinsic scheme of a reinforcement learning           Random changes are introduced into the genes responsible
strategy [12], where the interaction with the environment         for the Ag–Ab interactions and occasionally one such change
gives rise to the continuous improvement of the system            will lead to an increase in the affinity of the Ab. These
capability to perform a given task. To illustrate the adaptive    higher affinity variants are then selected to enter the pool of
immune learning mechanism, consider that an antigen Ag1 is        memory cells. Not only the repertoire is diversified through
introduced at time zero and it finds a few specific Ab’s          a hypermutation mechanism, but also mechanisms must exist
within the animal. After a lag phase, the Ab against antigen      such that rare B cells with high affinity mutant receptors can
Ag1 appears and its concentration rises up to a certain level     be selected to dominate the response. Those cells with low
and then starts to decline (primary response). Consider at        affinity or self-reactive receptors must be efficiently
this point the exposition to an antigen Ag2 not correlated        eliminated [20]–[22].
with antigen Ag1. Then, no specific Ab is present and the Ab         Somatic mutations guide to local optima, while receptor
response will be similar to that obtained in the case of Ag1      editing introduces diversity, leading to possibly better
[13]. On the other hand, one important characteristic of the      candidate receptors. In conclusion, point mutations are good
immune memory is that it is associative: B cells adapted to a     for exploring local regions, while editing may rescue
certain type of antigen present a faster and more efficient       immune responses stuck on unsatisfactory local optima.
secondary response not only to, but also to any structurally
related antigen. This phenomenon is called immunological
cross reaction or cross-reactive response [14]–[18]. This          III. AUTOMATED PROGRAM VERIFICATION AND PROGRAM
                                                                                           INVARIANTS
associative memory is contained in the process of
vaccination and is called generalization capability or simply        The field of automated program verification started with
generalization in other artificial (computational) intelligence   seminal work by Floyd [24] and Hoare [25]. They
fields, like neural networks [19].                                introduced the concept of a loop invariant: a mathematical
   Some characteristics of the associative memories are           formula that remains true throughout the execution of a loop.
particularly interesting in the context of AIS:                   The loop invariant completely captures the semantics of the
   1) the stored pattern is recovered through the presentation    loop, and along with the program preconditions and
   of an incomplete or corrupted version of the pattern;          postconditions, can be used to show correctness of the
   2) they are usually robust, not only to noise in the data,     program [25].
   but also to failure in the components of the memory.              Recent work [8] has shown how the loop invariant for a
By comparison with the primary response, the secondary            particular program can be generated by a priori agreement
response is characterized by a shorter lag phase, a higher        on the shape of the invariant: the approximate polynomial
rate, and longer synthesis of Ab’s with higher antigenic          representation of the invariant. However, the shape of the
affinities (see the affinity maturation section). Moreover, a     loop invariant can be hard to deduce for many programs.
dose of Ag substantially lower than that required to initiate a    The following shows an example program:
primary response may cause a secondary response.
   Under an engineering perspective, the cells with higher          {A  0, B  0}
affinity must somehow be preserved as high-quality                  x := A;
                                                                    y := B;
candidate solutions and shall only be replaced by improved
                                                                    z := 0;
candidates, based on statistical evidences. This is the reason
why the AIS has a specific memory set as part of the whole          while x > 0 do
repertoire.                                                           if odd(x) then z := z + y;
    y := 2 * y;                                                   (if <condition> then) e.g. x := x + 2, and while (x > 0) do,
    x := x/2;                                                     and if (x > 3) then, are all program fragments.
  end while
                                                                     The analogue of an antigen is a program fragment and the
                                                                  corresponding analogue of an antibody is an invariant for the
   Assuming the shape of the program invariant as                 program fragment it recognizes. Hence, the AIS will be
Ishape: Ax + By + Cz + Dxy + Eyz + Fxz + Gxyz + H = 0,
                                                                  presented with an antigen (program fragment), and the
(where A, B, C, D, E, F, G and H are constants or program
                                                                  immune system cells will either produce the antibody
variables), using quantifier elimination [8], I get the final     (invariant) immediately if it has encountered this antigen
loop invariant as Ifinal: z + xy - AB = 0. Coupled with a         before, or will undergo somatic hypermutations to generate
precondition P: {A  0 ^ B  0 ^ x = A ^ y = B ^ z = 0}
                                                                  the correct antibody (invariant).
and a postcondition Q: {z = A*B}, it can be shown that this          The individual invariants for each program fragment will
invariant is consistent with Q i.e. the program correctly         then be recombined to generate the invariant for the whole
multiplies 2 numbers A and B and stores the result in z.          program.
   Finding the precise shape of the loop invariant is generally
a non-trivial process and the AIS algorithm proposed aims to
use “cues” from the program to make informed predictions               VI. A SHAPE SPACE AND ANTIGENIC DISTANCE FOR
about the invariant shape and ultimately help in automated                                  PROGRAMS
program verification.
                                                                     We need a measure of distance between disparate
                       IV. PROPOSAL                               program fragments, so that the AIS can recognize them and
                                                                  generate an antibody in response. For a natural immune
   An AIS algorithm will be used to generate shapes of            system, the antibody combining region relevant to antigen
program invariant. Initially the AIS will be trained on           binding can be specified by a number of “shape” parameters
programs, for which the shape of invariant is known. Then a       [27]. Some of these parameters would be geometric
program will be presented to the AIS and it will try to           quantities specifying the size and shape of the combining
predict the form of the invariant.                                site, and others would specify physical characteristics of the
   An AIS approach presents many advantages over a                amino acids comprising the combining site such as charge,
traditional Machine Learning (ML) approach. In an AIS,            dipole moment, and the ability to form hydrogen bonds.
recognition can be sloppy [26] i.e. if it has previously             If there are N shape parameters, they can be combined
recognized program P (with an invariant I), then a new            into a vector, and antibody combining sites and antigenic
program P’ “similar” to P, can also be recognized, and an         determinants can be described as points Ab and Ag, in an N-
invariant I’ can be generated, that is similar in form to I.      dimensional Euclidean vector-space called shape space [27].
This is akin to our immune system recognizing a previously           Antigenic distance between 2 antigens is the distance in
encountered pathogen (program), and generating antibodies         shape space [14] between them e.g. ||Ag1 - Ag2|| is the
(invariant) similar to the previously produced antibodies.        distance between antigens Ag1 and Ag2 in shape space S.
   The natural immune system produces antibodies by a             The antibody distance is the distance ||Ab1 - Ab2|| in shape
process of mutation, and the same process is emulated in          space between 2 antibodies Ab1 and Ab2.
AIS algorithms. A candidate solution (invariant) will be             I define the program fragment shape space as the N-
generated, and then the solution will be improved by in-          dimensional Euclidean vector space of program fragment
silico mutation.                                                  characteristics like identifier name, exponent on the
   Previously encountered programs and their corresponding        identifier, operator, etc. I define the corresponding program
invariants will be stored as memory B cells. When a               fragment antigenic distance as the distance ||P1 - P2||
program similar to a stored one is presented, the time taken      between 2 program fragments P1 and P2 in program
to generate the invariant will be shorter than the time taken     fragment shape space. The program fragment antibody
to generate the original invariant (secondary response).          (invariant) distance is the distance ||I1 - I2|| between 2
   It is shown that such an evolutionary computing approach       program fragments I1 and I2 in program fragment shape
can help make more informed predictions about shapes of           space.
program invariants.                                                  Let us consider 2 program fragments P1: x := x + 2 and
                                                                  P2: t := t + 2. The corresponding antibody (invariant) for
                                                                  P1 is I1: x = x + 2n, where n is a program variable or
                V. COMPONENTS OF THE AIS                          constant (since upon n - 1 iterations, x gets the value x + 2n).
   Having resolved the question of how automated program          Let P1 and I1 constitute the training set. Then the AIS should
verification can benefit from an AIS approach, the specific       be able to produce an antibody (invariant) for the program
components of the AIS have to be determined. What is the          fragment P2 even though it has never encountered this
program analogue of an antigen and an antibody?                   antigen (program) before. The correct invariant is I2 : t = t +
   A program fragment is defined to be either an assignment       2n (where n is a program variable or constant) and this is
statement, a statement containing an iteration construct (for,    indeed what the AIS generates by somatic hypermutation.
while, repeat, etc), or a statement having a conditional check    The program P1 differs from P2 by 1 mutation (replacing x
by t on both sides of the assignment) i.e. the program                                          VIII. RESULTS
fragment antigenic distance ||P1 - P2|| is 1. The invariants I1        The AIS (trained on P1, I1) was presented with suites of
and I2 also differ by 1 mutation (replacing x by t) i.e. the           entire programs and it successfully generated the shape of
program fragment antibody (invariant) distance ||I1 - I2|| is          their invariant. The first program is shown below:
1. Hence, when an AIS trained on (P1, I1) is presented with
P2, it produces I2 using one mutation from I1 (Fig. 1).                  (x,y,u,v) := (a,b,b,0);
                                                                         x := a; y := b;
                                                                         u := b; v := 0;

                                                                         while (x  y) do
                                                                           while (x > y) do x := x - y; v := v + u;
                                                                           end while;
                                                                           while (x < y) do y := y - x; u := u + v;
                                                                           end while;
                                                                         end while

                                                                          This program takes 2 positive integers a and b, and
                                                                       calculates their g.c.d and l.c.m. The AIS presents itself with
                                                                       each assignment statement sequentially. The first 4
                                                                       assignment statements (lines 1-2) have no invariant, since
                                                                       they are not contained inside any loop. Hence, the AIS does
                                                                       not generate any invariant for them. The progress of the
                                                                       algorithm on the next 2 assignment statements (x := x -
                                                                       y; v := v + u;) is shown below:
Fig. 1. AIS mutation from the assignment statement Ag1 (x := x + 2;)
and invariant Ab1 (x + 2n) to Ag2 (t := t + 2;) and invariant
Ab2 (t + 2n) in shape space S.




                        VII. ALGORITHM
   The AIS was implemented in MATLAB and trained on
the antigen (program fragment) P1: x := x + 2 and given the
antibody (invariant) I1: x = x + 2n as a solution (training
phase). The AIS stores the solution I1 as a memory detector.
   When an entire program (as opposed to a program
fragment) is presented to the AIS, it breaks the program up
into program fragments (all the assignment statements in the
                                                                       Fig. 2. AIS mutations for the assignment statements x := x - y; v :=
program), and then “presents” each of these antigens                   v + u;
(fragments) to itself.
   If an antigen (program fragment) P2 “similar” to P1 is                  The AIS starts from the training set (P1: x := x + 2 & I1:
detected, it will generate I1 as a candidate solution. If I1           x = x + 2n) and then mutates the operators and operands to
itself does not act as an invariant, the AIS will keep on              create the invariant I3 : x = x - yn for the program fragment
carrying out mutations on I1 until it evolves the final                P3: x := x - y. The AIS stores I3 in the memory population
antibody (invariant) I2 that will act as the invariant for the         and for the next assignment statement (v := v + u;), it
program presented (somatic hypermutation phase). This is               starts mutating from (P3,I3) until it creates the invariant I4 : v
akin to how the natural immune system mutates B cell                   = v + un for the program fragment P4: v := v + u.
receptors (BCR) and ultimately produces a BCR that can                    For the next set of assignment statements (y := y - x;
recognize the antigen. In the last step, the AIS incorporates Ii       u := u + v;), the AIS then generates the invariants I5: y =
into its memory pool (learning).                                       y - xn and I6: u = u + vn (not shown). The 4 invariants I1, I2,
   The AIS then presents the next program fragment P3,                 I3 & I4 are then combined linearly (with n being substituted
generates the invariant I3 and stores it in the memory                 for all program variables, namely x, y, u, v) to yield the
population, and so on until all program fragments have been            invariant shape Ishape: Ax + Bv + Cy + Du + Exy + Fy2 +
presented. Finally, the AIS combines all invariants linearly,          Guy + Hvy + Jxu + Ku2 + Lvu + Mx2 + Nvx + Pv2 + Q =
producing a polynomial (shape of invariant) that captures the          0, where A, B, C, D, E, F, G, H, J, K, L, M, N, P and Q are
semantics of the entire program.                                       constants or program variables. This is the correct invariant
                                                                       shape, since using quantifier elimination [8], I get the final
                                                                       invariant Ifinal: xu + yv - ab = 0 (with A = B = C = D = E =
                                                                       F = G = K = L = M = N = P = 0, Q = -ab, H = J = 1).
  The AIS was also tested on another standard program [8]                                       REFERENCES
shown below:                                                       [1]  L. N. de Castro and J. Timmis, Artificial Immune Systems: A New
                                                                        Computational Intelligence Approach. London, U.K.: Springer-
  {A  0, B  0}                                                        Verlag, 1996.
  x := A;                                                          [2] J. E. Hunt and D. E. Cooke, “Learning using an artificial immune
                                                                        system,” J. Network Comput. Applicat., vol. 19, no. 2, pp. 189–212,
  y := B;                                                               Apr. 1996.
  z := 1;                                                          [3] D. Dasgupta, Artificial Immune Systems and Their Applications.
                                                                        Berlin, Germany: Springer-Verlag, 1999.
  while y > 0 do                                                   [4] S. A. Hofmeyr and S. Forrest, “Immunity by design: An artificial
  if odd(y) then y := y - 1; z := x * z;                                immune system,” in Proc. Genetic and Evolutionary Computation
  else x := x * x; y := y/2;                                            Conf., July 1999, pp. 1289–1296.
  end while                                                        [5] L. N. de Castro and F. J. Von Zuben. (1999) Artificial Immune
                                                                        Systems:Part I-Basic Theory and Applications. FEEC/Univ.
                                                                        Campinas,Campinas,Brazil.[Online].
This program calculates AB and stores it in z. The AIS                  Available:http://www.dca.fee.unicamp.br/~lnunes/immune.html
correctly calculates the invariant for the program fragment        [6] (2000) Artificial Immune Systems: Part II—A Survey of Applications.
                                                                        FEEC/Univ. Campinas, Campinas, Brazil. [Online]. Available:
P5: z := x * z as I5: z = xn * z. For the program fragment P6:           http://www.dca.fee.unicamp.br/~lnunes/immune.html
x := x * x, it generates the invariant I6: x = exp(x, exp(2,n)),   [7] de Castro, L. N. & Von Zuben, F. J. (2002), "Learning and
where exp() is the exponentiation function. Combining all               Optimization Using the Clonal Selection Principle", IEEE
                                                                        Transactions on Evolutionary Computation, Special Issue on Artificial
the program fragment invariants, gives us the following                 ImmuneSystems,6(3),pp.239-251.
invariant shape:                                                   [8] Kapur, D. Automatically Generating Loop Invariants Using Quantifier
 Ishape: Azxx + Bzxy + Czxz + D.exp(x,exp(2,x)) +                       Elimination (2004). IMACS Intl. Conf. on Applications of Computer
                                                                        Algebra.
E.exp(x,exp(2,y)) + F.exp(x,exp(2,z)) +G = 0.                      [9] Rodriguez, E, & Kapur, D. Automatic Generation of Polynomial Loop
This is the exact shape of the invariants, since quantifier             Invariants: Algebraic Foundations (2004). International Conference on
elimination yields the final invariant                                  Symbolic and Algebraic Computation
Ifinal: zxy = AB (with A = C = D = E = F = 0, G = -AB).            [10] F. M. Burnet, “Clonal selection and after,” in Theoretical
                                                                        Immunology,G. I. Bell, A. S. Perelson, and G. H. Pimbley Jr., Eds.
We can now readily verify the working of the program.                   New York: Marcel Dekker, 1978, pp. 63–85.
When the loop terminates, the invariant is true and y = 0,         [11] The Clonal Selection Theory of Acquired Immunity. Cambridge,U.K.:
which yields the correct postcondition: z = AB.                         Cambridge Univ. Press, 1959.
                                                                   [12] R. S. Sutton and A. G. Barto, Reinforcement Learning: An
                                                                        Introduction.Cambridge, MA: MIT Press, 1998.
            IX. CONCLUSION AND FUTURE WORK                         [13] C. A. Janeway, P. Travers, M.Walport, and J. D. Capra,
                                                                        Immunobiology: The Immune System in Health and Disease, 4th ed.
   I have presented an immune system inspired approach for              NewYork: Garland, 1999.
automated program verification. The AIS algorithm breaks           [14] D. J. Smith, S. Forrest, R. R. Hightower, and S. A. Perelson,
up a program into fragments and presents them to itself. It             “Deriving shape space parameters from immunological data,” J.
                                                                        Theor. Biol., vol. 189, no. 2, pp. 141–150, Nov. 1997.
then generates an invariant in response to each program            [15] P. D. Hodgkin, “Role of cross-reactivity in the development of
fragment and ultimately combines them to create the general             antibody responses,” Immunologist, vol. 6, no. 6, pp. 223–226, 1998.
shape of the invariant. This AIS algorithm was tested on           [16] G. L. Ada and G. Nossal, “The clonal selection theory,” Sci. Amer.,
                                                                        vol. 257, no. 2, pp. 50–57, 1987.
non-trivial benchmark programs [8] and was found to                [17] J. Sprent, “T and B memory cells,” Cell, vol. 76, no. 2, pp. 315–322,
correctly generate the general form of the program invariant.           Jan. 1994.
   Future work will focus on theoretical research into             [18] D. Mason, “Antigen cross-reactivity: Essential in the function of
                                                                        TCRs”Immunologist, vol. 6, no. 6, pp. 220–222, 1998.
whether there are classes of programs for which a linear
                                                                   [19] S. Haykin, Neural Networks—A Comprehensive Foundation, 2nd sed.
combination of individual program fragment invariants                   Englewood Cliffs, NJ: Prentice-Hall, 1999.
might not generate the invariant for the entire program.           [20] C. Berek and M. Ziegner, “The maturation of the immune
Research is also ongoing into how mutations on                          response,”Immun. Today, vol. 14, no. 8, pp. 400–402, 1993.
                                                                   [21] A. J. T. George and D. Gray, “Receptor editing during affinity
exponentiation would affect the invariant e.g. x := x + 2               maturation,” Immun. Today, vol. 20, no. 4, p. 196, 1999.
getting mutated to x := x2 + 2. Lastly, the AIS algorithm          [22] M. C. Nussenzweig, “Immune receptor editing: Revise and select,”
does not consider program fragments having iteration                    Cell, vol. 95, no. 7, pp. 875–878, Dec. 1998.
                                                                   [23] S. Tonegawa, “Somatic generation of antibody diversity,” Nature, vol.
constructs like while, repeat, etc. and future research will            302, no. 14, pp. 575–581, Apr. 1983.
investigate how incorporation of such program fragments            [24] R. W. Floyd. "Assigning meanings to programs." Proceedings of the
can enhance the predictive power of the algorithm.                      American Mathematical Society Symposia on Applied Mathematics.
                                                                        Vol. 19, pp. 19–31. 1967
                                                                   [25] C. A. R. Hoare. "An axiomatic basis for computer programming".
                                                                        Communications of the ACM, 12(10):576–585, October 1969.
                    ACKNOWLEDGMENTS                                     doi:10.1145/363235.363259
                                                                   [26] AS Perelson, FW Wiegel. Some design principles for immune system
  The author wishes to thank Prof. Deepak Kapur and                     recognition, Complexity, 1999
ThanhVu Nguyen for helpful comments.                               [27] A.S. Perelson & G.F. Oster. Theoretical Studies of Clonal Selection:
                                                                        Minimal Antibody Repertoire Size and Reliability of Self-Non-self
                                                                        Discrimination.       J.   theor.    Biol.   (1979)    81,   645-670.
