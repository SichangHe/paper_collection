                                                       An Iris for Expected Cost Analysis
                                                                            Technical Report


                                                                   Janine Lohse, Deepak Garg
                                                                                MPI-SWS

                                                                            June 02, 2024
arXiv:2406.00884v1 [cs.PL] 2 Jun 2024




                                                 We present ExpIris, a separation logic framework for the (amortized) ex-
                                                 pected cost analysis of probabilistic programs. ExpIris is based on Iris,
                                                 parametric in the language and the cost model, and supports both imper-
                                                 ative and functional languages, concurrency, higher-order functions and
                                                 higher-order state. ExpIris also offers strong support for correctness rea-
                                                 soning, which greatly eases the analysis of programs whose expected cost
                                                 depends on their high-level behaviour. To enable expected cost reasoning
                                                 in Iris, we build on the expected potential method. The method provides
                                                 a kind of “currency” that can be used for paying for later operations,
                                                 and can be distributed over the probabilistic cases whenever there is a
                                                 probabilistic choice, preserving the expected value due to the linearity of
                                                 expectations. We demonstate ExpIris by verifying the expected runtime
                                                 of a quicksort implementation and the amortized expected runtime of a
                                                 probabilistic binary counter.

                                        1   Introduction
                                        The performance of many algorithms relies on randomization. A classical example
                                        is Quicksort, whose expected runtime can be improved from O(n2 ) to O(n log n)
                                        through randomization. However, reasoning about probabilistic algorithms and pro-
                                        grams can be counterintuitive, making pen-and-paper proofs error-prone. This high-
                                        lights the necessity for expressive and mechanized logics for expected cost analysis.
                                        Iris [9] is an expressive separation logic framework that has been successfully applied
                                        to a large number of languages and domains, e.g., [22, 10, 21, 5, 14, 17]. In this
                                        report, we show how to adapt Iris to obtain ExpIris, a modular and expressive
                                        framework for (amortized) expected cost analysis of probabilistic programs. ExpIris
                                        is parametric in both the language and the cost model and applies to feature-rich
                                        languages supporting, amongst others, both imperative and functional programming,
                                        concurrency, higher-order functions and higher-order state.
                                        We build on the method of potentials for amortized cost analysis. Potential can be
                                        seen as a ghost “currency” that pays for operations that induce cost. Whenever some
                                        of the available potential is not immediately needed, it can be stored to pay for future
                                        operations. Typically, potential is expressed as function of the program state.
                                        The potential method has been adapted for amortized expected cost of probabilistic



                                                                                     1
programs [4]. The key idea is that when reasoning about expected cost, a probabilistic
branching gives the opportunity to distribute the potential among the different cases,
as long as the expected value of the distributed potentials does not increase. For
example, if a program flips a fair coin and a potential of 2 is available, one can
continue in the heads-case with a potential of 1 and in the tails-case with a potential
of 3. This is sound: if there is a cost of 1 with probability 12 , and a cost of 3 with
probability 21 , the expected cost is 2.
Existing work has embedded the expected potential method into program logics [4,
18, 24]. Specifically, [18] and [24] are syntax-based approaches designed for automated
expected cost analysis. While this approach works great for simple programs, it is not
suitable for programs whose expected cost depends on the correctness of their func-
tional behaviour. A crucial reason is the lack of support for correctness reasoning.
For example, the expected runtime of any randomized quicksort implementation cru-
cially depends on the correctness of the subprocedure implementing the partitioning.
In contrast, [4] supports correctness reasoning, but focuses on a simple imperative
language with binary probabilistic choice. It would be very hard in practice to imple-
ment and analyze an algorithm like quicksort in the logic of [4], since quicksort relies
on recursion and uniform sampling from a list.
In contrast, ExpIris supports all of the following:
  • We support almost all correctness reasoning that is supported by Iris, with the
    exception of prophecy variables and later credits.
  • ExpIris is parametric in the cost model and language, and supports feature-
    rich languages, including imperative and functional progamming, concurrency,
    higher-order functions and higher-order state.
  • ExpIris is mechanized in the Coq proof assistant. We also adapt the Iris Proof
    Mode [12] for ExpIris: the Iris Proof Mode provides an interface to keep track of
    assumptions and goals, and automates routine proof steps. We extend existing
    tactics for allowing manipulation of potential.
We demonstrate our framework with two case studies: We (1) bound the expected
runtime of a randomized in-place quicksort implementation and (2) analyze the amor-
tized expected runtime of a probabilistic binary counter.
Our Coq development can be found at https://gitlab.mpi-sws.org/FCS/expiris.
1.1    Example
To illustrate our method, consider the following program, which simulates tossing a
coin until we see a heads, counting a cost of 1 unit for every coin toss:
      toss _ := tick 1;;
               if ChooseUniform [h, t] = t then toss ()
      toss ()

In this language, tick is a primitive that increases the incurred cost by 1. We would
like to show that the expected cost of this program does not exceed 2. Specifically,
we can show in ExpIris that after any number of execution steps, the expected cost
does not exceed 2.



                                           2
The coin toss example is a typical example in expected cost analysis. The probability
that we have to toss at least once is 12 , the probability that we have to toss at least
twice is 41 = 212 , and so on. In total we get
                          ∞
                          X 1            1
            E[Tosses] =            =          =2             (geometric series)
                          i=1
                              2i       1 − 21
In ExpIris, we can show the Hoare Triple:
                           {$2, True} toss () {v. 0, v = ()}
which intuitively means the following: given that the precondition True holds, a
potential of 2 is enough to cover the expected cost of executing toss (). Additionally,
if the program terminates, there is a potential of at least 0 left, and the return value
is (). The postcondition of “there is a potential of at least p left” is discussed in more
detail in Section 4.
The proof proceeds by Löb induction, which, intuitively, is induction on the number
of steps that the program is executed for. It allows us to assume that the statement
we want to show already holds for the recursive call, but we have to do at least
one program step before applying the induction hypothesis. In ExpIris, this rule is
sound for expected cost analysis even for possibly non-terminating programs like the
example discussed in the section (because the postcondition is guaranteed to hold if
the program terminates).
The first statement to be executed is a tick, which reduces our (available) potential
from 2 to 1. The next statement is a uniform choice. This probabilistic branching
allows us to distribute the remaining potential of 1 among the cases. We can choose
to give the heads-case a potential of 0 and the tails-case a potential of 2. This is a
valid choice, since the expected potential is still 21 ×0+ 21 ×2 = 1. The proof continues
for the two cases separately. After the if is evaluated, we are left with two goals:
          {$0, True} () {v. 0, v = ()}        {$2, True} toss () {v. 0, v = ()}
The first goal is trivially true, and the second one holds by the induction hypothesis.
This concludes the proof.
After proving this triple, we apply ExpIris’s adequacy theorem, which yields that if
the program is executed for up to n steps (for any n), the expected cost will not
exceed 2.
This example is verified formally in Section 4.3.
2   Preliminaries: The Iris Base Logic
Iris is separated into a base logic that defines basic connectives and modalities, and
a program logic that is defined on top of the base logic. We leave the Iris’ base logic
untouched and only modify the program logic. In this section, we briefly summarize
the part of the Iris base logic that is used in this report.
Iris propositions include the following:
     P, Q ∈ iProp ::= True | False | P ∧ Q | P ∨ Q | ¬P | P ⇒ Q | ∃x. P | ∀x. P |
                                                   N
                       P −∗ Q | P ∗ Q | ⊲ P | P        | E1 |⇛E2 P | ℓ 7→ v



                                              3
Iris is a separation logic [19, 20]. The base ingredients for a separation logic are the
separating conjunction P ∗Q and the magic wand P −∗ Q. The separating conjunction
P ∗ Q asserts that the available resources can be separated (linearly) into two parts,
one of which satisfies P , and the other Q. For example, ℓ 7→ v is a resource asserting
that the heap location ℓ stores the value v. A statement ℓ 7→ v ∗ l′ 7→ v ′ means that
the heap can be separated into two parts, one satisfying ℓ 7→ v, the other satisfying
ℓ′ 7→ v ′ ; in particular, we must have that ℓ 6= ℓ′ .
The wand P −∗ Q asserts that if we disjointly add resources that satisfy P , then the
total resources satisfy Q: it holds that P ∗ (P −∗ Q) ⊢ Q.
                  N
The notation P      describes a sharable invariant with namespace N . Typically, the
program logic enforces all invariants to hold after every program step: It is possible
to open an invariant to obtain P but later in the proof, P has to be restored to again,
closing the invariant.
The fancy update modality E1 |⇛E2 P , allows updating the available resources before
proving P . The update is needed, for example, for keeping the resources ℓ 7→ v
and the physical heap in sync. The fancy update specifically says that P holds in
resources obtained after (1) opening all invariants contained in E1 , then (2) updating
our resources, and then (3) closing all invariants contained in E2 . Note that P holds
in a state where the invariants in E1 \E2 are open and those in E2 are closed.
The later modality ⊲ P asserts that P holds after the next program step. The later
modality supports Löb induction, which lifts induction on program steps to the logic:
                                        Löb
                                        ⊲P ⇒ P
                                          P

3     Probabilistic Language
3.1   Definition
Next, we adapt Iris’ definition of a language to the probabilistic setting.
Iris is language-agnostic: the framework can be instantiated with a language of the
user’s choice. In Iris, a language consists of expressions Expr, that describe pro-
grams in this language, the values Val that a program can evaluate to, and states
State, that can, for example, be used to model the memory state of a machine.
The operational semantics of the language is given by a primitive reduction relation
(−, − − →t −, −, −) ⊆ (Expr × State) × (Expr × State × List(Expr)) that for each
pair of expression and state, specifies what steps the program can take next. More
                    →t e′ , σ ′ , ~e means that the expression e can reduce to e′ , changing
specifically, e, σ, −
                 ′
the state to σ and forking the expressions in ~e as new threads. For example, in a
simple language, for an arbitrary state σ and expressions e, e′ , the following three
reduction triples might hold:

                      if true then e else e′ , σ −
                                                 →t       e, σ, []
                                 l ← 5, [l 7→ 3] −
                                                 →t       (), [l 7→ 5], []
                                      fork e, σ −→t       (), σ, [e]



                                               4
For cost analysis, we modify this description of languages. First, the description
also specifies the cost of each step. Second, it is necessary to capture the probability
distribution of possible next steps. Therefore, we modify the stepping relation so that
a pair of expression and state now steps to a distribution over tuples of expression,
state, cost and forked expressions. This leads to a new form of primitive reduction
relation.
Definition 3.1 (Discrete distribution) For P   a countable set X, a distribution over
X is a function µ ∈ (X → R≥0 ) that satisfies x∈X µ(X) = 1. The support of a
distribution is the set of outcomes with nonzero probability: supp(µ) = {x ∈ X |
µ(x) > 0}.

We are only interested in discrete distributions with finite support and we write D(X)
for the set of such distribution over X.
Definition 3.2 (Probabilistic Language) A probabilistic language is a tuple
(Expr, Val, State, −
                   →t ), where Expr is the set of expressions, Val ⊆ Expr is the set of
values, State is the set of possible states, and

       (−, − −
             →t −) ⊆ (Expr × State) × D(Expr × State × R≥0 × List(Expr))

is the primitive reduction relation. Additionally, values must not step:

                                 ∀e, σ, µ. e, σ −
                                                →t µ ⇒ e ∈
                                                         / Val

For example, an expression f lip that simulates a fair coin flip, could step to the value
heads with probability 12 and to the value tails with probability 12 , and incur a cost
of 1:
                               (
                                 heads, σ, 1, [] with probability 21
                  flip, σ −→t
                                 tails, σ, 1, [] with probability 21

Next, we show how to combine the individual steps into a relation modeling n steps
of program execution. This will be needed for stating the adequacy theorem (see
Section 5). Adequacy states, amongst others, that proving a weakest precondition in
ExpIris ensures that the expected cost does indeed not exceed the stated bound after
n steps of program execution (for any n).
Since we support concurrency, the reduction relation needs to be generalized from
individual expressions to thread pools. We follow the Iris approach of interleaving
thread reductions arbitrarily so, at any point in time, any thread may step next.
Additionally, we now allow starting with a nonzero cost:

  (−, −, − →tp −) ⊆ (List(Expr) × State × R≥0 ) × D(List(Expr) × State × R≥0 )

                                      e, σ →t µ
    T ++ [e] ++ T , σ, c →tp map(µ, λ(e′ , σ ′ , c′ , ~e). (T ++ [e′ ] ++ T ′ ++ ~e), σ ′ , c + c′ )
                    ′
                                                                                    X
                                                   where map(µ, f )(y) :=                     µ(x)
                                                                                   x∈f −1 (y)




                                                   5
Next, we define a relation, denoted →ntp , modeling up to n steps of program execution.
For composing multiple steps, we apply (a special case of) the bind operation of the
Giry Monad [6] of distributions.

                        bind : D(X) → (X → D(Y )) → D(Y )
                                           X
                           bind(µ, κ)(y) =   µ(x) · κ(x)(y)
                                                   x∈X

Intuitively, for obtaining y after at most n steps, we first have to step to some x in
step 1, and then from x to y with at most n − 1 additional steps. To obtain the total
probability of reaching y, we sum up the probabilities for all possible intermediate
steps x.

  (−, −, − →ntp −) ⊆ (List(Expr) × State × R≥0 ) × D(List(Expr) × State × R≥0 )


                            T, σ, c →ntp δ(T,σ,c)         (n ≥ 0)


        T, σ, c −
                →tp µ    ∀(T ′ , σ ′ , c′ ) ∈ supp(µ). T ′ , σ ′ , c′ − n−1
                                                                      →tp   κ((T ′ , σ ′ , c′ ))
                                          →ntp bind(µ, κ)
                                  T, σ, c −

3.2   Example Language: Probabilistic Heap Lang
We instantiate the framework above with a concrete probabilistic language by ex-
tending Iris’ example language HeapLang for probabilistic programming. HeapLang
is a simple but expressive language supporting concurrency, both imperative and
functional programming, higher-order state and programs. We make the following
extensions to the language:
  • We add support for the manipulation of reals (to model costs and probabilities).
  • We add the new primitive tick that increases the cost by the specified amount.
  • We add the probabilistic primitives ChooseUniform and ChooseWeighted.
    ChooseUniform uniformly samples a value from a given list. ChooseWeighted
    samples a value from a list of pairs, where each pair contains a value and a
    real number. The number represents the weight of this value. The weights are
    normalized to sum to 1 and interpreted as probabilities, and a value is sampled.
  • We add a shallow embedding of Coq lists to HeapLang to simplify working with
    the new probabilistic primitives.
The following grammar defines the syntax of ProbHeapLang, where z ∈ Z, r ∈ R,




                                               6
ℓ ∈ Loc and vs ∈ List Val:

 v, w ∈Val ::= z | r | vs | true | false | () | ℓ |
               recv f (x) = e | (v, w)v | inlv (v) | inrv (v)
  e ∈ Expr ::= v | x | rece f (x) = e | e1 (e2 ) |
                − e | e1 + e2 | e1 − e2 | e1 · e2 | e1 /e2 | e1 :: e2
                e1 < e2 | e1 ≤ e2 | e1 = e2 | e1 ∧ e2 | e1 ∨ e2 | if e then e1 else e2 |
                (e1 , e2 )e | fst(e) | snd(e) |
                inle (e) | inre (e) | match e with inl ⇒ e1 | inr ⇒ e2 end |
                AllocN(e1 , e2 ) | Free(e) | ! e | e1 ← e2 |
                CmpXchg(e1 , e2 , e3 ) | Xchg(e1 , e2 ) | FAA(e1 , e2 ) |
                fork {e} |
                tick e | ChooseUniform e | ChooseWeighted e

The semantics is mostly standard. Non-probabilistic primitives step to a Dirac distri-
bution of the form δx , which assigns the value x the probability 1. ! ℓ reads location ℓ
and ℓ ← v stores v in location ℓ. CmpXchg is an atomic compare-and-store primitive,
while Xchg is an atomic load-and-store. FAA(ℓ, z) is an atomic primitive that reads ℓ
and adds z to its value.
The reduction rules for the new constructs – tick and the probabilistic primitives –
are as follows.
                                                                             1
                                    vs 6= []        ∀v ∈ vs. µ((v, σ, 0, [])) =
            r ∈ R≥0                                                      length(vs)
     tick r, σ −
               →t δ((),σ,r,[])                   ChooseUniform vs, σ −
                                                                     →t µ

                                                                            r             X
  vs 6= []     ∀v ∈ vs. v = (r, v ′ )v ∧ r ∈ R+ ∧ µ((v ′ , σ, 0, [])) =           s=                 r
                                                                            s
                                                                                       (r,v ′ )∈vs
                                 ChooseWeighted vs, σ −
                                                      →t µ




                                                7
4   Probabilistic Weakest Precondition
In Iris, the heart of the program logic is the weakest precondition. Proving a weakest
precondition wp e {Φ} shows that e executes safely and if it terminates in a value v,
v fulfills the postcondition Φ.
To enable expected cost analysis, we extend the weakest precondition with two new
parameters: the initial potential p ∈ R and the postcondition potential P ∈ V al → R.
Then, the weakest precondition
           $p wp e {P, Φ}      or equivalently     $p wp e {v. P(v), Φ(v)}
intuitively means that the initial potential p is enough to cover the expected cost of
executing e and additionally, if e terminates in a value v, we still have a potential of
P(v) left. Additionally, as in standard Iris, safe execution of e and the fulfillment of
the postcondition Φ are guaranteed.
In particular, proving $p wp e {P, Φ} ensures that the expected cost of executing e
does not exceed p. The postcondition potential P enables modular proofs. To see
why it is useful, consider the following example:
        toss _ := if ChooseUniform [true, false] then 1
                      else 1 + toss ()
        Tick(toss ())

This is a variant of the coin toss example discussed in Section 1.1. Here, we first
count the number of coin tosses and then incur a cost of this amount. To prove
that this program has an expected cost of at most 2, we can first prove the weakest
precondition $2 wp toss() {v. v, True} by induction. This shows that if we execute
toss() with an initial potential of 2, we can distribute this potential in a way such
that if we terminate with a value v, then the final potential is also v. Next, we also
show that $v wp tick v {v. 0, True}, which directly follows from the rule wp-tick.
Then, the two parts of the proof are connected using the rule wp-bind:
        wp-bind                                           wp-tick
        $p wp e {v. P′ (v), $P′ (v) wp K[v] {P, Φ}}             ⊲ Φ ()
                    $p wp K[e] {P, Φ}                     $c wp tick c {0, Φ}
The rule wp-bind allows us to reason about a composed expression by reasoning
about both parts sequentially. The rule says that we should first evaluate e with the
initial potential p, yielding value v and potential P′ (v), and then continue the proof
for K[v] with the potential that remains in for this case. For proving the example
above, we can instantiate the rule in the following way:

                   $2 wp toss () {v. v, $v wp tick (v) {0, True}}
                           $2 wp tick toss () {0, True}
The premise of the rule follows from the two triples we discussed earlier.
The weakest precondition further satisfies the following rules:
                                  wp-value
                                  P(v) ≤ p     Φv
                                   $p wp v {P, Φ}


                                           8
                 wp-add-pot                                        upd-wp
                    p′ ≥ 0     $p wp e {P, Φ}                      |⇛$p wp e {P, Φ}
                 $(p + p ) wp e {λv. Pv + p′ , Φ}
                        ′
                                                                    $p wp e {P, Φ}

              wp-mono
              p ≤ p′        ∀v. Pv ≥ P′ v   ∀v. Φv −∗ Ψv                  $p wp e {P, Φ}
                                      $p′ wp e {P′ , Ψ}

A pure step is a deterministic computation step that has no side effects: e →pure e′ ,
∀σ. e, σ −
         →t δ(e′ ,σ,0,[]) . The weakest precondition is closed under the inverse of pure
reductions.
                                  wp-pure
                                  $p wp e′ {P, Φ}     e →pure e′
                                          $p wp e {P, Φ}

Additionally, the following rules hold for primitives of ProbHeapLang:


                       wp-choose-uniform                 X
                       l 6= []     ∀v ∈ l. Φ v                 P(v) ≤ p · length l
                                                         v∈l
                                  $p wp ChooseUniform l {P, Φ}

If there is a uniform choice in the program, the postcondition potential
                                                                P        P specifies how
to distribute the potential p among the fibers. The condition v∈l P(v) ≤ p · length l
ensures that the expected available potential does not increase. Moreover, we have
to show the postcondition for each value in the list.


   wp-choose-weighted                                                       P
                                   ′             ′                    ′         (r,v)∈vs r · P(v)
   vs 6= []      ∀v ∈ vs, ∃r, v . v = (r, v ) ∗ r > 0 ∗ Φ v                     P                   ≤p
                                                                                    (r,v)∈vs r
                                 $p wp ChooseWeighted vs {P, Φ}

For a weighted choice, we have to prove that the list in input indeed consists of pairs
of reals and values that fulfill the postcondition. The premise
                                                      
                             X                     X
                                   r · P(v) /        r ≤ p
                                 (r,v)∈vs                  (r,v)∈vs


ensures that the expected value of the available potential does not increase. (The
denominator normalizes the sum of the weights 1.)


                                  wp-fork
                                   ⊲ Φ ()    ⊲ $p wp e {0, True}
                                      $p wp fork {e} {0, Φ}



                                                     9
When a new thread is forked, it can use up the full available potential.
In addition to the above rules, all rules for the primitives from HeapLang (except for
prophecy) hold in ExpIris if we define the standard Iris precondition as:
                              wp e {Φ} , $0 wp e {0, Φ}
Those rules can be generalized to any arbitrary nonnegative potential using the rule
wp-add-pot. Moreover, proofs of HeapLang programs in Iris + HeapLang are also
ExpIris + ProbHeapLang proofs as long as they don’t make use of prophecies and
later credits. This allows us to use the existing library of verified HeapLang programs
when carrying out proofs in ProbHeapLang.
4.1   Recap of the Iris Weakest Precondition Definition
For the purposes of our exposition, we show a slightly simplified definition of the
standard Iris weakest precondition wp e {Φ}. We will adapt this definition to ExpIris
in the next section. The full definition is a bit more expressive: it additionally allows
the state interpretation to depend on the step counter and the number of threads,
it is parametric in whether the program is allowed to get stuck, parametric in the
postcondition that should hold for forked threads, and may contain more laters in
every step.
Additionally, this definition does not include prophecy variables or later credits. A
line-by-line explanation can be found below.
                    wp(S) , µwp rec. λE, e, Φ.                                       (1)
                             (e ∈ V al ∧ |⇛E Φ(e)) ∨                                 (2)
                             
                              e∈/ V al ∧ ∀σ. S(σ) −∗ E |⇛∅ red(e, σ)∗                (3)
                             ∀e′ , σ ′ , ~e. (e, σ −
                                                   →t e′ , σ ′ , ~e) −∗              (4)
                             ⊲ ∅|⇛E S(σ ′ ) ∗ wp rec(E, e′ , Φ) ∗                    (5)

                                    ∗ wp rec(⊤, e′′ , True)
                                    e′′ ∈~
                                         e
                                                              
                                                                                     (6)

  1. The weakest precondition is parametric in the state interpretation S. The state
     interpretation connects the physical state to the logic. It has to be preserved by
     every program step. For more details on how the state interpretation is used,
     we refer to Iris [9].
  2. If the program has terminated in a value, the postcondition must hold for that
     value.
  3. Next, consider the case that the program has not yet reduced to a value. The
     machine could now be in any state σ that fulfills the state interpretation. First,
     one must show that the expression is reducible, which means that the program
     should not be stuck. For this part of the proof, the invariants can stay open.
  4. Next, consider all possible combinations of expression, state, and forked expres-
     sions that the program could step to.
  5. Since the program reduced one step, the remaining formula is under a later
     modality. At this point, one has to close the invariants again, and can also


                                               10
      update the resources. The state interpretation must hold on the new state, and
      the weakest precondition must hold recursively for the next expression.
  6. All forked threads should execute safely.
4.2   Definition of the ExpIris Weakest Precondition
Next, we turn to the formal definition of the ExpIris weakest precondition. Compared
to the current Iris version, we drop support for prophecy and later credits. Addition-
ally, the definition shown in this section is simplified in the same way as the Iris
weakest precondition was simplified in the previous section. For the full definition,
see Appendix A
When an expression steps to a distribution µ in ExpIris, one has to choose how to
distribute the available potential among the fibers of µ. To avoid unnecessary side
conditions on the functionality of this potential distribution, we allow the user to give
the potential distribution as a list p~. For defining the expected value of such a list,
                     Pn order on the support of µ and define for n = |supp(µ)| =
we assume an arbitrary
length(~        p] = i=1 µ(supp(µ)i ) · p~i . After the potential has been distributed,
        p): Eµ [~
we have to (recursively) show a weakest precondition for each fiber in its allocated
potential.
The ExpIris weakest precondition is shown below with changes relative to the standard
Iris weakest precondition are highlighted in yellow . A line-by-line explanation of the
changes can be found below.

           wp(S) , µwp rec. λE, e, Φ, p, P .                                         (1)
                    (e ∈ V al ∧ |⇛E Φ(e) ∧ p ≥ P(e) ) ∨                              (2)
                    
                     e∈/ V al ∧ ∀σ. S(σ) −∗ E |⇛∅ red(e, σ) ∗ p ≥ 0 ∗                (3)

                               →t µ) −∗ ⊲ |⇛∅ ∃~
                     ∀µ. (e, σ −                         p] ≤ p − E( , ,c)∼µ [c] ∗
                                                  p. Eµ [~                           (4)
                              ^                           X
                                           ∃p′′ , pt.
                                                  ~ p′′ +      ~ ≤ p′ ∧
                                                               pt                    (5)
                     p′ ;(e′ ,σ′ , ,~
                                    e)∈~
                                       p;supp(µ)

                                  ′               ′      ′′
                          ∅|⇛E S(σ ) ∗ wp rec(E, e , Φ, p , P ) ∗                    (6)

                               ∗
                           e′′ ;p′′′ ∈~ ~
                                      e;pt
                                             wp rec(⊤, e′′ , True, p′′′ , 0 )
                                                                             
                                                                                     (7)


  1. The weakest precondition definition takes the initial and final potentials as
     additional parameters.
  2. When e is a value, in addition to proving the postcondition Φ, we have to show
     that the initial potential is at least as large as the final postcondition.
  3. The potential should never become negative. This is a standard requirement in
     the method of potentials.
  4. We now have to consider all possible distributions that the expression can step
     to. Fix such a distribution µ. The expected cost E( , ,c)∼µ [c] incurred by this
     execution step is deducted from the potential, and we have to choose how to



                                                    11
      distribute the remaining potential among the fibers of µ. This later distribution
      is given by a list of potentials ~p, which must have one entry for every fiber.
      This can be done in any way, as long as the expected value does not exceed the
      remaining potential. The invariants can remain open up to this point.
  5. V
     Once the potential is distributed, we reason separately for each fiber (the big
       ), and the distribution µ becomes irrelevant. Consider a concrete fiber with
     an assigned potential of p′ . If new threads were forked, we have to decide how
     to distribute the potential among all threads. p′′ is the potential for the main
                  ~ are the potentials for the forked threads. Again, these can be
     thread, and pt
     chosen arbitrarily as long as their sum is at most p′ .
  6. The state interpretation has to hold on the new state, and the proof continues
     recursively for the reduct expression and the initial potential p′′ .
                                                                  ~ assigned to them.
  7. All forked threads should execute safely with the potentials pt
We define the following notation:

                         $p wpS e {P, Φ} , wp(S) ⊤ e Φ p P
                               wpS e {Φ} , $0 wpS e {0, Φ}

When the state interpretation S is unambiguously fixed in the context, we often omit
it from $p wpS e {P, Φ} and simply write $p wp e {P, Φ}. We then define:

                       {$p, P } e {P, Ψ} , P ⊢ $p wp e {P, Ψ}

4.3   Example
We now formally verify the example that was already discussed at a high level in
Section 1.1.
toss _ := tick 1;;
         if ChooseUniform [h, t] = t then toss ()
toss ()

Recall that we want to prove that {$2, True} toss() {v. 0, v = ()}. A formal proof
outline is shown below. The initial goal is at the top of the diagram, and the following
steps are a (linearized) representation of the proof tree.




                                          12
Context:                                                                                                    Goal:
                                                                                 {$2, True} toss() {v. 0, v = ()}
                                                                                      $2 wp toss() {v. 0, v = ()}
⊲ $2 wp toss () {v. 0, v = ()}                                                        $2 wp toss() {v. 0, v = ()}
by Löb induction.
$2 wp toss () {v. 0, v = ()}
                             $2 wp tick 1; ; if ChooseUniform [h, t] = t then toss() {v. 0, v = ()}
by wp-pure.
$2 wp toss() {v. 0, v = ()}
           $2 wp tick 1 {v ′ . 1, $1 wp v ′ ; ; if ChooseUniform [h, t] = t then toss() {v. 0, v = ()}}
by wp-bind.
$2 wp toss() {v. 0, v = ()}
           $1 wp tick 1 {v ′ . 0, $1 wp v ′ ; ; if ChooseUniform [h, t] = t then toss() {v. 0, v = ()}}
by wp-add-pot
$2 wp toss() {v. 0, v = ()}
                                   $1 wp (); ; if ChooseUniform [h, t] = t then toss() {v. 0, v = ()}
by wp-tick, wp-value
$2 wp toss() {v. 0, v = ()}
                                      $1 wp if ChooseUniform [h, t] = t then toss() {v. 0, v = ()}
by wp-pure.
$2 wp toss() {v. 0, v = ()}
            $1 wp ChooseUniform [h, t] {v ′ . P(v ′ ), $P(v ′ ) wp if v ′ = t then toss() {v. 0, v = ()}}
by wp-bind with P(h) = 0, P(t) = 2.
apply wp-choose-uniform
Subgoal 1                                                                      P
                                                                                   v ′ ∈[h,t] P(v) ≤ 1 · length([h, t])
                                                                                                            0+2≤2
                                                                                                                     X
Subgoal 2
$2 wp toss() {v. 0, v = ()}
                                                 ∀v ′ ∈ [h, t]. $P(v ′ ) wp if v ′ = t then toss() {v. 0, v = ()}
Subgoal 2.1
                                                                         $0 wp if h=t then toss() {v.0, v = ()}
                                                                                                $0 wp () {v.0, v = ()}
by wp-pure
                                                                                                      0 ≤ 0 ∧ () = ()
                                                                                                                    X
by wp-value
Subgoal 2.2
$2 wp toss() {v. 0, v = ()}
                                                                         $0 wp if t=t then toss() {v.0, v = ()}
$2 wp toss() {v. 0, v = ()}
                                                                                        $2 wp toss() {v. 0, v = ()}
                                                                                                                    X
by wp-pure, Assumption.



                                               13
While this proof is quite verbose on paper, it is only three lines of code within the Coq
formalization (instead of values heads, tails which don’t exist in ProbHeapLang,
we use true and false).
Proof.
  wp_pures. iLob as "IH". wp_tick. iNext. wp_pures.
  wp_choose_uniform (fun v, match v with | #true => 2 | _ => 0 end).
  repeat iSplit; (auto || by wp_pures).
Qed.

The routine application of the rules wp-bind and wp-add-pot is handled automati-
cally by our tactics wp tick and wp choose uniform. For the uniform choice, the user
only has to provide a function that specifies how to distribute the potential. Since
the proof showing that the expected value does not increase is trivial in this case,
it is also handled automatically. wp-value is also applied automatically whenever
possible.
5    Adequacy
The adequacy theorem says that proving a weakest precondition implies the following
three statements:
    1. The postcondition Φ holds for all threads that have terminated in values.
    2. Progress: the program does not get stuck. If it terminates, it does so in a value.
    3. The expected sum of the final cost and the postcondition potential does not
       exceed the sum of the initial potential and the initial cost. In other words,
       the expected cost of the verified program, which is the difference between the
       expected final cost and the initial cost does not exceed the difference between
       the expected final potential and the initial potential. The expected sum of cost
       and postcondition potential for a distribution µ and a potential postcondition
       P is expressed by the following function ECP (µ).

                                            µ : D(List(Expr) × State × R)
                                                 (
                                                   c + P(e1 ) if e1 ∈ V al
                      CostP ((e1 ++ ~e, σ, c)) ,
                                                   c          else.
                                    ECP (µ) , Eµ [CostP ]

       Note that the potential postcondition only applies to the main thread, and thus
      ~e is irrelevant in CostP ((e ++ ~e, σ, c)).
                                                              →ntp µ. For (3), the
All proofs of (1)–(3) above proceed by induction over e, σ, c −
induction step follows from a variant of the law of total expectation, that allows
us to compose the expected cost bounds for each fiber into a bound for the whole
distribution:
Lemma 5.1

                 (∀p′ ; (e, σ, c) ∈ p~; supp(µ). ECP (κ(e, σ, c)) ≤ p′ + c) →
                                 ECP (bind(µ, κ)) ≤ E( , ,c)∼µ [c] + Eµ [~
                                                                         p]



                                             14
The three parts are, together with the soundness result of the Iris’ base logic, com-
posed into a full adequacy theorem, which can be found in Appendix B. For simplicity,
we only present a slightly weaker corollary in this section: Proving a weakest precon-
dition and the state interpretation for the initial state indeed shows that Claims (1)
- (3) hold:
Theorem 5.2 (Adequacy) Given an initial expression e, state σ, and cost c, some
pure proposition ϕ : V al → P rop, and potential postcondition P, the following holds
for the execution of e:

S(σ) ∗ $p wp e {v. P(v), ϕ(v)} →
             →ntp µ → (v :: T ′ , σ ′ , c′ ) ∈ supp(µ) → ϕ(v) ∧
                                                             
 ([e], σ, c) −                                                                        (postcondition)
             →ntp µ → (T ′ , σ ′ , c′ ) ∈ supp(µ) → e′ ∈ T ′ → ¬stuck(e′ , σ ′ )
                                                                               
 ([e], σ, c) −                                                                     ∧ (progress)
             →ntp µ → ECP (µ) ≤ p + c
                                             
 ([e], σ, c) −                                                                        (expected cost)

6     Case Studies
6.1    Probabilistic Binary Counter
In this section, we discuss a probabilistic variant of a classical example for amortized
cost analysis: the binary counter. In the deterministic variant of this example, one
shows that the amortized number of bit flips needed for incrementing a binary counter
(of any bit width) is in O(1), even though individual increments can be more expen-
sive. We analyze a probabilistic version of the binary counter example, where a bit
flip only succeeds with probability p. Each bit flip is repeated until it succeeds.
We analyze the following implementation of this example in ProbHeapLang. The
counter is implemented by an array of size n. The program iterates through the array
from the least significant to the most significant bit, and flips every bit up to and
including the first unset (0) bit.
      incr_counter n l p :=
      (rec incr l i n :=
          if i = n then ()
          else flip_bit (l + i) p ;;
             if !(l + i) // (l + i)th bit is now 1
             then ()
             else incr l (i + 1) n)
       l 0 n.

The implementation of flip bit is similar to the implementation of the coin toss
example in Section 1.1
      flip_bit :=
      rec flip l p :=
          Tick 1;;
          if ChooseWeighted [(p, true), (1-p, false)]
          then l <- not (!l)
          else flip l p.




                                                15
Similar to the coin toss example, we can show that the expected cost needed for one
bit flip is bounded by 1/p.
We would like to show that m increments do not incur a cost larger than 2m
                                                                         p .

      rec incr_m l m :=
          if m = 0 then ()
          else incr_counter n l p;; incr_m l (m-1)

Theorem 6.1 Let n ∈ N+ , m ∈ N, p ∈ R with 0 < p < 1. Then
              
            2m
       ⊢$        wp let ℓ = init_counter n in incr_m ℓ m {0, True}
             p

For proving this theorem, the key observation is that in each increment, we flip at
most one bit from 0 to 1. We get a potential of 2/p for each increment, of which
we use half, i.e., 1/p, to “pay” for the cost of flipping the 0 to a 1, and we use the
remaining 1/p, to “pay in advance” for flipping the bit back to 0 eventually.
More precisely, we maintain a potential of 1/p for every set (1) bit in the counter.
Whenever we flip a 1 to a 0, we “pay” for that flip using the potential that was
associated with this bit. When we flip a 0 to a 1, we instead use 1/p of the additional
potential to pay for the flip itself and associate the remaining 1/p with the new 1 in
the counter. This strategy is captured by the following lemma.
Lemma 6.2 Let p ∈ R, 0 < p < 1, ℓ ∈ Loc, vs : list val, and n = length(vs).
Let B be a function that counts the number of ones in a list. Furthermore, define
is counter as is counter ℓ vs := ℓ 7→ ∗vs where vs is a boolean list. Then
                                                     
                        2 1
                          + · B(vs) , is counter ℓ vs
                        p p
                               incr_counter n ℓ p
                                                                
                            1
                         λ , · B(incr vs), is counter ℓ (incr vs)
                            p

The proof of Theorem 6.1 then proceeds by induction over the number of increments
m, applying Lemma 6.2 in the induction step.
6.2    Quicksort
Next, we use ExpIris to bound the expected number of comparisons in an imperative
in-place implementation of the quicksort algorithm. For simplicity, we assume that
the list contains no duplicates.
The function partition reorders an array by putting all elements not greater than
some pivot x in the beginning, and all other elements to the end of the array.




                                           16
  partition n l x :=
    (rec partition i j :=
    if j = n then 0
      else
        Tick 1;;
        if !(l + j) <= x
        then
          swap (l + i) (l + j);;
          1 + partition (i + 1) (j + 1)
        else
          partition i (j + 1)
    ) 0 0

qsort uses a derived construct ChooseRange a b, that models choosing uniformly
from the integers from a (inclusive) to b exclusive. It can be defined using ChooseUniform
on a list ranging from a to b − 1.
  qsort :=
    rec qsort l n :=
      if n <= 1 then ()
      else let i := ChooseRange 0 n in
      let pos := partition l n !(l + i) in
      qsort l pos;;
      qsort (l + pos) (n - pos)

We show a concrete bound of cost(n) := 2n · (1 + log4/3 (n)) for the number of com-
parisons.
Theorem 6.3 (Expected Number of Comparisons for Quicksort) Let vs be
an integer list that contains no duplicates. Let n = length(vs). Then

                       {$cost(n), l 7→ ∗ vs} qsort l n {0, True}

The proof proceeds by induction on n. The key idea for the induction step is to
distinguish “good” pivots, which lead to two sublists that are both significantly smaller
than the input list, and “bad” pivots, which lead to highly unbalanced lists. We then
show that the probability of choosing a good pivot is sufficiently large. This analysis
is inspired by typical textbook proofs.
A good pivot is one that splits the list in a way that the larger sublist has at most a
size of 34 th the size of the original list.
Lemma 6.4 (Good Pivot Split)
Let n > 0, 14 · n ≤ k ≤ 34 · n. Then cost(k) + cost(n − k) ≤ cost(n) − 3n.
Lemma 6.5 (Bad Pivot Split)
Let 0 < k ≤ n. Then cost(k) + cost(n − k) ≤ cost(n).

We know that partition incurs a cost of n for a list of length n, and that the number




                                           17
of good pivots is at least ⌊ n2 ⌋. For n ≥ 2, we have that ⌊ n2 ⌋ ≥ n3 . Therefore
       n
    1X                                     1 j n k                    lnm          
          n + cost(k) + cost(n − k) ≤ n +           · (cost(n) − 3n) +     · cost(n)
    n                                      n    2                       2
      k=1
                                                      jnk
                                    ≤ n + cost(n) +        · (−3)
                                                        2
                                    ≤ cost(n)

This allows us to distribute the potential of cost(n) such that if the pivot is the k-th
smallest element, we continue with a potential of n + cost(k) + cost(n − k). Then,
we use a potential of n to pay for the cost of partition, the potential of cost(k) to
pay for the first recursive call, and the potential of cost(n − k) to pay for the second
recursive call. This concludes the proof of Theorem 6.3
7    Limitations and Ongoing Work
ExpIris’ choice of making the potential a parameter of the weakest precondition limits
how potential can be used. A particular limitation is that it is impossible to make
the postcondition potential depend on the final state that the program terminates
in while adhering to standard Iris convention. Postconditions related to the state
at some location l are typically encoded in Iris as a proposition ∃v. l 7→ v ∗ Φ(v).
However, expressing the postcondition potential in the same way is not possible,
since the potential is not part of the logic. To understand why this is a problem,
consider the following example, which is again a variant of the coin toss example:
          toss l := if ChooseUniform [true, false] then ()
                        else l <- !l + 1
          let l := alloc 0 in toss l;;Tick(!l)

We would like to show that the expected cost of this example is at most 2. For that,
we would first have to show that if we execute toss l with an initial potential of
2, we can distribute the potential such that if we terminate in a state where l 7→ v,
we have a potential of v left. However, it is unfortunately impossible to express this
postcondition in ExpIris, since the potential is not part of the logic.
In ongoing work, we are exploring how to embed a general notion of probabilistic
resources in the base logic of Iris. We hope that making the potential a (probabilistic)
resource in the logic rather than a parameter of the weakest precondition will enable
the verification of examples like the one stated above.
8    Related Work
In concurrent work, Aguirre et al. [1] introduce Eris, an Iris-based framework for
reasoning about (expected) error bounds of probabilistic programs. The key novelty
of Eris is error credits, which can be distributed during the program execution to “pay”
for outcomes that do not satisfy the postcondition. (Expected) error credits behave
like the potential in our logic: When there is a probabilistic choice in the program,
they can be distributed any way among the branches as long as the expected value
does not increase. In contrast to our work, Aguirre et al. choose a different way
to implement this behavior: whereas in our work, the potential is a parameter of
the weakest precondition, they introduce a guarded lifting modality that is used in


                                            18
the weakest precondition to distribute the credits. As a consequence, they do not
encounter the limitation described in Section 7, but are also not able to support
concurrent programs.
Polaris [23] presents a different Iris-based approach for probabilistic reasoning. There,
proofs proceed by first relating the program to an abstract model (using Iris), and
then reasoning within that model about properties like expected cost. This is a very
general technique for probabilistic reasoning. However, the technique requires finding
a suitable abstract model. For expected cost analysis, the definition of an individual
cost model is required for every proof.
Non-probabilistic runtime analysis in Iris was first studied through the concept of
time credits [16]. ExpIris was inspired by this work in that our potential behaves like
time credits, but potential can be divided along probabilistic branching, which is a
concept that does not arise in the deterministic setting of [16].
A different, more general approach to probabilistic reasoning in separation logic re-
lies on a modality that represents probabilistic conditioning [13, 2], in combination
with an interpretation of the separating conjunction as probabilistic independence
[3]. However, all this work lacks fully modular reasoning (in the sense that there is
no rule similar to wp-bind), and the languages are sequential and first-order. We
implicitly use probabilistic conditioning after every program step – this is encoded
in the definition of the weakest precondition (see 4.2). In ongoing work, we are ex-
amining whether it is possible to support a similar proof strategy for ExpIris using a
conditioning modality.
There is also a rich line of work on automated amortized expected cost analysis [18, 24]
based on automated amortized resource analysis [8, 7]. Like our work, this line of
work is also based on potentials. However, the focus is on automatically deriving
polynomial bounds on expected costs of programs that make binary choices. Since
this approach is designed for automated analysis, there is no support for correctness
reasoning and it is, therefore, not suitable when the expected cost of a program
depends on its functional behavior.
Another line of work develops Hoare-like calculi for expected cost analysis [15, 11,
4], including amortized cost analysis, based on the method of potentials [4]. This
line of work follows a syntax-based approach for computing the expected runtime
of sequential first-order programs. Their support for correctness proofs is limited
compared to Iris.
References
 [1] Alejandro Aguirre, Philipp G Haselwarter, Markus de Medeiros, Kwing Hei Li,
     Simon Oddershede Gregersen, Joseph Tassarotti, and Lars Birkedal. Error cred-
     its: Resourceful reasoning about error bounds for higher-order probabilistic pro-
     grams. arXiv preprint arXiv:2404.14223, 2024.
 [2] Jialu Bao, Emanuele D’Osualdo, and Azadeh Farzan. Bluebell: An al-
     liance of relational lifting and independence for probabilistic reasoning.
     CoRR, abs/2402.18708, 2024.      doi: 10.48550/ARXIV.2402.18708.     URL
     https://doi.org/10.48550/arXiv.2402.18708.




                                           19
 [3] Gilles Barthe, Justin Hsu, and Kevin Liao. A probabilistic separation logic. Proc.
     ACM Program. Lang., 4(POPL):55:1–55:30, 2020. doi: 10.1145/3371123. URL
     https://doi.org/10.1145/3371123.
 [4] Kevin Batz, Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Math-
     eja, and Lena Verscht. A calculus for amortized expected runtimes. Proc.
     ACM Program. Lang., 7(POPL):1957–1986, 2023. doi: 10.1145/3571260. URL
     https://doi.org/10.1145/3571260.
 [5] Lars Birkedal, Thomas Dinsdale-Young, Armaël Guéneau, Guilhem Jaber,
     Kasper Svendsen, and Nikos Tzevelekos. Theorems for free from separation
     logic specifications. Proc. ACM Program. Lang., 5(ICFP):1–29, 2021. doi:
     10.1145/3473586. URL https://doi.org/10.1145/3473586.
 [6] Michele Giry. A categorical approach to probability theory. In Categorical Aspects
     of Topology and Analysis: Proceedings of an International Conference Held at
     Carleton University, Ottawa, August 11–15, 1981, pages 68–85. Springer, 2006.
 [7] Jan Hoffmann, Klaus Aehlig, and Martin Hofmann. Multivariate amor-
     tized resource analysis. In Thomas Ball and Mooly Sagiv, editors, Pro-
     ceedings of the 38th ACM SIGPLAN-SIGACT Symposium on Principles of
     Programming Languages, POPL 2011, Austin, TX, USA, January 26-28,
     2011, pages 357–370. ACM, 2011. doi: 10.1145/1926385.1926427. URL
     https://doi.org/10.1145/1926385.1926427.
 [8] Martin Hofmann and Steffen Jost. Static prediction of heap space usage for
     first-order functional programs. In Alex Aiken and Greg Morrisett, editors, Con-
     ference Record of POPL 2003: The 30th SIGPLAN-SIGACT Symposium on
     Principles of Programming Languages, New Orleans, Louisisana, USA, January
     15-17, 2003, pages 185–197. ACM, 2003. doi: 10.1145/604131.604148. URL
     https://doi.org/10.1145/604131.604148.
 [9] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars
     Birkedal, and Derek Dreyer.        Iris from the ground up:       A modu-
     lar foundation for higher-order concurrent separation logic.      J. Funct.
     Program., 28:e20, 2018.       doi:     10.1017/S0956796818000151.     URL
     https://doi.org/10.1017/S0956796818000151.
[10] Jan-Oliver Kaiser, Hoang-Hai Dang, Derek Dreyer, Ori Lahav, and Viktor
     Vafeiadis. Strong logic for weak memory: Reasoning about release-acquire
     consistency in iris. In Peter Müller, editor, 31st European Conference on
     Object-Oriented Programming, ECOOP 2017, June 19-23, 2017, Barcelona,
     Spain, volume 74 of LIPIcs, pages 17:1–17:29. Schloss Dagstuhl - Leibniz-
     Zentrum für Informatik, 2017. doi: 10.4230/LIPICS.ECOOP.2017.17. URL
     https://doi.org/10.4230/LIPIcs.ECOOP.2017.17.
[11] Benjamin Lucien Kaminski, Joost-Pieter Katoen, Christoph Matheja, and Fed-
     erico Olmedo. Weakest precondition reasoning for expected runtimes of random-
     ized algorithms. J. ACM, 65(5):30:1–30:68, 2018. doi: 10.1145/3208102. URL
     https://doi.org/10.1145/3208102.
[12] Robbert Krebbers, Amin Timany, and Lars Birkedal.           Interactive proofs in



                                          20
    higher-order concurrent separation logic. In Giuseppe Castagna and Andrew D.
    Gordon, editors, Proceedings of the 44th ACM SIGPLAN Symposium on Prin-
    ciples of Programming Languages, POPL 2017, Paris, France, January 18-
    20, 2017, pages 205–217. ACM, 2017. doi: 10.1145/3009837.3009855. URL
    https://doi.org/10.1145/3009837.3009855.
[13] John M. Li, Amal Ahmed, and Steven Holtzen. Lilac: A modal separation logic
     for conditional probability. Proc. ACM Program. Lang., 7(PLDI):148–171, 2023.
     doi: 10.1145/3591226. URL https://doi.org/10.1145/3591226.
[14] Yusuke Matsushita, Xavier Denis, Jacques-Henri Jourdan, and Derek Dreyer.
     RustHornBelt: a semantic foundation for functional verification of Rust pro-
     grams with unsafe code. In Ranjit Jhala and Isil Dillig, editors, PLDI
     ’22: 43rd ACM SIGPLAN International Conference on Programming Lan-
     guage Design and Implementation, San Diego, CA, USA, June 13 - 17,
     2022, pages 841–856. ACM, 2022. doi: 10.1145/3519939.3523704. URL
     https://doi.org/10.1145/3519939.3523704.
[15] Annabelle McIver and Carroll Morgan.     Abstraction, Refinement and
     Proof for Probabilistic Systems.   Monographs in Computer Science.
     Springer, 2005. ISBN 978-0-387-40115-7. doi: 10.1007/B138392. URL
     https://doi.org/10.1007/b138392.
[16] Glen Mével, Jacques-Henri Jourdan, and François Pottier.    Time Cred-
     its and Time Receipts in Iris. In Luı́s Caires, editor, Programming Lan-
     guages and Systems - 28th European Symposium on Programming, ESOP
     2019, Held as Part of the European Joint Conferences on Theory and
     Practice of Software, ETAPS 2019, Prague, Czech Republic, April 6-11,
     2019, Proceedings, volume 11423 of Lecture Notes in Computer Science,
     pages 3–29. Springer, 2019.    doi: 10.1007/978-3-030-17184-1\ 1.   URL
     https://doi.org/10.1007/978-3-030-17184-1_1.
[17] Ike Mulder and Robbert Krebbers. Proof automation for linearizability in sep-
     aration logic. Proc. ACM Program. Lang., 7(OOPSLA1):462–491, 2023. doi:
     10.1145/3586043. URL https://doi.org/10.1145/3586043.
[18] Van Chan Ngo, Quentin Carbonneaux, and Jan Hoffmann. Bounded expec-
     tations: resource analysis for probabilistic programs. In Jeffrey S. Foster
     and Dan Grossman, editors, Proceedings of the 39th ACM SIGPLAN Con-
     ference on Programming Language Design and Implementation, PLDI 2018,
     Philadelphia, PA, USA, June 18-22, 2018, pages 496–512. ACM, 2018. doi:
     10.1145/3192366.3192394. URL https://doi.org/10.1145/3192366.3192394.
[19] Peter W. O’Hearn. Resources, concurrency, and local reasoning. Theor. Com-
     put. Sci., 375(1-3):271–307, 2007. doi: 10.1016/J.TCS.2006.12.035. URL
     https://doi.org/10.1016/j.tcs.2006.12.035.
[20] John C. Reynolds.     Separation logic: A logic for shared mutable data
     structures. In 17th IEEE Symposium on Logic in Computer Science (LICS
     2002), 22-25 July 2002, Copenhagen, Denmark, Proceedings, pages 55–74.
     IEEE Computer Society, 2002. doi: 10.1109/LICS.2002.1029817. URL
     https://doi.org/10.1109/LICS.2002.1029817.



                                       21
[21] Michael Sammler, Rodolphe Lepigre, Robbert Krebbers, Kayvan Memarian,
     Derek Dreyer, and Deepak Garg. RefinedC: automating the foundational ver-
     ification of C code with refined ownership types. In Stephen N. Freund and
     Eran Yahav, editors, PLDI ’21: 42nd ACM SIGPLAN International Conference
     on Programming Language Design and Implementation, Virtual Event, Canada,
     June 20-25, 2021, pages 158–174. ACM, 2021. doi: 10.1145/3453483.3454036.
     URL https://doi.org/10.1145/3453483.3454036.
[22] David Swasey, Deepak Garg, and Derek Dreyer.           Robust and com-
     positional verification of object capability patterns.  Proc. ACM Pro-
     gram. Lang., 1(OOPSLA):89:1–89:26, 2017. doi: 10.1145/3133913. URL
     https://doi.org/10.1145/3133913.
[23] Joseph Tassarotti and Robert Harper. A separation logic for concurrent ran-
     domized programs. Proc. ACM Program. Lang., 3(POPL):64:1–64:30, 2019. doi:
     10.1145/3290377. URL https://doi.org/10.1145/3290377.
[24] Di Wang, David M. Kahn, and Jan Hoffmann. Raising expectations: automating
     expected cost analysis with types. Proc. ACM Program. Lang., 4(ICFP):110:1–
     110:31, 2020. doi: 10.1145/3408992. URL https://doi.org/10.1145/3408992.




                                      22
Appendix
A    Full Weakest Precondition Definition
Changes to the Iris weakest precondition are highlighted in yellow.

          wp(S, ΦF , s) , µwp rec. λE, e, Φ, p, P .
                           (∃v. expr to val(e) = v ∧ |⇛E Φ(v) ∧ p ≥ P(v)) ∨

                                                                                       ∗
                           
                            expr to val(e) = ⊥ ∧ ∀σ, ns , nt . S(σ, ns , nt ) E ≡− ∅ ∗

                           (s = NotStuck ⇒ red(e, σ)) ∗ p ≥ 0 ∗ ∀µ. (e, σ, −
                                                                           →t µ) −∗
                           (|⇛∅ ⊲ |⇛∅ )n⊲ (ns )+1 ∃~                       p] ≤ p ∗
                                                   p. E( , ,c)∼µ [c] + Eµ [~
                                     ^                            X
                                                  ∃p′ , pt.
                                                        ~ p′′ +       ~ ≤ p′ ∧
                                                                      pt
                            p′ ;(e′ ,σ′ ,~
                                         e, )∈~
                                              p;supp(µ)

                                                 ′
                                                         e|) ∗ wp rec(E, e′ , Φ, p′′ , P ) ∗
                                 ∅|⇛E S(ns + 1, σ , n + |~


                                      ∗
                                  e′′ ;p′′′ ∈~ ~
                                             e;pt
                                                    wp rec(⊤, e′′ , ΦF , p′′′ , 0 )
                                                                                   


         S;ΦF
    $p wps;⊤  e {P, Φ} , wp(S, ΦF , s) e Φ p P
            S;ΦF              S;ΦF
          wps;⊤  e {Φ} , $0 wps;top e {0, Φ}

B    Full Adequacy Theorem
Theorem B.1 (Adequacy) Assume we are given some ~e, σ, c, n, µ such that
           →ntp µ. Moreover, assume we are given , a stuckness parameter s and meta-
(~e, σ, c) −
level property ϕ that we want to show. To verify that ϕ holds, it is sufficient to
                                ~ and (T2 , σ2 , c2 ) ∈ supp(µ) such that the following Iris
show that there exist lists p~, P
entailment holds:


                                                           ∗
                                                                              
                   ~ ΦF . S(σ1 , 0, 0) ∗ 
         ⊢ |⇛⊤ ∃S, Φ,                                                 $p wpS;Φ
                                                                           s;⊤ e {P, Φ} ∗
                                                                               F       
                                                    e;Φ;p;P∈~
                                                            e,Φ;~ ~
                                                              ~ p,P
                 ~ F
                                           
              S;Φ;Φ
             Cs;~ ~ (µ, T2 , σ2 ) ⊤⇛∅ ϕ̂
                p;P;c




                                                      23
where
    ~
C S;Φ;Φ                 e2 , T2′ . T2 = ~e2 ++ T2′ ∗
     ~ (µ, T2 , σ2 ) , ∃~
        F
  s;~
    p;P;c
                           |~e1 | = |~e2 | ∗
                           (s = NotStuck ⇒ ∀e ∈ T2 . expr to val(e) 6= ⊥ ∨ red(e, σ2 )) ∗
                           ∃n′ , n′ ≤ n. S(σ2 , n′ , |T2′ |) ∗
                                           X
                           ECP (µ) ≤ c +        p~ ∗


                               ∗
                                                                                 
                                          expr to val(e) 6= ⊥ −∗ Φ(expr to val(e)) ∗
                               e,Φ∈~   ~
                                   e2 ,Φ



                               ∗
                                                                               
                                      expr to val(e) 6= ⊥ −∗ ΦF (expr to val(e))
                               e∈T2′


Where ϕ̂ embeds ϕ into ExpIris.




                                                 24
