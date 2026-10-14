                                                          Size Relationships in
                                                   Abstract Cyclic Entailment Systems
arXiv:1702.03981v1 [cs.LO] 13 Feb 2017




                                                                       Reuben N. S. Rowe
                                                                  School of Computing
                                                           University of Kent, Canterbury, UK
                                                                r.n.s.rowe@kent.ac.uk

                                                                       James Brotherston
                                                                Dept. of Computer Science
                                                               University College London, UK
                                                                J.Brotherston@ucl.ac.uk
                                                                          February 2017


                                                                              Abstract
                                                  A cyclic proof system generalises the standard notion of a proof as
                                              a finite tree of locally sound inferences by allowing proof objects to be
                                              potentially infinite. Regular infinite proofs can be finitely represented as
                                              graphs. To preclude spurious cyclic reasoning, cyclic proof systems come
                                              equipped with a well-founded notion of ‘size’ for the models that interpret
                                              their logical statements. A global soundness condition on proof objects,
                                              stated in terms of this notion of ‘size’, ensures that any non-well-founded
                                              paths in the proof object can be disregarded.
                                                  We give an abstract definition of a subclass of such cyclic proof sys-
                                              tems: cyclic entailment systems. In this setting, we consider the prob-
                                              lem of comparing the size of a model when interpreted in relation to the
                                              antecedent of an entailment, with that when interpreted in relation to
                                              the consequent. Specifically, we give a further condition on proof objects
                                              which ensures that models of a given entailment are always ‘smaller’ when
                                              interpreted with respect to the consequent than when interpreted with re-
                                              spect to the antecedent. Knowledge of such relationships is useful in a
                                              program verification setting.

                                             We consider the following abstract formulation of sequent-style proof systems
                                         for entailments between antecedents and consequents.
                                         Definition 1 (Abstract Entailment Proof Systems). Let A and C be sets of
                                         antecedents and consequents, respectively. The set S of sequents is then the
                                         cartesian product A × C. We will write sequents (A, C) as A ⊢ C. A rule


                                                                                   1
(schema) R ⊆ S × S N is a set of rule instances. Rule instances (S, ǫ) are called
axiomatic. R = ℘(S × S N ) is the set of all rules, which we may assume to be
indexed by some set R. An entailment proof system is a tuple (S, r), where
r ⊆ R identifies the rule schemas of the proof system.
    Here, we use bold-font vector notation for sequences, writing si for the ith
element of s, ǫ for the empty sequence, s1 · s2 for sequence concatenation,
and |s| for the number of elements in s. We also write si..j to indicate that
s = si , . . . , sj and we sometimes abuse notation by using s to refer to the set of
elements occurring in s.
    A notion of cyclic proof (as found, e.g., in [2, 3, 4]) can also be formulated
in this abstract framework as follows.
Definition 2 (Cyclic Pre-proofs). A (cyclic) pre-proof P in an entailment proof
system (S, r) is a (finite) directed graph in which the children of each node
ν ∈ nodes(P) are ordered. A node represents a rule instance via the functions
seq : nodes(P) → S and rule : nodes(P) → R, which satisfy rule(ν) ∈ r and
(seq(ν), (seq(ν1 ), . . . , seq(νn ))) ∈ Rrule(ν) for each node ν ∈ nodes(P) with chil-
dren ν1 , . . . , νn . In an abuse of notation, we may use ν to refer to the rule
instance it corresponds to. A path in P is a (possibly infinite) sequence of nodes
ν of P such that ν i is the parent of ν i+1 for each non-terminal node ν i in the
path. We say that a path is rooted at its first node.
   The semantics of such proof systems can be given by satisfaction relations
between elements of the proof system (i.e. antecedents and consequents) and
any appropriate notion of ‘model’.
Definition 3 (Semantics). We fix a set M of models and assume two satisfac-
tion relations, |=A ⊆ M×A and |=C ⊆ M×C, writing m |=A A (resp. m |=C C)
to mean (m, A) ∈ |=A (resp. (m, C) ∈ |=C ) for m ∈ M, A ∈ A, and C ∈ C. We
also write m |= (A ⊢ C) to mean that m |=A A ⇒ m |=C C holds. Thus, when
we write m 6|= (A ⊢ C) we mean that m |=A A but m 6|=C C. We say that a
sequent A ⊢ C is consistent if there exists a model m |=A A, and inconsistent
otherwise.
   The definition of validity for sequents in our abstract framework is the stan-
dard one.
Definition 4 (Validity). We say that a sequent A ⊢ C is valid if and only if
m |= (A ⊢ C) for all models m ∈ M. Alternatively, writing M(A) and M(C)
for the set of models m such that m |=A A and m |=C C, respectively, we may
define A ⊢ C to be valid if and only if M(A) ⊆ M(C).
    The minimum that we require of any proof system is that its proof rules are
(locally) sound. The notion of local soundness has a uniform definition in terms
of validity.
Definition 5 (Local Soundness). We say that a rule instance (S, (S1 , . . . , Sn ))
is locally sound if and only if whenever each Si is valid then S is also valid. We
say that a rule R is locally sound when all of its instances (S, S) ∈ R are.

                                          2
    Local soundness of the proof rules is not sufficient to ensure the soundness of
cyclic proof systems however. For this, we must also require that cyclic proofs
satisfy a certain global soundness property. In our general abstract framework,
this can be defined using the following notion of traces.
Definition 6 (Trace Values). We fix disjoint sets TA and TC of trace values,
and assume two functions TA : A → ℘fn (TA ) and TC : C → ℘fn (TC ) that return
a finite set of trace values for each antecedent and consequent, respectively. In
an abuse of notation, for a sequent S = A ⊢ C, we may write TA (S) and TC (S)
to denote TA (A) and TC (C) respectively. Then, in a further abuse of notation,
for a node ν in a cyclic pre-proof we write TA (ν) and TC (ν) for TA (seq(ν)) and
TC (seq(ν)) respectively.
                      S Moreover, for a cyclic pre-proof P we may write TA (P)
to stand for the set ν∈P TA (ν), and write TC (P) for the similarly defined set
of consequent trace values appearing in P. We may drop the subscript and refer
to both functions using T where the meaning is clear from the context.
    Let O denote (an initial segment of) the ordinals.
Definition 7 (Trace Pair Functions). A trace pair function δ is a (computable)
family of pairs of functions, one for each (non-axiomatic) rule instance:

   δ (r,(S,S1..n ),i) : (TA (S) × TA (S i ) ⇀ O) × (TC (S) × TC (S i ) ⇀ O)

where for each function r ∈ R, (S, S 1..n ) ∈ Rr , and i ∈ {1, . . . , n}. For conve-
                                 (r,(S,S),i)
nience we will henceforth write δk           for projk (δ (r,(S,S),i) ) where k ∈ {1, 2}
and projk projects the k element of a tuple, or simply δ (r,(S,S),i) when the value
                        th

of k is clear from the context.
     The intuition behind the trace pair functions is that the ordinal assigned to
a trace pair represents a minimum distance between the ‘size’ of any models
that realize these trace values.
                                            (r,(S,S),i)
     When (τ, τ ′ ) is in the domain of δk               (for k ∈ {1, 2}), we say that (τ, τ ′ )
is a (resp. left-hand and right-hand) trace pair for the rule instance (S, S) ∈ Rr
                                             (r,(S,S),i)
with respect to the ith premise. If δk                   (τ, τ ′ ) > 0 then (τ, τ ′ ) is called a
                                                                                (r,(S,S),i)
progressing trace pair, and it is called non-progressing when δk                             (τ, τ ′ ) = 0.
                                                                       ′
If ν is a node in a cyclic pre-proof, with child nodes ν 1..m , then in an abuse of
                              (ν,ν ′ )  (rule(ν),(seq(ν),(seq(ν ′1 ),...,seq(ν ′m ))),i)
notation we may write δk i for δk                                                        , and say that
(τ, τ ′ ) is a left-hand (resp. right-hand) trace pair for (ν, ν ′i ) when (τ, τ ′ ) is in
                     (ν,ν ′ )
the domain of δk i for k = 1 (resp. k = 2). For a left-hand (resp. right-hand)
trace value τ ∈ T(ν), we say that τ is terminal for (ν, ν ′i ) if there is no trace
value τ ′ such that (τ, τ ′ ) is a left-hand (resp. right-hand) trace pair for (ν, ν ′i ).
We say that τ is simply terminal for ν when τ is terminal for each (ν, ν ′i ).
     A cyclic entailment proof system is a tuple (S, r, T, δ). From now on, we
shall assume some fixed cyclic entailment system.
Definition 8 (Traces). A left-hand (resp. right-hand) trace τ ∈ TAω (resp. τ ∈
TCω ) is a (possibly infinite) sequence of trace values. We say that a left-hand

                                                    3
(resp. right-hand) trace follows a path ν in a pre-proof P when for every non-
terminal value τ i in the trace there are corresponding nodes ν i and ν i+1 in
the path such that (τ i , τ i+1 ) is a trace pair for (ν i , ν i+1 ). If (τ i , τ i+1 ) is a
progressing trace pair for (ν i , ν i+1 ), then we say that the trace progresses at i.
If the trace progresses at infinitely many points, then we say that it is infinitely
progressing.
Definition 9 (Global Soundness). A cyclic pre-proof P is a valid cyclic proof
when every infinite path ν ∈ P has a tail that is followed by some infinitely
progressing left-hand trace.

    This global soundness condition is decidable via a Büchi automata construc-
tion. If the proof system is sufficiently well-behaved – specifically, if it admits
an ordinal trace function – then validity of sequents occurring in cyclic proofs
is guaranteed.
Definition 10 (Ordinal Trace Function). An ordinal trace function is a partial
function Θ : (TA ∪ TC ) × M ⇀ O which is (at least) defined on all (τ, m) such
that τ ∈ TA (A) and m |= A for some antecedent A and, dually, is undefined
on all (τ, m) such that τ ∈ TC (C) . As usual, we write Θ(τ, m)↓ to denote that
(τ, m) ∈ dom(Θ).
    The ordinal trace function must also satisfy the following condition.
Definition 11 (Descending Counter-model Property). An ordinal trace func-
tion Θ satisfies the descending counter-model property if and only if for all
r ∈ r:

  m 6|= S ∧ (S, S) ∈ Rr ⇒
                     ∃ m′ , Si ∈ S : m′ 6|= Si ∧
                                  (r,(S,S),i)
                               (δ1              (τ, τ ′ ) = α ⇒ Θ(τ ′ , m′ ) + α ≤ Θ(τ, m))

    The ordinal trace function can be seen as a realization function that assigns
realizers to trace values; thus models realize trace values. In fact, the ordinal
trace function provides more information: it also tells us the ‘size’ of each re-
alization. We note that the existence of an ordinal trace function entails local
soundness, because of the requirement that falsifiability of the conclusion of a
rule implies falsifiability of one of its premises.
    Let us assume that an ordinal trace function exists for our cyclic entailment
system. The following soundness result holds.
Theorem 12 (Soundness of Cyclic Proof Systems). Suppose P is a valid cyclic
proof of a sequent S (i.e. P satisfies the global soundness condition of Defini-
tion 9), then S is valid.
    We will now consider a further global condition on pre-proofs which allows
us to relate antecedent trace values to consequent trace values. The intention is


                                                 4
that, for valid cyclic proofs, this relation is sound in the sense that the ordinal
trace function respects this ordering.
    We begin by defining a maximality property for right-hand traces. For this
notion we fix a (decidable) predicate on rule instances (A ⊢ C, S) and right-
hand trace values τ ∈ T (C), that we call the exclusion predicate, with the
property that (A ⊢ C, S) excludes τ only if either there are no models m such
that m |= A or there is no model m of A such that Θ(τ, m)↓. For example, if the
proof system contains an inconsistency axiom (i.e. there exist no models of the
sequent) then every instance of that axiom excludes all consequent trace values
of the sequent. We use this predicate to disregard right-hand traces which do
not correspond to any model of the initial trace value.
Definition 13 (Maximal Right-hand Traces). Let τ be a right-hand trace fol-
lowing a path ν in a (cyclic) pre-proof; we say that τ is maximal when: i) it is
finite (of length n, say); and ii) τ n is terminal for ν n . When ν n excludes τ n
then we say τ is negative; otherwise, we say it is positive. In the case that ν n
is axiomatic, we say that τ is partially maximal, and fully maximal otherwise.
    We will need to ensure that maximal right-hand traces can be matched up
with left-hand traces in a way that allows us to relate the sizes of the models
that realize their initial trace values. To do so, we define two (semantic) notions
for rules instances and sequents, respectively. We will write 1 for the least value
taken by the ordinal trace function Θ.
Definition 14 (Grounded Traces). Let (A ⊢ C, S) ∈ Rr be an instance of rule
r and τ ∈ T(C) a trace value terminal for (A ⊢ C, S); we say that τ is ground
with respect to (A ⊢ C, S) if whenever A ⊢ C is valid then m |=A A implies
that, when defined, Θ(τ, m) = 1 for all models m. We say that a trace τ 1..n
following a path ν is grounded when its final trace value is ground (i.e. when
τ n is ground with respect to ν n ).
   Intuitively, this property allows us to determine when a maximal right-hand
trace (following some path) ends in a trace value that is realized by a ‘smallest’
model. Typically, the node in a path corresponding to the last value in such a
maximal right-hand trace will be an instance of an unfolding rule. Some proof
systems will allow maximal right-hand traces with final values whose realizers
are not minimal, and we will want to ensure that we do not consider such
traces. A typical example of such traces are those where the node in the proof
corresponding to the final trace value is an instance of a right weakening rule.
   We also define a family of relations between antecedent trace values TA and
consequent trace values TC , indexed by sequents. The intuition is that related
trace values have realizers of equal sizes.
Definition 15 (Trace Values Equated by a Sequent). We say that a sequent
S ≡ A ⊢ C equates trace values τ ∈ T(A) and τ ′ ∈ T(C), and write τ =S τ ′ , if
whenever S is valid then m |=A A and Θ(τ ′ , m)↓ implies that Θ(τ, m) = Θ(τ ′ , m)
for all models m.


                                        5
    The two properties that we have just defined will not, in general, be decidable
for any given cyclic proof system. Therefore, in order to infer size relationships
from cyclic proofs, we may need to approximate them. In the case of ground
trace values, it will be sufficient if we can decide this for all instances of a given
set of rules; then we can simply define no trace values to be ground with respect
to instances of rules outside this set. Similarly, for trace values equated by a
sequent, it will be sufficient for this to be decidable only for those sequents that
are the conclusion of an axiomatic rule instance.
    To relate antecedent and consequent trace, we will be considering a quantita-
tive property of left- and right-hand traces, essentially counting the progression
along each of the traces. We therefore define the following notion of size for
traces.
Definition 16 (Size of a Trace Along a Path). The size progν (τ ) of a finite
left-hand (resp. right-hand) trace τ 1..n along a path ν which it follows is defined
as follows, where k = 1 (resp. k = 2):

     progν (τ ) = 0                                                       (n = 1)
                   (ν   ,ν )                         (ν ,ν )
     progν (τ ) = δk n−1 n (τ n−1 , τ n ) + . . . + δk 1 2 (τ 1 , τ 2 )   (n > 1)

Notice that this definition uses a reverse sum. This is crucial for our result,
as can been seen in the proof of Lemma 21, and is necessary because ordinal
addition is not commutative.
    We can now define a trace value ordering relation with respect to pre-proofs.
It is this relation that we intend to express the size relationship between the
realizers (models) of trace values, and thus is at the heart of the result we present
here.
Definition 17 (Trace Value Ordering Relations). Let seq(ν) = A ⊢ C be a
sequent in a cyclic proof P, with trace values τ1 ∈ T(A) and τ2 ∈ T(C); we will
write τ2 ≤νP τ1 whenever it holds that for all positive maximal right-hand traces
τ 1..n with τ 1 = τ2 following paths ν ∈ P rooted at ν, there exists a left-hand
trace τ ′1..k , with k ≤ n and τ ′1 = τ1 , following ν such that:
    i) progν (τ ) ≤ progν (τ ′ ); and
   ii) either τ is grounded, or τ n is partially maximal, k = n and τ ′n =seq(ν n )
       τ n.
If this condition holds with progν (τ ) < progν (τ ′ ), then we write τ2 <νP τ1 .
    We now proceed to define the extra property required of the ordinal trace
function to be able to ensure that the trace value ordering relation is sound
for valid proofs. In the following definition, we call a rule instance (S, S) valid
whenever the conclusion S and each premise S i are all valid sequents.
Definition 18 (Descending Model Property). An ordinal trace function Θ sat-
isfies the descending model property if and only if for all valid, non-axiomatic
rule instances (A ⊢ C, S) ∈ Rr (r ∈ r), trace values τ1 ∈ T(A) and τ2 ∈ T(C),
and models m |=A A, there exists a premise Ai ⊢ Ci ∈ S and a model m′ such
that:

                                            6
   i) m′ |=A Ai ;
                                                               (r,(A⊢C,S),i)
  ii) τ2 is terminal for (A ⊢ C, S) or there is τ ′ such that δ2             (τ2 , τ ′ )
      is defined; and
 iii) for all trace values τ ′ ∈ T and k ∈ {1, 2}:

          (r,(A⊢C,S),i)
        δk                (τk , τ ′ ) = α ∧ Θ(τk , m)↓
                                           ⇒ Θ(τ ′ , m′ )↓ ∧ Θ(τ ′ , m′ ) + α ∼k Θ(τk , m)
                 def               def
      where ∼1 = ≤ and ∼2 = ≥
    Notice that this is different from the descending counter -model property
that we defined above, in that it says something about the models of valid
sequents rather than counter -models of invalid ones, and that it also talks about
consequent trace values. It asserts that the trace pair function soundly bounds
the difference in size between the realizations (i.e. models) of trace pairs. In the
case of antecedents this difference is bounded from above, and for consequents
from below. As we shall see below, this means that the (reverse) sum of all the
progression steps along a left-hand trace acts as a lower bound on the size of
realizations of the initial trace value; similarly, this sum for a right-hand trace
serves as an upper bound.
    If an ordinal trace function satisfies the trace descent property above, then
this is sufficient to guarantee that every model of a sequent in a valid cyclic
proof corresponds to some positive maximal right-hand trace. We make this
correspondence formal through the following notion of support.
Definition 19 (Trace Supports). Let ν be a path in a pre-proof P, where we
have seq(ν i ) ≡ Ai ⊢ Ci for each node ν i in the path, and let τ 1..n be a finite left-
hand (resp. right-hand) trace; we say that a sequence of models m1..k (k ≥ n)
supports τ along ν (and call m witness of the support) if τ follows ν and
mi |=A Ai (resp. mi |=C Ci ) with Θ(τ i , mi )↓ for each 0 < i ≤ n, and:
                                         (ν ,ν j+1 )
                Θ(τ j+1 , mj+1 ) + δk j                (τ j , τ j+1 ) ∼ Θ(τ j , mj )
                                                 def                              def
for each 0 < j < n where k = 1 and ∼ = ≤ (resp. k = 2 and ∼ = ≥). We may
also say that a model m supports a trace τ along a path ν when there exists a
support witness m of τ along ν with m1 = m.
   We can show that if the ordinal trace function satisfies the trace descent
property then every model of a sequent in a cyclic proof corresponds to (in the
sense that it supports) a (necessarily positive) maximal right-hand trace along
some path rooted at that sequent. In fact, we have the stronger result that the
same witness of this right-hand trace support additionally supports all left-hand
traces that also follow this path.
Lemma 20 (Supported Trace Existence). Assume the ordinal trace function
satisfies the Trace Descent Property. If A ⊢ C ≡ seq(ν) is the sequent of a node
ν in a cyclic proof P such that there is a trace value τ ′ ∈ T(C), and m is a

                                                7
model such that m |=A A and Θ(τ ′ , m)↓, then there exists a path ν in P rooted
at ν, a positive maximal right-hand trace τ ′1..n beginning with τ ′ and a witness
m with m1 = m such that m supports τ ′ along ν; moreover m supports all
left-hand traces τ that follow ν.
Proof. Since P is a cyclic proof, all the sequents it contains are valid. Using the
Trace Descent Property, we can then show that there exists a path ν ∈ P rooted
at ν, a right-hand trace τ ′1..n beginning with τ ′ following ν and a witness m with
m1 = m such that i) m supports τ ′ along ν; and ii) m supports all left-hand
traces τ that follow ν. Now, τ ′ cannot be infinite since if it were then, because
P is a valid cyclic proof, there would be an infinitely progressing left-hand trace
following ν from which we could infer, by the properties of supported traces, the
existence of an infinite descending chain of ordinals. Furthermore, there must
exist a maximal such right-hand trace since if τ ′1..n were not maximal then one of
the following two situations would hold. On the one hand, if An ⊢ Cn ≡ seq(ν n )
is an instance of an axiom then it cannot be inconsistent since we have that
mn |=A An ; thus it must be that τ ′ n is ground with respect to ν n , and so τ ′
is positve. On the other hand, if there exists a right-hand trace pair (τ ′n , τ ′′ )
for ν n then by the Trace Descent Property, a support must exist for this longer
trace.
    Supported traces have the following property, which expresses that the (re-
verse) sum of the progression steps in the trace bound (either from below, in
the case of left-hand traces, or from above in the case of right-hand traces) the
size of the models in the support as realizers of the values in the trace.
Lemma 21. If m supports a finite left-hand (resp. right-hand) trace τ 1..n along
                                                                               def
a path ν then it follows that Θ(τ n , mn ) + progν (τ ) ∼ Θ(τ 1 , m1 ) where ∼ = ≤
         def
(resp. ∼ = ≥).
Proof. By induction on the length of the trace n.
(n = 1): Immediate, since then progν (τ ) = 0, τ 1 = τ n and ν 1 = ν n .
(n = k + 1): Then m2.. supports τ 2..n along ν 2.. , so by the inductive hypothesis
                        Θ(τ n , mn ) + progν 2.. (τ 2..n ) ∼ Θ(τ 2 , m2 )
      Therefore, since ordinal addition is monotone in the right argument
                                                  (ν ,ν 2 )
         Θ(τ n , mn ) + progν 2.. (τ 2..n ) + δ1 1            (τ 1 , τ 2 )
                                                                                          (ν ,ν 2 )
                                                          ∼ Θ(τ 2 , m2 ) + δ1 1                       (τ 1 , τ 2 )
      By Definition 16, this gives
                                                                             (ν ,ν 2 )
                 Θ(τ n , mn ) + progν (τ ) ∼ Θ(τ 2 , m2 ) + δ1 1                         (τ 1 , τ 2 )
      Furthermore, by the definition of trace supports (Definition 19)
                                         (ν ,ν 2 )
                        Θ(τ 2 , m2 ) + δ1 1          (τ 1 , τ 2 ) ∼ Θ(τ 1 , m1 )
      Thus the result holds by the transitivity of ≤ for the ordinals.

                                              8
    This leads to the soundness of the trace value ordering relations of a cyclic
proof. Intuitively, this result holds because when two trace values are related by
a trace value ordering relation, for any given model, the upper bound on its size
as a realizer of the consequent trace value is not greater (or is strictly smaller)
than the lower bound on its size as a realizer of the antecedent trace value.
Theorem 22 (Soundness of Trace Value Ordering). Let seq(ν) = A ⊢ C be a
sequent in a cyclic proof P, with trace values τ1 ∈ T(A) and τ2 ∈ T(C); then,
for ∼ ∈ {<, ≤}

      τ2 ∼νP τ1 ⇒ ∀ m ∈ M : m |=A A ∧ Θ(τ2 , m)↓ ⇒ Θ(τ2 , m) ∼ Θ(τ1 , m)

Proof. Suppose that τ2 ∼νP τ1 and take an arbitrary model such that m |=A A
and Θ(τ2 , m)↓. By Lemma 20, there exists a path ν ∈ P rooted at ν, a positive
maximal right-hand trace τ ′1..n beginning with τ2 and a witness m with m1 = m
such that m supports τ ′ along ν.
    Since τ2 ∼νP τ1 there is also a left-hand trace τ 1..k , with k ≤ n and τ 1 = τ1 ,
following ν and satisfying progν (τ ′ ) ∼ progν (τ ). By the trace support existence
lemma, we also have that m supports τ along ν.
    There are now two possibilities: τ ′ is either fully or partially maximal. In
case of the former, τ ′n is ground with respect to ν n , so Θ(τ ′n , mn ) = 1 and
therefore Θ(τ ′n , mn ) ≤ Θ(τ k , mk ). In case of the latter, if τ ′n is not ground
with respect to ν n , then k = n and τ n =seq(ν n ) τ ′n therefore Θ(τ n , mn ) =
Θ(τ ′n , mn ), and so also Θ(τ ′n , mn ) ≤ Θ(τ k , mk ). Thus, the result derives from
the following chain of inequalities:

      Θ(τ ′1 , m1 ) ≤ Θ(τ ′n , mn ) + progν (τ ′ )   (Lemma 21)
                                                ′
                   ≤ Θ(τ k , mk ) + progν (τ )       (weak left monot. of +)
                   ∼ Θ(τ k , mk ) + progν (τ )       (right monot. of +)
                   ≤ Θ(τ 1 , m1 )                    (Lemma 21)

    To decide whether τ2 ≤νP τ1 holds for some given node in a cyclic proof, we
will encode the problem as a language containment problem between weighted
automata. Although the language containment problem for weighted automata
is known to be undecidable in general [7, 1], it is decidable for the sub-class of
finite-valued weighted sum-automata [6].
    Weighted automata [5] generalise finite-state automata by assigning to each
word a value that is taken from a (usually infinite) set of weights, rather than
simply a binary value indicating whether the word is included in the language or
not. A weighted automaton A over an alphabet Σ and a semiring (V, ⊕, ⊗) of
weights is a tuple (Q, qI , F, ∆, γ) where Q is a set of states, qI ∈ Q is the initial
state, F ⊆ Q is the set of final states, ∆ ⊆ Q × Σ × Q is the transition relation,
and γ : ∆ → V is a function assigning a weight to each transition. A run ρ of A
over a word w = σ1 . . . σn ∈ Σ∗ is a sequence q0 σ1 q1 . . . σn qn such that q0 = qI
                                                                      w
and (qi−1 , σi , qi ) ∈ ∆ for all i ∈ {1, . . . , n}. We write ρ : q0 −
                                                                      → qn to denote
                                                                                w
that ρ is a run over w starting at state q0 and ending at qn . A run ρ : q0 −   → qn


                                            9
                                                                                1 σ ...σ
                                                                                    n
is called accepting if qn ∈ F . The value V(ρ) of a run ρ : q0 −−                 −−→  qn is
defined as the semiring product of the weight of each transition in the run,
i.e. V(ρ) = γ(q0 , σ1 , q1 ) ⊗ . . . ⊗ γ(qn−1 , σn , qn ), if ρ is accepting, and V(ρ) = ⊥
otherwise1 . We write RA (w) to denote the set {V(ρ) | ρ is a run of A on w}.
When RA (w) is non-empty then we say that w is in the domain of A and
write w ∈ dom(A ). The quantitative language LA defined by A is aLfunction
LA : Σ∗ → V , defined by LA (w) = ⊥ if w 6∈ dom(A ), and LA (w) =                     RA (w)
otherwise. Given two weighted automata A and B, we write LA ≤ LB if
and only if LA (w) ≤ LB (w) for all words w ∈ Σ∗ . Furthermore, we will write
LA < LB if and only if LA (w) < LB (w) for all words w such that LA (w) 6= ⊥.
     The semiring over which we will construct our automata is the ordinal-valued
max-plus (tropical) semiring (O⊥ , ⊕, ⊗) where α ⊕ β = max(α, β) with ⊥ < α
for all α ∈ O, and α ⊗ β = β + α (where + is the usual addition on ordinals)
with ⊥ ⊗ α = α ⊗ ⊥ = ⊥ for all α ∈ O.
Definition 23. Let P be a cyclic proof, and define the alphabet ΣP = nodes(P)∪
(℘(TA (P)) × TC (P)), and for τ ∈ TC (ν) let Tν (τ ) denote the set defined by
Tν (τ ) = {τ ′ | τ ′ ∈ TA (ν)∧τ ′ =seq(ν) τ }. For each node νinit ∈ P and trace values
τ1 ∈ TA (νinit ) and τ2 ∈ TC (νinit ), we can construct two weighted automata over
ΣP and (O⊥ , ⊕, ⊗) as follows:
               (P,ν    )                  A       A    A    A    A
            A(τ1 ,τ2init
                     ) = (QA , qA , FA , ∆init ∪ ∆1 ∪ ∆2 ∪ ∆3 ∪ ∆4 , γA )
               (P,ν    )
            B(τ1 ,τinit
                   2)
                        = (QC , qC , FC , ∆Cinit ∪ ∆C1 ∪ ∆C2 , γC )

where

      QA = (nodes(P) × TA (P)) ⊎ {⊥} ⊎ {⊤} ⊎ {qA }
      QC = (nodes(P) × TC (P)) ⊎ {⊥} ⊎ {qC }
      FA = QA \ {qA }
      FC = {⊥} ∪ {(ν, τ ) | ν not axiomatic, τ terminal for ν,
                                                        and ν does not exclude τ }
                      ∪ {(ν, τ ) | ν axiomatic, τ ground with respect to ν,
                                                            and ν does not exclude τ }

    ∆A
     init = {(qA , νinit , (νinit , τ1 ))}
                                                                      (ν,ν ′ )
      ∆A               ′    ′ ′            ′             ′
       1 = {((ν, τ ), ν , (ν , τ )) | (ν, ν ) ∈ P ∧ (τ, τ ) ∈ dom(δ1             )}
      ∆A                    ′    ′                       ′                    ′
       2 = {((ν, τ ), (Tν (τ ), τ ), ⊥) | ν axiomatic ∧ τ ∈ TC (ν) ∧ τ ∈ Tν (τ )}

      ∆A               ′             ′
       3 = {((ν, τ ), ν , ⊤) | (ν, ν ) ∈ P}

      ∆A
       4 = {(⊤, ν, ⊤) | ν ∈ nodes(P)}

    ∆Cinit = {(qC , νinit , (νinit , τ2 ))}
   1 Note that we can always augment a semiring (V, ⊕, ⊗) with a fresh zero element ⊥, which

can be used to denote an ‘undefined’ value.


                                              10
                                                                                  (ν,ν ′ )
      ∆C1 = {((ν, τ ), ν ′ , (ν ′ , τ ′ )) | (ν, ν ′ ) ∈ P ∧ (τ, τ ′ ) ∈ dom(δ2              )}
      ∆C2 = {((ν, τ ), (Tν (τ ), τ ), ⊥) | τ ∈ TC (ν), ν axiomatic,
                                        τ not ground w.r.t. ν, ν does not exclude τ }

                               (
                                    (ν,ν ′ )
                        ′          δ1          (τ, τ ′ ) if q = (ν, τ ) and q = (ν ′ , τ ′ )
             γA (q, σ, q ) =
                                   0                     otherwise
                               (
                                    (ν,ν ′ )
                        ′          δ2          (τ, τ ′ ) if q = (ν, τ ) and q = (ν ′ , τ ′ )
             γC (q, σ, q ) =
                                   0                     otherwise

                                          (P,ν)
We say that the automaton B(τ1 ,τ2 ) is grounded whenever it holds that τ is
ground with respect to each reachable final state (ν, τ ) ∈ FC .
                            (P,ν)
    The language of B(τ1 ,τ2 ) contains all and only the paths in P rooted at ν
followed by positive maximal right-hand traces starting with τ2 , and the value
of a word is the maximum of the sizes of all such right-hand traces following
                                                                 (P,ν)
the path it corresponds to. Furthermore, the language of A(τ1 ,τ2 ) contains all
sequences of nodes (in P) containing a prefix which is a path in P rooted at ν
and followed by a (maximal) left-hand trace starting with τ1 . In particular, it
contains all (finite) paths in P rooted at ν, and the value of a path (word) is the
maximum of the sizes of all left-hand traces following it. Thus, provided that
  (P,ν)
B(τ1 ,τ2 ) is grounded, this construction then ensures that LB(P,ν) ≤ LA (P,ν) if
                                                                                  (τ1 ,τ2 )       (τ1 ,τ2 )
and only if τ2 ≤νP τ1 .
                                                                                     ν
Lemma 24. If ν 1..n is a path in a cyclic proof P and ρ : qA −      → qn is a run of
   (P,ν)
A(τ,τ ′ ) then there exists a left-hand trace τ 1..k (k ≤ n) with τ 1 = τ such that
qi = (ν i , τ i ) for each i ∈ {1, . . . , k} and qj = ⊤ for each j ∈ {k + 1, . . . , n}.
Moreover, if qn = (ν n , τ ′′ ) for some trace value τ ′′ then k = n and τ ′′ = τ n .
Proof. By induction on n.
Lemma 25. Let ν 1..n be a path in a cyclic proof P and let τ 1..k (k ≤ n) be a
                                                                                     ν
left-hand trace; then τ follows ν if and only if there exists a run ρ : qA −         → qn of
   (P,ν )
A(τ 1 ,τ 1′ ) such that qi = (ν i , τ i ) for each i ∈ {1, . . . , k}. Moreover it holds that
V(ρ) ≥ progν (τ ) and, furthermore, if k = n or qk+1 = ⊤ then progν (τ ) ≥ V(ρ).
Proof. By induction on n.
Lemma 26. Let ν be a finite sequence of nodes in a cyclic proof P and let τ 1..n
be a right-hand trace; then ν is a path in P followed by τ if and only if ρ =
                                                        (P,ν )
qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) is a run of B(τ ′ ,τ11 ) . Moreover V(ρ) = progν (τ ).

Proof. By induction on n.



                                                      11
Corollary 27. τ 1..n is a positive maximal right-hand trace following ν in P if
                                                   (P,ν )
and only if ρ is an accepting run of B(τ ′ ,τ11 ) such that either:
   i) ρ = qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) (in which case either τ is fully maximal
      or τ n is ground with respect to ν n ); or
  ii) ρ = qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) (Tν n (τ n ), τ n ) ⊥ (in which case τ is par-
      tially maximal).
Moreover it holds that V(ρ) = progν (τ ).
Proof. Immediately from lemma 26 and the definitions of maximal right-hand
traces (definition 13) and the automata constructions (definition 23).
Theorem 28 (Soundness and Completeness of the Automata Construction).
Let P be a cyclic proof, ν be a node in P, and τA ∈ TA (ν) and τC ∈ TC (ν) be
trace values; then, for ∼ ∈ {<, ≤}, τC ∼νP τA if and only if LB(P,ν) ∼ LA (P,ν)
                                                                               (τA ,τC )          (τA ,τC )
     (P,ν)
and B(τA ,τC ) is grounded.

Proof. (if ): Let τ 1..n be a positive maximal right-hand trace with τ 1 = τC
      following a path ν in P rooted at ν. We now consider the following two
     (exhaustive) possibilities:
       (τ is partially maximal): thus ν n is axiomatic and by corollary 27,
                                             (P,ν)
            there is an accepting run ρ of B(τA ,τC ) such that V(ρ) = progν (τ )
            and one of the following two cases holds:
               i) ρ = qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) and so τ n is ground with re-
                  spect to ν n . Since LB(P,ν) ∼ LA (P,ν) , there exists an ac-
                                                       (τA ,τC )   (τA ,τC )
                                     ′           ν 1..n   (P,ν)
                  cepting run ρ          : qA −−−→ q of A(τA ,τC ) such that V(ρ) ∼ V(ρ′ ).
                  By lemmas 24 and 25 it then follows that there exists a left-
                  hand trace τ ′ 1..k (k ≤ n) with τ ′1 = τA following ν such that
                  V(ρ′ ) = progν (τ ′ ), and thus that progν (τ ) ∼ progν (τ ′ ). There-
                  fore, the conditions of definition 17 are met for τ and ν.
              ii) ρ = qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) (Tν n (τ n ), τ n ) ⊥. Then, since
                                                                       ν 1..n ·(Tν (τ n ),τ n )
                  LB(P,ν)         ∼ LA (P,ν) , it follows ρ′ : qA −−−−−−−
                                                                        n
                                                                         −−−−−→ q is an
                      (τA ,τC )          (τA ,τC )
                                               (P,ν)
                  accepting run of A(τA ,τC ) such that V(ρ) ∼ V(ρ′ ). By construc-
                                                          ν                                  (P,ν)
                  tion, q = ⊥ and ρ′′ : qA −−1..n −→ (ν n , τ ′ ) is a run of A(τA ,τC ) for
                          ′
                  some τ and therefore, by lemmas 24 and 25, there exists a left-
                  hand trace τ ′1..n with τ ′1 = τA and τ ′n = τ ′ such that τ ′ follows
                  ν and V(ρ′′ ) = progν (τ ′ ). Also by construction, we have that
                  τ ′ ∈ Tν n (τ n ) and therefore that τ ′n =seq(ν n ) τ n . Now notice

                              V(ρ′ ) = V(ρ′′ ) ⊗ γA ((ν n , τ ′n ), (Tν n (τ n ), τ n ), ⊥)
                                      = V(ρ′′ ) ⊗ 0
                                      = 0 + V(ρ′′ ) = V(ρ′′ )



                                                     12
              and therefore that progν (τ ) ∼ progν (τ ′ ). Thus, the conditions
              of definition 17 are met for τ and ν.
     (τ is fully maximal): thus ν n is axiomatic and by corollary 27, there is
                                                                              (P,ν)
          an accepting run ρ = qC ν 1 (ν 1 , τ 1 ) . . . ν n (ν n , τ n ) of B(τA ,τC ) such
                                                             (P,ν)
           that V(ρ) = progν (τ ). Since B(τA ,τC ) is grounded it follows that τ n
           is ground with respect to ν n . The remainder of this case proceeds as
           for item (i) above.
     Thus, since the conditions of definition 17 are met for an arbitrary positive
     maximal right-hand trace τ and path ν in P, it follows that τC ∼νP τA .
                                                                               
                                                                          (P,ν)
(only if ): We first show LB(P,ν) ∼ LA (P,ν) . Take any w ∈ dom B(τA ,τC ) ;
                                         (τA ,τC )          (τA ,τC )
                                                                                (P,ν)
     there must exist a maximally valued run ρ of B(τA ,τC ) over w. Then
     LB(P,ν) (w) = V(ρ) since ρ is maximally valued. Notice that ρ may take
         (τA ,τC )
     one of two forms:
     ρ = qC ν1 (ν1 , τ1 ) . . . νn (νn , τn ) with ν1 = ν and τ1 = τC . Then by corol-
          lary 27 ν = ν1 . . . νn is a path in P followed by right-hand trace
          τ = τ1 . . . τn with τ a positive maximal trace, and V(ρ) = progν (τ ).
          Since τC ∼νP τA it follows that there exists a left-hand trace τ ′1..k fol-
          lowing ν with k ≤ n and τ ′1 = τA , and furthermore that progν (τ ) ∼
                                                                             ν
          progν (τ ′ ). Therefore by lemma 25 there is a run ρ′ : qA −       → qn of
             (P,ν)
          A(τA ,τC ) such that progν (τ ′ ) ≤ V(ρ′ ). Notice that ρ′ is an accepting
                                                                        (P,ν)
           run since all (non-initial) states in A(τA ,τC ) are accepting. So, by
           definition, V(ρ′ ) ≤ LA (P,ν) (ν). Therefore
                                               (τA ,τC )



               LB(P,ν) (ν) = V(ρ) = progν (τ )
                     (τA ,τC )

                                                            ∼ progν (τ ′ ) ≤ V(ρ′ ) ≤ LA (P,ν) (ν)
                                                                                            (τA ,τC )


     ρ = qC ν1 (ν1 , τ1 ) . . . νn (νn , τn ) (Tν n (τ n ), τ n ) ⊥ with ν1 = ν and τ1 = τC .
          Then by corollary 27 ν = ν1 . . . νn is a path in P followed by right-
          hand trace τ = τ1 . . . τn with τ a positive maximal trace and V(ρ) =
          progν (τ ). By construction, since there is a transition from (νn , τn )
          to ⊥, it follows that νn is axiomatic and that τn is not ground with
          respect to νn . Thus, since τC ∼νP τA , there exists a left-hand trace
          τ ′1..n following ν with τ ′1 = τA such that progν (τ ) ∼ progν (τ ′ )
          and τ ′n =seq(ν n ) τ n ; it therefore follows that τ ′n ∈ Tν n (τ n ). Now
          by lemma 25 there exists a run ρ′ = qA ν 1 (ν 1 , τ ′1 ) . . . ν n (ν n , τ ′n )
          such that V(ρ′ ) = progν (τ ′ ). Moreover by construction there is a
                                (P,ν)
          transition in A(τA ,τC ) from (ν n , τ ′n ) to ⊥ via (Tν n (τ n ), τ n ). Thus ρ′′
                                 (P,ν)
           is a run of A(τA ,τC ) over w, where

                         ρ′′ = qA ν 1 (ν 1 , τ ′1 ) . . . ν n (ν n , τ ′n ) (Tν n (τ n ), τ n ) ⊥

                                                       13
            Notice that it is an accepting run since all (non-initial) states in
              (P,ν)
            A(τA ,τC ) are accepting, and moreover that by construction V(ρ′′ ) =
            V(ρ′ ). Also, by definition it holds that V(ρ′′ ) ≤ LA (P,ν) (w). There-
                                                                                   (τA ,τC )
            fore

               LB(P,ν) (w) = V(ρ) = progν (τ )
                   (τA ,τC )

                                                       ∼ progν (τ ′ ) = V(ρ′′ ) ≤ LA (P,ν) (w)
                                                                                           (τA ,τC )


                         (P,ν)
      To see that B(τA ,τC ) is grounded, consider an arbitrary reachable final
                               (P,ν)
      state (ν ′ , τ ′ ) of B(τA ,τC ) where ν ′ is not axiomatic (in the case that ν ′ is ax-
      iomatic we have by construction that τ ′ is ground with respect to ν ′ ). Since
      (ν ′ , τ ′ ) is reachable, there is accepting run q = qC ν1 (ν1 , τ1 ) . . . νn (νn , τn )
      with ν ′ = νn and τ ′ = τn . Thus by corollary 27 it follows that ν =
      ν1 . . . νn is a path in P followed by positive maximal right-hand trace
      τ = τ1 . . . τn . Since τC ∼νP τA it follows that τn is ground with respect to
      νn . Since the choice of reachable final state was arbitrary, we have that
         (P,ν)
      B(τA ,τC ) is grounded.

   We now show that when certain constraints are placed on the trace pair
function δ, the constructions of definition 23 result in automata that are finitely
ambiguous. That is, the number of runs of the automata on any given word is
bounded. Finitely ambiguous automata (over certain semirings) have decidable
containment [6].
Definition 29. We say that a trace pair function δ is trace injective if every
 (r,(S,S),i)
δk           satisfies the following, for every τ , τ ′ , and τ ′′ :
                               (r,(S,S),i)                         (r,(S,S),i)
         (τ ′ , τ ) ∈ dom(δk                 ) ∧ (τ ′′ , τ ) ∈ dom(δk            ) ⇒ τ ′ = τ ′′

Lemma 30. Suppose δ is trace injective and let ν be a node in a cyclic proof
P with τ ∈ TA (ν) (resp. τ ∈ TC (ν)) a trace value in ν; then for all paths ν 1..n
rooted at ν and left-hand (resp. right-hand) traces τ 1..n and τ ′ 1..n following ν
with τ 1 = τ ′ 1 = τ , if τ n = τ ′ n then τ = τ ′ .
Proof. By induction on n. The base case (n = 1) is immediate. For the inductive
step, assume a path ν 1..(i+1) rooted at ν followed by left-hand (resp. right-
hand) traces τ 1..(i+1) and τ ′ 1..(i+1) with τ 1 = τ ′ 1 = τ ; furthermore, assume
that τ i+1 = τ ′ i+1 . Since both τ and τ ′ follow ν we have that (τ i , τ i+1 ) ∈
       (ν ,ν  )                              (ν ,ν    )
dom(δk i i+1 ) and (τ ′ i , τ ′ i+1 ) ∈ dom(δk i i+1 ) for k = 1 (resp. k = 2). Then,
since τ i+1 = τ ′ i+1 and δ is trace injective, it follows that τ i = τ ′ i . Then by the
inductive hypothesis we have that τ 1..i = τ ′ 1..i , whence the result follows.
    The significance of lemma 30 is that when the trace pair function is trace
injective there is a bound on the number of possible traces following any given


                                                     14
                                                                               (P,ν)
path. As an immediate corollary, every automaton B(τ1 ,τ2 ) is finitely ambiguous.
However, even when the trace pair function is trace injective it is not necessarily
                                                     (P,ν)
the case that a left-hand trace automaton A(τ1 ,τ2 ) is finitely ambiguous. The
reason for this is the presence of the ‘sink’ state ⊤. When a proof contains a
(left-hand) trace cycle (of the form (n1 , τ1 ) . . . (nj , τj ) with nodes n1 = nj and
trace values τ1 = τj ), the resulting left-hand trace automaton will contain the
following configuration of states:
                   n2                 nj−1
                                                                 n1
           n1                                        nj−1
                                ...                                        ⊤            n1 , . . . , nj−1
           τ1                                        τj−1
                                 n1

                                                            w                                         w
That is, there are runs (nj−1 , τj−1 ) −  → (nj−1 , τj−1 ), (nj−1 , τj−1 ) −
                                                                           → ⊤, and
    w
⊤−  → ⊤ with w = n1 . . . nj−1 . This results in the automaton being infinitely
ambiguous [8, §3] and thus when the weight of the cycle is non-zero it is also
infinite-valued.
    Nonetheless, it is possible to define a sequence of finitely ambiguous weighted
                 (P,ν)
automata A (n)(τ1 ,τ2 ) (where 0 < n ∈ N) that constitute successively better
                                (P,ν)
approximations to A(τ1 ,τ2 ) . For proofs P satisfying certain restrictions, we can
                                                                                (P,ν)
show that there exists n such that we can use A (n)(τ1 ,τ2 ) to decide the trace
value ordering relation ∼νP .
Definition 31. Let P be a cyclic proof and take the alphabet ΣP and sets Tν (τ )
as in definition 23. Then, for each node νinit ∈ P, trace values τ1 ∈ TA (νinit )
                                                                          (P,ν )
and τ2 ∈ TC (νinit ), and every n > 0, define the weighted automaton A (n)(τ1 ,τinit
                                                                                 2)
as follows:
                 (P,ν       )
          A (n)(τ1 ,τinit
                      2)
                          = (Q, qA , F, ∆init ∪ ∆1 ∪ ∆2 ∪ ∆3 ∪ ∆4 ∪ ∆5 , γ)

where    Q = (nodes(P) × TA (P)) ⊎ {⊥} ⊎ {qA }
                                                       ⊎ {⊤νi | ν ∈ nodes(P), 0 < i ≤ n}
         F = Q \ {qA }
      ∆init = {(qA , νinit , (νinit , τ1 ))}
                                                                                          (ν,ν ′ )
        ∆1 = {((ν, τ ), ν ′ , (ν ′ , τ ′ )) | (ν, ν ′ ) ∈ P ∧ (τ, τ ′ ) ∈ dom(δ1                     )}
        ∆2 = {((ν, τ ), (Tν (τ ), τ ), ⊥) | ν axiomatic ∧ τ ∈ TC (ν) ∧ τ ∈ Tν (τ ′ )}
                                         ′      ′                               ′

        ∆3 = {((ν, τ ), ν ′ , ⊤ν1′ ) | (ν, ν ′ ) ∈ P}
        ∆4 = {(⊤νi , ν ′ , ⊤νi ) | 0 < i ≤ n, ν ′ ∈ nodes(P), ν ′ 6= ν}
        ∆5 = {(⊤νi , ν, ⊤νi+1 ) | 0 < i < n}

                                  (
                                         (ν,ν ′ )
                        ′               δ1          (τ, τ ′ ) if q = (ν, τ ) and q = (ν ′ , τ ′ )
             γ(q, σ, q ) =
                                        0                     otherwise

                                                            15
    Note that these ‘approximate’ automata all share a common kernel with
the ‘full’ automaton: the only difference is in the number of ‘sink’ states that
they admit. The construction of Definition 31 refines the sink state of the full
construction into a collection of finite chains of sink states. The crucial difference
is that each chain remembers which letter of the alphabet (i.e. node in the proof)
was encountered on entry. The chain then serves to only allow words containing
a finite number of successive occurrences of that node (i.e. once a left-hand
trace terminates, only paths which visit the next node of the proof up to n
times, and not more, are accepted). It is this which results in the approximate
automata being finitely ambiguous. The full automaton, in contrast, permits
an unbounded number of successive occurrences. Thus, in an abuse of notation,
                                                             (P,ν)       (P,ν)
we will also sometimes find it convenient to write A (ω)(τ,τ ′ ) for A(τ,τ ′ ) .
Lemma 32. When the trace pair function δ is trace injective, each approximate
               (P,ν)
automaton A (n)(τ1 ,τ2 ) is finitely ambiguous.
                                                (P,ν)
Proof. As for the automata B(τ1 ,τ2 ) this follows from lemma 30, which gives
that there is a unique run ending in a state of the form (ν, τ ) for any given word.
We use W(P) to denote the maximum number of trace values occurring in the
antecedent or consequent of any node in P, and refer to this as the trace width
of P. We also use in(P) to denote the graph-theoretic notion of the in-degree
of P (i.e. the maximum number of predecessors for any given node in P). With
                                                                          (P,ν)
lemma 30, it is easy to see that the maximum number of runs of A (n)(τ1 ,τ2 ) that
end in the state ⊥ for any given word is | nodes(P)| × W(P). Similarly making
use of lemma 30, it can be shown by a straightforward induction on the number
of states in the run of the form ⊤nν that maximum number of runs ending in
such a state for any given word has a maximum bound of in(P) × W(P). (The
bound is realised immediately in the base case; the inductive case is a trivial
application of the inductive hypothesis since there can only be a single, unique
transition to the final state for any given letter of the alphabet).
   The approximate automata are sound
                        σ                                                        (P,ν)              σ
Lemma 33. ρ : qA −−−→ qm is a run of A (n)(τ,τ ′ ) only if ρ′ : qA −−
                  1..m                                              1..m ′
                                                                     −→ qm
                   (P,ν)
is a run of A (ω)(τ,τ ′ ) , with qi′ = ⊤ if qi ≡ ⊤jν (for some j and ν), and qi′ = qi
otherwise (for all 0 < i ≤ m); moreover, V(ρ′ ) = V(ρ).
Proof. By induction on the length m of the run.
Corollary 34. LB(P,ν) ∼ LA (n)(P,ν) implies that LB(P,ν) ∼ LA (ω)(P,ν) , for
                      (τ,τ ′ )                     (τ,τ ′ )                              (τ,τ ′ )   (τ,τ ′ )
∼ ∈ {<, ≤}.
                                 σ                                       (P,ν)
                      → q is a run of B(τ,τ ′ ) such that V(ρ) is a positive
Proof. Suppose ρ : q0 −
                                                                                                      σ
                                                                     → q ′ of
maximal trace. Since LB(P,ν) ∼ LA (n)(P,ν) , there is a run ρ′ : q0′ −
                                     (τ,τ ′ )                      (τ,τ ′ )
       (P,ν)
A (n)(τ,τ ′ ) such that V(ρ) ∼ V(ρ′ ). Then, by lemma 33, there is a run ρ′′ :
   σ               (P,ν)
     → q ′′ of A (ω)(τ,τ ′ ) such that V(ρ′ ) = V(ρ′′ ), whence the result follows.
q0′′ −


                                                              16
   We also prove a relative completeness lemma which will be useful later in
showing full completeness for the restricted set of proofs that we will consider.
                             σ1..m                             (P,ν)
Lemma 35. Let ρ : qA −−        −→ qm be a run of A (ω)(τ,τ ′ ) and k be the number
of occurrences of σ i+1 in the sequence σ (i+1)..m , where i is the least such that
                                                                        σ 1..m
qi+1 ≡ ⊤ (we take k = 0 when there exists no such i); then ρ′ : qA −−          ′
                                                                           −→ qm is
              (P,ν)                          ′
a run of A (n)(τ,τ ′ ) for each n ≥ k, with qj = qj if j ≤ i (or j ≤ m if no such i
                      ′
exists) and qj′ = ⊤kσi+1 otherwise, where k ′ is the number of occurrences of σ i+1
in the sequence σ (i+1)..j , and moreover V(ρ) = V(ρ′ ).
Proof. By induction on the length m of the run.
    To define our restrictions for decidability we will make use of standard graph-
theoretic notions of reachability and simple cycles, defined concretely for our
formalisation of cyclic proofs as follows. If ν and ν ′ are nodes in a cyclic proof P,
and τ ∈ T(ν) and τ ′ ∈ T(ν ′ ) are left-hand (resp. right-hand) trace values, then
we say that (ν ′ , τ ′ ) is reachable from (ν, τ ) when there exists a path ν 1..n ∈ P
with ν 1 = ν and ν n = ν ′ that is followed by some left-hand (resp. right-hand)
trace τ 1..n with τ 1 = τ and τ n = τ ′ . We say that τ 1..n is a left (resp. right)
cycle along a path ν 1..n (n > 1) in P to mean that τ is a left-hand (resp. right-
hand) trace following ν such that ν 1 = ν n and τ 1 = τ n ; we say that the cycle
is rooted at ν 1 . Furthermore, we say that τ is a simple cycle when, for all
1 < i < j ≤ n, it is not the case that ν i = ν j and τ i = τ j . Notice that
these definitions exactly correspond with reachability and (simple) cycles in the
automata constructed from P. We extend slightly the notion of cycle and say
that the pair (τ 1..n , τ ′ 1..n ) is a binary cycle along a path ν 1..n when both τ and
τ ′ are cycles along ν. Similarly, (τ , τ ′ ) is a simple binary cycle when, for all
1 < i < j ≤ n, it is not the case that ν i = ν j , with τ i = τ j and τ ′ i = τ ′ j . In
this case notice that, individually, neither τ nor τ ′ need necessarily be simple
cycles along ν.
    We now come to describe the restrictions that we place on proofs in order
to obtain decidability of trace value ordering relations.
Definition 36. Let P be a cyclic proof; we say that, with respect to some given
node νinit in P and trace values τA ∈ TA (νinit ) and τC ∈ TC (νinit ), P is:
   i) left finitely progressing when for each edge (ν, ν ′ ) ∈ P and pair of left-
      hand trace values τ ∈ TA (ν) and τ ′ ∈ TA (ν ′ ) such that (ν, τ ) is reachable
                                                      ′                            ′
      from (νinit , τA ) and (ν, ν ′ ) ∈ dom(δ (ν,ν ) ), it is the case that δ (ν,ν ) (τ, τ ′ )
                                  (ν,ν ′ )      ′
      is a finite ordinal, i.e. δ          (τ, τ ) < ω. We define P to be right finitely
      progressing analogously, and say that P is simply finitely progressing when
      it is both left and right finitely progressing.
  ii) dynamic when it is the case that progν (τ ) > 0 for every left and right
      simple cycle τ along ν such that (ν 1 , τ 1 ) is reachable from (νinit , τA ) and
      (νinit , τC ) respectively.



                                             17
 iii) balanced when progν (τ ) = progν (τ ′ ) for every simple left binary cycle
      (τ 1..n , τ ′ 1..n ) along ν 1..n such that (ν 1 , τ 1 ) and (ν 1 , τ ′ 1 ) are both reachable
      from (νinit , τ A ).
    The first condition ensures that the automata we construct from P are sum
automata. The second and third conditions, along with the first, ensure com-
pleteness of the restricted automata for the trace value ordering relations. Note
that all three conditions are decidable, since there are only finitely many edges
and simple (binary) cycles in any given proof.
    We will show that when a proof P satisfies the above three conditions with
respect to some node ν and trace values τ ∈ TA (ν) and τ ′ ∈ TC (ν), then there
                                                       (P,ν)
exists some n such that LB(P,ν) ∼ LA (n)(P,ν) with B(τ,τ ′ ) grounded if and only
                                 (τ,τ ′ )         (τ,τ ′ )
if τ ′ ∼νP τ (for ∼ ∈ {<, ≤}). We will rely on two properties, which relate to
the trace width W(P) of P (defined above in the proof of lemma 32) and the
(binary left-hand) cycle threshold C(P) of P, which we define as the (necessarily
finite) number of distinct triples (τ, τ ′ , ν) such that ν ∈ nodes(P), τ ∈ TA (ν)
and τ ′ ∈ TA (ν). These properties are:
   1. Any (left- or right-hand) trace τ 1..n following a path ν 1..n containing
      strictly more than W(P) occurrences of some node ν must contain a
      simple cycle.
   2. Any pair (τ 1..n , τ ′ 1..n ) of left-hand traces following a path ν 1..n ∈ P such
      that n > C(P) must contain a simple binary cycle.
   In particular, under the conditions of definition 36, the latter property entails
that the difference between the size of two traces along some path is bounded.
                                                        (ν,ν ′ )
Let δmax (P) denote the maximum value in the set {δ1             (τ, τ ′ ) | (ν, ν ′ ) ∈ P}.
Lemma 37. Let P satisfy the conditions of definition 36 with respect to some
node ν and trace values τ ∈ TA (ν) and τ ′ ∈ TC (ν), and let τ 1..n and τ ′ 1..n be
left-hand traces rooted at ν following some path ν 1..n ∈ P; then

                      | progν (τ ) − progν (τ ′ )| ≤ C(P) × δmax (P)

Proof. By well-founded induction on the length n of the traces/path. We first
note that progν (τ ) − progν (τ ′ ) is well-defined (and an integer) since both
progν (τ ) and progν (τ ) are finite ordinals, which is guaranteed since P is finitely
progressing (condition (i) of definition 36).
(n ≤ C(P)): The result follows since in this case progν (τ ) and progν (τ ′ ) are
     both bounded by C(P) × δmax (P).
(n > C(P)): In this case, by the property ((2)) above, (τ , τ ′ ) must contain a
     simple binary cycle. Suppose w.l.o.g. that this cycle is (τ i..j , τ ′ i..j ). Since
     (τ i..j , τ ′ i..j ) is a cycle, by definition we have that ν i = ν j with τ i = τ j
     and τ ′ i = τ ′ j . Thus ν 1..i · ν (j+1)..n is also a path in P which, moreover,
     is followed by both τ 1..i · τ (j+1)..n and τ ′ 1..i · τ ′ (j+1)..n . All that we have


                                                18
done here is remove the cycle from the original path. Now, notice that
the length of ν 1..i · ν (j+1)..n is strictly less than n, thus by the inductive
hypothesis we have that

  | prog(ν 1..i ·ν (j+1)..n ) (τ 1..i · τ (j+1)..n )
                        − prog(ν 1..i ·ν (j+1)..n ) (τ ′ 1..i · τ ′ (j+1)..n )|
                                                                         ≤ (C(P) × δmax (P))
From definition 16, we have the following:
  prog(ν 1..i ·ν (j+1)..n ) (τ 1..i · τ (j+1)..n ) = progν j..n (τ j..n ) + progν 1..i (τ 1..i )
and
               prog(ν 1..i ·ν (j+1)..n ) (τ ′ 1..i · τ ′ (j+1)..n )
                                    = progν j..n (τ ′ j..n ) + progν 1..i (τ ′ 1..i )
Moreover,
         prog(ν 1..i ·ν (i+1)..j ·ν (j+1)..n ) (τ 1..i · τ (i+1)..j · τ (j+1)..n )
                   = progν j..n (τ j..n ) + progν i..j (τ i..j ) + progν 1..i (τ 1..i )
and
         prog(ν 1..i ·ν (i+1)..j ·ν (j+1)..n ) (τ ′ 1..i · τ ′ (i+1)..j · τ ′ (j+1)..n )
                = progν j..n (τ ′ j..n ) + progν i..j (τ ′ i..j ) + progν 1..i (τ ′ 1..i )
Finally, since P is balanced (condition (iii) of definition 36), we have that
progν i..j (τ i..j ) = progν i..j (τ i..j ), and so therefore

       progν 1..n (τ 1..n ) − progν 1..n (τ 1..n )
       = progν j..n (τ j..n ) + progν i..j (τ i..j ) + progν 1..i (τ 1..i )
               − (progν j..n (τ ′ j..n ) + progν i..j (τ ′ i..j ) + progν 1..i (τ ′ 1..i ))
        = progν j..n (τ j..n ) + progν 1..i (τ 1..i )
               − (progν j..n (τ ′ j..n ) + progν 1..i (τ ′ 1..i ))
                     + progν i..j (τ i..j ) − progν i..j (τ ′ i..j )
        = progν j..n (τ j..n ) + progν 1..i (τ 1..i )
                     − (progν j..n (τ ′ j..n ) + progν 1..i (τ ′ 1..i ))
        = prog(ν 1..i ·ν (j+1)..n ) (τ 1..i · τ (j+1)..n )
                     − prog(ν 1..i ·ν (j+1)..n ) (τ ′ 1..i · τ ′ (j+1)..n )
whence the result then follows.
    Notice that this last piece of equational reasoning above does not hold
in general when the size of the traces can be infinite ordinals; however it
does hold for finite ordinals (i.e. natural numbers).

                                              19
   We now prove that, under the conditions of definition 36, the problem of
deciding trace value ordering relations is equivalent to deciding containment
between finitely ambiguous weighted languages.
Theorem 38. If P satisfies the three conditions of definition 36 with respect to
some node ν and trace values τ ∈ TA (ν) and τ ′ ∈ TC (ν), then
                                                 (P,ν)
              LB(P,ν) ∼ LA (N )(P,ν) ∧ B(τ,τ ′ ) grounded ⇔ τ ′ ∼νP τ
                  (τ,τ ′ )       (τ,τ ′ )


where ∼ ∈ {<, ≤} and N = 2 + C(P) × δmax (P) × W(P) + W(P)
Proof. (⇒): Immediately from corollary 34 and theorem 28.
(⇐): Assume that τ ′ ∼νP τ ; it follows from theorem 28 that LB(P,ν) ∼ LA (P,ν)
                                                                        (τ,τ ′ )           (τ,τ ′ )
               (P,ν)
     and that B(τ,τ ′ ) is grounded. To show that LB(P,ν) ∼ LA (N )(P,ν) , take an
                                                        ′    (τ,τ )    ′    (τ,τ )
                                            σ            (P,ν)
     arbitrary accepting run ρ : q −−1..n
                                      −→ qn of B(τ,τ ′ ) . Since LB(P,ν) ∼ LA (P,ν) ,
                                                                        (τ,τ ′ )           (τ,τ ′ )
                                                                  σ                (P,ν)
                                                              −→ qn′ of A(τ,τ ′ ) such
     it follows that there is also an accepting run ρ′ : q −−1..n
     that V(ρ) ∼ V(ρ′ ). We now consider the following two exhaustive cases:
                              ′
         - If there is no qi+1    = ⊤ (0 < i < n), or the number k of occurrences
                                                                              ′
     of σ i+1 in the sequence σ (i+1)..n , where i is the least such that qi+1   = ⊤,
     is strictly less than N , then we have immediately by lemma 35 that there
                        σ                 (P,ν)
                          −→ qn′′ of A (m)(τ,τ ′ ) for all m > 0 or m > k respectively,
     is a run q ′′ : q −−1..n
     such that V(ρ′ ) = V(ρ′′ ). Either way, this holds for for m = N > k ≥ 0 in
     particular.
            - We have k ≥ N , with k the number of occurrences of σ i+1 in the
                                                                     ′
     sequence σ (i+1)..n where i is the least such that qi+1            = ⊤. In this case,
                                                              σ            (P,ν)
     we show that there also exists a run ρ′′ : q −−−→ qn′′ of A(τ,τ ′ ) such that
                                                                1..n


     V(ρ′ ) ≤ V(ρ′′ ) and the number k ′ of occurrences of σ j+1 in the sequence
     σ (j+1)..n , where j is the least such that qj′′ = ⊤, satisfies k ′ < N .
            Firstly, notice that each element of σ is a node in P, thus in the
     remainder of this case we shall write σ 1..n as ν 1..n . Notice also that we
     can construct a left-hand trace τ 1..i (beginning with τ ) from the states
     q1′ , . . . , qi′ , since qm
                                ′
                                  = (ν m , τ m ) for each m ≤ i. Then we have by lemma 25
     that τ 1..i follows ν 1..n and V(ρ′ ) = progν (τ ). Similarly, we can construct
     a right-hand trace τ ′ 1..n (beginning with at τ ′ ) from the states of ρ which,
     by lemma 26, also follows ν 1..n and for which V(ρ) = progν (τ ′ ). Notice
     that since ρ is an accepting run, by corollary 27, τ ′ is also a positive
     maximal right-hand trace.
            Now, there are k ≥ N > W(P) occurrences of ν i+1 in the sequence
     ν (i+1)..n . Let ν m..n be the (smallest) path which is a tail of ν 1..n contain-
     ing W(P) + 1 occurrences of ν i+1 . By property (1) above, τ ′ m..n must
     contain a simple cycle, say τ ′ r..s (with m ≤ r < s ≤ n). Since P is both
     dynamic and finitely progressing we have that 0 < progν r..s (τ ′ r..s ) < ω.

                                                20
     This means that, via a ‘pumping’ construction, we can build a path in P
     followed by a positive maximal right-hand trace whose size is arbitrarily
     (finitely) large, as follows:
                                   arbitrarily many occurrences of ν (r+1)..s
                                                 z     }|        {
                          path:         ν 1..r · ν (r+1)..s · . . . · ν (s+1)..n
                          trace:        τ ′1..r · τ ′(r+1)..s · . . . · τ ′(s+1)..n
                                                  |      {z        }
                               matching number of occurrences of τ ′ (r+1)..s

      In particular, there exists such a path ν ′ followed by such a trace τ ′′ with
      progν ′ (τ ′′ ) ≥ δmax (P) × s. Since τ ′ ∼νP τ , there must exist a left-hand
      trace τ ′′′ 1..t following ν ′ such that progν ′ (τ ′′′ ) ≥ progν ′ (τ ′′ ). Crucially,
      since progν ′ (τ ′′′ ) ≥ δmax (P) × s, it must be that t ≥ s. Consequently,
      τ ′′′ 1..s follows ν 1..n .
            To complete the case, we note the following. First, by lemma 37, we
      have that | progν (τ 1..i ) − progν (τ ′′′ 1..i )| ≤ C(P) × δmax (P). Second, there
      are at least 1 + C(P) × δmax (P) × W(P) occurrences of ν i+1 in the path
      ν (i+1)..(m−1) . This means, again by property (1) above, that there are (at
      least) C(P) × δmax (P) basic cycles in the left-hand trace τ ′′′ (i+1)..(m−1) .
      Since P is dynamic it then follows that progν (i+1)..(m−1) (τ ′′′ (i+1)..(m−1) ) ≥
      C(P) × δmax (P), and therefore it must be that progν (τ ′′′ 1..(m−1) ) ≥
                                                                                   ν
      progν (τ 1..i ). Finally, by lemma 25, there exists a run ρ′′′ : q −−1..n      −→ qn′′′
               (P,ν)
      of A(τ,τ ′ ) with qu′′′ = (ν u , τ ′′′ u ) for each u < m; moreover we may as-
      sume without loss of generality that qu′′′ = ⊤ for m ≤ u ≤ n, since the
      automaton may transition to the ⊤ state at any point. Hence, V(ρ′′′ ) =
      progν (τ ′′′ 1..(m−1) ) ≥ progν (τ 1..i ) = V(ρ′ ). Notice that ν m is an occur-
      rence of ν i+1 , and that there must necessarily be fewer than N occurrences
      of ν i+1 in the path ν m..n . Thus, by lemma 35, it follows that there is a
                     ν                  (P,ν)
                       −→ qn′′ of A (N )(τ,τ ′ ) with V(ρ′′ ) = V(ρ′′′ ) ≥ V(ρ′ ).
      run ρ′′ : q −−1..n
                                                    σ                       (P,ν)
                                              −→ qn′′ of A (N )(τ,τ ′ ) such that V(ρ) ∼
     In both cases, we have a run q ′′ : q −−1..n
     V(ρ′ ) ≤ V(ρ′′ ). Notice that, by construction, this must be an accepting
     run, and so V(ρ′′ ) ≤ LA (N )(P,ν) (σ 1..n ), whence the result follows.
                                        (τ,τ ′ )


   Finally therefore, as a corollary, we may decide trace value relations.
Corollary 39. If P satisfies the three conditions of definition 36 with respect
to some node ν and trace values τ ∈ TA (ν) and τ ′ ∈ TC (ν), then it is decidable
whether or not τ ′ ∼νP τ holds.
                                                                                      (P,ν)
Proof. As stated previously, we may decide whether an automaton B(τ,τ ′ ) is
grounded or not, and whether the conditions of definition 36 hold with respect
to ν, τ and τ ′ . Under the conditions of definition 36, the weighted automata
      (P,ν)        (P,ν)
A (n)(τ,τ ′ ) and B(τ,τ ′ ) are finitely ambiguous sum automata, for which contain-
ment is decidable [6]. Decidability of τ ′ ∼νP τ then follows from theorem 38.

                                                   21
References
[1] Shaull Almagor, Udi Boker, and Orna Kupferman. What’s Decidable about
    Weighted Automata? In Proceedings of ATVA-9, volume 6996 of LNCS,
    pages 482–491. Springer-Verlag, 2011.
[2] James Brotherston. Cyclic Proofs for First-Order Logic with Inductive Def-
    initions. In Proceedings of TABLEAUX-14, volume 3702 of LNAI, pages
    78–92. Springer-Verlag, 2005.
[3] James Brotherston. Formalised Inductive Reasoning in the Logic of Bunched
    Implications. In Proceedings of SAS-14, volume 4634 of LNCS, pages 87–103.
    Springer-Verlag, 2007.
[4] James Brotherston and Alex Simpson. Sequent Calculi for Induction and
    Infinite Descent. Journal of Logic and Computation, 21(6):1177–1216, De-
    cember 2011.
[5] Manfred Droste, Werner Kuich, and Heiko Vogler. Handbook of Weighted
    Automata. Monographs in Theoretical Computer Science. An EATCS Series.
    Springer-Verlag, 2009.
[6] Emmanuel Filiot, Raffaella Gentilini, and Jean-François Raskin. Finite-
    Valued Weighted Automata. In Proceedings of FSTTCS-34, volume 29 of
    LIPICS, pages 133–145, 2014.
[7] Daniel Krob. The Equality Problem for Rational Series with Multiplicities
    in the Tropical Semiring is Undecidable. IJAC, 4(3):405–426, 1994.
[8] Andreas Weber and Helmut Seidl. On the Degree of Ambiguity of Finite
    Automata. Theor. Comput. Sci., 88(2):325–349, 1991.




                                     22
