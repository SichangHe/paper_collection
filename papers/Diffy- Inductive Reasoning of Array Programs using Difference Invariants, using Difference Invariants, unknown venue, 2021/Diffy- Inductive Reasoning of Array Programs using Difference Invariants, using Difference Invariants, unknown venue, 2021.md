                                            Diffy: Inductive Reasoning of Array Programs
                                                      using Difference Invariants

                                             Supratik Chakraborty1 , Ashutosh Gupta1 , and Divyesh Unadkat1,2
                                                      1
                                                          Indian Institute of Technology Bombay, Mumbai, India
                                                                   {supratik,akg}@cse.iitb.ac.in
                                                                      2
                                                                         TCS Research, Pune, India
                                                                        divyesh.unadkat@tcs.com
arXiv:2105.14748v2 [cs.PL] 2 Jul 2021




                                               Abstract. We present a novel verification technique to prove interest-
                                               ing properties of a class of array programs with a symbolic parameter
                                               N denoting the size of arrays. The technique relies on constructing two
                                               slightly different versions of the same program. It infers difference rela-
                                               tions between the corresponding variables at key control points of the
                                               joint control-flow graph of the two program versions. The desired post-
                                               condition is then proved by inducting on the program parameter N ,
                                               wherein the difference invariants are crucially used in the inductive step.
                                               This contrasts with classical techniques that rely on finding potentially
                                               complex loop invaraints for each loop in the program. Our synergistic
                                               combination of inductive reasoning and finding simple difference invari-
                                               ants helps prove properties of programs that cannot be proved even by
                                               the winner of Arrays sub-category from SV-COMP 2021. We have im-
                                               plemented a prototype tool called Diffy to demonstrate these ideas.
                                               We present results comparing the performance of Diffy with that of
                                               state-of-the-art tools.


                                        1    Introduction
                                        Software used in a wide range of applications use arrays to store and update
                                        data, often using loops to read and write arrays. Verifying correctness properties
                                        of such array programs is important, yet challenging. A variety of techniques
                                        have been proposed in the literature to address this problem, including inference
                                        of quantified loop invariants [20]. However, it is often difficult to automatically
                                        infer such invariants, especially when programs have loops that are sequentially
                                        composed and/or nested within each other, and have complex control flows.
                                        This has spurred recent interest in mathematical induction-based techniques for
                                        verifying parametric properties of array manipulating programs [12,42,11,44].
                                        While induction-based techniques are efficient and quite powerful, their Achilles
                                        heel is the automation of the inductive argument. Indeed, this often becomes
                                        the limiting step in applications of induction-based techniques. Automating the
                                        induction step and expanding the class of array manipulating programs to which
                                        induction-based techniques can be applied forms the primary motivation for our
                                        work. Rather than being a stand-alone technique, we envisage our work being
                                        used as part of a portfolio of techniques in a modern program verification tool.
    We propose a novel and practically efficient induction-based technique that
advances the state-of-the-art in automating the inductive step when reasoning
about array manipulating programs. This allows us to automatically verify inter-
esting properties of a large class of array manipulating programs that are beyond
the reach of state-of-the-art induction-based techniques, viz. [12,42]. The work
that comes closest to us is Vajra [12], which is part of the portfolio of tech-
niques in VeriAbs [1] – the winner of SV-COMP 2021 in the Arrays Reach
sub-category. Our work addresses several key limitations of the technique imple-
mented in Vajra, thereby making it possible to analyze a much larger class of
array manipulating programs than can be done by VeriAbs. Significantly, this
includes programs with nested loops that have hitherto been beyond the reach
of automated techniques that use mathematical induction [12,42,44].
    A key innovation in our approach is the construction of two slightly differ-
ent versions of a given program that have identical control flow structures but
slightly different data operations. We automatically identify simple relations,
called difference invariants, between corresponding variables in the two versions
of a program at key control flow points. Interestingly, these relations often turn
out to be significantly simpler than inductive invariants required to prove the
property directly. This is not entirely surprising, since the difference invariants
depend less on what individual statements in the programs are doing, and more
on the difference between what they are doing in the two versions of the pro-
gram. We show how the two versions of a given program can be automatically
constructed, and how differences in individual statements can be analyzed to in-
fer simple difference invariants. Finally, we show how these difference invariants
can be used to simplify the reasoning in the inductive step of our technique.
    We consider programs with (possibly nested) loops manipulating arrays,
where the size of each array is a symbolic integer parameter N (> 0)3 . We
verify (a sub-class of) quantified and quantifier-free properties that may depend
on the symbolic parameter N . Like in [12], we view the verification problem as
one of proving the validity of a parameterized Hoare triple {ϕ(N )} PN {ψ(N )}
for all values of N (> 0), where arrays are of size N in the program PN , and N
is a free variable in ϕ(·) and ψ(·).
    To illustrate the kind of programs that are amenable to our technique, con-
sider the program shown in Fig. 1(a), adapted from an SV-COMP benchmark.
This program has a couple of sequentially composed loops that update arrays
and scalars. The scalars S and F are initialized to 0 and 1 respectively before
the first loop starts iterating. Subsequently, the first loop computes a recurrence
in variable S and initializes elements of the array B to 1 if the corresponding
elements of array A have non-negative values, and to 0 otherwise. The outermost
branch condition in the body of the second loop evaluates to true only if the
program parameter N and the variable S have same values. The value of F is
reset based on some conditions depending on corresponding entries of arrays A
and B. The pre-condition of this program is true; the post-condition asserts that
F is never reset in the second loop.
3
    For a more general class of programs supported by our technique, please see [13].


                                           2
// assume(true)
1. S = 0; F = 1;
2. for(i = 0; i< N; i++) {
                                            // assume(true)
3. S = S + 1;
                                            1. S = 0;
4. if ( A[i] >= 0 ) B[i] = 1;
                                            2. for(i=0; i<N; i++) A[i] = 0;
5. else B[i] = 0;
                                            3. for(j=0; j<N; j++) S = S + 1;
6. }
                                            4. for(k=0; k<N; k++) {
7. for(j = 0; j< N; j++) {
                                            5. for(l=0; l<N; l++) A[l] = A[l] + 1;
8. if(S == N) {
                                            6. A[k] = A[k] + S;
9.    if ( A[j] >= 0 && !B[j] ) F = 0;
                                            7. }
10. if ( A[j] < 0 && B[j] ) F = 0;
                                            // assert(forall x in [0,N), A[x]==2*N)
11. }
12.}
// assert(F == 1)                                                (b)

                     (a)

                               Fig. 1. Motivating Examples
    State-of-the-art techniques find it difficult to prove the assertion in this pro-
gram. Specifically, Vajra [12] is unable to prove the property, since it cannot
reason about the branch condition (in the second loop) whose value depends on
the program parameter N . VeriAbs [1], which employs a sequence of techniques
such as loop shrinking, loop pruning, and inductive reasoning using [12] is also
unable to verify the assertion shown in this program. Indeed, the loops in this
program cannot be merged as the final value of S computed by the first loop
is required in the second loop; hence loop shrinking does not help. Also, loop
pruning does not work due to the complex dependencies in the program and the
fact that the exact value of the recurrence variable S is required to verify the
program. Subsequent abstractions and techniques applied by VeriAbs from its
portfolio are also unable to verify the given post-condition. VIAP [42] translates
the program to a quantified first-order logic formula in the theory of equality
and uninterpreted functions [32]. It applies a sequence of tactics to simplify and
prove the generated formula. These tactics include computing closed forms of
recurrences, induction over array indices and the like to prove the property. How-
ever, its sequence of tactics is unable to verify this example within our time limit
of 1 minute.
   Benchmarks with nested loops are a long standing challenge for most verifiers.
Consider the program shown in Fig. 1(b) with a nested loop in addition to
sequentially composed loops. The first loop initializes entries in array A to 0.
The second loop aggregates a constant value in the scalar S. The third loop is
a nested loop that updates array A based on the value of S. The entries of A
are updated in the inner as well as outer loop. The property asserts that on
termination, each array element equals twice the value of the parameter N .
   While the inductive reasoning of Vajra and the tactics in VIAP do not
support nested loops, the sequence of techniques used by VeriAbs is also un-
able to prove the given post-condition in this program. In sharp contrast, our
prototype tool Diffy is able to verify the assertions in both these programs
automatically within a few seconds. This illustrates the power of the inductive
technique proposed in this paper.
   The technical contributions of the paper can be summarized as follows:


                                           3
 – We present a novel technique based on mathematical induction to prove
   interesting properties of a class of programs that manipulate arrays. The
   crucial inductive step in our technique uses difference invariants from two
   slightly different versions of the same program, and differs significantly from
   other induction-based techniques proposed in the literature [12,42,11,44].
 – We describe algorithms to transform the input program for use in our in-
   ductive verification technique. We also present techniques to infer simple
   difference invariants from the two slightly different program versions, and to
   complete the inductive step using these difference invariants.
 – We describe a prototype tool Diffy that implements our algorithms.
 – We compare Diffy vis-a-vis state-of-the-art tools for verification of C pro-
   grams that manipulate arrays on a large set of benchmarks. We demonstrate
   that Diffy significantly outperforms the winners of SV-COMP 2019, 2020
   and 2021 in the Array Reach sub-category.


2    Overview and Relation to Earlier Work

In this section, we provide an overview of the main ideas underlying our tech-
nique. We also highlight how our technique differs from [12], which comes closest
to our work. To keep the exposition simple, we consider the program PN , shown
in the first column of Fig. 2, where N is a symbolic parameter denoting the
sizes of arrays a and b. We assume that we are given a parameterized pre-
condition ϕ(N ), and our goal is to establish the parameterized post-condition
ψ(N ), for all N > 0. In [12,44], techniques based on mathematical induction (on
N ) were proposed to solve this class of problems. As with any induction-based
technique, these approaches consist of three steps. First, they check if the base
case holds, i.e. if the Hoare triple {ϕ(N )} PN {ψ(N )} holds for small values of
N , say 1 ≤ N ≤ M , for some M > 0. Next, they assume that the inductive
hypothesis {ϕ(N − 1)} PN −1 {ψ(N − 1)} holds for some N ≥ M + 1. Finally,
in the inductive step, they show that if the inductive hypothesis holds, so does
{ϕ(N )} PN {ψ(N )}. It is not hard to see that the inductive step is the most
crucial step in this style of reasoning. It is also often the limiting step, since not
all programs and properties allow for efficient inferencing of {ϕ(N )} PN {ψ(N )}
from {ϕ(N − 1)} PN −1 {ψ(N − 1)}.
    Like in [12,44], our technique uses induction on N to prove the Hoare triple
{ϕ(N )} PN {ψ(N )} for all N > 0. Hence, our base case and inductive hypothesis
are the same as those in [12,44]. However, our reasoning in the crucial inductive
step is significantly different from that in [12,44], and this is where our primary
contribution lies. As we show later, not only does this allow a much larger class of
programs to be efficiently verified compared to [12,44], it also permits reasoning
about classes of programs with nested loops, that are beyond the reach of [12,44].
Since the work of [12] significantly generalizes that of [44], henceforth, we only
refer to [12] when talking of earlier work that uses induction on N .
    In order to better understand our contribution and its difference vis-a-vis the
work of [12], a quick recap of the inductive step used in [12] is essential. The


                                          4
     // ϕ(N) = true
    x = 0;                   x = 0;                 x = 0;                              x = 0;
 for(i=0; i<N; i++)          for(i=0; i<N-1; i++)   for(i=0; i<N-1; i++)               for(i=0; i<N-1; i++)
     x = x + N*N;              x = x + N*N;           x = x + N*N;                        x=x+(N-1)*(N-1);
     a[i] = a[i] + N;          a[i] = a[i] + N ;      a[i] = a[i] + N ;    QN −1          a[i] = a[i] + N-1;   PN −1

                             x = x + N*N;           for(j=0; j<N-1; j++)               for(j=0; j<N-1; j++)
                             a[N-1] = a[N-1]+N;       b[j] = x+N*N+ j;                    b[j] = x + j;
 for(j=0; j<N; j++)          for(j=0; j<N-1; j++)
                                                    x = x + N*N ;                      for(i=0; i<N-1; i++)
     b[j] = x + j;             b[j] = x + j;        a[N-1] = a[N-1]+N;     peel(PN )      x = x + 2*N-1;
                             b[N-1] = x + N-1;      b[N-1] = x + N-1;                     a[i] = a[i] + 1;

          PN                                                                           x = x + N*N;
                                                                                       a[N-1] = a[N-1]+N;      ∂PN
                                                                                       for(k=0; k<N-1; k++)
    //ψ(N) =                                                                            b[k] = b[k] +
     (∀j. b[j] = j + N3 )                                                               (N-1)*(2*N-1)+N*N;

                                                                                       b[N-1] = x + N-1;



                        Fig. 2. Pictorial Depiction of our Program Transformations
inductive step in [12] crucially relies on finding a “difference program” ∂PN and a
“difference pre-condition” ∂ϕ(N ) such that: (i) PN is semantically equivalent to
PN −1 ; ∂PN , where ’;’ denotes sequential composition of programs4 , (ii) ϕ(N ) ⇒
ϕ(N − 1) ∧ ∂ϕ(N ), and (iii) no variable/array element in ∂ϕ(N ) is modified by
PN −1 . As shown in [12], once ∂PN and ∂ϕ(N ) satisfying these conditions are
obtained, the problem of proving {ϕ(N )} PN {ψ(N )} can be reduced to that of
proving {ψ(N − 1) ∧ ∂ϕ(N )} ∂PN {ψ(N )}. This approach can be very effective
if (i) ∂PN is “simpler” (e.g. has fewer loops or strictly less deeply nested loops)
than PN and can be computed efficiently, and (ii) a formula ∂ϕ(N ) satisfying
the conditions mentioned above exists and can be computed efficiently.
     The requirement of PN being semantically equivalent to PN −1 ; ∂PN is a
very stringent one, and finding such a program ∂PN is non-trivial in general.
In fact, the authors of [12] simply provide a set of syntax-guided condition-
ally sound heuristics for computing ∂PN . Unfortunately, when these conditions
are violated (we have found many simple programs where they are violated),
there are no known algorithmic techniques to generate ∂PN in a sound man-
ner. Even if a program ∂PN were to be found in an ad-hoc manner, it may
be as “complex” as PN itself. This makes the approach of [12] ineffective for
analyzing such programs. As an example, the fourth column of Fig. 2 shows
PN −1 followed by one possible ∂PN that ensures PN (shown in the first column
of the same figure) is semantically equivalent to PN −1 ; ∂PN . Notice that ∂PN
in this example has two sequentially composed loops, just like PN had. In ad-
dition, the assignment statement in the body of the second loop uses a more
complex expression than that present in the corresponding loop of PN . Proving
{ψ(N − 1) ∧ ∂ϕ(N )} ∂PN {ψ(N )} may therefore not be any simpler (perhaps
even more difficult) than proving {ϕ(N )} PN {ψ(N )}.
4
     Although the authors of [12] mention that it suffices to find a ∂PN that satisfies
     {ϕ(N )} PN −1 ; ∂PN {ψ(N )}, they do not discuss any technique that takes ϕ(N ) or
     ψ(N ) into account when generating ∂PN .


                                                         5
    In addition to the difficulty of computing ∂PN , it may be impossible to find a
formula ∂ϕ(N ) such that ϕ(N ) ⇒ ϕ(N −1)∧∂ϕ(N ), as required by [12]. This can
                                                                   VN −1           
happen even for fairly routine pre-conditions, such as ϕ(N ) ≡      i=0 A[i] = N .
Notice that there is no ∂ϕ(N ) that satisfies ϕ(N ) ⇒ ϕ(N − 1) ∧ ∂ϕ(N ) in this
case. In such cases, the technique of [12] cannot be used at all, even if PN , ϕ(N )
and ψ(N ) are such that there exists a trivial proof of {ϕ(N )} PN {ψ(N )}.
    The inductive step proposed in this paper largely mitigates the above prob-
lems, thereby making it possible to efficiently reason about a much larger class
of programs than that possible using the technique of [12]. Our inductive step
proceeds as follows. Given PN , we first algorithmically construct two programs
QN −1 and peel(PN ), such that PN is semantically equivalent to QN −1 ; peel(PN ).
Intuitively, QN −1 is the same as PN , but with all loop bounds that depend on
N now modified to depend on N − 1 instead. Note that this is different from
PN −1 , which is obtained by replacing all uses (not just in loop bounds) of N
in PN by N − 1. As we will see, this simple difference makes the generation of
peel(PN ) significantly simpler than generation of ∂PN , as in [12]. While gener-
ating QN −1 and peel(PN ) may sound similar to generating PN −1 and ∂PN [12],
there are fundamental differences between the two approaches. First, as noted
above, PN −1 is semantically different from QN −1 . Similarly, peel(PN ) is also se-
mantically different from ∂PN . Second, we provide an algorithm for generating
QN −1 and peel(PN ) that works for a significantly larger class of programs than
that for which the technique of [12] works. Specifically, our algorithm works for
all programs amenable to the technique of [12], and also for programs that violate
the restrictions imposed by the grammar and conditional heuristics in [12]. For
example, we can algorithmically generate QN −1 and peel(PN ) even for a class of
programs with arbitrarily nested loops – a program feature explicitly disallowed
by the grammar in [12]. Third, we guarantee that peel(PN ) is “simpler” than
PN in the sense that the maximum nesting depth of loops in peel(PN ) is strictly
less than that in PN . Thus, if PN has no nested loops (all programs amenable to
analysis by [12] belong to this class), peel(PN ) is guaranteed to be loop-free. As
demonstrated by the fourth column of Fig. 2, no such guarantees can be given
for ∂PN generated by the technique of [12]. This is a significant difference, since
it greatly simplifies the analysis of peel(PN ) vis-a-vis that of ∂PN .
    We had mentioned earlier that some pre-conditions ϕ(N ) do not admit any
∂ϕ(N ) such that ϕ(N ) ⇒ ϕ(N −1)∧∂ϕ(N ). It is, however, often easy to compute
formulas ϕ0 (N − 1) and ∆ϕ0 (N ) in such cases such that ϕ(N ) ⇒ ϕ0 (N − 1) ∧
∆ϕ0 (N ), and the variables/array elements in ∆ϕ0 (N ) are not modified by either
PN −1 or QN −1 . For example, if we were to consider a (new) pre-condition ϕ(N ) ≡
  VN −1           
    i=0 A[i] = N for the program PN shown        in the first column of Fig. 2, then
           0
                          VN −2                      0
                                                                              
we have ϕ (N − 1) ≡          i=0 A[i] = N and ∆ϕ (N ) ≡ A[N − 1] = N . We
assume the availability of such a ϕ0 (N − 1) and ∆ϕ0 (N ) for the given ϕ(N ). This
significantly relaxes the requirement on pre-conditions and allows a much larger
class of Hoare triples to be proved using our technique vis-a-vis that of [12].
    The third column of Fig. 2 shows QN −1 and peel(PN ) generated by our al-
gorithm for the program PN in the first column of the figure. It is illustrative to

                                         6
compare these with PN −1 and ∂PN shown in the fourth column of Fig. 2. Notice
that QN −1 has the same control flow structure as PN −1 , but is not semanti-
cally equivalent to PN −1 . In fact, QN −1 and PN −1 may be viewed as closely
related versions of the same program. Let VQ and VP denote the set of vari-
ables of QN −1 and PN −1 respectively. We assume VQ is disjoint from VP , and
analyze the joint execution of QN −1 starting from a state satisfying the pre-
condition ϕ0 (N − 1), and PN −1 starting from a state satisfying ϕ(N − 1). The
purpose of this analysis is to compute a difference predicate D(VQ , VP , N − 1)
that relates corresponding variables in QN −1 and PN −1 at the end of their joint
execution. The above problem is reminiscent of (yet, different from) translation
validation [40,49,48,4,46,17,24], and indeed, our calculation of D(VQ , VP , N − 1)
is motivated by techniques from the translation validation literature. An im-
portant finding of our study is that corresponding variables in QN −1 and PN −1
are often related by simple expressions on N , regardless of the complexity of
PN , ϕ(N ) or ψ(N ). Indeed, in all our experiments, we didn’t need to go beyond
quadratic expressions on N to compute D(VQ , VP , N − 1).

     Once the steps described above are completed, we have ∆ϕ0 (N ), peel(PN )
and D(VQ , VP , N − 1). It can now be shown that if the inductive hypothesis,
i.e. {ϕ(N − 1)} PN −1 {ψ(N − 1)} holds, then proving {ϕ(N )} PN {ψ(N )}
reduces to proving {∆ϕ0 (N ) ∧ ψ 0 (N − 1)} peel(PN ) {ψ(N )}, where ψ 0 (N − 1) ≡
∃VP ψ(N −1)∧D(VQ , VP , N −1) . A few points are worth emphasizing here. First,
if D(VQ , VP , N − 1) is obtained as a set of equalities, the existential quantifier in
the formula ψ 0 (N − 1) can often be eliminated simply by substitution. We can
also use quantifier elimination capabilities of modern SMT solvers, viz. Z3 [39],
to eliminate the quantifier, if needed. Second, recall that unlike ∂PN generated
by the technique of [12], peel(PN ) is guaranteed to be “simpler” than PN , and is
indeed loop-free if PN has no nested loops. Therefore, proving {∆ϕ0 (N ) ∧ ψ 0 (N −
1)} peel(PN ) {ψ(N )} is typically significantly simpler than proving {ψ(N −
1) ∧ ∂ϕ(N )} ∂PN {ψ(N )}. Finally, it may happen that the pre-condition in
{∆ϕ0 (N ) ∧ ψ 0 (N −1)} peel(PN ) {ψ(N )} is not strong enough to yield a proof of
the Hoare triple. In such cases, we need to strengthen the existing pre-condition
by a formula, say ξ 0 (N − 1), such that the strengthened pre-condition implies
the weakest pre-condition of ψ(N ) under peel(PN ). Having a simple structure for
peel(PN ) (e.g., loop-free for the entire class of programs for which [12] works)
makes it significantly easier to compute the weakest pre-condition. Note that
ξ 0 (N −1) is defined over the variables in VQ . In order to ensure that the inductive
proof goes through, we need to strengthen the post-condition of the original
program by ξ(N ) such that ξ(N − 1) ∧ D(VQ , VP , N − 1) ⇒ ξ 0 (N − 1). Computing
ξ(N − 1) requires a special form of logical abduction that ensures that ξ(N − 1)
refers only to variables in VP . However, if D(VQ , VP , N − 1) is given as a set
of equalities (as is often the case), ξ(N − 1) can be computed from ξ 0 (N − 1)
simply by substitution. This process of strengthening the pre-condition and post-
condition may need to iterate a few times until a fixed point is reached, similar
to what happens in the inductive step of [12]. Note that the fixed point iterations
may not always converge (verification is undecidable in general). However, in our

                                          7
experiments, convergence always happened within a few iterations. If ξ 0 (N − 1)
denotes the formula obtained on reaching the fixed point, the final Hoare triple
to be proved is {ξ 0 (N − 1) ∧ ∆ϕ0 (N ) ∧ ψ 0 (N − 1)} peel(P   N ) {ξ(N ) ∧ ψ(N )},
where ψ 0 (N − 1) ≡ ∃VP ψ(N − 1) ∧ D(VQ , VP , N − 1) . Having a simple (often
                                                          
loop-free) peel(PN ) significantly simplifies the above process.
    We conclude this section by giving an overview of how QN −1 and peel(PN )
are computed for the program PN shown in the first column of Fig. 2. The second
column of this figure shows the program obtained from PN by peeling the last
iteration of each loop of the program. Clearly, the programs in the first and
second columns are semantically equivalent. Since there are no nested loops in
PN , the peels (shown in solid boxes) in the second column are loop-free program
fragments. For each such peel, we identify variables/array elements modified in
the peel and used in subsequent non-peeled parts of the program. For example,
the variable x is modified in the peel of the first loop and used in the body of the
second loop, as shown by the arrow in the second column of Fig. 2. We replace
all such uses (if needed, transitively) by expressions on the right-hand side of
assignments in the peel until no variable/array element modified in the peel is
used in any subsequent non-peeled part of the program. Thus, the use of x in
the body of the second loop is replaced by the expression x + N*N in the third
column of Fig. 2. The peeled iteration of the first loop can now be moved to
the end of the program, since the variables modified in this peel are no longer
used in any subsequent non-peeled part of the program. Repeating the above
steps for the peeled iteration of the second loop, we get the program shown in
the third column of Fig. 2. This effectively gives a transformed program that
can be divided into two parts: (i) a program QN −1 that differs from PN only
in that all loops are truncated to iterate N − 1 (instead of N ) times, and (ii) a
program peel(PN ) that is obtained by concatenating the peels of loops in PN in
the same order in which the loops appeared in PN . It is not hard to see that PN ,
shown in the first column of Fig. 2, is semantically equivalent to QN −1 ; peel(PN ).
Notice that the construction of QN −1 and peel(PN ) was fairly straightforward,
and did not require any complex reasoning. In sharp contrast, construction of
∂PN , as shown in the bottom half of fourth column of Fig. 2, requires non-trivial
reasoning, and produces a program with two sequentially composed loops.


3     Preliminaries and Notation

We consider programs generated by the grammar shown below:

      PB ::= St
       St ::= St ; St | v := E | A[E] := E | if (BoolE) then St else St |
              for (` := 0; ` < UB; ` := `+1) {St}
        E ::= E op E | A[E] | v | ` | c | N
       op ::= + | - | * | /
      UB ::= UB op UB | ` | c | N
    BoolE ::= E relop E | BoolE AND BoolE | NOT BoolE | BoolE OR BoolE

                                         8
Formally, we consider a program PN to be a tuple (V, L, A, PB, N ), where V
is a set of scalar variables, L ⊆ V is a set of scalar loop counter variables, A
is a set of array variables, PB is the program body, and N is a special symbol
denoting a positive integer parameter of the program. In the grammar shown
above, we assume that A ∈ A, v ∈ V \ L, ` ∈ L and c ∈ Z. We also assume
that each loop L has a unique loop counter variable ` that is initialized at the
beginning of L and is incremented by 1 at the end of each iteration. We assume
that the assignments in the body of L do not update `. For each loop L with
termination condition ` < UB, we require that UB is an expression in terms of
N , variables in L representing loop counters of loops that nest L, and constants
as shown in the grammar. Our grammar allows a large class of programs (with
nested loops) to be analyzed using our technique, and that are beyond the reach
of state-of-the-art tools like [1,12,42].
    We verify Hoare triples of the form {ϕ(N )} PN {ψ(N )}, where the for-
mulas ϕ(N ) and ψ(N ) are either universally quantified formulas of the form
∀I (α(I, N ) ⇒ β(A, V, I, N )) or quantifier-free formulas of the form η(A, V, N ).
In these formulas, I is a sequence of array index variables, α is a quantifier-free
formula in the theory of arithmetic over integers, and β and η are quantifier-free
formulas in the combined theory of arrays and arithmetic over integers. Our tech-
nique can also verify a restricted set of existentially quantified post-conditions.
We give a few illustrative examples in the Appendix.
    For technical reasons, we rename all scalar and array variables in the program
in a pre-processing step as follows. We rename each scalar variable using the well-
known Static Single Assignment (SSA) [43] technique, such that the variable
is written at (at most) one location in the program. We also rename arrays
in the program such that each loop updates its own version of an array and
multiple writes to an array element within the same loop are performed on
different versions of that array. We use techniques for array SSA [30] renaming
studied earlier in the context of compilers, for this purpose. In the subsequent
exposition, we assume that scalar and array variables in the program are already
SSA renamed, and that all array and scalar variables referred to in the pre- and
post-conditions are also expressed in terms of SSA renamed arrays and scalars.


4    Verification using Difference Invariants
The key steps in the application of our technique, as discussed in Section 2, are
A1: Generation of QN −1 and peel(PN ) from a given PN .
A2: Generation of ϕ0 (N − 1) and ∆ϕ0 (N ) from a given ϕ(N ).
A3: Generation of the difference invariant D(VQ , VP , N − 1), given ϕ(N − 1),
    ϕ0 (N − 1), QN −1 and PN −1 .
A4: Proving {∆ϕ0 (N ) ∧ ∃VP ψ(N − 1) ∧ D(VQ , VP , N − 1) } peel(PN ) {ψ(N )},
                                                           
    possibly by generation of ξ 0 (N − 1) and ξ(N ) to strengthen the pre- and
    post-conditions, respectively.
We now discuss techniques for solving each of these sub-problems.


                                        9
4.1   Generating QN −1 and peel(PN )


The procedure illustrated in Fig. 2 (going from the first column to the third
column) is fairly straightforward if none of the loops have any nested loops
within them. It is easy to extend this to arbitrary sequential compositions of
non-nested loops. Having all variables and arrays in SSA-renamed forms makes
it particularly easy to carry out the substitution exemplified by the arrow shown
in the second column of Fig. 2. Hence, we don’t discuss any further the generation
of QN −1 and peel(PN ) when all loops are non-nested.
     The case of nested loops is, how-             for(`1 =0; `1 <N ; `1 ++)
ever, challenging and requires addi-                                            B1
tional discussion. Before we present
                                                      for(`2 =0; `2 <N ; `2 ++)
an algorithm for handling this case, L1 L2
we discuss the intuition using an ab-                                             B2
stract example. Consider a pair of                                              B3
nested loops, L1 and L2 , as shown in
Fig. 3. Suppose that B1 and B3 are
loop-free code fragments in the body             Fig. 3. A Generic Nested Loop
of L1 that precede and succeed the nested loop L2 . Suppose further that the loop
body, B2, of L2 is loop-free. To focus on the key aspects of computing peels of
nested loops, we make two simplifying assumptions: (i) no scalar variable or ar-
ray element modified in B2 is used subsequently (including transitively) in either
B3 or B1, and (ii) every scalar variable or array element that is modified in B1 and
used subsequently in B2, is not modified again in either B1, B2 or B3. Note that
these assumptions are made primarily to simplify the exposition. For a detailed
discussion on how our technique can be used even with some relaxations of these
assumptions, the reader is referred to [13]. The peel of the abstract loops L1 and
L2 is as shown in Fig. 4. The first loop in the peel includes the last iteration of L2
in each of the N − 1 iterations of L1 , that was missed in QN −1 . The subsequent
code includes the last iteration of L1 that was missed in QN −1 .
     Formally, we use the notation L1 (N) to de- for(` =0; ` <N − 1; ` ++)
                                                          1      1           1
note a loop L1 that has no nested loops within
                                                                                   B2
it, and its loop counter, say `1 , increases from
0 to an upper bound that is given by an ex-
                                                                                 B1
pression in N . Similarly, we use L1 (N, L2 (N))
to denote a loop L1 that has another loop L2         for(`2 =0; `2 <N ; `2 ++)
nested within it. The loop counter `1 of L1                                        B2
increases from 0 to an upper bound expres-
                                                                                B3
sion in N , while the loop counter `2 of L2 in-
creases from 0 to an upper bound expression
in `1 and N . Using this notation, L1 (N, L2 (N,     Fig. 4. Peel of the Nested Loop
L3 (N))) represents three nested loops, and so on. Notice that the upper bound
expression for a nested loop can depend not only on N but also on the loop
counters of other loops nesting it. For notational clarity, we also use LPeel(Li ,
a, b) to denote the peel of loop Li consisting of all iterations of Li where the


                                         10
value of `i ranges from a to b-1, both inclusive. Note that if b-a is a constant,
this corresponds to the concatenation of (b-a) peels of Li .
    We will now try to see how we can for(`1 =0; `1 <UL (N-1); `1 ++)
                                                                       1
implement the transformation from the                  LPeel(L2 , UL2 (`1 ,N-1), UL2 (`1 ,N))
first column to the second column of LPeel(L1 , UL1 (N-1), UL1 (N))
Fig. 2 for a nested loop L1 (N, L2 (N)).
The first step is to truncate all loops                   Fig. 5. Peel of L1 (N, L2 (N))
to use N − 1 instead of N in the upper bound expressions. Using the nota-
tion introduced above, this gives the loop L1 (N-1, L2 (N-1)). Note that all
uses of N other than in loop upper bound expressions stay unchanged as
we go from L1 (N, L2 (N)) to L1 (N-1, L2 (N-1)). We now ask: Which are the
loop iterations of L1 (N, L2 (N)) that have been missed (or skipped) in going to
L1 (N-1, L2 (N-1))? Let the upper bound expression of L1 in L1 (N, L2 (N)) be
UL1 (N ), and that of L2 be UL2 (`1 , N ). It is not hard to see that in every it-
eration `1 of L1 , where 0 ≤ `1 < UL1 (N − 1), the iterations corresponding to
`2 ∈ {UL2 (`1 , N − 1), . . . , UL2 (`1 , N ) − 1} have been missed. In addition, all iter-
ations of L1 corresponding to `1 ∈ {UL1 (N − 1), . . . , UL1 (N ) − 1} have also been
missed. This implies that the “peel” of L1 (N, L2 (N)) must include all the above
missed iterations. This peel therefore is the program fragment shown in Fig. 5.
    Notice that if UL2 (`1 ,N) - for(`1 =0; `1 <UL (N-1); `1 ++) {
                                                             1
UL2 (`1 ,N-1) is a constant (as is            for(`2 =0; `2 <UL2 (`1 ,N-1); `2 ++)
the case if UL2 (`1 ,N) is any lin-             LPeel(L3 , UL3 (`1 ,`2 ,N-1), UL3 (`1 ,`2 ,N))
ear function of `1 and N ), then              LPeel(L2 , UL2 (`1 ,N-1), UL2 (`1 ,N))
the peel does not have any loop }
with nesting depth 2. Hence, the LPeel(L1 , UL1 (N-1), UL1 (N))
maximum nesting depth of loops
                                                 Fig. 6. Peel of L1 (N, L2 (N, L3 (N)))
in the peel is strictly less than
that in L1 (N, L2 (N)), yielding a peel that is “simpler” than the original pro-
gram. This argument can be easily generalized to loops with arbitrarily large
nesting depths. The peel of L1 (N, L2 (N, L3 (N))) is as shown in Fig. 6.
    As an illustrative example, for(i=0; i<N; i++) for(i=0; i<N-1; i++)
let us consider the program in                 for(j=0; j<N; j++)        A[i][N-1] = N;
Fig. 7(a), and suppose we wish                   A[i][j] = N;          for(j=0; j<N; j++)
to compute the peel of this pro-                                         A[N-1][j] = N;
gram containing nested loops. In                       (a)                       (b)
this case, the upper bounds of the
loops are UL1 (N ) = UL2 (N ) =                    Fig. 7. (a) Nested Loop & (b) Peel
N . The peel is shown in Fig. 7(b) and consists of two sequentially composed
non-nested loops. The first loop takes into account the missed iterations of the
inner loop (a single iteration in this example) that are executed in PN but are
missed in QN −1 . The second loop takes into account the missed iterations of the
outer loop in QN −1 compared to PN .
    Generalizing the above intuition, Algorithm 1 presents function GenQand-
Peel for computing QN −1 and peel(PN ) for a given PN that has sequentially
composed loops with potentially nested loops. Due to the grammar of our pro-

                                             11
Algorithm 1 GenQandPeel(PN : program)
1: Let sequentially composed loops in PN be in the order L1 , L2 , . . ., Lm ;
2: for each loop Li ∈ TopLevelLoops(PN ) do
3:     hQLi , RLi i ← GenQandPeelForLoop(Li );
4: while ∃v.use(v ) ∈ QLi ∧ def(v) ∈ RLj , for some 1 ≤ j < i ≤ N do           . v is var/array element
5:     Substitute rhs expression for v from RLj in QLi ;                       . If RLj is a loop, abort
6: QN −1 ← QL1 ; QL2 ; . . . ; QLm ;
7: peel(PN ) ← RL1 ; RL2 ; . . . ; RLm ;
8: return hQN −1 , peel(PN )i;
 9: procedure GenQandPeelForLoop(L: loop)
10:    Let UL (N ) be the UB expression of loop L;
11:    QL ← L with N − 1 substituted for N in all UB expressions (including for nested loops);
12:    if L has subloops then
13:        t ← nesting depth of inner-most nested loop in L;
14:        Rt+1 ← empty program with no statements;
15:        for k = t; k ≥ 2; k-- do
16:           for each subloop SLj in Li at nesting depth k do          . Ordered SL1 , SL2 , . . ., SLj
17:               RSLj ← LPeel(SLj , USLj (`1 , . . . , `k−1 , N − 1), USLj (`1 , . . . , `k−1 , N ));
18:           Rk ← for (i=0; i<ULk−1 (N − 1); i++) { Rk+1 ;RSL1 ;RSL2 ;...;RSLj };
19:        RL ← R2 ; LPeel(L, UL (N − 1), UL (N ));
20:    else
21:        RL ← LPeel(L, UL (N − 1), UL (N ));
22:    return hQL , RL i;

grams, our loops are well nested. The method works by traversing over the
structure of loops in the program. In this algorithm QLi and RLi represent the
counterparts of QN −1 and peel(PN ) for loop Li . We create the program QN −1
by peeling each loop in the program and then propagating these peels across
subsequent loops. We identify the missed iterations of each loop in the pro-
gram PN from the upper bound expression UB. Recall that the upper bound
of each loop Lk at nesting depth k, denoted by ULk is in terms of the loop
counters ` of outer loops and the program parameter N . We need to peel
ULk (`1 , `2 , . . . , `k−1 , N ) − ULk (`1 , `2 , . . . , `k−1 , N − 1) number of iterations from
each loop, where `1 ≤ `2 ≤ . . . ≤ `k−1 are counters of the outer nesting loops.
As discussed above, whenever this difference is a constant value, we are guaran-
teed that the loop nesting depth reduces by one. It may so happen that there
are multiple sequentially composed loops SLj at nesting depth k and not just
a single loop Lk . At line 2, we iterate over top level loops and call function
GenQandPeelForLoop(Li ) for each sequentially composed loop Li in PN . At
line 11, we construct QL for loop L. If the loop L has no nested loops, then the
peel is the last iterations computed using the upper bound in line 21. For nested
loops, the loop at line 15 builds the peel for all loops inside L following the above
intuition. The peels of all sub-loops are collected and inserted in the peel of L
at line 19. Since all the peeled iterations are moved after QL of each loop, we
need to repair expressions appearing in QL . The repairs are applied by the loop
at line 4. In the repair step, we identify the right hand side expressions for all
the variables and array elements assigned in the peeled iterations. Subsequently,
the uses of the variables and arrays in QLi that are assigned in RLj are replaced
with the assigned expressions whenever j < i. If RLj is a loop, this step is more
involved and hence currently not considered. Finally at line 8, the peels and Qs
of all top level loops are stitched and returned.


                                                  12
    Note that lines 4 and 5 of Algorithm 1 implement the substitution repre-
sented by the arrow in the second column of Fig. 2. This is necessary in order
to move the peel of a loop to the end of the program. If either of the loops Li or
Lj use array elements as index to other arrays then it can be difficult to iden-
tify what expression to use in QLi for the substitution. However, such scenarios
are observed less often, and hence, they hardly impact the effectiveness of the
technique on programs seen in practice. The peel RLj , from which the expression
to be substituted in QLi has to be taken, itself may have a loop. In such cases,
it can be significantly more challenging to identify what expression to use in
QLi . We use several optimizations to transform the peeled loop before trying to
identify such an expression. If the modified values in the peel can be summa-
rized as closed form expressions, then we can replace the loop in the peel with
its summary. For example consider the peeled loop, for (`1 =0; `1 <N; `1 ++) {
S = S + 1; }. This loop is summarized as S = S + N; before it can be moved
across subsequent code. If the variables modified in the peel of a nested loop are
not used later, then the peel can be trivially moved. In many cases, the loop in
the peel can also be substituted with its conservative over-approximation. We
have implemented some of these optimizations in our tool and are able to verify
several benchmarks with sequentially composed nested loops. It may not always
be possible to move the peel of a nested loop across subsequent loops but we have
observed that these optimizations suffice for many programs seen in practice.

Theorem 1. Let QN −1 and peel(PN ) be generated by application of function
GenQandPeel from Algorithm 1 on program PN . Then PN is semantically
equivalent to QN −1 ; peel(PN ).

Lemma 1. Suppose the following conditions hold;

 – Program PN satisfies our syntactic restrictions (see Section 3).
 – The upper bound expressions of all loops are linear expressions in N and in
   the loop counters of outer nesting loops.

Then, the max nesting depth of loops in peel(PN ) is strictly less than that in PN .

Proof. Let ULk (`1 , . . . , `k−1 , N ) be the upper bound expression of a loop Lk
at nesting depth k. Suppose ULk = c1 .`1 + · · · ck−1 .`k−1 + C.N + D, where
c1 , . . . ck−1 , C and D are constants. Then ULk (`1 , . . . , `k−1 , N ) − ULk (`1 , . . . `k−1 , N −
1) = C, i.e. a constant. Now, recalling the discussion in Section 4.1, we see that
LPeel(Lk , Uk (`1 , . . . , `k−1 , N −1), Uk (`1 , . . . , `k−1 , N )) simply results in con-
catenating a constant number of peels of the loop Lk . Hence, the maximum nest-
ing depth of loops in LPeel(Lk , Uk (`1 , . . . , `k−1 , N − 1), Uk (`1 , . . . , `k−1 , N ))
is strictly less than the maximum nesting depth of loops in Lk .
      Suppose loop L with nested loops (having maximum nesting depth t) is passed
as the argument of function GenQandPeelForLoop (see Algorithm 1). In
line 15 of function GenQandPeelForLoop, we iterate over all loops at nesting
depth 2 and above within L. Let Lk be a loop at nesting depth k, where 2 ≤ k ≤ t.
Clearly, Lk can have at most t − k nested levels of loops within it. Therefore,


                                               13
when LPeel is invoked on such a loop, the maximum nesting depth of loops
in the peel generated for Lk can be at most t − k − 1. From lines 18 and 19
of function GenQandPeelForLoop, we also know that this LPeel can itself
appear at nesting depth k of the overall peel RL . Hence, the maximum nesting
depth of loops in RL can be t − k − 1 + k, i.e. t − 1. This is strictly less than the
maximum nesting depth of loops in L.                                                t
                                                                                    u
Corollary 1. If PN has no nested loops, then peel(PN ) is loop-free.

4.2    Generating ϕ0 (N − 1) and ∆ϕ0 (N )
                                                 VN −1        WN −1
Given ϕ(N ), we check if it is of the form i=0 ρi (or i=0 ρi ), where ρi is
a formula on the ith elements of   VNone  or more WNarrays, and scalars used in PN .
                                      −2              −2
If so, we infer ϕ0 (N − 1) to be i=0 ρi (or i=0 ρi ) and ∆ϕ0 (N ) to be ρN −1
(assuming variables/array elements in ρN −1 are not modified by QN −1 ). Note
that all uses of N in ρi are retained as is (i.e. not changed to N − 1) in ϕ0 (N − 1).
In general, when deriving ϕ0 (N − 1), we do not replace any use of N in ϕ(N ) by
N − 1 unless it is the limit of an iterated conjunct/disjunct as discussed above.
Specifically, if ϕ(N ) doesn’t contain an iterated conjunct/disjunct as above, then
we consider ϕ0 (N −1) to be the same as ϕ(N ) and ∆ϕ0 (N ) to be True. Thus, our
generation of ϕ0 (N −1) and ∆ϕ0 (N ) differs from that of [12]. As discussed earlier,
this makes it possible to reason about a much larger class of pre-conditions than
that admissible by the technique of [12].

4.3   Inferring Inductive Difference Invariants
Once we have PN −1 , QN −1 , ϕ(N −1) and ϕ0 (N −1), we infer difference invariants.
We construct the standard cross-product of programs QN −1 and PN −1 , denoted
as QN −1 × PN −1 , and infer difference invariants at key control points. Note that
PN −1 and QN −1 are guaranteed to have synchronized iterations of correspond-
ing loops (both are obtained by restricting the upper bounds of all loops to use
N − 1 instead of N ). However, the conditional statements within the loop body
may not be synchronized. Thus, whenever we can infer that the corresponding
conditions are equivalent, we synchronize the branches of the conditional state-
ment. Otherwise, we consider all four possibilities of the branch conditions. It
can be seen that the net effect of the cross-product is executing the programs
PN −1 and QN −1 one after the other.
    We run a dataflow analysis pass over the constructed product graph to infer
difference invariants at loop head, loop exit and at each branch condition. The
only dataflow values of interest are differences between corresponding variables
in QN −1 and PN −1 . Indeed, since structure and variables of QN −1 and PN −1 are
similar, we can create the correspondence map between the variables. We start
the difference invariant generation by considering relations between correspond-
ing variables/array elements appearing in pre-conditions of the two programs.
We apply static analysis that can track equality expressions (including disjunc-
tions over equality expressions) over variables as we traverse the program. These
equality expressions are our difference invariants.


                                         14
     We observed in our experiments the most of the inferred equality expressions
are simple expressions of N (atmost quadratic in N ). This not totally surprising
and similar observations have also been independently made in [24,15,4]. Note
that the difference invariants may not always be equalities. We can easily extend
our analysis to learn inequalities using interval domains in static analysis. We
can also use a library of expressions to infer difference invariants using a guess-
and-check framework. Moreover, guessing difference invariants can be easy as
in many cases the difference expressions may be independent of the program
constructs, for example, the equality expression v = v0 where v ∈ PN −1 and
v0 ∈ QN −1 does not depend on any other variable from the two programs.
     For the example in Fig. 2, the difference invariant at the head of the first loop
of QN −1 ×PN −1 is D(VQ , VP , N −1) ≡ (x0 − x = i × (2 × N − 1) ∧ ∀i ∈ [0, N − 1),
a0 [i] − a[i] = 1), where x, a ∈ VP and x0 , a0 ∈ VQ . Given this, we easily get
x0 − x = (N − 1) × (2 × N − 1) when the first loop terminates. For the second
loop, D(VQ , VP , N −1) ≡ (∀j ∈ [0, N − 1), b0 [j] − b[j] = (x0 − x) + N2 = (N − 1)×
(2 × N − 1) + N2 ).
     Note that the difference invariants and its computation are agnostic of the
given post-condition. Hence, our technique does not need to re-run this analysis
for proving a different post-condition for the same program.

4.4   Verification using Inductive Difference Invariants
We present our method Diffy for verification of programs using inductive dif-
ference invariants in Algorithm 2. It takes a Hoare triple {ϕ(N )} PN {ψ(N )}
as input, where ϕ(N ) and ψ(N ) are pre- and post-condition formulas. We check
the base in line 1 to verify the Hoare triple for N = 1. If this check fails, we
report a counterexample. Subsequently, we compute QN −1 and peel(PN ) as de-
scribed in section 4.1 using the function GenQandPeel from Algorithm 1. At
line 5, we compute the formulas ϕ0 (N − 1) and ∆ϕ0 (N ) as described in sec-
tion 4.2. For automation, we analyze the quantifiers appearing in ϕ(N ) and
modify the quantifier ranges such that the conditions in section 4.2 hold. We
infer difference invariants D(VQ , VP , N − 1) on line 6 using the method described
in section 4.3, wherein VQ and VP are sets of variables from QN −1 and PN −1
respectively. At line 7, we compute ψ 0 (N − 1) by eliminating variables VP from
PN −1 from ψ(N − 1) ∧ D(VQ , VP , N − 1). At line 8, we check the inductive step of
our analysis. If the inductive step succeeds, then we conclude that the assertion
holds. If that is not the case then, we try to iteratively strengthen both the pre-
and post-condition of peel(PN ) simultaneously by invoking Strengthen.
    The function Strengthen first initializes the formula χ(N ) with ψ(N ) and
the formulas ξ(N ) and ξ 0 (N − 1) to True. To strengthen the pre-condition of
peel(PN ), we infer a formula χ0 (N − 1) using Dijkstra’s weakest pre-condition
computation of χ(N ) over the peel(PN ) in line 17. It may happen that we are
unable to infer such a formula. In such a case, if the program peel(PN ) has
loops then we recursively invoke Diffy at line 20 to further simplify the pro-
gram. Otherwise, we abandon the verification effort (line 22). We use quantifier
elimination to infer χ(N − 1) from χ0 (N − 1) and D(VQ , VP , N − 1)) at line 7.

                                         15
Algorithm 2 Diffy( {ϕ(N )} PN {ψ(N )} )
1: if {ϕ(1)} P1 {ψ(1)} fails then                                                 . Base case for N=1
2:    print “Counterexample found!”;
3:    return False;

 4: hQN −1 , peel(PN )i ← GenQandPeel(PN );
 5: hϕ0 (N − 1), ∆ϕ0 (N )i ← FormulaDiff(ϕ(N ));                      . ϕ(N ) ⇒ ϕ0 (N − 1) ∧ ∆ϕ0 (N )
 6: D(VQ , VP , N − 1) ← InferDiffInvs(QN −1 , PN −1 , ϕ0 (N − 1), ϕ(N − 1));
 7: ψ0 (N − 1) ← QE(VP , ψ(N − 1) ∧ D(VQ , VP , N − 1));
 8: if {ψ0 (N − 1) ∧ ∆ϕ0 (N )} peel(PN ) {ψ(N )} then
 9:     return True;                                                         . Verification Successful
10: else
                                                           0            0
11:      return Strengthen(PN , peel(PN ), ϕ(N ), ψ(N ), ψ (N − 1), ∆ϕ (N ), D(VQ , VP , N ));

12: procedure Strengthen(PN , peel(PN ), ϕ(N ), ψ(N ), ψ0 (N − 1), ∆ϕ0 (N ), D(VQ , VP , N ))
13:    χ(N ) ← ψ(N );
14:    ξ(N ) ← True;
15:    ξ 0 (N − 1) ← True;
16:    repeat
17:         χ0 (N − 1) ← WP(χ(N ), peel(PN ));                       . Dijkstra’s WP for loop free code
18:         if χ0 (N − 1) = ∅ then
19:              if peel(PN ) has a loop then
20:                  return Diffy({ξ 0 (N − 1) ∧ ∆ϕ0 (N ) ∧ ψ 0 (N − 1)} peel(PN ) {ξ(N ) ∧ ψ(N )});
21:              else
22:                  return False;                                                    . Unable to prove
23:         χ(N ) ← QE(VQ , χ0 (N ) ∧ D(VQ , VP , N ));
24:         ξ(N ) ← ξ(N ) ∧ χ(N );
25:         ξ 0 (N − 1) ← ξ 0 (N − 1) ∧ χ0 (N − 1);
26:         if {ϕ(1)} P1 {ξ(1)} fails then
27:              return False;                                                        . Unable to prove
28:         if {ξ 0 (N − 1) ∧ ∆ϕ0 (N ) ∧ ψ 0 (N − 1)} peel(PN ) {ξ(N ) ∧ ψ(N )} holds then
29:              return True;                                                  . Verification Successful
30:    until timeout;
31:    return False;

     The inferred pre-conditions χ(N ) and χ0 (N −1) are accumulated in ξ(N ) and
 0
ξ (N − 1), which strengthen the post-conditions of PN and QN −1 respectively in
lines 24 - 25. We again check the base case for the inferred formulas in ξ(N ) at
line 26. If the check fails we abandon the verification attempt at line 27. If the
base case succeeds, we then proceed to the inductive step. When the inductive
step succeeds, we conclude that the assertion is verified. Otherwise, we continue
in the loop and try to infer more pre-conditions untill we run out of time.
     The pre-condition in Fig. 2 is φ(N ) ≡ True and the post-condition is ψ(N ) ≡
∀j ∈ [0, N), b[j] = j + N3 ). At line 5, φ0 (N − 1) and ∆φ0 (N − 1) are computed
to be True. D(VQ , VP , N − 1) is the formula computed in Section 4.3. At line 7,
ψ 0 (N −1) ≡ (∀j ∈ [0, N − 1), b0 [j] = j + (N − 1)3 + (N − 1) × (2 × N − 1) + N2 =
j + N3 ). The algortihm then invokes Strengthen at line 11 which infers the
formulas χ0 (N − 1) ≡ (x0 = (N − 1)3 ) at line 17 and χ(N ) ≡ (x = N3 ) at line 23.
These are accumulated in ξ 0 (N − 1) and ξ(N ), simultaneosuly strengthening the
pre- and post-condition. Verification succeeds after this strengthening iteration.
     The following theorem guarantees the soundness of our technique.

Theorem 2. Suppose there exist formulas ξ 0 (N ) and ξ(N ) and an integer M >
0 such that the following hold

 – {ϕ(N )} PN {ψ(N ) ∧ ξ(N )} holds for 1 ≤ N ≤ M , for some M > 0.
 – ξ(N ) ∧ D(VQ , VP , N ) ⇒ ξ 0 (N ) for all N > 0.


                                                  16
           Program        Diffy        Vajra VeriAbs              VIAP
          Category     S    U TO S          U      S TO S           U TO
          Safe C1 110 110 0      0 110 0           96 14 16          1    93
          Safe C2 24 21     0    3     0    24      5   19     4     0    20
          Safe C3 23 20     3    0     0    23      9   14     0    23     0
            Total 157 151 3      3 110 47 110 47 20 24 113
         Unsafe C1 99 98    1    0    98     1     84 15 98          0     1
         Unsafe C2 24 24    0    0    17     7     19    5    22     0     2
         Unsafe C3 23 20    3    0     0    23 22        1     0    23     0
            Total 146 142 4      0 115 31 125 21 120 23                    3
Table 1. Summary of the experimental results. S is successful result. U is inconclusive
result. TO is timeout.

 – {ξ 0 (N − 1) ∧ ∆ϕ0 (N ) ∧ ψ 0 (N − 1)} peel(PN ) {ξ(N ) ∧ ψ(N )}holds for all
   N ≥ M , where ψ 0 (N − 1) ≡ ∃VP ψ(N − 1) ∧ D(VQ , VP , N − 1) .

Then {ϕ(N )} PN {ψ(N )} holds for all N > 0.


5    Experimental Evaluation

We have instantiated our technique in a prototype tool called Diffy. It is written
in C++ and is built using the LLVM(v6.0.0) [31] compiler. We use the SMT solver
Z3(v4.8.7) [39] for proving Hoare triples of loop-free programs. Diffy and the
supporting data to replicate the experiments are openly available at [14].
    Setup. All experiments were performed on a machine with Intel i7-6500U
CPU, 16GB RAM, running at 2.5 GHz, and Ubuntu 18.04.5 LTS operating sys-
tem. We have compared the results obtained from Diffy with Vajra(v1.0) [12],
VIAP(v1.1) [42] and VeriAbs(v1.4.1-12) [1]. We choose Vajra which also em-
ploys inductive reasoning for proving array programs and verify the benchmarks
in its test-suite. We compared with VeriAbs as it is the winner of the arrays
sub-category in SV-COMP 2020 [6] and 2021 [7]. VeriAbs applies a sequence of
techniques from its portfolio to verify array programs. We compared with VIAP
which was the winner in arrays sub-category in SV-COMP 2019 [5]. VIAP also
employs a sequence of tactics, implemented for proving a variety of array pro-
grams. Diffy does not use multiple techniques, however we choose to compare it
with these portfolio verifiers to show that it performs well on a class of programs
and can be a part of their portfolio. All tools take C programs in the SV-COMP
format as input. Timeout of 60 seconds was set for each tool. A summary of the
results is presented in Table 1.
    Benchmarks. We have evaluated Diffy on a set of 303 array benchmarks,
comprising of the entire test-suite of [12], enhanced with challenging benchmarks
to test the efficacy of our approach. These benchmarks take a symbolic parameter
N which specifies the size of each array. Assertions are (in-)equalities over array
elements, scalars and (non-)linear polynomial terms over N . We have divided
both the safe and unsafe benchmarks in three categories. Benchmarks in C1
category have standard array operations such as min, max, init, copy, compare


                                          17
               60                                                                              60
                        Diffy                                                                           Diffy
                        Vajra                                                                           VeriAbs
               50       VeriAbs                                                                50       VIAP
                        VIAP                                                                            Vajra


               40                                                                              40
CPU time (s)




                                                                                CPU time (s)
               30                                                                              30



               20                                                                              20



               10                                                                              10



               0                                                                                0
                    0     20      40   60       80      100   120   140   160                       0      20     40   60           80   100   120   140
                                            instances                                                                        instances


                                            (a)                                                                             (b)

                        Fig. 8. Cactus Plots (a) All Safe Benchmarks (b) All Unsafe Benchmarks
as well as benchmarks that compute polynomials. In these benchmarks, branch
conditions are not affected by the value of N , operations such as modulo and
nested loops are not present. There are 110 safe and 99 unsafe programs in the
C1 category in our test-suite. In C2 category, the branch conditions are affected
by change in the program parameter N and operations such as modulo are used
in these benchmarks. These benchmarks do not have nested loops in them. There
are 24 safe and unsafe benchmarks in the C2 category. Benchmarks in category
C3 are programs with atleast one nested loop in them. There are 23 safe and
unsafe programs in category C3 in our test-suite. The test-suite has a total of
157 safe and 146 unsafe programs.
    Analysis. Diffy verified 151 safe benchmarks, compared to 110 verified by
Vajra as well as VeriAbs and 20 verified by VIAP. Diffy was unable to verify
6 safe benchmarks. In 3 cases, the smt solver timed out while trying to prove
the induction step since the formulated query had a modulus operation and in
3 cases it was unable to compute the predicates needed to prove the assertions.
Vajra was unable to verify 47 programs from categories C2 and C3. These are
programs with nested loops, branch conditions affected by N , and cases where it
could not compute the difference program. The sequence of techniques employed
by VeriAbs, ran out of time on 47 programs while trying to prove the given
assertion. VeriAbs proved 2 benchmarks in category C2 and 3 benchmarks
in category C3 where Diffy was inconclusive or timed out. VeriAbs spends
considerable amount of time on different techniques in its portfolio before it
resorts to Vajra and hence it could not verify 14 programs that Vajra was able
to prove efficiently. VIAP was inconclusive on 24 programs which had nested
loops or constructs that could not be handled by the tool. It ran out of time on
113 benchmarks as the initial tactics in its sequence took up the allotted time
but could not verify the benchmarks. Diffy was able to verify all programs that
VIAP and Vajra were able to verify within the specified time limit.
    The cactus plot in Figure 8(a) shows the performance of each tool on all
safe benchmarks. Diffy was able to prove most of the programs within three
seconds. The cactus plot in Figure 9(a) shows the performance of each tool on
safe benchmarks in C1 category. Vajra and Diffy perform equally well in the
C1 category. This is due to the fact that both tools perform efficient inductive


                                                                                18
               60                                                                                         60
                        Vajra                                                                                      Vajra
                        Diffy                                                                                      Diffy
               50       VeriAbs                                                                           50       VIAP
                        VIAP                                                                                       VeriAbs


               40                                                                                         40
CPU time (s)




                                                                                         CPU time (s)
               30                                                                                         30



               20                                                                                         20



               10                                                                                         10



               0                                                                                           0
                    0             20    40                60        80        100                              0             20   40               60   80   100
                                                  instances                                                                            instances


                                                  (a)                                                                                  (b)

                        Fig. 9. Cactus Plots (a) Safe C1 Benchmarks (b) Unsafe C1 Benchmarks
reasoning. Diffy outperforms VeriAbs and VIAP in this category. The cactus
plot in Figure 10(a) shows the performance of each tool on safe benchmarks
in the combined categories C2 and C3, that are difficult for Vajra as most of
these programs are not within its scope. Diffy out performs all other tools in
categories C2 and C3. VeriAbs was an order of magnitude slower on programs
it was able to verify, as compared to Diffy. VeriAbs spends significant amount
of time in trying techniques from its portfolio, including Vajra, before one of
them succeeds in verifying the assertion or takes up the entire time allotted to it.
VIAP took 70 seconds more on an average as compared to Diffy to verify the
given benchmark. VIAP also spends a large portion of time in trying different
tactics implemented in the tool and solving the recurrence relations in programs.
    Our technique reports property violations when the base case of the analy-
sis fails for small fixed values of N . While the focus of our work is on proving
assertions, we report results on unsafe versions of the safe benchmarks from our
test-suite. Diffy was able to detect a property violation in 142 unsafe programs
and was inconclusive on 4 benchmarks. Vajra detected violations in 115 pro-
grams and was inconclusive on 31 programs. VeriAbs reported 125 programs as
unsafe and ran out of time on 21 programs. VIAP reported property violation
in 120 programs, was inconclusive on 23 programs and timed out on 3 programs.
   The cactus plot in Figure 8(b) shows the performance of each tool on all
unsafe benchmarks. Diffy was able to detect a violation faster than all other
               60                                                                                         60
                        Diffy                                                                                      Diffy
                        VeriAbs                                                                                    VeriAbs
               50       VIAP                                                                              50       VIAP
                        Vajra                                                                                      Vajra


               40                                                                                         40
CPU time (s)




                                                                                           CPU time (s)




               30                                                                                         30



               20                                                                                         20



               10                                                                                         10



               0                                                                                           0
                    0              10        20                30        40         50                         0             10   20               30   40   50
                                                  instances                                                                            instances


                                                  (a)                                                                                  (b)

Fig. 10. Cactus Plots (a) Safe C2 & C3 Benchmarks (b) Unsafe C2 & C3 Benchmarks


                                                                                         19
               100                                                                               100
                          Diffy                                                                            Diffy
                          Vajra                                                                            VeriAbs
                          VeriAbs                                                                          VIAP
                80        VIAP                                                                    80       Vajra

                60                                                                                60
CPU time (s)




                                                                                  CPU time (s)
                40                                                                                40


                20                                                                                20


                 0                                                                                 0
                     0     20       40   60       80      100   120   140   160                        0     20      40   60         80    100   120   140
                                              instances                                                                        instances

                                              (a)                                                                              (b)

                 Fig. 11. Cactus Plots. TO=100s. (a) Safe Benchmarks (b) Unsafe Benchmarks
tools and on more benchmarks from the test-suite. Figure 9(b) and Figure 10(b)
give a finer glimpse of the performance of these tools on the categories that
we have defined. In the C1 category, Diffy and Vajra have comparable per-
formance and Diffy disproves the same number of benchmarks as Vajra and
VIAP. In C2 and C3 categories, we are able to detect property violations in
more benchmarks than other tools in less time.
    To observe any changes in the performance of these, we also ran them with an
increased time out of 100 seconds. Performance remains unchanged for Diffy,
Vajra and VeriAbs on both safe and unsafe benchmarks, and of VIAP on
unsafe benchmarks. VIAP was able to additionally verify 89 safe programs in
categories C1 and C2 with the increased time limit.


6                        Related Work

Techniques based on Induction. Our work is related to several efforts that apply
inductive reasoning to verify properties of array programs. Our work subsumes
the full-program induction technique in [12] that works by inducting on the en-
tire program via a program parameter N . We propose a principled method for
computation and use of difference invariants, instead of computing difference
programs which is more challenging. An approach to construct safety proofs
by automatically synthesizing squeezing functions that shrink program traces is
proposed in [27]. Such functions are not easy to synthesize, whereas difference
invariants are relatively easy to infer. In [11], the post-condition is inductively
established by identifying a tiling relation between the loop counter and array
indices used in the program. Our technique can verify programs from [11], when
supplied with the tiling relation. [44] identifies recurrent program fragments for
induction using the loop counter. They require restrictive data dependencies,
called commutativity of statements, to move peeled iterations across subsequent
loops. Unfortunately, these restrictions are not satisfied by a large class of pro-
grams in practice, where our technique succeeds.
    Difference Computation. Computing differences of program expressions has
been studied for incremental computation of expensive expressions [41,35], op-
timizing programs with arrays [34], and checking data-structure invariants [45].


                                                                              20
These differences are not always well suited for verifying properties, in contrast
with the difference invariants which enable inductive reasoning in our case.
    Logic based reasoning. In [21], trace logic that implicitly captures inductive
loop invariants is described. They use theorem provers to introduce and prove
lemmas at arbitrary time points in the program, whereas we infer and prove
lemmas at key control points during the inductive step using SMT solvers. VIAP
[42] translates the program to an quantified first-order logic formula using the
scheme proposed in [32]. It uses a portfolio of tactics to simplify and prove
the generated formulas. Dedicated solvers for recurrences are used whereas our
technique adapts induction for handling recurrences.
    Invariant Generation. Several techniques generate invariants for array pro-
grams. QUIC3 [25], FreqHorn [19] and [9] infer universally quantified invariants
over arrays for Constrained Horn Clauses (CHCs). Template-based techniques
[23,47,8] search for inductive quantified invariants by instantiating parameters
of a fixed set of templates. We generate relational invariants, which are often
easier to infer compared to inductive quantified invariants for each loop.
    Abstraction-based Techniques. Counterexample-guided abstraction refinement
using prophecy variables for programs with arrays is proposed in [36]. Veri-
Abs [1] uses a portfolio of techniques, specifically to identify loops that can be
soundly abstracted by a bounded number of iterations. Vaphor [38] transforms
array programs to array-free Horn formulas to track bounded number of array
cells. Booster [3] combines lazy abstraction based interpolation[2] and acceler-
ation [10,28] for array programs. Abstractions in [16,18,22,26,29,33,37] implicitly
or explicitly partition the range array indices to infer and prove facts on array
segments. In contrast, our method does not rely on abstractions.


7   Conclusion

We presented a novel verification technique that combines generation of dif-
ference invariants and inductive reasoning. These invariants relate correspond-
ing variables and arrays from two versions of a program and are easy to infer
and prove. These invariants facilitate inductive reasoning by assisting in the in-
ductive step. We have instantiated these techniques in our prototype Diffy.
Experiments shows that Diffy out-performs the tools that won the Arrays sub-
category in SV-COMP 2019, 2020 and 2021. Investigations in using synthesis
techniques for automatic generation of difference invariants to verify properties
of array manipulating programs is a part of future work.


References

 1. Afzal, M., Chakraborty, S., Chauhan, A., Chimdyalwar, B., Darke, P., Gupta, A.,
    Kumar, S., Babu M, C., Unadkat, D., Venkatesh, R.: Veriabs : Verification by
    abstraction and test generation (competition contribution). In: Proc. of TACAS.
    pp. 383–387 (2020)


                                        21
 2. Alberti, F., Bruttomesso, R., Ghilardi, S., Ranise, S., Sharygina, N.: Lazy abstrac-
    tion with interpolants for arrays. In: Proc. of LPAR. pp. 46–61 (2012)
 3. Alberti, F., Ghilardi, S., Sharygina, N.: Booster: An acceleration-based verification
    framework for array programs. In: Proc. of ATVA. pp. 18–23 (2014)
 4. Barthe, G., Crespo, J.M., Kunz, C.: Relational verification using product programs.
    In: Proc. of FM. pp. 200–214 (2011)
 5. Beyer, D.: Competition on software verification (SV-COMP) (2019), http://
    sv-comp.sosy-lab.org/2019/
 6. Beyer, D.: Competition on software verification (SV-COMP) (2020), http://
    sv-comp.sosy-lab.org/2020/
 7. Beyer, D.: Competition on software verification (SV-COMP) (2021), http://
    sv-comp.sosy-lab.org/2021/
 8. Beyer, D., Henzinger, T.A., Majumdar, R., Rybalchenko, A.: Invariant synthesis
    for combined theories. In: Proc. of VMCAI. pp. 378–394 (2007)
 9. Bjørner, N., McMillan, K.L., Rybalchenko, A.: On solving universally quantified
    horn clauses. In: Proc. of SAS. pp. 105–125 (2013)
10. Bozga, M., Iosif, R., Konecný, F.: Fast acceleration of ultimately periodic relations.
    In: Proc. of CAV. pp. 227–242 (2010)
11. Chakraborty, S., Gupta, A., Unadkat, D.: Verifying array manipulating programs
    by tiling. In: Proc. of SAS. pp. 428–449 (2017)
12. Chakraborty, S., Gupta, A., Unadkat, D.: Verifying array manipulating programs
    with full-program induction. In: Proc. of TACAS. pp. 22–39 (2020)
13. Chakraborty, S., Gupta, A., Unadkat, D.: Diffy: Inductive reasoning of array pro-
    grams using difference invariants (2021), https://arxiv.org/abs/2105.14748
14. Chakraborty, S., Gupta, A., Unadkat, D.: Diffy: Inductive rea-
    soning of array programs using difference invariants (Apr 2021).
    https://doi.org/10.6084/m9.figshare.14509467
15. Churchill, B., Padon, O., Sharma, R., Aiken, A.: Semantic program alignment for
    equivalence checking. In: Proc. of PLDI. pp. 1027–1040 (2019)
16. Cousot, P., Cousot, R., Logozzo, F.: A parametric segmentation functor for fully
    automatic and scalable array content analysis. In: Proc. of POPL. pp. 105–118
    (2011)
17. Dahiya, M., Bansal, S.: Black-box equivalence checking across compiler optimiza-
    tions. In: Proc of APLAS. pp. 127–147 (2017)
18. Dillig, I., Dillig, T., Aiken, A.: Fluid updates: Beyond strong vs. weak updates. In:
    Proc. of ESOP. pp. 246–266 (2010)
19. Fedyukovich, G., Prabhu, S., Madhukar, K., Gupta, A.: Quantified invariants via
    syntax-guided-synthesis. In: Proc. of CAV. pp. 259–277 (2019)
20. Flanagan, C., Qadeer, S.: Predicate abstraction for software verification. In: Proc.
    of POPL. pp. 191–202 (2002)
21. Georgiou, P., Gleiss, B., Kovács, L.: Trace logic for inductive loop reasoning. In:
    Proc. of FMCAD. pp. 255–263 (2020)
22. Gopan, D., Reps, T.W., Sagiv, S.: A framework for numeric analysis of array
    operations. In: Proc. of POPL. pp. 338–350 (2005)
23. Gulwani, S., McCloskey, B., Tiwari, A.: Lifting abstract interpreters to quantified
    logical domains. In: Proc. of POPL. pp. 235–246 (2008)
24. Gupta, S., Rose, A., Bansal, S.: Counterexample-guided correlation algorithm for
    translation validation. Proc. of OOPSLA 4, 1–29 (2020)
25. Gurfinkel, A., Shoham, S., Vizel, Y.: Quantifiers on demand. In: Proc. of ATVA.
    pp. 248–266 (2018)


                                            22
26. Halbwachs, N., Péron, M.: Discovering properties about arrays in simple programs.
    In: Proc. of PLDI. pp. 339–348 (2008)
27. Ish-Shalom, O., Itzhaky, S., Rinetzky, N., Shoham, S.: Putting the squeeze on array
    programs: Loop verification via inductive rank reduction. In: Proc. of VMCAI. pp.
    112–135 (2020)
28. Jeannet, B., Schrammel, P., Sankaranarayanan, S.: Abstract acceleration of general
    linear loops. In: Proc. of POPL. pp. 529–540 (2014)
29. Jhala, R., McMillan, K.L.: Array abstractions from proofs. In: Proc. of CAV. pp.
    193–206 (2007)
30. Knobe, K., Sarkar, V.: Array ssa form and its use in parallelization. In: Proc. of
    POPL. pp. 107–120 (1998)
31. Lattner, C.: Llvm and clang: Next generation compiler technology. In: The BSD
    Conference. pp. 1–2 (2008)
32. Lin, F.: A formalization of programs in first-order logic with a discrete linear order.
    Artificial Intelligence 235, 1–25 (2016)
33. Liu, J., Rival, X.: Abstraction of arrays based on non contiguous partitions. In:
    Proc. of VMCAI. pp. 282–299 (2015)
34. Liu, Y.A., Stoller, S.D., Li, N., Rothamel, T.: Optimizing aggregate array compu-
    tations in loops. TOPLAS 27(1), 91–125 (2005)
35. Liu, Y.A., Stoller, S.D., Teitelbaum, T.: Static caching for incremental computa-
    tion. TOPLAS 20(3), 546–585 (1998)
36. Mann, M., Irfan, A., Griggio, A., Padon, O., Barrett, C.: Counterexample-guided
    prophecy for model checking modulo the theory of arrays. In: Proc. of TACAS
    (2021)
37. Monniaux, D., Alberti, F.: A simple abstraction of arrays and maps by program
    translation. In: Proc. of SAS. pp. 217–234 (2015)
38. Monniaux, D., Gonnord, L.: Cell morphing: From array programs to array-free
    horn clauses. In: Proc. of SAS. pp. 361–382 (2016)
39. de Moura, L.M., Bjørner, N.: Z3: an efficient SMT solver. In: Proc. of TACAS. pp.
    337–340 (2008)
40. Necula, G.C.: Translation validation for an optimizing compiler. In: Proc of PLDI.
    pp. 83–94 (2000)
41. Paige, R., Koenig, S.: Finite differencing of computable expressions. TOPLAS 4(3),
    402–454 (1982)
42. Rajkhowa, P., Lin, F.: Extending viap to handle array programs. In: Proc. of
    VSTTE. pp. 38–49 (2018)
43. Rosen, B.K., Wegman, M.N., Zadeck, F.K.: Global value numbers and redundant
    computations. In: Proc. of POPL. pp. 12–27 (1988)
44. Seghir, M.N., Brain, M.: Simplifying the verification of quantified array assertions
    via code transformation. In: Proc. of LOPSTR. pp. 194–212 (2012)
45. Shankar, A., Bodik, R.: Ditto: Automatic incrementalization of data structure
    invariant checks (in java). ACM SIGPLAN Notices 42(6), 310–319 (2007)
46. Sharma, R., Schkufza, E., Churchill, B., Aiken, A.: Data-driven equivalence check-
    ing. In: Proc of OOPSLA. pp. 391–406 (2013)
47. Srivastava, S., Gulwani, S.: Program verification using templates over predicate
    abstraction. ACM Sigplan Notices 44(6), 223–234 (2009)
48. Zaks, A., Pnueli, A.: Covac: Compiler validation by program analysis of the cross-
    product. In: Proc of FM. pp. 35–51 (2008)
49. Zuck, L., Pnueli, A., Fang, Y., Goldberg, B.: Voc: A translation validator for op-
    timizing compilers. ENTCS 65(2), 2–18 (2002)


                                            23
A    Programs with ∃ in the Post-Condition

In this section, we present examples with existentially quantified formulas as
post-condtions that can be verified using our technique.

                                         // assume(∀i ∈ [0,N), A[i] > 0)
// assume(true)                          1. void Average(int A[], int N)
1. void Max(int A[], int N) {            2.   float B[N], sum = 0;
2.   int Max=A[0];                       3.   for (int i=0; i<N; i=i+1)
3.   for(i=0; i<N; i++) {                4.     sum = sum + A[i];
4.     if(Max < A[i])                    5.   for (int j=0; j<N; j=j+1)
5.       Max = A[i];                     6.     B[j] = A[j]/sum;
6.   }                                   7.
7. }                                     // assert( sum > 0 and
// assert(∃i ∈ [0,N), Max = A[i])        //   (∃i ∈ [0,N), B[i] >= 1/N) and
                                         //   (∃j ∈ [0,N), B[j] <= 1/N) )
                    (a)
                                                              (b)

                                         // assume(N>1)
// assume(N>1)
                                         1. void EvenOdd(int A[], int N) {
1. void ExtGZN(int A[], int N) {
                                         2.   for(i = 0; i<N; i++) {
2.   for(i=0; i<N; i++) {
                                         3.     if(i%2 == 0) A[i] = 0;
3.     A[i] = i;
                                         4.     else A[i] = 1;
4.   }
                                         5.   }
5. }
                                         6. }
// assert(∃i ∈ [0,N), A[i] > 0)
                                         // assert(∃i ∈ [0,N), A[i] = 1)
// assert(∃j ∈ [0,N), A[j] >= N-1)
                                         // assert(∃j ∈ [0,N), A[j] = 0)

                    (c)                                       (d)

// assume(∀i ∈ [0,N), A[i] = 1)          // assume(∀i ∈ [0,N), A[i] = N)
1. void Sum(int A[], int N) {            1. void Sum2(int A[], int N) {
2.   int B[N], sum = 0;                  2.   int B[N], sum = 0;
3.   for (int i=0; i<N; i=i+1)           3.   for (int i=0; i<N; i=i+1)
4.     sum = sum + A[i];                 4.     sum = sum + A[i];
5.   for(int j=0; j<N; j++)              5.   for(int j=0; j<N; j++)
6.     B[j] = sum;                       6.     B[j] = sum + j;
7. }                                     7. }
// assert(∃i ∈ [0,N), B[i] = N)          // assert(∃i ∈ [0,N), B[i] = i + N*N)

                    (e)                                       (f)

          Fig. 12. Examples with Existentially Quantified Post-conditions




                                        24
