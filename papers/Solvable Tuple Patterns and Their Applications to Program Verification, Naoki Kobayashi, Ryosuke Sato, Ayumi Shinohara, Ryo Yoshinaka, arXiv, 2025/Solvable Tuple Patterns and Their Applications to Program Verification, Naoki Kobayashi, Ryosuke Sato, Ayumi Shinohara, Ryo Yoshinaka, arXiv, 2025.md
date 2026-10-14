                                                       Solvable Tuple Patterns and Their Applications
                                                                  to Program Verification
                                              Naoki Kobayashi∗                 Ryosuke Sato†                   Ayumi Shinohara‡                  Ryo Yoshinaka‡
                                                                                               May 27, 2026


                                                                                                    Abstract
                                                     Despite the recent progress of automated program verification techniques, fully automated
                                                 verification of programs manipulating recursive data structures remains a challenge. We in-
                                                 troduce solvable tuple patterns (STPs) and conjunctive STPs (CSTPs), novel formalisms for
arXiv:2508.20365v3 [cs.PL] 26 May 2026




                                                 expressing and inferring invariants between list-like recursive data structures. A distinguishing
                                                 feature of STPs is that they can be efficiently inferred from only a small number of positive
                                                 samples; no negative samples are required. After presenting properties and inference algorithms
                                                 of STPs and CSTPs, we show how to incorporate the CSTP inference into a CHC (Constrained
                                                 Horn Clauses) solver supporting list-like data structures, which serves as a uniform backend
                                                 for automated program verification tools. A CHC solver incorporating the (C)STP inference
                                                 has won the ADT-LIN category of CHC-COMP 2025 by a significant margin.


                                         1      Introduction
                                         1.1      Background
                                         Although a lot of progress has recently been made in automated program verification techniques,
                                         fully automated verification of programs involving algebraic data types (ADTs) such as lists and
                                         trees remains difficult. In the case of programs manipulating only integers, key invariants on loops
                                         and recursive functions can often be expressed by linear integer arithmetic, and good techniques
                                         (such as interpolants [27, 48] and counterexample-guided abstraction refinement [12]) for automat-
                                         ically finding them have been developed. In contrast, in the case of programs manipulating ADTs,
                                         key invariants often involve inductive predicates, which are difficult to find automatically.
                                             To see the difficulty of automated verification of programs involving ADTs, let us consider the
                                         following OCaml program:1
                                                 let rec reva l1 l2 = match l1 with [] -> l2 | x::l1’ -> reva l1’ (x::l2)
                                                 let main l1 l2 = assert(reva (reva l1 l2) [] = reva l2 l1)
                                         The function reva takes two lists l1 and l2 as arguments, and returns a list obtained by appending
                                         the reverse of l1 to l2 ; for instance, reva [1; 2] [3; 4] = [2; 1; 3; 4]. The function main takes two lists
                                         l1 and l2 and asserts that reva (reva l1 l2 ) [ ] = reva l2 l1 holds.
                                             Suppose we wish to prove that the assertion in the function main does not fail for any l1 and l2 .
                                         That amounts to proving the proposition:

                                                         ∀l1 , l2 , l3 , l4 , l5 . Reva(l1 , l2 , l3 ) ∧ Reva(l3 , [ ], l4 ) ∧ Reva(l2 , l1 , l5 ) ⇒ l4 = l5   (1)

                                         where Reva(l1 , l2 , l3 ) intuitively means that reva l1 l2 may return l3 ; it is defined as the least
                                         predicate that satisfies the following clauses:

                                                                             ∀l1 , l2 . Reva([ ], l2 , l2 ).                                                   (2)
                                             ∗ The University of Tokyo
                                             † Tokyo University of Agriculture and Technology
                                             ‡ Tohoku University
                                             1 This
                                                  example has been taken from https://github.com/chc-comp/chc-comp24-benchmarks/blob/main/
                                         ADT-LIA/chc-comp24-ADT-LIA-140.smt2.


                                                                                                          1
                            ∀x, l1′ , l2 , l3 . Reva(l1′ , x :: l2 , l3 ) ⇒ Reva(x :: l1′ , l2 , l3 ).             (3)

Equivalently, it suffices to prove that there exists a predicate Reva that satisfies all the three clauses
(1)–(3); in other words, it suffices to find an invariant Reva among the arguments and the return
value of reva that is strong enough to satisfy (1).
    Automatically proving the above property is non-trivial. One can easily see that directly trying
to prove (1) by induction on l1 , l2 , or l3 would get stuck. Unfold/fold transformations [54, 15, 5]
are often used for reasoning about relational properties (ones between multiple function calls, in
the above case), but they would not directly apply either, because the two recursive calls reva l1 l2
and reva l2 l1 induct over different variables. A reasonable way to prove (1) is to find a lemma
Reva(l1 , l2 , l3 ) ⇒ l1R l2 = l3 ,2 but how to automatically find such a lemma remains a challenge. In
fact, the satisfiability of the clauses (1)–(3) is an instance of the CHC satisfiability problem [7],
and there are various CHC solvers supporting ADTs [28, 40, 10, 67], but to our knowledge, none
of them (except the one proposed in this paper) can automatically find the model of Reva that
satisfies the clauses (1)–(3).

1.2     Our Approach
1.2.1    Solvable Tuple Patterns for Automated Invariant Discovery
To enable automated inference of invariant relations among list-like (functional) data structures
(like the relation l1R l2 = l3 above), we introduce the notion of solvable tuple patterns (STPs) and
conjunctive STPs (CSTPs), and apply a data-driven approach to infer them. A tuple pattern
is of the form (p1 , . . . , pn ), where pi consists of constants (representing elements of a sequence),
variables, concatenations, and the reverse operation. The pattern (p1 , . . . , pn ) represents the set
of all tuples of sequences obtained by instantiating the variables to sequences. For example, the
invariant on the relation Reva above is expressed as (l1 , l2 , l1R l2 ), where l1 and l2 are variables
representing sequences. The tuple pattern (l1 l2 , l2 l3 , l1 l2 l3 ) expresses the set of tuples (s1 , s2 , s3 )
where s1 and s2 are respectively a prefix and a suffix of s3 , and s1 and s2 overlap with each other
in s3 (as represented by l2 ); thus (ab, bcd, abcd)3 belongs to (l1 l2 , l2 l3 , l1 l2 l3 ), but (ab, d, abcd) does
not. The tuple patterns have been inspired from Angluin’s pattern language [3] (in fact, by using
a special symbol $, a tuple pattern (p1 , . . . , pn ) can be expressed as a pattern p1 $ · · · $pn ). Pattern
languages have a good property that they can be learned from only positive samples (in the sense
of Gold [22]), but dealing with them are computationally costly: even the membership problem
is NP-complete [2] and the inclusion is undecidable [52]. We thus introduce a subclass of tuple
patterns called solvable tuple patterns. As we discuss later, the solvable tuple patterns have several
pleasant properties:4 (i) like pattern languages, they can be learned from only positive samples; (ii)
there is a (non-deterministic) polynomial-time algorithm for inferring a solvable tuple pattern, given
positive samples; (iii) only a small number of positive samples are required for learning a solvable
tuple pattern (for example, to infer (l1 , l2 , l1R l2 ), only two samples: (ab, cd, bacd) and (bc, da, cbda)
are sufficient); and (iv) the satisfiability of quantifier-free formulas consisting of word equations and
membership constraints on solvable patterns is decidable. Both of the patterns (l1 , l2 , l1R l2 ) and
(l1 l2 , l2 l3 , l1 l2 l3 ) above belong to the class of solvable patterns.
     The learnability from only positive samples is attractive in the context of program verification.
Positive samples (such as input/output pairs of a function, and states at the beginning of a loop) can
be easily collected by random executions of a program. In contrast, negative samples (states that
would lead to errors) are also required by many of the recent data-driven approaches to invariant
discovery for automated program verification [21, 9, 74, 75], but collecting negative samples is often
harder, since it requires backward executions of a program. Some of the approaches require even
“implication constraints” [21, 9, 20].
     To apply STPs to automated verification of list-manipulating programs, we consider CHCs on
words, which are Horn clauses extended with word equality/inequality constraints. The clauses on
Reva above may be considered CHCs on words, by viewing lists as words. We show (i) given a
set of CHCs on words consisting of definite clauses, there exists an algorithm to compute the least
   2 Here, we identify lists with sequences. We write lR for the reverse of l , and l l for the concatenation of two
                                                        1                     1       1 2
sequences (or lists) l1 and l2 .
   3 Here, we denote elements by letters.
   4 The definition of solvability and the precise meaning of the properties (i)–(iv) will be given later in Section 3.




                                                                2
model describable by conjunctive STPs (i.e., a conjunction of a finite number of STPs),5 and (ii)
it is decidable whether a given system of CHCs over words has a model describable by conjunctive
STPs. We can directly apply these results to the Reva example, and automatically obtain the
invariant: Reva(l1 , l2 , l3 ) ≡ l3 = l1R l2 .

1.2.2    Combination with Arithmetic Reasoning
Whilst CSTPs have attractive features as mentioned above, invariants expressed by CSTPs are
not always strong enough for the purpose of program verification, especially for programs using a
combination of lists and integers. For example, consider the following program.

let rec take n l =                                          let rec drop n l =
  if n=0 then [] else                                         if n=0 then l else
    match l with [] -> []                                       match l with [] -> []
      | x::l’ -> x::(take (n-1) l’)                               | _::l’ -> drop (n-1) l’

Given an integer n and a list l as arguments, the function take returns the list consisting of the
first (at most) n elements of l, and drop returns the list obtained by removing the first (at most)
n elements from l. Suppose we wish to prove that (take n l)@(drop n l) = l holds for every
(non-negative) integer n and list l (where @ denotes the list append function). By using solvable
tuple patterns, we can infer the properties that take n l and drop n l respectively return a prefix
and a suffix of l, but they are not strong enough to derive (take n l)@(drop n l) = l.
    To address the issue above, we combine STP inference with existing automated verification tools
(more specifically, CHC solvers over integer arithmetic [28, 40, 10]). For the example above, we
construct the following integer program by abstracting lists to their lengths.6

let rec take’ n l =                                         let rec drop’ n l =
  if n=0 then 0 else if l=0 then 0 else                       if n=0 then l else if l=0 then 0 else
    let l’=l-1 in 1+(take’ (n-1) l’)                            let l’=l-1 in drop’ (n-1) l’

Here, the second argument l of take’ and drop’ is an integer, representing the length of the second
argument of the original functions take and drop. We then try to prove that the abstract version
of the property: (take’ n l) + (drop’ n l) = l holds for all integers n and l. State-of-the-art CHC
solvers can quickly solve that verification problem, and can infer invariants like:

                           Take ′ (n, l, r) ≡ (l < n ∧ r = l) ∨ (l ≥ n ∧ r = n)
                           Drop ′ (n, l, r) ≡ (l < n ∧ r = 0) ∨ (l ≥ n ∧ r = l − n).

Here, Take ′ (Drop ′ , resp.) represents the relationship between the arguments n and l of take’
(drop’, resp.) and the return value r. By combining them with the output of solvable tuple
pattern inference, we obtain the invariant candidates:

               Take(n, l, r) ≡ ∃s.rs = l ∧ ((|l| < n ∧ |r| = |l|) ∨ (|l| ≥ n ∧ |r| = n))
               Drop(n, l, r) ≡ ∃s.sr = l ∧ ((|l| < n ∧ |r| = 0) ∨ (|l| ≥ n ∧ |r| = |l| − n)).

These are indeed invariants strong enough to satisfy Take(n, l, r1 ) ∧ Drop(n, l, r2 ) ⇒ r1 r2 = l.
    The above method is somewhat reminiscent of methods (such as Nelson-Oppen combination
procedure [51]) for deciding combinations of theories; indeed, it combines a method for reasoning
about lists (based on STP inference) with one for verifying integer programs. Various techniques
to combine static analyses have also been proposed [13, 25, 14]. To our knowledge, however, the
way we combine methods for solving problems in individual domains also seems novel.
   5 Stated without using the terminology of CHCs, this means that there exists an algorithm that, given a list-

manipulating program with loops and first-order recursive functions, computes the strongest inductive invariant
expressible in CSTPs, .
   6 As discussed in Section 5, we actually apply this kind of transformation to CHCs, rather than source programs.




                                                        3
1.3     Contributions and the Organization of This Paper
The contributions of this paper are summarized as follows.
    • Development of the theory and algorithms for solvable tuple patterns (STPs) and conjunctive
      STPs (CSTPs). To the best of our knowledge, the notions of STPs and CSTPs are novel
      and of independent interest even outside the context of automated program verification, for
      example in algorithmic learning theory.
    • Applications of solvable tuple patterns to automated verification of list-manipulating pro-
      grams.7 To this end, we introduce CHCs over words and show that it is decidable whether
      a given system of CHCs over words has a model describable by CSTPs. We also consider
      CHCs over multisets and sets, and show that it is decidable whether a given system of CHCs
      over multisets or sets has a model describable by the corresponding multiset or set version
      of CSTPs. We further propose a method to strengthen this approach by combining it with
      verification methods for integer-manipulating programs.

    • Implementation and experiments. Based on the results above, we implemented a new CHC
      solver called CHoCoL, which supports list-like data structures. We evaluated CHoCoL on
      the benchmark set of the CHC-COMP 2025 ADT-LIA category, and found that CHoCoL
      significantly outperformed other CHC solvers. A combination of CHoCoL with another
      solver called Catalia [36] won the CHC-COMP 2025 ADT-LIA category by a large margin.

   The rest of the paper is structured as follows. In Sections 2–4, we introduce the notion of solvable
tuple patterns (STPs) and conjunctive STPs (CSTPs), present algorithms for inferring them from
positive samples, and prove that the classes of STPs and CSTPs satisfy desired properties. Section 5
shows how to apply CSTPs to CHC solving (and hence also automated program verification).
Section 6 reports an implementation and experimental results. Section 7 discusses related work and
Section 8 concludes the paper.


2     Tuple Patterns and Inference Algorithm
In this section, we introduce the notions of tuple patterns and conjunctive tuple patterns, and provide
inference algorithms. In the next section, we will introduce a subclass of tuple patterns called
solvable tuple patterns as the sound and complete characterization of the class of tuple patterns
inferable by the algorithm.

2.1     Tuple Patterns and Conjunctive Tuple Patterns
Let Σ be a set of letters, and V a (countably infinite) set of variables. We assume that Σ contains
at least two distinct letters. For the purpose of representing a relation among lists, Σ is the set of
possible list elements; for example, if we consider integer lists, then we let Σ be the set of integers.
Below we often write a, b, c, . . . for elements of Σ. We write dom(f ) for the domain of a map f .
    The sets of tuple patterns and conjunctive tuple patterns, ranged over by t and γ respectively,
are defined by:

                            t (tuple patterns) ::= (p1 , . . . , pk )    p ∈ (Σ ∪ V)∗
                            γ (conjunctive tuple patterns) ::= t1 ∧ · · · ∧ tm .

A tuple pattern t = (p1 , . . . , pk ) represents a set of k-tuples of Σ-sequences, i.e., a k-ary relation
between sequences, obtained by replacing each variable with a sequence of letters in Σ. For example,
(x, y, xy) represents the set of triples of the form (s1 , s2 , s1 s2 ) where s1 , s2 ∈ Σ∗ . Formally, we
define L(t) ⊆ Σ∗ × · · · × Σ∗ as: {[s1 /x1 , . . . , sn /xn ]t | s1 , . . . , sn ∈ Σ∗ } where x1 , . . . , xn are the
variables occurring in t, and [s1 /x1 , . . . , sn /xn ] denotes the simultaneous substitution of s1 , . . . , sn
for x1 , . . . , xn . A conjunctive tuple pattern t1 ∧ · · · ∧ tm (where m ≥ 1) represents the intersection
   7 This paper targets programs manipulating functional (i.e., immutable) lists. Handling programs manipulating

mutable linked lists and other mutable data structures would require combining our method with other techniques [47];
see Remark 5.2.



                                                          4
of the sets of tuples represented by t1 , . . . , tm , as defined by: L(t1 ∧ · · · ∧ tm ) = L(t1 ) ∩ · · · ∩ L(tm ).
For example, (x, y, xz) ∧ (x, y, yz) represents the set of triples (s1 , s2 , s3 ) where both s1 and s2 are
prefixes of s3 ; here, note that variables are implicitly bound in each conjunct: the two occurrences
of z in (x, y, xz) and (x, y, yz) may be distinct. We write e· for a sequence. By abuse of notation, we
write pe for a sequence p1 , . . . , pn and also for a tuple pattern (p1 , . . . , pn ), depending on the context;
similarly for sequences x e and se of variables and strings respectively.
    We identify tuple patterns up to variable renaming. For example, we identify (xy, x) with (yx, y).
We write Vars(p) and Vars(t) for the sets of variables occurring in p and t respectively. We write
p1 · p2 for the concatenation of two patterns sequences p1 and p2 , and often omit ·, writing p1 p2 .
We write |p| for the length of a pattern p. For a tuple pattern t = (p1 , . . . , pk ), we write |t| and #t
respectively for k and |p1 · · · pk | + k.
    We will later (in Section 4) extend tuple patterns with the pattern xR (which represents the
reverse of x), to accommodate the Reva example in Section 1.
Remark 2.1. In the case of a singleton tuple pattern (p), our definition of L coincides with the
definition of a variation of pattern languages [3, 2] called E-pattern languages (or erasing pattern
languages) [63]. In the definition of original pattern languages [3, 2] (called NE-pattern languages),
L(p) = {[s1 /x1 , . . . , sn /xn ]p | s1 , . . . , sn ∈ Σ+ }; empty strings cannot be substituted for variables.
In view of the application to program verification discussed in Section 5, we allow substitutions of
empty strings, which correspond to empty lists.

2.2     Tuple Pattern Inference Problem
Learning data, denoted by M , is an m × n-matrix consisting of elements of Σ∗ . We write M [i][j]
for the element in the i-th row and j-th column. We also write M [i] for (M [i][1], . . . , M [i][n]), and
M [∗][j] for (M [1][j],P . . . , M [m][j]). We write shape(M ) for (m, n), rows(M ) for m, dim(M ) for n,
and size(M ) for i∈{1,...,m},j∈{1,...,n} (1 + |M [i][j]|), where |s| denotes the length of string s ∈ Σ∗ .
We sometimes regard learning data M as the set {M [1], . . . , M [m]}, and write M1 ⊆ M2 when M1
is a subset of M2 as sets.
     Let xe = (x1 , . . . , xk ) and t = (p1 , . . . , pn ). If shape(M ′ ) = (m, k) and Vars(t) ⊆ {e    x},
we write [M ′ /e     x]t for the learning data M such that shape(M           ) = (m, n) and  M  [i][j]  =
    ′                    ′                                      ′         a b
[M [i][1]/x1 , . . . , M [i][k]/xk ]pj . For example, if M =                     and t = (x, y, xy), then
                                                                       bb a
                        a b ab
[M ′ /(x, y)]t =                        . We use the metavariable Θ for a substitution [M/e x]. We some-
                        bb a bba
times use the matrix notation:                                         
                                               x1        ···       xk
                                             s1,1
                                                        ···      s1,k 
                                             ···        ···       ··· 
                                              sm,1       ···      sm,k
for the substitution [M/(x1 , . . . , xk )] such that M [i][j] = si,j .
    When Θt = M holds, we write M, Θ |= t. We also write M, Θ |=s t if Θt = M and there exists
no variable x such that Θ(x) = e       ϵ (i.e., if no variable is always mapped to ϵ). We write M |= t
(M |=s t, resp.) if there exists Θ such that M, Θ |= t (M, Θ |=s t, resp.), and we call Θ a witness
substitution for M |= t (M |=s t, resp.). For a conjunctive tuple pattern γ = t1 ∧ · · · ∧ tm , we write
M |= γ (M |=s γ, resp.) if M |= ti (M |=s ti , resp.) holds for every i ∈ {1, . . . , m}.
                                                                                                   
                                                                                                x
                                  a aaa
Example 2.1. Let M be:                           and t be (x, axx). Then M |=s t, where Θ =  a  is a
                                  b abb
                                                                                                  b
                                                                              
                                                                          x y
witness substitution. We also have M, Θ |= (x, axxy) for Θ =  a ϵ , but M ̸|=s (x, xxy) as Θ
                                                                          b ϵ
always maps y to ϵ.
                                                                                                     
                                                                                                x y
                                  a b ab
Example 2.2. Let M be:                              . Then, M |= (ax, y, axy). In fact, for Θ =  ϵ b ,
                                aa ϵ aa
                                                                                                  a ϵ

                                                         5
we have M, Θ |= (ax, y, axy). In this case, we also have M |=s (ax, y, axy), with the same witness
substitution.
   The tuple pattern inference problem is the problem of, given learning data M , finding a tuple
pattern (p1 , . . . , pn ) such that M |= (p1 , . . . , pn ). For instance, for M in Example 2.1, (x, axx) is
an answer to the inference problem.

2.3       Inference Algorithm
We now present a (non-deterministic) algorithm for tuple pattern inference. We formalize it by
using a rewriting relation (t, Θ) −→ (t′ , Θ′ ). Starting with the initial state (e     x, [M/e x]) (where
x
e = (x1 , . . . , xn )), the algorithm repeatedly applies the rewriting rules below until no further rule
is applicable. When the final pair is (t′ , Θ′ ), then t′ is the inferred tuple pattern. In other words,
given M , our algorithm for tuple pattern inference (non-deterministically) outputs t′ such that
(e
 x, [M/ex]) −→∗ (t′ , Θ′ ) −→. ̸    As we will see later (in Theorem 2.1), (e     x]) −→∗ (t′ , Θ′ ) implies
                                                                            x, [M/e
M, Θ |= t , because the rewriting relation (t, Θ) −→ (t , Θ ) maintains the invariant Θt = Θ′ t′ .
      ′     ′                                                 ′  ′


                            M [∗][i] ̸= e
                                        ϵ   M [∗][j] = M [∗][i] · se        x′j fresh
                                                                                                                 (R-Prefix)
    (t, [M/(x1 , . . . , xm )]) −→ ([xi xj /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])
                                         ′



                                 M [∗][j] = a · se        a∈Σ           x′j fresh
                                                                                                                 (R-CPrefix)
  (t, [M/(x1 , . . . , xm )]) −→ ([ax′j /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])

                            M [∗][i] ̸= e
                                        ϵ        M [∗][j] = se · M [∗][i]        x′j fresh
                                                                                                                      (R-Suffix)
      (t, [M/(x1 , . . . , xm )]) −→ ([x′j xi /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])

                                  M [∗][j] = se · a        a∈Σ          x′j fresh
                                                                                                                 (R-CSuffix)
   (t, [M/(x1 , . . . , xm )]) −→ ([x′j a/xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])

                                                      M [∗][j] = e ϵ
                                                                                                               (R-Epsilon)
                   (t, [M/(x1 , . . . , xm )]) −→ ([ϵ/xj ]t, [M ↑j /(x1 , . . . , xj−1 , xj+1 , . . . , xm )])

Here, M ↑j denotes the matrix obtained from M by removing the j-th column, and M {j 7→ se}
denotes the matrix obtained from M by replacing the j-th column with se. We write a · se for the
sequence obtained from se by appending a to the head of each element of se.
    The rule R-Prefix is for the case where the i-th column of M is a prefix of the j-th column. In
this case, we replace the j-th column with its suffix obtained by removing the prefix M [∗][i], and
instantiate xj in t accordingly to xi · x′j . The rule R-CPrefix is for the case where a constant a
is a prefix of the j-th column, and the rule R-Epsilon is for the case where every element of the
j-th column is an empty sequence. In the latter case, the j-th column is removed.
                                                                  
                                                            a aaa
Example 2.3. Recall the data in Example 2.1: M =                     . The pattern (x, axx) is inferred
                                                            b abb
(up to variable renaming) as follows.

                                                   x1 x′2                            x1 x′′2
                                                                                          
                 x1    x2                                                                   
    (x1 , x2 ),  a aaa  −→ (x1 , ax′2 ),  a aa  −→ (x1 , ax1 x′′2 ),  a               a 
                   b  abb                            b   bb                            b    b
                                 ′′′
                                                                
                           x1 x2                             x1   
   −→ (x1 , ax1 x1 x′′′
                     2 ),
                           a     ϵ  −→ (x1 , ax1 x1 ),  a  −→       ̸
                             b    ϵ                              b

Actually, the patterns such as (x1 , ax′2 ) and (x1 , ax1 x1 x′′′
                                                              2 ) obtained in intermediate steps are also
valid solutions of the inference problem, but the final pattern describes a smaller relation than
them.



                                                                 6
                                                                              
                                                                  a   b   ab
Example 2.4. Recall the data in Example 2.2: M =                                . The pattern (ax, y, axy)
                                                                 aa   ϵ   aa
is inferred (up to variable renaming) as follows.
                                                                                      x1 x2 x′3
                                                                                             
                    x1 x2 x3                                                                   
  (x1 , x2 , x3 ),  a       b ab  −→(R-Prefix, x = x x′ ) (x1 , x2 , x1 x′3 ),  a      b   b 
                                                                 3     1 3
                     aa      ϵ aa                                                     aa  ϵ   ϵ
                                                                           ′′
                                                                              
                                                              x1 x2 x3           
 −→ (R-Prefix, x′ = x x′′ ) (x1 , x2 , x1 x2 x′′3 ),  a              b    ϵ 
                        3     2 3
                                                               aa      ϵ   ϵ
                                                                   
                                                          x1  x 2    
 −→ (R-Epsilon, x′′ = e       ϵ)   (x1 , x 2 , x1 x 2 ),  a     b  
                          3
                                                           aa    ϵ
                                                               ′        
                                                               x1 x2       
 −→ (R-CPrefix, x = ax′ ) (ax′1 , x2 , ax′1 x2 ),  ϵ                  b  −→   ̸
                           1     1
                                                                  a    ϵ


    The following example shows that the result of tuple pattern inference may not be unique.
                                                             
                                               aa    a aac
Example 2.5. Consider the data: M =                             . Here, both the first and second
                                                b bb bbd.
columns are prefixes of the third column. We obtain (x, y, xz) or (x, y, yz) depending on which
column is chosen in R-Prefix.
                                                                                x′3
                                                                                 
                               x1 x2  x3                           x1 x2           
             (x1 , x2 , x3 ),  aa  a aac  −→ (x1 , x2 , x1 x′3 ),  aa    a     c 
                                 b bb bbd.                             b bb bd.

                                                                                        x′3
                                                                                         
                                 x1   x2    x3                           x1    x2          
               (x1 , x2 , x3 ),  aa    a   aac  −→ (x1 , x2 , x2 x′3 ),  aa     a    ac  .
                                   b   bb   bbd.                             b    bb    d.
The first pattern obtained describes that the first element is a prefix of the third element, while the
second pattern describes that the second element is a prefix of the third element. The conjunctive
pattern (x1 , x2 , x1 x′3 ) ∧ (x1 , x2 , x2 x′3 ) subsumes both patterns.
Definition 2.1 (Algorithms TPinf and CTPinf). We write TPinf for a non-deterministic algorithm
that takes data M as input, applies the rewriting rules to (e
                                                            x, [M/e
                                                                  x]) until no further rule is appli-
cable, and outputs some tuple pattern t such that (e x, [M/ex]) −→∗ (t, Θ) −↛  . We write CTPinf
for a deterministic algorithm that takes data M as input  and outputs the conjunctive tuple pattern
              x]) −→∗ (t, Θ) −→
V
  {t | (e
        x, [M/e               ̸ }.
    Note that the set of (t, Θ) such that (e     x]) −→∗ (t, Θ) −→
                                           x, [M/e               ̸  is finite; thus we can indeed
compute CTPinf(M ) by an exhaustive search. Note, however, that CTPinf runs in time exponential
in size(M ) in the worst case.
    We now state some key properties of the algorithm TPinf; other important properties are
discussed in Section 3. Proofs omitted below are found in Appendix A. The theorem below states
the soundness of the algorithm, which follows immediately from the fact that (t1 , Θ1 ) −→ (t2 , Θ2 )
implies Θ1 t1 = Θ2 t2 . See Appendix A for more details.
Theorem 2.1 (soundness). Suppose x   e = x1 , . . . , xn are mutually distinct variables and shape(M ) =
(m, n). If TPinf(M ) returns t, then M |= t.
   Our non-deterministic algorithm can find a pattern in time polynomial in the size of given data.
Theorem 2.2. Given M as input, TPinf runs in time polynomial in size(M ).
Proof. In each step of rewriting, an applicable rule can be found and applied in polynomial time, if
there is any. Since each step of the rewriting strictly decreases size(M ), the length of the rewriting
sequence is linear in size(M ).


                                                       7
3      Solvable Tuple Patterns
In this section, we introduce the notions of solvable tuple patterns (STPs) and conjunctive solvable
tuple patters (CSTPs), which characterize the classes of (conjunctive) tuple patterns that can be
inferred by our algorithms. The pattern (xx) on a singleton tuple is obviously non-inferable by
our algorithm, and it is indeed deemed non-solvable in the characterization below. In contrast, the
pattern (xx, x) is solvable.
Remark 3.1. Instead of restricting the class of tuple patterns, one may expect to obtain an
extension of the algorithm that can infer arbitrary tuple patterns. Unfortunately, learning arbitrary
tuple patterns from positive samples is computationally infeasible. As mentioned in Remark 2.1,
singleton tuple patterns coincide with E-patterns [63], and the full class of E-pattern languages is
not learnable from positive data in general (more precisely, it is not learnable when the alphabet
size is 2, 3, or 4 [58, 59] and the learnability is unknown when the alphabet size is larger). Also,
the inclusion problem is undecidable for both NE- and E-pattern languages [31, 52]. In contrast,
STPs have good algorithmic properties, as discussed in Section 3.4.

3.1      Solvability
We define the notion of solvability via a reduction relation t ⇝ t′ on tuple patterns. Just
as the rewriting relation (t, Θ) −→ (t′ , Θ′ ) in Section 2 detects prefix/suffix relationships
in data and simplifies the data accordingly, the reduction t ⇝ t′ detects prefix/suffix rela-
tionships in patterns and simplifies the patterns. The reduction relation ⇝ is defined by:
             pj = pi · p′j pi ̸= ϵ                          pj = p′j · pi pi ̸= ϵ
  (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )       (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )
                                                   (PR-Prefix)                                                               (PR-Suffix)
                     pj = a · p′j       a∈Σ                                                    pj = p′j · a       a∈Σ
  (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )
                                                                (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )
                                                (PR-CPrefix)                                                   (PR-CSuffix)
                                                                                           pj = ϵ
                                                                  (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , pj+1 , . . . , pn )
                                                                                                               (PR-Epsilon)
Each rule of name PR-xx corresponds to the rule R-xx; while the rule R-xx manipulates
data M , the rule PR-xx applies the corresponding operation to a tuple pattern, and simpli-
fies the pattern. We define the set Tk of k-ary solvable tuple patterns (STPs, for short)                                      S as:
{t | t ⇝∗ (x1 , . . . , xn ), |t| = k, and x1 , . . . , xn are distinct from each other}, and write T for k Tk .
In other words, a tuple pattern t is solvable if t can be reduced to a trivial pattern (x1 , . . . , xn ) con-
sisting of distinct variables. A conjunctive tuple pattern γ = t1 ∧· · ·∧tm is solvable if t1 , . . . , tm ∈ Tk
for some k. We call the pattern modified or removed in the rewriting (p1 , . . . , pn ) ⇝ (p′1 , . . . , p′m )
(i.e., pj in the above rules) a principal pattern. We also call the pattern pi in PR-Prefix or
PR-Suffix an auxiliary pattern.
Example 3.1. (x1 x2 , x2 x1 ) ̸∈ T2 , but (x1 x2 , x2 x1 , x1 ) ∈ T3 . In fact, (x1 x2 , x2 x1 ) ̸∈ T2 is obvious,
as no rule is applicable to (x1 x2 , x2 x1 ). The latter follows by:

                   (x1 x2 , x2 x1 , x1 ) ⇝ (x2 , x2 x1 , x1 ) ⇝ (x2 , x1 , x1 ) ⇝ (x2 , x1 , ϵ) ⇝ (x2 , x1 ),

where PR-Prefix is applied in the first three steps, and PR-Epsilon is applied in the last step.
Remark 3.2. In the definition of Tk , we can actually drop the requirement that the variables
x1 , . . . , xn are distinct from each other. Indeed, if x1 = x2 , for example, then we can erase x1 by:

                            (x1 , x1 , x3 , . . . , xn ) ⇝ (ϵ, x1 , x3 , . . . , xn ) ⇝ (x1 , x3 , . . . , xn ).

Thus, Tk does not change even if we do not require that x1 , . . . , xn are distinct from each other.
Remark 3.3. The name “solvable tuple patterns” comes from the following fact. Suppose t =
(p1 , . . . , pn ) ∈ Tn . Then, the general solution for a system of equations p1 = s1 , . . . , pn = sn can be
expressed by using (i) s1 , . . . , sn , ϵ, (ii) constants a ∈ Σ, (iii) the (partial) operation s\s′ , which is


                                                                        8
defined as s0 such that ss0 = s′ if s is a prefix of s′ , and (iv) the (partial) operation s′ /s, which is
defined as s0 such that s0 s = s′ if s is a suffix of s′ . For example, t = (x1 x2 , x2 x1 , x1 ) is solvable
in the sense that the system of equations x1 x2 = s1 , x2 x1 = s2 , x1 = s3 has a general solution
x1 = s3 , x2 = s3 \s1 provided (s3 \s1 )\s2 = s3 (or, equivalently (s3 \s1 ) · s3 = s2 ).
    As in the case of ordinary pattern languages, the class of languages described by solvable tuple
patterns (where a tuple pattern (p1 , . . . , pn ) is identified with the language described by p1 $ · · · $pn )
is incomparable with the class of context-free languages, but is subsumed by the class of indexed
languages [1]. Note that the language {w$ww | w ∈ {a, b}∗ }, described by the solvable tuple pattern
(x, xx), is not context-free.

3.2     Properties of the Inference Algorithm
As stated in the following theorems, the algorithms TPinf and CTPinf defined in Definition 2.1
indeed infer STPs and CSTPs, respectively. Moreover, modulo a minor condition, they are complete
for these classes.
Theorem 3.1 (inferred patterns are solvable). If TPinf(M ) returns t, then t ∈ T .
Theorem 3.2 (completeness of TPinf). Let x
                                         e = x1 , . . . , xn be mutually distinct variables.
  (I) If M |=s t and t ∈ Tn , (e     x]) −→∗ (t, Θ) for some Θ.8
                               x, [M/e
 (II) If M |= t and t ∈ Tn , then there exists t′ ∈ T such that L(t′ ) ⊆ L(t) and t′ is a possible
      output of TPinf(M ), i.e., (e     x]) −→∗ (t′ , Θ) −→
                                  x, [M/e                 ̸ .
   The following theorem, obtained as a corollary of Theorems 2.1 and 3.2, says that CTPinf(M )
returns the least CSTP γ such that M |= γ.
Theorem 3.3 (completeness of CTPinf). Let M be learning data. Then M |= CTPinf(M ), and
L(CTPinf(M )) ⊆ L(γ) for every CSTP γ such that M |= γ.
Remark 3.4. Theorem 3.2 (I) would not hold if the assumption M |=s t were weakened to M |=
t. In fact, let t = (x, x) and M = (ϵ ϵ). Then M |= t and t ∈ T2 , but we can only obtain
(ϵ, ϵ), (ϵ, x), (x, ϵ), (x, y) by rewriting. In fact, the only possible reduction sequences are:
                                                                   
                                      x1 x2                    x1                
                         (x1 , x2 ),              −→ (x1 , ϵ),            −→ (ϵ, ϵ),
                                        ϵ  ϵ                       ϵ
                                                                  
                                       x1 x2                      x2
                                                                                   
                         (x1 , x2 ),              −→ (ϵ, x2 ),            −→ (ϵ, ϵ),     .
                                        ϵ  ϵ                       ϵ
The rule R-Prefix is inapplicable because of the side condition M [∗][i] ̸= e
                                                                            ϵ. The pattern (x, x)
could be obtained if we removed the condition, but then we would obtain unboundedly many
patterns, such as (xxx, xx). If we add one more sample, like (a, a) to M above, then we can infer
(x, x) as expected.
   As observed in Example 2.5, the output of TPinf is not unique due to non-determinism (whereas
CTPinf is), but the following theorem states that TPinf always outputs a minimal solvable pattern.
Theorem 3.4 (minimality). Suppose TPinf(M ) returns t1 . If M |= t0 with t0 ∈ T , then L(t1 ) ⊇
L(t0 ) implies L(t1 ) = L(t0 ).
   The minimality property above is important for learning from positive samples only. Sup-
pose that we are trying to learn the language described by a tuple pattern t0 . In learning from
positive samples, we are given data M consisting of only a (finite) subset of L(t0 ). Thus, our
non-deterministic algorithm may output a “wrong” pattern t1 such that M |= t1 but L(t1 ) ̸= L(t0 ).
Thanks to the theorem above, in such a case, there exists data se ∈ L(t0 ) \ L(t1 ). Thus, by adding
the new positive sample se to M and running our algorithm again, the wrong pattern t1 will not be
encountered again. Without the minimality property, it could be the case L(t1 ) ⊊ L(t0 ), and then
the pattern t1 would not be refutable with only positive samples.
   For each STP t, there exist polynomial-size data that uniquely characterize t. This property
ensures convergence of the learning process (cf. Theorem 3.6).
  8 Recall that tuple patterns are identified up to variable renaming.




                                                         9
Theorem 3.5 (Characteristic Data). Let t = (p1 , . . . , pn ) be an STP such that |p1 · · · pn | = m.
Then, there exists M such that (i) size(M ) = O((m + n) log n), (ii) for any M ′ such that M ⊆
M ′ ⊆ L(t), there exists Θ such that (e
                                      x, [M ′ /e
                                               x]) −→∗ (t, Θ) −↛  , and (iii) for any M ′ such that
        ′               ′       ∗   ′   ′
M ⊆ M ⊆ L(t), (e          x]) −→ (t , Θ ) −→
                   x, [M /e                ̸     implies L(t) = L(t′ ). Furthermore, given t, M can
be constructed in polynomial time.

3.3     Learnability
We have so far considered an algorithm for inferring t (γ, resp.) such that M |= t (M |= γ, resp.),
given M . In the whole learning process, we need to repeatedly invoke the algorithm for gradually
increasing learning data M0 ⊂ M1 ⊂ M2 ⊂ · · ·, until a true STP (or CSTP) is found. In Gold’s
learning model [22], a class C of languages is identifiable in the limit if there exists an algorithm
f such that, for any language L ∈ C and any infinite sequence s0 , s1 , s2 , . . . s.t. L = {si | i ∈ ω},
the sequence f ({s0 }), f ({s0 , s1 }), f ({s0 , s1 , s2 }), . . . eventually converges to (a representation of) L.
Both the class of STPs and that of CSTPs are learnable in this sense, and our algorithms TPinf
and CTPinf serve as f above, as stated below.
Theorem 3.6. Suppose t is an STP, L(t) = {e       si | i ∈ ω}, and Mi = {e sj | 0 ≤ j ≤ i}. Then, there
exists k such that L(TPinf(Mi )) = L(t) for all i ≥ k. Similarly, if γ is a CSTP, L(γ) = {e  si | i ∈ ω},
and Mi = {e sj | 0 ≤ j ≤ i}, then there exists k such that L(CTPinf(Mi )) = L(γ) for all i ≥ k.
    In applications to program verification discussed later, we use CSTPs to represent and infer
inductive invariants. To that end, we need to consider a different learning model where the goal
is to find the strongest inductive invariant among those describable by a CSTP, given an oracle to
check the inductiveness of a CSTP. This can be regarded as a kind of active learning framework
where the oracle is a teacher. The following theorem states that our algorithm CTPinf can also be
used in this learning framework.
                                 ∗        ∗         ∗      ∗
Theorem 3.7. Let F : 2Σ ×···×Σ → 2Σ ×···×Σ be a monotonic function, and suppose that there
exists an algorithm gF that, given a CSTP γ, returns “None” if L(γ) ⊇ F (L(γ)) holds, and returns
Some(e s) for some se ∈ F(L(γ)) \ L(γ) if the inclusion does not hold. Then the procedure below
eventually terminates and returns the least CSTP γ such that L(γ) ⊇ F(L(γ)).

    M ← ∅; γ ← (a, ϵ, . . . , ϵ) ∧ (ϵ, ϵ, . . . , ϵ);
                                   s) then (M ← M ∪ {e
    while true do if gF (γ) = Some(e                 s}; γ ← CTPinf(M )) else return γ

   The algorithm above first sets γ to (a, ϵ, . . . , ϵ) ∧ (ϵ, ϵ, . . . , ϵ) so that L(γ) = ∅. It then repeatedly
adds to M the element returned by the oracle gF and invokes CTPinf. A crucial property to
guarantee the theorem is that CTPinf(M ) always returns the least CSTP γ such that M ⊆ L(γ).
See Appendix for more details.
Example 3.2. Consider the function append defined by:
  let rec append l1 l2 = match l1 with [] -> l2 | x::l1’ -> x::(append l1’ l2).
A ternary relation I is an inductive invariant describing the input-output relation of append if and
only if I satisfies I ⊇ F(I) for the following function F:

            F(R) = {(l1 , l2 , l3 ) | (l1 = ϵ ∧ l2 = l3 ) ∨ (l1 = xl1′ ∧ (l1′ , l2 , l3′ ) ∈ R ∧ l3 = xl3′ )}.

Here, we identify lists with words. We wish to find the strongest CSTP γ such that L(γ) is such
an I, that is, the strongest γ satisfying L(γ) ⊇ F(L(γ)). Using the procedure above, we can derive
(y, z, yz) as the strongest γ. See also Example 5.2, where the same procedure is used to solve the
Reva example in Section 1.
    Theorem 3.7 above would not hold if CSTPs were replaced with STPs, because there is no
guarantee that there exists a least t such that L(t) ⊇ F (L(t)). For example, suppose that F
is a constant function that always returns {(a, ab, ab), (cd, c, cde)}. Then, L(t1 ) ⊇ F (L(t1 )) and
L(t2 ) ⊇ F(L(t2 )) hold for t1 = (x, y, xz) and t2 = (x, y, yz), but there is no STP t such that
L(t) ⊆ L(t1 ) ∩ L(t2 ) and L(t) ⊇ F(L(t)). We can, however enumerate all the minimal t’s such that
L(t) ⊇ F(L(t)).


                                                           10
                             ∗       ∗       ∗       ∗
Theorem 3.8. Let F : 2Σ ×···×Σ → 2Σ ×···×Σ be a monotonic function, and suppose that there
exists an algorithm gF that, given an STP t, returns “None” if L(t) ⊇ F(L(t)) holds, and returns
Some(e s) for some se ∈ F (L(t)) \ L(t) if the inclusion does not hold. Suppose also that F (∅) ̸= ∅,
and an element se such that se ∈ F (∅) is computable. Then there exists an algorithm that enumerates
all the STPs t such that L(t) ⊇ F (L(t)) and, for every t′ , L(t′ ) ⊊ L(t) implies L(t′ ) ̸⊇ F(L(t′ )).

3.4    Decision Problems
This section investigates decision problems on STPs. We first study the membership and inclusion
problems for STPs, which is useful for CTPinf. Note that the membership and inclusion prob-
lems are respectively NP-complete and undecidable for both NE-pattern languages and E-pattern
languages [52].
Theorem 3.9. The following decision problems can be solved in polynomial time.
   1. Given a tuple pattern t, decide whether t is solvable.
   2. Given an STP t and a tuple se ∈ Σ∗ × · · · × Σ∗ , decide whether se ∈ L(t).
   3. Given an STP t2 and a tuple pattern t1 , decide whether L(t1 ) ⊆ L(t2 ).
   4. Given two STPs t1 and t2 , decide whether L(t1 ) = L(t2 ).
    To solve (1), it suffices to reduce t by ⇝ and check whether it ends up with a trivial pattern
(x1 , . . . , xk ). Since the reduction strategy does not matter (as shown in Lemma A.6 in Appendix,
⇝ is weakly confluent up to permutations), and each reduction strictly decreases #t, it can be
checked in time polynomial in #t. For (3), it suffices to observe that if t2 ⇝ t′2 and L(t1 ) ⊆ L(t2 ),
then we can find a corresponding reduction t1 ⇝∗ t′1 such that L(t′1 ) ⊆ L(t′2 ) in polynomial time
(cf. Lemma A.4 in Appendix A). If there exists no such corresponding reduction, we can conclude
L(t′1 ) ̸⊆ L(t2 ); otherwise t2 is eventually reduced to a trivial pattern (x1 , . . . , xk ), at which point
we can conclude L(t1 ) ⊆ L(t2 ). (2) and (4) are immediate consequences of (3). More details are
found in Appendix A.
    We next prove the decidability of the theory of quantifier-free formulas containing formulas of
the form w     e ∈ L(t). This decidability is important for constructing the oracle gF in Theorem 3.7,
and plays an important role in the applications to program verification discussed in Section 5.
Definition 3.1. The set of (quantifier-free) STP formulas, ranged over by φ, is given by:
        φ ::= w1 = w2 | w1 ̸= w2 | w
                                   e ∈ L(t) | w
                                              e ̸∈ L(t) | φ1 ∧ φ2 | φ1 ∨ φ2          w ∈ (Σ ∪ V)∗ .
Here, t ranges over the set of STPs.
    For example, (x, y, z) ∈ L(t) ∧ w = yz ∧ (xy, y, w) ̸∈ L(t) (which is the negation of “(x, y, z) ∈
L(t) ∧ w = yz implies (xy, y, w) ∈ L(t)”), where t = (u, v, uv) is an STP formula. The semantics
of STP formulas is defined in an obvious manner, and is therefore deferred to the Appendix. The
only point to note is that the variables occurring in t are implicitly bound within L(t); for example,
(x, y, z) ∈ L(u, v, uv) is equivalent to (x, y, z) ∈ L(y, x, yx) (although we usually avoid variable
overloading to prevent confusion).
Remark 3.5. The definition of quantifier-free STP formulas above can be actually simplified to:
                                    e ∈ L(t) | w
                              φ ::= w          e ̸∈ L(t) | φ1 ∧ φ2 | φ1 ∨ φ2 ,
because w1 = w2 and w1 ̸= w2 can be expressed by (w1 , w2 ) ∈ L(x, x) and (w1 , w2 ) ̸∈ L(x, x)
respectively.
  According to the result on word equations [56, 35], the satisfiability of STP formulas without
STP membership constraints (i.e., Boolean combinations of formulas of the form w1 = w2 ) is in
PSPACE. Thus, we have:
Theorem 3.10. Given an STP formula φ, one can effectively construct an equi-satisfiable STP
formula φ′ such that φ′ contains no subformulas of the form (w1 , . . . , wk ) ∈ L(t) or (w1 , . . . , wk ) ̸∈
L(t), and the size of φ′ is polynomial in that of φ. Therefore, the satisfiability of STP formulas is
in PSPACE.


                                                     11
    Encoding of a formula w   e ̸∈ L(t) into word equations relies on the solvability of t. In fact,
if we allowed arbitrary tuple patterns, then the satisfiability would become undecidable, because
∃x ∈ Σ∗ .(x ∈ L(p1 ) ∧ x ̸∈ L(p2 )) if and only if L(p1 )̸⊆L(p2 ) and the latter is undecidable [31, 52].


4      Extensions and Variations of Solvable Tuple Patterns
This section discusses extensions and variations of STPs. Section 4.1 extends STPs with the reverse
pattern xR , which is needed to handle the Reva example in Section 1. Section 4.2 discusses variations
of STPs to reason about sets and multisets.

4.1       Reverse
Let us extend the set of pattern expressions (ranged over by p) to (Σ ∪ V ∪ V R )∗ , where V R = {xR |
x ∈ V}. Here, xR represents the set of the reverse of strings represented by x. We extend (·)R to
the operation on patterns, by aR = a, (xR )R = x, and (p1 p2 )R = pR    R
                                                                   2 · p1 , so that the set of extended
pattern expressions is closed under substitutions. For example, [ay/x]xR = (ay)R = y R a.
   We extend the tuple pattern inference algorithm with the following rules:

          M [∗][i] ̸= e
                      ϵ          M [∗][j] = M [∗][i]R · se            x′j fresh
                                                                         x
                                                                         e = (x1 , . . . , xm )
                                                                                                                           (R-RPrefix)
              x]) −→ ([xi · xj /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])
       (t, [M/e         R    ′



          M [∗][i] ̸= e
                      ϵ          M [∗][j] = se · M [∗][i]R            x′j fresh
                                                                         x
                                                                         e = (x1 , . . . , xm )
                                                                                                                           (R-RSuffix)
              x]) −→ ([xj · xi /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])
       (t, [M/e         ′    R



Here, M [∗][i]R denotes the pointwise extension of the reverse operation. Accordingly, we extend
solvable tuple patterns by adding the following rules:
                           ′
                pj = pR
                      i · pj             pi ̸= ϵ                                          pj = p′j · pR
                                                                                                      i          pi ̸= ϵ
(p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )        (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )
                                                (PR-RPrefix)                                                                (PR-RSuffix)

    The theorems in Sections 2 and 3 continue to hold for this extension. For the decidability and
complexity of the satisfiability problem (Theorem 3.10), we rely on known results on the satisfiability
of equations over free monoids with involution [17].
                                              
                                ab cd bacd
Example 4.1. Let M be                            . The pattern (x, y, xR y) is inferred as follows.
                                bc da cbda
                                                               
                                         x1       x2        x3   
                       (x1 , x2 , x3 ),  ab       cd      bacd 
                                          bc       da      cbda
                                              x1 x2 x′3
                                                        
                                                           
                                       ′
                    −→ (x1 , x2 , xR
                                   1 x3 ),
                                             ab cd cd                                                 (R-RPrefix)
                                               bc da da
                                                 x1 x2 x′′3
                                                           
                                                             
                                           ′′ 
                    −→ (x1 , x2 , xR
                                   1 x2 x3 ),    ab cd   ϵ                                               (R-Prefix)
                                                 bc da   ϵ
                                                    
                                             x1 x2    
                    −→ (x1 , x2 , xR x
                                   1 2   ),  ab cd                                                    (R-Epsilon).
                                               bc da

Remark 4.1. One may also be tempted to extend patterns with xS , which represents the sequence
obtained by sorting x. This is problematic, however, because (·)S does not commute with concate-
nation: (y · z)S ̸= y S · z S . One way to reason about sorted sequences is to introduce a new class of
patterns called sort patterns, given by: pS ::= x | u and u ::= xS | u1 ⋆ u2 . Here, u1 ⋆ u2 denotes


                                                                      12
the set of sorted sequences obtained by merging sorted sequences represented by u1 and u2 . Sort
patterns can naturally be extended to tuple sort patterns. For example, (x, xS ) denotes the set of
pairs, whose second element is obtained by sorting the first element, and (x, y S , xS ⋆ y S ) denotes
the set of triples (s1 , s2 , s3 ), where s3 is obtained by sorting s1 and merging it with s2 . We can
then design an inference algorithm for (solvable) tuple sort patterns in a manner similar to ordinary
tuple patterns. The details will be described in a separate paper.

4.2     Beyond Sequence Patterns
We have so far considered tuple patterns consisting of words, which form a free monoid. Almost
the same technique can be applied to represent and infer relations among other similar algebraic
structures such as multisets and sets. Note that multisets form a free commutative monoid, while
sets are obtained by further imposing idempotency on the binary operation.
    To deal with multisets, we just need to interpret the empty pattern and the pattern concatenation
as the empty set and the multiset union, respectively, and identify patterns up to permutations (for
example, xyz = yzx). The inferences and reduction rules for tuple patterns can be adjusted
accordingly, as follows.

      M [∗][i] ̸= e
                  ϵ       ∀k.M [k][j] ⊇ M [k][i]        se = M [∗][j] \ M [∗][i]          x′j fresh
                                      ′                                            ′
                                                                                                                (R-Subset)
 (t, [M/(x1 , . . . , xm )]) −→ ([xi xj /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , xj , xj+1 , . . . , xm )])

                        ∀k.a ∈ M [k][j]        se = M [∗][j] \ {a}         a∈Σ
                                                                                                             (R-CSubset)
 (t, [M/(x1 , . . . , xm )]) −→ ([ax′j /xj ]t, [M {j 7→ se}/(x1 , . . . , xj−1 , x′j , xj+1 , . . . , xm )])

                                           M [∗][j] = e∅
                                                                                                                (R-Empty)
        (t, [M/(x1 , . . . , xm )]) −→ ([ϵ/xj ]t, [M ↑j /(x1 , . . . , xj−1 , xj+1 , . . . , xm )])

                                           pj = pi p′j          pi ̸= ϵ
                                                                                                               (PR-Subset)
                         (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )

                                            pj = ap′j           a∈Σ
                                                                                                           (PR-CSubset)
                         (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , p′j , pj+1 , . . . , pn )

                                                   pj = ϵ
                                                                                                               (PR-Empty)
                           (p1 , . . . , pn ) ⇝ (p1 , . . . , pj−1 , pj+1 , . . . , pn )

    Most of the results for STPs and CSTPs carry over to their multiset versions (called SMTPs and
CSMTPs), including the soundness and completeness of the inference algorithm, Theorem 3.7, and
Theorem 3.10 (where word equations are replaced with multiset equations, and the complexity of
satisfiability is changed to NP). A notable exception is that the minimality property (Theorem 3.4)
fails, but it is not an obstacle to the application to program verification discussed in the next section.
Similarly, we can deal with sets by interpreting concatenation as disjoint union.
                                                             
                                    {a, a} {a, b} {a, a, b}
Example 4.2. Let M be:                                          . The pattern (xz, yz, xyz) (which means
                                     {a, b} {b, c} {a, b, c}
that the third set is a superset of the first and second sets, where z is the intersection of the first
and second sets) is inferred as follows.

                                                                                               x′3
                                                                                                
                        x1       x2          x3                               x1         x2       
  (x1 , x2 , x3 ),  {a, a} {a, b} {a, a, b}  −→ (x1 , x2 , x1 x′3 ),  {a, a} {a, b} {b} 
                     {a, b} {b, c} {a, b, c}                                {a, b} {b, c} {c}
                                            ′     ′
                                                                                           x′1 x′2   x′3
                                                                                                      
                                   x1     x2    x3                                                      
 −→ (x1 , x′3 x′2 , x1 x′3 ),  {a, a} {a} {b}  −→ (x′2 x′1 , x′3 x′2 , x′2 x′1 x′3 ),  {a} {a} {b}  .
                                {a, b} {b} {c}                                            {a} {b} {c}



                                                                   13
Remark 4.2. Similar techniques can also be applied to binary trees, which are obtained by dropping
associativity of the binary operation and thus form a free magma. Using the tree version of STPs, we
can, for example, represent and infer tree relations such as (x, N (x, y)), where N is the binary tree
constructor; this means that the first element is the left subtree of the second. The formalization
and applications of this tree version of STPs to automated program verification are left for future
work.
Remark 4.3. While the theory of STPs can be applied to other similar free algebraic structures
as discussed above, freeness is important for STPs. Many of the theorems in Section 3 rely on
properties such as the following: if L(p′ ) ⊆ L(ap1 ), then p′ = ap′1 with L(p′1 ) ⊆ L(p1 ) for some p′1 ;
and if L(p′1 , p′2 ) ⊆ L(p2 p3 , p2 ), then p′1 = p′2 p′3 with L(p′3 ) ⊆ L(p3 ) for some p′3 .9 Such properties
do not necessarily hold for arbitrary monoids. For example, consider a monoid generated by a, b,
and c with identity element ϵ, subject to the equation ab = ca and ac = ba. In this monoid,
L(ya) ⊆ L(ax) holds, but there is no pattern p such that ya = ap.
    One may wonder whether it is possible to develop a general, unifying theory of STPs for a
certain class of free algebraic structures, and then instantiate the theory to each structure. That
does not seem straightforward, however. The proof of minimality (Theorem 3.4) relies on word-
specific properties, such as the fact that p1 p2 = p′1 p′2 implies p1 and p′1 are in a prefix relation. Such
properties do not hold for free commutative monoids, and that is why minimality fails for multisets.
Moreover, the forms of characteristic data differ between words and multisets. Thus, developing
such a unifying theory is outside the scope of this paper and left for future work.


5      Applications to Automated                                        Verification               of       List-
       Manipulating Programs
This section discusses how to apply the (C)STP inference to automated verification of programs
manipulating list-like data structures. We focus on CHC-based automated program verification [8],
where program verification problems are reduced to the satisfiability problem for constrained Horn
clauses (CHCs, a.k.a. constraint logic programs), and passed to an automated CHC solver. The
CHC satisfiability problem is undecidable in general, but a number of CHC solvers that automati-
cally solve it have been developed, though they are inevitably incomplete. These solvers typically
support integer and real arithmetic, arrays, and ADTs. An annual competition on CHC solvers
called CHC-COMP is held. The CHC-based approach provides a uniform, language-agnostic ap-
proach to automated verification. It has recently been studied extensively and applied to various
languages, ranging from low-level languages like C and LLVM [26, 65], to high-level languages like
Java [33], Rust [47], and OCaml [66, 9]. As noted in Section 1, however, CHC solvers over ADTs
have so far been unsatisfactory.
    Below we first introduce a class of CHCs with word constraints, and show that it is decidable
whether a system of CHCs (i.e., a finite set of CHCs) in that class has a model describable us-
ing CSTPs in Section 5.1. This result is directly applicable to the Reva example in Section 1.
Sections 5.2 and 5.3 discuss further enhancement of the STP-based CHC solving.

5.1      Constrained Horn Clauses over Words
A constrained Horn clause (CHC) is a Horn clause extended with constraints. It is of the form:
    y1 ) ∧ · · · ∧ Pn (e
P1 (e                     yn ) ∧ φ ⇒ P (e           y1 ) ∧ · · · ∧ Pn (e
                                         x), or P1 (e                  yn ) ∧ φ ⇒ false, where n may be 0. We
call a clause of the former form a definite clause, and one of the latter form a goal clause. Here,
P and Pi are predicate variables, and φ ranges over the set of constraint formulas over certain
domains; the first-order variables yei and x        e are assumed to be implicitly universally quantified in
each clause. A clause that can be normalized to the above form is also called a CHC. For example,
P (x, 1) ⇒ x < 1 is also a CHC, as it is equivalent to P (x, y) ∧ (y = 1 ∧ x ≥ 1) ⇒ false. We often just
write P (t1 , . . . , tn ) for the clause x1 = t1 ∧ · · · ∧ xn = tn ⇒ P (x1 , . . . , xn ), by eliminating redundant
variables and omitting “true ⇒”.
    The CHC satisfiability problem (or, the CHC problem) asks, given a set of CHCs, whether there
exists a model (i.e., an interpretation of predicate variables) that makes all the clauses valid. For
    9 See the longer version [38] for a table summarizing the properties used in the proof of each main theorem.




                                                         14
example, consider the following system of CHCs over integer arithmetic.

      Plus(0, y, y).     Plus(x − 1, y, z) ∧ x ̸= 0 ⇒ Plus(x, y, z + 1).            Plus(x, y, z) ⇒ z ≥ y.

It is satisfiable. Indeed, {Plus 7→ {(x, y, z) | x ≥ 0 ∧ z = x + y}} satisfies all the clauses. Henceforth,
we often use a formula to express a model, like Plus(x, y, z) ≡ x ≥ 0 ∧ z = x + y. A model is not
unique in general; for the example above, Plus(x, y, z) ≡ z ≥ y is also a model.
    In this section, instead of CHCs over integer arithmetic, we consider CHCs on words over Σ.
Thus, each variable ranges over the set Σ∗ of words, and constraints φ are drawn from the set of
quantifier-free STP formulas as defined in Definition 3.1.

Example 5.1. The Reva example in Section 1 is expressed as the following system of CHCs SReva .

                   Reva(ϵ, l2 , l2 ).   Reva(l1′ , xl2 , l3 ) ∧ |x| = 1 ⇒ Reva(xl1′ , l2 , l3 ).
                    Reva(l1 , l2 , l3 ) ∧ Reva(l3 , ϵ, l4 ) ∧ Reva(l2 , l1 , l5 ) ⇒ l4 = l5 .
                                                               W
Here, the constraint |x| = 1 can be expressed by a∈Σ x = a, assuming that the alphabet Σ is
finite.
    Let t = (x, y, xR , y). Then {Reva 7→ L(x, y, xR y)} is a model of the CHCs above.

   We say that a system S of CHCs on words has a CSTP-model if there exist γ1 , . . . , γn such that
{P1 7→ L(γ1 ), . . . , Pn 7→ L(γn )} is a model of S. The following is the main result of this section.
Theorem 5.1. Given a system S of CHCs on words, it is decidable whether S has a CSTP-model.
Proof Sketch. Let S = SD ∪ SG , where SD and SG respectively consist of definite and goal clauses.
By Theorem 3.7, the least CSTP-model M0 = {P1 7→ L(γ1 ), . . . , Pn 7→ L(γn )} of SD exists and it
is computable (note that the algorithm for gF can be constructed by using Theorem 3.10). Then, S
has a CSTP-model if and only if M0 is a model of SG . The latter is decidable by Theorem 3.10.
    An analogous result holds also when restricted to STP-models. We say that a system S of CHCs
on words has an STP-model if there exist STPs t1 , . . . , tn such that {P1 7→ L(t1 ), . . . , Pn 7→ L(tn )}
is a model of S. Here, we add a special STP t∅ that denotes the empty set (i.e., L(t∅ ) = ∅).
Theorem 5.2. Given a system S of CHCs on words, it is decidable whether S has an STP-model.
   To prove the theorem, it suffices to use Theorem 3.8 instead of Theorem 3.7.
Proof Sketch. Let S = SD ∪ SG , where SD and SG respectively consist of definite and goal
clauses. By Theorems 3.8 and 3.10, we can enumerate all the minimal STP-models M0 = {P1 7→
L(t1 ), . . . , Pn 7→ L(tn )} of SD . Then, it suffices to check whether one of the minimal STP-models
is also a model of SG .
   The unsatisfiability of CHCs (where models are not restricted to CSTPs) is also semi-decidable:
Theorem 5.3. There exists a procedure which, given a system S of CHCs on words, eventually
outputs “Unsat” whenever S is not satisfiable.
Proof. This follows from the fact that S is unsatisfiable if and only if there is a resolution proof.
Thanks to the decidability of word equations, we just need to enumerate a candidate resolution
proof, and check whether it is a valid proof.

    Note, however, that the satisfiability of CHCs is undecidable in general if models are not re-
stricted to CSTPs. To see this, notice that a natural number n can be encoded as the word an .
    Below, we demonstrate how we can automatically obtain a CSTP-model for the Reva-example.
For the sake of simplicity, we omit constant patterns.
Example 5.2. Recall the CHCs SReva in Example 5.1. We first compute the least model of the
definite clauses (i.e., the first two clauses) SD , based on the algorithm in Theorem 3.7. First, we
set M0 = ∅ and γ0 = (a, ϵ, ϵ) ∧ (ϵ, ϵ, ϵ), and check whether γ0 satisfies SD . Using the algorithm in
Theorem 3.10, we obtain an element se0 = (ϵ, ab, ab) that should belong to the least model.



                                                      15
    Then, we set M1 = {(ϵ, ab, ab)}, and get γ1 = CTPinf({(ϵ, ab, ab)}) = (ϵ, x, x). This does not
satisfy the second clause. Indeed, the formula obtained by negating the second clause: (l1′ , xl2 , l3 ) ∈
L(γ1 ) ∧ |x| = 1 ∧ (xl1′ , l2 , l3 ) ̸∈ L(γ1 ) has a model (x, l1′ , l2 , l3 ) = (a, ϵ, b, ab), from which we obtain
a new element se1 = (a, b, ab). By setting M2 = {(ϵ, ab, ab), (a, b, ab)}, we obtain γ2 = (x, y, xy) ∧
(x, y, xR y). Since (l1′ , xl2 , l3 ) ∈ L(γ2 ) ∧ |x| = 1 ∧ (xl1′ , l2 , l3 ) ̸∈ L(γ2 ) has a model (x, l1′ , l2 , l3 ) =
(a, b, ϵ, ba), we obtain the new element: se2 = (ab, ϵ, ba).
    By setting M3 = {(ϵ, a, a), (a, b, ab), (ab, ϵ, ba)}, we obtain γ3 = (x, y, xR y). Now, γ3 is a model
of SD . Since γ3 is also a model of the goal clause, we can conclude that SReva is satisfiable, and
hence also that the reva program in Section 1 does not suffer from assertion failures.
    In Appendix B, we extend CSTP-models to piecewise CSTP-models, and apply them to verifi-
cation of functional queues.
Remark 5.1. In Example 5.2 above, if we replace CTPinf used inside the algorithm of Theorem 3.7
with TPinf, then the inference may fail. Consider the state M2 = {(ϵ, ab, ab), (a, b, ab)} above. If
TPinf is invoked instead of CTPinf, we may obtain t2 = (x, y, xy) as a minimal (but not the least)
t such that M2 ⊆ L(t). Then, as a model of (l1′ , xl2 , l3 ) ∈ L(t2 ) ∧ |x| = 1 ∧ (xl1′ , l2 , l3 ) ̸∈ L(t2 ), we
may obtain (x, l1′ , l2 , l3 ) = (c, ab, ϵ, abc), which yields se′2 = (cab, ϵ, abc).
    By setting M3′ = {(ϵ, a, a), (a, b, ab), (cab, ϵ, abc)}, we obtain TPinf(M3′ ) = (x, y, zy). Note that
L(x, y, xR y) ⊊ L(x, y, zy). Thus, we have failed to infer the least model {Reva 7→ (x, y, xR y)} of
SD , and therefore, we have also failed to prove that SReva is satisfiable.
    We can still prove the satisfiability of SReva by using only STPs, based on Theorem 5.2 (which
relies on Theorem 3.8 instead of Theorem 3.7).
Remark 5.2. The results above can be directly applied to automated verification of programs
manipulating functional lists. To handle programs manipulating mutable linked lists, we can use the
technique of RustHorn [47] to convert mutable linked lists into functional lists, and then apply our
technique. Other mutable data structures can be mapped to (functional) trees using the technique
of RustHorn [47]. We can then either (i) apply the tree version of STPs mentioned in Remark 4.2, or
(ii) abstract trees to lists and then apply our results on CHCs over words. We expect, for example,
that programs over binary search trees can be verified using the latter approach, by abstracting
a binary search tree to the list of its elements. Skip lists [57] could also be handled in a similar
manner: despite the name “lists,” they would first be mapped to trees reflecting their physical
structure, and then abstracted to a tuple of lists (ℓ1 , . . . , ℓk ), where ℓi is the list of elements at
level i. The structural properties of a skip list—namely, that each ℓi is a sorted sequence and that
ℓi is a subsequence of ℓj for any j < i—can be described using the pattern of sorted sequences
mentioned in Remark 4.1. At present, however, these applications remain speculative. A concrete
formalization and implementation are left for future work.

5.2     Combination with CHC Solving for Integer Arithmetic
The CHCs obtained from list-manipulating programs typically contain integer constraints in addi-
tion to word (or list) constraints. The CSTPs alone are not always sufficient to express appropriate
invariants for such CHCs. Let us recall the second example (involving take and drop) in Section 1.
It can be expressed as the satisfiability of the following CHCs:

 Take(0, l, ϵ).      n ̸= 0 ⇒ Take(n, ϵ, ϵ).         n ̸= 0 ∧ Take(n − 1, l′ , r) ∧ |x| = 1 ⇒ Take(n, xl′ , xr).
 Drop(0, l, l).      n ̸= 0 ∧ Drop(n, ϵ, ϵ).        n ̸= 0 ∧ Drop(n − 1, l′ , r) ⇒ Drop(n, xl′ , r).
 Take(n, l, r1 ) ∧ Drop(n, l, r2 ) ∧ Append (r1 , r2 , l′ ) ∧ l ̸= l′ ⇒ false.

Here, we have omitted the clauses for Append . As before we have encoded lists into words, but the
resulting CHCs also contain integer constraints. Ignoring the integer constraints, the least CSTP
model of the definite clauses obtained by CTPinf is: Take(n, l1 , l2 ) ≡ ∃l3 .l1 = l2 l3 , Drop(n, l1 , l2 ) ≡
∃l3 .l1 = l3 l2 , and Append (l1 , l2 , l3 ) ≡ l3 = l1 l2 . It is not strong enough to satisfy the goal clause
(i.e., the last clause above).
     To address the issue, we use a CHC solver over integers to strengthen the model of definite
clauses. We abstract lists to their lengths and obtain the following abstract version of the CHCs.

 Take ′ (0, l, 0).     n ̸= 0 ⇒ Take ′ (n, 0, 0).       n ̸= 0 ∧ Take ′ (n − 1, l′ , r) ⇒ Take ′ (n, 1 + l′ , 1 + r).


                                                          16
 Drop ′ (0, l, l).      n ̸= 0 ∧ Drop ′ (n, 0, 0).       n ̸= 0 ∧ Drop ′ (n − 1, l′ , r) ⇒ Drop ′ (n, 1 + l′ , r).
 Take ′ (n, l, r1 ) ∧ Drop ′ (n, l, r2 ) ∧ Append ′ (r1 , r2 , l′ ) ∧ l ̸= l′ ⇒ false.
In general, given a system of CHCs over lists S = SD ∪ SG , (i) the list constructors [ ] and :: are
replaced with their length abstractions 0 and λ(x, y) = 1 + y, (ii) the list equalities (which implicitly
occur in the clause bodies) are replaced with integer equalities; and (iii) the list inequalities l ̸= l′
in the body of goal clauses SG are replaced with the integer inequalities, and those in the bodies of
definite clauses SD are replaced with true.
                                                                                        ′
      The above abstraction ensures that a model of the abstract version SD               of definite clauses yields
                                                   ′     ′                      ′
that of the original definite clauses SD : if P (e   x, l ) ≡ φ satisfies SD , then P (e
                                                        e                                      l) ≡ [|e
                                                                                            x, e         l′ ]φ satisfies
                                                                                                      l|/e
SD (where we assume x        e are integer arguments and l are list arguments); this follows from the
                                                               e
soundness of the catamorphism-based abstraction of CHCs [36].
      In contrast, there is no such guarantee for the goal clauses: because of the replacement of =list
and ̸=list with =int and ̸=int , the abstract version of goal clauses is neither stronger nor weaker
than the original goal clauses. (Notice that |l1 | = |l2 | is an over-approximation of l1 = l2 , while
|l1 | ̸= |l2 | is an under-approximation of l1 ̸= l2 .) The abstract goal clauses, however, tend to help a
CHC solver to find an appropriate invariant. In the case above, if l ̸= l′ were replaced with true,
we would obtain Take ′ (n, l, r1 ) ∧ Drop ′ (n, l, r2 ) ∧ Append ′ (r1 , r2 , l′ ) ⇒ false, which is so strong that
the abstract CHCs would become unsatisfiable.
      Suppose a CHC solver yields the following model for the abstract CHCs above:
      Take ′ (n, l, r) ≡ r = l < n ∨ l ≥ n = r             Drop ′ (n, l, r) ≡ (l < n ∧ r = 0) ∨ l ≥ n = l − r.
Then we have the following model for the definite clauses of the original CHCs.
Take(n, l, r) ≡ |r| = |l| < n ∨ |l| ≥ n = |r|             Drop(n, l, r) ≡ (|l| < n ∧ |r| = 0) ∨ |l| ≥ n = |l| − |r|.
By conjoining them with the candidate model obtained by using STP inference, we obtain:
                     Take(n, l, r) ≡ ∃s.l = rs ∧ (|r| = |l| < n ∨ |l| ≥ n = |r|)
                     Drop(n, l, r) ≡ ∃s.l = sr ∧ ((|l| < n ∧ |r| = 0) ∨ |l| ≥ n = |l| − |r|).
This satisfies the goal clause, and thus we have proved that the original system of CHCs is satisfiable.
   In general, in parallel to running the least CSTP model, we apply the length abstraction and use
a CHC solver over integer arithmetic to solve the abstract CHCs and obtain a model P ′ (e            l′ ) ≡ φ.
                                                                                                  x, e
(Here, we assume that P ′ (e x, le′ ) is the length abstraction of the original predicate P (e
                                                                                             x, e
                                                                                                l), where x  e
and l are integer and list arguments respectively.) Then when checking whether the least CSTP
    e
model satisfies the goal clause, we strengthen the candidate model P by conjoining [|e          l′ ]φ.
                                                                                             l|/e
Remark 5.3. Instead of just using the information obtained from the length abstraction, it is
possible to propagate information gathered from STP inference and length abstraction to each other,
as in Nelson-Oppen procedure [51] for theory combinations. For example, suppose that P (l1 , l2 , l3 )
is found to imply l3 = l1 l2 by STP inference. Then, each occurrence of P (l1 , l2 , l3 ) in the body of
a clause can be replaced by P (l1 , l2 , l3 ) ∧ l3 = l1 l2 , before applying the length abstraction. Then, a
clause of the form P (l1 , l2 , l3 ) ∧ · · · ⇒ P (l4 , l5 , l6 ) is abstracted to P ′ (l1 , l2 , l3 ) ∧ l3 = l1 + l2 ∧ · · · ⇒
P ′ (l4 , l5 , l6 ).
Remark 5.4. In theory, the above method for utilizing CHCs over integer arithmetic is not re-
stricted to the length abstraction: any sound abstraction of lists to integers [36] would work. Our
restriction to the length abstraction comes from the following practical motivation. As in the exam-
ple above, the final candidate model involves both sequence constraints and constraints on integers
obtained by abstracting lists. The state-of-the-art SMT solvers like CVC5 and Z3 work fairly well
for a combination of sequences and length functions, but do not work well for a combination of
sequences and arbitrary recursive functions on sequences, to our knowledge.

5.3      Beyond Sequence and Integer Constraints
The (conjunctive) solvable set/multiset tuple patterns discussed in Section 4.2 are also applicable to
CHC solving, as stated in the theorem below. Here, CHCs over multisets refer to those whose con-
straint formulas are drawn from those on multisets [55]. The theorem follows from the set/multiset
versions of Theorems 3.7, 3.8, and 3.10.


                                                             17
Theorem 5.4. Given a system S of CHCs over multisets, it is decidable whether S has a CSMTP-
model. Similarly, given a system S of CHCs over sets, it is decidable whether S has a CSSTP-model.
Theorem 5.5. Given a system S of CHCs over multisets, it is decidable whether S has an SMTP-
model. Similarly, given a system S of CHCs over sets, it is decidable whether S has an SSTP-model.
Example 5.3. Let us consider the following insertion sort program:
    let rec insert x l =
      match l with [] -> [x] | y::l’ -> if x<y then x::l else y::(insert x l’)
    let rec isort l = match l with [] -> [] | x::l’ -> insert x (isort l’)
    let main l = assert(eq_as_multiset (isort l) l).
The function main takes a list l as input, sorts it, and asserts that the result is equivalent to l
as multisets; here, for the sake of simplicity, we assume that eq_as_multiset is a primitive. By
abstracting lists to multisets and overapproximating the formula x < y by true, we obtain the
following CHCs over multisets, whose satisfiability implies the lack of assertion failures.

 |x| = 1 ⇒ Insert(x, ϵ, x).       l = yl′ ∧ |x| = |y| = 1 ⇒ Insert(x, l, xl).
 l = yl′ ∧ |x| = |y| = 1 ∧ Insert(x, l′ , r) ⇒ Insert(x, l, yr).
 Sort(ϵ, ϵ).     |x| = 1 ∧ l = xl′ ∧ Sort(l′ , r′ ) ∧ Insert(x, r′ , r) ⇒ Sort(l, r).    Sort(l, r) ⇒ l = r.

By running the multiset version of the procedure of Theorem 3.7, we obtain the following least
CSMTP-model for definite clauses:

                 Insert(x, l, r) ≡ (x, l, r) ∈ L(x, l, xl)     Sort(l, r) ≡ (l, r) ∈ L(l, l).

Since it satisfies the goal clause Sort(l, r) ⇒ l = r, we can conclude that the system of CHCs
above is satisfiable, and hence also that the program does not suffer from assertion failures. In
the same manner, we can also verify that the merge and quick sort programs preserve the multiset
of elements, fully automatically (without any invariant annotations for auxiliary functions such as
merge and partition).


6       Implementation and Experiments
We have implemented a tool called TupInf for (C)STP inference based on the algorithm in Sec-
tion 3, and a new CHC solver called CHoCoL based on the method in Section 5, using TupInf
as a backend. Section 6.1 gives an overview of those tools, and Section 6.2 reports experimental
results.

6.1     Implementation
6.1.1    TupInf : a Solvable Tuple Pattern Inference Tool
TupInf has been implemented in OCaml. TupInf takes learning data in the csv format, and
outputs STPs or CSTPs with the extensions described in Sections 4.1 (reverse), and 4.2 (set and
multiset patterns). The alphabet Σ used in the learning data consists of digits and uppercase and
lowercase English letters. TupInf provides options to (i) enable or disable constant patterns (i.e.,
R-CPrefix and R-CSuffix), (ii) choose between STPs and CSTPs, and (iii) select between se-
quence, multiset, and set patterns. The option for constant patterns was disabled in the experiments
reported below.

6.1.2    CHoCoL: a CHC Solver for List-like Data Structures
CHoCoL (Constrained Horn Clauses over Lists) is also implemented in OCaml and uses TupInf
for CSTP inference, Z3 [16] and CVC5 [6] for SMT solving, and HoIce [9] for CHC solving over
integer arithmetic, as backend solvers. Currently, CHoCoL supports only list-like data structures
as ADTs, i.e., ADTs that have two constructors: one with no arguments and the other with two
arguments whose types are some element type and the ADT itself. CHoCoL also supports natural


                                                      18
Table 1: Numbers of solved instances by CHoCoL and the existing CHC solvers. The numbers in
parentheses are the numbers of uniquely solved instances.

           Solver                    Solved (SAT)        Solved (UNSAT)          Solved (all)
           CHoCoL                       180 ( 97)             80 ( 0)             260 ( 97)
           RInGen                       64 ( 23)              37 ( 4)             101 ( 27)
           Spacer                         20 ( 2)             90 ( 0)              110 ( 2)
           Eldarica                      20 ( 0)              84 ( 0)              104 ( 0)
           HoIce                          25 ( 6)             45 ( 0)               70 ( 6)
           Catalia                       87 ( 11)             87 ( 0)             174 ( 11)
           CHoCoL+Catalia                  194                    84                  278


numbers represented as lists with unit elements. CHoCoL has five internal modes: list-stp-mode,
set-mode, multiset-mode, list-len-mode, and list-cstp-mode. Given a system of CHCs as input,
CHoCoL tries five modes (in the order listed above) one by one until it finds that the CHCs are
satisfiable. In the list-stp-mode and list-cstp-mode, the tool infers tuple patterns for list-like data
structures as described in Section 5.1, but the inferred patterns are restricted to STPs in the former
for the sake of efficiency. (Experimental results suggest that CSTP inference itself can be performed
efficiently in practice, but it sometimes outputs a large CSTP, which can impose significant overhead
on the underlying SMT solver when checking its validity.) In the list-len-mode, it additionally infers
invariants on the lengths of lists as described in Section 5.2 by using the backend CHC solver for
integer arithmetic.
     The procedure explained so far can only prove the satisfiability of the CHCs. Thus, CHoCoL
also runs in parallel a procedure
                             V         based on symbolic execution to prove the unsatisfiability. Given a
CHC whose goal clauseVis i Pi (e      yi )∧C ⇒ false, CHoCoL searches for an assignment to variables yei
that makes the body ( i Pi (e    yi ) ∧ C) of the goal clause valid by recursively unfolding the predicates
in the goal in a breadth-first manner. The details of this procedure are omitted, since it is rather
straightforward and contains few novel ideas. It would be possible to utilize the result of tuple
pattern inference also to speed-up the refutation process, but that is left for future work.

6.2    Experiments
We have conducted experiments on a benchmark set selected from CHC-COMP 2025 ADT-LIN
category. The benchmark set consists of 445 instances of the CHC satisfiability problem, which are
all the instances of the ADT-LIN category where the used ADTs are only list-like data structures.
The experiments were conducted on a machine with AMD Ryzen 9 5900X CPU and 32GB RAM.
The cpu and wallclock time limits were 3 minutes, and the memory limit was 8GB. The number of
CPU cores was limited to 4.
    We compared CHoCoL with the state-of-the-art CHC solvers that support ADTs: RIn-
Gen [41], Spacer/Racer [40, 32], Eldarica [28], HoIce [9, 10], and Catalia [36]. The re-
sults are shown in Table 1 and Figure 1. To confirm that our method serves as a complement
to previous methods, we have also prepared a combination of CHoCoL and Catalia, shown as
CHoCoL+Catalia in the table and figure; it runs CHoCoL and Catalia in parallel.10
    Table 1 shows the numbers of solved instances by CHoCoL and the other CHC solvers. For
each solver, the column Solved (SAT) (resp. Solved (UNSAT)) shows the number of satisfiable
(resp. unsatisfiable) instances solved, and the column Solved (all) shows the total number of
instances solved. The numbers in parentheses indicate instances uniquely solved by the solver, i.e.,
those that no other solver (except CHoCoL+Catalia) could solve within the time limit.
    The experimental results demonstrate the effectiveness of CHoCoL. CHoCoL achieved the
highest total number of solved instances (260) among all compared solvers, showing its overall
superiority in handling CHCs with list-like data structures. A key strength of CHoCoL is its per-
formance on satisfiable instances, where it solved 180 instances compared to 87 by Catalia and 64
  10 A combination of CHoCoL (without seq-cstp-mode) and Catalia, called “ChocoCatalia” won the ADT-LIN

category of CHC-COMP 2025; the configuration of CHoCoL+Catalia reported in this submission slightly differs
from “ChocoCatalia”.



                                                    19
                  (a) All instances                                           (b) SAT instances

                         Figure 1: Numbers of solved instances within the time.

                   Table 2: Numbers of solved instances by each mode of CHoCoL.

        Mode                     Solved SAT instances            Uniquely solved SAT instances
        list-stp-mode                         89                                     50
        set/multiset-mode                     9                                      5
        list-len-mode                         78                                     42
        refutation                            4                                      0
        Total                                180                                     97


by RInGen. More importantly, CHoCoL uniquely solved 97 satisfiable instances,11 demonstrating
the effectiveness of the STP inference approach for CHC solving.
    The result of CHoCoL+Catalia, though, shows that CHoCoL also has a limitation, and
that it is better to use it as a complement to other solvers. Also, in contrast with the strong
performance of CHoCoL for SAT instances, CHoCoL showed slightly lower performance than
other solvers (except RInGen) for UNSAT instances. This is unsurprising because our current
refutation procedure is quite naive. We plan to apply STP inference also to improve the refutation
procedure.
    Figure 1 gives cactus plots, showing how many instances were solved within a given time. The
left subfigure (a) shows the numbers of solved instances for all instances, and the right subfigure (b)
shows the numbers of solved instances for SAT instances. It is remarkable that, for the successful
instances, CHoCoL solved many of them almost instantly, within one second.
    Table 2 shows the numbers of solved SAT instances by each mode of CHoCoL. The row “refu-
tation” shows the number of instances found to be satisfiable only by finite unfolding. Remarkably,
the list-stp-mode alone solved more SAT instances than the other solvers. As shown in the row
“list-len-mode”, the combination of STPs and CHC solving over integer arithmetic was also effec-
tive. There were no uniquely solved instances for list-cstp-mode; this suggests that although CSTPs
are required in theory (cf. Theorem 5.4), STPs often suffice in practice.
    We have also manually inspected some of the SAT instances that could not be solved by
CHoCoL. They typically involve functions such as sort, filter, map, and fold, whose input/output
relations cannot be expressed by STPs. We plan to extend our framework to support those list
functions, along the line suggested in Remark 4.1.
  11 A increase of the time limit would not significantly change the situation, because the benchmark set contains a

number of instances that require reasoning about list equalities, as in the examples in Section 1, which cannot be
solved by Catalia and RInGen, which abstract lists to integers or elements of a finite domain.




                                                        20
7     Related Work
7.1    Learning Languages from Positive Samples
The problem of learning a language from only positive samples [22] has been actively studied, and
various language classes have been found to be learnable. As already mentioned, most closely related
to our notion of tuple patterns is Angluin’s pattern languages [3, 2] and its variations [63, 64]. In-
deed, “erasing” pattern languages [63, 64] (in which empty strings may be substituted for variables,
as opposed to Angluin’s original pattern languages) can be considered singleton tuple patterns,
and conversely, if we introduce a special symbol $ (which must not occur in strings substituted for
variables; such a restriction may be expressed by patterns with regular constraints [63]), then a
tuple pattern (p1 , . . . , pn ) can be expressed as the pattern p1 $ · · · $pn . No polynomial time learning
algorithm is known for the full class of pattern languages (and in fact, the existence of such an algo-
rithm is highly unlikely given the result of [2]). Various subclasses of pattern languages are known
to be polynomial time learnable from positive data [2, 62, 58, 63, 49]. Among others, Angluin [2]
and Shinohara [64] gave polynomial time algorithms respectively for patterns consisting of a single
variable and for “regular” (erasing) patterns where each variable may occur only once. Mitchell [49]
extended the latter result to quasi-regular patterns, where variables must occur the same number
of times. Those subclasses are not large enough to express tuple patterns like (xy, xyx) (which
contains two variables, each of which occurs a different number of times).
    Other classes of languages learnable only from positive samples (i.e., “identifiable in the
limit” [22]) include: reversible languages [4], strictly locally testable languages [70], “very sim-
ple grammars” [69, 71], substitutable context-free languages and their variations [11, 72, 73], and
length-bounded elementary formal systems [64]. Except the length-bounded elementary formal sys-
tems [64], those classes are not expressive enough to subsume solvable tuple patterns. In fact, most
of them are subclasses of regular or context-free languages. For length-bounded elementary formal
systems [64], there exists no efficient learning algorithm.
    Gulwani et al. [24, 23] invented a method for inferring string functions from translation examples
and applied it to spreadsheets. Although their method is heuristic and does not satisfy good
learning-theoretic properties like ours to our knowledge, it would be interesting to integrate their
technique with ours to infer invariants for functional relations.

7.2    Data-Driven Approaches to Program Verification
Various data-driven approaches to program verification have recently been proposed, especially for
automated discovery of program invariants. Some of them require only positive samples [61, 29, 76],
some require negative samples as well [75, 74, 60], and some require even implication examples
of the form d1 ∧ · · · ∧ dk ⇒ d, which means “if d1 , . . . , dk are positive samples, then d is also
positive” [21, 9, 20, 39]. The used techniques vary from algebraic ones [61, 29], SVM [75, 74],
and neural networks [60, 39]. Most of those techniques have been used mainly for the discovery of
invariants on integers, and it is unclear how they can be adopted to discover invariants on list-like
data structures.
    Among them, the techniques of Sharma et al. [61] and Ikeda et al. [29] are technically closest
to ours (although they are for discovering numerical equality constraints), in that those methods
can also quickly infer equality constraints only from a small number of examples. In fact, our STP
inference algorithm, which repeatedly simplifies learning data in matrix form, has been inspired by
those techniques. Ikeda et al. [29] applied that technique to CHC solving. The application to CHC
solving is less trivial in our context, however. In the case of Ikeda et al. [29], which finds equality
constraints on integers, it is sufficient to insert those invariants as a part of preprocessing, and then
invoke an off-the-shelf CHC solver. For example, if we can find an invariant P (x, y) ⇒ x + 2y = 3,
then we can provide that information to a CHC solver, just by replacing every occurrence of
P (z, w) in CHC with P (z, w) ∧ z + 2w = 3. In contrast, since there are no CHC solvers that can
directly reason about sequence equality constraints, we had to develop a more sophisticated method
for applying the result of CSTP inference to CHC solving, as discussed in Section 5. Actually,
Theorem 5.1 can also be adopted for the method of Ikeda et al. [29] as follows: given a system S of
CHCs over linear integer arithmetic, it is decidable whether S     V has a model that can be described
solely by conjunctions of linear integer equalities of the form i ⃗ci ⃗xi + di = 0.


                                                     21
    Zhu et al. [76] proposed a data-driven approach to learning invariants of (immutable) data
structures. Their technique learns relations between two nodes of a data structure (e.g., “for every
cons-cell N1 in a list, the value of every cell reachable from N1 is no less than that of N1 ”), and
can therefore reason about properties such as the sortedness of a list. To our knowledge, however,
their technique cannot be applied to reasoning about the logical equivalence of lists; in fact, their
abstraction for lists cannot distinguish [1;1;1;2;2] from [1;1;2;2;2]. Therefore, their technique cannot
handle either of our motivating examples in Section 1. Related techniques have been developed
for verifying programs that manipulate mutable data structures [34, 30], but these techniques also
cannot reason about the logical equality of lists.

7.3    CHC Solving for Algebraic Data Types
Solving CHCs over algebraic data types (or, automated verification of programs manipulating
ADTs) often require finding and reasoning about inductive properties. To this end, Unno et al. [68]
introduced an automated method for applying induction in CHC solving. De Angelis et al. [15]
later proposed a method to achieve similar effects without explicit induction, by using unfold/fold
transformations. Mordvinov and Fedyukovich [50] also proposed a variation of unfold/fold trans-
formations. Losekoot et al. [43, 44] applied automata-based techniques to reason about relational
properties of ADTs, which also have a similar effect to unfold/fold transformation-based techniques.
These methods tend to be fragile, requiring a lot of heuristics to automatically decide how and when
to apply induction, unfold/fold transformations, etc.
    Several methods for CHC solving have also been proposed, which abstract ADTs to elements of a
finite domain or integers. Kostyukov [41] proposed a method for abstracting ADTs using automata,
while the Eldarica CHC solver [28] abstracts ADTs by their size. Govind V. K. et al. [32] proposed
a method that uses recursively defined functions (RDTs) over ADTs for abstraction, but those
RDTs must be explicitly specified. Katsura et al. [36] proposed a method for automatically finding
a catamorphism-based abstraction for ADTs. While these methods are effective for certain CHCs,
they are not effective for proving the equality of ADTs; although the abstraction by using an
abstraction map α may be used for proving α(l1 ) = α(l2 ), it does not imply l1 = l2 in general.
Thus, those methods cannot be used to prove neither of the examples in Section 1. As confirmed
in our experiments, our method using CSTPs is complementary to those methods; in fact, the
combination of our method with Catalia achieved the best performance in the experiments in
Section 6, and also in the competition CHC-COMP 2025.

7.4    Combination of Static Analyses
In Section 5.2, we have shown how to strengthen our STP inference-based CHC solving procedure
by combining it with an off-the-shelf CHC solver for integer arithmetic. There have been studies
on how to combine static analyses [13, 25, 14] in the context of abstract interpretation. The
particular way of combining CHC solving methods, however, appears to be novel. As discussed
in Section 5.2, the CHCs obtained by the length abstraction is neither sound nor complete with
respect to the original CHCs (the satisfiability of the abstract CHCs neither implies nor is implied
by the satisfiability of the original ones), but we can still obtain useful information from a solution
of the abstract CHCs, for solving the original CHCs. Our combination method treats a CHC solver
for integer arithmetic as a black box, allowing any CHC solvers to be used, including those based
on PDR [40], predicate abstraction [28], and data-driven methods [10, 74]. We have discussed only
a specific combination in Section 5.2; it would be an interesting direction for future work to further
generalize and formalize the idea of combining CHC solvers over different domains.


8     Conclusions
We have introduced the new notions of solvable tuple patterns (STPs) and conjunctive STPs
(CSTPs), and developed their theories. In particular we have shown that both STPs and CSTPs
are learnable from only positive samples, and that the satisfiability of quantifier-free formulas is de-
cidable. We have applied those theories to prove that it is decidable whether a system of CHCs over
words has a CSTP-describable model. We have implemented a new CHC solver called CHoCoL


                                                  22
based on the proposed approach, and confirmed the effectiveness of the approach through experi-
ments.
    Future work includes: (i) generalizing STPs to trees and other algebraic structures (cf. Re-
mark 4.2) to handle tree-like data structures and support reasoning about other list opera-
tions (cf. Remark 4.1); (ii) extending STPs to infer Boolean combinations of STPs, such as
(x, y, xz) ∨ (x, y, yz), meaning that either the first or second element is a prefix of the third; (iii) ap-
plying other classes of languages learnable from positive samples to CHC solving; and (iv) extending
and generalizing the method for combining CHC solvers over different domains.

Acknowledgment
We thank the anonymous reviewers for their useful feedback. This work was supported by JSPS
KAKENHI Grant Number JP20H05703 and JP26H02486.

Data Availability Statement
The artifact of this paper is available on Zenodo [37]. It includes the instructions, software, bench-
mark set, and scripts to reproduce the experiments in the paper.


References
 [1] Alfred V. Aho. 1968. Indexed Grammars—An Extension of Context-Free Grammars. J. ACM
     15, 4 (Oct. 1968), 647–671. https://doi.org/10.1145/321479.321488
 [2] Dana Angluin. 1980. Finding patterns common to a set of strings. J. Comput. System Sci. 21,
     1 (1980), 46–62. https://doi.org/10.1016/0022-0000(80)90041-0

 [3] Dana Angluin. 1980. Inductive inference of formal languages from positive data. Information
     and Control 45, 2 (1980), 117–135. https://doi.org/10.1016/S0019-9958(80)90285-5
 [4] Dana Angluin. 1982. Inference of Reversible Languages. J. ACM 29, 3 (July 1982), 741–765.
     https://doi.org/10.1145/322326.322334

 [5] Kazuyuki Asada, Ryosuke Sato, and Naoki Kobayashi. 2017. Verifying relational properties
     of functional programs by first-order refinement. Sci. Comput. Program. 137 (2017), 2–62.
     https://doi.org/10.1016/j.scico.2016.02.007
 [6] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai
     Mann, Abdalrhman Mohamed, Mudathir Mohamed, Aina Niemetz, Andres Nötzli, Alex
     Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng, Cesare Tinelli, and Yoni Zo-
     har. 2022. cvc5: A Versatile and Industrial-Strength SMT Solver. In Tools and Algo-
     rithms for the Construction and Analysis of Systems - 28th International Conference, TACAS
     2022, Held as Part of the European Joint Conferences on Theory and Practice of Software,
     ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part I (Lecture Notes in
     Computer Science, Vol. 13243), Dana Fisman and Grigore Rosu (Eds.). Springer, 415–442.
     https://doi.org/10.1007/978-3-030-99524-9_24
 [7] Nikolaj Bjørner, Arie Gurfinkel, Kenneth L. McMillan, and Andrey Rybalchenko. 2015. Horn
     Clause Solvers for Program Verification. In Fields of Logic and Computation II - Essays Ded-
     icated to Yuri Gurevich on the Occasion of His 75th Birthday (LNCS, Vol. 9300). Springer,
     24–51. https://doi.org/10.1007/978-3-319-23534-9_2

 [8] Nikolaj S. Bjørner, Kenneth L. McMillan, and Andrey Rybalchenko. 2013. On Solving
     Universally Quantified Horn Clauses. In Static Analysis - 20th International Symposium,
     SAS 2013, Seattle, WA, USA, June 20-22, 2013. Proceedings (Lecture Notes in Computer
     Science, Vol. 7935), Francesco Logozzo and Manuel Fähndrich (Eds.). Springer, 105–125.
     https://doi.org/10.1007/978-3-642-38856-9_8




                                                    23
 [9] Adrien Champion, Tomoya Chiba, Naoki Kobayashi, and Ryosuke Sato. 2020. ICE-Based
     Refinement Type Discovery for Higher-Order Functional Programs. J. Autom. Reason. 64, 7
     (2020), 1393–1418. https://doi.org/10.1007/s10817-020-09571-y
[10] Adrien Champion, Naoki Kobayashi, and Ryosuke Sato. 2018. HoIce: An ICE-Based Non-
     linear Horn Clause Solver. In Programming Languages and Systems - 16th Asian Symposium,
     APLAS 2018, Wellington, New Zealand, December 2-6, 2018, Proceedings (Lecture Notes in
     Computer Science, Vol. 11275), Sukyoung Ryu (Ed.). Springer, 146–156. https://doi.org/
     10.1007/978-3-030-02768-1_8
[11] Alexander Clark and Rémi Eyraud. 2007. Polynomial Identification in the Limit of Substi-
     tutable Context-free Languages. Journal of Machine Learning Research 8, 60 (2007), 1725–
     1745. http://jmlr.org/papers/v8/clark07a.html
[12] Edmund Clarke, Orna Grumberg, Somesh Jha, Yuan Lu, and Helmut Veith. 2003.
     Counterexample-guided abstraction refinement for symbolic model checking. JACM 50, 5
     (2003), 752–794.

[13] Michael Codish, Anne Mulkers, Maurice Bruynooghe, Maria Garcı́a de la Banda, and Manuel
     Hermenegildo. 1995. Improving abstract interpretations by combining domains. ACM Trans.
     Program. Lang. Syst. 17, 1 (Jan. 1995), 28–44. https://doi.org/10.1145/200994.200998
[14] Patrick Cousot, Radhia Cousot, and Laurent Mauborgne. 2011. The Reduced Product of
     Abstract Domains and the Combination of Decision Procedures. In Foundations of Software
     Science and Computational Structures, Martin Hofmann (Ed.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 456–472.
[15] Emanuele De Angelis, Fabio Fioravanti, Alberto Pettorossi, and Maurizio Proietti. 2018. Solv-
     ing Horn Clauses on Inductive Data Types Without Induction. Theory Pract. Log. Program.
     18, 3-4 (2018), 452–469. https://doi.org/10.1017/S1471068418000157

[16] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An Efficient SMT Solver.
     In Tools and Algorithms for the Construction and Analysis of Systems, 14th International
     Conference, TACAS 2008, Held as Part of the Joint European Conferences on Theory and
     Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings
     (Lecture Notes in Computer Science, Vol. 4963), C. R. Ramakrishnan and Jakob Rehof (Eds.).
     Springer, 337–340. https://doi.org/10.1007/978-3-540-78800-3_24
[17] Volker Diekert, Claudio Gutierrez, and Christian Hagenah. 2005. The existential theory of
     equations with rational constraints in free groups is PSPACE-complete. Information and Com-
     putation 202, 2 (2005), 105–140. https://doi.org/10.1016/j.ic.2005.04.002
[18] Volker Diekert, Artur Jez, and Wojciech Plandowski. 2016. Finding all solutions of equations
     in free groups and monoids with involution. Inf. Comput. 251 (2016), 263–286. https:
     //doi.org/10.1016/J.IC.2016.09.009
[19] Volker Diekert and Anca Muscholl. 2006.           SOLVABILITY OF EQUATIONS IN
     GRAPH GROUPS IS DECIDABLE.                 International Journal of Algebra and Com-
     putation 16, 06 (2006), 1047–1069.        https://doi.org/10.1142/S0218196706003372
     arXiv:https://doi.org/10.1142/S0218196706003372
[20] P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg, and P. Madhusudan. 2018. Horn-
     ICE learning for synthesizing invariants and contracts. Proc. ACM Program. Lang. 2, OOPSLA
     (2018), 131:1–131:25. https://doi.org/10.1145/3276501

[21] Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. 2014. ICE: A Robust
     Framework for Learning Invariants. In Proceedings of CAV 2014 (LNCS, Vol. 8559). Springer,
     69–87.
[22] E Mark Gold. 1967. Language identification in the limit. Information and Control 10, 5 (1967),
     447–474. https://doi.org/10.1016/S0019-9958(67)91165-5


                                                24
[23] Sumit Gulwani. 2011. Automating string processing in spreadsheets using input-output ex-
     amples. In Proceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of
     Programming Languages, POPL 2011, Austin, TX, USA, January 26-28, 2011, Thomas Ball
     and Mooly Sagiv (Eds.). ACM, 317–330. https://doi.org/10.1145/1926385.1926423

[24] Sumit Gulwani, William R. Harris, and Rishabh Singh. 2012. Spreadsheet data manipulation
     using examples. Commun. ACM 55, 8 (2012), 97–105. https://doi.org/10.1145/2240236.
     2240260
[25] Sumit Gulwani and Ashish Tiwari. 2006. Combining abstract interpreters. In Proceedings of
     the ACM SIGPLAN 2006 Conference on Programming Language Design and Implementation,
     Ottawa, Ontario, Canada, June 11-14, 2006, Michael I. Schwartzbach and Thomas Ball (Eds.).
     ACM, 376–386. https://doi.org/10.1145/1133981.1134026
[26] Arie Gurfinkel, Temesghen Kahsai, and Jorge A. Navas. 2015. SeaHorn: A Framework for
     Verifying C Programs (Competition Contribution). In Tools and Algorithms for the Construc-
     tion and Analysis of Systems - 21st International Conference, TACAS 2015, Held as Part
     of the European Joint Conferences on Theory and Practice of Software, ETAPS 2015, Lon-
     don, UK, April 11-18, 2015. Proceedings (Lecture Notes in Computer Science, Vol. 9035),
     Christel Baier and Cesare Tinelli (Eds.). Springer, 447–450. https://doi.org/10.1007/
     978-3-662-46681-0_41
[27] Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Kenneth L. McMillan. 2004. Ab-
     stractions from proofs. In Proceedings of the 31st ACM SIGPLAN-SIGACT Symposium on
     Principles of Programming Languages, POPL 2004, Venice, Italy, January 14-16, 2004, Neil D.
     Jones and Xavier Leroy (Eds.). ACM, 232–244. https://doi.org/10.1145/964001.964021
[28] H. Hojjat and P. Rümmer. 2018. The ELDARICA Horn Solver. In 2018 Formal Methods in
     Computer Aided Design (FMCAD). 1–7.

[29] Ryo Ikeda, Ryosuke Sato, and Naoki Kobayashi. 2023. Argument Reduction of Constrained
     Horn Clauses Using Equality Constraints. In Programming Languages and Systems - 21st Asian
     Symposium, APLAS 2023, Taipei, Taiwan, November 26-29, 2023, Proceedings (Lecture Notes
     in Computer Science, Vol. 14405), Chung-Kil Hur (Ed.). Springer, 246–265. https://doi.
     org/10.1007/978-981-99-8311-7_12

[30] Shachar Itzhaky, Nikolaj Bjørner, Thomas Reps, Mooly Sagiv, and Aditya Thakur. 2014.
     Property-Directed Shape Analysis. In Computer Aided Verification, Armin Biere and Roderick
     Bloem (Eds.). Springer International Publishing, Cham, 35–51.
[31] T. Jiang, A. Salomaa, K. Salomaa, and S. Yu. 1995. Decision Problems for Patterns. J.
     Comput. System Sci. 50, 1 (1995), 53–63. https://doi.org/10.1006/jcss.1995.1006

[32] Hari Govind V. K., Sharon Shoham, and Arie Gurfinkel. 2022. Solving constrained Horn
     clauses modulo algebraic data types and recursive functions. Proc. ACM Program. Lang. 6,
     POPL (2022), 1–29. https://doi.org/10.1145/3498722
[33] Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Martin Schäf. 2016. JayHorn: A
     Framework for Verifying Java programs. In Computer Aided Verification - 28th International
     Conference, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part I (Lecture
     Notes in Computer Science, Vol. 9779), Swarat Chaudhuri and Azadeh Farzan (Eds.). Springer,
     352–358. https://doi.org/10.1007/978-3-319-41528-4_19
[34] Aleksandr Karbyshev, Nikolaj Bjørner, Shachar Itzhaky, Noam Rinetzky, and Sharon Shoham.
     2017. Property-Directed Inference of Universal Invariants or Proving Their Absence. J. ACM
     64, 1, Article 7 (March 2017), 33 pages. https://doi.org/10.1145/3022187
[35] Juhani Karhumäki, Filippo Mignosi, and Wojciech Plandowski. 2000. The expressibility of
     languages and relations by word equations. J. ACM 47, 3 (May 2000), 483–505. https:
     //doi.org/10.1145/337244.337255



                                              25
[36] Hiroyuki Katsura, Naoki Kobayashi, Ken Sakayori, and Ryosuke Sato. 2025. Automated Cata-
     morphism Synthesis for Solving Constrained Horn Clauses over Algebraic Data Types. In Static
     Analysis - 32nd International Symposium, SAS 2025, Singapore, October 13-14, 2025, Pro-
     ceedings (Lecture Notes in Computer Science, Vol. 16100), Hakjoo Oh and Yulei Sui (Eds.).
     Springer, 305–327. https://doi.org/10.1007/978-3-032-07106-4_13
[37] Naoki Kobayashi, Ryosuke Sato, Ayumi Shinohara, and Yoshinaka Ryo. 2026. Solvable Tu-
     ple Patterns and Their Applications to Program Verification. https://doi.org/10.5281/
     zenodo.19907200
[38] Naoki Kobayashi, Ryosuke Sato, Ayumi Shinohara, and Ryo Yoshinaka. 2025. Solvable Tu-
     ple Patterns and Their Applications to Program Verification. CoRR abs/2508.20365 (2025).
     https://doi.org/10.48550/ARXIV.2508.20365 arXiv:2508.20365
[39] Naoki Kobayashi, Taro Sekiyama, Issei Sato, and Hiroshi Unno. 2025. Towards Neural-
     Network-Guided Program Synthesis and Verification. Formal Methods in System Design
     (2025).
[40] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2016. SMT-based model checking for
     recursive programs. Formal Methods Syst. Des. 48, 3 (2016), 175–205. https://doi.org/10.
     1007/s10703-016-0249-4
[41] Yurii Kostyukov, Dmitry Mordvinov, and Grigory Fedyukovich. 2021. Beyond the elementary
     representations of program invariants over algebraic data types. In PLDI ’21: 42nd ACM
     SIGPLAN International Conference on Programming Language Design and Implementation,
     Virtual Event, Canada, June 20-25, 2021, Stephen N. Freund and Eran Yahav (Eds.). ACM,
     451–465. https://doi.org/10.1145/3453483.3454055
[42] Viktor Kuncak, Huu Hai Nguyen, and Martin C. Rinard. 2006. Deciding Boolean Algebra
     with Presburger Arithmetic. J. Autom. Reason. 36, 3 (2006), 213–239. https://doi.org/
     10.1007/S10817-006-9042-1
[43] Théo Losekoot, Thomas Genet, and Thomas P. Jensen. 2023. Automata-Based Verification
     of Relational Properties of Functions over Algebraic Data Structures. In 8th International
     Conference on Formal Structures for Computation and Deduction, FSCD 2023, July 3-6, 2023,
     Rome, Italy (LIPIcs, Vol. 260), Marco Gaboardi and Femke van Raamsdonk (Eds.). Schloss
     Dagstuhl - Leibniz-Zentrum für Informatik, 7:1–7:22. https://doi.org/10.4230/LIPICS.
     FSCD.2023.7
[44] Théo Losekoot, Thomas Genet, and Thomas P. Jensen. 2024. Verification of Programs with
     ADTs Using Shallow Horn Clauses. In Static Analysis - 31st International Symposium, SAS
     2024, Pasadena, CA, USA, October 20-22, 2024, Proceedings (Lecture Notes in Computer
     Science, Vol. 14995), Roberto Giacobazzi and Alessandra Gorla (Eds.). Springer, 242–267.
     https://doi.org/10.1007/978-3-031-74776-2_10
[45] M. Lothaire. 2002. Algebraic Combinatorics on Words. Encyclopedia of Mathematics and its
     Applications, Vol. 90. Cambridge University Press.
[46] G. S. Makanin. 1977.    The Problem of Solvability of Equations in a Free Semi-
     group. Sbornik: Mathematics 32, 2 (Feb. 1977), 129–198. https://doi.org/10.1070/
     SM1977v032n02ABEH002376
[47] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2021. RustHorn: CHC-based
     Verification for Rust Programs. ACM Trans. Program. Lang. Syst. 43, 4 (2021), 15:1–15:54.
     https://doi.org/10.1145/3462205
[48] Kenneth L. McMillan. 2005. An interpolating theorem prover. Theor. Comput. Sci. 345, 1
     (2005), 101–121. https://doi.org/10.1016/J.TCS.2005.07.003
[49] Andrew R. Mitchell. 1998. Learnability of a Subclass of Extended Pattern Languages. In
     Proceedings of the Eleventh Annual Conference on Computational Learning Theory, COLT
     1998, Madison, Wisconsin, USA, July 24-26, 1998, Peter L. Bartlett and Yishay Mansour
     (Eds.). ACM, 64–71. https://doi.org/10.1145/279943.279955


                                               26
[50] Dmitry Mordvinov and Grigory Fedyukovich. 2017. Synchronizing Constrained Horn Clauses.
     In LPAR-21, 21st International Conference on Logic for Programming, Artificial Intelligence
     and Reasoning, Maun, Botswana, May 7-12, 2017 (EPiC Series in Computing, Vol. 46),
     Thomas Eiter and David Sands (Eds.). EasyChair, 338–355. https://doi.org/10.29007/
     GR5C

[51] Greg Nelson and Derek C. Oppen. 1980. Fast Decision Procedures Based on Congruence
     Closure. J. ACM 27, 2 (April 1980), 356–364. https://doi.org/10.1145/322186.322198
[52] Dirk Nowotka and Max Wiedenhöft. 2025. The Equivalence Problem of E-Pattern Languages
     with Length Constraints Is Undecidable. In 36th Annual Symposium on Combinatorial Pattern
     Matching (CPM 2025) (Leibniz International Proceedings in Informatics (LIPIcs), Vol. 331),
     Paola Bonizzoni and Veli Mäkinen (Eds.). Schloss Dagstuhl – Leibniz-Zentrum für Informatik,
     Dagstuhl, Germany, 4:1–4:23. https://doi.org/10.4230/LIPIcs.CPM.2025.4
[53] Chris Okasaki. 1995. Simple and efficient purely functional queues and deques. Journal of Func-
     tional Programming 5, 4 (1995), 583–592. https://doi.org/10.1017/S0956796800001489

[54] Alberto Pettorossi and Maurizio Proietti. 2000. Perfect Model Checking via Unfold/Fold
     Transformations. In Computational Logic - CL 2000, First International Conference, Lon-
     don, UK, 24-28 July, 2000, Proceedings (Lecture Notes in Computer Science, Vol. 1861),
     John W. Lloyd, Verónica Dahl, Ulrich Furbach, Manfred Kerber, Kung-Kiu Lau, Catuscia
     Palamidessi, Luı́s Moniz Pereira, Yehoshua Sagiv, and Peter J. Stuckey (Eds.). Springer, 613–
     628. https://doi.org/10.1007/3-540-44957-4_41
[55] Ruzica Piskac and Viktor Kuncak. 2008. Decision Procedures for Multisets with Cardinality
     Constraints. In Verification, Model Checking, and Abstract Interpretation, Francesco Logozzo,
     Doron A. Peled, and Lenore D. Zuck (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg,
     218–232.

[56] W. Plandowski. 1999. Satisfiability of word equations with constants is in PSPACE. In
     40th Annual Symposium on Foundations of Computer Science (Cat. No.99CB37039). 495–500.
     https://doi.org/10.1109/SFFCS.1999.814622
[57] William W. Pugh. 1990. Skip Lists: A Probabilistic Alternative to Balanced Trees. Commun.
     ACM 33, 6 (1990), 668–676. https://doi.org/10.1145/78973.78977

[58] Daniel Reidenbach. 2006. A non-learnable class of E-pattern languages. Theoretical Computer
     Science 350, 1 (2006), 91–102. https://doi.org/10.1016/j.tcs.2005.10.017 Algorithmic
     Learning Theory (ALT 2002).
[59] Daniel Reidenbach. 2008. Discontinuities in pattern inference. Theoretical Computer Science
     397, 1 (2008), 166–193. https://doi.org/10.1016/j.tcs.2008.02.029 Forty Years of
     Inductive Inference: Dedicated to the 60th Birthday of Rolf Wiehagen.
[60] Gabriel Ryan, Justin Wong, Jianan Yao, Ronghui Gu, and Suman Jana. 2020. CLN2INV:
     Learning Loop Invariants with Continuous Logic Networks. In 8th International Conference
     on Learning Representations, ICLR 2020. OpenReview.net.

[61] Rahul Sharma, Saurabh Gupta, Bharath Hariharan, Alex Aiken, Percy Liang, and Aditya V.
     Nori. 2013. A Data Driven Approach for Algebraic Loop Invariants. In Programming Languages
     and Systems, Matthias Felleisen and Philippa Gardner (Eds.). Springer Berlin Heidelberg,
     Berlin, Heidelberg, 574–592.
[62] Takeshi Shinohara. 1982. Polynomial time inference of pattern languages and its application.
     In Seventh IBM Symposium on Mathematical Foundations of Computer Science. 191–209.
[63] Takeshi Shinohara. 1983. Polynomial time inference of extended regular pattern languages.
     In RIMS Symposia on Software Science and Engineering, Eiichi Goto, Koichi Furukawa, Reiji
     Nakajima, Ikuo Nakata, and Akinori Yonezawa (Eds.). Springer Berlin Heidelberg, Berlin,
     Heidelberg, 115–127.


                                                27
[64] Takeshi Shinohara. 1994. Rich Classes Inferable from Positive Data: Length-Bounded Ele-
     mentary Formal Systems. Information and Computation 108, 2 (1994), 175–186. https:
     //doi.org/10.1006/inco.1994.1006
[65] John Toman, Ren Siqi, Kohei Suenaga, Atsushi Igarashi, and Naoki Kobayashi. 2020. Con-
     SORT: Context- and Flow-Sensitive Ownership Refinement Types for Imperative Programs.
     In Programming Languages and Systems - 29th European Symposium on Programming, ESOP
     2020, Held as Part of the European Joint Conferences on Theory and Practice of Software,
     ETAPS 2020, Dublin, Ireland, April 25-30, 2020, Proceedings (Lecture Notes in Computer
     Science, Vol. 12075), Peter Müller (Ed.). Springer, 684–714. https://doi.org/10.1007/
     978-3-030-44914-8_25

[66] Hiroshi Unno and Naoki Kobayashi. 2009. Dependent type inference with interpolants. In
     Proceedings of the 11th International ACM SIGPLAN Conference on Principles and Practice
     of Declarative Programming, September 7-9, 2009, Coimbra, Portugal. ACM, 277–288.
[67] Hiroshi Unno, Tachio Terauchi, and Eric Koskinen. 2021. Constraint-Based Relational Ver-
     ification. In Computer Aided Verification - 33rd International Conference, CAV 2021, Vir-
     tual Event, July 20-23, 2021, Proceedings, Part I (Lecture Notes in Computer Science,
     Vol. 12759), Alexandra Silva and K. Rustan M. Leino (Eds.). Springer, 742–766. https:
     //doi.org/10.1007/978-3-030-81685-8_35
[68] Hiroshi Unno, Sho Torii, and Hiroki Sakamoto. 2017. Automating Induction for Solv-
     ing Horn Clauses. In Computer Aided Verification - 29th International Conference, CAV
     2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part II (Lecture Notes in Com-
     puter Science, Vol. 10427), Rupak Majumdar and Viktor Kuncak (Eds.). Springer, 571–591.
     https://doi.org/10.1007/978-3-319-63390-9_30
[69] Takashi Yokomori. 2003. Polynomial-time identification of very simple grammars from positive
     data. Theoretical Computer Science 298, 1 (2003), 179–206. https://doi.org/10.1016/
     S0304-3975(02)00423-1 Selected Papers in honour of Setsuo Arikawa.
[70] T. Yokomori and S. Kobayashi. 1998. Learning local languages and their application to DNA
     sequence analysis. IEEE Transactions on Pattern Analysis and Machine Intelligence 20, 10
     (1998), 1067–1079. https://doi.org/10.1109/34.722617

[71] Ryo Yoshinaka. 2006. Polynomial-Time Identification of an Extension of Very Simple Gram-
     mars from Positive Data. In Grammatical Inference: Algorithms and Applications, Yasub-
     umi Sakakibara, Satoshi Kobayashi, Kengo Sato, Tetsuro Nishino, and Etsuji Tomita (Eds.).
     Springer Berlin Heidelberg, Berlin, Heidelberg, 45–58.
[72] Ryo Yoshinaka. 2008. Identification in the Limit of k,l-Substitutable Context-Free Languages.
     In Grammatical Inference: Algorithms and Applications, Alexander Clark, François Coste, and
     Laurent Miclet (Eds.). Springer Berlin Heidelberg, Berlin, Heidelberg, 266–279.
[73] Ryo Yoshinaka. 2011. Efficient learning of multiple context-free languages with multidimen-
     sional substitutability from positive data. Theoretical Computer Science 412, 19 (2011), 1821–
     1831. https://doi.org/10.1016/j.tcs.2010.12.058 Algorithmic Learning Theory (ALT
     2009).
[74] He Zhu, Stephen Magill, and Suresh Jagannathan. 2018. A data-driven CHC solver. In Pro-
     ceedings of the 39th ACM SIGPLAN Conference on Programming Language Design and Im-
     plementation, PLDI 2018. ACM, 707–721. https://doi.org/10.1145/3192366.3192416
[75] He Zhu, Aditya V. Nori, and Suresh Jagannathan. 2015. Learning refinement types. In
     Proceedings of the 20th ACM SIGPLAN International Conference on Functional Program-
     ming, ICFP 2015, Vancouver, BC, Canada, September 1-3, 2015. ACM, 400–411. https:
     //doi.org/10.1145/2784731.2784766




                                                28
[76] He Zhu, Gustavo Petri, and Suresh Jagannathan. 2016. Automatically learning shape specifica-
     tions. In Proceedings of the 37th ACM SIGPLAN Conference on Programming Language Design
     and Implementation, PLDI 2016, Santa Barbara, CA, USA, June 13-17, 2016, Chandra Krintz
     and Emery D. Berger (Eds.). ACM, 491–507. https://doi.org/10.1145/2908080.2908125




                                               29
Appendix
A       Proofs
A.1       Proofs and Additional Definitions for Sections 2 and 3
This section provides proofs omitted in Sections 2 and 3.
   We first show basic properties in Sections A.1.1–A.1.3. The dependency of each main property
on basic properties is summarized in Table 3, so that it is easy to discuss properties of the extensions
and variations of STPs considered in Section 4.

                        Table 3: Required Basic Properties for Each Main Property


  Properties                                        Required Properties
  Soundness (Theorem 2.1)                           Lemma A.2
  Soundness 2 (Theorem 3.1)                         Lemmas A.1, A.3, and A.10
  Completeness (Theorems 3.2 an 3.3)                Lemmas A.1 and A.11 and Theorem 2.1
  Minimality (Theorem 3.4)                          Lemmas A.1, A.3, A.4, A.6, A.7, Lemma A.8, and A.10
                                                    Lemmas A.14 and A.15,
  Characteristic Data (Theorem 3.5)
                                                    in addition to all the lemmas above
  Learnability of STPs                              Soundness and the existence of characteristic data
  (Theorems 3.6 and 3.8)                            (Theorems 2.1 and 3.5)
  Learnability of CSTPs
                                                    Soundness, completeness and Lemma A.16
  (Theorems 3.6 and 3.7)
  Complexity of Decision Prob-
                                                    Lemmas A.4, A.6, and A.7
  lems (Theorem 3.9)
  Decidability of Satisfiability
                                                    Lemma A.4 and decidability of word equations
  (Theorem 3.10)




A.1.1      Properties of −→
Lemma A.1. Let x     e be mutually distinct variables. If (t, [M/ex]) −→n (t′ , Θ′ ) −→,
                                                                                      ̸   then there exists
 ′′                          n  ′′   ′           ′       ′′
t such that (ex, [M/e x]) −→ (t , Θ ) −↛   and t = [t /e   x]t.
     Conversely, if (e     x]) −→n (t, Θ′ ), then (t0 , [M/e
                     x, [M/e                                             x]t0 , Θ′ ) for any tuple pattern
                                                             x]) −→n ([t/e
t0 .
Proof. This follows by a straightforward (simultaneous) induction on the length n of the rewriting
sequence, with case analysis used in the first step. Note that in the rules for (t, Θ) −→ (t′ , Θ′ ),
there is no condition on t in the premise.
Lemma A.2. If (t1 , Θ1 ) −→ (t2 , Θ2 ), then Θ1 t1 = Θ2 t2 .
Proof. This follows by a straightforward case analysis on the rule used for deriving (t1 , Θ1 ) −→
(t2 , Θ2 ).

A.1.2      Properties of ⇝
Lemma A.3. If t ⇝ t′ , then [t1 /e
                                 x]t ⇝∗ [t1 /e
                                             x]t′ .
Proof. Trivial by the definition of ⇝. We have actually [t1 /e                            x]t′ or [t1 /e
                                                                               x]t ⇝ [t1 /e                          x]t′ , and
                                                                                                          x]t = [t1 /e
the latter occurs only when empty sequences are substituted for some variables. For example, when
t = (x2 x1 , x2 , . . .) ⇝ (x1 , x2 , . . .) = t′ and t1 = (p1 , ϵ, . . .), [t1 /e                            x]t′ .
                                                                                 x]t = (p1 , ϵ, . . .) = [t1 /e
    When t1 ⇝ t2 holds, we define a partial function ⟨t1 ⇝ t2 ⟩ on tuple patterns as follows.




                                                              30
Definition A.1 (⟨t1 ⇝ t2 ⟩). Let t0 , t1 and t2 be tuple patterns such that t1 ⇝ t2 . We define the
tuple pattern ⟨t1 ⇝ t2 ⟩(t0 ) such that t0 ⇝∗ ⟨t1 ⇝ t2 ⟩(t0 ) as follows, by case analysis on the rule
used for deriving t1 ⇝ t2 :
    • Case PR-Prefix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = pi · p′j
      and pi ̸= ϵ for some i, j and p′k = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and qi is
      a prefix of qj , then ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where qj′ = qi \qj and qk′ = qk for k ̸= j.
      (Recall that qi \qj denotes q such that qi · q = qj . We have t0 ⇝ ⟨t1 ⇝ t2 ⟩(t0 ) if q2 ̸= ϵ, and
      t0 = ⟨t1 ⇝ t2 ⟩(t0 ) if q2 = ϵ.) Otherwise, ⟨t1 ⇝ t2 ⟩(t0 ) is undefined.
    • Case PR-Suffix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = p′j · pi and
      pi ̸= ϵ for some i, j and p′k = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and qi is a suffix
      of qj , then ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where qj′ = qj /qi and qk′ = qk for k ̸= j. Otherwise,
      ⟨t1 ⇝ t2 ⟩(t0 ) is undefined.
    • Case PR-CPrefix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = ap′j for
      some j and p′k = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and a is a prefix of qj , then
      ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where qj′ = a\qj and qk′ = qk for k ̸= j. Otherwise, ⟨t1 ⇝ t2 ⟩(t0 )
      is undefined.
    • Case PR-CSuffix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = p′j a for
      some j and p′k = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and a is a suffix of qj , then
      ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where qj′ = qj /a and qk′ = qk for k ̸= j. Otherwise, ⟨t1 ⇝ t2 ⟩(t0 )
      is undefined.
    • Case PR-Epsilon:                     In this case, t1 = (p1 , . . . , pj−1 , ϵ, pj+1 , . . . , pn ) and t2 =
      (p1 , . . . , pj−1 , pj+1 , . . . , pn ). If t0 is of the form (q1 , . . . , qj−1 , ϵ, qj+1 , . . . , qn ), then ⟨t1 ⇝
      t2 ⟩(t0 ) := (q1 , . . . , qj−1 , qj+1 , . . . , qn ). Otherwise, ⟨t1 ⇝ t2 ⟩(t0 ) is undefined.
Note that ⟨t1 ⇝ t2 ⟩ above depends on which rule has been used for deriving t1 ⇝ t2 ; for example,
⟨(ax, a) ⇝ (x, a)⟩(ap2 p1 , ap2 ) = (p1 , ap2 ) if (ax, a) ⇝ (x, a) has been derived by R-Prefix and
⟨(ax, a) ⇝ (x, a)⟩(ap2 p1 , ap2 ) = (p2 p1 , ap2 ) if (ax, a) ⇝ (x, a) has been derived by R-CPrefix.
Thus, when we write ⟨t1 ⇝ t2 ⟩, we assume that t1 ⇝ t2 carries information about the rule used for
deriving t1 ⇝ t2 .
   We defined ⟨t1 ⇝ t2 ⟩(t0 ) above so that the reduction t0 ⇝∗ ⟨t1 ⇝ t2 ⟩(t0 ) “simulates” the
reduction t1 ⇝ t2 in the following sense.
Lemma A.4.   1. If t1 ⇝ t′1 and L(t0 ) ⊆ L([t/e
                                              x]t1 ), then ⟨t1 ⇝ t′1 ⟩(t0 ) is well defined and
       ∗       ′
   t0 ⇝ ⟨t1 ⇝ t1 ⟩(t0 ).
   2. If ⟨t1 ⇝ t′1 ⟩(t0 ) is well defined, then L(t0 ) ⊆ L([t/e  x]t1 ) if and only if L(⟨t1 ⇝ t′1 ⟩(t0 )) ⊆
               ′
      L([t/ex]t1 ); and L(t0 ) ⊇ L([t/ex]t1 ) if and only if L(⟨t1 ⇝ t′1 ⟩(t0 )) ⊇ L([t/e
                                                                                        x]t′1 ).
Proof. Case analysis on the rule used for deriving t1 ⇝ t′1 . Since the other cases are similar
or simpler, we discuss only the case for PR-Prefix. We may assume, without loss of generality,
t1 = (p2 p1 , p2 , . . . , pn ) and t′1 = (p1 , p2 , . . . , pn ) with p2 ̸= ϵ. To show (1), assume L(t0 ) ⊆ L([t/e
                                                                                                                  x]t1 ).
Then for any (s1 , s2 , . . . , sn ) ∈ L(t0 ), s2 must be a prefix of s1 . Thus t0 must also be of the form
(q2 q1 , q2 , . . . , qn ). (To see this, suppose t0 = (q1′ , q2 , . . .) and q2 is not a prefix of q1′ . Then either
(i) q1′ q1′′ = q2 with q1′′ ̸= ϵ (i.e., q1′ is a strict prefix of q2 ) or (ii) q1′ = qα1 q1′′ and q2 = qα2 q2′′ with
α1 , α2 ∈ Σ ∪ V and α1 ̸= α2 (i.e., α1 , α2 are the first letters or variables that differ between q1′ and
q2 ). In case (i), let θ be a substitution such that θq1′′ ̸= ϵ, and in case (ii), let θ be a substitution
such that θα1 ̸= θα2 . Then s2 = θq2 is not a prefix of s1 = θq1′ . Thus, q2 must be a prefix of q1′ . )
Therefore, ⟨t1 ⇝ t′1 ⟩(t0 ) is well defined, and t0 ⇝∗ ⟨t1 ⇝ t′1 ⟩(t0 ).
     To show (2), suppose ⟨t1 ⇝ t′1 ⟩(t0 ) is well defined. Then, t0 = (q2 q1 , q2 , . . . , qn ) and t′0 := ⟨t1 ⇝
 ′
t1 ⟩(t0 ) = (q1 , q2 , . . . , qn ) where q2 may be ϵ. Thus, we have:
                            L(t′0 ) = {(w2 \w1 , w2 , . . . , wn ) | (w1 , . . . , wn ) ∈ L(t0 )}
                            L(t0 ) = {(w2 w1 , w2 , . . . , wn ) | (w1 , . . . , wn ) ∈ L(t′0 )}
                           x]t′1 ) = {(w2 \w1 , w2 , . . . , wn ) | (w1 , . . . , wn ) ∈ L([t/e
                      L([t/e                                                                  x]t1 )}
                      L([t/e                                                                x]t′1 )},
                           x]t1 ) = {(w2 w1 , w2 , . . . , wn ) | (w1 , . . . , wn ) ∈ L([t/e
from which the required properties follow immediately.

                                                             31
   Next, we will prove the weak confluence of ⇝ (up to permutations). To that end, we prepare
the following lemma.
Lemma A.5. Suppose pq1 = q2 p for p, q1 , q2 ∈ (Σ ∪ V)∗ . Then, there exists t such that (q1 , p) ⇝∗
t ∗ (q2 , p).
⇝

Proof. This follows by induction on |p|. If p = ϵ, then q1 = q2 . Therefore, the property holds for
t = (q1 , p). Otherwise, by the assumption pq1 = q2 p, either p is a prefix of q2 , or q2 is a prefix of p.
   In the former case, q2 = pr with q1 = rp. Thus, we have (q1 , p) ⇝ t ∗ (q2 , p) for t = (r, p).      ⇝
   In the latter case, p = q2 p′ = p′ q1 . We may assume that q2 ̸= ϵ, since (q1 , p) = (ϵ, p) = (q2 , p)
otherwise. Thus, we have |p′ | < |p|. By the induction hypothesis, there exists t such that (q1 , p′ ) ⇝∗
t ∗ (q2 , p′ ). Thus, we have (q1 , p) ⇝ (q1 , p′ ) ⇝∗ t ∗ (q2 , p′ ) (q2 , p) as required.
⇝                                                                      ⇝              ⇝

Remark A.1. The lemma above also follows immediately from the following property of words
(cf. [45], Proposition 12.1.2): “If p, q1 , q2 ∈ Σ∗ , pq1 = q2 p and q1 ̸= ϵ, then there exists r, s ∈ Σ∗
and an integer n such that p = (rs)n r, q1 = sr, and q2 = rs.” By using this property, we obtain
(q1 , p) ⇝∗ (sr, r) ⇝ (s, r) (rs, r) ∗ (q2 , p).
                                  ⇝            ⇝

    We write t ∼ t′ if t′ is a permutation of t. For example, (x, xy) ∼ (xy, x). The following lemma
states that ⇝ is weakly confluent up to ∼.
Lemma A.6 (weak confluence of ⇝ up to ∼). If t ⇝ t1 and t ⇝ t2 , then there exist t′1 and t′2 such
that t1 ⇝∗ t′1 ∼ t′2 ∗ t2 .
                       ⇝

Proof. It is sufficient to consider the cases where t1 ̸= t2 and the parts involved in the two reductions
overlap. Without loss of generality, we may assume that the first element p1 is principal in t ⇝ t1 .
We thus need to consider only the following cases; due to the symmetry between prefix and suffix,
the cases involving only suffixes are omitted.
    • Case t = (p2 p′1 , p2 , p3 , . . . , pn ) ⇝ (p′1 , p2 , p3 , . . . , pn ) = t1 and t = (p3 p′′1 , p2 , p3 , . . . , pn ) ⇝
      (p′′1 , p2 , p3 , . . . , pn ) = t2 (i.e., both reductions use PR-Prefix, and p1 is principal in both
      reductions).
      By p2 p′1 = p3 p′′1 , p2 and p3 are in the prefix relation. By symmetry, we may assume that
      p2 = p3 p′2 , with p′′1 = p′2 p′1 . Then we have:

                   t1 = (p′1 , p3 p′2 , p3 , . . . , pn ) ⇝ (p′1 , p′2 , p3 , . . . , pn )
                   t2 = (p′2 p′1 , p3 p′2 , p3 , . . . , pn ) ⇝ (p′2 p′1 , p′2 , p3 , . . . , pn ) ⇝∗ (p′1 , p′2 , p3 , . . . , pn ),

      as required. In the second reduction step for t2 , (p′2 p′1 , p′2 , p3 , . . . , pn ) = (p′1 , p′2 , p3 , . . . , pn ) if
      p′2 = ϵ and (p′2 p′1 , p′2 , p3 , . . . , pn ) ⇝ (p′1 , p′2 , p3 , . . . , pn ) otherwise.
    • Case t = (p2 p′1 , p2 , p3 , . . . , pn ) ⇝ (p′1 , p2 , p3 , . . . , pn ) = t1 and t = (p1 , p2 , p1 p′3 , . . . , pn ) ⇝
      (p1 , p2 , p′3 , . . . , pn ) = t2 (i.e., both reductions use PR-Prefix, and p1 is auxiliary in t ⇝ t2 ).
      In this case, we have p1 = p2 p′1 and p3 = p1 p′3 = p2 p′1 p′3 . Then we have:

                   t1 = (p′1 , p2 , p2 p′1 p′3 , . . . , pn ) ⇝ (p′1 , p2 , p′1 p′3 , . . . , pn ) ⇝∗ (p′1 , p2 , p′3 , . . . , pn )
                   t2 = (p2 p′1 , p2 , p′3 , . . . , pn ) ⇝ (p′1 , p2 , p′3 , . . . , pn ),

      as required. In the second reduction step for t1 , (p′1 , p2 , p′1 p′3 , . . . , pn ) = (p′1 , p2 , p′3 , . . . , pn ) if
      p′1 = ϵ and (p′1 , p2 , p′1 p′3 , . . . , pn ) ⇝ (p′1 , p2 , p′3 , . . . , pn ) otherwise.
    • Case t = (p2 p′1 , p2 , . . . , pn ) ⇝ (p′1 , p2 , . . . , pn ) = t1 and t = (ap′′1 , p2 , . . . , pn ) ⇝
      (p′′1 , p2 , . . . , pn ) = t2 (i.e., t ⇝ t1 uses PR-Prefix, while t ⇝ t2 uses PR-CPrefix, and
      p1 is principal in both reductions).
      In this case, p2 = ap′2 with p′′1 = p′2 p′1 . Thus, we have:

                           t1 = (p′1 , ap′2 , . . . , pn ) ⇝ (p′1 , p′2 , . . . , pn )
                           t2 = (p′2 p′1 , ap′2 , . . . , pn ) ⇝ (p′2 p′1 , p′2 , . . . , pn ) ⇝∗ (p′1 , p′2 , . . . , pn ),

      as required. In the second step for t2 , (p′2 p′1 , p′2 , . . . , pn ) = (p′1 , p′2 , . . . , pn ) if p′2 = ϵ and
      (p′2 p′1 , p′2 , . . . , pn ) ⇝ (p′1 , p′2 , . . . , pn ) otherwise.


                                                                     32
   • Case t = (p2 p′1 , p2 , . . . , pn ) ⇝ (p′1 , p2 , . . . , pn ) = t1 and t = (p1 , ap′2 , . . . , pn ) ⇝
     (p1 , p′2 , . . . , pn ) = t2 (i.e., t ⇝ t1 uses PR-Prefix, while t ⇝ t2 uses PR-CPrefix, and
     the auxiliary element p2 in the former reduction is principal in the latter).
     In this case, p2 = ap′2 . Thus, we have:

                          t1 = (p′1 , ap′2 , . . . , pn ) ⇝ (p′1 , p′2 , . . . , pn )
                          t2 = (ap′2 p′1 , p′2 , . . . , pn ) ⇝ (p′2 p′1 , p′2 , . . . , pn ) ⇝∗ (p′1 , p′2 , . . . , pn ),

     as required. In the second step for t2 , (p′2 p′1 , p′2 , . . . , pn ) = (p′1 , p′2 , . . . , pn ) if p′2 = ϵ and
     (p′2 p′1 , p′2 , . . . , pn ) ⇝ (p′1 , p′2 , . . . , pn ) otherwise.
   • Case where t = (p2 p′1 , p2 , . . . , pn ) ⇝ (p′1 , p2 , . . . , pn ) = t1 and t = (p′′1 p2 , p2 , . . . , pn ) ⇝
     (p′′1 , p2 , . . . , pn ) = t2 (i.e., p1 is principal and p2 is auxiliary in both reductions, and t ⇝ t1 uses
     PR-Prefix while t ⇝ t2 uses PR-Suffix). In this case, p2 p′1 = p′′1 p2 . Thus, by Lemma A.5,
     there exists t3 such that t1 ⇝∗ t3 ∗ t2 .           ⇝

   • Case where t = (p2 p′1 , p2 , . . . , pn ) ⇝ (p′1 , p2 , . . . , pn ) = t1 and t = (p′′1 p3 , p2 , p3 , . . . , pn ) ⇝
     (p′′1 , p2 , p3 , . . . , pn ) = t2 (i.e., p1 is principal in both reductions, and p2 is auxiliary in the
     former reduction while p3 is auxiliary in the latter; t ⇝ t1 uses PR-Prefix, t ⇝ t2 uses
     PR-Suffix). In this case, p2 p′1 = p′′1 p3 ; so, either (i) p′′1 = p2 p′′′                   ′        ′′′
                                                                                      1 and p1 = p1 p3 , or (ii)
                ′′ ′                 ′ ′
     p2 = p1 p2 and p3 = p2 p1 . In case (i), we have:

                                      t1 = (p′′′                               ′′′
                                             1 p3 , p2 , p3 , . . . , pn ) ⇝ (p1 , p2 , p3 , . . . , pn )
                                      t2 = (p2 p′′′                            ′′′
                                                1 , p2 , p3 , . . . , pn ) ⇝ (p1 , p2 , p3 , . . . , pn ).

     In case (ii), we have:

                  t1 = (p′1 , p′′1 p′2 , p′2 p′1 , . . . , pn ) ⇝ (p′1 , p′′1 p′2 , p′2 , . . . , pn ) ⇝ (p′1 , p′′1 , p′2 , . . . , pn )
                  t2 = (p′′1 , p′′1 p′2 , p′2 p′1 , . . . , pn ) ⇝ (p′′1 , p′2 , p′2 p′1 , . . . , pn ) ⇝ (p′′1 , p′2 , p′1 , . . . , pn )
                  (p′1 , p′′1 , p′2 , . . . , pn ) ∼ (p′′1 , p′2 , p′1 , . . . , pn ),

     as required. Here, notice that reductions are confluent only up to the permutation relation
     ∼.
   • Case where t = (p2 p′1 , p2 , . . . , pn ) ⇝ (p′1 , p2 , . . . , pn ) = t1 and t = (p1 , p′2 p3 , p3 , . . . , pn ) ⇝
     (p1 , p′2 , p3 , . . . , pn ) = t2 (i.e. the auxiliary element p2 in the former reduction is principal in
     the latter, and t ⇝ t1 uses PR-Prefix while t ⇝ t2 uses PR-Suffix). In this case, we have
     p1 = p2 p′1 and p2 = p′2 p3 . Then, we have:

                  t1 = (p′1 , p′2 p3 , p3 , . . . , pn ) ⇝ (p′1 , p′2 , p3 , . . . , pn )
                  t2 = (p′2 p3 p′1 , p′2 , p3 , . . . , pn ) ⇝ (p3 p′1 , p′2 , p3 , . . . , pn ) ⇝ (p′1 , p′2 , p3 , . . . , pn )

     as required.


   Recall that #(p1 , . . . , pk ) = |p1 · · · pk | + k.
Lemma A.7. If t ⇝ t′ , then #t > #t′ .

Proof. This follows immediately by the case analysis on the rule used for deriving t ⇝ t′ .
Lemma A.8. If t1 ∼⇝ t2 , then t1 ⇝∼ t2 .
Proof. This follows immediately from the definition of ⇝.
                                                                                                  ∗
Lemma A.9 (Church-Rosser property of ⇝ up to ∼). If tL,1                                      ⇝       tL ∼ tR ⇝∗ tR,1 , then there exist
tL,2 and tR,2 such that tL,1 ⇝∗ tL,2 ∼ tR,2 ∗ tR,1 .           ⇝




                                                                         33
Proof. This follows immediately from the standard fact that weak confluence (Lemma A.6) and
strong normalization (implied by Lemma A.7) implies the Church-Rosser property. For com-
pleteness, we provide a proof. We show the lemma by induction on #tL (= #tR ). Suppose
tL,1 ∗ tL ∼ tR ⇝∗ tR,1 . If tL = tL,1 or tR = tR,1 , the result follows immediately by Lemma A.8.
   ⇝
Otherwise, we have tL ⇝ t′L,1 ⇝∗ tL,1 and tR ⇝ t′R,1 ⇝∗ tR,1 . By Lemma A.6, there exist t′′L,1 and
t′′R,1 such that t′L,1 ⇝∗ t′′L,1 ∼ t′′R,1 ∗ t′R,1 . By the induction hypothesis, we also have:
                                          ⇝

                                              tL,1 ⇝∗ tL,3 ∼ t′L,3   ⇝  ∗ ′′
                                                                         tL,1
                                              tR,1 ⇝∗ tR,3 ∼ t′R,3    ⇝ ∗ ′′
                                                                          tR,1 .

By applying the induction hypothesis to t′L,3 ∗ t′′L,1 ∼ t′′R,1 ⇝∗ t′R,3 , we obtain t′L,3 ⇝∗ t′L,2 ∼
                                                          ⇝
t′R,2 ∗ t′R,3 . As tL,1 ⇝∗ tL,3 ∼ t′L,3 ⇝∗ t′L,2 and tR,1 ⇝∗ tR,3 ∼ t′R,3 ⇝∗ t′R,2 , by Lemma A.8, there
   ⇝
exist tL,2 and tR,2 such that tL,1 ⇝∗ tL,2 ∼ t′L,2 and tR,1 ⇝∗ tR,2 ∼ t′R,2 . Thus, we have

                                    tL,1 ⇝∗ tL,2 ∼ t′L,2 ∼ t′R,2 ∼ tR,2       ⇝    ∗
                                                                                       tR,1 ,

as required.

A.1.3    Correspondence between −→ and ⇝
Lemma A.10. If (e     x]) −→ (t, [M ′ /e
                x, [M/e                y ]), then t ⇝ ye.
Proof. This follows by a straightforward case analysis on (e     x]) −→ (t, [M ′ /e
                                                           x, [M/e                y ]).
Lemma A.11. Suppose M |= t. If t ⇝ t′ , then (e          x]) −→ (t′′ , [M ′ /e
                                                   x, [M/e                   y ]) for some t′′ , ye, and
  ′                                     ′     ′′      ′    ′
M . Furthermore, if M |=s t, then t = [t /e
                                          y ]t and M |=s t .

Proof. Suppose M, Θ |= t and t ⇝ t′ . We perform case analysis on the rule used for deriving t ⇝ t′ .
   • Case PR-Prefix: We may assume, without loss of generality, t = (p2 p1 , p2 , . . . , pn ) and
     t′ = (p1 , p2 , . . . , pn ), with p2 ̸= ϵ. By M, Θ |= t, we have M [∗][1] = M [∗][2] · se where se = Θp1 .
     If M [∗][2] = e  ϵ, then R-Epsilon is applicable to (e        x, [M/e    x]). Otherwise, let ye = (x′1 , x2 , . . . , xn )
                          ′                         ′
     with t1 = (x2 x1 , x2 , . . . , xn ) and M = (e     s, M [∗][2], . . . , M [∗][n]). Then, we have (e
                                                                                                        x, [M/e     x]) −→
     (t1 , [M ′ /e
                 y ]). Furthermore, if M, Θ |=s t, then M [∗][2] ̸= e            ϵ. Therefore, the latter case applies
     and we have t = [t′ /e        y ]t1 and M ′ , Θ |= t′ as required.
   • Case PR-CPrefix: In this case t = (ap1 , p2 , . . . , pn ) and t′ = (p1 , . . . , pn ). By M, Θ |= t, we
     have M [∗][i] = a · se. Thus, R-CPrefix is applicable to obtain

                                        (e     x]) −→ (t′′ , [M ′ /(x′1 , x2 , . . . , xn )])
                                         x, [M/e

      for t′′ = (ax′1 , x2 , . . . , xn ), with M ′ [∗][i] = se and M ′ [∗][j] = M [∗][j] for j ̸= i. Thus, we also
      have t = [t′ /e
                    y ]t′′ , and M, Θ |=s t implies M ′ , Θ |=s t′ .
   • Cases for PR-Suffix and PR-CSuffix:                          analogous to the cases for PR-Prefix and
     PR-CPrefix respectively.

   • Case PR-Epsilon: We may assume, without loss of generality, t = (ϵ, p2 , . . . , pn ) and
     t′ = (p2 , . . . , pn ). The required result holds for t′′ = (ϵ, x2 , . . . , xn ), M ′ = M ↑1 and
     ye = (x2 , . . . , xn ).



A.1.4    Proof of Soundness (Theorems 2.1 and 3.1)
Theorem 2.1 is a trivial consequence of Lemma A.2.
Proof of Theorem 2.1. Suppose (e     x]) −→∗ (t, Θ). By Lemma A.2, we have M = [M/e
                               x, [M/e                                            x]e
                                                                                    x = Θt,
i.e., M, Θ |= t as required.




                                                             34
Proof of Theorem 3.1. This follows by induction on the length of the rewriting sequence
(e     x]) −→∗ (t, Θ). The base case where (e
 x, [M/e                                    x, [M/e
                                                  x]) = (t, Θ) follows immediately. Suppose

                                       (e
                                        x, [M/e                 y ]) −→k (t, Θ).
                                              x]) −→ (t1 , [M1 /e

By Lemma A.1, there exist t′ such that (e          y ]) −→k (t′ , Θ) with t = [t′ /e
                                          y , [M1 /e                               y ]t1 . By the induction
hypothesis, t ∈ T . By Lemma A.10, we have t1 ⇝ ye. By Lemma A.3, we have t = [t′ /e
               ′
                                                                                                    y ]t1 ⇝∗
  ′         ′
[t /e  y = t . Thus, we have t ∈ T as required.
    y ]e

A.1.5      Proofs of Completeness (Theorems 3.2 and 3.3)
Proof of Theorem 3.2. For (I), suppose M |=s t and t ∈ Tn . By the latter condition, there exists
a rewriting sequence t ⇝∗ ye for mutually distinct variables ye. We show (e     x]) −→∗ (t, Θ) for
                                                                          x, [M/e
                                                                   ∗
some Θ by induction on the length of the rewriting sequence t ⇝ ye. The base case where t = ye
follows immediately. Suppose
                                           t ⇝ t′ ⇝∗ ye.
By Lemma A.11, we have

                           (e     x]) −→ (t1 , [M ′ /e
                            x, [M/e                  z ])           t = [t′ /e
                                                                             z ]t1      M ′ |=s t′ .

By the induction hypothesis, we have

                                                  z , [M ′ /e
                                                 (e         z ]) −→∗ (t′ , Θ)

for some Θ. By Lemma A.1, we have (t1 , [M ′ /e         z ]) −→∗ ([t′ /e
                                                                       z ]t1 , Θ) = (t, Θ). Thus, we have
                ∗
(e
 x, [M/ex]) −→ (t, Θ) as required.
    For (II), suppose M, Θ |= t. Let x e = x1 , . . . , xℓ be the variables x such that Θ(x) = e       ϵ. Then
we have M = Θ([e     x]t), i.e., M |=s [e
                   ϵ/e                  ϵ/e
                                          x]t. By (I), we have (e    y , [M/e  y ]) −→∗ ([e x]t, Θ′ ) for some
                                                                                          ϵ/e
Θ′ . Let t′ be an STP such that ([e    x]t, Θ′ ) −→∗ (t′ , Θ′′ ) −→.
                                     ϵ/e                          ̸     Then L(t′ ) ⊆ L([e    x]t) ⊆ L(t) as
                                                                                            ϵ/e
required.
Proof of Theorem 3.3. The condition M |= CTPinf(M ) follows immediately from Theorem 2.1.
    Suppose γ = t1 ∧ · · · ∧ tm is a CSTP and M |= γ. Then there exists Θk such that Θk tk = M
for each k ∈ {1, . . . , m}. Let x    e = x1 , . . . , xℓ be the variables x such that Θk (x) = e   ϵ. Then we
have M = Θk ([e    ϵ/ex]tk ), i.e., M |=s [e
                                           ϵ/e x]tk . By Theorem 3.2, we have (e   y , [M/ey ]) −→∗ ([eϵ/e
                                                                                                         x]tk , Θ).
Let t′k be an STP such that ([e         x]tk , Θ) −→∗ (t′k , Θ′ ) −→.
                                      ϵ/e                          ̸    Then t′k is a conjunct of CTPinf(M )
and L(t′k ) ⊆ L([e     x]tk ). Thus, we have L(CTPinf(M )) ⊆ L(t′k ) ⊆ L([e
                     ϵ/e                                                             ϵ/ex]tk ) ⊆ L(tk ) for every
k ∈ {1, . . . , m}, which implies L(CTPinf(M )) ⊆ L(γ).

A.1.6      Proof of Minimality (Theorem 3.4)
We prepare a few lemmas.
Lemma A.12. If (e       x, [M/ex]) −→
                                    ̸   and M |= t with t ∈ Tn , then t is of the form (x1 , . . . , xn ) where
x1 , . . . , xn are mutually distinct variables.
Proof. If t ∈ Tn is not of the given form, then t ⇝ t′ for some t′ . By Lemma A.11, (e     x]) −→
                                                                                     x, [M/e
(t′′ , Θ) for some t′′ and Θ, which contradicts the assumption (e
                                                                x, [M/ex]) −→.
                                                                            ̸
    The following is a key lemma.

Lemma A.13. Suppose (p1 , . . . , pn ) ⇝ (p′1 , . . . , p′m ). Then, (p1 , . . . , pn ) ∈ Tn if and only if
(p′1 , . . . , p′m ) ∈ Tm .
Proof. The ’if’ direction follows immediately from the definition. To show the converse, sup-
pose (p1 , . . . , pn ) ⇝ (p′1 , . . . , p′m ) and (p1 , . . . , pn ) is solvable, i.e., (p1 , . . . , pn ) ⇝∗ (x1 , . . . , xk )
for some mutually distinct variables x1 , . . . , xk . By Lemma A.9, there exist t3 and t4 such that
(p′1 , . . . , p′m ) ⇝∗ t3 ∼ t4 ∗ (x1 , . . . , xk ). The last condition implies (x1 , . . . , xk ) ∼ t3 , and thus,
                                ⇝
(p′1 , . . . , p′m ) is solvable.



                                                               35
Proof of Theorem 3.4. The proof proceeds by induction on the length of the rewriting sequence
(e
 x, [M/ex]) −→∗ (t1 , Θ1 ).
    In the base case, (e      x]) = (t1 , Θ1 ) ̸−→. By Lemma A.12, t0 must be a tuple of mutually
                        x, [M/e
distinct variables ye. Thus, L(t1 ) = L(t0 ) = Σ∗ × · · · × Σ∗ as required.
                                                |   {z       }
                                                            n
    In the induction step, we have (e   x, [M/ex]) −→ (t′ , [M ′ /e
                                                                  y ]) −→k (t1 , Θ1 ). By Lemma A.10, we
      ′
have t ⇝ ye. By Lemma A.1, there exists t2 such that (e     y , [M ′ /e                                 y ]t′ . By
                                                                      y ]) −→k (t2 , Θ1 ) and t1 = [t2 /e
                                            ′                                                 ′      ′
the assumption L(t0 ) ⊆ L(t1 ) = [t2 /ey ]t and Lemma A.4 with t1 ⇝ ye, we have (i) t0 := ⟨t ⇝ ye⟩(t0 )
is well-defined; (ii) L(t′0 ) ⊆ L([t2 /e  y ) = L(t2 ); and (iii) L(t′0 ) ⊆ L(t2 ) implies L(t0 ) = L(t1 ).
                                       y ]e
Furthermore, by T ∋ t0 ⇝ t0 and Lemma A.13, t′0 is also solvable. By (ii) and t′0 ∈ T , we can
                              ∗ ′

apply the induction hypothesis to obtain L(t′0 ) = L(t2 ), and by (iii), we obtain L(t0 ) = L(t1 ) as
required.

A.1.7     Proof of the Existence of Characteristic Data (Theorem 3.5)
To prove Theorem 3.5, we first define characteristic learning data M t for each solvable tuple pattern
t. Let t = (p1 , . . . , pn ) be a solvable tuple pattern. Since t is solvable, t contains at most n distinct
variables x1 , . . . , xk with k ≤ n. (Note that, at each reduction step by ⇝, the set of variables
occurring in the tuple pattern does not change, and the number of elements may only monotonically
decrease.) Let a, b be two distinct variables of Σ, and α1 , . . . , αn be binary codewords for 1, . . . , n
using a, b such that |αi | = O(log n) and for all i, j(i ̸= j), αi is neither a prefix nor a suffix of αj .
Let βi (i = 1, . . . , n) be [a/b, b/a]αi . We define M t as:12
                                                                     
                                             [e x]p1 · · · [e
                                              α/e            α/ex]pn
                                                             e x]pn .
                                              e x]p1 · · · [β/e
                                             [β/e

For example, let t be (ax1 x2 , x3 bx2 , x1 x2 x3 ) and α1 = aa, α2 = ab, α3 = ba. Then,
                                                                     
                                              aaaab babab aaabba
                                  Mt =                                   .
                                               abbba abbba bbbaab

    We use the following properties of characteristic data.

Lemma A.14. Let t and t1 be solvable tuple patterns. If M t |= t1 , then L(t) ⊆ L(t1 ).
Proof. This follows by induction on #t1 . If t1 ̸⇝, then t1 must be mutually distinct variables. Thus,
L(t1 ) = Σ∗ × · · · × Σ∗ ⊇ L(t). Suppose M t , Θ |= t1 and t1 ⇝ t′1 . We perform case analysis on the
rule used in the reduction t1 ⇝ t′1 .
    • Case PR-Prefix: We may assume without loss of generality that t1 = (q2 q1′ , q2 , . . . , qn ) and
      t′1 = (q1′ , q2 , . . . , qn ), with q2 ̸= ϵ. By the assumption M t , Θ |= t1 , M t [∗][1] must be of the form
                                                                                                            ′
      M t [∗][2] · se. By the definition of M t , t must be of the form (p2 p′1 , p2 , . . . , pn ), and M t , Θ |= t′1
           ′         ′                              ′
      for t = (p1 , p2 , . . . , pn ). Since #t1 < #t1 (by Lemma A.7), by the induction hypothesis, we
      have L(t′ ) ⊆ L(t′1 ). Thus, we have L(t) ⊆ L(t1 ).
    • Cases PR-CPrefix, PR-Suffix, and PR-CSuffix: Similar to the above case.

    • Case PR-Epsilon: We may assume without loss of generality that t1 = (ϵ, q2 , . . . , qn ) and
      t′1 = (q2 , . . . , qn ). By the assumption M t , Θ |= t1 , M t [∗][1] = e    ϵ. Therefore, t must be of the
                                          ′
      form (ϵ, p2 , . . . , pn ), with M t , Θ |= t′1 for t′ = (p2 , . . . , pn ). By the induction hypothesis, we
      have L(t′ ) ⊆ L(t′1 ). Thus, we have L(t) ⊆ L(t1 ) as required.

                                                                            
                                                              x1 · · · xk
Lemma A.15. Let t be a solvable tuple pattern, and Θ be  α1 · · · αk , where αi , βi are the
                                                              β1 · · · βk
                                       ′     t        ′
codewords for xi as defined above. If Θ t = M , then Θ (xi ) = Θ(xi ) for every xi ∈ Vars(t).
 12 The characteristic data M t depends on the choice of a, b ∈ Σ and binary prefix coding, but the choice does not

matter for the discussion below.



                                                          36
Proof. Since t is solvable, t ⇝∗ (x1 , . . . , xk ). We prove the required property by induction on
the length of the reduction sequence t ⇝∗ (x1 , . . . , xk ). If t = (x1 , . . . , xk ), the result follows
immediately, since M t = Θ t. Otherwise, we have t ⇝ t′ ⇝∗ (x1 , . . . , xk ). We perform the case
analysis on the rule used for deriving t ⇝ t′ . Since the other cases are simpler or simpler, we discuss
only the case for PR-Prefix, where we may assume t = (p2 p′1 , p2 , . . . , pn ) and t′ = (p′1 , p2 , . . . , pn ).
                                                      ′
By the assumption Θ′ t = M t , we have Θ′ t′ = M t . By the induction hypothesis, Θ′ (xi ) = Θ(xi )
for every xi ∈ Vars(t′ ) = Vars(t), as required.
Proof of Theorem 3.5. Let t = (p1 , . . . , pn ) be a solvable tuple pattern such that |p1 · · · pn | = m.
We show M = M t satisfies the required properties. By the definition of M t , size(M t ) = O((m +
n) log n). Suppose M ⊆ M ′ ⊆ L(t). We can assume that the first two rows of M ′ (as a matrix)
coincide with M . By M ′ |=s t and Theorem 3.2, we have (e               x]) −→∗ (t, Θ) for some Θ. For
                                                                x, [M t /e
(ii), it remains to show (t, Θ) −→.
                                 ̸  By Theorem 2.1, we have Θt = M ′ . By Lemma A.15, Θ must
be:                                                         
                                               x1 · · · x k
                                           α1 · · · α k 
                                           β1 · · · β k  .
                                                            

                                              ··· ··· ···
Because there exist no i and j such that αi is a prefix or suffix of αj , the rules R-Prefix and
R-Suffix are inapplicable. Since a and b are swapped between αi ’s and βi ’s, the rules R-CPrefix
and R-CSuffix are also inapplicable. Thus, we have (t, Θ) −→  ̸  as required. To show (iii), suppose
 x, [M ′ /e
(e        x]) −→∗ (t′ , Θ′ ) −→.
                              ̸  By Theorem 2.1, t′ |= M ′ . By Lemma A.14, we have L(t) ⊆ L(t′ ).
By Theorem 3.4, we have L(t) = L(t′ ) as required. Obviously, the size of the characteristic data
M t is O((m + n) log n), and it can be computed also in time O((m + n) log n).

A.1.8     Proofs for Section 3.3
Lemma A.16. Suppose M ′ ⊆ M and (e             x]) −→∗ (t, Θ). Then there exist t′ and Θ′ such that
                                         x, [M/e
      ′       ∗  ′   ′       ′
(e      x]) −→ (t , Θ ) and t = [e
 x, [M /e                        ϵ/e
                                   y ]t for some variables ye.
Proof. This follows by induction on the length n of the reduction sequence (e          x, M ) −→∗ (t, Θ). If
n = 0, then (e          x]) = (t, Θ) −→.
                  x, [M/e              ̸     Thus, the required result holds for the empty sequence of
variables ye.
      If n > 0, then we have (e   x, [M/e                  y ]) −→n−1 (t, Θ). By Lemma A.1, we have
                                         x]) −→ (t1 , [M1 /e
(e
 y , [M1 /ey ]) −→n−1 (t2 , Θ) with t = [t2 /e
                                             y ]t1 .
      We perform case analysis on the rule used for deriving (e  x, M ) −→ (t1 , Θ1 ). Since the other cases
are similar or easier, we discuss only the cases for R-Epsilon and R-Prefix.
    • Case R-Epsilon: In this case, we have:

                                         M [∗][i] = e
                                                    ϵ
                                         (e
                                          y ) = (x1 , . . . , xi−1 , xi+1 , . . . , xk )
                                         t1 = (x1 , . . . , xi−1 , ϵ, xi+1 , . . . , xk )
                                         M1 = M ↑i .

      Since M ′ ⊆ M , we have M ′ [∗][i] = e            ϵ. Thus, we can apply the same rule to obtain:
       x, [M ′ /e
      (e        x]) −→ (t1 , [M ′ ↑i /ey ]). Since M ′ ↑i ⊆ M ↑i = M1 , we can apply induction hypothesis
      to obtain t′2 such that (e y , [M ′ ↑i /ey ]) −→∗ (t′2 , Θ′ ) and t′2 = [e   ϵ/e
                                                                                     z ]t2 . Thus, the required result
                  ′    ′
      holds for t = [t2 /e
                         y ]t1 = [[e ϵ/e
                                       z ]t2 /e
                                              y ]t1 = [e
                                                       ϵ/ez ][t2 /e
                                                                  y ]t1 = [e
                                                                           ϵ/e
                                                                             z ]t.
    • Case R-Prefix: In this case, We have:

                                       M [∗][i] ̸= e
                                                   ϵ
                                       M [∗][j] = M [∗][i] · se
                                        y ) = (x1 , . . . , xj−1 , x′j , xj+1 , . . . , xk )
                                       (e
                                       t1 = (x1 , . . . , xj−1 , xi x′j , xj+1 , . . . , xk )
                                       M1 = M {j 7→ se}.


                                                            37
      For simplicity, we assume j = 2 and i = 1 below. If M ′ [∗][1] ̸= e                   ϵ, then we can apply the same
      rule to (e    x, [M ′ /ex]) and obtain the required result. If M ′ [∗][1] = e             ϵ, then we have M ′ ⊆ M1 .
                                                                         ′
      Thus, by the induction hypothesis, we have (e                 x, [M /ex]) −→ (t , Θ ) with t′ = [e
                                                                                    ∗     ′     ′
                                                                                                               ϵ/ez ]t2 for some
       ′            ′       ′       ′              ′ ′           ′         ′
      t . Let t = (p1 , . . . , pk ). Since Θ t = M and M [∗][1] = e                  ϵ, for every variable y occurring
      in p′1 , Θ′ (y) = e     ϵ. Thus, by applying R-Epsilon for such variables, we obtain t′′ such that
      (t , Θ ) −→ (t , Θ′′ ), t′′ = (ϵ, p′′2 , . . . , p′′k ), and t′′ = [e
         ′    ′         ∗   ′′
                                                                              ϵ/eu]t′ = [e   ϵ/ev ]t2 for ve = ue, ze. Let t2 =
      (p1 , . . . , pk ). Then t = (p1 , p1 p2 , p3 , . . . , pk ). Since ϵ = [eϵ/ev ]p1 , we have t′′ = [e   ϵ/ev ]t2 = [eϵ/ev ]t,
      as required.


    For data M such that dim(M ) = n, we define CSTPs(M ) as normalize(C0 , . . . , Cn ) where:

                 Ci = {t | (e     x] −→∗ (t, Θ) and |Vars(t)| = i}
                            x, [M/e
                 normalize(C0 , . . . , Cn ) = (C0′ , . . . , Cn′ )
              Ci′ = {t ∈ Ci | there exists no t′ ∈ Cj such that j < i and t′ = [e
                                                                                ϵ/e
                                                                                  y ]t.}
                                        
                          a ab abab
For example, for M =                       , CSTPs(M ) is:
                         bb     b     bb

                         (∅, ∅, {(x, y, yy)}, {(x, y, z), (x, y, xz), (x, y, yz), (x, y, zy)}).

(Note that we also have ((x, y, z), [M/(x, y, z)]) −→∗ ((x, y, yyz), Θ), but (x, y, yyz) is subsumed by
(x, y, yy), as [ϵ/z](x, y, yyz) = (x, y, yy).)
    We claim:
Lemma
   V      A.17. Suppose dim(M ) = n. If CSTPs(M ) = (C0 , . . . , Cn ), then L(CTPinf(M )) =
L( t∈C0 ∪···∪Cn t).
                                      V
Proof. To show L(CTPinf(M )) ⊇ L( t∈C0 ∪···∪Cn t), suppose t is a conjunct of CTPinf(M ). Since
t contains at most n variables, by the definition  of CSTPs(M ), there exists t′ ∈ Cj such that
 ′                                ′
                                           V
t V= [e  y ]t. Thus, L(t) ⊇ L(t ) ⊇ L( t∈C0 ∪···∪Cn t). Therefore, we have L(CTPinf(M )) ⊇
       ϵ/e
L( t∈C0 ∪···∪Cn t), as required.
    For the converse, suppose t ∈ Ci . Then, we have (e
                                                      x, [M/ex]) −→∗ (t, Θ) for some Θ. Let t′ be a
                                  ∗   ′  ′             ′
tuple pattern such that (t, Θ) −→ (t , Θ ) −→.
                                            ̸   Then, t is a conjunct of CTPinf(MV ), and therefore,
we have L(CTPinf(M ) ⊆ L(t′ ) ⊆ L(t). Thus, we have L(CTPinf(M )) ⊆ L( t∈C0 ∪···∪Cn t), as
required.
   We define the order (C0 , . . . , Cn ) < (C0′ , . . . , Cn′ ) by:        (C0 , . . . , Cn ) < (C0′ , . . . , Cn′ ) iff ∃i.(Ci ⊊
Ci ∧ ∀j < i.Cj = Cj′ ). Note that < is well-founded.
 ′


Lemma A.18. Suppose M0 , M1 , M2 , . . . is an infinite, strictly decreasing sequence of non-empty
data, i.e., ∅ ⊊ M0 ⊊ M1 ⊊ M2 ⊊ · · ·. Then, there exists j such that for all i ≥ j, L(CTPinf(Mi )) =
L(CTPinf(Mj )).
Proof. By Lemma A.16, we have:

                               CSTPs(M0 ) ≥ CSTPs(M1 ) ≥ CSTPs(M2 ) ≥ · · ·

Since < is well-founded, there exists j such that for all i ≥ j, CSTPs(Mi ) = CTPinf(Mj ). By
Lemma A.17, we have L(CTPinf(Mi )) = L(CTPinf(Mj )) for all i ≥ j.
Proof of Theorem 3.6. Suppose t is an STP, and L(t) = {e     si | i ∈ ω} with Mi = {e  sj | 0 ≤ j ≤ i}.
By Theorem 3.5, there exists M such that TPinf(M ′ ) always returns an STP equivalent to t
for any M ′ ⊇ M , and by the soundness of TPinf (Theorem 2.1), we have M ⊆ L(t). Since
L(t) = {esi | i ∈ ω}, there exists j such that M ⊆ Mj . Therefore, for every k ≥ j, TPinf(Mk )
always returns an STP equivalent to t.
    To show the case for CSTPs, suppose γ is a CSTP and L(γ) = {e      si | i ∈ ω} with Mi = {esj | 0 ≤
j ≤ i}. By Lemma A.18, there exist γ ′ and j such thatSfor all i ≥ j, L(CTPinf(Mi )) = L(γ ′ ). By
the soundness of TPinf (Theorem 2.1), we have L(γ) = i∈ω Mi ⊆ L(γ ′ ). By Theorem 3.3, we also
have L(γ) ⊇ L(γ ′ ). Therefore, we have L(γ) = L(γ ′ ), as required.


                                                               38
Proof of Theorem 3.7. We first show the termination of the procedure by contradiction. Suppose
the procedure does not terminate. Then, there exist infinite sequences se0 , se1 , se2 , . . . and γ0 , γ1 , γ2 , . . .
such that:

                                            ϵ) ∧ (ϵ, e
                                   γ0 = (a, e        ϵ)        Mj = {e
                                                                     si | i < j}.
                                   CTPinf(Mj ) = γj for j ≥ 1
                                                   sj ) for j ≥ 0.
                                   gF (γj ) = Some(e

These γj , sej , and Mj are the values of γ, se, and M at the j-th iteration of the loop in the
procedure. By the last condition and the assumption on gF , we have sej ∈ F (L(γj )) \ L(γj ). By
the soundness of CTPinf (Theorem 2.1), we have Mj ⊆ L(γj ). Therefore, sej ̸∈ Mj , and hence,
M0 = ∅ ⊊ M1 ⊊ M2 ⊊ M3 ⊊ · · · is a strictly increasing sequence. By Lemma A.18, there exist k
and γ such that L(γj ) = L(γ) for all j ≥ k. This however, contradicts sej ∈ F (L(γj )) \ L(γj ) and
sej ∈ Mj+1 ⊆ L(γj+1 ).
    Next, we show that the procedure returns the least CSTP γ such that L(γ) ⊇ F(L(γ)). Suppose
L(γ ′ ) ⊇ F(L(γ ′ )) for a CSTP γ ′ . Let γj , sej , and Mj be the values of γ, se, and M at the j-th
iteration of the loop in the procedure, as given above. It suffices to show L(γj ) ⊆ L(γ ′ ) by induction
on j. The case j = 0 is obvious, as L(γj ) = ∅. For the induction step, suppose L(γj ) ⊆ L(γ ′ ) and
gF (γj ) returns Some(e sj ). By the monotonicity of F, we have

                                         F(L(γj )) ⊆ F(L(γ ′ )) ⊆ L(γ ′ ).

Thus, sej ∈ F(L(γj )) \ L(γj ) ⊆ L(γ ′ ). Therefore, we have

                                 Mj+1 = Mj ∪ {e                sj } ⊆ L(γ ′ ).
                                              sj } ⊆ L(γj ) ∪ {e

By Theorem 3.3, we have γj+1 = CTPinf(Mj+1 ) ⊆ L(γ ′ ), as required.
Proof of Theorem 3.8. Let enumerate be the procedure defined as below, and suppose se0 ∈ F(∅).
Then enumerate({e  s0 }) outputs a superset of all the minimal t’s such that L(t) ⊇ F(L(t)). We can
then filter out non-minimal STPs by using the algorithm of Theorem 3.9 (3).

    Function enumerate(M ):
      U := {t | (ex, [M/ex]) −→∗ (t, Θ) −→};
                                           ̸
      while U ̸= ∅ do
          t := pick(U ); U := U \ {t};
          if gF (t) = Some(e s) then
              U := U \ {t′ | se ∈ L(t′ )};
              enumerate (M ∪ {e   s});
          else
              output(t);
      end

Note that U in the above algorithm is a local variable, prepared for each recursive call.
We first show the termination of the algorithm. Suppose enumerate({e           s0 }) does not terminate.
Since {t | (e
            x, [M/ex]) −→∗ (t, Θ) −→}̸  is a finite set, there must be an infinite chain of recursive calls
enumerate(M0 ), enumerate(M1 ), enumerate(M2 ), . . . where M0 = {e      s0 } and Mi = Mi−1 ∪ {e    si } for
i > 0. Let Ui be the value of U initialized at the beginning of the call enumerate(Mi ), and ti be the
value of t when enumerate(Mi+1 ) is called. Thus, Mi ⊆ L(ti ) and sei+1 ̸∈ L(ti ). By Theorem 3.6,
there exists k and t′ such that L(ti ) = L(t′ ) for all i ≥ k. But this contradicts the conditions
sei ∈ Mi ⊆ L(ti ) but sei ̸∈ L(ti−1 ).
     Next, suppose that t is a minimal STP such that L(t) ⊇ F (L(t)). It suffices to show that for
any M such that M ⊆ L(t), enumerate(M ) outputs (an STP equivalent to) t, or makes a recursive
call enumerate(M ′ ) for M ′ such that M ⊊ M ′ ⊆ L(t) (as we have already shown the termination
of the algorithm).
     By the completeness (Theorem 3.2) and minimality (Theorem 3.4), the value of U initialized
at the beginning of the call of enumerate(M ) must contain t′ such that M ⊆ L(t′ ) ⊆ L(t). We
perform case analysis on whether t′ is picked up in the while-loop.

                                                          39
   • Suppose t′ is eventually picked up in the while-loop. Then if L(t) = L(t′ ), then gF (t′ )
     returns None and t′ is output. If L(t′ ) ⊊ L(t), then gF (t′ ) returns Some(e   s) such that
     se ∈ F(L(t′ )) ⊆ F(L(t)) ⊆ L(t). Thus, enumerate(M ′ ) is called for M ′ = M ∪ {e
                                                                                     s} ⊆ L(t), as
     required.
   • Suppose t′ is never picked up in the while-loop. Then t′ must have been removed by the
     assignment U := U \ {t′ | se ∈ L(t′ )}. But then it must be the case that se ∈ L(t′ ). Therefore,
     enumerate(M ′ ) is called for M ′ = M ∪ {e s} ⊆ L(t′ ) ⊆ L(t), as required.



A.1.9    Proofs for Section 3.4
Proof of Theorem 3.9. (1): By Lemma A.6, if t ⇝ t′ , then t is solvable if and only if t′ is solvable.
By Lemma A.7, the length of a reduction sequence t ⇝ t1 ⇝ · · · ⇝ tn is bounded by #t. Thus, to
check whether t is solvable, it suffices to repeatedly reduce t (in a non-deterministic manner) until
no reduction is applicable, and check whether the resulting tuple pattern is of the form (x1 , . . . , xk ).
As each step can be performed in polynomial time, the algorithm runs in polynomial time.
   (3): Based on Lemma A.4, we can use the algorithm in Algorithm 1.

   Function decide inc(t1 , t2 ):
     if t2 is of the form (x1 , . . . , xn ) where x1 , . . . , xn are pairwise distinct then
          return True
     pick t′2 such that t2 ⇝ t′2 ;
     if t′1 := ⟨t2 ⇝ t′2 ⟩(t1 ) is well defined then
          return decide inc(t′1 , t′2 )
     else
          return False
                                                                              ?
                        Algorithm 1: Algorithm to decide L(t1 ) ⊆ L(t2 ).

Here, we assume |t1 | = |t2 |; otherwise, we can immediately conclude that L(t1 ) ̸⊆ L(t2 ). The
algorithm repeatedly reduces t2 and checks whether the reduction of t2 can be “simulated by” the
corresponding reduction of t1 . If t2 is of the form (x1 , . . . , xn ), we can immediately conclude that
t1 ⊆ t2 holds, as L(t2 ) = Σ∗ × · · · × Σ∗ . Otherwise, we can always pick t′2 such that t2 ⇝ t′2 by the
assumption that t2 is solvable. By Lemma A.4, if ⟨t2 ⇝ t′2 ⟩(t1 ) is well defined, then it suffices to
check whether L(t′1 ) ⊆ L(t′2 ); otherwise, we can immediately conclude that L(t1 ) ̸⊆ L(t2 ) (on the
last line).
    Each operation can be clearly performed in time polynomial in the size of the initial inputs
t1 and t2 . Since #t2 > #t′2 ≥ 0, the depth of the recursive call is bounded by #t2 . Thus, the
algorithm runs in polynomial time. (As this proof shows, t1 need not be solvable.)
    (2): This is a special case of (3), where t2 = t and t1 is the constant pattern (s1 , . . . , sn ) (whose
language is a singleton set {(s1 , . . . , sn )}).
    (4): This is an immediate consequence of (3), as L(t1 ) = L(t2 ) ⇔ L(t1 ) ⊆ L(t2 ) ∧ L(t2 ) ⊆
L(t1 ).
    Before proving Theorem 3.10, we define the semantics of formulas. A valuation is a map from
the set of variables to Σ∗ . For a valuation ρ and w ∈ (Σ ∪ V)∗ such that Vars(w) ⊆ dom(ρ), we
define ρw by:
                        ρϵ = ϵ     ρ(aw) = a · (ρw)    ρ(xw) = ρ(x) · (ρw).
For a valuation ρ and a quantifier-free STP-formula φ, the relation ρ |= φ is defined by induction
on φ, as follows.

                           ρ |= w1 = w2 if ρw1 = ρw2
                           ρ |= w1 ̸= w2 if ρw1 ̸= ρw2
                           ρ |= (w1 , . . . , wn ) ∈ L(t) if (ρw1 , . . . , ρwn ) ∈ L(t)
                           ρ |= (w1 , . . . , wn ) ̸∈ L(t) if (ρw1 , . . . , ρwn ) ̸∈ L(t)
                           ρ |= φ1 ∧ φ2 if ρ |= φ1 and ρ |= φ2


                                                         40
                              ρ |= φ1 ∨ φ2 if ρ |= φ1 or ρ |= φ2 .
We say a formula φ is satisfiable if ρ |= φ for some ρ. Without subformulas w    e ∈ L(t) and w
                                                                                              e ̸∈ L(t),
it is known that the satisfiability of quantifier-free formulas is decidable [46, 56, 35].
Proof of Theorem 3.10. Since the satisfiability of word equations is decidable and in PSPACE [46,
56, 35], it suffices to show that atomic formulas of the form w1 ̸= w2 , (w1 , . . . , wk ) ∈ L(t), or
(w1 , . . . , wk ) ̸∈ L(t) can be encoded into formulas using only word equations of polynomial size.
We can assume, without loss of generality, that the alphabet Σ is finite: note that if φ is satisfiable
for an infinite alphabet, then φ is also satisfiable for Σφ ∪ {a, b} where Σφ is the set of letters
occurring in φ and a, b are distinct letters not occurring in φ, and vice versa. First,               W we encode the
relation w1 ̸⪯ w2 , which  W   means  “w 1 is not a prefix  of w2 .” It can  be  expressed        by (  a,b∈Σ,a̸=b w1 =
xay ∧ w2 = xbz) ∨ a∈Σ w1 = w2 ax, where x, y, z are fresh variables. (This encoding of ̸⪯ is
standard; see, e.g. [17, 35].) We can then express w1 ̸= w2 as w1 ̸⪯ w2 ∨ w2 ̸⪯ w1 .
    The encoding of (w1 , . . . , wk ) ∈ L(t) is straightforward. Suppose t = (p1 , . . . , pℓ ). If k ̸= ℓ, then
(w1 , . . . , wk ) ∈ L(t) can be replaced with false (which can be expressed as a = ϵ). If k = ℓ, then
(w1 , . . . , wk ) ∈ L(t) is expressed as w1 = p′1 ∧ · · · ∧ wk = p′k , where (p′1 , . . . , p′k ) are obtained from t
by α-renaming, so that the variables in p′1 , . . . , p′k are fresh.
    Now we consider (w1 , . . . , wk ) ̸∈ L(t), where t = (p1 , . . . , pℓ ). If k ̸= ℓ, then it can be replaced
with true (which can be expressed as ϵ = ϵ). Thus, we assume k = ℓ. Since t is solvable, there exists
a reduction sequence t ⇝∗ (x1 , . . . , xm ). We encode the formula by induction on the length n of the
reduction sequence. If n = 0, then L(t) = L(x1 , . . . , xk ) = Σ∗ × · · · × Σ∗ . Thus, (w1 , . . . , wk ) ̸∈ L(t)
can be replaced with false. If n > 0, then t ⇝ t′ ⇝∗ (x1 , . . . , xm ). We perform case analysis on
the rule used for deriving t ⇝ t′ . Since the other cases are similar, we discuss only the cases for
PR-Prefix and PR-Epsilon.
    • Case PR-Prefix: In this case, there exist i, j such that t′ = (p′1 , . . . , p′k ) with pj = pi p′j
      and p′ℓ = pℓ for all ℓ ̸= j. Thus, (w1 , . . . , wk ) ̸∈ L(t) can be replaced with wi ̸⪯ wj ∨ (wj =
      wi x ∧ (w1′ , . . . , wk′ ) ̸∈ L(t′ )), where x is a fresh variable, wj′ = x, and wℓ′ = wℓ for all ℓ ̸= j.
      By the induction hypothesis, (w1′ , . . . , wk′ ) ̸∈ L(t′ ) can also be encoded into word equations.
    • Case PR-Epsilon: In this case, there exists j such that pj = ϵ and t′ =
      (p1 , . . . , pj−1 , pj+1 , . . . , pk ). Thus, (w1 , . . . , wk ) ̸∈ L(t) can be replaced with wj ̸= ϵ ∨
      (w1 , . . . , wj−1 , wj+1 , . . . , wk ) ̸∈ L(t′ ). By the induction hypothesis, (w1′ , . . . , wk′ ) ̸∈ L(t′ ) can
      also be encoded into word equations.
The size of the resulting formula is polynomial in the size of the original formula, as the length of
the reduction sequence t ⇝∗ (x1 , . . . , xm ) is linear in #t and the increase of the formula size in each
step of the encoding above is polynomial in the size of w     e ̸∈ L(t).
Remark A.2. The encoding of w    e ̸∈ L(t) above for the inductive case is actually based on a special
case of Lemma A.4 where t0 is a constant pattern se. By Lemma A.4, se ̸∈ L(t) if and only if
⟨t ⇝ t′ ⟩(e
          s) is undefined or L(⟨t ⇝ t′ ⟩(e s)) ̸⊆ L(t′ ). The (un)definedness of ⟨t ⇝ t′ ⟩(e
                                                                                           s) can be
expressed in terms of the prefix/suffix relations, which can further be expressed by word equations,
as discussed above.

A.2      Additional Definitions and Proofs for Section 4
A.2.1     The Extension in Section 4.1
First, we extend ∼ (used in Lemma A.6) to the least equivalence relation closed under not only
the permutations and but also the rule (p1 , . . . , pk ) ∼ (p1 , . . . , pi−1 , pR
                                                                                  i , pi+1 , . . . , pk ), and slightly
relax the requirement for solvability: a tuple pattern t is solvable if t ⇝∗ ∼ (x1 , . . . , xn ) for some
mutually distinct variables x1 , . . . , xn . Thus, (xR , y) is also solvable, as (xR , y) ∼ (x, y). Without
the reverse pattern constructor, the definition of solvability is the same.
    All the main properties are preserved by the extension of patterns with the reverse constructor.
This can be intuitively understood by noting that the rules R-RPrefix and R-RSuffix can be
emulated by R-Prefix and R-Suffix, if we augment the data M by adding, for each column
M [∗][i] of M , a new column consisting of the reverse of elements of M [∗][i]. For example,
                                          
                 ((x1 , x2 ), [ ab bac /(x1 , x2 )])


                                                          41
                                 ′
                   −→ ((x1 , xR                                   /(x1 , x′2 )])
                                                              
                              1 x2 ), [ ab                c                                     (R-RPrefix)
can be emulated by:
                                                                      
         ((x1 , x2 , y1 , y2 ), [ ab     bac         ba       cab
                                                               /(x1 , x2 , y1 , y2 )])
          −→ ((x1 , y1 x′2 , y1 , y2 ), [ ab c             ba cab /(x1 , x′2 , y1 , y2 )])
                                                                  
                                                                                                             (R-Prefix)
          −→ ((x1 , y1 x′2 , y1 , y2′ x1 ), [ ab          c ba c /(x1 , x′2 , y1 , y2′ )])
                                                                  
                                                                                                              (R-Suffix)
It should be obvious that the extended pattern (p1 , . . . , pn ) (consisting of variables z1 , . . . , zm ) is
inferable if and only if (θ1 p1 , . . . , θ1 pn , θ2 pR                 R
                                                        1 , . . . , θ2 pn ) is inferable from the augmented data, where
θ1 = [x1 /z1 , . . . , xm /zm , y1 /z1R , . . . , ym /zm
                                                       R
                                                         ] and θ2 = [y1 /z1 , . . . , ym /zm , x1 /z1R , . . . , xm /zm
                                                                                                                      R
                                                                                                                        ].
    A little more formally, we can confirm that the main properties listed in Table 3, by checking
that all the lemmas in the table remain to hold (modulo a minor adjustment due to the extension of
solvability). The lemmas required for soundness and completeness (Theorem 2.1, Theorem 3.1 and
Theorem 3.2) trivially hold. More care is necessary for minimality (Theorem 3.4). For Lemma A.4,
we extend the definition of ⟨t1 ⇝ t′1 ⟩(t0 ) (Definition A.1) by the following cases:
    • Case PR-RPrefix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = pR       ′
                                                                                                         i · pj and
                                        ′                                                                R ′
      pi ̸= ϵ for some i, j and pk = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and qj = qi qj , then
      ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where for k ̸= j. Otherwise, ⟨t1 ⇝ t2 ⟩(t0 ) is undefined.
    • Case PR-RSuffix: In this case, t1 = (p1 , . . . , pn ) and t2 = (p′1 , . . . , p′n ) with pj = p′j · pR
                                                                                                            i and
      pi ̸= ϵ for some i, j and p′k = pk for k ̸= j. If t0 is of the form (q1 , . . . , qn ) and qj = qj′ · qiR ,
      then ⟨t1 ⇝ t2 ⟩(t0 ) := (q1′ , . . . , qn′ ) where for k ̸= j. Otherwise, ⟨t1 ⇝ t2 ⟩(t0 ) is undefined.
Then Lemma A.4 holds as required.
   Lemma A.6 (weak confluence of ⇝ up to ∼) also remains to hold. We discuss only one new
case; the other cases are similar.
    • Case t = (p2 p′1 , p2 , p3 , . . . , pn ) ⇝ (p′1 , p2 , p3 , . . . , pn ) = t1 and t = (pR  ′′
                                                                                               3 p1 , p2 , p3 , . . . , pn ) ⇝
        ′′
      (p1 , p2 , p3 , . . . , pn ) = t2 (i.e., the two reductions use PR-Prefix and PR-RPrefix respec-
      tively, and p1 is principal in both reductions).
      By p2 p′1 = pR          ′′          R
                         3 p1 , p2 and p3 are in the prefix relation. Let us consider the case where p3 is a
                                                                                                                         R

      prefix of p2 ; the other case is similar. In that case, we have:
                           ′
                  p2 = pR
                        3 p2           p′′1 = p′2 p′1
                  t1 = (p′1 , pR  ′                         ′    ′
                               3 p2 , p3 , . . . , pn ) ⇝ (p1 , p2 , p3 , . . . , pn )

                  t2 = (p′2 p′1 , pR  ′                         ′ ′     ′                      ∗  ′    ′
                                   3 p2 , p3 , . . . , pn ) ⇝ (p2 p1 , p2 , p3 , . . . , pn ) ⇝ (p1 , p2 , p3 , . . . , pn ).

    For the existence of characteristic data (Theorem 3.5), it suffices to strengthen the requirement
for the codewords α1 , . . . , αn , by further requiring that for all i, j ∈ {1, . . . , n}, αi is neither a prefix
nor a suffix of αjR . Note that we can still choose such codewords such that |αi | = O(log n). (For
example, for the codewords α1′ , . . . , αn′ of the same length that satisfy the original conditions, let
αi = aαi b.) Then, we have a slightly weakened version of Lemma A.15, where “Θ′ (xi ) = Θ(xi ) for
every xi ∈ Vars(t)” is replaced with “Θ′ (xi ) is Θ(xi ) or (Θ(xi ))R for every xi ∈ Vars(t)”, which is
sufficient for proving Theorem 3.5.
    The lemmas for learnability in Table 3 remain to hold, and therefore, Theorems 3.6 and 3.7 also
remain to hold.
    For Theorem 3.10 (the decidability of quantifier-free STP formulas), the set of word expressions
are extended to w ∈ (Σ∪V ∪V R )∗ , and the definition of ρw is extended in an obvious manner. Then,
Theorem 3.10 remains to hold, thanks to the decidability of word equations with involution [19, 18].

A.2.2     The Extensions with Multisets and Sets
We now discuss the extensions sketched in Section 4.2.
    We first provide more precise definitions of multiset patterns. The sets of multiset tuple patterns
(MTPs) and conjunctive multiset tuple patterns (CMTPs), ranged over by t and γ respectively, are
defined by:
                          t ::= (p1 , . . . , pk )            p ∈ (Σ ∪ V)∗         γ ::= t1 ∧ · · · ∧ tm .


                                                                        42
Patterns are identified up to permutations; e.g., xyz = yxz (thus, a pattern p may actually be
viewed as a multiset consisting of elements of Σ and V). A multiset tuple pattern is solvable if
t ⇝∗ (x1 , . . . , xk ) for some mutually distinct variables x1 , . . . , xk . A conjunctive multiset tuple
pattern γ = t1 ∧ · · · ∧ tk is solvable if ti is solvable for every i ∈ {1, . . . , k}. Solvable multiset
tuple patterns and conjunctive multiset tuple patterns are abbreviated as SMTP and CSMTP
respectively.
   For a map ρ from V to the set of multisets over Σ, and a pattern p such that Vars(p) ⊆ dom(ρ),
we define ρp by:
                            ρϵ = ∅  ρ(ap) = {a} ⊎ (ρp)      ρ(xp) = ρ(x) ⊎ (ρp),
where ⊎ denotes the multiset union.
   For an MTP t and a CMTP γ, L(t) and L(γ) are defined by:
                           L(p1 , . . . , pn ) = {(ρp1 , . . . , ρpn ) | dom(ρ) ⊇ V(p1 · · · pn )}
                           L(t1 ∧ · · · ∧ tm ) = L(t1 ) ∩ · · · ∩ L(tm ).
   Among the properties listed in Table 3, the minimality property (Theorem 3.4) fails. For
example, consider the data: M = (abcd, ab, ac, ccd). We can reduce (e                         x, [M/ex]) in the following two
ways:
                                                                                  ′                      
                                x y z                w                                  x     y z       w
   ((x, y, z, w),                                           ) −→ ((x′ y, y, z, w),                            )
                         abcd ab ac ccd                                                 cd ab ac ccd
                                      ′
                                                  y z w′
                                                                                                     ′
                                                                                                           y z ′ w′
                                                                                                                      
                                          x                                                           x
    −→ ((x′ y, y, z, x′ w′ ),                                     ) −→ ((x′ y, y, z ′ w′ , x′ w′ ),                     )
                                          cd ab ac             c                                     cd ab a         c
                                                   ′
                                                     x y ′ z ′ w′
                                                                         
    −→ ((x′ y ′ z ′ , y ′ z ′ , z ′ w′ , x′ w′ ),                          )
                                                     cd b a           c
                                                           ′′
                                                                  y ′ z ′ w′
                                                                                
                                                              x
    −→ ((x′′ w′ y ′ z ′ , y ′ z ′ , z ′ w′ , x′′ w′ w′ ),                          ) −→
                                                                                      ̸
                                                               d b a          c
                                                                                  ′                      
                                x y z                w                                  x     y z       w
   ((x, y, z, w),                                           ) −→ ((x′ z, y, z, w),                            ) −→
                                                                                                                 ̸
                         abcd ab ac ccd                                                 bd ab ac ccd


Thus, TPinf(M ) outputs (xyzw, yz, zw, xww) or (xz, y, z, w) non-deterministically, but the latter
is not minimal; in fact, L(xwyz, yz, zw, xww) ⊊ L(xz, y, z, w).
    The failure of the minimality is attributed to the failure of weak confluence of ⇝ (Lemma A.6).
In fact, the reductions (xyzw, yz, zw, xww) ⇝ (xw, yz, zw, xww) and (xyzw, yz, zw, xww) ⇝
(xy, yz, zw, xww) are not confluent, because (xy, yz, zw, xww) ̸⇝.
    Due to the failure of minimality, Theorem 3.5 (about characteristic data) and the first part
of Theorem 3.6 (about the learnability of SMTPs) fail. However, the following weaker version of
Theorem 3.5 (obtained by weakening the condition (iii)) holds.
Theorem A.19 (Characteristic Data (Weaker Version)). Let t = (p1 , . . . , pn ) be an STP such that
|p1 · · · pn | = m. Then, there exists M such that (i) size(M ) is polynomial in m + n, (ii) for any M ′
such that M ⊆ M ′ ⊆ L(t), there exists Θ such that (e     x, [M ′ /e
                                                                   x]) −→∗ (t, Θ) −↛ , and (iii) for any
   ′                      ′               ′        ∗    ′  ′
M such that M ⊆ M ⊆ L(t), (e                x]) −→ (t , Θ ) −→
                                     x, [M /e                   ̸     implies L(t) ⊆ L(t′ ). Furthermore,
given t, M can be constructed in polynomial time.
Proof Sketch. For an SMTP t, we construct the characteristic data M t as follows. Let t =
(p1 , . . . , pn ), with Vars(p1 · · · pn ) = {x1 , . . . , xℓ }. Let ρi (i ∈ {1, . . . , ℓ}) be the map such that
ρi (xi ) = a and ρi (xj ) = ϵ for every j ̸= i. Let M t be:
                                                                       
                                                 ρ1 p1 · · · ρ1 pn
                                               ··· ···            ··· .
                                                 ρℓ p1 · · · ρℓ pn
For example, the characteristic data for (xyzw, yz, zw, xww) above is
                                                        
                                           a ϵ ϵ a
                                         a a ϵ ϵ 
                                         a a a ϵ .
                                                        

                                           a ϵ a aa

                                                             43
   Then, M := M t satisfies the conditions required in Theorem A.19.
    The class of SMTPs is still learnable if TPinf is modified so that it outputs a minimal STP
ti such that (e        x]) −→∗ (ti , Θ) −→.
               x, [Mi /e                 ̸      To do so, it suffices for TPinf to first compute the set
  ′
U := {t | (e        x]) −→∗ (ti , Θ) −→},
            x, [Mi /e                 ̸     filter out non-minimal STPs by computing U := {t ∈ U ′ |
¬∃t′ ∈ U ′ .L(t′ ) ⊊ L(t)}, and output an element of U non-deterministically. Then Theorem 3.6
holds for the modified version of TPinf.
    As for Theorem 3.9, the decidability remains to hold, but the complexity of deciding whether a
given multiset tuple pattern t is solvable may not belong to P, due to the failure of weak confluence
of ⇝. The membership and inclusion problems can still be solved in polynomial time if we are
given a witness for the solvability of t (i.e., a reduction sequence t ⇝∗ (x1 , . . . , xk )).
    The other properties—soundness (Theorem 2.1), completeness (Theorems 3.2 and 3.3), learn-
ability of CSTPs (the second part of Theorem 3.6 and Theorems 3.7 and 3.8), and the decidability of
quantifier-free formulas (Theorem 3.10)—remain to hold. Indeed, we can confirm that the required
lemmas listed in Table 3 remain to hold. In the proof of Theorem 3.8, the first line of the procedure
enumerate:
                                  U := {t | (e
                                             x, [M/e x]) −→∗ (t, Θ) −→}
                                                                      ̸
should be replaced with:

           U ′ := {t | (e     x]) −→∗ (t, Θ) −→};
                        x, [M/e               ̸   U := {t ∈ U ′ | ¬∃t′ ∈ U ′ .L(t′ ) ⊊ L(t)},

to filter out non-minimal STPs.
    The decidability of (the satisfiability of) quantifier-free formulas relies for the multiset-case
relies on that of linear integer arithmetic, instead of word equations. First, let us fix the syntax of
quantifier-free SMTP formulas:13

Definition A.2. The set of (quantifier-free) SMTP formulas, ranged over by φ, is defined by:

                    φ ::= |w1 | = |w2 | | w1 ⊆ w2 | w
                                                    e ∈ L(t) | φ1 ∧ φ2 | φ1 ∨ φ2 | ¬φ.

Here, w ∈ (Σ ∪ V)∗ , where the empty sequence is interpreted as the empty multiset, and the
concatenation is interpreted as the multiset union. |w| denotes the size of the multiset (expressed
by) w.
    The semantics of quantifier-free SMTP formulas is defined as follows. Let ρ be a map from V to
the set of finite multisets over Σ. We define ρw (where we assume dom(ρ) ⊇ Vars(w)) and ρ |= φ
by:

     ρϵ = ∅      ρ(aw) = {a} ⊎ ρw            ρ(xw) = ρ(x) ⊎ ρw
     ρ |= |w1 | = |w2 | if |ρw1 | = |ρw2 |
     ρ |= w1 ⊆ w2 if ρw1 ⊆ ρw2
     ρ |= w
          e ∈ L(t) if ρw
                       e ∈ L(t)
     ρ |= w
          e ̸∈ L(t) if ρw
                        e ̸∈ L(t)
     ρ |= φ1 ∧ φ2 if ρ |= φ1 and ρ |= φ2
     ρ |= φ1 ∨ φ2 if ρ |= φ1 or ρ |= φ2 .                             ρ |= ¬φ if ρ |= φ does not hold.

We say that a quantifier-free SMTP formula φ is satisfiable if ρ |= φ for some ρ. The following is a
multiset version of Theorem 3.10.
Theorem A.20. Given a quantifier-free SMTP formula φ, one can effectively construct an equi-
satisfiable SMTP formula φ′ that contains no subformulas of the form w       e ∈ L(t), or w
                                                                                          e ̸∈ L(t).
Therefore, the satisfiability of quantifier-free SMTP formulas is decidable.

Proof. It suffices to show encodings of w   e ∈ L(t) and w       e ̸∈ L(t) (by considering the negation normal
form). Let w e = (w1 , . . . , wn ) and t = (p1 , . . . , pℓ ). If n ̸= ℓ, then w
                                                                                e ∈ L(t) and w e ̸∈ L(t) can be
replaced by false and true respectively. Suppose n = ℓ. Then, w              e ∈ L(t) can be replaced by w1 =
 13 We can further add primitive constraints accommodated by [55].




                                                      44
p′1 ∧· · · wn = p′n , where (p′1 , . . . , p′n ) is obtained by α-renaming of t and all the variables in (p′1 , . . . , p′n )
are fresh. w  e ̸∈ L(t) can be encoded by induction on the sequence t ⇝∗ (x1 , . . . , xk ), in the same
manner as the case for STPs. For example, if t = (p2 p′1 , p2 , . . .) ⇝ (p′1 , p2 , . . .) ⇝∗ (x1 , . . . , xk ), then
e ̸∈ L(t) can be replaced by: ¬(w2 ⊆ w1 ) ∨ (w1 = w2 x ∧ (x, w2 , . . . , wn ) ̸∈ (p′1 , p2 , . . .)).
w
     By the decidability of multiset constraints [55], we can conclude that the satisfiability of
quantifier-free SMTP formulas is decidable.
    Analogous results hold for the case of sets, where the conjunction is interpreted as the dis-
joint union. The decidability of quantifier-free SSTP formulas follows from the decidability of set
constraints (e.g., see [42]).

A.3      Additional Definitions and Proofs for Section 5
A.3.1      Additional Details on Section 5.1
As defined in Section 5.1, a CHC over words is of the form P1 (e                y1 ) ∧ · · · ∧ Pn (e
                                                                                                   yn ) ∧ φ ⇒ H, where
Pi is a predicate variable, φ is a quantifier-free STP-formula, and H is of the form P (e                    y ) or false.
(Here, false may be viewed as an STP formula a = ϵ.)
    An interpretation for predicate variables is a function that maps each k-ary predicate variable
to a subset of (Σ∗ )k . Let M be an interpretation for predicates, and ρ be a map from V to Σ∗ . We
write M, ρ |= P (y1 , . . . , yk ) if (ρy1 , . . . , ρyk ) ∈ M(P ) and M, ρ |= φ if ρ |= φ (recall Section A.1.9
for the definition of the latter). Let C be a CHC P1 (e          y1 ) ∧ · · · ∧ Pn (e
                                                                                    yn ) ∧ φ ⇒ H. We write M |= C
if M, ρ |= H holds for every ρ such that M, ρ |= φ and M, ρ |= Pi (e                 yi ) for each i ∈ {1, . . . , n}. Let
S be a system of CHCs {C1 , . . . , Cm }. We write M |= S, and call M a model of S if M |= Ci for
every Ci ∈ S. A system S of CHCs is satisfiable if there exists a model of S.
    A CSTP-interpretation for predicates is a map {P1 7→ γ1 , . . . , Pn 7→ γn } where γi ’s are CSTPs.
A CSTP-interpretation Γ = {P1 7→ γ1 , . . . , Pn 7→ γn } is a CSTP-model of S, written Γ |= S, if
{P1 7→ L(γ1 ), . . . , Pn 7→ L(γn )} |= S. By abuse of notation, we often just write {P1 7→ γ1 , . . . , Pn 7→
γn } for {P1 7→ L(γ1 ), . . . , Pn 7→ L(γn )}.
Lemma A.21. Given a CSTP-interpretation Γ and a system S of CHCs, it is decidable whether
Γ is a CSTP-model of S. Furthermore, there is an algorithm which, given Γ and a finite set SD of
definite clauses, outputs “None” if Γ |= SD , and otherwise outputs Some(P, se) such that there exists
a valuation ρ and a clause P1 (e  y1 ) ∧ · · · ∧ Pn (e
                                                     yn ) ∧ φ ⇒ P (e
                                                                   y ) in SD , with Γ, ρ |= φ and Γ, ρ |= Pi (e
                                                                                                              yi )
                   y ) = se ̸∈ Γ(P ).
for every i, but ρ(e
Proof. This follows immediately from Theorem 3.10. Note that Γ is a CSTP-model of a CHC
    y1 ) ∧ · · · ∧ Pn (e
P1 (e                  yn ) ∧ φ ⇒ H, if and only if Γ(P1 (ey1 )) ∧ · · · ∧ Γ(Pn (e
                                                                                 yn )) ∧ φ ∧ ¬Γ(H) is unsatisfiable,
where Γ(P (e     y )) denotes the formula ye ∈ Γ(P ). Thus, if Γ |= SD does not hold, then Γ(P1 (e           y1 )) ∧ · · · ∧
Γ(Pn (eyn )) ∧ φ ∧ ¬Γ(P (e     x)) is satisfiable for some definite clause P1 (e   y1 ) ∧ · · · ∧ Pn (e
                                                                                                      yn ) ∧ φ ⇒ P (e   y ).
We can construct a model ρ for the formula and return Some(P, ρ(e                 x)).
   To prove Theorem 5.1 for the case where CHCs have multiple predicates, we need to extend
Theorem 3.7. Let I be the set of interpretations for predicate variables.
Theorem A.22. Let SD be a finite set of definite clauses consisting of predicates P1 , . . . , Pn . Let
g be the algorithm of Lemma A.21. Then the procedure below eventually terminates and returns the
least CSTP-model of SD .

    M ← {P1 7→ ∅, . . . , Pn 7→ ∅}; Γ ← {P1 7→ (a, e
                                                   ϵ) ∧ (ϵ, e
                                                            ϵ), . . . , Pn 7→ (a, e
                                                                                  ϵ) ∧ (ϵ, e
                                                                                           ϵ)};
    while true do
     if g(Γ, SD ) = Some(P, se)
     then (M ← M{P 7→ M(P ) ∪ {e        s}}; Γ ← Γ{P 7→ CTPinf(M(P ))}
     else return Γ


Proof. We first prove the termination of the procedure. Suppose that the procedure does not
terminate. Let Mi , Γi , sei be the values of M, Γ, se at the i-th iteration of the loop. We have
a strictly increasing infinite sequence M0 ⊊ M1 ⊊ M2 ⊊ · · ·. For every Pi such that


                                                             45
M0 (Pi ), M1 (Pi ), M2 (Pi ), . . . strictly increases infinitely often, by Lemma A.18, there exists ki
such that L(CTPinf(Mj (Pi ))) = L(CTPinf(Mki (Pi ))) for all j ≥ ki . For every Pi such that
M0 (Pi ), M1 (Pi ), M2 (Pi ), . . . strictly increases only finitely often, let ki be the index such that
Mj (Pi )) = Mki (Pi ) for all j ≥ ki . Let k = max(k1 , . . . , kn ). Then, we have L(Γj ) = L(Γk ) for
all k ≥ j. But then that contradicts g(Γk , SD ) = Some(Pi , sek ) (which implies sek ̸∈ L(Γk (Pi ))) and
sek ∈ Mk+1 (Pi ) ⊆ L(Γk+1 (Pi )).
    By the assumption on g, when the algorithm terminates at the k-th step, Γk is a model of SD .
Suppose there exists another CSTP-model Γ′ of SD . Then it follows by induction on j that Γj ≤ Γ′
for every j ≤ k (by the same argument as in the proof of Theorem 3.7).
   We can now prove Theorem 5.1.

Proof of Theorem 5.1. Let S = SD ∪ SG , where SD and SG respectively consist of definite and
goal clauses. By Theorem A.22, we can compute the least CSTP-model Γ of SD . Then, S has a
CSTP-model if and only if Γ is also a CSTP-model of SG . (Note that “only if” direction holds
since for any goal clause C, M′ |= C and M ≤ M′ imply M |= C.) The latter is decidable by
Theorem A.21.

   Theorem 5.2 is an immediate corollary of the following lemma, which is obtained as a straight-
forward generalization of Theorem 3.8.
Lemma A.23. Let SD be a finite set of definite clauses consisting of predicates P1 , . . . , Pn . Then
there exists an algorithm that enumerates all the minimal STP-models of SD .
Proof. Let enumModel be the procedure defined as below, and let P1 , . . . , Pn be the predicate
variables occurring in SD . Let g be the algorithm of Lemma A.21. Then it suffices to call
enumModel({P1 7→ ∅, . . . , Pn 7→ ∅}) to obtain a superset of all the minimal STP-models of SD ,
and then filter out non-minimal models.

   Function enumModel(M):
      U := {{P1 7→ t1 , . . . , Pn 7→ tn } | ∀i.(M(Pi ) = ∅ ∧ ti = t∅ ) ∨ (e          x]) −→∗ (ti , Θ) −→;}
                                                                           x, [M(Pi )/e                 ̸
      while U ̸= ∅ do
         Γ := pick(U ); U := U \ {Γ};
         if g(Γ, SD ) = Some(P, se) then
             U := U \ {Γ′ ∈ U | se ∈ L(Γ′ (P ))};
             enumModel (M{P 7→ M(P ) ∪ {e         s}});
         else
             output(t);
      end


The correctness of the algorithm follows by the same argument as that of Theorem 3.8.
Example A.1. Let us apply the algorithm in the proof above to the Reva example (cf. Example 5.2
and Remark 5.1). The computation of enumModel({Reva 7→ t∅ }) proceeds as follows.

  1. U is first set to {{Reva 7→ t∅ }} and Γ0 := {Reva 7→ t∅ } is picked. Suppose g(Γ0 , SD ) returns
     Some(Reva, (ϵ, ab, ab)).
  2. Then enumModel({Reva 7→ {(ϵ, ab, ab)}}) is recursively called, and U is set to {{Reva 7→
     (ϵ, x, x)}}, and Γ1 := {Reva 7→ (ϵ, x, x)} is picked.        Now g(Γ1 , SD ) may return
     Some(Reva, (a, b, ab)).

  3. Then enumModel({Reva 7→ {(ϵ, ab, ab), (a, b, ab)}}) is recursively called, and U is set to
     {{Reva 7→ (x, y, xy)}, {{Reva 7→ (x, y, xR y)}}}. Suppose Γ2,1 := {Reva 7→ (x, y, xy)} is
     picked and U is updated to {{Reva 7→ (x, y, xR y)}} (inside this recursive call). g(Γ2,1 , SD )
     may return Some(Reva, (cab, ϵ, abc)).
  4. Now, enumModel({Reva 7→ {(ϵ, ab, ab), (a, b, ab), (cab, ϵ, abc)}}) is recursively called, and U is
     set to {{Reva 7→ (x, y, zy)}}, and Γ3 := {Reva 7→ (x, y, zy)} is picked. Now g(Γ3 , SD ) returns
     None. So, the algorithm outputs Γ3 and returns to the middle of Step 3 above.



                                                       46
  5. From U = {{Reva 7→ (x, y, xR y)}}, Γ2,2 := {Reva 7→ (x, y, xR y)} is picked. Since g(Γ2,2 , SD )
     returns None, the algorithm outputs Γ2,2 . Now U becomes empty in chain of recursive calls,
     and the algorithm terminates.
Above, we have obtained {Γ3 , Γ2,2 } as models of SD . By filtering out the non-minimal model Γ3 ,
we obtain {Γ2,2 } as the set of minimal models of SD . Since Γ2,2 = {Reva 7→ (x, y, xR y)} is also a
model of SG , we can conclude that SD ∪ SG is satisfiable.

A.3.2       Additional Details on Section 5.3
A CHC over multisets (CHC over sets, resp.) is of the form P1 (e     y1 ) ∧ · · · ∧ Pn (e
                                                                                        yn ) ∧ φ ⇒ H,
where Pi is a predicate variable, φ is a quantifier-free SMTP-formula (SSTP-formula) as defined in
Definition A.2, and H is of the form P (e y ) or false.
   The semantics and satisfiability of CHCs over multisets (sets, resp.) is defined in the same
manner as those of CHCs over words, except that ρ maps each variable to a multiset (a set, resp.)
over Σ and M maps each k-ary predicate to a k-ary relation on multisets (sets, resp.) over Σ.
Theorems 5.4 and 5.5 follow by the same argument as Theorems 5.1 and Theorems 5.2.
Example A.2. Recall the following CHCs over multisets.

 |x| = 1 ⇒ Insert(x, ϵ, x).        l = yl′ ∧ |x| = |y| = 1 ⇒ Insert(x, l, xl).
 l = yl ∧ |x| = |y| = 1 ∧ Insert(x, l′ , r) ⇒ Insert(x, l, yr).
        ′

 Sort(ϵ, ϵ).      |x| = 1 ∧ l = xl′ ∧ Sort(l′ , r′ ) ∧ Insert(x, r′ , r) ⇒ Sort(l, r).     Sort(l, r) ⇒ l = r.

We can compute the least CMTP-model for the definite clauses (i.e., the above CHCs except the
last one) as follows. We write CMTPinf for the multiset version of CTPinf, and disable the rule
R-CSubset for simplicity.
    We first set:

                        M0 = {Insert 7→ ∅, Sort 7→ ∅}
                        Γ0 = {Insert 7→ (a, ϵ, ϵ) ∧ (ϵ, ϵ, ϵ), Sort 7→ (a, ϵ) ∧ (ϵ, ϵ)}.

By calling g(Γ0 , SD ), we may obtain Some(Insert, (a, ϵ, a)). As CMTPinf({(a, ϵ, a)}) = (x, ϵ, x), we
now have:

                             M1 = {Insert 7→ {(a, ϵ, a)}, Sort 7→ ∅}
                             Γ1 = {Insert 7→ (x, ϵ, x), Sort 7→ (a, ϵ) ∧ (ϵ, ϵ)}.

By calling g(Γ1 , SD ), we may obtain Some(Sort, (ϵ, ϵ)). We now have:

                                M2 = {Insert 7→ {(a, ϵ, a)}, Sort 7→ (ϵ, ϵ)}
                                Γ2 = {Insert 7→ (x, ϵ, x), Sort 7→ (ϵ, ϵ)}.

By calling g(Γ2 , SD ), we may get Some(Insert, (a, b, ab)) and:

                           M3 = {Insert 7→ {(a, ϵ, a), (a, b, ab)}, Sort 7→ (ϵ, ϵ)}
                           Γ3 = {Insert 7→ (x, y, xy), Sort 7→ (ϵ, ϵ)}.

By calling g(Γ3 , SD ), we may get Some(Sort, (a, a)). We now have:

                       M4 = {Insert 7→ {(a, ϵ, a), (a, b, ab)}, Sort 7→ (ϵ, ϵ), (a, a)}
                       Γ4 = {Insert 7→ (x, y, xy), Sort 7→ (x, x)}.

At this point, g(Γ4 , SD ) returns None. Thus, we have obtained the least CSMTP-model Γ4 =
{Insert 7→ (x, y, xy), Sort 7→ (x, x)}. Since Γ4 is a model of the goal clause Sort(l, r) ⇒ l = r, we
can conclude that S is satisfiable.




                                                       47
B      Verification of Functional Queues Using Piecewise Con-
       junctive Solvable Tuple Patterns
We have considered conjunctive STPs, but not arbitrary Boolean combinations of STPs. While
inferring arbitrary Boolean combinations seems infeasible, we can allow a restricted form of them
called piecewise CSTPs. Let us fix a finite set P of predicates of the form λe   x.φ where φ is a
(quantifier-free) STP-formula such that Vars(φ) ⊆ {e
                                                   x}. We call |e
                                                                x| the arity of the predicate λe
                                                                                               x.φ,
and write arity(λe x.φ) for it. We sometimes omit “λe
                                                    x.” when it is clear from context. A (k-ary)
piecewise CSTPs over P is an expression of the form
                                         (p1 ⇒ γ1 ) ∧ · · · ∧ (pℓ ⇒ γℓ ),
where p1 , . . . , pℓ are k-ary predicates, and γ1 , . . . , γℓ are k-ary CSTPs. The language represented
by a k-ary piecewise CSTPs is defined by:
                                                               \
                      L((p1 ⇒ γ1 ) ∧ · · · ∧ (pℓ ⇒ γℓ )) =           {e
                                                                      s | pi (e
                                                                              s) ⇒ se ∈ L(γi )}.
                                                           i∈{1,...,ℓ}

Here, for pi = λe     x.φi , pi (e
                                 s) denotes [es/ex]φi . For example, if P = {p1 , p2 } where p1 =
λ(x1 , x2 , x3 ).x1 = ϵ and p2 = λ(x1 , x2 , x3 ).x1 ̸= ϵ. then (p1 ⇒ (x, y, ϵ)) ∧ (p2 ⇒ (x, y, y)) is a
piecewise CSTP. It represents the set of triples of the form (ϵ, s2 , ϵ) or (s1 , s2 , s2 ) where s1 ̸= ϵ.
    Typically, the set P of predicates would be {λe      x.xi = ϵ | i ∈ {1, . . . , k}} ∪ {λex.xi ̸= ϵ | i ∈
{1, . . . , k}}. CSTPs can be considered a special case of piecewise CSTPs where P = {true}.
    Theorem 5.1 can be extended for piecewise CSTPs.
Theorem B.1. Given a finite set P of predicates as defined above and a system S of CHCs on
words, it is decidable whether S has a piecewise CSTP-model over P.
Proof. This follows from the fact that S has a piecewise CSTP-model if and only if S ′ obtained
from S by replacing each k-ary predicate P (x1 , . . . , xk ) with (p1 (x1 , . . . , xk ) ⇒ P1 (x1 , . . . , xk )) ∧
· · · ∧ (pℓ (x1 , . . . , xk ) ⇒ Pℓ (x1 , . . . , xk )) has a CSTP-model. Here, Pi ’s are fresh predicates and
{p1 , . . . , pℓ } is the set of k-ary predicates in P.
    Below we apply the result above to the verification of functional queues.
Example B.1. Let us consider the following OCaml program.
      let initq = ([], [])
      let rec reva l1 l2 =
        match l1 with
          [] -> l2
        | x::l1’ -> reva l1’ (x::l2)
      let enq x (l1,l2) = (l1, x::l2)
      let deq (l1,l2) =
        match l1 with
          [] ->
           (match reva l2 [] with
              [] -> ([], l1, l2)
            | x::l -> ([x], l, [])
           )
        | x::l1’ -> ([x], l1’, l2)
      let rec enqall l (l1,l2) =
        match l with
          [] -> (l1,l2)
        | x::l’ -> enqall l’ (enq x (l1,l2))
      let rec deqall (l1,l2) =
        match deq(l1,l2) with
          ([], _, _) -> []
        | (l, l1’,l2’) -> l@(deqall (l1’, l2’))
      let main l =
        assert(deqall (enqall l initq) = l)

                                                        48
Here, a queue is implemented as a pair of lists (l1 , l2 ) where l1 l2R is the sequence of elements in the
queue, so that the amortized cost of each enqueue or dequeue operation is O(1) [53]. The dequeue
function deq either returns [ ] (when the queue is empty, i.e., l1 = l2 = [ ]) or a singleton set [x]
consisting of the first element x of the queue, along with the updated queue. If l1 = [ ], then the first
element of the queue is computed by extracting the first element of the reverse of l2 . Given a list
l of elements as input, the main function enqueues all the elements of l, dequeues all the elements
from the queue, and then asserts that the result equals l.
    The correctness of the above program (i.e., the lack of assertion failures) is reduced to the
satisfiability problem for the following CHCs.

       |x| = 1 ⇒ Enq(x, l1 , l2 , xl1 , l2 ).
       Deq(ϵ, ϵ, ϵ, ϵ, ϵ).
       |x| = 1 ∧ Reva(l2 , ϵ, xl) ⇒ Deq(ϵ, l2 , x, l, ϵ).
       |x| = 1 ⇒ Deq(xl1′ , l2 , x, l1′ , l2 ).
       EnqAll (ϵ, l1 , l2 , l1 , l2 ).
       l = xl′ ∧ |x| = 1 ∧ Enq(x, l1 , l2 , l1′ , l2′ ) ∧ EnqAll (l′ , l1′ , l2′ , r1 , r2 ) ⇒ EnqAll (l, l1 , l2 , r1 , r2 ).
       Deq(l1 , l2 , ϵ, l1′ , l2′ ) ⇒ DeqAll (l1 , l2 , ϵ).
       Deq(l1 , l2 , l, l1′ , l2′ ) ∧ l ̸= ϵ ∧ DeqAll (l1′ , l2′ , r) ⇒ DeqAll (l1 , l2 , lr).
       EnqAll (l, ϵ, ϵ, l1 , l2 ) ∧ DeqAll (l1 , l2 , r) ⇒ r = l.

Here, each predicate represents the relation between inputs and outputs of the corresponding func-
tion. For example, Enq(x, l1 , l2 , r1 , r2 ) means that enq x (l1 , l2 ) may return (r1 , r2 ). The clauses
for Reva (which are found in Section 5.1) have been omitted.
    The system of CHCs above has the following piecewise CSTP-model:

                       {
                            Reva 7→ (l1 , l2 , l1R l2 ),
                            Enq 7→ (l, l1 , l2 , l1 , lR l2 ),
                            Deq 7→ ((λ(l1 , l2 , x, r1 , r2 ).l1 = l2 = ϵ) ⇒ (ϵ, ϵ, ϵ, ϵ, ϵ))
                                     ∧ (λ(l1 , l2 , x, r1 , r2 ).l1 = ϵ ∧ l2 ̸= ϵ) ⇒ (ϵ, lx, xR , lR , ϵ))
                                     ∧ (λ(l1 , l2 , x, r1 , r2 ).l1 ̸= ϵ ∧ l2 ̸= ϵ) ⇒ (xl1 , l2 , x, l1 , l2 )),
                            EnqAll 7→ (l, l1 , l2 , l1 , lR l2 ),
                            DeqAll 7→ (l1 , l2 , l1 l2R )
                      }.

Thus, if we set P to {p1 , p2 , p3 , p4 , p5 } where:

                                           p1 = λ(l1 , l2 , l3 , l4 , l5 ).l1 = l2 = ϵ
                                           p2 = λ(l1 , l2 , l3 , l4 , l5 ).l1 = ϵ ∧ l2 ̸= ϵ
                                           p3 = λ(l1 , l2 , l3 , l4 , l5 ).l1 ̸= ϵ ∧ l2 ̸= ϵ
                                           p4 = λ(l1 , l2 , l3 ).true
                                           p5 = λ(l1 , l2 , l3 , l4 , l5 ).true,

then we can automatically prove the satisfiability of the CHCs above. We expect that necessary
predicates in P can typically be mined from the source program; in fact, in the above case, the
function deq performs case analysis on whether l1 and l2 are empty lists. A general method to find
an appropriate set P of predicates is left for future work.




                                                                    49
