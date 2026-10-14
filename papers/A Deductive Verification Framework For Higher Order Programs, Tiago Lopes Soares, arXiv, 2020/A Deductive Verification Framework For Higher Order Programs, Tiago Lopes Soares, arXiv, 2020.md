                                          A Deductive Verification Framework For Higher
                                                        Order Programs

                                                                      Tiago Soares — 52965
                                                         Supervisors: Mário Pereira and António Ravara
arXiv:2011.14044v1 [cs.LO] 28 Nov 2020




                                                                tl.soares@campus.fct.unl.pt

                                                      NOVA LINCS & DI, FCT, Universidade Nova de Lisboa



                                               Abstract. In this report, we present the preliminary work developed
                                               for our research project for the APDC (Área Prática de Desenvolvimento
                                               Curricular ) course. The main goal of this project is to develop a frame-
                                               work, on top of the Why3 tool, for the verification of effectful higher-
                                               order programs. We use defunctionalization as an intermediate transfor-
                                               mation from higher-order OCaml implementations into first order ones.
                                               The target for our translation is WhyML, the Why3’s programming lan-
                                               guage. We believe defunctionalization can be an interesting route for the
                                               automated verification of higher-order programs, since one can employ
                                               off-the-shelf automated program verifiers to prove the correctness of the
                                               generated first-order program. This report also serves to introduce the
                                               reader to the subject of deductive program verification and some of the
                                               tools and concepts used to prove higher order effectful programs.

                                               Keywords: Deductive Software Verification · Imperative Programs ·
                                               Defunctionalization · Why3 · OCaml


                                         1   Introduction

                                         Producing error free code for a complex system is, regardless of the programmer’s
                                         skills, a herculean task. Customarily, the only weapons we have to combat the
                                         plethora of bugs rotting away our code are tests and plenty of caution. But
                                         caution can only get you so far and program testing, in Dijkstra’s words, "can
                                         be a very effective way to show the presence of bugs, but is hopelessly inadequate
                                         for showing their absence" [6]. Therefore, in order to make sure that our code
                                         does what we want, we need formal proofs of its correctness.
                                             There is no one definition of correctness, however, considering it depends
                                         on how we want to specify our program. We might simply want to make sure
                                         that there are no runtime errors involving type safety, arithmetic overflows or
                                         unhandled exceptions. We might also want to prove that the program eventually
                                         terminates. More generally, we might want to prove some relation to its input
                                         and/or the state with its output. For each definition of correctness there are
                                         better ways of proving it. For the class of programs we will analyse, that is,
                                         functional programs, the best alternative is deductive verification. [7]
2       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

    Dispatching proofs for imperative implementations can be challenging, as
they heavily rely on modifying data structures after they have been created,
which can be hard to model using first order logic. Therefore, writing in a pro-
gramming language that stays as close as possible to logical definitions, that is,
a functional language, means we will have an easier time identifying the nec-
essary assertions to create an adequate proof. OCaml is a good candidate for
writing effectful, verifiable code, not only because it is primarily a functional
language, but also because it allows us to use imperative constructs, such as
mutable records.
    To write specifications for code with side effects, we need additional in-
frastructure on top of first order logic. One of the most popular is Separation
Logic [17], which allows us to connect physical memory to logical statements.
Although it is very expressive, its intrinsic technicalities prevent it from being
widely adopted. In this work, we will be using GOSPEL (Generic OCaml SPEc-
ification Language) [2], which is built on top of Separation Logic, as a higher
level alternative to define changes in the heap and, to prove the specification, we
will use Why3 [9], a program verifier tailored towards automated verification.
    But effectful code is only one half of this project; the other being higher-order
functions. As previously said, code with side effects can be difficult to map onto
logical definitions, but this problem becomes exponentially more complex when
these effects originate from first class functions, due to the way programs are
proved. In short, we annotate them with pre and postconditions and check that
an implementation conforms to the provided specification. This is normally done
by employing some technique of verification conditions generation, such as Dijk-
stra Weakest Precondition Calculus [5]. However, if we don’t know the behaviour
of a part of our routine, and this unknown part might alter our program’s state,
then it can be hard to prove if a given program is correct.
    Some work has been put into bringing closer automated verification and
higher-order programs with effects, such as the tool Who [12]. Nonetheless, a
framework of that caliber can be complex to implement and maintain. Another
option would be Iris [11], one of the most powerful tools available in the realm
of program verification, but whose power comes at a cost. The logic employed
by it is, albeit very rich, extremely complex and almost inaccessible to anyone
without years of training in the field. In addition, there is no way to automate
proofs with it, this being the main reason why Iris falls out of the scope of our
project.
    Most options available for handling this problem present their own hin-
drances, such as, for example, their complexity, cross-compatibility and their
practical usefulness [13, Sec. 3.4]. We have put forth a small contribution to solve
these limitations by creating a Why3 plugin which makes use of defunctional-
ization [4, 16] to handle the verification of such programs. Defunctionalization
works by translating a higher-order implementation into an equivalent first-order
counterpart. We believe this technique can open the door to automatic verifi-
cation of higher-order code, since we can use an existing first-order verifier to
prove the defunctionalized program.
            A Deductive Verification Framework For Higher Order Programs           3

    Previous work studied the combination of defunctionalization and software
verification. [14]. However, no prototype was developed and all examples were
made entirely by hand. In this project, we lay the groundwork for a fully-fledged
verification framework for effectful higher-order programs, by exploring the tech-
nique of defunctionalization. To the best of our knowledge, this is the first prac-
tical implementation of defunctionalization as a proof technique. Our framework
will accept as input a higher-order program, annotated with assertions written
in GOSPEL, translate it into a first-order equivalent WhyML program so that
we can use Why3 to prove it satisfies the assertions.


2    Why3
Why3 is a verification framework that allows us to interface with multiple theo-
rem provers and automated solvers using the same surface syntax and underlying
logic [1,8]. This means that, if one such solver is not able to discharge a verifica-
tion condition, one can easily switch to another which might be able to complete
our proof.
    To understand how it works, we will present the defenition of an array list
type written in Why3’s dedicated programming language WhyML:
    type arrayList 'a = {
      mutable arr : array 'a;
      mutable size : int
    }
This type definition features a field arr of type array 'a, the polymorphic type
of arrays defined in Why3 standard library, and an integer size representing the
number of elements in a value of type arrayList.
    Although our type declaration has all we need to build a comprehensive set of
functions for our arrayList, from a logical point of view we are missing crucial
information. In particular, that the size attribute cannot be greater than the
length of the array. To express this, we will add the following type invariant:
    invariant { 0 <= size <= arr.length }
Next, we will write a function that replaces the element at a given index and
returns the old element:
    let set (al: arrayList 'a) (i : int) (e : 'a) : 'a
For simplicity’s sake, we will add a precondition requiring i to be within the
bounds of our list:
    requires { 0 <= i < al.size }
Had we not included such precondition, we would have to include in the body of
set an if..then..else expression to avoid accessing an index out of bounds.
This a common practice of defensive programming.
    Next, we will need to specify that the result of our function is the old value
at index i and that the new value is e. To do this, we will will introduce two
4       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

postconditions, where we use the old tag to refer to our array list before the
function was called and result for our function’s return value
    ensures   { result = old al.arr[i] }
    ensures   { al.arr[i] = e }
    Lastly, we also need to specify that every other element in the array, as well
as its size, is unchanged.
      ensures { al.size = old al.size }
      ensures { forall j. 0 <= j < al.size /\ not j = i ->
                  old al.arr[j] = al.arr[j] }
Now we simply write the body of the function, trivial as it is:
    = let ret = al.arr[i] in
      al.arr[i] <- e; ret
    The full annotated function can be found in annex A. When fed into Why3,
the above set function generates six verification conditions. These include safety
properties (access index in array bounds, which is proved with our invariant) and
functional ones (type invariant preservation and postcondition entailment). All
of these are automatically verified in less then a second by the Alt-Ergo [10]
SMT solver, one of the provers Why3 allows us to interface with.

3     Defunctionalization
Before jumping into our framework’s implementation lets first take a gander at
a few quick (original) examples to understand how defunctionalization works,
how it can be mechanized and how we can apply it to program verification.

3.1   A simple example
As previously mentioned, defunctionalization is the practice of turning higher-
order programs into equivalent first-order implementations. To illustrate this
method, we will convert a higher-order OCaml program that reverses a list. The
code will be written in CPS (Continuation Passing Style) [3], which, instead of
letting the program return a value to the function’s caller, passes the return
values as a parameter to a “continuation” function that is given as a first order
value. The implementation is as follows:
    let rec reverse_aux_cps l k = match l with
      | [] -> k []
      | x::t -> reverse_aux_cps t (fun r -> x ::            (k r))

    let reverse l = reverse_aux_cps l (fun r -> r)
There are two anonymous functions: the identity function (fun r -> r) and
the function which builds the reverse of the list (fun r -> x::(k r)). In order
to begin our gentle descent towards a first order version of this program, we
introduce a new algebraic data type to represent continuations:
            A Deductive Verification Framework For Higher Order Programs         5

  type 'a kont = Kid | Krev of 'a * 'a kont
The constructors Kid and Krev match, respectively, the identity function and
the one that builds the reverse. Krev‘s two extra arguments represent its free
variables, namely the appended value and the continuation function. Next, we
need to introduce an apply function which will replace all first order functions
calls:
  let rec apply kont arg = match kont with
    | Kid -> let r = arg in r
    | Krev(x, k) -> let r = arg in x::(apply r k)
The defunctionalization process terminates by replacing, in the original code,
native function application with calls to apply and anonymous functions with
constructors of the kont data type.
  let rec reverse_aux_defun l k = match l with
    | [] -> apply [] k
    | x::t -> reverse_aux_defun t (Krev(x, k))

  let reverse_defun l = reverse_aux_defun l Kid
    The full defunctionalized implementation can be found in annex B and if the
reader wishes to understand in more detail how this function would run, we have
included an example of the program running in annex C.

3.2   Proving a defunctionalized program
With defunctionalization’s bases covered, let us introduce how it’s used in a proof
context. For this, we consider a simpler function, namely one that computes a
list’s size, also written in CPS. The WhyML implementation is as follows:
  let rec length_cps (l : list 'a) (k : int -> 'b) : 'b =
    match l with
    | [] -> k 0
    | _ :: t -> length_cps t (fun l -> k (1 + l))
    end

  let len (l : list 'a) : int =
    length_cps l (fun x -> x)
Now we annotate our functions with their respective postconditions. The len
function’s specification is fairly straightforward:
  ensures { length l = result }
where length is a purely logical function, issued from the Why3 standard library,
which can only be used within specifications and shall never be mixed with
executable code. The CPS function’s specification is a bit more intricate. We
could, naively, write something like
6       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

    ensures { k (length l) = result }
However, this leaves us with the problem of how to interpret the use of func-
tions in our logic, since these may have side effects (e.g., divergence) which can
lead to logical inconsistencies. Therefore, we introduce a layer of abstraction
to allow us to use potentially effectful programs in our assertions: instead of
thinking of functions as a computation of an output from a given input, such as
f: t1 -> t2, we will think of them as a pair of predicates, namely their precon-
dition (pre : t1 -> prop) and postcondition (post : t1 -> t2 -> prop).
This is strongly inspired by the work of Régis-Gianas and Pottier [18]. Under
this setting, we would provide with length_cps the following specification:
     ensures { post k (length l) result }
and the continuation defined in length_cps with
     ensures { post k (l + 1) result }
Now we will proceed with our program’s defunctionalization as we did before,
first by defining a type to represent our first order functions:
    type kont = Kid | Klen kont
The next step, that is, the apply function, is quite similiar to our previous
example, which can be found in annex D. Finally, since we have no higher order
functions, we must define our own post predicate, as follows:
    predicate post (k : kont) (length : int) (result : int) =
      match k with
      | Kid -> result = length
      | Klen k -> post k (length + 1) result
      end
For the above first-order implementation and specification, all the verification
conditions generated by Why3 are automatically discharged in no time.
   As we can observe, the defunctionalized definition of predicate post is a
simple matter of collecting the predicate’s uses from the original higher-order
implementation. As for the specification of function apply, since this function
simulates native application, we provide it with a postcondition stating that
applying k to arg must be directly related to result. As we will show, the
translation of the post predicate and the generation of the specification of the
apply are indeed amenable to automatic tool translation.


4    The GOSPEL to Why3 Pipeline
In spite of the fact defunctionalization can be a bit of a difficult concept to grasp,
once it is understood it becomes clear that we can divide the process into neatly
defined steps and that these steps can very easily be mechanized. Although we
give a complete overview of how OCaml code is converted in our translation
scheme, found in annex E, we will explain in detail some of the trickier rules and
              A Deductive Verification Framework For Higher Order Programs          7

exemplify with some case studies how our converter fares when confronted with
decently complex programs. The full implementation for our translation scheme,
along with some test cases, can be found in our GitLab 1


4.1    Defunctionalization at Work

Explaining in detail every single one of our translation scheme’s minutia would
be a tad redundant, seeing as WhyML and OCaml are very similar, given they
both derive from the ML dialect. Indeed, most of our translations simply amount
to lightly re-organizing the OCaml code to fit WhyML’s syntax, picking up the
free variables and figuring out the type of the expression. Nevertheless, we will
convert a handful of expressions to explain some of the peculiarities of how we
approach defunctionalization before we get into the relatively more complex case
studies.
    First we will be looking at the translation of the following expression : x + y.
When converting an OCaml expression we will return, along with its WhyML
translation, its set of free variables and its type. Seeing as this expression belongs
to the class e1 o e2, x being e1, + being o and y being e2, we will need e1 and
e2’s translation and free variables. Seeing as e1 and e2 are simply two variables,
we will translating both directly, meaning e1’s translation will be x and e2′ s will
be y and their set of free variables will be a singleton set each only containing a
tuple with the variable’s name and its type, which we obtain from a dictionary
we refer to in our translation scheme as varType which binds the name of user
defined variables to their types.
    Finally we need only to combine the two translations with o’s, which will
simply be +, producing "x + y", and the two sets of free variables, giving us
{(x, int), (y, int)}. Note however that we do not define this expression’s type
attribute, seeing as it is only used when translating function applications and we
know that an addition can only produce integers, meaning we will never apply
the result of this expression as a function.
    It is worth noting that in order to use the addition operator in WhyML
we need to import the int.Int module. To handle this, we import, along with
int.Int, several other libraries so we can naturally use everything in the OCaml
standard library, such as lists and arithmetic operations.
    Next, we will bind the previous expression to a lambda and translate it with
the fun arg* : τ -> e1 construction
    fun (x : int) (z : int) : int -> x + y
    Important to note that z is not used and y is not defined in the scope of this
expression. First and foremost, we will be adding the function’s arguments’ type
to the aforementioned varType dictionary. After computing e1’s free variables,
we must remove x and z from the set. Since e1 is our last translated addition
(x + y), our new set of free variables is simply {(y, int)}, since x is defined in
the scope of this expression. Additionally, we will defunctionalize this lambda
using the buildApply function, which takes the lambda’s free variables, type
1
    https://gitlab.com/releaselab/defunctionalization/-/tree/patch-1
8       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

and arguments’ name and returns its defunctionalized alias. Given the previous
defunctionalization examples, the reader might be expecting something like this
     type kont1 = K int

     let apply (k : kont1) (arg1 : int) (arg2 : int) : int =
       match k with K y -> let x = arg1 in let z = arg2 in x + y

    Although this would be an accurate translation, it is not fully defunctional-
ized, due to the fact OCaml technically does not support functions with more
than one argument, which might seem unintuitive seeing as our original lambda
has two. When OCaml parses it, however, it produces a one argument function
that returns another one argument function, such as:
    fun (x : int) -> (fun z : int -> x + y)
    This means we can partially apply arguments and, instead of throwing an
error, OCaml will simply return a lambda where the applied arguments are now
free variables. Due to this detail, we defunctionalize our functions in the way
OCaml defines them instead of how the user does. Hence, we will first translate
the innermost lambda into K1 y x with the generated defunctionalization being
similar to:
     type kont1 = K1 int int

     predicate post1 (k : kont1) (arg :int) (result : int) =
       match k with K1 y x -> let z = arg in true

     let apply1 (k : kont1) (arg : int) : int =
       ensures { post1 k arg result }
       match k with
       | K1 y x -> let z = arg in y + x

     Seeing as we didn’t annotate our original lambda with a postcondition, we
fill in the post predicate with the default value true. Before moving on to the
outermost lambda, we will bind the type int -> int to the function apply1
the the predicate post1.
     Now all that is left is to translate the outermost lambda, which is largely
identical to the first one, except we now bind int -> (int -> int) to the
function apply2 and the predicate post2 and, seeing as the body of this function
will be our previously generated expression, we must append it a specification
that describes its return value so we may use this function in future specifications.
We then conclude that our post predicate is as follows:
     type kont2 = K2 int

     predicate post2 (k : kont2) (arg : int) (result : kont1) =
       match k with K2 y -> let x = arg in result = K1 y x
            A Deductive Verification Framework For Higher Order Programs         9

    In conclusion, we create two apply functions, one that takes the first argu-
ment and returns a continuation and another which accepts that continuation
along with the final argument returning the result of the original function.
    Another detail is that, unlike in our previous examples, we defined two types
(kont1 and kont2) with one constructor each instead of one type with two
constructors. This is due to the fact that we need different apply functions for
each different function type since WhyML does not support generalized algebraic
data types [19] as arguments or return values. We cannot put all our constructors
in the same definition because that would mean, if we had more than one apply
function, their pattern matching wouldn’t be exhaustive and Why3 wouldn’t be
able to dispatch a proof.
    Finally, we will set this expression’s type as int -> (int -> int) and reset
the changes made to varType at the start of the translation, that is, remove the
binding of x to int and the binding of z to int. Important to note that removing
a pairing means that, if there was any other value associated with the key before
adding the removed value, that becomes the new value, if not, the binding now
becomes undefined.
    To conclude, we will now convert the application of a function to a set of
arguments: (k 3) 4.
    First, we will translate the expression within brackets with the e1 e2 rule.
To do so, we will get the translation of e1 and e2, both of which are directly
obtained; their free variables (which are not relevant for this example), and their
type, e2’s is irrelevant, due to the fact it is a literal value and those are never
used as functions, and e1’s is obtained in the same manner as before: by checking
the current mapping for the variable name k. For the sake of argument, we will
assume k is bound to the previous lambda, whose type is int -> (int -> int).
    With both sub expressions now converted, it is time to turn our attention to
our original application, which will be converted as follows:
     apply2 k 3

and it’s type will be int -> int, seeing as we have already applied k’s first
argument.
    Next, we do the same thing for the next argument, the only notable difference
is that our expression’s type is now int -> int, which is bound to the integer
1 and thus we will use the apply1 function, giving us:
     apply1 (apply2 k 3) 4

    As the one might have noticed, the previous expressions were defunctional-
ized even though they weren’t used in a higher order context. This is another
quirk of our translation: any and all function declarations and applications, when
converted, are also defunctionalized, regardless of whether or not they are used
as parameters. The main reason for this is that, when a function is declared
we generally have no way of knowing if it is going to be used as a first order
value. Despite the fact that we are defunctionalizing more than what we strictly
10      Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

need, translating every function the same way makes the conversion process more
uniform and easier to define and implement.

4.2   Extending GOSPEL
Since we have covered the most relevant rules for translating and defunctional-
izing OCaml code, let us take a look at GOSPEL. We won’t go over its syntax
in much detail, seeing as its specifications are quite similar to Why3’s, although
there are some interesting divergences. Namely, GOSPEL annotations are added
as comments beginning with the symbol "@" at the tail end of our implementa-
tions or, for anonymous functions, between the fun keyword and the function’s
arguments like so

      fun [@gospel {| ensures Q |}] args... -> exp

    There are some other which are less relevant, for example, having to redefine
the name of each argument and the name for the result and the absence of
curly brackets, but for the most part we will use similar constructions as we did
for Why3 specifications. Due to this, our WhyML conversions will be almost
identical to their GOSPEL counterparts, with one small difference: the post
"predicate". To understand how we have extended GOSPEL to allow usages of
post, let us consider a small example.

          (*@ r = f g x
                ensures post (g : int -> int) x r *)

This will be the specification for a function f which takes a function g as a pa-
rameter and an integer x. we have omitted the implementation since we will
be focusing on how we will deal with the post condition. As previously ex-
plained, post is used to avoid directly using non-pure functions (that is, with
side-effects) in our specifications. Because post has to work for any function
applied to however many arguments of any types, it cannot be defined through
WhyML. Instead, as previously shown, we create several posts, one for each
apply function and whenever we encounter a post in our specifications, we will
replace its application with the respective defunctionalized post. That is why we
put predicate in quotation marks; post is not really a predicate nor a function,
but more of a meta-predicate: a predicate which, depending on the situation,
can be any predicate you need. The only restriction for using it is that the first
argument, that is, the function, must have its type explicitly declared so we know
which post to use.
    Now that we understand the keyword, let us look at how we convert it. For
one argument functions it is almost direct. For the aforementioned specification,
we would find the post predicate for functions of type int -> int, and replace
the call to post with post2 from our previous translation:
      ensures { post2 g x r }
            A Deductive Verification Framework For Higher Order Programs        11

    It gets interesting, however, when we apply post to a function that takes more
than one argument. Let us imagine that the g function was of type int -> (int -> int)
and was applied to an extra argument y, such as, post g x y r. The translation
of such post would be:
      ensures { forall var0 : kont1. post1 g x var0 -> post2 var0 y r }

   In simpler terms, if we assume the return value for g when applied to x is
var0, whose type would be kont1, then when var0 is applied to y, it will return
r.


5     Case studies
With the most important rules detailed and understood, we will examine how
our tool handles relatively complex programs. The following case studies, unlike
the ones presented in Section 3, are not original and were presented by one of the
project’s supervisors in their precursor paper on defunctionalized proofs [14].

5.1   Height of a tree
Firstly, we will look at at a function that computes the height of a binary tree
with the following signature

let height_tree_cps (t: int tree): int = ...
(*@ r = height_tree t
      ensures (height t) = r *)

    An interesting peculiarity of this program is that it only accepts a tree of
integers, even though, intuitively, a height function should work for any type
of tree. However, we won’t be dealing with any kind of polymorphism, for that
would add certain complications when building our constructors [15]. Another
thing worth mentioning is that OCaml does not have a binary tree type, al-
though WhyML does. This means that, even though the OCaml program we
will present technically does not compile on its own unless the programmers de-
fines a tree exactly as it’s done in WhyML, it will result in a valid program after
the conversion if we import the tree.Tree module. Even so, one could wonder
why we simply don’t define the tree type in our code instead of going in this
roundabout way. The reason is that we are going to need a logical function from
Why3 standard library, namely the height function, in our specification, which
we can only apply in conjunction with WhyML’s tree type. This solution, flawed
as it may be, will be sufficient to prove our program.
    First let us define the recursive auxiliary function that performs the calcula-
tion

let rec height_tree (t: int tree) (k: int -> int) : int
  = match t with
12      Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

    | Empty -> k 0
    | Node((lt : int tree), _, (rt : int tree)) ->
        height_tree lt (fun [@gospel
        {| ensures post (k : (integer -> integer))
            (1 + max hl (height rt)) result |}]
          (hl : int) : int ->
        height_tree rt (fun [@gospel
        {| ensures post (k : (integer -> integer))
            (1 + max hl hr) result |}] (hr : int) : int -> k (1 + max hl hr)))
(*@ r = height_tree t k
      ensures post (k : (integer -> integer)) (height t) r*)

    This one is a bit trickier than our previous examples, due to the nested
continuations. In short, we create two continuations, one for each tree branch,
which will calculate their heights. Finally, they will compare the two and return
the highest value plus 1. Then, all our main function has to do is run the recursive
auxiliary function with the identity function.

let height_tree_cps (t: int tree): int =
  height_tree t
    (fun [@gospel {|ensures result = x|}] (x : int) : int -> x)
(*@ r = height_tree t
      ensures (height t) = r*)

   The fully annotated program and its conversion can be found in our GitLab
and can be proved using the CVC4 prover, which dispatches the proof in less
than a second.


5.2   Small-step interpreter

The final example we will present is an interpreter for a small language that
consists entirely of integer literals and subtractions thereof:

               type exp = Const of integer | Sub of exp * exp

   To define how expressions are reduced, we will present two rules, first we
assert that a Sub node with two Const can be reduced to a single Const:
                                              e
                  Sub(Const v1)(Const v2) −
                                          → Const(v1 − v2)

Additionally, we will also need an inference rule that allows us to properly parse
larger expressions:

                                         e
                                      e−→ e′
                                        e
                                        → C[e′ ]
                                   C[e] −
            A Deductive Verification Framework For Higher Order Programs        13

   C representing the following reduction context:

                            C ::= 
                                 | C[Sub  e]
                                 | C[Sub (Const v) ]

    Simply put, C[e] represents a context where the expression e has completely
replaced the symbol , meaning our inference rule reads: if an expression e can
be reduced to a simpler e′ , then any context C[e] can be reduced to C[e′ ]
    With our interpreter clearly described let us move on to how we represent
our contexts. Although the most natural translation would be of an algebraic
data type with three constructors, one for each of our rules, we will represent
them as first order functions that take an expression and return an expression,
leading to much cleaner and compact code.
    Next, we will implement a function that quite directly translates our inference
rule by taking a context C and an expression e which returns a context and a
new expression making sure that C[e] = C ′ [e′ ], C ′ and e′ being the returned
context and expression respectively.

let rec decompose_term (e: exp) (c : exp -> exp) :
  ((exp -> exp) * exp)
= match e with
  | Sub (Const (v1 : int), Const (v2 : int)) -> (c, e)
  | Sub (Const (v : int), (e : exp)) ->
      decompose_term e (fun [@gospel
        {| ensures post (c : (exp -> exp)) (Sub (Const v) x) result |}]
      (x : exp) : exp -> c (Sub(Const v, x)))

| Sub ((e1 : exp), (e2 : exp)) -> decompose_term e1
    (fun [@gospel {| ensures post (c : (exp -> exp)) (Sub x e2) result |}]
    (x : exp) : exp -> c (Sub(x, e2)))

(*@ c_res, e_res = decompose_term e c
      requires not (is_value e)
      ensures is_redex e_res &&
        forall res. post (c : (exp -> exp)) e res ->
          post (c_res : (exp -> exp)) e_res res*)

    The first thing one might notice is the fact we only match e with Subs and
no Const. When pattern matching is non-exhaustive, WhyML will add an ex-
tra branch of the following type |_ -> absurd and attempt to prove that it is
never reached. In this case, it will meet this obligation knowing that e is not a
value, in other words, not a constant. This knowledge comes from the is_value
predicate, which we do not define above. We haven’t added its implementation,
nor the others we use, seeing as their quite simple. Moreover, functions with
preconditions are handled a bit differently: any function presenting these will be
converted directly instead of defunctionalized, seeing as there are no interesting
14     Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

case studies of stateless continuations with preconditions. Therefore we will as-
sume that any function with these will never be used as a first order value and
therefore has no need in being defucntionalized, thereby simplifying our proof
obligations.
    Now that we have a function that satisfies C ′ [e′ ] = C[e] we need one for
the condition C ′ [e′ ] = e. For this purpose, all we need is to apply our original
function with a context so that C[e] = e, in other words, the identity function.

let decompose (e: exp) : (exp -> exp) * exp =
  decompose_term e
    (fun [@gospel {| ensures result = x |}] (x : exp) : exp -> x)
(*@ c_res, e_res = decompose e
      requires not (is_value e)
      ensures is_redex e_res &&
              post (c_res : (exp -> exp)) e_res e *)

    With decomposition out of the way, all that’s left is to properly evaluate our
expressions. To do this, we will define a function which takes an expression and
keeps decomposing and performing head reductions, that is, applying the first
rule we presented that reduces a Sub into a Const, until it reaches a constant:

let red (e : exp) : int =
  match e with
  | Const (v : int) -> v
  | _ -> match decompose e with
         ((c : exp -> exp), (r : exp)) ->
           let r : exp = head_reduction r in red (c r)
(*@ r = red e
      ensures r = eval e *)

    When converted, this program, whose translation also available in our Git-
Lab, is once again successfully proved, this time by the Alt-ergo prover, in less
then a second. However to reach it, we need to supply it with the following
lemma, which says that for any two expressions, if they evaluate to the same
value and are applied to the same context, their evaluations will stay equal
relative to one another.
lemma post_eval:
  forall c: exp -> exp, arg1: exp, arg2: exp, r1: exp, r2 : exp.
    eval arg1 = eval arg2 -> post0 c arg1 r1 -> post0 c arg2 r2 ->
    eval r1 = eval r2
    Since this lemma is much broader than our target function’s post condi-
tion, there could be some value in making it part of GOSPEL’s (and, naturally,
Why3’s) standard library, along with other general axioms regarding higher or-
der functions, so that the programmer has a fairly decent safety net when their
provers are unable to reach the required proof obligations. Of course we couldn’t
put it as is, given that it depends on the eval function, which is specific to our
           A Deductive Verification Framework For Higher Order Programs          15

case study. Nonetheless, we could turn it into a kind of meta-lemma where we
take a logical function of type 'a -> 'a as an argument. To use such a "meta"-
lemma to prove our transitive property would be just a matter of instantiating
it with the proper ’eval’-like function.
    Due to the fact that GOSPEL does not yet support lemmas, it will have to
be placed directly in our translation. An interesting limitation for this lemma
is that it could cease to work if we introduced more first order functions of
type exp -> exp that are divorced from the contexts we have described. To
handle this, our tool would have to know which specific continuations the user
is referring to and create a lemma tailored to them. A hypothetical translation
that solves this problem can be found in annex F.


6   Limitations
Due to time constraints, we could only hope to produce a rough prototype that
could be used less as a fully fledged tool and more of a proof of concept. Nat-
urally, what we created presents itself with the following non-exhaustive list of
restrictions, along with those previously mentioned in Section 5:
 – To prove an OCaml program, we first needed a way to convert the source
   code into a more digestible format, such as an abstract syntax tree. Two
   choices emerged; the Typedtree module and the Parsetree module, both from
   OCaml’s compiler-libs library; the main difference between the two being
   that the Typedtree has already inferred the types for all expressions and
   the Parsetree only has the type information that the user puts in the source
   code. Seeing as, to build our defunctionalized constructors, we need to know
   the types of the free variables, our options were to simply use the Typedtree
   or, alternatively, the Parsetree, with the caveat that the user would have to
   explicitly add the types for all variables defined in ’let’ bindings, match cases
   and function definitions. We decided on using the later seeing as it would be
   the easiest option to convert programs, although it does pose a restriction
   on the type of programs we can convert.
   Due to this choice, our program does not actually type-check the original
   code and leaves this to WhyML. This means that, theoretically speaking,
   we could have a situation where a badly typed program is converted and
   the resulting WhyML program is correctly typed, leading to a nonsensical
   specification. Although we believe this situation is impossible, we have no
   formal proof that this is the case.
 – In order to make the best of the time given, we decided, instead of trans-
   lating it in its entirety, to focus our efforts onto a subset of the OCaml
   language. Although we are missing some very useful syntactic sugar such as
   module declarations and optional arguments, the constructions allowed by
   our converter (e.g., match expressions, let..in, if..then..else, lambda
   expressions) give us plenty of breathing room to write rich, functional code.
 – Due to the fact our apply functions will be mutually recursive, proving ter-
   mination, while not impossible [14] ,would be quite difficult, therefore, we
16     Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

   only prove partial correctness; in other words, we do not prove that these
   functions are terminating.
 – Defunctionalization can only be used knowing a priori which functions will
   be used as first order values. Therefore, if a function takes, for example, a
   lambda of type int -> int, and no functions of this type are defined, then
   our converter throws an error.
 – Although we hope to eventually use defunctionalization to prove functions
   with side effects, our prototype can only be used to prove pure programs.


7    Conclusions and future work

In this report we have proposed a translator that can convert GOSPEL an-
notated OCaml programs into WhyML in order to prove their specification,
possibly involving higher order functions. This represents not only the first work
involving the verification of GOSPEL implementations, but also, as far as we
know, the first usage of defunctionalization in the context of function specifica-
tion.
    While our tool covers an interesting subset of OCaml programs, we have only
scratched the surface of what defunctionalization is capable of. We will save for
future work patching up some of the limitations presented in Section 6, namely
dealing with effectful programs and polymorphism. To tackle the former, we
anticipate the need to by pass the state of the program as an extra parameter
to our posts [14]; for the latter, a much more profound extension to Why3 is
needed, namely extending Why3’s type system with generalized algebraic data
types [15].


References
 1. Bobot, F., Filliâtre, J.C., Marché, C., Paskevich, A.: Why3: Shepherd your herd
    of provers. In: . (2011)
 2. Charguéraud, A., Filliâtre, J., Lourenço, C., Pereira, M.: GOSPEL — Providing
    OCaml with a Formal Specification Language. In: Formal Methods - The Next 30
    Years - Third World Congress. Lecture Notes in Computer Science, vol. 11800, pp.
    484–501. Springer (2019), 10.1007/978-3-030-30942-8_29
 3. Danvy, O., Millikin, K., Nielsen, L.R.: On One-pass CPS Transformations. Journal
    of Functional Programming 17(6), 793–812 (2007)
 4. Danvy, O., Nielsen, L.R.: Defunctionalization At Work. In: International Con-
    ference on Principles and Practice of Declarative Programming (PPDP) (2001).
    https://doi.org/10.1145/773184.773202
 5. Dijkstra, E.W.: Guarded Commands, Nondeterminacy and Formal Derivation of
    Programs. Commun. ACM 18(8), 453–457 (Aug 1975), 10.1145/360933.360975
 6. Dijkstra, E.W.: The Humble Programmer, p. 1972. Association for Computing
    Machinery, New York, NY, USA (2007), https://doi.org/10.1145/1283920.1283927
 7. Filliâtre, J.C.: Deductive Software Verification. International Journal on Soft-
    ware Tools for Technology Transfer (STTT) 13(5), 397–403 (Aug 2011),
    10.1007/s10009-011-0211-0
            A Deductive Verification Framework For Higher Order Programs             17

 8. Filliâtre, J.C.: One Logic To Use Them All. In: International Conference on Auto-
    mated Deduction. pp. 1–20. Springer (2013)
 9. Filliâtre, J.C., Paskevich, A.: Why3 — Where Programs Meet Provers. In: Pro-
    gramming Languages and Systems. pp. 125–128. Springer Berlin Heidelberg (2013)
10. Iguernelala, M.: Strengthening the Heart of an SMT-Solver: Design and Implemen-
    tation of Efficient Decision Procedures. Thèse de doctorat, Université Paris-Sud
    (Jun 2013)
11. Jung, R., Krebbers, R., Jourdan: Iris From The Ground Up: A Modular Foundation
    For Higher-order Concurrent Separation Logic. Journal of Functional Programming
    28 (2018)
12. Kanig, J., Filliâtre, J.C.: Who: A Verifier for Effectful Higher-order Programs. In:
    Workshop on ML. Edinburgh, Scotland (Aug 2009), 10.1145/1596627.1596634
13. O’Hearn, P.W.: Continuous Reasoning: Scaling the Impact of Formal Meth-
    ods. In: Symposium on Logic in Computer Science. p. 13–25. IEEE (2018),
    10.1145/3209108.3209109
14. Pereira, M.: Desfuncionalizar para Provar. CoRR abs/1905.08368 (2019),
    http://arxiv.org/abs/1905.08368
15. Pottier, F., Gauthier, N.: Polymorphic typed defunctionalization. SIG-
    PLAN Not. 39(1), 89–98 (Jan 2004). https://doi.org/10.1145/982962.964009,
    https://doi.org/10.1145/982962.964009
16. Reynolds, J.C.: Definitional Interpreters for Higher-Order Programming Lan-
    guages. In: Proceedings of the ACM Annual Conference - Volume 2. p. 717–740.
    ACM ’72 (1972), 10.1145/800194.805852
17. Reynolds, J.C.: Separation logic: A Logic For Shared Mutable Data Structures. In:
    Symposium on Logic in Computer Science. pp. 55–74. IEEE (2002)
18. Régis-Gianas, Y., Pottier, F.: A Hoare Logic for Call-by-Value Func-
    tional Programs. In: International Conference on Mathematics of Pro-
    gram Construction (MPC). vol. 5133, pp. 305–335. Springer (Jul 2008),
    http://dx.doi.org/10.1007/978-3-540-70594-9_17
19. Xi, H., Chen, C., Chen, G.: Guarded recursive datatype constructors. In: Proceed-
    ings of the 30th ACM SIGPLAN-SIGACT symposium on Principles of program-
    ming languages. pp. 224–235 (2003)
18       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

A      Annotated set function

use array.Array
use int.Int

type arrayList 'a = {
    mutable arr : array 'a;
    mutable size : int
  }
invariant { 0 <= size <= arr.length }

let set (al : arrayList 'a) (i : int) (e : 'a) : 'a
  requires { 0 <= i < al.size }
  ensures { al.arr[i] = e }
  ensures { result = old al.arr[i]}
  ensures { al.size = old al.size}
  ensures { forall j. 0 <= j < al.size /\ not j = i ->
  old al.arr[i] = result.arr[i] }
= let ret = al.arr[i] in
  al.arr[i] <- e;
  ret
B      Defunctionalized reverse function
     type 'a kont = Kid | Krev of 'a * 'a kont

     let rec apply kont arg = match kont with
       | Kid -> let r = arg in r
       | Krev(x, k) -> let r = arg in x::(apply r k)

     let rec reverse_aux_defun l k = match l with
       | [] -> apply [] k
       | x::t -> reverse_aux_defun t (Krev(x, k))

     let reverse_defun l = reverse_aux_defun l Kid
            A Deductive Verification Framework For Higher Order Programs         19

C    Reverse function stack trace

reverse_defun [1;2;3]

    which then has the following stack trace

reverse_aux_defun [1;2;3] Kid

reverse_aux_defun [2;3] Krev(1, Kid)

reverse_aux_defun [3] Krev(2, Krev(1, Kid))

reverse_aux_defun [] Krev(3, Krev(2, Krev(1, Kid)))

apply [] Krev(3, Krev(2, Krev(1, Kid)))

3::(apply [] Krev(2, Krev(1, Kid))

3::2::(apply [] Krev(1, Kid))

3::2::1::(apply [] Kid)

3::2::1::[]

    Given this, we can see that this function returns the list 3::2::1::[], that is,
[3;2;1], the reverse of [1;2;3]. Interesting to note that for each call to apply the
first argument, namely the list, doesn’t change. With this in mind, we could
have had the apply function take a void value (called unit in ocaml) as its first
argument and had the Kid function simply return the empty list. We chose to
do it this way, despite this, to keep the reverse_cps function as close to CPS
conventions as possible.
20       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

D      Defunctionalized length

use int.Int
use list.List
use list.Length

     let rec function apply (k : kont) (arg : int) : int
       ensures { post k arg result } =
       match k with
       | Kid -> let x = arg in x
       | Klen kont -> let l = arg in apply kont (1 + l)
       end

 let rec function length_defun (l : list 'a) (k : kont) : int
   ensures { post k (length l) result } =
   match l with
   | Nil -> apply k 0
   | Cons _ t -> length_defun t (Klen k)
   end

     let length_fin (l : list 'a)
       ensures { result = length l } =
     length_defun l Kid
                           A Deductive Verification Framework For Higher Order Programs        21

            E     Translation Scheme


Symbol          Construction                                                   Translation

e                     ()                         e.trans := "()";

                                                 e.trans := s;
                       s                         e.type := varType[s].top();
                                                 e.freeVar := [(s, e.type)];

                      []                         e.trans := "Nil"

                      n                          e.trans := n
                                                 if is_constructor() then
                                                       c.trans := format("%s %s..., s, e1.trans, ...)
                (s)?(e1 (,e2)*)                  else
                                                       c.trans := format("(%s, ...), e1.trans...)
                                                 e.freeVar := union(c1.vars,...)

                                                 e.trans := format("%s %s %s", e1.trans, o.trans, e2.trans);
                   e1 o e2
                                                 e.freeVar := union(e1.freeVar, e2.freeVar)
                                                 e.trans := format("Cons (%s) (%s)",
                   e1 :: e2                      e1.trans, e2.trans);
                                                 e.freeVar = union(e1.freeVar, e2.freeVar);
                                                 e.trans := format("( %s) ; (%s)", e1.trans, e2.trans);
                    e1;e2                        e.freeVar := union(e1.freeVar, e2.freeVar);
                                                 e.type := e2.type
                                                 e.trans := format("%s in %s", var_def.trans, e2.trans);
                                                 e.freeVar := union(var_def.freeVar,
                var_def in e2                    e2.freeVar.except(var_def.vname));
                                                 e.type := e2.type;
                                                 varType[var_def.vname].pop();"
                                                 e.trans := format("match %s with
                                                 |%s -> %s... end", e1.trans, c.trans, e2.trans, ...);
         match e1 with (|c -> e2)+
                                                 e.freeVar := union(e1, e2.except(c.vars),..);
                                                 e.type := e2.type;
                                                 e.trans := format("if %s then %s else %s",
                                                 e1.trans, e2.trans, e3.trans);
            if e1 then e2 else e3
                                                 e.freeVar := union(e1.freeVar, e2.freeVar, e3.freeVar);
                                                 e.type := e2.type
                22       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara



                                                     for all arg do varType[arg.name].push(arg.type);
                                                     e.freeVar := e1.freeVar.except(arg1,...);
                                                     let name = buildApply(e.freeVar, e1.trans, arg1, ...,
                 fun arg+ : τ -> e1                  τ .trans) in
                                                     e.trans := format(%s(%s...,), name, e.freeVar[0]...);
                                                     e.type := (τ , arg1, ...);
                                                     for all arg do varType[arg.name].pop();
                                                     e.trans := format("%s %s %s", getApply(e1.type), e1.trans, e2.trans
                         e1 e2                       e.freeVar := union(e1.freeVar, e2.freeVar)
                                                     e.type := consumeArg(e1.type)

                                                     t.trans := fomat("type %s %s... = |"%s %s... =
    type (’s1 (,’s)*)? s2 = (| s3 (of s4(* s)*)?)+
                                                     %s...", s2, s1,..., arg.trans)
t                                                    t.trans := fomat("type %s %s... = |"%s %s... =
         type (’s1 (,’s)*)? s2 = arg(;arg)*
                                                     %s...", s2, s1,..., arg.trans)
                                                     t.trans := format("type %s %s... =
              type (’s1 (,’s)*)? s2 = τ
                                                     %s, s2, s1,..., τ .trans)

c                          n                         c.trans := n
                                                     if is_constructor() then
                                                           c.trans := format("%s %s..., s, c1.trans, ...)
                     (s)?(c1 (,c2)*)                 else
                                                           c.trans := format("(%s, ...), c1.trans...)
                                                     c.vars := union(c1.vars, c2.vars, ...)
                                                     l.trans := arg.trans;
                          arg
                                                     l.vars = {(arg.name)}

                           []                        c.trans := "Nil"
                                                     l.trans := format("Cons %s %s", c1.trans, c2.trans);
                         c1::c2
                                                     c1.vars := union(c1.vars, c2.vars)

o                        +(.)?                       o.trans := "+"

                          -(.)?                      o.trans := "-"

                          *(.)?                      o.trans := "*"

                          /(.)?                      o.trans := "/"

                          &&                         o.trans := "&&"

                           ||                        o.trans := "||"
                             A Deductive Verification Framework For Higher Order Programs      23



                        =                          o.trans := "="

τ                       s                          τ .trans := s

                   s (-> τ )+                      τ .trans := String.format("%s -> %s, s, τ .trans)
                        ()                         τ .trans :="()"

arg                     ()                         arg.trans := "()"
                                                   arg.trans := format("s : %s", τ .trans);
                     (s : τ )                      arg.type := τ .trans;
                                                   arg.var := s

                                                   varDef.vname := s; if isRec() then
                                                         varType[s].push((τ , arg1,...));
                                                   if isFun() then
var_def     let (rec)? s arg* : τ = e1                   buildApply(s, e1.freeVar, arg1, ..., τ .trans);
                                                   var_def.trans := format("let %s = %s in ", s, e1.trans);
                                                   if not isRec() then
                                                         varType[s].push((arg1.type,..., τ ));

top_level              t;;                         top_level.trans := t.trans

                    var_def;;                      top_level.trans := var_def.trans

                       e;;                         top_level.trans := format("let %s = %s", VAR_NAME, e.trans)
24       Tiago Soares — 52965 Supervisors: Mário Pereira, António Ravara

F      Defunctionalized lemma

     let rec lemma post_eval (k: kont0) (arg1 arg2 r1 r2: exp)
       requires { eval arg1 = eval arg2 }
       requires { post0 k arg1 r1 && post0 k arg2 r2 }
       ensures { eval r1 = eval r2 }
       variant { k }
     = match k with
       | K2 -> ()
       | K1 e c ->
          post_eval c (Sub arg1 e) (Sub arg2 e) r1 r2
       | K0 n c ->
          post_eval c (Sub (Const n) arg1) (Sub (Const n) arg2) r1 r2
       |_ -> true
       end
