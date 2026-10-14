                                                 Finding Memory Leaks in C/C++ Programs via Neuro-Symbolic Augmented
                                                                            Static Analysis


                                                                       Huihui Huang1 , Jieke Shi1,* , Bo Wang2 , Zhou Yang3 , David Lo1
                                                                                     1
                                                                                     Singapore Management University, Singapore
                                        2
                                            Beijing Jiaotong University, Beijing, China 3 University of Alberta & Alberta Machine Intelligence Institute, Alberta, Canada
                                                              {hhhuang, jiekeshi, davidlo}@smu.edu.sg, wangbo_cs@bjtu.edu.cn, zy25@ualberta.ca
arXiv:2603.27224v5 [cs.SE] 6 Oct 2026




                                        Abstract—Memory leaks remain prevalent in real-world C/C++          consumption of up to 20GB, rendering affected systems
                                        software. Static analyzers such as CodeQL provide scalable          unresponsive [5], while a heap memory leak in Ollama
                                        program analysis but frequently miss such bugs because they         enabled unauthenticated attackers to extract API keys and
                                        cannot recognize project-specific custom memory-management          user conversations, potentially affecting ∼300,000 servers
                                        functions and lack path-sensitive control-flow modeling. We         worldwide [6]. With over 1,800 CVEs (Common Vulner-
                                        present M EM H INT, a neuro-symbolic pipeline that addresses        abilities and Exposures) attributed to memory leaks as of
                                        both limitations by combining LLMs’ semantic understand-            May 2026 [7], effective automated detection of such defects
                                        ing of code with Z3-based symbolic reasoning. M EM H INT            remains a pressing need for software reliability and security.
                                        parses the target codebase and applies an LLM to classify               Memory leaks are notoriously difficult to detect. Dy-
                                        each function as a memory allocator, deallocator, or neither,       namic analysis approaches such as fuzzing [8]–[11] can
                                        producing function summaries that record which argument             identify leaks along executed paths but impose substantial
                                        or return value carries memory ownership, extending the             runtime overhead that limits scalability for large-scale or
                                        analyzer’s built-in knowledge beyond standard primitives such       long-running software [12], [13], and may fail to exercise the
                                        as malloc and free. A Z3-based validation step checks each          specific paths needed to trigger a leak within a practical time
                                        summary against the function’s control-flow graph, discarding       budget (as discussed in Section 2). Static analysis is a more
                                        those whose claimed memory operation is unreachable on any          attractive alternative, as it can reason over all program paths
                                        feasible path. The validated summaries are injected into Cod-
                                                                                                            without requiring execution. Static analyzers such as Cod-
                                                                                                            eQL [14] and Infer [15] perform interprocedural dataflow
                                        eQL and Infer via their respective extension mechanisms. Z3
                                                                                                            analysis to trace how memory is allocated and deallocated,
                                        path feasibility filtering then eliminates warnings on infeasible
                                                                                                            detecting mismatched or missing deallocations, and have
                                        paths, and a final LLM-based validation step confirms whether
                                                                                                            seen wide industrial adoption [16], [17]. However, these
                                        each remaining warning is a genuine bug. On eight real-world
                                                                                                            analyzers lack semantic understanding of custom memory
                                        C/C++ projects totaling over 3.6M lines of code, M EM H INT
                                                                                                            management and path feasibility, resulting in both missed
                                        detects 54 unique memory leaks, all confirmed or fixed, at
                                                                                                            detections and spurious warnings.
                                        approximately $1.7 per detected bug, compared to 19 by vanilla          In real-world C/C++ projects, developers often im-
                                        CodeQL and 3 by vanilla Infer.                                      plement custom variants of Memory Management (MM)
                                        Index Terms—Memory Leak Detection, Static Analysis, Large           functions rather than directly calling standard primitives
                                        Language Models, Neuro-Symbolic Analysis                            such as malloc and free. This practice is especially
                                                                                                            prevalent in large open-source codebases that span many
                                                                                                            modules from diverse contributors [2], [18]–[20], where
                                        1. Introduction                                                     a single project may define hundreds of custom memory
                                                                                                            allocation and deallocation functions (e.g., tree_init and
                                            C/C++, as programming languages with explicit mem-              policy_tree_free in OpenSSL [21]). Effective leak de-
                                        ory management, require developers to manually deallocate           tection thus requires identifying these custom functions and
                                        memory regions that are no longer needed. Failure to do             their allocation/deallocation pairings.
                                        so results in memory leaks: unreleased memory cannot                    Unfortunately, existing static analyzers such as CodeQL
                                        be reclaimed by the operating system, gradually depleting           by default operate with a fixed list of standard primitives,
                                        system resources and potentially causing system failures [1],       remaining blind to custom MM functions and silently miss-
                                        [2] or exploitable security vulnerabilities [3], [4]. Recent        ing leaks mediated by them. Prior work [2], [18], [22]–
                                        high-profile incidents underscore this risk: a memory leak          [24] resorts to heuristics or natural language processing
                                        in Windows 11’s update service caused unbounded RAM                 (NLP) techniques that infer memory management roles from
                                                                                                            function names or documentation, yet these heuristics do
                                        *
                                            Corresponding author.                                           not check whether the inferred allocation or deallocation is
reachable on any feasible intraprocedural path. A function           tool LeakGuard [24] finds 20. We construct a human-labeled
may contain a syntactic call to free inside a branch that is         dataset of 1,532 functions; evaluation on it shows that
never satisfiable; labeling such a function as a deallocator         M EM H INT achieves 100% precision and recall on reachable
will cause the analyzer to wrongly assume the memory can             memory management function identification, substantially
be freed through it, suppressing genuine leak reports. Even          outperforming LeakGuard (34.0% precision, 52.2% recall).
when custom MM functions are correctly identified, the an-           An ablation study confirms that each pipeline component
alyzers themselves remain path-insensitive: they often over-         independently contributes to the overall effectiveness. Ad-
approximate program behavior and report warnings along               ditionally, the total cost per detected bug is approximately
paths that are infeasible under actual runtime conditions,           $1.7, and the static analysis portion of the pipeline runs
flooding developers with false alarms that demand costly             2.8–3.1× faster than LeakGuard. These results demonstrate
manual triage [25]–[27].                                             that M EM H INT effectively bridges the gap between seman-
    Our key insight is that addressing the limitations above         tic understanding and symbolic reasoning, enabling precise
requires both semantic understanding and symbolic reason-            and scalable memory leak detection in real-world C/C++
ing: identifying custom MM functions calls for compre-               software.
hending developer intent from code context, while vali-                   Our paper makes the following contributions:
dating those identifications and filtering false positives de-       • We frame memory leak detection as a neuro-symbolic
mands rigorous symbolic analysis of program control flow.               task: LLMs infer custom memory-management functions
We realize this insight in M EM H INT, which is a neuro-                from code context, while Z3 validates their reachability
symbolic pipeline. For the neuro component, we leverage                 and filters infeasible leak warnings.
Large Language Models (LLMs), which have shown strong                • We show that LLM-generated MM function summaries
capabilities across various programming tasks [28]–[30] and             can faithfully encode allocator/deallocator semantics and,
cybersecurity tasks [31], [32], to infer the memory manage-             once injected into static analyzers, substantially boost
ment roles of functions. However, LLMs are susceptible to               their detection performance.
hallucinations [33], [34] and may produce incorrect annota-          • We implement M EM H INT , a neuro-symbolic pipeline that
tions. We thus complement them with a symbolic component                generates and validates function summaries via LLMs and
that validates each LLM-generated annotation and filters                Z3, injects them into CodeQL and Infer, and leverages
analyzer output against path feasibility constraints using              Z3 and a final LLM pass to suppress false alarms. Our
the Z3 Satisfiability Modulo Theories (SMT) solver [35].                replication package is available at https://github.com/jie
By composing the two, existing static analyzers can be                  keshi/MemHint.
augmented for more precise memory leak detection.                    • We evaluate M EM H INT on eight real-world C/C++
    Concretely, M EM H INT operates in three stages. It first           projects and detect 54 unique memory leak bugs (all
parses the target codebase to extract macros and functions              confirmed or fixed), outperforming vanilla CodeQL (19),
along with their signatures, bodies, and callees. An LLM                vanilla Infer (3), Semgrep (2), and LeakGuard (20).
(Gemini 3 in our study) then analyzes each function and
its callees to label it as a memory allocator, deallocator,
or neither, producing a function summary that records the            2. Motivating Example
function’s MM role and which argument or return value
carries memory ownership. Since LLMs may produce in-                      This section motivates M EM H INT by showing why cur-
correct annotations, M EM H INT further constructs a control-        rent approaches fall short on memory leak detection.
flow graph for each annotated function and encodes its path               Prior work has explored dynamic analysis ap-
conditions into Z3 to check whether the claimed allocation           proaches [37], particularly fuzzing [8]–[11], for detecting
or deallocation is reachable on any feasible path, discarding        memory leaks. These techniques combine coverage-guided
unsound annotations. In the second stage, the validated MM           input generation with runtime sanitizers (e.g., LeakSan-
function summaries are injected into static analyzers (Cod-          itizer [38]) that monitor memory allocation/deallocation
eQL and Infer) via their respective extension mechanisms.            events along executed paths. However, dynamic approaches
In the final stage, M EM H INT uses Z3 to check whether              can only detect leaks along paths that the fuzzer actually
each reported leak path is feasible and discards warnings on         exercises, and may silently miss leaks that require specific
infeasible paths; a final LLM-based validation step confirms         branch combinations that are difficult to reach through
whether each remaining warning is a genuine bug.                     crafted inputs. Figure 1 illustrates this limitation with a
    We evaluate M EM H INT on eight widely-used open-                confirmed memory leak in OpenSSL (v3.6.1), one of the
source C/C++ projects totaling over 3.6 million lines of             most widely used cryptographic libraries [21]. The func-
code. M EM H INT detects 54 unique memory leak bugs, all of          tion X509_policy_check() allocates a policy tree via
which have been confirmed or fixed by project maintainers            tree_init (➊). When the tree is non-explicit and empty,
or through our submitted patches. In comparison, current             the function correctly frees it before returning; yet when it is
open-source and industrial-strength static analyzers detect          both EXPLICIT and EMPTY (➋), the function returns without
far fewer: the best-performing baseline, vanilla CodeQL,             freeing the tree, leaking the allocated memory. Triggering
finds only 19, while vanilla Infer detects only 3, Sem-              this path requires an input satisfying both conditions simul-
grep [36] only 2, and the recent state-of-the-art academic           taneously, which a fuzzer may not systematically produce.


                                                                 2
   Finding
 Finding   Memory
         Memory   LeaksininC/C++
                Leaks       C/C++Programs
                                  Programsvia
                                            viaNeuro-Symbolic
                                                Neuro-SymbolicAugmented
                                                               AugmentedStatic
                                                                         StaticAnalysis
                                                                                Analysis                                                    Conferenceacronym
                                                                                                                                           Conference  acronym’XX,
                                                                                                                                                               ’XX,June
                                                                                                                                                                    June03–05,
                                                                                                                                                                        03–05, 2018,
                                                                                                                                                                               2018, Woodstock,
                                                                                                                                                                                     Woodstock, NY
                                                                                                                                                                                                NY


 1 1      /*/*openssl/crypto/x509/pcy_tree.c
                openssl/crypto/x509/pcy_tree.c (v3.6.1)
                                                  (v3.6.1)*/*/                                                    11     /* FreeRDP/libfreerdp/core/settings.c
                                                                                                                        /*   FreeRDP/libfreerdp/core/settings.c (FreeRDP (FreeRDP v3.23.0)
                                                                                                                                                                                  v3.23.0) */
                                                                                                                                                                                           */
 2 2        intX509_policy_check(X509_POLICY_TREE
          int    X509_policy_check(X509_POLICY_TREE**ptree,
                                                      **ptree,                                                    22     static BOOL
                                                                                                                        static    BOOL freerdp_settings_int_buffer_copy(rdpSettings*
                                                                                                                                        freerdp_settings_int_buffer_copy(rdpSettings*
 3 3             int*pexplicit_policy,
               int    *pexplicit_policy,STACK_OF(X509)
                                          STACK_OF(X509)*certs,
                                                         *certs,...)
                                                                  ...)                                                   ↩→ _settings,
                                                                                                                        ↩→                 const rdpSettings*
                                                                                                                              _settings, const     rdpSettings* settings)
                                                                                                                                                                   settings)
 4 4      {{                                                                                                      33    {{
 5 5             X509_POLICY_TREE   *tree = NULL;
               X509_POLICY_TREE *tree = NULL;                                                                     44          ...
                                                                                                                             ...
 6 6             ...
               ...                                                                                                55          if (settings->RdpServerCertificate)
                                                                                                                             if   (settings->RdpServerCertificate)
                    init_ret= = tree_init(&tree,
                                 tree_init(&tree,certs,
                                                  certs,flags);
                                                          flags);                                                 66         {{
 7 7           ➊➊init_ret                                                                                                             rdpCertificate* certcert ==
                                                                                                                  77              ➊➊ rdpCertificate*
 8 8
                                                                                                                  88                     freerdp_certificate_clone ((
                                                                                                                                        freerdp_certificate_clone
 9 9          ifif(init_ret
                    (init_ret<=<=0)0)
                     returninit_ret;
                            init_ret;                                                                             99                         settings->RdpServerCertificate);
                                                                                                                                            settings->RdpServerCertificate);
10 10              return
                                                                                                                 1010              if (!cert)
                                                                                                                                  if   (!cert)
11 11
                                                                                                                 1111                   goto out_fail;
                                                                                                                                       goto   out_fail;
12 12         ifif((init_ret
                    ((init_ret& &X509_PCY_TREE_EXPLICIT)
                                   X509_PCY_TREE_EXPLICIT)====0)0){ {
                                                                                                                                      if (!freerdp_settings_set_pointer_len(
                                                                                                                                          (!freerdp_settings_set_pointer_len(
                                                                                                                 1212             ➋➋ if
13 13              ifif(init_ret
                         (init_ret& &X509_PCY_TREE_EMPTY)
                                      X509_PCY_TREE_EMPTY){ {
                                                                                                                 1313                   _settings, FreeRDP_RdpServerCertificate,
                                                                                                                                       _settings,    FreeRDP_RdpServerCertificate, cert,
                                                                                                                                                                                       cert, 1))
                                                                                                                                                                                              1))
14 14                      X509_policy_tree_free(tree); /*/*tree
                         X509_policy_tree_free(tree);         treefreed
                                                                     freed*/*/                                                           goto out_fail;
                                                                                                                                               out_fail; /*      cert leaked
                                                                                                                                                             /* cert   leaked */
                                                                                                                                                                              */
                                                                                                                 1414                   goto
15 15                     returnX509_PCY_TREE_VALID;
                        return    X509_PCY_TREE_VALID;
                                                                                                                 1515        }}
16 16              }}                                                                                            1616         ...
                                                                                                                             ...
17 17              else{ {
              } }else                                                                                            1717    out_fail:
                                                                                                                        out_fail:
18 18                *pexplicit_policy= =1;1;
                   *pexplicit_policy                                                                             1818         return rc;
                                                                                                                             return    rc; /*/* cert
                                                                                                                                                 cert is
                                                                                                                                                       is never
                                                                                                                                                           never freed
                                                                                                                                                                  freed here
                                                                                                                                                                         here */
                                                                                                                                                                               */
19 19              ➋➋ifif(init_ret
                            (init_ret& &X509_PCY_TREE_EMPTY)
                                         X509_PCY_TREE_EMPTY)                                                    1919   }}
20 20                      returnX509_PCY_TREE_FAILURE;
                         return                                treeleaked!
                                   X509_PCY_TREE_FAILURE; /*/*tree    leaked!*/*/
21 21         }}                                                                                                  11     /* FreeRDP/libfreerdp/crypto/certificate.c
                                                                                                                        /*   FreeRDP/libfreerdp/crypto/certificate.c */ */
22 22           ...
              ...
            error:                                                                                                22    ➌➌ rdpCertificate*    freerdp_certificate_clone ((
                                                                                                                            rdpCertificate* freerdp_certificate_clone
23 23     error:
                X509_policy_tree_free(tree);                                                                      33          const rdpCertificate*
                                                                                                                                     rdpCertificate* certificate)
                                                                                                                                                      certificate)
24 24         X509_policy_tree_free(tree);                                                                                   const
25 25           returnX509_PCY_TREE_INTERNAL;
              return     X509_PCY_TREE_INTERNAL;                                                                  4
                                                                                                                    4
                                                                                                                        {{
     26     }                                                                                                     5
                                                                                                                    5         rdpCertificate* _certificate
                                                                                                                             rdpCertificate*   _certificate == freerdp_certificate_new();
                                                                                                                                                                freerdp_certificate_new();
26        }                                                                                                         6         ...
                                                                                                                  6          ...
                                                                                                                  7
                                                                                                                    7         return _certificate;
                                                                                                                             return   _certificate; /*/* heap-allocated
                                                                                                                                                          heap-allocated object
                                                                                                                                                                         object */
                                                                                                                                                                                */
   Figure
 Figure
 Figure    1:1:AAmemory
         1. A     memory
                memory        leak
                         leak in
                             leak   ininOpenSSL
                                 OpenSSL OpenSSL
                                             (v3.6.1) (v3.6.1)  [51].tree_init
                                                       [21]. tree_init
                                                    (v3.6.1) [51].
                                                                             allo-
                                                                       tree_init                                  8
                                                                                                                    8
                                                                                                                        }}
 cates a policy tree ➊. The green path frees it correctly, but at ➋ the function                                    9
   allocatesa apolicy
 allocates       policytree
                          tree➊.➊.The
                                    The greenpathpathfrees
                                                        freesititcorrectly,
                                                                  correctly,but
                                                                              but                                 9
 returns without  freeing tree    (red).green
                                         24 hours of fuzzing  with LeakSanitizer                                  10
                                                                                                                 10
                                                                                                                            void freerdp_certificate_free
                                                                                                                        ➍➍ void    freerdp_certificate_free (rdpCertificate*
                                                                                                                                                             (rdpCertificate* cert)
                                                                                                                                                                              cert)
 atat➋➋the
         the   function
            function      returnswithout
                        returns      withoutfreeing
                                               freeingtree       (red).24
                                                          tree(red).    24hours
                                                                           hours
 failed to trigger this path.                                                                                     11
                                                                                                                 11     {{
 ofoffuzzing
      fuzzingwithwithLeakSanitizer
                        LeakSanitizerfailedfailedtototrigger
                                                        triggerthis
                                                                  thispath.
                                                                        path.                                     12
                                                                                                                 12
                                                                                                                              if (!cert)
                                                                                                                             if   (!cert)
                                                                                                                  13
                                                                                                                 13
                                                                                                                                   return;
                                                                                                                                  return;
                                                                                                                  14
                                                                                                                 14
                                                                                                                              certificate_free_int(cert);
                                                                                                                             certificate_free_int(cert);
                                                                                                                  15          free(cert);
          OpenSSL has been continuously fuzzed by Google’s                                                       15          free(cert);
   doesnot
does      notappear
                 appearininitsitsbug bug tracker.We      We furtherrebuilt rebuiltOpenSSL
                                                                                     OpenSSLwith    with          16
                                                                                                                        }}
                      [39] since tracker. 2016, yet further
                                                                                                                 16
 OSS-Fuzz                                                     this bug, along                 with all
   LibFuzzer[53]
LibFuzzer           [53]andandLeakSanitizer
                                 LeakSanitizer[6]       [6]enabled
                                                             enabledand    andran
                                                                                ranthe thefuzzer
                                                                                             fuzzerforfor
 other bugs found by M EM H INT, does not appear in its bug
   24  hours;      it  executed      over     9.8   billion   test   cases    yet   failed    to  detect           Figure2.2:2: A
                                                                                                                  Figure
                                                                                                                 Figure          AA memory
                                                                                                                                     memory
                                                                                                                                      memory leak  leak in
                                                                                                                                                  leak    in FreeRDP
                                                                                                                                                         in  FreeRDP      (v3.23.0) [52].
                                                                                                                                                              FreeRDP (v3.23.0)
                                                                                                                                                                          (v3.23.0)     [52]. If
                                                                                                                                                                                        [41].   If
                                                                                                                                                                                                If
24   hours; We
 tracker.       it executed
                        furtherover        9.8 billion
                                     rebuilt        OpenSSL test cases withyet    failed to detect
                                                                                LibFuzzer           [40]                                                     fails (➋), the  object
                                                                                                                                                                                 (➋), allocated
   thisbug,
this     bug,suggesting
                  suggestingthat   thatsuchsuchpath-dependent
                                                    path-dependentleaks      leaksare aredifficult
                                                                                            difficulttoto          freerdp_settings_set_pointer_len
                                                                                                                 freerdp_settings_set_pointer_len                          fails
                                                                                                                  freerdp_settings_set_pointer_len fails (➋), the object allocated
                                                                                                                                                                                       the object
 and     LeakSanitizer
   reliably     detect     via     [38]
                                 dynamic     enabled
                                                 analysis.   and
                                                               Staticran    the
                                                                         analysis  fuzzer
                                                                                       is       for 24a
                                                                                          therefore                bythe
                                                                                                                       thecustom
                                                                                                                 allocated
                                                                                                                  by       custom
                                                                                                                           by          allocator
                                                                                                                               the custom   allocator freerdp_certificate_clone
                                                                                                                                                   freerdp_certificate_clone       (➊) is
                                                                                                                                                                                        is never
                                                                                                                                                                                           never
reliably      detect     via dynamic          analysis.      Static    analysis
                                                                           cases is      therefore     a         (➊)  is never  freed.allocator          miss this bug as neither(➊)
                                                                                                                                                  freerdp_certificate_clone
                                                                                                                                        Static analyzers
 hours;      it   executed
   naturalcomplement,
               complement,         over
                                   asititcan 9.8
                                           can       billion
                                                  reason          test
                                                            overall allprogram
                                                                         program     yet
                                                                                      paths  failed
                                                                                               without to          freed.
                                                                                                                  freed.   Static
                                                                                                                          Static    analyzers
                                                                                                                                   analyzers      miss
                                                                                                                                                 miss   this
                                                                                                                                                       this  bug as
                                                                                                                                                             bug   as neither
                                                                                                                                                                      neither thethethe  allocator
                                                                                                                                                                                      allocator
                                                                                                                                                                                      allocator
natural
 detect      thisexecution.      as
                      bug, suggesting           reason
                                                    that  over
                                                            suchstaticpath-dependentpaths     without
                                                                                                  leaks
                                                                                                                 nor its paired deallocator (➍) is a known MM function.
                                                                                                                  norits
                                                                                                                      itspaired
                                                                                                                          paireddeallocator
                                                                                                                                 deallocator(➍)
                                                                                                                                             (➍)is
                                                                                                                                                 is aa known
                                                                                                                                                       known MM
                                                                                                                                                             MM function.
                                                                                                                                                                function.
   requiring
requiring       execution.          However,current
                                  However,           current                analyzersstill
                                                                static analyzers            stillsuffer
                                                                                                  suffer         nor
 are    difficult
   fromseveral          to
           severallimitationsreliably
                        limitationsthat     detect
                                          thatMemHint    via    dynamic
                                                  MemHintisisdesigned           analysis.
                                                                       designedtotoaddress.
                                                                                          address.Static
from
       Thefirst
 analysis
     The      first
                 is and
                   and      foremost
                       therefore
                          foremost
                                        a limitation       isthat
                                                              thatthese
                                            natural complement,
                                        limitation       is           thesetools
                                                                               tools
                                                                                  as cannot
                                                                                         it canrecog-
                                                                                     cannot
                                                                                                    rea-
                                                                                                 recog-
   nize
 son      custom
         over       allmemory
                          program    management
                                            paths without  functions.       Real-world
                                                                        requiring             software
                                                                                          execution.                  Figure When
                                                                                                                   memory. When
                                                                                                                                 2 illustrates        this limitation with a real-world
                                                                                                                                         freerdp_settings_set_pointer_len fails (➋), ex-
nize    customcurrentmemorystatic  management            functions.        Real-world        software             memory.
                                                                                                                 memory       leak    in   FreeRDP        (v3.23.0), a widely fails
                                                                                                                                        freerdp_settings_set_pointer_len                 used(➋),open-ex-
   oftenimplements
 However,
often       implementsproject-specific
                                 project-specific
                                              analyzers
                                                         MMMMstill functions
                                                                         suffer
                                                                 functions         that
                                                                                 that
                                                                                     from  wrap
                                                                                          wrap      stan-
                                                                                               several
                                                                                                  stan-            ecution jumps
                                                                                                                  ecution     jumps to to out_fail
                                                                                                                                            out_fail without calling the paired dealloca-
                                                                                                                                                       without     calling    the paired dealloca-
   dard primitives
 limitations          that such
                             M EMasHmalloc INT isand        free behind
                                                        designed                multiple layers of
                                                                         to address.                             source     Remote         Desktop        Protocol       implementation
                                                                                                                   tor freerdp_certificate_free (➍), leaking the certificate. Existing             [41].
dard primitives such as malloc and free behind multiple layers of                                                 tor freerdp_certificate_free (➍), leaking          (➊, the➌)  certificate.
                                                                                                                                                                                     is two
                                                                                                                                                                                          a MM Existing
                                                                                                                                                                                               custom
   abstraction
       The first[12,and     59]. foremost
                                   Although the          underlyingisprimitives
                                                      limitation              that these     are transi-
                                                                                                   tools           static analyzers miss this bug entirely: neither
                                                                                                                 freerdp_certificate_clone                                     of the               func-
abstraction [12, 59]. Although the underlying primitives are transi-                                              static analyzers
                                                                                                                 allocator     that   miss this bug entirely:
                                                                                                                                      deep-copies        a          neitherinto
                                                                                                                                                             certificate       of the  two memory.
                                                                                                                                                                                    heap     MM func-
   tively reachable,
 cannot       recognize      static   analyzers
                                  custom               such asmanagement
                                                  memory           CodeQL [17], Clang              Static
                                                                                           functions.              tions, freerdp_certificate_clone and freerdp_certificate_free,
tively reachable, static analyzers such as CodeQL [17], Clang Static                                              tions, freerdp_certificate_clone              and freerdp_certificate_free        fails,
   Analyzer [41],
 Real-world                and Infer
                       software           [13] do
                                      often            not fully inline
                                                  implements                   every functionMM
                                                                        project-specific              but          has a predefined
                                                                                                                 When                    summary in their memory model, and the multi-
                                                                                                                               freerdp_settings_set_pointer_len
Analyzer [41], and Infer [13] do not fully inline every function but                                              has  a predefined     summary       in  their  memory      model,    and   the  multi-
   instead rely
 functions         thatonwrap
                            predefined
                                    standard  function      summaries,
                                                     primitives         such   which
                                                                                 as mallocare abstract
                                                                                                     and           layer delegation
                                                                                                                 (➋),     execution within  jumps thesetowrappers
                                                                                                                                                              out_fail preventswithout
                                                                                                                                                                                   the analyzer     from
                                                                                                                                                                                                calling
instead rely on predefined function summaries, which are abstract                                                 layer paired
                                                                                                                         delegationdeallocator
                                                                                                                                       within these wrappers          prevents the analyzer from
   descriptions
 free       behindofmultiplehow a function layersaffects        memory (e.g.,
                                                        of abstraction             [2],“malloc
                                                                                            [19].takes
                                                                                                     Al-           tracking the underlying
                                                                                                                 the                              primitives    (e.g., freerdp_certificate_free
                                                                                                                                                           freerdp_certificate_free
descriptions of how a function affects memory (e.g., “malloc takes                                                tracking   the underlying      primitives (e.g.,     freerdp_certificate_free
   a size argument
 though       the            and returns
                       underlying                 a heap-allocated
                                          primitives          are           pointer”),reachable,
                                                                     transitively           for a fixed          (➍),     leaking      the certificate.
                                                                                                                   → certificate_free_int           → X509_free       → free in
                                                                                                                                                                 Existing           one of analyzers
                                                                                                                                                                                 static     FreeRDP’s
a size argument and returns a heap-allocated pointer”), for a fixed                                               →   certificate_free_int → X509_free → free in one of FreeRDP’s
   set of analyzers
 static     standard primitives.
                               such asFor       For custom[14],
                                               CodeQL             wrappers Clang  outside
                                                                                       Static  this set,           deallocators)
                                                                                                                 miss      this bug across entirely:
                                                                                                                                              call boundaries.
                                                                                                                                                             neither of the two MM
set   of standard primitives.                       custom wrappers              outside      thisAna-
                                                                                                     set,         deallocators) across       call boundaries.
   the analyzer
 lyzer    [42],         hasInfer
                      and     no summary
                                       [15]      do and
                                                      not thus
                                                             fullycannot
                                                                       inline determine
                                                                                  every        whether
                                                                                             function                  Several studiesfreerdp_certificate_clone
                                                                                                                 functions,                have attempted to identify custom MM functions            and
the analyzer has no summary and thus cannot determine whether                                                        Several studies have attempted to identify custom MM functions
   a call  allocates       or frees     memory.functionEven if the        analyzer attempted           to          using heuristics, machine learning,, or natural
                                                                                                                 freerdp_certificate_free                              has language
                                                                                                                                                                                  a         processing
                                                                                                                                                                                          predefined
abut
   callinstead
         allocates    rely
                         or on
                             freespredefined
                                     memory. Even             if thesummaries,
                                                                        analyzer attempted which are  to          using heuristics, machine learning, or natural language processing
   look inside
 abstract             these wrappers
               descriptions           of   how for astandard
                                                       function   primitives,
                                                                       affects      multi-layer
                                                                                   memory             del-
                                                                                                  (e.g.,           (NLP) over function
                                                                                                                 summary         in theirnames,        documentation,
                                                                                                                                                   memory         model,andand    usagethepatterns    [12,
                                                                                                                                                                                                 multi-
look inside these wrappers for standard primitives, multi-layer del-                                              (NLP) over function names, documentation, and usage patterns [12,
   egation and         conditional       logic wouldand     break dataflow          tracking across                38–40, 42,
                                                                                                                 layer          65]. However,within
                                                                                                                            delegation             these methods
                                                                                                                                                               theserelywrappers
                                                                                                                                                                            on surface-level     signals
                                                                                                                                                                                              prevents
egation
 “malloc     andtakesconditional
                             a sizelogicargumentwould breakreturns  dataflow      tracking across
                                                                               a heap-allocated                   38–40, 42, 65]. However, these methods rely on surface-level signals
   call  boundaries.          As   a  result,      the  analyzer       cannot      establish      that a           such analyzer
                                                                                                                 the      as naming conventions
                                                                                                                                          from tracking  and comments,        which are unreliable
                                                                                                                                                                     the underlying              prim-
call   boundaries.
 pointer”),         for aAs      a result,
                             fixed     set ofthestandard
                                                      analyzerprimitives.
                                                                     cannot establish           that a
                                                                                        For custom                such as naming conventions and comments, which are unreliable
   wrapper’s outside return value         carries      heap    ownership         orno thatsummary
                                                                                              calling a            in practice:(e.g.,
                                                                                                                 itives          a functionfreerdp_certificate_free
                                                                                                                                                named cleanup may or may not free memory               →
wrapper’s return value carries heap ownership or that calling a
 wrappers                         this     set,     the    analyzer          has                                  in practice: a function named cleanup may or may not free memory
   wrapper       constitutes       a deallocation,         leaving      allocation/deallocation                    depending on its implementation,
                                                                                                                 certificate_free_int                            and the same name
                                                                                                                                                           → X509_free                → free can carry in
wrapper
 and    thusconstitutes          a deallocation,
                  cannot determine                       leaving
                                                   whether            allocation/deallocation
                                                                  a call     allocates or frees                   depending on its implementation, and the same name can carry
   pairings      invisible     and    memory         leaks    undetected.                                          different
                                                                                                                 one           semantics across
                                                                                                                        of FreeRDP’s                 projects. Crucially,
                                                                                                                                             deallocators)       across call  these   methods do not
                                                                                                                                                                                  boundaries.
pairings invisible and memory leaks undetected.look inside these
 memory.          Even      if  the   analyzer         attempted          to                                      different semantics across projects. Crucially, these methods do not
       Figure 2 illustrates            this     limitation with a real-world                  memory               validate  whether     the have
                                                                                                                                              allocation    or deallocation    operation     is actually
     Figure 2for
 wrappers           illustrates
                         standard    this    limitation multi-layer
                                         primitives,          with a real-world  delegation  memory  and          validate  whether
                                                                                                                      Several           the allocation
                                                                                                                                  studies                  or deallocation
                                                                                                                                                      attempted                operation
                                                                                                                                                                      to identify           is actually
                                                                                                                                                                                       custom      MM
   leak  in   FreeRDP        (v3.23.0),     a  widely     used    open-source         Remote       Desk-           reachable    under  the   function’s    control  flow.  A  function    may   contain
leak   in FreeRDP
 conditional               (v3.23.0),
                       logic     woulda widely
                                             break used         open-source
                                                         dataflow        tracking    Remote
                                                                                         acrossDesk- call         reachable under
                                                                                                                 functions      usingthe    function’smachine
                                                                                                                                        heuristics,       control flow.    A function
                                                                                                                                                                      learning,           may contain
                                                                                                                                                                                    or natural      lan-
   top Protocol implementation [52]. freerdp_certificate_clone (➊,                                                 a syntactic call to free inside a branch that is never satisfiable, yet a
top   Protocol
 boundaries.          implementation
                        As a result, the[52].       analyzer        cannot establish that
                                                         freerdp_certificate_clone
   ➌) is a custom allocator that deep-copies a certificate into heap
                                                                                                     (➊,a         aheuristic
                                                                                                                    syntactic
                                                                                                                 guage          call
                                                                                                                           processingto        inside
                                                                                                                                            (NLP)
                                                                                                                                         free           a
                                                                                                                                                       overbranch  that
                                                                                                                                                               function   is never
                                                                                                                                                                             names,  satisfiable,
                                                                                                                               or NLP-based approach would incorrectly annotate it as a
                                                                                                                                                                                         documenta- yet a
➌) is a custom allocator that deep-copies a certificate into heap
 wrapper’s          return     value      carries      heap     ownership          or   that   calling            heuristic
                                                                                                                 tion,   andorusage
                                                                                                                                 NLP-based      approach
                                                                                                                                           patterns     [2], would
                                                                                                                                                               [18], incorrectly
                                                                                                                                                                        [22], [24],   annotate
                                                                                                                                                                                          [43], it[44].
                                                                                                                                                                                                     as a
 a wrapper constitutes a deallocation, leaving allocation/deal-                                                  However, these methods rely on surface-level signals such as
 location pairings invisible and memory leaks undetected.                                                        function names, which are unreliable in practice: a function


                                                                                                             3
named cleanup may or may not free memory depending on                (Summary-Augmented Analysis), the validated summaries
its implementation, and the same name can carry different            are injected into CodeQL and Infer via their extension mech-
semantics across projects. Crucially, these methods do not           anisms, while in Stage 3 (Warning Validation), M EM H INT
validate whether the allocation or deallocation operation            applies Z3-based path feasibility checking and uses an LLM
is actually reachable under the function’s control flow. A           to filter false positives and retain validated warnings.
function may contain a syntactic call to free inside a
branch that is never satisfiable, yet a heuristic or NLP-based
approach would still annotate it as a deallocator, introducing
                                                                     3.1. Stage 1: Summary Generation
false annotations that actively mislead the analyzer. Sym-
bolic validation of MM function annotations is therefore             Phase 1: Code Extraction. M EM H INT begins by parsing
necessary but absent from prior work.                                the target codebase to extract metadata for each function.
     The final limitation lies in static analyzers themselves.       Specifically, we use Tree-sitter [48], a widely-used pars-
Even when a static analyzer is given an accurate mem-                ing library, to extract each function’s name, return type,
ory model with comprehensive MM functions and their                  parameter list with types, full source body, and the set of
summaries, it may still report spurious warnings [25]–[27],          direct callee names appearing in call expressions. We also
[45]. These tools are largely path-insensitive: they merge           extract C preprocessor macros that expand to function-like
control-flow branches into a single abstract flow and cannot         constructs, converting them into the same record format so
determine whether a reported warning is reachable under              they can be analyzed for memory-management semantics. In
actual program semantics. A memory leak that appears                 addition, we collect pointer-typedef aliases, which are used
along one branch may in fact be guarded by conditions that           in the subsequent pre-filtering step to recognize pointer types
make the path infeasible at runtime, yet the tool reports it         that do not contain an explicit * in the function signature.
regardless. For example, two branches may contain mutually           Phase 2: LLM Summary Generation. In this phase,
exclusive conditions that the analyzer fails to recognize,           M EM H INT classifies each candidate function as an allocator,
causing it to report a memory leak on a path that can never          a deallocator, or neither, and produces a structured func-
execute. Without a mechanism to filter out such warnings             tion summary for each identified MM function. A function
with infeasible paths, users must manually triage a large            summary is an analyzer-agnostic annotation that records the
number of false alarms, significantly reducing the practical         function’s MM role (allocator or deallocator) and which
utility of the tool [45]–[47].                                       argument or return value carries memory ownership; it can
     M EM H INT addresses these limitations by combining             be directly translated into the extension formats of different
LLMs’ semantic understanding of code with symbolic rea-              static analyzers. To reduce LLM cost, we apply a lightweight
soning through constraint solving. M EM H INT first uses             pre-filter and retain only functions whose signatures involve
an LLM to infer the memory management roles of cus-                  pointer types (e.g., return type or parameters containing *
tom functions from their source code and callees, produc-            or pointer-typedef aliases). Macros are always retained, as
ing function summaries that extend the analyzer’s built-in           they may expand to pointer operations not visible in their
knowledge beyond the standard primitives. Each summary               signature. Entry-point and test functions (e.g., main, wmain,
is then validated by Z3 against the function’s intraprocedural       and functions whose names contain test) are excluded.
control-flow graph, ensuring that the identified allocation              Each remaining function is analyzed by an LLM using
or deallocation is reachable on a feasible path. In addition,        its signature, full source body, and the source code of up
M EM H INT encodes each analyzer warning as a path con-              to five direct callees as context (the full prompt template
straint and uses Z3 to discard those on infeasible paths,            is given in Appendix A.1). Providing callee context
reducing false alarms before they reach the developer. To-           is important because many project-specific memory-
gether, these steps form a neuro-symbolic pipeline in which          management functions delegate to helper functions, making
semantic understanding and formal reasoning reinforce each           their semantics non-local. Functions classified as neither
other at every stage.                                                are discarded. For each identified MM function, the
                                                                     LLM produces a structured function summary containing
3. M EM H INT                                                        three fields: (1) name, the function’s name identifier;
                                                                     (2) role, the function’s memory management role, either
    As shown in Figure 3, M EM H INT operates in three               A LLOCATOR or D EALLOCATOR; and (3) target, which
stages. In Stage 1 (Summary Generation), M EM H INT parses           specifies return for allocators (indicating the return
the target codebase to extract each function’s metadata              value carries heap ownership) or argi for deallocators
(e.g., signature, body, callees), and filters functions via          (indicating the i-th argument is freed). For example,
pointer-type heuristics. An LLM then classifies potential            given freerdp_certificate_clone in Figure 2, the
MM functions and produces structured function summaries              LLM produces {name: freerdp_certificate_clone,
that specify whether a function acts as a memory allocator           role: Allocator, target: return}, as it calls
or deallocator and which argument or return value carries            freerdp_certificate_new and returns the newly allo-
ownership. Each summary is validated with the Z3 SMT                 cated pointer. Conversely, freerdp_certificate_free
solver [35] to ensure the claimed allocation or deallocation         yields {role: Deallocator, target: arg0}, as it
is reachable on a feasible control-flow path. In Stage 2             frees its first argument.


                                                                 4
                                                                                                  Stage II: Summary-
                                    Stage I: Summary Generation                                                                 Stage III: Warning Validation
                                                                                                 Augmented Analysis
                           1                       2                        3                               4                         5                     6
                     Code                     LLM Summary            Z3 Summary                       Static Analysis            Z3 Path              LLM Warning
                   Extraction                  Generation             Validation                                             Feasibility Filter        Validation
                                                                                                        SAST Tools          Warning         CFG
                      Functions                                  Summary           CFG                                                                 Function
                                                                                                                            Reports       Summaries      Body
                      Macros
 C/C++                                                                                                                                                              Validated
Codebase          Pointer Typedef                                        Validated               CodeQL          Infer        Feasible Warning         Warning      Warnings
                      Aliases                                            Summary                                                   Reports            Trace Code




Figure 3. Overview of the M EM H INT pipeline. Stage 1 (Summary Generation): extract metadata, generate summaries with an LLM, and validate with
Z3 SMT solver. Stage 2 (Summary-Augmented Analysis): inject validated summaries into static analyzers (e.g., CodeQL, Infer). Stage 3 (Warning
Validation): filter infeasible warnings with Z3 and validate remaining ones using an LLM.


     (a) Valid Allocator                                (b) Rejected Allocator                             This step also leverages callee information from Phase 2
                   Entry                                                   Entry                           to handle interprocedural cases by following transitive call
                                                                                                           chains up to a bounded depth, correctly validating sum-
                      b1                                                    b1                             maries involving transitive delegation (e.g., a wrapper that
              T                 F                                    T               F                     calls another wrapper before reaching malloc), parameter
      Alloc                     Ret NULL                     Alloc                    Ret NULL             aliasing (e.g., assigning a parameter to a local variable
                                                                                                           before freeing it), and indirect parameter derivation (e.g.,
     Ret ptr                                                 Free                                          freeing a field of a struct parameter rather than the parameter
   Z3: S AT ✓                                                                                              itself). Note that the alias analysis is intraprocedural and
                                                           Ret NULL                                        identifier-based: it tracks assignments of the form v = p
                                                         Z3: U NSAT ✗                                      and v = p->f together with their transitive closure, which
                                                                                                           suffices to recognize a free(v) as freeing parameter i
   (c) Valid Deallocator                               (d) Rejected Deallocator                            when v is derived from it. Transitive allocator and deal-
                        Entry                                                        Entry                 locator validation follows the project call graph up to a
                                                                                                           fixed depth bound (10 in our implementation), which ensures
                           b1                                                         b1                   termination on recursive and mutually recursive code.
                  T                  F                                        T              F                  We first describe how the CFG is constructed. For each
    free(arg0)                       Return                free(arg0->f)                     Return        function to be validated, M EM H INT parses its source and
                                                                                                           builds an intraprocedural control-flow graph (CFG) with a
       Return                                                   Return                                     designated E NTRY node and one or more E XIT nodes, as
     Z3: S AT ✓                                        arg0->f ̸= alias of arg0                            illustrated in Figure 4. Each node is assigned a semantic
                                                            Z3: U NSAT ✗                                   type: A LLOC for calls to allocation primitives (e.g., malloc,
Figure 4. Z3-based Summary Validation. (a)–(b) Allocator: (a) SAT: mem-                                    calloc, realloc, strdup), F REE for calls to deallocation
ory allocated at return; (b) UNSAT: memory is freed on all paths. (c)–(d)                                  primitives (e.g., free, delete), R ETURN for function ex-
Deallocator: (c) SAT: target argument is freed; (d) UNSAT: only internal                                   its, B RANCH for conditional control flow (e.g., if/else,
fields (e.g., arg0->f) are freed.
                                                                                                           switch), A SSIGN for assignments, and D EREF for pointer
                                                                                                           dereferences. Sequential statements are connected by single-
Phase 3: Z3-Based Summary Validation. LLM-generated                                                        successor edges, while each B RANCH node has two outgo-
summaries require validation before use for two reasons.                                                   ing edges corresponding to the true and false outcomes,
First, the LLM may misclassify functions; e.g., allocator-                                                 guarded by a Boolean variable bi and its negation ¬bi .
like names may not imply actual allocation, or control flow                                                     For a function labeled A LLOCATOR, M EM H INT checks
may obscure deallocation reachability. Second, operations                                                  whether there exists a feasible CFG path on which (i) a
such as malloc or free may occur only on infeasible                                                        known allocation primitive (or a transitively identified al-
paths, rendering the summary invalid. M EM H INT validates                                                 locator wrapper) is invoked, and (ii) the allocated value
each summary using the Z3 SMT solver [35]. Specifically,                                                   reaches the function’s return site without being overwritten
M EM H INT constructs an intraprocedural control-flow graph                                                or released. As illustrated in Figure 4 (a)–(b), a summary is
(CFG), encodes path conditions as constraints, and checks                                                  retained only if such a feasible path exists.
whether a feasible path exists on which the claimed alloca-                                                     Let G = (V, E) denote the intraprocedural CFG, where
tion or deallocation occurs in the corresponding MM func-                                                  each branch node v introduces a corresponding Boolean
tion. Summaries without such a feasible path are discarded,                                                variable bv . A path π = (n0 , n1 , . . . , nk ) from E NTRY to
and the remaining ones are retained as validated summaries.                                                a R ETURN node is feasible if its path condition φ(π) =


                                                                                                       5
V
  v∈branches(π) lv is satisfiable, where lv = bv if π takes the             For CodeQL, a declarative dataflow analysis
true branch at v and lv = ¬bv otherwise. Let A(π) denote               engine that traces value propagation across func-
the set of A LLOC nodes on π , and let reaches(a, r, π) be true        tion boundaries, M EM H INT injects the validated
when the value allocated at node a reaches the return site             summaries        through      its    extension     mechanism,
r along π without being overwritten or freed. An allocator             populating          allocationFunctionModel                and
summary is valid if and only if:                                       deallocationFunctionModel, which are CodeQL’s
                                                                       built-in extension points for registering custom MM
               ∃ π ∈ Paths(G), ∃ a ∈ A(π) :                            functions. With these extensions, CodeQL recognizes
                                                           (1)
                S AT φ(π) ∧ reaches(a, r, π)                           each function in an allocator summary as returning
                                                                       newly allocated memory and each function in a
If the constraint is satisfiable (SAT) for at least one path,          deallocator summary as freeing the specified argument.
the summary is retained; if it is unsatisfiable (UNSAT) for            However, CodeQL’s default memory leak queries (e.g.,
all candidate paths, the summary is discarded.                         MemoryNeverFreed, MemoryMayNotBeFreed) are largely
     For a D EALLOCATOR summary associated with argu-                  path-insensitive: they merge control-flow branches into a
ment index i, M EM H INT checks whether there exists a                 single abstract flow and check only whether a deallocation
feasible CFG path on which the value of parameter i, or                exists somewhere after an allocation, without distinguishing
a value derived from it, is passed to a known deallocation             which branch performs it. As a result, a leak that occurs
primitive. As illustrated in Figure 4 (c)–(d), a summary is            on a specific branch, such as an error-handling path that
retained only if such a path frees the target value. To track          returns early without freeing, may be missed if another
such flows, M EM H INT uses a lightweight alias analysis               branch does free the memory. To address this, M EM H INT
that records variables and fields derived from parameter i             augments CodeQL with extended queries that (i) track
and propagates this information along A SSIGN nodes. A                 deallocation on a per-branch basis, reporting a leak when
F REE node is considered a valid deallocation if its argument          any individual branch fails to free the allocated memory;
aliases parameter i under this analysis. To handle delega-             (ii) specifically model error-handling paths (e.g., goto
tion patterns, M EM H INT additionally follows transitive call         cleanup labels and early returns after failed checks) as
chains using a call graph constructed from the codebase. If a          potential leak sites; and (iii) detect cases where deallocation
callee has already been identified as a deallocator or is itself       is guarded by a condition that may not always hold, leaving
undergoing validation, the analysis recursively follows the            the memory unfreed on the alternative path.
chain up to a bounded depth.                                                For Infer, M EM H INT translates each validated summary
     Let F (π) denote the set of F REE nodes occurring on path         into the configuration format of Infer’s Pulse engine [15],
π , and let aliases(f, i, π) be true when the argument freed           a memory and value analysis engine developed by Meta
at node f is an alias of parameter i (or a value transitively          that is based on separation logic and tracks heap ownership
derived from it) along π . A deallocator summary is valid if           along execution paths. Allocator summaries are registered
and only if:                                                           via -pulse-model-alloc-pattern, so that Infer treats
                                                                       their return values as newly allocated heap objects with
               ∃ π ∈ Paths(G), ∃ f ∈ F (π) :
                                                           (2)        caller ownership; deallocator summaries are similarly reg-
                 S AT φ(π) ∧ aliases(f, i, π)                          istered so that calls to these functions are recognized as
                                                                       deallocation operations. With these summaries in place,
If the corresponding constraint is satisfiable (SAT), the
                                                                       Infer can track memory ownership through project-specific
summary is retained; otherwise (UNSAT), it is discarded.
                                                                       wrappers in the same way it handles standard primitives
Summaries that pass these checks are retained as validated
                                                                       such as malloc and free. While Infer’s Pulse complements
summaries and carried into Stage 2; the rest are discarded.
                                                                       CodeQL’s declarative dataflow analysis, both analyzers may
                                                                       still report warnings on infeasible paths, which are addressed
3.2. Stage 2: Summary-Augmented Analysis                               in the following stage.

     This stage injects the validated summaries into Cod-              3.3. Stage 3: Warning Validation
eQL [14] and Infer [15] and runs both analyzers to de-
tect memory leaks. The validated summaries are analyzer-               Phase 5: Z3-Based Path Feasibility Filtering. Static an-
agnostic: each summary specifies whether a function al-                alyzers may report memory leaks along infeasible paths,
locates or frees memory and which argument or return                   i.e., paths that exist syntactically but are unreachable at
value carries ownership, without relying on any tool-specific          runtime due to implicit invariants or mutually exclusive
representation (Appendix B shows a concrete summary and                branch conditions. To address this, M EM H INT performs an
its injected forms for CodeQL and Infer). We select CodeQL             intraprocedural analysis for each flagged function and uses
and Infer due to their complementary analysis foundations              Z3 to check whether a feasible execution path exists that
(declarative interprocedural dataflow and bi-abduction). In            exhibits the reported leak. Warnings without such a feasible
both analyzers, the summaries extend the memory model to               path are discarded.
support project-specific allocators and deallocators without                Concretely, for each warning, M EM H INT parses the
modifying the underlying codebase.                                     flagged function and constructs a CFG using the same node


                                                                   6
                                            Huihui Huang, Jieke Shi, Bo Wang, Zhou Yang, and David Lo


  along 𝜋.         FunctionCode
                  Function  Code (FreeRDP)
                                 (FreeRDP)                          CFG withwith
                                                                      CFG    Z3 State Encoding
                                                                                 Z3 State                                  chosen predecessor:
                 /* FreeRDP: freerdp_settings_int_buffer_copy */                 Encoding
                                                                                  Entry

       
                 if (settings->RdpServerCertificate)
                                                                                                                                                     _                           
                 {                                                                 Entry                                              state(n) =             e(u,n) ∧ state(u)        (4)
  𝜋)       (2)     ➊ rdpCertificate* cert =
                     freerdp_certificate_clone(...);                            ➊ Alloc: cert                                                      (u,n)∈E
                   ➋ if (!cert)
mmary is                 goto out_fail;
                                                                               ➊ Alloc: cert
                                                                                                                           Since at most one incoming edge is active (Equation 3),
                                                                                                 T
that pass
                   ➌ if (!freerdp_settings_set_pointer_len(                         ➋ 𝑏1                   ➍ Ret
                         _settings, ..., cert, 1))
                                                                                                T                          the disjunction effectively selects the state from the unique
ried into
                                                                                   ➋ b1                  ➍ Ret
                          goto out_fail;   /* cert leaked */                        F                  feasible path
                 }                                                                  F𝑏           T
                                                                                                           ➍ Ret
                                                                                                                           chosen predecessor. At A LLOC, F REE, and escape nodes,
                 ...                                                                ➌  2              feasible path
                 out_fail:                                                         ➌ b2         T
                                                                                                           ➍ Ret
                                                                                                                           the corresponding state variable is additionally set to true
                   ➍ return rc; /* no free(cert) here */                            F
                                                                                                                           when the node is reachable. A memory leak is feasible if
sis                 Key nodes: ➊ Alloc → ➋ Branch (𝑏 1 : !cert) →
                  Key nodes: ➊ Alloc → ➋ Branch (b1 : !cert) →
                                                                                    FRet
                                                                                                                           and only if:
                                                                                    Ret
  [17] and              ➌ Branch (𝑏 2 : !set_ptr) → ➍ Return
                      ➌ Branch (b2 : !set_ptr) → ➍ Return             ¬𝑏 1 ∧ 𝑏 2 : Alloc → Ret (no free)
 aks. The
                                                                        alloc=T, freed=F, escaped=F
                                                                     ¬b1 ∧ b2 : Alloc → Ret (no free)
                                                                           Z3: Sat — feasible leak
                                                                                                                                                                  ∃r ∈ Exits(G) :
                                                                       alloc=T, freed=F, escaped=F                                                                               (5)
  specifies                                                              Z3: S AT — feasible leak                           S AT reach(r) ∧ alloc(r) ∧ ¬freed (r) ∧ ¬escaped (r)
  rgument        Figure5. 5:Z3-based
                 Figure          Z3-based     memory-leak
                                        memory-leak                 feasibility
                                                      feasibility checking    (Phase checking
                                                                                      5) on the
                                                                                                                           If Z3 returns S AT, the warning is retained; otherwise
 any tool-       (Phase 5)bug
                 FreeRDP      oninthe  FreeRDP
                                    Figure 2. Left:bug  in Figure
                                                    flagged   function2. with
                                                                         Left:key
                                                                                flagged    func-
                                                                                    CFG nodes
                                                                                                                           (U NSAT), it is discarded as a false alarm. All remaining
e to their       (allocation ➊, branches ➋, ➌, return ➍). Right: intra-procedural CFG with
                 tion  with   key  CFG   nodes  (allocation     ➊,  branches      ➋, ➌,  return                            warnings are forwarded to Phase 6. Note that our CFG
 ocedural
                 Z3 encoding. Along the dashed path, cert is allocated (alloc = true )
                      Right:freed
                 ➍).neither
                 but           intra-procedural
                                   nor escaped; Z3 CFG
                                                    returnswith
                                                            SAT,Z3    encoding.
                                                                   indicating       Along
                                                                                a feasible   the
                                                                                           leak.                           models conditional, return, and goto control flow but is
maries ex-       dashed path, cert is allocated (alloc = true) but neither freed                                           acyclic: it does not currently represent loop constructs
ators and        nor escaped; Z3 returns SAT, indicating a feasible leak.                                                  (for/while/do). The leak patterns that dominate our set-
                 classification as in Phase 3. Allocation and deallocation                                                 ting, namely allocations on error branches and frees hidden
  at traces
 t injects        3.3 Stage
                 operations           3: Warning
                                  include                 Validation
                                              both standard         primitives (e.g., malloc,                              behind custom wrappers (Figures 1 and 2), arise from con-
                 free) and custom allocators/deallocators recorded in vali-                                                trol flow rather than loop iteration; loop-carried leaks are
  sm, pop-        Phasesummaries
                           5: Z3-Based(e.g.,          Feasibility Filtering. Static analyzers
                                              Pathfreerdp_certificate_clone
                 dated                                                                               in                    out of the current scope and discussed in Section 6.
 ionModel,        may    report   memory       leaks   along   infeasible
                 Figure 2). M EM H INT then                 encodes       thepaths,
                                                                                CFG i.e.,
                                                                                       as paths
                                                                                            a set that
                                                                                                     of                    Phase 6: LLM-Based Warning Validation. After Z3-based
  ring cus-       exist syntactically      but are    unreachable
                 constraints      over three       Boolean     state at    runtimethat
                                                                        variables     due track
                                                                                           to implicit
                                                                                                   the                     feasibility filtering, the remaining warnings correspond to
 izes each        invariants    or  mutually    exclusive    branch     conditions.   To address    this,
                 status of pointer p along each path:                                                                      feasible execution paths but may still include residual false
 allocated        MemHint performs an intraprocedural analysis for each flagged                                            positives that intraprocedural symbolic analysis alone cannot
 s freeing       • alloc(n): memory for p has been allocated at or before
                  function and uses Z3 to check whether a feasible execution path                                          eliminate. In particular, the Z3 encoding captures path feasi-
mory leak            node n;
                  exists that exhibits the reported leak. Warnings without such a                                          bility but not higher-level semantics such as callback-based
 e largely       • freed (n): memory for p has been freed at/before node n;
                  feasible path are discarded.                                                                             deallocation or project-specific ownership conventions (e.g.,
   a single      • escaped (n): ownership of p has been transferred at or
                      Concretely, for each warning, MemHint parses the flagged func-                                       borrowed pointers or non-owning references). For instance,
 sts some-           before node n (e.g., via return, global store, or ownership-
                  tion and constructs an intraprocedural control-flow graph (CFG),                                         in systems like Redis, certain APIs return pointers to in-
h branch             sink call).
                  following the same node classification as in Phase 3. Allocation                                         ternally managed data structures whose ownership remains
nch, such         andOnly
                        deallocation     operations
                                allocation,             include both
                                                deallocation,       and standard      primitives
                                                                           escape-related          (e.g.,
                                                                                               nodes
                                                                                                                           with the library, so the caller is not responsible for deallo-
 ing, may         malloc, free
                 update      these) and   functions
                                       states;    all identified
                                                       other nodes   by validated
                                                                            propagatesummaries
                                                                                          them un- (e.g.,                  cation; static analyzers nonetheless flag the missing free as
  ress this,     changed,       keeping the encoding
                  freerdp_certificate_clone            in Figure      2). MemHint
                                                                  lightweight.         then
                                                                                     The      encodes
                                                                                           encoding
                                                                                                                           a leak. Such conventions are encoded in API documentation
   (i) track      the CFG
                 does    notasmodel
                                 a set of   constraints
                                          pointer   values, thatheap
                                                                  trackcells,
                                                                          threeorBoolean    state vari-
                                                                                    array theories.
                                                                                                                           rather than in code structure, placing them beyond the reach
 n any in-        ables along each path for the tracked pointer 𝑝: allocator and
                 Because       Phase     3  has   already     labeled      custom
                                                                                                                           of constraint-based reasoning.
 ecifically       • alloc(𝑛): memory
                 deallocator       wrappers  foras𝑝 has   been allocated
                                                      A LLOC      or F REE,atPhaseor before
                                                                                         5 cannodestay
                                                                                                     𝑛;
   early re-
                                                                                                                                For each candidate warning, M EM H INT constructs a
                  • freed (𝑛): memory
                 intraprocedural:             for 𝑝the
                                           when      has function
                                                          been freedunder at or before   nodecalls
                                                                                  analysis      𝑛; a                       prompt that includes (i) the full source code of the function,
  ect cases      deallocator          ownership
                  • escaped (𝑛):wrapper,         M EMof H   has been
                                                         𝑝 INT    treatstransferred
                                                                            the call siteat itself
                                                                                            or beforeas
  t always
                                                                                                                           (ii) the warning type (memory leak) together with the warn-
                 a F node 𝑛 (e.g., via return, global store, or ownership-sink call).
                       REE     node,     without     analyzing       the   wrapper’s      body.    For
                                                                                                                           ing message and location, and (iii) the analysis path reported
h.               each Only   allocation,
                         allocation         deallocation,
                                         site,  M EM H INTand        escape-related
                                                                 checks      whether nodes      update
                                                                                        there exists
   into the      athese                                                                                                    by the static analysis tool (i.e., the CodeQL dataflow path
                          states; all other nodes propagate them unchanged,
                    feasible     path    from    the  allocation       to  a  function   exitkeeping
                                                                                                along
                                                                                                                           or Infer error trace), with code snippets at each program
mory and          the encoding
                 which              lightweight.
                           the pointer              For each
                                            is neither    freedallocation     site, MemHint checks
                                                                   nor ownership-transferred.
  paration
                                                                                                                           point. The LLM is asked to determine whether the reported
                  whether
                 As    shown  there   exists a5,feasible
                                 in Figure         such apath pathfrom     the allocation
                                                                      reaches     a R ETURN  to anode
                                                                                                  func-                    warning corresponds to a real bug or a false positive, to-
Allocator         tion exit along which the pointer is neither freed nor ownership-
                 without      encountering        a  matching       deallocation.
 n, so that
                                                                                                                           gether with a brief justification. Warnings classified as false
                  transferred.
                       To enforce  As shown
                                        a singleinconcrete
                                                     Figure 5, path,
                                                                 such aMpath EM H reaches   a Return
                                                                                    INT introduces
                                                                                                                           positive are discarded, and the remaining ones are reported
 ects with       anode   without encountering a matching
                     Boolean       edge     variable     e (u,v)    for deallocation. edge and
                                                                          each     CFG
egistered
                                                                                                                           as the final output. The full prompt template is given in
                      To enforce
                 constrains         a single
                                 each    nodeconcrete     path,at
                                                 to receive      MemHint
                                                                     most one   introduces
                                                                                   incoming a Boolean
                                                                                                edge:
                                                                                                                           Appendix A.2.
 ation op-       edge variable 𝑒 (𝑢,𝑣) for each CFG edge and constrains each node to
  memory         receive at
                         ∀ nmost
                              ∈ Vone    incoming
                                          T M OST 1edge:
                                                                             
                                                     {e(u,n) | (u, n) ∈ E}
                                                                          
                                     : A                                             (3)
me way it                                                                                                                  4. Evaluation
                              ∀ 𝑛 ∈ 𝑉 : AtMost1 {𝑒 (𝑢,𝑛) | (𝑢, 𝑛) ∈ 𝐸}                 (3)
 le Infer’s
                                                                   Ôreach(n)
  sis, both      Node reachability is defined as reach(𝑛) ⇔ (𝑢,𝑛) ∈𝐸 𝑒 (𝑢,𝑛) , with
                 Node     reachability       is    defined    as                      ⇔                                        We evaluate M EM H INT on eight real-world C/C++
which are                              The three state  variables are propagated   along
                 W
                   (u,n)∈E e(u,n)
                 reach(Entry)   = ⊤., with    reach(  E NTRY  ) =     ⊤. The three                                         projects, manually inspecting every warning and submitting
                 the selected
                 state        path. are
                        variables     At each  non-special
                                           propagated       node,the
                                                         along    the state is inherited
                                                                       selected   path.                                    confirmed cases to upstream maintainers. Our evaluation
                 At each non-special node, the state is inherited from the                                                 answers four questions: (i) the Bug-Finding Effectiveness


                                                                                                                       7
of M EM H INT, measured by discovered bugs and compari-              approach operating at a different abstraction level. We use
son with prior tools; (ii) the Summary Quality of inferred           Semgrep version 1.156.0 with the Pro engine enabled.
MM-function annotations, measured by precision and recall;                Table 2 reports the number of detected bugs per project
(iii) the Component Contribution of each pipeline stage              for each tool. All bugs found by the baseline tools are
to final detection performance; and (iv) the Efficiency of           strict subsets of those found by M EM H INT, and 20 bugs are
M EM H INT, measured by runtime and cost.                            uniquely found by M EM H INT. Vanilla CodeQL detects 19
                                                                     bugs; notably, running CodeQL with our extended queries
4.1. Experiment Setup                                                but without summary injection produces the same 19 bugs
                                                                     (marked with ∗ in Table 2), indicating that the additional
                                                                     detections are attributable to the summaries rather than the
    In Phase 2 (LLM summary generation), we use Gemini
                                                                     enhanced queries alone. Vanilla Infer detects only 3 bugs.
3 Flash, while in Phase 6 (LLM warning validation), we
                                                                     Without summaries, neither tool can track object lifetimes
use Gemini 3.1 Pro. We choose a lightweight model for
                                                                     through project-specific allocators and deallocators, miss-
summary generation because it needs to process a large
                                                                     ing a substantial number of leaks. LeakGuard detects 20
number of functions, where efficiency and cost are critical,
                                                                     bugs; although it identifies custom memory-management
whereas warning validation requires higher accuracy and
                                                                     functions, it misses leaks that require deeper interprocedural
thus benefits from a stronger model. When invoking the
                                                                     reasoning or that arise from complex control-flow patterns.
LLM, we follow the batching strategy of Li et al.’s work [49]
                                                                     Semgrep detects only 2 bugs, as its purely syntactic analysis
to reduce latency. Specifically, we batch multiple queries
                                                                     lacks the data-flow and path-sensitive reasoning required to
into a single prompt, using a batch size of 20 functions
                                                                     detect interprocedural leaks involving custom allocators.
per call for summary generation (Phase 2). For LLM-based
                                                                          Overall, M EM H INT outperforms all baselines in terms
validation (Phase 6), we validate one function per call.
                                                                     of confirmed bugs while maintaining competitive precision,
    We use CodeQL CLI version 2.23.9, Infer ver-
                                                                     highlighting the benefit of combining LLM-assisted sum-
sion 1.2.0, and Z3 version 4.15.4. We evaluate M EM H INT
                                                                     mary generation with Z3-based symbolic validation.
on eight widely used open-source C/C++ projects: Vim,
tmux, OpenSSL, Redis, FreeRDP, curl, FFmpeg, and the
linux/drivers/staging subsystem of the Linux ker-                    4.3. Summary Quality
nel, which we refer to as linux/staging hereafter. For
                                                                         To evaluate summary generation, we construct a human-
each project, we run the full M EM H INT pipeline (Stages 1–
                                                                     labeled dataset of functions drawn from the subject
3) on the entire codebase.
                                                                     projects, partitioned into three ground-truth categories:
                                                                     (1) MM + Reachable: custom MM functions whose allo-
4.2. Bug-Finding Effectiveness                                       cation or deallocation is on a feasible control-flow path;
                                                                     (2) MM + Not Reachable: custom MM functions that contain
    Table 1 summarizes the bug detection results of                  allocation or deallocation calls, but the call site lies on
M EM H INT across all eight projects. In total, M EM H INT           an infeasible path (e.g., guarded by an unsatisfiable con-
detects 54 unique memory-safety bugs, all of which have              dition); and (3) Not MM: functions that are not memory-
been confirmed or fixed by project maintainers or through            management functions. This three-way split allows us to
our submitted patches. As CodeQL and Infer both receive              evaluate the LLM and Z3 components separately: the LLM
the same validated summaries, they share 21 overlapping              should classify both MM categories as MM functions and re-
findings that both analyzers can detect once project-specific        ject Not MM; Z3 should retain MM + Reachable summaries
memory models are provided. However, CodeQL contributes              and discard MM + Not Reachable summaries.
44 findings and Infer contributes 31, leaving 23 bugs found          Dataset Construction. The full candidate pool comprises
only by CodeQL and 10 found only by Infer. The non-                  88,474 functions that pass the pointer-type pre-filter (Phase 1
overlap reflects differences in analysis strategy: CodeQL’s          in Stage 1) across the eight subject projects. Applying
declarative dataflow queries and Infer’s bi-abductive reason-        Cochran’s finite-population sample-size formula [50] at
ing capture complementary patterns.                                  95% confidence and 5% margin of error yields nadj =
Comparison with Baselines. We compare M EM H INT                     383 samples per comparison side (full derivation in Ap-
against four baselines: vanilla CodeQL [14], vanilla In-             pendix C). Because our evaluation involves two compar-
fer [15], LeakGuard [24], and Semgrep [36]. Vanilla Cod-             isons, namely (i) MM vs. Not MM for evaluating the LLM,
eQL and vanilla Infer serve as the most direct baselines,            and (ii) MM + Reachable vs. MM + Not Reachable for eval-
representing what off-the-shelf compilation-level static anal-       uating Z3, we sample 383 functions from each of the
ysis tools can detect without custom memory-model annota-            three classes, with Not MM doubled (383 × 2 = 766)
tions. LeakGuard is a state-of-the-art memory-leak detection         to balance against the combined MM pool. Samples are
approach that infers paired memory-management functions              allocated equally across the eight projects, with approx-
and integrates them into static analysis. We use the authors’        imately 48 functions per project per class. This yields
released implementation. Semgrep is a widely used source-            383 MM + Reachable, 383 MM + Not Reachable, and 766
level static analyzer that does not require compilation; we          Not MM functions, for 1,532 functions in total. To mitigate
include it to provide a comparison with a pattern-based              subjective bias, each function was independently labeled by


                                                                 8
                                                  TABLE 1. B UGS FOUND BY M EM H INT ACROSS PROGRAMS .

                                                                                                                       M EM H INT
       Program            Type                     Version         SLOC        #Func.       CodeQL         Infer      Overlap Detected               Confirmed
       Vim                Text Editor              9.2.0015         429K        10.9K            18           15           11       22                      22
       Tmux               Terminal Tool            3.6a              75K         2.5K             9            6            5       10                      10
       OpenSSL            Crypto Library           3.6.1            725K        20.7K             4            6            1        9                       9
       Redis              Database System          8.6-rc1          241K         5.2K             3            0            0        3                       3
       FreeRDP            Remote Desktop           3.23.0           436K        13.2K             5            2            2        5                       5
       curl               Network Tool             8.19.0-rc3       201K         5.0K             1            1            1        1                       1
       FFmpeg             Multimedia Tool          n8.1-dev         1.3M        31.1K             2            1            1        2                       2
       linux/staging      OS Subsystem             v7.0-rc1         229K         6.3K             2            0            0        2                       2
       Total              –                        –                3.6M        94.9K            44           31           21       54                      54
      SLOC: source lines of code (excluding blanks/comments). #Func.: number of functions. CodeQL/Infer: bugs detected by each summary-augmented analyzer. Overlap:
     bugs found by both. Detected: union of validated bugs. Confirmed: bugs confirmed or fixed by maintainers.



TABLE 2. C OMPARISON OF BUGS DETECTED PER PROGRAM BETWEEN                                TABLE 4. C ONTRIBUTION OF EACH S TAGE 1 PHASE TO CANDIDATE
               M EM H INT AND BASELINE TOOLS .                                                      REDUCTION AND SUMMARY VALIDATION .

Program       CodeQL∗ Infer LeakGuard Sgrep M EM H INT                                  Program            #Extr.      #Cand.      #Summ.        #Valid.
Vim                10     3         9     0         22                                  Vim                11,071 8,539 ↓22.9% 2,539 ↓70.3%     688 ↓72.9%
Tmux                7     0         4     1         10                                  Tmux                2,612   2,528 ↓3.2%    790 ↓68.8%   467 ↓40.9%
OpenSSL             0     0         4     1          9                                  OpenSSL            24,068 20,996 ↓12.8% 3,454 ↓83.5% 1,740 ↓49.6%
Redis               0     0         2     0          3                                  Redis               5,660 4,882 ↓13.7% 1,308 ↓73.2%     493 ↓62.3%
FreeRDP             2     0         1     0          5                                  FreeRDP            13,940 12,160 ↓12.8% 2,256 ↓81.4% 1,161 ↓48.5%
curl                0     0         0     0          1                                  curl                4,978 4,413 ↓11.4%     736 ↓83.3%   219 ↓70.2%
FFmpeg              0     0         0     0          2                                  FFmpeg             29,705 27,930 ↓6.0% 3,596 ↓87.1%     494 ↓86.3%
linux/staging       0     0         0     0          2                                  linux/staging       7,614   7,026 ↓7.7%    519 ↓92.6%   120 ↓76.9%
Total              19     3        20     2         54                                  Total              99,648 88,474 ↓11.2% 15,198 ↓82.8% 5,382 ↓64.6%
∗
    same bugs with/without extended queries. Sgrep = Semgrep.                           #Extr.: parsed functions/macros. #Cand.: after pre-filtering. #Summ.: LLM-generated
                                                                                       summaries. #Valid.: Z3-validated summaries. Red numbers show reduction per step.

    TABLE 3. E VALUATION OF MM IDENTIFICATION AND VALIDATION .
                                                                                       approach correctly identifies MM functions whose allocation
                            MM                         Validated MM
                                                                                       or deallocation is on a feasible path. For LeakGuard, both
                    Precision   Recall              Precision     Recall
                                                                                       criteria are evaluated directly on its output, as it relies
LeakGuard              78.1%    59.9%                  34.0%      52.2%
                                                                                       solely on NLP-based classification without symbolic path
M EM H INT             92.0%   100.0%                 100.0%     100.0%
                                                                                       validation. For M EM H INT, the MM criterion evaluates the
 MM: MM vs. non-MM classification. Validated MM: reachable MM functions on
feasible paths.                                                                        LLM component alone (Phase 2), while the Validated MM
                                                                                       criterion evaluates the full LLM + Z3 pipeline (Phases 2–3).
                                                                                           The results confirm that M EM H INT achieves 92.0%
two authors with Cohen’s κ of 0.94 (“almost perfect” [51]);                            MM precision with 100% recall, significantly outperform-
disagreements were resolved through discussion.                                        ing LeakGuard (78.1% precision, 59.9% recall). After Z3
Results and Analysis. We evaluate using precision and                                  validation, M EM H INT achieves 100% precision and recall
recall, and compare against LeakGuard [24], a state-of-the-                            on Validated MM, demonstrating that Z3 effectively filters
art approach that infers custom MM functions by mining                                 the LLM’s false positives while preserving all true MM
allocation–deallocation usage patterns from the codebase.                              functions with feasible allocation paths.
However, such pattern-based inference relies on observable
usage and may miss implicit or less frequent MM behaviors.                             4.4. Component Contribution
We also run LeakGuard on the same eight repositories to
obtain its inferred MM functions, and evaluate its precision                               Tables 4 and 5 quantify how each component contributes
and recall on the same set of 1,532 sampled functions.                                 to the overall pipeline.
     Table 3 reports precision and recall under two evaluation                         Stage 1: Summary Generation (Table 4). The pipeline pro-
criteria. MM evaluates whether each approach correctly clas-                           gressively narrows from 99,648 extracted functions to 5,382
sifies functions as memory-management vs. non-MM: a true                               validated summaries of MM functions, achieving a 94.6%
positive is a ground-truth MM function (MM + Reachable                                 overall reduction. Pre-filtering removes 11.2% of functions
or MM + Not Reachable) correctly identified as MM; a false                             that lack pointer types in their signatures. The LLM then
positive is a Not MM function mislabeled as MM; a false                                classifies the remaining 88,474 candidates, rejecting 82.8%
negative is an MM function the approach fails to identify.                             as non-MM functions and producing 15,198 summaries. Z3
Validated MM evaluates a stricter criterion: whether each                              validation further eliminates 64.6% of these summaries that


                                                                                   9
 TABLE 5. C ONTRIBUTIONS OF S TAGES 2–3 TO WARNING FILTERING                               TABLE 6. C OST AND RUNTIME BREAKDOWN OF M EM H INT ACROSS
                      AND VALIDATION .                                                                             PROGRAMS .

  Program                      #Warn.          #Z3        #Valid.       #Det.             Program                          Gen      Vrf     Static     LeakGuard
                CodeQL          1,011       86 ↓91.5%     24 ↓72.1%   18 (75.0%)                            CodeQL                 0.46      56m
  Vim                                                                                     Vim                            10.20                                  1.4h
                Infer           1,032      147 ↓85.8%     25 ↓83.0%   15 (60.0%)                            Infer                  0.65      57m
                CodeQL            291       70 ↓75.9%     13 ↓81.4%    9 (69.2%)                            CodeQL                 0.29        3m
  Tmux                                                                                    Tmux                             2.27                                 31m
                Infer             304       36 ↓88.2%      7 ↓80.6%    6 (85.7%)                            Infer                  0.17        3m
                CodeQL            891      118 ↓86.8%     14 ↓88.1%    4 (28.6%)                            CodeQL                 0.49      1.7h
  OpenSSL                                                                                 OpenSSL                        17.00                                  7.1h
                Infer           2,078      351 ↓83.1%     27 ↓92.3%    6 (22.2%)                            Infer                  1.52      1.9h
                CodeQL            705       89 ↓87.4%      8 ↓91.0%    3 (37.5%)                            CodeQL                 0.44        8m
  Redis                                                                                   Redis                            5.83                                 38m
                Infer             198       33 ↓83.3%      0 ↓100%        0 (–)                             Infer                  0.14      10m
                CodeQL            890      141 ↓84.2%      6 ↓95.7%    5 (83.3%)
  FreeRDP                                                                                                   CodeQL                 0.52      32m
                Infer             541       82 ↓84.8%      3 ↓96.3%    2 (66.7%)          FreeRDP                        14.11                                  1.1h
                                                                                                            Infer                  0.36      27m
                CodeQL            403       47 ↓88.3%      5 ↓89.4%    1 (20.0%)
  curl                                                                                                      CodeQL                 0.21      10m
                Infer             195       37 ↓81.0%      1 ↓97.3%    1 (100%)           curl                             4.86                                 13m
                                                                                                            Infer                  0.17        8m
                CodeQL            404       80 ↓80.2%      2 ↓97.5%    2 (100%)
  FFmpeg                                                                                                    CodeQL                 0.30      48m
                Infer             184       42 ↓77.2%      1 ↓97.6%    1 (100%)           FFmpeg                         26.09                                  18m
                CodeQL            120       57 ↓52.5%      9 ↓84.2%    2 (22.2%)                            Infer                  0.17      1.1h
  linux/staging                                                                                             CodeQL                 0.73      20m
                Infer              30       14 ↓53.3%      3 ↓78.6%      0 (0%)           linux/staging                    6.65                                 3.1h
                CodeQL          4,715      688 ↓85.4%     81 ↓88.2%   44 (54.3%)                            Infer                  0.24      12m
  Total                                                                                                     CodeQL                 3.44      4.6h
                Infer           4,562      742 ↓83.7%     67 ↓91.0%   31 (46.3%)          Total                          87.01                                14.3h
  #Warn.: SAST tool output warnings. #Z3: after Z3 filtering. #Valid.: LLM-                                 Infer                  3.42      5.0h
 validated warnings. #Det.: human-validated bugs (precision). Red percentages show         Gen: LLM cost ($) for summary generation. Vrf : LLM cost ($) for warning
 reduction per step.                                                                      validation. Static: M EM H INT static-phase runtime (Phases 1, 3, 4, and 5).



lack feasible allocation or deallocation paths, retaining only                            design is that summary generation is a one-time cost; once
validated summaries. Overall, this staged filtering process                               generated and validated, summaries can be reused across
effectively identifies high-quality summaries while aggres-                               multiple analyzers, project versions, and repeated analyses
sively pruning irrelevant candidates.                                                     without regeneration. In practice, summaries only need to be
Stages 2–3: Bug Detection (Table 5). Static analysis with                                 regenerated when significant code changes occur (e.g., new
injected summaries produces over 4,500 warnings per an-                                   custom allocators or major API refactoring); incremental up-
alyzer. Z3 feasibility filtering eliminates 85.4% (CodeQL)                                dates between releases require no re-generation. This design
and 83.7% (Infer) of these warnings by discarding those                                   amortizes the upfront LLM cost over all downstream uses.
on infeasible paths. LLM-based validation further reduces                                 The static analysis phases (Phases 1, 3, 4, and 5) require
the remaining warnings by approximately 88–91%, retaining                                 approximately 35 minutes per program for CodeQL and 38
81 (CodeQL) and 67 (Infer) validated warnings. Among                                      minutes for Infer on average, confirming that the pipeline’s
these LLM-validated warnings, manual validation confirms                                  recurring cost is modest. Compared to LeakGuard, which
44 true bugs for CodeQL and 31 for Infer, corresponding to                                averages 107 minutes per program, M EM H INT achieves
precisions of 54.3% and 46.3%, respectively.                                              a 2.8–3.1× speedup in the static analysis phase. Overall,
     In summary, the false positive reduction rate exceeds                                M EM H INT demonstrates high efficiency: the most expensive
98% for both analyzers, with Z3 filtering removing most                                   step, summary generation, is shared and reusable, while all
false alarms before LLM invocation, significantly reducing                                downstream stages are fast and inexpensive.
unnecessary cost. To assess whether the LLM incorrectly
filters out true bugs, we randomly sampled 50 warnings clas-                              5. Related Work
sified as non-bugs by the LLM; none were true bugs upon
manual inspection, suggesting that LLM filtering is unlikely                              Memory Leak Bug Detection Static and dynamic tech-
to discard genuine bugs, consistent with prior work [52].                                 niques have been extensively studied for memory leak
                                                                                          detection. Static approaches include abstract interpreta-
4.5. Efficiency                                                                           tion and model checking (e.g., Sparrow [53], Infer [15]),
                                                                                          Boolean satisfiability modeling (SATURN [54]), and sym-
    Table 6 presents the cost and runtime breakdown of                                    bolic execution that tracks object lifecycles along program
M EM H INT. Summary generation dominates both cost and                                    paths (KLEE [55]). A prominent line of work reduces
runtime ($87.01 in total, approximately $10.9 per program,                                leak detection to graph reachability on sparse value-flow
and about 2.1 hours per program), as it must process all can-                             graphs (SVFGs), as in Saber [56], FastCheck [57], Pin-
didate functions across the codebase. Warning validation for                              point [58], LeakFix [59], and SMOKE [4]. Other static
each analyzer’s output incurs minimal overhead ($3.44 for                                 frameworks target specific defect patterns: partial call-
CodeQL and $3.42 for Infer), due to the aggressive filtering                              path analysis (PCA [60]), intraprocedural inconsistencies in
performed by Z3 in earlier stages. A key advantage of this                                error-handling code (Hector [61]), and practical memory


                                                                                     10
ownership models (Clouseau [62]). On the dynamic side,                 This keeps the per-warning cost negligible and suffices for
runtime monitors such as Purify [63], AddressSanitizer [13],           the error-handling and wrapper-mediated leaks that dom-
and Valgrind’s memcheck [64] instrument code to track                  inate our study (Figures 1–2), making Phase 5 an over-
memory states during execution or fuzzing [8], [9], [11],              approximation; residual false positives that depend on richer
while Sniper [65] leverages hardware-assisted instruction              semantics are deferred to the LLM validation in Phase 6.
sampling for lower overhead. A separate line of work tar-              Scope and Dependencies. M EM H INT currently targets
gets project-specific custom memory management (MM)                    memory leaks in C/C++ source parseable by Tree-sitter and
functions through heuristics, NLP, or usage-aware rules                buildable by CodeQL or Infer; related defects such as use-
(e.g., Goshawk [18], K-MELD [2], LeakGuard [24], and                   after-free and double-free are left to future work. Within this
others [22], [23], [43], [44]). However, these rely on surface-        scope, Z3 validation discards structurally invalid summaries
level signals (e.g., naming conventions, comments) and do              and infeasible warnings, but cannot detect a semantically
not verify whether the inferred allocation or deallocation             incorrect summary that nonetheless admits a feasible path;
operations are reachable under the function’s control flow. In         such cases rely on the final LLM validation. As noted in
contrast, M EM H INT combines LLM-based annotation with                our LLM usage statement, detection also depends on the
Z3-based symbolic validation to verify the reachability of             specific LLM and prompts, affecting reproducibility when
inferred annotations and filter out infeasible leak paths.             the model is not openly available. We mitigate this with Z3
LLM-assisted Static Analysis Large Language Models                     validation of every summary and a second LLM pass on
(LLMs) have been integrated into static analysis to bridge             surviving warnings, but the dependence remains.
the semantic gap between code structures and developer                 Future Work. First, we plan to strengthen the symbolic
intent. One line of work focuses on automated specification            layer with bounded loop unrolling, interpreted branch con-
and annotation inference: frameworks such as IRIS [49]                 ditions to refute semantically infeasible paths, and a parti-
and LAMeD [19] extract source and sink metadata to guide               tioned memory model for aliasing and heap updates. Second,
external analyzers and mitigate path explosion, while Spec-            since the allocator/deallocator summary abstraction is not
Gen [66] and AutoSpec [67] leverage LLMs to synthesize                 specific to leaks, we plan to extend it to use-after-free,
more general program specifications. A second line targets             double-free, and other resource types (e.g., file descriptors,
the high false discovery rates of classical tools through              locks), as well as to other languages. Third, building on the
contextual warning triage, as exemplified by post-refinement           validated leak paths, we plan to explore LLM-based program
systems like BUGLENS [68] and ZeroFalse [69]. More                     repair [72]–[75] for candidate fixes. Finally, we will study
recently, the frontier has shifted toward autonomous agen-             the impact of LLM choice, including smaller open-weight
tic auditing, where agents such as RepoAudit [70] and                  models, on cost and reproducibility.
QRS [71] mimic human code auditors by navigating repos-
itories on-demand to track data-flow facts across feasible             7. Conclusion
paths. Most closely related, IMMI [20] detects kernel mem-
ory bugs by using an LLM to infer inconsistent caller/callee               This paper presents M EM H INT, a neuro-symbolic
MM intentions on error-handling paths within a bespoke                 pipeline for detecting memory leaks in C/C++ programs.
LLVM-IR engine. M EM H INT differs in three respects: (i) it           M EM H INT uses an LLM to infer the memory-management
produces analyzer-agnostic allocator/deallocator summaries             roles of custom functions, producing function summaries
that are Z3-validated for reachability and injected into               that extend the analyzer’s built-in knowledge beyond stan-
off-the-shelf analyzers (CodeQL and Infer) for user-space              dard primitives. Each summary is validated by Z3 to ensure
C/C++; (ii) it adds a dedicated Z3 path-feasibility filter on          the claimed allocation or deallocation is reachable on a
the analyzer’s output, which IMMI does not perform; and                feasible path. The validated summaries are injected into
(iii) it frames memory leak detection as a multi-stage neuro-          CodeQL and Infer, and Z3-based path feasibility filtering
symbolic pipeline in which symbolic validation gates every             combined with LLM-based validation suppresses false pos-
LLM-generated artifact before it influences the analysis.              itives. Evaluated on eight widely used open-source projects
                                                                       totaling over 3.6M lines of code, M EM H INT discovers 54
6. Limitations and Future Work                                         unique memory leaks (all confirmed or fixed), substantially
                                                                       outperforming vanilla CodeQL (19), vanilla Infer (3), Sem-
Abstraction of the Symbolic Layer. M EM H INT’s Z3 en-                 grep (2), and LeakGuard (20).
coding is deliberately lightweight: it models control-flow
reachability and the propagation of three memory-state pred-           Ethical Considerations
icates (alloc, freed, escaped), rather than the full heap
semantics of weakest-precondition or symbolic-execution                    This work discovers previously unknown memory-leak
engines. Branch conditions are treated as uninterpreted                defects in widely deployed open-source software. We fol-
Boolean variables in Equations 1–2, so the solver discards a           lowed responsible disclosure practices and reported con-
warning only when no control-flow path structurally reaches            firmed bugs to upstream maintainers through each project’s
the leak while leaving the object allocated, unfreed, and              disclosure channel; all 54 reported bugs have been confirmed
unescaped; it does not refute paths that are infeasible solely         or fixed. The study analyzes only publicly available source
under the numeric or pointer semantics of their guards.                code and does not involve private code, personal data, or


                                                                  11
human subjects. As an ethical safeguard, we use human                               [8]   C. Wen, H. Wang, Y. Li, S. Qin, Y. Liu, Z. Xu, H. Chen, X. Xie,
validation rather than relying solely on automated outputs.                               G. Pu, and T. Liu, “Memlock: memory usage guided fuzzing,”
                                                                                          in Proceedings of the ACM/IEEE 42nd International Conference
Our summary-quality evaluation is based on 1,532 C/C++                                    on Software Engineering, ser. ICSE ’20. New York, NY, USA:
functions independently labeled by two authors with high                                  Association for Computing Machinery, 2020, p. 765–777. [Online].
agreement (Cohen’s κ = 0.94), and all final bug reports                                   Available: https://doi.org/10.1145/3377811.3380396
were manually inspected before upstream submission.                                 [9]   J. Ba, G. J. Duck, and A. Roychoudhury, “Efficient greybox fuzzing
                                                                                          to detect memory errors,” in Proceedings of the 37th IEEE/ACM
Data Availability                                                                         International Conference on Automated Software Engineering, ser.
                                                                                          ASE ’22. New York, NY, USA: Association for Computing
                                                                                          Machinery, 2023. [Online]. Available: https://doi.org/10.1145/3551
    A replication package, including the implementation                                   349.3561161
of M EM H INT and detailed instructions for running it, is                          [10] W. Han, B. Joe, B. Lee, C. Song, and I. Shin, “Enhancing mem-
available at: https://github.com/jiekeshi/MemHint.                                       ory error detection for large-scale applications and fuzz testing,” in
                                                                                         Network and Distributed Systems Security (NDSS) Symposium 2018,
                                                                                         2018.
LLM Usage Statement
                                                                                    [11] G. Kim, D. Ryu, S. Bae, C. Lee, and T. Kim, “ Fuzzing Acceleration
                                                                                         for Memory Safety Bug Discovery with Slicer ,” in 2025 IEEE
    LLMs are used as components of M EM H INT. In Stage 1,                               Annual Computer Security Applications Conference (ACSAC). Los
M EM H INTuses an LLM to generate memory-management                                      Alamitos, CA, USA: IEEE Computer Society, Dec. 2025, pp. 46–59.
function summaries by classifying candidate functions as al-                             [Online]. Available: https://doi-ieeecomputersociety-org.libproxy.sm
locators, deallocators, or neither. In Stage 3, M EM H INTuses                           u.edu.sg/10.1109/ACSAC67867.2025.00020
an LLM to validate warnings that remain after Z3-based                              [12] W. Xu, S. Kashyap, C. Min, and T. Kim, “Designing new operating
path-feasibility filtering. We do not directly accept LLM out-                           primitives to improve fuzzing performance,” in Proceedings of the
                                                                                         2017 ACM SIGSAC Conference on Computer and Communications
puts. Generated summaries are validated by Z3 before being                               Security, ser. CCS ’17. New York, NY, USA: Association for
injected into static analyzers, and LLM-validated warnings                               Computing Machinery, 2017, p. 2313–2328. [Online]. Available:
are manually inspected before being submitted upstream. A                                https://doi.org/10.1145/3133956.3134046
limitation is that results may depend on the specific LLM                           [13] K. Serebryany, D. Bruening, A. Potapenko, and D. Vyukov, “Address-
versions and prompts used, which may affect reproducibility                              sanitizer: a fast address sanity checker,” in Proceedings of the 2012
when the underlying models are not openly available. LLMs                                USENIX Conference on Annual Technical Conference, ser. USENIX
                                                                                         ATC’12. USA: USENIX Association, 2012, p. 28.
were used for editorial purposes in this manuscript, and all
outputs were inspected by the authors to ensure accuracy                            [14] GitHub, “Codeql,” https://codeql.github.com/, 2026, [Accessed 23-
                                                                                         03-2026].
and originality.
                                                                                    [15] Facebook, “Infer Static Analyzer,” https://fbinfer.com, 2026, [Ac-
                                                                                         cessed 23-03-2026].
References                                                                          [16] D. Distefano, M. Fähndrich, F. Logozzo, and P. W. O’Hearn, “Scaling
                                                                                         static analyses at facebook,” Commun. ACM, vol. 62, no. 8, p. 62–70,
[1]   D. Zhang, O. R. Gatla, W. Xu, and M. Zheng, “A study of persistent                 Jul. 2019. [Online]. Available: https://doi.org/10.1145/3338112
      memory bugs in the linux kernel,” in Proceedings of the 14th ACM              [17] GitHub, “GitHub Actions workflow security analysis with CodeQL
      International Conference on Systems and Storage, ser. SYSTOR ’21.                  is now generally available,” https://github.blog/changelog/2025-04-2
      New York, NY, USA: Association for Computing Machinery, 2021.                      2-github-actions-workflow-security-analysis-with-codeql-is-now-g
      [Online]. Available: https://doi.org/10.1145/3456727.3463783                       enerally-available/, 2026, [Accessed 23-03-2026].
[2]   N. Emamdoost, Q. Wu, K. Lu, and S. McCamant, “Detecting kernel                [18] Y. Lyu, Y. Fang, Y. Zhang, Q. Sun, S. Ma, E. Bertino, K. Lu, and
      memory leaks in specialized modules with ownership reasoning,” in                  J. Li, “Goshawk: Hunting memory corruptions via structure-aware
      The 2021 Annual Network and Distributed System Security Sympo-                     and object-centric memory operation synopsis,” in 43rd IEEE
      sium (NDSS’21), 2021.                                                              Symposium on Security and Privacy, SP 2022, San Francisco, CA,
[3]   MITRE, “CWE-401: Missing Release of Memory after Effective                         USA, May 22-26, 2022. IEEE, 2022, pp. 2096–2113. [Online].
      Lifetime (4.19.1),” https://cwe.mitre.org/data/definitions/401.html,               Available: https://doi.org/10.1109/SP46214.2022.9833613
      2026, [Accessed 23-03-2026].                                                  [19] E. Shemetova, I. Smirnov, A. Alekseev, I. Shenbin, A. Rukhovich,
[4]   G. Fan, R. Wu, Q. Shi, X. Xiao, J. Zhou, and C. Zhang, “Smoke:                     S. Nikolenko, V. Lomshakov, and I. Piontkovskaya, “Lamed: Llm-
      Scalable path-sensitive memory leak detection for millions of lines of             generated annotations for memory leak detection,” in Proceedings
      code,” in 2019 IEEE/ACM 41st International Conference on Software                  of the 29th International Conference on Evaluation and Assessment
      Engineering (ICSE), 2019, pp. 72–82.                                               in Software Engineering, ser. EASE ’25. New York, NY, USA:
                                                                                         Association for Computing Machinery, 2025, p. 1024–1034. [Online].
[5]   D. Murphy, “This hidden Windows 11 setting might be quietly                        Available: https://doi.org/10.1145/3756681.3756999
      draining your RAM,” https://tech.yahoo.com/computing/articles/
      hidden-windows-11-setting-might-121538216.html, 2025, [Accessed               [20] D. Liu, Z. Lu, S. Ji, K. Lu, J. Chen, Z. Liu, D. Liu,
      23-03-2026].                                                                       R. Cai, and Q. He, “Detecting kernel memory bugs through
                                                                                         inconsistent memory management intention inferences,” in 33rd
[6]   C. Research, “Bleeding Llama: Critical Unauthenticated Memory                      USENIX Security Symposium (USENIX Security 24). Philadelphia,
      Leak in Ollama,” https://www.cyera.com/research/bleeding-llama                     PA: USENIX Association, Aug. 2024, pp. 4069–4086. [Online].
      -critical-unauthenticated-memory-leak-in-ollama, 2026, [Accessed                   Available: https://www.usenix.org/conference/usenixsecurity24/prese
      27-05-2026].                                                                       ntation/liu-dinghao-detecting
[7]   OpenCVE, “CVEs and Security Vulnerabilities,” https://app.opencv              [21] OpenSSL, “openssl/openssl: TLS/SSL and crypto library,” https://gi
      e.io/cve/?weakness=CWE-401, 2026, [Accessed 23-03-2026].                           thub.com/openssl/openssl, 2026, [Accessed 23-03-2026].



                                                                               12
[22] J. Wang, S. Ma, Y. Zhang, J. Li, Z. Ma, L. Mai, T. Chen,                      [37] G. O. de Sena and R. Matias, “A systematic mapping review of
     and D. Gu, “NLP-EYE: Detecting memory corruptions via                              memory leak detection techniques,” in 2018 IEEE International Sym-
     Semantic-Aware memory operation function identification,” in 22nd                  posium on Software Reliability Engineering Workshops (ISSREW),
     International Symposium on Research in Attacks, Intrusions and                     2018, pp. 264–270.
     Defenses (RAID 2019). Chaoyang District, Beijing: USENIX                      [38] Clang, “LeakSanitizer: a run-time memory leak detector,” https://cl
     Association, Sep. 2019, pp. 309–321. [Online]. Available: https:                   ang.llvm.org/docs/LeakSanitizer.html, Accessed 2026.
     //www.usenix.org/conference/raid2019/presentation/wang-0
                                                                                   [39] K. Serebryany, “OSS-Fuzz - google’s continuous fuzzing service for
[23] X. Chen, A. Slowinska, and H. Bos, “Membrush: A practical tool to                  open source software.” Vancouver, BC: USENIX Association, Aug.
     detect custom memory allocators in c binaries,” in 2013 20th Working               2017.
     Conference on Reverse Engineering (WCRE), 2013, pp. 477–478.
                                                                                   [40] L. Project, “libFuzzer: a library for coverage-guided fuzz testing,”
[24] H. Liang, L. Yin, G. Wu, Y. Li, Q. Yi, and L. Wang, “Leakguard:                    https://llvm.org/docs/LibFuzzer.html, Accessed 2026.
     Detecting memory leaks accurately and scalably,” arXiv preprint
                                                                                   [41] F. Project, “FreeRDP: A remote desktop protocol implementation,”
     arXiv:2504.04422, 2025.
                                                                                        https://www.freerdp.com, Accessed 2026.
[25] H. Hu, Y. Wang, J. Rubin, and M. Pradel, “An empirical                        [42] LLVM Project, “Clang static analyzer,” https://clang-analyzer.llvm.o
     study of suppressed static analysis warnings,” Proc. ACM Softw.                    rg/, 2026, [Accessed 23-03-2026].
     Eng., vol. 2, no. FSE, Jun. 2025. [Online]. Available: https:
     //doi.org/10.1145/3715729                                                     [43] H. Liu, Y. Wang, L. Jiang, and S. Hu, “Pf-miner: A new paired
                                                                                        functions mining method for android kernel in error paths,” in 2014
[26] T. Muske and A. Serebrenik, “Survey of approaches for                              IEEE 38th Annual Computer Software and Applications Conference.
     postprocessing of static analysis alarms,” ACM Comput. Surv., vol. 55,             IEEE, 2014, pp. 33–42.
     no. 3, Feb. 2022. [Online]. Available: https://doi.org/10.1145/3494521
                                                                                   [44] H.-Q. Liu, J.-J. Bai, Y.-P. Wang, Z. Bian, and S.-M. Hu, “Pairminer:
[27] H. J. Kang, K. L. Aw, and D. Lo, “Detecting false alarms                           mining for paired functions in kernel extensions,” in 2015 IEEE
     from automatic static analysis tools: how far are we?” in                          International Symposium on Performance Analysis of Systems and
     Proceedings of the 44th International Conference on Software                       Software (ISPASS). IEEE, 2015, pp. 93–101.
     Engineering, ser. ICSE ’22. New York, NY, USA: Association
                                                                                   [45] Z. Guo, T. Tan, S. Liu, X. Liu, W. Lai, Y. Yang, Y. Li, L. Chen,
     for Computing Machinery, 2022, p. 698–709. [Online]. Available:
                                                                                        W. Dong, and Y. Zhou, “Mitigating false positive static analysis warn-
     https://doi.org/10.1145/3510003.3510214
                                                                                        ings: Progress, challenges, and opportunities,” IEEE Transactions on
[28] X. Hou, Y. Zhao, Y. Liu, Z. Yang, K. Wang, L. Li, X. Luo, D. Lo,                   Software Engineering, vol. 49, no. 12, pp. 5154–5188, 2023.
     J. Grundy, and H. Wang, “Large language models for software                   [46] K. Li, S. Chen, L. Fan, R. Feng, H. Liu, C. Liu, Y. Liu, and Y. Chen,
     engineering: A systematic literature review,” ACM Trans. Softw.                    “Comparison and evaluation on static application security testing
     Eng. Methodol., vol. 33, no. 8, Dec. 2024. [Online]. Available:                    (sast) tools for java,” in Proceedings of the 31st ACM Joint European
     https://doi.org/10.1145/3695988                                                    Software Engineering Conference and Symposium on the Foundations
[29] J. Jiang, F. Wang, J. Shen, S. Kim, and S. Kim, “A survey on                       of Software Engineering, 2023, pp. 921–933.
     large language models for code generation,” ACM Trans. Softw.                 [47] T. Muske and A. Serebrenik, “Survey of approaches for handling
     Eng. Methodol., vol. 35, no. 2, Jan. 2026. [Online]. Available:                    static analysis alarms,” in 2016 IEEE 16th International Working
     https://doi.org/10.1145/3747588                                                    Conference on Source Code Analysis and Manipulation (SCAM).
[30] J. Shi, Z. Yang, and D. Lo, “Efficient and green large language                    IEEE, 2016, pp. 157–166.
     models for software engineering: Literature review, vision, and the           [48] M. Brunsfeld and T. sitter contributors, “Tree-sitter: An incremental
     road ahead,” ACM Trans. Softw. Eng. Methodol., vol. 34, no. 5, May                 parsing system for programming tools,” https://tree-sitter.github.io/tr
     2025. [Online]. Available: https://doi.org/10.1145/3708525                         ee-sitter/, accessed: 2026.
[31] Z. Sheng, Z. Chen, S. Gu, H. Huang, G. Gu, and J. Huang, “Llms in             [49] Z. Li, S. Dutta, and M. Naik, “Iris: Llm-assisted static analysis for
     software security: A survey of vulnerability detection techniques and              detecting security vulnerabilities,” arXiv preprint arXiv:2405.17238,
     insights,” ACM Comput. Surv., vol. 58, no. 5, Nov. 2025. [Online].                 2024.
     Available: https://doi.org/10.1145/3769082                                    [50] W. G. Cochran, Sampling Techniques, 3rd Edition. John Wiley, 1977.
[32] H. Xu, S. Wang, N. Li, K. Wang, Y. Zhao, K. Chen, T. Yu, Y. Liu, and          [51] A. J. Viera, J. M. Garrett et al., “Understanding interobserver agree-
     H. Wang, “Large language models for cyber security: A systematic                   ment: the kappa statistic,” Fam med, vol. 37, no. 5, pp. 360–363,
     literature review,” ACM Trans. Softw. Eng. Methodol., Sep. 2025,                   2005.
     just Accepted. [Online]. Available: https://doi.org/10.1145/3769676
                                                                                   [52] X. Du, J. Feng, Y. Zou, W. Xu, J. Ma, W. Zhang, S. Liu, X. Peng, and
[33] Z. Zhang, C. Wang, Y. Wang, E. Shi, Y. Ma, W. Zhong, J. Chen,                      Y. Lou, “Reducing false positives in static bug detection with llms:
     M. Mao, and Z. Zheng, “Llm hallucinations in practical code                        An empirical study in industry,” arXiv preprint arXiv:2601.18844,
     generation: Phenomena, mechanism, and mitigation,” Proc. ACM                       2026.
     Softw. Eng., vol. 2, no. ISSTA, Jun. 2025. [Online]. Available:
                                                                                   [53] Y. Jung and K. Yi, “Practical memory leak detector based on parame-
     https://doi.org/10.1145/3728894
                                                                                        terized procedural summaries,” in Proceedings of the 7th international
[34] N. Jain, R. Kwiatkowski, B. Ray, M. K. Ramanathan, and V. Kumar,                   symposium on Memory management, 2008, pp. 131–140.
     “On mitigating code llm hallucinations with api documentation,” in            [54] Y. Xie and A. Aiken, “Context-and path-sensitive memory leak
     2025 IEEE/ACM 47th International Conference on Software Engi-                      detection,” in Proceedings of the 10th European software engineering
     neering: Software Engineering in Practice (ICSE-SEIP), 2025, pp.                   conference held jointly with 13th ACM SIGSOFT international sym-
     237–248.                                                                           posium on Foundations of software engineering, 2005, pp. 115–125.
[35] L. De Moura and N. Bjørner, “Z3: an efficient smt solver,” in                 [55] C. Cadar, D. Dunbar, D. R. Engler et al., “Klee: unassisted and
     Proceedings of the Theory and Practice of Software, 14th Interna-                  automatic generation of high-coverage tests for complex systems
     tional Conference on Tools and Algorithms for the Construction and                 programs.” in OSDI, vol. 8, 2008, pp. 209–224.
     Analysis of Systems, ser. TACAS’08/ETAPS’08. Berlin, Heidelberg:
     Springer-Verlag, 2008, p. 337–340.                                            [56] Y. Sui, D. Ye, and J. Xue, “Detecting memory leaks statically
                                                                                        with full-sparse value-flow analysis,” IEEE Trans. Software Eng.,
[36] Semgrep Inc., “Semgrep,” Accessed 2026. [Online]. Available:                       vol. 40, no. 2, pp. 107–122, 2014. [Online]. Available: https:
     https://semgrep.dev                                                                //doi.org/10.1109/TSE.2014.2302311



                                                                              13
[57] S. Cherem, L. Princehouse, and R. Rugina, “Practical memory leak               [74] Y. Zhang, H. Ruan, Z. Fan, and A. Roychoudhury, “Autocoderover:
     detection using guarded value-flow analysis,” in Proceedings of the                 Autonomous program improvement,” in Proceedings of the 33rd ACM
     28th ACM SIGPLAN Conference on Programming Language Design                          SIGSOFT International Symposium on Software Testing and Analysis,
     and Implementation, 2007, pp. 480–491.                                              2024, pp. 1592–1604.
[58] Q. Shi, X. Xiao, R. Wu, J. Zhou, G. Fan, and C. Zhang, “Pinpoint:              [75] A. Murali, M. Alfadel, M. Nagappan, M. Xu, and C. Sun, “Address-
     Fast and precise sparse value flow analysis for million lines of                    watcher: Sanitizer-based localization of memory leak fixes,” IEEE
     code,” in Proceedings of the 39th ACM SIGPLAN Conference on                         Transactions on Software Engineering, vol. 50, no. 9, pp. 2398–2411,
     Programming Language Design and Implementation, 2018, pp. 693–                      2024.
     706.
[59] Q. Gao, Y. Xiong, Y. Mi, L. Zhang, W. Yang, Z. Zhou, B. Xie,                   Appendix A.
     and H. Mei, “Safe memory-leak fixing for c programs,” in 2015
     IEEE/ACM 37th IEEE International Conference on Software Engi-                  Prompt Templates
     neering, vol. 1. IEEE, 2015, pp. 459–470.
[60] W. Li, H. Cai, Y. Sui, and D. Manz, “Pca: memory leak detection                    This appendix lists the Phase 2 LLM summary gen-
     using partial call-path analysis,” in Proceedings of the 28th ACM              eration prompt and the Phase 6 LLM warning valida-
     Joint Meeting on European Software Engineering Conference and
     Symposium on the Foundations of Software Engineering, 2020, pp.
                                                                                    tion prompt. Further details on the implementation of
     1621–1625.                                                                     M EM H INT, together with instructions for running it, are
[61] S. Saha, J.-P. Lozi, G. Thomas, J. L. Lawall, and G. Muller, “Hector:
                                                                                    available at: https://github.com/jiekeshi/MemHint.
     Detecting resource-release omission faults in error-handling code for
     systems software,” in 2013 43rd Annual IEEE/IFIP International                 A.1. Phase 2: LLM Summary Generation Prompt
     Conference on Dependable Systems and Networks (DSN). IEEE,
     2013, pp. 1–12.
[62] D. L. Heine and M. S. Lam, “A practical flow-sensitive and context-            You are a memory safety expert analyzing C/C++
     sensitive c and c++ memory leak detector,” in Proceedings of the                   code to identify function semantics that help
     ACM SIGPLAN 2003 conference on Programming language design                         static analyzers detect memory leaks.
     and implementation, 2003, pp. 168–181.
                                                                                    ## Task
[63] R. Hastings, “Purify: Fast detection of memory leaks and access                Analyze this function and determine whether it is
     errors,” in Proceedings of the USENIX Winter’92 Conference, 1992,                  a memory allocator, deallocator, or neither.
     pp. 125–136.
[64] N. Nethercote and J. Seward, “Valgrind: a framework for heavyweight            **Function:** `{func_name}`
     dynamic binary instrumentation,” ACM Sigplan notices, vol. 42, no. 6,          **Return type:** `{return_type}`
     pp. 89–100, 2007.                                                              **Parameters:** `{parameters}`
[65] C. Jung, S. Lee, E. Raman, and S. Pande, “Automated memory leak
                                                                                    ```c
     detection for production use,” in Proceedings of the 36th International
                                                                                    {code}
     Conference on Software Engineering, 2014, pp. 825–836.
                                                                                    ```
[66] L. Ma, S. Liu, Y. Li, X. Xie, and L. Bu, “Specgen: Automated                   {context}
     generation of formal program specifications via large language mod-
     els,” in 2025 IEEE/ACM 47th International Conference on Software               ## Semantic Categories
     Engineering (ICSE). IEEE, 2025, pp. 16–28.
[67] C. Wen, J. Cao, J. Su, Z. Xu, S. Qin, M. He, H. Li, S.-C. Cheung,              ### Allocator
     and C. Tian, “Enchanting program specification synthesis by large              Function returns **newly allocated heap memory**
     language models using static analysis and program verification,” in                that caller must eventually free.
     International Conference on Computer Aided Verification. Springer,
     2024, pp. 302–328.                                                             **Positive indicators:**
                                                                                    - Calls malloc/calloc/realloc/aligned_alloc/new/
[68] H. Li, H. Zhang, K. Pei, and Z. Qian, “Towards more accurate                       new[] and returns the result
     static analysis for taint-style bug detection in linux kernel,” in 2025        - Calls another known allocator (e.g., g_malloc,
     40th IEEE/ACM International Conference on Automated Software                       xmalloc, kmalloc) and returns result
     Engineering (ASE). IEEE, 2025, pp. 380–392.                                    - Returns result of a wrapper function that
[69] M. Iranmanesh, S. M. Sabet, S. Marefat, A. J. Ghasr, A. Wilson,                    allocates
     I. Sharafaldin, and M. A. Tayebi, “Zerofalse: Improving precision in
     static analysis with llms,” arXiv preprint arXiv:2510.02534, 2025.             **Negative indicators (NOT an allocator):**
                                                                                    - Returns pointer to static/global buffer
[70] J. Guo, C. Wang, X. Xu, Z. Su, and X. Zhang, “Repoaudit: An                    - Returns pointer to struct field or array member
     autonomous llm-agent for repository-level code auditing,” arXiv                - Returns one of the input arguments
     preprint arXiv:2501.18160, 2025.                                               - Allocates internally but doesn't return the
[71] G. Tsigkourakos and C. Patsakis, “Qrs: A rule-synthesizing neuro-                  allocated memory
     symbolic triad for autonomous vulnerability discovery,” arXiv                  - Returns stack-allocated memory (dangling pointer
     preprint arXiv:2602.09774, 2026.                                                    bug, but not allocator semantic)
[72] C. Le Goues, M. Pradel, and A. Roychoudhury, “Automated program                ### Deallocator
     repair,” Communications of the ACM, vol. 62, no. 12, pp. 56–65,                Function **frees/releases memory** passed as an
     2019.                                                                              argument.
[73] Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan,
     “Automated repair of programs from large language models,” in 2023             **Positive indicators:**
     IEEE/ACM 45th International Conference on Software Engineering                 - Calls free/delete/delete[]/g_free/kfree on an
     (ICSE). IEEE, 2023, pp. 1469–1481.                                                 argument



                                                                               14
- Calls another deallocator on an argument                 Role: You are a senior static-analysis engineer
- Wrapper around resource cleanup                              specializing in C/C++ memory-safety.
                                                           You review memory-leak bug reports and assess
## Analysis Guidelines                                         whether the reported findings correspond to
                                                               actual memory-leak defects in the program.
1. **Trace data flow:** Follow where return values
     come from and where arguments flow to.                Does this function actually have a {bug_type_desc
2. **Consider all paths:** Check all branches and              }? Determine whether the reported issue is a
    return statements.                                         genuine bug (true) or a false alarm (false).
3. **Indirect calls matter:** If function calls
    helper that allocates/frees, propagate that            Decision policy:
    semantic.                                               - true: at least one reported issue plausibly
4. **Be precise:** Only report semantics you can                 corresponds to a real memory leak based on
    verify from the code.                                        the shown code.
                                                            - false: all reported issues are not real defects
## Output Format                                                  based on the shown code.

Return a JSON object with a `hints` array. Each            If only some issues are real, output true and list
    hint is a function summary with:                            only the real ones by index (1 = first, 2 =
- `name`: the function name                                    second, ...).
- `role`: "Allocator" or "Deallocator"
- `target`: "return" for allocators (return value          Respond with a single JSON object, no other text.
    carries heap ownership), or "argN" for                     Keep reason SHORT:
    deallocators (the N-th argument is freed, 0-            {"verdict": true | false, "confidence": 0.0-1.0,
    indexed)                                                     "reason": "one short sentence", "bug_indices
                                                                 ": [1] or [2,3] or []}
```json
{                                                          Output rules:
    "hints": [                                              - bug_indices: 1-based indices of reported issues
       {"name": "{func_name}", "role": "Allocator",               you consider real; [] when verdict=false.
            "target": "return"},                            - reason: ONE short sentence only. Do not quote
       {"name": "{func_name}", "role": "Deallocator              code.
           ", "target": "arg0"}
    ]
}
```                                                        Appendix B.
If no memory semantics apply, return: `{"hints":
                                                           Example Summary and Analyzer Injection
    []}`
                                                                We illustrate the output of Stage 1 and the format
Now analyze the function above and return the JSON         in which it is injected into the two analyzers, using the
     result.                                               FreeRDP running example from Section II. After LLM clas-
                                                           sification and Z3 validation, the pipeline emits the following
                                                           entries in its consolidated hints.json:
A.2. Phase 6: LLM Warning Validation Prompt
                                                           {
                                                               "hints": {
You are a memory-safety expert. Analyze the                      "freerdp_certificate_clone": [
    following C function and the reported bug(s).                  {
                                                                     "name": "freerdp_certificate_clone",
                                                                     "role": "Allocator",
**Project:** {project_name}
                                                                     "target": "return"
**File:** {file}
                                                                   }
**Function:** {function}
                                                                 ],
**Reported category:** {category}
                                                                 "freerdp_certificate_new": [
                                                                   {
**Reported issues (numbered 1, 2, ... for
     reference):**                                                   "name": "freerdp_certificate_new",
  {idx}. Line {line_num}: {msg}                                      "role": "Allocator",
    allocation_site: {allocation_site}                               "target": "return"
    trace step {i}: {location}                                     }
    code at that step:                                           ],
      {code}                                                     "freerdp_certificate_free": [
    code at line {line_num}:                                       {
      {code_at_line}                                                 "name": "freerdp_certificate_free",
                                                                     "role": "Deallocator",
                                                                     "target": "arg0"
**Function source:**
```c                                                               }
{source with "// <-- reported bug" markers on bug                ]
     lines}                                                    }
```                                                        }




                                                      15
CodeQL      injection  (data-extension   YAML).                      where the second equation applies the finite-population cor-
Each validated summary is appended to a data-                        rection. Substituting Z = 1.96 (95% confidence), p = 0.5
extension pack that registers the function with                      (worst-case proportion), e = 0.05 (5% margin of error),
CodeQL’s built-in allocationFunctionModel or                         and N = 88,474 (the candidate pool after pointer-type pre-
deallocationFunctionModel:                                           filtering across the eight subject projects) gives an initial
                                                                     sample size of n = 384.16 and a corrected sample size of
extensions:
  - addsTo:                                                          nadj = 382.50, which rounds to 383 samples per comparison
      pack: codeql/cpp-all                                           side.
      extensible: allocationFunctionModel
    data:
      - ["", "", false, "freerdp_certificate_clone",
           "", "", "", true]
      - ["", "", false, "freerdp_certificate_new",
          "", "", "", true]
  - addsTo:
      pack: codeql/cpp-all
      extensible: deallocationFunctionModel
    data:
      - ["", "", false, "freerdp_certificate_free",
          "0"]

Each row is a positional tuple for CodeQL’s extensible
predicates  allocationFunctionModel(namespace,
type, subtypes, name, sizeArg, sizeMult,
reallocArg, requiresDealloc)                      and
deallocationFunctionModel(namespace, type,
subtypes, name, freedArg). For these FreeRDP
global functions, namespace and type are empty, and
subtypes is false. The size and realloc slots are left
empty because our summaries encode ownership transfer
but not allocation-size semantics. The trailing true
marks the returned allocation as requiring a matching
deallocation; the deallocator’s trailing "0" indicates that
the first argument is freed, corresponding to arg0 in the
summary.
Infer injection (Pulse CLI flags). For Infer, validated
summaries are passed to the Pulse engine via two regex
patterns at invocation time:
infer run --pulse \
  --pulse-model-alloc-pattern \
    '^(freerdp_certificate_clone|
        freerdp_certificate_new|...)$' \
  --pulse-model-free-pattern \
    '^(freerdp_certificate_free|...)$' \
  -- <build command>

Pulse then treats calls matching the allocation pattern as
returning caller-owned allocated objects, and calls matching
the free pattern as releasing ownership of their argument. In
this way, Infer can track memory ownership through project-
specific wrappers using the validated summaries.

Appendix C.
Sample-Size Derivation
    For a finite population of size N , the required sample
size at confidence level Z , worst-case proportion p, and
margin of error e is
           Z 2 p(1 − p)                      n
      n=                ,     nadj =                 ,
                e2                     1 + (n − 1)/N


                                                                16
