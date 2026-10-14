                                                         Towards SMT Solver Stability via Input
                                                                   Normalization
                                                                Daneshvar Amrollahi∗ , Mathias Preiner∗ , Aina Niemetz∗ , Andrew Reynolds† ,
                                                                           Moses Charikar∗ , Cesare Tinelli† , Clark Barrett∗
                                                                                                ∗ Stanford University, USA

                                                             {daneshvar, preiner, niemetz, moses, barrett}@cs.stanford.edu
                                                                                 † The University of Iowa, USA

                                                                      {andrew-reynolds, cesare-tinelli}@uiowa.edu
arXiv:2410.22419v2 [cs.LO] 15 May 2025




                                            Abstract—In many applications, SMT solvers are utilized to           both are important, this paper focuses on the first: changes
                                         solve similar or identical tasks over time. Significant variations in   to the input. In other words, we are interested in reducing
                                         performance due to small changes in the input are not uncommon          the sensitivity of solving time to minor changes in an input
                                         and lead to frustration for users. This sort of stability problem
                                         represents an important usability challenge for SMT solvers.            formula, especially if those changes are semantics-preserving.
                                         We introduce an approach for mitigating the stability problem              Two common misconceptions about stability are worth not-
                                         based on normalizing solver inputs. We show that a perfect              ing. First, instability should not be confused with poor solver
                                         normalizing algorithm exists but is computationally expensive.          performance. Improving solver performance is an important
                                         We then describe an approximate algorithm and evaluate it on            and worthy goal; however, it is orthogonal to addressing the
                                         a set of benchmarks from related work, as well as a large set
                                         of benchmarks sampled from SMT-LIB. Our evaluation shows                stability problem. Our focus is on making solver performance
                                         that our approximate normalizer reduces runtime variability             more consistent in the face of mutations to its input. Im-
                                         with minimal overhead and is able to normalize a large class            portantly, many users in our study reported that they would
                                         of mutated benchmarks to a unique normal form.                          welcome any improvement to stability, even if it came at the
                                                                                                                 cost of a degredation in performance. The other misconception
                                                                I. I NTRODUCTION
                                                                                                                 is the failure to recognize that the stability problem is linked to
                                            SMT solvers are used to solve a large variety of problems            computational complexity. Because the SMT problem is NP-
                                         in academia and industry [4], [14], [21]. As these solvers are          hard (or worse, depending on the theory being used), solvers
                                         integrated into more and more workflows, they are increasingly          try to guide worst-case exponential algorithms in such a way
                                         used in situations where there are many calls to a solver               that solutions are found quickly when possible. However, even
                                         with identical or similar queries. For example, a software              a small change in the input can trigger a different search
                                         verification tool may run a regression suite nightly to check           path, which could result in an exponentially worse (or better)
                                         that some software meets its specification, and for the most            runtime. This is similar to the well-known “butterfly effect”
                                         part, this nightly run does not differ much, if at all, from the        in chaos theory. Despite this, as we show in this paper, there
                                         previous night’s run. A common pain point in such situations            are steps that can be taken to reduce instability.
                                         is that SMT solver performance can vary significantly, even                SMT solvers typically already use deterministic data struc-
                                         if there are only minor changes. This has been termed the               tures and algorithms to eliminate easily avoidable sources of
                                         stability problem: queries that are semantically similar or             instability. In a sequential execution setting, the remaining
                                         identical may require vastly different amounts of time to solve.        source of variability is their heuristics, primarily their branch-
                                         Or, even worse, some minor changes may result in a formerly             ing heuristics, which typically break ties based on the order in
                                         solved query not being solved at all.                                   which declarations and assertions appear in the input formula.
                                            As part of an NSF-supported project [3], we spoke with a             Our key idea is to reduce this variability by using the structure
                                         large number of SMT stakeholders and cataloged and ranked               of the input problem to determine the order of declarations and
                                         over 100 different issues, based on how often they came                 assertions. Our approach uses the principle of normalization:
                                         up in interviews. In this ranking, instability was ranked as            we attempt to map classes of semantically equivalent inputs to
                                         the second-highest area of concern (behind only requests for            the same normal form. Note that if perfect normalization could
                                         better diagnostic output when the solver is unable to solve             be achieved in this setting, it would result in perfect stability,
                                         a problem). The instability concern was also highlighted in             with respect to the semantically equivalent input classes, as
                                         a keynote talk by Neha Rungta at CAV 2022 [21] on the                   the input to the core solver would be the same in every case.
                                         use of SMT solvers at Amazon Web Services and has been                  We present an approach aimed at getting closer to that ideal
                                         identified by another senior manager at Amazon as one of two            without introducing too much overhead. A notable feature of
                                         top priorities for improving their SMT solving workflows [13].          our approach is that it is agnostic to the underlying solver. It
                                            There are two kinds of changes that can introduce insta-             can thus be used to improve the stability of any SMT solver
                                         bility: changes to the input and changes to the solver. While           with respect to changes in the input.
   We consider normalization with respect to a set of basic,        via the use of different random seeds, and use a statistical ap-
semantics-preserving transformations: (i) reordering of asser-      proach to identify instability arising from these mutations. We
tions; (ii) reordering of operands of commutative operators;        include an evaluation of our technique on their benchmarks,
(iii) reordering and renaming of user-defined symbol decla-         with the notable difference that we do not include solver-
rations; and (iv) replacing anti-symmetric operators by their       modifying mutations. This is because we aim to improve
converse. These transformations are representative of the kinds     stability with respect to input changes, rather than across
of changes that happen in the real-world scenarios motivating       changes to a solver. In [25], Zhou et al. identify irrelevant
our work. For example, in a program verification workflow,          context in a query as one source of instability and propose
if a function is moved or renamed, this could result in a           a novel approach to filter out such context to improve solver
reordering of declarations and assertions, a different name for a   stability. This approach is complementary to our own, and
user-defined symbol, or both. These transformations are also        combining the two is an interesting direction for future work.
a superset of the solver input transformations considered in           Also closely related is the work of Weber [24], which
previous work on measuring instability [26]. We will refer          introduces a normalizer designed to reverse the effects of
to these transformations as mutations and to inputs that have       mutations used to scramble benchmarks for the SMT-COMP
been transformed this way as mutated inputs. We address the         competition at the time. However, the normalizer introduced
following research questions:                                       in [24] was specifically designed to expose a weakness in
  1) Is it possible to design a normalizing algorithm that          the scrambling algorithm, namely that symbols were renamed
     utilizes these mutations to map all mutated variants to a      but not reordered. This weakness makes it possible to achieve
     single unique normal form?                                     perfect normalization efficiently, which their algorithm does.
  2) If such an algorithm exists, what is its time complexity?      However, in the presence of the more expressive and realistic
  3) How closely can an efficient algorithm approximate the         mutations we consider, their normalizer performs poorly, as
     ideal algorithm?                                               we show in Section V.

   After covering some background in Section II, we formalize                              II. BACKGROUND
the problem in Section III and answer the first two questions,         We work in the context of many-sorted logic (e.g., [9]),
showing that such an algorithm does indeed exist but is as          where we assume an infinite set of variables of each sort and
hard as graph isomorphism. We provide an answer to the              the usual notions of signatures, terms, formulas, assignments,
third question in the remainder of the paper. Section IV            and interpretations. We assume a signature Σ consisting of
introduces an algorithm that approximates the ideal algorithm,      sort symbols and sorted function symbols. It is convenient to
and Section V presents an evaluation of our implementation,         assume that Σ has a distinguished sort Bool, for the Booleans,
showing that it significantly improves SMT solver stability         and to represent relation symbols as function symbols whose
on benchmarks from [26] and from the SMT-LIB benchmark              return sort is Bool. We also assume the signature includes
library [20]. Finally, Section VI concludes.                        equality. Symbols in Σ are partitioned into theory symbols
Related work. The importance of the issue of stability in           (e.g., =, ∧, ∨, +, −, 0, 1) and user-defined symbols (e.g., f ,
SMT solving has been raised in other work [8], [10], [12],          g, x, y). We assume some background theory restricts the
[17]. Dodds [8], highlights the problem of proof fragility          theory symbols to have fixed interpretations, whereas the
under changes in verification tools. Ferraiuolo et al. [10]         interpretation of user-defined symbols is left unrestricted.
mention proof instability as the most frustrating recurring            We represent formulas as finite sequences of symbols in
problem, especially when proof complexity increases as a            prefix notation, where each symbol is either a theory symbol
result of reasoning about procedures with many instructions         or a user-defined symbol. This causes no ambiguity when each
and complex specifications. In Hawblitzel et al. [12], verifi-      symbol has a fixed arity. If S is a sequence ⟨s1 , . . . , sn ⟩, we
cation instability is observed in large formulas and non-linear     write |S| to denote n, the length of the sequence, and Si to
arithmetic due to different options for applicable heuristics.      denote the ith element of the sequence. We write s ∈ S to
Leino et al. [17] identify matching loops—caused by certain         mean that s occurs in the sequence S, and write S ◦ S ′ for
forms of quantifiers that lead an SMT solver to repeatedly          the sequence obtained by appending S ′ at the end of S. We
instantiate a limited set of quantified formulas—as a key factor    write user (S) to mean the sequence obtained by deleting all
contributing to instability in verification times, and describe     theory symbols in S, e.g., user (⟨x, +, y, −, x⟩) = ⟨x, y, x⟩.
techniques to detect and prevent them.                              We denote the set of integers between m and n inclusive,
   More relevant to our work is the work of Zhou et al. [26],       where n ≥ m, as [m, n]. And we abbreviate [1, n] as [n].
[25]. In [26], they pioneer an effort to detect and quantify           A formula in the SMT-LIB 2.6 format [2] is shown in
instability and introduce a tool for this task called Mariposa.     Figure 1. We use this as a running example throughout the
They show that mainstream SMT solvers such as Z3 [7] and            paper. The example includes arithmetic theory symbols, a user-
cvc5 [1] exhibit instability on a set of F∗ [22] and Dafny [16]     defined function f , and user-defined constants v, w, x, y,
benchmarks [5], [10], [11], [18], [19], [23]. They consider         and z. We will refer to the sequence of six assertions in the
the benchmark-modifying mutations of symbol renaming and            running example as ⟨β1 , . . . β6 ⟩. Figure 2 shows two different
assertion reordering, as well as solver-modifying mutations         representations of the first two assertions in the example: the
  (set-logic QF_UFLIA)                                                  β2 has two commutative operators, + and ∗. Consequently,
                                                                        C(⟨β1 , β2 ⟩) has eight elements, representing all combinations
  (declare-fun f (Int) Int)      (declare-const v Int)
  (declare-const w Int)          (declare-const x Int)                  of one formula each from C(β1 ) and C(β2 ).
  (declare-const y Int)          (declare-const z Int)
                                                                        Definition III.3 (Pattern). Let α be a formula. The pattern
  (assert (>= (+ (f x) y) (- v 12)))
  (assert (< (+ x y) (* x z)))
                                                                        of α, written P (α), is a sequence of the same length as α,
  (assert (>= (+ (f y) x) (- w 12)))                                    defined for each i ∈ [|α|] by
  (assert (< (+ y x) (* x x)))                                                      
  (assert (< (+ x y) (* y y)))                                                        αi       if αi is a theory symbol,
  (assert (< (+ y x) (* y v)))                                                      
                                                                                    
                                                                                    
                                                                                       @1       if αi is the first user-defined symbol
                                                                                    
                                                                                    
  (check-sat)                                                                       
                                                                                    
                                                                                    
                                                                                                appearing in α,
                                                                                    
                                                                                    
                                                                                    
                   Fig. 1: Running Example.                               P (α)i = P (α)j if αi is a user-defined symbol and
                                                                                    
                                                                                    
                                                                                                there exists j ∈ [i − 1] with αj = αi ,
                                                                                    
                                                                                    
  (assert (>= (+ (f x) y) (- v 12)))                                                
                                                                                    
  (assert (< (+ x y) (* x z)))
                                                                                    
                                                                                    
                                                                                    
                                                                                      @k       otherwise, where k = 1 +
                                                                                    
                                                                                                 {αj | j ∈ [i − 1], αj user-defined} .
                                                                                    
  (assert (> (* u4 u2) (+ u2 u3)))
  (assert (>= (+ (g u2) u3) (- u1 12)))                                 For convenience, we assume that each symbol @k is a fresh
                                                                        constant1 of the same sort as the symbol it is replacing, so
Fig. 2: Two different mutated versions of the same assertions.          that if α is well-sorted, then so is P (α). We call introduced
first is from the example and the second is a mutation of it.           symbols starting with “@” pattern symbols and sequences in
In particular, the order of the assertions has been swapped,            the co-domain of P patterns. We define a total order ≺ on
the operands of the * operator have been reordered, the user-           patterns to be the lexicographic order induced by some total
defined symbols have been renamed (with w, x, y, and z                  order on formula symbols.2 For our example assertions, we
renamed to u1 through u4, respectively, and f renamed to                have P (β1 ) = ⟨>=, +, @1, @2, @3, −, @4, 12⟩ and P (β2 ) =
g), and the assertion using < has been rewriiten to use >.              ⟨<, +, @1, @2, ∗, @1, @3⟩.
                                                                           We lift this notation to sequences and sets of sequences. To
                     III. F ORMALIZATION                                explain how, we need two more definitions.
   Consider again the first two assertions from the example.            Definition III.4. Given a sequence of formulas A =
Here, the user-defined symbols are {f , x, y, v, z}, and the            ⟨α1 , . . . , αn ⟩, the conjoining of A, Conj (A) is the formula
theory symbols are {>=, <, +, −, ∗, 12}. When written as                ⟨∧⟩◦α1 ◦α2 ◦· · ·◦αn . Similarly, given a formula ⟨∧⟩◦α1 ◦α2 ◦
a sequence in prefix notation, β1 is ⟨>=, +, f, x, y, −, v, 12⟩.        · · ·◦αn , where αi is a formula for i ∈ [n], the unconjoining of
Similarly, β2 is ⟨<, +, x, y, ∗, x, z⟩.                                 α, written Unconj (α) is the formula sequence ⟨α1 , . . . , αn ⟩.
   Recall that mutations include four operations: (i) reordering
assertions; (ii) reordering operands of commutative operators;          For a sequence A of formulas, we define P (A) =
(iii) reordering and renaming symbols; and (iv) replacing anti-         Unconj (P (Conj (A))). If X is a set (containing either formu-
symmetric operators. We defer (iv) to the end of this section,          las or sequences of formulas), then P (X) = {P (x) | x ∈ X}.
as it can easily be handled separately. To formalize the others,        We similarly lift ≺ to sequences of formulas: if A and A′
we introduce some definitions.                                          are sequences of patterns, then A ≺ A′ iff α1 ◦ · · · ◦ α|A| ≺
                                                                        α1′ ◦ · · · ◦ α|A
                                                                                       ′
                                                                                         ′ | . We next define renaming and normalization.
Definition III.1 (Shuffle Set). The shuffle set of a sequence
A is defined as S(A) = {A′ | A′ is a permutation of A}.                 Definition III.5 (Renaming). Let V be a set of variables. A
                                                                        renaming R is an injective function from pattern symbols to
For example, S(⟨β1 , β2 ⟩) = {⟨β1 , β2 ⟩, ⟨β2 , β1 ⟩}.                  V . For a formula α, R(α) is defined to be a sequence of the
Definition III.2 (Commutative Reordering Set). Let α be a               same size as α, defined as follows:
formula, possibly containing (binary) commutative operators.
                                                                                         (
                                                                                           αi       if αi is a theory symbol,
The commutative reordering set of α is defined as C(α) =                        R(α)i =
{α′ | α′ is the result of swapping the operands of zero or more                            R(αi ) if αi is a pattern symbol.
of these commutative operators in α}. For a sequence A of n             For a sequence of formulas A = ⟨α1 , . . . , αn ⟩, R(A) =
formulas, C(A) is the set of all sequences ⟨α1′ , . . . , αn′ ⟩ where   ⟨R(α1 ), . . . , R(αn )⟩. If X is a set (containing either formulas
for each i ∈ [n], αi′ ∈ C(αi ). If X is a set (containing either        or sequences of formulas), then R(X) = {R(x) | x ∈ X}.3
formulas or sequences of formulas), then C(X) = {x′ | x′ ∈
                                                                          1 The SMT-LIB 2.6 standard reserves symbols starting with @ for internal
C(x) for some x ∈ X}.
                                                                        use by solvers, so this assumption is a reasonable one.
                                                                          2 An obvious choice for this order (and the one we use) is the lexicographic
For example, C(β1 ) = {β1 , ⟨>=, +, y, f, x, −, v, 12⟩}. Note
that there is only one entry in C(β1 ) besides β1 itself,               order on the string representations of theory and pattern symbols.
                                                                          3 When representing an assertion sequence as an SMT-LIB 2.6 script, we
because + is the only commutative operator appearing in β1 .            declare user-defined symbols in lexicographic order, so a renaming can affect
On the other hand, there are four elements in C(β2 ), since             the order of declarations.
Definition III.6 (Normalizing Function). A function N from                    (assert (>= (+ (f x) y) (- v 12)))
sequences of formulas to sequences of formulas is said to be                  (assert (< (+ x y) (* x z)))

normalizing if, for every sequence A of formulas:
                                                                              (assert (>= (+ (f x) y) (- v 12)))
  1) N (A) = R(A′ ) for some A′ ∈ P (C(S(A))) and some                        (assert (> (* x z) (+ x y)))
      renaming R; and
  2) if M1 = R1 (M1′ ) and M2 = R2 (M2′ ), with R1 , R2                        Fig. 3: Original (top) and normalized (bottom) assertions.
      renamings and with M1′ , M2′ ∈ P (C(S(A))), then                           IV. A PPROXIMATING A N ORMALIZATION A LGORITHM
      N (M1 ) = N (M2 ).
                                                                                 As a first step towards a general practical algorithm for
We can now introduce our first research question: does there                  normalization, we describe a heuristic procedure designed to
exist a normalizing function? We show that the question can                   handle two of the four mutations: shuffling and renaming. We
be answered affirmatively.                                                    leave the handling of the other operations to future work.
                                                                              We expect support for normalizing antisymmetric operator
Definition III.7 (Normalizing Function). Let N be defined as
                                                                              replacement to be straightforward (as described above), while
follows. Given a sequence of formulas A, let N (A) be the
                                                                              normalizing commutative operand swapping will be more
≺-minimal element of P (C(S(A))).
                                                                              challenging. Note that shuffling and renaming are also the two
Theorem III.8. Function N is normalizing.                                     operations used to mutate benchmarks in the Mariposa work
                                                                              (the closest related work) [26]. We describe our algorithm
Due to lack of space, proofs for this and other theorems in                   at a conceptual level here, and discuss several optimizations
this paper are omitted.4                                                      necessary to make it work well in practice in Section V-C. Our
                                                                              algorithm consists of three steps: (i) Sorting the assertions; (ii)
A. Complexity
                                                                              Renaming all symbols; and (iii) Sorting the assertions again.
   We have shown the existence of a normalizing function. The                 In the rest of this section, we discuss these steps in detail.
next question is whether normalization can be done efficiently.               Sorting the assertions. Step one is to sort the assertions. The
An informal argument that computing the normalization of                      challenge is to do this in a way that does not depend on
an arbitrary set of formulas is at least as hard as graph                     the names of user-defined symbols. The key idea is to use
isomorphism can be found in [15], and a formal proof can be                   patterns. In particular, to order assertions α and α′ , we can
found in [24]. The question of whether graph isomorphism can                  compare P (α) and P (α′ ) using the ≺ order. For instance,
be solved in polynomial time is a long-standing open problem.                 considering agian assertions from our running example, β5
                                                                              is ⟨<, +, x, y, ∗, y, y⟩, and β6 is ⟨<, +, y, x, ∗, y, v⟩, so we
Theorem III.9. Let N be a normalizing function. Then,
                                                                              have P (β5 ) = ⟨<, +, @1, @2, ∗, @2, @2⟩ and P (β6 ) = ⟨<
computing N (A) for an arbitrary A is as hard as solving
                                                                              , +, @1, @2, ∗, @1, 3⟩. The first difference in the patterns is
graph isomorphism.
                                                                              in the sixth position. Assuming @1 is ordered before @2, we
The use of C is not essential for the proof to succeed. Nor-                  have that P (β6 ) ≺ P (β5 ), so we can conclude that β6 should
malizing just the result of shuffling and renaming is already                 be placed before β5 .
as hard as graph isomorphism.                                                    Note, however, that it is possible for two formulas to have
                                                                              the same pattern. Thus, after sorting according to patterns, we
B. Anti-symmetric Operators                                                   obtain an ordered list of equivalence classes EC 1 , · · · , EC n
  As mentioned above, mutations can randomly replace anti-                    with the following features:
symmetric operators with their dual operator. For example, (<                    1) α and α′ belong to the same equivalence class iff
(+ x y) (* x z)) could be changed to (> (* x z)                                      P (α) = P (α′ ).
(+ x y) ). In general, we allow mutations that transform                         2) α ∈ EC i and α′ ∈ EC j where i < j iff P (α) < P (α′ ).
expressions of the form A op B into B op′ A, where (op, op′ )                    The next question is whether we can easily order the
pairs include: (>, <), (>=, <=), (bvugt, bvult), (bvuge,                      assertions belonging to the same equivalence class. We give an
bvule), . . . .                                                               efficient approximation method. For this, we need the notions
  A normalization algorithm can easily handle anti-symmetric                  of role and super-pattern.
operators, simply by choosing one representative operator for                 Definition IV.1 (Role). The role of a symbol s in a formula α,
each pair and forcing all assertions to use only the chosen                   denoted role(s, α), is 0 if s ̸∈ α and the index of the earliest
operators. For example, if the first operator in each pair listed             occurrence of s in user (α), otherwise. The role of s in a set
above is the chosen one, then Figure 3 shows the result of                    of formulas is the multiset consisting of all the roles played
normalizing the first two assertions in our running example.                  by s in the formulas in the set.
Notice that the second assertion is modified by replacing <
with > and swapping the operands but the first assertion is                   For example, consider the role of y in β5 . First of all, we
unchanged because it is already using the chosen operator.                    compute user (β5 ), which is ⟨x, y, y, y⟩. We can then see that
                                                                              y occurs first at the second position, so role(y, β5 ) = 2.
  4 For the reviewers’ convenience, the proofs are provided in an appendix.   Similarly, role(x, {β4 , β5 , β6 }) = {1, 1, 2}.
  (assert (< (+ x y) (* x z)))                                       (assert (< (+ X1     X 2 ) (* X 1   X3 )))
  (assert (< (+ y x) (* y v)))                                       (assert (< (+ X2     X 1 ) (* X 2   X4 )))

  (assert (< (+ y x) (* x x)))                                       (assert (< (+ X2     X 1 ) (* X 1   X1 )))
  (assert (< (+ x y) (* y y)))                                       (assert (< (+ X1     X 2 ) (* X 2   X2 )))

  (assert (>= (+ (f x) y) (- v 12)))                                 (assert (>= (+ (X5     X1 ) X2 ) (- X4       12)))
  (assert (>= (+ (f y) x) (- w 12)))                                 (assert (>= (+ (X5     X2 ) X1 ) (- X6       12)))


             Fig. 4: Assertions sorted by pattern.                         Fig. 5: Assertions after sorting and renaming.
Definition IV.2 (Super-pattern). The super-pattern of a symbol     Similarly, by computing super-patterns for z and v, we can
s over a sequence X of sets X1 , . . . , Xn , denoted SP (s, X),   see that we should keep the order of the assertions in the first
is the sequence of roles of the symbol in each set: SP (s, X) =    equivalence class.
⟨role(s, X1 ), role(s, X2 ), . . . , role(s, Xn )⟩.                   It is possible for all of the super-patterns of corresponding
Let EC be a sequence of formula equivalence classes. The           symbols in two assertions in the same equivalence class to be
super-pattern of EC captures the role of a symbol across           the same. In this case, our heuristic algorithm fails, and the
all equivalence classes, while treating the formulas in each       assertion order is left unchanged. For example, for EC 2 , the
equivalence class as unordered.                                    only user-defined symbols available for comparison are x and
   To illustrate, recall the example from Figure 1. Figure 4       y, and they have the same super-pattern. Thus, we leave these
shows the result of sorting the assertions by pattern, re-         assertions in their original order for now. Algorithm 1 shows
sulting in three equivalence classes, each separated by an         the full algorithm for ordering two assertions.
empty line. The patterns of the equivalence classes in EC =
{EC 1 , . . . , EC 3 }, from top to bottom, are as follows:        Algorithm 1 Algorithm for ordering assertions A and B given
                                                                   EC , a sequence of equivalence classes (with respect to pattern
      EC 1 : ⟨<, +, @1, @2, ∗, @1, @3⟩
                                                                   equality) of assertions.
      EC 2 : ⟨<, +, @1, @2, ∗, @2, @2⟩
      EC 3 : ⟨>=, +, @1, @2, @3, −, @4, 12⟩                          if P (A) ̸= P (B) then
Now, suppose we want to order the formulas in EC 3 . We                 return P (A) ≺ P (B)
compare the super-patterns of the first different pair of user-      end if
defined symbols, in this case, x and y. The roles of x               for i ← 1 to |user (A)| do
throughout the equivalence classes are:                                 u ← user (A)i
                                                                        v ← user (B)i
      role(x, EC 1 ) = {role(x, β2 ), role(x, β6 )} = {1, 2}
                                                                        if u = v then
      role(x, EC 2 ) = {role(x, β4 ), role(x, β5 )} = {1, 2}
                                                                           continue
      role(x, EC 3 ) = {role(x, β1 ), role(x, β3 )} = {2, 3}
                                                                        end if
Therefore, applying the definition of super-pattern for x yields        if SP (u, EC ) = SP (v, EC ) then
SP (x, EC ) = ⟨{1, 2}, {1, 2}, {2, 3}⟩. It is not hard to see              return SP (u, EC ) < SP (v, EC )
that the super-pattern for y is the same, so the two assertions         end if
cannot be distinguished by looking at x and y. The next              end for
pair of different user-defined variables also consists of x and      return inconclusive
y. However, the last pair is v and w. Following the same
process, we find that SP (v, EC ) = ⟨{0, 4}, {0, 0}, {0, 4}⟩ and
                                                                   Renaming all symbols. After sorting the assertions according
SP (w, EC ) = ⟨{0, 0}, {0, 0}, {0, 4}⟩. Now, all we need is a
                                                                   to Algorithm 1, we rename all the symbols in the assertions.
way to order different super-patterns.
                                                                   We use a renaming R that maps a variable whose pattern
Definition IV.3 (Integer multiset order). Given multi-sets         symbol is @k to Xk . More precisely, if A is the sequence of
of integers m1 and m2 , m1 < m2 iff the sequence of                assertions after sorting, we replace A with R(P (A)). Figure 5
nondecreasing elements of m1 is lexicographically less than        shows the assertions from our running example after sorting
the sequence of nondecreasing elements of m2 .                     and renaming.
                                                                   Sorting the assertions again. After renaming, there is one
Definition IV.4 (Super-pattern order). For super-patterns s1
                                                                   more step that can improve the normalizer. It is based on the
and s2 , s1 < s2 iff s1 comes before s2 when compared using
                                                                   observation that within an equivalence class, different assertion
the lexicographic order induced by the integer multiset order.
                                                                   orders are possible, depending on the initial order, when all
Thus, when comparing super-patterns, we compare the entries        symbols in a pair of assertions have the same super-patterns.
in the sequences one by one using the integer multiset order.      This can be partially addressed by lexicographically sorting
The first two entries in SP (v, EC ) and SP (w, EC ) are {0, 4}    each equivalence class after renaming. This ensures that if we
for v and {0, 0} for w. Because ⟨0, 0⟩ < ⟨0, 4⟩, we can            have two benchmarks for which the first two steps produce
conclude that SP (w, EC ) < SP (v, EC ). Thus, we should           the same set of assertions, but in different orders, then these
switch the order of assertions in the last equivalence class.      two benchmarks will be normalized the same way.
   Looking again at Figure 5, we see that assertions in the                     timed out during the normalization phase (of these, 58 timed
first and last equivalence classes are already in sorted order.                 out during parsing, before ever getting to the normalization
However, the assertions in equivalence class 2 should be                        algorithm), for any of the 10 mutated versions. In mariposa,
reordered. Recall that in the previous step, we did not have a                  we only exclude 2 benchmarks, both of which timed out
way to order these assertions, but now there is an unambiguous                  during normalization. Overall, this resulted in 41,075 eligible
order for them. It is important to note that our algorithm                      benchmarks in smtlib and 16,620 in mariposa.
does not guarantee the normalization property. The reason
for this incompleteness is that when assertions cannot be                       A. Normalization Effectiveness
distinguished by super-patterns, there can be different normal                     In our first experiment, we evaluate how closely our im-
forms for benchmarks, even if one is a mutation of the other                    plementation of an efficient normalization algorithm approx-
(via shuffling and renaming). However, our algorithm works                      imates the ideal algorithm on both benchmark sets. For this,
well in practice, as we show next.                                              we measure, for each benchmark: (i) the number of distinct
                                                                                outputs produced by our normalizer for the 10 mutations (the
                          V. E XPERIMENTS                                       best possible is 1; the worst possible is 10); and (ii) the
   We implemented our normalization algorithm in C++. We                        similarity of the 10 normalized outputs, computed as the av-
evaluate its effectiveness on three dimensions: normalization                   erage percentage of identical lines among all pairs of outputs.
effectiveness, stability, and runtime.                                          Table I shows our results. Each row starts with a category
   We use two sets of benchmarks. The first set, smtlib, is                     name (the name of the division or family) and a pair of
obtained by randomly selecting 50 benchmarks from each                          numbers (x/y) denoting the number of excluded benchmarks
family (or all of them, if there are fewer than 50) in the SMT-                 x vs. the total number of benchmarks y in that category. We
LIB benchmark library [20]. A family, in this context, consists                 then list the number of considered benchmarks (#Bench, equal
of all benchmarks in a single leaf directory of the filesystem                  to y − x) and the average number of distinct benchmarks
heirarchy. Note that even though our normalization algorithm                    produced by the 10 mutations, before normalization (pre) and
as described in Section IV is, in theory, applicable to all of                  after normalization, without (wo-SP) and with (w-SP) the use
SMT-LIB without limitation, our current implementation does                     of super-patterns. We next show the average and maximum
not support the normalization of algebraic datatypes due to                     runtime for the normalization algorithm. Finally, we show
implementation-level complexities. We thus excluded bench-                      the average similarity among the mutated benchmarks, again
marks with algebraic datatypes from our evaluation. Still,                      comparing pre, wo-SP, and w-SP. Figure 6 shows histograms
smtlib contains 41,166 benchmarks from 1,581 benchmark                          of the number of distinct benchmarks among the 10 mutations
families. We group benchmarks from this set into the (so-                       before and after (with super-patterns) normalization.
called) divisions used by the annual SMT-COMP [6] to keep                          First, we observe that before normalization, we nearly
the number of categories manageable.                                            always have 10 distinct versions of a benchmark. Exceptions
   The second set, mariposa, consists of the benchmarks                         (e.g., in the QF Strings category) occur when there are not
used in [26] (as provided in [27]), originating from program                    a sufficient number of user-defined symbols and assertions
verification projects written in Dafny [16], Serval [19], and F*                to create 10 distinct versions. For the smtlib benchmark
[22]. mariposa contains 16,622 benchmarks and is divided into                   set, normalization always significantly reduces the number
six families: Dice∗F [23] (1536), KomodoD and KomodoS [10]                      of distinct versions of a benchmark, and results with super-
(2,054 and 773), VeriBetrKVD [11] (5,170), VeriBetrKVL                          patterns always improve over those without super-patterns—
[18] (5,334) and vWasmF [5] (1,755).                                            sometimes significantly (e.g., in the Equality division).
   For each benchmark, we produce 10 mutations by randomly                         For other benchmarks, however, especially the
applying assertion shuffling and renaming. Our renaming uses                    QF Equality+NonLinearArith division and several families
a fixed enumeration of names (i.e., a benchmark wth n user-                     in the mariposa benchmark set, our normalizer struggles to
defined symbols always uses the first n of these names), but                    produce a small number of distinct outputs. Investigating
shuffles the order in which they appear in assertions (and thus                 these benchmarks reveals large numbers of assertions with
the order in which they are declared, since we declare symbols                  lots of symmetry. In these cases, the super-pattern comparison
in the order in which they appear). We ran all experiments on a                 fails to distinguish between assertions with identical patterns,
cluster of 48 machines with AMD Ryzen 9 7950X CPUs using                        resulting in different normal forms because of assertions
a time limit of 60 seconds and a memory limit of 8GB. We                        appearing in a non-deterministic order. It is worth highlighting
used this same time and memory limit to separately limit the                    that for these benchmarks, our normalization algorithm still
mutation step, the normalization step, and the solving step.5                   achieves a high level of similarity. As we discuss below, there
We do not report results for benchmarks that timed out during                   is also an improvement in stability for these benchmarks. This
mutation or normalization. For the smtlib set, we exclude 6                     suggests that full normalization is not necessary to improve
benchmarks that timed out during the mutation step and 85 that                  stability. Improved similarity is already helpful.
  5 This is long enough to be able to catch cases when the normalizer is slow
                                                                                   As mentioned above, over all of the benchmarks, only 87
and short enough to help keep a large evaluation computationally tractable.     are excluded due to timeouts during normalization, and these
Using the same timeout for all stages also keeps things simple.                 are typically very large benchmarks where parsing alone takes
                           (a) Before Normalization                                                (b) After Normalization

                               Fig. 6: Number of distinct benchmarks before and after normalization.

           Division (smtlib)             (Excluded/Total)   #Bench           #Unique              Time (s)               Similarity (%)
                                                                       pre    wo-SP  w-SP       Avg       Max      pre      wo-SP     w-SP
           Arith                                  (0/883)      883    9.33     1.05    1.02   0.0010    0.1720    7.07      99.39    99.62
           BitVec                                 (5/793)      788    9.36     1.07    1.03   0.0139    3.5230    5.81      99.01    99.48
           Equality                             (0/1,570)    1,570   10.00     8.48    2.79   0.0075    0.1020    0.05      47.59    98.48
           Equality+LinearArith                 (0/2,595)    2,595    9.99     7.34    5.35   0.0030    0.0860    1.29      65.56    86.78
           Equality+MachineArith                  (2/905)      903   10.00     1.25    1.22   0.0295    3.6140    0.76      97.97    98.18
           Equality+NonLinearArith              (0/1,452)    1,452    9.70     2.98    1.64   0.0080    0.4980    3.14      88.89    98.48
           FPArith                                (0/319)      319    9.48     1.03    1.03   0.0000    0.0010    5.25      99.61    99.61
           QF Bitvec                           (42/3,320)    3,278    9.55     4.94    4.78   0.7248   38.7570    4.63      74.17    79.88
           QF Equality                            (0/667)      667   10.00     2.63    2.16   0.0306    1.0710    0.73      85.67    93.24
           QF Equality+Bitvec                  (20/1,208)    1,188    9.87     4.49    4.44   0.1222   13.3070    2.94      71.07    74.06
           QF Equality+LinearArith               (12/812)      800    9.95     3.66    3.38   0.0590    6.6460    1.58      83.17    89.38
           QF Equality+NonLinearArith             (0/589)      589   10.00     6.73    6.22   0.2908   29.6690    1.76      71.40    85.08
           QF FPArith                           (0/4,813)    4,813    9.08     2.80    2.52   0.0002    0.0290   13.17      90.93    92.30
           QF LinearIntArith                   (6/10,801)   10,795    9.98     6.35    4.21   0.2728   37.2840    8.62      78.79    88.67
           QF LinearRealArith                   (3/1,466)    1,463    9.95     3.72    3.26   0.2230   30.3610    6.77      91.19    93.86
           QF NonLinearIntArith                   (0/653)      653    9.88     3.04    2.64   0.0752    4.5400    4.77      94.00    95.69
           QF NonLinearRealArith                (1/3,343)    3,342    9.83     1.83    1.67   0.0620   10.5110    8.42      96.05    97.76
           QF Strings                           (0/4,977)    4,977    6.21     2.69    2.45   0.0004    0.0190   44.50      91.75    94.93
           Family (mariposa)
           Dice∗F                               (0/1536)      1536   10.00    10.00   10.00   5.4847   12.4670    0.93      99.45    98.75
           KomodoD                              (0/2054)      2054   10.00    10.00   10.00   1.2750    3.7500    0.18      34.87    88.28
           KomodoS                               (2/773)       771   10.00     1.00    1.00   0.0004    0.0790    1.09     100.00   100.00
           VeriBetrKVD                          (0/5170)      5170   10.00    10.00   10.00   0.0790    9.1740    0.19      18.15    87.30
           VeriBetrKVL                          (0/5334)      5334   10.00    10.00   10.00   1.2533    9.6420    0.17      12.73    81.85
           vWasmF                               (0/1755)      1755   10.00     3.16    3.15   0.0657    4.2050    0.01      99.53    99.52


               TABLE I: Number of unique outputs, normalization time, and similarity of normalized outputs.

most or all of the time. For the vast majority of the remaining              in the SMT-COMP’s scrambling algorithm in use at the time
benchmarks, the normalization overhead is extremely low (a                   rather than with general-purpose normalization in mind.
fraction of a second on average as shown in Table I). The
aggregate overhead, computed as the sum of the normalizing                   B. Stability
time for all benchmarks divided by sum of the normalization                     In our second experiment, we evaluate how our normal-
plus solving time for all benchmarks, is less than 0.8%.                     ization algorithm affects solver stability. We use two SMT
   We also conducted exploratory experiments on a random                     solvers: cvc5 [1] and Z3 [7]. These are natural choices, as both
subset of smtlib (4,461 benchmarks) to evaluate the perfor-                  are used extensively and support a wide range of theories. We
mance of the normalizer in [24] in terms of uniqueness of the                limit our evaluation to these two solvers, as they are the only
normalized output. We observed that it was able to produce                   solvers that support all of our benchmarks. For the mariposa
unique outputs for only 12%, of the benchmarks, which is                     benchmark set, we limit our evaluation to Z3. This is because
vastly outperformed by our approach (87% on this set). This                  these benchmarks come from a specific use case targeting Z3
result, however, is not unexpected since the algorithm in [24]               (as observed already by Zhou et al. [26]), and most of them
was designed for the purpose of exploiting a specific weakness               are unsolvable by cvc5.
 Division (smtlib)                    cvc5 PR-2                   Z3 PR-2
                               no norm.       norm.        no norm.       norm        C. Code Optimizations
                                avg. MAD     avg. MAD       avg. MAD    avg. MAD
                                                                                         Some of the benchmarks in our benchmark sets are ex-
 Arith                       17,161 93.5 17,264 2.9 21,532 120.6 11,346 0.3
 BitVec                      29,141 41.0 29,247 14.6 34,245 121.4 28,248 14.6         tremely large, with sizes up to hundreds of megabytes and
 Equality                   101,912 286.0 101,778 4.0 107,718 108.8 107,885 10.7
 Equality+LinearArith        77,933 208.4 77,620 32.8 72,603 254.5 73,041 22.2
                                                                                      with up to hundreds of thousands of user-defined symbols
 Equality+MachineArith       91,935 23.4 91,518 6.8 74,037 452.8 73,539 37.2          and assertions. In this section, we discuss three optimizations
 Equality+NonLinearArith     97,462 351.0 95,961 10.8 89,615 375.5 90,551 17.1
 FPArith                     18,089 49.6 17,920 49.5 14,371 143.2 14,214 28.5         that are crucial for scalability of our algorithm on such
 QF Bitvec                  149,591 282.8 153,082 208.9 104,282 751.8 94,428 174.6
 QF Equality                  2,408 49.0 2,435 3.7        1,285 64.4 1,195 1.0
                                                                                      benchmarks.
 QF Equality+Bitvec          40,712 157.1 40,246 153.7 36,282 265.5 35,870 84.7             a) Pattern Compression: As presented in Section III,
 QF Equality+LinearArith     14,927 46.4 16,070 44.9      8,278 296.4 4,862 179.5
 QF Equality+NonLinearArith 34,344 422.9 34,234 276.0 25,811 374.6 25,731 175.3       formulas are sequences whose size corresponds to the size
 QF FPArith                  28,971 289.6 28,063 108.1 56,349 324.4 55,262 106.3
 QF LinearIntArith          242,429 402.8 244,127 148.7 151,935 606.8 132,783 345.7
                                                                                      of their abstract syntax tree. However, internally, SMT solvers
 QF LinearRealArith          30,567 313.6 29,539 101.0 23,547 310.8 21,260 160.4      represent formulas as directed acyclic graphs (DAGs), because
 QF NonLinearIntArith        34,201 615.7 34,267 26.3 23,914 194.7 22,265 6.8
 QF NonLinearRealArith       39,951 86.8 39,377 27.9 26,186 188.3 28,016 131.7        they often share subterms. The DAG representation can be
 QF Strings                  34,092 341.4 33,255 121.6 56,970 321.4 56,420 158.4
                                                                                      exponentially more concise. It is thus essential to also incor-
 Family (mariposa)
                                                                                      porate this kind of sharing in our representation of patterns.
 Dice∗F                            –    –       –     –    7,531 559.3 8,951 545.3
 KomodoD                           –    –       –     –   12,561 264.2 13,327 59.9    In our implementation, we represent a pattern as an index
 KomodoS                           –    –       –     –    3,284 79.9 3,181 17.2      into a dictionary of the subterms in the tree representation
 VeriBetrKVD                       –    –       –     –   12,623 414.4 12,612 169.0
 VeriBetrKVL                       –    –       –     –   24,889 203.6 23,971 172.7   of the pattern. For example, the formula ⟨+, ∗, x, x, ∗, x, x⟩
 vWasmF                            –    –       –     –    2,919 9.5 3,018 0.2
                                                                                      would be represented as the index 2 into the dictionary
TABLE II: PR-2 and MAD scores on mutated benchmarks                                   (1 : ⟨∗, x, x⟩, 2 : ⟨+, 1, 1).
                                                                                            b) Super-pattern Computation: A naive way to compute
before and after normalization.
                                                                                      the super-pattern for a symbol s is to traverse all of the asser-
   We use penalized runtime (PR-2) and Median Absolute                                tions and look up the role of s in every assertion. However, this
Deviation (MAD) as metrics. Penalized runtime the sum of                              approach is not scalable for large benchmarks. To address this
the time taken for solved benchmarks plus a penalty equal to                          issue, we perform a one-time indexing pass over the assertions
two times the timeout for each unsolved benchmark (timeouts,                          to create arrays for each symbol s containing pointers to
memory outs, or other errors). PR-2 thus combines elements of                         only the assertions in which s appears. This way, we only
both total time and number of solved benchmarks into a single                         need to traverse these assertions when calculating the super-
metric. MAD measures how much variation there is among a                              pattern for s. This optimization reduces the number of lookups
set of results, with lower numbers indicating less variation and                      from hundreds of millions to hundreds of thousands on some
higher numbers indicating more variation. Applying MAD to                             problematic benchmarks, improving the normalization time by
PR-2 scores is thus a good proxy for stability.                                       more than an order of magnitude.
                                                                                            c) Super-pattern Compression: This optimization lever-
   Results are shown in Table II for each division (in smtlib)
                                                                                      ages the sparsity of super-patterns: in large benchmarks,
and family (in mariposa). We report results on the benchmarks
                                                                                      each symbol typically appears in only a small subset of the
before normalization (no norm.) and after normalization with
                                                                                      assertions. Thus, the role of a symbol is likely to be 0 in
super-patterns (norm.). The column labeled avg contains the
                                                                                      most assertions. To exploit this, we represent super-patterns
average PR-2 score, computed as follows. Recall that we create
                                                                                      as sequences consisting of the non-zero role values interleaved
ten mutations for each benchmark. Each mutation is based on
                                                                                      with counts of the number of zeros.
a specific random seed. We compute the total PR-2 score for
all the benchmarks for each seed separately. We then take the                                               VI. C ONCLUSION
average of these ten PR-2 scores. The MAD is also computed                               Our normalization algorithm is a promising step towards
over these ten cumulative PR-2 scores (one for each seed).                            a more stable and predictable SMT solving experience. It
   We see that, for both solvers, the performance (avg. column)                       generally scales well and is applicable to a wide range of
on normalized benchmarks is generally comparable with that                            benchmarks and logics. We have shown that it can often
of non-normalized benchmarks, showing that, on average,                               produce a single unique normal form for a set of mutated
normalization does not appear to greatly affect runtime.                              benchmarks, and even when it cannot, it greatly increases the
   More importantly, the MAD score improves significantly                             similarity of the benchmarks. We also saw that, on average, it
in all cases, sometimes by more than an order of magnitude                            improves stability without significantly affecting performance.
(e.g., in the Equality division). This strongly suggests that our                        In future work, we intend to expand our normalizer to
normalization algorithm improves stability. Even for bench-                           handle other mutations such as antisymmetric operator re-
marks for which the normalizer completely fails to produce                            placement and operand swapping for commutative operators.
normal forms (e.g., the mariposa benchmarks that always still                         We also plan to explore whether additional normalization
have 10 distinct benchmarks after normalization), the stability                       techniques can be used to further improve our results. Finally,
improves, sometimes significantly. This provides promising                            we plan to investigate the use of our normalization algorithm
evidence that full normalization is not required for improving                        as a preprocessing step to improve the hit rate of applications
stability. An improvement in similarity may be sufficient.                            that cache formulas in order to reuse solving results.
                              R EFERENCES                                             Part I, volume 9779 of Lecture Notes in Computer Science, pages 361–
                                                                                      381. Springer, 2016.
 [1] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna
     Lachnitt, Makai Mann, Abdalrhman Mohamed, Mudathir Mohamed,
     Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew         [18] Jialin Li, Andrea Lattuada, Yi Zhou, Jonathan Cameron, Jon Howell,
     Reynolds, Ying Sheng, Cesare Tinelli, and Yoni Zohar. cvc5: A versatile          Bryan Parno, and Chris Hawblitzel. Linear types for large-scale systems
     and industrial-strength SMT solver. In Dana Fisman and Grigore Rosu,             verification. Proc. ACM Program. Lang., 6(OOPSLA1):1–28, 2022.
     editors, Tools and Algorithms for the Construction and Analysis of
     Systems - 28th International Conference, TACAS 2022, Held as Part
     of the European Joint Conferences on Theory and Practice of Software,       [19] Luke Nelson, James Bornholt, Ronghui Gu, Andrew Baumann, Emina
     ETAPS 2022, Munich, Germany, April 2-7, 2022, Proceedings, Part I,               Torlak, and Xi Wang. Scaling symbolic evaluation for automated
     volume 13243 of Lecture Notes in Computer Science, pages 415–442.                verification of systems code with serval. In Tim Brecht and Carey
     Springer, 2022.                                                                  Williamson, editors, Proceedings of the 27th ACM Symposium on
 [2] Clark Barrett, Pascal Fontaine, and Cesare Tinelli. The Satisfiability           Operating Systems Principles, SOSP 2019, Huntsville, ON, Canada,
     Modulo Theories Library (SMT-LIB). www.SMT-LIB.org, 2016.                        October 27-30, 2019, pages 225–242. ACM, 2019.
 [3] Clark Barrett and Cesare Tinelli. POSE: Phase ii: An open-source
     ecosystem for the cvc5 SMT solver, 2023.
 [4] Nikolaj S. Bjørner. SMT solvers: Foundations and applications. In Javier    [20] Mathias Preiner, Hans-Jörg Schurr, Clark Barrett, Pascal Fontaine, Aina
     Esparza, Orna Grumberg, and Salomon Sickert, editors, Dependable                 Niemetz, and Cesare Tinelli. Smt-lib release 2024 (non-incremental
     Software Systems Engineering, volume 45 of NATO Science for Peace                benchmarks), April 2024.
     and Security Series - D: Information and Communication Security, pages
     24–32. IOS Press, 2016.
 [5] Jay Bosamiya, Wen Shih Lim, and Bryan Parno. Provably-safe multi-           [21] Neha Rungta. A billion SMT queries a day (invited paper). In
     lingual software sandboxing using webassembly. In Kevin R. B. Butler             Sharon Shoham and Yakir Vizel, editors, Computer Aided Verification
     and Kurt Thomas, editors, 31st USENIX Security Symposium, USENIX                 - 34th International Conference, CAV 2022, Haifa, Israel, August 7-10,
     Security 2022, Boston, MA, USA, August 10-12, 2022, pages 1975–1992.             2022, Proceedings, Part I, volume 13371 of Lecture Notes in Computer
     USENIX Association, 2022.                                                        Science, pages 3–18. Springer, 2022.
 [6] Martin Bromberger, François Bobot, and Martin Jonáš. SMT Competi-
     tion (SMT-COMP) 2024, 2024.
 [7] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. Z3: an efficient        [22] Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine
     SMT solver. In C. R. Ramakrishnan and Jakob Rehof, editors, Tools                Delignat-Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Fournet,
     and Algorithms for the Construction and Analysis of Systems, 14th                Pierre-Yves Strub, Markulf Kohlweiss, Jean Karim Zinzindohoue, and
     International Conference, TACAS 2008, Held as Part of the Joint                  Santiago Zanella Béguelin. Dependent types and multi-monadic effects
     European Conferences on Theory and Practice of Software, ETAPS                   in F*. In Rastislav Bodı́k and Rupak Majumdar, editors, Proceedings of
     2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings, volume             the 43rd Annual ACM SIGPLAN-SIGACT Symposium on Principles of
     4963 of Lecture Notes in Computer Science, pages 337–340. Springer,              Programming Languages, POPL 2016, St. Petersburg, FL, USA, January
     2008.                                                                            20 - 22, 2016, pages 256–270. ACM, 2016.
 [8] Mike Dodds. Formally verifying industry cryptography. IEEE Secur.
     Priv., 20(3):65–70, 2022.
 [9] Herbert Enderton and Herbert B. Enderton. A mathematical introduction       [23] Zhe Tao, Aseem Rastogi, Naman Gupta, Kapil Vaswani, and Aditya V.
     to logic. Elsevier, 2001.                                                        Thakur. Dice*: A formally verified implementation of DICE measured
[10] Andrew Ferraiuolo, Andrew Baumann, Chris Hawblitzel, and Bryan                   boot. In Michael D. Bailey and Rachel Greenstadt, editors, 30th USENIX
     Parno. Komodo: Using verification to disentangle secure-enclave hard-            Security Symposium, USENIX Security 2021, August 11-13, 2021, pages
     ware from software. In Proceedings of the 26th Symposium on Operating            1091–1107. USENIX Association, 2021.
     Systems Principles, Shanghai, China, October 28-31, 2017, pages 287–
     305. ACM, 2017.
[11] Travis Hance, Andrea Lattuada, Chris Hawblitzel, Jon Howell, Rob            [24] Tjark Weber. Scrambling and descrambling SMT-LIB benchmarks.
     Johnson, and Bryan Parno. Storage systems are distributed systems (so            In Tim King and Ruzica Piskac, editors, Proceedings of the 14th
     verify them that way!). In 14th USENIX Symposium on Operating Sys-               International Workshop on Satisfiability Modulo Theories, Coimbra,
     tems Design and Implementation, OSDI 2020, Virtual Event, November               Portugal, July 1-2, 2016, volume 1617 of CEUR Workshop Proceedings,
     4-6, 2020, pages 99–115. USENIX Association, 2020.                               pages 31–40, July 2016.
[12] Chris Hawblitzel, Jon Howell, Jacob R. Lorch, Arjun Narayan, Bryan
     Parno, Danfeng Zhang, and Brian Zill. Ironclad apps: End-to-end
     security via automated full-system verification. In Jason Flinn and         [25] Y. Zhou, J. Bosamiya, J. G. Li, M. J. H. Heule, and B. Parno. Context
     Hank Levy, editors, 11th USENIX Symposium on Operating Systems                   pruning for more robust smt-based program verification. In N. Nar-
     Design and Implementation, OSDI ’14, Broomfield, CO, USA, October                odytska and P. Rümmer, editors, Proceedings of the 24th Conference
     6-8, 2014, pages 165–181. USENIX Association, 2014.                              on Formal Methods in Computer-Aided Design – FMCAD 2024, pages
[13] Robert Jones. Private communication, 2024.                                       59–69. TU Wien Academic Press, 2024.
[14] Daniel Kroening and Ofer Strichman. Decision Procedures - An Algo-
     rithmic Point of View, Second Edition. Texts in Theoretical Computer
     Science. An EATCS Series. Springer, 2016.                                   [26] Yi Zhou, Jay Bosamiya, Yoshiki Takashima, Jessica Li, Marijn Heule,
[15] Misha Lavrov. Algorithm for finding a “normal” form for a set of strings         and Bryan Parno. Mariposa: Measuring SMT instability in automated
     under character-mapping isomorphism? Mathematics Stack Exchange.                 program verification. In Alexander Nadel and Kristin Yvonne Rozier,
     https://math.stackexchange.com/q/2925668 (version: 2018-09-21).                  editors, Formal Methods in Computer-Aided Design, FMCAD 2023,
[16] K. Rustan M. Leino. Dafny: An automatic program verifier for                     Ames, IA, USA, October 24-27, 2023, pages 178–188. IEEE, 2023.
     functional correctness. In Edmund M. Clarke and Andrei Voronkov,
     editors, Logic for Programming, Artificial Intelligence, and Reasoning
     - 16th International Conference, LPAR-16, Dakar, Senegal, April 25-         [27] Yi Zhou, Bryan Parno, Marijn Heule, and Jay Bosamiya. Mariposa:
     May 1, 2010, Revised Selected Papers, volume 6355 of Lecture Notes               Measuring smt instability in automated program verification [bench-
     in Computer Science, pages 348–370. Springer, 2010.                              marks], January 2025.
[17] K. Rustan M. Leino and Clément Pit-Claudel. Trigger selection
     strategies to stabilize program verifiers. In Swarat Chaudhuri and Azadeh
     Farzan, editors, Computer Aided Verification - 28th International Confer-
     ence, CAV 2016, Toronto, ON, Canada, July 17-23, 2016, Proceedings,
                       VII. A PPENDIX                             argument of f in Ai and then adding an edge between u−1 (x)
Lemma VII.1. Let A be a sequence of formulas. If AR =             and u−1 (y) whenever the formula ⟨=, x, y⟩ appears in Ai .
R(AP ), where AP ∈ P (C(S(A))) and R is a renaming, then          Furthermore, shuffling the formulas in Ai , permuting the order
P (C(S(AR ))) = P (C(S(A))).                                      of the operands in equalities (the only commutative operator
                                                                  appearing in Ai ), or renaming the user-defined symbols does
Proof. First, note that for any formula sequence A, we have       not change the structure of the graph being represented. Thus,
R(P (C(S(A)))) = C(S(R(P (A)))). This is because the              all elements of P (C(S(Ai ))) represent isomorphic graphs.
first generates a set of equivalent formula sequences and then       Now, suppose N (A1 ) = N (A2 ), For i ∈ [1, 2], we know
renames the symbols, while the second renames the symbols         that N (Ai ) = R(A′i ) for some A′i ∈ P (C(S(Ai ))). Further-
and then generates a set of equivalent formula sequences, but     more, because renamings are injective, A′1 = P (R(A1 )) =
these two transformations are indpendent, so the result is the    P (N (A1 )) = P (N (A2 )) = P (R(A2 )) = A′2 . But for
same, regardless of which order they are done in.                 i ∈ [1, 2], the graph represented by Ai is isomorphic to the
     Now, we can write AR = R(P (A′ )) for some                   graph represented by A′i . Thus the graph represented by A1 ,
   ′
A       ∈ C(S(A)). It follows that P (C(S(AR ))) =                namely G1 , is isomorphic to the graph represented by A2 ,
P (C(S(R(P (A′ )))))        =      P (R(P (C(S(A′ )))))      =    which is G2 .
           ′
P (C(S(A ))), since computing the pattern of a renaming of           On the other hand, suppose G1 and G2 are isomorphic.
a pattern is just the same as computing the pattern. It remains   Let h : V1 → V2 be the isomorphism function for the graph
to show that P (C(S(A′ ))) = P (C(S(A))).                         vertices. Let R be a renaming such that ∀ v. R(P (v)) = h(v).
     But A′ ∈ C(S(A)), which means that A can be ob-              Applying this renaming to A1 must be equivalent (modulo or-
tained from A′ by swapping zero or more commutative               der) to A2 . In other words, A1 ∈ R(P (S(A2 ))). Then, because
operators and permuting the order of the formulas in A′ .         N is normalizing, we must have N (A1 ) = N (A2 ). Thus,
But then, any element of C(S(A)) can be obtained from             computing N is at least as difficult as graph isomorphism.
A′ by swapping commutative operators and permuting the
order, so C(S(A′ )) is just the same as C(S(A)). Thus,
P (C(S(A′ ))) = P (C(S(A))).
Lemma VII.2. For any formula A, P (C(S(A)))) has a
unique minimal element, according to ≺.
Proof. When comparing two elements of P (C(S(A))), each
of which is a sequence of patterns, we concatenate the patterns
together and compare them with ≺. Since ≺ is a total order,
one of them is always smaller. Thus there is a minimal element
of P (C(S(A))).
Theorem III.8. Function N is normalizing.
Proof. Notice that N (A) = R(A′ ), where R is the identity
function and A′ is the ≺-minimal element of P (C(S(A))).
It is not hard to see that R is also a renaming, so the first
requirement is met. Now, let M1 = R1 (M1′ ) and M2 =
R2 (M2′ ), with M1′ , M2′ ∈ P (C(S(A))), where R1 , R2 are re-
namings. By Lemma VII.1, P (C(S(M1 ))) = P (C(S(A))) =
P (C(S(M2 ))). But P (C(S(A))) has a unique minimal el-
ement, A′ by Lemma VII.2. Thus, N (M1 ) = A′ =
N (M2 ).
Theorem III.9. Let N be a normalizing function. Then,
computing N (A) for an arbitrary A is as hard as solving
graph isomorphism.
Proof. Let G1 = (V1 , E1 ) and G2 = (V2 , E2 ) be two
undirected graphs. Assume without loss of generality that
V1 ∩ V2 = ∅. For each v ∈ {V1 ∪ V2 }, let u(v) map v to
some unique user-defined symbol (i.e., u is injective). Now,
define Ai = {⟨f, x⟩ | x ∈ Vi } ∪ {⟨=, x, y⟩ | ∃ (v, v ′ ) ∈
Ei . {x, y} = {u(v), u(v ′ )}}, where f is some Boolean
predicate. Note that Gi can be recovered from Ai , simply by
creating a vertex for every user-defined symbol appearing as an
