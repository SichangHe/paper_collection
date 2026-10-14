            Incremental Forward Reasoning for
                 White-Box Proof Search

                     Xavier Généreux        and Jannis Limperg

            Ludwig-Maximilians-Universität München, Munich, Germany
                   {xavier.genereux,jannis.limperg}@lmu.de



      Abstract Several proof assistants provide automation tactics based on
      tableau-style tree search, such as Isabelle’s and Rocq’s auto and Lean’s
      Aesop. In this setting we consider forward rules, which apply a given
      theorem, say, A → B → C, to any goal containing hypotheses A and
      B, adding C as a new hypothesis. When treated naively, such rules are
      tried on every goal encountered during the search, leading to repeated
      unifications of premises A and B with the hypotheses of each goal. We
      present an approach to forward rules that avoids some of this repeated
      work by taking advantage of similarities between successive goals. For
      each goal, we cache partial applications of forward rules in a custom data
      structure that enables efficient updates. Our technique is compatible with
      any search strategy and most logics. It has been implemented in Aesop.

      Keywords: Forward Reasoning · Forward Chaining · Tactics · Interact-
      ive Theorem Proving


1   Introduction
In many proof assistants, simple “white-box” proof automation tactics based
on tableau-style tree search play a substantial role in practice: Isabelle’s [15]
and Rocq’s [18] auto [14], ACL2’s ‘waterfall’ [7,8], various PVS [2,13] tactics,
Lean’s [12] Aesop [9], etc. These tactics operate on goals Γ ⊢ A, where the
context Γ is a list of hypotheses and A is the proposition to be proved. Faced with
an initial goal, the tactics try various user-specified r ules, w hich c orrespond to
admissible inferences in the prover’s logic. A successful rule reduces the current
goal to zero or more subgoals, which are solved recursively until either a full
proof is found or no rule applies to any open goal or the search times out. A
typical rule is the ∧-introduction lemma A → B → A ∧ B, which, when applied
backwards, reduces a goal Γ ⊢ A ∧ B to subgoals Γ ⊢ A and Γ ⊢ B.
   In addition to such backwards rules, most search tactics can also use arbitrary
tactics as rules. For example, Aesop uses the cases tactic on disjunctive hypo-
theses, splitting goals of the form Γ, h : A ∨ B ⊢ C into subgoals Γ, h : A ⊢ C
and Γ, h : B ⊢ C. Tactics implement arbitrary inferences; in particular, they can
remove any hypothesis and add any provable proposition as a new hypothesis.
   ACL2, PVS and Aesop additionally provide special support for forward reas-
oning, also known as forward chaining, in the form of forward rules. Given, for

© The Author(s) 2026
S. Junges and G. Katz (Eds.): TACAS 2026, LNCS 16505, pp. 276–294, 2026.
https://doi.org/10.1007/978-3-032-22752-2_14
              Incremental Forward Reasoning for White-Box Proof Search          277

example, the transitivity lemma ∀ x y z, x < y → y < z → x < z, a forward
rule run on the goal h1 : a < b, h2 : b < c ⊢ A produces the single subgoal
h1 : a < b, h2 : b < c, h3 : a < c ⊢ A. Hence, forward rules can be used to
establish additional facts that may be relevant for other rules. For example, the
Aeneas project [6] uses a mechanism similar to Aesop’s forward rules to establish
facts that are later used by an arithmetic decision procedure.
    Until recently, Aesop used what we call the naive algorithm to apply forward
rules. When a forward rule was run on a goal, the rule would search the goal’s
context for all combinations of hypotheses satisfying its premises. This method
is simple but involves much repeated work because in practice, contexts en-
countered during the search tend to be similar. For example, the ∧-introduction
rule, when run on Γ ⊢ A ∧ B, produces subgoals Γ ⊢ A and Γ ⊢ B, so the naive
algorithm runs the same forward rules on the same context Γ three times. More
generally, any backwards rule leaves the context unchanged, and many rules that
alter the context do so only in limited ways.
    In this paper, we present an alternative way to apply forward rules that
addresses this issue. The central idea is to remember, for each goal Γ ⊢ A, which
forward rules can be partially applied to which sets of hypotheses. When a non-
forward rule then generates subgoals ∆1 ⊢ A1 , . . . , ∆n ⊢ An , the new contexts
∆i are likely similar to Γ . Hence, it is generally cheaper (and often much cheaper)
to start with the partial matches for Γ and update them for each of the ∆i . The
update first deletes partial matches that include hypotheses no longer present
in ∆i . Afterwards it adds new partial matches for the hypotheses that are new
in ∆i , extending the existing partial matches for a rule if the new hypothesis
is compatible with them. Whenever this process produces a full match—i.e., all
premises of a forward rule are satisfied by a set of hypothesis in ∆i —the rule is
applied and adds a corresponding new hypothesis to ∆i .
    Our main contribution is a data structure, the forward state, that organises
the partial matches so that updates can be done efficiently. In addition to this
incrementality, the forward state satisfies two other desiderata:

 – It is persistent, i.e. forward states for parent and child goals share much of
   their structure. This is desirable since Aesop supports search strategies other
   than depth-first search and must therefore keep all goals encountered during
   the search, along with their forward states, in memory.
 – It reduces the number of unifications performed when matching hypotheses
   against rule premises. In dependent type theory, unification happens up to
   definitional equality, which makes it expensive. We therefore want to avoid
   redundant unifications.

    Our evaluation (Sec. 6) shows that this new implementation of forward reas-
oning in Aesop substantially outperforms the previous, naive implementation
on synthetic benchmarks involving heavy use of forward rules. On a natural
benchmark involving primarily light use of forward rules, we still obtain mod-
est speedups. Both implementations are available in recent versions of Aesop;
benchmarks and evaluation data are available in the artifact.
278     X. Généreux and J. Limperg

2     Preliminaries
We first introduce some terminology for matches and for forward rules (which
we identify with their underlying lemmas). We use dependent type theory as a
foundation, but our technique generalises to other logics.
    Given a lemma ∀ (x1 : A1 ) . . . (xn : An ), B, the xi are premises and B is
the lemma’s conclusion. The type Ai of the ith premise may depend on (i.e.,
refer to) any premise xj with j < i. Implication A → B is an abbreviation for
∀ x : A, B where B does not depend on x. Propositions are (certain) types, and
we do not distinguish between the two concepts.
    Using somewhat non-standard terminology, we call premises on which a later
premise depends variables. These are usually terms of non-propositional types,
e.g. natural numbers or lists. The non-variable premises, whose types are typ-
ically propositions, are called slots. For example, the lemma ∀ (x y z : N), x <
y → y < z → x < z has variables x, y, z and slots of types x < y and y < z.
If more than two premises depend on a variable (e.g. y), the variable is shared.
Note that premises on which only the conclusion depends are not considered
variables.
    If a lemma has n slots, each slot is assigned a unique number between 1 and
n, and we identify slots with their numbers. For now, we assume that the slots
are numbered consecutively, so in the example above slot 1 has type x < y and
slot 2 has type y < z. The shared variables of slot i, svars(i), are those variables
that appear in the type of i and also in at least one type of a slot j < i.
    If h : C is a hypothesis and C matches the type A of slot i, we say that
h matches i. Matching induces a substitution σ such that A[σ] is definitionally
equal to C; we define subi (h) := σ. What ‘matching’ means is explained in Sec. 5.
    A match m for a given rule r with n slots is a list containing between one and
n hypotheses. We interpret m as a partial map from slots of r to hypotheses, so
dom(m) = {i | 1 ≤ i ≤ |m|} and for each slot i ∈ dom(m), m(i) is the hypothesis
assigned to i. A match m must additionally satisfy the following requirements:
 1. For each slot i ∈ dom(m), the hypothesis m(i) matches i.
 2. For all slots i, j ∈ dom(m), the substitutions subi (m(i)) and subj (m(j)) are
    compatible. This means that the substitutions agree on all common vari-
    ables, i.e. for each variable x ∈ dom(subi (m(i))) ∩ dom(subj (m(j))) we have
    subi (m(i))(x) = subj (m(j))(x).
The substitution of a match m, sub(m), is the union of the substitutions induced
by the hypotheses in m, i.e. sub(m) := i∈dom(m) subi (m(i)). This is well-defined
by requirement 2. The level of a match m, lvl(m), is the length of m. A match
for rule r is complete if i ∈ dom(m) for every slot i of r, and partial otherwise.
    A partial match m for rule r corresponds to a partial application of the rule
to the terms given in sub(m). The application is type-correct by requirements 1
and 2. If m is complete, then sub(m) contains a term for every slot and every
variable—hence for every premise—of r, and we have a full application.
    Note that matches represent only those partial applications where arguments
are added without gaps. Hence, for a rule r : A → B → C, the applications
              Incremental Forward Reasoning for White-Box Proof Search            279

r a _ : B → C and r a b : C for some a : A and b : B correspond to matches,
but not r _ b : A → C. This prevents us from constructing r a b in two different
but ultimately redundant ways.


3    Naive Forward Reasoning

Before this work, Aesop used what we call naive forward reasoning [9]. This
approach treats forward rules like any other Aesop rule. Hence, when Aesop
selects a forward rule r with n slots of types A1 , . . . , An as the highest-priority
rule currently applicable to a goal Γ ⊢ T , we look for all complete matches for
r in Γ , using an approach reminiscent of backtracking subsumption algorithms.
    More specifically, we first match the type of the last slot, An , with each
hypothesis h : B (using an imperfect discrimination tree [11] index to quickly
determine potentially matching hypotheses). If successful, this results in a sub-
stitution σ1 containing all variables that occur in An . We then match An−1 [σ1 ]
against the type of each hypothesis in the context, yielding a substitution σ2 ,
and proceed with An−2 [σ2 ], etc., until we obtain a complete match for r. If a
premise An−i [σi ] does not match any hypothesis type, we backtrack and consider
other potential matching hypotheses for An−i+1 . These may lead to a different
substitution τ and therefore to different matching hypotheses for An−i [τ ]. For
each complete match m with substitution σ found during this process, we add
a new hypothesis of type C[σ], where C is the conclusion of r.
    This approach is efficient when the last slot of a rule does not match any
hypothesis in the context since the rule is then usually excluded by indexing
and never run. Otherwise, we match large numbers of premises and hypotheses
against each other, though this process could likely be sped up heuristically [17].
Moreover, the whole process is repeated when we proceed to another goal with
a similar context. In particular, the contexts of subgoals produced by whatever
rule is eventually applied to the current goal are likely to be similar to the current
context, but the naive algorithm does not exploit these similarities.


4    Incremental Forward Reasoning

With the weaknesses of the naive approach in mind, we introduce an incremental,
stateful solution to the problem of finding complete matches. The main idea is
to store, for each goal Γ ⊢ A, the partial matches implied by the hypotheses
in Γ , and to reuse these partial matches for subgoals ∆ ⊢ B. This rests on the
assumption that ∆ is likely similar to Γ in practice, and that it is therefore
cheaper to update the partial matches for Γ than to compute those of ∆ from
scratch. Our main contribution is a data structure, the forward state, that allows
us to perform these updates efficiently.

Forward States. We associate with each goal in Aesop’s search tree a forward
state that reflects the goal’s context. Let S be the set of forward states, H the
280     X. Généreux and J. Limperg

set of hypotheses, R the set of rules, C the set of complete matches and P(X)
the powerset of X. The forward state’s interface then consists of two functions

          addHyp : S → H → S × P(R × C)             delHyp : S → H → S

The addHyp function adds a hypothesis to the forward state. Hence, if s is the
forward state corresponding to context Γ and addHyp(s, h : T ) = (s′ , C), then
s′ is the forward state corresponding to Γ, h : T . Similarly, if s is the forward
state corresponding to Γ, h : T , then delHyp(s, h : T ) is the forward state
corresponding to Γ . The second output of addHyp, C , is a set of pairs (r, m)
where r is a rule and m is a complete match for r. These are the matches that
were completed by adding h : T .
    When Aesop is run on an initial goal with context h1 : T1 , . . . , hn : Tn , the
forward state for it is built by starting with an empty state and applying addHyp
to each hypothesis hi . Afterwards, whenever an Aesop rule is run on a goal with
context Γ , producing subgoals with contexts ∆1 , . . . , ∆n , we derive the forward
state for each subgoal context ∆j from the forward state for Γ , in two steps:

 1. Apply delHyp once for each hypothesis that was deleted, i.e. that appears
    in Γ but not in ∆j .
 2. Apply addHyp once for each hypothesis that was added, i.e. that appears in
    ∆j but not in Γ .

Changes to a hypothesis (e.g. a change of its type) are treated as a deletion
followed by an addition.

Rule States. Partial matches are specific to each rule, so the forward state
naturally decomposes into a set of rule states, one per rule. Given a goal Γ ⊢ A
and a rule r, the rule state for r contains exactly the partial matches of r in
context Γ . A rule state supports addHyp and delHyp methods analogous to
those on forward states. Adding a hypothesis to a forward state then amounts to
adding it to each rule state (which may yield new complete matches for the rule);
deleting a hypothesis amounts to deleting it from each rule state. We initially
focus on how to add hypotheses, since this question motivates much of the design
of the rule state data structure.
    When a hypothesis is added to a rule state, two things can happen. First, the
hypothesis may allow us to extend partial matches already present in the state.
For instance, consider the rule r : ∀ x, P x → Q x → R x → S x and a rule
state containing the partial match [h1 ], which assigns some hypothesis h1 : P a
to the first slot of type P x. Adding a new hypothesis h2 : Q a to this rule state
means that we should add to the state the extended match [h1 , h2 ].
    Second, adding a match may trigger the insertion of further matches. Suppose
that before adding h1 and h2 , we had already added a hypothesis h0 : R a to
the rule state. Once the partial match [h1 , h2 ] arrives, we should recognise that
it can be extended with h0 to obtain the (complete) match [h1 , h2 , h0 ].
               Incremental Forward Reasoning for White-Box Proof Search             281

Variable Indices. Extending the matches above was possible only because all
hypotheses are compatible on the shared variable x, i.e. they all instantiate x
with the same term a. In general, to extend a match m with a hypothesis h : T
at slot i, we need to ensure that the substitution of m, sub(m), is compatible
with the substitution of h, subi (h).
    The rule state therefore uses two variable indices H and M to index hypo-
theses and matches by their instantiations for shared variables, allowing us to
quickly determine compatible pairs of matches and hypotheses. We could use a
substitution tree [5], but our custom data structure is simpler. The hypothesis
index H maps each triple (x, i, t) (where i > 1 is a slot, x ∈ svars(i) a variable
and t a term) to a set containing hypotheses h added to the rule state such that h
matches i and subi (h)(x) = t. In other words, H indexes the known hypotheses
by the slots they match and the instantiations of shared variables. Note that
hypotheses matching slot 1 are not stored since they can never extend a match.
    Similarly, the match index M maps each triple (x, i, t) to a set containing
partial matches m (that can be derived from the hypotheses added to the rule
state) such that i = lvl(m), x ∈ svars(i + 1) and sub(m)(x) = t. Matches for
the maximal slot are not stored because, being complete, they never need to be
extended. We write Mx (i, t) instead of M (x, i, t) and Hx (i, t) instead of H(x, i, t).
    Given a hypothesis h : T that matches slot i > 1 with substitution σ =
subi (h), the partial matches that can be extended by h are those at level i − 1
whose substitutions are compatible with σ on the variables svars(i) (i.e., the
variables shared between i and any earlier slot). Assuming for the moment that
svars(i) is non-empty for all slots i > 1, these matches are

                                           Mx (i − 1, σ(x))
                              x∈svars(i)

Similarly, given a partial match m at level i with substitution σ = sub(m), the
hypotheses that could extend m are

                                            Hx (i + 1, σ(x))
                             x∈svars(i+1)

The number of shared variables tends to be small in practice, so these intersec-
tions can be computed efficiently.
    From here we can directly derive two procedures for adding hypotheses and
matches to the rule state. The procedures maintain the invariants of the variable
indices while reporting any complete matches discovered during this process.
Specifically, if a rule state for a rule r corresponds to the context Γ —i.e., it
contains the hypotheses of Γ and all partial matches of r that can be derived
from them—then the rule state obtained from addHyp(h : T ) corresponds to
Γ, h : T .
    The rule state’s addHyp method (Algorithm 1) adds a hypothesis h : T
matching slot i to the rule state. (If a hypothesis matches multiple slots, addHyp
is called multiple times.) For i = 1, we add the singleton match [h] to the rule
state. For i > 1, we first insert h into the hypothesis index H . Then we query
 282    X. Généreux and J. Limperg

   Input : A hypothesis h : T
   Output : All complete matches of r in context Γ, h : T that contain h
   Procedure addHyp(h : T )
      completeMs ← ∅
      for all slots i of r such that h matches i do
          if i = 1 then
               completeMs ← completeMs ∪ addMatch([h])
          else
               let σ := subi (h)
               for x in svars(i) do
                   Insert h into the set Hx (i, σ(x))
               let ms := x∈svars(i) Mx (i − 1, σ(x))
               for m in ms do
                   completeMs ← completeMs ∪ addMatch(m ++ [h])
      return completeMs
 Algorithm 1: Add a hypothesis to the rule state for a rule r and context Γ


the match index M for matches that can be extended by h and add the extended
matches to the rule state. While adding matches, we may discover new complete
matches, which are collected and returned.


   Input : A partial match m of r at level i with substitution σ
   Output : A set of complete matches of r
   Procedure addMatch(m)
      if m is complete then
          return {m}
      else
          let σ := sub(m)
          for x in svars(i + 1) do
              Insert m into the set Mx (i, σ(x))
          let hs := x∈svars(i+1) Hx (i + 1, σ(x))
          completeMs ← ∅
          for h in hs do
              completeMs ← completeMs ∪ addMatch(m ++ [h])
          return completeMs
         Algorithm 2: Add a match to the rule state for a rule r


   The rule state’s addMatch method (Algorithm 2) adds a match m with level
i = lvl(m) to the rule state. If m is already complete, it is returned. Otherwise,
m is inserted into M and we query H for hypotheses that can extend m. Any
extended matches thus produced are added to the rule state recursively.

Variable Clusters. We have so far only considered rules where for each slot
i > 1, the set of shared variables svars(i) is non-empty, i.e. each slot shares at
               Incremental Forward Reasoning for White-Box Proof Search                 283

least one variable with at least one of the previous slots. However, there are also
rules such as ∀ x y, P x → Q y → R x y, where slot 2 (Q y) shares no variables
with slot 1 (P x). In this case, any match at level 1 can be extended with any
hypothesis at level 2, since the two slots are independent.
    To account for this fact, we partition the set of premises of each rule into max-
imal subsets of premises connected by shared variables, called variable clusters,
using the same construction as Aesop’s metavariable clusters [9]. The variable
clusters share no variables with each other, so each can be treated as a separate
rule with its own rule state. Finding a complete match for a rule then amounts
to finding one complete match for each of its clusters. The slots within each
cluster can be ordered to ensure that each slot shares at least one variable with
the previous slots.

Deletion. When a hypothesis h is removed from a goal’s context, we must
update the forward state accordingly. This means deleting h from any rule state
to which it was previously added, i.e. from any rule state for a rule r with a
slot i matching h. To facilitate deletion, we cache this information when h is
added to the rule state. When h is deleted, we can then efficiently determine the
relevant rule states and delete h from the hypothesis index H at slot i and from
the match index M at all slots j ≥ i.

Example 1. As a first example, consider a rule state for the transitivity rule
r1 : ∀ x y z, x ≤ y → y ≤ z → x ≤ z to which we add, in order, the hypotheses
h1 : b ≤ c and h2 : a ≤ b. The rule has two slots of types x ≤ y and y ≤ z which
share the variable y.
     The hypothesis h1 : b ≤ c unifies with both slots, so we execute the outer
loop of Algorithm 1 twice. For slot 1, unification yields the substitution {x →
b, y → c}. Since this is the first slot, Algorithm 2 inserts the new partial match
[h1 ] into the set My (1, c). This match cannot be extended since the hypothesis
index H does not contain a hypothesis for slot 2.
     For slot 2, unification yields the substitution σ := {y → b, z → c}, so we
insert h1 into Hy (2, b). No matches at level 1 can be extended by h1 since

                                    Mx (1, σ(x)) = My (1, b) = ∅
                       x∈svars(2)

At this point, H and M are in state (1), shown below.


              2               1                         2                       1
(1)   Hy :    b      My :     c         (2) Hy :    b       a      My :     c       b
             {h1 }          {[h1 ]}                {h1 } {h2 }            {[h1 ]} {[h2 ]}

   Now we add h2 : a ≤ b, which again unifies with both slots. For slot 1,
sub1 (h2 )(y) = b, so we add the match [h2 ] to My (1, b). We then check for hypo-
theses in slot 2 that also instantiate y with b, and indeed we find Hy (2, b) = {h1 }.
284     X. Généreux and J. Limperg

Hence, we return the complete match [h2 , h1 ], which induces h3 : a ≤ c to be
added later. For slot 2, we add h2 to Hy (2, a). There are no compatible matches
at level 1, so we are done with h2 , yielding the final rule state (2).

Example 2. We now consider a rule r2 : ∀ x y, A x y → B x y → C x y
with multiple shared variables. We add hypotheses h1 : B a a, h2 : A a b and
h3 : B a b to the rule state of r2 , starting with h1 , which is added to H with
slot 2. There are no matches yet, so there is nothing to extend. We then add
h2 : A a b, which initially generates a match m = [h2 ] that is added to M ,
yielding the following rule state:

                 2                      2                      1                  1
       Hx :      a              Hy :    a            Mx :      a         My :     b
               {h1 }                   {h1 }                {[h2 ]}             {[h2 ]}

   To find hypotheses compatible with m, we consider the set of variables
svars(lvl(m) + 1). These are the variables shared between slot lvl(m) + 1 = 2
and all previous slots, i.e. x and y. Hence, the compatible hypotheses are

                             Hx (lvl(m) + 1, sub(m)(x)) = Hx (2, a) ∩ Hy (2, b) = ∅
      x∈svars(lvl(m)+1)


This means the match cannot currently be extended. We now turn to h3 : B a b,
adding it first to H. This yields the following rule state:

                 2                          2                      1                  1
      Hx :       a              Hy :    a       b       Mx :       a      My :        b
             {h1 , h3 }                {h1 } {h3 }             {[h2 ]}           {[h2 ]}

Since h3 matches slot i = 2, the matches that can be extended by h3 are

                           Mx (i − 1, subi (x)) = Mx (1, a) ∩ My (1, b) = {[h2 ]}
              x∈svars(i)


This produces the complete match [h2 , h3 ], so we can add a new hypothesis of
type C a b.


5     Implementation

Implementing the preceding technique efficiently requires some care, particularly
in the context of dependent type theory.
              Incremental Forward Reasoning for White-Box Proof Search          285

Matching. In type theory, types contain programs and matching (or, more
generally, unification) is expected to respect definitional equality, i.e. equality
up to evaluation. For instance, a theorem with premise P 2, where P is some
predicate, should apply to a hypothesis of type P ((λ x. x) 2) since the two
types are definitionally equal. As a result, matching premises and hypotheses is
arbitrarily expensive in theory and a major cost centre in practice. We therefore
seek to avoid redundant invocations of the matching procedure.
    To limit the cost of matching, we match with reducible transparency. Lean
has multiple transparency levels that determine which constants are unfolded.
‘Reducible’ is the most restrictive of these, so we unfold few (and, in practice,
only non-recursive) definitions. Additionally, we use Lean’s usual approximation
of higher-order matching, which is complete for first-order matching problems
and heuristically solves some higher-order problems. Either of these limitations
render forward reasoning incomplete, but since the same matching algorithm is
used throughout Lean, users are used to this source of incompleteness.


Variable Index Implementation The hypothesis index H and the match
index M of a rule state have the same domain and are combined into one map.
This map, whose domain is a set of triples (x, i, t), is represented by three nested
maps. The first two of these, whose keys are variable names x and slot indices
i, are persistent hash maps. The third map, called the instantiation map, whose
keys are instantiation expressions t, is implemented as a persistent array storing
pairs (t, d), where t is the instantiation and d is the associated data.
    Keys of the instantiation map are identified up to definitional equality at re-
ducible transparency. This means that insertions and lookups involve one defin-
itional equality check for each element of the map, which is fairly expensive. To
reduce the number of such checks, we add an imperfect discrimination tree index
that allows us to efficiently determine which keys of the map may match a given
expression.


Match Equivalence. Naively, two matches would be considered equal if they
contain the same hypotheses. However, consider the rule r : ∀ x y, P x y →
Q x z → R x and the hypotheses h1 : P a b, h2 : P a c, h3 : Q a d and
h4 : Q a e. The complete matches m1 := [h1 , h3 ] and m′1 := [h1 , h4 ] contain
different hypotheses, but the difference does not matter because the applications
r h1 h3 and r h1 h4 both have type R a. Generating both m1 and m′1 would
therefore be redundant. Similarly, the partial matches m2 := [h1 ] and m′2 := [h2 ]
are redundant because the choice between h1 and h2 affects neither the type of
any eventual application derived from m2 and m′2 nor the hypotheses that can
be used to complete them. Hence, we should store only one of m2 and m′2 in the
rule state of r. Based on these observations, we consider two matches m and m′
of a rule r equal if lvl(m) = lvl(m′ ) and for each premise x that appears either
in the conclusion of r or in the type of a slot i of r with i > lvl(m) we have
sub(m)(x) = sub(m′ )(x).
286     X. Généreux and J. Limperg

Redundant Hypotheses. When we find a complete match, we add a new
hypothesis of the corresponding type T to the goal, but only if there is no other
hypothesis of type T already present. To determine this, we iterate through the
hypotheses, comparing their types to T up to definitional equality. While this
can be expensive, the local context is generally small and definitional equality
comparisons are cached globally.
    Beyond preventing redundant hypotheses, this check also allows us to sim-
plify the implementation of match equality. When determining whether matches
are redundant, we do not use definitional equality but compare expressions struc-
turally (i.e., up to α-equivalence). As a result, we may fail to identify redundant
matches, but these are detected once we check whether the hypotheses generated
by them are already present.

Lazy Insertion. Adding a hypothesis to a rule state is cheap, but not free: it
involves one unification for each slot that the hypothesis may match, according
to a discrimination tree index, followed by several operations on the variable
indices. We therefore delay insertions in two ways. First, we observe that com-
plete matches can only be generated once all slots have been filled. Therefore,
hypotheses are matched against slots and inserted into the variable indices only
once we have found a potentially matching hypothesis for each slot. Second, we
observe that the variable indices are only queried for hypotheses at a slot i > 1
when a match is added at slot i − 1. Hence, we delay the insertion of hypotheses
at i until there is at least one match in slot i − 1.

Phased Insertion We delay insertions further by taking advantage of Aesop’s
partitioning of rules into several phases. When Aesop tries to solve a goal, it
first normalises it, using only rules tagged with the normalisation phase. Then
it tries to apply rules from the safe phase, and only when all of them fail does
it consider rules from the unsafe phase.
    This means that we can delay updates to the rule states of normalisation rules
until we start working on the goal; updates to safe rules until normalisation is
finished; and updates to unsafe rules until we have applied all the safe rules.
Sometimes, this allows us to avoid expensive operations, e.g. when a goal is
solved only by safe rules and no unsafe rules need to be considered at all. At
other times, we can skip specific updates, for example when a hypothesis is added
by a normalisation rule but then immediately removed by another normalisation
rule. Phased insertion skips any updates to safe and unsafe rules resulting from
the transient hypothesis.
    To implement this optimisation, we split insertion into two operations. When
a hypothesis is added, it is initially just enqueued in per-slot queues of rule states
for which it may be relevant. (The same queues are also used to implement lazy
insertion.) Then, once we need to determine which rules of a given phase apply
to the goal, we move the hypotheses from the slot queues into the variable indices
and construct matches, including, perhaps, complete matches that allow us to
apply the rules.
              Incremental Forward Reasoning for White-Box Proof Search      287

6   Evaluation
There are unfortunately no standard benchmarks for Aesop-like tactics, and
forward rules are currently little used by Aesop’s main client, the Mathlib lib-
rary [19]. We therefore use two complementary evaluation schemes. First, we
compare our technique against the previous, naive Aesop implementation on
synthetic benchmarks that highlight its advantages and disadvantages. Second,
we compare the two implementations on the benchmark used by lean-auto [16],
which runs Aesop on all human-written Mathlib theorems with simulated per-
fect premise selection. The results shown below were obtained on an m8g.metal-
48xlarge AWS instance equipped with 192 Graviton4 processors and 768 GB of
RAM.


                                           naive
                                        incremental
                                 213
                    Time in ms




                                 29



                                 25



                                 21
                                   20         21           22      23
                                            Number of hypotheses


       Figure 1: Transitivity benchmark for a = 0 ( ) and a = 100 ( )



Synthetic Benchmarks. For each benchmark, we set up certain forward rules
and a goal with hand-picked hypotheses. We then run the saturate tactic,
which uses either naive or incremental forward reasoning to exhaustively apply
the forward rules. Performing only forward reasoning is the best-case scenario
for the incremental algorithm since previous results can be fully reused. When
forward reasoning is combined with other rules, we would expect smaller gains,
depending on how much reuse the non-forward rules allow.
    Instead of the natural numbers from Lean’s standard library, which are rep-
resented by arbitrary-precision integers, we use a custom type of Peano naturals
for the benchmarks. Matching two concrete Peano natural numbers n and m
involves comparing min(n, m) constructors. We can therefore use moderately
large numbers to simulate the bigger matching problems that Aesop encounters,
for example, in Mathlib’s category theory development. All results are averaged
over 10 runs per benchmark.

Transitivity Benchmark. Our first benchmark is a scaled-up variant of the trans-
itivity example from Sec. 4. Given some relation ≺ on natural numbers, we re-
288                     X. Généreux and J. Limperg

gister the lemma ∀ x y, x ≺ y → y ≺ z → x ≺ z as the sole forward rule and set
up a goal with hypotheses h1 : a ≺ a + 1, . . . , hn : a + n − 1 ≺ a + n, where either
a = 0 (yielding easy unification problems) or a = 100. Saturating this goal adds
n(n − 1)/2 hypotheses to the context.


              210                                                     210
                                                                                     naive
              29                                                      29          incremental

              28                                                      28
 Time in ms




                                                         Time in ms
              27                                                      27

              26                                                      26

              25                                                      25

              24                                                      24

              23                                                      23
                    1         2        3      4      5                      1        2            3     4   5
                                     Depth                                                      Depth

                        (a) Without precompilation                              (b) With precompilation

Figure 2: Results of the depth benchmark for n = 6 with precompilation disabled
(a) or enabled (b) and with a = 0 ( ) or a = 100 ( ).


    In Fig. 1 the incremental algorithm has a sizeable advantage over the naive
algorithm. We use a logarithmic scale, with each dotted horizontal line represent-
ing a 16-fold increase. Hence, for 23 = 8 hypotheses and a = 0, the incremental
implementation is over 30 times faster than the naive one. The speedup for
a = 100 is around 35x, with naive forward reasoning taking over 19 seconds.
    These results are largely explained by the number of times either algorithm
matches a premise against a hypothesis. The naive algorithm iterates over the
context, which initially contains n hypotheses, and compares all hypotheses pair-
wise. This is repeated approximately for each of the n(n − 1)/2 added hypo-
theses, so O(n4 ) match operations are performed. By contrast, the incremental
algorithm considers each hypothesis only once, matching it against both slots
and then comparing it with at most n other hypotheses. It therefore performs
only O(n2 ) match operations.
    Both algorithms generate all possible transitivity chains. If only the longest
such chain, from a to a+n, is desired, the rule can be registered as a destruct rule,
a special sort of forward rule that removes from the context any hypotheses it is
applied to. The incremental algorithm then needs only O(n) match operations.

Depth Benchmark. Our second benchmark concerns situations where many rules
match almost, but not quite. We use 100 copies of a rule r : ∀ x, P1 x →
. . . → Pn x → A, where the predicates Pi are all distinct and A is an arbitrary
proposition. Given a depth k ≤ n, the initial goal contains hypotheses of types
               Incremental Forward Reasoning for White-Box Proof Search        289

Pi a for each i ̸= n − k with 1 ≤ i ≤ n, as well as one hypothesis Pn−k (a + 1)
(with a = 0 or a = 100). In other words, the hypotheses match all premises
with compatible substitutions, except the kth premise from the back. Since the
naive algorithm processes the premises from back to front, k determines how
many premises the algorithm matches before it notices that the rule cannot be
applied. The incremental algorithm would do constant work per hypothesis if
not for the lazy insertion optimization, which—combined with a heuristic that
reorders slots so later premises come first—has a similar effect.
    This setup is challenging for the incremental algorithm because no rule is ever
applied, so incrementality does not help. And indeed, Fig. 2a shows that while
both approaches slow down for greater k (only slightly as the context contains
only n = 6 hypotheses), the incremental approach remains slower.
    Fig. 2b shows the results of the depth benchmark with precompilation en-
abled. This is a feature of Lean that compiles tactics ahead of time instead of
interpreting them. Both implementations benefit from this, but incremental for-
ward reasoning does so disproportionately, perhaps because it uses more custom
code that, unlike Lean’s built-in routines, is usually interpreted. However, pre-
compilation also substantially increases Aesop’s build time, so it is disabled by
default.

Mathlib Benchmark. We now use the benchmark introduced by lean-auto [16]
to evaluate our forward reasoning technique on 263412 theorems from Mathlib
(version 4.27.0-rc1), in two different configurations. In each configuration, the
constants that appear in Mathlib’s proof of the respective theorem are added as
forward rules, simulating perfect premise selection.
    In the Aesop configuration, Aesop, using naive or incremental forward reas-
oning, is run on each theorem. An invocation is successful if Aesop proves the
theorem. Constants from the theorem’s Mathlib proof are added as unsafe for-
ward rules, so they receive a relatively low priority and their application can be
backtracked. This configuration yields better results in practice than marking
the rules as safe—even though forward rules are conceptually always safe—since
it prevents Aesop from applying forward rules in an infinite loop.
    In the saturate configuration, the saturate tactic with naive or incremental
forward reasoning is run on each theorem. An invocation is successful if saturate
generates a hypothesis that matches the theorem statement. The maximum
depth of saturate is set to 10 to prevent infinite loops.
    In either configuration, constants are not added as forward rules if they are
private or typeclass instances, or if their types contain only logical symbols. In
the Aesop configuration, we also exclude equations used by the simplifier, which
Aesop already uses during its search. We use a timeout of 10 s for each tactic
invocation, and 1.5 h for each Mathlib module. The module timeout affects 176
modules (out of 7452) where, due to unknown issues, the tactic timeout is not
effective.
    Each tactic is run three times, and we exclude samples where the minimal
and maximal runtime differ by more than 20%. Furthermore, when comparing
performance, we only consider theorems where both the naive and the incre-
   290                                     X. Généreux and J. Limperg

    mental tactic variant succeed. This reduces the likelihood that differences are
    caused by minor, unintentional changes in behaviour. If the latter restriction is
    removed, incremental forward reasoning produces an even larger average speedup
    over naive forward reasoning than that reported below. After these exclusions,
    the evaluation comprises 53524 Aesop samples and 16452 saturate samples.
        Aesop is not expected to perform well on this benchmark since it is designed
    for carefully curated rulesets in which constants are appropriately registered
    as backward, forward or other types of rules. Nevertheless, the results may be
    indicative of Aesop’s performance on real use cases involving forward rules.


                                Configuration            Solved Mean       p1                       p10             p25      p50        p75      p90         p99
                                Aesop naive               55870 146.37 6.70 8.98 11.97 24.05 67.71 235.69 2652.54
                                Aesop incr.               55394 118.25 6.98 9.29 12.34 25.07 67.96 206.76 1784.33
                                Aesop speedup                    1.24x 0.96x 0.97x 0.97x 0.96x 1.00x 1.14x 1.49x
                                Saturate naive   17346 71.59 0.91 2.64 4.03 7.69 21.80 76.33 1576.46
                                Saturate incr.   16995 34.35 0.64 2.22 3.24 6.15 14.38 43.36 523.06
                                Saturate speedup       2.08x 1.42x 1.19x 1.24x 1.25x 1.52x 1.76x 3.01x
    Table 1: Number of problems solved, average elapsed time (in ms) and elapsed
    time percentiles for the Aesop and saturate configuration with naive and incre-
    mental forward reasoning. Each speedup is the ratio of naive and incremental
    time at the respective location of the distribution.




                              104          Parity                                                             104         Parity
Incremental Total Time (ms)




                                                                                Incremental Total Time (ms)




                              103                                                                             103


                                                                                                              102
                              102

                                                                                                              101
                              101

                                                                                                              100
                              100
                                    100        101       102        103   104                                       100            101       102       103         104
                                                 Naive Total Time (ms)                                                              Naive Total Time (ms)
                                          (a) Aesop configuration                                                   (b) Saturate configuration

    Figure 3: Elapsed time (log scale) per problem with naive and incremental for-
    ward reasoning. Points below the parity line indicate a speedup.
                                              Incremental Forward Reasoning for White-Box Proof Search   291




                                              n=28711
                                              n=10403
                                       1.15




                                              n=6937
                                              n=2414
                                              n=610
                                              n=238
       Speedup (Naive / Incremental)




                                              n=76
                                              n=28
                                              n=23
                                              n=14




                                                                                                 n=53
                                              n=2




                                                                                          n=1
                                       1.10
                                       1.05
                                       1.00
                                       0.95
                                       0.90
                                              0       5       10        15         20       25    30
                                                           Maximum Goal Depth (Incremental)

Figure 4: Aesop speedup by maximum goal depth. Problems solved by Aesop are
grouped by the maximum depth of any goal in the Aesop search tree. For each
depth, n is the number of problems with that maximum depth, and a violin plot
shows the distribution of speedups. The whisker indicates the median speedup.
We apply the interquartile range method with factor 3 to exclude outliers.




Results. As shown in Table 1, incremental forward reasoning improves the av-
erage performance of both Aesop and saturate. For saturate, we obtain a
substantial mean speedup of 2.08x, with incremental forward reasoning out-
performing the naive approach at each location of the time distribution. For
Aesop, the mean speedup is a more modest 1.24x, and we see slight slowdowns
at the lower percentiles, meaning Aesop calls that were already fast become a bit
slower. However, we also obtain substantial speedups on problems where Aesop
was previously slow, compensating for the slowdowns. Fig. 3 shows a more de-
tailed comparison of running times. Naive and incremental forward reasoning
are almost exactly semantically equivalent, so they are expected to solve almost
exactly the same number of problems.
    A possible explanation for the modest gains in the Aesop configuration is that
the vast majority of solved problems require very few rule applications, so the
maximum depth of goals in Aesop’s search tree is low. As a result, incrementality,
which reuses partial matches from parent goals for child goals, does not help
much. Fig. 4 shows that with larger maximum depths, we obtain larger speedups
(except at Aesop’s depth limit of 30; these invocations likely involve looping
rules). Combined with our synthetic benchmarks, this indicates that we would see
larger gains from incremental forward reasoning with larger-scale Aesop searches.


7   Related Work

White-Box Tactics. Among white-box proof automation tactics, to our know-
ledge only ACL2’s ‘waterfall’ [7,8] and PVS’s various proof search strategies [13,2]
292     X. Généreux and J. Limperg

have special support for forward reasoning. Both use approaches similar to
Aesop’s naive algorithm; in particular, the context of each goal is saturated inde-
pendently. ACL2 additionally allows forward rules to be annotated with trigger
terms, which cause the rules to be run if the trigger terms are matched anywhere
in a goal. Aesop implements a similar mechanism, rule patterns, not described
here due to space constraints. The auto2 tactic [21] employs an SMT-like search
procedure based on forward reasoning and e-matching [3]. As such, it does not
require incrementality, but it could perhaps benefit from our indexing schemes.

SATCHMO. The SATCHMO first-order theorem prover [10] uses a search
procedure that treats a given set of implications as forward rules and uses a case-
splitting rule to perform case analysis on disjunctive hypotheses. SATCHMO-
style provers may benefit from our incremental approach if the set of implications
is large. However, since unification is comparatively cheap in first-order logic, it
is not clear what effect it will have. SATCHMO also employs an optimisation
that “focuses” forward reasoning on the hypothesis established by the last case
split, providing a different form of incrementality.

Knowledge-Based Systems. Some knowledge-based reasoning systems, e.g.
Algernon [1] and EYE [20], support combined forward and backward reasoning.
However, to our knowledge, no such system allows non-forward rules to change
the assumptions available to forward rules, so they do not require incrementality.
Nevertheless, our technique bears some resemblance to the RETE algorithm [4]
for forward reasoning in large knowledge bases.


8     Conclusion
We have presented a technique that integrates forward reasoning into a tree-
based proof search procedure supporting arbitrary proof rules. We avoid re-
dundant reasoning steps by caching partial forward rule applications in a data
structure, the forward state, that enables efficient updates. The technique is in-
dependent of the search strategy and logic used. Our evaluation shows that the
technique outperforms Aesop’s previous implementation on both a synthetic and
a natural benchmark.
    One obvious extension of our method would be to exploit redundancy not
just between contexts of parent and child goals, but also between those of siblings
or even unrelated goals. This would require no changes to the forward state data
structure; we would only need to find pairs of goals that produce small diffs.

Acknowledgements. We thank Jasmin Blanchette, Massin Guerdi and the
anonymous reviewers for their very insightful comments on drafts of this paper.
Généreux’s research was co-funded by the European Union (ERC, 101083038)
and by the Fonds de recherche du Québec, 330205. Views and opinions expressed
are however those of the authors only and do not necessarily reflect those of the
European Union or the European Research Council. Neither the European Union
nor the granting authority can be held responsible for them.
                Incremental Forward Reasoning for White-Box Proof Search            293

Data Availability Statement

The data and software necessary to reproduce our results are available in an
artifact at DOI 10.5281/zenodo.18188520. For the purpose of reuse, the artifact’s
source code is available at https://github.com/JLimperg/artifact-aesop-forward,
and Aesop’s at https://github.com/leanprover-community/aesop. Aesop’s main
branch contains the naive and incremental implementations of forward reasoning.


References
 1. Crawford, J.M., Kuipers, B.J.: Algernon—a tractable system for knowledge-
    representation. SIGART Bull. 2(3), 35–44 (1991). https://doi.org/10.1145/122296.
    122302
 2. Crow, J., Owre, S., Rushby, J., Shankar, N., Srivas, M.: A tutorial introduction to
    PVS. In: Workshop on Industrial-Strength Formal Specification Techniques (1995),
    http://www.csl.sri.com/papers/wift-tutorial/
 3. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: A theorem prover for program check-
    ing. J. ACM 52(3), 365–473 (2005). https://doi.org/10.1145/1066100.1066102
 4. Forgy, C.L.: RETE: A fast algorithm for the many pattern/many object pat-
    tern match problem. In: Mylopolous, J., Brodie, M. (eds.) Readings in Artifi-
    cial Intelligence and Databases, pp. 547–559. Morgan Kaufmann (1989). https:
    //doi.org/10.1016/B978-0-934613-53-8.50041-8
 5. Graf, P.: Substitution tree indexing. In: Rewriting Techniques and Applications
    (1995). https://doi.org/10.1007/3-540-59200-8_52
 6. Ho, S., Protzenko, J.: Aeneas: Rust verification by functional translation. In: ICFP
    (2022). https://doi.org/10.1145/3547647
 7. Kaufmann, M., Strother Moore, J.: ACL2: An industrial strength version of Nqthm.
    In: COMPASS (1996). https://doi.org/10.1109/CMPASS.1996.507872
 8. Kaufmann, M., Manolios, P., Strother Moore, J.: Computer-Aided Reasoning: An
    Approach. Springer (2000)
 9. Limperg, J., From, A.H.: Aesop: White-box best-first proof search for Lean. In:
    CPP (2023). https://doi.org/10.1145/3573105.3575671
10. Manthey, R., Bry, F.: SATCHMO: A theorem prover implemented in Prolog. In:
    CADE (1988). https://doi.org/10.1007/BFb0012847
11. McCune, W.: Experiments with discrimination-tree indexing and path indexing
    for term retrieval. Journal of Automated Reasoning 9(2), 147–167 (1992). https:
    //doi.org/10.1007/BF00245458
12. de Moura, L., Ullrich, S.: The Lean 4 theorem prover and programming language.
    In: CADE (2021). https://doi.org/10.1007/978-3-030-79876-5_37
13. Owre, S., Rushby, J.M., Shankar, N.: PVS: A prototype verification system. In:
    CADE (1992). https://doi.org/10.1007/3-540-55602-8_217
14. Paulson, L.C.: Generic automatic proof tools. Tech. Rep. UCAM-CL-TR-396, Uni-
    versity of Cambridge (1996). https://doi.org/10.48456/tr-396
15. Paulson, L.C., Nipkow, T., Wenzel, M.: From LCF to Isabelle/HOL. Formal As-
    pects of Computing 31(6) (2019). https://doi.org/10.1007/s00165-019-00492-1
16. Qian, Y., Clune, J., Barrett, C.: Lean-Auto: An Interface Between Lean 4 and
    Automated Theorem Provers, pp. 175–196 (07 2025). https://doi.org/10.1007/
    978-3-031-98682-6_10
294     X. Généreux and J. Limperg

17. Tammet, T.: Towards efficient subsumption. In: CADE (1998). https://doi.org/10.
    1007/BFb0054276
18. The Coq development team: The Coq proof assistant (2024). https://doi.org/10.
    5281/zenodo.1003420
19. The Mathlib community: The Lean mathematical library. In: CPP (2020). https:
    //doi.org/10.1145/3372885.3373824
20. Verborgh, R., De Roo, J.: Drawing conclusions from linked data on the web: The
    EYE reasoner. IEEE Software 32(3), 23–27 (2015). https://doi.org/10.1109/MS.
    2015.63
21. Zhan, B.: AUTO2, a saturation-based heuristic prover for higher-order logic. In:
    ITP (2016). https://doi.org/10.1007/978-3-319-43144-4_27




Open Access. This chapter is licensed under the terms of the Creative Com-
mons Attribution-NonCommercial-NoDerivatives 4.0 International License (http://
creativecommons.org/licenses/by-nc-nd/4.0/), which permits any noncommercial use,
sharing, distribution and reproduction in any medium or format, as long as you give
appropriate credit to the original author(s) and the source, provide a link to the
Creative Commons license and indicate if you modified the licensed material. You do
not have permission under this license to share adapted material derived from this
chapter or parts of it.
   The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
