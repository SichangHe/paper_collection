      Lazy Annotation for Program Testing and
                    Verification

                                  Kenneth L. McMillan

                                  Cadence Berkeley Labs



       Abstract. We describe an interpolant-based approach to test genera-
       tion and model checking for sequential programs. The method generates
       Floyd/Hoare style annotations of the program on demand, as a result of
       failure to achieve goals, in a manner analogous to conflict clause learning
       in a DPLL style SAT solver.


1    Introduction
The DPLL approach to Boolean satisﬁability combines search and deduction
in a mutually reinforcing way. It focuses deduction where the search becomes
blocked, deducing facts that guide the search away from the failure. Here, we
consider an approach to program testing and veriﬁcation inspired by DPLL. As
in DART [3], we use symbolic execution to search the space of execution paths.
When the search fails to reach a goal, we deduce a program annotation that will
prevent us from being blocked in the same way in the future. Since annotations
are deduced only in response to search failures, we will call this method lazy
annotation.
   The algorithm proceeds roughly as follows. We designate a set of program
locations as goals to be reached. In the following examples, the goals are calls to a
function error. The vertices (locations) and edges (statements) of the program’s
control ﬂow graph will be labeled with formulas. A label represents a condition
under which no goal can be reached. Initially, there are no labels (no annotation
being equivalent to false). We execute the program symbolically along some
chosen path. Each input to the program is represented by a symbolic value pi . In
the symbolic state, each program variable is evaluated as a symbolic expression
over these parameters. A constraint is also maintained, which accumulates the
conjunction of the branch guards along the chosen path, as a function of the
parameters.
   We say that our state is blocked if the current vertex label is implied, meaning
we cannot reach a goal from this state. When we are blocked, we will backtrack
along the edge we just executed, annotating it with a new label that blocks that
edge. When choosing a branch to execute, we are guided by these edge labels.
A blocked edge cannot lead to a goal, so we always continue along an unblocked
edge if there is one. When all outgoing edges are blocked in the current state,
we label the current location with the conjunction of the conditions that block
the outgoing edges, thus blocking the current state and causing us to backtrack.

T. Touili, B. Cook, and P. Jackson (Eds.): CAV 2010, LNCS 6174, pp. 104–118, 2010.

c Springer-Verlag Berlin Heidelberg 2010
                      Lazy Annotation for Program Testing and Verification     105

   As an example, consider the fragment simple in Figure 1. Suppose on entering
this code at l1 , our symbolic state is x = p0 with constraint T (true). Branching
from l1 to l2 , we obtain the constraint p0 = 0. At l2 we have the choice to branch
to l3 or l6 . Since neither edge is labeled, we choose arbitrarily l6 . Now there
is only one choice and we branch to l7 , obtaining the unsatisﬁable constraint
p0 = 0 ∧ p0 < 0. At this point we are blocked, since F (false) holds in the current
state and absence of annotation is equivalent to F .
   We therefore backtrack, annotating edge l6 → l7 . In general, if the current
annotation is φ, we can annotate the incoming edge with the weakest precondi-
tion of φ along that edge. In this case, the current annotation is φ = F and the
weakest precondition is x ≥ 0. After backtracking, we return to l6 . There is only
outgoing edge, labeled x ≥ 0. Therefore, we can label l6 : x ≥ 0. We are now
blocked (since x = 0 in our current state) so we backtrack to l2 , labeling edge
l2 → l6 : x ≥ 0 (again using the wp). Notice that each time we label an edge,
that edge becomes blocked in the current symbolic state (and possibly other
states).
   Since the edge l2 → l3 , is still unblocked, we follow it. Our annotation has
forced the search in a diﬀerent direction. Moving on to l4 , we have y = p1 (a new
input), then at l5 we have the constraint p1 ≥ 0 (corresponding to the guard
y ≥ 0). Finally we arrive at l6 in the state x = p0 +p1 with constraints p0 = 0 and
p1 ≥ 0. Since this implies the previous annotation l6 : x ≥ 0, we are blocked.
The fact we previously learned tells us there is no path to the goal from our
current state. Backtracking to l5 and taking the weakest precondition of x ≥ 0
then gives us l5 : x + y ≥ 0. When we backtrack to l4 , however, we observe a
slight problem. The weakest (liberal) precondition of x + y ≥ 0 with respect to
the assertion y ≥ 0 is y < 0∨x+y ≥ 0. However, the variable y is irrelevant here,
and we could just as well block the state with x ≥ 0 (also a precondition, not
the weakest). This latter fact can be computed as an interpolant as we will show
later. The advantage of the interpolant becomes clear in the next step when the
weakest precondition would yield l3 : ∀y. (y < 0∨x+y ≥ 0). We can simplify this
to x ≥ 0, but this requires quantiﬁer elimination, which can be very expensive.
By computing preconditions with interpolants, we avoid the need for quantiﬁer
elimination.
   Now we backtrack to l2 , labeling the edge (l2 → l3 ) with x ≥ 0. At this
point, both edges from l2 are blocked, so we label it with the conjunction of the
blocking labels along these edges, yielding l2 : x ≥ 0. Finally, we label l1 : T ,
proving that the goal error cannot be reached from l1 .
   Lazy annotation has the advantage that, like DPLL, it can recover from irrel-
evant or too-speciﬁc deductions. Consider, for example, fragment diamond, and
suppose we ﬁrst execute the path through l3 and l7 . After backtracking, we label
l6 → l7 : p. Then executing edge l6 → l9 we are blocked, because a = 1 in the
current state. Thus, rather than exploring this path and discovering it is also
safe because p holds, we label l6 → l9 with the irrelevant condition a, and thus
we label l6 : p ∧ a. However, when we return to l6 via l5 , note what happens. The
edge l6 → l7 is blocked by label p so we follow l6 → l9 , ultimately labeling it p
106      K.L. McMillan


                                   diamond:
                                   l1 assert(p);
      simple:                                                loop1:
                                   l2 if(*)
      l1 assume(x == 0);                                     l1 assert(x == y);
                                   l3     a = 1;
      l2 if(*){                                              l2 i = 0
                                       else
      l3     int y = *;                                      l3 while(i < n){
                                   l5     a = 0;
      l4     assume(y >= 0);                                 l4     x = x + 1;
                                   l6 if(a)
      l5     x = x + y;                                      l5     i = i + 1;
                                   l7     x = x + 1;
         }                                                   l6 }
                                   l8 else
      l6 if(x < 0)                                           l10 if(x < y)
                                   l9     x = x - 1;
      l7     error();                                        l11    error();
                                   l10 if(!p)
                                   l11    error();

                      int x;                        int x;

                      foo(){                        rec1(){
                 l1      x = x + 1;            l1      if(*){
                 l2          }
                         return;               l3          rec1();
                                               l4          rec1();
                 call1:                                }
                 l3 x = y;                     l5      x = x + 1;
                 l4 foo();                     l6      return;
                 l5 if(x < y)                       }
                 l6     error();

                         Fig. 1. Example program fragments

as well. Thus, we label l6 : p. Location l6 is now labeled by the disjunction of p
and p ∧ a. The stronger condition p ∧ a is eﬀectively subsumed, and we discard
it.
    Note how this diﬀers from partition reﬁnement approaches such as Synergy [5]
and its descendants [4]. In Synergy, after executing the path through l7 , loca-
tion l9 is on the frontier. This causes l6 to be partitioned by the irrelevant
predicate a. There is no way to recover from this irrelevant reﬁnement. With
sequences of such diamonds, we can construct reasonable scenarios in which this
leads Synergy to an exponential explosion of partitions, while lazy annotation is
polynomial.

Unbounded loops. Consider the simple unbounded loop in fragment loop1.
To force this loop to terminate, we will use a simple trick: we instrument the
program with a variable τ that decreases in every iteration, and we annotate all
locations with τ < 0, blocking any path in which τ becomes negative. We pick
an arbitrary initial value of τ , say, zero. This forces the loop to be executed at
most once. Say we execute ﬁrst the path that skips the loop. Using interpolants,
we label l3 → l10 : x ≥ y and backtrack into the loop. When the loop completes,
we decrement τ and are thus blocked by l3 : τ < 0. We thus backtrack through
the loop. Using interpolants, we obtain l3 → l4 : τ < 1. Thus, we label l3 : x ≥
y ∧ τ < 1. Backtracking further, we label l1 : τ < 1 and terminate. We have not
                      Lazy Annotation for Program Testing and Verification       107

proved unreachability of error, since our annotation depends on the bogus label
τ < 0. However, our annotation can be strengthened by induction. We simply
plug τ = 0 into our labels and see if they are inductive. We obtain l3 : x ≥ y
which is in fact inductive, so we keep it. We drop any non-inductive labels
iteratively, obtaining the greatest inductive subset as a ﬁxed point. Eﬀectively
we have used bounded model checking as a heuristic for constructing an inductive
invariant. Note that using weakest precondition, we would have obtained l3 : x ≥
0 ∨ i < n which is not inductive. To handle unbounded loops, we need some form
of generalization, here provided by interpolation. If strengthening by induction
fails to prove unreachability, we can increase the initial τ value and try again.

Procedure summaries. To handle programs with procedures modularly, we
label them with negative summaries. This is a formula that uses primed variables
to represent the exit state of the procedure, and is true when that exit state is not
reachable. For example, if on exit the value of x must be greater than its current
value, the negative summary would be x ≤ x. We can use lazy annotation to
compute a summary for a procedure from a given initial state, with a desired
post-condition ψ. This reusable summary can replace a call to the procedure in
various contexts. Consider fragment call1 in the ﬁgure. Here, we start at l3 in
state x = p0 , y = p1 . When we reach the call to foo at l4 , we recursively call
lazy annotation to compute a summary of foo that proves the current post-
condition of the call, which is l5 : F . Obviously, this cannot be proved, and we
obtain a counterexample, which is a path to the return state x = p1 + 1, y = p1 .
Continuing from l5 , we eventually label l5 : y ≤ x. Now when we backtrack to l4 ,
we recursively try to compute a summary of foo that proves the post-condition
y ≤ x. This time we succeed, computing the negative summary l1 : x < x as
an interpolant (see Section 2.3). Using this summary for l4 → l5 , we can label
l4 : x ≥ y and terminate. Moreover this same summary at l1 may be useful in
other contexts, allowing us to return immediately from foo.
   The advantage of using interpolants to compute summaries is that we can
obtain more general summaries. A method such as Smash [4] that uses weakest
precondition to compute a summary with the post-condition x ≥ y would yield
                            foo
a summary such as x ≥ y ⇒ x ≥ y containing the irrelevant variable y. To be
able to reuse this summary in another context, we need to be able to univer-
sally quantify over y, which again involves us in quantiﬁer elimination. Using
interpolants, this complication is avoided.

Recursion. Finally, consider the recursive function rec1 in the ﬁgure and sup-
pose we want to compute a summary for initial state x = 0 and post-condition
x ≥ 0. To force termination, we decrement τ on recursive calls, and initialize τ
to 1. Now suppose we ﬁrst take the path through l3 . Because τ is decremented,
the recursive calls at l3 and l4 must take the non-recursive path, yielding an
exit state x = 2. This satisﬁes the post-condition x ≥ 0, giving a negative
summary l5 : x < x. Backtracking to l4 , we again call recursively with a post-
condition equivalent to x ≥ 0 (for details, see Section 2.3) which yields a sum-
mary l1 : x < x ∧ τ < 1. The same summary is reused in backtracking to
108    K.L. McMillan

l3 , which eventually gives us l1 : x < x ∧ τ < 2. Setting τ = 0, we ﬁnd that
l1 : x < x is inductive and terminate.

Related work. Lazy annotation is similar to lazy abstraction with interpolants
[8] in that it computes an inductive invariant using only interpolation. Because
it explores only feasible paths, however, it is useful for testing, and can eﬃ-
ciently handle bounded loops. Moreover, it handles procedures modularly. It is
also similar in some respects to Synergy [5] and related methods [4] that use
partition reﬁnement. However, unlike these methods, it can recover from too-
speciﬁc reﬁnements. In fact, we can think of the annotation as partitioning each
location into exactly two state sets. Lazy annotation can also compute more
general summaries using interpolants.
    Relative to predicate abstraction approaches [1,9], lazy annotation has the
advantage that it avoids the expensive predicate image computation. However
it is in another sense orthogonal to these methods, as predicate abstraction can
be used to inductively strengthen the annotations obtained by lazy annotation,
possibly speeding convergence for unbounded loops, while avoiding the many
iterations produced by counter-example guided abstraction reﬁnement. In fact,
any backward abstract interpretation can be used for this purpose.


2     Lazy Annotation

Throughout this paper, we will use standard ﬁrst-order logic (FOL) and the
notation L(Σ) to denote the set of well-formed formulas (wﬀ ’s) of FOL over a
vocabulary Σ of uninterpreted symbols (the formulas may also include various
interpreted symbols, such as = and +). For a given formula φ, L(φ) will denote
the wﬀ ’s over the uninterpreted vocabulary of φ. We will write φ[σ] to indicate
that structure σ is a model of formula φ. To every uninterpreted symbol s, we
associate a unique symbol s (that is, s with one prime added). For any formula
or term φ or vocabulary S, we will write φ or S  for the result of adding one
prime to all the non-logical symbols in φ or S.
   Given a pair of FOL formulas (A, B), such that A ∧ B is inconsistent, an
interpolant for (A, B) is a formula Â such that A implies Â, Â implies ¬B, and
Â ∈ L(A) ∩ L(B). The Craig interpolation lemma [2] states that interpolants
always exist for inconsistent formulas in FOL. A variety of techniques exist for
deriving an interpolant for (A, B) from refutation of A ∧ B in a suitable proof
system [7]. This allows us to generate interpolants using a theorem prover or
proof-generating decision procedure.

Modeling programs. We assume a vocabulary S of variables representing the
program’s data state, a domain D of data values, and a collection of program
actions A provided by the programming language. A program is a ﬁnite, rooted,
labeled graph (Λ, l0 , Δ) where Λ is a ﬁnite set of program locations, l0 ∈ Λ is a
distinguished initial location and Δ ⊆ Λ × A × Λ is a set of transitions labeled
by actions. Let Out(l) denote the set of outgoing edges from location l.
                        Lazy Annotation for Program Testing and Verification           109

   A program path of length k is an alternating sequence of the form l0 a0 l1 a1 . . . lk ,
where each triple (li , ai , li+1 ) is in Δ. A data state in D is a map S → D. We ﬁx
an initial data state d0 . The semantics of an action a ∈ A, denoted Sem(a), is
subset of D × D. A program run of length k is a pair (π, σ), where π is a program
path, and σ = d0 · · · dk is a sequence of data states such that for all 0 ≤ i < k,
(di , di+1 ) ∈ Sem(ai ). A state is a pair (l, d) ∈ Λ × D. The reachable states are all
the pairs (lk , dk ) for some run of length k.
   A state formula is a formula in L(S). A transition formula is a formula in
L(S ∪ S  ). For action a and formulas φ, ψ (that may contain non-program vari-
ables) the Hoare triple {φ}a{ψ} is valid when for every data state d1 , and in-
terpretation I of the non-program variables, such that φ[d1 ∪ I] and every d2
such that (d1 , d2 ) ∈ Sem(a), we have ψ[d2 ∪ I]. We assume that Sem(a) can
be expressed as a transition formula, which by abuse of notation, we will write
Sem(a). Since actions and transition formulas are interchangeable, we will also
write {φ}t{ψ} where t is an arbitrary transition formula.
   It is useful to deﬁne a relational join operator for relations expressed as for-
mulas. Let φ and ψ be formulas, and f be an indexed set of variables with
a unique variable fv associated to each v ∈ S. Then φ ×f ψ is the formula
φ fv /v   ∧ ψ fv /v. If φ and ψ are transition formulas, we can think of this for-
mula as representing a succession of two transitions, the ﬁrst satisfying φ and
the second satisfying ψ, with f representing the intermediate state. If we omit
the subscript f , then the intention is that f is some set of variables not previ-
ously used. One important fact we will use is that {φ}t{ψ} is valid exactly when
φ ∧ (t × ¬ψ) is unsatisﬁable.

Symbolic Interpreters. A symbolic data state represents a set of data states
parametrically. The symbolic data states S consist of the triples (P, C, E), where
P is a set of parameters (variables not in S), C ∈ L(P ) is a constraint over the
parameters, and E is a map from the program variables S to functions over P .
We assume the these functions are expressible as ﬁrst order terms over P . Thus, a
symbolic state s can be characterized by the predicate χ(s) = C∧ v∈S v = E(v).
A symbolic data state s represents a set of data states γ(s) deﬁned as follows:

                            γ(s) = {d ∈ D | d |= ∃P. χ(s)}

This is the set of data states produced by the map E for some valuation of the
parameters satisfying the constraint C. We assume a deﬁned initial symbolic data
state so such that γ(s0 ) = {do }. A (full) symbolic state is a pair (l, s) ∈ Λ × S.
   A symbolic interpreter SI maps A to S × S. We require that SI(a) is total for
all actions a. Intuitively, a symbolic interpreter takes a symbolic state and an
action, and returns a non-empty set of symbolic states representing the eﬀect of
executing a. Symbolic interpreter SI is sound when, for all symbolic states s and
actions a,

                             ∪γ(SI(a)(s)) = Sem(a)(γ(s))
110     K.L. McMillan

That is, the symbolic successors of s must together represent exactly the suc-
cessors of the concrete states represented by s. Note that the set of states rep-
resented can be empty, since the constraint in a symbolic state can be F .
   Note that SI(a) may be a function (i.e., deterministic). In this case, non-
determinism in a is modeled by the introduction of parameters. On the other
hand, we may decide based on heuristic considerations to replace parameters
with concrete values, introducing non-determinism in SI(a). Injecting concrete
values in this way is analogous to decision making in DPLL. Soundness is not
sacriﬁced as long as SI is sound. As in DART, however, it is also possible to
substitute concrete values in an unsound way for operations which cannot be
modeled symbolically [3].

2.1   Intraprocedural Algorithm
We ﬁrst consider the case without procedure calls. We deﬁne a set of goals
G0 ⊂ Λ that we wish to reach. For each goal, we wish to ﬁnd a concrete run
reaching the goal, or a proof that it is unreachable. The state of the algorithm is
a triple (Q, A, G), where Q is a query set, A is a program annotation, and G ⊆ Λ
is the set of remaining goals. A query is a pair (s, ψ), where s is a symbolic state
called the initial state, and ψ is a formula called the post-condition of the query.
In the intraprocedural setting, the post-condition serves no purpose. It will be
used later when computing procedure summaries.
    An annotation is a set of pairs in (Λ ∪ Δ) × L(S). We will notate these pairs
in the form l : φ or e : φ, where l is a location, e an edge and φ a formula called
the label. The intended semantics is that no path beginning with location l or
edge e can reach any remaining goal if φ is initially true. We will write A(l) for
∨{φ | l : φ ∈ A}.
    For an edge e = (l1 , a, l2 ), we say that a label e : φ is justiﬁed in A when
{φ} a {A(l2 )}, that is, when it implies the annotation of l2 after executing a.
We notate this condition J (e : φ, A). For a location l, we will say that a label
l : φ is justiﬁed in A when, for all edges e ∈ Out(l), there exists e : ψ ∈ A such
that φ ⇒ ψ. An annotation is justiﬁed when all its elements are justiﬁed. A
justiﬁed annotation is inductive. If it is also initially true, then it is an inductive
invariant. Our algorithm maintains the invariant that A is always justiﬁed.
    We will say that a query q = ((l, s), ψ) is blocked by formula φ, when s |= φ
and write B(q, φ). With respect to q, the edge e is blocked when B(q, A(e)), and
the location l is blocked when B(q, A(l)).
    The algorithm IntraLA proceeds according to the transition rules deﬁned in
Figure 2. The initialization rule Init sets the algorithm state to Q = {((l0 , s0 ), ψ0 )},
A = A0 = ∅, G = G0 . That is, we are at the program’s initial state, with no loca-
tions labeled, and all goals yet to be reached. The decision rule Decide generates
a new query from an existing one by symbolically executing one program action. It
may choose any edge that is not blocked, and any symbolic successor state gener-
ated by the action a. If the newly generated query is itself not blocked, it is added
to the query set.
                      Lazy Annotation for Program Testing and Verification            111


                             Init
                                    {((l0 , s0 ), ψ0 }, A0 , G0


                                                      q = ((l1 , s1 ), ψ) ∈ Q
                                                      e = (l1 , a, l2 ) ∈ Δ
                             Q, A, G
             Decide                                   ¬B(q, A(e))
                      Q + ((l2 , s2 ), ψ), A, G
                                                      s2 ∈ SI(a)(s1 )
                                                      ¬B(((l2 , s2 ), ψ), A(l2 ))


                                                q = ((l, s), ψ) ∈ Q
                      Q, A, G                   ¬B(q, A(l))
       Conjoin
               Q − q, A + l : φ, G − l          ∀e ∈ Out(l), e : φe ∈ A ∧ B(q, φe )
                                                φ = ∧{φe | e ∈ Out(l)}


                                                   q = ((l1 , s1 ), ψ) ∈ Q
                           Q, A, G                 e = (l1 , a, l2 ) ∈ Δ
                  Learn
                        Q, A + e : φ, G            B(q, φ)
                                                   J (e : φ, A)

                            Fig. 2. Algorithm IntraLA

   If all of the outgoing edges of a query are blocked, the Conjoin rule is used
to block the query by labeling its location with the conjunction of the labels
that block the outgoing edges. At this point, we know that the symbolic state
is not empty (since otherwise the query would already be blocked). Thus, if the
location is a goal, we have reached the goal, and we remove it from the set of
remaining goals. The blocked query is discarded.
   The remaining case is that some outgoing edge e = (l1 , a, l2 ) is not blocked,
but every possible symbolic step along that edge leads to a blocked state. In this
case, the Learn rule infers a new label φ that blocks the edge. The new edge label
can be any formula φ that both blocks the current query and is justiﬁed. Such
a formula can be obtained as an interpolant for (A, B), where A = χ(s1 ) and
B = Sem(a) ∧ ¬A(l2 ) . Thus we can derive φ, if it exists, using an interpolating
theorem prover [7].
   The algorithm maintains the invariant that no queries are blocked, and, for
every l ∈ G, A(l) = F . It terminates when no rules can be applied, which implies
the query set is empty.

Theorem 1. When algorithm IntraLA terminates, all the locations in G0 \ G
are reachable and all the locations in G are unreachable.

Proof sketch. All the rules preserve the invariant that A is justiﬁed (therefore
inductive), that all the locations in G are unlabeled (meaning their annotation is
equivalent to F ) and that no queries are blocked. Now suppose the algorithm is
in a state where no rules can be applied and consider some q ∈ Q. Since Decide
does not apply, all possible successor queries are blocked. Thus, since Learn does
112     K.L. McMillan

not apply, all outgoing edges are blocked. Thus, since Conjoin does not apply,
q is blocked, a contradiction. Since Q is empty, it follows that the initial query
is blocked, meaning that d0 |= A(l0 ). Therefore, A is an inductive invariant.
Since all remaining goals are annotated F , it follows that they are unreachable.
Moreover, since goals are only removed from G when reached, all locations in
G0 \ G are reachable.                                                           2
Of course, we can also terminate the algorithm immediately if the set of remain-
ing goals becomes empty.

2.2   Handling Unbounded Executions
The approach described above has one clear drawback: if the program has any
loop that can execute unboundedly, then the algorithm will not terminate. That
is, for any learning to occur, we must ﬁrst reach a blocked state. However, if
there is an unbounded loop, we can keep extending the run inﬁnitely without
reaching a blocked state.
    To deal with this situation, we use the following generic approach. We intro-
duce an auxiliary variable τ to the program. This variable must be non-increasing
and inﬁnitely often decreasing according to some pre-order that is well-founded
over a domain characterized by some predicate W . For example, τ could be an
integer that is decremented by every program action and the domain predicate
could be τ >= 0. We can think of τ as the program’s “time to live”. Alterna-
tively, it would be suﬃcient to decrement τ on each back-edge of the program
graph, so that τ has to be decremented at least once on each cycle. Or, τ could
be a vector with one element for each SCC of the graph.
    Now ﬁx an initial value τ0 of τ , and label every location l with the predicate
¬W . With this construction, every inﬁnite run is eventually blocked. Thus, algo-
rithm IntraLA is guaranteed to terminate (at least if the symbolic interpreter
SI is ﬁnitely non-deterministic). When termination occurs, the annotation A is a
proof that the remaining goals cannot be reached for the particular initial value
τ0 . This is, in eﬀect, a form of bounded model checking.
    To obtain an unbounded proof, we can use the heuristic that bounded proofs
may contain the ingredients of unbounded proofs. To do this, we will eliminate
the dependence on τ in the annotation A, resulting in an unbounded annotation
AU . This can be done, for example by substituting some ﬁxed value ⊥ for τ ,
typically the bottom value of the pre-order.
    The unbounded annotation AU is not necessarily justiﬁed. However, we can
make it justiﬁed by iteratively dropping labels that are not justiﬁed until a ﬁxed
point is reached. The result is the greatest inductive subset of AU . This set of
unbounded facts can then be used to strengthen A. If the resulting annotation is
true in the initial state for all values of τ , then we have proved unreachability of
the remaining goals. Otherwise, we increase τ0 and repeat algorithm IntraLA.
This overall procedure is depicted in Figure 3.
    Because the problem of determining the reachable goals is undecidable, we
do not expect this algorithm to terminate in all cases. The hope is that the
                       Lazy Annotation for Program Testing and Verification       113


Algorithm Strengthen
Input: a query q and goal set G0
Output: set of unreachable goals

Q ← {q}, A ← ∅, G ← G0
while T do
     Run IntraLA on (q, A, G) to termination
     AU ← {l : φ⊥/τ | l : φ ∈ A}
     while exists l : φ ∈ AU s. t. ¬J (l : φ, A) do
           AU ← AU − l : φ
     done
     if B(q, AU (l0 )) return G
     A ← A ∪ AU
     increase τ0
done
                   Fig. 3. Algorithm with inductive strengthening

computed interpolants will converge to inductive assertions after a small number
of iterations of the loops, and thus τ0 will not become large. An alternative
inductive strengthening approach would be to apply predicate abstraction using
the atomic predicates occurring in AU . Though the cost would be higher, the
chance of convergence might be better.
    We must also take care to handle loops with large ﬁxed bounds eﬃciently. That
is, suppose we have a loop that iterates N times where N is a large ﬁxed number.
If we increment τ0 by one, then we may increment τ0 N times before exiting
the loop, resulting in O(N 2 ) decision steps. One simple way to prevent this
would be to double τ0 instead of incrementing it, which would give O(N log N )
steps. Alternatively, if we can determine statically that the loop is bounded,
we can simply remove the decrements of τ from the loop, without causing non-
termination of IntraLA.

2.3   Interprocedural Algorithm
To handle procedures in a modular fashion, we will annotate the program with
negative summaries. This is a transition formula φ with the intended meaning
that if φ[d0 , d1 ] holds, then entry to the procedure in data state d0 may not result
in exit in state d1 . Negative summaries are used because they are inductive in
the normal, forward sense.
   To detect goals reached within procedures, we designate a special variable f .
On reaching a goal, a procedure aborts, that is, it exits immediately with f true.
On normal exit, f is false. Given a negative summary φ, we can think of φ T /f  
as a pre-condition under which the procedure guarantees not to reach a goal and
abort.
Modeling Programs with Procedures. To model data in programs with
procedures we designate a set of global variables G and local variables L. For
i = 0, 1, . . . the frame Li consists of a variable vi for each v ∈ L. A frame
114     K.L. McMillan


Function Sum(q0 , A, G)

      Apply IntraLA from initial state ({q0 }, A, G) until
      1) there exists ((l, d), ψ) ∈ Q, where l ∈ Ω:
            in which case, return (d, A, G), or
      2) Q is empty:
            in which case, return (, A, G).

               Fig. 4. Algorithm for procedure summary construction

represents the local state of one procedure instance, with L0 representing the
current procedure instance.
   To model procedure calls, we introduce special actions call(l), where l is a
location of a procedure to be called. We introduce a set of procedure call edges Θ
that are distinct from the ordinary edges Δ. We also designate a set Ω ⊂ Λ of exit
states. Due to space considerations, we give the semantics of calls only informally.
The eﬀect of an edge (l1 , call(l2 ), l3 ) is to transfer control to l2 , execute until
reaching an exit state, then return by transferring control to l3 . The eﬀect of a
call action on the data state is to “push” one frame on the “stack”. We deﬁne an
operation push on data states that shifts the local variables up by one frame, so
that push(d)(vi+1 ) = d(vi ). On return, one stack frame is “popped”. We deﬁne
pop(d) so that pop(d)(vi ) = d(vi+1 ). We also deﬁne corresponding renaming
operators on formulas, so that push(φ) = φ Li+1 /Li  and pop(φ) = φ Li−1 /Li .
Computing summaries. We will say a query q = ((l, s), ψ) is blocked by a
negative summary φ, that is, B(q, φ), when every exit allowed by φ satisﬁes the
post-condition ψ. Because summaries are negative, this is equivalent to saying
that {χ(s)} ¬φ {ψ} or that the formula χ(s) ∧ (¬φ × ¬ψ) is unsatisﬁable.
   Justiﬁcation of ordinary edges and locations remains as before. Now, however,
we say that φ is justiﬁed at an exit state l when φ = ¬IS ∨ f  , where IS is
the identity relation over the data variables S. In other words, exiting from
a procedure leaves the data unchanged, and does not abort. We will consider
justiﬁcation of call edges shortly.
   Using algorithm IntraLA, we can deﬁne a function Sum (see Figure 4) that
constructs a negative summary for a procedure. It takes a query ((l1 , d1 ), ψ) and
returns either a reachable exit state d2 that does not satisfy the post-condition ψ
(i.e. a counterexample to the query) or it labels l1 with a summary that ensures
that no such counterexample exists.
Using procedure summaries. We use procedure summaries to justify the
annotation of call edges. Intuitively, a summary φ is justiﬁed at a call edge
e = (l1 , call(l2 ), l3 ) if it is justiﬁed by considering the summary of the called pro-
cedure l2 as an action. There are two subtleties involved in this, however. The
ﬁrst is that we must account for the shift in stack frames between the calling and
called contexts. We can do this by applying the push operator to the formulas
in the calling context. The second is that the calling context must abort if the
called context aborts. We can eﬀect this by weakening the summary at the return
                           Lazy Annotation for Program Testing and Verification               115

location. We deﬁne W(φ) = φ∧¬(f ∧f  ). In eﬀect, this removes transitions from
the negative summary at the return site, allowing the calling context to abort
when the called function does. Using this notion, the justiﬁcation condition for
procedure calls is deﬁned as follows:

       J ((l1 , call(l2 ), l3 ) : φ, A)   iﬀ {push(φ)} ¬A(l2 ) {push(W(A(l3 ))}

We can then prove the following lemma:

Lemma 1. If negative summary annotation A is justiﬁed, and if d0 |= A(l0 )
T /f   and if A(l) = F for some location l, then location l is unreachable.

Proof sketch. By induction on the length of runs, we show that if the initial state
(l0 , d0 ) of a run satisﬁes A(l0 ) T /f   then every state (li , di ) satisﬁes A(li ) T /f  .
This property is preserved by call actions because we have weakened the sum-
mary at the return site, so that the caller aborts when the callee aborts. As a
result, no reachable state can be labeled F .                                                  2
Now we are ready to deﬁne versions of the Decide and Learn rules for call
edges. These are shown in Figure 5. In both cases, we have an outgoing call
edge e from the current query. We compute a post-condition ψ2 for the called
function based on the current summary of the return site and the post-condition
of the calling context. Notice we use the weakened summary to allow the called
function to abort. Also notice that we apply push to the current state when
entering the called function. If Sum returns an exit state, then the return site
is not blocked, and DecideC generates a new query after the call (note pop is
applied to this state). On the other hand, if Sum returns , then we are blocked.
Thus LearnC can annotate the edge with a blocking formula φ.
   A suitable condition φ that is both blocking and justiﬁed can be obtained
as an interpolant for (A, B), where A = χ(s1 ) ∧ ¬ψ1 and B = ¬pop(A(l2 )) ×
¬W(A(l3 )). That is, the transition formulas implied by A are exactly the negative
summaries blocking the query q (note s1 is the symbolic state of q and ψ1 is the
post-condition of q). The transition formulas inconsistent with B are exactly
those justiﬁed at the call edge. Moreover, an interpolant for (A, B) must be a
transition formula, since only variables in S ∪ S  can be common to A and B.
Thus, any interpolant for (A, B) satisﬁes the conditions for the annotation φ of
the call edge.
   We will call the algorithm IntraLA with the addition of these two rules
InterLA. The initial annotation A0 consists of the labels r : ¬IS ∨ f  , for
all the exit locations r ∈ Ω. The initial post-condition ψ0 = ¬f . Essentially,
this constructs a summary that proves that the program does not abort. This
procedure is recursive. When it encounters a call edge, it calls Sum with a suitable
query. This in turn runs InterLA on the called procedure. The recursive call
can result in the addition of labels, and the elimination of reachable goals.

Theorem 2. When algorithm InterLA terminates, all the locations in G0 \ G
are reachable and all the locations in G are unreachable.
116     K.L. McMillan


                             Q, A, G                  (s3 , A3 , G3 ) = Sum(q2 , A, G)
      DecideC
                Q + ((l3 , pop(s3 )), ψ1 ), A3 , G3   ¬B(q, A(e))


                                              (, A3 , G3 ) = Sum(q2 , A, G)
                           Q, A, G
               LearnC                         B(q, φ)
                        Q, A + e : φ, G
                                              J (e : φ, A3 )

                                 ⎧
                                 ⎪
                                 ⎪ q = ((l1 , s1 ), ψ1 ) ∈ Q
                                 ⎨
                                   e = (l1 , call(l2 ), l3 ) ∈ Θ
                           where
                                 ⎪
                                 ⎪ ψ2 = ¬W(A(l3 )) × ψ1
                                 ⎩
                                   q2 = ((l2 , push(s1 ), ψ2 )

                Fig. 5. Rules for InterLA (in addition to IntraLA)

Proof sketch. As in the intraprocedural case, all the rules preserve the invariant
that A is justiﬁed and that the locations in G are unlabeled. When the initial
query ((l0 , s0 ), ¬f ) is blocked, we know that d0 |= A(l0 ) T /f   therefore by the
lemma, all unlabeled locations are unreachable.                                      2

3     Implementation and Experiments
Algorithm InterLA has been implemented in a tool we will call Impact II.
This tool uses the LLVM compiler infrastructure [6] to generate CFG’s from C
programs, with basic blocks corresponding to edges of the graph. The tool uses
the FOCI interpolating prover [7] both for checking satisﬁability of formulas
and computing interpolants. The C heap is modeled using the theory of arrays.
Static analysis is used to partition loads and stores into alias classes, with each
alias class modeled by an array. External functions are modeled as having no
side eﬀects and returning a non-deterministic value, which can be considered an
input to the program.
   When a goal location is reached, Impact II extracts a satisfying assignment
to the symbolic constraint C of the symbolic state as a test case. By initially
marking every location as a goal, we can generate a set of tests that provides
100% coverage of reachable locations, and prove that the uncovered locations
are unreachable (since the compiler inlines small functions, some goals may be
duplicated).
   Experiments were conducted to test the hypothesis that this approach can
produce a greater diversity of program behavior more quickly than methods
such as DART that enumerate all execution paths. We used as benchmarks sev-
eral device driver examples previously used as software model checking bench-
marks [8]. We compare InterLA against an implementation of DART using
the same symbolic interpreter and prover. This allows us to gauge the eﬀect of
learned annotations in guiding the search. Without learning, we simply enumer-
ate all possible control paths. DART terminates in these tests because all the
loops are bounded and there is no recursion.
                        Lazy Annotation for Program Testing and Verification           117



                learn                                            no learn
                                                            learn   no learn   ratio
                                               saturation   87      1290       15

                           driver: kbfiltr     completion   94      1811       19




              learn
                                                                 no learn
                                                            learn   no learn   ratio
                                               saturation   214     7552       35

                         driver: diskperf      completion   221     15148      69




                learn                                            no learn
                                                            learn   no learn   ratio
                                               saturation   327     13827      42

                          driver: floppy       completion   330     27788      84




           Fig. 6. Comparison of test generation with and without learning

   Figure 6 plots the number of coverage goals reached as a function of the num-
ber of times the symbolic interpreter backtracked to an alternative program branch
(which is also the number of test sequences generated). Three examples1 are shown,
with the number of reachable basic blocks ranging from 104 to 279. Each plot
shows a line for InterLA (“learn”) and a line for DART (“no learn”). The tables
compare the number of backtracks needed for saturation (all reachable locations
reached) and completion. Without learning, there are long plateaus during which
many paths are explored but no new locations are reached. Learning clearly acts
to push the search away from these regions, allowing the search to make steady
progress. This eﬀect is more pronounced in the larger program, with learning re-
ducing backtracks to completion by a factor 84.


4     Conclusion
Lazy annotation allows us to deduce program annotations in response to search
failure, much in the way that a DPLL SAT solver learns conﬂict clauses. As we
1
    Source code available at http://www.kenmcmil.com/benchmarks.html
118     K.L. McMillan

have seen, this allows us to prune the search in test generation to achieve a given
coverage goal at a greatly reduced cost. The method also has some potential ad-
vantages with respect to existing software model checking techniques. Since it
is based entirely on interpolants, it avoids the expense of quantiﬁer elimination
or predicate image computations. The annotation approach avoids irreversible
partitioning of the abstract state space, and potentially allows more general pro-
cedure summaries. Compared to lazy abstraction with interpolants, the method
allows procedure summarization (thus may be more eﬀective for deeply nested
procedures) and handles bounded loops more eﬀectively. In the other hand, it
may be that the lazy abstraction approach of exploring infeasible program paths
produces interpolants that are more relevant to the property being checked.
Moreover, the question of how to obtain convergence in practice for unbounded
loops needs further study.


References
1. Ball, T., Rajamani, S.K.: The SLAM project: Debugging system software via static
   analysis. In: POPL, pp. 1–3 (2002)
2. Craig, W.: Three uses of the Herbrand-Gentzen theorem in relating model theory
   and proof theory. J. Symbolic Logic 22(3), 269–285 (1957)
3. Godefroid, P., Klarlund, N., Sen, K.: DART: directed automated random testing.
   In: PLDI, pp. 213–223 (2005)
4. Godefroid, P., Nori, A.V., Rajamani, S.K., Tetali, S.D.: Compositional may-must
   program analysis: Unleashing the power of alternation. In: POPL, pp. 43–56 (2010)
5. Gulavani, B., Henzinger, T.A., Kannan, Y., Nori, A., Rajamani, S.K.: Synergy: A
   new algorithm for property checking. In: Robshaw, M.J.B. (ed.) FSE 2006. LNCS,
   vol. 4047, pp. 117–127. Springer, Heidelberg (2006)
6. Lattner, C., Adve, V.: LLVM: A compilation framework for lifelong program analysis
   & transformation. In: CGO, pp. 75–88 (2004)
7. McMillan, K.L.: An interpolating theorem prover. Theor. Comput. Sci. 345(1),
   101–121 (2005)
8. McMillan, K.L.: Lazy abstraction with interpolants. In: Ball, T., Jones, R.B. (eds.)
   CAV 2006. LNCS, vol. 4144, pp. 123–136. Springer, Heidelberg (2006)
9. Majumdar, R., Henzinger, T.A., Jhala, R., Sutre, G.: Lazy abstraction. In: POPL,
   pp. 58–70 (2002)
