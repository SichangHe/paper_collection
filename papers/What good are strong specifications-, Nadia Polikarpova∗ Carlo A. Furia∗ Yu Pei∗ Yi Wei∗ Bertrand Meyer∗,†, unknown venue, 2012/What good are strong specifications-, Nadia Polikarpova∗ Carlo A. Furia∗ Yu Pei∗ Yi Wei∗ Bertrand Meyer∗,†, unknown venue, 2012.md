                                                            What Good Are Strong Specifications?
                                                            Nadia Polikarpova∗                Carlo A. Furia∗          Yu Pei∗         Yi Wei∗        Bertrand Meyer∗,†
                                          ∗                                                                            †
                                              Chair of Software Engineering, ETH Zurich, Switzerland ITMO National Research University, St. Petersburg, Russia
                                                                                       firstname.lastname@inf.ethz.ch


                                           Abstract—Experience with lightweight formal methods sug-                           Using strong contracts involves costs and possible benefits.
                                        gests that programmers are willing to write specification if it                    Among the former we have the programming effort necessary
                                        brings tangible benefits to their usual development activities.                    to write such strong specifications and the runtime overhead
                                        This paper considers stronger specifications and studies whether
                                        they can be deployed as an incremental practice that brings                        of checking them during execution. The benefits may include
                                        additional benefits without being unacceptably expensive. We                       finding more errors, finding more subtle errors, finding errors
arXiv:1208.3337v4 [cs.SE] 22 Feb 2013




                                        introduce a methodology that extends Design by Contract to                         more quickly, and exposing errors in ways that are easier
                                        write strong specifications of functional properties in the form of                to understand and correct. Our contributions address the
                                        preconditions, postconditions, and invariants. The methodology                     cost factors—by measuring and trying to mitigate them—and
                                        aims at being palatable to developers who are not fluent in formal
                                        techniques but are comfortable with writing simple specifications.                 assess the benefits:
                                        We evaluate the cost and the benefits of using strong specifications                 • Sect. III presents a methodology to write strong
                                        by applying the methodology to testing data structure implemen-
                                        tations written in Eiffel and C#. In our extensive experiments,
                                                                                                                               specifications—extending our previous work [5]—that
                                        testing against strong specifications detects twice as many bugs                       does not require fluency in formal techniques because it
                                        as standard contracts, with a reasonable overhead in terms of                          is an extension of such traditional practices as Design by
                                        annotation burden and run-time performance while testing. In                           Contract. This is instrumental in reducing the program-
                                        the wide spectrum of formal techniques for software quality,                           ming effort associated with strong specifications.
                                        testing against strong specifications lies in a “sweet spot” with a
                                                                                                                             • The methodology comes with tool support and specifica-
                                        favorable benefit to effort ratio.
                                                                                                                               tion libraries, so that strong specifications are usable with
                                                              I. I NTRODUCTION                                                 standard debugging and testing tools.
                                        Many years of progress in the theory and practice of formal                          • Sect. IV and V describe an extensive empirical study that
                                        methods notwithstanding, writing software specifications1 still                        evaluates the use of strong contracts for real software
                                        seems to be “disliked by almost everyone” [1]. In many cases,                          and measures their costs and benefits in terms of defect
                                        this disliking is a consequence of a high cost/benefit ratio—                          detection.
                                        perceived or real—of writing and maintaining accurate spec-                           The bulk of our empirical study targets EiffelBase, a library
                                        ifications on top of the code. After all, developers will write                    of generic containers and data structures (such as lists, tables,
                                        specifications as long as they are simple, have a straightfor-                     and trees), which has been in use in the Eiffel community
                                        ward connection with the implementation, and help them write                       for more than 20 years. The production version of EiffelBase
                                        and debug code better and faster. One example is Design by                         includes simple contracts, a form of partial specification, that
                                        Contract [2], [3] where simple executable specifications, writ-                    are nonetheless quite effective at finding implementation bugs
                                        ten in the same syntax as programming language expressions,                        automatically using contract-based random testing [6], where
                                        support design, incremental development, and testing and                           executable contracts serve as oracles and enable a push-button
                                        debugging. Another one is test-driven development [4], where                       testing process. In the present paper, we augment the simple
                                        rigorously defined test cases play the role of specifications                      contracts that come with EiffelBase using the methodology
                                        in defining correct and incorrect behavior. Experiences with                       discussed in Sect. III. The result is EiffelBase+: a version of
                                        these techniques show that providing lightweight specifications                    EiffelBase with identical implementation but strong (mostly
                                        is an accepted practice when it brings tangible benefits and                       complete) specifications.
                                        integrates well with the overall development process.
                                                                                                                              In an extensive set of experiments, we compare the effec-
                                           But what about strong specifications, which attempt to cap-
                                                                                                                           tiveness of random testing on EiffelBase and EiffelBase+, with
                                        ture the entire (functional) behavior of the software? Should
                                                                                                                           the goal of assessing whether the additional effort invested
                                        we dismiss them on the grounds that the effort required to
                                                                                                                           into the strong contracts pays off in terms of quantity and
                                        write them is not justified against the benefits they bring in
                                                                                                                           complexity of the bugs found. Our experiments show that
                                        the majority of mundane software projects? This paper studies
                                                                                                                           these measures dramatically increase when deploying strong
                                        the impact of deploying strong behavioral specifications, in
                                                                                                                           specifications: random testing found twice as many bugs in
                                        the form of contracts (pre- and postconditions and class
                                                                                                                           EiffelBase+, and the simple contracts of EiffelBase would
                                        invariants), for detecting errors in software using automatic
                                                                                                                           have uncovered none of the new bugs. The overhead size
                                        testing.
                                                                                                                           of specifications, in contrast, remains moderate, with the
                                          1 In this paper, we target formal specifications of functional properties.       specification-to-code ratio going from 0.2 to 0.46.
merge right (other: LINKED LIST [G])                                    merge right (other: LINKED LIST [G])
 require                                                                 require
    not after                                                               −− As in Tab. I
    other 6= Void                                                        modify sequence
    other 6= Current                                                     ensure
 ensure                                                                     sequence = old (sequence.front (index) +
    count = old count + old other.count                                                      other.sequence + sequence.tail (index + 1))
    index = old index                                                    end
 end
                                                                                                     TABLE II
                                  TABLE I                               M ODEL - BASED SPECIFICATION OF ROUTINE merge right IN LINKED LIST.
  S TANDARD SPECIFICATION OF ROUTINE merge right IN LINKED LIST.



                                                                        occurs in the special case of calling merge right with cursor
   Our approach to writing strong specifications that are ef-           before the list (index = 0): the implementation will insert other
fective for testing is not limited to Eiffel programs. In a             at the second rather than at the first position. For example,
companion set of experiments, we applied the same technique             merging f·o·l·d and u·n when the cursor is before yields f·u·n·o·l·d
to writing strong specifications for the DSA C# library [7] and         instead of the correct u·n·f·o·l·d.
tested the result using Pex [8]; in this case too we discovered
                                                                           Sect. III presents a methodology to write, with moderate ef-
new bugs with reasonable additional effort.
                                                                        fort, strong specifications that extend and, whenever possible,
         II. S TRONG S PECIFICATIONS : A N E XAMPLE                     complete this kind of partial specification. Tab. II shows the
                                                                        strong specification obtained by applying the methodology to
The following example illustrates and justifies the use of strong       merge right, the way it appears in EiffelBase+. As is common
specifications. Consider the EiffelBase class LINKED LIST—              in most Eiffel projects, the programmer who wrote merge right
Eiffel’s standard implementation of linked lists. Like many             did a good job with the precondition, which is sufficiently
containers in EiffelBase, LINKED LIST includes an internal              detailed and need not be strengthened. The postcondition,
cursor to iterate over elements of the list. The query2 index           however, turns into a single assertion that defines the sequence
gives the cursor’s position, which can be on any element of the         of elements stored in the list after calling merge right as the
list in positions 1 through count, or take the special boundary         concatenation (operator +) of three segments: Current’s original
values 0 (“before” the list) and count + 1 (“after” the list). The      sequence up until position index (written sequence.front (index)),
attribute count denotes the number of elements in the list.             followed by other’s element sequence, followed by the original
   Tab. I shows the EiffelBase specification of LINKED LIST’s           sequence from position index + 1 (written sequence.tail (index + 1)).
routine (method) merge right. The routine inserts another list          This postcondition relies on an abstract model of the linked
other passed as argument into the current list (denoted Current in      list in the form of a mathematical sequence of elements,
Eiffel, corresponding to this in Java and C#) immediately after         which was already implicitly present above, in the informal
the cursor position. For example, if Current stores the sequence        description of the semantics of merge right. Models blend well
of elements b·a·r·t with cursor positioned on the “r” (index = 3)       with Eiffel’s standard specification constructs to help formalize
and other stores o·n·e, merge right changes Current to b·a·r·o·n·e·t.   programmers’ intuitive understanding of data structures se-
The precondition (require) specifies that the routine cannot be         mantics. Using the strong postcondition in Tab. II, completely
called when the cursor is after: there is no valid position to the      automatic testing with the AutoTest tool [6] detected the error
right of it. It also demands that other be non-Void (null in Java       that occurs in merge right when the cursor is before.
and C#) and not aliased with the Current list: otherwise, merg-            The postcondition in Tab. II describes how the sequence
ing is not well defined. The postcondition (ensure) describes           changes, but it does not say what does not change. Including
some expected effects of executing merge right: the Current list        the assertion index = old index from the original postcondition is
will contain as many elements as it contained before the call to        not sufficient, as it only mentions one piece of state that does
merge right (denoted by old count) plus the number of elements          not change. Instead we include the assertion modify sequence,
of the other list; and the cursor’s position index will not change.     which means that merge right may only modify the sequence
   The contracts in Tab. I are a good example of the kind of            of elements in the Current list and nothing else. Together pre-,
specification that Eiffel programmers normally write [9]: it is         postcondition, and modify clause give a complete specification
correct and nontrivial, and it can help detect errors in the im-        of merge right behavior, against which we can automatically test
plementation, such as performing partial merges or incorrectly          any implementation for correctness.
leaving the cursor at a different position. Unfortunately the
specification is also incomplete, because it does not precisely                 III. H OW TO W RITE S TRONG S PECIFICATIONS
describe the expected state of the list after merging. In fact,
the current implementation of merge right contains an error that        Writing good specification is hard; at least this is the common
is undetectable against the specification of Tab. I. The error          belief. Experience with Design by Contract suggests that
                                                                        programmers can competently write simple specifications if
  2 A query is an attribute or a function [2].                          they can be expressed using familiar syntax. See for example
the specification in Tab. I, which refers to regular class queries   class LINKED LIST [G]
such as count and index, also used in the implementation.
                                                                       model sequence, index
   Without further guidance and language support, however,
programmers tend to write only partial specifications, because         sequence: MML SEQUENCE [G]
expressing complex properties is cumbersome. This section                status specification
                                                                         −− Specification query: sequence of elements in the list.
describes model-based contracts (MBC): a methodology to
write strong specifications that structures and extends tradi-         index: INTEGER
tional Design by Contract. MBC includes simple guidelines                −− Internal cursor position.
to define the abstract model of a class (Sect. III-A), and to          off: BOOLEAN
write pre- and postconditions of routines (Sect. III-B and III-C)           −− Is the cursor not on a list element?
and other, more advanced, specification elements (Sect. III-D             ensure
                                                                            Result = not sequence.domain.has (index)
and III-E).                                                               end
   The MBC approach supports writing strong specifications in
a number of ways: models facilitate choosing the right level         invariant
                                                                       −− Model constraint
of abstraction and expressing complex behavioral properties            0 ≤ index and index ≤ sequence.count + 1
concisely, while the structured discipline for writing postcon-        −− Attribute definition
ditions and invariants, together with the notion of complete-          count = sequence.count
                                                                       −− Linking invariant
ness (Sect. III-D), provides precise guidelines as to which            bag = sequence.to bag
properties are worth documenting in a contract, and when a             −− Internal representation constraint
contract is strong enough. While fostering rigor and accuracy          not sequence.is empty implies last cell.item = sequence.last
                                                                     end
in specifications, MBC is still palatable to practitioners be-
cause its notation is part of the programming language. When                                     TABLE III
                                                                       E XCERPT OF LINKED LIST’ S MBC SPECIFICATION IN E IFFEL BASE +.
developing specifications for testing, as opposed to formal
verification, MBC can be exploited incrementally: developers
may skip writing the most advanced specification elements (for
example, complex class invariants) while still getting strong        make use of MML classes to represent complex components
specifications that are useful to detect subtle errors.              of class models. For example, LINKED LIST’s model in Tab. III
   The following subsections present MBC using examples              has two components: a specification function sequence with
from EiffelBase. The few additional constructs introduced            return type MML SEQUENCE that gives the abstract sequence
by MBC are highlighted in a different color and underlined           of elements stored in the list, and the ordinary class attribute
in the examples (e.g., modify). The current presentation of          index of integer type.
MBC derives from previous work of ours [5], which focused               Class models should be expressive enough to formalize the
on using strong specifications when designing new software.          class behavior as seen at the API level, without exposing
In this paper we adapt the principles introduced in [5] to           implementation-specific details. For example, the same ab-
the goal of supplying existing software with flexible strong         stract model—a sequence of elements—is suitable for all three
specifications for runtime checking and automatic testing (see       implementations of lists in EiffelBase: singly-linked, doubly-
Sect. III-F). We also extend the specification methodology with      linked and array-based, as the particular representation does
new construct that handle framing (Sect. III-D) and complex          not influence the functional properties of public routines. In
class invariants (Sect. III-E).                                      practice, it is usually easy to devise a model for a data struc-
A. Abstract Class Models                                             ture using MML abstractions. Even for classes representing
                                                                     complex real-world concepts, such as an ATM or a flight
Writing strong specifications becomes simpler if we can              scheduler, MML remains applicable if used incrementally to
readily express the abstract state space of classes and how          define partial yet useful behavioral properties.
it changes. Therefore, the first step in specifying a class with
MBC is defining a model for the class: a set of mathematical         B. Preconditions
elements that capture the abstract state space.
   Syntactically, the annotation model (see Tab. III) declares       The precondition of a routine defines when a call to the routine
the abstract model of a class as a list of attributes or functions   is valid. In practice preconditions appear to be the most widely
called model queries; each element listed after model is either      and accurately used form of contract [9]. Therefore, MBC does
a query of basic type (Boolean, integer, or object reference)        not introduce special guidelines for writing preconditions.
already used in the implementation, or a specification query,
meaning a query introduced solely to define the model. As part       C. Postconditions
of our work on MBC, we developed the Mathematical Model              The postcondition of a routine r describes the intended effects
Library (MML), a collection of immutable Eiffel classes that         of executing r on the object state; it is a relation between the
represent mathematical concepts useful for specification: sets,      state just before (denoted using the keyword old) and the state
bags, sequences, maps, and relations. Specification queries          just after executing r.
   MBC postconditions express the intended effect of execut-          E. Class Invariants
ing a routine on the model, that is in terms of the model             The class invariant specifies global properties of valid in-
queries. Procedure merge right in Tab. II, for example, declares      stances of a class, which every operation must preserve. Since
its effect on the model query sequence of the current object. For     the semantics of class invariants can be subtle MBC intro-
functions, the postcondition also mentions the returned object        duces additional dedicated constructs for complex invariant
(and its model queries) using the keyword Result. For example,        properties. We borrow some ideas from the existing techniques
function off in Tab. III defines Result in terms of sequence and      developed for formal correctness proofs (e.g., [10], among
index.                                                                many); unlike these sophisticated techniques, MBC’s solution
                                                                      for class invariants does not target comprehensiveness, but is
D. Framing Specification                                              easy to deploy and sufficient in practice for finding errors by
                                                                      testing and avoiding spurious invariant violations.
An accurate routine specification should limit the effects of            Class invariant types. Like postconditions, class invariants
the routine execution to a certain part of the program state.         in MBC use models to describe which object states are valid
Such specification elements are called framing specifications.        and which are not. For example, the first invariant clause in
   Eiffel offers no dedicated language support for writing            Tab. III constrains the values of the model queries sequence
framing specifications. In principle this support is not strictly     and index, stating that index must never take values outside the
necessary, because one can express the unchanged elements             interval [0..sequence.count + 1].
in postconditions with expressions such as index = old index in          Additionally, class invariants in MBC have three more spe-
Tab. I. In practice, however, this is cumbersome because              cific usages: definitions of public attributes, linking invariants
any given routine usually affects only a handful of program           and internal representation constraints. Public attributes, from
elements; hence explicitly specifying all that does not change        the class interface standpoint, are indistinguishable from public
is verbose and tedious. In fact, Eiffel practitioners rarely write    functions, and thus their values should be defined in terms of
framing specifications in this form.                                  model queries. An example of such attribute definition is the
   In MBC, the keyword modify introduces a routine’s framing          second invariant clause in Tab. III, which explains the attribute
specification: a list of all model queries whose value is allowed     count is terms of the model query sequence.
to change after executing the routine. For example, routine              Parent classes may use simpler abstract models than their
merge right in Tab. II may only change sequence, but not index        children. LINKED LIST, for instance, inherits from a generic
and not any component of the other list’s model.                      CONTAINER class whose model is a bag (multiset) rather than
   The modify clause mechanism is taken from other specifi-           a sequence, because the order of its elements is immaterial.
cation notations and methodologies (e.g., Spec# [10]) usually         To reuse the specification of the parent stated in terms of
targeted to formal correctness proofs. It is only with a speci-       a different model, we introduce class invariants that define
fication technique based on models, however, that it becomes          the parent’s model queries in terms of the child’s model; we
practical for real classes and standard programming practices.        call them linking invariants. For example, the third invariant
Writing modify clauses in terms of attributes would violate           clause in Tab. III says that the parent’s model query bag
information hiding and be of limited usefulness to the client,        contains the same elements as sequence, disregarding the order
while listing arbitrary public queries is too tedious: since the      (sequence.to bag).
values of several regular queries are often related (for example,        Finally, internal representation constraints introduce speci-
the value of off may change when index changes; see Tab. III),        fications that relate the values of model queries to the private
modify clauses should include all related queries, possibly also      attributes of the class. For example, the last invariant clause
queries with arguments and on other objects. Model queries            in Tab. III says that the private attribute last cell stores the
are instead normally only a small number, they are orthogonal,        same value as sequence’s last element (whenever the sequence
and only depend on the state of the Current object. Hence             is not empty). Unlike other MBC specifications, invariants
specifying which model queries change is not onerous; the             of this type do not describe the public interface of the
values of all other queries are automatically defined in terms        class and usually cannot be made complete without revealing
of them.                                                              unnecessary implementation details in the model. However,
   This approach to framing also supports a simple definition         even in this limited form, they turned out to be very effective
of specification completeness: a routine postcondition and            at revealing errors that corrupt object’s internal representation
framing specification are complete if the relation between the        (see Sect. V-A).
model’s pre- and poststate is a function.3 Completeness is not           Class invariant semantics. Eiffel checks class invariants
an imperative in the MBC methodology: programmers can still           at the beginning and at the end of every qualified4 call
approach writing postconditions and framing incrementally. It         on an object of the class. This rule prevents checking the
should rather be viewed as a safeguard against accidentally           invariant whenever routines of a class call one another within
missing an important property.                                        the boundaries of a single object, in order to accomplish a
                                                                      common task, as the object will normally be inconsistent
  3 Such notion of completeness is of course relative to the model.     4 A call t.r is qualified when the target t is an object other than Current.
(“open”) until all operations are completed. When circular               prune (n: NODE)
dependencies between objects arise, this semantics may lead                do
                                                                             if left = n then
to spurious invariant violations: this is the dependent delegate                left.set parent (Void) ; left.set root (True) ; left := Void
problem [11].                                                                end
   Consider an example derived from real code in EiffelBase:                 if right = n then . . . end
                                                                           end
a binary tree data structure, where each node has a link to its
parent and left and right children. The Current node is executing      When prune’s call to left.set parent returns, the invariant about
one of its routines and is temporarily in a state that violates        parent and is root is violated (left.parent = Void but left.is root is still
the invariant; to restore it, it makes a qualified call on, say, its   false). Annotating prune with open n suspends checking of n’s
right child. The object right, however, does not know that its         invariant until prune terminates, thus removing the spurious
parent is in the middle of executing a call; if right calls back       invariant violation.
to Current, then, it detects an invariant violation even if right’s       As we discuss in Sect. IV, in EiffelBase+ we had to deploy
call does not rely on the invariant.                                   explicit depend and open annotations only in a very few cases,
   MBC deploys a runtime semantics where these spurious in-            limited to doubly-linked list nodes, and binary and n-ary trees.
variant violations do not occur. Objects are implicitly equipped
with a Boolean attribute is open that is set to true at the entrance   F. Runtime Support for Strong Specifications
of every public routine call on the object and restored to its         Model-based postconditions and invariants can be checked at
previous value when the routine terminates; class invariants           runtime and used in testing out of the box: with the same
are checked only if is open is false. This automatically solves        tools and user experience as standard Eiffel contracts. Model
the dependent delegate problem in the presence of callbacks:           queries introduced for specification purposes are implemented
when right calls back to Current, the latter is open, and hence        as regular functions that compute the abstract model value
its invariant is not checked.                                          from the concrete object state, and thus do not require explicit
   This “implicit opening” mechanism is not sufficient to              initialization or updates. The specification classes we provide
avoid spurious invariant violations when an object’s invariant         in MML are also regular Eiffel classes, implemented in a
depends on the state of other objects. Consider again binary           functional style. Even though this approach to implementation
trees; an invariant states that the Current node is its parent’s       of model queries and model classes potentially incurs a high
left or right child:                                                   runtime overhead, the experiment results in Sect. V confirm
   parent 6= Void implies (parent.left = Current or parent.right =     that using MBC for contract-based testing is feasible.
         Current)                                                         Newly introduced specification constructs, such as modify,
                                                                       depend and open, do not have any effect in the standard
Routine prune left removes Current’s left child as follows:
                                                                       Eiffel semantics: they are specified using note meta-annotations
     old left := left                                                  (similar to Javadoc or C#’s meta-data). We have developed a
     left := Void
     if old left 6= Void then old left.set parent (Void) end           simple tool that rewrites these annotations into plain Eiffel; for
                                                                       example, modify clauses become explicit postconditions such
When old left.set parent (Void) is called to remove the back-link      as item = old item. The MBC methodology is conservative, in
from Current’s child, old left’s class invariant is violated: its      that the class semantics is still sound if we ignore the spe-
parent’s left is already set to Void and old left is not open; in      cial annotations; ignoring modify clauses, for instance, yields
fact, the very reason for calling set parent is to remove this         weaker, yet correct, postconditions.
inconsistency. MBC provides the keyword depend to declare
that an invariant clause depends on the state of an attribute,             IV. U SING S TRONG S PECIFICATIONS : E XPERIMENTS
and hence it should be checked only if the object attached to
                                                                       We performed an extensive experimental evaluation to assess
attribute is closed. Annotating the invariant in the example
                                                                       the benefits of using strong specifications for finding errors in
with depend parent removes the spurious invariant violation
                                                                       software.
(old left.parent is Current, which is open).
   In the few cases when fine-grained control over the opening         A. Research Questions
of objects is necessary, MBC provides the open clause for
routines, which explicitly opens the objects attached to some of       The overall goal of this evaluation is assessing and comparing
the routine’s arguments when the routine begins execution and          the advantages and the cost of deploying strong specifications
restores them when the routine terminates (as we discussed,            in the form of model-based contracts (MBC, described in
the target is always opened implicitly). Consider a variant of         Sect. III) when applied to automatic contract-based testing of
the binary tree example where nodes have an attribute is root          real software.
that should be true when their parent node is Void:                       This materializes into the following research questions:
                                                                          1) Are strong specifications effective for finding faults in
   parent = Void implies is root = True
                                                                             software?
In this variant, prune takes an argument of class NODE that is            2) Do strong specifications find subtle and complex faults?
supposed to be its left or right child and removes it as follows:         3) Do strong specifications find faults in little testing time?
   4) What is the performance overhead of checking strong                     the number of faults, since it would impose a heavier burden
      specifications at runtime?                                              on its implementation. We treat preconditions as developers’
   5) What is the development effort required to provide                      design decisions, which we normally take at face value. This
      strong specifications for existing software?                            policy makes the experiments with EiffelBase and EiffelBase+
   To answer these questions, we conducted two sets of experi-                fully comparable.
ments, targeting software written in Eiffel (Sect. IV-B) and C#                  The only exception occurred with four routines of class
(Sect. IV-C). In both cases, we selected an open-source library,              BINARY TREE and eight routines of class TWO WAY TREE that
specified it following the MBC methodology, and extensively                   insert new nodes into a tree. In these twelve cases, we strength-
tested it with a standard automatic testing tool. The rest of this            ened the preconditions to disallow creating cycles among
section discusses the experiments; Sect. V presents the results.              nodes in the tree. Without the strengthening, tree instances can
                                                                              be driven into inconsistent states with cycles where the whole
B. Eiffel Experiments                                                         specification of trees would be inapplicable. These changes in
The main experiments target EiffelBase (rev. 506)—Eiffel’s                    preconditions are conservative: the EiffelBase+ experiments
standard base library—from which we selected 21 classes                       using these stronger preconditions miss a few faults that are
of varying size and complexity. Using the facilities of the                   detected in EiffelBase, because the new preconditions rule out
EiffelStudio IDE, we built the flat version of each class, which              some previously valid failing test cases. Since these changes
is a self-contained implementation including all inherited                    affect only a small fraction of all the experiments, the results
members explicitly in the class text. This simplified the task of             with EiffelBase and EiffelBase+ remain comparable.
writing specifications without being distracted by EiffelBase’s                  Specification correctness. To write correct strong contracts
deep multiple inheritance hierarchy. For each of the 21 classes               with MBC, we analyzed the original implementation, con-
in their flat version, Tab. IV lists the size (in LOC) and                    tracts, and comments in EiffelBase, and relied on our informal
the number of public routines (PR), possibly also including                   knowledge of the semantics of data structures and their imple-
helper classes directly used in the class implementation. Since               mentation. To increase our confidence in the correctness of the
different classes may share some parent or helper classes, the                new specification, we ran a series of short preliminary testing
totals at the bottom of the table are in general less than the                sessions with the goal of detecting inconsistencies and inaccu-
sum of the elements in each column.                                           racies. All our changes were conservative, in that whenever a
   Like most Eiffel software, EiffelBase comes with partial                   new contract forbade a behavior that was not clearly forbidden
specification in the form of contracts: the 21 classes include                by the comments, standard contracts, or informal knowledge,
561 precondition clauses, 985 postcondition clauses, and 250                  we weakened the specification to allow the behavior. In all,
class invariant clauses. In EiffelBase+ we completely replaced                we reached a high confidence that EiffelBase+’s specification
EiffelBase’s original postconditions and class invariants with                is correct and strong enough. The results of the main testing
model-based annotations, but we kept EiffelBase’s precondi-                   sessions (Sect. V) corroborate this informal assessment.
tions (with a few exceptions discussed below)5 . EiffelBase+’s                   Testing experiments. We ran a large number of random
strong specification includes 589 precondition clauses, 1066                  testing sessions with the AutoTest framework [6] on a com-
postcondition clauses and 164 class invariant clauses (21%                    puting cluster of the Swiss National Supercomputing Centre,
model constraints, 23% attribute definitions, 10% linking                     configured to allocate a standard 1.6 GHz core and 4 GB
invariants, 46% internal representation constraints), as well as              memory to each parallel AutoTest session. The experiments
278 modify, 4 depend and 7 open clauses. Tab. IV shows the                    totalled 1680 hours of testing time that generated nearly 87
size (in LOC and PR) of EiffelBase+, which also includes                      millions of test cases; the TC columns in Tab. IV list the
model definitions and implementations of the model queries                    million of test cases drawn when testing each class in Eiffel-
necessary to write MBC.                                                       Base and in EiffelBase+. The testing of every class was split
   Preconditions. In all but two EiffelBase+ classes we kept                  into 30 sessions of 80 minutes, each with a new seed for the
the same preconditions as in EiffelBase. Within the specific                  random number generator, such that corresponding sessions in
setup of our experiments, where we compare traditional con-                   EiffelBase and EiffelBase+ use the same seeds. This thorough
tracts and strong contracts, it is important to have the same                 testing protocol guaranteed statistically significant results [13].
preconditions in the two artifacts under comparison. Precondi-
tions define the valid calling contexts of routines (in particular,           C. C# Experiment
contract-based testing tools use them to select valid test cases).
                                                                              A smaller set of experiments targets 9 classes from DSA
Changing preconditions would change the semantics of classes
                                                                              (v. 0.6)—an open-source data structure and algorithm library
in a way similar to changing implementation: strengthening
                                                                              written in C# [7]. Support for contracts in C# appeared
a precondition may reduce the number of faults detectable
                                                                              only recently, through the Code Contracts framework [14];
for the routine, since it would move obligations from the
                                                                              therefore, most C# projects (including DSA) do not have
routine to its clients; weakening a precondition may increase
                                                                              any formal specification. This was a chance to extend the
  5 All the code developed as part of the study, as well as descriptions of   validation of the MBC methodology to other languages and to
found faults are publicly available online [12].                              projects without pre-existing specification.
                                                                      TABLE IV
                                                      E IFFEL CLASSES UNDER TEST AND RESULTS .

                                                                  E IFFEL BASE                                            E IFFEL BASE +
 C LASS                                     LOC       PR       TC     S PEC    I NC   R EAL     N EW      LOC      PR        TC    I NC  R EAL   N EW
 ARRAY                                       831       53      2.8        2       0       2        1       986      59       1.2      0      3       2
 ARRAYED LIST                               1840       86      3.5        0       0       0        0      2037      92       1.7      0      1       1
 ARRAYED QUEUE                               537       32      1.8        0       0       2        0       648      37       3.8      0      2       0
 ARRAYED SET                                1960       49      5.8        3       1       8        0      2053      58       5.4      0     16       8
 BINARY TREE                                1122       64      1.0        2       5       6        0      1366      70       1.1      0     16      10
 BOUNDED QUEUE                               558       32      1.4        0       0       2        0       659      37       3.8      0      2       0
 HASH TABLE                                 1345       51      0.9        1       0       1        0      1626      63       0.9      0      2       1
 HASH TABLE ITERATOR                         217       15      0.4        0       0       0        0       248      15       0.5      0      0       0
 INDEXABLE ITERATOR                          186       14      1.0        2       0       0        0       228      15       2.7      0      0       0
 INTEGER INTERVAL                            519       42      4.3        1       1       0        0       637      45       0.9      0      3       3
 LINKED LIST                                1759       69      2.0        0       0       2        0      1942      77       2.5      0      5       3
 LINKED LIST ITERATOR                        311       15      0.7        0       0       0        0       357      16       0.7      0      0       0
 LINKED SET                                 2128       83      5.4        5       2       7        0      2410      94       4.8      0     24      17
 LINKED SET ITERATOR                         311       15      0.7        0       0       0        0       357      16       0.7      0      0       0
 LINKED STACK                               1077       27      1.0        0       0       3        1      1078      32       3.2      0      6       4
 TWO WAY LIST                               2007       71      0.8        0       0       3        0      2184      79       2.2      0      6       3
 TWO WAY LIST ITERATOR                       412       15      0.7        0       0       0        0       462      16       0.7      0      0       0
 TWO WAY SORTED SET                         2706       91      5.3        5       2       9        0      2983     102       4.8      1     34      25
 TWO WAY SORTED SET ITERATOR                 412       15      0.7        0       0       0        0       462      16       0.7      0      0       0
 TWO WAY TREE                               2548       90      1.4        4       4      22        5      2865     101       1.3      0     29      12
 TWO WAY TREE ITERATOR                       412       15      0.7        0       0       0        0       462      16       0.7      0      0       0
 Total                                     17841     1033     42.5       15      12      48        7     19400    1164     44.4       1    103      62
   LOC: Lines of code, PR: Public routines, TC: Test cases drawn (million)
   S PEC: Specification errors found, I NC: Inconsistency errors found, R EAL: Real faults found, N EW: Faults found only in this experiment


                             TABLE V
                C# CLASSES UNDER TEST AND RESULTS .                            The experiment setup is consistent with this programming
                                                                               style: we do not consider such exceptions to be faults.
                              DSA             DSA+          T ESTING              Testing experiments. We performed automatic testing with
    C LASS                 LOC    PR        LOC   PR          T    F
    AvlTree                 345    6         391    7        23    1           the Pex concolic testing framework [8] running on a Windows
    BinarySearchTree        205    5         213    5        21    1           box equipped with a 2.16 GHz Intel Core2 processor and 3 GB
    CommonBinaryTree        419   13         536   18        83    0           of memory. The experiments ran for about 12 hours; column
    Deque                   201   14         231   15       145    0
    DoublyLinkedList        408   17         458   19       171    3           T in Tab. V reports the breakdown per class in minutes. The
    Heap                    371   11         390   12        61    1           testing time is different from class to class because Pex testing
    OrderedSet              136    9         158   11        10    0           sessions by default are limited by coverage criteria rather than
    PriorityQueue           186   13         216   14        65    0
    SinglyLinkedList        439   20         492   22       148    3           duration. We only tested DSA+ since DSA has no formal
    Total                  3043 133         3486 149        727    9           specification elements usable as automated testing oracles.
      LOC: Lines of code, PR: Public routines                                     The C# experiment is less extensive than the Eiffel exper-
      T: Testing time (minutes), F: Faults found                               iment and intended as a control mechanism to identify any
                                                                               potential dependency of the results on the Eiffel language,
                                                                               libraries (EiffelBase) or tools.
   We instructed one of our bachelor’s students to follow
the methodology of Sect. III and create DSA+: a variant                                V. U SING S TRONG S PECIFICATIONS : R ESULTS
of DSA with the same implementation but equipped with                          This section discusses the result of the experiments, focusing
strong model-based contracts. DSA+’s specification includes                    on the larger EiffelBase experiments, with V-A through V-E
6 precondition clauses, 143 postcondition clauses and 23 class                 targeting the research questions 1–5 of Sect. IV-A. Then, V-F
invariant clauses. For each of the 9 classes, Tab. V shows the                 briefly discusses the experiments with C#, and V-G presents
size (in LOC and PR) of both DSA and DSA+, inclusive of                        possible threats to validity of the results.
all specification elements and model query implementations.
As in Tab. IV, the count also includes (possibly shared) helper                A. Faults Found
classes. Flattening was not necessary in this case because the                 AutoTest found 75 faults in EiffelBase and 104 in EiffelBase+;
inheritance hierarchy is shallow.                                              these are unique, that is they identify distinct and independent
   Specification correctness. We manually inspected the                        errors. We classified them in three categories.
DSA+ specification written by our student, and assessed its                       Specification faults correspond to violations of wrong con-
quality to be comparable to that of EiffelBase+ in terms of                    tracts (meaning that in our judgement they specify the ex-
correctness and completeness. Since DSA was not designed                       pected behavior of the program incorrectly). We found 15
with contracts in mind, it makes recurrent usage of defensive                  specification faults in EiffelBase (column S PEC in Tab. IV)
programming, throwing exceptions to signal invalid arguments.                  and none in EiffelBase+, which increased our confidence
that the preliminary testing sessions mentioned in Sect. IV-B
were sufficient to achieve correct specifications. We consider
specification faults spurious in our study, because we are not
                                                                        EiffelBase                                                  EiffelBase+
comparing the correctness of the specification in EiffelBase
and EiffelBase+ but rather their effectiveness at finding real
                                                                        40           50           60              70           80        90
errors in the implementation.
   Inconsistency faults correspond to failures triggered by calls                               Total number of faults found

on objects in inconsistent states, which are not captured by a
partial class invariant. For example, LINKED SET may be driven      Fig. 1. Unique real faults found in all classes over 80-minute testing sessions.
into a state where the container stores duplicate elements;
calling remove (x) in such a state triggers a failure (only one
occurrence of x is removed), but remove is not to blame for            Except for the two ITERATOR classes (no faults in both
it, since it is due to previous erroneous behavior that went        cases) and the two QUEUE classes (the same two faults in
undetected. While inconsistency faults are genuine errors, we       both cases), the number of faults found is consistently higher
classify them separately because understanding and locating         in EiffelBase+ in each class. As evident from the boxplot in
the ultimate source of an inconsistency is normally harder.         Fig. 1, the difference is highly significant: the Mann-Whitney
Additionally, a single inconsistency fault often results in many    U test gives U = 0 (testing EiffelBase+ outperforms testing
failing test cases (potentially in all routines of the class that   EiffelBase in all sessions), and p = 2 · 10−11 overall and
rely on the broken invariant), requiring additional effort from     p ≤ 2.1 · 10−11 for every class (except the ITERATORs and
                                                                    QUEUEs). The difference remains highly statistically significant
the developer when analyzing the testing results.
   We found 12 inconsistency faults in EiffelBase and 1 in          even if we aggregate the experiments in sessions of different
EiffelBase+ (columns I NC in Tab. IV); the ultimate source of       length.
the latter fault is a class invariant not including all internal          Testing with strong specifications detected 55 more
representation constraints (see Sect. III-E), which would have            (twice as many) unique real faults than testing with
required exposing implementation details in the model. The               standard, partial contracts. 62 (56%) of the faults are
other inconsistency faults of EiffelBase are not detected in                    detected only with strong specifications.
EiffelBase+, because, due to stronger class invariants, their
real source is detected instead. In the LINKED SET example          B. Fault Complexity
above, instead of the inconsistency fault in remove, MBC report     Although it is to some extent subjective whether a fault is
a fault in routine replace, which does not check if the new value   “deep” or “subtle”, faults violating postconditions or class
is already present in the set, thereby introducing duplicates.      invariants are arguably more complex because so are the
The results in this category indicate that strong specifications    violated properties. While there is no significant difference in
report faults in a way that is easier to understand and debug.      the percentage of class invariant violations between EiffelBase
   All other errors are real faults which correspond to genuine     and EiffelBase+ (33% in both cases), postconditions trigger
errors directly traceable to the code. We found 48 real faults in   42% of violations in EiffelBase+ but only 11% in EiffelBase:
EiffelBase and 103 in EiffelBase+ (columns R EAL in Tab. IV);       the Wilcoxon signed-rank test among all classes gives W = 0
41 of them are found in both sets of experiments, 7 only in         and p = 6 · 10−3 both for postconditions alone and for
EiffelBase, and 62 only in EiffelBase+. We submitted bug            postconditions and class invariants counted together, which
reports for all the 110 faults found in our experiments. The        demonstrates that strong specifications systematically detect
Eiffel Software developers in charge confirmed 107 (97%) of         more complex errors. 76% of faults in EiffelBase+ are detected
them as real bugs to be fixed. This is evidence that we are         thanks to postconditions or invariants—a direct consequence
dealing with genuine faults in our evaluation. The remaining        of the effectiveness of the MBC methodology for writing them.
three faults not taken on by the developers also arguably              One example of a fault detected by a model-based postcon-
highlight real problems in the implementation, but they are         dition was already discussed in Sect. II. Here we give two
probably not so likely to occur during “normal” runs. The rest      other examples to demonstrate that they are indeed subtle yet
of the discussion focuses on real faults unless stated otherwise.   understandable:
   Only seven faults are found in EiffelBase but not in                • Routine ARRAY.force(v, i) inserts value v at position i into
EiffelBase+ (columns N EW in Tab. IV). Four of them are                  an array, extending its bounds if needed. All elements
prevented by the strengthened preconditions in the tree classes          in between the old bound and i are supposed to be
(Sect. IV-B); two are shadowed by new failures occurring                 initialized with default values, however force contains an
earlier; and one disappears with MBC due to an unintentional             off-by-one error, and in a particular scenario fails to
side-effect of a model query that amends an invariant violation.         initialize one element. This is missed by the original
None of these faults found only in EiffelBase show inherent              postcondition item(i)= v, which only takes care of the newly
deficiencies of strong specifications or of the MBC method.              inserted element, but detected by the complete model-
In contrast, the 62 faults found only in EiffelBase+ are                 based postcondition, which, following the methodology,
undetectable in EiffelBase.                                              specifies array elements at all positions.
                                                                                                             TABLE VI
                                                                                                     S PECIFICATION OVERHEAD

                                                                                   # TOKENS          E IFFEL BASE   E IFFEL BASE +   OVERHEAD
                                                                                   Preconditions             1514             1696        1.12
                                                                                   Postconditions            5410            11837        2.19
                                                                                   Invariants                1508             1587        1.05
                          80




                                                                                   MBC annotations                            1893
                                                                                   Model queries                              2268
                                                                                   Total                    8432             19281        2.29
                                                                                   Spec/code                 0.20             0.46
                          60
Unique faults found




                                                                                that the behavior with strong specifications dominates over
                          40




                                                                                standard contracts after only a few minutes. Dominance is
                                                                                observed consistently in all classes (with the usual exception of
                                                                                ITERATORs and QUEUEs): a median session with strong contracts
                          20




                                                                                finds more faults than a median session with standard contracts
                                                                                after a time between two seconds and five minutes depending
                                                            ●   EiffelBase
                                                            ●   EiffelBase+
                                                                                on the class under test; after a time between 13 seconds and 20
                          0




                                                                                minutes, testing with strong contracts finds more faults than
                               0   20      40         60               80       testing with standard contracts will find in the whole session.
                                        Time (min)                                 Testing with standard contracts also seems to exhaust earlier
                                                                                its fault-finding potential: given any time from 20 minutes on,
Fig. 2. Median number of faults, aggregated from all classes, in time. Dotted   there are more EiffelBase sessions than EiffelBase+ sessions
lines show minimum and maximum for each case.                                   that have found all the faults they ever will by this time. This
                                                                                may indicate that standard contracts are good to find “quick
                                                                                to detect” faults, but they also soon run out of steam.
      Both ARRAYED SET and LINKED SET inherit most of their
                      •
                                                                                   We considered other differences between experiments with
      implementation from the corresponding list classes, in-                   EiffelBase and with EiffelBase+ in the usage of testing time:
      cluding the implementation of is equal: the object equality               repeatability of testing session history, and the presence of rare
      function. As a result, two sets with the same elements in                 faults triggered only in a small number of cases. Our exper-
      a different order are considered different. The original                  iments with strong specifications are slightly less repeatable
      postcondition only states that equal sets must have the                   and include a few more rare faults, but the differences with
      same size and that equality is symmetric, which does not                  standard contracts are not statistically significant.
      capture the specifics of set equality.
   It is revealing that 11 faults in EiffelBase+ are detected due               D. Runtime Performance Overhead
to violations of contracts generated automatically by our tool
that processes MBC annotations (Sect. III-F) such as modify                     Runtime checking of strong specifications based on models
and depend. These faults are practically out of the scope of                    often requires traversing the whole data structure to construct
regular contracts, as specifying the corresponding properties                   an object of a model class, whenever a contract element is
explicitly is extremely onerous.                                                exercised. As a rule, this demands more computational re-
   Throughout the whole experiment we encountered one                           sources than executing the simple checks involved in standard
violation of an invariant that could be later restored before                   contracts. To measure the runtime overhead of checking MBC
the enclosing public routine call terminates. Strictly speaking,                specifications in automated testing, we compared the number
such violation is spurious, and to eliminate it we would                        of test cases generated by AutoTest in the same amount of
have to extend the notation for open clauses, in order to                       time when testing EiffelBase and EiffelBase+. Contrary to
support opening arbitrary expressions rather than just routine                  our expectations, the overhead is small in many cases and not
arguments. However in reality this particular invariant was                     significant overall (see column TC of Tab. IV). A possible
not restored, so the violation pointed to a real fault. This                    interpretation of this data is that the overhead of strong
example suggests that if an object is too “far away” in the                     specifications grows as larger data structures are instantiated;
object structure from the call target to be mentioned in the                    because random testing most of the time only exercises small
open or depend clause, it is likely that a developer forgets to                 data structures, this overhead does not show.
restore its invariant anyway, because the object is not in the                     We did not find a significant correlation between the vari-
area of immediate interest for the routine.                                     ation of overhead for different classes and any source code
                                                                                metrics we considered. On the other hand, some AutoTest
C. Usage of Testing Time                                                        heuristics that decide to discard previously created objects are
Fig. 2 plots the number of faults detected in EiffelBase and                    activated more often for classes where strong specifications
EiffelBase+ over a median 80-minute session; it is clear                        are faster to check.
E. Specification Writing Overhead                                    G. Threats to Validity
Applying MBC to create EiffelBase+ required roughly one              Threats to internal validity of our findings come from the usage
person-month, plus one person-week of preliminary testing            of randomized testing tools, whose behavior may change in
for fine-tuning the specification, which puts the overall ratio      different sessions. We designed the experimental protocol [13]
benefit/effort at about four defects detected per person-day.        to reduce this threat to a minimum: we ran a large number
Tab. VI measures the amount of work produced in this time:           of repeated experiments and we performed suitable non-
for each specification item, including preconditions, postcon-       parametric statistical tests of significance for all differences
ditions, class invariants, MBC annotations such as modify,           we observed.
and model query implementations, we compare the number                  Threats to external validity refer to the generalizability of
of tokens in EiffelBase+ against those in EiffelBase (when           our findings. While MBC leads to very good results in our
applicable) and give the OVERHEAD of strong specifications           experiments, applying it to programs in application domain
as the ratio of the two values. The last line also shows the         other than data structures might be more difficult or require
overall specification to code ratios.                                an extension of the technique. Our results remain significant,
                                                                     however, if compared to the state of the art in deploying
   Reflecting the importance MBC gives to strong postcondi-
                                                                     strong specifications. The generalizability to other languages
tions and the more restricted role of class invariants, 67% of all
                                                                     and analysis tools is partially addressed by our experiments
new specification in EiffelBase+ are postconditions, whereas
                                                                     targeting two languages (Eiffel and C#) and two automatic
only 9% are class invariants. MBC-specific annotations are
                                                                     testing technologies (random and concolic). Future work will
11%, mostly modify clauses that are however straightforward
                                                                     experiment with even more approaches and notations.
to write and dispense for more intricate explicit framing
specifications. Model query implementations account for the                              VI. R ELATED W ORK
remaining 13%.                                                       This section discusses the most significant related work in
   These numbers suggest that the specification overhead of          three areas: using formal specifications for testing; using
MBC is moderate and abundantly paid off by the advantages            inferred specifications to improve testing; and model-based
in terms of errors found and quality of documentation. The           specification methods.
specification to code ratio also compares favorably to other ap-        Formal specifications for testing. The idea of using formal
proaches to improving software quality. Detailed quantitative        specifications for testing has a history that stretches back
data about industrial experiences with test-driven development       more than three decades; see [20] for a comprehensive survey.
is scarce, but few references indicate [4], [15], [16] that it is    Various proposals targeted different specification formalisms
common to have between 0.4 and 1.0 lines of tests per line of        including algebraic datatypes [21], [22], logic-based nota-
application code for projects of size comparable to EiffelBase.      tions [23], UML Statecharts [24] and other state machines, and
Correctness proofs are normally much more demanding, as              contracts and similar forms of embedded assertions [25], [26],
they require between 1.5 and 9 specification elements per            [27], [6]. In these applications, formal specifications provide
implementation element [17], [18], [19].                             reliable—often automated—testing oracles [28] and can also
                                                                     guide test planning and test case generation.
F. C# Experiments                                                       This extensive experience is evidence that formal speci-
                                                                     fications can improve the testing process. From a software
Pex found 9 unique faults in DSA+ violating the model-               engineering viewpoint, however, an outstanding open issue
based specification (column F in Tab. V). Unfortunately, we          is finding optimal trade-offs between the effort required to
could not get an evaluation of these faults by the original          provide formal specifications and the improvements (in ef-
code developers. We have confidence, however, that the faults        ficiency and effectiveness) they bring to the testing of real
uncover some obvious errors and, even in the most benign             software. The evidence—empirical [29] or anecdotal [1]—
interpretation, some instances of bad object-oriented design.        is scarce in this area: most successful experiences do not
    The fault rates (faults per line of executable code) are com-    explicitly take into account the effort required to produce
parable in the Eiffel and C# experiments, being respectively         reliable specifications against the benefits gained for testing
6 · 10−3 and 3 · 10−3 . The fault complexity is also qualitatively   (e.g., [30]); or they only target partial specifications, which
similar for the two languages. The testing time (column T            have the advantage of being easy to write (e.g., [27], [6]).
in Tab. V) is instead incomparable, as Pex and AutoTest              In contrast, this paper targeted the high-hanging fruit of
implement very different testing algorithms.                         deploying strong specifications, explicitly addressing the dif-
    Applying MBC to create DSA+ required roughly 50 person-          ficulties of writing and using such specifications for existing
hours, plus another 8 person-hours used by the student to            software. Our results that strong specifications reveal complex
learn the MBC methodology on small examples. The spec-               (design) errors corroborate Hoare’s view that the real value
ification/code ratio is perceptibly higher in DSA+ compared          of tests is that “they detect inadequacy in the [development]
to EiffelBase+ (0.9); this is largely due to the verbose syntax      methods” [31].
of Code Contracts which are a library, as opposed to Eiffel’s           Inferred specifications for testing. When specifications can
native language support for contracts.                               be inferred automatically from the code, the deployment effort
is negligible compared to the benefits they bring. Therefore,                 [2] B. Meyer, Object Oriented Software Construction. Prentice Hall, 1997.
a number of recent works (e.g., [32], [33], [34], [35]) devel-                [3] P. Chalin, “Are practitioners writing contracts?” in The RODIN Book,
                                                                                  ser. LNCS, vol. 4157, 2006, p. 100.
oped sophisticated techniques for inferring specifications from               [4] K. Beck, Test-Driven Development. Addison-Wesley, 2002.
program executions with the intent of using them to improve                   [5] N. Polikarpova, C. A. Furia, and B. Meyer, “Specifying reusable
testing. The experiments reported in these papers show that                       components,” in VSTTE, ser. LNCS, vol. 6217, 2010, pp. 127–141.
inferred specifications can boost automated testing [36]; on                  [6] B. Meyer, A. Fiva, I. Ciupa, A. Leitner, Y. Wei, and E. Stapf, “Programs
                                                                                  that test themselves,” IEEE Computer, vol. 42, no. 9, pp. 46–55, 2009.
the other hand, even the most accurate inferred specifications                [7] http://dsa.codeplex.com/.
only express the code from a different angle, and hence cannot                [8] N. Tillmann and J. de Halleux, “Pex–white box test generation for
take the developer’s intent fully into account and are nec-                       .NET,” in TAP, 2008, pp. 134–153.
                                                                              [9] N. Polikarpova, I. Ciupa, and B. Meyer, “A comparative study of
essarily limited to detecting certain types of inconsistencies.                   programmer-written and automatically inferred contracts,” in ISSTA,
Combining inferred and manually written specifications is an                      2009, pp. 93–104.
interesting endeavor that belongs to future work (see [9], [37]              [10] M. Barnett, K. R. M. Leino, and W. Schulte, “The spec# programming
for some preliminary studies).                                                    system: an overview,” in CASSIS. Berlin, Heidelberg: Springer-Verlag,
                                                                                  2005, pp. 49–69.
   Model-based specification methods. The methodology                        [11] B. Meyer, “The dependent delegate dilemma,” in Engineering Theories
described in Sect. III extends our previous work [5] with                         of Software Intensive Systems. Springer, 2005.
the specific goal of developing executable specifications for                [12] http://se.inf.ethz.ch/people/polikarpova/mbctesting.
                                                                             [13] A. Arcuri and L. Briand, “A practical guide for using statistical tests to
automated testing. The same goal has also motivated the                           assess randomized algorithms in software engineering,” in ICSE. ACM,
techniques to improve the runtime checking of strong spec-                        2011, pp. 1–10.
ifications described in Sect. III-F. The related work section                [14] http://research.microsoft.com/en-us/projects/contracts/.
of [5] compares the foundations of our model-based method                    [15] N. Nagappan, E. M. Maximilien, T. Bhat, and L. Williams, “Realizing
                                                                                  quality improvement through test driven development: results and ex-
against other similar approaches such as JML [38].                                periences of four industrial teams,” ESE, vol. 13, no. 3, pp. 289–302,
                                                                                  2008.
           VII. C ONCLUSIONS AND F UTURE W ORK                               [16] E. M. Maximilien and L. Williams, “Assessing test-driven development
This paper presents a methodology to write strong specifi-                        at IBM,” in ICSE, 2003, pp. 564–569.
cations that extends the traditional Design by Contract, and                 [17] V. Klebanov et al., “The 1st verified software competition,” in FM, ser.
                                                                                  LNCS, vol. 6664, 2011, extended version at www.vscomp.org.
applied it to specifying data structure classes in Eiffel and C#.            [18] F. Dupressoir, A. D. Gordon, J. Jürjens, and D. A. Naumann, “Guiding
We carried out an extensive empirical evaluation to determine                     a general-purpose C verifier to prove cryptographic protocols,” in IEEE
the benefits of using such strong specifications in testing with                  Computer Security Foundations Symposium, 2011.
                                                                             [19] J.-C. Filliâtre, “Verifying two lines of C with Why3: an exercise in
automatic tools. We found twice as many bugs in the software                      program verification,” in VSTTE, ser. LNCS, 2012, pp. 83–97.
with strong specifications as in the same software specified                 [20] R. M. Hierons et al., “Using formal specifications to support testing,”
with standard partial contracts. We also demonstrated that the                    ACM Comput. Surv., vol. 41, no. 2, 2009.
effort required to write the strong specifications was moderate              [21] J. D. Gannon, P. R. McMullin, and R. G. Hamlet, “Data-abstraction
                                                                                  implementation, specification, and testing,” ACM Trans. Program. Lang.
thanks to the methodology that is practical and palatable to                      Syst., vol. 3, no. 3, pp. 211–223, 1981.
professionals not fluent in formal techniques.                               [22] J. Chang and D. J. Richardson, “Structural specification-based testing:
   The benefits brought by strong specifications are not limited                  Automated support and experimental evaluation,” in ESEC/FSE, 1999,
                                                                                  pp. 285–302.
to finding errors through testing. While the present paper                   [23] P. Stocks and D. A. Carrington, “Test templates: A specification-based
focused on adding strong specifications to existing code a pos-                   testing framework,” in ICSE, 1993, pp. 405–414.
teriori, our related work [5] shows that model-based contracts               [24] A. J. Offutt and A. Abdurazik, “Generating tests from UML specifica-
                                                                                  tions,” in UML, 1999, pp. 416–429.
help achieve consistent designs and higher-quality code by
                                                                             [25] D. Marinov and S. Khurshid, “TestEra: A novel framework for auto-
construction.                                                                     mated testing of Java programs,” in ASE, 2001, p. 22.
   As future work, we plan to extend the MBC methodology                     [26] Y. Cheon and G. T. Leavens, “A simple and practical approach to unit
and supporting tools to work on more complicated application                      testing: The JML and JUnit way,” in ECOOP, 2002, pp. 231–255.
                                                                             [27] C. Boyapati, S. Khurshid, and D. Marinov, “Korat: automated testing
domains with a higher degree of automation, and to support                        based on Java predicates,” in ISSTA, 2002, pp. 123–133.
other software analysis techniques such as correctness proofs                [28] M. Staats, M. W. Whalen, and M. P. E. Heimdahl, “Programs, tests, and
and static analysis. We will also expand the experimental                         oracles,” in ICSE, 2011, pp. 391–400.
evaluation to more projects and programming languages.                       [29] M. M. Müller, R. Typke, and O. Hagner, “Two controlled experiments
                                                                                  concerning the usefulness of assertions as a means for programming,”
   Acknowledgements. Thanks to Rosemary Monahan and                               in ICSM, 2002, pp. 84–92.
Scott West for comments on a draft of this paper; and to                     [30] L. du Bousquet, Y. Ledru, O. Maury, C. Oriat, and J.-L. Lanet, “Reusing
                                                                                  a JML specification dedicated to verification for testing, and vice-versa:
Tobias Kiefer for carrying out the C# experiments. This work                      Case studies,” J. Autom. Reasoning, vol. 45, no. 4, pp. 415–435, 2010.
was partially supported by the Swiss SNF under projects                      [31] C. A. R. Hoare, “How did software get so reliable without proof?” in
FullContracts (200021-137931) and ASII (200021-134976);                           FME, 1996, pp. 1–17.
we also acknowledge the support of the Swiss National                        [32] C. Pacheco and M. D. Ernst, “Eclat: Automatic generation and classifi-
                                                                                  cation of test inputs,” in ECOOP, 2005, pp. 504–527.
Supercomputing Centre for the testing experiments.                           [33] T. Xie and D. Notkin, “Tool-assisted unit-test generation and selection
                                                                                  based on operational abstractions,” Autom. Softw. Eng., vol. 13, no. 3,
                            R EFERENCES                                           pp. 345–371, 2006.
 [1] D. L. Parnas, “Precise documentation: The key to better software,” in   [34] A. Zeller, “Mining specifications: A roadmap,” in The Future of Software
     The Future of Software Engineering. Springer, 2011, pp. 125–148.             Engineering. Springer, 2010, pp. 173–182.
[35] Y. Wei, H. Roth, C. A. Furia, Y. Pei, A. Horton, M. Steindorfer,
     M. Nordio, and B. Meyer, “Stateful testing: Finding more errors in code
     and contracts,” in ASE, 2011, pp. 440–443.
[36] M. d’Amorim, C. Pacheco, T. Xie, D. Marinov, and M. D. Ernst,
     “An empirical comparison of automated generation and classification
     techniques for object-oriented unit testing,” in ASE, 2006, pp. 59–68.
[37] Y. Wei, C. A. Furia, N. Kazmin, and B. Meyer, “Inferring better
     contracts,” in ICSE, 2011, pp. 191–200.
[38] G. T. Leavens, Y. Cheon, C. Clifton, C. Ruby, and D. R. Cok, “How
     the design of JML accommodates both runtime assertion checking and
     formal verification,” Sci. Com. Prg., vol. 55, no. 1-3, pp. 185–208, 2005.
