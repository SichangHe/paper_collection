                                         myjournal manuscript No.
                                         (will be inserted by the editor)




                                         Constraint Solving for Finite Model Finding in SMT
                                         Solvers

                                         Andrew Reynolds · Cesare Tinelli · Clark
                                         Barrett




                                         Received: date / Accepted: date
arXiv:1706.00096v1 [cs.LO] 31 May 2017




                                         Abstract SMT solvers have been used successfully as reasoning engines for auto-
                                         mated verification and other applications based on automated reasoning. Current
                                         techniques for dealing with quantified formulas in SMT are generally incomplete,
                                         forcing SMT solvers to report “unknown” when they fail to prove the unsatisfia-
                                         bility of a formula with quantifiers. This inability to return counter-models limits
                                         their usefulness in applications that produce queries involving quantified formu-
                                         las. In this paper, we reduce these limitations by integrating finite model finding
                                         techniques based on constraint solving into the architecture used by modern SMT
                                         solvers. This approach is made possible by a novel solver for cardinality constraints,
                                         as well as techniques for on-demand instantiation of quantified formulas. Exper-
                                         iments show that our approach is competitive with the state of the art in SMT,
                                         and orthogonal to approaches in automated theorem proving.
                                         Keywords Satisfiability Modulo Theories · Finite Model Finding

                                         Under consideration for publication in Theory and Practice of Logic Programming
                                         (TPLP)


                                         1 Introduction

                                         Satisfiability modulo theories (SMT) is a subfield of automated reasoning con-
                                         cerned with the problem of determining the satisfiability of formulas in some first-

                                         The work of the first two authors was partially funded by a grant from Intel Corporation.

                                         Andrew Reynolds
                                         Department of Computer Science, The University of Iowa
                                         E-mail: andrew.j.reynolds@gmail.com
                                         Cesare Tinelli
                                         Department of Computer Science, The University of Iowa
                                         E-mail: cesare-tinelli@uiowa.edu
                                         Clark Barrett
                                         Department of Computer Science, Stanford University
                                         E-mail: barrett@cs.stanford.edu
2                                                               Andrew Reynolds et al.


order theory T , where T is usually a combination of several sub-theories. SMT
techniques and solvers have been used successfully in recent years to support a
variety of formal methods for hardware and software development, including au-
tomated verification. They are especially effective for tasks that can be reduced
to proving the unsatisfiability of quantifier-free formulas in certain theories, such
as theories of linear arithmetic, algebraic datatypes, bit vectors, arrays, strings
and so on, for which it is possible to build specialized constraint solvers. A num-
ber of applications, however, require reasoners that can prove the unsatisfiability
of quantified formulas in those theories. In verification applications, for instance,
quantified formulas are necessary to express properties of systems with an un-
bounded number of processes, or properties involving a number of memory loca-
tions. In general, the need for quantified formulas arises naturally when dealing
with function or predicate symbols that do not belong to the signature of an SMT
solver’s built-in theories.
     The few SMT solvers that can currently reason about quantified formulas are
based on incomplete methods and often report “unknown” when they fail, after
some predetermined amount of effort, to prove a quantified formula unsatisfiable.
For many client applications, however, it is very useful to know if the failure is due
to the fact that the input formula is indeed satisfiable, especially if the solver can
also return some representation of the formula’s model. Current SMT solvers are
able to produce models of satisfiable quantified formulas only in fairly restricted
cases [17], which limits their scope and usefulness.
     We reduce these limitations with a novel approach for model finding in SMT.
Since, by the undecidability of first-order logic, there are no automated methods for
finding arbitrary models, we focus on finite models, which can be represented sym-
bolically and enumerated. More precisely, because SMT solvers work with sorted
logics with both built-in and free (“uninterpreted”) sorts, we focus on finding mod-
els that interpret the free sorts as finite domains. As with traditional finite model
finders for first-order logic, the main idea is simply to check universally quantified
formulas exhaustively over candidate models with increasingly large domains for
the free sorts, until an actual model is found. Our approach differs from previous
ones in that it does not rely on the explicit introduction of domain constants for
the free sorts, as done by MACE-style model finders [10], and in that we are able
to reason modulo more theories than just the theory of equality, unlike SEM-style
model finders [38]. Moreover, and crucially for our goals, the approach is fully
integrated into the general architecture underlying most SMT solvers.
     While limited to SMT formulas with quantifiers ranging only over free sorts or
built-in finite sorts (such as, for instance, bit vector sorts or enumeration sorts),
our approach is still quite useful. Formulas with such quantifiers occur often, for
instance, in verification applications; moreover, when they are satisfiable they usu-
ally have small finite models.
     We present our model finding method in the context of an abstract framework
that models a large class of SMT solvers supporting multiple theories and quan-
tified formulas [23]. We incorporate in this framework an efficient mechanism for
deciding the satisfiability of a set of ground SMT formulas under finite cardinality
constraints for the free sorts. This is used first to find a candidate model, a model
M of a heuristically generated finite set of ground consequences of the input for-
mula ϕ. To check that M satisfies ϕ as well, the model finder then verifies, in
a complete way, that all ground consequences of ϕ over the universe of M are
Constraint Solving for Finite Model Finding in SMT Solvers                          3


satisfied by M. When this check fails, the model finder looks for a new candidate
model, possibly under extended cardinality bounds for the free sorts. The practical
effectiveness of this approach relies on two crucial components: (i) a method for
constructing and representing candidate models efficiently and (ii) a model-based
quantifier instantiation heuristic that avoids the explicit generation and checking
of all the ground instances of the input formula. The two are strictly related since
the instantiation heuristic takes advantage of the way candidate models are rep-
resented to identify, and ignore, entire sets of instances that do not need to be
considered.
    The paper is organized as follows. After discussing preliminaries in Section 3,
we present the framework used by SMT solvers in Section 4. We then present a
high-level overview of our approach for finite model finding in Section 5, followed
by details in Sections 6–8 This includes, in particular, the strategy used by the
solver for finding small candidate finite models and the algorithm for checking
the satisfiability of quantified formulas against these candidate models. Section 9
describes an experimental evaluation of our implementation of these techniques in
the SMT solver cvc4 on several sets of benchmarks.
    This paper builds on material from previous conference papers [29, 30], as well
as the PhD dissertation by the first author [32].




2 Related Work

Most traditional finite model finders for quantified formulas are based on a re-
duction to a decidable logic, propositional logic or some decidable fragments of
first-order logic, where the reduction introduces finite upper bounds on the cardi-
nalities of the atomic types. This technique was pioneered by McCune in the Mace
tool [24], and is often referred to as MACE-style model finding. These techniques
were later implemented in the tool Paradox [10], which incorporated successful
techniques for symmetry breaking. Other conceptually similar tools include FM-
Darwin [6], which handles first-order logic with equality, the Alloy Analyzer with
its backend Kodkod [36] which handles first-order relational logic, and Nitpick
[8] which handles higher-order logic. Recently, a MACE-style finite model finding
approach was also implemented in the Vampire theorem prover [28].
     A different approach to model finding, pioneered by the SEM model finder [38],
does not encode the input problem into propositional logic. Instead, it uses built-
in support for equality together with constraint propagation techniques similar
to those used in modern constraint solvers. In this respect, our approach is more
similar to SEM-style model finding than it is to MACE-style model finding.
     Our approach uses on-demand quantifier instantiation to check the satisfiabil-
ity of universally quantified formulas. Other instantiation-based approaches have
been developed, both in the automated theorem proving community [21] and in
SMT. For the latter, instantiation-based techniques are most typically used in an
incomplete way for finding proofs of unsatisfiability [13, 16, 25]. Other techniques
establish the satisfiability of quantified formulas, either by using model-based tech-
niques [17], or by reasoning in local theories where only a finite set of instances is
required for completeness [19].
4                                                                        Andrew Reynolds et al.


3 Preliminaries

We work in the context of many-sorted first-order logic with equality. A (many-
sorted) signature Σ consists of a set of sort symbols and a set of (sorted) function
symbols, f : S1 × · · · × Sn → S, where n ≥ 0 and S1 , . . . , Sn , S are sorts in Σ.
When n is 0, f is also called a constant symbol. We use the binary predicate ≈
to denote equality. We assume that Σ always includes a Boolean sort Bool and
constants true and false of that sort—allowing us to encode all other predicate
symbols as function symbols of return sort Bool. For such symbols, we may write,
e.g., P (t1 , . . . , tn ) as shorthand for the equality P (t1 , . . . , tn ) ≈ true. A signature
Σ0 is a subsignature of a signature Σ, and Σ is a supersignature of Σ0 , if every
sort and function symbol of Σ0 is also in Σ.
      Given a signature Σ, a Σ-term is either a (sorted) variable x with sort from
Σ, or an expression of the form f (t1 , . . . , tn ), where f is a function from Σ, and
t1 , . . . , tn are Σ-terms. A term t is a well-sorted term of sort S if t is a variable
having sort S, or t is of the form f (t1 , . . . , tn ) where f is of sort S1 × · · · × Sn → S,
and t1 , . . . , tn are well-sorted terms of sorts S1 , . . . , Sn respectively. An atomic
Σ-formula is an equality t1 ≈ t2 where t1 and t2 are well-sorted Σ-terms of the
same sort. A Σ-literal is either an atomic Σ-formula p or its negation ¬p. We write
s 6≈ t as an abbreviation for ¬s ≈ t. A Σ-clause is a disjunction of Σ-literals, e.g.
l1 ∨ . . . ∨ ln . A Σ-formula is an expression built from atomic Σ-formulas logical
connectives such as ∨, ∧, and ¬, and quantifiers ∀ and ∃. An occurrence of variable
x is free in a formula ϕ if it does not reside within a subformula ∀x ψ or ∃x ψ of
ϕ. We write F V (ϕ) to denote the set of variables that occur free in ϕ, or the
free variables of ϕ. A Σ-sentence is a Σ-formula with no free variables. A Σ-
term or formula is ground if it contains no variables. More generally, by a slight
abuse of terminology, we will sometimes call ground any quantifier-free term or
formula. Where x = (x1 , . . . , xn ) is a tuple of sorted variables, we write ∀x ϕ as
an abbreviation for ∀x1 · · · ∀xn ϕ and ∃x ϕ as an abbreviation for ¬∀x ¬ϕ. When
using this notation, we will implicitly assume that x is maximal—for example we
assume that ∀x1 ∀x2 ϕ is instead written as ∀x1 x2 ϕ.
      A substitution σ is a mapping from variables to terms, applied in postfix form,
such that xσ and x have the same sort for every variable x and the set Dom(σ) :=
{x | xσ 6= x}, the domain of σ, is finite. We say σ is a most general unifier (or
mgu) of terms t1 and t2 if σ is a substitution with minimal domain such that
t1 σ = t2 σ.
      A Σ-interpretation I maps each sort S in Σ to a non-empty set S I , the domain
of S in I; it maps each variable x of sort S to an element xI of S I and each func-
tion symbol f : S1 × · · · × Sn → S ∈ Σ to a total function f I : S1I × · · · × SnI → S I .
If Σ0 is a subsignature of Σ, the Σ0 -reduct of I is the Σ0 -interpretation I0 that in-
terprets the symbols of Σ0 exactly as I does. The evaluation of a term f (t1 , . . . , tn )
in I, denoted I[[t]], is defined recursively as (i) I[[x]] = xI ; (ii) I[[f (t1 , . . . , tn )]] =
f I (I[[t1 ]], . . . I[[tn ]]). For a Σ-interpretation I, a variable x of sort S, and an ele-
ment u of S I , we write I[x → u] to denote a Σ-interpretation that interprets x
as u, and is otherwise identical to I. The usual satisfiability relation |= between
Σ-interpretations and Σ-formulas, written |=, is defined as follows1

  1 Cases for additional constructs such as ⇒, ⇔ and ∃ can be defined as usual by reduction

to the cases below.
Constraint Solving for Finite Model Finding in SMT Solvers                             5


- I |= t1 ≈ t2 iff I[[t1 ]] = I[[t2 ]]
- I |= ϕ ∧ ψ iff I |= ϕ and I |= ψ
- I |= ϕ ∨ ψ iff I |= ϕ or I |= ψ
- I |= ¬ϕ iff I 6|= ϕ
- I |= ∀x ϕ iff I[x → v] |= ϕ for all v ∈ S I where S is the sort of x.
A Σ-interpretation M satisfies (or is a model of ) a Σ-formula ϕ if M |= ϕ; M
satisfies (or is a model of ) a set of Σ-formulas if it satisfies all of them. A Σ-
formula or set of Σ-formulas is satisfiable if it has a model and is unsatisfiable
otherwise. We consider only interpretations that interpret Bool as a binary set
and true and false as distinct elements of that set. We write ⊥ to abbreviate the
unsatisfiable formula false ≈ true. A set Γ of formulas propositionally entails a
formula ϕ, written Γ |=p ϕ, if the set Γ ∪ {¬ϕ} is unsatisfiable when considering
all atomic formulas in it as propositional (Boolean) variables.
    A theory is a pair T = (Σ, I) where Σ is a signature and I is a class of Σ-
interpretations, the models of T , closed under variable reassignment (that is, for all
I ∈ I, every Σ-interpretation that differs from I only in how it interprets variables
is also in I). The union of two theories T1 = (Σ1 , I1 ) and T2 = (Σ2 , I2 ), when it
exists, is the theory T1 ∪ T2 = (Σ, I) where Σ is the smallest supersignature of
Σ1 and Σ2 and I is the set of all Σ-interpretations whose Σi -reduct is in Ii for
i = 1, 2. This definition extends to more than two theories as expected.
    Given a theory T = (Σ, I), a Σ-formula ϕ is satisfiable modulo T , or T -
satisfiable, if and only if there is a model of T that satisfies ϕ. A set Γ of Σ-formulas
T -entails a Σ-formula ϕ, written Γ |=T ϕ, if every model of T that satisfies all
formulas in Γ satisfies ϕ as well. The formula ϕ is T -valid if it is T -entailed by
the empty set—equivalently, if it is satisfied by every model of T . Two sets Γ1 and
Γ2 of Σ-formulas are equisatisfiable in T if for every model of T that satisfies one
there is a model of T that satisfies the other, and the two models differ at most
on the way they interpret the free variables not shared by Γ1 and Γ2 .


4 The DPLL(T1 , . . . , Tm ) Framework

Most SMT solvers have a basic architecture that combines in a principled way a
propositional satisfiability solver, the SAT engine, with a number of theory solvers,
specialized constraint solvers for sets of literals over a specific theory. A general
framework, called DPLL(T ), to describe at an abstract but formal level the work-
ing of such SMT solvers and the interaction of their main components was orig-
inally developed by Nieuwenhuis et al. [26]. The framework, parametrized by a
background theory T , describes entire families of procedures to determine the T -
satisfiability of a ground set of input clauses. We present here a variant of it,
introduced by Krstić and Goel [23], where T is not a monolithic theory but is
instead the union of a number of separate sub-theories, each with its own theory
solver.


4.1 The theory T

For the rest of the paper, we will consider a Σ-theory T = T1 ∪ · · · ∪ Tm where each
Ti is a theory with signature Σi . One of these theories, say Te with e ∈ {1, . . . , m},
6                                                                  Andrew Reynolds et al.


may be the theory of equality—over the symbols Σe . This theory, whose set of
models consists of all Σe -interpretations, is also known as the theory of equality
with uninterpreted functions (EUF). As a consequence, we will refer to the sort
and function symbols of T that occur only in Σe as uninterpreted and to the other
symbols of T as interpreted. To stress that we treat the component theories of T
individually we will refer to our variant of DPLL(T ) as DPLL(T1 , . . . , Tm ).
    For convenience and without loss of generality, we assume that if a signature
from {Σ1 , . . . , Σm } shares a sort symbol with another signature then it shares it
also with all the signatures in the set. Finally, we impose the (true) restriction
that the signatures Σ1 , . . . , Σm share no function symbols at all except for true
and false. This restriction is currently imposed by all SMT solvers that support
multiple theories as it enables the modular combination of theory solvers for the
individual theories.


4.2 Transition system

The DPLL(T1 , . . . , Tm ) framework for theory T defines a state transition system
for each ground Σ-formula ϕ0 whose T -satisfiability one is interested in. Intuitively,
the initial state of the system corresponds to a CNF encoding of ϕ0 . Under the
right conditions on T , all of the executions of the system starting from such a state
end in a distinguished fail state if and only if ϕ0 is not T -satisfiable.

States System states are all triples of the form hM, F, Ci where
    – M , the current assignment, is a sequence of literals and decision points •,
    – F is a set of ground clauses derived from ϕ0 , and
    – C is either the distinguished value no or a clause, which we will refer to as a
      conflict clause.
Each assignment M can be factored uniquely into the subsequence concatenation
M0 • M1 • · · · • Mn , where no Mi contains decision points. For i = 0, . . . , n, we call
Mi the decision level i of M and denote with M [i] the subsequence M0 • · · · • Mi .
When convenient, we will treat M as the set of its literals. The formulas in F have
a particular purified form that can be assumed with no loss of generality since any
formula can be efficiently converted into that form while preserving equisatisfia-
bility in T : each element of F is a ground clause, and each atom occurring in F
is pure, that is, has signature Σi for some i ∈ {1, . . . , m}. By the way assignments
are constructed, their atoms too are always pure.
    Initial states have the form h∅, F0 , noi where F0 is an input set of clauses to
be checked for T -satisfiability. The expected final states are states of the form
hM, F, ⊥i, when F0 is not T -satisfiable; or else hM, F, noi with M satisfiable in T ,
F equisatisfiable with F0 in T , and M |=p F .
    If M is T -satisfiable and M |=p F we call M a satisfying assignment for F .

Transition rules The possible behaviors of the system are defined by a set of non-
deterministic state transition rules, specifying a set of successor states for each
current state. The rules are provided in Figure 1 in guarded assignment form [23].
A rule applies to a state s if all of its premises hold for s. In the rules, M , F and
C respectively denote the assignment, formula set, and conflict clause component
Constraint Solving for Finite Model Finding in SMT Solvers                                                           7

                l1 , . . . , ln ∈ M   l1 , . . . , ln |=i l l ∈ LitF ∪ IntM   l, l ∈
                                                                                   /M
Propagatei
                                                    M := M l

           l ∈ LitF ∪ IntM l, l ∈
                                /M                              C = no   l1 , . . . , ln ∈ M l1 , . . . , ln |=i ⊥
Decide                                             Conflicti
                   M := M • l                                                C := l1 ∨ · · · ∨ ln

            C =l∨D         l1 , . . . , ln |=i l l1 , . . . , ln ≺M l
Explaini
                          C := l1 ∨ · · · ∨ ln ∨ D

           ∅ |=i l1 ∨ · · · ∨ ln l1 , . . . , ln ∈ LitM |i ∪ IntM ∪ Li                      C 6= no • ∈ M
Learni                                                                          Learn0
                            F := F ∪ {l1 ∨ · · · ∨ ln }                                      F := F ∪ {C}

              C = l1 ∨ · · · ∨ ln ∨ l lev l1 , . . . , lev ln ≤ i < lev l                C 6= no • ∈
                                                                                                   /M
Backjump                                                                          Fail
                              C := no M := M [i] l                                           C := ⊥

Fig. 1 DPLL(T1 , . . . , Tm ) rules



of the current state. The conclusion describes how each component is changed, if
at all.
    We write l to denote the complement of literal l and write l ≺M l0 to indicate
that l occurs before l0 in M . The function lev maps each literal of M to the (unique)
decision level at which l occurs in M . The set LitF (resp., LitM ) consists of all
literals in F (resp., all literals in M ) and their complements. For i = 1, . . . , m,
the set LitM |i consists of the Σi -literals of LitM . IntM is the set of all interface
literals of M : the equalities and disequalities between shared variables where the
set of shared variables is

     {x | x is a variable in both LitM |i and LitM |j for some 1 ≤ i < j ≤ m} .

    The index i in the rules ranges from 0 to m for Propagatei , Conflicti and
Explaini , and from 1 to m for Learni . In all rules, |=i abbreviates |=Ti when i > 0.
In Propagate0 , l1 , . . . , ln |=0 l simply means that l1 ∨ · · · ∨ ln ∨ l ∈ F . Similarly, in
Conflict0 , l1 , . . . , ln |=0 ⊥ means that l1 ∨ · · · ∨ ln ∈ F ; in Explain0 , l1 , . . . , ln |=0 l
means that l1 ∨ · · · ∨ ln ∨ l ∈ F .
    The rules Decide, Propagate0 , Explain0 , Conflict0 , Learn, and Backjump model
the behavior of the SAT engine, which treats atoms as Boolean variables. The rules
Conflict0 and Explain0 model the conflict discovery and analysis mechanism used
by CDCL SAT solvers. All the other rules model the interaction between the SAT
engine and the individual theory solvers in the overall SMT solver.
    Generally speaking, the system uses the SAT engine to construct the assign-
ment M as if the problem were propositional, but it periodically asks the sub-
solvers for each theory Ti to check if the set of Σi -literals in M is Ti -unsatisfiable,
or entails in Ti some yet undetermined literal from LitF ∪ IntM . In the first case,
the sub-solver returns an explanation of the unsatisfiability as a conflict clause,
which is modeled by Conflicti with i ∈ {1, . . . , m}. The propagation of entailed
theory literals and the extension of the conflict analysis mechanism to them is
modeled by the rules Propagatei and Explaini .
    The inclusion of the interface literals IntM in Decide and Propagatei achieves
the effect of the Nelson-Oppen combination method [9, 35]. Under the right con-
ditions on the component theories, the two rules allows the overall system to
determine the T -satisfiability of the input formula by doing only local reasoning
8                                                                    Andrew Reynolds et al.


in the individual component theories and exchanging information between their
corresponding solvers just through (dis)equalities between interface variables.
    The rule Learni with i > 0 is needed to model theory solvers following the
splitting-on-demand paradigm [3]. When asked about the satisfiability of their
constraints, these solvers may instead return a splitting lemma, a Ti -valid formula
that encodes an additional guess that needs to be made about the literals in M
before the solver can determine their satisfiability. The set Li in the rule is a finite
set consisting of literals, not present in the input set F0 , which may be generated
by such solvers.


4.3 System executions and correctness

An execution of a transition system modeled as above is a (possibly infinite) se-
quence s0 , s1 , . . . of states such that s0 is an initial state and for all i ≥ 0, si+1 can
be generated from si by the application of one of the transition rules. A system
state is reachable if it occurs in some execution; it is irreducible if no transition
rules besides Learni , apply to it. An exhausted execution is a finite execution whose
last state is irreducible. A complete execution is either an exhausted execution or
an infinite execution. An application of Learni , with i ≥ 0, is redundant in an
execution if the execution contains a previous application of Learni with the same
premise.
    Adapting results from [3, 23, 26], it can be shown that every execution starting
with a state h∅, F0 , noi and ending in hM, F, Ci satisfies the following invariants:
1. M contains only pure literals and no repetitions;
2. F |=T C and M |=p ¬C when C 6= no;
3. F0 and F are equisatisfiable in T .
Moreover, the transition system is terminating: every execution with no redundant
applications of Learni is finite; and sound : for every execution starting with a state
h∅, F0 , noi and ending with a state hM, F, ⊥i, the clause set F0 is T -unsatisfiable.
Under suitable assumptions on the sub-theories T1 , . . . , Tm , the system is also
complete: for every exhausted execution starting with h∅, F0 , noi and ending with
hM, F, noi, M is satisfiable in T and M |=p F0 . Here, we provide a sketch of the
correctness proof for DPLL(T1 , . . . , Tm ) restricted to a single theory T1 based on
the proof for the original framework [26].
Theorem 1 Suppose T = T1 . With any strategy where all applications of Learn1
are not redundant and introduce new literals only from a finite set L1 , DPLL(T1 )
is sound, complete, and terminating for all sets F0 of ground clauses.
Proof: (Sketch)
    Soundness) Observe that all reachable states of the form hM, F, Ci where C 6=
no are such that C is T1 -entailed by F0 . When C is introduced by Conflict0 , it is
a clause from F ; when it is introduced by Conflict1 , it is T1 -valid. When applying
Explaini , we replace a literal l in C with disjunction of literals l1 ∨ · · · ∨ ln which
is entailed by l either in the theory T1 (when i = 1), or together with F (when
i = 0). Thus, when a state of the form hM, F, ⊥i is reachable, we can conclude
that F |=T1 ⊥. Since all clauses in F are T1 -entailed by F0 by construction, ⊥ is
T1 -entailed by F0 as well.
Constraint Solving for Finite Model Finding in SMT Solvers                               9

 proc check(M, F, C) ≡                          proc check conflict(M, F, C) ≡
   (Propagate0 | . . . | Propagaten )∗ ;          if C 6= no
   if weak effort(M, F, C) = true                    (Explain0 | . . . | Explainn )∗ ;
      if l, l ∈
              / M for some l ∈ LitF                  if C = ∅
         Decide on l                                    return hM, F, ⊥i
      else if strong effort(M, F, C)                 else
         return hM, F, noi                              Learn; Backjump
   return check conflict(M, F, C)                 return check(M, F, C)

Fig. 2 A typical strategy check for applying DPLL(T1 , . . . , Tm ) rules.



    Termination) For all reachable states hM, F, Ci, every literal occurring in M ,
F or C belongs to the finite set of literals LitM ∪ IntM ∪ L1 . As a consequence,
there is only a finite number of reachable states. Consider a partial ordering 
on assignments M , with the empty assignment as maximal element, such that
(e1 M1 )  (e2 M2 ) if either (i) e1 = • and e2 6= • or (ii) e1 = e2 and M1  M2 .
In addition, consider a partial ordering  on conflict clauses, seeing as sets of
literals, such that C1  C2 if either C1 is no, or neither C1 nor C2 are no and
C2 ≺mul
      M    C1 , where ≺mul
                        M     is the multiset extension of ≺M . Extend this ordering
to states so that hM1 , F1 , C1 i  hM2 , F2 , C2 i if and only if M1  M2 , or M1 = M2
and C1  C2 . One can show that this ordering is well founded. Moreover, applying
all rules besides Learn1 to a state s results in a state s0 where s  s0 . Termination
then follows from the fact that Learn1 is applicable only a finite number of times.
    Completeness) We claim that for every irreducible reachable state hM, F, noi,
M is a T1 -satisfiable satisfying assignment for F . To see this, consider first that
since Decide does not apply to the state, M must contain an assignment for all
literals in F . Moreover, M is a satisfying assignment for F since Conflict0 does
not apply. Since Conflict1 does not apply, then M must be T1 -satisfiable. Since
F0 ⊆ F , we have that M propositionally entails F0 , and thus F0 is T1 -satisfiable
as well. Thus, since our procedure is terminating, it is also complete.            
   The soundness and termination arguments in the proof above immediately ex-
tend to the multiple theory case of DPLL(T1 , . . . , Tm ) where m > 1. The complete-
ness argument can be extended as well under further model-theoretic assumptions
on the component theories [23, 20].



4.4 A Typical Strategy for DPLL(T1 , . . . , Tm )

A typical strategy for applying the theory-specific rules of DPLL(T1 , . . . , Tm ) is
outlined in Figure 2 where | denotes alternative choice and ∗ denotes zero or more
rule applications. The check procedure involves two sub-procedures weak effort and
strong effort, which are not shown here and are specific to the theory T . Each of
these methods when invoked either applies Conflicti or Learni for some 1 ≤ i ≤ m
and returns false, or applies no rules and returns true.
    Weak effort checks, as denoted by weak effort, are commonly used to eagerly
avoid extensions that are clearly unsatisfiable in one of the theories. On the
other hand, strong effort checks, as denoted by strong effort, are required to make
progress towards determining the T -satisfiability of the conjunction of literals
in M . In particular, unlike weak effort, we require that strong effort returns true
10                                                                Andrew Reynolds et al.


only when M is T -satisfiable. Generally speaking, weak effort checks typically in-
volve computationally inexpensive reasoning at the cost of incompleteness, whereas
strong effort checks are complete but may involve expensive reasoning. The design
of a theory solver in the DPLL(T1 , . . . , Tm ) framework depends largely on how the
methods weak effort and strong effort are implemented. We will see an example of
these functions in Section 6.2.
    In more detail, the first sub-procedure check in Figure 2 applies to states
hM, F, Ci where C = no. We first apply the rule Propagatei for sub-theories Ti ,
possibly multiple times. Afterwards, we apply a weak effort check. If no conflicts
or clauses are learned at weak effort, we apply Decide on some unassigned literal
l from LitF , if one exists. Otherwise, our assignment M is complete, and we apply
a strong effort check to verify the T -satisfiability of M . If strong effort(M, F, C)
returns true, then M is satisfiable in T , and the method returns the (final) state
hM, F, noi, indicating that F is satisfiable. In all other cases, we apply check conflict.
    The second sub-procedure check conflict is applied to states hM, F, Ci where C
may be different from no. In those cases, we perform conflict analysis by repeated
applications of Explaini . If we reach the fail state, then we know F is unsatisfiable.
Otherwise, we add a learned clause via Learn, and apply Backjump to return to a
prefix of M .
    We formally state the requirements of weak and strong effort checks for the
single theory case in the following proposition which is a consequence of Theorem 1.

Proposition 1 Suppose T = T1 . The check method in Figure 2 implements a
sound, complete, and terminating strategy for all sets F0 of ground clauses provided
all of the following hold.
1. In weak effort and strong effort, all applications of Learn1 are not redundant
   and introduce new literals only from a finite set L1 .
2. weak effort and strong effort return false only when they apply at least one rule.
3. strong effort(M, F, C) returns true only when the conjunction of the literals in
   M is T1 -satisfiable.

Proof: (Sketch) The first point ensures that check meets the requirements on
applications of Learn1 as given in Theorem 1; the second point ensures that check is
a terminating method; and the third point ensures that check generates exhaustive
executions.                                                                       


5 Finite Model Finding in SMT

The DPLL(T1 , . . . , Tm ) framework described in the previous section is limited to
quantifier-free formulas. This section outlines an approach for finite model finding
for quantified formulas that can be integrated in DPLL(T1 , . . . , Tm )-based SMT
solvers. Concretely, we consider Σ-formulas in the following language:

                     φ := t1 ≈ t2 | φ1 ∧ φ2 | φ1 ∨ φ2 | ¬φ | ∀x ϕ

where t1 and t2 are Σ-terms, and the sort of x is either an uninterpreted sort or
a sort interpreted in every model of T as a finite set of some fixed cardinality.
Examples of the latter include sorts denoting fixed-length bit-vectors or finite
(non-recursive) datatypes. Certain integer arithmetic constraints with bounded
Constraint Solving for Finite Model Finding in SMT Solvers                                     11


quantifiers, where the bounds are explicitly provided or can be inferred, can be
treated similarly to finite interpreted sorts [32, 5]. Many applications of SMT rely
on solving problems that fall into such categories, given a careful encoding of the
constraints.
    Given an input formula ψ in the grammar above, our approach first performs
a purification step, which results in a set F of ground clauses, and a set A of
equivalences of the form a ≈ true ⇔ ∀x ϕ, abbreviated as a ⇔ ∀x ϕ, where a
is a Boolean variable uniquely associated with the quantified formula ∀x ϕ. We
will refer to a as the proxy variable for ∀x ϕ. The set F can be constructed by
a standard conversion of ψ to clausal form which, however, treats the quantified
subformulas of ψ as atoms. After that, each quantified formula ∀x ϕ occurring in a
clause of F is replaced with its proxy variable a if it occurs positively in the clause,
and with ϕ{x 7→ k} otherwise, where ϕ{x 7→ k} is the result of substituting each
occurrence in ϕ of a variable x of x with a fresh variable k (to be treated like a
Skolem constant). The process is repeated until F contains no quantifiers. This
conversion from ψ to F and A can be done so that ψ and F ∪ A are equisatisfiable.
We will denote by bψc the resulting pair (F, A).

Example 1 Consider the formula ψ = ¬P (b, c) ∧ (Q(b, c) ⇔ ∀x P (b, x)) where P
and Q are uninterpreted predicates and x, b and c are of some uninterpreted sort
S. The purified form bψc is computed as follows. First, a conversion of ψ to clausal
normal form results in the clauses:

            F0 := {¬P (b, c), ¬Q(b, c) ∨ ∀x P (b, x), Q(b, c) ∨ ¬∀x P (b, x)}

We replace the occurrence of ¬∀x P (b, x) in the third clause of F0 with ¬P (b, k),
where k is a fresh variable of sort S, and replace the positive occurrence in the
second clause with a fresh proxy variable a of sort Bool. We obtain the quantifier-
free set of purified clauses F and equivalences A:

                  F    :=    {¬P (b, c), ¬P (b, k) ∨ Q(b, c), a ∨ ¬Q(b, c)}
                  A    :=    {a ⇔ ∀x P (b, x)}

It is not hard to see that φ and F ∪ A are equisatisfiable in T .                              



Model finding procedure

Figure 3 describes a finite model finding procedure called FM-SolveH that takes
as input a set F and a set A, where (F, A) = bφc for some Σ-formula ψ, and tries
to determine the satisfiability of F ∪ A by adding to F instances of the quanti-
fied formulas that occur in A. The procedure is parametrized by an instantiation
heuristic H for the quantified formulas.
    In Step 1, it looks for a satisfying assignment M for F .2 This assignment
can be found using the DPLL(T1 , . . . , Tm ) procedure from the previous section.
If no satisfying assignment can be found, the procedure terminates with unsat,
for “unsatisfiable.” Otherwise, in Step 2, it constructs a Σ-interpretation M that
  2 Recall that a satisfying assignment is a T -satisfiable set of Σ-literals that propositionally

entail F .
12                                                                           Andrew Reynolds et al.


     FM-SolveH (F, A)
     Input: A set F of purified Σ-clauses and a set A of equivalences
     Output: sat or unsat

     1. Find a satisfying assignment M for F . If none is found, return unsat.
     2. Construct a Σ-interpretation M that satisfies M . Let V be a minimal set of Σ-terms
        such that, for each uninterpreted sort S of Σ, every element of S M is denoted by a
        term in V (that is, for all s ∈ S M there is a v ∈ V such that s = M[[v]]).
     3. For each ∀x ϕ where a ⇔ ∀x ϕ ∈ A and a ∈ M ,
        (a) let Ix be the set of substitutions from x to terms in V chosen by H(M, ∀x ϕ);
        (b) let (F, A) = (F ∪ F 0 , A ∪ A0 ) where (F 0 , A0 ) = b{¬a ∨ ϕσ | σ ∈ Ix }c.
        If each of the sets Ix was empty, return sat, otherwise go to Step 1.



Fig. 3 Finite Model Finding Procedure FM-SolveH , parameterized by a quantifier instantia-
tion heuristic H.


satisfies M . In doing so, however, it considers only Σ-interpretations M that
interpret the uninterpreted sorts of Σ as finite sets. This makes it feasible to
actually construct the set V used in Step 3. In that step, the procedure considers
the set of quantified formulas that are active in M , that is, those whose proxy
variable occurs positively in M . It adds new constraints F 0 ∪ A0 to F ∪ A based on
instances of quantified formulas chosen by the heuristic H, which takes as input a
model and a quantified formula. We consider only heuristics that are sound with
respect to models: if H returns no instances for quantified formulas in Step 3, it
is because M satisfies all active quantified formulas in M , and so the procedure
terminates with sat, for “satisfiable.”

Theorem 2 For all inputs F, A for FM-SolveH , the following hold.
1. If the method for finding satisfying assignments M for F in Step 1 is sound,
   then the procedure FM-SolveH returns unsat only if F ∪ A is T -unsatisfiable.
2. If for all inputs, H(M, ∀x ϕ) returns the empty set only if M |= ∀x ϕ, then the
   procedure FM-SolveH returns sat only if F ∪ A is T -satisfiable.
Proof: To show Point 1, assume the method for finding satisfying assignments
M for F in Step 1 is sound. Thus, when the procedure returns unsat, we have
that F is T -unsatisfiable. Since the formulas added to F and A in Step 3 preserve
satisfiability, we have that our input is T -unsatisfiable as well.
    To show Point 2, the procedure returns sat when H(M, ∀x ϕ) returns the empty
set for all quantified formulas where a ⇔ ∀x ϕ ∈ A and a ∈ M . Assume M |= ∀x ϕ
                                                                        0
for all such formulas. Then, F ∪A is satisfied by a model M0 where aM = (∀x ϕ)M
for each a ⇔ ∀x ϕ ∈ A and a 6∈ M , and where all other symbols are interpreted
as in M. Since during all iterations of the procedure F ∪ A remains a superset of
the original input, we have that the latter is satisfied by M0 as well.         

    The following sections will examine in more detail the main ideas behind the
three steps of procedure FM-SolveH . In Section 6, we describe techniques for find-
ing satisfying assignments in Step 1. These assignments have models that interpret
Constraint Solving for Finite Model Finding in SMT Solvers                         13


uninterpreted sorts as sets of minimal cardinality and are used in Step 2. In Sec-
tion 7, we describe methods for constructing such models. Finally, in Section 8,
we describe quantifier instantiation heuristics that can be used to choose sets of
substitutions for Step 3.
     Although Theorem 2 holds in general for inputs that involve several theories,
for simplicity, we restrict ourselves in the following to problems in EUF only, that
is, involving only uninterpreted sorts and function symbols. Under these restric-
tions, we provide arguments for the correctness of the three steps of FM-SolveH
in Theorems 4 and 5, which ensure the correctness of our finite model finding
procedure according to Theorem 2.


6 EUF with Finite Cardinality Constraints (FCC)

In this section, we introduce techniques for finding satisfying assignments in Step
1 of procedure FM-SolveH from Figure 3. We will focus on satisfying assignments
that have small models, that is, models which interpret the uninterpreted sorts of
our signature as finite sets of minimal size. To do this, we introduce an extension of
the theory EUF with finite cardinality constraints (FCC). We describe its signature
(ΣFCC ) and semantics, give a satisfiabiliy procedure for conjunctions of literals in
this theory, and describe how it can be integrated into the DPLL(T1 , . . . , Tm ) ar-
chitecture. Finally, we discuss a strategy, fixed-cardinality checkFCC , which ensures
that upper bounds are incrementally established for all uninterpreted sorts.

Definition 1 (FCC) Let EUF be the theory of equality and uninterpreted func-
tions over some signature ΣEUF . The theory FCC of EUF with finite cardinality
constraints is the extension of EUF obtained as follows. The signature ΣFCC of
FCC extends ΣEUF with a constant cardS,k of sort Bool for each sort S of ΣEUF
and integer k > 0. Its models are all ΣFCC -interpretations that satisfy each atomic
formula cardS,k exactly when they interpret S as a set of cardinality at most k.

    As shown below, the FCC-satisfiability of sets of ΣFCC -literals is a decidable
problem. By a reduction from graph (vertex) coloring, one can show that the
problem is NP-hard. The main idea of the reduction is to represent the set of k
colors as a sort C and represent the vertices of the graph as variables of sort C.
An edge between two vertices x and y is encoded as the constraint x 6≈ y. The
cardinality constraint on C is encoded by cardC,k . It is not difficult to see that
given a model M of FCC (which is finitely representable), checking whether M
satisfies a set of ΣFCC -literals can be done in polynomial time. It follows that this
satisfiability problem is NP-complete.
    We prove its decidability by providing an effective satisfiability procedure. The
procedure relies on computing certain congruence closures of sets of constraints,
so we start by introducing that notion.

Definition 2 (Congruence Closure) Let M be a set of literals, in any signa-
ture, and let TM be the set of all terms (and subterms) occurring in M . The
congruence closure M ∗ of M is the smallest set of literals such that
1. M ⊆ M ∗ ⊆ {s ≈ t | s, t ∈ TM } ∪ {s 6≈ t | s, t ∈ TM };
2. for all s, t ∈ TM , M ∗ |=EUF s ≈ t iff s ≈ t ∈ M ∗ .
14                                                                     Andrew Reynolds et al.


     Input: A set M of ΣFCC -literals
     Output: sat or unsat
     1. If s ≈ t ∈ M ∗ for some s 6≈ t ∈ M ∪ {false 6≈ true}, return unsat.
     2. If M contains no positive cardinality literals, return sat;
        otherwise, let k be the smallest integer such that cardS,k ∈ M .
     3. If ¬cardS,j ∈ M for some j ≥ k, return unsat.
     4. If there are k or fewer equivalence classes in M ∗ , return sat.
     5. If there exists two terms s and t in distinct equivalence classes of M ∗ such that
        M 6|=EUF s 6≈ t, run the procedure recursively on M ∪ s ≈ t and M ∪ s 6≈ t, returning
        sat if either of the two subcalls returns sat, and returning unsat otherwise.
     6. Return unsat.



Fig. 4 Decision Procedure for FCC.


    By construction, the relation {(s, t) | s ≈ t ∈ M ∗ } induced by M ∗ is a con-
gruence, and hence an equivalence, relation over TM . For brevity, we will identify
M ∗ with its induced equivalence relation when convenient. It can be shown (see,
e.g., [1]) that (i) M ∗ is computable whenever M is finite, and (ii) if M is satis-
fiable it is satisfied by an interpretation M that interprets each sort S as the set
VS = {v1S , . . . , vn
                     S
                      S
                        } consisting of an arbitrary representative viS for each of the nS
equivalence classes of M ∗ over terms of sort S. We call M a normal model of M .
Our procedure will seek to find normal models for given input sets M of literals.


6.1 Decision Procedure

This section presents a decision procedure for the satisfiability of sets of constraints
in the theory FCC. For now, we limit ourselves to signatures ΣFCC whose set of
sorts consists of a single (uninterpreted) sort S. Figure 4 gives the decision proce-
dure for the satisfiability problem in this case. As input, the procedure takes a set
M consisting of cardinality constraint literals for S and equalities and disequalities
over ground ΣFCC -terms of sort S, and terminates with sat or unsat.

Lemma 1 The procedure in Figure 4 is sound, complete and terminating for every
set M of ΣFCC -literals.

Proof: Soundness) Let us start by observing that splitting the problem based on
equalities s ≈ t, as done in Step 5 of the procedure, is trivially sound since all
models of FCC satisfy exactly one of s ≈ t and s 6≈ t. The procedure answers
unsat in one of the following cases:
1. an equality s ≈ t is entailed by M where s 6≈ t is also in M ∪ {false 6≈ true},
2. conflicting literals cardS,k and ¬cardS,j are asserted for j ≥ k, or
3. there exist k + 1 terms (each in a different equivalence class) that are entailed
   to be mutually disequal by M .
For the first case, it is immediate that M has no models. For conflicts in the second
case, no model can be constructed with both at most k and at least j + 1 elements
in the domain of S. For conflicts in the third case, note that if the procedure reaches
Step 6 there must be k + 1 equivalence classes with representatives t1 , . . . , tk+1 ,
Constraint Solving for Finite Model Finding in SMT Solvers                          15


say, where M |=EUF ti 6≈ tj for all 1 ≤ i < j ≤ k + 1; hence no model can be
constructed satisfying cardS,k .
    Termination) It is easy to see that when the procedure recurses in Step 5,
the set of equalities and disequalities in M without the cardinality constraints is
satisfiable. Let C be a set collecting the equivalence classes of M ∗ and let [t]M
denote the equivalence class of a term t. We argue that the splitting on the equality
of s and t done at Step 5 decreases the size of the set

         EM := { ([u]M , [v]M ) ∈ C × C | [u]M 6= [v]M , M 6|=EUF u 6≈ v }         (1)

in other words, it decreases the number of equivalence classes that are pairwise not
entailed to be disequal. In either branch of the split on s ≈ t, no equivalence classes
are created (although two existing ones are possibly merged), and ([s]M , [t]M ) is
no longer an element of EM in the recursive call. When EM becomes empty, the
procedure is guaranteed to terminate, since either more than k equivalence classes
are entailed to be distinct, in which case the procedure answers unsat, or there are
at most k equivalence classes, in which case the procedure answers sat.
    Completeness) The procedure answers sat when the congruence closure M ∗
contains no equality whose negation occurs in M , and either there is no positive
cardinality literal in M , or M ∗ has at most k equivalence classes where k is the
smallest integer such that cardS,k ∈ M . In either case, we can construct a model
where S is interpreted as a set of size j, with j ≤ k for all cardS,k ∈ M and j ≥ k
for all ¬cardS,k ∈ M . If j is greater than the number of equivalence classes in M ∗ ,
arbitrary new elements can be added to the domain of S without affecting the
satisfiability of the equalities and disequalities in M .                          
  An immediate consequence of this lemma is that constraint satisfiability in
FCC is decidable.

Proposition 2 The FCC-satisfiability of sets of ΣFCC -literals is decidable.

   The completeness argument in Lemma 1 also suggests a constructive proof of
the following result.
Proposition 3 Every satisfiable set of ΣFCC -literals has a finite model.
   We point out that in the absence of cardinality constraints the decision pro-
cedure in Figure 4 reduces to the standard congruence closure procedure used to
decide the satisfiability of constraints in EUF. SMT solvers supporting EUF have
theory solvers that essentially implement that procedure.


6.2 Integration into DPLL(T1 , . . . , Tm )

Our decision procedure for FCC can be integrated into the DPLL(T1 , . . . , Tm )
framework by capitalizing on the existence of a theory solver for EUF (Te ). We
effectively extend such a solver modularly with facilities to reason about cardinality
constraints as well. Since FCC is an extension of EUF, we now replace the latter
with the former in the framework and make Te = FCC. Recall the strategy outlined
in Figure 2 of Section 4.4. In the following, we detail how the methods weak effort
and strong effort of this strategy are implemented for FCC.
16                                                                            Andrew Reynolds et al.

proc weak effort FCC (M, F, C) ≡
  if l1 , . . . , ln |=EUF ⊥ for some l1 , . . . , ln ∈ M
     Apply Conflicte with C := l1 ∨ · · · ∨ ln , return false
  else if cardS,k , ¬cardS,j ∈ M for j > k,
     Apply Conflicte with C := ¬cardS,k ∨ cardS,j , return false
  else if cardS,k ∈ M and M |=EUF distinct(t1 , . . . , tk+1 )
     Apply Learne to ¬cardS,k ∨ ¬distinct(t1 , . . . , tk+1 ), return false
  else
     return true


Fig. 5 Weak effort check for FCC.


   For simplicity, we maintain the restriction for now that FCC contains a single
uninterpreted sort S. Also, when convenient, we identify equivalence classes of
terms with their representative terms.

Weak Effort Check

At weak effort, we recognize conflicting states of three different forms, outlined in
Figure 5. First, if we are unable to construct a congruence closure for M that is
consistent with the disequalities from M , we identify a subset {l1 , . . . , ln } of M that
is EUF-unsatisfiable and apply Conflicte to it. Second, if M contains the conflicting
cardinality constraints cardS,k ∈ M and ¬cardS,j with j > k, we construct the
conflict clause ¬cardS,k ∨cardS,j . Third, we may recognize cases when M contains a
literal of the form cardS,k while its other literals entails that k+1 terms t1 , . . . , tk+1
are pairwise disequal. In this case, we use Learne to add the lemma ¬cardS,k ∨
¬distinct(t1 , . . . , tk+1 ) to the current set F of clauses, where distinct(t1 , . . . , tk+1 )
is shorthand for the conjunction of disequalities stating that the terms t1 , . . . , tk+1
are pairwise distinct.3 We will refer to a lemma of this form as a clique lemma. We
assume that this instance of Learne is applied only when the resultant clause does
not occur in F . In practice, this can be achieved either by maintaining a cache of
learned clauses or by ensuring Propagatee is applied to completion between each
call. We apply Learne because the constraint ¬distinct(t1 , . . . , tk+1 ) may contain
literals not belonging to F . We could alternatively apply Conflicte to construct a
conflict clause of form l1 ∨ . . . ∨ ln ∨ ¬cardS,k , where {l1 , . . . , ln } is a subset of M
that entails distinct(t1 , . . . , tk+1 ). However, we have found that in practice this is
inefficient, as many different sets of literals can be found for essentially the same
conflict.

Generating clique lemmas For the purposes of discovering and learning clique
lemmas, we incrementally construct and maintain on the side a disequality graph
D for S, whose vertices correspond to the equivalence classes of terms of sort S
induced by the congruence closure of M , and whose edges represent disequalities in
M between terms in different equivalence classes. In this representation, a sufficient
condition for discovering a conflict reduces to finding a (k + 1)-clique in D. Now,
even just checking for the presence of a (k + 1)-clique in a n-vertex graph is too
expensive in general—as this is an NP-complete problem [15]. For this reason, the
weak effort check of our procedure uses an incomplete check for potential cliques.
 3   Note that ¬cardS,k ∨ ¬distinct(t1 , . . . , tk+1 ) is a valid formula of FCC.
Constraint Solving for Finite Model Finding in SMT Solvers                            17


This is done by partitioning the vertices of the graph into suitable subsets that
we call regions. After defining regions formally, we explain below how we exploit
them to discover clique-related conflicts efficiently in practice.

Definition 3 (k-Region) Let D = (V, E) be an undirected graph and let R be
a subset of V . For all vertices v ∈ R, let ext(v) be the number of edges between
v and vertices not in R. We say R is a k-region of D if for all 0 < i ≤ k, the size
of the set {v | v ∈ R, ext(v) ≥ i} is smaller than k − i. A k-regionalization RD of
D is a partition of V into k-regions. We will refer to it simply as a regionalization
when k is understood or not important.

     Regionalizations are useful for us because they facilitate the discovery of cliques.

Lemma 2 If RD is a k-regionalization of a graph D and D contains a k-clique
C, then all the vertices of C reside in the same region of RD .

Proof: If k ≤ 1, the statement is trivial. Otherwise, assume by contradiction D
contains k-clique C = C1 ∪ C2 for non-empty C1 , C2 where, for some region R
of RD , v ∈ R for all v ∈ C1 and v 6∈ R for all v ∈ C2 . Say |C2 | = i, and thus
|C1 | = k − i. Since C is a k-clique, ext(v) must be at least i for all v ∈ C1 ,
contradicting the assumption that R is a region.                              
    Notice that any graph D = (V, E) has a trivial regionalization, with just one
region which contains all vertices in V .

Example 2 Consider the constraints {c1 6≈ c2 , c2 6≈ c3 , c3 6≈ c4 }, all over sort S,
and the partition {{c1 , c2 }, {c3 , c4 }}. This partition is a 3-regionalization in the
disequality graph induced by this set, because a 3-clique can span two regions only
if it contains two vertices with interregional edges, and this partition only has one
such edge. Adding the disequality c2 6≈ c4 or c1 6≈ c4 breaks the regionalization
invariant.                                                                            

    Let us examine how to maintain a k-regionalization in an (initially empty)
evolving graph D, a data structure supporting the dynamic allocation of vertices
and edges, as well as the merging of vertices. In our framework, where D’s vertices
correspond to equivalence classes of terms and edges to disequalities between them,
these operations are triggered by operations performed on the data structure that
stores the congruence closure M ∗ of the current assignment M . In particular, a
vertex ve is added to D when a new equivalence class e is created, which happens
whenever a new term is added to M ; an edge between the vertices v1 and v2
corresponding to equivalence classes e1 and e2 is added to D when the disequation
t1 6≈ t2 is added to M , for some term t1 in e1 and t2 in e2 ; and two vertices
are merged, in a single vertex that inherits their edges, when their corresponding
equivalence classes are merged during the computation of M ∗ .
    We maintain at all times a (k + 1)-regionalization RD of the graph D, where
k is the smallest integer such as cardS,k ∈ M .4 As the graph D is modified, it
may be necessary to merge certain regions of the current within RD to ensure
the invariant in Definition 3 holds. The procedure fix region from Figure 6 ensures
that a set R within RD is a k-region by merging it as needed with another set
 4   Recall that cardS,k states that sort S has at most k elements.
18                                                                   Andrew Reynolds et al.

proc fix region(R, RD ) ≡
  if R is not a k-region
     choose some R0 ∈ RD , where R0 6= R
     R := R \ {R, R0 } ∪ {R ∪ R0 }
     fix region({R ∪ R0 }, RD )

Fig. 6 The fix region procedure. Ensures R ∈ RD is a k-region by merging it with another
R0 ∈ RD , and repeating this process recursively.


R0 in RD , and repeating this process recursively until R becomes a k-region. As
a heuristic, we choose the R0 with the highest density of interregional edges to R.
    Assuming we have a regionalization RD for graph D, here is how we construct a
regionalization RD0 for graph D0 resulting from an addition to M . In the following,
R(v) denotes the region in a regionalization R that contains the vertex v.

Adding Vertices: When a vertex v is added to D, RD0 is the result of adding the
  singleton region {v} to RD .
Adding Edges: When we add an edge (v1 , v2 ) to D, we have that RD0 = RD is still
  a partition of V . However, RD (v1 ) or RD (v2 ) may not be regions of D0 . We ap-
  ply the procedure fix region first to (RD (v1 ), RD0 ) and then to (RD (v2 ), RD0 )
  to ensure that RD0 is a regionalization.
 Merging Vertices: When a vertex v1 is merged with another vertex v2 in D, we
  have that D0 is a quotient graph of D, that is, D0 contains a new vertex, call
  it u, connected to all vertices that are connected to either v1 or v2 in D. If
  RD (v1 ) is equal to RD (v2 ), let R be (RD (v1 ) ∪ {u}) \ {v1 , v2 }. Then RD0 is
  equal to (RD ∪ R) \ {RD (v1 )}. To ensure RD0 is a regionalization, we apply
  fix region to (R, RD0 ). If RD (v1 ) is not equal to RD (v2 ), let {vi , vj } = {v1 , v2 },
  Ri = (RD (vi ) ∪ {u}) \ {vi }, and Rj = RD (vj ) \ {vj }. Then, RD0 is equal to
  (RD ∪ {Ri , Rj }) \ {RD (v1 ), RD (v2 )}. We apply fix region to (Ri , RD0 ) and
  subsequently to (Rj , RD0 ).

    Additionally, when cardS,k0 is asserted for k0 < k, we discard the (k + 1)-
regionalization and rebuild a (k0 + 1)-regionalization.
    Given a (k + 1)-regionalization RD of D, we will call each region in RD with
at least k + 1 vertices a large region, and all others small regions. For the purposes
of efficiently discovering (k + 1)-cliques during weak effort checks, we maintain a
watched set of k + 1 vertices for each large region R in RD , which we will write as
w(R). This set is incrementally updated when vertices are added or removed from
regions, and when regions are combined. If there exists a large region R in RD
where each vertex in w(R) is connected, then we add the clique lemma ¬cardS,k ∨
¬distinct(t1 , . . . , tk+1 ) to F using the rule Learne , where w(R) = {t1 , . . . , tk+1 }.

Strong Effort Check

Recall from Section 4.4 that a strong effort check must determine that the current
set of constraints is consistent, or otherwise report a conflict or lemma. The strong
effort check of the FCC solver is given in Figure 7. If cardS,k ∈ M for some
(minimal) k, and there are more than k equivalence class of sort S in the congruence
closure of M , then we choose two equivalence class representatives ti and tj and
apply Learne to add the splitting lemma (ti ≈ tj ∨ ti 6≈ tj ) to F . In practice,
Constraint Solving for Finite Model Finding in SMT Solvers                                19

proc strong effort FCC (M, F, C) ≡
  let k be the smallest integer such that cardS,k ∈ M
  let t1 , . . . , tn be the equivalence class representatives of sort S in M ∗
  if n > k
     choose 1 ≤ i < j ≤ n such that M 6|=EUF ti 6≈ tj
     apply Learne to ti ≈ tj ∨ ti 6≈ tj
     return false
  else
     return true


Fig. 7 Strong effort check for FCC.


we also insist that future applications of Decide on the atom ti ≈ tj should be
invoked with positive polarity. If the number of equivalence classes is less than or
equal to k, then the procedure returns true, indicating that M is FCC-satisfiable.
    The choice of ti and tj is guided by the watched set of vertices within regions.
In particular, if there is a large region R in RD , we know that w(R) does not form
a clique. We choose ti , tj to be two vertices from w(R) that are not connected
in D. Otherwise, if there are no large regions in RD and there are more than k
vertices in D, then there must be at least two small regions. We select two regions
Ri and Rj based on a heuristic (namely, the maximum density of interregional
edges), combine them into a new region Ri ∪ Rj , apply fix region to Ri ∪ Rj , and
repeat.
    We illustrate the operation of the FCC solver with a couple of examples.
Example 3 Consider the constraints {a ≈ f (b), b ≈ f (c), a 6≈ b, b 6≈ c, cardS,2 }
where all terms are over the single sort S. First, the FCC solver computes the con-
gruence {{a, f (b)}, {b, f (c)}, {c}}. Using a, b, c as the representatives, the solver
builds the disequality graph with edges {(a, b), (b, c)}. Since cardS,2 limits the size
of S to at most 2, the solver generates the lemma a ≈ c ∨ a 6≈ c. Adding the
constraint a ≈ c produces no conflicts and allows the FCC solver to answer “sat-
isfiable”.                                                                           
Example 4 Consider the constraints {c1 ≈ c, c4 ≈ c, c1 6≈ c2 , c2 6≈ c3 , c3 6≈
c4 , cardS,2 } with all constants of sort S. The corresponding disequality graph for
these constraints contains a clique of size 3. By discovering that clique, the FCC
solver can conclude that it is impossible to shrink the model to 2 elements, and
hence reports a clique lemma of the form ¬distinct(c1 , c2 , c3 ) ∨ ¬cardS,2 .    
    Because of congruence constraints, guesses on merge lemmas may sometimes
lead to inconsistencies when constructing the congruence closure, unless we com-
pute and propagate all entailed disequalities—which is usually not done, for effi-
ciency. This is demonstrated in the following example.
Example 5 Consider the constraints {c3 ≈ f (c1 ), c4 ≈ f (c2 ), c3 6≈ c4 , cardS,2 }
where all the terms have sort S. Unless the EUF subsolver propagates the entailed
literal c1 6≈ c2 , the FCC solver will construct the disequality graph (V, E) =
({c1 , c2 , c3 , c4 }, {(c3 , c4 )}) for S. Say we decide to apply Learne on (c1 ≈ c2 ∨ c1 6≈
c2 ), and then the literal c1 ≈ c2 is added to our set of constraints. The subset
{c3 ≈ f (c1 ), c4 ≈ f (c2 ), c3 6≈ c4 , c1 ≈ c2 } will then be found unsatisfiable by
congruence closure. In contrast, adding the equalities c1 ≈ c3 and c2 ≈ c4 to our
set will produce a model of the required cardinality.                                       
20                                                                     Andrew Reynolds et al.


   We now state the correctness of our FCC procedure as integrated in the
DPLL(T1 , . . . , Tm ) framework. In the following, we let checkFCC denote the strat-
egy that applies the rules of DPLL(TFCC ) according to Figure 2, with the weak
and strong effort checks described in this section.

Theorem 3 checkFCC is a sound, complete and terminating strategy for every set
of ground clauses F0 .

Proof: Notice that the weak and strong effort methods in this section legally
apply DPLL(T1 , . . . , Tm ) rules, that is, they apply Conflicte only to clauses whose
negated literals imply a contradiction and Learne to clauses that hold in all models.
We follow the three requirements for weak and strong effort checks as described
in Proposition 1.
    To show the first point, the only literals introduced by applications of Learne
(call them LFCC ) are equalities and disequalities between terms occurring in F0 .
Clearly LFCC is finite. To show the second point, the weak and strong effort
methods in this section false only when they apply at least one rule. To show the
third point, strong effort FCC (M, F, C) returns true only when the congruence
closure of M contains k or fewer equivalence classes for all cardS,k ∈ M . In such
states, we are guaranteed that M is satisfiable in FCC.                              



6.3 Establishing Finite Cardinalities

We have now shown that a theory solver for FCC can be integrated into the
DPLL(T1 , . . . , Tm ) architecture with support for eager conflict detection through
the use of weak effort checks. In this section, we show an approach that makes
use of this solver for answering the following problem: given an input F , find the
smallest integer n > 0 such that F ∧ cardS,n is satisfiable.
    A straightforward scheme for solving this problem is the following. First, use
the solver to determine if F ∧cardS,1 is satisfiable, and answer satisfiable if so. If this
is unsatisfiable, use the solver to determine if F ∧ cardS,2 is satisfiable, and so on.
Due to Proposition 3, this process is guaranteed to terminate when F is satisfiable.
A clear disadvantage of this scheme is that, in the absence of conflict analysis, it
diverges when F is unsatisfiable. This section describes an alternative approach
that overcomes this limitation. At a high level, our approach modifies the weak
effort check of the FCC solver by introducing splits on cardinality constraints
(cardS,k ∨ ¬cardS,k ), and deciding upon literals of the cardS,k for the minimal
feasible k. Before formally defining this approach, we discuss a generalization that
is applicable to signatures with multiple uninterpreted sorts.


Extension to Multiple Sorts

Consider the case when our signature Σ contains multiple sorts S1 , . . . , Sn . Given
a set of input clauses F , we wish to determine that either F is unsatisfiable, or
find a tuple (k1 , . . . , kn ) such that F ∧ cardS1 ,k1 ∧ . . . ∧ cardSn ,kn is satisfiable. To
find such a tuple, a challenge is to devise a strategy that is fair. As an illustrative
example, consider the formula (c 6≈ d ∨ ϕ), where c and d are constants of sort S1 ,
Constraint Solving for Finite Model Finding in SMT Solvers                                          21

proc weak effort fc FCC (M, F, C) ≡                                 proc fix(a, M, F, C) ≡
  Let k be the least N s.t. k ≥ n and ¬cardΣ,k 6∈ M                   if a 6∈ LitF
  if fix(cardΣ,k , M, F, C) = false                                      Apply Learne to (a ∨ ¬a)
     return false                                                        return false
  For each Si ∈ Σ, let ki be the least N s.t. ¬cardSi ,ki 6∈ M        else if a 6∈ M
  if fix(cardSi ,ki , M, F, C) = false for a minimal i                   Apply Decide to a
     return false                                                        return false
  if k1 + . . . + kn > k                                              else
     Apply Conflicte to C := (∨n     i=1 cardSi ,ki −1 ∨ ¬cardΣ,k )      return true
     return false
  return weak effort FCC (M, F, C)

Fig. 8 A version of the weak effort check procedure of the FCC solver that fixes the cardinality
of uninterpreted sorts {S1 , . . . , Sn } in signature Σ according to a fair strategy.



and the formula ϕ does not have a model where S2 is interpreted as a finite set.5
Clearly this formula has a model where the cardinality of sorts S1 and S2 are 2
and 1 respectively. However, in the absence of a fair strategy, a naive approach
could search for models of size (1, 1), (1, 2), (1, 3), and so on, ad infinitum.
      To devise a strategy for finite model finding that is fair in the presence of
multiple sorts, we extend the signature Σ of FCC to include signature cardinality
constraints cardΣ,k , constants of sort Bool for each integer k > 0. Let Σ be a
signature containing uninterpreted sorts S1 , . . . , Sn . Let I be a Σ-interpretation
that interprets sort Si ∈ Σ as a set of size ki for 1 ≤ i ≤ n. Then, I satisfies
cardΣ,k if and only if k1 + . . . + kn ≤ k.
      Figure 8 gives an extension of the weak effort check of the FCC solver that
introduces cardinality constraints for the purposes of finding small models. In
detail, we first find the minimal natural number k such that the literal ¬cardΣ,k
does not occur in M . Using the sub-routine fix, if the atom cardΣ,k does not occur
in F , we apply Learne to add (cardΣ,k ∨ ¬cardΣ,k ) to F . If it does occur in F , we
apply Decide to cardΣ,k . We then do the same for each of the uninterpreted sorts
S1 , . . . , Sn in our signature. If these steps do not apply a rule, then M contains
the literals cardΣ,k and ¬cardSi ,` for each 1 ≤ ` < ki , i = 1, . . . , n. We then
check if cardΣ,k is in conflict with the negatively asserted cardinality constraints.
In particular, k1 + . . . + kn > k, we return a conflict of the form (cardS1 ,k1 −1 ∨
. . . ∨ cardSn ,kn −1 ∨ ¬cardΣ,k ), where we write cardSi ,ki −1 to denote a cardinality
constraint when ki > 1 and ⊥ if ki = 1. Otherwise, we apply the original weak
effort check of the FCC solver from Figure 5.
      Let fixed-cardinality checkFCC be the strategy that applies the rules of DPLL(TFCC )
according to Figure 2 where the weak effort check is the one from Figure 8, and the
strong effort check is the one from Figure 7. This strategy maintains the following
invariant.

Proposition 4 Given a signature Σ containing uninterpreted sorts S1 , . . . , Sn ,
for each execution of fixed-cardinality checkFCC ending in hM, F, Ci, either M
contains no decision points, or M is of the form N • cardΣ,k M0 ( • cardS1 ,k1 M1 )
· · · (•cardSm ,km Mm ) N 0 , for some m, 0 ≤ m ≤ n, where N ,M0 , . . ., Mm contain
no decision points, N 0 contains no decision points if m < n, ¬cardΣ,j ≺M cardΣ,k
for each n ≤ j < k, and ¬cardSi ,j ≺M cardSi ,ki for each 1 ≤ i ≤ m, 1 ≤ j < ki .

 5   Observe that ϕ must contain universal quantifiers for this to be the case.
22                                                                     Andrew Reynolds et al.


    In other words, using the strategy fixed-cardinality checkFCC , minimal positive
cardinality literals are the first decision literals in satisfying assignments. This
invariant follows directly from definition of the method given in Figure 8.
Theorem 4 Fixed-cardinality checkFCC is a sound, complete and terminating
strategy for every set of ground clauses F .
Proof: Assume our signature Σ contains uninterpreted sorts S1 , . . . , Sn . Note that
the weak effort check method in Figure 8 extends our original weak effort check
while additionally applying only legal applications of DPLL(T1 , . . . , Tm ) rules,
noting we apply Learne to tautologies of the form (a ∨ ¬a), Conflicte to sets of
literals that are collectively inconsistent according to our extension of FCC, and
Decide to literals whose atom does not occur in M . To show this strategy is sound,
complete, and terminating, we again follow the three requirements for weak and
strong effort checks as given in Proposition 1.
    To show the first point, we must show that the set LFCC of literals introduced
by applications of Learne is finite. For each 1 ≤ i ≤ n, let ki be smallest integer
greater than the number of terms of sort Si in F , and such that the literal ¬cardSi ,ki
does not occur in F . Let k be the smallest integer greater than k1 + . . . + kn ,
and such that the literal ¬cardΣ,k does not occur in F . We claim that the set
of literals introduced by applications of Learne , call them LfFCC        c
                                                                             , are a subset of
the set of all equalities and disequalities between terms from F , the literals of
the form (¬)cardSi ,j where 1 ≤ j < ki for each sort Si , and the literals (¬)cardΣ,j
where n ≤ j < k. First, only equalities and disequalities between terms from F are
introduced by applications of Learne for the same reason as in Theorem 3. Second,
assume by contradiction that a literal (¬)cardSi ,ki is introduced by an application
of Learne . Then, it must be the case that an execution of fixed-cardinality checkFCC
results in a state where ¬cardSi ,ki −1 ∈ M . For this to be the case, ¬cardSi ,ki −1
must be added to M by Propagatee or Backjump. In either case, there must exist
a set of literals l1 , . . . , ln from F such that l1 , . . . , ln |=FCC ¬cardSi ,ki −1 . By our
selection of ki this is a contradiction since there must be at least ki terms of sort
Si in F for this to be the case. Third, for similar reasons, by our selection of
k, a literal (¬)cardΣ,k cannot be introduced by an application of Learne unless
there exists an execution of fixed-cardinality checkFCC resulting in a state where
¬cardSi ,j ∈ M for some Si where j ≥ ki . This cannot be the case for the reasons
mentioned above.
    To show the second point, weak effort check method in Figure 8 returns false
only when it applies a rule.
    To show the third point, the strong effort check of fixed-cardinality checkFCC
is the same as the strong effort check in checkFCC and thus this holds for the same
reason as in the proof of Theorem 3.                                                          

    Combining the results of Theorem 4 and Proposition 4, given as input a set
of ground Σ-clauses F , fixed-cardinality checkFCC will terminate either in (i) a
fail state, establishing that F is unsatisfiable, or (ii) a state hM, F, noi where
M contains cardSi ,ki for each uninterpreted sort Si in Σ, establishing that F is
satisfied by a (finite) model.
    For the remainder of the paper, we assume that Step 1 of our finite model
finding procedure in Figure 3 uses fixed-cardinality checkFCC for finding satisfying
assignments M .
Constraint Solving for Finite Model Finding in SMT Solvers                                        23


7 Constructing Candidate Models

We now focus our attention to Step 2 of procedure FM-SolveH from Figure 3,
which attempts to constructs models M of satisfying assignments M for the input
clause set F . We refer to M as a candidate model. Note that the assignment
M computed by the procedure may contain occurrences of proxy variables a for
quantified formulas ∀x ϕ with the variables in x ranging over uninterpreted or finite
sorts. Recall that those formulas are stored in the input set A in equivalences of
the form a ⇔ ∀x ϕ. The goal of the procedure is to construct M so that it
satisfies not just M but also all its active quantified formulas (those whose proxy
variable a occurs positively in M ). The reason is that such a model witnesses the
T -satisfiability of F ∪ A.
    To discuss the model construction we focus on the variables and the uninter-
preted sorts and function symbols of Σ, since the interpretation of the other sorts
and function symbols is fixed by the theory. We construct a candidate model M by
associating each uninterpreted sort S with a finite set VS of domain elements (i.e.,
S M = VS ). Contrary to other model finding approaches, which use fresh symbols
as domain elements, we use the equivalence classes of M ∗ or, rather, representative
terms for these classes. All interpreted sorts are interpreted in M as usual. We
extend M ∗ to another T -satisfiable set, call it Mc∗ , such that the representative of
each equivalence class of interpreted sort Si in Mc∗ is a value from SiM . Such an
extension is always possible since M is T -satisfiable.
    We then associate each uninterpreted function f of sort S1 × . . . × Sn → S to
a function f M from S1M × · · · × SnM to S M . We construct this function based on
the literals in M that contain f . For instance, if M contains f (c) ≈ b, then f M
is defined so that it maps the interpretation of c to the interpretation of b. Using
those equalities typically produces only a partial definition for f . To complete
it, one can use arbitrary output values for the missing input tuples. We describe
choices for doing so in the following.
    Concretely, we represent candidate Σ-models with the following data structure.
Definition 4 (Defining map) Let f : S1 × · · · × Sn → S be an uninterpreted
function symbol of Σ and let y1 , . . . , yn be distinct fresh variables of respective
sort S1 , . . . , Sn . A defining map for f is a finite set ∆f of well-sorted (directed)
equations of the form f (t1 , . . . , tn ) ≈ v with v ∈ S M and ti ∈ {yi } ∪ SiM for
i = 1, . . . , n, satisfying the following requirements.
1. If s1 ≈ v1 , s2 ≈ v2 ∈ ∆f with s1 6= s2 and s1 and s2 have an mgu σ, then
   (a) σ is non-empty, and
   (b) s1 σ ≈ v ∈ ∆f for some v.
2. f (y1 , . . . , yn ) ≈ v ∈ ∆f for some v.
                             S
A Σ-map is a set ∆ = f ∈Σ f ∆f where each ∆f is a defining map for f .                            
   For the rest of this section, we will use letters y, y1 , y2 , . . . to denote variables
and c, c1 , c2 , . . . to denote constant symbols.
Example 6 The set {f (c1 , y2 ) ≈ c2 , f (y1 , c2 ) ≈ c1 , f (c1 , c2 ) ≈ c3 , f (y1 , y2 ) ≈ c3 } is
a defining map for f . Notice that f (c1 , y2 ) and f (y1 , c2 ) have mgu {y1 7→ c1 , y2 7→
c2 }. As required in point 1, this mgu is non-empty and an equality of the form
f (c1 , c2 ) ≈ v also occurs in this set.                                                          
24                                                                                    Andrew Reynolds et al.


     Input: A satisfying assignment M and a set U ⊆ TM
     Output: A Σ-map ∆
     1. For each uninterpreted function symbol f : S1 × · · · × Sn → S of Σ,
        (a) Let D1 = {f (VM (t1 ), . . . , VM (tn )) ≈ VM (t) | t ∈ TM , t = f (t1 , . . . , tn )}
        (b) Let D2 = {f (t1 , . . . , tn )∀ ≈ VM (t) | t ∈ U, t = f (t1 , . . . , tn )}
        (c) Let ∆f = D1 ∪ D2 and let {ti ≈ vi }0≤i≤m be an arbitrary enumeration of ∆f .
            For all ti ≈ vi , tj ≈ vj with i < j that are unifiable with mgu σ, if ti σ does not
            already occur as a left-hand side in ∆f , add ti σ ≈ vi to ∆f .
        (d) If f (y1 , . . . , yn ) does not occur as a left-hand side in ∆f , add f (y1 , . . . , yn ) ≈ v
            for some arbitrary value v ∈ S M .
                  S
     2. Let ∆ = f ∈Σ ∆f                                                                                  



Fig. 9 Model construction procedure.



By construction of ∆, every flat term, a Σ-term t = f (v1 , . . . , vn ) has exactly one
most specific generalization s among the left-hand sides of the equalities in ∆f ,
where s is a generalization of t if t = sσ for some substitution σ, and s is more
specific than s0 if s0 is a generalization of s. The existence of this generalization
is guaranteed by Point 2 in the definition above; its uniqueness by Point 1. The
value of t in ∆ is the value v in the (unique) equality s ≈ v ∈ ∆f . Thus, a Σ-map
∆ represents a normal model M where each uninterpreted sort S is interpreted as
the term set VS and each uninterpreted function symbol f : S1 × · · · × Sn → S is
interpreted as the function f M mapping every (v1 , . . . , vn ) ∈ S1M × · · · × SnM to
the value of f (v1 , . . . , vn ) in ∆.6


Model Construction Procedure

We now describe a procedure for constructing Σ-maps from satisfying assignments.
In particular, we describe a parametrized method for completing the partial defi-
nitions (of uninterpreted functions) induced by an assignment M .
    Let M be an assignment. Recall that if M is T -satisfiable, it is satisfied by a
normal model, that is, a model that interprets each uninterpreted sort S as the set
VS consisting of a representative term for each equivalence class of (the extension
of) M ’s congruence closure Mc∗ . For each term t, we write VM (t) to denote the
representative of t’s equivalence class in Mc∗ .
    For every uninterpreted function symbol f : S1 × · · · × Sn → S in Σ, we fix
n distinct fresh variables y1 , . . . , yn of respective sort S1 . . . , Sn . To each uninter-
preted sort S, we associate a distinguished ground Σ-term eS , which we will write
as e when S is understood. This ground term guides the selection of default values
of the interpretation of uninterpreted function symbols in our model construction
procedure, based on the following operation. For a ground Σ-term f (t1 , . . . , tn ),
we denote by f (t1 , . . . , tn )∀ the term f (u1 , . . . , un ) where ui = yi if ti = e, and
ui = VM (ti ) otherwise, for i = 1, . . . , n.
  6 More precisely, a Σ-map represents a family of normal models which differ only over the

variables and the interpreted symbols of Σ.
Constraint Solving for Finite Model Finding in SMT Solvers                                                 25


    The non-deterministic procedure described in Figure 9 constructs a Σ-map
from M and a subset U of the set of terms TM occurring in M . The subset U
determines which terms will be used as the basis for default values of function
interpretations. For example, let M be a normal model induced by the defining
map constructed by the procedure in Figure 9 for some U . If f (e, e) ∈ U , then the
default value of f in M is the value of f (e, e) in M. In our implementation of the
procedure, we choose the set U to be the entire set TM , although other choices
are possible.

Example 7 Consider an assignment M with the following constraints

 {c1 ≈ f (c2 , e), c3 ≈ f (c4 , c6 ), c3 ≈ f (e, c4 ), c6 ≈ f (c2 , c5 ), c2 ≈ c5 , c4 ≈ f (e, e)}

where all terms are of uninterpreted sort S. The equivalence classes in the congru-
ence closure of M are

 {c1 , f (c2 , e)}, {c2 , c5 }, {c3 , f (c4 , c6 ), f (e, c4 )}, {c4 , f (e, e)}, {c6 , f (c2 , c5 )}, {e} .

Let VS = {c1 , c2 , c3 , c4 , c6 , e} and U = {f (c2 , e), f (e, c4 ), f (e, e)}. Following the
procedure to construct the defining map ∆f , we let:

          D1       =     {f (c2 , e) ≈ c1 , f (c4 , c6 ) ≈ c3 , f (c2 , c2 ) ≈ c6 , f (e, e) ≈ c4 }
          D2       =     {f (c2 , y2 ) ≈ c1 , f (y1 , c4 ) ≈ c3 , f (y1 , y2 ) ≈ c4 }
          ∆f       =     D1 ∪ D2

Since f (c2 , y2 ) and f (y1 , c4 ) are unifiable with σ = {y1 7→ c2 , y2 7→ c4 }, and
f (c2 , c4 ) is not in ∆f , we add the equality f (c2 , c4 ) ≈ c1 (alternatively, f (c2 , c4 ) ≈
c3 ) to ∆f . Finally, since f (y1 , y2 ) is already in ∆f , this gives us the set

       ∆f      =       { f (c2 , e) ≈ c1 , f (c4 , c6 ) ≈ c3 , f (c2 , c2 ) ≈ c6 , f (e, e) ≈ c4 ,
                         f (c2 , y2 ) ≈ c1 , f (y1 , c4 ) ≈ c3 , f (y1 , y2 ) ≈ c4 , f (c2 , c4 ) ≈ c1 }

which is a complete definition for f . Notice that a different selection of U would
have led to a different construction for ∆f . Let M be the normal model induced by
a ∆ containing ∆f . We have that, for instance, M[[f (c2 , c3 )]] = c1 since f (c2 , y2 ) ≈
c1 ∈ ∆f and f (c2 , y2 ) is the most specific generalization of f (c2 , c3 ) among the
left-hand sides of equalities in ∆f . Similarly, we have that M[[f (c6 , c4 )]] = c3 and
M[[f (c3 , c3 )]] = c4 .                                                                  

Proposition 5 Let M be a T -satisfiable assignment containing only uninterpreted
function symbols over uninterpreted sorts. The set ∆ constructed by the procedure
in Figure 9 is a Σ-map. Moreover, the normal model M represented by ∆ satisfies
M.

Proof: To show that ∆ is a Σ-map, we show that Σf is a defining map for each
function symbol f of Σ. Step 1(c) of the procedure ensures that Point 1(b) of
Definition 4 is met for all pairs of equalities in ∆f , while Step 1(d) makes sure
that Point 2 is met. We prove by contradiction that Point 1(a) of Definition 4
also holds for ∆f . Assume that t ≈ v1 , t ≈ v2 ∈ ∆f with v1 6= v2 . Due to our
construction, both t ≈ v1 and t ≈ v2 are in D1 ∪ D2 . Thus, there must exist terms
t = f (t1 , . . . , tn ) and s = f (s1 , . . . , sn ) in TM such that VM (t1 ) = VM (s1 ), . . .,
26                                                                  Andrew Reynolds et al.


VM (tn ) = VM (sn ) and VM (t) = v1 6= v2 = VM (s), contradicting our assumption
that M is a (consistent) satisfying assignment. Thus, ∆f is a defining map for all
f ∈ Σ, and thus ∆ is a Σ-map.
    For each term f (t1 , . . . , tn ) ∈ TM , we have that f (VM (t1 ), . . . , VM (tn )) ≈
VM (t) ∈ D1 , and thus M(t) = VM (t). Thus, M satisfies all equalities between
pairs of terms in the same equivalence class of Mc∗ . Since Mc∗ is T -satisfiable, we
have that M satisfies all disequalities in Mc∗ as well. Since Mc∗ is a superset of M ,
we have that M satisfies M .                                                              


8 Model-Based Quantifier Instantiation

We now focus our attention on Step 3 of our finite model finding procedure
FM-SolveH from Figure 3. In this step, the procedure FM-SolveH considers quan-
tified formulas in the set:

                         {∀x ϕ | (a ⇔ ∀x ϕ) ∈ A and a ∈ M }                            (2)

Call this set Q. For each formula ∀x ϕ ∈ Q, it uses a quantifier instantiation heuris-
tic H that returns a set of substitutions from x to terms in the set V constructed
in Step 2. A trivial way to implement H is to choose all such possible substitu-
tions. If x is a tuple of n variables each ranging of a sort with k domain elements,
this heuristics will return kn substitutions, which is clearly unfeasible unless both
k and n are rather small. Significantly more scalable heuristics can be adopted
if it is possible to identify sets of substitutions σ yielding instances ϕσ that are
already satisfied by the current candidate model, as these substitutions can be
safely ignored. These heuristics are collectively known as model-based quantifier
instantiation.
     A way to perform model-based quantifier instantiation, as implemented in the
SMT solver Z3 [17], is to use the SMT solver itself as an oracle: a separate copy of
the SMT solver is run on another query to determine whether a candidate model
M satisfies each quantified formula. If it does not, a single instance that is falsified
by M is added to the current clause set F . This approach incurs the performance
overhead of constructing the corresponding query as well as initializing the ora-
cle. Our version of model-based instantiation relies instead upon specialized data
structures when checking candidate models and choosing instantiations, and may
add more than one instantiation per invocation.
     We describe below a model-based quantifier instantiation method that iden-
tifies entire sets of instances as satisfiable in M without actually generating and
checking those instances individually [30]. The main idea is to determine the sat-
isfiability in M of some instance ϕσ of a quantified formula ∀x ϕ ∈ Q, generalize
ϕσ to a set J of instances equisatisfiable with ϕσ in M, and then look for further
instances only outside that set. The set J is computed by identifying which vari-
ables of ϕ actually matter in determining the satisfiability of ϕσ. Technically, for
each ψ = ∀x ϕ, substitution σ = {x 7→ v} into V, and instance ϕ0 = ϕσ of ψ, if
M |= ϕ0 we compute a partition of x into x1 and x2 and a corresponding partition
of v into v1 and v2 such that M |= ∀x2 ϕ{x1 7→ v1 }; similarly, if M 6|= ¬ϕ0 we
compute a partition such that M 6|= ∀x2 ¬ϕ{x1 7→ v1 }. In either case, we then
know that all instances of ϕ{x1 7→ v1 } over V are equisatisfiable with ϕ0 in M,
Constraint Solving for Finite Model Finding in SMT Solvers                                       27

proc eval(M, t, σ) ≡
  match t with
    | f (t1 , . . . , tn ) →
                          for j = 1, . . . , n
                            let (vj , Xj ) = eval(M, tj , σ)
                          choose a critical argumentSsubset C of {1, . . . , n}
                          return (f M (v1 , . . . , vn ), i∈C Xi )
     |x →       return (σ(x), {x})

Fig. 10 The eval procedure for candidate model M. Returns a pair (v, S) where (tσ)M = v,
and S is a subset of the domain of σ that was used to compute this interpretation.



and so it is enough to consider just ϕ0 in lieu of all them. We will refer to the ele-
ments of x1 above as a set of critical variables for ϕ (under σ)—although strictly
speaking this is a misnomer as we do not insist that x1 be minimal.


8.1 Generalizing Evaluations

We have developed a general procedure that, given the Σ-map of a candidate
model M, a term t, and a substitution σ over t’s variables, computes and returns
both the value of tσ in M and a set of critical variables for σ. This procedure
effectively extends to quantifier-free formulas as well by treating them as Boolean
terms—which evaluate to either true or false in a Σ-interpretation depending on
whether they are satisfied by the model or not.
    The procedure, called eval, is defined recursively over its input term and is
sketched in Figure 10. For uniformity, we assume that function symbols and logical
operators are all in prefix form.
    When evaluating a non-variable term f (t1 , . . . , tn ), eval determines a criti-
cal argument subset C for it. This is a subset of {1, . . . , n} such that the term
f (s1 , . . . , sn ) denotes a constant function in M where each si is the value com-
puted by eval for ti if i ∈ C, and is a unique variable otherwise. If f is a logical
symbol, the choice of C is dictated by the symbol’s semantics. For instance, for
≈(t1 , t2 ), C is {1, 2}; for ∨(t1 , . . . , tn ), it is {1, . . . , n} if the disjunction evaluates
to false; otherwise, we it chooses {i} for some i where ti evaluates to true. If f is a
function symbol of Σ, eval computes C by first constructing a custom index data
structure for interpreting applications of f to values. The key feature of this data
structure is that it uses information on the sets X1 , . . . Xn to choose an evaluation
order for the arguments of f . For example, given the term t = f (g(x, y, z), v2 , h(x)),
say that eval computes the values v1 , v2 , v3 and the critical variable sets {x, y, z},
∅, {x} for the three arguments of f , respectively. With those sets, it will use the
evaluation order (2, 3, 1) for those arguments—meaning that the second argument
is evaluated first, then the third, etc. Using the index data structure, it will first
determine if f (x1 , v2 , x3 ) has a constant interpretation in M for all x1 , x3 . If so,
then the evaluation of t depends on none of its variables, and the returned set of
critical variables for t will be ∅. Otherwise, if f (x1 , v2 , v3 ) has a constant interpre-
tation in M , then the evaluation of t depends on {x}, or else it depends on the
entire variable set {x, y, z}.
    The next example gives more details on the whole process of using eval to
generalize a ground instance to a set of ground instances equisatisfiable with it in
a given model.
28                                                                   Andrew Reynolds et al.


Example 8 Let Q = {∀x1 x2 f (x1 ) ≈ g(x2 , b) ∨ h(x2 , x1 ) 6≈ b}, where all terms are
of some sort S. Consider a candidate model M induced by a Σ-map containing
the following definitions :
                    ∆g = {g(a, a) ≈ c, g(y1 , b) ≈ a, g(y1 , y2 ) ≈ b}
                    ∆f = {f (b) ≈ b, f (y1 ) ≈ a}
                    ∆h = {h(y1 , y2 ) ≈ b}

Suppose VS = {a, b, c}. The table below shows the bottom-up calculation per-
formed by eval on the formula ϕ = f (x1 ) ≈ g(x2 , b) ∨ h(x2 , x1 ) 6≈ b with M above
and σ = {x1 7→ a, x2 7→ a}.

                      input                     output        critical arg. subset
                         x1                     (a, {x1 })
                         x2                     (a, {x2 })
                          b                     (b, ∅)                  ∅
                       f (x1 )                  (a, {x1 })             {1}
                     g(x2 , b)                  (a, ∅)                 {2}
                    h(x2 , x1 )                 (b, ∅)                  ∅
                f (x1 ) ≈ g(x2 , b)             (true, {x1 })         {1, 2}
                  h(x2 , x1 ) 6≈ b              (false, ∅)            {1, 2}
       f (x1 ) ≈ g(x2 , b) ∨ h(x2 , x1 ) 6≈ b   (true, {x1 })          {1}


For most entries in the table the evaluation is straightforward. For a more in-
teresting case, consider the evaluation of g(x2 , b). First, the arguments of g are
evaluated, respectively to (a, {x2 }) and (b, ∅). Using an indexing data structure
built from ∆g for the evaluation order (2, 1), we determine that g(x2 , b) has con-
stant value a for all x2 . Hence we return an empty set of critical variables for
g(x2 , b).
    Similarly, the fact that eval returns (true, {x1 }) for the original input formula ϕ
and the substitution σ = {x1 7→ a, x2 7→ a} means that we were able to determine
that all ground instances of ϕ{x1 7→ a} = (f (a) ≈ g(x2 , b) ∨ h(x2 , a) 6≈ b), not
just the instance ϕσ, are satisfied in M. We can then use this information in
FM-SolveH to completely avoid generating and checking those instances.                 


8.2 A Model-Based Instantiation Heuristic

For any given quantified formula ψ, the eval procedure allows us to identify a set
of instances over V that can be represented by a single one, as far as satisfiability
in the candidate model M is concerned. In this subsection, we present a quantifier
instantiation heuristic that generates a set I of instances that together represent
all instances of ψ over V that are falsified by M. This kind of exhaustiveness is
crucial because it allows us to conclude that M |= ψ by just checking that I is
empty.
    The heuristic is implemented by a procedure that relies on eval for computing
the set I above, or rather, a set of substitutions for generating the elements of
I from ψ. The procedure is fairly unsophisticated and quite conservative in its
choice of representative instances, which makes it very simple to implement and
Constraint Solving for Finite Model Finding in SMT Solvers                                    29

proc Hm (M, ∀x ϕ) ≡
  Ix := ∅; t := vmin
  do
    (v, {xi1 , . . . , xim }) := eval(M, ϕ, {x 7→ t})
    if v = false then Ix := Ix ∪ {{x 7→ t}}
    t := nexti (t) where i = n + 1 − max{0, i1 , . . . , im }
  while t 6= vmin
  return Ix

Fig. 11 A model-based instantiation heuristic Hm , where x = (x1 , . . . , xn ).


prove correct. Its main shortcoming is that it does not take full advantage of the
information provided by eval, and so may end up producing more representative
instances than needed in many cases.
    Let ψ = ∀x ϕ ∈ Q with x = (x1 , . . . , xn ), where Q is the set defined in (2).
For i = 1, . . . , n, let Si be the sort of xi and let Vx = VS1 × · · · × VSn . For each
S ∈ {S1 , . . . , Sn }, let <S be an arbitrary total ordering over the values VS of sort
S. Let < be the lexicographic extension of these orderings to the tuples in Vx and
observe that Vx is totally ordered by <. We write vmin to denote the minimum
of Vx with respect to this ordering.
    For every v = (v1 , . . . , vn ) ∈ Vx Let nexti (v) denote the smallest tuple u with
respect to < such that v(j) <Sj u(j) for some 1 ≤ j ≤ n + 1 − i, if such a tuple
exists, and denote vmin otherwise (including when i > n).7 For instance, with
n = 3, S1 = S2 = S3 and VS1 = {a, b} with a <S1 b, we have that next1 (a, a, a) =
(a, a, b), next2 (a, a, a) = (a, b, a), next2 (a, b, a) = (b, a, a), next3 (a, a, a) = (b, a, a),
and next2 (b, b, a) = vmin = (a, a, a). Note that except in the case that nexti (v) is
vmin , we have that v < nexti (v).
    Our instantiation heuristic Hm is given in Figure 11. It takes in a quantifier-
free formula ϕ with variables x and returns a set Ix of substitutions σ for x such
that M 6|= ϕσ. At each execution of its loop the procedure implicitly determines
with eval a set I of instances of ϕ that are equisatisfiable with ϕ{x 7→ v} in M,
where v is the tuple stored in the program variable t. The next value tnext for t is
a greater tuple chosen to maintain the invariant that all the tuples between t and
tnext generate instances of ϕ that are in I. To see that, it suffices to observe that
these tuples differ from t only in positions that correspond to non-critical variables
of ϕ, namely those before position i where xi is the first critical variable of ϕ in
the enumeration x1 , . . . , xn . This observation is the main argument in the proof
of the following result.
Lemma 3 Let v0 , . . . , vm be all values successively taken by variable t at the
beginning of the loop in Hm . Let vmax be the maximum element of Vx . Then for
all j = 1, . . . , m,
1. vj−1 < vj ,
2. for all u with vj−1 ≤ u < vj , M |= ϕ{x 7→ u} iff M |= ϕ{x 7→ vj−1 },
3. for all u with vm ≤ u ≤ vmax , M |= ϕ{x 7→ u} iff M |= ϕ{x 7→ vm }.
Proof: (Sketch) The first statement is immediate since for all j = 1 . . . m, we have
vj = nextk (vj−1 ) for some k and vj 6= vmin . To show the second statement for a
j, assume vj = nextk (vj−1 ) for some k. For each u where vj−1 ≤ u < vj , we have
  7   Where v(j) and u(j) are the j-th component of v and u, respectively.
30                                                              Andrew Reynolds et al.


that u(`) = vj−1 (`) for all ` ≥ k. For all ` < k, the eval procedure determined
that the variable x` was not a critical variable for ϕ. Since u and vi−1 vary on
only these variables, we have M |= ϕ{x 7→ u} iff M |= ϕ{x 7→ vj−1 }. The third
statement holds for similar reasons as the second.                             
Theorem 5 The set Ix returned by Hm (M, ϕ, x) is empty if and only if M |=
∀x ϕ.
Proof: Thanks to the previous lemma, if there is an instance of ϕ that is falsified
by M, then Hm will consider at least one vi for which ϕ{x 7→ vi } evaluates to
false, and hence it will return at least one instance. Conversely, if all instances of
ϕ are satisfied by M, then all instances of ϕ considered by Hm evaluate to true,
and hence it will return no instances.                                              
    We remark that, for the model finding purposes of procedure FM-SolveH , there
is no need for the procedure Hm to compute the full set Ix once it contains at least
one substitution. Any non-empty subset would suffice to trigger a (more incremen-
tal) revision of the current candidate model M. That said, our current implemen-
tation does compute the whole set and adds all the corresponding instances to the
clause set F before computing another model for it. Our experiments show that
computing and using one substitution at a time is worse for overall performance
than computing and using the full set Ix .
Example 9 Consider the quantified formula ∀x1 x2 ϕ and candidate model M from
Example 8. Assume that a <S b <S c. The result of running Hm on M, ϕ and
x = (x1 , x2 ) is summarized in the table below. Each row in the column shows the
value of variable t at the beginning of the loop in Hm , the result of computing
eval, the substitution (if any) added to Ix on that iteration, and the computation
of the next tuple of terms nexti (t).
      Iteration   t    eval(M, ϕ, {x 7→ t})    Add to Ix           i nexti (t)
          1     (a, a)      (true, {x1 })           ∅              2 (b, a)
          2     (b, a)     (false, {x1 })   {x1 7→ b, x2 7→ a}     2 (c, a)
          3     (c, a)      (true, {x1 })           ∅              2 (a, a)
We begin by setting t to vmin = (a, a). As demonstrated in Example 8, we have
that eval(M, ϕ, {x1 7→ a, x2 7→ a}) returns the pair (true, {x1 }). The first com-
ponent of this pair indicates that M[[ϕ{x1 7→ a, x2 7→ a}]] = true, and hence
we do not add this substitution to Ix . The second component of this pair indi-
cates moreover that this interpretation did not depend on the value of x2 , and
hence (ϕ{x1 7→ a, x2 7→ v})M = true for all values of v. Thus, we need not
consider t = (a, b) or t = (a, c). Instead, on the second iteration, we consider
next2 (a, a) = (b, a). Subsequently, eval(M, ϕ, {x1 7→ b, x2 7→ a}) returns the pair
(false, {x1 }). This indicates that (ϕ{x1 7→ b, x2 7→ v})M = false for all values of
v. We add the substitution {x1 7→ b, x2 7→ a} to Ix only. Finally, on the third
iteration, eval(M, ϕ, {x1 7→ c, x2 7→ a}) returns the pair (true, {x1 }); we add no
substitutions to Ix , and the loop terminates. Overall, Hm returns the singleton
set of substitutions {{x1 7→ b, x2 7→ a}}.                                        


8.3 Enhancement: Heuristic Instantiation

Modern SMT solvers rely on syntatic heuristic instantiation methods for finding
unsatisfiable instances for quantified formulas [13, 25, 31]. In these methods, quan-
Constraint Solving for Finite Model Finding in SMT Solvers                                  31


tified formulas are instantiated based on pattern matching. For instance, the solver
may choose to instantiate the quantified formula ∀x P (f (x)) ⇒ Q(x) based on the
substitution {x 7→ c} when P (f (c)) is a ground term occurring in its current satis-
fying assignment. This technique is often referred to as E-matching. We found that
heuristic instantiation-based E-matching can be helpful in the context of our finite
model finding approach as well, because the instances it generates are helpful in
quickly ruling out candidate models that are obviously spurious.
     A quantifier instantiation heuristic H, such as the model-based one from the
previous section, can be enhanced by applying heuristic instantiation with a higher
priority. That is, we may consider a modified quantifier instantiation heuristic that
first computes the set of instances Ix returned by E-matching for a quantified for-
mula ∀x ϕ. If this set is non-empty, it returns Ix ; otherwise it returns the instances
from the original heuristic H on ∀x ϕ.
     In practice, we have found that it is best to apply heuristic quantifier instan-
tiation after finding a satisfying assignment with a bounded number of equiva-
lence classes. By waiting to apply quantifier instantiation until after a satisfying
assignment of this form can be constructed, we can avoid pitfalls common to E-
matching. In particular, having a finite cardinality for uninterpreted sorts ensures
that only a finite number of terms are unique up to congruence, thus ensuring
that E-matching, which is non-terminating in general, will eventually return in-
stances that rule out the current upper bound on cardinality, or terminate with no
instances. We discuss the impact of heuristic instantiation further in Section 9.2.


9 Results

We implemented all features mentioned in this paper inside cvc4 [2], a state-
of-the-art SMT solver based on the DPLL(T1 , . . . , Tm ) architecture. This section
presents experimental results on this implementation.8 We separate this section
into two sets of experiments, the first to evaluate the relative effectiveness of
various strategies for the FCC solver, and the second to evaluate the model finder’s
overall performance when used with quantified formulas. For the second set of
experiments, we compare our model finder against state-of-the-art SMT solvers
and automated theorem provers.


9.1 FCC Solver Evaluation

We first examine the effectiveness of approach to handling ground problems in
the theory of EUF with finite cardinality constraints (FCC). In this section, all
experiments were run on a Linux machine with an 8-core 2.60GHz Intel R Xeon R
E5-2670 processor with 16GB of RAM.
    We tested various configurations of the FCC solver, starting with the default
configuration cvc4+f, which contains the region-based enhancements described
in Section 6.2, where conflicting states are reported by using clique lemmas of the
form (¬distinct(t1 , . . . , tk+1 ) ∨ ¬cardS,k ). We also tested a configuration, cvc4+fe,
which reports conflict clauses of the form (l1 ∨ . . . ∨ ln ∨ ¬cardS,k ), where l1 , . . . , ln
 8   Details can be found at http://cs.uiowa.edu/~ajreynol/TPLP-fmf.
32                                                                         Andrew Reynolds et al.

      100                                        100


         10                                         10
      CVC4+f




                                                 CVC4+f
               1                                          1


         .1                                         .1


                   .1      1       10     100                 .1       1        10      100
                        CVC4+f-r                                   CVC4+mace

Fig. 12 Results for randomly generated benchmarks. Runtimes are on a log-log scale.


are equalities and disequalities that entail distinct(t1 , . . . , tk+1 ). This configuration
avoids the introduction of new equalities into the search (contained in the expan-
sion of distinct), but has the disadvantage that it can generate different conflict
clauses for essentially the same clique. Additionally, we considered configuration
cvc4+f-r, which differs from cvc4+f only in that regionalizations have always
just one region per sort S, encompassing the entire disequality graph for S.
    We also evaluated the MACE-style approach to finite model finding described
in related work [24], which we implemented in the configuration cvc4+mace. In
the case of a set of ground clauses F involving a single sort, if TF is the set of
all terms in F and c1 , . . . , ck are fresh constants serving as domain constants, this
configuration checks the satisfiability of
                                                 ^
                F ∧ distinct(c1 , . . . , ck ) ∧   (t ≈ c1 ∨ . . . ∨ t ≈ ck )             (3)
                                                t∈TF

for k = 1, 2, . . . until (3) is found satisfiable for some k. Then, the minimal model
size for F is k. A major and well-known shortcoming of this approach is the in-
troduction of unwanted symmetries in the problem due to the use of domain con-
stants. cvc4 can address this issue to some extent since it incorporates symmetry
breaking techniques directly at the ground EUF level [12].
     We considered satisfiable benchmarks encoding randomly generated graph col-
oring problems and consisting of a conjunction of disequalities between constants
of a single sort. In particular, we considered a total of 793 non-trivial problems
containing between 20 and 50 unique constants and between 100 and 900 dise-
qualities, and measured the time it takes each configuration to find a model of
minimum size, with a 60 second timeout. For the benchmarks we tested, the con-
figuration cvc4+f solves the most benchmarks within the time limit: 723. The
configuration cvc4+f was an order of magnitude faster than cvc4+fe on most
benchmarks, with the latter only being able to solve 309 benchmarks within the
time limit. This strongly suggests that generating explanations for cliques in con-
flict lemmas involving cardinality constraints is not an effective approach in this
scheme.
     Figure 12 compares the performance of the configuration cvc4+f against
cvc4+f-r and cvc4+mace. The second scatter plot clearly shows that the cvc4+f
configuration generally requires less time and solves more benchmarks (723 vs.
664) than cvc4+f-r, confirming the usefulness of a region-based approach for
clique detection. The third scatter plot compares cvc4+f against cvc4+mace.
The latter configuration was able to solve only 617 benchmarks and generally
Constraint Solving for Finite Model Finding in SMT Solvers                                33


performed poorly on benchmarks with larger model size. The median model size
of the 123 benchmarks solved only by cvc4+f was 17, whereas the median size
of the 13 benchmarks solved only by cvc4+mace was 10. This suggests that for
larger cardinalities cvc4+mace suffers from the model symmetries created by the
introduction of domain constants, something that cvc4+f avoids.



9.2 Finite Model Finder Evaluation

We provide results on cvc4 with finite model finding for three sets of benchmarks
coming from different formal methods applications, including verification and au-
tomated theorem proving. We will refer to various configurations of cvc4 based on
the features they include. Configuration cvc4+f uses the finite model finding tech-
niques described earlier. Additionally, configurations containing m in their suffix
use the model-based quantifier instantiation heuristic described in Section 8, and
configurations with i use heuristic instantiation, which can be paired with finite
model finding configurations as described in Section 8.3.
    Experiments from Section ?? were run on a Linux machine with an 8-core
2.60GHz Intel R Xeon R E5-2670 processor. All others were run on a Linux machine
with an 8-core 3.20GHz Intel R Xeon R E5-1650 processor with 16GB of RAM.


Intel benchmarks

We evaluated the overall effectiveness of cvc4’s finite model finder for quantified
SMT formulas taken from verification conditions generated by DVF [18], a tool
used at Intel for verifying properties of security protocols and design architectures,
among other applications. Both unsatisfiable and satisfiable benchmarks were pro-
duced, the latter by manually removing necessary assumptions from verification
conditions. All benchmarks contain quantifiers, although only over uninterpreted
sorts, and span a wide range of theories, including linear integer arithmetic, arrays,
EUF, and algebraic datatypes.
    For comparison we looked at the SMT solvers cvc3 [4] (version 2.4.1)9 , Yices [14]
(version 1.0.32), and z3 [11] (version 4.1). We did not consider traditional theorem
provers and finite model finders because they do not have built-in support for
the theories in our benchmark set. All these solvers use E-matching as a heuristic
method for answering unsatisfiable in the presence of universally quantified for-
mulas. Z3 additionally relies on model-based quantifier instantiation techniques to
establish satisfiability in the presence of quantified formulas [17].
    The results, separated into unsatisfiable and satisfiable instances, are shown in
Figure 13 for five classes of benchmarks and a timeout of 600 seconds per bench-
mark. The first two classes, refcount and german, represent verification condi-
tions for systems described in [18]; benchmarks in the third are taken from [37];
the last two classes are verification problems internal to Intel.
    For the satisfiable benchmarks, our finite model finder is the only tool capa-
ble of solving any instance in the last three benchmark classes. In fact, cvc4+f
  9 cvc3 is the predecessor of cvc4. The latter was developed from scratch, and does not have

any code in common with cvc3.
34                                                                        Andrew Reynolds et al.

     Sat          german       refcount         agree              apg              bmk
                    (45)          (6)            (42)              (19)             (37)
                 #     time    #    time     #        time    #        time      #       time
     cvc3         0      0.0   0      0.0     0         0.0    0         0.0      0        0.0
     yices        2      0.0   0      0.0     0         0.0    0         0.0      0        0.0
     z3          45      1.1   1      7.0     0         0.0    0         0.0      0        0.0
     cvc4+i       2      0.0   0      0.0     0         0.0    0         0.0      0        0.0
     cvc4+f      45      0.3   6      0.1    42       15.5    18      200.0      36   1201.5
     cvc4+f-r    45      0.3   6      0.1    42       18.6    15      364.3      34     720.4
     cvc4+fi     45      0.4   6      0.1    42       14.2    19      492.8      36     831.0
     cvc4+fm     45      0.3   6      0.1    42       23.6    19      210.2      37     375.1
     cvc4+fmi    45      0.3   6      0.1    42       16.4    19      221.1      37     176.8
     Unsat       german        refcount          agree             apg              bmk
                   (145)          (40)           (488)            (304)             (244)
                 #     time    #     time     #       time     #       time      #       time
     cvc3       145      0.4   40      0.2   457        6.8   267       77.0    229       76.2
     yices      145      1.8   40      7.0   488    1475.4    304       35.8    244       25.3
     z3         145      1.9   40      0.9   488       10.6   304       12.2    244        5.3
     cvc4+i     145      0.1   40      0.2   484        6.8   304       11.2    244        2.9
     cvc4+f     145      0.8   40      0.4   476    3782.1    298    2252.5     242    1507.0
     cvc4+f-r   145      0.4   40      0.2   475    1574.3    294    3836.0     240    1930.5
     cvc4+fi    145      0.7   40      0.1   488     188.7    302     342.0     244     660.3
     cvc4+fm    145      0.4   40      0.3   471    5018.2    300    1122.7     242     834.1
     cvc4+fmi   145      0.3   40      0.1   488     185.9    302     339.8     244     668.5

Fig. 13 Number of solved satisfiable and unsatisfiable Intel (DVF) benchmarks and cumula-
tive time for solved benchmarks. All times are in seconds.




is able to solve all but two, and most of them in less than a second. When ex-
tended to include techniques for model-based quantifier instantiation (configura-
tions cvc4+fm and cvc4+fmi), we are able to solve all satisfiable benchmarks
within the timeout. By comparing cvc4+f against cvc4+f-r, we see that the
region-based approach for recognizing cliques is beneficial, particularly for the
harder classes where the latter configuration solves fewer benchmarks within the
timeout. The model sizes found for these benchmarks were relatively small; only a
handful had a model with sort cardinalities larger than 4. To our knowledge, our
model finder is the only tool capable of solving these benchmarks.
    For the unsatisfiable benchmarks, Yices and Z3 can solve all of them, with
Z3 being much faster in some cases. We observe that cvc4 with finite model
finding is orders of magnitude slower than the SMT solvers on these benchmarks.
This is, however, to be expected since it is geared towards finding models, and
applies exhaustive instantiation with increasingly large cardinality bounds, which
normally delays the discovery that the problem is unsatisfiable regardless of those
bounds.
    However, we found that each unsatisfiable problem can be solved by either cvc4
or cvc4+fmi, and in less than 3s. Additionally, configuration cvc4+fmi solves all
unsatisfiable benchmarks within 900s, suggesting that cvc4’s model finder makes
consistent progress towards answering unsatisfiable on provable DVF verification
conditions. From the perspective of verification tools, the results here seem promis-
ing. A common strategy for handling a verification condition would be to first use
an SMT solver hoping that it can quickly find it unsatisfiable with E-matching
techniques; and then resort to finite model finding if needed to either answer un-
satisfiable, or produce a model representing a concrete counterexample for the
verification condition.
Constraint Solving for Finite Model Finding in SMT Solvers                                       35

                                 Unsat                                        Sat
              EPR      NEQ      SEQ       PEQ      Total    EPR     NEQ     SEQ     PEQ     Total
              (920)   (2008)   (7682)    (1796)   (12406)   (388)   (618)   (340)   (612)   (1958)
  z3           840     1406     3366       656     6268      345     261     175     160      941
  cvc3         596      910     3091       648     5245       24      0       8       0       32
  iprover      888     1786     3346       310     6330      384     434     106     156     1080
  iprover+f     -        -        -         -        -       378     555     224     268     1425
  paradox       -        -        -         -        -       343     534     201     372     1450
  cvc4+i       809     1346     3277      668      6100       21      1       8       0       30
  cvc4+f       736      900     1261       531     3428      329     441     178     242     1190
  cvc4+fm      725      942     1315       419     3401      329     448     214     286     1277
  cvc4+fi      733      994     1594       457     3778      329     422     178     231     1160
  cvc4+fmi     748      997     1594       459     3798      327     416     190     232     1165


Fig. 14 Number of solved TPTP benchmarks. All experiments were run with a 300 second
timeout.



TPTP benchmarks

We considered benchmarks from a recent version of the TPTP library [34] (5.4.0),
a widely-used library from the automated theorem proving community. The bench-
marks from this library involve no theory reasoning other than equality, and are
composed mostly of quantified formulas.
     We compared cvc4 (version 1.2) against other SMT solvers including z3 (ver-
sion 4.3) and cvc3 (version 2.4.1), as well as various automated theorem provers
and model finders for first order logic, including Paradox [10] and iProver [21]
(version 0.99). Paradox is a MACE-style model finder that uses preprocessing op-
timizations such as sort inference and clause splitting, among others, and then
encodes to SAT the original problem together with increasingly looser constraints
on the size of the model. iProver is an automated theorem prover based in the
Inst-Gen calculus that can also run in finite model finding mode (iprover+f). In
that mode, it incrementally bounds model sizes in a manner similar to MACE-style
model finding. However, it encodes the whole problem into the EPR fragment,10
for which it is a decision procedure. Since these two tools are limited to classical
first-order logic with equality, we considered only the unsorted first-order bench-
marks of TPTP.
     Figure 14 shows results for benchmarks from the TPTP library that are known
to be satisfiable or unsatisfiable. All experiments were run with a 300 second time-
out per benchmark. The benchmarks were placed into (exactly one) category based
on its logical and syntactic characteristics, where EPR includes benchmarks that
reside in the effectively propositional fragment, NEQ are benchmarks that do not
contain any equality reasoning, SEQ are benchmarks containing some equality, and
PEQ are benchmarks containing only pure equality. Both configurations iprover
and iprover+f used scheduling strategies that iProver incorporated for CASC 24,
a competition for automated theorem provers, meaning that multiple configura-
tions of this solver were run sequentially. The latter of these configurations, as well
as the configuration paradox were solely run on the satisfiable benchmarks from
this set. All configurations of cvc4 with finite model finding used sort inference
techniques as described in [32], which is capable of treating unsorted inputs as
multi-sorted based on their structure. Sort inference techniques are known to be
useful for this set of benchmarks, and are used in most competitive ATP systems,
including Paradox and iProver.

 10 This fragment of first-order logic consists of all formulas of the form ∃x.∀y.ϕ, where ϕ is

quantifier-free and contains no function symbols.
36                                                                                                       Andrew Reynolds et al.



                      1e+12                                                            1e+12
     # of Instances




                                                                      # of Instances
                      1e+11                                                            1e+11
                      1e+10            cvc4+fm                                         1e+10            cvc4+f
                       1e+9                                                            1e+9
                       1e+8                                                            1e+8
                       1e+7                                                            1e+7
                       1e+6                                                            1e+6
                       1e+5                                                            1e+5
                       1e+4                                                            1e+4
                       1000                                                            1000
                        100                                                              100
                           800   900     1000    1100   1200   1300                         800   900     1000   1100   1200   1300
                                       # Solved                                                         # Solved


Fig. 15 Satisfiable TPTP problems with (cvc4+fm) and without (cvc4+f) model-based
instantiation. A point (x, y) on this graph says the configuration solves x benchmarks each
having at most y ground instances of quantified formulas.



    For satisfiable benchmarks, cvc4’s model finder with exhaustive instantiation
(cvc4+f) solves 1190 benchmarks. Using model-based quantifier instantiation,
that number goes up to 1277 (configuration cvc4+fm). Using heuristic instanti-
ation (cvc4+fmi) in addition to model-based instantiation led to finding fewer
satisfiable benchmarks, solving 1165 within the timeout, suggesting that the solver
becomes overloaded with the large number of instantiations produced by exhaus-
tive instantiation.
    While cvc4 solves more than z3, which finds 941 satisfiable benchmarks, our
model finder still trails the overall performance of the other model finders on these
problems. Paradox was the overall best solver, finding 1450 satisfiable benchmarks.
We attribute this to the fact that we have not implemented advanced preprocessing
techniques, such as clause splitting, that have been shown to be critical for finding
finite models of TPTP benchmarks. Nevertheless, cvc4’s model finder solves more
satisfiable benchmarks (214) than Paradox for classes of problems having some
equality reasoning (SEQ). Collectively, some configuration of cvc4 with finite
model finding was able to solve 52 satisfiable benchmarks that paradox was not
able to solve, and 36 satisfiable benchmarks that iprover+f was not able to solve.
    Figure 14 also shows results for unsatisfiable problems. Although these results
are not comparable to those achieved by state-of-the-art theorem provers, such as
Vampire and E [22, 33], we note that iprover solves the most benchmarks, 6330.
Here, cvc4+fmi was the best configuration of cvc4 with finite model finding,
solving 3781 within the timeout. While finite model finding configurations solved
considerably fewer than using heuristic instantiation alone, some configuration
of cvc4 with finite model finding solves 144 unsatisfiable benchmarks that were
unable to be solved by any other solver in these experiments, including iProver
and z3.
    To further evaluate the impact of model-based quantifier instantiation on our
model finder, we recorded statistics on the domain size of quantified formulas in
benchmarks solved by its various configurations. We measured the total number
of possible ground instances for all quantified formulas in the smallest model for
that benchmark (a quantified formula over n variables each with domain size k
has kn instances). For a problem with d total instances, the configuration cvc4+f
Constraint Solving for Finite Model Finding in SMT Solvers                                 37

 Sat            Arr    FFT     FTA      Hoare     NSS     QEp     SN     TSq     TSf     Total
 z3              2      19      24         47       7      47      1      17      8       172
 cvc3            0       9       0         0        0      0       0      8       0        17
 cvc4+i          0       9       0         0        0      0       0      8       0        17
 cvc4+f         35      145    177        162      56      85     12     57      90       819
 cvc4+fm        33      141     173       155      43      86     12      54     89       786
 cvc4+fi        36      146     172       162     61      86      12      55     93       823
 cvc4+fmi       36     147      174      162       61      83     12      56     93      824
 Unsat         Arr     FFT     FTA      Hoare     NSS     QEp      SN    TSq     TSf     Total
 z3             178     277     917       549      108     325     241    620    291      3506
 cvc3          321     296     1124      607       105     297     207    643     227     3827
 cvc4+i         307     288     990       563     117     360     242    708      283    3858
 cvc4+f         165     106     451       239      44      131     88     442     151     1817
 cvc4+fm        132     92      442       238      26      160     88     430     128     1736
 cvc4+fi        172     185     589       383      47      222     112    585     196     2491
 cvc4+fmi       168     186     589       379      47      222     112    584     196     2483

Fig. 16 Number of solved satisfiable and unsatisfiable Isabelle benchmarks for various classes
within a 300 second timeout.


must explicitly generate these d instances, while a model-based configuration may
avoid doing so.
    The graph on the right hand side of Figure 15 shows that cvc4+f was only
able to solve 13 problems having more than 100K instances, the maximum having
around 5.6 million instances. On the other hand, cvc4+fm was capable of solving
123 problems having more than 100K instances, with the largest having more than
2.8 trillion instances. This indicates that the model-based instantiation approach
improves the scalability of our model finder, and allows it to solve benchmarks
where exhaustive instantiation is clearly infeasible. Model finders such as Paradox
have other ways of handling the explosion in the number of instances, namely by
minimizing the number of variables per clause. Coupling these techniques with
model-based techniques could then lead to additional improvements in scalability.
Since techniques for reducing variables in clauses rely on introducing new symbols
into the problem, we have found that they have a negative impact on performance
for several classes of benchmarks, and thus are disabled by default in cvc4.

Isabelle benchmarks

Recent work has shown that SMT solvers are effective at discharging proof obliga-
tions for Isabelle, a generic proof assistant [27]. The performance of these solvers
can benefit from an encoding that makes use of theories [7]. We considered a set
of 13,041 benchmarks corresponding to both provable and unprovable proof goals,
corresponding to a superset of those discussed in [7]. Most benchmarks in this set
contain quantifiers, and a significant portion contain integer arithmetic. For many
of them, the quantification is limited to the uninterpreted sorts, thus making our
finite model finding approach applicable.
    The results are shown in Figure 16. For satisfiable benchmarks, all config-
urations of cvc4’s model finder find more satisfiable problems than z3, which
finds only 172 of them overall. The model-based quantifier instantiation technique
from Section 8 (configuration cvc4+fm) was less effective than naive instantiation
(configuration cvc4+f) which solves 819, suggesting that model-based techniques
were not effective at minimizing the number of instantiations for this set of bench-
marks. Using heuristic E-matching noticeably improved the search for models,
38                                                                    Andrew Reynolds et al.


as configuration cvc4+fi solves 823 satisfiable benchmarks. Using both model-
based instantiation and heuristic instantiation, configuration cvc4+fmi, found
more satisfiable problems (824) than any other configuration.
   For unsatisfiable problems, cvc4+i is the overall winner, solving 3,858, which
was more than both z3 and cvc3 which solved 3,506 and 3,827 respectively.
Configurations of cvc4 with finite model finding generally solves less unsatisfiable
benchmarks, but is orthogonal to other solvers and configurations. In these exper-
iments, 309 unsatisfiable benchmarks that cvc3 cannot solve are solved by at least
one configuration of cvc4 with finite model finding. Similarly, a configuration of
cvc4 with finite model finding solves 429 unsatisfiable benchmarks that z3 cannot,
and 168 that cvc4+i cannot.



10 Conclusion

We developed a general approach for finite model finding in SMT that is efficient
for many classes of problems that are of practical interest to formal methods
applications. Experimental evidence from an implementation of these methods in
the SMT solver cvc4 shows that our approach is effective in practice at solving
many classes of benchmarks, including verification conditions from industry, and
benchmarks from automated theorem proving libraries. The implementation is
highly competitive with respect to other SMT solvers and to automated theorem
provers.
    In ongoing work, we plan to extend our approach to the problem of finding
models of formulas with quantifiers ranging over built-in domains such as the
integers and inductive datatypes. We are also investigating the use of cvc4 as
a backend to interactive proof assistants such as Isabelle and Coq, where small
counterexamples to conjectures are often helpful to the user.

Acknowledgements We would like to thank Amit Goel and Sava Krstić for their valuable
contributions to this work, Sascha Böhme for proving the Isabelle benchmarks, and François
Bobot for his help in writing a TPTP front end for CVC4.



References

 1. Baader, F., Nipkow, T.: Term Rewriting and All That. Cambridge University Press (1998)
 2. Barrett, C., Conway, C., Deters, M., Hadarean, L., Jovanovic, D., King, T., Reynolds, A.,
    Tinelli, C.: CVC4. In: Proceedings of CAV’11, LNCS, vol. 6806, pp. 171–177. Springer
    (2011)
 3. Barrett, C., Nieuwenhuis, R., Oliveras, A., Tinelli, C.: Splitting on demand in SAT modulo
    theories. In: Proceedings of LPAR’06, LNCS, vol. 4246, pp. 512–526. Springer (2006)
 4. Barrett, C., Tinelli, C.: CVC3. In: W. Damm, H. Hermanns (eds.) Proceedings of the
    19th International Conference on Computer Aided Verification (CAV ’07), Lecture Notes
    in Computer Science, vol. 4590, pp. 298–302. Springer-Verlag (2007). Berlin, Germany
 5. Baumgartner, P., Bax, J., Waldmann, U.: Finite quantification in hierarchic theorem prov-
    ing. In: Automated Reasoning - 7th International Joint Conference, IJCAR 2014, Held
    as Part of the Vienna Summer of Logic, VSL 2014, Vienna, Austria, July 19-22, 2014.
    Proceedings, pp. 152–167 (2014)
 6. Baumgartner, P., Fuchs, A., de Nivelle, H., Tinelli, C.: Computing finite models by reduc-
    tion to function-free clause logic. J. Applied Logic 7(1), 58–74 (2009)
Constraint Solving for Finite Model Finding in SMT Solvers                                        39


 7. Blanchette, J.C., Böhme, S., Paulson, L.C.: Extending Sledgehammer with SMT solvers.
    In: N. Børner, V. Sofronie-Stokkermans (eds.) Automated Deduction, Lecture Notes in
    Computer Science, vol. 6803, pp. 116–130. Springer (2011)
 8. Blanchette, J.C., Nipkow, T.: Nitpick: A counterexample generator for higher-order logic
    based on a relational model finder. In: M. Kaufmann, L.C. Paulson (eds.) ITP 2010,
    LNCS, vol. 6172, pp. 131–146. Springer (2010)
 9. Bruttomesso, R., Cimatti, A., Franzén, A., Griggio, A., Sebastiani, R.: Delayed theory
    combination vs. Nelson-Oppen for satisfiability modulo theories: a comparative analysis.
    AMAI 55(1-2), 63–99 (2009)
10. Claessen, K., Sörensson, N.: New techniques that improve MACE-style finite model build-
    ing. In: CADE-19 Workshop: Model Computation – Principles, Algorithms, Applications,
    pp. 11–27 (2003)
11. De Moura, L., Bjørner, N.: Z3: an efficient SMT solver. In: Proceedings of the Theory
    and practice of software, 14th international conference on Tools and algorithms for the
    construction and analysis of systems, TACAS’08/ETAPS’08, pp. 337–340. Springer-Verlag,
    Berlin, Heidelberg (2008)
12. Déharbe, D., Fontaine, P., Merz, S., Paleo, B.W.: Exploiting symmetry in SMT problems.
    In: Proceedings of CADE-23, LNCS, vol. 6803, pp. 222–236. Springer (2011)
13. Detlefs, D., Nelson, G., Saxe, J.B.: Simplify: A theorem prover for program checking. Tech.
    rep., J. ACM (2003)
14. Dutertre, B., De Moura, L.: The yices smt solver. Tool paper at http://yices. csl. sri.
    com/tool-paper. pdf 2, 2 (2006)
15. Garey, M.R., Johnson, D.S., Stockmeyer, L.: Some simplified np-complete problems. In:
    Proceedings of the Sixth Annual ACM Symposium on Theory of Computing, STOC ’74,
    pp. 47–63. ACM, New York, NY, USA (1974)
16. Ge, Y., Barrett, C., Tinelli, C.: Solving quantified verification conditions using satisfiability
    modulo theories. Annals of Mathematics and Artificial Intelligence 55(1-2), 101–122 (2009)
17. Ge, Y., de Moura, L.: Complete instantiation for quantified formulas in satisfiability mod-
    ulo theories. In: Proceedings of CAV’09, LNCS, vol. 5643, pp. 306–320. Springer (2009)
18. Goel, A., Krstić, S., Leslie, R., Tuttle, M.: SMT-based system verification with DVF. In:
    Proceedings of SMT’12 (2012)
19. Ihlemann, C., Jacobs, S., Sofronie-Stokkermans, V.: On local reasoning in verification. In:
    C.R. Ramakrishnan, J. Rehof (eds.) TACAS 2008, pp. 265–281. Springer Berlin Heidelberg,
    Berlin, Heidelberg (2008)
20. Jovanovic, D., Barrett, C.: Being careful about theory combination. Formal Methods in
    System Design 42(1), 67–90 (2013)
21. Korovin, K.: iProver – an instantiation-based theorem prover for first-order logic. In:
    Proceedings of IJCAR’08, LNCS, vol. 5195, pp. 292–298. Springer (2008)
22. Kovács, L., Voronkov, A.: First-order theorem proving and vampire. In: Computer Aided
    Verification - 25th International Conference, CAV 2013, Saint Petersburg, Russia, July
    13-19, 2013. Proceedings, pp. 1–35 (2013)
23. Krstić, S., Goel, A.: Architecting solvers for SAT modulo theories: Nelson-Oppen with
    DPLL. In: Proceeding of FroCoS’07, LNCS, vol. 4720, pp. 1–27. Springer (2007)
24. McCune, W.: A Davis–Putnam program and its application to finite first-order model
    search: Quasigroup existence problems. Tech. rep., Argonne National Laboratory (1994)
25. de Moura, L., Bjørner, N.: Efficient E-Matching for SMT solvers. In: Automated Deduction
    - CADE-21, 21st International Conference on Automated Deduction, Bremen, Germany,
    July 17-20, 2007, Proceedings, Lecture Notes in Computer Science, vol. 4603, pp. 183–198.
    Springer (2007)
26. Nieuwenhuis, R., Oliveras, A., Tinelli, C.: Solving SAT and SAT Modulo Theories: from
    an Abstract Davis-Putnam-Logemann-Loveland Procedure to DPLL(T). Journal of the
    ACM 53(6), 937–977 (2006)
27. Paulson, L.C., Wenzel, M.: Isabelle/HOL: a proof assistant for higher-order logic, vol.
    2283. Springer (2002)
28. Reger, G., Suda, M., Voronkov, A.: Finding finite models in multi-sorted first-order logic.
    In: Theory and Applications of Satisfiability Testing - SAT 2016 - 19th International
    Conference, Bordeaux, France, July 5-8, 2016, Proceedings, pp. 323–341 (2016)
29. Reynolds, A., Tinelli, C., Goel, A., Krstić, S.: Finite model finding in SMT. In: N. Shary-
    gina, H. Veith (eds.) Computer Aided Verification, Lecture Notes in Computer Science,
    vol. 8044, pp. 640–655. Springer Berlin Heidelberg (2013)
40                                                                      Andrew Reynolds et al.


30. Reynolds, A., Tinelli, C., Goel, A., Krstić, S., Deters, M., Barrett, C.: Quantifier instan-
    tiation techniques for finite model finding in SMT. In: M.P. Bonacina (ed.) Automated
    Deduction CADE-24, Lecture Notes in Computer Science, vol. 7898, pp. 377–391. Springer
    Berlin Heidelberg (2013)
31. Reynolds, A., Tinelli, C., de Moura, L.M.: Finding conflicting instances of quantified for-
    mulas in SMT. In: FMCAD, pp. 195–202. IEEE (2014). DOI 10.1109/FMCAD.2014.
    6987613
32. Reynolds, A.J.: Finite model finding in satisfiability modulo theories. Ph.D. thesis, The
    University of Iowa (2013)
33. Schulz, S.: E–a brainiac theorem prover. Ai Communications 15(2, 3), 111–126 (2002)
34. Sutcliffe, G.: The TPTP Problem Library and Associated Infrastructure: The FOF and
    CNF Parts, v3.5.0. Journal of Automated Reasoning 43(4), 337–362 (2009)
35. Tinelli, C., Harandi, M.T.: A new correctness proof of the Nelson–Oppen combination
    procedure. In: Proceeding of FroCoS’96, Applied Logic, pp. 103–120. Kluwer Academic
    Publishers (1996)
36. Torlak, E., Jackson, D.: Kodkod: a relational model finder. In: Proceedings of TACAS’07,
    LNCS, vol. 4424, pp. 632–647. Springer (2007)
37. Tuttle, M.R., Goel, A.: Protocol proof checking simplified with SMT. In: Proceedings of
    NCA’12, pp. 195–202. IEEE Computer Society (2012)
38. Zhang, J., Zhang, H.: SEM: a system for enumerating models. In: Proceedings of IJCAI’95,
    pp. 298–303 (1995)
