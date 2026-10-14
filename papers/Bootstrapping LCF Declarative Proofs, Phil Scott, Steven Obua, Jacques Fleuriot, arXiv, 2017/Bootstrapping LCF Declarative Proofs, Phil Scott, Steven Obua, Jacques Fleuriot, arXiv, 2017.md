                                                 Bootstrapping LCF Declarative Proofs
arXiv:1703.05351v1 [cs.LO] 15 Mar 2017




                                                        Phil Scott, Steven Obua, Jacques Fleuriot

                                                                             Abstract
                                                  Suppose we have been sold on the idea that formalised proofs in an
                                              LCF system should resemble their written counterparts, and so consist
                                              of formulas that only provide signposts for a fully verified proof. To be
                                              practical, most of the fully elaborated verification must then be done
                                              by way of general purpose proof procedures. Now if these are the only
                                              procedures we implement outside the kernel of logical rules, what does the
                                              theorem prover look like? We give our account, working from scratch in
                                              the ProofPeer theorem prover [12], making observations about this new
                                              setting along the way.


                                         1    Introduction
                                         LCF [10] style theorem provers are based on small kernels of inference/typing
                                         rules. Ultimately, all theorems are proven by applying these rules, though in
                                         practice, users will call derived inference rules and higher-level proof procedures
                                         which call yet more derived inference rules and procedures until they ultimately
                                         hit the kernel rules. This leads to a zoo of often composable proof tools cul-
                                         minating in full decision procedures, which together afford the user a variety of
                                         ways to verify their theorems balancing elegance and simplicity against perfor-
                                         mance.
                                             There is a more consolidated approach to verification with a less program-
                                         matic aesthetic. One can use a declarative language, such as those offered by
                                         Isabelle, HOL Light and Coq [4, 11, 17]. A user of such a language writes
                                         structured proofs by stating assumptions, variable declarations and intermedi-
                                         ate conclusions, and indicating how these are connected by logical consequence.
                                         The languages often approximate written mathematical proofs, and could be
                                         viewed as the ideal implementation of a formal language for written mathemat-
                                         ics. We might then expect them to be more accessible to working mathemati-
                                         cians, a core demographic for ProofPeer. Thus, the language with which users
                                         interface with our system, ProofScript [1], takes structured proof as a core part
                                         of its syntax, with the traditional panoply of proof procedures intended only to
                                         support these readable declarative proofs.
                                             In both Isar and HOL Light’s Mizar Light, the heavy duty automation
                                         tends to be handed to clausal form automated theorem provers, and we have
                                         not sought to make ProofPeer an exception. In the following sections, we de-
                                         scribe our streamlined approach to implementing just the scaffolding necessary

                                                                                  1
to make such provers work in the novel setting of ProofScript, a dynamically
typed, purely functional language with primitives for working with the terms
and theorems of the safely encapsulated and secure logical kernel of ProofPeer.


2    Organisation
In the next section, we will give some motivation for the use of general purpose,
external automated theorem provers in interactive theorem proving. In §4, we
shall describe the minimal infrastructure we used to talk the basic language
of these provers and in §5 we shall discuss what we needed to understand the
response. We conclude in §6.


3    Accessing external tools
The Sledgehammer [9] tool in Isabelle began as an impressive effort to integrate
external theorem provers, initially Vampire [8] and SPASS [16], into declarative
proofs by automatically processing their certificates as inference rules in the Isar
language. Since then, many more theorem provers have been integrated [3], but
it has turned out that it is sufficient, and much easier besides, to just use the
provers to minimise the number of lemmas needed for a first-order proof and
then let it be found by Hurd’s METIS [6]. METIS is a generic resolution prover for
first-order logic with equality, based on a small LCF style kernel with full proof-
recording. As with other resolution provers, its job is to refute the negation of
a posed problem, and because of its easily trusted kernel, when METIS claims
to find a refutation, we have a high guarantee that the proof record really is a
proof of the refutation.
    Both Isabelle and METIS are written in Standard ML, so the automated
theorem prover is easily usable as a library of the other interactive theorem
prover. ProofPeer, on the other hand, runs on the JVM and Javascript, and
is implemented entirely in Scala. One of our first efforts, then, was to write a
clean port of METIS to Scala, where it can now be used as a library for other
JVM or Javascript based-projects. Entirely under our control, this prover is
in place to become the standard automated theorem prover which ProofPeer
uses to reconstitute first-order proofs, just as its Standard ML variant does for
Isabelle’s Sledgehammer.
    To access METIS from ProofScript, we equip the language with a built-in
function callmetis which can send and receive ProofScript data structures to
and from a wrapper around the METIS library. This is currently a somewhat
ad-hoc approach, but ProofScript’s data structures are easy to read and write
and can serve as a general data exchange format in the manner of S-expressions
and JSON, and we certainly intend to provide a general mechanism to integrate
more external tools with ProofScript, communicating with wrappers in the same
way.
    A cautionary note is due because functions which get their data from third


                                         2
parties may not behave nicely and return the same output for the same input,
thereby breaking ProofScript’s promises about functional purity. For now, we
can at least be reassured that our implementation of METIS is guaranteed to be
fully deterministic, and that callmetis will always return the same output for
the same input.


4     Conversion
Any time a user wishes to make an inference in a declarative proof, they will
implicitly have in mind a conjecture that the next formula to be derived is
a logical consequence of the assumptions currently in force. To a resolution
prover, this is turned into a conjunctive normal form problem asserting that the
contradiction of the next step together with the assumptions in force entails a
contradiction. It therefore suffices to show that such a refutation entails the
user’s conjecture.
    Normally, however, we show something much stronger, namely that the
user’s conjecture and the refutation of its conjunctive normal form are logically
equivalent, by computing the latter from the former by successive term rewrit-
ing. From its earliest days, the original LCF theorem prover implemented its
rewriters via conversions [14], which still represent an impressive demonstration
of how higher-order functions can be used to design combinator languages [15].
ProofScript has excellent support for higher-order functions, and even though it
eschews the static type system familiar to users of Standard ML, we found this
gave us no real difficulty when it came to implementing and using conversions.
    In the next few sections, we shall discuss how we go about building the basic
infrastructure to compute the CNF form of the user’s conjecture. We shall then
describe how we send the version of the problem to METIS via callmetis and
how we interpret METIS’s resolution proof trace from its own kernel.

4.1    Primitive inference rules
Our kernel implements rules for a classical, monomorphic, simply typed lambda
calculus with just two primitive types: the type of propositions P and the type
U of ZFC sets. All theorems generated by this kernel are associated with rich
context objects, which provide the hypotheses of the theorem, and information
on how to resolve names to fully qualified identifiers with a logical type.
    The contexts are used to support structured declarative proof. At any point
in ProofScript code, there is an assumed context of constants that have been
introduced and assumptions which have been made of these constants, which
can be extended via primitive assume and let statements. ProofScript code
is then structured in nested blocks, allowing us to escape back into a parent
context as we leave each code block.
    The use of these contexts means that there is no need to distinguish con-
stants from free variables, as we do in traditional HOL based theorem provers.



                                       3
In ProofScript, we do not instantiate free variables in terms, but only spe-
cialise quantifiers. We believe this makes ProofScript conceptually simpler for
end-users, though as we shall discuss in the coming sections, it presents some
complications as far as interfacing with our resolution prover, which does make
such syntactic distinctions.

4.2     Conversions and conversionals
Historically, conversions were functions which take a term t and either produce
an equational theorem t = t′ or else throw an exception. These exceptions are
standardly caught by derived conversions which may try an alternative conver-
sion strategy. We do not support such an exception mechanism in ProofScript,
so our conversions must signal any errors via appropriate return values.
    Conversions are operated upon using higher-order functions called conver-
sionals, which allow us to build conversion strategies out of existing conversions,
targeting individual parts of a term and responding to failure by trying alter-
native strategies.
    Most of the 1500 lines of ProofScript library code which integrates Proof-
Script with METIS does so by way of conversions. We define about 50 conversions
and conversionals which are used around 500 times.

4.2.1   Basic conversions
Some basic conversions are mostly implemented directly in terms of the kernel’s
inference rules or via simple derived rules. Other conversionals exist simply to
deal with failure. The conversion c1 orElseConv c2 takes a term t and tries
c1 t, checks if it fails, and if so, returns c2 t instead. Another conversion,
noConv, is the identity of orElseConv, and is just the constant function to nil,
representing a conversion that always fails.
    The conversional thenConv provides sequencing, taking two conversions t        t′
      ′     ′′                                       ′′
and t      t , and producing the conversion t       t via a derived rule for transi-
tivity of equality. This conversional also has an identity, allConv, which is just
an alias for the kernel’s reflexivity inference rule.
    As noticed by Paulson [14], both conversionals are associative, with thenConv
distributing over orElseConv on the left. We also notice that, if we make conver-
sions non-deterministic such that they return lists of equations with the empty
list representing failure, we retain right-distributivity, while if we have them
return sets, we get all the axioms of a ring.

4.2.2   Subterm conversionals
ProofScript terms compose only as combinations and abstractions, and so it
suffices to define two basic conversionals which can be used to arbitrarily rewrite
subterms. The conversional combConv is implemented in terms of the primitive
kernel destructor destcomb, which splits combinations, and the inference rule
combine which says that combining equal terms yields equal combinations. The


                                         4
conversional accepts conversions f       g and x     y and yields the conversion
fx      g y.
    Another conversional deals with abstractions via the primitive kernel de-
structor destabs, which tears apart abstractions, and the inference rule abstract
which sends ∀x. φ(x) = ψ(x) to (x 7→ φ(x)) = (y 7→ ψ(y)). Using these, absConv
sends the conversion φ(x)     ψ(x) to the conversion x 7→ φ(x)     x 7→ ψ(x).
    It should be noted that ProofScript’s abstraction destructor differs from
those of traditional HOL systems, which would normally return the body of
the abstraction as a term with a new free variable. As mentioned in §4.1, all
ProofScript variables are bound, leaving only the constants. Thus, when passed
an abstraction, destabs returns a triple (v, φ(v), ctx), where ctx extends the
current context with a new declaration for a new constant c, and such that φ(c)
is a valid term in this context.
    By locally entering the returned context ctx, we can apply our conversion
φ(x)      ψ(x) which, if successful, yields the equational theorem φ(c) = ψ(c).
When this is returned to the enclosing context, the kernel discharges the con-
stant declaration and replaces the constant in the theorem with a universally
quantified variable. We can then apply the abstraction inference rule to yield
our desired result.
d e f absConv conv =
   tm =>
      match d e s t a b s tm
        c a s e [ ctx , _, body ] =>
           match i n c o n t e x t <ctx> conv body
               c a s e n i l => n i l
               c a s e th => a b s t r a c t ( l i f t ! th )
        c a s e _ => n i l


4.2.3     Other primitive conversions
As mentioned, ProofScript’s kernel inference rule reflexive is already a con-
version. There is one other kernel rule which is a conversion, namely normalize.
This sends a term to its βη long normal form.
   The following are the only other primitive conversions we need:
subsConv Given a theorem ⊢ t = t′ , sends t to a normalized t′ , and any other
     term to nil.
rewrConv1 Given a theorem

                  ⊢ ∀x1 x2 . . . , xn . φ(x1 , x2 , . . . , xn ) = ψ(x1 , x2 , . . . , xn )

        sends t to t′ if it finds a substitution θ such that t = φ(x1 , x2 , . . . , xn )[θ]
        and t′ = ψ(x1 , x2 , . . . , xn )[θ]. If no such substitution is found, returns
        nil 1 .
  1 The matching algorithm which finds θ is quite rudimentary, but sufficient for our purposes.




                                                 5
     Of these, only the primitive rewriting conversion rewrConv1 has a non-trivial
implementation in the form of a pattern matching algorithm for terms. The
pattern is represented by the left hand side of the quantified equation in the
theorem passed to rewrConv1.
     Here, there is some minor awkwardness in not having free variables. In a
regular HOL, a pattern is straightforwardly represented by a term, with the
substitutable atoms the free variables, and the unsubstitutable atoms the con-
stants. ProofScript does not support free variables, so we must instead represent
the substitutable parts of a pattern with bound variables and keep track of sub-
stitutions by associating new constants with binding positions.
     The conversion rewrConv1 therefore takes a quantified equational theorem
whose left-hand side is the pattern to match against. The quantified vari-
ables are the ones we can substitute for, and the quantifiers are stripped by
repeated applications of destabs, giving us the equational body in a new con-
text ctx where the quantified variables have been replaced with fresh variables
x1 , x2 , . . . , xn in the quantification order. These variables will have been de-
clared in ctx.
     We then prime our matching algorithm with a list of those constants, so
that it knows it can treat these as substitutable while all other variables must
be treated as fixed constants. The matching algorithm returns an instantiation
as an association list [(x1 , t1 ), (x2 , t2 ), . . . , (xn , tn )]. We can then specialise the
quantifiers of the original equational theorem in turn with t1 , t2 , . . . , tn , apply
the equational form of Modus Ponens 2 , and thus obtain the desired right-hand
side.

4.2.4    Proving theorems by conversion
By definition, a successful conversion proves a theorem given a term. But they
can also be used to infer non-equational theorems via convRule, which takes a
theorem, applies a conversion to its term, and if successful, uses the equational
form of Modus Ponens to prove the converted form of the theorem. We can
also prove non-equational theorems ⊢ φ is if we have a conversion φ           ⊤.
Equivalences of a proposition to true can be eliminated to the proposition via
a simple derived inference rule.

4.3     CNF Conversion
A full CNF conversion from ProofScript conjectures can be obtained through
the following passes:

    • convert the term to first-order by:
         – eliminating set builder notation;
         – lifting abstractions, by pulling them out to the front and making
           them the arguments to β redexes (let-definitions);
   2 This rule sends ⊢ φ = ψ and ⊢ φ to ⊢ ψ.




                                               6
        – lifting any terms of type P used as first-order function or predicate
          arguments, pulling them out to the front and making them the ar-
          guments to β redexes;
   • converting the term to its negation normal form:
        – eliminating all propositional connectives other than ∧, ∨ and ¬;
        – pushing all negations to the leaves of the term and eliminating double
          negations;
   • converting to prenex normal form by pulling all quantifiers out to the front
     of the formula;
   • converting the propositional matrix of the quantified formula to conjunc-
     tive normal form;
   • eliminating all quantifiers by skolemisation.

4.4    Tautology checking
The parts of the CNF conversion which manipulate propositional formulas are
easy enough to implement once we have proven a number of simple propositional
equivalences. These are tedious to obtain by hand, so it is helpful to be able to
decide and verify propositional tautologies automatically.
    A simple but complete tautology checker can be implemented by what amounts
to truth-table evaluation. First, we collect a list of equational rewrite theorems,
that tell us the semantics of each propositional connective in terms of its valu-
ations on ⊤ and ⊥ (theorems such as ⊢ ∀p. (p ∨ ⊤) = ⊤). Then, given a propo-
sitional conjecture, we sweep through and extract each variable p, performing
a case-analysis ⊢ p = ⊤ ∨ p = ⊥. Each complete case-analysis corresponds
to a row of a truth-table, and gives us a set of equations which evaluate each
variable. Next, using a derived conversional upConv, we descend to the leaves
of a term and then work upwards, applying our equations and rewrite rules,
calculating the truth value of the whole proposition and hoping to reach the ⊤.
    We thus have a tautology checker which can be used to prove classical propo-
sitional theorems of a few variables (and at most three at a time suits our pur-
poses). As a decision procedure, it can be easily integrated into declarative
proof by the ProofScript keyword by, as in the following code:
theorem andDeMorgan : ∀p q. (¬(p ∧ q)) = (¬p ∨ ¬q)
  by t a u t
    Case splitting on propositional variables, as we have done, requires that
we have first proven the law of excluded middle, which can be done via Dion-
conescu’s [5] proof, suitably modified for Hilbert’s indefinite description opera-
tor, which assumes full classical choice. ProofScript has a novel implementation
of choice, and, unlike the HOLs, does not take indefinite descriptions as primi-
tive. The classical inference is instead achieved automatically by ProofScript’s
rules for lifting theorems out of contexts:

                                        7
c h o o s e c h o i c e D e f : ’ ǫ : (P → P) → P ’
    l e t ’p : P → P ’
   assume ex : ’ ∃x. p x ’
    c h o o s e ’ cho sen : P ’ ex
    Here, we define an ǫ function based on a nested proof. This proof assumes
that there exists some object satisfying p and then chooses a witness. When
the assertion that the witness satisfies p is lifted out of the context, the assump-
tions are discharged and a quantifier introduced for the variable p, yielding the
theorem
                       ∀p. ∃chosen. (∃x. p x) → p chosen.
    By applying choose to this universal theorem, ProofScript will first skolem-
ize to

                       ∃chosen. ∀p. (∃x. p x) → p (chosen p)
and then introduce ǫ as a new Skolem constant.

4.5     Skolemisation
A higher-order theorem which captures the main rewrite rule we need to perform
skolemisation is given by:

                     ⊢ ∀p. (∀x. ∃y. p x y) = (∃f. ∀x. p x (f x)).               (1)
   Repeated rewriting with this theorem allows us to fully skolemize. To take
an example:


      ∀x y : U. ∃z : U. P x y z = ∀x : U. ∃f : U → U. ∀y. P x y (f y)
                                = ∃g : U → U → U. ∀x. ∀y. P x y (g y x).

.
    But notice that the type of f in the second formula differs from the type
of g in the third, meaning that we are applying variants of (1) with different
types. This is no issue in traditional HOLs which support a simple form of type
polymorphism and type instantiation. ProofScript, however, due to a deliberate
decision to limit the expressivity of its higher-order metalogic, can only express
the above as a monomorphic theorem.
    This means that an arbitrary number of variants of (1) may be needed
to skolemize theorems in ProofScript, each requiring its own proof, because
there are infinitely many possible types that the Skolem functions may inhabit.
The best we can hope to do is capture the theorems in a single definition, a
metatheorem expressed in the language of ProofScript, as it were:
d e f skolemThm [ a , b ] =
   theorem ’ ∀p. (∀x. ∃y. p x y) = (∃f : ‹a› → ‹b›. ∀x. p x (f x)) ’
   ...

                                            8
    Here, ProofScript inserts the type variables passed as function arguments a
and b into the ‹ › quoted positions of the theorem.
    This is still an unpleasant state of affairs, since every time we call skolemThm,
we may find ourselves redoing a proof, namely when the arguments a and b have
been passed in before. Our solution is to introduce a primitive memoisation
mechanism via the ProofScript keyword table. This can replace def in the
above code and will cause ProofScript to save the result of calls to skolemThm
and return the saved copy whenever the function is called with the same argu-
ments.
    In general, it is worth being wary of the consequences of one’s decisions to
simplify a logic because one does not have need of the expressive power. While
we have chosen to keep the logic monomorphic to encourage users to work as
much as possible within the ZF object logic, we would not want to push this to
the point of using a first-order logic, where we cannot properly express axioms
such as the axiom of comprehension, and where we would require the system to
waste time proving arbitrarily many instances of metatheorems for any generally
useful consequence of such axioms.
    With conversions, the ProofScript code which performs the CNF conversion
is structurally very similar to the pseudocode algorithms which do the same, but
with the benefit that any result is formally verified for correctness. Conversions
give us a powerful way to drive computation, and are well suited to this sort of
algebraic normalisation.


5     Talking to METIS
METIS’s logical kernel deals only in CNF clauses, which are represented as sets
of literals. There are no connectives or quantifiers in the logical syntax.

5.1    Representing METIS clauses and certificates
METIS proof certificates are returned to ProofScript as a tree, rooted at the
empty clause which represents the refutation, and with nodes labelled with
clauses derived and the inference rule used. The possible rules are:

Axiom leaf nodes containing an arbitrary clause;
Assume leaf nodes with clause of the form {φ, ¬φ};
Refl leaf nodes with clause of the form {x = x};
Equality(L(x), s, t) leaf nodes with a clause of the form {s 6= t, L′ , L[t/x]}
     where L′ is the negation of L[s/x];
RemoveSym a derived rule in Hurd’s implementation, this node has a clause
     which is the same as its child, minus duplicate equalities and inequalities
     (up to symmetry of equality);



                                         9
Irreflexive a node which is the same as its child, but without literals of the
     form x 6= x;
Subst(θ) a node whose clause is a substitution θ of its child clause;
Resolve(L) uses of the resolution rule mark nodes with two children, whose
     clauses are of the form C1 ∪ {L} and C2 ∪ {L′ } where L′ is the negation
     of L. The resolution’s clause is C1 ∪ C2 − {L, L′ }.

    Generally, the more powerful METIS’s kernel rules, the more work we have cut
out for us on the ProofScript side. For one example, METIS implements clauses
as sets of literals, and so assumes a bunch of rules for working with disjunctions
without telling us how they are applied. For another, we have taken the liberty
of replacing some of METIS’s derived kernel rules with primitive ones, but each
such liberty comes at a cost of extra work in certificate translation.
    To deal with literals as sets, it makes sense to ensure that our ProofScript
clause representation is in some normal form, and for us, that just means making
sure we are always normalised with respect to associativity and idempotency of
disjunction. In that way, we can treat our clauses as lists of literals with unique
elements. Passes over the clause to remove duplicates are only needed to imple-
ment Subst and Resolve, and are handled with a conversion nubClauseConv.
We need no pass for associativity, which is always preserved by our implemen-
tation of the METIS kernel rules.
    In ProofScript, we represent proof certificates as a tree made by nesting lists,
with clauses as sets and literals encoded in an S-expression like format according
to θ:
            
            
             t, if t is a variable
              [F, θ(t1 ), θ(t2 ), . . . , θ(tn )], if t is the function application
            
            
            
            
            
                    F (t1 , t2 , . . . , tn ) with function symbol F
            
            
            
            
    θ(t) = [true, [P, θ(t1 ), θ(t2 ), . . . , θ(tn )]], if t is the positive literal
            
                    P (t1 , t2 , . . . , tn ) with predicate symbol P
            
            
            
            
            
            
            
            
             [false, [P, θ(t1 ), θ(t2 ), . . . , θ(tn )]], if t is the negative literal
                    ¬P (t1 , t2 , . . . , tn ) with predicate symbol P .
            

   Our port of METIS has literals which are polymorphic in variable, function
symbol and predicate symbol alphabets, and it is up to the caller to decide what
alphabets to use. So can get away with just using actual ProofScript function
terms as METIS function symbols and Proofscript predicate terms as predicate
symbols.

5.1.1   Free variables aren’t
METIS variables often need to be instantiated, so when represented as a Proof-
Script theorem, they must be bound in clauses by quantifiers. Since they must
also be instantiated on a clause-by-clause basis, we need a set of bindings per


                                          10
clause. However, METIS likes to be able to identify variables across clauses, even
as it substitutes for them independently.
     We cannot make this identification reliably in ProofScript, which only iden-
tifies bound variables between clauses up to α-equivalence, and even if we have
some control over the naming of variables, we cannot reliably control Proof-
Script’s naming of fresh ones.
     The best we can do is single out a variable by the index of its binding site (the
DeBruijn index in this case), but with METIS potentially generating hundreds
of fresh variables during resolution, it would be disastrous to take such indices
as a direct representation of METIS variables.
     Instead, we introduce maps from bound variable indices to METIS variables
and carry the mapping around in our clauses. A clause of n variables and m
literals is therefore represented by a pair consisting of a list of METIS variables
and a ProofScript theorem:

            ([v1 , v2 , v3 , . . . , vn ], ⊢ ∀x1 x2 . . . xn . φ1 ∨ φ2 ∨ . . . ∨ φm ).

   where we assume that the ith bound variable corresponds to the METIS vari-
able vi . Plain integers make a convenient choice for the representation of these
METIS variables, and at the call-site, we ask the resolution prover to use them
both internally and in proof certificates. For a concrete example, the METIS
clause {p(3, 8), ¬q(2, 5)} could be represented by any of the ProofScript pairs:

                 ([3, 2, 8, 5], ⊢ ∀x y z w. p x z ∨ ¬q y w);
                 ([8, 5, 3, 2], ⊢ ∀a b c d. ¬q d b ∨ (p c a));
                 ([5, 2, 8, 3], ⊢ ∀x1 x2 x3 x4 . p x4 x3 ∨ ¬q x2 x1 ).

Now suppose we want to perform the substitution [h(1, 2, 9)/8]. The resulting
clause will be {p(3, h(1, 2, 9)), ¬q(2, 5)}, represented by a ProofScript clause that
is α-equivalent to

                         ⊢ ∀x y z u v. p x (h y z u) ∨ ¬q z v.
   To find this, we must first figure out how many bound variables will be
needed after the substitution, generate fresh constants for them, and then recre-
ate the mapping from indices to METIS free variables.
   Next suppose we want to resolve our new clause with {q(2, 5), r(4, 6)} which
might happen to be represented by

                        ([5, 4, 2, 6], ⊢ ∀x y z w. r y w ∨ q z x).
    We can strip away quantifiers from one of the clauses to get at the literals,
introducing new constants into the current context along the way, but we will
have to make sure that we instantiate rather introduce variables in the other
clause whenever our bound variable mappings tell us there is a match. And after
resolution, we will have lost the free METIS variable 5, and so will be deleting it
from our index mapping.


                                               11
    This requires a lot of delicate work, and a clear understanding of how the
introduction of universal quantifiers by lifting out of contexts can be exploited
programmatically. It is not the sort of thing we expect the average ProofPeer
user to get their hands dirty with, though if they feel the need to, the tight fit
between ProofScript’s structured proof language and its programming language
should make it seem natural. But the regular user, we hope, will mostly enjoy
writing simple theorems such as the following, based on our working implemen-
tation of METIS:
l e t oneDef : ’ one = P ∅ ’
l e t twoDef : ’ two = P one ’

theorem one : ’ ∀x.x ∈ one = (x = ∅) ’
  by m e t i s [ empty , oneDef , power , s u b s e t , e x t ]

theorem two : ’ ∀x. x ∈ two = (x = ∅ ∨ x = one) ’
  by m e t i s [ empty , one , twoDef , power , s u b s e t , e x t ]

theorem oneNotZero : ’ ¬(∅ = one) ’
  by m e t i s [ empty , one ]


6    Conclusion
The scripting language for ProofPeer, aptly named ProofScript, is intended to
be the programmable metalanguage for an LCF kernel, but what distinguishes
it from other languages designed for this purpose, such as Standard ML, is that
it aims primarily to be the natural vehicle for writing accessible, declarative
proofs, where black-box automation is left to fill out the tedious gaps.
     The route we have taken towards this goal has not required any stops at
the tactic systems or contextual rewriters of traditional LCF, but we have made
extensive use of conversions and higher-order conversionals in order to connect to
the METIS first-order theorem prover. If the success of the Isabelle Sledgehammer
project is anything to go by, this could be the only integrated tool that we need
when it comes to first-order automated proof.
     ProofScript shares qualities of the ML dialects in its succinctness and support
for higher-order functions, and we were pleased that we were able to reason easily
with what would become quite complex types in ML. We did not really miss the
static type system reminding us not to mix list parameterised conversionals with
term parameterised ones. This is not to say that there are not other benefits to
having a type system, in terms of automatic documentation in type-signatures
and in supporting refactoring of complex code-bases, but our needs are quite
modest for now.
     When designing the logic of ProofScript, we aimed at some conceptual sim-
plifications so as not to distract users. Users are not left to choose between
building mathematical structures out of user-defined types and exhibiting those


                                          12
structures in ZFC sets as they are in HOL/ZFC [2]. Our type inference [13]
algorithm guides users away from polymorphic universes to the ZFC one. And
users writing declarative proofs are not left wondering what the difference is be-
tween a universally quantified theorem and one where all the variables are free
to be instantiated. The distinction between free variables and constants is just
a logical confusion to a user working in a declarative setting where constants
can be freely introduced in local contexts.
    But when it comes to the nuts-and-bolts of programming proofs, there is
sometimes another story. Simple polymorphic types can improve the efficiency of
proofs by replacing infinitely many metatheorems with a single instantiable one.
And free variables, effectively being named holes in terms and theorems which
can be identified across contexts, become a means by which a programmer can
represent their own instantiation mechanisms. Not having such things meant
that in sections 4.2.3 and 5.1.1, we were forced to shadow DeBruijn indices with
our own metadata. This is just the usual reminder that there are balances to be
struck between conceptual simplicity and practicalities. We feel justified that
we have struck such a balance.
    Future work on automation in ProofPeer will focus on replicating the impres-
sive and ongoing development of Sledgehammer and its HOL Light counterpart
HOL(y) Hammer [7], thus allowing Proofscript to access a wide variety of pow-
erful ATP tools which can then be used to advise the METIS prover. As we
proceed, we expect that the necessary infrastructure of ProofScript will remain
lean compared to those of its friends in the LCF tradition.


References
 [1] Proofscript:       Proof     scripting   for               the       masses.
     http://proofpeer.net/papers/proofscript.
 [2] Sten Agerholm and Mike Gordon. Experiments with ZF Set Theory in
     HOL and Isabelle. In in Proceedings of the 8th International Workshop on
     Higher Order Logic Theorem Proving and its Applications, LNCS, pages
     32–45. Springer-Verlag, 1995.
 [3] Jasmin Christian Blanchette, Sascha Böhme, Mathias Fleury, Steffen Juilf
     Smolka, and Albert Steckermeier. Semi-intelligible Isar Proofs from
     Machine-Generated Proofs. Journal of Automated Reasoning, 56(2):155–
     200, 2015.
 [4] Pierre Corbineau. Types for Proofs and Programs: International Confer-
     ence, TYPES 2007, Cividale des Friuli, Italy, May 2-5, 2007 Revised Se-
     lected Papers, chapter A Declarative Language for the Coq Proof Assistant,
     pages 69–84. Springer Berlin Heidelberg, Berlin, Heidelberg, 2008.
 [5] Radu Diaconescu. Axiom of Choice and Complementation. Proceedings of
     the American Mathematical Society, 51(1):pp. 176–178, 1975.


                                       13
 [6] Joe Hurd. First-Order Proof Tactics in Higher-Order Logic Theorem
     Provers. In Myla Archer, Ben Di Vito, and César Muñoz, editors, Design
     and Application of Strategies/Tactics in Higher Order Logics (STRATA
     2003), number NASA/CP-2003-212448 in Technical Reports, pages 56–68,
     September 2003.
 [7] Cezary Kaliszyk and Josef Urban. HOL(y)Hammer: Online ATP Service
     for HOL Light. Mathematics in Computer Science, 9(1):5–22, 2014.
 [8] Laura Kovács and Andrei Voronkov. First-Order Theorem Proving and
     Vampire. In Natasha Sharygina and Helmut Veith, editors, Computer Aided
     Verification: 25th International Conference, CAV 2013, Saint Petersburg,
     Russia., pages 1–35, Berlin, Heidelberg, 2013. Springer Berlin Heidelberg.
 [9] Jia Meng, Claire Quigley, and Lawrence C. Paulson. Automation for inter-
     active proof: First prototype. Inf. Comput., 204(10):1575–1596, 2006.
[10] Christopher P Wadsworth Michael J Gordon, Arthur J Milner. Edinburgh
     LCF. Springer-Verlag, 1979.
[11] Tobias Nipkow. A Tutorial Introduction to Structured Isar Proofs.
     http://www.cl.cam.ac.uk/research/hvg/Isabelle/dist/Isabelle2011/doc/isar-overview.pdf/.
[12] Steven Obua, Jacques D. Fleuriot, Phil Scott, and David Aspinall. Proof-
     Peer: Collaborative Theorem Proving. CoRR, abs/1404.6186, 2014.
[13] Steven Obua, Jacques D. Fleuriot, Phil Scott, and David Aspinall. Type
     Inference for ZFH. In Manfred Kerber, Jacques Carette, Cezary Kaliszyk,
     Florian Rabe, and Volker Sorge, editors, Intelligent Computer Mathematics
     - International Conference, CICM 2015, Washington, DC, USA, July 13-
     17, 2015, Proceedings, volume 9150 of Lecture Notes in Computer Science,
     pages 87–101. Springer, 2015.
[14] Lawrence C. Paulson. A Higher-Order Implementation of Rewriting. Sci-
     ence of Computer Programming, 3, 1983.
[15] S. Doaitse Swierstra, Pablo R. Azero Alcocer, and João Saraiva. Design-
     ing and Implementing Combinator Languages. In Advanced Functional
     Programming, volume 1608 of Lecture Notes in Computer Science, pages
     150–206. Springer, 1999.
[16] Christoph Weidenbach, Dilyana Dimova, Arnaud Fietzke, Rohit Kumar,
     Martin Suda, and Patrick Wischnewski. SPASS Version 3.5. In Re-
     nate A. Schmidt, editor, 22nd International Conference on Automated
     Deduction, Montreal, Canada., pages 140–145, Berlin, Heidelberg, 2009.
     Springer Berlin Heidelberg.
[17] Freek Wiedijk. Mizar Light for HOL Light. In Theorem Proving in Higher
     Order Logics, volume 2152, pages 378–394, London, UK, 2001. Springer-
     Verlag.


                                      14
