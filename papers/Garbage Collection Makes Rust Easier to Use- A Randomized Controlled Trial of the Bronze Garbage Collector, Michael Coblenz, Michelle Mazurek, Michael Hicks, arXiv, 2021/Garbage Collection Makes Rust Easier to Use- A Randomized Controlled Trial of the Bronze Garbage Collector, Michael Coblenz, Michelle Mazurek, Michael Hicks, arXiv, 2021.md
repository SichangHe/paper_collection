                                              Garbage Collection Makes Rust Easier to Use: A Randomized
                                                   Controlled Trial of the Bronze Garbage Collector
                                                          Michael Coblenz                                          Michelle L. Mazurek                                  Michael Hicks
                                                     University of Maryland                                       University of Maryland                          University of Maryland
                                                   College Park, Maryland, USA                                  College Park, Maryland, USA                     College Park, Maryland, USA
                                                       mcoblenz@umd.edu                                           mmazurek@cs.umd.edu                                mwh@cs.umd.edu
                                         ABSTRACT                                                                                    discipline of ownership and lifetimes (based on linear logic [32] and
                                         Rust is a general-purpose programming language that is both type-                           region-based memory management [14, 30], respectively) to ensure
                                         and memory-safe. Rust does not use a garbage collector, but rather                          that no object reference will be used after its referent is freed. This
arXiv:2110.01098v2 [cs.SE] 15 Feb 2022




                                         achieves these properties through a sophisticated, but complex,                             discipline imposes restrictions on aliasing: an alias can only be
                                         type system. Doing so makes Rust very efficient, but makes Rust                             borrowed temporarily, and doing so limits mutation (which also
                                         relatively hard to learn and use. We designed Bronze, an optional,                          helps avoid data races). For example:
                                         library-based garbage collector for Rust. To see whether Bronze
                                         could make Rust more usable, we conducted a randomized con-                                 fn foo () {
                                         trolled trial with volunteers from a 633-person class, collecting data                        let s1 = String :: from (" hello ") ;
                                         from 428 students in total. We found that for a task that required                            let len = calc_len (& s1 ) ; // lends reference
                                                                                                                                       println !(" the length of '{} ' is {}" , s1 , len ) ;
                                         managing complex aliasing, Bronze users were more likely to com-
                                                                                                                                       // s1 lifetime ends ; dropped
                                         plete the task in the time available, and those who did so required                         }
                                         only about a third as much time (4 hours vs. 12 hours). We found                            fn calc_len ( s : & String ) -> usize {
                                         no significant difference in total time, even though Bronze users                             // s . push_str (" hi ") ; <-- not allowed : s immutable
                                         re-did the task without Bronze afterward. Surveys indicated that                              s . len () // s lifetime ends ; but not its referent ' s
                                                                                                                                     }
                                         ownership, borrowing, and lifetimes were primary causes of the
                                         challenges that users faced when using Rust.
                                                                                                                                     Here, function foo defines a String owned by variable s1. It then
                                         CCS CONCEPTS                                                                                calls calc_len to compute its length by lending a reference &s1 to
                                                                                                                                     the called function, which may only read it, not write it. When
                                         • Software and its engineering → General programming lan-
                                                                                                                                     the function returns, the borrowed reference’s lifetime ends so it is
                                         guages; • Human-centered computing → Empirical studies
                                                                                                                                     dropped, which restores full ownership to s1. When function foo
                                         in HCI; • Social and professional topics → Computing edu-
                                                                                                                                     completes, s1’s lifetime ends so it is dropped and the data is freed.
                                         cation.

                                         KEYWORDS                                                                                    1.1    Rust is Hard to Learn and Use
                                         Rust, garbage collection, usability of programming languages, em-                           Despite its performance and safety advantages and a loyal core of
                                         pirical study of programming languages, programming education                               devotees [26], Rust remains relatively unpopular; the TiOBE index
                                         ACM Reference Format:                                                                       ranks Rust at #27 as of July 2021 [7], and the IEEE Spectrum ranks
                                         Michael Coblenz, Michelle L. Mazurek, and Michael Hicks. 2022. Garbage                      Rust at #20 [11]. In the interest of bringing the benefits of the design
                                         Collection Makes Rust Easier to Use: A Randomized Controlled Trial of                       ideas behind Rust to more software projects, it is worth considering
                                         the Bronze Garbage Collector. In 44th International Conference on Software                  why Rust has seen limited adoption.
                                         Engineering (ICSE ’22), May 21–29, 2022, Pittsburgh, PA, USA. ACM, New                         A partial explanation resides in the difficulty of learning Rust.
                                         York, NY, USA, 12 pages. https://doi.org/10.1145/3510003.3510107                            Fulton et al. [12] interviewed and surveyed software practitioners
                                                                                                                                     who adopted or attempted to adopt Rust, finding that 59% of survey
                                         1     INTRODUCTION                                                                          respondents felt that Rust was harder to learn than other languages.
                                         Rust is a general-purpose programming language that has an em-                              Seven of the 16 interviewees reported that the biggest challenges
                                         phasis on performance while also being type-, memory-, and thread-                          in learning Rust were the borrow checker—the part of the compiler
                                         safe [28]. One reason for Rust’s efficiency is that it does not use                         that enforces the ownership/borrowing discipline—and the overall
                                         garbage collection (GC). Instead, it imposes a compiler-enforced                            change of programming paradigm to one that requires that the
                                                                                                                                     compiler be able to reason about lifetimes. Ashley Williams, the
                                         Permission to make digital or hard copies of part or all of this work for personal or       interim executive director of the Rust Foundation, agreed: “[Refer-
                                         classroom use is granted without fee provided that copies are not made or distributed       ences and borrowing] is notoriously something that people find to
                                         for profit or commercial advantage and that copies bear this notice and the full citation
                                         on the first page. Copyrights for third-party components of this work must be honored.      be the most difficult part of learning Rust” [34]. The difficulty of
                                         For all other uses, contact the owner/author(s).                                            learning Rust has implications on adoption in software teams: 42%
                                         ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                              of respondents in Fulton et al.’s survey were concerned about their
                                         © 2022 Copyright held by the owner/author(s).
                                         ACM ISBN 978-1-4503-9221-1/22/05.                                                           ability to hire Rust developers, since it would take a long time for
                                         https://doi.org/10.1145/3510003.3510107                                                     new team members to become productive.
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


   In addition to being challenging to learn, Rust can be difficult to    Topic                     Traditional task         Bronze task
use. Programming with DAGs and cyclic data structures is straight-
forward in most popular languages, but such structures do not             Basics                    BasicsnoGC               BasicsnoGC
conform to Rust’s aliasing restrictions. Rust provides safe building      Ownership, lifetimes      OwnershipnoGC            OwnershipGC
blocks to work around these restrictions. The structure Rc<T> is for      Aliased, mutable data     AliasingnoGC             AliasingGC
references to immutable T objects with manually managed reference         Aliased, mutable data     (none)                   AliasingnoGC
counts (confirmed safe by the borrow checker), and RefCell<T> is a       Table 1: Tasks in each condition. Subscripts indicate versions
container for a mutable T object with dynamically tracked borrow-        of tasks adapted to use GC, or not. Bronze participants com-
ing. Together (e.g., Rc<RefCell<T>>) these can implement a discipline    pleted AliasingnoGC after completing AliasingGC .
of interior mutability that supports rich aliasing patterns [19], but
in a manner far more complex than most programmers are used
to. As such, they may be tempted to use Rust’s unsafe feature to
sacrifice safety for ease of use.                                        assigned to condition Bronze or Traditional; the former group used
   Easing Use with Garbage Collection? Rust’s restrictions are due       Bronze in the assignment while the latter group did not. Ultimately,
to the compiler’s inability to verify the safe use of richer, aliased    333 students were part of the random assignment, and 428 students
data structures. These restrictions would not be needed if Rust          participated in the study in some way.
used GC. As such, an extension to Rust that included GC could               The experiment design is shown in Table 1; the tasks are de-
enable programmers to be productive sooner, without having to            scribed in detail in section 3.1. In the assignment, students were
learn the trickier parts of the language right away. By making the       given functions and declarations that needed to be completed;
GC optional, programmers could still learn and use the harder parts      Bronze participants were given versions of the interfaces that were
of Rust later, and convert their GC-using code to traditional Rust       structurally similar but which had been adapted to use GC. The
as needed to improve performance.                                        assignment parts were cumulative, and the final step for Bronze
   Moreover, by making a Rust GC library-based, it could even prove      participants was to redo their previous implementation without
useful to experts. While 63% of the respondents in the survey by         using GC, ensuring all participants learned how to use traditional
Fulton et al. [12] cited lack of GC as a reason to use Rust, 87% cited   Rust. We provided students with unit tests (including source code),
high performance as a reason—between the two is a category of            and we assigned grades according to which of the unit tests passed.
user open to the idea that high performance and garbage collection          We found, after conducting the experiment, that Bronze’s inter-
are not always at odds. Most code is not performance-critical: a         face required small changes to ensure soundness. Because of the
guideline is that 90% of the time is spent executing only 10% of the     small size of the required changes, which are described in more
code [2]. Thus GC- and manual-based memory management could              detail in section 4, we believe that our results apply to the revised
coexist. Experiments in Cyclone [14], a C-like systems program-          version of Bronze as well.
ming language, found nearly no performance cost of using GC when            Study Results. At the conclusion of the study we carried out both
it was applied judiciously alongside safe, manual techniques [27].       quantitative and qualitative analysis of measured data (e.g., project
                                                                         score) and survey responses. Our large sample enabled us to re-
1.2     Bronze: A Library-Based GC for Rust                              serve 10% of the participants’ data (with their survey responses) for
This paper presents Bronze,1 a new Rust library that provides a          exploratory analysis. This allowed us to explore which hypothe-
clean garbage collection interface, and an experiment evaluating the     ses might be worth testing while preserving soundness, since the
possible benefits of using Bronze while learning Rust. By creating       results in section 5 are based on the remaining 90% of the data.
a library in which GC is optional, we were able to study the effects        We did not observe a difference between conditions in comple-
of GC without including the rest of the language design as an            tion rates (fraction of students scoring 100%) or in times complet-
independent variable in the study.                                       ing Ownership. However, students who used Bronze were more
    Bronze provides a structure, GcRef<T>, that implements a garbage-    likely to complete their aliasing task (AliasingGC ) than Traditional
collected reference to a mutable object; such references are not         students were to complete theirs (AliasingnoGC ), and did so sig-
subject to Rust’s aliasing restrictions. Bronze uses LLVM stack maps     nificantly faster, spending a median of 4 hours instead of 12 hours.
to automatically find roots, obviating the need for programmers          The additional time spent by Bronze students doing the aliasing
to specify tracing roots manually, as is necessary in some existing      task again, this time without GC (AliasingnoGC ) resulted in no sig-
Rust GCs [4, 18].                                                        nificant difference in total time spent on the project. We conclude
    We deployed Bronze in an IRB-approved, randomized, controlled        that for newcomers to Rust, if the goal is simply to accomplish a
experiment in a sophomore-level programming languages course.            programming task, garbage collection may present a significant
Because the course was required for graduation at a university with      benefit for productivity. Further, there may be enough advantage to
a large computer science enrollment, we were able to recruit from        using garbage collection while learning Rust to compensate for the
a population of 633 students who were enrolled in the course. All        additional time required to learn, apply, and switch to traditional
students carried out a multi-part Rust programming assignment,           Rust memory management approaches.
but those who agreed to participate in the research were randomly           Survey results confirmed past reports [12, 34] that ownership
                                                                         and borrowing are significant programming challenges. Partici-
1 So named for bronze’s corrosion resistance.                            pants were much more likely to believe that GC makes writing
Garbage Collection Makes Rust Easier to Use: A Randomized Controlled Trial of the Bronze Garbage Collector            ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA


programs easier after completing the experiment than they were                              Rust permits only one mutable reference to a value at a time. For
before the experiment. Bronze participants were more likely to                          greater flexibility, (standard) Rust supports interior mutability of an
believe that GC made writing programs easier after completing the                       object through an immutable reference to it [19]. The programmer
whole assignment than they did at the beginning, and 64 of the 89                       may borrow a special reference to the value that permits muta-
Bronze participants (72%) who responded to the question strongly                        tion, and dynamic checks ensure that only one such reference can
agreed at the end that using GC makes writing programs easier.                          exist at a time, enabling a safe relaxation of compile-time checks.
Only 3 (3%) strongly disagreed. Interestingly, although participants                    With Bronze, mutation is permitted through all references to each
reported that GC made programming easier, participants who used                         garbage-collected object, with no extra effort. For example, Figure 1
GC did not report liking Rust significantly more than participants                      shows how GcRef simplifies code when there are multiple muta-
who did not. We observed a stronger negative correlation between                        ble aliases. Bronze does not guarantee thread safety; as in other
liking Rust and stress than between liking Rust and time spent                          garbage-collected languages, it is the programmer’s responsibility
relative to participants’ expectations.                                                 to ensure safety.
                                                                                            Bronze is a precise, mark/sweep garbage collector. We selected
1.3     Implications                                                                    this design rather than using a conservative collector [5] because
                                                                                        precise collection has the potential for better performance and com-
Software engineers should be aware of a possible productivity bene-
                                                                                        plete collection of garbage. As our primary objective in the design
fit of garbage collectors relative to using Rust’s aliasing restrictions;
                                                                                        was usability, we designed Bronze to find roots automatically. Prior
it may be better to re-architect a system, use a garbage collection li-
                                                                                        garbage collectors for Rust either include root and unroot methods
brary, or use a garbage-collected language if the architecture cannot
                                                                                        that must be manually called by the user of the GC library [4, 18]
be changed. If engineers use a library-based GC with Rust and need
                                                                                        or require references to be cloned manually [13, 25].
to remove it to improve performance, using GC saves enough time
                                                                                            Bronze defines the Trace trait, which indicates functionality used
that programmers can switch away from GC without a significant
                                                                                        by the garbage collector to trace through the object graph to find
loss in productivity.
                                                                                        live objects. Only types that implement Trace can be put on the
    That positive feelings about Rust were more strongly correlated
                                                                                        garbage-collected heap. Bronze also defines the Finalize trait, which
with frustration and stress than with time spent on the assignment
                                                                                        allows users to write code that runs just before an object is deallo-
suggests that language designers who want to promote adoption (by
                                                                                        cated by the collector; it serves as an alternative to drop, which is
making languages programmers like) should consider focusing on
                                                                                        for deallocation that runs at a statically-determined time. Bronze
how to reduce stress, such as by making progress more predictable,
                                                                                        provides macros that automatically derive implementations of Trace
rather than how to (only) maximize programmer productivity.
                                                                                        and Finalize for straightforward types, but users can provide their
    In survey responses, participants reported extreme difficulty with
                                                                                        own implementations if needed.
references, lifetimes, and ownership. Participants said examples and
                                                                                            Rust’s compiler translates Rust code to LLVM IR, which has a
live coding demonstrations helped them learn these concepts most
                                                                                        primitive that allows emitting stack maps to annotate the stack
effectively. These responses have implications for pedagogy: we
                                                                                        with compiler-specified metadata. In the case of Bronze, the meta-
hypothesize that using examples and live coding demonstrations
                                                                                        data allow the runtime to determine which stack addresses corre-
is more effective to explain these challenging Rust concepts than
                                                                                        spond with objects that must be traced because they may reference
traditional slide-based explanations.
                                                                                        garbage collected objects. The Bronze tracer relies on a modified
                                                                                        version of the Rust compiler that emits stack map information in
1.4     Contributions                                                                   the emitted LLVM IR. The particular stack map mechanism used by
Key contributions of this paper include:                                                Bronze assumes that the program is single-threaded; other available
                                                                                        mechanisms could relax this requirement in the future at additional
    (1) The design and prototype implementation of Bronze, a GC
                                                                                        engineering cost for Bronze.
        for Rust that is simpler to use than prior Rust GCs.
                                                                                            Bronze uses a mark/sweep algorithm based on Goregaokar’s
    (2) A randomized controlled trial of Bronze, in which we found
                                                                                        implementation [13]. To identify which objects can be collected,
        that Bronze can enable more people to complete tasks within
                                                                                        the runtime keeps a linked list of all objects that it allocated. Then
        time limits and, among those who finished, significantly re-
                                                                                        it can collect objects on the list that were not marked by the tracer.
        duce time required. We also collected qualitative data, con-
                                                                                        Bronze’s mark/sweep implementation is only a proof of concept,
        firming that ownership, lifetimes, and references are partic-
                                                                                        however, and is not production-ready. In particular, the implementa-
        ularly challenging for new Rust programmers.
                                                                                        tion can trace local variables of type GcRef<T>, but additional work is
                                                                                        required to enable tracing of arbitrary types. In the experiment, we
2     BRONZE: DESIGN AND IMPLEMENTATION                                                 used a version of Bronze that never collects. This approach was suit-
Bronze introduces GcRef<T>, which represents a reference to a value                     able for the programs in the experiment, since they do not allocate
of type T that exists in a garbage-collected portion of the heap.                       enough memory to require collection. We think it is unlikely that
GcRef<T> implements the Deref trait, so the * operator can be used                      a full, performant implementation would require changes to the
to obtain a reference to the underlying value. If one has a mutable                     design, since the work that remains should be beneath the interface.
GcRef<T>, the reference can be used to mutate the value. GcRef::new(v)                      While this paper was under review, we found that GcRef’s as_ref
moves value v into the garbage-collected portion of the heap and                        and as_mut methods could be abused to create multiple mutable &
generates a GcRef pointing to it.                                                       references to GC objects, breaking Rust’s invariant of allowing only
     ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                            Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


 1         pub struct IntContainer { n : i32 }                                  1       #[ derive ( Trace , Finalize ) ]
 2                                                                              2       pub struct IntContainer { n : i32 }
 3         pub fn set (c: & Rc < RefCell < IntContainer > > , n : i32 ) {       3
 4           let mut m = c . borrow_mut () ;                                    4       pub fn set ( mut c : GcRef < IntContainer > , n : i32 ) {
 5           m.n = n;                                                           5         c.n = n;
 6         }                                                                    6       }
 7                                                                              7
 8         pub fn make_two_references () {                                      8       pub fn make_two_references () {
 9           let c1 = Rc :: new ( RefCell :: new ( IntContainer { n : 42}) ) ; 9          let c1 = GcRef :: new ( IntContainer { n : 42}) ;
10           let c2 = c1 . clone () ;                                          10         let c2 = c1 ;
11           // c1 and c2 both reference the same object .                     11         // c1 and c2 both reference the same object .
12                                                                             12
13           set (& c2 , 42) ;                                                 13           set ( c2 , 42) ;
14           set (& c1 , 43) ;                                                 14           set ( c1 , 43) ;
15           // Now both reference an object with value 43.                    15           // Now both reference an object with value 43.
16         }                                                                   16       }

         (a) Two mutable references to a value using interior mutability.                    (b) Two mutable references to a value using Bronze.

     Figure 1: A comparison of mutable aliasing with and without Bronze. The interior mutability version (left) requires manually
     borrowing a mutable reference to the contents of the RefCell (line 4). Then, the reference count must be manually incremented
     via clone (line 10). With Bronze (right), no borrowing is needed (line 5) and a second reference can be obtained with plain
     assignment (line 10). The Trace and Finalize traits needed for GCed objects can be derived automatically (line 1).


     one mutable reference to an object. The Deref trait implementation             3.1      Tasks
     on GcRef could be abused in the same way. Section 4 describes how              We devised a multi-part programming assignment for our study.
     we obtained soundness in a revised version of Bronze and why we                The specification of each part differed slightly depending on
     believe the changes, although slightly reducing usability, do not              whether participants should use GC or traditional Rust; we label a
     have a significant impact on our results.                                      task with subscript GC or noGC to clarify this, as needed.
        Why is Bronze easier to use than interior mutability? We believe               The Basics task, carried out using traditional Rust, focused on
     that the primary cause is that Bronze allows free persistent (in-field)        the basics of Rust syntax. The Ownership task introduced owner-
     aliasing. These aliases can be obtained without using a separate data          ship and borrowing. This and later parts involve programming a
     structure (e.g., Rc) and without invoking a special method to obtain           simulation of turtles living on the university campus. The instruc-
     them (e.g., borrow). When references need to be passed in fields of            tions4 included:
     structures, the structures can be initialized and managed without
                                                                                    In turtle . rs , implement :
     explicitly manipulating the lifetimes of the references. In addition,          * `new ` function according to the given signature .
     GcRef<T> provides a unified interface compared to Rc<RefCell<T>>,              * Accessors ` walking_speed `, ` favorite_flavor `,
     which requires understanding two separate structures and how                     ` favorite_color `, and `name `.
     they can be used together. The distinction between these structures
                                                                                    Campus should maintain a vector (` Vec `) of turtles .
     can appear blurry to users due to Rust’s “Deref coercion” feature,               In campus . rs , implement methods :
     which means that programmers can omit * when dereferencing in                  * `new `: creates a new , empty Campus
     certain (but not all) cases. Finally, garbage collection works even            * `size `: returns the number of turtles on campus
     in the presence of cycles, which must be managed manually when                 * ` add_turtle `: adds a new Turtle to campus .
                                                                                    * ` get_turtle `: returns a reference to an turtle at a
     reference counting is used.
                                                                                        given index .
        Bronze is available on Cargo, the Rust package manager.2                    * ` turtles `: returns an iterator that a caller can use to
                                                                                        iterate through the turtles .
                                                                                    * ` fastest_walker `: Returns None if the campus is empty .
     3     METHOD                                                                       Otherwise , returns Some of a reference to the turtle
     We conducted an experiment in which we randomly assigned par-                      with the fastest walking speed .
                                                                                    * ` breed_turtles `, which uses the functions in ` genetics `
     ticipants to use either traditional Rust or Bronze when completing               to breed two turtles , resulting in a new Turtle .. . .
     a multi-part programming assignment. We measured their perfor-
     mance and surveyed them about their experiences. Complete task                    Every turtle has a name . Of course , as with people ,
     and survey materials are available in the artifact that accompanies               several turtles may have the same name . In campus .rs ,
                                                                                       implement ` turtles_with_name ` so that it returns a
     this paper.3 The study was approved by our IRB.
                                                                                       vector of turtles that have the given name .

                                                                                       Completing this part required understanding ownership trans-
                                                                                    fer (add_turtle), references (get_turtle), iterators (turtles), options
                                                                                    and borrowing (fastest_walker), and mutable vectors (add_turtle and
     2 https://crates.io/crates/bronze_gc
     3 https://doi.org/10.5281/zenodo.6045904                                       4 Instructions have been slightly edited for space.
Garbage Collection Makes Rust Easier to Use: A Randomized Controlled Trial of the Bronze Garbage Collector                   ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA


breed_turtles). In OwnershipnoGC , the get_turtle method of Campus                      Participants were free to withdraw from the experiment at any time;
returned a value of type TurtleRef<'a>, which was defined as &'a                        students who started the experiment but withdrew received 2.5%
Turtle. In OwnershipGC , TurtleRef was defined as GcRef<Turtle>.                        extra credit. Students who withdrew, or opted not to participate
   The Aliasing task introduced the requirement of multiple mu-                         at all, could complete any version of the assignment. Students had
table references. The instructions included:                                            the option of accepting random assignment and/or carrying out
Change `Turtle ` so that each turtle has a field that
                                                                                        surveys but not having their data included in our research analysis;
keeps track of its children in a `Vec `. `Vec ` of what ?                               we awarded extra credit independently of this choice. Only three
You ' ll have to figure that out . Do NOT store indices                                 students did not consent to their data being used.5
into the Campus ' s vector because those may change in
the future ( some day we may support removing turtles
from Campus ). Do NOT invent your own indexing scheme
                                                                                        3.3     Procedure
and store a map somewhere .                                                             The instructor gave lectures on programming in Rust during four
                                                                                        80-minute class periods over a period of two weeks (April 13–27).
If you breed two turtles , each parent should include
                                                                                        Lecture slides can be found in the paper supplement. The Basics
the child in its vector of children . In turtle . rs ,
implement methods :                                                                     task in the assignment overlapped with, and was due at the end of,
* ` num_children `                                                                      the second week of lectures (April 21–29). The remaining parts of
* ` teach_children `                                                                    the assignment were released on April 29 and were due May 11.
                                                                                            The README file for the Ownership and Aliasing tasks de-
Note that this task may require you to revisit some of
the decisions you made in Basics . You are welcome to
                                                                                        scribed the study in detail and linked to a Qualtrics survey, which
copy / paste implementations from your Basics work , but                                included a consent form and requested demographic information
note that some of the signatures are different ( in order                               from students who consented. The form also asked for their uni-
to facilitate the design changes you will need to make ) .                              versity ID number so that we could associate student grades with
                                                                                        participants. The Qualtrics tool randomly assigned participants to
Your previous implementation of ` turtles_with_name ` had
to do a linear search through the whole vector of                                       a condition (Bronze or Traditional) upon consent, emailing them
turtles. . . Improve the performance of ` turtles_with_                                 which condition they were assigned to. The email also contained
name ` by adding a cache to Campus. . .                                                 a personalized link to a survey to fill out after completing each
                                                                                        part of the programming assignment, allowing us to track which
    Campus needed a vector of turtles, each of which needed a vector
                                                                                        students had completed the surveys.
that had references to the same turtles referenced by Campus. Because
                                                                                            The course used a question-and-answer web site, Piazza [29], to
of breed_turtle, the turtles needed to be mutable. Finally, the cache
                                                                                        allow the students to ask questions about course content. Because
required returning collections that referenced the same turtles.
                                                                                        we had revised the Rust content relative to the prior semester, the
    For AliasingnoGC , these requirements could be addressed using
                                                                                        first author joined the teaching assistants (TAs) in answering ques-
reference counting and interior mutability. The get_turtle method of
                                                                                        tions about the assignment. We made sure to answer all questions
Campus, as in OwnershipnoGC returned a value of type TurtleRef, but
                                                                                        in a timely fashion with high quality. In addition, as a result of posts
TurtleRef was now a struct with fields that the participants needed
                                                                                        on Piazza indicating that students found the assignment difficult,
to define. TurtleRef, in turn, exposed a method borrow_turtle, which
                                                                                        the first author conducted live-coding demonstrations on May 6 and
returned a value of type BorrowedTurtle. BorrowedTurtle implemented
                                                                                        7.6 Demonstrations delved into topics covered in class, including
the Deref and DerefMut traits, allowing clients to obtain a temporary
                                                                                        Rc, RefCell, smart pointers, mutability, scope and borrowing, a com-
mutable reference. Participants were required to fill in the fields of
                                                                                        parison between GC and reference counting, string literals, interior
TurtleRef and BorrowedTurtle; a typical solution was Rc<RefCell<Turtle
                                                                                        mutability, mutable structs, lifetime specifiers, and Box. The Piazza
>> and RefMut<'a, Turtle>. This approach allowed external clients to
                                                                                        forum and live demonstrations were not separated by experimental
obtain references to Turtles that could be made temporarily mutable
                                                                                        condition, so these did not provide additional data about perceived
if needed for the application.
                                                                                        difficulty.
    In AliasingGC , TurtleRef is defined as GcRef<Turtle>, just as in
OwnershipGC —because GcRef supports mutation of the referenced
value, there is no need for additional structure.
                                                                                        4     LIMITATIONS
    Bronze participants were asked to complete task AliasingnoGC                        Students’ abilities to complete the assignment depended to some
after completing AliasingGC .                                                           extent on the quality of our instruction and the extent to which we
                                                                                        emphasized each topic. To help decouple our instructional design
3.2     Recruitment                                                                     from the experiment, we based our instructional materials on the
                                                                                        online Rust book [20] and leveraged materials that had been used
We recruited participants from the 633 students who were enrolled
                                                                                        successfully in previous editions of the course.
in a required, sophomore-level programming course. Our program-
                                                                                           Because the first author taught the live coding demonstrations
ming assignment was part of the course’s grade, but participation
                                                                                        and answered many student questions on Piazza, it is possible that
in the research was voluntary, and confirmed by informed consent.
                                                                                        this could have introduced bias. One of two course instructors is
Research participants were randomly assigned to use either Bronze
                                                                                        also a co-author, so there could have been bias in teaching as well,
or traditional Rust, and agreed to take a survey after completing
each part of the assignment. In doing so, they received extra credit                    5 Students were required to opt out if they were under 18 years old.

on the assignment—1% extra credit per survey, or 5% for all three.                      6 Student privacy regulations preclude us from sharing the videos of these demos.
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                    Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


since GC and interior mutability, which were taught in the course,           Component                                   Traditional       Bronze
were of interest in the study.
                                                                             Random assignment to condition              194               139
    Our study focused on programmers who are new to Rust; our
                                                                             Basics survey                               154               117
sample was of students. While professionals (many of whom are
                                                                             Ownership survey                            153               113
also new at Rust) would have more programming experience, prior
                                                                             Aliasing survey                             142               101
work [1, 23, 24] suggests that results with students corresponds
                                                                             AliasingGC survey                                             84
with results with professionals in related, but not identical, tasks.
    All times spent by participants were self-reported. Although we                      Table 2: Participation by component
asked participants to use a tool to track time spent for Ownership
and Aliasing, we did not confirm that they did so. However, any
noise or bias in reported times are likely to be consistent across
experimental conditions. Although we asked participants to com-
plete the surveys immediately after completing each part of the          of the cases. A small refactoring addressed these. One case that
assignment, some participants submitted the surveys in batches.          used an iterator required inserting a * operator to dereference the
    The extra credit incentive could have resulted in a non-uniformly    iterator’s returned reference.
selected sample. However, as we discuss in more detail in section 7,
the small difference in median class grade between participants and
                                                                         5     RESULTS
non-participants (90% vs. 87%) suggests that this does not result in
a significant threat to validity.                                        In this section, we describe the analysis we conducted. Anonymous
    More Bronze participants withdrew from the study than Tradi-         raw data as well as an RStudio script to analyze the data are included
tional participants (see section 7); the withdrawing Bronze partici-     in the artifact that accompanies the paper.7
pants may have been weaker, less industrious, or more risk-averse
than the students that remained, leaving a stronger overall Bronze       5.1     Participants
population compared to the traditional one. We believe the magni-        Of 633 students who were enrolled in the course, 385 students
tude of the difference in times between conditions (section 5.4) is      signed up for the experiment, with 190 assigned to use Bronze and
large enough that it cannot be explained by this possibility.            195 to Traditional. Of these, 41 withdrew; an additional 11 students
    All of the students worked on the assignment in the same time-       submitted code for both versions of the assignment. We did not
frame, so trends over time could have been due to external in-           analyze the data from those 52 students, leaving experimental data
fluences, such as stress caused by the approach of final exams.          from 333 students for analysis: 139 Bronze, and 194 Traditional.
However, these trends would have been equally applicable across             383 students completed 1120 surveys. 34 students submitted
experimental conditions.                                                 surveys but did not accept random assignment. 36 accepted ran-
    While this paper was under review, we found that GCRef was           dom assignment but did not submit surveys. Overall, 428 students
unsound for the reasons discussed in section 2. To make Bronze           participated in the study. Only the data from the 333 experiment
sound, we removed the Deref implementation, replacing it with new        participants were used in the analyses below, except for the overall
borrow and borrow_mut methods. These methods return objects whose
                                                                         demographics of the population and the analysis of whether GC
lifetimes are tracked dynamically, similar to RefCell’s borrowing        participants thought GC makes programming easier (section 5.5).
mechanism. We also removed the as_ref and as_mut methods, which          For each task, we analyzed the corresponding survey data, as shown
were only used in one of the student submissions.                        in Table 2.
    There is a risk that had the students used the corrected version        We asked students about their Rust experience. Of the 333 ex-
of GCRef, they might not have seen the same benefits. To under-          periment participants, 84 had read about Rust or talked to a friend
stand whether this might be so, we applied the corrected version of      about it. 12 had played with Rust on their own, two had used it on a
Bronze to a sample of student implementations; we believe that our       team, and three had used it in an open-source project. When asked
results would largely hold up, even if students had used this version.   to self-assess their prior level of Rust knowledge, 307 reported no
We manually modified student programs until we were confident            experience; 17 reported passing familiarity (maybe wrote a few
we had seen the relevant challenges; in doing so, we modified 43         lines of code); 6 reported a moderate amount or a lot of experience.
student submissions. Two changes were common: inserting calls               Figure 2 shows the distribution of course grades by decision to
to borrow or borrow_mut; and introducing local variables to extend       enroll in the experiment in superimposed violin and box plots. To
lifetimes of borrows. In the vast majority of cases, calling borrow or   test whether the decision to enroll was related to course grade, we
borrow_mut sufficed; this could be done automatically by a compiler,
                                                                         conducted a logistic regression. We found 𝑝 ≈ .017, with higher
similar to Deref coercion, which is already supported by the com-        grades being associated with choosing to enroll in the study. The
piler. Some cases required manipulating lifetimes with additional        odds ratio was 0.035 with a 95% confidence interval of [0.011, 0.057]
local variables or inserting curly braces, which is a common tech-       (𝑁 = 584), meaning that a 1-point increase in grade correlates with
nique in Rust. Rust programmers need to be able to do this already       multiplying the odds of enrolling by 𝑒 .035 ≈ 1.036.
(indeed, we taught this technique in our lectures). Two programs
manipulated in this way panicked due to multiple borrows after the
naive transformation above; both of these used match on something
that was borrowed, and then took a mutable reference inside one          7 https://doi.org/10.5281/zenodo.6045904
Garbage Collection Makes Rust Easier to Use: A Randomized Controlled Trial of the Bronze Garbage Collector                                               ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA


   100                                                                                                                OwnershipGC      3                          122

                                                                                                                    OwnershipnoGC      4                          172




                                                                                         Condition and part
    90                                                                                                                  AliasingGC           32                          93
                                                                                                                                                                                                      Complete
                                                                                                                       AliasingnoGC                80                         96                      Incomplete
    80                                                                                                             Overall—Bronze                       72                         53

                                                                                                              Overall—Traditional                  80                         96
    70                                                                                                                                0.00        0.25           0.50         0.75          1.00
                                                                                                                                                        Fraction of participants


    60
                                                                                        Figure 3: Fractions of participants who completed each part

    50
                                                                                                              70
                 Did not participate                 Participated                                                                                                                                   Participant’s
                                                                                                                                                                                                    condition
                                                                                                              60
                                                                                                                                                                                                        Bronze
                                                                                                              50
      Figure 2: Course grade by experiment enrollment                                                                                                                                                   Traditional




                                                                                         Hours
                                                                                        Hours
                                                                                                              40                                                                                           Bronze
                                                                                                                                                                                                           Traditional
                                                                                                              30
5.2      Analysis Methods                                                                                     20
We designed the overall experiment to allow us to examine the                                                 10
relationship between time spent and outcomes (grades and com-
                                                                                                               0
pletion); the association between testing practices, sources of help,                                                 Ownership          Aliasing            AliasingnoGC
                                                                                                                      GC  noGC          GC    noGC                noGC                  GCTotal
                                                                                                                                                                                             noGC
and editor selection and outcomes; and the effect of condition on                                              Task
                                                                                                                      Ownership         Aliasing                AliasingnoGC              Total
the amount of time and fun students predicted if they had done the
assignment in other languages, as well as the effect of condition on
                                                                                        Figure 4: Total reported time spent on parts after Owner-
amount and sources of help.
                                                                                        ship.
   In order to help us refine our list of hypotheses while ensuring a
sound data analysis, we randomly reserved data from 10% of the
participants for exploratory analysis. We visualized this exploratory                   the odds of finishing for participants who DID use Bronze. When
data and conducted statistical tests to identify interesting hypothe-                   considering probability of completing all parts, Fisher’s exact test
ses about the effects of garbage collection and other factors that                      indicated no significant difference between conditions (𝑝 ≈ .51).
might influence outcomes. From this exploration, we selected spe-
cific questions of interest and associated hypothesis tests. Finally,                   5.4                           Completion times
we discarded the reserved 10% and performed the planned tests on                        For tasks after Basics (i.e., after participants were assigned to con-
the remaining 90%. All results reported below are drawn from this                       ditions), we hypothesized that Bronze would enable participants
90%, except overall demographic information (e.g., participation                        to complete tasks faster. We analyzed the 149 participants who
rates), which is reported for the entire dataset.                                       finished all the tasks. For these tasks, a Shapiro-Welk normality
   Because we conducted multiple hypothesis tests, we interpret the                     test found a likely violation of normality of the completion times
results with a Holm-Bonferroni correction [17]. All of the reported                     (𝑝 < .001). Therefore, we conducted nonparametric Wilcoxon tests
p-values are corrected and can be compared directly with 𝛼; we set                      rather than ANOVA tests. Figure 4 shows the total times reported
𝛼 = 0.05 in our interpretation.                                                         across the conditions. Figure 4 excludes the Basics task, since that
                                                                                        task preceded assignment to conditions and because we only asked
5.3      Completion rates                                                               participants to start tracking their time after the Basics task was
We wanted to know whether Bronze participants were more likely                          complete. Nevertheless, we asked participants to estimate how long
to finish either individual parts of the assignment or the assignment                   they spent on the Basics task, and they reported a mean of 3.5 hours
as a whole. We conducted Fisher’s exact tests to compare comple-                        (SD ≈ 3 hours). Task AliasingnoGC is not compared to any other
tion rates (rates of scoring 100%) on each part of the assignment                       task; instead, we leverage it for computing the total time spent on
across conditions. This analysis concerns 301 of the 333 total ex-                      all tasks (column “Total” in Figure 4).
periment participants, which omits the 10% of the participants that                         We did not find a significant difference in Ownership time
were withheld for exploratory analysis. Completion rates of each                        (𝑊 = 2449.5, 𝑝 ≈ 1). However, Bronze participants finished Alias-
part are shown in Figure 3. For Ownership, we found no significant                      ing significantly faster (median = 4 hours) than Traditional Rust par-
difference in completion rate (𝑝 ≈ 1.00). Comparing AliasingnoGC                        ticipants (median = 12 hours) (𝑊 = 561, 𝑝 < .001). We did not find a
(Traditional) and AliasingGC , we found that Bronze users were                          significant difference in total completion time (𝑊 = 2354.5, 𝑝 ≈ 1).
significantly more likely to score 100% (𝑝 ≈ .006). The odds ra-                            We also compared completion times spent by participants who
tio was approximately 0.41, indicating that the odds of finishing                       did not finish. A Wilcoxon rank sum test found no significant dif-
for participants not using Bronze were approximately 0.41 times                         ference (𝑊 = 829, 𝑝 ≈ 1). We also compared times reported by
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                                   Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


                                                         Strongly disagree                  OwnershipnoGC                                     N=153
      Basics                                     N=151
                                                         Somewhat disagree
                                                                                              OwnershipGC                                     N=112     Dislike a lot
OwnershipGC                                      N=139   Neither agree nor disagree
                                                         Somewhat agree                        AliasingnoGC                                   N=142     Dislike somewhat
  AliasingGC                                     N=122                                                                                                  Like somewhat
                                                         Strongly agree                         AliasingGC                                    N=99
 AliasingnoGC                                    N=102                                                                                                  Like a lot
                                                                                      AliasingnoGC (Bronze)                                   N=83
            0.00    0.25    0.50      0.75   1.00
                           Fraction                                                                       0.00     0.25    0.50      0.75   1.00
                                                                                                                          Fraction


Figure 5: Agreement with “GC in Rust makes writing pro-
grams easier” (Bronze participants only).                                             Figure 6: Amount participants reported liking Rust on a 4-
                                                                                      point Likert scale. AliasingnoGC (Bronze) indicates that task
                                                                                      done by Bronze participants.
participants who scored 100% to times by participants who did not,
finding no significant difference (𝑊 = 5675, 𝑝 ≈ 1).
   Figure 4 also shows the distribution of times for AliasingnoGC                     We asked a corresponding question asking about prediction of fun
when completed by Bronze participants. The median time was 8                          compared to Rust. Responses were on a five-point Likert scale, with
hours (mean = 9.9, 𝑆𝐷 = 8.4). The difference between medians of                       an additional “I’m not familiar enough with this language to judge”
Aliasing times across conditions was also 8 hours, explaining why                     option. We asked about C, C++, Java, and Python. Our exploratory
we did not find a difference in total time spent across conditions.                   data analysis led us to hypothesize that the relationships were weak,
                                                                                      if they could be found at all. The strongest relationship appeared to
5.5      Does GC make writing programs easier?                                        be with prediction of time in C, and we hypothesized that Bronze
If users feel that GC makes programming easier, then including                        participants would estimate longer times in C than the non-Bronze
GC in a language might improve language adoption rates. We were                       participants, since they would be more aware of the cost of manual
interested in how Bronze participants’ opinions of GC changed                         memory management.
while using it. Responses to our question about whether GC makes                          To compare predicted time in C across the two conditions (for
programs easier were on a Likert scale with a 0 to 4 point range,                     which we received 864 responses from people familiar enough with
with 4 indicating a strong belief that GC made programming easier.                    C to answer), we used an ordinal regression mixed model. This
Median scores were 2 after Basics and 4 after AliasingnoGC . Thus,                    approach accounted for the fact that we asked the same question
after trying the assignment with and without GC, they recognized                      of each participant after completing each part of the assignment.
a strong benefit of GC. An ordinal regression yielded 𝑝 < .001 (odds                  We found no significant difference (𝑝 ≈ 1).
ratio 21.4), indicating a significant effect of doing the assignment on
beliefs about GC helpfulness. Figure 5 illustrates how participants’                  5.8     Correlations among opinions
beliefs about GC changed over time.                                                   To improve adoption of a language, it might be useful to understand
                                                                                      what factors of a programmer’s experience correlate with liking a
5.6      Liking Rust: comparison between                                              language. After participants completed each part of the assignment,
         conditions and over time                                                     we asked them how much stress, time, intellectual challenge, and
We hypothesized that if Bronze helped participants complete tasks                     frustration they experienced compared to their expectation, as well
faster, Bronze participants might like Rust better than Traditional                   as how much they liked Rust. We analyzed the correlations among
participants. Each survey asked: “How much do you like Rust?”                         feelings about Rust and other aspects of participants’ experiences.
on a four-point Likert scale (we omitted a neutral option in order                    Figure 7 shows the pairwise correlations. For the time metric, we
to force expressing a preference). Figure 6 shows the responses.                      asked participants to compare the amount of time they spent to
We conducted an ordinal regression to assess whether there was a                      the amount of time they expected to spend; we asked this question
difference in Likert-scale responses across conditions after experi-                  rather than using the reported times in order to focus on partici-
ment participants were finished with the project (including those                     pants’ feelings about time. Stress, time, intellectual challenge, and
who did not score 100%). We found 𝑝 ≈ 1, indicating no significant                    frustration appear to be strongly correlated, and assessments of
effect of GC on liking Rust by the end of the assignment. We also                     whether participants like Rust are moderately correlated with stress
compared responses to this question after Ownership; the ordinal                      and frustration.
regression gave 𝑝 ≈ 1, also indicating no significant difference.
                                                                                      5.9     Amount learned about Rust
5.7      Estimated time and fun in other languages                                    After completing each part of the assignment, we asked participants
We were interested in how usage of Bronze might impact beliefs                        how much they felt they learned about various topics in Rust. Fig-
about time required in other languages, since a high estimate of                      ure 8 shows the results for ownership and borrowing. The amount
time in another language might correlate with a higher chance of                      participants reported learning in each part of the assignment does
choosing Rust, and since a good experience with GC might lead                         not appear to depend on whether participants used Bronze.
to higher estimates in languages that do not provide GC. In each
survey, we asked participants: “Suppose you had done this part of                     5.10       Factors influencing grades
the assignment in a different language instead. How much time                         Factors other than usage of Bronze may affect success; we hoped
would it have taken in THAT language compared to using Rust?”                         to understand what factors were relevant. In our exploratory data
Garbage Collection Makes Rust Easier to Use: A Randomized Controlled Trial of the Bronze Garbage Collector                                   ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA


                                                                                                               a significant correlation only with grade (𝑝 < .001, adjusted 𝑟 2 =




                                   t




                                                                   n
                                 en



                                                e



                                                                tio
                                              ng
                               sp




                                                              ra
                                           lle




                                                                           ss
                             e
                                                                                                               0.2465, 𝑁 = 864). However, when predicting grades for Aliasing




                                                            t
                                                         us
                                         ha




                                                                         re
                            m




                                                        Fr



                                                                        St
                          Ti



                                        C
                                                                                      1
                                                                                                               only (both GC and non-GC, with grades re-scaled from 0 to 100%),
         Like Rust                                                                   0.8                       we found that time spent and course grade were both significant
                         −0.33      −0.38             −0.43        −0.44
                                                                                     0.6                       predictors (𝑝 < .001 for both factors). The model for Aliasing
                                                                                     0.4                       explained 20.9% of the variance in grades (𝑟 2 ≈ .209).
                  Time spent            0.64           0.71            0.66          0.2
                                                                                      0                        6   QUALITATIVE ANALYSIS OF RESPONSES
                                 Challenge                                           −0.2                      The surveys included two free-response questions: “What aspects of
                                                       0.72            0.71
                                                                                     −0.4                      this part of the assignment did you find most difficult?” and “What
                                                                                     −0.6                      should we change about the class to help future students understand
                                                Frustration            0.8                                     the concepts in Rust better?” Although not all participants tried both
                                                                                     −0.8

                                                                                     −1                        conditions, their subjective experiences with only one condition can
                                                                                                               provide insights about their experiences as well as help understand
Figure 7: Correlations among participants’ assessments of                                                      factors that may relate to their future decisions about programming
their experiences.                                                                                             tools. To analyze the data, we conducted a thematic analysis [6].
                                                                                                               A single domain expert inductively developed the codebook and
                                                                                                               coded all responses, in consultation with the research team. Because
       OwnershipnoGC                                                         N=153
         OwnershipGC                                                         N=112        Already understood
                                                                                                               answers to the two questions overlapped, we analyzed all responses
          AliasingnoGC                                                       N=142        Learned nothing      together. We were interested in gleaning insights about language
                                                                                          Learned a little     design as well as pedagogy from the responses.
           AliasingGC                                                        N=100        Learned a lot
 AliasingnoGC (Bronze)                                                       N=83

                        0.00     0.25          0.50      0.75          1.00
                                                                                                                   References, lifetimes, ownership among the most challenging as-
                                            Fraction                                                           pects. We received 1,143 comments on challenges that participants
                     (a) Amounts learned about ownership                                                       faced. 340 pertained to references, of which 204 were about lifetimes.
      OwnershipnoGC                                                      N=152
                                                                                                               116 comments indicated syntax had been challenging. 100 men-
        OwnershipGC                                                      N=112            Already understood
                                                                                                               tioned interior mutability, 83 dynamic borrowing, and 70 mutability.
         AliasingnoGC                                                    N=142
                                                                                          Learned nothing          Consistent with earlier reports [12, 34], 199 participants reported
                                                                                          Learned a little
          AliasingGC                                                     N=98             Learned a lot
                                                                                                               that ownership was challenging; 76 such reports were about borrow-
AliasingnoGC (Bronze)                                                    N=82                                  ing. One student, after finishing AliasingGC , reported: “Learning
                     0.00        0.25       0.50        0.75           1.00                                    rust ownership is like navigating a maze where the walls are made
                                          Fraction
                                                                                                               of asbestos and frustration, and the maze has no exit, and every
                     (b) Amounts learned about borrowing                                                       time you hit a dead end you get an aneurysm and die.” A Tradi-
                                                                                                               tional student reported: “Coding with ownership rules and trying
Figure 8: Amounts learned after each part of the study.                                                        to implement mutability, in general, was just such a headache. It is
AliasingnoGC (Bronze) indicates that task done by Bronze                                                       like someone had combined the worst part of C and Java.”
participants.                                                                                                      AliasingnoGC required designing structures that supported dy-
                                                                                                               namic borrowing — a borrowed reference whose safety was checked
                                                                                                               dynamically rather than statically. This required understanding the
analysis (on 10% of the data), we used a linear mixed-effects model                                            Rust Ref and RefMut structures, which dynamically track outstand-
to evaluate the relationship between methods that participants re-                                             ing borrows of cells. One participant explained the difficulty: “It
ported using and their assignment grades. We looked at time spent,                                             took me a long time to figure out the field types with the correct
sources of help, and choice of developing on their own machine or                                              lifetimes. . . Once I knew what the types were, it took me about an
on a server. Based on this, we hypothesized that course grade and                                              hour or two to figure out the rest of the functions. It was quite
development location might be significant factors. Students who do                                             confusing and frustrating figuring out how to use Rc and RefCell
the work on a department server may have less access to computing                                              in the right spots, and my initial approach did not use them nearly
resources or less skill at configuring systems. A linear regression                                            as much as my final solution did.”
found a significant positive correlation with course grade (𝑝 < .001,
adjusted 𝑟 2 ≈ .044, 𝑁 = 864) and that a 1-point increase in course                                               Error messages can help, but may not aid design or comprehension.
grade corresponded with a .692-point increase in assignment grade.                                             Although Rust’s error messages have a reputation for being high-
Development location was not a significant factor.                                                             quality [12] (one participant wrote “the Rust compiler pretty much
   Because course grade only explained a small amount of the                                                   just wrote the program for me”), the compiler cannot give high-
variance in assignment grade, we did additional exploration with                                               level design feedback. One GC participant explained: “When I was
the 10% withheld samples to identify a stronger predictor of grades,                                           testing my non-GC version, I’d never run into so many errors in
focusing on the whole assignment grade (rather than individual                                                 my life. When I tried fixing my errors, new ones just came up.
tasks). Returning to the remaining dataset, when predicting score on                                           I’ve heard students compare the debugging process for the non-
parts after Basics from hours spent and course grade, we found that                                            GC version to a never-ending game of whack-a-mole.” Another
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                   Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


reported: “Translating from GC to no GC was a nightmare. It wasn’t          have been a problem. However, because of the fundamental way
as simple as switching GcRef<Turtle> to Rc<RefCell<Turtle>> because         ownership is used in Rust, much of the code required understanding
of the new structs. Figuring out the typing of the structs along            ownership and borrowing even with GC. In this assignment, GC
with debugging all the mutable references errors that resulted took         primarily served to aid situations that involved multiple references
hours and even some of the TAs couldn’t help me.” Error messages            to values. As Figure 8 shows, participants reported learning similar
could also lead to working code without teaching the programmer             amounts about these critical topics across conditions.
what was wrong: “Getting weird errors that I still don’t understand
but just fixed by listening to the compiler.”                                  Most of the benefit of GC comes from architectural simplification.
   Error messages also tend to give local advice that does not neces-       Participants reported that the architectural requirements in Alias-
sarily lead the user in the right direction. One participant reported       ingnoGC were extremely challenging; it is likely that the design
“error messages were cyclical with things like remove & then after          was a significant contributor to the difference in performance be-
removing try adding &.” Three participants said it was possible to fix      tween non-Bronze and Bronze participants. In particular, although
errors by following instructions without understanding what was             Bronze participants only needed to return GC references, Tradi-
going on. A higher-level error management approach, and better              tional Rust participants participants needed to fill in TurtleRef and
integration into an IDE (e.g., with visualizations [16]), could help.       BorrowedTurtle structures, which required additional design insight.
                                                                            The challenge posed by this design was apparent in the survey
   Garbage collection avoids mutability problems. We received 103           responses, in which 100 comments pertained to interior mutability
comments regarding garbage collection. 28 asked us to explain GC            and 83 to dynamic borrowing (almost as many total as the 199 who
more thoroughly. 43 said they had a hard time understanding GC.             complained about ownership or borrowing). We conclude that a
However, some Bronze participants observed, after finishing the             significant part of the benefit of GC in Rust programs is the archi-
assignment, that GC had been very helpful. One reported: “After             tectural simplifications it enables and promotes.
doing this part, I actually realized the power of garbage collection.
Using RefCell and Rcs to create interior mutability, etc. is so hectic. I      Participants and non-participants were comparable. We were sur-
would always prefer GcRef! Technically Rc<RefCell<T>> acts like GcRef       prised that students with higher grades were more likely to enroll;
but much more work!” Another participant said: “Understanding               we had expected students with lower grades would be more incen-
references, lifetimes, and mutability without garbage collection is         tivized by the extra credit. Perhaps students with higher grades
very difficult. It is not intuitive or understandable without GC.”          were more willing to accept the additional work of participating,
   Free copying of GC references appeared to be critical to the help-       or perhaps those students care more about even small grade boosts.
fulness of GC. One participant said: “The transition from garbage           However, the difference in median course grade between partici-
collection to non-gc was rough. I think the garbage collection was          pants and non-participants (90% vs. 87.0%) was small enough that
as easy as it was because it implemented the Copy trait. My most            we believe that our results likely generalize to the entire class.
common error in this project was the one where a certain variable
was moved because it was of a type that didn’t implement copy. If              Students would have benefitted from more time to complete the
not for some TA help, I would have been completely lost.”                   assignment. The students were motivated by grades to complete
                                                                            the assignment, but nearly half of students in both conditions did
   Students wanted more time and more examples to support learn-            not finish it (Figure 3). Some students reported that they wished the
ing. We received 715 comments regarding the course design, as-              work had been assigned over a longer period of time or earlier in
signments, lectures, and recitations. Participants reported that the        the semester (further from exams). The median participant spent 15
Aliasing task was extremely challenging, and that previous parts            hours on the experiment, which is a bit high for a 12-day homework
of the assignment left them unprepared for it. 182 comments asked           assignment, and some participants spent significantly more time. If
us to revise the project design or clarify the specifications.              we had allocated more time for the assignment and given it earlier
   190 comments asked for a longer, more complete treatment of              in the semester, perhaps more students would have finished.
Rust in future versions of the course. 54 asked for an intermediate-
level assignment. One participant put the steep learning curve                 Withdrawals were mostly assigned to Bronze. Of the 41 with-
(despite splitting the work over multiple parts) as follows: “I think       drawals, 40 had been assigned to use Bronze. Eight withdrew within
having this . . . project is a bit steep. I felt like I was being thrown    20 minutes of signing up, suggesting they did not make a serious
into a big steaming wok.” In particular, students requested more            attempt before switching. When withdrawing, 24 students reported
or more detailed examples (74), more or continued live coding               that they felt the non-GC version would be easier, perhaps because
demonstrations (35), and more discussion sections (31).                     the GC version required completing an additional part of the as-
                                                                            signment. Six said they didn’t understand GC well enough or that
7    DISCUSSION                                                             it was poorly documented. Eleven students gave no explanation.
                                                                               We suspect the withdrawal rate would have been lower if we
We discuss key takeaways and lessons learned from our experiment.
                                                                            could have convinced participants that they were likely to spend
   Even with GC, Rust learners need to understand ownership, bor-           the same amount of time total regardless of which condition they
rowing, and lifetimes. When designing the experiment, we were               picked. Of course, this approach may not be practical in situations
concerned that using GC would allow participants to avoid learning          where the expected times are not yet known. Future experiments
about ownership, borrowing, and lifetimes. Because we were hop-             could provide incentives that depend on time spent; our design
ing Bronze would be an aid to learning traditional Rust, this might         incentivized unbiased time reporting.
Garbage Collection Makes Rust Easier to Use: A Randomized Controlled Trial of the Bronze Garbage Collector                 ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA


    Encouraging adoption of safer languages by reducing stress. The                        Cyclone [14] integrated region-based memory management [30],
apparent decrease over time in how much students like Rust (Fig-                        including an optional garbage collector, into a safe dialect of C. Later
ure 6) suggests that if one wants to encourage Rust adoption,                           extensions included support for ownership and borrowing [27].
changes to the assignment design are needed. It would appear                            Case studies found that similar performance could be obtained if
that the Aliasing task had the largest influence on (dis)liking Rust.                   the GC was used judiciously, but that GC can have a significant
    It might be surprising that Bronze participants did not like Rust                   performance cost if used globally.
any better than Traditional Rust participants after AliasingGC ,
which Bronze participants completed in about a third of the time                        9    CONCLUSIONS AND FUTURE WORK
of Traditional Rust participants. We observed that stress and frus-                     We developed Bronze, a new library-based GC whose goal is to
tration correlate more closely with liking Rust than whether the                        ease the learning and use of Rust. We carried out a randomized,
task took longer than participants expected. Expectancy-value the-                      controlled trial of Bronze that showed that it can significantly alle-
ory [33] suggests that an expectation of success contributes to                         viate some of the challenges posed by the Rust aliasing restrictions
people’s motivation in doing tasks. The theory might suggest that                       for Rust beginners: Bronze participants completed a task that re-
if we want to encourage adoption of Rust and other safe languages,                      quired a complex aliasing structure in about a third as much time
it is more important to provide users with a consistent feeling of                      as traditional Rust participants. GC may enable Rust programmers,
progress rather than focusing on minimizing total task completion                       particularly beginners, to complete tasks in much less time.
time. Predictability is beneficial for practicing software engineers                       We hope to extend the collector to trace arbitrary objects that
as well as for students, and language adopters must first learn the                     may transitively contain references to GC objects. We would like
language before using it in a project, so this emphasis is valuable                     to investigate the impact of using GC not just for complex alias-
in practice as well as in education.                                                    ing scenarios, but to mitigate the impact of ownership in general;
                                                                                        perhaps doing so could flatten the learning curve and help users
                                                                                        feel more positively about Rust. We would also like to relax the
                                                                                        single-thread assumption in the collector, which would likely entail
8    RELATED WORK                                                                       changing from the shadow stack GC8 that is currently in use.
Empirical studies have been used to study several programming                              The experiment is the first (to our knowledge) evaluating the
language design questions, such as static typing [15], lambdas in                       usability benefits of GC. We focused on using GC to relax alias-
C++ [31], immutability features [10], and typestate [8]. Qualitative                    ing restrictions, but GC can also be used to avoid the challenges
studies have also been used to understand what factors contribute                       of reference counting and manual memory allocation. In the fu-
to users’ perceptions of languages [9]. This is the first empirical                     ture, library-based garbage collection could be used to evaluate the
study of the usability of garbage collection of which we are aware.                     usability tradeoffs of garbage collection in other contexts as well.
    Some work investigated how Rust is used in the wild. Astrauskas
et al. investigated the use of the unsafe keyword [3], finding that                     ACKNOWLEDGMENTS
much code relies on unsafe. Fulton et al. [12] conducted a survey and                   We appreciate Dan Votipka’s feedback on drafts of this paper, as
interviews of Rust programmers to understand their motivations                          well as the feedback from the anonymous reviewers. We thank
for adopting or not adopting Rust, finding that programmers are                         Alan Jeffrey, Manish Goregaokar, Felix Klock, and Philip Reames
motivated by the safety benefits but concerned about the learning                       for insightful discussions regarding garbage collection and Rust. We
curve and challenges in hiring experienced Rust programmers.                            also thank those who piloted the experimental materials, including
    Other GCs for Rust include rust-gc [13], Shifgrethor [4], and                       Michael Dong, Aaron Eline, and the course TAs, who supported the
Josephine [18], which require manual specification of roots.                            experiment while it was running. Finally, we appreciate the helpful
Josephine is for implementation of JavaScript in Rust. Shredder [25]                    design suggestions and guidelines from our IRB. This material is
supports concurrency, unlike Bronze, but accessing a GC object                          based upon work supported by the National Science Foundation
requires obtaining a guard to prevent concurrent access. It manages                     under Grant No. 1801545. Any opinions, findings, and conclusions
roots automatically by keeping a global list of all allocations. As                     or recommendations expressed in this material are those of the
a result, references do not implement the Copy trait and therefore                      author(s) and do not necessarily reflect the views of the National
cannot be copied freely as they can in Bronze.                                          Science Foundation.
    Meyerovich investigated programming language adoption [22];
developers reported preferring more-expressive languages. Because
adding optional garbage collection allows developers to express
different kinds of aliasing structures than does Rust alone, adding
GC to Rust might make it more likely to be adopted. Zeng and
Crichton [35] investigated forum posts about Rust adoption, hy-
pothesizing that adoption barriers for Rust included poor tool pub-
licity, difficulty solving complex aliasing problems, and integration
challenges with existing contexts. GCs, such as Bronze, may help
make it easier for programmers to solve complex aliasing problems.
    RustViz [21] is a visualization tool that may help programmers
learn Rust ownership semantics.                                                         8 https://llvm.org/docs/GarbageCollection.html#the-shadow-stack-gc
ICSE ’22, May 21–29, 2022, Pittsburgh, PA, USA                                                                       Michael Coblenz, Michelle L. Mazurek, and Michael Hicks


REFERENCES                                                                                 [26] Stack Exchange, Inc. 2020. Developer Survey Results.             https://insights.
 [1] Yasemin Acar, Christian Stransky, Dominik Wermke, Michelle L. Mazurek, and                 stackoverflow.com/survey/2020#technology-most-loved-dreaded-andwanted-
     Sascha Fahl. 2017. Security Developer Studies with GitHub Users: Exploring a               languages-loved
     Convenience Sample. In Thirteenth Symposium on Usable Privacy and Security            [27] Nikhil Swamy, Michael Hicks, Greg Morrisett, Dan Grossman, and Trevor Jim.
     (SOUPS 2017). USENIX Association, Santa Clara, CA, 81–95. https://www.usenix.              2006. Safe Manual Memory Management in Cyclone. Science of Computer Pro-
     org/conference/soups2017/technical-sessions/presentation/acar                              gramming (SCP) 62, 2 (Oct. 2006), 122–144. Special issue on memory management.
 [2] Alfred V. Aho and Jeffrey D. Ullman. 1992. Foundations of Computer Science. W.             Expands ISMM conference paper of the same name.
     H. Freeman. http://infolab.stanford.edu/~ullman/focs.html                             [28] The Rust team. 2021. The Rust Programming Language. http://rust-lang.org/
 [3] Vytautas Astrauskas, Christoph Matheja, Federico Poli, Peter Müller, and Alexan-      [29] Piazza Technologies. 2021. Piazza. https://piazza.com
     der J. Summers. 2020. How Do Programmers Use Unsafe Rust?. In Object-                 [30] Mads Tofte and Jean-Pierre Talpin. 1997. Region-Based Memory Management.
     oriented programming systems, languages, and applications (OOPSLA). 27 pages.              Inf. Comput. 132, 2 (Feb. 1997), 109–176.
     https://doi.org/10.1145/3428204                                                       [31] Phillip Merlin Uesbeck, Andreas Stefik, Stefan Hanenberg, Jan Pedersen, and
 [4] Without Boats. 2019. Shifgrethor. https://github.com/withoutboats/shifgrethor              Patrick Daleiden. 2016. An Empirical Study on the Impact of C++ Lambdas
 [5] Hans-Juergen Boehm and Mark Weiser. 1988. Garbage collection in an uncoop-                 and Programmer Experience. In International Conference on Software Engineer-
     erative environment. Software: Practice and Experience 18, 9 (1988), 807–820.              ing (Austin, Texas) (ICSE ’16). ACM, 760–771. https://doi.org/10.1145/2884781.
 [6] Virginia Braun and Victoria Clarke. 2006. Using thematic analysis in psychology.           2884849
     Qualitative research in psychology 3, 2 (2006), 77–101.                               [32] Philip Wadler. 1990. Linear types can change the world. In Programming concepts
 [7] TiOBE Software BV. 2021. The TiOBE Index. https://www.tiobe.com/tiobe-index/               and methods, Vol. 2. 347–359.
 [8] Michael Coblenz, Jonathan Aldrich, Brad A. Myers, and Joshua Sunshine. 2020.          [33] Allan Wigfield and Jacquelynne S. Eccles. 2000. Expectancy–Value Theory of
     Can Advanced Type Systems Be Usable? An Empirical Study of Ownership,                      Achievement Motivation. Contemporary Educational Psychology 25, 1 (2000),
     Assets, and Typestate in Obsidian. In Object-oriented programming systems, lan-            68–81. https://doi.org/10.1006/ceps.1999.1015
     guages, and applications (OOPSLA ’20).                                                [34] Ashley Williams. 2021. Safety - DS3 Summit Talk. https://youtu.be/9bQgVlqwduY
 [9] Michael Coblenz, Gauri Kambhatla, Paulette Koronkevich, Jenna L. Wise, Celeste        [35] Anna Zeng and Will Crichton. 2018. Identifying Barriers to Adoption for Rust
     Barnaby, Joshua Sunshine, Jonathan Aldrich, and Brad A. Myers. 2021. PLIERS:               through Online Discourse. PLATEAU.
     A Process That Integrates User-Centered Methods into Programming Language
     Design. TOCHI 28, 4, Article 28 (July 2021), 53 pages. https://doi.org/10.1145/
     3452379
[10] Michael Coblenz, Whitney Nelson, Jonathan Aldrich, Brad Myers, and Joshua
     Sunshine. 2017. Glacier: Transitive Class Immutability for Java. In International
     Conference on Software Engineering (ICSE ’17). IEEE Press, 496–506. https:
     //doi.org/10.1109/ICSE.2017.52
[11] Nick Diakopoulous, Mythili Bagavandas, Gurdeep Singh, Preeti Kulkarni, and
     Erico Guizzo. 2021. Top Programming Languages. https://spectrum.ieee.org/top-
     programming-languages/
[12] Kelsey R. Fulton, Anna Chan, Daniel Votipka, Michael Hicks, and Michelle L.
     Mazurek. 2021. Benefits and Drawbacks of Adopting a Secure Programming
     Language: Rust as a Case Study. In Seventeenth Symposium on Usable Privacy and
     Security (SOUPS 2021). USENIX Association. https://www.usenix.org/conference/
     soups2021/presentation/fulton
[13] Manish Goregaokar. 2021. rust-gc. https://github.com/Manishearth/rust-gc/
[14] Dan Grossman, Greg Morrisett, Trevor Jim, Michael Hicks, Yanling Wang, and
     James Cheney. 2002. Region-based Memory Management in Cyclone. In Pro-
     gramming Language Design and Implementation (PLDI ’02). ACM, 282–293.
[15] Stefan Hanenberg, Sebastian Kleinschmager, Romain Robbes, Éric Tanter, and
     Andreas Stefik. 2014. An empirical study on the impact of static typing on
     software maintainability. Empirical Software Engineering 19, 5 (Oct 2014), 1335–
     1382. https://doi.org/10.1007/s10664-013-9289-1
[16] Trent Hill, James Noble, and John Potter. 2002. Scalable Visualizations of Object-
     Oriented Systems with Ownership Trees. Journal of Visual Languages & Com-
     puting 13, 3 (2002), 319–339. https://doi.org/10.1006/jvlc.2002.0238
[17] Sture Holm. 1979. A Simple Sequentially Rejective Multiple Test Procedure.
     Scandinavian Journal of Statistics 6, 2 (1979), 65–70. http://www.jstor.org/stable/
     4615733
[18] Alan Jeffrey. 2018. Josephine. https://github.com/asajeffrey/josephine
[19] Steve Klabnik and Carol Nichols. 2018. RefCell<T> and the Interior Mutability
     Pattern, Chapter 15.5. In [20].
[20] Steve Klabnik and Carol Nichols. 2018. The Rust Programming Language. No
     Starch Press, USA.
[21] Gongming Luo, Vishnu Reddy, Marcelo Almeida, Yingying Zhu, Ke Du, and
     Cyrus Omar. 2020. RustViz: Interactively Visualizing Ownership and Borrowing.
     arXiv:2011.09012 [cs.PL]
[22] Leo A. Meyerovich and Ariel S. Rabkin. 2013. Empirical Analysis of Programming
     Language Adoption. In Object-oriented programming systems, languages, and
     applications (Indianapolis, Indiana, USA) (OOPSLA ’13). 1–18. https://doi.org/10.
     1145/2509136.2509515
[23] Alena Naiakshina, Anastasia Danilova, Eva Gerlitz, and Matthew Smith. 2020. On
     Conducting Security Developer Studies with CS Students: Examining a Password-
     Storage Study with CS Students, Freelancers, and Company Developers. In CHI
     Conference on Human Factors in Computing Systems (CHI 2020). 1–13. https:
     //doi.org/10.1145/3313831.3376791
[24] Alena Naiakshina, Anastasia Danilova, Eva Gerlitz, Emanuel von Zezschwitz,
     and Matthew Smith. 2019. "If You Want, I Can Store the Encrypted Password":
     A Password-Storage Field Study with Freelance Developers. In Proceedings of
     the 2019 CHI Conference on Human Factors in Computing Systems. 1–12. https:
     //doi.org/10.1145/3290605.3300370
[25] Others. 2021. Shredder. https://github.com/Others/shredder
