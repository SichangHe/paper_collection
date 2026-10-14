                 Flexible Proof Production
           in an Industrial-Strength SMT Solver

    Haniel Barbosa1 , Andrew Reynolds2 , Gereon Kremer3 , Hanna Lachnitt3 ,
       Aina Niemetz3 , Andres Nötzli3 , Alex Ozdemir3 , Mathias Preiner3 ,
      Arjun Viswanathan2 , Scott Viteri3 , Yoni Zohar4(B) , Cesare Tinelli2 ,
                              and Clark Barrett3
            1
                Universidade Federal de Minas Gerais, Belo Horizonte, Brazil
                        2
                           The University of Iowa, Iowa City, USA
                           3
                             Stanford University, Stanford, USA
                         4
                           Bar-Ilan University, Ramat Gan, Israel
                                   yoni206@gmail.com

       Abstract. Proof production for SMT solvers is paramount to ensure
       their correctness independently from implementations, which are often
       prohibitively diﬃcult to verify. Historically, however, SMT proof pro-
       duction has struggled with performance and coverage issues, resulting in
       the disabling of many crucial solving techniques and in coarse-grained
       (and thus hard to check) proofs. We present a ﬂexible proof-production
       architecture designed to handle the complexity of versatile, industrial-
       strength SMT solvers and show how we leverage it to produce detailed
       proofs, including for components previously unsupported by any solver.
       The architecture allows proofs to be produced modularly, lazily, and with
       numerous safeguards for correctness. This architecture has been imple-
       mented in the state-of-the-art SMT solver cvc5. We evaluate its proofs
       for SMT-LIB benchmarks and show that the new architecture produces
       better coverage than previous approaches, has acceptable performance
       overhead, and supports detailed proofs for most solving components.


1    Introduction
SMT solvers [9] are widely used as backbones of formal methods tools in a
variety of applications, often safety-critical ones. These tools rely on the solver’s
correctness to guarantee the validity of their results such as, for instance, that an
access policy does not inadvertently give access to sensitive data [4]. However,
SMT solvers, particularly industrial-strength ones, are often extremely complex
pieces of engineering. This makes it hard to ensure that implementation issues do
not aﬀect results. As the industrial use of SMT solvers increases, it is paramount
to be able to convince non-experts of the trustworthiness of their results.
    A solution is to decouple conﬁdence from the implementation by coupling
results with machine-checkable certiﬁcates of their correctness. For SMT solvers,
This work was partially supported by the Oﬃce of Naval Research (Contract No.
68335-17-C-0558), a gift from Amazon Web Services, and by NSF-BSF grant numbers
2110397 (NSF) and 2020704 (BSF).
c The Author(s) 2022
J. Blanchette et al. (Eds.): IJCAR 2022, LNAI 13385, pp. 15–35, 2022.
https://doi.org/10.1007/978-3-031-10769-6_3
16      H. Barbosa et al.

this amounts to providing proofs of unsatisﬁability. The main challenges are
justifying a combination of theory-speciﬁc algorithms while keeping the solver
performant and providing enough details to allow scalable proof checking, i.e.,
checking that is fundamentally simpler than solving. Moreover, while proof pro-
duction is well understood for propositional reasoning and common theories,
that is not the case for more expressive theories, such as the theory of strings,
or for more advanced solver operations such as formula preprocessing.
     We present a new, ﬂexible proof-production architecture for versatile, indus-
trial-strength SMT solvers and discuss its integration into the cvc5 solver [5]. The
architecture (Sect. 2) aims to facilitate the implementation eﬀort via modular
proof production and internal proof checking, so that more critical components
can be enabled when generating proofs. We provide some details on the core proof
calculus and how proofs are produced (Sect. 3), in particular how we support
eager and lazy proof production with built-in proof reconstruction (Sect. 3.2).
This feature is particularly important for substitution and rewriting techniques,
facilitating the instrumentation of notoriously challenging functionalities, such as
simpliﬁcation under global assumptions [6, Section 6.1] and string solving [40,46,
48], to produce detailed proofs. Finally, we describe (Sect. 5) how the architecture
is leveraged to produce detailed proofs for most of the theory reasoning, critical
preprocessing, and underlying SAT solving of cvc5. We evaluate proof production
in cvc5 (Sect. 6) by measuring the proof overhead and the proof quality over an
extensive set of benchmarks from SMT-LIB [8].
     In summary, our contributions are a ﬂexible proof-producing architecture
for state-of-the-art SMT solvers, its implementation in cvc5, the production of
detailed proofs for simpliﬁcation under global assumptions and the full theory
of strings, and initial experimental evidence that proof-production overhead is
acceptable and detailed proofs can be generated for a majority of the problems.
Preliminaries. We assume the usual notions and terminology of many-sorted
ﬁrst-order logic with equality (≈) [29]. We consider signatures Σ all containing
the distinguished Boolean sort Bool. We adopt the usual deﬁnitions of well-sorted
Σ-terms, with literals and formulas as terms of sort Bool, and Σ-interpretations.
A Σ-theory is a pair T = (Σ, I) where I, the models of T , is a class of Σ-
interpretations closed under variable reassignment. A Σ-formula ϕ is T-valid
(resp., T-unsatisfiable) if it is satisﬁed by all (resp., no) interpretations in I.
Two Σ-terms s and t of the same sort are T-equivalent if s ≈ t is T -valid.
We write a to denote a tuple (a1 , . . . , an ) of elements, with n ≥ 0. Depending
on context, we will abuse this notation and also denote the set of the tuple’s
elements or, in case of formulas, their conjunction. Similarly, for term tuples s, t
of the same length and sort, we will write s ≈ t to denote the conjunction of
equalities between their respective elements.


2    Proof-Production Architecture
Our proof-production architecture is intertwined with the CDCL(T ) architec-
ture [43], as shown in Fig. 1. Proofs are produced and stored modularly by each
solving component, which also checks they meet the expected proof structure
             Flexible Proof Production in an Industrial-Strength SMT Solver                17


                                 Pre-processor           ϕ

                               φ1 ... φn                 L
                                                        P:L
                      Propositional Engine                            Theory Engine

                                   Clausifier                       Theory Combination
P : ϕ → φ1                                 C1p ... Cm
                                                    p
                                                               P : L1 L1          L2 P : L2
                 P : ψ1 → C1
    ...




P : ϕ → φn                        SAT Solver                          T1    ...       T2
                    ...




                P : ψm → Cm                   →⊥
                                           P:C                             Lk P : Lk
                                Post-processor
                                                                            Tk


                                                Asserted Literals
               →⊥
             P:φ
                                                                                  ⊥
                                           SMT Proof Post-processor               P:ϕ→⊥


Fig. 1. Flexible proof-production architecture for CDCL(T )-based SMT solvers. In the
               L}
above, ψi ∈ {φ,   for each i, with ψi not necessarily distinct from ψi+1 .



for that component, as described below. Proofs are combined only when needed,
via post-processing. The pre-processor receives an input formula ϕ and simpliﬁes
it in a variety of ways into formulas φ1 , . . . , φn . For each φi , the pre-processor
stores a proof P : ϕ → φi justifying its derivation from ϕ.
     The propositional engine receives the preprocessed formulas, and its clausifier
converts them into a conjunctive normal form C1 ∧ · · · ∧ Cl . A proof P : ψ → Ci
is stored for each clause Ci , where ψ is a preprocessed formula. Note that sev-
eral clauses may derive from each formula. Corresponding propositional clauses
C1p , . . . , Clp , where ﬁrst-order atoms are abstracted as Boolean variables, are sent
to the SAT solver, which checks their joint satisﬁability. The propositional engine
enters a loop with the theory engine, which considers a set of literals asserted
by the SAT solver (corresponding to a model of the propositional clauses) and
veriﬁes its satisﬁability modulo a combination of theories T . If the set is T -
unsatisﬁable, a lemma L is sent to the propositional engine together with its
proof P : L. Note that since lemmas are T -valid, their proofs have no assump-
tions. The propositional engine stores these proofs and clausiﬁes the lemmas,
keeping the respective clausiﬁcation proofs in the clausiﬁer. The clausiﬁed and
abstracted lemmas are sent to the SAT solver to block the current model and
cause the assertion of a diﬀerent set of literals, if possible. If no new set is
asserted, then all the clauses C1 , . . . , Cm generated until then are jointly unsat-
isﬁable, and the SAT solver yields a proof P : C1 ∧ · · · ∧ Cm → ⊥. Note that
the proof is in terms of the ﬁrst-order clauses, as are the derivation rules that
18      H. Barbosa et al.

conclude ⊥ from them. The propositional abstraction does not need to be rep-
resented in the proof.
    The post-processor of the propositional engine connects the assumptions of
the SAT solver proof with the clausiﬁer proofs, building a proof P : φ1 ∧· · ·∧φn →
⊥. Since theory lemmas are T -valid, the resulting proof only has preprocessed
formulas as assumptions. The ﬁnal proof is built by the SMT solver’s post-
processor combining this proof with the preprocessing proofs P : ϕ → φi . The
resulting proof P : ϕ → ⊥ justiﬁes the T -unsatisﬁability of the input formula.


3     The Internal Proof Calculus

In this section, we specify how proofs are represented in the internal calculus of
cvc5. We also provide some low-level details on how proofs are constructed and
managed in our implementation.
    The proof rules of the internal calculus are similar to rules in other calculi for
ground ﬁrst-order formulas, except that they are made a little more operational
by optionally having argument terms and side conditions. Each rule has the form

                  ϕ1 · · · ϕn                ϕ1 · · · ϕn | t1 , . . . , tm
              r                   or     r                                 if C
                      ψ                                 ψ
with identifier r, premises ϕ1 , . . . , ϕn , arguments t1 , . . . , tm , conclusion ψ, and
side condition C. The argument terms are used to construct the conclusion from
the premises and can be used in the side condition together with the premises.


3.1   Proof Checkers and Proofs

The semantics of each proof rule r is provided operationally in terms of a proof-
rule checker for r. This is a procedure that takes as input a list of argument
terms t and a list of premises ϕ for r. It returns fail if the input is malformed,
i.e., it does not match the rule’s arguments and premises or does not satisfy the
side condition. Otherwise, it returns a conclusion formula ψ expressing the result
of applying the rule. All proof rules of the internal calculus have an associated
proof-rule checker. We say that a proof rule proves a formula ψ, from given
arguments and premises, if its checker returns ψ.
     cvc5 has an internal proof checker built modularly out of the individual
proof-rule checkers. This checker is meant mostly for internal debugging dur-
ing development, to help guarantee that the constructed proofs are correct. The
expectation is that users will rely instead on third-party tools to check the proof
certiﬁcates emitted by the solver.
     A proof object is constructed internally using a data structure that we will
                                                                      , t) consisting
describe abstractly here and call a proof node. This is a triple (r, N
of a rule identiﬁer r; a sequence N of proof nodes, its children; and a sequence t
of terms, its arguments. The relationships between proof nodes and their children
induces a directed graph over proof nodes, with edges from proofs nodes to their
children. We call a single-root graph rooted at node N a proof. A proof P is
              Flexible Proof Production in an Industrial-Strength SMT Solver        19




                   Fig. 2. Core proof rules of the internal calculus.


well-formed if it is ﬁnite, acyclic, and there is a total mapping Ψ from the
nodes of P to formulas such that, for each node N = (r, (N1 , . . . , Nm ), t), Ψ (N )
is the formula returned by the proof checker for rule r when given premises
Ψ (N1 ), . . . , Ψ (Nn ) and arguments t. For a well-formed proof P with root N and
mapping Ψ , the conclusion of P is the formula Ψ (N ); a subproof of P is any
proof rooted at a descendant of N in P . For convenience, we will identify a
well-formed proof with its root node from now on.


3.2    Core Proof Rules
In total, the internal calculus of cvc5 consists of 155 proof rules,1 which cover
all reasoning performed by the SMT solver, including theory-speciﬁc rules, rules
for Boolean reasoning, and others. In the remainder of this section, we describe
the core rules of the internal calculus, which are used throughout the system,
and are illustrated in Fig. 2.
Proof Rules for Equality. Many theory solvers in cvc5 perform theory-speciﬁc
reasoning on top of basic equational reasoning. The latter is captured by the
proof rules eq res, refl, symm, trans, and cong. The ﬁrst rule is used to prove a
formula ψ from a formula ϕ that was proved equivalent to ψ. The rest are the
standard rules for computing the congruence closure of a set of term equalities.
Proof Rules for Rewriting, Substitution and Witness Forms. A single
coarse-grained rule, sr, is used for tracking justiﬁcations for core utilities in the
SMT solver such as rewriting and substitution. This rule, together with other
non-core rules with side conditions (omitted for brevity), allows the generation of
coarse-grained proofs that trust the correctness of complex side conditions. Those
conditions involve rewriting and substitution operations performed by cvc5 dur-
ing solving. More ﬁne-grained proofs can be constructed from coarse-grained
ones by justifying the various rewriting and substitution steps in terms of sim-
pler proof rules. This is done with the aid of the equality rules mentioned above
and the additional core rules atom rewrite and witness. To describe atom rewrite,
witness, and sr, we ﬁrst need to introduce some deﬁnitions and notations.

1
    See https://cvc5.github.io/docs/cvc5-1.0.0/proofs/proof rules.html.
20        H. Barbosa et al.

     A rewriter R is a function over terms that preserves equivalence in the back-
ground theory T , i.e., returns a term t↓R T -equivalent to its input t. We call
t↓R the rewritten form of t with respect to R. Currently, cvc5 uses a handful
of specialized rewriters for various purposes, such as evaluating constant terms,
preprocessing input formulas, and normalizing terms during solving. Each indi-
vidual rewrite step executed by a rewriter R is justiﬁed in ﬁne-grained proofs
by an application of the rule atom rewrite, which takes as argument both (an
identiﬁer for) R and the term s the rewrite was applied to. Note that the rule’s
soundness requires that the rewrite step be equivalence preserving.
     A (term) substitution σ is a ﬁnite sequence (t1 → s1 , . . . , tn → sn ) of oriented
pairs of terms of the same sort. A substitution method S is a function that takes a
term r and a substitution σ and returns a new term that is the result of applying
σ to r, according to some strategy. We write S(r, σ) to denote the resulting term.
We distinguish three kinds of substitution methods for σ: simultaneous, which
returns the term obtained by simultaneously replacing every occurrence of term
ti in r with si , for i = 1, . . . , n; sequential, which splits σ into n substitutions
(t1 → s1 ), . . . , (tn → sn ) and applies them in sequence to r using the simultane-
ous strategy above; and fixed-point, which, starting with r, repeatedly applies σ
with the simultaneous strategy until no further subterm replacements are pos-
sible. For example, consider the application S(y, (x → u, y → f (z), z → g(x))).
The steps the substitution method takes in computing its result are the fol-
lowing: y  f (z) if S is simultaneous; y  f (z)  f (g(x)) if S is sequential;
y  f (z)  f (g(x))  f (g(u)) if S is ﬁxed-point.
     In cvc5, we use a substitution derivation method D to derive a contextual
substitution (t1 → s1 , . . . , tn → sn ) from a collection ϕ
                                                               of derived formulas. The
substitution essentially orients a selection of term equalities ti ≈ si entailed by
ϕ
 and, as such, can be applied soundly to formulas derived from ϕ            .2 We write
D(ϕ) to denote the substitution computed by D from ϕ           .
     Finally, cvc5 often introduces fresh variables, or Skolem variables, which are
implicitly globally existentially quantiﬁed. This happens as a consequence of
Skolemization of existential variables, lifting of if-then-else terms, and some kinds
of ﬂattening. Each Skolem variable k is associated with a term k↑ of the same
sort containing no Skolem variables, called its witness term. This global map
from Skolem variables to their witness term allows cvc5 to detect when two
Skolem variables can be equated, as a consequence of their respective witness
terms becoming equivalent in the current context [47]. Witness terms can also be
used to eliminate Skolem variables at proof output time. We write t↑ to denote
the witness form of term t, which is obtained by replacing every Skolem variable
in t by its witness term. For example, if k1 and k2 are Skolem variables with
associated witness terms ite(x ≈ z, y, z) and y − z, respectively, and ϕ is the
formula ite(x ≈ k2 , k1 ≈ y, k1 ≈ z), the witness form ϕ↑ of ϕ is the formula
ite(x ≈ y − z, ite(x ≈ z, y, z) ≈ y, ite(x ≈ z, y, z) ≈ z). When a Skolem variable k


2
      Observe that substitutions are generated dynamically from the formulas being pro-
     cessed, whereas rewrite rules are hard-coded in cvc5’s rewriters.
              Flexible Proof Production in an Industrial-Strength SMT Solver      21

appears in a proof, the witness proof rule is used to explicitly constrain its value
to be the same as that of the term k↑ it abstracts.3
    We can now explain the sr proof rule, which is parameterized by a substitution
method S, a rewriter R, and substitution derivation method D. The rule is used
to transform the proof of a formula ϕ into one of a formula ψ provided that the
two formulas are equal up to rewriting under a substitution derived from the
premises ϕ . Note that this rule is quite general because its conclusion ψ, which
is provided as an argument, can be any formula that satisﬁes the side condition.
Proof Rules for Scoped Reasoning. Two of the core proof rules, assume
and scope, enable local reasoning. Together they achieve the eﬀect of the ⇒-
introduction rule of Natural Deduction. However, separating the local assump-
tion functionality in assume provides more ﬂexibility. That rule has no premises
and introduces a local assumption ϕ provided as an argument. The scope rule
is used to close the scope of the local assumptions ϕ1 , . . . , ϕn made to prove a
formula ϕ, inferring the formula ϕ1 ∧ · · · ∧ ϕn ⇒ ϕ.
    We say that ϕ is a free assumption in proof P if P has a node (assume, (), ϕ)
that is not a subproof of a scope node with ϕ as one of its arguments. A proof
is closed if it has no free assumptions, and open otherwise.
Soundness. All proof rules other than assume are sound with respect to the
background theory T in the following sense: if a rule proves a formula ψ from
premises ϕ , every model of T that satisﬁes ϕ  , and assigns the same values to
Skolem variables and their respective witness term, satisﬁes ψ as well. Based on
this and a simple structural induction argument, one can show that well-formed
closed proofs have T -valid conclusions. In contrast, open proofs have conclusions
that are T -valid only under assumptions. More precisely, in general, if ϕ  are all
the free assumptions of a well-formed proof P with conclusion ψ and k are all
the Skolem variables introduced in P , then k ≈ k↑ ∧ ϕ ⇒ ψ is T -valid.


3.3    Constructing Proof Nodes

We have implemented a library of proof generators that encapsulates common
patterns for constructing proof nodes. We assume a method getProof that takes
the proof generator g and a formula ϕ as input and returns a proof node with
conclusion ϕ based on the information in g. During solving, cvc5 uses a combina-
tion of eager and lazy proof generation. In general terms, eager proof generation
involves constructing proof nodes for inference steps at the time those steps are
taken during solving. Eager proof generation may be required if the computation
state pertinent to that inference cannot be easily recovered later. In contrast,
lazy proof generation occurs for inferred formulas associated with proof genera-
tors that can do internal bookkeeping to be able to construct proof nodes for the
formula after solving is completed. Depending on the formula, diﬀerent kinds of
proof generators are used. For brevity, we only describe in detail (see Sect. 3.2)
3
    The proof rules that account for the introduction of Skolem variables in the ﬁrst
    place are not part of the core set and so are not discussed here.
22       H. Barbosa et al.

Algorithm 1 . Proof generation for term-conversion generators, rewrite-once
policy. B is a lazy proof builder, R a map from terms to their converted form,
and cpre , cpost are sets of pairs of equalities and the proof generators justifying
them.
getProof(g, ϕ) where g contains cpre , cpost and ϕ is t1 ≈ t2
 1: B := ∅, R := ∅
 2: getTermConv(t1 , cpre , cpost , B, R)
 3: if R[t1 ] = t2 then fail else return getProof(B, t1 ≈ R[t1 ])
getTermConv(s, cpre , cpost , B, R), where s = f (s1 , . . . , sn )
 1: if s in dom(R) then return
 2: if (s ≈ s , g  ) ∈ cpre for some s , g  then
 3:    R[s] := s , addLazyStep(B, s ≈ s , g  )
 4:    return
 5: for 1 ≤ i ≤ n do getTermConv(si , cpre , cpost , B, R)
 6: R[s] := r, where r = f (R[s1 ], . . . , R[sn ])
 7: if s = r then addStep(B, cong, (s1 ≈ R[s1 ], . . . , sn ≈ R[sn ]), f )
 8: else addStep(B, rfl, (), s ≈ s)
 9: if (r ≈ r , g  ) ∈ cpost for some r , g  then
10:    R[s] := r , addLazyStep(B, r ≈ r , g  ), addStep(B, trans, (s ≈ r, r ≈ r ), ())



the proof generator most relevant to the core calculus, the term-conversion proof
generator, targeted for substitution and rewriting proofs.


4    Proof Reconstruction for Substitution and Rewriting

Once it determines that the input formulas ϕ1 , . . . , ϕn are jointly unsatisﬁable,
the SMT solver has a reference to a proof node P that concludes ⊥ from the
free assumptions ϕ1 , . . . , ϕn . After the post-processor is run, the (closed) proof
(scope, P  , (ϕ1 , . . . , ϕn )) is then generated as the ﬁnal proof for the user, where
P  is the result of optionally expanding coarse-grained steps (in particular, appli-
cations of the rule sr) in P into ﬁne-grained ones. To do so, we require the
following algorithm for generating term-conversion proofs.
     In particular, we focus on equalities t ≈ s whose proof can be justiﬁed by
a set of steps that replace subterms of t until it is syntactically equal to s. We
assume these steps are provided to a term-conversion proof generator. Formally,
a term-conversion proof generator g is a pair of sets cpre and cpost . The set cpre
(resp., cpost ) contains pairs of the form (t ≈ s, gt,s ) indicating that t should
be replaced by s in a preorder (resp., postorder) traversal of the terms that g
processes, where gt,s is a proof generator that can prove the equality t ≈ s. We
require that neither cpre nor cpost contain multiple entries of the form (t ≈ s1 , g1 )
and (t ≈ s2 , g2 ) for distinct (s1 , g1 ) and (s2 , g2 ).
     The procedure for generating proofs from a term-conversion proof generator
g is given in Algorithm 1. When asked to prove an equality t1 ≈ t2 , getProof
traverses the structure of t1 and applies steps from the sets cpre and cpost from g.
              Flexible Proof Production in an Industrial-Strength SMT Solver             23

The traversal is performed by the auxiliary procedure getTermConv which relies
on two data structures. The ﬁrst is a lazy proof builder B that stores the inter-
mediate steps in the overall proof of t1 ≈ t2 . The proof builder is given these
steps either via addStep, as a concrete triple with the proof rule, a list of premise
formulas, and a list of argument terms, or as a lazy step via addLazyStep, with a
formula and a reference to another generator that can prove that formula. The
second data structure is a mapping R from terms to terms that is updated (using
array syntax in the pseudo-code) as the converted form of terms is computed
by getTermConv. For any term s, executing getTermConv(s, cpre , cpost , B, R) will
result in R[s] containing the converted form of s according to the rewrites in cpre
and cpost , and B storing a proof step for s ≈ R[s]. Thus, the procedure getProof
succeeds when, after invoking getTermConv(t1 , cpre , cpost , B, R) with B and R ini-
tially empty, the mapping R contains t2 as the converted form of t1 . The proof
for the equality t1 ≈ R[t1 ] can then be constructed by calling getProof on the
lazy proof builder B, based on the (lazy) steps stored in it.
    Each subterm s of t1 is traversed only once by getTermConv by checking
whether R already contains the converted form of s. When that is not the case,
s is ﬁrst preorder processed. If cpre contains an entry indicating that s rewrites
to s , this rewrite step is added to the lazy proof builder and the converted form
R[s] of s is set to s . Otherwise, the immediate subterms of s, if any, are traversed
and then s is postorder processed. The converted form of s is set to some term
r of the form f (R[s1 ], . . . , R[sn ]), considering how its immediate subterms were
converted. Note that B will contain steps for s ≈ R[s ]. Thus, the equality s ≈ r
can be proven by congruence for function f with these premises if s = r, and by
reﬂexivity otherwise. Furthermore, if cpost indicates that r rewrites to r , then
this step is added to the lazy proof builder; a transitivity step is added to prove
s ≈ r from t ≈ r and r ≈ r ; and the converted form R[s] is set to r .

Example 1. Consider the equality t ≈ ⊥, where t = f (b)+f (a) < f (a−0)+f (b),
and suppose the conversion of t is justiﬁed by a term-conversion proof generator
g containing the sets cpre = {(f (b) + f (a) ≈ f (a) + f (b), g AC ), (a − 0 ≈ a, g0Arith )}
and cpost = {(f (a) + f (b) < f (a) + f (b) ≈ ⊥, g1Arith )}. The generator g AC provides
a proof based on associative and commutative reasoning, whereas g0Arith and
g1Arith provide proofs based on arithmetic reasoning. Invoking getProof(g, t ≈ ⊥)
initiates the traversal with getTermConv(t, cpre , cpost , ∅, ∅). Since t is not in the
conversion map, it is preorder processed. However, as it does not occur in cpre ,
nothing is done and its subterms are traversed. The subterm f (b) + f (a) is
equated to f (a) + f (b) in cpre , justiﬁed by g AC . Therefore R is updated with
R[f (b) + f (a)] = f (a) + f (b) and the respective lazy step is added to B. The
subterms of f (b)+f (a) are not traversed, therefore the next term to be traversed
is f (a−0)+f (b). Since it does not occur in cpre , its subterm f (a−0) is traversed,
which analogously leads to the traversal of a−0. As a−0 does occur in cpre , both R
and B are updated accordingly and the processing of its parent f (a−0) resumes.
A congruence step added to B justiﬁes its conversion to f (a) being added to R.
24           H. Barbosa et al.

No more additions happen since f (a) does not occur in cpost . Analogously, R and
B are updated with f (b) not changing and f (a − 0) + f (b) being converted into
f (a) + f (b). Finally, the processing returns to the initial term t, which has been
converted to R[f (b) + f (a)] < R[f (a + 0) + f (b)], i.e., f (a) + f (b) < f (a) + f (b).
Since this term is equated to ⊥ in cpost , justiﬁed by g1Arith , the respective lazy
step is added to B, as well as a transitivity step to connect f (b) + f (a) <
f (a − 0) + f (b) ≈ f (a) + f (b) < f (a) + f (b) and f (a) + f (b) < f (a) + f (b) ≈ ⊥.
At this point, the execution terminates with R[f (b)+f (a) < f (a+0)+f (b)] = ⊥,
as expected. A proof for t ≈ ⊥ with the following structure can then be extracted
from B:
                                                AC
                                            g
                       Lazy
                              f (b) + f (a) ≈ f (a) + f (b)   P1 |   <                          | f (b) ≈ f (b)
P0 : cong                                                                          P2 : refl
               f (b) + f (a) < f (a − 0) + f (b) ≈ f (a) + f (b) < f (a) + f (b)                f (b) ≈ f (b)
                                                                                       Arith
                                                                                      g0
                                    Arith                                   Lazy
                                   g1                                              a−0≈a | f
              Lazy                                                   cong
        P0           f (a) + f (b) < f (a) + f (b) ≈ ⊥                         f (a − 0) ≈ f (a)      P2 | +
trans                                                    P1 : cong
             f (b) + f (a) < f (a − 0) + f (b) ≈ ⊥                        f (a − 0) + f (b) ≈ f (a) + f (b)


    We use several extensions to the procedures in Algorithm 1. Notice that this
procedure follows the policy that terms on the right-hand side of conversion
steps (equalities from cpre and cpost ) are not traversed further. The procedure
getTermConv is used by term-conversion proof generators that have the rewrite-
once policy. A similar procedure which additionally traverses those terms is used
by term-conversion proof generators that have a rewrite-to-fixpoint policy.
    We now show how the term-conversion proof generator can be used for recon-
structing ﬁne-grained proofs from coarse-grained ones. In particular we focus on
                                    (S, R, D, ψ)). Recall from Fig. 2 that the
proofs Pψ1 of the form (sr, (Qψ0 , Q),
proof rule sr concludes a formula ψ that can be shown equivalent to the for-
mula ψ0 proven by Qψ0 based on a substitution derived from the conclusions of
            A proof like Pψ above can be transformed to one that involves
the nodes Q.                   1
(atomic) theory rewrites and equality rules only. We show this transformation
in two phases. In the ﬁrst phase, the proof is expanded to:

                           (eq res, (Qψ0 , (trans, (R0 , (symm, R1 )))))
                           ϕ , (S, D, ψi )), (rewrite, (), (R, S(ψi , D(
with Ri = (trans, ((subs, Q                                                  ϕ)))))) for i ∈
{0, 1} where ϕ
              are the conclusions of Q   ϕ , and subs and rewrite are auxiliary proof
rules used for further expansion in the second phase. We describe them next.
Substitution Steps. Let Pt≈s be the subproof (subs, Q         ϕ , (S, D, t)) of Ri above
proving t ≈ s with s = S(ψi , D(    ϕ)) and D(   ϕ) = (t1 → s1 , . . . , tn → sn ). Sub-
stitution steps can be expanded to ﬁne-grained proofs using a term-conversion
proof generator. First, for each j = 1, . . . , n, we construct a proof of tj ≈ sj ,
which involves simple transformations on the proofs of ϕ           . Suppose we store all
of these in an eager proof generator g. If S is a simultaneous or ﬁxed-point
substitution, we then build a single term-conversion proof generator C, which
             Flexible Proof Production in an Industrial-Strength SMT Solver            25

recall is modeled as a pair of mappings (cpre , cpost ). We add (tj ≈ sj , g) to cpre
for all j. We use the rewrite-once policy for C if S is a simultaneous substi-
tution, and the rewrite-ﬁxed-point policy for C otherwise. We then replace the
proof Pt≈s by getProof(C, t ≈ s), which runs the procedure in Algorithm 1.
Otherwise, if S is a sequential substitution, we construct a term-conversion
generator Cj for each j, initializing it so that its cpre set contains the single
rewrite step (tj ≈ sj , g) and uses a rewrite-once policy. We then replace the
proof Pt≈s by (trans, (P1 , . . . , Pn )) where, for j = 1, . . . , n: Pj is generated by
getProof(Cj , sj−1 ≈ sj ); s0 = t; si is the result of the substitution D(       ϕ) after
the ﬁrst i steps; and sn = s.
Rewrite Steps. Let P be the proof node (rewrite, (), (R, t)), which proves the
equality t ≈ t↑↓R . During reconstruction, we replace P with a proof involving
only ﬁne-grained rules, depending on the rewrite method R. For example, if
R is the core rewriter, we run the rewriter again on t in proof tracking mode.
Normally, the core rewriter performs a term traversal and applies atomic rewrites
to completion. In proof tracking mode, it also return two lists, for pre- and post-
rewrites, of steps (t1 ≈ s1 , g), . . . , (tn ≈ sn , g) where g is a proof generator that
returns (atom rewrite, (), (R, ti )) for all equalities ti ≈ si . Furthermore, for each
Skolem k that is a subterm of t, we construct the rewrite steps (k ≈ k↑, g  ) where
g  is a proof generator that returns (witness, (), (k)) for equalities k ≈ k↑. We
add these rewrite proof steps to a term-conversion generator C with rewrite-
ﬁxed-point policy, and replace P by getProof(C, t ≈ t↑↓R ).


5     SMT Proofs

Here we brieﬂy describe each component shown in Sect. 2 and how it produces
proofs with the infrastructure from Sects. 3 and 3.2.


5.1   Preprocessing Proofs

The pre-processor transforms an input formula ϕ into a list of formulas to be
given to the core solver. It applies a sequence of preprocessing passes. A pass
may replace a formula ϕi with another one φi , in which case it is responsible for
providing a proof of ϕi ≈ φi . It may also append a new formula φ to the list,
in which case it is responsible for providing a proof for it. We use a (lazy) proof
generator that tracks these proofs, maintaining the invariant that a proof can be
provided for all (preprocessed) formulas when requested. We have instrumented
proof production for the most common preprocessing passes, relying heavily on
the sr rule to model transformations such as expansion of function deﬁnitions
and, with witness forms, Skolemization and if-then-else elimination [6].
Simplification Under Global Assumptions. cvc5 aggressively learns literals that
hold globally by performing Boolean constraint propagation over the input for-
mula. When a learned literal corresponds to a variable elimination (e.g., x ≈ 5
corresponds to x → 5) or a constant propagation (e.g., P (x) corresponds to
26      H. Barbosa et al.

P (x) → ), we apply the corresponding (term) substitution to the input. This
application is justiﬁed via sr, while the derivation of the globally learned literals
is justiﬁed via clausiﬁcation and resolution proofs, as explained in Sect. 5.3.
    The key features of our architecture that make it feasible to produce proofs
for this simpliﬁcation are the automatic reconstruction of sr steps and the abil-
ity to customize the strategy for substitution application during reconstruction,
as detailed in Sect. 3.2. When a new variable elimination x → t is learned, old
ones need to be normalized to eliminate any occurrences of x in their right-hand
sides. Computing the appropriate simultaneous substitution for all eliminations
requires quadratically many traversals over those terms. We have observed that
the size of substitutions generated by this preprocessing pass can be very large
(with thousands of entries), which makes this computation prohibitively expen-
sive. Using the ﬁxed-point strategy, however, the reconstruction for the sr steps
can apply the substitution eﬃciently and its complexity depends on how many
applications are necessary to reach a ﬁx-point, which is often low in practice.

5.2   Theory Proofs

The theory engine produces lemmas, as disjunctions of literals, from an indi-
vidual theory or a combination of them. In the ﬁrst case, the lemma’s proof is
provided directly by the corresponding theory solver. In the second case, a the-
ory solver may produce a lemma ψ containing a literal derived by some other
theory solver from literals . A lemma over the combined theory is generated by
replacing in ψ by . This regression process, which is similar to the computa-
tion of explanations during solving, is repeated until the lemma contains only
input literals. The proof of the ﬁnal lemma then uses rules like sr to combine the
proofs of the intermediate literals derived locally in various theories and their
replacement by input literals in the ﬁnal lemma.
Equality and Uninterpreted Function (EUF) Proofs. The EUF solver can be
easily instrumented to produce proofs [31,42] with equality rules (see Fig. 2).
In cvc5, term equivalences are also derived via rewriting in some other theory
T : when a function from T has all of its arguments inferred to be congruent to
T -values, it may be rewritten into a T -value itself, and this equivalence asserted.
Such equivalences are justiﬁed via sr steps. Since generating equality proofs
incurs minimal overhead [42] and rewriting proofs are reconstructed lazily, EUF
proofs are generated during solving and stored in an eager proof generator.
Extensional Arrays and Datatypes Proofs. While these two theories diﬀer sig-
niﬁcantly, they both combine equality reasoning with rules for handling their
particular operators. For arrays, these are rules for select, store, and array exten-
sionality (see [36, Sec. 5]). For datatypes, they are rules reﬂecting the properties
of constructors and selectors, as well as acyclicity. The justiﬁcations for lemmas
are also generated eagerly and stored in an eager proof generator.
Bit-Vector Proofs. The bit-vector solver applies bit-blasting to reduce bit-vector
problems to equisatisﬁable propositional problems. Thus, its lemmas amount
            Flexible Proof Production in an Industrial-Strength SMT Solver      27

to the rewriting of the bit-vector literals into Boolean formulas, which will be
solved and proved by the propositional engine. The bit-vector lemmas are proven
lazily, analogous to sr steps, with the diﬀerence that the reconstruction uses the
bit-blaster in the bit-vector solver instead of the rewriter.
Arithmetic Proofs. The linear arithmetic solver is based on the simplex algo-
rithm [24], and each of its lemmas is the negation of an unsatisﬁable conjunction
of inequalities. Farkas’ lemma [30,49] guarantees that there exists a linear com-
bination of these inequalities equivalent to ⊥. The coeﬃcients of the combination
are computed during solving with minimal overhead [38], and the equivalence
is proven with an sr step. To allow the rewriter to prove this equivalence, the
bounds of the inequalities are scaled by constants and summed during recon-
struction. Integer reasoning is proved through rules for branching and integer
bound tightening, recorded eagerly.
    Non-linear arithmetic lemmas are generated from incremental linearization
[16] or cylindrical algebraic coverings [1]. The former can be proven via propo-
sitional and basic arithmetic rules, with only a few, such as the tangent plane
lemma, needing a dedicated proof rule. The latter requires two complex rules
that are not inherently simpler than solving, albeit not as complex as those for
regular CAD-based theory solvers [2]. We point out that checking these rules
would require a signiﬁcant portion of CAD-related theory, whose proper formal-
ization is still an open, if actively researched, problem [18,25,34,41,53].
Quantifier Proofs. Quantiﬁed formulas not Skolemized during pre-processing are
handled via instantiation, which produces theory lemmas of the form (∀x ϕ) ⇒
ϕσ, where σ is a grounding substitution. An instantiation rule proves them
independently of how the substitution was actually derived, since any well-typed
one suﬃces for soundness.
String Proofs. The strings solver applies a layered approach, distinguishing
between core [40] and extended operators [48]. The core operators consist of
(dis)equalities between string concatenations and length constraints. Reasoning
over them is proved by a combination of equality and linear integer arithmetic
proofs, as well as speciﬁc string rules. The extended operators are reduced to core
ones via formulas with bounded quantiﬁers. The reductions are proven with rules
deﬁning each extended function’s semantics, and sr steps justifying the reduc-
tions. Finally, regular membership constraints are handled by string rules that
unfold occurrences of the Kleene star operator and split up regular expression
concatenations into diﬀerent parts. Overall, the proofs for the strings theory
solver encompass not only string-speciﬁc reasoning but also equality, linear inte-
ger arithmetic, and quantiﬁer reasoning, as well as substitution and rewriting.
Unsupported. The theory solvers for the theories of ﬂoating-point arithmetic,
sequences, sets and relations, and separation logic are currently not proof-
producing in cvc5. These are relatively new or non-standard theories in SMT
and have not been our focus, but we intend to produce proofs for them in the
future.
28      H. Barbosa et al.

Table 1. Cumulative solving times (s) on benchmarks solved by all conﬁgurations,
with the slowdown versus cvc+s in parentheses.

         Logics             # cvc+os cvc+s          cvc+sp      cvc+spr
         non-BVs 116,321         164k    166k   284k (1.7×) 299k (1.8×)
         BVs      29,192          45k     57k   150k (2.6×) 224k (3.9×)



5.3   Propositional Proofs

Propositional proofs justify both the conversion of preprocessed input formulas
and theory lemmas into conjunctive normal form (CNF) and the derivation of
⊥ from the resulting clauses. CNF proofs are a combination of Boolean trans-
formations and introductions of Boolean formulas representing the deﬁnition of
Tseytin variables, used to ensure that the CNF conversion is polynomial. The
clausiﬁer uses a lazy proof builder which stores the clausiﬁcation steps eagerly,
with the preprocessed input formulas as assumptions, and the theory lemmas as
lazy steps, with associated proof generators.
    For Boolean reasoning, cvc5 uses a version of MiniSat [27] instrumented to
produce resolution proofs. It uses a lazy proof builder to record resolution steps
for learned clauses as they are derived (see [7, Chap 1] for more details) and to
lazily build a refutation with only the resolution steps necessary for deriving ⊥.
The resolution rule, however, is ground ﬁrst-order resolution, since the proofs are
in terms of the ﬁrst-order clauses rather than their propositional abstractions.


6     Evaluation

In this section, we discuss an initial evaluation of our implementation in cvc5 of
the proof-production architecture presented in this paper. In the following, we
denote diﬀerent conﬁgurations of cvc5 by cvc plus some suﬃxes. A conﬁguration
using variable and clause elimination in the SAT solver [26], symmetry break-
ing [23] in the EUF solver, and black-box SAT solving in the bit-vector (BV)
solver, is denoted by the suﬃx o. These techniques are currently incompatible
with the proof production architecture. Other cvc5 techniques for which we do
not yet support ﬁne-grained proofs, however, are active and have their inferences
registered in the proofs as trusted steps. A conﬁguration that includes simpli-
ﬁcation under global assumptions is denoted by s; one that includes producing
proofs by p; and one that additionally reconstructs proofs by r. The default
conﬁguration of cvc5 is cvc+os.
    We split our evaluation into measuring the proof-production cost as well
as the performance impact of making key techniques proof-producing; the proof
reconstruction overhead; and the coverage of the proof production. We also com-
ment on how cvc5’s proofs compare with CVC4’s proofs. Note that the internal
proof checking described in Sect. 3, which was invaluable for a correct implemen-
tation, is disabled for evaluating performance. Experiments ran on a cluster with
                                   Flexible Proof Production in an Industrial-Strength SMT Solver                                                                                                           29

                              cvc+os
                                                                                                                                      cvc+os (BV)
                              cvc+s
                                                                                                                                      cvc+s (BV)
                              cvc
                  102                                                                                                   102           cvc (BV)
                              cvc+pr
                                                                                                                                      cvc+pr (BV)
                              cvc+spr
                                                                                                                                      cvc+spr (BV)
                              cvc+sp
    runtime [s]




                                                                                                          runtime [s]
                                                                                                                                      cvc+sp (BV)



                  101                                                                                                   101




                  100                                                                                                   100
                   100000        105000         110000                     115000     120000                             20000 22500 25000 27500 30000 32500 35000 37500
                                           solved instances                                                                                          solved instances
                                                                a                                                                                                             b

                                                                                                                              10x                                                   10x
              102                                                    102                                            102       100x                                            102   100x
                                                                                                                              1000x                                                 1000x
                                                  cvc+spr (BV) [s]




                                                                                                                                                           cvc+spr (BV) [s]
cvc+spr [s]




                                                                                                      cvc+spr [s]
              101                                                    101                                            101                                                       101



              100                                                    100                                            100                                                       100
                                          10x                                                 10x
                                          100x                                                100x
                                          1000x                                               1000x
       10−1 −1                                              10−1 −1                                          10−1 −1                                                 10−1 −1
          10            100        101    102                  10            100    101       102               10             100        101        102                10           100    101       102
                              cvc+s [s]                                      cvc+s (BV) [s]                                       cvc+sp [s]                                        cvc+sp (BV) [s]

                                                                c                                                                                                             d

Fig. 3. (a) Cactus plot for non-BVs (b) Cactus plot for BVs (c) Scatter plot of overall
proof cost (d) Reconstruction cost


Intel Xeon E5-2620 v4 CPUs, with 300s and 8GB of RAM for each solver and
benchmark pair. We consider 162,060 unsatisﬁable problems from SMT-LIB [8],
across all logics except those with ﬂoating point arithmetic, as determined by
cvc5 [5, Sec. 4]. We split them into 38,732 problems with the BV theory (the
BVs set) and 123,328 problems without (the non-BVs set).
Proof Production Cost. The cost of proof production is summarized in Table 1
and Figs. 3a to 3d. The impact of running without o is negligible overall in non-
BVs, but steep for BVs, both in terms of solving time and number of problems
solved, as evidenced by the table and Fig. 3b respectively. This is expected given
the eﬀectiveness of combining bit-blasting with black-box SAT solvers. The over-
head of p is similar for both sets, although more pronounced in BVs. While the
total time is around double that of cvc+s, Fig. 3c shows a ﬁner distribution,
with most problems having a less signiﬁcant overhead. Moreover, the total num-
ber of problems solved is quite similar, as shown in Figs. 3a and 3b, particularly
for non-BVs. The diﬀerence in overhead due to p between the BVs and non-
BVs sets can be attributed to the cost of managing large proofs, which are
more common in BVs. This stems from the well-known blow-up in problem size
incurred by bit-blasting, which is reﬂected in the proofs.
    The cost of generating ﬁne-grained steps for the sr rule and for the similarly
reconstructed theory-speciﬁc steps mentioned in Sect. 5, varies again between
30      H. Barbosa et al.

the two sets, but more starkly. While for non-BVs the overall solving time and
number of problems solved are very similar between cvc+sp and cvc+spr, for
the BVs set cvc+spr is signiﬁcantly slower overall. This diﬀerence again arises
mainly because of the increased proof sizes. Nevertheless, r leads to only a small
increase in unsolved problems in BVs, as shown in Fig. 3b.
    The importance of being able to produce proofs for simpliﬁcation under
global assumptions is made clear by Fig. 3a: the impact of disabling s is virtu-
ally the same as that of adding p; moreover, cvc+spr signiﬁcantly outperforms
cvc+pr. In Fig. 3b the diﬀerence is less pronounced but still noticeable.
Proofs Coverage. When using techniques that are not yet fully proof-producing,
but still active, cvc5 inserts trusted steps in the proof. These are usually steps
whose checking is not inherently simpler than solving. They eﬀectively represent
holes in the proof, but are still useful for users who avail themselves of powerful
proof-checking techniques. Trusted steps are commonly used when integrating
SMT solvers into proof assistants [11,28,51].
    The percentage of cvc+spr proofs without trusted steps is 92% for BVs and
80% for non-BVs. That is to say, out of 145,683 proofs, 120,473 of them are
fully ﬁne-grained proofs. The vast majority of the trusted steps in the remaining
proofs are due to theory-speciﬁc preprocessing passes that are not yet fully proof-
producing. In non-BVs, the occurrence of trusted steps is heavily dependent
on the speciﬁc SMT-LIB logic, as expected. Common oﬀenders are logics with
datatypes, with trusted steps for acyclicity checks, and quantiﬁed logics, with
trusted steps for certain α-equivalence eliminations. In non-linear real arithmetic
logics, all cylindrical algebraic coverings proofs are built with trusted steps (see
Sect. 5.2), but we note this is the state of the art for CAD-based proofs. As for
non-linear integer arithmetic logics, our proof support is still in its early stages,
so a signiﬁcant portion of their theory lemmas are trusted steps.
    We stress the extent of our coverage for string proofs, which were previously
unsupported by any SMT solver. In the string logics without length constraints,
100% of the proofs are fully ﬁne-grained. This rate goes down to 80% in the
logics with length. For the remaining 20%, the overwhelming majority of the
trusted steps are for theory-speciﬁc preprocessing or some particular string or
linear arithmetic inference within the proof of a theory lemma.
Comparison with CVC4 Proofs. We compare the proof coverage of cvc5 versus
CVC4. The cvc5 proof production replaces CVC4’s [32,36], which was incom-
plete and monolithic. CVC4 did not produce proofs at all for strings, substitu-
tions, rewriting, preprocessing, quantiﬁers, datatypes, or non-linear arithmetic.
In particular, simpliﬁcation over global assumptions had to be disabled when
producing proofs. In fragments supported by both systems, CVC4’s proofs are
at most as detailed as cvc5’s. The only superior aspect of CVC4’s proof produc-
tion was to support proofs from external SAT solvers [45] used in the BV solver,
which are very signiﬁcant for solving performance, as shown above. Integrating
this feature into cvc5 is left as future work, but we note that there is no limi-
tation in the proof architecture that would prevent it. We also point out that
cvc5 produces resolution proofs for the bit-blasted BV constraints, which can
            Flexible Proof Production in an Industrial-Strength SMT Solver      31

be checked in polynomial time, whereas external SAT solvers produce DRAT
proofs [33] (or reconstructions of them via other tools [19,20,37,39]), which can
take exponential time to check. So there is a signiﬁcant trade-oﬀ to be considered.


7   Related Work
Two signiﬁcant proof-producing state-of-the-art SMT solvers are z3 [22] and
veriT [14]. Both can have their proofs successfully reconstructed in proof assis-
tants [3,12,13,51]. They can produce detailed proofs for the propositional and
theory reasoning in EUF and linear arithmetic, as well as for quantiﬁers. How-
ever, z3’s proofs are coarse-grained for preprocessing and rewriting, and for bit-
vector reasoning, which complicates proof checking. Moreover, to the best of our
knowledge, z3 does not produce proofs for its other theories. In contrast, veriT
can produce ﬁne-grained proofs for preprocessing and rewriting [6], which has led
to a better integration with Isabelle/HOL [51]. However, it does so eagerly, which
requires a tight integration between the preprocessing and the proof-production
code. In addition, it does not support simpliﬁcation under global assumptions
when producing proofs, which signiﬁcantly impacts its performance. Other proof-
producing SMT solvers are MathSAT5 [17] and SMTInterpol [15]. They produce
resolution proofs and theory proofs for EUF, linear arithmetic, and, in SMTIn-
terpol’s case, array theories. Their proofs are tailored towards unsatisﬁable core
and interpolant generation, rather than external certiﬁcation. Moreover, they do
not seem to provide proofs for preprocessing, clausiﬁcation or rewriting.
    While cvc5 is possibly the only proof-producing solver for the full theory of
strings, CertiStr [35] is a certiﬁed solver for the fragment with concatenation
and regular expressions. It is automatically generated from Isabelle/HOL [44]
but is signiﬁcantly less performant than cvc5, although a proper comparison
would need to account for proof-checking time in cvc5’s case.


8   Conclusion and Future Work
We presented and evaluated a ﬂexible proof production architecture, showing it
is capable of producing proofs with varying levels of granularity in a scalable
manner for a state-of-the-art and industrial-strength SMT solver like cvc5.
    Since currently, there is no standard proof format for SMT solvers, our archi-
tecture is designed to support multiple proof formats via a ﬁnal post-processing
transformation to convert internal proofs accordingly. We are developing back-
ends for the LFSC [52] proof checker and the proof assistants Lean 4 [21],
Isabelle/HOL [44], and Coq [10], the latter two via the Alethe proof format [50].
Since using these tools requires mechanizing the respective target proof calculi in
their languages, besides external checking, another beneﬁt is to decouple conﬁ-
dence on the soundness of the proof calculi from the internal cvc5 proof calculus.
    A considerable challenge for SMT proofs is the plethora of rewrite rules used
by the solvers, which are speciﬁc for each theory and vary in complexity. In
32      H. Barbosa et al.

particular, string rewrites can be very involved [46] and hard to check. We are
also developing an SMT-LIB-based DSL for specifying rewrite rules, to be used
during proof reconstruction to decompose rewrite steps in terms of them, thus
providing more ﬁne-grained proofs for rewriting.
    Finally, we plan to incorporate into the proof-production architecture the
unsupported theories and features mentioned in Sects. 5.2 and 6, particularly
those relevant for solving performance that currently either leave holes in proofs,
such as theory pre-processing or non-linear arithmetic reasoning, or that have
to be disabled, such as the use of external SAT solvers in the BV theory.

References
 1. Ábrahám, E., Davenport, J.H., England, M., Kremer, G.: Deciding the consistency
    of non-linear real arithmetic constraints with a conﬂict driven search using cylin-
    drical algebraic coverings. J. Log. Algebr. Methods Program. 119, 100633 (2021)
 2. Abrahám, E., Davenport, J.H., England, M., Kremer, G.: Proving UNSAT
    in SMT: the case of quantiﬁer free non-linear real arithmetic. arXiv preprint
    arXiv:2108.05320 (2021)
 3. Armand, M., Faure, G., Grégoire, B., Keller, C., Théry, L., Werner, B.: A modular
    integration of SAT/SMT solvers to coq through proof witnesses. In: Jouannaud, J.-
    P., Shao, Z. (eds.) CPP 2011. LNCS, vol. 7086, pp. 135–150. Springer, Heidelberg
    (2011). https://doi.org/10.1007/978-3-642-25379-9 12
 4. Backes, J., et al.: Semantic-based automated reasoning for AWS access policies
    using SMT. In: Bjørner, N., Gurﬁnkel, A. (eds.) Formal Methods in Computer-
    Aided Design (FMCAD), pp. 1–9. IEEE (2018)
 5. Barbosa, H., et al.: cvc5: a versatile and industrial-strength SMT solver. In: Fis-
    man, D., Rosu, G. (eds.) Tools and Algorithms for Construction and Analysis of
    Systems (TACAS). LNCS, Springer, Cham (2022). https://doi.org/10.1007/978-
    3-030-99524-9 24
 6. Barbosa, H., Blanchette, J.C., Fleury, M., Fontaine, P.: Scalable ﬁne-grained proofs
    for formula processing. J. Autom. Reason. 64(3), 485–510 (2020)
 7. Barrett, C., de Moura, L., Fontaine, P.: Proofs in satisﬁability modulo theories.
    All About Proofs Proofs All (APPA) 55(1), 23–44 (2014)
 8. Barrett, C., Fontaine, P., Tinelli, C.: The SMT-LIB standard: version 2.6. Technical
    report, Department of Computer Science, The University of Iowa (2017). www.
    SMT-LIB.org
 9. Barrett, C., Tinelli, C.: Satisﬁability Modulo Theories. In: Clarke, E., Henzinger,
    T., Veith, H., Bloem, R. (eds.) Handbook of Model Checking, pp. 305–343.
    Springer, Cham (2018). https://doi.org/10.1007/978-3-319-10575-8 11
10. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program Development -
    Coq’Art: The Calculus of Inductive Constructions. Texts in Theoretical Computer
    Science. An EATCS Series, Springer, Heidelberg (2004). https://doi.org/10.1007/
    978-3-662-07964-5
11. Blanchette, J.C., Böhme, S., Paulson, L.C.: Extending sledgehammer with SMT
    solvers. J. Autom. Reason. 51(1), 109–128 (2013)
12. Böhme, S., Fox, A.C.J., Sewell, T., Weber, T.: Reconstruction of Z3’s bit-vector
    proofs in HOL4 and Isabelle/HOL. In: Jouannaud, J.-P., Shao, Z. (eds.) CPP
    2011. LNCS, vol. 7086, pp. 183–198. Springer, Heidelberg (2011). https://doi.org/
    10.1007/978-3-642-25379-9 15
             Flexible Proof Production in an Industrial-Strength SMT Solver         33

13. Böhme, S., Weber, T.: Fast LCF-style proof reconstruction for Z3. In: Kaufmann,
    M., Paulson, L.C. (eds.) ITP 2010. LNCS, vol. 6172, pp. 179–194. Springer, Hei-
    delberg (2010). https://doi.org/10.1007/978-3-642-14052-5 14
14. Bouton, T., Caminha B. de Oliveira, D., Déharbe, D., Fontaine, P.: veriT: an open,
    trustable and eﬃcient SMT-solver. In: Schmidt, R.A. (ed.) CADE 2009. LNCS
    (LNAI), vol. 5663, pp. 151–156. Springer, Heidelberg (2009). https://doi.org/10.
    1007/978-3-642-02959-2 12
15. Christ, J., Hoenicke, J., Nutz, A.: SMTInterpol: an interpolating SMT solver.
    In: Donaldson, A., Parker, D. (eds.) SPIN 2012. LNCS, vol. 7385, pp. 248–254.
    Springer, Heidelberg (2012). https://doi.org/10.1007/978-3-642-31759-0 19
16. Cimatti, A., Griggio, A., Irfan, A., Roveri, M., Sebastiani, R.: Satisﬁability mod-
    ulo transcendental functions via incremental linearization. In: de Moura, L. (ed.)
    CADE 2017. LNCS (LNAI), vol. 10395, pp. 95–113. Springer, Cham (2017).
    https://doi.org/10.1007/978-3-319-63046-5 7
17. Cimatti, A., Griggio, A., Schaafsma, B.J., Sebastiani, R.: The MathSAT5 SMT
    solver. In: Piterman, N., Smolka, S.A. (eds.) TACAS 2013. LNCS, vol. 7795, pp.
    93–107. Springer, Heidelberg (2013). https://doi.org/10.1007/978-3-642-36742-7 7
18. Cohen, C.: Construction of real algebraic numbers in Coq. In: Beringer, L., Felty,
    A. (eds.) ITP 2012. LNCS, vol. 7406, pp. 67–82. Springer, Heidelberg (2012).
    https://doi.org/10.1007/978-3-642-32347-8 6
19. Cruz-Filipe, L., Heule, M.J.H., Hunt, W.A., Kaufmann, M., Schneider-Kamp, P.:
    Eﬃcient certiﬁed RAT veriﬁcation. In: de Moura, L. (ed.) CADE 2017. LNCS
    (LNAI), vol. 10395, pp. 220–236. Springer, Cham (2017). https://doi.org/10.1007/
    978-3-319-63046-5 14
20. Cruz-Filipe, L., Marques-Silva, J., Schneider-Kamp, P.: Eﬃcient certiﬁed resolu-
    tion proof checking. In: Legay, A., Margaria, T. (eds.) TACAS 2017. LNCS, vol.
    10205, pp. 118–135. Springer, Heidelberg (2017). https://doi.org/10.1007/978-3-
    662-54577-5 7
21. de Moura, L., Ullrich, S.: The lean 4 theorem prover and programming language.
    In: Platzer, A., Sutcliﬀe, G. (eds.) CADE 2021. LNCS (LNAI), vol. 12699, pp.
    625–635. Springer, Cham (2021). https://doi.org/10.1007/978-3-030-79876-5 37
22. de Moura, L.M., Bjørner, N.: Proofs and refutations, and Z3. In: Rudnicki, P.,
    Sutcliﬀe, G., Konev, B., Schmidt, R.A., Schulz, S. (eds.) Logic for Programming,
    Artiﬁcial Intelligence, and Reasoning (LPAR) Workshops. CEUR Workshop Pro-
    ceedings, vol. 418. CEUR-WS.org (2008)
23. Déharbe, D., Fontaine, P., Merz, S., Woltzenlogel Paleo, B.: Exploiting symmetry
    in SMT problems. In: Bjørner, N., Sofronie-Stokkermans, V. (eds.) CADE 2011.
    LNCS (LNAI), vol. 6803, pp. 222–236. Springer, Heidelberg (2011). https://doi.
    org/10.1007/978-3-642-22438-6 18
24. Dutertre, B., de Moura, L.: A fast linear-arithmetic solver for DPLL(T). In: Ball,
    T., Jones, R.B. (eds.) CAV 2006. LNCS, vol. 4144, pp. 81–94. Springer, Heidelberg
    (2006). https://doi.org/10.1007/11817963 11
25. Eberl, M.: A decision procedure for univariate real polynomials in Isabelle/HOL.
    In: Proceedings of the 2015 Conference on Certiﬁed Programs and Proofs, CPP
    2015, pp. 75–83. Association for Computing Machinery, New York (2015)
26. Eén, N., Biere, A.: Eﬀective preprocessing in SAT through variable and clause
    elimination. In: Bacchus, F., Walsh, T. (eds.) SAT 2005. LNCS, vol. 3569, pp.
    61–75. Springer, Heidelberg (2005). https://doi.org/10.1007/11499107 5
27. Eén, N., Sörensson, N.: An extensible SAT-solver. In: Giunchiglia, E., Tacchella,
    A. (eds.) SAT 2003. LNCS, vol. 2919, pp. 502–518. Springer, Heidelberg (2004).
    https://doi.org/10.1007/978-3-540-24605-3 37
34      H. Barbosa et al.

28. Ekici, B., et al.: SMTCoq: a plug-in for integrating SMT solvers into Coq. In:
    Majumdar, R., Kunčak, V. (eds.) CAV 2017. LNCS, vol. 10427, pp. 126–133.
    Springer, Cham (2017). https://doi.org/10.1007/978-3-319-63390-9 7
29. Enderton, H.B.: A Mathematical Introduction to Logic, 2nd edn. Academic Press,
    Cambridge (2001)
30. Farkas, G.: A Fourier-féle mechanikai elv alkamazásai. Mathematikaiés
    Természettudományi Értesı́tö 12, 457–472 (1894). Reference from Schrijver’s Com-
    binatorial Optimization textbook (Hungarian)
31. Fontaine, P., Marion, J.-Y., Merz, S., Nieto, L.P., Tiu, A.: Expressiveness +
    automation + soundness: towards combining SMT solvers and interactive proof
    assistants. In: Hermanns, H., Palsberg, J. (eds.) TACAS 2006. LNCS, vol. 3920,
    pp. 167–181. Springer, Heidelberg (2006). https://doi.org/10.1007/11691372 11
32. Hadarean, L., Barrett, C., Reynolds, A., Tinelli, C., Deters, M.: Fine grained SMT
    proofs for the theory of ﬁxed-width bit-vectors. In: Davis, M., Fehnker, A., McIver,
    A., Voronkov, A. (eds.) LPAR 2015. LNCS, vol. 9450, pp. 340–355. Springer, Hei-
    delberg (2015). https://doi.org/10.1007/978-3-662-48899-7 24
33. Heule, M.J.H.: The DRAT format and drat-trim checker. CoRR, abs/1610.06229
    (2016)
34. Joosten, S.J.C., Thiemann, R., Yamada, A.: A veriﬁed implementation of algebraic
    numbers in Isabelle/HOL. J. Autom. Reason. 64, 363–389 (2020)
35. Kan, S., Lin, A.W., Rümmer, P., Schrader, M.: Certistr: a certiﬁed string solver.
    In: Popescu, A., Zdancewic, S. (eds.) Certiﬁed Programs and Proofs (CPP), pp.
    210–224. ACM (2022)
36. Katz, G., Barrett, C., Tinelli, C., Reynolds, A., Hadarean, L.: Lazy proofs for
    DPLL(T)-based SMT solvers. In: Piskac, R., Talupur, M. (eds.) Formal Methods
    in Computer-Aided Design (FMCAD), pp. 93–100. IEEE (2016)
37. Kiesl, B., Rebola-Pardo, A., Heule, M.J.H.: Extended resolution simulates DRAT.
    In: Galmiche, D., Schulz, S., Sebastiani, R. (eds.) IJCAR 2018. LNCS (LNAI), vol.
    10900, pp. 516–531. Springer, Cham (2018). https://doi.org/10.1007/978-3-319-
    94205-6 34
38. King, T.: Eﬀective algorithms for the satisﬁability of quantiﬁer-free formulas over
    linear real and integer arithmetic (2014)
39. Lammich, P.: Eﬃcient veriﬁed (UN)SAT certiﬁcate checking. In: de Moura, L.
    (ed.) CADE 2017. LNCS (LNAI), vol. 10395, pp. 237–254. Springer, Cham (2017).
    https://doi.org/10.1007/978-3-319-63046-5 15
40. Liang, T., Reynolds, A., Tinelli, C., Barrett, C., Deters, M.: A DPLL(T ) theory
    solver for a theory of strings and regular expressions. In: Biere, A., Bloem, R. (eds.)
    CAV 2014. LNCS, vol. 8559, pp. 646–662. Springer, Cham (2014). https://doi.org/
    10.1007/978-3-319-08867-9 43
41. Mahboubi, A.: Implementing the cylindrical algebraic decomposition within the
    coq system. Math. Struct. Comput. Sci. 17(1), 99–127 (2007)
42. Nieuwenhuis, R., Oliveras, A.: Proof-producing congruence closure. In: Giesl, J.
    (ed.) RTA 2005. LNCS, vol. 3467, pp. 453–468. Springer, Heidelberg (2005).
    https://doi.org/10.1007/978-3-540-32033-3 33
43. Nieuwenhuis, R., Oliveras, A., Tinelli, C.: Solving SAT and SAT modulo theories:
    from an abstract Davis-Putnam-Logemann-Loveland procedure to DPLL(T). J.
    ACM 53(6), 937–977 (2006)
44. Nipkow, T., Wenzel, M., Paulson, L.C. (eds.): Isabelle/HOL. LNCS, vol. 2283.
    Springer, Heidelberg (2002). https://doi.org/10.1007/3-540-45949-9
             Flexible Proof Production in an Industrial-Strength SMT Solver           35

45. Ozdemir, A., Niemetz, A., Preiner, M., Zohar, Y., Barrett, C.: DRAT-based bit-
    vector proofs in CVC4. In: Janota, M., Lynce, I. (eds.) SAT 2019. LNCS, vol.
    11628, pp. 298–305. Springer, Cham (2019). https://doi.org/10.1007/978-3-030-
    24258-9 21
46. Reynolds, A., Nötzli, A., Barrett, C., Tinelli, C.: High-level abstractions for sim-
    plifying extended string constraints in SMT. In: Dillig, I., Tasiran, S. (eds.) CAV
    2019. LNCS, vol. 11562, pp. 23–42. Springer, Cham (2019). https://doi.org/10.
    1007/978-3-030-25543-5 2
47. Reynolds, A., Nötzli, A., Barrett, C.W., Tinelli, C.: Reductions for strings and
    regular expressions revisited. In: Formal Methods in Computer-Aided Design
    (FMCAD), pp. 225–235. IEEE (2020)
48. Reynolds, A., Woo, M., Barrett, C., Brumley, D., Liang, T., Tinelli, C.: Scaling
    up DPLL(T) string solvers using context-dependent simpliﬁcation. In: Majumdar,
    R., Kunčak, V. (eds.) CAV 2017. LNCS, vol. 10427, pp. 453–474. Springer, Cham
    (2017). https://doi.org/10.1007/978-3-319-63390-9 24
49. Schrijver, A.: Theory of Linear and Integer Programming. Wiley, Hoboken (1998)
50. Schurr, H.-J., Fleury, M., Barbosa, H., Fontaine, P.: Alethe: towards a generic SMT
    proof format (extended abstract). CoRR, abs/2107.02354 (2021)
51. Schurr, H.-J., Fleury, M., Desharnais, M.: Reliable reconstruction of ﬁne-grained
    proofs in a proof assistant. In: Platzer, A., Sutcliﬀe, G. (eds.) CADE 2021. LNCS
    (LNAI), vol. 12699, pp. 450–467. Springer, Cham (2021). https://doi.org/10.1007/
    978-3-030-79876-5 26
52. Stump, A., Oe, D., Reynolds, A., Hadarean, L., Tinelli, C.: SMT proof checking
    using a logical framework. Formal Methods Syst. Des. 42(1), 91–118 (2013)
53. Thiemann, R., Yamada, A.: Algebraic numbers in Isabelle/HOL. In: Blanchette,
    J.C., Merz, S. (eds.) ITP 2016. LNCS, vol. 9807, pp. 391–408. Springer, Cham
    (2016). https://doi.org/10.1007/978-3-319-43144-4 24




Open Access This chapter is licensed under the terms of the Creative Commons
Attribution 4.0 International License (http://creativecommons.org/licenses/by/4.0/),
which permits use, sharing, adaptation, distribution and reproduction in any medium
or format, as long as you give appropriate credit to the original author(s) and the
source, provide a link to the Creative Commons license and indicate if changes were
made.
     The images or other third party material in this chapter are included in the
chapter’s Creative Commons license, unless indicated otherwise in a credit line to the
material. If material is not included in the chapter’s Creative Commons license and
your intended use is not permitted by statutory regulation or exceeds the permitted
use, you will need to obtain permission directly from the copyright holder.
