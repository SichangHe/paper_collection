                                                                CDCL-inspired Word-level Learning
                                                                 for Bit-vector Constraint Solving∗
                                                            Zakaria Chihani, François Bobot, Sébastien Bardin
                                                          CEA, LIST, Software Security Lab, Gif-sur-Yvette, France
                                                                            (first.last@cea.fr)
arXiv:1706.09229v1 [cs.LO] 28 Jun 2017




                                                                                        Abstract
                                                       The theory of quantifier-free bitvectors is of paramount importance in software
                                                   verification. The standard approach for satisfiability checking reduces the bitvector
                                                   problem to a Boolean problem, leveraging the powerful SAT solving techniques
                                                   and their conflict-driven clause learning (CDCL) mechanisms. Yet, this bit-level
                                                   approach loses the structure of the initial bitvector problem. We propose a conflict-
                                                   driven, word-level, combinable constraints learning for the theory of quantifier-free
                                                   bitvectors. This work paves the way to truly word-level decision procedures for
                                                   bitvectors, taking full advantage of word-level propagations recently designed in CP
                                                   and SMT communities.


                                         1        Introduction

                                         Context. Since the early 2000’s, there is a significant trend in the research community
                                         toward reducing verification problems to the satisfiability (SAT) problem of first-order
                                         logical formulas over well-chosen theories (e.g. bitvectors, arrays or floating-point arith-
                                         metic), leveraging the advances of modern powerful SAT and SMT solvers [1, 2, 3, 4].
                                         Besides weakest-precondition calculi dating back to the 1970’s [5], most major recent
                                         verification approaches follow this idea [6, 7, 8, 9].
                                             In the context of verification, it is of paramount importance to efficiently and faith-
                                         fully represent basic data types found in any programming language, such as arrays,
                                         floating points, integers and – as is the focus of this paper – bitvectors (i.e., fixed-sized
                                         arrays of bits equipped with standard low-level machine instructions [1]).

                                         The problem. The standard approach for satisfiability checking reduces the bitvector
                                         problem to a Boolean problem, leveraging the powerful SAT solving techniques and their
                                         conflict-driven clause learning (CDCL) mechanisms [10, 11]. Yet, this bit-level approach
                                         loses the structure of the initial bit-vector problem, disallowing any possible high-level
                                         simplification other than at preprocessing and, in some cases, yielding scalability issues.
                                             ∗
                                                 Work partially funded by ANR under grants ANR-14-CE28-0020 and ANR-12-INSE-0002.


                                                                                            1
Recent efforts in both the CP and SMT communities have demonstrated the potential
benefits of word-level reasoning over bitvectors [12, 13, 14, 15, 16, 17] (where structural
information “is not blasted into bits” [18]), but these works are mostly limited to the
propagation step while the strength of modern SAT solvers rely on their learning mech-
anism [11]. Actually, two recent works [15, 19] do combine word-level propagation and
learning for bitvectors, yet the learning is either bit-level [15] or assignment-dependent
[19] in the vein of NoGood Learning [20].

Goal and challenge. Our goal is precisely to design a CDCL-like technique for the
theory of quantifier-free bitvectors, such that it is truly word-level, and such that the
learning stems from an interaction between the constraints involved in the conflict instead
of a particular assignment to variables that lead to a conflict. This learning should
be able to work together with recently developed word-level propagation techniques
for bitvectors. Furthermore, in the context of verification where several theories can
cooperate, it is also desirable that the technique can be combined with learning methods
over other theories.

Proposal and contributions. We propose to lift bit-level learning mechanism to
the word-level. This learning only makes sense if the decisions are allowed to be word-
level, propagation is word-level, the conflict detection is word-level, the explanations
are word-level and the sound rules of inference that derive knew knowledge from these
explanations are also word-level. Our very main contribution is a CDCL-style, word-
level learning over the theory of quantifier-free bitvectors, enjoying all good properties
from the SAT-based CDCL: the learnt clauses are part of the the theory of quantifier-free
bitvectors theory, they are asserting, they are minimal (only involve propagations that
lead to the conflict and variables that actively participated in the conflict), and of course
adding them is a sound extension of the original problem (they are implied by some of
the original constraints). More specifically, to achieve this goal, we design the following
original ingredients:
   • Word-level explanations for propagations of logical and structural bitvector opera-
     tions, through bitvector constraints, associated with masks indicating the positions
     that they fix in the variables (Sec. 3.1).
   • A sound extension to word level of the Resolution rule, using bitvector variables
     and constraints (Sec. 3.2).
   • An explanation selection algorithm that relies on bit-wise operations to minimize
     the number of learnt constraints (Sec. 3.3).
   • Finally, our learning mechanism, being based on resolution, can be combined with
     resolution-based learning on other theories (notably arithmetic), allowing to learn
     also from simplifications (Sec. 3.4) used at propagation [14].

Discussion. This work paves the way to truly word-level decision procedures for bitvec-
tors, taking full advantage of the word-level propagations recently designed in both CP
[12, 13, 14, 15] and SMT communities [16, 17, 19]. The presentation of our technique

                                             2
is high-level. The many important design questions behind an efficient implementation
(e.g., heuristics for clause deletion, using first versus last Unit Implication Point [2],
explanation recording techniques [21] – forward, backward or clausal, etc.) are left as
future work – but our current method is fully compatible with all of them.


2     Background
We briefly present the main characteristics of Conflict-Driven Clause Learning (CDCL),
and give a high-level presentation of the theory of quantifier-free bitvectors.

2.1    Conflict-driven clause learning
A constraint is a formula dependant on some variables to which one wishes to find, if
 any, an assignment to the variables that makes the formula true. A clause is a special
 kind of constraint in the form of a disjunction of Boolean variables. We use the word
“constraint” and “clause” interchangeably. A conflict is a state of affairs (empty domain
 for a variable, falsehood of an original constraint) that makes the problem unsatisfiable.
 Most solving algorithms follow a sequence: 1- propagate, 2- if there is a conflict then 3- do
“some Process C”, 4- else (once propagation is exhausted) make a decision (assign value
 to a variable, or restrict domain of a variable, or choose truth value of a constraint, etc.),
 then repeat. Originally, “Process C” was simply backtracking to the previous decision,
 but very early on, the problem of multi-occurring conflicts (or trashing [22]) lead to non-
 chronological backtracking algorithms. One of the most famous of these algorithm – the
 conflict-driven backjumping [23] – directly inspired [24] CDCL [10, 11], which deduces
 from a conflict some new facts (here: Boolean clauses) allowing to circumvent future
 similar conflicts, significantly short-cutting the search.
Learning techniques: requirements and properties. Learning algorithms are
usually built on the following key elements [11]:
 Explanations: to analyse the conflict, the solver needs to “know” the reasons for all the
     propagations that lead to that conflict. This implies that each propagation can
     generate some form of explanation, which is implied by the original set of clauses
     – either a theory lemma or some logical entailment (explanation soundness).
 Selection: once a conflict is detected, the learning algorithm must be able to select,
      from those explanations, the ones that actively participated in the conflict.
 Sound extension: to ensure that the learning algorithm only generates constraints (or
     clauses) that are implied by the original set of constraints, the relevant explana-
     tions that are selected are used to derive knew knowledge through sound rules
     of inference. In the case of CDCL, this rule is Resolution [25]. Thus adding a
     constraint that is a result of this inference is a sound extension.
    Besides these three key elements a few other properties are also desirable. (1) Theory
inclusion: if the learnt constraint is part of the theory of the original set of constraints,

                                              3
then there is no need to introduce extra machinery (any non-theory included constraint
must be supplied with dedicated propagation, conflict detection, learning, etc.) in order
to proceed with the solving. (2) Asserting clause: in order to shortcut the search, the
added (learnt) constraint should force, immediately after (non-chronological) backtrack,
a propagation that prevents the same decisions as those which generated the conflict.
(3) Minimality: the number of the constraints added through learning can be significant,
thus it is preferable to learn through information relevant to the conflict at hand, and
nothing more, in order to minimize the size of the added knowledge. The selection al-
gorithm should therefore discard what is not relevant to the conflict. However, if it is
possible to avoid more conflicts (create more shortcuts) with the same additional space
consumption (e.g., the same constraint), that would be an advantage. (4) Composition-
ality: problems involving many theories are common and very useful to verification, it is
therefore desirable that the different learning components of each theory can cooperate
with each another. The learning we introduce here can naturally be used in a wider
Resolution-based learning context.

2.2   Quantifier-free Bit-vector theory

Theory. A bitvector is a vector of binary values, 0 or 1 (as such, the representation of an
integer can be considered a bitvector). The theory of quantifier-free bitvectors surrounds
that data type with logical operations (bitwise disjunction (|), conjunction ( & ), negation
(.), etc.), structural operations (shift (≫, ≪), extraction (⌊.⌉i.j with j < i < size − 1 ),
concatenation ( :: ), etc.), and modular arithmetic. A bitvector constraints is of the
form a binop b = c, where binop is a binary operator, and of the form unop a = b,
where unop is a unary operator. These constraints can be considered atomically or
appear in a clause (a logical disjunction). We will present our algorithm in terms of unit
clauses which atoms are bitvector constraints. Through compositionality with Boolean
Resolution, however, it is possible to treat the wider clausal setting (Sec 3.2).

Bitvector domains inside a decision procedure. During a decision procedure, a bit
in a given bitvector variable can have one of 4 states, depending on previous decisions and
propagations: set (1), cleared (0), not yet known (?) and conflicting (⊥). A conflicting
bit is a bit that was fixed (cleared or set) and that a propagation requires to be fixed
to another value (resp. set or cleared). A conflicting variable is a variable containing
at least one conflicting bit. In this paper, a conflict is detected when a conflicting bit
is created, which is somewhat different from detecting conflict when a clause becomes
unsatisfiable. Interestingly, these bitvector domains are shared by different word-level
bitvector solvers from CP [12, 14, 15] and SMT [17, 19]. From a practical point of view,
they can be implemented either by a list [12], a run-length encoding (a representation
dependent on bit-alteration) [19] or (much more efficient) by a pair of integers, with a
clever use of machine operations [13].




                                             4
3     CDCL-inspired Word-level learning
Following the CDCL scheme (Section 2), we first introduce word-level explanations for
word-level propagations over bitvectors (Sec. 3.1), we soundly extend resolution rules to
bitvectors (Sec. 3.2), then we show how we analyse the conflict, select the explanations
and derive new constraints from them through our extended resolution (Sec. 3.3). Fi-
nally, we extend the explanation language and illustrate the compositionality of learning
through Resolution in order to encompass simplifications in the solver (Sec. 3.4).

3.1    Word-level explanations
We consider as a source for explanation the information propagated through the bitvector
abstract domain (Sec. 2), as it is clear that word-level learning should be based on
word-level decisions and propagations. Moreover, bitvector domains are already used in
existing word-level bitvectors solvers from CP [12, 14, 15] and SMT [16, 17, 19].
    The main idea here is to extend Boolean Resolution (the combination rule of CDCL)
to bitvector. The first step is to find clause-like structures that are really bitvector
constraints, yet still enjoying some of the properties of Boolean clauses. In the following,
We reuse notations of bitvector domains from Section 2. We also use the usual notation
bi to mean the ith bit of b (recall that indices start at 0 and that the least significant bit
is the rightmost one).

Definition 3.1. A word-level literal L (or simply literal when clear from context), when
b is a bitvector variable, is given through the following rules:

         L ::= T | T         T ::= A | A ≫ A | A ≪ A            A ::= b | b | constant

where ≫, ≪ are logical shift operators. •

     We say that a bitvector variable b is set (resp. cleared) through a list of literals L
if its domain is set (resp. cleared) wherever (i.e., on all positions where) the domains
of all literals of L are set (resp. cleared), and we write (L) ⇁1 b (resp. (L) ⇁0 b).
For example, from a constraint a & b = c, where a, b, c respectively have the abstract
domains J1??1K, J01??K, J??01K, we forward propagate into c, through (c) ⇁0 c, clearing
c1 , and (a, b) ⇁1 c setting c0 , and backward propagate through (c) ⇁1 a and (c) ⇁1 b
setting a2 and b2 , (c, a) ⇁0 b clearing b3 . The constraint a ≫ n = b backward propagates
using (b ≪ n) ⇁0 a and (b ≪ n) ⇁1 a.

Definition 3.2. A word-level clause, or w-clause is of the form L = 1 where L is a
bitwise disjunction of l-sized literals and 1 is a sequence of l ones ( i.e., the bitvector that
is set on every bit). By analogy with a Boolean clause, we write the constraint (L = 1 )
simply as the disjunction of literals L. •

     A w-clause is called a “propagation clause” when it is used in the explanation of a
propagation. When a propagation takes place in the domain of a variable x through
(a1 , · · · , an ) ⇁0 x (resp. (b1 , · · · , bm ) ⇁1 x), where ai and bi are (possibly shifted)

                                               5
    Table 1: Propagation constraints for &, |, ⊕, and shifts, where {♦, } = {≪, ≫}

                          x&y=z          x|y=z          x⊕y =z        x♦y = z
                            z|x           x|z            z|x|y        z | x♦y
                            z|y           y|z            z|x|y        z | x♦y
                           z|x|y         z|x|y           z|x|y        x | zy
                                                         z|x|y        x | zy



literals, it can be explained through the w-clause x | a1 | · · · | an (resp. x | b1 | · · · | bm ).
Table 1 summarizes the w-clauses for the four main bitvector constraints.

Proposition 3.1 (Explanation soundness). The propagation clauses of Table 1 are im-
plied by their respective bitvector constraint.

   Consider the (on the right) logical simplification using classical equivalencies and de
Morgan rules of the bit-blasting encoding [1] (on the left) of the constraint x & y = z,
where v0 , · · · , vl−1 are the Boolean variables representing the l long bitvector variable v:

         ^
         l−1                                    ^
                                                l−1
               ((xi ∧ yi ) ←→ zi )       ≡            ((xi ∨ yi ∨ zi ) ∧ (zi ∨ xi ) ∧ (zi ∨ yi ))
         i=0                                    i=0

From this, it follows that each bitvector conjunction constraint implies three other con-
straints that are really w-clauses:
         (x & y = z)        =⇒       (z | x | y = 1)     ∧    (z | x = 1)     ∧     (z | y = 1)

A similar argument can be made for the other constraints of Table 1.
   Note that the same w-clause can serve as a propagation explanation for more than
one constraint. For example, z | x | y explains setting z wherever x is set and y is cleared
from the constraints z = x & y, z = x ⊕ y, x = y | z, etc.

Explanation triples. To be useful, each explanation must record two pieces of infor-
mation : why the propagation took place – the propagation w-clause, call it C– and
when it took place – by indicating the decision level or depth p of the propagation (the
number of decisions that preceded this propagation).
    In addition, because we deal with bitvector variables of which some bits may be
unaffected by the propagation, we need a third piece of information m we call impact
mask which is set for those bits of the variable that were unknown before and that were
cleared or set through the propagation.

Definition 3.3. An explanation triple (p, m, C) explains the propagation at decision level
p on a variable along the positions set in the mask m using the propagation clause C. The
set of explanations of a variable x is written E(x). We say that an explanation covers a
bit (or a position) if its impact mask is set on that position. •


                                                   6
    We emphasize the following remarks. Firstly, because the impact mask only indicates
the bits that were unknown and became fixed, no two explanations can cover the same
bit: the order in which the propagations are done imposes this separation. For example,
from the two constraints e & c = a, f | b = c, with a = J1110K, b = J0111K and e, f, c
are unknown, at a decision level p, both constraints can set the two middle bits of c,
through the propagation w-clauses a|c or b|c respectively. However, only one of them
(the first to “fire”) will be in an explanation that covers the two middle positions, i.e.,
either {(p, a|c, 1110), (p, b|c, 0001)} ⊆ E(c) or {(p, a|c, 1000), (p, b|c, 0111)} ⊆ E(c).
    Secondly, consider the constraint C : x | y = z, where x and z are unknown, y =
J00??K. After a decision at level p on some other variable, the propagations can follow
this ordered sequence: x gets cleared by some other constraint (x = J0000K), which clears
z on some bits (z = J00??K) through C, then y gets cleared by some other constraint (y =
J0000K), and then z gets completely cleared (z = J0000K). Notice that the explanations
for z will both have the same propagation w-clause: (p, 1100, x | y | z), (p, 0011, x | y | z).
We choose to simplify such instances, i.e., same propagation w-clause occurring at the
same decision level, to (p, 1111, x | y | z) by disjuncting their impact mask. Thus there
is always a unique pair (p, C) for each decide depth and propagation w-clause in the set
of explanations of a given variable.

3.2    Word-level resolution for w-clauses
A sequence of resolution steps involving disjoint set of clauses and variables can be
carried out in parallel. Because a w-clause is essentially a group of Boolean clauses, they
can subject to a word-level Resolution rule. Indeed, l resolution steps between clauses
involving the Boolean units ai , bi , ci (for i = 0..l − 1) can be considered as a word-level
rule of Resolution between w-clauses involving l−bit long variables a, b and c.
   a0 ∨ c0     c0 ∨ b0 a1 ∨ c1      c1 ∨ b1        al−1 ∨ cl−1     cl−1 ∨ bl−1   a|c     c|b
                      ,                     ,··· ,                             ≡
         a0 ∨ b0             a 1 ∨ b1                      al−1 ∨ bl−1               a|b

Proposition 3.2 (Soundness of inference). Word-level Resolution is a sound extension
of binary Resolution.
     Word-level resolution on a shifted literal is less immediate. Consider    Vl−1−nthat a shift
constraint a ≫ n = b is equiprovable with the Boolean encoding ( i=0 an+i ←→
        V                                     Vl−1−n                  V
bi ) ∧ ( l−1
          i=l−n 0 ←→ bi ), which implies ( i=0         an+i ∨ bi ) ∧ ( l−1
                                                                        i=l−n bi ), which in turn
is equivalent and justifies the propagation w-clause a ≫ n | b. The resolution can be
extended to bitvector constraints  V involving shift. One can, for example resolve a ≫ n | b
with a | c, whose encoding is ( l−1  i=0 ai ∨ ci ) to obtain c ≫ n | b. Indeed, this bitvector
resolution can be simply seen as a group of n Boolean      resolution steps between an+i ∨cn+i
                                                      Vl−1−n
and an+i ∨ bi , for i = 0..l − 1 − n, obtaining ( i=0 cn+i ∨ bi ), which in conjunction
        V
with ( l−1i=l−n bi ) is equivalent to c ≫ n | b. More generally we can use the resolution
rules:
                      A | (y ≫ n) B | y                  A | (y ≪ n) B | y
                         A | (B ≫ n)                         A | (B ≪ n)

                                               7
    The word-level resolution rules acting on two shifted literals are justified in the same
way. Of course, such a resolution only makes sens if the two shifts preserve some bits
that are common to (that come from the same position of) the two literals, for example
the literals y ≪ n and y ≫ m, such that n + m ≥ size(y) have no bits in common.
Fortunately, the selection algorithm presented in the next section, by construction, only
selects w-clauses for which resolution is justified. The two literals can either have the
same shift or opposing shift. The rules to apply depend on the length of each shift. In
the following, {♦, } = {≪, ≫}:
        A | (y♦n) B | (y♦m) n > m             A | (y♦n) B | (y♦m) n ≤ m
                A | ((Bm)♦n                          B | ((An)♦m
Finally, resolution on two opposing shifted literals is as follows:
      A | (y ≫ n) B | (y ≪ m) n > m                     A | (y ≫ n) B | (y ≪ m) n ≤ m
A | (B ≫ (m + n)) | (2m − 1) ≪ (l − (n + m))            B | (A ≪ (m + n)) | (2n − 1) ≪ m
notice that these rules subsume the above Resolution rules (if n = 0 or m = 0).
    The logical and structural operations on bitvectors all can be propagated using the
basic blocks of conjunction, disjunction, negation and shift. For example, concatenation:
a :: b = (a ≪ kbk) | b, extraction: ⌊a⌉i.j = (a ≫ j) & (−1) ≪ (i − j + 1), in addition
to involutive negation of these operations: a :: b = a :: b and ⌊a⌉i.j = ⌊a⌉i.j . If the
literal’s syntax is extended to include extraction and concatenations, one can also use
the derivable rules of inference:
            A | ⌊x⌉i.j x | B         A | x :: C x | B         A | C :: x x | B
                A | ⌊B⌉i.j               A | B :: C               A | C :: B

However, for simplicity, we will present the conflict analysis and learning only through
the basic blocks.
Normalizing. In order to obtain the actual w-clauses, we normalize using (non-exhaustively
listed) rewrite rules such as:

    (A#B) :: C 7−→ (A :: C)#(B :: C)          ⌊(A#B)⌉i.j 7−→ ⌊A⌉i.j #⌊B⌉i.j
    C :: (A#B) 7−→ (C :: A)#(C :: B)          A & B 7−→ A ∧ B
    (A#B)♦n 7−→ A♦n#B♦n                       A♦n 7−→ (2n − 1)(kAk − n) | A♦n

where # ∈ { & , |} and {♦, } = {≪, ≫}.
Proposition 3.3. The normalization rewrite rules form a terminating rewrite system.
   Sketch of proof: By decreasing distance between the root and the logical connectives.
Mixing theories. While this paper is concerned with purely bitvector constraints, it is
worth noting that the above bitvector resolution rules can combine with usual resolution.
                                  F ∨ (a | c) (c | b) ∨ G
                                     F ∨ (a | b) ∨ G

                                             8
In section 3.4, we will use this fact to explain simplifications and factorizations, and
include them in our analysis.
Theorem 3.1 (Learning soundness). Any constraint obtained from the word-level resolu-
tion of w-clause (and Boolean resolution) is implied by the original problem and therefore
constitutes a sound extension of it.

3.3    Word-level Conflict analysis
We recall that a conflict is detected when a conflicting variable has a conflicting bit (Sec-
tion 2.2). We now show how word-level analysis is carried out, isolating the explanations
for that conflict from the irrelevant explanations, resulting in conflict-driven word-level
learning that is expressed inside the theory of quantifier-free bitvectors, i.e., through
bitvector constraints.
    When the propagation of a constraint requires to set (resp. clear) one or more bits
of a variable that were previously cleared (resp. set), a conflict is detected on those bits.
A mask that is set on those conflicting positions is called a conflict mask. For example,
propagating from a & b = c, with current domains a = J?1111111K, b = J1?111111K
and c = J00?00000K may generate a conflict through forward propagation resulting in
c = J001⊥⊥⊥⊥⊥K or through backward propagation, resulting a = J011⊥⊥⊥⊥⊥K or
b = J101⊥⊥⊥⊥⊥K, in all these cases the conflict mask is 00011111 and the aborted
propagation clause is c | b | a. This w-clause is called conflict w-clause.
    This grouped detection exploits the word-level propagation as opposed to the conflict
detection done through bit-blasting, one bit at a time. The main observation is the
following: if several conflicting bits are generated through the same propagations from
the same variables, then there is no need to learn more than one bitvector constraint
for those bits. In general more than one w-clause is learnt, possibly in parallel, after a
single conflict.
Main idea. For simplicity, we only discuss the algorithm for non-shifted literals (i.e.,
variables) and we will then extend it. The algorithm starts from the conflict at decide
level p caused by a propagation clause R on the positions set in a conflict mask m
of some variable. The algorithm could be seen as applying Boolean CDCL in parallel
on all the set bits in the conflict mask m. At some points the bits could have different
explanations and so the mask would be split and the algorithm continues on two different
inputs. Seeing each bit in isolation should be reminiscent of Boolean CDCL: each bit bi
of each variable b of R, such that the ith bit of m is set, is necessarily fixed (a propagation
through a w-clause on that bit has the same behaviour as a unit propagation through a
Boolean clause: all other variables in the clause must be fixed). We call such bits – that
participated in the conflict – the culprit bits of b. The values of the culprit bits were
either fixed before p (pre-p) or through a propagation at p (@p). In the former case, there
are no @p explanations that cover bi ; in the latter case, there is exactly one explanation
that covers it. We define the explanation equivalence (=E ) of bits bi and bj such that
bi =E bj if they are either both pre-p or are both covered by the same @p explanation
in E(b). This equivalence relation is the one that fixes the number of eventually learnt

                                              9
clauses: there is a new clause each time there is more than one equivalence class on the
bits of a variable.

Definition 3.4. A reason R is a w-clause that serves as an accumulator and is initialized
with the conflict w-clause. Each reason is associated with an analysed mask m, initialized
by the conflict mask. For each equivalence class E = of the culprit bits of each variable
in R, a separate copy of R is created and associated with a new analysed mask which
is set on the position of the bits in E = . Once a variable has been investigated in this
manner, it is marked, such that it is purged from future resolution steps of the algorithm.
We call a leaf a reason whose literals are all marked (thus it is fully investigated). At
the end of the analysis, all leaves are learnt. Finally, we call set of reasons the set of
tuples (p, R, ma , M) containing the reason R, associated analysed mask ma , decide depth
p, with marked literals M. •


Algorithm 1 analyse(p, R, ma , M) (reason R, analysed mask ma , decide depth p,
with marked literals M)
 1: if ∃x ∈ R, x ∈/ M then
 2:    if ∃(p, C, mi) ∈ E (x) s.t. mi & ma 6= 0 then
 3:       if mi & ma = ma then
 4:          return {(p, Resol(R,C,x,M), ma , {x} ⊎ M)}
 5:       else
 6:          min = mi & ma
 7:          mout = ma ⊕ min
 8:          S = Resol(R,C,x,M)
 9:          return {(p, S, min , {x} ⊎ M), (p, R, mout , M)}
10:       end if
11:    else
12:       return {(p, R, ma , {x} ⊎ M)}
13:    end if
14: else
15:    return {leaf(R)}
16: end if



Conflict analysis algorithm. After a conflict, the set of reasons starts as a single-
ton containing the tuple formed with the conflict propagation R, the conflict mask m,
the current decision level p and an empty set that will hold the marked literals, i.e.,
{(p, R, m, {})}. The (parallelizable) algorithm consists of the repeated rewriting of the
set of analysed reasons until all its elements become leaves, at which point they are all
learnt.
                   {(p, R, ma , M)} ⊎ S 7−→ analyse(p, R, ma , M) ⊎ S
    For now, we voluntarily omit shifted literals in Algorithm 1, (we will see shortly how
to easily extend it for shifted literals). We comment this algorithm through the following
example, where, at decide level (i-1), values are c =??11, v = 1111, e = 0000, g = 00??,




                                                   10
h =??00, and unknown for the rest.

        (1.)d = c | x                   (2.)e = b ⊕ f                    (3.)f = d & v
        (4.)g = f & a                   (5.)h = f & a                    (6.)a = b & c

Then, at level i, we decide d = 0000. The following table lists the explanations stemming
from that decision. We omit the decide level from the triples (all explanations are of the
current decision level i) and replace it, for readability, with the index of the constraint
that spawned the propagation they explain.

                      f                      b                     c                    a
            (3, f | d | v, 1111)   (2, b | e | f , 1111)   (1, c | d, 1100)   (4, g | f | a, 1100)
                                                                              (5, h | f | a, 0011)

At this point the 6th constraint tries to propagate with w-clause a | b | c and provokes a
conflict on all bits. Conflict analysis then begins with the initial set of analysed reasons
containing the tuple {(i, a | b | c, 1111, {})}.

Unfolding the algorithm. The algorithm selects the literal a (Line 1), and the first
selected explanation for a is (i, g | f | a, 1100) since 1100 & 1111 6= 0. The test of
Line 3 is not satisfied however because the impact mask of the propagation clause does
not cover all the conflict mask. In the else branch, two masks are created: one, min ,
will be the analysed mask of the reason resulting from the resolution of the propagation
clause and the current reason, the other, mout , represent the conflict bits that must be
explained elsewhere. The algorithm returns two tuples: {(i, g | f | b | c, 1100, {a}), (i, a |
b | c, 0011, {})}. The former will be rewritten along the left branch of Figure 1, the
latter – where a is not marked – will select a again and this time chose the all covering
explanation that comes from the 5th constraint. Once there are no more variables to
select from a reason (i.e., all variables are marked, Line 11), that reason is marked as a
leaf. Interestingly, because the learnt constraint has a clausal form, it serves as its own
propagation clause.
    Figure 1 summarizes the learning through conflict analysis. The nodes are the reasons
and the analysed mask (with the root being the initial pair). Each edge labelled with
a variable name represents a resolution step on that variable between the parent reason
and the propagation clause of the explanation of that variable that covers the resulting
analysed mask.
    Notice how c stays only in one of the learnt w-clauses, because the right analysed
mask is not covered by any current decision-level explanation of c, meaning that the part
of c that participated in the conflict predates the decision, and indeed, initial value for c
was ??11. The two learnt clauses propagate each 2 bits into d, avoiding the conflict.
    This learning through interaction of constraints, independent of a particular assign-
ment, has the advantageous side effect of preventing word-level conflicts from potentially
bit-level conflicts, i.e., even a conflict mask with a single set bit will result in a learnt
w-clause that impacts all positions of its variables, thus avoiding more than that exact
conflict with the same amount of added space.

                                                      11
                                              a | b | c , 1111
                                        a                         a

                      g | f | b | c, 1100                         h | f | b | c, 0011
                                b                                            b
                      g | f | e | c, 1100                         h | f | e | c, 0011
                                 f                                            f
                    g | d | v | e | c, 1100                      h | d | v | e | c, 0011
                                c
                      g | d | v | e, 1100

              Figure 1: Conflict analysis through rewriting and resolution


Different strategies. The order in which the analysed reasons are rewritten by analyse
can be tuned to obtain certain known strategies such as First-UIP or Last-UIP [2]. The
determined strategy can be implemented by the order induced by a trail.

Treating structural operations. A slight addition to the above algorithm allows to
treat shift operations. If the selected literal appears shifted by n, then the search for an
explanation among the literal (line 3) uses the same shift of the impact mask. Line 1’s
test becomes ∃a ≫ n ∈ R, and line 2’s test becomes “s.t (mi ≫ n) & ma 6= 0”. Other
structural operations are also adapted accordingly, or supported through the rewriting
that uses shift operations and logical operations.

Taming non-asserting learnt clauses. To be useful, a learnt clause must be asserting,
i.e., force a propagation after a backtrack (or a back-jump) so as to avoid the same
conflict. With our method, this is not always the case. Consider the example on 2-
bits variables given on the left of Figure 2, where current assignment for a, b, c, v is
respectively 0?, 0?, ?1, 00. Then we decide that d = 11, we get (omitting impact mask
and decide depth): from 3 that a = 00 with the propagation clause a | v | d ; from 2,
that b = 01 with b | d ≫ 1 ; from 1, we get a = 01 with a | c | b: conflict with mask
01. Then resolution gives us the clausal constraint c | v | d | d ≫ 1, the conclusion of
the derivation on the right of Figure 2. After backtracking and applying the values for
c and v, we get ?0 | d | d ≫ 1 which does not propagate. Indeed, if we look at the level
of bits, this gives the clauses c1 ∨ d1 and d0 ∨ d1 .

           1. a = c & b                                            a|c|b      a|v|d
           2. b = d ≫ 1                               b|d≫1            c|b|v|d
           3. v = a & d                                     c|v|d|d≫1
          Figure 2: Non-asserting clauses justify partial decision on variables

   The above clause provokes a problem because it relates different positions in the
same variable (the variable d above appears both as a literal with and without shift).
This sort of problem arises because a decision is allowed to be made on many bits of the

                                                    12
same variable, unlike in bit-blasting where decisions are made on Boolean variables.
    To account for these problematic cases, the constraint solver must include in the
bitvector domain representation some indication that the incriminated variable (the one
which bits are related by the clause, here d) can only be subject to partial decisions.
This extra information can be a simple flag that, if set, forces a naive bit-by-bit decision,
but a more sophisticated information can be generated using the conflict mask to derive
decision masks associated to the variable, whereby grouped decisions are allowed on the
bits indicated by that mask for that variable. This way, the clause becomes asserting, in
the sense that the domain representation of the variable has been propagated in a way
that prevents the conflict from arising again.

3.4   Extended explanations for learning from simplifications
The explanations presented so far fit well bitvector domain propagation, yet the solving
process can be greatly improved by simplifications and factorizations [14]. We explain
how the learning presented in this paper can be naturally extended to these extra prop-
agations.
                                                   ε
Extended explanations. We use C                  E to mean that the constraint C can
generate the explanation containing the propagation clause E and omit decide depth.
We can now explain using regular Boolean clauses as well, where atoms are formed
through bitvector constraints, equalities or disequalities. Some selected simplifications
and factorizations are as follows (we consider the equality constraint a = 0 and the
bitvector literal a to be equivalent):
   • A logical shift constraint a = a ≫ c implies the nullity of a if c > 0. We allow each
     logical shift constraint to generate an explanation for such an update:
                                      ε
                   a1 = a2 ≫ c              (a1 = a2 ) ∧ (c > 0) → (a1 = a2 = 0)

   • A disjunction constraint a = b1 | b2 becomes an equality between a and b1 when
     b2 becomes 0, and vice versa, with explanations:
                                  ε
                    a = b1 | b2           bi = 0 → (a = bj ) with {i, j} = {1, 2}

   • The exclusive disjunction constraint a = b ⊕ c is equivalent to any permutation of
     its variables, and two ⊕ constraints with 2 common variables prompt an equality
     between their third respective variables, with the following explanation – where
     x, y, z (resp. x′ , y ′ , z ′ ) is a permutation of a, b, c (resp. a′ , b′ , c′ ):
                                               ε
                 a = b ⊕ c ∧ a′ = b′ ⊕ c′              (x = x′ ) ∧ (y = y ′ ) → (z = z ′ )

   The basic idea is then to combine our word-level resolution together with regular
Boolean resolution in order to derive learnt clauses.

Example. We now give an example where, to keep it simple, the explanations cover all
the conflict mask, such that only one clause is learnt in the end.


                                               13
     (1.)x = x ≫ y          (2.)z = x | t            (3.)z = a ⊕ b        (4.)b = c ⊕ t
     (5.)a = c ≫ y          (6.)a = v & m            (7.)a = v | n

    We suppose current known values are m = 1111 and n = 0000, and we decide on
y = 0011, (or 3, in decimal notation). Then, propagation steps are: x = 0 from 1
because y = 3 > 0, z = t from 2 because x turned into the neutral element, then from
3 and 4 get a = c, and from that and y = 3 > 0 get a = 0, finally, through bitvector
propagation a = v & m propagates that v = 0 then a = v | n attempts to change that
to v = 1111: conflict. The resolution derivation that allows learning is shown in Figure
3 (the numbers in the leaves are those of the constraints that prompted the respective
explanation clause). This derivation uses both bitvector word-level resolution (marked
with a double horizontal line) and regular Boolean resolution (marked with a single
horizontal line). The conclusion of that derivation, i.e., the learnt clause (m|n)∨¬(y > 0)
(combining both bitvector and arithmetic atoms) excludes any value strictly greater than
0 from the concretization of y in the (current) event that n = 0 and m = 1111.

                                                        6.      7.
                                                         ..      ..
                                                          .       .             5.
                                                      v|a|m   v|a|n              ..
                                         3, 4                                     .
                                           ..
                          2.                ..           a|m|n       ¬(a = c) ∨ ¬(y > 0) ∨ a
                           ..     ¬(z = t) ∨ (a = c)         (m|n) ∨ ¬(a = c) ∨ ¬(y > 0)
           1.               .
            ..       ¬x ∨ (z = t)               (m|n) ∨ ¬(z = t) ∨ ¬(y > 0)
             .
      ¬(y > 0) ∨ x                  (m|n) ∨ ¬x ∨ ¬(y > 0)
                        (m|n) ∨ ¬(y > 0)
    Figure 3: Learning through a combination of bitvector- and Boolean- resolution



4    Related work
We have already discussed at length the general CDCL approach [10, 11] as well as its
straightforward instantiation to bit-level learning over bitvectors in Sections 1 and 2. We
present now a few other learning methods from Constraint Programming (CP) – that
can be in some ways adapted to world-level bitvector learning , as well as the very few
learning methods dedicated to bitvectors.

Learning in Constraint Programming. There is a number of published work ex-
ploring learning capabilities in the context of a CP solver. Lazy Clause Generation [26]
converts constraint propagators into clauses and feeds them to a SAT solver, showing sig-
nificant results for scheduling problems. We are not aware of any treatment for bitvectors
in this context but suspect that any such treatment would resort to bit-blasting (neces-
sary to use a SAT solver in the background), which is precisely what we are trying to


                                                14
avoid. (Generalized) NoGood Learning techniques [27, 20] improve backtracking search
in the context of Constraint Satisfaction Problems. Basically, (Generalized) NoGood
learning allows to add partial assignments and non-assignments that are known to lead
to conflict. This method extends naturally to word-level learning for bitvectors, yet our
own approach is more general, as our learnt constraints do not mention particular as-
signments, they are solely derived from the relationship between the propagation clauses
of the constraints that lead to a conflict. The HaifaCSP solver [28] is able to learn
general constraints through a resolution-inspired method in a more general and concise
way than nogood assignments. The approach uses a non-clausal learning that relies on
direct inference between the constraints themselves as well as SAT inspired techniques,
notably a similar heuristic to VSIDS [3] for variable ordering. It currently handles many
of the constraints appearing in modern CP solvers, yet bitvector constraints are not
handled. Being resolution-based able to handle integer constraints, this technique is a
good candidate to test the limits of the ideas presented in this paper for theory learning
cooperation.

Learning over bitvectors. There are two most closely related papers, mentioned in
the introduction. First, Wang et al. describes a solver [15] that uses the same word-level
propagations as we do but delegates bit-level learning to a SAT solver. Focusing on the
learning scheme, which is the subject of our paper, the comparison between our work
and this one is the same as with any bit-blasting learning approach.
    The closest related work is a model constructing SAT solver [17] whose learning
mechanism was extended [19] to the theory of quantified free bit-vectors, named mcBV
and avoiding bit-blasting. The learning mechanism of mcBV resembles nogood learning
in that it starts from a particular failing assignment. The difference is in mcBV’s gener-
alization method that starts from that assignment and weakens it as much as possible
through successive flipping of bits from known to unknown. In contrast to our learning,
which directly involves interactions between propagators, this learning is still tied to a
particular assignment. Finally, the mcBV approach’s handling of bounded arithmetic
makes it a good candidate for combination with our approach.
    One can also find a relation to the lazy layered [18] treatment of the theory of
quantifier-free bitvectors, where bit-blasting is only invoked if necessary (the bits of
a bitvector are all considered equal until those bits are affected differently – through a
propagation or through a conflict – at which moment that vector is only blasted as much
as necessary). Learning in that setting depends on where bit-blasting is done and is still,
in essence, Boolean CDCL, even if each Boolean variable can potentially represent all
bits of a variable (since those bits must be equal).


5    Conclusion
This paper presents a word-level CDCL-style learning mechanism for the theory of bitvec-
tors, which is of paramount importance in software verification. The technique can be
integrated in any world-level bitvector solver, whatever the underlying technology (CP


                                            15
[14] or natural-domain SMT [16]), as long as the deduction mechanism produces the
required domain-based explanations and conflict detection. This work illustrates the ef-
fect of cross-fertilization between the CP and SMT community that brought forth many
fruitful advances, most notably CDCL itself.
     The immediate future work is, of course, the implementation of our ideas in a word-
level solver for practical evaluation and the fine-tuning of all practical ingredients of an
efficient CDCL-style learning mechanism, including clause deletion, variable ordering,
and other learning-related heuristics.


References
 [1] Daniel Kroening and Ofer Strichman. Decision Procedures: An Algorithmic Point
     of View. Springer Publishing Company, Incorporated, 1 edition, 2008. ISBN
     3540741046, 9783540741046.

 [2] João P. Marques Silva and Karem A. Sakallah. GRASP: A search algorithm for
     propositional satisfiability. IEEE Trans. Computers, 48(5):506–521, 1999. URL
     http://dx.doi.org/10.1109/12.769433.

 [3] Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang, and Sharad
     Malik. Chaff: Engineering an efficient SAT solver. In Design Automation Confer-
     ence, DAC. ACM, 2001.

 [4] Clark W. Barrett, Roberto Sebastiani, Sanjit A. Seshia, and Cesare Tinelli. Satisfi-
     ability modulo theories. In Handbook of Satisfiability, pages 825–885. 2009.

 [5] Edsger Wybe Dijkstra. A discipline of programming, volume 1. Prentice-Hall En-
     glewood Cliffs, 1976.

 [6] Edmund M. Clarke, Daniel Kroening, and Flavio Lerda. A tool for checking ansi-c
     programs. In TACAS, pages 168–176, 2004.

 [7] Patrice Godefroid. Test generation using symbolic execution. In FSTTCS, pages
     24–33, 2012.

 [8] Thomas A. Henzinger, Ranjit Jhala, Rupak Majumdar, and Grégoire Sutre. Lazy
     abstraction. In POPL, pages 58–70, 2002.

 [9] Kenneth L. McMillan. Lazy abstraction with interpolants. In CAV, pages 123–136,
     2006.

[10] Matthew W. Moskewicz, Conor F. Madigan, Ying Zhao, Lintao Zhang, and Sharad
     Malik. Chaff: Engineering an efficient SAT solver. In Design Automation Confer-
     ence, DAC. ACM, 2001.




                                            16
[11] Armin Biere, Marijn Heule, Hans van Maaren, and Toby Walsh. Conflict-driven
     clause learning sat solvers. Handbook of Satisfiability, Frontiers in Artificial Intelli-
     gence and Applications, pages 131–153, 2009.

[12] Sébastien Bardin, Philippe Herrmann, and Florian Perroud. An alternative to sat-
     based approaches for bit-vectors. In Javier Esparza and Rupak Majumdar, editors,
     TACAS, pages 84–98, Berlin, Heidelberg, 2010. Springer Berlin Heidelberg. ISBN
     978-3-642-12002-2.

[13] Laurent D. Michel and Pascal Van Hentenryck. Constraint satisfaction over bit-
     vectors. In Michela Milano, editor, CP, Lecture Notes in Computer Science, pages
     527–543. Springer Berlin Heidelberg, 2012. ISBN 978-3-642-33557-0.

[14] Zakaria Chihani, Bruno Marre, François Bobot, and Sébastien Bardin. Sharpening
     constraint programming approaches for bit-vector theory. In CPAIOR, 2017.

[15] Wenxi Wang, Harald Søndergaard, and Peter J. Stuckey. A bit-vector solver with
     word-level propagation. In Claude-Guy Quimper, editor, CPAIOR, pages 374–391,
     Cham, 2016. Springer International Publishing. ISBN 978-3-319-33954-2.

[16] Scott Cotton. Natural domain smt: A preliminary assessment. In International Con-
     ference on Formal Modeling and Analysis of Timed Systems, pages 77–91. Springer,
     2010.

[17] Leonardo De Moura and Dejan Jovanović. A model-constructing satisfiability cal-
     culus. In International Workshop on Verification, Model Checking, and Abstract
     Interpretation, pages 1–12. Springer, 2013.

[18] Roberto Bruttomesso, Alessandro Cimatti, Anders Franzén, Alberto Griggio, Ziyad
     Hanna, Alexander Nadel, Amit Palti, and Roberto Sebastiani. A lazy and layered
     smt (\ mathcal {BV}) solver for hard industrial verification problems. In Interna-
     tional Conference on Computer Aided Verification, pages 547–560. Springer, 2007.

[19] Aleksandar Zeljić, Christoph M Wintersteiger, and Philipp Rümmer. Deciding bit-
     vector formulas with mcsat. In International Conference on Theory and Applications
     of Satisfiability Testing, pages 249–266. Springer, 2016.

[20] George Katsirelos and Fahiem Bacchus. Generalized nogoods in csps. In AAAI,
     volume 5, pages 390–396, 2005.

[21] Thibaut Feydy, Andreas Schutt, and Peter Stuckey. Semantic learning for lazy
     clause generation. In TRICS workshop, held alongside CP, 2013.

[22] Alan K Mackworth. Consistency in networks of relations. Artificial intelligence, 8
     (1):99–118, 1977.

[23] Patrick Prosser. Hybrid algorithms for the constraint satisfaction problem. Com-
     putational intelligence, 9(3):268–299, 1993.

                                             17
[24] Roberto J Bayardo Jr and Robert Schrag. Using csp look-back techniques to solve
     real-world sat instances. In AAAI/IAAI, pages 203–208, 1997.

[25] J. A. Robinson. A machine-oriented logic based on the resolution principle. JACM,
     12:23–41, January 1965.

[26] Olga Ohrimenko, Peter J. Stuckey, and Michael Codish. Propagation = Lazy
     Clause Generation, pages 544–558. Springer Berlin Heidelberg, Berlin, Heidel-
     berg, 2007. ISBN 978-3-540-74970-7. doi: 10.1007/978-3-540-74970-7 39. URL
     http://dx.doi.org/10.1007/978-3-540-74970-7_39.

[27] Rina Dechter. Enhancement schemes for constraint processing: Backjumping, learn-
     ing, and cutset decomposition. Artificial Intelligence, 41(3):273–312, 1990.

[28] Michael Veksler and Ofer Strichman. Learning general constraints in csp. Artificial
     Intelligence, 238:135–153, 2016.




                                          18
