                                                  Invariant Detection with Program Verification Tools∗
                                                                                            Wei He†
                                                                           Department of Computer Science
                                                                               University of Arizona
                                                                                  AZ 85721, USA
arXiv:1906.11929v1 [cs.PL] 27 Jun 2019




                                                                                   hewei@email.arizona.edu




                                                                                            Abstract
                                                  Compilers can specialize programs having invariants for performance improvement. Detect-
                                               ing program invariants that span large and complex code, however, is difficult for compilers.
                                               Traditional compilers do not perform very expensive analysis and thus only identify limited
                                               invariants, which limits the potential of subsequent optimizations. We would like to address the
                                               invariant detection problem via more sophisticated analyses using program verification tools.
                                               In this paper, we reveal pitfalls of choosing program verification tools for invariant detection,
                                               identify challenges of modeling program behavior using one of these tools—CVC4, and propose
                                               some ideas about how to address the challenges.


                                         1     Introduction
                                         In this paper, we attempt to address the problem of detecting invariants—program properties,
                                         such as variable values, that remain unchanged along all possible execution paths between two
                                         points in a program. It has been shown that program optimization based on invariants identified
                                         via domain knowledge can achieve significant performance improvement [15]. However, detecting
                                         invariants that span large and complex code is difficult for compilers for two reasons: (1) Compilers
                                         usually do not perform expensive analysis due to its performance concern, (2) and therefore can not
                                         find all possible invariants in a program. In our research, we would like to explore whether more
                                         sophisticated analyses by program verification tools can help us find more invariants that enable
                                         further optimization than traditional compilers.
                                             Compiler optimization has been a effective approach to speedup softwares for a long time. Some
                                         of these optimization techniques utilizes invariants in a program source code. In general, invariants
                                         are properties that something is known to remain unchanged along all possible execution path
                                         of a program. For example, loop-invariant code motion is a compiler optimization that moves
                                         computations whose result remain unchanged in the loop body to the outside. The growing size and
                                         complexity of programs nowadays, however, makes it difficult for compilers to detect invariants they
                                         can utilize. For instance, it is challenging to detect invariants when modern programming language
                                         allows a memory location to be accessed through different alias in the program (e.g., pointers in
                                         C/C++). Meanwhile, the size of Linux kernal grows from less than 0.5M SLOC to over 2M SLOC
                                         within five years from 1994 to 1999 [11] and is over 20M SLOC now.
                                             Since examining properties of programs has been studied in the program verification community
                                         as model-checking problems and many tools are available, we would like to detect program invariants
                                         by utilizing program verification tools. SAT (Boolean Satisfiability) solver and SMT (Satisfiability
                                         Modulo Theories) solver are widely used tools on the model checking problem [4, 10, 12]. Users need
                                         to model their programs using the input language of a solver and give a query about the property
                                            ∗ All discussions about tools in this paper are based on our experiments performed during August 2014—November

                                         2014.
                                            † This research was conducted under the supervision of Prof. Saumya Debray




                                                                                                1
they would like to check. The solver then answers the user’s queries. Both SMT and SAT solvers
answer a query by either proving the queries property is true or finding a counterexample. For SAT
solvers, the input needs to be boolean formula in CNF (Conjunctive Normal Form). On the other
hand, SMT solvers provide more expressive input languages and is thus easier to use. Considering
that real-world softwares can be huge, our first attempt is to model programs using SMT solver for
simplicity.
    In the paper, we attempt to explore the approach of leveraging sophisticated analysis via an
SMT solver to detect invariants in C programs. This paper makes the following contributions:
    • We describe an idea of modeling program behavior using an SMT solver—CVC4 and identify
      C program structures that are easy or hard to model.
    • We identify pitfalls of choosing program verification tools to detect invariants for optimizations.
      One needs to pay attention on the approximation taken by the tools because the approximation
      may affect the correctness of later optimizations.
    • Given that it is hard to model some C structures accurately, we give an initial idea about how
      to identify the rest of the program not influenced by these structures. Modeling the rest of
      the program could enable us to detect a subset of invariants in the program.
    In the rest of this report, we introduce several tools we have tried for invariant detection and the
features of each tool in Section 2. Section 3 presents how some C language structures can be easily
modeled in the input language of an SMT solver—CVC4. In this section, we also discuss structures
that are hard to modeled and the specific challenges. Finally, we give an initial idea about how to
model a C program with complex structures via a compromise of precision in Section 4.


2     Tools
For our purpose of detecting invariants in C programs, we consider using SMT solvers, SAT solver, or
C program analysis tools built on top of these solvers. As we will discuss in this section, we have two
possible options: (1) using a C program analysis tool that takes over-approximation on examined
properties or (2) modeling the C program behavior in the language of an SMT or SAT solver that
proves invariant properties. We explain the requirement of over-approximation and summarize four
tools we have tried in this section.
    Some C program analysis tools do not examine all possible execution paths of programs (espe-
cially for those with loops) but take an approximation. According to how they take the approx-
imation, these tools fall into two categories: over-approximation and under-approximation. The
difference between them is that over-approximation guarantees if the tool gives a positive answer
to a query, the true answer of this query is positive indeed. In contrast, under-approximation en-
sures that if the tool gives a negative answer, there exists a concrete counterexample to the query.
For example, suppose there is an integer variable int x in a tool’s input and the tool cannot find
out a concrete value of x. The user would like to know whether x == 0 is true. If the tool takes
an over-approximation, it answers False because the value of x is uncertain. If the tool takes an
under-approximation, it answers True because the solver cannot find a concrete counterexample.
Note that for the reverse question, i.e., whether x != 0, the tool will give the same answer as to the
question x == 0 because it has no knowledge about the value of x.
    For the purpose of invariant detection, we need the tool to take over-approximation because
detected invariants are used by subsequent optimizations that must guarantee the correctness. Sup-
pose we would like to determine whether the value of a variable x remains the same after some
statements. Let old x and new x be the value of x before and after the statements, our query to the
tool simply ask whether new x == old x is true or not. If the tool answers true, an optimization
may be performed based on this property, so we would like the tool to answer true only if it is
provable.
    CVC4 [2] is an open-source SMT solver that can be either used alone or utilized as a backend of
other program analysis tools. CVC4 provides a number of commonly used built-in theories including


                                                    2
integer linear arithmetic, arrays, tuples, records, inductive data types, and bit-vectors. When used
alone, it takes code in CVC4’s native language (we’ll call it CVC4-language for brevity) or SMT-LIB
as input, and checks the properties specified by queries in the code. CVC4-language does not allow
an instance to change its value, which makes it inherent difficult to model loop behavior precisely
in CVC4-language. We’ll discuss this limitation and how loop behavior can be modeled through
induction in Section 3.2.1.
    Based on CVC4 and another SMT solver—Z3 [7], Cascade [14] is a C program static analysis tool
that utilizes these SMT solvers as its backend. It takes as input a C program and a control file that
specifies assertions and constraints, and checks the assertions with the backend tools. Cascade takes
under-approximation. It unwinds loops and inlines functions in the input program, and reports the
assertions to be safe if no counterexample can be reached within a fixed number of iterations [13].
    Another program verification tool is CBMC [5, 6], which implements Bounded Model Checking
(BMC) [3] for ANSI-C/C++ programs. CBMC is based on SAT solver and uses MiniSat2 as the
backend in default. It takes a C program as input, and outputs the verification result. Same as
Cascade, CBMC takes under-approximation and models functions and loops in the similar way.
    Included in the CBMC, a k-induction tool provides more powerful verification to programs with
loops [8]. It splits a program into two pieces, a base case and a step case, and checks for loop
invariants inductively: it checks whether the first k iterations ensure the property and whether the
next iteration after k consecutive iterations ensures the property separately.
    Unlike CBMC and Cascade which do under-approximating analysis, 2LS is an over-approximation
tool [9] which takes C programs as input and reports the checking results. 2LS combines together
three existed techniques: bounded model checking, k-induction, and abstract interpretation, obtain-
ing a new algorithm which is better than any single one of them. Unfortunately, 2LS is still under
development and is not robust enough to be applied on very large programs such as PostgreSQL.
    For invariant detection, all the tools we’ve tried and described above cannot deal with real-world
programs because they take under-approximation or lack robustness. So the rest of this paper
describes our effort on modeling C programs in CVC4-language.


3       Modeling C Structures in CVC4-language
CVC4-language is very different from C programming languages in that it does not allow an instance
to change its value, which makes it difficult to model some C program structures in CVC4-language.
In this section, we identify C structures that can be easily modeled in CVC4-language and structures
that are difficult to model. We will discuss how to address some difficult C structures in the next
section.
    CVC4-language provides a number of built-in types, such as integer, real, boolean, array, tu-
ple, record, bit-vector, and function. This makes it easier to model basic type instance and some
structures in C program. There are two big differences between CVC4-language and most other
programming languages. Firstly, instances in CVC4-language can never change their value after
they are defined. Secondly, if an instance is not assigned an initial value when it is defined, it has a
non-deterministic value rather than a default value as in C language. To avoid ambiguity, we avoid
using “variable” to refer to an instance in CVC4-language program.

3.1     Simple structures
3.1.1    Data types
CVC4-language has several built-in types corresponding to the basic types in C program. Specifically,
integers, floating point numbers, and boolean variables can be modeled with built-in types INT, REAL,
and BOOLEAN. User defined basic type is also supported but as uninterpreted type whose domain is
unknown[1].
    Here is an example of how struct in C program can be modeled with RECORD in CVC4-language.
struct Pair



                                                   3
{
     int x;
     double y;
};
     The C code above can be represented in CVC4-language as follows.
Pair :    TYPE = [# x :   INT, y :   REAL #];
   For pointers in C language, we model the memory with one array for each data type used in the
program. We then model a C pointer as an integer instance associated with an array index as the
memory address by an ASSERT statement in CVC4-language.
int i;
double d;
int *ip = &i;
double *dp = &d;
     It can be represented in CVC4-language as follows.
Memory int : TYPE = ARRAY INT OF INT;
Memory real : TYPE = ARRAY INT OF REAL;
MEMORY : TYPE = [# mem int : Memory int, mem real :       Memory real #];
mem : MEMORY;
i : INT;
r : REAL;
ip, dp : INT;
ASSERT(mem.mem int[ip] = i);
ASSERT(mem.mem real[dp] = d);


3.1.2    Operation
Common arithmetic operators for basic data types are supported in CVC4-language. Besides,
one can access members in record or tuple with . (dot) operator such as instance.i for a tu-
ple where i is an integer constant indicating the serial number of the member being accessed, or
instance.member name for a record.
    One can also “update” an array or a record using WITH operator as follows.
Array new : ARRAY T1 OF T2 = Array old WITH [i] := newValue;
Record new : RecordType = Record old WITH .member name := newValue;


3.1.3    Function
A function in C can be modeled in CVC4-language as an instance of type (T1, T2, ..., Tn) -> T,
where T1, T2, ..., Tn on the left-hand side are the types of parameters and T on the right-hand
side is the type of return value. We use LAMDA expression and LET statement to specify a concrete
function of its type. When modeling functions in C program, we use an instance of the memory
array as an extra parameter and part of the return value. This enables changes made on instances
in the function body to be visible from outside. An example is given below.
int GetRowLength(TableHeader table header, int index)
{
    int row length = 0;
    row length += column length[index];
     return row length;
}



                                                 4
   This C function can be represented in CVC4-language as follows.
GetRowLength : (TableHeader, INT, MEMORY) -> [INT, MEMORY]
= LAMBDA(table header : TableHeader, index : INT, mem : MEMORY) :
LET
    row length = 0,
    row length new = row length + column length[index],
IN (row length new, mem);
   An exception is that CVC4-language doesn’t support recursive function. We’ll discuss the prob-
lem of recursion in Section 3.2.2.

3.1.4   Branching
As one of the mostly used constructs in C program, the if-else branching is supported by CVC4-
language. It commonly can be simply modeled with an IF-THEN-ELSE statement of the following
form where bi are expressions returning boolean value and ti are statements.
IF b1 THEN t1 ELSIF b2 THEN t2 ELSIF ...    ENDIF

3.1.5   Function pointer
Function pointer is not supported by CVC4-language, but we can model it with IF-THEN-ELSE
statements. The method here is to associate an unique integer with each function as their address,
and comparing the function pointer with these possible function addresses to decide which function
to call.
    A simple example is given below.
int EqualInt4(unsigned long value1, unsigned long value2)
{
    return (int)value1 - (int)value2;
}
int LessthanInt8(unsigned long value1, unsigned long value2)
{
    if ((long)value1 < (long)value2)
    {
        return 0;
    }
    return 1;
}
typedef int (*PredicateOperatorFunc)(unsigned long, unsigned long);
PredicateOperatorFunc fp = &EqualInt4;
unsigned long column value;
unsigned long constant operand;
int result = fp(column value, constant operand);
   This C program can be modeled as follows.
FuncType Compare : TYPE = (INT, INT, MEMORY) -> [INT, MEMORY]
EqualInt4 : FuncType Compare
= LAMBDA(value1 : INT, value2 : INT, in mem : MEMORY) :
LET
    x = value1 - value2
IN (x, in mem);
LessthanInt8 : FuncType Compare
= LAMBDA(value1 : INT, value2 :     INT, in mem :   MEMORY) :
LET


                                                5
x = IF value1 < value2 THEN 0 ELSE 1 ENDIF
IN (x, in mem);
addr EqualInt4, addr LessthanInt8 : INT;
ASSERT DISTINCT (addr EqualInt4, addr LessthanInt8);
fp : INT = addr EqualInt4;
column value : INT;
constant operand : INT;
mem : MEMORY;
result : [INT, MEMORY] = IF fp = addr EqualInt4
                    THEN EqualInt4(column value, constant operand, mem)
                    ELSIF fp = addr LessthanInt8
                    THEN LessthanInt8(column value, constant operand, mem)
                    ELSE (0, mem)
                    ENDIF;


3.2     More complicated structures
3.2.1   Loop
Loops are difficult to model because CVC4-language does not allow loop iterators to be updated on
themselves. But we can approximate to loop behavior via induction.
    One straightforward intuition is unwinding the loop for exactly the number of iterations being
executed at runtime. However, there are two potential problems. First, the number of iterations of
a loop may be very large, which makes it impractical to unwind all iterations. Second, the number
of iterations of a loop may dependent on runtime data which is unknown at the static analysis time.
Therefore, we have to think of another idea to model loops in CVC4-language.
    For a C program with a single loop, if a variable remains the same value before the loop, at the
bottom of the loop body for all possible execution path, and after the loop, this variable can be
considered as an invariant. This conclusion can be proved by induction. Therefore, each loop in
the C program can be modeled with only one iteration. Note that we have to model all possible
execution paths in the loop body in this one iteration to guarantee correctness. This modeling
guarantees that all variables being labeled as invariants are indeed unchanged.
    In some cases, however, the modeling method presented above fails to recognize some invariants
because the information presented by a single iteration is not enough. One example of these excep-
tions is listed below. In this example, sum has the same value at the second line and after the loop.
But modeling with only one iteration cannot recognize this fact.
int arr[5] = {1, 2, 3, 4, 5};
int sum = arr[0] + arr[1] + arr[2] + arr[3] + arr[4];
int i;
sum = 0;
for (i = 0; i < 5; ++i)
{
    sum += arr[i];
}


3.2.2   Recursive function
Because CVC4 doesn’t support recursion, a recursive function has to be transformed into iteration.
When it comes to loop, the problems are the same with those we have just described above.




                                                 6
3.2.3   Address of members in structures
In our method, we model the memory with an array for each C basic type, and associate an instance
with an address by ASSERT statement. So each instance has only one address, including structures
like tuple, record, and array. The reference to a member in an instance of these structures is a
potential problem.
    One possibility might be whenever the adress of a structure’s member is used, we simply give it
an undefined value. However, if this address is dereferenced by an update operation later, CVC4
considers that all instance in the same memory array may be changed because this dereferenced
address has a non-deterministic value. A naive fix-up is to assert that this address is distinct from
all other addresses used in the same program. It, however, doesn’t work in the following case.
struct T1
{
    int idx;
};
struct T2
{
    T1 t;
};
int arr[5] = {1, 2, 3, 4, 5};
T1 t 1;
t 1.idx = 0;
T2 t 2;
t 2.t = t 1;
T1 *tp = &t 2.t;
arr[tp->idx] = 0;
    In this program, tp actually points to t 1. But since we cannot model &t 2.t, we assign an
unknown value which is distinct from all other addresses to tp. Because tp is non-deterministic,
so is tp->idx. As the result, all element in arr are considered to be possibly changed by the last
statement even though only the first element should be changed according to the semantics of the
original C program.
    Our first attempt is to extend the address from an integer to a structure including a base address
and an offset. Also, all the structs in C are modeled with tuples in CVC4-language such that the
member of their instance can be accessed with an offset rather than a name.
ADDRESS : TYPE = [# base : INT, offset : INT #];
Memory someStruct : TYPE = ARRAY INT OF SomeStructure;
addr : ADDRESS;
ASSERT(mem.Memory someStruct[addr.base] = someInstance);
   In the code above, base is the index of the target instance in memory array and offset indicates
the number of the target member in this instance. Unfortunately, we do not use this method because
mem.Memory someStruct[addr.base].(addr.offset) is an illegal expression in CVC language. Another
problem is that if a function receives a structure member address and a new value for an update,
unless the type of the host structure is known in the context, this function doesn’t know which
memory array to update. A simple C example is given below:
void update(int *ip, int new)
{
    *ip = new;
}
update(someInstance.int member, 0);
   Focusing on these two issues, our second attempt is to store structure members separately. The


                                                  7
main idea here is to use a memory array for each basic types and put the structure members in these
arrays corresponding to their types.
    For each record R : TYPE = [# t1 : T1, t2 : T2, ..., tn : Tn #] where Ti(0 < i ≤ n) is a
basic type, the address structure is ADDRESS : TYPE = [# base : INT, offset : INT #], just like
our first attempt. The index of memory arrays, however, is not an integer but an instance of type
ADDRESS, which means that for an instance r of R whose base address is k, the value of ti in r resides
at (k, i) in the memory array for Ti.
ADDRESS : TYPE = [# base : INT, offset : INT #];
R : TYPE = [# t1 : T1, t2 : T2, ..., tn : Tn #];
Memory R : TYPE = ARRAY INT OF R;
Memory T1 : TYPE = ARRAY ADDRESS OF T1;
ASSERT(mem.Memory R[k] = r)
addr : ADDRESS = [# k, i #];
ASSERT(mem.Memory T1[addr] = valur of ti);
    With this modeling, the target array of an update is known once we know the type of the structure
member to be updated. Since the address structure is used as the index of memory arrays, there is
no syntax problem. Unfortunately, two other problems emerge for more complex programs. First,
we need a more complex address structure to model possibly nested C program structs. Second,
storing structure members separately according to their types makes it difficult to compare two
arrays of structures in their entirety, which is sometimes useful.


4     Heuristic of modeling with weaker precision
In Section 3.2.3, we have seen that it is difficult to model address of members in structures, but it is
possible that some program invariants are not influenced by this kind of address. In this situation,
we would like partially model the program to find invariants not influenced by structures that we
cannot model accurately. A simple example to illustrate our idea is given below:
void foo(struct ComplexType c1, int i) {
    int *mp = &c1.member1;
    int cnt = 0;
    while (cnt < 100) {
        if (i) {
            cnt++;
            *mp += cnt;
        }
    }
}
    In this example, we cannot model mp accurately, but i is not influenced by mp and the value of
i is an invariant. If we can identify the part of the program not influenced by mp, we could model
this part of the program and identify the invariant of i.
    In general, we would like to model parts of a program and detect invariant properties as long
as they are not influenced by complex structures that we cannot accurately model. Since there is
always a complicated interrelationship among variables in programs, it is necessary to determine
how variables are influenced by each other.
    The rest of this section propose an initial idea of determining the influence among variables in a
program and modeling the parts of the program not influenced by variables that we cannot model
accurately.

4.1    Methodology
Before presenting the method to compute the interrelationship among variables, we first make some
claims.


                                                   8
     Def inition1: We define that a variable vi depends on a variable vj if and only if the change to
the value of vj may cause the change to the value of vi . And we say that vi is polluted by an item
t if we cannot model vi accurately without knowing how to model t.
    Claim1: In any C program P , there is a variable v being polluted by item t iff v depends on t.
    P roof : First, we prove that if a variable v is polluted by an item t, v depends on t by contra-
diction. Suppose a variable v is polluted by an item t but does not depend on t. v doesn’t depend
on t means that the change to the value of t will not influence the value of v. So v either has a
deterministic value or an unknown value, which means that we can model v simply with this value.
But we supposed that v is polluted by t, which indicates that we cannot model v, so there is a
contradiction. Therefore, if a variable v is polluted by an item t, v depends on t
    Now, we prove that if a variable v depends on an item t, v is polluted by t by contradiction.
Suppose that there is a variable v that depends on t while v is not polluted by t. v depends on t
means that the change to the value of t may cause the change to the value of v. So we cannot model
v accurately without knowing how to model t. But we’ve supposed that v is not polluted, which
means that we can model v, so there is a contradiction. Therefore, if some variable v depends on
item t, v is polluted by t.
    Claim2: In any C program P without function call, there is a variable being polluted by an item
t only if t appears in assignment statements.
    P roof : The statements in program can be roughly classified into three categories, assignment
statement, control statement, and variable definition. Note that we consider a compound statement
as a series of separate statements here.
    For t appearing in variable definition, other variables will not be polluted because there is no
other variable introduced in a variable definition.
    For t appearing in control statement as a condition, it influences the execution path rather than
other variables. Suppose there is an if-else branching in P as follows where t appears in condition 1,
because we cannot model t, we cannot model condition 1 either. But for any variable in statement j ,
the only possible relationship between its value and t is that its value, which can be modeled as
either its original value or the value appears in statement j , may depend on the execution path.
Since all the possible values of this variable can be modeled, it’s not polluted by the item t.
if (condition 1)
{
     statement 1;
     statement 2;
     ...
     statement k;
}
else
{
     statement k+1;
     statement k+2;
     ...
}
     For t appearing in assignment statement, however, other variables may be polluted because there
is either an explicit or implicit dependency between them. We’ll see which variables are polluted by
t if t appears in assignment statements in the following claims.
    Observation: Every single assignment in a C program without function call can be transformed
into a series of simple assignment statements in the form of x = op(y1 , y2 ) or ∗x = op(y1 , y2 ) where
op is a single operator other than function call, and x, y1 , y2 are simple variables. (The case of
x = op(y1 ) and ∗x = op(y1 ) is even simpler and can be inferred from the case using binary operator
directly.)
   Claim3: In simple assignment x = op(y1 , y2 ), x may be polluted if either of y1 and y2 is polluted.


                                                   9
    P roof : We prove this claim by contradiction. Suppose that in this assignment, x is polluted
while none of y1 and y2 is polluted. Since x depends on y1 and y2 , and both y1 and y2 are not
polluted indicates that we can model them accurately, we can model x accurately with a given op.
So x is not polluted. But we supposed that x is polluted, which is a contradiction. Therefore, x
may be polluted if either of y1 and y2 is polluted.
   Def inition2: We define a variable v to be the base variable pointed by a pointer x iff the object
pointed by x is v itself, or the pointed object is a member of v and v is not a member of any other
variables.
     Claim4: In simple assignment ∗x = op(y1 , y2 ), the base variable pointed by x may be polluted
if either of x, y1 , y2 is polluted.
     P roof : We prove this claim by contradiction. The semantic of ∗x = op(y1 , y2 ) is assigning the
value of op(y1 , y2 ) to the object pointed by x. Suppose that in this assignment, the base variable
pointed by x is polluted while none of x, y1 and y2 is polluted. All of x, y1 and y2 are not polluted
indicates that we can model them accurately. Since the new value of the base variable depends on
y1 and y2 , now we know which object should be assigned with what value, which means that we
can do this assignment deterministically. So the base variable pointed by x is not polluted. But we
supposed that the base variable is polluted, which is a contradiction. Therefore, the base variable
pointed by x may be polluted if either of x, y1 and y2 is polluted.

4.1.1   Constructing interrelationship graph
Now we present a way to decide which variables in a C program are polluted by a given item t. To
find all the variables being polluted by t in a program P , we construct a directed graph G = (V, E)
in the following way.

  1. Inline all the functions used in P .
  2. Transform all the assignments to a series of simple assignment statements. Let P ′ be the new
     program.
  3. For each variable vi in P ′ , add a vertex ui to G.
  4. For each simple assignment x = op(y1 , y2 ), add edges (y1 , x), (y2 , x) to G.
  5. For each simple assignment ∗x = op(y1 , y2 ) where v is a base variable pointed by x, add edges
     (y1 , v), (y2 , v), (x, v) to G.

    With this directed graph G representing the interrelationship among variables in P , we can label
all the variables that are polluted by a given item t that we cannot model as follows.
  1. For each assignment statement in P , if t appears on the right-hand side, label the vertex
     corresponding to the variable on the left-hand side if it is a single variable, or label the base
     variable pointed by it if it is a dereference.
  2. For each assignment statement in P , if t appears on the left-hand side as a pointer dereference,
     label the vertex corresponding to the base variable pointed by t.
  3. Run BreadthF irstSearching on G from the vertices being labeled and label all the vertices
     it can reach.
   The edges in G represents the dependencies among variables, and if a variable v depends on an
item t that we cannot model, we cannot model v accurately either. So v is polluted by the item
t. Therefore, when modeling the program P , we first assign an unknown value to all the variables
being labeled. Second, we remove all the statements involving dereference of unknown variables.
Finally, we replace all the control condition, such as condition of if statement, involving an unknown
variable with an unknown value of boolean type.


                                                   10
4.1.2   A problem in this method

There is, however, a problem with function inlining. Considering function inlining, functions can be
classified into three categories: regular functions, recursive functions, and library functions. Regular
functions can be inlined in the regular way, while it is problematic to inline recursive functions and
library functions. The problem of recursive function inlining is that there is still a function call after
inlining. And library functions cannot be easily inlined because we do not have the source code of
them.
    Our first attempt is to inline the recursive function but set all the branch conditions in it to be
non-deterministic, and ignore the recursive call. The reason is that any variable actually changed
by a function call should be assigned a new value in some statement other than the recursive call in
the function body. But a counterexample is listed below.
void RecursiveFunction(int *intArray, int index)
{
    intArray[index] = 0;
    if (index >= 2)
    {
        RecursiveFnction(intArray, index - 2);
    }
}
   Obvious that by inlining only one call, we cannot reach all the indices where the elements of
array are changed. Someone may think that we could set the arguments being modified in the
recursive call to be non-deterministic, but it is possible that some of those arguments are pointers
and a non-deterministic pointer could cause more pollution.
   The problem to library functions is the same because we do not know the semantics of these
functions. Given the semantics of them, maybe we could do something further.

4.2     Formal proof
In this section, we give a proof that the variables whose corresponding vertices are not labeled in G
will not be polluted by a given item. To prove this conclusion, we first give some claims.
     Claim5: A variable vi depends on a variable vj if and only if there is a path in G from uj to ui .
     P roof : First, we prove that if there is a path in G of length k from uj to ui , vi depends on vj .
We prove this conclusion by induction of k.
     Base case: When k = 1, uj is adjacent to ui , which means that there is an edge (uj , ui ) in G.
Recall the construction of G, in either case where we add an edge (uj , ui ) to G, the value of vi
depends on the value of vj .
     Induction hypothesis: Suppose a path of length k from uj to ui in G implies that vi depends on
vj .
     Induction step: Let p = un1 , un2 , un3 , ..., unk , unk+1 be a path of length k+1 from un1 to unk+1 .
Since p is a path of length k+1, p′ = un1 , un2 , un3 , ..., unk is a path of length k. Because we supposed
that a path of length k from uj to ui in G implies that vi depends on vj , and an edge (unk , unk+1 )
indicates that the value of vnk+1 depends on the value of vnk as we’ve shown in the base case, we
know vnk depends on vn1 and vnk+1 depends on vnk . So vnk+1 depends on vn1 .
     Now we prove that if vi depends on some variable vj , there is a path in G from uj to ui by
contradiction.
     Suppose that there is variable vi depends on some variable vj while there is no path from uj
to ui in G, we’ll show a contradiction. Because vi depends on vj , vi depends directly on either vj
itself or another variable vm depending on vj . If vi depends directly on vj , there must be an edge
from uj to ui according to our construction. So there is a path of length 1 from uj to ui . But we
supposed that there is no path from uj to ui , which is a contradiction. If vi depends directly on
another variable vm that depends on vj , there must be no path from uj to um because otherwise
there is an edge from um to ui according to our construction and thus a path from uj to ui through


                                                    11
um . Likewise, vm depends directly on either vj itself or another variable depending on vj . If we
trace back like this, we can finally find a vertex vd which depends directly on vj yet there is no
edge from uj to ud . But according to our construction, there must be an edge (uj , ud ), which is a
contradiction. Therefore, if vi depends on some variable vj , there is a path in G from uj to ui .
    Claim6: A variable vi in P is polluted by t if and only if there is a path in G from a labeled
vertex to the vertex ui .
    Before we prove this claim, we first show that the initial labeled vertices are polluted. According
to our construction of G, the initial labeled vertices are those corresponding to variables which
appear on the left-hand side of some assignment statements where t appears on the right-hand side.
These variables are polluted because their values depend on the value of t, and we cannot model
them without knowing how to model t.
    P roof : First, we prove that if there is a path in G from the vertex ui to a labeled vertex up , vi
in P is polluted. Because there is a path in G from the vertex ui to a labeled vertex up , the value
of vi depends on the value of vp . Since vp is polluted by t as we showed above, which means that vp
depends on t, vi also depends on t. So vi is polluted.
    Now, we prove that if a variable vi in P is polluted by t, there is a path in G from a labeled
vertex up to ui .
    Because vi is polluted by t, vi depends on t. So vi depends directly on either t itself or another
variable vm depending on t. If vi depends directly on t, ui is an initial labeled vertex according to
our construction. So there is a path of length 0 from a labeled vertex to ui . If vi depends on another
variable vm depending on t, there is a path from um to ui . Likewise, vm depends directly on either
t itself or another variable depending on t. If we trace back like this, we can finally find a vertex vd
which depends directly on t. According to our construction, vd is an initial labeled vertex, so there
is a path from a labeled vertex to vi .
    So far, we have shown that a vertex ui is accessible from a labeled vertex iff the variable vi is
polluted by the item t. Because we cannot model these variables, we label all the variables accessible
from a labeled vertex and assign a non-deterministic value to them. Also, considering that some
of these variables may be pointers and it’s unsafe to dereference a non-deterministic pointer, we
remove the assignment statements where a dereference of an unknown pointer appears. It is safe to
remove a dereference of non-deterministic pointer because the base variable pointed by it is labeled
and assigned a non-deterministic value. Finally, the non-deterministic value of labeled variables will
not influence unlabeled variables because all the vertices accessible from them have already been
labeled, which means that the value of unlabeled variables do not depend on them. Therefore, it is
safe to make them non-deterministic.

4.3    Example
As an example, we present a function extracted and simplified from one of our tiny prototype. The
item that we cannot model is &((*predicates)[i]) which appears in SequentialScan .
int SequentialScan(int scan direction,
                int num predicates,
                Predicate** predicates,
                const TableHeader* schema)
{
    column offset = 0;
    for (i = 0; i < schema->num columns; ++i)
    {
        column type = schema->column definitions[i].column type;
        if (column type == DATATYPE INT4)
        {
            row values[i] = *(int*)&(row data[column offset]));
            column offset += 4;
        }


                                                  12
        else if (column type == DATATYPE INT8)
        {
            row values[i] = *(long*)(&(row data[column offset]));
            column offset += 8;
        }
    }
    column value = 0;
    current predicate = NULL;
    for (i = 0; i < num predicates; ++i)
    {
        current predicate = &((*predicates)[i]);
        column value = row values[current predicate->column id];
    }
    return 0;
}
   Given this program, we first transform each assignment to a series of simple assignment state-
ments as follows. And then construct a graph according to the variables and dependencies among
them.
int SequentialScan(int scan direction,
                 int num predicates,
                 Predicate** predicates,
                 const TableHeader* schema)
{
    column offset = 0;
    for (i = 0; i < schema->num columns; ++i)
    {
        TableHeader schema inst = *schema;
        ColumnDefinition *col def;
        col def = schema inst.column definitions;
        ColumnDefinition col def i;
        col def i = col def[i];
        column type = col def i.column type;
        if (column type == DATATYPE INT4)
        {
            int *row value i;
            row value i = row values + i * sizeof(int);
            *row value i = row data[column offset];
            column offset += 4;
        }
        else if (column type == DATATYPE INT8)
        {
            int *row value i = row values + i * sizeof(long);
            *row value i = row data[column offset];
            column offset += 8;
        }
    }
    column value = 0;
    current predicate = NULL;
    for (i = 0; i < num predicates; ++i)
    {
        Predicate *predicates arr;
        predicates arr = *predicates;
        Predicate predicate i;


                                               13
          predicate i = predicates arr[i];
          current predicate = &predicate i;
          Predicate curr pred inst;
          curr pred inst = *current predicate;
          int col id;
          col id = curr pred inst.column id;
          column value = row values[col id];
      }
      return 0;
}



     schema       schema inst       col def       col def i        column type




column of f set      row values     row value i         row data        column values




                                                                                                  col id




    predicates     predicates arr      predicate i      current predicate        curr pred inst


   According to our construction, the initial labeled vertex is current predicate because
&((*predicates)[i]) appears in the statement current predicate = &((*predicates)[i]); . We run
BreadthF irstSearch on G from the vertex current predicate and label all the vertices being visited,
which is curr pred inst, col id and column value. we replace them with non-deterministic values.
    One potential problem of this method is that the transformation from each assignment to a series
of simple assignment statements introduces more variables, which increases the scale of the graph.
Also, when it is applied to larger and more complex programs, function inlining may be unpractical.


5      Conclusion
This paper describes our attempt of detecting program invariants with sophisticated analysis by
program verification tools. This work is motivated by the fact that some program invariants that
enable significant performance improvement can be identified by domain experts of the programs but
not compilers. One reason to this limitation of compilers is that compilers usually do not perform
expensive analysis due to performance concerns.
   We described four tools we have tried for invariant detection: one SMT solver and three C pro-
gram analysis tools based on SMT or SAT solvers. We noticed that these C program tools sometimes
take an approximation to the examined property and only tools taking over-approximation is safe


                                                   14
to use for invariant detection. These C program tools either take under-approximation or are not
robust enough for large programs.
    On the other hand, it is hard for SMT solver to model some complex C structures. For one of
these tools—CVC4, we described how we can model program behavior in its input language and
discussed challenges of modeling loops and addresses of structure members. Finally, we gave an
initial idea for identify a subset of invariants using CVC4 when some C structures in the program
cannot be modeling accurately.


References
 [1] CVC4’s native language. http://cvc4.cs.stanford.edu/wiki/CVC4%27s_native_language
     accessed June 2019.
 [2] Clark Barrett, Christopher L Conway, Morgan Deters, Liana Hadarean, Dejan Jovanović, Tim
     King, Andrew Reynolds, and Cesare Tinelli. Cvc4. In Computer-aided verification, pages 171–
     177. Springer, 2011.
 [3] Armin Biere, Alessandro Cimatti, Edmund Clarke, and Yunshan Zhu. Symbolic Model Checking
     without BDDs. In International conference on tools and algorithms for the construction and
     analysis of systems, pages 193–207. Springer, 1999.
 [4] Nikolaj Bjørner and Leonardo de Moura. Applications of SMT solvers to Program Verification.
     Notes for the Summer School on Formal Techniques, 2014.
 [5] Edmund Clarke, Daniel Kroening, and Flavio Lerda. A Tool for Checking ANSI-C Programs.
     In Tools and Algorithms for the Construction and Analysis of Systems, pages 168–176. Springer,
     2004.
 [6] Edmund Clarke, Daniel Kroening, and Karen Yorav. Behavioral Consistency of C and Verilog
     Programs Using Bounded Model Checking. In Design Automation Conference, 2003. Proceed-
     ings, pages 368–371. IEEE, 2003.
 [7] Leonardo De Moura and Nikolaj Bjørner. Z3: An efficient smt solver. In Tools and Algorithms
     for the Construction and Analysis of Systems, pages 337–340. Springer, 2008.
 [8] Alastair F Donaldson, Leopold Haller, Daniel Kroening, and Philipp Rümmer. Software Veri-
     fication Using k-Induction. In Static Analysis, pages 351–368. Springer, 2011.
 [9] Brain Martin, Joshi Saurabh, Kroening Daniel, and Schrammel Peter. Safety Verification and
     Refutation by k-Invariants and k-Induction. 2015.
[10] Mary Sheeran, Satnam Singh, and Gunnar Stålmarck. Checking Safety Properties Using Induc-
     tion and a SAT-Solver. In Formal Methods in Computer-Aided Design, pages 127–144. Springer,
     2000.
[11] Qiang Tu et al. Evolution in open source software: A case study. In Proceedings 2000 Interna-
     tional Conference on Software Maintenance, pages 131–142. IEEE, 2000.
[12] Julien Vanegue, Sean Heelan, and Rolf Rolles. SMT Solvers in Software Security. In Workshop
     on Offensive Technologies, pages 85–96, 2012.
[13] Wei Wang and Clark Barrett. Cascade. In International Conference on Tools and Algorithms
     for the Construction and Analysis of Systems, pages 420–422. Springer, 2015.
[14] Wei Wang, Clark Barrett, and Thomas Wies. Cascade 2.0. In Verification, Model Checking,
     and Abstract Interpretation, pages 142–160. Springer, 2014.
[15] Rui Zhang, Richard T Snodgrass, and Saumya Debray. Micro-Specialization in DBMSes. In
     Data Engineering (ICDE), 2012 IEEE 28th International Conference on, pages 690–701. IEEE,
     2012.


                                                15
