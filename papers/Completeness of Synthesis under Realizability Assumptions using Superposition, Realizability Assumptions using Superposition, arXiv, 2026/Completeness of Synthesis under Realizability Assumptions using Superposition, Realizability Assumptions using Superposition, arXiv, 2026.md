                                                    Completeness of Synthesis under
                                             Realizability Assumptions using Superposition

                                         Márton Hajdu , Petra Hozzová , Laura Kovács , and Eva Maria Wagner( )

                                                                      TU Wien, Vienna, Austria
                                                                    eva.maria.wagner@tuwien.ac.at
arXiv:2605.19683v1 [cs.LO] 19 May 2026




                                               Abstract. Program synthesis is the task of automatically deriving a pro-
                                               gram that has been speciﬁed by a user in advance. Combining automated
                                               theorem proving with program synthesis enables the automated construc-
                                               tion of proven-to-be-correct programs, thereby ensuring software reliabil-
                                               ity. In this paper, we consider the superposition-based calculus extended to
                                               support synthesis of recursion-free programs allowing reasoning with un-
                                               computable symbols. We present cases where the calculus fails and reﬁne it
                                               to solve them. We prove that the reﬁned calculus is sound. Finally, we also
                                               prove completeness in the following sense: if at least one computable pro-
                                               gram satisfying the given speciﬁcation exists, we show that the modiﬁed
                                               calculus ﬁnds one.

                                               Keywords: Program Synthesis · Saturation · Superposition · Theorem
                                               Proving.


                                         1   Introduction

                                         Program synthesis focuses on constructing programs from a given functional spec-
                                         iﬁcation. There are many diﬀerent approaches for solving diﬀerent ﬂavors of this
                                         problem, including ones that guarantee that the found program satisﬁes a log-
                                         ical speciﬁcation [13, 14, 25]; techniques that synthesize a program based on a
                                         set of input-output examples [8, 10, 27]; and LLM-based methods which require
                                         external correctness checking [18]. In this paper, we focus on an automated de-
                                         ductive synthesis approach using a superposition-based theorem prover, in which
                                         a saturation-based framework proves a given speciﬁcation while simultaneously
                                         generating code conforming to that speciﬁcation.
                                            Recent work in [14] extracts a recursion-free program from a superposition-
                                         based proof of a logical speciﬁcation (requirement) on the program. Our approach
                                         explores and revises this framework and solves program synthesis in the presence
                                         of uncomputable symbols [13, 14]. Doing so, we impose the following syntactic
                                         restrictions on the program to be synthesized: (i) the program should use only
                                         so-called computable symbols, while (ii) its functional speciﬁcation may use both
                                         computable and uncomputable symbols. Uncomputable symbols include, for ex-
                                         ample, symbols annotated as such by the user of the synthesis system, allowing
                                         for better control of what the output program should (not) use. Uncomputable
2         Hajdu, Hozzová, Kovács, Wagner

symbols may, however, also include fresh symbols, such as Skolem functions, in-
troduced during the proving process.

Motivating Example. We motivate our work using an example adapted from [11,
23]. Consider the following constraints from the FLoC 2026 workshop schedule:
 1. On Friday (f), the Vampire (v) workshop is taking place. Using the unary
    predicate w for workshops, we assert w(v)).
 2. On Saturday (s), the PAAR (p) workshop is taking place (thus, w(p)).
 3. Today (x) is either Friday (f) or Saturday (s).
Our task for program synthesis is to infer what workshop y takes place depending
on x, with the condition that w is uncomputable, i.e. the answer should not contain
w.
   We encode this instance of program synthesis as follows. For readability, we
might omit parentheses in unary symbol applications throughout the paper, e.g.
we might write wv instead of w(v). We are looking for a program that is a witness
for y in the following formula:

            ϕ : ∀x∃y.(((x ≈ f ∨x ≈ s)∧(x ≈ f → wv)∧(x ≈ s → wp)) → wy).            (1)

A program that is a witness for y in (1) is called a solution of the synthesis problem
speciﬁed by (1); see Section 3 for precise formulation of program synthesis and
its solution. In the case of (1), two possible programs found by our approach are
if x ≈ f then v else p and if x ≈ s then p else v.                                   ❏

Synthesis and Saturation. In our approach to program synthesis, we build on
the saturation-based framework for program synthesis with uncomputable sym-
bols using the superposition calculus, as introduced in [14]. While the approach
was shown to be correct in [14], the question of completeness remained open un-
til now. In this paper, we close this gap by investigating the completeness of the
calculus under the assumption of realizability: if a computable program satisfying
the speciﬁcation exists, is the calculus guaranteed to derive it? We identify prop-
erties that make the calculus of [14] inherently incomplete. We adjust the calculus
accordingly, resulting in our SUPRA framework (Section 5). We further prove
completeness of SUPRA under the assumption of realizability (Section 5).
    This paper starts with preliminaries in Section 2, summarizing necessary no-
tions of ﬁrst-order logic and automated reasoning. Section 3 deﬁnes our synthesis
problem and presents a framework for solving it, by revising the setting of [14].
Following are our main contributions:
    – We introduce a new superposition-based calculus for synthesis (Section 4).
      Our calculus is coined as Superposition with Realizability Assumptions, in
      short SUPRA. Motivated by examples that cannot be solved by [14], SUPRA
      includes tailored conditions for term orderings and selection functions.
    – We prove completeness of our SUPRA calculus (Section 5). By completeness
      we mean that, if at least one computable program satisfying a given speciﬁca-
      tion exists, our SUPRA calculus ﬁnds one such program.
                                  Completeness of Synthesis under Realizability            3

We then review related work in Section 6, and conclude our paper in Section 7.
The (omitted) proofs of our results from Sections 4 and 5 are given in Sections A
and C, respectively.


2    Preliminaries

First-order Logic. We assume familiarity with standard multi-sorted ﬁrst-order
logic (FOL) with equality, where equality is denoted by ≈. We consider a ﬁxed sig-
nature Σ consisting of a ﬁnite set of function symbols with associated arities and a
set of variables V; variables are not part of the signature. We deﬁne the set of terms
T (Σ ∪V), or simply T when it is clear from the context, in the standard way over
Σ ∪V. We denote variables by x,y,z; terms by s,t,l,r,k; literals by L,K; clauses by
C,D; and formulas by F,G, all possibly with indices. Further, we write α for Skolem
constants. We denote lists of literals by L and K. We denote the empty list of liter-
als by ǫ. Let L be a literal and L a list of literals, then LL denotes the list of literals
having L as a head and L as a tail. We write ā for the tuple of variables or terms
a1 ,...,an . When a term t is of the form f (t̄), we say that f is the top-level symbol of t.
By cnf(F ) we denote the clausal normal form (CNF) of the formula F . We reserve
the symbol  for the empty clause which is logically equivalent to ⊥. We write L̂
for the literal complementary to L. We write t 6≈ s as a shorthand for ¬(t ≈ s). We
use the symbol ≈   ˙ to denote either ≈ or 6≈. An expression is a term, literal, clause,
or formula. We write E1 = E2 to denote syntactic equality of two expressions. If an
expression does not contain variables, we call it ground. We write E[t] to denote
all (possibly zero) occurrences of the term t. Then, E[s] denotes the expression
E[t] where all occurrences of t are replaced by the term s. Formulas with free vari-
ables are considered implicitly universally quantiﬁed; that is, we consider closed
formulas. A substitution σ is a mapping from variables to terms such that the set
{x | σ(x) 6= x} of variables is ﬁnite. A substitution σ is a uniﬁer of two expressions E
and E ′ if Eσ = E ′ σ, and is a most general uniﬁer (mgu) if for every uniﬁer θ of E and
E ′ , there exists substitution τ such that θ = στ . We denote the mgu of expressions
E1 ,E2 ,E1′ ,E2′ with mgu(E1 ,E1′ ) and mgu((E1 ,E2 ),(E1′ ,E2′ )) for the mgu of tuples.

Saturation-Based Proving and Superposition. A saturation-based prover works
with clauses. To prove a theorem G from axioms A1 ,...,An (assumed to be clauses),
the prover: (1) negates and clausiﬁes G, obtaining clauses cnf(¬G) = {C1 ,...,Cm };
(2) forms the saturation set S = {C1 ,...,Cm ,A1 ,...,An }; (3) repeats the following:
chooses clauses D1 ,... ,Dk ∈ S, uses an inference rule to derive a new clause D
from D1 ,...,Dk , and adds D into S. Deriving the empty clause  at any point in
step (3) concludes the proof, because it means that ¬G is inconsistent with the
axioms, which is equivalent to G following from the axioms. A common calculus
(a set of inference rules) used in saturation-based provers is the superposition cal-
culus [21]. The calculus is parametrized by a simpliﬁcation order ≻ on terms (see
next paragraph) and a selection function, which selects in each non-empty clause
some non-empty subset of literals. We denote selected literals by underlining them.
An inference rule can be applied to the given premise(s) if the literals selected in
4        Hajdu, Hozzová, Kovács, Wagner

the rule are also selected in the premise(s). For a certain class of selection functions,
the superposition calculus is sound (if  is derived from F , then F is unsatisﬁable)
and refutationally complete (if F is unsatisﬁable, then  can be derived from it).

Rewriting and Simpliﬁcation orders. A binary relation → over the set of terms is
a rewrite relation if (i) l → r ⇒ lθ → rθ and (ii) l → r ⇒ s[l] → s[r] for any terms l, r,
s and substitution θ. We write ← to denote the inverse of →. We call an ordered
pair l → r a rewrite rule if (i) l is not a variable and (ii) l contains all variables
that occur in r. A rewrite system R is a set of rewrite rules. We denote by →R the
smallest rewrite relation that contains R. A term l is irreducible in R if there is no r
s.t. l →R r ∈ R. We denote with →∗R the reﬂexive-transitive closure of →R . A term
r is a normal form of a term l w.r.t R if l →∗R r and r is irreducible in R. A rewrite
order is a strict (irreﬂexive) rewrite relation. A reduction order is a well-founded
rewrite order. We consider reduction orders which are total on ground terms; such
orders are also called simpliﬁcation orders. A precedence relation, denoted by ≫,
is a total order on the signature Σ.
    The lexicographic path order (LPO), denoted by ≻lpo , is parameterized by a
precedence relation ≫. Let s,t be terms with s = f (s1 ,...,sn ) and ≻lexlpo the standard
lexicographic ordering extension of ≻lpo . We write s ≻lpo t if:

 1. t is a variable and a proper subterm of s, or
 2. there is i ∈ {1,...,n} such that si lpo t, or
 3. t = f (t1 ,...,tn ), (s1 ,...,sn ) ≻lex
                                        lpo (t1 ,...,tn ) and s ≻lpo tj , for all j ∈ {1,...,n},or
 4. t = g(t1 ,...,tm ), f ≫ g and s ≻lpo tj , for all j ∈ {1,...,m}.

It is known that LPOs are simpliﬁcation orders [21].
    We view equalities as bags, ﬁnite multisets, and deﬁne and extend the term
orderings on bags. The bag extension for an ordering ≻ on a set X is a binary re-
lation on bags over X, denoted by ≻bag , deﬁned as the smallest transitive relation
on bags such that {x,y1 ,...,yn } ≻bag {x1 ,...,xm ,y1 ,...,yn } if x ≻ xi for all i ∈ {1,...,m}
and m ≥ 0. If ≻ is well-founded, then ≻bag is too. We order equality literals by
mapping each equality s ≈ t to the bag {s,t} and each disequality s 6≈ t to the bag
{s,s,t,t}, and then using ≻bag over these bags. Finally, we order clauses by taking
the bag extension of the bag extension for literals. We only write E1 ≻ E2 for two
expressions E1 and E2 when it is clear from the context which ordering is used.
We also write E1  E2 instead of E1 ≻ E2 ∨E1 = E2 .


3    The Synthesis Problem and How to Solve It

In this section, we adjust notions [14] to the purposes of our work. We assume a
ﬁxed signature Σ.

Deﬁnition 1 (Synthesis speciﬁcation). Let Σc be a subset of Σ and ϕ a closed
formula in ﬁrst-order logic over Σ of the form:

                                           ∀x̄∃y.F [x̄,y].                                           (2)
                                 Completeness of Synthesis under Realizability        5

We deﬁne a synthesis speciﬁcation, or simply speciﬁcation, Λ as the pair hΣc ,ϕi.
We call any symbol in Σc computable w.r.t. Λ, or just computable when Λ is clear
from the context. Further, any symbol in Σ \Σc is uncomputable w.r.t. Λ, or just
uncomputable. We denote the set of uncomputable symbols by Σu .
   An expression containing an uncomputable symbol is called uncomputable. Ex-
pressions that are not uncomputable are called computable.                     ❏

To synthesize programs for speciﬁcations, we use an if-then-else term constructor,
denoted by ite.
Deﬁnition 2 (ite and program terms). We deﬁne the conditional term con-
structor ite as follows. Let F be a formula over Σ and p,q be terms. When F is
true, then ite(F,p,q) is interpreted as the interpretation of p; otherwise, ite(F,p,q)
is interpreted as the interpretation of q. We call F the ite-condition.
    We deﬁne program terms as the smallest set P such that (i) T ⊆ P, and (ii)
ite(l ≈ r,p,q) ∈ P for any l,r ∈ T , and p,q ∈ P. We denote program terms by p, q,
possibly with indices. A term that does not contain a conditional term constructor
is called a simple term.                                                            ❏
We note that any term with the ite symbol containing arbitrary Boolean expres-
sions as conditions can be translated into an equivalent program term in P.

Deﬁnition 3 (Solution for a speciﬁcation). Let Λ = hΣc ,∀x̄∃y.F [x̄,y]]i be a
speciﬁcation. A computable p[x̄] ∈ P is called a solution for the speciﬁcation Λ
if ∀x̄.F [x̄, p[x̄]θ] is valid for an arbitrary substitution θ grounding p[ā] for fresh
constants ā.                                                                         ❏

Note that if x̄ are the only variables in p[x̄], then the condition for p[x̄] being a
solution reduces to ∀x̄.F [x̄,p[x̄]] being valid. On the other hand, if p[x̄] contains
variables z̄ other than x̄, then p[x̄] represents a class of solutions, one for each
grounding of z̄.
Deﬁnition 4 (Realizable speciﬁcation). Let Λ be a speciﬁcation. We call Λ
realizable if there exists a computable program term that is a solution to it. ❏
We are now ready to state the problem that is the focus of the present paper.

       The Synthesis Problem under Realizability Assumptions
  Given a realizable speciﬁcation Λ, the synthesis problem under realizability
  assumptions is the task of ﬁnding a solution to Λ.

In the following, we refer to the synthesis problem under realizability assumptions
simply as the synthesis problem.

Saturation-based synthesis framework. One approach to solving synthesis prob-
lems is the saturation-based synthesis framework introduced in [14], which extends
a saturation-based ﬁrst-order theorem prover into a synthesizer. The framework
constructs a program for speciﬁcation Λ in parallel with searching for a proof that
6       Hajdu, Hozzová, Kovács, Wagner

speciﬁcation (2) holds. Intuitively, y in (2) represents the output for the inputs x̄,
and thus substitutions into y in the proof correspond to fragments of the sought
program. To track these substitutions throughout the proof, the framework of [14]
uses a mechanism called answer literals [7]. In this paper, we use constrained
clauses, called answer clauses, rather than adding answer literals to clauses.
Deﬁnition 5 (Answer clause). Let C be a clause and p a program term. We
call the expression CJpK an answer clause. We call p the answer for the answer
clause CJpK. We denote answer clauses with C and D, possibly with indices. Given
a substitution σ, we write CJpKσ to denote CσJpσK.                             ❏
W.l.o.g. we assume that axioms A1 , ... , An are a part of speciﬁcation (2); that
is, F [x̄, y] is of the form (A1 ∧ ··· ∧ An ) → G[x̄, y]. To derive a program, the
framework ﬁrst preprocesses (2) like a saturation-based prover would: the for-
mula ¬∀x̄∃y.F [x̄,y] is converted to the equivalent ∃x̄∀y.¬F [x̄,y] and skolemized,
obtaining the equisatisﬁable ∀y.¬F [ᾱ,y],1 which is then clausiﬁed, resulting into
cnf(¬F [ᾱ,y]) = {C1 ,...,Cm }. The framework then extends the clauses C1 ,...,Cm ,
among which are also the axioms, into answer clauses C1 JyK,...,Cm JyK,2 and ini-
tializes the saturation set S = {C1 JyK,...,Cm JyK}, called the initial set from Λ. We
denote the consecutive steps of clausiﬁcation and extending clauses into answer
clauses by cnf(¬F [ᾱ,y])JyK.
Deﬁnition 6 (Semantics of answer clauses). CJpK is true with respect to a
given speciﬁcation Λ = hΣc ,∀x̄∃y.F [x̄,y]i, if the universal closure of C ∨F [ᾱ,p] is
true, where w.l.o.g. we assume CJpK and F [ᾱ,y] to have disjoint sets of variables.3 ❏
To work with answer clauses, we use an extension of the superposition calculus [21].
Using this calculus, we saturate S like a saturation-based prover: we extend the
set S by new clauses derived by rules from the calculus based on premises already
present in the set. We call S the set saturated from Λ. The work [14] proves that
the saturation approach is sound: it only derives valid answer clauses, and thus
when the answer clause Jp[ᾱ]K is derived, it is guaranteed that p[x̄] is a solution
for Λ. However, [14] makes no completeness claims. In the following section, we
show an example for which the approach fails to derive a program even though a
computable program exists.


4    Superposition with Synthesis
In this section, we present our new calculus SUPRA, adapted from [14]. We dis-
cuss the orderings and selection constraints that guide SUPRA (Section 4.1). We
also introduce an abstraction mechanism that separates computable and uncom-
putable terms via an inference rule, in addition to SUPRA (Section 4.2).
 1
   Since the skolems ᾱ represent the input of the sought program, they are computable.
 2
   In [14], only the clauses C containing y are extended into answer clauses CJyK. In this
   paper we extend all clauses C in preprocessing, including axioms, into answer clauses
   CJyK.
 3
    [14] uses analogous semantics while denoting CJpK by C ∨ans(p).
                                   Completeness of Synthesis under Realizability    7

4.1      The SUPRA Calculus

Our new calculus for Superposition with Realizability Assumptions, in short SUPRA,
is summarized in Figure 1. Compared to [14], we do not use so-called computable
uniﬁers (abstracting uniﬁers preventing uncomputable symbols from appearing in
the answer term), but most general uniﬁers and only allow an inference when the
answer term after applying σ is computable. Further, we include the rule SupU ,
which uniﬁes the answer terms p, q from premises, while [14] included a super-
position rule which did not unify p, q but rather added a constraint p 6≈ q into
the resulting clause. Finally, for simplicity, we work only with equality predicates;
thus, we do not include binary resolution or factoring rules as in [14].

Remark 1. The two variants of Superposition are both needed in the synthesis set-
ting. Applying the superposition rule branches the proof upon the equality literal.
The SupC rule reﬂects this branching in the answer by introducing an ite construc-
tor with the equality literal in the condition. However, since the answers cannot
contain uncomputable symbols, and even a computable non-ground condition
could become uncomputable by a subsequent substitution, we need an additional
mechanism for applying superposition. This is provided by SupU , which is applied
if the answers from the premises are uniﬁable. Since it is not clear upfront which
rule makes progress, our framework uses both of them in parallel.

   We next establish soundness of SUPRA; this result guarantees that the pro-
grams derived by SUPRA are solutions of the synthesis speciﬁcation.4

Theorem 1 (Soundness). The SUPRA calculus is sound with respect to the
semantics of answer clauses.

It follows from Theorem 1 that SUPRA derives solutions to synthesis speciﬁcations.


Corollary 1 (Solution to the Synthesis Problem). Given a synthesis speci-
ﬁcation Λ = hΣc ,∀x̄∃y.F [x̄,y]i, if SUPRA derives Jp[ᾱ]K from the initial set of Λ,
then p[x̄] is a solution for Λ.

The rules of SUPRA are, however, not the only ingredient necessary to guarantee
that a solution for a realizable speciﬁcation will be derived. The following example
illustrates how a derivation can get stuck.

Example 1. Our motivating example corresponding to the speciﬁcation (1) can
be expressed as a synthesis speciﬁcation with computable symbols f, s, p and v.
That is, Λ : h{f, s, p, v}, ϕi. We consider predicate symbols as function symbols
mapping values to {⊤, ⊥} in a two-sorted logic. We will try to derive a solution
for Λ using SUPRA. The initial set from Λ, where α is the Skolem constant intro-
duced for x and numbers denote clause labels, is {(1) α ≈ f ∨ α ≈ sJyK,(2) α 6≈ s ∨
wpJyK,(3) α 6≈ f ∨wvJyK,(4) ¬wyJyK}. We use a selection function that selects either
 4
     We provide detailed proofs for all our results in the Appendix.
8           Hajdu, Hozzová, Kovács, Wagner

                                                           (1) σ = mgu(l,l′ )
               l ≈ r∨CJpK             ′
                                       ˙ t∨DJqK
                                 s[l ] ≈                   (2) l′ is not a variable
     (SupC )                                         where
                     ˙ t∨C ∨DJite(l ≈ r,q,p)Kσ
                s[r] ≈                                     (3) rσ  lσ, tσ  s[l′ ]σ
                                                           (4) ite(l ≈ r,q,p)σ is computable

                                                           (1) σ = mgu((l,p),(l′ ,q))
               l ≈ r∨CJpK               ˙ t∨DJqK
                                 s[l′ ] ≈                  (2) l′ is not a variable
     (SupU )                                         where
                             ˙ t∨C ∨DJpKσ
                        s[r] ≈                             (3) rσ  lσ, tσ  s[l′ ]σ
                                                           (4) pσ is a computable simple term

                           s 6≈ t∨CJpK                       (1) σ = mgu(s,t)
               (EqRes)                               where
                              CJpKσ                          (2) pσ is computable


                         s ≈ t∨l ≈ r∨CJpK                  (1) σ = mgu(s,l)
            (EqFac)                                  where (2) tσ  sσ, rσ ⊁ tσ
                        s ≈ t∨t 6≈ r∨CJpKσ                 (3) pσ is computable


Fig. 1: Rules of SUPRA, where all maximal literals in a clause are selected (denoted
underlined), and CJpKσ denotes the application of σ on CJpK.

(i) all maximal literals or (ii) at least one negative literal.5 Let ≻ be an LPO with
the following symbol precedence: s ≫ f ≫ p ≫ v ≫ w ≫ α. We obtain the following
derivation, where we write SE for a Sup inference followed by an EqRes inference:
                  (1)                     (2)
            α ≈ f ∨α ≈ sJyK       α 6≈ s∨wpJyK               (3)
     (SE)
                        α ≈ f ∨wpJyK                   α 6≈ f ∨wvJyK          (4)
                (SE)
                                          wp∨wvJyK                         ¬wyJyK             (4)
                                 (SE)
                                                          wvJpK                           ¬wyJyK
                                                                   (inference not possible)

Here we get stuck, as no more inferences are possible. Superposition into (4) ¬wyJyK
with wvJpK cannot be applied, because v and p do not unify; moreover, we cannot
create an ite with condition wv, because w ∈ Σu . However, as mentioned before, Λ
is realizable, e.g. by the solution ite(x ≈ f,v,p). We did not derive a solution due to
the selection of computable literals in clauses which also contained uncomputable
literals.                                                                            ❏
Remark 2. Since [14] does not restrict selection nor simpliﬁcation orders in any
way, the failed derivation from Example 1 can be replicated by the calculus of [14].
Therefore, the calculus [14] does not always ﬁnd a solution if one exists – it is not
complete under realizability assumptions.                                          ❏
Based on Example 1, we observe that we have to select uncomputable literals
before computable ones. To this end, we make uncomputable terms bigger than
 5
     Such a selection function is called well-behaved and is suﬃcient to achieve refutational
     completeness in standard superposition reasoning.
                                                Completeness of Synthesis under Realizability                      9

computable terms in the simpliﬁcation order and restrict the selection functions
admissible for SUPRA to always select all maximal literals. We formally reﬁne the
simpliﬁcation order used by SUPRA as follows.
Deﬁnition 7 (Partitioned ordering). An ordering ≻ on terms is called parti-
tioned if for any ground uncomputable term s and any ground computable term t
it holds that s ≻ t.                                                       ❏
We require that the simpliﬁcation order that parameterizes SUPRA is partitioned.
In the rest of the paper, we will use an LPO with a precedence function where any
uncomputable symbol is greater than any computable symbol. Not only can these
types of LPOs be used for SUPRA, but also speciﬁc KBOs that are partitioned
orderings, see Section B for further discussion.
Example 2. Let ≻ be an LPO based on w ≫ v ≫ p ≫ s ≫ f. With a selection function
selecting all maximal literals w.r.t. ≻, we ﬁnd a solution for Λ from Example 1:
                       (2)               (4)

              α 6≈ s∨wpJyK           ¬wyJyK               (1)                  (4)                 (3)
      (SE)
                             α 6≈ sJpK              α ≈ f ∨α ≈ sJyK     ¬wyJyK            α 6≈ f ∨wvJyK
                 (SE)                                                                                       (SE)
                                            α ≈ fJpK                                   α 6≈ fJvK
                                     (SE)
                                                         Jite(α ≈ f,v,p)K
                                                                                                                   ❏

4.2     Abstraction of Computable Terms in Uncomputable Literals
While our motivating example (1) shows that inferences with uncomputable liter-
als should be applied before inferences with computable literals, sometimes this
cannot be enforced, as some uncomputable equations can only be used in a super-
position inference after performing a superposition into them with a computable
equation.
Example 3. Consider constants a,b,c,d,e, unary symbols f,g,h, and the speciﬁca-
tion:
         h{a,b,c,d,e}, ∃y.(f d 6≈ e∨(d 6≈ c∧gy ≈ ga)∨(f c ≈ e∧hy ≈ hb))i.
We perform the following derivation using an LPO ≻ with h ≫ g ≫ f ≫ e ≫ d ≫
c ≫ b ≫ a. The leaves are obtained from the initial set of the above speciﬁcation:
                                                        (2)

                               (1)               d ≈ c∨gy 6≈ gaJyK                           (3)
                                         (ER)
                        f d ≈ eJyK                    d ≈ cJaK                       f c 6≈ e∨hy 6≈ hbJyK
             (SupU )                                                    (ER)
                                f c ≈ eJite(d ≈ c,y,a)K                                   f c 6≈ eJbK
                  (SupC )
                                                    (inference not possible)

The last step of the derivation is not possible, because the answers b and ite(d ≈
c,y,a) do not unify, and we cannot construct an ite in the answer, because the
condition f c ≈ e is uncomputable.                                               ❏
10            Hajdu, Hozzová, Kovács, Wagner

The general observation we make from Example 3 is that we should resolve all un-
computable literals, even those containing computable subterms, before applying
inferences with computable symbols. For this purpose, we abstract the computable
subterms of uncomputable literals, thus separating reasoning with uncomputable
and computable symbols. We do this by adding an auxiliary inference rule Abs,
which replaces its premise by its consequence, indicated by the crossed-out premise.
We apply Abs exhaustively on each clause before we allow any further inferences:

                                     (1) s 6 t
                                     (2) there is a substitution θ s.t. s[k]θ
              s[k] ≈  ✘ ✘ ✘
                   ˙ t∨CJpK              is uncomputable and kθ is computable
                   ✘
    (Abs)    ✘✘                where (3) no proper superterm of k in s[k]
               ˙ t∨x 6≈ k∨CJpK
          s[x] ≈                         satisﬁes property (2)
                                     (4) k is not a variable
                                     (5) x is a fresh variable

Lemma 1. The rule Abs is sound with respect to the semantics of answer clauses.

To apply the rule in practice, we use the following syntactic conditions in place of
condition (2) of Abs.
Lemma 2. Condition (2) of rule Abs holds iﬀ (2a) k is computable, and (2b) ei-
ther s[k] is uncomputable, or it contains a variable not contained in k, and there
exists at least one uncomputable term.

Example 4. The derivation from Example 3 changes as follows when using Abs:
                                                                                               (3)
                                                                                        6≈ e∨hy
                                                                                     f c✭  ✭✭6≈   ✭✭
                                                                                                ✭hbJyK
                                                                        (Abs)        ✭
                                                                                  f c 6≈ e∨hy 6≈ hx∨x 6≈ bJyK
                                                                         (ER)                         ✭
                           (2)                          (1)                             ✭  6≈ e∨x
                                                                                        f c✭  ✭✭  6≈✭
                                                                                                    bJxK
                                ✭✭                                        (Abs)
                    d ≈✭
                       c∨gy
                        ✭✭  6≈✭
                              gaJyK                 f d✘ ✘✘
                                                       ≈ eJyK                       f z 6≈ e∨z 6≈ c∨x 6≈ bJxK
     (Abs)          ✭                    (Abs)
                                                    ✘                     (ER)
              d ≈ c∨gy 6≈ gx∨x 6≈ aJyK           f x ≈ e∨x 6≈ dJyK                      f z 6≈ e∨z 6≈ cJbK
     (ER)                                 (SE)
                     d ≈ c∨x 6≈ aJxK                                 y 6≈ d∨y 6≈ cJbK
             (ER)                                             (ER)
                        d ≈ cJaK                                        d 6≈ cJbK
                (SE)
                                         Jite(d ≈ c,b,a)K

Our new Abs rule allowed us to solve the speciﬁcation of Example 3, deriving the
program ite(d ≈ c,b,a).
                                                                              ❏


5      Completeness of SUPRA under Realizability
       Assumptions
In this section, we prove that the SUPRA calculus is complete with respect to
realizability assumptions. In particular, we show that if there exists a solution to
                                  Completeness of Synthesis under Realizability         11

the speciﬁcation Λ, then SUPRA used exhaustively with the rule Abs is guaranteed
to derive some (possibly diﬀerent) computable program, which is also a solution for
Λ since SUPRA is sound (see Section 4.1). Our main result is the following theorem.
Theorem 2 (Completeness under Realizability). Let Λ = hΣc ,∀x̄∃y.F [x̄,y]i
be a speciﬁcation. If Λ is realizable, then SUPRA with Abs derives an answer clause
of the form Jp[ᾱ]K from Λ where p[x̄] is a computable program term that is a
solution to Λ.
We prove Theorem 2 similarly to the completeness proof of the superposition cal-
culus [22], by contradiction. We assume that S is a set saturated from Λ up to
redundancy and abstracted (Deﬁnition 12), and that Jp[ᾱ]K ∈           / S for any p[ᾱ].
Yet, we assume that Λ is realizable and that t[x̄] is a solution to it – i.e., that
∀x̄.F [x̄,t[x̄]] is valid. W.l.o.g. we assume t[x̄] does not contain any variables except
for x̄. We then consider a grounding of S using t[ᾱ] (Deﬁnition 15) and construct
an interpretation for it (Deﬁnition 10). However, since the grounding of S is equi-
satisﬁable with ¬F [ᾱ,t[ᾱ]], which is unsatisﬁable because ∀x̄.F [x̄,t[x̄]] is valid, the
interpretation should not be a model of S. We then consider the smallest clause
C in the grounding that is false in the interpretation. Based on it, we either ﬁnd
an even smaller clause in the grounding that is also false in the interpretation, or
show that the clause in S, instance of which is C, should have been removed by Abs,
since S is abstracted. In either case, we obtain a contradiction. We split this part
of the proof into two steps: ﬁrst, in Lemma 4 we show that all computable clauses
in the grounding of S are satisﬁed in the model; then in Lemma 6 we extend this
property to all uncomputable clauses.
    Our construction involves substituting program terms into clauses – the term
t[ᾱ] is substituted for y in cnf(¬F [ᾱ, y])JyK. If t[ᾱ] contains ite terms, we have
to unroll them by creating multiple instances of the clause and adding the condi-
tion(s) from the ite into them. We collect the unrolled condition literals in lists
and separate them from the original clause, using so-called conditional clauses, as
deﬁned below.
Deﬁnition 8 (Conditional clause, c-clause). Let C be a clause and L a list
of literals. A conditional clause, c-clause for short, is an expression of the form
C ▽ L. We call L the condition of the  W c-clause C ▽ L. The c-clause C ▽ L is
logically equivalent to the clause C ∨ L∈L L. We denote c-clauses with C and D.
We use the notation CH to denote the c-clause C ▽ ǫ.                              ❏
We extend the ordering ≻ over clauses to c-clauses as follows.
Deﬁnition 9 (Ordering on c-clauses). We deﬁne an ordering ≻ over c-clauses
as follows. First, we extend ≻ to lists of literals. We have L ≻ ǫ for any non-empty L
and LL ≻ KK if either (i) L ≻ K or (ii) L = K and L ≻ K. We have C ▽ L ≻ D ▽ K
if either (i) C ≻ D, or (ii) C = D and L ≻ K.6                                       ❏
We now deﬁne a model for sets of c-clauses. As usual in superposition completeness
proofs, we use rewrite systems as interpretations, where any equation s ≈ t is true
 6
     This ordering preserves well-foundedness.
12      Hajdu, Hozzová, Kovács, Wagner

in a rewrite interpretation R, denoted R  s ≈ t, if s and t have the same normal
form in R. As usual, when s,t are ground, R  s 6≈ t ⇐⇒ R 2 s ≈ t. A c-clause C ▽ L
is true in R if C or L contain at least one literal L such that R  L.
Deﬁnition 10 (Model for c-clauses). Let S be a set of ground c-clauses. For
every c-clause C ∈ S, we deﬁne in parallel two sets of term rewrite rules RSC and
RS≺C as partial interpretations by induction on the relation ≻ on ground c-clauses.
First, we deﬁne:                          [
                                RS≺C :=        RSD .
                                         D≺C,D∈S

A ground c-clause C of the form l ≈ r∨C ▽ L is called productive if
 1. L is computable,
 2. l ≈ r∨C is false in RS≺C ,
 3. if l ≈ r∨C is not computable, then all literals in L are false in RS≺C ,
 4. l ≈ r is strictly maximal in C,
 5. l ≻ r,
 6. C is false in RS≺C ∪{l → r},
 7. l is irreducible in RS≺C .
In this case, we also say that C produces the rule l → r. Now we deﬁne
                            ≺C
                             RS ∪{l → r}, if C produces l → r;
                    RSC :=
                             RS≺C ,          otherwise.
Finally, we deﬁne the total interpretation RS for S as C∈S RSC . As usual, an
                                                            S
interpretation which satisﬁes a set of c-clauses S is called a model of S.  ❏
We state two standard properties about the model.
Lemma 3. Let S be a set of ground c-clauses.
 1. RS is a convergent rewrite system.
 2. RSC  C if and only if for all D ≻ C we have RSD  C, if and only if RS  C.
We will construct a model for a set which is saturated up to redundancy and ab-
stracted, with the following redundancy notions.
Deﬁnition 11 (Redundant answer clause/inference). An answer clause C
is redundant w.r.t. S if every ground instance of C follows from smaller ground
instances in S. Let N be the set of all ground instances of answer clauses in S. An
inference C1 ,...,Cn ⊢ D is redundant w.r.t. S if for each θ grounding for C1 ,...,Cn
and D either
 1. Dθ ≻ Ci θ for some 1 ≤ i ≤ n, or
 2. Dθ follows from the set {C | C ∈ N and Ci θ ≻ C for some 1 ≤ i ≤ n}.           ❏
Deﬁnition 12 (Saturation up to redundancy, abstracted set). A set of
answer clauses S is saturated up to redundancy if, given non-redundant answer
clauses C1 ,...,Cn ∈ S, any SUPRA inference C1 ,...,Cn ⊢ D is redundant w.r.t. S.
If there is no clause C ∈ S on which Abs would apply, then we call S abstracted. ❏
                                 Completeness of Synthesis under Realizability        13

In the remainder of this section, we assume Λ = hΣc ,∀x̄.∃y.F [x̄,y]i to be a ﬁxed but
arbitrary speciﬁcation, and S a set of answer clauses saturated up to redundancy
from Λ and abstracted. We assume JpK ∈    / S for any p ∈ P. Note that the set of all
ground instances of S might be unsatisﬁable even if there is no computable solution
for the speciﬁcation, just an uncomputable one. Therefore, we cannot show refu-
tational completeness of SUPRA. Instead, we show that from S, we can construct
a counter-model for any computable program being a solution to Λ. Formally, we
show that given any ground computable program term t[ᾱ] (possibly using ite),
the formula cnf(¬F [ᾱ,t]) is satisﬁable. Towards this, we ﬁrst eliminate ite from
answer clauses C1 JtK,...,Cm JtK coming from preprocessing, resulting in c-clauses.

Deﬁnition 13 (ite normal form). Let C = C[y]JyK be an answer clause and t a
program term. The ite normal form of C w.r.t. t, denoted iteNF(C,t), is the set of
c-clauses deﬁned inductively as follows:

 1. If C[y] contains y and t is of the form ite(L,s1 ,s2 ), then it is

            {D ▽ L̂L | D ▽ L ∈ iteNF(C,s1 )}∪{D ▽ LL | D ▽ L ∈ iteNF(C,s2 )},

 2. otherwise, it is {C[t]H}.                                                         ❏

Intuitively, we obtain a c-clause C[s] ▽ L by elimination of ite from CJtK when L
is the list of negations of ite-conditions needed to reach the branch term s in t.
    For any ground computable program term t, we construct a set of ground c-
clauses S ′ such that if S ′ is satisﬁable, then cnf(¬F [ᾱ,t]) is also satisﬁable. Then,
we show that the total model RS′ satisﬁes S ′ . The computable part of S ′ is deﬁned
as follows.

Deﬁnition 14 (Computable grounding). We deﬁne the computable ground-
ing of S, denoted cGr(S), as the set of c-clauses that contains:

 1. all computable ground instances of c-clauses in iteNF(C, t′ ) for all C in the
    initial set of Λ and program terms t′ , and
 2. all computable ground c-clause instances of answer clauses in S.            ❏

We prove that the model RcGr(S) satisﬁes all computable clauses in cGr(S). The
proof is very similar to standard completeness proofs, since the rules of SUPRA
for computable clauses correspond to the standard superposition rules: we do not
apply any extra restrictions to inferences between computable clauses, and any
inference between them results in a computable clause. By induction on ≻ over
c-clauses, we obtain the following.
                 / S for any computable p ∈ P, then RcGr(S)  C for all
Lemma 4. If JpK ∈
C ∈ cGr(S).
To obtain S ′ , we extend the set cGr(S) with uncomputable ground clauses. This
set also depends on a computable program term t, and is called a grounding of S
w.r.t. t.
14      Hajdu, Hozzová, Kovács, Wagner

Deﬁnition 15 (Grounding w.r.t. a program term). Let t ∈ P be ground
and t′ be the normal form of t w.r.t. RcGr(S) . We deﬁne the grounding of S w.r.t.
program term t, denoted Gr(S,t). In parallel, we deﬁne the derivation length for
each uncomputable C in Gr(S,t), denoted dl(C).
We deﬁne Gr(S,t) as the minimal set of c-clauses containing cGr(S) such that:
 1. For any answer clause C in the initial set of Λ, the set Gr(S,t) contains all
    ground instances of c-clauses in iteNF(C,t′ ).
    For any C added to Gr(S,t) by this step, we deﬁne dl(C) = 0.
 2. For any inference C1 Jp1 K, ... , Cn Jpn K ⊢ CJpKσ such that Ci Jpi K ∈ S for all
    1 ≤ i ≤ n, and CJpK ∈ S, if there is a substitution θ such that σθ = θ, Gr(S,t) con-
    tains uncomputable c-clauses C1 θ ▽ L1 ,...,Cn θ ▽ Ln , and there is j, 1 ≤ j ≤ n,
    such that for all 1 ≤ i ≤ n, either Li = ǫ, or Li = Lj , then Cθ ▽ Lj is in Gr(S,t).
    Take the inference and θ such that max(dl(C1 θ ▽ L1 ), ... , dl(Cn θ ▽ Ln )) is
    minimal. We deﬁne dl(Cθ ▽ Lj ) = max(dl(C1 θ ▽ L1 ),...,dl(Cn θ ▽ Ln ))+1. ❏
In the remainder of this section, we assume that t is an arbitrary but ﬁxed ground
computable program term. One key step in our main result is to show that infer-
ences between uncomputable answer clauses with non-uniﬁable answers are not
needed for a refutation that yields a computable answer. Towards this, we prove
the following lemma about the grounding of S w.r.t. t, using induction on the
derivation length of c-clauses.
Lemma 5. There is a set of lists of computable ground literals ∆ that satisﬁes the
following properties:
 1. Any uncomputable C ∈ Gr(S,t) is of the form C ▽ L where L ∈ ∆∪{ǫ}.
 2. For any L ∈ ∆∪{ǫ}, there is a ground computable simple term tL such that for
    any uncomputable C ′ ▽ L ∈ Gr(S,t), substitution θ, and clause CJpK ∈ S such
    that Cθ = C ′ , it holds that p is a simple term and pθ = tL or p is a variable not
    in C.
         / ∆, then for any uncomputable C ′ H ∈ Gr(S,t), substitution θ, and clause
 3. If ǫ ∈
    CJpK ∈ S such that Cθ = C ′ , it holds that p is a variable not in C.
 4. For any L,K ∈ ∆ such that L =    6 K, L and K contain a complementary literal.
Intuitively, any list of literals L in ∆ corresponds to the negation of ite-conditions
needed to reach some branch term, i.e. a simple term s in t. The lemma states that:
 (i) Any c-clause C in Gr(S,t) represents an instance of an answer clause CJpK in
     S with either the empty condition, meaning that p is any program term not
     depending on C, or with some conditions L in ∆ such that s is an instance of p.
(ii) Any two lists of conditions in ∆ contain a pair of complementary literals.
This ensures that inferences between uncomputable c-clauses corresponding to
diﬀerent branches from t are not needed, because if one of them is productive
(Deﬁnition 10), the other one is necessarily satisﬁed by the model. Now we can
prove that RGr(S,t) , obtained by extending RcGr(S) with uncomputable clauses,
is a model of Gr(S,t), and thus also of ¬F [ᾱ,t].
                                 Completeness of Synthesis under Realizability         15

Lemma 6. If Jp[ᾱ]K ∈    / S for any computable program term p[ᾱ], then the formula
¬F [ᾱ,t] is satisﬁable for any ground computable program term t.
We conclude this section with the proof of our main result.
Proof (of Theorem 2). Since Λ is realizable, there is a program term t[x̄] with no
variables except for x̄, such that ∀x̄.F [x̄,t[x̄]] is valid. By contraposition of Lemma 6
it then follows that Jp[ᾱ]K ∈ S for an abstracted set S saturated up to redundancy
from Λ. Since SUPRA and Abs are sound (Theorem 1), p[x̄] is a solution to Λ. ❏


6    Related Work

Saturation-Based Synthesis. A saturation-based solution to the synthesis of recursion-
free programs is introduced in [14]. We show that [14] is not complete. We introduce
the SUPRA calculus to simplify the reasoning of [14], as (i) we assume all clauses
to be answer clauses, and (ii) use most general uniﬁers instead of the arbitrary
computable uniﬁers of [14] in inferences. Further, (iii) SUPRA implements a new
abstraction rule Abs, needed for completeness under realizability assumptions.

Deductive Approaches to Synthesis. Our work, as well as [12,14], are based on the
deductive synthesis approach of [19], adapted for resolution [17]. The mechanism
in [29] restricts allowed programs, and subsumes our computability restrictions.
    The work of [14] extends [12] with induction to support synthesis of recursive
programs, with a proof of soundness and implementation, but without any com-
pleteness guarantees. Our notion of realizability does not cover recursive programs,
as their construction requires a mechanism for deﬁning new functions not included
in the computable symbols we work with.
    A practical approach for synthesis in the presence of uncomputable symbols uses
quantiﬁer elimination and SMT solving [13], and requires F [x̄,y] to be quantiﬁer-
free in (2) but may use linear arithmetic. The approach is complete only when
F [x̄,y] uses theories that admit quantiﬁer elimination, which excludes e.g. equal-
ities or uninterpreted functions.
    The SyGuS [2] format allows specifying programs in a fragment of ﬁrst-order
logic extended by theories and optionally a grammar for the sought programs.
Some prominent SyGuS solvers are cvc5 [25] and DryadSynth [15], as evidenced
by the SyGuS competition [3]. Component-based synthesis methods construct pro-
grams from logical speciﬁcations using a predeﬁned set of functions. The approach
of [28] is deductive, while [9, 30] use SMT solving. The GAPT framework [6] syn-
thesizes programs from proofs, by computing witnesses of second-order formulas
with quantiﬁer elimination [1], or by extracting programs from natural deduction
proofs in classical logic [26].

Related Completeness Results. Our completeness proof is inspired by standard
completeness proofs for superposition [22]. Yet, our model construction only works
for groundings that substitute computable program terms into the speciﬁcation
due to realizability assumptions. This relates our work to [29]. Finally, [31] proved
16      Hajdu, Hozzová, Kovács, Wagner

that a general synthesis system for recursive programs cannot exist. This does
not contradict our ﬁndings, as we claim completeness under the assumption that
a program exists.

Restricted Inferences. A rule similar to Abs is used in [4, 22] to disallow super-
positions into certain terms, while [5] introduces uniﬁcation constraints to the
clause level that are similar to abstracted terms. In [24], the uniﬁcation algorithm
is extended by abstraction to enhance theory reasoning within superposition, ab-
stracting terms on demand to enable inferences while postponing expensive theory
reasoning.


7    Summary and Outlook
We tackle program synthesis and introduce the SUPRA calculus for saturation-
based proof search. Our calculus revises [14] by using an abstract uniﬁcation rule,
which unravels computable subterms from uncomputable literals such that uncom-
putable literals can be resolved without disobeying the computability constraint
of the calculus. We also use speciﬁc simpliﬁcation orders and selection functions in
SUPRA, ensuring that uncomputable literals are always selected if there are any in
a clause. SUPRA changes the notion of clauses with answer literals to constrained
clauses to make reasoning simpler. Not only do these adaptions retain soundness
of SUPRA, but they enable proving completeness of SUPRA under the assump-
tion that synthesis speciﬁcations have a solution. A natural direction for future
work is investigating completeness under realizability assumption for synthesis of
recursive functions using calculi that make use of induction.

Acknowledgements. This research was funded in whole or in part by the
ERC Consolidator Grant ARTIST 101002685, the Austrian Science Fund (FWF)
10.55776/DOC1345324, and the SBA Research COMET Center SBA-K1 NGC
managed by the FFG.

Disclosure of Interests. The authors have no competing interests to declare
that are relevant to the content of this article.


References
 1. Achammer, F., Hetzl, S., Schmidt, R.: Computing Witnesses Using the SCAN Algo-
    rithm. In: CADE (2025), https://dl.acm.org/doi/10.1007/978-3-031-99984-0_27
 2. Alur, R., Bodík, R., Dallal, E., Fisman, D., Garg, P., Juniwal, G., Kress-Gazit,
    H., Madhusudan, P., Martin, M.M.K., Raghothaman, M., Saha, S., Seshia,
    S.A., Singh, R., Solar-Lezama, A., Torlak, E., Udupa, A.: Syntax-Guided
    Synthesis. In: Dependable Software Systems Engineering. IOS Press (2015).
    https://doi.org/10.3233/978-1-61499-495-4-1
 3. Alur, R., Fisman, D., Padhi, S., Reynolds, A., Singh, R., Udupa, A.: SyGuS-Comp
    2019. https://sygus.org/comp/2019/
                                  Completeness of Synthesis under Realizability          17

 4. Bachmair, L., Ganzinger, H., Waldmann, U.: Refutational theorem prov-
    ing for hierarchic ﬁrst-order theories. In: AAECC 5, 193–212 (1994).
    https://doi.org/10.1007/BF01190829
 5. Bhayat, A., Schoisswohl, J., Rawson, M.: Superposition with Delayed Uniﬁcation.
    In: CADE (2023). https://doi.org/10.1007/978-3-031-38499-8_2
 6. Ebner, G., Hetzl, S., Reis, G., Riener, M., Wolfsteiner, S., Zivota, S.: System Descrip-
    tion: GAPT 2.0. In: IJCAR (2016). https://doi.org/10.1007/978-3-319-40229-1_20
 7. Green, C.: Theorem-Proving by Resolution as a Basis for Question-Answering
    Systems. Machine Intelligence 4, 183–205 (1969)
 8. Gulwani, S.: Automating string processing in spreadsheets using input-output
    examples. In: POPL (2011). https://doi.org/10.1145/1926385.1926423
 9. Gulwani, S., Jha, S., Tiwari, A., Venkatesan, R.: Synthesis of Loop-Free Programs.
    In: PLDI (2011). https://doi.org/10.1145/1993498.1993506
10. Gulwani, S., Jojic, N.: Probabilistic inference of programs from input/output
    examples (2006), https://api.semanticscholar.org/CorpusID:59650668
11. Hozzová, P.: Integrating Answer Literals with AVATAR for Program Synthesis. In:
    Proc. of the 7th and 8th Vampire Workshop (2024). https://doi.org/10.29007/vmn9
12. Hozzová, P., Amrollahi, D., Hajdu, M., Kovács, L., Voronkov, A., Wagner, E.M.:
    Synthesis of Recursive Programs in Saturation. In: Automated Reasoning (2024).
    https://doi.org/10.1007/978-3-031-63498-7_10
13. Hozzová, P., Bjørner, N.: Synthesiz3 This: an SMT-Based Approach
    for    Synthesis      with   Uncomputable      Symbols.       In:    FMCAD       (2025).
    https://doi.org/10.34727/2025/isbn.978-3-85448-084-6_28
14. Hozzová, P., Kovács, L., Norman, C., Voronkov, A.: Program Synthesis in Saturation.
    In: CADE (2023). https://doi.org/10.1007/978-3-031-38499-8_18
15. Huang, K., Qiu, X., Shen, P., Wang, Y.: Reconciling Enumerative and Deductive
    Program Synthesis. In: PLDI (2020). https://doi.org/10.1145/3385412.3386027
16. Kovács, L., Moser, G., Voronkov, A.: On Transﬁnite Knuth-Bendix Orders. In:
    CADE (2011). https://doi.org/10.1007/978-3-642-22438-6_29
17. Lee, R.C.T., Waldinger, R.J., Chang, C.L.: An Improved Program-
    Synthesizing Algorithm and Its Correctness. Communications of ACM (1974).
    https://doi.org/10.1145/360924.360967
18. Li, Y., Parsert, J., Polgreen, E.: Guiding Enumerative Program Synthesis with Large
    Language Models. In: CAV (2024). https://doi.org/10.1007/978-3-031-65630-9_15
19. Manna, Z., Waldinger, R.: A Deductive Approach to Program Synthesis. TOPLAS
    (1980). https://doi.org/10.1145/357084.357090
20. Newman, M.H.A.: On Theories with a Combinatorial Deﬁnition of "Equivalence.".
    Journal of Symbolic Logic (1942). https://doi.org/10.2307/2269299
21. Nieuwenhuis, R., Rubio, A.: Paramodulation-Based Theorem Proving. In:
    Handbook of Automated Reasonings. Elsevier and MIT Press (2001).
    https://doi.org/10.1016/B978-044450813-3/50009-6
22. Nieuwenhuis, R., Rubio, A.: Basic superposition is complete. In: Krieg-Brückner, B.
    (ed.) ESOP ’92 (1992). https://doi.org/10.1007/3-540-55253-7_22
23. Reger, G.: Revisiting Question Answering in Vampire. In: 4th Vampire Workshop
    (2018). https://doi.org/10.29007/fjc4
24. Reger, G., Suda, M., Voronkov, A.: Uniﬁcation with Abstraction and
    Theory Instantiation in Saturation-Based Reasoning. In: TACAS (2018).
    https://doi.org/10.1007/978-3-319-89960-2_1
25. Reynolds, A., Kuncak, V., Tinelli, C., Barrett, C., Deters, M.: Refutation-
    based Synthesis in SMT. Formal Methods in System Design (2019).
    https://doi.org/10.1007/s10703-017-0270-2
18      Hajdu, Hozzová, Kovács, Wagner

26. Rietdijk, M.: Extracting programs from proofs using Friedman’s A-translation and
    realizability (2018), https://repositum.tuwien.at/handle/20.500.12708/8452
27. Singh, R., Gulwani, S.: Synthesizing Number Transformations from Input-Output
    Examples. In: CAV (2012). https://doi.org/10.1007/978-3-642-31424-7_44
28. Stickel, M., Waldinger, R., Lowry, M., Pressburger, T., Underwood, I.: Deductive
    composition of astronomical software from subroutine libraries. In: CADE (1994).
    https://doi.org/10.1007/3-540-58156-1_24
29. Tammet, T.: Completeness of resolution for deﬁnite answers with case analysis. In:
    Computer Science Logic (1995). https://doi.org/10.1007/BFb0022265
30. Tiwari, A., Gascón, A., Dutertre, B.: Program Synthesis Using Dual Interpretation.
    In: CADE (2015), 10.1007/978-3-319-21401-6_33
31. Voronkov, A.: On completeness of program synthesis systems. In: Computer Science
    Logic (1992). https://doi.org/10.1007/BFb0023785
                                 Completeness of Synthesis under Realizability         19

Appendix

A     Proofs from Section 4

Theorem 1 (Soundness). The SUPRA calculus is sound with respect to the
semantics of answer clauses.

Proof. We prove soundness for the rules EqRes and SupC . For the other rules the
proofs are analogous.
   By cl(G) we denote the universal closure of the formula G. When v is a variable
assignment, by v(x) we denote the value it assigns to the value x. When I is an
interpretation, by I(t) we denote the value by which it interprets the term t.
   The semantics of answer clauses were deﬁned as follows: an interpretation I
satisﬁes an answer clause CJpK w.r.t. a given speciﬁcation Λ if I  cl(C ∨ F [ᾱ,p])
for fresh constants ᾱ. For any rule of SUPRA,

                                 C1 Jp1 K    ... Cn Jpn K ,
                                            CJpKσ
we have to show that if (i) I  cl(C1 ∨ F [ᾱ,p1 ]),...,I  cl(Cn ∨ F [ᾱ,pn ]), then (ii)
I  cl(Cσ∨F [ᾱ,pσ]). We prove this by contradiction: assume (i) holds but (ii) does
not. Then there exists a variable assignment v such that I extended by v, denoted
Iv , does not satisfy Cσ∨F [ᾱ,pσ]. Therefore, Iv 6 Cσ and Iv 6 F [ᾱ,pσ].
    Recall the rule EqRes:
                            s 6≈ t∨CJpK              (1) σ = mgu(s,t)
                  (EqRes)                    where
                               CJpKσ                 (2) pσ is computable
For EqRes, we assume (i) Iu  s 6≈ t∨C ∨F [ᾱ,p] for any variable assignment u and
(ii) Iv 6 Cσ and Iv 6 F [ᾱ,pσ]. We construct a variable assignment v ′ such that
v ′ (x) = Iv (xσ) for each variable x occurring in s 6≈ t∨CJpK, and v ′ (z) = v(z) for all
other variables z. Since σ uniﬁes s and t, we get Iv′ 6 s 6≈ t. Further, from Iv 6 Cσ
we get Iv′ 6 C. Hence, from (i) follows that Iv′  F [ᾱ, p]. Now, in Deﬁnition 6
we assumed that F [ᾱ,y] and CJpK do not have any common variables. Therefore
Iv′ (p) = Iv (pσ), and thus from (ii) and the deﬁnition of v ′ we get Iv′ 6 F [ᾱ,p]. We
derived a contradiction, EqRes is therefore sound.
     Recall now the rule SupC :
                                                      (1) σ = mgu(l,l′ )
            l ≈ r∨CJpK       s[l′ ] ≈
                                    ˙ t∨DJqK          (2) l′ is not a variable
  (SupC )                                       where
                 ˙ t∨C ∨DJite(l ≈ r,q,p)Kσ
            s[r] ≈                                    (3) rσ  lσ, tσ  s[l′ ]σ
                                                      (4) ite(l ≈ r,q,p)σ is computable
For SupC , we assume (i) Iu  l ≈ r ∨ C ∨ F [ᾱ,p], Iu  s[l′ ] ≈
                                                                ˙ t ∨ D ∨ F [ᾱ,q] for any
variable assignment u and (ii) Iv 6 (s[r] ≈ ˙ t∨C ∨D)σ and Iv 6 F [ᾱ,ite(l ≈ r,q,p)σ]
for some variable assignment v. We construct a variable assignment v ′ such that
v ′ (x) = Iv (xσ) for each variable x occurring in l ≈ r ∨ CJpK and s[l′ ] ≈   ˙ t ∨ DJqK,
and v ′ (z) = v(z) for all other variables z. Then from Iv 6 (s[r] ≈˙ t∨C ∨D)σ we get
20       Hajdu, Hozzová, Kovács, Wagner

            ˙ t∨C ∨D. We have two cases, either Iv′  l ≈ r or Iv′ 6 l ≈ r. Assume the
Iv′ 6 s[r] ≈
ﬁrst, then from Iv′ 6 s[r] ≈ ˙ t, also Iv′ 6 s[l′ ] ≈
                                                      ˙ t (the evaluation of l and l′ under v ′ is
                                              ′
the same since σ is a uniﬁer of l and l ), hence (i) implies Iv′  F [ᾱ,q]. We evaluate
Iv′ (ite(l ≈ r,q,p) = Iv′ (q) = Iv (qσ), and note that we assumed that answer clauses
CJpK do not have common variables with F [ᾱ,y], thus from (ii) we get Iv′ 6 F [ᾱ,q],
contradiction.
    Similarly, the second case, Iv′ 6 l ≈ r, implies Iv′  F [ᾱ, p]. From Iv′ (ite(l ≈
r,q,p) = Iv′ (p) = Iv (pσ) and (ii) we derive the contradiction Iv′ 6 F [ᾱ,p].
    Hence, SupC is sound.                                                                       ❏

Corollary 1 (Solution to the Synthesis Problem). Given a synthesis speci-
ﬁcation Λ = hΣc ,∀x̄∃y.F [x̄,y]i, if SUPRA derives Jp[ᾱ]K from the initial set of Λ,
then p[x̄] is a solution for Λ.

Proof. We ﬁrst show that all answer clauses in the initial set S0 from Λ hold (Def-
inition 6). The initial set S0 is cnf(¬F [ᾱ,y])JyK. Each answer clause in S0 is thus
of the form CJyK, where C ∈ cnf(¬F [ᾱ,y]).
    We will show that C ∨F [ᾱ,y] is true in any interpretation I under any variable
assignment v. The formula ¬F [ᾱ,y] is either true or false in I under v. If ¬F [ᾱ,y]
is true in I under v, and C ∈ cnf(¬F [ᾱ,y]), also C is true in I under v. Thus,
C ∨F [ᾱ,y] is true too. On the other hand, if ¬F [ᾱ,y] is false in I under v, it means
that its negation F [ᾱ,y] is true in I under v. Then C ∨F [ᾱ,y] is true too. It follows
that C ∨F [ᾱ,y] is true in any interpretation and any variable assignment, therefore
it holds, and thus also CJyK holds.
    We have shown that we start saturation with a set of valid answer clauses. Since
each inference by SUPRA is sound by Theorem 1, all answer clauses derived in
saturation are also valid. Then, if Jp[ᾱ]K is derived, it is valid, meaning that
 ∨F [ᾱ,p[ᾱ]] holds. Further,  ∨F [ᾱ,p[ᾱ]] is equivalent to F [ᾱ,p[ᾱ]], which thus
also holds. Finally, since ᾱ were fresh Skolem constants, it follows that ∀x̄.F [x̄,p[x̄]]
is valid too, meaning that p[x̄] is a solution for Λ.                                   ❏

Lemma 1. The rule Abs is sound with respect to the semantics of answer clauses.

Proof. The soundness of Abs is given as follows. Let I be an interpretation that
                 ˙ t ∨ CJpK). If I satisﬁes cl(s[k] ≈
satisﬁes cl(s[k] ≈                                   ˙ t) but not cl(x 6≈ k) it satisﬁes
        ˙ t). Conversely, if it does not satisfy cl(s[x] ≈
cl(s[x] ≈                                                 ˙ t) it satisﬁes cl(x 6≈ k). If I
satisﬁes cl(C) or cl(F [ᾱ,p]) the conclusion trivially holds.                           ❏

Lemma 2. Condition (2) of rule Abs holds iﬀ (2a) k is computable, and (2b) ei-
ther s[k] is uncomputable, or it contains a variable not contained in k, and there
exists at least one uncomputable term.

Proof. Suppose condition (2) holds. From kθ being computable follows that k is
computable too and thus (2a) holds. Further, s[k]θ is uncomputable. Either s[k] is
uncomputable too, or the uncomputable symbol was introduced as a part of some
term u by {y 7→ u} ⊆ θ for some y. In the latter case, since kθ is computable, we
know that y must occur in s[k] but not in k. Thus (2b) holds too.
                                  Completeness of Synthesis under Realizability          21

   Suppose now conditions (2a) and (2b) hold. If s[k] is uncomputable, the empty
substitution satisﬁes condition (2). Otherwise s[k] contains some variable y not
occurring in k. Then θ = {y 7→ u} for an arbitrary uncomputable term u satisﬁes
condition (2).                                                                ❏


B      Orderings
B.1     Orderings and selection
The following lemmas state that for these types of LPOs any uncomputable term,
literal or clause cannot be smaller than or equal to any computable term, literal
or clause respectively.
Lemma 7. For a signature Σ = Σc ⊎ Σu , an LPO with a precedence relation
≫, such that every k ∈ Σu has higher precedence than any k ′ ∈ Σc , and terms
s ∈ Tc , t ∈ Tu it holds that s lpo t.
Proof. Note that s 6= t, because t contains an uncomputable symbol while s does
not. We still need to prove that s ⊁lpo t. We prove this by induction over the term
t. Term t cannot be a variable, so case 1 in the deﬁnition of LPO is trivially never
fulﬁlled.

Base case. The topmost symbol of term t is uncomputable; top(t) ∈ Σu 7 . Assume
by contradiction that s ≻lpo t. Let s′ be smallest subterm of s such that s′ ≻lpo t.
By deﬁnition top(t) ≫ top(s′ ), neither case 2 nor 3 can hold, contradiction.

Induction step. Let t = f (t1 , ... tj−1 , tj , tj+1 ... , tn ) where top(tj ) ∈ Σu . Assume
by contradiction that s ≻lpo t. Let s′ be smallest subterm of s such that s′ ≻lpo t.
Because s′ ⊁lpo tj neither case 3 nor 4 can hold, contradiction.                           ❏
  The next Lemma immediately highlights that we don’t lose the property from
Lemma 7 using bag extensions.
Lemma 8. Assume that for two bags {x1 , ... , xn } and {y1 , ... , ym } there is j ∈
{1,...,m} such that for any i ∈ {1,...,n} it holds that xi  yj . Then {x1 ,...,xn } bag
{y1 ,...,ym }.
Proof. Assume by contradiction that {x1 , ... , xn } bag {y1 , ... , ym }. By deﬁni-
tion of the bag extension {y1 , ... , ym } bag {yj }. By transitivity this implies
{x1 , ... , xn } bag {yj }. But this can only be if there is i ∈ {1, ... , n} such that
xi  yj . By assumption this cannot be the case.                                      ❏
    The next two Lemmas follow very easily from Lemma 8.
Lemma 9. Let L1 ,L2 be two literals, where L1 is uncomputable and L2 is com-
putable. By ≻ we denote the bag extension of an LPO with a precedence relation ≫
such that every k ∈ Σu has higher precedence than any k ′ ∈ Σc . Then L2  L1 , i.e.
for an uncomputable clause C at least one uncomputable literal in C is maximal.
7
    By top(t) we denote the topmost symbol of term t.
22        Hajdu, Hozzová, Kovács, Wagner

Proof. We have already shown that uncomputable terms cannot be smaller than
computable terms. Therefore by Lemma 8 L2  L1 .                          ❏

Lemma 10. Let C1 ,C2 be two clauses, where C1 is uncomputable and C2 is com-
putable. By ≻ we denote the bag extension of literals of the bag extension of an
LPO with a precedence relation ≫ such that every k ∈ Σu has higher precedence
than any k ′ ∈ Σc . Then C2  C1 .

Proof. We have already shown that uncomputable literals cannot be smaller than
computable literals. Therefore by Lemma 9 C2  C1 .                          ❏

B.2      Knuth-Bendix orders
In the following we give an extended deﬁnition for Knuth-Bendix orders that can
also be used with SUPRA. A transﬁnite weight function is a function w from
Σ = Σc ⊎ Σu to the union of the ordinals ω ∪ ω1 , where ω := {0, 1, 2, ... } and
ω1 = {ω + 1,ω + 2,...} such that w(Σc ) ⊆ ω and w(Σu ) ⊆ ω1 8 . We will refer to
w(f ) as the weight of f . We denote by w0 the smallest weight of constants. For
p ∈ Σ ∪ V, we write |t|p to denote the number of occurrences of p in term t. For
example, |f (x,x)|f = 1, |f (x,x)|x = 2 and |f (x,x)|y = 0. Let P(V) be the set of
linear expressions over V with integer coeﬃcients. The weight of a term t, denoted
by |t|, is a linear expression in P(V) deﬁned as:
                                   X              X
                            |t| :=   |t|f ·w(f )+   |t|x ·x,
                                   f ∈Σ            x∈V

where arithmetic (i.e. +,·,<) on ordinal numbers is deﬁned in the standard way. A
substitution σ can also be considered as mapping from linear expressions to linear
expressions, as follows:

              σ(α0 +α1 ·x1 +...+αn ·xn ) := α0 +α1 ·|x1 σ|+...+αn ·|xn σ|.

For example, if w(f ) = 2, w(a) = 1 and σ = {x 7→ a}, then |f (x,x)| = 2 · x + 2 and
σ(|f (x,x)|) = σ(2·x+2) = 2·|xσ|+2 = 4. It is not hard to argue that |tσ| = σ(|t|).
Let e ∈ P(V) be a linear expression. We call a substitution σ grounding for e if
σ(e) does not contain variables. We write e1 > e2 if σ(e1 ) > σ(e2 ) for all grounding
substitutions σ for e1 and e2 . We write e1 & e2 if σ(e1 ) ≥ σ(e2 ) for all grounding
substitutions σ for e1 and e2 .
   The transﬁnite Knuth-Bendix order (tKBO) [16]9 , denoted by ≻tkbo , is parame-
terized by a precedence relation ≫ and a transﬁnite weight function w. For terms
s,t, we have s ≻tkbo t if:
 1. |s| > |t|, or
8
     we denote with f (A) the image of a function, where f : X → Y and A ⊆ X.
9
     Note that this deﬁnition is only a speciﬁc instance of the family of transﬁnite KBOs
     given in [16] but similar properties hold.
                                  Completeness of Synthesis under Realizability          23

 2. |s| & |t|, s = f (s1 ,...,sn ), t = g(t1 ,...,tm ) and f ≫ g, or
 3. |s| & |t|, s = f (s1 ,...,sn ), t = f (t1 ,...,tn ) and there exists 1 ≤ i ≤ n such that
    si ≻tkbo ti and sj = tj for all 1 ≤ j < i.

    The transﬁnite KBO is a simpliﬁcation order for any precedence relation ≫
and transﬁnite weight function w, if w0 > 0 and f ≫ g for all g ∈ Σ diﬀerent from
f , for all unary f ∈ Σ with w(f ) = 0 [16].


Lemma 11. For a signature Σ = Σc ⊎ Σu , a transﬁnite KBO on Σ and terms
s ∈ Tc , t ∈ Tu it holds that s tkbo t.

Proof. The term t contains an uncomputable symbol, while s does not, therefore
s 6= t. Assume further that s ≻tkbo t. This implies that |s| & |t|. Therefore for any
grounding substitution σ it holds that σ(|s|) ≥ σ(|t|). In particular σ(|s|) ≥ σ(|t|)
for any substitution σ that maps variables to only computable terms. This cannot
be the case because by assumption σ(|s|) ∈ ω0 and σ(|t|) ∈ ω1 .                    ❏

Remark 3. In particular computable expressions (literals or clauses) can never be
bigger than uncomputable expressions using transﬁnite KBOs, see Lemma 8,9,10.


C     Proofs from Section 5

Lemma 3. Let S be a set of ground c-clauses.

 1. RS is a convergent rewrite system.
 2. RSC  C if and only if for all D ≻ C we have RSD  C, if and only if RS  C.

Proof. Towards the ﬁrst property, ﬁrst, we prove that the rewrite relation of RS
is terminating. RS terminates since l ≻ r for all its rules l → r by condition 5 of
Deﬁnition 10.
    Second, we prove that the rewrite relation of RS is conﬂuent. Newman’s lemma
states that every terminating and locally conﬂuent term rewriting system is con-
ﬂuent [20]. Using Newman’s lemma, it suﬃces to show local conﬂuence. Since all
rules in RS are ground, it is enough to show that the rules are non-overlapping, i.e.
that there are no two diﬀerent rules l → r and l′ → r′ in RS where l′ is a subterm
of l. Let C be a c-clause that produces a rule l → r. By condition 7 of Deﬁnition 10,
RSC cannot contain any rule l′ → r′ s.t. l′ is a subterm of l. Suppose that some l′ → r′
is produced by a c-clause D ≻ C s.t. l′ is a subterm of l. Since l′ is maximal in D
(condition 4 and 5 of Deﬁnition 10), we have l′ ≻ l, hence l′ cannot be a subterm
of l (using the subterm property of ≻).
    Towards the second property, suppose that RSC  C due to a positive literal s ≈ t
in C with RSC  s ≈ t. For any clause D ≻ C, we have RS ⊇ RSD ⊇ RSC . This implies that
RSD  s ≈ t and RS  s ≈ t, hence RSD  C and RS  C. Otherwise, there is a negative
literal s 6≈ t in C and RSC 2 s ≈ t. W.l.o.g. assume s ≻ t. For any clause D ≻ C that
produces a rewrite rule l → r, l cannot be a subterm of s, hence no rule in RSD (or RS )
can rewrite s. Since RS is convergent (by property 1), this means that RS 2 s ≈ t.❏
24       Hajdu, Hozzová, Kovács, Wagner

                 / S for any computable p ∈ P, then RcGr(S)  C for all
Lemma 4. If JpK ∈
C ∈ cGr(S).
Proof. The proof is by contradiction and by induction on ≻ over c-clauses. Sup-
pose there is a c-clause C ∈ cGr(S) such that (i) RcGr(S) 2 C and (ii) C is the
minimal such c-clause in cGr(S) w.r.t. ≻. We consider the following cases. 10
Case 1. C is of the form C ′ ▽ L where L is not empty.
Let D be the c-clause C ′ H, which is also in cGr(S). Moreover, C ≻ D and since
C ′ is false, RcGr(S) 2 D. Hence we have found a smaller false c-clause in cGr(S),
contradiction.
Case 2. C is of the form C ′ H and there is an answer clause CJpK in S and a
substitution θ s.t. Cθ = C ′ , and there is a variable x in C such that xθ is reducible
in RcGr(S) .
Let θ′ be the substitution θ, except that it maps x to the normal form of xθ w.r.t.
RcGr(S) , and let D be the c-clause Cθ′ H. We have D ∈ cGr(S) and since xθ ≻ xθ′
and C contains x, we have C ≻ D. Also, xθ′ is the normal form of xθ, so RcGr(S) 2 D
either. Thus, we have found a false clause smaller than C in cGr(S), contradiction.
Case 3. C is of the form s′ 6≈ t′ ∨C ′ H where s′ 6≈ t′ is maximal in s′ 6≈ t′ ∨C ′ .

Subcase 3.1. s′ = t′ .
Then there is an answer clause s 6≈ t∨CJpK in S, a ground substitution θ such that
(s 6≈ t∨C)θ = s′ 6≈ t′ ∨C ′ . Consider the following inference:

                                             s 6≈ t∨CJpK
                                  (EqRes)
                                               CJpKσ
where σ = mgu(s, t). Let D be the c-clause C ′ H. By sθ = tθ = s′ , we have
that θ is a uniﬁer of s and t. Since p and C are computable, the uniﬁer σ only
contains computable symbols in its range, hence pσ is also computable, satisfy-
ing condition 2 of EqRes. Therefore, CJpKσ ∈ S and thus D ∈ cGr(S). Due to
{{s′ ,s′ ,s′ ,s′ }}⊎C ′ ≻bag C ′ , we also have C ≻ D. Also, RcGr(S) 2 C ′ , so RcGr(S) 2 D.
Thus, we have found a smaller false c-clause in cGr(S), contradiction.
Subcase 3.2. W.l.o.g. s′ ≻ t′11 and s′ is reducible by some l′ → r′ ∈ RcGr(S) .
Then s′ is of the form s′ [l′ ] and there is a rule l′ → r′ in RcGr(S) produced by some
computable clause l′ ≈ r′ ∨D′ ▽ K. Note that we have K = ǫ, as l′ ≈ r′ ∨D′ ▽ K is
smaller than all clauses l′ ≈ r′ ∨D′ ▽ K′ where K′ is non-empty, therefore it must
produce the rule l′ → r′ . Then there are clauses s[k] 6≈ t∨CJpK and l ≈ r ∨DJqK in
S such that k is not a variable (see Case 2), and a ground substitution θ such that
lθ = kθ = l′ , (s[k] 6≈ t∨C)θ = s′ 6≈ t′ ∨C ′ and (l ≈ r∨D)θ = l′ ≈ r′ ∨D′ . Consider the
following inference:
10
   Note that in all cases we assume that all preceding cases do not hold, to make our
   case distinction simpler. Similarly in Lemma 6.
11
   Note that ≻ is total on ground terms.
                                       Completeness of Synthesis under Realizability          25

                                      l ≈ r∨DJqK             s[k] 6≈ t∨CJpK
                           (SupC )
                                       s[r] 6≈ t∨C ∨DJite(l ≈ r,p,q)Kσ
where σ = mgu(l,k). Since l′ ≈ r′ ∨ D′ is productive, Item 5 from Deﬁnition 10
and the assumption s′ ≻ t′ imply that rσ  lσ and tσ  s[k]σ (condition 3 of
the SupC rule). Also, since both c-clauses (and therefore both answer clauses) are
computable, ite(l ≈ r,p,q)σ must be also computable, satisfying condition 4 of the
SupC rule. Then, (s[r] 6≈ t∨C ∨D)σ ∈ S. Let D be the c-clause s′ [r′ ] 6≈ t′ ∨C ′ ∨D′ H.
Note that D ∈ cGr(S). Further, we have

               {{s′ [l′ ],s′ [l′ ],t′ ,t′ }}⊎C ′ ≻bag {{s′ [r′ ],s′ [r′ ],t′ ,t′ }}⊎C ′ ⊎D′

and hence C ≻ D. Also, RcGr(S) 2 D: (1) by assumption, C ′ and D′ are false in
RcGr(S) , and (2) s′ [l′ ] has the same normal form as t′ and s′ [r′ ], therefore t′ and
s′ [r′ ] have the same normal form too by conﬂuence. Thus, we have found a false
c-clause smaller than C in cGr(S), contradiction.
Subcase 3.3. W.l.o.g. s′ ≻ t′ and s′ is irreducible.
Then, since s′ ≻ t′ and s′ is in normal form, RcGr(S)  s′ 6≈ t′ and C is satisﬁed,
contradiction.
Case 4. C is of the form s′ ≈ t′ ∨C ′ H where s′ ≈ t′ is maximal in s′ ≈ t′ ∨C ′ .
W.l.o.g. s′ ≻ t′ .
Subcase 4.1. s′ is reducible by l′ → r′ ∈ RcGr(S) .
This is similar to Case 3.2. Then s′ is of the form s′ [l′ ] and l′ → r′ is produced by
some c-clause l′ ≈ r′ ∨ D′ H. There are clauses s[k] ≈ t ∨ CJpK and l ≈ r ∨ DJqK in
S, such that k is not a variable (see Case 2), a ground substitution θ such that
lθ = kθ = l′ , (s[k] ≈ t∨C)θ = s′ [l′ ] ≈ t′ ∨C ′ and (l ≈ r ∨D)θ = l′ ≈ r′ ∨D. Consider
the following inference:
                                      l ≈ r∨DJqK             s[k] ≈ t∨CJpK
                           (SupC )
                                       s[r] ≈ t∨C ∨DJite(l ≈ r,p,q)Kσ
where σ = mgu(l,k). Let D be the c-clause s′ [r′ ] ≈ t′ ∨ C ′ ∨ D′ H. We check the
conditions the SupC rule similarly as in Subcase 3.2. Therefore, s[r]∨C ∨DJite(l ≈
r,p,q)Kσ ∈ S and D ∈ cGr(S). We also have the following

                         {{s′ [l′ ],t′ }}⊎C ′ ≻bag {{s′ [r′ ],t′ }}⊎C ′ ⊎D′

and hence C ≻ D. Also, RcGr(S) 2 D: (1) by assumption, C ′ and D′ are false in
RcGr(S) , and (2) s′ [l′ ] have distinct normal forms with t′ , so s′ [r′ ] and t′ must have
distinct normal forms too (otherwise C would be true in RcGr(S) by conﬂuence).
Thus, we have found a false clause in S smaller than C.

Subcase 4.2. s′ is irreducible in RcGr(S) .
Then, C ′ is of the form s′ ≈ r′ ∨ D′ such that t′  r′ and s′ ≈ r′ is true in
 ≺C
RcGr(S) ∪ {s′ → t′ } (i.e. Item 6 of Deﬁnition 10 is violated). Note that this also
26      Hajdu, Hozzová, Kovács, Wagner

covers the case when Item 4 of Deﬁnition 10 is violated, as then t′ = r′ and C is of
the form s′ ≈ t′ ∨s′ ≈ t′ ∨D′ H.
   Then there is an answer clause s ≈ t∨l ≈ r∨DJpK in S, a ground substitution θ
such that (s ≈ t∨l ≈ r∨D)θ = s′ ≈ t′ ∨s′ ≈ r′ ∨D′ . Consider the following inference:
                                          s ≈ t∨l ≈ r∨DJpK
                             (EqFac)
                                         s ≈ t∨t 6≈ r∨DJpKσ
where σ = mgu(s,l). Let D be the c-clause s′ ≈ t′ ∨ t′ 6≈ r′ ∨ D′ . Since s′ ≻ t′ and
t′  r′ by assumption, condition 2 of the EqFac rule holds. Also, since p and C are
computable, the uniﬁer σ only contains computable symbols in its range, hence pσ
is also computable, satisfying condition 3 of EqFac. Then, s ≈ t∨t 6≈ r∨DJpKσ ∈ S
and D ∈ cGr(S). By s′ ≻ t′  r′ , we have the following

                {{s′ ,t′ },{s′ ,r′ }}⊎D′ ≻bag {{s′ ,t′ },{t′ ,t′ ,r′ ,r′ }}⊎D′

and hence C ≻ D. Also, RcGr(S) 2 (s′ ≈ t′ ∨t′ 6≈ r′ ∨D′ ): (1) by assumption, s′ ≈ t′
                                                                 ≺C
and D′ are false in RcGr(S) , and (2) since s′ ≈ r′ is true in RcGr(S)   ∪{s′ → t′ }, we
have that RcGr(S)  t′ ≈ r′ and therefore t′ 6≈ r′ is false in RcGr(S) . Thus, we have
found a false clause in cGr(S) smaller than C.                                         ❏
Lemma 12. Given a computable ground program term t, there is a set of lists of
computable literals ∆ that satisﬁes the following properties:
 1. For any answer clause C of the form C[x]JxK, any uncomputable c-clause in
    iteNF(C,t) is of the form C ▽ L, where L ∈ ∆∪{ǫ}.
 2. For any L ∈ ∆∪{ǫ}, there is a ground computable simple term tL such that for
    any answer clause C of the form C[x]JxK, uncomputable C ′ ▽ L ∈ iteNF(C,t),
    and substitution θ such that Cθ = C ′ , it holds that xθ = tL or x is a variable
    not in C.
 3. If ǫ ∈/ ∆, then for any answer clause C of the form C[x]JxK, uncomputable
    C ′ H ∈ iteNF(C,t), and substitution θ such that Cθ = C ′ , it holds that x is a
    variable not in C.
 4. For any L,K ∈ ∆ such that L = 6 K, L and K contain a complementary literal.
Proof. By induction on the structure of t.
Case 1. t is of the form ite(L,s,s′ ).
By the induction hypothesis, there are clause sets S and S ′ for program terms s and
s′ , respectively, that satisfy the four properties. We now prove that the following
computable ground clause set ∆ satisﬁes the properties for t:

                              {L̂L | L ∈ S}∪{LL | L ∈ S ′ }

Towards Item 1, let C be an answer clause of the form C[x]JxK. Suppose that C
does not contain x. Then, iteNF(C,t) is {CH} and the property is satisﬁed.
   Otherwise, we have by induction hypothesis that any clause in iteNF(C,s) (resp.
iteNF(C,s′ )) is of the form C ▽ L where L ∈ S ∪{ǫ} (resp. L ∈ S ′ ∪{ǫ}). By construc-
tion, any clause in ite(C,t) is either of the form D ▽ L̂L where D ▽ L ∈ iteNF(C,s)
                                 Completeness of Synthesis under Realizability        27

or D ▽ LK where D ▽ K ∈ iteNF(C,s′ ). Both L̂L and LK are in ∆, proving the ﬁrst
property.

Towards Item 2, let C be an answer clause of the form C[x]JxK and θ a substitution.
Suppose that C does not contain x. Then, iteNF(C, t) is the set {CH} and the
property trivially holds due to x being a variable not in C.
   Otherwise, by construction, any clause in iteNF(C, t) is one of the following
forms:

 1. D ▽ L̂L where D ▽ L ∈ iteNF(C,s): by induction hypothesis there is a ground
    computable term tL for D ▽ L such that xθ = tL or x is a variable not in C if
    C[x]θ = D. It follows trivially for D ▽ L̂L, too and we set tL̂∨L = tL .
 2. D ▽ LL where D ▽ L ∈ iteNF(C,s′ ): by induction hypothesis there is a ground
    computable term tL for D ▽ L such that xθ = tL or x is a variable not in C if
    C[x]θ = D. It follows trivially for D ▽ LL, too and we set tL∨L = tL .

Towards Item 3, let C be an answer clause of the form C[x]JxK and θ a substitution.
Suppose that C does not contain x. Then, iteNF(C, t) is the set {CH} and the
property trivially holds due to x being a variable not in C.
   Otherwise, by construction, any clause in iteNF(C,t) is either of the form D ▽ L̂L
where D ▽ L ∈ iteNF(C,s) or of the form D ▽ LL where D ▽ L ∈ iteNF(C,s′ ). These
clauses are not of the form CH so the property trivially holds for them.

Towards Item 4, any pair of clauses in iteNF(C,s), respectively iteNF(C,s′ ) with
diﬀerent conditions have complementary literals by assumption, and this is still
true after adding L̂, respectively L to these clauses. All other pairs (between the
two clause sets) have the complementary L and L̂ in their conditions.

Case 2. Otherwise.

The set ∆ is simply {ǫ}. Let C[x]JxK be an answer clause and θ a substitution. We
have that iteNF(C[x]JxK,t) = {C[t]H}. By Deﬁnition 13, thus Item 1 is satisﬁed.
For Item 2, either θ = {x 7→ t} and the term in question tǫ has to be t or C[x]θ 6= C[t].
Item 3 is trivially satisﬁed as ǫ ∈ ∆. Item 4 is also trivially satisﬁed, since there are
no two diﬀerent elements in the set ∆.                                                 ❏

Lemma 5. There is a set of lists of computable ground literals ∆ that satisﬁes the
following properties:

 1. Any uncomputable C ∈ Gr(S,t) is of the form C ▽ L where L ∈ ∆∪{ǫ}.
 2. For any L ∈ ∆∪{ǫ}, there is a ground computable simple term tL such that for
    any uncomputable C ′ ▽ L ∈ Gr(S,t), substitution θ, and clause CJpK ∈ S such
    that Cθ = C ′ , it holds that p is a simple term and pθ = tL or p is a variable not
    in C.
         / ∆, then for any uncomputable C ′ H ∈ Gr(S,t), substitution θ, and clause
 3. If ǫ ∈
    CJpK ∈ S such that Cθ = C ′ , it holds that p is a variable not in C.
 4. For any L,K ∈ ∆ such that L =    6 K, L and K contain a complementary literal.
28      Hajdu, Hozzová, Kovács, Wagner

Proof. Let ∆ be the set of ground literals obtained by applying Lemma 12 for the
term t.
Towards Item 1, let C ∈ Gr(S, t). We prove the property by induction on the
derivation length of C.
Case 1. C has a derivation length 0.
By Item 1 of Deﬁnition 15, C is in iteNF(C,t) for some C of the form C[x]JxK and
the claim holds due to Lemma 12.
Case 2. C has non-zero derivation length.
By Item 2 of Deﬁnition 15, there are clauses C1 ▽ K1 ,...,Cn ▽ Kn from which C
is derived, all with smaller derivation length, so we have that Item 1 holds for all
these clauses, i.e. for all 1 ≤ i ≤ n, we have Ki is empty or Ki ∈ ∆. From Item 2 of
Deﬁnition 15, either Ki is empty for all 1 ≤ i ≤ n, and we have that C is of the form
CH, or there is some 1 ≤ i ≤ m such that C is of the form C ▽ L for L = Ki . In both
cases we have L ∈ ∆∪{ǫ}. This proves the claim.
Towards Item 2, let L ∈ ∆∪{ǫ} and tL be the ground computable term obtained
from Item 2 of Lemma 12. We show that this tL satisﬁes the property for L. Let
C be any clause from Gr(S,t) of the form C ′ ▽ L. The proof is again by induction
on the derivation length of C.
Case 1. C has a derivation length 0.
By Item 1 of Deﬁnition 15, C is in iteNF(C,t), and the claim holds for all answer
clauses C[x]JxK ∈ S and substitutions θ due to Lemma 12.
Case 2. C has non-zero derivation length.
By Item 2 of Deﬁnition 15, there is an inference C1 Jp1 K,...,Cn Jpn K ⊢ CJpKσ, clauses
C1′ ▽ K1 , ..., Cn′ ▽ Kn , and a substitution θ such that σθ = θ, Cθ = C, and by
assumption for all 1 ≤ i ≤ n, we have Ki ∈ ∆∪{ǫ}, and by the induction hypothesis,
the property holds for clause Ci′ ▽ Ki , answer clause Ci Jpi K and θ.
   For all SupU , EqRes and EqFac rule applications, there is an idempotent most
general uniﬁer σ such that Ci σθ = Ci′ and pi σ = p for all 1 ≤ i ≤ n.
   Suppose that for all 1 ≤ i ≤ n, we have that pi is a variable not in Ci . Then, it
follows that p is also a variable not in C. Otherwise, there is at least one 1 ≤ i ≤ n
such that pi σθ = tL . Note that for all 1 ≤ j ≤ n, if pj is not a variable not in Cj , also
pj σθ = tL and pj is a simple term. We get that pi σθ = pθ = tL and pj σ is a simple
term too, proving the claim.
Towards Item 3, let C be any clause from Gr(S,t) of the form C ′ H. The proof is
again by induction on the derivation length of C.
Case 1. C has a derivation length 0.
By Item 1 of Deﬁnition 15, C is in iteNF(C,t), and the claim holds for all answer
clauses C[x]JxK ∈ S and substitutions θ due to Lemma 12.
Case 2. C has non-zero derivation length.
                                     Completeness of Synthesis under Realizability      29

By Item 2 of Deﬁnition 15, and by the induction hypothesis, there is an inference
C1 Jx1 K,...,Cn Jxn K ⊢ CJpKσ, clauses C1′ H, ..., Cn′ H, and a substitution θ such that
σθ = θ, Cθ = C, and xi is a variable not in Ci for all 1 ≤ i ≤ n. Again, by inspecting
the uniﬁer applied in all SupU , EqRes and EqFac rule applications, we get that
xi σ = p for all 1 ≤ i ≤ n and therefore p must be also a variable not in C.
Finally, the clause set ∆ satisﬁes Item 4 by Lemma 12.                                  ❏

Lemma 6. If Jp[ᾱ]K ∈    / S for any computable program term p[ᾱ], then the formula
¬F [ᾱ,t] is satisﬁable for any ground computable program term t.

Proof. We show that for any c-clause C ∈ Gr(S,t), it holds that RGr(S,t)  C. Since
S
   C∈S0 iteNF(C,t) is equisatisﬁable with ¬F [σ̄,t[σ̄]], it then follows that ¬F [σ̄,t[σ̄]]
is satisﬁable too.12
    The proof is by induction on ≻ on c-clauses. By contradiction, suppose that
there is a c-clause C ∈ Gr(S,t) such that RGr(S,t) 2 C. Since ≻ is well-founded,
there is a minimal such C. Since all c-clauses in Gr(S, t) \ cGr(S) are uncom-
putable and greater w.r.t. ≻ than any (necessarily computable) c-clause in cGr(S),
by Lemma 3 and Lemma 4 we have that C is satisﬁed if C ∈ cGr(S). Hence, C is
uncomputable. We distinguish the following cases.
Case 1. C is of the form C ′ ▽ L and there is an answer clause CJpK in S and a
substitution θ s.t. Cθ = C ′ , and there is a variable x in C such that xθ is reducible
in RGr(S,t) .
Note that p cannot contain x by Deﬁnition 15. Let θ′ be the substitution θ, except
that it maps x to the normal form of xθ w.r.t. RGr(S,t) . Let D be the c-clause
C ′ θ′ ▽ L. Then, since xθ ≻ xθ′ and C contains x, we have C ≻ D. Also, xθ′ is the
normal form of xθ, so RGr(S,t) 2 D too. Note that D is in Gr(S,t) by Deﬁnition 15.
Thus, we have found a c-clause in Gr(S,t) smaller than C.
Case 2. C is of the form s′ 6≈ t′ ∨C ′ ▽ L such that s′ 6≈ t′ is maximal in C.

Subcase 2.1. s′ = t′ .
There is a clause s 6≈ t∨CJpK in S, a ground substitution θ such that (s 6≈ t∨C)θ =
s′ 6≈ t′ ∨C ′ . Consider the following inference:

                                                s 6≈ t∨CJpK
                                     (EqRes)
                                                 (CJpK)σ
where σ = mgu(s,t). Let D be C ′ ▽ L. By sθ = tθ = s′ , we have that θ is a uniﬁer of
s and t. By Lemma 5, we get that pθ is computable or p is a variable and not in
s 6≈ t∨C, and therefore pσ is also computable. Therefore, condition 2 of the EqRes
rule is satisﬁed and CJpKσ ∈ S and D ∈ Gr(S,t). Due to {{s′ ,s′ ,s′ ,s′ }}⊎C ′ ≻bag C ′ ,
we also have C ≻ D. Also, RGr(S,t) 2 C ′ , so RGr(S,t) 2 D. Thus, we have found a
false clause smaller than C, contradiction.
12
     The initial set S0 is cnf(¬F [ᾱ,y])JyK.
30      Hajdu, Hozzová, Kovács, Wagner

Subcase 2.2. W.l.o.g. s′ ≻ t′ and s′ is reducible by some l′ → r′ ∈ RGr(S,t) where
l′ is not computable.
Then s′ is of the form s′ [l′ ] and there is a rule l′ → r′ in RGr(S,t) produced by some
uncomputable clause l′ ≈ r′ ∨D′ ▽ K in Gr(S,t). Let ∆ be the set from Lemma 5. By
Item 1 of Lemma 5, we have that L,K ∈ ∆∪{ǫ}. If they are in ∆ and diﬀerent, then
by Item 4 of Lemma 5, we have that L and K contain complementary conditions,
that is, there is a literal L such that L ∈ L and L̂ ∈ K. By Item 3 of Deﬁnition 10,
RGr(S,t) 2 L̂, and thus RGr(S,t)  L, so C cannot be false, contradiction.
     Otherwise s[k] 6≈ t∨CJpK and l ≈ r∨DJqK in S such that k is not a variable (see
Case 1), and there is a ground substitution θ such that lθ = kθ = l′, (s[k] 6≈ t∨C)θ =
s′ [l′ ] 6≈ t′ ∨C ′ and (l ≈ r∨D)θ = l′ ≈ r′ ∨D′ . If L,K ∈ ∆, then they must be the same,
and by Item 2 of Lemma 5, we get that there is a term tL (= tK ) such that (i) qθ = tL
or q is a variable not in l ≈ r∨D and (ii) pθ = tL or p is a variable not in s[k] 6≈ t∨C.
Otherwise L or K is empty, and then by Item 3 of Lemma 5, we get that p (resp.
q) is a variable that is not in s[k] 6≈ t∨C (resp. l ≈ r ∨D). In all of these cases, we
get that the uniﬁer σ = mgu((l,p),(k,q)) exists. Consider the following inference:

                                  l ≈ r∨DJqK         s[k] 6≈ t∨CJpK
                        (SupU )
                                        s[r] 6≈ t∨C ∨DJpKσ
Since l′ ≈ r′ ∨ D′ is productive, Item 5 from Deﬁnition 10 and the assumption
s′ ≻ t′ imply that rσ  lσ and tσ  s[k]σ (condition 3 of the SupU rule). By the
above reasoning, we also have that pθ is either tL , tK or a variable, therefore pσ
is computable and condition 4 of the SupU rule is satisﬁed. Then we have that
s[r] 6≈ t∨C ∨DJpKσ ∈ S. Let D be the c-clause s′ [r′ ] 6≈ t′ ∨C ′ ∨D′ ▽ L′ where L′ is L
if K is empty, otherwise K. By Item 2 of Deﬁnition 15, we have D ∈ Gr(S,t). Sim-
ilarly to Subcase 3.2 of Lemma 4, we get that C ≻ D and s′ [r′ ] 6≈ t′ ∨C ′ ∨D′ is false.
Note that L′ is either empty or false because L is false (by Item 3 of Deﬁnition 10).
Thus, D is a false clause in Gr(S,t) smaller than C, contradiction.
Subcase 2.3. W.l.o.g. s′ ≻ t′ and s′ is reducible by some l′ → r′ ∈ RGr(S,t) where
l′ is computable.
Then s′ is of the form s′ [l′ ] and there is a rule l′ → r′ in RGr(S,t) produced by some
computable clause l′ ≈ r′ ∨C ′ H. Suppose that s′ is computable. Then, since s′ ≻ t′ ,
t′ must also be computable. But then, since C is uncomputable, there must be an
uncomputable literal in C ′ and this literal is strictly greater than s′ 6≈ t′ w.r.t. ≻,
which contradicts the assumption that s′ 6≈ t′ is maximal. Therefore, s′ must be
uncomputable. This also means that l′ is a strict subterm of s′ , otherwise s′ would
be computable.
   There is s[l] 6≈ t∨CJpK in S such that l is not a variable, a ground substitution θ
such that lθ = l′ and (s[l] 6≈ t∨C)θ = s′ [l′ ] 6≈ t′ ∨C ′ . Consider the following inference
where the variable x is fresh and k is some superterm of l (possibly l itself):

                                          s[k] 6≈ t∨CJpK
                              (Abs)
                                      s[x] 6≈ t∨x 6≈ k∨CJpK
                                     Completeness of Synthesis under Realizability     31

We have s′ ≻ t′ , so s  t satisfying condition 1 of the Abs rule. Condition 2 of the
Abs rule is satisﬁed for l and θ. W.l.o.g. we can assume that k is chosen such that
condition 2 is still satisﬁed, and such that no superterm of k satisﬁes condition 2,
satisfying condition 3 of the rule. But this means that the Abs rule was not applied
to this clause, and thus S is not abstracted, contradiction.
Subcase 2.4. W.l.o.g. s′ ≻ t′ and s′ is irreducible.
Then, since s′ ≻ t′ and s′ is in normal form, RGr(S,t)  s′ 6≈ t′ and C is satisﬁed,
contradiction.
Case 3. C is of the form s′ ≈ t′ ∨C ′ ▽ L where s′ ≈ t′ is maximal in s′ ≈ t′ ∨C ′ .
W.l.o.g. s′ ≻ t′ .
Subcase 3.1. s′ is reducible by some l′ → r′ ∈ RGr(S,t) where l′ is uncomputable.
This is similar to Subcase 2.2. Then s′ is of the form s′ [l′ ] and l′ → r′ is produced
by some c-clause l′ ≈ r′ ∨D′ ▽ K. There are clauses s[k] ≈ t∨CJpK and l ≈ r∨DJqK
in S, such that k is not a variable, a ground substitution θ such that lθ = kθ = l′ ,
(s[k] ≈ t ∨ C)θ = s′ [l′ ] ≈ t′ ∨ C ′ and (l ≈ r ∨ D)θ = l′ ≈ r′ ∨ D. Similarly to Subcase
2.2, we assert that either RGr(S,t)  C reaching a contradiction, or that the uniﬁer
σ = mgu((l,p),(k,q)) exists. Consider the following inference:

                                     l ≈ r∨DJqK       s[k] ≈ t∨CJpK
                       (SupU )
                                            s[r]∨C ∨DJpKσ
Let D be the c-clause s [r ] ≈ t ∨C ∨D′ ▽ L′ where L′ is L if K is empty, otherwise
                         ′   ′   ′      ′

K. We check the conditions the SupU rule similarly as in Subcase 2.2. Therefore,
s[r]∨C ∨DJpKσ ∈ S and D ∈ Gr(S,t). We also have the following

                      {{s′ [l′ ],t′ }}⊎C ′ ≻bag {{s′ [r′ ],t′ }}⊎C ′ ⊎D′

and hence C ≻ D. Also, RGr(S,t) 2 D: (1) by assumption, C ′ and D′ are false in
RGr(S,t) , and (2) s′ [l′ ] have distinct normal forms with t′ , so s′ [r′ ] and t′ must
have distinct normal forms too (otherwise C would be true in RGr(S,t) by conﬂu-
ence), and (3) L′ is either empty or false because L is empty or false by Item 3 of
Deﬁnition 10. Thus, we have found a false clause in S smaller than C.
Subcase 3.2. W.l.o.g. s′ ≻ t′ and s′ is reducible by some l′ → r′ ∈ RGr(S,t) where
l′ is computable.
Analogous to Subcase 2.3.
Subcase 3.3. s′ is irreducible in RGr(S,t) .
Then, C ′ is of the form s′ ≈ r′ ∨ D′ such that t′  r′ and s′ ≈ r′ is true in
  ≺C
RcGr(S)  ∪ {s′ → t′ } (i.e. Item 6 of Deﬁnition 10 is violated). Note that this also
covers the case when Item 4 of Deﬁnition 10 is violated, as then t′ = r′ and C is of
the form s′ ≈ t′ ∨s′ ≈ t′ ∨D′ ▽ L.
   Then there is an answer clause s ≈ t∨l ≈ r∨DJpK in S, a ground substitution θ
such that (s ≈ t∨l ≈ r∨D)θ = s′ ≈ t′ ∨s′ ≈ r′ ∨D′ . Consider the following inference:
32      Hajdu, Hozzová, Kovács, Wagner

                                       s ≈ t∨l ≈ r∨DJpK
                            (EqFac)
                                      s ≈ t∨t 6≈ r∨DJpKσ
where σ = mgu(s,l). Let D be the c-clause s′ ≈ t′ ∨ t′ 6≈ r′ ∨ D′ . Since s′ ≻ t′ and
t′  r′ by assumption, condition 2 of the EqFac rule holds. By Lemma 5, we get
that pθ is computable or p is a variable and not in s 6≈ t ∨ C, and therefore pσ is
also computable, satisfying condition 3 of EqFac. Then, s ≈ t ∨ t 6≈ r ∨ DJpKσ ∈ S
and D ∈ Gr(S,t). Similarly to Subcase 4.2 of Lemma 4, we get that C ≻ D and
RGr(S,t) 2 (s′ ≈ t′ ∨t′ 6≈ r′ ∨D′ ). We also have that RGr(S,t) 2 L, hence RGr(S,t) 2 D.
Thus, we have found a false clause in Gr(S,t) smaller than C.                         ❏
