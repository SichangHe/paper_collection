                                            Rusty Linux: Advances in Rust for Linux Kernel Development
                                                                         Shane K. Panter                                                                  Nasir U. Eisty
                                                              Department of Computer Science                                                    Department of Computer Science
                                                                   Boise State University                                                            Boise State University
                                                                     Boise, Idaho, USA                                                                 Boise, Idaho, USA
                                                                shanepanter@boisestate.edu                                                         nasireisty@boisestate.edu

                                        ABSTRACT                                                                                    (ONCD) released a report calling for the technical community to
                                        Context: The integration of Rust into kernel development is a                               proactively reduce the attack surface in cyberspace with a two-
                                        transformative endeavor aimed at enhancing system security and                              pronged approach [30]. First, we need to address the root cause of
                                        reliability by leveraging Rust’s strong memory safety guarantees.                           many of the most heinous cyber attacks: memory-unsafe program-
arXiv:2407.18431v2 [cs.SE] 6 Sep 2024




                                        Objective: We aim to find the current advances in using Rust in                             ming languages. Second, we need to establish better cybersecurity
                                        Kernel development to reduce the number of memory safety vulner-                            quality metrics so we can have a better understanding of the cyber-
                                        abilities in one of the most critical pieces of software that underpins                     security landscape.
                                        all modern applications. Method: By analyzing a broad spectrum                                  In the ever-evolving landscape of software development, the
                                        of studies, we identify the advantages Rust offers, highlight the                           reliability and security of computer systems stand as a paramount
                                        challenges faced, and emphasise the need for community consen-                              concern for all parties involved. Modern software is constructed by
                                        sus on Rust’s adoption. Results: Our findings suggest that while                            building ever more complex abstractions, one on top of the other.
                                        the initial implementations of Rust in the kernel show promising                            Thus, if we aim to have a secure system, we must start to peel
                                        results in terms of safety and stability, significant challenges re-                        back all the layers and tackle one of the fundamental abstractions
                                        main. These challenges include achieving seamless interoperability                          in computer science: the programming language. Programming
                                        with existing kernel components, maintaining performance, and                               languages that provide and enforce memory safety eliminate whole
                                        ensuring adequate support and tooling for developers. Conclu-                               classes of bugs, such as buffer overflows, dangling pointers, and
                                        sions: This study underscores the need for continued research and                           memory leaks which have been implicated in a myriad of security
                                        practical implementation efforts to fully realize the benefits of Rust.                     vulnerabilities and system crashes.
                                        By addressing these challenges, the integration of Rust could mark                              Most operating system kernels are predominantly written in the
                                        a significant step forward in the evolution of operating system                             C programming language with bits of assembly. C has been favored
                                        development towards safer and more reliable systems.                                        for its low-level capabilities and performance efficiency, crucial for
                                                                                                                                    kernel development. However, the inherent lack of memory safety
                                        CCS CONCEPTS                                                                                in C has led to numerous security vulnerabilities, including buffer
                                                                                                                                    overflows and use-after-free errors, which have plagued operation
                                        • General and reference → Surveys and overviews; • Security
                                                                                                                                    system development for decades [23]. Addressing these vulnerabil-
                                        and privacy → Operating systems security; • Software and
                                                                                                                                    ities is paramount to enhancing the security and reliability of all
                                        its engineering → Operating systems; Language features.
                                                                                                                                    operating systems.
                                                                                                                                        Rust, a systems programming language developed by Mozilla, has
                                        KEYWORDS
                                                                                                                                    garnered significant attention for its strong emphasis on memory
                                        Memory safety, Rust, Kernel, Operating System, Linux                                        safety without sacrificing performance. Rust’s ownership model and
                                        ACM Reference Format:                                                                       its compile-time checks effectively prevent common programming
                                        Shane K. Panter and Nasir U. Eisty. 2024. Rusty Linux: Advances in Rust                     errors that lead to security vulnerabilities [10]. What makes Rust
                                        for Linux Kernel Development. In Proceedings of the 18th ACM / IEEE Inter-                  unique is the fact that it accomplishes these tasks without the
                                        national Symposium on Empirical Software Engineering and Measurement                        use of a garbage collector, making it an ideal candidate for kernel
                                        (ESEM ’24), October 24–25, 2024, Barcelona, Spain. ACM, New York, NY, USA,                  development where safety and performance are critical.
                                        7 pages. https://doi.org/10.1145/3674805.3690756
                                                                                                                                        The potential integration of Rust into kernel development rep-
                                                                                                                                    resents a significant shift in the landscape of operating system
                                        1     INTRODUCTION                                                                          development. This shift prompts a comprehensive evaluation of
                                        The 1995 movie Hackers prescient predictions regarding the ease                             both the opportunities and challenges associated with using Rust as
                                        of breaking into computing systems in cyberspace have come to                               such a foundational component of modern computing. Therefore,
                                        fruition. The White House Office of the National Cyber Director                             we aim to synthesize existing research and practical experiences
                                                                                                                                    related to the use of Rust in the kernel, providing a detailed under-
                                        Permission to make digital or hard copies of part or all of this work for personal or
                                        classroom use is granted without fee provided that copies are not made or distributed       standing of the current state of this emerging field.
                                        for profit or commercial advantage and that copies bear this notice and the full citation       This reflection paper presents a systematic literature review
                                        on the first page. Copyrights for third-party components of this work must be honored.      (SLR) focusing on strategies and methodologies for integrating Rust
                                        For all other uses, contact the owner/author(s).
                                        ESEM ’24, October 24–25, 2024, Barcelona, Spain                                             into one of the most fundamental areas that are typically dominated
                                        © 2024 Copyright held by the owner/author(s).                                               by unsafe languages, the operating system kernel. We aim to provide
                                        ACM ISBN 979-8-4007-1047-6/24/10.                                                           a comprehensive overview of existing research, identify gaps, and
                                        https://doi.org/10.1145/3674805.3690756
ESEM ’24, October 24–25, 2024, Barcelona, Spain                                                                Shane K. Panter and Nasir U. Eisty


suggest future directions in this domain. Through a rigorous search       Database           Query                            Results
process, we synthesized relevant studies and extracted key findings       ACM                (Abstract:("operating system" 30
to offer insights into effective approaches for ensuring memory                              OR Kernel OR linux OR OS)
safety when working closely with hardware.                                                   AND Abstract:(Rust)) OR (Ti-
                                                                                             tle:("operating system" OR OS
                                                                                             OR kernel OR linux) AND Ti-
2     RESEARCH METHODOLOGY
                                                                                             tle:(Rust))
For our research methodology, we followed the Kitchenham and               IEEE              ("All Metadata":"operating sys- 39
Charters [9] methodology to conduct a SLR in software engineering.                           tem" AND "All Metadata":rust)
We divided our review into three discrete phases, planning the                               OR ("All Metadata":kernel AND
review, conducting the review, and reporting the review results. The                         "All Metadata":rust) OR ("All
following sections detail our review process and are diagrammed                              Metadata":linux AND "All Meta-
in figure 1.                                                                                 data":rust)
                                                                           Scopus            TITLE-ABS-KEY ( ( "operating 87
2.1     Planning                                                                             system" OR kernel OR linux )
                                                                                             AND rust ) AND PUBYEAR >
To begin our study, we must first confirm the need for a SLR. The
                                                                                             2018 AND PUBYEAR < 2025
recent report released by ONCD [30] has conveniently done this job
                                                                                             AND ( LIMIT-TO ( SUBJAREA ,
for us by compiling a report detailing the need for research in the
                                                                                             "COMP" ) ) AND ( LIMIT-TO (
domain of memory safety. While the ONCD report detailed a two-
                                                                                             LANGUAGE , "English" ) )
pronged approach, for this reflection paper, we will be focusing on a
                                                                           Springer Link     Operating      System     Rust 29
memory-safe programming language, specifically Rust. While there
                                                                                             Kernel (Conference Paper,
are many modern memory-safe programming languages available
                                                                                             Article,    Research    article)
for software developers to use, Rust is one of the few languages that
                                                                                             Subdiscipline: Software en-
is feasible to use when developing operating system kernels due to
                                                                                             gineering/programming and
its lack of runtime and garbage collector [27]. The Linux kernel is
                                                                                             operating systems
currently in the early stages of adding real support for Rust [29]
thus, we will focus on Rust as a primary candidate to replace the              Table 1: Search Queries used for each Database.
aging C programming language.


2.2     Research Questions                                                    Besides technical challenges and limitations, developers’ per-
We have defined the following research questions:                             ceptions are very important in software development. There-
                                                                              fore, through this research question, we want to find devel-
      • RQ1: What are the existing approaches for implement-                  opers’ reflections on what went well and what didn’t go well
        ing operating system kernels in Rust?                                 while developing kernels in Rust.
        Although Rust in the Linux kernel is recent, we want to see
        what approaches researchers have explored in any operating
                                                                        2.3   Data Collection
        system. Experiential and research kernels can provide new
        ideas that can be integrated into the Linux kernel.             2.3.1 Search Strategy. We employed a robust multi-step search
      • RQ2: What are the performance implications of using             strategy across four databases: ACM Digital Library, IEEE Xplore,
        Rust for operating system kernel development?                   Scopus, and Springer Link to find all the current research. We
        The C programming language has the advantage of 40 years        leveraged the advanced search features of all three databases to
        of improvements and lessons learned regarding how to write      search the titles and abstracts for keywords using boolean search
        fast code. Rust, being a new language, still has many un-       operators.
        explored areas regarding how to write fast code, especially     2.3.2 Search criteria. We searched all four databases with the
        in kernel space. Therefore, we want to explore the perfor-      keywords listed in table 1 between January 1, 2019 and April 1,
        mance implications of Rust for kernel development in terms      2024. We choose to look at only the previous 5 years of research in
        of throughput, latency, and resource utilization.               order to capture the bleeding-edge research that is currently being
      • RQ3: What are the major challenges and limitations              done. While both ACM and IEEE had mutually exclusive results,
        when developing operating system kernels in Rust?               Scopus had 44 duplicates that needed to be removed and Springer
        Kernel space presents unique challenges for the software        Link didn’t have any new papers that were not also in ACM or
        engineer using Rust. Rust was not designed to implement         IEEE. We then used Google Scholar to do forward and backward
        kernels and is more restrictive than C. Thus, we want to        snowballing.
        identify if there are any stumbling blocks that have already
        been found when using Rust in kernel development.               2.3.3 Inclusion and exclusion criteria. Following the guide-
      • RQ4: What are the lessons learned when developing               lines outlined by Kitchenham and Charters [9] we set the inclusion
        operating systems kernels in Rust?                              and exclusion criteria based on our research questions outlined
Rusty Linux: Advances in Rust for Linux Kernel Development                                                        ESEM ’24, October 24–25, 2024, Barcelona, Spain




                                                                                                        Application of
                                                     ACM DL                30 Results                 inclusion criteria




                           Apply Search                                                               Screen Titles and
      Potential                                       IEEE                                               Abstracts
                           Query to each                                    39 Results                                             Total Papers: 28
       Papers               Database                  Xplore



                                                                                                      Manual Filtering
                                                                                                         Studies
                                                      Scopus               87 Results


                                                                                                        Snowballing
                                                                                                          Studies
                                                     Springer               29 Results



                                                     Figure 1: Process Diagram for Paper selection

                                         Table 2: Approaches and Methodologies for Rust in the Kernel

                                   Approach           Papers                       Operating System in Rust
                                   Monolithic         [29], [16], [21], [26]       Linux kernel v6.1+
                                   Micro-kernel       [5],[17], [18], [25], [24]   Atmosphere, Redox, Redleaf
                                   Embedded           [6], [31]                    Tock, Hubris, Drone, Bern, HarSaRK
                                   Unikernel          [12], [3], [8], [28]         RustyHermit, Theseus
                                   Exokernel          [15]                         W-Kernel


in section 2.2. We only considered papers that are written in Eng-                  Since the results were straightforward and came from a compar-
lish and published in conferences, journals, and workshops. The                     atively small number of papers, there were no discrepancies or
published papers should describe using the Rust programming lan-                    missing results to solve.
guage for either developing a new kernel, extending an existing
kernel, or authoring drivers. We included any type of kernel ar-
chitecture, including monolithic kernel, microkernel, or unikernel                  3     RESULTS
in both the embedded and non-embedded space, as long as the
                                                                                    In this section, we present our findings. We address each research
paper is using the Rust programming language in some way. Papers
                                                                                    question from RQ1 - RQ4.
that describe solutions that reside 100% in user space or papers
that relied too heavily on a component written in C were excluded.
Early efforts to use Rust in kernel development were impacted by
changes and updates in both the Rust language and compiler and
                                                                                    3.1    RQ1: Existing Approaches
relied on unstable features, which were thus excluded from this                     The integration of Rust into operating system kernel development
review.                                                                             has garnered significant attention due to Rust’s promise of mem-
                                                                                    ory safety and concurrency guarantees. Several approaches and
                                                                                    methodologies have emerged to leverage Rust for kernel develop-
2.4     Data Analysis                                                               ment, each addressing different aspects of kernel functionality and
Once we had our initial collection of papers from the databases,                    integration. We found several approaches that researchers are tak-
we merged all duplicate papers into one record and then started                     ing to integrate Rust into kernel development. The first approach is
our first pass, which consisted of reading the title and abstract and               a greenfield approach where the operating system architecture is
either marking the paper as include or exclude. Once we completed                   redesigned and built from the ground up in order to fully leverage
the initial screening, we were left with 22 papers that needed an                   the Rust programming language [3, 6]. The second approach is
in-depth reading and analysis. We found an additional 6 papers                      the incremental integration of Rust into existing kernels, such as
during forward and backward snowballing that were also reviewed,                    the Linux kernel [21, 26, 29]. This methodology involves gradually
bringing the total number of papers to 28. The first author manually                rewriting or augmenting specific components of the kernel with
reviewed all 28 papers, built the first dataset, and conducted the                  Rust while maintaining compatibility with the existing C codebase.
analysis. The second author then verified all the data and results.                 Finally, researches are porting existing C kernels over to Rust and
ESEM ’24, October 24–25, 2024, Barcelona, Spain                                                                 Shane K. Panter and Nasir U. Eisty


then evaluating the differences. Table 2 summarizes our findings re-    Table 3: Performance Implications of Rust in the Kernel
garding what existing approaches researchers are using to integrate
rust into the kernel.                                                        No.   Implication    Studies that Reported the challenge
    For the first approach, Boos et al. [3] created an experimental          1     Performance    [7], [14], [19]
operating system named Theseus that operates in a single address             2     Throughput     [7]
space and single privilege level and uses properties of the Rust             3     Latency        [6]
programming language to realize isolation instead of relying on
hardware. This novel approach pushes some of the roles that a
traditional operating system would take onto the compiler. The
design of Theseus uses a novel cell-based structure where owner-       General Purpose Operating System, are not directly meaningful
ship of memory and resources is enforced by the compiler, thus         due to the vastly different goals of each system and the overhead
avoiding these checks during runtime to get improved performance.      that is imposed by the hardware [1]. Therefore, we will focus more
In addition to memory safety, Theseus has a goal of addressing the     on the overall efforts that are specific to the Rust programming
state spill problem. State spill happens when a single service in an   language and the challenges presented. We summarize our findings
operating system can harbor a state change induced by interacting      in table 3.
with other services. That state change can eventually cause a sys-        Culic et al. [6] looked at latency issues in Tock. Tock is a new op-
tem crash or system instability at some point in the future, making    erating system written in Rust that is designed to run on embedded
it very difficult to track down the problem due to the separation      systems but does not provide real-time capabilities. The authors
between when the problem occurred and when it was observed.            attempted to add real-time capabilities by integrating eBPF into the
Theseus OS is an operating system that was designed to match the       Tock kernel to improve the interrupt handler’s response time. The
Rust language instead of the more traditional route of matching the    authors found that early work (still in the prototype stage) lowers
hardware. Li and Sato [15] explored using Rust to write an exoker-     the response times of the system and interrupts response times 3x.
nel named W-Kernel. The authors proposed a novel architecture             Gonzalez et al. [7] explored using the Rust for Linux Project
for an OS by embedding a WebAssembly (WASM) runtime into               to implement a native UDP driver in Rust in order to explore the
the kernel that can run programs written in any language that can      performance of the Rust programming language. The authors were
compile down to WASM.                                                  able to get a basic driver working with performance only slightly
    For the second approach, researchers take a more traditional       slower than C using the Rust for Linux (RFL) project. The RFL
micro-kernel implementation [5, 17]. By pushing most kernel func-      project is still too immature to get a full driver up and running,
tionality to user space, the authors limited the surface area that     but it is at a stage where researchers can start experimenting with
needs to be proved. Chen X et al. [5] took their implementation one    different approaches.
step further by formally verifying their new micro-kernel named           Li et al. [14] explored the feasibility of using Rust in kernel
Atmosphere by using both the liner type system of Rust in combina-     space. The authors took an existing component, the Out of Memory
tion with an SMT solver. They were able to get a 7.5:1 proof-to-code   (OOM), and implemented a replacement using the Rust program-
ratio, which is higher than other formerly verified micro-kernels      ming language. The non-encapsulated interface Rust component
SeL4 and CeriKOS both of which have proof code ratios of 19:1 and      which was almost identical to the original C component, only in-
20:1, respectively. While this approach was novel, drivers running     troduced a 0.7% overhead. The encapsulated Rust component, on
in userspace are still not formally verified and don’t have to be      the other hand, added a 3% performance overhead.
written in Rust.
    Finally, researchers have taken existing unikernels written in C   3.3     RQ3: Challenges and Limitations
and ported them to Rust. Unikernels are designed to do one thing       The development of operating system kernels in Rust introduces
and one thing only, thus limiting the complexity that a general-       several unique challenges and limitations compared to more tradi-
purpose operating system has to deal with [20]. This reduced com-      tional languages like C. These challenges arise from Rust’s strict
plexity allowed Lankes et al. [12] to take HermitCore and rewrite      safety guarantees, its relatively recent adoption in systems program-
it in Rust. The new Unikernel named RustyHermit consists of only       ming, and the inherent complexities of kernel development [27].
3.27% unsafe Rust, with the rest of the code base consisting of        This section discusses these challenges, limitations, and the lessons
safe Rust, dramatically decreasing the surface area where memory       learned from various projects and research efforts. We summarize
errors could originate.                                                our findings in table 4.
                                                                          A primary concern for programming languages that are used for
                                                                       operating system development is the size of the binary especially in
3.2     RQ2: Performance Implications                                  an embedded environment, we must be careful to keep the size of
Comparing performance, throughput and latency between different        the Rust component as close as we can to the C component so we
systems with different architectures is very difficult. For example,   can still run on the same hardware. Li et al. [14] found that there
several of the operating systems written in Rust are a complete        was only a 0.06% size increase when compared to the original C
rethinking of how an operating system is designed [3] while others     implementation. Ayers et al. [2] focused on reducing the size of
run entirely in kernel space [12]. Additionally, direct comparisons    binaries produced by the rust compiler while working with Tock
between a Monolithic kernel, Micro-kernel, and Unikernel, or com-      OS. They were able to identify several causes of binary growth
parisons between a Real Time Operation System (RTOS) and a             that are specific to the Rust programming language and have the
Rusty Linux: Advances in Rust for Linux Kernel Development                                               ESEM ’24, October 24–25, 2024, Barcelona, Spain


                                        Table 4: Challenges Unique to the Rust Programming Language

    No.          Challenge                                   Description
    1            Binary Size [2]
                                                                 • Deeply ingrained monomorphization which increased the size of the
                                                                   rust binaries
                                                                 • Compiler optimizations are not as mature as some C based compilers,
                                                                   thus increasing binary size
                                                                 • Hidden data structures and data
                                                                 • Sub-optimal compiler generated support code

    2            Missing Features [4]
                                                                 • Supporting trait bounds on functions and closures with any number of
                                                                   arguments
                                                                 • Expose type information in procedural macros
                                                                 • Support a collision-free, unique type identifier
                                                                 • Support typed assembly language for Rust
                                                                 • Support trusted build environments
                                                                 • Provide software-only stack guard with extensible probing interface
                                                                 • Develop zero-copy serialization of “plain-old” data structures

    3            Soundness [11]
                                                                 • Unsynchronized Global State - any use of mutable statics is unsafe
                                                                 • C-Style Abstractions - Use rust style abstractions to properly encapsulate
                                                                   internal unsafe usage of raw pointers
                                                                 • Aliasing Mutable References - Giving out raw pointers to memory that
                                                                   is also referenced mutably
                                                                 • Re-implementing Memory Access - instead of accessing specific memory
                                                                   regions in assembly, creating and using references to the whole region
                                                                   is preferable

    4            Panics [19],[4]
                                                                 • Support extendable, no_std unwind library
                                                                 • Stack unwinding in embedded environments

    5            C Interop [22], [13]
                                                                 • Kernel interfaces, while designed for extensibility, are not designed for
                                                                   type safety
                                                                 • Hybrid Code Flow. The Rust compiler can not track ownership when
                                                                   switching between modules written in C and Rust



following 5 recommendations when using Rust in a size-constrained            system development that are detailed in table 4. The authors argue
environment:                                                                 that with these changes or inclusions to the Rust programming lan-
     • Minimize Length + Instantiations of Generic Code                      guage developing operating system kernels would be much easier
     • Use Trait Objects Sparingly                                           and safer.
     • Don’t Panic
     • Carefully Use Compiler Generated Support Code                         3.4    RQ4: Lessons Learned
     • Don’t use static mut                                                  Klimt et al. [11] details the lessons learned and challenges when im-
   Burtsev et al. [4] explored what is missing in the Rust program-          plementing Theseus. First, they found that it is impossible to write
ming language to help solve the isolation problem in an operating            a complete operating system in 100% safe Rust. For example, when
system. Currently, Rust lacks the ability to express isolation in            writing a memory management system, raw pointers must be used
the heap without external support. For example, the RedLeaf ex-              to modify the hardware. Despite the limitations imposed by the
periential operating system, which was written in Rust, relied on            hardware, the authors describe how Theseus leveraged intralingual
a complex interface definition language (IDL) to enforce isolated            design to maximize the compiler’s role in enforcing correctness. By
heaps. The paper enumerates several properties of the Rust Lan-              leveraging Rust’s type system and borrow checker memory safety,
guage that could help with isolation with regards to operating               correct ownership transfer can be achieved at a higher level than
ESEM ’24, October 24–25, 2024, Barcelona, Spain                                                                           Shane K. Panter and Nasir U. Eisty


what could be done in C. The authors also detailed some of the            about the limitations. Despite these threats, our results provide a
limitations of intralingual design, such as not being as expressive       valuable synthesis of the current state of research on the use of
as many other formal verification techniques due to the limited           Rust in kernel development, highlighting both its potential benefits
invariance that the type system can enforce. One of the most impor-       and the challenges that need to be addressed.
tant lessons learned was the insight that a linear type system itself
cannot guarantee the uniqueness of the resource represented, such         5    DISCUSSION & CONCLUSION
as when a memory resource may overlap. The authors introduce the          The integration of Rust into kernel space represents a significant
idea of using a hybrid approach of verification where they leverage       evolution in operating system development, promising to address
both the linear type system and an SMT solver. The authors also           long-standing issues related to memory safety and system relia-
explore the bootstrapping problem with rust systems. In operating         bility. We synthesized the current state of research and practice
systems written in C, the kernel provides the ownership root to           concerning the use of Rust in multiple types of kernels, including
applications running on top. Finding a new ownership root is an           the venerable Linux kernel, highlighting both the progress made
open research question with regard to using Rust for operating            and the challenges that remain.
system development.                                                          Our review indicates that Rust’s strong guarantees of memory
                                                                          safety, enabled by its ownership model and strict compile-time
4    THREATS TO VALIDITY                                                  checks, offer a compelling advantage over traditional C-based ker-
Internal Threats. Potential internal threats include:                     nel development. These features have the potential to reduce com-
     • Quality of Studies: The methodological rigor of the included       mon vulnerabilities such as buffer overflows and use-after-free er-
       studies varies, and some may suffer from design flaws or           rors, which are prevalent in C and have historically led to critical se-
       biases that were not adequately controlled for, thus affecting     curity exploits. Several case studies and prototype implementations
       the reliability of their findings.                                 have demonstrated that Rust can be successfully integrated into
     • Selection Criteria: The inclusion and exclusion criteria for se-   the kernel, providing safer interfaces and reducing the incidence of
       lecting relevant studies might inadvertently bias the review       memory-related bugs without incurring significant performance
       towards certain types of research, such as those reporting         penalties.
       successful integration while underrepresenting studies de-            However, the adoption of Rust for kernel development is not
       tailing challenges and failures.                                   without its challenges. Truly, the biggest challenge is existing code-
                                                                          bases and mountains of legacy code. With extensive use of C and re-
    External Threats. Threats to external validity include:
                                                                          liance on specific C idioms and low-level programming techniques,
     • Context-Specific Findings: Many studies focus on specific ker-     researchers have substantial integration hurdles to overcome. Any
       nel modules or use-cases, which may not be representative          efforts to rewrite substantial portions of an existing kernel such
       of the broader kernel environment. The success of Rust in          as Linux in Rust, are constrained by the need for interoperability
       isolated components does not necessarily translate to the          with existing C code and the necessity to maintain the kernel’s
       entire kernel.                                                     performance characteristics. Furthermore, the operating system
     • Temporal Changes: The rapidly evolving nature of both the          development community must reach a consensus on Rust’s role
       Rust programming language and the Linux kernel means               and ensure that sufficient tooling, documentation, and support are
       that findings from older studies may no longer be applicable,      available for developers.
       as improvements and changes in both domains can alter the             In conclusion, while Rust’s incorporation into the kernel space
       landscape significantly.                                           is still in its nascent stages, the initial results are promising. The
     • Definition Ambiguity: The term “Kernel development in Rust”        potential for enhanced security and stability aligns with the long-
       encompasses a wide range of activities, from minor module          term goals of kernel development, and continued research, coupled
       development to complete subsystem rewrites. Variations in          with practical implementation efforts, will be crucial in realizing
       how researchers and developers interpret this integration          these benefits. Future work should focus on addressing integration
       could lead to inconsistent findings.                               challenges, refining interoperability mechanisms, and expanding
    Conclusion Threats. Potential conclusion threats include:             the body of empirical evidence on Rust’s impact within the kernel
     • Heterogeneity of Studies: The diverse methodologies, metrics,      environment. As the community navigates these challenges, the
       and contexts of the included studies can lead to challenges        evolution of Rust in the kernel may well mark a transformative
       in synthesizing findings and drawing unified conclusions.          period in the pursuit of safer, more reliable operating systems.
       For example, it is very difficult to directly compare a micro-
       kernel, Unikernel, and hybrid Kernel.                              REFERENCES
     • Reviewer Bias: Personal biases of the reviewers in interpret-       [1] Andrew Arnott. 2012. The cost of context switches. https://devblogs.microsoft.
                                                                               com/premier-developer/the-cost-of-context-switches/. Accessed: 2024-6-5.
       ing data and making judgments about study quality and               [2] Hudson Ayers, Evan Laufer, Paul Mure, Jaehyeon Park, Eduardo Rodelo, Thea
       relevance may skew the results                                          Rossman, Andrey Pronin, Philip Levis, and Johnathan Van Why. 2022. Tighten
                                                                               rust’s belt: shrinking embedded Rust binaries. In Proceedings of the 23rd ACM
   We made efforts to minimize this through predefined criteria and            SIGPLAN/SIGBED International Conference on Languages, Compilers, and Tools for
multiple reviewers, but some degree of subjectivity is inevitable. In          Embedded Systems (San Diego, CA, USA) (LCTES 2022). Association for Comput-
                                                                               ing Machinery, New York, NY, USA, 121–132.
addressing these threats, we employed rigorous methods for study           [3] Kevin Boos, Namitha Liyanage, Ramla Ijaz, and Lin Zhong. 2020. Theseus:
selection, data extraction, and analysis, and we remain transparent            an Experiment in Operating System Structure and State Management. In 14th
Rusty Linux: Advances in Rust for Linux Kernel Development                                                                      ESEM ’24, October 24–25, 2024, Barcelona, Spain


     USENIX Symposium on Operating Systems Design and Implementation (OSDI 20).              [23] MSRC Team. 2019.          We need a safer systems programming language.
     USENIX Association, virtual, 1–19. https://www.usenix.org/conference/osdi20/                 https://msrc.microsoft.com/blog/2019/07/we-need-a-safer-systems-
     presentation/boos                                                                            programming-language/. Accessed: 2024-5-28.
 [4] Anton Burtsev, Dan Appel, David Detweiler, Tianjiao Huang, Zhaofeng Li, Vikram          [24] Vikram Narayanan, Marek S Baranowski, Leonid Ryzhyk, Zvonimir Rakamarić,
     Narayanan, and Gerd Zellweger. 2021. Isolation in Rust: What is Missing?. In                 and Anton Burtsev. 2019. RedLeaf: Towards An Operating System for Safe and
     Proceedings of the 11th Workshop on Programming Languages and Operating Sys-                 Verified Firmware. In Proceedings of the Workshop on Hot Topics in Operating
     tems (Virtual Event, Germany) (PLOS ’21). Association for Computing Machinery,               Systems (Bertinoro, Italy) (HotOS ’19). Association for Computing Machinery,
     New York, NY, USA, 76–83.                                                                    New York, NY, USA, 37 – 44.
 [5] Xiangdong Chen, Zhaofeng Li, Lukas Mesicek, Vikram Narayanan, and Anton                 [25] Vikram Narayanan, Tianjiao Huang, David Detweiler, Dan Appel, Zhaofeng Li,
     Burtsev. 2023. Atmosphere: Towards Practical Verified Kernels in Rust. In Pro-               Gerd Zellweger, and Anton Burtsev. 2020. RedLeaf: Isolation and Communication
     ceedings of the 1st Workshop on Kernel Isolation, Safety and Verification (Koblenz,          in a Safe Operating System. In 14th USENIX Symposium on Operating Systems
     Germany) (KISV ’23). Association for Computing Machinery, New York, NY, USA,                 Design and Implementation (OSDI 20). USENIX Association, virtual, 21–39. https:
     9–17.                                                                                        //www.usenix.org/conference/osdi20/presentation/narayanan-vikram
 [6] Ioana Culic, Alexandru Vochescu, and Alexandru Radovici. 2022. A Low-Latency            [26] Shuichi Oikawa. 2023. The Experience of Developing a FAT File System Module
     Optimization of a Rust-Based Secure Operating System for Embedded Devices.                   in the Rust Programming Language. Stud. Comput. Intell. 1074 (2023), 45 – 58.
     Sensors 22, 22 (2022), 8700.                                                            [27] Miguel Ojeda. 2021. LKML: ojeda@kernel ...: [PATCH 00/13] [RFC] Rust support.
 [7] Amélie Gonzalez, Djob Mvondo, and Yérom-David Bromberg. 2023. Takeaways of                   https://lkml.org/lkml/2021/4/14/1023. Accessed: 2024-6-5.
     Implementing a Native Rust UDP Tunneling Network Driver in the Linux Kernel.            [28] Mincheol Sung, Pierre Olivier, Stefan Lankes, and Binoy Ravindran. 2020. Intra-
     In Proceedings of the 12th Workshop on Programming Languages and Operating                   unikernel isolation with Intel memory protection keys. In Proceedings of the 16th
     Systems (Koblenz, Germany) (PLOS ’23). Association for Computing Machinery,                  ACM SIGPLAN/SIGOPS International Conference on Virtual Execution Environ-
     New York, NY, USA, 18–25.                                                                    ments (Lausanne, Switzerland) (VEE ’20). Association for Computing Machinery,
 [8] Ramla Ijaz, Kevin Boos, and Lin Zhong. 2023. Leveraging Rust for Lightweight                 New York, NY, USA, 143 – 156.
     OS Correctness. In Proceedings of the 1st Workshop on Kernel Isolation, Safety and      [29] The kernel development community. 2024. Rust — The Linux Kernel documenta-
     Verification (Koblenz, Germany) (KISV ’23). Association for Computing Machinery,             tion. https://docs.kernel.org/rust/index.html. Accessed: 2024-4-1.
     New York, NY, USA, 1–8.                                                                 [30] United States Gov. 2024. Press Release: Future Software Should Be Mem-
 [9] Barbara Kitchenham. 2004. Procedures for Performing Systematic Reviews. Keele,               ory Safe. https://www.whitehouse.gov/oncd/briefing-room/2024/02/26/press-
     UK, Keele Univ. 33 (08 2004).                                                                release-technical-report/. Accessed: 2024-3-13.
[10] Steve Klabnik and Carol Nichols. 2024. The Rust Programming Language -                  [31] K I Vishnunaryan and Gourinath Banda. 2022. HarSaRK_multi_rs: A Hard Real-
     The Rust Programming Language. https://doc.rust-lang.org/book/. Accessed:                    time Kernel for Multi-core Microcontrollers in Rust Language. Smart Innovation,
     2024-6-1.                                                                                    Systems and Technologies 283 (2022), 21 – 32.
[11] Jonathan Klimt, Martin Kröning, Stefan Lankes, and Antonello Monti. 2023. On
     the Challenge of Sound Code for Operating Systems. In Proceedings of the 12th           accepted 22 July 2024
     Workshop on Programming Languages and Operating Systems (Koblenz, Germany)
     (PLOS ’23). Association for Computing Machinery, New York, NY, USA, 83–90.
[12] Stefan Lankes, Jens Breitbart, and Simon Pickartz. 2019. Exploring Rust for
     Unikernel Development. In Proceedings of the 10th Workshop on Programming
     Languages and Operating Systems (Huntsville, ON, Canada) (PLOS ’19). Associa-
     tion for Computing Machinery, New York, NY, USA, 8–15.
[13] Jialin Li, Samantha Miller, Danyang Zhuo, Ang Chen, Jon Howell, and Thomas
     Anderson. 2021. An incremental path towards a safer OS kernel. In Proceedings of
     the Workshop on Hot Topics in Operating Systems (Ann Arbor, Michigan) (HotOS
     ’21). Association for Computing Machinery, New York, NY, USA, 183–190.
[14] Linhan Li, Qianying Zhang, Zekun Xu, Shijun Zhao, Zhiping Shi, and Yong Guan.
     2024. rOOM: A Rust-Based Linux Out of Memory Kernel Component. IEICE
     Trans. Inf. Syst. E107.D, 3 (2024), 245–256.
[15] Shaowen Li and Hiroyuki Sato. 2024. W-Kernel: An OS Kernel Architecture
     Designed With Isolation and Customizability. In Proceedings of the 2023 5th
     International Conference on Software Engineering and Development (Singapore,
     Singapore) (ICSED ’23). Association for Computing Machinery, New York, NY,
     USA, 42 – 50.
[16] Zhuohua Li, Jincheng Wang, Mingshen Sun, and John C S Lui. 2019. Securing
     the Device Drivers of Your Embedded Systems: Framework and Prototype. In
     Proceedings of the 14th International Conference on Availability, Reliability and Se-
     curity (Canterbury, CA, United Kingdom) (ARES ’19). Association for Computing
     Machinery, New York, NY, USA, 1–10.
[17] Yuanzhi Liang, Lei Wang, Siran Li, and Bo Jiang. 2021. Rustpi: A Rust-powered
     Reliable Micro-kernel Operating System. In International Symposium on Soft-
     ware Reliability Engineering Workshops (ISSREW). IEEE, Wuhan University of
     Technology, 272 – 273.
[18] Guojun Liu, Jili Huang, and Xiaoyan Liu. 2024. An OS Kernel Based on RISC-V
     Architecture. Commun. Comput. Inf. Sci. 1899 (2024), 3 – 16.
[19] Zhiyao Ma, Guojun Chen, and Lin Zhong. 2023. Panic Recovery in Rust-based
     Embedded Systems. In Proceedings of the 12th Workshop on Programming Lan-
     guages and Operating Systems (PLOS ’23). Association for Computing Machinery,
     New York, NY, USA, 66 – 73.
[20] Anil Madhavapeddy and David J Scott. 2014. Unikernels: the rise of the virtual
     library operating system. Commun. ACM 57, 1 (Jan. 2014), 61–69.
[21] Samantha Miller, Kaiyuan Zhang, Mengqi Chen, Ryan Jennings, Ang Chen,
     Danyang Zhuo, and Thomas Anderson. 2021. High Velocity Kernel File Systems
     with Bento. In 19th USENIX Conference on File and Storage Technologies (FAST 21).
     USENIX Association, virtual, 65–79. https://www.usenix.org/conference/fast21/
     presentation/miller
[22] Samantha Miller, Kaiyuan Zhang, Danyang Zhuo, Shibin Xu, Arvind Krishna-
     murthy, and Thomas Anderson. 2019. Practical Safe Linux Kernel Extensibility.
     In Proceedings of the Workshop on Hot Topics in Operating Systems (Bertinoro,
     Italy) (HotOS ’19). Association for Computing Machinery, New York, NY, USA,
     170 – 176.
