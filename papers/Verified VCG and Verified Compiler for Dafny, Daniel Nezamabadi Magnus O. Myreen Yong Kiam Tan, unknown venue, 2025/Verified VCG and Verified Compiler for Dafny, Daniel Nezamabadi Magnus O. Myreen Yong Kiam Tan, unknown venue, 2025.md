                                                  Verified VCG and Verified Compiler for Dafny
                                                   Daniel Nezamabadi                                Magnus O. Myreen                               Yong Kiam Tan
                                                          ETH Zurich                        Chalmers University of Technology           Institute for Infocomm Research (I2 R),
                                                          Switzerland                           University of Gothenburg                                A*STAR
                                                                                                         Sweden                                        Singapore
                                                                                                                                         Nanyang Technological University
                                                                                                                                                       Singapore

                                        Abstract                                                                  method M(n: int) returns (r: int)
                                        Dafny is a verification-aware programming language that                     ensures r == if n <= 100 then 91 else n - 10
                                        comes with a compiler and static program verifier. However,                 decreases 111 - n
                                        neither the compiler nor the verifier is proved correct; in fact,         {
arXiv:2512.05262v1 [cs.PL] 4 Dec 2025




                                        soundness bugs have been found in both tools. This paper                    if n <= 100 {
                                        shows that the aforementioned Dafny tools can be devel-                       var tmp := M(n + 11);
                                        oped with foundational correctness guarantees. We present                     r := M(tmp);
                                        a functional big-step semantics for an imperative subset of                 } else {
                                        Dafny and, based on this semantics, a verified verification                   r := n - 10;
                                        condition generator (VCG) and a verified compiler for Dafny.                }
                                        The subset of Dafny we have formalized includes mutually                  }
                                        recursive method calls, while loops, and arrays—these lan-
                                        guage features are significant enough to cover challenging                               Figure 1. “91 function” in Dafny.1
                                        examples such as McCarthy’s 91 function and array-based
                                        programs that are used when teaching Dafny. The verified
                                        VCG allows one to prove functional correctness of annotated                  To build an intuition on how Dafny works, consider Mc-
                                        Dafny programs, while the verified compiler can be used                   Carthy’s 91 function [43] shown in Figure 1, a nested re-
                                        to compile verified Dafny programs to CakeML programs.                    cursive function that is used as a basic test for automated
                                        From there, one can obtain executable machine code via                    verification. It is interesting from an automation perspective
                                        the (already verified) CakeML compiler, all while provably                because to show that the value of the decreases clause ac-
                                        maintaining the functional correctness guarantees that were               tually decreases in the second recursive call, the prover must
                                        proved for the source-level Dafny programs. Our work has                  simultaneously establish the postcondition for tmp. To prove
                                        been mechanized in the HOL4 theorem prover.                               that the implementation satisfies the specifications given
                                                                                                                  in the ensures and decreases clauses, the verifier trans-
                                        CCS Concepts: • Theory of computation → Higher order                      lates Dafny to Boogie [6, 40], an intermediate verification
                                        logic; Program verification; • Software and its engineer-                 language and verification condition generator (VCG). The
                                        ing → Compilers; Software verification;                                   generated verification conditions are then checked using a
                                                                                                                  satisfiability modulo theories (SMT) solver, such as Z3 [17].
                                        Keywords: verified compilation, verified verification condi-              In order to run the program, the Dafny compiler translates it
                                        tion generator, CakeML, Dafny, interactive theorem proving                to a language, e.g., C#, whose toolchain(s) can then be used
                                                                                                                  to generate a binary.
                                                                                                                     Both the Dafny compiler and VCG pipeline are substantial
                                        1    Introduction
                                                                                                                  pieces of software that must produce trustworthy results.
                                        Dafny [41] is a verification-aware programming language                   Unfortunately, past work has identified issues—particularly
                                        with built-in support for specifications and supporting tools:            soundness bugs—in both the implementation of the compiler
                                        a compiler and static program verifier. Recently, Dafny has               and the verifier [18, 34]. We aim to address these limitations
                                        been successfully used by Amazon Web Services to develop                  by showing that it is possible for Dafny to be done in a
                                        a new and improved version of their authorization engine                  foundational, end-to-end manner. In this work, we make the
                                        while provably maintaining the functional behavior of the                 following contributions:
                                        original implementation [13].
                                                                                                                      • Define functional big-step semantics [49] for an im-
                                                                                                                        perative subset of Dafny, including mutually recursive
                                                                                                                        method calls, while loops, and arrays (Section 2).
                                        This work is licensed under a Creative Commons Attribution 4.0 Interna-
                                        tional License.                                                           1 Adapted from the Dafny GitHub repository.
                                                                                 Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


      • Implement a verified compiler from our subset of            Array values hold their length, location on the heap, and
        Dafny to CakeML [38], which, in turn, provides a            the type of their elements.2 Note that our language supports
        verified compiler down to machine code (Section 3).         nested arrays, e.g., an array of arrays of integers, which is
      • Define a weakest precondition (wp) calculus for the         not to be confused with multi-dimensional arrays. The heap
        Dafny subset, prove its soundness, and use it to im-        itself is a list of heap values; thus, heap locations are indices
        plement a verified VCG (Section 4).                         into that list. We currently only support arrays but plan to
   Our subset is expressive enough to support examples such         add objects in the future.
as the previously introduced 91 function, and array-based
programs that are used when teaching Dafny. We demon-                             heap_value = HArr (value list) type
strate our contributions in Section 5, where we apply both
the compiler and VCG to the 91 function and a method that              Results. The interpreter can fail due to undefined behav-
swaps two elements in an array (Swap), followed by proving          ior (Rfail), such as trying to read an undeclared or uninitial-
the resulting verification conditions to be valid. This yields      ized variable, or timing out (a feature of functional big-step
functional correctness guarantees at the level of compiled          semantics):
CakeML functions.
   We have mechanized this work in the HOL4 theorem                                    err_result = Rfail | Rtimeout
prover. Below, we present and motivate key design choices
in the formalization that enabled each of our contributions.          The result type is different for expressions and statements.
                                                                    Evaluating an expression can either return a value or fail
2     Semantics                                                     due to the reasons above:
Before we can write a verified compiler or verified VCG,
we must first formalize the meaning of Dafny programs. We                       𝛼 exp_result = Rval 𝛼 | Rerr err_result
opted to define an untyped, functional big-step semantics [49]
for Dafny, i.e., a definitional interpreter function with a clock   By parameterizing the type of the value being returned, we
(also called fuel) to ensure its termination and thereby de-        can use the same data type when returning a single value or
finability within the HOL4 logic. This style of semantics is        a list of values, with the latter occurring when we evaluate
also used for CakeML and its compiler’s intermediate lan-           a list of expressions.
guages because it is particularly well-suited for mechanizing          When evaluating a statement, the result can be to either
compiler correctness results in HOL4 [49].                          continue or stop the current evaluation:
   The main syntactic objects are expressions (dfy_exp), state-
ments (dfy_stmt), and programs (program); Dafny programs                            stmt_result = Rcont | Rstop stop
are a list of declarations used to look up functions and meth-
ods. Our interpreters for Dafny expressions and statements          The current evaluation can be stopped due to evaluating a
have the following type signatures, respectively:                   return statement or an error:
      evaluate_exp : state → dfy_env → dfy_exp
                                                                                       stop = Sret | Serr err_result
                      → state × value exp_result
      evaluate_stmt : state → dfy_env → dfy_stmt
                      → state × stmt_result                         By factoring out the reason for stopping into a separate
                                                                    type, we make it easier in the future to add support for more
   In this section, we will first introduce the types repre-        statements that cause changes in the control flow, such as
senting the semantic primitives such as value, 𝛼 exp_result,        continue and labeled break statements.
stmt_result, dfy_env, and state. Afterward, we will define
interpreter semantics for Dafny expressions and statements,            Environments. The semantic environment record con-
followed by the semantics of Dafny programs.                        tains the entire Dafny program, which is searched when
                                                                    calling functions or methods.
2.1    Semantic Primitives
  Values. We support integers, booleans, strings, and arrays,                        dfy_env = ⟨| prog : program |⟩
and define the value type as follows:
                   value =                                          2While it is not necessary for array values to hold the length of the array in
                      IntV int
                                                                    the one-dimensional case, it is necessary for multi-dimensional arrays (for
                    | BoolV bool                                    which we plan to add support in the future), as in some cases we cannot
                    | StrV string                                   determine the length of inner arrays by indexing to them first if they follow
                    | ArrV num num type                             zero-length dimensions.
Verified VCG and Verified Compiler for Dafny


   States. We define the state of the interpreters with the            order for expressions follows Dafny’s short-circuit seman-
following record:                                                      tics. In the absence of short-circuiting, we choose to evaluate
                                                                       expressions from left to right, which feels more natural in
        state = ⟨|
                                                                       the context of Dafny.
            clock : num;
                                                                          As a verification-oriented programming language, Dafny
            locals : (string × value option) list;
                                                                       provides expressions that are only for verification. These
            heap : heap_value list;
                                                                       can be used to give hints to the automated verifier (with
            locals_old : (string × value option) list;
                                                                       the assert statement) or annotate methods with a pre- and
            heap_old : heap_value list;
                                                                       postcondition (with keywords requires and ensures re-
            locals_prev : (string × value option) list;
                                                                       spectively). In particular, the expressions in these constructs
            heap_prev : heap_value list
                                                                       are required to be Dafny expressions that evaluate to boolean
         |⟩
                                                                       values. The postcondition expression for many methods will
   To ensure that the functional big-step interpreters are well-       often need to relate the state of the heaps before and after
defined, terminating functions, the clock keeps track of the           the execution of the method body. Accordingly, Dafny has
number of clock ticks that are still available. Each time we           special support for old-expressions, which allow referring
evaluate an expression or statement that could potentially             to the state before the body was executed within the post-
diverge, such as calls or while loops, we first check whether          condition.
there are ticks still available. If no more ticks are available, the      To illustrate this, consider the following method that swaps
interpreter returns the timeout error as its result. Otherwise,        two elements in an array:
the clock is decremented, and evaluation continues.
                                                                       method Swap(a: array<int>, i: int, j: int)
   The locals field is an association list that keeps track of all
                                                                         requires 0 <= i < a.Length && 0 <= j < a.Length
declared variables and their values. By using the first match
                                                                         ensures a[i] == old(a[j]) && a[j] == old(a[i])
when looking up a variable, we can support shadowing by
                                                                         modifies a
simply prepending elements. Since Dafny does not require
                                                                       {
local variables to be initialized immediately when they are
                                                                         // <- old refers to the state here
declared, we use an option to indicate their initialization sta-
                                                                         var temp := a[i];
tus. Recall that trying to read an undeclared or uninitialized
                                                                         a[i] := a[j];
variable causes the interpreter to return the Rfail error. As
                                                                         a[j] := temp;
mentioned earlier, the heap field models a list of heap values,
                                                                         // <- ensures refers to state here
where elements are looked up via their (list) index.
                                                                       }
   The locals_old and heap_old fields hold the values of lo-
cals and heap right before executing the body of a method.             As ensures refers to the state after executing the method
These are necessary to support the semantics of Dafny’s                body, the user must use old to refer to the array before it
old-expressions, which are discussed in the next section.              was modified.
   Finally, the locals_prev and heap_prev fields are used in-            We define the semantics for old as
ternally by the generated verification conditions, allowing                  evaluate_exp st env (OldHeap e) =
                                                                                                                 def

them to refer to a previously set state as needed.                            case evaluate_exp (use_old_heap st) env e of
                                                                                (st1 ,r) ⇒ (unuse_old_heap st1 st,r)
2.2   Expressions and old-expressions
The semantics of Dafny expressions is straightforward. For                                def
                                                                        use_old_heap st = st with heap := st.heap_old
example, we define the semantics for a unary operation as                                       def
follows by first evaluating the operand to a value, then ap-            unuse_old_heap cur prev = cur with heap := prev.heap
plying the unary operator:                                                In other words, a user-annotated expression wrapped
                                                     def               within old is evaluated in the heap state with respect to the
           evaluate_exp st0 env (UnOp uop e) =                         old heap, which the semantics sets when it enters a callee.
            case evaluate_exp st0 env e of                                We also track the old locals because the state does not sep-
              (st1 ,Rval v) ⇒                                          arate track parameters, i.e., they are indistinguishable from
                (case do_uop uop v of                                  other locals, and because Dafny allows shadowing parame-
                   None ⇒ (st1 ,Rerr Rfail)                            ters. To illustrate this point, suppose that after swapping the
                 | Some res ⇒ (st1 ,Rval res))                         elements in the array, the user writes var a := 0; shadow-
            | (st1 ,Rerr err) ⇒ (st1 ,Rerr err)                        ing a to be an integer. If we were to take the ensures as is,
Evaluating an expression only changes the state by decre-              a would mistakenly refer to the newly declared integer vari-
menting the clock when function calls are made, which we               able. We avoid this by interpreting references to parameters
have proven as a theorem about the semantics. Evaluation               in ensures annotations to be implicitly wrapped in an Old
                                                                              Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


expression, which, analogous to OldHeap above, evaluates          method Find(a: array<int>, key: int)
an expression in the old heap and the old locals.                   returns (i: int)
                                                                    ensures 0 <= i ==> i < a.Length && a[i] == key
2.3   Statements                                                    ensures i < 0 ==>
                                                                      forall k :: 0 <= k < a.Length ==> a[k] != key
As many Dafny programs are written in an imperative style,
                                                                  {
we also define semantics for statements, which may modify
                                                                    i := 0;
the state of the program.
                                                                    while i < a.Length
   Skip, Return, and Then. We can easily define the seman-            invariant 0 <= i <= a.Length
tics of Skip, Return, and Then:                                       invariant
                                                                        forall k :: 0 <= k < i ==> a[k] != key
                                  def                               {
      evaluate_stmt st env Skip = (st,Rcont)                          if a[i] == key { return; }
                                     def
      evaluate_stmt st env Return = (st,Rstop Sret)                   i := i + 1;
                                                def
      evaluate_stmt st0 env (Then stmt1 stmt2 ) =                   }
       case evaluate_stmt st0 env stmt1 of                          i := -1;
         (st1 ,Rcont) ⇒ evaluate_stmt st1 env stmt2               }
       | (st1 ,Rstop stp) ⇒ (st1 ,Rstop stp)
                                                                                 Figure 2. Linear search in Dafny.4
Recall that the clock is used to prove termination of the
interpreter. As the recursive call in the Then case takes a
                                                                     While. We define the semantics for While as follows:3
strictly smaller statement as an argument, we do not need
to decrement the clock to prove termination.                           evaluate_stmt st0 env
                                                                                                                 def
                                                                        (While guard invs decrs mods body) =
  Assign. Dafny supports parallel assignment, meaning                   if st0 .clock = 0 then (st0 ,Rstop (Serr Rtimeout))
that it is possible to swap the value of two variables by               else
writing, e.g.,                                                            case evaluate_exp (dec_clock st0 ) env guard of
                      x, y := y, x;                                         (st1 ,Rval (BoolV F)) ⇒ (st1 ,Rcont)
                                                                          | (st1 ,Rval (BoolV T)) ⇒
which we support by first evaluating the expressions on the                 (case evaluate_stmt st1 env body of
right-hand side of an assignment, followed by assigning to                     (st2 ,Rcont) ⇒
the left-hand sides from left to right.                                          evaluate_stmt st2 env
                                                                                   (While guard invs decrs mods body)
  Array Allocation. To allocate a (possibly nested) one-                     | (st2 ,Rstop stp) ⇒ (st2 ,Rstop stp))
dimensional array in Dafny, we can write                                  | (st1 ,Rval guard_v) ⇒ (st1 ,Rstop (Serr Rfail))
                    a := new T[len];                                      | (st1 ,Rerr err) ⇒ (st1 ,Rstop (Serr err))
                                                                  Note that, unlike Then, the recursive call takes the same
where T is the type of the array and len its length. Note that
                                                                  while loop as an argument, meaning that the size of the
the allocation on the right-hand side of the assignment does
                                                                  statement being evaluated stays the same. Thus, every time
not specify an initial value. According to the Dafny reference,
                                                                  we enter the loop, we need to check and decrement the clock.
the initial array elements are arbitrary values of type T. This
                                                                     It is not strictly necessary to check and decrement the
is in contrast to our semantics, which supplies a default value
                                                                  clock immediately on entry; instead, it is possible to check
for the array elements. For the types supported by our subset,
                                                                  and decrement the clock right before the recursive call. We
defining a default value is straightforward. The advantage of
                                                                  decided to use the former, as it simplifies the correctness
this tweak is that it avoids the non-deterministic choice of
                                                                  proof for the compiler by more closely matching the seman-
an arbitrary value in the semantics, which otherwise would
                                                                  tics of function calls, which is what loops compile to.
have to be accounted for, e.g., by making the semantics non-
deterministic via an oracle.                                       Method Call. We avoid showing the full semantics of a
    Formally, array allocation is defined as appending a heap     method call due to its length. Instead, we use an example.
value HArr xs t to the heap, where xs is a list of len copies
                                                                  3 Note that we do not check that the loop invariants invs hold here. As
of the default value, and returning a value ArrV which, as
                                                                  we will see in Section 4, they are considered in the wp-calculus instead.
described in Section 2.1, records the length, location on the     This suggests that our semantics for Dafny is actually a combination of the
heap, and the type of the array. Note that Dafny does not         functional big-step semantics presented here and the sound wp-calculus.
support deallocation.                                             4 Adapted from https://dafny.org/dafny/OnlineTutorial/guide.
Verified VCG and Verified Compiler for Dafny


Suppose we want to call a method Find, which implements                  1. Generate an S-expression from an extended version
linear search (Fig. 2). We write                                            of Dafny’s existing frontend.
                    idx := Find(a, key)                                  2. Parse the S-expression into a Dafny AST in HOL4.
                                                                         3. Remove assert statements by replacing them with
as the method call. Note that the caller must assign all out-               Skip.
parameters. The semantics of the method call are as follows:             4. Freshen the AST, which updates all variable names to
     1. Look up “Find” in the prog field of the environment.                be unique and start with “v”, simplifying proofs.
     2. Evaluate the parameters a and key in the caller.                 5. Compile the freshened Dafny AST into a CakeML AST,
     3. Check if the in- and out-parameters a, key, and i are               discarding annotations.
        distinct.                                                        6. Compile the CakeML AST to machine code in a veri-
     4. Change locals to only contain the parameters a and                  fied manner using the CakeML compiler [59].
        key initialized with their values, and the uninitialized   This pipeline is engineered to maintain compatibility with
        out-parameter i.                                           both Dafny tooling and the CakeML codebase and proofs. We
     5. Copy the changed locals and the current heap to lo-        have successfully compiled and run machine code for 18 code
        cals_old and heap_old, respectively.                       examples, including Fibonacci, the 91 function, swapping
     6. Check the clock, and time out if no more ticks remain.     two elements in an array, and binary search.
     7. Decrement the clock and evaluate the method body,            In the rest of this section, we focus on describing the
        expecting Rstop Sret as the return value.                  Dafny-to-CakeML transformation, namely steps 3 and 4. The
     8. Evaluate the out-parameter i in the callee.                compiler for these steps is defined as the function compile
     9. Restore locals, locals_old, and heap_old to the original
        values of the caller.
                                                                                   def
                                                                    compile dfy =
    10. Assign the value of the out-parameter i to idx.              from_program (freshen_program (remove_assert dfy))
There are two noteworthy points regarding the evaluation of           The technical challenges in implementing and verifying
the method body in step 6. First, evaluating the method body       compile include reconciling our choice of left-to-right evalu-
requires a recursive call to evaluate_stmt. As the method          ation order with CakeML’s right-to-left order and handling
body can be arbitrarily large, we must check and decrement         the possibility of early returns from Dafny method calls. We
the clock to be able to prove termination. Second, we require      first explain our implementation, then present the compiler
the recursive call to return Rstop Sret; that is, the method       correctness statement and proof.
body must end with a return statement. Note that if a source
program does not explicitly end with return (such as in Fig. 2),   3.1    Compiler Implementation
the return statement is added automatically by our frontend.
                                                                   Let us return to the linear search implementation shown in
                                                                   Figure 2 to describe our compiler. This example showcases
2.4    Programs
                                                                   many key features of Dafny; in order to compile it, we need
Matching Dafny’s notion of executable programs, we define          to map Dafny’s variables, arrays, while loops, (early) returns,
the semantics of a program as first checking whether meth-         and methods to CakeML. Note that neither ensures nor
ods and functions have unique names, followed by calling           invariant clauses, nor their contents such as forall, are
“Main” from an initial state where locals, heap, and their old     compiled, as they are used only for verification purposes.
counterpart are initialized with the empty list.
                                                                     Variables. We compile Dafny variables to CakeML ref-
                                                   def
      evaluate_program ck (Program members) =                      erences, which are mutable variables and thus semantically
       if ¬distinct (map member_name members) then                 equivalent. For example, i := i + 1 in Dafny is compiled to
         (init_state ck,Rstop (Serr Rfail))                        i := !i + 1, where ! is the dereference operator in CakeML.
       else                                                        We postpone the discussion of variable declarations to the
         evaluate_stmt (init_state ck)                             compilation of the method signature later in this section.
           (mk_env (Program members))
           (MetCall [] «Main» [])                                    Arrays. Dafny arrays are compiled to tuples that hold the
                                                                   array and its length for the reason mentioned in Footnote 2.
3     Verified Compiler                                            For example, in Figure 2, the array a is represented by a
                                                                   corresponding CakeML value of type (int * int array).
We now turn to describing our formally verified compiler           Thus, a[i] is compiled to Array.sub (snd (!a)) (!i)
from Dafny to CakeML, which, together with CakeML’s                and a.Length is compiled to fst (!a).
formally verified compiler [59], yields a verified compilation
pipeline for Dafny down to machine code. Our overall Dafny           While Loops. We compile while loops as tail-recursive
compilation pipeline is as follows:                                functions, matching the definition of while in Standard
                                                                            Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


ML [44]. The CakeML compiler performs tail-call optimiza-                  let val (t0, t1) = dfy_Find key a
tion, i.e., tail-recursive functions do not require allocating             in min := t0; max := t1 end
a new stack frame with every call, meaning that there is          If a method does not have any out-parameters, its return
no risk of our compilation of loops causing excessive stack       value and the assignment become ().
allocation. The loop in Figure 2 is compiled to:                     By prepending “dfy_” to method names, combined with
       let fun loop () =                                          the fact that after the freshen pass all user-generated variable
           if !i < fst (!a) then (                                names start with “v”, the compiler can generate additional
              if Array.sub (snd (!a), !i) = !key                  names, such as t0 and t1 in the preceding examples, which
              then raise Return else ();                          (provably) do not change the semantics of the program.
              i := !i + 1;                                           We reverse the order of arguments to account for the
              loop ()                                             difference in evaluation order between CakeML and Dafny.
           ) else ()                                              Instead of reversing the order of arguments, we could have
       in loop (); ... end                                        enforced a left-to-right evaluation order using let-bindings.
Note that we call loop at least once. After entering the loop,    The disadvantage of this approach is that we need to generate
we check whether the loop condition holds. If it does, we         as many internal variables as there are arguments and prove
execute the body and recursively tail-call the loop. If the       that they do not change the semantics. While this is possible
condition does not hold, the expression evaluates to ().          and we do similar proofs in other parts of the compiler, they
   Additionally, observe that the Dafny code returns imme-        are tedious.
diately once the key is found. In CakeML, we compile this            Having a picture of how method calls are compiled, we can
as raising the Return exception. To ensure the existence of       now discuss the compilation of the rest of the method outside
this exception, the compiler inserts                              the body. In particular, the compiled method must return
                     exception Return;                            the values of the out-parameters at the end of the method.
                                                                  As a method always explicitly returns, we can simply wrap
at the beginning of every program. We postpone the dis-
                                                                  the compiled body in an exception handler, which reads the
cussion of how we handle the Return exception from the
                                                                  out-parameters and returns their value:
perspective of the caller until later in the text.
   The rest of the body after the loop is compiled as                              <compiled body>
                         i := ~1;                                                    handle Return => !i
                         raise Return                               The last remaining step is to compile the method signature:
Recall that the final (non-early) return line is implicitly in-                    fun dfy_Find key a =
serted by the Dafny frontend at the source level and thereby                       let
compiled the same way as all return calls to a CakeML                                val key = ref key
Return exception. This insertion ensures that every method                           val a = ref a
call explicitly returns, which is consistent with our seman-                         val i = ref 0
tics.                                                                              in ... end
   Methods. Before discussing the compilation of the rest            As the body refers to the parameters as variables, and we
of the method outside the body, it is useful to first discuss     compile variables as references, we have to allocate refer-
the compilation of method calls. Suppose that idx is a local      ences for key, a, and i. Note that key and a are initialized
variable, and a and key are bound to some array and integer,      with the respective arguments, whereas the out-parameter i
respectively. Then, the method call                               (uninitialized in Dafny) is initialized to be 0.
                  idx := Find(a, key)                                In general, we compile variable declarations, including
is compiled to                                                    out-parameters, as references that are initialized with 0 re-
                let val t0 = dfy_Find key a                       gardless of their type. This can produce CakeML code that
                in idx := t0 end                                  does not pass CakeML’s type checker but allows us to avoid
                                                                  an extra layer of boxing, e.g., by storing references to op-
   Note how we assign to the left-hand side in a separate         tions. However, in some cases, this compilation scheme still
expression, prepend “dfy_” to the method name, and reverse        introduces unnecessary assignments. In the future, we plan
the order of arguments. While separating the assignment is        to implement a compiler pass that eliminates such redun-
not necessary in this case, it is necessary when a method has     dant assignments where possible, which would allow further
multiple out-parameters, in which case, the method returns        optimizations such as removing references in cases where a
a tuple. For example,                                             variable is only read.
                 min, max := MinMax(a)                               Note that generating potentially type-incorrect CakeML
is compiled to                                                    is not necessarily a problem in terms of correctness for two
Verified VCG and Verified Compiler for Dafny


exception Return;                                                  whose definition is straightforward for integers, booleans,
                                                                   and strings. For example, it is defined as follows for integers:
(* fst and snd are inlined in the compiler *)
                                                                               ⊢ val_rel m (IntV i) (Litv (IntLit i))
fun fst (x, y) = x;
fun snd (x, y) = y;                                                  Array values in Dafny are equivalent to a CakeML tu-
                                                                   ple containing the length of an array and its location in
fun dfy_Find (key: int) (a: int * (int array)) =                   CakeML’s store. We require that the lengths match, convert-
let                                                                ing between num and int as necessary, and that the locations
   val key = ref key                                               are related through the map m.
   val a = ref a
                                                                         ⊢ lookup m loc = Some loc ′ ⇒
   val i = ref 0
                                                                             val_rel m (ArrV len loc ty)
in
                                                                              (Tuplev [Litv (IntLit (&len)); Loc T loc ′ ])
   (i := 0;
    let fun loop () =                                                Result Relation. The equivalence between Dafny and
       if !i < fst (!a) then (                                     CakeML expression results is built on val_rel:
         if Array.sub (snd (!a), !i) = !key                                                                              def
         then raise Return else ();                                      exp_res_rel m (Rval dfy_v) (Rval [cml_v]) =
         i := !i + 1;                                                     val_rel m dfy_v cml_v
         loop ()                                                     For statements that execute normally in Dafny, we only
       ) else ()                                                   require that the corresponding CakeML expression return
    in                                                             some value. In the case of return, we check that the correct
       loop ();                                                    Return exception has been raised in CakeML:
       i := ~1;                                                                                            def
       raise Return                                                     stmt_res_rel Rcont (Rval v0 ) = T
                                                                                                                      def
    end)                                                                stmt_res_rel (Rstop Sret) (Rerr (Rraise val)) =
   handle Return => !i                                                   is_ret_exn val
end;
                                                                     State Relation. We define the equivalence between a
                                                                   Dafny and CakeML state as follows:
       Figure 3. Result of compiling Find to CakeML
                                                                                                     def
                                                                         state_rel m l s t cml_env =
                                                                          s.clock = t.clock ∧ array_rel m s.heap t.refs ∧
reasons: first, the correctness theorem of the CakeML com-                locals_rel m l s.locals t.refs cml_env.v
piler applies to all programs with well-defined semantics,
regardless of their type correctness. Second, as a valid Dafny        Here, s and t are the Dafny and CakeML states, respec-
program will always assign variables before reading them,          tively. By requiring the clocks to be equal, we can prove that
the generated CakeML program will also have well-defined           a Dafny program diverges if and only if the corresponding
semantics. We will formalize a more general version of this        CakeML program diverges.
argument with the correctness of our compiler in Section 3.2.         The array_rel relation requires that for every array on
   Figure 3 shows the final compilation result for Find.           Dafny’s heap, the mapping m provides the location of the
                                                                   corresponding array on CakeML’s store and additionally
3.2   Compiler Correctness                                         requires that their contents satisfy val_rel.
Informally, our correctness theorem states that evaluating a          The locals_rel relation requires that for every local vari-
Dafny program using Dafny’s functional big-step semantics          able in Dafny, the mapping l provides the corresponding
is equivalent to evaluating the compiled Dafny program             reference in CakeML, which must be bound to the same
using CakeML’s functional big-step semantics, according to         name in the CakeML environment (cml_env). If the local
a notion of equivalence we define.                                 variable is initialized in Dafny, the values must be equivalent
                                                                   with respect to val_rel.
3.2.1 Equivalence. Recall from Section 2 that the func-
tional big-step semantics returns a state and a result. Step-by-      Environment Relation. We define env_rel to specify
step, we will build up our notion of equivalence for values,       both a notion of equivalence between Dafny’s and CakeML’s
results, states, and environment, which we will use for our        environments and additional well-formedness conditions
correctness theorems.                                              on the environments. First, we require the presence of ba-
                                                                   sic functions and constructors such as True, False, and ::
   Value Relation. We define equivalence between Dafny             (cons) in CakeML. Additionally, we require that the pro-
(left) and CakeML (right) values using the inductive val_rel,      gram in Dafny’s environment be well-formed, and for each
                                                                            Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


of its members, the corresponding function must exist in             Note the similarities to the top-level correctness statement.
CakeML’s environment.                                             Here, we prove that evaluating a Dafny statement and its
                                                                  compiled counterpart results in a state and result that are
3.2.2 Compiler Correctness Statement. We formalize                equivalent under their respective relations; we also permit
the correctness statement described informally at the begin-      the CakeML semantics to begin with more clock ticks.
ning of this section:                                                The main difference is that the assumptions of this latter
   ⊢ evaluate_program dfy_ck prog = (s,Rcont) ∧                   statement are more general. In particular, we universally
     compile prog = inr cml_decs ⇒                                quantify over all states and environments that satisfy state_-
      ∃ ck t ′ m′ r_cml.                                          rel and env_rel, respectively. Additionally, we assume the
       evaluate_decs (cml_init_state ffi (dfy_ck + ck))           properties that are established by the freshen pass, namely
         (cml_init_env ffi) cml_decs =                            that variable names are unique and begin with “v”, which is
         (t ′ ,r_cml) ∧                                           captured by is_fresh_stmt and no_shadow. This generality
       state_rel m′ empty s t ′ (cml_init_env ffi) ∧              allows us to prove compiler correctness using the induction
       stmt_res_rel Rcont r_cml                                   principle arising from the termination proof of the functional
                                                                  big-step semantics for Dafny.
   This is a forward simulation result, which suffices to show
that the (deterministic) semantics of Dafny programs are          4     Verified VCG
preserved in the output CakeML programs. Note that the            This section presents our formally verified verification con-
correctness statement only talks about Dafny programs that        dition generator (VCG), which, given a Dafny program, pro-
terminate successfully (Rcont). We can use the VCG to be          duces a list of verification conditions as Dafny expressions.
sure that a given program successfully terminates, which is       Verifying the output expressions shows functional correct-
implied by the correctness of the VCG and the soundness of        ness of Dafny programs and, moreover, guarantees well-
the weakest precondition calculus (Section 4.2). In Section 5,    definedness as assumed by our compiler. A key challenge is
we will combine this fact with the compiler theorem in the        to design the VCG to support sound analysis for loop framing
context of the 91 function. As indicated by the sum value,        and termination, which, in particular, enables verification
the Dafny-to-CakeML compiler can fail, for example, if the        for subtle examples like the 91 function (Fig. 1).
compiler is asked to compile a forall-expression; compiler           We approached the VCG formalization in two phases:
correctness only applies when it succeeded.
   To understand why we existentially quantify over addi-              1. Define a weakest precondition calculus for Dafny as
tional clock ticks ck in the CakeML initial state, recall that            an inductive relation in HOL4 and prove it sound with
state_rel requires Dafny’s and CakeML’s clocks to be the                  respect to the Dafny semantics.
same. However, in some cases it may be necessary to compile            2. Define a concrete VCG implementation function that
Dafny code into CakeML code that requires (finitely) more                 checks the program and emits verification conditions
ticks in the semantics. For example, a Dafny method with 𝑛                as Dafny expressions; this step is proved correct with
parameters is compiled to a curried function, meaning that                respect to the wp-calculus.
a call to that method requires at least one tick in Dafny’s          This two-phase methodology is also applied when extend-
semantics, whereas it requires at least 𝑛 ticks in CakeML’s       ing the wp-calculus with new rules or refining existing ones.
semantics.                                                        By splitting the VCG into a calculus and a function, we can
                                                                  focus on clearly and concisely specifying the wp-rules in the
    Correctness of Statement Compilation. A major com-            calculus while leaving potential performance considerations
ponent of the top-level correctness proof is the correctness of   to the implementation of the VCG function. Mirroring our
the compiler for statements. Omitting some technical details,     development process, we will first describe our calculus and
it is stated as                                                   its soundness, followed by the VCG and its correctness.
 ⊢ evaluate_stmt s env_dfy stmt_dfy = (s′ ,r_dfy) ∧               4.1   Weakest Precondition Calculus
   r_dfy ≠ Rstop (Serr Rfail) ∧
                                                                  We implement the wp-calculus as an 8-place inductive rela-
   from_stmt stmt_dfy lvl = inr e_cml ∧
                                                                  tion for Dafny statements:
   state_rel m l s t env_cml ∧
   env_rel env_dfy env_cml ∧ is_fresh_stmt stmt_dfy ∧                       stmt_wp m reqs stmt post ens decs mods ls
   no_shadow (set (map fst s.locals)) stmt_dfy ⇒                     In order of appearance, the parameters are: the set of avail-
     ∃ ck t ′ m′ r_cml.                                           able methods m, the preconditions reqs, a Dafny statement
      evaluate (t with clock := t.clock + ck) env_cml             stmt, the postconditions post and ens, a termination measure
         [e_cml] = (t ′ ,r_cml) ∧                                 decs, a list of locations that may be modified mods, and a
      state_rel m′ l s′ t ′ env_cml ∧ m ⊑ m′ ∧                    list of defined locals and their types ls. The parameters reqs,
      stmt_res_rel r_dfy r_cml                                    post, ens, decs, and mods are lists of expressions, matching
Verified VCG and Verified Compiler for Dafny


the type of user annotations in the input program. The rules        with the final result being
of our calculus are more easily understood if one considers                      let b = a + a + a in
the parameter reqs as the output and all the other parame-                       let x = b + b + b, y = c in
ters as inputs, which, as we will see later, is mirrored by the                     x < y
implementation of the VCG.
                                                                      Formally, the complete rule for assignment is as follows:
   We distinguish two kinds of postconditions, where the pa-
rameter ens determines the conditions that must hold upon            ⊢ map fst l = map VarLhs ret_names ∧
statement return (i.e., Rstop), while post determines the con-         map snd l = map ExpRhs exps ∧ distinct ret_names ∧
ditions that must hold assuming we continue executing nor-             every (𝜆 v. ¬mem v mods) ret_names ∧
mally (i.e., Rcont). This is necessary to support early-return         length exps = length ret_names ∧
semantics, and the difference is easily illustrated by the def-        set ret_names ⊆ set (map fst ls) ∧
inition of stmt_wp for the Return and Skip cases, which                get_types ls exps = inr rhs_tys ∧
requires their preconditions to be ens and post, respectively:         get_types ls (map Var ret_names) = inr lhs_tys ∧
                                                                       lhs_tys = rhs_tys ⇒
       ⊢ stmt_wp m ens Return post ens decs mods ls
                                                                         stmt_wp m [Let (ZIP (ret_names,exps)) (conj post)]
       ⊢ stmt_wp m post Skip post ens decs mods ls
                                                                           (Assign l) post ens decs mods ls
 We can also easily express the relation in the case of state-
                                                                       The precondition is now a Let expression that binds the
ment composition:
                                                                    names being assigned to their respective expressions in the
   ⊢ stmt_wp m pre1 s1 pre2 ens decs mods ls ∧                      scope of the postcondition. The rule also performs several
     stmt_wp m pre2 s2 post ens decs mods ls ⇒                      syntactic well-formedness and type correctness5 checks on
      stmt_wp m pre1 (Then s1 s2 ) post ens decs mods ls            assignments, which is necessary for soundness; these checks
   The verification condition lists are interpreted conjunc-        are usually added/modified as we discovered their necessity
tively, so to add a verification condition, we can simply           when formalizing soundness of the calculus. We omit further
prepend it to the precondition, as in the case of user as-          discussion of these checks for brevity.
sertions:                                                              Array Update. We also support array updates such as
  ⊢ stmt_wp m (e::post) (Assert e) post ens decs mods ls                                      a[idx] := e;
Note that there is an implicit well-formedness check for               Similar to the assignment rule, the rule for array updates
verification conditions: since they are expressions, to prove       performs several syntactic well-formedness and type cor-
their validity we must show that they evaluate to True in           rectness checks. In particular, it syntactically checks that a
all states, which is impossible if an expression is not well-       is part of the modifies clause. As a consequence, only vari-
formed, as its evaluation would fail in some state.                 ables can be included in the modifies, and not expressions
                                                                    such as a[idx]; we aim to lift this restriction in the future.
   Assign. A classical wp-rule for assignment would per-
                                                                       Omitting some well-formedness checks, the weakest pre-
form variable substitution, which can be tricky to get right,
                                                                    condition for the example above is:
in particular in the presence of parallel assignment. Addi-
tionally, if variables are substituted for large expressions, the               0 <= idx /\ idx < a.Length /\
generated conditions can explode in size [23]. We avoid both                    SetPrev (ForallHeap [a]
of these issues by using a let-expression instead, for which                      (a[Prev idx] = (Prev e) /\
we have defined functional big-step semantics similar to the                       forall i: int ::
assignment statement.                                                                 (i != (Prev idx) /\
   To illustrate this, suppose we want to determine the weak-                          0 <= i /\ i < a.Length ==>
est precondition for the statement                                                        a[i] = PrevHeap (a[i]))
                                                                                   ==> post))
                   b := a + a + a;
                   x, y := b + b + b, c;                            The expressions SetPrev, Prev, PrevHeap, and ForallHeap
                                                                    are our extensions to provide sufficient expressivity for ver-
and the postcondition x < y. In the case of variable substi-
                                                                    ification conditions. The expression ForallHeap quantifies
tution, the intermediate result stemming from Then is
                                                                    over all heaps where previously allocated locations outside
                        b + b + b < c                               a remain unchanged, including heaps with newly allocated
with the final result being                                         locations. More specifically, the argument to ForallHeap is a
       a + a + a + a + a + a + a + a + a < c                        list of locations that are havoced and thus must be a subset
   With our approach of using let, the intermediate result is       of what is provided in the modifies clause. By using Prev
               let x = b + b + b, y = c in                          5While VCG and type checking are typically performed as separate passes,

                 x < y                                              we have combined them into a single phase for this work.
                                                                             Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


and PrevHeap within SetPrev, expressions are evaluated at          method SumToN(n: int) returns (sum: int)
the point of SetPrev, with locals and heap appropriately set.        requires n >= 0
The index must be wrapped in Prev to correctly handle cases          ensures sum == n * (n + 1) / 2
such as a[a[idx]] := a[idx]. Together, the verification              ensures n >= 0
condition frames the unmodified state around the update.           {
                                                                     var i := 1;
   Array Allocation. To understand the wp-rule for array             sum := 0;
allocation, consider
          a := new T[len]; <next statement>                            while i <= n
Observe that the example above is a sequence of statements,              invariant 1 <= i <= n + 1
with the first statement assigning the newly allocated array             invariant sum == (i - 1) * i / 2
to a. This is because the wp-rule for array allocation is a              decreases n - i
special case of the wp-rule for statement composition: sub-            {
sequent statements may modify a, so it must be added to                  sum := sum + i;
the list of locations that the following statement may mod-              i := i + 1;
ify. Note that requiring allocation to be followed by another          }
statement does not limit expressivity: statements only occur       }
in methods, which, as previously mentioned, must explicitly
return using a Return statement, meaning that allocation                        Figure 4. Summing to n in Dafny.
never occurs on its own.
   Again, omitting some well-formedness checks, the weak-
                                                                      Note that in the final conjunct, where we prove the post-
est precondition for the example above is:
                                                                   condition, we only quantify over sum and i, which we have
   0 <= len /\                                                     determined by syntactically checking which locals are as-
   SetPrev (ForallHeap [] (forall a: array<T> ::                   signed to. In particular, we do not quantify over n, effectively
      (a.Length = (Prev len) /\                                    framing the property n >= 0. Since the loop does not include
       let x = (Prev default_e) in                                 a modifies clause, the heap is unchanged.
          (forall i: int ::                                           To ensure that the loop terminates, we need to check
              (0 <= i /\ i < a.Length ==> a[i] = x))               whether the expression in decreases actually decreases. For
       ==> wp_next_stmt)))                                         this, we need to be able to refer to the value of decreases at
Note that it uses the constructs Prev and ForallHeap, which        the beginning of an iteration, which we achieve by storing
were introduced in the context of array updates. However,          that value in fresh variables.
in contrast to array updates, the list passed to ForallHeap is        If we were to explicitly apply this transformation to the
empty, meaning that, except for potentially newly allocated        loop body in Figure 4, we would get
locations, the heap is unchanged. Recall from Section 2.3 that                      var prev_n_i := n - i;
we define arrays to be initialized with some default value.                         sum := sum + i;
This fact is expressed in the verification condition using the                      i := i + 1;
let-expression. Finally, wp_next_stmt is the weakest precon-
                                                                   It should be noted that we do not explicitly apply this trans-
dition of the statement following the allocation. It is the same
                                                                   formation. Instead, the wp-calculus quantifies over a list of
as in the general rule for statement composition, except that
                                                                   variables that are sufficiently unique.
a has been added to its mods.
                                                                      Knowing this, we can now discuss where the decreases
   While. Fundamentally, our definition of the wp-rule for         check happens, namely as part of checking that the invariant
while loops is the same as the standard Hoare Logic rule           is maintained
with annotated invariants. However, our definition must ad-                   i <= n /\ invariant ==> body_wp
ditionally account for termination and framing to ensure that
                                                                   where body_wp represents the weakest precondition of the
the loop preserves properties of variables not modified by
                                                                   loop body and the postcondition
its body. To illustrate these points, consider SumToN (Fig. 4),
which includes the decreases clause automatically guessed                        invariant /\
by the Dafny frontend. Keeping it high-level, the weakest                        n - i < prev_n_i /\
precondition for the while loop is:                                              0 <= prev_n_i /\ 0 <= n - i
        invariant (holds on entry) /\                                 Method Call. The weakest precondition for method calls
        invariant is maintained /\                                 must make sure that the precondition of the call is satis-
        forall sum, i ::                                           fied, recursive calls decrease the termination measure in
           !(i <= n) /\ invariant ==> ensures                      decreases, and that the postcondition of the method call
Verified VCG and Verified Compiler for Dafny


implies the weakest precondition of the rest of the state-          of the decreases clause actually decrease at calls. Otherwise,
ments. An (optional) modifies clause indicates locations on         the callee has a lower level than the caller, and no decreases
the heap that may have changed.                                     clause is required.
   For example, the weakest precondition of the first call in          The soundness proof of methods uses the following sound-
the 91 function (Fig. 1) is                                         ness theorem for the weakest precondition for statements.
   // precondition                                                  One can read this soundness theorem as saying: if reqs holds
   let n = n + 11 in True /\                                        in the initial state st, and all methods in m can be found in
   // decreases                                                     the environment env, then evaluating stmt will terminate
   (let n = n + 11 in 111 - n) < old(111 - n) /\                    and result in a state where post or ens is satisfied, depending
   0 <= (let n = n + 11 in 111 - n) /\                              on whether the statement returns.
   0 <= old(111 - n) /\                                                 ⊢ stmt_wp m reqs stmt post ens decs ls ⇒
   // postcondition implies wp for the rest                               conditions_hold st env reqs ∧
   forall tmp: int ::                                                     compatible_env env m ∧ . . . ⇒
      (let n = n + 11, r = tmp in                                          ∃ st ′ ret.
          r == if n <= 100 then 91 else n - 10)                                eval_stmt st env stmt st ′ ret ∧
       ==> ...                                                                 case ret of
   We can simplify the condition by noticing that, at the                         Rcont ⇒ conditions_hold st ′ env post
method call, n <= 100 holds, and that because the method                       | Rstop Sret ⇒ conditions_hold st ′ env ens
does not update n, we know that old(n) is equal to n.                          | Rstop (Serr v3 ) ⇒ F ∧
   Applying substitution and basic simplification rules to the                 ...
last conjunct, we get:
                                                                    Note that this is a total correctness result—the fact that evalu-
        forall tmp: int ::                                          ating stmt will terminate is hidden in the eval_stmt relation
           tmp == if n <= 89 then 91 else n + 1                     (more details below), which requires there to exist clocks
           ==> ...                                                  such that evaluation does not time out.
By considering the fact that n <= 100, we know that tmp                The soundness theorem above has some of its assumptions
is a number that is between 91 and 101. Hence, it is less           omitted (. . . ) because the assumptions include the lengthy in-
than 111, meaning that the value of 111 - tmp is non-               ductive hypothesis regarding method calls: specifically, that
negative. Considering what we know about tmp from the               we can assume that every method that we might call adheres
postcondition of the call, we also know that it is larger than n.   to its specification if the call is made in a state where the
Thus, the next recursive call will pass the decreases check.        well-founded order used in the method soundness proof has
From the postcondition and the range of tmp, we know that           decreased. The fact that the measure decreases is something
r will be exactly 91, proving the postcondition of the method       we get to know from the verification conditions we generate
for n <= 100.                                                       for each call site.
                                                                       To prove the soundness of stmt_wp, we proceed by in-
4.2   Weakest Precondition Soundness Statement                      duction over the definition of stmt_wp, showing that each
The soundness of our weakest precondition calculus consists         wp-rule is locally sound. For its proof, it is more convenient
of a top-level soundness theorem for methods, which uses a          to work with a relational-style semantics, as opposed to the
soundness result for stmt_wp.                                       functional big-step style used in the compiler proof.
    Informally, the soundness theorem for methods states that          To bridge the relational and functional styles, we defined
if for every method its precondition (requires) implies the         the relations eval_exp and eval_stmt (shown below), which
weakest precondition (stmt_wp) of its method body, then             effectively quotient out the functional big-step clocks in
each method will adhere to its specification whenever started       evaluate_exp and evaluate_stmt, respectively, by existential
from a state satisfying its precondition.                           quantification.
    This top-level method soundness theorem is proved by                                     def
induction on a well-founded order in such a way that we get            eval_exp st env e v =
an inductive hypothesis stating that any method call using              ∃ ck 1 ck 2 .
an input state that is smaller, according to the well-founded            evaluate_exp (st with clock := ck 1 ) env e =
order, behaves according to its specification. The order we                (st with clock := ck 2 ,Rval v)
                                                                                                        def
use is a lexicographic order on the “level” of a method and            eval_stmt st env body st ′ ret =
the values of its decreases clause. The level of a method               ∃ ck 1 ck 2 .
is determined using a topological sort on the call graph of              evaluate_stmt (st with clock := ck 1 ) env body =
a program. Thus, if methods are (mutually) recursive, they                 (st ′ with clock := ck 2 ,ret) ∧
have the same level and may only call each other if the values           ret ≠ Rstop (Serr Rtimeout)
                                                                               Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


This allows us to make further relational big-step-style defini-     wp-rule for array allocation as a special case of statement
tions and also to prove lemmas about these relations. For ex-        composition.
ample, given an expression e, eval_true asserts that there ex-          We proved the correctness of stmt_vcg by showing that
ist clocks such that e evaluates to true; in fact, conditions_hold   it only produces verification conditions that can be derived
(used in the statement of the soundness theorem) is also for-        using the wp-calculus:
mally defined with respect to this relation.
                                                                         ⊢ stmt_vcg m stmt post ens decs mods ls = inr res ⇒
                         def
      eval_true st env e = eval_exp st env e (BoolV T)                      stmt_wp (set m) res stmt post ens decs mods ls
                             def
      conditions_hold st env = every (eval_true st env)                While we have focused on the VCG for statements in this
We can state the relational big-step-style semantics for the         section, our mechanization also includes a formalization of
“then” branch of an if-statement as                                  the VCG for methods. In particular, the generated verification
                                                                     condition for methods requires that the requires clause of
  ⊢ eval_true st env grd ∧ eval_stmt st env thn st1 ret ⇒            a method imply the weakest precondition of the body.
     eval_stmt st env (If grd thn els) st1 ret
Similar relational big-step style lemmas about the definitions       5    Putting It All Together
eval_exp and eval_stmt are used throughout the soundness             To demonstrate that our formally verified tools work in uni-
proof.                                                               son, we have used them to compile and verify the 91 function
                                                                     in an end-to-end manner. As a brief reminder, the complete
4.3    Verified VCG Implementation                                   workflow is as follows.
The final step in our development of a verified VCG for Dafny            1. We use an (untrusted) Dafny frontend to produce an
is to define a function that generates verification conditions.             S-expression for the 91 function.
The implementation follows naturally from the definition                 2. The S-expression is parsed in HOL4, and we use HOL4’s
of the wp-calculus and is written in a result monad. For                    in-logic evaluation to generate verification conditions
example, several clauses of the generator are shown below,                  from stmt_vcg.
corresponding to the wp-calculus snippets defined earlier.               3. Since the verification condition is a Dafny expression,
                                               def
 stmt_vcg m Return post ens decs mods ls = inr ens                          we prove its validity by showing that the expression
                                           def                              evaluates to True in all states. We have mechanized
 stmt_vcg m Skip post ens decs mods ls = inr post                           this proof, which involves expanding the semantics
                                                   def
 stmt_vcg m (Then s1 s2 ) post ens decs mods ls =                           and using HOL4’s decision procedure for integers.
  case dest_ArrayAlloc s1 of                                             4. Finally, we combine the validity of the verification
     None ⇒                                                                 condition, the soundness of the wp-calculus, the cor-
      do                                                                    rectness of the VCG, and the correctness of the com-
        pre′ ← stmt_vcg m s2 post ens decs mods ls;                         piler to prove that the generated CakeML function
        stmt_vcg m s1 pre′ ens decs mods ls                                 satisfies the specification of the 91 function:
      od
                                                                         ⊢ compile_member mccarthy = inr mccarthy_cml ∧
   | Some . . . ⇒ . . .
                                               def                         clos_env_ok clos_env ⇒
 stmt_vcg m (Assert e) post ens decs mods ls =                               AppReturns (INT n)
  inr (e::post)                                                               (Recclosure clos_env [mccarthy_cml] “dfy_M”)
                                                   def
 stmt_vcg m (Assign ass) post ens decs mods ls =                              (INT (if n ≤ 100 then 91 else n − 10))
  let (lhss,rhss) = UNZIP ass                                           The assumption clos_env_ok ensures that basic functions
  in                                                                 and constructors are available to the method, while the predi-
     do                                                              cate AppReturns [14] is defined in the context of the CakeML
      vars ← result_mmap dest_VarLhs lhss;                           translator [47] and best understood as a Hoare triple. Here,
      es ← result_mmap dest_ExpRhs rhss;                             it says that applying the (recursive) closure of the CakeML
      assert (distinct vars)                                         91 function to an input CakeML integer 𝑛 returns a CakeML
        «stmt_vcg:Assign: variables not distinct»;                   integer that is either 91 if 𝑛 ≤ 100 or 𝑛 − 10 otherwise. No-
      assert (list_disjoint vars mods)                               tice that this result is verified entirely for CakeML program
        «stmt_vcg:Assign: assigning to mods»;                        semantics and does not involve the Dafny toolchain(s).
      ...                                                               We can apply both the compiler and the VCG to other
      inr [Let (ZIP (vars,es)) (conj post)]                          methods, including the previously presented methods Swap,
     od                                                              Find, and SumToN. Out of these methods, we have also proved
Note that in the case of Then, we split on whether the first         the validity of the verification condition for Swap. We have
statement allocates an array, matching our description of the        not attempted to prove the verification conditions of the
Verified VCG and Verified Compiler for Dafny


other methods, as the manual approach does not scale well.          mechanized in F*. There has also been work on embedding
Our aim is to improve this in future work by adding a path          a subset of the x64 assembly language in F* [25], which in-
to SMT, allowing the use of SMT solvers to automatically            cludes an embedding of Vale [10], an automated verifier for
prove the validity of verification conditions.                      high-performance assembly code that builds on top of exist-
   Similarly, we hope to minimize the proof effort needed           ing verification languages like Dafny and F*, and a verified
to carry the functional correctness guarantees of verified          and efficient VCG. To our knowledge, these embeddings have
Dafny methods to their CakeML counterparts, as we have              not been verified in a foundational proof assistant.
manually done for the 91 function.
                                                                    Why3 and Why. Why3 [21] is a platform for deductive pro-
                                                                    gram verification. It provides an ML dialect called WhyML
6     Related Work                                                  for which it can generate verification conditions. Unlike
We start with an overview of related work at the intersection       Dafny, it does not automatically discharge the generated
of formalization and verification-aware programming plat-           verification conditions. Instead, users can choose between
forms like Dafny, F*, and Why/Why3. This is followed by a           automated and interactive provers. To generate simpler ver-
discussion of the broader literature on verified compilation        ification conditions, it statically controls aliasing using its
and verified verification condition generation/checking.            type system [22]. Why is a verification condition generator
                                                                    for a “WHILE” language [20]. Similar to Why3, Why can
6.1   Verified Verification-Aware Programming                       output its verification condition to automated and interac-
Dafny. To the best of our knowledge, verification condition         tive provers. It has inspired work by Herms et al. [31], where
generation and compilation for Dafny has not been done              they have implemented a VCG that can produce verification
in a foundational way before. Nezamabadi and Myreen [48]            conditions for multiple provers and proven it sound in Rocq.
implemented a Dafny-to-CakeML compiler for a subset of
Dafny that is larger than the one we present here, but only         6.2   Verified Compilation and Verified Verification
proved correctness for the compilation of some binary ex-                 Condition Generation
pressions. There have also been efforts to implement Dafny’s        Combining Compilation and Verification. The Verified
compilers in Dafny [16], with the initial target being a purely     Software Toolchain (VST) [4] project combines CompCert
functional subset of Dafny.                                         with static analysis tools for invariant generation and verified
   Dafny targets the intermediate verification language Boo-        invariant checking for an end-to-end verified toolchain for
gie [6, 40] in order to generate verification conditions; there     C programs. It has been used, for example, to verify the
has been work by Parthasarathy et al. [50] on validating            OpenSSL implementation of SHA-256 [5] and HMAC with
Boogie’s outputs using Isabelle/HOL.                                SHA-256 [8].
   Gladshtein et al. [27] present a framework for founda-              CakeML provides a verified implementation of Character-
tional, multi-modal program verifiers, which they instantiate,      istic Formulae for ML [15, 19, 30, 51], which allows users to
among other things, to reason about Dafny-style programs.           state specifications in the style of separation logic and prove
In contrast to the deep embedding presented in this work,           them correct using tactics within HOL4.
they use a monadic shallow embedding in Lean.                          seL4 [36] is a verified microkernel written in C that has
                                                                    been formalized in Isabelle/HOL. Its compilation down to
F*. F* [57] is a proof-oriented programming language that,
                                                                    machine code has been proven correct using a translation
like Dafny, supports automated reasoning about programs
                                                                    validation approach [55]. More specifically, it makes use of
using SMT solvers. However, while Dafny mostly follows
                                                                    a proof-producing decompilation of the binary [45, 46], a
an imperative style, F* encourages a higher-order functional
                                                                    formalization of the machine architecture [24], and SMT
programming with effects style and has a dependent type
                                                                    solvers to show that the binary is a refinement of its C se-
system. Strub et al. [56] have implemented a type checker
                                                                    mantics. It has also made extensive use of the VCG provided
for F* in F* that returns type derivations. In particular, it can
                                                                    by Simpl to prove refinement between its executable, monad
return the type derivation for typechecking itself, which in
                                                                    specification, and high-performance C implementation [63].
turn can be checked in Rocq.
   F* is also a popular target for embedding domain-specific        Verification Condition Generation. Over the years, there
programming languages: Low* [53] is a low-level program-            have been multiple works on verification condition genera-
ming language that is shallowly embedded into F* and has            tion that were built as tactics in interactive theorem provers
a paper formalization of extracting it to Clight [9], which         such as HOL or Isabelle: Gordon [28] presented a shallow
can be compiled by the CompCert [42] compiler, a verified C         embedding of a simple imperative language, for which he
compiler that has been formalized in Rocq. Steel [26] is a con-     mechanically derived a Hoare logic and developed tactics to
current programming language that is shallowly embedded             generate verification conditions.
into F*. It is based on the concurrent separation logic Steel-         Agerholm [2] presented a shallow embedding of an imper-
Core [58] and has verified verification condition generation        ative language with non-determinism and loops, for which
                                                                             Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


he formalized weakest precondition semantics and imple-          Future Work
mented a verification condition generator using tactics.         Beyond the contributions described in this paper, we believe
   Homeier and Martin [32] presented a deep embedding of a       that our work provides a scaffolding that can be expanded
standard while loop language including expressions with side     in different directions: feature support, automation, and in-
effects, for which they proved sound axiomatic semantics and     tegration with the CakeML ecosystem.
used the axiomatic semantics to define a verified verification      By improving feature support and automation, we can
condition generator.                                             bring our implementation closer to a drop-in replacement
   Huisman and Jacobs [33] formalized the semantics of an        for the current Dafny toolchain. Initial steps in this regard
imperative language including loops and abrupt termination       could be to support Dafny’s compiler litmus test suite and
(e.g., return and continue) in higher-order logic, provided      to implement and verify a connection to SMT, allowing the
an extension of Hoare logic with abrupt termination, and         use of automatic SMT solvers. Supporting Dafny’s compiler
used it in the context of Java with the proof tool PVS. Its      litmus test suite will most likely involve building support
approach is reminiscent of our combination of functional         for Dafny’s object-oriented features (traits and classes) as
big-step semantics and a weakest precondition calculus.          well as functional features (first-class function values and
   Schirmer [54] presented Simpl, a model for sequential im-     algebraic data types). The latter features have straightfor-
perative programming languages, including a proven sound         ward compilation targets in CakeML, and ideas to compile
and complete Hoare logic for both partial and total correct-     traits and classes have been very briefly sketched in previous
ness and a verification condition generator embedded as an       work [48].
Isabelle tactic.                                                    Furthermore, a deeper integration of our work with the
   There has also been work on verifying optimized verifi-       CakeML ecosystem could allow CakeML code to call Dafny
cation condition generation: Vogels et al. [62] used Rocq to     code, and vice versa. Thus, it may enable the input and out-
formalize an efficient VC generation algorithm [23, 39] that     put of Dafny programs to be placed on solid foundations.
avoids an exponential blowup. Grégoire and Sacchini [29]         More generally, a program could simultaneously make use
formalized in Rocq the use of static analysis to simplify gen-   of Dafny’s verification automation, CakeML’s HOL4 fron-
erated verification conditions for Java bytecode.                tend [1, 47], and Hoare-style reasoning using separation
Verified End-to-End Compilers. PureCake [35] is a veri-          logic [19, 30, 51], without compromising on trustworthiness.
fied compiler for a Haskell-like language, which, similar to
our Dafny compiler, is built on top of CakeML. Pancake [52]      Acknowledgments
is a systems programming language with a verified compiler,      We thank Clément Pit-Claudel for early discussions of this
which reuses the lower parts of the CakeML backend.              work, Fabio Madge for answering our questions about Dafny,
   CertiCoq [3] compiles Gallina, the specification language     Rustan Leino for discussions about Dafny at LICS 2025, and
of Rocq, to C, which can be compiled using CompCert to form      the anonymous reviewers for their comments. This work
an end-to-end verified compiler. Note that while CertiCoq’s      was supported by an Amazon Research Award and NTU
components have been verified, proving a composed end-to-        Singapore’s Global Connect Fellowship. The second author
end correctness theorem is still ongoing work [37].              was partially funded by Swedish Research Council grant
   Vélus [11] is a verified compiler for synchronous dataflow    2021-05165.
languages like Lustre [12] and is built on top of CompCert.
   In the context of the CompCert project, the translation       References
validation approach has been employed for an SSA-based            [1] Oskar Abrahamsson, Son Ho, Hrutvik Kanabar, Ramana Kumar, Mag-
middle-end [7], instruction scheduling [60], and software             nus O. Myreen, Michael Norrish, and Yong Kiam Tan. 2020. Proof-
pipelining [61].                                                      Producing Synthesis of CakeML from Monadic HOL Functions. J. Au-
                                                                      tom. Reason. 64, 7 (2020), 1287–1306. doi:10.1007/S10817-020-09559-8
                                                                  [2] Sten Agerholm. 1991. Mechanizing Program Verification in HOL.
7   Conclusion                                                        In 1991 International Workshop on the HOL Theorem Proving System
We have presented a verified compiler and verified verifica-          and its Applications, Myla Archer, Jeffrey J. Joyce, Karl N. Levitt, and
tion condition generator based on functional big-step seman-          Phillip J. Windley (Eds.). IEEE Computer Society, 208–222.
                                                                  [3] Abhishek Anand, Andrew W. Appel, Greg Morrisett, Zoe
tics for an imperative subset of Dafny. Our subset includes           Paraskevopoulou, Randy Pollack, Olivier Savary Bélanger, Matthieu
mutually recursive method calls, while loops, and arrays,             Sozeau, and Matthew Weaver. 2017. CertiCoq: A verified compiler
which is expressive enough to support interesting examples            for Coq. In The third international workshop on Coq for programming
such as McCarthy’s 91 function and array-based programs               languages (CoqPL).
that are used when teaching Dafny. Together, our formaliza-       [4] Andrew W. Appel. 2011. Verified Software Toolchain - (Invited Talk).
                                                                      In ESOP (LNCS, Vol. 6602), Gilles Barthe (Ed.). Springer, 1–17. doi:10.
tion shows that it is possible to obtain foundational correct-        1007/978-3-642-19718-5_1
ness guarantees across the entire toolchain for verification-     [5] Andrew W. Appel. 2015. Verification of a Cryptographic Primitive:
aware programming languages.                                          SHA-256. ACM Trans. Program. Lang. Syst. 37, 2 (2015), 7:1–7:31.
Verified VCG and Verified Compiler for Dafny


     doi:10.1145/2701415                                                           (Eds.). Springer, 173–177. doi:10.1007/978-3-540-73368-3_21
 [6] Michael Barnett, Bor-Yuh Evan Chang, Robert DeLine, Bart Jacobs,         [21] Jean-Christophe Filliâtre and Andrei Paskevich. 2013. Why3 - Where
     and K. Rustan M. Leino. 2005. Boogie: A Modular Reusable Verifier for         Programs Meet Provers. In ESOP (LNCS, Vol. 7792), Matthias Felleisen
     Object-Oriented Programs. In FMCO (LNCS, Vol. 4111), Frank S. de Boer,        and Philippa Gardner (Eds.). Springer, 125–128. doi:10.1007/978-3-
     Marcello M. Bonsangue, Susanne Graf, and Willem P. de Roever (Eds.).          642-37036-6_8
     Springer, 364–387. doi:10.1007/11804192_17                               [22] Jean-Christophe Filliâtre, Léon Gondelman, and Andrei Paskevich.
 [7] Gilles Barthe, Delphine Demange, and David Pichardie. 2014. Formal            2016. A Pragmatic Type System for Deductive Verification. (2016).
     Verification of an SSA-Based Middle-End for CompCert. ACM Trans.              https://inria.hal.science/hal-01256434
     Program. Lang. Syst. 36, 1 (2014), 4:1–4:35. doi:10.1145/2579080         [23] Cormac Flanagan and James B. Saxe. 2001. Avoiding exponential
 [8] Lennart Beringer, Adam Petcher, Katherine Q. Ye, and Andrew W.                explosion: generating compact verification conditions. In POPL, Chris
     Appel. 2015. Verified Correctness and Security of OpenSSL HMAC.               Hankin and Dave Schmidt (Eds.). ACM, 193–205. doi:10.1145/360204.
     In USENIX Security, Jaeyeon Jung and Thorsten Holz (Eds.). USENIX             360220
     Association, 207–221.                                                    [24] Anthony C. J. Fox and Magnus O. Myreen. 2010. A Trustworthy
 [9] Sandrine Blazy and Xavier Leroy. 2009. Mechanized Semantics for               Monadic Formalization of the ARMv7 Instruction Set Architecture. In
     the Clight Subset of the C Language. J. Autom. Reason. 43, 3 (2009),          ITP (LNCS, Vol. 6172), Matt Kaufmann and Lawrence C. Paulson (Eds.).
     263–288. doi:10.1007/S10817-009-9148-3                                        Springer, 243–258. doi:10.1007/978-3-642-14052-5_18
[10] Barry Bond, Chris Hawblitzel, Manos Kapritsos, K. Rustan M. Leino,       [25] Aymeric Fromherz, Nick Giannarakis, Chris Hawblitzel, Bryan Parno,
     Jacob R. Lorch, Bryan Parno, Ashay Rane, Srinath T. V. Setty, and             Aseem Rastogi, and Nikhil Swamy. 2019. A verified, efficient embed-
     Laure Thompson. 2017. Vale: Verifying High-Performance Crypto-                ding of a verifiable assembly language. Proc. ACM Program. Lang. 3,
     graphic Assembly Code. In USENIX Security, Engin Kirda and Thomas             POPL (2019), 63:1–63:30. doi:10.1145/3290376
     Ristenpart (Eds.). USENIX Association, 917–934.                          [26] Aymeric Fromherz, Aseem Rastogi, Nikhil Swamy, Sydney Gibson,
[11] Timothy Bourke, Lélio Brun, Pierre-Évariste Dagand, Xavier Leroy,             Guido Martínez, Denis Merigoux, and Tahina Ramananandro. 2021.
     Marc Pouzet, and Lionel Rieg. 2017. A formally verified compiler              Steel: proof-oriented programming in a dependently typed concurrent
     for Lustre. In PLDI, Albert Cohen and Martin T. Vechev (Eds.). ACM,           separation logic. Proc. ACM Program. Lang. 5, ICFP (2021), 1–30.
     586–601. doi:10.1145/3062341.3062358                                          doi:10.1145/3473590
[12] Paul Caspi, Daniel Pilaud, Nicolas Halbwachs, and John Plaice. 1987.     [27] Vladimir Gladshtein, George Pîrlea, Qiyuan Zhao, Vitaly Kurin, and
     Lustre: A Declarative Language for Programming Synchronous Sys-               Ilya Sergey. 2026. Foundational Multi-Modal Program Verifiers. Proc.
     tems. In POPL. ACM Press, 178–188. doi:10.1145/41625.41641                    ACM Program. Lang. POPL. To appear.
[13] Aleks Chakarov, Jaco Geldenhuys, Matthew Heck, Michael Hicks,            [28] Michael J. C. Gordon. 1989. Mechanizing Programming Logics in Higher
     Sam Huang, Georges-Axel Jaloyan, Anjali Joshi, K. Rustan M. Leino,            Order Logic. Springer, New York, NY, 387–439. doi:10.1007/978-1-
     Mikael Mayer, Sean McLaughlin, Akhilesh Mritunjai, Clément Pit-               4612-3658-0_10
     Claudel, Sorawee Porncharoenwase, Florian Rabe, Marianna Rapoport,       [29] Benjamin Grégoire and Jorge Luis Sacchini. 2007. Combining a Ver-
     Giles Reger, Cody Roux, Neha Rungta, Robin Salkeld, Matthias                  ification Condition Generator for a Bytecode Language with Static
     Schlaipfer, Daniel Schoepe, Johanna Schwartzentruber, Serdar Tasiran,         Analyses. In TGC (LNCS, Vol. 4912), Gilles Barthe and Cédric Fournet
     Aaron Tomb, Emina Torlak, Jean-Baptiste Tristan, Lucas G. Wag-                (Eds.). Springer, 23–40. doi:10.1007/978-3-540-78663-4_4
     ner, Michael W. Whalen, Remy Willems, Tongtong Xiang, Tae Joon           [30] Armaël Guéneau, Magnus O. Myreen, Ramana Kumar, and Michael
     Byun, Joshua M. Cohen, Ruijie Fang, Junyoung Jang, Jakob Rath,                Norrish. 2017. Verified Characteristic Formulae for CakeML. In ESOP
     Hira Taqdees Syeda, Dominik Wagner, and Yongwei Yuan. 2025. For-              (LNCS, Vol. 10201), Hongseok Yang (Ed.). Springer, 584–610. doi:10.
     mally Verified Cloud-Scale Authorization. In ICSE. IEEE, 2508–2521.           1007/978-3-662-54434-1_22
     doi:10.1109/ICSE55347.2025.00166                                         [31] Paolo Herms, Claude Marché, and Benjamin Monate. 2012. A Certi-
[14] Arthur Charguéraud. 2010. Characteristic formulae for mechanized              fied Multi-prover Verification Condition Generator. In VSTTE (LNCS,
     program verification. Ph. D. Dissertation. Université Paris Diderot.          Vol. 7152), Rajeev Joshi, Peter Müller, and Andreas Podelski (Eds.).
[15] Arthur Charguéraud. 2011. Characteristic formulae for the verification        Springer, 2–17. doi:10.1007/978-3-642-27705-4_2
     of imperative programs. In ICFP, Manuel M. T. Chakravarty, Zhenjiang     [32] Peter V. Homeier and David F. Martin. 1994. Trustworthy Tools for
     Hu, and Olivier Danvy (Eds.). ACM, 418–430. doi:10.1145/2034773.              Trustworthy Programs: A Verified Verification Condition Generator.
     2034828                                                                       In Higher Order Logic Theorem Proving and Its Applications, 7th Inter-
[16] Dafny. [n. d.]. compiler-bootstrap. https://github.com/dafny-lang/            national Workshop, Proceedings (LNCS, Vol. 859), Thomas F. Melham
     compiler-bootstrap.                                                           and Juanito Camilleri (Eds.). Springer, 269–284. doi:10.1007/3-540-
[17] Leonardo Mendonça de Moura and Nikolaj S. Bjørner. 2008. Z3: An               58450-1_48
     Efficient SMT Solver. In TACAS (LNCS, Vol. 4963), C. R. Ramakrishnan     [33] Marieke Huisman and Bart Jacobs. 2000. Java Program Verification
     and Jakob Rehof (Eds.). Springer, 337–340. doi:10.1007/978-3-540-             via a Hoare Logic with Abrupt Termination. In FASE (LNCS, Vol. 1783),
     78800-3_24                                                                    T. S. E. Maibaum (Ed.). Springer, 284–303. doi:10.1007/3-540-46428-
[18] Alastair F. Donaldson, Dilan Sheth, Jean-Baptiste Tristan, and Alex           X_20
     Usher. 2024. Randomised Testing of the Compiler for a Verification-      [34] Ahmed Irfan, Sorawee Porncharoenwase, Zvonimir Rakamaric, Neha
     Aware Programming Language. In ICST. IEEE, 407–418. doi:10.1109/              Rungta, and Emina Torlak. 2022. Testing Dafny (experience paper). In
     ICST60714.2024.00044                                                          ISSTA, Sukyoung Ryu and Yannis Smaragdakis (Eds.). ACM, 556–567.
[19] Hugo Férée, Johannes Åman Pohjola, Ramana Kumar, Scott Owens,                 doi:10.1145/3533767.3534382
     Magnus O. Myreen, and Son Ho. 2018. Program Verification in the          [35] Hrutvik Kanabar, Samuel Vivien, Oskar Abrahamsson, Magnus O.
     Presence of I/O - Semantics, Verified Library Routines, and Verified          Myreen, Michael Norrish, Johannes Åman Pohjola, and Riccardo
     Applications. In VSTTE (LNCS, Vol. 11294), Ruzica Piskac and Philipp          Zanetti. 2023. PureCake: A Verified Compiler for a Lazy Functional
     Rümmer (Eds.). Springer, 88–111. doi:10.1007/978-3-030-03592-1_6              Language. Proc. ACM Program. Lang. 7, PLDI, 952–976. doi:10.1145/
[20] Jean-Christophe Filliâtre and Claude Marché. 2007.                The         3591259
     Why/Krakatoa/Caduceus Platform for Deductive Program Verifica-           [36] Gerwin Klein, June Andronick, Kevin Elphinstone, Gernot Heiser,
     tion. In CAV (LNCS, Vol. 4590), Werner Damm and Holger Hermanns               David A. Cock, Philip Derrin, Dhammika Elkaduwe, Kai Engelhardt,
                                                                                            Daniel Nezamabadi, Magnus O. Myreen, and Yong Kiam Tan


     Rafal Kolanski, Michael Norrish, Thomas Sewell, Harvey Tuch, and                McLaughlin, Remy Seassau, Magnus O. Myreen, Michael Norrish, and
     Simon Winwood. 2010. seL4: formal verification of an operating-                 Gernot Heiser. 2023. Pancake: Verified Systems Programming Made
     system kernel. Commun. ACM 53, 6 (2010), 107–115. doi:10.1145/                  Sweeter. In PLOS. ACM, 1–9. doi:10.1145/3623759.3624544
     1743546.1743574                                                            [53] Jonathan Protzenko, Jean Karim Zinzindohoué, Aseem Rastogi, Tahina
[37] Joomy Korkut, Kathrin Stark, and Andrew W. Appel. 2025. A Verified              Ramananandro, Peng Wang, Santiago Zanella-Béguelin, Antoine
     Foreign Function Interface between Coq and C. Proc. ACM Program.                Delignat-Lavaud, Catalin Hritcu, Karthikeyan Bhargavan, Cédric Four-
     Lang. 9, POPL (2025), 687–717. doi:10.1145/3704860                              net, and Nikhil Swamy. 2017. Verified low-level programming em-
[38] Ramana Kumar, Magnus O. Myreen, Michael Norrish, and Scott Owens.               bedded in F. Proc. ACM Program. Lang. 1, ICFP (2017), 17:1–17:29.
     2014. CakeML: a verified implementation of ML. In POPL, Suresh                  doi:10.1145/3110261
     Jagannathan and Peter Sewell (Eds.). ACM, 179–192. doi:10.1145/            [54] Norbert Schirmer. 2006. Verification of sequential imperative pro-
     2535838.2535841                                                                 grams in Isabelle-HOL. Ph. D. Dissertation. Technical University
[39] K. Rustan M. Leino. 2005. Efficient weakest preconditions. Inf. Process.        Munich, Germany. http://mediatum.ub.tum.de/mediatum/servlets/
     Lett. 93, 6 (2005), 281–288. doi:10.1016/J.IPL.2004.10.015                      TUMDistributionServlet?id=mediaTUM_derivate_000000000002972
[40] K. Rustan M. Leino. 2008. This is Boogie 2. (June 2008). https://www.      [55] Thomas Arthur Leck Sewell, Magnus O. Myreen, and Gerwin Klein.
     microsoft.com/en-us/research/publication/this-is-boogie-2-2/                    2013. Translation validation for a verified OS kernel. In PLDI, Hans-
[41] K. Rustan M. Leino. 2010. Dafny: An Automatic Program Verifier for              Juergen Boehm and Cormac Flanagan (Eds.). ACM, 471–482. doi:10.
     Functional Correctness. In LPAR (LNCS, Vol. 6355), Edmund M. Clarke             1145/2491956.2462183
     and Andrei Voronkov (Eds.). Springer, 348–370. doi:10.1007/978-3-          [56] Pierre-Yves Strub, Nikhil Swamy, Cédric Fournet, and Juan Chen.
     642-17511-4_20                                                                  2012. Self-certification: bootstrapping certified typecheckers in F*
[42] Xavier Leroy. 2009. Formal verification of a realistic compiler. Com-           with Coq. In POPL, John Field and Michael Hicks (Eds.). ACM, 571–
     mun. ACM 52, 7 (2009), 107–115. doi:10.1145/1538788.1538814                     584. doi:10.1145/2103656.2103723
[43] Zohar Manna and John McCarthy. 1969. PROPERTIES OF PROGRAMS                [57] Nikhil Swamy, Catalin Hritcu, Chantal Keller, Aseem Rastogi, Antoine
     AND PARTIAL FUNCTION LOGIC.                                                     Delignat-Lavaud, Simon Forest, Karthikeyan Bhargavan, Cédric Four-
[44] Robin Milner, Mads Tofte, and David Macqueen. 1997. The Definition              net, Pierre-Yves Strub, Markulf Kohlweiss, Jean Karim Zinzindohoue,
     of Standard ML. MIT Press, Cambridge, MA, USA.                                  and Santiago Zanella-Béguelin. 2016. Dependent types and multi-
[45] Magnus O. Myreen, Michael J. C. Gordon, and Konrad Slind. 2008.                 monadic effects in F. In POPL, Rastislav Bodík and Rupak Majumdar
     Machine-Code Verification for Multiple Architectures - An Applica-              (Eds.). ACM, 256–270. doi:10.1145/2837614.2837655
     tion of Decompilation into Logic. In FMCAD, Alessandro Cimatti and         [58] Nikhil Swamy, Aseem Rastogi, Aymeric Fromherz, Denis Merigoux,
     Robert B. Jones (Eds.). IEEE, 1–8. doi:10.1109/FMCAD.2008.ECP.24                Danel Ahman, and Guido Martínez. 2020. SteelCore: an extensible
[46] Magnus O. Myreen, Michael J. C. Gordon, and Konrad Slind. 2012.                 concurrent separation logic for effectful dependently typed programs.
     Decompilation into logic - Improved. In FMCAD, Gianpiero Cabodi                 Proc. ACM Program. Lang. 4, ICFP (2020), 121:1–121:30. doi:10.1145/
     and Satnam Singh (Eds.). IEEE, 78–81.                                           3409003
[47] Magnus O. Myreen and Scott Owens. 2014. Proof-producing transla-           [59] Yong Kiam Tan, Magnus O. Myreen, Ramana Kumar, Anthony C. J.
     tion of higher-order logic into pure and stateful ML. J. Funct. Program.        Fox, Scott Owens, and Michael Norrish. 2019. The verified CakeML
     24, 2-3 (2014), 284–315. doi:10.1017/S0956796813000282                          compiler backend. J. Funct. Program. 29 (2019), e2. doi:10.1017/
[48] Daniel Nezamabadi and Magnus Myreen. 2025. Baking for Dafny: A                  S0956796818000229
     CakeML Backend for Dafny. CoRR abs/2501.05111 (2025). doi:10.48550/        [60] Jean-Baptiste Tristan and Xavier Leroy. 2008. Formal verification of
     ARXIV.2501.05111 arXiv:2501.05111 Accepted to the Dafny workshop                translation validators: a case study on instruction scheduling opti-
     at POPL 2025.                                                                   mizations. In POPL, George C. Necula and Philip Wadler (Eds.). ACM,
[49] Scott Owens, Magnus O. Myreen, Ramana Kumar, and Yong Kiam Tan.                 17–27. doi:10.1145/1328438.1328444
     2016. Functional Big-Step Semantics. In ESOP (LNCS, Vol. 9632), Peter      [61] Jean-Baptiste Tristan and Xavier Leroy. 2010. A simple, verified val-
     Thiemann (Ed.). Springer, 589–615. doi:10.1007/978-3-662-49498-1_23             idator for software pipelining. In POPL, Manuel V. Hermenegildo and
[50] Gaurav Parthasarathy, Peter Müller, and Alexander J. Summers. 2021.             Jens Palsberg (Eds.). ACM, 83–92. doi:10.1145/1706299.1706311
     Formally Validating a Practical Verification Condition Generator. In       [62] Frédéric Vogels, Bart Jacobs, and Frank Piessens. 2010. A machine-
     CAV (LNCS, Vol. 12760), Alexandra Silva and K. Rustan M. Leino (Eds.).          checked soundness proof for an efficient verification condition gen-
     Springer, 704–727. doi:10.1007/978-3-030-81688-9_33                             erator. In SAC, Sung Y. Shin, Sascha Ossowski, Michael Schumacher,
[51] Johannes Åman Pohjola, Henrik Rostedt, and Magnus O. Myreen. 2019.              Mathew J. Palakal, and Chih-Cheng Hung (Eds.). ACM, 2517–2522.
     Characteristic Formulae for Liveness Properties of Non-Terminating              doi:10.1145/1774088.1774610
     CakeML Programs. In ITP (LIPIcs, Vol. 141), John Harrison, John            [63] Simon Winwood, Gerwin Klein, Thomas Sewell, June Andronick,
     O’Leary, and Andrew Tolmach (Eds.). Schloss Dagstuhl - Leibniz-                 David A. Cock, and Michael Norrish. 2009. Mind the Gap. In TPHOLs
     Zentrum für Informatik, 32:1–32:19. doi:10.4230/LIPICS.ITP.2019.32              (LNCS, Vol. 5674), Stefan Berghofer, Tobias Nipkow, Christian Urban,
[52] Johannes Åman Pohjola, Hira Taqdees Syeda, Miki Tanaka, Krishnan                and Makarius Wenzel (Eds.). Springer, 500–515. doi:10.1007/978-3-
     Winter, Tsun Wang Sau, Benjamin Nott, Tiana J. Tsang Ung, Craig                 642-03359-9_34
