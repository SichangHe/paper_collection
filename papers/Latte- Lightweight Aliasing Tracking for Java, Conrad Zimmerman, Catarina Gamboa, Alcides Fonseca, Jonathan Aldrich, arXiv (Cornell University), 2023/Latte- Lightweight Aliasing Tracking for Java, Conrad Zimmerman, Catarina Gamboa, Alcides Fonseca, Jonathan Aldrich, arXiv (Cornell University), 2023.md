                                                     Latte: Lightweight Aliasing Tracking for Java
                                                                 Conrad Zimmerman∗                                         Catarina Gamboa∗
                                                                   Brown University                                 Carnegie Mellon University, and
                                                                  Providence, RI, USA                        Faculdade de Ciências da Universidade de Lisboa
                                                            conrad_zimmerman@brown.edu                                    Pittsburgh, PA, USA
                                                                                                                       cgamboa@andrew.cmu.edu

                                                                     Alcides Fonseca                                       Jonathan Aldrich
                                                  Faculdade de Ciências da Universidade de Lisboa                      Carnegie Mellon University
arXiv:2309.05637v1 [cs.PL] 11 Sep 2023




                                                                 Lisbon, Portugal                                          Pittsburgh, PA, USA
                                                                amfonseca@fc.ul.pt                                    jonathan.aldrich@cs.cmu.edu

                                         Abstract                                                         the hardest concepts to learn in the Rust programming lan-
                                         Many existing systems track aliasing and uniqueness, each        guage [19, 23].
                                         with their own trade-oﬀ between expressiveness and devel-           Thus, we propose a type system for uniqueness and alias-
                                         oper eﬀort.                                                      ing that aims to be more usable and impose low overhead
                                            We propose Latte, a new approach that aims to minimize        on developers. Moreover, we intend to keep our approach
                                         both the amount of annotations and the complexity of in-         as simple as possible so that it can support the development
                                         variants necessary for reasoning about aliasing in an object-    of more complex type systems (like Liquid Types [24]) that
                                         oriented language with mutation. Our approach only requires      require reasoning about uniqueness and aliasing.
                                         annotations for parameters and ﬁelds, while annotations for         In particular, we propose a type system for a subset of the
                                         local variables are inferred. Furthermore, it relaxes unique-    Java language that tracks uniqueness and heap aliasing with
                                         ness to allow aliasing among local variables, as long as this    low annotation eﬀort and no necessary runtime changes. To
                                         aliasing can be precisely determined. This enables support       handle uniqueness, we provide the developer with the sim-
                                         for destructive reads without changes to the language or its     ple invariant that no two references in the heap point to the
                                         run-time semantics.                                              same unique object.
                                            Despite this simplicity, we show how this design can still       We require few annotations, speciﬁcally two (unique and
                                         be used for tracking uniqueness and aliasing in a local se-      shared) for object ﬁelds and return types, and three (adding
                                         quential setting, with practical applications, such as model-    owned) for method parameters, and we infer the remaining
                                         ing a stack.                                                     information for local variables.
                                                                                                             Moreover, we aim to maintain Java’s runtime semantics
                                         CCS Concepts: • Theory of computation → Program se-              unaltered, and therefore do not build in destructive reads;
                                         mantics; • Software and its engineering → Object ori-            the programmer can, however, get a similar eﬀect with an
                                         ented languages.                                                 explicit assignment to null.
                                         Keywords: aliasing, uniqueness, ownership, java                     In the remainder of the paper, we present an overview
                                                                                                          of previous work that is closely related to ours (Section 2),
                                         1    Introduction                                                followed by our approach with the presentation of an exam-
                                                                                                          ple and the system’s grammar and typing rules (Section 3).
                                         From low-level languages like C to high-level programming
                                                                                                          At the end, we discuss some of the system’s limitations and
                                         languages like Python, the combination of mutability with
                                                                                                          future directions for this work (Section 4).
                                         aliasing has been the source of many bugs, warranting its
                                         own term (Aliasing Bug).
                                            Reasoning about aliasing is diﬃcult, as it usually requires
                                         a global analysis of the program and its possible traces of
                                         execution. To overcome this challenge, the community has         2 Related Work
                                         proposed type systems that track and restrict aliasing [7, 8].
                                                                                                          There are diﬀerent approaches for managing aliasing in pro-
                                         In this very large design space, there are lines of work more    gramming languages. One popular line of work focuses on
                                         focused on uniqueness, ownership and permissions. How-           ownership types [10], a type system that restricts access to
                                         ever, these proposals add complexity relative to ordinary
                                                                                                          objects according to their owners. There have been multiple
                                         type systems, and in some cases require developers to un-        proposals for ownership types with diﬀerent ﬂavors [9]. Un-
                                         derstand and reason about quite complex concepts. For ex-        fortunately, classic ownership types alone do not track alias-
                                         ample, ownership has been frequently mentioned as one of
                                                                                                          ing within ownership boundaries, making it diﬃcult for ver-
                                         ∗ Both authors contributed equally to this research.             iﬁcation tools to precisely track the eﬀect of assignments.
   Tracking uniqueness can provide strong guarantees about      Our approach is similar in spirit, but achieves greater sim-
aliasing, which is useful for veriﬁcation as well as safe man-  plicity by doing without ownership and ownership parame-
ual memory management, e.g. as implemented in Rust [21].        ters, while allowing more local alising within a method.
However, more powerful systems such as Rust’s (which is            Many early systems for uniqueness used destructive reads,
called “ownership,” though it provides uniqueness in the sense  but these often negatively impact program complexity by
described in the research literature) are known to be com-      reducing the ability to query information contained in ob-
plex and diﬃcult for developers to understand [11].             jects [5]. Therefore, alias burying [3] aims to deﬁne a unique-
   Uniqueness types [12] allow uniqueness properties to be      ness system for Java-like languages without using destruc-
speciﬁed as part of a data type. However, this approach is      tive reads by relying on the idea that aliases that will not
tailored to functional programming languages and requires       be used again can be buried. However, as noted by Boyland
a signiﬁcantly diﬀerent type system, thus its applicability to  and Retert [5], the analysis described in the initial work [3]
Java is limited.                                                exposes implementation details, such as the ﬁelds read by a
   Other type systems for uniqueness focus on the use cases     method, which breaks encapsulation and modularity.
of concurrency and message passing. For example, Haller            In summary, the prior work has one of three limitations:
and Odersky [16] use capabilities [4] to add uniqueness and     reliance on language or type system features not present in
borrowing to a Java-like languages with a focus on message      Java, modularity or coding pattern issues, or a larger and
passing in concurrent object-oriented programming. They         more complex set of abstractions for programmers to un-
use a concept of separate uniqueness, where distinct vari-      derstand compared to our goals. All of these design choices
ables do not share a common reachable object. Thus unique-      raise the adoption cost for developers. In our approach, Latte,
ness is used to enforce separation, which is desirable for con- we try to address these diﬃculties by creating a lightweight
current message-passing systems.                                uniqueness system with few annotations. Latte, which we
   More recently, Milano et al. [22] presented a new lan-       present in the following section, requires no changes to the
guage and type system for safe concurrency by statically        language semantics, and allows many common code pat-
ensuring that diﬀerent threads cannot access the same heap      terns while precisely tracking aliasing.
regions. Their proposal focused on reducing the annotation
burden and eliminating the need for unnatural rewrites re-
quired by more restrictive programming models. Also aim-        3 Approach
ing for a minimal set of annotations, LaCasa [15] adds unique-  As we described previously, our design aims to impose min-
ness to the Scala language using object capabilities. How-      imal restrictions while enforcing unique references (in the
ever, this approach requires classes to adhere to the object-   heap) and tracking aliasing (in the stack). While our system
capability discipline, and their empirical evaluation showed    is not as expressive as others in previous work, its main ad-
that most classes from the standard library do not follow       vantages are an easily-understood programming model and
these rules.                                                    low annotation complexity.
   There are other approaches that focus on modeling dif-          In particular, our design only requires annotations on ﬁelds
ferent aspects of aliasing. Reachability types [2] uses reach-  and parameters (with only two and three possible choices,
ability sets to reason about ownership, and tracks reachable    respectively). This burden can be further reduced by choos-
values using type qualiﬁers. This work layers uniqueness,       ing sensible defaults. Local variables do not need annota-
nested mutable state and other concepts over the tracking       tions, as the aliasing between local variables and ﬁeld val-
of reachability sets. Unique accesses are enabled by killing    ues is inferred, which reduces the barrier to adopting this
all other access paths to a reference.                          system.
   Castegren and Wrigstad [6] combined many of the previously-     In this section, we ﬁrst give a high-level description of
mentioned concepts in their 𝜅 language. This language uses      our approach, and then use an example to build intuition
reference capabilities to ensure separation, and combines       about our model. We then formally deﬁne the typing rules
techniques from ownership types, linear types [25], and re-     on top of a Featherweight Java [18]-inspired core language
gions [14] in a concurrent and parallel object-oriented set-    and explain how these rules result in the intended behavior.
ting.                                                           Finally, we demonstrate the expressive power of our system
   The systems described above were not implemented for         with a more complex example.
Java, however, and it is unclear how to do so, as they rely
on language features that Java does not have, such as capa-
bilities in Scala or a primitive swap operation.                3.1 Description
   AliasJava [1] does extend Java with type annotations in      First, we restrict our deﬁnition of uniqueness to only con-
Java that specify data sharing relationships. The type sys-     sider reachable values on the heap, thus unique values may
tem includes four annotations: unique, owned, lent and shared,  be stored in at most one reachable heap location, and aliased
and reduces the annotation burden by inferring annotations.     in the local environment. However, these dynamic aliases
Latte: Lightweight Aliasing Tracking for Java


[17] may only be used as long as such aliasing can be pre-            1 class Node {
cisely inferred. Our treatment of dynamic aliases and un-             2   unique Object value;
reachable heap locations is similar to that of alias burying          3   unique Node next;
[5].                                                                  4
   In Latte, the annotation unique is used to identify unique         5   Node(unique Object value, unique Node next)
values (as deﬁned above). owned identiﬁes borrowed values,            6   { this.value = value;
since it is only used on method parameters whose value                7     this.next = next; }
will be owned by some other context when entering the                 8 }
method body. shared identiﬁes values that may or may not              9
                                                                     10 class Stack {
be unique.
                                                                     11   unique Node root;
   We aim to use our analysis in an automated veriﬁer such
                                                                     12
as LiquidJava [13] to reason about mutation of unique (and           13   Stack(unique Node root)
borrowed) values. This requires precisely identifying all val-       14   { this.root = root; }
ues that may be aﬀected by a particular mutation. Our ap-            15
proach does this while permitting dynamic aliases, by in-            16   void push(owned Stack this,
ferring annotations of the form alias(𝑝) or ⊥ during type            17              unique Object value) {
checking. These special annotations are only inferred; they                    Δ = this : owned Stack, value : unique Object
are never written by the developer.                                  18     Node r; Node n;
   For each local variable 𝑥, our typing environment Δ con-                    Δ = · · · , r : ⊥ Node, n : ⊥ Node
tains a class 𝐶 and an annotation 𝛼 which describes the              19     r = this.root;
uniqueness of 𝑥 at that point. The formal deﬁnition of Δ                       Δ = · · · , r : alias( this.root ) Node
is given later in Figure 3.                                          20     this.root = null;
                                                                               Δ = · · · , r : unique Node
3.2 Example
                                                                     21     n = new Node(value, r);
    We illustrate the main features of our approach by imple-                  Δ = this : owned Stack, value : ⊥ Object,
menting push and pop operations for a stack storing unique
                                                                                   r : ⊥ Node, n : unique Node
values. References to objects pushed onto the stack may not
                                                                     22     this.root = n;
be stored on the heap anywhere else. This invariant could
be used by an automated veriﬁer to show that values pushed                     Δ = · · · , n : alias( this.root ) Node
onto the stack will not be mutated until they are returned           23   }
by pop. The code is shown in Figure 1.                               24
                                                                     25   unique Object pop(owned Stack this) {
    First, we demonstrate how the push method is validated.
                                                                     26     Object value;
At each step, we have listed (in Figure 1) the current typing
                                                                     27     if (this.root == null) {
context Δ to illustrate the veriﬁcation process.                     28        value = null;
    The typing environment at the beginning of the method            29     } else {
body contains the parameters and their types (line 17). Be-          30        value = this.root.value;
cause the two variables r and n are declared, but not yet ini-       31        Node next;
tialized at line 18, they are annotated with ⊥ to mark them          32        next = this.root.next;
inaccessible. r is aliased with this.root at line 19, and            33        this.root = next;
this aliasing information is added to the environment by an-         34     }
notating r with alias(this.root). Next, this.root is                 35     return value;
assigned, which isolates it in the typing environment (a pro-        36   }
                                                                     37 }
cess that we describe in §3.4.5). This invalidates all aliases to
it, which allows the previously-aliased variable r to become
unique and thus claim ownership.                                          Figure 1. Example: a stack for unique references
    Note that lines 19-20 are equivalent to a destructive read.
However, we do not need to change the language semantics
or introduce new language constructs. Also, the need for               Continuing with our example, we initialize a new Node
this destructive read is easily understood: we want to store        object at line 21. The constructor of Node has the signature
this.root in a diﬀerent place in the heap, thus we need             (unique Object, unique Node), which states that it con-
to remove its current value from the heap. Otherwise, our           sumes both arguments. This marks value and r as inac-
uniqueness invariant would be violated since the value at           cessible (⊥) in the calling context. We encapsulate construc-
this.root (which is declared unique) would be stored in             tor bodies, thus we do not know what value or r may be
multiple reachable places in the heap.                              aliased with after they are passed to the constructor. Since
                                                                  within the method body – the value is owned by some other
    𝑃 ::= 𝐶𝐿
                                                                  context.
  𝐶𝐿 ::= class 𝐶 extends 𝐶 { 𝐹 𝐾 𝑀 }
                                                                  3.4 Typing rules
  𝛼 𝑓 ::= unique | shared
                                                                  Our typing rules use a local type environment Δ. This envi-
   𝛼 𝑝 ::= unique | shared | owned
                                                                  ronment maps variables to an annotated class (𝛼 𝐶), where
    𝐹 ::= 𝛼 𝑓 𝐶 𝑓 ;                                               the annotation speciﬁes the current aliasing or uniqueness
   𝐾 ::= 𝐶 (𝛼 𝑓 𝐶 𝑔, 𝛼 𝑓 𝐶 𝑓 ){ super(𝑔);this.𝑓 = 𝑓 ; }           information. The form of Δ is given in Figure 3.
                                                                     A shared annotation denotes that the variable can be ac-
    𝜏 ::= 𝛼 𝑓 𝐶 | void
                                                                  cessed by outside objects – untracked aliases may exist. owned
   𝑀 ::= void 𝑚(𝛼 𝑝 𝐶 this, 𝛼 𝑝 𝐶 𝑥) { 𝑠 }                        denotes that the value of the variable is borrowed; speciﬁ-
                                                                  cally, its value is unique in the current context and no new
         | 𝛼 𝑓 𝐶 𝑚(𝛼 𝑝 𝐶 this, 𝛼 𝑝 𝐶 𝑥) { 𝑠 return 𝑒; }
                                                                  aliases may be added to the heap. unique denotes ownership
    𝑝 ::= 𝑥 | 𝑝.𝑓                                                 – the value is only stored at this location (modulo precisely-
    𝑒 ::= null | 𝑝                                                tracked dynamic aliases). A local variable annotated unique
    𝑠 ::= 𝐶 𝑥; | 𝑥 = 𝑒; | 𝑥 .𝑓 = 𝑒;                               may be converted to a shared, based on its usage. ⊥ denotes
                                                                  that the value is inaccessible.
         | 𝑥 = new 𝐶 (𝑒); | 𝑥 = 𝑥 .𝑚(𝑒); | 𝑥 .𝑚(𝑒);
         | if (𝑒 == 𝑒) 𝑠 else 𝑠 | { 𝑠 }
                                                                         𝛼𝑒 ::= owned | shared | unique | unique(𝑝.𝑓 )
                                                                          𝛼 ::= owned | shared | unique | alias(𝑝) | ⊥
  Figure 2. Grammar extended from Featherweight Java
                                                                          Δ ::= · | 𝑥 : 𝛼 𝐶, Δ


we cannot track this aliasing, any usage of these values is       Figure 3. Typing environment and annotations used in typ-
disallowed after they are passed to the constructor.              ing rules
   Finally, we assign n to this.root at line 22. Since our
typing context only stores annotations for local variables,
and not for ﬁelds, we update the annotation for the local         3.4.1 Aliasing. Aliasing between variables and ﬁelds is
variable n, which is on the RHS of the assignment. The an-        tracked by entries of the form 𝑥 : alias(𝑝) in Δ. This de-
notation alias(this.root) simply denotes that its target          notes that the 𝑥 stores the same value as the path (a vari-
this.root contains the same value as the annotated vari-          able or some ﬁeld access) 𝑝. Two paths are aliased iﬀ they
able n, thus it does not matter which side of an alias is an-     reference the same object, thus aliasing is an equivalence re-
notated. After this line, Δ indicates that n is aliased with      lation. This is encoded by the judgment Δ ⊢ 𝑝 1 ≡ 𝑝 2 , which
this.root, thus we have precisely determined all local            denotes that Δ indicates that the path 𝑝 1 is aliased with 𝑝 2 .
aliases to the unique value this.root, and ensured that           Formal rules are given in Appendix A.4.
this.root is stored at only one location on the heap.                Given an environment Δ, we deﬁne its alias graph to be
   This ﬁrst method gives an overview of our approach; the        a (undirected) graph whose nodes are syntactic paths (𝑝 as
second method (pop, at line 32) will be presented in Sec-         deﬁned in Figure 2), and distinct paths 𝑝 1 and 𝑝 2 are con-
tion 3.4.7 after the grammar and typing rules are introduced.     nected iﬀ Δ ⊢ 𝑝 1 ≡ 𝑝 2 . Each component of this graph may
                                                                  contain at most one path annotated with owned, unique, or
3.3 Grammar                                                       shared.
                                                                     Intuitively, the alias graphs for each program point (which
For our grammar, presented in Figure 2, we extended Feath-
                                                                  identify allowable aliasing), along with validation of unique-
erweight Java [18] with statements, including ﬁeld and vari-
                                                                  ness invariants (which ensures that no other aliases of unique
able assignments as in Java, to better approximate the Java
                                                                  values exists), is the primary product of our analysis. This
language in terms of mutability (a key concern in this pa-
                                                                  output can then be used to automatically verify the eﬀects
per). To model our particular system, we added the unique,
                                                                  of mutation or, more generally, separation invariants.
shared, and owned annotations. All ﬁelds (𝐹 ) must be anno-
tated with either unique or shared (𝛼 𝑓 ), while method pa-       3.4.2 Side note: concurrency. Since we are tracking aliases
rameters (in 𝑀) must be annotated with one of the three           across multiple statements, and our alias annotations may
annotations (𝛼 𝑝 ). Note that variable declarations are not an-   point to mutable heap locations, it may seem challenging
notated (ﬁrst production of 𝑠).                                   to handle concurrency. However, we only claim to precisely
   Our owned annotation is often called lent or borrowed          track aliases of unique or borrowed values, i.e. expressions
in other systems. Our choice reﬂects the state of the value       for which Δ ⊢ 𝑒 : owned 𝐶 ⊣ Δ′ holds for some 𝐶 and Δ′ .
Latte: Lightweight Aliasing Tracking for Java


Intuitively, if this holds for a variable 𝑥, and 𝑥 is aliased to        E-Owned                        E-Shared
𝑦.𝑓 , then 𝑦.𝑓 is also unique, which requires 𝑦 to be unique.              Δ(𝑥) = owned 𝐶                Δ(𝑥) = shared 𝐶
In other words, either the current context or some calling               Δ ⊢ 𝑥 : owned 𝐶 ⊣ Δ           Δ ⊢ 𝑥 : shared 𝐶 ⊣ Δ
context is the sole owner of 𝑦, and thus of the heap location
𝑦.𝑓 . (This reasoning may be extended for 𝑦.𝑓 .𝑔, etc.) There-          E-UniqeOwned                   E-UniqeShared
fore we can determine all mutations that would aﬀect this                 Δ(𝑥) = unique 𝐶               Δ(𝑥) = unique 𝐶
alias relation. In other words, assuming soundness of our ap-            Δ ⊢ 𝑥 : owned 𝐶 ⊣ Δ           Δ ⊢ 𝑥 : shared 𝐶 ⊣
proach for sequential programs, it should remain sound for                                                Δ[𝑥 ↦→ shared 𝐶]
concurrent programs, as long as unique values accessible to
the spawned thread are consumed after a fork operation.               E-UniqeUniqe                  E-UniqeAlias
                                                                        Δ(𝑥) = unique 𝐶                  Δ(𝑥) = unique 𝐶
3.4.3 Reachable aliasing. Δ ⊢ 𝑝 1 ≅ 𝑝 2 denotes that a                Δ ⊢ 𝑥 : unique 𝐶 ⊣            Δ ⊢ 𝑥 : unique(𝑝.𝑓 ) 𝐶 ⊣
value reachable from 𝑝 1 (for example, 𝑝 1 .𝑓 ) may be aliased                 Δ[𝑥 ↦→ ⊥ 𝐶]               Δ[𝑥 ↦→ alias(𝑝.𝑓 ) 𝐶]
with a value reachable from 𝑝 2 (for example, 𝑝 2 .𝑓 .𝑔). Formal
rules are given in appendix A.5. If Δ 0 𝑝 1 ≅ 𝑝 2 then 𝑝 1 and          E-Alias                  E-FieldOwned
𝑝 2 are separately unique, as deﬁned in [16].                           Δ(𝑥) = alias(𝑝) 𝐶            Δ ⊢ 𝑝 : owned 𝐶 ⊣ Δ
                                                                        Δ ⊢ 𝑝 : 𝛼 𝑒 𝐶 ⊣ Δ′        ftype(𝐶) (𝑓 ) = unique 𝐶 ′
3.4.4 Expression typing. Δ ⊢ 𝑒 : 𝛼𝑒 𝐶 ⊣ Δ′ denotes that                 Δ ⊢ 𝑥 : 𝛼 𝑒 𝐶 ⊣ Δ′           Δ ⊢ 𝑝.𝑓 : owned 𝐶 ′ ⊣ Δ
𝑒 may be used as a value with class 𝐶 and ownership anno-
tation 𝛼𝑒 , provided that all future typing uses the Δ′ typing          E-FieldShared                      E-Sub
environment. Formal rules are given in Figure 4.                               Δ ⊢𝑝 :𝐶                     Δ ⊢ 𝑒 : 𝛼 𝑒 𝐶 ⊣ Δ′
    Δ ⊢ 𝑒 : unique(𝑝.𝑓 ) ⊣ Δ′ denotes that 𝑒 refers to a unique         ftype(𝐶) (𝑓 ) = shared 𝐶 ′              𝐶 <: 𝐷
value (as deﬁned in §3.1), and 𝑒 is aliased with 𝑝.𝑓 in Δ′ .             Δ ⊢ 𝑝.𝑓 : shared 𝐶 ′ ⊣ Δ          Δ ⊢ 𝑒 : 𝛼 𝑒 𝐷 ⊣ Δ′
This is used to validate assignments to unique ﬁelds, since
the assignee is a ﬁeld whose annotation is not stored in Δ.                            E-Null
Thus aliasing information is tracked by annotating the as-
signment value, instead of annotating the assignee.                                     Δ ⊢ null : 𝛼𝑒 𝐶 ⊣ Δ
    For a variable 𝑥 annotated with alias(𝑝), Δ ⊢ 𝑥 : 𝛼𝑒 𝐶 ⊣ Δ′
holds if and only if Δ ⊢ 𝑝 : 𝛼𝑒 𝐶 ⊣ Δ′ – in other words,                     Figure 4. Expression usage typing rules
aliased variables may be used exactly how the path they
alias may be used.
    When borrowing a unique ﬁeld value (i.e. passing the           An edge 𝑥 → 𝑝 exists iﬀ Δ contains an annotation 𝑥 :
value to a parameter annotated as owned), the object refer-        alias(𝑝. · · · ).
ence must also be unique. For example, if we have variables            Intuitively, the origin of an edge in the alias graph iden-
𝑥 : shared 𝐶 and 𝑦 : shared 𝐶, and 𝐶 contains a unique ﬁeld        tiﬁes a variable whose annotation requires updating when
𝑓 , we cannot borrow 𝑥 .𝑓 because we do not know whether           its target is mutated. Unlike the alias graph deﬁned in §3.4.1,
the same heap location is already borrowed through 𝑦.𝑓 .           this graph is not symmetric or transitive.
Thus one can introduce aliases to a unique ﬁeld of a shared            For example, in the pop method, after line 30 we have the
value, but those values can only be used after a destructive       annotation value : alias(this.root.value). Thus the
read or some equivalent operation.                                 reference graph contains the edge value → this.root.
    Finally, a value of a subtype 𝐶 may be used as a value of      If the value of this.root is changed, we must determine
the supertype type 𝐷 with the same annotation.                     a new annotation for value.
                                                                       Formal rules are given in appendix A.7. The rules deal
3.4.5 Isolation. Δ ∗ 𝑝 ⊣ Δ′ denotes that 𝑝 is isolated from        with three main cases:
Δ′ – all references to 𝑝 contained in Δ are removed in Δ′ .           1. No node in either the reference graph or the alias
Δ′ represents a state where 𝑝 is assigned a new value, thus              graph 𝑝 is connected to 𝑝. Δ is unchanged, except to
all aliases to 𝑝 in Δ should be removed in Δ′ . Moreover, if             remove 𝑝 from dom(Δ). (See the I-Remove* rules.)
𝑝 represented a unique value and a variable 𝑥 was aliased                This case is applied during validation of line 30 in Fig-
to 𝑝, 𝑥 contains a unique value after 𝑝 is overwritten. Thus             ure 1 to remove the initial annotation value : ⊥.
destructive reads are accomplished by ﬁrst introducing an             2. For some variable 𝑥 (distinct from 𝑝), 𝑥 is aliased with
alias to 𝑝, and then overwriting 𝑝 with a diﬀerent value, such           𝑝. In this case, all paths rooted in 𝑝 may be replaced
as null.                                                                 by paths rooted in 𝑥. (See the I-Replace* rules.)
   Given an environment Δ, we deﬁne its reference graph               3. 𝑝 is disconnected in the alias graph, but 𝑝 is the target
to be a (directed) graph whose nodes are syntactic paths.                of an edge in the reference graph. In this case, we can
      isolate the subﬁeld that induces this edge (such as 𝑝.𝑓 )                S-AssignVar
      before isolating 𝑝. (See the I-Elim* rules.)                                            Δ(𝑥) = 𝛼 𝐶
      This case is applied during validation of line 33 in Fig-                Δ⊢𝑒 :𝐶         Δ0𝑥 ≡𝑒            Δ ∗ 𝑥 ⊣ Δ′
      ure 1 when isolating this.root. The annotation of                             Δ ⊢ 𝑥 = 𝑒; ⊣ 𝑥 : alias(𝑒) 𝐶, Δ′
      value is updated from alias(this.root.value)
      to unique.                                                      S-Call
                                                                           𝛼 0 𝐶 0 , · · · , 𝛼𝑛 𝐶𝑛 → 𝛼 𝐶 = mtype(𝐶 0 ) (𝑚)
3.4.6 Framing. When a reference is passed to a method,                Δ ⊢ 𝑒 0 : 𝛼 0 𝐶 0 , · · · , 𝑒𝑛 : 𝛼 𝑛 𝐶𝑛 ⊣ Δ ′  Δ′ (𝑥) = 𝛼 ′ 𝐵
any ﬁeld of the referenced object can be modiﬁed. The frame            𝐵 <: 𝐶             ′
                                                                                        Δ ★ 𝑒0 , · · · , 𝑒𝑛 ⊣ Δ ′′
                                                                                                                    Δ′′ ∗ 𝑥 ⊣ Δ′′′
of a method call contains all such ﬁelds. Any aliases to ﬁelds                                                                   
                                                                       ∀0 ≤ 𝑖 < 𝑗 ≤ 𝑛 : 𝛼𝑖 = owned =⇒ Δ′ 0 𝑒𝑖 ≅ 𝑒 𝑗
in the method’s frame must be invalidated after the method
call.                                                                       Δ ⊢ 𝑥 = 𝑒 0 .𝑚(𝑒 1 , · · · , 𝑒𝑛 ); ⊣ 𝑥 : 𝛼 𝐵, Δ′′′
   Δ ★ 𝑒 ⊣ Δ′ denotes that all variables that are connected
                                                                         S-AssignUniqe
(in the reference graph of Δ) to any path in the list 𝑒 are
                                                                                              Δ ⊢𝑥 :𝐶
marked in Δ′ as either shared, in cases where alias tracking              Δ ∗ 𝑥 .𝑓 ⊣ Δ′        ftype(𝐶) (𝑓 ) = unique 𝐶 ′
is unnecessary, or ⊥, in cases where aliases must be tracked.
                                                                         Δ 0 𝑥 .𝑓 ≅ 𝑒        Δ ⊢ 𝑒 : unique(𝑥 .𝑓 ) 𝐶 ′ ⊣ Δ′′
                                                                                              ′
Formal rules are given in appendix A.8.
                                                                                          Δ ⊢ 𝑥 .𝑓 = 𝑒; ⊣ Δ′′
3.4.7 Statement typing. Statements are typed by the judg-
ment Δ ⊢ 𝑠 ⊣ Δ′ . Selected rules are shown in Figure 5. See             S-Conditional
appendix A.10 for a complete listing.                                          Δ ⊢ 𝑒 1 : Object         Δ ⊢ 𝑒 2 : Object
   An assignment such as 𝑥 = 𝑝 adds an edge 𝑥 → 𝑝 to                                  Δ ⊢ 𝑠 1 ⊣ Δ1      Δ ⊢ 𝑠 2 ⊣ Δ2
the alias graph. Note that as a special case, 𝑥 = null adds             Δ ⊢ if (𝑒 1 == 𝑒 2 ) 𝑠 1 else 𝑠 2 ⊣ unify(Δ; Δ1 ; Δ2 )
the annotation 𝑥 : unique (see deﬁnition of alias in Appen-
dix A.3).
                                                                                  Figure 5. Statement typing rules
   When 𝑓 is a unique ﬁeld and 𝑒 is a path, 𝑥 .𝑓 = 𝑒 adds
an edge 𝑒 → 𝑥 .𝑓 to the alias graph by using the annota-
tion unique(𝑥 .𝑓 ) when validating 𝑒. Note that 𝑥 .𝑓 is iso-
lated before typing 𝑒, which allows patterns such as lines        with shared. If a variable is not referenced in starting Δ, the
32-33 in Figure 1, where this.root is updated to point to         variable may be isolated from Δ1 and Δ2 . This removes all
this.root.next without a destructive read. Since the              aliasing to variables deﬁned within a particular branch.
ﬁeld this.root is unique, the variable aliased to this               If 𝑥 is annotated alias(𝑝 1 ) in Δ1 and alias(𝑝 2 ) in Δ2 , and
.root.next may overwrite this.root without violat-                there is a path 𝑝 where Δ1 ⊢ 𝑝 1 ≡ 𝑝 and Δ2 ⊢ 𝑝 2 ≡ 𝑝, then 𝑥
ing uniqueness.                                                   may be annotated with alias(𝑝) after uniﬁcation. Otherwise,
   Method calls are validated by validating each argument         if none of these cases apply, the variable is annotated with
according to the corresponding parameter deﬁnition. Note          ⊥, thus making its value inaccessible.
that after typing an argument as unique, all paths rooted            Uniﬁcation occurs in the pop method in Figure 1 prior to
in the argument are inaccessible. Therefore reachable alias-      the return statement. In the ﬁrst branch, value is unique
ing cannot exist between parameters annotated with unique.        since it is null. In the second branch, value is ﬁrst aliased
However, aliasing is not prohibited simply by typing argu-        with this.root.value, but then becomes unique after
ments passed to parameters annotated owned, since bor-            line 33. Thus value is unique in both branches, and we
rowed values are not consumed. Therefore we explicitly pro-       can use value in the return statement, which requires a
hibit reachable aliasing between owned parameters. We also        unique value.
invalidate aliases to ﬁelds in the frame of the method call, as      Note that more speciﬁc uniﬁcation procedures could be
discussed in §3.4.6.                                              developed. For example, we could implement conditional
                                                                  aliasing annotations, or validate every possible execution
3.4.8 Uniﬁcation. When an if statement is validated, each         path independently (and thus eliminate uniﬁcation entirely).
branch must be validated, which produces two separate typ-        However, we feel that this conservative uniﬁcation algorithm
ing environments, Δ1 and Δ2 . These environments are uni-         is more usable since it allows clear error messages when at-
ﬁed by ﬁnding an annotation that can be used in both en-          tempting to access variables that are inaccessible due to uni-
vironments for each variable in the outer environment Δ.          ﬁcation.
Formal rules are given in appendix A.9.
   If some variable 𝑥 has the same annotation in both branches,   3.4.9 Program typing. A valid program is deﬁned in ap-
then this common annotation may be used. If 𝑥 refers to a         pendix A.11, along with rules for typing method and class
shared value in both Δ1 and Δ2 , then it may be annotated         declarations.
Latte: Lightweight Aliasing Tracking for Java



  1 unique Object dequeue(owned Stack this) {
                                                                  system and evaluate it in larger examples with users. A com-
  2   Node r = this.root;                                         parison of the eﬀort in diﬀerent examples with the alter-
  3   Object value;                                               natives in the related work would also be interesting, to
  4   if (r == null || r.next == null) {                          conﬁrm whether our invariant helps developers to annotate
  5     value = this.pop();                                       their code. Additionally, our current approach includes only
  6   } else {                                                    a core set of Java features that we would like to extend to
  7     value = dequeueHelper(r);                                 include while loops.
  8   }                                                              One of the motivations of this work was to introduce
  9   return value;                                               enough information to reason about mutability to support
 10 }
                                                                  Liquid Types in a mutable context. Flux [20] took the ﬁrst
 11
                                                                  steps in this area, by using Rust’s ownership type in combi-
 12 unique Object dequeueHelper(owned Stack this,
 13                              owned Node n) {
                                                                  nation with a Liquid Type System. Our proposal targets the
 14   Object value;                                               Java language instead, and serves as the basis to extend Liq-
 15   if (n.next.next == null) {                                  uidJava [13] to better model aliasing and uniqueness com-
 16     value = n.next.value;                                     bined with reﬁnements. Because Liquid Types supports a
 17     n.next = null;                                            logic-based version of symbolic execution, the information
 18   } else {                                                    from reﬁnements could be used in the uniﬁcation to have a
 19     value = dequeueHelper(n.next);                            more precise alias tracking, instead of the conservative in-
 20   }                                                           validation we took instead.
 21   return value;
 22 }
                                                                  5 Conclusion
                                                                  We have described Latte, a simple type system for unique-
Figure 6. Example: a dequeue method for the Stack                 ness and aliasing for Java, which prioritizes usability and
class from Figure 1                                               low development overhead. Our vision is that more complex
                                                                  type systems may utilize the uniqueness and aliasing infor-
3.5   Extended example                                            mation determined by Latte. Latte enforces (and requires
The dequeue method in Figure 6 allows the stack to be             consideration of) simple invariants of values on the heap,
used as a FIFO queue. The recursive traversal of the linked       imposes a low annotation burden, and requires no changes
list is handled by the dequeueHelper method. Note that            to existing Java semantics.
the entire list is traversed, and the tail modiﬁed, using only       Our simple uniqueness invariant indicates that a unique
a single destructive read.                                        object is stored at most once on the heap. In addition, all
   This is enabled by borrowing the unique value this.root,       usable references to a unique object from the local environ-
and in turn each next node. The value of an owned param-          ment are precisely inferred. The developer only needs to
eter is guaranteed to be unique, but its value may not be         annotate ﬁeld declarations and the parameters and return
consumed or placed on the heap. Thus dequeueHelper                types of method declarations, using one of unique, owned
guarantees that no additional aliases to n will be introduced.    or shared.
However, the contents of an owned value may be modiﬁed,              While it may lack the expressive power of related approaches,
which allows the tail Node to be removed.                         we hope that Latte provides a lower barrier to entry for ex-
   Also note that the unique value n.next.value is read           isting Java developers, thus enhancing the appeal of auto-
without an explicit destructive read at line 16. Instead, it is   mated veriﬁcation tools built on Latte. Further evaluation
known to be unique since its container (n.next) is isolated       of its usability, along with the development of such veriﬁca-
at line 17.                                                       tion tools, is required to validate this goal.
   In a survey of related work, Milano et al. [22] found that
ownership systems often require explicit destructive reads        6 Acknowledgments
at each step when traversing and modifying a linked list          This work was supported by the National Science Founda-
as in this example. However, our isolation technique, com-        tion under Grant No. CCF-1901033 and by the Algorand
bined with local aliased values and borrowing, eliminates         Centres of Excellence programme managed by Algorand Foun-
this requirement while allowing common code patterns and          dation. The work is also co-ﬁnanced by a Dual Degree Ph.D.
requiring few annotations.                                        Scholarships awarded by the Portuguese Foundation for Sci-
                                                                  ence and Technology through the Carnegie Mellon Portugal
4     Future Work                                                 Program, through the RAP project (EXPL/CCI-COM/1306/2021)
While the design decisions were guided by making this sys-        and through the LASIGE unit (UIDB/00408/2020 and UIDP/00408/2020).
tem usable by developers, we would need to implement the          Any opinions, ﬁndings, and conclusions or recommendations
expressed in this material are those of the author(s) and do                          2007, Freiburg, Germany, September 27-29, 2007. Revised Selected
not necessarily reﬂect the views of the NSF or the Algorand                           Papers (Lecture Notes in Computer Science, Vol. 5083), Olaf Chi-
Foundation.                                                                           til, Zoltán Horváth, and Viktória Zsók (Eds.). Springer, 201–218.
                                                                                      https://doi.org/10.1007/978-3-540-85373-2_12
                                                                                 [13] Catarina Gamboa, Paulo Canelas, Christopher Timperley, and Alcides
References                                                                            Fonseca. 2023. Usability-Oriented Design of Liquid Types for Java. In
                                                                                      2023 IEEE/ACM 45th International Conference on Software Engineering
 [1] Jonathan Aldrich, Valentin Kostadinov, and Craig Chambers. 2002.                 (ICSE). 1520–1532. https://doi.org/10.1109/ICSE48619.2023.00132
     Alias annotations for program understanding. In Proceedings of the          [14] Aaron Greenhouse and John Boyland. 1999. An Object-Oriented Ef-
     2002 ACM SIGPLAN Conference on Object-Oriented Programming Sys-                  fects System. In ECOOP’99 - Object-Oriented Programming, 13th Euro-
     tems, Languages and Applications, OOPSLA 2002, Seattle, Washington,              pean Conference, Lisbon, Portugal, June 14-18, 1999, Proceedings (Lec-
     USA, November 4-8, 2002, Mamdouh Ibrahim and Satoshi Matsuoka                    ture Notes in Computer Science, Vol. 1628), Rachid Guerraoui (Ed.).
     (Eds.). ACM, 311–330. https://doi.org/10.1145/582419.582448                      Springer, 205–229. https://doi.org/10.1007/3-540-48743-3_10
 [2] Yuyan Bao, Guannan Wei, Oliver Bracevac, Yuxuan Jiang, Qiyang He,           [15] Philipp Haller and Alexander Loiko. 2016. LaCasa: lightweight
     and Tiark Rompf. 2021. Reachability types: tracking aliasing and sepa-           aﬃnity and object capabilities in Scala. In Proceedings of the 2016
     ration in higher-order functional programs. Proc. ACM Program. Lang.             ACM SIGPLAN International Conference on Object-Oriented Program-
     5, OOPSLA (2021), 1–32. https://doi.org/10.1145/3485516                          ming, Systems, Languages, and Applications, OOPSLA 2016, part of
 [3] John Boyland. 2001.           Alias burying: Unique variables with-              SPLASH 2016, Amsterdam, The Netherlands, October 30 - November
     out destructive reads. Softw. Pract. Exp. 31, 6 (2001), 533–553.                 4, 2016, Eelco Visser and Yannis Smaragdakis (Eds.). ACM, 272–291.
     https://doi.org/10.1002/spe.370                                                  https://doi.org/10.1145/2983990.2984042
 [4] John Boyland, James Noble, and William Retert. 2001. Capabilities for       [16] Philipp Haller and Martin Odersky. 2010. Capabilities for Unique-
     Sharing: A Generalisation of Uniqueness and Read-Only. In ECOOP                  ness and Borrowing. In ECOOP 2010 - Object-Oriented Programming,
     2001 - Object-Oriented Programming, 15th European Conference, Bu-
                                                                                      24th European Conference, Maribor, Slovenia, June 21-25, 2010. Proceed-
     dapest, Hungary, June 18-22, 2001, Proceedings (Lecture Notes in Com-
                                                                                      ings (Lecture Notes in Computer Science, Vol. 6183), Theo D’Hondt (Ed.).
     puter Science, Vol. 2072), Jørgen Lindskov Knudsen (Ed.). Springer, 2–
                                                                                      Springer, 354–378. https://doi.org/10.1007/978-3-642-14107-2_17
     27. https://doi.org/10.1007/3-540-45337-7_2
                                                                                 [17] John Hogg. 1991. Islands: Aliasing Protection in Object-Oriented
 [5] John Tang Boyland and William Retert. 2005. Connecting ef-
                                                                                      Languages. In Proceedings of the Sixth Annual Conference on Object-
     fects and uniqueness with adoption. In Proceedings of the 32nd
                                                                                      Oriented Programming Systems, Languages, and Applications, OOPSLA
     ACM SIGPLAN-SIGACT Symposium on Principles of Programming
                                                                                      1991, Phoenix, Arizona, USA, October 6-11, 1991, Andreas Paepcke (Ed.).
     Languages, POPL 2005, Long Beach, California, USA, January 12-
                                                                                      ACM, 271–285. https://doi.org/10.1145/117954.117975
     14, 2005, Jens Palsberg and Martín Abadi (Eds.). ACM, 283–295.
                                                                                 [18] Atsushi Igarashi, Benjamin C. Pierce, and Philip Wadler. 2001.
     https://doi.org/10.1145/1040305.1040329
                                                                                      Featherweight Java: a minimal core calculus for Java and
 [6] Elias Castegren and Tobias Wrigstad. 2016. Reference Capabilities                GJ.     ACM Trans. Program. Lang. Syst. 23, 3 (2001), 396–450.
     for Concurrency Control. In 30th European Conference on Object-                  https://doi.org/10.1145/503502.503505
     Oriented Programming, ECOOP 2016, July 18-22, 2016, Rome, Italy             [19] Steve Klabnik and Carol Nichols. 2023. What Is Ownership?
     (LIPIcs, Vol. 56), Shriram Krishnamurthi and Benjamin S. Lerner                  https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html
     (Eds.). Schloss Dagstuhl - Leibniz-Zentrum für Informatik, 5:1–5:26.        [20] Nicolás Lehmann, Adam T. Geller, Niki Vazou, and Ranjit Jhala. 2022.
     https://doi.org/10.4230/LIPIcs.ECOOP.2016.5                                      Flux: Liquid Types for Rust. Proceedings of the ACM on Programming
 [7] Dave Clarke, James Noble, and Tobias Wrigstad (Eds.). 2013. Alias-               Languages 7 (2022), 1533 – 1557.
     ing in Object-Oriented Programming. Types, Analysis and Veriﬁca-            [21] Nicholas D. Matsakis and Felix S. Klock. 2014. The Rust Language. In
     tion. Lecture Notes in Computer Science, Vol. 7850. Springer.                    Proceedings of the 2014 ACM SIGAda Annual Conference on High In-
     https://doi.org/10.1007/978-3-642-36946-9                                        tegrity Language Technology (Portland, Oregon, USA) (HILT ’14). As-
 [8] Dave Clarke, James Noble, and Tobias Wrigstad. 2013.                 Be-         sociation for Computing Machinery, New York, NY, USA, 103–104.
     yond the Geneva Convention on the Treatment of Object Alias-                     https://doi.org/10.1145/2663171.2663188
     ing. In Aliasing in Object-Oriented Programming. Types, Analysis            [22] Mae Milano, Joshua Turcotti, and Andrew C. Myers. 2022. A ﬂexible
     and Veriﬁcation, Dave Clarke, James Noble, and Tobias Wrigstad                   type system for fearless concurrency. In PLDI ’22: 43rd ACM SIGPLAN
     (Eds.). Lecture Notes in Computer Science, Vol. 7850. Springer, 1–6.             International Conference on Programming Language Design and Imple-
     https://doi.org/10.1007/978-3-642-36946-9_1                                      mentation, San Diego, CA, USA, June 13 - 17, 2022, Ranjit Jhala and Isil
 [9] Dave Clarke and Tobias Wrigstad. 2003. External Uniqueness Is                    Dillig (Eds.). ACM, 458–473. https://doi.org/10.1145/3519939.3523443
     Unique Enough. In ECOOP 2003 - Object-Oriented Programming, 17th            [23] Nicholas Rempel. 2023. Understanding rust’s ownership model.
     European Conference, Darmstadt, Germany, July 21-25, 2003, Proceed-              https://www.learnrust.blog/p/understanding-rusts-ownership-model#:~:text=In%20R
     ings (Lecture Notes in Computer Science, Vol. 2743), Luca Cardelli (Ed.).   [24] Patrick Maxim Rondon, Ming Kawaguchi, and Ranjit Jhala. 2008. Liq-
     Springer, 176–200. https://doi.org/10.1007/978-3-540-45070-2_9                   uid types. In Proceedings of the ACM SIGPLAN 2008 Conference on
[10] David G. Clarke, John Potter, and James Noble. 1998. Ownership                   Programming Language Design and Implementation, Tucson, AZ, USA,
     Types for Flexible Alias Protection. In Proceedings of the 1998 ACM              June 7-13, 2008, Rajiv Gupta and Saman P. Amarasinghe (Eds.). ACM,
     SIGPLAN Conference on Object-Oriented Programming Systems, Lan-                  159–169. https://doi.org/10.1145/1375581.1375602
     guages & Applications, OOPSLA 1998, Vancouver, British Columbia,            [25] Philip Wadler. 1990. Linear Types can Change the World!. In Program-
     Canada, October 18-22, 1998, Bjørn N. Freeman-Benson and Craig                   ming concepts and methods: Proceedings of the IFIP Working Group 2.2,
     Chambers (Eds.). ACM, 48–64. https://doi.org/10.1145/286936.286947               2.3 Working Conference on Programming Concepts and Methods, Sea of
[11] Will Crichton. 2020.          The Usability of Ownership.           HA-          Galilee, Israel, 2-5 April, 1990, Manfred Broy and Cliﬀ B. Jones (Eds.).
     TRA 2020 abs/2011.06171 (2020).                       arXiv:2011.06171           North-Holland, 561.
     https://arxiv.org/abs/2011.06171
[12] Edsko de Vries, Rinus Plasmeijer, and David M. Abrahamson.
     2007. Uniqueness Typing Simpliﬁed. In Implementation and Ap-
     plication of Functional Languages, 19th International Workshop, IFL
Latte: Lightweight Aliasing Tracking for Java


A Typing rules                                                        A.4     Aliasing
A.1 Reference typing                                                  Δ ⊢ 𝑝 ≡ 𝑝 ′ denotes that a path 𝑝 refers to the same value as
Δ ⊢ 𝑝 : 𝐶 denotes that the path 𝑝 is accessible and contains          𝑝 ′.
either null or an reference to an instance of class 𝐶.
                                                                                              A-Var                               A-Cong
                                                                       A-Refl                 Δ(𝑥) = alias(𝑝) 𝐶                      Δ ⊢ 𝑝1 ≡ 𝑝2
                                        T-Field
         T-Var                               Δ⊢𝑝 :𝐶                     Δ⊢𝑝 ≡𝑝                     Δ⊢𝑥 ≡𝑝                         Δ ⊢ 𝑝 1 .𝑓 ≡ 𝑝 2 .𝑓
                 𝛼≠⊥                    ftype(𝐶) (𝑓 ) = 𝛼 𝐶 ′
                                                                             A-Symm                         A-Trans
         Δ, 𝑥 : 𝛼 𝐶 ⊢ 𝑥 : 𝐶                     Δ ⊢ 𝑝.𝑓 : 𝐶 ′                 Δ ⊢ 𝑝1 ≡ 𝑝2                   Δ ⊢ 𝑝1 ≡ 𝑝2            Δ ⊢ 𝑝2 ≡ 𝑝3
                                                                              Δ ⊢ 𝑝2 ≡ 𝑝1                               Δ ⊢ 𝑝1 ≡ 𝑝3
A.2    Subtyping
𝐶 <: 𝐷 denotes that 𝐶 extends a parent class 𝐷. It is a reﬂex-        A.5 Reachable aliasing
ive and transitive relation.                                          Δ ⊢ 𝑝 ≅ 𝑝 ′ denotes that a value reachable from 𝑝 may be
                                                                      aliased with a value reachable from 𝑝 ′ , given the aliasing
                                    C-Transitive                      speciﬁed in Δ.
             C-Id                   𝐶 <: 𝐷          𝐷 <: 𝐸
                                                                                        RA-Symm                    RA-Trans
              𝐶 <: 𝐶                       𝐶 <: 𝐸                     RA-Refl           Δ ⊢ 𝑝1 ≅ 𝑝2                 Δ ⊢ 𝑝1 ≅ 𝑝2          Δ ⊢ 𝑝2 ≅ 𝑝3
                 C-Def                                                Δ⊢𝑝 ≅𝑝            Δ ⊢ 𝑝2 ≅ 𝑝1                             Δ ⊢ 𝑝1 ≅ 𝑝3
                 class 𝐶 extends 𝐷 { 𝐹 𝐾 𝑀 }
                                                                                 RA-Field                            RA-Var
                                 𝐶 <: 𝐷
                                                                                   Δ ⊢ 𝑝1 ≅ 𝑝2                        Δ(𝑥) = alias(𝑝) 𝐶
A.3    Auxiliary functions                                                       Δ ⊢ 𝑝 1 .𝑓 ≅ 𝑝 2                              Δ⊢𝑥 ≅𝑝
fields(𝐶) denotes the list of ﬁeld declarations in 𝐶. ftype(𝐶) (𝑓 )   A.6 Replacement
denotes the annotation and class speciﬁed in the declaration
                                                                      𝑝 [𝑝 ′′ /𝑝 ′ ] denotes the path 𝑝 with the path 𝑝 ′ replaced by
of ﬁeld 𝑓 in class 𝐶. mtype(𝐶) (𝑚) denotes the signature of
                                                                      𝑝 ′′ . For example, 𝑥 .𝑓 [𝑦.𝑔/𝑥] = 𝑦.𝑔.𝑓 .
method 𝑚 in class 𝐶. alias(𝑒) is a helper function which de-
notes the annotation alias(𝑒) when 𝑒 is a path, and unique                                              (
when 𝑒 is null.                                                                                             𝑝 ′′   if 𝑥 = 𝑝 ′
                                                                                    𝑥 [𝑝 ′′ /𝑝 ′ ] :=
                                                                                                            𝑥      otherwise
                         F-Obj
                                                                                                        (
                                                                                         ′′    ′            𝑝 ′′                if 𝑝.𝑓 = 𝑝 ′
                                                                                  𝑝.𝑓 [𝑝 /𝑝 ] :=
                         fields(Object) = ·                                                                 𝑝 [𝑝 ′′ /𝑝 ′ ].𝑓    otherwise

             F-Decl                                                       Δ[𝑝 ′′ /𝑝 ′ ] denotes the environment Δ with all aliases that
               class 𝐶 extends 𝐷 { 𝐹 𝐾 𝑀 }                            reference the path 𝑝 ′ updated to instead reference the path
                                                                      𝑝 ′′ .
              𝐹 = 𝛼𝑓 𝐶 𝑓 ; fields(𝐷) = 𝛼 𝑓 ′ 𝐷 𝑔
                    fields(𝐶) = 𝛼 𝑓 ′ 𝐷 𝑔 𝛼 𝑓 𝐶 𝑓
                                                                                 ·[𝑝 ′′ /𝑝 ′ ] := ·
                                 M-Class                                                           𝑥 : alias(𝑝 [𝑝 ′′ /𝑝 ′ ]) 𝐶, Δ[𝑝 ′′ /𝑝 ′ ]
                                                                                                  
                                                                                                  
                                                                                                  
F-Type                           class 𝐶 extends 𝐷 { 𝐹 𝐾 𝑀 }                         ′′ ′
                                                                                                  
                                                                                                      if 𝛼 = alias(𝑝) for some 𝑝
                                                                      (𝑥 : 𝛼 𝐶, Δ) [𝑝 /𝑝 ] :=
 𝛼 𝑓 𝐵 𝑓 ∈ fields(𝐶)             𝜏 𝑚(𝛼 𝑝 this, 𝛼 𝑝 𝐵 𝑥) { 𝑠 } ∈ 𝑀                                 
                                                                                                   𝑥 : 𝛼 𝐶, Δ′ [𝑝 ′′ /𝑝 ′ ]
                                                                                                  
                                                                                                  
ftype(𝐶) (𝑓 ) = 𝛼 𝑓 𝐵               mtype(𝐶) (𝑚) = 𝛼 𝑝 𝐵 → 𝜏                                          otherwise

                 M-Super
                                                                      A.7 Isolation
                 class 𝐶 extends 𝐷 { 𝐹 𝐾 𝑀 }                          Δ⊢𝑥       𝑝 denotes that a variable 𝑥 is aliased with a path
                   mtype(𝐷) (𝑚) = 𝛼 𝑝 𝐵 → 𝜏                           rooted in 𝑝, i.e. 𝑝, 𝑝.𝑓 , 𝑝.𝑓 .𝑔, etc. In other words, an aliased
                                                                      edge exists between 𝑥 and 𝑝 or a reference edge points to 𝑝.
                    mtype(𝐶) (𝑚) = 𝛼 𝑝 𝐵 → 𝜏
                             (                                           VA-Intro                                                  VA-FieldElim
                           unique          if 𝑒 = null                      Δ(𝑥) = alias(𝑝 ′ )              Δ ⊢ 𝑝 ≡ 𝑝′             Δ⊢𝑥         𝑝.𝑓
               alias(𝑒) :=
                           alias(𝑒)        otherwise                                    Δ⊢𝑥             𝑝                            Δ⊢𝑥        𝑝
  Δ ∗ 𝑝 ⊣ Δ′ denotes that a path 𝑝 is isolated from Δ′ , as
described in Section 3.4.5.                                         R-Shared
                                                                     𝛼 ∈ { shared, owned, unique, ⊥ }              Δ ⊢ Δ′ ★ 𝑝 ⊣ Δ′′
                 I-RemoveField                                                      Δ ⊢ 𝑥 : 𝛼 𝐶, Δ′ ★ 𝑝 ⊣ 𝑥 : 𝛼 𝐶, Δ′′
                 𝑥 ∈ dom(Δ) : Δ ⊢ 𝑥              𝑝.𝑓
                                                                           R-SharedAlias
                          Δ ∗ 𝑝.𝑓 ⊣ Δ                                       Δ ⊢ 𝑝 ′ : shared 𝐶 ⊣ Δ          Δ ⊢ Δ′ ★ 𝑝 ⊣ Δ′′
                                                                           Δ ⊢ 𝑥 : alias(𝑝 ′ ) 𝐶, Δ′ ★ 𝑝 ⊣ 𝑥 : shared 𝐶, Δ′′
          I-ReplaceUniqe
                 Δ = 𝑥 : alias(𝑝 ′ .𝑓 ) 𝐶, Δ′                                 R-Separate
          Δ ⊢ 𝑝 ≡ 𝑝′     Δ ⊢ 𝑝.𝑓 : owned 𝐶 ′ ⊣ Δ                              𝑓 : Δ ⊢ 𝑥          𝑝.𝑓     Δ ⊢ Δ′ ★ 𝑝 ⊣ Δ′′
                                             ′
             Δ ∗ 𝑝.𝑓 ⊣ 𝑥 : unique 𝐶, Δ [𝑥/𝑝.𝑓 ]                                     Δ ⊢ 𝑥 : 𝛼 𝐶, Δ′ ★ 𝑝 ⊣ 𝑥 : 𝛼 𝐶, Δ′′

          I-ReplaceShared                                             R-Inaccessible
                                                                                  Δ ⊢ Δ′ ★ 𝑝 ⊣ Δ′′                    R-Empty
                 Δ = 𝑥 : alias(𝑝 ′ .𝑓 ) 𝐶, Δ′
          Δ ⊢ 𝑝 ≡ 𝑝′     Δ ⊢ 𝑝.𝑓 : shared 𝐶 ′ ⊣ Δ                     Δ ⊢ 𝑥 : 𝛼 𝐶, Δ′ ★ 𝑝 ⊣ 𝑥 : ⊥ 𝐶, Δ′′              Δ ⊢ ·★𝑝 ⊣ ·
                                             ′
             Δ ∗ 𝑝.𝑓 ⊣ 𝑥 : shared 𝐶, Δ [𝑥/𝑝.𝑓 ]
                                                                   Δ ★ 𝑝 1, · · · , 𝑝𝑛 ⊣ Δ′ ⇐⇒ Δ = Δ0 ⊢ Δ0 ★ 𝑝 1 ⊣ Δ1
          I-ReplaceInaccessible                                                                              ..
          Δ = 𝑥 : alias(𝑝 ′ .𝑓 ) 𝐶, Δ′           Δ ⊢ 𝑝 ≡ 𝑝′                                                   .
                  Δ ∗ 𝑝.𝑓 ⊣ 𝑥 : ⊥ 𝐶, Δ′ [𝑥/𝑝.𝑓 ]                                                        Δ𝑛−1 ⊢ Δ𝑛−1 ★ 𝑝𝑛 ⊣ Δ𝑛 = Δ′

   I-ElimField                                                    A.9 Uniﬁcation
              𝑥 ∈ dom(Δ) : Δ(𝑥) ⊢ 𝑥 ≡ 𝑝.𝑓                        𝛼  𝛼 ′ denotes that an annotation 𝛼 may be used in place
   Δ⊢𝑥       𝑝.𝑓 .𝑔  Δ ∗ 𝑝.𝑓 .𝑔 ⊣ Δ′   Δ′ ∗ 𝑝.𝑓 ⊣ Δ′′             of 𝛼 ′ – this means that 𝛼 represents fewer permissions than
                          Δ ∗ 𝑝.𝑓 ⊣ Δ′′                           𝛼 ′.

      I-RemoveVar                                                   A-Id                 A-Shared                        A-Inacc
      Δ = 𝑥 : 𝛼 𝐶, Δ′        𝑦 ∈ dom(Δ′ ) : Δ ⊢ 𝑦            𝑥
                                                                    Δ⊢𝛼 𝛼               Δ ⊢ shared  unique              Δ⊢⊥𝛼
                           Δ ∗ 𝑥 ⊣ Δ′
                                                                   A-Alias                                A-SharedAlias
                     I-ReplaceAlias                                         Δ ⊢ 𝑝1 ≡ 𝑝2                    Δ ⊢ 𝑝.𝑓 : shared 𝐶 ⊣ Δ
                     Δ = 𝑥 : alias(𝑝) 𝐶, Δ′
                                                                    Δ ⊢ alias(𝑝 1 )  alias(𝑝 2 )          Δ ⊢ shared  alias(𝑝.𝑓 )
                        Δ ∗ 𝑥 ⊣ Δ′ [𝑝/𝑥]
                                                                    unify(Δ; Δ1 ; Δ2 ) denotes the uniﬁcation of branches Δ1
      I-ReplaceAliased                                            and Δ2 , given a parent environment Δ.
             Δ = 𝑥 : 𝛼 𝐶, 𝑦 : 𝛼 ′ 𝐶 ′ , Δ′
      Δ⊢𝑦 ≡𝑥   𝛼 ∈ { unique, owned, shared, ⊥ }                                                          U-Comm
                                                                         U-Empty                          unify(Δ; Δ1 ; Δ2 ) = Δ′
                                         ′
                    Δ ∗ 𝑥 ⊣ 𝑦 : 𝛼 𝐶, Δ [𝑦/𝑥]
                                                                         unify(·; Δ1 ; Δ2 ) = ·           unify(Δ; Δ2 ; Δ1 ) = Δ′
      I-ElimVar                                                          U-Join
      Δ = 𝑥 : 𝛼 𝐶, Δ′        𝑦 ∈ dom(Δ′ ) : Δ ⊢ 𝑦 ≡ 𝑥
                                                                                        unify(Δ; Δ1 ; Δ2 ) = Δ′
      Δ⊢𝑦      𝑥 .𝑓        Δ ∗ 𝑥 .𝑓 ⊣ Δ′   Δ′ ∗ 𝑥 ⊣ Δ′′
                                                                         Δ1 (𝑥) = 𝛼 1 𝐶     Δ2 (𝑥) = 𝛼 2 𝐶      Δ′ ⊢ 𝛼 1  𝛼 2
                           Δ ∗ 𝑥 ⊣ Δ′′
                                                                                  unify(𝑥 : 𝛼 𝐶, Δ1 ; Δ2 ) = 𝑥 : 𝛼 1 𝐶, Δ′
A.8 Framing                                                                   U-Isolate
Δ ⊢ Δ★𝑝 ⊣ Δ′ denotes that all edges 𝑝 in the reference graph                   𝑦 ∗ Δ1 ⊣ Δ′1         unify(Δ; Δ′1 ; Δ2 ) = Δ′
of Δ are inaccessible or shared in Δ′ . This is used to remove                       unify(Δ; 𝑦 : 𝛼 𝐶, Δ1 ; Δ2 ) = Δ′
alias references to ﬁelds that are contained in a method call’s
frame since those aliases may no longer be correct if the         A.10     Statement typing
method changes that ﬁeld.                                         A statement 𝑠 is valid if Δ ⊢ 𝑠 ⊣ Δ′ . Δ′ represents the state
   Δ ★ 𝑝 ⊣ Δ′ repeats this process for all paths in the list 𝑝.   after 𝑠 is executed.
Latte: Lightweight Aliasing Tracking for Java


  For ease of notation, we deﬁne Δ ⊢ 𝑒 1 : 𝛼 1 𝐶 1 , · · · , 𝑒𝑛 :            A.11    Program typing
𝛼𝑛 𝐶𝑛 ⊣ Δ′ to hold iﬀ, for some Δ0, · · · , Δ𝑛 ,                             A program 𝑃 = 𝐶𝐿 is valid if 𝐶𝐿 ok for all class declarations
                  Δ = Δ0 ⊢ 𝑒 1 : 𝛼 1 𝐶 1 ⊣ Δ1                                𝐶𝐿.
                           ..                                                       T-Method
                            .
                                                           ′
                                                                                            this : 𝛼 𝑝0 𝐶, 𝑥 : 𝛼 𝑝 𝐶 ⊢ 𝑠 ⊣ Δ′
                     Δ𝑛−1 ⊢ 𝑒𝑛 : 𝛼𝑛 𝐶𝑛 ⊣ Δ𝑛 = Δ                                                     Δ′ ⊢ 𝑒 : 𝛼 𝐶 ′ ⊣ Δ′′
   Similarly, Δ ⊢ 𝑠 1, · · · , 𝑠𝑛 ⊣ Δ′ holds iﬀ, for some Δ0, · · · , Δ𝑛 ,                    class 𝐶 extends 𝐷 { ... }
                                                                                          if mtype(𝐷) (𝑚) = 𝛼 𝑝′ 𝐷 → 𝜏𝑑 , then
       Δ = Δ0 ⊢ 𝑠 1 ⊣ Δ1, · · · , and Δ𝑛−1 ⊢ 𝑠𝑛 ⊣ Δ𝑛 = Δ′ .                                  𝛼 𝑝 𝐶 = 𝛼 𝑝′ 𝐷 and 𝛼 𝐶 ′ = 𝜏𝑑
                                                                                     𝛼 𝐶 ′ 𝑚(𝛼 𝑝0 this, 𝛼 𝑝 𝐶 𝑥) { 𝑠 return 𝑒; }
         S-Block                                                                                      ok in 𝐶
           Δ ⊢ 𝑠 ⊣ Δ′                 S-Decl
                                                                                    T-VoidMethod
         Δ ⊢ { 𝑠 } ⊣ Δ′                Δ ⊢ 𝐶 𝑥; ⊣ 𝑥 : ⊥ 𝐶, Δ
                                                                                          this : 𝛼 𝑝0 𝐶, 𝑥 : 𝛼 𝑝 𝐶 ⊢ 𝑠 ⊣ Δ′
  S-AssignVar                                                                              class 𝐶 extends 𝐷 { · · · }
   Δ(𝑥) = 𝛼 𝐶          Δ ⊢𝑒 :𝐶           Δ0𝑥 ≡𝑒                Δ ∗ 𝑥 ⊣ Δ′             if mtype(𝐷) (𝑚) = 𝛼 𝑝′ 𝐷 → 𝜏𝑑 , , then
                  Δ ⊢ 𝑥 = 𝑒; ⊣ 𝑥 : alias(𝑒) 𝐶, Δ′                                          𝛼 𝑝 𝐶 = 𝛼 𝑝′ 𝐷 and void = 𝜏𝑑

   S-AssignShared
                                                                                    void 𝑚(𝛼 𝑝0 this, 𝛼 𝑝 𝐶 𝑥) { 𝑠 } ok in 𝐶
                  Δ ⊢𝑥 :𝐶              Δ ∗ 𝑥 .𝑓 ⊣ Δ′
                                                                              T-Class
    ftype(𝐶) (𝑓 ) = shared 𝐶 ′           Δ′ ⊢ 𝑒 : shared 𝐶 ′ ⊣ Δ′′
                                                                                  𝐾 = 𝐶 (𝛼 𝑓 ′ 𝐷 𝑔, 𝛼 𝑓 𝐶 𝑓 ){ super(𝑔); 𝑡ℎ𝑖𝑠.𝑓 = 𝑓 ; }
                         Δ ⊢ 𝑥 .𝑓 = 𝑒; ⊣ Δ′′                                   𝐹 = 𝛼𝑓 𝐶 𝑓 ;       fields(𝐷) = 𝛼 𝑓 ′ 𝐷 𝑔   𝑀 ok in C
 S-AssignUniqe                                                                          class 𝐶 extends 𝐷 { 𝐹 𝐾 𝑀 } ok
  Δ ⊢𝑥 :𝐶      Δ ∗ 𝑥 .𝑓 ⊣ Δ′     ftype(𝐶) (𝑓 ) = unique 𝐶 ′
      Δ 0 𝑥 .𝑓 ≅ 𝑒      Δ ⊢ 𝑒 : unique(𝑥 .𝑓 ) 𝐶 ′ ⊣ Δ′′
                          ′
                                                                             Received 20 February 2007; revised 12 March 2009; accepted 5 June
                         Δ ⊢ 𝑥 .𝑓 = 𝑒; ⊣ Δ      ′′                           2009

      S-New
              𝛼 1 𝐶 1 𝑓1, · · · , 𝛼𝑛 𝐶𝑛 𝑓𝑛 = fields(𝐶)
              Δ ⊢ 𝑒 1 : 𝛼 1 𝐶 1 , · · · , 𝑒𝑛 : 𝛼 𝑛 𝐶𝑛 ⊣ Δ ′
            ′
          Δ (𝑥) = 𝛼 𝐵  𝐵 <: 𝐶                    Δ′ ∗ 𝑥 ⊣ Δ′′ 
      ∀0 ≤ 𝑖 < 𝑗 ≤ 𝑛 : 𝛼𝑖 = owned =⇒ Δ′ 0 𝑒𝑖 ≅ 𝑒 𝑗
             Δ ⊢ 𝑥 = new 𝐶 (𝑒); ⊣ 𝑥 : unique 𝐵, Δ′′
    S-Call
          𝛼 0 𝐶 0, · · · , 𝛼𝑛 𝐶𝑛 → 𝛼 𝐶 = mtype(𝐶 0 ) (𝑚)
     Δ ⊢ 𝑒 0 : 𝛼 0 𝐶 0 , · · · , 𝑒𝑛 : 𝛼 𝑛 𝐶𝑛 ⊣ Δ ′  Δ′ (𝑥) = 𝛼 ′ 𝐵
                         ′                     ′′
      𝐵 <: 𝐶          Δ ★ 𝑒0, · · · , 𝑒𝑛 ⊣ Δ      Δ′′ ∗ 𝑥 ⊣ Δ′′′
                                                                
      ∀0 ≤ 𝑖 < 𝑗 ≤ 𝑛 : 𝛼𝑖 = owned =⇒ Δ′ 0 𝑒𝑖 ≅ 𝑒 𝑗
            Δ ⊢ 𝑥 = 𝑒 0 .𝑚(𝑒 1 , · · · , 𝑒𝑛 ); ⊣ 𝑥 : 𝛼 𝐵, Δ′′′
      S-CallVoid
          𝛼 0 𝐶 0 , · · · , 𝛼𝑛 𝐶𝑛 → 𝜏 = mtype(𝐶 0 ) (𝑚)
              Δ ⊢ 𝑒 0 : 𝛼 0 𝐶 0 , · · · , 𝑒𝑛 : 𝛼 𝑛 𝐶𝑛 ⊣ Δ ′
                          Δ′ ★ 𝑒 0, · · · , 𝑒𝑛 ⊣ Δ′′       
      ∀0 ≤ 𝑖 < 𝑗 ≤ 𝑛 : 𝛼𝑖 = owned =⇒ Δ′ 0 𝑒𝑖 ≅ 𝑒 𝑗
                    Δ ⊢ 𝑒 0 .𝑚(𝑒 1 , · · · , 𝑒𝑛 ); ⊣ Δ′′
   S-Conditional
            Δ ⊢ 𝑒 1 : Object       Δ ⊢ 𝑒 2 : Object
   Δ ⊢ 𝑠 1 ⊣ Δ1       Δ ⊢ 𝑠 2 ⊣ Δ2   unify(Δ; Δ1 ; Δ2 ) = Δ′
               Δ ⊢ if (𝑒 1 == 𝑒 2 ) 𝑠 1 else 𝑠 2 ⊣ Δ′
