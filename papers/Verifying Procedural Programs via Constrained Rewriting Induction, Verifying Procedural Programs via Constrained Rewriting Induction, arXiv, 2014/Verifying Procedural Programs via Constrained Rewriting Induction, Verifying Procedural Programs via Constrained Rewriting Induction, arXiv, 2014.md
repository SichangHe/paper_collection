                                                                                                                                                                A
                                        Verifying Procedural Programs via Constrained Rewriting Induction
                                        CARSTEN FUHS, Birkbeck, University of London
                                        CYNTHIA KOP, University of Innsbruck and University of Copenhagen
                                        NAOKI NISHIDA, Nagoya University


                                        This paper aims to develop a verification method for procedural programs via a transformation into Logically
                                        Constrained Term Rewriting Systems (LCTRSs). To this end, we extend transformation methods based on
                                        integer TRSs to handle arbitrary data types, global variables, function calls and arrays, as well as encode
                                        safety checks. Then we adapt existing rewriting induction methods to LCTRSs and propose a simple yet
                                        effective method to generalize equations. We show that we can automatically verify memory safety and
                                        prove correctness of realistic functions. Our approach proves equivalence between two implementations, so
arXiv:1409.0166v6 [cs.LO] 29 Aug 2025




                                        in contrast to other works, we do not require an explicit specification in a separate specification language.
                                        Categories and Subject Descriptors: D.2.4 [Software Engineering]: Software/Program Verification; I.2.3
                                        [Artificial Intelligence]: Deduction and Theorem Proving
                                        General Terms: Formal Verification
                                        Additional Key Words and Phrases: constrained term rewriting, inductive theorem proving, rewriting in-
                                        duction, lemma generation, program analysis
                                        ACM Reference Format:
                                        Carsten Fuhs, Cynthia Kop, and Naoki Nishida, 2017. Verifying Procedural Programs via Constrained
                                        Rewriting Induction. ACM Trans. Comput. Logic V, N, Article A ( YYYY), 48 pages.
                                        DOI:http://dx.doi.org/10.1145/0000000.0000000


                                           This is an author copy of the paper Verifying Procedural Programs via Con-
                                           strained Rewriting Induction, published at ACM TOCL in 2017. The published
                                           paper can be found at https://dl.acm.org/doi/10.1145/3060143.
                                           The contents are the same as in the published paper, except for one modification:
                                           in Definition 4.9 (the definition of E XPANSION), we had erroneously failed to
                                           include the condition that γ(x) ∈ Val ∪ V for all x ∈ Var (φ) ∪ Var (ψ). Without
                                           this condition, the definition is not necessarily well-defined, since for instance an
                                           equation f (x, x) ≈ a and a rule f (y, g(z)) → b [y > 0] would cause an equation to
                                           be created with g(z) > 0 in the constraint, which is not legal (assuming that g is
                                           not a theory symbol).




                                        This work is supported by Austrian Science Fund (FWF) international project I963, Marie Skłodowska-Curie
                                        action “HORIP” (H2020-MSCA-IF-2014, 658162), the Japan Society for the Promotion of Science (JSPS), and
                                        Nagoya University’s Graduate Program for Real-World Data Circulation Leaders from MEXT, Japan.
                                        Authors’ addresses: C. Fuhs, Dept. of Comp. Sci. and Inf. Sys., Birkbeck, Univ. of London, UK; C. Kop, Dept.
                                        of Comp. Sci., Univ. of Copenhagen, Denmark; N. Nishida, Grad. School of Informatics, Nagoya Univ., Japan.
                                        Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted
                                        without fee provided that copies are not made or distributed for profit or commercial advantage and that
                                        copies show this notice on the first page or initial screen of a display along with the full citation. Copyrights
                                        for components of this work owned by others than ACM must be honored. Abstracting with credit is per-
                                        mitted. To copy otherwise, to republish, to post on servers, to redistribute to lists, or to use any component
                                        of this work in other works requires prior specific permission and/or a fee. Permissions may be requested
                                        from Publications Dept., ACM, Inc., 2 Penn Plaza, Suite 701, New York, NY 10121-0701 USA, fax +1 (212)
                                        869-0481, or permissions@acm.org.
                                        © YYYY ACM 1529-3785/YYYY/-ARTA $15.00
                                        DOI:http://dx.doi.org/10.1145/0000000.0000000


                                                                   ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:2                                                                           C. Fuhs, C. Kop, N. Nishida

1. INTRODUCTION
Ensuring with certainty that a program always behaves correctly is a hard problem.
One approach to this is formal verification—proving with mathematical rigor that all
executions of the program will have the expected outcome. Several methods for this
have been investigated (see e.g., [Huth and Ryan 2000]). However, classically many of
them require expert knowledge to manually prove relevant properties about the code.
  Instead, we hope to raise the degree of automation, ideally creating a fully automatic
verification / refutation process and tools to raise developer productivity. Indeed, over
the last years automatic provers for program verification have flourished, as witnessed,
e.g., by tool competitions like SV-COMP [SV-COMP] and the Termination Competition
(http://termination-portal.org/wiki/Termination Competition). Program verification is
also recognized in industry, cf. e.g. Facebook’s safety prover Infer [Calcagno et al. 2015]
or Microsoft’s temporal prover T2 [Brockschmidt et al. 2016]. However, these tools
generally use specific reasoning techniques for imperative programs and benefit from
the progress in automated theorem proving over the last decades only to a limited
extent. This suggests likely avenues for improvement.
  One such avenue is inductive theorem proving. This method is well investigated in
functional programming [Bundy 2001] and term rewriting, the underlying core calcu-
lus of functional programming. To check a functional program f against a specification
by a reference implementation fspec , it suffices that f (→−
                                                           x ) ≈ fspec (→
                                                                        −
                                                                        x ) is an inductive
theorem. Thus, no explicit specification language is needed: giving a (possibly not opti-
mized) reference implementation fspec in the same programming language suffices.
  To analyze imperative programs (in C, Java, etc.), recent works have applied trans-
formations into term rewrite systems (e.g., [Otto et al. 2010]). In particular, con-
strained rewriting systems are popular as target language, since logical constraints to
model the control flow can be separated from terms to model intermediate states [Fu-
ruichi et al. 2008; Falke and Kapur 2009; Sakata et al. 2009; Nakabayashi et al. 2010;
Falke et al. 2011]. Unifying existing approaches, Kop and Nishida [2013] have pro-
posed the framework of logically constrained term rewriting systems (LCTRSs).
Aims. The aim of this paper is twofold. First, we propose a new transformation method
from procedural programs into constrained term rewriting. This transformation makes
it possible to use the many methods available to term rewriting also to analyze imper-
ative programs. Unlike previous methods, we do not limit interest to integer functions.
   Second, we develop a verification method for LCTRSs, based on rewriting induc-
tion [Reddy 1990]—a well-investigated method of inductive theorem proving—to prove
(total) equivalence of two functions. We also supply two generalization techniques, the
main one of which is specialized for transformed iterative functions.
   The applications are many. First, checking equivalence between different implemen-
tations comes to mind. This allows the user to determine automatically if a modifica-
tion in the program has changed its semantics (see e.g. [Godlin and Strichman 2013;
Lahiri et al. 2012]). Proposing equivalent replacements may even be done automati-
cally, via algorithm recognition (see e.g. [Alias and Barthou 2003]).
   In compilation, automated equivalence checking can validate correctness of compiler
optimizations on a per-instance basis [Necula 2000; Pnueli et al. 1998] or once-and-for-
all for a given optimization template [Kundu et al. 2009; Lopes and Monteiro 2016].
Equivalence checking is also used in proofs of secure information flow [Terauchi and
Aiken 2005] and can be used to prove safety properties, e.g., memory safety.
Why LCTRSs. Direct support of basic types like the integers, and of constraints to re-
strict evaluation—features absent in basic TRSs—is essential to handle realistic pro-
grams. Unlike earlier constrained rewriting systems, LCTRSs do not limit the under-
lying theory to (linear) integer arithmetic: we might use (combinations of) arbitrary

                     ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:3

first-order theories, including, e.g., n-dimensional integer arrays, floating point num-
bers, and bitvectors. This makes it possible to natively handle sophisticated programs.
   Despite the generality, we get strong results on LCTRSs by reducing analysis prob-
lems like termination and equivalence to a sequence of satisfiability problems over
the underlying theories. Automatic tools—like our tool Ctrl [Kop and Nishida 2015] for
rewriting, termination, and inductive theorem proving—can defer such queries to an
external SAT Modulo Theories (SMT) solver [Nieuwenhuis et al. 2006], as a black box.
Future advances in the SMT world then directly transfer to analysis of LCTRSs.
Structure. We first recall the LCTRS formalism from [Kop and Nishida 2013] (§ 2) and
show a way to translate procedural programs to LCTRSs (§ 3). Then we lift rewriting
induction methods for constrained rewriting to LCTRSs (§ 4) and strengthen them
with two dedicated generalization techniques (§ 5). Finally we discuss automation and
experimental results (§ 6) as well as related and future work (§§ 7–8) and conclude.
Contributions over the conference version. The present paper provides several addi-
tional contributions over the conference version [Kop and Nishida 2014]: (1) We signif-
icantly extend our method to translate procedural programs to LCTRSs. (2) We extend
our theory of constrained inductive theorem proving to disproving equivalence (follow-
ing [Sakata et al. 2009; Falke and Kapur 2012]) and add several inference rules. (3)
We provide an additional generalization technique and a detailed proof strategy to au-
tomate rewriting induction for translated procedural programs. (4) We have improved
the implementation and added an automatic translation from C programs to LCTRSs.
1.1. Motivating Example
Aside from business applications, automatic equivalence proving can be used as an
aid in grading student programming assignments. Combining a test run of the assign-
ments on a set of sample inputs (which identifies many incorrect programs, but leaves
false positives) with an automatic correctness check can save teachers a lot of time.
   Example 1.1. Consider the following programming assignment.
     Write a function sum which, given an integer array and its length as input,
     returns the sum of its elements. Do not modify the input array.
We consider four different C implementations of this exercise:
 int sum1(int arr[],int n){                  int sum2(int arr[], int n) {
   int ret=0;                                   int ret, i;
   for(int i=0;i<n;i++)                         for (i = 0; i < n; i++) {
     ret+=arr[i];                                 ret += arr[i];
   return ret;                                  }
 }                                              return ret;
                                             }

 int sum3(int arr[], int len) {                 int sum4(int *arr, int k) {
    int i;                                         if (k <= 0) return 0;
    for (i = 0; i < len-1; i++)                    return arr[k-1] +
      arr[i+1] += arr[i];                                  sum4(arr, k-1);
    return arr[len-1];                          }
 }
  The first solution is correct. The second is not, because ret is not initialized—which
may be missed in standard tests depending on the compiler used. The third solution is
incorrect because the array is modified against the instructions, and moreover, gives a
random result or segmentation fault if len = 0. The fourth solution is correct.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:4                                                                             C. Fuhs, C. Kop, N. Nishida

   These implementations can be transformed into the following LCTRSs:
   (1a) sum1(arr, n) → u(arr, n, 0, 0)
   (1b) u(arr, n, ret, i) → error                              [i < n ∧ (i < 0 ∨ i ≥ size(arr))]
   (1c) u(arr, n, ret, i) → u(arr, n, ret + select(arr, i), i + 1)    [i < n ∧ 0 ≤ i < size(arr)]
   (1d) u(arr, n, ret, i) → return(arr, ret)                                              [i ≥ n]

   (2a)    sum2(arr, n) → u(arr, n, ret, 0)
              u rules as copied from above

   (3a) sum3(arr, len) → v(arr, len, 0)
   (3b)   v(arr, len, i) → error                   [i < len − 1 ∧ (i < 0 ∨ i + 1 ≥ size(arr))]
   (3c)   v(arr, len, i) → v(store(arr, i + 1, select(arr, i + 1) + select(arr, i)), len, i + 1)
                                                      [i < len − 1 ∧ 0 ≤ i ∧ i + 1 < size(arr)]

  (3d)       v(arr, len, i) → return(arr, select(arr, len − 1))
                                                        [i ≥ len − 1 ∧ 0 ≤ len − 1 < size(arr)]
  (3e)       v(arr, len, i) → error        [i ≥ len − 1 ∧ (len − 1 < 0 ∨ len − 1 ≥ size(arr))]

  (4a)     sum4(arr, k) → return(arr, 0)                                          [k ≤ 0]
  (4b)     sum4(arr, k) → error                                       [k − 1 ≥ size(arr)]
  (4c)     sum4(arr, k) → w(select(arr, k − 1), sum4(arr, k − 1)) [0 ≤ k − 1 < size(arr)]
  (4d)        w(n, error) → error
  (4e) w(n, return(a, r)) → return(a, n + r)
 Note that arrays carry an implicit size (their allocated memory) which is queried to
 model the runtime behavior of the C program and test for out-of-bound errors. The
 fresh variable in the right-hand side of (2a) models that the third parameter of u is
 assigned an arbitrary integer. The details of this transformation are discussed in § 3.
   Using inductive theorem proving, we can now prove that
— ∀arr ∈ array(int). ∀len ∈ int. sum1(arr, len) ↔∗ sum4(arr, len) if 0 ≤ len ≤ size(arr)
— ∃arr ∈ array(int). ∃len ∈ int. sum3(arr, len) ̸↔∗ sum4(arr, len) with 0 ≤ len ≤ size(arr)
 So sum1 and sum4 return the same result on any input such that the given length
 does not cause out-of-bound errors, but sum3 and sum4 do not. (It seems likely that the
 disproof obtained from inductive theorem proving could be used to extract counterex-
 ample inputs, but at present we have not studied a systematic way of doing so.)
   For sum2, we do have sum2(arr, len) ↔∗ sum4(arr, len), since we can always choose
 to instantiate ret with 0. The system is not confluent; we can also prove that there
 exist a, n such that sum2(a, n) →∗ s ̸= t ←∗ sum4(a, n) for terms s, t in normal form. As
 explained in § 6, we use a proof strategy which typically proves only the “̸=” statement.
 1.2. Practical Use
 The primary application that we see for our technique is the following:
    1.2.1. Comparing a function to a specification. As in Ex. 1.1, we can verify correctness of
 a C function f against a reference implementation g by translating both functions to
 LCTRS rules (§ 3) and proving that f(x1 , . . . , xn ) ≈ g(x1 , . . . , xn ) [true] is an induc-
 tive theorem. If we only need equivalence under given preconditions on the input
 variables—such as 0 ≤ len ≤ size(arr ) in Ex. 1.1—we formulate this as a constraint
 φ and analyze whether f(x1 , . . . , xn ) ≈ g(x1 , . . . , xn ) [φ] is an inductive theorem.
    Note that we do not require a separate specification language—although if desirable,
 it is of course possible to specify the reference implementation directly as an LCTRS.

                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                  A:5

  Further possible applications of our technique include:
   1.2.2. Code optimization (or other improvement). Sometimes the “reference implementa-
tion” g suggested above can simply be an existing—and inefficient, or inelegant—
version of a function. Thus, inductive theorem proving can be used to prove that it
is safe to replace a function in a large real-life program by an optimized alternative.
  1.2.3. Error checking. As the transformation from C to LCTRSs includes error checking
(as seen for memory safety violations in Ex. 1.1), we can use inductive theorem proving
to verify the absence of such errors. This is done by adding error-checking rules, e.g.,
                 errorfree(return(a, n)) → true                       errorfree(error) → false
and proving that errorfree(sum4(a, n)) ≈ true [φ] is an inductive theorem, where φ is
the precondition on the input. Aside from memory safety, this approach can be used to
certify the absence of for instance divisions by zero or integer overflow. The key is in
the transformation, where we can choose which constructions result in an error.
   1.2.4. Classical correctness checks. Aside from comparisons to an example implementa-
tion, we can also specify a correctness property directly in SMT. For instance, given an
implementation of the strlen function, its correctness could be verified by proving that
strlen(x) ≈ return(n) [0 ≤ n < size(x) ∧ select(x, n) = 0 ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0)]
is an inductive theorem. Alternatively, we can use extra rules to test properties in SMT.
   Example 1.2. To analyze correctness of an implementation of strcpy, we may use
                  test(x, n, error) → false
             test(x, n, return(y)) → b [b ⇔ ∀i ∈ {0, . . . , n}(select(x, i) = select(y, i))]
and prove that the following equation is an inductive theorem:
                                test(x, n, strcpy(y, x)) ≈ true
   [0 ≤ n < size(x) ∧ n < size(y) ∧ select(x, n) = 0 ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0)]
Note that this more sophisticated test is needed in this case, since correctness of strcpy
does not require that x = y if strcpy(x) →∗ return(y) (the sizes of x and y may differ).
2. PRELIMINARIES
In this section, we briefly recall Logically Constrained Term Rewriting Systems (usu-
ally abbreviated as LCTRSs), following the definitions in [Kop and Nishida 2013].
2.1. Logically Constrained Term Rewriting Systems

Many-sorted terms. We introduce terms, typing, substitutions, contexts, and subterms
(with corresponding terminology) in the usual way for many-sorted term rewriting.
   Definition 2.1. We assume given a set S of sorts and an infinite set V of variables,
each variable equipped with a sort. A signature Σ is a set of function symbols f , disjoint
from V, each equipped with a sort declaration [ι1 × · · · × ιn ] ⇒ κ, with all ιi and κ sorts.
For readability, we often write κ instead of [] ⇒ κ. The set Terms(Σ, V) of terms over Σ
and V contains any expression s such that ⊢ s : ι can be derived for some sort ι, using:
                                ⊢ s1 : ι1 . . . ⊢ sn : ιn
           (x : ι ∈ V)                                       (f : [ι1 × · · · × ιn ] ⇒ κ ∈ Σ)
    ⊢x:ι                          ⊢ f (s1 , . . . , sn ) : κ
  We fix Σ and V. Note that for every term s, there is a unique sort ι with ⊢ s : ι.
   Definition 2.2. Let ⊢ s : ι. We call ι the sort of s. Let Var (s) be the set of variables
occurring in s; we say that s is ground if Var (s) = ∅.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:6                                                                               C. Fuhs, C. Kop, N. Nishida

    Definition 2.3. A substitution γ is a sort-preserving total mapping from V to
 Terms(Σ, V). The result sγ of applying a substitution γ to a term s is s with all occur-
 rences of a variable x replaced by γ(x). The domain of γ, Dom(γ), is the set of variables
 x with γ(x) ̸= x. The notation [x1 := s1 , . . . , xk := sk ] denotes a substitution γ with
 γ(xi ) = si for 1 ≤ i ≤ n, and γ(y) = y for y ∈/ {x1 , . . . , xn }. For two substitutions γ and
 δ, their composition γ ◦ δ is given by (γ ◦ δ)(x) = γ(δ(x)) = (xδ)γ for all variables x.
    Two terms s and t are unifiable if there exists a substitution γ such that sγ = tγ.
 Then γ is called a unifier for s and t. If moreover for all unifiers γ ′ for s and t there is a
 substitution δ such that γ ′ = δ ◦ γ, we call γ a most general unifier (mgu) for s and t.
    Definition 2.4. Given a term s, a position in s is a sequence p of positive integers
 such that s|p is defined, where s|ϵ = s and f (s1 , . . . , sn )|i·p = (si )|p . We call s|p a sub-
 term of s. If ⊢ s|p : ι and ⊢ t : ι, then s[t]p denotes s with the subterm at position
 p replaced by t. A context C is a term containing one or more typed holes 2i : ιi . If
 s1 : ιi , . . . , sn : ιn , we define C[s1 , . . . , sn ] as C with each 2i replaced by si .

 Logical terms. Specific to LCTRSs, we consider different kinds of symbols and terms.
    Definition 2.5. We assume given:
— signatures Σterms and Σtheory such that Σ = Σterms ∪ Σtheory ;
— a mapping I which assigns to each sort ι occurring in Σtheory a set Iι ;
— a mapping J which assigns to each f : [ι1 × · · · × ιn ] ⇒ κ ∈ Σtheory a function in
  Iι1 × · · · × Iιn =⇒ Iκ ;
— for all sorts ι occurring in Σtheory a set Valι ⊆ Σtheory of values: function symbols
  a : [] ⇒ ι such that J gives a bijective mapping from Valι to Iι .
                                              S
We require that Σterms ∩ Σtheory ⊆ Val = ι Valι . The sorts occurring in Σtheory are
called theory sorts, and the symbols theory symbols. Symbols in Σtheory \ Val are calcu-
lation symbols. A term in Terms(Σtheory , V) is called a logical term.
    Definition 2.6. For ground logical terms, let Jf (s1 , . . . , sn )K := Jf (Js1 K, . . . , Jsn K). For
 every ground logical term s there is a unique value c such that JsK = JcK; we say that c is
 the value of s. A constraint is a logical term φ of some sort bool with Ibool = B = {⊤, ⊥},
 the set of booleans. A constraint φ is valid if JφγK = ⊤ for all substitutions γ which map
 Var (φ) to values, and satisfiable if JφγK = ⊤ for some such substitutions. A substitution
 γ respects φ if γ(x) is a value for all x ∈ Var (φ) and JφγK = ⊤.
   Terms in Terms(Σterms , ∅) can be thought of as the primary objects of rewriting: a
 reduction typically begins and ends with such terms, with elements of Σtheory \ Val
 (also called calculation symbols) to perform calculations in the underlying theory.
    We typically choose a theory signature with Σtheory ⊇ Σcore                    core
                                                                  theory , where Σtheory contains
 true, false : bool, ∧, ∨, ⇒: [bool × bool] ⇒ bool, ¬: [bool] ⇒ bool, and, for all theory sorts ι,
 symbols =ι , ̸=ι : [ι × ι] ⇒ bool, and an evaluation function J that interprets these sym-
 bols as expected. We omit the sort subscripts from = and ̸= when clear from context.
    Definition 2.7. The standard integer signature Σint                    core
                                                                theory is Σtheory ∪ {+, −, ∗, exp, div,
 mod : [int × int] ⇒ int; ≤, <: [int × int] ⇒ bool} ∪ {n : int | n ∈ Z} with values true, false and
 n for all n ∈ Z. Thus, we use n (in sans-serif font) as the function symbol for n ∈ Z (in
 math font). We define J in the natural way, except: since all Jf must be total functions,
 we set Jdiv (n, 0) = Jmod (n, 0) = Jexp (n, k) = 0 for all n and all k < 0. Of course, when
 constructing LCTRSs, we normally add explicit error checks to prevent such calls.

                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                             A:7

   Example 2.8. Let S = {int, bool}, and Σ = Σterms ∪ Σint
                                                       theory , where

                           Σterms = { fact : [int] ⇒ int } ∪ { n : int | n ∈ Z }
Then both int and bool are theory sorts. We also define set and function interpretations,
i.e., Iint = Z, Ibool = B, and J is defined as above. With = for =int and infix notation,
examples of logical terms are 0 = 0 + −1 and x + 3 ≥ y + −42. Both are constraints.
5 + 9 is also a (ground) logical term, but not a constraint. Expected starting terms are,
e.g., fact(42) or fact(fact(−4)): ground terms fully built using symbols in Σterms .

Rules and rewriting. We adapt the standard notions of rewriting (see, e.g., [Baader and
Nipkow 1998]) by including constraints and adding rules to perform calculations.
   Definition 2.9. A rule is a triple ℓ → r [φ] with ℓ and r terms of the same sort and φ a
constraint. Here, ℓ has the form f (ℓ1 , . . . , ℓn ) and contains at least one symbol in Σterms \
Σtheory (so ℓ is not a logical term). If φ = true with J (true) = ⊤, we may write ℓ → r. We
define LVar (ℓ → r [φ]) as Var (φ) ∪ (Var (r) \ Var (ℓ)). A substitution γ respects ℓ → r [φ]
if γ(x) ∈ Val for all x ∈ LVar (ℓ → r [φ]), and JφγK = ⊤. The rule is left-linear if ℓ is
linear, i.e., all variables occur at most once in ℓ, and irregular if Var (φ) \ Var (ℓ) ̸= ∅.
  Note that it is allowed to have Var (r) ̸⊆ Var (ℓ), but fresh variables in the right-hand
side may only be instantiated with values. This is done to model user input or random
choice. Otherwise, variables outside the constraint may be instantiated by any term;
we do not impose strategies like innermost or call-by-value reduction.
   Definition 2.10. We assume given a set of rules R and let Rcalc be the set
{f (x1 , . . . , xn ) → y [y = f (→ −
                                    x )] | f : [ι1 × · · · × ιn ] ⇒ κ ∈ Σtheory \ Val} (writing →
                                                                                                −
                                                                                                x
for x1 , . . . , xn ). The rewrite relation →R is a binary relation on terms, defined by:
              C[ℓγ] →R C[rγ] if ℓ → r [φ] ∈ R ∪ Rcalc and γ respects ℓ → r [φ]
Here, C is a context with exactly one hole. We say that the reduction occurs at position
p if C = C[2]p . Let s ↔R t if s →R t or t →R s. A reduction step with Rcalc is called a
calculation. A term is in normal form if it cannot be reduced with →R . We say that t
is a normal form of s if s →∗R t and t is a normal form. The relation →R is confluent if
whenever s →∗R t and s →∗R t′ , there exists also some u with t →∗R u and t′ →∗R u.
   We usually call the elements of Rcalc rules—or calculation rules–even though their
left-hand side is a logical term. Note that if →R is confluent, every term has at most one
normal form (intuitively, then R is deterministic with respect to big-step semantics).
   Definition 2.11. For f (ℓ1 , . . . , ℓn ) → r [φ] ∈ R we call f a defined symbol; non-defined
elements of Σterms and all values are constructors. Let D be the set of all defined sym-
bols and Cons the set of constructors. A term in Terms(Cons, V) is a constructor term.
  Now we may define a logically constrained term rewriting system (LCTRS) as the
abstract rewriting system (Terms(Σ, V), →R ). An LCTRS is usually given by supplying
Σ, R, and an informal description of I and J if these are not clear from context.
  Example 2.12. To implement an LCTRS calculating the factorial function, we use
the signature Σ from Ex. 2.8 and the following rules:
              Rfact = { fact(x) → 1 [x ≤ 0] , fact(x) → x ∗ fact(x − 1) [¬(x ≤ 0)] }
Using calculation steps, a term 3 − 1 reduces to 2 in one step (using the calculation rule
x − y → z [z = x − y]), and 3 ∗ (2 ∗ (1 ∗ 1)) reduces to 6 in three steps. Using also the
rules in Rfact , fact(3) reduces in ten steps to 6.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:8                                                                               C. Fuhs, C. Kop, N. Nishida

   Example 2.13. To implement an LCTRS calculating the sum of elements in an
array, let Ibool = B, Iint = Z, Iarray(int) = Z∗ , so array(int) is mapped to finite-length
integer sequences. Let Σtheory = Σinttheory ∪ {size : [array(int)] ⇒ int, select : [array(int) ×
int] ⇒ int} ∪ {a | a ∈ Z∗ }. (We do not encode arrays as lists: every “array”—integer
sequence—a corresponds to a unique symbol a.) The interpretation function J behaves
on Σint
     theory as usual, maps the values a to the corresponding integer sequence, and has:


Jsize (a) = k if a = ⟨n0 , . . . , nk−1 ⟩    Jselect (a, i) = ni if a = ⟨n0 , . . . , nk−1 ⟩ and 0 ≤ i < k
                                                              0 otherwise

In addition, let Σterms = { sum, sum0 : [array(int)] ⇒ int }∪{ n : int | n ∈ Z }∪{ a | a ∈ Z∗ }
and let R consist of
  sum(x) → sum0(x, size(x) − 1)              sum0(x, k) → select(x, k) + sum0(x, k − 1) [k ≥ 0]
                                             sum0(x, k) → 0                             [k < 0]

Note that this implementation differs from the ones in Ex. 1.1, because there we an-
alyzed encodings of imperative programs; on C level there is no functionality for the
programmer to explicitly query the size of an array. Here, we avoided boundary checks.

  Values are new in LCTRSs compared to older styles of constrained rewriting. These
representatives of the underlying theory are always constants (constructor symbols
which do not take arguments), even if they represent complex structures, as seen in
Ex. 2.13. Note that variables in a rule’s constraint must be instantiated by values; for
instance in Ex. 2.12, a term fact(1 + 2) must be reduced by a calculation first. We also
do not match modulo theories, e.g., we do not equate 0 + (x + y) with y + x for matching.

Differences to [Kop and Nishida 2013]. In the original definition of LCTRSs, variables
in V are unsorted, and a separate variable environment is used for typing. Also, →R
is there defined as the union of two relations →rule and →calc rather than including
Rcalc . These changes give equivalent results, but the current definitions cause less
bookkeeping. A larger difference is the restriction on rules: in [Kop and Nishida 2013]
left-hand sides must have a root symbol in Σterms \ Σtheory . We follow Kop [2013] and
Kop and Nishida [2014] in weakening this (only asking that they are not logical terms).

2.2. Quantification
The definition of LCTRSs does not permit constraints with quantifiers (constraints are
terms, and first-order rewriting does not allow quantifiers in terms). In, for instance,
an LCTRS over integers and arrays, which has addtoend : [int × array(int)] ⇒ array(int) ∈
Σtheory and extend : [array(int) × int] ⇒ array(int) ∈ Σterms , we cannot specify a rule like:

      extend(arr , x) → addtoend(x, arr ) [∀y ∈ {0, . . . , size(arr ) − 1}(x ̸= select(arr , y))]

  However, one of the key features of LCTRSs is that theory symbols, including pred-
icates, are not confined to a fixed list. Therefore, we can add a new symbol to Σtheory
(and J ). For the extend rule, we might introduce a symbol notin : [int × array(int)] ⇒ bool
with Jnotin (u, ⟨a0 , . . . , an−1 ⟩) = ⊤ iff for all i: u ̸= ai , and replace the constraint by
notin(x, arr ). This generates exactly the same reduction relation as the original rule.
  Thus, we can permit quantifiers in the constraints of rules and also on right-hand
sides of rules, as an intuitive notation for fresh predicates. However, an unbounded
quantification would likely not be useful, as it would give an undecidable relation →R .

                         ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:9


   Comment: One might argue that adding symbols like this is problematic in prac-
   tice: no SMT solver will support new symbols like notin. However, for the tech-
   nique this makes no difference. In an implementation, we might allow quanti-
   fiers as syntactic sugar (and pass the same sugar to the SMT solver), or add a
   layer on top of the SMT solver which translates the new symbol(s), replacing for
   instance (notin u a ) by (forall ((x Int)) (distinct u (select a x))).

2.3. Rewriting Constrained Terms
In LCTRSs, the objects of study are terms, with →R defining the relation between
them. However, for analysis it is often useful to consider constrained terms:
   Definition 2.14. A constrained term is a pair s [φ] of a term s and a constraint φ. We
say s [φ] and t [ψ] are equivalent, notation s [φ] ∼ t [ψ], if for all substitutions γ which
respect φ there is a substitution δ which respects ψ such that sγ = tδ, and vice versa.
   Intuitively, a constrained term s [φ] represents all terms sγ where γ respects φ, and
can be used to reason about such terms. Equivalent constrained terms represent the
same set of terms; for example f(0) [true] ∼ f(x) [x = 0], and g(x, y) [x > y] ∼ g(z, u) [u ≤
z − 1]. Note that s [φ] ∼ s [ψ] if and only if ∀→
                                                −
                                                x (∃→−
                                                     y (φ) ↔ ∃→ −
                                                                z (ψ)) holds, where Var (s) =
 →
 −                          →
                            −                             →
                                                          −
{ x }, Var (φ) \ Var (s) = { y } and Var (ψ) \ Var (s) = { z }.
    Definition 2.15. For a rule ρ := ℓ → r [ψ] ∈ R ∪ Rcalc and position q, we let s [φ] →ρ,q
t [φ] if there exists a substitution γ such that s|q = ℓγ, t = s[rγ]q , γ(x) is a value or
variable in Var (φ) for all x ∈ LVar (ℓ → r [ψ]), and φ ⇒ (ψγ) is valid. Let s [φ] →base t [φ]
if s [φ] →ρ,q t [φ] for some ρ, q. The relation →R on constrained terms is defined as
∼ · →base · ∼. We say that s [φ] →R t [ψ] at position q by rule ρ if s [φ] ∼ · →ρ,q · ∼ t [ψ].
    Example 2.16. In the LCTRS from Ex. 2.12, we have fact(x) [x > 3] →R x ∗ fact(x −
1) [x > 3]. Now we can use a calculation rule x − y → z [z = x − y], with a non-empty ∼-
step, as follows: x∗fact(x−1) [x > 3] ∼ x∗fact(x−1) [x > 3∧z = x−1] →base x∗fact(z) [x >
3 ∧ z = x − 1]. The ∼-relation holds because indeed ∀x(x > 3 ↔ ∃z(x > 3 ∧ z = x − 1)).
   Example 2.17. The ∼-relation also allows us to reformulate the constraint after
a reduction. For example, with the rule f(x) → g(y) [y > x], we have: f(x) [x > 3] ∼
f(x) [x > 3 ∧ y > x] →base g(y) [x > 3 ∧ y > x] ∼ g(y) [y > 4]. We do not have that
f(x) [true] →R g(x + 1) [true], as x + 1 cannot be instantiated to a value.
   Example 2.18. A constrained term does not always need to be reduced in the most
general way. With the rule f(x) → g(y) [y > x], we have f(0) [true] ∼ f(0) [y > 0] →base
g(y) [y > 0], but we also have f(0) [true] ∼ f(0) [1 > 0] →base g(1) [1 > 0] ∼ g(1) [true].
As intended, constrained reductions give information about usual reductions:
   T HEOREM 2.19. If s [φ] →R t [ψ], then for all substitutions γ which respect φ there
exists δ which respects ψ such that sγ →R tδ. Both steps use the same rule and position.
    P ROOF. We first observe (**): If u [ξ] →base q [ξ], then for any substitution γ which
respects ξ also uγ →R qγ. Proof: if u [ξ] →base q [ξ], then there are p, ℓ → r [c] and δ such
that u|p = ℓδ, q = u[rδ]p , δ(x) ∈ Var (ξ) ∪ Val for all x ∈ LVar (ℓ → r [c]) and ξ ⇒ (cδ) is
valid. With η = γ ◦ δ, we have (uγ)|p = u|p γ = ℓδγ = ℓη and qγ = u[rδ]p γ = (uγ)[rδγ]p =
(uγ)[rη]p . We also have η(x) = δ(x)γ ∈ Val for x ∈ LVar (ℓ → r [c]) because γ respects ξ
and, since JξγK = ⊤ and ξ ⇒ (cδ) is valid, also J(cδ)γK = JcηK = ⊤. So indeed uγ →R qγ.
    Now, suppose s [φ] →R t [φ], so s [φ] ∼ s′ [ξ] →base t′ [ξ] ∼ t [ψ], and let γ respect φ. By
definition of ∼, there is some substitution η which respects ξ such that sγ = s′ η. By (**)
s′ η →R t′ η. Again by definition of ∼, we find δ which respects ψ such that t′ η = tδ.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:10                                                                           C. Fuhs, C. Kop, N. Nishida

   T HEOREM 2.20. If s [φ] →R t [ψ], then for all substitutions δ which respect ψ there
exists γ which respects φ such that sγ →R tδ. Both steps use the same rule and position.
  P ROOF. Parallel to the proof of Thm. 2.19: if s [φ] ∼ s′ [ξ] →base t′ [ξ] ∼ t [ψ], then by
definition of ∼ there are suitable η, γ such that tδ = t′ η ←R s′ η = sγ.
   Comment: The relation →R on constrained terms is not stable: for instance, in
   the system from Ex. 2.18, we can derive f(x) [true] →R g(x) [true] even though
   f(0) [true] ̸→R g(0) [true]. This is because the variables in a constrained term s [φ]
   are fully changeable; one can see variables in Var (s) as universal and the oth-
   ers as existential. This is not problematic, as we do not instantiate constrained
   terms; to reason with constrained reduction we only use Theorems 2.19 and 2.20.

3. TRANSFORMING IMPERATIVE PROGRAMS INTO LCTRSS
Equivalence-preserving transformations of imperative programs into constrained
rewriting systems operating on integers have been investigated in e.g. [Falke and Ka-
pur 2009; Falke et al. 2011; Furuichi et al. 2008]; more generally, such translations
from imperative to functional programs have been investigated at least since [Mc-
Carthy 1960]. Although these papers use different definitions of constrained rewrit-
ing, the proposed transformations can be adapted to produce LCTRSs that operate on
integers, i.e., use Σtheory as in Ex. 2.12. What is more, we can extend the ideas to also
handle more advanced programming structures, such as arrays and exceptions.
  In this section, we will discuss a number of ideas towards a translation from C to
LCTRS. A more detailed and formal treatment of the limitation to integers and one-
dimensional integer arrays is available online along with an implementation, at:
                       http://www.trs.css.i.nagoya-u.ac.jp/c2lctrs/
Given the extensiveness of the C specification, we will not attempt to prove that the
result of our transformation corresponds to the origin. Instead, we shall rely on an
appeal to intuition. An advantage is that the same ideas apply to other programming
languages; we should be able to use similar translations for, e.g., Python or Java.
3.1. Transforming Simple Integer Functions
The base form of the transformation—limited to integer functions with no global vari-
ables or function calls—is very similar to the transformations for integer TRSs in
[Falke and Kapur 2009; Falke et al. 2011; Furuichi et al. 2008]. Each function is trans-
formed separately. We introduce a function symbol for every statement (including dec-
larations), which operates on the variables in scope. The transition from one statement
to another is encoded as a rule, with assignments reflected by argument updates in the
right-hand side, and conditions by the constraint. Return statements are encoded by
reducing to an expression returnf (e), where returnf : [int] ⇒ resultf is a constructor.
  Example 3.1. Consider the following C function and its translation:
                                                                 fact(x) → u1 (x, 1)
  int fact(int x) {                                             u1 (x, z) → u2 (x, z, 1)
    int z = 1;                                                u2 (x, z, i) → u3 (x, z, i)     [i ≤ x]
    for (int i = 1; i <= x; i++) z *= i;                      u2 (x, z, i) → u5 (x, z)        [¬(i ≤ x)]
    return z;                                                 u3 (x, z, i) → u4 (x, z ∗ i, i)
  }                                                           u4 (x, z, i) → u2 (x, z, i + 1)
                                                                u5 (x, z) → returnfact (z)
For Σtheory we assume the standard integer signature; Σterms contains fact, all ui and
the constructor returnf , all of which have output sort resultf and argument sorts int.

                      ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                       A:11

   A realistic translation of C code must also handle the absence of a boolean data type,
 operator precedence, and expressions with side effects (e.g., a loop condition --x). All
 this is easily doable1 (and included in our implementation), but for the sake of brevity
 we will not go into detail here.

   Finally, the generated system is optimized to make it more amenable to analysis:2

— rules are combined where possible, e.g., replacing a pair of rules ℓ → u(r1 , . . . , rn ) [φ]
  and u(x1 , . . . , xn ) → s [true] by ℓ → s[x1 := r1 , . . . , xn := rn ] if u is not used elsewhere;
— unused arguments of function symbols are removed, such as the second (but not the
  first!) argument of u in an LCTRS with rules u(x, y, z) → u(x − 1, y + 1, z ∗ 2) [x > 0]
  and u(x, y, z) → return(z) [¬(x > 0)];
— constraints are simplified, for instance replacing ¬(x > 0) by x ≤ 0 in the rules above.

   We will use these optimizations also for the extended transformations of §§ 3.2–3.6.
   Comment: When time complexity—defined as, e.g., the number of certain calcula-
   tion steps—is considered, the argument removal step is dangerous, as it may re-
   move calculations. In such cases we would use a different simplification method.

    Example 3.2. Optimizing the LCTRS from Ex. 3.1, we obtain:

               fact(x) → u2 (x, 1, 1)                   u2 (x, z, i) → u2 (x, z ∗ i, i + 1) [i ≤ x]
                                                        u2 (x, z, i) → returnfact (z)       [i > x]



 Differences to older work. In contrast to existing transformations to integer TRSs
 (e.g. [Falke and Kapur 2009; Falke et al. 2011; Furuichi et al. 2008]), we do not consider
 basic blocks, but simply create rules for every statement; this gives no substantial dif-
 ference after optimization. Additionally, returnf is new here: in the work by Falke et al,
 the return statement is omitted, as they focus on termination, while in [Furuichi et al.
 2008] the final term reduces directly to the return-value, e.g. u4 (x, z) → z + x [x ≤ 0].

 3.2. Non-Integer Data Types
 Integers are not special: as the definition of LCTRSs permits arbitrary theories, we can
 handle any data type in C. We might for instance interpret double as either real num-
 bers or double-precision floating point numbers; this choice is left to the user and may
 vary by application. The only requirement is that a suitable theory signature—with
 corresponding SMT solver if the system is to be analyzed automatically—is available.
 The translation is straightforward, with the only difficulty that type casts must be
 made explicit, and we need to use separate symbols such as +. for double addition.

    Example 3.3. Consider the following C function and its translation.


 1 This is discussed in the formal treatment at http://www.trs.css.i.nagoya-u.ac.jp/c2lctrs/formal.pdf
 2 Variations of such preprocessing steps preserving the properties of interest to simplify the output of an
 automatic translation are fairly standard in program analysis, see e.g. [Albert et al. 2008; Alpuente et al.
 2007; Beyer et al. 2009; Falke et al. 2011; Giesl et al. 2017; Spoto et al. 2009].


 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:12                                                                             C. Fuhs, C. Kop, N. Nishida

double halfsum(double thold) { halfsum(t) → u (t, 0.0, 2)
                                                 2
  double ret = 0.0;              u2 (t, r, d) → u4 (t, r +. 1.0/todouble(d), d) [d < 100]
  for (int d = 2; d < 100;       u2 (t, r, d) → returnhalfsum (rnd)             [d ≥ 100]
                  d *= 2) {      u4 (t, r, d) → returnhalfsum (r)               [r >. t]
    ret += 1.0 / d;              u4 (t, r, d) → u2 (t, r, d ∗ 2)                [r ≤. t]
    if (ret > thold) return ret;
} }
This demonstrates both an explicit cast and one possible way to handle an undefined
return value (by a fresh variable, which may be instantiated with a random value).

3.3. Error Handling
The transformation of § 3.1 does not fully reflect the original C program: as computers
have limited memory, integers are internally represented as bitvectors. To address this,
we could change the theory. Rather than using Z, we let Valint = {MININT, . . . , MAXINT}
and make J+ , J− , and J∗ wrap around (e.g., J− (MININT, 1) = MAXINT). The resulting
LCTRS has the same rules, but acts more closely to the real program behavior.
  However, integer overflow is often indicative of an error. Indeed, in C an overflow for
the type int leads to undefined behavior (which also surfaces in optimizing compilers
such as gcc or clang). In order to model this (or other instances of undefined behavior
in C, such as a missing return statement), we will reduce to a special error state.
  Thus, for every rule ui (x1 , . . . , xn ) → r [φ]: if this rule represents a transition where
an error may occur under condition τ , then we split it in two:
              ui (x1 , . . . , xn ) → r [φ ∧ ¬τ ]       ui (x1 , . . . , xn ) → errorf [φ ∧ τ ]
As usual, we simplify the resulting constraint (writing, e.g., x < 0 instead of ¬(x ≥ 0)).
  Example 3.4. Continuing Ex. 3.2, we generate the following rewrite rules:
   fact(x) → u2 (x, 1, 1)
u2 (x, z, i) → u2 (x, z ∗ i, i + 1) [i ≤ x ∧ z ∗ i ≤ MAXINT ∧ z ∗ i ≥ MININT ∧ i + 1 ≤ MAXINT]
u2 (x, z, i) → errorfact            [i ≤ x ∧ (z ∗ i > MAXINT ∨ z ∗ i < MININT ∨ i + 1 > MAXINT)]
u2 (x, z, i) → returnfact (z)       [i > x]
Note that we could easily model assertions and throw statements for exceptions in the
same way. Division by zero is handled in a similar way.
  We can choose whether to add error transitions before or after the simplification step.
The distinction is important: when simplifying, calculations which do not contribute to
the final result are thrown away. In the case of overflow errors, it may seem reasonable
to consider the post-simplification rules, as we did in Ex. 3.4. In the case of for instance
division by zero, we should add the errors to the pre-simplification rules.
   Comment: When transforming a function into an LCTRS, we can choose what
   errors to model. For instance, we could ignore overflows (effectively assuming
   unbounded integers), but still test for division by zero. We could also let errorf be
   a constructor which takes an argument, i.e., errorf : [Errors] ⇒ resultf ∈ Σterms ,
   where Errors is a sort with constructors IntegerOverflow, DivisionByZero, and so on.

3.4. Global Variables
Thus far, we have considered very local code: a function never calls other functions
or modifies global variables. By altering the return constructors, we easily change the
latter: we assume that a function symbol is given all global variables that it uses as
input, and that it returns those global variables it alters as output, along with its
return value. This change also allows for non-redundant void functions.

                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                      A:13

   Example 3.5. Consider the following short program and its (simplified) translation:
   int best;
   int up(int x) {                                 up(b, x) → returnup (x, 1) [x > b]
     if (x > best) { best = x; return 1; }         up(b, x) → returnup (b, 0) [x ≤ b]
     return 0;
   }
 3.5. Function Calls
 Next, let us consider function calls. A difficulty is that they may occur in an expres-
 sion, e.g., fact(3) + 5, which is not well sorted in the corresponding LCTRS: fact(3) has
 sort resultfact , not int. To avoid this issue, and to propagate errors, we split off function
 calls occurring inside expressions other than var = func(arg 1 , . . . , arg n ) and store their
 return value into a temporary variable. For example:
                                                               int ncr(int x, int y) {
   int ncr(int x, int y) {                                       int a = fact(x);
      int a = fact(x);                                           int tmp1 = fact(y);
      int b = fact(y) * fact(x - y);
      return a / b;
                                                              =⇒ int tmp2 = fact(x - y);
                                                                 int b = tmp1 * tmp2;
   }                                                             return a / b;
                                                               }
   This change may cause declarations at places in the function where a C compiler
 would not accept them, but for the translation, this is no issue. We translate the result-
 ing function by executing function calls in a separate parameter and using a separate
 step to examine the outcome of a function call and assign it to the relevant variable(s).
   Example 3.6. The ncr program above is transformed to the following optimized
 LCTRS (where we test for division by zero but not integer overflow for simplicity):
                     ncr(x, y) → u2 (x, y, fact(x))                        u2 (x, y, errorfact ) → errorncr
      u2 (x, y, returnfact (k)) → u3 (x, y, k, fact(y))                 u3 (x, y, a, errorfact ) → errorncr
   u3 (x, y, a, returnfact (k)) → u4 (x, y, a, k, fact(x − y)) u4 (x, y, a, t1 , errorfact ) → errorncr
                 u4 (x, y, a, t1 , returnfact (k)) → errorncr                     [t1 ∗ k = 0]
                 u4 (x, y, a, t1 , returnfact (k)) → returnncr (a div (t1 ∗ k)) [t1 ∗ k ̸= 0]
 3.6. Statically Allocated Arrays
 Finally, let us consider arrays. After we have seen Ex. 1.1 and the way side effects were
 handled in § 3.4, this is largely as expected. For now, we will not consider aliasing.
    To start, we must fix a theory signature and corresponding interpretations. For a
 given theory sort ι which admits at least one value, say 0ι , let array(ι) be a new sort
 and Iarray(ι) = Iι∗ —so each value corresponds to a finite sequence. We introduce the
 following theory symbols (in addition to Σint
                                             theory and other desired theories):

— sizeι : [array(ι)] ⇒ int: we define Jsizeι (a) as the length of the sequence a.
— selectι : [array(ι) × int] ⇒ ι: if a = ⟨a0 , . . . , an−1 ⟩, we define Jselectι (a, k) = ak if 0 ≤ k < n
  and Jselectι (a, k) = 0ι otherwise.
— storeι : [array(ι) × int × ι] ⇒ array(ι): if a = ⟨a0 , . . . , an−1 ⟩, we define Jstoreι (a, k, v) =
  ⟨a0 , . . . , ak−1 , v, ak+1 , . . . , an−1 ⟩ if 0 ≤ k < n and Jstoreι (a, k, v) = a otherwise.
 We will usually omit the subscript ι when the sort is clear from context.
    Our arrays are different from SMT-LIB (cf. http://www.smt-lib.org/), where arrays
 are functions from one (possibly infinite) domain to another. For program analysis,
 finite-length sequences seem practical instead. SMT problems on our arrays can be
 translated to SMT-LIB format using an additional integer variable asize for the size of
 an array a and universal quantification to set entries outside the array to a fixed value.

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:14                                                                               C. Fuhs, C. Kop, N. Nishida

   We encode lookups a[i] as select(a, i); for assignments a[i] = e, we replace a by store(a,
i, e). To ensure correctness here, we add boundary checks to the constraint and reduce
to errorf if such a check is not satisfied. After an assignment, the updated variable is
included in the return value since the underlying memory of the array was altered.
   Example 3.7. Consider the following C implementation of the strcpy function,
which copies the contents of original into the array goal, until a 0 is reached.
void strcpy(char goal[], char original[]) {
  int i = 0;
  for (; original[i] != 0; i++) goal[i] = original[i];
  goal[i] = 0;
}
  For simplicity, we think of strings as integer arrays (although alternative choices
for Ichar make little difference). The function never updates original, but may update
goal, so the return value must include the latter. We obtain the following LCTRS:
       strcpy(gl, org) → v(gl, org, 0)
          v(gl, org, i) → errorstrcpy     [i < 0 ∨ i ≥ size(org)]
          v(gl, org, i) → w(gl, org, i) [0 ≤ i < size(org) ∧ select(org, i) = 0]
          v(gl, org, i) → errorstrcpy     [0 ≤ i < size(org) ∧ select(org, i) ̸= 0 ∧ i ≥ size(gl)]
          v(gl, org, i) → v(store(gl, i, select(org, i)), org, i + 1)
                                          [0 ≤ i < size(org) ∧ select(org, i) ̸= 0 ∧ i < size(gl)]
          w(gl, org, i) → errorstrcpy     [i < 0 ∨ i ≥ size(gl)]
          w(gl, org, i) → returnstrcpy (store(gl, i, 0)) [0 ≤ i < size(gl)]
Here, the notation 0 ≤ i < size(org) is shorthand for 0 ≤ i ∧ i < size(org). Note that this
LCTRS could be further simplified by combining the third rule with the last two rules.
   Comment: It should now be clear how the systems from § 1.1 have been trans-
   lated from C code to LCTRSs. The only deviation is that there we have included
   the array arr in the return value of sum1, sum2, and sum4, which is not necessary
   as it is not modified in these cases. This was done to allow for a direct comparison
   with sum3, where the array is modified. In addition, the return and error symbols
   in these examples are not indexed, for the same reason.

3.7. Dynamically Allocated Arrays and Aliasing
The transformation in § 3.6 allows us to abstract from the underlying memory model
when encoding arrays. This makes analysis easier, but does not allow for aliasing or
pointer arithmetic beyond accessing an array element. As a result, properties we prove
about strcpy from Ex. 3.7 might fail to hold for a call like strcpy(a, a).
  As we seek to handle only part of the language, this does not need to be an issue; in
practice, a fair number of programs are written without explicit pointer use and with
easily removable aliasing only. For example, we might replace strcpy(a, a) by strcpy′ (a),
and create new rules for strcpy′ by collapsing the variables in the rules for strcpy. To
handle programs with more sophisticated pointer use, including dynamically allocated
arrays, we can encode the memory as a list of arrays and pass this along as a variable.
This is somewhat beyond the scope of this paper, but is explored in Appendix A.2.
3.8. Remarks
The treatment in this section is both informal and incomplete: we have discussed
only a fraction of the C language—albeit an important fraction for verification. We
believe that these ideas easily extend further, with for instance the switch statement,
user-defined data structures, or standard library functions, as well as compiler-specific

                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                               A:15

choices. Important to note is that the translation gives several choices. Most perti-
nently, we saw the choices what sort interpretations to use (e.g., whether int should
be mapped to the set of integers or bitvectors) and what errors to consider.
   In this paper, and in line with our automatic translation at http://www.trs.css.i.
nagoya-u.ac.jp/c2lctrs/, we have chosen to work with real integers and not test for over-
flows. We also do not permit aliasing. By avoiding the more sophisticated translation
steps, we obtain LCTRSs which are correspondingly easier to analyze.
   The LCTRSs from this transformation are well behaved: all rules are left-linear and
non-overlapping,3 and have the property that all ground terms can be reduced or are
constructor terms. Rules ℓ → r [φ] can have variables in r or φ which do not occur in
ℓ: this is mostly due to unspecified values in the C code. Where such variables do not
occur—or are removed in the optimization step—the resulting LCTRSs are confluent.

4. REWRITING INDUCTION FOR LCTRSS
In this section, we adapt the inference rules from [Reddy 1990; Falke and Kapur 2012;
Sakata et al. 2009] to inductive theorem proving with LCTRSs. This provides the core
theory for rewriting induction, strengthened with two generalization techniques in § 5.
  We start by listing some restrictions we need to impose on LCTRSs for the method to
work (§ 4.1). Then, we provide the theory for the technique (§ 4.2) and some illustrative
examples (§ 4.3). Compared to older definitions of rewriting induction, we make several
changes to best handle the new formalism. We complete by proving correctness (§ 4.4).

4.1. Restrictions
In order for rewriting induction to be successful, we need to impose certain restrictions.
   Definition 4.1. In the following, we limit interest to LCTRSs which satisfy (1)–(4):
(1) all core theory symbols are present in Σtheory : Σtheory ⊇ Σcore
                                                                theory ;
(2) the LCTRS is terminating: there is no infinite reduction s1 →R s2 →R · · · ;
(3) the system is quasi-reductive: i.e., for every ground term s either s ∈ Terms(Cons, ∅)
    (we say s is a ground constructor term), or there is some t such that s →R t;
(4) there are ground terms of every sort occurring in Σ.
   Property 1 is the standard assumption from § 2. We will need symbols such as =,
∧ and ⇒ to add new information to a constraint. Termination (property 2) essentially
indicates that a program cannot run indefinitely; this is crucial for our inductive rea-
soning, as the method uses induction on an extension of →R on terms.
   Property 3 indicates that an evaluation cannot get “stuck”; roughly, that pattern
matching and case analysis are exhaustive. Termination and quasi-reductivity to-
gether ensure that every ground term reduces to a constructor term. This makes it
possible to do an exhaustive case analysis on the rules applicable to an equation, and
lets us assume that variables are always instantiated by ground constructor terms.
   The last property is natural, since inductive theorem proving makes a statement
on ground terms; there is no point in regarding empty sorts. Together with quasi-
reductivity and termination, this implies that all sorts admit ground constructor terms.
   Methods to prove both quasi-reductivity and termination have previously been pub-
lished for different styles of constrained rewriting; see e.g. [Falke and Kapur 2012] for

3 Non-overlappingness means that for every term s and rule ρ : ℓ → r [φ] such that s reduces with ρ at
the root position: (a) there are no other rules ρ′ such that s reduces with ρ′ at the root position, and (b)
if s reduces with any rule at a non-root position q, then q is not a position of ℓ. For our translations, this
holds because (a) rules with the same defined symbol have either incompatible constraints or non-unifiable
arguments, and (b) in a rule f (ℓ1 , . . . , ℓn ) → r [φ], the terms ℓi do not contain defined or calculation symbols.


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:16                                                                           C. Fuhs, C. Kop, N. Nishida

quasi-reductivity and [Falke 2009; Sakata et al. 2011] for termination. These meth-
ods are easily adapted to LCTRSs. Quasi-reductivity is handled in [Kop 2017] and is
moreover always satisfied by systems obtained from the transformations in § 3. Some
basics of termination analysis for LCTRSs are discussed in [Kop 2013].

  Example 4.2. As a running example in this section, we will consider Rfact , which
combines the factorial function from Ex. 3.2 with a recursive variant obtained from
int fact(int x) { if (x <= 1) return 1; else return x * fact(x - 1); }.

(1) factiter(x) → iter(x, 1, 1)                   (4)        factrec(x) → return(1)       [x ≤ 1]
(2) iter(x, z, i) → iter(x, z ∗ i, i + 1) [i ≤ x] (5)        factrec(x) →
(3) iter(x, z, i) → return(z)             [i > x]                  mul(x, factrec(x − 1)) [x > 1]
                                                  (6) mul(x, return(y)) → return(x ∗ y)

(Function symbols were renamed for readability.) We can choose a signature which in-
cludes Σcoretheory , and each of the sorts—int, bool, result—clearly admits ground terms (e.g.,
0, false, return(0)). The system was obtained using § 3, so is quasi-reductive. Termination
follows because in the recursive rule (2), the value x − i is decreased, while bounded
from below by 0, and in the recursion in rule (5), x decreases against the bound 1.
This could be proved using, e.g., interpretations with support for built-in integers and
non-theory symbols [Fuhs et al. 2009], and is automatically handled by our tool Ctrl.

4.2. Rewriting Induction
We now introduce the notions of constrained equations and inductive theorems.

   Definition 4.3. A (constrained) equation is a triple s ≈ t [φ] with s and t terms and
φ a constraint. We write s ≃ t [φ] to denote either s ≈ t [φ] or t ≈ s [φ]. A substitution
γ respects s ≈ t [φ] if γ respects φ and Var (s) ∪ Var (t) ⊆ Dom(γ); it is called a ground
constructor substitution if all γ(x) with x ∈ Dom(γ) are ground constructor terms.
  An equation s ≈ t [φ] is an inductive theorem of an LCTRS R if sγ ↔∗R tγ for any
ground constructor substitution γ that respects this equation.

  Intuitively, if an equation f (→−
                                  x ) ≈ g(→
                                          −
                                          x ) [φ] is an inductive theorem, then f and g
define the same function (conditional on φ, and assuming confluence). As we require
termination, we thus consider total equivalence in the categorization of Godlin and
Strichman [2008]: on all inputs, both programs terminate and return the same values.
  To prove that an equation is an inductive theorem, we consider nine inference
rules, in §§ 4.2.1–4.2.9. Four originate in [Reddy 1990]; three are based on extensions
[Bouhoula 1997; Falke and Kapur 2012; Sakata et al. 2009]; two are new. All these
rules modify a triple (E, H, b), called a proof state. Here, E is a set of equations, H a
set of rules with →R∪H terminating, and b ∈ {COMPLETE, INCOMPLETE}. A rule in H
plays the role of an induction hypothesis for “proving” the equations in E and is called
an induction rule. The flag b indicates whether we can use the current proof state to
refute that the initial equation is an inductive theorem; we can do so if b = COMPLETE.
  The definition of these rules is used in the following result, proved in § 4.4.

   T HEOREM 4.4. Let an LCTRS with rules R and signature Σ, satisfying the restric-
tions from Def. 4.1, be given. Let E be a finite set of equations and let flag = COMPLETE if
we can confirm that R is confluent and flag = INCOMPLETE otherwise. If (E, ∅, flag) ⊢∗ri
(∅, H, flag ′ ) for some H, flag ′ , then every equation in E is an inductive theorem of R. If
(E, ∅, flag) ⊢∗ri ⊥, then there is some equation in E that is not an inductive theorem of R.

                      ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                        A:17

   Example 4.5. We will illustrate the various rules by proving that factrec and factiter
 are equivalent on positive input,4 by showing that (FCT.A) is an inductive theorem:
                                  (FCT.A) factrec(n) ≈ factiter(n) [n ≥ 1]
 Rfact is confluent: as seen in § 3.8, it is left-linear and non-overlapping, and the right-
 hand sides do not introduce fresh variables, so confluence is given by [Kop and Nishida
 2013, Thm. 4]. Thus, we will start with the proof state ( { (FCT.A) }, ∅, COMPLETE ).
   Let us now define the nine inference rules to reduce proof states.
   4.2.1. S IMPLIFICATION. Our first inference rule originates in [Reddy 1990] and can be
 considered one of the core rules of rewriting induction.
   Definition 4.6. If s ≈ t [φ] →R∪H u ≈ t [ψ], where ≈ is seen as a fresh constructor for
 the purpose of constrained term reduction,5 then we may derive:
                          (E ⊎ {(s ≃ t [φ])}, H, b) ⊢ri (E ∪ {(u ≈ t [ψ])}, H, b)
   This inference rule allows us to reduce one side of an equation. This is altered from
 Reddy’s definition by using constrained rather than normal reduction.
   Example 4.7. Following Ex. 4.5, we observe that factiter(n) can be reduced by the
 unconstrained rule (1). Thus, using S IMPLIFICATION we obtain the proof state:
                  ( { (FCT.B) : iter(n, 1, 1) ≈ factrec(n) [n ≥ 1] } , ∅, COMPLETE )
 Here we reduce the right-hand side of the equation (recall that s ≃ t in the rule means
 s ≈ t or t ≈ s); the reduced term moves to the left-hand side of the new equation. Next,
 observe that iter(n, 1, 1) can be reduced by rule (2) if n ≥ 1; S IMPLIFICATION then gives:
             ( { (FCT.C) : iter(n, 1 ∗ 1, 1 + 1) ≈ factrec(n) [n ≥ 1] } , ∅, COMPLETE )
   Recall that constrained reduction also allows for steps with calculation rules; see,
 e.g., Ex. 2.16. The added complexity is that we must decide how to handle the fresh
 variable these rules introduce. In this paper we will use the following strategy:
— if s →calc u then s ≈ t [φ] is simplified to u ≈ t [φ], e.g. f(0 + 1) ≈ r [φ] reduces to
  f(1) ≈ r [φ];
— a calculation containing variables can be replaced by a fresh variable, which is de-
  fined in the (updated) constraint, e.g. f(x + 1) ≈ r [φ] reduces to f(y) ≈ r [φ ∧ y = x + 1];
  if such a definition already occurs in the constraint, the relevant variable is used
  instead, e.g. f(x + 1) ≈ r [φ ∧ y = x + 1] reduces to f(y) ≈ r [φ ∧ y = x + 1].
    Example 4.8. The proof state from Ex. 4.7 is further simplified to:
                  ( { (FCT.D) : iter(n, 1, 2) ≈ factrec(n) [n ≥ 1] } , ∅, COMPLETE )
   4.2.2. E XPANSION. Our second core rule also originates from [Reddy 1990], but has
 been more heavily adapted to support irregular rules.
   Definition 4.9. Let s, t be terms and φ a constraint, all with variables distinct from
 those in R (we can always rename the variables in the rules to support this), and p a

 4 We limit interest to positive input for demonstration purposes only: these functions give the same result
 on all input, but considering only n ≥ 1 allows us to apply the inference rules in a convenient order.
 5 It does not suffice if s [φ] →
                                 R u [ψ]: when reducing constrained terms, unused variables may be manipu-
 lated at will, which causes problems if they are used in t. For example,
                  f (x + 0) [x > y] ∼ f (x + 0) [z = x + 0] →base f (z) [z = x + 0] ∼ f (x) [x < y]
 but we should certainly not replace an equation f (x + 0) ≈ g(y) [x > y] by f (x) ≈ g(y) [x < y].


 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:18                                                                            C. Fuhs, C. Kop, N. Nishida

position of s. Let Expd (s ≈ t [φ], p) be a set of equations containing, for all rules ℓ →
r [ψ] ∈ R such that ℓ is unifiable with s|p with most general unifier γ and γ(x) ∈ Val ∪ V
for all x ∈ Var (φ) ∪ Var (ψ), an equation s′ ≈ t′ [φ′ ] where sγ ≈ tγ [(φγ) ∧ (ψγ)] →R s′ ≈
t′ [φ′ ] with rule ℓ → r [ψ] at position 1 · p. Here, as in S IMPLIFICATION, ≈ is seen as
a fresh constructor for the reduction. If s|p is basic (i.e., s|p = f (s1 , . . . , sn ) with f ∈ D
and all si constructor terms), we may derive:
                   (E ⊎ {s ≃ t [φ]}, H, b) ⊢ri (E ∪ Expd (s ≈ t [φ], p), H, b)
If, moreover, R ∪ H ∪ {s → t [φ]} is terminating, we may even derive:
           (E ⊎ {s ≃ t [φ]}, H, b) ⊢ri (E ∪ Expd (s ≈ t [φ], p), H ∪ {s → t [φ]}, b)
  Intuitively, this inference rule uses narrowing for a case analysis: Expd generates all
resulting equations if a ground constructor instance of s ≈ t [φ] is reduced at position
p of s. In addition, we save the current equation as a rule to take an induction step.
   Example 4.10. Following Ex. 4.8, we consider which rules may apply to an instance
of factrec(n) with n ≥ 1. For Expd (factrec(n) ≈ iter(n, 1, 2) [n ≥ 1], ϵ), we choose:
                                                                                 
               (FCT.E):               return(1) ≈ iter(n, 1, 2) [n ≥ 1 ∧ n ≤ 1],
               (FCT.F): mul(n, factrec(n − 1)) ≈ iter(n, 1, 2) [n ≥ 1 ∧ n > 1]

In both cases we used the unifier γ = [x := n]. If we write (FCT.D−1 ) for the rule gener-
ated from the inverse of (FCT.D)—so factrec(n) → iter(n, 1, 2) [n ≥ 1]—R ∪ {(FCT.D−1 )}
is terminating as the new rule does not cause mutual recursion between iter and factrec.
We continue with ( {(FCT.E), (FCT.F)}, {(FCT.D−1 )}, COMPLETE ). Now we can show
the second kind of calculation step, using S IMPLIFICATION on (FCT.F), which gives:
                                                                                     
      (FCT.E):           return(1) ≈ iter(n, 1, 2) [n ≥ 1 ∧ n ≤ 1],       {(FCT.D−1 )},
                                                                        ,
      (FCT.G): mul(n, factrec(m)) ≈ iter(n, 1, 2) [n > 1 ∧ m = n − 1]      COMPLETE

Here, we also removed the redundant clause n ≥ 1, which is allowed by definition of
→R on constrained terms. As n ≥ 1 ∧ n ≤ 1 implies n = 1, we may use S IMPLIFICATION
with rule (3) on (FCT.E), and with rule (2) followed by calculations on (FCT.G), to get:
                                                                                     
     (FCT.H): return(1) ≈ return(1)               [n = 1],                {(FCT.D−1 )},
                                                                        ,
      (FCT.I): iter(n, 2, 3) ≈ mul(n, factrec(m)) [n > 1 ∧ m = n − 1]      COMPLETE

Now we can use “induction”: we eliminate the occurrence of factrec with a S IMPLIFI -
CATION step using the induction rule (FCT.D−1 ) and substitution [n := m]. This gives:
                                                                                      
    (FCT.H):            return(1) ≈ return(1) [n = 1],                     {(FCT.D−1 )},
                                                                         ,
    (FCT.J): mul(n, iter(m, 1, 2)) ≈ iter(n, 2, 3) [n > 1 ∧ m = n − 1]      COMPLETE

  Note that the choice of Expd is non-deterministic, as it uses reduction of constrained
terms. The most natural choice for Expd (s ≈ t [φ], p)—which we use in examples—is
       { s[r]p γ ≈ tγ [(φγ) ∧ (ψγ)] | ℓ → r [ψ] ∈ R, s|p unifies with ℓ with mgu γ }
However, for irregular rules in particular, it may be strategic to choose a different set.
Consider for example a (non-confluent) LCTRS with rules f (x) → g(y) [x > 0 ∧ x > y]
and f (x) → g(y) [x ≤ 0 ∧ x ≤ y]. With the choice for Expd (s ≈ t [φ], p) above, an equation
f (x) ≈ g(0) [true] results in { g(y) ≈ g(0) [x > 0 ∧ x > y], g(y) ≈ g(0) [x ≤ 0 ∧ x ≤ y] }. If
g is a constructor, neither of these equations can be handled. Using the full definition
of E XPANSION, we can choose g(0) ≈ g(0) [true] for both equations.

                       ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:19

  Also note that there is no choice in the orientation of the rule added to H: this is
determined by the side of the equation on which the expansion was applied. Thus, in
Ex. 4.10 we were not allowed to add (FCT.D) instead of (FCT.D−1 ).
  Our definition of E XPANSION differs from both its original and existing work on
constrained rewriting induction. To start, those works define Expd (s ≈ t [φ], p) simply
as the “natural choice” given above. Second, we included a case where no rule is added,
to allow for progress when adding the rule might cause non-termination. Forms of this
case appear as a separate rule in other work, e.g., C ASE A NALYSIS in [Bouhoula 1997]
and R EWRITE /PARTIAL S PLITTING in [Bouhoula and Jacquemard 2008b; 2008a]. A
weaker form with constraints is given in [Falke and Kapur 2012] (C ASE -S IMPLIFY).

  4.2.3. D ELETION. The last of the core rules serves to remove solved equations from E.

   Definition 4.11. If s = t or φ is not satisfiable, we can delete s ≈ t [φ] from E:

                                    (E ⊎ {s ≈ t [φ]}, H, b) ⊢ri (E, H, b)

   Compared to the corresponding rule in [Reddy 1990], the unsatisfiability case is new;
it is similar to the corresponding rules in [Sakata et al. 2009; Falke and Kapur 2012].

   Example 4.12. Following Ex. 4.10, the left- and right-hand side of (FCT.H) are
the same, so we may remove the equation with D ELETION, obtaining ( { (FCT.J) },
{ (FCT.D−1 ) }, COMPLETE ). We will see the other form of D ELETION in Ex. 4.18.

  4.2.4. P OSTULATE. Sometimes it is useful to make the problem seemingly harder. To
this end, we consider the last inference rule from [Reddy 1990].

   Definition 4.13. For any set of equations E ′ , we can derive:

                                 (E, H, b) ⊢ri (E ∪ E ′ , H, INCOMPLETE)

  The P OSTULATE rule allows us to add additional equations to E (although at a price:
we cannot conclude non-equivalence after adding a potentially unsound equation). The
reason to do so is that in proving the equations in E ′ to be inductive theorems, we may
derive new induction rules. These can then be used to simplify the elements of E.

   Example 4.14. Following Ex. 4.12, E XPANSION followed by S IMPLIFICATION gives:

                (FCT.K): mul(n, iter(m, 2, 3)) ≈ iter(n, 6, 4) [n ≥ 3 ∧ m = n − 1]

But now a pattern starts to arise. Expanding and fully simplifying again, we obtain:

                (FCT.L): mul(n, iter(m, 6, 4)) ≈ iter(n, 24, 5) [n ≥ 4 ∧ m = n − 1]

And so on. Here, (FCT.K) cannot be handled by the induction rule (FCT.J−1 ), nor can
(FCT.L) be handled by (FCT.K−1 ). We have a divergence: a sequence of increasingly
complex equations, each generated from the same leg in an E XPANSION (see also the
divergence critic in [Walsh 1996]). Yet the previous induction rules never apply to the
new equation. This suggests we need a lemma equation. We use P OSTULATE to get:

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:20                                                                            C. Fuhs, C. Kop, N. Nishida

          (FCT.J):         mul(n, iter(m, 1, 2)) ≈ iter(n, 2, 3)
                                                                                    
                                                                    
                                  [n > 1 ∧ m = n − 1]                    {(FCT.D−1 )}, 
                                                                    
                                                                       ,
       
        (FCT.M):
                         mul(n, iter(m, x, y)) ≈ iter(n, x′ , y ′ )    INCOMPLETE
                                                                                       
                                              ′             ′
                     [n ≥ y ∧ m = n − 1 ∧ y = y + 1 ∧ x = x ∗ y]
                                                                    

Using E XPANSION on the right-hand of (FCT.M), we have:
                                                                                    
    (FCT.J):           mul(n, iter(m, 1, 2)) ≈ iter(n, 2, 3)      
                               [n > 1 ∧ m = n − 1]
                                                                  
                                                                 
                                                                         (FCT.D−1 )
                                                                                   
                         ′    ′ ′
                                                                   
  (FCT.N):       iter(n, x ∗ y , y + 1) ≈ mul(n, iter(m, x, y))                      ,
                                                                                     
                                                                                −1
                                                                     ,   (FCT.M    )
         [n ≥ y ∧ m = n − 1 ∧ y ′ = y + 1 ∧ x′ = x ∗ y ∧ y ′ ≤ n]                    
                                                                        INCOMPLETE
                                                                                     
                                  ′
   (FCT.O):           return(x ) ≈ mul(n, iter(m, x, y))
                                                                  
                                                                                      
   
                                                                  
                                                                   
                                    ′            ′            ′
          [n ≥ y ∧ m = n − 1 ∧ y = y + 1 ∧ x = x ∗ y ∧ y > n]
                                                                  

But now we have added (FCT.M−1 ) as an induction rule. As a result—since n > 1
clearly implies n ≥ 2—we can use S IMPLIFICATION with a substitution [n := n, x :=
1, y := 2, x′ := 2, y ′ := 3] to reduce (FCT.J) to the equation mul(n, iter(m, 1, 2)) ≈
mul(n, iter(m, 1, 2)) [. . . ], which we may immediately remove by D ELETION. We continue
with the proof state ({ (FCT.N), (FCT.O) }, { (FCT.D−1 ), (FCT.M−1 ) }, INCOMPLETE).
  Although the need to choose arbitrary new equations for use in P OSTULATE may
seem somewhat problematic, this is actually a key step. Complex theorems typically
require more than straight induction, both in our setting and in mathematical proofs
in general. Thus, generation of suitable lemma equations E ′ is not only part, but even
at the heart, of inductive theorem proving. Hence, this subject has been extensively in-
vestigated [Bundy et al. 2005; Kapur and Sakhanenko 2003; Kapur and Subramaniam
1996; Nakabayashi et al. 2010; Urso and Kounalis 2004; Walsh 1996], and a large va-
riety of lemma generation techniques exist, at least in the setting without constraints.
  4.2.5. G ENERALIZATION. A very typical use of P OSTULATE is to generalize a problem-
atic equation. For simplicity, we add a shortcut to do this in one step.
  Definition 4.15. If for all substitutions γ which respect φ there is a substitution δ
which respects ψ with sγ = s′ δ and tγ = t′ δ, then we can derive:
              (E ⊎ {s ≈ t [φ]}, H, b) ⊢ri (E ∪ {s′ ≈ t′ [ψ]}, H, INCOMPLETE)
   This inference rule is rarely necessary: we could usually add s′ ≈ t′ [ψ] using P OS -
TULATE , and use the resulting induction rules to eliminate s ≈ t [φ], as we did in
Ex. 4.14. By generalizing instead, we avoid extra steps, and intuitively, we strengthen
an induction statement rather than add a separate lemma. Without constraints, G EN -
ERALIZATION can be seen as a combination of P OSTULATE and the S UBSUMPTION
rule in [Bouhoula 1997]. As there are several results for generalizing equations in the
literature [Bundy et al. 1993; Bundy et al. 2005; Basin and Walsh 1992; Walsh 1996;
Urso and Kounalis 2004], the combination is useful beyond just this paper.
   Example 4.16. In Ex. 4.14, we could have used G ENERALIZATION immedi-
ately to move from the proof state ({ (FCT.J) }, { (FCT.D−1 ) }, INCOMPLETE) to
({ (FCT.M) }, { (FCT.D−1 ) }, INCOMPLETE).
  4.2.6. EQ- DELETION. The following rule, which was adapted from [Sakata et al. 2009],
provides a link between the equation part s ≈ t and the constraint.
   Definition 4.17. Let C be an arbitrary context with n holes (C may contain symbols
in Σtheory ). If all si , ti ∈ Terms(Σtheory , Var (φ)), then we can derive:
                    (E ⊎ {C[s1 , . . . , sn ] ≃ C[t1 , . . . , tn ] [φ]},
                                                                     Vn H, b) ⊢ri
              (E ∪ {C[s1 , . . . , sn ] ≈ C[t1 , . . . , tn ] [φ ∧ ¬( i=1 si = ti )]}, H, b)

                       ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                        A:21
                  Vn
  Intuitively, if i=1 si = ti holds, then C[s1 , . . . , sn ]γ ↔∗Rcalc C[t1 , . . . , tn ]γ, so we are
done. EQ- DELETION excludes this case from the equation. In combination with D ELE -
TION , this rule gives a more general variation of T HEORY ⊤ in [Falke and Kapur 2012].

    Example 4.18. Continuing from Ex. 4.14 (or Ex. 4.16), we observe that n ≥ y,
y ′ = y + 1 and y ′ > n together imply n = y, and with m = n − 1 we thus have y > m as
well. Therefore, S IMPLIFICATION on (FCT.O) by rule (3) followed by (6) gives:
      (FCT.P): return(n ∗ x) ≈ return(x′ ) [n = y ∧ m = n − 1 ∧ y ′ = y + 1 ∧ x′ = x ∗ y]
We can use EQ- DELETION with the context C[2] = return(2) to replace (FCT.P) by:
(FCT.Q): return(n∗x) ≈ return(x′ ) [n = y ∧m = n−1∧y ′ = y +1∧x′ = x∗y ∧¬(n∗x = x′ )]
As n = y and x′ = x ∗ y together imply that n ∗ x = x′ , the constraint of this equa-
tion is not satisfiable. We may remove it using D ELETION, giving the proof state
({ (FCT.N) }, { (FCT.D−1 ), (FCT.M−1 ) }, INCOMPLETE).
  EQ- DELETION is among the core rules for constrained rewriting induction: almost
all inductive proofs use it, in contrast to the remaining three inference rules.
  Example 4.19. To complete our example, consider (FCT.N). As y + 1 = y ′ ≤ n ∧ m =
n − 1 implies y ≤ m, we may apply S IMPLIFICATION with rule (2) to replace it by:
                   (FCT.R): mul(n, iter(m, x ∗ y, y + 1)) ≈ iter(n, x′ ∗ y ′ , y ′ + 1)
                          [n ≥ y ∧ m = n − 1 ∧ y ′ = y + 1 ∧ x′ = x ∗ y ∧ y ′ ≤ n]
Then, using S IMPLIFICATION with calculations (and observing that both x ∗ y and y + 1
are “defined” in the constraint, as discussed in § 4.2.1), we get:
                 (FCT.S):        mul(n, iter(m, x′ , y ′ )) ≈ iter(n, x′′ , y ′′ )
                   [n ≥ y ∧ m = n − 1 ∧ x′ = x ∗ y ∧ x′′ = x′ ∗ y ′ ∧ y ′′ = y ′ + 1]
                          ′

(We removed the clauses with y from the constraint, as y does not occur in the equation
part.) But now the induction rule (FCT.M−1 ) applies! As this rule is irregular, we must
be careful. We use the substitution γ = [n := n, m := m, x′′ := x′ , y ′ := y ′′ , x := x′ , y :=
y ′ ], which also affects variables not occurring in the left-hand side. The substituted
constraint for the rule is n ≥ y ′ ∧ m = n − 1 ∧ y ′′ = y ′ + 1 ∧ x′′ = x′ ∗ y ′ , which is indeed
implied by the constraint of (FCT.S). Using S IMPLIFICATION, we thus obtain:
                      mul(n, iter(m, x′ , y ′ )) ≈ mul(n, iter(m, x′ , y ′ ))
                                                                                              
        (FCT.T):                                                                      {· · · } ,
                                                                                 ,
          [n ≥ y ′ ∧ m = n − 1 ∧ x′ = x ∗ y ∧ x′′ = x′ ∗ y ′ ∧ y ′′ = y ′ + 1]     INCOMPLETE

As the left- and right-hand side of the remaining equation are the same, we may re-
move it using D ELETION. This leaves a proof state of the form (∅, H, INCOMPLETE), so
by Thm. 4.4, the equation factrec(n) ≈ factiter(n) [n ≥ 1] is an inductive theorem.
  4.2.7. C ONSTRUCTOR. Where Falke and Kapur [2012] and Sakata et al. [2009] focus
on systems with only theory symbols and defined symbols, here we are also interested
in non-theory constructors, such as errorf and returnf . To support this, we add:
   Definition 4.20. If f is a constructor, we can derive:
    (E ⊎ {f (s1 , . . . , sn ) ≈ f (t1 , . . . , tn )[φ]}, H, b) ⊢ri (E ∪ {si ≈ ti [φ] | 1 ≤ i ≤ n}, H, b)
  The C ONSTRUCTOR rule originates in [Bouhoula 1997], where it is called P OSITIVE
D ECOMPOSITION, although variations occur in earlier work on implicit induction, e.g.,
[Huet and Hullot 1982]. It is used to split up a large equation into smaller problems.
This inference rule is particularly useful in applications where a recursive structure,
such as a list, is inductively built up, but will also be invaluable as part of a disproof.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:22                                                                          C. Fuhs, C. Kop, N. Nishida

    Example 4.21. Suppose that, in Ex. 4.5, we had started with (BAD.A): factiter(x) ≈
 factrec(x − 1) [true]. Following some expansions and simplifications, we arrive at
                                                                                
           (BAD.B): return(2) ≈ return(1) [x = 2]
                                                                     , H, COMPLETE
           (BAD.C): iter(x, 1, 1) ≈ factrec(y) [y = x − 1 ∧ y > 1]
 (for some H). We can use C ONSTRUCTOR to replace (BAD.B) by (BAD.D): 2 ≈ 1 [x = 2].
  4.2.8. D ISPROVE. Recall that, to show that an equation is not an inductive theorem,
 we must derive ⊥ from a COMPLETE proof state. For this, we use D ISPROVE.
   Definition 4.22. Suppose ⊢ s : ι and one of the following holds:
— s, t ∈ Terms(Σtheory , V), ι is a theory sort, and φ ∧ s ̸= t is satisfiable;
                         →
                         −
— s = f (→−
          s ) and t = g( t ) with f, g distinct constructors and φ satisfiable;
— s ∈ V \ Var (φ), φ is satisfiable, at least two different constructors have output sort ι,
                                                                      →
                                                                      −
  and either t is a variable distinct from s or t has the form g( t ) with g ∈ Cons;
 Then we may derive:
                          (E ⊎ {s ≃ t [φ]}, H, COMPLETE) ⊢ri ⊥
   The first case of this rule corresponds to T HEORY⊤ in [Falke and Kapur 2012] and
 Thm. 7.2 in [Sakata et al. 2009]; note that the restriction to theory sorts only excludes
 the case where s and t are non-logical variables. The second case corresponds to P OS -
 ITIVE C LASH in [Bouhoula 1997]. The third case is new in rewriting induction, but
 appears in [Huet and Hullot 1982], an implicit induction method based on completion.
   Example 4.23. Following Ex. 4.21, we observe that x = 2∧2 ̸= 1 is satisfiable. Thus,
 by D ISPROVE we reduce ({ (BAD.D), (BAD.C) }, H, COMPLETE) to ⊥. By confluence of
 Rfact , we see that factiter(x) and factrec(x − 1) have different normal forms for some x.
   4.2.9. C OMPLETENESS. A downside of P OSTULATE and G ENERALIZATION is the po-
 tential loss of the completeness flag. To weaken this problem—and empower automatic
 tools to combine the search for a proof and a disproof—we add our final inference rule.
   Definition 4.24. For any set of equations E and E ′ ⊆ E we can derive:
                      If (E, H, COMPLETE) ⊢∗ri (E ′ , H′ , INCOMPLETE)
                   then (E, H, COMPLETE) ⊢ri (E ′ , H′ , COMPLETE)
     Essentially, C OMPLETENESS allows us to return the completeness flag that was
 lost due to a P OSTULATE or G ENERALIZATION step, once we have managed to re-
 move all the added / generalized lemma equations. In practice, a tool or human prover
 might have a derivation that could be denoted (E, H, COMPLETE) ⊢ri (P OSTULATE) (E ∪
 E ′ , H, INCOMPLETE) ⊢ri · · · ⊢ri (E, H ∪ H′ , INCOMPLETE) ⊢ri (C OMPLETENESS) (E, H ∪
 H′ , COMPLETE) by remembering the set E where the completeness flag was lost.
   Example 4.25. Recall Ex. 4.14. Starting in ({ (FCT.J) }, { (FCT.D−1 ) }, COMPLETE),
 we lost completeness by adding a lemma equation. Then, after using E XPANSION, we
 arrived at ({ (FCT.J), (FCT.N), (FCT.O) }, { (FCT.D−1 ), (FCT.M−1 ) }, INCOMPLETE).
 Applying the proof steps of Examples 4.18 and 4.19 without touching (FCT.J), we could
 reduce this state to ({ (FCT.J) }, { (FCT.D−1 ), (FCT.M−1 ) }, INCOMPLETE). But the
 only equation (FCT.J) in this set is the one we started with. Thus, we may restore the
 completeness flag, resulting in ({ (FCT.J) }, { (FCT.D−1 ), (FCT.M−1 ) }, COMPLETE).
   There are many other potential inference rules we could consider, as various exten-
 sions of the base method have been studied in the literature (see e.g. [Bouhoula 1997]).
 For now, we stick to these nine rules and leave the remainder to future work.

                      ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                      A:23

4.3. Examples
The running example in § 4.2 gives a good general idea of the power of the method and
the way it is applied. In this section we present some further examples. For brevity, we
only list the equations E in each step, not the completeness flag or induction rules H.
Unless stated otherwise, these induction rules are not applicable to new equations.
    Example 4.26. Let us look at an assignment to implement strlen, a string function
which operates on 0-terminated char arrays. As char is a numeric data type, we use
integer arrays in the LCTRS translation (although another underlying sort Ichar would
make little difference). The example function and its LCTRS translation are as follows:
  int strlen(char *s) {
     for(int i = 0;;i++){ (1) strlen(x) → u(x, 0)
       if(s[i] == 0)           (2) u(x, i) → error          [i < 0 ∨ i ≥ size(x)]
         return i;             (3) u(x, i) → return(i) [0 ≤ i < size(x) ∧ select(x, i) = 0]
     }                         (4) u(x, i) → u(x, i + 1) [0 ≤ i < size(x) ∧ select(x, i) ̸= 0]
  }
Note that the bounds checks guarantee termination. To see that strlen does what we
would expect it to do, we want to know that for valid C strings, strlen(a) returns the
first integer i such that a[i] = 0. Following § 1.2.4, this corresponds to the equation:
      (LEN.A)                                strlen(x) ≈ return(n)
                   [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ select(x, n) = 0]
Here, we use bounded quantification, which, as described in § 2.2, can be seen as syn-
tactic sugar for an additional predicate; the underlying LCTRS could, e.g., use a symbol
nonzero and replace ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) by nonzero(x, n) in the constraint.
  We first use S IMPLIFICATION with rule (1), which gives (LEN.B):
u(x, 0) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ select(x, n) = 0]
We continue with E XPANSION, again on the left-hand side. Since the constraint implies
that 0 < size(x), the error case (2) is unsatisfiable, so we delete it, which leaves:
(LEN.C) return(0) ≈ return(n)   [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
                                      select(x, n) = 0 ∧ 0 ≤ 0 < size(x) ∧ select(x, 0) = 0]
(LEN.D) u(x, 0 + 1) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
                                      select(x, n) = 0 ∧ 0 ≤ 0 < size(x) ∧ select(x, 0) ̸= 0]
  As the constraint of (LEN.C) implies that n = 0, we can remove (LEN.C) using EQ-
DELETION and D ELETION . (LEN.D) is simplified with a calculation:
   (LEN.E) u(x, 1) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
                                         select(x, n) = 0 ∧ 0 < size(x) ∧ select(x, 0) ̸= 0]
Which we expand again (once more skipping the error case due to unsatisfiability):
 (LEN.F) return(1) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
       select(x, n) = 0 ∧ 0 < size(x) ∧ select(x, 0) ̸= 0 ∧ 0 ≤ 1 < size(x) ∧ select(x, 1) = 0]
 (LEN.G) u(x, 1 + 1) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
       select(x, n) = 0 ∧ 0 < size(x) ∧ select(x, 0) ̸= 0 ∧ 0 ≤ 1 < size(x) ∧ select(x, 1) ̸= 0]
The constraint of (LEN.F) implies that n = 1, so we easily remove this equation.
(LEN.G) is simplified using a calculation and then expanded again:
 (LEN.H) return(2) ≈ return(n) [· · · ∧ 2 < size(x) ∧ select(x, 2) = 0]
  (LEN.I) u(x, 2 + 1) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0)
                                   ∧ select(x, n) = 0 ∧ 0 < size(x) ∧ select(x, 0) ̸= 0 ∧ 1 <
                                  size(x) ∧ select(x, 1) ̸= 0 ∧ 2 < size(x) ∧ select(x, 2) ̸= 0]

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:24                                                                             C. Fuhs, C. Kop, N. Nishida

We drop (LEN.H) easily. Simplifying (LEN.I) and reformulating its constraint gives:
 (LEN.J) u(x, 3) ≈ return(n) [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
                    select(x, n) = 0 ∧ 0 ≤ 2 < size(x) ∧ ∀j ∈ {0, . . . , 2}(select(x, j) ̸= 0)]
Note that we grouped together the ̸= 0 statements into a quantification, which looks a
lot like the other quantification in the constraint. Now, let us generalize! We will use
the generalized equation (LEN.K): u(x, k) ≈ return(n) [φ], where:
          φ : k = m + 1 ∧ 0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧
              select(x, n) = 0 ∧ 0 ≤ m < size(x) ∧ ∀j ∈ {0, . . . , m}(select(x, j) ̸= 0)
Obviously, (LEN.J) is an instance of (LEN.K); we use E XPANSION to obtain:
          (LEN.L) error ≈ return(n)       [φ ∧ (k < 0 ∨ k ≥ size(x))]
          (LEN.M) return(k) ≈ return(n) [φ ∧ 0 ≤ k < size(x) ∧ select(x, k) = 0]
          (LEN.N) u(x, k + 1) ≈ return(n) [φ ∧ 0 ≤ k < size(x) ∧ select(x, k) ̸= 0]
The two ∀ statements in φ, together with select(x, n) = 0, imply that m < n, so k ≤
n. Consequently, (LEN.L) has an unsatisfiable constraint and may be deleted: k < 0
cannot hold because k = m + 1 and 0 ≤ m, nor k ≥ size(x) because k ≤ n and n < size(x).
  For (LEN.M), the two ∀ statements together with select(x, k) = 0 imply that n−1 < k,
so n ≤ k. Thus, n = k. EQ- DELETION gives an equation with an unsatisfiable con-
straint, which we remove using D ELETION. As for (LEN.N), we use S IMPLIFICATION
with a calculation and reformulate the constraint to obtain:
      (LEN.O) u(x, p) ≈ return(n) [p = k + 1 ∧ select(x, n) = 0 ∧ 0 ≤ n < size(x) ∧
                           ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ 0 ≤ k < size(x) ∧
                         ∀j ∈ {0, . . . , k}(select(x, j) ̸= 0) ∧ some constraints on m]
This equation is simplified to an equation of the form return(n) ≈ return(n) [. . .] using
the induction rule obtained from (LEN.K); we complete with D ELETION.
   Example 4.27. We consider Rsum , the LCTRS with the two correct implementations
of the motivating Ex. 1.1; that is, rules (1a)–(1d) and (4a)–(4e). The rules are termi-
nating because in the recursive rule (1c), n − i decreases in every step and is bounded
from below by 0, and in rule (4c), the value k decreases against the bound 0.
  To prove equivalence of these implementations when the given length is within the
array bounds, we must show that (ARR.A) is an inductive theorem:
                      (ARR.A) sum1(a, k) ≈ sum4(a, k) [0 ≤ k ≤ size(a)]
The derivation follows a similar pattern as with factorial: we first simplify the left
hand using rule (1a), then expand on the right and use the induction rule, sum4(a, k) →
u(a, k, 0, 0) [0 ≤ k ≤ size(a)], to eliminate the remaining occurrence of sum4. This gives:
                                 w(n, u(a, k ′ , 0, 0)) ≈ u(a, k, r, 1)
            [k ′ = k − 1 ∧ 0 ≤ k ′ < size(a) ∧ n = select(a, k ′ ) ∧ r = 0 + select(a, 0)]
Continuing to expand and simplify, we easily remove the equations resulting from
rules (1b) and (1d) in every step, but the recursive rule (1c) causes a divergence.
u(a, k, r2 , 3) ≈ w(n, u(a, k ′ , r1 , 2)) [k ′ = k − 1 ∧ 2 < k ≤ size(a) ∧ r2 = r1 + select(a, 1) ∧ . . .]
u(a, k, r3 , 4) ≈ w(n, u(a, k ′ , r2 , 3)) [k ′ = k − 1 ∧ 3 < k ≤ size(a) ∧ r3 = r2 + select(a, 2) ∧ . . .]
u(a, k, r4 , 5) ≈ w(n, u(a, k ′ , r3 , 4)) [k ′ = k − 1 ∧ 4 < k ≤ size(a) ∧ r4 = r3 + select(a, 3) ∧ . . .]
We can easily complete after generalizing any of these equations to:
    (ARR.GEN): u(a, k, r, i) ≈ w(n, u(a, k ′ , r′ , i′ )) [k ′ = k − 1 ∧ 0 ≤ i′ < k ≤ size(a) ∧
                                    i′ = i − 1 ∧ r = r′ + select(a, i′ ) ∧ n = select(a, k ′ )]

                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                      A:25

   Example 4.28. Recall strcpy from Ex. 3.7 and the analysis rules and equation from
Ex. 1.2. The inductive proof follows roughly the same lines as the one for strlen and is
found automatically by our tool (see § 6). We reach a divergence in equations such as:
    •       test(x, n, v(a, x, 1)) ≈ true [0 ≤ n < size(x) ∧ n < size(a) ∧ select(x, n) = 0 ∧
        ∀i ∈ {0, . . . , n − 1}(select(x, i) = 0) ∧ select(x, 0) ̸= 0 ∧ select(x, 0) = select(a, 0)]
    •        test(x, n, v(b, x, 2)) ≈ true [0 ≤ n < size(x) ∧ n < size(b) ∧ select(x, n) = 0 ∧
      ∀i ∈ {0, . . . , n − 1}(select(x, i) = 0) ∧ select(x, 0) ̸= 0 ∧ select(x, 0) = select(b, 0) ∧
                                                     select(x, 1) ̸= 0 ∧ select(b, 1) = select(x, 1)]
    •          test(x, n, v(c, x, 3)) ≈ true [· · · ∧ select(c, 2) ̸= 0 ∧ select(c, 2) = select(x, 2)]
To generalize, we abstract 1, 2, 3 by k ≥ 0, collect similar statements into quantifica-
tions and remove the endpoint. We quickly complete after this G ENERALIZATION to:
    test(x, n, v(c, x, k)) ≈ true [0 ≤ n < size(x) ∧ n < size(c) ∧ select(x, n) = 0 ∧ 0 ≤ k ∧
             ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ ∀i ∈ {0, . . . , k − 1}(select(x, i) ̸= 0) ∧
                                                   ∀i ∈ {0, . . . , k − 1}(select(c, i) = select(x, i))]
   Example 4.29. Let us compare two implementations of the Fibonacci function:
            (1)                   fibrec(x) → 0                                  [x ≤ 0]
            (2)                   fibrec(1) → 1
            (3)                   fibrec(x) → plus(fibrec(x − 1), fibrec(x − 2)) [x ≥ 2]
            (4) plus(return(x), return(y)) → return(x + y)
            (5)                  fibiter(x) → iter(x, 1, 0, 1)
            (6)             iter(x, i, y, z) → iter(x, i + 1, z, y + z)          [x ≥ i]
            (7)             iter(x, i, y, z) → return(y)                         [x < i]
Starting with the equation fibrec(x) ≈ fibiter(x) [true] eventually results in a divergence:
iter(n, 3, 1, 2) ≈ plus(iter(m, iter(m, 2, 1, 1)), iter(k, iter(k, 1, 0, 1))) [m = n − 1 ∧ k = n − 2]
iter(n, 4, 2, 3) ≈ plus(iter(m, iter(m, 3, 1, 2)), iter(k, iter(k, 2, 1, 1))) [m = n − 1 ∧ k = n − 2]
iter(n, 5, 3, 5) ≈ plus(iter(m, iter(m, 4, 2, 3)), iter(k, iter(k, 3, 1, 2))) [m = n − 1 ∧ k = n − 2]
The proof is easily finished by using the following generalization:
                iter(n3 , i3 , z3 , z4 ) ≈ plus(iter(n2 , i2 , z2 , z3 ), iter(n1 , i1 , z1 , z2 ))
    [n2 = n3 − 1 ∧ n1 = n2 − 2 ∧ i3 = i2 + 1 ∧ i2 = i1 + 1 ∧ z3 = z1 + z2 ∧ z4 = z2 + z3 ]
Thus, we can show equivalence of functions with wildly different time complexities
(fibrec’s running time is exponential in the input value, whereas that of fibiter is linear).
   Example 4.30. Finally, we consider an example which Godlin and Strichman [2008,
§ 6, item 2] P
             describe as beyond their method. Here two recursive imperative programs
               n
calculating i=1 i are compared. The methods from § 3 yield the following LCTRS.
(1)             f(n) → return(n)    [n ≤ 0] (4)            g(n) → return(n)    [n ≤ 1]
(2)             f(n) → u(n, f(n−1)) [n > 0] (5)            g(n) → v(n, g(n−1)) [n > 1]
(3) u(n, return(m)) → return(n+m)           (6) v(n, return(m)) → return(n+m)
Starting with the equation f(x) ≈ g(x) [true] eventually results in a divergence:
(CR.A):                         u(x, u(y1 , g(y2 ))) ≈ v(x, u(z1 , g(z2 )))
                   [x > 1 ∧ y1 = x − 1 ∧ z1 = x − 1 ∧ y2 = y1 − 1 ∧ z2 = z1 − 1]
(CR.B):                  u(x, u(y1 , u(y2 , g(y3 )))) ≈ v(x, u(z1 , u(z2 , g(z3 ))))
  [x > 1 ∧ y1 = x − 1 ∧ z1 = x − 1 ∧ y2 = y1 − 1 ∧ z2 = z1 − 1 ∧ y3 = y2 − 1 ∧ z3 = z2 − 1]
(CR.C):           u(x, u(y1 , u(y2 , u(y3 , g(y4 ))))) ≈ v(x, u(z1 , u(z2 , u(z3 , g(z4 ))))) [. . . ]
As the constraints imply that each yi = zi , these equations can all be generalized to
u(x, u(y, z)) ≈ v(x, u(y, z)) [x > 1]. Again, the proof is quickly completed.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:26                                                                            C. Fuhs, C. Kop, N. Nishida

4.4. Soundness and Completeness of Rewriting Induction
We now give an intuition on how to prove Thm. 4.4. The complete proof can be found
in Appendix B. We follow the proof method of [Sakata et al. 2009], which builds on the
original proof idea in [Reddy 1990]. This uses the relation ↔E , defined by
           C[sγ]p ↔E C[tγ]p if s ≈ t [φ] ∈ E or t ≈ s [φ] ∈ E, and γ respects φ
for E a set of equations. The proof is split up into several auxiliary lemmas. To start:
  L EMMA 4.31. All equations in E are inductive theorems if and only if ↔E ⊆ ↔∗R on
ground terms (so if s, t are ground and s ↔E t, then also s ↔∗R t).
  This is obvious from the definitions. The next lemma originates in [Sakata et al.
2009], which is adapted from [Koike and Toyama 2000] and is key to our method.
   L EMMA 4.32 ([S AKATA ET AL . 2009]). Let →1 and →2 be binary relations. We have
↔∗1 = ↔∗2 if (a) →1 ⊆ →2 , (b) →2 is well founded, and (c) →2 ⊆ (→1 · →∗2 · ↔∗1 · ←∗2 ).
   P ROOF. It follows from →1 ⊆ →2 that ↔∗1 ⊆ ↔∗2 . To show that ↔∗2 ⊆ ↔∗1 , we prove →∗2
⊆ ↔∗1 by well-founded induction on →2 . Since the base case s →∗2 s is clear, we suppose
s →2 t →∗2 u. As →2 ⊆ (→1 · →∗2 · ↔∗1 · ←∗2 ) there must be some a, b, c such that s →1 a
→∗2 b ↔∗1 c ←∗2 t. Since →1 ⊆ →2 (i.e., s →2 a), we can apply the induction hypothesis
both on a and on t, so a ↔∗1 b ↔∗1 c ↔∗1 t and t ↔∗1 u. Therefore, s ↔∗1 u.
  We will use Lemma 4.32 with →R for →1 , and →R∪H for →2 . Soundness of the
algorithm then follows if ↔E is included in ↔∗H whenever (E, ∅, flag) ⊢∗ri (∅, H, flag ′ ).
  Thm. 4.4 is the combination of Lemma 4.31 with Lemmas 4.33 and 4.34 below.
   L EMMA 4.33. If (E, ∅, flag) ⊢∗ri (∅, H, flag ′ ), then ↔E ⊆ ↔R holds on ground terms.
   P ROOF IDEA . Let ←→  ∥ E denote a parallel application of zero or more ↔E steps. We
first show that (E, H, flag) ⊢ri (E ′ , H′ , flag ′ ) by any rule other than C OMPLETENESS
implies both (a) ←→ ∥ E ⊆ (→∗R∪H′ · ←→   ∥ E ′ · ←∗R∪H′ ) on ground terms, and (b) if →R∪H
            ∗
⊆ (→R · →R∪H · ←→   ∥ E · ←R∪H ) on ground terms, then →R∪H′ ⊆ (→R · →∗R∪H′ · ←→
                            ∗
                                                                                             ∥ E′
· ←∗R∪H′ ) on ground terms. We show this by considering how each step alters E and
H, which we use to see that (E, H, flag) ⊢∗ri (E ′ , H′ , flag ′ ) implies (a) and (b), by induc-
tion on the total number of ⊢ri -steps in the derivation (counting also the hidden steps
inside C OMPLETENESS). Thus, if (E, ∅, flag) ⊢∗ri (∅, H, flag ′ ) then →R∪H ⊆ →R · →∗R∪H
· ←∗R∪H , so we can apply Lemma 4.32 to conclude that →R and →R∪H are the same (on
ground terms). Therefore, and by property (a), ↔E ⊆ ←→        ∥ E ⊆ →∗R∪H · ←∗R∪H ⊆ ↔∗R .
  L EMMA 4.34. If R is confluent and (E, ∅, COMPLETE) ⊢∗ri ⊥, then ↔E ̸⊆ ↔R holds
on ground terms.
   P ROOF IDEA . By confluence and termination together, we can speak of the normal
form u ↓R of any term u; if u is ground, then by quasi-reductivity its normal form is
a ground constructor term. A property of confluence is that if w ↔∗R q, then w ↓R =
q ↓R . So, it suffices to prove that for some s ≈ t [φ] ∈ E there is a ground constructor
substitution γ which respects this equation, such that sγ ̸= tγ. We first note that if
(E, H, COMPLETE) ⊢ri ⊥, then this can only be a D ISPROVE step; in all cases the
equation that causes the disproof has this property. We also see, by examining the
various inference rules, that if (E1 , H1 , COMPLETE) ⊢ri (E2 , H2 , COMPLETE) and both
(a) →R∪H1 ⊆ →R · →∗R∪H1 · ←→               ∥ E · ←∗R∪H1 and (b) ↔E1 ∪ ↔H1 ⊆ ↔∗R on ground
                                          ∗
terms, then also ↔E2 ∪ ↔H2 ⊆ ↔R on ground terms. In a reduction (E, ∅, COMPLETE) =
(E1 , H1 , flag 1 ) ⊢ri · · · ⊢ri (En , Hn , flag n ) ⊢ri ⊥, we may assume (a) by the observations
in the proof of Lemma 4.33, and (b) is inductively preserved. As ↔En ∪Hn cannot be
included in ↔∗R , therefore neither can ↔E = ↔E1 ∪H1 . We complete by Lemma 4.31.

                       ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                 A:27

5. GENERALIZING EQUATIONS
Divergence, as encountered in all examples in § 4, is very common in inductive theorem
proving: we often need a more general claim to obtain a stronger induction hypothesis.
As it is not always easy to find a suitable generalization, the (automatic) generation of
suitable generalizations, and lemma equations for P OSTULATE, has been extensively
investigated [Bundy et al. 2005; Kapur and Sakhanenko 2003; Kapur and Subrama-
niam 1996; Nakabayashi et al. 2010; Urso and Kounalis 2004; Walsh 1996].
  Also for transformed procedural programs, we will certainly need a large variety of
lemma generation techniques to handle most practical cases. We start the work by
proposing two methods to generalize equations, specialized to deal with constraints.
5.1. Generalizing Initializations
Our first and most important technique fundamentally relies on the constrained set-
ting. Although it may appear deceptively simple (at its core, the generalization just
drops a part of the constraint), it is particularly effective for dealing with loops.
   Example 5.1. Let us state the rules of Rfact from Ex. 4.2 in an alternative way:
we replace rule (1) factiter(x) → iterm(x, 1, 1) by (1′ ): factiter(x) → iter(x, v1 , v2 ) [v1 =
1 ∧ v2 = 1]. That is, the values corresponding to initializations int z = 1; int i = 1;
are moved into the constraint. Evidently, this change does not alter the relation →R .
  Now consider what happens if we use the same steps as in Ex. 4.2–4.14. The result-
ing proof has the same shape, but with more complex equations. Some instances:
(FCT.B′ ) : iter(n, v1 , v2 ) ≈ factrec(n) [n ≥ 1 ∧ v1 = 1 ∧ v2 = 1]
(FCT.D′ ) : iter(n, z1 , i1 ) ≈ factrec(n) [n ≥ 1 ∧ v1 = 1 ∧ v2 = 1 ∧ z1 = v1 ∗ v2 ∧ i1 = v2 + 1]
(FCT.J′ ) : mul(n, iter(m, z1 , i1 )) ≈ iter(n, z2 , i2 ) [n > 1 ∧ v1 = 1 ∧ v2 = 1 ∧ m = n − 1 ∧
                                           z1 = v1 ∗ v2 ∧ i1 = v2 + 1 ∧ z2 = z1 ∗ i1 ∧ i2 = i1 + 1]
(FCT.K′ ) : mul(n, iter(m, z2 , i2 )) ≈ iter(n, z3 , i3 ) [n > 1 ∧ v1 = 1 ∧ v2 = 1 ∧ m = n − 1 ∧
           z1 = v1 ∗ v2 ∧ i1 = v2 + 1 ∧ z2 = z1 ∗ i1 ∧ i2 = i1 + 1 ∧ z3 = z2 ∗ i2 ∧ i3 = i2 + 1]
Here the left- and right-hand side of the divergent equations (FCT.J′ ) and (FCT.K′ ) are
the same modulo variable renaming, while the constraint grows. Essentially, we keep
track of parts of the history of an equation in its constraint. We generalize (FCT.J′ ) by
dropping all clauses vi = qi where vi is an initialization variable and qi a value. We
rename the variables vi (as they no longer play a special role) and obtain:
  (FCT.M′ ) :                        mul(n, iter(m, z1 , i1 )) ≈ iter(n, z2 , i2 )
                  [n > 1 ∧ m = n − 1 ∧ z1 = x1 ∗ x2 ∧ i1 = x2 + 1 ∧ z2 = z1 ∗ i1 ∧ i2 = i1 + 1]
We can complete the derivation with (FCT.M′ ) as we did with (FCT.M) before.
  Formally, what we do here is threefold. First, we alter the set of rules we work from.
  Definition 5.2 (Initialization-free Rules). Given R, fix a set Vinit ⊊ V of variables
not occurring in R. The initialization-free counterpart R′ of R is obtained by stepwise
replacing any rule ℓ → C[f (r1 , . . . , ri , . . . , rn )] [φ] with f ∈ D and ri a value by ℓ →
C[f (r1 , . . . , v, . . . , rn )] [φ ∧ v = ri ] for some fresh v ∈ Vinit , until no such rules remain.
  Then, to apply G ENERALIZATION to an equation s ≈ t [φ1 ∧ · · · ∧ φn ] we choose
        ^
 s ≈ t [ {φi | 1 ≤ i ≤ n ∧ φi does not have the form v = u with v ∈ Vinit and u ∈ Val}]
as the generalized equation and rename its variables in Vinit to variables in V.
  Finally, we restrict the S IMPLIFICATION and E XPANSION steps to preserve initial-
ization constraints throughout the proof. The strategy we use in Ctrl—which includes
an approach to handle the v ∈ Vinit —is described in § 6.1, but in particular:

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:28                                                                                C. Fuhs, C. Kop, N. Nishida

— When we rename rules for use in S IMPLIFICATION or E XPANSION, the renaming
  must respect membership in Vinit , i.e., if x is renamed to y, then y ∈ Vinit iff x ∈ Vinit .
— In ∼-steps, any conjuncts v = n are ignored: to simplify s ≈ t [φ∧v1 = n1 ∧· · ·∧vk = nk ],
  we modify s ≈ t [φ], obtaining s′ ≈ t′ [φ′ ], and continue with s′ ≈ t′ [φ ∧ v1 = n1 ∧ · · · ∧
  vk = nk ]. Thus we avoid, e.g., translating f (vi ) [vi = 0] back to f (0) [true].
 5.2. Abstracting Equivalent Recursive Calls
 Our second generalization technique aims to remove recursive symbols where possible.
                                                                      →
                                                                      −
   Definition 5.3. For symbols f, g, let f ; g if there is a rule f ( ℓ ) → r [φ] with g a
 symbol in r. A symbol f is recursive if it is a defined symbol with f ;+ f .
   The key idea is to identify equivalent occurrences of a recursive call on both sides of
 an equation and to replace them by a variable. For example, g(x)+f(y) ≈ f(z)+g(x) [y ≥
 z ∧ y ≤ z] is replaced by a + b ≈ b + a [true] because for values k, n, m: if n ≥ m ∧ m ≤ n
 holds, then both g(k) and g(k), as well as f(n) and f(m), are syntactically equal.
    Definition 5.4. A recursion-abstraction of s ≈ t [φ] is any equation of the form
 C[x1 , . . . , xn ] ≈ D[xi1 , . . . , xin ] such that (a) s = C[s1 , . . . , sn ] and t = D[ti1 , . . . , tin ] for
 some ⃗s, ⃗t; (b) {ij | 1 ≤ j ≤ n} = {1, . . . , n}; (c) neither C nor D contain recursive symbols;
 (d) each sj and tj has a recursive symbol as root symbol; (e) for 1 ≤ i ≤ n and all ground
 substitutions γ which respect s ≈ t [φ]: si γ = ti γ; (f) x1 , . . . , xn are fresh w.r.t. s, t.
   For a given equation, at most one choice of C, D is possible, and there are only finitely
 many permutations i1 , . . . , in . Requirement (e) can be checked by confirming that an
 equation sj ≈ tj [φ] is removed by the combination of EQ- DELETION and D ELETION.
    Example 5.5. In Ex. 4.30, we find an abstraction for (CR.A) by choosing C =
 u(x, u(y1 , 2)), D = v(x, u(z1 , 2)), s1 = g(y2 ) and t1 = g(z2 ). Requirement (e) holds:
 if we write φ for the constraint of (CR.A), EQ- DELETION on g(y2 ) ≈ g(z2 ) [φ] pro-
 duces the unsatisfiable constraint φ ∧ y2 ̸= z2 . Thus, we generalize the equation to
 u(x, u(y1 , a)) ≈ v(x, u(z1 , a)) [φ], which is ∼-equivalent to the equation used in Ex. 4.30.
    Example 5.6. Given g(x) + f(y) ≈ f(z) + g(x) [y ≥ z ∧ y ≤ z], let C and D be 2 + 2,
 s1 = g(x), s2 = f(y), t1 = g(x), t2 = f(z), i1 = 2 and i2 = 1. We must see that for all γ
 which respect y ≥ z ∧ y ≤ z: g(x)γ = g(x)γ and f(y)γ = f(z)γ. Both are easily confirmed,
 so we generalize to x1 + x2 ≈ x2 + x1 [y ≥ z ∧ y ≤ z] ∼ a + b ≈ b + a [true] as suggested.
   One can see this generalization heuristic as an instance of the inference rule S PE -
 CIALIZATION by Aubin [1979] for unconstrained explicit induction; restricted to recur-
 sive function calls and combined with S UBSTITUTIVITY OF E QUALITY from the same
 paper. Here we lift equality from syntactic level to semantic level in SMT-theories.
 5.3. Discussion
 The first method to generalize equations is strong (§ 5.1), but only for equations of a
 specific form: we can only use the method if the equation part of the divergence has
 the same shape every time. This is the case for fact, because the rule that causes the
 divergence has the form iter(x1 , . . . , xn ) → iter(r1 , . . . , rn ) [φ], preserving its outer shape.
   In general, the method is most likely to be successful for the analysis of tail-recursive
 functions (with accumulators), such as those obtained from procedural programs. We
 can also handle mutually recursive functions, like u(x1 , . . . , xn ) → w(r1 , . . . , rm ) [φ] and
 w(y1 , . . . , ym ) → u(q1 , . . . , qn ) [ψ]. It is not suitable for analyzing systems with (only)
 non-tail-recursion, however. Here, the second technique comes in (§ 5.2). Although we
 do not claim that this technique is very powerful, it is often useful to eliminate appar-
 ently simple equations. It is also straightforward to use in practice.

                            ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:29

   Note that strlen and strcpy also have the required tail-recursive form to successfully
use the first generalization method. However, here we additionally have to collect mul-
tiple clauses into a quantification before generalizing, as with equation (LEN.I).
   One may wonder if generalizing initializations loses too much; e.g., when removing
vi = 1, we also forget that vi ≥ 0. However, this is usually not an issue: if a rule
is constrained with vi ≥ 0, this clause is added to the constraint of the equation via
E XPANSION before we generalize, as in the expansion from (LEN.B). There is a possible
issue with losing information on the relations between variables; more on this in § 6.2.
6. IMPLEMENTATION
The method for program verification in this paper can be broken down into two parts:
(1) transforming a procedural program into an LCTRS;
(2) proving correctness properties on this LCTRS using rewriting induction.
An initial implementation of part 1, limited to functions on integers and one-
dimensional statically allocated integer arrays is available at:
                              http://www.trs.css.i.nagoya-u.ac.jp/c2lctrs/
In future work, we hope to extend this implementation to include the remaining fea-
tures discussed in § 3 and Appendix A.2 such as floating points and explicit pointers.
  Part 2, the core method on LCTRSs, has been implemented in our tool Ctrl [Kop
and Nishida 2015], along with basic techniques to verify termination, confluence and
quasi-reductivity. To handle constraints, the tool is coupled both with a small internal
reasoner and the external SMT solver Z3 [de Moura and Bjørner 2008]. Z3 is equipped
to prove unsatisfiability as well as satisfiability, which is essential for testing validity.
  The internal reasoner serves to detect satisfiability or validity of simple statements
quickly, without a call to an SMT solver, and to preprocess certain kinds of queries
which arise often (e.g., for termination proving by polynomial interpretations, we pre-
process queries with ∃∀-quantifier prefix to ∃-queries). The reasoner is also used to sim-
plify the constraints of equations, by for instance combining statements into quantifi-
cations (which is an essential part of the derivations for functions like strlen or strcpy).
  We also translate our array formulas into the SMT-LIB array format as discussed in
§ 3.6, encoding an array as a function from Z to Z with a second variable for its size.
  The latest version of Ctrl (tool paper: [Kop and Nishida 2015]) can be downloaded at:
                             http://cl-informatik.uibk.ac.at/software/ctrl/
6.1. Strategy
Let us discuss the various choices made during a derivation with rewriting induction.
   6.1.1. What inference rule to apply. Ctrl always selects the first rule (combination) from:
(1) EQ- DELETION (if applicable) immediately followed by D ELETION;
(2) D ISPROVE, but without the limitation to COMPLETE proof states;
(3) C ONSTRUCTOR;
(4) S IMPLIFICATION;
(5) a limited form of E XPANSION;
(6) G ENERALIZATION using a recursion-abstraction;
(7) G ENERALIZATION of all initialization variables vi ∈ Vinit at once;
(8) the full form of E XPANSION.
  6.1.2. Generalization and backtracking. Core to the rewriting induction process is a back-
tracking mechanism. Every proof state (E, H) keeps track of all ancestor states on

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:30                                                                             C. Fuhs, C. Kop, N. Nishida

which G ENERALIZATION was applied; a state is COMPLETE if it has no such ances-
tors. The completeness restriction on D ISPROVE is dropped; however, when D ISPROVE
succeeds on an incomplete state, the prover does not conclude failure, but instead back-
tracks to the most recent ancestor and continues without (immediately) generalizing.
Typically, if a G ENERALIZATION is attempted too soon in the proof and results in an
unsound equation, this can be derived very quickly, which allows Ctrl to conclude fail-
ure of the G ENERALIZATION step and to move on to the remaining expansions.
   Example 6.1. Following Ex. 4.26 (but altered with initialization-free rules), our
strategy moves from ({(LEN.A′ )}, ∅) to ({(LEN.B′ )}, ∅) as before. But here, “restricted
expansion” does not apply (as we will see in Ex. 6.3), nor is there a recursion-
abstraction. So we generalize the initializations, obtaining:
                                                                                               
     (BGEN)                              u(x, r0 ) ≈ return(n)
                                                                                              , ∅
          [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ select(x, n) = 0]
We store ({(LEN.B′ )}, ∅) as an ancestor state of ({(BGEN)}, ∅). The only option now is
E XPANSION. Expanding in the left-hand side gives three equations, including:
                                   return(r0 ) ≈ return(n)
          [0 ≤ n < size(x) ∧ ∀i ∈ {0, . . . , n − 1}(select(x, i) ̸= 0) ∧ select(x, n) = 0]
C ONSTRUCTOR gives r0 ≈ n [φ], where φ is satisfied by, e.g., [r0 := 0, n := 1, x := [1, 0]];
by D ISPROVE, we obtain ⊥. However, the state is incomplete as it has an ancestor
stored. Thus, we backtrack to ({(LEN.B′ )}, ∅), and continue with full expansion.
   The C OMPLETENESS rule is implemented via the same mechanism: if (E, H) has a
most recent ancestor (E ′ , H′ ) with E ⊆ E ′ , then (E ′ , H′ ) is dropped from the ancestor
list. If a D ISPROVE succeeds when the list is empty, we conclude failure, resulting in
NO if the system is confluent and MAYBE otherwise.
   Example 6.2. In Ex. 4.16, we would add ({(FCT.J)}, {(FCT.D−1 )}) to the list of an-
cestors when generalizing (FCT.J) to (FCT.M). Once (FCT.T) is removed in Ex. 4.19, we
are allowed to remove this state from the list (although since the proof is finished at
that point, it is not really necessary in this example).
  Aside from backtracking due to D ISPROVE, there is a second backtracking mecha-
nism: although S IMPLIFICATION and E XPANSION prioritize choices (for positions and
rules) most likely to result in success, sometimes the first choice does not work out, but
the second one does. Thus, Ctrl uses an evaluation limit: when a path has more than N
expansions, it is aborted, and the prover backtracks to a direct parent. Ctrl starts with
N = 2 and increases this limit if it does not result in a successful proof or disproof.
   6.1.3. Simplification. For S IMPLIFICATION, there are three choices to be made: the po-
sition, the rule and how to instantiate fresh variables in that rule.
   For the position, Ctrl selects the leftmost, innermost position where a rule matches.
This prevents a need to reevaluate a term after its subterms change.
   For the rule, rules in H are attempted before rules in R; if a rule leads to a (pre-
sumed) divergence, the backtracking mechanism ensures that the next one is tried.
   In some cases—in particular for induction rules—the right-hand side and perhaps
the constraint of a rule contain variables not occurring in the left-hand side, such as
(FCT.M−1 ) in Ex. 4.14 and (LEN.K) in Ex. 4.26. Here, Ctrl tries to instantiate as many
variables in the rule by variables in the equation as possible. To rewrite an equation
s ≈ t [φ1 ∧ · · · ∧ φn ] at the root of s with a rule ℓ → r [ψ1 ∧ · · · ∧ ψm ], we first determine a
γ such that s = ℓγ and γ(vi ) = vi for all vi ∈ Vinit . If any ψi has the form C[x, y1 , . . . , yk ]
with x ∈ Dom(γ) and all yi ∈      / Dom(γ), and there is some φj = Cγ[γ(x), s1 , . . . , sk ], then

                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                        A:31

we extend γ with [yi := si ] for all i. This process is finite and corresponds to the choices
for the equations (FCT.S) and (LEN.O). Other variables are chosen fresh.
  Note: if some rule can be applied, but the backtracking mechanism aborts all at-
tempts, Ctrl backtracks to the parent state rather than continuing with E XPANSION.
This is because testing suggests that allowing E XPANSION to be applied on terms not
in R-normal form is generally not effective and causes an explosive number of states.
   6.1.4. Expansion. To categorize E XPANSIONs for step (5) and (8) of § 6.1.1, we ana-
lyze recursion. Let f ≿ g if f ;∗ g (following Def. 5.3), and let f ≻ g if f ≿ g and
g ̸≿ f . Symbols are split into five categories: constructors, calculation symbols, non-
recursive defined symbols, tail-recursive symbols, and non-tail-recursive symbols. A re-
cursive symbol is tail-recursive if its only defining rules (in R) have either the form
f (ℓ1 , . . . , ℓk ) → x [φ] with x a variable, or the form f (ℓ1 , . . . , ℓk ) → g(r1 , . . . , rm ) [φ] with
f ≻ h for all h in any ri . Recursive functions not of this form are non-tail-recursive.
   An expansion of s ≃ t [φ] at position p of s, with s|p = f (⃗u), is restricted—so eligible for
step (5)—if (a) f is non-recursive, or (b) the induction rule s → t [φ] is admissible and
either f is tail-recursive and (Var (s)∪Var (t))∩Vinit = ∅, or f is non-tail-recursive. The
induction rule is added only in case (b). Here, a rule ρ : g(ℓ1 , . . . , ℓk ) → r [φ] is admissible
if R ∪ H ∪ {ρ} is terminating and g ∈ D: we do not add rules with a constructor or
calculation symbol as root symbol g, as this makes it harder to prove termination,
which may prevent the addition of more promising rules later on.
   For unrestricted expansion, an induction rule is added when admissible, unless f
is tail-recursive. The unrestricted tail-recursive case concerns rules such as those got
from (FCT.J), (LEN.B), and (LEN.E), which—testing suggests—are typically not use-
ful. Omitting them lets Ctrl skip many termination checks, a bottleneck in the process.
Similarly, we do not add induction rules when expanding at a non-recursive position.
   Example 6.3. In Examples 4.2–4.18, the first expansion occurs in ({(FCT.D′ )}, ∅,
COMPLETE ), in the right-hand side. This is not an arbitrary choice: restricted expan-
sion cannot be used with the tail-recursive symbol iter, only the non-tail-recursive sym-
bol factrec. Then, our strategy closely follows the given derivation. When we reach
({(FCT.J)}, {(FCT.D−1 )}, COMPLETE), restricted expansion is impossible, so we gener-
alize instead. After this, an expansion on the iter symbol on either side is restricted.
We can complete the example without backtracking or using unrestricted E XPANSION.
   For the position to expand at, we follow the same approach as for S IMPLIFICATION,
trying all suitable positions via the backtracking mechanism. However, rather than a
pure leftmost innermost choice, in the restricted case (step (5) of § 6.1.1), we prioritize
the more promising equations by first attempting expansions on a non-tail-recursive
symbol, then those with a non-recursive defined symbol, and finally those with a tail-
recursive one. In the unrestricted setting, we follow the leftmost innermost strategy.
   Testing shows that this method is very effective for proving equivalence between a
non-tail-recursive and a tail-recursive function (as needed for equivalence of a recur-
sive and an iterative C function). The examples of § 4 show its effect: by eliminating
the non-tail-recursive functions early on, we are more likely to arrive at a diverging se-
quence where all equations have the same outer shape; e.g., (u(→    −
                                                                    q i ) ≈ C[u(→
                                                                                −
                                                                                v i ), u(→
                                                                                         −
                                                                                         w i )] |
i ∈ N). As observed in § 5.3, this is ideal for our generalization method.
   Following an E XPANSION, we first process those new equations in Expd (s ≈ t [φ], p)
whose multiset of new symbols is smallest in the recursion order ≻. Thus, for exam-
ple in Ex. 4.10, after expanding (FCT.D) we consider (FCT.E)—which has new sym-
bols {return, 1}—before (FCT.F)—with new symbols {mul, factrec, −, 1}—since factrec ≻
return, 1. Intuitively, “smaller” terms are “closer” to the end of a function, which allows
D ISPROVE to succeed faster and thus aids the backtracking mechanism.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:32                                                                               C. Fuhs, C. Kop, N. Nishida

   6.1.5. Constraint Modification. Following S IMPLIFICATION and E XPANSION, Ctrl modi-
fies the constraint, as follows. First, when a clause φi in the constraint φ1 ∧ · · · ∧ φn
is implied by the others, it is removed unless it is a definition clause vi = n. We also
remove clauses for variables which do not play a role. Most importantly, Ctrl introduces
ranged quantifications ∀x ∈ {k1 , . . . , kn }(φ(x)) whenever possible, provided n ≥ 3 (to
lessen the effect of coincidence). Formally, we could describe our approach as follows:
   if φ has clauses C[a], C[b], C[c] for some context C and variables a, b, c, as well as
 b = f (a) and c = f (b), then we may replace the C-clauses by ∀i ∈ {0, . . . , 2}(C[f i (a)])
This is more general than what we use; it lets us for instance replace a[i] = 0 ∧ a[j] =
0 ∧ a[k] = 0 ∧ j = i + 2 ∧ k = j + 2 by ∀l ∈ {0, . . . , 2}(a[i + 2 · l] = 0), for f = λx.x + 2. But to
represent f i , Ctrl must know the relevant theory. Therefore, we currently only consider
clauses where b = a+1 and c = b+1, and replace them by ∀i ∈ {a, . . . , c}(C[i]). Since we
implement loop counters as integers, this still captures a large group of constraints.
   After ∀-introduction, if a boundary of the range (0 and 2 in the example) is some
vi ∈ Vinit , we replace it by the value it is defined as, to avoid generalizing the starting
point of a quantification. Thus, e.g., ∀j ∈ {v0 , . . . , k}(select(x, j) ̸= 0) ∧ v0 = 0 ∧ i =
v0 +1∧k = i+1 is replaced by ∀j ∈ {0, . . . , k}(select(x, j) ̸= 0)∧v0 = 0∧i = v0 +1∧k = i+1.
  6.1.6. Non-Confluence. Our strategy is admittedly unfair to non-confluent systems: a
successful application of D ISPROVE is treated as evidence of an unsound equation,
which is not the case without confluence: the non-confluent (LC)TRSs R = {f → a, f →
b, g → a, g → b} along with the inductive theorem f ≈ g highlights that we only have
to prove that two functions can produce the same result, not that they always do.
  This is deliberate: when proving that two functions produce the same result, we
can see non-confluent LCTRSs as inherently incorrect. Thus, we focus on confluent
systems. For LCTRSs whose confluence is unknown, it is preferable to show non-
equivalence (which translates to a MAYBE in the output) over equivalence.
6.2. Experiments
To assess performance and precision of Ctrl empirically, we tested five assignments
from a group of students in the first-year programming course in Nagoya,
                                                                    Pn         all automat-
ically translated to LCTRSs by c2lctrs: sum: given n, implement
                                                              Pm       i=1 i; fib:  compute
the nth Fibonacci number; sumfrom: given n, m, implement i=n i; strlen and strcpy.
We compared the first three to LCTRS-versions of recursive reference implementa-
tions;6 for strlen and strcpy we used a specification as in Ex. 4.26 and 4.28.7 We also
tested our own implementations of fact from Ex. 4.2 and arrsum from Ex. 4.27, along
with 25 function comparisons from the literature and 12 memory-safety benchmarks
from the Competition on Software Verification [SV-COMP]. The benchmarks (also from
the literature) are typically fairly small: the largest, lit03 GS13 fig6, has 70 lines of
C code and 55 rewrite rules. We used an Intel i7-5600U CPU at 2.6 GHz under Linux.
   We quickly found that many of the student programs had failed to account for bound-
ary conditions, such as empty strings or negative input. This causes a NO, or a MAYBE
if the system cannot be proved confluent, so if not all variables are initialized. To limit
the impact of these errors, we did a second test, where we altered the specification to
account for these mistakes. The results of both tests are summarized in Figure 1.

6 However, honesty compels us to mention that for fib, we used a manual translation because the one ob-
tained from c2lctrs was impractical: where our manual translation has a rule fibrec(x) → plus(fibrec(x −
1), fibrec(x − 2)) [x ≥ 2], the automatic one splits the two recursive calls (recall § 3.5). Therefore, a more
sophisticated termination argument is needed, and it is harder to eliminate the recursion in the inductive
process. Handling such cases in the future will likely necessitate an additional lemma generation technique.
7 Interestingly, in strcpy02 the student’s strlen solution is called as a helper function for strcpy.




                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                           A:33

  function            YES         NO        MAYBE             time           Legend: YES indicates that
     sum              9/9         0/0        6/6            2.1 / 2.1        a proof was found, NO a
     fib              4 / 10      6/1        3/2            7.6 / 5.6        disproof (so a conclusion ⊥);
   sumfrom            3/3         1/0        2/3            1.8 / 2.1        MAYBE denotes that Ctrl
   strlen             1/2         0/0        5/4            4.1 / 4.0
   strcpy             3/5         0/0        3/1           21.8 / 17.1       found no proof or disproof,
   arrsum             1/1         0/0        0/0            3.9 / 3.9        took more than 60 seconds, or
    fact              1/1         0/0        0/0            2.2 / 2.2        failed to prove termination of
 literature           4/5         3/2       18 / 18         4.0 / 3.9        the LCTRS. The time column
   safety             3/3         2/2        7/7           22.3 / 22.3       lists the average runtime on
    total            29 / 39     12 / 5     44 / 41                          YES and NO results.
Fig. 1. Results of Ctrl in the initial test (before the slash), and with obvious mistakes fixed (after the slash).

   We found five classes of recurring failures. First, cases where the function was
wrong, but Ctrl could not answer NO as it could not prove confluence. This accounts
for six MAYBEs in the initial test and two in the second, and could be considered an
incorrect implementation. Second (six failures in either table) is the termination re-
quirement: we need termination independent from the starting symbol, which is often
not satisfied or cannot be proved by our admittedly limited termination module.
   The remaining groups of failures each demonstrate a weakness of our method. The
third failure occurs when generalization drops a relation between two variables; e.g.,
when x and y are both initialized to 0 and then increased by 1 in every loop iteration
(with loops corresponding to tail-recursive functions); after generalizing, the informa-
tion that they are equal is lost. Typically, this manifests as an E XPANSION where the
non-diverging case can easily be removed before generalization, but afterwards gives
an equation that can be disproved. This suggests a natural direction for improvement.
   The fourth group are those benchmarks where our primary generalization technique
(§ 5.1) does not apply because there are no variables to generalize. This happens when
both sides have non-tail-recursive functions or loops counting down rather than up.
Recursion-abstraction (§ 5.2) lets us solve several benchmarks, but further lemma gen-
eration will be needed for the majority. Nonetheless, this generalization technique does
allow us to handle Ex. 4.30, which can be challenging for existing approaches.
   The final group concerns nested loops. Ctrl’s strategy fails because the counters for
the inner and outer loop are generalized at the same time. However, inductive proofs
with Ctrl’s interactive mode show that such benchmarks can be handled by our method.
Thus, in future work a more sophisticated generalization strategy would be desirable.
   Demonstrative examples of these last three issues are given in Appendix D. A full
evaluation page, including exact problem statements, is given at:
                          http://cl-informatik.uibk.ac.at/software/ctrl/tocl/

7. RELATED WORK
The related work can be split into two categories. First, the literature on rewriting
induction; and second, the work on program verification and equivalence analysis.

7.1. Rewriting Induction
Our inductive theorem proving method builds on a long literature about rewriting in-
duction (see e.g., [Bouhoula 1997; Falke and Kapur 2012; Reddy 1990; Sakata et al.
2009]). Its core method extends existing techniques to the LCTRS formalism intro-
duced in [Kop and Nishida 2013], thus generalizing the possibilities of earlier work.
  The most relevant related works are [Falke and Kapur 2012; Sakata et al. 2009],
defining rewriting induction for different styles of constrained rewriting. Both use only

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:34                                                                          C. Fuhs, C. Kop, N. Nishida

integer functions and predicates; it is not clear how to generalize these approaches to
more advanced theories. The more general setting of LCTRSs enables rewriting induc-
tion also for systems with, e.g., arrays, bitvectors, or real numbers. Moreover, not re-
stricting the predicates in Σtheory enables (a limited form of) quantifiers in constraints.
   These advantages are enabled by subtle changes to the inference rules, in particular
S IMPLIFICATION and E XPANSION. Our changes let us modify constraints of an equa-
tion and handle irregular rules with fresh variables in the constraint. This additionally
enables E XPANSION steps to create such (otherwise infeasible) rules. The method re-
quires a very different implementation from previous definitions: we need separate
strategies to simplify constraints (e.g., deriving quantified statements), and, for the
desired generality, must rely primarily on external solvers to manipulate constraints.
   Moreover, we have introduced a completely new generalization technique, as a pow-
erful tool for analyzing loops in particular. Nakabayashi et al. [2010] use a similar
idea (abstracting the initialization values), but the execution is very different: for an
equation s ≈ t [φ], first s ≈ t is adapted via templates obtained from the rules, then
φ is generalized via a set of relations between positions tracked by the proof process.
In our method, the constraint carries all the information. We succeed on all examples
in [Nakabayashi et al. 2010], and on some where their method fails (cf. Appendix C;
e.g., for non-negative n, a for-loop summing up from 1 to n is compared to n*(n+1)/2).
   For unconstrained systems, the literature contains several generalization methods,
e.g., [Kapur and Sakhanenko 2003; Kapur and Subramaniam 1996; Urso and Kounalis
2004]. Mostly, our method in § 5.1 is very different from these approaches. Most sim-
ilar, perhaps, is [Kapur and Sakhanenko 2003], which also proposes a method to gen-
eralize initial values. As observed by Nakabayashi et al. [2010], this method is not
sufficient for even our simplest benchmarks sum and fact, as the argument for the
loop variable cannot be generalized; in contrast, our method has no problem with such
variables. As discussed in § 5.2, the recursion-abstraction technique presented there
essentially lifts a technique from explicit induction [Aubin 1979] to constrained rewrit-
ing induction.
   As far as we are aware, there is no other work for lemma generation of rewrite
systems (or functional programs) obtained from procedural programs.
   Like Giesl et al. [2007], we verify procedural programs via a transformation to a
functional program, followed by an invocation of an inductive theorem prover. In an un-
constrained setting, they propose an equivalence-preserving program transformation
to a non-tail-recursive program to eliminate accumulator arguments. A combination
of their approach with ours could be beneficial e.g. for programs with nested loops.


7.2. Automatic Program Verification and Equivalence Proving
Our goal is to (automatically) verify correctness properties of procedural programs.
Fully automated verifiers for properties like (memory) safety and termination are reg-
ularly assessed at the Competition on Software Verification [SV-COMP]. However, a
comparison with these tools does not seem useful. While we can, to some extent, tackle
(memory) safety and termination, our main topic is equivalence, which is not studied
in SV-COMP. Technically, equivalence problems can be formulated as safety problems
(by self-composition [Barthe et al. 2011]: call both programs on equal inputs and assert
that their results are also equal). However, none of the tools in the “recursive” category
of SV-COMP 2015 could prove equivalence for our simplest (integer) example sum.
   Apart from constrained rewriting, another intermediate representation for verifica-
tion of imperative programs is based on (constrained) logic programs or, closely related,
Horn clauses [Albert et al. 2007; Gupta et al. 2011]. It should be possible to express our
contributions also in this framework, provided that constructor terms are supported.

                     ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:35

   For the setting of Ex. 1.1, automated grading, Vujosevic-Janicic et al. [2013] apply
verification techniques like bounded model checking. While this enables significant
improvements over classic testing, there is still a non-zero risk of missing bugs due to
under-approximation. Thus, it could be beneficial to add our approach to the portfolio.
   For program equivalence, we discuss (fully) automated techniques for proving par-
tial equivalence and its special case total equivalence. Two programs P1 and P2 are
partially equivalent if for the same inputs, terminating executions of P1 and P2 return
the same value. They are totally equivalent if they moreover both terminate on all
inputs (see [Godlin and Strichman 2008] for a more extensive discussion).
   This paper addresses total equivalence: we require termination to analyze partial
equivalence. We allow constrained equivalence queries so that only certain inputs are
considered. This includes properties that cannot be checked programmatically, like the
size of an array in a C program. As mentioned in § 6.1, for non-confluent programs P1
and P2 , we analyze if running P1 on the input can lead to the same result as P2 .
   Godlin and Strichman [2008] propose a Hoare-style proof rule for partial equivalence
of recursive programs (among other properties). To analyze two recursive functions
f1 and f2 , these symbols are first replaced in recursive calls in their bodies by the
same uninterpreted function symbol f . Under this premise, it is then proved (e.g., by
a bounded model checker) that the bodies of f1 and f2 also have equivalent results. In
this sense, Godlin and Strichman [2008] also use inductive reasoning. However, our
approach proves equivalence of Ex. 4.30 with different recursion base cases, whereas
their proof rule is not applicable. Moreover, the use of uninterpreted function symbols
requires that the programs must be deterministic, in contrast to our approach.
   Lopes and Monteiro [2016] prove partial equivalence for programs on integers and
undefined function symbols (which may arise also as abstractions of deterministic com-
plex functions). They combine self-composition [Barthe et al. 2011], a safety-preserving
transformation of undefined functions to polynomials (yielding a program on integers
only), recurrence solving for loops, and a standard software model checker. However,
their approach does not support mutable arrays, whose content can be changed during
the program’s execution (as in Ex. 4.28 for strcpy), in contrast to our method.
   Verdoolaege et al. [2012] use widening to prove program equivalence. For validation
of compiler optimizations [Necula 2000], they consider programs with (linear-)affine
arithmetic and arrays. A restriction of their approach is that it does not exploit the
semantics of arithmetic operations beyond associativity and commutativity.
   Recently, regression verification has become an active topic of research in program
equivalence proving [Godlin and Strichman 2013; Lahiri et al. 2012; Felsing et al.
2014]. As in regression testing, two programs are compared that are syntactically al-
most the same, e.g., different revisions of the same code base with a refactored function.
Regression verification then analyzes if the two programs are semantically equivalent.
   Godlin and Strichman [2013] improve modularity over [Godlin and Strichman 2008]
by decomposing the proof obligations into smaller units via the call graph of the pro-
gram. Hawblitzel et al. [2013] propose mutual summaries, relating the postconditions
of two program functions. This generalizes uninterpreted functions as summaries and
allows analysis of non-deterministic programs. A challenge is to find such mutual sum-
maries automatically. Felsing et al. [2014] address this problem via Horn constraint
solving to find coupling predicates over linear arithmetic between program points. It
would be interesting to adapt their approach for lemma generation. They also analyze
total equivalence: a separate termination proof is required. The web interface of their
tool llrêve currently fails on the same example as [Nakabayashi et al. 2010] (cf. § 7.1).
They mention an extension to arrays and heap data structures as future work.




ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:36                                                                             C. Fuhs, C. Kop, N. Nishida

8. DIRECTIONS FOR FUTURE WORK
This paper is by no means intended as the end station for inductive theorem proving
on LCTRSs, but rather as the beginning. The generalization methods we supply are
powerful together, but they do not suffice for more complicated systems or equations.
A mere two methods cannot bypass the need to search for loop invariants altogether.
  A natural extension would thus be both to adapt existing lemma generation tech-
niques to the constrained setting and to adapt techniques for finding loop invariants
towards the setting of rewriting induction, e.g., to suggest suitable lemmas. It might
also be worthwhile to directly look at the constraints and develop advanced methods
for constraint modification, which could be followed by a generalization step. More-
over, our generalization technique from § 5.1 could be improved to generalize not only
initializations with constants, but also initializations with other values, e.g., copies of
function parameters. This is motivated by loops that count down instead of up. Ad-
ditionally, inspired by [Lopes and Monteiro 2016], one might consider LCTRSs with
uninterpreted functions to model functions with unknown implementations.
  For a different direction, we may extend the translation from § 3, e.g., by translating
structs to term data structures (cf. [Otto et al. 2010]). The ideas from § 3 can also be
applied for languages such as Python or Java, enabling equivalence proofs between
functions in different languages. This could be particularly interesting for a reference
implementation in an inherently memory-safe language like F# or Java, and an effi-
cient implementation in a language like C that has no such memory safety guarantees.
  Finally, we hope to extend the implementation in the future, both to increase the
strength of the inductive theorem proving—adding new theory and testing for more
sophisticated heuristics—and to add more features to the translation from C code.
9. CONCLUSIONS
In this paper, we have done two things. First, we have discussed a transformation from
procedural programs to constrained term rewriting. By abstracting from the memory
model underlying a particular programming language and instead encoding concepts
like integers and arrays in an intuitive way, this transformation can be applied to
various different (imperative) programming languages. The resulting LCTRS is close
to the original program and has built-in error checking for all mistakes of interest.
   Second, we have extended rewriting induction to the setting of LCTRSs. We have
shown how this method can be used to prove correctness of procedural programs. The
LCTRS formalism is a good analysis backend for this, since the techniques from stan-
dard rewriting can typically be extended to it, and native support for logical constraints
and data types like integers and arrays is present.
   We have also introduced two new techniques to generalize equations. The idea of
the core method is to identify constants used as variable initializations, keep track of
them during the proof process, and abstract from these constants when a proof attempt
diverges. The LCTRS setting is instrumental in the simplicity of this method, as it
boils down to dropping a (cleverly chosen) part of a constraint. The second method
recognizes—and abstracts—recursive calls on semantically equivalent arguments.
   In addition to the theory, we provide an implementation of these techniques. Initial
results on a small database of programs from students and the literature are very
promising. In future work, we aim to increase the strength of our implementations.

ACKNOWLEDGMENTS
We are grateful to Stephan Falke, who contributed to an older version of this work, and for the helpful
remarks of the reviewers for [Kop and Nishida 2014] and for the present paper.




                        ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                  A:37

 A. TRANSLATING C PROGRAMS TO LCTRSS
 This appendix provides further details on the translation from C programs to LCTRSs.
 A.1. Optimizing LCTRSs
 After generating the LCTRS, we simplify the (left-linear) result by the following steps:
(1) Combining unconstrained rules. Like [Falke et al. 2011], we repeat the following:
    — select any unconstrained rule ρ of the form u(x1 , . . . , xn ) → r where u is not the
       initial symbol of a C function (like fact in Ex. 3.1), and u neither occurs in r nor
       in the left-hand side of any other rule; the repetition stops if no such ρ exists;
    — rewrite all right-hand sides with ρ;
    — remove both the rule ρ and the symbol u.
    This process does not substantially alter the multi-step reduction relation →∗ as
    the only symbols removed are those which we think of as “intermediate” symbols.
(2) Combining constrained rules. If there are distinct rules ℓ → r [φ] and ℓ → r [ψ] (mod-
    ulo renaming), these are combined into ℓ → r [φ∨ψ]. Given rules ℓ → u(s1 , . . . , sm ) [φ]
    and u(x1 , . . . , xm ) → ri [ψi ] for 1 ≤ i ≤ n with all xj variables, we may replace them
    by ℓ → ri [x1 := s1 , . . . , xm := sm ] [φ ∧ ψi [x1 := s1 , . . . , xm := sm ]] for 1 ≤ i ≤ n, if:
    — u is not the initial symbol of a function and does not occur in any other rule, or ℓ;
    — the terms sj do not contain defined symbols (as then we might remove a non-
       terminating subterm, which would impact the multi-step reduction relation).
(3) Removing unused arguments. For all function symbols and all their argument posi-
    tions, we mark whether the position is “used”:
    — all argument(s) of every returnf and initial symbols (e.g. fact) are used;
    — for other symbols ui of arity n and every 1 ≤ j ≤ n: if there is a rule
       ui (ℓ1 , . . . , ℓn ) → r [φ] where ℓj is not a variable (which can arise for instance
       with the transformation in § 3.5) or occurs in φ, then argument j is used in ui ;
    — for all rules ui (ℓ1 , . . . , ℓn ) → r [φ] and 1 ≤ j ≤ n: argument j is used in ui if ℓj is a
       variable occurring at a used position in r; here, a position p is used in s if either
       p = ϵ or p = i · p′ , s = f (⃗t), argument i is used in f and position p′ is used in ti .
    The last, recursive, step essentially calculates a fixpoint; in summary, an argument
    position is used if it is possible to reduce to a term where we actually need the
    subterm at that position as part of a constraint or the function’s return value. When
    a variable is not used in any later statement, we will avoid carrying it along.
(4) Simplifying constraints. Constraints may be brought into an equivalent form, e.g.,
    by removing duplicate clauses or replacing, e.g., ¬(x > y) by x ≤ y. Here, φ is
    “equivalent” to ψ in a rule ℓ → r [φ] if ∀⃗x(∃⃗y (φ) ↔ ∃⃗z(ψ)) holds, where Var (ℓ) ∪
    Var (r) = {⃗x}, Var (φ) \ {⃗x} = {⃗y }, and Var (ψ) \ {⃗x} = {⃗z} (much like the observation
    on ∼ below Def. 2.14). We typically only remove negations and unused variables.
    Example A.1. As an example, let us consider the simplification of a toy function.
   int f(int x) {                                             f(x) → u1 (x, y, z)
     int y,z;                                          u1 (x, y, z) → u2 (x, y, z)     [x < 0]
     if (x < 0) return 0;                              u1 (x, y, z) → u3 (x, y, z)     [¬(x < 0)]
     z = 0;                                            u2 (x, y, z) → returnf (0)
     while (x > 0) {                                   u3 (x, y, z) → u4 (x, y, 0)
       x--;                                            u4 (x, y, z) → u5 (x, y, z)     [x > 0]
       z += x;                                         u4 (x, y, z) → u7 (x, y, z)     [¬(x > 0)]
     }                                                 u5 (x, y, z) → u6 (x − 1, y, z)
     y = z + x;                                        u6 (x, y, z) → u4 (x, y, z + x)
     return y;                                         u7 (x, y, z) → u8 (x, z + x, z)
   }                                                   u8 (x, y, z) → returnf (y)

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:38                                                                              C. Fuhs, C. Kop, N. Nishida

    The rule f(x) → u1 (x, y, z) has unconstrained variables y and z in the right-hand side
 which do not occur on the left. A step with this rule instantiates y and z by arbitrary
 type-correct values. This reflects that in the C program the variables y and z are at
 first not initialized and may contain an arbitrary value (depending on the compiler).
 In the simplified version, this does not occur; consider the remainder obtained from
 combining rules:
            f(x) → returnf (0)               [x < 0]    Now, the first and third arguments
            f(x) → u4 (x, y, 0)              [¬(x < 0)] of u are used (in the constraint
                                                             4
     u4 (x, y, z) → u4 (x − 1, y, z + x − 1) [x > 0]    and return value), but the second is
     u4 (x, y, z) → returnf (z + x)          [¬(x > 0)] not: it is merely passed along in the
 recursive call. Removing this variable and simplifying the constraints, we obtain:
                                               This system is orthogonal in the sense
         f(x) → returnf (0)            [x < 0]
                                               of [Kop and Nishida 2013] and thus con-
         f(x) → u4 (x, 0)              [x ≥ 0]
                                               fluent, which is beneficial for analysis.
     u4 (x, z) → u4 (x − 1, z + x − 1) [x > 0]
                                               The original LCTRS was also confluent,
     u4 (x, z) → returnf (z + x)       [x ≤ 0]
                                               but this was harder to see.

   Correctness relies on the fact that the LCTRSs created using the transformation
 described in § 3 are “well behaved”; most importantly, all rules are left-linear.

 A.2. Translating C Programs with Explicit Pointers
 As observed at the end of § 3.6, the simple translation explored there has both up- and
 downsides. On the one hand, by abstracting from the memory model, we can simplify
 analysis. On the other hand, there are certain programs we cannot handle.
    For C programs with dynamically allocated arrays and/or explicit pointer use, we
 consider the memory model from the C standard. Declaring or allocating an array
 selects an amount of currently unused space in memory and designates it for use by the
 given array. The allocated space is not guaranteed to be at a given position in memory
 relative to existing declarations; when an array is indexed out of its declared bounds,
 the resulting behavior is undefined—so this can safely be considered an error (see
 paragraph 6.5.6:9 in: http://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf).
    We will think of a program’s memory as a set of blocks, each block corresponding to a
 sequence of values. A pointer then becomes a location in such a block. In an LCTRS we
 will model this using a “global memory” variable, which lists the blocks as a sequence
 of arrays; a pointer is a pair of integers, selecting a memory block and its offset.
    Limiting interest to programs on (dynamically allocated) integer or char arrays, we
 will use a memory variable of sort array(array(int)), which represents a sequence of
 integer arrays (i.e. (Z∗ )∗ ); the default value 0array(int) is the empty sequence ⟨⟩ ∈ Z∗ . We
 use a theory signature with the array symbols introduced in § 3.6, along with:

— allocate : [array(array(int))×array(int)] ⇒ array(array(int)), where Jallocate (⟨a0 , . . . , ak ⟩, b) =
  ⟨a0 , . . . , ak , b⟩; that is, allocate(mem, arr ) adds the new sequence arr to the memory;
— free : [array(array(int)) × int] ⇒ array(array(int)), where Jfree (⟨a0 , . . . , ak ⟩, n) = ⟨a0 , . . . ,
  an−1 , ⟨⟩, an+1 , . . . , ak ⟩ if 0 ≤ n ≤ k and ⟨a0 , . . . , ak ⟩ otherwise; that is, the memory block
  indexed by n is considered empty, and any further attempt to address a location in
  that memory block should be considered an error.

 A pointer is represented by a pair (b, o) of a block index and an offset within that block.
 The NULL-pointer is represented by (−1, 0).

                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                A:39

    Example A.2. Consider the following example C++ function:

 int *create(int k) {
   int *a = new int[k];
   int *b = a + 1;
   for (int i = 0; i < k; i += 2) b[i] = 42;
   return a;
 }

 Now, a and b share memory, and new memory is allocated. We might encode this as:
           create(mem, k) → u(allocate(mem, x), k, size(mem), 0)                       [size(x) = k]
         u(mem, k, ai, ao) → v(mem, k, ai, ao, ai, ao + 1, 0)
   v(mem, k, ai, ao, bi, bo, i) → w(mem, k, ai, ao, bi, bo, i)                                [i < k]
   v(mem, k, ai, ao, bi, bo, i) → return(mem, ai, ao)                                         [i ≥ k]
   w(mem, k, ai, ao, bi, bo, i) → error               [bo + i < 0 ∨ bo + i ≥ size(select(mem, bi))]
   w(mem, k, ai, ao, bi, bo, i) → v(store(mem, bi, store(select(mem, bi), bo + i, 42)), k,
                                    ai, ao, bi, bo, i + 2)     [0 ≤ bo + i < size(select(mem, bi))]

 (For clarity, we omit the optimization step that combines the first two rules, and the
 one that combines the third with the last two.)
   Consider how this example is executed, starting from empty memory. We will use ⟨·⟩
 to refer to specific arrays of type array(array(int)) and [·] for arrays of type array(int).

(1) We call create(⟨⟩, 2), representing a function call when no arrays have been allocated.
(2) By the first rule, we get u(allocate(⟨⟩, x), 2, size(⟨⟩), 0), where x is a random array. All
    we know is that it has size 2—this rule uses irregularity to represent the random-
    ness involved in an allocation. Thus, assume the sequence [−4, 9] is chosen. Using
    calculation steps to evaluate allocate and size, we get u(⟨[−4, 9]⟩, 2, 0, 0). Here, the pair
    (0, 0) represents the array a: the first block in memory, read from the start (offset 0).
(3) Then by the second rule (and a calculation), we reduce to v(⟨[−4, 9]⟩, 2, 0, 0, 0, 1, 0).
    The new pair (0, 1) represents b: the same memory block as a, but with offset 1. This
    location points to the sequence [9]. The final 0 is the index for the loop counter i.
(4) Entering the loop (as indeed 0 < 2), we reduce to w(⟨[−4, 9]⟩, 2, 0, 0, 0, 1, 0).
(5) Here, we do an array store: b[i] = 42;. The LCTRS first tests whether b[i]
    corresponds to a position in allocated memory and reduces to an error state if
    not. This is done by selecting the corresponding block from mem, then testing
    whether the offset for b and i together exceed the block’s bounds. We succeed, as
    0 ≤ 0 + 1 < size(select(⟨[−4, 9]⟩, 0)) ⇔ 0 ≤ 1 < size([−4, 9]) ⇔ 0 ≤ 1 < 2.
(6) Thus, the update is done: we reduce to:
    v(store(⟨[−4, 9]⟩, 0, store(select(⟨[−4, 9]⟩, 0), 1 + 0, 42)), 2, 0, 0, 0, 1, 0 + 2)
    →∗calc v(store(⟨[−4, 9]⟩, 0, store([−4, 9], 1, 42)), 2, 0, 0, 0, 1, 2)
    →∗calc v(store(⟨[−4, 9]⟩, 0, [−4, 42]), 2, 0, 0, 0, 1, 2)
    →calc v(⟨[−4, 42]⟩, 2, 0, 0, 0, 1, 2)
    So we retrieve the space for b from memory (getting the full block [−4, 9]), update
    the position corresponding to b[0] (which is the same as a[1]), get [−4, 42], and store
    the result into the corresponding position in memory. Then we carry on with i + 2.
(7) Since 2 ≥ 2, we reduce to return(⟨[−4, 42]⟩, 0, 0), returning the dynamic array [−4, 42].

 Note that in step 5, we do not test whether b corresponds to currently allocated mem-
 ory. This is safe because, if b is the NULL-pointer or corresponds to previously freed
 memory, then select(mem, bi) is ⟨⟩, and any indexing in this array will cause an error
 regardless. Note also that this function gives a non-error result only for even k.

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:40                                                                           C. Fuhs, C. Kop, N. Nishida

   While Ex. A.2 considers only integer arrays, we could also handle programs with dy-
 namically allocated arrays of varying types. In this case, we would simply use multiple
 memory variables with different type declarations.

 B. CORRECTNESS PROOF
 In this appendix, we give the full correctness proof, which was only sketched in § 4.4.
   First, we prove Lemma 4.31, reformulated as follows:
   L EMMA 4.31. The following statements are equivalent:
— all equations in E are inductive theorems;
— ↔E ⊆ ↔∗R on ground terms (so if s, t are ground and s ↔E t, then also s ↔∗R t).
    P ROOF. Suppose ↔E ⊆ ↔∗R on ground terms. If s ≈ t [φ] ∈ E and the ground con-
 structor substitution γ respects this equation, then sγ and tγ are ground (since, by
 definition of “respects” (Def. 4.3), Var (s) ∪ Var (t) ⊆ Dom(γ)). Since obviously sγ ↔E tγ
 (with empty C), by assumption sγ ↔∗R tγ. Thus, s ≈ t [φ] is an inductive theorem.
   Suppose that all equations in E are inductive theorems, and u ↔E w for ground u, w;
 we must see that u ↔∗R t. We have u = C[sγ] and w = C[tγ] for some s ≈ t [φ] ∈ E and
 substitution γ that respects φ and maps all variables in s, t to ground terms. Let δ be
 a substitution such that each δ(x) is a normal form of γ(x); by termination of R, such
 a δ exists, and by quasi-reductivity, it is a ground constructor substitution. As values
 cannot be reduced, also δ respects φ. Therefore sδ ↔E tδ, which implies sδ ↔∗R tδ. We
 conclude: C[sγ] ↔∗R C[sδ] ↔∗R C[tδ] ↔∗R C[tγ], giving the desired result.
   Recall also the following key lemma (whose proof has been given in the main text):
   L EMMA 4.32 ([S AKATA ET AL . 2009]). Let →1 and →2 be binary relations over
 some set A. Then, ↔∗1 = ↔∗2 if all of the following hold:
— →1 ⊆ →2 ,
— →2 is well founded, and
— →2 ⊆ (→1 · →∗2 · ↔∗1 · ←∗2 ).
   Lemma 4.33 in the main text is the combination of the following Lemmas B.1–B.4.
    L EMMA B.1. Let s, t be terms, φ a constraint and p a position of s such that s|p has
 the form f (s1 , . . . , sn ) with f a defined symbol and all si constructor terms. Suppose
 that the variables in s, t, φ are distinct from those in R. Then:
(1) For any ground constructor substitution γ which respects s ≈ t [φ] and any choice of
    Expd (s ≈ t [φ], p), we have:
                                                            
                                  sγ →R,p · ↔Expd(s≈t [φ],p) tγ
    Here, →R,p indicates a reduction at position p with a rule in R ∪ Rcalc .
(2) For any s′ → t′ [φ′ ] in any choice of Expd (s ≈ t [φ], p) and any ground constructor
    substitution δ which respects s′ ≈ t′ [φ′ ], we have:
                                  s′ δ ←R,p · ↔{s ≈ t [φ]} t′ δ
                                                          

    P ROOF. sγ|p = s|p γ = f (s1 γ, . . . , sn γ), where all si γ are ground constructor terms.
 Since f is defined, f (→
                        −
                        s γ) reduces by quasi-reductivity, which can only be a root reduc-
 tion. Thus, sγ = (sγ)[ℓδ]p for some rule ℓ → r [ψ] and substitution δ which respects ψ.
 Since the rule variables are distinct from the ones in the equation, we can assume that
 δ is an extension of γ, so sγ = s[ℓ]p δ. Clearly, both φδ and ψδ evaluate to ⊤, and δ(x) is
 a value for all x ∈ Var (φ) ∪ Var (ψ).

                       ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                                             A:41

   As δ unifies s|p and ℓ, there is a most general unifier η, so s|p η = ℓη and we can write
 δ = δ ′ ◦ η for some δ ′ . As δ(x) is a value for all x ∈ Var (φ) ∪ Var (ψ), η(x) can only be the
 same value, or a variable. Now, by definition of constrained term reduction, any choice
 of Expd (s ≈ t [φ], p) has an element s′ ≈ t′ [φ′ ] where we can write (for suitable u, η ′
 etc.):
                                                sη[ℓη]p ≈ tη [φη ∧ ψη]
                                             ∼ u[ℓη ′ ]p ≈ t′′ [φ′′ ]
                                    →ℓ→r[ψ],1·p u[rη ′ ]p ≈ t′′ [φ′′ ]
                                             ∼         s′ ≈ t′ [φ′ ]
 Consider the “term” sδ ≈ tδ. This is an instance of the first constrained term in this
 reduction, so by Thm. 2.19, this “term” reduces at position 1 · p to s′ δ ′′ ≈ t′ δ ′′ for some
 substitution δ ′′ which respects φ′ . As the reduction happens inside sδ, we see that
 tδ = t′ δ ′′ . Thus, sγ = sδ →R s′ δ ′′ ↔Expd(s≈t [φ],p) t′ δ ′′ = tδ = tγ.
    As for the second part, note that by definition of Expd there are a substitution γ and
 constraint ψ such that the constrained term sγ ≈ tγ [φγ ∧ ψγ] reduces to s′ ≈ t′ [φ′ ] at
 position 1 · p. By Thm. 2.20, we find a substitution η which respects φγ ∧ ψγ, such that
 sγη ≈ tγη →R s′ δ ≈ t′ δ at position 1 · p. Since the reduction takes place in the left part
 of ≈, we have tγη = t′ δ and sγη →R s′ δ. We are done if also sγη ↔s≈t [φ] tγη, which
 indeed holds because η ◦ γ respects φ (as (φγ ∧ ψγ)η implies φγη).
   L EMMA B.2. Suppose that (E, H, flag) ⊢ri (E ′ , H′ , flag ′ ) by any inference rule other
 than C OMPLETENESS. Then,
                                      ∥ E ⊆ (→∗R∪H′ · ←→
                                     ←→                ∥ E ′ · ←∗R∪H′ )
 on ground terms.
   Here, ←→
          ∥ E ′ denotes a parallel application of zero or more ↔E ′ steps.
    P ROOF. It suffices to show that ↔E\E ′ ⊆ (→∗R∪H′ · ←→                ∥ E ′ · ←∗R∪H′ ) on ground terms:
 if C[u1 , . . . , un ] ←→∥ E C[v1 , . . . , vn ] because each ui ↔ρi vi for some ρi ∈ E, then this gives
 ui →∗R∪H′ u′i ←→       ∥ E ′ vi′ ←∗R∪H′ vi if ρi ∈  / E ′ and ui = u′i ←→
                                                                         ∥ E ′ vi′ = vi if ρi ∈ E ′ , so (sequen-
 tializing parallel steps) C[u1 , . . . , un ] →R∪H′ C[u1 , . . . , u′n ] ←→
                                                          ∗        ′
                                                                                   ∥ E ′ C[v1′ , . . . , vn′ ] ←∗R∪H′
 C[v1 , . . . , vn ] as desired. For all inference rules (except C OMPLETENESS) either E\E ′ = ∅
 or we can write E \ E ′ = {s ≃ t [φ]}. Consider which inference rule is applied for ⊢ri .
— (S IMPLIFICATION). Suppose that s ≃ t [φ] is replaced by u ≈ t [ψ] where s ≈ t [φ]
  →R∪H u ≈ t [ψ]. Let C[sγ] ↔{s≃t [φ]} C[tγ], where γ is a substitution which respects φ.
  It follows from Thm. 2.19 that sγ ≈ tγ →R∪H uδ ≈ tδ where δ is a substitution which
  respects ψ, and thus, as ≈ is a constructor, C[sγ] →R∪H C[uδ] and tγ = tδ. Then,
  C[uδ] ↔{u≈t [ψ]} C[tδ] = C[tγ], and we have C[sγ] →R∪H · ↔E ′ C[tγ]. Symmetrically,
  if C[tγ] ↔{s≃t [φ]} C[sγ], then C[tγ] ↔E ′ · ←R∪H C[sγ]. Thus, ↔s≃t [φ] ⊆ (→∗R∪H · ↔E ′
  · ←∗R∪H ). This suffices because in this case H = H′ .
— (D ELETION). In the case that s = t, the relation ↔E\E ′ is the identity. Otherwise, φ is
  unsatisfiable, so s ≃ t [φ] is never used, i.e., ↔E\E ′ = ∅.
— (E XPANSION). Suppose C[sγ] ↔s≃t [φ] C[tγ], where γ respects s ≃ t [φ]; as we only
  consider ground terms, γ(x) is ground for all variables in its domain. Noting that by
  quasi-reductivity and termination every ground term reduces to a ground constructor
  term, let δ be a substitution where for each x ∈ Dom(γ), δ(x) is a constructor term
  such that γ(x) →∗R δ(x). Then it follows from Lemma B.1 that C[sγ] →∗R C[sδ] (→R
  · ↔E ′ ) C[tδ] ←∗R C[tγ]. The situation where C[tγ] ↔s≃t [φ] C[sγ] is symmetric.
— (EQ- DELETION). Let s = C[s1 , . . . , sn ] and t = C[t1 , . . . , tn ] where s1 , t1 , . . . , sn , tn ∈
  Terms(Σtheory , Var (φ)). Any ground substitution γ which respects φ, and whose do-

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:42                                                                             C. Fuhs, C. Kop, N. Nishida

  main contains all variables in the terms si and ti , must map these variables to val-
  ues. Therefore, si γ →∗calc vi and ti γ →∗calc wi , where vi is the value of si γ and wi is the
  value of ti γ. Now, suppose q ↔s≃t[φ] u for ground q, u. Then (a) q = D[C[s1 , . . . , sn ]]γ
                                                                                               →
                                                                                               −
  and u = D[C[t1 , . . . , tn ]]γ for some ground γ which respects φ, or (b) u = D[C[ t ]]γ and
  q = D[C[→  −
             s ]]γ. In case (a), q →∗R Dγ[Cγ[v1 , . . . , vn ]] and u →∗R Dγ[Cγ[w1 , . . . , wm ]]. If
  each vi = wi , then clearly q →∗R · ←∗R u. Otherwise, (φ ∧ ¬(s1 = t1 ∧ · · · ∧ sn = tn ))γ is
  valid, so we easily get the desired q →∗R · ↔E ′ · ←∗R u. Case (b) is symmetric.
— (D ISPROVE) In this case we do not have (E, H, b) ⊢ri (E ′ , H′ , b′ ).
— (C ONSTRUCTOR) Let s = f (s1 , . . . , sn ), t = f (t1 , . . . , tn ), and suppose C[sγ] ↔{s≈t [φ]}
  C[f (tγ)], where γ is a substitution which respects φ. Since E ′ contains all equations
  si ≈ ti [φ], we have C[sγ] = C[f (s1 γ, . . . , sn γ)] ←→
                                                          ∥ E ′ C[f (t1 γ, . . . , tn γ)] = C[tγ].
— (P OSTULATE) E \ E ′ = ∅, so there is nothing to prove!
— (G ENERALIZATION) Suppose that s ≈ t [φ] is replaced by s′ ≈ t′ [ψ]. Suppose that
  C[sγ] ↔{s≈t [φ]} C[tγ] for some substitution γ which respects φ. Then there exists a
  substitution δ which respects ψ such that C[sγ] = C[s′ δ] ↔{s′ ≈t′ [φ] C[t′ δ] = C[tγ].

   L EMMA B.3. Suppose that (E, H, flag) ⊢ri (E ′ , H′ , flag ′ ) by any inference rule other
 than C OMPLETENESS. If
                             →R∪H ⊆ (→R · →∗R∪H · ←→
                                                   ∥ E · ←∗R∪H )
 on ground terms, then
                           →R∪H′ ⊆ (→R · →∗R∪H′ · ←→
                                                   ∥ E ′ · ←∗R∪H′ )
 on ground terms.
    P ROOF. It suffices to consider the case that E XPANSION is applied (for the other
 cases, we use Lemma B.2). Suppose that s →H′ \H t. Using that, by quasi-reductivity
 and termination, every ground term reduces to a ground constructor term, it follows
 from Lemma B.1 that there exist ground constructor terms s′ , t′ such that s →∗R s′
 (→R · ↔E ′ ) t′ ←∗R t, and hence:
                               s (→R · →∗R∪H′ · ←→
                                                 ∥ E ′ · ←∗R∪H′ ) t


    L EMMA B.4. Suppose that (E, H, flag) ⊢ri · · · ⊢ri (E ′ , H′ , flag ′ ). Then:
(1) ←→ ∥ E ⊆ (→∗R∪H′ · ←→∥ E ′ · ←∗R∪H′ ) on ground terms,
                       ∗
(2) if →R∪H ⊆ (→R · →R∪H · ←→     ∥ E · ←∗R∪H ) on ground terms, then
                             →R∪H′ ⊆ (→R · →∗R∪H′ · ←→
                                                     ∥ E ′ · ←∗R∪H′ )
    on ground terms, and
(3) if R ∪ H is terminating, then so is R ∪ H′ .
   P ROOF. In the following, we will consider relations limited to ground terms only.
 We prove the statements by induction on the number of ⊢ri -steps, where steps in the
 premise of a C OMPLETENESS step are also counted. The base case is evident, so sup-
 pose (E, H, flag) ⊢ri (E1 , H1 , flag 1 ) ⊢∗ri (E ′ , H′ , flag ′ ).
(1) If the first step uses inference rule C OMPLETENESS, then (E, H, flag)                                    ⊢∗ri
    (E1 , H1 , INCOMPLETE) in fewer steps, so by the induction hypothesis:
                               ∥ E ⊆ →∗R∪H1 · ←→   ∥ E1 · ←∗R∪H1
                                                                 
                             ←→

                         ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 Verifying Procedural Programs via Constrained Rewriting Induction                               A:43

    If the first step uses another inference rule, this same property follows from
    Lemma B.2. By the induction hypothesis we have
                                       ∥ E1 ⊆ (→∗R∪H′ · ←→
                                      ←→                 ∥ E ′ · ←∗R∪H′ )
    It follows from H1 ⊆ H′ that
                                        ∥ E ⊆ (→∗R∪H′ · ←→
                                       ←→                ∥ E1 · ←∗R∪H′ )
                  ∥ E1 with (→∗R∪H′ · ←→
    By replacing ←→                    ∥ E ′ · ←∗R∪H′ ), we thus obtain
                           ∥ E ⊆ (→∗R∪H′ · →∗R∪H′ · ←→
                          ←→                         ∥ E ′ · ←∗R∪H′ ·· ←∗R∪H′ )
(2) Assume →R∪H ⊆ (→R · →∗R∪H · ←→ ∥ E · ←∗R∪H ). By the induction hypothesis (in
    case of C OMPLETENESS) or Lemma B.3 (otherwise),
                      →R∪H1 ⊆ →R · →∗R∪H1 · ←→  ∥ E1 · ←∗R∪H1
                                                              

    We complete by the induction hypothesis on (E1 , H1 , flag 1 ) ⊢∗ri (E ′ , H′ , flag ′ ).
(3) Trivial with the induction hypothesis, with the first step using either the induction
    hypothesis again (in case of C OMPLETENESS), the definition of E XPANSION, or the
    observation that other inference rules do not alter H.
 Thus we obtain Lemma 4.33 or, equivalently, Lemma B.5, as the first part of Thm. 4.4.
   L EMMA B.5. If (E, ∅, flag) ⊢ri · · · ⊢ri (∅, H, flag ′ ), then every equation in E is an
 inductive theorem of R.
    P ROOF. It is clear that →R ⊆ →R∪H . It follows from Lemma B.4 that:
— ↔E ⊆ ←→ ∥ E ⊆ →∗R∪H · ←∗R∪H on ground terms,
— →R∪H ⊆ →R · →∗R∪H · ←∗R∪H on ground terms, and
— R ∪ H is terminating.
 By Lemma 4.32 (as equality is included in ↔∗R ) we find that ↔∗R = ↔∗R∪H , and hence
 ↔E ⊆ ↔∗R , on ground terms. We complete with Lemma 4.31.
   Moving on to disproving, we need two auxiliary lemmas:
   L EMMA B.6. If R is confluent and (E, H, COMPLETE) ⊢ri ⊥, then E contains an
 equation s ≈ t [φ] which is not an inductive theorem.
    P ROOF. By confluence and termination together, we can speak of the normal form
 u ↓R of any term u; if u is ground, then by quasi-reductivity its normal form is a ground
 constructor term. A property of confluence is that if w ↔∗R q, then w ↓R = q ↓R . So, it
 suffices to prove that for some s ≈ t [φ] ∈ E there is a ground constructor substitution
 γ which respects this equation, such that sγ and tγ have distinct normal forms.
    The only inference rule that could be used to obtain (E, H, COMPLETE) ⊢ri ⊥ is
 D ISPROVE, so E = E ′ ∪ {s ≃ t [φ]} and one of the following holds:
(1) s, t ∈ Terms(Σtheory , V) with φ ∧ s ̸= t satisfiable. That is, there is a substitution γ
    mapping all variables in the equation to values, such that φγ is valid and sγ and tγ
    reduce to different values by →calc . We are done since all values are normal forms.
(2) s = f (s1 , . . . , sn ) and t = g(t1 , . . . , tm ) with f and g different constructors, and φ is
    satisfiable, so there is a substitution δ mapping all variables in φ to values such that
    φδ is valid. Let γ be an extension of δ which additionally maps all other variables in
    s, t to ground terms (by assumption, ground instances of all variables exist). Then
    φγ is still valid, and sγ and tγ are ground terms with sγ →∗R (sγ)↓R = f ((⃗sγ)↓R ) ̸=
    g((⃗tγ)↓R ) = (tγ)↓R ←∗R tγ.

 ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
 A:44                                                                              C. Fuhs, C. Kop, N. Nishida

(3) s : ι is a variable not occurring in φ, φ is satisfiable, there are at least two different
    constructors f, g with output sort ι and either t is a variable distinct from s or t has
    a constructor symbol at the root. By satisfiability of φ, a substitution δ exists whose
    domain does not contain s, with φδ valid. If t is a variable, let γ be an extension of δ
    mapping s to some ground term rooted by f and t to a ground term rooted by g (by
                                                               →
                                                               −
    assumption ground instances always exist). If t = f ( t ), then let γ be an extension
    of δ mapping s to some ground term rooted by g and mapping all other variables in
    t to ground terms as well. Either way, φγ is valid and (sγ) ↓R ̸= (tγ) ↓R .
    L EMMA B.7. Suppose that →R∪H is terminating and that →R∪H ⊆ →R · →∗R∪H
 · ←→∥ E · ←∗R∪H . If, moreover, R is confluent, (E, H, COMPLETE) ⊢ri (E ′ , H′ , COMPLETE),
 and ↔E ∪ ↔H ⊆ ↔∗R on ground terms, then ↔E ′ ∪ ↔H′ ⊆ ↔∗R on ground terms.
     P ROOF. Assume that all conditions are satisfied; we consider the inference rule used
 to derive (E, H, COMPLETE) ⊢ri (E ′ , H′ , COMPLETE).
    First, suppose the rule used was C OMPLETENESS, so (E, H, COMPLETE) ⊢∗ri
 (E ′ , H′ , INCOMPLETE) and E ′ ⊆ E. As we have assumed that ↔E ∪ ↔H ⊆ ↔∗R , cer-
 tainly ↔E ′ ⊆ ↔E ⊆ ↔∗R . As for ↔H′ , Lemma B.4 gives us that →R∪H′ ⊆ →R · →∗R∪H′
 · ←→  ∥ E ′ · ←∗R∪H′ , so (using again that ↔E ′ ⊆ ↔R and that ←→
                                                                 ∥ E ′ ⊆ ↔∗E ′ ) we can apply
 Lemma 4.32 and termination of →R∪H′ to obtain ↔H′ ⊆ ↔R∪H′ ⊆ ↔∗R .
    If a different rule was applied, then each element in H′ either also belongs to H or
 (in the case of E XPANSION) corresponds to an equation in E. Thus, ↔H′ ⊆ ↔E∪H ⊆↔∗R .
 So let s ≈ t [φ] ∈ E ′ \ E; we must see that ↔{s≈t [φ]} ⊆ ↔∗R on ground terms. By
 Lemma 4.31, it suffices if for all ground constructor substitutions γ which respect this
 equation, sγ ↔∗R tγ. We fix γ and use a case analysis on the applied inference rule.
— (S IMPLIFICATION). There is s′ ≃ t′ [φ′ ] ∈ E such that s′ ≈ t′ [φ′ ] →R∪H s ≈ t [φ] at
  position 1 · p. By Thm. 2.20, we can find δ which respects φ′ such that s′ δ →R∪H sγ at
  position p and t′ δ = tγ. As →R ∪ →H ⊆ ↔∗R by the assumption, sγ ↔∗R s′ δ ↔E t′ δ = tγ,
  which suffices because ↔E ⊆ ↔∗R .
— (D ELETION). No equations are added in this case.
— (E XPANSION). There is s′ ≃ t′ [φ′ ] ∈ E such that s ≈ t [φ] ∈ Expd (s′ ≈ t′ [φ′ ], p) for some
  p. By Lemma B.1(2), we have sγ (←R · ↔E ) tγ, which suffices because ↔E ⊆ ↔∗R .
— (EQ- DELETION) s ≃ t [φ′ ] ∈ E, where φ = φ′ ∧ ¬(s1 = t1 ∧ · · · ∧ sn = tn ), and
                                                                    →
                                                                    −
  s = C[s1 , . . . , sn ], t = C[t1 , . . . , tn ] for some C, → −
                                                                 s , t . Since any substitution which
  respects φ also respects φ , we must have sγ ↔E tγ, so sγ ↔∗R tγ.
                                        ′

— (D ISPROVE) A reduction with this rule does not have the required form.
— (C ONSTRUCTOR) There is f (. . . , s, . . .) ≈ f (. . . , t, . . .) [φ] ∈ E, and by assumption
  f (. . . , s, . . .)γ ↔∗R f (. . . , t, . . .)γ. By confluence, this means that f (. . . , sγ, . . .) ↓R =
  f (. . . , tγ, . . .) ↓R , which implies that (sγ) ↓R = (tγ) ↓R .
— (P OSTULATE, G ENERALIZATION) A reduction with these rules does not have the form
  required by the lemma (as the COMPLETE flag is removed).
    This leads to the second part of Thm. 4.4, which largely corresponds to Lemma 4.34:
   L EMMA B.8. If R is confluent and (E, ∅, COMPLETE) ⊢ri · · · ⊢ri ⊥, then there is
 some equation in E which is not an inductive theorem of R.
   P ROOF. If (E, ∅, COMPLETE) = (E1 , H1 , flag 1 ) ⊢ri · · · ⊢ri (En , Hn , flag n ) ⊢ri ⊥, then
 we easily see that flag i = COMPLETE for all i. By Lemma B.6, En contains an equation
 s ≈ t [φ] which is not an inductive theorem. Then ↔En ̸⊆ ↔∗R on ground terms. By
 Lemma B.7, Lemma B.4, and induction on n − i, this means that ↔E ∪ ↔∅ ̸⊆ ↔∗R on
 ground terms, so by Lemma 4.31, not all e ∈ E are inductive theorems.

                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                            A:45

Proof of Thm. 4.4. Immediately by Lemmas B.5 and B.8.

C. SIMPLE SUM
To demonstrate the difference in power between our technique and earlier work,
even when not considering advanced data structures which were not supported
in [Nakabayashi et al. 2010] or [Falke and Kapur 2012], we have included an example
that can be handled with the technique in this paper (and is automatically proved by
Ctrl), but not with [Nakabayashi et al. 2010] or [Falke and Kapur 2012] (the latter of
which is not surprising, as it does not use any lemma generation at all).

   Example C.1. In the programming course in Nagoya, students in the first lecture
were asked to implement a function sum which computes the summation from 0 to a
given non-negative integer x. The teacher’s reference implementation was:


int sum(int x) {
    int z = 0;
    for (int i = 1; i <= x; i++) {
        z += i;
    }
    return z;
}


Some of the students solved (or tried to solve) this in the clever way instead:

int sum1(int x) {                                          int sum2(int x) {
    return x * (x + 1) / 2;                                    return x * (x - 1) / 2;
}                                                          }



To stay close to the transformation from [Nakabayashi et al. 2010] (which does not use
the return and error symbols), we consider the following translation:

                                    sum(x) → u(x, 1, 0)
                                   u(x, i, z) → u(x, i + 1, z + i) [i ≤ x]
                                   u(x, i, z) → z                  [i > x]
                                   sum1(x) → x ∗ (x + 1) div 2
                                   sum2(x) → x ∗ (x − 1) div 2

Our implementation succeeds in proving that sum(n) ≈ sum1(n) [n ≥ 0] is an in-
ductive theorem and that sum(n) ≈ sum2(n) [n ≥ 0] is not. We also succeed on the
translation using the methods in the current paper. On the other hand, the method
in [Nakabayashi et al. 2010] fails to prove or disprove these claims.

D. SOME EXAMPLES WE CANNOT HANDLE.
To demonstrate the kind of problemsPn Ctrl cannot yet handle, we compare a recursive
definition sum of the function n 7→ i=1 i with three iterative implementations.

ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:46                                                                               C. Fuhs, C. Kop, N. Nishida

 int sum(n) {                         int sum1(n) {
   if (n < 0) return 0;                 int i = 0, j = 0, sum = 0;
   return n + sum(n-1);                 for (; i <= n; i++,j++) sum += j;
 }                                      return len;
                                      }


 int sum2(int n){                     int sum3(n) {
   int i,sum=0;                         int ret = 0;
   for (i=n;i>=0;i--)                   for (int i = 0; i <= n; i++)
     sum=sum+i;                           for (int j = 0; j < i; j++) ret++;
   return sum;                          return ret;
 }                                    }
  Equivalence between sum and each of sum1, sum2 and sum3 fails for the three main
reasons discussed in § 6.2. For sum1, generalizing the initialization variables loses the
information that always i = j. For sum2, our main generalization method (§ 5.1) does
not apply because we do not recognize i = n as an initialization. For sum3, our strategy
fails because the two loop counters are generalized together.

References
A LBERT, E., A RENAS, P., G ENAIM , S., P UEBLA , G., AND Z ANARDINI , D. 2008. Removing useless variables
    in cost analysis of Java bytecode. In SAC ’08. 368–375.
A LBERT, E., G ÓMEZ -Z AMALLOA , M., H UBERT, L., AND P UEBLA , G. 2007. Verification of Java bytecode
    using analysis and transformation of logic programs. In PADL ’07. 124–139.
A LIAS, C. AND B ARTHOU, D. 2003. Algorithm recognition based on demand-driven data-flow analysis. In
    WCRE ’03. 296–305.
A LPUENTE , M., E SCOBAR , S., AND L UCAS, S. 2007. Removing redundant arguments automatically. Theory
    and Practice of Logic Programming 7, 1-2, 3–35.
AUBIN, R. 1979. Mechanizing structural induction part I: formal system. Theor. Comp. Sci. 9, 3, 329–345.
B AADER , F. AND N IPKOW, T. 1998. Term Rewriting and All That. Cambridge University Press.
B ARTHE , G., D’A RGENIO, P. R., AND R EZK , T. 2011. Secure information flow by self-composition. Mathe-
    matical Structures in Computer Science 21, 6, 1207–1252.
B ASIN, D. A. AND WALSH , T. 1992. Difference matching. In CADE ’92. 295–309.
B EYER , D., C IMATTI , A., G RIGGIO, A., K EREMOGLU, M. E., AND S EBASTIANI , R. 2009. Software model
    checking via large-block encoding. In FMCAD ’09. 25–32.
B OUHOULA , A. 1997. Automated theorem proving by test set induction. J. Symb. Comput. 23, 1, 47–77.
B OUHOULA , A. AND J ACQUEMARD, F. 2008a. Automated induction for complex data structures. Tech. Rep.
    arXiv:0811.4720 [cs.LO], CoRR. Available on http://arxiv.org/abs/0811.4720.
B OUHOULA , A. AND J ACQUEMARD, F. 2008b. Automated induction with constrained tree automata. In
    IJCAR ’08. 539–554.
B ROCKSCHMIDT, M., C OOK , B., I SHTIAQ, S., K HLAAF, H., AND P ITERMAN, N. 2016. T2: Temporal property
    verification. In TACAS ’16. 387–393.
B UNDY, A. 2001. The automation of proof by mathematical induction. In Handbook of Automated Reasoning.
    Elsevier, 845–911.
B UNDY, A., B ASIN, D., H UTTER , D., AND I RELAND, A. 2005. Rippling: Meta-Level Guidance for Mathemat-
    ical Reasoning. Cambridge University Press.
B UNDY, A., S TEVENS, A., VAN H ARMELEN, F., I RELAND, A., AND S MAILL , A. 1993. Rippling: a heuristic
    for guiding inductive proofs. Artificial Intelligence 62, 2, 185–253.
C ALCAGNO, C., D ISTEFANO, D., D UBREIL , J., G ABI , D., H OOIMEIJER , P., L UCA , M., O’H EARN, P. W., PA -
    PAKONSTANTINOU, I., P URBRICK , J., AND R ODRIGUEZ , D. 2015. Moving fast with software verification.
    In NFM ’15. 3–11.
DE M OURA , L. AND B JØRNER , N. 2008. Z3: An efficient SMT solver. In TACAS ’08. 337–340.
FALKE , S. 2009. Term rewriting with built-in numbers and collection data structures. Ph.D. thesis, Univer-
    sity of New Mexico.


                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
Verifying Procedural Programs via Constrained Rewriting Induction                                     A:47

FALKE , S. AND K APUR , D. 2009. A term rewriting approach to the automated termination analysis of
    imperative programs. In CADE ’09. 277–293.
FALKE , S. AND K APUR , D. 2012. Rewriting induction + linear arithmetic = decision procedure. In IJCAR ’12.
    241–255.
FALKE , S., K APUR , D., AND S INZ , C. 2011. Termination analysis of C programs using compiler intermediate
    languages. In RTA ’11. 41–50.
F ELSING, D., G REBING, S., K LEBANOV, V., R ÜMMER , P., AND U LBRICH , M. 2014. Automating regression
    verification. In ASE ’14. 349–360.
F UHS, C., G IESL , J., P L ÜCKER , M., S CHNEIDER -K AMP, P., AND FALKE , S. 2009. Proving termination of
    integer term rewriting. In RTA ’09. 32–47.
F URUICHI , Y., N ISHIDA , N., S AKAI , M., K USAKARI , K., AND S AKABE , T. 2008. Approach to procedural-
    program verification based on implicit induction of constrained term rewriting systems. IPSJ Trans.
    Prog. 1, 2, 100–121. In Japanese; translated summary at http://www.trs.css.i.nagoya-u.ac.jp/crisys/.
G IESL , J., A SCHERMANN, C., B ROCKSCHMIDT, M., E MMES, F., F ROHN, F., F UHS, C., H ENSEL , J., O TTO,
     C., P L ÜCKER , M., S CHNEIDER -K AMP, P., S TR ÖDER , T., S WIDERSKI , S., AND T HIEMANN, R. 2017.
    Analyzing program termination and complexity automatically with AProVE. J. Aut. Reasoning 58, 1,
    3–31.
G IESL , J., K ÜHNEMANN, A., AND V OIGTL ÄNDER , J. 2007. Deaccumulation techniques for improving prov-
    ability. J. Log. Algebr. Program. 71, 2, 79–113.
G ODLIN, B. AND S TRICHMAN, O. 2008. Inference rules for proving the equivalence of recursive procedures.
    Acta Inf. 45, 6, 403–439.
G ODLIN, B. AND S TRICHMAN, O. 2013. Regression verification: proving the equivalence of similar programs.
    Softw. Test., Verif. Reliab. 23, 3, 241–258.
G UPTA , A., P OPEEA , C., AND R YBALCHENKO, A. 2011. Predicate abstraction and refinement for verifying
    multi-threaded programs. In POPL ’11. 331–344.
H AWBLITZEL , C., K AWAGUCHI , M., L AHIRI , S. K., AND R EB ÊLO, H. 2013. Towards modularly comparing
    programs using automated theorem provers. In CADE ’13. 282–299.
H UET, G. P. AND H ULLOT, J.-M. 1982. Proofs by induction in equational theories with constructors. Journal
    of Computer and System Sciences 25, 2, 239–266.
H UTH , M. AND R YAN, M. 2000. Logic in Computer Science: Modelling and Reasoning about Systems. Cam-
    bridge University Press.
K APUR , D. AND S AKHANENKO, N. A. 2003. Automatic generation of generalization lemmas for proving
    properties of tail-recursive definitions. In TPHOLs ’03. 136–154.
K APUR , D. AND S UBRAMANIAM , M. 1996. Lemma discovery in automated induction. In CADE ’96. 538–552.
K OIKE , H. AND T OYAMA , Y. 2000. Comparison between inductionless induction and rewriting induction.
    Comp. Soft. 17, 6, 1–12. In Japanese.
K OP, C. 2013. Termination of LCTRSs. In WST ’13. 59–63.
K OP, C. 2017. Quasi-reductivity of Logically Constrained Term Rewriting Systems. Tech. Rep.
    arXiv:1702.02397 [cs.LO], CoRR. Available on https://arxiv.org/abs/1702.02397.
K OP, C. AND N ISHIDA , N. 2013. Term rewriting with logical constraints. In FroCoS ’13. 343–358.
K OP, C. AND N ISHIDA , N. 2014. Automatic constrained rewriting induction towards verifying procedural
    programs. In APLAS ’14. 334–353.
K OP, C. AND N ISHIDA , N. 2015. ConsTrained Rewriting tooL. In LPAR ’15. 549–557.
K UNDU, S., T ATLOCK , Z., AND L ERNER , S. 2009. Proving optimizations correct using parameterized pro-
    gram equivalence. In PLDI ’09. 327–337.
L AHIRI , S. K., H AWBLITZEL , C., K AWAGUCHI , M., AND R EB ÊLO, H. 2012. SYMDIFF: A language-agnostic
    semantic diff tool for imperative programs. In CAV ’12. 712–717.
L OPES, N. P. AND M ONTEIRO, J. 2016. Automatic equivalence checking of programs with uninterpreted
    functions and integer arithmetic. Int. J. Softw. Tools Technol. Transfer 18, 4, 359–374.
M C C ARTHY, J. 1960. Recursive functions of symbolic expressions and their computation by machine, part I.
    Commun. ACM 3, 4, 184–195.
N AKABAYASHI , N., N ISHIDA , N., K USAKARI , K., S AKABE , T., AND S AKAI , M. 2010. Lemma generation
    method in rewriting induction for constrained term rewriting systems. Computer Software 28, 1, 173–
    189. In Japanese; translation at http://www.trs.css.i.nagoya-u.ac.jp/crisys/.
N ECULA , G. C. 2000. Translation validation for an optimizing compiler. In PLDI ’00. 83–94.
N IEUWENHUIS, R., O LIVERAS, A., AND T INELLI , C. 2006. Solving SAT and SAT modulo theories: From an
    abstract Davis–Putnam–Logemann–Loveland procedure to DPLL(T). J. ACM 53, 6, 937–977.


ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
A:48                                                                               C. Fuhs, C. Kop, N. Nishida

O TTO, C., B ROCKSCHMIDT, M., VON E SSEN, C., AND G IESL , J. 2010. Automated termination analysis of
    Java bytecode by term rewriting. In RTA ’10. 259–276.
P NUELI , A., S IEGEL , M., AND S INGERMAN, E. 1998. Translation validation. In TACAS ’98. 151–166.
R EDDY, U. S. 1990. Term rewriting induction. In CADE ’90. 162–177.
S AKATA , T., N ISHIDA , N., AND S AKABE , T. 2011. On proving termination of constrained term rewrite sys-
    tems by eliminating edges from dependency graphs. In WFLP ’11. 138–155.
S AKATA , T., N ISHIDA , N., S AKABE , T., S AKAI , M., AND K USAKARI , K. 2009. Rewriting induction for con-
    strained term rewriting systems. IPSJ Trans. Prog. 2, 2, 80–96. In Japanese; a translated summary is
    available at http://www.trs.css.i.nagoya-u.ac.jp/crisys/.
S POTO, F., L U, L., AND M ESNARD, F. 2009. Using CLP simplifications to improve Java bytecode termination
    analysis. Electr. Notes Theor. Comput. Sci. 253, 5, 129–144.
SV-COMP. Competition on software verification. http://sv-comp.sosy-lab.org/.
T ERAUCHI , T. AND A IKEN, A. 2005. Secure information flow as a safety problem. In SAS ’05. 352–367.
U RSO, P. AND K OUNALIS, E. 2004. Sound generalizations in mathematical induction. Theor. Comput.
    Sci. 323, 1-3, 443–471.
V ERDOOLAEGE , S., J ANSSENS, G., AND B RUYNOOGHE , M. 2012. Equivalence checking of static affine pro-
    grams using widening to handle recurrences. ACM Trans. Program. Lang. Syst. 34, 3, 11.
V UJOSEVIC -J ANICIC, M., N IKOLIC, M., T OSIC, D., AND K UNCAK , V. 2013. Software verification and graph
    similarity for automated evaluation of students’ assignments. Inf. & Softw. Technology 55, 6, 1004–1016.
WALSH , T. 1996. A divergence critic for inductive proof. J. Artificial Intelligence Research 4, 209–235.




                          ACM Transactions on Computational Logic, Vol. V, No. N, Article A, Publication date: YYYY.
