                                         Gillian: Compositional Symbolic Execution for All

                                         JOSÉ FRAGOSO SANTOS, Imperial College London, UK and INESC-ID/IST, Univ. of Lisbon, Portugal
                                         PETAR MAKSIMOVIĆ, Imperial College London, UK and Mathematical Institute SASA, Serbia
arXiv:2001.05059v1 [cs.PL] 14 Jan 2020




                                         SACHA-ÉLIE AYOUN, Imperial College London, UK
                                         PHILIPPA GARDNER, Imperial College London, UK
                                         We present Gillian, a language-independent framework for the development of compositional symbolic anal-
                                         ysis tools. Gillian supports three ﬂavours of analysis: whole-program symbolic testing, full veriﬁcation, and
                                         bi-abduction. It comes with fully parametric meta-theoretical results and a modular implementation, designed
                                         to minimise the instantiation eﬀort required of the user. We evaluate Gillian by instantiating it to JavaScript
                                         and C, and perform its analyses on a set of data-structure libraries, obtaining results that indicate that Gillian
                                         is robust enough to reason about real-world programming languages.


                                         1    INTRODUCTION
                                         Developing symbolic execution analyses for modern programming languages is a challenging and
                                         time-consuming task. The complexity of the underlying meta-theory and the associated tool devel-
                                         opment is substantial. However, symbolic execution tools share a number of features independent of
                                         the target language: for instance, interaction with ﬁrst-order solvers [De Moura and Bjørner 2008]
                                         and the management of the variable store. Even so, the amount of eﬀort required to transfer an anal-
                                         ysis from one programming language to another is often prohibitive. While there has been work on
                                         streamlining this process by embedding the target language into a host language with support for
                                         symbolic analysis [Bucur et al. 2014; Torlak and Bodík 2013], these approaches do not scale well to
                                         fully-ﬂedged real-world languages.
                                            We present Gillian, a general framework for swift development of compositional symbolic anal-
                                         ysis tools for real-world programming languages. Gillian is underpinned by GIL, a simple goto lan-
                                         guage parametric on the memory model of the target language: that is, on a set of actions describing
                                         the fundamental ways in which the programs of the target language interact with their respective
                                         memories. Gillian comes with a fully parametric meta-theory that uniﬁes the treatment of symbolic
                                         execution, compositional program reasoning based on separation logic (SL), and bi-abduction. In
                                         particular, it supports three main styles of analysis:
                                             • whole-program symbolic execution, where end-users write unit tests with symbolic inputs and
                                               outputs and use simple ﬁrst-order assertions to describe the properties that the outputs must
                                               satisfy, while Gillian tries to generate symbolic traces that invalidate those assertions;
                                             • veriﬁcation, where end-users annotate the functions of their programs with SL-style speciﬁca-
                                               tions and use Gillian to verify that the functions meet their speciﬁcations; and
                                             • bi-abduction, where end-users simply provide a program with no speciﬁcations or unit tests
                                               and are given back a set of SL-style speciﬁcations describing the behaviour of every function
                                               in the program up to a pre-established bound; if, in this process, a possible bug is found, users
                                               are given back the symbolic trace that leads to the bug.
                                            To obtain an instantiation of each type of analysis for their target languages, users need to
                                         provide a compiler from the target language to GIL, and then simply instantiate Gillian with a
                                         memory model that provides an action-level implementation of the corresponding analysis: whole-
                                         program symbolic execution requires a symbolic implementation of the memory model of the target
                                         language; veriﬁcation additionally requires that memory model to expose a set of core predicates
                                         describing the memory’s atomic constituents (essentially, SL assertions speciﬁc to that memory
                                         model); and bi-abduction requires the memory model to provide, on top of that, a mechanism for
2                  José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

inferring missing resource whenever an action cannot be executed due to missing information. The
implementation of a memory model with support for these three types of analyses (in OCaml) is
substantially simpler than the implementation of each type of analysis from scratch.
   Importantly, the meta-theory of Gillian is fully parametric on the memory model of the target
language. Hence, the soundness theorems of whole-program symbolic execution, veriﬁcation, and
bi-abduction are proven in general once and for all, and can be instantiated to each target language
provided that the user proves the necessary memory-speciﬁc lemmas. Similarly to the implemen-
tation, proving the memory-speciﬁc lemmas is far easier than creating a new soundness proof for
each instantiation and analysis.
   We evaluate Gillian by instantiating it to JavaScript and C. Using the obtained tools, we run
the three analyses of Gillian on a series of data-structure libraries, purposefully written using the
programming idioms speciﬁc to the two languages. For instance, our JavaScript examples rely on
extensible objects, prototype-based inheritance, and closures, while our C examples use dynamic
memory allocation, structures, and pointer arithmetic. The evaluation results indicate that Gillian
is robust enough to reason about real-world programming languages.
Outline of the Paper. In §2, we present the parametric symbolic execution of Gillian. In §3, we give
a thorough account of our parametric soundness result. The veriﬁcation and bi-abduction analyses
are then presented in detail in §4 and §5, respectively. In §6, we instantiate Gillian to obtain analysis
tools for JavaScript and C. We discuss the related work in §7 and conclude in §8.
   Throughout the paper, to give the reader a better intuition, we illustrate how to instantiate Gillian
to each type of analysis using as an example a simple While language with static objects, reminis-
cent of that of [Berdine et al. 2005]. We also comment on our implementation choices and demon-
strate how the implementation closely follows the theory.

2   PARAMETRIC SYMBOLIC EXECUTION
At the core of Gillian is a parametric interpreter for GIL, the simple intermediate goto language of
Gillian. We present the syntax of GIL and give its semantics in terms of state models (§2.1). A state
model can be viewed as an interface through which a programming language interacts with its state,
and is parametric on the underlying memory model. We introduce concrete and symbolic state and
memory models, and demonstrate how to automatically lift memory models to appropriate state
models (§2.3). As the running example, we introduce a simple While language: we give its syntax,
actions, and compiler to GIL in §2.2, and present its concrete and symbolic memory models in §2.4.

2.1 GIL Syntax and Semantics
GIL is a simple goto language with top-level procedures. It is parametric on a set of actions, A, which
provide a general mechanism for interacting with GIL states. This parametricity allows us to main-
tain GIL states opaque throughout the meta-theoretical development and to provide parametric
soundness results, minimising the burden of proof for users of Gillian.
The Syntax of GIL
v ∈ V , n ∈ N | s ∈ S | b ∈ B | l, ς ∈ Symb | τ ∈ T | f ∈ F | v         e ∈ E , v | x ∈ X | ⊖e | e 1 ⊕ e 2
c ∈ CA , x := e | ifgoto e i | x := e(e ′) | x := α(e) |                proc ∈ Proc A , proc f (x){c}
          x := symbj | x := freshj | return e | fail e | vanish         p ∈ ProдA : F ⇀ Proc A
where i, j ∈ N and α ∈ A.

   GIL values, v ∈ V, include numbers, strings, booleans, uninterpreted symbols, types, procedure
identiﬁers, and lists of values. Uninterpreted symbols are mostly used to denote memory locations
and instantiation-speciﬁc constants. Types are standard: they include, for example, the types of
Gillian: Compositional Symbolic Execution for All                                                                        3

numbers, strings, booleans, and lists. GIL expressions, e ∈ E, include values, program variables x,
and various unary and binary operators.
   GIL commands include, ﬁrst of all, the standard variable assignment, conditional goto, and dy-
namic procedure call.1 Next, we have three GIL-speciﬁc commands: action execution, x := α(e), exe-
cutes the action α ∈ A with the argument obtained by evaluating e; and two allocations, x := symbj
and x := freshj , which generate fresh uninterpreted and interpreted symbols, respectively. These al-
locations are annotated with a jointly unique identiﬁer j ∈ N, addressed in §2.1.1 and §2.3. Finally,
we have three additional control-ﬂow related commands: return terminates the execution of the
current procedure; fail terminates the execution of the entire program with an error; and vanish
silently terminates the execution of the entire program without generating a result.
   A GIL procedure, proc ∈ Proc A is of the form proc f (x){c}, where f is its identiﬁer, x is its
formal parameter, and its body c is a sequence of GIL commands. A GIL program, p ∈ ProдA , is a
ﬁnite partial function, mapping procedure identiﬁers to their corresponding procedures.
Semantics. The semantics of GIL is parameterised by a state model, S ∈ S, deﬁned as follows.
   Deﬁnition 2.1 (State Model). A state model S ∈ S is a triple h|S |, V , Ai, consisting of: (1) a set of
states on which GIL programs operate, |S | ∋ S, (2) a set of values stored in those states, V ∋ v, and
(3) a set of actions that can be performed on those states, A ∋ α. All GIL states contain a variable
store, ρ : X ⇀ V , mapping program variables to values.
   A state model deﬁnes the following functions for acting on states (≡pp denotes pretty-printing
for readability):
     • setVar : |S | → X → V → |S |                                   (setVar(σ , x, v) ≡pp σ .setVar(x, v))
     • setStore : |S | → (X ⇀ V ) → |S |                               (setStore(σ , ρ) ≡pp σ .setStore(ρ))
     • getStore : |S | → (X ⇀ V )                                           (getStore(σ ) ≡pp σ .getStore)
     • ee : |S | → E ⇀ V                                                             (ee(σ , e) ≡pp σ .ee(e))
     • ea : A → |S | → V ⇀ ℘(|S | × V )                  ((σ ′, v′ ) ∈ ea(α, σ , v) ≡pp σ .α (v)    (σ ′, v′ ))
   The intuition behind the state functions is as follows: (1) setVar(σ , x, v) sets x to v in the store
of σ ; (2) setStore(σ , x, ρ) replaces the store of σ with ρ; (3) getStore(σ ) obtains the store of σ ; and
(4) ee(σ , e) evaluates the expression e in the store of σ ; and (5) ea(α, σ , v) executes the action α
on the state σ with argument v. Note that, since actions result in sets of state-value pairs, the GIL
semantics may be non-deterministic.
   A state model S = h|S |, V , Ai is said to be proper if and only if it deﬁnes the following three
distinguished actions: assume, for extending the state with new information; and symb and fresh,
for generating new uninterpreted and interpreted symbols, respectively. Onward, we assume to
work with proper state models.
GIL Semantic Domains for S = h|S |,V , Ai
   Call stacks:            cs ∈ Cs S , hf i | hf , x, ρ, ii : cs         where f ∈ F , x ∈ X, ρ : X ⇀ V , i ∈ N
   Conﬁgurations:       cf ∈ Con f S , hp, σ, cs, ii                     where p ∈ ProдA , σ ∈ |S |, cs ∈ Cs S , i ∈ N
   Outcomes:                  o ∈ O , · | N(v) | E(v)                    where v ∈ V

   The GIL semantics is deﬁned in Figure 1. On each procedure call, it keeps track of the execution
context of the caller, so that control can correctly be returned once the execution of the callee
ﬁnishes. We achieve this by using call stacks, cs ∈ Cs S , which are non-empty lists of stack frames. A
top-level stack frame, hf i, only contains the identiﬁer of the procedure that started the execution.
An inner stack frame, hf , x, ρ, ii, contains: (1) the identiﬁer f of the procedure being executed;
(2) the variable x to which the return value of f will be assigned; (3) the store ρ of the caller of f ;
1 The procedure call is dynamic in that the identiﬁer is obtained by evaluating the caller expression.
4                            José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

and (4) the index i to which control is transferred when the execution of f terminates. Additionally,
we denote the argument of a function f by f .arg.
       Assignment                                                        Action
          cmd(p, cs, i) = x := e              σ .ee (e) = v               cmd(p, cs, i) = x := α (e)         σ .ee (e) = v σ .α (v)            (σ ′, v′ )
                                                                                                              ′                   ′
        p ⊢ hσ, cs, i i        hσ .setVar(x, v), cs, i+1i                           p ⊢ hσ, cs, i i        hσ .setVar(x, v ), cs, i+1i

    IfGoto - True                                 IfGoto - False
      cmd(p, cs, i) = ifgoto e j                      cmd(p, cs, i) = ifgoto e j                   Symb
             σ .ee (e) = v                                   σ .ee (¬e) = v                                   cmd(p, cs, i) = x := symbj
       σ .assume (v)     (σ ′, −)                      σ .assume (v)     (σ ′, −)                               σ .symb (j)      (σ ′, v)
     p ⊢ hσ, cs, i i        hσ ′, cs, j i          p ⊢ hσ, cs, i i       hσ ′, cs, i + 1i          p ⊢ hσ, cs, i i           hσ ′ .setVar(x, v), cs, i+1i
         Fresh                                                               Call
                   cmd(p, cs, i) = x := freshj                                cmd(p, cs, i) = e(e ′ )   σ .ee (e) = f       σ .ee (e ′ ) = v
                     σ .fresh (j)    (σ ′, v)                                               ′
                                                                                         cs = hf , x, σ .getStore, i + 1i : cs
          p ⊢ hσ, cs, i i        hσ ′ .setVar(x, v), cs, i+1i                    p ⊢ hσ, cs, i i       hσ .setStore([f .arg 7→ v]), cs′, 0i

 Return                                                              Top Return                                          Fail
      cmd(p, cs, i) = return e      σ .ee (e) = v                         cmd(p, cs, i) = return e                              cmd(p, cs, i) = fail e
    cs = h−, x, ρ, j i : cs′   σ ′ = σ .setStore(ρ)                            σ .ee (e) = v                                       σ .ee (e) = v
      p ⊢ hσ, cs, i i        hσ ′ .setVar(x, v), cs′, j i            p ⊢ hσ, hf i, i i      hσ, hf i, i i N(v)           p ⊢ hσ, cs, i i      hσ, cs, i i E(v)
                                                                                                                         ′
                                            Fig. 1. Semantics of GIL: p ⊢ hσ, cs, ii ·                hσ ′ , cs ′, jio
     To capture the ﬂow of the execution, we use outcomes, o ∈ O. GIL has three possible outcomes:
(1) continuation, ·, signifying that the execution should proceed; (2) return, N(v), signifying that
there was a top-level return with value v; and (3) error, E(v), signifying that the execution failed
with value v. In the rules, we elide the continuation outcome whenever it is clear from the context.
   Semantic transitions for GIL commands are of the form p ⊢ hσ , cs, ii ·                 ′   ′   o
                                                                                     S hσ , cs , ji , meaning
that, given a program p, the evaluation of the i-th command of the top procedure of the call stack
cs in the state σ generates the state σ ′, call stack cs ′ , and outcome o, and the next command to be
evaluated is the j-th command of the top procedure of cs ′ .
Implementation. In the implementation, procedure module type State = sig
                                                                    type t (** Type of Gil states *)
calls and actions may have multiple parameters. Further,            type vt (** Type of Gil values *)
we have several additional commands: the unconditional              type a (** Type of Gil actions *)
goto, goto i; procedure application, x := apply (e, e), for         val init : t
modelling functions which take a variable number of ar-             val setVar : t -> Var.t -> vt -> t
                                                                    val setStore : t -> (Var.t, vt) Map.t -> t
guments; the external procedure call, x := extern e(e),             val store : t -> (Var.t, vt) Map.t
for modelling language features that step out of the pro-           val ee : t -> Expr.t -> vt
                                                                    val ea : a -> t -> vt -> (t * vt) list
gram, such as the eval command of JavaScript or system              val assume : t -> vt -> (t * vt) list
calls in C;argument collection, arguments , which returns           val fresh : t -> vt -> (t * vt) list
                                                                    val symb : t -> vt -> (t * vt) list
a GIL list containing the arguments with which the cur-             ...
rent procedure was called; and the phi-node command, end
x := phi (x : x), which allows GIL programs to be writ- module type Allocator = sig
ten in Single-Static-Assignment (SSA) style [Cytron et al.          type t   (** Type of allocation records *)
                                                                    type vts (** Type of unintepreted symbols *)
1989]. These commands can all be compiled to the GIL of             type vtf (** Type of interpeted symbols *)
the paper, with the exception of the external procedure
                                                                    val alloc_s : t -> int -> t * vts
call. We do not provide meta-theoretical guarantees for             val alloc_f : t -> int -> t * vtf
GIL programs that use external procedure calls.                   end
   The general GIL interpreter follows the GIL semantics            Fig. 2. OCaml State/Allocator Signature
given in Figure 1 and is implemented as an OCaml func-
tor parameterised by an OCaml module with type State. The State module type, whose signature
Gillian: Compositional Symbolic Execution for All                                                                        5

                           Assume                        Assert
 Assignment                                                                                 Lookup
                            CW (assume e, pc) ,            CW (assert e, pc) ,
   CW (x := e, pc) ,                                                                         CW (x := e .p, pc) ,
                             pc : ifgoto e (pc + 2)         pc : ifgoto e (pc + 2)
    pc : x := e                                                                               pc : x := lookup([e, p])
                             pc + 1 : vanish                pc + 1 : fail e
    · ← pc + 1                                                                                · ← pc + 1
                             · ← pc + 2                     · ← pc + 2

                  Fig. 3. While-to-GIL Compiler: CW : Stmt W → N → CAW list × N (excerpt)

is partially given in Figure 2, follows our formal deﬁnition of state models as per Deﬁnition 2.1.
In addition, it contains functions related to, for example, state and value simpliﬁcation, as well as
interaction with the ﬁrst-order solver.
2.1.1 GIL Allocation. Fresh value generation is a common source of technical clutter often omitted
or hand-waved in the formal presentation of program analyses. Gillian relieves the user of the frame-
work from needing to reason about this issue by having built-in fresh-value allocators, inspired by
the work of Banerjee and Naumann [2002].
   Deﬁnition 2.2 (Allocator). An allocator AL ∈ AL is a pair, h|AL|, V i, consisting of: (1) a set |AL| ∋ ξ
of allocation records2 ; and (2) the set V of values that may be allocated. It exposes the function
alloc : |AL| → N → ℘(V ) ⇀ |AL| × V , which satisﬁes the well-formedness constraint (ξ ′, v) =
alloc (ξ , j, Y ) =⇒ v ∈ Y , and is pretty printed as ξ .alloc (j) →Y (ξ ′, v).
   Informally, alloc (ξ , j, Y ) generates a fresh value v taken from Y ⊆ V , associates it with the al-
location site3 uniquely identiﬁed by the natural number j, and returns it together with a updated
allocation record. We discuss allocators and their properties in more detail in §3.2, in the context
of our soundness results.
Implementation. We implement allocators as shown in Figure 2. As we do not have the expressive
power to pass arbitrary subsets in OCaml, we instead require two separate types, vts/vtf used gen-
erating fresh uninterpreted/interpreted symbols, each generated by a dedicated allocation function,
alloc_s/alloc_f. We show how allocators can be used in practice in §2.3.

2.2    While: Syntax, Actions, and Compilation to GIL
We demonstrate how to instantiate Gillian using a simple While language with static objects. Its syn-
tax includes: the variable assignment; the skip command; sequencing; the if-then-else conditional;
the while loop; the static function call; the return statement; assume and assert statements for driv-
ing the symbolic analysis; and statements for operating on static objects: object creation, property
lookup, property mutation, and object disposal. For simplicity, we assume that the semantics of
expressions and the variable store are the same for While and GIL.
The Syntax of While
 ws ∈ Stmt W , x := e | skip | ws1 ; ws2 | if(e){ws1 }else {ws2 } | while (e){ws} | x := f (e) | return e |
               assume e | assert e | x := pi : ei |in=1 | x := e.p | e.p := e ′ | dispose e

   In order to compile While to GIL, we ﬁrst have to pick a set of actions AW for acting on While
states. As we have four operations on objects—allocation, lookup, mutation, and disposal—assigning
an action to each of those would be a reasonable ﬁrst attempt. However, since Gillian has a built-
in allocator for generating fresh locations, we do not need a separate action for object allocation,
arriving at the set of actions AW = {lookup, mutate, dispose}.
2 Intuitively, an allocation record maintains information about already allocated values; this approach is complementary to

the free set approach of Raza and Gardner [2009], where information is maintained about values that can still be allocated.
3 An allocation site j is the program point that is associated with either the symb or the fresh command.
                                                                                   j            j
6                 José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   A part of the While-to-GIL compiler is given in Figure 3 (cf. Appendix A). It is modelled as a
function CW : Stmt W → N → CAW list × N, mapping a While statement ws ∈ Stmt W and a natural
number pc (read: program counter) to a sequence of GIL commands and the next available program
counter, npc (denoted in Figure 3 using the notation · ← npc). For instance, if CW (ws, pc) = (c, npc),
then the while statement ws compiles to the sequence of GIL commands given by c and that the
commands in c are labelled with indexes pc to npc − 1.
   The compilation rules are straightforward; we explain the ones given in Figure 3. We compile
the While assignment to a GIL assignment, shallowly embedding While variables to GIL variables.
The assume statement, assume e, compiles to a goto statement, ifgoto e (pc + 2), which branches
on the value of the expression to be assumed, followed by a silent cutting of the branch in which
it does not hold by using the GIL command vanish . The assert statement, assert e, is compiled to
the same goto statement that branches on e, but this time, if the branch in which e does not hold is
reached, the execution will terminate with error by using the GIL command fail. Finally, the lookup
of While is compiled as a call to the corresponding action, lookup, whose parameter is a GIL list
containing the expression denoting the address of the object, e, and the looked-up property, p.

2.3   Concrete and Symbolic States
Reasoning about programs can, at a high level, be separated into reasoning about the variable store
and about the memory model of the programming language in question. Gillian simpliﬁes this pro-
cess by providing built-in reasoning about the variable store, leaving to the user only to take care of
the memory model. In particular, it is possible to lift a given memory to a GIL state by coupling said
memory with an appropriate variable store and allocator. In this section, we illustrate this lifting
for concrete and symbolic memories, obtaining concrete and symbolic states.
   Concrete memories store concrete values, v ∈ V. Symbolic memories store logical expressions,
ê ∈ Ê, generated by the grammar ê ∈ Ê , v | x̂ ∈ X̂ | ⊖ê | ê 1 ⊕ ê 2 , where x̂ ranges over a set of
logical variables, X̂. The formal deﬁnitions of these two memory models are as follows.
  Deﬁnition 2.3 (Concrete Memory Model). A concrete memory model M ∈ M is a pair h|M |, Ai,
consisting of a set of concrete memories, |M | ∋ µ, and a set of actions A ∋ α. A concrete memory
model additionally deﬁnes a function ea , for concrete action execution on memories:
               ea : A → |M | → V ⇀ |M | × V                            (ea (α, µ, v) ≡pp µ.α(v))

  Deﬁnition 2.4 (Symbolic Memory Model). A symbolic memory model M̂ ∈ M̂ is a pair h|M̂ |, Ai,
consisting of a set of symbolic memories, |M̂ | ∋ µ̂, and a set of actions A ∋ α. A symbolic memory
                                      ˆ for symbolic action execution on memories:
model additionally deﬁnes a function ea
 ˆ : A→|M̂ | → Ê →Π⇀℘(|M̂ | × Ê × Π)
ea                                            ((µ̂ ′, ê ′, π ′) ∈ ea
                                                                    ˆ (α, µ̂, ê, π ) ≡pp µ̂.α (ê, π )   (µ̂ ′, ê ′, π ′ ))
where π ∈ Π ⊂ Ê denotes a boolean logical expression.
   From a concrete memory, µ ∈ |M |, we construct a concrete state σ by coupling µ with a concrete
store, ρ : X ⇀ V, and a concrete allocation record, ξ ∈ |AL|. Analogously, from a symbolic mem-
ory, µ̂ ∈ |M̂ |, we construct a symbolic state σ̂ by coupling µ̂ with a symbolic store, ρ̂ : X ⇀ Ê, and
a symbolic allocation record, ξˆ ∈ |AL|.
                                       ˆ Symbolic states also include a boolean logical expression
π ∈ Π, referred to as the path condition of σ̂ . Path conditions [Baldoni et al. 2018] bookeep the con-
straints on the symbolic variables that led the execution to the current symbolic state. We formally
describe the liftings from concrete and symbolic memories to the appropriate states below, with
A0 = {assume, fresh, symb}.
Gillian: Compositional Symbolic Execution for All                                                                7

   Deﬁnition 2.5 (Concrete State Constructor (CST )). Given an allocator AL = h|AL|, Vi, the concrete
state constructor CST : M → S is deﬁned as CST (h|M |, Ai) , h|S |, V, A ⊎ A0 i, where:
   • |S | = |M | × (X ⇀ V) × |AL|
   • setVar(hµ, ρ, ξ i, x, v) , hµ, ρ[x 7→ v], ξ i
   • setStore(hµ, _, ξ i, ρ)  , hµ, ρ, ξ i
   • getStore(h_, ρ, _i)      , ρ
   • ee(h_, ρ, _i, e)         , neo ρ
   • ea(α, hµ, ρ, ξ i, v)     , {(hµ ′, ρ, ξ i, v ′) | (µ ′,v ′ ) = ea (α, µ, v)}
   • assume(σ,v)              , {(σ,v) | v = true}
   • symb(hµ, ρ, ξ i, j)      , {(hµ, ρ, ξ ′i, ς) | ξ .alloc (j) → Symb (ξ ′, ς)}
   • fresh(hµ, ρ, ξ i, j)           ,       {(hµ̂, ρ̂, ξ ′i, v) | ξ .alloc (j) → V (ξ ′,v)}
                                                                          ˆ = h|AL|,
   Deﬁnition 2.6 (Symbolic State Constructor (SST )). Given an allocator AL       ˆ Êi, the symbolic
                                                                 ˆ
state constructor SST : M̂ → S is deﬁned as SST (h|M̂ |, Ai) , hS, Ê, A ⊎ A0 i, where:
   • |Sˆ| = | M̂ | × (X ⇀ Ê) × |AL|ˆ ×Π
                        ˆ
   • setVar(hµ̂, ρ̂, ξ , π i, x, e) , hµ̂, ρ̂[x 7→ e],
                                 ˆ                      ˆ ξˆ, π i
   • setStore(hµ̂, _, ξˆ, π i, ρ̂)   , hµ̂, ρ̂, ξˆ, π i
   • getStore(h_, ρ̂, _, _i)         , ρ̂
   • ee(h_, ρ̂, _, _i, e)            , ρ̂(e)
   • ea(α, hµ̂, ρ̂, ξˆ, π i, e)
                             ˆ       , {(hµ̂ ′, ρ̂, ξˆ, π ∧ π ′ i, ê ′) | (µ̂ ′ , eˆ′, π ′ ) ∈ ea
                                                                                                 ˆ (α, µ̂, e)}
                                                                                                           ˆ
   • assume(hµ̂, ρ̂, ξ , π i, π ) , {(hµ̂, ρ̂, ξˆ, π ∧ π ′ i, true) | π ∧ π ′ SAT}
                          ˆ      ′

   • symb(hµ̂, ρ̂, ξˆ, π i, j)       , {(hµ, ρ, ξˆ′, π i, ς) | ξˆ.alloc (j) → Symb (ξˆ′, ς)}
   • fresh(hµ̂, ρ̂, ξˆ, π i, j)         ,     {(hµ, ρ, ξˆ′, π i, x̂) | ξˆ.alloc (j) → X̂ (ξˆ′, x̂)}

   The concrete/symbolic lifting constructs all of the functions that a state model exposes, with the
help of the action execution function of the parameter concrete/symbolic memories and the alloc
function of the parameter concrete/symbolic allocator. In both cases, the construction of setVar,
setStore, and getStore is straightforward. The remaining cases are described below.
[EvalExpr]. In the concrete case, expression evaluation is performed concretely (we use neo ρ to
denote the standard expression evaluation of e with respect to ρ). In the symbolic case, it amounts
to substituting all the program variables in e with their associated logical expressions given by the
store (we denote this substitution by ρ̂(e)). In the implementation, Gillian’s ﬁrst-order solver applies
a number of algebraic identities to simplify the expression resulting from ρ̂(e). It is also in charge
of discharging satisﬁability/entailment questions (e.g. π ⊢ ê = ê ′ ), by encoding them into the Z3
solver of De Moura and Bjørner [2008].
[Action]. Action execution on states amounts to calling action execution on the parameter mem-
ory. As symbolic actions, unlike concrete actions, may branch, they additionally generate a logical
expression, π ′ , describing the conditions under which the chosen branch is taken. Hence, the path
condition of the obtained state is a conjunction of π ′ with the path condition π of the original state.
[Assume]. The function assume(σ , v) extends the state σ with information that the value v holds. In
the concrete case, assume(σ , b) returns the singleton set containing the original state when b = true
and the empty set otherwise. In the symbolic case, assume(σ̂ , π ′) returns σ̂ with its path condition
strengthened with π ′ if this new path condition is satisﬁable, and the empty set otherwise.
[Symb/Fresh]. The functions symb and fresh generate symbols using the parameter allocator. We
use the arrow parameter of the allocator to indicate the set from which to pick the freshly generated
value: symb picks an uninterpreted and fresh picks an interpreted symbol. As symbolic values are
logical expressions, it makes sense to pick a fresh logical variable when generating a fresh inter-
preted symbol and then later impose constraints on it via the assume function.
8                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

Implementation. The concrete and symbolic state                 module type SMemory = sig
constructors are implemented as OCaml functors,                   type t
                                                                  type a
                                                                                    (** Type of symbolic memories *)
                                                                                    (** Type of actions           *)
respectively parameterised by OCaml modules with                  type vt = LExpr.t (** Type of symbolic values   *)
types CMemory and SMemory (cf. Figure 4). Both                    val ea : a -> t -> vt -> vt -> (t * vt * vt) list
functors are additionally parameterised by a mod-               end
ule with type Allocator for the generation of
                                                                module SState
fresh values. The CMemory and SMemory module                      (SMem : SMemory)
types precisely follow our formal characterisation                (Alloc : Allocator with type vtus = Loc.t
                                                                                      and type vtis = LVar.t) :
of concrete and symbolic state models as per Deﬁni-               (State with type a = SMem.a) = struct
tions 2.3 and 2.4. Furthermore, the functors CState                 type vt = LExpr.t
                                                                    type mt = SMem.t
and SState also follow the concrete and symbolic                    type at = Alloc.t
liftings described in Deﬁnitions 2.5 and 2.6.                       type t = mt * vt Store.t * at * LExpr.t
                                                                    type a = SMem.a
                                                                    ...
2.4    While: Concrete and Symbolic Memories                    end

We show how to instantiate Gillian to obtain a con- Fig. 4. OCaml Signatures: Symbolic Memories
crete/symbolic interpreter for While by combining and States
the While-to-GIL compiler of §2.2 with the con-
crete/symbolic While memory model.
   The ﬁrst step towards deﬁning a memory model is to pick the carrier set of the model, in this
case: the set of While memories. We deﬁne a concrete While memory as a partial mapping from
symbols (corresponding to object locations) and strings (corresponding to property names) to val-
ues; formally: µ ∈ M W : Symb × S ⇀ V. Analogously, we deﬁne a symbolic memory to be a partial
mapping from logical expressions and strings to logical expressions; formally: µ̂ ∈ M̂ W : Ê ×S ⇀ Ê.
Property names are not lifted to logical expressions in the symbolic case, since the While statements
that act on object properties do not allow the property name to be resolved dynamically.
   Having chosen the concrete and symbolic carrier sets, we can now deﬁne the functions ea and ea       ˆ,
for acting on concrete and symbolic memories, respectively. In particular, these functions must
support the actions AW = {lookup, mutate, dispose} introduced in §2.2. The deﬁnition of the While
concrete/symbolic actions is given in Figure 5 (concrete on the left and symbolic on the right), and
is straightforward. In the rules, we use several projection operators: µ ↾l splits the concrete memory
µ into a pair (µ ′, µ ′′ ), where µ ′ contains the memory cells at location l and µ ′′ contains the others;

           C-Lookup                                           S-Lookup
               µ = _ ⊎ l .p 7→ v                                π ⊢ ê = eˆ′        µ̂ = _ ⊎ eˆ′ .p 7→ eˆv
           µ.lookup ([l, p])        (µ, v)                                ˆ p] , π )
                                                              µ̂.lookup ([e,                 {(µ̂, eˆv , true)}

    C-Mutate-Present                               S-Mutate-Present
    µ = µ ′ ⊎ l .p 7→ _ µ ′′ = µ ′ ⊎ l .p 7→ v     π ⊢ ê = eˆ′′ µ̂ = µ̂ ′ ⊎ eˆ′′ .p 7→ _ µ̂ ′′ = µ̂ ′ ⊎ eˆ′′ .p 7→ eˆ′
                                                                              
         µ.mutate ([l,p,v])         (µ ′′ ,v)                          ˆ p, eˆ′ , π )
                                                          µ̂.mutate ( e,                 {(µ̂ ′′ , true, true)}

    C-Mutate-Absent                                       S-Mutate-Absent
    (l, p) < dom(µ) µ ′ = µ ⊎ l .p 7→ v                        µ̂ ↾ê,p, π = ∅ µ̂ ′ = µ̂ ⊎ e.p
                                                                                           ˆ 7→ eˆ′
                                                                                
         µ.mutate ([l,p,v])          (µ ′, v)             µ̂.mutate ( e, ˆ p, eˆ′ , π )  {(µ̂ ′, true, true)}

           C-Dispose                                           S-Dispose
                 µ ↾l = (_, µ ′ )                                           µ̂ ↾ê, π = (_, µ̂ ′ )
           µ.dispose (l)       (µ ′ , true)                                ˆ π)
                                                               µ̂.dispose (e,            {(µ̂ ′, true, true)}

                             Fig. 5. While: Actions in Concrete and Symbolic Memories
Gillian: Compositional Symbolic Execution for All                                                                       9

µ̂ ↾ê, π splits the symbolic memory µ̂ into a pair (µ̂ ′, µ̂ ′′ ), where µ̂ ′ contains the memory cells at
location corresponding to ê under π and µ̂ ′′ contains the others; and µ̂ ↾ê,p, π returns a set of possible
locations in µ̂ corresponding to ê under π that have property p. We describe the rules [C-Dispose]
and [S-Dispose] in detail.
[C-Dispose]. To dispose of the object at location l, we split the memory µ using µ ↾l and return the
part of the memory that does not contain the cells at location l, and the value true. The value true
is returned to comply with the expected type of ea ; it is not used by the compiled code.
[S-Dispose]. Analogously to [C-Dispose], we split the symbolic memory µ̂ using µ̂ ↾ê, π and return
the part of the memory that does not contain the cells corresponding to ê under π , the value true,
and the path condition true. The returned path condition indicates that the action does not branch
and that, therefore, the path condition of the corresponding state will eﬀectively not be updated.

3 PARAMETRIC SOUNDNESS
Proving the soundness of symbolic analyses is a time-
                                                                     Sˆ             RS              S
consuming task that often requires a considerable number
of auxiliary lemmas and deﬁnitions. The complexity of such
proofs becomes unwieldy as we move towards real-world pro- SST                      RT             CST
gramming languages with multiple program constructs and
intricate runtime environments, which tends to detract from          M̂             RM              M
mathematical rigour in favour of less time consuming, but also
                                                                         Fig. 6. Proof Infrastructure
less trustworthy, informal arguments. Gillian streamlines the
development of soundness proofs for the instantiations of the framework, by focussing the user’s
proof eﬀort only on the target language memory and the actions that it exposes.
   We propose a proof infrastructure, illustrated in Figure 6, consisting of: (1) a class of soundness
relations between state models, R S , which are preserved by the semantics of GIL; (2) a class of
soundness relations between memory models, R M , which, when lifted to states, yield relations
in R S ; and (3) the lifting mechanism, RT . With this infrastructure in place, proving the soundness
of a given symbolic semantics in terms of a given concrete semantics amounts to proving that the
soundness relation between the two corresponding memory models is in R M .
   The section is structured as follows: §3.1 describes a class of soundness relations that are pre-
served by the semantics of GIL; §3.2 describes the mechanism for lifting a soundness relation be-
tween memories to a soundness relation between states; and §3.3 shows how to leverage the pro-
posed proof infrastructure to prove the soundness of the While symbolic analysis.

3.1    Parametric Soundness
The standard approach for deﬁning soundness [Cousot and Cousot 1977] can be coarsely described
as in the diagram of Figure 7 (left), where: (1) σ̂1 is an abstract state over-approximating a concrete
state, σ1 ; (2) σ̂2 is the abstract state obtained by abstractly executing a given command on σ̂1 ; and
(3) σ2 is the state obtained by concretely executing the same command on σ1 . In this setting, the
abstract semantics is sound with respect to the concrete one if σ̂2 also over-approximates σ2 .
   In the context of abstract analyses that may branch, this elegant characterisation of soundness
cannot describe what it means for a single abstract trace to be sound. For instance, Figure 7 (mid)
shows a scenario with two possible abstract transitions from the original abstract state. The only
way to ensure that the ﬁnal abstract state over-approximates the ﬁnal concrete state is to merge the
two ﬁnal abstract states,4 forcing us to reason about all possible abstract traces at the same time.

4 The union of abstract states as in the standard collecting semantics [Cousot and Cousot 2004] is a form of merging.
10                José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   We propose a characterisation of soundness that allows us to describe both what it means for a
single abstract trace to be sound independently of all the others and also to recover the standard
notion of soundness when given the set of all possible abstract traces. This property is inspired
by work on symbolic execution [Cadar et al. 2011; Cadar and Sen 2013], where one can talk about
the soundness of single symbolic execution trace by strengthening the path condition of the initial
symbolic state with the path condition of the ﬁnal state. This eﬀectively ﬁlters out all of the initial
concrete states for which the concrete execution diverges from the path of the given symbolic trace.
      σ̂1        RS        σ1        σ̂1       RS         σ1          σ̂1        RS          σ1

                                     σ̂2′         σ̂2′′                       σ̂1 = σ̂1 ⇃σ̂2


      σ̂2        RS         σ2              σ̂2           RS             σ2                σ̂2           RS          σ2
                                            Fig. 7. Soundness Properties
Restriction Operators. As Gillian states are general, we cannot use path conditions as a device to
pinpoint the set of concrete traces that need to be modelled by a given abstract trace. Instead, we
introduce restriction operators on abstract states. Informally, the restriction of an abstract state σ̂1
with another abstract state σ̂2 , written σ̂1 ⇃σ̂2 , denotes the state σ̂1 strengthened with some informa-
tion coming from σ̂2 . In Figure 7 (right), we give further intuition on how we will use restriction:
for example, if σ̂1 over-approximates σ1 and it also holds that σ̂1 = σ̂1 ⇃σ̂2 , meaning that σ̂1 does not
learn anything from σ̂2 , then σ̂2 will also over-approximate σ2 .
   We deﬁne restriction operators algebraically. A restriction operator ⇃: X → X ⇀ X on a set X ,
written x 1 ⇃x 2 for ⇃ (x 1, x 2 ), is a binary associative function satisfying the following properties:
                                                                                       Weakening
             Idempotence               Right Commutativity                                       x 1 ⇃x 2⇃x3 = x 1
             x ⇃x = x                  (x 1 ⇃x 2 ) ⇃x 3 = (x 1 ⇃x 3 ) ⇃x 2
                                                                      x 1 ⇃x 2 = x 1 ∧ x 1 ⇃x 3 = x 1
meaning that self-restriction does not gain information, the order of applied restrictions does not
inﬂuence the accumulated information gain, and that if x 1 cannot gain information from the com-
bined knowledge of x 2 and x 3 , then it cannot gain information from either x 2 or x 3 . It is easily
veriﬁable that every restriction operator ⇃: X → X ⇀ X induces a pre-order (X , ⊑), given by
x 1 ⊑ x 2 ⇐⇒ x 1 ⇃x 2 = x 1 .
   A restriction operator on states ⇃: |S | → |S | ⇀ |S | is said to be preserved by a state model
S = h|S |, V , Ai if all of the state-generating functions exposed by the state model are monotonic
with respect to the pre-order induced by ⇃; put formally:
  RMono-SetVar                          RMono-SetStore                                    RMono-Action
  σ .setVar(x, v) = σ ′ =⇒ σ ′ ⊑ σ      σ .setStore(ρ) = σ ′ =⇒ σ ′ ⊑ σ                   σ .α (v) (σ ′, −) =⇒ σ ′ ⊑ σ

   We say that ⇃ is a restriction operator on a state model S = h|S |, V , Ai, if ⇃ is a restriction operator
on the carrier set |S | and ⇃ is preserved by S. Restriction operators are extended from states to
conﬁgurations straightforwardly: hp, σ , cs, ii ⇃ hp, σ ′, −, −i , hp, σ ⇃σ ′ , cs, ii.
Compatibility. In the following, we assume a pre-order ≤ on abstract states, writing σ̂2 ≤ σ̂1 to
mean that the models of σ̂2 are contained in the models of σ̂1 (we say that σ̂2 is more precise than σ̂1 ).
This pre-order may diﬀer from that induced by the chosen restriction operator on abstract states.
Consider the symbolic execution setting: the fact that the path condition of a state σ̂2 implies the
path condition of a state σ̂1 does not necessarily mean that all the models of σ̂2 are contained in the
models of σ̂1 , as these two states may describe diﬀerent memories. However, the chosen restriction
operator must be compatible with the pre-order on states. Formally, we say that a pre-order (X , ≤)
is compatible with a restriction operator ⇃ on X iﬀ the following properties hold:
Gillian: Compositional Symbolic Execution for All                                                                                 11

                                                        ≤-⇃ Compatibility                        Strengthening
                ⇃-≤ Compatibility                       x1 ≤ x2                                  x 1 ≤ x 1′   x 2 ⊑ x 2′
                x 1 ⇃x 2 ≤ x 1
                                          x1 ⊑ x2                       x 1 ⇃x 2 ≤ x 1′ ⇃x 2′
   These properties essentially describe that restriction increases ≤-precision, that ≤-precision im-
plies ⊑-precision, and how ≤-precision and ⇃ combine under ⊑-precision. Unsurprisingly, the pre-
order ⊑ induced by ⇃ is indeed compatible with ⇃.
Soundness Relations. We are now in the position to describe the class of soundness relations that
are preserved by the semantics of GIL. This class is formally given in Deﬁnition 3.1, which makes
use of the notion of induced pre-order. Formally, given a relation ∼ ∈ X × Y between two sets X
and Y , the pre-order on X induced by ∼, written ≤∼ , is deﬁned as follows: x 1 ≤∼ x 2 if and only if
{y | x 1 ∼ y} ⊆ {y | x 2 ∼ y}. We elide the ∼ in ≤∼ when it is clear from the context.

    Deﬁnition 3.1 (Soundness Relation - States). Given two state models, Sˆ = h|Sˆ|, V̂ , Ai and S =
h|S |, V , Ai, a soundness relation SR for Sˆ with respect to S is a triple h⇃, ∼s , ∼v i, consisting of: (1) a
restriction operator ⇃ on S;  ˆ (2) a binary relation ∼s ⊆ |Sˆ| × |S |; and (3) a ternary relation ∼v ⊆
 ˆ
|S | × V̂ × V , such that ⇃ is compatible with the pre-order induced by ∼s (denoted by ≤) and the
following constraints hold:
       Store                                                    EvalExpr
       σ̂ ∼s σ =⇒ σ̂ ⊢ σ̂ .store ∼v σ .store                    σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ =⇒ σ̂ ′ ⇃σ̂ ⊢ σ̂ ′ .ee (e) ∼v σ .ee (e)

      SetVar                                                               SetStore
       σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ v̂ ∼v v                                   σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ ρ̂ ∼v ρ
           =⇒ σ̂ ′ .setVar(x, v̂) ⇃σ̂ ∼s σ .setVar(x, v)                        =⇒ σ̂ ′ .setStore(ρ̂) ⇃σ̂ ∼s σ .setStore(ρ)

   Action                                                                                             Weakening
        σ̂ ′ .α (v̂) (σ̂ ′′ , v̂ ′ ) ∧ σ̂ ≤ σ̂ ′ ⇃σ̂ ′′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ v̂ ∼v v                       σ̂ ⊑ σ̂ ′ ∧ σ̂ ⊢ v̂ ∼v v
       =⇒ ∃ σ ′, v ′ . σ .α (v)          (σ ′, v ′) ∧ σ̂ ′ ⇃σ̂ ∼s σ ′ ∧ σ̂ ′ ⇃σ̂ ⊢ v̂ ′ ∼v v ′                =⇒ σ̂ ′ ⊢ v̂ ∼v v

where σ̂ ⊢ ρ̂ ∼v ρ is shorthand for: dom(ρ̂) = dom(ρ) = X and ∀x ∈ X . σ̂ ⊢ ρ̂(x) ∼v ρ(x).

   In a nutshell, if SR = h⇃, ∼s , ∼v i is a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in terms of S =
h|S |, V , Ai, then: (1) σ̂ ∼s σ means that σ̂ is an over-approximation of σ , and (2) σ̂ ⊢ v 1 ∼v v 2 means
that, considering the information in σ̂ , v 1 is an over-approximation of v 2 . The constraints imposed
on the state functions guarantee that ∼s and ∼v are preserved by the GIL interpreter. Below, we
discuss the Action and Weakening constraints; the other ones can be understood analogously.
[Action]. This constraint states that if we have an abstract action execution σ̂ ′ .α (v̂)            (σ̂ ′′, v̂ ′),
then, for any abstract state σ̂ , concrete state σ , and concrete value v, such that: (1) σ̂ ≤ σ̂ ′ ⇃σ̂ ′′
(meaning that σ̂ is more precise than the original state σ̂ ′ restricted to the ﬁnal state σ̂ ′′ ), (2) σ̂ ∼s σ
(meaning that σ̂ is an over-approximation of σ ), and (3) σ̂ ⊢ v̂ ∼v v (meaning that, according to
σ̂ , v̂ is an over-approximation of v); then, there must exist a concrete state σ ′ and a concrete value
v ′, such that: (i) σ .α (v)   (σ ′, v ′), (ii) σ̂ ′ ⇃σ̂ ∼s σ ′ (meaning that the restriction of the ﬁnal state,
σ̂ to σ̂ is an over-approximation of the ﬁnal concrete state, σ ′ ), and (iii) σ̂ ′ ⇃σ̂ ⊢ v̂ ′ ∼v v ′ (meaning
   ′

that v̂ ′ is an over-approximation of v ′ according to σ̂ ′ ⇃σ̂ ).
[Weakening]. This constraint states that, if σ̂ is more ⊑-precise than σ̂ ′ and, according to σ̂ , v̂ is
an over-approximation of v, then v̂ is also an over-approximation of v according to σ̂ ′.
   Next, Theorem 3.2 states that the semantics of GIL preserves soundness relations. It uses the
standard liftings of ∼v , ∼s , and ≤∼s to call stacks and conﬁgurations (cf. Appendix B).
12                    José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   Theorem 3.2 (Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in
terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                  ′          ′′          ′                                                              ′′
              cfˆ     ∗
                          cfˆ ∧ cfˆ ≤ cfˆ ⇃cfˆ ′′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf              ∗
                                                                                              cf ′ ∧ cfˆ ⇃cfˆ ∼s cf ′
                                      ′
     From there, by choosing cfˆ ≡ cfˆ ⇃cfˆ ′′ , we obtain the desired soundness result.

   Corollary 3.3 (Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in
terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                                        ′                                                         ′
                          cfˆ    ∗
                                     cfˆ ∧ (cfˆ ⇃cfˆ ′ ) ∼s cf =⇒ ∃ cf ′ . cf       ∗
                                                                                        cf ′ ∧ cfˆ ∼s cf ′
   This corollary states that, if we have an abstract GIL trace and the initial concrete conﬁguration cf
is over-approximated by the initial abstract conﬁguration strengthened with the information of the
ﬁnal abstract conﬁguration, then there exists a concrete GIL trace starting from cf such that the
ﬁnal abstract conﬁguration is an over-approximation of the ﬁnal concrete conﬁguration.

3.2     Concrete-Symbolic Soundness
We identify a class of relations between symbolic memory models and concrete memory models
from which one can construct soundness relations between the corresponding symbolic state mod-
els and concrete state models.
Symbolic Memory Interpretation. Intuitively, a symbolic memory model M̂ = h|M̂ |, A, ea             ˆ i is
related to a concrete memory model M = h|M |, A, ea i, if there is an interpretation function I
mapping the memories in |M̂ | to memories in |M |. Memory interpretation must preserve actions,
meaning that: if an action can be executed in a given symbolic memory µ̂ under a path condition π ,
then it can also it can also be executed in any interpretation of µ̂ that satisﬁes both the original path
condition, π , and the path condition generated by the action, π ′ . Furthermore, the output concrete
memory must be an interpretation of the output symbolic memory. The notion of interpretation is
made precise in Deﬁnition 3.4.
                                                                                                  ˆi
   Deﬁnition 3.4 (Symbolic Memory Interpretation). Given a symbolic memory model M̂ = h|M̂ |, A, ea
and a concrete memory model M = h|M |, A, ea i, an interpretation of M̂ with respect to M is a func-
tion I : |M̂ | → (X̂ ⇀ V) ⇀ |M | such that:
                            µ̂.α (ê, π )    (µ̂ ′, ê ′, π ′ ) ∧ µ = I(µ̂, ε) ∧ nπ ∧ π ′ oε = true
                                                                                                                        (1)
                                            =⇒ ∃ µ ′ . µ ′ = I(µ̂ ′, ε) ∧ µ.α (nêoε ) = (µ ′, nê ′oε )
   Note that the interpretation function is parametric on a logical environment, ε, which maps sym-
bolic variables to concrete values. Onward, we write nêoε to denote interpretation of logical expres-
sions under ε, deﬁned in the standard way.
Allocator Interpretation and Restriction. Before we proceed to the lifting of memories to states,
we introduce the notions of interpretation and restriction for allocators. The interpretation is straight-
forwardly deﬁned as follows.
                                                                                  ˆ = h|AL|,
   Deﬁnition 3.5 (Symbolic Allocator Interpretation). Given a symbolic allocator AL      ˆ V̂ i and
                                                            ˆ with respect to AL is a function IAL :
a concrete allocator AL = h|AL|, V i, an interpretation of AL
  ˆ → (V̂ ⇀ V ) ⇀ |AL| such that:
|AL|
     ξˆ.alloc (j) →Y (ξˆ′, v̂) ∧ ξ = IAL (ξˆ, ε) =⇒ ∃ ξ ′ . ξ ′ = IAL (ξˆ′, ε) ∧ ξ .alloc (j) →ε (Y ) (ξ ′, ε(v̂))
  On the other hand, restriction is more involved. A restriction operator on allocator records, ⇃:
|AL| → |AL| ⇀ |AL|, is deﬁned algebraically, in the same way as in §3.1. The intuition behind
Gillian: Compositional Symbolic Execution for All                                                              13

it, however, is diﬀerent. In this setting, it makes sense to talk about ξ ⇃ξ ′ only if ξ ′ has allocated
the same values as ξ , and possibly more. Then, ξ ⇃ξ ′ describes an allocator record that necessarily
follows the allocation of ξ ′ on values already allocated by ξ ′ , but not yet by ξ .
    A restriction operator is said to be preserved by an allocator AL = h|AL|, V i if it satisﬁes the
following two properties:

                                                                    FutureToPastAlloc
             RMono-Alloc
                                      ′                   ′         ξ .alloc (j) →Y (ξ ′, v) ∧ ξ ′′ ⊑ ξ ⇃ξ ′
             ξ .alloc (j) →Y (ξ , v) =⇒ ξ ⊑ ξ
                                                                       =⇒ ξ ′′ .alloc (j) →Y (ξ ′ ⇃ξ ′′ , v)

We say that ⇃ is a restriction operator on an allocator AL = h|AL|, V i, if ⇃ is a restriction operator
on the carrier set |AL| and ⇃ is preserved by AL.
   We turn our attention now to the [FutureToPastAlloc] property,               ξ             ξ ⇃ξ ′
which merits further discussion. In §3.1, we showed how to use re-
striction to transfer state-level information from the ﬁnal abstract          j       =⇒          j
state to the initial abstract state in order to ﬁlter out initial concrete  (ξ ′, v)        (ξ ′, v)
states for which the concrete execution diverges from the given ab-
stract trace. Here, similarly, restriction allows us to use future allo- Fig. 8. [FutureToPastAlloc]
cation information to direct present allocation to the desired traces. This is essential, as both the
allocation of locations and symbolic variables can be non-deterministic. We discuss a simpliﬁed
version of [FutureToPastAlloc] given diagrammatically in Figure 8; the full version is a straight-
forward generalisation. This property states that, if we allocate using ξ at site j and obtain ξ ′ and a
value v, then allocation using ξ restricted to ξ ′ at the same site must yield the same allocator and
the same value. Combined with the deﬁnition of the lifting from memories to states, given shortly,
this property eﬀectively directs concrete allocation to the appropriate traces.
Lifting Interpretations. Given an interpretation I : |M̂ | → (X̂ ⇀ V) ⇀ |M | of a symbolic mem-
                           ˆ i in terms of a concrete memory model M = h|M |, A, ea i, the candidate
ory model M̂ = h|M̂ |, A, ea
soundness relation RT (I) = h⇃, ∼s , ∼v i for SST(M̂) in terms of CST (M) is deﬁned as follows:

                       hµ̂, ρ̂, ξˆ, π i ⇃ h_, _, ξˆ′, π ′ i   ,   hµ̂, ρ̂, ξˆ ⇃ξˆ′ , π ∧ π ′ i
                       σ̂ ∼s σ                                ,   ∃ ε . (σ , ε) ∈ Mod(σ̂ )
                       h_, _, _, π i ⊢ ê ∼v v                ,   ∃ ε . nπ oε = true ∧ nêoε = v

where:
                         n                                                                                o
  Mod(hµ̂, ρ̂, π , ξˆi) , (hµ, ρ, ξ i, ε) | nπ oε = true ∧ µ = I(µ̂, ε) ∧ ρ = nρ̂oε ∧ ξ = IAL (ξˆ, n.oε )

   Theorem 3.6 states that, given a memory interpretation I, RT (I) is a soundness relation as per
Deﬁnition 3.1. Hence, we conclude, appealing to Theorem 3.2, that RT (I) is preserved by the se-
mantics of GIL. This means that, in order to prove the soundness of their analyses, the users of
Gillian only have to provide an interpretation function linking their symbolic memories to their
concrete memories and prove that that interpretation preserves the actions exposed by the memo-
ries, meaning that they must satisfy Equation 1.

   Theorem 3.6 (Soundness Relation - Lifting). Let I be an interpretation of a symbolic memory
model M̂ in terms of a concrete memory model M; then, RT (I) = h⇃, ∼s , ∼v i is a soundness relation
for SST (M̂) in terms of CST (M).
14                 José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

3.3     While: Sound Symbolic Analysis
The interpretation of While symbolic memories in terms of While concrete memories, IW , is induc-
tively deﬁned as follows:
                            Cell                                      Union
       Empty                  l = nêoε       v = nê ′ oε            µ 1 = IW (µ̂ 1 , ε)       µ 2 = IW (µ̂ 2 , ε)
       IW (∅, ε) , ∅                      ′
                            IW (ê.p 7→ ê , ε) , l .p 7→ v                IW (µ̂ 1 ⊎ µ̂ 2 , ε) , µ 1 ⊎ µ 2
This interpretation is standard: While memories are interpreted piecemeal and the interpretations
are composed together using the disjoint union operator.
  Lemma 3.7 states that IW preserves the actions of While, AW = {lookup, mutate, dispose}. Its
proof is straightforward, requiring only a case analysis on the rules given in Figure 5. This is much
simpler than the customary inductive proofs on semantic derivations, which underpin standalone
soundness proofs.
     Lemma 3.7 (While: Memory Interpretation). IW is an interpretation of M̂ W with respect to M W .
     We conclude with the instantiation of Theorem 3.2 to While.
     Theorem 3.8 (While: Soundness). Given h⇃, ∼s , ∼v i = RT (IW ), it holds that:
                   cfˆ   ∗ ˆ′     ˆ
                         W cf ∧ (cf ⇃cfˆ ′ ) ∼s cf   =⇒ ∃ cf ′ . cf      W cf
                                                                                ′
                                                                                    ∧ cfˆ ′ ∼s cf ′

4     PARAMETRIC VERIFICATION
We extend the semantics of GIL with support for separation logic (SL) speciﬁcations. This allows the
general semantics to: (i) use SL speciﬁcations to jump over procedure calls instead of re-executing
a procedure at each call site; and (ii) use symbolic execution to verify SL speciﬁcations eﬃciently
instead of re-implementing an SL proof system from scratch. To achieve this, we introduce a para-
metric assertion language, whose semantics is deﬁned in terms of an underlying state model. In this
way, users of Gillian gain access to an out-of-the-box veriﬁcation tool for their target languages,
while only having to provide a minimal description of their own speciﬁc assertions (onward, core
predicates) in terms of the actions of the state model.
   The section is structured as follows: §4.1 discusses the type of veriﬁcation guarantee that can be
obtained from the analysis presented in §2 and its main shortcomings; §4.2 presents our parametric
assertion language together with its semantics; §4.3 describes the extension of the semantics of GIL
to account for the use of SL-speciﬁcations and predicates; and, ﬁnally, §4.4 shows how to leverage
the proposed infrastructure to obtain a veriﬁcation tool for While.

4.1 Naïve Verification
The symbolic analysis presented in §2 is sound in the following sense: if we pick a concrete execu-
tion that follows the same path as that of the given symbolic execution and if the initial symbolic
state is an over-approximation of the initial concrete state; then, we are guaranteed to terminate
in a concrete state that is also over-approximated by the ﬁnal symbolic state. The key point here
is that we are only referring to concrete executions that follow the same path as that of the given
symbolic execution; nothing is said about the others.
   Note, however, that if the symbolic execution does not branch, then no restriction needs to be
imposed on the corresponding concrete executions. This intuition is captured by Theorem 4.1, be-
low, using the notion of restriction (cf. §3.1): essentially, a symbolic execution is guaranteed not to
branch if the initial symbolic state is as ⊑-precise as the ﬁnal symbolic state.
Gillian: Compositional Symbolic Execution for All                                                                       15

   Theorem 4.1 (Naïve Verification). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai
in terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                              ′           ′                                               ′
                cfˆ    ∗
                           cfˆ ∧ cfˆ ⊑ cfˆ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf        ∗
                                                                                 cf ′ ∧ cfˆ ∼s cf ′
   Theorem 4.1 gives us a standard veriﬁcation guarantee for programs that do not branch. Most
programs, however, do branch and are, therefore, not in the conditions of the theorem. To account
for branching, we need a mechanism for merging symbolic execution traces. With such a mecha-
nism, one can re-interpret Theorem 4.1 as follows: if a concrete execution follows the same path as
that of one of the symbolic execution traces that are merged together in the given symbolic trace,
then the conclusions of the theorem hold.
   In general, merging symbolic traces is not easy, as diﬀerent traces may describe diﬀerent struc-
tures in memory. In the symbolic execution literature, many techniques address this problem, such
as predicate abstraction [Jhala and McMillan 2006; Pasareanu et al. 2007] or the combination of
guarded unions with carefully crafted merging algorithms [Torlak and Bodík 2014]. Here, we use SL
predicates for describing inductive data structures in memory, allowing us to fold symbolic traces
that operate on diﬀerent unfoldings of the same data structure.

4.2 Parametric Assertion Language
Given a set of core predicates ∆ to be provided by the GIL Parametric Assertions
user of the framework, GIL assertions, P, Q ∈ A ∆ ,
                                                              P, Q ∈ A ∆ , emp | π | δ hei | pn(e) | P ∗ Q
include: the empty memory assertion emp, boolean
logical expressions, π ∈ Π, core predicate assertions,        pred   ∈ Pred , pred pn(x) :− P0 ; ... ; Pn
δ hei with δ ∈ ∆, user-deﬁned predicate assertions, ω ∈ ΩV , pn(v), where v ∈ V
pn(e) (where pn ∈ PN ⊂ S, the set of predicate
names), and the standard separating conjunction, P ∗ Q. User-predicate deﬁnitions are of the form
pred pn(x) :− P0 ; ... ; Pn where: pn is the predicate name, x its argument, and P0 , ..., Pn are n alterna-
tive predicate deﬁnitions, each a GIL assertion. This is a presentational simpliﬁcation, as predicates
in general can have more than one argument. To model folded predicate assertions in a state with
values v ∈ V , we introduce the notion of value predicates. A value predicate ω ∈ ΩV , is a pair
(pn, v), written pn(v) for legibility, consisting of a predicate name, pn, and a value, v. Onward, we
refer to value predicates simply as predicates.
Predicate States. Unsurprisingly, in order to deﬁne the interpretation of assertions, we require that
the carrier set of the parameter state model, |S |, forms a partial commutative monoid [Calcagno et al.
2007], under a given composition operator, ◦, and neutral element ∅. Furthermore, we require all
the state-generating functions to be frame preserving. Put formally:
   Frame-SetVar                          Frame-SetStore                          RMono-Action
       σ .setVar(x, v) = σ ′                 σ .setStore(ρ) = σ ′                    σ .α (v) (σ ′, −)
   (σ ◦ σf ).setVar(x, v) = σ ′ ◦ σf      (σ ◦ σf ).setStore(ρ) = σ ′ ◦ σf       (σ ◦ σf ).α (v)      ((σ ′ ◦ σf , −)
Finally, we extend a given state model with support for predicates. We say that a state model sup-
ports predicates if it exposes an action getP for recovering a given predicate from the state and an
action setP for adding a new predicate to the state. Given an arbitrary state model S = h|S |, V , Ai,
we construct a new state model with support for predicates by coupling |S | with a list of predicates
ω ∈ ΩV . There, getP simply removes the required predicate from ω, while setP adds it to ω. This
lifting is formally described below.
  Deﬁnition 4.2 (Predicate State Constructor (PST )). The predicate state constructor PST : S → S is
deﬁned as PST (h|S |, V , Ai) , h|S ′ |, V , A ⊎ {setP, getP}i, where:
16                   José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

     • |S ′ |                        ,   |S | × ΩV
     • setVarp (hσ, ωi, x, v)        ,   hsetVar(σ, x, v), ωi
     • setStorep (hσ, ωi, ρ)         ,   hsetStore(σ, ρ), ωi
     • storep (hσ, −i)               ,   store(σ )
     • eep (hσ, −i, e)               ,   ee(σ, e)
     • eap (α, hσ, ωi, v)            ,   {(hσ ′, ωi, v ′) | (σ ′,v ′ ) ∈ ea(α, σ, v)}, if α < {getP, setP}
     • eap (setP, hσ, ωi, [pn, v])   ,   (hσ, (pn(v) : ω)i, −)
     • eap (getP, hσ, ωi, [pn, v])   ,   (hσ, ω 1 ++ ω 2 i, −), where ω = ω 1 ++ [ pn(v) ] ++ ω 2

Core Predicate Interpretation. In order to deﬁne the semantics of their assertions, the users of
the framework need to describe the meaning of their core predicates in terms of the actions exposed
by the parameter state model. Informally, each core predicate δ ∈ ∆ is associated with two actions:
(i) the getter action, getδ , for recovering its footprint from the state; and (ii) the setter action, setδ ,
for extending the state with the footprint of the core predicate.

   Deﬁnition 4.3 (Core Predicate Action Interpretation). A core predicate action interpretation is a
4-tuple AI ∈ AI = h∆, A, set, дeti consisting of a set of core predicates ∆, a set of actions A, and
two functions set, дet : ∆ → A; we write setδ for set(δ ) and getδ for дet(δ ). A core predicate action
interpretation h∆, A, set, дeti is said to be well-formed with respect to a state model S = h|S |, V , Ai
if and only if, for all core predicates δ ∈ ∆, it holds that:

                                     σ .getδ (v)     σ ′ ⇐⇒ σ ′ .setδ (v)           σ                                  (2)

   This well-formedness constraint captures the intuition behind getters and setters and states that
they have to be, essentially, each other’s inverses.
   Given a state model S = h|S |, V , Ai and a core action interpretation h∆, A, set, дeti, the induced
action interpretation of an assertion P ∈ A ∆ is a pair of functions consisting of the getter and setter
of P, respectively, getP and setP . Formally, Figure 9 deﬁnes two induced functions:
     • set ∆S : A ∆ → |S | → (X̂ ⊎ X ⇀ V ) ⇀ |S |                         (σ ′ = set ∆S (P, σ , θ ) ≡pp σ .setP (θ )   σ ′)
     • дet ∆S : A ∆ → |S | → (X̂ ⊎ X ⇀ V ) ⇀ |S |                        (σ ′ = дet ∆S (P, σ , θ ) ≡pp σ .getP (θ )    σ ′)

mapping each assertion P ∈ A ∆ to its getter and setter, respectively. The deﬁnition makes use of a
substitution, θ , essentially a function mapping variables and logical variables to values.

   Lemma 4.4 states that, if we are given a well-formed core predicate interpretation, the induced
getter and setter of every assertion P satisfy the well-formedness constraint stated in Equation 2.
Finally, Theorem 4.5 establishes that assertion interpretation preserves soundness relations. Hence,
if we execute the getter/setter of a given assertion P in a given abstract state, and if we are given
an initial concrete state that is over-approximated by the initial abstract state strengthened with
the information of the ﬁnal abstract state, then the concrete execution of the getter/setter of P will
yield a ﬁnal state that is over-approximated by the ﬁnal abstract state.

   Lemma 4.4 (Assertion Interpretation). Let h∆, A, set, дeti be a well-formed core predicate in-
terpretation with respect to a predicate state model S = h|S |, V , Ai; then, it holds that: σ .setP (θ ) σ′
                ′
if and only if σ .getP (θ )  σ.

   Theorem 4.5 (Assertion Interpretation - Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness
relation for Sˆ = h|Sˆ|, V̂ , Ai in terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s ; and let
Gillian: Compositional Symbolic Execution for All                                                                                   17

        set - star                     get - star                           set - boolean expr        get - boolean expr
           σ .set P (θ)       σ′         σ .get P (θ)         σ′               σ .ee (θ(e)) = v       σ .ee (¬ θ(e)) = v
          σ ′ .setQ (θ)       σ ′′      σ ′ .getQ (θ)         σ ′′          σ .assume (v)       σ′    σ .assume(v) = ∅
        σ .set (P ∗Q ) (θ)     σ ′′    σ .get(P ∗Q ) (θ)       σ ′′           σ .set π (θ)   σ′        σ .get π (θ)        σ

      set - pred                         get - pred                     set - core pred                 get - core pred
      σ .ee ([pn, θ(e)]) = v             σ .ee ([pn, θ(e)]) = v           σ .ee (θ(e)) = v                σ .ee (θ(e)) = v
        σ .setP (v)     σ′                 σ .дetP (v)     σ′            σ .setδ (v)    σ′               σ .getδ (v)     σ′
       σ .set pn(e ) (θ)     σ′           σ .get pn(e ) (θ)      σ′     σ .setδ he i (θ)     σ′         σ .getδ he i (θ)       σ′
                           Fig. 9. Assertion Interpretation: σ .setP (θ)            σ ′ and σ .get P (θ)     σ′

h∆, A, set, дeti be a well-formed core predicate action interpretation for Sˆ and S; then, it holds that:
                                         ˆ
                              σ̂ .set P (θ)  σ̂ ′ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                                                                                                                                    (3)
                                           =⇒ ∃ σ ′ . σ .setP (θ )         σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
                                        ˆ
                              σ̂ .getP (θ)   σ̂ ′ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                                                                                                                                    (4)
                                           =⇒ ∃ σ ′ . σ .getP (θ )         σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′

Implementation. The predicate state constructor is implemented as an OCaml functor param-
eterised by an OCaml module of type State. The PState functor precisely follows the lifting de-
scribed in Deﬁnition 4.2: the action type of the returned state extends the action type of the parame-
ter state with the actions getP and setP of the formalism. We also deﬁne the module type CorePred,
describing core predicate action interpretations. CorePred modules must deﬁne the getter and
setter functions, mapping core predicates to their corresponding getter and setter actions.
 type 'a pred_act = GetP | SetP | OtherAct of 'a
                                                                      module type CorePred = sig
 module PState (St : State) :                                             type a (** Type of actions         *)
   (State with type a = St.a pred_act) = struct                           type t (** type of core predicates *)
     type vt = St.vt
     type t = St.t * (PName.t * vt) list                                    val getter : t -> a
     type a = St.a pred_act                                                 val setter : t -> a
     ...                                                              end
 end
                                         Fig. 10. OCaml Predicate State Constructor

4.3   Parametric Verification Semantics
We extend the syntax of GIL commands with logical commands for interacting with predicate asser-
tions and speciﬁcations in state models with support for predicates. Besides the original commands
c ∈ CA , we include: a command fold pn(e) with [j; (x̂ i : ei ) |in=0 ] for folding the predicate denoted
by pn(e)5 ; a command unfold pn(e) for unfolding the predicate denoted by pn(e); and, a command
x := e 1 (e 2 ) with [j; (x̂ i : ei ) |in=0 ] for executing the procedure denoted by e 1 with the argument de-
noted by e 2 using the procedure speciﬁcation instead of executing the body of the procedure. Observe
that the standard procedure call command remains part of the syntax, as it is included in c ∈ CA ;
to avoid confusion, we refer to the logical procedure call as spec call. Finally, we write p and proc
to respectively denote GIL programs and procedures that use logical commands.
Extended GIL Syntax
 c ∈ C A , c ∈ CA | x := e 1 (e 2 ) with [j; (x̂i : ei ) |in=0 ] |                                proc ∈ Proc A , proc f (x){c}
           fold pn(e) with [j; (x̂i : ei ) |in=0 ] | unfold pn(e)                                 p ∈ Proд : F ⇀ Proc A
                                                                                                           A


5 (ignoring the additional symbolic paraphernalia for the moment)
18                       José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   GIL speciﬁcations have the form {P } f (x) {Q, e}, where P and Q are the pre- and post-condition
of the procedure with identiﬁer f and parameter x, and e denotes its return value. Procedures
are allowed to have multiple speciﬁcations; we use p.specs.f .j to refer to the j-th speciﬁcation
of the procedure with identiﬁer f in the program p. Note that both speciﬁcations and predicate
deﬁnitions may include logical variables. Accordingly, the fold and spec call commands allow the
programmer to provide the appropriate bindings for these variables. At the implementation level,
Gillian includes a search algorithm that automatically ﬁnds the appropriate bindings. A description
of this algorithm, however, is out of the scope of this paper.
   An excerpt of the semantics of GIL logical commands is given in Figure 11 (cf. Appendix C). The
rules have the same structure as those of GIL commands (given in Figure 1). Below, we give a brief
description of their behaviour.

  Fold                                                         Spec Call
                                                      n                                                                     n
  cmd(p, cs, i) = fold pn(e0 ) with [j; (x̂ i : ei ) |i=1  ]           cmd(p, cs, i) = x := e(e0 ) with [j; (x̂ i : ei ) |i=1  ]
                                       n                                                                                n
                  (v i = σ .ee (ei )) |i=0                                    f = σ .ee (e)       (v i = σ .ee (ei )) |i=0
      p.preds.pn = pred pn(x ) :− P 0 ; ... ; P n                                p.specs.f .j = {P } f (x 0 ) {Q, e ′ }
      θ = [x 7→ v 0, x̂ 1 7→ v 1, ..., x̂ n 7→ v n ]                               θ = [x 0 7→ v 0, ..., x̂ n 7→ v n ]
  σ .get P j (θ )   σ′      σ ′ .set P ([pn, v])       σ ′′    σ .ee (θ (e ′ )) = v      σ .getP (θ )     σ′       σ ′ .setQ (θ )   σ ′′
                                    ′′                                                             ′′
             p ⊢ hσ, cs, i i     hσ , cs, i+1i                            p ⊢ hσ, cs, i i      hσ .setVar(x, v), cs, i+1i
                                                                                                        ′
                    Fig. 11. Verification Semantics of GIL: p ⊢ hσ, cs, iio                 hσ ′, cs ′, jio (excerpt)

[Fold]. The rule folds the predicate denoted by pn(e). First, it obtains the j-th deﬁnition of the
predicate to be folded, P j , and uses its getter, getP j , to remove the corresponding footprint from the
current state; then, it uses the action setP to extend the current state with the folded predicate.
[Spec Call]. The rule executes the procedure with the identiﬁer denoted by e with the argument
denoted by e 0 using its j-th speciﬁcation. In order to “execute” the procedure, it uses the getter of
the precondition, getP , to remove the corresponding footprint from the current state, and the setter
of the postcondition, setQ , to produce the corresponding footprint in the obtained state.

   Finally, Theorem 4.6 states that the execution of logical commands preserves correctness rela-
tions. At ﬁrst glance, it coincides with the Naïve Veriﬁcation Theorem (Theorem 4.1). However,
since logical commands oﬀer us a mechanism to merge symbolic traces together, the theorem is
applicable to programs which branch and loop.

   Theorem 4.6 (Verification). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in
terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                                  ′                                                                         ′
                   cfˆ     ∗
                               cfˆ ∧ cfˆ = cfˆ ⇃cfˆ ′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf              ∗
                                                                                                  cf ′ ∧ cfˆ ∼s cf ′

4.4    While: Verification
The only core predicate for While is the cell([l, p, v]) predicate, whose footprint is a single heap cell
and which states that the property p of the object at location l has value v. We also introduce the
setter and the getter actions for the cell core predicate, setCell and getCell. The rules for setCell are
given below (cf. Appendix C). One can observe that those rules are similar to the rules of mutate,
except that they produce the resource of the cell core predicate. In fact, we could have chosen to have
only setCell and getCell, but pay the price of complicating While-to-GIL to pre-emptively remove
the resource that setCell produces and re-produce the resource that getCell consumes, cluttering
the presentation.
Gillian: Compositional Symbolic Execution for All                                                                              19

                    C-SetCell                                     S-SetCell
                    (l,p) < dom(µ)        µ ′ = µ ⊎ l .p 7→ v         µ̂ ↾êl ,p, π = ∅         µ̂ ′ = µ̂ ⊎ eˆl .p 7→ eˆv
                       µ.setCell ([l,p,v])       (µ ′, true)       µ̂.setCell ([eˆl , p, eˆv ] , π )    {(µ̂ ′, true, true)}

  In summary, we have that ∆W = {cell} and AW = {lookup, mutate, dispose, setCell, getCell} and
proceed to state the property required for Theorem 4.6 to hold for While.

  Lemma 4.7 (While: Core Predicate Interpretation). The core predicate action interpretation
h∆W , AW , [cell 7→ setCell], [cell 7→ getCell]i is well-formed with respect to CST (M W ) and SST(M̂ W ).

5     PARAMETRIC BI-ABDUCTIVE ANALYSIS
Bi-abductive symbolic analyses are quickly becoming the gold-standard of automatic compositional
testing [O’Hearn 2018]. These analyses allow developers to ﬁnd bugs in their code even when no
speciﬁcations or (unit) tests are given. The foremost example of this is Infer [Calcagno et al. 2015],
a fully automatic compositional tool aimed at lightweight bug-ﬁnding for static languages (C, C++,
Java, Objective C), which is part of the code review pipeline at Facebook.
   Bi-abductive analyses symbolically analyse one procedure at a time, relying on a built-in mecha-
nism for automatic inference of resource when the footprint of the command at hand is not part of
the current state. We extend Gillian with a parametric bi-abductive analysis that only requires the
parameter state model to expose a minimal mechanism for inferring missing resource, while the
bi-abductive analysis keeps track of all the generated ﬁxes and combines them to generate a set of
speciﬁcations describing the behaviour of the analysed procedure up to a bound.
   The section is structured as follows: §5.1 presents our parametric bi-abductive analysis; and §5.2
shows how to instantiate it for the While language.

5.1    Parametric Bi-abductive Analysis
Instead of redesigning a bi-abductive analysis from scratch, we maintain the semantics of GIL un-
altered and, instead, instrument the parameter state model with a mechanism for on-the-ﬂy correc-
tion of action errors during execution. This approach streamlines the formalism, avoiding redun-
dancy, and leads to a modular implementation, which has no code duplication.
Action Fixes. The ﬁrst step toward having automatic error correction is the appropriate modelling
of action errors. To this end, we modify the signature of the action execution function, ea, exposed
by every state model, in order to account for the cases in which the resource required by the pa-
rameter action, α, is not part of the given state.
      • ea : A → |S | → V ⇀ ℘(|S | × V ) ⊎ ℘(A ∆ )                      ((σ ′, v ′) ∈ ea(α, σ , v) ≡pp σ .α (v)    Shσ ′, v ′i)
                                                                                     (P ∈ ea(α, σ , v) ≡pp σ .α (v)    FhPi)
We write σ .α (v)     Shσ ′, v ′i to mean that α terminates successfully when executed on σ , gener-
ating the state σ and the value v ′ , and σ .α (v)
                  ′                                  FhPi to mean that the state model was not able
to execute the action α due to not having the required resource. The assertion P, which we refer
to as the action ﬁx, describes a possible way of completing the original state so that the action can
be performed successfully. Unsurprisingly, ﬁxes are assumed to work6 ; meaning that, if we extend
the original state with the generated ﬁx, it must be possible to execute the action successfully. This
constraint is formally described by the equation below:

                   σ .α (v)       FhPi ∧ σ .set(P)             σ ′′ =⇒ ∃ σ ′, v ′ .σ ′′ .α (v)             Shσ ′, v ′i         (5)

6 This is for the user of Gillian to prove.
20                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   We note that, since we model ﬁxes using assertions, the underlying parameter state model must
have support for predicates. Additionally, only the ﬁxes that talk about logical variables that existed
in the initial state are admissible.
Bi-Abductive Analysis. In order to deﬁne the bi-abductive analysis, we instrument the parameter
state model so that every time an action generates a ﬁxable error, the corresponding ﬁx is applied
and the execution continues. The bi-abductive execution also keeps track of all the applied ﬁxes to
allow for the generation of procedure speciﬁcations from from bi-abductive execution traces.
   Given a state model with support for predicates S = h|S |, V , Ai, we construct a new state model
with support for automatic error ﬁxing by coupling |S | with an assertion P ∈ A ∆ , representing the
ﬁxes that were generated so far. Every time an action generates an error, we extend the current state
σ ∈ |S | with the footprint of the corresponding ﬁx and continue with the execution. The lifting is
formally described below. We write ⌈v⌉ to denote the upcast of a value to a boolean expression.
  Deﬁnition 5.1 (BiState Constructor (BiST )). The bi-abductive state constructor BiST : S → S is
deﬁned as BiST (h|S |, V , Ai) , h|S ′ |, V , Ai, where:
      • |S ′ |                     ,    |S | × A ∆
      • setVarbi (hσ, Pi, x, v)    ,    hsetVar(σ, x, v), Pi
      • setStorebi (hσ, Pi, ρ)     ,    hsetStore(σ, ρ), Pi
      • storebi (hσ, −, −i)        ,    store(σ )
      • eebi (hσ, −, −i, e)        ,    ee(σ, e)
      • eabi (α, hσ, Pi, v)        ,    {(hσ ′, Pi, v ′ ) | σ .α (v)    Shσ ′, v ′i} if α , assume
      • eabi (assume, hσ, Pi, v)   ,    {(hσ  ′              ′
                                                , P ∗ π i, v ) | ⌈v⌉ = π ∧ σ .assume (v)         Shσ ′ ,v ′ i}
                                                                                                                                  
                                            hσ ′′ , P ∗ Qi, v ′)
      • eabi (α, hσ, Pi, v)        ,
                                                    | σ .α (v)    FhQi ∧ σ .setQ ([ ])      σ ′ ∧ σ ′ .α (v)      Shσ ′′ ,v ′ i

  Finally, Theorem 5.2 connects successful bi-abductive executions to successful parameter-state
executions. Given a bi-abductive execution p ⊢ hhσ , [ ]i, cs, ii ∗BiST(S ) hhσ , Pi, cs ′, jio , we construct
a parameter-state execution by extending its initial state σ with the missing resource computed
during the bi-abductive execution, described by P.
     Theorem 5.2 (Bi-abduction).
 p ⊢ hhσ , empi, cs, ii       ∗        hhσ ′, Pi, cs ′, jio ∧ σ .set(P)       σ ′′ =⇒ p ⊢ hσ ′′, cs, ii          ∗ hσ ′ , cs ′ , ji o
                              BiST(S )                                                                           S

Implementation. The bi-abductive state constructor is imple- module BiState
                                                                    (St : State)
mented as an OCaml functor parametric on an OCaml module            (CP : CorePred with type a = St.a) :
of type State together with a module of type CorePred. The            (State with type a = St.a) = struct
                                                                        type vt = St.vt
BiState functor precisely follows the lifting described in Deﬁ-         type t = St.t * CP.t Asrt.t
nition 5.1. It is straightforward to check that the carrier type of     type a = St.a
the bi-abductive state, t, matches the carrier sets of the lifted end ...
state, |S | × A ∆ . The CorePred module is required for extending
the parameter state with the footprint of the generated ﬁxes during the bi-abductive analysis.

5.2 While: Bi-abductive Analysis
Let us recall the actions of the While: AW = {lookup, mutate, dispose, setCell, getCell}. Out of those,
the two that may fail and can be ﬁxed are lookup and getCell; mutate will always succeed, setCell
may fail because the resource to be set could still be in the heap, but this cannot be corrected; and
dispose may fail because the object might not be in the heap, but this also cannot be corrected. For
lookup and getCell, the only cause of error is the absence of the looked-up property in the heap,
Gillian: Compositional Symbolic Execution for All                                                      21

and the ﬁx is, simply, to add it. We give the ﬁx for lookup; the ﬁx for getCell is similar.
             S-Lookup - Missing Prop
             µ̂ ↾ê, π = (µ̂ ′, −)     µ̂ ′ = ⊎ni=0 (−.pi 7→ −)       π ⊢ p < {pi |in=0 }   x̂ fresh
                                     µ̂.lookup ([ê, p] , π )   Fhcellh[ê, p, x̂]ii

  The following lemma is easily shown to hold by case analysis on the ﬁxes.
  Lemma 5.3 (While: Correctness of Fixes). The ﬁxes of While satisfy Equation (5).

6 GILLIAN IN THE REAL WORLD: JAVASCRIPT AND C
We instantiate the Gillian framework to obtain analysis tools for JavaScript and C, two real-world,
widely-used programming languages. For each language, we present the concrete and symbolic
memory models along with one of their actions, and discuss the challenges encountered in the
process. We highlight the trustworthiness of the obtained analyses: we compile JavaScript to GIL
by linking to JS-2-JSIL [Santos et al. 2018b], a thoroughly tested compiler for JavaScript; and we
compile C to GIL by linking to CompCert [Leroy 2009a,b], the ﬁrst veriﬁed C compiler. We evaluate
the obtained tools by successfully performing whole-program symbolic testing, full veriﬁcation, and
automatic compositional testing on a series of data-structure libraries, including binary search trees,
key-value maps, priority queues, and singly-and doubly-linked lists, purposefully written using the
programming idioms speciﬁc to the two languages. This demonstrates that Gillian can be used to
quickly obtain analysis tools suﬃciently robust to reason about complex real-world languages.

6.1   Gillian-JS: Trustworthy Analysis of ES5 Strict Programs
The JavaScript Memory Model. We inherit the concrete and symbolic memory models of JavaScript
from Santos et al. [2019], adapting them slightly to the setting of Gillian.
   Concrete JavaScript memories, µ ∈ M JS , consist of a concrete heap and a concrete domain table.
The concrete heap, h : Symb × S ⇀ V, maps object locations (modelled as symbols) and property
names (modelled as strings) to GIL values. This is similar to the While semantics except that, in
the values, we designate a distinguished symbol  (read: none) to denote property absence: that is,
if h(l, p) = , then the object at l does not have property p. This ability to explicitly address the
absence of properties is required because JavaScript has extensible objects. The concrete domain
table, d : Symb ⇀ ℘(S), maps objects to the sets of properties that they may have: that is, if p < d(l),
then the object located at l is guaranteed not to have property p. This, together with the use of ,
ensures that we have a semantics of JavaScript that respects the frame property [Reynolds 2002].
   Symbolic JavaScript memories, µ̂ ∈ M̂ JS , consist of a symbolic heap and a symbolic domain table.
The symbolic heap, ĥ : Ê × Ê ⇀ Ê, maps pairs of logical expressions (property names are also
modelled as logical expressions, as JavaScript has dynamic property access) to logical expressions.
The signature of the symbolic domain table, analogously, is: dˆ : Ê ⇀ Ê.
   We note that heaps and domain tables are connected both in the concrete and in the symbolic
semantics via the heap-domain invariant: for a given location, if its domain is deﬁned, then all of
the properties of that object that are in the heap must also be in its domain.
   Below, we present a rule for one of the actions of the memory model, getProp, which is meant to
receive an object location and a property and retrieve the value of the property. This rule illustrates
a branching action, which passes the constraint êp = êi back into the state after understanding that
we have full knowledge about the object in question (meaning that the properties of the object in
the heap, collected by ĥ ↾êl , coincide with its domain) and that the looked-up property êp may be
equal to one of its properties.
22                    José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner


                     SGetProp - Branch - Found                            
                                ˆ
                      µ̂ = (ĥ, d)   π ⊢ êl = êl′ ∧ dˆ(êl′ ) = ĥ ↾ê ′   π ∧ (êp = êi ) SAT ĥ = _ ⊎ (êl′ .êi 7→ ê)
                                                                        l
                                                                        
                                              µ̂ .getProp ( êl , êp , π )     ( µ̂, ê, êp = êi )

Implementation. We take the implementations of the concrete and symbolic memory models of
JavaScript (ES5 Strict) from JaVerT 2.0 and plug them directly into Gillian, with minor modiﬁcations
in the symbolic memory model related to diﬀerences in design in the ﬁxes of the bi-abduction. Addi-
tionally, we compile the runtime environment of JaVerT 2.0, which consists of JSIL implementations
of the internal and built-in functions of ES5 Strict, to GIL using a JSIL-to-GIL compiler.
Trustworthiness. As JS-2-JSIL is a well-tested, trusted compiler from ES5 Strict to JSIL, the trust-
worthiness of the analysis of Gillian-JS rests on the correctness of JSIL-to-GIL. However, JSIL-to-GIL
is very simple, as the two languages have similar constructs, with the only noteworthy diﬀerence
being that JSIL has commands that directly work with objects, whereas GIL has the actions. To gain
conﬁdence in the correctness of JSIL-to-GIL, we have replayed and passed the 8797 concrete tests
of the Test262 oﬃcial JavaScript test suite [ECMA TC39 2017] also passed by JS-2-JSIL.

6.2    Gillian-C: Towards Certified Verification of C Programs
The C Memory Model. We inherit the concrete memory model of C from CompCert [Leroy et al.
2012], with minor adaptations related to encoding C values in GIL. We deﬁne a symbolic memory
model, deriving it from the concrete model and using ideas from CompCertS [Besson et al. 2017], a
memory model for CompCert that uses symbolic values to improve precision. For clarity, we elide
the details from the CompCert memory model related to concurrency.
   Concrete C memories, µ ∈ M C , consist of a concrete heap and a concrete permission table. The
concrete heap, h : Symb × Z ⇀ V, maps memory locations (modelled as symbols) and oﬀsets
(modelled as integers) to concrete C memory values. A C memory value, mv ∈ V, is either a byte
(integer in the range [0, 255]) or a three-element GIL list [l, oﬀ , k], denoting the k th byte of the
pointer to location l with oﬀset oﬀ . The concrete permission table, d : Symb × Z ⇀ Z, maps
memory locations and oﬀsets to their permissions, which indicate the allowed operations on the
associated cell. We model permissions as integers from 1 to 4, representing, respectively, Nonempty,
Readable, Writable, and Freeable, where Nonempty indicates that the cell only admits pointer
comparison.
   Symbolic C memories, µ̂ ∈ M  bC , consist of a symbolic heap and a symbolic permission table, which
have the same meaning as in concrete memories. Symbolic heaps, ĥ : (Ê × Ê) ⇀ Ê, model locations
and oﬀsets using logical expressions, similarly to While and JavaScript. Symbolic memory values,
mvˆ ∈ Ê, are three-element lists, [ê, k, n], denoting the k th out of n bytes of the C value represented
by ê. Luckily, we always statically know the size of a value, meaning that k and n will always be
concrete. The signature of symbolic permission tables, expectedly, is pbt : Ê × Ê ⇀ Ê.
   In Figure 12, we present one symbolic rule SLoad - Valid Access
for the load action, which retrieves a value                           µ̂ = (ĥ, pbt) π ⊢ êl = êl′ ∧ êo = êo′
from the memory. Note that, when loading or                                   π ⊢ êo′ mod alignment = 0
                                                                     (π ⊢ pt( b êl′ , êo + i) ≥ Readable) |i=0size−1
storing a value, a memory chunk has to be pro-                              ′                  ′                size−1
                                                                      (ĥ(êl , êo + i) = [ê , i, size − 1]) |i=0
vided to indicate the size, alignment, and type                                ê = decodeSymb(ê ′, type)
of what should be read in the memory. For clar-
                                                         µ̂ .load ([[size, alignment, type], êl , êo ] , π )       ( µ̂, ê, true)
ity, we present chunks as three-element lists,
mch = [size, alignment, type]. The load func-                  Fig. 12. Symbolic load Action of C (excerpt)
tion receives a memory chunk, the location, and the oﬀset. First, it ensures that the value is cor-
rectly aligned and that it is allowed to be read. Next, it conﬁrms that the read part of the memory
Gillian: Compositional Symbolic Execution for All                                                    23

represents the symbolic value ê ′ . Finally, it decodes ê ′ using its type. The decoding, for example,
understands if the result should be an integer or a ﬂoating-point, and of which precision.
Implementation. We import the concrete memory model of CompCert into Gillian by directly
plugging in the appropriate OCaml module, extracted from the Coq development; the symbolic
memory model we implement ourselves. We also implement directly in GIL the functions describing
various internals of C, such as, for example, unary and binary operators, malloc and free. We note
that, currently, Gillian-C assumes that, whenever memory is dynamically allocated, the size of the
allocated chunk is known. This allows us to focus on making the analyses work and leave the
complex layer of reasoning about maps with unknown domains for immediate future work.
Trustworthiness. We compile C to GIL via C#m (read: C-sharp-minor), one of the intermediate
representations of CompCert. Therefore, similarly to Gillian-JS, the correctness of compilation for
Gillian-C rests on the correctness of C-to-C#m and our C#m-to-GIL compiler. However, we have a
stronger correctness guarantee for C-to-C#m than for JS-2-JSIL, as this compilation step has been
already veriﬁed in Coq as part of CompCert. Moreover, as C#m and Gillian-C share the same mem-
ory model by design, we could formalise GIL in Coq and re-use the proof techniques of CompCert
to obtain a fully certiﬁed C-to-GIL compiler.

6.3 Evaluation: Data-Structure Libraries
We evaluate Gillian-JS and Gillian-C on data-structure libraries: binary search trees, key-value maps,
priority queues, singly-and doubly-linked lists, and sorted lists. To demonstrate that Gillian can
handle the complexity of the memory models of JavaScript and C, we write these libraries using
the programming idioms speciﬁc to the two languages: for JavaScript, we use prototype inheritance
and function closures; for C, we use pointers and structures.
Whole-Program Symbolic Testing. We Table 1. Whole-program Symbolic Testing:
write symbolic tests with the goal of achiev- Gillian-JS (left); Gillian-C (right)
ing full line coverage for each of the data
structures. The results are given in Table 1 Name #T GIL Time Name #T GIL Time
                                                              cmds                       cmds
and they include, for each data structure: the
number of tests, the number of executed GIL BST         6 137,379 1.36s BST         5 15,256 0.33s
commands, and the obtained times.               KVMap 3 67,216 0.35s KVMap 1 1,165 0.13s
   The results indicate that whole-program PriQ 6 61,338 0.42s PriQ 4 1,008 0.13s
symbolic testing can scale to larger code- SLL          6 28,389 0.21s SLL          3 4,218 0.18s
                                                DLL     6 30,929 0.21s DLL          5 7,000 0.22s
bases. The obtained times for Gillian-
                                                SL      6 37,251 0.42s SL           3 2,688 0.11s
JS are comparable to those of JaVerT
2.0 [Santos et al. 2019], with the number of
commands run being higher, as GIL is more low-level than JSIL. The analysis of Gillian-C demon-
strates the diﬀerence in complexity between the JavaScript and the C semantics: the large number
of executed commands for Gillian-JS stems from the repeated execution of numerous internal func-
tions, of which C has far fewer. It also shows that the core of the obtained time does not lie with
the number of executed commands, but rather with the time spent in the ﬁrst-order solver, as high-
lighted by the BST example, which yields more complex entailments than the other examples.
Veriﬁcation. We specify and verify the data structures. For JS, we manually write the required
predicates, using the speciﬁcation techniques of JaVerT [Santos et al. 2018b]. For C, we use the
type information to automatically generate recursive predicates describing structures in memory,
which we then extend with required information about the values. The results are shown in Table 2.
For each data structure, we give: the number of veriﬁed functions, the total number of speciﬁcations
for those functions, the number of executed GIL commands, and the veriﬁcation time.
24                José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   We can observe that, when com-              Table 2. Verification: Gillian-JS (left); Gillian-C (right)
pared to whole-program symbolic test-
ing, the number of executed com- Name #F #S GIL Time Name #F #S GIL Time
mands is dramatically lower, but the                       cmds                                cmds
obtained times are longer. This is in BST          5 5 9,620 2.26s BST                5 6 3,968 5.57s
line with the facts that whole-program KVMap 4 9 11,284 0.75s KVMap 3 5 733 0.99s
symbolic testing does not use proce- PriQ 6 9 12,823 1.38s PriQ 5 9 1,161 1.08s
dure summaries during execution and SLL            3 3 2,978 0.61s SLL                6 6 1,201 0.17s
that veriﬁcation involves considerable     DLL     3    3   4,220   0.82s    DLL      5 5 2,980 0.39s
predicate manipulation. We also note       SL      2    2   3,152   0.42s    SL       4 4 702 0.82s
that obtained times for Gillian-JS are
marginally slower than those of JaVerT 2.0. This is expected, given the more general nature of
Gillian. The veriﬁcation times for Gillian-C are fast across the board, with the exception of binary
search trees, which, as mentioned earlier, yield complex entailments that Z3 has to solve.
Bi-abduction. We use bi-abduction to au- Table 3. Bi-abduction: Gillian-JS (left); Gillian-C (right)
tomatically create speciﬁcations for the data
structures. We note that these speciﬁcations                    S/E/B                   S/B
                                                       Name            Time     Name          Time
describe the behaviour of the up to a given                     specs                  specs
bound. The results are presented in Table 1.           BST     26/0/5 3.98s     BST     37/8 0.37s
For both languages, we give the number of suc-         KVMap 9/12/12 1.57s      KVMap 9/0 0.13s
cess and bug specs found (S/B), and the time           PriQ 15/1/12 3.23s       PriQ 19/3 0.21s
required to ﬁnd them. For JavaScript, we addi-         SLL      6/0/2 0.78s     SLL     20/3 0.16s
tionally include the number of error specs (as         DLL      9/0/3 1.04s     DLL     37/7 0.24s
JavaScript programs can terminate with a user-         SL       8/0/2 1.09s     SL      12/0 0.15s
thrown error). It is important to clarify that, for
JavaScript, a bug spec means that the program terminated with a native error (e.g. a TypeError or
ReferenceError); for C, a bug spec means that the program has thrown an exception (e.g. a segmen-
tation fault). To obtain bug specs for C, we introduce errors into the code; for JavaScript, the lack of
typing information in the language is suﬃcient on its own. Finally, we note that the obtained spec-
iﬁcations may describe behaviour outside of the use cases of the function and could contain false
positive bug reports that need to be treated afterwards either automatically or by the developer.
   As for veriﬁcation, the obtained times for Gillian-JS are slightly slower than those of JaVerT 2.0
due to Gillian being a general framework. We note that they are still quite long, as we have not
yet solved the bi-abduction issues of JaVerT 2.0 related to the internal branching of the JavaScript
semantics, and view this to be beyond the scope of this paper. The bi-abduction of Gillian-C, on the
other hand, yields promising results, as it is able to detect the introduced bugs in very quick times.

7    RELATED WORK
There is a wide range of works on symbolic analyses for C and JavaScript, such as [Botincan et al.
2009; Jensen et al. 2009; Jourdan et al. 2015; Kashyap et al. 2014; Park and Ryu 2015]. As this pa-
per focusses on the design of Gillian and its associated meta-theory, we centre our discussion on
parametric frameworks for obtaining modular symbolic analyses in general, covering the ﬁelds of
symbolic execution, abstract interpretation, and logic-based analysis and veriﬁcation.
Symbolic Execution. Building and maintaining new symbolic execution engines for real-world
programming languages is known to be a daunting task [Cadar et al. 2011; Cadar and Sen 2013].
Researchers in the ﬁeld have, therefore, tried to automate this process, with tools such as Rosette
Gillian: Compositional Symbolic Execution for All                                                    25

[Torlak and Bodík 2013, 2014] and Chef [Bucur et al. 2014], which propose two diﬀerent mecha-
nisms to automatically lift a user-provided vanilla concrete interpreter for a given target language
to a fully-ﬂedged symbolic execution engine for the same language.
   More concretely, Rosette is an extension of Racket [Racket 2017] which additionally provides
a set of solver-aided facilities for creating symbolic values and expressing constraints on those
values. With Rosette, the concrete interpreter of the target language is written directly in Racket
and is then symbolically interpreted using Rosette’s core symbolic execution engine. In contrast,
Chef takes a specially-packaged interpreter as input and executes the target language programs
symbolically by symbolically executing the interpreter’s binary.
   Importantly, neither Rosette nor Chef can scale to real-world programming languages. Rosette
is aimed at domain-speciﬁc languages with restricted expressive power, while Chef is limited to lan-
guages with “moderately-sized” interpreters. Interestingly, by implementing a JavaScript symbolic
execution engine natively in OCaml [Santos et al. 2019], instead of running a concrete interpreter
on top of Rosette [Santos et al. 2018a], Fragoso Santos et al. gained a performance speed-up of
two orders of magnitude.
Abstract Interpretation. When it comes to general abstract interpreters, we identify two main
strands of work: those based on small-step semantics and those based on big-step semantics.
   Small-Step Abstract Interpreters. Might [Might 2010] proposes a methodology for automatically
deriving a family of sound, computable abstract interpreters from a given concrete interpreter writ-
ten in small-step style. This methodology assumes an initial Galois connection [Cousot and Cousot
1977] between the concrete and abstract domains in order to guarantee the optimality of the de-
rived abstract interpreters. Later, Might and others [Horn and Might 2010, 2012] apply the proposed
methodology to a family of abstract machines, obtaining the so called abstract abstract machines,
which include expressive programming language features, such as: ﬁrst-class control, exception
handling, and state. This technique is further reﬁned in [Sergey et al. 2013], where the authors
show how to derive monadically-parameterised abstract interpreters from concrete interpreters.
The additional level of parameterisation is used to capture in a single uniﬁed formalism a number
of diﬀerent styles of program analyses, making it easy to instrument an analysis with parameteris-
able strategies for improving precision and performance. In [Darais et al. 2015], the authors propose
a library of Galois tranformers to streamline the construction of such strategies. The appeal of this
approach is that each Galois transformer can be proved sound once and for all, making it much
easier to prove the soundness of the obtained analysis.
   We observe that, despite oﬀering a general methodology for designing abstract interpreters, none
of the works mentioned above automates that methodology, in that one always has to manually
follow it to obtain an abstract interpreter for a given language. We further note that none of these
techniques has been applied to real world programming languages, such as JavaScript and C.
   Big-Step Abstract Interpreters. In [Schmidt 1995], Schmidt presents a general approach for de-
signing abstract interpreters based on co-inductively deﬁned big-step semantics. Following similar
ideas, Bodin et al. [2019] establish a general framework, the skeletal semantics, for developing con-
crete and abstract big-step semantics, connected with a general consistency result, leaving the user
to prove a number of simple language-dependent lemmas. This work, however, has only been ap-
plied to a simple While language with no heap, making its broader applicability diﬃcult to assess.
Logic-based Analysis and Veriﬁcation. K [G. Roşu and T. Florin Şerbănuţă 2010] is a language-
independent veriﬁcation infrastructure instantiated to several real-world languages, such as Java,
JavaScript, and C [Bogdanas and Rosu 2015; Hathhorn et al. 2015; Park et al. 2015; Stefanescu et al.
2016], and evaluated on data-structure libraries similar to those of Gillian. As in Gillian, the user of
K gets the veriﬁcation guarantee for free, by construction. Gillian, however, has several advantages
26               José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

over K: Gillian speciﬁcations are language-tailored; it supports compositional analyses; and it is
faster. For example, the functions of the BST example are veriﬁed in K for C in 88.5 seconds and for
JavaScript in 25.5 seconds; we verify the same functions in approx. 8 seconds for both languages.
   CoreStar [Botinčan et al. 2011], was envisioned as a general back-end for tools based on sepa-
ration logic, where the user would encode the assertions of their language as abstract predicates
and provide CoreStar with a separation algebra describing the entailments speciﬁc to those predi-
cates. However, CoreStar does not appear to be ﬁt for reasoning about highly complex real-world
dynamic languages, such as JavaScript. For instance, in JaVerT [Santos et al. 2018b], the authors
obtained prohibitive performance even for simple examples.
   Viper [Müller et al. 2016, 2017] is also a veriﬁcation framework designed to serve as a back-end
for tools for permission-based veriﬁcation, such as separation-logic-based tools. However, Silver,
the intermediate language of Viper, is not parameterisable. Hence, in order to use Viper, users have
to encode their memory models in the memory model of Silver. We believe that this approach does
not scale well when there is a big mismatch between the memory model to encode and that of the
host language, in this case, Silver.
   Iris [Jung et al. 2018, 2015] is a Coq-based framework for reasoning about the safety of concur-
rent programs. It provides a general methodology for designing new sound concurrent program
logics, as users can encode their own program logics into Iris and leverage Iris’s soundness result
to prove the soundness of their logics. Iris is, however, mainly aimed at the mechanisation of meta-
theory, while the main goal of Gillian is to streamline the development of analysis tools.
   JaVerT 2.0 [Santos et al. 2019] is a tool for compositional analysis of JavaScript programs, Sim-
ilarly to Gillian, it supports whole-program symbolic testing, full veriﬁcation, and bi-abduction.
While the analysis of JaVerT 2.0 is structured modularly, all of its meta-theoretical results, as well
as its implementation, are speciﬁc to its intermediate language and rely on the speciﬁc concrete and
symbolic memory models of JavaScript. Gillian takes the highly non-trivial step of generalising both
the theory and the implementation of JaVerT 2.0 to a fully language-independent setting.

8    CONCLUSIONS AND FURTHER WORK
We have presented Gillian, a language-independent framework for the development of composi-
tional symbolic analysis tools, and demonstrated that it can be used to reason about real-world pro-
gramming languages. Thanks to its parametric meta-theory and modular implementation, Gillian
can readily be used by developers to create analysis tools for their language of choice, be it toy,
domain-speciﬁc, or real-world. We believe that Gillian will be of interest to a broad range of users
wishing to obtain correctness guarantees for their code.
   The avenues for further work on Gillian are numerous. First of all, our immediate next steps are
to streamline the bi-abduction of Gillian-JS and extend the reasoning about the symbolic memory
model of Gillian-C to include arbitrary dynamic memory allocation, taking inspiration for the latter
from the work of [Kirchner et al. 2015] done for Frama-C.
   We are also investigating ways of extending Gillian with support for reasoning about complex
language features, such as events and concurrency, as well as with additional forms of analysis,
such as concolic execution. The modular design of Gillian lends itself well to these purposes.
   Moreover, the infrastructure of Gillian can be extended to support the analysis of systems running
code written in multiple programming languages that inter-operate with each other. A noteworthy
goal in this vein of research would be a joint analysis of JavaScript and WebAssembly [Haas et al.
2017], the emerging low-level language for the Web.
   Finally, we plan to improve Gillian’s error reporting mechanisms and develop interactive tools,
such as a trace visualiser and a code-stepper, for the debugging of programs analysed by Gillian, in
order to make Gillian more accessible to a wider audience of interested users.
Gillian: Compositional Symbolic Execution for All                                                                         27

REFERENCES
R. Baldoni, E. Coppa, D. Cono D’Elia, C. Demetrescu, and I. Finocchi. 2018. A Survey of Symbolic Execution Techniques.
    ACM Computing Surveys 51, 3 (2018), 50:1–50:39.
A. Banerjee and D. A. Naumann. 2002. Secure Information Flow and Pointer Conﬁnement in a Java-like Language. In CSFW.
J. Berdine, C. Calcagno, and P. W. O’Hearn. 2005. Symbolic Execution with Separation Logic. In APLAS. 52–68.
Frédéric Besson, Sandrine Blazy, and Pierre Wilke. 2017. CompCertS: A Memory-Aware Veriﬁed C Compiler Using Pointer
    as Integer Semantics. In ITP.
M. Bodin, P. Gardner, T. Jensen, and A. Schmitt. 2019. Skeletal Semantics and their Interpretations. PACMPL 3, POPL (2019).
D. Bogdanas and G. Rosu. 2015. K-Java: A Complete Semantics of Java. In POPL. 445–456.
M. Botincan, M. J. Parkinson, and W. Schulte. 2009. Separation Logic Veriﬁcation of C Programs with an SMT Solver. Electr.
    Notes Theor. Comput. Sci. 254 (2009), 5–23.
M. Botinčan, D. Distefano, M. Dodds, R. Grigore, D. Naudžiūnienė, and M. J. Parkinson. 2011. coreStar: The Core of jStar. In
    Boogie.
S. Bucur, J. Kinder, and G. Candea. 2014. Prototyping Symbolic Execution Engines for Interpreted Languages. In ASPLOS.
C. Cadar, P. Godefroid, S. Khurshid, C. S. Păsăreanu, K. Sen, N. Tillmann, and W. Visser. 2011. Symbolic Execution for
    Software Testing in Practice: Preliminary Assessment. In ICSE. 1066–1071.
C. Cadar and K. Sen. 2013. Symbolic Execution for Software Testing: Three Decades Later. Commun. ACM 56 (2013), 82–90.
C. Calcagno, D. Distefano, J. Dubreil, D. Gabi, P. Hooimeijer, M. Luca, P. W. O’Hearn, I. Papakonstantinou, J. Purbrick, and
    D. Rodriguez. 2015. Moving Fast with Software Veriﬁcation. In NASA Formal Methods Symposium. 3–11.
C. Calcagno, P. W. O’Hearn, and H. Yang. 2007. Local Action and Abstract Separation Logic. In LICS.
Patrick Cousot and Radhia Cousot. 1977. Abstract Interpretation: A Uniﬁed Lattice Model for Static Analysis of Programs
    by Construction or Approximation of Fixpoints. In POPL. ACM Press, 238–252.
P. Cousot and R. Cousot. 2004. Basic Concepts of Abstract Interpretation. In IFIP.
Ron Cytron, Jeanne Ferrante, Barry K. Rosen, Mark N. Wegman, and F. Kenneth Zadeck. 1989. An Eﬃcient Method of
    Computing Static Single Assignment Form. In Conference Record of the Sixteenth Annual ACM Symposium on Principles
    of Programming Languages, Austin, Texas, USA, January 11-13, 1989. 25–35.
David Darais, Matthew Might, and David Van Horn. 2015. Galois transformers and modular abstract interpreters: reusable
    metatheory for program analysis. In OOPSLA.
Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Eﬃcient SMT Solver. In TACAS.
ECMA TC39. 2017. Test262 Test Suite. https://github.com/tc39/test262.
G. Roşu and T. Florin Şerbănuţă . 2010. An Overview of the K Semantic Framework. Journal of Logic and Algebraic Program-
    ming 79, 6 (2010), 397–434.
A. Haas, A. Rossberg, D. L. Schuﬀ, B. L. Titzer, M. Holman, D. Gohman, L. Wagner, A. Zakai, and JF Bastien. 2017. Bringing
    the Web Up to Speed with WebAssembly. In PLDI (PLDI 2017).
C. Hathhorn, C. Ellison, and G. Rosu. 2015. Deﬁning the undeﬁnedness of C. In PLDI.
D. Van Horn and M. Might. 2010. Abstracting Abstract Machines. In ICFP.
D. Van Horn and Matthew Might. 2012. Systematic Abstraction of Abstract Machines. J. Funct. Program. 22, 4-5 (2012),
    705–746.
S. H. Jensen, A. Møller, and P. Thiemann. 2009. Type Analysis for JavaScript. In SAS (Lecture Notes in Computer Science),
    Vol. 5673. Springer, 238–255.
R. Jhala and K. L. McMillan. 2006. A Practical and Complete Approach to Predicate Reﬁnement. In TACAS.
J-H. Jourdan, V. Laporte, S. Blazy, X. Leroy, and D. Pichardie. 2015. A Formally-Veriﬁed C Static Analyzer. In POPL.
R. Jung, R. Krebbers, J. Jourdan, A. Bizjak, L. Birkedal, and D. Dreyer. 2018. Iris from the ground up: A modular foundation
    for higher-order concurrent separation logic. J. Funct. Program. 28 (2018).
R. Jung, D. Swasey, F. Sieczkowski, K. Svendsen, A. Turon, L. Birkedal, and D. Dreyer. 2015. Iris: Monoids and Invariants as
    an Orthogonal Basis for Concurrent Reasoning. In POPL.
Vineeth Kashyap, Kyle Dewey, Ethan A Kuefner, John Wagner, Kevin Gibbons, John Sarracino, Ben Wiedermann, and Ben
    Hardekopf. 2014. JSAI: a static analysis platform for JavaScript. In FSE. ACM.
F. Kirchner, N. Kosmatov, V. Prevosto, J. Signoles, and B. Yakobowski. 2015. Frama-C: A software analysis perspective. Formal
    Aspects of Computing 27, 3 (2015), 573–609.
X. Leroy. 2009a. Formal veriﬁcation of a realistic compiler. Commun. ACM 52, 7 (2009), 107–115.
X. Leroy. 2009b. A formally veriﬁed compiler back-end. Journal of Automated Reasoning 43, 4 (2009), 363–446.
X. Leroy, A. W. Appel, S. Blazy, and G. Stewart. 2012. The CompCert Memory Model, Version 2. Research Report RR-7987.
    INRIA. 26 pages.
M. Might. 2010. Abstract Interpreters for Free. In SAS.
P. Müller, M. Schwerhoﬀ, and A. J. Summers. 2016. Viper: A Veriﬁcation Infrastructure for Permission-Based Reasoning. In
    VMCAI.
28                   José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

P. Müller, M. Schwerhoﬀ, and A. J. Summers. 2017. Viper: A Veriﬁcation Infrastructure for Permission-Based Reasoning. In
    Dependable Software Systems Engineering.
P. W. O’Hearn. 2018. Continuous Reasoning: Scaling the Impact of Formal Methods. In LICS. 13–25.
Changhee Park and S. Ryu. 2015. Scalable and Precise Static Analysis of JavaScript Applications via Loop-Sensitivity. In
    ECOOP. 735.
D. Park, A. Stefanescu, and G. Rosu. 2015. KJS: a Complete Formal Semantics of JavaScript. In PLDI.
C. S. Pasareanu, R. Pelánek, and W. Visser. 2007. Predicate Abstraction with Under-Approximation Reﬁnement. Logical
    Methods in Computer Science 3, 1 (2007).
Racket. 2017. The Racket Programming Language. racket-lang.org.
Mohammad Raza and Philippa Gardner. 2009. Footprints in Local Reasoning. Logical Methods in Computer Science 5, 2
    (2009).
J. C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable Data Structures. In LICS. 55–74.
J. Fragoso Santos, P. Maksimovic, T. Grohens, J. Dolby, and P. Gardner. 2018a. Symbolic Execution for JavaScript. In PPDP.
    11:1–11:14.
J. Fragoso Santos, P. Maksimovic, D. Naudziuniene, T. Wood, and P. Gardner. 2018b. JaVerT: JavaScript Veriﬁcation Toolchain.
    PACMPL 2, POPL (2018), 50:1–50:33.
J. Fragoso Santos, P. Maksimovic, G. Sampaio, and P. Gardner. 2019. JaVerT 2.0: Compositional Symbolic Execution for
    JavaScript. PACMPL 3, POPL (2019), 66:1–66:31.
D. A. Schmidt. 1995. Natural-Semantics-Based Abstract Interpretation (Preliminary Version). In SAS. 1–18.
I. Sergey, D. Devriese, M. Might, J. Midtgaard, D. Darais, D. Clarke, and F. Piessens. 2013. Monadic Abstract Interpreters. In
    PLDI.
A. Stefanescu, D. Park, S. Yuwen, Y. Li, and G. Rosu. 2016. Semantics-based Program Veriﬁers for All Languages. In OOPSLA.
E. Torlak and R. Bodík. 2013. Growing Solver-aided Languages with Rosette. In Onward!
E. Torlak and R. Bodík. 2014. A Lightweight Symbolic Virtual Machine for Solver-Aided Host Languages. In PLDI.
Gillian: Compositional Symbolic Execution for All                                                                                                           29

A      SECTION 2: PARAMETRIC EXECUTION
The Syntax of GIL
 v ∈ V , n ∈ N | i ∈ Z | s ∈ S | b ∈ B | ς ∈ Symb | τ ∈ T | f ∈ F | v                                           e ∈ E , v | x ∈ X | ⊖e | e 1 ⊕ e 2
 c ∈ CA      , x := e | ifgoto e i | x := e(e ′) | x := α(e) |                                                  proc ∈ Proc A , proc f (x){c}
                x := symbj | x := freshj | return e | fail e | vanish                                           p ∈ ProдA : F ⇀ Proc A

   Deﬁnition A.1 (State Model). A state model S ∈ S is a triple h|S |, V , Ai, consisting of: (1) a set of
states on which GIL programs operate, |S |, (2) a set of values stored in those states, V , and (3) a set
of actions that can be performed on those states, A. A state model deﬁnes the following functions
for acting on states (≡pp denotes pretty-printing for readability):
    • setVar : |S | → X → V → |S |                                    (setVar(σ , x, v) ≡pp σ .setVar(x, v))
    • setStore : |S | → (X ⇀ V ) → |S |                                 (setStore(σ , ρ) ≡pp σ .setStore(ρ))
    • store : |S | → (X ⇀ V )                                                        (store(σ ) ≡pp σ .store)
    • ee : |S | → E ⇀ V                                                               (ee(σ , e) ≡pp σ .ee(e))
    • ea : A → |S | → V ⇀ ℘(|S | × V )                   ((σ ′, v ′) ∈ ea(α, σ , v) ≡pp σ .α (v)     (σ ′, v ′))
A state model S = h|S |, V , Ai is said to be proper iﬀ it deﬁnes the following three distinguished
actions: assume, symb, and fresh.
GIL Semantic Domains for S = h|S |,V , Ai
 Call stacks:                   cs ∈ Cs S , | f | | | f , x, ρ, i | : cs          where: f ∈ F , x ∈ X, ρ : X ⇀ V , i ∈ Z
 Conﬁgurations:              cf ∈ Con f S , hp, σ, cs, ii                         where: p ∈ ProдA , σ ∈ |S |, cs ∈ Cs S , i ∈ Z
 Outcomes:                         o ∈ O , · | N(v) | E(v)                        where: v ∈ V

GIL semantic transitions:      S :               |S | × Cs S × N × O ⇀ ℘(|S | × Cs S × N × O).
                                                                       ′
Semantics of GIL: p ⊢ hσ, cs, iio                   hσ ′ , cs ′, jio
      Assignment                                                           Action
        cmd(p, cs, i) = x := e          σ .ee (e) = v                      cmd(p, cs, i) = x := α (e)       σ .ee (e) = v       σ .α (v)      (σ ′, v ′ )
                                                                                                                ′               ′
      p ⊢ hσ, cs, i i        hσ .setVar(x, v), cs, i+1i                             p ⊢ hσ, cs, i i        hσ .setVar(x, v ), cs, i+1i

 IfGoto - True                                IfGoto - False
     cmd(p, cs, i) = ifgoto e j                   cmd(p, cs, i) = ifgoto e j                     Symb
           σ .ee (e) = v                               σ .ee (¬e) = v                                           cmd(p, cs, i) = x := symbj
       σ .assume (v)      σ′                        σ .assume (v)      σ′                                         σ .fresh (j)    (σ ′, v ′ )
    p ⊢ hσ, cs, i i     hσ ′, cs, j i         p ⊢ hσ, cs, i i          hσ ′, cs, i + 1i             p ⊢ hσ, cs, i i       hσ ′ .setVar(x, v ′ ), cs, i+1i
                                                                                  Call
          Fresh                                                                                    cmd(p, cs, i) = e(e ′ )
                      cmd(p, cs, i) = x := fresh j                                           σ .ee (e) = f       σ .ee (e ′ ) = v
                       σ .symb (j)     (σ ′, v ′ )                                           cs′ = |f , x, σ .store, i + 1 | : cs
           p ⊢ hσ, cs, i i       hσ ′ .setVar(x, v ′ ), cs, i+1i                  p ⊢ hσ, cs, i i        hσ .setStore([f .arg 7→ v]), cs′, 0i

 Return                                                         Top Return                                            Fail
   cmd(p, cs, i) = return e      σ .ee (e) = v                             cmd(p, cs, i) = return e                          cmd(p, cs, i) = fail e
 cs = |−, x, ρ, j | : cs′   σ ′ = σ .setStore(ρ)                               σ .ee (e) = v                                    σ .ee (e) = v
    p ⊢ hσ, cs, i i      hσ ′ .setVar(x, v ′ ), cs′, j i        p ⊢ hσ, |f |, i i         hσ, |f |, i i N(v )         p ⊢ hσ, cs, i i      hσ, cs, i i E(v )


   Deﬁnition A.2 (Allocator Model). An allocator model AL ∈ AL is a pair h|AL|, V i consisting of: (1)
a set |AL| ∋ ξ of allocators; and (2) a set V of values to allocate. It exposes the following function:
                                         alloc : |AL| → N → ℘(V ) ⇀ |AL| × V
30                      José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

which satisﬁes the well-formedness constraint:
                                                  (ξ ′, v) = alloc (ξ , j, Y ) =⇒ v ∈ Y .

       Logical variables : x̂ ∈ X̂.
     Logical expressions : ê ∈ Ê , v | x̂ ∈ X̂ | ⊖ê | ê 1 ⊕ ê 2 .
Additionally, we write π ∈ Π to denote logical expressions that that be statically typed as boolean
(for example, true, false, x̂ and ŷ, etc.).

  Deﬁnition A.3 (Concrete Memory Model). A concrete memory model M ∈ M is a pair h|M |, Ai,
consisting of a set of concrete memories, |M | ∋ µ, and a set of actions A. A concrete memory model
additionally deﬁnes a function ea for acting on memories:
                   ea : A → |M | → V ⇀ |M | × V                                                (ea (α, µ, v) ≡pp µ.α(v))

  Deﬁnition A.4 (Symbolic Memory Model). A symbolic memory model M̂ ∈ M̂ is a pair h|M̂ |, Ai,
consisting of a set of symbolic memories, |M̂ | ∋ µ̂, and a set of actions A. A symbolic memory model
additionally deﬁnes a function eaˆ for acting on memories:

                                         eaˆ : A → |M̂ | → Ê → Π ⇀ ℘(|M̂ | × Ê × Π)
                               ((µ̂ ′, ê ′, π ′ ) ∈ ea
                                                      ˆ (α, µ̂, ê, π ) ≡pp µ̂.α (ê, π ) (µ̂ ′, ê ′, π ′ ))
.
        Concrete stores : ρ : X ⇀ V                                                           Symbolic stores : ρ̂ : X ⇀ Ê
     Concrete allocators : ξ ∈ |AL| V                                                      Symbolic allocators : ξˆ ∈ |AL| Ê
     Mandatory actions : A0 , {assume, fresh, symb}
   Deﬁnition A.5 (Concrete State Constructor (CST )). Given an allocator AL = h|AL|, Vi, the concrete
state constructor CST : M → S is deﬁned as CST (h|M |, Ai) , h|S |, V, A ⊎ A0 i, where:
     • |S | = |M | × (X ⇀ V) × |AL| V
     • setVar(hµ, ρ, ξ i, x, v) , hµ, ρ[x 7→ v], ξ i
     • setStore(hµ, _, ξ i, ρ)  , hµ, ρ, ξ i
     • store(h_, ρ, _i)         , ρ
     • ee(h_, ρ, _i, e)         , neo ρ
     • ea(α, hµ, ρ, ξ i, v)     , {(hµ ′, ρ, ξ i, v ′) | (µ ′,v ′ ) = ea (α, µ, v)}
     • assume(σ,v)              , {(σ,v) | v = true}
     • fresh(hµ, ρ, ξ i, i)     , {(hµ, ρ, ξ ′i, ς) | ξ .alloc (i) → Symb (ξ ′, ς)}
     • symb(hµ, ρ, ξ i, i)              ,       {(hµ̂, ρ̂, ξ ′i, v) | ξ .alloc (i) → V (ξ ′,v)}

                                                                          ˆ = h|AL|,
   Deﬁnition A.6 (Symbolic State Constructor (SST )). Given an allocator AL       ˆ Êi, the symbolic
                                                                 ˆ Ê, A ⊎ A0 i, where:
state constructor SST : M̂ → S is deﬁned as SST (h|M̂ |, Ai) , hS,
     • Sˆ = | M̂ | × (X ⇀ Ê) × |AL| Ê × Π
     • setVar(hµ̂, ρ̂, ξˆ, π i, x, e)
                                   ˆ        ,     hµ̂, ρ̂[x 7→ e], ˆ ξˆ, π i
     • setStore(hµ̂, _, ξˆ, π i, ρ̂)        ,     hµ̂, ρ̂, ξˆ, π i
     • store(h_, ρ̂, _, _i)                 ,     ρ̂
     • ee(h_, ρ̂, _, _i, e)                 ,     ρ̂(e)
     • ea(α, hµ̂, ρ̂, ξˆ, π i, e)
                               ˆ            ,     {(hµ̂ ′, ρ̂, ξˆ, π ∧ π ′ i, ê ′) | (µ̂ ′ , eˆ′, π ′ ) ∈ ea
                                                                                                            ˆ (α, µ̂, e)}
                                                                                                                      ˆ
     • assume(hµ̂, ρ̂, ξˆ, π i, π ′ )       ,     {(hµ̂, ρ̂, ξˆ, π ∧ π ′ i, true) | π ∧ π ′ not UNSAT}
     • fresh(hµ̂, ρ̂, ξˆ, π i, i)           ,     {(hµ, ρ, ξˆ′, π i, ς) | ξˆ.alloc (i) → Symb (ξˆ′, ς)}
     • symb(hµ̂, ρ̂, ξˆ, π i, i)            ,     {(hµ, ρ, ξˆ′, π i, x̂) | ξˆ.alloc (i) → X̂ (ξˆ′, x̂)}
Gillian: Compositional Symbolic Execution for All                                                                                                  31

A.1     While: Syntax, Actions, Compilation to GIL, Concrete/Symbolic memories
While: Syntax, Actions, Memories
 ws ∈ Stmt W , x := e | skip | ws1 ; ws2 | if(e){ws1 }else {ws2 } | while (e){ws} | return e | x := f (e) |
                 assume e | assert e | x := pi : ei |in=1 | x := e.p | e.p := e ′ | dispose e
          AW , {lookup, mutate, dispose}
     µ ∈ M W : Symb × S ⇀ V
     µ̂ ∈ M̂ W : Ê × S ⇀ Ê
                                           
While-to-GIL Compiler: CW : Stmt W → Z → CAW × Z
 Assignment                      Skip                                               Return                               Call
  CW (x := e, pc) ,                  CW (skip , pc) ,                                CW (return e, pc) ,                   CW (x := f (e), pc) ,
   pc : x := e                        pc : ifgoto true (pc + 1)                       pc : return e                         pc : x := f e
   · ← pc + 1                         · ← pc + 1                                      · ← pc + 1                            · ← pc + 1

   Seqence                                        If
      CW (ws1, pc) = (c 1, pc1 )                         CW (ws1, pc + 1) = (c 1, pc1 )                While
      CW (ws2, pc1 ) = (c 2, pc2 )                       CW (ws2, pc1 + 1) = (c 2, pc2 )                      CW (ws, pc + 1) = (c, pc′ )
        CW (ws1 ; ws2, pc) ,                           CW (if (e){ws1 }else {ws2 }, pc) ,                 CW (while (e){ws }, pc) ,
         c1                                             pc : ifgoto (not e) (pc1 + 1)                      pc : ifgoto (not e) (pc′ + 1)
         c2                                             c1                                                 c
         · ← pc2 + 1                                    pc1 : ifgoto true pc2                              pc′ : ifgoto true pc
                                                        c2                                                 · ← pc′ + 1
                                                        · ← pc2

   Assume                                          Assert                                    New                  n
       CW (assume e, pc) ,                              CW (assert e, pc) ,                     CW (x := p i : ei |i=1 , pc) ,
        pc : ifgoto e (pc + 2)                           pc : ifgoto e (pc + 2)                  pc : x := symb
                                                                                                                                       n
        pc + 1 : vanish                                  pc + 1 : fail e                         pc + i : _ := mutate([x, p i , ei ]) |i=1
        · ← pc + 2                                       · ← pc + 2                              · ← pc + n + 1

        Lookup                                              Mutate                                             Dispose
          CW (x := e .p, pc) ,                                CW (e1 .p := e2, pc) ,                              CW (dispose e, pc) ,
           pc : x := lookup(x, p)                              pc : _ := mutate([e1, p, e2 ])                      pc : _ := dispose(e)
           · ← pc + 1                                          · ← pc + 1                                          · ← pc + 1

While: Actions in Concrete and Symbolic Memories

            C-Lookup                                                              S-Lookup
                µ = _ ⊎ l .p 7→ v                                                   π ⊢ eˆ = eˆ′        µ̂ = _ ⊎ eˆ′ .p 7→ eˆv
            µ.lookup ([l,p])             (µ, v)                                               ˆ p] , π )
                                                                                  µ̂.lookup ([e,                  {(µ̂, eˆv , true)}

  C-Mutate-Present                                                   S-Mutate-Present
  µ = µ ′ ⊎ l .p 7→ _ µ ′′ = µ ′ ⊎ l .p 7→ v                         π ⊢ eˆ = eˆ′′ µ̂ = µ̂ ′ ⊎ ê ′′ .p 7→ _ µ̂ ′′ = µ̂ ′ ⊎ eˆ′′ .p 7→ ê ′
                                                                                                  
         µ.mutate ([l,p,v])              (µ ′′ ,v)                          µ̂.mutate ( ê, p, ê ′ , π )   {(µ̂ ′′, true, true)}

   C-Mutate-Absent                                                           S-Mutate-Absent
   (l,p) < dom(µ)  µ ′ = µ ⊎ l .p 7→ v                                            µ̂ ↾ê,p, π = ∅ µ̂ ′ = µ̂ ⊎ ê.p 7→ eˆ′
                                                                                                  
          µ.mutate ([l, p,v])             (µ ′,v)                            µ̂.mutate ( ê, p, eˆ′ , π )   {(µ̂ ′, true, true)}

           C-Dispose                                                              S-Dispose
                 µ ↾l = (_, µ ′ )                                                               µ̂ ↾ê, π = (_, µ̂ ′ )
                                     ′
            µ.dispose (l)       (µ , true)                                                     ˆ π)
                                                                                   µ̂.dispose (e,            {(µ̂ ′, true, true)}
32                        José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

B SECTION 3: PARAMETRIC SOUNDNESS
B.1       Parametric Soundness
Restriction Operators. A restriction operator ⇃: X → X ⇀ X on a set X , written x 1 ⇃x 2 for ⇃ (x 1, x 2 ),
is a binary associative function satisfying the following properties:
                                                                                                  Weakening
                Idempotence                       Right Commutativity                                     x 1 ⇃x 2⇃x3 = x
                x ⇃x = x                          (x 1 ⇃x 2 ) ⇃x 3 = (x 1 ⇃x 3 ) ⇃x 2
                                                                                                  x 1 ⇃x 2 = x 1 ∧ x 1 ⇃x 3 = x 1
  A restriction operator on states ⇃: |S | → |S | ⇀ |S | is said to be preserved by a state model
S = h|S |, V , Ai if all of the state-generating functions exposed by the state model are monotonic
with respect to the pre-order induced by ⇃; put formally:
 RMono-SetVar                                          RMono-SetStore                                   RMono-Action
 σ .setVar(x, v) = σ ′ =⇒ σ ′ ⊑ σ                      σ .setStore(ρ) = σ ′ =⇒ σ ′ ⊑ σ                  σ .α (v) (σ ′, −) =⇒ σ ′ ⊑ σ
  We say that ⇃ is a restriction operator on a state model S = h|S |, V , Ai, if ⇃ is a restriction operator
on the carrier set |S | and ⇃ is preserved by S. Restriction operators are extended from states to
conﬁgurations in the standard way: hp, σ , cs1 , ii ⇃ hp, σ ′, −, −i , hp, σ ⇃σ ′ , cs1 , ii.
Compatibility. A pre-order (X , ≤) is compatible with a restriction operator ⇃ on X iﬀ the following
properties hold:
                                                               ≤-⇃ Compatibility                       Strengthening
                  ⇃-≤ Compatibility                            x1 ≤ x2                                 x 1 ≤ x 1′     x 2 ⊑ x 2′
                  x 1 ⇃x 2 ≤ x 1
                                                               x1 ⊑ x2                                    x 1 ⇃x 2 ≤ x 1′ ⇃x 2′

Soundness Relations. Given a relation ∼ ∈ X × Y between two sets X and Y , the pre-order on X
induced by ∼, written ≤∼ , is deﬁned as follows: x 1 ≤∼ x 2 if and only if {y | x 1 ∼ y} ⊆ {y | x 2 ∼ y}.
   Deﬁnition B.1 (Soundness Relation - States). Given two state models, Sˆ = h|Sˆ|, V̂ , Ai and S =
h|S |, V , Ai, a soundness relation SR for Sˆ in terms of S is a triple h⇃, ∼s , ∼v i, consisting of: (1) a
restriction operator ⇃ on S;ˆ (2) a binary relation ∼s ⊆ |Sˆ| × |S | between |Sˆ| and |S |; and (3) a ternary
relation ∼v ⊆ |S | × V̂ ×V between |Sˆ|, V̂ , and V , such that ⇃ is compatible with the pre-order induced
                  ˆ
by ∼s (denoted by ≤) and the following constraints hold:
         Store                                                           EvalExpr
         σ̂ ∼s σ =⇒ σ̂ ⊢ σ̂ .store ∼v σ .store                           σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ =⇒ σ̂ ′ ⇃σ̂ ⊢ σ̂ ′ .ee (e) ∼v σ .ee (e)

        SetVar                                                                     SetStore
         σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ v̂ ∼v v                                         σ̂ ≤ σ̂ ′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ ρ̂ ∼v ρ
             =⇒ σ̂ ′ .setVar(x, v̂) ⇃σ̂ ∼s σ .setVar(x, v)                              =⇒ σ̂ ′ .setStore(ρ̂) ⇃σ̂ ∼s σ .setStore(ρ)

     Action                                                                                                     Weakening
          σ̂ ′ .α (v̂)    (σ̂ ′′ , v̂ ′ ) ∧ σ̂ ≤ σ̂ ′ ⇃σ̂ ′′ ∧ σ̂ ∼s σ ∧ σ̂ ⊢ v̂ ∼v v                            σ̂ ⊑ σ̂ ′ ∧ σ̂ ⊢ v̂ ∼v v
                       ′ ′
         =⇒ ∃ σ ,v . σ .α (v)                 (σ ′ ,v ′ ) ∧ σ̂ ′ ⇃σ̂ ∼s σ ′ ∧ σ̂ ′ ⇃σ̂ ⊢ v 1′ ∼v v ′                    =⇒ σ̂ ′ ⊢ v̂ ∼v v
where σ̂ ⊢ ρ̂ ∼v ρ is shorthand for: dom(ρ̂) = dom(ρ) = X and ∀x ∈ X . σ̂ ⊢ ρ̂(x) ∼v ρ(x).

Soundness Relations - Call stacks and Conﬁgurations
                        Inner Frame                                           ∼s -Configuration                   ≤-Configuration
 Top Frame                  σ̂ ⊢ ρ̂ ∼v ρ                ˆ ∼v cs
                                                  σ̂ ⊢ cs                     σ̂ ∼s σ          ˆ ∼v cs
                                                                                         σ̂ ⊢ cs                         σ̂ ≤ σ̂ ′
 σ̂ ⊢ | f | ∼v | f |
                                                  ˆ ∼v | f , x, ρ, i | : cs
                         σ̂ ⊢ | f , x, ρ̂, i | : cs                                     ˆ ii ∼s hp, σ, cs, ii
                                                                              hp, σ̂ , cs,                                 ˆ ii ≤ hp, σ̂ ′ , cs, ii
                                                                                                                  hp, σ̂, cs,
Gillian: Compositional Symbolic Execution for All                                                              33

   Theorem B.2 (One-Step Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness criterion for Sˆ =
  ˆ
h|S |, V̂ , Ai in terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                 ′      ′′          ′                                                   ′′
             cfˆ     cfˆ ∧ cfˆ ≤ cfˆ ⇃cfˆ ′′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf       cf ′ ∧ cfˆ ⇃cfˆ ∼s cf ′

Proof:
                                                          ′       ′′
We proceed by case analysis on the rule that produced cfˆ      cfˆ . We only provide the proof for
the variable assignment and action cases. The others cases are analogous.
                         ′        ′′
1. Assume: 1. (H1) cfˆ        cfˆ
                               ′
             2. (H2) cfˆ ≤ cfˆ ⇃ ˆ ′′
                                 cf
                  3. (H3) cfˆ ∼s cf
2. Case: Assignment
             ′
   2.1. cfˆ = hσ̂ ′, cs, ˆ ii [Destructing on H1 - assignment case]
   2.2. cmd(p, cs,   ˆ i) = x := ê
   2.3. σ̂ .ee(ê)       (σ̂1 , v̂)
   2.4. σ̂1 .setVar(x, v̂ 1 ) = σ̂ ′′
             ′′
   2.5. cfˆ = (σ̂ ′′, cs,  ˆ i + 1)
   2.6. cfˆ = (σ̂, cs,ˆ i) [From H2 + deﬁnition of ≤cf ]
   2.7. σ̂ ≤ σ̂ ′ ⇃σ̂ ′′
   2.8. cf = (σ , cs, i) [From H3 + 2.7 + deﬁnition of ∼cf ]
   2.9. σ̂ˆ ∼s σ
   2.10. σ̂ ⊢ cs  ˆ ∼v cs
   2.11. cmd(p, cs, i) = x := e [From 2.2 + 2.11]
   2.12. σ̂ ≤ σ̂ ′ ⇃σ̂1 [From 2.4 we know that σ̂ ′′ ≤ σ̂1 and from 2.7 we know that σ̂ ≤ σ̂ ′ ⇃σ̂ ′′ .
           From σ̂ ′′ ⊑ σ̂1 , it follows that σ̂ ′ ⇃σ̂ ′′ ≤ σ̂ ′ ⇃σ̂1 , from which it follows, by transitivity that
           σ̂ ≤ σ̂ ′ ⇃σ̂1 .]
   2.13. ∃σ1 , v·
      1. σ .ee(e)         (σ1 , v) [From 2.3 + 2.9 + 2.12 + Correctness relation]
      2. σ̂1 ⇃σ̂ ∼s σ1
      3. σ̂1 ⇃σ̂ ⊢ v̂ ∼v v
   2.14. ∃σ̂2 · [From 2.5 + SM(Trans. strenghtening)]
      1. (σ̂1 ⇃σ̂ ).setVar(x, v̂) = σ̂2
      2. σ̂2 ≤ σ̂ ′′
   2.15. ∃σ ′ : [From 2.14.1 + 2.13.2 + 2.13.3 + CR(setVar )]
      1. σ̂3 ⇃σ̂ ∼s σ ′′
      2. σ̂1 .setVar(x, v) = σ̂ ′′
   2.16. σ̂ ′′ ⇃σ̂ ∼s σ ′ [From 2.14.2 + 2.15.1 + CR-Orders]
   2.17. cf ∼s (σ ′, cs, i + 1) = cf ′ [From 2.8 + 2.11 + 2.13.1 + 2.15.2]
                      ˆ ∼v cs [From 2.10 + noting that σ̂ ′′ ⇃σ̂ ⊑ σ̂ ]
   2.18. σ̂ ′′ ⇃σ̂ ⊢ cs
               ′′
            ˆ
   2.19. cf ⇃cfˆ ∼ cf ′
3. Case: Action
             ′
   3.1. cfˆ = hσ̂ ′, cs, ˆ ii [Destructing on (H1) - action case]
   3.2. cmd(p, cs,   ˆ i) = x := α(ê)
   3.3. σ̂ ′ .ee(ê)       (σ̂1 , v̂ 1 )
   3.4. σ̂1 .ea ˆ (v)       (σ̂2 , v̂ 2 )
   3.5. σ̂2 .setVar(x, v̂ 2 ) = σ̂ ′′
             ′′
   3.6. cfˆ = (σ̂ ′′, cs,  ˆ i + 1)
34                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

     3.7. cfˆ = (σ̂ cs,  ˆ i) [From H2 + deﬁnition of ≤]
     3.8. σ̂ ≤ σ̂ ′ ⇃σ̂ ′′
     3.9. cf = (σ , cs, i) [From H3 + 3.6 + deﬁnition of ∼ cf ]
     3.10. σ̂ ∼s σ
     3.11. σ̂ ⊢ cs  ˆ ∼v cs
     3.12. cmd(p, cs, i) = x := α(ê) [From 3.2 + 3.11]
     3.13. σ̂ ≤ σ̂ ′ ⇃σ̂1 [From 3.4 we know that σ̂2 ⊑ σ̂1 and from 3.5 we know that σ̂ ′′ ⊑ σ̂2 . If follows
             by transitivity that σ̂ ′′ ⊑ σ̂1 , from which it follows (together with σ̂ ′′ ⊑ σ̂ ′ ) that σ̂ ≤ σ̂ ′ ⇃σ̂1 .]
     3.14. ∃σ1 , v 1 · [From 3.5 + 3.11 + 3.13 + CR(ee)]
        1. σ .ee(e)            (σ1 , v 1 )
        2. σ̂1 ⇃σ̂ ∼s σ1
        3. σ̂1 ⇃σ̂2 ⊢ v̂ 1 ∼v v 1
     3.15. σ̂ ′′ ⊑ σ̂2 [From 3.4 + SM(monotonicity)]
     3.16. σ̂ ⊑ σ̂ ′′ [From 3.8 + 3.15]
     3.17. σ̂1 ⇃σ̂ ⊑ σ̂1 ⇃σ̂2 [From 3.16]
     3.18. ∃σ2 , v 2 · [From 3.4 + 3.18 + 3.14.2 + 3.14.3 + CR(ea)]
        1. σ2 .ea (v 2 ) ∼ (σ3 , v 2 )
        2. σ̂2 ⇃(σ̂ ′⇃σ̂ ) ∼ σ2
        3. σ̂ ′′ ⇃(σ̂ ′⇃σ̂ ) ⊢ v 2 ∼v v 2
     3.19. σ̂ ′′ ⊑ σ̂ ′ [From 3.4 + SM(Monotonicity)]
     3.20. σ̂ ′′ ⇃σ̂ ∼ σ3 [From 3.14.1 + 3.14.3 + 3.15, noting that: σ̂3 ⇃(σ̂ ′⇃σ̂ ) = (σ̂ ′′ ⇃σ̂ ′ ) ⇃σ̂ = σ̂ ′′ ⇃σ̂ (since
             σ̂2 ⊑ σ̂1 )]
     3.21. ∃σ̂4 · [From 3.5 + SM(Trans. strenghtening)]
        1. σ̂ ′′ ⇃σ̂ .setVar(x, v 1 ) = σ̂4
        2. σ̂4 ≤ σ̂ ′′
     3.22. ∃σ ′ · [From 3.14 + 3.15 + 3.21.1 + CR(setVar)]
        1. σ̂ ′′ ⇃σ̂ ∼s σ ′
        2. σ1 .setVar(x, v 1) = σ ′
     3.23. σ̂ ′′ ⇃σ̂ ∼s σ ′ [From 3.21.2 + 3.22.1 + CR - Orders]
     3.24. σ̂ ′′ ⇃σ̂ ⊢ cs ∼v cs [From 3.11 + noting that σ̂ ′′ ⇃σ̂ ⊑ σ̂ ]
                ′′
     3.25. cfˆ ⇃cfˆ ∼ cf ′ [From 3.6 + 3.7 + 3.23 + 3.24]

   Theorem B.3 (Soundness - General). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ =
h|Sˆ|, V̂ , Ai in terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                  ′          ′′          ′                                                        ′′
              cfˆ     ∗
                          cfˆ ∧ cfˆ ≤ cfˆ ⇃cfˆ ′′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf        ∗
                                                                                        cf ′ ∧ cfˆ ⇃cfˆ ∼s cf ′

Proof: We proceed by induction on n.
1. Base Case: n = 0
                    ′
   1.1. 1. (H1) cfˆ     0 cfˆ ′′
                          ′
        2. (H2) cfˆ ≤ cfˆ ⇃ ˆ ′′   cf
          3. (H3) cfˆ ∼s cf
             ′       ′′
     1.2. cfˆ = cfˆ [From H1]
     1.3. cf      0 cf ′ [-]
                            ′
     1.4. To prove: cfˆ ⇃cfˆ ∼s cf ′
                          ′
        1.4.1. cfˆ ≤ cfˆ ⇃ ˆ ′ [H2 + 1.2]
                              cf
                          ′
        1.4.2. cfˆ ≤ cfˆ [1.4.1]
Gillian: Compositional Symbolic Execution for All                                                                    35

      1.4.3. cfˆ ≤ cfˆ
      1.4.4. cfˆ ⊑ cfˆ [1.4.3]
                       ′
      1.4.5. cfˆ ≤ cfˆ ⇃cfˆ ′′ [1.4.2 + 1.4.4]
                 ′
      1.4.6. cfˆ ⇃ ˆ ∼s cf [1.4.5 + (H3)]
                         cf
2. Inductive Step: n = k + 1
                       ′
   2.1. 1. (H1) cfˆ              ˆ ′′
                            k+1 cf
                             ′
        2. (H2) cfˆ ≤ cfˆ ⇃cfˆ ′′
        3. (H3) cfˆ ∼s cf [From H1]
   2.2. ∃cfˆ 1 :
              ′
      1. cfˆ     k ˆ
                     cf 1 [To prove: cfˆ 1 ⇃cfˆ ≤ cfˆ 1 ⇃cfˆ ′′ ]
                       ′′
      2. cfˆ 1     cfˆ
             ′′
   2.3. cfˆ ⊑ cfˆ 1 [From 2.2.2]
             ′       ′
   2.4. cfˆ ≤ cfˆ
             ′            ′
   2.5. cfˆ ⇃ ˆ ′′ ≤ cfˆ ⇃ ˆ [From 2.3 + 2.4]
               cf                   cf 1
                     ′
   2.6. cfˆ ≤ cfˆ ⇃cfˆ [From H2 + 2.5]
                         1
   2.7. ∃cf ′ : [Applying the IH on H3 + 2.2.1 + 2.6]
      1. cf       k cf ′
           ˆ
      2. cf 1 ⇃cfˆ ∼s cf ′′
   2.8. cfˆ 1 ≤ cfˆ 1 [-]
                    ′′
   2.9. cfˆ ⊑ cfˆ [From H2]
   2.10. cfˆ ⇃ ˆ ≤ cfˆ ⇃ ˆ ′′ [From 2.8 + 2.9]
              1 cf             1 cf
   2.11. ∃cf : [Applying Theorem 3.2 to 2.2.1 + 2.7.1 + 2.10]
      1. cf ′′    cf
            ′′
      2. cfˆ ⇃cfˆ ∼s cf ′
   2.12. cf k+1 cf ′ [From 2.7.1 + 2.11.1]
                                    ′
   From there, by choosing cfˆ ≡ cfˆ ⇃ ˆ ′′ , we obtain the desired soundness result.
                                                             cf


   Corollary B.4 (Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in
terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:

                                                  ′                                                      ′
                              cfˆ          ∗
                                               cfˆ ∧ (cfˆ ⇃cfˆ ′ ) ∼s cf =⇒ ∃ cf ′ . cf     ∗
                                                                                                cf ′ ∧ cfˆ ∼s cf ′

B.2     Concrete-Symbolic Soundness
   Deﬁnition B.5 (Symbolic Memory Interpretation). Given a symbolic memory model M̂ = h|M̂ |, A, eaˆi
and a concrete memory model M = h|M |, A, ea i, an interpretation of M̂ with respect to M is a func-
tion I : |M̂ | → (X̂ ⇀ V) ⇀ |M | such that:

                                µ̂.α (ê, π )        (µ̂ ′, ê ′, π ′ ) ∧ µ = I(µ̂, ε) ∧ nπ ∧ π ′ oε = true
                                                                                                                     (6)
                                                    =⇒ ∃ µ ′ . µ ′ = I(µ̂ ′, ε) ∧ µ.α (nêoε ) = (µ ′, nê ′oε )


Allocator Interpretation and Restriction.
36                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

   Deﬁnition B.6 (Symbolic Allocator Interpretation). Given a symbolic allocator model AL         ˆ = h|AL|, ˆ V̂ i
                                                                              ˆ
and a concrete allocator model AL = h|AL|, V i, an interpretation of AL with respect to AL is a func-
              ˆ → (V̂ ⇀ V ) ⇀ |AL| such that:
tion IAL : |AL|
   ξˆ.alloc (j) →Y (ξˆ′, v̂) ∧ ξ = IAL (ξˆ, ε) =⇒ ∃ ξ ′ . ξ ′ = IAL (ξˆ′, ε) ∧ ξ .alloc (j) →ε (Y ) (ξ ′, ε(v̂))
  A restriction operator is said to be preserved by an allocator model AL = h|AL|, V i if it satisﬁes
the following two properties:
                                                                     FutureToPastAlloc
                 RMono-Alloc
                                      ′                    ′         ξ .alloc (j) →Y (ξ ′, v) ∧ ξ ′′ ⊑ ξ ⇃ξ ′
                 ξ .alloc (j) →Y (ξ , v) =⇒ ξ ⊑ ξ
                                                                        =⇒ ξ ′′ .alloc (j) →Y (ξ ′ ⇃ξ ′′ , v)
We say that ⇃ is a restriction operator on an allocator model AL = h|AL|, V i, if ⇃ is a restriction
operator on the carrier set |AL| and ⇃ is preserved by AL.
Lifting Interpretations. Given an interpretation I : |M̂ | → (X̂ ⇀ V) ⇀ |M | of a symbolic mem-
ory model M̂ = h|M̂ |, A, ea ˆ i in terms of a concrete memory model M = h|M |, A, ea i, the candidate
soundness relation RT (I) = h⇃, ∼s , ∼v i for SST(M̂) in terms of CST (M) is deﬁned as follows:
                       hµ̂, ρ̂, ξˆ, π i ⇃ ˆ′ ′   , hµ̂, ρ̂, ξˆ ⇃ ˆ′ , π ∧ π ′ i
                                              h_, _, ξ , π i               ξ
                            σ̂ ∼s σ                            ,   ∃ ε . (σ , ε) ∈ Mod(σ̂ )
                            h_, _, _, π i ⊢ ê ∼v v            ,   ∃ ε . nπ oε = true ∧ nêoε = v
where:
                         n                                                                                o
  Mod(hµ̂, ρ̂, π , ξˆi) , (hµ, ρ, ξ i, ε) | nπ oε = true ∧ µ = I(µ̂, ε) ∧ ρ = nρ̂oε ∧ ξ = IAL (ξˆ, n.oε )

     Deﬁnition B.7 (Env). The function Env : Π → Env is deﬁned as follow :
                                                 Env(π ) , {ε | nπ oε = true}
     If σ̂ = hµ̂, ρ̂, ξˆ, π i, we also note
                                                          Env(σ̂ ) = Env(π )
   Deﬁnition B.8 (Restriction of Interpretations with Path Conditions). Given a path condition π ∈ Π,
a concrete memory model M ∈ M, a symbolic memory model M̂ ∈ M̂ and an intepretation I ::
|M̂ | → Env ⇀ |M | of M̂ with respect to M, we deﬁne Iπ :: |M̂ | → Env(π ) ⇀ |M |, the restriction of
I to Env(π ) :
                                             Iπ = I| Env(π )
  Lemma B.9. Let M ∈ M and M̂ ∈ M̂ be a concrete and a symbolic memory model and I :: |M̂ | →
Env ⇀ |M | an interpretation of M̂ with respect to M, and let SR = h⇃, ∼s , ∼v i be the candidate
soundness relation between CST (M) and SST (M̂) induced by I. It holds that :
                          σ̂ ⊑ σ̂ ′ ⇐⇒ Env(σ̂ ) ⊆ Env(σ̂ ′) ∧ σ̂ ′ .ξˆ ⊑ σ̂ .ξˆ
Proof:
First, we need to observe that σ̂ ⊑ σ̂ ′ is just a shorthand for σ̂ ⇃σ̂ ′ = σ̂ . We rewrite the equivalence
we want to prove as
                                      σ̂ ⇃σ̂ ′ = σ̂ ⇐⇒ Env(σ̂ ) ⊆ Env(σ̂ ′) ∧ σ̂ ′ .ξˆ ⊑ σ̂ .ξˆ
We analyse one direction of the equivalence at a time, ﬁrst destructuring on σ̂ and σ̂ ′ .
1. Let: Let σ̂ = hµ̂, ρ̂, ξˆ, π i and σ̂ ′ = hµ̂ ′, ρ̂ ′, ξˆ′, π ′ i
2. Prove: σ̂ ⇃σ̂ ′ = σ̂ =⇒ Env(σ̂ ) ⊆ Env(σ̂ ′) ∧ σ̂ ′ .ξˆ ⊑ σ̂ .ξˆ
   2.1. Assume: σ̂ ⇃σ̂ ′ = σ̂
   2.2. σ̂ ⇃σ̂ ′ = hµ̂, ρ̂, ξˆ ⇃ξˆ′ , π ∧ π ′ i [From 1 and 2.1]
Gillian: Compositional Symbolic Execution for All                                                             37

   2.3. π =⇒ π ′ [From 2.1 and 2.2]
   2.4. ξˆ ⇃ξˆ′ = ξˆ [From 2.1 and 2.2]
   2.5. Env(σ̂ ) ⊆ Env(σ̂ ′) [From 2.3]
   2.6. ξˆ′ ⊑ ξˆ [From 2.4]
3. Prove: σ̂ ⇃σ̂ ′ = σ̂ ⇐= Env(σ̂ ) ⊆ Env(σ̂ ′) ∧ σ̂ ′ .ξˆ ⊑ σ̂ .ξˆ
   3.1. Assume: 1. Env(σ̂ ) ⊆ Env(σ̂ ′)
                      2. σ̂ ′ .ξˆ ⊑ σ̂ .ξˆ
   3.2. π =⇒ π ′ [From 3.1.1]
   3.3. σ̂ ⇃σ̂ ′ = σ̂ [From 3.1.2 and 3.2]
  Lemma B.10. Let σ̂ = hµ̂, ρ̂, ξˆ, π i and σ̂ ′ = hµ̂ ′, ρ̂ ′, ξˆ′, π ′ i. Then it holds that
                                                             Iπ (µ̂) = Iπ (µ̂ ′)
                                                  ′
                                        σ̂ ≤ σ̂       ⇐⇒   ∧ Iπ (ρ̂) = Iπ (ρ̂ ′)
                                                           ∧ π =⇒ π ′
                                                           ∧ Iπ (ξˆ′) ⊑ Iπ (ξˆ)
  Lemma B.11. Let σ̂ = hµ̂, ρ̂, ξˆ, π i and σ̂ ′ = hµ̂ ′, ρ̂ ′, ξˆ′, π ′ i. Then it holds that
                           σ̂ ⊑ σ̂ ′ ⇐⇒ (π =⇒ π ′ ) ∧ Iπ (ξˆ′ ) ⊑ Iπ (ξˆ)
  Lemma B.12 (Lifted Restriction Operator). Let I be an interpretation of a symbolic memory
model M̂ in terms of a concrete memory model M, and h⇃, ∼s , ∼v i = RT (I). Then ⇃ is a restriction
operator on SST (M̂).
Proof:
Let M ∈ M, M̂ ∈ M̂, I an interpretation of M̂ in term of M, h⇃, _, _i = RT (I). We need to prove that
⇃ is a restriction operator on the carrier set |SST (M̂)|, and that it is preserved by SST (M̂).
1. Prove: ⇃ is a restriction operator
   In order to prove that ⇃ is a restriction operator, we need to prove its associativity, idempotence,
   right-commutativity and that it has the Weakening property. We only provide the proof for as-
   sociativity, the other proofs are analogous.
   Prove: (σ̂ ⇃σ̂ ′ ) ⇃σ̂ ′ = σ̂ ⇃(σ̂ ′⇃σ̂ ′′ )
   1.1. Let: 1. σ̂ = hµ̂, ρ̂, ξˆ, π i
                 2. σ̂ ′ = hµ̂ ′, ρ̂ ′, ξˆ′, π ′ i
                 3. σ̂ ′′ = hµ̂ ′′ , ρ̂ ′′, ξˆ′′ , π ′′ i
   1.2. σ̂ ⇃σ̂ ′ = hµ̂, ρ̂, ξˆ ⇃ξˆ′ , π ∧ π ′ i [From 1.1.1 and 1.1.2]
   1.3. (σ̂ ⇃σ̂ ′ ) ⇃σ̂ ′ = hµ̂, ρ̂, (ξˆ ⇃ ˆ′ ) ⇃ ˆ′′ , π ∧ π ′ ∧ π ′′ i [From 1.1.3 and1.2]
                                  ξ          ξ
  1.4. σ̂ ′ ⇃σ̂ ′′ = hµ̂, ρ̂, ξˆ′ ⇃ξˆ′′ , π ′ ∧ π ′′ i [From 1.1.2 and 1.1.3]
  1.5. σ̂ ⇃(σ̂ ′⇃ ′′ ) = hµ̂, ρ̂, ξˆ ⇃ ˆ′ , π ′ ∧ π ′′ i [From 1.1.1 and 1.4]
              σ̂               (ξ ⇃ξˆ ′′ )
   1.6. (σ̂ ⇃σ̂ ′ ) ⇃σ̂ ′ = σ̂ ⇃(σ̂ ′⇃σ̂ ′′ ) [From 1.3, 1.5 and associativity of allocator restriction operator]
2. Prove: ⇃ is preserved by SST(M̂)
   In order to prove that ⇃ is preserved by SST(M̂), we need to prove that all of the state-generating
   functions exposed by the state model are monotonic with respect to the pre-order ⊑ induced by
   ⇃. We only provide the proof for the monotonicity with respect to action executions, the other
   cases are analogous.
   Case: Actions
   Prove: σ̂ .α (v)                (σ̂ ′, −) =⇒ σ̂ ′ ⊑ σ̂
                                  ˆ
   2.1. Let: σ̂ = hµ̂, ρ̂, ξ , π i ∈ SST (M̂)
38                   José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

     2.2. Assume: σ̂ .α (v)              (σ ′, −)
               ′
     2.3. ∃µ̂ , π · ′

               1. (µ̂ ′, ê ′, π ′) ∈ ea
                                       ˆ (α, µ̂, ê)
               2. σ̂ ′ = hµ̂ ′, ρ̂, ξˆ, π ∧ π ′ i
          [From 2.2 and 2.3]
     2.4. Env(σ̂ ′) ⊆ Env(σ̂ ) [From 2.3.2]
     2.5. σ̂ .ξˆ ≤ σ̂ ′ .ξˆ [From 2.3.2]
     2.6. σ̂ ′ ⊑ σ̂ [From 2.4, 2.5 and Lemma B.9]

   Theorem B.13 (Soundness Relation - Lifting). Let I be an interpretation of a symbolic memory
model M̂ in terms of a concrete memory model M; then, RT (I) = h⇃, ∼s , ∼v i is a soundness relation
for SST (M̂) in terms of CST (M).

Proof:
In order to establish that RT (I) = h⇃, ∼s , ∼v i is a soudness relation for SST (M̂) in terms of CST (M),
we need to prove that
   1. ⇃ is a restriction order on SST (M̂)
   2. ∼s and ∼v are monotonic with respect to the functions exposed by the state model
   3. ⇃ is compatible with ≤
The ﬁrst property is the result of Lemma B.12. Let us prove property 2 and 3.
1. Prove: ∼s and ∼v are monotonic with respect to the functions exposed by the state model
   We need to prove that the property holds for store, ee, setVar, setStore and actions. We only
   provide the proof for the action cases. The other cases are analogous.
   Case: Actions
   Prove: σ̂ .α (v̂)          (σ̂ ′, v̂ ′) ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ v̂ ∼v v
                =⇒ ∃ σ , v ′ . σ .α (v)
                            ′                         (σ ′, v ′) ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ⊢ v̂ ′ ∼v v ′
   1.1. Assume: 1. (H1) σ̂ = hµ̂, ρ̂, ξˆ, π i
                       2. (H2) σ̂ ′′ = hµ̂ ′′ , ρ̂ ′′, ξˆ′′ , π ′′ i
                       3. (H3) σ = hµ, ρ, ξ i
                       4. (H4) σ̂ .α (v̂)          (σ̂ ′, v̂ ′)
                       5. (H5) σ̂ ′′ ≤ σ̂ ⇃σ̂ ′
                       6. (H6) σ̂ ∼s σ
                       7. (H7) σ̂ ⊢ v̂ ∼v v
   1.2. ∃µ̂ ′, v̂ ′, π ′ ·
            1. µ̂.α (v̂, π )     (µ̂ ′, v̂ ′, π ′ )
            2. σ̂ .α (v̂)     hµ̂, ρ̂, ξˆ, π ∧ π ′ i, v̂ ′ )
            3. σ̂ = hµ̂, ρ̂, ξˆ, π ∧ π ′ i
                   ′

         [From H1 and H4]
   1.3. ∃ε·
            1. nπ ′′ oε = true
            2. nv̂oε = v
         [From H2 and H7]
   1.4. ∃ε ′ ·
            1. ε ≤ ε ′
            2. nπ ′′ oε ′ = true
            3. I(µ̂ ′′, ε ′) = µ
            4. I ρ̂ ′′ε ′ = ρ
            5. I(ξˆ′′ ) ⊑ ξ
Gillian: Compositional Symbolic Execution for All                                                          39

        [From H6, 1.3.1 ]
   1.5. σ̂ ⇃σ̂ ′ = hµ̂, ρ̂, ξˆ, π ∧ π ′ i [From H1 and 1.2.3]
   1.6. 1. π ′′ =⇒ π ∧ π ′
             2. ξˆ ⊑ ξˆ′′
             3. Iπ ′′ (µ̂) = Iπ ′′ (µ̂ ′′ )
             4. Iπ ′′ (ρ̂) = Iπ ′′ (ρ̂ ′′ )
        [From H2, H5, 1.5 ]
   1.7. nv̂oε ′ = v[From 1.3.2 and 1.4.1]
   1.8. nπ ∧ π ′ o= true [From 1.4.2 and 1.6.1]
   1.9. I µ̂, ε ′ = µ [From 1.4.2, 1.4.3 and 1.6.3]
   1.10. ∃ε ′′, µ ′ ·
               1. µ ′ = I(µ̂ ′, ε ′′)
               2. ε ′ ≤ ε ′′
               3. µ.α (v)            (µ ′, nv̂ ′oε ′′ )
          [From 1.2.1, 1.7, 1.8, 1.9]
   1.11. Let: σ ′ = hµ ′ , ρ, ξ i
   1.12. σ .α (v)            (σ ′, nv̂ ′oε ′′ )[From H3, 1.10.3 and 1.11]
   1.13. σ̂ ⇃σ̂ ′′ = hµ̂ , ρ̂, ξˆ′′ , π ′′ i [From 1.2.3 and H2]
             ′              ′

   1.14. Prove: (σ ′, ε ′′) ∈ Mod(σ̂ ′ ⇃σ̂ ′′ )
      1.14.1. nπ ′′ o= true [From 1.4.2 and 1.10.2]
      1.14.2. µ̂ ′ = I(µ̂, ε ′′) [From 1.10.1]
      1.14.3. ρ = I(ρ̂, ε ′′ ) [From 1.4.4 and 1.10.2]
      1.14.4. ξ = I(ξˆ, ε ′′ ) [From 1.4.5 and 1.10.2]
      1.14.5. (σ̂ ′, ε ′′ ) ∈ Mod(σ̂ ′ ⇃σ̂ ′′ ) [From 1.14.1 to 1.14.4]
   1.15. nπ ′′ oε ′′ = true
   1.16. σ̂ ′ ⇃σ̂ ′′ ⊢ v̂ ′ ∼v nv̂oε ′′ [From 1.13 and 1.15]
2. Prove: ⇃ is compatible with ≤
   In order to prove that ⇃ is compatible with ≤, we need to prove the ⇃ − ≤ compatibility, the ≤ − ⇃
   compatibility and the strengthening property. We only provide the proof for the strengthening
   property. The other cases are analogous.
   2.1. Let: 1. (H1) σ̂1 = hµ̂ 1 , ρ̂ 1 , ξˆ1 , π1 i
                  2. (H2) σ̂2 = hµ̂ 2 , ρ̂ 2 , ξˆ2 , π2 i
                  3. (H3) σ̂1′ = hµ̂ 1′ , ρ̂ 1′ , ξˆ1′, π1′ i
                  4. (H4) σ̂2′ = hµ̂ 2′ , ρ̂ 2′ , ξˆ2′, π2′ i
                  be 4 symbolic states
   2.2. Assume: 1. (H5) sst 1 ≤ σ̂1′
                        2. (H6) σ̂2 ⊑ σ̂2′
        Prove: σ̂1 ⇃σ̂2 ≤ σ̂1′ ⇃σ̂2′
   2.3. Mod hµ̂ 1 , ρ̂ 1 , ξˆ1 , π1 i ⊆ Mod hµ̂ 1′ , ρ̂ 1′ , ξˆ1′, π1′ i [From H1, H2 and H5]
   2.4. (π2 =⇒ π2′ ) ∧ ξˆ2′ ⊑ ξˆ2 [From H6]
   2.5. σ̂1 ⇃σ̂2 = hµ̂ 1 , ρ̂ 1, ξˆ1 ⇃ξˆ2 , π1 ∧ π2 i[From H1 and H2]
   2.6. σ̂ ′ ⇃σ̂ ′ = hµ̂ ′ , ρ̂ 1,′ ξˆ′ ⇃ ˆ′ , π ′ ∧ π ′ i [From H3 and H4]
         1    2      1         1 ξ2     1       2
  2.7. Prove:    Mod hµ̂ 1 , ρ̂ 1, ξˆ1 ⇃ξˆ2 , π1 ∧ π2 i ⊆ Mod hµ̂ 1′ , ρ̂ 1′ , ξˆ1′ ⇃ξˆ′ , π1′ ∧ pc 2′ i
                                                                                       2
     2.7.1. Let: (hµ, ρ, ξ i, ε) ∈ Mod hµ̂ 1 , ρ̂ 1, ξˆ1 ⇃ ˆ , π1 ∧ π2 i
                                                               ξ2
     2.7.2.       1. nπ1 ∧ π2 oε = true
40                       José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

               2. µ = I µ̂, ε
               3. I ξˆ1 ⇃ξˆ2 ⊑ ξ
               4. ρ = I ρ̂ 1ε
             [From 2.7.1]
      2.7.3. Mod hµ̂ 1 , ρ̂ 1, ξˆ1 ⇃ξˆ2 , π1 ∧ π2 i ⊆ Mod hµ̂ 1 , ρ̂ 1 , ξˆ1 , π1 i
      2.7.4. Mod hµ̂ 1 , ρ̂ 1, ξˆ1 ⇃ ˆ , π1 ∧ π2 i ⊆ Mod hµ̂ ′ , ρ̂ ′ , ξˆ′, π ′ i [From 2.3 and 2.7.3]
                                         ξ2                         1   1   1   1
      2.7.5. (hµ, ρ areci) ∈ Mod hµ̂ 1′ , ρ̂ 1′ , ξˆ1′, π1′ i [From 2.7.1 and 2.7.4]
      2.7.6. 1. nπ1′ oε = true
                2. µ = I µ̂ ′, ε
                3. I ξˆ1′ ⊑ ξ
                4. ρ = I ρ̂ 1′ ε
             [From 2.7.5]
      2.7.7. I(ξˆ1 , ε) ⇃ I(ξˆ2, ε ) ⊑ ξ [From 2.7.2.3 ]
      2.7.8. I(ξˆ2 , ε) ⊑ ξ [From 2.7.7]
      2.7.9. I(ξˆ2′, ε) ⊑ I(ξˆ2 , ε) [From 2.4]
      2.7.10. I(ξˆ2′, ε) ⊑ ξ [From 2.7.8 and 2.7.9]
      2.7.11. I(ξˆ′, ε) ⇃ ˆ′ ⊑ ξ [From 2.7.6.4 and 2.7.10]
                     1      I(ξ 2, ε )
      2.7.12. I(ξˆ1′ ⇃ξˆ′ , ε) ⊑ ξ [From 2.7.11 ]
                        2
      2.7.13. nπ2 oε = true [From 2.7.2.1]
      2.7.14. nπ2′oε = true [From 2.4 and 2.7.13]
      2.7.15. nπ1′ ∧ π2′ oε = true [From 2.7.2.1 and 2.7.14]
      2.7.16. (hµ, ρ, ξ i, ε) ∈ Mod(hµ̂ 1′ , ρ̂ 1′ , ξˆ1′ ⇃ξˆ′ , π1′ ∧ π2′ i)
                                                             2


B.3    While: Sound Symbolic Analysis
The interpretation of While symbolic memories in terms of While concrete memories, IW , is induc-
tively deﬁned as follows:
                                   Cell                                             Union
      Empty                              l = nêoε       v = nê ′ oε               µ 1 = IW (µ̂ 1 , ε)     µ 2 = IW (µ̂ 2 , ε)
      IW (∅, ε) , ∅                                  ′
                                    IW (ê.p 7→ ê , ε) , l .p 7→ v                      IW (µ̂ 1 ⊎ µ̂ 2 , ε) , µ 1 ⊎ µ 2

 Lemma B.14 (While: Memory Interpretation). IW is an interpretation of M̂ W with respect to
MW.
Proof:
For every action α ∈ A, we have to prove that:
                   µ̂.α (ê, π )  (µ̂ ′, ê ′, π ′ ) ∧ µ = I(µ̂, ε) ∧ nπ ∧ π ′ oε = true
                                                                                                                                  (7)
                                 =⇒ ∃ µ ′ . µ ′ = I(µ̂ ′, ε) ∧ µ.α (nêoε ) = (µ ′, nê ′oε )
We proceed by case analysis on the rule that was used to derive µ̂.α (ê, π )                             (µ̂ ′, ê ′, π ′ ).
1. Case: lookup
   1.1. Assume: 1. (H1) µ̂.lookup ([ê, p] , π ) (µ̂ ′, ê ′, π ′ )
                        2. (H2) nêoε = v
                        3. (H3) µ = IW (µ̂, ε)
   1.2. ∃ ê ′′ ·
           1. π ⊢ ê ′′ = ê
           2. µ̂ = _ ⊎ (ê ′′, p) 7→ ê ′
Gillian: Compositional Symbolic Execution for All                                                         41

            3. π ′ = π
            4. µ̂ ′ = µ̂
        [From H1]
   1.3. µ = _ ⊎ IW ((ê ′′, p) 7→ ê ′, ε) [From H3 + 1.2.2]
   1.4. µ = _ ⊎ (nê ′′ oε , p) 7→ nê ′ oε [From 1.3]
   1.5. nê ′′ oε = nêoε [From H4 + 1.2]
   1.6. µ = _ ⊎ (nêoε , p) 7→ nê ′oε [From 1.4 and 1.5]
   1.7. µ.lookup ([nêoε , p])            (µ, nê ′oε ) [From 1.6]
2. Case: mutate
   2.1. Assume: 1. (H1) µ̂.mutate ([ê, p, ê ′] , π )                   (µ̂ ′, ê ′′, π ′ )
                          2. (H2) nêoε = v and nê oε = v ′          ′

                          3. (H3) µ = IW (µ̂, ε)
   2.2. ∃ê ′′ , µ̂ ′′ ·
            1. µ̂ = µ̂ ′′ ⊎ (ê ′′, p) 7→ _
            2. π ′ ⊢ ê = ê ′′
            3. µ̂ ′ = µ̂ ′′ ⊎ (ê ′′, p) 7→ ê ′
        [From H1]
   2.3. µ = IW (µ̂ ′′, ε) ⊎ (nê ′′ oε , p) 7→ _ [From H3 + 2.2.3]
   2.4. nê ′′ oε = nêoε = v [From H2 + H4 + 2.2.2]
   2.5. ∃l · v = l [We assume ε is "well-formed"]
   2.6. µ = IW (µ̂ ′′, ε) ⊎ (l, p) 7→ _ [From 2.3 + 2.5]
   2.7. µ.mutate ([l, p, v ′])            (IW (µ̂ ′′, ε) ⊎ (l, p) 7→ v ′, v ′)
   2.8. IW (µ̂ , ε) = IW (µ̂ , ε) ⊎ IW ((ê ′′, p) 7→ ê ′, ε)
                    ′                 ′′

                           = IW (µ̂ ′′, ε) ⊎ (nê ′′ oε , p) 7→ nê ′ oε
                           = IW (µ̂ ′′, ε) ⊎ (l, p) 7→ v ′                    [From H2 + 2.4 + 2.5]
3. Case: dispose
   3.1. Assume: 1. (H1) µ̂.dispose (ê, π )                    (µ̂ ′, true, π )
                          2. (H2) nêoε = v
                          3. (H3) µ = IW (µ̂, ε)
   3.2. µ̂ ↾ê, π = (_, µ̂ ′ ) [From H1]
   3.3. IW (µ̂ ↾ê, π , ε) = (_, IW (µ̂ ′, ε)) [From 3.2]
   3.4. IW (µ̂ ↾ê, π , ε) = IW (µ̂, ε) ↾nêoε
   3.5. IW (µ̂, ε) ↾nêoε = µ ↾nê oε [From H3]
   3.6. µ ↾nê oε = (_, IW (µ̂ ′, ε)) [From 3.3 - 3.5]
   3.7. µ.dispose (nêoε )            (IW (µ̂ ′, ε), true)
   Theorem B.15 (While: Soundness). Given h⇃, ∼s , ∼v i = RT (IW ), it holds that:
               cfˆ  ∗ ˆ′
                      cf ∧ (cfˆ ⇃ ˆ ′ ) ∼s cf =⇒ ∃ cf ′ . cf
                             W                cf
                                                                  ′     ˆ′
                                                             W cf ∧ cf ∼s cf
                                                                                 ′
                                                                                                      2
42                           José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

C     SECTION 4: PARAMETRIC VERIFICATION
C.1      Parametric Assertion Language
GIL Parametric Assertions
   P, Q ∈ A ∆            ,     π | δ hei | pn(e) | P ∗ Q
 pred ∈ Pred             ,     pred pn(x) :− P0 ; ... ; Pn
      ω ∈ ΩV             ,     pn(v), where v ∈ V

  Deﬁnition C.1 (Predicate State Constructor (PST )). The predicate state constructor PST : S → S is
deﬁned as PST (h|S |, V , Ai) , h|S ′ |, V , A ⊎ {setP, getP}i, where:
      • |S ′ |                              ,    |S | × ΩV
      • setVarp (hσ, ωi, x, v)              ,    hsetVar(σ, x, v), ωi
      • setStorep (hσ, ωi, ρ)               ,    hsetStore(σ, ρ), ωi
      • storep (hσ, −i)                     ,    store(σ )
      • eep (hσ, −i, e)                     ,    ee(σ, e)
      • eap (α, hσ, ωi, v)                  ,    {(hσ ′, ωi, v ′) | (σ ′,v ′ ) ∈ ea(α, σ, v)}, if α < {getP, setP}
      • eap (setP, hσ, ωi, [pn, v])         ,    (hσ, (pn(v) : ω)i, −)
      • eap (getP, hσ, ωi, [pn, v])         ,    (hσ, ω 1 ++ ω 2 i, −), where ω = ω 1 ++ [ pn(v) ] ++ ω 2
   Deﬁnition C.2 (Core Predicate Action Interpretation). A core predicate action interpretation is a
4-tuple AI ∈ AI = h∆, A, set, дeti consisting of a set of core predicates ∆, a set of actions A, and
two functions set, дet : ∆ → A; we write setδ for set(δ ) and getδ for дet(δ ). A core predicate action
interpretation h∆, A, set, дeti is said to be well-formed with respect to a state model S = h|S |, V , Ai
in and only if, for all core predicates δ ∈ ∆, it holds that:
                                            σ .getδ (v)        σ ′ ⇐⇒ σ ′ .setδ (v)           σ                                       (8)
   Given a state model S = h|S |, V , Ai and a core action interpretation h∆, A, set, дeti, the induced
action interpretation of an assertion P ∈ A ∆ is a pair of functions consisting of the getter and setter
of P, respectively, getP and setP . Formally, we deﬁne two induced functions:
   • set ∆S : A ∆ → |S | → (X̂ ⊎ X ⇀ V ) ⇀ |S |              (σ ′ = set ∆S (P, σ , θ ) ≡pp σ .setP (θ )                               σ ′)
   • дet ∆S : A ∆ → |S | → (X̂ ⊎ X ⇀ V ) ⇀ |S |             (σ ′ = дet ∆S (P, σ , θ ) ≡pp σ .getP (θ )                                σ ′)
mapping each assertion P ∈ A ∆ to its getter and setter, respectively, as follows:
Assertion Interpretation: σ .set P (θ)     σ ′ and σ .getP (θ)     σ′
  set - star                 get - star                      set - boolean expr                          get - boolean expr
     σ .set P (θ) σ′            σ .get P (θ)    σ′              σ .ee (θ(e)) = v                         σ .ee (¬ θ(e)) = v
    σ ′ .setQ (θ) σ ′′         σ ′ .getQ (θ)     σ ′′        σ .assume (v)       σ′                      σ .assume(v) = ∅
     σ .set(P ∗Q ) (θ)        σ ′′        σ .get(P ∗Q ) (θ)    σ ′′         σ .set π (θ)      σ′          σ .get π (θ)       σ

     set - pred                            get - pred                      set - core pred               get - core pred
     σ .ee ([pn, θ(e)]) = v                σ .ee ([pn, θ(e)]) = v            σ .ee (θ(e)) = v              σ .ee (θ(e)) = v
       σ .setP (v)     σ′                    σ .дetP (v)     σ′             σ .setδ (v)     σ′            σ .getδ (v)     σ′
      σ .setpn(e ) (θ)        σ′           σ .get pn(e ) (θ)   σ′          σ .setδ he i (θ)    σ′         σ .getδ he i (θ)       σ′

   Lemma C.3 (Assertion Interpretation). Let h∆, A, set, дeti be a well-formed core predicate in-
terpretation with respect to a predicate state model S = h|S |, V , Ai; then, it holds that: σ .setP (θ ) σ′
if and only if σ ′ .getP (θ ) σ.
   Theorem C.4 (Assertion Interpretation - Soundness). Let SR = h⇃, ∼s , ∼v i be a soundness
relation for Sˆ = h|Sˆ|, V̂ , Ai in terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s ; and let
Gillian: Compositional Symbolic Execution for All                                                           43

h∆, A, set, дeti be a well-formed core predicate action interpretation for Sˆ and S; then, it holds that:
                                 ˆ
                      σ̂ .set P (θ)  σ̂ ′ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                                                                                                        (9)
                                   =⇒ ∃ σ ′ . σ .setP (θ )         σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
                                ˆ
                      σ̂ .getP (θ)   σ̂ ′ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                                                                                                       (10)
                                   =⇒ ∃ σ ′ . σ .getP (θ )         σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
Proof:
We are going to prove equations the two equations by induction on the structure of P, consider-
ing only the core predicate and separating conjunction cases for both proofs. The other cases are
analogous.
1. Prove: σ̂ .setP (θ)     ˆ         σ̂ ′ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                             ′
               =⇒ ∃ σ . σ .setP (θ )               σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
   1.1. Case: δ hei
      1.1.1. Assume: 1. (H1) σ̂ .setδ he i (θ)        ˆ       σ̂ ′
                                           ′′
                            2. (H2) σ̂ ≤ σ̂ ⇃σ̂ ′
                            3. (H3) σ̂ ′′ ∼s σ
                            4. (H4) σ̂ ′′ ⊢ θˆ ∼v θ
             Prove: ∃ σ ′ . σ .setδ he i (θ )               σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
      1.1.2. ∃v̂.
                               ˆ
                  1. σ̂ .ee (θ(e))      = v̂
                  2. σ̂ .setδ (v̂)         σ̂ ′
             [From H1]
      1.1.3. ∃v.
                  1. σ .ee (θ (e)) = v
                  2. σ̂ ′′ ⊢ v̂ ∼v v
             [From H2, H3, H4 and 1.1.2.1]
      1.1.4. ∃σ̂ ′ .
                  1. σ .setδ (v)           σ′
                        ′
                  2. σ̂ ⇃σ̂ ′′ ∼s σ    ′

             [From H2, H3 1.1.2.2 and 1.1.3.2]
      1.1.5. σ .setδ he i (θ )         σ′
      Âă[From 1.1.3.1 and 1.1.4.1]
   1.2. Case: P ∗ Q
      1.2.1. Assume: 1. (H1) σ̂ .setP ∗Q (θ)         ˆ       σ̂ ′
                                           ′′
                            2. (H2) σ̂ ≤ σ̂ ⇃σ̂ ′
                            3. (H3) σ̂ ′′ ∼s σ
                            4. (H4) σ̂ ′′ ⊢ θˆ ∼v θ
             Prove: ∃ σ ′ . σ .setP ∗Q (θ )                 σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
      1.2.2. ∃σ̂1 .
                  1. σ̂ .setP (θ)ˆ        σ̂1
                  2. σ̂1 .setQ (θ) ˆ        σ̂ ′
                ′
      1.2.3. σ̂ ⊑ σ̂1 [From 1.2.2.2]
      1.2.4. σ ≤ σ̂
      1.2.5. σ̂ ⇃σ̂ ′ ≤ σ̂ ⇃σ̂1 [From 1.2.3 and 1.2.4]
      1.2.6. σ̂ ′′ ≤ σ̂ ⇃σ̂1 [From (H2) and 1.2.5]
      1.2.7. ∃σ1 .
                  1. σ .setP (θ )         σ1
44                   José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

                 2. σ̂1 ⇃σ̂ ′′ ∼s σ1
             [From H3, H4, 1.2.2.1 and IH]
      1.2.8. σ̂1 ≤ σ̂1
      1.2.9. σ̂ ′′ ⊑ σ̂ ′ [From H2]
      1.2.10. σ̂ ′′ ⊑ σ̂ ′ [From 1.2.8 and 1.2.9]
      1.2.11. σ̂ ′′ ⊑ σ̂1 [From 1.2.6]
      1.2.12. σ̂ ′′ ⊑ σ̂ ′′
      1.2.13. σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′ [From 1.2.11 and 1.2.12]
      1.2.14. σ̂1 ⇃σ̂ ′′ ⊢ θˆ ∼v θ [From H4 and 1.2.13]
      1.2.15. ∃σ ′ .
                   1. σ1 .setQ (θ )             σ′
                   2. σ̂ ⇃(σ̂1⇃σ̂ ′′ ) ∼s σ ′
                          ′

               [From 1.2.2.2 and 1.2.7.2]
      1.2.16. σ̂ ′ ⊑ σ̂1 [From 1.2.2.2]
      1.2.17. σ̂ ′ ⇃σ̂1⇃σ̂ ′′ = (σ̂ ′ ⇃σ̂1 ) ⇃σ̂ ′′ [From 1.2.16]
                                 = σ̂ ′ ⇃σ̂ ′′
      1.2.18. σ̂ ′ ⇃σ̂ ′′ ∼s σ ′ [From 1.2.17 and 1.2.15.2]
      1.2.19. σ .setP ∗Q (θ )             σ ′ [From 1.2.7.1 and 1.2.15.2]
2. Prove: σ̂ .getP (θ)      ˆ       σ̂ ∧ σ̂ ′′ ≤ σ̂ ⇃σ̂ ′ ∧ σ̂ ′′ ∼s σ ∧ σ̂ ′′ ⊢ θˆ ∼v θ
                                         ′
                             ′
               =⇒ ∃ σ . σ .getP (θ )               σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
   2.1. Case: δ hei
      2.1.1. Assume: 1. (H1) σ̂ .getδ he i (θ)       ˆ      σ̂ ′
                                             ′′
                            2. (H2) σ̂ ≤ σ̂ ⇃σ̂ ′
                            3. (H3) σ̂ ′′ ∼s σ
                            4. (H4) σ̂ ′′ ⊢ θˆ ∼v θ
             Prove: ∃ σ ′ . σ .getδ he i (θ )             σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
      2.1.2. ∃v̂.
                               ˆ
                 1. σ̂ .ee (θ(e))       = v̂
                 2. σ̂ .getδ (v̂)            σ̂ ′
             [From H1]
      2.1.3. ∃v.
                 1. σ .ee (θ (e)) = v
                 2. σ̂ ′′ ⊢ v̂ ∼v v
             [From H2, H3, H4 and 2.1.2.1]
      2.1.4. ∃σ̂ ′ .
                 1. σ .getδ (v)              σ′
                        ′
                 2. σ̂ ⇃σ̂ ′′ ∼s σ     ′

             [From H2, H3 2.1.2.2 and 2.1.3.2]
      2.1.5. σ .getδ he i (θ )          σ′
      Âă[From 2.1.3.1 and 2.1.4.1]
   2.2. Case: P ∗ Q
      2.2.1. Assume: 1. (H1) σ̂ .getP ∗Q (θ)         ˆ     σ̂ ′
                                             ′′
                            2. (H2) σ̂ ≤ σ̂ ⇃σ̂ ′
                            3. (H3) σ̂ ′′ ∼s σ
                            4. (H4) σ̂ ′′ ⊢ θˆ ∼v θ
             Prove: ∃ σ ′ . σ .setP ∗Q (θ )              σ ′ ∧ σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
      2.2.2. ∃σ̂1 .
Gillian: Compositional Symbolic Execution for All                                                                           45

                  1. σ̂ .getQ (θˆ)          σ̂1
                  2. σ̂1 .getP (θ)  ˆ        σ̂ ′
      2.2.3. Prove: σ̂ ≤ σ̂ ⇃σ̂1′′

         2.2.3.1. σ̂ ′′ ≤ σ̂ [From H2]
         2.2.3.2. σ̂ ′ ⊑ σ̂1 [From 2.2.2.2]
         2.2.3.3. σ̂ ′′ ⇃σ̂ ′ ≤ σ̂ ′′ ⇃σ̂1 [From 2.2.3.1 and 2.2.3.2]
         2.2.3.4. σ̂ ′′ ≤ σ̂ ′′ ⇃σ̂1 [From H2 and 2.2.3.3]
      2.2.4. ∃σ1 .
                  1. σ .getQ (θ )           σ1
                  2. σ̂1 ⇃σ̂ ′′ ∼s σ1
      2.2.5. Prove: σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂ ′
         2.2.5.1. σ̂1 ≤ σ̂1
         2.2.5.2. σ̂ ′′ ⊑ σ̂ ′ [From H2]
         2.2.5.3. σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂ ′ [From 2.2.5.1 and 2.2.5.2]
      2.2.6. Prove: σ̂1 ⇃σ̂ ′′ ⊢ θˆ ∼v θ
         2.2.6.1. σ̂ ′ ⊑ σ̂1 [From 2.2.2.2]
         2.2.6.2. σ̂ ′′ ⊑ σ̂ ′ [From H2]
         2.2.6.3. σ̂ ′′ ⊑ σ̂1 [From 2.2.6.1 and 2.2.6.2]
         2.2.6.4. σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′ [From 2.2.6.3]
         2.2.6.5. σ̂1 ⇃σ̂ ′′ ⊢ θˆ ∼v θ [From H4 and 2.2.6.4]
      2.2.7. ∃σ ′ .
                  1. σ1 .getP (θ )           σ′
                  2. σ̂ ⇃(σ̂1⇃σ̂ ′′ ) ∼s σ ′
                         ′

             [From 2.2.2.2, 2.2.4.2, 2.2.5, 2.2.6 and IH]
      2.2.8. Prove: σ̂ ′ ⇃(σ̂1⇃σ̂ ′′ ) = σ̂ ′ ⇃σ̂ ′′
         2.2.8.1. σ̂ ′ ⊑ σ̂1 [From 2.2.2.2]
         2.2.8.2. σ̂ ′ ⇃(σ̂1⇃σ̂ ′′ ) = (σ̂ ′ ⇃σ̂1 ) ⇃σ̂ ′′
         2.2.8.3. σ̂ ′ ⇃(σ̂1⇃σ̂ ′′ ) = σ̂ ′ ⇃σ̂ ′′ [From 2.2.8.1 and 2.2.8.2]
      2.2.9. σ̂ ′ ⇃σ̂ ′′ ∼s σ ′
      2.2.10. σ .getP ∗Q (θ )            σ ′ [From 2.2.4.1 and 2.2.7.1]

C.2    Parametric Verification Semantics

Extended GIL Syntax
 c ∈ C A , c ∈ CA | x := e 1 (e 2 ) with [j; (x̂i : ei ) |in=0 ] |                          proc ∈ Proc A , proc f (x){c}
           fold pn(e) with [j; (x̂i : ei ) |in=0 ] | unfold pn(e)                           p ∈ Proд : F ⇀ Proc A
                                                                                                        A




                                                                              ′
Veriﬁcation Semantics of GIL: p ⊢ hσ, cs, iio               hσ ′, cs ′, jio
                                                        UnFold
          Non-logical Cmd                                      cmd(p, cs, i) = unfold pn(e)        v = σ .ee (e)
                 cmd(p, cs, i) ∈ CA                         p.preds.pn = pred pn(x ) :− P 0 ; ... ; P n 0 ≤ j ≤ n
           ⌊p⌋ ⊢ hσ, cs, i i    hσ ′, cs′, j i          σ .дet P ([pn, v])    σ′     σ ′ .setP j ([x 7→ v])    (σ ′′, −)
            p ⊢ hσ, cs, i i    hσ ′, cs′, j i                            p ⊢ hσ, cs, i i   hσ ′′, cs, i+1i
46                       José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

                                                                            ′
Veriﬁcation Semantics of GIL: p ⊢ hσ, cs, iio                  hσ ′, cs ′, jio (continued)
  Fold                                                          Spec Call
                                                      n                                                                      n
  cmd(p, cs, i) = fold pn(e0 ) with [j; (x̂ i : ei ) |i=1  ]            cmd(p, cs, i) = x := e(e0 ) with [j; (x̂ i : ei ) |i=1  ]
                                       n                                                                                 n
                  (v i = σ .ee (ei )) |i=0                                     f = σ .ee (e)       (v i = σ .ee (ei )) |i=0
      p.preds.pn = pred pn(x ) :− P 0 ; ... ; P n                                 p.specs.f .j = {P } f (x 0 ) {Q, e ′ }
      θ = [x 7→ v 0, x̂ 1 7→ v 1, ..., x̂ n 7→ v n ]                                θ = [x 0 7→ v 0, ..., x̂ n 7→ v n ]
  σ .get P j (θ )   σ′      σ ′ .set P ([pn, v])       σ ′′     σ .ee (θ (e ′ )) = v      σ .getP (θ )     σ′       σ ′ .setQ (θ )   σ ′′
                                    ′′                                                             ′′
             p ⊢ hσ, cs, i i     hσ , cs, i+1i                             p ⊢ hσ, cs, i i     hσ .setVar(x, v), cs, i+1i


   Theorem C.5 (Verification). Let SR = h⇃, ∼s , ∼v i be a soundness relation for Sˆ = h|Sˆ|, V̂ , Ai in
terms of S = h|S |, V , Ai and ≤ the pre-order induced by ∼s . It holds that:
                                  ′                                                                         ′
                   cfˆ     ∗
                               cfˆ ∧ cfˆ = cfˆ ⇃cfˆ ′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf              ∗
                                                                                                  cf ′ ∧ cfˆ ∼s cf ′
Proof:
In order to prove this theorem, we prove the following more general claim, from which the theorem
immediately follows :
                       ∗ ˆ′            ′′                    ′′                          ′
             cfˆ          cf ∧ cfˆ ≤ cfˆ ⇃cfˆ ′ ∧ cfˆ ∼s cf =⇒ ∃ cf ′ . cf ∗ cf ′ ∧ cfˆ ⇃cfˆ ′′ ∼s cf ′
We proceed by use analysis on the rule used to derive cfˆ                   ˆ ′ . We only cover the non-logic
                                                                         ∗ cf

command, unfold and spec call cases, the other cases being analogous.
1. Case: Non-logic commands
                                           ∗ ˆ′
   1.1. Assume: 1. (H1) cfˆ                  cf
                                       ′′
                        2. (H2) cfˆ ≤ cfˆ ⇃cfˆ ′
                                       ′′
                        3. (H3) cfˆ ∼s cf
                                                          ′
        Prove: ∃ cf ′ . cf ∗ cf ′ ∧ cfˆ ∼s cf ′
                        ′
   1.2. cfˆ         cfˆ [From H1]
   1.3. ∃cf .′

            1. cf         cf ′
                    ′
            2. cfˆ ⇃cfˆ ′′ cf ′
        [From H2, H3, 1.2 and Theorem 4.1]
   1.4. cf ∗cf ′ [From 1.3 and execution of non-logic command.]
2. Case: Unfold
   2.1. Assume: 1. (H1) cfˆ                ∗ cfˆ′
                                       ′′
                        2. (H2) cfˆ = cfˆ ⇃cfˆ ′
                                       ′′
                        3. (H3) cfˆ ∼s cf
                                                          ′
        Prove: ∃ cf ′ . cf ∗ cf ′ ∧ cfˆ ∼s cf ′
   2.2. ∃ p, σ̂ , σ̂1 , σ̂ ′, cs1 , i, j, pn, e, x, Pi |in=0, v̂.
            1. cfˆ = hσ̂ , cs1 , ii
            2. cmd(p, cs 1 , i) = unfold pn(e)
            3. p.preds.pn = pred pn(x) :− P0 ; ... ; Pn
            4. σ̂ .ee (e) = v̂
            5. σ̂ .дetP ([pn, v̂])            σ̂1
            6. σ̂1 .setP j ([x 7→ v̂])            (σ̂ ′, −)
                    ′
                  ˆ           ′
            7. cf = hσ̂ , cs 1 , i + 1i
   2.3. ∃ σ̂ ′′ .
                    ′′
            1. cfˆ = hσ̂ ′′ , cs1 , ii
Gillian: Compositional Symbolic Execution for All                                          47

           2. σ̂ ′′ ≤ σ̂ ⇃σ̂ ′
       [From 2.2.1 and H2]
  2.4. ∃ σ , cs2 .
                    ′′
           1. cfˆ = hσ , cs 2 , ii
           2. s σ̂ ′′σ
           3. σ̂ ′′ ⊢ cs 1 ∼v cs 2
       [From 2.3.1 and H3]
  2.5. cmdp, cs 2 , i = unfold pn(e) [From 2.4.3] and 2.2.2
  2.6. σ̂ ′′ ≤ σ̂ [From 2.3.2]
  2.7. ∃ v.
           1. σ .ee (e) = v
           2. σ̂ ′′ ⊢ v̂ ∼v v
  2.8. Prove: σ̂ ′′ ≤ σ̂ ⇃σ̂1
     2.8.1. σ̂ ≤ σ̂
     2.8.2. σ̂ ′ ⊑ σ̂1 [From 2.2.6]
     2.8.3. σ̂ ⇃σ̂ ′ ≤ σ̂ ⇃σ̂1 [From 2.8.1 and 2.8.2]
     2.8.4. σ̂ ′′ ≤ σ̂ ⇃σ̂1 [From 2.3.2 and 2.8.3]
  2.9. ∃σ1 .
           1. σ .дetP ([pn, v])               σ1
           2. σ̂1 ⇃σ̂ ′′ ∼s σ1
       [From 2.2.5, 2.4.2, 2.7.2, 2.8]
  2.10. Prove: σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂ ′
     2.10.1. σ̂1 ≤ σ̂1
     2.10.2. σ̂ ′′ ⊑ σ̂ ′ [From 2.3.2]
     2.10.3. σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂ ′ [From 2.10.1 and 2.10.2]
  2.11. Prove: σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′
     2.11.1. σ̂ ′′ ⊑ σ̂ ′ [From 2.3.2]
     2.11.2. σ̂ ′ ⊑ σ̂2 [From 2.2.6]
     2.11.3. σ̂ ′′ ⊑ σ̂1 [From 2.11.1 and 2.11.2]
     2.11.4. σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′                                 [From 2.11.3]
                  σ̂ ′′ ⇃(σ̂1⇃σ̂ ′′ )    = (σ̂ ′′ ⇃σ̂1 ) ⇃σ̂ ′′
                  = σ̂ ′′ ⇃σ̂ ′′         = σ̂ ′′
  2.12. σ̂1 ⇃σ̂ ⊢ v̂ ∼v v [From 2.7.2 and 2.11]
                 ′′

  2.13. ∃σ ′ .
             1. σ1 .setP j ([x 7→ v])               (σ ′, −)
                     ′
             2. σ̂ ⇃(σ̂1⇃σ̂ ′′ ) ∼s σ   ′

         [From 2.2.6, 2.9.2, 2.10, 2.12 and Theorem 4.5]
  2.14. Prove: σ ′ ⇃(σ̂1⇃σ̂ ′′ ) = σ̂ ′ ⇃σ̂ ′′
     2.14.1. σ̂ ′ ⊑ σ̂1 [From 2.2.6]
     2.14.2. σ̂ ′ ⇃(σ̂1⇃σ̂ ′′ ) = (σ̂ ′ ⇃σ̂1 ) ⇃σ̂ ′′
     2.14.3. (σ̂ ′ ⇃σ̂1 ) ⇃σ̂ ′′ = σ̂ ′ ⇃σ̂ ′′ [From 2.14.1]
     2.14.4. σ̂ ′ ⇃(σ̂1⇃σ̂ ′′ ) = σ̂ ′ ⇃σ̂ ′′ [From 2.14.2 and 2.14.3]
  2.15. σ̂ ′ ⇃σ̂ ′′ ∼s σ ′ [From 2.13.2 and 2.14.3]
  2.16. cf ∗ hσ ′, cs2 , i + 1i = cf ′ [From 2.2.3, 2.4.1, 2.5, 2.7.1, 2.9.1 and 2.13.1]
  2.17. Prove: σ̂ ′′ ⊑ σ̂ ′ ⇃σ̂ ′′
     2.17.1. σ̂ ′′ ⊑ σ̂ ′ [From 2.3.2]
48                      José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner




      2.17.2. σ̂ ′′ ⊑ σ̂ ′ ⇃σ̂ ′′                                [From 2.17.1]
                 σ̂ ′′ ⇃(σ̂ ′⇃σ̂ ′′ )    = (σ̂ ′′ ⇃σ̂ ′ ) ⇃σ̂ ′′
                 = σ̂ ′′ ⇃σ̂ ′′          = σ̂ ′′
                  ′ ′′
      2.17.3. σ̂ ⇃σ̂ ⊢ cs1 ∼v cs 2 [From 2.4.3 and 2.17.2]
      2.17.4. cfˆ ⇃cfˆ ′′ cf ′ [From 2.2.7, 2.3.1, 2.15, 2.16 and 2.17.3]
3. Case: Spec Call
                                          ∗ ˆ′
   3.1. Assume: 1. (H1) cfˆ                 cf
                                      ′′
                       2. (H2) cfˆ ≤ cfˆ ⇃cfˆ ′
                                      ′′
                       3. (H3) cfˆ ∼s cf
                                                          ′
        Prove: ∃ cf ′ . cf ∗ cf ′ ∧ cfˆ ∼s cf ′
     3.2. ∃ p, σ̂ , σ̂1 , σ̂2 , σ̂ ′, cs1 , i, j, e R , v̂ R , e f , f , x 0 , x̂ i |in=1 , ei |in=0, v̂i |in=0, P, Q, θˆ.
              1. cfˆ = hσ̂ , cs1 , ii
              2. cmd(p, cs 1 , i) = x := e f (e 0 ) with [j; (x̂ i : ei ) |in=1 ] ∧ f = σ̂ .ee (e f )
              3. p.specs.f .j = {P } f (x 0 ) {Q, e R }
              4. σ̂ .ee (e 0 ) = v̂ 0
              5. σ̂ .ee (ei ) = v̂i |in=1
              6. σ̂ .ee (e R ) = v̂ R
              7. θˆ = [x 0 7→ v̂ 0, ..., x̂ n 7→ v̂n ]
              8. σ̂ .getP (θ)  ˆ        σ̂1
              9. σ̂1 .setQ (θ)   ˆ       σ̂2
            10. σ̂2 .setVar(x R , v̂ R ) hσ̂ ′, cs1 , i + 1i
                     ′
            11. cfˆ = hσ̂ ′, cs 1 , i + 1i
     3.3. ∃ σ̂ ′′
                     ′′
              1. cfˆ = hσ̂ ′′ , cs1 , ii
              2. σ̂ ′′ ≤ σ̂ ⇃σ̂ ′
          [From 3.2.1, 3.2.11 and H2]
     3.4. ∃ σ , cs2 ,
              1. cf = hσ , cs2 , ii
              2. σ̂ ′′ ∼s σ
              3. σ̂ ′′ ⊢ cs 1 ∼v cs 2
          [From 3.3.1 and H3]
     3.5. cmd(p, cs2 , i) = x := e f (e 0 ) with [j; (x̂ i : ei ) |in=1 ] ∧ f = σ .ee (e f ) [From 3.2.2 and 3.4.3]
     3.6. σ̂ ′′ ≤ σ̂ [From 3.3.2]
     3.7. ∃ v 0 .
              1. σ .ee (e 0 ) = v 0
              2. σ̂ ′′ ⊢ v̂ 0 ∼v v 0
          [From 3.2.4, 3.4.2 and 3.6]
     3.8. ∃ vi |in=1 . ∀1 ≤ i ≤ n.
              1. σ .ee (ei ) = vi
              2. σ̂ ′′ ⊢ v̂i ∼v vi
          [From 3.2.5, 3.4.2 and 3.6]
     3.9. ∃ v R
              1. σ .ee (e R ) = v R
              2. σ̂ ′′ ⊢ v̂ R ∼v v R
Gillian: Compositional Symbolic Execution for All                                49

       [From 3.2.6, 3.4.2 and 3.6]
  3.10. Let: θ = [x 0 7→ v 0 , ..., x̂ n 7→ vn ]
  3.11. σ̂ ′′ ⊢ θˆ ∼v θ [From 3.2.7, 3.7.2, 3.8.2, 3.9.2, 3.10]
  3.12. Prove: σ̂ ′′ ≤ σ̂ ⇃σ̂1
     3.12.1. σ̂ ≤ σ̂
     3.12.2. σ̂ ′ ⊑ σ̂1 [From 3.2.9]
     3.12.3. σ̂ ⇃σ̂ ′ ≤ σ̂ ⇃σ̂1 [From 3.12.2 and 3.12.3]
     3.12.4. σ̂ ′′ ≤ σ̂ ⇃σ̂1 [From 3.3.2 and 3.12.3]
  3.13. ∃ σ1 .
             1. σ .getP (θ )          σ1
             2. σ̂1 ⇃σ̂ ′′ ∼s σ1
        [From 3.2.8, 3.4.2, 3.11, 3.12 and Theorem 4.5]
  3.14. Prove: σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂2
     3.14.1. σ̂1 ≤ σ̂1
     3.14.2. σ̂ ′′ ⊑ σ̂ ′ [From 3.3.2]
     3.14.3. σ̂ ⊑ σ̂2 [From 3.2.10]
     3.14.4. σ̂ ′′ ⊑ σ̂2 [From 3.14.2 and 3.14.3]
     3.14.5. σ̂1 ⇃σ̂ ′′ ≤ σ̂1 ⇃σ̂2 [From 3.14.1 and 3.14.4]
  3.15. Prove: σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′
     3.15.1. σ̂ ′′ ⊑ σ̂ ′ [From 3.3.2]
     3.15.2. σ̂ ′ ⊑ σ̂1 [From 3.2.9, 3.2.10 and transitivity]
     3.15.3. σ̂ ′′ ⊑ σ̂1 [From 3.15.1 and 3.15.2]
     3.15.4. σ̂ ′′ ⊑ σ̂1 ⇃σ̂ ′′                                [From 3.15.3]
                 σ̂ ′′ ⇃(σ̂1⇃σ̂ ′′ )    = (σ̂ ′′ ⇃σ̂1 ) ⇃σ̂ ′′
                 = σ̂ ′′ ⇃σ̂ ′′         = σ̂ ′′
                      ˆ
  3.16. σ̂1 ⇃σ̂ ′′ ⊢ θ ∼v θ [From 3.11 and 3.15]
  3.17. ∃ σ2
             1. σ1 .setQ (θ )          σ2
             2. σ̂2 ⇃σ̂ ′′ ∼s σ2
        [From 3.2.2, 3.13.2, 3.14, 3.16 and Theorem 4.5]
  3.18. Prove: σ̂2 ⇃σ̂ ′′ ≤ σ̂2 ⇃σ̂ ′
     3.18.1. σ̂2 ≤ σ̂2
     3.18.2. σ̂ ′′ ⊑ σ̂ ′ [From 3.3.2]
     3.18.3. σ̂2 ⇃σ̂ ′′ ≤ σ̂2 ⇃σ̂ ′ [From 3.18.1 and 3.18.2]
  3.19. Prove: σ̂ ′′ ⊑ σ̂2 ⇃σ̂ ′′
     3.19.1. σ̂ ′′ ⊑ σ̂ ′ ⊑ σ̂2 [From 3.3.2 and 3.2.10]
     3.19.2. σ̂ ′′ ⇃(σ̂2⇃σ̂ ′′ ) = (σ̂ ′′ ⇃σ̂2 ) ⇃σ̂ ′′ [From 3.19.1]
                 = σ̂ ′′ ⇃σ̂ ′′      = σ̂ ′′
  3.20. σ̂2 ⇃σ̂ ′′ ⊢ v̂ R ∼v v R [From 3.9.2 and 3.19]
  3.21. ∃ σ ′ .
             1. σ2 .setVar(x R , v R )             σ′
                   ′
             2. σ̂ ⇃(σ̂2⇃σ̂ ′′ ) ∼s σ  ′

  3.22. Prove: σ̂ ′ ⇃(σ̂2⇃σ̂ ′′ ) = σ̂ ′ ⇃σ̂ ′′
     3.22.1. σ̂ ′ ⇃(σ̂2⇃σ̂ ′′ ) = (σ̂ ′ ⇃σ̂2 ) ⇃σ̂ ′′ [Given that σ̂ ′ ⊑ σ̂2 ]
                                     = σ̂ ′ ⇃σ̂ ′′
           ′
  3.23. σ̂ ⇃σ̂ ′′ ∼s σ     ′

  3.24. Prove: σ̂ ′′ ⊑ σ̂ ′ ⇃σ̂ ′′
50                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

        3.24.1. σ̂ ′′ ⊑ σ̂ ′ [From 3.3.2]
        3.24.2. σ̂ ′′ ⇃(σ̂ ′⇃σ̂ ′′ ) = (σ̂ ′′ ⇃σ̂ ′ ) ⇃σ̂ ′′
                                     = σ̂ ′′ ⇃σ̂ ′′ = σ̂ ′′
              ′
     3.25. σ̂ ⇃σ̂ ⊢ cs1 ∼v cs2 [From 3.4.3 and 3.23]
                  ′′

     3.26. cf = hσ , cs 2 , ii       hσ ′, cs2 , i + 1i = cf ′
            ˆ
     3.27. cf ⇃cfˆ ∼s cf
                   ′      ′


C.3      While: Verification
      • ∆W = {cell}
      • AW = {lookup, mutate, dispose, setCell, getCell}
While: Concrete and Symbolic Memories (Continued)

      C-SetCell                                                  S-SetCell
      (l,p) < dom(µ)      µ ′ = µ ⊎ l .p 7→ v                        µ̂ ↾êl ,p, π = ∅        µ̂ ′ = µ̂ ⊎ eˆl .p 7→ êv
         µ.setCell ([l,p,v])      (µ ′, true)                    µ̂.setCell ([ˆel , p, eˆv ] , π )    {(µ̂ ′, true, true)}

        C-GetCell                                            S-GetCell
             µ = µ ′ ⊎ l .p 7→ v                             π ⊢ (eˆl = eˆl′ ∧ êv = eˆv′ )          µ̂ = µ̂ ′ ⊎ êl′ .p 7→ êv′
         µ.getCell ([l,p,v])      (µ ′, true)                    µ̂.getCell ([eˆl , p, eˆv ] , π )    {(µ̂ ′, true, true)}


   Lemma C.6 (While: Concrete Core Predicate Interpretation). The core predicate action in-
terpretation h∆W , AW , [cell 7→ setCell], [cell 7→ getCell]i is well-formed with respect to CST (M W ).
Proof:
We need to prove that the following equivalent holds for any concrete memories µ, µ ′ ∈ M W , and
any triple [l, p, v] :
                             σ .getCell ([l, p, v])     σ ′ ⇐⇒ σ ′ .setCell ([l, p, v]) σ
We start by proving the left to right implication, before proving the right to left implication.
1. Prove: σ .getCell ([l, p, v])             σ ′ ⇒ σ ′ .setCell ([l, p, v]) σ
   1.1. Assume: (H1) σ .getCell ([l, p, v])             σ ′

        Prove: σ ′ .setCell ([l, p, v])           σ
   1.2. ∃ µ ′ .µ = µ ′ ⊎ (l, p) 7→ v [From (H1)]
   1.3. ∃ µ ′′, pi |in=1 .
            1. µ ′ ↾l = µ ′′ ⊎ _
            2. µ ′′ = ⊎ni=1 (l, pi ) 7→ _
            3. (pi , p) |in=1
        [From 1.2]
   1.4. σ ′ .setCell ([l, p, v])       σ [From 1.3]
2. Prove: σ .getCell ([l, p, v])             σ ′ ⇐ σ ′ .setCell ([l, p, v]) σ
   2.1. Assume: (H1) σ .setCell ([l, p, v])             σ′
        Prove: σ ′ .getCell ([l, p, v])            σ
             ′′      n
   2.2. ∃ µ , pi |i =1 .
            1. µ ′ ↾l = µ ′′ ⊎ _
            2. µ ′′ = ⊎ni=1 (l, pi ) 7→ _
            3. p ∈ {p1 , ..., pn }
            4. µ ′ = µ ⊎ (l, p) 7→ v
        [From 2.2]
Gillian: Compositional Symbolic Execution for All                                                                       51

   2.3. σ ′ .getCell ([l, p, v])     σ [From 2.2]
   Lemma C.7 (While: Symbolic Core Predicate Interpretation). The core predicate action in-
terpretation h∆W , AW , [cell 7→ setCell], [cell 7→ getCell]i is well-formed with respect to SST (M̂ W ).
Proof: The proof is analogous to the proof of Lemma C.6.
  Lemma C.8 (Extended While: Memory Interpretation). IW is an intepretation of While sym-
bolic memories M̂ W with respect to the concrete memories M W , for While extended with speciﬁcations.
Proof:
For every action α ∈ AW , we have to prove that:
∀µ̂, µ̂ ′ ∈ M̂ W ; µ ∈ M W ; ê, ê ′ ∈ Ê; ε ∈ Env; π , π ′ ∈ Π.
                              µ̂.α (ê, π )    (µ̂ ′, ê ′, π ′ ) ∧ µ = IW (µ̂, ε) ∧ nπ ∧ π ′ oε = true
                                                                                                                        (11)
                                             =⇒ ∃ µ ′ . µ ′ = IW (µ̂ ′, ε) ∧ µ.α (nêoε ) = (µ ′, nê ′oε )
We proceed by case analysis on the rule that was used to derive µ̂.α (ê, π )                              ′    ′   ′
                                                                                                        (µ̂ , ê , π ).
For the lookup, mutate and dispose actions we refer to the Lemma 3.7.
Only the setCell and getCell cases remain. We prove the setCell case, the getCell case being analo-
gous.
1. Case: setCell
   1.1. Assume: 1. (H1) µ̂.setCell ([êl , p, êv ] , π )                (µ̂ ′, ê ′, π ′ )
                          2. (H2)
                              a. nêl oε = l
                              b. nêv oε = v
                          3. (H3) µ = IW (µ̂, ε)
                          4. (H4) nπ ∧ π ′ oε = true
          Prove: ∃ µ ′ . µ ′ = IW (µ̂ ′, ε) ∧ µ.α (nêoε ) = (µ ′, nê ′oε )
   1.2. ∃ µ̂ 1 , µ̂ 2 , pi |in=1
             1. µ̂ ↾êl , π = µ̂ 1 ⊎ _
             2. µ̂ 1 = ⊎ni=1 (êi , pi ) 7→ _
             3. (p , pi ) |in=1
             4. µ̂ ′ = µ̂ ⊎ (êl , p) 7→ êv
             5. ê ′ = true
             6. π ′ = true
          [From (H1)]
   1.3. IW (µ̂, ε) ↾nêl oε = IW (µ̂, ε) ⊎ _ [From 1.2.1 and (H4)]
   1.4. IW (µ̂ 1 , ε) = ⊎ni=1 (nêl oε , pi ) 7→ _ [From 1.2.2]
   1.5. µ ↾l = IW (µ̂ 1 , ε) ⊎ _ [From (H2.a), (H3) and 1.3]
   1.6. IW (µ̂ 1 , ε) = ⊎ni=1 (l, pi ) 7→ _ [From (H2.a) 1.4]
   1.7. µ.setCell ([l, p, v])               (µ ⊎ (l, p) 7→ v, true) [From 1.2.3, 1.5 and 1.6]
                    ′
   1.8. IW (µ̂ , ε) = IW (µ̂ ⊎ (êl , p) 7→ êv , ε)                          [From 1.2.4]
                               = IW (µ̂, ε) ⊎ IW ((êl , p) 7→ êv , ε)
                               = µ̂ ⊎ (nêl oε , p) 7→ nêv oε                [From (H3)]
                               = µ̂ ⊎ (l, p) 7→ v                             [From (H2)]
52                     José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

D SECTION 5: PARAMETRIC BI-ABDUCTIVE ANALYSIS
D.1      Parametric Bi-abductive Analysis
Action Fixes
  ea : A → |S | → V ⇀ ℘(|S | × V ) ⊎ ℘(A ∆ )                         ((σ ′ ,v ′ ) ∈ ea(α, σ, v) ≡pp σ .α (v)   Shσ ′ ,v ′ i)
                                                                                   (P ∈ ea(α, σ, v) ≡pp σ .α (v)    FhPi)

 Deﬁnition D.1 (Well-formedness of Fixes). If the original state is extended with a generated ﬁx, it
must be possible to execute the action successfully.
                  σ .α (v)     FhPi ∧ σ .setP ([ ])         σ ′′ =⇒ ∃ σ ′, v ′ .σ ′′ .α (v)         Shσ ′, v ′i                (12)

Bi-Abductive Analysis.
  Deﬁnition D.2 (BiState Constructor (BiST )). The bi-abductive state constructor BiST : S → S is
deﬁned as BiST (h|S |, V , Ai) , h|S ′ |, V , Ai, where:
      • |S ′ |                     ,    |S | × A ∆
      • setVarbi (hσ, Pi, x, v)    ,    hsetVar(σ, x, v), Pi
      • setStorebi (hσ, Pi, ρ)     ,    hsetStore(σ, ρ), Pi
      • storebi (hσ, −, −i)        ,    store(σ )
      • eebi (hσ, −, −i, e)        ,    ee(σ, e)
      • eabi (α, hσ, Pi, v)        ,    {(hσ ′, Pi, v ′ ) | σ .α (v)    Shσ ′, v ′i} if α , assume
      • eabi (assume, hσ, Pi, v)   ,    {(hσ  ′              ′
                                                , P ∗ π i, v ) | ⌈v⌉ = π ∧ σ .assume (v)         Shσ ′ ,v ′ i}
                                                                                                                                 
                                            hσ ′′ , P ∗ Qi, v ′)
      • eabi (α, hσ, Pi, v)        ,
                                                    | σ .α (v)    FhQi ∧ σ .setQ ([ ])      σ ′ ∧ σ ′ .α (v)      Shσ ′′ ,v ′ i
     Lemma D.3 (One-Step).
       p ⊢ hhσ , Pi, cs, ii BiST(S ) hhσ ′, Qi, cs ′, jio
             =⇒ ∃ P ′ . Q ⊢ P ∗ P ′ ∧ σ .setP ′ ([])         σ ′′ ∧ σ ′′ ≤ σ ⇃σ ′ p ⊢ hσ ′′ , cs, ii            ′    ′
                                                                                                            S hσ , cs , ji
                                                                                                                           o


Proof:
We proceed by case analysis on the rule used to produce p ⊢ hhσ , Pi, cs, ii BiST(S ) hhσ ′, Qi, cs ′, jio .
We only provide the proof for the execute action case. The other cases are analogous.
There are two rules concerning the execute action case :
   1. The case where the action does not generate an error
   2. The case where the action generates an error.
We are providing the proof for both cases.
1. Case: [No Error]
   1.1. Assume: p ⊢ hhσ , Pi, cs, ii BiST(S ) hhσ ′, Qi, cs ′, jio
   1.2. 1. cmd(p, cs, i) = x := α(exp)
           2. σ .ee (exp) = v
           3. σ .α (v)    Shσ ′′, v ′i
           4. σ = σ .setVar(x, v ′)
                ′      ′′

        [From 1.1]
   1.3. p ⊢ hσ , cs, ii S hσ ′, cs, i + 1io [From 1.2]
   1.4. P ⊢ P ∗ emp
   1.5. σ .setemp ([])    σ
2. Case: [Action Error]
   2.1. Assume: p ⊢ hhσ , Pi, cs, ii BiST(S ) hhσ ′, Qi, cs ′, jio
   2.2. 1. cmd(p, cs, i) = x := α(exp)
Gillian: Compositional Symbolic Execution for All                                                                           53

          2. σ .ee (exp) = v
          3. σ .α (v)       FhQi
          4. σ ′ = σ ′′ .setVar(x, v ′)
          5. σ .setP ′ ([])    σ ′′
                ′′
          6. σ .α (v)        Shσ1 , v 1 i
          7. σ ′ = σ1 .setVar(x, v 1 )
          8. Q = P ∗ P ′
       [From 2.1]
  2.3. σ ′′ .ee (exp) = v [From 2.2.2 and 2.2.4]
  2.4. p ⊢ hσ ′′, cs, ii S hσ ′, cs, i + 1io [From 2.2.1, 2.3 and 2.2.3]
  Theorem D.4 (Multiple-Step).
    p ⊢ hhσ , Pi, cs, ii ∗BiST(S ) hhσ ′, Qi, cs ′, jio
          =⇒ ∃ P ′ . Q ⊢ P ∗ P ′ ∧ σ .setP ′ ([])         σ ′′ ∧ σ ′′ ≤ σ ⇃σ ′ p ⊢ hσ ′′ , cs, ii    ∗ hσ ′ , cs ′ , ji o
                                                                                                     S
Proof:
We proceed by induction on the length of the derivation p ⊢ hhσ , Pi, cs, ii                 ∗        hhσ ′ , Qi, cs ′, jio .
                                                                                             BiST(S )
1. Case: n = 0
   1.1. Assume: p ⊢ hhσ , Pi, cs, ii 0BiST(S ) hhσ ′, Qi, cs ′, jio
   1.2. 1. σ ′ = σ
        2. Q = P
        3. cs ′ = cs
        4. j = i
   1.3. p ⊢ hσ , cs, ii 0S hσ , cs, iio
   1.4. P ⊢ P ∗ emp
   1.5. σ .setemp ([])           σ
2. Case: n = k + 1
   2.1. Assume: p ⊢ hhσ , Pi, cs, ii k+1       BiST(S )
                                                        hhσ ′, Qi, cs ′, jio
   2.2. ∃ σ1 , Q 1 , cs1 , j 1 .
           1. p ⊢ hhσ , Pi, cs, ii kBiST(S ) hhσ1 , Q 1 i, cs 1 , j 1 io
           2. p ⊢ hhσ1 , Q 1 i, cs 1 , j 1 i BiST(S ) hhσ ′, Qi, cs ′, j ′io
        [From 2.2]
   2.3. ∃ σ2 , P2
           1. Q 1 ⊢ P ∗ P2
           2. σ .setP2 ([])          σ2
           3. ] ⊢ hσ2 , cs, jii K h[i σ1, cs1, j1 Spo
        [From IH and 2.2.1]
   2.4. ∃ P3 , σ3
           1. Q ⊢ Q 1 ∗ P3
           2. σ1 .setP3 ([])          σ3
           3. p ⊢ hσ3 , cs, ii S hσ ′, cs ′, jio
        [From previous Lemma]
   2.5. ∃ σ4
           1. σ2 .setP3 ([])          σ4
           2. p ⊢ hσ4 , cs, ii kS hσ3 , cs1 , j 1 io
        [From Frame rule, 2.4.2 and 2.3.3]
   2.6. p ⊢ hσ4 , cs, ii k+1            ′   ′  o
                                 S hσ , cs , ji [From 2.4.3 and 2.5.2]
   2.7. σ .set⋆P2 P3 ([])          σ5 [From 2.3.2 and 2.5.1]
54                  José Fragoso Santos, Petar Maksimović, Sacha-Élie Ayoun, and Philippa Gardner

     2.8. Q ⊢ P ∗ P2 P3 ∗ [From 2.3.1 and 2.4.1]
     Theorem D.5 (Bi-Abduction).
                     p ⊢ hhσ , empi, cs, ii ∗BiST(S ) hhσ ′ , Pi, cs ′, jio ∧ σ .setP ([ ])   σ ′′
                           =⇒ p ⊢ hσ ′′ , cs, ii S hσ ′, cs ′, jio
Proof:: Immediate corollary from Theorem D.4
