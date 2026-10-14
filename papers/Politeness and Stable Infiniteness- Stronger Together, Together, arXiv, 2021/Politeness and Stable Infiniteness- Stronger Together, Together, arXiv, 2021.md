                                             Politeness and Stable Infiniteness: Stronger
                                                              Together

                                                    Ying Sheng1 , Yoni Zohar1 , Christophe Ringeissen2 ,
                                                   Andrew Reynolds3 , Clark Barrett1 , and Cesare Tinelli3
arXiv:2104.11738v2 [cs.LO] 27 Apr 2021




                                                                         1
                                                                             Stanford University
                                               2
                                                   Université de Lorraine, CNRS, Inria, LORIA, F-54000 Nancy, France
                                                                         3
                                                                           The University of Iowa



                                               Abstract. We make two contributions to the study of polite combina-
                                               tion in satisfiability modulo theories. The first is a separation between
                                               politeness and strong politeness, by presenting a polite theory that is not
                                               strongly polite. This result shows that proving strong politeness (which
                                               is often harder than proving politeness) is sometimes needed in order to
                                               use polite combination. The second contribution is an optimization to
                                               the polite combination method, obtained by borrowing from the Nelson-
                                               Oppen method. The Nelson-Oppen method is based on guessing arrange-
                                               ments over shared variables. In contrast, polite combination requires an
                                               arrangement over all variables of the shared sorts. We show that when
                                               using polite combination, if the other theory is stably infinite with respect
                                               to a shared sort, only the shared variables of that sort need be considered
                                               in arrangements, as in the Nelson-Oppen method. The time of reason-
                                               ing about arrangements is exponential in the worst case, so reducing the
                                               number of variables considered has the potential to improve performance
                                               significantly. We show preliminary evidence for this by demonstrating a
                                               speed-up on a smart contract verification benchmark.


                                         1   Introduction

                                         Solvers for satisfiability modulo theories (SMT) [4] are used in a wide variety
                                         of applications. Many of these applications require determining the satisfiability
                                         of formulas with respect to a combination of background theories. In order to
                                         make reasoning about combinations of theories modular and easily extensible,
                                         a combination framework is essential. Combination frameworks provide mecha-
                                         nisms for automatically deriving a decision procedure for the combined theories
                                         by using the decision procedures for the individual theories as black boxes. To
                                         integrate a new theory into such a framework, it then suffices to focus on the de-
                                         coupled decision procedure for the new theory alone, together with its interface
                                         to the generic combination framework.
                                             In 1979, Nelson and Oppen [17] proposed a general framework for combining
                                         theories with disjoint signatures. In this framework, a quantifier-free formula in
                                         the combined theory is purified to a conjunction of formulas, one for each theory.
                                         Each pure formula is then sent to a dedicated theory solver, along with a guessed
arrangement (a set of equalities and disequalities that capture an equivalence re-
lation) of the variables shared among the pure formulas. For completeness [16],
this method requires all component theories to be stably infinite. While many
important theories are stably infinite, some are not, including the widely-used
theory of fixed-length bit-vectors. To address this issue, the polite combination
method was introduced by Ranise et al. [18], and later refined by Jovanovic
and Barrett [13]. In polite combination, one theory must be polite, a stronger
requirement than stable-infiniteness, but the requirement on the other theory is
relaxed: specifically, it need not be stably infinite. The price for this generality is
that unlike the Nelson-Oppen method, polite combination requires guessing ar-
rangements over all variables of certain sorts, not just the shared ones. At a high
level, polite theories have two properties: smoothness and finite witnessability
(see Section 2). The polite combination theorem in [18] contained an error, which
was identified in [13]. A fix was also proposed in [13], which relies on stronger
requirements for finite witnessability. Following Casal and Rasga [9], we call this
strengthened version strong finite witnessability. A theory that is both smooth
and strongly finitely witnessable is called strongly polite.
    This paper makes two contributions. First, we give an affirmative answer to
the question of whether politeness and strong politeness are different notions, by
giving an example of a theory that is polite but not strongly polite. The given
theory is over an empty signature and has two sorts, and was originally studied
in [9] in the context of shiny theories. Here we state and prove the separation
of politeness and strong politeness, without using shiny theories. Proving that a
theory is strongly polite is harder than proving that it is just polite. This result
shows that the additional effort is sometimes needed in order to be able to use the
combination theorem from [13]. We show that for empty signatures, at least two
sorts are needed to present a polite theory that is not strongly polite. However,
for the empty signature with only one sort, there is a finitely witnessable theory
that is not strongly finite witnessable. Such a theory cannot be smooth.
    Second, we explore different polite combination scenarios, where additional
information is known about the theories being combined. In particular, we im-
prove the polite combination method for the case where one theory is strongly
polite w.r.t. a set S of sorts and the other is stably infinite w.r.t. a subset S ′ ⊆ S
of the sorts. For such cases, we show that it is possible to perform Nelson-Oppen
combination for S ′ and polite combination for S \ S ′ . This means that for the
sorts in S ′ , only shared variables need to be considered for the guessed arrange-
ment, which can considerably reduce its size. We also show that the set of shared
variables can be reduced for a couple of other variations of conditions on the the-
ories. Finally, we present a preliminary case study using a challenge benchmark
from a smart contract verification application. We show that the reduction of
shared variables is evident and significantly improves the solving time. Verifica-
tion of smart contracts using SMT, and in particular the analyzed benchmark,
are the main motivation behind the second contribution of this paper.

Related Work: Polite combination is part of a more general effort to replace the
stable infiniteness symmetric condition in the Nelson-Oppen approach with a

                                          2
weaker condition. Other examples of this effort include the notions of shiny [22],
parametric [14], and gentle [12] theories. Gentle, shiny and polite theories can
be combined à la Nelson-Oppen with any arbitrary theory. Shiny theories were
introduced by Tinelli and Zarba [22] as a class of mono-sorted theories. Based
on the same principles as shininess, politeness is particularly well-suited to deal
with theories expressed in many-sorted logic. Polite theories were introduced by
Ranise et al. [18] to provide a more effective combination approach compared
to parametric and shiny theories, the former requiring solvers to reason about
cardinalities and the latter relying on expensive computations of minimal car-
dinalities of models. Shiny theories were extended to many-sorted signatures
in [18], where there is a sufficient condition for their equivalence with polite
theories. For the mono-sorted case, a sufficient condition for the equivalence of
shiny theories and strongly polite theories was given by Casal and Rasga [8].
In later work [9], the same authors proposed a generalization of shiny theories
to many-sorted signatures different from the one in [18], and proved that it is
equivalent to strongly polite theories with a decidable quantifier-free fragment.
The strong politeness of the theory of algebraic datatypes [5] was proven in [19].
That paper also introduced additive witnesses, that provided a sufficient con-
dition for a polite theory to be also strongly polite. In this paper we present a
theory that is polite but not strongly polite. In accordance with [19], the witness
that we provide for this theory is not additive.
    The paper is organized as follows. Section 2 provides the necessary notions
from first-order logic and polite theories. Section 3 discusses the difference be-
tween politeness and strong politeness and shows they are not equivalent. Sec-
tion 4 gives the improvements for the combination process under certain condi-
tions, and Section 5 demonstrates the effectiveness of these improvements for a
challenge benchmark. 4


2     Preliminaries
2.1    Signatures and Structures
We briefly review the usual definitions of many-sorted first-order logic with
equality (see [11,20] for more details). A signature Σ consists of a set SΣ (of
sorts), a set FΣ of function symbols, and a set PΣ of predicate symbols. We as-
sume SΣ , FΣ and PΣ are countable. Function symbols have arities of the form
σ1 × . . . × σn → σ, and predicate symbols have arities of the form σ1 × . . . × σn ,
with σ1 , . . . , σn , σ ∈ SΣ . For each sort σ ∈ SΣ , PΣ includes an equality symbol
=σ of arity σ × σ. We denote it by = when σ is clear from context. When =σ
are the only symbols in Σ, we say that Σ is empty. If two signatures share no
symbols except =σ we call them disjoint. We assume an underlying countably
infinite set of variables for each sort. Terms, formulas, and literals are defined in
the usual way. For a Σ-formula φ and a sort σ, we denote the set of free variables
in φ of sort σ by vars σ (φ). This notation naturally extends to vars S (φ) when S
4
    The appendix contains proofs that are omitted from the main text.


                                          3
is a set of sorts. vars (φ) is the set of all free variables in φ. We denote by QF (Σ)
the set of quantifier-free Σ-formulas.
    A Σ-structure is a many-sorted structure that provides semantics for the
symbols in Σ (but not for variables). It consists of a domain σ A for each sort
σ ∈ SΣ , an interpretation f A for every f ∈ FΣ , as well as an interpretation P A
for every P ∈ PΣ . We further require that =σ be interpreted as the identity
relation over σ A for every σ ∈ SΣ . A Σ-interpretation A is an extension of a
Σ-structure with interpretations for some set of variables. For any Σ-term α,
αA denotes the interpretation of α in A. When α is a set of Σ-terms, αA =
  xA | x ∈ α . Satisfaction is defined as usual. A |= ϕ denotes that A satisfies ϕ.


    A Σ-theory T is a class of all Σ-structures that satisfy some set Ax of
Σ-sentences. For each such set Ax, we say that T is axiomatized by Ax. A Σ-
interpretation whose variable-free part is in T is called a T -interpretation. A
Σ-formula φ is T -satisfiable if A |= φ for some T -interpretation A. A set A of
Σ-formulas is T -satisfiable if A |= φ for every φ ∈ A. Two formulas φ and ψ are
T -equivalent if they are satisfied by the same T -interpretations.
    Note that for any class C of Σ-structures there is a theory TC that corresponds
to it, with the same satisfiable formulas: the Σ-theory axiomatized by the set
Ax of Σ-sentences that are satisfied in every structure of C. In the examples that
follow, we define theories TC implicitly by specifying only the class C, as done in
the SMT-LIB 2 standard [3]. This can be done without loss of generality.5
Example 1. Let ΣList be a signature of finite lists containing the sorts elem1 ,
elem2 , and list, as well as the function symbols cons of arity elem1 ×elem2 ×list →
list, car1 of arity list → elem1 , car2 of arity list → elem2 , cdr of arity list → list,
and nil of arity list. The ΣList -theory TList corresponds to an SMT-LIB 2 theory
of algebraic datatypes [3,5], where elem1 and elem2 are interpreted as some sets
(of “elements”), and list is interpreted as finite lists of pairs of elements, one
from elem1 and the other from elem2 . cons is a list constructor that takes two
elements and a list, and inserts the two elements at the head of the list. The
pair (car1 (l), car2 (l)) is the first entry in l, and cdr(l) is the list obtained from l
by removing its first entry. nil is the empty list.                                    ⊓
                                                                                       ⊔
Example 2. The signature ΣInt includes a single sort int, all numerals 0, 1, . . .,
the function symbols +, − and · of arity int × int → int and the predicate
symbols < and ≤ of arity int × int. The ΣInt -theory TInt corresponds to integer
arithmetic in SMT-LIB 2, and the interpretation of the symbols is the same as
in the standard structure of the integers. The signature ΣBV4 includes a single
sort BV4 and various function and predicate symbols for reasoning about bit-
vectors of length 4 (such as & for bit-wise and, constants of the form 0110, etc.).
The ΣBV4 -theory TBV4 corresponds to SMT-LIB 2 bit-vectors of size 4, with the
expected semantics of constants and operators.                                   ⊓
                                                                                 ⊔
    Let Σ1 , Σ2 be signatures, T1 a Σ1 -theory, and T2 a Σ2 -theory. The combina-
tion of T1 and T2 , denoted T1 ⊕ T2 , consists of all Σ1 ∪Σ2 -structures A, such that
AΣ1 is in T1 and AΣ2 is in T2 , where AΣi is the reduct of A to Σi for i ∈ {1, 2}.
5
    For further discussion on this point, see Appendix A.1.


                                             4
Example 3. Let TIntBV4 be TInt ⊕ TBV4 . It is the combined theory of integers and
bit-vectors. It has all the sorts and operators from both theories. If we rename
the sorts elem1 and elem2 of ΣList to int and BV4, respectively, we can obtain a
theory TListIntBV4 defined as TIntBV4 ⊕ TList . This is the theory of lists of pairs,
where each pair consists of an integer and a bit-vector of size 4.                 ⊓
                                                                                   ⊔

      The following definitions and theorems will be useful in the sequel.

Theorem 1 (Theorem 9 of [20]). Let Σ be a signature, and A a set of Σ-
formulas that is satisfiable. Then there exists an interpretation A that satisfies
A, in which σ A is countable whenever it is infinite.6

      The following theorem from [13] is a variant of a theorem from [21].

Definition 1 (Arrangement). Let V be a finite set of variables whose sorts
are in S and let {Vσ | σ ∈ S} be a partition of V such that Vσ is the set of
variables of sort σ in V . A formula δ is an arrangement of V if
                      ^       ^                        ^
                 δ=       (          (x = y) ∧                      (x 6= y)) ,
                      σ∈S (x,y)∈Eσ               x,y∈Vσ ,(x,y)∈E
                                                              / σ


where Eσ is some equivalence relation over Vσ for each σ ∈ S.

Theorem 2 (Theorem 2.5 of [13]). For i = 1, 2, let Σi be disjoint signatures,
Si = SΣi with S = S1 ∩ S2 , Ti be a Σi -theory, Γi be a set of Σi -literals, and
V = vars (Γ1 )∩vars (Γ2 ). If there exist a T1 -interpretation A, a T2 interpretation
B, and an arrangement δV of V such that: 1. A |= Γ1 ∪ δV ; 2. B |= Γ2 ∪ δV ;
and 3. |Aσ | = |Bσ | for every σ ∈ S, then Γ1 ∪ Γ2 is T1 ⊕ T2 -satisfiable.


2.2     Polite Theories

We now give the background definitions necessary for both Nelson-Oppen and
polite combination. In what follows, Σ is an arbitrary (many-sorted) signature,
S ⊆ SΣ , and T is a Σ-theory. We start with stable infiniteness and smoothness.

Definition 2 (Stably Infinite). T is stably infinite with respect to S if ev-
ery quantifier-free Σ-formula that is T -satisfiable is also satisfiable in a T -
interpretation A in which σ A is infinite for every σ ∈ S.

Definition 3 (Smooth). T is smooth w.r.t. S if for every quantifier-free for-
mula φ, T -interpretation A that satisfies φ, and function κ from S to the class of
cardinals such that κ(σ) ≥ σ A for every σ ∈ S, there exists a T -interpretation
                               ′
A′ that satisfies φ with σ A = κ(σ) for every σ ∈ S.

6
    In [20] this was proven more generally, for ordered sorted logics.


                                             5
We identify singleton sets with their single elements when there is no ambiguity
(e.g., when saying that a theory is smooth w.r.t. a sort σ).
    We next define politeness and related concepts, following the presentation
in [19]. Let φ be a quantifier-free Σ-formula. A Σ-interpretation A finitely wit-
nesses φ for T w.r.t. S (or, is a finite witness of φ for T w.r.t. S), if A |= φ
and σ A = vars σ (φ)A for every σ ∈ S. We say that φ is finitely witnessed for
T w.r.t. S if it is either T -unsatisfiable or has a finite witness for T w.r.t. S.
We say that φ is strongly finitely witnessed for T w.r.t. S if φ ∧ δV is finitely
witnessed for T w.r.t. S for every arrangement δV of V , where V is any set of
variables whose sorts are in S. A function wit : QF (Σ) → QF (Σ) is a (strong)
witness for T w.r.t. S if for every φ ∈ QF (Σ) we have that: 1. φ and ∃ −→
                                                                         w . wit (φ)
                       →
                       −
are T -equivalent for w = vars (wit (φ)) \ vars (φ); and 2. wit (φ) is (strongly)
finitely witnessed for T w.r.t. S. T is (strongly) finitely witnessable w.r.t. S if
there exists a computable (strong) witness for T w.r.t. S. T is (strongly) polite
w.r.t. S if it is smooth and (strongly) finitely witnessable w.r.t. S.


3     Politeness and Strong Politeness
In this section we study the difference between politeness and strong politeness.
Since the introduction of strong politeness in [13], it has been unclear whether
it is strictly stronger than politeness, that is, whether there exists a theory
that is polite but not strongly polite. We present an example of such a theory,
answering the open question affirmatively. This result is followed by further
analysis of notions related to politeness. This section is organized as follows.
In Section 3.1 we reformulate an example given in [13], showing that there are
witnesses that are not strong witnesses. We then present a polite theory that
is not strongly polite in Section 3.2. The theory is over a signature with two
sorts but is otherwise empty. We show in Section 3.3 that politeness and strong
politeness are equivalent for empty signatures with a single sort. Finally, we show
in Section 3.4 that this equivalence does not hold for finite witnessability alone.

3.1    Witnesses vs. Strong witnesses
In [13] an example was given for a witness that is not strong. We reformulate this
example in terms of the notions that are defined in the current paper, that is,
witnessed formulas are not the same as strongly witnessed formulas (Example 4),
and witnesses are not the same as strong witnesses (Example 5).

Example 4. Let Σ0 be a signature with a single sort σ and no function or pred-
icate symbols, and let T0 be a Σ0 -theory consisting of all Σ0 -structures with at
least two elements. Let φ be the formula x = x ∧ w = w. This formula is finitely
witnessed for T0 w.r.t. σ, but not strongly. Indeed, for δV ≡ (x = w), φ ∧ δV is
not finitely witnessed for T0 w.r.t. σ: a finite witness would be required to have
only a single element and would therefore not be a T0 -interpretation.           ⊓
                                                                                 ⊔
The next example shows that witnesses and strong witnesses are not equivalent.

                                         6
Example 5. Take Σ0 , σ, and T0 as in Example 4, and define wit (φ) as the function
(φ ∧ w1 = w1 ∧ w2 = w2 ) for fresh w1 , w2 . The function is a witness for T0
w.r.t. σ. However, it is not a strong witness for T w.r.t. σ.                    ⊓
                                                                                 ⊔
   Although the theory T0 in the above examples does serve to distinguish for-
mulas and witnesses that are and are not strong, it cannot be used to do the
same for theories themselves. This is because T0 is, in fact, strongly polite, via
a different witness function.
Example 6. The function wit ′ (φ) = (φ ∧ w1 6= w2 ), for some w1 , w2 ∈
                                                                      / vars σ (φ),
is a strong witness for T0 w.r.t. S, as proved in [13].                          ⊓
                                                                                 ⊔
A natural question, then, is whether there is a theory that can separate the two
notions of politeness. The following subsection provides an affirmative answer.

3.2     A Polite Theory that is not Strongly Polite
Let Σ2 be a signature with two sorts σ1 and σ2 and no function or predicate
symbols (except =). Let T2,3 be the Σ2 -theory from [9], consisting of all Σ2 -
structures A such that either σ1A = 2 ∧ σ2A ≥ ℵ0 or σ1A ≥ 3 ∧ σ2A ≥ 3 [9].7
    T2,3 is polite, but is not strongly polite. Its smoothness is shown by extending
any given structure with new elements as much as necessary.
Lemma 1. T2,3 is smooth w.r.t. {σ1 , σ2 }.
      For finite witnessability, consider the function wit defined as follows:
    wit (φ) := φ ∧ x1 = x1 ∧ x2 = x2 ∧ x3 = x3 ∧ y1 = y1 ∧ y2 = y2 ∧ y3 = y3         (1)
for fresh variables x1 , x2 , and x3 of sort σ1 and y1 , y2 , and y3 of sort σ2 . It can
be shown that wit is a witness for T2,3 but there is no strong witness for it.
Lemma 2. T2,3 is finitely witnessable w.r.t. {σ1 , σ2 }.

Lemma 3. T2,3 is not strongly finitely witnessable w.r.t. {σ1 , σ2 }.
    Lemmas 1 to 3 have shown that T2,3 is polite but is not strongly polite. And
indeed, using the polite combination method from [13] with this theory can cause
problems. Consider the theory T1,1 that consists of all Σ2 -structures A such that
 σ1A = σ2A = 1. Clearly, T1,1 ⊕T2,3 is empty, and hence no formula is T1,1 ⊕T2,3 -
satisfiable. However, denote the formula true by Γ1 and V            the formula x = x by
Γ2 for some variable x of sort σ1 . Then wit (Γ2 ) is x = x ∧ 3i=1 xi = xi ∧ yi = yi .
Let δ be the arrangement x = x1 = x2 = x3 ∧ y1 = y2 = y3 . It can be shown that
wit (Γ2 ) ∧ δ is T2,3 -satisfiable and Γ1 ∧ δ is T1,1 -satisfiable. Hence the combination
method of [13] would consider Γ1 ∧ Γ2 to be T1,1 ⊕ T2,3 -satisfiable, which is
impossible. Hence the fact that T2,3 is not strongly polite propagates all the way
to the polite combination method.8
7
  In [9], the first condition is written σ1A ≥ 2. We use equality as this is equivalent
  and we believe it makes things clearer.
8
  Notice that T2,3 can ben axiomatized  o using the following set of axioms, given the
                               σ1    σ2      σ1      σ2
  definitions in Figure 1: ψ≥2    , ψ≥3  ∪ {ψ=2 → ¬ψ=n   | n ≥ 3}


                                           7
                                                         ^
                      distinct (x1 , . . . , xn ) :=              xi 6= xj
                                                       1≤i<j<=n
                        σ
                       ψ≥n := ∃x1 , . . . , xn .distinct (x1 , . . . , xn )
                                                          n
                                                          _
                            σ
                           ψ≤n := ∃x1 , . . . , xn .∀y.       y = xi
                                                  i=1
                                     σ      σ     σ
                                    ψ=n := ψ≥n ∧ ψ≤n

  Fig. 1. Cardinality formulas for sort σ. All variables are assumed to have sort σ.




Remark 1. An alternative way to separate politeness from strong politeness us-
ing T2,3 can be obtained through shiny theories, as follows. Shiny theories were
introduced in [22] for the mono-sorted case, and were generalized to many-sorted
signatures in two different ways in [9] and [18]. In [9], T2,3 was introduced as a
theory that is shiny according [18], but not according to [9]. Theorem 1 of [9]
states that their notion of shininess is equivalent to strong politeness for theories
in which the satisfiability problem for quantifier-free formulas is decidable. Since
this is the case for T2,3 , and since it is not shiny according to [9], we get that
T2,3 is not strongly polite. Further, Proposition 18 of [18] states that every shiny
theory (according to their definition) is polite. Hence we get that T2,3 is polite
but not strongly polite.
    We have (and prefer) a direct proof based only on politeness, without a detour
through shininess. Note also that [9] dealt only with strongly polite theories and
did not study the weaker notion of polite theories. In particular, the fact that
strong politeness is different from politeness was not stated nor proved there.


3.3   The Case of Mono-sorted Polite Theories

Theory T2,3 includes two sorts, but is otherwise empty. In this section we show
that requiring two sorts is essential for separating politeness from strong polite-
ness in otherwise empty signatures. That is, we prove that politeness implies
strong politeness otherwise. Let Σ0 be the signature with a single sort σ and
no function or predicate symbols (except =), We show that smooth Σ0 -theories
have a certain form, and conclude strong politeness from politeness.

Lemma 4. Let T be a Σ0 -theory. If T is smooth w.r.t. σ and includes a finite
                                σ
structure, T is axiomatized by ψ≥n from Figure 1 for some n > 0.

Proposition 1. If T is a Σ0 -theory that is polite w.r.t. σ, then it is strongly
polite w.r.t. σ.

Remark 2. We again note (as we did in Remark 1) that an alternative way
to obtain this result is via shiny theories, using [18], which introduced polite
theories, as well as [7], which compared strongly polite theories to shiny theories

                                                8
in the mono-sorted case. Specifically, in the presence of a single sort, Proposition
19 of [18] states that:
 (∗) every polite theory over a finite signature such that it is decidable
      whether a finite structure is a member of the theory, is shiny.
In turn, Proposition 1 of [7] states that:
 (∗∗) every shiny theory over a mono-sorted signature with a decidable sat-
      isfiability problem for quantifier-free formulas, is also strongly polite.
It can be shown that for every polite Σ0 -theory it is decidable whether a finite
structure is in the theory. It can also be shown that satisfiability of quantifier-free
formulas is decidable for such theories. Using (∗) and (∗∗), we get that in Σ0 -
theories, politeness implies strong politeness. Similarly to Remark 1, we prefer
a direct route for showing this result, without going through shiny theories.


3.4    Mono-sorted Finite witnessability

We have seen that for Σ0 -theories, politeness and strong politeness are the same.
Now we show that smoothness is crucial for this equivalence, i.e., that there is
no such equivalence between finite witnessability and strong finite witnessability.
       ∞
Let TEven  be the Σ0 -theory of all Σ0 -structures A such that σ A is even or
         9
infinite. Clearly, this theory is not smooth.
          ∞
Lemma 5. TEven is not smooth w.r.t. σ.
                                          ∞
    We can construct a witness wit for TEven  as follows. Let φ be a quantifier-free
Σ0 -formula, and let E be the set of all equivalence relations over vars (φ) ∪ {w}
for some fresh variable w. Let even(E) be the set of all equivalence W relations in
E with an even number of equivalence classes. Then, wit (φ) is φ ∧ e∈even(E) δe ,
where for each e ∈ even(E), δe is the arrangement induced by e:
                     ^                       ^
                         x=y ∧                             x 6= y
                    (x,y)∈e         x,y∈vars (φ)∪{w}∧(x,y)6∈e

                                                        ∞
It can be shown that wit is indeed a witness, and that TEven has no strong
witness, similarly to Lemma 3.
          ∞
Lemma 6. TEven is finitely witnessable w.r.t. σ.
          ∞
Lemma 7. TEven is not strongly finitely witnessable w.r.t. σ.


4     A Blend of Polite and Stably-Infinite Theories

In this section, we show that the polite combination method can be optimized
to reduce the search space of possible arrangements. In what follows, Σ1 and Σ2
are disjoint signatures, S = SΣ1 ∩ SΣ2 , T1 is a Σ1 -theory, T2 is a Σ2 -theory, Γ1
is a set of Σ1 -literals, and Γ2 is a set of Σ2 -literals.
9                ∞                                        σ
    Notice that TEven can be axiomatized using the set {¬ψ=2n+1 | n ∈ N}.


                                          9
    The Nelson-Oppen procedure reduces the T1 ⊕ T2 -satisfiability of Γ1 ∪ Γ2
to the existence of an arrangement δ over the set V = vars S (Γ1 ) ∩ vars S (Γ2 ),
such that Γ1 ∪ δ is T1 -satisfiable and Γ2 ∪ δ is T2 -satisfiable. The correctness of
this reduction relies on the fact that both theories are stably infinite w.r.t. S. In
contrast, the polite combination method only requires a condition (namely strong
politeness) from one of the theories, while the other theory is unrestricted and,
in particular, not necessarily stably infinite. In polite combination, the T1 ⊕ T2 -
satisfiability of Γ1 ∪ Γ2 is again reduced to the existence of an arrangement δ,
but over a different set V ′ = vars S (wit (Γ2 )), such that Γ1 ∪ δ is T1 -satisfiable
and wit (Γ2 ) ∪ δ is T2 -satisfiable, where wit is a strong witness for T2 w.r.t. S.
Thus, the flexibility offered by polite combination comes with a price. The set
V ′ is potentially larger than V as it contains all variables with sorts in S that
occur in wit (Γ2 ), not just those that also occur in Γ1 . Since the search space
of arrangements over a set grows exponentially with its size, this difference can
become crucial. If T1 happens to be stably infinite w.r.t. S, however, we can fall
back to Nelson-Oppen combination and only consider variables that are shared
by the two sets. But what if T1 is stably infinite only w.r.t. to some proper subset
S ′ ⊂ S? Can this knowledge about T1 help in finding some set V ′′ of variables
between V and V ′ , such that we need only consider arrangements of V ′′ ? In this
section we prove that this is possible by taking V ′′ to include only the variables
of sorts in S ′ that are shared between Γ1 and wit (Γ2 ), and all the variables of
sorts in S \ S ′ that occur in wit (Γ2 ). We also identify several weaker conditions
on T2 that are sufficient for the combination theorem to hold.

4.1    Refined Combination Theorem
To put the discussion above in formal terms, we recall the following theorem.
Theorem 3 ([13]). If T2 is strongly polite w.r.t. S with a witness wit , then
the following are equivalent: 1. Γ1 ∪ Γ2 is (T1 ⊕ T2 )-satisfiable; 2. there exists an
arrangement δV over V , such
                          S that Γ1 ∪ δV is T1 -satisfiable and wit (Γ2 ) ∪ δV is
T2 -satisfiable, where V = σ∈S Vσ , and Vσ = vars σ (wit (Γ2 )) for each σ ∈ S.
    Our goal is to identify general cases in which information regarding T1 can
help reduce the size of the set V . We extend the definitions of stably infinite,
smooth, and strongly finitely witnessable to two sets of sorts rather than one.
Roughly speaking, in this extension, the usual definition is taken for the first
set, and some cardinality-preserving constraints are enforced on the second set.
Definition 4. Let Σ be a signature, S1 , S2 two disjoint subsets of SΣ , and T a
Σ-theory.
    T is (strongly) stably infinite w.r.t. (S1 , S2 ) if for every quantifier-free Σ-
formula φ and T -interpretation A satisfying φ, there exists a T -interpretation B
such that B |= φ, |σ B | is infinite for every σ ∈ S1 , and |σ B | ≤ |σ A | (|σ B | = |σ A |)
for every σ ∈ S2 .
    T is smooth w.r.t. (S1 , S2 ) if for every quantifier-free Σ-formula φ, T -
interpretation A satisfying φ, and function κ from S1 to the class of cardinals

                                             10
such that κ(σ) ≥ σ A for each σ ∈ S1 , there exists a T -interpretation B that
satisfies φ, with σ B = κ(σ) for each σ ∈ S1 , and with σ B infinite whenever
 σ A is infinite for each σ ∈ S2 .
    T is strongly finitely witnessable w.r.t. (S1 , S2 ) if there exists a computable
function wit : QF (Σ) → QF (Σ) such that for every quantifier-free Σ-formula φ:
1. φ and ∃ −→
            w . wit (φ) are T -equivalent for −
                                              →
                                              w = vars (wit (φ)) \ vars (φ); and 2. for
every T -interpretation A and arrangement δ of any set of variables whose sorts
are in S1 , if A satisfies wit (φ) ∧ δ, then there exists a T -interpretation B that
finitely witnesses wit (φ) ∧ δ w.r.t. S1 and for which σ B is infinite whenever
 σ A is infinite, for each σ ∈ S2 .

Our main result is the following.

Theorem 4. Let S si ⊆ S and S nsi = S \ S si . Suppose T1 is stably infinite
w.r.t. S si and one of the following holds:

1. T2 is strongly stably infinite w.r.t. (S si , S nsi ) and strongly polite w.r.t. S nsi
   with a witness wit .
2. T2 is stably infinite w.r.t. (S si , S nsi ), smooth w.r.t. (S nsi , S si ), and strongly
   finitely witnessable w.r.t. S nsi with a witness wit .
3. T2 is stably infinite w.r.t. S si and both smooth and strongly finitely-witnessable
   w.r.t. (S nsi , S si ) with a witness wit .

Then the following are equivalent: 1. Γ1 ∪Γ2 is (T1 ⊕T2 )-satisfiable; 2. There exists
an arrangement δV over VSsuch that Γ1 ∪δV is T1 -satisfiable, and wit (Γ2 )∪δV is
T2 -satisfiable, where V = σ∈S Vσ , with Vσ = vars σ (wit (Γ2 )) for every σ ∈ S nsi
and Vσ = vars σ (Γ1 ) ∩ vars σ (wit (Γ2 )) for every σ ∈ S si .

    All three items of Theorem 4 include assumptions that guarantee that the two
theories agree on cardinalities of shared sorts. For example, in the first item, we
first shrink the S nsi -domains of the T2 -model using strong finite witnessability,
and then expand them using smoothness. But then, to obtain infinite domains
for the S si sorts, stable infiniteness is not enough, as we need to maintain the
cardinalities of the S nsi domains while making the domains of the S si sorts
infinite. For this, the stronger property of strong stable infiniteness is used.
    The formal proof of this theorem is provided in Section 4.2, below. Figure 2
is a visualization of the claims in Theorem 4. The theorem considers two variants
of strong finite witnessability, two variants of smoothness, and three variants of
stable infiniteness. For each of the three cases of Theorem 4, Figure 2 shows
which variant of each property is assumed. The height of each bar corresponds
to the strength of the property. In the first case, we use ordinary strong finite
witnessability and smoothness, but the strongest variant of stable infiniteness;
in the second, we use ordinary strong finite witnessability with the new variants
of stable infiniteness and smoothness; and for the third, we use ordinary stable
infiniteness and the stronger variants of strong finite witnessability and smooth-
ness. The order of the bars corresponds to the order of their usage in the proof of
each case. The stage at which stable infiniteness is used determines the required

                                           11
     strong
   medium
    regular

                  Case 1               Case 2                       Case 3
                strong finite witnessability    smoothness       stable infiniteness

  Fig. 2. Theorem 4. The height of each bar corresponds to the strength of the
  property. The bars are ordered according to their usage in the proof.




strength of the other properties: whatever is used before is taken in ordinary
form, and whatever is used after requires a stronger form.
    Going back to the standard definitions of stable infiniteness, smoothness, and
strong finite witnessability, we get the following corollary by using case 1 of the
theorem and noticing that smoothness w.r.t. S implies strong stable infiniteness
w.r.t. any partition of S.

Corollary 1. Let S si ⊆ S and S nsi = S \ S si . Suppose T1 is stably infinite
w.r.t. S si and T2 is strongly finitely witnessable w.r.t. S nsi with witness wit and
smooth w.r.t. S. Then, the following are equivalent: 1. Γ1 ∪Γ2 is (T1 ⊕T2 )-satisfiable;
2. there exists an arrangement δV over VSsuch that Γ1 ∪ δV is T1 -satisfiable and
wit (Γ2 ) ∪ δV is T2 -satisfiable, where V = σ∈S Vσ , with Vσ = vars σ (wit (Γ2 )) for
σ ∈ S nsi and Vσ = vars σ (Γ1 ) ∩ vars σ (wit (Γ2 )) for σ ∈ S si .

    Finally, the following result, which is closest to Theorem 3, is directly ob-
tained from Corollary 1, since the strong politeness of T2 w.r.t. S si ∪ S nsi implies
that it is strongly finitely witnessable w.r.t. S nsi and smooth w.r.t. S si ∪ S nsi .

Corollary 2. Let S si ⊆ S and S nsi = S \ S si . If T1 is stably infinite w.r.t. S si
and T2 is strongly polite w.r.t. S with a witness wit , then the following are
equivalent: 1. Γ1 ∪ Γ2 is (T1 ⊕ T2 )-satisfiable; 2. there exists an arrangement
δV over V such S that Γ1 ∪ δV is T1 -satisfiable and wit (Γ2 ) ∪ δV is T2 -satisfiable,
where V = σ∈S Vσ , with Vσ = vars σ (wit (Γ2 )) for each σ ∈ S nsi and Vσ =
vars σ (Γ1 ) ∩ vars σ (wit (Γ2 )) for each σ ∈ S si .

    Compared to Theorem 3, Corollary 2 partitions S into S si and S nsi and
requires that T1 be stably infinite w.r.t. S si . The gain from this requirement is
that the set Vσ is potentially reduced for σ ∈ S si . Note that unlike Theorem 4
and Corollary 1, Corollary 2 has the same assumptions regarding T2 as the
original Theorem 3 from [13]. We show its potential impact in the next example.

Example 7. Consider the theory TListIntBV4 from Example 3. Let ΓV        1 be x =
                                                                          n
5 ∧ v = 0000 ∧ w = w & v, and let Γ2 be a0 = cons(x, v, a1 ) ∧ i=1 ai =
cons(yi , w, ai+1 ). Using the witness function wit from [19], wit (Γ2 ) = Γ2 . The

                                           12
polite combination approach reduces the TListIntBV4 -satisfiability of Γ1 ∧ Γ2 to
the existence of an arrangement δ over {x, v, w}∪{y1 , . . . , yn }, such that Γ1 ∧δ is
TIntBV4 -satisfiable and wit (Γ2 ) ∧ δ is TList -satisfiable. Corollary 2 shows that we
can do better. Since TIntBV4 is stably infinite w.r.t. {int}, it is enough to check
the existence of an arrangement over the variables of sort BV4 that occur in
wit (Γ2 ), together with the variables of sort int that are shared between Γ1 and
Γ2 . This means that arrangements over {x, v, w} are considered, instead of over
{x, v, w}∪{y1 , . . . , yn }. As n becomes large, standard polite combination requires
considering exponentially more arrangements, while the number of arrangements
considered by our combination method remains the same.                                ⊓
                                                                                      ⊔


4.2   Proof of Theorem 4

The left-to-right direction is straightforward, using the reducts of the satisfy-
ing interpretation of Γ1 ∪ Γ2 to Σ1 and Σ2 . We now focus on the right-to-left
direction, and begin with the following lemma, which strengthens Theorem 1,
obtaining a many-sorted Löwenheim-Skolem Theorem, where the cardinality of
the finite sorts remains the same.

Lemma 8. Let Σ be a signature, T a Σ-theory, ϕ a Σ-formula, and A a T -
                                             fin     inf
interpretation that satisfies φ. Let SΣ = SA     ⊎ SA    , where σ A is finite for
             fin       A                            inf
every σ ∈ SA and σ is infinite for every σ ∈ SA . Then there exists a T -
                                                                           fin
interpretation B that satisfies ϕ such that σ B = σ A for every σ ∈ SA         and
                                 inf
σ B is countable for every σ ∈ SA    .

The proof of Theorem 4 continues with the following main lemma.

Lemma 9 (Main Lemma). Let S si ⊆ S and S nsi = S \ S si , Suppose T1
is stably infinite w.r.t. S si and that one of the three cases of Theorem 4 holds.
Further, assume there exists an arrangement δV over V such        S that Γ1 ∪ δV is
T1 -satisfiable, and wit (Γ2 ) ∪ δV is T2 -satisfiable, where V = σ∈S Vσ , with Vσ =
vars σ (wit (Γ2 )) for each σ ∈ S nsi and Vσ = vars σ (Γ1 ) ∩ vars σ (wit (Γ2 )) for each
σ ∈ S si . Then, there is a T1 -interpretation A that satisfies Γ1 ∪ δV and a T2 -
interpretation B that satisfies wit (Γ2 ) ∪ δV such that σ A = σ B for all σ ∈ S.

Proof : Let ψ2 := wit (Γ2 ). Since T1 is stably infinite w.r.t. S si , there is a T1 -
interpretation A satisfying Γ1 ∪ δV in which σ A is infinite for each σ ∈ S si .
By Theorem 1, we may assume that σ A is countable for each σ ∈ S si . We
consider the first case of Theorem 4 (the others are omitted due to space con-
straints). Suppose T2 is strongly stably infinite w.r.t. (S si , S nsi ) and strongly
polite w.r.t. S nsi . Since T2 is strongly finitely-witnessable w.r.t. S nsi , there
exists a T2 -interpretation B that satisfies ψ2 ∪ δV such that σ B = VσB for
each σ ∈ S nsi . Since A and B satisfy δV , we have that for every σ ∈ S nsi ,
 σ B = VσB = VσA ≤ σ A . T2 is also smooth w.r.t. S nsi , and so there ex-
                                                                   ′
ists a T2 -interpretation B ′ satisfying ψ2 ∪ δV such that σ B         = σ A for each


                                           13
σ ∈ S nsi . Finally, T2 is strongly stably infinite w.r.t. (S si , S nsi ), so there is a T2 -
                                                          ′′
interpretation B ′′ that satisfies ψ2 ∪ δV such that σ B is infinite for each σ ∈ S si
        ′′         ′
and σ B = σ B = σ A for each σ ∈ S nsi . By Lemma 8, we may assume that
    ′′                                              ′′
σ B is countable for each σ ∈ S si . Thus, σ B           = σ A for each σ ∈ S.              ⊓
                                                                                            ⊔

     We now conclude Theorem 4: Let T := T1 ⊕ T2 . Lemma 9 gives us a T1
interpretation A with A |= Γ1 ∪ δV and a T2 interpretation B with B |= ψ2 ∪ δV ,
and σ A = σ B for σ ∈ S. Set Γ1′ := Γ1 ∪ δV and Γ2′ := ψ2 ∪ δV . Then, Vσ =
vars σ (Γ1′ )∩vars σ (Γ2′ ) for σ ∈ S. Now, A |= Γ1′ ∪δV and B |= Γ2′ ∪δV . Also, |σ A | =
|σ B | for σ ∈ S. By Theorem 2, Γ1′ ∪ Γ2′ is T -satisfiable. In particular, Γ1 ∪ {ψ2 } is
T -satisfiable, and hence also Γ1 ∪ {∃w.ψ2 }, with w = vars (wit (Γ2 )) \ vars (Γ2 ).
Finally, ∃w.wit (Γ2 ) is T2 -equivalent to Γ2 , hence Γ1 ∪ Γ2 is T -satisfiable.         ⊓
                                                                                         ⊔



5        Preliminary Case Study

The results presented in Section 4 was motivated by a set of smart contract
verification benchmarks. We obtained these benchmarks by applying the open-
source Move Prover verifier [23] to smart contracts found in the open-source
Diem project [10]. The Move prover is a formal verifier for smart contracts writ-
ten in the Move language [6] and was designed to target smart contracts used
in the Diem blockchain [1]. It works via a translation to the Boogie verifica-
tion framework [15], which in turn produces SMT-LIB 2 benchmarks that are
dispatched to SMT solvers. The benchmarks we obtained involve datatypes, in-
tegers, Booleans, and quantifiers. Our case study began by running CVC4 [2] on
the benchmarks. For most of the benchmarks that were solved by CVC4, theory
combination took a small percentage of the overall runtime of the solver, account-
ing for 10% or less in all but 1 benchmark. However, solving that benchmark
took 81 seconds, of which 20 seconds was dedicated to theory combination.
    We implemented an optimization to the datatype solver of CVC4 based on
Corollary 2. With the original polite combination method, every term that orig-
inates from the theory of datatypes with another sort is shared with the other
theories, triggering an analysis of the arrangements of these terms. In our op-
timization, we limit the sharing of such terms to those of Boolean sort. In the
language of Corollary 2, T1 is the combined theory of Booleans, uninterpreted
functions, and integers, which is stably infinite w.r.t. the uninterpreted sorts
and integer sorts. T2 is an instance of the theory of datatypes, which is strongly
polite w.r.t its element sorts, which in this case are the sorts of T1 .
    A comparison of an original and optimized run on the difficult benchmark
is shown in Figure 3. As shown, the optimization reduces the total running
time by 75%, and the time spent on theory combination in particular by 83%.
To further isolate the effectiveness of our optimization, we report the number of
terms that each theory solver considered. In CVC4, constraints are not flattened,
so shared terms are processed instead of shared variables. Each theory solver

                                             14
                            total (s) comb (s) DT INT UFB shared
                optimized     34.9      3.4    236.1 212.1 78.4 125.8
                 original     81.5      20.3   116.0 281.0 123.9 163.5

    Fig. 3. Runtimes (in seconds) and number of terms (in thousands) added to the
    data structures of DT, INT, UFB, and the number of shared terms (shared).




maintains its own data structure for tracking equality information. These data
structures contain terms belonging to the theory that either come from the
input assertions or are shared with another theory. A data structure is also
maintained that contains all shared terms belonging to any theory. The last 4
columns of Figure 4 count the number of times (in thousands) a term was added
to the equality data structure for the theory of datatypes (DT), integers (INT),
and uninterpreted functions and Booleans (UFB), as well as to the the shared
term data structure (shared). With the optimization, the datatype solver keeps
more inferred assertions internally, which leads to an increase in the number of
additions of terms to its data structure. However, sharing fewer terms, reduces
the number of terms in the data structures for the other theories. Moreover, while
the total number of terms considered remains roughly the same, the number of
shared terms decreases by 24%. This suggests that although the workload on the
individual theory solvers is roughly similar, a decrease in the number of shared
terms in the optimized run results in a significant improvement in the overall
runtime. Although our evidence is only anecdotal at the moment, we believe this
benchmark is highly representative of the potential benefits of our optimization.

6     Conclusion
This paper makes two contributions: First, we separated politeness and strong
politeness, which shows that sometimes, the (typically harder) task of finding a
strong witness is not a waste of efforts. Then, we provided an optimization to
the polite combination method, which is applies when one of the theories in the
combination is stably infinite w.r.t a subset of the sorts.
    We envision several directions for future work. First, the sepration of polite-
ness from strong politeness demonstrates a need to identify sufficient criteria for
the equivalence of these notions — such as, for instance, the additivity criterion
introduced by Sheng et al. [19]. Second, polite combination might be optimized
by applying the witness function only to part of the purified input formula. Fi-
nally, we plan to extend the initial implementation of this approach in CVC4
and evaluate its impact based on more benchmarks.

References
 1. Amsden, Z., Arora, R., Bano, S., Baudet, M., Blackshear, S., Bothra, A., Cabrera,
    G., Catalini, C., Chalkias, K., Cheng, E., Ching, A., Chursin, A., Danezis, G.,


                                          15
    Giacomo, G.D., Dill, D.L., Ding, H., Doudchenko, N., Gao, V., Gao, Z., Garillot,
    F., Gorven, M., Hayes, P., Hou, J.M., Hu, Y., Hurley, K., Lewi, K., Li, C., Li, Z.,
    Malkhi, D., Margulis, S., Maurer, B., Mohassel, P., de Naurois, L., Nikolaenko,
    V., Nowacki, T., Orlov, O., Perelman, D., Pott, A., Proctor, B., Qadeer, S., Rain,
    Russi, D., Schwab, B., Sezer, S., Sonnino, A., Venter, H., Wei, L., Wernerfelt,
    N., Williams, B., Wu, Q., Yan, X., Zakian, T., Zhou, R.: The Libra Blockchain.
    https://developers.diem.com/docs/technical-papers/the-diem-blockchain-paper/
    (2019)
 2. Barrett, C., Conway, C.L., Deters, M., Hadarean, L., Jovanović, D., King, T.,
    Reynolds, A., Tinelli, C.: CVC4. In: Proceedings of the 23rd International Con-
    ference on Computer Aided Verification. pp. 171–177. CAV’11, Springer-Verlag
    (2011), http://dl.acm.org/citation.cfm?id=2032305.2032319
 3. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB Standard: Version 2.6. Tech.
    rep., Department of Computer Science, The University of Iowa (2017), available
    at www.SMT-LIB.org
 4. Barrett, C., Tinelli, C.: Satisfiability modulo theories. In: Handbook of Model
    Checking, pp. 305–343. Springer (2018)
 5. Barrett, C.W., Shikanian, I., Tinelli, C.: An abstract decision procedure for a
    theory of inductive data types. Journal on Satisfiability, Boolean Modeling and
    Computation 3(1-2), 21–46 (2007)
 6. Blackshear, S., Cheng, E., Dill, D.L., Gao, V., Maurer, B., Nowacki,
    T., Pott, A., Qadeer, S., Rain, Russi, D., Sezer, S., Zakian,
    T., Zhou, R.: Move: A language with programmable resources.
    https://developers.diem.com/docs/technical-papers/move-paper/ (2019)
 7. Casal, F., Rasga, J.: Revisiting the equivalence of shininess and politeness. In:
    McMillan, K., Middeldorp, A., Voronkov, A. (eds.) Logic for Programming, Arti-
    ficial Intelligence, and Reasoning. pp. 198–212. Springer Berlin Heidelberg, Berlin,
    Heidelberg (2013)
 8. Casal, F., Rasga, J.: Equivalence of shiny and strongly polite theories (2014),
    https://pdfs.semanticscholar.org/109f/d4f188663a28076b7eb7931f69c5ffc7b3c5.pdf ,
    unpublished
 9. Casal, F., Rasga, J.: Many-sorted equivalence of shiny and strongly polite theories.
    J. Autom. Reasoning 60(2), 221–236 (2018)
10. diem: https://github.com/diem/diem
11. Enderton, H.B.: A mathematical introduction to logic. Academic Press (2001)
12. Fontaine, P.: Combinations of theories for decidable fragments of first-order logic.
    In: Ghilardi, S., Sebastiani, R. (eds.) Frontiers of Combining Systems, 7th Inter-
    national Symposium, FroCoS 2009, Trento, Italy, September 16-18, 2009. Proceed-
    ings. Lecture Notes in Computer Science, vol. 5749, pp. 263–278. Springer (2009)
13. Jovanovic, D., Barrett, C.W.: Polite theories revisited. In: Fermüller, C.G.,
    Voronkov, A. (eds.) Logic for Programming, Artificial Intelligence, and Rea-
    soning - 17th International Conference, LPAR-17, Yogyakarta, Indonesia, Oc-
    tober 10-15, 2010. Proceedings. Lecture Notes in Computer Science, vol. 6397,
    pp. 402–416. Springer (2010), extended technical report is available at
    http://theory.stanford.edu/∼barrett/pubs/JB10-TR.pdf
14. Krstic, S., Goel, A., Grundy, J., Tinelli, C.: Combined satisfiability modulo para-
    metric theories. In: Grumberg, O., Huth, M. (eds.) Tools and Algorithms for the
    Construction and Analysis of Systems, 13th International Conference, TACAS
    2007, Held as Part of the Joint European Conferences on Theory and Practice
    of Software, ETAPS 2007 Braga, Portugal, March 24 - April 1, 2007, Proceedings.
    Lecture Notes in Computer Science, vol. 4424, pp. 602–617. Springer (2007)


                                          16
15. Leino, K.R.M.: This is boogie 2 (2008), https://www.microsoft.com/en-us/research/publication/this-is-boogie-2-2/,
    manuscript KRML 178
16. Nelson, G.: Techniques for program verification. Tech. Rep. CSL-81-10, Xerox, Palo
    Alto Research Center (1981)
17. Nelson, G., Oppen, D.C.: Simplification by cooperating decision procedures. ACM
    Trans. Program. Lang. Syst. 1(2), 245–257 (1979)
18. Ranise, S., Ringeissen, C., Zarba, C.G.: Combining data structures with non-
    stably infinite theories using many-sorted logic. In: Gramlich, B. (ed.) Frontiers
    of Combining Systems, 5th International Workshop, FroCoS 2005, Vienna, Aus-
    tria, September 19-21, 2005, Proceedings. Lecture Notes in Computer Science,
    vol. 3717, pp. 48–64. Springer (2005), extended technical report is available at
    https://hal.inria.fr/inria-00070335/
19. Sheng, Y., Zohar, Y., Ringeissen, C., Lange, J., Fontaine, P., Barrett, C.: Polite-
    ness for the theory of algebraic datatypes. In: Peltier, N., Sofronie-Stokkermans,
    V. (eds.) Automated Reasoning. pp. 238–255. Springer International Publishing,
    Cham (2020)
20. Tinelli, C., Zarba, C.G.: Combining decision procedures for sorted theories. In:
    Alferes, J.J., Leite, J.A. (eds.) Logics in Artificial Intelligence, 9th European Con-
    ference, JELIA 2004, Lisbon, Portugal, September 27-30, 2004, Proceedings. Lec-
    ture Notes in Computer Science, vol. 3229, pp. 641–653. Springer (2004)
21. Tinelli, C., Zarba, C.G.: Combining decision procedures for sorted theories. In:
    JELIA. Lecture Notes in Computer Science, vol. 3229, pp. 641–653. Springer (2004)
22. Tinelli, C., Zarba, C.G.: Combining nonstably infinite theories. J. Autom. Reason-
    ing 34(3), 209–238 (2005)
23. Zhong, J.E., Cheang, K., Qadeer, S., Grieskamp, W., Blackshear, S., Park, J.,
    Zohar, Y., Barrett, C.W., Dill, D.L.: The move prover. In: CAV (1). Lecture Notes
    in Computer Science, vol. 12224, pp. 137–150. Springer (2020)




                                         17
A     Appendix

A.1    Theories vs. Classes of Structures

In papers about theory combination, theories are often defined in terms of some
set Ax of sentences (axioms) (see, e.g., [9,20,13]). Specifically, a theory is defined
as the set of all sentences entailed by Ax or, interchangeably, as the class of all
structures that satisfy Ax. This is the approach we take in this paper. The main
reason for this is that the combination theorems we prove and cite here rely on
some forms of the Löwenheim-Skolem theorem, which do not hold for arbitrary
classes of structures, but do hold when defining theories this way. On the other
hand, theories in the SMT-LIB 2 standard, as well as in many SMT papers about
individual theories, are defined more generally as classes of structures without
reference to a set of axioms.
    However, this discrepancy is not substantial since the two notions of a theory
as a class of structures are easily interreducible; as mentioned in the introduction,
every theory T in the second, more general sense induces a theory in the first
sense that is equivalent to T for all of our intents and purposes since it entails
exactly the same sentences as T . To be more precise, the combination theorems
that we prove and cite only regard satisfiability of formulas in a theory (though
their proofs may analyze the structures of a theory). The important thing is
that the transformation between the two notions preserves satisfiability, and
therefore interchanging these notions can be done without loss of generality. For
completeness, we prove this fact below:

Lemma 10. Let Σ be a signature, C a class of Σ-structures, Ax the set of Σ-
sentences satisfied by all structures of C, and TC the class of all Σ-structures that
satisfy all sentences of Ax. Then, for every Σ-formula ϕ, ϕ is TC -satisfiable iff
ϕ is satisfied by some Σ-interpretation whose variable-free part is in C.

Proof : Every interpretation whose variable-free part is in C is a TC -interpretation,
and so the right-to-left direction trivially holds. Now, suppose ϕ is not satisfied
by any Σ-interpretation whose variable-free part is in C. Then its existential
closure ∃x.ϕ is not satisfied by any structure of C, and hence ¬∃x.ϕ ∈ Ax. Ad
absurdum, suppose that ϕ is TC -satisfiable. Then there is a TC -interpretation A
such that A |= ϕ. In particular, A |= ∃x.ϕ. But since A is a TC -interpretation,
we must also have A |= ¬∃x.ϕ, which is a contradiction.                             ⊓
                                                                                    ⊔



A.2    Proof of Lemma 1

Let φ be a quantifier-free Σ2 -formula, A a T2,3 -interpretation that satisfies φ and
κ a function from {σ1 , σ2 } to the class of cardinals such that κ(σ1 ) ≥ σ1A and
κ(σ2 ) ≥ σ2A . We construct a Σ2 -interpretation A′ as follows. For i ∈ {1, 2}, we
       ′
let σiA := σiA ⊎ B for some set B of countable cardinality if κ(σi ) is infinite or
of cardinality κ(σi ) − |σi |A otherwise. Notice that this is well defined because

                                         18
                                         ′
κ(σi ) ≥ σiA . As for variables, xA := xA for each variable in vars (φ). This is
well defined because the domains of σ1 and σ2 were only possibly extended, not
reduced. First, we prove that A′ is a T2,3 -interpretation. If κ(σ1 ) = 2, then since
                                                                        A
κ(σ1 ) ≥ σ1A , we must have that σ1A = 2, which means that |σ2 | is infinite,
which in turn means that κ(σ2 ) is infinite as well. Hence in this case we have
    ′                       ′
 σ1A = κ(σ1 ) = 2 and σ2A = κ(σ2 ) = ∞. Otherwise, κ(σ1 ) ≥ 3, and hence
    ′                                ′
σ1A     = κ(σ1 ) ≥ 3 and also σ2A        = κ(σ2 ) ≥ σ2A ≥ 3. Clearly, A′ satisfies φ
                                                                         ′
as the interpretations of variables did not change. Finally, σ1A             = κ(σ1 ) and
   ′
σ2A     = κ(σ2 ) by construction.
                                                                                         ⊓
                                                                                         ⊔


A.3     Proof of Lemma 2

Define a function wit by wit (phi) := phi ∧ x1 = x1 ∧ x2 = x2 ∧ x3 = x3 ∧ y1 =
y1 ∧ y2 = y2 ∧ y3 = y3 for fresh variables x1 , x2 and x3 of sort σ1 and y1 ,
y2 and y3 of sort σ2 . We prove that wit is a witness for T2,3 w.r.t. {σ1 , σ2 }. φ
and ∃x1 , x2 , x3 , y1 , y2 , y3 .wit (φ) are trivially logically equivalent and in partic-
ular T2,3 -equivalent. We prove that wit (φ) is finitely witnessed for T2,3 w.r.t.
{σ1 , σ2 }. Suppose that wit (φ) is T2,3 -satisfiable and let A be a satisfying T2,3 -
interpretation. Define a Σ2 -interpretation B simply by σ1B = vars σ1 (φ)A ⊎{a1 , a2 , a3 }
and σ2B = vars σ2 (φ)A ⊎ {b1 , b2 , b3 } for a1 , a2 , a3 ∈ / σ1A and b1 , b2 , b3 ∈/ σ2A . The
interpretations of variables from φ are the same as in A. As for the fresh vari-
ables xB                   B
         i := ai and yi := bi for i ∈ {1, 2, 3}. We prove that B finitely witnesses
wit (φ) for T2,3 w.r.t. {σ1 , σ2 }. First, B is a T2,3 -interpretation, as by construc-
tion σ1B , σ2B ≥ 3. Second, B |= φ as the interpretations of variables from φ did
not change, and trivially satisfies the new identities, and so B |=wit (φ). Third,
by construction σ1B = vars σ1 (φ)A ⊎ {a1 , a2 , a3 } = vars σ1 (φ)B ⊎ xB              B    B
                                                                                 1 , x2 , x3 =
                 B
vars σ1 (wit (φ)) , and similarly for σ2 .
                                                                                              ⊓
                                                                                              ⊔


A.4     Proof of Lemma 3

Let wit be a witness for T2,3 w.r.t. {σ1 , σ2 }. We show that it is not strong. In
particular, we show that wit (v = v) is not strongly finitely witnessed for T2,3
w.r.t. {σ1 , σ2 }. Consider a T2,3 -interpretation A with σ1A = 2 and σ2A = ℵ0 .
Clearly, A |= v = v, and so A |= ∃ w. wit (v = v), with w being the variables in
wit (v = v) other than v. This in turn means that there is a T2,3 -interpretation
A′ that satisfies wit (v = v), different from A only in the interpretations of w,
if anywhere. Let δ be the arrangement over vars (wit (v = v)) induced by A′ .
Then, δ either asserts that all variables in vars σ1 (wit (v = v)) are identical, or
it partitions them into two equivalence classes. A′ |= wit (v = v) ∧ δ, and so
wit (v = v)∧δ is T2,3 -satisfiable. We show that it does not have a finite witness for
T2,3 w.r.t. S. Suppose for contradiction that B is a finite witness of wit (v = v)∧δ

                                             19
for T2,3 w.r.t. S. Then σ1B = vars σ1 (wit (v = v) ∧ δ)B . Now, B |= δ and B is a
T2,3 -interpretation, meaning σ1B ≥ 2, so if δ requires all variables of sort σ1 to
be equal, we already have a contradiction. On the other hand, if δ partitions the
variables into two equivalence classes, we get that σ1B = 2. But since B finitely
witnesses wit (v = v) ∧ δ for T2,3 w.r.t. {σ1 , σ2 }, we also get that σ2B is finite,
meaning B is not a T2,3 -interpretation.                                           ⊓
                                                                                   ⊔


A.5    Proof of Lemma 4

Let A be the T -structure with a minimal number of elements, and let n = σ A .
                                                    σ
To show that every Σ0 -structure that satisfies ψ≥n     belongs to T , let B be a
Σ0 -structure that satisfies ψ≥n and let m be the cardinality of σ B . Then m ≥ n.
                              σ

Clearly, A |= x = x and has n elements. Since T is smooth w.r.t. σ, there exists
a T -interpretation (that satisfies x = x) with cardinality m. This interpretation
must be B, as the lack of any symbols means that the only thing that distin-
guishes between Σ0 -structures is their cardinality (modulo isomorphism). For
the converse, note that by the choice of n as minimal, every T -structure satisfies
  σ
ψ≥n  .                                                                           ⊓
                                                                                 ⊔


A.6    Proof of Proposition 1

x = x is clearly T -satisfiable. Since T is finitely witnessable (say with witness
wit ), there is a T -interpretation A that satisfies wit (x = x) such that σ A is finite.
                                                                         σ
T is smooth, and hence, by Lemma 4, it is axiomatized by ψ≥n                for some n. Define
    ′
wit (φ) := φ ∧ distinct (x1 , . . . , xn ) for fresh x1 , . . . , xn . Since T is axiomatized
by ψ≥nσ
         , φ is T -equivalent to ∃x.wit ′ (φ). Further, for any arrangement δ over
some set of variables, and any T -interpretation A′ that satisfies wit ′ (φ) ∧ δ, if
                                                                                             ′
the domain of A′ is reduced to contain only the elements in vars (wit ′ (φ) ∧ δ)A ,
the result is still a T -interpretation since wit ′ (φ) contains distinct (x1 , . . . , xn ).
We therefore get that wit ′ is a strong witness for T w.r.t. σ.                              ⊓
                                                                                             ⊔


A.7    Proof of Lemma 5

Let φ be x = x and A be a Σ-interpretation with σ A = {1, 2} and xA = 1. Then
         ∞
A is a TEven -interpretation that satisfies φ. Let κ defined by κ(s) = 3. Then
                                                                                     ′
3 = κ(s) ≥ σ A = 2. However, there is no Σ-interpretation A′ with σ A = 3.
                                                                         ⊓
                                                                         ⊔


A.8    Proof of Lemma 6

Define wit (φ) as follows. Let E be the set of all equivalence relations over
vars (φ)∪{w} for some fresh variable w. Let even(E) be the set of all equivalence
relations in E for which the number of equivalence classes is even. Then, wit (φ)

                                             20
      W
is φ ∧ e∈even(E) δe , where for an equivalence relation e ∈ even(E), δe is the
arrangement induced by e:
                     ^                    ^
                         x=y∧                          x 6= y
                     (x,y)∈e          x,y∈vars (φ)∪{w}∧(x,y)6∈e

We prove that wit is a witness. Let φ be a Σ-formula. We first prove that it
     ∞
is TEven -equivalent to ∃ w. wit (φ). Since φ is a conjunct of wit (φ) that does not
include w, every A-interpretation that satisfies wit (φ) also satisfies φ. For the
                                   ∞
other direction, let A be a TEven      -interpretation satisfying φ. Even though A
may have infinitely many elements, the number of elements in vars (φ)A must
be finite. If the number of elements in vars (φ)A is even, then let a be some
arbitrary element of vars (φ)A . Otherwise, let a be an element in A different
from all the elements in vars (φ)A (there must be such an element since A has
an even or infinite number of elements). In either case, the number of elements
in (vars (φ) ∪ {w})A is even. Thus, if we modify A to map w to a, then it must
satisfy one of the disjuncts in wit (φ). Hence, A satisfies ∃ w. wit (φ).
                         ∞                                              ∞
    Next, if wit (φ) is TEven -satisfiable, then there is a satisfying TEven -interpreta-
tion A satisfying it. A must satisfy one of the disjuncts in wit (φ), which means
 vars (wit (φ))A is even. The restriction of A to vars (wit (φ))A is a TEven   ∞
                                                                                   -inter-
pretation that finitely witnesses wit (φ).                                              ⊓
                                                                                        ⊔

A.9    Proof of Lemma 7
Let wit : QF (Σ0 ) → QF (Σ0 ). We prove that wit is not a strong witness for
  ∞
TEven  w.r.t. σ, by showing that wit (x = x) is not strongly finitely witnessed for
  ∞                            ∞
TEven w.r.t. σ. Consider a TEven   -interpretation A with 2 elements, which inter-
prets all the variables in vars (wit (x = x)). Clearly, A |= x = x, and therefore,
A |= ∃ w. wit (x = x), where w is vars (wit (x = x)) \ {x}. Hence, there exists a
  ∞
TEven -interpretation A′ , identical to A, except possibly in its interpretation of
variables in vars (wit (x = x)) \ {x}, that satisfies wit (x = x). In particular, A′
has two elements. Let δA′ be the arrangement over vars (wit (x = x)) satisfied
by A′ . Then δA′ induces an equivalence relation with either 1 or 2 equivalence
classes. Let v be a variable not in vars (wit (x = x)). Define an arrangement
δ over varsV(wit (x = x)) ∪ {v} as follows: If δA′ inducesVone equivalence class,
δ := δA′ ∧ u∈vars (wit (x=x)) v = u. Otherwise, δ := δA′ ∧ u∈vars (wit (x=x)) v 6= u.
In the first case, δ induces one equivalence class, and in the second, three.
                                                           ∞
wit (x = x) ∧ δ does not have a finite witness for TEven       w.r.t. σ, as any in-
terpretation B that finitely witnesses it has either 1 or 3 elements, and hence it
            ∞
is not in TEven .

A.10     Proof of Corollary 1
T2 is smooth w.r.t. S si ∪S nsi . In particular, it is smooth w.r.t. S nsi . We show that
it is also strongly stably infinite w.r.t. (S si , S nsi ), and then the result follows from
case 1 of Theorem 4. Let φ be a Σ-formula, A a T -interpretation that satisfies

                                            21
    φ. Define κ(σ) to be ℵ0 for every σ ∈ S si such that σ A is finite, κ(σ) = σ A for
    every σ ∈ S si such that σ A is infinite, and κ(σ) = σ A for every σ ∈ S nsi . Since
    T is smooth w.r.t. S si ∪ S nsi , there exists a T -interpretation B that satisfies φ
    with σ B = κ(σ) for every σ ∈ S si and σ B = κ(σ) = σ A for every σ ∈ S nsi .
                                                                                        ⊓
                                                                                        ⊔

    A.11      Proof of Lemma 8
    Let Ax be the set of sentences that are satisfied by every T -structure. Define
    the following sets, based on formulas that are defined in Figure 1:
                                       n                        o
                                           σ                fin
                               fin A := ψ=|σ   A | | σ ∈ SA

                                     n                            o
                                         σ             inf
                           inf A := ¬ψ=n     | σ ∈ SA      ,n ∈ N
                                  A := Ax ∪ fin A ∪ inf A ∪ {φ}


    Clearly, A |= A. By Theorem 1, there exists a Σ-interpretation B that satisfies
    A in which σ B is countable whenever it is infinite, for every σ ∈ SΣ . This in
                                    inf                   fin
    particular holds for every σ ∈ SA   . Now let σ ∈ SA      , then since B |= fin A ,
      B       A
     σ = σ . Finally, B |= φ and it is a T -interpretation.
                                                                                    ⊓
                                                                                    ⊔

    A.12      Remaining Cases in The Proof of Lemma 9
    Let ψ2 := wit (Γ2 ). Since T1 is stably infinite w.r.t. S si , there is a T1 -interpretation
    A satisfying Γ1 ∪ δV in which σ A is infinite for each σ ∈ S si . By Theorem 1, we
    may assume that σ A is countable for each σ ∈ S si .

Case 2 : Suppose T2 is stably infinite w.r.t (S si , S nsi ), smooth w.r.t. (S nsi , S si ),
       and strongly finitely witnessable w.r.t. S nsi . Then, there exists a T2 -inter-
       pretation B that satisfies ψ2 ∪ δV such that σ B = VσB for every σ ∈ S nsi .
       Since A and B satisfy δV , we have that for every σ ∈ S nsi , σ B = VσB =
        VσA ≤ σ A . T2 is stably infinite w.r.t. (S si , S nsi ), and so there exists a
                                                                    ′
       T2 -interpretation B ′ that satisfies ψ2 ∪ δV such that σ B is infinite for ev-
                               ′
       ery σ ∈ S si and σ B ≤ σ B ≤ σ A for every σ ∈ S nsi . T2 is smooth
         w.r.t. (S nsi , S si ) and so there is a T2 -interpretation B ′′ satisfying ψ2 ∪ δV
                          ′′                                              ′′
         such that σ B         = σ A for every σ ∈ S nsi and σ B               is infinite for ev-
                     si                                           B′′
         ery σ ∈ S . Using lemma 8, we may assume σ                     is countable and hence
             ′′
          σ B = σ A for every σ ∈ S.
Case 3 : Suppose T2 is stably infinite w.r.t. S si , smooth w.r.t. (S nsi , S si ), and
       strongly finitely witnessable w.r.t. (S nsi , S si ). Since it is stably infinite w.r.t. S si ,
       there exists a T2 -interpretation B that satisfies ψ2 ∪ δV such that σ B is in-
       finite for every σ ∈ S si . T2 is strongly finitely-witnessable w.r.t. (S nsi , S si ),

                                                  22
and hence there exists a T2 -interpretation B ′ that satisfies ψ2 ∪ δV such that
   ′     ′                             ′
σ B = VσB for every σ ∈ S nsi and σ B is infinite for every σ ∈ S si . Since A
                                                            ′        ′
and B ′ satisfy δV , we have that for every σ ∈ S nsi , σ B = VσB = VσA ≤
σ A . T2 is smooth w.r.t. (S nsi , S si ), and so there exists a T2 -interpretation
                                            ′′
B ′′ that satisfies ψ2 ∪ δV such that σ B        = σ A for every σ ∈ S nsi and
     ′′                                                                          ′′
σB        is infinite for every σ ∈ S si . By Lemma 8, we may assume that σ B
is countable for every σ ∈ S si , with the same cardinalities for sorts of S nsi ,
                    ′′
and so we have σ B = σ A also for every σ ∈ S.




                                      23
