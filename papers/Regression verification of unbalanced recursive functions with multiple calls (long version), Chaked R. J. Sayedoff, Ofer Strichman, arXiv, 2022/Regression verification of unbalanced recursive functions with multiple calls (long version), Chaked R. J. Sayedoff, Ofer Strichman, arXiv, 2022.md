                                             Regression verification of unbalanced recursive
                                              functions with multiple calls (long version)

                                                           Chaked R.J. Sayedoff1 and Ofer Strichman1

                                                                   IE, Technion, Haifa, Israel.
arXiv:2207.14364v1 [cs.LO] 28 Jul 2022




                                                   chaked@campus.technion.ac.il           ofers@technion.ac.il



                                               Abstract. Given two programs p1 and p2 , typically two versions of the
                                               same program, the goal of regression verification is to mark pairs of func-
                                               tions from p1 and p2 that are equivalent, given a definition of equivalence.
                                               The most common definition is that of partial equivalence, namely that
                                               the two functions emit the same output if they are fed with the same
                                               input and they both terminate. The strategy used by the Regression
                                               Verification Tool (RVT) is to progress bottom up on the call graphs of
                                               P1 , P2 , abstract those functions that were already proven to be equivalent
                                               with uninterpreted functions, turn loops into recursion, and abstract the
                                               recursive calls also with uninterpreted functions. This enables it to create
                                               verification conditions in the form of small programs that are loop- and
                                               recursion-free. This method works well for recursive functions as long as
                                               they are in sync, and typically fails otherwise. In this work we study the
                                               problem of proving equivalence when the two recursive functions are not
                                               in sync. Effectively we extend previous work that studied this problem
                                               for functions with a single recursive call site, to the general case. We
                                               also introduce a method for detecting automatically the unrolling that is
                                               necessary for making two recursive functions synchronize, when possible.
                                               We show examples of pairs of functions with multiple recursive calls that
                                               can now be proven equivalent with our method, but cannot be proven
                                               equivalent with any other automated verification system.


                                         1    Introduction: Regression Verification

                                         It is very common that changes in a program introduce new unwanted behaviors
                                         (‘bugs’). Informal methods for checking the new code include code review, testing
                                         the new program, and regression testing [30,9], a method by which the output
                                         of the new and old versions of the program are compared on a given set of test
                                         cases. Formal methods include program verification, which attempts to formally
                                         verify the correctness of the new program against user-specified assertions in the
                                         code, and formal program equivalence checking. Both problems are undecidable
                                         in general. While the general problem of proving equivalence of programs was
                                         studied for decades, mostly in the theorem proving world, e.g., [8,22,23], the
                                         specialization of this problem to closely-related programs, coined by Godlin and
                                         Strichman as regression verification [13,14,16], stirred the development of various
                                         tools and approaches, such as RVT [16], Reve [10], SymDiff [21], ARDiff [3]
and others. Regression verification suggests verifying the program against an
older version of itself rather than verifying it against a user-supplied specification
or assertions. That is, generate an automated proof of equivalence between a
program and its previous version. Although this problem is still undecidable,
for closely related programs regression verification is believed to be easier in
practice than program verification, and also spares the need to manually specify
assertions. Furthermore, it can exploit the similarity between the programs to
enable the proof and to reduce the computational complexity [16]. Admittedly
the notion of correctness is weaker compared to functional verification, since
the previous version of the code may have suffered from the same problems
as the new one, but on the other hand it might be applicable in large scale
programs, where formal functional verification is impractical, and where there
is no specification or the assertions cover only a small part of the program’s
behavior. Regression verification is relevant especially when the code has changed
but is supposed to behave the same towards its interface, e.g., as a result of
refactoring and performance tuning. There is more than one definition to what
equivalence between functions means (see six definitions in [15]), but here we
will use the most commonly used, namely that of partial equivalence [16]: f1 and
f2 are partially equivalent if given the same input, and both terminate, they
return the same output.
    The problem of program equivalence can be easily reduced to that of software
verification, by generating a new program, whose template is shown in Fig. 1 for
a case in which the compared main functions are f1 and f2 (these functions can
generally call other functions). This program executes the given programs with
the same non-deterministic input and then asserts that their output is equal
(renaming of functions may be required to avoid collisions, and global variables
need to be added to the parameters lists). Hence, any software verification tool
as well as interactive theorem provers can be used to prove equivalence between
programs. However, this route does not take any advantage of the assumed
similarity between the compared programs.


<code o f f 1 ( i ) and f 2 ( i ) >;

main ( ) {
  i = non det ( ) ;
  a s s e r t ( f 1 ( i ) == f 2 ( i ) ) ;
}
Fig. 1: A template for proving the equivalence of two functions, f1 and f2, by a reduction
to a single-program verification task. Assume that the input i is sent by value.




    Let us mention here a selected set of systems that specialize in regression
verification. RVT (Regression Verification Tool) will be described in detail in
the next section, as its strategy for proving the equivalence of recursive functions

                                             2
is the basis of the current work. Reve (stands for REgression VErification)
[10] uses weakest liberal precondition (wlp) calculus to reduce the equivalence
problem into a Horn constraint and solve it using Z3 [20] or Eldarica [25], to try
to prove the equivalence or generate a counterexample. Symdiff by Microsoft
[21] translates the given programs into an intermediate language called Boogie,
which has its own formal verifier based on Z3. ARDiff by Badihi at al. [3] is, to
the best of our knowledge, the latest implementation of a regression verification
tool and is based on symbolic execution. It also uses an abstraction/refinement
loop based on CEGAR [6] to remove parts of the code that are not relevant for
the equivalence proof. Noteworthy previous tools in this area are CLEVER [12],
MDDiff [28], IMP-S [2] and DSE [24].
    The topic of this article is a new proof rule and a corresponding (incomplete)
verification method for proving the equivalence of unbalanced recursive func-
tions, when there are multiple such calls in the top frame of the functions. The
simpler case, of a single recursive call, was dealt with in the past in [27]. We also
show a method for finding the proper unrolling of the two compared functions
so they will synchronize. Our implementation in RVT of this rule together with
the automation of the unrolling, is capable of proving equivalence of functions
that no other regression verification tool or software verification tool can prove.
    The rest of the article is structured as follows. In the next section we explain
RVT’s strategy of proving the equivalence of recursive functions. In Sec. 2.1 we
show why proving the equivalence of recursive functions that are not synchro-
nized, fail the proof rule that is used by RVT. Our contribution begins in Sec. 2.1,
where we show how to prove equivalence of unbalanced recursive functions when
there is a single path to the function call site, given a correct unrolling of the
functions that make them synchronize. In Sec. 4 we show how to automate the
process of finding that correct unrolling. In Sec. 5 we generalize the results of
Sec. 2.1 to general functions, i.e., with multiple paths, by leveraging ‘concolic
execution’ to get all the paths of the function in its top frame, to recursive
call sites. We conclude that section by describing cases that demonstrate the
incompleteness of our new proof rule.


2   An overview of RVT’s Strategy for Proving Equivalence

Given a mapping between the functions of two programs, RVT [16,17] tries to
prove the partial equivalence of each of the paired functions. It has a decomposi-
tion algorithm, which traverses bottom-up the call graphs of the two programs,
and generates each time a verification condition for proving the equivalence of a
pair of functions. If that verification condition is proven correct, then RVT marks
those functions as equivalent, and from thereon any call to those functions is re-
placed with a call to the same uninterpreted function. This algorithm becomes
more complicated in the presence of mutually recursive functions, but we will
not go into more details here. The full decomposition algorithm is described as
Alg 1 in [17].

                                         3
    In the rest of this section we explain how RVT attempts to prove the equiva-
lence of two recursive functions, rather than full programs. Furthermore, we will
assume from hereon that those functions accept a single parameter by value,
that there are no global variables, and that if those functions call other func-
tions, then those were already proven equivalent and replaced with uninterpreted
functions.
    RVT’s strategy for proving the equivalence of recursive functions is inspired
by Hoare’s inference rule for proving a given pre-post condition over a single
recursive function, that was published already in 1971 [19]:

                       {p}call proc{q} ⊢H {p}proc-body{q}
                                                                                  (1)
                                 {p}call proc{q}
Here p and q are the pre- and post-conditions. The rule says that if assuming
that the p, q relation holds for calls to procedure proc enables us to prove that
this relation holds for the procedure’s body (proc-body), then it also holds for
calls to proc. Hence, the correctness is based on an inductive argument: we use
what we want to infer as a hypothesis on the recursive call.
    [16] introduced a new inference rule for proving the equivalence of two re-
cursive functions, that is based on the same principle. Here, however, the pre-
and post-conditions are fixed: the pre-condition is the equivalence of the inputs,
and the post-condition is the equivalence of the outputs. More specifically, for
recursive functions f1 and f2 the rule is

           in[call f1] = in[call f2] → out[call f1] = out[call f2]
        ⊢ in[f1 body] = in[f2 body] → out[f1 body] = out[f2 body]
                                                                   (part-eq)      (2)
           in[call f1] = in[call f2] → out[call f1] = out[call f2]

This rule states that if assuming that the calls to f1 and f2 are partially-equivalent
(i.e., same inputs result in the same outputs) enables us to prove that f1 and
f2 bodies are partially-equivalent, then f1 and f2 are partially equivalent. RVT
checks the premise of (2) by replacing the recursive calls in f1, f2 with calls to
the same uninterrupted function (U F s). An uninterpreted function, by defini-
tion, is congruent and over-approximates the substituted function. Hence, this
substitution fulfills the first part of the premise. We define related calls as:

Definition 1 (Related Calls). Recursive calls to f1 and f2 are called related
if they are made with the same parameters.

The uninterpreted functions that replace the recursive calls emit the same (non-
deterministic) value on related calls, which is many time sufficient for proving
equivalence.

Example 1. Consider the two functions in Fig. 2. The verification condition that
RVT generates uses the template of Fig. 1, where the two functions in Fig. 2
are replaced with those that appear in Fig. 3. A ‘pass’ result on this condition
implies that the premise of (2) is true.

                                          4
                                            i n t sum2 ( i n t n ) {
i n t sum1 ( i n t n ) {                         int r e s ;
     i f ( n <= 1 ) return n ;                   i f ( n <= 1 ) return n ;
     return n + sum1 ( n −1);                    r e s = sum2 ( n −1);
}                                                return r e s + n ;
                                            }
                      Fig. 2: Two equivalent recursive functions.



                                            i n t sum2 ( i n t n ) {
i n t sum1 ( i n t n ) {                         int r e s ;
     i f ( n <= 1 ) return n ;                   i f ( n <= 1 ) return n ;
     return n + UF( n −1);                       r e s = UF( n −1);
}                                                return r e s + n ;
                                            }
Fig. 3: The functions of Fig. 2, after replacing the recursive calls with the same unin-
terpreted function ‘UF’
                                            .



    As a preprocessing step, RVT replaces all loops with calls to new recursive
functions. Hence after replacing all the recursive calls with uninterpreted func-
tions, the program in Fig. 1 is flat, and hence its verification is decidable. RVT
calls CBMC [7], a software bounded model checker, to verify this program.

2.1   Proving equivalence of functions with Unbalanced Recursion
Example 1 listed functions that are in sync, which we formally define as follows.


Definition 2 (Sync). Let f1 and f2 be two recursive functions. f1 and f2 are
said to be in sync if for every input they are called recursively at the top frame
with the same sets of parameters, or not called at all.
In such cases (part-eq) is typically very successful in proving equivalence. How-
ever, it turns out that once the functions are not in sync, it typically fails. In such
a case the uninterpreted functions do not necessarily return the same value, be-
cause they are called with different parameters, and this typically fails the proof
of equivalence. Moreover, if there exists an input for which f1 invokes the base
case whereas f2 makes a recursive call, (part-eq) fails as well, because the re-
cursive call is replaced with a UF which is not matched on the other side, and
that UF returns a non-deterministic value. As mentioned in the introduction, a
past publication [27] attempted to deal with this problem, but only considered
a simple case in which there is a single recursive call in the function, and also
relied on a manual input of the unrolling that is necessary in order to synchro-
nize the two functions. The rest of this article is dedicated to a proof rule and

                                           5
corresponding strategy that in some cases are able to solve the general case in
which there are multiple calls and some of them may be conditioned, and do so
automatically.


3   Equivalence of single-path unbalanced recursions: the
    rule (path-part-eq)



                                             int f2 ( int n){
int f1 ( int n ){
                                                i f ( n < 1 ) return 0 ;
   i f ( n < 1 ) return 0 ;
                                                i f ( n <= 2 ) return 1 ;
   i f ( n <= 2 ) return 1 ;
                                                return f 2 ( n−2) + f 2 ( n−2)
   return f 1 ( n−1) + f 1 ( n −2);
                                                                  + f 2 ( n−3) ;
}
                                             }
         Fig. 4: Two equivalent implementations of the Fibonacci sequence.




    In this section we will consider pairs of recursive functions f1, f2 with the
following properties:

 – the control flow of f1 and f2 contains a single path with recursive calls (in
   Sec.5 we will remove this requirement)
 – f1 and f2 are not in sync, and
 – there exists an unrolling of f1, f2 that synchronizes them.

   Let us demonstrate a case in which two input functions f1 and f2, which are
not in sync, can be synchronized with unrolling.
Example 2. Consider the pair f1, f2 in Fig 4. We will use them as a running
example in this article. These functions are not in sync: for example, with input
n = 4, f1 makes recursive calls with parameters 3, 2 whereas f2 makes recursive
calls with parameters 2, 1. Hence, e.g., f1’s recursive call with the parameter 3
does not have a related call (see Def. 1) by f2, which fails a proof based on the
technique that was described in Sec. 2. However, after unrolling the call f1(n− 1)
once, each recursive call has a related call, as depicted in Fig. 5.            ⊓
                                                                                ⊔
    More formally, we need to find an unrolling of the two functions with the
following property.
Definition 3 (Sync-Unrolling). An unrolling su of two recursive functions f1
and f2 is called Sync-Unrolling if after applying it the sets of recursive calls on
both sides are the same.
Going back to Example 2, the unrolling that we applied is indeed a sync-
unrolling, because both functions now have the set of parameters {n − 2, n − 3}.

                                        6
    Since the recursive calls in the functions can be conditioned, the correct
unrolling may depend on the input value, and in such cases it is not likely that
there is a single unrolling which is a sync-unrolling for all inputs. This is the
reason that we decompose the proof to the granularity of paths in the top frame
of the functions, and the reason that in this section we only consider a single
path.
    Also, clearly such an unrolling does not necessarily exist even if the two
functions are equivalent. For example, if f1 sums an array of numbers from the
beginning to the end, and f2 in the reverse order, no unrolling can synchronize
these two functions.



                           f1(n)
                                                                                   f2(n)


             f1 (n − 1)                 f1(n − 2)
                                                            f2(n − 2)                         f2(n − 3)

                                                                                  f2(n − 2)
 f1(n − 2)                f1(n − 3)


Fig. 5: The call graphs of f1 and f2 after unrolling f1(n − 1) once. Related calls are
colored the same.



    We observe that the ‘pruned’ call graph corresponding to the sync-unrolling
of a function has a specific structure. Let c(f ) denote the number of function
calls in the path of f that is being considered. The root of the call graph is f ,
and the number of branches that each node has is either c(f ) (if we choose to
expand it), or 0 (if we choose not to expand it). Reconsidering Example 2, f1
has two recursive calls (c(f1) = 2) in its path, and indeed each node has either
2 or 0 branches. In Sec. 4 we will describe a method for finding synchronization
unrolling instructions automatically, when at all possible.
    Let su(f1, f2) denote the sync-unrolling instructions of f1 and f2, which we
will abbreviate to su from hereon. Correspondingly, f1su , f2su denote f1, f2 after
being unrolled according to su. If su exists and we can find it, then our proof
strategy is based on splitting the input domain to two:

 – The base-case domain: all the inputs that reach a base case on at least one
   of f1su or f2su .
 – The step-case domain: the complement of the base-case domain.

   We then use the following proof rule:
                            su
    path-base-equiv (f1          , f2su )   path-step-equiv (f1
                                                                  su
                                                                       , f2su )
                                                                                  (path-part-eq)     (3)
                           partial-equiv(f1, f2)


                                                    7
The premises (path-base-equiv) and (path-step-equiv) prove equivalence for the
base-case and step-case domains, respectively.
Proposition 1. Rule (path-part-eq) is sound.
Proof. The whole input domain is covered by definition of the step case as a com-
plement of the base case. Hence if each of (path-base-equiv) and (path-step-equiv)
is a sound test of equivalence for its designated inputs, then the rule is sound.
After presenting how we test those premises below, we will prove in Proposi-
tion 2 that those methods are indeed sound as well.                             ⊓
                                                                                ⊔
    For the step case we use the original method of RVT as described in Sec. 2,
namely we replace all recursive calls with UFs. Note that since the input func-
tions are possibly unrolled, only the actual recursive calls are replaced, e.g., only
the calls at the leaves in Fig. 5.
    For the base-case we must use a different strategy, because the above strategy
would likely fail in cases where there exists an input that drives f1su to return
on a base case, whereas it drives f2su to call an uninterpreted function. As an
example, consider the input n = 3 in Fig. 4. In f1su it returns on the base cases,
whereas in f2su it returns on a recursive call turned into a call to a UF. That
called UF has no related call in f1su and is hence likely to fail the proof.
    Our strategy for handling the base-case is thus different: we maintain the
recursive calls in f1su , f2su (that is, we do not replace them with UFs), and use
symbolic execution to attempt to prove the equivalence. Since we restrict the
runs to the base-case domain, it is likely that both sides will converge after a
few iterations, which will enable the proof. In the next subsection we describe
this method in more detail.
Proposition 2. The tests of (path-base-equiv) and (path-step-equiv) are sound.
Proof. Both rules are checked based on the reduction presented in Fig. 1, of
equivalence to verification, a reduction that was used in most past publications
about program equivalence, e.g., [13,14], and its soundness is rather obvious.
The fact that we check unrolled recursions cannot hinder soundness, because
unrolling f1, f2 into f1su , f2su does not change the semantics of the functions.
After unrolling, we use symbolic execution in the case of the base-case, which is
a well-known sound technique, and the rule (part-eq) (see (2)), as described in
the previous section, that was proven to be sound in [13].                     ⊓
                                                                               ⊔

3.1   (path-base-equiv) - Proving equivalence in the base-case domain
Algorithm 1 describes our process for proving (path-base-equiv) (a note on ty-
pography from hereon: when we refer to one of f1, f2 we write fi for i ∈ {1, 2}.
We will avoid repeating the range i ∈ {1, 2}). Its parameters are the compared
functions and the sync-unrolling su information: a sequence of unrolling instruc-
tions corresponding to a pruned call graph as explained in the previous section.
The algorithm begins by applying these unrolling instructions, after which the
recursive calls at the leaves are in sync.

                                         8
Algorithm 1 Checking (path-base-equiv).
1: function ProvePathBaseEquiv( Programs f1, f2, sync-unrolling su)
2:    for i ∈ {1, 2} do
3:       f¯i = ApplyUnrolling(fi ,su)
4:       bcpci = GetBaseCasePrecondition(f¯i )
5:    P = CreateVerificationProgram(f1, ¯ f2)
                                            ¯
6:    P = AddAssumption(P , bcpc1 ∨ bcpc2 )
7:    P = AddEquivalenceAssertion(P )
8:    return SymbolicExecution(P )




      It then infers a weakest precondition predicate for the base-case domain of
f¯i , denoted bcpci . Specifically GetBaseCasePrecondition(f ) finds this pred-
icate in two steps:
1. In the first step it finds a condition on the input parameters, for the base-case
   to be taken in the top frame of f . This is done by (1) replacing all recursive
   calls with calls to a function with a single assume(false) statement, and (2)
   invoking Concolic Execution [26] (specifically, PathCrawler [29]), to generate
   a predicate over the input parameters that represents the feasible paths,
   namely the base-cases. As an example, in Fig. 6 we present the generated
   program for f1 from Fig 4. Note that since this is a flat program (no loops
   and recursions) by construction, this step is guaranteed to terminate with a
   correct answer. Let ρi denote this predicate for function fi . For f1 in Fig. 6
   we have ρ1 = n < 3.
2. In the second step, it computes the weakest precondition predicates bcpci for
   the base-case domain of the unrolled function. It declares a global variable
   bc f lag (initially set to 0) and use ρi in order to set it to 1 if the base case is
   taken in one of the frames. It then adds an ‘assume(bc f lag)’ statement after
   calling fi , in order to restrict the executions to paths that return on at least
   one base case. The recursive calls are replaced with a call to a function ret
   (short for ‘return’) with a single return statement. Using Concolic execution
   again, it computes bcpci .
   An example of the second step, referring to the same f1 of Fig 4, is presented
   in Fig 7. Note how ρ1 = n < 3 is used to set the base-case flag in each of
   the frames (f1, f1 ). The base-case predicate bcpc1 computed in this step is
   n ≤ 3: indeed, in this range the unrolled program returns on at least one
   base case.
    RVT calls CreateVerificationProgram to generate a verification con-
dition following the pattern in Fig. 1 while restricting the inputs, in Line 6, by
adding assume(bcpc1 ∨ bcpc2 ) at the beginning of P . Finally, it calls a symbolic
execution engine to prove the equivalence. By the very fact that we invoke it on
a program with recursion, this makes our method incomplete. While one would
expect that when we restrict the executions only to inputs that drive the func-
tions to their base-cases, symbolic execution will be successful in a relatively

                                          9
int f1 ( int n ) {
          i f ( n < 1 ) return 0 ;
                                                int block ( int n ){
          i f ( n <= 2 ) return 1 ;
                                                    assume ( f a l s e ) ;
          return b l o c k ( n−1) +
                                                }
                      b l o c k ( n −2);
}
Fig. 6: The program generated in the first step of GetBaseCasePrecondition and
sent to PathCrawler in order to compute ρi .




b c f l a g= 0 ;
                                                int f 1 ( int n ){
i n t main ( i n t n ) {
                                                   i f ( n < 3) b c f l a g = 1 ;
     f1 (n ) ;
                                                   i f ( n < 1 ) return 0 ;
     assume ( b c f l a g ) ;
                                                   i f ( n <= 2 ) return 1 ;
}
                                                   return r e t ( n−1) + r e t ( n −2);
                                                }
int f1 ( int n ){
   i f ( n < 3) b c f l a g = 1 ;
                                                int r e t ( int n ){
   i f ( n < 1 ) return 0 ;
                                                    return 0 ;
   i f ( n <= 2 ) return 1 ;
                                                }
   return f 1 ( n−1) + r e t ( n −2);
}
Fig. 7: The program generated in the second step of GetBaseCasePrecondition in
order to compute the base-case precondition bcpc.




                                           10
i n t p1 ( i n t n , i n t m) {            i n t p2 ( i n t n , i n t m) {
i f (m< 1 | | n < 1 | |m > n )             i f (m< 1 | | n < 1 | |m > n )
    return 0 ;                                 return 0 ;
i f (m==1||n==1||m == n )                  i f (m==1|| n==1||m == n )
    return 1 ;                                 return 1 ;
return p1 ( n − 1 , m − 1 )                return p2 ( n − 1 , m − 1 )
   + p1 ( n −1, m) ;                          + p2 ( n − 2 , m − 1 )
}                                             + p2 ( n − 2 , m) ;
                                           }




                 Fig. 8: Equivalent implementations of the Pascal’s triangle.



i = non det ( )                                    i = non det ( )
assume ( bcpc1 ∨ bcpc2 )                           assume ( ! ( bcpc1 ∨ bcpc2 ) )
r e s 1 = f1  ¯(i)                                 r e s 1 = f1  ˆ(i)
r e s 2 = f2  ¯(i)                                 r e s 2 = f2  ˆ(i)
a s s e r t ( r e s 1==r e s 2 )                   a s s e r t ( r e s 1==r e s 2 )
                       (a)                                             (b)
Fig. 9: A verification program to prove conditional equivalence for (a) the base cases,
and (b) the step case. The difference between f¯ and fˆ is that in the former recursive
calls are maintained, whereas in the latter they are replaced with UFs.




short amount of time, the following example shows that this is not always the
case.

Example 3. Consider the pair of functions in Fig. 8. In this example, the base
case contains a value of m that is dependent on n. Specifically, if m=n-1, the call
to p1(n-1,m) terminates in its base case since the condition m==n is invoked.
On the other hand the other recursive call, p1(n - 1, m - 1), is repeatedly
called until one of the lower bounds of n or m are reached, a process that is likely
to fail symbolic execution for large values of n and m. Indeed KLEE times out
when trying to prove the equivalence of this base-case.

    A schematic depiction of P is shown in Fig. 9(a). If the verification of P in
line 8 is successful, then RVT deems the base-case equivalence of the pair as
correct.


Comparing methods to prove the base-cases equivalence We choose to
use Symbolic Execution to prove the base cases equivalence due to complex-
ity. We will compare here the complexity of two alternatives. The first is using

                                             11
CBMC and increasing the unrolling factor until the verification is successful or
timeout is reached. The second is using Symbolic Execution. CBMC invokes
the SAT solver once after traversing the whole call graph, which is a tree as we
unroll the recursions, while symbolic execution runs in a DFS style on the call
graph and calls the SAT solver every time it reaches a leaf.
    Assume that we try to prove the said equivalence of two programs P1 and
P2 and that at least one of them contains C, C > 1, recursive calls in its body
that are executed on the same trace. Without loss of generality, assume that
the equivalence is proved when P1 is unrolled k times, for some k ≥ 1. If we
were to use CBMC, the unrolling would create a program that is translated to a
formula that represents C k calls. The call graphs in Fig. 5 illustrate this point:
the number of nodes in such a tree is O(C k ). The encoding to a propositional
formula creates a different set of variables for every call, and thus the number
of variables in this formula is proportional to C k . CBMC calls a SAT solver
to solve this formula, which in itself is exponential in the number of variables.
Hence the complexity for the verification task is exponential in C k , thus double
exponential in k.
    On the other hand, using Symbolic Execution, the size of the formula is
proportional to k, as it represents only a single trace. Symbolic Execution goes
through all paths up to a given bound, and the number of paths is worst-case
exponential (this is the known “path explosion” problem [1]). Each of these trace
verification tasks is a formula handed to a SAT solver and therefore has an expo-
nential run-time bound. That means that the overall complexity of this method
is exponential squared in the program’s size. Hence using symbolic execution for
this task has better worst-case complexity.

3.2   (path-step-equiv) - Proving equivalence in the step-case domain
The step-case proof covers the inputs that are not contained in the base-case


Algorithm 2 A sound algorithm to prove equivalence of programs for their base
cases.
1: function ProvePathStepEquiv( Programs f1, f2, sync-unrolling su, precondition
   ebcp)
2:     ˆ = ApplyUnrolling(f1,su)
      f1
3:     ˆ = ApplyUnrolling(f2,su)
      f2
4:                                    ˆ f2)
      P = CreateVerificationProgram(f1,  ˆ
5:    P = ReplaceRecursionsWithUFs(P )
6:    P = AddAssumption(P, !ebcp)
7:    P = AddEquivalenceAssertion(P )
8:    return CBMC(P )



domain. Algorithm 2 describes RVT’s process for this proof. It is different than
ProvePathBaseEquiv (Fig. 1) in that it receives as input the base-case pre-
condition that is generated in algorithm 1 and is aliased here as ebcp. Based on

                                        12
int f 1 ( int n ){
   i f ( n < 1 ) return 0 ;
   i f ( n <= 2 ) return 1 ;
                                                  int f2 ( int n){
   return f 1 ( n−1) + f 1 ( n −2);
                                                      i f ( n < 1 ) return 0 ;
 }
                                                      i f ( n <= 2 ) return 1 ;
int f1 ( int n ){
                                                      return f 2 ( n−2) + f 2 ( n−2)
   i f ( n < 1 ) return 0 ;
                                                                        + f 2 ( n −3);
   i f ( n <= 2 ) return 1 ;
                                                    }
   return f 1 ( n−1) + f 1 ( n −2);
 }
      Fig. 10: Unrolling once the call to f1(n − 1), to achieve synchronization.




the definition of the step-case domain (see Sec. 3), it restricts the input space
to its negation. Another difference is that ReplaceRecursionsWithUFs re-
places all the recursive calls (those that are left after applying su) with UFs.
         ˆ and f2
    Now f1       ˆ are loop-and recursion-free, and can be verified by any software
(bounded or unbounded) model-checker. In our case we chose to work with
CBMC, which among other things has native support of uninterpreted functions,
a useful feature in our case. P is presented in Fig. 9 (b). If CBMC validates P
then the pair of input functions is declared by RVT to be step-case equivalent.


4   Automatic synchronization of recursive functions

The motivation for automating the process of finding sync-unrolling is clear.
Both in [27] and [10], who considered the problem of unbalanced recursive func-
tions, supplied this data manually.
    We already saw in Example 2 a pair of functions for which there exist sync-
unrolling (see Fig. 5). The unrolled code that RVT generates for that example
appears in Fig. 10.
    Our method for finding sync-unrolling, when possible, is described in algo-
rithm 3. It creates a C program with an assertion, such that a counterexample
represents an unrolling number per function call site, and those numbers define
a sync-unrolling. We exploit CBMC’s non det() instruction, corresponding to a
non-deterministic choice, to let the solver decide whether to unroll or not in each
call site. The program records the call parameters in cases in which it decides
not to unroll — these will be the leaves of the call graph, where we will call the
uninterpreted functions. At the end of the generated program we assert that the
set of recorded parameters of the two programs is different. Hence, from a coun-
terexample that CBMC finds, we can extract the sync-unrolling, together with
a particular input to the functions. A single input is enough since we consider a
single path (that has recursive calls) at a time.
    The main functions of the algorithm are:

                                         13
 – AddDepthAndCallsTracking(f ) adds the auxiliary infrastructure needed
   for recording the unrolling choices at each recursive call site. Specifically at
   each call site that it chooses to stop unrolling (i.e., the leaves), it records the
   depth D and the index of the call site Site (i.e., each recursive call site is
   given a unique index). This data is later extracted from the counterexample
   in order to produce the sync-unrolling.
 – GetNaturalBaseCasePrecondition is called. It produces ρi as described
   in the first step of GetBaseCasePrecondition in section 3.1.
 – AddAssumption(f, p) assumes the precondition p at the beginning of f .
 – ApplyNonDeterministicRecording(f ) adds a non-deterministic condi-
   tion. A ‘true’ choice corresponds to no-more unrolling (i.e,. the leaves of the
   pruned call graph). In that case the input of the current iteration is recorded
   and the function returns.
 – CreateSyncUnrollingProgram(f1, f2) generates a new program based
   on the template of 1. After the calls to f1 and f2, it asserts that the sets of
   recorded inputs from ApplyNonDeterministicRecording that contain
   more than one recording (i.e., went through at least one recursive call) are
   different.
 – GenerateSyncUnrolling(f1, f2, ce) extracts the values of D and Site
   from the counterexample in order to generate the sync-unrolling.




Algorithm 3 An algorithm for finding a synchronization unrolling, if it exists.
 1: function FindSyncUnrolling(Loops Free Programs f1, f2)
 2:    for i ∈ {1, 2} do
 3:       fi = AddDepthAndCallsTracking(fi)
 4:       ρi = GetNaturalBaseCasePrecondition(fi)
 5:       fi = AddAssumption(fi , !ρi )
 6:       fi = ApplyNonDeterministicRecording(fi)
 7:    P = CreateSyncUnrollingProgram(f1, f2)
 8:    for unwinding factor uw increasing from 1 up until a predefined timeout do
 9:       Punwinded = Unwind(P, uw)
10:        if CBMC(Punwinded ) results with a counterexample ce then
11:            return GenerateSyncUnrolling(f1, f2, ce)




Example 4. Reconsider the functions in Fig. 4. The program P that is generated
in line 7 is shown in Fig. 11.
    After unwinding P enough times CBMC will find a counterexample for
any n bigger than 2, from which GenerateSyncUnrolling derives the sync-
unrolling shown in Fig. 5.                                                   ⊓
                                                                             ⊔

Example 5. Consider the pair of functions in Fig. 12. As we have seen, the steps
are equivalent for n > 3, m2’s base case handles n = 2 and thus this pair is

                                        14
i n t f 1 ( i n t n , i n t D, i n t S i t e ) {   i n t f 2 ( i n t n , i n t D, i n t S i t e ) {
      assume ( n > 2 ) ;                                 assume ( n > 2 ) ;
      i f ( non det ( ) ) {                              i f ( non det ( ) ) {
              Leav es1 [ S i z e 1 ++] = n ;                     Leav es2 [ S i z e 2 ++] = n ;
              return −1;                                         return −1;
      }                                                  }
      i f ( n < 1 ) return 0 ;                           i f ( n < 1 ) return 0 ;
      i f ( n <= 2 ) return 1 ;                          i f ( n <= 2 ) return 1 ;
      return f 1 ( n−1 ,D+1 ,0) +                        return f 2 ( n−2 ,D+1 ,0) +
                  f 1 ( n−2 ,D+ 1 , 1 ) ;                f 2 ( n−2 ,D+1 ,1) + f 2 ( n−3 ,D+1 ,2) ;
}                                                  }

                   main ( ) {
                     i = non det ( ) ;
                     Leav es1 = Leav es2 = { } ;
                     Size1 = Size2 = 0;
                     f1 ( i ,0 , −1);
                     f2 ( i ,0 , −1);
                     assume ( S i z e 1 > 1 && S i z e 2 > 1 ) ;
                     a s s e r t ( Leav es1 != Leav es2 ) ; // s e t compari son
                   }
Fig. 11: The program generated in line 7 of Algorithm 3. The capitalized variables are
not part of the original functions f1, f2. Leaves and Size are global.




equivalent. For the case where mode is true, RVT generates a sync-unrolling
that unrolls the call m1(n-1,!flag) once and blocks everything else on both
sides. When trying to prove the related step case, CBMC fails. This happens
because in the unrolled frame the polarity of flag is negated to the polarity of
mode in the related calls due to the odd number of unrolling, and as a consequence
the generated UFs are unrelated and fails the proof, even though flag does not
affect m1’s result.


Example 6. In this example we will show a case in which the method we de-
scribed fails. Consider the pair of functions in Fig. 13. In this example, the
values in t2 are calculated in advance, and are used differently according to the
parity of n. The problem occurs when RVT tries to generate a sync unrolling
while one of the recursive calls is redundant (i.e., its result is not used). Algo-
rithm 3 aims to find a value for which all the recursive calls have related calls.
To achieve that, each recursive call on each side is either recorded, unrolled or is
not reached. The redundant calls in t2 are not on a branched path and therefore
must be executed; it cannot be recorded as there is no equivalent recording for
them in t1 and unrolling them will yield more redundant calls. Whenever RVT
fails to generate a sync unrolling, it does not unroll at all, and this fails the proof
with this pair.

                                             15
i n t m1( i n t n , i n t f l a g ) {          i n t m2( i n t n , i n t mode ) {
i f ( n < 1 ) return 0 ;                       i f ( n < 1 ) return 0 ;
i f ( n == 1 ) return 1 ;                      i f ( n == 1 | | n == 2 )
return m1( n − 1 , ! f l a g )                                 return 1 ;
            + m1( n − 2 , ! f l a g ) ;        int r e s u l t s = 0 ;
}                                              i f ( mode )
                                                   r e s u l t s = m2( n − 2 , ! mode )
                                                              + m2( n − 2 , ! mode )
                                                              + m2( n − 3 , ! mode ) ;
                                               i f ( ! mode )
                                                   r e s u l t s = m2( n − 1 , ! mode )
                                                              + m2( n − 2 , ! mode ) ;
                                               return r e s u l t s ;
                                               }
Fig. 12: Equivalent implementations of Fibonacci. m2 alternates between two paths in
the control flow.




5   Equivalence of general unbalanced recursions: the rule
    (full-part-eq)




We now generalize the solution of Sec. 3.1 to general unbalanced recursive func-
tions, i.e., with multiple paths in which a recursive call is made. As explained
right after Def. 3, the correct sync-unrolling may depend on the input, if it leads
to different paths. The recursions in Fig. 14 demonstrate this fact.

    Indeed, for e.g., n = 2 and n = 3 the sync-unrolling is clearly different ow-
ing to the condition that checks the parity of n. Hence, we need to decompose
the proof, by partitioning the domain such that each partition induces a single
path in the program. For each such partition, we will use the method suggested
in the previous two sections. Formally, let CF (f ) be the set of all the paths
in the control flow of the top frame of a function f . Let inB (f ) be the set of
inputs that drive f to its base case, i.e., without a recursive (or mutual re-
cursive) calls. Let in(p) denote all the inputs that their traces go through the
path p, f |a denote the function f with an assumption a restricting its inputs,
and part(f1, f2, p) = inB (f1) ∪ inB (f2) ∪ in(p). ‘su’, as in Sec. 3, is the sync-
unrolling information. This time, those instructions are adjusted to the new

                                          16
int t1 ( int n ) {                     int t2 ( int n) {
  i f ( n < 1 ) return 0 ;               i f ( n < 1 ) return 0 ;
  i f ( n == 1 ) return 1 ;              i f ( n == 1 | | n == 2 ) return 1 ;
  return t 1 ( n − 1 )                   int r e s u l t s = 0 ;
     + t1 (n − 2 ) ;                     i n t r 1 = t 2 ( n −1);
}                                        i n t r 2 = t 2 ( n −2);
                                         i n t r 3 = t 2 ( n −3);
                                         i f ( n % 2 == 0 )
                                             r e s u l t s = r2 + r2 + r3 ;
                                         else r e s u l t s = r1 + r2 ;
                                         return r e s u l t s ;
                                       }
Fig. 13: Equivalent implementations of Fibonacci. t2 chooses between two paths de-
pending on the input, but nevertheless makes the same recursive calls.




i n t h1 ( i n t n ) {                     i n t h2 ( i n t n ) {
     i f ( n < 1 ) return 0 ;                   i f ( n < 1 ) return 0 ;
     i f ( n == 1 ) return 1 ;                  i f ( n == 1 ) return 1 ;
     return h1 ( n−1) + h1 ( n −2);             i f ( n & 1 == 0 )
}                                                  return h2 ( n−1) + h2 ( n −2);
                                                i f ( n & 1 == 1 )
                                                   return h2 ( n−2) + h2 ( n−2)
                                                                       + h2 ( n −3);
                                           }
Fig. 14: Equivalent implementations of Fibonacci, where h2 has a conditioned step. The
condition n&1 checks the parity of n.




                                         17
restricted functions fi |part(f1,f2,pi ) . Based on this notation, we define the proof
rule (full-part-eq):

       ^         path-base-equiv (f1|su                  su
                                     part(f1,f2,p ) , f2|part(f1,f2,p ) ) ∧
                                                   1                2

                      path-step-equiv (f1|su                  su
                                          part(f1,f2,p ) , f2|part(f1,f2,p ) )
  p1 ∈ CF (f1)                                          1                 2


  p2 ∈ CF (f2)
                                                                                 (full-part-eq)
                           partial-equiv(f1, f2)
                                                                           (4)
Note that the programs provided to (path-base-equiv) and (path-step-equiv) are
the same, and hence we can prove these premises as described in the previous
sections without a change.
Proposition 3. (full-part-eq) is sound.

Proof. (full-part-eq) covers all the possible pairs of paths. For each such pair it
checks the same premise as in (path-part-eq) , the soundness of which was proved
in Proposition 1.                                                                ⊓
                                                                                 ⊔



Algorithm 4 Proving equivalence of general (i.e., multi-path) unbalanced re-
cursions.
1: function ProvePartEq( Functions f1, f2)
2:    AreEquivalent = TRUE
3:    for i ∈ {1, 2} do
4:       P athsP redicatesi = GetAllPaths(fi )
5:       ppf i   = GetNaturalBaseCasePrecondition(fi)
             base

 6:    for every pair (pp1 , pp2 ) in P athsP redicates1 × P athsP redicates2 do
 7:       if pp1 ∩ pp2 = ∅ then continue
 8:       f1 = AddAssumption(f1, pp1 ∨ ppf 1 )
                                                 base
 9:       f2 = AddAssumption(f2, pp2 ∨ ppf 2 )
                                                 base
10:        su = FindSyncUnrolling(f1,f2)
11:        BaseCaseEquiv = ProvePathBaseEquiv(f1, f2, su)
12:        StepCaseEquiv = ProvePathStepEquiv(f1, f2, su, bcpc1 ∨ bcpc2 )
13:        if !( BaseCaseEquiv ∧ StepCaseEquiv) then return FALSE;
14:    return TRUE;



    We check the premise of (full-part-eq) with Algorithm 4. It partitions the
input domain of the two input functions, such that each partition corresponds
to a separate path in their flattened version, as explained above. It then tries to
prove the equivalence of each pair of such partitions. We now describe the main
elements of the algorithm:
 – In line 4, GetAllPaths(f ) uses concolic execution to get all the paths
   in the top frame of f . To that end, GetAllPaths flattens f by replacing

                                              18
                  i = non det ( )
                  assume (pp1 (i) && (pp2 (i) )
                  assert ( false )
Fig. 15: A verification task for checking the emptiness of an intersection of two input
domains, which are defined by the path predicates pp1 and pp2 over an input argument
i.




   recursive calls with calls to ret, which is a function containing a single return
   statement and nothing else as described in Fig. 7, and calls PathCrawler [29].
   PathCrawler generates a list of path conditions for all the possible paths in
   that flattened version of f .
 – In line 5 GetNaturalBaseCasePrecondition is called (see Sec. 4).
 – In line 7 we screen out infeasible paths, as a performance optimization. It
   is based on the observation that some of the paths predicates combinations
   in P athsP redicates1 × P athsP redicates2 are not feasible. RVT checks
   this by creating a verification task as presented in Fig. 15. In the generated
   program, we assume both path predicates on the same non deterministic
   inputs. Sending this task to a model checker results in two option: 1. If the
   verification is successful, that means the conjunctions of the assumptions
   is unsatisfiable and thus the intersection of pp1 and pp2 is empty. 2. If the
   verification fails, that means that the paths in question are feasible as the
   verification reaches the false assertion.
 – As of line 8, for each feasible pair of paths predicates, RVT treats the pro-
   grams as though they had a single step by restricting the inputs and tries
   to prove them with ProvePathBaseEquiv and ProvePathStepEquiv
   from sections 3.1 and 3.2, respectively. AddAssumption in those algorithms
   deviates from how is was originally described. Rather than just adding the
   assumptions, it replaces the assumptions added in algorithm 4 in lines 8
   and 9. Otherwise, when blocking the base cases for example, we will assume
   contradicting assumptions and the verification task would be vacuously true.
   The formula bcpc1 ∨ bcpc2 in line 12 is computed as part of ProvePath-
   BaseEquiv in the line above.
 – In line 13, we return False (i.e., we failed proving that f1 and f2 are equiva-
   lent), if we failed proving equivalence for one of the pairs.



6    Summary

(full-part-eq) can prove a range of use cases beyond what was demonstrated here
— see RVT’s website: https://rvt.iem.technion.ac.il for more examples. To the
best of our knowledge, based on experiments, RVT is the only tool that can prove
the equivalence of programs with unsynchronized multiple recursive calls such as
the pairs in Figs. 4 and 14. Symbolic execution based tools such as CLEVER [12]

                                          19
and ARDiff [3] cannot handle unbounded loops and recursions. REVE [11] fails
to prove those examples. We also created a simple verification task based on the
reduction in Fig. 1, and experimented with the state-of-the-art software model
checkers that performed best in the 2022 software verification competition SV-
COMP 2022 [4]: CPAchecker [5] and Ultimate Automizer [18] failed to
prove these examples.


References

 1. Saswat Anand, Patrice Godefroid, and Nikolai Tillmann. Demand-driven com-
    positional symbolic execution. In C. R. Ramakrishnan and Jakob Rehof, editors,
    Tools and Algorithms for the Construction and Analysis of Systems, pages 367–381,
    Berlin, Heidelberg, 2008. Springer Berlin Heidelberg.
 2. John Backes, Suzette Person, Neha Rungta, and Oksana Tkachuk. Regression
    verification using impact summaries. volume 7976, 07 2013.
 3. Sahar Badihi, Faridah Akinotcho, Yi Li, and Julia Rubin. Ardiff: Scaling pro-
    gram equivalence checking via iterative abstraction and refinement of common
    code. In Proceedings of the 28th ACM Joint Meeting on European Software Engi-
    neering Conference and Symposium on the Foundations of Software Engineering,
    ESEC/FSE 2020, page 13–24, New York, NY, USA, 2020. Association for Com-
    puting Machinery.
 4. Dirk Beyer. Progress on software verification: Sv-comp 2022. In Dana Fisman and
    Grigore Rosu, editors, Tools and Algorithms for the Construction and Analysis of
    Systems, pages 375–402, Cham, 2022. Springer International Publishing.
 5. Dirk Beyer and M. Erkan Keremoglu. Cpachecker: A tool for configurable software
    verification. In Ganesh Gopalakrishnan and Shaz Qadeer, editors, Computer Aided
    Verification, pages 184–190, Berlin, Heidelberg, 2011. Springer Berlin Heidelberg.
 6. Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith.
    Counterexample-guided abstraction refinement. In E. Allen Emerson and Ar-
    avinda Prasad Sistla, editors, Computer Aided Verification, pages 154–169, Berlin,
    Heidelberg, 2000. Springer Berlin Heidelberg.
 7. Edmund Clarke, Daniel Kroening, and Flavio Lerda. A tool for checking ANSI-C
    programs. In Kurt Jensen and Andreas Podelski, editors, Tools and Algorithms for
    the Construction and Analysis of Systems (TACAS 2004), volume 2988 of Lecture
    Notes in Computer Science, pages 168–176. Springer, 2004.
 8. Sorin Craciunescu. Proving the equivalence of clp programs. In ICLP, pages 287–
    301, 2002.
 9. Dustin E. Effective Software Testing: 50 SpecificWays to Improve Your Testing.
    Addison-Wesley Professional.
10. Dennis Felsing, Sarah Grebing, Vladimir Klebanov, Philipp Rümmer, and Mattias
    Ulbrich. Automating regression verification. In ACM/IEEE International Confer-
    ence on Automated Software Engineering, ASE ’14, Vasteras, Sweden - September
    15 - 19, 2014, pages 349–360, 2014.
11. Dennis Felsing, Sarah Grebing, Vladimir Klebanov, Philipp Rümmer, and Mattias
    Ulbrich. Automating regression verification. In 29th IEEE/ACM International
    Conference on Automated Software Engineering (ASE 2014), ASE ’14, pages 349–
    360. ACM, September 2014.


                                         20
12. Nick Feng, Federico Mora, Vincent Hui, and Marsha Chechik. Scaling client-specific
    equivalence checking via impact boundary search. In 2020 35th IEEE/ACM Inter-
    national Conference on Automated Software Engineering (ASE), pages 734–745,
    2020.
13. Benny Godlin and Ofer Strichman. An inference rule for the equivalence of proce-
    dures. (Submitted to Acta-Informatica).
14. Benny Godlin and Ofer Strichman. Regression verification - a practical way to
    verify programs. In Bertrand Meyer and Jim Woodcock, editors, VSTTE: Verified
    Software: theories, tools, experiments, volume 4171, 2005. conf in 2005, published
    in 2007.
15. Benny Godlin and Ofer Strichman. Inference rules for proving the equivalence of
    recursive procedures. Acta Informatica, 45(6):403–439, 2008.
16. Benny Godlin and Ofer Strichman. Regression verification. In Proceedings of the
    46th Design Automation Conference, DAC 2009, San Francisco, CA, USA, July
    26-31, 2009, pages 466–471, 2009.
17. Benny Godlin and Ofer Strichman. Regression verification: proving the equivalence
    of similar programs. Softw. Test. Verification Reliab., 23(3):241–258, 2013.
18. Matthias Heizmann, Yu-Fang Chen, Daniel Dietsch, Marius Greitschus, Jochen
    Hoenicke, Yong Li, Alexander Nutz, Betim Musa, Christian Schilling, Tanja
    Schindler, and Andreas Podelski. Ultimate automizer and the search for perfect in-
    terpolants. In Dirk Beyer and Marieke Huisman, editors, Tools and Algorithms for
    the Construction and Analysis of Systems, pages 447–451, Cham, 2018. Springer
    International Publishing.
19. C. A. R. Hoare. Procedures and parameters: An axiomatic approach. In Symposium
    on Semantics of Algorithmic Languages, pages 102–116. 1971.
20. Krystof Hoder and Nikolaj Bjørner. Generalized property directed reachability. In
    Theory and Applications of Satisfiability Testing - SAT 2012 - 15th International
    Conference, Trento, Italy, June 17-20, 2012. Proceedings, pages 157–171, 2012.
21. Shuvendu K. Lahiri, Chris Hawblitzel, Ming Kawaguchi, and Henrique Rebêlo.
    SYMDIFF: A language-agnostic semantic diff tool for imperative programs. In
    Computer Aided Verification - 24th International Conference, CAV 2012, Berkeley,
    CA, USA, July 7-13, 2012 Proceedings, pages 712–717, 2012.
22. Panagiotis Manolios and Matt Kaufmann. Adding a total order to acl2. In The
    Third International Workshop on the ACL2 Theorem Prover, 2002.
23. Panagiotis Manolios and Daron Vroon. Ordinal arithmetic: Algorithms and mech-
    anization. Journal of Automated Reasoning, 2006. to appear.
24. Suzette Person, Matthew B. Dwyer, Sebastian Elbaum, and Corina S. Pundefined-
    sundefinedreanu. Differential symbolic execution. SIGSOFT ’08/FSE-16, page
    226–237, New York, NY, USA, 2008. Association for Computing Machinery.
25. Philipp Rümmer, Hossein Hojjat, and Viktor Kuncak. Disjunctive interpolants
    for horn-clause verification. In Computer Aided Verification - 25th International
    Conference, CAV 2013, Saint Petersburg, Russia, July 13-19, 2013. Proceedings,
    pages 347–363, 2013.
26. Koushik Sen. Concolic testing. In Proceedings of the Twenty-Second IEEE/ACM
    International Conference on Automated Software Engineering, ASE ’07, page
    571–572, New York, NY, USA, 2007. Association for Computing Machinery.
27. Ofer Strichman and Maor Veitsman. Regression verification for unbalanced re-
    cursive functions. In FM 2016: Formal Methods - 21st International Symposium,
    Limassol, Cyprus, November 9-11, 2016, Proceedings, pages 645–658, 2016.


                                         21
28. Anna Trostanetski, Orna Grumberg, and Daniel Kroening. Modular demand-
    driven analysis of semantic difference for program versions. In Francesco Ran-
    zato, editor, Static Analysis, pages 405–427, Cham, 2017. Springer International
    Publishing.
29. Nicky Williams, Bruno Marre, Patricia Mouy, and Muriel Roger. Pathcrawler:
    Automatic generation of path tests by combining static and dynamic analysis. In
    Mario Dal Cin, Mohamed Kaâniche, and András Pataricza, editors, Dependable
    Computing - EDCC 5, pages 281–292, Berlin, Heidelberg, 2005. Springer Berlin
    Heidelberg.
30. Andreas Zeller. Yesterday, my program worked. today, it does not. why? In Oscar
    Nierstrasz and Michel Lemoine, editors, Software Engineering - ESEC/FSE’99, 7th
    European Software Engineering Conference, Held Jointly with the 7th ACM SIG-
    SOFT Symposium on the Foundations of Software Engineering, Toulouse, France,
    September 1999, Proceedings, volume 1687 of Lecture Notes in Computer Science,
    pages 253–267. Springer, 1999.




                                        22
