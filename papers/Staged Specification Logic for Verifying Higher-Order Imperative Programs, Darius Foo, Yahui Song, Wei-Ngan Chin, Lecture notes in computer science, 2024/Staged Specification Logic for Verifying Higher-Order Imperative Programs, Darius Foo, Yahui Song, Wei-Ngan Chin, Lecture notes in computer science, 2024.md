                                                   Staged Specification Logic for Verifying
                                                     Higher-Order Imperative Programs

                                             Darius Foo( )[0000−0002−3279−5827] , Yahui Song[0000−0002−9760−5895] , and
                                                              Wei-Ngan Chin[0000−0002−9660−5682]

                                                    School of Computing, National University of Singapore, Singapore
arXiv:2308.00988v2 [cs.PL] 2 Jul 2024




                                                               {dariusf,yahuis,chinwn}@comp.nus.edu.sg



                                                 Abstract. Higher-order functions and imperative states are language
                                                 features supported by many mainstream languages. Their combination
                                                 is expressive and useful, but complicates specification and reasoning, due
                                                 to the use of yet-to-be-instantiated function parameters. One inherent
                                                 limitation of existing specification mechanisms is its reliance on only two
                                                 stages : an initial stage to denote the precondition at the start of the
                                                 method and a final stage to capture the postcondition. Such two-stage
                                                 specifications force abstract properties to be imposed on unknown func-
                                                 tion parameters, leading to less precise specifications for higher-order
                                                 methods. To overcome this limitation, we introduce a novel extension to
                                                 Hoare logic that supports multiple stages for a call-by-value higher-order
                                                 language with ML-like local references. Multiple stages allow the behav-
                                                 ior of unknown function-type parameters to be captured abstractly as
                                                 uninterpreted relations; and can also model the repetitive behavior of
                                                 each recursion as a separate stage. In this paper, we define our staged
                                                 logic with its semantics, prove its soundness and develop a new auto-
                                                 mated higher-order verifier, called Heifer, for a core ML-like language.


                                        1      Introduction
                                        Programs written in modern languages today are rife with higher-order func-
                                        tions [3, 34], but specifying and verifying them remains challenging, especially if
                                        they contain imperative effects. Consider the foldr function from OCaml. Here
                                        is a good specification for it in Iris [17], a state-of-the-art framework for higher-
                                        order concurrent separation logic that is built using Coq proof assistant.

                                                                       (∀ x, a′ , ys. {P x ∗ Inv ys a′ } f (x, a′ ) {r. Inv (x::ys) r})
                                                                                                                                         
                                            ∀ P, Inv , f, xs, l.
                                                                       ∗ isList l xs ∗ all P xs ∗ Inv [] a
                                                                                       foldr f a l
                                                                               {r. isList l xs ∗ Inv xs r}

                                            While this specification is conventional in weakest-precondition calculi like
                                        Iris, one might argue that that this specification is not the best possible specifica-
                                        tion for foldr , since it requires two abstract properties Inv and P to summarize
                                        the behaviour of f . Moreover, the input list l is also immutable, through the
2       Darius Foo, Yahui Song, Wei-Ngan Chin

same isList predicate in both its pre- and postcondition. (If mutation of list is
allowed, a more complex Inv with an extra mutated list parameter is required.)
    These abstract properties must be correspondingly instantiated for each in-
stance of f , but unfortunately some usage scenarios (to be highlighted later in
Sec 2.2) of foldr cannot be captured by this particular pre/post specification of
Iris, despite how well-designed it was. Thus, the conventional pre/post approach
to specifying higher-order functions currently suffers from possible loss in preci-
sion in its specifications since the presence of these abstract properties implicitly
strengthens the preconditions for higher-order imperative methods.
    This paper proposes a new logic, Higher-Order Staged Specification Logic
(HSSL), for specifying and verifying higher-order imperative methods. It is de-
signed for automated verification via SMT and uses separation logic as its core
stateful logic, aiming at more precise specifications of heap-based changes. While
we have adopted separation logic to support heap-based mutations, HSSL may
also be used with other base logics, such as those using dynamic frames [24].
We next provide an overview of our methodology by examples before providing
formal details and an experimental evaluation of our proposal.

2     Illustrative Examples
We provide three examples to highlight the key features of our methodology.
2.1    A Simple Example
    We introduce the specification logic using 1 let hello f x y =
a simple example (Fig. 1), to highlight a key 2          x := !x + 1;
challenge we hope to solve, namely how should 3          let r = f y in
we specify the behavior of hello without pre- 4          let r2 = ! x + r in
committing to some abstract property on f ? 5            y := r2 ;
To do that, we can model f using an unin- 6              r2
terpreted relation. We use uninterpreted rela-
tion rather than a function here in order to         Fig. 1: A Simple Example
model both over-approximation and possible
side-effect. Since f is effectful and may modify arbitrary state, including the
references x and y, a modular specification of hello must express the ordering of
the call to f with respect to the other statements in it so that the caller of hello
may reason precisely about its effects. Therefore, a first approximation is the
following specification. We adopt standard separation logic pre/post assertions
and extend them with sequential composition and uninterpreted relations. A fi-
nal parameter (named as res here) is added to denote the result of each staged
specification’s relation (hello here), a convention we follow henceforth.
hello(f, x, y, res) =
  ∃ a · req x 7→ a;                     // Stage 1: requiring x be pre-allocated
  ens[ ] x 7→ a+1;                      // Stage 2: ensuring x is updated
  ∃ r · f (y, r);                       // Stage 3: unknown higher-order f call
  ∃ b · req x 7→ b ∗ y 7→ ;             // Stage 4: requiring x , y be pre-allocated
  ens[res] x 7→ b ∗ y 7→ res∧res =b+r   // Stage 5: y is updated, and x is unchanged
    Staged Specification Logic for Verifying Higher-Order Imperative Programs                    3

    We can summarize the imperative behavior of hello before the call to f with
a read from x , followed by a write to x , as captured by Stages 1-2. The same
applies to the portion after the call to f (lines 4-6), but here we only consider the
scenario when x and y are disjoint 1 . Stages 4 and 5 state that memory location
x is being read while y will be correspondingly updated.
    The ordering of the unknown f call with respect to the parts before and after
does matter, so the call can be seen as stratifying the temporal behavior of the
function into stages. Should a specification for f become known, usually at a call
site, its instantiation may lead to a staged formula with only req/ens stages;
which can always be compacted into a single req/ens pair. We detail a normal-
ization procedure to do this in Section 3.2.
    As mentioned before, f can modify x despite not having direct access to it via
an argument, as it could capture x from the environment of the caller of hello.
To model this, we make worst-case assumptions on the footprints of unknown
functions, resulting in the precondition x 7→ b in stage 4.


2.2     Pre/Post vs Staged Specifications via foldr

We now specify foldr and compare it with the Iris specification from Section 1.

    1   let rec foldr f a l =             foldr (f, a, l, rr) =
    2     match l with
                                               ens[rr] l=[]∧rr=a
    3     | [] => a
    4     | h :: t =>
                                             ∨ ∃ x, r, l1 · ens[ ] l=x::l1 ;
    5       f h ( foldr f a t )                             foldr (f, a, l1 , r); f (x, r, rr)


    We model foldr as a recursive predicate whose body is a staged formula. The
top-level disjunction represents the two possible paths that result from pattern
matching. In the base case, when l is the empty list, and the result of foldr is a.
In the recursive case, when l is nonempty, the specification expresses that the
behavior of foldr is given by a recursive call to foldr on the tail of l to produce a
result r , followed by a call to f with r to produce a value for res. Crucially, we are
able to represent the call to the unknown function f directly in the specification,
without being forced to impose a stronger precondition on f .
    foldr ’s specification’s is actually very precise, to the point of mirroring the
foldr program. Nevertheless, abstraction may readily be recovered by proving
that this predicate entails a weaker formula, and a convenient point for this
would be when the unknown function-typed parameter is instantiated at each of
foldr ’s call sites; we discuss an example of this shortly. The point of specifying
foldr this way is that the precision of stages enables us not to have to commit
to an abstraction prematurely. We should, of course, summarize as early as is
appropriate to keep our proving process tractable.
1
    For simplicity, the intersection of specifications ∧sp that arises from disjoint pre-
    conditions is omitted (with some loss in precision) in the main paper, but its core
    mechanism is briefly described in Appendix D.
4            Darius Foo, Yahui Song, Wei-Ngan Chin

    Recursive staged formulae are needed mainly to specify higher-order func-
tions with unknown function-typed parameters. Otherwise, our preference is to
apply summarization to obtain non-recursive staged formulae whenever unknown
function-type parameters have been suitably instantiated. Under this scenario,
we may still use recursive pure predicates or recursive shape predicates in order
to obtain best possible modular specifications for our program code.
    Now, we show how the staged specification for foldr can be used by proving
that we can sum a list by folding it. sum can be specified in a similar way to foldr ,
but since this is a pure function that can be additionally checked for termination,
we can automatically convert it into a pure predicate (without any stages or
imperative side effects) to be used in (the pure fragment of) our specification
logic. Termination of pure predicates is required for them to be safely used in
specifications. (Techniques to check for purity and termination are well-known
and thus omitted.) Also, each pure predicate may be used as either a staged
predicate or a pure predicate. In case a pure predicate p(v ∗ , res) is used as a
staged predicate; its staged definition is:

                  p(v ∗ , res) = req emp∧pre(v ∗ ); ens[ ] emp∧p(v ∗ , res)

where pre(v ∗ ) denotes the precondition to guarantee termination and avoids ex-
ceptions. Note that p(v ∗ , res) is overloaded to be used as either a staged predicate
or a pure predicate. This is unambiguous from the context of its use.

    6    let rec sum li =
                                   sum(li, res) =
    7      match li with
                                       l=[]∧res=0
    8      | [] -> 0
    9      | x :: xs -> x + sum xs   ∨ ∃ r, l1 · l=x::l1 ∧sum(l1 , r)∧res=x+r


        We can now re-summarize an imperative use of foldr with the help of sum.

        10   let foldr_sum_state x xs init
        11   foldr sum state(x , xs, init, res) =
                  ∃ i, r · req x 7→ i; ens[res] x 7→ i+r∧res=r+init∧sum(xs, r)
        12   = let g c t = x := ! x + c ; c + t in foldr g xs init


This summarization gives rise to the following entailment:

                  ∀ m, xs, init , res. foldr (g, xs, init, res)
              ⊑   ∃ i, r · req x 7→ i; ens[res] x 7→ i+r∧res=r+init∧sum(xs, r)

    We have implemented a proof system for subsumption (denoted by ⊑) be-
tween staged formulae in our verifier, called Heifer. This particular entailment
can be proved automatically by induction on xs. While Iris’s earlier pre/post
specification for foldr can handle this example through a suitable instantiation
of (Inv ), it is unable to handle the following three other call instances.
  Staged Specification Logic for Verifying Higher-Order Imperative Programs                     5


13     let foldr_ex1 l = foldr ( fun x r -> let v = ! x
14                                          in x := v +1; v + r ) l 0
15     let foldr_ex2 l = foldr ( fun x r -> assert (x +r >=0) ; x + r ) l 0
16     let foldr_ex3 l = foldr ( fun x r -> if x >=0 then x + r
17                                          else raise Exc () ) l 0

    The first example cannot be handled since Iris’s current specification for
foldr expects its input list l to be immutable. The second example fails since
the precondition required cannot be expressed using just the abstract property
(P x). The last example fails because the abstract property (Inv (x :: ys) r)
used in the postcondition of f expects its method calls to return normally. In
contrast, using our approach via staged specification, we can re-summarize the
above three call instances to use the following subsumed specifications.
     foldr ex1 (l, res) ⊑ ∃ xs · req List(l , xs) ; ∃ ys ·
                          ens[res ] List(l, ys)∧mapinc(xs, ys)∧sum(xs, res)
     foldr ex2 (l, res) ⊑ req allSPos(l ) ; ens[res] sum(l, res)
     foldr ex3 (l, res) ⊑ ens[res ] allP os(l)∧sum(l, res) ∨ (ens[ ] ¬allP os(l); Exc())

    Note that the first example utilizes a recursive spatial List (l, xs) predicate,
while the last example used Exc() as a relation to model exception as a stage
in our specification. The three pure predicates and one spatial predicate used in
the above can be formally defined, as shown below.

mapinc(xs, ys) = (xs=[]∧ys=[]) ∨ (∃ x, xs1 , ys1 · xs=x::xs1 ∧ys=(x+1)::ys1
                                                     ∧ mapinc(xs1 , ys1 ))
allPos(l)      = (l=[]) ∨ (∃ x, l1 · l=x::l1 ∧allPos(l1 )∧x≥0)
allSPos(l)     = (l=[]) ∨ (∃ x, r, l1 · l=x::l1 ∧allSPos(l1 )∧sum(l, r)∧r≥0)
List (l, rs)   = (emp∧l=[]) ∨ (∃ x, rs1 , l1 · x 7→ r ∗ List (l1 , rs1 )∧l=x::l1 ∧rs=r::rs1 )

    We emphasize that our proposal for staged logics is strictly more expressive
than traditional two-stage pre/post specifications, since the latter can be viewed
as an instance of staged logics. As an example, the earlier two-stage specification
for foldr can be modelled non-recursively in our staged logics as:
      foldr(f, a, l, res) =
         ∃ P, Inv, xs · req List(l, xs) ∗ Inv ([], a)∧all(P, xs)
           ∧f (x, a′ , r)⊑(∃ ys · req Inv (ys, a′ )∧P (x); ens[r] Inv (x::ys, r)) ;
         ens[res] List (l, xs) ∗ Inv (xs, res)


2.3      Inferrable vs User-provided Specifications via map
    Our methodology for higher-order functions is further explicated by the
map method, shown in Fig. 2. Specifications typeset in lavender must be user-
supplied, whereas those shown in ◦ red (with the small circle) may be automated
or inferred (using the rules of Section 4). Like sum before, length and incrg may
be viewed as ghost functions, written only for their specifications to be used
to describe behavior. These specifications are also routine and can be mechani-
cally derived; we elide them here and provide them in Appendix A. The method
6        Darius Foo, Yahui Song, Wei-Ngan Chin


1    let rec length xs =                14   let rec map f xs =
      ◦                                      ◦
2       length(xs, res) = ...           15    map(f , xs, res) = ...
3        match xs with                  16     match xs with
4        | [] -> 0                      17     | [] -> []
5        | x :: xs1 ->                  18     | x :: xs1 ->
6          1 + length xs1               19       f x :: map f xs1
7                                       20

8    let rec incrg init li =            21   let map_incr xs x
     ◦
9      incrg(init, li , res) = ...      22   map incr (xs, x, r) =
10       match li with                           ∃ i · req x 7→ i; ∃ m · ens[r] x 7→ i+m
11       | [] -> []                               ∧ length(xs, m)∧incrg(i+1, xs, r)
12       | x :: xs -> init ::           23   = let f a = x := ! x +1; ! x
13            incrg ( init + 1) xs      24     in map f xs

Fig. 2: Implementation of map incr with a Summarized Specification from map

map incr describes the scenario we are interested in, where the state of the clo-
sure affects the result of map. Its specification states that the pointer x must
have its value incremented by the length of xs. Moreover, the contents of the
resulting list is captured by another pure function incrg, which builds a list of
as many increasing values as there are elements in its input list.
    These examples illustrate the methodology involved with staged specifica-
tions. They inherit the modular verification and biabduction-based[4] specifi-
cation inference of separation logic, adding the ability to describe imperative
behavior using function stages to the mix; biabduction then doubles as a means
to normalize and compact stages. There is emphasis on the inference of specifi-
cations and proof automation, and proofs are built out of simple lemmas, which
help summarize behavior and the shapes of data, and either remove recursion or
move it into a pure ghost function where it is easier to comprehend.
    In summary, staged logic for specifying imperative higher-order functions rep-
resents a fundamentally new approach that is more general and yet can be more
precise than what is currently possible via state-of-the-art pre/post specification
logics for imperative higher-order methods. Our main technical contributions to
support this new approach include:
 1. Higher-Order Staged Specification Logic (HSSL): we design a novel
    program logic to specify the behaviors of imperative higher-order methods
    and give its formal semantics.
 2. Biabduction-based Normalization: we propose a normalization proce-
    dure for HSSL that serves two purposes: (i) it allows us to produce succinct
    staged formulae for programs automatically, and (ii) it helps structure entail-
    ment proof obligations, allowing them to be discharged via SMT.
 3. Entailment: we develop a proof system to solve subsumption entailments
    between normalized HSSL formulae, prove its soundness, and implement an
    automated prover based on it.
 4. Evaluation: we report on initial experimental results, and present various
    case studies highlighting HSSL’s capabilities.
    Staged Specification Logic for Verifying Higher-Order Imperative Programs                    7

3      Language and Specification Logic

We target a minimal OCaml-like imperative language with higher-order func-
tions and state. The syntax is given in Fig. 3. Expressions are in ANF (A-normal
form); sequencing and control over evaluation order may be achieved using let-
bindings, which define immutable variables. Mutation may occur through heap-
allocated ref s. Functions are defined by naming lambda expressions, which may
be annotated with a specification Φ (covered below). For simplicity, they are
always in tupled form and their calls are always fully applied. Pattern matching
is encoded using recognizer functions (e.g., is cons) and if statements. assert
allows proofs of program properties to be carried out at arbitrary points.

    (Expressions ) e ::= v | x | let x=e1 in e2 | f (x∗ ) | ref x | x1 := x2 | !x | x1 :: x2 |
                         assert D | if x then e1 else e2
    (Values)       v ::= c | nil | x1 ::x2 | fun (x∗ ) Φ[r]→ e
    (Staged )      Φ ::= E | Φ1 ∨ Φ2 | Φ1 ; Φ2 | ∃ x∗ · Φ
    (Stage)       E ::= req D | ens[r] D | f (x∗ , r)                 (State) D ::= σ ∧ π
    (Heap)         σ ::= emp | x1 7→ x2 | σ1 ∗ σ2
    (Pure)         π ::= true | π1 ∨π2 | ¬π | ∃ x. π | t1 =t2 | a1 <a2 | Φ1 ⊑Φ2
    (A-Terms)      a ::= i | x | a1 + a2 | −a
    (Terms)        t ::= nil | t1 ::t2 | c | a | f | λ (x∗ , r)→ Φ

              c ∈ B ∪ Z ∪ unit                   i ∈Z                  x , f , r ∈ var

                Fig. 3: Syntax of the Core Language and Staged Logics

    Program behavior is specified using staged formulae Φ, which are disjunc-
tions and/or sequences of stages E. A stage is an assertion about program state
at a specific point. Each stage takes one of three forms: a precondition req D, a
postcondition ens[r] D with a named result r , or a function stage f (v ∗ , r), rep-
resenting the specification of a (possibly-unknown) function call. For brevity, we
use a context notation Φ[r ] where r explictly identifies the final result of specifi-
cation Φ. Program states D are described using separation logic formulae from
the symbolic heap fragment [4], without recursive spatial predicates (for simplic-
ity of presentation). Most values of the core language are as usual also terms of
the (pure) logic; a notable exception is the lambda expression fun (x∗ ) Φ[r]→ e,
which occurs in the logic as λ (x∗ , r)→ Φ[r], without its body. Subsumption as-
sertions between two staged formulae (Sec 5) are denoted by Φ1 ⊑Φ2 .

3.1      Semantics of Staged Formulae

From Triples to Stages Staged formulae generalize standard Hoare triples.
The standard partial-correctness interpretation of the separation logic Hoare
triple { P (v ∗ , x∗ ) } e { ∃y ∗ ·Q(v ∗ , x∗ , y ∗ , res) } where v ∗ denote valid pro-
gram variables and x ∗ denote specification variables (e.g., ghost variables) is
that for all states st satisfying P (v ∗ , x∗ ), given a reduction e, st      ∗
                                                                                v, st ′ , if
8       Darius Foo, Yahui Song, Wei-Ngan Chin

e, st 6 ∗ fault , then st ′ satisfies ∃y ∗ ·Q(v ∗ , x∗ , y ∗ , res). The staged equivalent
is { Φ } e { Φ; ∃ x∗ · req P (v ∗ , x∗ ); ∃ y ∗ · ens[ ] Q(v ∗ , x∗ , y ∗ , res) }. Apart from
mentioning the history Φ, which remains unchanged, its meaning is identical.
Consider, then, { Φ } e { Φ; req P1 ; ens[ ] Q1 ; req P2 ; ens[ ] Q2 } – an intuitive
extension of the semantics of triples is that given e, st ∗ e1 , st 1 , where st 1 sat-
isfies Q1 , the extended judgment holds if st 1 further satisfies P2 , and reduction
from there, e1 , st 1 ∗ e2 , st 2 , results in a state st 2 that satisfies Q2 .
     While heap formulae are satisfied by program states, staged formulae (like
triples), are satisfied by traces which begin and end at particular states. Uninter-
preted function stages further allow stages to describe the intermediate states of
programs in specifications – a useful ability in the presence of unknown higher-
order imperative functions, as we illustrate in Section 2 and Appendix C. To
formalize all this, we give a semantics for staged formulae next.

Formal Semantics We first recall the standard semantics for separation logic
formulae in Fig. 4, which provides a useful starting point.
      S , h|=σ ∧ π       iff   JπKS and S , h|=σ
      S , h|=emp         iff   dom(h) = {}
      S , h|=x 7→ y      iff   dom(h) = {S (x )} and h(S (x )) = JyKS
      S , h|=σ1 ∗ σ2     iff   ∃h1 h2 . h1 ◦h2 = h such that S , h1 |=σ1 and S , h2 |=σ2

                      Fig. 4: Semantics of Separation Logic Formulae
     Let var be the set of program variables, val the set of primitive values, and
loc ⊂ val the set of heap locations; ℓ is a metavariable ranging over locations.
The models are program states, comprising a store of variables S, a partial
mapping from a finite set of variables to values var ⇀ val , and the heap h, a
partial mapping from locations to values loc ⇀ val . JπKS denotes the valuation
of pure formula π under store S. dom(h) denotes the domain of heap h. h1 ◦h2 =h
denotes disjoint union of heaps; if dom(h1 )∩dom(h2 ) = {}, h1 ∪h2 = h. We write
h1 ⊆h2 to denote that h1 is a subheap of h2 , i.e., ∃ h3 · h1 ◦h3 =h2 . s[x:=v] and
s[x6:=] stand for store/heap updates and removal of keys.
     We define the semantics of HSSL formulae in Fig. 5. Let S, h S1 , h1 , R|=Φ
denote the models relation, i.e., starting from the program state with store S
and heap h, the formula Φ transforms the state into S1 , h1 , with an intermediate
result R. R is either Norm(r ) for partial correctness, Err for precondition failure,
or ⊤ for possible precondition failure in one of its execution paths.
     When Φ is of the form req σ∧π, the heap h is split into a heaplet h1 satisfying
σ∧π, which is consumed, and a frame h2 , which is left as the new heap. Read-only
heap assertions (σ∧π)@R under req check but do not change the heap.
     When Φ is of the form ens[ ] σ∧π, σ describes locations which are to be
added to the current heap. The semantics allows some concrete heaplet h1 that
satisfies σ∧π (containing new or updated locations) be (re-)added to heap h.
     When Φ is a function stage f (x∗ , r), its semantics depends on the specification
of f . A staged existential causes the store to be extended with a binding from x
  Staged Specification Logic for Verifying Higher-Order Imperative Programs                           9

  S, h    S, h1 , Norm( )|=req σ∧π          iff h1 ⊆h and S, h1 |=σ∧π
  S, h    S, h, Err |=req σ∧π               iff ∀h1 · h1 ⊆h ⇒ S, h1 6|=σ∧π
  S, h    S, h, R|=req (σ∧π)@R              iff S, h      S, h1 , R|=req (σ∧π)
  S, h    S, h◦h1 ,Norm(r)|=ens[r] σ∧π iff S, h1 |=σ∧π and dom(h1 )∩dom(h)={}
  S, h    S1 , h1 , R|=f (x∗ , r)           iff S(f ) = fun (y ∗ ) Φ[r ′ ]→ e,
                                                S, h      S1 , h1 , R|=[r ′ :=r][y ∗ :=x∗ ]Φ
  S, h    S1 , h1 , R|=∃ x · Φ              iff ∃v · S[x:=v], h       S1 , h1 , R|=Φ
  S, h    S2 , h2 , R|=Φ1 ; Φ2              iff S, h      S1 , h1 , Norm(r)|=Φ1 ,
                                                S1 , h1     S2 , h2 , R|=Φ2
  S, h    S1 , h1 , ⊤|=Φ1 ; Φ2              iff S, h      S1 , h1 , ⊤|=Φ1
  S, h    S3 , h3 , Norm(r3 )|=Φ1 ∨ Φ2      iff ∃h1 ,h2 ,r1 ,r2 · S, h      S1 , h1 , Norm(r1 )|=Φ1
                                                 and S, h       S2 , h2 , Norm(r2 )|=Φ2 , and
                                                (S3 , h3 , r3 )∈{(S1 , h1 , r1 ), (S2 , h2 , r2 )}
  S, h    S1 , h1 , ⊤|=Φ1 ∨ Φ2              iff S,h       S1 ,h1 ,⊤|=Φ1 or S,h      S1 ,h1 ,⊤|=Φ2

                            Fig. 5: Semantics of Staged Formulae
to an existential value v . Sequential composition Φ1 ;Φ2 results in a failure ⊤ if
Φ1 does, while disjunction Φ1 ∨Φ2 requires both branches not to fail.

3.2   Compaction

Staged formulae subsume separation logic triples, but triples suffice for many
verification tasks, particularly those without calls to unknown functions, and
we would like to recover their succinctness in cases where intermediate states
are not required. This motivates a compaction or normalization procedure for
staged formulae, written Φ ==> Φ (Fig. 6). Compaction is also useful for aligning
staged formulae, allowing entailment proofs to be carried out stage by stage; we
elaborate on this use in Section 5.
                                            req D1 ; req D2 ==> req (D1 ∗ D2 )
ens[ ] false ; Φ ==> ens[ ] false
                                        ens[ ] D1 ; ens[r] D2 ==> ens[r] (D1 ∗ D2 )
         emp; Φ ==> Φ
         Φ; emp ==> Φ                                 DA ∗ D1 ⊢ D2 ∗ DF
                                         ens[r] D1 ; req D2 ==> req DA ; ens[r] DF

                                 Fig. 6: Select compaction rules

   The three rules on the left simplify flows. A false postcondition (ens σ∧false)
models an unreachable or nonterminating program state, so the rest of a flow
may be safely ignored. emp in the next two rules is either (req emp∧true) or
(ens emp∧true); either may serve as an identity for flows. The first two rules on
the right merge consecutive pre- and postconditions. Intuitively, they are sound
because symbolic heaps separated by sequential composition must be disjoint to
be meaningful – this follows from the use of disjoint union in Fig. 5. The last rule
10        Darius Foo, Yahui Song, Wei-Ngan Chin

allows a precondition req D2 to be transposed with a preceding postcondition
ens D1 . This is done using biabduction [4], which computes a pair of antiframe
DA and frame DF such that the antiframe is the new precondition required,
and frame is what remains after proving the known precondition. The given rule
assumes that D1 and D2 are disjoint2 . A read-only @R heap assertion under
req would be handled by matching but not removing from DF (see [8]).
    Thus staged formulae can always be compacted into the following form, con-
sisting of a disjunction of flows θ (a disjunction-free staged formula)3 , each
consisting of a prefix of function stages (preceded by a description of the inter-
mediate state at that point), followed by a final pre- and postcondition, capturing
any behavior remaining after calling unknown functions.

     Φ ::= θ | Φ ∨ Φ
      θ ::= (∃ x∗ · req D; ∃ x∗ · ens[ ] D; f (v ∗ , r) ; )∗ ∃ x∗ · req D; ∃ x∗ · ens[ ] D

    An example of compaction is given below (Fig. 7, left). We start at the first
two stages of the flow and solve a biabduction problem (shown on the right,
with solution immediately below) to infer a precondition for the whole flow, or,
more operationally, to “push” the req to the left. We will later be able to rely
on the new precondition to know that a = 1 when proving properties of the
rest of the flow. Finally, we may combine the two ens stages because sequential
composition guarantees disjointness. Normalization is sound in the sense that it
transforms staged formulae without changing their meaning.

           ens x 7→ 1 ∗ y 7→ 2; req x 7→ a; ens x 7→ a+1
    <==> req a=1; ens y 7→ 2; ens x 7→ a+1                 DA ∗ x 7→ 1 ∗ y 7→ 2 ⊢ x 7→ a ∗ DF
    <==> req a=1; ens y 7→ 2 ∗ x 7→ a+1                          DA =(a=1), DF =(y 7→ 2)

                            Fig. 7: An example of compaction

Theorem 1 (Soundness of Normalization). Given Φ1 ==>Φ2 , if S, H                           S1 , H1 , R1 |=Φ1 ,
then S, H S1 , H1 , R1 |=Φ2 .

Proof. By case analysis on the derivation of Φ1 ==>Φ2 . See Appendix I.2.

4      Forward Rules for Staged Logics

To verify that a program satisfies a given specification Φs , we utilize a set of rules
(presented in Fig. 8) to compute an abstraction or summary of the program Φp ,
then discharge the proof obligation Φp ⊑Φs (covered in Section 5), in a manner
similar to strongest postcondition calculations.
   We make use of the following notations. denotes an anonymous existentially
quantified variable. [x:=v]Φ denotes the substitution of x with v in Φ, giving
2
     More exhaustive aliasing scenarios are considered in Appendix D.
3
     Using further normalization rules such as (Φ1 ∨Φ2 ); Φ3 ==> (Φ1 ; Φ3 )∨(Φ2 ;Φ3 )
  Staged Specification Logic for Verifying Higher-Order Imperative Programs                      11


   Φ1 ⊑Φ3    { Φ3 } e { Φ4 }      Φ4 ⊑Φ2                         { Φ1 } e { Φ2 }
                                             Consequence                             Frame
             { Φ1 } e { Φ2 }                                   { Φ; Φ1 } e { Φ; Φ2 }

           fresh res                                   fresh res
                                 Var                                         Val (c | nil | x1 ::x2 )
 { Φ } x { Φ ; ens[res] res =x }             { Φ } v { Φ ; ens[res ] res=v }
                                        fresh r
                                                              Ref
                            { Φ } ref x { Φ ; ens[r] r 7→ x }
                                      fresh a, res
                                                                          Deref
              { Φ } !x { Φ ; ∃ a · req x 7→ a ; ens[res ] x 7→ a∧res =a }
                                                                          Assign
                 { Φ } x1 :=x2 { Φ ; req x1 7→ ; ens[ ] x1 7→ x2 }

            { Φ; ens[ ] x } e1 { Φ1 [r1 ] } { Φ; ens[ ] ¬x } e2 { Φ2 [r2 ] }
                                                                             If
                   { Φ } if x then e1 else e2 { Φ1 ∨ [r2 :=r1 ]Φ2 }
                fresh x   { Φ } e1 { Φ1 [r] } { [r:=x]Φ1 } e2 { Φ2 }
                                                                     Let
                           { Φ } let x=e1 in e2 { ∃ x · Φ2 }
         fresh res { ens[ ] Pure(Φ) } e { Φp [r ′ ] } ([r ′ :=r]Φp )⊑Φs
                                                                         Lambda
           { Φ } fun (x∗ ) Φs [r]→ e { Φ ; ens[res] res=λ (x∗ , r)→ Φs }
             fresh res                                                                  Assert
                                      Call
   { Φ } f (x∗ ) { Φ ; f (x∗ , res) }             { Φ } assert D { Φ ; req D@R }

            Fig. 8: Forward Reasoning Hoare Rules with Staged Logics

priority to recently bound variables. We lift sequencing from flows to disjunctive
staged formulae in the natural way: Φ1 ; Φ2 , {θ1 ; θ2 | θ1 ∈ Φ2 , θ2 ∈ Φ2 }.
                                                 W

    The first two rules in Fig. 8 are structural. The Consequence rule uses speci-
fication subsumption (detailed in Section 5) in place of implication – a form of
behavioral subtyping. The Frame rule has both a temporal interpretation, which
is that the reasoning rules are compositional with respect to the history of the
current flow, and a spatial interpretation, consistent with the usual one from sep-
aration logic, if one uses the normalization rules (Section 3.2) to move untouched
p from the final states of Φ1 and Φ2 into the frame Φ.
    The Val rule illustrates how the results of pure expressions are tracked, in a
distinguished res variable. The Ref rule results in a new, existentially-quantified
location being added to the current state. The Deref and Assign rules are similar,
both requiring proof that a named location exists with a value, then respec-
tively either returning the value of the location and leaving it unchanged, or
changing the location and returning the unit value. Assert checks its heap state
without modifying it using the @R read-only annotation. If is where disjunctive
formula arises, and Let sequences expressions, renaming the intermediate result
of e1 accordingly. In the Let rule, program variable in staged formulae may ex-
tend scope of its corresponding variable in program code if no name clashes. It
becomes existentially quantified when the local variable is out of scope.
12      Darius Foo, Yahui Song, Wei-Ngan Chin

    The Lambda rule handles function definition annotated with a given specifi-
cation Φs . The body of the lambda is summarized into Φp starting from pure
information Pure(Φ) from its program context. Its behavior must be subsumed
by the given specification. The result is then the lambda expression itself.
    The Call rule is completely trivial, yet perhaps the most illuminating as to
the design of HSSL. A standard modular verifier would utilize this rule to look
up the specification associated with f , prove its precondition, then assume its
postcondition. In our setting, however, there is the possibility that f is higher-
order, unknown, and/or unspecified. Moreover, there is no need to prove the
precondition of f immediately, due to the use of flows for describing program
behaviors. Both of these point to the simple use of a function stage, which
stands for a possibly-unknown function call. Utilizing the specification of f , if it
is provided, is deferred to the unfolding done in the entailment procedure.
    We prove soundness of these rules, which is to say that derived specifications
faithfully overapproximate the programs they are derived from. In the following
theorem, e, h, S h1 , S1 is a standard big-step reduction relation whose defini-
tion we leave to Appendix I.1. Termination is also considered in Appendix I.5.
However, completeness is yet to be established.

Theorem 1 (Soundness of Forward Rules) Given { emp } e { Φ }, then
∀S, h, S2 , h1 · (S, h S2 , h1 , Norm(r)|=Φ) ⇒ ∃S1 · e, h, S Norm(v), h1 , S1 and
S1 ⊆ S2 and S1 (r) = v.
Proof. By induction on the derivation of e, h, S1     R1 , h1 , S1 . See Appendix I.3.

5    Staged Entailment Checking and its Soundness
In this section, we outline how entailments of the form F ⊢ Φp ⊑Φs may be
automatically checked. F denotes heap and pure frames that are propagated by
our staged logics entailment rules. Our entailment is always conducted over the
compacted form where non-recursive staged predicate definitions are unfolded,
while unknown predicates are matched exactly. Lemmas are also used to try
re-summarize each instantiation of recursive staged predicates to simpler forms,
where feasible. As staged entailment ensures that all execution traces that sat-
isfy Φp must also satisfy Φs , we rely on theory of behavioral subtyping [18] to
relate them. Specifically, we check that contravariance holds for pre-condition
entailment, while covariance holds for post-condition entailment, as follows:

           fresh y ∗   F0 ∗ D2 ⊢ (∃ x∗ . D1 ) ∗ F      F ⊢ θ a ⊑θ c
                                                                    EntReq
               F0 ⊢ (∃ x∗ · req D1 ; θa )⊑(∃ y ∗ · req D2 ; θc )
           fresh x∗     F0 ∗ D1 ⊢ (∃ y ∗ . D2 ) ∗ F    F ⊢ θa ⊑θc
                                                                    EntEns
             F0 ⊢ (∃ x · ens[r] D1 ; θa )⊑(∃ y ∗ · ens[r] D2 ; θc )
                      ∗

    More details of staged entailment rules are given in Appendix G. Note that
we use another entailment over separation logic D1 ⊢ D2 ∗ Fr that can propagate
residual frame, Fr . Lastly, we outline the soundness of staged entailemt against
the semantics of staged formulae, ensuring that all derivations are valid.
    Staged Specification Logic for Verifying Higher-Order Imperative Programs               13

Theorem 2 (Soundness of Entailment). Given Φ1 ⊑Φ2 and S, h Norm(r1 ), S1 , h1 |=Φ1 ,
then there exists h2 such that S, h Norm(r1 ), S2 , h2 |=Φ2 where h2 ⊆ h1 . (Here,
h1 ⊆ h2 denotes that ∃ h3 . h1 ◦h3 = h2 .)

Proof. By induction on the derivation of Φ1 ⊑Φ2 . See Appendix I.4.

6     Implementation and Initial Results
We prototyped our verification methodology in a tool named Heifer. Our tool
takes input programs written in a subset of OCaml annotated with user-provided
specifications. It analyzes input programs to produce normalized staged formu-
lae (Section 3.2, Section 4), which it then translates to first-order verification
conditions (Section 5) suitable for an off-the-shelf SMT solver. Here, our proto-
type targets SMT encodings via Why3 [12]. As an optimization, it uses Z3 [9]
directly for queries which do not require Why3’s added features.

Table 1: A Comparison with Cameleer and Prusti. (Programs that are natively
inexpressible are marked with “✗”. Programs that cannot be reproduced from Prusti’s
artifact [1] are marked with “-” denoting incomparable. We use T to denote the total
verification time (in seconds) and TP to record the time spent on the external provers.)

                               Heifer             Cameleer [22]           Prusti [31]
 Benchmark            LoC   LoS     T      TP    LoC LoS     T      LoC      LoS        T
 map                  13    11 0.66       0.58   10   45    1.25               -
 map closure          18     7     1.06   0.77        ✗                        -
 fold                 23    12 1.06       0.87   21   48    8.08               -
 fold closure         23    12 1.25       0.89        ✗                        -
 iter                 11     4     0.40   0.32        ✗                        -
 compose               3    1      0.11   0.09   2    6     0.05               -
 compose closure      23     4     0.44   0.32        ✗                       ✗
 closure [27]         27     5     0.37   0.27        ✗              13       11   6.75
 closure list          7    1      0.15   0.09        ✗                        -
 applyN                6    1      0.19   0.17   12   13    0.37               -
 blameassgn [13]      14     6     0.31   0.28        ✗              13        9   6.24
 counter              16     4     0.24   0.18        ✗              11        7   6.37
 lambda               13     5     0.25   0.22        ✗                        -
                      197   73                   45  112             37       27

    We have verified a suite of programs (Table 1) involving higher-order func-
tions and closures. As the focus of our work is to explore a new program logic
and subsumption-based verification methodology (rather than to verify existing
programs), the benchmarks are small in size, and are meant to illustrate the
style of specification and give a flavor of the potential for automation.
    Table 1 provides an overview of the benchmark suite. The first two sub-
columns show the size of each program (LoC) and the number of lines of user-
provided specifications (LoS) required. The next two give the total wall-clock time
taken (in seconds) to verify all functions in each program against the provided
specifications, and the amount of time spent in external provers.
14     Darius Foo, Yahui Song, Wei-Ngan Chin

    The next column shows the same programs verified using Cameleer [22, 25], a
state-of-the-art deductive verifier. Cameleer serves as a good baseline for several
reasons: it is representative of the dominant paradigm of pre/post specifications
and, like Heifer, targets (a subset of) OCaml. It supports higher-order functions
in both programs and specifications [26]. The most significant differences between
Cameleer and Heifer are that Cameleer does not support effectful higher-order
functions and is intended to be used via the Why3 IDE in a semi-interactive way
(allowing tactic-like proof transformations, used in the above programs).
    The last column shows results for Prusti [31]. Despite Rust’s ownership type
system, we compare it against Prusti because of its state-of-the-art support for
mutable closures, highlighting differences below. While we were able to reproduce
the claims made in Prusti’s OOPSLA 2021 artifact [1], we were not able to verify
many of our own benchmark programs due to two technical reasons, namely
lacking support for Rust’s impl Trait (to return closures) and ML-like cons
lists (which caused timeouts and crashes). Support for closures is also not yet
in mainline Prusti [2]. Nevertheless, we verified the programs we could use for
the artifact, the results of which are shown in Table 1. All experiments were
performed on macOS using a 2.3 GHz Quad-Core Intel Core i7 CPU with 16
GB of RAM. Why3 1.7.0 was used, with SMT solvers Z3 4.12.2, CVC4 1.8, and
Alt-Ergo 2.5.2. The Prusti artifact, a Docker image, was run using Moby 25.0.1.

User annotations required. Significantly less specification than code is re-
quired in Heifer, with an average LoS/LoC ratio of 0.37. This is helped by two
things: the use of function stages in specifications, and the use of biabduction-
based normalization, which allows the specifications of functions to be mostly
automated, requiring only properties and auxiliary lemmas to be provided. In
contrast, Cameleer’s ratio is 2.49, due to the need to adequately summarize the
behaviors of the function arguments and accompany these summaries with in-
variants and auxiliary lemmas. Two examples illustrating this are detailed in
Appendix F. Prusti’s ratio is 0.73, but a caveat is that in the programs for it,
only closure reasoning was used, without lemmas or summarization.

Expressiveness. Heifer is able to express many programs that Cameleer can-
not, particularly closure-manipulating ones. This accounts for the ✗ rows in
Table 1. While some of these can be verified with Prusti, unlike stages, Prusti’s
call descriptions do not capture ordering [11, 1]; an explicit limitation as shown
by the ✗ rows in Prusti’s column. Prusti is able to use history invariants and the
ownership of the Rust type system, but this difference is more than mitigated in
Heifer with the adoption of an expressive staged logic with spatial heap state;
more appropriate for the weaker (but more general) type system of OCaml.

7    Related Work
The use of sequential composition in specifications goes back to classic theories
of program refinement, such as Morgan’s refinement calculus [19] and Hoare
and He’s Unifying Theories [15], as well session types [10] and logics [7]. It has
    Staged Specification Logic for Verifying Higher-Order Imperative Programs   15

also been used to structure verification conditions and give users control over
the order in which they are given to provers [14], allowing more reliable proof
automation. We extend both lines of work, developing the use of sequential
composition as a precise specification mechanism for higher-order imperative
functions, and using it to guide entailment proofs of staged formulae.
    Higher-order imperative functions were classically specified in program logics
using evaluation formulae [16] and reference-reachability predicates [33]. The
advent of separation logic has allowed for simpler specifications using invariants
and nested triples (Section 1). These techniques are common in higher-order
separation logics, such as HTT [20], CFML [5], Iris [17] and Steel/Pulse [29],
which are encoded in proof assistants (e.g. Coq, F⋆ [28]) which do not natively
support closures or heap reasoning. While the resulting object logics are highly
expressive, they are much more complex (owing to highly nontrivial encodings)
and consequently less automated than systems that discharge obligations via
SMT. We push the boundaries in this area by proposing stages as a new, precise
specification mechanism which is compatible with automated verification.
    The guarantees of an expressive type system can significantly simplify how
higher-order state is specified and managed. Prusti [31] exploits this with call
descriptions (an alternative to function stages, as pure assertions saying that a
call has taken place with a given pre/post) and history invariants, which rely
on the ownership of mutable locations that closures have in Rust. Creusot [11]
uses a prophetic mutable value semantics to achieve a similar goal with pre/post
specifications of closures. Our solution is not dependent on an ownership type
system, applying more generally to languages with unrestricted mutation.
    Defunctionalization [23] is another promising means of reasoning about higher-
order effectful programs [26], pioneered by the Why3-based Cameleer [22]. This
approach currently does not support closures.
    Our approach to automated verification is currently based on strict evalua-
tion. It would be interesting to see how staged specifications can be extended to
support verification of lazy programs, as had been explored in [32] and [30].
8     Conclusion
We have explored how best to modularly specify and verify higher-order impera-
tive programs. Our contributions are manifold: we propose a new staged specifi-
cation logic, rules for deriving staged formulae from programs and normalizing
them using biabduction, and an entailment proof system. This forms the basis
of a new verification methodology, which we validate with our prototype Heifer.
    To the best of the authors’ knowledge, this work is the first to introduce a
fundamental staged specification mechanism for verifying higher-order impera-
tive programs without any presumptions; being more concise (without the need
for specifying abstract properties) and more precise (without imposing precon-
ditions on function-typed parameters) when compared to existing solutions.

Acknowledgments This research is supported by the Ministry of Education,
Singapore, under the Academic Research Fund Tier 1 (FY2023) (Project Title:
Automated Verification for Imperative Higher-Order Programs).
                         Bibliography


[1] Modular specification and verification of closures in Rust (artefact), 2021.
[2] Documentation of closures. https://github.com/viperproject/prusti-dev/issues/1431,
    2024.
[3] Fernando Alves, Delano Oliveira, Fernanda Madeiral, and Fernando Castor.
    On the bug-proneness of structures inspired by functional programming in
    JavaScript projects. CoRR, abs/2206.08849, 2022.
[4] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok
    Yang. Compositional shape analysis by means of bi-abduction. In Zhong
    Shao and Benjamin C. Pierce, editors, Proceedings of the 36th ACM
    SIGPLAN-SIGACT Symposium on Principles of Programming Languages,
    POPL 2009, Savannah, GA, USA, January 21-23, 2009, pages 289–300.
    ACM, 2009.
[5] Arthur Charguéraud. Characteristic formulae for the verification of imper-
    ative programs. In Manuel M. T. Chakravarty, Zhenjiang Hu, and Olivier
    Danvy, editors, Proceeding of the 16th ACM SIGPLAN international con-
    ference on Functional Programming, ICFP 2011, Tokyo, Japan, September
    19-21, 2011, pages 418–430. ACM, 2011.
[6] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao Qin. En-
    hancing modular OO verification with separation logic. In George C. Nec-
    ula and Philip Wadler, editors, Proceedings of the 35th ACM SIGPLAN-
    SIGACT Symposium on Principles of Programming Languages, POPL
    2008, San Francisco, California, USA, January 7-12, 2008, pages 87–99.
    ACM, 2008.
[7] Andreea Costea, Wei-Ngan Chin, Shengchao Qin, and Florin Craciun. Au-
    tomated modular verification for relaxed communication protocols. In Suky-
    oung Ryu, editor, Programming Languages and Systems - 16th Asian Sym-
    posium, APLAS 2018, Wellington, New Zealand, December 2-6, 2018, Pro-
    ceedings, volume 11275 of Lecture Notes in Computer Science, pages 284–
    305. Springer, 2018.
[8] Cristina David and Wei-Ngan Chin. Immutable specifications for more
    concise and precise verification. In Cristina Videira Lopes and Kathleen
    Fisher, editors, Proceedings of the 26th Annual ACM SIGPLAN Conference
    on Object-Oriented Programming, Systems, Languages, and Applications,
    OOPSLA 2011, part of SPLASH 2011, Portland, OR, USA, October 22 -
    27, 2011, pages 359–374. ACM, 2011.
[9] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. Z3: an efficient
    SMT solver. In C. R. Ramakrishnan and Jakob Rehof, editors, Tools and
    Algorithms for the Construction and Analysis of Systems, 14th Interna-
    tional Conference, TACAS 2008, Held as Part of the Joint European Con-
    ferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hun-
    gary, March 29-April 6, 2008. Proceedings, volume 4963 of Lecture Notes
    in Computer Science, pages 337–340. Springer, 2008.
 Staged Specification Logic for Verifying Higher-Order Imperative Programs   17

[10] Pierre-Malo Deniélou, Nobuko Yoshida, Andi Bejleri, and Raymond Hu.
     Parameterised multiparty session types. Log. Methods Comput. Sci., 8(4),
     2012.
[11] Xavier Denis and Jacques-Henri Jourdan. Specifying and verifying higher-
     order Rust iterators. In Sriram Sankaranarayanan and Natasha Sharygina,
     editors, Tools and Algorithms for the Construction and Analysis of Systems
     - 29th International Conference, TACAS 2023, Held as Part of the European
     Joint Conferences on Theory and Practice of Software, ETAPS 2022, Paris,
     France, April 22-27, 2023, Proceedings, Part II, volume 13994 of Lecture
     Notes in Computer Science, pages 93–110. Springer, 2023.
[12] Jean-Christophe Filliâtre and Andrei Paskevich. Why3 - where programs
     meet provers. In European Symposium on Programming, 2013.
[13] Robert Bruce Findler and Matthias Felleisen. Contracts for Higher-order
     Functions. In Mitchell Wand and Simon L. Peyton Jones, editors, Pro-
     ceedings of the Seventh ACM SIGPLAN International Conference on Func-
     tional Programming (ICFP ’02), Pittsburgh, Pennsylvania, USA, October
     4-6, 2002, pages 48–59. ACM, 2002.
[14] Cristian Gherghina, Cristina David, Shengchao Qin, and Wei-Ngan Chin.
     Structured specifications for better verification of heap-manipulating pro-
     grams. In Michael J. Butler and Wolfram Schulte, editors, FM 2011: Formal
     Methods - 17th International Symposium on Formal Methods, Limerick,
     Ireland, June 20-24, 2011. Proceedings, volume 6664 of Lecture Notes in
     Computer Science, pages 386–401. Springer, 2011.
[15] Jifeng He and Charles Antony Richard Hoare. Unifying theories of pro-
     gramming. In RelMiCS, 1998.
[16] Kohei Honda, Nobuko Yoshida, and Martin Berger. An observationally com-
     plete program logic for imperative higher-order frame rules. In 20th IEEE
     Symposium on Logic in Computer Science (LICS 2005), 26-29 June 2005,
     Chicago, IL, USA, Proceedings, pages 270–279. IEEE Computer Society,
     2005.
[17] Ralf Jung, Robbert Krebbers, Jacques-Henri Jourdan, Ales Bizjak, Lars
     Birkedal, and Derek Dreyer. Iris from the ground up: A modular foundation
     for higher-order concurrent separation logic. J. Funct. Program., 28:e20,
     2018.
[18] Gary T. Leavens and David A. Naumann. Behavioral subtyping, specifi-
     cation inheritance, and modular reasoning. ACM Trans. Program. Lang.
     Syst., 37(4):13:1–13:88, 2015.
[19] Carroll Morgan. The refinement calculus. In NATO ASI PDC, 1994.
[20] Aleksandar Nanevski, J. Gregory Morrisett, and Lars Birkedal. Hoare type
     theory, polymorphism and separation. J. Funct. Program., 18(5-6):865–911,
     2008.
[21] Peter W. O’Hearn. A primer on separation logic (and automatic program
     verification and analysis). In Tobias Nipkow, Orna Grumberg, and Benedikt
     Hauptmann, editors, Software Safety and Security - Tools for Analysis and
     Verification, volume 33 of NATO Science for Peace and Security Series - D:
     Information and Communication Security, pages 286–318. IOS Press, 2012.
18     Darius Foo, Yahui Song, Wei-Ngan Chin

[22] Mário Pereira and António Ravara. Cameleer: A deductive verification tool
     for OCaml. In Alexandra Silva and K. Rustan M. Leino, editors, Com-
     puter Aided Verification - 33rd International Conference, CAV 2021, Vir-
     tual Event, July 20-23, 2021, Proceedings, Part II, volume 12760 of Lecture
     Notes in Computer Science, pages 677–689. Springer, 2021.
[23] John C. Reynolds. Definitional interpreters for higher-order programming
     languages. In John J. Donovan and Rosemary Shields, editors, Proceedings
     of the ACM annual conference, ACM 1972, 1972, Volume 2, pages 717–740.
     ACM, 1972.
[24] Jan Smans, Bart Jacobs, and Frank Piessens. Implicit dynamic frames.
     ACM Trans. Program. Lang. Syst., 34(1):2:1–2:58, 2012.
[25] Tiago Soares and Mário Pereira. A framework for the automated verification
     of algebraic effects and handlers (extended version). ArXiv, abs/2302.01265,
     2023.
[26] Tiago Lopes Soares. A deductive verification framework for higher order
     programs. CoRR, abs/2011.14044, 2020.
[27] Kasper Svendsen. Modular specification and verification for higher-order
     languages with state. IT-Universitetet i København, 2013.
[28] Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine
     Delignat-Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Fournet,
     Pierre-Yves Strub, Markulf Kohlweiss, Jean Karim Zinzindohoue, and San-
     tiago Zanella Béguelin. Dependent types and multi-monadic effects in F. In
     Rastislav Bodı́k and Rupak Majumdar, editors, Proceedings of the 43rd An-
     nual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Languages, POPL 2016, St. Petersburg, FL, USA, January 20 - 22, 2016,
     pages 256–270. ACM, 2016.
[29] Nikhil Swamy, Aseem Rastogi, Aymeric Fromherz, Denis Merigoux, Danel
     Ahman, and Guido Martı́nez. Steelcore: an extensible concurrent separation
     logic for effectful dependently typed programs. Proc. ACM Program. Lang.,
     4(ICFP):121:1–121:30, 2020.
[30] Niki Vazou, Eric L. Seidel, and Ranjit Jhala. LiquidHaskell: experience with
     refinement types in the real world. In Wouter Swierstra, editor, Proceedings
     of the 2014 ACM SIGPLAN symposium on Haskell, Gothenburg, Sweden,
     September 4-5, 2014, pages 39–51. ACM, 2014.
[31] Fabian Wolff, Aurel Bı́lý, Christoph Matheja, Peter Müller, and Alexan-
     der J. Summers. Modular specification and verification of closures in Rust.
     Proc. ACM Program. Lang., 5(OOPSLA):1–29, 2021.
[32] Dana N. Xu, Simon L. Peyton Jones, and Koen Claessen. Static contract
     checking for Haskell. In Zhong Shao and Benjamin C. Pierce, editors, Pro-
     ceedings of the 36th ACM SIGPLAN-SIGACT Symposium on Principles
     of Programming Languages, POPL 2009, Savannah, GA, USA, January
     21-23, 2009, pages 41–52. ACM, 2009.
[33] Nobuko Yoshida, Kohei Honda, and Martin Berger. Logical reasoning for
     higher-order functions with local state. In Helmut Seidl, editor, Foundations
     of Software Science and Computational Structures, 10th International Con-
     ference, FOSSACS 2007, Held as Part of the Joint European Conferences
 Staged Specification Logic for Verifying Higher-Order Imperative Programs   19

     on Theory and Practice of Software, ETAPS 2007, Braga, Portugal, March
     24-April 1, 2007, Proceedings, volume 4423 of Lecture Notes in Computer
     Science, pages 361–377. Springer, 2007.
[34] Fiorella Zampetti, Francois Belias, Cyrine Zid, and Giuliano Antonioland
     Massimiliano Di Penta. An empirical study on the fault-inducing effect of
     functional constructs in Python. 2022 IEEE International Conference on
     Software Maintenance and Evolution (ICSME), pages 47–58, 2022.
20       Darius Foo, Yahui Song, Wei-Ngan Chin

Appendix

A      Inferred specifications
Inferred specifications for the examples in the paper.
    Pure predicates that can also be proven terminating are shown below. One
of them, namely range, has a precondition to ensure termination.

     length(xs, res) = xs=[]∧res=0
                       ∨ ∃ r, x, xs 1 · xs=x::xs 1 ∧length(xs 1 , r) ∧ res=r+1
incrg(init , li , res) = li =[]∧res=[]
                          ∨ ∃ r, x, xs1 · li =x::xs1 ∧incrg(init +1, xs1 , r) ∧ res=init ::r
       inc(x, res) = res=x+1
  range(x, n, res) = req n≥0;
                        ens[ ] n=0∧res=[] ∨ ∃ r · n>0∧range(x+1, n−1, r)∧res=x::r
    Note that the precondition to ensure termination of each pure predicate
would have been baked into the pure predicate’s definition itself. For example,
range(x , n, res) ⇒ n≥0 .
    Below are staged specifications for higher-order methods that have been in-
ferred. Since the unknown function parameter may be imperative, these higher-
order functions are currently only expressible in the staged specification format.


     map(f, xs, res) = ens[ ] xs=[] ∧ res=[]
                       ∨ ∃ h, x, xs1 · ens[ ] xs=x::xs1 ; f (x, h); ∃ t · map(f, xs1 , t);
                           ens[ ] res=h::t
applyN (f, x , n, res) = ens[ ] n=0 ∧ res=x
                         ∨ ens[ ] n6=0; ∃ r · f (x, r); applyN (f, r, n−1, res)
       take(f, n, res) = ens[ ] n=0 ∧ res=[]
                           ∨ ens[ ] n6=0; ∃ r, r2 · f (r); take(f, n−1, r2); ens[ ] res=r::r2


   Below is a staged specification for a first-order imperative method that has
been inferred. Two-staged pre/post specifications are always possible for first-
order imperative method that returns normally.


             integers(res) = ∃ a · req x 7→ a; ens[ ] x 7→ res∧res=a+1


B      Details on Mutable Closures
   We provide some verification details on an effectful higher-order function in
Fig. 9. Here counter is a function that captures a heap-allocated location x ,
     Staged Specification Logic for Verifying Higher-Order Imperative Programs            21


1     let mut_closure () ◦ m c(res) = ∃ x · ens[ ] x 7→ 2 ∧ res=1 =
2       let counter =
3           let x = ref 0 in
4           fun () ◦ λ(res) ∃ i · req x 7→ i; ens[ ] x 7→ i+1 ∧ res=i ->
5             let r = !x in x := !x + 1; r
6       in
        ◦
7         { ∃ x · ens[ ] x 7→ 0∧counter (res)=∃ i · req x 7→ i; ens[ ] x 7→ i+1∧res=i }
8       counter () ;
        ◦
9         { ∃ x · ens[ ] x 7→ 0∧counter (res)= · · · ; ∃ r · counter (r) }
        ◦
10        { ∃ x, r · ens[ ] x 7→ 1∧counter (res)= · · · ∧r=0 }
11      counter ()
        ◦
12        { ∃ x, r, counter · ens[ ] x 7→ 1∧counter (res)= · · · ∧r=0; counter (res) }
        ◦
13        { ∃ x, r, counter · ens[ ] x 7→ 2∧counter (res)= · · · ∧r=0∧res=1 }
        ◦
14        { ∃ x · ens[ ] x 7→ 2∧res=1 }


                Fig. 9: A higher-order function using a mutable closure


which is no longer in scope by the point counter is invoked. The specification
λ(res) (line 4) compositionally describes the behavior of the lambda expression
in counter: it updates the value of a known location x which initially has some
value i, which it returns. Reasoning about its enclosing let-expression (line 3),
however, we see that x is a new location, distinct from any other, resulting
in it being existentially quantified. This quantifier ensures that x may only be
modified by calling counter , and surfaces in the specification m c at line 1,
allowing us to precisely describe its result.
    For modularity, we might wish to hide the persistence of locations created
by mut closure (e.g., assuming the presence of a garbage collector). We can do
this simply by using the specification ens[ ] res=1, which is an (intuitionistic)
weakening of m c.
    A subtlety about λ(res) is that it does not assume anything about the value
of x , requiring only that x exists as a location. Thus, even if we swapped lines 2
and 3, changing the scope of x and allowing the rest of mut closureto mutate it,
λ(res) would be unchanged. This is in contrast to other systems which require
additional guarantees to specify the lambda modularly; an example is Prusti [31],
which leverages the ownership guarantees provided by the Rust type system.


C       Additional Examples

This section may be read as an extension to Section 2. Here we highlight a few
more interesting and involved example programs.


Closure-local state Fig. 10a shows a simple extension of Fig. 9. The internal
states of multiple closures may be faithfully modelled using staged formulae.
Again, the existential quantifiers serve both to restrict access to both x locations
22        Darius Foo, Yahui Song, Wei-Ngan Chin


     let two_closures ()
     ◦
      ∃ i, j · ens[ ] i 7→ 1 ∗ j 7→ 2 ∧ res=3
     = let f = let x = ref 0 in                                  let rec range x n =
                                                                ◦
          fun () -> x :=! x +1; ! x                                range(x, n, res) = req n≥0; · · ·
        ◦                                                            if n = 0 then []
          {∃ x · ens[ ] x 7→ 0 ∧ f (r)=∃ a ·
                req x 7→ a; ens[ ] x 7→ r∧r=a+1}                     else x :: range ( x +1) (n -1)
        in let g = let x = ref 0 in
                   fun () -> x :=! x +2; ! x                     let rec take f n =
        ◦                                                       ◦
          {∃ x, x2 · ens[ ] x 7→ 0 ∗ x2 7→ 0∧f (r)= · · ·∧         take(f, n, res) = · · ·
                g(r)=∃ a2 · req x2 7→ a2 ;                           if n = 0 then []
                           ens[ ] x2 7→ r∧r=a2 +2}                   else f () :: take f (n -1)
        in f () +g ()
        ◦
          {∃ x, x2 · ens[ ] x 7→ 0 ∗ x2 7→ 0∧f (r)= · · ·∧ let gen_contents x n
                g(r)=· · ·; ∃ r1 , r2 · f (r1 ); g(r2 );        gen contents(x, n, res) = ∃ i · req x 7→ i
                                   ens[ ] res=r1 +r2 }                 ; ens[ ] x 7→ i+n∧range(i, n, res)
        ◦
          {∃ x, x2 , r1 , r2 · ens[ ] x 7→ 1 ∗ x2 7→ 0∧f (r)= · =· · let integers =
                ∧g(r)=· · ·∧r1 =1; g(r2 ); ens[ ] res=r1 +r2 } fun () -> let r = ! x in
        ◦                                                                       x := ! x + 1; r
          {∃ x, x2 , r1 , r2 · ens[ ] x 7→ 1 ∗ x2 7→ 2∧f (r)= · · ·
                ∧g(r)=· · ·∧r1 =1∧r2 =2∧res=r1 +r2 }                 in take integers n

                (a) Multiple closures                             (b) Closures as generators

                           Fig. 10: More uses of stateful closures


(renamed to i and j) and as a means of enforcing modularity in specifications.
Specification subsumption provides a way to hide them, if the internal state of
the closure does not matter in a particular context.

Closures as generators With mutable closures, we can build generators –
“next-element” functions of type unit → 'a which represent potentially infinite
sequences. In Fig. 10b, we recast counter (from Fig. 9) as the generator integers.
We then prove a lemma gen contents that uses the ghost functions range and
take that says what integers contains, for all n. With only the given specification,
this proof goes through automatically.


D        Intersection of Staged Specifications
Intersection specifications are meant to capture different call scenarios and have
an opposite semantics from disjunctions from conditional expressions. They cur-
rently arise primarily from a more exhaustive consideration of aliasing scenarios
and it can be used to support proof search over disjoint preconditions.
    An example of how intersection specifications may originate is from the fol-
lowing more complete consideration from bi-abduction rule:
                         V
                            (DA ∗ D1 ⊢ D2 ∗ DF )
                                    V                             Float Pre
          ens[ ] D1 ; req D2 <==> sp (req DA ; ens[ ] DF )
  Staged Specification Logic for Verifying Higher-Order Imperative Programs        23

    A concrete application is the following where x and y may be aliases or not.

 ens[ ] x 7→ a ; req y 7→ b <==> (req y 7→ b; ens[ ] x 7→ a) ∧sp (req x=y∧a=b)

   We use the symbol ∧sp to distinguish it from ∨ that results from conditional
constructs. Our normalization rules would place ∧sp at outermost construct so
that they may be used to support proof search during forward verification.

                                 Φ ::= Φ′ | Φ ∧sp Φ
                                Φ′ ::= θ | Φ′ ∨ Φ′

    An example of its use is the following more general staged specification of
hello example from Sec 2.1 where ∧sp is used in Stage 4a/4b.

hello(f, x, y, res) =
  ∃ a · req x 7→ a;               // Stage 1: requiring x be pre-allocated
  ens[ ] x 7→ a+1;                // Stage 2: ensuring x is updated
  ∃ r · f (y, r);                 // Stage 3: unknown higher-order f call
  ∃ b · ( req x 7→ b ∗ y 7→ ;     // Stage 4a: requiring x , y be pre-allocated
  ens[ ] x 7→ b ∗ y 7→ res∧res=b+r// Stage 5a: y is updated, and x is unchanged
  ∧sp req x 7→ b∧x=y;             // Stage 4b: requiring x be pre-allocated with x = y
     ens[ ] x 7→ res∧res=b+r ) // Stage 5b: y (and hence x ) is updated

   The intersection operator ∧sp can be floated outermost so that its new staged
specifications below can support proof search via Hoare-style verification rules.

     hello(f, x, y, res) =
       ∃ a · req x 7→ a∧x6=y; ens[ ] x 7→ a+1; ∃ r · f (y, r);
       ∃ b · req x 7→ b ∗ y 7→ ; ens[ ] x 7→ b ∗ y 7→ res∧res=b+r
       ∧sp ∃ a · req x 7→ a∧x=y; ens[ ] x 7→ a+1; ∃ r · f (y, r);
             ∃ b · req x 7→ b; ens[ ] x 7→ res∧res=b+r


E    An Example to Illustrate the Forward Rules

As an example to illustrate the forward (Hoare) rules, consider the program in
Fig. 11, annotated with intermediate specifications generated by the rules. It
defines a location x that is captured by a closure and mutates x through the
closure, asserting something about the closure’s result at the end.
    Line 2 is the result of applying the Ref rule, resulting in a new, existentially-
quantified location x. Next, we reason about the lambda expression, starting
with an empty history. Inferring a specification for the assignment involves first
applying with Deref rule, then Val (taking + as primitive), then Assign, resulting
in line 5. This is then normalized into the specification at line 6. The Deref rule
is applied again, and the result is normalized.
    Saving the specification of the lambda expression Φf for later, we continue
outside it to line 11, using the Call rule twice, followed by the Assert rule. The
24        Darius Foo, Yahui Song, Wei-Ngan Chin


1    let x = ref 0 in
     ◦
2      { ens[ ] x 7→ 0 }
3    let f = fun () ->
4        x := ! x + 1;
        ◦
5         { ∃ a · req x 7→ a;ens[ ] x 7→ a ∧ res=a;ens[ ] res =
               a+1;req x 7→ ;ens[ ] x 7→ a+1 ∧ res=() }
        ◦
6         { ∃ a · req x 7→ a;ens[ ] x 7→ a+1 ∧ res=() }
7        !x
        ◦
8         { ∃ a · req x 7→ a;ens[ ] x 7→ a+1;∃ b · req x 7→ b;ens[ ] x 7→ b ∧ res =b }
        ◦
9         { ∃ a · req x 7→ a;ens[ ] x 7→ res ∧ res=a+1 }
10   in
     ◦
11     { ens[ ] x 7→ 0∧f (res)=∃ a · req x 7→ a; ens[ ] x 7→ res ∧ res=a+1 }
12   f () ;
     ◦
13     { ens[ ] x 7→ 0∧f (res)= · · · ;∃ r1 · f (r1 ) }
     ◦
14     { ens[ ] x 7→ 1∧f (res)= · · · }
15   let r = f () in
     ◦
16     { ens[ ] x 7→ 1∧f (res)= · · · ;f (r) }
     ◦
17     { ens[ ] x 7→ 2∧f (res)= · · · ∧r=2 }
18   assert ( r = 2) ;
     ◦
19     { ens[ ] x 7→ 1∧f (res)= · · · ∧r=2;req r=2 }
     ◦
20     { ens[ ] x 7→ 1∧f (res)= · · · ∧r=2 }
21   r
     ◦
22     { ens[ ] x 7→ 2∧f (res)= · · · ∧r=2;ens[ ] res=r }
     ◦
23     { ens[ ] x 7→ 2∧f (res)= · · · ∧r=2∧res =r }
     ◦
24     { ∃ x, f, r · ens[ ] x 7→ 2∧f (res)= · · · ∧r=2∧res=r }
     ◦
25     { ∃ x · ens[ ] x 7→ 2∧res=2 }

                             Fig. 11: Forward rules example

result at line 15 is the inferred specification of the entire program and cannot be
normalized further.
   With this done, the next step might be to prove that this specification is sub-
sumed by another specification that a user might write, e.g., ∃ x · ens[ ] x 7→ 2 ∧
res=2. In the next section, we detail a procedure to do this.


F        Comparing with User Annotations in Cameleer
Of the programs that can be handled, Heifer requires much less specification. As
an example, Fig. 12 illustrate Cameleer specifications for map and foldr , which
may be compared to the programs given in Section 2.
    Because of the need to summarize the effects of f , map’s postcondition uses
a quantifier (over sequence indices) to talk about the elements of the input
and output lists. This then necessitates lemmas such as index shift for relating
indices to list destructuring, finally requiring more lines of specification per line
of code. The foldr specification is similar to the one for Iris (Section 1), but does
not use a higher-order triple, instead requiring a ghost argument for an invariant
that must be preserved between calls to f . This approach is representative of
     Staged Specification Logic for Verifying Higher-Order Imperative Programs   25


1     let rec map ( f :’ a -> ’b ) ( xs :’ a list ) =
2        match xs with
3        | [] -> []
4        | x :: xs1 -> f x :: map f xs1
5     (* @ ys = map f xs
6            variant xs
7            ensures length ys = length xs
8            ensures forall i. 0 <= i < length ys ->
9                        ys [ i ] = f ( xs [ i ]) *)
10

11    (* @ lemma index_shift : forall x :’a , xs :’ a list , i : int .
12        1 <= i /\ i < length ( Cons x xs ) ->
13          ( Cons x xs )[ i ] = xs [i -1] *)
14

15    let rec foldr (( inv : ’b -> ’a seq -> bool ) [ @ghost ])
16       (f : ’a -> ’b -> ’b) ( xs : ’a list ) ( acc : ’b )
17    = match xs with
18       | [] -> acc
19       | x :: t -> f x ( foldr inv f t acc )
20    (* @ r = foldr inv f xs acc
21           requires inv acc []
22           requires forall acc x ys .
23                      inv acc ys -> inv ( f x acc ) ( cons x ys )
24           variant xs
25           ensures inv r xs *)


                       Fig. 12: foldr and map in Cameleer [22]

many verifiers, including Dafny, WhyML, and vanilla F⋆. As mentioned before,
this parameterization of the specification with a summary of f is nontrivial, in
that it cannot be mechanically done for every higher-order function, as this pair
of examples shows.


G       Entailment for Staged Specifications
Our entailment over staged specification is always conducted over the compacted
form where non-recursive staged predicate definitions are unfolded and com-
pacted, while unknown predicates are always matched exactly. Lemmas are also
also used to try re-summarize each instantiation of recursive staged predicates.

G.1       Staged (Specification) Subsumption
We assume staged formulae Φ are normalized, i.e., in the form described at the
end of Section 3.2. Normalization both aligns and compacts staged formulae and
is a crucial ingredient to the entailment procedure, which interleaves normaliza-
tion and rewriting to prove subsumption stage by stage. We illustrate this proof
system formally in Fig. 13, and by example at the end of this section.
26       Darius Foo, Yahui Song, Wei-Ngan Chin

    The rules DisjLeft and DisjRight reduce disjunctive subsumption to subsump-
tion between flows F ⊢ θi ⊑ θj , where F is an assumption σ∧π which arises from
the propagation of separation logic frames; where unspecified, it is emp∧true.
    The next three rules check subsumption between the individual stages of
flows, matching them pairwise before continuing on their tails. This matching is
possible because flows are normalized. The rules EntReq and EntEns respectively
express the contravariance of req preconditions and covariance of ens postcon-
ditions. Subsumption between stages reduces to standard separation logic entail-
ments of the form D1 ⊢ D2 ∗ F , where F is an inferred frame, and all heaps that
satisfy D1 also satisfy D2 . Notably, inferred frames F propagate forward and be-
come assumptions in the separation logic entailments of next stage; a motivating
example is the subsumption req x 7→ 1; ens[ ] x 7→ 2⊑req x 7→ 1 ∗ F ; ens[ ] x 7→ 2 ∗ F
for any F . The propagation of frames from req to ens stages has previously been
called enhanced specification subsumption [6, Section 2.4], and has been histori-
cally used for verification of object-oriented programs; we extend this use to ens
and req in multi-stage specifications.
    The rule EntFunc requires that function constructors f match, and their ar-
guments and return value are provably equal under the pure assumptions in F0 .
Something notable about EntFunc is that only the pure portion of the frame
propagates further across function stages, as the effects of instantiated function
stages may invalidate any assumptions about the heap. Heap frames may thus
be dropped if we are using intuitionistic separation logic. If classical separation
logic is adopted, our subsumption procedure will need to enforce σ=emp at the
start of EntRule and at the end of our specification subsumption procedure.


           θ1 ⊑Φc         θ2 ⊑Φc                     θa ⊑θi (i=1∨i=2)
                                 DisjLeft                              DisjRight
               (θ1 ∨ θ2 )⊑Φc                            θa ⊑(θ1 ∨ θ2 )

                 fresh y ∗   F0 ∗ D2 ⊢ (∃ x∗ . D1 ) ∗ F      F ⊢ θa ⊑θc
                                                                        EntReq
                     F0 ⊢ (∃ x∗ · req D1 ; θa )⊑(∃ y ∗ · req D2 ; θc )

                 fresh x∗     F0 ∗ D1 ⊢ (∃ y ∗ . D2 ) ∗ F    F ⊢ θa ⊑θc
                                                                          EntEns
                   F0 ⊢ (∃ x · ens[r] D1 ; θa )⊑(∃ y ∗ · ens[r] D2 ; θc )
                            ∗



fresh x∗ , y ∗   πp =xpure(σ∧π) πp ⇒ (∃y ∗ · x∗1 =x∗2 ∧r1 =r2 ) emp ∗ πp ⊢ θa ⊑θc
                                                                                  EntFunc
                   σ∧π ⊢ ∃ x∗ · f (x∗1 , r1 ) ; θa ⊑ ∃ y ∗ · f (x∗2 , r2 ) ; θc
                                                                         


    xpure(σ)∧π1 ⇒ ∃ x∗ . π2                  D1 ⊢ (∃ x∗ . D2 ∧ v1 =v2 ) ∗ F
            ∗                     SLBase                                             SLMatch
 σ∧π1 ⊢ (∃ x . emp∧π2 ) ∗ (σ∧π1 )        y 7→ v1 ∗ D1 ⊢ (∃ x∗ . y 7→ v2 ∗ D2 ) ∗ F

                 fresh x      D1 ∧ z=x ⊢ (∃ y ∗ . D2 ∧ v1 =v2 ) ∗ F
                                                                      SLMatchEx
                      z 7→ v1 ∗ D1 ⊢ (∃ xy ∗ . x 7→ v2 ∗ D2 ) ∗ F

            Fig. 13: Staged Subsumption and Selected Entailment Rules
  Staged Specification Logic for Verifying Higher-Order Imperative Programs       27

    Separation logic entailments are then reduced into first-order implication
using the so-called “crunch, crunch” approach [21], via the next three rules:
SLMatch reduces matching locations on both sides into equalities on their con-
tents, SLMatchEx does the same for existentially-quantified locations (matching
locations regardless of name to instantiate existentials, and possibly requiring
backtracking), and SLBase serves as the base case, at which point the frame is
abstracted to first-order logic (via the function xpure), and the final proof obli-
gation is checked via SMT. We use xpure to soundly approximate the spatial
information of a heap formula in first-order logic. We illustrate its behavior by
example: xpure(emp) = true and xpure(x 7→ 1 ∗ y 7→ 2) = x6=null∧y6=null∧x6=y.

G.2    Inductive predicates and unfolding
The proof system we propose allows inductive predicates, which are useful for
specifying data structures (as well) as the behaviors of recursive functions –
examples of these were given in Section 2 and later in Appendix C. Unlike in
classic separation logic, where such predicates are used to describe the shapes of
data in the heap, here inductive predicates describe flows via staged formulae.
    An inductive predicate definition is of the form g(x∗ , r) , Φg , where g, x∗ ,
and r may occur in Φg . Unfolding an inductive definition simply replaces a
function stage g(y ∗ , rg ) with [r:=rg ][x∗ :=y ∗ ]Φg This is the meat of the Unfold
rule, which then normalizes the result to Φu before continuing.

                    ∃ u∗ · [r:=rg ][x:=xg ]Φg ; θa <==> Φu 
             g(x, r) , Φg       F0 ⊢ Φu ⊑ ∃ w∗ · f (xf , rf ) ; θc
                                                                    Unfold
              F0 ⊢ ∃ u∗ · g(xg , rg ) ; θa ⊑ ∃ w∗ · f (xf , rf ) ; θc

    The first premise in the rule above may be satisfied by a previous definition of
an inductive predicate, or by a local name bound to a logical lambda expression.
For example, we may unfold y in the flow ens[ ] y=λ (x∗, r)→ Φ; y(v∗). This
underscores the first-class nature of lambda terms in the logic, which is necessary
to precisely model higher-order behaviors like currying. Such logical lambda
terms are manipulated mostly by the above rule and are encoded in a form that
preserves alpha equivalence before being sent to the SMT solver.
    One more ingredient is required for reasoning about recursive functions: the
use of induction. Inductive predicates provide the means of specification, and an-
nother piece is the automated application of lemmas which is left in Appendix H.


H     Proving Lemmas and Rewriting

Nontrivial proofs in automated program verifiers are often made possible by
user-supplied lemmas. A typical way to provide such lemmas in verifiers for
Hoare logic and two-state separation logic is to make use of the Curry-Howard
correspondence. By encoding the lemma P ⇒ Q as a ghost procedure with
precondition P and postcondition Q, application of the procedure at a specific
28       Darius Foo, Yahui Song, Wei-Ngan Chin

point corresponds to applying the lemma to the proof state at that point, and
the lemma can be separately proved by writing a body for the procedure.
    By analogy to this, we allow subsumption lemmas in the system of the form
∀x∗ . f (y, r) ⊑ θq , where x∗ may occur free in both f (y, r) and θq . This may
be seen as a specific case of the subsumption relation between two disjunctive
staged formulae, but with singleton disjuncts on both sides, and only a single
function stage on the left. The restricted form is sufficient to express the induc-
tion hypotheses of subsumptions between recursive functions.
    Rewriting is very similar to unfolding – the one difference is that not all
arguments of the function stage on the left are parameters, hence the universal
quantifier on some.
    With both the unfolding and rewriting rules, the proof system is fully defined.
As an example, we consider proving a property of following function.

1    let rec applyN f x n =                                             5   let incr x = x + 1
       ◦
2        applyN (f , x , n, res) = · · ·                                6   let summary x n
3      if n = 0 then x                                                  7    summary(x , n, res) =
4      else let r = f x in applyN f r                                           req n≥0; ens[ ] res=x+n
             (n -1)                                                     8   = applyN incr x n


   The proof begins with a suitable induction hypothesis. We infer the following
one using heuristics. In general, it would have to be provided by the user as a
lemma (for re-summarization).

           ∀ x, n, res. applyN (incr, x, n, res) ⊑ req n≥0 ens[ ] res=x+n
    The following proof can then be carried out automatically. it illustrates the
general approach: subsumption proofs go stage by stage, attempting to match
function stages by interleaving unfolding and normalization. This ends with ei-
ther an unknown function stage on both sides or a simple pre- and postcondition,
in which case the separation logic proof obligations are discharged, or a pair of
differing unknown function stages, in which case the proof fails.

                         n ≥ 0 ⇒ true       res = (x + 1) + n − 1 ⇒ res = x + n
                                                                                               EntNorm
             ens[ ] n > 0 ∧ r = x + 1 ∧ res = r + n − 1      ⊑ req n ≥ 0; ens[ ] res = x + n
                                                                                                        Normalize
     ens[ ] n>0; (ens[ ] r=x+1) ; (req n−1 ≥ 0; ens[ ] res=x+n−1) ⊑ req n≥0; ens[ ] res=x+n
                                                                                                        Unfold
        ens[ ] n>0; inc(x, r); (req n−1 ≥ 0;ens[ ] res=x+n−1)           ⊑ req n≥0; ens[ ] res=x+n
                                                                                                         Rewrite
         (... ∨ ens[ ] n > 0;inc(x, r);applyN (inc, n − 1, r, res))   ⊑ req n ≥ 0; ens[ ] res = x + n
                                                                                                          Unfold
                          applyN (inc, n, x, res) ⊑ req n ≥ 0; ens[ ] res = x + n



    In the above example, with boxes indicating changes from one step to the
next, we unfold applyN and focus on the inductive case. After rewriting with the
induction hypothesis, we unfold inc and normalize to compact everything into a
single req/ens stage, allowing an application of EntNorm to produce first-order
proof obligations.
    Staged Specification Logic for Verifying Higher-Order Imperative Programs                        29

I      Soundness
I.1     Operational semantics
To facilitate the following soundness proofs, we define a big-step reduction re-
lation with judgments of the form e, h, S Re , h1 , S1 . Program states consist of
a heap h and store S, like in Section 3.1. Outcomes Re ::= Norm(v) | Err are
more constrained compared to R – evaluation results in a value v, not a variable
r, and there is only a Err outcome representing a failure, without possible failure
as there might be in the specification.


                              Nil,Const,Lambda                                              Cons
       v, h, S     v, h, S                          x1 ::x2 , h, S   S(x1 )::S(x2 ), h, S


                                          Var           h, S|=σ∧π
                 x, h, S     S(x), h, S                                     Assert
                                                (assert σ∧π), h, S (), h, S

                    e1 , h, S v, h1 , S1     e2 , h1 , S1 [x:=v] v1 , h2 , S2
                                                                              Let
                            (let x=e1 in e2 ), h, S v1 , h2 , S2 [x6:=]


    S(f ) = fun (x∗ ) Φ→ e       S(x∗ ) = v ∗
            ∗     ∗                                              x1 ∈ dom(h)
          [x :=v ]e, h, S v2 , h1 , S1                                                     Assign
                                              App (x1 := x2 ), h, S (), h1 [S(x):=S(v)], S
            f (x∗ ), h, S v2 , h1 , S1


                                           Deref             l∈/ dom(h)
            !x, h, S       h(S(x)), h, S                                         Ref
                                                    ref x, h, S ℓ, h[ℓ:=S(x)], S


       S(b)=true      e1 , h, s v, h1 , S1          S(b)=false     e2 , h, s v, h1 , S1
                                             If1                                          If2
    (if b then e1 else e2 ), h, S v, h1 , S1     (if b then e1 else e2 ), h, S v, h1 , S1

I.2     Soundness of Normalization
Theorem 1 (Soundness of Normalization). Given Φ1 ==>Φ2 , if S, H                                   S1 , H1 , R1 |=Φ1 ,
then S, H S1 , H1 , R1 |=Φ2 .

Intuitively, normalization of a staged formula preserves its behavior.

Proof. By case analysis on the derivation of Φ1 ==>Φ2 . Most cases follow im-
mediately from the semantics of staged formulae (Fig. 5). For example, given
==>req D1 ; req D2 req D1 ∗ req D2 , h = h0 ◦h1 ◦h2 , where h1 |=D1 and h2 |=D2 ,
and L1 = h1 ◦h2 .
   The only remaining case is Float Pre (Section 3.2). Here we reason about
heaps instead of heap formulae. Let h(Di ) be a heap such that h(Di )|=Di for
i ∈ {a, f, 1, 2}. First, it must be the case that Da describes a heap that is in
30     Darius Foo, Yahui Song, Wei-Ngan Chin

h, otherwise it would be impossible to prove the conclusion. From this we know
h = h(Da )◦F for some framing heap F . Now, from the second premise, we have
h◦h(D1 ) = h(D2 )◦h1 . Substituting h, we have (h(Da )◦F )◦h(D1 ) = h(D2 )◦h1 .
From the first premise, assuming soundness of ⊢, we have h(Da )◦h(D1 ) =
h(D2 )◦h(Df ). h1 must thus be h(Df )◦F . Consider the conclusion. It suffices
to prove that h = h(Da )◦F and h(Df )◦F = h1 , which is exactly what we have.

I.3   Soundness of Forward Rules
The rules are sound if every derivable triple { emp } e { Φ } is valid.
     A staged formula Φ is valid if: given that it specifies a transition from
initial configuration S, h to final configuration S2 , h1 , Norm(r), execution of e
from the same initial configuration results in a compatible final configuration
h1 , S1 , Norm(v).
     Compatibility requires that S1 ⊆ S2 and S1 (r) = v. Intuitively, the heap and
result have to be equal, while the final store of Φ is allowed to contain more
bindings due to existentials.

Theorem 1 (Soundness of Forward Rules) Given { emp } e { Φ }, then
∀S, h, S2 , h1 · (S, h S2 , h1 , Norm(r)|=Φ) ⇒ ∃S1 · e, h, S Norm(v), h1 , S1 and
S1 ⊆ S2 and S1 (r) = v.

Proof. By induction on the derivation of e, h, S1   Norm(v), h1 , S1 .
 – The nil, cons, and constant are straightforward: their reduction has no effect
   on the heap, Φ is of the form ens[res] res=v, S1 = S2 , and S1 (res) = v.
 – The variable case is similar: Φ is of the form ens[res] res=x, S1 = S2 , and
   S1 (res) = x.
 – The lambda case is immediate from the induction hypothesis on e, assuming
   that entailment is sound.
 – e is of the form ref x. Reduction results in a store S1 = S and heap h1 =
   h[ℓ:=S(x)]. Φ is of the form ens[res] res 7→ x, with final state S2 = S and
   heap h1 , if we choose h1 = {ℓ 7→ S(x)}. We also have S1 (res) = v = ℓ.
 – e is of the form x1 := x2 . Reduction results in a store S1 = S and heap
   h1 = h[S(x1 ):=S(x2 )]. Given Φ is of the form req x1 7→ ; ens[ ] x1 7→ x2 ,
   reduction removes the heap location x1 , then re-adds it via with new value
   S(x2 ), effectively modifying the heap at that the assigned location to h1 .
 – e is of the form !x. Reduction has no effect on the heap and store and results
   in v = S(x). Φ is of the form ∃ a · req x 7→ a; ens[res] x 7→ a∧res=a, reduction
   removes some heap location ℓ with value v, then immediately readds it,
   leaving the heap unchanged. The store S2 is extended with {a 7→ v}. It is a
   superset of S1 because h(S(x)) = h(ℓ) = v.
 – e is of the form assert D. Reduction has no effect on the heap, and reduction
   of Φ is similar to the case for !x.
 – e is of the form let x=e1 in e2 . Reduction evaluates e1 to a value v, evaluates
   e2 with x bound to v in the store, then removes the binding for x, result-
   ing in a heap h and store S1 . Φ is Φ = ∃ x · [res:=x]Φ1 ; [x:=x]Φ2 , where
  Staged Specification Logic for Verifying Higher-Order Imperative Programs       31

   { emp } e1 { Φ1 } and { emp } e2 { Φ2 }. Given the induction hypotheses,
   it remains to show that the heap resulting from reducing Φ is h and the
   resulting store S2 is a superset of S1 . The former follows directly from the
   semantics of staged formulae as let expressions do not further change the
   heap.
 – e is of the form if x then e1 else e2 . Reduction proceeds with either e1 or e2 ,
   depending on the value of S(x). The conclusion follows from case analysis
   on x, then application of either induction hypothesis.
 – e is of the form f (x∗ ). Its a summary is a simple function stage f (x∗ , res).
   From the big-step reduction relation, we know that e evaluates as [x∗ :=S(x∗ )]e1
   would, given S(f ) = fun (x∗ ) Φ→ e1 . Also, from the semantics of staged for-
   mulae, it suffices to prove soundness for [y ∗ :=x∗ ]Φ. We know that e1 is
   summarized soundly from the induction hypothesis, and the substitutions
   do not compromise this as both e1 and Φ contain (the values of) x∗ after.

I.4   Soundness of Entailment
As we use a standard fragment of separation logic with the usual semantics, we
assume the soundness of its entailment proof system.
Theorem 3 (Soundness of SL entailment). Given D1 ⊢ D2 and S, h|=D1
then S, h|=D2 .
   We focus on the soundness of the entailment proof system for staged formulae.
Given a derivation Φ1 ⊑Φ2 and the same starting configuration S, H with an
empty local heap, “executing” Φ1 should result in an an ending configuration
with a smaller global heap and larger local heap than executing Φ1 . The relation
between heaps is containment rather than equality intuitively because a stronger
formula is allowed to entail a weaker one, e.g., ens[ ] x 7→ 1 ∗ y 7→ 1 should entail
ens[ ] x 7→ 1.
Theorem 2 (Soundness of Entailment). Given Φ1 ⊑Φ2 and S, h Norm(r1 ), S1 , h1 |=Φ1 ,
then there exists h2 such that S, h Norm(r1 ), S2 , h2 |=Φ2 where h2 ⊆ h1 . (Here,
h1 ⊆ h2 denotes that ∃ h3 . h1 ◦h3 = h2 .)
Proof. By induction on the derivation of Φ1 ⊑Φ2 .
 – In DisjLeft, when the derivation is of the form (Φ1 ∨ Φ2 )⊑Φ2 , we know from
   the induction hypothesis that execution of both Φ1 and Φ2 result in global
   heaps H3 and H4 that are larger than H2 , and local heaps L3 and L4 that are
   smaller than L2 . Since both ending configurations satisfy the property, and
   the semantics of disjunction allows us to choose either ending configuration,
   the conclusion is true.
 – In DisjRight, when the derivation is of the form Φa ⊑(Φ1 ∨ Φ2 ), we know from
   the induction hypothesis that only the execution of Φ1 produces an ending
   configuration that satisfies the property. Since the semantics of disjunction
   allow execution of Φ1 ∨ Φ2 to choose either Φ1 or Φ2 , it suffices to prove the
   property for just one disjunct, which we have by the induction hypothesis.
32     Darius Foo, Yahui Song, Wei-Ngan Chin

 – In EntReq, when the derivation is of the form F0 ⊢ (∃ x∗ · req D1 ; Φa )⊑(∃ y ∗ · req D2 ; Φc ),
   we must show that req D2 results in an identical store, smaller global heap,
   and larger local heap than req D1 (and the induction hypothesis ensures that
   these relations are preserved). In other words, D2 should move more of the
   global heap than D1 does into L2 (resp. L1 ). Since we know emp ∗ D2 ⊢ D1,
   from Theorem 3, we know that any heap satisfying D2 must satisfy D1 . D2
   must thus be a more precise heap formula, with more conjuncts. Thus, it
   may removed more of the heap than D1 , making H2 smaller. Correspond-
   ingly, L2 will be larger than L1 as a larger portion of the heap was moved
   into it. req does not update the store, hence the conclusion is true.
 – The EntEns case is dual to EntReq, but largely similar. Given a derivation of
   the form F0 ⊢ (∃ x∗ · ens[ ] D1 ; Φa )⊑(∃ y ∗ · ens[ ] D2 ; Φc ), we know D1 ⊢ D2 .
   Hence D1 must add a larger portion of heap into the global heap H1 than
   D2 does, resulting in H1 being larger and L1 being smaller. ens does update
   res in the store, but the compatibility of the values that the store is updated
   with is ensured by the validity of the separation logic entailment.
 – The EntFunc case seeks to prove that both sides of the entailment are ef-
   fectively equal under the assumptions in F0 . As the store and both heaps
   are modified the same way (by the formula that is the definition of f ), they
   remain equal, hence the conclusion is true.
 – Both rules for unfolding are technically involved, but conceptually simple.
   As we replace function stages with their specifications (which have been
   earlier checked for soundness), the conclusion follows from the soundness of
   normalization (Theorem 1).

I.5   Termination
We outline termination arguments for our normalization procedure, Hoare-style
forward rules and also the entailment/subsumption procedure for staged speci-
fications

I.6   Termination of Normalization
The normalization procedure Φ1 ==>Φ2 is terminating since staged logic ex-
pression is always getting smaller, except for the F loatP re rule, where each
pre-condition is being floated outwards. Hence, by giving lower weights to pre-
condition stages, this rule will continues to decrease the termination measure
of our normalization procedure.Hence, each application of normalization/com-
paction will always terminate.

I.7   Termination of Hoare-Style Forward Rules
Except for the consequence rule, all the forward reasoning rules are either just
terminating (CVar, Val, Assign, Call and Assert). or works on structurally
smaller expressions (e.g. Lambda, Let and If Hoare-rules). If we assume that
Consequence rule is applied at most once for each distinct sub-expression, the
set of Hoare-style forward-reasoning rules is always terminating.
  Staged Specification Logic for Verifying Higher-Order Imperative Programs      33

I.8   Termination of Staged Entailment
Staged Entailment is used mostly for the summarization of recursive staged
predicates. This process requires users to provide suitable lemmas that must be
appropriately generalized. In case this is not done properly, there is a possibility
that staged entailment may go into an infinite loop. To prevent this problem,
we only allow a bounded set of new staged predicate definitions to be defined,
and a bound number of unfoldings. Once these two bounds are exceeeded, we
approximate our staged entailment outcome with a failure. This approximation
is sound but may lead to incompleteness for our entailment procedure over staged
logics.
