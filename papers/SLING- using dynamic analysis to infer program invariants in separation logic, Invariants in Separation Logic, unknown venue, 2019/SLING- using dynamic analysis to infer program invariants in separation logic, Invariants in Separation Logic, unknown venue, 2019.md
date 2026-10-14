                                               SLING: Using Dynamic Analysis to Infer Program
                                                        Invariants in Separation Logic
                                                         Ton Chanh Le                               Guolong Zheng                          ThanhVu Nguyen
                                                Stevens Institute of Technology               University of Nebraska-Lincoln          University of Nebraska-Lincoln
                                                  Hoboken, New Jersey, USA                       Lincoln, Nebraska, USA                  Lincoln, Nebraska, USA
                                                    letonchanh@gmail.com                           gzheng@cse.unl.edu                     tnguyen@cse.unl.edu

                                         Abstract                                                              bug can be avoided by preserving an invariant capturing the
arXiv:1903.09713v2 [cs.PL] 29 Jun 2019




                                         We introduce a new dynamic analysis technique to discover             proper size of the received payload message [16]. Invariants
                                         invariants in separation logic for heap-manipulating pro-             also help developers understand programs, e.g., showing in-
                                         grams. First, we use a debugger to obtain rich program exe-           teresting or unexpected behaviors, and even discover non-
                                         cution traces at locations of interest on sample inputs. These        functional bugs, e.g., revealing that the program has an un-
                                         traces consist of heap and stack information of variables             usual high runtime complexity [37]. Invariants are also use-
                                         that point to dynamically allocated data structures. Next, we         ful in other programming tasks, including documentation,
                                         iteratively analyze separate memory regions related to each           maintenance, code optimization, fault localization, program
                                         pointer variable and search for a formula over predeﬁned              repair, and security analysis [1, 2, 15, 18, 30, 37, 45].
                                         heap predicates in separation logic to model these regions.              Unfortunately, software developers appear to perceive a
                                         Finally, we combine the computed formulae into an invari-             “speciﬁcation burden” [2] which leads them to eschew the
                                         ant that describes the shape of explored memory regions.              writing of invariants in favor of executable code. For the
                                            We present SLING, a tool that implements these ideas to            past decade, researchers have been chipping away at this
                                         automatically generate invariants in separation logic at ar-          challenge of automatic invariant generation using static or
                                         bitrary locations in C programs, e.g., program pre and post-          dynamic analyses. A static analysis can reason about all
                                         conditions and loop invariants. Preliminary results on exist-         program paths soundly, but doing so is expensive and is
                                         ing benchmarks show that SLING can eﬃciently generate                 only possible to relatively small programs or simple forms
                                         correct and useful invariants for programs that manipulate            of invariants, e.g., simple list structures [3, 11, 35]. In con-
                                         a wide variety of complex data structures.                            trast, dynamic analysis focuses on program traces observed
                                                                                                               from running the program on small sample inputs, and thus
                                         CCS Concepts • Theory of computation → Separation                     provides no correctness guarantee on generated invariants.
                                         logic; Invariants; Pre- and post-conditions; Program                  However, dynamic analysis is generally eﬃcient and can
                                         analysis; • Software and its engineering → Dynamic                    infer expressive invariants because it only analyzes a ﬁnite,
                                         analysis; Software veriﬁcation.                                       typically small, set of traces.
                                         Keywords dynamic invariant analysis, separation logic                    Existing invariant techniques often focus on invariants
                                                                                                               over scalar variables, e.g., relations among numerical val-
                                         ACM Reference Format:
                                                                                                               ues [19, 37, 42]. However, modern programs construct and
                                         Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen. 2019. SLING:
                                         Using Dynamic Analysis to Infer Program Invariants in Separation
                                                                                                               manipulate data structures, i.e., highly-structured sets of
                                         Logic. In Proceedings of the 40th ACM SIGPLAN Conference on Pro-      memory locations within which these scalar values are
                                         gramming Language Design and Implementation (PLDI ’19), June          stored. Examples of such data structures are dynamically-
                                         22–26, 2019, Phoenix, AZ, USA. ACM, New York, NY, USA, 14 pages.      allocated objects, e.g., heap-based objects created via the
                                         https://doi.org/10.1145/3314221.3314634                               new keyword, standard data structures, e.g., lists and trees,
                                                                                                               or customized and user-deﬁned structures that extend the
                                         1    Introduction                                                     standard ones and contain other structures internally. Un-
                                         A program invariant is a property that holds whenever pro-            derstanding and reasoning about these heap-based pro-
                                         gram execution reaches a speciﬁc location. For example, a             grams are more challenging, e.g., even the task of accessing
                                         loop invariant can indicate a relation among the program              a variable requires checking if it points to a valid memory
                                         variables at the loop entrance. Invariants help prove pro-            region (to avoid null pointer dereferencing).
                                         gram correctness, e.g., classical veriﬁcation approaches by              An emerging approach to analyzing heap programs is to
                                         Floyd-Hoare and Dijkstra [13, 21] can be automated when               use invariants written in separation logic (SL) to represent
                                         given needed loop invariants and the infamous Heartbleed              memory structures [41, 47]. SL extends classical logic and
                                                                                                               allows for compact and precise representations of program
                                         PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA
                                                                                                               semantics and reasoning to be localized to small portions of
                                         2019. ACM ISBN 978-1-4503-6712-7/19/06. . . $15.00
                                         https://doi.org/10.1145/3314221.3314634
                                                                                                               memory. In the last decade, research in SL has grown rapidly
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                           Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

and led to practical techniques used in tools such as the Face-       1    typedef struct Node {
book Infer (FBInfer) analyzer [17].                                   2      struct node * next , * prev ;
   Most existing SL works focus on static analyses to ob-             3    } Node ;
tain sound results, and therefore can only consider simple            4
classes of invariants or programs, e.g., to support the goal of       5    Node * concat ( Node *x , Node * y ) {
“move fast to ﬁx more things” [8, 40], FBInfer only consid-           6      [ L1 ]
                                                                      7      if ( x == NULL ) {
ers simple data structures and restricts supported language
                                                                      8         [ L2 ]
features. Moreover, while many static analyzers, including
                                                                      9         return y;
FBInfer, compute SL invariants internally to verify pro-             10      } else {
grams, we are aware of only a few researchers who have               11         Node * tmp = concat (x - > next , y ) ;
investigated reifying those invariants for consumption by            12         x - > next = tmp ;
developers, and even then only for a restricted language             13         if ( tmp ) tmp - > prev = x ;
of list manipulating [32] or tree traversing programs [5].           14         [ L3 ]
Also, most static SL tools aim to infer suﬃciently strong            15         return x;
invariants to achieve a speciﬁc goal, e.g., to prove memory          16      }
safety or (programmer-provided) postconditions, and thus             17    }
are not well suited for discovering useful invariants to help
understand code that lacks such formal speciﬁcations.                     Figure 1. Concatenating two doubly linked lists
   In this work, we introduce SLING (Separation Logic
Invariant Generation), a tool that dynamically discovers SL
invariants for heap programs. SLING takes as inputs a pro-        2 Illustration
gram, a location of interest, a set of predeﬁned predicates
deﬁning data structures, and a set of sample inputs. SLING        We describe SLING using the function concat shown in Fig-
next runs the program on the inputs and uses a debugger           ure 1. This function recursively concatenates two doubly
to obtain traces capturing memory information of the vari-        linked lists x and y and returns (i) y when x is empty or
ables at the considered location. These traces consist of the     (ii) a new doubly linked list by appending y to the tail of x.
contents of the stack and heap of the program. SLING then             Although simple, concat requires several subtle precon-
iteratively analyzes variables using these traces to compute      ditions over its inputs to work properly. First, x must be a nil-
invariants. For each pointer variable, SLING generates SL         terminated list, i.e., the next ﬁeld of its tail node is NULL, oth-
formulae using predeﬁned predicates to model the traces de-       erwise concat may not terminate when x contains a cycle or
scribing memory regions related to the variable. SLING also       may refer to an unallocated memory region when the next
propagates computed information to improve the analysis           ﬁeld of x’s tail node is a dangling pointer. Second, x and y
of other variables in subsequent iterations. Finally, SLING       must be non-overlapping, i.e., point to lists in separate mem-
combines the obtained formulae into a ﬁnal invariant that         ory regions, otherwise the resulting list contains a cycle.
represents the explored memory regions.                           These conditions can be diﬃcult to analyze or even to spec-
   We use SLING to infer invariants for 157 C programs            ify because they involve dynamically-allocated data struc-
taken from two existing benchmarks [51] and [6]. These            tures and their separations in memory. SLING aims to auto-
programs implement basic algorithms over standard data            matically discover such preconditions at program entrances
structures (e.g., singly-linked, doubly-linked, circular lists,   and, more generally, invariant properties at arbitrary pro-
binary trees, AVL, red-black trees, heaps, queues, stacks, it-    gram locations, including postconditions and loop invari-
erators) and complex functions from open source libraries         ants.
and the Linux kernel that manipulate customized data struc-
tures. Preliminary results show that SLING can eﬃciently          2.1 Heap Predicates
generate invariants that are correct and more precise than        SLING infers invariants expressed as formulae in separation
the documented invariants and speciﬁcations in these pro-         logic (SL) to describe properties of heap-manipulating pro-
grams. Even when given incomplete traces, the tool can still      grams. Comparing to existing works for heap programs [26,
discover partial invariants that are useful for users. We also    48], SL provides concise and expressive syntax and seman-
show that SLING’s invariants can help reason about non-           tics to describe memory (shape) information [41, 47].
trivial bugs and reveal false positives in modern SL static          To analyze heap programs, SL works often use inductive
analyzers. We believe that SLING strikes a practical balance      heap predicates to compactly represent recursively-deﬁned
between correctness and expressive power, allowing it to          data structures. For concat, we use the predicate dll to de-
discover complex, yet interesting and useful invariants out       ﬁne doubly linked lists:
                                                                                           def
of the reach of the current state of the art.                         dll(hd, pr , tl, nx) = (emp ∧ hd=nx ∧ pr =tl)
                                                                                           ∨ (∃u. hd7→u, pr ∗ dll(u, hd, tl, nx))
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                       PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

The parameters hd, tl, pr , and nx point to the list’s head, tail,                             heap                   s1
                                                                                                                                   h 1 , h 2, h 3
                                                                           stack
previous, and next element, respectively. The deﬁnition of                                                           x = 0x01                  0x01
dll uses the built-in predicate emp to represent an empty                 x = 0x01                     0x01
                                                                                                              t1   tmp = 0x02




                                                                                                                                next

                                                                                                                                        prev
                                                          Node                                                       y = 0x04




                                                                                        next

                                                                                                prev
heap, e.g., a NULL list, and the singleton predicate x 7→ nx, pr                                                   res = 0x01
                                                                                                                                               0x02
to denote a memory cell that a variable x of type Node shown                                           0x02           s2




                                                                                                                                next

                                                                                                                                        prev
in Figure 1 points to (nx and pr correspond to the next and                                                          x = 0x02




                                                                                        next

                                                                                                prev
prev ﬁelds of x, respectively1 ).                                                                             t2   tmp = 0x03
                                                                                                                     y = 0x04                  0x03
   Conceptually, dll states that a doubly linked list is either                                        0x03        res = 0x02




                                                                                                                                next

                                                                                                                                        prev
an empty or a non-empty list, which is recursively deﬁned
                                                                                                                      s3
by having the head hd point to a doubly linked list whose                                                                                      0x04
                                                                                                                     x = 0x03
head node is u. In the latter case, the separating conjunction            y = 0x04                     0x04
                                                                                                                   tmp = 0x04




                                                                                                                                next

                                                                                                                                        prev
                                                                                                              t3
connector ∗ speciﬁes the separation of memory regions mod-                                                           y = 0x04




                                                                                        next

                                                                                                prev
                                                                                                                   res = 0x03
eled by hd’s singleton predicate and u’s dll predicate, i.e., the                                                                              0x05
                                                                                                       0x05
heaplets of hd and u are disjoint.
   SLING uses such heap predicates to discover invariants
                                                                        (a) a trace at L1                     (b) sequence of traces at L3
and speciﬁcations of heap programs. For concat, SLING
uses dll to generate the precondition on line 6 and the post-
                                                                          Figure 2. Traces collected at L1 and L3 in concat.
condition on line 8 and 14 in Figure 1 as

                                                                     2.2 Traces
    pre = ∃p, u, v. dll(x, p, u, nil) ∗ dll(y, nil, v, nil)          Given a program annotated with locations of interest,
                                                                     SLING runs the program on sample inputs to collect ex-
   post = ∃v. dll(y, nil, v, nil) ∧ x=nil ∧ res=y ∨
                                                                     ecution traces. Currently, we use the LLDB debugger [31]
            ∃p, u, v. dll(x, p, u, y) ∗ dll(y, u, v, nil) ∧ res=x    to observe execution traces containing memory addresses
                                                                     and values of the variables in scope at considered locations2 .
                                                                        Figure 2a shows two doubly linked lists x and y of size 3
                                                                     and 2, respectively. When running on these inputs, SLING
   These pre and postconditions form a valid speciﬁcation            records traces such as those given in Figures 2. Figure 2a
for concat. The precondition requires that inputs x and              shows the trace obtained in the ﬁrst iteration of concat
y point to two disjoint, nil-terminated doubly linked lists.         at L1. The trace contains information about both the stack,
Note that unlike y, the dll of x shows that it can take any          containing values of variables accessible at this location,
arbitrary previous pointer, i.e., the existential argument p,        e.g., x=0x01, y=0x04, and the heap, containing allocated
because this pointer changes across the recursive call on            memory cells reachable from the stack’s variables, e.g.,
line 11.                                                             0x017→Node{next:0x02;prev:nil}.
   The postcondition ensures two exit conditions: (i) when              Figure 2b shows three set of traces collected at L3 for
x is empty, the return value res is y, and (ii) otherwise,           the ﬁrst three iterations of concat. Note that the values
res = x is the result of appending y to x by changing the            of x and tmp are diﬀerent in the stacks because x and tmp
next element of x’s predicate from nil to y. Also, note that         change across the recursive calls in concat. However, the
the previous ﬁeld of y now points to the tail element of x.          heap is similar because concat does not change the heap,
Lastly, the postcondition states that the separation of the          e.g., delete or create cells, and all memory cells are still
heaps of x and y is preserved, i.e., concat only changes the         reachable from the stack variables. Moreover, the stack at
ﬁeld values of the lists and does not alter the allocated mem-       L3 contains a ghost variable res, which stores the return
ory.                                                                 value of the function3 .
   Inductive heap predicates such as dll are standard in SL
(e.g., provided by the users or predeﬁned in an analyzer [7,         2.3 Inference
24, 29, 33]) and compactly capture crucial shape properties          SLING infers invariants consisting of SL predicates such as
(e.g., doubly linked lists are acyclic). In addition, compared       dll over variables at a location of interest. For each (pointer)
to normal, non-SL predicates such as isOdd or x ≥ y, check-
ing SL heap predicates is nontrivial because we have to “un-
                                                                     1 When the context is clear, we simply use x 7→nx, pr for xNode
                                                                                                                                 7→ nx, pr .
fold” data structures recursively and ﬁnd concrete values to         2 These "traces", which are snapshots of program states, are often referred
instantiate the existential quantiﬁers, e.g., the pre and post-      to as the stack-heap models in SL literature, which we review in Section 3.
conditions above require ﬁnding the correct quantiﬁed vari-          3 This value is captured when the LLDB debugger steps out of the function

ables and parameters in dll.                                         and jumps back to its call site.
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                                                              Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

  x,                                                                                                 The checker either refutes the formula, which is then dis-
                      0x01   h 1′                       0x01                           0x01
  res
                                                                                                     carded, or accepts it, which SLING then considers as a




                                          next




                                                                         next
                                                 prev




                                                                                prev
        next

               prev                                            h 2′
                                                                                                     valid formula over the sub-heaps. Intuitively, accepted for-
                                    x,
 tmp                  0x02          res                 0x02                           0x02   h 3′   mulae represent partial invariants computed from memory
                                                                                                     regions, e.g., the sub-heaps, related to the analyzed variable.


                                          next




                                                                         next
                                                 prev




                                                                                prev
        next

               prev




                                                                                                        In our example, among the generated candidates, the
                                                                  x,
                      0x03          tmp                 0x03      res                  0x03          checker accepts the formula F x = ∃u 1 , u 2 . dll(x, u 1 , u 2 , tmp).
                                          next                                                       This formula shows that x is a doubly linked list to the next




                                                                         next
                                                 prev




                                                                                prev
        next

               prev




                                                                                                     pointer tmp. The existential variables u 1 , u 2 indicate that
                                      y                           tmp,
   y                  0x04                              0x04      y                    0x04          SLING cannot ﬁnd concrete stack or nil variables for the
                                                                                                     second and third parameters of dll from the traces.
                                          next




                                                                         next
                                                 prev




                                                                                prev
        next

               prev




                                                                                                        Although F x holds over the given sub-heaps, it might not
                      0x05                              0x05                           0x05          generalize to the entire heap in the observed traces. Thus,
                                                                                                     when analyzing F x , the checker also computes a residual
                                                                                                     heap, which represents the part of the heap that is not mod-
Figure 3. Sub-heaps of x (in blue dashed boxes) and their                                            eled by F x . The checker also computes a mapping from exis-
boundaries (nil and the variables in red). The common                                                tential variables to concrete memory addresses from given
boundary of these sub-heaps is {x, tmp, res, nil}.                                                   traces. SLING propagates these details to improve the anal-
                                                                                                     yses of other variables in subsequent iterations.
                                                                                                        SLING now continues with the other variables tmp, y, res
variable, SLING explores relevant memory regions in ob-                                              using the described steps and computed information (resid-
served traces to compute invariants for that variable. Fi-                                           ual heaps and address mappings). For tmp, SLING computes
nally, SLING combines the computed invariants to model                                               the sub-heaps and boundary {tmp, x, res, y}, and obtains
the whole explored memory regions.                                                                   then the formula F tmp = ∃u 3 . dll(tmp, x, u 3 , y), which indi-
                                                                                                     cates a doubly linked list from tmp to the next pointer y.
Postcondition We now show how SLING computes the                                                     Also, observe that the previous pointer points to x, showing
postcondition at L3 using the predicate dll and the traces                                           the connection between this list and the one modeled by F x .
shown in Figure 2b. For demonstration we assume that                                                    Similarly, for the last two variables y and res, SLING ob-
SLING analyzes the variables at L3 in the order x, tmp, y, res.                                      tains the formulae Fy = ∃u 4 , u 5 . dll(y, u 4 , u 5 , nil) and F res =
    From given traces, SLING ﬁrst computes the sub-heaps                                             emp. F res is emp because every sub-heap reachable from
of x and their boundaries. The sub-heaps contain memory                                              res is empty in the traces observed in the last iteration.
cells reachable from x but not pointed to by other stack vari-                                          The obtained formulae F x , F y , F tmp , and F res model sepa-
ables. The boundaries of x’s sub-heaps contain x itself, the                                         rate sub-heaps, thus SLING combines them using the ∗ op-
nil pointer if it is reachable from x, and all variables reach-                                      erator to form a shape invariant capturing the shape of the
able from x or its aliasing pointers. Next, SLING takes the                                          memory at L3, e.g., connections among separate heaplets:
intersection of the boundaries to obtain the common bound-                                         F L3 = ∃u 1 , u 2 , u 3 , u 4 , u 5 , tmp.
ary, which consists of variables used to compute invariants
in the next step. Figure 3 shows the computed sub-heaps                       dll(x, u 1 , u 2 , tmp) ∗ dll(tmp, x, u 3 , y) ∗ dll(y, u 4 , u 5 , nil).
  ′             ′                        ′
h 1 = {0x01}, h 2 = {0x01, 0x02}, and h 3 = {0x01, 0x02, 0x03}          Note that the constraint F res = emp is discarded from the
over the three traces of x and their respective boundaries              conjunction. Also note that the local variable tmp is not in
{x, res, nil, tmp}, {x, res, nil, tmp}, and {x, res, nil, tmp, y}.      the scope of the function’s exit, thus SLING considers it as
Their common boundary is {x, res, nil, tmp}.                            an existential variable in F L3 . In general, SLING only uses
    From computed sub-heaps and boundary variables, SLING               the function’s parameters and the ghost variable res as free
searches the predeﬁned predicates for formulae that are                 variables in the function’s pre and postconditions.
consistent with sub-heap traces using boundary variables.                    SLING also examines analyzed information to ﬁnd ad-
For each predicate, SLING creates candidate formulae by in-             ditional pure (not related to memory) relations among the
stantiating predicate parameters with boundary variables. It            stack and existential variables in the inferred formula. In
does so by enumerating diﬀerent subsets of boundary vari-               this example, SLING determines that res = x, indicating
ables as predicate parameters. For subsets of size smaller              that the return value at L3 is x. It also infers aliasing informa-
than the number of parameters, SLING introduces fresh ex-               tion such as x = u 2 , u 3 =u 4 from the address mapping. From
istential variables to instantiate the predicate. In our exam-          these additional equalities, SLING derives the ﬁnal result:
ple, SLING enumerates formulae such as ∃u 1 . dll(x, nil, tmp, u 1 ), ∃u 1 . dll(x, nil, u 1 ,′ tmp), . . . .
    Next, SLING then uses an SMT-based model checker to                                    F L3 = ∃u 1 , u 3 , u 5 , tmp. dll(x, u 1 , x, tmp) ∗
check each candidate formula against the given sub-heaps.                                                    dll(tmp, x, u 3 , y) ∗ dll(y, u 3 , u 5 , nil) ∧ res = x.
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                                    PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

This result F L3′ is correct at L3 and even more precise than                   predicate emp models an empty heap, the singleton heap
                                                                                                  τ
(stronger) the postcondition shown in Section 2.1 when x ,                      predicate x 7→t 1 , ..., tn models an n-ﬁeld data structure type
nil: ∃p, u, v. dll(x, p, u, y) ∗ dll(y, u, v, nil) ∧ res = x. The rea-          τ where x points to, and the inductive heap predicate
                                                                ′ en-
son is because dll(x, u 1 , x, tmp) ∗ dll(tmp, x, u 3 , y) in F L3              p(t 1 , ..., tn ) models a recursively deﬁned data structure. The
tails ∃p, u. dll(x, p, u, y) in the given postcondition. The re-                spatial formulae Σ consist of these predicates and their
versed direction of this entailment does not hold as it re-                     compositions using the ∗ separating conjunction operator.
quires a non-trivial condition x , y.                                           Π denotes pure formulae in linear arithmetic, which do not
Precondition and Other Invariants Using the same in-                            contain any predicates. Note that we can negate the pre-
ference process over the traces obtained from the input x, y                    sented formulae to obtain formulae involving disjunctions,
given in Figure 2, SLING infers the precondition at location                    universal quantiﬁers, and other comparison relations.
L1 and the invariant at location L2 of concat as
     ′
                                                                                Semantics Given a set Var of variables, Type of types, Val
   F L1 = ∃u 1 , u 2 , u 3 , u 4 .                                              of values, and Loc ⊂ Val of memory addresses, an SL stack-
           dll(x, u 1 , u 2 , nil) ∗ dll(y, u 3 , u 4 , nil) ∧ u 3 = nil, and   heap model, i.e., concrete trace, is a pair of a stack model s,
      ′
    F L2 = ∃u 1 , u 2 .                                                         which is a function s: Var → Val, and a heap model h, which
                                                                                is a partial function h: Loc ⇀ (Type × Val∗ ). We write nΠos
            dll(y, u 1 , u 2 , nil) ∧ u 1 = nil ∧ x = nil ∧ res = y.
                                                                                to denote the valuation of a formula Π under the stack model
These are the pre and postconditions shown in Section 2.1.                      s and s, h |= F to denote a model s, h satisﬁes a formula F .
From these results, we obtain the speciﬁcation of concat be-                    Moreover, dom(h) denotes the domain of h, h 1 # h 2 denotes
                                                        ′                       h 1 and h 2 have diﬀerent domains, and h 1 ◦ h 2 denotes the
cause the complete post condition is the disjunction F L2  ∨
  ′
F L3 . In general, SLING can compute invariants at arbitrary                    union of two disjoint heaps h 1 and h 2 , and [f | x : y] indi-
program locations by applying the described inference pro-                      cates a function like f but returns y for input x. We also
cess to traces obtained at those locations.                                     deﬁne the heap union and diﬀerence operators over two se-
                                                                                                                                                 def
    Depending on the program, we could create scenarios                         quences of stack-heap models as (si , hi )ni=1 ⊕ (si , hi′ )ni=1 =
where diﬀerent orders of analyzed variables produce weaker                                                                               def
                                                                                (si , hi ◦ hi′ )ni=1 and (si , hi )ni=1 \ (si , hi′ )ni=1 = (si , hi \ hi′ )ni=1 , re-
results. This is because the propagated residue information
                                                                                spectively.
aﬀects the computation of boundary variables and thus
the instantiations of parameters in the predicates. SLING                       Model Checking We follow the technique given in [7] to
prevents these scenarios by using a simple heuristic that
                                                                                implement a model checker, which checks if a formula F is
only selects the next variables to analyze from those di-
                                                                                satisﬁed by a stack-heap model s, h and returns a residual
rectly reachable from previously considered variables. This
                                                                                heap h ′ , i.e., memory regions in h not modeled by F , and
gives a ﬁxed order that works well in our experiments (Sec-
                                                                                an instantiation ι that maps existential variables in F to con-
tion 5.3).
                                                                                crete addresses in the model. These checking and instanti-
                                                                                ation tasks are encoded as logical formulae solvable using
3     Separation Logic                                                          the Z3 SMT solver [12].
SL [26, 48] has been actively used to reason about imper-                          Note that the model checking technique proposed in [7]
ative programs that manipulate data structures. Crucially,                      does not return the instantiation ι, which is needed by
SL uses the separating conjunction operation ∗ to describe                      SLING to compute equalities among variables in F . To
the separation of computer memory, i.e., the assertion p ∗ q                    obtain ι, we slightly redeﬁne the problem with a new satis-
states that p and q hold for disjoint memory regions. More-                     faction relation:
over, SL is often equipped with the ability for users to deﬁne
inductive heap predicates (such as the predicate dll used in                    Deﬁnition 1 (Satisfaction Relation with Existential Instan-
Section 2 for doubly linked list). The combination of the ∗                     tiation). The relation s, h |=ι F is the satisfaction relation
operator and heap predicates make SL expressive enough to                       s, h |= F except that the value of an existential variable in F
model various types of data structures.                                         is obtained from the instantiation ι, which is a function from
   Figure 4 shows the syntax and semantics of the SL formu-                     Var to Val similar to the stack model.
lae we consider in this work. These represent the standard
symbolic-heap fragment of SL [7, 49, 50] with user-deﬁned                          We also lift this relation to sequences of stack-heap mod-
inductive heap predicates.                                                                                                              def
                                                                                els and instantiations as (si , hi )ni=1 |=(ι i )ni=1 F = ∀i. si , hi |=ι i
Syntax We denote x as a variable, k, e as an integer con-                       F.
stant and an integer expression, respectively, nil as a con-
stant denoting a dangling memory address (null), and a                          Deﬁnition 2 (Symbolic-heap Model Checking). A reduc-
as a spatial expression modeling a memory address. The                          tion s, h k− F h ′, ι is valid if h ′ ⊆ h and s, h \ h ′ |=ι F .
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                                                   Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

 Syntax                                                            Semantics
 eF          k | x | − e | e1 + e2 | k · e   Integer exps          s, h |= emp                   iﬀ   dom(h) = ∅
                                                                              τ
 aF          nil | x                         Spatial exps          s, h |= x 7→t 1 , ..., tn     iﬀ   dom(h) = {s(x)} and h(s(x)) = (τ , {s(t 1 ), ..., s(tn )})
                                                                                                                             def
 ΠF          a1 = a2 | e1 = e2 | e1 < e2 |   Pure formulae         s, h |= p(t 1 , ..., tn )     iﬀ   s, h |= F , where F ⇒ p(t 1 , ..., tn )
             ¬Π | Π1 ∧ Π2 | ∃x. Π                                  s, h |= Σ1 ∗ Σ2               iﬀ   ∃h 1 , h 2 . h 1 # h 2 ∧ h 1 ◦ h 2 = h ∧ s, h 1 |= Σ1 ∧ s, h 2 |= Σ2
                          τ
 ΣF          emp | x 7→t 1 , ..., tn |       Spatial formulae      s, h |= Σ ∧ Π                 iﬀ   nΠos = true and s, h |= Σ
             p(t 1 , ..., tn ) | Σ1 ∗ Σ2                           s, h |= ∃x. F                 iﬀ   ∃v ∈ Val. [s | x : v], h |= F
 F F         Σ | Π | Σ ∧ Π | ∃x. F           SL formulae

                                       Figure 4. Syntax and semantics of symbolic-heap SL formulae.

Algorithm 1 The main algorithm of SLING                                              stack variables to infer invariants. At each iteration, SLING
Input: A program C, a set of predeﬁned predicates P, a test suite                    updates the result set R with a tuple (F , SH, I), where the
T, and a program location l                                                          formula F holds for the models analyzed in the previous iter-
Output: A set of invariants at l                                                     ation, the set of stack-heap models SH captures the residue
 1: SH ← CollectModels(C, l, T)                                                      of the initial heaps that are not modeled by F , and the se-
 2: V ← GetVars(l)                                     ⊲ stack variables             quence I contains existential instantiations which map the
 3: R ← {(emp, SH, (ιi = {})i ∈T )}                       ⊲ initial result           existential variables in F to concrete memory addresses.
 4: for each pointer v in V do                                                          In each iteration, given a stack variable v ∈ V and a tuple
 5:     R′ ← {}                                                                      (F , SH, I) ∈ R, SLING derives a set of atomic heap predi-
 6:     for each (F , SH, I) in R do                                                 cates (i.e., inductive heap predicates, singleton heap predi-
 7:         SHv , SHr , B ← SplitHeap(SH, v) ⊲ SHv ⊕ SHr ≡ SH                        cates, or emp), which models the sub-heaps in SH that con-
 8:         Rv ← InferAtom(v, SHv , B, P)
                                                                                     tain memory cells reachable from v. The heaps modeled by
 9:         for each (Fv , SH′, I′ ) in Rv do        ⊲ SHv \ SH′ |=I′ Fv
                                                                                     these predicates and F are disjoint, thus we can strengthen
10:             R ← R ∪ {(F ∗ Fv , SHr ⊕ SH , I ⊕ I′ )}
                 ′      ′                          ′
                                                                                     F with each predicate using the ∗ operator of SL. Intuitively,
11:     R ← {(InferPure(F , SH, I), SH, I) | (F , SH, I) ∈ R′ }
                                                                                     SLING splits the original stack-heap models into multiple
12: return R
                                                                                     sub-heaps, which are pointed-to by distinct (non-aliasing)
                                                                                     stack variables. To model a sub-heap, SLING derives atomic
Deﬁnition 2 redeﬁnes the model checking reduction relation                           formulae from the given predicates and the stack variables
to return, in addition to the residual heap model h ′ , an in-                       related to the sub-heap. Sections 4.1 and 4.2 describes the
stantiation ι of existential variables in F that satisﬁes the                        two sub-procedures SplitHeap and InferAtom, respectively.
relation s, h \ h ′ |=ι F in Deﬁnition 1.                                               In addition to ﬁnding invariants describing shape proper-
                                                                                     ties, SLING infers equality constraints over stack variables
4    The SLING Algorithm                                                             in V to represent pure properties. Section 4.3 describes the
Algorithm 1 shows the implementation of SLING. Given a                               InferPure procedure that performs this step.
program C, a set P of predeﬁned inductive heap predicates,
a target location l in C, and a test suite T, SLING returns a                       Validation When we discover both pre and postcondi-
set R of SL formulae satisﬁed by observed traces at l.                              tions, we combine them to obtain program speciﬁcations.
   SLING infers invariants using the three main phases de-                          We also leverage the frame rule of SL to check if this com-
scribed below. In the following we use the term stack-heap                          bination is consistent with respect to the corresponding
models to refer to concrete traces.                                                 residual models. Thus, when inferring invariants at multi-
                                                                                    ple return statements, SLING has an additional step that
Model Collection (line 1) SLING ﬁrst calls CollectModels                            combines and validates formulae inferred at these locations.
to collect all stack-heap models observed at location l when                        We describe this step in Section 4.4.
running the program over the tests in T. CollectModels uses
a software debugger such as LLDB to set a breakpoint at                              4.1 Heap Partitioning
l and inspect the memory layout when executing the pro-
                                                                                     Given a sequence SH of collected stack-heap models, SLING
gram. It then collects the set of stack-heap models SH from
                                                                                     calls SplitHeap to splits the heap in each model si , hi ∈ SH
the memory whenever hitting the breakpoint at l.
                                                                                     into smaller sub-heaps so that each of them can be modeled
Inference (lines 2–11) After obtaining the stack-heap                                by atomic heap predicates. Moreover, SplitHeap returns the
models at l, SLING performs a heap inference and then a                              common boundary of these sub-heaps, which consist of the
pure inference to derive a set of results satisﬁed by the mod-                       nil and stack variables that are subsequently used to deter-
els. SLING uses an iterative reﬁnement process over the                              mine the arguments for these atomic heap predicates.
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                                    PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

Algorithm 2 InferAtom: Inferring Atomic Predicates                                 as the root pointer. Also, for simplicity of presentation, we
Input: A stack pointer root, its sub-models SHr oot and their                      assume that the parameters t 1 , ..., tn of p are pointer types.
common boundary B, and a set of predeﬁned predicates P                                  SLING chooses potential arguments of predicate p from
Output: A set of atomic formulae modeling the sub-models and                       the common boundary B of all sub-heaps in the sub-models
their residue information                                                          SHr oot . It searches for these arguments from all permuta-
 1: R ← {}                                                                         tion of B’s subsets whose size is less than or equal to n and
 2: for each p(t 1 , ..., t n ) in P do             ⊲ Consider a predicate p       contains root (line 3). The inferred inductive predicates can
 3:     bA ← {A | A ∈ PowerSet(B) ∧ |A| ≤ n ∧ root ∈ Ai }                          contain as many stack variables as its arguments, thus we
 4:      for each A in b    A do                     ⊲ Consider a subset of B      examine each subset in the ascending order of their size.
 5:          {u 1, ..., um }m=n−|A| ← fresh(n−|A|)                                 Also, to reduce the search space, we only consider a permu-
 6:          A ← A ∪ {u 1, ..., um }m=n−|A|                                        tation (k 1, ..., kn ) if it is type-consistent with the parameters
 7:          for each permutation (k 1 , ..., kn ) in Permn (A) do                 t 1 , ..., tn of the predicate p. That is, if ki is a stack pointer
 8:              if ∀1 ≤ i ≤ n. ki ∈ B → type(ki ) <: type(ti ) then
                                                                                   variable in B then its type must be a subtype of the corre-
 9:                     F ← ∃u 1 , ..., um . p(k 1 , ..., kn )
                                                                                   sponding parameter ti ’s type (line 8).
10:                     if ∀si , hi ∈ SHr oot . si , hi k− F        hi′, ιi then
11:                                                   ′
                            R ← R ∪ {(F , ((si , hi ))i , (ιi )i )}                     Next, we construct a formula F from the inductive heap
                                                                                   predicate p(k 1 , ..., kn ) (line 9). A formula F is valid if it is
12: if ∀si , h i ∈ SHr oot . |h i | = 1 then
                                                                                   successfully checked by all models in SHr oot (line 10). This
13:     R ← R ∪ InferSingleton(root, SHr oot )
                                                                                   validity check also returns a residual heap hi′ and an exis-
14: if R = ∅ then R ← {(emp, SHr oot , (ιi = {})i )}
                                                                                   tential instantiation ι i for each stack-heap model si , hi in
15: return R
                                                                                   SHr oot . They are respectively the member of the sequence
                                                                                   of residual models and the sequence of existential instanti-
    SplitHeap uses a depth-ﬁrst search to traverse the pointer                     ations associating with the valid formula F as an inference
ﬁelds of memory cells from a root pointer to partition the                         result in the set R (line 11).
heap model hi into two non-overlapping parts: sub-heap hi′                              In the concat example, when selecting the argument set
and the remaining sub-heap hi′′ = hi \ hi′ . The sub-heap                          {x, res, tmp, nil} ∈ A, the algorithm derives the formula
hi′ contains memory cells reachable from the root pointer                          F x = ∃u 1 . dll(u 1 , nil, x, tmp). This result shows that x is the
variable up to the nil pointer or memory cells pointed to by                       last node of doubly linked lists whose head is u 1 and its
other stack pointer variables. We call these pointer variables                     next pointer is tmp. Moreover, F x models the whole sub-
or the nil pointer the boundary between the sub-heap hi′ and                       heaps of x in Figure 3, i.e., all residue models have empty
the other memory regions in the heap hi . The sub-heap hi′′                        heaps, when the existential variable u 1 is instantiated to the
may contain memory cells unreachable from root and those                           address 0x01. As another example, when considering an-
reachable from root, but also pointed-to by other stack vari-                      other set of potential arguments {x, tmp} ∈ A, we infer
ables non-aliasing with root.                                                      F x = ∃u 1 , u 2 . dll(x, u 1 , u 2 , tmp), indicating that x is the head
    For the concat example, Figure 3 illustrates that the                          of a doubly linked list segment to tmp.
boundaries of the sub-heaps h 1′ , h 2′ , and h 3′ of the root vari-      Singleton Heap Predicates We only derive singleton
able x are {x, res, nil, tmp}, {x, res, nil, tmp}, and {x, res, nil, tmp, y},
                                                                          heap predicates of root when there is a single memory
respectively. Their common boundary is {x, res, nil, tmp}.                cell in every root’s sub-model in SHr oot (line 12). We con-
                                                                                   sider a τ -typed singleton predicate template of the form
4.2    Inferring Atomic Heap Predicates                                                  τ
                                                                                   root 7→k 1 , ..., kn . The value of each ﬁeld ki in the template is
Given the sequence of sub-models SHr oot of the root pointer                       the common pointer variable (including nil) pointing to the
and its boundary B, the function InferAtom shown in Algo-                          corresponding ﬁeld of every memory cell in SHr oot . If there
rithm 2 computes a set of atomic predicates satisﬁed by all                        is no such variable, we create a fresh existential variable for
sub-models in SHr oot . These atomic (shape) predicates con-                       ki and update this variable’s instantiation to the value of
sist of either (i) inductive heap predicates whose deﬁnitions                      the corresponding ﬁeld in each model.
are given in the set P (lines 2–11), (ii) singleton predicates
of the root pointer when the heap size of all sub-models                           4.3 Pure Inference
in SHr oot is 1 (lines 12–13), or (iii) the emp predicate with
                                                                                   The heap predicates derived in the previous steps mainly
SHr oot as the residual models when it cannot derive any
                                                                                   present the heap memory, but not the relations of variables
predicates in the two former forms (line 14).
                                                                                   within a predicate and among predicates in the overall re-
Inductive Heap Predicates SLING discovers instances of                             sults. In these results, the heap predicates are solely related
each predeﬁned predicate p(t 1 , ..., tn ) ∈ P. For optimization,                  via the common stack variables in their arguments.
we ﬁlter the set P of predicate deﬁnitions to contain only                            We infer additional pure constraints over arguments of
those that have at least one parameter having the same type                        the predicates by searching for equality constraints over
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                            Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

two diﬀerent variables among stack variables, existential          predicates over combinations of variables over many col-
variable, nil, and the special variable res if we are inferring    lected stack-heap models can be slow. To improve perfor-
post-conditions which are satisﬁed by every stack model            mance, SLING uses a type-checker (Algorithm 2, line 8) to
and existential instantiation.                                     eliminate variable combinations having inconsistent types
   For example, we use this inference to obtain the relation       to observed traces. The experiments in Section 5 also show
res = x about the return value of concat and other aliasing        that only a few traces are needed to discover accurate invari-
information, e.g., those shown in Section 2.3.                     ants and the Z3-based model checker performs eﬃciently
                                                                   over these traces.
4.4   Validation
When obtaining multiple postconditions (e.g., at each return       5 Evaluation
statements), we combine them with the inferred precondi-           SLING is implemented in Python and uses the LLDB de-
tions to derive program speciﬁcations. Next, we validate           bugger [31] to collect traces at target program locations.
these speciﬁcations using frame rule of separation logic,          Below we evaluate SLING on C programs, but SLING also
i.e.,                                                              works with programs written in other languages supported
                       {P } C {Q }                                 by LLDB (e.g., C++ and Objective-C) or having debuggers
                   {R ∗ P } C {R ∗ Q }                             capable of capturing memory information (e.g., JDB for
                                                                   Java [25], PDB for Python [43], and GDB [20]).
This rule says that if a triple {P }C{Q } is valid (i.e., C exe-
                                                                     Our experiments described below are conducted on a
cutes safely in the precondition P and its post-states satisfy-
                                                                   MacBook with 2.2GHz Intel CPU, 16 GB memory, and runs
ing the postcondition Q) then the triple {R ∗ P }C{R ∗ Q }, in
                                                                   Mac OS. The source code of SLING and experimental data
which R is a frame modeling memory regions that are not
                                                                   are available at https://github.com/guolong-zheng/sling/.
manipulated by C, also holds.
    For example, if C is a function, then P and Q are the pre
                                                                   5.1 Benchmark Programs
and postconditions computed from the stack-heap models
observed at the entry and exit of C, respectively. As another      We evaluate SLING using the VCDryad benchmark [51] con-
example, if C is a loop body, then P and Q, inferred from          sisting of 153 C heap-manipulating programs collected from
the models collected at the loop’s head, are identical and         various veriﬁcation works, e.g., SV-COMP [4], GRASShop-
considered as a loop invariant.                                    per [46] and AFWP [23]. These programs range from those
    According to the frame rule, if the inferred conditions        that manipulate standard data structures (e.g., heaps and
P and Q are valid, then we can expand the corresponding            trees) to functions from popular open source libraries (e.g.,
memory regions modeled by P and Q by the same mem-                 Glib, OpenBSD) and the Linux kernel that manipulate cus-
ory regions non-overlapping with them to obtain the whole          tomized data structures. Some of these programs have non-
memories observed at the entry and exit C. Otherwise, the          trivial bugs (e.g., causing segmentation faults) intended to
inferred pair P, Q is considered invalid (spurious). Therefore,    test static analyzers. We also use 4 programs4 from [7].
we can check that the residual models corresponding to P           These programs implement non-trivial algorithms using
and Q are unchanged with respect to observed models to             multiple data structures (e.g., the Schorr-Waite graph mark-
determine the validity of this result.                             ing algorithm using binary trees).
    In concat, we obtain the precondition F L1 ′ and two post-        In total, these benchmark programs contain a wide vari-
              ′                           ′
conditions F L2 (when x = nil) and F L3 (when x , nil). For        ety of structures including singly-linked lists, doubly-linked
each pair of a model collected at L1 and the corresponding         lists, sorted lists, circular lists, binary trees, AVL trees, red-
model collected at L2 or L3, we check if the residual heap         black trees, heaps, queues, stacks, iterators, etc. Moreover,
in the model at L1, which is not captured by F L1     ′ , is the   these programs contain documented invariants (e.g., pre
same as the residual heap in model at L2 or L3, which is not       and postconditions such as those given in Section 2.1),
captured by F L2′ or F ′ , respectively. For example, given the    which we use to evaluate SLING’s inferred invariants.
                       L3
model at L1 in Figure 2a and its corresponding model t 1 at           Table 1 shows these 157 programs (the last row shows the
L3 in Figure 2b, the residual heaps corresponding to F L1 ′ and    4 programs from [7]). Column Programs lists the programs,
  ′
F L3 are both empty. On the other hand, in the last iteration      categorized by data structures that they use. Column LoC
of concat (when x = nil), the residual heaps of F L1 ′ and F ′     shows the total lines of code of these programs. For example,
                                                              L2
both contain three memory cells 0x01, 0x02, and 0x03.              the ﬁrst row lists 8 programs that use standard singly-link
                                                                   lists (SLL) and have in total 168 LoC. In total, we have 157
4.5   Complexity                                                   programs in 22 categories with 4649 lines of C code.
SLING is exponential in the number of predicates and their
parameters. In addition, the complexity of the general heap        4 This benchmark has 6 programs, we use 4 of them and exclude the other

model checking problem is EXPTIME [7]. Thus, checking              2 because they use concurrency which SLING currently does not support.
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                                 PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

Table 1. Experimental results. Programs denoted with ∗ contain bugs preventing us to obtain traces. Programs denoted with
† cause SLING to timeout at certain locations. Italic programs have locations that cannot be reached using random inputs.

Bold programs contain locations with free statements that give invalid traces. SLL and DLL stand for Singly and Doubly
Linked Lists, respectively.

Programs                                                                                          Total                  Avg. Per Inv
                                                                                  LoC iLocs Traces Invs A/S/X Time(s) Single Pred Pure
SLL (8): append, delAll, ﬁnd, insert, reverse, insertFront, insertBack, copy      168 26     226     30 8/0/0 40.54    0.37 0.83 1.03
Sorted List (10): concat, ﬁnd, ﬁndLast, insert, insertIter, delAll,
                                                                                  268   25    194      82     9/0/1   137.32   0.39   2.40 0.67
reverseSort, insertionSort, mergeSort, quickSort∗
DLL (12): append, concat, meld, delAll, insertBack, insertFront, midInsert,
                                                                                  160   31    168     238     12/0/0 399.12    0.46   1.68 3.93
midDel, midDelError, midDelHd, midDelStar, midDelMid
Circular List (4): insertFront, insertBack, delFront, delBack                      97   11     14    42(16)   2/2/0   11.43    0.81   1.19   2.10
Binary Search Tree (5): del, ﬁndIter, ﬁnd, insert, rmRoot∗                        144   16     66      24     2/2/1   24.02    0.50   1.21   1.54
AVL Tree (4): avlBalance, del, ﬁndSmallest, insert                                194   13     56      37     2/2/0   22.12    1.22   0.57   3.08
Priority Tree (4): del, ﬁnd, insert, rmRoot                                       154   19     64     273     2/2/0   341.37   3.30   1.66   3.30
Red-black Tree (2): del∗ , insert                                                 287   11     70      63     0/1/1    44.8    2.10   1.08   8.11
Tree Traversal (5): traverseInorder, traversePostorder, traversePreorder,
                                                                                  168   12    174      12     4/0/1   22.93    0.08   0.58 0.50
tree2list, tree2listIter∗
glib/glist_DLL (10): ﬁnd, free, index, last,
                                                                                  216   31    128   435(20) 9/1/0     403.13    0     2.61 7.29
length, nth, nthData, position, prepend, reverse
glib/glist_SLL (22): append, concat, copy, delLink, ﬁnd, free, index,
insertAtPos, insertBefore, insertSorted, last, length, nth, nthData,              606   69    299   382(11) 17/5/0 879.35      0.56   2.28 2.07
position, prepend, rm, rmAll, rmLink, reverse, sortMerge, sortReal
OpenBSD Queue (6): init, insertAfter, insertHd, insertTl, rmAfter, rmHd           105   12     12    27(4)    4/2/0   10.04    0.15   2.04 0.15
Memory Region (1): memRegionDllOps                                                 67   7      14     52      1/0/0   17.70    0.73   0.81 7.96
Binomial Heap (2): ﬁndMin, merge                                                  117   8      54     89      0/2/0   76.56    1.39   0.90 9.15
SV-COMP (Heap Programs) (7): allocSlave, insertSlave,
                                                                                  119   16     34      71     7/0/0   58.17    0.24   1.66 3.41
createSlave, destroySlave, add, del, init
GRASShopper_SLL (Iterative) (8): concat, copy, dispose, ﬁlter, insert, rm,
                                                                                  193   27    111    98(9)    6/2/0   71.03    0.17   2.72 1.15
reverse, traverse
GRASShopper_SLL (Recursive) (8): concat, copy, dispose, ﬁlter, insert, rm,
                                                                                  173   24    118    40(3)    6/2/0   30.94    0.28   2.00   1.1
reverse, traverse
GRASShopper_DLL (8): concat, copy, dispose, ﬁlter† , insert, rm,
                                                                                  209   24    108   638(20) 5/2/1     803.58   0.04   2.95 8.50
reverse, traverse
GRASShopper_SortedList (14): concat, copy, dispose, ﬁlter, insert, reverse,
                                                                                  394   43    195    222(1) 10/2/2    160.1    1.04   2.27 4.29
rm, split, traverse, merge, doubleAll, pairwiseSum, insertionSort† , mergeSort∗
AFWP_SLL (11): create, delAll, ﬁnd, last, reverse, rotate, swap, insert, del† ,
                                                                                  264   25     89    94(11) 7/3/1     71.04    0.18   1.73 1.85
ﬁlter, merge
AFWP_DLL (2): dll_ﬁx, dll_splice                                                   40   5     16      133     2/0/0   75.51    0.02   2.96 6.67
Cyclist (4): aplas-stack, composite4, iter, schorr-waite                          506   32    360     132     1/3/0   165.26   0.27   0.63 0.67


5.2 Setup                                                                         benchmark programs often modify and loop over data (e.g.,
For each program, we obtain traces, i.e., stack-heap models,                      as in concat), allowing us to generate suﬃcient and diverse
to infer invariants at program entrances for preconditions,                       traces.
at loop entrances for loop invariants, and at program exits                          For each category shown in Table 1, we adopt the predi-
for postconditions (we systematically obtain traces at each                       cate deﬁnitions given for that data from the benchmark pro-
return statement in a program). We use LLDB to set break-                         grams, e.g., all programs DLL use the dll inductive predicate
points at these locations to collect traces.                                      shown in Section 2. The shape and complexity of these pred-
   To obtain traces, we run each program on empty and ran-                        icates vary, e.g., dll has 4 parameters, 1 singleton predicate,
domly generated data structure inputs of a ﬁxed size of 10.                       and 1 inductive predicate, and the treeSeg predicate has 2
For example, for the concat program in Figure 1 that takes                        parameters, 2 singletons, and 4 inductive predicates.
as input 2 doubly-linked lists, we generate 3 inputs consist-                        Programs in several categories such as SV-COMP and
ing of a nil list and two randomly generated doubly-linked                        Cyclist use complex nested data structures, which are
lists a, b of size 10. Then we run concat over all input com-                     data structures whose ﬁelds are other data structures. The
binations, e.g., (nil,a), (nil,b), (a,b), . . . . Although
these inputs are random and relatively small (size 10), the
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                                  Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

predicates for these data structures involve multiple predi-              (bold text), we obtained invalid traces and therefore gen-
cates that are quite complex, e.g., the iter predicate has 10             erated spurious invariants. This is an interesting behavior
parameters, 5 singleton and 6 inductive predicates.                       of running C programs and the LLDB debugger: a free(x)
                                                                          statement does not immediately free the pointer x so LLDB
5.3 Results                                                               still observes (now invalid) heap values of x in the execu-
Table 1 shows our results. Columns iLocs, Traces, and Invs                tion traces. Thus we conservatively consider all generated
lists, for programs in each category, the total number of tar-            invariants depending on these traces spurious and report
get locations, obtained traces, and generated invariants, re-             them in Table 1.
spectively. Column Invs also lists the number of spurious                    For other programs (and those where we only obtain
invariants in parentheses (rows with no such parentheses                  traces at certain locations), we manually analyzed and com-
have no spurious invariants). Finally, column Time lists the              pared SLING’s generated invariants to documented ones.
total analysis time in seconds (including program execution,              First, we found that all generated invariants are correct,
trace collection, and invariant inference).                               i.e., they are true invariants at the considered locations.
   For several programs, we were not able to obtain traces                Thus, the spurious results reported in Table 1 are only
at considered locations using random inputs and thus could                those caused by invalid traces as described above. Second,
not infer invariants at those locations. Column A/S/X shows               our results either matched (syntactically or semantically
the number of programs where we obtained traces at all con-               equivalent) or, in many cases, were stronger than the doc-
sidered locations (A), obtained traces for some locations or              umented invariants. For example, for SLL/reverse, we
inferred spurious results (S), and could not obtain traces or             inferred the documented postcondition sll(res) and the
invariants at some locations (X). For example, for the 5 pro-             additional constraints x = nil ∧ x = tmp showing that the
grams using binary search trees, we obtained traces at all                header of the input list x becomes the tail of the resulting
considered locations in 2 programs, obtained traces at some               list. In many similar cases, we achieved stronger results
locations in 2 programs, and could not obtain any traces in               by inferring both the expected invariants and additional
one program (quicksort).                                                  equalities.
   The last three columns in the table give additional details               A potential reason for these sound results is because
about the generated invariants. Columns Single, Pred, and                 SLING only infers shape properties using inductive pred-
Pure list the average numbers of singleton predicates (e.g.,              icates and pure equalities. These properties have strict
 node                                                                     patterns and thus a property that holds for the observed
x 7→ nx, pr), inductive predicates (e.g., dll), and pure equali-
                                                                          traces will likely hold for others. We also do not consider
ties (e.g., x = res) found in the invariants, respectively.
                                                                          general disjunctive invariants or numerical relations (e.g.,
   In total, SLING generated 3214 invariants in 487 target
                                                                          only check equivalences among memory addresses and
locations (average 6.60 invariants per location). These in-
                                                                          do not consider other relationships such as the address of
variants consists of 309 preconditions, 2442 postconditions
                                                                          x is greater than that of y). Existing numerical invariant
and 463 loop invariants. The total run time of SLING is
                                                                          studies [38, 39] have shown that dynamic analysis often
3866.06s for 149 programs5 (average 25.95s per program and
                                                                          produces many spurious invariants involving disjunctions
1.2s per invariant). The time to run the program and collect-
                                                                          and general inequalities.
ing traces is negligible (about a second for all programs).
                                                                             Although we tried our best to carefully check all gener-
   Out of 157 programs, we were not able to obtain any
                                                                          ated results, the process of checking many complex SL in-
traces for 5 programs (marked with ∗ in the table). These
                                                                          variants manually is time-consuming and diﬃcult. In future
programs contain bugs that immediately result in runtime
                                                                          work, we will use an automatic veriﬁer that supports SL for-
errors such as segmentation faults (thus we obtained no
                                                                          mulae to check SLING’s invariants (see additional details in
traces and inferred no invariants). For 15 programs (italic
                                                                          Section 6). Moreover, we might be able to leverage test-input
text), we could not reach certain return branches using ran-
                                                                          generation techniques, e.g., symbolic execution with lazy-
dom inputs and thus were not able to obtain traces or infer
                                                                          initialization [28] or SL predicates [27], to construct smart
invariants at those locations. For 3 programs (marked with
                                                                          inputs, which can explore hard-to-reach program paths to
†), we were able to generate pre and postconditions, but
                                                                          infer better invariants.
not loop invariants. For these programs we hit loops more
frequently than program entrance/exit points and thus ob-                 5.4 Uses of Inferred Invariants
tained many traces for loops. Checking generated formulae
                                                                          Dynamically inferred invariants can help users understand
over many traces is expensive (Section 4.5) and appears
                                                                          programs (e.g., discovering loop invariants, pre and postcon-
to cause Z3 to stop responding. Finally, for 17 programs
                                                                          ditions for unknown programs) and gain conﬁdence about
                                                                          expected properties (e.g., the generated invariants met the
5 We exclude the 5 buggy programs that produce no traces and 3 programs   expectation). They can also be used to catch regression
that cause Z3 to time out.                                                bugs: the user instruments these invariants as assertions
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                            PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

in code to detect changes that break these assertions when                                 Table 2. Comparing SLING to S2.
the program run6 . Existing works also list many other uses
of dynamic invariants including documentation, complex-                         Programs               Total Both S2 SLING Neither
                                                                                SLL                      9    8    0   1      0
ity analysis, fault localization, and bug repair [1, 15, 37, 45].
                                                                                Sorted List             14    6    0   6      2
Below we show two concrete uses of SLING’s SL invariants.                       DLL                     13    0    0   13     0
                                                                                Circular List            4    0    0   2      2
Explaining Bugs Although SLING cannot generate in-
                                                                                Binary Search Tree       6    1    1   2      2
puts to reach a buggy location, it can, when given such                         AVL Tree                 4    0    0   2      2
inputs, discover useful invariants to alert and help the de-                    Priority Tree            4    1    1   1      1
veloper analyze that bug. For Red-black Tree/insert,                            Red-black Tree           2    0    0   0      2
we obtained an invariant that appears too “simple”. Man-                        Tree Traversal           6    3    0   2      1
ual inspection showed that the inferred invariant is indeed                     glib/glist_DLL          19    0    0   18     1
correct: the program always crashes after the ﬁrst iteration,                   glib/glist_SLL          40    6    0   29     5
                                                                                OpenBSD Queue            6    0    0   4      2
thus the inferred invariant only captures a portion of data
                                                                                Memory Region            3    1    0   2      0
operated during the ﬁrst iteration. For glib/glist_SLL/sortMerge,               Binomial Heap            2    0    1   0      1
SLING reported an unexpected postcondition stating that                         SV-COMP                  9    0    0   9      0
the result is always null. Manual inspection revealed this is                   GRASShopper_SLL (Iter)  16    2    0   12     2
correct and is due to a (typo) bug in the program that returns                  GRASShopper_SLL (Rec)    8    3    2   3      0
list_next instead of list->next. For AFWP/dll_fix.c,                            GRASShopper_DLL         16    0    0   13     3
                                                                                GRASShopper_SortedList 29     1    0   24     4
the expected loop invariant is ∃u 1 , u 2 , u 3 , u 4 . sll(i)∗dll(j, u 1 , k, u 2 )∗
                                                                                AFWP_SLL                20    1    0   15     4
dll(k, u 3 , u 4 , nil), but SLING returned sll(i) ∧ i = h ∧ k = j ∧            AFWP_DLL                 3    0    0   3      0
k = nil. Thus, the expected invariant shows that k can be                       Cyclist                  4    0    0   1      3
non-nil, but SLING’s invariant shows the opposite. Man-                                  Total Sum               237 33 5   162     37
ual inspection showed a (potentially seeded) bug, where a
guard checking for k = nil was commented out. Indeed, with
this guard uncommented, SLING inferred the expected in-                              conﬁrmed the warning and even revealed that the error is
variant.                                                                             caused by a dangling pointer.
Identifying Spurious Warnings SLING’s invariants can                       5.5 Comparing to the S2 Static Analyzer
help check results from static analyzers, e.g., to understand
and gain conﬁdence about reported results or detect po-                    We compare SLING to the static tool S2 [29], which uses the
tential problems. The FBInfer tool mentioned in Section 1                  state-of-the-art bi-abduction technique [9] in SL to generate
is a well-known SL static analyzer that produces warn-                     invariants proving memory safety of C programs, e.g., no
                                                                           null pointer dereferencing and memory leaks. In addition
ings for memory safety bugs for iOS and Android apps.
However, FBInfer can produce spurious (false positive)                     to memory checking, S2 attempts to ﬁnd strongest speciﬁ-
warnings. For example, when analyzing the correct ver-                     cations consisting of pre and postconditions for heap pro-
sion of the mentioned glib/glist_SLL/sortMerge pro-                        grams.
gram, FBInfer reported a memory leak after the assignment                     We compare S2 to SLING using the same C benchmark
l->next = NULL; at the end of a loop because it thinks that                programs8 listed in Table 1. S2 only supports shape invari-
l->next is not reachable. However, SLING’s inferred in-                    ants, thus we only compare shape invariants generated by
variants at that location showed l->next is a valid alias to               the two tools and ignore the pure invariants generated by
                                                                           SLING. Moreover, S2 does not infer invariants at arbitrary
other pointer variables and reachable. Manual inspection
conﬁrmed that SLING’s generated invariants are correct                     locations like SLING, instead it attempts to ﬁnd complete
and the program has no memory leak at that location. We                    speciﬁcations (involving both pre and postconditions) and
applied the same technique and found similar spurious                      loop invariants. Thus, we do not consider invariants gener-
warnings from FBInfer for 7 other programs7 .                              ated at individual locations as shown in Table 1 and instead
   Note that FBInfer also reported an error at another loca-               consider speciﬁcations as a whole and loop invariants. Note
tion of sortMerge. However, this time, SLING’s invariants                  that each program has a speciﬁcation but only programs
                                                                           with loops have loop invariants. As with SLING, we man-
6 The work in [36] shows how to encode SL formulae, which contain non-     ual analyze the results of S2 and compare them to the docu-
standard operations such as ∗ , to executable functions that can be used   mented invariants9 .
assertions in code to enable run-time checking.
7 Programs with spurious warnings: merge in Binomial_Heap, delBack         8 Several of these programs, e.g., those in SLL, DLL, and Binary trees, are

in Circular_List, copy in Grasshopper_SLL(Rec), insert in                  also used in [29] to evaluate S2’s capability of proving memory safety.
GRASShopper_DLL, GRASShoper_SLL(Iter), GRASShoper_SortedList,              9 We use these documented, veriﬁed invariants as “ground truths” and

and Grasshopper_SLL(Rec).                                                  check if S2’s results can match them. It is possible that these invariants
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                                  Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

   Table 2 shows the comparison results. Column Programs                     Static program analysis in SL has rapidly gained adoption
lists the program categories, similarly to those listed in                from both academia and industry in the past decade. Mem-
Table 1. Column Total lists the number of documented                      CAD [22] and THOR [33, 34] reason about shape and numer-
properties consisting of speciﬁcations and loop invariants                ical properties of programs, but generate invariants for a re-
for the programs in the corresponding category. The next                  stricted language of list manipulating programs [32]. FBIn-
four columns list the respective numbers of properties that               fer [8, 17] uses bi-abduction to generate invariants to detect
Both tools can generate, S2 can generate but SLING cannot,                real memory bugs, but only supports simple structures (e.g.,
SLING can generate but S2 cannot, and Neither tools can                   linked lists) and restricted language features (e.g., no arith-
generate. For example, the 10 programs in Sorted List                     metic). CABER [6] and S2 (described in Section 5.5) also use
have 14 properties (10 speciﬁcations and 4 loop invariants),              bi-abduction to oﬀer more general, but more expensive, ap-
from which there are 6 properties that both tool found, none              proaches to infer shape properties. These tools do not con-
that only S2 found, 6 that only SLING found, and 2 that both              sider invariants at arbitrary locations: CABER only analyzes
fail to ﬁnd. Finally, S2 takes less than a second for all but             preconditions and S2 only infers pre and postconditions.
the 4 concat programs in the GRASShopper categories, from                    The data-driven tool DOrder [52] generates speciﬁcations
which S2 appears to stop responding.                                      for data structures in OCaml. Given the deﬁnition of a data
   The last row of Table 2 summarizes the results. First,                 structure, DOrder generates predicates capturing shape and
both tools discovered and failed about 14% and 15% of the                 ordering relations among data (e.g., element x is reachable
properties, respectively. Properties found by both tools are              from element y or the value x appears in the left subtree of
from simple recursive programs with singly-linked lists and               a node containing the value y), learns speciﬁcations from
trees. For programs containing properties that neither tool               predicates and in/output data, and veriﬁes speciﬁcations us-
found, we observed no patterns and diﬀerent failure reasons,              ing a reﬁnement type system. SLING makes an orthogonal
e.g., for SLL/quicksort, S2 did not produce any speciﬁca-                 contribution in ﬁnding a diﬀerent form of shape properties
tion while SLING inferred no properties due the program                   to express sharing and aliasing information, e.g., nodes x
crashed and produced no traces. Next, S2 found 5 properties               and y point to (sub)trees in separate heaps.
that SLING did not. These properties are mostly in programs                  The tool Locust [5] hybridizes dynamic and static analy-
where SLING obtained incomplete or spurious results due to                ses to infer SL invariants for programs written in a restricted
lack of traces, e.g., binary_search_tree/find_rec.c, or                   language. To infer an invariant, Locust expands the syntax
the “free” problem, e.g., GRASShopper/rec/dispose.c (de-                  of an SL formula using a machine learning model trained
tails in Section 5.3). Finally, SLING found many properties               from a large set of data. Locust iteratively reﬁnes inferred in-
that S2 did not (162/237). For these properties, which often              variants using counterexamples obtained by the Grasshop-
come from complex programs with rich data structures, S2                  per static veriﬁer [46]. Locust is mainly evaluated on exam-
either completely failed to produce them or produced much                 ple programs with singly-linked lists and binary trees and
weaker than expected results.                                             does not support more complex data structures (e.g., Locust
   In summary, SLING found more documented invariants                     does not support doubly-linked list and returns no results
comparing to S2. We ﬁnd this result encouraging as it shows               when applied to our concat example). The tool also relies
the competitiveness of SLING to static analyzers.                         on an expensive training process over large data sets.
                                                                             Finally, automatic veriﬁcation tools such as HIP [10],
                                                                          Grasshopper [46], Verifast [24], and VCDryad [44] can
6    Related Work
                                                                          prove given SL speciﬁcations and invariants in heap-based
SLING is inspired by the well-known dynamic invariant tool                programs. In future work, we intend to use these tools to
Daikon [14, 15]. Daikon comes with a large list of invariant              automatically check SLING’s inferred invariants.
templates and predicates, tests them against program traces,
removes those that fail, and reports the remains as candidate
invariants. Recently, several techniques (such as PIE [42],               7 Conclusion
ICE [19], DIG [38], and SymInfer [37]) have been developed                We introduce a new dynamic analysis to infer SL invariants
to infer numerical invariants using a hybrid approach that                for heap-manipulating programs. The approach is based on
dynamically infers candidate invariants and then statically               the insight that the heap at a program location can be par-
checks them against the program code. These approaches                    titioned into disjoint regions reachable from various stack
do not consider SL invariants for memory shape analysis.                  variables and that these regions can be modeled by atomic
                                                                          SL formulae. Moreover, these formulae can be dynamically
                                                                          inferred and then combined using separating conjunction.
                                                                             We present SLING, a tool that implements these ideas
are incomplete and not the “best” and thus non-matching results from S2   to generate SL invariants at arbitrary program locations.
do not necessarily mean they are worse than these invariants.             SLING has several technical details including ﬁnding and
SLING: Using Dynamic Analysis to Infer Program Invariants . . .                                PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

using boundary variables instantiate predicates, using an                      [15] Michael D. Ernst, Jeﬀ H. Perkins, Philip J. Guo, Stephen McCamant,
SL model checker to compute both an instantiation for exis-                         Carlos Pacheco, Matthew S. Tschantz, and Chen Xiao. 2007. The
tential variables and the residual heap, and using the frame                        Daikon system for dynamic detection of likely invariants. Science of
                                                                                    Computer Programming (2007), 35–45.
rule to validate inferred speciﬁcations.                                       [16] Daniel Fava, Julien Signoles, Matthieu Lemerre, Martin Schäf, and
  Preliminary results on a large set of nontrivial programs                         Ashish Tiwari. 2015. Gamifying program analysis. In LPAR. Springer,
show that SLING is eﬀective in discovering useful invariants                        591–605.
describing operations over a wide variety of data structures.                  [17] FBInfer 2018. The Infer Static Analyzer. http://fbinfer.com/.
We believe that SLING takes an important step in broaden-                      [18] Cormac Flanagan and K. Rustan M. Leino. 2001. Houdini, an Annota-
                                                                                    tion Assistant for ESC/Java. In Formal Methods for Increasing Software
ing the space of properties about heap programs that can                            Productivity. 500–517.
be dynamically inferred and exposes opportunities for re-                      [19] Pranav Garg, Daniel Neider, P. Madhusudan, and Dan Roth. 2016.
searchers to exploit new dynamic SL invariant analyses.                             Learning Invariants Using Decision Trees and Implication Counterex-
                                                                                    amples. In POPL. 499–512.
                                                                               [20] GDB 2018.                GDB: The GNU Project Debugger.
Acknowledgments                                                                     https://www.gnu.org/software/gdb/.
We thank our shepherd Nadia Polikarpova and the anony-                         [21] Charles Antony Richard Hoare. 1969. An axiomatic basis for com-
                                                                                    puter programming. Commun. ACM 12, 10 (1969), 576–580.
mous reviewers for their feedback. The ﬁrst author was sup-
                                                                               [22] Hugo Illous, Matthieu Lemerre, and Xavier Rival. 2017. A Relational
ported by the Oﬃce of Naval Research award N000141712787.                           Shape Abstract Domain. In NASA Formal Methods. 212–229.
                                                                               [23] Shachar Itzhaky, Anindya Banerjee, Neil Immerman, Aleksandar
References                                                                          Nanevski, and Mooly Sagiv. 2013. Eﬀectively-Propositional Reason-
                                                                                    ing about Reachability in Linked Data Structures. In CAV. 756–772.
 [1] Tien-Duy B Le, David Lo, Claire Le Goues, and Lars Grunske. 2016. A
                                                                               [24] Bart Jacobs, Jan Smans, Pieter Philippaerts, Frédéric Vogels, Willem
     learning-to-rank based fault localization approach using likely invari-
                                                                                    Penninckx, and Frank Piessens. 2011. VeriFast: A Powerful, Sound,
     ants. In ISSTA. ACM, 177–188.
                                                                                    Predictable, Fast Veriﬁer for C and Java. In NASA Formal Methods. 41–
 [2] Thomas Ball and Sriram K. Rajamani. 2002. The SLAM Project: De-
                                                                                    55.
     bugging System Software via Static Analysis. In POPL. 1–3.
                                                                               [25] JDB       2018.               jdb     -     The    Java     Debugger.
 [3] Josh Berdine, Cristiano Calcagno, and Peter W. O’Hearn. 2004. A De-
                                                                                    https://docs.oracle.com/javase/8/docs/technotes/tools/windows/jdb.html.
     cidable Fragment of Separation Logic. In Foundations of Software Tech-
                                                                               [26] Neil D. Jones and Steven S. Muchnick. 1982. A Flexible Approach
     nology and Theoretical Computer Science. 97–109.
                                                                                    to Interprocedural Data Flow Analysis and Programs with Recursive
 [4] Dirk Beyer. 2017. Software Veriﬁcation with Validation of Results. In
                                                                                    Data Structures. In POPL. 66–74.
     TACAS. 331–349.                                                           [27] JSF 2018.       JSF: The Java StarFinder Symbolic Execution Tool.
 [5] Marc Brockschmidt, Yuxin Chen, Pushmeet Kohli, Siddharth Krishna,              https://github.com/star-finder/jpf-star.
     and Daniel Tarlow. 2017. Learning Shape Analysis. In Static Analysis      [28] Sarfraz Khurshid, Corina S Păsăreanu, and Willem Visser. 2003.
     Symposium. 66–87.                                                              Generalized symbolic execution for model checking and testing. In
 [6] James Brotherston and Nikos Gorogiannis. 2014. Cyclic Abduction of             TACAS. Springer, 553–568.
     Inductively Deﬁned Safety and Termination Preconditions. In Static        [29] Quang Loc Le, Cristian Gherghina, Shengchao Qin, and Wei-Ngan
     Analysis. 68–84.                                                               Chin. 2014. Shape Analysis via Second-Order Bi-Abduction. In CAV.
 [7] James Brotherston, Nikos Gorogiannis, Max I. Kanovich, and Reuben              52–68.
     Rowe. 2016. Model checking for symbolic-heap separation logic with        [30] Xavier Leroy. 2006. Formal certiﬁcation of a compiler back-end or:
     inductive predicates. In POPL. 84–96.                                          programming a compiler with a proof assistant. In POPL. 42–54.
 [8] Cristiano Calcagno, Dino Distefano, Jérémy Dubreil, Dominik Gabi,         [31] LLDB 2018. The LLDB Debugger. https://lldb.llvm.org/.
     Pieter Hooimeijer, Martino Luca, Peter W. O’Hearn, Irene Papakon-         [32] Stephen Magill, Aleksandar Nanevski, Edmund Clarke, and Peter Lee.
     stantinou, Jim Purbrick, and Dulma Rodriguez. 2015. Moving Fast                2006. Inferring invariants in separation logic for imperative list-
     with Software Veriﬁcation. In NASA Formal Methods. 3–11.                       processing programs. SPACE 1, 1 (2006), 5–7.
 [9] Cristiano Calcagno, Dino Distefano, Peter W. O’Hearn, and Hongseok        [33] Stephen Magill, Ming-Hsien Tsai, Peter Lee, and Yih-Kuen Tsay. 2008.
     Yang. 2011. Compositional Shape Analysis by Means of Bi-Abduction.             THOR: A Tool for Reasoning about Shape and Arithmetic. In CAV.
     J. ACM 58, 6 (2011), 26:1–26:66.                                               428–432.
[10] Wei-Ngan Chin, Cristina David, Huu Hai Nguyen, and Shengchao              [34] Stephen Magill, Ming-Hsien Tsai, Peter Lee, and Yih-Kuen Tsay. 2010.
     Qin. 2012. Automated veriﬁcation of shape, size and bag properties             Automatic numeric abstractions for heap-manipulating programs. In
     via user-deﬁned predicates in separation logic. Sci. Comput. Program.          POPL. 211–222.
     77, 9 (2012), 1006–1036.                                                  [35] Juan Antonio Navarro Pérez and Andrey Rybalchenko. 2011. Separa-
[11] Byron Cook, Christoph Haase, Joël Ouaknine, Matthew J. Parkinson,              tion Logic + Superposition Calculus = Heap Theorem Prover. In PLDI.
     and James Worrell. 2011. Tractable Reasoning in a Fragment of Sepa-            556–566.
     ration Logic. In CONCUR. 235–249.                                         [36] Huu Hai Nguyen, Viktor Kuncak, and Wei-Ngan Chin. 2008. Runtime
[12] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An eﬃcient SMT                Checking for Separation Logic. In VMCAI. 203–217.
     solver. In TACAS. 337–340.                                                [37] ThanhVu Nguyen, Matthew Dwyer, and William Visser. 2017. SymIn-
[13] Edsger W. Dijkstra. 1975. Guarded commands, nondeterminacy and                 fer: Inferring Program Invariants using Symbolic States. In ASE. 804–
     formal derivation of programs. Commun. ACM 18 (1975), 453–457.                 814.
     Issue 8.                                                                  [38] ThanhVu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie
[14] Michael D Ernst, Jake Cockrell, William G Griswold, and David                  Forrest. 2014. DIG: A Dynamic Invariant Generator for Polynomial
     Notkin. 2001. Dynamically discovering likely program invariants to             and Array Invariants. Transactions on Software Engineering Method-
     support program evolution. Transactions on Software Engineering 27,            ology 23, 4 (2014), 30:1–30:30.
     2 (2001), 99–123.
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA                                      Ton Chanh Le, Guolong Zheng, and ThanhVu Nguyen

[39] ThanhVu Nguyen, Deepak Kapur, Westley Weimer, and Stephanie                  errors in deployed software. In Symposium on Operating Systems Prin-
     Forrest. 2014. Using Dynamic Analysis to Generate Disjunctive In-            ciples. 87–102.
     variants.. In ICSE. 608–619.                                            [46] Ruzica Piskac, Thomas Wies, and Damien Zuﬀerey. 2014. GRASShop-
[40] Peter W. O’Hearn. 2016. CurryOn ’16 Talk: Move fast to ﬁx more               per - Complete Heap Veriﬁcation with Mixed Speciﬁcations. In
     things.                                                                      TACAS. 124–139.
[41] Peter W. O’Hearn, John C. Reynolds, and Hongseok Yang. 2001. Local      [47] John C. Reynolds. 2002. Separation Logic: A Logic for Shared Mutable
     Reasoning about Programs that Alter Data Structures. In CSL. 1–19.           Data Structures. In Symposium on Logic in Computer Science. 55–74.
[42] Saswat Padhi, Rahul Sharma, and Todd Millstein. 2016. Data-driven       [48] Mooly Sagiv, Thomas Reps, and Reinhard Wilhelm. 2002. Parametric
     Precondition Inference with Learned Features. In PLDI. 42–56.                shape analysis via 3-valued logic. TOPLAS 24, 3 (2002), 217–298.
[43] PDB      2018.               pdb   -    The    Python     Debugger.     [49] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan
     https://docs.python.org/2/library/pdb.html.                                  Chin. 2016. Automated Mutual Explicit Induction Proof in Separation
[44] Edgar Pek, Xiaokang Qiu, and P. Madhusudan. 2014. Natural Proofs             Logic. In FM. 659–676.
     for Data Structure Manipulation in C Using Separation Logic. In PLDI.   [50] Quang-Trung Ta, Ton Chanh Le, Siau-Cheng Khoo, and Wei-Ngan
     440–451.                                                                     Chin. 2018. Automated Lemma Synthesis in Symbolic-heap Separa-
[45] Jeﬀ H. Perkins, Sunghun Kim, Sam Larsen, Saman Amarasinghe,                  tion Logic. PACMPL 2, POPL (2018), 9:1–9:29.
     Jonathan Bachrach, Michael Carbin, Carlos Pacheco, Frank Sher-          [51] VCDryad 2018.        Automated deductive veriﬁcation framework.
     wood, Stelios Sidiroglou, Greg Sullivan, Weng-Fai Wong, Yoav Zibin,          http://madhu.cs.illinois.edu/vcdryad/.
     Michael D. Ernst, and Martin Rinard. 2009. Automatically patching       [52] He Zhu, Gustavo Petri, and Suresh Jagannathan. 2016. Automatically
                                                                                  learning shape speciﬁcations. In PLDI. ACM, 491–507.
