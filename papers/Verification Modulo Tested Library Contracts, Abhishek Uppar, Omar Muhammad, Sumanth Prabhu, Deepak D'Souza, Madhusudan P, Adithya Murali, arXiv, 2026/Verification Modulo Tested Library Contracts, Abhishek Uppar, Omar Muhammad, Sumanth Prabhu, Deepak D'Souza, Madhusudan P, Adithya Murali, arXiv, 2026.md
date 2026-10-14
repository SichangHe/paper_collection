                                        Verification Modulo Tested Library Contracts
                                        ABHISHEK UPPAR, Indian Institute of Science, India
                                        OMAR MUHAMMAD, Indian Institute of Science, India
                                        SUMANTH PRABHU S, Relyance AI, India
                                        DEEPAK D’SOUZA, Indian Institute of Science, India
                                        P. MADHUSUDAN, University of Illinois Urbana-Champaign, Department of Computer Science, USA
                                        ADITHYA MURALI, University of Wisconsin, USA
arXiv:2604.15533v2 [cs.PL] 7 May 2026




                                        We consider the problem of verification modulo tested library contracts as a step towards automating the
                                        verification of client programs that use complex libraries. We formulate this problem as the synthesis of
                                        modular contracts for the library methods used by the client that are adequate to prove the client correct, and
                                        that also pass the scrutiny of a testing engine that tests the library against these contracts. We also consider a
                                        new form of method contracts called contextual contracts that arise in this setting that hold in the context of
                                        the client program, and can often be simpler and easier to infer than classical modular contracts. We provide a
                                        counterexample-guided learning framework to solve this problem, in which the synthesizer interacts with a
                                        constraint solver as well as the testing engine in order to infer adequate modular/contextual method contracts
                                        and inductive invariants for the client. The main synthesis engines we use are generalizing CHC solvers that
                                        are realized using ICE learning algorithms. We realize this framework in a tool called Dualis and show its
                                        efficacy on benchmarks where clients call large libraries.

                                        1   Introduction
                                        Formal verification mechanisms have made great strides in the last few decades, resulting in mature
                                        logics, verification paradigms, automation using logic engines, and tool frameworks. However, for
                                        expressive specifications of large programs, complete automation is not within reach. Effective
                                        verification methods for large software today call for human-written annotations, such as contracts,
                                        that enable modular and hence scalable verification. Furthermore, human annotations in terms of
                                        inductive invariants for iterative blocks of code are needed to enable scalable automation using logic
                                        solvers. While there are techniques for synthesizing inductive invariants and contracts [15, 16, 28, 29,
                                        34, 45], inductive invariant synthesis is a hard search problem, and current synthesis techniques do
                                        not scale. We are at an impasse today as it has become clear that completely automated verification
                                        is unlikely to scale to large code and complex specifications. Automated verification, however, does
                                        work well for smaller pieces of code with complex specifications, or large code bases with simple
                                        specifications (e.g., null pointer dereference checking, data races, etc.).
                                           In this paper, we explore a more pragmatic choice in the design space—relaxing verification
                                        guarantees in order to achieve scalable and complete automation for larger code-bases. In particular,
                                        we are interested in automatically verifying smaller client programs that utilize large libraries.
                                        A traditional verification approach would require annotating the libraries with contracts strong
                                        enough to prove the client code, and then proving the client code and the libraries against their
                                        contracts using further annotations (such as inductive loop invariants). Annotating and proving
                                        large libraries against their contracts is a daunting task; however, in many settings, the client code
                                        is smaller, and we can automate the synthesis of annotations using current techniques.
                                           We negotiate this space by relaxing the guarantee of formal verification of libraries in order to
                                        scale verification. More precisely, our aim is to automatically synthesize contracts for libraries,
                                        formally prove that the client is correct assuming these contracts, and, instead of formally verifying
                                        the library code, demand that the library pass extensive testing against the contracts.
                                           We propose the following novel verification modulo tested library contracts problem: Given a
                                        client program 𝐶 using a library 𝐿, find a set of formal contracts Π for the methods in 𝐿 such that
                                        (a) the client 𝐶 is proved correct assuming the contracts Π for 𝐿, and (b) a given deterministic

                                                                                                1
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


test-generator with a bound on its resources is unable to find any tests for the library methods that
violate their contract in Π.
   Though the precise problem we define here seems new, there have been several variants of the
above problem in recent years that have considered synthesizing contracts for libraries aided by
testing only (and not verification)—for functional programs (albeit without synthesizing inductive
invariants for clients) [48] and for synthesizing preconditions and contracts purely from libraries [4,
5] (see related work in Section 8 for more details).
   In this paper, we seek entirely automated methods that solve the stated problem, both in terms
of synthesizing contracts for libraries as well as synthesizing the inductive annotations for the
client that prove it correct. Furthermore, we are interested in the setting of imperative object-
oriented programming languages, where we assume libraries implement classes that encapsulate
data and the methods, where classes manage unbounded collections of objects (like container
classes implemented using data structures), and classes and objects have state that evolves with
method calls.

Learning Library Contracts and Client Invariants Simultaneously. The key problem to solve
is one of synthesis—synthesizing contracts Π for the libraries as well as synthesizing annotations
for the client code (inductive loop invariants, contracts for client’s methods, etc.) such that a logic
engine can validate the verification conditions for the basic blocks in the client code, and at the
same time ensure the library contracts are vetted correct by the given test generator.
   The first main technical contribution of this paper is a learning framework that simultaneously
synthesizes adequate contracts for libraries and inductive annotations for client code to solve the
above problem. We propose a counterexample guided learning/synthesis framework. In each round,
we require the verifier to handle a set of CHC (Constrained Horn Clause) constraints derived from
the client, 𝐶𝐻𝐶 (𝐶), along with a set of positive samples for library methods. Intuitively, we require
the verification engine to solve the CHC constraints of the client in a way that the predicates
associated with library contracts in the CHC include the positive samples. (These positive samples
can also be encoded into CHC constraints, of course; but the crucial aspect is that these positive
examples evolve during the verification process). In each round, we require that the verification
engine solves the CHC constraints (thereby finding inductive annotations for the client and contracts
for the library methods) while ensuring that the contracts for the library methods include the
positive samples.
   It is important to our framework that the CHC solver generalize as well (a generic CHC solver
does not suffice). A CHC solver that overfits the contracts (say allowing only the given positive
examples to be the library’s contract) will not be useful in our context— the problem is not to solve
the CHCs but to simultaneously generalize the library contracts and solve the CHCs.
   Our framework pairs a generalizing solver for CHCs and positive samples with a test generator,
working in rounds. In each round, we take the CHC solver proposed annotations, and check if the
testing engine can find violations of the library against their synthesized contracts. If the testing
engine is able to produce failing tests, we extract positive examples that show violation of the
contract, augment the set of positive samples, and iterate. If the testing engine is unable to falsify
the contracts, we can terminate, as we have verified the client modulo tested library contracts.
   Turning to realizing generalizing solvers for CHCs and positive examples, we propose ICE-
learning engines [12, 16, 17] as natural candidates. ICE-learning engines strive to solve CHCs
by learning inductive invariants and annotations in hypothesis classes, aiming to find simplest
expressions that solve CHC constraints, and thus naturally generalize. Given CHC constraints,
an ICE solver works itself in an iterative loop involving an ICE learner and a constraint solver.
The ICE learner, in each iteration proposes inductive invariants that solve the CHCs, and the

                                                   2
Verification Modulo Tested Library Contracts


constraint solver responds using positive, negative, and implication counterexamples (ICE samples)
when validity fails. Consequently, the positive examples generated by testing engines (in the outer
loop) naturally fit into an ICE-learning framework as we can add them to the set of ICE samples
the learner considers in each round. The learning algorithm required in our framework can be any
ICE-learning algorithm that synthesizes invariants and contracts given counterexamples. Moreover,
when the hypotheses spaces of invariants and contracts is finite, our framework is guaranteed to
converge and verify the client modulo tested library contracts, provided they exist.
Contextual contracts. The second contribution of this paper is the study of a new form of
contracts that emerges particularly in the setting of verification modulo tested libraries. Consider
a client 𝐶 and a library 𝐿 that it utilizes. In traditional verification, contracts Π for 𝐿 are valid if
the methods in 𝐿 verify their contract when they are called in all possible states and all possible
inputs. However, since we are interested in verification primarily of the client, it is sufficient if
𝐿 satisfies the contracts Π, in the context of the client 𝐶. More precisely, the library is not called
in every possible state of object heap and input parameters—the client only calls it in particular
states. Hence, there is an implicit precondition that the overall program satisfies when calling library
functions. Under these preconditions, the contracts for the libraries could be made stronger, which
in turn can help prove the client correct. We call these contracts that hold in the context of the
client contextual contracts.
   For example, consider a library that has a class that maintains a datastructure for a set, with
methods to insert and delete elements, and a method to check membership. Now consider a client
𝐶 that only inserts positive integers into a set maintained by such a datatype, and then checks for
membership of a negative number, and asserts that this must return false. In this case, a contextual
contract for the membership method could state that it returns false for all negative numbers. Note
that this contract holds in the context of this client as the client only adds positive integers to the
container (and proves the assertion in the client correct), but does not hold in general. 1
   We propose the following verification modulo tested contextual library contracts problem: given
a client program 𝐶 using a library 𝐿, find a set of formal contracts Π for the library methods in 𝐿 at
each call site in 𝐶 such that (a) the client 𝐶 is proved correct assuming the contracts Π for 𝐿, and
(b) a predetermined test-generator with fixed resources is unable to find any tests for the program
with the client and the library methods that violate the contracts in Π.
   Our framework can cater to synthesizing contextual contracts by testing the contracts only in the
context of the client. We modify our framework so that the testing phase is performed not modularly
on the library, but on the entire program, involving the client and the library.
Learning Algorithms: Search, Contraint-solving and LLMs. As mentioned earlier, our frame-
work allows the use of any ICE learning algorithm, and we use a decision-tree learning called
HornICE [12].
   We can also use large language models (LLMs) in this context as ICE-learners. Note that we do
not assume LLMs to produce reliable annotations as we will always validate them (using formal
verification and testing). Given a client program, and only a description of the library, we can utilize
LLMs to propose contracts (and invariants for the client). When proposals are found to be incorrect
(either in verification of the client or testing of libraries), we can feed the counterexamples back to
the LLM and ask it to modify its proposal, turning it into an ICE learner. While, of course, there are
no guarantees that proposals would avoid the counterexamples or converge, the LLM can speculate
on contracts using the documentation, code, and semantics of natural language. For example, an
1 A contract that holds in all settings and proves the client correct does exist but is much more complex—we would need

preconditions that say that any number inserted into the set is positive, keep a class invariant that all elements stored in the
set are positive (which will require quantification or recursive definitions).


                                                               3
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


LLM easily predicts that isEmpty() should return false after calling insert() in a container class,
even with no access to library code.
  We also develop algorithms that combine LLMs with symbolic methods. In particular, we propose
an ICE-learning algorithm that extracts predicates from the LLM proposed contracts to use in a
symbolic learning algorithm to synthesize contracts that truly avoid counterexamples.
Limitations. Note that VMTLC with modular/contextual contracts can, of course, succeed on
incorrect programs, as library contracts are not verified, but only tested. In order to succeed,
spurious contracts would needed to be synthesized that pass testing, and inductive invariants for
the client found that prove the client under these library contracts. While modular contracts are
tested extensively in all possible contexts, contextual contracts are tested only in the context of the
client, and hence are more susceptible to being spurious. See Section 4.1 for a detailed discussion.
Evaluation. To evaluate our framework, we build a tool called Dualis that implements our
framework for verifying clients modulo tested library contracts. Our tool combines verification
engines that return counterexamples, test generators, and a variety of ICE learners. We evaluate our
proposed techniques on a suite of benchmarks drawn from open-source data structure libraries, most
beyond the power of automated verification today. We evaluate (a) the efficacy of our framework in
solving the VMTLC problem, for several choices of generalizing CHC solvers, including LLMs (b)
comparison of modular and contextual contracts, (c) whether synthesized contracts by the various
approaches are indeed valid, and (d) ablations that study the effectiveness of generalizing CHC
solvers and nongeneralizing ones.
   Our evaluation shows that our framework is effective on verifying clients modulo synthesized
library contracts, and holds promise to scale verification.

2   Illustrative Example
In this section we illustrate the VMTLC problem via an example. Consider the client program
shown in Fig. 1(a). The program uses a Set library to maintain a set of integers. It inserts a number
of non-negative integers into the set, and then removes them from the set while computing the
sum of their values. The programmer asserts that sum variable contains a non-negative value at
the end of the program. We would like to establish that the assertion is valid.
   In addition to the insert, remove, empty (and the implicit init constructor) methods, let us say
the Set library has a couple of “observer” methods size() and min() that take no arguments and
return integer values. We will also consider the method empty() to be an observer. The observer
methods size and min are meant to return the size and the minimum value stored in the set,
respectively, but our technique is agnostic to these semantics. We associate uninterpreted functions
empty (of type Set → Bool), and size and min (of type Set → Int) with the observer methods, to
abstractly represent the state of the data structure maintained by the library.
   Our goal is now to come up with annotations for the client program in the form of loop invariants
and method contracts, which constitute a valid Floyd-Hoare proof that the program satisfies its
assertion. There are a couple of caveats though. Firstly, the library method contracts must make
use of only the observer functions (instead of the actual data structure state maintained by the
library), apart from the formal parameters and return values of the method. The method contracts
may also refer to the auxiliary state after the invocation of the method, using primed versions of
the observer functions. For example, the contract for insert could be a predicate over the variables
o (representing the receiver object on which the method is invoked), empty(o), size(o), min(o),
empty ′ (o), size′ (o), and min′ (o) (representing the values returned by the observer functions in the
state pre and post the method invocation), and ival (the formal parameter to insert). The loop
invariant inv1 for the for-loop would be a predicate over the variables 𝑁 , 𝑖 and S (variables in scope

                                                   4
     Verification Modulo Tested Library Contracts


 1    i n t main ( ) {                                         void i n i t ( S e t t ) ; // Contract: empty ′ (o)
 2          Set S ;
                                                               void i n s e r t ( S e t t , i n t i v a l ) ;
 3          i n t N = nondet ( ) ;
                                                               // Contract: ((empty(o) ∨ min(o) ≥ 0) ∧ ival ≥
 4          f o r ( i n t i = 0 ; i < N ; i ++ ) {
                                                               0)) ⇒ min′ (o) ≥ 0
 5                  i n t v1 = nondet ( ) ;
 6                  i f ( v1 >= 0 )                            bool empty ( S e t t ) ;
 7                      S . i n s e r t ( v1 ) ;               // Contract: ret ≡ empty(o) ∧ empty ′ (o) ≡
 8          }                                                  empty(o)
 9          i n t sum = 0 ;                                    i n t remove ( S e t t ) ;
10          while ( ! S . empty ( ) ) {                        // Contract: (¬empty(o) ∧ min(o) ≥ 0) ⇒ (ret ≥
11              i n t v2 = S . remove ( ) ;                    0) ∧ (empty ′ (o) ∨ min′ (o) ≥ 0)
12              sum = sum + v2 ;
                                                               // Loop invariants:
13          }
                                                               inv1 : empty(S) ∨ min(S) ≥ 0
14          a s s e r t ( sum >= 0 ) ;
                                                               inv2 : sum ≥ 0 ∧ (empty(S) ∨ min(S) ≥ 0)
15    }

                                   (a)                                         (b)

     Fig. 1. (a) A client program that uses a Set library, and (b) Library methods along with contracts, and loop
     invariants, learnt by our approach.


     at the loop head), and likewise the loop invariant inv2 for the while-loop would be a predicate over
     𝑁 , S, and sum. The second caveat is that the method contracts need only pass the given tester—they
     need not be formally proved.
        For this program, the approach we describe in this paper essentially comes up with the adequate
     testable annotations (library method contracts and loop invariants) shown in Fig. 1(b). Here ret
     represents the return value of the methods empty and remove. The annotations are adequate to
     prove the assertion in the client, as well as pass the Tester.
        Finally, to illustrate the use of contextual contracts, consider the same client program of Fig. 1(a),
     but where the library does not provide the min observer method. There is clearly no adequate
     testable modular contract for the library methods using these observer methods. However, what we
     can say is that, in the context of the given client program, the call to remove() at Line 11 satisfies
     the contract “empty(o) ∨ ret ≥ 0”. This contextual contract can be tested by the Tester by simply
     executing the client program with different inputs and checking whether the call to remove() at
     Line 11 satisfies this contract. Our approach comes up with this contract and the other annotations
     below:
          init (Line 2) ↦→ empty ′ (o)      empty (Line 10) ↦→ ret ≡ empty(o) ∧ empty ′ (o) ≡ empty(o),
          insert (Line 7) ↦→ true           remove (Line 11) ↦→ empty(o) ∨ ret ≥ 0
          inv1 ↦→ true                      inv2 ↦→ sum ≥ 0
     which turns out to be adequate to prove the assertion in the client, and also pass the contextual
     Tester.

     3   The Verification Modulo Tested Library Contracts Problem
     In this section we formally define the main technical objects of study, namely the verification
     modulo tested library contracts (VMTLC) problem and the concept of contextual contracts. We
     begin with some preliminaries to develop the vocabulary for our definitions.

                                                           5
        Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


Classes and Objects. In this work we study the VMTLC problem in the domain of object-oriented
programs. We work with a client program 𝐶 (with a main method) that creates and manipulates
objects of classes that are part of a library. Let us consider a set of primitive sorts (mainly integers
and Booleans in this paper). We model a class 𝑐 using a designated sort 𝑂𝑐 for objects of that class.
We will use these to explicitly model manipulation of objects by methods. A class 𝑐 consists of a
set of methods {𝑓cons (𝑝 cons ), 𝑓1 (𝑜, 𝑝 1 ), . . . , 𝑓𝑛 (𝑜, 𝑝𝑛 )}, where 𝑓cons is a constructor method to create
objects, and 𝑓1, . . . , 𝑓𝑛 are methods on receiver object 𝑜 given as the first parameter (a method
call o.f(p) is modeled as calling 𝑓 (𝑜, 𝑝)). These methods in general have side effects, and return
a reference to an object in 𝑂𝑐 as well as a return value in a primitive sort. We don’t formalize
programming languages further as our problems are meant to work on real programming languages;
we assume that they come with a sound verification condition generator for verifying programs
with adequate annotations, and a test generator for testing programs against annotations.
Observer Methods and Annotations. We now define the syntax and semantics for annotations
(both invariants and contracts) that we consider in this work.
    Let us fix a first-order signature consisting of a set of sorts S as well as a set of relation symbols
R and function symbols (includes constant symbols) F . Function and relation symbols are also
equipped with a signature in the usual way: a function 𝑓 has a signature of the form (𝜏1 × 𝜏2 ×
· · · × 𝜏𝑛 ) → 𝜏 where 𝑛 is its arity and 𝜏𝑖 , 𝜏 ∈ S, and a relation symbol 𝑟 has a signature of the form
𝜂 1 × 𝜂 2 × · · · × 𝜂𝑚 where 𝑚 is its arity and 𝜂𝑖 ∈ S.
    Our annotations use a set of observer methods corresponding to a class which are pure, side-
effect-free, terminating functions on objects. These do not change the state of the class or of the
object, and are used to measure properties of an object. For example, in a stack class, a method
that returns the element stored on the top of the stack (without popping it) would be an observer
method. Another example is a method that returns the size of the stack. Observer methods can
be used to write rich annotations/specifications. For example, we could say that after popping an
element, the size of a stack object reduces by 1 (formally size′ (𝑜) = size(𝑜) − 1). Note that we treat
the receiver object as the first parameter for the method, and use primes to denote the value of the
observer method computed in the post-state2 .
    The annotations we consider are formulas in multi-sorted first-order logic over the above
vocabulary. We require well-formed formulas to only use primed observer methods on primed
objects, i.e., one cannot evaluate an observer method that computes over the heap in the post-state
on an object from the pre-state. We will typically focus on using quantifier-free formulas.
    Invariants for the client program are written not only using (as free variables) the variables in
scope, but also using observer methods applied to object variables in scope, and combinations using
the FO logic over the primitive types.
    The syntax for contracts is more involved. Rather than have preconditions and postconditions
for methods, we write contracts as postconditions that can relate pre- and post-states (in particular,
postconditions that hold upon certain preconditions holding can be expressed as pre ⇒ post).
Contracts for a library method 𝑚 are logical formulas involving (a) the receiver object variable 𝑜, (b)
the formal parameters 𝑝 for 𝑚 (which could involve objects), and (d) a variable ret for the returned
value. Contracts can use both primed and unprimed versions of observer methods. For example, a
contract for insert (𝑜, 𝑘) into a container object 𝑜, can be (size′ (𝑜) = size(𝑜) + 1) ∧ contains′ (𝑜, 𝑘)
where size and contains are observer methods. In our problem definitions and evaluation, we fix
particular precise logics for annotations. We model exceptions as special sentinel values to denote

2 The reason observer methods can be primed is because their computation depends on the heap. When the heap is modified,

the observer methods become logically distinct from what they were before the modification. This is a common modeling
choice in verification involving defined functions over heaps.


                                                           6
Verification Modulo Tested Library Contracts


error states and evaluate formulas over an error-aware semantics. This is similar to modeling
exceptions using Option-type return values.
   Observe here that invariants for the client can involve the client’s local variables, but may also
need to talk about the state of the object heap even though it is only accessible through the library
methods. The observer methods mediate this interface and provide a vocabulary that the client can
use to state invariants. Correspondingly the library methods must provide contracts in the same
vocabulary. For a formal treatment of modular annotations in OOP, see [3].
   We denote formulas with free variables 𝑝 and that use observer methods 𝑜𝑏𝑠 as 𝜑 [obs] (𝑝), and
when the observer methods are clear from context, as simply 𝜑 (𝑝).
Object-Oriented Programs and Verification Conditions. We consider an object-oriented client
program 𝑃 that utilizes a set of classes C and set of library methods L = {𝐿1, . . . , 𝐿𝑚 }. We assume
that 𝑃 has a set of methods including a main method 𝑀 (we call this part of the program the client
𝐶), apart from the library methods L. Our client programs can perform the usual computations
associated with objects, including creating new objects using constructors, and manipulate objects
using method calls of the class, with conditionals, iterations, and function calls to internal auxiliary
methods. We also assume that the library methods do not call the client code.
   Importantly, our client programs contain assertions. The verification problem we are interested in
involves showing that these assertions are valid assuming certain contracts for the library methods.
We capture this aspect of the problem by modeling the validity of the assertions with respect to
contracts as the validity of a verification condition (VC) 𝜑 in our logic described above. The VC 𝜑 is
stated over a set of free variables 𝑣 (modeling versioned variables for capturing basic blocks) as
well as formula meta-variables I = {𝐼 1, 𝐼 2, . . . , 𝐼𝑛 } and A = {𝐴1, 𝐴2, . . . , 𝐴𝑚 } corresponding to the
invariants for the client code and the contracts for the library methods, respectively. We refer to
client invariants in a broad sense, to include loop invariants and auxiliary method contracts. The
signature and vocabulary of the invariants and the library contracts are as described above.
   We note that using contracts that refer to observer methods/pure functions is standard. Assertion
frameworks established in the literature for Object-Oriented Languages like JML [22, 31] and
Spec#/Code Contracts [32] allow contracts using observer methods. In OO languages, encapsulation
naturally demands using observers to observe the internal state of objects.
   When proving the client correct, we can model observer methods as fields of objects that are kept
up to date across methods. Formally, we model them as uninterpreted functions that get updated
according to contracts. Multiple objects do not pose any issue, and the modeling works in general.
   However, we acknowledge that in cases where clients and library methods make changes to a
shared pointer-based heap (not common in OO programming), our current contract language needs
to be more expressive in order to be effective (e.g., include modifies sets to facilitate frame reasoning,
etc.) Although there is nothing that precludes our framework from handling such contracts, we
do not utilize them in this work as we study applications that embrace encapsulation. We leave
synthesizing such richer contracts clauses to future work.
   We denote the VC with its parameters by 𝜑 (𝑣, I, A). The verification objective with respect to
the client is to synthesize formulas for the predicates in I ∪ A (with the appropriate signature and
in the logic) such that the VC is valid.3 .
Test Generators. We use test generators to validate contracts for the library methods with
respect to the library implementation. We model a test generator formally as a deterministic
terminating oracle 𝑇 (𝑃, mode, 𝑁 , A;e RB) that takes in a program 𝑃 in the form of a client program
3 Verification conditions can be typically expressed as Constrained Horn Clauses [20, 33], and we will assume this form in

our techniques. However, note that the observer methods in 𝜑 are not to be synthesized, which is not formally allowed in
traditional formulations of CHCs. We show how we handle this when using CHC solvers later (see Section 5.2)


                                                            7
         Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


𝐶 and library 𝐿, a mode (“modular” or “contextual”), a library method 𝑁 , a set of contracts A           e=
              ′                             ′
{𝐴1 [𝑜𝑏𝑠, 𝑜𝑏𝑠 ] (𝑥 1 ), . . . , 𝐴𝑚 [𝑜𝑏𝑠, 𝑜𝑏𝑠 ] (𝑥 𝑚 )} for the library methods with observer methods 𝑜𝑏𝑠 and
  e                             e
free variables 𝑥 𝑖 over which the contracts are expressed, and a resource bound RB. We use RB
to model forced termination since a testing strategy might go on forever. In practice, since test
generators can be nondeterministic, we determinize them by fixing all random seeds.
   In the modular mode, the test generator does the following. It creates objects and manipulates
them using methods, with invented parameters, to find valid objects, and generates test inputs for
the method 𝑁 and executes the method. It looks for a violation of the contract for 𝑁 , by evaluating
the terms in the contract, and substituting the values in the formula. Specifically, it interprets
the variable o to be the receiver object, variables 𝑝 to be the values corresponding to the formal
parameters, and ret to be the return value of the method. Importantly, it interprets the observer
method symbols in 𝑜𝑏𝑠 to be the functions defined by the respective method definitions given in the
code. It also executes unprimed methods in the pre-state and their primed versions in the post-state.
It substitutes the computed values for all these terms in the contract for 𝑁 and evaluates whether
the contract holds. If any of them do not hold, the test generator raises a contract violation.
   In the contextual mode, the test generator essentially executes the client program 𝐶 with different
inputs it generates. Like in the modular case it checks for violations of the method contracts
whenever a library method is invoked in the client, and raises violations accordingly.
   In both modes, the test generator can either return OK to say that it was not able to find a
contract violation, or return a method name 𝑁 ′ along with a valuation of inputs to 𝑁 ′ , its return
value, and observer function outputs, that evidence the violation of the contract for the method.

Problem Statement
We are now ready to define the main problem of study for which we develop algorithms in Section 5.
   Definition 3.1 (Modular Contract Synthesis for Verification Modulo Tested Libraries). Fix classes
C, library L, a program 𝑃 with both client code 𝐶 and library code, with verification condition
𝜑 (𝑣, I, A), test generator 𝑇 , and resource bound RB. Fix also the signatures of the client invariants
I and method contracts A, as described above.
   Synthesize a set of formulas I  e corresponding to client invariants I over the appropriate variables,
as well as a set of contracts A     e corresponding to the library contracts A over the appropriate
variables such that:
    (1) the VC substituted with the definitions for the invariant and contract predicates is valid,
         i.e., 𝜑 (𝑣, I,
                     e A)
                        e is valid, and
    (2) the test generator 𝑇 (𝑃, modular, 𝑁 , A;e RB) returns OK for each library method 𝑁 .           □
   A set of invariants I
                       e and library contracts A
                                               e is said to verify a client modulo tested (modular)
library contracts (VMTLC-Mod) if they satisfy the two conditions in the above definition4 .

4   Contextual Contracts
We study a new notion of contracts that emerges in the setting of verification modulo tested library
contracts, which we call contextual contracts. Contextual contracts are essentially contracts for
library methods that are stated at each call-site in the client where library methods are called, with
potentially different contracts at each call site. The meaning of such contracts is that the summaries
4 Observe that the definition of the VMTLC-Mod synthesis problem is similar to SyGuS problems which utilize a syntactically

defined space of hypotheses, along with logical constraints involving the functions to be synthesized. In our case we want to
synthesize definitions for the I and A where the hypothesis space for each is the set of FOL formulas over the appropriate
variables, and our constraints are twofold, involving a verifier and a tester.


                                                             8
Verification Modulo Tested Library Contracts


they denote hold when methods are called by the given client at the respective call sites. Note that
these are not modular contracts in the classical sense in that they need not hold in arbitrary contexts.
More precisely, at each call site of the client, when the client makes a call to the library, it implicitly
ensures a more restrictive precondition on the states of the library as well as the parameters passed
to the method when the call is made, and the contextual contract captures more precise summaries
for such calls.
   We recall the illustrated example from Section 2. When a client inserts only nonnegative integers
into a container class, and later retrieves them and computes their sum, the client can assert that
this sum is always nonnegative. Proving this using classical contracts is certainly possible, but
the contracts will be more complex. If there is an observer method such as min, as discussed in
Section 2, then there are valid modular contracts coupled with stronger client invariants that can
prove correctness of the client.
   However, when observer methods such as min are missing, modular contracts can get much more
complex to state. In this example, we could define a logical predicate min, but such a definition on a
linked pointer-based container class would have to involve recursive definitions and more complex
logics such as separation logic, which make both verification (of the client) and testing extremely
hard, A contextual contract, on the other hand, is delightfully simple—it simply says that in the
context of the client, removal of any member from the set will be nonnegative, and helps us show
that the sum computed is nonnegative. This contract for remove is not true for all clients, of course.
   Note that modular contracts are contextual contracts as well, as contracts that hold in all contexts
hold for the client’s contexts. However, contextual contracts need not be modular, as the above
example shows.

Why are Contextual Contracts Simpler?
We now discuss precisely why contextual contracts
are simpler than classical contracts.
Let 𝐶 be a client that using a library 𝐿, where 𝐿
exposes classes. Note that there is a global heap 𝐻 of
objects of the library that is modified by the library
methods when they are called, and persist between
calls. The client 𝐶 has references to instances but
does not modify the heap directly. Assume we want
to prove a safety property of the client 𝐶.

The standard approach in formal verification is to establish:
      • An inductive invariant 𝐼𝑛𝑣𝐶 for the client that avoids the unsafe states of 𝐶. This invariant
        is expressed in terms of the variables of the client as well as properties of the object heap 𝐻
        maintained by the library that can be gleaned using observer methods.
      • A precondition 𝑃𝑟𝑒 for when 𝐶 makes calls to 𝐿. This is a predicate on both the parameters
        passed to 𝐿 as well as the state of the object heap 𝐻 at the time of the call expressed using
        observer methods.
      • A return condition 𝑅𝑒𝑡 that constrains the values returned by calls to methods of 𝐿
      • 𝑆𝑢𝑚𝑚 that captures the transformation of the object heap 𝐻 across method calls, expressed
        again using observer methods on the pre and post object heaps.
      • An inductive invariant 𝐼𝑛𝑣 𝐿 that is used to prove that 𝐿 does ensure 𝑅𝑒𝑡 and 𝑆𝑢𝑚𝑚 hold.
        This invariant can complex, involving the internal structure of the object heap, and may
        use aspects unobservable to the client.

                                                    9
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


   In formal verification, we would prove (1) 𝐶 maintains the invariant 𝐼𝑛𝑣𝐶 and guarantees 𝑃𝑟𝑒
at calls to 𝐿, assuming 𝑅𝑒𝑡 and 𝑆𝑢𝑚𝑚 hold, and (2) the library 𝐿, assuming 𝑃𝑟𝑒, maintains the
inductive invariant 𝐼𝑛𝑣 𝐿 , ensures return condition 𝑅𝑒𝑡, and ensures the summary 𝑆𝑢𝑚𝑚.
   In verification modulo tested modular library contracts, we dispense with 𝐼𝑛𝑣 𝐿 , as we are not
proving the library correct. We instead prove (1) above and test that 𝐿, assuming 𝑃𝑟𝑒, satisfies 𝑅𝑒𝑡
and summary 𝑆𝑢𝑚𝑚. Note that we need the annotations 𝐼𝑛𝑣𝐶 , 𝑃𝑟𝑒, 𝑅𝑒𝑡 and 𝑆𝑢𝑚𝑚.
   In verification modulo contextual contracts, we dispense with both 𝐼𝑛𝑣 𝐿 and 𝑃𝑟𝑒! We prove that
𝐶 maintains its invariant 𝐼𝑛𝑣𝐶 assuming 𝑅𝑒𝑡 and 𝑆𝑢𝑚𝑚 hold. And test that 𝐿’s contract in terms of
𝑅𝑒𝑡 and 𝑆𝑢𝑚𝑚 hold when tested in the context of the client 𝐶 (it need not hold when it is called
from arbitrary object heaps or arbitrary parameters). Note that we do not formalize 𝑃𝑟𝑒, as the
precondition is implicitly the set of all parameters and object heaps at which 𝐶 calls 𝐿.
   The advantage of using contextual contracts in the verification modulo testing setting is that
it can be much simpler than modular contracts, as we do not have to precisely delineate the
precondition 𝑃𝑟𝑒, and hence easier to synthesize. In fact, since 𝐶 is not proved to ensure 𝑃𝑟𝑒
formally, the verification task for the client is simpler, In particular, the return condition 𝑅𝑒𝑡, the
summary 𝑆𝑢𝑚𝑚, and the inductive invariant 𝐼𝑛𝑣𝐶 can potentially be simpler as well.

Formal Problem of Verification Modulo Tested Libraries with Contextual Contracts
We can now formally define the problem of verification modulo testing of libraries using contextual
contracts:
   Definition 4.1 (Contextual Contract Synthesis for Verification Modulo Tested Libraries). Fix classes
C, library L, a program 𝑃 with both client code (with main method 𝑀) and library code, verification
condition 𝜑 (𝑣, I, A), test generator 𝑇 , and resource bound RB. Fix also the client invariants I, and
method contracts A (containing a contract for each call-site in client code that makes a call to the
library). We assume the VC 𝜑 for the client is also in terms of these contextual method names.
   Synthesize a set of formulas Ie corresponding to the client invariants I over the appropriate vari-
                                    e corresponding to the library contracts A over the appropriate
ables, as well as a set of formulas A
variables, such that:
    (1) the VC substituted with the invariants and contracts 𝜑 (𝑣, I,e A)
                                                                        e is valid, and
    (2) the test generator 𝑇 (𝑃, contextual, 𝑀, A; RB) returns OK.
                                                 e                                                   □
  Note that in condition (2) above the method under test is the client itself (with entry point as
main method 𝑀 of client), i.e., we require that the library contracts hold when calls are reached via
the main method of the client. There are no individual “unit” testing requirements for each library
method (in contrast to verification modulo testing of modular library contracts; Definition 3.1).
This is the sense in which the contracts are contextual: they are only required to hold on inputs
and library states that can occur in a context of the client program’s calls to the library. Note that
we are still limited to having one contract per call site (independent of the call stack).

4.1   The Added Value of VMTLC with Contextual Contracts
The argument as to why VMTLC with modular contracts adds value to just testing alone is that it
must surely be hard to prove a wrong program correct by generating spurious contracts for libraries
that pass independent testing and provide inductive invariants that prove the client correct modulo
these contracts. Of course, there are programs where this can happen, as testing of contracts is
incomplete.
   Contextual contracts help prove more correct programs correct (as described above) but they
also can validate more incorrect programs. The reason is that there is no explicit precondition

                                                   10
Verification Modulo Tested Library Contracts


stated under which the library is tested independently, and the only tests of libraries occur in the
context of testing the entire program, with the client.
   For example, let’s assume that there is a rare event in the client that testing cannot reveal. An
example code for a rare event is:
                  int x:=0; while (*) { int v:= nondet[1,10]; x :=x+v }
with the rare event being say x = 1729 after this code. This rare event would be hard to find by fuzz
testing (or other forms of testing); for the sake of argument in this section, let us assume this is so.
   Now consider a client that manipulates a set— it first adds only positive numbers to the set,
except that it adds a negative number to the set when the rare event happens. The client then
removes the elements from the set, and asserts that each element is positive.
   This program is incorrect, and testing will not find an error. However, a spurious contextual
contract that says that removing elements from the set will always result in positive elements will
pass the tester that tests the client and the library together. And using this spurious contract, we
can prove the client correct.
   Note that in this case, the spurious contract will not pass as a modular contract, as testing a
modular contract allows the tester to add negative numbers, which will easily show the contract to
be incorrect. A modular contract that has an explicit precondition saying elements added are positive
will not work either as it would be impossible to prove that the client meets this precondition.
   Given the above, it is natural to wonder if VMTLC with contextual contracts adds any value to
testing. We do believe that spurious contextual contracts may occur more often than spurious
modular contracts, but posit that they do add value to just testing.
   Here is an example. Let foo be a function that has access to a static/global variable 𝑣 (initially 0).
For an input integer 𝑥, it returns 2 when 𝑥 = 𝑣 and increments 𝑣 by 3, and otherwise, returns 0.
Consider the program:
 x:= 0; while (*) { y:=nondet(); z:= foo(y); x:= x + z; }; assert (x != 1220);
   The above program is incorrect, but it would be hard for testing to find an error. However,
note that any contextual contract (or modular contract) for foo that allows the return value to
be 2 cannot help prove the program correct. Furthermore, testing will easily reject any contract
that doesn’t allow the return value to be 2, even when tested as the entire program (one of the
nondeterministic values that foo is called with needs to be 0, in some test case). Consequently,
VMTLC with contextual contracts (or modular contracts) will not prove this program correct. Also,
note that if foo instead always returned values that are a multiple of 3, contextual (and modular)
contracts exist that prove the program correct (with a loop invariant that 𝑥 is a multiple of 3).
   We hence believe that contextual contracts may also add value to testing, as it continues to be
the case that finding spurious contracts that enable inductive invariants of the client to prove it
correct will be hard to find in practice.

5   A Solution to the VMTLC Problem
In this section, we describe our solution to the VMTLC problem. We begin with an overview of our
algorithm, followed by a discussion of our design choices for input verification conditions and the
helper methods used in our algorithm, and finally present the algorithm.

5.1 Overview
Fig. 2 shows the schematic diagram of our general proposed technique. It takes as input a client
program that calls library methods (𝐶), as well as verification conditions generated for the client
with annotation and contract holes (𝐶𝐻𝐶 (𝐶)). Additionally, the observer methods of the library are
also passed as input (𝑂). These observer methods are used in the contracts of the library method.

                                                   11
        Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


                                                                          Client   Obs Meth                        Client Program 𝐶
                                                                        Program      Sig                                   +
                                                                       𝐶 + CHC(𝐶 )    𝑂                                Library 𝐿
          Generalizing CHC Solver
                                                       CHC(𝐶 )
                    Invs +                                +
                   Contracts                          Pos Exs 𝑃                                    Lib Contracts
      Constraint                   ICE                                                                                 Tester
                                                                         VMTLC Verifier
       Solver                     Learner
                     ICE                              Client Invs                                    Pos Exs
                     Exs                                   +
                                                     Lib Contracts

                                                                                    Verified

                                  Fig. 2. Schematic diagram of our proposed solution.


  Our technique then synthesizes contracts for the library methods and invariants for the client
program in a counterexample guided loop. In each iteration of the loop, contracts and invariants
are first synthesized by a generalizing CHC solver (details to follow in Section 5.3) such that the
verification conditions are valid. This is followed by testing of contracts: either the library methods
for modular contracts, or the client program for contextual contracts. If the testing fails, the test
cases that cause the failure are passed as positive examples to the generalizing CHC solver. In the
next iteration, the generalizing CHC solver learns contracts for methods (ensuring that the positive
examples are included), along with invariants. This loop continues until the solver synthesizes
contracts and invariants that verify the client, and where the contracts also pass the testing engine.

5.2   Constrained Horn Clauses as Verification Conditions
We assume a verification condition generator that works on the client program to produce verification
conditions in the form of constrained Horn clauses (CHCs). Our technique is agnostic to the
semantics of the programming language, the specification logics, frame reasoning, etc., as VC
generation into CHC constraints takes these into account, and our framework takes CHCs as input.
CHCs have become popular as a symbolic intermediate representations of correctness of programs,
and verification conditions for CHCs have been developed for several programming languages
and program reasoning methods have been developed for CHCs [13, 14, 19–21, 23, 24, 33, 43, 49].
A CHC is a first-order logic formula over a fixed set of uninterpreted relations, and a system of
CHCs is a finite conjunctions of such formulas. A solution to a CHC system maps uninterpreted
relations to predicates from a fixed logic. When a CHC system represents a program’s verification
conditions, a solution to the system is a proof of the program’s correctness.
   Formally, for a fixed set of sorts S, a set of relation symbols R, and function symbols F , a CHC
can be of one of the following forms:
                                                                                      
                                                       ∀®𝑥 0 . 𝜓 (𝑥®0 ) =⇒ 𝑟 0 (𝑥®0 )             (fact)
                                    Û                                                      
              ∀®
               𝑥 0, . . . , 𝑥®𝑘+1 .   𝑟𝑖 (𝑥®𝑖 ) ∧ 𝜓 (𝑥®0, . . . , 𝑥®𝑘+1 ) =⇒ 𝑟𝑘+1 (𝑥®𝑘+1 )   (inductive)
                                      0≤𝑖 ≤𝑘
                                           Û                                                   
                    ∀®
                     𝑥 0, . . . , 𝑥®𝑘 .        𝑟𝑖 (𝑥®𝑖 ) ∧ 𝜓 (𝑥®0, . . . , 𝑥®𝑘 ) =⇒ false                                    (query)
                                          0≤𝑖 ≤𝑘
where, for each 𝑖, 𝑟𝑖 is a relation in R of type 𝜂 1 ×𝜂 2 × · · · ×𝜂𝑚𝑟𝑖 , where 𝑚𝑟𝑖 is the arity of 𝑟𝑖 and each
𝜂𝑖 ∈ S. Further, 𝑥®𝑖 represents the vector of variables (𝑥 1, . . . , 𝑥𝑚𝑟𝑖 ), with each 𝑥𝑖 of sort 𝜂𝑖 . Also, 𝜓 ,
called a constraint, is a formula in conjunctive normal form without uninterpreted relations.

                                                                  12
Verification Modulo Tested Library Contracts



                                                                   init (S) ∧ 𝑖 = 0 =⇒ inv 1′ (𝑖, 𝑁 , S)          (𝜑𝐶1 )
                                                                         ′
               inv 1 (𝑖, 𝑁 , S) ∧ 𝑖 < 𝑁 ∧ v1 ≥ 0 ∧ insert (S, v1) ∧ 𝑖 = 𝑖 + 1 =⇒          inv 1′ (𝑖 ′, 𝑁 , S)     (𝜑𝐶2 )
                                         inv 1 (𝑖, 𝑁 , S) ∧ ¬(𝑖 < 𝑁 ) ∧ sum = 0 =⇒ inv 2 (𝑁 , S, sum)             (𝜑𝐶3 )
                                                                    ′
      inv 2 (𝑁 , S, sum) ∧ ¬empty(S) ∧ remove(S, v2) ∧ sum = sum + v2 =⇒                  inv 2′ (𝑁 , S, sum′ )   (𝜑𝐶4 )
                                    inv 2 (𝑁 , S, sum) ∧ empty(S) ∧ sum < 0 =⇒ false                              (𝜑𝐶5 )


                                   Fig. 3. CHCs for the client program from Fig. 1.


  For a given client program, S consists of primitive sorts (like boolean and integer) and desig-
nated sorts of classes used in the program (like Set or BinarySearchTree), R = {𝐼 1, 𝐼 2, . . . , 𝐼𝑛 } ∪
{𝐴1, 𝐴2, . . . , 𝐴𝑚 }, containing relations representing invariants and library method contracts, re-
spectively, and F consists of operations and constants used in the program. The CHCs then encode
the proof obligations of a Floyd-Hoare style proof, with constraints in them corresponding to
program statements. In CHCs, the relations 𝐼 1, 𝐼 2, . . . , 𝐼𝑛 will be over variables that are in scope, and
the relations 𝐴1, 𝐴2, . . . , 𝐴𝑚 will be over the called object, and arguments and return values of the
corresponding methods they are representing.
  Example 5.1. Consider the CHCs in Fig. 3, corresponding to a Floyd-Hoare proof of the client
program of Fig. 1(a). Here, R = {inv 1, inv 2 } ∪ {init, insert, empty, remove}, where inv 1 and inv 2 are
the loop invariants5 , init represents the constructor, and insert, empty and remove represent the class
methods insert, empty and remove, resp. Since variables of types int (variables 𝑁 , 𝑠𝑢𝑚, 𝑣1, 𝑣2),
and Set (variable S) are used in the program, S = {Z, Set}. Further, the signature of init will be
Set, as it initializes the object S, insert will be Set × Z, as it is called on the S object and takes an
int variable as input. Similarly, the signature of empty will be Set, and remove will be Set × Z. The
invariant relation inv 1 will have the signature Z × Z × Set, as the variables 𝑖, 𝑁 , S are in scope of
the loop, while inv 2 will have the signature Z × Set × Z, corresponding the variables 𝑁 , S, 𝑠𝑢𝑚.
These relations are used in the CHCs 𝜑𝐶1 to 𝜑𝐶5 , where CHCs 𝜑𝐶1 to 𝜑𝐶4 are of type inductive and
correspond to the initial and inductive conditions of the loops, while 𝜑𝐶5 is of type query.
    For a system of CHCs over R, a map of interpretations Sol assigns to each relation symbol 𝑟 ∈ R
an interpretation 𝜃 (𝑥 1, . . . , 𝑥𝑚𝑟 ), where 𝜃 is a formula in a fixed logic. We use a quantifier-free
fragment of a multi-sorted first-order logic of annotations (defined in Section 3). This logic will
have a finite set of observer methods and their primed versions as uninterpreted functions of fixed
sorts.
    For a CHC 𝜑𝐶 and a map Sol, we can obtain a formula 𝜑𝐶 (Sol) by replacing all the relations
𝑟𝑖 (𝑦1, . . . , 𝑦𝑚𝑟𝑖 ) in 𝜑𝐶 by Sol [𝑟𝑖 ] (𝑦1 /𝑥 1, . . . , 𝑦𝑚𝑟𝑖 /𝑥𝑚𝑟𝑖 ) 6 . If this formula is valid, then Sol is a solution
to 𝜑𝐶 and 𝜑𝐶 is said to be satisfiable. Sol is a solution to a system of CHCs if it is a solution to all the
CHCs in the system. If it is not a solution to a CHC 𝜑𝐶 , a counterexample to validity (a ground
formula in the logic of Sol) can be obtained. Such examples are classified as positive if 𝜑𝐶 is of
type fact, Horn implication if 𝜑𝐶 is of type inductive, and negative if 𝜑𝐶 is of type query.

5.3    Need for Generalizing CHC Solvers
Recall that in our setting the input 𝜑 is a system of CHCs over R = {𝐼 1, 𝐼 2, . . . , 𝐼𝑛 } ∪ {𝐴1, 𝐴2, . . . , 𝐴𝑚 },
which are relations representing the client program’s invariants and library method contracts,
5 inv ′ and inv ′ are the same relations with slightly different interpretations; details to follow soon.
      1         2
6 For primed relations like inv ′ , the interpretation Sol [inv ] is used, except that uninterpreted functions corresponding to

observer methods in Sol [inv ] are replaced by their primed versions.


                                                              13
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


respectively. The positive examples returned by the tester in each round in our framework can also
be encoded as CHC constraints (these constraints will be fact constraints where the relation on the
right side of the implication is a contract relation 𝐴𝑖 ).
   Our technique calls for a generalizing CHC solver to synthesize a solution to 𝜑, as opposed to an
arbitrary CHC solver. Note that the contracts 𝐴𝑖 are only constrained from below by the positive
counterexamples returned by the tester. An arbitrary CHC solver could choose to solve the CHC by
overfitting this set of positive examples (say by insisting that the 𝐴𝑖 ’s cover precisely the positive
counterexamples). This would cause repeated calls to the tester and cause divergence, where we
never find the right contracts. Hence we require that the CHC solver generalizes the library method
contracts 𝐴1, . . . , 𝐴𝑚 . One common way to generalize is to bias the search towards small logical
expressions for each 𝐴𝑖 in the annotation logic, which automatically forces generalization.

5.4   ICE Learners as Generalizing CHC Solvers
We use the data-driven learning framework called Implication Counterexample (ICE) learning [10,
12, 16, 17] as the basis of a generalizing CHC solver. Learners in this framework find a general
solution by learning from positive, Horn implication, and negative examples, which are counterex-
amples to the satisfaction of CHCs. At a high level, ICE learners operate in an incremental loop.
In each iteration, a candidate solution is learned using examples from previous iterations. This
candidate solution is then checked to see whether it satisfies all the CHCs. If not, counterexamples
to satisfaction are collected and used in subsequent iterations to refine the candidate solution.


 Algorithm 1: ICE-CHCSolver(𝜑, PosCex)
  Input: 𝜑 – system of CHCs for a client program over relations R = I ∪ A, where I and A
         represent program invariants and library method contracts respectively; PosCex – set
         of positive examples for relations in A
  Output: Sol (map from R to predicates) which is a solution to 𝜑
1 E ← PosCex, Sol𝑐𝑎𝑛𝑑 ← {𝑟 ↦→ true | 𝑟 ∈ R};
2 while exists 𝜑𝐶 such that 𝜑𝐶 (Sol𝑐𝑎𝑛𝑑 ) is not valid do
3    E ← E ∪ GetCex(𝜑𝐶 , Sol𝑐𝑎𝑛𝑑 );
4    Sol𝑐𝑎𝑛𝑑 ← ICELearner(E);
5 return ⟨Sol𝑐𝑎𝑛𝑑 , 𝑡𝑟𝑢𝑒⟩;




   Algorithm 1 provides a formal description of a generalizing CHC solver built on the ICE learner
framework. It takes as input the CHCs 𝜑 and positive examples PosCex from the test generator. The
algorithm first initializes the set of examples (E) with the input set of positive examples (line 1).
Subsequently, in each iteration of the loop, the algorithm checks whether there exists a CHC 𝜑𝐶 for
which the current candidate Sol𝑐𝑎𝑛𝑑 is not a solution (line 2). If such a 𝜑𝐶 is found, a counterexample
is generated (line 3). Recall that the counterexample is a ground formula in the logic of the solution.
It will be classified as a positive example if 𝜑𝐶 is of type fact, a Horn implication example if 𝜑𝐶
is inductive, and a negative example if query. A new candidate solution is then learned that is not
only consistent with the examples, but also generalizes the solution (line 4). This loop repeats till
Sol𝑐𝑎𝑛𝑑 becomes a solution to the system 𝜑.

  We now present different realizations of the learning algorithm that synthesize generalized
candidate solutions which are consistent with a given set of examples.

                                                   14
Verification Modulo Tested Library Contracts


5.4.1 HornICE An ICE learner, HornICE [12] uses a decision tree learning algorithm to synthesize
solutions, extending standard decision tree algorithms for positive/negative samples to work on
ICE samples. A candidate solution is synthesized by learning a decision tree for each relation, and
works in polynomial time. The decision tree is guaranteed to be consistent with the ICE samples.
The decision trees constructed in this way have base formulas from a fixed template (e.g. octagonal
constraints over variables). As a result, decision trees correspond to boolean combinations of these
base formulas. Also, the construction favors small decision trees by using heuristics such as entropy,
which often leads to generalized formulas.
5.4.2 Large Language Models (LLMs) Transformer-based neural networks realizing Large Language
Model (LLM) have recently been found to be useful in program verification tasks, such as invariant
and precondition synthesis [9, 26, 27, 47]. Furthermore, they have been trained on coding tasks [1,
46], many of which use data-structure libraries. Motivated by these, we use an LLM as an ICE
learner.
   Our algorithm interacts with the LLM through textual prompts (the prompt templates can be
found in Appendix C). The initial prompt includes the input client program (𝐶), its CHC encoding
(𝜑𝐶 ), and a textual description of the task (see C.1). The algorithm expects the LLM to return a
candidate solution to the formula variables in 𝜑, which includes invariants and library method
contracts. If the candidate is not a solution or subsequent testing fails, a repair prompt is generated,
which includes the examples, and sent to the LLM, expecting it to repair the solution (prompt
templates in C.3 and C.4).
5.4.3 Combination of HornICE and Large Language Models In this approach, initially the LLM is
queried to get atomic formulas (prompt template in C.5). These are passed to the HornICE learner
as a template. Subsequently, HornICE is used as the ICE learner. It now considers the normalized
atomic formulas as node attributes, in place of the fixed templates used previously, and learns
decision trees.

5.5   Test Generator
In our algorithm, the test generator takes as input library contracts present in the solution synthe-
sized by the learner and tests them against the library implementation. This step is necessary as a
solution of the CHC system can overly restrict the contracts of library methods. Our algorithm
expects the test generator to check such solutions by generating test cases and returning the failing
test cases as positive examples. In turn, the learner generalizes the contracts by using these positive
examples. For example, consider the solution to the CHCs in Fig. 3, which maps all the relations
to false (which vacuously satisfies all the CHCs). In this case, the test generator should produce
positive examples for library methods which violate the specification false as a method contract.
   A formal description of the test generator is presented in Algorithm 2. The algorithm takes
as input the client program 𝐶, the library 𝐿, the mode of verification (modular/contextual), the
library method 𝑁 to test (for use in modular mode), contracts for the library methods, and a testing
resource bound. The call to ConstructProgram constructs a program (TestProgram) which will
read its inputs from an input buffer Buf and test the appropriate method contracts. In the modular
mode, TestProgram creates library objects necessary to invoke the method 𝑁 , sets up the state of
the these objects by calling library methods on them (the operations to call and the arguments to
pass are determined by the input buffer Buf ). It then invokes method 𝑁 on the appropriate object
(once again with arguments determined by Buf ). Before and after this invocation, it records the
values of the observer methods on the pre/post state of the object, along with the arguments and
return value of 𝑁 , in val. Finally, it asserts the contract for 𝑁 (i.e. Sol(𝑁 )) with the values from val
plugged in. If the assertion fails it returns TestOk = false, along with the method name 𝑁 and val. If

                                                   15
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


 Algorithm 2: TestGenerator(𝐶, 𝐿, mode, 𝑁 , Sol, RB)
  Input: Client program 𝐶, library 𝐿, method under test 𝑁 , contracts Sol for methods in 𝐿,
         resource bound on testing RB
  Output: Result of testing TestOk, set of positive examples 𝑃
1 TestProgram ← ConstructProgram(𝐶, 𝐿, mode, 𝑁 , Sol);
2 while RB is not exhausted do
3     Buf ← InitBuf();
4     ⟨TestOk, 𝑁 ′, val⟩ ← Execute(TestProgram, Buf );
5     if ¬TestOk then return ⟨false, {(𝑁 ′, val)}⟩;
6 return ⟨true, ∅⟩;



the assertion passes it returns true. If the mode is contextual, TestProgram is essentially the client
program 𝐶 with instrumentation for each contextual method call, similar to the modular mode.
Then, in a loop, the test generator algorithm initializes Buf (line 3), and executes TestProgram on
it. If TestProgram returns an assertion failure, the corresponding method name 𝑁 ′ and valuation
val are returned. The loop continues until RB is exhausted. If no assertion violation is found in the
loop, the algorithm returns success (line 6).

5.6   Complete Algorithm

 Algorithm 3: VMTLC(𝐶, 𝐿, mode, 𝜑, RB)
  Input: Client program 𝐶, library 𝐿, Mode mode (modular/contextual), CHCs 𝜑 for 𝐶 over
         relations R = I ∪ A, test resources RB
  Output: Solution Sol to 𝜑, in the form of a map from R to predicates
1  PosCex ← ∅, TestOk ← false, CHCOk ← false;
2  while ¬(CHCOk ∧ TestOk) do
 3    ⟨Sol, CHCOk⟩ ← ICE-CHCSolver(𝜑, PosCex);
 4    if mode = contextual then
 5        ⟨TestOk, 𝑃⟩ ← TestGenerator(𝐶, 𝐿, contextual, −, Sol, RB);
 6        if ¬TestOk then PosCex ← PosCex ∪ 𝑃 ;
 7    else // modular mode, test each library method 𝑁 in Ł
 8        TestOk ← true ;
 9        foreach method 𝑁 in 𝐿 do
10            ⟨TestOk ′, 𝑃⟩ ← TestGenerator(𝐶, 𝐿, modular, 𝑁 , Sol, RB);
11            if ¬TestOk ′ then PosCex ← PosCex ∪ 𝑃 ;
12            TestOk ← TestOk ∧ TestOk ′ ;
13        end
14 return Sol;



  Algorithm 3 gives a formal description of our approach to find contracts in the verification
modulo testing setting. It takes as input a client program 𝐶, along with the library 𝐿, a string mode
representing the verification mode (contextual/modular), corresponding CHCs of the program (𝜑),
and resource constraints on the test generator (RB). The algorithm operates in a counterexample
guided synthesis loop until it finds a solution to 𝜑 (variable CHCOk is true) that also passes

                                                   16
Verification Modulo Tested Library Contracts


testing (variable TestOk is true). In the first iteration of the loop, a generalizing CHC solver (helper
method ICE-CHCSolver) synthesizes a map of interpretations (Sol, line 3) that is a solution to the
CHCs 𝜑. This is followed by testing, where the library contracts in Sol are tested. If the mode is
contextual, the contracts are tested through the client program 𝐶 (line 5). If the mode is modular, the
contracts for each library method 𝑁 are checked separately (line 10) via a test harness. Whenever
testing fails the corresponding valuations (𝑃) are added to the set of positive examples PosCex
(lines 6 and 11). In the subsequent iterations, ICE-CHCSolver will make sure that the solution it
synthesizes to 𝜑 also generalizes positive examples in PosCex. Algorithm 3 always terminates with
a solution if the following conditions are satisfied: 1) the logic of the CHC solutions is finite, 2) a
general solution exists within the logic, and 3) ICE-CHCSolver correctly classifies examples.

6   Implementation
We implement our framework (Algorithm 3) in a tool named Dualis, in Python. Dualis orchestrates
the communication between the learning algorithms and the constraint solvers in the framework.
In particular, our implementation offers the following ICE learners: (1) HornICE [12], a decision
tree learner, (2) an LLM-based ICE learner built using Gemini v2.5 Pro and appropriate prompts,
(c) and a combined HornICE+LLM learner that uses the decision tree learner for synthesizing
client invariants and library contracts using atomic formulas generated by Gemini v2.5 Pro. We
use Z3 [11] to check verification conditions for the client. The test generator is implemented using
the AFL++7 fuzzing framework.
   The HornICE learner synthesizes expressions in a grammar that is a boolean combination of
octogonal constraints over integer variables and booleans. The variables are input parameters
and values of observer functions. In the case of the combined learner, the LLM is asked for base
expressions which are incorporated into the grammar.
   To use AFL++ for testing, we create a test harness that (a) creates objects and manipulates them
using methods from the class as dictated by an input controlled by AFL++, and (b) calls the method
under test instrumented with the candidate contracts as runtime assertions. When a contract
violation is encountered, we get a counterexample. Note that the testing setup is different for
modular and contextual contracts; modular contracts are tested directly with the library methods
as the methods under test, and contextual contracts are tested via the client.
   We provide different prompts to the LLM for synthesizing modular and contextual contracts (see
Appendix C). The prompt contains (a) the client code, (b) signatures of library methods, (c) the CHCs
corresponding to the VC, (d) ICE counterexamples from the verifier and positive counterexamples
from the test engine, and (e) instructions for the LLM for the contract and invariant synthesis
problems, including the expected output format.

7   Evaluation
In this section we describe our benchmark suite and the research questions we study.

Benchmarks
Our benchmark suite consists of 43 C++ client programs that utilize various popular open-source
data structure libraries. These client programs are primarily adapted from unit tests into more
challenging clients for verification. We derive 19 benchmarks from Folly8 (libraries used in Face-
book), 9 from Abseil9 (libraries used in Google), and 1 from the Android source-code10 . Additionally,
7 https://github.com/AFLplusplus/AFLplusplus
8 https://github.com/facebook/folly
9 https://github.com/abseil/abseil-cpp/
10 https://cs.android.com/android/kernel/superproject



                                                        17
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


we incorporated 14 benchmarks from SV-COMP Java category [7], which already had client and
library implementations. We rewrite these benchmarks into C++. Overall, these benchmarks include
libraries with lines of code ranging from 100 to 3000, client programs with 2-6 library methods. 6
of our benchmarks are ∼3000 LoC. A detailed description of the suite can be found in Table 2 in
Appendix A.
   Our benchmark suite is beyond the scope of the state-of-the-art in full automated verification.
More precisely, we tried to verify our benchmarks using SeaHorn [20], and all but 7 of them failed to
verify or returned spurious counterexamples. The 7 benchmarks contained libraries on the smaller
side in our suite (< 200 LoC). In fact, even when given contracts for the library methods that would
prove the client correct, SeaHorn failed to verify.
   Our suite contains benchmarks that are challenging both in size and in the complexity of the
verification problem. For example, the FlatHashMap4 benchmark, has a client with ∼30 LoC and
a library with ∼3000 LoC. The library is adapted from similar classes found in both the Abseil
and Folly repositories, and the client is adapted from a test harness that captures a common
usage pattern of the data structure. The ProcessQueue benchmark is another interesting example,
adapted from SV-COMP and derived from a real-world scheduling application. The client (∼20 LoC)
utilizes a library (∼100 LoC) that implements a waiting process queue, tracking time-to-wake for
processes, returning those that are due. SeaHorn was not able to verify either of these benchmarks
automatically given more than an hour.

Research Questions
We study the following research questions:

RQ1: How effective are the proposed techniques at verifying clients modulo tested
library contracts, both modular and contextual contracts?
To answer this question we evaluate our proposed techniques on our benchmarks suite. We present
the detailed results of our evaluation in Table 1. We report the results grouped by the choice of ICE
learner: HornICE, LLM, or HornICE+LLM. We consider a benchmark to be solved by a technique
if it is able to generate contracts for libraries that pass the test generator, and the client is verified
to be correct using these contracts. We run the pure LLM-based pipeline thrice to account for
nondeterministic behavior of LLMs. We gave a timeout of 1000 seconds for the ICE learners to
synthesize a solution and AFL++ was provided with a timeout of 500 seconds, for each round they
are called. We ran our tool on an Intel(R) Xeon(R) W-2295 CPU @ 3.00 GHz with 256 GB RAM,
running Ubuntu 20.04.
    For modular contracts, out of 43 benchmarks, HornICE solved 19 benchmarks, HornICE+LLM
solved 25, and the LLM solution solved 38. For contextual contracts, HornICE solved 21, Hor-
nICE+LLM solved 28, and LLM solved 41 benchmarks. We find our framework fairly effective in
solving VMTLC, given that the benchmarks cannot be verified by state-of-the-art automated tools.
    Upon further analysis we observed that the failures of HornICE and HornICE+LLM could be
explained significantly by the absence of required predicates in their templates. For example, in the
benchmark TokenBucket a library method contract required an expression over three variables.
The pure LLM learner was able to synthesize the expression, but the expression was not covered
by the grammar for the HornICE learner (octagonal constraints over two variables), and it was not
part of the initial set of predicates given by the LLM for the HornICE+LLM learner. We leave the
improvement of the latter two learners to address these failure modes to future work.
    One failure mode we observed for VMTLC is the lack of sufficiently expressive observer methods.
For example, in the AtomicLinkedList2 benchmark, the client inserts keys into a linked list and
pops them in LIFO order. The assertion asks to show that the last element popped is the first one

                                                   18
Verification Modulo Tested Library Contracts

                                      HornICE                 HornICE+LLM                     LLM
          Benchmark                Modular   Contextual     Modular    Contextual       Modular   Contextual
                                 E+I T(m)    E+I T(m)     E+I T(m)     E+I T(m)       E+I T(m)    E+I T(m)
          AlternatingList      8+311 12.00 5+154 3.86    6+95 2.67    1+70 2.27       2+3 3.12    1+1 0.92
          AtomicHashMap1         2+3   TO    4+9    TO 5+199    TO     4+5    TO      5+7 10.68   2+4 11.38
          AtomicHashMap2        3+31   TO 5+212     TO   4+87   TO 6+117      TO      4+5 8.95    2+3 6.28
          AtomicHashMap3        2+16   TO 2+15      TO    2+7   TO     2+8    TO     8+10 20.77   1+1 1.83
          AtomicHashMap4       5+140   TO 3+16 1.35      5+65   TO    3+50 1.29       6+7 10.72   2+2 4.33
          AtomicHashMap5        4+58   TO 5+51 3.36      6+98   TO 17+124     TO      2+2 8.92    2+2 4.25
          AtomicLinkedList1    5+225   TO 4+134 2.49 4+125      TO    4+38 2.17       2+3 2.38    1+2 1.55
          AtomicLinkedList2     2+12   TO 2+12      TO    2+7   TO 3+183      TO    15+25   TO 15+21     TO
          BinaryHeap1           2+14   TO 2+14      TO    2+8   TO     2+8    TO    15+31   TO    7+9 16.97
          BinaryHeap2           3+47 4.31 4+14 2.23      3+43 4.96    4+13 2.20       1+1 1.58    2+2 3.18
          BinaryTree            5+88 6.90 4+48 2.21       3+7 6.72    3+28 1.30       2+1 3.12    3+5 2.25
          BlueWhiteList         5+42 3.36 4+27 2.20      6+57 4.69    4+12 2.14       1+1 0.88    1+1 1.15
          Calendar             5+199 5.58 6+139 4.96     5+32 3.60    1+20 3.23       1+1   1.3   1+1 1.80
          DLL_Circular         9+144 10.26 6+74 4.63     9+52 6.67    6+25 4.33       1+1 0.96    1+1 1.07
          DLL_Token            5+335   TO 3+157 5.08     2+18 14.90 6+150 5.70        1+1 1.37    3+3 2.60
          FlatHashMap1         7+182 13.52 5+131 3.49 10+58     TO    4+28 2.18       4+4 6.22    1+1 1.07
          FlatHashMap2        11+273   TO    2+6 3.43    9+54 16.33   5+61 3.28      9+11 16.37   1+1 0.83
          FlatHashMap3         8+290   TO 4+144 3.67 5+142      TO    4+35 2.24     15+19   TO    1+2 2.93
          FlatHashMap4          3+59   TO 3+55      4.3  6+93   TO    3+53    TO    15+22   TO    2+3 5.72
          FlatHashSet            2+5   TO 5+23      TO    2+5   TO    5+14    TO    13+20 43.75   3+5 4.91
          LruCache1              2+3   TO    3+6    TO 4+288 12.8      3+4    TO    15+18   TO 15+20     TO
          List (Max)            5+75 3.43 5+62 3.24 11+275 3.09       5+43 4.43       2+3 1.08    1+1 0.73
          List (Min)            5+76 3.38 2+20 0.68 11+738 5.35       2+19 0.69       1+1 0.63    1+1 0.63
          Multimap1            5+283   TO 14+40 2.79     5+33 4.13    3+33 1.32       2+2 1.45    1+1 0.70
          Multimap2             3+19   TO    3+6    TO 12+75    TO     3+4    TO      1+1 0.85    1+1 0.85
          Multiset1             3+36   TO    2+8    TO 4+196 5.14 4+128 3.63          1+1 0.72    1+1    0.7
          Multiset2             3+12   TO    3+6    TO 15+138   TO    4+22    TO      1+1 0.85    1+1 1.05
          NormalFilterQueue     3+67 2.39 4+131 2.64     3+23 2.30    4+26 2.17       2+2 2.01    1+1 1.32
          PriorityFilterQueue   3+67 2.48 3+95 1.59      4+45 4.46    7+61 2.21       2+2 2.45    1+1 2.24
          ProcessQueue          3+24   TO 5+211 3.00 4+127 4.88       5+95 2.62     13+23 40.97    1,2 1.87
          RedBlackTree           2+3   TO 4+20 1.56 11+57       TO    4+18 1.55       2+2 5.70    1+1 1.83
          SkipList1              2+3   TO 4+228 9.68     2+18   TO 5+244 3.22         2+3 7.07    3+3 4.38
          SkipList2             3+17 2.71 4+16 2.17       3+4 2.76     4+8 2.13       2+3 4.02    3+4 4.82
          SkipList3             3+11 2.72 4+14 2.13      3+11 2.71     4+8 2.13       2+2 4.23    2+2 3.50
          SkipList4             2+15   TO 3+84      TO    2+7   TO     2+7    TO      2+4 6.87    1+3 3.54
          SkipList5             3+21 2.74 4+34 2.17      3+20 2.30    4+16 2.16       3+3 6.72    2+2 3.77
          SkipList6             3+32   TO 4+198 7.20      3+5   TO    4+60 2.23       3+5 8.23    2+4 4.50
          SkipList7             4+52 4.70 4+26 2.15      3+19 3.40    4+13 2.13       2+5 3.67    3+5 7.62
          Stack                6+330 11.61 6+254 5.34 5+163 18.07     6+71 4.40       2+3 2.70    1+1 1.63
          StockOrder            3+72 1.54 5+90 3.36      3+38 1.51    4+49 2.13       2+6 5.93    1+1 0.95
          TokenBucket1         3+186 5.00 6+229 4.20     3+30 4.34    1+14 1.16       2+3 2.55    1+1 1.03
          TokenBucket2          3+84 2.90 4+97 1.94      3+50 2.15    7+45 2.18       2+2 2.33    1+1 1.80
          TokenBucket3         7+227   TO 4+126     TO   4+20 4.16    3+68 3.16       2+2 2.18    1+1 1.62
Table 1. Results of Dualis using different learners. Columns represent: benchmark name (Benchmark), and
for each learner’s contextual and modular approach: the sum of iterations (E+I) and execution time in minutes
(Time). The ‘E’ value represents the total iterations between learner and test generator (i.e. external loop in
Algorithm 3), and ‘I’ represents the total iterations the learner took (i.e. loop of Algorithm 1). For the LLM
learner, we report the maximum iteration counts over two runs, or the counts from the single successful run
if only one completed. Entries for benchmarks with TO in the ‘T(m)’ represent a time out, where the entry in
‘E+I’ column is the number of iterations completed before time out.




that was inserted. This can of course be established easily using an observer method that tracks the
last element in the list, but there was no such method provided by the library. Consequently, our
tool found no modular or contextual contracts that verified the client. We leave the exploration of
synthesizing observer methods to future work.

                                                         19
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


   A small mutant study: We study the performance of our framework in rejecting mutants of
our benchmark programs that are incorrect but pass testing. We systematically create a class of
complex incorrect mutants that evade testing (see Appendix A for details). We do this because our
clients formulate rich functional specifications that depend on the libraries, which results in simple
mutants generated by off-the-shelf mutation generators being found incorrect by the tester.
   We create 30 mutants by applying 2 intentionally unsafe mutation templates on 15 benchmarks
that were previously VMTLC-verified using contextual or modular contract synthesis. These tem-
plates modify the client by introducing a probabilistically rare execution path inside the program’s
non-deterministic loop. When triggered, this rare path injects unexpected values (such as inserting
a negative number when the client asserts that all elements are positive) altering the local or library
state and eventually driving the program to an assertion violation. We observe that the tester is
not able to find the bug in any of them. Using the pure LLM Learner, we observe that VMTLC
with modular contracts does not prove any of them, i.e., rejects them as expected. VMTLC with
contextual contracts verifies 11/30 benchmarks, synthesizing spurious contracts that were not
caught by testing due to hard-to-reach paths. See discussion in Section 4.1 on why we expect
contextual contracts to be more likely to be spurious than modular ones. The buggy programs
obtained by our mutations are not very natural/realistic, and this study should not be taken as a
comprehensive evaluation of VMTLC on incorrect programs. Our findings suggest, however, that
VMTLC fails on many incorrect programs that testing is unable to find fault with (see Section 4.1).

RQ2: Are contextual contracts simpler than modular contracts, and are they easier to
synthesize?
Synthesizing contextual contracts was indeed much more effective (i.e., more benchmarks solved)
than synthesizing modular contracts to establish VMTLC. All techniques took less time to synthesize
contextual contracts. A manual inspection revealed that the synthesized contextual contracts were
consistently smaller and less complex than their modular counterparts across all benchmarks.

RQ3: Are the synthesized library method contracts valid?
Determining the accuracy of synthesized contracts automatically is a nontrivial problem. One can
try to ascertain their correctness using a program verification engine, but our benchmarks cannot
be proved using such engines (we tried using SeaHorn [20] and it failed, as mentioned earlier). It is
in fact this hardness that motivated us to propose the VMTLC problem in the first place!
   We first manually vetted all contracts generated by all learners to establish a verified baseline.
However, due to the inherent non-determinism of LLMs, subsequent runs might yield syntactically
different contracts. To account for this variance, we executed the LLM pipeline two additional
times. For these subsequent runs, we utilized a constraint solver to verify whether the newly
synthesized contracts were logically implied by our manually vetted baseline. Contracts satisfying
this implication were automatically deemed correct, while any that did not were vetted manually.
Our examination found that all synthesized contextual and modular contracts using all learners
are correct.
   The level of guarantee that VMTLC contracts provide is influenced by the quality of the test
generator. We therefore investigate the robustness of our results in two ways. First, we check all
the final specifications generated by our tool (across learner variations) against the test generator
(AFL++) for an additional 30 minutes after each run. We found no violations of any synthesized
specifications. Second, we report on the quality of tests using standard fuzzing metrics tracked by
AFL++. On average, each of the final contracts were tested against 34 test cases (after AFL++’s
removal of cases it deems redundant). The average bitmap coverage, defined as the percentage of
edges exercised in the test object, was 50%, indicating substantial exploration of program behaviors.

                                                   20
Verification Modulo Tested Library Contracts


Finally, the stability metric was 100%, meaning that executions were fully deterministic and the
generated tests were reproducible across runs.

RQ4: How important is it to use a generalizing CHC solver to solve VMTLC?
As argued in the introduction, our VMTCL framework is best served by a generalizing CHC engine,
and the learners we implement are generalizing. To evaluate how a non-generalizing CHC solver
would fare, we replaced the CHC solver in our tool with CVC5 [6]. With CVC5 as the solver, the
tool produced only 10 modular contracts and 15 contextual contracts on our benchmarks, showing
a significant reduction in succeeding at VMTLC compared to learning-based CHC solvers.

8   Related Work
   Data-driven inference of library preconditions and invariants. Several works consider the problem
of synthesizing testable preconditions for library methods w.r.t. a postcondition [4, 5, 18, 39, 44]. In
particular [4, 5] synthesize weakest preconditions (w.r.t. not causing exceptions) and a strongest
post-condition corresponding to this precondition, in a similar setting to ours, where the conditions
are phrased in terms of observer methods of the library. However, these techniques are not directly
applicable in our setting as the client program may typically need a stronger precondition and
a stronger postcondition to prove its assertions. [35] infers data-structure invariants that are
sufficient to prove a given specification for a library module. The candidate invariants are tested
for inductiveness and sufficiency w.r.t. the specification. In contrast, we only have access to the
data structure via the observer methods, and we have a client that needs to be formally proved.
   Data-driven inference of library specifications. Zhou et al. [48] look at a closely related problem,
where they synthesize contracts for library methods used by a client functional program, using
observer methods (or what they call “method predicates”), that are adequate to both prove a property
of the client and pass a tester. The main technique they use is an adaptation of multi-abduction [2] to
a setting of richer types. However, there are a couple of crucial differences between their setting and
ours. Firstly, they do not infer inductive invariants for recursive client programs: the user is required
to supply these along with the property assertion. As a consequence, in the resulting VCs the
only unknown predicates to be synthesized are the library method contracts, making the problem
amenable to abduction-based techniques. In contrast, in our setting we need to synthesize loop
invariants in addition to the library method contracts. In our experience, abduction-based techniques
in this setting (for example [42]) don’t perform well on this problem. Not having to synthesize loop
invariants also means that data-driven approaches in the functional setting can get by with just
positive and negative examples, while in our setting we need to handle Horn-implication examples.
Finally, in contrast to the functional setting, reasoning about heap-manipulating programs and
libraries with persistent state is harder and requires more sophisticated program logics.
   Satisfiability/Synthesis modulo oracles. The tester in our setting can be viewed as an oracle that
is part of the synthesis specification. Such oracle-based synthesis has been considered in other
work (e.g. [41]). However it is not clear if these techniques generalize the examples given by the
oracle. [38, 41] consider the related problem where given a constraint with unknown black-box
functions (whose implementation alone is available) one tries to find a satisfying assignment to
free variables in the formula that is consistent with the behaviour of the black-box functions.
While our problem does not exactly fit in this setting, these techniques could be used to tackle
the complementary problem of falsifying the assertions in the client program in a way that is
consistent with the library method implementations. Extending this line of work [37] tries to prove
F* programs correct modulo contracts for library methods which are tested for consistency with
the library implementation, while [30] learns almost-correct invariants for loops containing opaque

                                                   21
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


calls to library functions. In contrast to our setting, the contracts are not about stateful methods,
and are either supplied by the user or not synthesized at all.
   Using LLMs for synthesizing invariants. Several researchers have explored the use of LLMs for
reasoning about program verification tasks like precondition and loop invariant synthesis [9, 25–
27, 36, 40, 47], demonstrating their usefulness in coming up with candidate specifications, and
their performance being comparable to state-of-the-art symbolic techniques when combined with
traditional techniques like static analysis, solvers, and fuzzing. Our work explores their use in
synthesizing library specifications and in constructing an effective generalizing CHC Solver.
   Assume-Guarantee Testing. VMTLC has similarities to assume-guarantee testing [8], which
proposes decomposing global specifications to modular specifications, in order to have more
effective unit testing and predictive testing. However, our work aims for synthesizing modular
specifications and have some components (the client) verified while others are only tested.

9   Conclusions
We have presented a significant advance in the problem of verification of clients using synthesized
contracts for libraries, where libraries are only tested for validity. In particular, in this work we have
developed a general and novel framework that utilizes generalizing CHC solvers, and techniques
for realizing such solvers using ICE-learning algorithms. We have proposed and evaluated our
framework using several ICE learning algorithms ranging from those that learn decision-trees,
those that use LLMs, and their combinations Our evaluation shows that our technique shows
promise in effectively solving verification modulo tested library contracts, in settings where clients
are small and libraries are large, and where current automated techniques fail.
   Verification modulo testing library contracts presents a new point in the design space for
automated verification—to get scalability to larger code bases we give up verification guarantees
for parts of the code. A natural question that arises is: how valuable is this partial verification given
that contracts for libraries are tested, but not verified? First, if synthesized contracts for libraries
happen to be valid, there is clear value in the approach, as we have formally verified the client.
Consequently, it is very important to have effective testing engines to test contracts. As borne
out in our evaluation, an effective testing strategy practically eliminates invalid contracts, though
not provably so. We believe that the chances that the synthesizer comes up with invalid contracts
that pass the tester as well as simultaneously happen to prove a nontrivial client program correct
would be rare. However, much larger scale experiments are needed to validate this hypothesis in
practical contexts. We believe our results show that VMTLC has the potential to make automated
verification significantly more applicable to larger programs than the current state of the art.
   There are several future directions to consider. First, it would be interesting to evaluate what the
guarantee of verification modulo tested libraries brings over simply testing a program, in practice.
An evaluation on a large corpus of programs, in a particular context, as to how many correct
programs are VMTLC verifiable, and also how many wrong programs are rejected by the VMTLC
framework but not by testing, would be interesting.
   On the technical front, we have primarily explored verification of clients for simple assertions.
It would be interesting to extend our framework to more complex logics, such as clients that
manipulate their own heaps (in addition to heaps maintained by libraries), and handle specification
logics for clients that involve heaps. The verification conditions may not lie in decidable logics
unlike the setting of this paper, and the ability to generate counterexamples may be more limited.
   Finally, contextual contracts that stem from our work seem interesting even under non-automated
settings, where verification engineers prove clients using human written annotations, but with
contextual contracts only tested. This is an appealing idea that is worth exploring further.

                                                   22
Verification Modulo Tested Library Contracts


Acknowledgments: This work was supported in part by a research grant from Amazon.




                                               23
         Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


Data-Availability Statement
The artifact supporting this paper, which includes the implementation of our tool Dualis, the
complete suite of benchmarks, and the evaluation scripts required to reproduce the experimental
results presented in Section 7, is publicly available. To ensure long-term archival, and reproducing
the results of this article, the artifact has been packaged and published on Zenodo at https://doi.
org/10.5281/zenodo.19519743. For building upon the framework, the public repository is hosted on
GitHub at https://github.com/omar826/Dualis-VMTLC.


References
 [1] Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida,
     Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al. 2023. GPT-4 Technical Report. arXiv preprint arXiv:2303.08774
     (2023).
 [2] Aws Albarghouthi, Isil Dillig, and Arie Gurfinkel. 2016. Maximal specification synthesis. In Proc. 43rd Annual ACM
     SIGPLAN-SIGACT Symp. Principles of Programming Languages (POPL 2016), St. Petersburg, USA, January 20-22, 2016.
     ACM, 789–801.
 [3] Krzysztof R. Apt and Ernst-Rüdiger Olderog. 2019. Fifty years of Hoare’s logic, Chapter 9. Form. Asp. Comput. 31, 6
     (2019).
 [4] Angello Astorga, P. Madhusudan, Shambwaditya Saha, Shiyu Wang, and Tao Xie. 2019. Learning stateful preconditions
     modulo a test generator (PLDI 2019). ACM, New York, NY, USA, 775–787.
 [5] Angello Astorga, Shambwaditya Saha, Ahmad Dinkins, Felicia Wang, P. Madhusudan, and Tao Xie. 2021. Synthesizing
     contracts correct modulo a test generator. Proc. ACM Program. Lang. 5, OOPSLA, Article 104 (Oct. 2021), 27 pages.
 [6] Haniel Barbosa, Clark W. Barrett, Martin Brain, Gereon Kremer, Hanna Lachnitt, Makai Mann, Abdalrhman Mohamed,
     Mudathir Mohamed, Aina Niemetz, Andres Nötzli, Alex Ozdemir, Mathias Preiner, Andrew Reynolds, Ying Sheng,
     Cesare Tinelli, and Yoni Zohar. 2022. cvc5: A Versatile and Industrial-Strength SMT Solver. In Proc. 28th Intl. Conf.
     Tools and Algorithms for the Construction and Analysis of Systems (TACAS 2022), Munich, Germany, April 2-7, 2022
     (LNCS, Vol. 13243). Springer, 415–442.
 [7] Dirk Beyer and Jan Strejček. 2025. Improvements in software verification and witness validation: SV-COMP 2025. In
     International Conference on Tools and Algorithms for the Construction and Analysis of Systems. Springer, 151–186.
 [8] Colin Blundell, Dimitra Giannakopoulou, and Corina S. Pasareanu. 2006. Assume-Guarantee Testing. ACM SIGSOFT
     Softw. Eng. Notes 31, 2 (2006).
 [9] Weining Cao, Guangyuan Wu, Tangzhi Xu, Yuan Yao, Hengfeng Wei, Taolue Chen, and Xiaoxing Ma. 2025. Clause2Inv:
     A Generate-Combine-Check Framework for Loop Invariant Inference. Proc. ACM on Software Engineering 2, ISSTA
     (2025), 1009–1030.
[10] Adrien Champion, Tomoya Chiba, Naoki Kobayashi, and Ryosuke Sato. 2018. ICE-Based Refinement Type Discovery
     for Higher-Order Functional Programs. In TACAS, Part I (LNCS, Vol. 10805). Springer, 365–384.
[11] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT Solver. In Proc. 14th Intl. Conf. Tools and Algorithms
     for the Construction and Analysis of Systems (TACAS 2008) (Budapest, Hungary). Springer-Verlag, Berlin, Heidelberg,
     337–340.
[12] P. Ezudheen, Daniel Neider, Deepak D’Souza, Pranav Garg, and P. Madhusudan. 2018. Horn-ICE learning for
     synthesizing invariants and contracts. PACMPL 2, OOPSLA (2018), 131:1–131:25.
[13] Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. 2018. Solving Constrained Horn Clauses
     Using Syntax and Data. In FMCAD. IEEE, 170–178.
[14] Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. 2019. Quantified Invariants via Syntax-
     Guided Synthesis. In CAV, Part I (LNCS, Vol. 11561). Springer, 259–277.
[15] Cormac Flanagan and K. Rustan M. Leino. 2001. Houdini, an Annotation Assistant for ESC/Java. In Proc. Intl. Symp.
     Formal Methods Europe (FME ’01). Springer-Verlag, 500–517.
[16] Pranav Garg, Christof Löding, P. Madhusudan, and Daniel Neider. 2014. ICE: A Robust Framework for Learning
     Invariants. In Proc. 26th International Conference on Computer Aided Verification CAV 2014, Vienna, Austria, 2014. (LNCS,
     Vol. 8559), Armin Biere and Roderick Bloem (Eds.). Springer, 69–87.
[17] Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. 2016. Learning invariants using decision trees and
     implication counterexamples. In Proc. 43rd ACM SIGPLAN-SIGACT Symp. Principles of Programming Languages (POPL
     2016), St. Petersburg, USA, 2016, Rastislav Bodík and Rupak Majumdar (Eds.). ACM, 499–512.
[18] Timon Gehr, Dimitar Dimitrov, and Martin T. Vechev. 2015. Learning Commutativity Specifications. In Proc. 27th Intl.
     Conf. Computer Aided Verification (CAV 2015), San Francisco, USA, July 18-24, 2015 (LNCS, Vol. 9206). Springer, 307–323.


                                                             24
Verification Modulo Tested Library Contracts


[19] Sergey Grebenshchikov, Nuno P. Lopes, Corneliu Popeea, and Andrey Rybalchenko. 2012. Synthesizing software
     verifiers from proof rules. In PLDI. ACM, 405–416.
[20] Arie Gurfinkel, Temesghen Kahsai, Anvesh Komuravelli, and Jorge A. Navas. 2015. The SeaHorn Verification Frame-
     work. In Proc. 27th Intl. Conf. Computer Aided Verification (CAV 2015), San Francisco, USA, July 18-24, 2015. Springer,
     343–361.
[21] Hossein Hojjat and Philipp Rümmer. 2018. The ELDARICA Horn Solver. In FMCAD. IEEE, 158–164.
[22] Bart Jacobs and Erik Poll. 2001. A Logic for the Java Modeling Language JML. In Proc. 4th International Conference on
     Fundamental Approaches to Software Engineering (FASE ’01). Springer-Verlag, Berlin, Heidelberg, 284–299.
[23] Temesghen Kahsai, Rody Kersten, Philipp Rümmer, and Martin Schäf. 2017. Quantified Heap Invariants for Object-
     Oriented Programs. In LPAR (EPiC Series in Computing, Vol. 46). EasyChair, 368–384.
[24] Temesghen Kahsai, Philipp Rümmer, Huascar Sanchez, and Martin Schäf. 2016. JayHorn: A Framework for Verifying
     Java programs. In CAV, Part I (LNCS, Vol. 9779). Springer, 352–358.
[25] Adharsh Kamath, Nausheen Mohammed, Aditya Senthilnathan, Saikat Chakraborty, Pantazis Deligiannis, Shuvendu K.
     Lahiri, Akash Lal, Aseem Rastogi, Subhajit Roy, and Rahul Sharma. 2024. Leveraging LLMs for Program Verification.
     In Proc. Formal Methods in Computer-Aided Design (FMCAD 2024), Prague, Czech Republic, October 15-18, 2024, Nina
     Narodytska and Philipp Rümmer (Eds.). IEEE, 107–118.
[26] Adharsh Kamath, Aditya Senthilnathan, Saikat Chakraborty, Pantazis Deligiannis, Shuvendu K Lahiri, Akash Lal,
     Aseem Rastogi, Subhajit Roy, and Rahul Sharma. 2023. Finding inductive loop invariants using large language models.
     arXiv preprint arXiv:2311.07948 (2023).
[27] Daragh King, Vasileios Koutavas, and Laura Kovács. 2025. Llm-Based Generation of Weakest Preconditions and Precise
     Array Invariants. In Proc. 13th IEEE/ACM Intl. Conf. Formal Methods in Software Engineering (FormaliSE). IEEE, 1–5.
[28] Anvesh Komuravelli, Nikolaj Bjørner, Arie Gurfinkel, and Kenneth L. McMillan. 2015. Compositional verification of
     procedural programs using horn clauses over integers and arrays. In Proc. 15th Conf. Formal Methods in Computer-Aided
     Design (Austin, Texas) (FMCAD ’15). FMCAD Inc, Austin, Texas, 89–96.
[29] Anvesh Komuravelli, Arie Gurfinkel, and Sagar Chaki. 2014. SMT-Based Model Checking for Recursive Programs. In
     Proc. 26th Intl. Conf. Computer Aided Verification (CAV 2014), Vienna, Austria, July 18-22, 2014. Springer, 17–34.
[30] Sumit Lahiri and Subhajit Roy. 2022. Almost correct invariants: synthesizing inductive invariants by fuzzing proofs.
     In Proc. 31st ACM SIGSOFT Intl. Symp. on Software Testing and Analysis (ISSTA 2022), South Korea, July 18 - 22, 2022,
     Sukyoung Ryu and Yannis Smaragdakis (Eds.). ACM, 352–364.
[31] Gary T. Leavens. 2007. Tutorial on JML, the Java Modeling Language. In Proc. 22nd IEEE/ACM Intl. Conf. Automated
     Software Engineering (ASE 2007) (Atlanta, Georgia, USA). ACM, New York, NY, USA, 573.
[32] Francesco Logozzo. 2013. Practical specification and verification with code contracts. Ada Lett. 33, 3 (Nov. 2013), 7–8.
     https://doi.org/10.1145/2658982.2534188
[33] Yusuke Matsushita, Takeshi Tsukada, and Naoki Kobayashi. 2020. RustHorn: CHC-Based Verification for Rust Programs.
     In Programming Languages and Systems, Peter Müller (Ed.). Springer International Publishing, Cham, 484–514.
[34] Kenneth L. McMillan. 2003. Interpolation and SAT-Based Model Checking. In Proc. 15th Intl. Conf. Computer Aided
     Verification (CAV 2003), Boulder, USA, July 8-12, 2003 (LNCS, Vol. 2725), Warren A. Hunt Jr. and Fabio Somenzi (Eds.).
     Springer, 1–13.
[35] Anders Miltner, Saswat Padhi, Todd D. Millstein, and David Walker. 2020. Data-driven inference of representation
     invariants. In Proc. 41st ACM SIGPLAN Intl, Conf. Programming Language Design and Implementation (PLDI 2020),
     London, UK, June 15-20, 2020. ACM, 1–15.
[36] Nausheen Mohammed, Akash Lal, Aseem Rastogi, Rahul Sharma, and Subhajit Roy. 2025. LLM Assistance for Memory
     Safety. In 47th IEEE/ACM International Conference on Software Engineering, ICSE 2025, Ottawa, ON, Canada, April 26 -
     May 6, 2025. IEEE, 1717–1728.
[37] Sujit Kumar Muduli, Rohan Ravikumar Padulkar, and Subhajit Roy. 2024. Interactive Theorem Proving Modulo
     Fuzzing. In Proc. 36th Intl. Conf. Computer Aided Verification (CAV 2024), Montreal, QC, Canada, July 24-27, 2024 (LNCS,
     Vol. 14681), Arie Gurfinkel and Vijay Ganesh (Eds.). Springer, 480–493.
[38] Sujit Kumar Muduli and Subhajit Roy. 2022. Satisfiability modulo fuzzing: a synergistic combination of SMT solving
     and fuzzing. Proc. ACM Program. Lang. 6, OOPSLA2 (2022), 1236–1263.
[39] Saswat Padhi, Rahul Sharma, and Todd D. Millstein. 2016. Data-driven precondition inference with learned features. In
     Proc. 37th ACM SIGPLAN Conference on Programming Language Design and Implementation (PLDI 2016), Santa Barbara,
     USA, June 13-17, 2016, Chandra Krintz and Emery D. Berger (Eds.). ACM, 42–56.
[40] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023. Can Large Language Models Reason
     about Program Invariants?. In International Conference on Machine Learning, ICML 2023, 23-29 July 2023, Honolulu,
     Hawaii, USA (Proc. Machine Learning Research, Vol. 202), Andreas Krause, Emma Brunskill, Kyunghyun Cho, Barbara
     Engelhardt, Sivan Sabato, and Jonathan Scarlett (Eds.). PMLR, 27496–27520.



                                                             25
        Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


[41] Elizabeth Polgreen, Andrew Reynolds, and Sanjit A. Seshia. 2022. Satisfiability and Synthesis Modulo Oracles. In Proc.
     23rd Intl. Conf. Verification, Model Checking, and Abstract Interpretation (VMCAI 2022), Philadelphia, USA, January
     16-18, 2022 (LNCS, Vol. 13182). Springer, 263–284.
[42] Sumanth Prabhu, Grigory Fedyukovich, Kumar Madhukar, and Deepak D’Souza. 2021. Specification Synthesis with
     Constrained Horn Clauses. In PLDI. ACM, 1203–1217.
[43] Sumanth Prabhu, Kumar Madhukar, and R Venkatesh. 2018. Efficiently learning safety proofs from appearance as well
     as behaviours. In SAS (LNCS, Vol. 11002). Springer, 326–343.
[44] Sriram Sankaranarayanan, Swarat Chaudhuri, Franjo Ivancic, and Aarti Gupta. 2008. Dynamic inference of likely data
     preconditions over predicates by tree learning. In Proc. ACM/SIGSOFT Intl. Symp. on Software Testing and Analysis
     (ISSTA 2008), Seattle, USA, July 20-24, 2008. ACM, 295–306.
[45] Fabio Somenzi and Aaron R. Bradley. 2011. IC3: where monolithic and incremental meet. In Proc. Intl. Conf. Formal
     Methods in Computer-Aided Design (FMCAD 2011), Austin, USA, October 30 - November 02, 2011, Per Bjesse and Anna
     Slobodová (Eds.). FMCAD Inc., 3–8.
[46] Gemini Team, Petko Georgiev, Ving Ian Lei, Ryan Burnell, Libin Bai, Anmol Gulati, Garrett Tanzer, Damien Vincent,
     Zhufeng Pan, Shibo Wang, et al. 2024. Gemini 1.5: Unlocking multimodal understanding across millions of tokens of
     context. arXiv preprint arXiv:2403.05530 (2024).
[47] Cheng Wen, Jialun Cao, Jie Su, Zhiwu Xu, Shengchao Qin, Mengda He, Haokun Li, Shing-Chi Cheung, and Cong
     Tian. 2024. Enchanting program specification synthesis by large language models using static analysis and program
     verification. In Proc. Intl. Conf. Computer Aided Verification (CAV 2024). Springer, 302–328.
[48] Zhe Zhou, Robert Dickerson, Benjamin Delaware, and Suresh Jagannathan. 2021. Data-driven abductive inference of
     library specifications. Proc. ACM Program. Lang. 5, OOPSLA (2021), 1–29.
[49] He Zhu, Stephen Magill, and Suresh Jagannathan. 2018. A data-driven CHC solver. In PLDI. ACM, 707–721.




                                                            26
Verification Modulo Tested Library Contracts


A    Benchmark Details

    Name                        Lbry LOC Clnt LOC #Obs-Mthds #Mthd Specs #LoopInvs
    AlternatingList                     100          15             2                1             1
    AtomicHashMap (1 - 5)              ∼3k      17 - 28             4             1-2           1-3
    AtomicLinkedList (1 - 2)          ∼500      16 - 19           1-2                2             2
    BinaryHeap (1 - 2)                ∼200      15 - 19           2-3                3          1-2
    BinaryTree                    100 - 200          14             2                2             1
    BlueWhite                         ∼100           14             1                1             2
    Calendar                          ∼100           12             2                1             1
    DLL_Circular                      ∼100           12             1                1             1
    DLL_Token                         ∼100            7             2                1             1
    FlatHashMap (1 - 2)                ∼3k      16 - 22             3                2          1-2
    FlatHashSet                        ∼3k           30             4                2             3
    LruCache                           ∼3k           19             3                2             1
    List (Max)                        ∼100           13             2                1             1
    List (Min)                        ∼100           13             2                1             1
    Multimap (1 - 2)                   ∼3k      12 - 21           2-3                1             1
    Multiset (1 - 2)                   ∼3k      13 - 20           2-3                1             1
    NormalFilterQueue                 ∼100           16             3                2             1
    PriorityFilterQueue               ∼100           16             3                2             1
    ProcessQueue                      ∼100           15             2                2             1
    RedBlackTree                      ∼100           17             4                2             1
    SkipList (1 - 7)                 ∼1000      14 - 16             4                2             1
    Stack                              ∼50           18             1                2             1
    StockOrder                        ∼100           13             2                1             1
    TokenBucket(1 - 3)                ∼200      15 - 18             1                2             1
Table 2. Features of Benchmarks. Columns represent: benchmark name (name), lines of code of library (Lbry
LOC), lines of code of client code (Clnt LOC), number of observer methods in the library (#Obs-methods),
number of methods to synthesize specifications (#Mthd Specs), and number of loops (#LoopInvs).




B Mutation Study
This section presents additional details of the mutation study used to evaluate the effectiveness of
VMTLC beyond testing.




                                                   27
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


B.1   Results

                                                         Passed by Passed by
                     Mutant                Passed by Contextual Modular
                  Benchmarks                Testing       VMTLC         VMTLC
                  AtomicHashMap1Mut1           ✓             ✓            ×
                  AtomicHashMap1Mut2           ✓              ×           ×
                  AtomicLinkedList1Mut1        ✓              ×           ×
                  AtomicLinkedList1Mut2        ✓              ×           ×
                  BinaryTreeMut1               ✓             ✓            ×
                  BinaryTreeMut2               ✓             ✓            ×
                  BlueWhiteMut1                ✓              ×           ×
                  BlueWhiteMut2                ✓             ✓            ×
                  CalendarMut1                 ✓              ×           ×
                  CalendarMut2                 ✓              ×           ×
                  DLL_CircularMut1             ✓             ✓            ×
                  DLL_CircularMut2             ✓              ×           ×
                  FlatHashSetMut1              ✓              ×           ×
                  FlatHashSetMut2              ✓              ×           ×
                  MaxMut1                      ✓              ×           ×
                  MaxMut2                      ✓              ×           ×
                  MinMut1                      ✓              ×           ×
                  MinMut2                      ✓              ×           ×
                  Multimap1Mut1                ✓             ✓            ×
                  Multimap1Mut2                ✓              ×           ×
                  NormalFilterQueueMut1        ✓              ×           ×
                  NormalFilterQueueMut2        ✓              ×           ×
                  ProcessQueueMut1             ✓             ✓            ×
                  ProcessQueueMut2             ✓             ✓            ×
                  RedBlackTreeMut1             ✓              ×           ×
                  RedBlackTreeMut2             ✓              ×           ×
                  SkipList1Mut1                ✓             ✓            ×
                  SkipList1Mut2                ✓             ✓            ×
                  StackMut1                    ✓              ×           ×
                  StackMut2                    ✓             ✓            ×
Table 3. Mutant Benchmarks that passed/failed Testing(30/0), Contextual VMTLC(11/19), and Modular
VMTLC(0/30)




B.2 Mutation Templates
To systematically introduce meaningful faults, we designed two mutation templates that inject
unsafe behavior through probabilistically rare execution paths. Both templates are designed to hide
unsafe states behind rare conditions that are difficult for testing to explore.
     • Mutation Template 1
       while (*) {
            v=*
            if ( v == Const) {
                 count++

                                                   28
Verification Modulo Tested Library Contracts


               } else {
                   count=0
               }
               if (count = 100) {
                   rare operation
               } else {
                   normal operation
               }
               //other operations
         }
         assert (client condition)
         }
       • Mutation Template 2
         while (*) {
             v=*
             if ( v == Const) {
                 count++
             } else {
                 count=0
             }
             //other operations
         }
         if (count = 100) {
             rare operation
         } else{
             normal operation
         }
         assert (client condition)

B.3     Why did 11 mutations pass VMTLC verification for contextual contracts?
The rare operations in both the above templates are difficult for the tester to explore and hence the
learner is able to give any strong adequate contextual contract which the verifier can accept to
prove the mutation.

C     LLM Prompts
C.1     Initial Prompt for Modular Contract Generation


You are an expert programmer specializing in formal verification with Z3Py. Your task is to define
specifications for general-purpose library functions (e.g., insert, search). You will also be given a
client program (in the Abstract and CHC sections) that uses these functions in a specific way. Your
goal is to find a Z3Py specification for each library function that meets two conditions:
      (1) The specification must encapsulate the library’s behavior, meaning it must be true
          for any valid inputs the library function might receive, not just the specific inputs used by
          the client.
      (2) The specification must be strong enough to prove the assertions of the client
          program when used within its specific context.

                                                   29
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


   The ultimate goal is for your generated Z3Py definitions to make all the client’s CHC rules valid.
   I. System Behavior Overview:
   Please analyze the following abstract program description to understand the intended behavior,
state variables, and operations. This provides semantic context for the relations you will define.
                                 [Client Program Pseudo Code]
  Z3 integer variables are used to model non-deterministic choices, indicated by [*].
  II. Formal CHC Specification Context:
  Please analyze the following CHC content. This is the formal basis for your task.
   (1) declare-rel statements: These define the names and expected arguments (types and
       order) for the Python/Z3Py functions you must create.
   (2) declare-var statements: These list the symbolic variables used within the CHC rules.
   (3) rule statements: These are the most critical part. Each rule (=> antecedent_formula
       consequent_formula) defines a logical implication. Your Z3Py function definitions must
       ensure that every one of these rules translates into a VALID Z3 implication.
   (4) extra info: ite stands for if then else.
                                            [CHC Rules]
   III. Pre-defined Z3 Variables and Constants in the Testing Environment:
   The Python script where your generated functions will be inserted has ALREADY DEFINED
global Z3 variables and Python constants. DO NOT redefine these in your output. The parameters
of your functions will be called with these Z3 variables (or expressions derived from them) in the
testing script.
      • Globally Available Z3 Integer Variables (These are examples):
           – len (representing current state values for some benchmarks)
           – len1 (representing next state values for some benchmarks)
           – prio_input (representing non-deterministic inputs to a loop iteration, if applicable to
             the benchmark)
      • Globally Available Z3 Boolean Variables (if applicable, based on declare-var):
           – ret1 (e.g., for a return status)
      • Globally Available Python Constants (These are examples; refer to define-fun in
         CHC.txt or initial values in Abst_Program.txt for benchmark-specific constants):
           – INT_MAX = 32767
           – INIT_MIN_PRIO = 1
           – INIT_MAX_PACKET_SIZE = 499
   IV. Your Task: Define Z3Py Function Bodies for Declared Relations
    (1) Identify Target Functions: For each (declare-rel relation_name (Type1 Type2
         ...)) statement in the CHC content (Section II), you must define a corresponding Python
         function.
    (2) Function Signatures: These are the function signatures:
                                          [Function Signatures]
   (3) Function Logic (The Core Task):
         • The body of each Python function must construct and return a single Z3 boolean
           expression.
         • This Z3 expression is the definition of the relation.
         • The logic for this expression should be derived from your understanding of the
           Abst_Program.txt (Section I) and, most importantly, by analyzing how the relation is

                                                   30
Verification Modulo Tested Library Contracts


             used within the rule statements of the CHC.txt (Section II). The goal is to define the
             relation such that all rules involving it become valid implications.
           • For example, an inv_loop function should define properties that make the CHC rules
             for initialization and preservation hold. An append_op function should define state
             changes that are consistent with the rules where append_op appears.
  V. Expected Output Format:
  Provide ONLY the complete Python code definitions for the required functions. Do not include
any surrounding text, explanations, or from z3 import *. Do not redefine any global Z3 variables
or constants (as per Section III).
  Example of Expected Output Structure (for a hypothetical benchmark):
def inv_relation_from_chc(p_arg1, p_arg2):
  # Logic using p_arg1, p_arg2, and implicitly relying on how these
  # parameters will be mapped to global Z3 variables in the CHC rules.
  # Constants like INT_MAX can be used if they are listed in Section III.
  return And(p_arg1 > 0, p_arg2 < INT_MAX)

def operation_relation_from_chc(p_curr_state_arg, p_next_state_arg, p_input_arg):
  # Logic defining the transition
  return (p_next_state_arg == p_curr_state_arg + p_input_arg - 1)
   VI. Additional Guidelines & Goal Clarification:
      • Primary Goal: Validity. The most important objective is that your generated Z3Py function
        definitions make ALL CHC rules (from Section II), when translated into Z3 implications,
        VALID.
      • Plausibility: The library functions you are defining are general-purpose. For example, an
        insert function can accept any valid integer, even if the client program in the abstract only
        ever calls it with 1 and 2.
      • For the key verification conditions (like invariant preservation for different paths), the
        antecedent of the implication should be satisfiable.
      • Maximal Specification (Secondary Goal, Strive For):
          – Once validity is achieved, aim for your specifications to be "maximal." Think of a specifi-
             cation (like an invariant inv(state) or an operation op(current_state, next_state))
             as defining a set of allowed states or state transitions.
          – A valid specification is maximal if you cannot add any more states (for an invariant)
             or any more input/output state pairs (for an operation) to the set it accepts without
             making the specification invalid (i.e., without causing one of the CHC rules to no longer
             hold).
          – Essentially, try to make your Z3 definitions as general or "permissive" as possible, in-
             cluding all behaviors that are consistent with the CHC rules and the abstract program’s
             intent. Avoid being overly restrictive if a more general valid definition exists.
          – There might be multiple different maximal specifications. Your goal is to find one that
             is as comprehensive as possible.
          – Crucially, prioritize achieving VALIDITY of all CHC rules above striving for maximality
             if there’s a conflict. A valid, slightly less general specification is much better than a
             more general but invalid one.
      • Consider edge cases (e.g., empty queues if len is a variable) as implied by the abstract
        program and CHC rules.

                                                 31
        Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


      • Pay close attention to how variables declared with (declare-var ...) in the CHC rules
        are used as arguments to your functions within those rules. This mapping is key.
  VII. Tips
  To succeed, you MUST follow this strategic guidance:
   (1) Think Relationally, Not Mathematically: Your primary goal is to define the relationship
       between the state at one step and the state at the next.
   (2) Prioritize the General Function First: Your mental process should be:
         • First: Define a plausible, general-purpose library function based on common data
           structure behavior.
         • Then: Define the invariant (inv1, inv2) to be a property that is true for the client’s
           specific usage of that general function. The invariant proves the client correct; the
           function defines the library.
   (3) How to Interpret Counterexamples: When you receive a counterexample, do not just
       patch the code to handle that specific case. Instead, try to infer the simplest, most general
       logical rule that the counterexample reveals.
   (4) The code is not wrong: There are no issues from my side. Rethink the logic if you think
       you are stuck.
   (5) keep it simple: Try to find simple contracts that satisfy validity.

C.2    Initial Prompt for contextual contract generation


You are an expert programmer specializing in formal verification with Z3Py. Your task is to analyze
a client program (described in the Abstract and CHC sections) and define Z3Py specifications for
the relations it uses. Your goal is to find a specification that is true for the relations within the
specific context of the client program’s execution flow. The ultimate goal is for these generated
contextual specifications to make all the client’s CHC rules valid.
   I. System Behavior Overview:
   Please analyze the following abstract program description to understand the intended behavior,
state variables, and operations. This provides semantic context for the relations you will define.
   Insert the abstract program description below:
                                  [Client Program Pseudo Code]
  Z3 integer variables are used to model non-deterministic choices, indicated by [*].
  II. Formal CHC Specification Context:
  Please analyze the following CHC content. This is the formal basis for your task.
   (1) declare-rel statements: These define the names and expected arguments (types and
       order) for the Python/Z3Py functions you must create.
   (2) declare-var statements: These list the symbolic variables used within the CHC rules.
   (3) rule statements: These are the most critical part. Each rule (=> antecedent_formula
       consequent_formula) defines a logical implication. Your Z3Py function definitions must
       ensure that every one of these rules translates into a VALID Z3 implication.
   (4) extra info: ite stands for if then else.
  Insert the CHC content below:
                                                 [CHC]
  III. Pre-defined Z3 Variables and Constants in the Testing Environment:

                                                    32
Verification Modulo Tested Library Contracts


   The Python script where your generated functions will be inserted has ALREADY DEFINED
global Z3 variables and Python constants. DO NOT redefine these in your output. The parameters
of your functions will be called with these Z3 variables (or expressions derived from them) in the
testing script.
      • Globally Available Z3 Integer Variables (These are examples):
          – len (representing current state values for some benchmarks)
          – len1 (representing next state values for some benchmarks)
          – prio_input (representing non-deterministic inputs to a loop iteration, if applicable to
             the benchmark)
      • Globally Available Z3 Boolean Variables (if applicable, based on declare-var):
          – ret1 (e.g., for a return status)
      • Globally Available Python Constants (These are examples; refer to define-fun in
        CHC.txt or initial values in Abst_Program.txt for benchmark-specific constants):
          – INT_MAX = 32767
          – INIT_MIN_PRIO = 1
          – INIT_MAX_PACKET_SIZE = 499
   IV. Your Task: Define Z3Py Function Bodies for Declared Relations
    (1) Identify Target Functions: For each (declare-rel relation_name (Type1 Type2
        ...)) statement in the CHC content (Section II), you must define a corresponding Python
        function.
    (2) Function Signatures: These are the function signatures. Do not define any other function
        beyond these.: Insert the function signatures below:
                                               [signatures]
    (3) Function Logic (The Core Task):
          • The body of each Python function must construct and return a single Z3 boolean
            expression.
          • This Z3 expression is the definition of the relation.
          • The logic for this expression should be derived from your understanding of the
            Abst_Program.txt (Section I) and, most importantly, by analyzing how the relation is
            used within the rule statements of the CHC.txt (Section II). The goal is to define the
            relation such that all rules involving it become valid implications.
          • For example, an inv_loop function should define properties that make the CHC rules
            for initialization and preservation hold. An append_op function should define state
            changes that are consistent with the rules where append_op appears.
  V. Expected Output Format:
  Provide ONLY the complete Python code definitions for the required functions. Do not include
any surrounding text, explanations, or from z3 import *. Do not redefine any global Z3 variables
or constants (as per Section III).
  Example of Expected Output Structure (for a hypothetical benchmark):
def inv_relation_from_chc(p_arg1, p_arg2):
  # Logic using p_arg1, p_arg2, and implicitly relying on how these
  # parameters will be mapped to global Z3 variables in the CHC rules.
  # Constants like INT_MAX can be used if they are listed in Section III.
  return And(p_arg1 > 0, p_arg2 < INT_MAX)

def operation_relation_from_chc(p_curr_state_arg, p_next_state_arg, p_input_arg):

                                                 33
        Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


  # Logic defining the transition
  return (p_next_state_arg == p_curr_state_arg + p_input_arg - 1)
  VI. Additional Guidelines & Goal Clarification:
      • Primary Goal: Validity. The most important objective is that your generated Z3Py func-
        tion definitions make ALL CHC rules (from Section II), when translated into Z3 implications,
        VALID. These function definitions will be tested against their corresponding library func-
        tions only on inputs that occur in the execution of the Client Program (Abstract).
      • For the key verification conditions (like invariant preservation for different paths), the
        antecedent of the implication should be satisfiable.
      • Consider edge cases (e.g., empty queues if len is a variable) as implied by the abstract
        program and CHC rules.
      • Pay close attention to how variables declared with (declare-var ...) in the CHC rules
        are used as arguments to your functions within those rules. This mapping is key.
  VII. Tips
  To succeed, you MUST follow this strategic guidance:
   (1) Think Relationally, Not Mathematically: Your primary goal is to define the relationship
       between the state at one step and the state at the next.
   (2) How to Interpret Counterexamples: When you receive a counterexample, do not just
       patch the code to handle that specific case. Instead, try to infer the simplest, most general
       logical rule that the counterexample reveals.
   (3) The code is not wrong: There are no issues from my side. Rethink the logic if you think
       you are stuck.
   (4) keep it simple: Try to find simple contracts that satisfy validity.

C.3    Repair Prompt for Z3 Validity Failures



  The previous Z3 code was invalid. The validator failed with this output:
                                    [Validity Checker Report]
   Your task is to fix the code based on the validator’s output. Respond with ONLY the complete,
corrected, and runnable Python code for all functions. Do not include any explanations, apologies,
introductory text, or markdown formatting like “‘python. Your entire response must be valid Python
code.

C.4    Repair Prompt for Testing Failures



  The previous Z3 specification was valid but failed testing. The counterexample data is:
                                           [Tester Report]
   Your task is to analyze the counterexample and provide a new, corrected version of the Z3 code
to fix the logical flaw. Respond with ONLY the complete, corrected, and runnable Python code for
all functions. Do not include any explanations, introductory text, or markdown formatting like
“‘python. Your entire response must be valid Python code.

                                                    34
Verification Modulo Tested Library Contracts


C.5    Initial Prompt for HornICE+LLM



   You are an expert in program semantics and formal verification. Your primary task is to analyze
an abstract program description and its corresponding CHC specification. For each relation declared
in the CHC file (like inv, insert, etc.), you will generate a textual description of its parameters
and a list of core arithmetic and logical sub-expressions that describe the relationships between
those parameters.
   I. System Behavior Overview:
   Please analyze the following abstract program description to understand the intended behavior,
state variables, and operations. This provides semantic context for the relations you will analyze.
                                     [Client Program Pseudo Code]
   II. Formal CHC Specification Context:
   Please analyze the following CHC content. This content primarily serves to:
      • Identify the names and expected arguments (types and order) for the Python functions you
        must create (from declare-rel statements).
      • Provide context on how these relations are used in logical rules, which will inform the
        plausible semantics you need to model.
      • List the symbolic variables involved (from declare-var statements).
                                               [CHC Rules]
  III. Pre-defined Variable and Constant Context:
  The CHC file may use pre-defined constants. Your analysis should be consistent with these
definitions.
  Example: (define-fun INT_MAX () Int 32767) means INT_MAX is 32767.
  IV. Your Task: Generate Textual Expression Sets for Each Relation
  For each relation defined by a (declare-rel ...) statement in Section II, you must:
      • Analyze its plausible behavior based on its name, its arguments, the abstract program, and
        its usage in the CHC rules.
      • Identify the core arithmetic relationships between its parameters. For example, if a relation
        describes len1 = len + 1, a key expression is len1 - len .
      • Format your output for that relation exactly as described in Section V below.
   Function Signatures: These are the function signatures:
                                          [Function Signatures]
   Function Logic (The Core Task):
   From the behavior of these functions, you will extract key arithmetic or boolean terms.
   Canonical Form: Where possible, express relationships as terms that would be compared to
zero. For example, if you infer a behavior x = y + 2, the corresponding expression to return in
the list would be x - y. If you infer a > b, a good expression would be a - b.
   V. Expected Output Format:
   Provide your response as a block of text. For each relation, you must generate a multi-line entry
strictly following this format:
      • A header line: <relation_name> <num_parameters> <num_expressions>
      • A list of parameter mappings, one per line: <index> <parameter_name>
      • A list of the extracted expressions, one per line, using the parameter names you just defined.

                                                   35
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


  Example of the Required Output Format (for a hypothetical benchmark):
insert 5 7
0 n
1 min
2 min1
3 isEmpty
4 isEmpty1
n - min1
min1 - n
n - min
min - n
min1 - min
min - min1
min1 - n

search 4 2
0 v
1 min
2 isEmpty
3 ret1
v - min
min - v
   VI. Goal Clarification:
   Primary Goal: Useful Expressions. Your goal is to provide a rich set of fundamental expres-
sions (building blocks). A downstream solver will take these expressions e and try to find a valid
specification by combining them into predicates of the form e > c, or e = c (where c is a constant).
Your generated expressions should be these e terms.
   Completeness: Aim to provide a comprehensive set of simple expressions that capture the
relationships. For example, if a and b are compared, providing both a - b and b - a can be useful
for the solver.

C.6   initial prompt for hornice+llm (contextual)


You are an expert in program semantics and formal verification. Your task is to analyze a specific
client program and its corresponding CHC specification. For each relation (like inv, insert, etc.),
you will generate a list of core arithmetic sub-expressions. These expressions must describe the
relationships between the function parameters only as they occur within the specific execution
flow of the client program.
   I. System Behavior Overview:
   Please analyze the following abstract program description to understand the intended behavior,
state variables, and operations. This client program description defines the exact execution context
for your analysis. The expressions you generate must be consistent with the state changes and
variable values that can occur within this specific program.
                                 [Client Program Pseudo Code]
  II. Formal CHC Specification Context:
  Please analyze the following CHC content. This content primarily serves to:

                                                   36
Verification Modulo Tested Library Contracts


     • Identify the names and expected arguments (types and order) for the Python functions you
       must create (from declare-rel statements).
     • Provide context on how these relations are used in logical rules, which will inform the
       plausible semantics you need to model.
     • List the symbolic variables involved (from declare-var statements).
                                               [CHC Rules]
  III. Pre-defined Variable and Constant Context:
  The CHC file may use pre-defined constants. Your analysis should be consistent with these
definitions.
  Example: (define-fun INT_MAX () Int 32767) means INT_MAX is 32767.
  IV. Your Task: Generate Textual Expression Sets for Each Relation
  For each relation defined by a (declare-rel ...) statement in Section II, you must:
     • Analyze its plausible behavior based on its name, its arguments, the abstract program, and
        its usage in the CHC rules.
     • Identify the core arithmetic relationships between its parameters. For example, if a relation
        describes len1 = len + 1, a key expression is len1 - len.
     • Format your output for that relation exactly as described in Section V below.
  Function Signatures: These are the function signatures:
                                          [Function Signatures]
   Function Logic (The Core Task):
      • From the behavior of these functions, you will extract key arithmetic or boolean terms.
      • Canonical Form: Where possible, express relationships as terms that would be compared
         to zero. For example, if you infer a behavior x = y + 2, the corresponding expression to
         return in the list would be x - y. If you infer a > b, a good expression would be a - b.
   V. Expected Output Format:
   Provide your response as a block of text. For each relation, you must generate a multi-line entry
strictly following this format:
      • A header line: <relation_name> <num_parameters> <num_expressions>
      • A list of parameter mappings, one per line: <index> <parameter_name>
      • A list of the extracted expressions, one per line, using the parameter names you just defined.
   Example of the Required Output Format (for a hypothetical benchmark):
insert 5 7
0 n
1 min
2 min1
3 isEmpty
4 isEmpty1
n - min1
min1 - n
n - min
min - n
min1 - min
min - min1
min1 - n


                                                   37
       Abhishek Uppar, Omar Muhammad, Sumanth Prabhu S, Deepak D’Souza, P. Madhusudan, and Adithya Murali


search 4 2
0 v
1 min
2 isEmpty
3 ret1
v - min
min - v
  VI. Goal Clarification:
    • Primary Goal: Useful Expressions. Your goal is to provide a rich set of fundamental
       expressions (building blocks). A downstream solver will take these expressions e and try to
       find a valid specification by combining them into predicates of the form e > c, or e = c
       (where c is a constant). Your generated expressions should be these e terms.
    • Completeness: Aim to provide a comprehensive set of simple expressions that capture the
       relationships. For example, if a and b are compared, providing both a - b and b - a can
       be useful for the solver.
    • Focus on Context, Not Generality: The expressions you generate should model the
       function’s behavior only as it’s called by the client program. For example, if the client’s
       logic ensures an insert function is only ever called with positive integers, your expressions
       should reflect this constraint. You do not need to generate expressions for behaviors that
       are impossible within this specific client’s execution flow.
    • Allowed Symbols: Each expression should be constructed using variable names, and the
       symbols: (, ), +, -. Integers, logical expressions etc are not allowed.

Received 20 February 2007; revised 12 March 2009; accepted 5 June 2009




                                                   38
