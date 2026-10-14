                                                                                   Circular Induction

                                                           Dorel Lucanu1 , Grigore Roşu2 , Eugen Goriac1 , and Georgiana Caltais1
                                                                                    1
                                                                                      Faculty of Computer Science
                                                        Alexandru Ioan Cuza University, Iaşi, Romania, [dlucanu,egoriac]@info.uaic.ro
                                                                                 2
                                                                                   Department of Computer Science
                                                             University of Illinois at Urbana-Champaign, USA, grosu@illinois.edu



                                                Abstract. The Circularity Principle was successfully applied for developing a coinductive proving
                                                technique, known as circular coinduction. In this paper we show that the same principle can be
                                                used to develop an inductive proving technique. A main advantage of this uniform approach is
                                                that the two proving techniques can be easily combined during the verification process. Circular
arXiv:2605.24968v1 [cs.LO] 24 May 2026




                                                induction is simple, flexible, generic, and therefore it is a good candidate framework for combining
                                                different proving schemes into a competitive tool. We exhibit this potential by presenting how the
                                                circular induction is implemented in CIRC, a prover built around the Circularity Principle.
                                                Disclaimer. This paper was written in 2010, at the time the CIRC prover was developed, and the
                                                main body reflects the state of the work and of the prover as of that date. For this arXiv technical
                                                report, only the related-work discussion (Section 6) and the concluding section have been revised:
                                                Section 6 has been extended to situate circular induction within the cyclic-proof and infinite-descent
                                                literature that has appeared or matured since 2010. No other part of the paper—its definitions,
                                                results, proofs, examples, or implementation description—has been modified, and the technical
                                                content should be read as a 2010 contribution. References to developments after 2010 appear only
                                                in the updated related-work section.


                                         1     Introduction

                                         Circular coinduction [20] is a coinductive proving technique for behavioral properties. By a behavioral
                                         property we mean a property which can be experimentally evaluated. The soundness of the circular
                                         coinduction can be explained, among other interpretations, by a graph whose equalities from nodes can
                                         be regarded as lemmas inferred in order to prove the original task, and the graph itself as a dependence
                                         relation among these lemmas; one can take all these and produce a parallel proof. We exemplify this
                                         technique proving a very simple property over streams (infinite lists). Let zeros be the streams of 0’s (=
                                         0 : 0 : 0 : . . .), ones the stream of 1’s, oz the stream 0 : 1 : 0 : 1 . . ., zo the stream 1 : 0 : 1 : 0 . . ., and let
                                         zip(S , S ′ ) be the operation which is zipping two streams. The formal definitions for these streams are
                                         given by the following corecursive equations:
                                                                 zeros = 0 : zeros                                            zo = 0 : oz
                                                                                        zip(a : S , S ′ ) = a : zip(S ′ , S )
                                                                 ones = 1 : ones                                              oz = 1 : zo
                                         We consider the destructors hd (head) and tl (tail) defined by hd (a : S ) = a and tl (a : S ) = S . The
                                         two destructors define two derivatives hd (∗:Stream) and tl (∗:Stream), which can be seen as equation
                                         transformers: an equation S = S ′ over streams is transformed into hd (S ) = hd (S ′ ) and tl (S ) = tl (S ′ ),
                                         respectively. The proof tree of the property zip(zeros, ones) = zo by circular coinduction is represented
                                         in Fig. 1. The head derivative produces a new property (equation), which can be immediately proved
                                         using the definition of the operations. The tail derivative produces a new lemma, which is processed
                                         in the same way. Again, the property produced by the head derivative is immediately proved. The tail
                                         derivative produces exactly the initial property, so there is no reason to continue because we ended into
                                         a circularity. For the general case, the circularity is modulo a substitution and/or special contexts.
                                           In this paper we exploit this viewpoint in order to develop a similar inductive proving technique. We
                                         start to explain this technique using a simple example. Let us consider the following two definitions for
                                         even, one iterative and the other one mutual (using odd):3
                                                     even(0 ) = true             evenm(0 ) = true           oddm(0 ) = false
                                                     even(s(0 )) = false
                                                     even(s(s(N ))) = even(N ) evenm(s(N )) = oddm(N ) oddm(s(N )) = evenm(N )
                                         3
                                             This example is from Induction Challenge Problems site: http://www.cs.nott.ac.uk/~lad/research/
                                             challenges/
                                            zip(zeros, ones) = zo

                                           hd                           tl


                  hd (zip(zeros, ones)) = hd (zo)                  tl (zip(zeros, ones)) = tl (zo)
                             0 =0 ✓                                     zip(ones, zeros) = oz

                                                                      hd                     tl


                                        hd (zip(ones, zeros)) = hd (oz )              tl (zip(ones, zeros)) = tl (oz )
                                                   1 = 1✓                                  zip(zeros, ones) = zo

                                  Fig. 1. Intuitive proof by circular induction


                                  even(n) = evenm(n)

                                    0                       s( )                  n2 ∼ n


                  even(0 ) = evenm(0 )              even(s(n1 )) = evenm(s(n1 ))
                     true = true ✓                    even(s(n1 )) = oddm(n1 )

                                                        0                             s( )


                                 even(s(0 )) = oddm(0 )                           even(s(s(n2 ))) = oddm(s(n2 ))
                                     false = false✓                                  even(n2 ) = evenm(n2 )

                                  Fig. 2. Intuitive proof by circular induction



The proof of the conjecture (∀N )even(N ) = evenm(N ) is intuitively represented by the graph in Figure
2. The constructors of naturals, 0 and s( ), can be seen as properties (here equalities) transformers,
by applying an appropriate substitution over an inductive variable. These transformers obtained from
constructors are called derivatives. The initial goal is transformed by derivatives into two new proof
obligations: even(0 ) = evenm(0 ) and even(s(n1 )) = evenm(s(n1 )).The former is reduced using the
axioms from the specification and the latter is simplified to a simpler goal; this is then derived into
two new proof obligations: even(s(0 )) = oddm(0 ) and even(s(s(n2 ))) = oddm(s(n2 )). Again the former is
reduced using the axioms; the latter is very ”similar” to initial goal (the similarity is expressed by n2 ∼ n
meaning that ”n2 is an incarnation of n and therefore satisfies the same properties as n), so there is no
reason to continue the proving process, and we may conclude that property holds. The composition of
the derivatives produces experiments. We may say that the property above was proved using only three
such derivations because we ended up into a cycle. It is easy to see now that this proof technique is very
similar to the one applied for circular coinduction.
   In this paper we formalize the above exemplified proof technique following the line from [22, 20]. We
introduce notions like derivative, experiment, freezing operator, special hypothesis suitable for inductive
properties, and we show that the circularity principle holds for the new framework. Then we define the
circular induction proof calculus based on this principle. Since both circular coinduction and circular
induction are presented at a generic level, parameterized in the basic entailment relation, many proofs
from circular coinduction are reused for circular induction by duality. This strengthens our belief that
the circularity principle is a foundation for combining different proving paradigms into a powerful prover.
We exemplify that by showing how the two mentioned proving techniques are implemented in CIRC. We
present in Figure 3 the correspondence between the similar concepts, which are expressing in fact the
duality between the two paradigms. We illustrate the concepts using streams (for circular coinduction)
and natural numbers (for circular induction), as canonical examples for two approaches.
   We regard circular induction as a rather complementary inductive proving technique which can con-
tribute to the development of more powerful automated provers. The main advantages of the circular
induction are its simplicity - only two inference rules, no explicit well-ordering, no algorithm for computing
cover/test sets, flexibility - it can be combined with other proving techniques, e.g., circular coinduction,
or disproving techniques using simplification rules [16] or decision procedures, generality - it is parametric


                                                            2
                               Circular coinduction                   Circular induction
              sorts            hidden (coinductive),                  inductive (initial),
                               visible (non-coinductive)              non-inductive (loose)
              derivatives ∆    destructor (context)                   constructor (substitution)
                               hd (∗:Stream), tl (∗:Stream) 0.Nat, s(N :Nat)
              derived equation δ[t] = δ[t′ ]                          δc [t] = δc [t′ ]
                               hd (t) = hd (t ′ ), tl (t) = tl (t ′ ) t[0/y:Nat] = t′ [0/y:Nat],
                                                                      t[s(y:Nat)/y:Nat] = t′ [s(y:Nat)/y:Nat]
              ∆-experiment     visible ∆-context                      ground ∆-substitution
              freezing         at top        inhibits                 at bottom             inhibits
                               t 7→ t        contexts                 N :Nat 7→ N.Nat substitutions
              frozen equation t = t′                                  t[y.s/y:s] = t′ [y.s/y:s]
                       Fig. 3. Duality between circular coinduction and circular induction

in the basic entailment relation, which allows using circular induction as framework suitable to combine
more proving techniques.
   The structure of the paper is as follows. In Section 2 we present some preliminary notions used through-
out the paper, including a brief recall of the circular coinduction in order to facilitate the comparison
of the two proof techniques. Section 3 shows how inductive consequences can be regarded as behavioral
properties. Section 4 is dedicated to presenting the circular induction principle and the circular induction
proof calculus. In Section 5 we show how circular induction is implemented in CIRC and how the two
proof techniques, circular coinduction and circular induction may work together. Section 6 discusses the
related work and Section 7 concludes the paper and outlines future work.


2     Preliminaries

We assume the reader familiar with the basics of many sorted algebraic specifications and only briefly
recall our notation. An algebraic specification, or simply a specification, is a triple (S, Σ, E), where S is a
set of sorts, Σ is a (S ∗ ×S)-signature and E is a set of Σ-equations of the form (∀X) t = t′ if ∧i∈I ui = vi
with t, t′ , ui , and vi Σ-terms with variables in X, i = 0, . . . , n; the pair t, t′ and each pair ui , vi for
each i ∈ I, have, respectively, the same sort. If the sort of t and t′ is s we may say that the sort of
the equation is also s. When i = 0 we call the equation unconditional and omit the condition (i.e.,
write it (∀X) t = t′ ). When X = ∅ we drop the quantifier and call the equation ground. An equational
transformer is a mapping δ which maps a Σ-equation e into a S          set of Σ-equations δ[e].SIf ∆ is a set of
equational transformers and E a set of equations, then ∆[e] = δ∈∆ δ[e] and ∆[E] = e∈E ∆[e]. The
following introduces the notion of basic entailment relation used by both circular proof techniques.

Definition 1. Let (S, (Σ, ∆)) be a signature with equational transformers. A ∆-contextual entailment
system is an (infix) relation ⊢ between sets of equations and equations, with:

1. (reflexivity) {e} ⊢ e;
2. (monotonicity) If E1 ⊇ E2 and E2 ⊢ e then E1 ⊢ e;
3. (transitivity) If E1 ⊢ E2 and E2 ⊢ e then E1 ⊢ e;
4. and (∆-congruence) If E ⊢ e then E ⊢ ∆[e].

  Above, E, E1 , E2 range over sets of equations and e over equations; we tacitly extended ⊢ to sets of
equations as expected: E1 ⊢ E2 iff E1 ⊢ e for any e ∈ E2 .

    If B = (S, (Σ, ∆), E) is a specification with equational transformers, we often write B ⊢ e for E ⊢ e.


2.1    Behavioral Coinductive Specifications and Circular Coinduction

By behavioral properties we mean those properties which can be proved using experiments: a behavioral
property e holds if and only if it cannot be disproved by experiments, i.e., for each experiment C, the
instance of e corresponding to C, usually written as C[e], holds. In this section we briefly recall the
notion of behavioral specification and circular coinduction proof system; this will help us to compare and
emphasize the duality of the two proof systems. For more details, the reader is invited to read [22, 20].


                                                             3
  A Σ-context for the sort s is a term δ[∗:s] having a single occurrence of the distinguished variable
∗:s. If δ[∗:s] is a context and t a Σ-term of sort s, then δ[t] denotes the term t where the variable
∗:s is substituted with t. A Σ-context can be seen as an equational transformer, where δ[e] is the
equation (∀X) δ[t] = δ[t′ ] if ∧i∈I ui = vi . A behavioral coinductive signature (S, (Σ, ∆)) is a signature
(S, Σ) together with a set ∆ of Σ-contexts viewed as equational transformers, called derivatives. The
derivatives δ[∗:s] ∈ ∆ are also known as destructors. A sort s occurring into a derivative δ[∗:s] is called
hidden; the other sorts are called visible. Therefore, the sorts S are partitioned into two subsets: the
subset of hidden sorts H and the subset of visible sorts V . The set of ∆-experiments is inductively
defined as follows: 1) any visible derivative δ[∗:h] is an experiment for h ∈ H, and 2) if C[∗:h] is an
experiment for h and δ[∗:h′ ] is a derivative of sort h (and for h′ ), then C[δ[∗:h′ ]] is an experiment for h′ .
A behavioral coinductive specification B is a triple (S, (Σ, ∆), E), where (S, (Σ, ∆)) is a behavioral
coinductive signature and E is a set of Σ-equations. In the rest of this section, B denotes a behavioral
coinductive specification as above and ⊢ a ∆-contextual entailment relation.

Definition 2. B behaviorally satisfies equation e, written B ⊪ e, iff: B ⊢ e if e is visible, and B ⊢ C[e]
for each appropriate experiment C if e is hidden.

Example 1. The behavioral coinductive specification STREAM of streams discussed in Section 1, consists
of a hidden sort Stream for streams, a visible sort Bit for data elements, a set of operations among
which we point out the head hd : Stream → Bit and tl : Stream → Stream, and a set of equations
defining the other operations (zeros, ones, zip . . . ) in terms of head and tail. The set ∆ of derivatives
is {hd (∗:Stream), tl (∗:Stream)} and the experiments one can perform on streams are therefore contexts
of the form hd (tl i (∗:Stream)), where i ≥ 0. The basic entailment relation is given by the conventional
equational reasoning; in other words, STREAM ⊢ e iff e is derivable using equational reasoning from
the equations in STREAM .

  A key notion in the definition of circular coinduction proof system is that of a “frozen” equation.
The motivation underlying frozen equations is that they structurally inhibit their use underneath proper
contexts; because of that, they will allow us to capture the informal notion of “circular behavior”.
Formally, the signature Σ is extended with a new sort Frozen and a new operation - : s → Frozen for
each sort s. If t is a term, then we call t the frozen (form of ) t. If e is an equation (∀X) t = t′ if c, then
we let e be the frozen equation (∀X) t = t′ if c; note that the condition c stays unfrozen, but recall
that we only assume visible conditions. The equations over the original signature Σ are called unfrozen
equations.

Definition 3. A ∆-contextual entailment system with freezing is a ∆-contextual entailment sys-
tem such that:

  (A1) E ∪ F ⊢ e      iff E ⊢ e;
  (A2) E ∪ F ⊢ G implies E ∪ δ[F ] ⊢ δ[G] for each δ ∈ ∆,
    where E ranges over unfrozen equations, e over visible unfrozen equations, and F and G over
    frozen hidden equations.

   However, the freezing operator is too restrictive. There are contexts under which is safe to use the
frozen hypothesis; these are called special contexts. The formal definition is technical and can be found in
[20]. Obviously, a special context does not include derivatives. For the example of streams, the contexts
zip(∗:Stream, S ) and zip(S , ∗:Stream) are special, whereas odd (∗:Stream) is not special, where odd :
Stream → Stream is defined by hd (odd (S )) = hd (S ) and tl(odd(S)) = odd(tl(tl(S))) ( a counterexample
can be found in [14, 20]). Each special context γ[∗:s] defines an equation transformer similar to derivatives.

Definition 4. The circular coinduction proof system consists of the following inference rules, rep-
resented as conditional reduction rules:

    [Reduce]: (B, F, G ∪ { e }) ⇒ (B, F, G) if B ∪ F ⊢ e
    [Derive]: (B, F, G ∪ { e }) ⇒ (B, F ∪ { e } ∪ Γ [e], G ∪ { ∆[e] })
               if B ∪ F ̸⊢ e ∧ e is hidden

where F a set of frozen hypotheses, G is a set of goals represented also as frozen equations, and Γ is a
set of special contexts.


                                                        4
   The rule [Reduce] says that if the current goal is a ⊢–consequence of B ∪ F then e is dropped. When
the current goal e is hidden and it is not a ⊢–consequence, it and the equations defined by the special
contexts over it are added to the specification and its derivatives to the set of goals using the rule [Derive].
The proof of zip(zeros, ones) = zo given in Section 1 is obtained with the above system, where all the
equations should be considered frozen. Without freezing the added hypotheses, we can wrongly deduce,
e.g., that zeros = oz .


2.2   Inductive Specifications

A signature with constructors is a pair (S, (Σ, Σ ctor )), where (S, Σ) is a many sorted signature and
Σ ctor ⊆ Σ is the subsignature of constructors. A sort s is called inductive sort if there is a constructor
of sort s. An inductive variable is a variable of inductive sort. A goal (conjecture) is a conditional
equation written as (∀Y )(∀Z)t = t′ if cond, where Y is a set of inductive variables. If θ : Y → TΣ ctor
is a constructor ground substitution, then θ[e] denotes the equation (∀∅)(∀Z)t = t′ if cond. A goal e
is an (equational) inductive consequence of the specification (S, (Σ, Σ ctor ), E), if (S, Σ, E) satisfies
in the equational deduction system all constructor ground instances θ[e]. More details about inductive
consequences can be found, e.g., in [6].
  In order to exhibit the concepts and results presented in this paper, we consider the following examples.

Example 2. (Sum of natural numbers)
The specification NATSUM, defining natural numbers, consists of a sort Nat, two constructors 0 : → Nat
and s : Nat → Nat, an operator sum : Nat Nat → Nat defined by the equations sum(M , 0 ) = 0 ,
sum(M , s(N )) = s(sum(M , N )). We will exhibit how the commutativity and associativity of sum can
be automatically proved with the basic circular induction proof system; two new lemmas are discov-
ered during the proof process: sum(0 , M ) = M and sum(s(M ), N ) = s(sum(M, N )). The goal ex-
pressing the associativity is given by the unconditional equation (∀P )(∀M , N )sum(M , sum(N , P )) =
sum(sum(M , N ), P ), where only P is viewed as an inductive variable for this goal. In order to exemplify
how non-linear goals are handled, we use a max operator defined by max (M , 0 ) = M , max (0 , s(N )) =
s(N ), max (s(M ), s(N )) = s(max (M , N )), and we show that the non-linear goal max (N , N ) = N is
automatically proved in exactly one derivation step.

Example 3. (Generic trees)
This example exhibits inductive properties over generic data types defined using the mutual recursion
and the case when a constructor could have more than one inductive parameter. The specification TREE
includes the inductive definition of trees built over a parameter data type Elt and where a node has a
list of children. The lists are defined using a sort TList and the constructors
                    nil : → TList          [ ] : Tree → TList      ; : TList TList → TList
Note that the concatenation is defined as a constructor; it replaces the usual constructor cons : Tree TList →
TList. We made this choice because we want to exhibit how the nonlinear conjectures are handled in
more complex examples. The trees are defined using the sort Tree and the constructors
                                  [ ] : Elt → Tree        tr : Elt TList → Tree
We further consider the mirroring operation defined by
              mirror (nil ) = nil                             mirror ([E ]) = [E ]
              mirror ([T ]) = [mirror (T )]
              mirror (L1 ; L2 ) = mirror (L2 ); mirror (L1 ) mirror (tr (E , L)) = tr (E , mirror (L))
We show how the goal mirror (mirror (L:TList)) = L:TList is automatically proved by circular induction.
Note that the property can only be proved together with mirror (mirror (T :Tree)) = T :Tree, which is
automatically discovered using the help of the first goal.

Example 4. (Fibonacci sequence)
The specification FIB includes the definition of the Fibonacci sequence. The definition of the natural
numbers consists of a sort Nat and two constructors 0 : → Nat and s : Nat → Nat. We also consider
an associative and commutative operator + : Nat Nat → Nat defined by the equations M + 0 = 0,
M + s(N )) = s(M + N ). The definition of Fibonacci sequence is given by
                     fib(0) = 0 fib(s(0)) = s(0) fib(s(s(N ))) = fib(s(N )) + fib(N )
and the definition of the number of calls of + is given by


                                                       5
                np(0) = np(s(0)) = 0     np(s(s(N ))) = np(s(N )) + np(N ) + s(0)
                        PN
We exhibit how the goal k=0 fib(k) = np(s(N )) can be proved with the enhanced circular induction
proof system implemented in CIRC.


3     Inductive Consequences are Behavioral Properties

In this section we show that the inductive consequences can be viewed as behavioral properties, i.e.,
we can define notions like experiments and derivatives, which satisfy the same properties as for the
coinductive case, and define the inductive satisfaction similarly to behavioral coinductive satisfaction.

Definition 5. Let (S, (Σ, Σ ctor )) be a signature with constructors. Each constructor c ∈ Σ ctor defines
a derivative (equational transformer) δc = {δc,y } as follows: if e is (∀Y )(∀Z)t = t′ if cond then

 – δc,y [e] is (∀Y \ {y})(∀Z)t[c/y] = t′ [c/y] if cond[c/y] for each y ∈ Y and constructor constant c having
   the same sort as that of y;
 – δc,y [e] is (∀Y \ {y} ∪ {y1 , . . . , yn })(∀Z)t[u/y] = t′ [u/y] if cond[u/y] for each y ∈ Y of sort s and
   c : s1 . . . sn → s, where u = c(y1 , . . . , yn ) and yi is a fresh variable of sort si for i = 1, . . . , n; in this
   case we write yi ∼ y for each i such that si = s (yi can be seen as a new incarnation of y);
 – δc [e] = {δc,y [e] | y ∈ Y ∧ sort(c) = sort(y)} for each c ∈ Σ ctor .
 – ∆ = ∪c∈Σ ctor δc .

Example 5. Let us consider the specification TREE defined in Example 3. If e is mirror (mirror (T :
Tree)) = T : Tree and c is tr (E :Elt, L:TList), then δc [ e ] consists of mirror (mirror (tr (E , L))) =
tr (E , L). If e is mirror (mirror (L : TList)) = L and c is L1 :TList; L2 :TList, then δc [ e ] consists of
mirror (mirror (L1 ; L2 )) = L1 ; L2 and L ∼ L1 and L ∼ L2 .

  The relation ∼ between frozen variables plays also a key role in the definition of the circular induction
proof system.

Proposition 1. Let e be an equation (∀Y )(∀Z)t = t′ if cond and let θ : Y → TΣ ctor be a ground Σ ctor -
substitution. Then there exist certain constructors (not necessarily distinct) c1 , . . . , cn and inductive
variables y1 , . . . , yn such that Y ⊆ {y1 , . . . , yn } and θ[e] = δc1 ,y1 [. . . δcn ,yn [e] . . .].

Proof. Let der (θ)[e] denote the equation inductively defined as follows:

 – if Y = {y} and θ(y) is a constant c, then der (θ)[e] is δc,y [e];
 – if Y = {y} and θ(y) = c(u1 , . . . , un ), then der (θ)[e] is der (θ′ )[δc,y [e]], where θ′ : {y1 , . . . , yn } → TΣ ctor
   and θ′ (yi ) = ui for i = 1, . . . , n;
 – if Y = Y ′ ∪ {y}, then der (θ)[e] is der (θ|Y )[der (θ|{y} )[e]].

It is easy to check that θ[e] and der (θ)[e] are the same and der (θ)[e] has the shape asked by the conclusion.
                                                                                                             ⊔
                                                                                                             ⊓

    For instance, if e is (∀N )max (N, N ) = N and θ(N ) = s(0), then θ[e] is the same with δ0 [δs [e]].
  Proposition 1 says that the ground Σ ctor -substitutions are in fact experiments and can be inductively
defined in a similar way to the coinductive case.

Definition 6. An experiment for the inductive variable y is defined as follows:

 – if c ∈ Σ ctor of sort s and y is an inductive variable of sort s, then δc,y [•] is an experiment for y (it
   designates the substitution y 7→ c);
 – if (c : s1 . . . sn → s) ∈ Σ ctor , y is an inductive variable of sort s, and θi is an experiment for yi of sort
   si (designating the substitution yi 7→ ti ), then [θ1 , . . . , θn ][δc,y [•]] is an experiment for y (designating
   the substitution y 7→ c(t1 , . . . , tn );
 – an experiment for a set of inductive variable Y consists of a experiment θ for each y ∈ Y .


                                                             6
The notation [θ1 , . . . , θn ][•] is a shorthand for θ1 [. . . [θn [•]] . . .] (or an equivalent one because the order
we compose θi does not matter).

It is worth noting to emphasize the duality between the two notions of experiment: for the coinductive
case it is a context for a hidden sort, for the inductive case it is a substitution for a set of inductive
sorts. The inductive definition of the experiments and their view as equation transformers are fully
exploited by circular induction proof system we define later. From now on we often write (S, (Σ, ∆)) for
(S, (Σ, Σ ctor )) in order to have a uniform notation and to stress that a signature with constructors defines
a set of equational transformers. This double notation is not confusing because if we know Σ ctor then
we can compute ∆ and, reciprocally, if we know ∆ then we can compute Σ ctor and [•] is a placeholder
for equations. Having defined ∆, it does make sense to consider ∆-contextual entailment systems ⊢ for
the signature with constructors, and define inductive consequences parameterized over these systems,
similar it is done for coinductive behavioral consequences.

Definition 7. Let B = (S, (Σ, ∆), E) be a specification with constructors and let e be an equation
(∀Y )(∀Z)t = t′ if cond. We say that B inductively satisfies e, written B ⊪ e, if B ⊢ θ[e] for each
experiment θ for Y .


4     Circular Induction

Similar to circular coinduction, a key notion for circular induction is that of frozen equation. If for the
case of circular coinduction, the frozen equations inhibit the use of the frozen equations ”underneath”
proper contexts, for circular induction the frozen equation inhibit their use ”over” proper substitution.
The frozen equations help us to capture the informal notion of ”circular inductive reasoning” elegantly,
rigorously, and generally (modulo a restricted form of equational reasoning).

Definition 8. 1. A frozen form of a variable y:s is a distinguished constant y.s of sort s.
2. A frozen form of a goal e ≡ (∀Y )(∀Z)t = t′ if cond is the equation e ≡ (∀∅)(∀Z)t = t′ if cond,
where the inductive variables Y are replaced with their frozen forms.
3. The set of frozen variables of a goal e is FVar ( e ) = {y.s | y:s ∈ Y }.
4. If F is a set of goals, then F = { e | e ∈ F } and FVar ( F ) = ∪e∈F FVar ( e ).

    Let δc be a derivative, e a goal, and F a set of goals . Then we write δc,y [ e ] for δc,y [e] , δc [ e ] for
δc [e] , ∆[ e ] for ∆[e] , and ∆[ F ] for ∆[F ] . If θ is an experiment and Θ is a set of experiments, then
θ[ e ] = θ[e] , θ[ F ] = {θ[ e ] | e ∈ F }, and Θ[ F ] = ∪θ∈Θ θ[ F ].
   Let (S, Σ, E) ∪ F ⊢ e denote the entailment relation (S, Σ(YF ∪ Ye ), E ∪ F ) ⊢ e , where YF is the set
of the all designated inductive variables of the equations F , Ye is the set of the all designated inductive
variables of e, and Σ(Y ) is the signature Σ enriched with the frozen forms of the variables Y (recall that
these are constants). The following is an adaptation of Definition 3 for the case of derivatives defined by
constructors.

Definition 9. Let (S, (Σ, ∆)) be a signature together with the associated derivatives. A ∆-contextual
entailment system with freezing is a ∆-contextual entailment ⊢ satisfying the following two assump-
tions:
(A1) (S, Σ, E) ∪ F ⊢ e iff (S, Σ, E) ⊢ e if e is an equation without frozen variables.
(A2) if (S, Σ, E) ∪ F ⊢ G then (S, Σ, E) ∪ δc [ F ] ⊢ δc [ G ].

    If ⊢ is the equational deduction, then the axioms (A1) and (A2) are satisfied. If e has no inductive
variables then obviously no axiom from F is used in the inference of e . The proof of a goal g [δc /y.s] ∈
δc [ G ] from (S, Σ, E) ∪ δc [ F ] is obtained from a proof of g from (S, Σ, E) ∪ F by replacing each equation
e from this proof with e[δc /y.s].

Theorem 1. (circular induction principle)
Let B = (S, (Σ, ∆), E) be a specification and F be a set of goals. If B ∪ F ⊢ ∆[ F ] then B ⊪ F .


                                                          7
Proof. Since both the circular coinduction and circular induction are defined over entailment relations
and dual freezing operators satisfying the same properties, we may reuse the proof of Theorem 2 given
in [22], by defining a dual definition for contexts and a well-founded order over them. For circular
coinduction, contexts are defined in the same way as experiments, but they could have arbitrary sorts,
including hidden. Dually, a ”context” for circular induction is a ∆-substitution θ : Y → TΣ ctor (Y ′ ) defined
                                                                                                        ctor
in the same way as the experiments but removing the constraint of being ground. If θ : Y → T Σ (Y ′ )
                    ctor                                                                      ctor
and θ′ : Y ′ → T Σ (Y ′′ ) are two contexts for Y and respectively Y ′ , then θ′ [θ] : Y → T Σ (Y ′′ ) is the
context defined by θ′ [θ](y) = θ′ (θ(y)) for each y ∈ Y , where we implicitly assumed θ extended over terms.
We consider the well-founded order over contexts given by θ ≻ θ′ iff there is θ′′ such that θ = θ′ [θ′′ ] or
θ = θ′′ [θ′ ]. Now, the conclusion of Theorem 1 follows by performing the same steps as in the proof of
Theorem 2 in [22].

  The above proof shows that the circularity mechanism is abstracted from both implementations, of the
entailment relation and of the freezing operator; it depends only on some assumptions these two concepts
have to satisfy. However, the duality relationship between the corresponding concepts is not obvious; a
direct proof of the above theorem for the case when the basic entailment is equational deduction is
tedious and very long.
   Moreover, the result above can be extended using the mechanism of the special hypotheses [20]. We
introduce first some notations. If θ is an experiment for Y , then |θ| = max{|θ(y)| | y ∈ Y }, where |t|
denotes the depth of the term t. Let θ≤ denote the set of experiments (for Y ) θ′ with |θ′ | ≤ |θ|.

Definition 10. (special hypotheses) Let B = (S, (Σ, ∆), E) be a specification and F a set of goals.
The special-hypothesis closure of F is the set F ≤ satisfying: 1) B ⊪ θ≤ [ F ] implies B ⊢ θ[ F ≤ ], 2)
F1 ⊆ F2 implies F1≤ ⊆ F2≤ , and 3) (F ≤ )≤ = F ≤ .
An equation e is special for F if e ∈ F ≤ .

  The first condition is general enough to include many induction schemes, e.g., strong induction (see
Example 8), and the third condition says that F ≤ is maximal. The following result is similar to Theorem 3
in [20] and shows that the special hypotheses can be used as lemmas for free; its proof is similar to
Theorem 1.

Theorem 2. (extended inductive circularity principle)
  Let B = (S, (Σ, ∆), E) be a specification. If F is a set of goals such that B∪ F ≤ ⊢ ∆[ F ], then B ⊪ F ≤ .

Definition 11. The circular induction proof system consists of the following inference rules, rep-
resented as conditional reduction rules:

                [Reduce]
                   (B, F, G ∪ { e }) ⇒ (B, F, G)       if B ∪ F ⊢ e
                [Derive]
                   (B, F, G ∪ { e }) ⇒ (B, F ∪ H( e , FVar (∆[ e ])), G ∪ ∆[ e ])   if B ∪ F ̸⊢ e

where H( e , F V ) = { e [y ′ /y] | y ′ ∼ y, y ′ ∈ F V, y ∈ FVar ( e )}

   The rule [Reduce] eliminates a goal whenever it can be deduced using the the basic entailment system.
The key role is played by [Derive] rule: if a goal cannot be deduced with the initial entailment relation,
it and the equations ”similar” to it are added as frozen hypotheses and its derived goals are added as
new proof obligations.

Example 6. (successful examples)
Assume that B is the specification NATSUM defined in Example 2 and that G consists of the goal
sum(m, n) = sum(n, m), where m is the frozen form of M :Nat and n is the frozen form of N :Nat. We
also assume that the basic entailment relation ⊢ is the equational deduction. The initial F is empty. The
derivation tree of the for proving the above goal is described by the following table:


                                                            8
           F                                   G                                           Rule
        1.∅                                    sum(m, n) = sum(n, m)                       [Derive]
           sum(m, n) = sum(n, m)               sum(m, 0 ) = sum(0 , m)
        2.                                                                                 [Derive]
           sum(m, n1 ) = sum(n1 , m)           sum(m, s(n1 )) = sum(s(n1 ), m)
           sum(m, n) = sum(n, m)               0 = sum(0 , 0 )
        3.sum(m, n1 ) = sum(n1 , m)            s(m1 ) = sum(0 , s(m1 ))                    [Reduce]
           m1 = sum(0 , m1 )                   sum(m, s(n1 )) = sum(s(n1 ), m)
           sum(m, n) = sum(n, m)
           sum(m, n1 ) = sum(n1 , m)           s(m1 ) = sum(0 , s(m1 ))
        4.                                                                                 [Reduce]
           m = sum(0 , m)                      sum(m, s(n1 )) = sum(s(n1 ), m)
           m1 = sum(0 , m1 )
        5.     idem                            sum(m, s(n1 )) = sum(s(n1 ), m)             [Derive]
           sum(m, n) = sum(n, m)
           sum(m, n1 ) = sum(n1 , m)
           m = sum(0 , m)                      s(sum(n1 , 0 )) = sum(s(n1 ), 0 )
        6.                                                                                 [Reduce]
           m1 = sum(0 , m1 )                   s(sum(s(n1 ),m2 ))=sum(s(n1 ),s(m2 ))
           s(sum(n1 , m))=sum(s(n1 ), m)
           s(sum(n1 , m2 ))=sum(s(n1 ), m2 )
        7.     idem                            s(sum(s(n1 ),m2 ))=sum(s(n1 ),s(m2 ))       [Reduce]
               idem                             ∅


In the first step only [Derive] can be applied. Two new proof obligations (goals) are derived and added
to G: the first one is obtained using the derivative δ0 = 0 and the second one using the derivative
δs = s(N1 :Nat). Since we have n1 ∼ n, the initial goal with n1 replacing n is added as a frozen hypothesis
to F. In the second step we assume that s(m) = sum(0 , s(m)) is processed. Then only [Derive] can be
applied again. The current goal, where m is replaced by m1 (m1 ∼ m) and sum(m1 , 0 ) is reduced to
m, is added as a frozen hypothesis to F and its derived goals are added as new proof obligations to G.
The goal 0 = sum(0 , 0 ) is reduced using the basic entailment relation (= equational deduction). In the
fourth step, the goal s(m1 ) = sum(0 , s(m1 )) is reduced using the frozen hypothesis m1 = sum(0 , m1 ). In
the fifth step, the goal sum(m, s(n1 )) = sum(s(n1 ), m) is equivalent to s(sum(n1 , m)) = sum(s(n1 ), m)
by applying the definition of sum and the frozen hypothesis sum(m, n1 ) = sum(n1 , m). The derived goals
of this last goal are added to G as new proof obligations and the frozen hypothesis obtained from it by
replacing m by m2 (m2 ∼ m1 ).
  The non-linear goals can also be handled with circular induction. For instance, the goal max (N , N ) =
N can be proved just in one step:



               F                               G                                       Rule
            1. ∅                               max (n, n) = n                          [Derive]
               max (n, n) = n                  max (0 , 0 ) = 0
            2.                                                                         [Reduce]
               max (n1 , n1 ) = n1             max (s(n1 ), s(n1 )) = s(n1 )
            3.     idem                        max (s(n1 ), s(n1 )) = s(n1 )           [Reduce]
                   idem                        ∅


It is known that non-linear conjectures are problematic for automated inductive provers [12]; all non-
linear examples from [12] were successfully handled with circular induction.

Theorem 3. (soundness of circular induction proof system)
 Let B a specification with constructors and G be a set of goals. If (B, F0 = ∅, G0 = G ) ⇒ . . . ⇒
(B, Fn , Gn = ∅) using the rules of the proof system defined in Definition 11, then B ⊪ G.

Proof. Let H denote the set of unfrozen equations from H( e , FVar (∆[ e ])). First we show that H is
a set of special hypotheses for e. Let θ be an experiment such that B ⊢ θ≤ [ e ]. We have to show that
B ⊢ θ[ H ]. Let e′ be an arbitrary equation from H. It follows that e′ is e [y ′ /y] for some y ′ ∼ y. There


                                                     9
is a constructor c such that θ(y) = c(. . . θ(y ′ ) . . .) by the definition of ∼. Let θ′ denote the substitution
equal to θ excepting θ′ (y) which is equal to θ(y ′ ). Obviously, θ′ ≤ θ and hence B ⊢ θ′ [ e ]. The conclusion
B ⊢ θ[ e′ ] follows from the fact that θ′ [ e ] and θ[ e′ ] are the same.
The rest of the proof of the theorem follows the same steps as that of Theorem 5 in [20], but using the
dual notions: “equation without inductive variables” instead of “visible equation” and “equation with
inductive variables” instead of “hidden equation”.                                                              ⊔
                                                                                                                ⊓

Example 7. (Failing example)
 We present an example where the circular induction proof system defined in Definition 11 fails. Later,
we show how the proof system can be extended in order to handle such examples. Assume that B is the
specification TREE defined in Example 3 and that G consists of the goal mirror (mirror (ℓ)) = ℓ, where ℓ
is the frozen form of L:TList. The initial F is empty. The derivation tree generated by the proof system
defined in Definition 11 is described as follows

           F                                    G                                                     Rule
        1. ∅                                    mirror (mirror (ℓ)) = ℓ                               [Derive]
           mirror (mirror (ℓ)) = ℓ              mirror (mirror (nil )) = nil
        2. mirror (mirror (ℓ1 )) = ℓ1           mirror (mirror (ℓ1 ; ℓ2 )) = ℓ1 ; ℓ2                  [Reduce]
           mirror (mirror (ℓ2 )) = ℓ2           mirror (mirror ([t])) = [t]
                                                mirror (mirror (ℓ1 ; ℓ2 )) = ℓ1 ; ℓ2
        3.      idem                                                                                  [Reduce]
                                                mirror (mirror ([t])) = [t]
        4.     idem                             [mirror (mirror (t))] = [t]                           [Derive]
           mirror (mirror (ℓ)) = ℓ
           mirror (mirror (ℓ1 )) = ℓ1           [mirror (mirror ([e1 ]))] = [[e1 ]]
        5.                                                                                            [Reduce]
           mirror (mirror (ℓ2 )) = ℓ2           [mirror (mirror (tr (e2 , ℓ3 ]))] = [tr (e2 , ℓ3 )]
           [mirror (mirror (t))] = [t]
        6.     idem                             [mirror (mirror (tr (e2 , ℓ3 ))] = [tr (e2 , ℓ3 )]



where ℓi is the frozen form of Li :TList, t is the frozen form of T :Tree, and ei is the frozen form of Ei :Elt. In
the first step, [Derive] produces two hypotheses because ℓ1 ∼ ℓ and ℓ2 ∼ ℓ; these hypotheses will be used in
the non-linear conjecture added by this rule. The last goal can be reduced to [tr (e2 , mirror (mirror (ℓ3 ))] =
[tr (e2 , ℓ3 )], which is irreducible because we have no hypotheses on ℓ3 . The problem could be solved if
we extend ∼ such that t ∼ ℓ, ℓ3 ∼ t. Then, at the fourth step when [Derive] is applied again, we add
mirror (mirror (ℓ3 )) = ℓ3 to F, which is a special hypothesis, because ℓ3 ∼+ ℓ, where ∼+ is the transitive
closure of ∼. Next we formalize this extension.

    Let δc be a derivative and e a goal. If δc [ e ] is an equation of the form e [c(y1 .s1 , . . . , yn .sn )/y.s], then
       ∗                                   ∗                                   ∗
yi .si ∼ y.s for all i = 1, . . . , n. Let ∼+ denote the transitive closure of ∼.

Definition 12. The extended circular induction proof system consists of the following inference
rules, represented as conditional reduction rules:

                   [Reduce]
                       (B, F, G ∪ { e }) ⇒ (B, F, G)       if B ∪ F ⊢ e
                   [Derive]
                       (B, F, G ∪ { e }) ⇒
                       (B, F ∪ { e } ∪ H( e , FVar (∆[ e ])) ∪ H∗ (F, FVar (∆[ e ])), G ∪ ∆[ e ])
                     if B ∪ F ̸⊢ e
                                         ∗
where H ( f , F V ) = { f [y ′ /y] | y ′ ∼+ y, y ′ ∈ F V, y ∈ FVar ( f ), sort(y) = sort(y ′ )} and H∗ (F, F V ) =
         ∗
        ∗
S
  e ∈F H ( e , F V )

   H∗ (F, FVar (∆[ e ])) includes an instance of each frozen hypothesis in F having a frozen variable y
                                                                                               ∗
for which there is a similar new frozen variable y ′ , added by the new derived goals. Using ∼+ , the
”reincarnation” of a variable y can be made by means of some intermediate ”hosts” (= variables of
different sorts).


                                                           10
Example 8. Using the rules of the extended circular induction proof system, the derivation tree from
Example 7 can be continued as follows:
           mirror (mirror (ℓ)) = ℓ
        4. mirror (mirror (ℓ1 )) = ℓ1        [mirror (mirror (t))] = [t]                          [Derive]
           mirror (mirror (ℓ2 )) = ℓ2
           mirror (mirror (ℓ)) = ℓ
           mirror (mirror (ℓ1 )) = ℓ1
                                           [mirror (mirror ([e1 ]))] = [[e1 ]]
        5. mirror (mirror (ℓ2 )) = ℓ2                                                            [Reduce]
                                           [mirror (mirror (tr (e2 , ℓ3 ]))] = [tr (e2 , ℓ3 )]
           mirror (mirror (ℓ3 )) = ℓ3
           [mirror (mirror (t))] = [t]
        6.     idem                        [mirror (mirror (tr (e2 , ℓ3 ))] = [tr (e2 , ℓ3 )]    [Reduce]
        7.     idem                          ∅


Comparing with the previous proving attempt, a new frozen axiom was added to F in the fourth step
           ∗
because ℓ3 ∼+ ℓ.

Theorem 4. (soundness of extended circular induction proof system)
 Let B a specification with constructors and G be a set of goals. If (B, F0 = ∅, G0 = G ) ⇒ . . . ⇒
(B, Fn , Gn = ∅) using the rules of the proof system defined in Definition 12, then B ⊪ G.

Proof. It is enough to observe that H∗ (F, FVar (∆[ e ])) is a set of special hypotheses for F . The rest of
the proof is similar to that of Theorem 3.                                                                ⊔
                                                                                                          ⊓


5   Implementation in CIRC

CIRC [18, 19] is an automated inductive and coinductive prover built around the circularity principle.
It is implemented in Maude [7] as a metalanguage application, thus making use of important reflection
capabilities in order to enhance a specification during a proving session. The prover extends Maude
specifications with behavioral properties. The specifications provided to CIRC are order-sorted [15] rather
than many-sorted. This involves the definition of a partial order relation between sorts which has the
role of avoiding the explicit use of inclusion operators. For instance, for the specification presented in
Example 3, instead of using the operation [ ] : Tree → TList we can simply specify the subsort relation
Tree < TList. The capability of working with subsorts is also exploited in the efficient implementation
of the circular induction.
  As presented in [19], the entailment relation used in CIRC is B ⊢ (∀X)t = t′ if ∧i∈I (ui = vi ) iff
nf(t) = nf(t′ ), where nf(t) is computed as follows:
  – the variables X of the equations are turned into fresh constants;
  – the condition equalities ui = vi are added as equations to the specification;
  – the equations in the specification are oriented and used as rewrite rules.
  The engine implements the proof system given in [22] by a set of reduction rules (B, F, G) ⇒ (B, F ′ , G ′ ),
where B represents the (original) algebraic specification, F is the set of frozen axioms and G is the current
set of proof obligations. During a proof by induction session, the steps followed by the engine resemble
those made during a proof by coinduction. The difference consists of the way in which frozen goals and
special hypotheses are handled.
  In what follows we present the correlation between the theory presented so far and the way CIRC
manages data during a proving session by induction. The inference rules are implemented using a similar
mechanism to that used for coinductive proofs. The main difficulty raised by circular induction is the in-
ternal management of special hypotheses H(F , FV ) ∪ H∗ (F, FV ). The number of these hypotheses could
exponentially increase, and their computation become expensive. We use the subsort facility in order to
drastically reduce the number of stored hypotheses. We store only generic hypotheses represented with
variables of fresh subsorts and each new generated constant is declared as inhabitant to an appropriate
such subsort. Then the set of all needed special hypotheses are obtained by instantiation. For that we
need to distinguish between initial variables and their incarnations.
                                                                                      ∗
Definition 13. A frozen inductive variable y.s is a source iff (̸ ∃y ′ .s)y.s ∼+ y ′ .s.


                                                       11
   For each frozen induction variable y ′ .s we define the operation source such that source(y ′ .s) = y.s if
 ′   ∗
y .s ∼+ y.s and y.s is a source. Each time we add a new source y.s, either at the beginning, or during a
proof session, we enrich the specification with a fresh subsort s⟨y⟩ such that s⟨y⟩ < s.
  CIRC implements a variant of the rule [Derive] from Definition 12 such that instead of adding a specific
hypothesis (equation) for each of the generated variables, it adds only one hypothesis that may be used
by all the frozen variables with a common source. This leaves the set of hypotheses uncluttered and helps
for improving the speed of the matching engine:

               [Derive]
                 (B, F, G ∪ { e }) ⇒     (B′ , F ∪ H′ ( e , FVar (∆[ e ])), G ∪ ∆[ e ])   if B ∪ F ̸⊢ e
               where H ( e , FV ) = { e [y ′ :s⟨source(y)⟩/y.s] | y ′ .s ∈ FV , y.s ∈ FVar ( e ),
                          ′

                    ∗
               y ′ .s ∼+ y.s} and B ′ is B enriched with the constants y ′ .s′ of sort s′ ⟨source(y ′ )⟩
               for each y ′ .s′ ∈ FVar (∆[ e ]).

We have f ∈ H∗ (F, FV )∪H( e , FVar (∆[ e ])) iff f is an instance of a hypothesis in F ∪H′ ( e , FVar (∆[ e ])).
In order to understand the special hypothesis management algorithm better, let us analyze the derivation
steps from Examples 7 and 8.
  Step 1 involves the creation of a new sort TList⟨ℓ⟩ < TList. The source function is defined as:
source(ℓ) = ℓ, source(ℓ1 ) = ℓ, source(ℓ2 ) = ℓ. Here ℓ, ℓ1 , ℓ2 are added as constants of sort TList⟨ℓ⟩.
The frozen hypothesis added to the specification is mirror (mirror (L:TList⟨ℓ⟩)) = L:TList⟨ℓ⟩.
   At step 4 we add the sort Tree⟨t⟩ < Tree and enhance the source function such that source(t) =
t, source(l3 ) = l. The added constants are t.Tree⟨t⟩ and ℓ3 .TList⟨ℓ⟩. The new frozen hypothesis is
[mirror (mirror (T :Tree⟨t⟩))] = [T :Tree⟨t⟩].
     The reduction at step 6 succeeds because it makes use of the first hypothesis instantiated with ℓ3 .
  Excepting the management of the special contexts and the meanings of the frozen equations, the engines
implementing circular induction and circular coinduction, respectively, are similar. An immediate main
advantage is that the mechanisms added to increase the power of one engine can be used for free by
the other one. We exemplify this feature showing how the simplification rules [16], initially added for
the coinduction
         PN       engine, can be used by the induction engine for deriving simpler goals. Let us consider
the goal k=0 f ib(k) = np(s(N )) from Example 4. The sum can be computed by an operation sum⟨k ⟩
defined by sum⟨k ⟩(0 ) = 0 and sum⟨k ⟩(s(N )) = sum⟨k ⟩(N )+fib(s(N )). One intermediate goal computed
by circular induction is fib(s(N ))+sum⟨k ⟩(N ) = s(np(N ))+sum⟨k ⟩(N ). CIRC succeeds to automatically
prove this goal, but it would be nice to have it in a simpler way, as a general result: fib(s(N )) = s(np(N )).
This can be accomplished by adding to the specification the following simplification rule:
                                                   M +P =N +P
                                                      M =N
and to define a proof tactic which tries to apply a simplification before each derivation. The proof tactics
are specified in CIRC using a simple strategy language [13].


5.1     Circular Coinduction and Circular Induction Working Together

Since both circular coinduction and circular induction are defined using the same algebraic framework,
they could be combined for proving a given goal. Here we present a simple example to exhibit how the two
proof techniques are combined in the current version of CIRC. We consider the specification NATSUM
defined in Example 2 and streams defined over natural numbers with the operations hd, tl, and zeros
defined as in Example 1 and together with an addition operation + : Stream Stream → Stream
defined by hd (S1 + S2 ) = sum(hd (S1 ), hd (S2 )), tl (S1 + S2 ) = tl (S1 ) + tl (S2 ). The goal is to prove that
zeros + S = S . We start by applying the circular coinduction proof tactic:

(add goal zeros + S:Stream = S:Stream .)
(coinduction .)
. . .
Visible goal [* sum(0,hd(S:Stream)) *] = [* hd(S:Stream) *]
failed during coinduction.


                                                          12
The proof sticks on the intermediate goal sum(0 , hd (S )) = hd (S ), because that it is not direct conse-
quence of NATSUM, and we have to prove it by induction. We cannot apply the circular induction proof
technique because the goal does not include a variable of sort Nat. We save the current state of the proof,
and start a proof by induction on a generalization of the goal: sum(0 , N ) = N , where N is a variable of
sort Nat (this can be obtained using the command (generalize .)). After the engine finishes the proof
by induction, it automatically reloads the saved state and resume the left proof by coinduction:

(save proof state .)
(add goal sum(0, N:Nat) = N:Nat .)
(induction .)
. . .
Proof state loaded.
(coinduction .)
Proof succeeded.
. . .
Proved properties:
  sum(0,N#0:Nat<N>) = N#0:Nat<N>
  sum(0,N:Nat) = N:Nat
  zeros + S:Stream = S:Stream

The above procedure is not yet completely mechanized. In order to make it automated, the tool must be
extended with the ability to handle the induction reasoning as a basic entailment relation for the circular
coinduction.


6     Related Work

There are many mechanizable induction techniques proposed in the literature; reviews of the explicit
techniques can be found in [6] and of the implicit ones in [10]. We group the discussion into two families:
the classical coverset/test-set tradition, to which circular induction was originally compared, and the
more recent cyclic-proof (or infinite-descent) tradition, into which circular induction most naturally fits
when viewed with hindsight.


6.1   Coverset, rewrite and test-set induction

Coversets provide the basis for many mechanizable induction principles. Coverset induction (see, e.g., [23])
explores the recursive definitions of the operations occurring in conjectures; the method is tied to a well-
founded ordering, which is not always easy to find. The set of derivatives used in circular induction are
coversets associated with sorts (not operations), used to derive new goals that are not always subgoals;
circular induction requires no explicit well-founded ordering, its soundness resting instead on the implicit
ordering of the experiments. Rewrite (term-rewriting) induction [21] is also based on coversets and
uses the rewrite relation of a uniformly terminating rewrite system as its well-founded ordering, which
typically assumes an explicit partial ordering over operators. Test-set induction (see, e.g., [1]) combines
an explicit, test-set–based induction scheme with proof by consistency (implicit induction) used as a
refutation technique, and was implemented in Spike [2]. Circular induction discovers the analogue of
a test set on-the-fly while it unrolls the derivation graph, with no separate algorithm for computing
test/cover sets and no built-in refutation procedure.


6.2   Cyclic proof and proof by infinite descent

Seen from today, circular induction is an instance of a much broader idea that crystallized independently
and almost simultaneously in the proof-theory community: cyclic proof, in which the explicit induction
rule is replaced by a finite derivation containing “back-links” (cycles), whose soundness is guaranteed by
a global condition expressing an argument by Fermat-style infinite descent. The foundational reference
is Brotherston and Simpson [5], who give two sequent calculi for first-order logic with inductively defined
predicates: one with explicit (Henkin-complete) induction rules, and one with non-well-founded proofs
in which the left rules for inductive predicates are mere case-splits and soundness is recovered by a
global trace condition—every infinite path must carry a trace that progresses (decreases) infinitely often.
Restricting the infinitary system to regular (finitely representable) proofs yields the cyclic system, which


                                                    13
they show subsumes explicit induction and conjecture to be equivalent to it. Circular induction can be
read as the dual, equational-logic counterpart of this picture: our derivatives are exactly the case-split
(unfolding) steps; our frozen equations play the structural role that the trace condition plays globally,
inhibiting unsound use of a hypothesis until descent has genuinely occurred; and our soundness theorems
(Theorems 1, 3 and 4) appeals to the implicit well-founded order on experiments rather than to a
separately checked global condition. A distinctive feature of our setting is that the very same circularity
principle, applied to destructors instead of constructors, yields circular coinduction, so that induction
and coinduction live in one framework—a unification that the cyclic-proof literature reached only later
(see below).

Generic cyclic provers ( Cyclist). Brotherston, Gorogiannis and Petersen [4] distil the construction
of [5] into Cyclist, a generic, fully automated cyclic theorem prover: an OCaml functor parametric in
the sequents, inference rules and trace-pair function of the object logic, instantiated to first-order logic
with inductive predicates, separation-logic entailment, and separation-logic program termination. The
global trace condition is decided by checking language inclusion of two Büchi automata via a model
checker. Cyclist and CIRC share the ambition of a single, logic-generic engine—Cyclist is parametric
in the logic, while circular (co)induction is parametric in the basic entailment relation ⊢. The technical
contrast is instructive. Cyclist reasons about inductively defined predicates and, as its authors note, has
“difficulty dealing with heavily-equational goals”; commutativity of addition is reported as not provable,
precisely because it needs equational rewriting and a non-trivial lemma. Circular induction, working
natively over equational specifications, proves commutativity and associativity of sum automatically,
discovering the required lemmas as frozen hypotheses. Conversely, Cyclist’s Büchi-automaton soundness
check copes with overlapping cycles and complex induction schemes (e.g. Wirth’s “P&Q” example) that
are beyond a purely local discipline; circular induction trades some of that generality for the simplicity
of needing only two inference rules and no global automaton check.

Synthesising the induction (cyclic abduction). Brotherston and Gorogiannis [3] push cyclic proof from
verification towards synthesis: their Caber tool (built on Cyclist) performs cyclic abduction, simul-
taneously constructing a cyclic safety/termination proof of a heap-manipulating while program and
abducing the inductive separation-logic predicates (lists, trees, cyclic and composite structures) that the
proof needs. This is a close relative, in spirit, of the lemma discovery that circular induction performs
while it unrolls a proof: in both cases the missing inductive content is guessed on demand to make the
cycle close. The settings differ—Caber abduces shape predicates for imperative pointer programs in
separation logic, whereas circular induction discovers auxiliary equational lemmas (e.g. sum(0, M ) = M )
and incarnation relations for algebraic data types.

Integrating induction and coinduction. Cohen and Rowe [8] are, to our knowledge, the first in the cyclic-
proof tradition to integrate induction and coinduction in one system, an aim that motivated circular
(co)induction from the outset. They extend transitive-closure logic with a dual “co-closure” operator
forming greatest fixed points, and give a sound and complete non-well-founded proof system whose
cyclic subsystem supports automated inductive and coinductive reasoning, demonstrated on streams.
The parallel with our Figure 3 is striking: where we obtain coinduction by dualising constructors to
destructors and “freezing at top” to “inhibiting at bottom”, they obtain it by dualizing least to the
greatest fixed points via closure/co-closure. Their development is carried out for a relational fixed-point
logic with completeness results; ours is carried out for behavioral equational logic with an implemented
prover (CIRC), and the two can be seen as complementary realizations of the same unifying intuition.

Deciding infinite descent efficiently ( Cyclone). A recurring cost in the Cyclist line is the sound-
ness check itself: deciding the infinite-descent/trace condition is PSPACE-complete. Cohen, Rowe and
Shaked [9] address this with Cyclone, a heterogeneous tool that combines several fast semi-decision
procedures with a complete decision procedure as a fallback, achieving high coverage and large speed-
ups on benchmarks harvested from Cyclist. This work is orthogonal to, but illuminating for, circular
induction: it engineers exactly the global check that our use of frozen equations and the implicit ordering
of experiments lets us avoid, at the price of the more restricted (but cheaper) local discipline we adopt.

Cyclic equational reasoning ( CycleQ). The closest modern analogue of circular induction is arguably
CycleQ by Jones, Ong and Ramsay [17], a cyclic proof system for automated equational reasoning about


                                                    14
pure functional programs, in which cyclic proof and equational reasoning are mediated by contextual
substitution as a cut rule. Like circular induction, CycleQ replaces the explicit induction rule by cyclic
unfolding over an equational goal, and the authors explicitly position it as subsuming “inductionless
induction”, “rewriting induction” and “proof by consistency”—the same classical lineage to which we
compared circular induction above. Its soundness is checked incrementally with the size-change principle
(rather than a Büchi-automaton inclusion test), and it is implemented as a GHC plugin. The conceptual
overlap with our work is considerable; the main differences are that CycleQ targets a typed functional
language with a size-change soundness check and contextual-substitution cut, whereas circular induction
targets order-sorted algebraic specifications, derives soundness from the experiment ordering, and is
embedded in the same engine as circular coinduction.

Inductive theorem proving in Maude ( NuITP). Within the same Maude/rewriting-logic ecosystem as
CIRC, Durán, Escobar, Meseguer and Sapiña [11] have developed NuITP, a next-generation inductive
theorem prover based on inductive order-sorted first-order logic. NuITP targets the same equational pro-
grams as circular induction but emphasises expressiveness—types and subtypes, conditional equations
and rewriting modulo associativity, commutativity and identity—and scalability, leveraging Maude’s
modern symbolic infrastructure (variant narrowing and unification, variant satisfiability, order-sorted
congruence closure, equality predicates). Its central inference rule, Generator-Set Induction, is an ex-
plicit, constructor-based induction scheme: it requires a user-supplied recursive path ordering (RPO) for
termination and manages explicit induction hypotheses, in contrast to circular induction, which uses
no explicit well-founded ordering and discovers its hypotheses (frozen equations) during proof search.
The two thus represent the explicit-induction and circular-induction strategies, respectively, instantiated
over very similar order-sorted equational theories, and the comparison highlights what each style buys:
NuITP gains modulo-AC(U) reasoning, decision procedures and scalability; circular induction gains a
minimal two-rule calculus and free interoperation with circular coinduction.

Table 1. Circular induction in the context of cyclic / infinite-descent provers. “Implicit order” means soundness
rests on a well-founded order that is never computed explicitly.

  System/paper         Paradigm         Logic/domain          Soundness           Explicit    Ind.+Coind.?
                                                              mechanism           order?
  Circular induc- Circular              Order-sorted equa- Frozen eqs. + im- No               Yes (with circu-
  tion (this paper, (cyclic)            tional specs       plicit order on ex-                lar coind.)
  2010)                                                    periments
  Brotherston–        Cyclic / ex- FO logic + induc- Global trace con- Implicit               Induction only
  Simpson         [5] plicit (both) tive predicates  dition (infinite de- (trace)
  (LICS’07)                                          scent)
  Cyclist         [4] Cyclic, generic FO ind. preds.; sep. Trace via Büchi- Implicit         Induction only
  (APLAS’12)                          logic; termination   automata inclu- (trace)
                                                           sion
  Cyclic abduction   Cyclic + ab- Separation    logic, Safety/termination Implicit            Induction only
  / Caber        [3] duction (syn- while programs      trace condition    (trace)
  (SAS’14)           thesis)
  Cohen–Rowe      [8] Non-well-        Transitive       (co- Trace condition; Implicit        Yes
  (IJCAR’20)          founded        / )closure logic        sound & complete (trace)         (closure/co-
                      cyclic                                                                  closure)
  Cyclone         [9] Decision pro- Trace graphs (logic- Heterogeneous      n/a               n/a
  (TACAS’25)          cedures      for agnostic)         (semi-)decision of
                      cyclic proofs                      descent
  CycleQ         [17] Cyclic,   equa- Typed pure func- Size-change prin- Implicit             Induction only
  (PLDI’22)           tional          tional programs  ciple; contextual- (size-
                                                       subst. cut         change)
  NuITP        [11] Explicit induc- Order-sorted   eq. User-supplied   Yes                    Induction only
  (PPDP’24 / 2025) tion             logic,      modulo RPO + induction (RPO)
                                    AC(U)              hyps.




                                                        15
6.3   Summary

Table 1 summarises the comparison along the dimensions that matter most for circular induction: the
proof paradigm, the logic/domain, the mechanism that justifies soundness, whether an explicit well-
founded order is required, what (if anything) is discovered during the proof, whether the framework is
generic, and whether induction and coinduction are unified.


7     Conclusion

We have shown that the Circularity Principle, originally used to justify circular coinduction, also under-
lies a sound inductive proving technique, circular induction. Presenting the two techniques at a generic
level, parametric in the basic entailment relation, exposes them as dual instances of one principle: deriva-
tives arise from constructors rather than destructors, experiments are ground substitutions rather than
contexts, and freezing inhibits the use of a hypothesis “over” a substitution rather than “underneath”
a context. This duality let us reuse much of the metatheory of circular coinduction and, at the level of
implementation, let the two engines in CIRC share machinery—so that enhancements such as simpli-
fication rules, generalization, or special hypotheses benefit both. The resulting calculus is deliberately
minimal: two inference rules, no explicit well-founded ordering, and no separate algorithm for computing
cover or test sets, with the required inductive content (auxiliary lemmas and the analogue of a test set)
discovered on the fly as the derivation graph is unrolled.
   Because coinductive behavioral equality and inductive equality share the same abstract structure based
on experiments, they also share the same complexity: inductive equality is Π20 -complete, so no procedure
can be complete for proving and disproving inductive conjectures. In particular, the present version of
circular induction has no explicit refutation mechanism, and a non-terminating derivation may indicate
either that the goal is false or merely that the system was unable to prove it.
   Several directions remain open. The combination of induction and coinduction illustrated in Section 5
is not yet fully mechanized: to automate it, the tool must be able to use inductive reasoning as a basic
entailment relation for circular coinduction. Adding a complementary disproving or refutation procedure
would let circular induction reject false conjectures rather than merely fail to prove them.


References
 1. Bouhoula, A.: Automated theorem proving by test set induction. J. Symb. Comput. 23(1), 47–77 (1997),
    https://doi.org/10.1006/jsco.1996.0076
 2. Bouhoula, A., Rusinowitch, M.: SPIKE: A system for automatic inductive proofs. In: Alagar, V.S., Nivat, M.
    (eds.) Algebraic Methodology and Software Technology, 4th International Conference, AMAST ’95, Montreal,
    Canada, July 3-7, 1995, Proceedings. pp. 576–577. Lecture Notes in Computer Science, Springer (1995),
    https://doi.org/10.1007/3-540-60043-4_79
 3. Brotherston, J., Gorogiannis, N.: Cyclic abduction of inductively defined safety and termination precon-
    ditions. In: Müller-Olm, M., Seidl, H. (eds.) Static Analysis - 21st International Symposium, SAS 2014,
    Munich, Germany, September 11-13, 2014. Proceedings. pp. 68–84. Lecture Notes in Computer Science,
    Springer (2014), https://doi.org/10.1007/978-3-319-10936-7_5
 4. Brotherston, J., Gorogiannis, N., Petersen, R.L.: A generic cyclic theorem prover. In: Jhala, R., Igarashi,
    A. (eds.) Programming Languages and Systems - 10th Asian Symposium, APLAS 2012, Kyoto, Japan,
    December 11-13, 2012. Proceedings. pp. 350–367. Lecture Notes in Computer Science, Springer (2012), https:
    //doi.org/10.1007/978-3-642-35182-2_25
 5. Brotherston, J., Simpson, A.: Complete sequent calculi for induction and infinite descent. In: 22nd IEEE
    Symposium on Logic in Computer Science (LICS 2007), 10-12 July 2007, Wroclaw, Poland, Proceedings. pp.
    51–62. IEEE Computer Society (2007), https://doi.org/10.1109/LICS.2007.16
 6. Bundy, A.: The automation of proof by mathematical induction. In: Robinson, J.A., Voronkov, A. (eds.)
    Handbook of Automated Reasoning (in 2 volumes), pp. 845–911. Elsevier and MIT Press (2001), https:
    //doi.org/10.1016/b978-044450813-3/50015-1
 7. Clavel, M., Durán, F., Eker, S., Lincoln, P., Martı́-Oliet, N., Meseguer, J., Talcott, C.L. (eds.): All About
    Maude - A High-Performance Logical Framework, How to Specify, Program and Verify Systems in Rewriting
    Logic, Lecture Notes in Computer Science, vol. 4350. Springer (2007)
 8. Cohen, L., Rowe, R.N.S.: Integrating induction and coinduction via closure operators and proof cycles. In:
    Peltier, N., Sofronie-Stokkermans, V. (eds.) Automated Reasoning - 10th International Joint Conference,
    IJCAR 2020, Paris, France, July 1-4, 2020, Proceedings, Part I. pp. 375–394. Lecture Notes in Computer
    Science, Springer (2020), https://doi.org/10.1007/978-3-030-51074-9_21


                                                       16
 9. Cohen, L., Rowe, R.N.S., Shaked, M.: Cyclone: A heterogeneous tool for verifying infinite descent. In:
    Gurfinkel, A., Heule, M. (eds.) Tools and Algorithms for the Construction and Analysis of Systems - 31st
    International Conference, TACAS 2025, Held as Part of the International Joint Conferences on Theory and
    Practice of Software, ETAPS 2025, Hamilton, ON, Canada, May 3-8, 2025, Proceedings, Part I. pp. 336–354.
    Lecture Notes in Computer Science, Springer (2025), https://doi.org/10.1007/978-3-031-90643-5_18
10. Comon, H.: Inductionless induction. In: Robinson, J.A., Voronkov, A. (eds.) Handbook of Automated
    Reasoning (in 2 volumes), pp. 913–962. Elsevier and MIT Press (2001), https://doi.org/10.1016/
    b978-044450813-3/50016-3
11. Durán, F.J., Escobar, S., Meseguer, J., Sapiña, J.: Nuitp: An inductive theorem prover for equational program
    verification. In: Bruni, A., Momigliano, A., Pradella, M., Rossi, M., Cheney, J. (eds.) Proceedings of the 26th
    International Symposium on Principles and Practice of Declarative Programming, PPDP 2024, Milano, Italy,
    September 9-11, 2024. pp. 6:1–6:11. ACM (2024), https://doi.org/10.1145/3678232.3678236
12. Falke, S., Kapur, D.: Inductive decidability using implicit induction. In: LPAR. Lecture Notes in Computer
    Science, vol. 4246, pp. 45–59. Springer (2006)
13. G. Caltais, E. Goriac, D.L., Grigoraş, G.: A Rewrite Stack Machine for ROC! In: 10th International Sympo-
    sium on Symbolic and Numeric Algorithms for Scientific Computing. IEEE Computer Society (2008)
14. Goguen, J., Lin, K., Roşu, G.: Conditional circular coinductive rewriting with case analysis. In: WADT.
    Lecture Notes in Computer Science, vol. 2755, pp. 216–232. Springer (2002)
15. Goguen, J., Meseguer, J.: Order-sorted algebra I: Equational deduction for multiple inheritance, overloading,
    exceptions and partial operations. Theoretical Computer Science 105(2), 217–273 (1992)
16. Goriac, E., Caltais, G., Lucanu, D.: Simplification and Generalization in CIRC. In: 12th International Sym-
    posium on Symbolic and Numeric Algorithms for Scientific Computing. IEEE Computer Society (2009)
17. Jones, E., Ong, C.L., Ramsay, S.J.: Cycleq: an efficient basis for cyclic equational reasoning. In: Jhala,
    R., Dillig, I. (eds.) PLDI ’22: 43rd ACM SIGPLAN International Conference on Programming Language
    Design and Implementation, San Diego, CA, USA, June 13 - 17, 2022. pp. 395–409. ACM (2022), https:
    //doi.org/10.1145/3519939.3523731
18. Lucanu, D.: Circ v1.5 (May 2026). https://doi.org/10.5281/zenodo.20345982, https://github.com/
    dlucanu/circ
19. Lucanu, D., Goriac, E.I., Caltais, G., Roşu, G.: CIRC : A behavioral verification tool based on circular
    coinduction. In: CALCO 2009. LNCS, vol. 5728, pp. 433–442. Springer (2009)
20. Lucanu, D., Roşu, G.: Circular coinduction with special contexts. In: ICFEM. LNCS, vol. 5885, pp. 639–659.
    Springer (2009)
21. Reddy, U.S.: Term rewriting induction. In: Stickel, M.E. (ed.) 10th International Conference on Automated
    Deduction, Kaiserslautern, FRG, July 24-27, 1990, Proceedings. pp. 162–177. Lecture Notes in Computer
    Science, Springer (1990), https://doi.org/10.1007/3-540-52885-7_86
22. Roşu, G., Lucanu, D.: Circular Coinduction – A Proof Theoretical Foundation. In: CALCO 2009. LNCS,
    vol. 5728, pp. 127–144. Springer (2009)
23. Zhang, H., Kapur, D., Krishnamoorthy, M.S.: A mechanizable induction principle for equational specifica-
    tions. In: Lusk, E.L., Overbeek, R.A. (eds.) 9th International Conference on Automated Deduction, Argonne,
    Illinois, USA, May 23-26, 1988, Proceedings. pp. 162–181. Lecture Notes in Computer Science, Springer
    (1988), https://doi.org/10.1007/BFb0012831




                                                        17
