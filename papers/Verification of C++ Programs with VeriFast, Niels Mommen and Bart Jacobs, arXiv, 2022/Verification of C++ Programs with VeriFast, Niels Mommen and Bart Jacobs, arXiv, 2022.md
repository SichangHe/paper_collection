                                         Verification of C++ Programs with VeriFast
arXiv:2212.13754v1 [cs.LO] 28 Dec 2022




                                                          Niels Mommen and Bart Jacobs

                                           imec-DistriNet Research Group, KU Leuven, Belgium

                                                  {niels.mommen, bart.jacobs}@kuleuven.be

                                                                     December 2022


                                                                           Abstract
                                               VeriFast is a prototype tool based on separation logic for modular
                                           verification of C and Java programs. We are in the process of adding
                                           support for C++. In this report, we describe the features of C++
                                           for which we added support so far, as well as the proof obligations
                                           we generate for these features. At this point, VeriFast has basic sup-
                                           port for most object-oriented programming features of C++: member
                                           functions, member function and operator overloading, implicit and
                                           explicit conversions, constructors and initializer lists, destructors, ref-
                                           erence types, allocation and deallocation on the stack or on the heap
                                           (using new and delete), inheritance (including multiple inheritance
                                           but not virtual base classes), and virtual member functions and over-
                                           riding. To support specification of inheritance hierarchies, we added
                                           support for instance predicates, which can be introduced in a base
                                           class and overridden in derived classes. The main missing feature at
                                           this point is support for C++ templates, which we plan to work on
                                           next.




                                                                               I
Contents
1 Introduction                                                               1

2 C++ basic features                                                         1

3 Classes and objects                                                        2
  3.1 Construction of objects . . . . . . . . . . . . . . . . . . . . . .    2
  3.2 Destruction of objects . . . . . . . . . . . . . . . . . . . . . .     3

4 Inheritance                                                                4
  4.1 Upcasts . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .    5
  4.2 Multiple inheritance . . . . . . . . . . . . . . . . . . . . . . .     5
  4.3 Construction and destruction . . . . . . . . . . . . . . . . . .       6

5 Virtual methods                                                        7
  5.1 Object types at run time . . . . . . . . . . . . . . . . . . . . . 8
  5.2 Construction and destruction . . . . . . . . . . . . . . . . . . 9
  5.3 Behavioural subtyping . . . . . . . . . . . . . . . . . . . . . . 11

6 Instance predicates                                                       13

7 Limitations                                                               16

8 Future work                                                               16




                                     II
1         Introduction
VeriFast1 is a prototype tool that performs modular symbolic execution for
modular verification of C and Java programs, based on separation logic [2].
Currently, support for verification of programs written in C++ is being
added to VeriFast. We use LibTooling, a library to write tools based on
Clang, to retrieve a typechecked abstract syntax tree for well-typed C++
programs 2 . This report describes the C++ features that are currently
verifiable by VeriFast and the changes that were needed in order to ver-
ify these features. The added features include verification of member func-
tions, constructors and destructors, and virtual member functions in the
presence of multiple inheritance. To conclude, present limitations and future
work is discussed. A snapshot of binaries and the source code of VeriFast
with C++ support at the time of writing is available as a Zenodo drop at
https://zenodo.org/record/7486648.


2         C++ basic features
A first extension added to VeriFast is support for lvalue references and the
new and delete operator for primitive types.

Lvalue references VeriFast treats lvalue references similar to pointers.
By default, an lvalue reference evaluates to the address the reference points
to. When an lvalue to rvalue conversion is needed to retrieve to value of the
object the reference points to, VeriFast implicitly dereferences the pointer.
Lvalue reference types are currently not supported in ghost code. It is how-
ever possible to reason about an object that is referenced by an lvalue refer-
ence by taking the address of that reference, which is equivalent to a pointer
to that object.

new and delete The new and delete operators in C++ are the coun-
terparts of malloc and free in C. However, it is not allowed to use them
interchangeably: an object allocated on the heap through new cannot be
    1
        https://github.com/verifast/verifast
    2
        https://clang.llvm.org/docs/LibTooling.html




                                         1
destroyed by passing the address returned by new to free. Therefore, Veri-
Fast respectively produces and consumes a new block when calling new and
delete, instead of malloc block chunks.


3       Classes and objects
Classes in C++ are an extended form of structs in C. First, optional default
expressions can be specified for data members. Such an expression is evalu-
ated to initialize the data member when an instance of the class, an object,
is created.
    During object creation of class type S at address addr, VeriFast traverses
each field of S in their order of declaration and produces a corresponding
field chunk S field name (addr,value )3 , where field name is the name of
the class field and value either is the evaluation result of field name’s default
member initializer or represents an unspecified value in case no initializer is
present.
    Next to data members, static and non-static member functions can be
defined. A non-static member function always has an implicit this parame-
ter, which is a pointer to an instance of the declaring class: it points to the
target of the function call.
    When verifying a non-static member function, VeriFast produces a fresh
symbol that represents its implicit this argument, which is assumed to not
be zero, i.e. not a null pointer. Verification of a non-static member function
continues as usual: first the precondition is produced, next the compound
statement of the function body is verified, and finally the postcondition of
the function is consumed and a check is performed to verify that no chunks
are leaked. Calling a member function on a null pointer results in unde-
fined behaviour. Therefore, a member function cannot be called when it not
possible to prove that the target object of the member function call is not
zero.

3.1     Construction of objects
A constructor in C++ is a special member function of a class that cannot
be called directly; it is automatically called when an instance of that class is
    3
    A points-to chunk a ->field name |-> v can alternatively be used to refer to a field
chunk at address a with value v.


                                           2
created. Multiple constructors can be defined within a class. An applicable
constructor is selected using overload resolution when an object is created.
     A constructor consists of an optional initializer list and a body consisting
of a compound statement. During construction, all fields are initialized in
their declaration order prior to executing the destructor’s body. An initializer
list optionally defines data member initializer expressions which take prece-
dence over the default member initializers declared in its class. Therefore,
during field initialization of data field m of an object of class type S, Veri-
Fast selects the appropriate expression from the initalizer list if it mentions
m. Otherwise, the default member initializer is used if available or the field is
initialized using its default constructor when the field type is a class type, or
it is initialized with an unspecified value if the field type is a primitive type.
Accordingly, verification of a constructor consists of the following steps:

   1. Initialize fields in order of declaration, where entries in the initializer
      list take precedence over default member initializers;

   2. Symbolically execute the constructor body.

    An initializer list of constructor C of class type S can alternatively consist
of exactly one call to another constructor C’. This skips field initialization
and delegates construction to the applicable constructor C’ selected using
overload resolution, in which case VeriFast verifies a call to C’. Afterwards,
construction continues by verifying the body of C.
    An object can either be allocated on the stack or on the heap. A stack-
allocated object of class type S is created when a variable of type S is declared
by automatically verifying a call to an applicable constructor. Objects can be
allocated on the heap by invoking a new expression. This expression invokes a
call to an applicable constructor and returns a pointer to the object that has
been allocated on the heap. Verification of a new expressions for an object of
class type S first verifies a call to the constructor and additionally produces a
new block S(addr ) chunk analogously to a malloc block S(addr ) chunk
in C, where addr is the address in the heap at which the object was created.

3.2    Destruction of objects
Destructors are the counterpart of constructors: they are called automatically
when the lifetime of an object ends. Contrary to constructors, destructors
do not have an equivalent counterpart of an initializer list.

                                        3
    Verification of a destructor D for an object of class type S at address addr
happens in reverse order of verifying a constructor of S. First, the destructor
body is verified. Next, all fields of the object are destroyed in reverse order
of their declaration. For a field m of primitive type, its corresponding field
chunk S m(addr, ) is consumed, where represents a dummy pattern which
matches any value. Fields that are of class type S’ are destroyed by verifying
a call to the destructor of S’. Verification of a destructor performs following
the steps:

    1. Symbolically execute the destructor body;

    2. Destruct fields in reverse order of declaration.

    Objects that are allocated on the stack are automatically destroyed at the
end of their scope by verifying a call to their destructor. Explicitly calling a
destructor on a stack-allocated object is not allowed by VeriFast. This would
lead to undefined behaviour when an object gets destroyed automatically at
the end of its scope when it was already explicitly destroyed.
    For an object that was allocated on the heap at address addr, the delete
operator can be used to destruct its operand. Verification of a delete addr
expression, where addr is a pointer to an object of class type S, takes place
in two steps. First, a call to the destructor of S is verified. Afterwards,
a new block S(addr ) chunk is consumed. This guarantees that an object
allocated on the heap is never destroyed twice, which would otherwise lead
to undefined behaviour.


4      Inheritance
A class in C++ can extend another class, inheriting all accessible members
from the class it extends. When class D extends class B, B is called a (direct)
base class of D and D is a derived class of B.
    VeriFast models a base object of class type B as a subobject in a derived
object of class type D. For an object d of class type D created at address
d addr, its base object of class type B can be accessed through a field pointer
field ptr(d addr, D B offset), where D B offset represents an offset, ≥
0, from d to its base object of class type B.




                                        4
4.1    Upcasts
Upcasting a derived object to its base object is supported by VeriFast both
implicitly and explicitly. Such a cast is first required when accessing a base
field member. Second, a cast is needed when passing a derived object as
an argument to a function or method parameter that expects a base object,
base object pointer or reference. Lastly, casting a derived object to its base
object is required when calling a base member function on a derived object.
    The evaluation of an upcast from a derived object of class type D at
address d addr to a base object of class type B is executed in two steps. First
a check is performed to make sure that D derives from B. Next, a field pointer
field ptr(d addr, D B offset) is computed to retrieve the address of the
base object.
    Note that implicit upcasts are limited in ghost code. The type checker
of VeriFast automatically inserts them when it is able to deduce the need
for such a cast. This is currently not supported when a points-to notation is
used to reason about base fields in a derived object. E.g., B m(d addr, ?m )
implicitly involves an upcast to access base field m from derived object d,
while ((B *) d addr)->m |-> ?m requires an explicit upcast to access the
same field.

4.2    Multiple inheritance
C++ offers the feature to derive from multiple base classes. Treating base
classes as subobjects through field pointers in VeriFast includes support for
multiple inheritance. Fields of any base object can be accessed by first up-
casting the derived object to the base, prior to accessing the field in that
base. Similarly, visible base member functions from any base can be used
through a derived object by first implicitly or explicitly performing an upcast
to the base target.
    In the presence of multiple inheritance, an implicit upcast from a
derived object to a base object might be ambiguous when multiple base
classes derive from the same class. Assume a diamond scenario where
class D derives from both class B and class C, and classes B and C in
turn both derive from class A. In this scenario, an object of class type
D at address d addr has two subobjects: one object of class type B at
address field ptr(d addr, D B offset) and another object of class type
C at address field ptr(d addr, D C offset). These subobjects both


                                      5
have one subobject of class type A themselves at respectively address
field ptr(field ptr(d addr, D B offset), B A offset) and address
field ptr(field ptr(d addr, D C offset), C A offset). Accessing a
field m of class A from d addr is ambiguous: it not clear whether this refers
to field m reachable through the subobject of class type B or the subobject
of class type C. Hence, an explicit cast is required to render the upcast
unambiguous. E.g., A m((B *) d addr, ?m val) can be used to reason
about field m in the subobject at address field ptr(field ptr(d addr,
D B offset), B A offset).

4.3    Construction and destruction
Verification of constructors and destructors in the presence of inheritance
requires additional steps in the verification process. Verifying a constructor
first starts with constructing all base classes in declared derivation order if the
constructor being verified is not a delegating constructor. Next, verification
proceeds as described before in Section 3.1.
    VeriFast verifies the construction of bases by verifying a call to a base
constructor of each direct base class. An appropriate base constructor is se-
lected by overload resolution if the initializer list of the constructor mentions
a base class initialization, otherwise the default base constructor is used.
The value of the implicit this argument passed to the base constructor is
calculated by performing an upcast from the current constructor’s implicit
this parameter to the base object that will be constructed by verifying the
selected constructor call. E.g., when verifying a base constructor call of class
B in the constructor of derived class D for an object at address d addr, a value
field ptr(d addr, D B offset) is passed as the implicit this argument to
the constructor call of class B.
    Verification of a destructor accordingly accounts for inheritance. After
following the verification steps for destruction listed in Section 3.2, VeriFast
first verifies a call to each destructor of all direct bases in reverse order of
derivation if the class object to be destroyed has any base objects. Anal-
ogously to constructors, an upcast to the base object is performed when
calculating the value passed as the implicit this argument to the base de-
structor verification call.
    Care has to be taken during construction and destruction of objects
in the presence of inheritance. Member functions can be called directly
and indirectly during construction or destruction, but this results in

                                        6
undefined behaviour if not all bases have been fully constructed. Therefore,
an S bases constructed(S *s addr ) chunk is introduced to determine
whether all bases for an object of class type S at address s addr have been
constructed. This chunk is required when verifying a member function call
where the target object derives from at least one class, disallowing calling
any member function when this chunk is not available.
   Verification of a constructor can now be summarized by the following
steps:

    1. Verify a constructor call for each base class in order of derivation;

    2. Produce an S bases constructed(s addr ) chunk if S derives from at
       least one class, where S is the class type of the object that is currently
       being constructed and s addr is the address of the object;

    3. Initialize fields in order of declaration, where entries in the initializer
       list take precedence over default member initializers;

    4. Symbolically execute the constructor body.

   Verification of a destructor now additionally destructs base classes and
optionally consumes a bases constructed chunk:

    1. Symbolically execute the destructor body;

    2. Destruct fields in reverse order of declaration;

    3. Consume an S bases constructed(s addr ) chunk if S derives from at
       least one class, where S is the class type of the object that is currently
       being destructed and s addr is the address of the object;

    4. Verify a destructor call for each base class in reverse order of derivation.



5      Virtual methods
A Member function can be declared virtual with the virtual keyword. This
allows to override the member function in derived classes. Dynamic dispatch
is used to select the appropriate member function implementation when an
unqualified member function call is evaluated: the dynamic type of the target

                                         7
object is inspected at run time in order to select a member function imple-
mentation. That is, if a virtual member function is called on a base object,
dynamic dispatch selects the final overrider. A virtual member function in a
base class is a final overrider if no derived class declares a member function
that overrides it. Qualified member function calls are interpreted as stati-
cally bound calls, not resulting in dynamic dispatch at run time. A class
(object) that has at least one virtual member function, will be referred to as
a polymorphic class (object).

5.1     Object types at run time
In order to reason about virtual member functions and polymorphic classes,
VeriFast first introduces a typeid construct that can be used in ghost code.
This construct acts similar to the typeid operator in C++: it takes one
argument, a type expression, and returns a reference to an std::type info
object which uniquely represents that type. The difference is that typeid in
VeriFast only accepts type expressions as its argument, whereas the typeid
operator in C++ accepts any expression. A typeid(S) evaluates to value
S type info, where S is a type expression referring to class type S.
    In addition, for each polymorphic class S, VeriFast introduces a predicate
S vtype(S *s addr ; std::type info *s info). This predicate allows to
reason about the run-time type or its most derived type. In case class S has
at least one polymorphic base, this predicate is defined as
/* @ p r e d i c a t e S _ v t y p e( S * s_addr , std :: t y p e _ i n f o * s_info ) =
     B 0 _ v t y p e( s_addr , s_info ) &*&
     B 1 _ v t y p e( s_addr , s_info ) &*&
     ... &*&
     B n _ v t y p e( s_addr , s_info ) ;
@ */

where B0 , . . . , Bn are polymorphic direct base classes of S with n > 0. Oth-
erwise, the vtype predicate is opaque and cannot be opened or closed.
    This allows to open a vtype chunk of a polymorphic class in order to
retrieve all vtype chunks of its polymorphic direct bases. Analogously, all
vtype chunks of polymorphic direct base objects are required to close a vtype
chunk of a polymorphic derived object.
    When verifying a virtual member function call on a target object at ad-
dress s addr with static class type S, VeriFast first checks that (some fraction
of) an S vtype(s addr, ) chunk is available. Otherwise, the member func-

                                              8
tion call is not allowed. In order to call a base member function on a derived
target object, the vtype chunk of the derived object can be opened to obtain
a vtype chunk for the base object.

5.2    Construction and destruction
To be able to call virtual member functions, vtype chunks for polymorphic
objects have to be produced at some point during construction. These chunks
then have to be consumed during destruction of an object.
    Like regular member functions, virtual member functions can be called
during construction and destruction of an object. However, in presence of
multiple inheritance, care has to be taken. First, during construction or
destruction of an object, the virtual function called is the final overrider in
the constructor or destructor class. Hence, potential overriders in derived
classes are not taken into account during the construction or destruction of
a base class.
    A second point of attention is the presence of multiple inheritance. Dur-
ing construction and destruction, virtual base member function calls on the
object under construction or destruction are only allowed for bases that be-
long to the inheritance sub hierarchy of that object. Otherwise, if a virtual
member function is called on a subobject belonging to another branch of
the inheritance hierarchy, the virtual member call would result in undefined
behaviour.
    Listing 1 illustrates an example where virtual base member functions
are called in the constructor of C. These calls are allowed because at the
time of the call, both base A and B are fully constructed and they belong to
the inheritance hierarchy of C. However, the constructor of B that is called
through the constructor of class C would lead to undefined behaviour because
it calls member function foo of base class A: the subobject of class type A is
fully constructed, but it does not belong to the inheritance hierarchy of the
subobject of class type B.
    In order to address these instances where calling virtual member
functions would lead to undefined behaviour, VeriFast produces the
D vtype(d addr, D type info) chunk in the constructor of polymorphic
class D after all its bases have been constructed, where d addr is the
address of the object that is constructed. Right after a constructor of a
polymorphic base class B has finished, the derived constructor of class D
consumes the B vtype(field ptr(d addr, D B offset), B type info)

                                      9
struct A {
   v i r t u a l void foo () {}
};

struct B {
  B(A *a) {
    a - > foo () ; // u n d e f i n e d b e h a v i o u r
  }

     v i r t u a l void bar () {}
};

struct C : public A , public B {
   C () : A () , B ( this ) {
      foo () ;
      bar () ;
   }
};
Listing 1: Virtual member call during construction, resulting in undefined
behaviour.


that was produced by the base constructor call. This disallows other base
objects that still have to be constructed in other branches of the inheritance
hierarchy from calling virtual methods in branches that would lead to
undefined behaviour. Verification of a constructor goes as follows:

     1. Verify a constructor call for each base class in order of derivation;

         (a) If the base class is polymorphic, consume a B vtype(field ptr(
             d addr D B offset), B vtype info) chunk, where d addr is the
             address of the derived object of class type D and B represents the
             class type of the base object;

     2. Produce a D vtype(d addr, D type info) chunk if the object under
        construction is polymorphic, where D is the class type of the object
        under construction;

     3. Produce a D bases constructed(d addr ) chunk if D derives from at
        least one class, where D is the class type of the object that is currently
        being constructed and d addr is the address of the object;


                                               10
  4. Initialize fields in order of declaration, where entries in the initializer
     list take precedence over default member initializers;
  5. Symbolically execute the constructor body.
    Verification of a destructor again changes in a similar fashion. After
destructing all member fields of class D, VeriFast consumes a vtype(d addr,
D type info) chunk if it is polymorphic, where d addr is the address of the
object under destruction. This disables polymorphic base objects from calling
virtual member functions of its derived object and calling member functions
of bases that are are part of another branch in the inheritance hierarchy.
Prior to verifying a polymorphic base destructor call, VeriFast produces a
B vtype(b addr, B type info) chunk, where B is the class type of the base
object at address b addr. This allows the polymorphic base object to call
virtual member functions in its inheritance sub hierarchy. Hence, verification
of a destructor can be performed through the following steps:
  1. Symbolically execute the destructor body;
  2. Destruct fields in reverse order of declaration;
  3. If the object of class type D at address d addr under destruction is
     polymorphic, consume a D vtype(d addr, D type info) chunk;
  4. Consume a D bases constructed(d addr ) chunk if D derives from at
     least one class, where D is the class type of the object that is currently
     being constructed and d addr is the address of the object;
  5. Verify a destructor call for each base class in reverse order of derivation;


      (a) Prior to verifying a base destructor call of a base object of class
          type B that is polymorphic, produce a vtype(field ptr(d addr,
          D B offset), B type info), where D is the class type of the de-
          rived object at address d addr.


5.3    Behavioural subtyping
When verifying a virtual member function call, VeriFast uses the same con-
tract that would be used during a statically bound call. However, the run-
time type of the target object might be a derived type of the statically known

                                      11
struct A {
   v i r t u a l int foo ()
   // @ r e q u i r e s true ;
   // @ e n s u r e s result >= 0;
   {
       return 0;
   }
};

struct B : public A {
  int m = 10;

     int foo () o v e r r i d e
     /* @ r e q u i r e s
          B _ b a s e s _ c o n s t r u c t e d ( this ) &*&
          this - >m | - > ? m_val &*&
          m_val >= 0;
     @ */
     /* @ e n s u r e s
          B _ b a s e s _ c o n s t r u c t e d ( this ) &*&
          this - >m | - > m_val &*&
          result == m_val ;
     @ */
     {
        return m ;
     }
};
Listing 2: Virtual member function override, violating behavioural subtyping.


target type. The static type acts as an upper bound for the objects’s dynamic
type [3]. Therefore, VeriFast performs a behavioural subtyping check for each
virtual member function that is overridden to make sure that the overriding
member function can statically call the member function that is overridden
[4]. First, the precondition of the overridden member function is produced.
Next, VeriFast consumes the precondition of the overriding member function
and produces the postcondition of the overriding member function. Lastly,
VeriFast consumes the postcondition of the overridden member function.
    This behavioural subtyping requirement makes verification of virtual
member functions harder and sometimes impossible. It often also requires
changes to the specification of the member function that is overridden and
reverification of the overridden member function.

                                                   12
    Take as an example the code snippet in Listing 2. Class B overrides
member function foo from its base class A. The specification in class B clearly
violates the behavioural subtyping check: the precondition of the overriden
member function does not imply the precondition of the overriding member
function. In order to be able to verify this program, the precondition of foo
in A has to be changed to require the chunks mentioned in the precondition
of foo in B. However, these chunks would only be available when the run
time class type of the target object would be B. Changing the specification
requires reverification of the overridden method, making modular verification
harder. In order to tackle this problem, VeriFast supports the use of instance
predicates.


6    Instance predicates
VeriFast already supports dynamically bound instance predicates for Java
programs [5]. An instance predicate can be defined in a class body and does
not have a single definition: each subclass defines its own definition of the
predicate. We also added this feature for classes in C++.
    An instance predicate has, similar to C++ member functions, an implicit
this parameter that is bound to the target object. Each derived class can
override an instance predicate that is declared in one of its base classes.
Hence, an instance predicate chunk contains an index argument to distinguish
between the different versions of the predicate. This index is a pointer to
an std::type info object in VeriFast when verifying C++ programs. For
example, an index with value S type info determines the instance predicate
defined in class S. Every type has a unique std::type info object, which
allows to differentiate overridden instance predicate chunks by their index.
    The example in Listing 3 defines an abstract Shape class that declares an
instance predicate valid. This class is inherited by the Square class, which
also overrides the definition of valid. An instance predicate chunk of valid
in Shape has signature Shape#valid(addr, Shape type info), where addr
is a pointer to the target object and Shape type info is the symbolic value
that represents a pointer to the std::type info object of class Shape. Re-
member that this value can be obtained by evaluating &typeid(Shape).
    Both the constructor of Shape and Square in Listing 3 mention a thisType
variable: a ghost variable that exists to make verification feasible. This
variable is implicitly available in each non-static member function of a class


                                      13
struct Shape {
  // @ p r e d i c a t e valid () = true ;

     Shape ()
     // @ r e q u i r e s true ;
     // @ e n s u r e s valid () &*& S h a p e _ v t y p e( this , t h i s T y p e) ;
     {
        // @ close valid () ;
     }

     v i r t u a l int c a l c A r e a () const = 0;
     // @ r e q u i r e s valid () ;
     // @ e n s u r e s valid () &*& result >= 0;
};

class Square : public Shape {
  int m _ w i d t h;

public :
  /* @ p r e d i c a t e valid () =
       this - > valid (& typeid ( Shape ) ) () &*&
       this - > m _ w i d t h | - > ? w &*&
       w >= 0 &*&
       S q u a r e _ b a s e s _ c o n s t r u c t e d ( this ) ;
  @ */

     Square ( int width ) : m _ w i d t h( width )
     // @ r e q u i r e s width >= 0;
     // @ e n s u r e s valid () &*& S q u a r e _ v t y p e( this , t h i s T y p e) ;
     {
        // @ close valid () ;
     }

     int c a l c A r e a () const o v e r r i d e
     // @ r e q u i r e s valid () ;
     // @ e n s u r e s valid () &*& result >= 0;
     {
        // @ open valid () ;
        return m _ w i d t h * m _ w i d t h;
        // @ m u l _ m o n o _ l (0 , this - > m_width , this - > m _ w i d t h) ;
        // @ close valid () ;
     }
};
         Listing 3: Shape and Square example with instance predicates.


                                                  14
and represents the value that would be obtained from evaluating &typeid(S),
where S is the class type of the target object that is bound the member
function call. The thisType ghost variable is implicitly used by VeriFast as
the index of an instance predicate where the target object is implicit this.
Hence, the chunk produced by valid() in the postcondition of constructor
Shape() is Shape#valid(addr, thisType ), where addr is the address of
the Shape object that would be constructed by the constructor.
    The value of thisType depends on whether a member function call is dy-
namically or statically bound. This allows to use a different interpretation
of the contract for statically bound member function calls and dynamically
bound member function calls, only requiring one specification from the pro-
grammer. I.e., the value of thisType depends on the binding of a member
function call.
    The value of thisType is assumed to be equal to S type info during
verification of a non-static member function, where S is the static type of
the target object. On the other hand, during verification of a dynamically
bound member function call, thisType is assumed to be a pointer to the
std::type info object for the most derived class type of the target. As
explained in Section 5.1, a check is performed for the existence of (some
fraction of) an S vtype(addr, ?info ) before verifying a virtual member
function call, where S is the static class type of the target expression and
addr its address. VeriFast now assumes that thisType has value info during
verification of the virtual member function call. The interpretation of a
specification must be the same during verification at the call site and during
verification of the callee. Therefore, VeriFast checks that a derived class
overrides all virtual member functions in all of its polymorphic direct bases
to meet this requirement [1].
    The target object of a predicate instance assertion can also be men-
tioned explicitly, as Listing 3 shows in the instance predicate definition of
valid in class Square. In this instance, this->valid(&typeid(Shape))()
refers to the instance predicate definition of Shape and is represented by a
Shape#valid(this, Shape type info) chunk.
    Evaluation of an instance predicate assertion with an explicit target
object that does not mention an explicit index depends on the nature
of its target. For a class S that is not polymorphic and defines an
instance predicate s pred(a0 ,. . .,an ), and an object of class type S at
address s addr, s addr->s pred(a0 ,. . .,an ) evaluates to S#s pred(s addr,
S type info, a0 ,. . .,an ). However, when S is polymorphic, VeriFast

                                     15
treats s addr->s pred(a0 ,. . .,an ) as syntactic sugar for S vtype(s addr,
?s type) &*& s addr->s pred(s type)(a0 ,. . .,an ).
    Using instance predicates, we can now annotate and verify the exam-
ple from Listing 2 while preserving behavioural subtyping as illustrated in
Listing 4.


7    Limitations
It is currently only possible to pass objects by reference or by pointers. No
support has been added yet to pass objects by value. Therefore, all function
parameters and function return types are either primitive types, reference to
objects or pointers to objects.
    Explicit destructor calls are currently not allowed by VeriFast. This
avoids explicitly destroying a stack-allocated object, when it might later
be destroyed automatically when the object goes out of scope, potentially
leading to undefined behaviour. However, explicit constructor calls are re-
quired once placement new is supported in order to construct an object in
preallcoated memory.
    Verification for virtual destructors is infeasible when a polymorphic class
inherits from multiple polymorphic base classes that have a virtual destruc-
tor. The overriding virtual destructor in the derived class can only meet the
requirement of behavioural subtyping for one of its base classes, because it
is currently not supported to declare an instance predicate in a derived class
that overrides multiple instance predicates defined in its base classes.
    Furthermore, heap-allocated objects that inherit from at least one base
object cannot be destroyed with the new operator through a pointer to one
of its base objects, even if it has a virtual destructor. Verification of the
delete operator on a pointer to a base object of a derived object requires a
new block chunk that was allocated for the base object.


8    Future work
Support for verification of C++ programs with VeriFast is still in develop-
ment. We are first planning to address the limitations discussed in Section 7.
In addition, we plan to add support for virtual inheritance and rvalue refer-
ences. Next, our goal is support for verification of programs with C++ tem-


                                      16
struct A {
  // @ p r e d i c a t e valid () = true ;

     v i r t u a l int foo ()
     // @ r e q u i r e s valid () ;
     // @ e n s u r e s valid () &*& result >= 0;
     {
         return 0;
     }
};

struct B : public A {
  int m = 10;

     /* @ p r e d i c a t e valid () =
          this - >m | - > ? m_val &*&
          m_val >= 0 &*&
          B _ b a s e s _ c o n s t r u c t e d ( this ) ;
     @ */

     int foo () o v e r r i d e
     // @ r e q u i r e s valid () ;
     // @ e n s u r e s valid () &*& result >= 0;
     {
        // @ open valid () ;
        return m ;
        // @ close valid () ;
     }
};
Listing 4: Verifiable version of Listing 2 with instance predicates, while
preserving behavioural subtyping.




                                                      17
plates, which is one of the main missing features in VeriFast. Constraints and
concepts, language features added in C++20, are interesting aspects when
looking into verification of programs with templates. Once these features
have been added to VeriFast, we plan to verify some critical industrial C++
programs. This would give insight in C++ features that are commonly used
and might involve interesting and new verification challenges.




                                     18
References
[1] Michael Barnett, Robert DeLine, Manuel Fähndrich, K Rustan M Leino,
    and Wolfram Schulte. Verification of object-oriented programs with in-
    variants. J. Object Technol., 3(6):27–56, 2004.

[2] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem
    Penninckx, and Frank Piessens. VeriFast: A powerful, sound, predictable,
    fast verifier for C and Java. In NASA formal methods symposium, pages
    41–55. Springer, 2011.

[3] Gary T Leavens, Krishna Kishore Dhara, and Krishna Kishore Dhara.
    Concepts of behavioral subtyping and a sketch of their extension to
    component-based systems. 2000.

[4] Matthew J Parkinson. Local reasoning for Java. Technical report, Uni-
    versity of Cambridge, Computer Laboratory, 2005.

[5] Jan Smans, Bart Jacobs, and Frank Piessens. VeriFast for Java: A tu-
    torial. Aliasing in Object-Oriented Programming. Types, Analysis and
    Verification, pages 407–442, 2013.




                                    19
