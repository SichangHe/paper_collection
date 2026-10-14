                                                Bounded Synthesis of Reactive Programs⋆

                                                       Carsten Gerstacker, Felix Klein, and Bernd Finkbeiner

                                                       Reactive Systems Group, Saarland University, Germany
                                                    {gerstacker,fklein,finkbeiner}@cs.uni-saarland.de
arXiv:1807.09047v1 [cs.FL] 24 Jul 2018




                                                 Abstract. Most algorithms for the synthesis of reactive systems focus
                                                 on the construction of finite-state machines rather than actual programs.
                                                 This often leads to badly structured, unreadable code. In this paper,
                                                 we present a bounded synthesis approach that automatically constructs,
                                                 from a given specification in linear-time temporal logic (LTL), a program
                                                 in Madhusudan’s simple imperative language for reactive programs. We
                                                 develop and compare two principal approaches for the reduction of the
                                                 synthesis problem to a Boolean constraint satisfaction problem. The first
                                                 reduction is based on a generalization of bounded synthesis to two-way
                                                 alternating automata, the second reduction is based on a direct encoding
                                                 of the program syntax in the constraint system. We report on preliminary
                                                 experience with a prototype implementation, which indicates that the
                                                 direct encoding outperforms the automata approach.


                                         1     Introduction
                                         In reactive synthesis, we automatically construct a reactive system, such as the
                                         controller of a cyberphysical system, that is guaranteed to satisfy a given specifi-
                                         cation. The study of the synthesis problem, known also as Church’s problem [2],
                                         dates back to the 1950s and has, especially in recent years, attracted a lot of
                                         attention from both theory and practice. There is a growing number of both
                                         tools (cf. [3,4,5,6]) and success stories, such as the synthesis of an arbiter for the
                                         AMBA AHB bus, an open industrial standard for the on-chip communication
                                         and management of functional blocks in system-on-a-chip (SoC) designs [7].
                                             The practical use of the synthesis tools has, however, so far been limited. A
                                         serious criticism is that, compared to code produced by a human programmer,
                                         the code produced by the currently available synthesis tools is usually badly
                                         structured and, quite simply, unreadable. The reason is that the synthesis tools
                                         do not actually synthesize programs, but rather much simpler computational
                                         models, such as finite state machines. As a result, the synthesized code lacks
                                         control structures, such as while loops, and symbolic operations on program
                                         variables: everything is flattened out into a huge state graph.
                                             A significant step towards better implementations has been the bounded syn-
                                         thesis [8] approach, where the number of states of the synthesized implementa-
                                         tion is bounded by a constant. This can be used to construct finite state machines
                                         ⋆
                                             Some of the results of the paper are part of the first author’s Bachelor thesis [1].
                                             Supported by the European Research Council (ERC) Grant OSARES (No. 683300)
                                             and by the Saarbrücken Graduate School of Computer Science.
with a minimal number of states. Bounded synthesis has also been extended with
other structural measures, such as the number of cycles [9]. Bounded synthesis
reduces the synthesis problem to a constraint satisfaction problem: the existence
of an implementation of bounded size is expressed as a set of Boolean constraints,
which can subsequently be solved by a SAT or QBF solver [10]. Bounded syn-
thesis has proven highly effective in finding finite state machines with a simple
structure. However, existing methods based on bounded synthesis do not make
use of syntactical program constructs like loops or variables. The situation is dif-
ferent in the synthesis of sequential programs, where programs have long been
studied as the target of synthesis algorithms [11,12,13,14,15]. In particular, in
syntax-guided synthesis [11], the output of the synthesis algorithm is constrained
to programs whose syntax conforms to a given grammar. A first theoretical step
in this direction for reactive systems was proposed by Madhusudan [16]. Mad-
husudan defines a small imperative programming language and shows that the
existence of a program in this language with a fixed set of Boolean variables is
decidable. For this purpose, the specification is translated into an alternating
two-way tree automaton that reads in the syntax tree of a program, simulates
its behavior, and accepts all programs whose behavior satisfies the specification.
Because the set of variables is fixed in advance, the approach can be used to syn-
thesize programs with a minimal number of variables. However, unlike bounded
synthesis, this does not lead to programs that are minimial in other ways, such
as the number of states or cycles.

    In this paper, we present the first bounded synthesis approach for reactive
programs. As in standard bounded synthesis [8], we reduce the synthesis problem
to a constraint satisfaction problem. The challenge is to find a constraint system
that encodes the existence of a program that satisfies the specification, and that,
at the same time, can be solved efficiently. We develop and compare two princi-
pal methods. The first method is inspired by Madhusudan’s construction in that
we also build a two-way tree automaton that recognizes the correct programs.
The key difficulty here is that the standard bounded synthesis approach does
not work with two-way automata, let alone the alternating two-way automata
produced in Madhusudan’s construction. We first give a new automata con-
struction that produces universal, instead of alternating, two-way automata. We
then generalize bounded synthesis to work on arbitrary graphs, including the run
graphs of two-way automata. The second method follows the original bounded
synthesis approach more closely. Rather than simulating the execution of the
program in the automaton, we encode the existence of both the program and its
run graph in the constraint system. The correctness of the synthesized program
is ensured, as in the original approach, with a universal (one-way) automaton
derived from the specification. Both methods allow us to compute programs that
satisfy the given specification and that are minimal in measures such as the size
of the program. The two approaches compute the exact same reactive programs,
but differ, conceptually, in how much work is done via an automata-theoretic
construction vs. in the constraint solving. In the first approach, the verification
of the synthesized program is done by the automaton, in the second approach
by the constraint solving. Which approach is better? While no method has a
clear theoretical advantage over the other, our experiments with a prototype
implementation indicate a strong advantage for the second approach.


2     Preliminaries
We denote the Boolean values {0, 1} by B. The set of non-negative integers is
denoted by N and for a ∈ N the set {0, 1, . . . , a} is denoted by [a]. An alphabet
Σ is a non-empty finite set of symbols. The elements of an alphabet are called
letters. A infinite word α over an alphabet Σ is a infinite concatenation α =
α0 α1 . . . of letters of Σ. The set of infinite words is denoted by Σ ω . With αn ∈ Σ
we access the n-th letter of the word. For an infinite word α ∈ Σ ω we define
with Inf(α) the set of states that appear infinitely often in α. A subset of Σ ω is
a language over infinite words.

2.1    Implementations
Implementations are arbitrary input-deterministic reactive systems. We fix the
finite input and output alphabet I and O, respectively. A Mealy machine is a
tuple M = (I, O, M, m0 , τ, o) where I is an input-alphabet, O is an output-
alphabet, M is a finite set of states, m0 ∈ M is an initial state, τ : M × 2I → M
is a transition function and o : M × 2I → 2O is an output function. A system
path over an infinite input sequence αI is the sequence m0 m1 . . . ∈ M ω such
that ∀i ∈ N : τ (mi , αIi ) = mi+1 . The thereby produced infinite output sequence
is defined as αO = αO        O           O ω
                         0 α1 . . . ∈ (2 ) , where every element has to match the
output function, i.e., ∀i ∈ N : αi = o(mi , αIi ). We say a Mealy machine M
                                        O

produces a word α = (αI0 ∪ αO             I   O
                                    0 )(α1 ∪ α1 ) . . . ∈ (2
                                                             I∪O ω
                                                                ) , iff the output αO is
                       I
produced for input α . We refer to the set of all producible words as the language
of M, denoted by L(M) ⊆ (2I∪O )ω .
    A more succinct representation of implementations are programs. The pro-
grams we are working with are imperative reactive programs over a fixed set
of Boolean variables B and fixed input/output aritys NI /NO . Our approach
builds upon [16] and we use the same syntax and semantics. Let b ∈ B be a
variable and both b~I and b~O be vectors over multiple variables of size NI and
NO , respectively. The syntax is defined with the following grammar
 hstmti ::= hstmti ; hstmti | skip | b := hexpri | input b~I | output b~O
          | if (hexpri) then {hstmti} else {hstmti} | while(hexpri){hstmti}
 hexpri ::= b | tt | ff | (hexpri ∨ hexpri) | (¬ hexpri)
The semantics are the natural one. Our programs start with an initial variable
valuation we define to be 0 for all variables. The program then interacts with the
environment by the means of input and output statements, i.e., for a vector over
Boolean variables ~b the statement “input ~b” takes an input in {0, 1}NI from the
environment and updates the values of ~b. The statement “output ~b” outputs
the values stored in ~b, that is an output in {0, 1}NO . Therefor a program with
                                                     while
         while(tt) {
           input (r1 , r2 );                  tt                   ;

           if(r1 ) then {
                                                   input r1r2               ;
              r2 = ff
           } else {                                                if           output r1r2

              skip
                                                       r1                  then
           };
           output (r1 , r2 )                                    assignr2           skip

         }
                                                       ff




          Fig. 1. Example-Code           Fig. 2. Example-Program-Tree


input/output arity NI /NO requires at least max(NI , NO ) many variables, i.e.,
|B| ≥ max(NI , NO ). Between two input and output statements the program
can internally do any number of steps and manipulate the variables using as-
signments, conditionals and loops. Note that programs are input-deterministic,
i.e., a program maps an infinite input sequence αI ∈ ({0, 1}NI )ω to an infinite
output sequence αO ∈ ({0, 1}NO )ω and we say a program can produce a word
α = (αI0 αO     I O
           0 )(α1 α1 ) . . . ∈ ({0, 1}       ) , iff it maps αI to αO . We define the
                                       NI +NO ω

language of T , denoted by L(T ), as the set of all producible words. We assume
programs to alternate between input and output statements.
     We represent our programs as Σ-labeled binary trees, i.e., a tuple (T, τ ) where
T ⊆ {L, R}∗ is a finite and prefix closed set of nodes and τ : T → Σ is a labeling
function. Based on the defined syntax, we fix the set of labels as

            ΣP = {¬, ∨, ; , if , then, while} ∪ B ∪ {assignb | b ∈ B}
               ∪{input ~b | ~b ∈ B NI } ∪ {output ~b | ~b ∈ B NO }.

We refer to ΣP -labeled binary trees as program trees. If a node has only one
subtree we define it to be a the left subtree. Note that our program trees do
therefore not contain nodes with only a right subtree. For example, Fig. 1 depicts
an arbitrary program and Fig. 2 the corresponding program tree.
   We express the current variable valuation as a function s : B → B. We update
variables ~b ∈ B n with new values ~v ∈ Bn using the following notation:
                                     (
                                       vi   if bi = x, for all i
                      s[~b/~v ](x) =
                                       s(x) otherwise


2.2   Automata

We define alternating automata over infinite words as usual, that is a tuple
A = (Σ, Q, q0 , δ, Acc) where Σ is a finite alphabet, Q is a finite set of states,
q0 ∈ Q is an initial state, δ : Q × Σ → B+ (Q) is a transition function and
Acc ⊆ Qω is an acceptance condition.
                         condition BÜCHI(F ) on a set of states F ⊆ Q is de-
    The Büchi acceptance
fined as BÜCHI(F ) = q0 q1 . . . ∈ Qω | Inf(α) ∩ F 6= ∅ and F is called the set
of accepting states. The co-Büchi acceptance condition      COBÜCHI(F ) on a set
of states F ⊆ Q is defined as COBÜCHI(F ) = q0 q1 . . . ∈ Qω | Inf(α) ∩ F = ∅ ,
                                                  

where F is called the set of rejecting states. To express combinations of Büchi
and co-Büchi expressions we use the Streett acceptance condition. Formally,
STREETT F on a set of tuples F = {(Ai , Gi )}i∈[k] ⊆ Q × Q is defined as
STREETT(F ) = q0 q1 . . . ∈ Qω | ∀i ∈ [k] : Inf(α) ∩ Ai 6= ∅ → Inf(α) ∩ Gi 6= ∅ .
A run with a Streett condition is intuitively accepted, iff for all tuples (Ai , Gi ),
the set Ai is hit only finitely often or the set Gi is hit infinitely often.
    Two-way alternating tree automata are tuple (Σ, P, p0 , δL , δR , δLR , δ∅ , Acc),
where Σ is an input alphabet, P is a finite set of states, p0 ∈ P is an initial
state, Acc is an acceptance condition, and δ are transition functions of type
δS : P ×Σ ×(S ∪{D}) → B+ (P ×(S ∪{U })), for S ∈ {L, R, LR, ∅}. We introduce
µ : T × {L, R, U } → T × {L, R, D} as a function to map states and directions to
move in, to the reached states and the matching incoming directions.
                 µ(t, L) = (t · L, D)            µ(t.L, U ) = (t, L)
                 µ(t, R) = (t · R, D)            µ(t.R, U ) = (t, R)
    We consider specifications given in linear time-temporal logic (LTL). Such
specifications can be translated into non-deterministic Büchi automata or dually
into an universal co-Büchi automata as shown in [17]. For an arbitrary specifi-
cation we denote by Aspec and Aspec the corresponding non-deterministic Büchi
and universal co-Büchi automaton, respectively.


3    Automata Construction
We have already argued that programs, as a more succinct representation of
implementations, are highly desirable. However, in contrast to Mealy machines,
which only dependent on the current state and map an input to a corresponding
output, in programs such a direct mapping is not possible. Instead, programs
need to be simulated, variables to be altered, expressions to be evaluated and an
output statement to be traversed until we produce the corresponding output to
the received input. These steps not only depend on the current position in the
program but additionally also on the valuation of all variables.
    We build upon Madhusudans reactive program synthesis approach [16] were
program synthesis is solved by means of two-way alternating Büchi tree automata
walking up and down over program trees while keeping track of the current valu-
ation and the state of a given Büchi specification automaton, which is simulated
by the input/output produced by traversing the program tree. The automaton
accepts a program tree whenever the simulated specification automaton accepts
the provided input/output. The constructed automaton, we will further refer
to as A, is intersected with two other constructed automata which enforce syn-
tactically correctness and reactivity of the synthesized program, respectively.
Then a reactive and syntactically correct program is synthesized by means of an
emptiness check of the obtained automaton, involving an exponential blowup to
eliminate two-wayness and alternation.
3.1   Two-way Universal Co-Büchi Tree Automaton

We construct a two-way non-deterministic Büchi tree automaton B that is equiv-
alent to A by using deterministic evaluation of Boolean expressions. We construct
B without an exponential blowup in the state space. We then complement B into
a two-way universal co-Büchi tree automaton convenient for the bounded syn-
thesis approach.
     The two-way alternating Büchi tree automaton A uses universal choices
only in relation to Boolean expression evaluation. For example, for if, while
and assignb -statements a Boolean evaluation is needed. In this cases it non-
deterministically guesses whether the expression evaluates to 0 or 1 and then
universally sends one copy into the Boolean expression, which evaluates to true
iff the expression evaluates to the expected value, and one copy to continue the
corresponding normal execution. The copy evaluating the Boolean expression
walks only downwards and since the subtree corresponding to the Boolean ex-
pression is finite, this copy terminates to either true or f alse after finitely many
steps. Instead of using both non-deterministic and universal choices, we evaluate
the Boolean subtree deterministically in finitely many steps and then continue
the normal execution based on the result of the evaluation.
     Note that we not only remove all universal choices but additionally all un-
necessary sources of non-determinism. Therefore, besides traversing input- and
output-labels, that introduce unavoidable non-determinism, our program simu-
lation is deterministic.
     Our automaton B with the set of states

                     Pexec = S × Qspec × BNI × {inp, out} × B
                   B
                  Pexpr = S × Qspec × BNI × {inp, out} × {⊤, ⊥}

                                  P B = Pexpr
                                         B
                                              ∪ Pexec
and initial state pB 0 = (s0 , q0 , i0 , inp, 0), is defined with the transitions shown in
Fig. 3, where s ∈ S is a variable valuation, q ∈ Qspec the state of the simulated
specification automaton, i ∈ BNI the last received input, m ∈ {inp, out} a flag
to ensure alternation between inputs and outputs, r ∈ {⊤, ⊥} the result of a
Boolean evaluation and t ∈ {0, 1} a flag for the Büchi condition, which ensures
that the specification automaton is simulated for infinite steps and is only set to
1 for a single simulation step after an output statement. We express states corre-
                                                                                      B
sponding to Boolean evaluations and program execution as (s, q, i, m, r) ∈ Pexpr
                       B
and (s, q, i, m, t) ∈ Pexec , respectively.
    The notation reads as follows: If the automaton enters a node with one of the
black incoming edges, it can move in the direction of the black outgoing edges,
while updating his state corresponding to the annotated update expression, de-
picted by an enclosing rectangle. Additionally, the automaton needs to fulfill the
conditions annotated to the edges it traverses. To express non-determinism we
use sets of update expressions, such that each expression represents one possible
successor. All state values not contained in the update expression stay the same,
except t which is set to 0. When changing from Boolean evaluation to program
execution, we copy s, q, i, m and vice versa.
   The set of accepting states is defined as

                         F B = (s, q, i, m, 1) | q ∈ Fspec
                              


    A formal construction of B is given in Appendix A.1. Note that B behaves
similar to A during normal execution and that only Boolean evaluation was
altered. Therefore, the state spaces of the automata only differ in the states
corresponding to Boolean evaluation and especially the sets of accepting states
F A and F B are equivalent. Therefore, we can prove the equivalence by showing
that both automata visit the same sequences of accepting states and thus accept
the same program trees.

Theorem 1 (Appendix A.1). L(A) = L(B)

    We now complement the constructed two-way non-deterministic Büchi au-
tomaton into a two-way universal co-Büchi automaton. From this point onwards,
we refer with B to the two-way universal co-Büchi automaton.
    Since A accepts precisely the programs that fail the specification and in-
teract infinitely often with the environment, the complement now only accepts
programs that do satisfy the specification or interact finitely often with the envi-
ronment. We fix the remaining misbehavior by enforcing syntactical correctness
and reactiveness.


3.2   Guarantee Syntactical Correctness

Due to the fact that B was designed to correctly simulate programs of our de-
fined syntax and transitions were only defined for syntax-valid statements, B
implicitly rejects programs that are syntactically invalid. But such programs are
only then rejected when their syntactically incorrect statements are traversed
in the simulation, therefore B does not check for syntactically correct subtrees
that are unreachable. It is now arguable whether the syntax check is necessary
in practice. One could expect programs to be syntactically correct in total and
this expectation is in general well-argued. On the other hand, we do perform
bounded synthesis, i.e., we search for implementations with a bound on the im-
plementation size and then increment this bound until a valid implementation is
found. It is easy to see that programs with unreachable parts can be represented
by smaller programs with the same behavior simply by removing unreachable
statements. Therefore, with an incremental search one first finds the smallest
and thus syntactically correct programs.


3.3   Guarantee Reactiveness

It now remains to guarantee reactiveness of the programs accepted by B. For
that purpose, we introduce a two-way universal Büchi automaton Breactive , which
           tt     r→⊤                ff    r→⊥                   b      r → s[b]



                                                                r=⊤

                  ∨                   ∨                     ∨

                                                                     r=⊥




                            ¬                    ¬        r→r



                      r=⊥

while             while                          assign b             assign b     s[b] → r

                            r=⊤




if                              if                                     if



           then                           then                                     then

                                r=⊤                      r=⊥

     m = inp

           input ~b       {s[~b] → val,
                                    ~ i → val,
                                           ~ m → out | val
                                                        ~ ∈ BNI }



     m = out

          output ~b       {q → q ′ , m → inp, t → 1 | q ′ ∈ δ(q, i, s[~b])}




           skip                 ;                    ;                  ;




        Fig. 3. Semantics of the constructed two-way automata
only accepts program trees that are reactive. This automaton is designed with
the exact same states and transitions as B but with another acceptance condi-
tion. The intersection of B and Breactive then yields a two-way universal Streett
automaton B ′ . We construct Breactive with the set of accepting states:
                        B
                                 
                      Freactive = (s, q, i, m, 1) | ∀s, q, i, m
Breactive accepts a program tree, iff it produces infinitely many outputs on all
possible executions. Due to the alternation between input and output statements
the program reacts infinitely often with its environment, i.e., it is reactive.
                                                                           ′
   Formally, B ′ is the tuple (ΣP , P B , δL
                                           B B B
                                             , δR , δLR , δ∅B , STREETT(F B )), where
                            ′
                         F B = (F B , ∅), (P B , Freactive
                                                     B
                               
                                                                ) .
Lemma 1. L(B ′ ) = L(B) ∩ L(Breactive )
Proof. Besides the acceptance condition, all three automata are equivalent. The
tuples of the Streett condition (F B , ∅) and (P B , Freactive
                                                      B
                                                               ) express the co-Büchi
and Büchi condition of B and Breactive , respectively.                             ⊓
                                                                                    ⊔
    We capture the complete construction by the following theorem.
Theorem 2. Let B be a finite set of Boolean variables and ϕ a specification
given as LTL-formula. The constructed two-way universal Streett automaton B ′
accepts program trees over B that satisfy the specification.


4    Bounded Synthesis
In this section, we generalize the bounded synthesis approach towards arbitrary
universal automata and then apply it to the constructed two-way automaton to
synthesize bounded programs.
     We fix Q to be a finite set of states. A run graph is a tuple G = (V, v0 , E, f ),
where V is a finite set of vertices, v0 is an initial vertex, E ⊆ V × V is a set of
directed edges and f : V → Q is a labeling function. A path π = π0 π1 . . . ∈ V ω
is contained in G, denoted by π ∈ G, iff ∀i ∈ N : (πi , πi+1 ) ∈ E and π0 = v0 ,
i.e., a path in the graph starting in the initial vertex. We denote with f (π) =
f (π0 )f (π1 ) . . . ∈ Qω the application of f on every node in the path, i.e., a
projection to an infinite sequence of states. We call a vertex v unreachable,
iff there exists no path π ∈ G containing v. Let Acc ⊆ Qω be an acceptance
condition. We say G satisfies Acc, iff every path of G satisfies the acceptance
condition, i.e., ∀π ∈ G : f (π) ∈ Acc.
     Run graphs are used to express all possible runs of a universal automaton
on some implementation. This is usually done for universal word automata on
Mealy machines, but we need a generalized version to later utilize it for two-
way universal tree automata on program trees. Let Σ = 2I∪O . We define a run
          A
graph GM      = (V, v0 , E, f ) of a universal word automaton A = (Σ, Q, q0 , δ, Acc)
on a Mealy machine M = (I, O, M, m0 , τ, o) as an instantiation of the given
definition, where
 – V = Q × M,
 – v0 = (q0 , m0 ),
 – E = (q, m), (q ′ , m′ ) | ∃in ∈ 2I , out ∈ 2O :
                          

   τ (m, in) = m′ ∧ o(m, in) = out ∧ q ′ ∈ δ(q, in ∪ out) and
 – f (q, m) = q.
    Since the run graph contains all infinite runs of A on words producible by
                                           A                        A
M, A accepts M, iff all runs in GM            are accepting, i.e., GM  satisfies Acc.
    For some bound c ∈ N we denote {0, 1, . . . , c} by Dc . For a run graph G =
(V, v0 , E, f ) and a bound c ∈ N a c-bounded annotation function on G is a
function λ : V → Dc . An annotation comparison relation of arity n is a family
of relations ⊲ = (⊲0 , ⊲1 , . . . , ⊲n−1 ) ∈ (2Q×Dc ×Dc )n . We refer to ⊲i ⊆ Q × Dc × Dc
as basic comparison relations for i ∈ [n]. We denote the arity with | ⊲ | = n.
We write λ(v) ⊲i λ(v ′ ) for (f (v), λ(v), λ(v ′ )) ∈ ⊲i and for comparison relations of
arity | ⊲ | = 1 we omit the index.
    We say a path π ∈ G satisfies a comparison relation ⊲ with arity | ⊲ | = n,
denoted by π |= ⊲, iff for every basic comparison relation there exists an an-
notation function that annotates every node with a value such that the anno-
tated number for all consecutive nodes in the path satisfy the basic comparison
relation, i.e., ∀i ∈ [n] : ∃λ : ∀j ∈ N : λ(πj ) ⊲i λ(πj+1 ). For an acceptance con-
dition Acc ⊆ Qω we say a comparison relation ⊲ expresses Acc, iff all paths
in G satisfy the relation if and only if the path satisfies the acceptance con-
dition, i.e., ∀π ∈ G : π |= ⊲ ↔ f (π) ∈ Acc. A c-bounded annotation func-
tion λ on G = (V, v0 , E, f ) is valid for a basic annotation comparison relation
⊲ ⊆ Q × Dc × Dc , iff for all reachable v, v ′ ∈ V : (v, v ′ ) ∈ E → λ(v) ⊲ λ(v ′ ).
    We use the following annotation comparison relations to express Büchi, co-
Büchi and Streett acceptance conditions.
 – Let F ⊆ Q and Acc = BÜCHI(F ). Then ⊲F  B is defined as
                                 (
                       F    ′      true           if f (v) ∈ F
                 λ(v) ⊲B λ(v ) =             ′
                                   λ(v) > λ(v ) if f (v) 6∈ F

 – Let F ⊆ Q and Acc = CO-BÜCHI(F ). Then ⊲F    C is defined as
                                 (
                            ′      λ(v) > λ(v ′ ) if f (v) ∈ F
                 λ(v) ⊲F
                       C λ(v ) =
                                   λ(v) ≥ λ(v ′ ) if f (v) 6∈ F

 – Let F = {(Ai , Gi )}i∈[k] ⊆ 2Q×Q and Acc = STREETT(F ). Then ⊲F      S =
     F,0 F,1           F,k−1
   (⊲S , ⊲S , . . . , ⊲S     ) is defined as
                                   
                                   true
                                                   if f (v) ∈ Gi
                      F,i    ′                  ′
           λ(v) ⊲S λ(v ) = λ(v) > λ(v ) if f (v) ∈ Ai ∧ f (v) 6∈ Gi
                                     λ(v) ≥ λ(v ′ ) if f (v) 6∈ Ai ∪ Gi
                                   
                                   

   Note that | ⊲F        F              F
                B | = | ⊲C | = 1 and | ⊲S | = k.
Theorem 3 ([8,18]). Let F be a set, the acceptance condition of A be expressed
by ⊲F                                             A
     X with X ∈ {B, C, S}, c ∈ N a bound and GM the run graph of A on M.
                                                                              A
    If and only if, there exists a valid c-bounded annotation function λi on GM
                                               A
for each basic comparison relation ⊲i , then GM satisfies Acc.

4.1   General Bounded Synthesis
In Theorem 3 we saw that the acceptance of a Mealy machine M by a universal
automata A can be expressed by the existence of an annotation comparison
relation. To do the same for two-way automata on program trees, we generalize
this theorem towards arbitrary run graphs.
    Let A = (ΣP , P, p0 , δL , δR , δLR , δ∅ , Acc) be a two-way universal tree automa-
ton and T = (T, τ ) a program tree. We define the run graph of A on T as
GTA = (V, v0 , E, f ), where
 – V = P × T × {L, R, D},
 – v0 = (p0 , ǫ, D),
 – E = (p, t, d), (p′ , t′ , d′ ) | ∃d′′ ∈ {L, R, U } : µ(t, d′′ ) = (t′ , d′ )
                                   

   ∧(p′ , d′′ ) ∈ δt (p, τ (t), d) and
 – f (p, t, d) = p.
    For the generalized encoding, we use the same construction for the annotation
comparison relation as presented in [18] for Street acceptance conditions, which
conveniently suffices for the general run graphs. Büchi and co-Büchi then follow
as special cases.
Lemma 2 (Appendix A.2). For a Streett acceptance condition Acc = Streett(F )
with set of tuples of states F ⊆ 2Q×Q and a run graph G = (V, v0 , E, f ):
    If G satisfies Acc, then there exists a valid |V |-bounded annotation function λ
for each basic comparison relation in ⊲F   S.

Theorem 4. Let G = (V, v0 , E, f ) be a run graph, Acc ⊆ Qω a Büchi, co-Büchi
or Streett acceptance condition expressed by the relation ⊲X for X ∈ {B, C, S}.
   There exists a valid |V |-bounded annotation function λi on G for each basic
comparison relation ⊲i , if and only if G satisfies Acc.
Proof. ” ⇒ ” : Let G, Acc, ⊲ with arity | ⊲ | = n and c be given and λi be a
valid c-bounded annotation comparison relation on G for ⊲i for all i ∈ [n]. Let
π = π0 π1 . . . ∈ G be an arbitrary path in G and i ∈ [n]. Since λi is a valid
annotation function, λi (π0 ) ⊲i λi (π1 ) ⊲i . . . holds and therefore π |= ⊲. Since ⊲
expresses Acc it follows that f (π) ∈ Acc, i.e., G satisfies Acc.
” ⇐ ” : Lemma 2.                                                                     ⊓
                                                                                     ⊔

4.2   General Encoding
We showed that the run graph satisfies an acceptance condition Acc, iff the
implementation is accepted by the automaton. We also proved that the satisfac-
tion of Acc by a run graph can be expressed by the existence of valid annotation
functions.
    We encode these constraints in SAT. The valid implementation can then be
extracted from the satisfied encoding. Note that in our definition of program
trees the structure was implicitly expressed by the nodes and for the encoding
we need to express them explicitly. Therefore, the structure of the tree is en-
coded with successor functions L and R, expressing the left and right child of a
node, respectively. We encode the program tree and the annotation function as
uninterpreted functions as explained in the following. We introduce the follow-
ing variables for arbitrary two-way automata A, program trees T , bounds c and
annotation comparison relations ⊲:
 – τt encodes label l of t with log(|Σ|) many variables, notated as τt ≡ l
 – Lt iff t has left child (implicitly the next program state t + 1)
 – Rt encodes right the child of t ∈ T with log(|T |) many variables
 – λBp,t,d iff state (p, t, d) is reachable in the run graph
 – λ#i,p,t,d encodes the i-th annotation of state (p, t, d) with log(c) many vari-
   ables. We omit the index i in the encoding
   The SAT formula ΦA,⊲
                    T   consists of the following constraints:
 – The initial state is reachable and all annotations fulfill the given bound:
                                               λ#
                                          ^
                            λBp0 ,t0 ,D ∧        p,t,d ≤ c
                                             p∈P,
                                             t∈T,
                                          d∈{L,R,D}

 – Bounded synthesis encoding
                                                             ϕ → λBp′ ,t′ ,d′ ∧ λ#        #
    ^            ^                             ^
       λBp,t,d →   (τt ≡ σ) →                                                    p,t,d ⊲ λp′ ,t′ ,d′
     p∈P,          σ∈Σ                ′   ′′
                                   (p ,d )∈δ(p,σ,d),
     t∈T,                                 t′ ∈T,
     d∈D                           (ϕ,d′ )∈µ′ (t,d′′ ,t′ )

    µ′ : T × D′ × T → [B(Lt , Rt ) × D] returns a list of pairs (ϕ, d′ ), where the
    formula ϕ enforces the tree structure needed to reach p′ , t′ , d′ .
    The encoding checks whether universal properties in the run graph hold.
Note that we need to additionally forbid walking up from the root node, which
is omitted here.
Theorem 5. Given a two-way universal tree automaton A with a Büchi, co-
Büchi or Streett acceptance condition Acc expressed by ⊲ and a bound c ∈ N.
The constraint system ΦA,⊲T   is satisfiable, iff there is a program tree T with size
|T | ≤ ⌊c/|A|⌋ that is accepted by A.
Proof. ” ⇒ ” : Let T be accepted by A, then with Theorem 4 there exists a valid
annotation function λi on G for each i ∈ [| ⊲ |]. Let λi be represented by λ# i and
λBi be true for all reachable states in the run graph G. Then ΦA,⊲T   is satisfied.
    ” ⇐ ” : Let ΦA,⊲
                   T   be satisfied. Then there exists a valid annotation function
λi encoded by λ#  i for each i ∈ [| ⊲ |] (set λi (v) = 0 for all unreachable states
v, i.e., where λ#
                i (v) is f alse) that satisfies the encoding. With Theorem 4 the
acceptance of T by A follows.                                                       ⊓
                                                                                    ⊔
                                                                                ′
   Utilizing this theorem, we now can by means of the encoding ΦB    S synthesize
program trees accepted by B ′ , i.e., precisely those program trees, which corre-
spond to reactive programs that satisfy the given specification the automaton
was constructed with.
                                         ′
Corollary 1. The SAT encoding ΦB    S is satisfiable, if and only if there exists a
program tree T with size |T | ≤ ⌊c/|B ′ |⌋ accepted by B ′ .

Size of construction The automaton can be constructed of size O(2|B|+|ϕ| ),
i.e., for a fixed set of Boolean variables the automaton is linear in the size
of the specification automaton or exponential in the size of the specification
                                               ′
formula. The constructed constraint system ΦB S is of size O(|T | · |δ| · |ΣP |) with
x many variables, where x ∈ O(|T | · (|T | + |ΣP | + |Q| · log(|Q| · |T |))). Note
that |ΣP | ∈ O(|B|NI +NO ) grows polynomial in the number of variables for fixed
input/output arities.

5   Two-Wayless Encoding
Next, we sketch the second encoding that avoids the detour via universal two-way
automata. To this end, we alter the construction in that input- and output-labels
collapse to a single InOut -label with semantics as follows



                InOut            ~ q → q ′ | val
                          {~i → val,          ~ ∈ BNI , q ′ ∈ δ(q,~i, s[~o])}


where we use output variables ~o and input variables ~i that correspond to inputs
and outputs of the system, respectively. In a nutshell, our new encoding consists
of four parts:
 1. The first part guesses the program and ensures syntactical correctness.
 2. The second part simulates the program for every possible input from every
    reachable InOut -labeled state until it again reaches the next InOut -labeled
    state. Note that every such simulation trace is deterministic once the input,
    read at the initial InOut -labeled state, has been fixed.
 3. The third part extracts a simplified transition structure from the resulting
    execution graph, that consists of direct input labeled transitions from one
    InOut -labeled state to the next one and output labeled states.
 4. In the last part, this structure is then verified by a run graph construction
    that must satisfy the specification, given as universal co-Büchi automaton.
    To this end, we couple inputs on the edges with the outputs of the successor
    state to preserve the Mealy semantics of the program.
   The first part utilizes a similar structure as used for the previous encoding
and thus is skipped for convenience here. To simulate the program in the second
part, we introduce the notion of a valuation v ∈ V, where
                         V = P × BBrI × {L, R, U } × B
         Table 1. Comparison of the general and the two-wayless encoding.

                                additional             two-way     two-wayless
    specification     states                   |B′ |
                                 variables             encoding     encoding
   in ↔ out             6            0         16       00m16s       00m02s
   in ↔ out             9            1         64       11m29s       08m34s
   latch                10           0         64       >120m        08m07s
   2-bit arbiter        10           0         128      66m48s       14m18s




captures the current program state, the current values of all non-input variables,
the current direction, and the result of the evaluation of the last Boolean expres-
sion, respectively. The simulation of the program is then expressed by a finite
execution graph, in which, after fixing a inputs ~i ∈ 2I , every valuation points to a
successor valuation. This successor valuation is unique, except for InOut -labeled
states, whose successor depends on the next input to be read. The deterministic
evaluation follows from the rules of Figure 3 and selects a unique successor for
every configuration, accordingly.

    In part three, this expression graph then is compressed into a simplified
transition structure. To this end, we need for every input and InOut -labeled
starting valuation, the target InOut -labeled valuation that is reached as a result
of the deterministic evaluation. In other words, we require to find a shortcut from
every such valuation to the next one. We use an inductive chain of constraints
to determine this shortcut efficiently. Remember that we only know the unique
successor of every valuation which only allows to make one step forward at
a time. Hence, we can store for every valuation and input a second shortcut
successor, using an additional set of variables, constrainted as follows: if the
evaluated successor is InOut -labeled, then the shortcut successor must be the
same as the evaluated one. Otherwise, it is the same as the shortcut successor of
the successor valuation, leading to the desired inductive definition. Furthermore,
to ensure a proper induction base, we use an additional ranking on the valuations
that bounds the number of steps between two InOut labeled valuations. This
annotation is realized in a similar fashion as in the previously presented encoding.

    With these shortcuts at hand, we then can extract the simplified transition
structure, which is verified using a standard run graph encoding as used for clas-
sical bounded synthesis. Furthermore, we use an over-approximation to bound
the size of the struture and use a reachability annotation that allows the solver
to reduce the constraints to those parts as required by the selected solution. The
size can, however, also be bound using an explicit bound that is set manually.

   Using this separation into four independent steps allows to keep the encoding
compact in size, and results in the previously promised performance improve-
ments presented in the next section.
        Table 2. Synthesized implementations for the two-wayless encoding.

      in ↔ out           in ↔    out             latch            2-bit arbiter

 while(tt) {         while(tt) {          while (tt) {         while (tt) {
   out = in;           out = var;           if (upd) {           g0 = g1;
   InOut               var = in;               out = in          g1 = not g1;
 }                     InOut                } else {             InOut
                     }                         skip            }
                                            };
                                            InOut
                                          }



6   Experimental Results

Table 1 compares the general encoding of Section 4.1 and the two-wayless en-
coding of Section 5 on a selection of standard benchmarks. The table contains
the of number of states of the program’s syntax tree, the number of additional
variables, i.e., variables that are not designated to handle inputs and outputs, the
size of the two-way universal Streett automaton, created for the general encod-
ing, and the solving times for both encodings. Table 2 shows the results in terms
of the synthesized program trees for the two-wayless encoding. The experiments
indicate a strong advantage of the second approach.


7   Conclusions

We introduced a generalized approach to bounded synthesis that is applicable
whenever all possible runs of a universal automaton on the possibly produced
input/output words of an input-deterministic implementation can be expressed
by a run graph. The acceptance of an implementation can then be expressed
by the existence of valid annotation functions for an annotation comparison
relation that expresses the acceptance of the automaton for Büchi, co-Büchi and
Streett acceptance conditions. The existence of valid annotation functions for a
run graph is encoded as a SAT query that is satisfiable if and only if there exists
an implementation satisfying a given bound that is accepted by the automaton.
    For LTL specifications, we constructed a two-way universal Streett automa-
ton which accepts reactive programs that satisfy the specification. We then con-
structed a run graph that represents all possible runs and applied the generalized
bounded synthesis approach. Next, we constructed a SAT query that guesses a
reactive program of bounded size as well as valid annotation functions that wit-
nesses the correctness of the synthesized program.
    Finally, we merged the previous transformations into an extended encoding
that simulates the program direclty via the constraint solver. We evaluated both
encodings with the clear result that the encoding avoiding the explicit run graph
construction for two-way automata wins in the evaluation.
References
 1. Gerstacker, C.: Bounded Synthesis of Reactive Programs (2017) Bachelor’s Thesis.
 2. Church, A.: Application of recursive arithmetic to the problem of circuit synthesis.
    Journal of Symbolic Logic 28(4) (1963) 289–290
 3. Jobstmann, B., Galler, S.J., Weiglhofer, M., Bloem, R.: Anzu: A Tool for Property
    Synthesis. In Damm, W., Hermanns, H., eds.: Computer Aided Verification, 19th
    International Conference, CAV 2007, Berlin, Germany, July 3-7, 2007, Proceedings.
    Volume 4590 of Lecture Notes in Computer Science., Springer (2007) 258–262
 4. Ehlers, R.: Unbeast: Symbolic Bounded Synthesis. In Abdulla, P.A., Leino,
    K.R.M., eds.: Tools and Algorithms for the Construction and Analysis of Systems
    - 17th International Conference, TACAS 2011, Held as Part of the Joint Euro-
    pean Conferences on Theory and Practice of Software, ETAPS 2011, Saarbrücken,
    Germany, March 26-April 3, 2011. Proceedings. Volume 6605 of Lecture Notes in
    Computer Science., Springer (2011) 272–275
 5. Bohy, A., Bruyère, V., Filiot, E., Jin, N., Raskin, J.: Acacia+, a Tool for LTL
    Synthesis. In Madhusudan, P., Seshia, S.A., eds.: Computer Aided Verification
    - 24th International Conference, CAV 2012, Berkeley, CA, USA, July 7-13, 2012
    Proceedings. Volume 7358 of Lecture Notes in Computer Science., Springer (2012)
    652–657
 6. Faymonville, P., Finkbeiner, B., Tentrup, L.: BoSy: An Experimentation Frame-
    work for Bounded Synthesis. [19] 325–332
 7. Bloem, R., Galler, S.J., Jobstmann, B., Piterman, N., Pnueli, A., Weiglhofer, M.:
    Interactive presentation: Automatic hardware synthesis from specifications: a case
    study. In Lauwereins, R., Madsen, J., eds.: 2007 Design, Automation and Test in
    Europe Conference and Exposition, DATE 2007, Nice, France, April 16-20, 2007,
    EDA Consortium, San Jose, CA, USA (2007) 1188–1193
 8. Finkbeiner, B., Schewe, S.: Bounded Synthesis. STTT 15(5-6) (2013) 519–539
 9. Finkbeiner, B., Klein, F.: Bounded Cycle Synthesis. In Chaudhuri, S., Farzan,
    A., eds.: Computer Aided Verification - 28th International Conference, CAV 2016,
    Toronto, ON, Canada, July 17-23, 2016, Proceedings, Part I. Volume 9779 of Lec-
    ture Notes in Computer Science., Springer (2016) 118–135
10. Faymonville, P., Finkbeiner, B., Rabe, M.N., Tentrup, L.: Encodings of Bounded
    Synthesis. In Legay, A., Margaria, T., eds.: Tools and Algorithms for the Construc-
    tion and Analysis of Systems - 23rd International Conference, TACAS 2017, Held
    as Part of the European Joint Conferences on Theory and Practice of Software,
    ETAPS 2017, Uppsala, Sweden, April 22-29, 2017, Proceedings, Part I. Volume
    10205 of Lecture Notes in Computer Science. (2017) 354–370
11. Alur, R., Bodı́k, R., Juniwal, G., Martin, M.M.K., Raghothaman, M., Seshia, S.A.,
    Singh, R., Solar-Lezama, A., Torlak, E., Udupa, A.: Syntax-guided synthesis. In:
    Formal Methods in Computer-Aided Design, FMCAD 2013, Portland, OR, USA,
    October 20-23, 2013, IEEE (2013) 1–8
12. Gulwani, S.: Automating string processing in spreadsheets using input-output ex-
    amples. In Ball, T., Sagiv, M., eds.: Proceedings of the 38th ACM SIGPLAN-
    SIGACT Symposium on Principles of Programming Languages, POPL 2011,
    Austin, TX, USA, January 26-28, 2011, ACM (2011) 317–330
13. Osera, P., Zdancewic, S.: Type-and-example-directed program synthesis. In Grove,
    D., Blackburn, S., eds.: Proceedings of the 36th ACM SIGPLAN Conference on
    Programming Language Design and Implementation, Portland, OR, USA, June
    15-17, 2015, ACM (2015) 619–630
14. Solar-Lezama, A.: Program sketching. STTT 15(5-6) (2013) 475–495
15. Vechev, M.T., Yahav, E., Yorsh, G.: Abstraction-guided synthesis of synchroniza-
    tion. STTT 15(5-6) (2013) 413–431
16. Madhusudan, P.: Synthesizing Reactive Programs. In Bezem, M., ed.: Com-
    puter Science Logic, 25th International Workshop / 20th Annual Conference of
    the EACSL, CSL 2011, September 12-15, 2011, Bergen, Norway, Proceedings. Vol-
    ume 12 of LIPIcs., Schloss Dagstuhl - Leibniz-Zentrum fuer Informatik (2011)
    428–442
17. Vardi, M.Y., Wolper, P.: Reasoning About Infinite Computations. Inf. Comput.
    115(1) (1994) 1–37
18. Khalimov, A., Bloem, R.: Bounded Synthesis for Streett, Rabin, and CTL∗ . [19]
    333–352
19. Majumdar, R., Kuncak, V., eds.: Computer Aided Verification - 29th International
    Conference, CAV 2017, Heidelberg, Germany, July 24-28, 2017, Proceedings, Part
    II. Volume 10427 of Lecture Notes in Computer Science., Springer (2017)
A     Appendix
A.1    Equivalence of A and B
To prove the equivalence, i.e., L(A) = L(B), we need the formal definition of
acceptance of trees by two-way tree automata and of the two-way automata A
and B. We fix the specification to be given as a non-deterministic Büchi word
automaton Aspec = (Σ, Qspec , q0 , δspec , BÜCHI(Fspec )).

Acceptance of two-way tree automata The acceptance is defined over
run trees as follows. A run of a two-way alternating tree automaton A =
(Σ, P, p0 , δ, Acc) on a program tree T = (T, τ ) is an infinite labeled binary tree
TR = (TR , τR ), where τR : TR → T × P × {L, R, D} is a labeling function, which
labels are tuples that contain the current state of the automaton and program
tree as well as the direction it came from. For TR it holds that
 – ǫ ∈ TR , τR (ǫ) = (ǫ, p0 , D) and
 – ∀y ∈ TR with
              τR (y) = (t, p, d) and δt (p, τ (t), d) = θ :
   Let S = (p1 , d1 ), . . . , (pn , dn ) ⊆ Q × {L, R, U } be a set that satisfies θ.
   Then ∀1 ≤ i ≤ n : y · i ∈ TR and τR (y · i) = t′ , pi , d′ with (t′ , d′ ) = µ(t, di ).

Two-way alternating Büchi tree automaton A The constructed two-way
alternating Büchi automaton A over the alphabet ΣP with the set of states P A ,
                                    A
                                   Pexpr = S × Bool

                   Pexec = S × Qspec × BNI × {inp, out} × Bool
                                 P A = Pexpr
                                        A
                                             ∪ Pexec
and initial state pA
                   0 = (s0 , q0 , i0 , inp, 0), is defined with the following transitions,
where s ∈ S, v ∈ Bool, q ∈ Qspec , i ∈ BNI , m ∈ {inp, out} and t ∈ {0, 1}.
 – Transitions to evaluate Boolean expressions:
    • δ∅A ((s, 1), tt, D) = true
      δ∅A ((s, 0), tt, D) = f alse
    • δ∅A ((s, 1), ff, D) = f alse
      δ∅A ((s, 0), ff, D) = (
                            true
                               true    , if s[b] = v
      • δ∅A ((s, v), b, D) =
                               f alse , otherwise
        A
    • δLR  ((s, 1), ∨, D) = ((s, 1), L) ∨ ((s, 1), R)
        A
      δLR  ((s, 0), ∨, D) = ((s, 0), L) ∧ ((s, 0), R)
        A
    • δL ((s, v), ¬, D) = ((s, 1 − v), L)
 – Transitions to evaluate non I/O statements:
    • δ∅A ((s, q, i, m, t), skip, D) = ((s, q, i, m, 0), U )
        A
    • δL  ((s, q, i, m, t), assignb , D) =                                           
       ((s[b/0], q, i, m, 0), U )∧((s, 0), L) ∨ ((s[b/1], q, i, m, 0), U )∧((s, 1), L)
        A
    • δLR  ((s, q, i, m, t), if, D) =                                                       
       ((s, 1), L) ∧ ((s, q, i, m, 0), LR) ∨ ((s, 0), L) ∧ ((s, q, i, m, 0), RR)
        A
    • δLR  ((s, q, i, m, t), while, D)
           A
      = δLR   ((s, q, i, m, t), while, R)                                                  
      = ((s, 1), L) ∧ ((s, q, i, m, 0), R) ∨ ((s, 0), L) ∧ ((s, q, i, m, 0), U )
 – Transitions to evaluate input and            W output: ~ ~
    • δ∅A ((s, q, i, inp, t), input ~b, D) = val∈B~
                                                                            ~
                                                        NI ((s[b/val], q, val, out, 0), U )

    • δ∅A ((s, q, i, out, t), output ~b, D) = q′ ∈δspec (q,i,s[~b]) ((s, q ′ , i, inp, 1), U )
                                                 W

 – Transitions to move to next statement in program:
        A
    • δLR  ((s, q, i, m, t), ;, D) = ((s, q, i, m, t), L)
        A
      δLR  ((s, q, i, m, t), ;, L) = ((s, q, i, m, t), R)
        A
      δLR  ((s, q, i, m, t), ;, R) = ((s, q, i, m, t), U )
        A
    • δLR  ((s, q, i, m, t), then, L)
           A
      = δLR   ((s, q, i, m, t), then, R)
      = ((s, q, i, m, t), U )
        A
    • δLR  ((s, q, i, m, t), if, R) = ((s, q, i, m, t), U )
All other transitions evaluate to f alse. The set of accepting states is defined as

                         F A = (s, q, i, m, 1) | q ∈ Fspec
                               


Two-way non-deterministic Büchi tree automaton B Our automaton B
with the set of states
                    B
                   Pexpr = S × Qspec × BNI × {inp, out} × {⊤, ⊥}

                                    P B = Pexpr
                                           B
                                                ∪ Pexec
and initial state pB
                   0 = (s0 , q0 , i0 , inp, 0), is defined with the following transitions,
where b ∈ B, s ∈ S, q ∈ Qspec , i ∈ BNI , m ∈ {inp, out}, r ∈ {⊤, ⊥} and
t ∈ {0, 1}.

 – Transitions to evaluate Boolean expressions:
    • δ∅B ((s, q, i, m, ⊥), tt, D) = ((s, q, i, m, ⊤), U )

      • δ∅B ((s, q, i, m, ⊥), ff, D) = ((s, q, i, m, ⊥), U )
                                       (
                                         ((s, q, i, m, ⊤), U ) , if s[b] = 1
      • δ∅B ((s, q, i, m, ⊥), b, D) =
                                         ((s, q, i, m, ⊥), U ) , otherwise
          B
      • δLR  ((s, q, i, m, ⊥), ∨, D) = ((s, q, i, m, ⊥), L)
                                       (
          B                               ((s, q, i, m, r), U ) , if r = ⊤
        δLR ((s, q, i, m, r), ∨, L) =
                                          ((s, q, i, m, r), R) , otherwise
          B
        δLR ((s, q, i, m, r), ∨, R) = ((s, q, i, m, r), U )
          B
      • δL  ((s, q, i, m, ⊥), ¬, D) = ((s, q, i, m, ⊥), L)
          B
        δL  ((s, q, i, m, r), ¬, L) = ((s, q, i, m, r), U )
 – Transitions to evaluate non I/O statements:
    • δ∅B ((s, q, i, m, t), skip, D) = ((s, q, i, m, 0), U )
        B
    • δL  ((s, q, i, m, t), assignb , D) = ((s, q, i, m, ⊥), L)
        B
      δL  ((s, q, i, m, r), assignb , L) = ((s[b/r], q, i, m, 0), U )
        B
    • δLR  ((s, q, i, m, t), if, D) = (((s, q, i, m, ⊥), L)
        B                                ((s, q, i, m, 0), RL) , if r = ⊤
      δLR  ((s, q, i, m, r), if, L) =
                                         ((s, q, i, m, 0), RR) , otherwise
        B
    • δLR  ((s, q, i, m, t), while, D)
           B
      = δLR    ((s, q, i, m, t), while, R)
      = ((s, q, i, m, ⊥), L)                (
        B                                      ((s, q, i, m, 0), R) , if r = ⊤
      δLR  ((s, q, i, m, r), while, L) =
                                               ((s, q, i, m, 0), U ) , otherwise
 – Transitions to evaluate input and output:
    • δ∅B ((s, q, i, inp, t), input ~b, D) = val∈B             ~ ~          ~
                                                W
                                                   ~    NI ((s[b/val], q, val, out, 0), U )

    • δ∅B ((s, q, i, out, t), output ~b, D) = q′ ∈δspec (q,i,s[~b]) ((s, q ′ , i, inp, 1), U )
                                                  W

 – Transitions to move to next statement in program:
        B
    • δLR  ((s, q, i, m, t), ;, D) = ((s, q, i, m, 0), L)
        B
      δLR  ((s, q, i, m, t), ;, L) = ((s, q, i, m, 0), R)
        B
      δLR  ((s, q, i, m, t), ;, R) = ((s, q, i, m, 0), U )
        B
    • δLR  ((s, q, i, m, t), then, L)
           B
      = δLR    ((s, q, i, m, t), then, R)
      = ((s, q, i, m, t), U )
        B
    • δLR  ((s, q, i, m, t), if, R) = ((s, q, i, m, 0), U )


All other transitions evaluate to f alse. The set of accepting states is defined as

                         F B = (s, q, i, m, 1) | q ∈ Fspec
                               


    Note that B behaves similar to A during normal execution and that only
boolean evaluation was altered. Therefore, the state spaces of the automaton
only differs in the states corresponding to boolean evaluation. Additionally, the
set of accepting states F A and F B are equivalent.


Equivalence Proof In this section we prove that A and B accept the exact same
program trees. We do so by showing first that B evaluates boolean expressions
to the same result as A, but instead of terminating with true or f alse the
automaton walks the tree up again and eventually reaches the node where the
boolean evaluation was started from containing the correct result. Combined
with the fact that the automata have the same behavior on normal executions
we show the equivalence of A and B.

Lemma 3. Given a program tree T that contains a boolean expression subtree
                                              A
with root t ∈ T . Let A be in state (s, v) ∈ Pexpr , B be in state (s, q, i, m, ⊥) ∈
  B
Pexpr and both automata are reading program node t coming down from the
parent.
    A evaluates for state (s, 1) to true and state (s, 0) to f alse, if and only if
                                                                  B
B moves upwards from node t with state (s, q, i, m, ⊤) ∈ Pexpr        . Vice versa, A
evaluates for state (s, 1) to f alse and state (s, 0) to true, if and only if B moves
                                                      B
upwards from node t with state (s, q, i, m, ⊥) ∈ Pexpr    .
Proof. Let A, B be defined as above, T be a valid program tree, t ∈ T be the
root of an boolean expression subtree. We proof the statement by structural
induction over the boolean expression.
Base-cases: For τ (t) :
 – tt :
   δ∅A (s, 1), tt, D = true and δ∅A (s, 0), tt, D = f alse
                                                       

   ⇔ δ∅B (s, q, i, m, ⊥), tt, D = ((s, q, i, m, ⊤), U )
                                
 – ff :
   δ∅A (s, 1), ff, D = f alse and δ∅A (s, 0), ff, D = true
                                                       

   ⇔ δ∅B (s, q, i, m, ⊥), ff, D = ((s, q, i, m, ⊥), U )
 – b:                              (
     A                               true       , if s[b] = v
   δ∅ ((s, v), b, D)             =
                                     f alse , otherwise
                                   (
                                     ((s, q, i, m, ⊤), U ) , if s[b] = 1
   ⇔ δ∅B ((s, q, i, m, ⊥), b, D) =
                                     ((s, q, i, m, ⊥), U ) , otherwise
Inductive-step: For τ (t) =
 – ¬:
   By definition, A continues with (s, 1 − v) and B continues with (s, q, i, m, ⊥)
   in the left subtree. By induction, B returns from the left subtree with state
   (s, q, i, m, r) for r = ⊤/⊥ and by definition sends (s, q, i, m, r) upwards,
   where r matches the acceptance of (s, v − 1) and r with (s, v).
 – ∨:
   By definition, B continues with (s, q, i, m, ⊥) in the left subtree. We make a
   case distinction based on v.
   Either v = 1: Then by definition, A evaluates to true, iff (s, 1) if either
   the left or right subtree evaluates to true. Assuming the left subtree eval-
   uates to true, then by induction B returns from the left subtree with state
   (s, q, i, m, ⊤) and by definition sends the same state upwards. For the other
   case, the right subtree evaluates to true for (s, 1). By induction B first returns
   with (s, q, i, m, ⊥) from the left subtree and by definition sends this state into
   the right subtree. Again by induction, B returns with state (s, q, i, m, ⊤) from
   the right subtree and by definition sends this state upwards.
   Or v = 0: Then by definition, A evaluates to true, iff (s, 0) in both the
   left and right subtree evaluate to true. By induction, B returns with copy
   (s, q, i, m, ⊥) from the right subtree and by definition sends this copy into
   the right subtree. Again by induction, B returns with (s, q, i, m, ⊥) and by
   definition sends it upwards.
                                                                                        ⊓
                                                                                        ⊔
Theorem 6. L(A) = L(B).
Proof. ” ⇒ ” :
Let T ∈ L(A) be a program tree with accepting run tree RA = hRA , τA i. The
initial state p0 of A is a normal execution state (p0 ∈ Pexec ). The transitions of
A are defined such that whenever A is in a normal execution state p ∈ Pexec
exactly one successor is again a normal execution state p′ ∈ Pexec . There can be
an additional successor state that is used to evaluate a boolean expression but
those subtrees of the accepting run graph are finite and terminate to true on
every path. Therefore there only exists a single infinite path
                                                                                     ω
          r0 r1 . . . = (t0 , p0 , d0 )(t1 , p1 , d1 ) . . . ∈ T × Pexec × {L, R, D}

in the accepting run tree RA that satisfies the Büchi acceptance condition.
                                                              ω
    We show that B visits the same states p0 p1 . . . ∈ Pexec      in the same order
while traversing T , that is whenever A is in state pi ∈ Pexec reading a node
ti ∈ T moving to node ti+1 with state pi+1 , B in the same state reading the
same node eventually moves to node ti+1 with state pi+1 . We show this with a
case analysis over the possible labels τA (ti ). In all three interesting cases ri has
two children, namely ri+1 and (t′ , p′ , L) with p′ = (s, v) ∈ Pexpr
                                                                  A
                                                                      .
 – assignb : Since the run tree is accepting, the boolean evaluation evaluates
   to true. With Lemma 3 we know that B traverses the boolean expression
   subtree and returns with state (s, q, i, m, r) to ti , where r = ⊤/⊥ for v = 1/0,
   respectively. By definition B now sends (s[b/v], q, i, m, 0) upwards yielding
   ri+1 .
 – if: Since the run tree is accepting, the boolean evaluation evaluates to true.
   With Lemma 3 we know that B traverses the boolean expression subtree
   and returns with state (s, q, i, m, r) to ti , where r = ⊤/⊥ for v = 1/0,
   respectively. Depending on v having the value 0 or 1 the only valid move for
   B is either ((s, q, i, m, 0), RR) or ((s, q, i, m, 0), RL), respectively. Either way
   it matches the move of A yielding ri+1 .
 – while: Since the run tree is accepting, the boolean evaluation evaluates
   to true. With Lemma 3 we know that B traverses the boolean expression
   subtree and returns with state (s, q, i, m, r) to ti , where r = ⊤/⊥ for v = 1/0,
   respectively. Depending on v having the value 0 or 1 the only valid transition
   for B is either ((s, q, i, m, 0), U ) or ((s, q, i, m, 0), R), respectively. Either way
   it matches the move of A yielding ri+1 .
All other valid transitions are equally defined such that B can make the same
move.
    Since B visits for every accepted run tree the same normal execution states
equally often and the set of accepting states for A and B are equivalent and a
subset of normal execution states, B accepts the same program trees as A.
    ”⇐”:
Let T ∈ L(B) be a program tree with accepting run tree RB = hRB , τB i. The
initial state p0 of B is a normal execution state (p0 ∈ Pexec ). Since B has no
universal choices the run tree is 1-ary, that is a single infinite path
                                                                                    ω
           r0 r1 . . . = (t0 , p0 , d0 )(t1 , p1 , d1 ) . . . ∈ T × P B × {L, R, D}

    We show that A can visit the same normal execution states as B, more
precisely: Let B be in state pi ∈ Pexec reading a node ti ∈ T . If B moves to node
ti+1 with state pi+1 ∈ Pexec , then A can also perform a valid move from ti with
state pi to ti+1 with state pi+1 .
                                    B
If B moves to a state pi+1 ∈ Pexpr        and traverses the boolean expression subtree
                                                                 B
and therefore visits the states pi+2 pi+3 . . . pi+j−1 ∈ (Pexpr     )∗ until it returns to
                                           B
node ti (= ti+j ) with state pi+j ∈ Pexpr      and subsequently moves to node ti+j+1
with state pi+j+1 ∈ Pexec , then A can also perform a valid move from ti with
state pi to node ti+j+1 with state pi+j+1 .
    In the first case, where B moves from normal execution state to another
normal execution state A can always do the same move since those transitions are
equally defined. We show the second case with a case analysis over the possible
                                                                                       B
labels τB (ti ). Let pi = (s, q, i, m, t) ∈ Pexec , ti ∈ T , pi+1 = (s, q, i, m, ⊥) ∈ Pexpr
and pi+j = (s, q, i, m, r)).

 – assignb : In this case B moves from pi+j to (s[b/v], q, i, m, 0). Depending on
   v, A moves from ti with state pi into ti+j+1 with state (s[b/v], q, i, m, 0) and
   universally into ti+1 with state (s, v), thus satisfying the transition relation.
   The second copy send into the boolean expression terminates to true based
   on Lemma 3.
 – if and while: A moves from ti with state pi into ti+j+1 with state pi+j+1 and
   depending on v universally into ti+1 with state (s, v). Again with Lemma 3
   the second copy send into the boolean expression terminates to true.

Since A visits the same normal execution states as B in the same order and the
set of accepting states are equivalent and is a subset of normal execution states,
A fulfills the Büchi acceptance condition.                                     ⊓
                                                                                ⊔


A.2    Proof of Lemma 2

For a Streett acceptance condition Acc = Streett(F ) with set of tuples of states
F ⊆ 2Q×Q and a run graph G = (V, v0 , E, f ):
If G satisfies Acc, then there exists a valid |V |-bounded annotation function λ
for each basic comparison relation in ⊲FS.

Proof. Let F = {(Ai , Gi )}i∈[k] be a set of tuples of states, Acc = STREETT(F )
an acceptance condition and G = (V, v0 , E, f ) a run graph satisfying Acc.
    We construct the k different valid c-bounded annotation functions λi . We
first define λi (v) = 0 for all unreachable states v ∈ V and then remove those
states from G. We then define each λi (v) for all i ∈ [k] with:

 – ∀v ∈ V with f (v) ∈ Gi : λi (v) = 0.
– Remove outgoing edges for states v ∈ V with f (v) ∈ Gi . That results in G ′ =
  (V, E ′ , f ), where E ′ = E \ {(v, v ′ ) ∈ E | f (v) ∈ Gi }. G ′ contains no strongly
  connected components (SCCs) that have a vertex v with f (v) ∈ Ai ∪ Gi . For
  Gi it is obvious since all outgoing edges are removed. For Ai : Assume there
  is an SCC containing a state v where f (v) ∈ Ai , then there exists an infinite
  path π inside this SCC that infinitely often visits Ai without infinite visits
  to the corresponding set Gi and therefore f (π) 6∈ Acc which contradicts the
  assumption.
– Now let S be the set S    off all SCCs of G ′ . We define G ′′ = (V ′′ , E ′′ , f ). Where
  V = S ∪ {{v} | v 6∈ S∈S S} and E ′′ = {(S1 , S2 ) | ∃v1 ∈ S1 , v2 ∈ S2 : S1 6=
     ′′

  S2 ∧ (v1 , v2 ) ∈ E ′ }.
  G ′′ is a directed acyclic graph and therefor all paths in G ′′ are of finite length
  and there only exist finitely many paths.
– We define nbi (π) : (V ′′ )∗ → N as the max number of bad states visited on
  some path π = S1 , . . . , Sm . Let Occ(π)
                                          S      denote the set of occurring SCCs in
  π. We formally define nbi (π) =           S∈Occ(π) S ∩ {v ∈ V | f (v) ∈ Ai } .
– ∀v ∈ S ∈ V ′′ with f (v) 6∈ Gi : λi (v) = max({nbi (π) | π is a path from S}).
                                                                                          ⊓
                                                                                          ⊔
