                                         Automated Verification of Integer Overflow
                                         Asankhaya Sharma1
                                         1 SourceClear


                                         Corresponding author:
                                         Asankhaya Sharma1
                                         Email address: asankhaya@sourceclear.com
arXiv:1909.09324v1 [cs.PL] 20 Sep 2019




                                         ABSTRACT

                                         Integer overflow accounts for one of the major source of bugs in software. Verification systems typically assume
                                         a well defined underlying semantics for various integer operations and do not explicitly check for integer overflow
                                         in programs. In this paper we present a specification mechanism for expressing integer overflow. We develop an
                                         automated procedure for integer overflow checking during program verification. We have implemented a prototype
                                         integer overflow checker and tested it on a benchmark consisting of already verified programs (over 14k LOC). We
                                         have found 43 bugs in these programs due to integer overflow.



                                         INTRODUCTION
                                         Numerical errors in software are quite common and yet are ignored by most verifications systems. Integer overflow in
                                         particular has been among the top 25 software bugs (Christey et al., 2011). These errors can lead to serious failures and
                                         exploitable vulnerabilities. Program verification helps to build reliable software by ensuring that relevant properties of
                                         can be validated. In Hoare logic style program verification we typically specify programs using pre and post conditions.
                                         The verifier assumes an underlying well defined semantics and generates proofs of correctness of program. Most
                                         verification systems do not check for errors due to undefined behaviors in programs. In C/C++ the integer operations
                                         may lead to undefined behaviors as specified by the standard. Undefined behaviors in the C/C++ specification lead
                                         to confusion among programmers. Moreover many programmers expect wrap around behavior for integer overflow
                                         (Dietz et al., 2012) and may intentionally write code that leads to such overflows. The code written with undefined (in
                                         the language specification) intentional overflows is not guaranteed to be portable and the behavior may depend on the
                                         optimizations used in various compilers.
                                             It is no surprise that automated verifiers typically assume a well defined semantics for various integer operations.
                                         However in order to increase the completeness of verification it is desirable to specify and verify integer overflow.
                                         The starting point of this work is the HIP/SLEEK verification system (Chin et al., 2011) based on separation logic.
                                         HIP/SLEEK system can do automated verification of shape, size and bag properties of programs (Chin et al., 2012).
                                         We extend the domain of integers (extended number line) with two logical infinite constants ∞ and −∞, corresponding
                                         to positive and negative infinity respectively. Even though this kind extension of integers is common in libraries
                                         for programming languages for portability reasons, it is eventually typically mapped to a fixed value for a particular
                                         underlying architecture (32-bit or 64-bit). In a verification setting we find it better to enrich the underlying specification
                                         logic with these constants and reason with them automatically during entailment. This mechanism allows us to specify
                                         intentional and unintentional integer overflow in programs. In particular our key contributions are
                                             • A specification mechanism for integer overflows using logical infinities
                                             • Entailment procedure for handling logical infinities
                                             • Integrated integer overflow checking with automated verification
                                             • A prototype implementation of an Integer overflow checker
                                             • Finding 43 integer overflow bugs in existing benchmark of verified programs
    The rest of the paper is structured as follows. In the next section, we motivate our approach with a few examples.
Then we present our specification language with logical infinities. This specification language is used to describe
automated verification with integer overflow checking. We also formulate some soundness properties of our system.
In the experiments section we present our implementation with a benchmark of already verified programs. We describe
some related work and finally we conclude in the last section.

MOTIVATING EXAMPLES
We illustrate the integration of integer overflow checking in a verification system by means of few examples. The
following function increments the value passed to it.


       void ex1(int n)
         requires n≥0
         ensures res=n+1;
         {
           return n + 1;
         }

    If the value of n that is passed to this function is the maximum value that can be represented by the underlying
architecture this program will lead to an integer overflow. In order to avoid dealing with absolute values of maximum
and minimum integers we introduce a logical constant ∞ in the specification language. With this constant it is possible
to write the specification for the function to avoid integer overflow.


       void ex2(int n)
         requires 0≤n + 1<∞
         ensures res=n+1;
         {
           return n + 1;
         }

    Another benefit of adding this constant to the specification language is that it allows users to specify intentional
integer overflow. A recent study (Dietz et al., 2012) has found intentional integer overflow occurs frequently in real
codes. We allow a user to express integer overflow using ∞ constant where such behavior is well defined. The
following example shows how to specify intentional overflow.


       void ex3(int n)
         requires n≥0
         ensures (n+1<∞∧res=n+1)
                 ∨ (n+1≥∞∧(true)0ioc );
         {
           return n + 1;
         }

    In this example we use the error calculus from (Le et al., 2013) to specify integer overflow with an error status
(0ioc ). This error status is verified and propagated during entailment. Details of the error validation and localization
mechanism are given in (Le et al., 2013). Use of logical infinity constants (∞) enable us to specify intentional integer
overflow as an explicit error scenario in the method specification. Another benefit of using an enhanced specification
mechanism (with ∞ constants) is that we can integrate integer overflow checking in an expressive logic like separation
logic. This addresses two major problems faced by static integer overflow checkers - tracking integer overflow through
heap and integer overflows inside data structures. As an example consider the following method which returns the sum
of values inside a linked list.

                                                           2
       data {int val; node next}

       llhroot, sumi≡(root=null∧sum=0)∨
         ∃ d, q · (root7→nodehd, qi∗llhq, resti)∧sum=d+rest∧sum<∞

       int ex4(node x)
         requires llhx, si
         ensures llhx, si∧res=s
         {
           if (x == null)
             return 0;
           else
             return x.val + ex4(x.next);
         }
    We can specify the linked list using a predicate in separation logic (ll). In the predicate definition we use ∞
constant to express the fact that the sum of values in the list cannot overflow. With this predicate we can now write
the pre/post condition for the function ex4. During verification we can now check that the sum of values of linked list
will not lead to an integer overflow. A common security vulnerability that can be exploited using Integer overflow is
the buffer overrun. The following example (ex5) shows how two character arrays can be concatenated. We express
the bounds on the domain of arrays using a relation dom. This program can lead to an integer overflow if the sum of
the size of two arrays is greater than the maximum integer that can be represented by the underlying architecture. By
capturing the explicit condition under which this function can lead to an integer overflow (0ioc ) we can verify and
prevent buffer overrun. We again use the ∞ logical constant in the precondition to specify the integer overflow.

       dom(char[] c, int low, int high)

       dom(c, low, high)∧low ≤ l∧h ≤ high =⇒ dom(c, l, h)

       int ex5(ref char[] buf1, char[] buf2, size t len1, size t len2)
         requires dom(buf1, 0, len1)∧dom(buf2, 0, len2)∧len1 + len2 ≤ 256
         ensures res = 0∧dom(buf1, 0, len1 + len2);
         requires dom(buf1, 0, len1)∧dom(buf2, 0, len2)∧len1 + len2 > 256
         ensures res = −1∧dom(buf1, 0, len1);
         requires dom(buf1, 0, len1)∧dom(buf2, 0, len2)∧len1 + len2 > ∞
         ensures (true)0ioc ;
         {
           char buf[256];
           if(len1 + len2 > 256) return − 1;
           memcpy(buf, buf1, len1);
           memcpy(buf + len1, buf2, len2);
           buf1 = buf;
           return 0;
         }
     Using ∞ constant as part of the specification language we can represent various cases of integer overflows in a
concise manner. In this way we also avoid multiple constants like INT MAX, INT MIN etc., typically found in header
files for various architectures. When compared to other approaches, this specification mechanism is more suited to
finding integer overflows during verification.
     Exploitable vulnerabilities caused by integer overflows can also be prevented by specifications preventing overflow
using ∞. The following example (taken from (Dowd et al., 2006)) shows how integer overflow checking can prevent

                                                           3
network buffer overrun. For brevity we show only part of the functions and omit the specification for the method as
well. The function ex6 reads an integer from the network and performs some sanity checks on it. First, the length is
checked to ensure that it’s greater than or equal to zero and, therefore, positive. Then the length is checked to ensure
that it’s less than MAXCHARS. However, in the second part of the length check, 1 is added to the length. This opens
a possibility of the following buffer overrun: A value of INT MAX passes the first check (because it’s greater than
0) and passes the second length check (as INT MAX + 1 can wrap around to a negative value). read() would then be
called with an effectively unbounded length argument, leading to a potential buffer overflow situation. This situation
can be prevented by using the specifications given for the network get int method that ensures that length is always
less than ∞.


       int network get int(int sockfd)
         requires true
         ensures res < ∞;
       char ∗ ex6(int sockfd)
         {
           char buf;
           int length = network get int(sockfd);
           if(!(buf = (char∗) malloc(MAXCHARS)))
              die(“malloc : %m′′ );
           if(length < 0 || length + 1 >= MAXCHARS)
           {
              free(buf);
              die(“badlength : %d′′ , value);
           }
           if(read(sockfd, buf, length) <= 0)
           {
              free(buf);
              die(“read : %m′′ );
           }
           return buf;
         }


SPECIFICATION LANGUAGE
We present the specification language of our system which is extended from (Chin et al., 2012) with the addition of a
constant representing logical infinity. The detailed language is depicted in figure 1. Φpr ∗→ Φpo captures a precondition
Φpr and a postcondition Φpo of a method or a loop. They are abbreviated from the standard representation requires
Φpr and ensures Φpo , and formalized by separation logic formula Φ. In turn, the separation logic formula is a
disjunction of a heap formula and a pure formula (κ ∧π ). The pure part π captures a rich constraint from the domains
of Presburger arithmetic (supported by Omega solver (Pugh, 1992)), monadic set constraint (supported by MONA
solver (Klarlund and Moller, 2001)) or polynomial real arithmetic (supported by Redlog solver (Dolzmann and Sturm,
1997)). Following the definitions of separation logic in (Ishtiaq and O’Hearn, 2001; Reynolds, 2002), the heap part
provides notation to denote emp heap, singleton heaps 7→, and disjoint heaps ∗.
    The major feature of our system compared to (Ishtiaq and O’Hearn, 2001; Reynolds, 2002) is the ability for user
to define recursive data structures. Each data structure and its properties can be defined by an inductive predicate pred,
that consists of a name p, a main separation formula Φ and an optional pure invariant formula π that must hold for
every predicate instance. In addition to the integer constant k we now support a new infinite constant denoted by ∞.
This enables us to represent positive and negative infinities by ∞ and −∞ respectively. For the following discussion we
assume the existence of an entailment prover for separation logic (like (Chin et al., 2012)) and a solver for Presburger
arithmetic (like (Pugh, 1992)). We now focus only on integrating automated reasoning with the new infinite constant
∞ inside these existing provers.

                                                            4
                                pred     ::= p(v∗ ) ≡ Φ [inv π ]
                                mspec    ::= Φpr ∗→ Φpo
                                             W
                                Φ        ::= (∃w∗ ·κ ∧π )∗
                                κ        ::= emp | v7→c(v∗ ) | p(v∗ ) | κ1 ∗ κ2
                                π        ::= α | π1 ∧π2
                                α        ::= β | ¬β
                                β        ::= v1 =v2 | v=null | a1 ≤a2 | a1 =a2
                                a        ::= k | k×v | a1 + a2 | −a | max(a1 ,a2 )
                                              | min(a1 ,a2 ) | ∞

                                where     p is a predicate name; v, w are variable names;
                                          c is a data type name; k is an integer constant;


                                        Figure 1. The Specification Language



    An entailment prover for the specification language is used to discharge proof obligations generated during forward
verification. The entailment checking for separation logic formulas is typically represented (Chin et al., 2012) as
follows.


      Φ1 ⊢ Φ2 , Φr

    This attempts to prove that Φ1 entails Φ2 with Φr as its frame (residue) not required for proving Φ2 . This entailment
holds, if Φ1 =⇒ Φ2 ∗ Φr . Entailment provers for separation logic deal with the heap part (κ ) of the formula and
reduce the entailment checking to satisfiability queries over the pure part (π ). We now show how this reasoning can
be extended to deal with the new constant representing infinity (∞). A satisfiability check over pure formula with ∞
is reduced to a satisfiability check over a formula without ∞ which can be discharged by using existing solvers (like
Omega). In order to eliminate ∞ from the formula we take help of the equisatisfiable normalization rules shown in
figure 2 and proceed as follows.


       SAT (π )
       substitute equalities(v=∞)
        =⇒ SAT ([v/∞]π )
       normalization
        =⇒ SAT (π ; πnorm )
       elimintate ∞
        =⇒ SAT ([∞/v∞ ]πnorm )

    We start with substituting any equalities with ∞ constants then we apply the normalization rules. The normalization
rules eliminate certain expressions containing ∞ based on comparison with integer constants (k) and variables (v). We
show rules for both ∞ and −∞ in figure 2. In the normalization rules we use a1 6=a2 as a shorthand for ¬(a1 =a2 ).
During normalization, we may generate some equalities involving ∞ (in [NORM−VAR−INF]). In that case, we normalize
again after substituting the new equalities in the pure formula. Once no further equalities are generated we eliminate
the remaining ∞ constant if any by replacing it with a fresh integer variable v∞ in the pure formula. The pure formula
now does not contain any infinite constants and a satisfiability check on the formula can now be done using existing
methods.

                                                            5
                                  [NORM−INF−INF]
                                  ∞=∞ ; true                 [NORM−CONST−INF]
                                 ∞6=∞ ; false                  k=∞ ; false
                                  ∞≤∞ ; true                    k6=∞ ; true
                                ∞=−∞ ; false                    k≤∞ ; true
                                 ∞6=−∞ ; true                  ∞≤k ; false
                                ∞≤−∞ ; false                  k=−∞ ; false
                                −∞=−∞ ; true                   k6=−∞ ; true
                                −∞6=−∞ ; false                k≤−∞ ; false
                                −∞≤−∞ ; true                   −∞≤k ; true
                                 −∞≤∞ ; true

                                [NORM−VAR−INF]             [NORM−MIN−MAX]
                                  v≤∞ ; true                min(a, ∞) ; a
                                  ∞≤v ; v=∞                max(a, ∞) ; ∞
                                v≤−∞ ; v=−∞               min(a, −∞) ; −∞
                                 −∞≤v ; true               max(a, −∞) ; a

                                       Figure 2. Equisatisfiable Normalization



    Enriching the specification language with infinite constants is quite useful as it allows users to specify properties
(integer overflows) using ∞ as demostrated in the motivating examples. The underlying entailment procedure can
automatically handle ∞ by equisatisfiable normalization.

VERIFICATION WITH INTEGER OVERFLOW
Our core imperative language is presented in figure 3. A program P comprises of a list of data structure declarations
tdecl∗ and a list of method declarations meth∗ (we use the superscript ∗ to denote a list of elements). Data structure
declaration can be a simple node datat or a recursive shape predicate declaration pred as shown in figure 1.
    A method is declared with a prototype, its body e, and multiple specification mspec∗. The prototype comprises
a method return type, method name and method’s formal parameters. The parameters can be passed by value or
by reference with keyword ref and their types can be primitive τ or user-defined c. A method’s body consists of
a collection of statements. We provide basic statements for accessing and modifying shared data structures and for
explicit allocation of heap storage. It includes:
   1. Allocation statement: new c(v∗ )
   2. Lookup statement: For simplifying the presentation but without loss of expressiveness, we just provide one-level
      lookup statement v.f rather than v.f1 .f2 .
   3. Mutation statement: v1 .f := v2
    In addition we provide core statements of an imperative language, such as semicolon statement e1 ; e2 , function
call mn(v∗), conditional statement if v e1 e2 , and loop statement while v e (mspec)∗ . Note that for simplicity, we
just allow boolean variables (but not expression) to be used as the test conditions for conditional statements and loop
statement must be annotated with invariant through mspec∗. To illustrate some of the basic operations on integers in the
                                                                                                          [u]int    [u]int
language we also show the addition operation between two integers (unsigned and signed) in figure 3 as k1        + k2      .
    We now present the modifications needed to do forward verification with interger overflow. The core language used
by our system is a C-like imperative language described in figure 3. The complete set of forward verification rules are

                                                             6
                           P       ::= tdecl∗ meth∗
                           tdecl   ::= datat | pred
                           datat   ::= data c { field∗ }
                           field   ::= t v
                           t       ::= c | τ
                           τ       ::= uint | int | bool | float | void
                           meth    ::= t mn (([ref] t v)∗ ) where (mspec)∗ {e}
                                                      [u]int      [u]int
                           e       ::= null | kτ | k1        + k2        | v | v. f | v:=e | v1 . f :=v2
                                      | new c(v∗ ) | e1 ; e2 | t v; e | mn(v∗ )
                                      | if v then e1 else e2 | while v do e(mspec)∗


                                        Figure 3. A Core Imperative Language



as given in (Chin et al., 2012). We use P to denote the program being checked. With the pre/post conditions declared
for each method in P, we can now apply modular verification to its body using Hoare-style triples ⊢ {∆1 }e{∆2 }. We
expect ∆1 to be given before computing ∆2 since the rules are based on a forward verifier. To capture proof search,
we generalize the forward rule to the form ⊢ {∆1 }e{Ψ} where Ψ is a set of heap states, discovered by a search-based
verification process (Chin et al., 2012). When Ψ is empty, the forward verification is said to have failed for ∆1 as
prestate. As most of the forward verification rules are standard (Nguyen et al., 2007), we only provide those for method
verification and method call. Verification of a method starts with each precondition, and proves that the corresponding
postcondition is guaranteed at the end of the method. The verification is formalized in the rule [FV−[METH]]:

    • function prime(V) returns {v′ | v ∈ V }.
                                        V           ′
    • predicate nochange(V) returns       v∈V (v = v ). If V = {}, nochange(V)=true.

    • ∃W · Ψ returns {∃W · Ψi |Ψi ∈ Ψ}.


                                         [FV−[METH]]
                                V ={vm ..vn } W=prime(V )
                      ∀i = 1, .., p · ( ⊢ {Φipr ∧nochange(V )} e {Ψi1 }
                                           κ
                              (∃W·Ψi1 ) ⊢V,I Φipo ∗ Ψi2   Ψi2 6={})
                                                                             p
       t0 mn((ref t j v j )m−1             n                 i           i
                           j=1 , (t j v j ) j=m ) {requires Φpr ensures Φpo }i=1 {e}

                                                                               κ
    At a method call, each of the method’s precondition is checked, ∆⊢V,I        ρ Φipr ∗ Ψi , where ρ represents a substitution
           ′
of v j by v j , for all j = 1, .., n. The combination of the residue Ψi and the postcondition is added to the poststate. If a
precondition is not entailed by the program state ∆, the corresponding residue is not added to the set of states. The test
Ψ6={} ensures that at least one precondition is satisfied. Note that we use the primed notation for denoting the latest
value of a variable. Correspondingly, [v′0 /vi ] is a substitution that replaces the value vi with the latest value of v′0 .


                                                   [FV−[CALL]]
                            m−1                                                    p
        t0 mn((ref t j v j ) j=1 , (t j v j ) j=m ) {requires Φipr ensures Φipo }i=1
                                             n                                       {e} ∈ P
                                                        κ
                        ρ =[v′j /v j ]nj=m           ∆⊢V,I ρ Φipr ∗ Ψi ∀i=1, .., p
                                              Sp
                                     Ψ = i=1        Φipo ∗ Ψi       Ψ 6= {}
                                      ⊢ {∆} mn(v1 ..vn ) {Ψ}

                                                                  7
     In order to integrate integer overflow checking with automated verification we first translate the basic operations in
the core language (like integer addition) to method calls to specific functions which do integer overflow checking. In
this paper we illustrate the verification using only the addition overflow, however similar translations can be done for
other operators like multiplication (Moy et al., 2009) etc.. The addition operation for unsigned integers kuint1   + kuint
                                                                                                                       2
is translated to the method uadd whose specification is given below.


       int uadd(uint k1 , uint k2 )
         requires k1 +k2 >∞
         ensures (true)0ioc ;
         requires k1 +k2 ≤∞
         ensures res=k1 +k2 ;

    The addition of unsigned integers overflows when their sum is greater than ∞. The case of signed integer overflow
has several cases. We translate addition of signed integers to the method add. The specification of the add method
covers all the cases for signed integer overflow as detailed in (Dannenberg et al., 2010).


       int add(int k1 , int k2 )
         requires k1 >0∧k2 >0∧k1 +k2 >∞
                 ∨k1 >0∧k2 ≤0∧k1 +k2 <−∞
                 ∨k1 ≤0∧k2 >0∧k1 +k2 <−∞
                 ∨k1 ≤0∧k2 ≤0∧k1 +k2 <∞∧k1 6=0
         ensures (true)0ioc ;
         requires k1 >0∧k2 >0∧k1 +k2 ≤∞
                 ∨k1 >0∧k2 ≤0∧k1 +k2 ≥−∞
                 ∨k1 ≤0∧k2 >0∧k1 +k2 ≥−∞
                 ∨k1 ≤0∧k2 ≤0∧(k1 +k2 ≥−∞∨k1 =0)
         ensures res=k1 +k2 ;

    The specification of these methods (uadd and add) uses the infinite constants (∞ and −∞) from the enriched
specification language given in the previous section. An expressive specification language reduces the task of integer
overflow checking to just specifying and verifying of appropriate methods. After translation of basic operators into
method calls, during forward verification the [FV−[CALL]] rule will ensure that we check each operation for integer
overflow. Thus a simple encoding of basic operators and translation of the source program before verification enables
us to do integer overflow checking along with automated verification.

SOUNDNESS
In this section we outline the soundness properties of our entailment procedure with infinities and the forward ver-
ifier with integer overflow checking. We assume the soundness of the underlying entailment checker and verifier
(Chin et al., 2012).
Lemma 1. (Equisatisfiable Normalization)
 If π ; πnorm then SAT (π ) =⇒ SAT (πnorm ) and SAT (πnorm ) =⇒ SAT (π )
Proof       We sketch the proof for each normalization rule given in figure 2.
     case [NORM−INF−INF]: From the first rule we get, SAT (∞ = ∞) ≡ true
and the normalization gives ∞ = ∞ ; true, since SAT (true) ≡ true
we have, SAT (∞ = ∞) =⇒ SAT (∞ = ∞ ; true)
and SAT (∞ = ∞ ; true) =⇒ SAT (∞ = ∞).
Hence the normalization preserves satisfiability of pure formulas. We can prove the other rules in [NORM−INF−INF]
similarly.
     case [NORM−CONST−INF]: From the first rule we get, SAT (k = ∞) ≡ false
and the normalization gives k = ∞ ; false, since SAT (false) ≡ false

                                                            8
we have, SAT (k = ∞) =⇒ SAT (k = ∞ ; false)
and SAT (k = ∞ ; false) =⇒ SAT (k = ∞).
Hence the normalization preserves satisfiability of pure formulas. We can prove the other rules in [NORM−CONST−INF]
similarly.
   case [NORM−VAR−INF]: We sketch the proof for the following rule,
SAT (∞ ≤ v)
⇐⇒ SAT (∞ < v ∨ ∞ = v)
⇐⇒ SAT (false ∨ ∞ = v)
we have, SAT (∞ ≤ v) =⇒ SAT (∞ ≤ v ; v = ∞)
and SAT (∞ ≤ v ; v = ∞) =⇒ SAT (∞ ≤ v)
Hence the normalization preserves satisfiability of pure formulas. Other rules from [NORM−VAR−INF] can be proven
similarly.
   case [NORM−MIN−MAX]: We sketch the proof for the following rule,
SAT (max(a, ∞))
⇐⇒ SAT ((a > ∞ =⇒ a) ∨ (a ≤ ∞ =⇒ ∞))
⇐⇒ SAT ((false =⇒ a) ∨ (a ≤ ∞ =⇒ ∞))
⇐⇒ SAT ((true) ∨ (a ≤ ∞ =⇒ ∞))
⇐⇒ SAT (a ≤ ∞ =⇒ ∞)
⇐⇒ SAT (true =⇒ ∞)
⇐⇒ SAT (∞)
we have, SAT (max(a, ∞)) =⇒ SAT (max(a, ∞) ; ∞)
and SAT (max(a, ∞) ; ∞) =⇒ SAT (max(a, ∞))
Hence the normalization preserves satisfiability of pure formulas. Other rules from [NORM−MIN−MAX] can be proven
similarly.

Lemma 2. (Soundness of Integer Overflow Checking)
 If the program e has an integer overflow (0ioc ) then,
with forward verification ⊢ {∆1 }e{Ψ}, we have (true)0ioc ∈ Ψ
Proof       Provided all basic operators on integers in the program are translated to method calls that check for integer
overflows. The soundness of integer overflow checking follows from lemma 1 and the soundness of error calculus
(Le et al., 2013).
     The soundness of heap entailment and forward verification with separation logic based specifications is already
established in (Chin et al., 2012). Lemma 1 establishes that the normalization rules indeed preserve the satisfiability
of pure formulas. Lemma 2 then shows that the integer overflow checking with forward verification is sound. If the
program has an integer overflow the forward verification with integer overflow checking detects it.

EXPERIMENTS
We have implemented our approach in an OCaml prototype called HIPioc 1 evaluate automated verification using log-
ical infinities (∞) we created benchmark of several programs that use infinite constants as sentinel values in searching
and sorting. As an example the following predicate definition of a sorted linked list uses ∞ in the base case to express
that the minimum value in an empty list is infinity.


       data {int val; node next}

       Sortedllhroot, mini≡(root=null∧min=∞)∨
         ∃ q · (root7→nodehmin, qi∗Sortedllhq, minresti)∧min<minrest

   In addition, HIPioc allows us to do integer overflow checking of programs during verification. We have run
HIPioc on several existing verification benchmarks which contain different kinds of programs. The benchmarks
  1 Available at http://loris-5.d2.comp.nus.edu.sg/SLPAInf/SLPAInf.ova (md5sum 4afb66d65bfa442726717844f46eb7b6)




                                                           9
include many examples of programing manipulating complex heap, arrays, concurrency (barriers and variable permis-
sions) and some programs taken from real software (SIR). The results are shown in the table below. Sorting(with ∞)
are the programs which use ∞ as sentinel value in predicate definitions as described above and do not contain integer
overflows. Comparing the times between HIPioc and previous version we see that the verification with ∞ in general
adds some overhead.



                    Benchmark                 LOC    Num o f  Time    Time    Integer                         False
                     Programs               (Total) Programs (Secs) (HIPioc) Over f lows                     Positives
                  Sorting(with ∞)             282       4      5.45   5.42       0                              0
                      Arrays                  1432     21     47.92  76.65       1                              0
         HIP/SLEEK (Chin et al., 2012)        5779     42     56.15  78.80       4                              0
           Imm (David and Chin, 2011)         2069     11    120.82 126.61      18                              0
              V Perm (Le et al., 2012)        778      14      3.43   3.46       3                              0
       Barriers (Hobor and Gherghina, 2012)   1281     10     60.54  60.83      16                              0
                SIR (Le et al., 2013)         2616      4     34.64  41.73       1                              1
                       Total                 14237     106   328.95  393.5      43                              1

    In total we found 43 integer overflows in these programs. Since these programs were already verified by using
automated provers we notice that integer overflows are prevalent even in verified software. As our verification system
is based on over approximation (sound but not complete), it can lead to false positives when finding integer overflows.
In practice, we see that only 1 example in the experiments we conducted contained a false positive. The time taken to
do verification of programs without and with integer overflow checking shows that our technique can be applied to do
integer overflow checking of programs during verification with modest overhead.


RELATED WORK
There has been considerable interest in recent years to detect and prevent integer overflows in software (Cotroneo and Natella,
2012). Dietz et al. (Dietz et al., 2012) present a study of integer overflows in C/C++ programs. They find out that
intentional and unintentional integer overflows are prevalent in system software. Integer overflows often lead to ex-
ploitable vulnerabilities in programs (Christey et al., 2011). In this paper we presented a method to detect uninten-
tional integer overflows and provided a mechanism to specify intentional integer overflows. Program transformations
(Coker and Hafiz, 2013) can be used to guide the programmer and aid in refactoring the source code to avoid integer
overflows. Our focus is on specification of intentional integer overflows which helps make the conditions under which
the program may use an integer overflow explicit. It also aids in automated verification as such cases can be validated
as error scenarios for the program.
    Most existing techniques for detecting integer overflows are focused on dynamic checking and testing of programs
(Molnar et al., 2009; Wang et al., 2009; Chen et al., 2009; Brumley et al., 2007). Dynamic analysis suffers from the
path explosion problem and although several improvements in constraints solving have been proposed (Sharma, 2012,
2013) the approach cannot guarantee the absence of integer overflows. There are not many verification or static
analysis tool that can do integer overflow checking. KINT (Wang et al., 2012) is a static analysis tool which can
detect integer overflows by solving constraints generated from source code of programs. Another static analysis based
approach by Moy et al. (Moy et al., 2009) uses the Z3 solver to do integer overflow checking as part of the PREFIX
tool (Bush et al., 2000). A certified prover for presburger arithmetic extended with positive and negative infinities has
been described in (Sharma, 2015; Sharma et al., 2015).
    Our focus in this paper is on integrating integer overflow checking with program verification to improve the re-
liability of verified software. Dynamic techniques may not explore all paths in the programs while static techniques
suffer form loss of precision in tracking integer overflows. Our specification mechanism allows us to integrate integer
overflow checking inside a prover for specification logic. This allows us to track integer overflows through the heap
and inside various data structures. The benefit of this integration is that we can detect numeric integer overflow errors
in programs with complex sharing and heap manipulation.

                                                           10
CONCLUSION
Integer overflows are a major source of errors in programs. Most verification systems do not focus on the underlying
numeric operations on integers and do not handle integer overflow checking. We presented a technique to do integer
overflow checking of programs during verification. Our specification mechanism also allows expressing intentional
uses of integer overflows. We implemented a prototype of our proposal inside an existing verifier and found real
integer overflow bugs in benchmarks of verified software.


REFERENCES
Brumley, D., Song, D. X., cker Chiueh, T., Johnson, R., and Lin, H. (2007). Rich: Automatically protecting against
   integer-based vulnerabilities. In NDSS. 10
Bush, W. R., Pincus, J. D., and Sielaff, D. J. (2000). A static analyzer for finding dynamic programming errors. Softw.
  Pract. Exper., 30(7):775–802. 10
Chen, P., Wang, Y., Xin, Z., Mao, B., and Xie, L. (2009). Brick: A binary tool for run-time detecting and locating
   integer-based vulnerability. In Availability, Reliability and Security, 2009. ARES ’09. International Conference on,
   pages 208–215. 10
Chin, W.-N., David, C., and Gherghina, C. (2011). A hip and sleek verification system. In OOPSLA Companion,
   pages 9–10. 1
Chin, W.-N., David, C., Nguyen, H. H., and Qin, S. (2012). Automated verification of shape, size and bag properties
  via user-defined predicates in separation logic. Sci. Comput. Program., 77(9):1006–1036. 1, 4, 5, 7, 8, 9, 10
Christey, S., Martin, R. A., Brown, M., Paller, A., and Kirby, D. (2011). 2011 CWE/SANS Top 25 Most Dangerous
   Software Errors. Technical report, MITRE Corporation. http://cwe.mitre.org/top25. 1, 10
Coker, Z. and Hafiz, M. (2013). Program transformations to fix c integers. In Proceedings of the 2013 International
  Conference on Software Engineering, ICSE 2013. 10
Cotroneo, D. and Natella, R. (2012). Monitoring of aging software systems affected by integer overflows. In Software
  Reliability Engineering Workshops (ISSREW), 2012 IEEE 23rd International Symposium on, pages 265–270. 10
Dannenberg, R. B., Dormann, W., Keaton, D., Seacord, R. C., Svoboda, D., Volkovitsky, A., Wilson, T., and Plum, T.
  (2010). As-if infinitely ranged integer model. In Proceedings of the 2010 IEEE 21st International Symposium on
  Software Reliability Engineering, ISSRE ’10, pages 91–100, Washington, DC, USA. IEEE Computer Society. 8
David, C. and Chin, W.-N. (2011). Immutable specifications for more concise and precise verification. In OOPSLA,
   pages 359–374. 10
Dietz, W., Li, P., Regehr, J., and Adve, V. (2012). Understanding integer overflow in c/c++. In Proceedings of the
  2012 International Conference on Software Engineering, ICSE 2012, pages 760–770, Piscataway, NJ, USA. IEEE
   Press. 1, 2, 10
Dolzmann, A. and Sturm, T. (1997). Redlog: computer algebra meets computer logic. SIGSAM Bull., 31:2–9. 4
Dowd, M., McDonald, J., and Schuh, J. (2006). Art of Software Security Assessment, The: Identifying and Preventing
  Software Vulnerabilities. Addison-Wesley Professional. 3
Hobor, A. and Gherghina, C. (2012). Barriers in concurrent separation logic: Now with tool support! Logical Methods
   in Computer Science, 8(2). 10
Ishtiaq, S. and O’Hearn, P. (2001). BI as an assertion language for mutable data structures. In ACM POPL, pages
  14–26, London. 4
Klarlund, N. and Moller, A. (2001). MONA Version 1.4 - User Manual. BRICS Notes Series. 4
Le, D.-K., Chin, W.-N., and Teo, Y. M. (2012). Variable permissions for concurrency verification. In ICFEM, pages
   5–21. 10
Le, Q. L., Sharma, A., Craciun, F., and Chin, W.-N. (2013). Towards complete specifications with an error calculus.
   In NASA Formal Methods. 2, 9, 10
Molnar, D., Li, X. C., and Wagner, D. A. (2009). Dynamic test generation to find integer bugs in x86 binary linux
   programs. In Proceedings of the 18th conference on USENIX security symposium, SSYM’09, pages 67–82, Berkeley,
   CA, USA. USENIX Association. 10
Moy, Y., Bjørner, N., and Sielaff, D. (2009). Modular bug-finding for integer overflows in the large: Sound, efficient,
   bit-precise static analysis. Technical report, Microsoft Research. 8, 10

                                                         11
Nguyen, H., David, C., Qin, S., and Chin, W. (2007). Automated Verification of Shape And Size Properties via
  Separation Logic. In VMCAI, pages 251–266. 7
Pugh, W. (1992). The Omega Test: A fast practical integer programming algorithm for dependence analysis. Commu-
  nications of the ACM, 8:102–114. 4
Reynolds, J. (2002). Separation Logic: A Logic for Shared Mutable Data Structures. In IEEE LICS, pages 55–74. 4
Sharma, A. (2012). A critical review of dynamic taint analysis and forward symbolic execution. Technical report,
  National University of Singapore. 10
Sharma, A. (2013). An empirical study of path feasibility queries. arXiv preprint arXiv:1302.4798. 10
Sharma, A. (2015). Certified Reasoning for Automated Verification. PhD thesis, National University of Singapore. 10
Sharma, A., Wang, S., Costea, A., Hobor, A., and Chin, W.-N. (2015). Certified reasoning with infinity. In Interna-
  tional Symposium on Formal Methods, pages 496–513. Springer. 10
Wang, T., Wei, T., Lin, Z., and Zou, W. (2009). Intscope: Automatically detecting integer overflow vulnerability in
  x86 binary using symbolic execution. In NDSS. 10
Wang, X., Chen, H., Jia, Z., Zeldovich, N., and Kaashoek, M. F. (2012). Improving integer security for systems with
  kint. In Proceedings of the 10th USENIX conference on Operating Systems Design and Implementation, OSDI’12,
  pages 163–177, Berkeley, CA, USA. USENIX Association. 10




                                                        12
