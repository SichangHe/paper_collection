Journal of Signal Processing Systems    (2026) 98:40
https://doi.org/10.1007/s11265-026-02011-x

    RESEARCH



Safety and Security Critical Systems with Rust
Malte Munch1 · Marcus Lindner2 · Johan Eriksson3 · Pawel Dzialo1 · Per Lindgren1

Received: 19 March 2026 / Revised: 31 July 2026 / Accepted: 12 August 2026
© The Author(s) 2026, modified publication 2026


Abstract
Rust is a modern systems level language with built in safety features providing strong guarantees to memory safety and
defined behavior. In this work we identify challenges and opportunities for adopting Rust in the context of safety-critical
systems. In particular we focus on software safety and security requirements akin to ISO 26262, IEC 61508, and ISO/
SAE 21434. We discuss Rust based development in relation to commonplace C/C++ software design and validation pro-
cesses. Furthermore we compare two distinct system categories: hosted and bare-metal systems and which opportunities
and challenges developers face in the context of safety and security certification in each of them.

Keywords ISO 26262 · Software certification · Software security · Cybersecurity · Security certification · Rust ·
MISRA C · Memory safety · DO-178C · ISO/SAE 21434 · Linux · libc · AUTOSAR · Coding guidelines



1 Introduction                                                               the usage of C/C++ and its confinement to subsets through
                                                                             guidelines is common and encouraged [1]. This seems to
Ensuring the functional safety of safety-critical systems,                   be insufficient as memory-related weaknesses, classes of
requires rigorous development processes. The increased                       vulnerabilities that can be completely evaded by the usage
connectivity of safety-critical systems, inevitably brings                   of a memory-safe programming language, still rank high
cybersecurity concerns into attention. Confidentiality, integ-               (Out-of-bounds Write (2nd), Out-of-bounds Read (6th), Use
rity, and availability of information is no longer confined,                 After Free (8th)) in the 2024 CWE Top 25 Most Dangerous
but extends beyond the physical perimeters of the system. It                 Software Weaknesses [2].1
can be argued that traditional development processes based                      In 2024, the Biden White House Administration stressed
on C/C++ language subsets and guidelines no longer suffice                   the need to act and mentioned the Rust language as a prom-
due to their unsafety. In traditional development processes                  ising alternative [4].
                                                                                In 2025, an independent group of 21 authors from aca-
                                                                             demia and industry also demanded action. They describe
     Malte Munch                                                             the presence of memory related vulnerabilities as endemic,
     malte.munch@ltu.se                                                      underpinning the analysis that this state is not going to
     Marcus Lindner                                                          change unless a systemic shift happens [5].
     marcus.lindner@scania.se                                                   The european union is responding as well; by releasing
     Johan Eriksson                                                          legislation targeting digital connected devices in the cyber
     johan.eriksson@grepit.se                                                resilience act (CRA) [6] and critical infrastructure in the
     Pawel Dzialo                                                            NIS 2 Directive [7]. Though not specifically focusing on
     pawel.dzialo@ltu.se                                                     the intersection of safety and security critical systems these
     Per Lindgren                                                            developments show the emerging awareness for the need to
     per.lindgren@ltu.se                                                     act across the broad spectrum of cybersecurity.
                                                                                These developments are increasingly reflected in the
1
     Department of Computer Science, Electrical and                          industry with major car manufacturers starting consortia
     Space Engineering, Luleå University of Technology,
     Laboratorievägen 14, Luleå 97187, Norrbotten, Sweden
2
     Scania AB, Luleå, Sweden                                                1
                                                                               The 2025 Edition does not look much different: Out-of-bounds
3
     Grepit AB, Luleå, Sweden                                                 Write (5th), Out-of-bounds Read (8th), Use After Free (7th) [3].
    40    Page 2 of 12                                                            Journal of Signal Processing Systems         (2026) 98:40


and reporting first adoptions of Rust in automotive develop-               While the mentioned standards are typically not mandated,
ment [8, 9].                                                               they have gained wide adoption towards product certifica-
   Introductions to Rust, also in the safety-critical and                  tion3 in respective domains and serve to establish compa-
embedded domain have previously been given in [10–12]. In                  rable levels of safety along the supply chain.
this paper, we identify a set of key challenges and opportuni-                The ISO/SAE 21434 standard has been recently intro-
ties to Rust based development of safety and security critical             duced (2021), defining engineering requirements for
systems. We focus on safety and security requirements akin                 cybersecurity risk management in the context of road vehi-
to ISO 26262 and IEC 61508 as well as ISO 21434 in the                     cles[17]. A unique aspect of this standard is that it in practice
context of two distinct environments: hosted systems (e.g.                 is required for type approval through UNECE Regulation
Linux, but also AUTOSAR AP/QNX/VxWorks) and bare-                          155 [18]. ISO/SAE 21434 and UNECE R155 are turning
metal solutions (AUTOSAR CP/RTIC). We use dynamic                          points in standards and type approval as continuous updates
application loading and heap-allocations as the distinguish-               might become part of type approval which traditionally
ing factors between hosted and bare-metal solutions. Where                 has been a once-only process. This is a novelty in safety
bare-metal environments feature neither dynamic applica-                   and security standardization and the only correct way to
tion loading nor heap allocations via a standard library. That             address security, which has to take a dynamic, hostile envi-
means all code (operating system and application logic) is                 ronment into account (whereas with safety you can make
linked together in one step whereas in a hosted environment                static assumptions).4 Consequently, this shift in standardiza-
the hosting kernel is compiled and linked independent from                 tion will require new technical and organizational responses
the applications that it will execute during runtime.                      to adhere to the defined requirements. It will reshape the
   The paper is outlined as follows: Section 2, covers safety              development process of safety (and then security) critical
and security standards, the underlying problem with permis-                systems from develop once towards evolve continuously.
sible undefined behavior, attempted mitigations for C/C++                  The necessity for a system that carries out these continu-
(MISRA guidelines), and Rust (at language level). Section                  ous updates is already accounted for in UNECE R156 which
3 identifies a set of key challenges and opportunities using               describes the requirements for type approval of a System
Rust in safety-critical systems in comparison to C/C++ for                 Update Management System (SUMS) [19].
both bare metal systems (Section 3.1) and hosted systems
(Section 3.2). Section 4 is dedicated to the common obser-                 2.2 Undefined Behavior may Cause Demons to Fly
vation of increase in codesize over time [13] and if and how               out of your Nose
this affects Rust. In Section 5, we assess three commercially
available qualified-to-standards Rust toolchains along with                Languages like C/C++ have been developed with per-
recent industry developments regarding standardization of                  formance in mind, for which code generation guarantees
safety practices and coding guidelines for Rust.2 In Section               assume programs for which the behavior is defined. This
6 we elaborate on the identified opportunities, and propose                assumption allows the compiler to use undefined behavior
hardening of the Rust semantics to further improve reliabil-               for code optimization, producing highly efficient binaries.
ity and deducible properties of Rust applications.                         The downside is that the generated code exposes arbi-
                                                                           trary behavior (including demons flying out of your nose)
                                                                           along any path leading up to undefined behavior. This was
2 Background                                                               observed already in a Usenet:comp.std.c discussion
                                                                           in 1992 [20].
2.1 Safety and Security Standards                                             The C/C++ languages have undergone multiple revisions
                                                                           since 1992. In recent editions C++ started to add memory
Common standards used in the development of safety-crit-                   safety features (lifetime checks) similar to the ones of Rust
ical systems are the ISO 26262 series [1] (automotive) and                 described in Section 2.5. These are however additions,
IEC 61508 [14] (industrial). IEC 61508 originates as early
as 1998 whereas ISO 26262 was first introduced in 2011 as a
refinement of IEC 61508 for the road vehicle realm. Both are               3
                                                                             With product we talk about intermediate products such as an oper-
standards that define functional safety for equipment appli-                ating system, a library, a computing chip, RAM, complete devices,
cable throughout the lifecycle of safety-related systems. For               everything except an end product (brought to market by an original
                                                                            equipment manufacturer (OEM), which is subject of type approval,
other domains we find similar standards, e.g, DO-178C [15]                  where legislative requirements count
for aviation and IEC 62304 for medical equipment [16].                     4
                                                                             The only other feasible alternative would be to statically standard-
                                                                            ize attacks and attackers too, which is not capturing the real world
2
  This paper is not based on the latest edition of standards and current    scenario sufficiently; a non-exhaustive list of scenarios that have to be
 Rust documentation by SAE.                                                 taken into account is defined in Annex 5 of UNECE R155


13
Journal of Signal Processing Systems         (2026) 98:40                                                           Page 3 of 12   40


requiring toolchain switches, adoption and cleanup of leg-               half of them (95 out of 201) do not or only partially apply
acy code.                                                                when using unsafe Rust. For safe Rust only (62 of 201)
   The underlying problem of permissible undefined behav-                Rules apply fully or partially [22]. Reasons for Rules to not
ior still remains to this date. Memory unsafety (e.g., out               apply are for example different syntax: Octal notation ini-
of bounds array indexing, use-after free, double free, etc.)             tiated by a leading zero 0 in C can cause confusion, thus
are prominent and still highly prevalent examples, as men-               it is discouraged by MISRA C (in Rust it is 0o). Another
tioned in Section 1.                                                     reason is more sound language design: A match clause in
                                                                         Rust requires the conjunction of match arms to cover the
2.3 MISRA C/C++                                                          complete range of the type, thus eliminating the necessity of
                                                                         all MISRA Rules concerned with well-formed switch state-
The shortcomings and problems that come with the usage                   ments. A reason for Rules to continue to apply for Rust is
of the C/C++ programming languages are known and                         for example the danger of a stack overflow, which we will
acknowledged in the safety critical software domain. Yet                 discuss in Section 6.3.
those are (still) the most commonly used languages in the
safety critical and embedded field [21].                                 2.4 Rust
    MISRA C aims to reduce the risks that come with the
usage of the C programming language by providing guide-                  Rust is a modern systems level programming language seek-
lines that try to mitigate common sources of error or confu-             ing to address many/most of the issues of C/C++ brought
sion. The first published version of MISRA C stems from                  to attention by MISRA. To do so, Rust’s uses a fundamen-
April 1998, with the latest version being released in 2025               tally different approach to memory management, and a clear
[21]. The guidelines consist of 22 Directives and 201 Rules.             separation between safe and unsafe code. Further, it offers
The Directives are more coarse and targeted at the overarch-             zero-runtime-cost abstractions.
ing project scope, e.g., that all software must have corre-
sponding documentation stating its necessity (Directive 3.1              2.5 Memory Management
[21]). The Rules on the other hand describe more tangible
guidelines such that easily confusable characters such as ’1’            Safe Rust guarantees that each memory allocation has
and ’l’ are not allowed to be the distinguishing characters              exactly one defined owner. From the begin (allocation),
between variables.                                                       throughout the lifetime, all the way to the automatic deallo-
    Guidelines come with different strictness levels that                cation at the end. References are possible, either an infinite
define to which extent they have to be applied. The strictness           amount of read-only references or at most one that can also
levels are Mandatory, Required5, Advisory6, or Disapplied.               alter an allocation. These strict and simple rules, that are
Over 90% of the guidelines fall into either the Required or              enforced by the compiler (even in multi-threaded contexts),
Advisory case. Mandatory guidelines are compulsory, while                prevent race conditions. This source of undefined behavior
it is allowed to violate Required guidelines if the violation is         is completely eliminated in safe Rust.
documented and appropriately justified. Advisory guidelines
should be followed, a deviation does not need to be justified.           2.5.1 Dynamic Heap Allocations
Disapplied guidelines do not apply at all.
    MISRA C is suited for advising developers directly as                With ergonomics in mind, the std library of Rust makes
well as for developing tools that can automatically check                the assumption that allocations are infallible. However, in
whether code adheres to the MISRA Rules.7 MISRA C++,                     reality, memory is a finite resource, thus the underlying allo-
similarly provides guidelines for the use of C++ in safety-              cator may internally run Out Of Memory (OOM), with the
critical applications. MISRA C++ was first launched in                   only option to call into panic!, which is defined behavior
2008, its latest revision has been released in 2023.                     but may have catastrophic consequences for the reliability
    In its 2025 edition MISRA also released an Addendum                  of the running application. In Section 6.1 we will discuss
6 ranking the applicability of the guidelines when using                 possible mitigations.
the Rust programming language, classified by the usage of                   In case a reference to a resource becomes unreachable
unsafe. The Addendum mentions that for the Directives a                  (e.g., a variable t goes out of scope), Rust automatically
majority also applies to Rust whereas in the Rules almost                injects code calling t.drop(). This is a unique improve-
                                                                         ment of Rust compared to other memory-safe languages
5
    Guidelines are formulated with "shall"                               which use an unpredictable (from the application perspec-
6
    Guidelines are formulated with "should"                              tive) garbage collection process. In case of dynamic data
7
  Guidelines are either decidable or undecidable, in the latter case a   structures the drop implementation will de-allocate (and
 compliance can not be deduced programmatically.


                                                                                                                              13
 40     Page 4 of 12                                                    Journal of Signal Processing Systems     (2026) 98:40


re-cycle) the memory. However, Rust’s std library assumes            Dereferencing of raw pointers, calls of unsafe functions,
the underlying allocator to be incapable of de-allocating         reading or writing mutable static variables, implementation
cyclic data structures, with the consequence that Rust may/       of unsafe traits, and accessing fields of unions.
will leak memory (even in the case of purely safe code).             These actions can be used in cases where defined behav-
Based on that assumption, the programmer may from safe            ior can/should not be established by the Rust language and
code even instruct the compiler to voluntarily leak memory        compiler, for example:
Box::leak(x). The thinkable attack scenario is that
an (external) malicious actor triggers code that allocates        1. Interfacing the environment: e.g., calling into assembly,
and leaks repeatedly until system resources are exhausted            C/C++ (SP2), interacting with an underlying operating
(OOM). Arguably, the design decision is a missed opportu-            system (SP1/SP2), and/or accessing the underlying hard-
nity regarding the reliability of Rust, which we return to in        ware through memory mapped peripherals (SP1).
Section 6.2.                                                      2. Interfacing other, marked-as-unsafe, items: e.g., calling
   As mentioned above this describes behavior of the std             unsafe Rust-functions(SP2), and implementing unsafe
library. In Rust it is easily possible to develop applications       traits (SP4).
using no_std, turning off all dependencies on surrounding         3. Optionally, unsafe can be used to address limitations
libraries and external allocators, making it trivial to fulfill      of the current Rust compiler: e.g., copy free splitting of
the requirements for a bare metal system.                            arrays into non-overlapping slices (SP1).

2.5.2 Stack Allocations                                           The pivotal point, is that a developer has to explicitly opt-
                                                                  out of the strong guarantees that Rust provides. Defined
Rust assumes stack space allocations to be infallible. How-       behavior is the default, nothing that needs to be activated
ever, any occurrence of stack overflow leads to UB, invali-       or added through features, compiler additions, or third party
dating the integrity of the whole system. Hardware assisted       tooling.
Memory Protection may be used to prevent the system from
running into UB, but will not solve the reliability issue         2.8 Safe Zero-Runtime-Cost Abstractions
in context of critical applications. In Section 6.3, we will
return to the problem.                                            Being a systems level programming language, Rust shares
                                                                  domain specific requirements with C/C++, e.g., offering
2.6 Runtime Checks                                                low-level control and producing efficient, target-specific
                                                                  executables.
For cases out of reach by static analysis, the Rust compiler         This is achieved by building upon the existing optimizing
injects runtime checks (asserting the safety condition for        backend compiler infrastructure, by the LLVM project for
e.g., memory safety, bounds checking, division, etc.) in the      the code generation.
generated binary. In case safety conditions are violated at          Rust together with the optimizing LLVM backend pro-
run-time, the generated code calls panic! to terminate            vides zero-runtime-cost abstractions. This implies, that no
execution in a defined way. In this way, the code execution       execution overhead is to be expected besides the bare mini-
of safe Rust is guaranteed to almost never reach UB, thus         mum to uphold safety invariants.8 As an example, raw array
a leap-step improvement over C/C++. The obligation of             indexing typically implies run-time overhead (as memory
defined behavior lies with the Rust language and Rust com-        safety is validated at run-time), while iterator access can be
piler infrastructure, not with the developer, best practices or   proven safe at compile time. Thus, where applicable, using
third party tooling.                                              Rust abstractions, performance of the generated binary will
                                                                  be on par with an unsafe C counterpart, and indeed outper-
2.7 Unsafe Rust                                                   form any C implementation that enforces safety at run-time.
                                                                     Zero-runtime-cost abstractions can be used to provide
In contrast to C/C++, Undefined Behavior (UB) is only per-        safe Application Programming Interfaces (APIs) to code
missible for sections of code explicitly marked unsafe,           that internally uses unsafe code and thus bridging the safe
while for safe Rust, the compiler ensures defined behavior.       and unsafe worlds in a controlled manner. Contracts for safe
   This opt-out of the strict safety obligations of safe Rust     use can be enforced by the Rust type system, where attempts
allows five additional actions, also called unsafe superpow-
ers [23]:                                                         8
                                                                    In general zero-runtime-cost abstractions imply that high-level
                                                                   constructs (classes, wrapper functions, iterators, type templates,
                                                                   etc) will not incur any runtime overhead compared to its low-level
                                                                   implementation.


13
Journal of Signal Processing Systems       (2026) 98:40                                                              Page 5 of 12   40


- involuntary (bugs), and voluntary (attacks) - of misuse are             former scenario the challenge lies in addressing bad luck
rejected at compile time. A prominent example thereof is                  with more or less static probability of hazards, in the latter
the Rust standard library, which internally uses unsafe code,             responses to an attacker that actively tries to turn the odds
to bind to a libc implementation, for interacting with an                 against the system have to be found.
underlying operating system while providing safe APIs for                    In the following, we discuss challenges and opportunities
operating system services (I/O, memory allocation etc.).                  for two classes of critical systems: bare metal systems, and
    Other examples include a plethora of publicly avail-                  hosted systems.
able crates (Rust libraries) providing safe APIs (bindings)
to unsafe legacy C/C++ libraries. Together these provide a                3.1 Bare-Metal Systems
migration path towards Rust based development in almost
all domains (web, sound/graphics, compute, AI etc.). It is                In this category we find systems supported by linked-
even more encouraging from safety and security perspec-                   together, library-based (Real-Time) Operating Systems. For
tives to see the increasing number of native Rust crates to               the automotive domain, operating systems standards have
consistently reduce the need for dependencies to unsafe                   evolved (e.g., AUTOSAR CP) and are widely adopted. The
legacy code.                                                              AUTOSAR initiative was formed in 2003 by key Euro-
                                                                          pean automotive actors (BMW, Bosch, Continental, Mer-
2.9 Undefined Behavior in Rust                                            cedes-Benz, Siemens, and Volkswagen). Over the last two
                                                                          decades, AUTOSAR has grown to include US and Japanese
To summarize, the goal of safe Rust, is to ensure defined                 actors as core members, and gained world wide uptake [27].
behavior of the executing binary at all times.9 Exceptions to             In the industrial automation and avionics domains we see
guaranteed defined behavior are:                                          similar constellations, where qualified to standards operat-
                                                                          ing systems along with supporting infrastructure are widely
1. Unsafe code: The goal is to isolate code that needs to                 adopted.
   opt-out of the strict compiler checking into code small                   These standards are implemented by vendors who sell
   blocks that particularly scrutinized                                   their respective implementations (e.g. EB tresos OS [28],
2. Stack overflow: leads to undefined behavior, thus in that              MICROSAR Classic [29]). These typically provide safety
   perspective outside of the (current) Rust guarantees.                  manuals or guidelines which, when followed, uphold
3. Bugs/shortcomings in the Rust toolchain: A historic and                the criteria for safe/secure usage within the qualification
   now fixed example thereof were infinite loop constructs                domain. While legislations (e.g., Automotive type approval)
   without side effects being UB [24].                                    typically do not stipulate specifics (methods, tools and pro-
                                                                          cesses), vendors can build upon pre-qualified implemen-
                                                                          tations and processes when arguing safety and security of
3 Challenges and Opportunities                                            their products.
                                                                             Besides the aforementioned, functional correctness
Safety critical systems may vary largely in their topol-                  of the code needs to be argued, depending on the safety-
ogy and required Safety Integrity Level (SIL), moreover,                  criticality of the component in question. In cases where a
their overall safety is context dependent [25]. Historically,             formal specification exists, one may adopt different formal
safety and security could be treated in separation. Academic              verification techniques, where deductive verification using
research evolved into disparate disciplines with limited                  e.g., Frama-c [30] for programs written in C, and Creusot
overlap. With increased connectivity, a shift of paradigm is              [31] for programs written in the Rust can be done. If formal
required to cover the overlap between safety and security.                specifications might be lacking, deemed too complex, or are
As an example, Security Engineering author Ross Anderson                  not required, lighter weight alternatives such as (coverage-
started to teach security and safety in one course whereas                guided) fuzz-based testing [32], down to manual unit and
they have been two separate ones before [26]. The safety/                 integration based testing [33] can be used.
security overlap gives rise to new challenges. In contrast                   Non-functional requirements typically include real-time
to the safety domain where a system must be fault tolerant                properties and resource constraints (memory, power-con-
to sustain in hazardous conditions, systems in the security               sumption etc). Hard real-time guarantees require schedula-
domain have to be defended against dynamic threats. In the                bility analysis based on worst-case execution time analysis,
                                                                          which is a large topic on its own. Mechanisms for sched-
9
  In conjunction with the assumption that executing hardware is           uling, resource allocation etc. are highly dependent on the
 behaving according to specification, which is not always the case, but   underlying infrastructure, and thus left out of the discussion.
 an area that is payed dedicated attention to in safety standards (e.g.
 ISO 26262-11:2018).


                                                                                                                               13
 40      Page 6 of 12                                                          Journal of Signal Processing Systems   (2026) 98:40


3.1.1 Challenges of Traditional C Based Methods                          allows the semantic gap between specification and code to
                                                                         be narrowed.
As discussed in Section 2 traditional software development                  Low level hardware interactions can especially benefit
in C/C++ implies a high risk of breaking safety and security             from Rust guarantees, for example type state programming
invariants. Following the MISRA C guidelines, mitigates                  can be used to enforce mutual access restrictions for hard-
inherent risks caused by the underlying problem of permis-               ware, such as pin access on microcontrollers. These restric-
sible UB only partially. This is apparent as MISRA C Rule                tions are from that point on enforced by the compiler and
1.3 classifies general UB as undecidable, and claims only to             eliminate misuse.
address a certain set of common/often occurring scenarios
specifically whereas the rest of the UB is non-compliant                 3.2 Hosted Systems
too by catch-all Rule 1.3 [21]. The problem with C/C++
increases with complexity and code size, as each and every               As a hosted system we define one that has dynamic appli-
line of code may invalidate the requirements for safe/secure             cation loading as well as dynamic memory allocation (see
use of the underlying infrastructure, essentially weakening              Section 1). Thus, we have two domains of development:
pre-qualification guarantees.10                                          userland and kernel.

3.1.2 Challenges for Rust Based Approaches                               3.2.1 Challenges of Traditional Methods

Operating systems, interfaces, drivers and standards have                In context of hosted systems, its the obligation of the devel-
evolved over decades and have as such a strong safety                    oper to uphold the contract for safe interaction. Each line of
argument as being proven in use. Rust in contrast has to be              C/C++ may violate this contract. This topic has long been
adapted into such a grown ecosystem. In [10] the authors                 known and calls to action are getting louder [4, 5]. In effect,
give an example for a transitional approach using foreign                no matter how safe and secure the services provided by
function interfaces (FFI) to bind Rust and C code together.              the host are, safety and security of the system is up to the
Pre-qualification requirements of hardware and software                  developer.
components may assume C/C++. Using Rust, the developer
would need to argue that a Rust equivalent, upholds the                  3.2.2 Challenges for Rust Based Approaches
same or stronger guarantees.
   Sourcing competent developers might be a problem (not                 In contrast to the use of traditional C/C++, the contract
exclusive to Rust, Ada faces the same challenge [34]). How-              between the user application and host can be validated at
ever, using languages such as Ada and Rust, the obligation               compile time, providing an outset for arguing safety and
for correctness is shifted towards the tool, reducing risk at            security at system level. As an example, the Rust std library
the cost of a higher initial investment. Google reported suc-            provides safe abstractions of operating system services.
cess in retraining staff in Rust. They created their own, pub-              The usage of dynamic memory allocation is common in
licly available [35], Rust training material and conducted a             non-critical environments. For critical systems, the chal-
survey with training participants: 2/3 of them felt confident            lenge lies in allowing dynamic memory allocation while
to contribute Rust code after 2 months or less of usage [36].            keeping predictability. In hosted environments (e.g., Linux)
                                                                         we usually have three layers involved in dynamic memory
3.1.3 Opportunities for Rust Based Approaches                            allocation:

An obvious benefit is the guarantees that Rust brings over               1. The Rust Layer, defining String, Box, Vec, and its
C/C++: A project, even written completely in unsafe Rust,                   challenges will be discussed in Section 6.1 and Section
satisfies 91 MISRA Rules by default (becoming 139 when                      6.2. This layer is less problematic as the code is compiled
using safe Rust only). Automated tools can traverse depen-                  by the Rust toolchain, thus gaining all performance and
dencies to aid the developer, e.g., finding known vulner-                   safety benefits that Rust brings.
abilities and use of unsafe code. Rust brings the opportunity            2. The libc Layer, defining C-APIs like malloc and
for better systems engineering as the high level language                   free. This is the more problematic layer. It has been
                                                                            chosen because it is already available on hosted plat-
10
                                                                            forms. However only few of the functions are used regu-
   An increased codesize raises the probability for bugs in Rust too.
The advantage when using Rust is the split into safe and unsafe code.       larly, with malloc() and free() being the most used
Under the assumption that the minority of code is crucial unsafe code.      ones. It is inherently unsafe as it is written in C (recall
These specifically marked unsafe blocks can then be vetted more             Section 1). It is not passed through the Rust toolchain
thoroughly


13
Journal of Signal Processing Systems     (2026) 98:40                                                                    Page 7 of 12    40


   but just linked (whether statically or dynamically does              an implementation of a solution.12 These programs can be
   not matter). The libc layer is also missing out on the               proven correct as adhering to their specification. Examples
   opportunity to benefit from LLVM optimizations while                 of these programs are implementations for classical com-
   keeping defined behavior.                                            puter science problems such as approximation of π , deter-
3. The Linux Kernel, defining APIs such as mmap. This                   mination of a greatest common denominator, or the traveling
   layer is non-debatable once one chooses to use Linux (or             salesman problem.
   another kernel) as operating system. With the advent of                 In contrast, the E-type13 program is capturing a much
   the Rust programming language in the Linux kernel it is              larger context both throughout program development
   possible that this layer will, over time, benefit from Rust          (changing requirements, changes to the problem state-
   safety gains as well.11                                              ment), runtime (deviation from expected runtime context),
                                                                        and lifetime(changing demands/wishes by customers/the
With the upper and lower layer being pretty much fixed,                 society).
one challenge lies in thinning the complexity in the middle-               Traditional safety critical systems as well as the safety
layer. A re-implementation in Rust of libc is tried in [38].            and security critical systems of the future are clearly E-type
We discuss an approach focusing only on memory alloca-                  programs. We can see the interconnectedness of the new
tion in Section 6.1.1.                                                  security critical systems further exacerbate the dynamicity
                                                                        of requirements and making them even more E-ish com-
3.2.3 Opportunities for Rust Based Approaches                           pared to traditional safety critical systems.
                                                                           With this insight comes the applicability of The Laws of
Rust delivers a major improvement over C based develop-                 Program Evolution [39]. Among these is the Law of Increas-
ment, by providing modern tooling, including a native build             ing complexity: that a program, if it changes (E-type),
system, linters, test environment, library management and               through its lifetime will become more complex unless suffi-
code documentation. Given its low runtime requirements                  cient countermeasures are undertaken. This is a serious and
Rust can be used everywhere where C is used today in user-              demanding safety and security issue, if we recall that "The
land (Linux, QNX, VxWorks,...). Safety and security critical            worst enemy of security is complexity" [40]. Safety stan-
systems will benefit from the guarantees safe Rust provides,            dards argue along the same line calling for simplicity and
making Rust a good choice when facing requirements like                 reduced complexity (even naming indicators of complexity
ISO/SAE 21434.                                                          in ISO 26262-6:2018 7.4.3).

                                                                        4.2 Growth Risks
4 Safety, Security, and Program Evolution
                                                                        Rust clearly brings leapstep improvements regarding
Traditional safety critical systems address more or less                maintainability, security, and quality of code for safety
static hazards and apply established mechanisms to mitigate             and security critical software to the table. The challenge
risks. These hazard probabilities are (assumed to be) static            that lies ahead here is to not mistake these improvements
throughout the lifecycle of a product and can thus be speci-            to be immune to complexity and growth. Google, namely
fied statically. Safety critical systems which are connected            the Android project, pivots to Rust with great success: tre-
to the larger outside world through a plethora of interfaces            mendous security and productivity gains have been reported
increase their attack surface targeted by potential malicious           recently [41].
actors. The entities of concern to be modeled are in addition              Without an awareness of the need of complexity reduc-
to the static hazards constantly changing threats.                      tion program growth will compensate gains in security
                                                                        eventually. Google reports a vulnerability rate in Rust that is
4.1 S-Type and E-Type Programs                                          5000x lower than the assumed one in non memory safe lan-
                                                                        guages [41]. With the Android codebase doubling every six
In his article "Programs, Life Cycles, and Laws of Software             years [42] security vulnerability amount will be back at its
Evolution" Meir M. Lehman introduces two categories of                  current level within less than 13 doubling cycles or 78 years.
programs: The S-type and the E-type [39].
   The former being characterized by the existence of a
strict problem specification to which the S-type program is             12
                                                                             The S stands for specification
                                                                        13
                                                                           The "E" stands for embedded referring to the embeddedness of the
                                                                        program into the real world and the society, not to be confused with the
11
   This process is neither friction-free nor simple nor guaranteed to   term embedded system where the term embedded usually refers to the
succeed, as of now Rust adoption is negligibly low in the kernel [37]   embeddedness of a computer in a cyber-physical system


                                                                                                                                   13
 40     Page 8 of 12                                                    Journal of Signal Processing Systems    (2026) 98:40


   To avoid such a scenario Lehman et al. call for an aware-      and Medical IEC 62304 (Class C) standards. However, the
ness to that problem, especially in management, which might       Rust core library is according to publicly available infor-
be driven by the achievement of short term goals (imple-          mation currently qualified to IEC 61508 SIL-2, while the
menting a feature and reporting success) while neglecting         certification obligation for other use lies with the developer.
long term goals (keeping a project manageable) [39].              While Ferrous claims "The amount of pre-certified APIs
   A programming language is incapable of mitigating these        is expected to increase in future releases", meeting higher
kind of risks. Culture and paradigms are soft but strong          certification requirements (beyond SIL-2) still remains[46].
levers to pivot towards leaner solutions. This is well-known      Targets are currently limited to ARM v8 (bare-metal/QNX),
and asked for in safety standards (ISO 26262-2:2018 5.4.2)        ARM v7em (bare-metal), and x86-64 (Linux/QNX). More-
as well as in systems thinking literature [43].                   over it is unclear, to which extent pre-qualification applies
                                                                  to the operating system APIs, as the underlying std is a
4.3 Rust != Rust                                                  super-set of the only partially pre-qualified core library.
                                                                     In context of Hosted Systems (Section 3.2), this currently
The Rust programming language offers a large utility box. It      limits the scope of applicability to QNX based platforms
is possible to have two very versed developers in Rust, one       [47] and hardened Linux based distributions (e.g., the Red
being an expert in type state programming while the other         Hat In-Vehicle Operating System [48]).
one is very fluent in macro programming. Due to the large            In context of bare metal, Ferrocene is directly applicable
set of language features it is not a given that a Rust program-   to commonplace v8/v7em microcontrollers, with the caveat
mer may be comfortable in any Rust codebase.                      that the certification obligation of libraries (partially includ-
                                                                  ing the core library) lies within the responsibility of the
4.3.1 Language Choice Alone is Insufficient                       developer.14

With the term Rust being associated with positive aspects         5.2 HighTec Rust Development Platform
such as productivity, quality, and safety risks grow that the
mere usage of Rust is used to argue for the existence of          While publicly available information is scarce, one can con-
named benefits.                                                   clude that HighTec aims to provide a complete solution for
   In the most extreme case claims may be made for a C pro-       AUTOSAR based development. In that, they have partnered
gram to confer safety properties commonly associated with         with Vector for the AUTOSAR integration [49], directly
Rust because it is wrapped in one large unsafe extern             addressing one of the challenges mentioned in Section 3.1.2.
"C" block. This would technically be Rust syntax and com-
piled through a Rust compiler but clearly misses out on the       5.3 WindRiver/AdaCore
benefits of Rust. This exaggerated example is made to stress
that it is insufficient to refer to the programming language      WindRiver/AdaCore provides a Rust development envi-
used to argue for safety guarantees, even if it brings strong     ronment suitable for applications that require safety certi-
safety features with it, such as in the case of Rust.             fication, e.g., avionic (DO-178C), rail (EN-50128), space
   Solid argumentation for system safety needs to be done         (ECSS-E-ST-40C and ECSS-Q-ST-80C) [50]. They provide
along the lines defined by the established safety standards.      Rust support for VxWorks 7 RTP: full support via native
                                                                  APIs, and VxWorks 7 DKM: via no-std target support. The
                                                                  processes involved certify Rust software in hosted environ-
5 Rust: Are we Safety/Security Critical yet?                      ments that are based on the GNAT (Ada) tool-suite. This is
                                                                  no coincidence. Both, Ada [51] and Rust try to address short-
Over the last decade Rust has transformed from being              comings of C development processes (inherent unsafety,
a niche language, to becoming a realistic alternative for         undefined behaviour) at the language level.
mainstream development in many application domains. In
context of safety/security critical systems, initiatives like     5.4 Safety-Critical Rust Consortium by The Rust
Ferrocene [44] and the HighTec Rust Development Plat-             Foundation
form [45] are set-out to facilitate the use of Rust.
                                                                  The Rust Foundation has announced the Safety-Critical
5.1 Ferrocene                                                     Rust Consortium in 2024 [52]. Work is done publicly and
                                                                  all work done there is published under open source licenses.
Ferrocene provides a Rust toolchain pre-qualified to Auto-
                                                                  14
motive ISO 26262 ASIL-D, Industrial IEC 61508 (SIL 4),              The information of this paragraph is taken from the public docu-
                                                                  mentation, which "might be incomplete or inaccurate" [46].


13
Journal of Signal Processing Systems   (2026) 98:40                                                                 Page 9 of 12    40


Recent developments show a Rust Gap analysis for the               Allocator trait, providing a fallible allocation API. In
applicability of Rust under ISO 26262 [53, 54].                    the future we foresee the std collections to use the new
                                                                   Allocator API unwrapping the result, thus retaining back-
5.5 SAE JA1020                                                     wards compatibility, while incrementally providing fallible
                                                                   APIs. By being allocator generic, the std collections might
SAE International published a first version of their standard      eventually cover all use-cases of the Heapless crate, making
SAE JA1020 - aiming to standardize best practices for the          it obsolete.
usage of the Rust language in critical systems. The standard
is not in the public domain but is intellectual property of        6.2 Drop
SAE International [55, 56]. A published statement is vague
about the contents mentioning recommendations about the            Rust currently allows to opt-out of the drop guarantees,
use of macros, unsafe and dependency management [57].              even in safe code. This essentially allows safe leaking of
                                                                   memory, which together with the fallible allocator API,
                                                                   severely hampers guarantees of reliability.
6 Rust Into the Future                                                There are indeed cases, for which the programmer may
                                                                   want to opt-out of the drop guarantees of Rust, (e.g., when
In this section, we discuss a set of topics and potential future   leaking a buffer to hardware or external legacy code), but
directions of Rust to improve reliability towards high assur-      we argue that such interactions are inherently unsafe, thus
ance, safety and security critical applications.                   any code that voluntarily leaks memory should require
                                                                   unsafe Rust.
6.1 Out Of Memory                                                     This would be a breaking change, requiring a language
                                                                   edition, to which libraries (including core and std) would
The assumption of an infallible allocator is problematic for       need to be updated. However, occurrences of voluntary leak-
dependable/high assurance systems. In the following we             age are rare, and likely clustered to other unsafe low-level
propose two approaches to improve the situation.                   interaction (e.g., allocator implementations, and external
                                                                   interfaces). Notice, this does not immediately make Rust
6.1.1 Heapless                                                     stop leaking memory in safe code (given the default alloca-
                                                                   tor), but prevents misuse of intentional leakage. Provided a
One can from user side opt-out of using the the std lib,           custom allocator with strong re-claim guarantees, leakage
but in many cases, as developers we want the convenience           can be prevented altogether. As a consequence, drop guar-
to use dynamic (heap allocated) data structures (e.g., col-        antees of safe Rust, can be used to ensure, e.g., that un-han-
lections such as Box, Vec, String, Heap). The                      dled sockets will always be closed, or peripheral devices
Heapless crate [58, 59] offers solutions by providing a set        automatically set in sleep mode unless a transaction is ongo-
of dynamic data-structure abstractions backed by stack or          ing, etc., and as such strengthening the deducible properties
static heap pre-allocations. The underlying allocators are         of the application.
fallible, producing an Result::Err in case allocation                 Alternatively, language guidelines, which are common
fails. Unlike the use of a global allocator (as in std), the       in safety-critical development, can be set in place to dis-
developer will get an error for the exact allocator and allo-      courage or prohibit leaking of memory. In Rust, this is eas-
cation that caused the issue, which allows the developer           ily detectable on a syntax level15, making this a decidable
to focus on the code with access to the particular allocator       property.
when searching for allocation bugs (unlike the needle in the
haystack problem, where any dynamic allocation may be              6.3 Stack Overflow
the offender). This works today, and has gained wide uptake
with 35 million downloads.                                         Stack overflow in Rust is as dangerous regarding UB as in
                                                                   any of the legacy languages it strives to succeed, assembly,
6.1.2 Fallible Allocator in std                                    C, and C++ (MISRA C 2025 Addendum 6 Rule 17.2 [22]).
                                                                      Today, external tools such as Symex/EASY can be used
A majority of code written in Rust uses std, thus propos-          for stack-depth and schedulability analysis [60].
ing breaking changes would be hard. A potential alternative           If seen as a high-assurance language, the Rust foundation
is to retain the current API, while internally re-structuring      may consider including stack allocation checking directly
the std implementation in an incremental fashion. First
steps in this direction have been taken by the experimental
                                                                   15
                                                                        searching for terms such as Box::leak or std::mem::forget


                                                                                                                              13
 40       Page 10 of 12                                                             Journal of Signal Processing Systems                                               (2026) 98:40

                                                                          gional Development Fund and the Cybersäkerhetsnod Norr-project
into the obligations of the compiler. One possibility, would be           (no. 20366918).
to adopt a scheme, where the Rust core library provides an
(overridable) default stack allocator (preserving the current             Data Availability No datasets were generated or analysed during the
stack allocation semantics). A custom stack allocator would               current study.
require the backend to prove that the generated code meets
the transitive stack requirement along each reachable path.               Declarations
The LLVM backend already supports compile time assess-
                                                                          Competing interests The authors declare no competing interests.
ment of per-function stack memory allocation. Unlike C/C++
this is possible since Rust requires all stack allocations to be          Open Access This article is licensed under a Creative Commons
sized, thus the generated code is free of dynamic stack alloca-           Attribution 4.0 International License, which permits use, sharing,
tions using alloca(). Left, to do for the backend would be                adaptation, distribution and reproduction in any medium or format,
to span the call graph in order to give a safe bound, similar to          as long as you give appropriate credit to the original author(s) and the
                                                                          source, provide a link to the Creative Commons licence, and indicate
the cargo-call-stack approach presented in [61, 62].                      if changes were made. The images or other third party material in this
   In case the backend fails to prove a bound (e.g., due to               article are included in the article’s Creative Commons licence, unless
unknown loop/recursion bounds, function pointers, etc.), a                indicated otherwise in a credit line to the material. If material is not
compiler error could detail the need for additional informa-              included in the article’s Creative Commons licence and your intended
                                                                          use is not permitted by statutory regulation or exceeds the permitted
tion. The developer could refine the implementation, e.g.,                use, you will need to obtain permission directly from the copyright
by means of const-generics resolved at compile time, help-                holder. To view a copy of this licence, visit ​h​t​t​​p​:​/​/​​c​r​e​​a​t​i​​v​e​c​o​m​m​o​n​s​.​o​
ing the backend.                                                          r​g​/​l​i​c​e​n​s​e​s​/​b​y​/​4​.​0​/​​​​.​​​
   Whether or not stack allocation checking should be
regarded as a language feature depends on which future
direction we want Rust to take.                                           References
                                                                          1.     Standardization, I.O. (2018). ISO 26262 Road Vehicles Func-
                                                                                 tional Safety, Iso 26262:2018 edn. International Organization for
7 Conclusions and Future Work                                                    Standardization, Vernier, Geneva, Switzerland. ​h​t​t​​p​s​:​/​​/​w​w​​w​.​i​​s​o​.​o​
                                                                                 r​g​/​p​u​b​l​i​c​a​t​i​o​n​/​P​U​B​2​0​0​2​6​2​.​h​t​m​l​​​​
While Rust provides a realistic alternative and improvement               2.     CWE - CWE Top 25 Most Dangerous Software Weaknesses
over commonplace C/C++ for use in critical applications we                       (2024). ​h​t​t​​p​s​:​/​​/​c​w​​e​.​m​​i​t​r​​e​.​o​​r​g​/​t​​o​p​​2​5​/​a​r​c​h​i​v​e​/​2​0​2​4​/​2​0​2​4​_​c​w​e​_​t​o​p​
                                                                                 2​5​.​h​t​m​l​​​​. Accessed 29 Aug 2025
must conclude that "There is no magic formula that makes                  3.     CWE - CWE Top 25 Most Dangerous Software Weaknesses
an intrinsically hard job easy." [26].                                           (2025). ​h​t​t​​p​s​:​/​​/​c​w​​e​.​m​​i​t​r​​e​.​o​​r​g​/​t​​o​p​​2​5​/​a​r​c​h​i​v​e​/​2​0​2​5​/​2​0​2​5​_​c​w​e​_​t​o​p​
   In this paper we have covered the weaknesses of com-                          2​5​.​h​t​m​l​​​​Accessed 31 July 2026
monplace developments using C/C++ in safety critical                      4.     House, T. W. BACK TO THE BUILDING BLOCKS: A Path
                                                                                 Toward Secure and Measurable Software. The White House.​
systems and how they have been addressed previously.                             h​t​t​​p​s​:​/​​/​b​i​​d​e​n​​w​h​i​​t​e​h​​o​u​s​e​​.​a​​r​c​h​​i​v​e​s​​.​g​o​​v​/​w​​p​-​c​o​n​t​e​n​t​/​u​p​l​o​a​d​s​/​2​0​
The expansion of safety critical systems to security critical                    2​4​/​0​2​/​F​i​n​a​l​-​O​N​C​D​-​T​e​c​h​n​i​c​a​l​-​R​e​p​o​r​t​.​p​d​f​​​​.​ Accessed 29 Aug
systems in the future through the increase of connectivity                       2025
puts further stress on the weaknesses of prior development                5.     Watson, R. N. M., Baldwin, J., Chisnall, D., Chen, T., Clarke, J.,
                                                                                 Davis, B., Filardo, N., Gutstein, B., Jenkinson, G., Laurie, B.,
techniques. We found that Rust, in two different deploy-                         Mazzinghi, A., Moore, S., Neumann, P.G., Okhravi, H., Richard-
ment scenarios - hosted and bare-metal - can address certain                     son, A., Rebert, A., Sewell, P., Tratt, L., Vijayaraghavan, M., Vin-
shortcomings of prior development techniques.                                    cent, H., & Witaszczyk, K. It is time to standardize principles and
   Further we surveyed ongoing commercial efforts by,                            practices for software memory safety 68(2), 40–45. ​h​t​t​​p​s​:​/​​/​d​o​​i​.​o​​r​
                                                                                 g​/​1​0​.​1​1​4​5​/​3​7​0​8​5​5​3​​​​. Accessed 28 May 2025
Ferrous Systems (Ferrocene), HighTec (Rust Development                    6.     Regulation (EU) 2024/2847 of the European Parliament and of
Platform), WindRiver/AdaCore (VxWorks/GNAT).                                     the Council of 23 October 2024 on Horizontal Cybersecurity
   Additionally we have identified a set of remaining chal-                      Requirements for Products with Digital Elements and Amending
lenges regarding the Rust memory model and possible                              Regulations (EU) No 168/2013 and (EU) 2019/1020 and Direc-
                                                                                 tive (EU) 2020/1828 (Cyber Resilience Act) (Text with EEA rel-
directions for hardening the Rust language.                                      evance). Legislative Body: OP_DATPRO. ​h​t​t​​p​:​/​/​​d​a​t​​a​.​e​​u​r​o​p​a​.​e​u​/​e​
                                                                                 l​i​/​r​e​g​/​2​0​2​4​/​2​8​4​7​/​2​0​2​4​-​1​1​-​2​0​​​​. Accessed 31 Jul 2026
Author Contributions M.M wrote the main manuscript text. M.L. and         7.     Directive (EU) 2022/2555 of the European Parliament and
J.E. contributed with Industry experience and background knowledge               of the Council of 14 December 2022 on Measures for a High
and insights into safety critical systems. P.D. helped formulating text          Common Level of Cybersecurity Across the Union, Amending
passages, proofreading, and debating concepts. P.L. helped with the              Regulation (EU) No 910/2014 and Directive (EU) 2018/1972,
initial text, and discussing concepts.                                           and Repealing Directive (EU) 2016/1148 (NIS 2 Directive)
                                                                                 (Text with EEA relevance). Legislative Body: OP_DATPRO.​
Funding Open access funding provided by Lulea University of Tech-                h​t​t​​p​:​/​/​​d​a​t​​a​.​e​​u​r​o​p​a​.​e​u​/​e​l​i​/​d​i​r​/​2​0​2​2​/​2​5​5​5​/​2​0​2​2​-​1​2​-​2​7​.​​​​ Accessed
nology. This research is financially supported by the European Re-               31 Jul 2026



13
Journal of Signal Processing Systems                                              (2026) 98:40                                                                                                                                           Page 11 of 12                     40

8.    Volvo (2023). Why Rust is actually good for your car. ​h​t​t​​p​s​:​/​​/​m​                                                              28. Classic AUTOSAR Operating System. ​h​t​t​​p​s​:​/​​/​w​w​​w​.​e​​l​e​k​​t​r​o​​b​i​t​.​​c​
      e​​d​i​u​​m​.​c​​o​m​/​​v​o​l​v​​o​-​​c​a​r​​s​-​e​n​​g​i​n​​e​e​r​​i​n​g​/​w​h​y​-​v​o​l​v​o​-​t​h​i​n​k​s​-​y​o​u​-​s​h​o​u​l​             o​​m​/​p​r​o​d​u​c​t​s​/​e​c​u​/​e​b​-​t​r​e​s​o​s​/​o​p​e​r​a​t​i​n​g​-​s​y​s​t​e​m​s​/​​​​. Accessed 30 Aug
      d​-​h​a​v​e​-​r​u​s​t​-​i​n​-​y​o​u​r​-​c​a​r​-​4​3​2​0​b​d​6​3​9​e​0​9​​​​                                                                  2025
9.    Delgado, M. T. Eclipse Safe Open Vehicle Core | Projects.eclipse.                                                                        29. MICROSAR Classic. ​h​t​t​​p​s​:​/​​/​w​w​​w​.​v​​e​c​t​​o​r​.​​c​o​m​/​​i​n​​t​/​e​n​/​p​r​o​d​u​c​t​s​/​p​
      org.                       https:/​/projec​ts.ecli​pse.o​rg/projects/automotive.score.                                                       r​o​d​u​c​t​s​-​a​-​z​/​e​m​b​e​d​d​e​d​-​s​o​f​t​w​a​r​e​/​m​i​c​r​o​s​a​r​-​c​l​a​s​s​i​c​/​​​​. Accessed 30
      Accessed 29 June 2026                                                                                                                        Aug 2025
10.   Seidel, L., & Beier, J. Bringing rust to safety-critical systems in                                                                      30. Correnson, L., Cuoq, P., Kirchner, F., Maroneze, A., Prevosto,
      space. In 2024 Security for Space Systems (3S) (pp. 1–8). ​h​t​t​​p​s​:​/​​/​                                                                V., Puccetti, A., Signoles, J., & Yakobowski, B. Frama-C User
      d​o​​i​.​o​​r​g​/​1​0​.​2​3​9​1​9​/​3​S​6​0​5​3​0​.​2​0​2​4​.​1​0​5​9​2​2​8​7​​​​ . ​h​t​t​​p​s​:​/​​/​i​e​​e​e​x​​p​l​o​r​e​.​i​e​          Manual. https:/​/frama-​c.com/d​ownlo​ad/frama-c-user-manual.pdf
      e​e​.​o​r​g​/​d​o​c​u​m​e​n​t​/​1​0​5​9​2​2​8​7​/​​​​. Accessed 21 May 2025                                                              31. Denis, X., Jourdan, J.-H., & Marché, C. (2022) Creusot: a
11.   Noseda, M., Frei, F., Rüst, A., & Künzli, S. Rust for secure IoT                                                                             Foundry for the Deductive Verification of Rust Programs. In Lec-
      applications: Why c is getting rusty.                                                                                                        ture Notes in Computer Science. Lecture Notes in Computer Sci-
12.   Gasiba, T. E., & Amburi, S.I think this is the beginning of a beau-                                                                          ence. Springer Verlag, Madrid, Spain. ​h​t​t​​p​s​:​/​​/​i​n​​r​i​a​​.​h​a​l​.​s​c​i​e​n​c​e​/​h​a​
      tiful friendship - on the rust programming language and secure                                                                               l​-​0​3​73​ ​7​8​7​8​​​​
      software development in the industry.                                                                                                    32. Introduction - Rust Fuzz Book. https:/​/rust-f​uzz.git​hub.i​o/book/.
13.   Lehman, M. (1969). The programming process, ibm reserch                                                                                      Accessed 29 Aug 2025
      report rc2722m. ibm research centre, yorktown heights. Program                                                                           33. Test Organization - The Rust Programming Language. ​h​t​t​​p​s​:​/​​/​d​o​​c​
      Evolution-Processes of Software Change.                                                                                                      .​r​​u​s​t​​-​l​a​​n​g​.​o​​r​g​​/​b​o​o​k​/​c​h​1​1​-​0​3​-​t​e​s​t​-​o​r​g​a​n​i​z​a​t​i​o​n​.​h​t​m​l​​​​.​ Accessed 29
14.   Commission, I. E. (2010). IEC 61508 Commented Version, 2.0                                                                                   Aug 2025
      edn. International Electrotechnical Commission, Geneva, Swit-                                                                            34. Robb, J. H. Hey- C and C++ Can Be Used In Safety Critical
      zerland. https:/​/websto​re.iec.​ch/en​/publication/22273                                                                                    Applications Too! https://archive.ph/CCrxN. Accessed 26 July
15.   Inc., R. (2011). RTCA DO-178C Software considerations in                                                                                     2025
      airborne systems and equipment certification, includes errata                                                                            35. Welcome to Comprehensive Rust - Comprehensive Rust. ​h​t​t​​p​s​:​/​​/​
      (2020). RTCA Inc., 1150 18th NW, Suite 910 Washington, D.C.                                                                                  g​o​​o​g​l​​e​.​g​i​t​h​u​b​.​i​o​/​c​o​m​p​r​e​h​e​n​s​i​v​e​-​r​u​s​t​/​​​​. Accessed 08 Mar 2026
      20036. ​h​t​t​​p​s​:​/​​/​s​t​​o​r​e​​.​a​c​​c​u​r​​i​s​t​e​​c​h​​.​c​o​m​/​s​t​a​n​d​a​r​d​s​/​r​t​c​a​-​d​o​-​1​7​8​c​?​p​r​o​         36. Rust Fact Vs. Fiction. 5 Insights from Google’s Rust Journey in
      d​u​c​t​_​i​d​= ​2​2​0​0​1​0​5​​​​                                                                                                           2022. ​h​t​t​​p​s​:​/​​/​o​p​​e​n​s​​o​u​r​​c​e​.​​g​o​o​g​​l​e​​b​l​o​​g​.​c​o​​m​/​2​​0​2​3​​/​0​6​/​r​u​s​t​-​f​a​c​t​-​v​s​-​f​i​
16.   Commission, I. E. (2006). IEC 62304 Consolidated Version, 1.1                                                                                c​t​i​o​n​-​5​-​i​n​s​i​g​h​t​s-​ ​f​r​o​m​-​g​o​o​g​l​e​s-​ ​r​u​st​​-​j​o​u​r​n​e​y​-​2​0​2​2​.​h​tm        ​ ​l​​​​.​ Accessed
      edn. International Electrotechnical Commission, Geneva, Swit-                                                                                08 Mar 2026
      zerland. https:/​/websto​re.iec.​ch/en​/publication/22794                                                                                37. Li, H., Guo, L., Yang, Y., Wang, S., & Xu, M. An empirical study
17.   Standardization, I. O. (2021). ISO/SAE 21434:2021 Road Vehi-                                                                                 of rust-for-linux: The success, dissatisfaction, and compromise.
      cles — Cybersecurity Engineering, Edition 1, 2021 edn. Inter-                                                                            38. Redox-os / Relibc · GitLab. ​h​t​t​​p​s​:​/​​/​g​i​​t​l​a​​b​.​r​e​d​o​x​-​o​s​.​o​r​g​/​r​e​d​o​x​-​o​s​/​r​
      national Organization for Standardization, Vernier, Geneva,                                                                                  e​l​i​b​c​​​​.​ Accessed 31 Aug 2025
      Switzerland. https:/​/www.is​o.org/s​tanda​rd/70918.html                                                                                 39. Lehman, M. M. (1980). Programs, life cycles, and laws of soft-
18.   Addenda to the 1958 Agreement (2021). UN Regulation No. 155                                                                                  ware evolution. Proceedings of the IEEE, 68(9), 1060–1076.
      - Cyber security and cyber security management system. ​h​t​t​​p​s​:​/​​/​u​                                                             40. A Plea for Simplicity. ​h​t​t​​p​s​:​/​​/​w​w​​w​.​s​​c​h​n​​e​i​e​​r​.​c​o​​m​/​​e​s​s​a​y​s​/​a​r​c​h​i​v​e​s​/​
      n​​e​c​e​​.​o​r​​g​/​t​​r​a​n​s​​p​o​​r​t​/​​d​o​c​u​​m​e​n​​t​s​/​​2​0​2​1​/​0​3​/​s​t​a​n​d​a​r​d​s​/​u​n​-​r​e​g​u​l​a​t​i​o​n​-​n​       1​9​9​9​/​1​1​/​a​_​p​l​e​a​_​f​o​r​_​s​i​m​p​l​i​c​i​t​.​h​t​m​l​​​​. Accessed 17 June 2025
      o​-​1​5​5​-​c​y​b​e​r​-​s​e​c​u​r​i​t​y​-​a​n​d​-​c​y​b​e​r​-​s​e​c​u​r​i​t​y​​​​                                                        41. Stoep, J. V., Android. Rust in Android: Move Fast and Fix Things.​
19.   Addenda to the 1958 Agreement (2021). UN Regulation No. 156                                                                                  h​t​t​​p​s​:​/​​/​s​e​​c​u​r​​i​t​y​​.​g​o​​o​g​l​e​​b​l​​o​g​.​c​o​m​/​2​0​2​5​/​1​1​/​r​u​s​t​-​i​n​-​a​n​d​r​o​i​d​-​m​o​v​e​-​f​
      - Uniform provisions concerning the approval of vehicles with                                                                                a​s​t​-​f​i​x​-​t​h​i​n​g​s​.​h​t​m​l​​​​. Accessed 08 Mar 2026
      regards to software update and software updates management                                                                               42. team, J. V. S.-A., & Foundations, A. R.-S. Eliminating memory
      system. https:/​/unece.​org/sit​es/de​fault/files/2024-03/R156e                                                                              safety vulnerabilities at the source. ​h​t​t​​p​s​:​/​​/​s​e​​c​u​r​​i​t​y​​.​g​o​​o​g​l​e​​b​l​​o​g​.​​c​
20.   Usenet:comp.std.c (1992). Undefined Behavior. ​h​t​t​​p​s​:​/​​/​g​r​​o​u​p​​s​.​g​​                                                         o​m​/​​2​0​2​​4​/​0​​9​/​e​l​i​m​i​n​a​t​i​n​g​-​m​e​m​o​r​y​-​s​a​f​e​t​y​-​v​u​l​n​e​r​a​b​i​l​i​t​i​e​s​-​A​n​d​r​o​i​d​
      o​o​g​​l​e​.​c​​o​m​​/​g​/​c​o​m​p​.​s​t​d​.​c​/​c​/​y​c​p​V​K​x​T​Z​k​g​w​/​m​/​S​2​h​H​d​T​b​v​4​d​8​J​?​h​l​                              .​h​t​m​l​​​​ Accessed 08 Mar 2026
      = ​e​n​&​p​l​i​= ​1​​​​                                                                                                                  43. Meadows, D. H. Thinking in Systems a Primer. Chelsea Green
21.   Consortium, T. M. (2025). MISRA C:2025 Guidelines for the Use                                                                                Pub.
      of the C Language in Critical Systems. The MISRA Consortium                                                                              44. Systems, F. (2025). This is Rust for critical systems. ​h​t​t​p​s​:​/​/​f​e​r​r​o​c​
      Limited.                                                                                                                                     e​n​e​.​d​e​v​​​​
22.   Consortium, T. M. (2025) MISRA C:2025 Addendum 6 Applica-                                                                                45. Systeme, H. E. (2025). Rust Development Platform. ​h​t​t​p​s​:​/​/​h​i​g​h​t​
      bility of MISRA C:2025 to the Rust Programming Language. The                                                                                 e​c​-​r​t​.​c​o​m​/​r​u​st​​​​​
      MISRA Consortium Limited.                                                                                                                46. Ferrocene Documentation Index. ​h​t​t​​p​s​:​/​​/​p​u​​b​l​i​​c​-​d​o​c​s​.​f​e​r​r​o​c​e​n​e​.​d​e​
23.   Unsafe Rust - The Rust Programming Language. ​h​t​t​​p​s​:​/​​/​d​o​​c​.​r​​u​s​                                                             v​/​m​a​i​n​/​i​n​d​e​x​.​h​t​m​l​​​​Accessed 30 June 2026
      t​​-​l​a​​n​g​.​o​​r​g​​/​b​o​o​k​/​c​h​2​0​-​0​1​-​u​n​s​a​f​e​-​r​u​s​t​.​h​t​m​l​#​u​n​s​a​f​e​-​r​u​s​t​​​​.​ Accessed               47. QNX Safety Certifications | ISO 26262, IEC 61508, IEC
      31 Jul 2026                                                                                                                                  62304. https:/​/blackb​erry.qn​x.com​/en/developers/certifications.
24.   LLVM Loop Optimization Can Make Safe Programs Crash ·                                                                                        Accessed 29 Aug 2025
      Issue #28728 · Rust-lang/rust. ​h​t​t​​p​s​:​/​​/​g​i​​t​h​u​​b​.​c​o​m​/​r​u​s​t​-​l​a​n​g​/​r​u​s​t​/​                                 48. Functional Safety and Continuous Certification on Linux. ​h​t​t​​p​s​:​/​​/​
      i​s​s​u​e​s​/​2​8​7​2​8​​​​. Accessed 29 Aug 2025                                                                                            w​w​​w​.​r​​e​d​h​​a​t​.​​c​o​m​/​​e​n​​/​t​o​​p​i​c​s​​/​o​p​​e​n​-​​s​o​u​r​c​e​/​f​u​n​c​t​i​o​n​a​l​-​s​a​f​e​t​y​-​a​n​d​-​c​o​
25.   Le Lann, G. An analysis of the ariane 5 flight 501 failure-a system                                                                          n​t​i​n​u​o​u​s​-​c​e​r​t​i​f​i​c​a​t​i​o​n​-​o​n​-​l​i​n​u​x​​​​. Accessed 29 Aug 205
      engineering perspective. In Proceedings international conference                                                                         49. Vector and HighTec Bring Functional Safety Applications With
      and workshop on engineering of computer-based systems (pp.                                                                                   Rust and AUTOSAR Classic to the Road ​h​t​t​​p​s​:​/​​/​w​w​​w​.​v​​e​c​t​​o​r​.​​c​o​m​
      339–346). https:/​/doi.or​g/10.11​09/EC​BS.1997.581900. ​h​t​t​​p​s​:​/​​/​i​e​​                                                             /​​s​e​​/​e​n​​/​n​e​w​​s​/​n​​e​w​s​​/​s​a​f​e​t​y​-​a​p​p​l​i​c​a​t​i​o​n​s​-​w​i​t​h​-​r​u​s​t​-​a​n​d​-​a​u​t​o​s​a​r​-​c​l​a​s​
      e​e​x​​p​l​o​r​e​.​i​e​e​e​.​o​r​g​/​d​o​c​u​m​e​n​t​/​5​8​1​9​0​0​/​​​​. Accessed 31 Aug 2025                                               s​i​c​/​​​​
26.   Anderson, R. J. (2020). Security Engineering: A Guide to Build-                                                                          50. Enabling rust for critical systems. ​h​t​t​​p​s​:​/​​/​w​w​​w​.​w​​i​n​d​​r​i​v​​e​r​.​c​​o​m​​/​r​e​s​
      ing Dependable Distributed Systems (3rd ed.). USA: Wiley.                                                                                    o​u​r​c​e​/​e​n​a​b​l​i​n​g​-​r​u​s​t​-​f​o​r​-​c​r​i​t​t​i​c​a​l​-​s​y​s​t​e​m​s​​​​. Accessed 31 Aug 2025
27.   AUTOSAR (Automotive Open System Architecture). ​h​t​t​p​s​:​/​/​w​w​                                                                     51. Ada Language Reference Manual 2022. ​h​t​t​​p​:​/​/​​w​w​w​​.​a​d​​a​-​a​u​t​h​.​o​r​g​
      w​.​a​u​t​o​s​a​r​.​o​r​g​/​​​​. Accessed 30 Aug 2025                                                                                        /​s​t​a​n​d​a​r​d​s​/​a​d​a​2​2​.​h​tm       ​ ​l​​​​. Accessed 03 Oct 2025




                                                                                                                                                                                                                                                               13
   40              Page 12 of 12                                                                                                                          Journal of Signal Processing Systems                                   (2026) 98:40

52. Announcing the Safety-Critical Rust Consortium - The Rust                                                                                  58. Heapless - Crates.io: Rust Package Registry. ​h​t​t​​p​s​:​/​​/​c​r​​a​t​e​​s​.​i​o​/​c​r​a​t​
    Foundation. ​h​t​t​​p​s​:​/​​/​r​u​​s​t​f​​o​u​n​​d​a​t​​i​o​n​.​​o​r​​g​/​m​e​d​i​a​/​a​n​n​o​u​n​c​i​n​g​-​t​h​e​-​s​a​                      e​s​/​h​ea​ ​p​l​e​ss​ ​​​​. Accessed 29 Aug 2025
    f​e​t​y​-​c​r​i​t​i​c​a​l​-​r​u​s​t​-​c​o​n​s​o​r​t​i​u​m​/​​​​. Accessed 16 Mar 2026                                                      59. Rivera, J. A., Lindner, M., & Lindgren, P. (2018). Heapless:
53. ISO Vs. Rust Gap Analysis | Are We Safety Critical Yet? 26262. .                                                                               Dynamic data structures without dynamic heap allocator for rust.
    Accessed 19 Mar 2026 ​h​t​t​​p​s​:​/​​/​a​r​​e​w​e​​s​a​f​e​t​y​c​r​i​t​i​c​a​l​y​e​t​.​o​r​g​/​d​o​c​s​/​i​s​o​                               In IEEE 16th International Conference on Industrial Informatics
    2​6​2​6​2​​​​                                                                                                                                  (INDIN) (pp. 87–94). ​h​t​t​​p​s​:​/​​/​d​o​​i​.​o​​r​g​/​1​0​.​1​1​0​9​/​I​N​D​I​N​.​2​0​1​8​.​8​4​7​2​0​9​7​​​​
54. ISO 26262 and Rust Gap Analysis for the Front-page to Evalu-                                                                               60. Dzialo, P., Joensson, I., Muench, M., Serrander, E., Eriksson, J.,
    ate Rust S… · Rustfoundation/safety-critical-rust-consortium@                                                                                  & Lindgren, P. (2025). Minimally intrusive safety and security
    c2ce7af. ​h​t​t​​p​s​:​/​​/​g​i​​t​h​u​​b​.​c​​o​m​/​​r​u​s​t​​f​o​​u​n​d​​a​t​i​o​​n​/​s​​a​f​e​​t​y​-​c​r​i​t​i​c​a​l​-​r​u​s​t​-​c​o​       verification of rust rtic applications. In DVCon Europe 2025;
    n​s​o​r​t​i​u​m​/​c​o​m​m​i​t​/​c​2​c​e​7​a​f​4​2​0​e​9​f​c​f​b​e​b​b​d​6​a​e​b​c​9​4​2​1​6​1​9​b​d​e​f​f​c​c​8​​​​.​                          Design and verification conference and exibition (pp. 22–28).
    Accessed 19 Mar 2026                                                                                                                           https:/​/doi.or​g/10.30​420/5​66664004
55. SAfEr Rust Task Force - SAE StandardsWorks. ​h​t​t​​p​s​:​/​​/​s​t​​a​n​d​​a​                                                              61. Aparicio,                      J.    Japaric/cargo-call-stack.                        original-date:
    r​d​​s​w​o​​r​k​s​.​​s​a​​e​.​o​r​g​/​s​t​a​n​d​a​r​d​s​-​c​o​m​m​i​t​t​e​e​s​/​s​a​f​e​r​-​r​u​s​t​-​t​a​s​k​-​f​o​r​c​e​​​​​.                2018-12-03T01:52:30Z. ​h​t​t​​p​s​:​/​​/​g​i​​t​h​u​​b​.​c​o​m​/​j​a​p​a​r​i​c​/​c​a​r​g​o​-​c​a​l​l​-​s​t​
    Accessed 19 Mar 2026                                                                                                                           a​c​k​​​​.​ Accessed 29 Aug 2025
56. Committee, F. S. (2026). Safety and cybersecurity recommenda-                                                                              62. Lindgren, P., Fitinghoff, N., & Aparicio, J. (2019). Cargo-call-
    tions for the use of the rust language in critical systems. ​h​t​t​​p​s​:​/​​/​d​                                                              stack static call-stack analysis for rust. In IEEE 17th International
    o​​i​.​o​​r​g​/​1​0​.​4​2​7​1​/​J​A​1​0​2​0​_​2​0​2​6​0​3​​​​                                                                                  Conference on Industrial Informatics (INDIN) (vol. 1, pp. 1169–
57. SAE JA | Blog | SAE International - SAE International 1020. ​h​t​                                                                              1176). https:​​​//d​oi.​or​g/10​.110​9/INDI​N410​52.2019.8972088
    t​​p​s​:​/​​/​w​w​​w​.​s​​a​e​.​​o​r​g​​/​n​e​w​​s​/​​b​l​o​​g​/​s​a​​e​-​j​​a​1​0​​2​0​-​s​a​f​e​t​y​-​c​y​b​e​r​s​e​c​u​r​i​t​y​-​r​e​
    c​o​m​m​e​n​d​a​t​i​o​n​s​-​u​s​e​-​r​u​s​t​-​l​a​n​g​u​a​g​e​-​c​r​i​t​i​c​a​l-​ ​s​y​st​​e​ms​ ​​​​. Accessed 30                         Publisher's Note Springer Nature remains neutral with regard to juris-
    June 2026                                                                                                                                  dictional claims in published maps and institutional affiliations.




13
