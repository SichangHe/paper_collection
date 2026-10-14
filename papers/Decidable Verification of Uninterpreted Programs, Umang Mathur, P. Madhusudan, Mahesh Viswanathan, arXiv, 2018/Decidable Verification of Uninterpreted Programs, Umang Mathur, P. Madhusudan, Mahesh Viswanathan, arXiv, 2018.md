                                         Decidable Verification of Uninterpreted Programs

                                         UMANG MATHUR, University of Illinois, Urbana Champaign, USA
arXiv:1811.00192v4 [cs.PL] 26 Aug 2020




                                         P. MADHUSUDAN, University of Illinois, Urbana Champaign, USA
                                         MAHESH VISWANATHAN, University of Illinois, Urbana Champaign, USA
                                         We study the problem of completely automatically verifying uninterpreted programs—programs that work
                                         over arbitrary data models that provide an interpretation for the constants, functions and relations the pro-
                                         gram uses. The veriﬁcation problem asks whether a given program satisﬁes a postcondition written using
                                         quantiﬁer-free formulas with equality on the ﬁnal state, with no loop invariants, contracts, etc. being pro-
                                         vided. We show that this problem is undecidable in general. The main contribution of this paper is a subclass
                                         of programs, called coherent programs that admits decidable veriﬁcation, and can be decided in Pspace. We
                                         then extend this class of programs to classes of programs that are k-coherent, where k ∈ N, obtained by
                                         (automatically) adding k ghost variables and assignments that make them coherent. We also extend the de-
                                         cidability result to programs with recursive function calls and prove several undecidability results that show
                                         why our restrictions to obtain decidability seem necessary.
                                         CCS Concepts: • Theory of computation → Logic and veriﬁcation; Automated reasoning;
                                         Additional Key Words and Phrases: Uninterpreted Programs, Coherence, Program Veriﬁcation, Decidability,
                                         Streaming Congruence Closure
                                         ACM Reference Format:
                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan. 2019. Decidable Veriﬁcation of Uninterpreted Pro-
                                         grams. Proc. ACM Program. Lang. 3, POPL, Article 46 (January 2019), 36 pages. https://doi.org/10.1145/3290359

                                         1   INTRODUCTION
                                         Completely automatic veriﬁcation of programs is almost always undecidable. The class of sequen-
                                         tial programs, with and without recursive functions, admits a decidable veriﬁcation problem when
                                         the state-space of variables/conﬁgurations is ﬁnite, and this has been the cornerstone on which
                                         several fully automated veriﬁcation techniques have been based, including predicate abstraction,
                                         and model-checking. However, when variables range over inﬁnite domains, veriﬁcation almost
                                         inevitably is undecidable. For example, even for programs manipulating natural numbers with
                                         increment and decrement operators, and checks for equality, program veriﬁcation is undecidable.
                                            In this paper, we investigate classes of programs over uninterpreted functions and relations over
                                         inﬁnite domains that admit, surprisingly, a decidable veriﬁcation problem (with no user help what-
                                         soever, not even in terms of inductive loop invariants or pre/post conditions).
                                            A program can be viewed as working over a data-domain that consists of constants, functions                                46
                                         and relations. For example, a program manipulating integers works on a data-model that provides
                                         constants like 0, 1, functions like +, −, and relations like ≤, where there is an implicit assumption
                                         Authors’ addresses: Umang Mathur, Department of Computer Science, University of Illinois, Urbana Champaign, USA,
                                         umathur3@illinois.edu; P. Madhusudan, Department of Computer Science, University of Illinois, Urbana Champaign, USA,
                                         madhu@illinois.edu; Mahesh Viswanathan, Department of Computer Science, University of Illinois, Urbana Champaign,
                                         USA, vmahesh@illinois.edu.

                                         Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without fee
                                         provided that copies are not made or distributed for proﬁt or commercial advantage and that copies bear this notice and
                                         the full citation on the ﬁrst page. Copyrights for third-party components of this work must be honored. For all other uses,
                                         contact the owner/author(s).
                                         © 2019 Copyright held by the owner/author(s).
                                         2475-1421/2019/1-ART46
                                         https://doi.org/10.1145/3290359


                                                                          Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:2                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

 on the meaning of these constants, functions, and relations. Programs over uninterpreted data
 models work over arbitrary data-models, where the interpretation of functions and relations are
 not restricted in any way, except of course that equality is a congruence with respect to their
 interpretations (e.g., if x = y, then f (x) = f (y), no matter what the interpretation of f is). A
 program satisﬁes its assertions over uninterpreted data models if it satisﬁes the assertions when
 working over all data-models.
    The theory of uninterpreted functions is a theory that only has the congruence axioms, and
 is an important theory both from a theoretical and practical standpoint. Classical logic such as
 Gödel’s (weak) completeness theorem are formulated for such theories. And in veriﬁcation, when
 inductive loop invariants are given, veriﬁcation conditions are often formulated as formulas in
 SMT theories, where the theory of uninterpreted functions is an important theory used to model
 memory, pointers in heaps, arrays, and mathematical speciﬁcations. In particular, the quantiﬁer-
 free logic of uninterpreted functions is decidable and amenable to Nelson-Oppen combination with
 other theories, making it a prime theory in SMT solvers.
    We show, perhaps unsurprisingly, that veriﬁcation of uninterpreted programs is undecidable.
 The main contribution of this paper is to identify a class of programs, called coherent programs,
 for which veriﬁcation is decidable.
    Program executions can be viewed abstractly as computing terms conditioned on assumptions
 over terms. Assignments apply functions of the underlying data-domain and hence the value of
 a variable at any point in an execution can be seen as computing a term in the underlying data-
 model. Conditional checks executed by the program can be seen as assumptions the program
 makes regarding the relations that hold between terms in the data-model. For example, after an
 execution of the statements x := y; x := x + 1; assume(x > 0); z := x ∗ y, the program variable z
 corresponds to the term (b y + 1) ∗ yb, and the execution makes the assumption that yb+ 1 > 0, where
yb is the value of variable y at the start of the execution. A coherent program has only executions
 where the following two properties hold. The ﬁrst is the memoizing property that says that when
 a term is recomputed by the execution, then some variable of the program already has the same
 term (or perhaps, a diﬀerent term that is equivalent to it, modulo the assumptions seen so far in the
 execution). The second property, called early assumes says, intuitively, that when an assumption
 of equality between variables x and y is made by a program, superterms of the terms stored in
 variables x and y computed by the program must be stored in one of the current variables.
    We show that the notion of coherence eﬀectively skirts undecidability of program veriﬁcation.
 Both notions of memoizing and early-assumes require variables to store certain computed terms in
 the current set of variables. This notion in fact is closely related to bounded path-width of the com-
 putational graph of terms computed by the program; bounded path-width and bounded tree-width
 are graph-theoretic properties exploited by many decision procedures of graphs for decidability
 of MSO and for eﬃcient algorithms [Courcelle and Engelfriet 2012; Seese 1991], and there have
 been several recent works where they have been useful in ﬁnding decidable problems in veriﬁca-
 tion [Chatterjee et al. 2016, 2015; Madhusudan and Parlato 2011].
    Our decidability procedure is automata-theoretic. We show that coherent programs generate
 regular sets of coherent executions, and we show how to construct automata that check whether
 an execution satisﬁes a post-condition assertion written in quantiﬁer-free theory of equality. The
 automaton works by computing the congruence closure of terms deﬁned by equality assumptions
 in the execution, checking that the disequality assumptions are met, while maintaining this infor-
 mation only on the bounded window of terms corresponding to the current valuation of variables
 of the program. In fact, the automaton can be viewed as a streaming congruence closure algorithm
 that computes the congruence closure on the moving window of terms computed by the program.
 The assumption of coherence is what allows us to build such a streaming algorithm. We show that

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                   46:3

if either the memoizing assumption or the early-assumes assumption is relaxed, the veriﬁcation
problem becomes undecidable, arguing for the necessity of these assumptions.
   The second contribution of this paper is a decidability result that extends the ﬁrst result to a
larger class of programs — those uninterpreted programs that can be converted to coherent ones.
A program may not be coherent because of an execution that either recomputes a term when no
variable holds that term, or makes an assumption on a term whose superterm has been previously
computed but later over-written. However, if the program was given access to more variables,
it could keep the required term in an auxiliary variable to meet the coherence requirement. We
deﬁne a natural notion of k-coherent executions — executions that can be made coherent by adding
k ghost variables that are write-only and assigned at appropriate times. We show that programs
that generate k-coherent executions also admit a decidable veriﬁcation problem. The notion of k-
coherence is again related to path-width — instead of demanding that executions have path-width
|V |, we allow them to have path-width |V | + k, where V is the set of program variables.
   We also show that k-coherence is a decidable property. Given a program and k ∈ N, we can
decide if its executions can be made k-coherent. Notice that when k = 0, k-coherence is simply
coherence, and so these results imply the decidability of coherence as well. And if they can, we can
automatically build a regular collection of coherent executions that automatically add the ghost
variable assignments. This result enables us to verify programs by simply providing a program
and a budget k (perhaps iteratively increased), and automatically check whether the program’s
executions can be made k-coherent, and if so, perform automatic veriﬁcation for it.
   The third contribution of this paper is an extension of the above results to programs with re-
cursive function calls. We show that we can build visibly pushdown automata (VPA) that read
coherent executions of programs with function calls, and compute congruence closure eﬀectively.
Intersecting such a VPA with the VPA accepting the program executions and checking emptiness
of the resulting VPA gives the decidability result. We also provide the extension of veriﬁcation to
k-coherent recursive programs.
   To the best of our knowledge, the results here present the ﬁrst interesting class of sequential
programs over inﬁnite data-domains for which veriﬁcation is decidable1 .
   The main contributions of this paper are:
    • We show veriﬁcation of uninterpreted programs (without function calls) is undecidable.
    • We introduce a notion of coherent programs and show veriﬁcation of coherent uninterpreted
      programs (without function calls) is decidable and is Pspace-complete.
    • We introduce a notion of k-coherent programs, for any k. We show that given a program
      (without function calls) and a constant k, we can decide if it is k-coherent; and if it is, decide
      veriﬁcation for it.
    • We prove the above results for programs with (recursive) function calls, showing decidability
      and Exptime-completeness.
   The paper is structured as follows. Section 2 introduces uninterpreted programs and their veri-
ﬁcation problem, and summarizes the main results of the paper. Section 3 contains our main tech-
nical result and is devoted to coherent programs and the decision procedure for verifying them, as
well as the decision procedure for recognizing coherent programs. In Section 4, we show our un-
decidability results for general progams as well as programs that satisfy only one of the conditions
of the coherence deﬁnition. Section 5 consists of our decidability results for k-coherent programs.
In Section 6 we extend our results to recursive programs. Related work discussion can be found
1 There are some automata-theoretic results that can be interpreted as decidability results for sequential programs; but

these are typically programs reading streaming data or programs that allow very restricted ways of manipulating counters,
which are not natural classes for software veriﬁcation. See Section 7 for a detailed discussion.


                                 Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:4                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

in Section 7 and concluding remarks in Section 8 where we also discuss possible extensions and
applications of our results. We refer the reader to the appendix for detailed proofs of the results
presented.

2   THE VERIFICATION PROBLEM AND SUMMARY OF RESULTS
In this paper we investigate the veriﬁcation problem for imperative programs, where expressions
in assignments and conditions involve uninterpreted functions and relations. We, therefore, begin
by deﬁning the syntax and semantics of the class of programs we study, and then conclude the
section by giving an overview of our main results; the details of these results will be presented in
subsequent sections.
   Let us begin by recalling some classical deﬁnitions about ﬁrst order structures. A (ﬁnite) ﬁrst
order signature Σ is a tuple (C, F , R), where C, F , and R are ﬁnite sets of constants, function
symbols, and relation symbols, respectively. Each function symbol and relation symbol is implicitly
associated with an arity in N >0 . A ﬁrst order signature is algebraic if there are no relation symbols,
i.e., R = ∅. We will denote an algebraic signature as Σ = (C, F ) instead of Σ = (C, F , ∅). An
algebra or data model for an algebraic signature Σ = (C, F ), is M = (U , {JcK | c ∈ C}, {Jf K | f ∈
F }) which consists of a universe U and an interpretation for each constant and function symbol in
the signature. The set of (ground) terms are those that can be built using the constants in C and the
function symbols in F ; inductively, it is the set containing C, and if f is an m-ary function symbol,
and t 1 , . . . tm are terms, then f (t 1 , . . . tm ) is a term. We will denote the set of terms as TermsΣ or
simply Terms, since the signature Σ will often be clear from the context. Given a term t and a data
model M, the interpretation of t (or the value that t evaluates to) in M will be denoted by JtK M .

2.1 Programs
Our imperative programs will use a ﬁnite set of variables to store information during a computa-
tion. Let us ﬁx V = {v 1 , . . . vr } to be this ﬁnite set of variables. These programs will use function
symbols and relation symbols from a ﬁrst order signature Σ = (C, F , R) to manipulate values
stored in the variables. We will assume, without loss of generality, that the ﬁrst order signature
has constant symbols that correspond to the initial values of each variable at the begining of the
computation. More precisely, let V       b = {b x | x ∈ V } ⊆ C represent the initial values for each
variable of the program. The syntax of programs is given by the following grammar.
hstmti ::= skip | x := c | x := y | x := f (z) | assume (hcondi) | hstmti ; hstmti
             | if (hcondi) then hstmti else hstmti | while (hcondi) hstmti

hcondi ::= x = y | x = c | c = d | R(z) | hcondi ∨ hcondi | ¬hcondi
Here, f ∈ F , R ∈ R, c, d ∈ C, x, y ∈ V , and z is a tuple of variables in V and constants in C.
   The constructs above deﬁne a simple class of programs with conditionals and loops. Here, ‘:=’
denotes the assignment operator, ‘;’ stands for sequencing of programs, skip is a “do nothing” state-
ment, if − then − else is a construct for conditional statements and while is our looping construct.
We will also use the shorthand ‘if (hcondi) then hstmti’ as syntactic sugar for ‘if (hcondi) then hstmti else skip
The conditionals can be equality (=) atoms, predicates deﬁned by relations (R(·)), and boolean com-
binations (∨, ¬) of other conditionals. Formally, the semantics of the program depends on an un-
derlying data model that provides a universe, and meaning for functions, relations, and constants;
we will deﬁne this precisely in Section 2.3.
   The conditionals in the above syntax involve Boolean combinations of equalities as well as rela-
tions over variables and constants. However, for technical simplicity and without loss of generality,
we disallow relations entirely. Note that a relation R of arity m can be modeled by ﬁxing a new

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                              46:5

            P1                                       P2                                         P3

    assume(T , F);                         assume(x , z);                             assume(x , z);
    b := F;                                y := n(x);                                 y := n(x);
    while(x , y) {                         assume(y , z);                             g := y;
       d := key(x);                        y := n(y);                                 assume(y , z);
       if(d = k) then {                    while(y , z) {                             y := n(y);
          b := T;                             x := n(x);                              while(y , z) {
          r := x;                             y := n(y);                                 x := n(x);
       }                                   }                                             g := y;
       x := n(x);                                                                        y := n(y);
    }                                                                                 }

     @post: b=T ⇒ key(r)=k                  @post: z = n(n(x))                        @post: z = n(n(x))

         Fig. 1. Examples of Uninterpreted Programs; P1 and P3 are coherent, P2 is not coherent




constant ⊤ and introducing a new function f R of arity m and a variable bR . Then, each time we see
R(z), we add the assignment statement bR := f R (z) and replace the occurrence of R(z) by the condi-
tional ‘bR = ⊤’. Also, Boolean combinations of conditions can be modeled using the if−then−else
construct. Constant symbols used in conditionals and assignments can also be removed simply by
using a variable in the program that is not modiﬁed in any way by the program. Hence we will
avoid the use of constant symbols as well in the program syntax. Henceforth, without loss gener-
ality, we can assume that our ﬁrst order signature Σ is algebraic (R = ∅), constant symbols do not
appear in any of the program expressions, and our programs have conditionals only of the form
x = y or x , y.

Example 1. Consider the uninterpreted program P1 in Figure 1. The program works on any ﬁrst-
order model that has an interpretation for the unary functions n and key, and an initial interpreta-
tion of the variables T, F, x, y and k. The program is similar to a program that searches whether a
list segment from x to y contains a key k. However, in the program above, the functions n and key
are uninterpreted, and we allow all possible models on which the program can work. Note that if
and when the program terminates, we know that if b = T, then there is an element reachable from
x before reaching y such that key applied to that node is equal to k. Note that we are modeling T
and F, which are Boolean constants, as variables in the program (assuming that they are diﬀerent
elements in the model).
   Programs P2 and P3 in Figure 1 are also uninterpreted programs, and resemble programs that
given a linked list segment from x to z, ﬁnds the node that is two nodes before the node z (i.e., ﬁnd
the node u such that n(n(u)) = z).

2.2 Executions
Deﬁnition 1 (Executions). An execution over a ﬁnite set of variables V is a word over the alphabet
Π = {“x := y”, “x := f (z)”, “assume(x = y)”, “assume(x , y)” | x, y, z are in V }.

  We use quotes around letters for readability, and may sometimes skip them.

                            Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:6                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

Deﬁnition 2 (Complete and Partial Executions of a program). Complete executions of programs
that manipulate a set of variables V are executions over V deﬁned formally as follows:

               Exec(skip)         = ϵ
              Exec(x := y)        = “x := y”
           Exec(x := f (z))       = “x := f (z)”
         Exec(assume(c))          = “assume(c)”
 Exec(if c then s 1 else s 2 )    = “assume(c)” · Exec(s 1 ) ∪ “assume(¬c)” · Exec(s 2 )
              Exec( s 1 ; s 2 )   = Exec(s 1 ) · Exec(s 2 )
       Exec(while c {s} )         = [“assume(c)” · Exec(s 1 )]∗ · “assume(¬c)”

Here, c is a conditional of the form x = y or x , y, where x, y ∈ V .
   The set of partial executions, denoted by PExec(s), is the set of preﬁxes of complete executions
in Exec(s).

Example 2. For the example program P1 in Figure 1, the following word ρ
 ∆
ρ= assume(T , F) · b := F · assume(x , y) · d := key(x) · assume(d , k) · x := n(x)
       · assume(x , y) · d := key(x) · assume(d = k) · b := T · r := x · x := n(x)

is a partial execution of P1 and the word ρ 1 = ρ · assume(x = y) is a complete execution.

   Our notion of executions is more syntactic than semantic. In other words, we do not insist that
executions are feasible over any data model. For example, the word assume(x = y) · assume(x ,
y) · x := f (x) is an execution though it is not feasible over any data model. Note also that the com-
plete executions of a program capture (syntactically) terminating computations, i.e., computations
that run through the entire program.
   It is easy to see that an NFA accepting Exec(s) (as well as for PExec(s)) of size linear in s, for any
program s, can be easily constructed in polynomial time from s, using the deﬁnitions above and a
standard translation of regular expressions to NFAs.

Example 3. For the program P1 in Figure 1, its set of executions is given by the following regular
expression

assume(T , F) · b := F · R · assume(x = y)

where R is the regular expression

[assume(x , y) · d := key(x) · (assume(d , k) + assume(d = k) · b := T · r := x) · x := n(x)]∗

2.3     Semantics of Programs and The Verification Problem
Terms Computed by an Execution
We now deﬁne the set of terms computed by executions of a program over variables V . The idea
is to capture the term computed for each variable at the end of an execution. Recall that V    b = {b
                                                                                                    x |
x ∈ V } is the set of constant symbols that denote the initial values of the variables in V when the
execution starts, i.e., b
                        x denotes the initial value of variable x, etc. Recall that Terms are the set of
all terms over signature Σ. Let Π = {“x := y”, “x := f (z)”, “assume(x = y)”, “assume(x , y)” |
x, y, z are in V } be the alphabet of executions.


Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                               46:7


                                 y
                                     b
                                     y
                     T       b
                         b
                         T
                                                                 r                             x
                                     b
                                     x                     x)
                                                         n(b                       x))
                                                                               n(n(b
                     F
                         b
                         F
                                 k                                                             d
                                     b
                                     k                     x)
                                                       key(b                        x))
                                                                              key(n(b

                                         b

Fig. 2. Computation Graph of ρ 1 . Nodes represent terms computed in ρ 1 . Directed edges (      ) represent
immediate subterm relation. Nodes are labelled by variables that correspond to the terms denoted by nodes.
Undirected solid lines ( ) denote equalities and dashed lines (     ) denote disequalities seen in ρ 1


Deﬁnition 3. The term assigned to a variable x after some partial execution is captured using the
function Comp : Π∗ × V → Terms deﬁned inductively as follows.
                 Comp(ϵ, x)     = bx                                      for each x ∈ V
        Comp(ρ · “x := y”, x)   = Comp(ρ, y)
       Comp(ρ · “x := y”, x ′)  = Comp(ρ, x ′)                            x′ , x
     Comp(ρ · “x := f (z)”, x)  = f (Comp(ρ, z 1 ), . . . , Comp(ρ, zr )) where z = (z 1 , . . . , zr )
    Comp(ρ · “x := f (z)”, x ′) = Comp(ρ, x ′)                            x′ , x
 Comp(ρ · “assume(y = z)”, x)   = Comp(ρ, x)                              for each x ∈ V
 Comp(ρ · “assume(y , z)”, x)   = Comp(ρ, x)                              for each x ∈ V
                                                                      Ð
  The set of terms computed by an execution ρ is Terms(ρ) =                   Comp(ρ ′, x).
                                                                        ρ ′ is a preﬁx of ρ,
                                                                                 x ∈V

  Notice that the terms computed by an execution are independent of the assume statements in
the execution and depend only on the assignment statements.
Example 4. Consider the execution (from Example 2) below
   ∆
ρ1 = assume(T , F) · b := F · assume(x , y) · d := key(x) · assume(d , k) · x := n(x)
     · assume(x , y) · d := key(x) · assume(d = k) · b := T · r := x · x := n(x) · assume(x = y)
   For this execution, the set of terms computed can be visualized by the computation graph in Fig-
ure 2. Here, the nodes represent the various terms computed by the program, the solid directed
edges represent the immediate subterm relation, the solid lines represent the assumptions of equal-
ity made in the execution on terms, and the dashed lines represent the assumptions of dis-equality
made by the execution. The labels on nodes represent the variables that evaluate to the terms at
the end of the execution.
   Hence, we have Comp(ρ 1, x) = n(n(b                            x)), Comp(ρ 1 , b) = b
                                        x)), Comp(ρ 1, d) = key(n(b                    T, Comp(ρ 1, y) =
b                 b                   b                 b
y, Comp(ρ 1, k) = k, Comp(ρ 1 , T) = T, Comp(ρ 1 , F) = F, and Comp(ρ 1, r) = n(bx).

Equality and Disequality Assumptions of an Execution
Though the assume statements in an execution do not inﬂuence the terms that are assigned to any
variable, they play a role in deﬁning the semantics of the program. The equalities and disequalities
appearing in assume statements must hold in a given data model, for the execution to be feasible.
We, therefore, identify what these are.

                             Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:8                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

  For an (partial) execution ρ, let us ﬁrst deﬁne the set of equality assumes that ρ makes on terms.
Formally, for any execution ρ, the set of equality assumes deﬁned by ρ, called α(ρ), is a subset of
Terms(ρ) × Terms(ρ) deﬁned as follows.
       α(ϵ)   = ∅
                (
                  α(ρ) ∪ {(Comp(ρ, x), Comp(ρ, y))}                if a is “assume(x = y)”
 α(ρ · a)     =
                  α(ρ)                                            otherwise
   The set of disequality assumes, β(ρ), can be similarly deﬁned inductively.
       β(ϵ) =     ∅
                  (
                    β(ρ) ∪ {(Comp(ρ, x), Comp(ρ, y))}              if a is “assume(x , y)”
 β(ρ · a)     =
                    β(ρ)                                          otherwise
Example 5. Consider the execution (from Example 2) below
   ∆
ρ1 = assume(T , F) · b := F · assume(x , y) · d := key(x) · assume(d , k) · x := n(x)
       · assume(x , y) · d := key(x) · assume(d = k) · b := T · r := x · x := n(x) · assume(x = y)
                          x)), b
We have α(ρ 1 ) = {(key(n(b    k), (n(n(b   y)} and β(ρ 1 ) = {(b
                                        x)),b                   T, b
                                                                   F), (b          x), b
                                                                          y), (key(b
                                                                        x,b            k), (n(b
                                                                                              x),b
                                                                                                 y)}.

Semantics of Programs
We deﬁne the semantics of a program with respect to an algebra or data model that gives inter-
pretations to all the constants and function symbols in the signature. An execution ρ is said to be
feasible with respect to a data model if, informally, the set of assumptions it makes are true in that
model. More precisely, for an execution ρ, recall that α(ρ) and β(ρ) are the set of equality assumes
and disequality assumes over terms computed in ρ. An execution ρ is feasible in a data-model M,
if for every (t, t ′ ) ∈ α(ρ), JtK M = Jt ′ K M , and for every (t, t ′ ) ∈ β(ρ), JtK M , Jt ′ K M .

The Verification Problem
Let us now deﬁne the logic for postconditions, which are quantiﬁer-free formulas Boolean combi-
nation of equality constraints on variables. Given a ﬁnite set of variables V , the syntax for post-
conditions is deﬁned by the following logic L= .
        L= : φ ::= x =y | φ ∨ φ | ¬φ
where above, x, y ∈ V .
  Note that a more complex post-condition in the form of a quantiﬁer-free formulae using the
functions/relations/constants of the underlying data domain and the current variables can be in-
corporated by inserting code at the end of the program that computes the relevant terms, leaving
the actual postcondition to check only properties of equality over variables.
We can now deﬁne the veriﬁcation problem for uninterpreted programs.
Deﬁnition 4 (The Veriﬁcation Problem for Uninterpreted Programs). Given a L= formula φ over a
set of variables V , and a program s over V , determine, for every data-model M and every execution
ρ ∈ Exec(s) that is feasible in M, if M satisﬁes the formula φ under the interpretation that maps
every variable x ∈ V to JComp(ρ, x)K M .                                                          
  It is useful to observe that the veriﬁcation problem for a program s with postcondition φ in
L= can be reduced to the veriﬁcation of a program s ′ with additional assumes and if − then −
else statements and postcondition ⊥. Thus, without loss of generality, we may assume that the
postcondition is ﬁxed to be ⊥. Observe that in this situation, the veriﬁcation problem essentially

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                              46:9

reduces to determining the existence of an execution that is feasible in some data model. If there is
a feasible execution (in some data model) then the program violates its postcondition; otherwise
the program is correct.

2.4   Main Results
In this paper, we investigate the decidability of the veriﬁcation problem for uninterpreted pro-
grams. Our ﬁrst result is that this problem is, in general, undecidable. We discuss this in detail
in Section 4.
  Result #1: The veriﬁcation problem for uninterpreted programs is undecidable.
Since the general veriﬁcation problem is undecidable, we identify a special class of programs for
which the veriﬁcation problem is decidable. In order to describe what these special programs are,
we need to introduce a notion of coherent executions. Observe that as an execution proceeds, more
(structurally) complex terms get computed and assigned to variables, and more assume statements
identify constraints that narrow the collection of data models in which the execution is feasible.
Coherent executions satisfy two properties. The ﬁrst property, that we call memoizing, requires
that if a term t is computed (through an assignment) and either t or something “equivalent” (w.r.t.
to the equality assumes in the execution) to t was computed before in the execution, then it must
be currently stored in one of the variables. This is best illustrated through an example. Consider
the partial execution
 ∆
π= assume(x , z) · y := n(x) · g := y · assume(y , z) · y := n(y) · assume(y , z) · x := n(x)
of program P3 (in Figure 1). The term n(bx) is re-computed in the last step, but it is currently stored
in the variable g. On the other hand, a similar partial execution
   ∆
π′ = assume(x , z) · y := n(x) · assume(y , z) · y := n(y) · assume(y , z) · x := n(x)
of P2 is not memoizing since when n(b     x) is recomputed in the last step, it is not stored in any
variable; the contents of variable y, which stored n(b  x) when it was ﬁrst computed, have been over-
written at this point, or, in other words, the term n(b   x) was “dropped” by the execution before it
was recomputed. The second property that coherent executions must satisfy is that any step of the
form “assume(x = y)” in the execution comes “early”. That is, any superterms of the terms stored
in x and y computed by the execution upto this point, are still stored in the program variables and
have not been overwritten. The formal deﬁnition of coherent executions will be presented later
in Section 3 . Finally, a program is coherent if all its executions are coherent. The most technically
involved result of this paper is that the veriﬁcation problem for coherent uninterpreted programs
is decidable.
  Result #2: The veriﬁcation problem for coherent uninterpreted programs is decidable.
The notion of coherence is inspired by the notion of bounded pathwidth, but is admittedly techni-
cal. However, we show that determining if a given program is coherent is decidable; hence users
of the veriﬁcation result need not ensure that the program are coherent manually.
  Result #3: Given a program, the problem of checking whether it is coherent is decidable.
The notion of coherence has two properties, namely, that executions are memoizing and have early-
assumes. Both these properties seem to be important for our decidability result. The veriﬁcation
problem for programs all of whose executions satisfy only one of these two conditions turns out
to be undecidable.

                            Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:10                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

   Result #4: The veriﬁcation problem for uninterpreted programs whose executions are memoizing
is undecidable. The veriﬁcation problem for uninterpreted programs whose executions have early as-
sumes is undecidable.
The memoizing and early-assume requirements of coherence may not be satisﬁed by even sim-
ple programs. For example, program P2 in Figure 1 does not satisfy the memoizing requirement
as demonstrated by the partial execution π ′ above. However, many of these programs can be
made coherent by adding a ﬁnite number of ghost variables. These ghost variables are only writ-
ten and never read, and therefore, play no role in the actual computation. They merely remember
terms that have been previously computed and can help meet the memoizing and early-assume
requirements. We show that given a budget of k variables, we can automatically check whether
a corresponding coherent program with k additional ghost variables exists, and in fact compute
a regular automaton for its executions, and verify the resulting coherent program. The notation
and terminology for k-coherent programs is more complex and we delay deﬁning them formally
to Section 5, where they are considered.
  Result #5: Given a program P and k ∈ N, we can decide whether executions of P can be augmented
with k ghost variables and assignments so that they are coherent (i.e., check whether P is k-coherent).
Furthermore, if such a coherent program exists, we can construct it and verify it against speciﬁcations.

Finally, in Section 6, we consider programs with recursive function calls, and extend our results to
them. In particular, we show the following two results.
   Result #6: The veriﬁcation problem for coherent uninterpreted programs with recursive function
calls is decidable.
  Result #7 Given a program P, with recursive function calls, and k ∈ N, we can decide whether
executions of P can be augmented with k local ghost variables (for each function) and interleaved
ghost assignments that results in a coherent program. Furthermore, if such a coherent program exists,
we can construct it and verify if against speciﬁcations.

3     VERIFICATION OF COHERENT UNINTERPRETED PROGRAMS
The veriﬁcation problem for uninterpreted programs is undecidable; we will establish this result
in Section 4. In this section, we establish our main technical results, where we identify a class of
programs for which the veriﬁcation problem is decidable. We call this class of programs coherent.
We begin by formally deﬁning this class of programs. We then present our algorithm to verify
coherent programs. Finally, we conclude this section by showing that the problem of determining
if a given program is coherent is also decidable.
     Before presenting the main technical content of this section, let us recall that an equivalence
relation ⊆ Terms × Terms is said to be a congruence if whenever t 1  t 1′ , t 2  t 2′ , . . .tm  tm′ and f
                                                     ′          ′
is an m-ary function then f (t 1 , . . . tm )  f (t 1 , . . . tm ). Given a binary relation A ⊆ Terms × Terms,
the congruence closure of A, denoted A , is the smallest congruence containing A.
     For a congruence  on Terms, the equivalence class of a term t will be denoted by [t] ; when
=A , we will write this as [t]A instead of [t]A . For terms t 1 , t 2 ∈ Terms and congruence  on
Terms, we say that t 2 is a superterm of t 1 modulo  if there are terms t 1′ , t 2′ ∈ Terms such that t 1′  t 1 ,
t 2′  t 2 and t 2′ is a superterm of t 1′ .

3.1     Coherent Programs
Coherence is a key property we exploit in our decidability results, and is inspired by the concept
of bounded pathwidth. In order to deﬁne coherent programs we ﬁrst need to deﬁne the notion of

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                            46:11

coherence for executions. Recall that, for a partial execution ρ, α(ρ) denotes the set of equality
assumes made in ρ.

Deﬁnition 5 (Coherent executions). We say that a (partial or complete) execution ρ over variables
V is coherent if it satisﬁes the following two properties.
Memoizing. Let σ ′ = σ · “x :=f (z)” be a preﬁx of ρ and let t = Comp(σ ′, x). If there is a term t ′ ∈
     Terms(σ ) such that t ′ α (σ ) t, then there must exist some y ∈ V such that Comp(σ , y) α (σ )
     t.
Early Assumes. Let σ ′ = σ · “assume(x = y)” be a preﬁx of ρ and let t x = Comp(σ , x) and
     ty = Comp(σ , y). If there is a term t ′ ∈ Terms(σ ) such that t ′ is either a superterm of t x or
     of ty modulo α (σ ) , then there must exist a variable z ∈ V such that Comp(σ , z) α (σ ) t ′ .

Formally, the memoizing property says that whenever a term t is recomputed (modulo the con-
gruence enforced by the equality assumptions until then), there must be a variable that currently
corresponds to t. In the above deﬁnition, the assignment x := f (z) is computing a term t, and if
t has already been computed (there is a term t ′ computed by the preﬁx σ that is equivalent to t),
then we demand that there is a variable y which after σ , holds a term that is equivalent to t.
   The second requirement of early assumes imposes constraints on when “assume(x = y)” steps
are taken within the execution. We require that such assume statements appear before the execu-
tion “drops” any computed term t that is a superterm of the terms corresponding to x and y, i.e.,
before the execution reassigns the variables storing such superterms; notice that Terms(σ ) also in-
cludes those terms that have been computed along the execution σ and might have been dropped.
Formally, we demand that whenever an assume statement is executed equating variables x and y,
if there is a superterm (t ′ ) of either the term stored in x or y modulo the congruence so far, then
there must be a variable (z) storing a term equivalent to t ′ .
   Finally, we come to the main concept of this section, namely, that of coherent programs.

Deﬁnition 6 (Coherent programs). A coherent program is a program all of whose executions are
coherent.

Example 6. Consider the partial execution π ′ of P2 (Figure 1) that we considered in Section 2.4.
   ∆
π′ = assume(x , z) · y := n(x) · assume(y , z) · y := n(y) · assume(y , z) · x := n(x)
Any extension of π ′ to a complete execution of P2 , will not be coherent. This is because ρ ′ is not
memoizing — when n(b   x) is recomputed in the last step, it is not stored in any variable; the contents
of variable y, which stored n(bx) when it was ﬁrst computed, have been over-written at this point.
   On the other hand, the following execution over variables {x, y, z}
 ∆
σ= z := f(x) · z := f(z) · assume(x = y)

is also not coherent because “assume(x = y)” is not early. Observe that Comp(σ , x) = b
                                                                                      x, Comp(σ , y) =
b
y, and Comp(σ , z) = f(f(bx)). Now f(b
                                     x) ∈ Terms(σ ), is a superterm of Comp(σ , x) but is not stored
in any variable.
   Consider the programs in Figure 1. P2 is not coherent because of partial execution π ′ above.
On the other hand, program P1 is coherent. This is because whenever an execution encounters
“assume(d = k)”, both d and k have no superterms computed in the execution seen so far. The same
holds for the “assume(x = y)” at the end of an execution due to the while loop. Further, whenever
a term gets dropped, or over-written, it never gets computed again, even modulo the congruence
induced by the assume equations. Similar reasoning establishes that P3 is also coherent.

                            Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:12                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

3.2 Verifying Coherent Programs
We are now ready to prove that the veriﬁcation problem for coherent programs is decidable. Recall
that, without loss of generality, we may assume that the postcondition is ⊥. Observe that, when
the postcondition is ⊥, a program violates the postcondtion, if there is an execution ρ and a data
model M such that ρ is feasible in M, i.e., every equality and disequality assumption of ρ holds in
M. On the face of it, this seems to require evaluating executions in all possible data models. But
in fact, one needs to consider only one class of data models. We begin by recalling the notion of
an initial model.
    Given a binary relation A ⊆ Terms × Terms of equalities, M is said to satisfy A (or A holds in M)
if for every pair (t, t ′ ) ∈ A, JtK M = Jt ′ K M . For a relation A, there is a canonical model in which A
holds.
Deﬁnition 7. The initial term model for A ⊆ Terms×Terms over an algebraic signature Σ = (C, F )
is T (A) = (U , {JcK | c ∈ C}, {Jf K | f ∈ F }) where
    • U = Terms/A ,
    • JcK = [c]A for any c ∈ C, and
    • Jf K([t 1 ]A , . . . [tm ]A ) = [f (t 1 , . . . tm )]A for any m-ary function symbol f ∈ F and terms
       t 1 , . . . tm ∈ Terms.
   An important property of the initial term model is the following.
Proposition 1. Let A be a binary relation on terms, and M be any model satisfying A. For any
pair of terms t, t ′ , if JtK T(A) = Jt ′ K T(A) then JtK M = Jt ′ K M .
  Proof. Any model M deﬁnes an equivalence on terms ≡ M as follows: t ≡ M t ′ iﬀ JtK M = Jt ′ K M .
Observe that ≡ M is a congruence, and if M satisﬁes A, then A ⊆≡ M . Thus, A ⊆≡ M . Next, observe
that for the term model T (A), ≡ T(A) =A . The proposition follows from these observations.     
   One consequence of the above proposition is the following. Let A be a set of equalities, t 1 , t 2 be
terms, and M be a data model satisfying A. If Jt 1 K M , Jt 2 K M then Jt 1 K T(A) , Jt 2 K T(A) . This means
that to check the feasibility of an execution ρ, it suﬃces to check its feasibility in T (α(ρ)).
Corollary 2. Let ρ be any execution. There is a data model M such that ρ is feasible in M if and
only if ρ is feasible in T (α(ρ)).
That is, an execution ρ is feasible iﬀ α (ρ ) ∩β(ρ) = ∅.
   Let us return to the problem of verifying if a program satisﬁes the postcondition ⊥. This requires
us to check that no execution of the program is feasible in any data model. Let us now focus on the
simpler problem of execution veriﬁcation — given an execution ρ check if there is some data model
in which ρ is feasible. If we can solve the execution veriﬁcation problem, then we could potentially
solve the program veriﬁcation problem; since the set of executions of a program are regular, we
could run the execution veriﬁcation algorithm synchronously with the NFA representing the set
of all program executions to see if any of them are feasible.
   Corollary 2 has an important consequence for execution veriﬁcation — to check if ρ is feasible,
evaluate ρ in the data model T (α(ρ)). If the execution veriﬁcation algorithm is to be lifted to verify
all executions of a program, then the algorithm must evaluate the execution as the symbols come in.
It cannot assume to have the entire execution. This poses challenges that must be overcome. First
the term model T (α(ρ)) is typically inﬁnite and cannot be constructed explicitly. Second, since
equality assumptions come in as the execution unfolds, α(ρ) is not known at the beginning and
therefore, neither is the exact term model on which ρ must be evaluated known. In fact, in general,
we cannot evaluate an arbitrary execution ρ in a term model T (α(ρ)) in an incremental fashion.

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                               46:13

The main result of this section shows that we can exploit properties of coherent executions to
overcome these challenges.
   To explain the intuition behind our algorithm, let us begin by considering a naïve algorithm
that evaluates an execution in a data model. Suppose the data model M is completely known.
One algorithm to evaluate an execution ρ in M, would keep track of the values of each program
variable with respect to model M, and for each assume step, check if the equality or disequality
assumption holds in M. When M is the term model, the value that variable x takes after (partial)
execution ρ ′ , is the equivalence class of Comp(ρ ′, x) with respect to congruence deﬁned by all the
equality assumptions in the complete execution ρ.
   Our algorithm to verify an execution, will follow the basic template of the naïve algorithm above,
with important modiﬁcations. First, after a preﬁx ρ ′ of the execution ρ, we have only seen a par-
tial set of equality assumptions and not the entire set. Therefore, the value of variable x that the
algorithm tracks will be [Comp(ρ ′, x)]α (ρ ′) and not [Comp(ρ ′, x)]α (ρ ). Now, when a new equality
assumption assume(y = z) is seen, we will need to update the values of each variable to be that in
the term model that also satisﬁes this new equation. This requires updating the congruence class
of the terms corresponding to each variable as new equalities come in. In addition, the algorithm
needs to ensure that if a previously seen disequality assumption is violated because of the new
equation, it can be determined, eventhough the disequality assumption maybe between two terms
that are no longer stored in any of the program variables. Second, our algorithm will also track the
interpretation of the function symbols when applied to the values stored for variables in the pro-
gram. Thus, after a preﬁx ρ ′, the algorithm constructs part of the model T (α(ρ ′)) when restricted
to the variable values. This partial model helps the algorithm update the values of variables when
a new equality assume is read. The third wrinkle concerns how [Comp(ρ ′, x)]α (ρ ′) is stored. We
could store a representative term from this equivalence class. This would result in an algorithm
whose memory requirements grow with the execution. Instead the algorithm only maintains, for
every pair of variables x, y, whether their values in T (α(ρ ′)) are equal or not. This means that the
memory requirements of the algorithm do not grow with the length of the execution being ana-
lyzed. Thus, we will in fact show, that the collection of all feasible partial executions is a regular
language.
   In order to be able to carry out the above analysis incrementally, our algorithm crucially ex-
ploits the coherence properties of the execution. To illustrate one reason why the above approach
would not work for non-coherent executions, consider a preﬁx ρ ′ such that Comp(ρ ′, x) = b                       x,
Comp(ρ ′, y) = yb, Comp(ρ ′, u) = f 100 (b    x ), and Comp(ρ ′, v) = f 100 (b  y ). Let us assume that α(ρ ′) = ∅.
Suppose we now encounter assume(x = y). This means that in the term model that satisﬁes this
equality, the values of variables u and v are the same. However, this is possible only if the algo-
rithm somehow maintains the information that u and v are the result of hundred applications of
f to the values in x and y. This cannot be done using bounded memory. Notice, however, that in
this case ρ ′ · “assume(x = y)” is not a coherent execution because the assume at the end is not
early. Early assumes ensure that the eﬀect of an new equality assumption can be fully determined
on the current values to the variables.
   To understand the importance of the memoizing property in the decision procedure, consider the
                ∆
execution ρ ′ =   x := y ·y := f (y) · · · y := f (y) · x := f (x) · · · x := f (x). This execution trivially satis-
                          |          {z              } |           {z             }
                                    n times                     n times
                                                                                      y ), . . . , f n−1 (b
ﬁes the “early assumes” criterion. However it is not memoizing since the terms yb, f (b                   y)
                                                                             ∆ ′
have been re-computed after they have been dropped. Now, suppose that ρ = ρ · assume(x , y)
is a complete extension of ρ ′. Notice that ρ is not memoizing but still satisﬁes the “early as-
sumes” criterion (as it has no equality assumptions). Now, in order for the algorithm to correctly

                               Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:14                                              Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

determine that this execution is infeasible, it needs to correctly maintain the information that
Comp(ρ ′, y) = Comp(ρ ′, x) = f n (b
                                   y ). This again, is not possible using bounded memory.

Formal Details
We will now ﬂesh out the intuitions laid out above. We will introduce concepts and properties that
will be used in the formal construction and its correctness proof.
  Recall that our algorithm will track the values of the program variables in a term model. When
we have a coherent execution σ ′ = σ · assume(x = y), the terms corresponding to program
variables obey a special relationship with the set of terms Terms(σ ′) constructed anytime during
the execution and with the equality assumptions seen in σ . We capture this through the following
deﬁnition which has been motivated by the condition of early assumes.
Deﬁnition 8 (Superterm closedness modulo congruence). Let T be a subterm closed set of terms.
Let E ⊆ T × T be a set of equations on T and E be its congruence closure. Let W ⊆ T and let
t 1 , t 2 ∈ W . Then, W is said to be closed under superterms with respect to T , E and (t 1 , t 2 ) if for any
term s ∈ T such that s is a superterm of either t 1 or t 2 modulo E , there is term s ′ ∈ W such that
s ′ E s.
   Coherent executions ensure that the set of values of variables (or equivalently the set of terms
corresponding to the variables) is superterm closed modulo congruence with respect to a newly
encountered equality assumption; observe that for any partial execution ρ, Terms(ρ) is subterm
closed.
Lemma 3. Let σ be a coherent execution over variables V and let ρ ′ = ρ · “assume(x = y)” be any
preﬁx of σ . Then W = {Comp(ρ, v) | v ∈ V } is closed under superterms with respect to Terms(ρ),
α(ρ) and (Comp(ρ, x), Comp(ρ, y)).
   As pointed out in the overview, our algorithm will not explicitly track the terms stored in pro-
gram variable, but instead track the equivalence between these terms in the term model. In addi-
tion, it also tracks the interpretations of function symbols on the stored terms in the term model.
Finally, it will store the pairs of terms (stored currently in program variables) that have been as-
sumed to be not equal in the execution. The following deﬁnition captures when such an algorithm
state is consistent with a set of terms, equalities, and disequalities. In the deﬁnition below, the
reader may think of W as the set of terms corresponding to each program variable, E as the set
equality assumptions, and D as the set of disequality assumptions after a preﬁx of the execution.
Deﬁnition 9 (Consistency). Let W be a set of terms, E a set of equations on terms, and D be a
set of disequalities on terms. Let ≡W be an equivalence relation on W , DW ⊆ W /≡W ×W /≡W
be a symmetric relation, and P be a partial interpretation of function symbols, i.e., for any k-ary
function symbol f , P(f ) is a partial function mapping k-tuples in (W /≡W )k to W /≡W . We will say
(≡W , DW , P) is consistent with respect to (W , E, D) iﬀ the following hold.
   (a) For t 1 , t 2 ∈ W , t 1 ≡W t 2 if and only if Jt 1 K T(E) = Jt 2 K T(E) , i.e., t 1 and t 2 evaluate to the same
       value in T (E),
  (b) ([t 1 ]≡W , [t 2 ]≡W ) ∈ DW iﬀ there are terms t 1′ , t 2′ such that t 1′ E t 1 , and t 2′ E t 2 and {(t 1′ , t 2′ ), (t 2′ , t 1′ )}∩
       D , ∅.                               (
                                              [t]≡W if f (t 1 , . . . tk ) E t
   (c) P(f )([t 1 ]≡W , . . . , [tk ]≡W ) =
                                              undef otherwise
  There are two crucial properties about a set W that is superterm closed (Deﬁnition 8). When
we have a state that is consistent (as per Deﬁnition 9), we can correctly update it when we add an

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                       46:15

equation by doing a “local” congruence closure of the terms in W . This is the content of Lemma 4
and its detailed proof can be found in Appendix A.

Lemma 4. Let T be a set of subterm-closed set of terms, E ⊆ T ×T be a set of equalities on T , and
D ⊆ T × T be a set of disequalities. Let W ⊆ T be a set closed under superterms with respect to
T , E and some pair (s 1 , s 2 ) ∈ W × W . Let (≡W , DW , P) be consistent with (W , E, D). Deﬁne ∼s,s ′ to
be the smallest equivalence relation on W such that
     • ≡W ∪{(s, s ′)} ⊆∼s,s ′
     • for every k-ary function symbol f and terms t 1 , t 1′ , t 2 , t 2′ , . . . tk , tk′ , t, t ′ ∈ W such that t ∈
       P(f )([t 1 ]≡W , . . . [tk ]≡W ), t ′ ∈ P(f )([t 1′ ]≡W , . . . [tk′ ]≡W ), and (ti , ti′ ) ∈∼s,s ′ for each i, we have
       (t, t ′ ) ∈∼s,s ′ .
In addition, take DW     ′ = {([t ]
                                          1 ∼s, s ′ , [t 2 ]∼s, s ′ ) | ([t 1 ]≡W , [t 2 ]≡W ) ∈ DW } and
                                                           
                                                              [t]∼s, s ′ if P(f )([t 1 ]≡W , . . . [tk ]≡W ) = [t]≡W
        P ′ (f )([t 1 ]∼s, s ′ , . . . [tk ]∼s, s ′ ) =
                                                              undef otherwise
                ′ , P ′ ) is consistent with (W , E ∪ {(s, s ′ )}, D).
Then (∼s,s ′ , DW

   The second important property about W being superterm closed is that feasibility of executions
can be checked easily. Recall that, our previous observations indicate that an execution is feasible,
if all the disequality assumptions hold in the term model, i.e., if E is a set of equality assumptions
and D is a set of disequality assumptions, feasibility requires checking that E ∩D = ∅. Now,
we show that when W is superterm closed, then checking this condition when a new equation is
added to E can be done by just looking at W ; notice that D may have disequalities involving terms
that are not in W , and so the observation is not trivial.

Lemma 5. Let T be a set of subterm-closed set of terms, E ⊆ T ×T be a set of equalities on T , and
D ⊆ T ×T be a set of disequalities such that D∩ E = ∅. Let W ⊆ T and let t 1 , t 2 ∈ W be such that
W is closed under superterms with respect to T , E and (t 1 , t 2 ). Let (≡W , DW , P) be consistent with
(W , E, D). Then, E∪{(t1,t2 )} ∩D , ∅ iﬀ there are terms t 1′ , t 2′ ∈ W such that ([t 1′ ]≡W , [t 2′ ]≡W ) ∈ DW
and t 1′ ∼t1,t2 t 2′ , where ∼t1,t2 is the equivalence relation on W deﬁned in Lemma 4.

  Further, the notion of consistency allows us to correctly check for feasibility when a disequality
assumption is seen, and this is formalized below.

Lemma 6. Let T be a set of subterm-closed set of terms, W ⊆ T , E ⊆ T × T be a set of equalities
on T , and D ⊆ T × T be a set of disequalities such that D∩ E = ∅. Let (≡W , DW , P) be consistent
with (W , E, D) and let t 1 , t 2 ∈ W . Then, E ∩(D ∪ {(t 1 , t 2 )} , ∅ iﬀ (t 1 , t 2 ) ∈≡W .

   Lemmas 3, 4, 5 and 6 suggest that when an execution is coherent, the equivalence between
terms stored in program variables can be tracked and feasibility of the execution can be checked,
as equality and disequality assumptions are seen. Next, we will exploit these observations to give
the construction of an automaton that accepts exactly those coherent executions that are feasible.

Streaming Congruence Closure: Automaton for Feasibility of Coherent Executions
Having given a broad overview of our approach, and deﬁned various concepts and properties, we
are ready to present the main result of this section, which says that the collection of feasible partial
executions forms a regular language. Let us ﬁx V to be the set of program variables and Σ = (C, F )
to be the signature of operations. Recall that Π denotes the alphabet over which executions are

                                     Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:16                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

deﬁned. We now formally deﬁne the automaton Afs whose language is the collection of all partial
executions that are feasible in some data model.
States. The states in our automaton are either the special state q reject or tuples of the form (≡, d, P)
where ≡⊆ V × V is an equivalence relation, d ⊆ V /≡ ×V /≡ is symmetric and irreﬂexive, and P be
a partial interpretation of the function symbols in F , i.e., for any k-ary function symbol f , P(f ) is
a partial function from (V /≡)k to V /≡. Intuitively, in a state of the form (≡, d, P), ≡ captures the
equivalence amongst the terms stored in the variables that hold in the term model satisfying the
equalities seen so far, d are the disequality assumptions seen so far restricted to the terms stored
in the program variables, and P summarizes the interpretations of the function symbols in the
relevant term model.
Initial state. The initial state q 0 = (≡0 , d 0, P0 ), where ≡0 = {(x, x) | x ∈ V }, d 0 = ∅, and for every
k-ary function symbol f , and any x 1 , . . . x k ∈ V , P(f )([x 1 ]≡0 , . . . [x k ]≡0 ) = undef (undeﬁned).
Accepting states. All states except q reject are accepting.
Transitions. The q reject state is absorbing, i.e., for every a ∈ Π, δ fs (q reject , a) = q reject . For the
other states, the transitions are more involved. Let q = (≡, d, P) and let q ′ = (≡′, d ′, P ′ ). There is
a transtion δ fs (q, a) = q ′ if one of the following conditions holds. If in any of the cases d ′ is not
irreﬂexive then δ fs (q, a) = q reject in each case. For a subset V ′ ⊆ V , we will use the notation ≡ y   ′
                                                                                                          V
to denote the relation ≡ ∩V ′ × V ′ .

a = “x := y” .
      In this case if y and x are the same variables, then ≡′ = ≡, d ′ = d and P ′ = P. Otherwise,
      the variable x gets updated to be in the equivalence class of the variable y, and d ′ and P ′ are
      updated in the most natural way. Formally,
      • ≡′= ≡  y
                   V \{x }
                             ∪ {(x, y ′ ), (y ′, x) | y ′ ≡ y} ∪ {(x, x)}.
          ′
      • d = {([x 1 ]≡′ , [x 2 ]≡′ ) | x 1 , x 2 ∈ V \ {x }, ([x 1 ]≡, [x 2 ]≡ ) ∈ d }
      • P ′ is such that for every r -ary function h,
                                                        
                                                         [u] ′    x < {u, x 1 , . . . x r } and
                                                        
                                                         ≡
                                                        
                      ′
                   P (h)([x 1 ]≡′ , . . . [x r ]≡′ ) =             [u]≡ = P(h)([x 1 ]≡ , . . . [x r ]≡ )
                                                        
                                                        
                                                         undef otherwise
                                                        
a = “x := f (z 1 , . . . zk )” .
      There are two cases to consider.
    (1) Case P(f )([z 1 ]≡ , . . . [zk ]≡ ) is deﬁned.
        Let P(f )([z 1 ]≡, . . . [zk ]≡ ) = [v]≡. This case is similar to the case when a is “x := y”. That
        is, when x ∈ [v]≡, then ≡′ = ≡, d ′ = d and P ′ = P. Otherwise, we have
        • ≡′ = ≡    y
                        V \{x }
                                ∪ {(x, v ′), (v ′, x) | v ′ ≡ v} ∪ {(x, x)}
             ′
        • d = {([x 1 ]≡′ , [x 2 ]≡′ ) | x 1 , x 2 ∈ V \ {x }, ([x 1 ]≡, [x 2 ]≡ ) ∈ d }
        • P ′ is such that for every r -ary function h,
                                                           
                                                            [u] ′   x < {u, x 1 , . . . x r } and
                                                           
                                                            ≡
                                                           
                          ′
                       P (h)([x 1]≡′ , . . . [x r ]≡′ ) =            [u]≡ = P(h)([x 1 ]≡, . . . [x r ]≡ )
                                                           
                                                           
                                                            undef otherwise
                                                           
    (2) Case P(f )([z 1 ]≡ , . . . [zk ]≡ is undeﬁned.
        In this case, we remove x from its older equivalence class and make a new class that
        only contains the variable x. We update P to P ′ so that the function f maps the tuple


Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                          46:17

        ([z 1 ]≡′ , . . . , [zk ]≡′ ) (if each of them is a valid/non-empty equivalence class) to the class
        [x]≡′ . The set d ′ follows easily from the new ≡′ and the older set d. Thus,
        • ≡′ = ≡     y
                        V \{x }
                                    ∪ {(x, x)}
             ′
        • d = {([x 1 ]≡ 2 ]≡′ ) | x 1 , x 2 ∈ V \ {x }, ([x 1 ]≡, [x 2 ]≡ ) ∈ d }
                                ′ , [x
        • P ′ behaves similar to P for every function diﬀerent from f .
           – For every r -ary function h , f ,
                                                                    
                                                                     [u]≡′     if x < {u, x 1 , . . . x k } and
                                                                    
                                                                    
                                                                    
                              ′
                            P (h)([x 1 ]≡′ , . . . , [x r ]≡′ ) =               [u]≡ = P(h)([x 1 ]≡ , . . . [x r ]≡ )
                                                                    
                                                                    
                                                                     undef otherwise
                                                                    
           – For the function f , we have the following.
                                                                    
                                                                      [x]≡′     if x i = zi ∀i and x < {x 1 , . . . x k }
                                                                    
                                                                    
                                                                    
                                                                    
                                                                      [u]≡′     if x < {u, x 1 , . . . x k } and
                            P ′ (f )([x 1]≡′ , . . . , [x k ]≡′ ) =
                                                                    
                                                                                [u]≡ = P(f )([x 1 ]≡, . . . [x k ]≡ )
                                                                    
                                                                    
                                                                     undef otherwise
                                                                    
a = “assume(x = y)” .
      Here, we essentially merge the equivalence classes in which x and y belong and perform
      the “local congruence closure” (as in Lemma 4). In addition, d ′ and P ′ are also updated as in
      Lemma 4.
      • ≡′ is the smallest equivalence relation on V such that (a) ≡ ∪{(x, y)} ⊆≡′ , and (b) for
        every k-ary function symbol f and variables x 1 , x 1′ , x 2 , x 2′ , . . . x k , x k′ , z, z ′ ∈ V such that
        [z]≡ = P(f )([x 1 ]≡, . . . [x k ]≡ ), [z ′ ]≡ = P(f )([x 1′ ]≡ , . . . [x k′ ]≡ ), and (x i , x i′) ∈≡′ for each i, we
        have (z, z ′ ) ∈≡′.
      • d ′ = {([x 1 ]≡′ , [x 2 ]≡′ ) | ([x 1 ]≡ , [x 2 ]≡ ) ∈ d }
      • P ′ is such that for every r -ary function           (        h,
                                                               [u]≡′      if [u]≡ = P(h)([x 1 ]≡ , . . . [x r ]≡ )
                    P ′ (h)([x 1 ]≡′ , . . . [x r ]≡′ ) =
                                                               undef otherwise
a = “assume(x , y)” .
      In this case,
      • ≡′=≡
      • d ′ = d ∪ {([x]≡′ , [y]≡′ ), ([y]≡′ , [x]≡′ )}
      • P′ = P
 The formal description of automaton Afs is complete. We begin formally stating the invariant
maintained by the automaton during its computation.
Lemma 7. Let ρ be a coherent partial execution. Let q ρ be the state reached by Afs after reading
ρ. The following properties are true.
   (1) If ρ is infeasible then q ρ = q reject .
   (2) If ρ is feasible in some data model, then q ρ is of the form (≡, d, P) such that (≡, d, P) is consis-
       tent with ({Comp(ρ, x) | x ∈ V }, α(ρ), β(ρ)); see Deﬁnition 9 for the notion of consistency.
                                                                                                           O (1)
   Assuming that the signature Σ is of constant size, the automaton Afs has O(2 |V |                               ) states.

Verifying a Coherent Program
We have so far described a ﬁnite memory, streaming algorithm that given a coherent execution
can determine if it is feasible in any data model by computing congruence closure. We can use that
algorithm to verify coherent, uninterpreted programs.

                                  Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:18                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

Theorem 8. Given a coherent program s with postcondition ⊥, the problem of verifying s is PSPACE-
complete.
   Proof Sketch. Observe that a coherent program with postcondition ⊥ is correct if it has no
feasible executions. If As is the NFA accepting precisely the executions of s, the goal is to determine
if L(As )∩L(Afs ) , ∅. This can be done taking the cross product of the two automata and searching
for an accepting path. Notice that storing the states of Afs uses space that is polynomial in the
number of variables, and the cross product automaton can be constructed on the ﬂy. This gives us
a PSPACE upper bound for the veriﬁcation problem.
   The lower bound is obtained through a reduction from Boolean program veriﬁcation. Recall that
Boolean programs are imperative programs with while loops and conditionals, where all program
variables take on Boolean values. The veriﬁcation problem for such programs is to determine if
there is an execution of the program that reaches a special halt statement. This problem is known
to be PSPACE-hard. The Boolean program veriﬁcation problem can be reduced to the veriﬁcation
problem for uninterpreted programs — the uninterpreted program corresponding to a Boolean
program will have no function symbols in its signature, have constants for true and false, and
have two program variables that are never modiﬁed which store true and false respectively. Since
in such a program the variables never store terms other than constants, the executions are trivially
coherent.                                                                                             

3.3     Decidability of Coherence
Manually checking if a program is coherent is diﬃcult. However, in this section we prove that,
given a program s, checking if s is coherent can be done in PSPACE. The crux of this result is an
observation that the collection of coherent executions form a regular language. This is the ﬁrst
result we will prove, and we will use this observation to give a decision procedure for checking if
a program is coherent. Let us recall that executions of programs over variables V are words over
the alphabet Π.
Theorem 9. The language L cc = {ρ ∈ Π∗ | ρ is coherent} is regular. More precisely, there is a DFA
                O (1)
Acc of size O(2V ) such that L(Acc ) = L cc .
   Proof. Observe that an execution ρ is coherent if and only if the execution ρ⇂Π\{assume(x ,y) | x,y ∈V }
is coherent; here ρ ⇂Π\{assume(x ,y) | x,y ∈V } is the execution obtained by dropping all the disequal-
ity assumes from ρ. Hence, the automaton Acc will ignore all the disequality assumes and only
process the other steps.
   The automaton Acc heavily uses the automaton Afs , constructed in Section 3.2. Intuitively, given
a word ρ, our algorithm inductively checks whether preﬁxes of ρ are coherent. Hence, when ex-
amining a preﬁx σ · a, we can assume that σ is coherent and use the properties of the state of Afs
obtained on σ .
   The broad outline of how Acc works is as follows.
    • We keep track of the state of the automaton Afs . Recall that its state is of the form (≡, d, P),
      where ≡ deﬁnes an equivalence relation over the variables V , d is a set of disequalities, and
      P is a partial interpretation of the function symbols in the signature, restricted to contents of
      the program variables. Now, since we will drop all the disequality assumes, d in this context
      is always ∅ and so the state of Afs will never be q reject .
    • In addition, the state of Acc will have a function E that associates with each function symbol
       f of arity k, a function from (V /≡)k to {⊤, ⊥}. Intuitively, E tracks, for each function symbol
       f and each tuple of variables, whether f has ever been computed on that tuple at any point
      in the execution — E(f )(z) = ⊤, if f (z) has been computed, and is ⊥ if it has not. Note that,

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                              46:19

      if P(f )(z) is deﬁned (here P is the component that is part of the state of Afs ) then E(f )(z)
      will deﬁnitely be ⊤. The role of E(f ), however, is to remember in addition whether f has
      been computed on terms but the image has been “dropped” by the program.
   The update of the extra information E(f ) is not hard. Whenever Acc reads “x := f (z 1 , . . . zk )”,
we set E(f )([z 1 ]≡ , . . . [zk ]≡ ) to ⊤. If E(f )([z 1 ]≡ , . . . [zk ]≡ ) = ⊤, then we know it was computed,
and hence check if P(f )([z 1 ]≡ , . . . [zk ]≡ ) is deﬁned. If it is not, then we reject the word as it is not
memoizing and therefore, not coherent.
   An assume(x = y) statement is dealt with as follows. Let us assume that the state of Acc is
q = (≡, ∅, P, E) when it processes assume(x = y). First Acc checks if the equality is early as
follows. We will say that a variable v is an immediate superterm of u in q, if there is a function f
and arguments z such that P(f )(z) = [v]≡ and [u]≡ ∈ z. More generally, v is a superterm of u in q
if either [v]≡ = [u]≡ , or there is a variable w such that w is an immediate superterm of u in q and v
(inductively) is a superterm of w in q. To check that assume(x = y) is not early, we will ﬁrst check
if there is a superterm u of either x or y in q and a tuple z such that [u]≡ ∈ z such that P(f )(z)
is undeﬁned but E(f )(z) = ⊤. If assume(x = y) is early then Acc will merge several equivalence
classes of variables as it performs congruence closure locally. Whenever two equivalence classes
C and C ′ merge, we set E(f )(z) to ⊤ and appropriately deﬁne P(f )(z) (similar to the transition in
Afs ) if there were any equivalent variables that were to ⊤ by E(f ).
   After reading each letter, if the word is not rejected, we are guaranteed that the word is coherent,
and hence the meaning of the state of automaton Afs is correct when reading the next letter. Hence
the above automaton precisely accepts the set of coherent words.                                              

   Observe that since Acc constructed in Theorem 9 is deterministic, it can be modiﬁed without
blowup to accept only non-coherent words as well.
   Using Acc we can get a PSPACE algorithm to check if a program is coherent.
   We can now compute, given a program s, the NFA for Exec(s), and check whether the intersec-
tion of Exec(s) and the above automaton constructed for accepting non-coherent words is empty.
Hence
Theorem 10. Given a program s, one can determine if s is coherent in PSPACE.

  Proof. Let As be the NFA accepting the set of execution of program s. Let Acc be the au-
tomaton accepting the collection of all non-coherent executions. Notice that s is coherent iﬀ
L(As ) ∩ L(Acc ) = ∅. The PSPACE algorithm will construct the product of As and Acc on the
ﬂy, while it searches for an accepting computation.                                         

4 UNDECIDABILITY OF VERIFICATION OF UNINTERPRETED PROGRAMS
We show that verifying uninterpreted programs is undecidable by reducing the halting problem
for 2-counter machines.
  A 2-counter machine is a ﬁnite-state machine (with Q as the set of states) augmented with two
counters C 1 and C 2 that take values in N. At every step, the machine moves to a new state and
performs one of the following operations on one of the counters: check for zero, increment by 1,
or decrement by 1. We can reduce the halting problem for 2-counter machines to veriﬁcation of
uninterpreted programs to show the following result (detailed proof in Appendix B).
Theorem 11. The veriﬁcation problem for uninterpreted programs is undecidable.
  The reduction in the above proof proceeds by encoding conﬁgurations using primarily three
variables, a variable x curr modeling the current state, and two variables y1 and y2 modeling the

                              Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:20                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

two counters, along with other variables {x q }q ∈Q modeling constants for the set of states and the
constant 0 ∈ N and few other auxiliary variables.
   The key idea is to model a counter value i using the term f i (0), and to ensure the data model has
two functions f and д, modeling increment and decrement functions respectively, that are inverses
of each other on terms representing counter values. We refer the reader to the details of the proof,
but note here that this reduction in fact creates programs that are not memoizing nor have early
assumes, and in fact cannot be made coherent with any bounded number of ghost variables.
   In the following undecidability results (Theorem 12 and Theorem 13) that argue that both our
restrictions are required for decidability. The proof ideas of these theorems are provided in Appen-
dix B.
Theorem 12. The veriﬁcation problem for uninterpreted programs all of whose executions are mem-
oizing is undecidable.
Theorem 13. The veriﬁcation problem for uninterpreted programs all of whose executions have
early-assumes is undecidable.
  The proofs for the theorems above also give reductions from the halting problem for 2-counter
machines; one ensures that executions satisfy the memoizing property (while sacriﬁcing the early-
assumes criterion) and the other that executions satisfy early-assumes (but not memoizing).
  Note that the above results do not, of course, mean that these two conditions themselves cannot
be weakened while preserving decidability. They just argue that neither condition can be simply
dropped.

5 k-COHERENT UNINTERPRETED PROGRAMS
In this section, we will generalize the decidability results of Section 3 to apply to a larger class of
programs. Programs may sometimes not be coherent because they either violate the memoizing
property, i.e., they have executions where a term currently not stored in any of the program vari-
ables, is recomputed, or, they violate the early assumes criterion, i.e., have executions where an
assume is seen after some superterms have been dropped entirely. However, some of these pro-
grams could be made to coherent, if they were given access to additional, auxiliary variables that
store the terms that need to be recomputed in the future or are needed until a relevant assume
statement is seen in the future. For example, we observed that program P2 in Figure 1 is not coher-
ent (Example 6), but program P3 , which is identical to P2 except for the use of auxiliary variable g
is coherent. These auxiliary variables, which we call ghost variables, can only be written to. They
are never read from, and so do not aﬀect the control ﬂow in the program. We show that the veriﬁ-
cation problem for k-coherent programs — programs that can be made coherent by adding k ghost
variables — is decidable. In addition, we show that determining if a program is k-coherent is also
decidable.
   Let us ﬁx the set of program variables to be V = {v 1 , v 2, . . . vr } and the signature to be Σ =
(C, F ) such that V b ⊆ C is the set of initial values of the program variables. Recall that executions
of such programs are over the alphabet Π = {“x := y”, “x := f (z)”, “assume(x = y)”, “assume(x ,
y)” | x, y, z are in V }.
   Let us deﬁne executions that use program variables V and ghost variables G = {д1 , д2 , . . . дl }.
These will be words over the alphabet Π(G) = Π ∪ {“д := x” | д ∈ G and x ∈ V }. Notice, that
the only additional step allowed in such executions is one where a ghost variable is assigned the
value stored in a program variable. Before presenting the semantics of such executions, we will
introduce some notation. For an execution ρ ∈ Π(G)∗ , ρ⇂Π denotes its projection onto alphabet Π,
i.e., it is the sequence obtained by dropping all ghost variable assignment steps.

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                           46:21

   To deﬁne the semantics of such executions, we once again need to associate terms with variables
at each point in the execution. The (partial) function Comp : Π(G)∗ × (V ∪ G) → Terms will
be deﬁned in the same manner as in Deﬁnition 3. The main diﬀerence will be that Comp now
is a partial function, since we will assume that ghost variables are undeﬁned before their ﬁrst
assignment; we do not have constants in our signature Σ corresponding to initial values of ghost
variables. For variables x ∈ V , we deﬁne Comp(ρ, x) = Comp(ρ⇂Π , x), where the function Comp
on the right hand side is given in Deﬁnition 3. For ghost variables, Comp is deﬁned inductively as
follows.
                    Comp(ϵ, д) = undef              for each д ∈ G
          Comp(ρ · “д := x”, д) = Comp(ρ, x)
         Comp(ρ · “д := x”, д ′ ) = Comp(ρ, д ′) for д ′ , д
                 Comp(ρ · a, д) = Comp(ρ, д) for any д ∈ G, and a ∈ Π
  The set of equality and disequality assumes for executions with ghost variables can be deﬁned in
the same way as it was deﬁned for regular executions. More precisely, for any execution ρ ∈ Π(G)∗ ,
the set of equality assumes is α(ρ) = α(ρ⇂Π ) and the set of disequality assumes is β(ρ) = β(ρ⇂Π ).
  An execution ρ with ghost variables is coherent if it satisﬁes the memoization and early assumes
conditions given in Deﬁnition 5, except that we also allow variables in G to hold superterms mod-
ulo congruence. We are now ready to deﬁne the notion of k-coherence for executions and programs.
Deﬁnition 10. An execution σ ∈ Π∗ over variables V is said to be k-coherent if there is an
execution ρ ∈ Π(G) over V and k ghost variables G = {д1 , . . . дk } such that (a) ρ is coherent,
and (b) ρ⇂Π = σ .
  A program s over variables V is said to be k-coherent if every execution σ ∈ Exec(s) is k-
coherent.
  Like coherent executions, the collection of k-coherent executions are regular.
Proposition 14. The collection of k-coherent executions over program variables V is regular.
  Proof. Theorem 9 establishes the regularity of the collection of all coherent executions. The
automaton Acc constructed in its proof in Section 3.3 essentially also recognizes the collection
of all coherent executions over the set V ∪ G. Now, observe that the collection of k-coherent
executions over the set V is L(Acc ) ⇂Π , and therefore the proposition follows from the fact that
regular languages are closed under projections.                                                 

  Given a program, one can decide if it is k-coherent.
Theorem 15. Given an uninterpreted program s over variables V , one can determine if s is k-coherent
in space that is linear in |s | and exponential in |V |.
   Proof. Let As be the NFA that accepts the executions of program s, and Acc be the automaton
recognizing the set of all coherent executions over V and G. Let Akcc be the automaton recogniz-
ing L(Acc )⇂Π , which is the collection of all k-coherent executions. Observe that s is k-coherent if
                                                                        O (1)
L(As ) ⊆ L(Akcc ). Akcc is a nondeterministic automaton with O(2 |V | ) states, and the proposi-
tion therefore follows.                                                                            

  Finally, the veriﬁcation problem for uninterpreted k-coherent programs is PSPACE-complete.
Theorem 16. Given a k-coherent program s with postcondition ⊥, the problem of verifying s is
PSPACE-complete.

                           Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:22                                           Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

   Proof. Since every coherent program is also k-coherent (for any k), the lower bound follows
from Theorem 8. Let As be the automaton accepting executions of s, Acc the automaton ac-
cepting coherent executions over V and G, and Afs the automaton checking feasibility of exe-
cutions. Observe that the automaton A recognizing (L(Acc ) ∩ L(Afs ))⇂Π accepts the collection of
k-coherent executions that are feasible. The veriﬁcation problem requires one to determine that
L(A) ∩L(As ) = ∅. Using an argument similar to the proof of Theorem 8, this can be accomplished
in PSPACE because A has exponentially many states.                                             

6 VERIFICATION OF COHERENT AND k-COHERENT RECURSIVE PROGRAMS
In this section, we extend the decidability results to recursive programs. In particular, we deﬁne
the notions of coherence and k-coherence for recursive programs, and show that the following
problems are decidable: (a) verifying recursive coherent programs; (b) determining if a recursive
program is coherent; (c) verifying recursive k-coherent programs; and (d) determining if a program
is k-coherent.
   This section will extend the automata-theoretic constructions to visibly pushdown automata [Alur and Madh
2004], and use the fact that they are closed under intersection; we assume the reader is familiar
with these automata as well as with visibly context-free languages [Alur and Madhusudan 2009].

6.1     Recursive Programs
Let us ﬁx a ﬁnite set of variables V = {v 1 , . . . , vr } and a ﬁnite set of method names/identiﬁers M.
Let m 0 ∈ M be a designated “main” method. Let us also ﬁx a permutation hv 1 , . . . , vr i of variables
and denote it by hV i.
   For technical simplicity and without loss of generality, we will assume that for each method m ∈
M, the set of local variables is exactly the set V ; methods can, however, ignore certain variables if
they use fewer local variables. We will also assume that each method always gets called with all the
r variables, thereby initializing all local variables. This also does not lead to any loss in generality—
if a constant c is used2 in some function call, the caller can pass this constant to the called function,
which will use the passed parameter to initialize its local copy of the variable reserved for c. Finally,
we will assume that when a method m is invoked, the order of the parameters is ﬁxed to be hV i.
This again does not lead to a loss of generality — the caller can rearrange the variables to the
right order (by swapping) and then reassign them after m returns. These conventions simplify the
exposition considerably. We will, however, allow functions to return multiple values back, and
allow the caller to assign these to local variables on return.
   For every method m, let us ﬁx a tuple om of output variables over V . We require the output
variables in om to be distinct (in order to avoid implicit aliasing that can be caused when variables
are repeated).
   The syntax of recursive programs now has method deﬁnitions, where the body of the methods
can also include recursive calls, besides the usual assignment, sequencing, conditionals and loops.
hpдmi ::= m ⇒ om hstmti | hpдmi hpдmi
hstmti ::= skip | x := y | x := f (z) | assume (hcondi) | hstmti ; hstmti
              | if (hcondi) then hstmti else hstmti | while (hcondi) hstmti | w := m(hV i)
hcondi ::= x = y | x , y
 Here, m is a method in M, and the variables x, y, z, w belong to V . The length of the vector w
must of course match the length of the vector om of output parameters of the called method m. A
2 Recall that, we model constants as initial values of certain variables.



Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                            46:23

                          m 0 ⇒ hbi {
                              assume(T , F);
                              d := key(x);
                              if(d = k) then {
                                 b := T;
                              }
                                 else {
                                  y := x;
                                  x := left(x);
                                  b := m 0 (x, k, b, d, y, T, F);
                                  if(b = F) then {
                                    x := right(x);
                                    b := m 0 (x, k, b, d, y, T, F);
                                  }
                              }
                          }

                           Fig. 3. Example of uninterpreted recursive program.


program consists of a deﬁnition for each method m ∈ M, and we assume each method is deﬁned
exactly once.
Example 7. The example in Figure 3 illustrates a recursive program with a single method m 0 . This
program checks whether any node reachable from x using left and right pointers (which deﬁnes
a directed acyclic graph) contains a node with key k. The method returns a single value—value of
the variable b upon return. The variables x and k are the true parameters, but we additionally
augment the other variables b,d,y,T,F for simplifying notations and have the method rewrite
those variables as described before. Here T and F are variables storing the constants true and
false, respectively. Notice that, it is hard to ﬁnd an iterative program with a bounded number of
variables and without recursive functions that achieves the same functionality.
  The semantics of recursive programs given by the grammar hpдmi is a standard call-by-value
semantics. We next deﬁne the formal semantics using terms over a data model.

6.2   Executions
Executions of recursive programs over the ﬁnite set of variables V and the ﬁnite set of methods
M are sequences over the alphabet Π M = {“x := y”, “x := f (z)”, “assume(x = y)”, “assume(x ,
y)”, “call m”, “w := return” | x, y, z, w are in V , m ∈ M }.
   We will, in fact, treat the above alphabet as partitioned into three kinds: a call-alphabet, a return-
alphabet, and an internal-alphabet. The letters of the form “call m” belong to the call-alphabet, the
letters of the form “z := return” belong to the return alphabet, and the remaining letters belong
to the internal alphabet.
   The collection of all executions, denoted Exec, is given by the following context-free grammar
with start variable E.
E →“x := y” | “x := f (z)” | “assume(x = y)” | “assume(x , y)”
      | “call m” · E · “w := return” | E · E
  In the above rule, m ranges over M. Furthermore, with respect to the call-return-internal alpha-
bet deﬁned above, the above deﬁnes a visibly pushdown language.

                            Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:24                                         Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

Deﬁnition 11 (Complete and Partial Executions of a recursive program). Complete executions of
recursive programs that manipulate a set of variables V are sequences over Π M and are deﬁned
as follows. Let P be a recursive program. For each method m ∈ M, we denote by s(m) the body
(written over the grammar hstmti) in the deﬁnition of m.
   Consider a grammar where we have nonterminals of the form Ss , for various statements s ∈
hstmti, where the rules of the grammar are as follows.




                           Sϵ     →   ϵ
                    S skip ; s    →   Ss
                    S x :=y ; s   →   “x := y” · Ss
                S x :=f (z) ; s   →   “x := f (z)” · Ss
             S assume(c) ; s      →   “assume(c)” · Ss
 S if (c) then s1 else s2 ; s     →   “assume(c)” · Ss1 ; s | “assume(¬c)” · Ss2 ; s
          S while (c){s1 } ; s    →   “assume(c)” · Ss1 ; while (c){s1 } ; s | “assume(¬c)” · Ss
            S w:=m(hV i) ; s      →   “call m” · Ss(m) · “z := return” · Ss



The set of executions of a program P ∈ hpдmi, Exec(P) are those accepted by the above grammar
with start symbol Ss(m0 ) ; ϵ , where s(m 0 ) is the body of the “main” method m 0 . The set of partial
executions, denoted by PExec(P), is the set of preﬁxes of complete executions in Exec(P).


   In the above deﬁnition, the grammar for the language Exec(P) is taken to be the one that
can be deﬁned by using the minimal set of nonterminals for the deﬁnitions Ss(m) ; ϵ , where m ∈
M. It is easy to see that this is a ﬁnite set of nonterminals, and hence the above grammar is a
context-free grammar. In fact, all productions rules except the one involving method calls (i.e.,
production rules for non-terminals of the form S w:=m(hV i) ; s ) are right-regular grammar produc-
tions. Further, the production rules for method calls have a call-letter and return-letter guarding
the ﬁrst nonterminal. Therefore, it is easy to see that the above deﬁnes a visibly pushdown lan-
guage [Alur and Madhusudan 2009]. A visibly pushdown automaton (VPA) that is at most qua-
dratic in the size of the program accepts this language as follows. This VPA will have states of the
form Ssm and mimic the right-regular grammar productions using internal transitions generating
the associated terminal, and the rule for method calls by pushing the nonterminal to execute after
return onto the stack, and recovering it in its state after the pop when simulating the return from
the method call. This construction is fairly standard and simple, and we omit formal deﬁnitions.


6.3 Semantics of Recursive Programs and The Verification Problem
Terms Computed by an Execution
Let us now deﬁne the term computed for any (local) variable at any point in the computation. We
say a subword σ of an execution is matched if σ has an equal number of call-letters and return-
letters.
   We now deﬁne the terms that correspond to local variables in scope after a partial execution ρ.


Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                       46:25

Deﬁnition 12. We deﬁne Comp : Exec × V → Terms inductively as follows
                              Comp(ϵ, x)     = b
                                               x
                Comp(ρ · “x := y”, x)        = Comp(ρ, y)
               Comp(ρ · “x := y”, x ′)       = Comp(ρ, x ′)                            x′ , x
          Comp(ρ · “x := f (z)”, x)          = f (Comp(ρ, z 1 ), . . . , Comp(ρ, zr )) z = (z 1 , . . . , zr )
         Comp(ρ · “x := f (z)”, x ′)         = Comp(ρ, x ′)                            x′ , x
    Comp(ρ · “assume(R(z))”, x)              = Comp(ρ, x)
                Comp(ρ · “call m”, x)        = Comp(ρ, x)
 Comp(ρ · “call m” · ρ ′                                                  ′
    ·“hw 1 , . . . w r i := return”, w i )   = Comp(ρ · “callm” · ρ , om [i])                    ρ ′ is matched
 Comp(ρ · “call m” · ρ ′                                                                          x < {w 1 , . . . w r },
      ·“hw 1 , . . . w r i := return”, x)    = Comp(ρ, x)                                            ρ ′ is matched
                                                                                  Ð
  The set of terms computed by an execution ρ is Terms(ρ) =                                      Comp(ρ ′, v).
                                                                          ρ ′ is a preﬁx of ρ,
                                                                                  v ∈V

Semantics of Recursive Programs
Semantics of programs are, again, with respect to a data-model. We deﬁne the maps α and β
that collect the assumptions of equality and disequality on terms, as we did for programs without
function calls; we skip the formal deﬁnition as it is the natural extension to executions of recursive
programs, ignoring the call and return letters. An execution is feasible on a data model if these
assumptions on terms are satisﬁed in the model.

Verification Problem
As before, without loss of generality we can assume that the post condition is ⊥ (false). The veriﬁ-
cation problem is then: given a program P, determine if there is some (complete) execution ρ and
data model M such that ρ is feasible on M.

Coherence
The notion of coherence is similar to the one for non-recursive programs and their executions. In
fact, it is precisely the deﬁnition of coherence for regular programs (Deﬁnition 5), except for the
fact that it uses the new deﬁnitions of Comp, and α for recursive programs. We skip repeating the
deﬁnition. Note that, in this case, the memoizing condition and the early assumes condition are
based on the set Terms(σ ) (where σ is a partial execution), which also includes all terms computed
before, including those by other methods. A recursive program is said to be coherent if all its
executions are coherent.
   We can now state our main theorems for recursive programs.
Theorem 17. The veriﬁcation problem for coherent recursive programs is decidable, and is Exptime-
complete.                                                                                      
   The proof of the above result proceeds by constructing a VPA A P that accepts the executions of
the program P and a VPA Arfs that accepts feasible executions of recursive programs, and checking
if L(A P ∩ L(Arfs )) is empty, the latter being a decidable problem.
   The automaton Arfs is designed similar to the automaton Afs constructed in Section 3.2. Below,
we sketch the primary ideas for handling the extension to recursive program executions.
   Proof Sketch. Recall that the automaton for nonrecursive program executions keeps track of
(a) an equivalence relation ≡ over the variables V , (b) partial maps for each k-ary function that map

                              Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:26                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

from (V /≡)k to V /≡, and (c) a set of disequalities over the equivalence classes of ≡. The automaton
Arfs will keep a similar state, except that it would keep this over double the number of variables
V ∪ V ′ , where V ′ = {v ′ | v ∈ V }. The variables in V ′ correspond to terms in the caller at the time
of the call, and these variables do not get reassigned till the current method returns to its caller.
   When the automaton sees a symbol of the form “call m”, it pushes the current state of the
automaton on the stack, and moves to a state that has only the equivalence classes of the current
V variables (along with the partial functions and disequalities restricted to them). It also makes
each v ′ equivalent to v. When processing assignments, assumes, etc. in the called method, the
variables V ′ will never be reassigned, and hence the terms corresponding to them will not be
dropped. At the end of the method, when we return to the caller reading a symbol of the form
“w := return”, we pop the state from the stack and merge it with the current state.
   This merging essentially recovers the equivalence classes on variables that were not changed
across the call and sets up relationship (equivalence, partial f -maps, etc.) to the variables w as-
signed by the return. This is done as follows. Let the state popped be s ′ and the current state be s.
Let us relabel variables in s ′, relabeling each v ∈ V to v and each v ′ ∈ V to v ′. Let V = {v | v ∈ V }
and V ′ = {v ′ | v ′ ∈ V ′ }. Now let us take the union of the two states s and s ′ (inheriting equiv-
alence classes, partial function maps, disequalities), to get s ⊕ s ′ over variables V ′ ∪ V ∪ V ′ ∪ V .
In this structure, we merge (identify) each node v with v ′, retaining its label as v ′. Merging can
cause equivalence classes to merge, thereby also updating partial function interpretations and dis-
equalities. We now drop the variables V ′, dropping the equivalence classes if they become empty.
The new state is over V ′ ∪ V , and we relabel the variables v ′ to v ′ to obtain the actual state we
transition to. The f -maps and set of disequalities get updated across these manipulations.
   The resulting VPA has exponentially many states in |V | and taking its intersection with the
automaton A P and checking emptiness clearly can be done in exponential time. The lower bound
follows from the fact that checking reachability in recursive Boolean programs is already Exptime-
hard and the fact that we can emulate any recursive Boolean program using a recursive uninter-
preted program (even with an empty signature of functions).                                            
   We can also extend the notion of k-coherence to executions of recursive programs; here we
allow executions to have ghost assignments at any point to local (write-only) ghost variables in
scope, in order to make an execution coherent. We can build an automaton, again a VPA, that
accepts all k-coherent executions that are semantically feasible. Then, given a program P and a
k ∈ N, we can build an automaton that accepts all coherent extensions of executions of P, and also
check whether every execution of P has at least one equivalent coherent execution. If this is true,
then P is k-coherent, and we can check whether the automaton accepts any word to verify P.
Theorem 18. The problem of checking, given a program P and k ∈ N, whether P is k-coherent is
decidable. And if P is found to be k-coherent, veriﬁcation of P is decidable.

7 RELATED WORK
The class of programs (with and without recursion) over a ﬁnite set of Boolean variables admits
a decidable veriﬁcation problem [Alur et al. 2005; Esparza et al. 2000; Esparza and Knoop 1999;
Godefroid and Yannakakis 2013; Schwoon 2002]. As mentioned in the introduction, we believe
that our work is the ﬁrst natural class of programs that work over inﬁnite data domains and also
admits decidability for the veriﬁcation problem, without any severe restrictions on the structure
of programs.
   There are several automata-theoretic decidability results that could be interpreted as decidabil-
ity results for programs—for example, coverability and reachability in (unsafe) Petri nets are de-
cidable [Karp and Miller 1969; Kosaraju 1982; Mayr 1981], and this can be interpreted as a class

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                           46:27

of programs with counters with increments, decrements, and checks for positivity (but no checks
for zero), which is arguably not a very natural class of programs. The work in [Godoy and Tiwari
2009] establishes decidability of checking equality assertions in uninterpreted Sloopy programs
with restricted control ﬂow—such programs disallow the use of conditionals, loops and recursive
calls inside other loops.
   Complete automatic veriﬁcation can be seen as doing both the task of ﬁnding inductive invari-
ants and validating veriﬁcation conditions corresponding to the various iteration/recursion-free
snippets. In this light, there is classical work for certain domains like aﬃne programs, where certain
static analyses techniques promise to always ﬁnd an invariant, if there exists one that can be ex-
pressed in a particular logic [Granger 1991; Karr 1976; Müller-Olm and Seidl 2004; Müller-Olm and Seidl
2005]. However, these results do not imply decidable veriﬁcation for these programs, as there are
programs in these classes that are correct but do not have inductive invariants that fall in the
fragment of logic considered.
   There is a line of work that takes an automata-theoretic ﬂavor to veriﬁcation [Farzan et al. 2014,
2015; Heizmann et al. 2010, 2013], which rely on building automata accepting infeasible program
traces, obtained by generalizing counterexample traces that can be proved infeasible through SMT
solving. The method succeeds when it can prove that the set of traces of the program that are erro-
neous, are contained in the constructed set of infeasible traces. The technique can handle several
background theories, but of course tackles an undecidable problem. Our work relates to this line
of work and can be interpreted as a technique for providing, directly and precisely, the set of in-
feasible coherent traces as a regular/visibly-pushdown language, and thereby providing decidable
veriﬁcation for programs with coherent traces. Combining our techniques for uninterpreted traces
with the techniques above for other theories seems a promising future direction.
   The theory of uninterpreted functions is a fragment of ﬁrst order logic with decidable quantiﬁer
free fragment [Bradley and Manna 2007], and has been used popularly in abstract domains in pro-
gram analysis [Alpern et al. 1988; Gulwani and Necula 2004a,b], veriﬁcation of hardware [Bryant et al.
2001; Burch and Dill 1994] and software [Gulwani and Tiwari 2006; Lopes and Monteiro 2016].
   The notion of memoizing executions, which is an integral part of our coherence and k-coherence
deﬁnitions, is closely related to bounded path-width [Robertson and Seymour 1983]. We can think
of a computation of the program as sweeping the initial model using a window of terms deﬁned
by the set of program variables. The memoizing condition essentially says that the set of windows
that contain a term must be a contiguous set; i.e., a term computed should not be “dropped” if
it will recomputed. The notion of bounded path-width and the related notion of bounded tree-
width have been exploited recently in many papers to provide decidability results in veriﬁca-
tion [Chatterjee et al. 2016, 2015].

8   CONCLUSIONS
We have proved that the class of coherent programs and k-coherent programs (for any k ∈ N)
admit decidable veriﬁcation problems. Checking whether programs are coherent or k-coherent
for a given k is also decidable. Moreover, the decision procedure is not very expensive, and in fact
matches the complexity of verifying the weaker class of Boolean programs over the same number
of variables.
   Our results lay foundational theorems for decidable reasoning of uninterpreted programs, and
open up a research direction exploring problems that can be tackled using uninterpreted function-
s/relations. There are several avenues for applications that we foresee. One is reasoning about pro-
grams using uninterpreted abstractions, as in the work on reasoning with containers [Dillig et al.
2011] and modeling pointers in heap manipulating programs[Löding et al. 2017; Pek et al. 2014;
Qiu et al. 2013]. Such applications will likely call for an extension of our results to handle axioms

                           Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:28                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

that restrict the uninterpreted functions (such as associativity and commutativity of certain func-
tions) or to incorporate ﬁrst order theories such as arithmetic and sets. Speciﬁcations for heap
manipulating programs often involve recursive deﬁnitions, and this may require enriching our re-
sults to incorporate such deﬁnitions. We also conjecture that our results can be useful in domains
such as veriﬁcation of compiler transformations (such as instruction reordering), when proofs of
correctness of transformations rely only on a few assumptions on the semantics of operations
and library functions. Trace abstraction based veriﬁcation approaches [Farzan et al. 2014, 2015;
Heizmann et al. 2009, 2010] build automata that capture infeasible traces incompletely using a
counter-example guided approach. In this context, our results would enrich such automata—we
can accept precisely the set of infeasible traces that become infeasible when making functions un-
interpreted. This is a possible direction to combine with other background theories in veriﬁcation
applications.




Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                                       46:29

A PROOFS FROM SECTION 3.2
A.1 Proof of Lemma 3
  Proof. This follows trivially from the observation that every preﬁx of a coherent execution is
coherent and thus has early assumes.                                                          

A.2      Proof of Lemma 4
     Proof. First let us argue that ∼s,s ′ is consistent with the term model. Consider (t 1 , t 2 ) ∈ W ×
W . First it is easy to see that since (≡W , DW , P) is consistent, we have that if t 1 ∼s,s ′ t 2 , then
Jt 1 K T(E ′) = Jt 2 K T(E ′ ) , where E ′ = E ∪ {(s, s ′)}. We now prove the reverse direction. Assume that
Jt 1 K T(E ′) = Jt 2 K T(E ′ ) . We will show that t 1 ∼s,s ′ t 2 by inducting on the step in the congruence
closure algorithm that adds (t 1 , t 2 ) in the congruence E ′ . In the base case, (w.l.o.g) t 1 ≡W s and
t 2 ≡W s ′ , in which case clearly we have t 1 ∼s,s ′ t 2 . In the inductive case, there is a k-ary function
f and terms u 11 , u 12 , . . . , u 1k and u 21 , u 22 , . . . u 2k with t 1 = f (u 11 , . . . , u 1k ) and t 2 = f (u 21 , . . . , u 2k ), and
we have that Ju 1i K T(E ′ ) = Ju 2i K T(E ′ ) for each 1 ≤ i ≤ k. Now, since W is super-term closed with
respect to W , E and (s, s ′), we have that there are terms v 11 , v 12, . . . , v 1k , v 21, . . . , v 2k ∈ W such that
u ij E v ij for all i, j. Now, by inductive hypothesis, v 1i ∼s,s ′ v 2i for all 1 ≤ i ≤ k. Further, consistency
ensures that P(f )([vi1]≡W , . . . , [vi1 ]≡W ) = [ti ]≡W for i ∈ {1, 2}. This means that our procedure for
constructing ∼s,s ′ will imply that t 1 ∼s,s ′ t 2 .
     The proof of consistency of DW         ′ and P ′ is rather straightforward and follows from the fact that

∼s,s ′ is an equivalence and that (≡W , DW , P) is consistent.                                                                                

A.3      Proof of Lemma 5
   Proof. We will assume that (t 1 , t 2 ) <E as otherwise the proof is straigtforward. Let E ′ = E ∪
{(t 1 , t 2 )}. We ﬁrst observe that for every (s, s ′) ∈E ′ \ E , we have that there are terms r , r ′ such
that s E r , s ′ E r ′, r is a superterm of t 1 and r ′ is a superterm of t 2 .
   Now, let us consider the case when (s, s ′) ∈E ′ ∩D. It follows from the previous paragraph and
because W is superterm closed that there are terms u, u ′ ∈ W such that u E s and u ′ E s ′ .
Also, since ∼t1,t2 is consistent with respect to (W , E ∪ {t 1 , t 2 }, D) (see Lemma 4), we must have
that u ∼t1,t2′ u ′ . Also since DW is consistent, we have ([u]W , [u ′ ]W ) ∈ DW . This proves the ﬁrst
direction.
   The other direction is more straightforward and follows from consistency of (≡W , DW , P) with
respect to (W , E, D) and that ∼t1,t2′ is consistent with respect to (W , E ∪ {t 1 , t 2 }, D) (from Lemma 4).
                                                                                                             

A.4      Proof of Lemma 6
   Proof. Direct consequence of consistency.                                                                                                

A.5 Proof of Lemma 7
  Proof. We will induct on the length of the execution ρ.
  Base case. In the base case ρ = ϵ and q ρ = q 0 . This execution is clearly feasible and q ρ , q reject .
Also, q ρ is trivially consistent with respect to ({Comp(ρ, x) | x ∈ V }, α(ρ), β(ρ)).
  Inductive case. Here, ρ = σ · a.
  LetTγ = Terms(γ ) be the set of terms computed by γ , where γ ∈ {ρ, σ }. Let Eγ = α(γ ), Dγ = β(γ )
and Wγ = {Comp(γ , v) | v ∈ V } ⊆ Tγ for γ ∈ {ρ, σ }. We have that Tσ ⊆ Tρ , E σ ⊆ E ρ and
Dσ ⊆ D ρ .

                                       Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:30                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

   If q σ = q reject , then q ρ = q reject . In this case, from the inductive hypothesis, we have that σ is
infeasible and thus Eσ ∩D σ , ∅. Since α(σ ) ⊆ α(ρ) and β(σ ) ⊆ β(ρ), we have that E ρ ∩D ρ , ∅
and thus ρ is also infeasible.
   Otherwise, let us assume that σ is feasible. Let q σ = (≡, d, P). and let q ρ = (≡′, d ′, P ′ ). Inductively,
q σ is consistent with respect to (Wσ , E σ , D σ ). Below, we prove that q ρ is consistent with respect
to (Wρ , E ρ , D ρ ). If d ′ is reﬂexive, then we will have q ρ = q reject instead.
   Depending upon what the letter a is, we have the following cases.
   (1) Case a is “x := y”.
        In this case, Tρ = Tσ , E ρ = E σ and D ρ = D σ and thus ρ is also feasible. We will assume that
        y , x (otherwise q ρ = q σ , which is consistent with respect to (Wρ , E ρ , D ρ )).
        Further, Comp(ρ, v) = Comp(σ , v) for all v , x and Comp(ρ, x) = Comp(σ , y).
        Since (≡, d, P) is consistent with respect to (Wσ , D σ , E σ ), we have that for every x 1 , x 2 ∈ V
        with (x 1 , x 2 ) ∈≡, JComp(σ , v 1 )K T(Eσ ) = JComp(σ , v 2 )K T(Eσ ) . Consider a pair (v 1, v 2 ) ∈≡′ .
        Now, if v 1 , x and v 2 , x, we have that (v 1, v 2 ) ∈≡, and thus JComp(ρ, v 1)K T(E ρ ) =
        JComp(ρ, v 2)K T(E ρ ) . Otherwise, assume without loss of generality that v 1 = x and v 2 , x. In
        this case we have (v 2 , y) ∈≡, and by consistency we have JComp(ρ, v 2)K T(E ρ ) = JComp(σ , v 2 )K T(Eσ ) =
        JComp(σ , y)K T(Eσ ) = JComp(ρ, x)K T(E ρ ) .
        The consistency of d ′ and P ′ follows from the consistency of q σ . Further, d ′ is irreﬂexive
        because d is irreﬂexive.
   (2) Case a is ‘x := f (z 1 , . . . zk )’ where k = arity(f ).
        Here, we have two cases:
      (a) Case P(f )([z 1 ]≡ , . . . , [zk ]≡ ) = [v]≡ is deﬁned.
           Here, if x ∈ [v]≡, then we have ≡′=≡, d ′ = d and P ′ = P. The resulting state is con-
           sistent with (Wρ , E ρ , D ρ ). This is because q σ is consistent with (Wσ , E σ , D σ ) and thus
           JComp(σ , x)K T(Eσ ) = JComp(σ , v)K T(Eσ ) and thus JComp(ρ, x)K T(E ρ ) = JComp(ρ, v)K T(E ρ ) .
           The consistency of d ′ and P ′ follows similarly.
           Otherwise, we have that x < [v]≡. The consistency of q ρ again follows from the facts that
           (a) q σ is consistent, (b) E σ = E ρ , (c) D σ = D ρ , and, (d) JComp(ρ, x)K T(E ρ ) = JComp(ρ, v)K T(E ρ ) .
      (b) Case P(f )([z 1 ]≡ , . . . , [zk ]≡ ) is undeﬁned
           In this case, since ρ is memoizing, it must be the case that there is no term t ∈ Tσ such
           that JtKEσ = Jf (t 1 , t 2 , . . . , tk )KEσ , where ti = Comp(σ , zi ). This, in conjuction with the
           facts that (a) E σ = E ρ , (b) D σ = D ρ , and (c) q σ is consistent with respect to (Wσ , E σ , D σ )
           ensures the consistency of q ρ .
        In both the above cases, feasibility of σ implies feasibility of ρ and this is also correctly
        reﬂected in d ′, which is not reﬂexive since d is irreﬂexive.
   (3) Case a is “assume (x = y)”.
        In this case, consistency follows from Lemma 4. Further, if ρ is infeasible, then d ′ is not
        reﬂexive (Lemma 5), in which case we set q ρ = q reject .
   (4) Case a is “assume (x , y)”.
        In this case Tσ = Tρ ,Wσ = Wρ , E σ = E ρ . Further, D ρ = D σ ∪ {(Comp(σ , x), Comp(σ , y))}.
        Also, ≡′=≡ and P ′ = P and we just have argue for the consistency of d ′ which is immediate
        from the fact that the new pair (c 1 , c 2 ) ∈ d ′ \ d (if it exists) is such that x ∈ c 1 and y ∈ c 2 for
        which we have the witness (Comp(ρ, x), Comp(ρ, y)) ∈ D ρ .
        If ρ is infeasible, then d ′ becomes irreﬂexive (Lemma 6)
                                                                                                                 




Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                 46:31

B APPENDIX: UNDECIDABILITY OF VERIFICATION PROBLEM
We show the proof of Theorem 11 that the veriﬁcation of (unrestricted) uninterpreted programs,
even without recursion, is undecidable. We do this through a reduction from the halting problem
for 2-counter machines to the veriﬁcation of uninterpreted programs. In fact, our proof shows that
veriﬁcation of uninterpreted programs with even two unary functions is undecidable.
   Let M = (Q, s, HALT, C 1 , C 2 , δ ) be a 2-counter Minsky machine such that Q is a ﬁnite set of states,
s ∈ Q is the start, HALT ∈ Q is a special state, C 1 and C 2 are counters, both of which take values
in N and δ : Q → {INC, DEC, CHECK} × {C 1 , C 2 } × Q is the deterministic transition function.
   Let Σ = (F , R, C) be a signature with R = C = ∅ and F = { f , д} where f and д are both unary
functions. We will deﬁne a program P M over Σ and an L= formula ϕ M such that M reaches HALT
starting from s iﬀ P M |= ϕ M .

Variables. We ﬁrst deﬁne the set of variables VM of the program. For every state q ∈ Q, we have
a variable x q , which will behave like constants—they will never occur on the left hand side of any
assignment statement of our program. We will also have a variable x curr that will keep track of the
current state of the machine in a run of the machine. We will have two variables y1 and y2 that will
correspond to the values of the values of counters C 1 and C 2 respectively in a run. We will have a
variable z which will correspond to the constant 0. Finally, we will also have two auxiliary (helper)
variables w 1 , w 2 , w 3 and w 4 . Thus, we have VM = {x q | q ∈ Q } ∪ {x curr, y1 , y2 , z, w 1 , w 2 , w 3 , w 4 }.

Statements. The ﬁrst few statements in P M correspond to initialization: x curr is initialized to x q0
and both y1 and y2 get initialized to z. Further we demand that all constants are diﬀerent from
each other: for every q , q ′ we demand that x q and x q ′ are unequal, and that z is diﬀerent from
any x q .




INIT:
       assume (x q , x q ′ )                                  (** for every q , q ′ **)
       assume (x q , z)                                             (** for every q**)
       assume (x curr := x s )
       assume (y1 := z)
       assume (y2 := z)




   The initialization block is followed by a while loop with the condition (x curr , x HALT ). The body
of the loop contains, one block (labelled BLOCKq ) for every for every q → (instr , Ci , q ′ ) ∈ δ . The
statements inside BLOCKq depend upon what instr is:


                                 Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:32                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

  (1) Case instr is INC or DEC:
      In this case the code block is
BLOCKq :
           if (x curr = x q ){
               w 1 := f (yi )
               w 2 := д(yi )
               w 3 := д(w 1 )
               w 4 := f (w 2 )
               assume (w 3 = yi )
               assume (w 4 = yi )
               hstmti
               x curr := x q ′
           }
      where hstmti is yi := f (yi ) if instr is INC and yi := д(yi ) if instr is DEC.
  (2) Case instr is CHECK:
      In this case the code block is
BLOCKq :
           if (x curr = x q ){
               assume (yi = z)
           }
                                   ∆
   Finally the speciﬁcation is ϕ M = (x curr , x HALT )
   The correctness of the reduction is captured by the following lemma
Lemma 19. M does not reach HALT iﬀ P M |= ϕ M .
   Proof. Before we begin the actual proof, we note that every complete execution of P M ends in
“assume(x curr = x HALT )”.
   Let us ﬁrst prove the forward direction: If M does not reach HALT, then P M |= ϕ M . Let’s say M
does not reach HALT. In this case, we show that no complete execution of P M is feasible (and thus
P M |= ϕ M ). Assume, on the contrary, that there is a complete execution σ which is also feasible.
As we noted before, σ ends in “assume(x curr = x HALT )”. We ﬁrst observe that σ is feasible in MN
where the universe is the set of natural numbers, z is interpreted as 0 and f and д are respectively
λi.i + 1 and λi.i − 1. Now, let INIT, BLOCKqi1 . . . BLOCKqik be the sequence of blocks taken in σ .
Since σ is feasible, it must be that in the last block BLOCKqik , x curr must be assigned to x HALT . Now,
consider the corresponding run ρ = s → qi 1 · · · qi k → HALT. It easily follows that ρ is a valid run
of M, contradicting our initial assumption that M does not reach HALT.
   Let us now prove the other direction (in a contrapositive manner): If M reaches HALT, then
P M 6 |= ϕ M . Consider the run ρ of M that reaches HALT. Then, ρ = qi 0 → qi 1 · · · qi k → HALT,
where qi 0 = s. We now construct a feasible complete execution σ of P M , which, as we noted
before, ends in “assume(x curr = x HALT )” (and thus P M 6 |= ϕ M ). The execution σ will essentially
mimic the run ρ of M, and is the sequence of statements generated by the sequence of blocks
INIT, BLOCKqi1 . . . BLOCKqik . Since ρ is a run of M, it follows that σ is feasible in the FO model MN ,
where the universe is the set of natural numbers, the constant z is interpreted as 0, f is interpreted
to be the function λi.i + 1 and д is the function λi.i − 1.                                             

Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                  46:33

B.1    Undecidability when programs executions have early-assumes but are not
       memoizing
We now give the main modiﬁcations of the above proof to adapt it to a proof of Theorem 12.
     We will continue to have an input variable that stands for the counter value 0, and f and д
deﬁned over it with f i (0) denoting the counter value i. Again, we would like to assert that for
each of the terms f i (0), д(f (f i (0))) = f i (0). The assumes that we executed in the previous proof
are not, however, early assumes.
     In order to ensure the above property of the model, we introduce a “fake” counter variable
c ∗ . The program always ensures, in every round of simulating the 2-CM one step, that c ∗ always
advances (i.e., we update c ∗ to f (c ∗ )), and we assure that c ∗ = д(f (c ∗ )) using an assume. We remove
the assumes that we did using the true counters c 1 and c 2 to ensure д is the inverse of f .
     Note that the counter c ∗ always stays ahead of the other counters, and hence the assumes it
makes are early.
     The second complication to deal with are the assumptions that c 1 and c 2 make when they check
for equality with 0. These again are not early assumes in the construction. We modify the manip-
ulation of the counter c ∗ so that at every point it computes r 1 (c ∗ ), r 2 (c ∗ ), s 1 (c ∗ ), and s 2 (c ∗ ). It also
assumes the ﬁrst two terms are equal and the second two terms are disequal. Furthermore, for 0 we
have the reverse; r 1 (0) , r 2 (0) and s 1 (0) = s 2 (0). These assumes are again early as c ∗ stays ahead
of the true computation. Now, when we want to simulate the check that c 1 is 0, we instead check
whether r 1 (c 1 ) , r 2 (0), and to check if c 1 is not 0, we check s 1 (c 1 ) , s 2 (c 1 ). Hence all assumes on
the real simulation are disequality assumes, and hence do not break the early assume requirement.
     The rest of the construction and proof is simple.



B.2    Undecidability when programs executions are memoizing but do not have
       early-assumes
We now give the main modiﬁcations of the main proof above to adapt it to a proof of Theorem 13.
In fact we will show programs with a single non-early assume already are undecidable to verify.
    We again model the counters on terms as above. However, we start with two variables x and y,
both representing 0.
    In every step, we simulate the counters c 1 and c 2 on terms constructed from x, as before, but
we make no assumes of equality. Consequently, the initial model on terms involving x would be a
“free” structure. Meanwhile, on y, we simulate a fake counter as before, that continually increases,
staying always ahead of the computation on x, and ensuring that д is the inverse of f on terms
involving y.
    The initial model will keep the two submodels from x and y disjoint.
    At the end of the computation (when we reach a ﬁnal state of the 2-CM machine), we do a single
assume x = y. This will collapse two models, and impose the structure the model on y had on the
free model on x. Hence the counters and simulation become a correct simulation.
    We again need to handle assumes that we need to make to check counters equality with 0. We
do this as follows. We have functions h 1 and h 2 that operate on the free model involving x, and in
particular we consider the terms of the form hn1 (x) and hn2 (x). These essentially are meant to keep
a copy of 0, i.e., x. The fact that these are equal to x will be enforced later when the models of x
and y merge. Every time we want to check if a counter c i is equal to x, we check instead whether
r (hi (0)) = r (c i ), where r is yet another function we introduce. The idea is that r will be identity
on these terms, but again that is assured later.


                                 Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:34                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

  Meanwhile, in y, we ensure that h 1 (y) = y and h 1 (y) = y and r is identity. When we ﬁnally
collapse the models with an assume that x and y are equal, it will impose the required structure
on the model of x, and hence the 0-equality tests will become correct.
  The above is the main idea of the construction; the rest of the construction and proof is straight-
forward.

ACKNOWLEDGMENTS
We gratefully acknowledge National Science Foundation for supporting Umang Mathur (grant NSF
CSR 1422798), P. Madhusudan (grants 1138994 and SHF 1527395) and Mahesh Viswanathan (grant
NSF CPS 1329991).

REFERENCES
B. Alpern, M. N. Wegman, and F. K. Zadeck. 1988. Detecting Equality of Variables in Programs. In Proceedings of the 15th
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’88). ACM, New York, NY, USA, 1–11.
    https://doi.org/10.1145/73560.73561
Rajeev Alur, Michael Benedikt, Kousha Etessami, Patrice Godefroid, Thomas Reps, and Mihalis Yannakakis.
    2005. Analysis of Recursive State Machines. ACM Trans. Program. Lang. Syst. 27, 4 (July 2005), 786–818.
    https://doi.org/10.1145/1075382.1075387
Rajeev Alur and P. Madhusudan. 2004. Visibly Pushdown Languages. In Proceedings of the Thirty-sixth Annual ACM Sympo-
    sium on Theory of Computing (STOC ’04). ACM, New York, NY, USA, 202–211. https://doi.org/10.1145/1007352.1007390
Rajeev Alur and P. Madhusudan. 2009. Adding Nesting Structure to Words. J. ACM 56, 3, Article 16 (May 2009), 43 pages.
    https://doi.org/10.1145/1516512.1516518
Aaron R. Bradley and Zohar Manna. 2007. The Calculus of Computation: Decision Procedures with Applications to Veriﬁcation.
    Springer-Verlag, Berlin, Heidelberg.
Randal E. Bryant, Steven German, and Miroslav N. Velev. 2001. Processor Veriﬁcation Using Eﬃcient Reductions of
    the Logic of Uninterpreted Functions to Propositional Logic. ACM Trans. Comput. Logic 2, 1 (Jan. 2001), 93–134.
    https://doi.org/10.1145/371282.371364
Jerry R. Burch and David L. Dill. 1994. Automatic Veriﬁcation of Pipelined Microprocessor Control. In Proceedings of
    the 6th International Conference on Computer Aided Veriﬁcation (CAV ’94). Springer-Verlag, London, UK, UK, 68–80.
    http://dl.acm.org/citation.cfm?id=647763.735662
Krishnendu Chatterjee, Amir Kafshdar Goharshady, Rasmus Ibsen-Jensen, and Andreas Pavlogiannis. 2016. Algorithms
    for Algebraic Path Properties in Concurrent Systems of Constant Treewidth Components. In Proceedings of the 43rd
    Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’16). ACM, New York, NY,
    USA, 733–747. https://doi.org/10.1145/2837614.2837624
Krishnendu Chatterjee, Rasmus Ibsen-Jensen, Andreas Pavlogiannis, and Prateesh Goyal. 2015. Faster Algorithms for
    Algebraic Path Properties in Recursive State Machines with Constant Treewidth. In Proceedings of the 42Nd Annual
    ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’15). ACM, New York, NY, USA,
    97–109. https://doi.org/10.1145/2676726.2676979
Professor Bruno Courcelle and Dr Joost Engelfriet. 2012. Graph Structure and Monadic Second-Order Logic: A Language-
    Theoretic Approach (1st ed.). Cambridge University Press, New York, NY, USA.
Isil Dillig, Thomas Dillig, and Alex Aiken. 2011. Precise Reasoning for Programs Using Containers. In Proceedings of the
    38th Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’11). ACM, New York,
    NY, USA, 187–200. https://doi.org/10.1145/1926385.1926407
Javier Esparza, David Hansel, Peter Rossmanith, and Stefan Schwoon. 2000. Eﬃcient Algorithms for Model Checking Push-
    down Systems. In Proceedings of the 12th International Conference on Computer Aided Veriﬁcation (CAV ’00). Springer-
    Verlag, London, UK, UK, 232–247. http://dl.acm.org/citation.cfm?id=647769.734087
Javier Esparza and Jens Knoop. 1999. An Automata-Theoretic Approach to Interprocedural Data-Flow Analysis. In Foun-
    dations of Software Science and Computation Structures, Wolfgang Thomas (Ed.). Springer Berlin Heidelberg, Berlin,
    Heidelberg, 14–30.
Azadeh Farzan, Zachary Kincaid, and Andreas Podelski. 2014. Proofs That Count. In Proceedings of the 41st ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’14). ACM, New York, NY, USA, 151–164.
    https://doi.org/10.1145/2535838.2535885
Azadeh Farzan, Zachary Kincaid, and Andreas Podelski. 2015. Proof Spaces for Unbounded Parallelism. In Proceedings of
    the 42Nd Annual ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’15). ACM, New
    York, NY, USA, 407–420. https://doi.org/10.1145/2676726.2677012


Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
Decidable Verification of Uninterpreted Programs                                                                      46:35

Patrice Godefroid and Mihalis Yannakakis. 2013. Analysis of Boolean Programs. In Proceedings of the 19th International
   Conference on Tools and Algorithms for the Construction and Analysis of Systems (TACAS’13). Springer-Verlag, Berlin,
   Heidelberg, 214–229. https://doi.org/10.1007/978-3-642-36742-7_16
Guillem Godoy and Ashish Tiwari. 2009. Invariant Checking for Programs with Procedure Calls. In Proceedings
   of the 16th International Symposium on Static Analysis (SAS ’09). Springer-Verlag, Berlin, Heidelberg, 326–342.
   https://doi.org/10.1007/978-3-642-03237-0_22
Philippe Granger. 1991. Static Analysis of Linear Congruence Equalities Among Variables of a Program. In Proceedings
   of the International Joint Conference on Theory and Practice of Software Development on Colloquium on Trees in Alge-
   bra and Programming (CAAP ’91): Vol 1 (TAPSOFT ’91). Springer-Verlag New York, Inc., New York, NY, USA, 169–192.
   http://dl.acm.org/citation.cfm?id=111310.111320
Sumit Gulwani and George C. Necula. 2004a. Global Value Numbering Using Random Interpretation. In Proceedings of the
   31st ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’04). ACM, New York, NY, USA,
   342–352. https://doi.org/10.1145/964001.964030
Sumit Gulwani and George C Necula. 2004b. A polynomial-time algorithm for global value numbering. In International
   Static Analysis Symposium. Springer, 212–227.
Sumit Gulwani and Ashish Tiwari. 2006. Assertion Checking over Combined Abstraction of Linear Arithmetic and Unin-
   terpreted Functions. In Proceedings of the 15th European Conference on Programming Languages and Systems (ESOP’06).
   Springer-Verlag, Berlin, Heidelberg, 279–293. https://doi.org/10.1007/11693024_19
Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2009. Reﬁnement of Trace Abstraction. In Proceed-
   ings of the 16th International Symposium on Static Analysis (SAS ’09). Springer-Verlag, Berlin, Heidelberg, 69–85.
   https://doi.org/10.1007/978-3-642-03237-0_7
Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2010. Nested Interpolants. In Proceedings of the 37th Annual
   ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’10). ACM, New York, NY, USA,
   471–482. https://doi.org/10.1145/1706299.1706353
Matthias Heizmann, Jochen Hoenicke, and Andreas Podelski. 2013. Software Model Checking for People Who Love Au-
   tomata. In Computer Aided Veriﬁcation, Natasha Sharygina and Helmut Veith (Eds.). Springer Berlin Heidelberg, Berlin,
   Heidelberg, 36–52.
Richard M. Karp and Raymond E. Miller. 1969. Parallel Program Schemata. J. Comput. Syst. Sci. 3, 2 (May 1969), 147–195.
   https://doi.org/10.1016/S0022-0000(69)80011-5
Michael Karr. 1976. Aﬃne Relationships Among Variables of a Program. Acta Inf. 6, 2 (June 1976), 133–151.
   https://doi.org/10.1007/BF00268497
S. Rao Kosaraju. 1982. Decidability of Reachability in Vector Addition Systems (Preliminary Version). In Proceedings
   of the Fourteenth Annual ACM Symposium on Theory of Computing (STOC ’82). ACM, New York, NY, USA, 267–281.
   https://doi.org/10.1145/800070.802201
Christof Löding, P. Madhusudan, and Lucas Peña. 2017. Foundations for Natural Proofs and Quantiﬁer Instantiation. Proc.
   ACM Program. Lang. 2, POPL, Article 10 (Dec. 2017), 30 pages. https://doi.org/10.1145/3158098
Nuno P. Lopes and José Monteiro. 2016. Automatic equivalence checking of programs with uninterpreted functions
   and integer arithmetic. International Journal on Software Tools for Technology Transfer 18, 4 (01 Aug 2016), 359–374.
   https://doi.org/10.1007/s10009-015-0366-1
P. Madhusudan and Gennaro Parlato. 2011. The Tree Width of Auxiliary Storage. In Proceedings of the 38th Annual ACM
   SIGPLAN-SIGACT Symposium on Principles of Programming Languages (POPL ’11). ACM, New York, NY, USA, 283–294.
   https://doi.org/10.1145/1926385.1926419
Ernst W. Mayr. 1981.         An Algorithm for the General Petri Net Reachability Problem. In Proceedings of the
   Thirteenth Annual ACM Symposium on Theory of Computing (STOC ’81). ACM, New York, NY, USA, 238–246.
   https://doi.org/10.1145/800076.802477
Markus Müller-Olm and Helmut Seidl. 2004. A Note on Karr’s Algorithm. In Automata, Languages and Programming,
   Josep Díaz, Juhani Karhumäki, Arto Lepistö, and Donald Sannella (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
   1016–1028.
Markus Müller-Olm and Helmut Seidl. 2005. A Generic Framework for Interprocedural Analysis of Numerical Properties. In
   Proceedings of the 12th International Conference on Static Analysis (SAS’05). Springer-Verlag, Berlin, Heidelberg, 235–250.
   https://doi.org/10.1007/11547662_17
Edgar Pek, Xiaokang Qiu, and P. Madhusudan. 2014. Natural Proofs for Data Structure Manipulation in C Using Separation
   Logic. In Proceedings of the 35th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI
   ’14). ACM, New York, NY, USA, 440–451. https://doi.org/10.1145/2594291.2594325
Xiaokang Qiu, Pranav Garg, Andrei Ştefănescu, and Parthasarathy Madhusudan. 2013. Natural Proofs for Structure, Data,
   and Separation. In Proceedings of the 34th ACM SIGPLAN Conference on Programming Language Design and Implemen-
   tation (PLDI ’13). ACM, New York, NY, USA, 231–242. https://doi.org/10.1145/2491956.2462169


                                  Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
46:36                                        Umang Mathur, P. Madhusudan, and Mahesh Viswanathan

Neil Robertson and Paul D Seymour. 1983. Graph minors. I. Excluding a forest. Journal of Combinatorial Theory, Series B
   35, 1 (1983), 39–61.
Stefan Schwoon. 2002.        Model-Checking Pushdown Systems.        Ph.D. Thesis. Technische Universität München.
   http://www.lsv.ens-cachan.fr/Publis/PAPERS/PDF/schwoon-phd02.pdf
D. Seese. 1991. The structure of the models of decidable monadic theories of graphs. Annals of Pure and Applied Logic 53,
   2 (1991), 169 – 195. https://doi.org/10.1016/0168-0072(91)90054-P




Proc. ACM Program. Lang., Vol. 3, No. POPL, Article 46. Publication date: January 2019.
