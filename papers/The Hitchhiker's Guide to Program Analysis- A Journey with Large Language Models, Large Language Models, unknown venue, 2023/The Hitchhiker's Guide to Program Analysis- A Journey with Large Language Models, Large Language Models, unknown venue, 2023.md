                                             The Hitchhiker’s Guide to Program Analysis: A Journey with
                                                               Large Language Models
                                                                        Haonan Li                                                                   Yu Hao
                                                                    hli333@ucr.edu                                                           yhao016@ucr.edu
                                                                     UC Riverside                                                              UC Riverside
                                                               Riverside, California, USA                                                Riverside, California, USA

                                                                      Yizhuo Zhai                                                               Zhiyun Qian
                                                                  yzhai003@ucr.edu                                                          zhiyunq@cs.ucr.edu
                                                                     UC Riverside                                                              UC Riverside
arXiv:2308.00245v3 [cs.SE] 15 Nov 2023




                                                               Riverside, California, USA                                                Riverside, California, USA
                                         ABSTRACT                                                                       and (2) a precise symbolic execution with limited scalability. The
                                         Static analysis is a widely used technique in software engineering             solution illuminates the need for alternative strategies to navigate
                                         for identifying and mitigating bugs. However, a significant hurdle             the complex trade-offs between precision and scalability effectively.
                                         lies in achieving a delicate balance between precision and scalabil-           Despite this strategic combination of analysis techniques, nearly
                                         ity. Large Language Models (LLMs) offer a promising alternative,               40% of the potential bugs reported from the static analysis phase
                                         as recent advances demonstrate remarkable capabilities in com-                 experience a timeout or memory exhaustion during the static sym-
                                         prehending, generating, and even debugging code. Yet, the logic                bolic execution phase, preventing any conclusive results on such
                                         of bugs can be complex and require sophisticated reasoning and a               cases. This limitation hinders the overall effectiveness of the tool,
                                         large analysis scope spanning multiple functions. Therefore, at this           leading to the potential of two distinct outcomes: missed bugs if
                                         point, LLMs are better used in an assistive role to complement static          these potential bug reports are ignored (what UBITect performs),
                                         analysis. In this paper, we take a deep dive into the open space of            or false positives if they are sent to developers for inspection.
                                         LLM-assisted static analysis, using use-before-initialization (UBI)               In this paper, we investigate the possibility of leveraging Large
                                         bugs as a case study. To this end, we develop LLift, a fully auto-             Language Models (LLMs) as an alternative to handle such “difficult
                                         mated framework that interfaces with both a static analysis tool and           cases”. This is because recent LLMs have exhibited strong potential
                                         an LLM. By carefully designing the framework and the prompts, we               in understanding, generating, and even debugging code [4, 8, 13].
                                         are able to overcome a number of challenges, including bug-specific            Nevertheless, navigating the intricacies of utilizing LLMs for bug
                                         modeling, the large problem scope, the non-deterministic nature                discovery proves to be a complex feat. The technical report on
                                         of LLMs, etc. Tested in a real-world scenario analyzing nearly a               GPT-4 underscores this challenge, admitting that when it comes
                                         thousand potential UBI bugs produced by static analysis, LLift                 to discovering new vulnerabilities, it may not be the best solution
                                         demonstrates a potent capability, showcasing a reasonable preci-               standalone [21]: “... is less effective than existing tools for complex
                                         sion (50%) and appears to have no missing bug. It even identified 13           and high-level activities like novel vulnerability identification”. In
                                         previously unknown UBI bugs in the Linux kernel. This research                 the same vein, prior research demonstrates the competence of LLMs
                                         paves the way for new opportunities and methodologies in using                 mostly in simpler tasks or programs [1, 25, 26]. This is because LLMs
                                         LLMs for bug discovery in extensive, real-world datasets.                      are far from perfect. For instance, they suffer from hallucination [11]
                                                                                                                        where instead of identifying the bugs in faulty code, LLMs may
                                         1    INTRODUCTION                                                              create non-existent facts in an attempt to rationalize the original
                                                                                                                        intention behind the problematic code [17, 31]. Another issue is the
                                         Static analysis is a popular technique in software engineering, par-
                                                                                                                        stochasticity of LLMs which can result in inconsistent or outright
                                         ticularly in the area of bug discovery, that can improve code quality,
                                                                                                                        incorrect results, thus throwing another wrench into the gears of
                                         reliability, and security. However, the effectiveness of these tech-
                                                                                                                        bug discovery [41]. Finally, LLMs have limited context windows,
                                         niques is influenced by the fundamental trade-off between precision
                                                                                                                        meaning they can only scrutinize a relatively small codebase.
                                         and scalability, especially when dealing with extensive and com-
                                                                                                                           In response, we propose LLift, a fully automated framework
                                         plex programs [9, 24]. On the one hand, static analysis solutions
                                                                                                                        that bridges static analysis with LLMs in analyzing UBI bugs. Our
                                         with lower precision tend to generate numerous false positives. On
                                                                                                                        solution packages several novel components. First, LLift performs
                                         the other hand, expensive static analysis or symbolic execution
                                                                                                                        post-constraint guided path analysis, which helps verify the path
                                         solutions with higher precision often struggle to complete the anal-
                                                                                                                        feasibility of the “use” of an initialized variable, a difficult task for
                                         ysis. Consequently, achieving comprehensive and accurate static
                                                                                                                        static analysis and symbolic execution. Second, to efficiently in-
                                         program analysis for sizable programs like the Linux kernel poses
                                                                                                                        teract with LLMs, we employ task decomposition to break down
                                         a significant challenge.
                                                                                                                        the analysis into more than a single step. Third, we employ pro-
                                            UBITect [40], a powerful static analysis solution illustrates these
                                                                                                                        gressive prompting by providing information incrementally only
                                         inherent limitations thoroughly. Targeting Use-Before-Initialization
                                                                                                                        when necessary, instead of providing an enormous scope of code
                                         (UBI) bugs in the Linux kernel, it packages a pipeline of (1) a scalable
                                                                                                                        at once. Finally, we propose self-validation by requesting LLMs to
                                         bottom-up summary-based static analysis with limited precision,
                                                                                                                    1
                                                                                                                                               Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian
                                                                                                                                              Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian


                                                                                                           which are false alarms. The static analysis is imprecise partly due
1       static int libcfs_ip_str2addr(...){                                                              which are false alarms. The static analysis is imprecise partly due
2         unsigned int a, b, c, d;                                                                         to its lack of path sensitivity (often needed to discover UBI bugs).
                                                                                                         to its lack of path sensitivity (often needed to discover UBI bugs).
3         if (sscanf(str, %u.%u.%u.%u%n , &a, &b, &c, &d, &n) >= 4){
                                                                                                           It is complemented by a second stage of static symbolic execution
4             // use of a, b, c, d                                                                       It is complemented by a second stage of static symbolic execution
                                                                                                           that filters as many false alarms as possible by verifying their path
5         }                                                                                              that �lters as many false alarms as possible by verifying their path
6       }                                                                                                  feasibility. However, 40% of the reported bugs are discarded due
                                                                                                         feasibility. However, 40% of the reported bugs are discarded due
7       int sscanf(const char *buf, const char *fmt, ...){
8         va_list args;                                                                                  tototimeout
                                                                                                               timeout(10   (10minutes)
                                                                                                                                 minutes)orormemory memorylimitations
                                                                                                                                                                  limitations(2(2GB)   GB)during
                                                                                                                                                                                              during    the
                                                                                                                                                                                                      the
9         int i;                                                                                           symbolicexecution,
                                                                                                         symbolic        execution,potentially
                                                                                                                                        potentiallymissing missinggenuine
                                                                                                                                                                        genuinebugs.bugs.
10        va_start(args, fmt);                                                                                 Figure1 1shows
                                                                                                             Figure          showsa acase casewherewhereUBITect’s
                                                                                                                                                              UBITect’sstatic staticanalysis
                                                                                                                                                                                        analysisstage stage
11        i = vsscanf(buf, fmt, args);
12        va_end(args);                                                                                    considers      it a  potential   UBI     bug    (a  false   alarm)
                                                                                                         considers it a potential UBI bug (a false alarm) and the subsequent     and   the   subsequent
13      }                                                                                                  symbolicexecution
                                                                                                         symbolic        executionstagestagetimes
                                                                                                                                                timesout outandandfails
                                                                                                                                                                     failstoto  generate
                                                                                                                                                                             generate        a definitive
                                                                                                                                                                                           a de�nitive
                                                                                                           conclusion.InInother
                                                                                                         conclusion.            otherwords,
                                                                                                                                        words,UBITect
                                                                                                                                                    UBITectfailedfailedtotorule
                                                                                                                                                                              ruleout
                                                                                                                                                                                    outthisthiscase
                                                                                                                                                                                                 caseasasaa
                     Figure
                      Figure1:1:Code
                                 Codesnippet
                                      snippetofofsscanf
                                                  sscanfand
                                                         anditsits
                                                                 usecase
                                                                   usecase
                                                                                                         false alarm. As Table 1 presents, the static analysis stage generates a a
                                                                                                           false  alarm.     As  Table  1  presents,      the   static   analysis   stage    generates
      Table1:1:UBITect’s
     Table      UBITect’ssummary
                              summary     for
                                        for            Both
                                                     Both
                                               sscanf.
                                             sscanf.         useand
                                                           use   and  initialization
                                                                    initialization   for
                                                                                   for   va_args
                                                                                       va_args             summaryofofsscanf()
                                                                                                         summary              sscanf()asas“may   “maynot notinitialize       parameters
                                                                                                                                                               initializeparameters         a,a,
                                                                                                                                                                                               b,b,
                                                                                                                                                                                                  c, c,
                                                                                                                                                                                                     andand
      areincorrect.
     are   incorrect.3✓and and7 ✗stand
                                   standfor
                                          forwhether
                                               whether  this
                                                      this   parameter
                                                           parameter     will
                                                                       will bebe used/initialized
                                                                               used/initialized
      after  its call. “...” represents    all other parameters   of
     after its call. “...” represents all other parameters of va_args.va_args.
                                                                                                           d”  but  does   use  them   at Line     3. Consequently,         the
                                                                                                         d” but does use them at Line 3. Consequently, the static analysis stage static   analysis    stage
                                                                                                           reportstwo
                                                                                                         reports      twolocations
                                                                                                                             locationsofofuse-before-initialization
                                                                                                                                               use-before-initializationatatLine      Line3 and
                                                                                                                                                                                              3 andLineLine
                                           fmt ...... *buf
                                                                                                         4, respectively. There are two reasons for the static analysis stage toto
                                                                                                           4, respectively.      There   are   two     reasons     for  the  static  analysis     stage
                                      buf fmt
                                     buf               *buf *fmt
                                                             *fmt
                      Use
                     Use         3✓            3✓ 3✓          3✓         3✓                                considerthe
                                                                                                         consider       thecase
                                                                                                                              casea apotential
                                                                                                                                      potentialbug:   bug:1)1)inability
                                                                                                                                                                inabilitytotorecognize
                                                                                                                                                                                   recognize      special
                                                                                                                                                                                                special
                      Initialize 7✗
                     Initialize                7✗ 7✗          7✗         7✗                                functions:For
                                                                                                         functions:          Forsoundness,
                                                                                                                                   soundness,UBITect  UBITectassumedassumedthe   theva_start()
                                                                                                                                                                                       va_start()is is
                                                                                                         a anormal
                                                                                                              normalfunction.
                                                                                                                         function.However,
                                                                                                                                       However,since    sinceit itcannot
                                                                                                                                                                    cannot�nd  finditsitsde�nition,
                                                                                                                                                                                           definition,it it
                                                                                                         has to conservatively assume that the arguments passed totoit it
                                                                                                           has   to conservatively        assume        that   the   arguments       passed             will
                                                                                                                                                                                                     will
       review   responses     at various   stages to obtain     accurate                                   be   used   inside.    Unfortunately,          in   reality,   va_start        is a  compiler
     we  propose    self-validation   by requesting     LLMs to     reviewand      reliable
                                                                              responses                  be used inside. Unfortunately, in reality, va_start is a compiler
                                                                                                           built-infunction
                                                                                                                      functionthat thatsimply
                                                                                                                                         simply“prepares’
                                                                                                                                                      “prepares’the   thearguments
                                                                                                                                                                           argumentswithout without     any
     atresponses.
        various stages to obtain accurate and reliable responses.                                        built-in
                                                                                                           uses.   2)  insensitivity        of    path     constraints:         It fails   to
                                                                                                                                                                                                     any
                                                                                                                                                                                               recognize
          Weimplement
         We    implementa aprototype
                                 prototypeofofLL���LLiftand andtest
                                                                 testititininreal-world
                                                                               real-world                uses. 2) insensitivity of postconditions: It fails to recognize the
       scenarios.   Focusing     on  the  inconclusive      cases   of  UBITect     caused                 the path
                                                                                                         check    of itsconstraint,
                                                                                                                          return value, i.e.,i.e.,
                                                                                                                                               if(sscanf(...)>=4),
                                                                                                                                                   if(sscanf(...)>=4),             which
                                                                                                                                                                                     whichensures
                                                                                                                                                                                                ensuresits
     scenarios. Focusing on the inconclusive cases of UBITect caused
                                                                                                           arguments        a  to d  must   be    initialized
                                                                                                         its arguments a to d must be initialized before use.      before    use.
     bybytime
           timeorormemory
                    memorylimitation,
                                limitation,LL���
                                               LLiftsuccessfully
                                                      successfullyidenti�es
                                                                       identifies1313pre-
                                                                                        pre-
      viouslyunknown
     viously     unknownUBI   UBIbugs
                                    bugsininthe
                                              theLinux
                                                  Linuxkernel
                                                           kernelthat
                                                                    thatwe wecon�rmed
                                                                                confirmed
      withthe
     with    theLinux
                  Linuxcommunity.
                          community.With  With2626positive
                                                     positivereports
                                                                 reportsout outofofnearly
                                                                                     nearly
      1,000cases,
     1,000    cases,LL���
                       LLiftreaches
                               reachesa ahighhighprecision
                                                    precisionofof50%.50%.We Wealsoalsotest
                                                                                        test              2.2 Practical
                                                                                                         2.2   PracticalChallenges
                                                                                                                         ChallengesofofStatic
                                                                                                                                        StaticAnalysis
                                                                                                                                               Analysis
       LLiftagainst
               againstallallpreviously
                             previouslyknownknownbugs bugsfound
                                                             foundbybyUBITect,
                                                                           UBITect,and  and
     LL���                                                                                               InInlight
                                                                                                               lightofofour
                                                                                                                         ourmotivating
                                                                                                                              motivatingexample
                                                                                                                                            exampleofofthe
                                                                                                                                                         thesscanf()
                                                                                                                                                              sscanf()case,case,wewecan
                                                                                                                                                                                      can
       observea arecall
     observe       recallofof100%.
                               100%.                                                                       summarizethe   thereasons
                                                                                                                               reasonsfor
                                                                                                                                        forUBITect’s
                                                                                                                                            UBITect’sfailure
                                                                                                                                                        failureasasfollows:
                                                                                                                                                                     follows:
                                                                                                         summarize
          We   summarize      our   contributionsasasfollows:
         We summarize our contributions                  follows:                                          InherentKnowledge
                                                                                                                          KnowledgeBoundaries.                 Developersneed
                                                                                                                                            Boundaries.Developers              needtotomodel
                                                                                                                                                                                          model
          NewOpportunities.
                 Opportunities.We      Weintroduce
                                            introducea anovel
                                                            novelapproach
                                                                    approachtotostaticstatic             Inherent
     ••New                                                                                                 specific   functions    or  language    features.     Otherwise,    they  influence
          analysisthat
                     thatenhances
                           enhancesitsitsprecision
                                            precisionandandscalability
                                                              scalabilityatatthe thesame
                                                                                      same               speci�c functions or language features. Otherwise, they in�uence
        analysis                                                                                           thecorrectness
                                                                                                                 correctnessofofthetheresults.
                                                                                                                                         results.For
                                                                                                                                                   Forcompiler
                                                                                                                                                          compilerbuilt-in
                                                                                                                                                                     built-infunctions,
                                                                                                                                                                                functions,   e.g.,
          time  by  harnessing      the capabilities    of  LLMs.    To  the  best   of  our             the                                                                               e.g.,
        time by harnessing the capabilities of LLMs. To the best of our                                    va_start(),their  theirde�nitions
                                                                                                                                    definitionsarearesimply
                                                                                                                                                         simplynot
                                                                                                                                                                 notavailable.
                                                                                                                                                                      available.Beyond
                                                                                                                                                                                   Beyond    this
          knowledge,     we   are  the first  to use  LLMs    to  assist  static  analysis               va_start(),                                                                      this
        knowledge, we are the �rst to use LLMs to assist static analysis                                   example,therethereexists
                                                                                                                                existsananarray
                                                                                                                                             arrayofofother
                                                                                                                                                          otherscenarios,
                                                                                                                                                                 scenarios,which
                                                                                                                                                                               whicharearepar-
                                                                                                                                                                                             par-
                                                                                                         example,
        ininbug-�nding
             bug-findingtaskstaskswith
                                     withlarge-scale
                                           large-scaleand andreal-world
                                                               real-worlddatasets.
                                                                              datasets.                    ticularly    prevalent    in  the  Linux     kernel.   These   situations   include
                Methodologies. We                                                                        ticularly prevalent in the Linux kernel. These situations include
     ••NewNewMethodologies.            Wedevelop
                                             developLLift,
                                                       LL���,anan  innovative
                                                                      innovative  andand
                                                                                       fully               assemblycode, code,hardware
                                                                                                                                 hardwarebehaviors,
                                                                                                                                               behaviors,callback
                                                                                                                                                               callbackfunctions,
                                                                                                                                                                          functions,concur-
                                                                                                                                                                                       concur-
          automated     framework     that  arms   static analysis    with   LLMs.    LLift              assembly
        fully automated agent that arms static analysis with LLMs. LL���                                   rency,andandcompiler
                                                                                                                          compilerbuilt-in
                                                                                                                                      built-infunctions.
                                                                                                                                                functions.However,
                                                                                                                                                               However,ininpractical
                                                                                                                                                                               practicalterms,
                                                                                                                                                                                          terms,
          employsseveral
                     severalprompt
                               promptstrategies
                                        strategiestotoengage
                                                        engagewithwithLLMs,
                                                                          LLMs,eliciting
                                                                                   eliciting             rency,
        employs                                                                                            it is  often  time-consuming         to discover     and  model     all these  cases,
          accurateandandreliable
                           reliableresponses.
                                     responses.                                                          it is often time-consuming to discover and model all these cases,
        accurate                                                                                           becausethey theycancanbebehighly
                                                                                                                                       highlydependent
                                                                                                                                                dependentononthe    theanalysis
                                                                                                                                                                         analysistarget
                                                                                                                                                                                    targetandand
          Results.We  Werigorously
                           rigorouslyinvestigate
                                         investigateLL���
                                                        LLiftbybyconducting
                                                                     conductingananin-    in-            because
     ••Results.                                                                                            evolveoverovertime.
                                                                                                                           time.This
                                                                                                                                   Thislimitation
                                                                                                                                          limitationoftenoftencompromises
                                                                                                                                                                compromisesthe   thee�ective-
                                                                                                                                                                                      effective-
          depth   analysis    of  nearly   1000   cases,   resulting    in  a reasonable                 evolve
        depth analysis of nearly 1000 cases, resulting in a high precision                                 nessofofstatic
                                                                                                                      staticanalysis,
                                                                                                                              analysis,leaving
                                                                                                                                           leavingit itless
                                                                                                                                                         lessprecise
                                                                                                                                                               preciseand
                                                                                                                                                                        andcomprehensive
                                                                                                                                                                              comprehensive
          precision    raterecall
                             (50%).   Additionally,    our examination          led to the               ness
        rate  (50%) and            rate (100%). Additionally,        our examination                       than    desired.
          discovery    of 13 previously      unknownunknown
                                                          bugs. bugs.                                    than desired.
        led  to the discovery     of 13 previously
          Opensource.         Committedtotoopen
                  source.Committed               openresearch,
                                                         research,we  wewillwillpublicly
                                                                                  publicly                  ExhaustivePath
                                                                                                         Exhaustive          PathExploration.          Correctlyhandling
                                                                                                                                     Exploration.Correctly           handlingcases caseslike
                                                                                                                                                                                          like
     ••Open
                                                                                                                         requires     it to  consider    the   check:
                                                                                                         sscanf() requires it to consider the check: sscanf(...)>=4.
                                                                                                            sscanf()                                                     sscanf(...)>=4.
        release all of our code and data, fostering further exploration ofof
          release  all of  our  code  and   data,  fostering   further    exploration
          thenew
               newspace
                     spaceofofLLM-assisted
                                LLM-assistedprogram
                                                  programanalysis.
                                                              analysis.                                     Unfortunately,existing
                                                                                                         Unfortunately,       existingpath-sensitive
                                                                                                                                         path-sensitivestatic
                                                                                                                                                           staticanalysis
                                                                                                                                                                   analysis(and
                                                                                                                                                                             (andsymbolic
                                                                                                                                                                                    symbolic
        the
                                                                                                            execution)techniques
                                                                                                         execution)       techniquesoperate
                                                                                                                                         operateunder
                                                                                                                                                  undera amethodical
                                                                                                                                                              methodicalbut butexhaustive
                                                                                                                                                                                  exhaustive
                                                                                                            paradigm,exploring
                                                                                                         paradigm,        exploringallallpotential
                                                                                                                                            potentialexecution
                                                                                                                                                        executionpathspathsthrough
                                                                                                                                                                              throughthe   the
     22 BACKGROUND
         BACKGROUND&&MOTIVATION
                          MOTIVATION
                                                                                                            codebase.    While     this  approach    is  theoretically    comprehensive,
                                                                                                         codebase. While this approach is theoretically comprehensive,
      2.1 UBITect
     2.1   UBITectand
                   andMotivating
                      MotivatingExample
                                 Example                                                                 it itoften
                                                                                                               oftenleads
                                                                                                                       leadstotoa acombinatorial
                                                                                                                                     combinatorialexplosion.
                                                                                                                                                        explosion.The Thevastvastarray
                                                                                                                                                                                    arrayofof
       UBITectisisa astate-of-the-art
     UBITect           state-of-the-artstatic
                                         staticanalysis
                                                analysissolution
                                                          solutionaiming
                                                                       aimingatat�nd-
                                                                                  find-                     executionpaths
                                                                                                         execution       pathsnecessitates
                                                                                                                                necessitatesthe theexploration
                                                                                                                                                     explorationofofmyriad
                                                                                                                                                                        myriadfunctions,
                                                                                                                                                                                   functions,
       ingUse
     ing   UseBefore
                 BeforeInitialization     (UBI)bugs
                          Initialization(UBI)    bugsininthe
                                                           theLinux
                                                                  Linuxkernel
                                                                          kernel[41].
                                                                                  [40].                     manyofofwhich
                                                                                                         many          whichultimately
                                                                                                                               ultimatelyprove
                                                                                                                                             proveirrelevant
                                                                                                                                                    irrelevanttotothethespeci�c
                                                                                                                                                                          specificanalysis
                                                                                                                                                                                     analysis
     It employs a two-stage pipeline where the �rst stage employs a a
       It employs    a  two-stage   pipeline    where  the   first   stage employs                          task  at hand.   In  the              case,   its return  value
                                                                                                         task at hand. In the sscanf() case, its return value is computed
                                                                                                                                      sscanf()                                 is  computed
       bottom-upsummary-based
     bottom-up       summary-basedstatic staticanalysis
                                                analysisofofthe
                                                              theLinux
                                                                     Linuxkernel.
                                                                           kernel.ByBy                      insideananunbounded
                                                                                                         inside         unboundedloop  loopwhen
                                                                                                                                             wheniterating
                                                                                                                                                    iteratingover
                                                                                                                                                                overananunknown
                                                                                                                                                                          unknownstring string
       design,this
     design,    thisstage
                      stageaims
                             aimsfor
                                   forscalability
                                       scalabilityand
                                                    andsacri�ces
                                                         sacrificesprecision,
                                                                       precision,pro-
                                                                                   pro-                    variablebuf.
                                                                                                         variable           Thiscauses
                                                                                                                      buf.This     causesUBITect’s
                                                                                                                                           UBITect’ssymbolic
                                                                                                                                                        symbolicexecution
                                                                                                                                                                    executiontototimetime  out
                                                                                                                                                                                         out
       ducinga asigni�cant
     ducing       significantnumber
                               numberofofpotential
                                            potentialbugs
                                                       bugs(i.e.,
                                                               (i.e.,⇠140k),  mostofof
                                                                      ∼140k),most                           exactlydue
                                                                                                         exactly     duetotothis
                                                                                                                              thisproblem.
                                                                                                                                    problem.
                                                                                                    22
    The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models
     The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models

    UBITect
     UBITect
                                                  40%
                                                                                         result
                                                                                        result        Specifically, they detail the guarantees a routine
                                                                                                                                                    UBITect offers
                                                                                                                                                             reportsbased    on use-
                                                                                                                                                                      potential  its
                                 Symbolic         40% undecided
                                                      undecided
      Static
       StaticAnalysis
              Analysis            Symbolic
                                 Execution
                                                                       LL���
                                                                       LLift                          observable outcomes.                            before-initialization bugs
                                 Execution
                                                                                                         For a routine 𝑅, consider its set of outcomes
                                                                                                                                                  1     as O. These outcomes
                                                                                                                                                    Identify the initializer: sscanf
                                                                 60% successful
                                                                 60% successfulexecution
                                                                                execution             are defined as updates to its parameters (and return value) for a path
                                                                                                      of 𝑅. Particularly, O does not include initialization    for  variables for
                                                                                                                                                  2

    Figure                                                                                                                                           Extract the  post-constraint:
     Figure2:2:The
                Theoverview
                    overviewof
                             ofLL���.
                               LLift. Start
                                      Start with
                                            with the discarded cases
                                                 the discarded  casesby
                                                                     byUBITect
                                                                        UBITectand
                                                                                and
    determine
     determinewhether
                 whetherthese
                          thesepotential
                                potential bugs
                                          bugs are
                                               are true or false.
                                                   true or false.                                     convenience. In the study of UBI bug, for a routine      𝑅 that can yield
                                                                                                                                                           sscanf(...)>=4
                                                                                                      a set of outcomes O, the postcondition P    3 can be defined as:
1      int caller_function(){                                                                                                                               Summarize the initializer with
2          int X; // declare of suspicious variable -                                                                         P𝑅 : S(𝑅) → O × must_init                      (2)
                                                                                                                                                 context (e.g., post-constraints)
3          ...
4          init(&X); // initializer of -                                                              Here, S(𝑅) signifies all possible execution paths through the routine
5          ...                                                                                        𝑅,Figure  4: Example run of LL���. For each potential bug, we ¨ identify its
                                                                                                          O describes    all updates of 𝑅 on its variables, and must_init is a
6          use(X); // use of -                                                                         initializer, ≠ extract the post-constraints of the initializer, and Æ analyze the
7      }                                                                                              set  of variables   that mustwith
                                                                                                       behavior of the initializer   be initialized.
                                                                                                                                         the post-constraints via LLM.
                                                                                                      Motivating Example. Consider the sscanf() function in our mo-
    Figure
      Figure3:3:AAtypical
                    typicaltype
                              typeof
                                   ofpotential
                                      potential UBI
                                                 UBI bug. For each
                                                              each suspicious
                                                                   suspiciousvariable
                                                                                variable𝑋-, ,
    we
                                                     bug. For                                         tivating   example.
                                                                                                       it is passed    to a Based
                                                                                                                             calleeon  these return
                                                                                                                                    function   to bevalues,    the postconditions
                                                                                                                                                       initialized   (typically condi-
      weexpect
          expectitittoto1)1)have
                             havean
                                  aninitializer
                                     initializer function that probably
                                                 function that probably initializes
                                                                         initializes𝑋-and
                                                                                       and
    2)2)use
         use-𝑋. .
                                                                                                      assure   the  initialization of certain  variables:
                                                                                                       tionally) before its use. We assume there can be multiple layers of
                                                                                                       indirection where the initialization actually occurs. Note that there
     2.3 Capability
    2.3  Capability of
                    of LLMs
                       LLMs                                                                            are other     less common
                                                                                                                 P (𝑝𝑎𝑡ℎ  1 ) : {𝑟𝑒𝑡 ↦→cases,   i.e., the variable
                                                                                                                                           0, must_init        ↦→ ∅} is initialized directly
      Fortunately,LLMs   LLMs [21]
                                [21] o�ers
                                     offers aa promising
                                                 promising alternative                                 in the function
                                                                                                                 P (𝑝𝑎𝑡ℎ 2 )where
                                                                                                                              : {𝑟𝑒𝑡 ↦→the1,variable      is declared.
                                                                                                                                                                ↦→ {𝑎}} We choose not to
    Fortunately,                                               alternative to   to summa-
                                                                                    summa-                                                    must_init
                                                                                                       account for them, as most such cases are easier cases and more
    rizing code behaviors [22] in a �exible way and bypassing the
      rizing     code   behaviors   [22]   in  a  flexible   way   and    bypassing       the                    P (𝑝𝑎𝑡ℎ 3 ) : {𝑟𝑒𝑡 ↦→ 2, must_init ↦→ {𝑎, 𝑏}}
      aforementionedchallenges.
                             challenges. This
                                           This isis because
                                                      because LLMs                                     likely solved successfully by UBITect already.
    aforementioned                                              LLMs are are trained
                                                                              trainedand  and                    P (𝑝𝑎𝑡ℎ 4 ) : {𝑟𝑒𝑡 ↦→ 3, must_init ↦→ {𝑎, 𝑏, 𝑐}}
      alignedwith
    aligned        withextensive
                         extensive datasets
                                    datasets that
                                               that include
                                                      include both
                                                                both natural
                                                                       natural language
                                                                                  language             Conceptual Work�ow. Figure 4 demonstrates the work�ow of
                                                                                                                          5 ) : {𝑟𝑒𝑡       4, must_init
    and programs. Speci�cally, we observe that LLMs possess
      and    programs.      Specifically, we   observe     that  LLMs     possessfunda-
                                                                                                                 P (𝑝𝑎𝑡ℎtakes
                                                                                                       LL���. LL���              bug ↦→reports                ↦→ {𝑎,as
                                                                                                                                                   from UBITect        𝑏, 𝑐, 𝑑 }} which con-
                                                                                                                                                                          inputs,
                                                                                      funda-
      mental abilities that assist in addressing each challenge: 1) domain-                                         (𝑝𝑎𝑡ℎ 6 ) : {𝑟𝑒𝑡
                                                                                                       tain thePsuspicious            ↦→ 5, must_init
                                                                                                                                  variable    that may be↦→      used  before
                                                                                                                                                                   {𝑎, 𝑏,         initialization,
                                                                                                                                                                          𝑐, 𝑑, 𝑛}}
    mental      abilities that assist in addressing each challenge: 1) domain-
      specific code recognition and 2) smart code summarization.                                       and the function that it sits in. We follow the following three key
    speci�c code recognition and 2) smart code summarization.
      Domain-specific Programming Constructs Recognition. This                                         subtasks when interacting with LLMs:
    Domain-speci�c Programming Constructs Recognition. This                                           Here, the 𝑝𝑎𝑡ℎ 1 − 𝑝𝑎𝑡ℎ 6 represent different possible paths in the
      proficiency is showcased in three key areas: 1) Function Recogni-                                    ¨ Identify potential initializers of the suspicious variable. In our
    pro�ciency is showcased in three key areas: 1) Function Recogni-                                  sscanf() and each path corresponds with a different postcondition.
      tion: LLMs can identify frequently used interfaces in the Linux ker-                             motivating      example,not
                                                                                                          For UBI detection,        sscanf()        is the initializer.
                                                                                                                                       every associated       postcondition is relevant;
    tion: LLMs can identify frequently used interfaces in the Linux ker-
      nel from its semantics, such as sscanf(), kzalloc(), kstrtoul(),                                     ≠ Extract
                                                                                                      instead,   only thetheoutcomes
                                                                                                                              path constraints
                                                                                                                                           making from        the reachable
                                                                                                                                                       the 𝑢 (𝑣)   initializerare  return  to the
    nel from its semantics, such as sscanf(), kzalloc(), kstrtoul(),                                                                                                                  critical.
      and ‘list for each’, simplifying the analysis and making the analysis                           The constraints of the use are post-constraints C𝑝𝑜𝑠𝑡 [? ]. Theour
                                                                                                       use,   i.e., the  constraints     that    ensure     the   use  is  reachable.     In
    and
      more        for each’,2)simplifying
           ‘listscalable.                    the analysisandand   making the    LLMsanalysis
                                                                                         can
                               Function pointers               callbacks:                              example,postcondition,
                                                                                                      qualified      the constraint     is sscanf(...)>=4.
                                                                                                                                             , is a subset of P refined by C𝑝𝑜𝑠𝑡 :
    more      scalable.    2)  Function     pointers     and    callbacks:
      accurately interpret complex uses of function pointers as callbacks,       LLMs     can                                        P𝑞𝑢𝑎𝑙
                                                                                                           Æ Summarize the behavior of the initializer, capturing the vari-
    accurately
      which often    interpret
                        require complex    uses of function
                                 manual modeling.       We willpointers
                                                                   show anas      callbacks,
                                                                               interesting             able initialization status,Pi.e., either         must_init or may_init, given
    which
      case in  often
                  §6.6.require manual modeling. We will show an interesting                                                              𝑞𝑢𝑎𝑙 = P | C𝑝𝑜𝑠𝑡
                                                                                                       the path constraints learned in ≠. In our example, a correct response
    case in §6.7.                                                                                         For the sscanf() case, if the post-constraint is C𝑝𝑜𝑠𝑡 = ret ≥ 4,
      Smart Code Summarization. LLMs can work with complicated                                         should be must_init: a,b,c,d.
                                                LLMs                                                  the qualified postcondition would be P (𝑝𝑎𝑡ℎ 5 ) ∧ P (𝑝𝑎𝑡ℎ 6 ), which
    Smart
      functions;Code  forSummarization.
                           example, that they       can can   work with
                                                         summarize      loopcomplicated
                                                                               invariants                  If the �nal output is must_init, we can safely �lter out such
                                                                                                      ensures that variables a, b, c, and d must be initialized; therefore,
    functions;
      [26], whichfor   is example,   thatdifficult
                                            they can    summarize
                                                            in programloop      invariants             cases    as non-bugs;     if the output
                          an inherently               task                 analysis.   This           all variables    used subsequently        are isinitialized,
                                                                                                                                                        may_init,   andwenowillUBIconsider
                                                                                                                                                                                     happens.it a
    [26],   which     is an  inherently   di�cult     task  in program
      is likely because it has been trained on various functions with loopsanalysis.     This          potential     bug.  Note    that   this   simple     policy   may     still lead  to false
                                                                                                          In subsequent discussions, unless otherwise specified, the term
    isand
       likely    because    it has been trained      on various   functions
             their semantics. In contrast, traditional static analysis follows  with   loops           alarms     (which   we    evaluate     in  §6).  For   example,     our     work�ow      by
                                                                                                      ‘postcondition’ shall denote ‘qualified postcondition’.
    and    their semantics.
      explicitly                 In contrast,
                     defined rules  without atraditional        statictoanalysis
                                                   limited ability       generalize. follows           design does not take into account preconditions,
    explicitly de�ned rules without a limited ability to generalize.
                                                                                                      3.2      Post-Constraint Guided Path Analysis
     3 PROBLEM FORMULATION                                                                             4 DESIGN
                                                                                                      When    analyzing a routine or function in a path-sensitive manner,
    33.1PROBLEM    FORMULATION
          Definitions and Scope                                                                        Wenumber
                                                                                                            have illustrated   theexplore
                                                                                                                                    conceptual   work�ow
                                                                                                      the            of paths to           can grow   rapidly.previously   in Figure
                                                                                                                                                                Fortunately,  if we 4
    Based
     3.1.1 on   our observation, we propose
             Use-Before-Initialization.     A UseLL���,
                                                     Beforean     automated (UBI)
                                                               Initialization agent                    that information
                                                                                                      have   works together aboutlogically
                                                                                                                                    what thetofunction
                                                                                                                                                 solve our    formulated
                                                                                                                                                         is expected         problem.
                                                                                                                                                                        to achieve
    that  interfaces    with  UBITect    and   LLMs     (e.g.,  ChatGPT)
     bug refers to the erroneous scenario where a variable 𝑣 is accessed    to help                    However,
                                                                                                      (given  by Cto   achieve
                                                                                                                    𝑝𝑜𝑠𝑡        better
                                                                                                                         ), we can      results,
                                                                                                                                     prune   pathswethat
                                                                                                                                                      have  to overcome
                                                                                                                                                         inherently    don’ta meet
                                                                                                                                                                              number
    identify  and   reason   about  UBI  bugs   in the   Linux   kernel.
     or involved in any operation prior to its correct initialization. Let:                            of challenges
                                                                                                      those             in interacting
                                                                                                             expectations.              with LLMs.
                                                                                                                              We categorize           This means
                                                                                                                                                two scenarios,      that applica-
                                                                                                                                                                 direct   will need to
    Scope.• Our
              𝑑 (𝑣)goal   of developing
                      represent          LL��� isofnot
                                 the declaration       𝑣. to replace UBITect and                       mapand
                                                                                                      tion   the outcome
                                                                                                                 conceptual     work�ow
                                                                                                                             conflicts,  in into an instantiated
                                                                                                                                             applying               work�ow which
                                                                                                                                                       this optimization.
    static analysis    in general.  Instead,  we   aim
            • 𝑢 (𝑣) signify a use operation involving    to use
                                                             𝑣. LL��� to analyze                         Letfollow
                                                                                                       will   𝑅 be the   routine of
                                                                                                                      a number    or principles
                                                                                                                                     function under    analysis
                                                                                                                                                  described       and section.
                                                                                                                                                              in this S(𝑅) be its
    the di�cult    cases  for UBITect,  i.e., 40%   of cases
            • 𝑖 (𝑣) denote the initialization operation of     that
                                                                  𝑣. are considered                   path set. Let 𝑝𝑎𝑡ℎ ∈ S(𝑅) refer to a specific path in 𝑅. Besides,
    inconclusive. In other words, we aim to use LL��� primarily as a                                  Each
                                                                                                       4.1 path   𝑝𝑎𝑡ℎ hasChallenges
                                                                                                               Design         an associated path constraint 𝑝 that dictates its
        if there exists 𝑑 (𝑣) and 𝑢 (𝑣), then 𝑣 is used before initialization if:                     feasibility. These two optimizations can be formed with:
    complementary solution to UBITect. This relationship is depicted                                   It is non-trivial to prompt LLMs e�ectively [28, 42]. We meet the
    in Figure∃𝑣 2. : (𝑑 (𝑣) < 𝑢 (𝑣)) ∧ ¬(∃𝑖 (𝑣) : 𝑑 (𝑣) < 𝑖 (𝑣) < 𝑢 (𝑣))        (1)                   Direct         challengesFor
                                                                                                               Application.
                                                                                                       following                   anddirect
                                                                                                                                        proposeapplication,
                                                                                                                                                   solutions thecorrespondingly
                                                                                                                                                                  post-constraint in
    Assumptions.      As aa�rst
      where < indicates          exploratory
                             temporal        study
                                      sequence       of assisting
                                                 in the  programstatic  analy-
                                                                  execution.                            𝑝𝑜𝑠𝑡 can be
                                                                                                      Cdesigning       directly
                                                                                                                    LL���.      applied   as  a path constraint.   A path can be
    sis with LLMs, we restrict our scope to commonly observed patterns                                discarded   if:
                                                                                                       • C1. Limited Understanding of Postconditions. Despite LLMs
      3.1.2exceed
    that      Postcondition.
                  the time andPostconditions encapsulate
                                 memory limits             the expected
                                                 set for UBITect’s      state
                                                                    symbolic                              (e.g., GPT-4) are able to comprehend the de�nition of postcondi-
      or behavior
    execution       of aSpeci�cally,
                stage.    system upon    the conclusion
                                     depicted  in Figure 3,ofwe
                                                              a routine
                                                                 observe[18].
                                                                          that                            tions and apply them ¬(𝑝
                                                                                                                                 in(𝑝𝑎𝑡ℎ)
                                                                                                                                    simple∧scenarios,
                                                                                                                                             C𝑝𝑜𝑠𝑡 ) we found their capacity
    it is often the case that the variable is declared in one function and 3                              to utilize this knowledge in actual program analysis—such as
                                                                                                  3
                                                                                                                 Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian


   This implies that if a 𝑝𝑎𝑡ℎ inherently contradicts the                                                                           UBITect reports potential use-
post-constraint, it can be removed from consideration.                                                                                before-initialization bugs
Outcome Conflicts. Let O (𝑝) denote the set of all outcomes or                                                                  1
                                                                                                                                    Identify the initializer: sscanf
effects produced by path 𝑝. A path can be pruned if any of its
outcomes conflict with the post-constraint:
                                                                                                                                2
                                                                                                                                     Extract the post-constraint:
                                                                                                                                                ret>=4
                    ∃𝑜 ∈ O (𝑝𝑎𝑡ℎ) : ¬(𝑜 ∧ C𝑝𝑜𝑠𝑡 )                                                                               3
                                                                                                                                     Analyze the initializer with
   This stipulates that if an outcome from 𝑝𝑎𝑡ℎ inherently con-                                                                       post-constraint guidance
tradicts the post-constraint, that path can be disregarded in the
analysis.                                                                       Figure 4: Example run of LLift. For each potential bug, LLift ① (Φ1 ) identifies
                                                                                its initializer, ② (Φ2 ) extracts the post-constraints of the initializer, and ③ (Φ3 )
Correctness. The validity of these optimization methods can be                  analyzes the behavior of the initializer with the post-constraints via LLM.
proved by contradiction. Consider an instance where one of these
paths is executed. If this path conflicts with the Cpost , it would
                                                                                practice presents its challenges. Even with the advanced knowledge
render 𝑢 (𝑣) unreachable. Thus, it becomes evident that such paths
                                                                                and analytical capabilities of cutting-edge LLMs, achieving optimal
can be pruned without sacrificing the correctness of the analysis.
                                                                                results remains a challenge. Throughout the development of LLift,
   We provide a concrete example of how we perform these opti-
                                                                                we identified several obstacles and subsequently introduced four
mizations in §4.3.3.
                                                                                distinct design components to effectively address these challenges.
3.3    Conceptual Workflow
                                                                                4.1     Design Challenges
Given a bug report containing a suspicious variable 𝑣 and its resid-
ing function 𝐹 , the workflow Φ is as follows:                                  It is non-trivial to prompt LLMs effectively [28, 41]. We meet the
                                                                                following challenges and propose solutions correspondingly in
    (1) Φ1 (𝐹, 𝑣) → {𝑖 (𝑣)}: Identify potential initializers for 𝑣 from
                                                                                designing LLift.
        the bug report.
                                                                                • C1. Limited Understanding of Post-constraint. Despite
    (2) Φ2 (𝐹, 𝑖 (𝑣)) → C𝑝𝑜𝑠𝑡 : Extract the C𝑝𝑜𝑠𝑡 from the bug report
                                                                                   LLMs (e.g., GPT-4) are able to comprehend the definition of
        for each 𝑖 (𝑣).
                                                                                   post-constraint and apply them in simple scenarios, we found
    (3) Φ3 (𝐹, {𝑖 (𝑣), C𝑝𝑜𝑠𝑡 }) → InitStatus(𝑣): Summarize the ini-
                                                                                   their capacity to utilize this knowledge in actual program
        tialization status for variable 𝑣 after all possible initializers
                                                                                   analysis—such as summarizing function behavior in line with
        completion (merge multiple initializers).
                                                                                   specific post-constraint —to be limited. This critical limitation
Decision Policy. The decision policy Δ is defined as:                              often results in unpredictable and inconsistent outcomes.
            Δ(InitStatus(𝑣) = must_init) : non-bug                              • C2. Token Limitations. It is known that LLMs have token
                                                                                   limitations. For example, GPT-3.5 supports 16k tokens and GPT-4
            Δ(InitStatus(𝑣) ≠ must_init) : potential bug
                                                                                   supports 32k tokens [20]. This means that we do not want to
   In this policy, we adopt a conservative approach by treating all                copy a large number of function bodies in our prompts to LLMs.
variables not explicitly marked as must_init as potential vulnerabili-          • C3. Unreliable and Inconsistent Response. LLMs are known
ties. And it is worth noting that this policy may introduce some false             to result in unreliable and inconsistent responses due to halluci-
positives. For example, it might over-approximate preconditions.                   nation and stochasticity [41]. Stochasticity refers to the inherent
   Conceptually, LLift will not miss more bugs. The post-constraint                unpredictability in the model’s outputs [32]; and the halluci-
guided path optimizations and decision policies are safe.                          nation refers to LLMs generating nonsensical or unfaithful re-
                                                                                   sponses [11, 42]. By design, the stochasticity can be mitigated
3.4    Turns and Conversations in LLMs                                             with lower temperature, a hyperparameter controlling the degree
We define two key concepts in interacting with LLMs: turn and                      of randomness in outputs [27]; however, reducing temperature
conversation.                                                                      may impair the model’s exploring ability [37] and therefore may
• Turn: A turn encapsulates a singular interaction with the LLM.                   miss corner cases that result in vulnerabilities.
  Formally, it’s defined as a tuple, (𝑝, 𝑟 ), where 𝑝 represents the
  problem or question, and 𝑟 denotes the LLM’s response.                        4.2     Design Overview
• Conversation: Leveraging the capabilities of LLMs often                       We will discuss our design strategies to address the above chal-
  necessitates a series of interactions, especially for complex                 lenges in the rest of the section. Before that, we provide a high-level
  problem-solving. A conversation is an ordered sequence of                     overview of our solution.
  turns. A conversation comprising 𝑛 turns can be expressed as                  • To tackle challenge C1 (Post-constraint), we propose to encode
  [(𝑝 1, 𝑟 1 ), (𝑝 2, 𝑟 2 ), . . . , (𝑝𝑛 , 𝑟𝑛 )].                                 (D#1) Post-Constraint Guided Path Analysis by teaching
                                                                                   LLMs with examples, or few-shot in-context learning, of post-
4     DESIGN                                                                       constraints. This approach enables LLMs to learn from a small
In Section §3.3, we introduced a conceptual workflow. Elaborating                  number of demonstrative examples, assimilate the underlying
on that foundation, Figure 4 showcases a compelling illustration of                patterns, and apply this understanding to process post-constraint
our methodological approach. Yet, translating this workflow into                   guidance in our analysis.
                                                                            4
The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models           The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models


                                                                                                     Table2:2:Two
                                                                                                    Table     Twotypes
                                                                                                                  types of
                                                                                                                        of post-constraints
                                                                                                                           post-constraints and
                                                                                                                                            and their
                                                                                                                                                their variants.
                                                                                                                                                      variants.
 Convo.1: Initializer &                 Convo.2: Initializer Behavior Summarization                                                                                              details on
          Post-constraints Extraction
                                                                                            Check Before Use                        Failure Check                                automatic
    Prompt LLMs to extract the                      Prompt LLMs to summarize                                                                                                     response.
                                                                                            Type A:                                 Type B:
   initializer & post-constraints                        the initializer                                                                                                            Speci�c
                                                                                            if (sscanf(...) >= 4) {                 err = func(&a);
                                                                                              use(a, b, c, d);                      if (err) { return/break/goto; }              a speci�c
                                                                                            }                                       use(a)                                             [{ ty

                                                                                            Type A’:                                Type B’:                                        Subseq
                                                    Perform Progressive Prompt
                                                    with requested information              switch(ret=func(&a)){                   while(func(&a)){                             each requ
      Perform Self-validation
                                                                                               case some_irrelevant_case:               do_something(...);                       ing code
                                                                                                 do_something(...);                 }
      with previous response
                                              If need more          If succeed
                                                                                                 break;                             use(a);                                      code. Tho
                                                                                               case critical_case:                                                               function d
                                                    Perform Self-validation with            }
                                                                                                 use(a);
                                                                                                                                                                                 support to
                                                         previous response                                                                                                          The ite
                                                                                                                                                                                 quests add
                                                                                                                                                                                 details. In
                                                                                          thaterror    conditions
                                                                                                  current            cause
                                                                                                           LLMs (e.g.,      the use
                                                                                                                         GPT-4)   aretonotbecome
                                                                                                                                            nativelyunreachable,
                                                                                                                                                      sensitive toastheillus-
                                                                                                                                                                          sen-   informati
       Conclude the previous                           Conclude the previous                    tratedwithout
                                                                                          sitivity;     in TypeanyB, the  post-constraint
                                                                                                                      additional             is 4AALLMs
                                                                                                                                  instructions,     7! 0.usually
                                                                                                                                                          Type B’overlook
                                                                                                                                                                    depicts      prompt th
                                                                                          the apost-constraints.
                                                                                                   variant where the initializer keeps retrying til success, and
         response in JSON                                response in JSON
                                                                                                                      Therefore, we teach the LLM to be sensitive to             the LLM i
                                                                                                therefore with expected output A4C 7! 0, which indicates its �rst                data and
                                                                                          post-constraints rules through few-shots in-context learning. We
                                                                                                successful execution to break the endless loop.                                  analysis e
Figure 5: The workflow of LLift. Given a potential bug, we let LLM first iden-            describe the design details as follows:
tify the initializer and then extract its post-constraints (Convo.1), then leverage        4.3.2 Function Behavior Summarization. Once we obtain the post-
them to summarize the behavior of the initializer (Convo.2). A conversation               4.3.1 Post-Constraints Extraction. To extract the qualified postcon-                   4.5     De
                                                                                           contraints in Convo.1, we feed them to the LLM to obtain the behav-
consists of prompts (boxes) and responses (edges).                                        dition, we first determine the post-constraints that lead to the use
                                                                                           ior summary in Convo.2 . For example, we provide the following:                       We system
                                                                                          of{ suspicious variables. We incorporate few-shot in-context learn-
                                                                                                                                                                                 vital elem
                                                                                          inginitializer
                                                                                                 to teach LLMs: rethow    to extract %u.%u.%u.%u%n
                                                                                                                      = sscanf(str,   such constraints     from the caller
                                                                                                                                                      ,&a,&b,&c,&d,&n)    ,
• To tackle challenge C2 (Token Limitation), We employ two strate-                             suspicious : [ a , b , c , d ],                                                   primarily
                                                                                          context.    Table 2 demonstrates
                                                                                               postconstraint    : ret >= 4       how we teach LLM with in-context
  gies: (D#2) Progressive Prompt. Instead of copying a large num-                          }
                                                                                          learning.     We may
                                                                                                             focusrespond
                                                                                                                    primarily   on two types of code patterns:                   Multistag
  ber of function bodies (i.e., subroutines), we only provide function                          The LLM                      with
                                                                                          •{ Check       Before Use. Type A is our motivating example; by look-                  ploy a two
  details on demand, i.e., when LLMs are not able to conduct a re-                             ret : success ,
                                                                                              ing   at its: check,
                                                                                               response     {        the post-constraint should be 𝑟𝑒𝑡 ≥ 4. Type                 versation
  sult immediately. (D#3) Task Decomposition. We break down                                       must_init : [ a , b , c , d ],
                                                                                              A’ may_init
                                                                                                   describes   a similar                                                         and respo
                                                                                                            : [{  name : ncase   with switch-cases,
                                                                                                                            , condition     : ret > 4 }] with expected
  the problem into sub-problems that can be solved in independent                                                                                                                extracting
                                                                                           } output 𝑟𝑒𝑡 ↦→ crticial_case.
                                                                                               }
  conversations, i.e., a sequence of prompt and response pairs.                                                     This pattern     capturesthe thepostcondition,
                                                                                                                                                     opposite of the     first   tasks 1 an
                                                                                                The response
                                                                                          • Failure       Check. succinctly   encapsulates                           where
• To tackle challenge C3 (Unreliable Response), we employ the                                 pattern.a,b,c,d
                                                                                                          They commonly        occur    in the Linux    kernel   where the       on summ
                                                                                           variables               are classi�ed   as must_init,     and  n is categorized
  following strategies: (D#4) Self-Validation. We ask LLMs to                                                                                                                    identi�ed
                                                                                           aserror    conditions
                                                                                                may_init.           cause
                                                                                                              This is  due the   useinitialization
                                                                                                                            to the    to become unreachable,        as illus-
                                                                                                                                                     of n only occurring
  review and correct their previous responses. This helps improve                                                                                                                and e�ect
                                                                                           when
                                                                                              trated        4, and
                                                                                                    A4Cin>Type   B, not
                                                                                                                    the when    A4C 7! 4. is 𝑒𝑟𝑟 ↦→ 0. Type B’ depicts
                                                                                                                         post-constraint
  the consistency and accuracy based on our observation. Besides,                                                                                                                three subt
                                                                                              aNote    thatwhere
                                                                                                  variant    this seemingly    simplekeeps
                                                                                                                    the initializer      interaction   with
                                                                                                                                                retrying  til LLMs  canand
                                                                                                                                                               success,    be
  (D#2) Progressive Prompt and (D#3) Task Decomposition also                                                                                                                     decompos
                                                                                           challenging
                                                                                              therefore withfor static  analysis
                                                                                                                 expected         or symbolic
                                                                                                                             output   𝑟𝑒𝑡 ↦→ 0,execution.     Consider
                                                                                                                                                  which indicates        the
                                                                                                                                                                     its first
  help to deal with this challenge. Additionally, we implement                                successful
                                                                                           sscanf()       example,
                                                                                                             executioneven
                                                                                                                         toifbreak
                                                                                                                              the analysis    is aware
                                                                                                                                    the endless    loop.that the quali�ed        Thinking
  majority voting by running each case multiple times and use                              postcondition should be limited to those where A4C 4, it would still                  output, su
  majority voting to combat stochasticity.                                                4.3.2
                                                                                           need to  Function
                                                                                                       enumerateBehavior   Summarization.
                                                                                                                     the paths                  Once wewhich
                                                                                                                                 inside of sscanf(),       obtaininvolves
                                                                                                                                                                   the post-     serve that
   We elaborate the design of (D#1 - #4) Post Constraint Guided                            loops andincan
                                                                                          contraints        Convo.1,   we feed
                                                                                                               easily lead       them to as
                                                                                                                            to timeouts    theexplained
                                                                                                                                                 LLM to obtain   the behav-
                                                                                                                                                          in §2.1.               prompted
Path Analysis, Progressive Prompts, Task Decomposition, and                               ior summary in Convo.2 . For example, we provide the following:                        mentally,
Self-Validation detailed in the rest of this section. The effectiveness                   {4.4    Design #2: Progressive Prompt                                                  prompts t
and efficiency of these design strategies are rigorously evaluated in                      "initializer": "ret = sscanf(str,'%u.%u.%u.%u%n',&a,&b,&c,&d,&n)",                    This emph
                                                                                           The  Linux  kernel
                                                                                                          ["a",has an"c",
                                                                                                                      extremely
                                                                                                                          "d"], large codebase. Summarizing
§6.4, revealing a substantial enhancement in bug detection within
                                                                                           "suspicious":        "b",
                                                                                                                                                                                 natural la
                                                                                           an initializer using
                                                                                           "postconstraint":     LLMs
                                                                                                              "ret >= 4"without providing any supplementary
the Linux kernel.                                                                         }function de�nitions can result in incomplete or erroneous responses.                  Conseque
                                                                                                                                                                                 processes
                                                                                            OnThetheLLM
                                                                                                     othermay
                                                                                                            hand,  �ooding
                                                                                                                respond      the LLM with every relevant function
                                                                                                                          with
4.3     Design #1: Post-Constraint Guided Path                                                                                                                                   their resp
                                                                                            de�nition upfront risks exceeding their context window limitations.
                                                                                          {
        Analysis                                                                                To address
                                                                                           "ret":            this dilemma, we choose to progressively provide
                                                                                                    "success",
                                                                                            function de�nitions    as needed. Illustrated in Figure 5, this approach,            4.6     De
The Linux kernel frequently employs return value checks as illus-                          "response":   {
                                                                                           which    we refer["a",
                                                                                              "must_init":     to as"b",          Prompt, fosters a dynamic inter-
                                                                                                                         "c", "d"],
                                                                                                                      Progressive                                                At times,
trated in Table 2. Through our detailed examination of non-bug                                "may_init": [{"name":"n", "condition": "ret > 4"}]
                                                                                            action  with  the LLM    rather than expecting a response in one shot.               iors, parti
instances, we found that a path-sensitivity analysis can effectively                         }
                                                                                          }Throughout this iterative exchange, we consistently prompt the                        constructs
eliminate over 70% of these negative cases. However, path-sensitive
                                                                                            LLM: “If you encounter uncertainty due to a lack of function de�ni-                  dition mus
static analysis usually suffers from path explosion, especially in                             The response succinctly encapsulates the function behavior,
                                                                                            tions, please signal your need, and I’ll supply them”. Should the LLM                to be may_
large-scale codebases like the Linux kernel.                                              where variables a,b,c,d are classified as must_init, and n is cat-
                                                                                            need more information, LL��� will promptly extract the relevant                      A4C 7! 0.
   Fortunately, we can prompt the LLM to collect C𝑝𝑜𝑠𝑡 and sum-                           egorized as may_init. This is due to the initialization of n only
                                                                                                                                                                      5
marize the function with respective to the C𝑝𝑜𝑠𝑡 . It is worth noting                     occurring when 𝑟𝑒𝑡 > 4, and not when 𝑟𝑒𝑡 ↦→ 4.
                                                                                      5
                                                                                                                     Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian

                                    must_init = ∅ if:
                                    C𝑝𝑜𝑠𝑡 = ⊤ or                                            Subsequently, LLift scans this format in the LLM’s response. For
1   int func(int* a){
2     if(some_condi)                ∀𝑝𝑠 ∈ {¬some_condi} : 𝑝𝑠 ⊥ C𝑝𝑜𝑠𝑡 ∧                   each requested function definition, LLift supplies its correspond-
3       return -1;                       ∀𝑜 ∈ {𝑟𝑒𝑡 ↦→ 0} : 𝑜 ⊥ C𝑝𝑜𝑠𝑡                     ing code along with comments extracted from the Linux source
4
5
      *a = ... // init
      return 0;                     must_init = {𝑎} if:                                  code. Though GPT-4 may seek other types of information beyond
6   }                               (¬some_condi) ∧ C𝑝𝑜𝑠𝑡 or                             function definitions (e.g., struct definitions), we currently limit our
                                    (𝑟𝑒𝑡 ↦→ 0) ∧ C𝑝𝑜𝑠𝑡                                   support to requests pertaining to function definitions.
                                                                                            The iterative process continues until either the LLM no longer re-
    Figure 6: A sample case of initializer func, *a is may_init or must_init under
    different post-constraints.
                                                                                         quests additional information, or LLift cannot supply the requested
                                                                                         details. In certain situations where LLift is unable to provide more
       Note that this seemingly simple interaction with LLMs can be                      information (e.g., the definition of an indirect call), LLift will still
    challenging for static analysis or symbolic execution. Consider the                  prompt the LLM to proceed with the analysis. In these instances,
    sscanf() example, even if the analysis is aware that the qualified                   the LLM is encouraged to infer the behavior based on the available
    postcondition should be limited to those where 𝑟𝑒𝑡 ≥ 4, it would still               data and its inherent knowledge, thereby facilitating continued
    need to enumerate the paths inside of sscanf(), which involves                       analysis even when not all information is directly accessible.
    loops and can easily lead to timeouts as explained in §2.1.
                                                                                         4.5    Design #3: Task Decomposition
    4.3.3 Apply Path Analysis. Following §3.2, Figure 6 presents a con-
                                                                                         We systematically apply the principle of task decomposition, a
    cert example of post-constraint guided path analysis. This case
                                                                                         vital element of our design process. This concept is incorporated
    shows a simple initializer 𝑖 (𝑎) of the variable 𝑎. Given an early
                                                                                         primarily in two distinct ways.
    return, the initialization in line 4 may not be executed. As such, the
    qualified postconditions become contingent on the post-constraints                   Multistage Problem Solving. As illustrated in Figure 5, we em-
    C𝑝𝑜𝑠𝑡 . There are:                                                                   ploy a two-conversation approach to complete the task. Each con-
    • If the use of variable a is unconditional, i.e., C𝑝𝑜𝑠𝑡 = ⊤. In this                versation, essentially consists of multiple iterations of prompts
       case, the variable 𝑎 is labeled as may_init given that the initial-               and responses. The first conversation (Convo.1) is dedicated to
       ization may not be reached.                                                       extracting the initializer and its associated post-constraints (sub-
       In general, if all path constraints and outcomes of must_init                     tasks 1 and 2), while the second conversation (Convo.2) focuses
       are disjoint from C𝑝𝑜𝑠𝑡 , no path can be pruned out. We could also                on summarizing the function (subtask 3) based on the previously
       conclude 𝑎 as may_init.                                                           identified post-constraints. This division allows a more manageable
    • If the use of variable 𝑎 is conditional with constraints, i.e., C𝑝𝑜𝑠𝑡 ≠            and effective way of achieving the task, compared to combining all
       ⊤, two cases emerge:                                                              three subtasks into a single conversation. The efficacy of this task
        (1) C𝑝𝑜𝑠𝑡 clashes with the constraints of the path (e.g.,                        decomposition approach is further evaluated in §6.5.
            some_condi), or                                                              Thinking in English. Our workflow necessitates a structured
        (2) C𝑝𝑜𝑠𝑡 conflicts with the path outcome (e.g., return -1).                     output, such as a JSON format, for automation. However, we ob-
       In these instances, C𝑝𝑜𝑠𝑡 could be some_condi or func(...)==0                     serve that LLMs often produce suboptimal results when directly
       and we can designate *a as must_init.                                             prompted to output in this format. As LLMs build responses incre-
                                                                                         mentally, word-by-word, based on preceding outputs [32], direct
    4.4     Design #2: Progressive Prompt                                                prompts to output JSON may interrupt their thought progression.
    The Linux kernel has an extremely large codebase. Summarizing                        This emphasizes the importance of initially soliciting responses in
    an initializer using LLMs without providing any supplementary                        natural language to ensure comprehensive and effective reasoning.
    function definitions can result in incomplete or erroneous responses.                Consequently, we instruct the LLM to first articulate their thought
    On the other hand, flooding the LLM with every relevant function                     processes in English, followed by a subsequent prompt to transform
    definition upfront risks exceeding their context window limitations.                 their response into a JSON summary.
       To address this dilemma, we choose to progressively provide
    function definitions as needed. Illustrated in Figure 5, this approach,              4.6    Design #4: Self-Validation
    which we refer to as Progressive Prompt, fosters a dynamic inter-                    At times, LLMs can display unpredictable or inconsistent behav-
    action with the LLM rather than expecting a response in one shot.                    iors, particularly in complex scenarios involving detailed logical
    Throughout this iterative exchange, we consistently prompt the                       constructs. Consider a case where an initializer carries the postcon-
    LLM: “If you encounter uncertainty due to a lack of function defini-                 dition must_init if 𝑟𝑒𝑡 ↦→ 0. LLMs may still mistakenly assume it
    tions, please signal your need, and I’ll supply them”. Should the LLM                to be may_init, despite the explicit presence of the post-constraint
    need more information, LLift will promptly extract the relevant                      𝑟𝑒𝑡 ↦→ 0.
    details on demand from the source code and provide it to the LLM                        Conversely, an LLM might erroneously interpret a non-existent
    automatically, enabling it to reassess and generate a more accurate                  post-constraint and incorrectly infer a may_init case as must_init.
    response.                                                                            This phenomenon is known as hallucination. Essentially, the hallu-
       Specifically, We teach the LLM to ask for more information with                   cination can lead to both false positives and false negatives in bug
    a specific format:                                                                   detection, thereby affecting accuracy and reliability.
        [{"type":"function_def", "name":"some_func" }]                                      In addition to task decomposition, we also introduce the concept
                                                                                         of self-validation to enhance reliability. Before the LLM reaches its
                                                                                     6
The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models


final conclusion, this method reinforces specific rules, allowing the                  and 2 for GPT models); however, an overly low temperature can
LLM to reassess their previous responses for adherence and make                        result in repetitive or overly simplistic responses. We set it to 1.0
necessary corrections. We observed that this practice yields better                    (also the default of gpt-4-0613), which allows for higher-quality
results. We evaluate the effect of self-validation in §6.4.                            responses, and use strategies such as self-validation and majority
   As seen in Figure 5, we employ self-validation in both conversa-                    voting to improve the consistency of responses.
tions. By prompting a list of correct properties that we expect, LLMs
can verify and correct their results by themselves automatically.
                                                                                       6     EVALUATION
4.7     Additional Prompting Strategies                                                Our evaluation aims to address the following research questions.
                                                                                       • RQ1 (Precision): How accurately is LLift able to identify bugs?
In order to further optimize the efficacy of our model, we have
                                                                                       • RQ2 (Recall): Is there a possibility for LLift to miss real bugs?
incorporated several additional strategies into our prompt design:
                                                                                       • RQ3 (Comparison): How does the performance of individual
• Chain-of-Thought. Leveraging the Chain-of-Thought (CoT)
                                                                                         components within LLift compare to that of the final design?
  approach, we encourage the LLMs to engage in stepwise reason-
                                                                                       • RQ4 (Model Versatility): How does LLift perform when ap-
  ing, using the phrase “think step by step”. This not only helps
                                                                                         plied to LLMs other than GPT-4?
  generate longer, comprehensive responses, but it also provides
  intermediate results at each juncture of the thought process. Pre-                     We evaluate RQ1 to RQ3 in GPT-4, under API from OpenAI
  vious studies suggest the CoT approach considerably enhances                         with version gpt4-0613. For RQ4, we also test GPT-3.5 with version
  the LLMs’ reasoning capabilities [3]. We incorporate the CoT                         gpt-3.5-turbo-0613 and Claude 2 additionally for comparison.
  strategy into every prompt.
• Source Code Analysis. Rather than analyzing abstract repre-                          6.1    Dataset
  sentations, we opt to focus our attention directly on the functions
  within the source code. This approach not only economizes on                         Our experiment data, sourced from UBITect, includes all potential
  token use compared to LLVM IR, but also allows the model to                          bugs labeled by its static analysis stage but experienced timeout or
  leverage the semantic richness of variable names and other pro-                      memory exhaustion during its symbolic execution stage. Overall,
  gramming constructs to conduct a more nuanced analysis.                              UBITect’s static analysis stage produced 140,000 potential bugs,
                                                                                       with symbolic execution able to process only 60%, leaving 53,000
There are still some interesting details in designing an effective                     cases unattended, which means that these cases are generally diffi-
prompt but due to space constraints and without changing the                           cult for static analysis or symbolic execution to decide We craft the
overall strategy, we will not list them all. Readers intrigued can                     following dataset from 53,000 cases to evaluate LLift:
delve into the intricacies of our open-sourced prompt1 design and                          (1) Random-1000. We randomly chose 1,000 from the 53,000
experimental implementations to gain a deeper understanding.                           cases for testing. However, there are 182 cases where there are no
                                                                                       initializers, which are automatically recognized and filtered (see
5     IMPLEMENTATION                                                                   §3). The remaining 818 cases are used in evaluating precision, i.e.,
We implement the prototype of LLift based on OpenAI’s API [19]                         the ratio of true positives to false positives.
(i.e., gpt-4-0613). We describe some implementation details in the                         (2) Bug-50. This dataset comprises the 52 confirmed UBI bugs
following aspects:                                                                     previously identified by UBITect. It is used as ground truth for
Interaction with LLMs. LLift’s interaction with LLMs is managed                        assessing recall by verifying if any true bugs were overlooked.
by a simple agent developed in Python, containing roughly 1,000                            (3) Cmp-40. This dataset comprises 27 negative and 13 positive
lines of code. In addition, it uses seven prompts, which altogether                    cases selected from the Random-1000. We utilize this dataset to
constitute about 2,000 tokens in two conversations. All interactions                   illustrate which of our design strategies contributed most to the
are fully automated via APIs of OpenAI. Besides sending prompts                        outcome of our solution.
and waiting for responses, our agent also 1) interacts with LLMs                       Turns and Conversations. Due to the progressive prompt, each
according to the progressive prompt design, 2) locates function                        case may require different turns (pairs of a prompt and a response).
definitions within the Linux source code, and 3) processes responses                   In Random-1000, the average number of turns is 2.78, with a max
from LLMs, then receives and stores to a database.                                     of 8 and a variance of 1.20.
Hyper-Parameters. There are several hyper-parameters in                                Cost. On average, it costs 7,000 tokens in GPT-4 to analyze each
calling the APIs provided by OpenAI. We choose max_token and                           potential bug.
temperature to 1,024 and 1.0, respectively. max_token controls
the output length; since LLMs always predict the next words by
                                                                                       6.2    RQ1: Precision
the previous output, the longer output can benefit and allow its
reasoning. However, too many tokens will exhaust the context                           LLift reports 26 positives among the Random-1000 dataset, where
window quickly, so we pick 1024 as a reasonable balance.                               half of them are true bugs based on our manual inspection. This
   The temperature controls the randomness and also the ability to                     represents a precision of 50%. In keeping with UBITect and we
reason. Intuitively, we want the analysis to be as non-random as                       focus on the analysis of Linux v4.14, 12 of the bugs still exist in the
possible and reduce the temperature (it can take a value between 0                     latest Linux kernel. We are in the process of reporting the 12 bugs
                                                                                       to the Linux community. So far, we have submitted patches for 4
1 https://sites.google.com/view/llift-open/prompt                                      bugs and received confirmation that they are true bugs.
                                                                                   7
                                                                                                             Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian


                                   Table 3: True bugs identified by LLift from Random-1000, analyzing in Linux v4.14

       Initializer              Caller                                File Path                                         Variable                 Line
       read_reg                 get_signal_parameters                 drivers/media/dvb-frontends/stv0910.c             tmp                      504
       regmap_read              isc_update_profile                    drivers/media/platform/atmel/atmel-isc.c          sr                       664
       ep0_read_setup           ep0_handle_setup                      drivers/usb/mtu3/mtu3_gadget_ep0.c                setup.bRequestType       637
       regmap_read              mdio_sc_cfg_reg_write                 drivers/net/ethernet/hisilicon/hns_mdio.c         reg_value                169
       bcm3510_do_hab_cmd       bcm3510_check_firmware_version        drivers/media/dvb-frontends/bcm3510.c             ver.demod_version        666
       readCapabilityRid        airo_get_range                        drivers/net/wireless/cisco/airo.c                 cap_rid.softCap          6936
       e1e_rphy                 __e1000_resume                        drivers/net/ethernet/intel/e1000e/netdev.c        phy_data                 6580
       pci_read_config_dword    adm8211_probe                         drivers/net/wireless/admtek/adm8211.c             reg                      1814
       lan78xx_read_reg         lan78xx_write_raw_otp                 drivers/net/usb/lan78xx.c                         buf                      873
       t1_tpi_read              my3126_phy_reset                      drivers/net/ethernet/chelsio/cxgb/my3126.c        val                      193
       pci_read_config_dword    quirk_intel_purley_xeon_ras_cap       arch/x86/kernel/quirks.c                          capid0                   562
       ata_timing_compute       opti82c46x_set_piomode                drivers/ata/pata_legacy.c                         &tp                      564
       pt_completion            pt_req_sense                          drivers/block/paride/pt.c                         buf                      368


                                                                               Table 4: Performance evaluation of bug detection tool with progressive ad-
Imprecise and Failed Cases. Despite the effectiveness of LLift,                dition of design components: Post-Constraint Guided Path Analysis (PCA),
there are instances where it does not yield precise results, resulting         Progressive Prompt (PP), Self-Validation (SV), and Task Decomposition (TD).
in 13 false positives by mistakenly classifying must_init cases as             (C) indicates the number of Consistent cases.
may_init. Upon a careful examination of these cases, we attribute              Combination       TN(C)    TP(C)    Precision   Recall   Accuracy    F1 Score
the imprecision to a variety of factors, which we discuss in detail            Simple Prompt      12(9)    2(1)        0.12     0.15      0.35          0.13
in §6.7. Briefly, we give a breakdown of them here: Incomplete con-            PCA                13(9)    5(1)        0.26     0.38      0.45          0.31
straint extraction (4 cases), Information gaps in UBITect (5 cases),           PCA+PP             5(3)     6(1)        0.21     0.46      0.28          0.29
                                                                               PCA+PP+SV          5(2)     11(8)       0.33     0.85      0.40          0.48
Variable reuse (1 case), Indirect call (1 case), and Additional con-           PCA+PP+TD         22(14)    6(4)        0.55     0.46      0.70          0.50
straints (1 case). Additionally, there is one false positive caused by         PCA+PP+SV+TD      25(17)   13(12)       0.87     1.00      0.95          0.93
inconsistent output (i.e., two false positives in three runs). Four            Oracle            27(27)   13(13)        -          -         -           -
cases exceed the maximum context length while exploring deeper
functions in the progressive prompt.
                                                                                  Takeaway 2. LLift has proven effective in identifying UBI bugs,
                                                                                  consistently detecting all known instances.
  Takeaway 1. LLift Can effectively summarize initializer behav-
  ior and discover new bugs with high precision (50%).
                                                                               6.4      RQ3: Contributions of Design Strategies
                                                                               In our effort to delineate the contributions of distinct design strate-
                                                                               gies to the final results, we undertook an evaluative exercise against
6.3    RQ2: Recall Estimate                                                    the Cmp-40 dataset, employing varying configurations of our solu-
Conceptually, the core optimization (post-constraint guided path               tion, each entailing a unique combination of our proposed strate-
analysis) of LLift is sound, and we also prompt a series of rules to           gies. As illustrated in Table 4, the strategies under consideration
let LLMs tend to respond “may_init when uncertain. We expect                   encompass Post-constraint Analysis (PCA), Progressive Prompt
LLift would not reject true bugs or with a high recall.                        (PP), Self-Validation (SV ), and Task Decomposition (TD). The find-
   We sample 300 negative cases from Random-1000 in an effort to               ings underscore an overall trend of enhanced performance with the
see whether we will miss any true bugs. We confirm that all are true           integration of additional design strategies.
negatives. Despite the limited data sampled, this result indicates                 In this study, the Baseline corresponds to a straightforward
that integrating GPT-4 into our implementation does not introduce              prompt, "check this code to determine if there are any UBI bugs",
apparent unsoundness.                                                          a strategy that has been found to be rather insufficient for discover-
   Further, we test LLift on the Bug-50 dataset to see whether it will         ing new vulnerabilities, as corroborated by past studies [17, 21, 31],
miss any bugs discovered by UBITect. LLift has demonstrated full               reflecting a modest recall rate of 0.15 and a precision of 0.12.
effectiveness in identifying all real bugs from Bug-50. This result,               Incorporating PCA offers a notable enhancement, enabling the
while encouraging, does not imply that LLift is flawless. Detailed             LLM to uncover a wider array of vulnerabilities. As shown in Table
data analysis reveals that: 1) There remain some inconsistencies               4, there is a substantial improvement in recall in comparison to the
in 3∼5 cases occasionally, though they are mitigated by majority               baseline, an anticipated outcome considering PCA’s pivotal role in
voting; and 2) all the bugs found by UBITect have trivial post-                our solution. However, solely relying on this strategy still leaves a
constraints (C𝑝𝑜𝑠𝑡 = ⊤) and postcondition of may_init (P𝑞𝑢𝑎𝑙 :                 lot of room for optimization.
must_init ↦→ ∅). Hence, LLift could identify them easily. It is                    The influence of Progressive Prompt (PP) on the results is quite
noteworthy that these cases are already those cases detectable by              intriguing. While its impact appears to lower precision initially, the
UBITect. Such cases tend to be simpler in nature and can be verified           introduction of task decomposition and self-validation in conjunc-
by symbolic execution in UBITect.                                              tion with PP reveals a substantial boost in performance. Without
                                                                           8
 The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models                                                                 Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian

 Table5:5:Comparison
Table      Comparisonof
                      ofdi�erent
                         differentLLMs
                                   LLMson
                                        onreal
                                           realbugs,
                                                bugs,from
                                                      fromaasubset
                                                             subsetof
                                                                    ofBug-50
                                                                       Bug-50
                                                                                                            1        static int sgl_map_user_pages(...){
                                                                                                            2        ...
                                                    GPT
                                                   GPT                                                      3        if ((pages = kmalloc(..., GFP_KERNEL)) == NULL)
       Caller
       Caller                                             Claude2 Bard
                                                   4  3.5 Claude2 Bard
                                                  4 3.5
                                                                                                            4
                                                                                                            5
                                                                                                                       return -ENOMEM;
                                                                                                                     res = get_user_pages_unlocked(..., pages, ...);
                                                                                                            6          /* Errors and no page mapped should return here */
        hpet_msi_resume
       hpet_msi_resume                           3✓      3✓           3✓             7✗                     7        if (res < nr_pages)
                                                                                                            8            goto out_unmap;
        ctrl_cx2341x_getv4lflags
       ctrl_cx2341x_getv4l�ags                   3✓      3✓           7✗             7✗                     9        ...
        axi_clkgen_recalc_rate
       axi_clkgen_recalc_rate                    3✓      3✓           3✓             3✓
                                                                                                           10
                                                                                                           11
                                                                                                                     out_unmap:
                                                                                                                       if (res > 0) {
        max8907_regulator_probe
       max8907_regulator_probe                   3✓      3✓           3✓             3✓                    12            for (j=0; j < res; j++)
        ov5693_detect
       ov5693_detect                             3✓      3✓           7✗             3✓
                                                                                                           13             put_page( pages[j] );
                                                                                                           14             res = 0;
        iommu_unmap_page
       iommu_unmap_page                          3✓      7✗           3✓             7✗                    15          }
        mt9m114_detect
       mt9m114_detect                            3✓      3✓           3✓             3✓
                                                                                                           16
                                                                                                           17        }
                                                                                                                       kfree(pages);
        ec_read_u8
       ec_read_u8                                3✓      3✓           3✓             3✓
        compress_sliced_buf
       compress_sliced_buf                       3✓      3✓           7✗             3✓                          Figure
                                                                                                                  Figure6:7:Case
                                                                                                                             CaseStudy
                                                                                                                                  StudyII(Loop
                                                                                                                                          (Loopand
                                                                                                                                                andIndex).
                                                                                                                                                    Index).Derived
                                                                                                                                                            Derivedfrom
                                                                                                                                                                    fromdrivers/scsi/st.c
                                                                                                                                                                         drivers/scsi/st.c

                                                                                                                   It is imperative
                                                                                                                 decomposition          to note that not
                                                                                                                                     is implemented,           all design
                                                                                                                                                            these  modelsstrategies     in our tool-
                                                                                                                                                                            often misinterpret      or
  PP, the LLM is restricted to deducing the function behavior merely                                            box   are universally
                                                                                                                 inaccurately      collect applicable      acrosssubsequently
                                                                                                                                           post-constraints,        all language compromising
                                                                                                                                                                                    models. Bard
  based on the function context’s semantics without further code                                                and
                                                                                                                 the GPT-3.5,
                                                                                                                      results. To inharness
                                                                                                                                     particular,
                                                                                                                                               theirexhibit
                                                                                                                                                       maximumlimited  adaptability
                                                                                                                                                                    potential,        towards
                                                                                                                                                                                we only    applythethe
inanalysis.
    recall inEvencomparison
                         thoughtothis  the approach
                                             baseline, an   can anticipated
                                                                   be effective outcome      con-
                                                                                     in a range                 progressive
                                                                                                                 PCA designprompt          and task
                                                                                                                                  specifically    (i.e., decomposition      strategies.
                                                                                                                                                         without other design             Bard’s in-
                                                                                                                                                                                    strategies)    for
sidering     PCA’s     pivotal    role   in   our   solution.     However,
  of situations, it confines the reasoning ability to the information          solely    relying                teraction    patterns
                                                                                                                 GPT-3.5 and      Bard. suggest a preference for immediate response
on   this strategy
  available              still leaves
               in its training      data.a Bylot checking
                                                  of room for   theoptimization.
                                                                     detailed conversation,                     generation,     leveraging
                                                                                                                    Contrasting      the GPT its     internal
                                                                                                                                                 series,  Bard knowledge
                                                                                                                                                                 and Claude 2base     rather than
                                                                                                                                                                                 demonstrate      less
 weThe     in�uence
       notice             of Progressive
                  the omission         of TDPromptor SV tends(PP) on tothe    results
                                                                          result   in theis quite
                                                                                             LLM                requesting
                                                                                                                 familiarityadditional
                                                                                                                               with the Linuxfunction     de�nitions,
                                                                                                                                                      kernel    and are thereby
                                                                                                                                                                          more pronehindering     the
                                                                                                                                                                                          to failures
intriguing.      While     its  impact    appears       to lower
  neglecting the post-constraints, subsequently leading to errors.  precision    initially,   the               e�ectiveness      of the progressive
                                                                                                                 due to their unawareness          of theprompt
                                                                                                                                                            may_init approach.   Similarly,
                                                                                                                                                                         possibility           when
                                                                                                                                                                                      of initializers.
introduction        of  task    decomposition           and  self-validation
      Beyond influencing precision and recall, Task Decomposition                 in   conjunc-                 task decomposition is implemented, these models often misinterpret
tion
 (TD)withand PP     reveals a substantial
               Self-Validation        (SV ) alsoboost  play aincrucial
                                                                  performance.         Without
                                                                           role in enhancing                    or Takeaway
                                                                                                                   inaccurately4.collect
                                                                                                                                      GPT-4 post-constraints,        subsequently
                                                                                                                                               remains at the pinnacle                 compromis-
                                                                                                                                                                             of performance      for
PP,   the LLM In
  consistency.     is restricted
                       this context, to deducing
                                           a result isthe      function
                                                           deemed           behavior
                                                                       consistent         merely
                                                                                     if the  LLM                ingLLift,
                                                                                                                     the results.
                                                                                                                            yet otherToLLMs
                                                                                                                                         harnesscantheir
                                                                                                                                                      achievemaximum
                                                                                                                                                                 promisingpotential,
                                                                                                                                                                             results. we apply a
based     on   the   function      context’s        semantics
  yields the same outcome across its initial two runs. A comparison without     further     code                postcondition-aware design speci�cally (i.e., without other design
analysis.
  between Even         though this approach
               our comprehensive              final design canencompassing
                                                                  be e�ective inalla compo-range                strategies) for GPT-3.5 and Bard.
of  situations,
  nents,   and theitdesigns
                        con�nes       the reasoning
                                   lacking      TD and SV,   ability    to the information
                                                                 respectively,     reveals that                  6.6      Case Study
                                                                                                                   Contrasting the GPT series, Bard and Claude 2 demonstrate less
available
  both TD in  and itsSV
                      training
                          notably  data.   By checking
                                      augment                  the detailed
                                                      the number                conversation,
                                                                        of consistent      results,              In this casewith
                                                                                                                familiarity      study,
                                                                                                                                      thewe   pickkernel
                                                                                                                                           Linux      three interesting
                                                                                                                                                               and are more cases  demonstrating
                                                                                                                                                                                prone    to failures
weand deliver 17 and 23 consistent results in its negative in
      notice    the   omission       of   TD     or   SV   tends    to   result   andthe    LLM
                                                                                         positive                the toeffectiveness
                                                                                                                due                      of LLift
                                                                                                                         their unawareness             in analyzing
                                                                                                                                                  of the                function behaviors
                                                                                                                                                           may_init possibility                   and
                                                                                                                                                                                     of initializers.
neglecting       the postcondition,
  results, respectively,          underscoring subsequently        leading to errors.
                                                         their importance         in ensuring                    detecting uninitialized variables. All these cases are undecided
     Beyond      in�uencing                                                                                      Takeaway.          GPT-4   remains      at theUBITect.
                                                                                                                                                                  pinnacleWe of put
                                                                                                                                                                                performance      for
  reliable   and    consistent precision
                                    outcomes.and recall, Task Decomposition                                      for  the previous      static   analyzer,                           the complete
(TD)Finally,
        and Self-Validation                                                                                      LL���,   yet other   LLMs    can   achieve    promising   results.
                 TD also holds (SV         ) also playinaterms crucial of role in enhancing                      conversations on an anonymous online page for reference .                   2
                                      significance                        conserving       tokens.
  In our evaluation phase, we identified two instances ifwithin
consistency.      In  this   context,    a  result     is deemed      consistent       the LLM the              Loop Case
                                                                                                                     and Index. Figure 7 presents an intriguing case involving
yields
  PCA+PP  the and
                samePCA+PP+SV
                        outcome across            its initial two
                                           configurations              runs.the
                                                                   where      A comparison
                                                                                 token count
                                                                                                                6.7        Study
                                                                                                                 the variable pages[j], which is reported by UBITect as used
between
  surpassed   ourthecomprehensive
                       limitations set�nal           design encompassing
                                                by GPT-4.       However, this all        compo-
                                                                                     constraint                 In
                                                                                                                 inthis
                                                                                                                    Linecase
                                                                                                                          17 study,   we pick
                                                                                                                              potentially       three interesting
                                                                                                                                            without               cases demonstrating
                                                                                                                                                      being initialized.  Unfortunately,
nents,
 was not  andbreached
                the designs       lacking
                             in any    case TD  when andTD SV,was
                                                                respectively,
                                                                     incorporated.reveals that                  the
                                                                                                                 thise�ectiveness
                                                                                                                      case is a falseofpositive
                                                                                                                                        LL��� inwhich
                                                                                                                                                   analyzing   function
                                                                                                                                                         is hard to prunebehaviors  and
                                                                                                                                                                           due to loops.
both TD and SV notably augment the number of consistent results,                                                detecting   uninitialized   variables.  All these cases  are undecided
                                                                                                                 Specifically, the initializer function get_user_pages_unlocked(),
andTakeaway
       deliver 17 3.  and All23ofconsistent
                                   LLift’s design results   in its negative
                                                          strategies             and positive
                                                                         contributed      to the                for  the previous
                                                                                                                 which              static for
                                                                                                                         is responsible     analyzer,  UBITect.
                                                                                                                                                 mapping    user We  putpages
                                                                                                                                                                 space    the complete
                                                                                                                                                                               into  the
results,
    positiverespectively,
                results.         underscoring their importance in ensuring                                      conversations    on an  anonymous     online page for reference2.
                                                                                                                 kernel space, initializes the pages array allocated in Line        3. If
reliable and consistent outcomes.                                                                               Loop   and Index. Figure 6 presents
                                                                                                                 get_user_pages_unlocked()                   an intriguing
                                                                                                                                                     is successfully          case involving
                                                                                                                                                                        executed,   pages[0]
     Finally, TD also holds signi�cance in terms of conserving tokens.                                          the  variable
                                                                                                                 through        pages[j], which       is reported
                                                                                                                                               pointers               by UBITect
                                                                                                                                                          will be initialized     to as  used
                                                                                                                                                                                      point to
  6.5 RQ4: Alternative Models
In our evaluation phase, we identi�ed two instances within the
                                                                                                                            pages[res-1]
                                                                                                                in  Linepage
                                                                                                                 struct   17 potentially
                                                                                                                               instances. without being initialized. Unfortunately,
 Table 5 provides
PCA+PP        and PCA+PP+SVa comprehensivecon�gurationsview ofwhere
                                                                  the performance
                                                                            the token count of our
                                                                                                                thisTo
                                                                                                                     case  is a falsethe
                                                                                                                        summarize       positive which
                                                                                                                                           behavior,  i.e.,ismust_init
                                                                                                                                                              hard to prune
                                                                                                                                                                          factsdue   to loops.
                                                                                                                                                                                 under  condi-
  solution, LLift,
surpassed                 when implemented
                the limitations         set by GPT-4.   across    an arraythis
                                                              However,        of LLMs      includ-
                                                                                    constraint                  Speci�cally,
                                                                                                                 tions wherethe theinitializer function get_user_pages_unlocked(),
                                                                                                                                      use is reachable,    we must first extract the post-
  ing not
was    GPT-4.0,
             breachedGPT-3.5,
                            in anyClaude
                                      case when2 [2], and
                                                        TD wasBardincorporated.
                                                                     [12]. GPT-4 passes all
                                                                                                                which    is responsible
                                                                                                                 constraints  that lead to for   mapping
                                                                                                                                            the use of pages. userThrough
                                                                                                                                                                    space pages      into with
                                                                                                                                                                             interacting  the
  tests, while GPT-3.5, Claude 2, and Bard exhibit recall rates of 89%,
  Takeaway.                                                                                                     kernel
                                                                                                                 ChatGPT,space,  initializes
                                                                                                                             LLift            the pages
                                                                                                                                     successfully  extracts  array
                                                                                                                                                               it: allocated in Line 3. If
  67%,   and 67%,   Allrespectively.
                         of LL���’s design Despite       the unparalleled
                                                    strategies    contributedperformance
                                                                                  to the posi-
                                                                                                                get_user_pages_unlocked()           is successfully executed, pages[0]
  of
  tiveGPT-4,
        results.the other LLMs still produce substantial and competitive                                         {
                                                                                                                through    pages[res-1]"res = pointers   will be initialized to      point to
  results, thereby indicating the wide applicability of our approaches.                                              "initializer":           get_user_pages_unlocked(uaddr,      nr_pages,
                                                                                                                struct page   instances.
                                                                                                                           pages,   rw == READ ? FOLL_WRITE : 0)",
6.6It isRQ4:         Alternative
            imperative       to note thatModels  not all design strategies in our tool-                              "suspicious": ["pages[j]"],
                                                                                                                   To"postconstraint":
                                                                                                                       summarize the "res behavior,                      facts
  box   are   universally        applicable        across
                                                                                                                                                     i.e., must_init        j < under
                                                                                                                                                                                 res", condi-
                                                      view all    language      models.ofBard                                                  < nr_pages    && res > 0 &&
Table 5 provides a comprehensive                             of the    performance            our               tions
                                                                                                                 }     where the use is reachable, we must �rst extract the post-
  and GPT-3.5,
solution,     LL���, inwhen
                          particular,     exhibit limited
                                 implemented           across an adaptability
                                                                     array of LLMstowards      the
                                                                                          includ-               constraints that lead to the use of pages. Through interacting with
  progressive
ing                 prompt and
      GPT-4.0, GPT-3.5,          Claudetask2decomposition
                                                [2], and Bard [12].    strategies.    Bard’sall
                                                                            GPT-4 passes        in-                 After feeding the post-constraints to LLM, LLift then success-
                                                                                                                ChatGPT, LL��� successfully extracts it:
  teraction     patterns       suggest      a   preference       for
tests, while GPT-3.5, Claude 2, and Bard exhibit recall rates of 89%, immediate        response                 {
                                                                                                                 fully obtains the result:
  generation,
67%,    and 67%,leveraging
                      respectively. its internal
                                          Despite knowledge
                                                        the unparalleledbase rather       than re-
                                                                                performance                     {
                                                                                                                       initializer : res = get_user_pages_unlocked(uaddr, nr_pages,

ofquesting
    GPT-4, additional
               the other LLMs  functionstilldefinitions,     thereby hindering
                                               produce substantial                      the effec-
                                                                            and competitive
                                                                                                                õ!    pages, rw == READ ? FOLL_WRITE : 0) ,

  tivenessthereby
results,      of the indicating
                        progressivethe     prompt       approach. Similarly,
                                               wide applicability                    when task
                                                                          of our approaches.
                                                                                                                 2 https://sites.google.com/view/llift-open/case-studies
                                                                                                                2 https://sites.google.com/view/llift-open/case-studies

                                                                                                      89
     The
     The Hitchhiker’s
         Hitchhiker’s Guide
                      Guide to
                            to Program
                               Program Analysis:
                                       Analysis: AA Journey
                                                    Journey with
                                                            with Large
                                                                 Large Language
                                                                       Language Models
                                                                                Models                                                                                      Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian


11        static
          static int hv_pci_enter_d0(struct hv_device
                 int hv_pci_enter_d0(struct  hv_device *hdev){
                                                       *hdev){                                                                     11        int
                                                                                                                                              int p9_check_zc_errors(...){
                                                                                                                                                  p9_check_zc_errors(...){
22          ...
            ...                                                                                                                    22           ...
                                                                                                                                                ...
33          init_completion(&comp_pkt.host_event);
            init_completion(&comp_pkt.host_event);                                                                                 33           err
                                                                                                                                                err == p9pdu_readf(req->rc,
                                                                                                                                                       p9pdu_readf(req->rc, c->proto_version,
                                                                                                                                                                            c->proto_version, dd ,, &ecode);
                                                                                                                                                                                                    &ecode);
44          pkt->completion_func
            pkt->completion_func == hv_pci_generic_compl;
                                    hv_pci_generic_compl;                                                                          44           err
                                                                                                                                                err == -ecode
                                                                                                                                                        -ecode ;;
55          pkt->compl_ctxt
            pkt->compl_ctxt == &comp_pkt;
                               &comp_pkt;
66          ...
            ...                                                                                                                    55           ...
                                                                                                                                                ...
77                                                                                                                                 66        }}
                                                                                                                                   77
88             wait_for_completion(&comp_pkt.host_event);
               wait_for_completion(&comp_pkt.host_event);
99                                                                                                                                 88        int  p9pdu_readf(struct p9_fcall
                                                                                                                                              int p9pdu_readf(struct           *pdu, int
                                                                                                                                                                      p9_fcall *pdu,      proto_version, const
                                                                                                                                                                                     int proto_version,  const
                                                                                                                                              õ! char
                                                                                                                                             õ!   char *fmt,
                                                                                                                                                        *fmt, ...)
                                                                                                                                                              ...)
10
10             if
               if (( comp_pkt.completion_status
                     comp_pkt.completion_status << 0)
                                                   0)                                                                           99              ...
                                                                                                                                                ...
11
11             ...
               ...                                                                                                             10
                                                                                                                               10               ret
                                                                                                                                                ret == p9pdu_vreadf(pdu,
                                                                                                                                                       p9pdu_vreadf(pdu, proto_version,
                                                                                                                                                                         proto_version, fmt,
                                                                                                                                                                                         fmt, ap);
                                                                                                                                                                                              ap);
12
12        }}                                                                                                                   11
                                                                                                                               11               ...
                                                                                                                                                ...
13
13                                                                                                                             12
                                                                                                                               12               return
                                                                                                                                                return ret;
                                                                                                                                                        ret;
14
14        static
          static void
                 void hv_pci_generic_compl(void
                      hv_pci_generic_compl(void *context,
                                                 *context, ...){
                                                           ...){                                                               13
                                                                                                                               13            }}
15
15          struct
            struct hv_pci_compl
                   hv_pci_compl *comp_pkt
                                *comp_pkt == context;
                                             context;                                                                          14
                                                                                                                               14
16
16                                                                                                                             15
                                                                                                                               15            int    p9pdu_vreadf(struct p9_fcall
                                                                                                                                              int p9pdu_vreadf(struct                  *pdu, int
                                                                                                                                                                             p9_fcall *pdu,      proto_version, const
                                                                                                                                                                                             int proto_version, const
17
17             if
               if (resp_packet_size
                   (resp_packet_size >=
                                     >= offsetofend(...))
                                        offsetofend(...))                                                                                     õ! char
                                                                                                                                             õ!           *fmt, va_list
                                                                                                                                                    char *fmt,    va_list ap){
                                                                                                                                                                           ap){
18
18                comp_pkt->completion_status
                  comp_pkt->completion_status == resp->status;
                                                 resp->status;                                                                 16
                                                                                                                               16                 switch
                                                                                                                                                   switch (*fmt)
                                                                                                                                                           (*fmt) {{
19
19             else
               else                                                                                                            17
                                                                                                                               17                    case
                                                                                                                                                     case dd :{:{
20
20                comp_pkt->completion_status
                  comp_pkt->completion_status == -1;
                                                 -1;                                                                           18
                                                                                                                               18                      int32_t
                                                                                                                                                        int32_t *val      va_arg(ap, int32_t
                                                                                                                                                                  *val == va_arg(ap,   int32_t *);
                                                                                                                                                                                               *);
21
21                                                                                                                             19
                                                                                                                               19                      if
                                                                                                                                                        if (pdu_read(...))
                                                                                                                                                           (pdu_read(...)) {{
22
22             complete(&comp_pkt->host_event);
               complete(&comp_pkt->host_event);                                                                                20
                                                                                                                               20                                errcode   =  -EFAULT;
                                                                                                                                                                  errcode = -EFAULT;
23
23        }}                                                                                                                   21
                                                                                                                               21                                break;
                                                                                                                                                                  break;
                                                                                                                               22
                                                                                                                               22                      }}
     Figure                                                                                                                    23
                                                                                                                               23                      val
                                                                                                                                                        val == ...;
                                                                                                                                                               ...; //// initialization
                                                                                                                                                                          initialization
      Figure 7:
     Figure   8: Case
             7:  Case Study
                 Case  Study II
                      Study   II (Concurrency
                             II   (Concurrency and
                                 (Concurrency   and Indirect
                                               and   Indirect Call).
                                                    Indirect  Call). Derived
                                                              Call). Derived from
                                                                     Derived from
                                                                              from                                             24
                                                                                                                               24               }}
     drivers/pci/host/pci-hyperv.c
     drivers/pci/host/pci-hyperv.c
      drivers/pci/host/pci-hyperv.c                                                                                            25
                                                                                                                               25               return    errcode;
                                                                                                                                                 return errcode;
                                                                                                                               26
                                                                                                                               26            }}
            suspicious
            suspicious :: [[ pages[j]
                             pages[j] ],],
            postconstraint
            postconstraint :: resres << nr_pages
                                        nr_pages &&
                                                 && res
                                                    res >> 00 &&
                                                              && jj << res
                                                                       res ,,                                                                 Figure
                                                                                                                                               Figure8:
                                                                                                                                              Figure  9:Case
                                                                                                                                                     8: CaseStudy
                                                                                                                                                        Case StudyIII
                                                                                                                                                             Study III(Unfamiliar
                                                                                                                                                                   III  (UnfamiliarFunction),
                                                                                                                                                                       (Unfamiliar  Function),derived
                                                                                                                                                                                   Function),  derivedfrom
                                                                                                                                                                                              derived from
                                                                                                                                                                                                       fromnet/9p
                                                                                                                                                                                                           net/9p
                                                                                                                                                                                                            net/9p
     }}    "ret": "success",
         After
         After  feeding
                 feeding{ the
           "response":
                           the post-constraints
                                post-constraints toto LLM,
                                                      LLM, LL���
                                                              LL��� then
                                                                      then success-
                                                                             success-                                               merely
                                                                                                                                     merelyTheas as  aa blurry
                                                                                                                                                  case   blurry
                                                                                                                                                          presentssearch
                                                                                                                                                                   search anengine”
                                                                                                                                                                            engine”    [6],
                                                                                                                                                                              intriguing     is
                                                                                                                                                                                             is misguided
                                                                                                                                                                                       [6], real-world
                                                                                                                                                                                                 misguided    according
                                                                                                                                                                                                              according
                                                                                                                                                                                                           bug.              to
                                                                                                                                                                                                                              to our
                                                                                                                                                                                                                   The function     our
               "must_init": ["pages[j]"],
     fully
      fully obtains
             obtains the
                      the result:
               "may_init": result:
                             [],                                                                                                    experiments.
                                                                                                                                     experiments.          This
                                                                                                                                                            This    viewpoint
                                                                                                                                                                    viewpoint      is
                                                                                                                                                                                   is robustly
                                                                                                                                                                                      robustly     contradicted
                                                                                                                                                                                                    contradicted
                                                                                                                                       p9pdu_readf() mirrors sscanf() in structure, yet lacks a check                 by
                                                                                                                                                                                                                       by the
                                                                                                                                                                                                                           the  case
                                                                                                                                                                                                                                case
     {{ }                                                                                                                           illustrated
                                                                                                                                     illustrated
                                                                                                                                       of its return   in
                                                                                                                                                       in Figure
                                                                                                                                                           value, 8.
                                                                                                                                                           Figure      8.
                                                                                                                                                                       leaving    the parameter ecode at risk of being
            ret
       }    ret :: success
            response
                    success ,,
            response :: {{                                                                                                                The
                                                                                                                                          The casecase presents
                                                                                                                                       uninitialized,     presents       an
                                                                                                                                                                         an intriguing
                                                                                                                                                                             intriguing
                                                                                                                                                             i.e., if pdu_read()            real-world
                                                                                                                                                                                            real-world
                                                                                                                                                                                        returns           bug.
                                                                                                                                                                                                           bug.inThe
                                                                                                                                                                                                    non-zero         linefunction
                                                                                                                                                                                                                   The    function
                                                                                                                                                                                                                            19 (thus
                must_init
                 must_init :: [[ pages[j]
                                 pages[j] ],
                                           ],                                                                                       p9pdu_readf()
                                                                                                                                     p9pdu_readf()
                                                                                                                                     “break” early). Notably,   mirrors
                                                                                                                                                                mirrorsunlike
                                                                                                                                                                            sscanf()
                                                                                                                                                                             sscanf()      in
                                                                                                                                                                                           in structure,
                                                                                                                                                                                    sscanf(),   structure,  yet
                                                                                                                                                                                                            yet lacks
                                                                                                                                                                                                    where GPT-4   lackscanaaprovide
                                                                                                                                                                                                                             check
                                                                                                                                                                                                                              check
          As wemay_init
                  can see,::GPT-4
                 may_init    [], exhibits impressive comprehension of this
                             [],
                                                                                                                                    of    its  return     value,      leaving    the  parameter               at   risk   of  being
          }}                                                                                                                         of    its return      value,     leaving    the  parameter       ecode
                                                                                                                                                                                                       ecode
                                                                                                                                       a precise summary of the function without asking for its definition,    at  risk   of  being
     }}complex function. It perceives the variable pages[j] being used
                                                                                                                                    uninitialized,
                                                                                                                                     uninitialized,        i.e.,
                                                                                                                                                            i.e., if
                                                                                                                                                                  if  pdu_read()
                                                                                                                                                                       pdu_read()      returns
                                                                                                                                                                                        returns
                                                                                                                                       it does request the function definition of p9pdu_readf(), asnon-zero
                                                                                                                                                                                                   non-zero     in
                                                                                                                                                                                                                in  line
                                                                                                                                                                                                                    line  19
                                                                                                                                                                                                                           19  (thus
                                                                                                                                                                                                                               (thusit is
       inAsAsa loop
                 we
                 we can  that
                       can   see,iterates
                              see,    GPT-4from
                                     GPT-4        exhibits
                                                  exhibits 0 to    res-1. This
                                                               impressive
                                                                impressive               insight leadsof
                                                                                  comprehension
                                                                                   comprehension               ofGPT-
                                                                                                                   this
                                                                                                                   this             “break”      early).
                                                                                                                                    “break”       early). Notably,
                                                                                                                                       not as ubiquitous     Notably,      unlike   sscanf(), where
                                                                                                                                                                           unlike sscanf(),
                                                                                                                                                                   as sscanf().                    where GPT-4
                                                                                                                                                                                                           GPT-4 can  can provide
                                                                                                                                                                                                                            provide
       4  to
     complex    correctly
      complex function.         deduce
                       function. It            that
                                         It perceives  all
                                             perceives the    elements
                                                              the variable    in   the
                                                                                    pages[j] being
                                                                     variable pages[j]     pages       array
                                                                                                       being used must
                                                                                                                  used              aa precise      summary         of
                                                                                                                                         precise     summaryour
                                                                                                                                           Furthermore,              of the
                                                                                                                                                                         the functionnotwithout
                                                                                                                                                                              function
                                                                                                                                                                         solution        without     asking
                                                                                                                                                                                                      asking for
                                                                                                                                                                                           only produces        theits
                                                                                                                                                                                                              for       de�nition,
                                                                                                                                                                                                                    itscorrect
                                                                                                                                                                                                                        de�nition, out-
     inbeaainitialized,
      in       loop
                loop thatthat i.e.,    they from
                                iterates
                                iterates         are must_init.
                                                 from     00 to
                                                              to res-1.    ThisThis
                                                                               This  example
                                                                                        insightunderscores
                                                                                        insight        leads
                                                                                                       leads GPT-GPT-               ititcome
                                                                                                                                         does    request
                                                                                                                                          doesfor     this particular case but also pinpoints that ecodeas
                                                                                                                                                  request      the
                                                                                                                                                               the   function
                                                                                                                                                                     function     de�nition
                                                                                                                                                                                  de�nition      of
                                                                                                                                                                                                 of                              itit is
                                                                                                                                                                                                                             ascould  is
                                                                   res-1.                                                                                                                            p9pdu_readf(),
                                                                                                                                                                                                     p9pdu_readf(),
     44GPT-4’s
         to
         to correctly proficiency
                correctly       deduceinthat
                               deduce           handling
                                               that   all        loop andin
                                                       all elements
                                                             elements        ineven
                                                                                 the      index
                                                                                          pagessensitivity.
                                                                                  the pages           array
                                                                                                      array must must               not
                                                                                                                                     not    as
                                                                                                                                             as ubiquitous
                                                                                                                                                 ubiquitous       as
                                                                                                                                                                   as  sscanf().
                                                                                                                                                                        sscanf().
                                                                                                                                       be initialized when p9pdu_readf() returns 0, demonstrating the
     be
      be   initialized,
            initialized, i.e.,
       Concurrency               and  they
                                      they     are
                                                are must_init.
                                           Callback.          ConsiderThis   the example
                                                                          This      example
                                                                                    case illustratedunderscores
                                                                                                     underscoresin Fig-                   Furthermore,
                                                                                                                                                    of LLiftour   for solution
                                                                                                                                                                         solution not     only    produces    theas correct
                                                                                                                                                                                                                      follows:out-
                               i.e.,                  must_init.                                                                          Furthermore,           our                not   onlyThe produces     the    correct    out-
                                                                                                                                       efficacy                         unfamiliar    cases.          result is
     GPT-4’s
       ure 8. Atpro�ciency
      GPT-4’s         pro�ciency
                        first glance,      in  handling
                                           in UBITect
                                               handlingflags   loop    and
                                                                loopLineand even
                                                                               even
                                                                                10 for  index
                                                                                         index      sensitivity.
                                                                                                    sensitivity.
                                                                                             potentially         using              come
                                                                                                                                     come for   for this
                                                                                                                                                      this particular
                                                                                                                                                            particular case case but
                                                                                                                                                                                   but also
                                                                                                                                                                                         also pinpoints
                                                                                                                                                                                                pinpoints that       ecode could
                                                                                                                                                                                                             that ecode       could
       the variable comp_pkt.completion_status
     Concurrency
      Concurrency               and       Callback. Consider
                                and Callback.                Consider the   the case   before
                                                                                    case            initialization.
                                                                                            illustrated
                                                                                             illustrated       in
                                                                                                               in Fig-
                                                                                                                    Fig-            be
                                                                                                                                     be{ initialized when p9pdu_readf() returns 0, demonstrating the
                                                                                                                                           initialized      when p9pdu_readf() returns 0, demonstrating the
                                                                                                                                            "initializer":
       The7.
     ure
      ure     7.function’s
                  At
                  At �rst
                       �rst glance,body seemingly
                               glance,        UBITect
                                              UBITect �ags       lacks
                                                              �ags    Lineany
                                                                       Line    10code
                                                                               10   for      that initializes
                                                                                     for potentially
                                                                                            potentially         using
                                                                                                                using  it,          e�cacy
                                                                                                                                     e�cacy"err    of
                                                                                                                                                   of LL���
                                                                                                                                                        LL���    for
                                                                                                                                                                 for unfamiliar
                                                                                                                                                                        unfamiliar cases.
                                                                                                                                                         = p9pdu_readf(req->rc,       cases.   The
                                                                                                                                                                                                The result
                                                                                                                                                                                                      result is
                                                                                                                                                                                         c->proto_version,   is as
                                                                                                                                                                                                                 as follow:
                                                                                                                                                                                                                 'd',follow:
                                                                                                                                                                                                                        &ecode)",
       leading
     the
      the variable   UBITect        to    report     it  as
                            comp_pkt.completion_status before
              variable comp_pkt.completion_status             a  potential      bug.      However,         the
                                                                                      before initialization.
                                                                                                   initialization.mys-                  {{     "suspicious": ["ecode"],
                                                                                                                                                initializer
                                                                                                                                                 initializer ::
       teryfunction’s
     The
      The        unravels when
               function’s        body        we
                                  body seemingly   examine
                                             seemingly         lacks     any
                                                                         any codecode that
                                                                   hv_pci_generic_compl(),
                                                                lacks                                initializesthe
                                                                                            that initializes          it,
                                                                                                                      it,
                                                                                                                                               "postconstraint":
                                                                                                                                                     err
                                                                                                                                                                        null,
                                                                                                                                                     err == p9pdu_readf(req->rc,
                                                                                                                                                             p9pdu_readf(req->rc,       c->proto_version,
                                                                                                                                                                                        c->proto_version, dd ,, &ecode)
                                                                                                                                                                                                                &ecode) ,,
                                                                                                                                               "response":     {
       actual initializer
     leading
      leading       UBITect
                    UBITect to       function
                                    to   report ititassigned
                                         report        as             to pktbug.
                                                        as aa potential
                                                                potential         in Line
                                                                                bug.    However,4. Thethe
                                                                                         However,           variable
                                                                                                           the   mys-
                                                                                                                  mys-
                                                                                                                                                suspicious
                                                                                                                                                 suspicious :: [[ ecode
                                                                                                                                                    "must_init":
                                                                                                                                                                      ecode ],
                                                                                                                                                                       [],
                                                                                                                                                                             ],
                                                                                                                                                postconstraint
                                                                                                                                                 postconstraint :: null, null,
       in question
     tery
      tery      unravelsiswhen
               unravels           indeed
                               when         weinitialized,
                                            we    examine           but intriguingly, its initializer
                                                   examine hv_pci_generic_compl(),
                                                                   hv_pci_generic_compl(),                          the
                                                                                                                    the                             "may_init":
                                                                                                                                                response
                                                                                                                                                 response  :: {{ [{
                                                                                                                                                     must_init
       emerges
     actual
      actual initializerfrom     a    concurrent
                   initializer function
                                     function assigned      function
                                                     assigned to     to pktinstead
                                                                         pkt    in
                                                                                 in Line
                                                                                      Lineof 4. within
                                                                                                4. The       its own
                                                                                                    The variable
                                                                                                           variable                                  may_init
                                                                                                                                                     may_init
                                                                                                                                                             "name":
                                                                                                                                                     must_init      :: [],
                                                                                                                                                                  :: [{
                                                                                                                                                                       [],
                                                                                                                                                                      [{
                                                                                                                                                             "condition":
                                                                                                                                                                          "ecode",
                                                                                                                                                                               "p9pdu_readf returns 0"
     inthread.
      in   question
            questionHereis      indeed
                                 indeed initialized,
                                                initialized, but
                            iswait_for_completion()                        is a synchronization
                                                                    but intriguingly,
                                                                          intriguingly,           its           primi-
                                                                                                   its initializer
                                                                                                         initializer                                }]          name
                                                                                                                                                                 name   ::  ecode
                                                                                                                                                                            ecode ,,
                                                                                                                                                                condition
                                                                                                                                                                 condition :: p9pdu_readf
                                                                                                                                                                                  p9pdu_readf returns
                                                                                                                                                                                              returns 00
       tive that pauses
     emerges
      emerges          from aathe
                      from                current thread
                                    concurrent
                                     concurrent            function
                                                           functionand waits
                                                                         instead
                                                                          instead  for ofthewithin
                                                                                         of     new thread
                                                                                               within      its
                                                                                                            its own (i.e.,
                                                                                                                  own
                                                                                                                                               } }] }]
                                                                                                                                         }
     thread.
      thread. Here          wait_for_completion() is
       hv_pci_generic_compl())
                    Here wait_for_completion()           to   complete.        Despite
                                                                          is aa synchronizationthis    complexity,
                                                                                  synchronization primi-        primi-                  }}
                                                                                                                                              }}

       GPT-4
     tive
      tive    thatadeptly
              that   pauses
                      pauses the  navigates
                                  the    currentthe
                                         current     thread
                                                      threadconcurrency
                                                                  and
                                                                  and waits
                                                                         waits forand
                                                                                   for the
                                                                                        thecallback
                                                                                               new
                                                                                                new threadhandling,
                                                                                                        thread     (i.e.,
                                                                                                                   (i.e.,               6.7 Reason
                                                                                                                                        6.8 Reason for
                                                                                                                                                    for Imprecision
                                                                                                                                                         Imprecision
       pinpointing the accurate initializer
     hv_pci_generic_compl())
      hv_pci_generic_compl())                           to
                                                         to complete.and outputting
                                                             complete.        Despite
                                                                               Despite this     a precise
                                                                                              this              result.
                                                                                                      complexity,
                                                                                                      complexity,
            It isadeptly
                    worth noting             thatthewe concurrency
                                                           do   not encodeand       anycallback
                                                                                             knowledge           about                   DespiteLL���
                                                                                                                                        Despite
                                                                                                                                        Despite    LLiftachieving
                                                                                                                                                  LL���    achievingaaaprecision
                                                                                                                                                           achieving        precisionof
                                                                                                                                                                            precision      of50%
                                                                                                                                                                                          of   50%in
                                                                                                                                                                                              50%      inreal-world
                                                                                                                                                                                                      in  real-worldapplica-
                                                                                                                                                                                                          real-world      applica-
                                                                                                                                                                                                                         applica-
     GPT-4
      GPT-4        adeptly      navigates
                                 navigates          the     concurrency          and      callback       handling,
                                                                                                          handling,
       the      Linux      kernel          synchronization               primitives.           LLift       prompts                       tions,the
                                                                                                                                        tions,
                                                                                                                                        tions,  theprecision
                                                                                                                                                the precisioncan
                                                                                                                                                    precision    canstill
                                                                                                                                                                can   stillbe
                                                                                                                                                                      still  beimproved
                                                                                                                                                                            be    improvedin
                                                                                                                                                                                 improved       inthe
                                                                                                                                                                                               in   thefuture.
                                                                                                                                                                                                   the    future.Some
                                                                                                                                                                                                         future.   Somecan
                                                                                                                                                                                                                   Some     canbe
                                                                                                                                                                                                                           can   be
                                                                                                                                                                                                                                be
     pinpointing
      pinpointing the      the accurate
                                   accurate initializer
                                                   initializer and  and outputting
                                                                           outputting aa precise  precise result.
                                                                                                                result.
       LLMs         with “The           ‘initializer’                                                                                    solved
                                                                                                                                        solved   with
                                                                                                                                        solved with    better
                                                                                                                                                 with better   prompts
                                                                                                                                                      better prompts
                                                                                                                                                               prompts or   or  better
                                                                                                                                                                           or better     integration
                                                                                                                                                                                better integration
                                                                                                                                                                                        integration with   with static
                                                                                                                                                                                                          with static    analysis.
                                                                                                                                                                                                                static analysis.
                                                                                                                                                                                                                         analysis.
          ItIt is
                is worth
                   worth      noting
                              noting        that
                                            that we we do  domust
                                                               not     be the any
                                                               not encode
                                                                      encode        ‘actual’
                                                                                   any             functionabout
                                                                                           knowledge
                                                                                            knowledge              that
                                                                                                                about
       initializes
     the
      the      Linuxthe
               Linux           variable.
                           kernel
                           kernel             ” and then LLMs
                                          synchronization
                                          synchronization                   can automatically
                                                                        primitives.
                                                                        primitives.           LL���
                                                                                               LL��� prompts identify
                                                                                                           prompts                       Challengesin
                                                                                                                                        Challenges
                                                                                                                                        Challenges      inConstraint
                                                                                                                                                        in  ConstraintExtraction.
                                                                                                                                                            Constraint        Extraction.Beyond
                                                                                                                                                                             Extraction.         Beyondthe
                                                                                                                                                                                                 Beyond      thefour
                                                                                                                                                                                                             the  fourprimary
                                                                                                                                                                                                                  four    primary
                                                                                                                                                                                                                         primary
       the function
     LLMs
      LLMs        with
                   with “The“The hv_pci_generic_compl()
                                      ‘initializer’
                                       ‘initializer’ must    must be  be the        as the function
                                                                           the ‘actual’
                                                                                   ‘actual’        initializerthat
                                                                                                  function        that of                codepatterns
                                                                                                                                        code
                                                                                                                                        code   patternswe
                                                                                                                                               patterns    weaddressed
                                                                                                                                                          we   addressedin
                                                                                                                                                              addressed       in§4.3,
                                                                                                                                                                             in   §4.3,there
                                                                                                                                                                                  §4.3,  thereexist
                                                                                                                                                                                        there     existadditional
                                                                                                                                                                                                 exist    additionalforms
                                                                                                                                                                                                          additional     formsof
                                                                                                                                                                                                                        forms    of
                                                                                                                                                                                                                                 of
                              variable.”” and
       comp_pkt.completion_status.
     initializes
      initializes the    the variable.           and then
                                                        then LLMs LLMs can can automatically
                                                                                   automatically identify   identify                     post-constraints.
                                                                                                                                        post-constraints.
                                                                                                                                        post-constraints. For For  instance,
                                                                                                                                                             For instance,       during
                                                                                                                                                                  instance, during         error
                                                                                                                                                                                 during error      handling,
                                                                                                                                                                                          error handling,
                                                                                                                                                                                                   handling, the the   checks
                                                                                                                                                                                                                the checks
                                                                                                                                                                                                                      checks forfor
                                                                                                                                                                                                                               for
     the
      the      function
                function Function.
       Unfamiliar                                   As previously delineated
                                hv_pci_generic_compl()
                                hv_pci_generic_compl()                            as
                                                                                   as thethe in  initializer
                                                                                                  initializer
                                                                                                       §2.3, LLMs    of
                                                                                                                      of                 failuresmay
                                                                                                                                        failures
                                                                                                                                        failures  mayinvolve
                                                                                                                                                  may    involveanother
                                                                                                                                                        involve    anotherfunction
                                                                                                                                                                  another       functionor
                                                                                                                                                                                function    ormacro.
                                                                                                                                                                                            or   macro.This
                                                                                                                                                                                                 macro.     Thisproblem
                                                                                                                                                                                                            This   problemcan
                                                                                                                                                                                                                   problem     can
                                                                                                                                                                                                                              can
       possess the inherent ability to recognize the semantics (e.g., post-
     comp_pkt.completion_status.
      comp_pkt.completion_status.                                                                                                        beaddressed
                                                                                                                                        be
                                                                                                                                        be   addressedby
                                                                                                                                            addressed     byeither
                                                                                                                                                         by  eithermore
                                                                                                                                                             either   moreexamples
                                                                                                                                                                     more      examplesduring
                                                                                                                                                                               examples      duringprompts
                                                                                                                                                                                            during       prompts(in-context
                                                                                                                                                                                                         prompts     (in-context
                                                                                                                                                                                                                     (in-context
       conditions) Function.of   commonAs          functions        like                                                                 learning),or
                                                                                                                                        learning),
                                                                                                                                        learning),   orlightweight
                                                                                                                                                     or  lightweightprogram
                                                                                                                                                        lightweight      programanalysis
                                                                                                                                                                         program        analysis(e.g.,
                                                                                                                                                                                       analysis      (e.g.,path
                                                                                                                                                                                                     (e.g.,  pathexploration
                                                                                                                                                                                                            path    exploration
                                                                                                                                                                                                                    exploration
     Unfamiliar
      Unfamiliar            Function.            As  previously
                                                     previously         delineated
                                                                           sscanf().
                                                                        delineated          in However,
                                                                                           in   §2.3,    LLMssome
                                                                                                §2.3, LLMs        pos-
                                                                                                                   pos-
       argue      that    “the    LLM       simply      learns     everything         from      the   internet      and                  insymbolic
                                                                                                                                        in
                                                                                                                                        in  symbolicexecution
                                                                                                                                            symbolic   executionto
                                                                                                                                                       execution     tocollect
                                                                                                                                                                     to  collectthe
                                                                                                                                                                        collect     thepost-constraints).
                                                                                                                                                                                    the   post-constraints).
                                                                                                                                                                                         post-constraints).
     sess
      sess the inherent ability to recognize the semantics (e.g., postcon-
               the   inherent        ability      to  recognize         the   semantics          (e.g.,    postcon-
       acts merely
     ditions)
      ditions)      of     as a search
                     of common
                          common               engine”like
                                          functions
                                           functions         [6].sscanf().
                                                            like    This viewpoint
                                                                   sscanf().         However,
                                                                                      However, is challenged
                                                                                                        the
                                                                                                        the notion
                                                                                                              notion  by                 InformationGaps
                                                                                                                                        Information
                                                                                                                                        Information        Gapsin
                                                                                                                                                           Gaps    inUBITect.
                                                                                                                                                                  in   UBITect.For
                                                                                                                                                                       UBITect.       Forinstance,
                                                                                                                                                                                      For    instance,UBITect
                                                                                                                                                                                            instance,       UBITectdoes
                                                                                                                                                                                                           UBITect      doesnot
                                                                                                                                                                                                                        does   not
                                                                                                                                                                                                                              not
       the case
     that
      that      “the illustrated
               “the   LLM
                       LLM simply
                                simply    inlearns
                                              Figureeverything
                                              learns       9.
                                                         everything        from
                                                                            from the  the internet
                                                                                             internet and  and actsacts                  provide explicit
                                                                                                                                        provide
                                                                                                                                        provide    explicit �eld
                                                                                                                                                   explicit   field names
                                                                                                                                                              �eld   names within
                                                                                                                                                                    names        within aaa structure
                                                                                                                                                                                 within       structure when
                                                                                                                                                                                              structure       when aaa speci�c
                                                                                                                                                                                                             when         specific
                                                                                                                                                                                                                          speci�c
                                                                                                                             910
                                                                                                                              9
The Hitchhiker’s Guide to Program Analysis: A Journey with Large Language Models


field is in use. This information gap can result in LLift lacking                       Deploying on Open-sourced LLMs. The reproducibility of LLift
precision in its analysis. Additionally, UBITect only reports the                       could be potentially challenged, considering its dependency on
variable utilized, not necessarily the same variable passed to an                       GPT-4, a closed-source API subject to frequent updates. At the
initializer. For example, consider an uninitialized variable a passed                   time of writing, Meta introduced Llama 2, an open-source language
to an initializer, which is then assigned to variable b for usage. In                   model with capabilities rivaling GPT-3.5. Our initial assessments
such a scenario, LLift may fail to identify the initializer due to this                 suggest that Llama 2 can understand our instructions and appears
incomplete information correctly. These challenges, primarily due                       well-suited to support LLift. The open-source nature of Llama
to the interface design in UBITect, can be addressed with focused                       2 provides us with opportunities to deploy and refine the model
engineering efforts to enrich the output information from UBITect.                      further. We plan to leverage these prospects in future studies.
Variable Reuse. Varaible reuse is an interesting problem of LLM. In
general, LLM usually confuses different variables in different scopes
(e.g., different function calls). For example, if the suspicious variable               8   RELATED WORK
is ret and passed as a argument to its initializer (say, func(&ret))                    Techniques of Utilizing LLMs. Wang et al. [33] propose an em-
and there is another stack variable defined in func also called ret,                    bodied lifelong learning agent based on LLMs. Pallagani et al. [23]
LLM will confuse them. Explicitly prompting and teaching LLM                            explores the capabilities of LLMs for automated planning. Weng
to note the difference does not appear to work. One solution is to                      [35] summarizes recent work in building an autonomous agent
leverage a simple static analysis to normalize the source code to                       based on LLMs and proposes two important components for plan-
ensure each variable has a unique name.                                                 ning: Task Decomposition and Self-reflection, which are similar to
Indirect Call. As mentioned §4.4, LLift follows a simple but impre-                     the design of LLift. Beyond dividing tasks into small pieces, task
cise strategy to handle indirect calls. Theoretically, existing static                  decomposition techniques also include some universal strategies
analysis tools, such as MLTA [16], can give possible targets for in-                    such as Chain-of-thought [34] and Tree-of-thought [38]. The gen-
direct calls. However, each indirect call may have multiple possible                    eral strategy of self-reflection has been used in several flavors:
targets and dramatically increase the token usage. We leave the                         ReAct [39], Reflexion [29] and Chain of Hindsight [15]. Despite the
exploration of such an exhaustive strategy for future work. LLift                       similarity in name, self-reflection is fundamentally different from
may benefit from a more precise indirect call resolution.                               self-validation in LLift where the former focuses on using external
Additional Constraints. There are many variables whose values                           sources to provide feedback to their models. Huang et al. [10] let an
are determined outside of the function we analyze, e.g., precondi-                      LLM self-improve its reasoning without supervised data by asking
tions capturing constraints from the outer caller. Since our analysis                   the LLM to lay out different possible results.
is fundamentally under-constrained, this can lead LLift to incor-                       LLMs for Program Analysis. Ma et al. [17] and Sun et al. [30]
rectly determine a must_init case to be may_init. Mitigating this                       explore the capabilities of LLMs when performing various program
imprecision relies on further analysis to provide more information.                     analysis tasks such as control flow graph construction, call graph
                                                                                        analysis, and code summarization. They conclude that while LLMs
                                                                                        can comprehend basic code syntax, they are somewhat limited in
                                                                                        performing more sophisticated analyses such as pointer analysis
7    DISCUSSION AND FUTURE WORK
                                                                                        and code behavior summarization. In contrast to their findings, our
Post-Constraint Analysis. Our approach prioritizes post-                                research with LLift has yielded encouraging results. We conjecture
constraints over other constraints, such as preconditions. By                           that this might be due to several reasons: (1) benchmark selection,
focusing on the post-constraints, we enhance the precision and                          i.e., Linux kernel vs. others. (2) Prompt designs. (3) GPT-3.5 vs. GPT-
scalability significantly. Importantly, our utilization of large                        4.0 – prior work only evaluated the results using only GPT-3.5. Pei
language models in program analysis suggests strong abilities in                        et al. [26] use LLMs to reason about loop invariants with decent
summarizing complex function behaviors involving loops, a classic                       performance. In contrast, LLift leverages LLMs for a variety of
hurdle in program analysis.                                                             tasks (including program behavior summarization) and integrates
Better Integration with Static Analysis. Our work presents op-                          them successfully into a static analysis pipeline.
portunities for greater integration and synergy with static analysis                    LLMs for Software Engineering. Xia et al. [36] propose an au-
methods. Currently, our proposed solution operates largely inde-                        tomated conversation-driven program repair tool using ChatGPT,
pendently of the static analysis methods, taking only inputs from                       achieving nearly 50% success rate. Pearce et al. [25] examine zero-
static analysis initially. Looking into the future, we can consider                     shot vulnerability repair using LLMs and found promise in synthetic
integrating static analysis and LLMs in a holistic workflow. For                        and hand-crafted scenarios but faced challenges in real-world ex-
example, this could involve selectively utilizing LLM as an assistant                   amples. Chen et al. [5] teach LLMs to debug its own predicted
to overcome certain hurdles encountered by static analysis, e.g.,                       program to increase its correctness, but only performs on relatively
difficulty in scaling up the analysis or summarizing loop invari-                       simple programs. Lemieux et al. [14] leverages LLM to generate
ants. In turn, further static analysis based on these findings can                      tests for uncovered functions when the search-based approach got
provide insights to refine the queries to the LLM. This iterative                       coverage stalled. Feng and Chen [7] use LLM to replay Android
process could enable a more thorough and accurate analysis of                           bug automatedly. Recently, LangChain proposed LangSimith [13],
complex cases. We believe such a more integrated approach is a                          a LLM-powered platform for debugging, testing, and evaluating.
very promising future direction.                                                        These diverse applications underline the vast potential of LLMs in
                                                                                   11
                                                                                                                               Haonan Li, Yu Hao, Yizhuo Zhai, and Zhiyun Qian


software engineering. LLift complements these efforts by demon-                                    Schulman, Jacob Hilton, Fraser Kelton, Luke Miller, Maddie Simens, Amanda
strating the efficacy of LLMs in bug finding in the real world.                                    Askell, Peter Welinder, Paul Christiano, Jan Leike, and Ryan Lowe. 2022. Training
                                                                                                   language models to follow instructions with human feedback. http://arxiv.org/
                                                                                                   abs/2203.02155 arXiv:2203.02155 [cs].
9    CONCLUSION                                                                               [23] Vishal Pallagani, Bharath Muppasani, Keerthiram Murugesan, Francesca Rossi,
                                                                                                   Biplav Srivastava, Lior Horesh, Francesco Fabiano, and Andrea Loreggia. 2023.
This work presents a novel approach that utilizes LLMs to aid                                      Understanding the Capabilities of Large Language Models for Automated Plan-
static analysis using a completely automated agent. By carefully                                   ning. http://arxiv.org/abs/2305.16151 arXiv:2305.16151 [cs].
                                                                                              [24] Jihyeok Park, Hongki Lee, and Sukyoung Ryu. 2022. A Survey of Parametric
considering the scope and designing the interactions with LLMs,                                    Static Analysis. ACM Comput. Surv. 54, 7 (2022), 149:1–149:37. https://doi.org/
our solution has yielded promising results. We believe our effort                                  10.1145/3464457
                                                                                              [25] Hammond Pearce, Benjamin Tan, Baleegh Ahmad, Ramesh Karri, and Bren-
only scratched the surface of the vast design space, and hope our                                  dan Dolan-Gavitt. 2023. Examining Zero-Shot Vulnerability Repair with Large
work will inspire future research in this exciting direction.                                      Language Models. In 2023 IEEE Symposium on Security and Privacy (S&P). IEEE
                                                                                                   Computer Society, Los Alamitos, CA, USA. https://doi.org/10.1109/SP46215.20
                                                                                                   23.00001
REFERENCES                                                                                    [26] Kexin Pei, David Bieber, Kensen Shi, Charles Sutton, and Pengcheng Yin. 2023.
 [1] Toufique Ahmed, Kunal Suresh Pai, Premkumar Devanbu, and Earl T. Barr.                        Can Large Language Models Reason about Program Invariants?. In Proceedings
     2023. Improving Few-Shot Prompts with Relevant Static Analysis Products.                      of the 40th International Conference on Machine Learning.
     http://arxiv.org/abs/2304.06815 arXiv:2304.06815 [cs].                                   [27] Luke Salamone. 2021. What is Temperature in NLP? https://lukesalamone.git
 [2] Anthropic (2023). 2023. Claude 2. https://www.anthropic.com/index/claude-2                    hub.io/posts/what-is-temperature/ Section: posts.
 [3] Jiuhai Chen, Lichang Chen, Heng Huang, and Tianyi Zhou. 2023. When do you                [28] Jessica Shieh. 2023. Best practices for prompt engineering with OpenAI API
     need Chain-of-Thought Prompting for ChatGPT? http://arxiv.org/abs/2304.032                    | OpenAI Help Center. https://help.openai.com/en/articles/6654000-best-
     62 arXiv:2304.03262 [cs].                                                                     practices-for-prompt-engineering-with-openai-api
 [4] Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde                         [29] Noah Shinn, Federico Cassano, Beck Labash, Ashwin Gopinath, Karthik
     de Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph,                  Narasimhan, and Shunyu Yao. 2023. Reflexion: Language Agents with Ver-
     Greg Brockman, et al. 2021. Evaluating large language models trained on code.                 bal Reinforcement Learning. http://arxiv.org/abs/2303.11366 arXiv:2303.11366
     arXiv preprint arXiv:2107.03374 (2021).                                                       [cs].
 [5] Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou. 2023. Teaching              [30] Weisong Sun, Chunrong Fang, Yudu You, Yun Miao, Yi Liu, Yuekang Li, Gelei
     Large Language Models to Self-Debug. http://arxiv.org/abs/2304.05128                          Deng, Shenghan Huang, Yuchen Chen, Quanjun Zhang, Hanwei Qian, Yang Liu,
 [6] Ted Chiang. 2023. ChatGPT Is a Blurry JPEG of the Web. The New Yorker (Feb.                   and Zhenyu Chen. 2023. Automatic Code Summarization via ChatGPT: How
     2023). https://www.newyorker.com/tech/annals-of-technology/chatgpt-is-a-                      Far Are We? http://arxiv.org/abs/2305.12865 arXiv:2305.12865 [cs].
     blurry-jpeg-of-the-web Section: annals of artificial intelligence.                       [31] Haoye Tian, Weiqi Lu, Tsz On Li, Xunzhu Tang, Shing-Chi Cheung, Jacques
 [7] Sidong Feng and Chunyang Chen. 2023. Prompting Is All Your Need: Automated                    Klein, and Tegawendé F. Bissyandé. 2023. Is ChatGPT the Ultimate Programming
     Android Bug Replay with Large Language Models. https://doi.org/10.48550/arX                   Assistant – How far is it? http://arxiv.org/abs/2304.11938 arXiv:2304.11938 [cs].
     iv.2306.01987 arXiv:2306.01987 [cs].                                                     [32] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones,
 [8] Github. 2023. GitHub Copilot documentation. https://ghdocs-prod.azurewebsit                   Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. 2017. Attention is All
     es.net/_next/data/mHA_XfBBaMPyfcP0Q05C5/en/free-pro-team@latest/copi                          you Need. In Advances in Neural Information Processing Systems, Vol. 30. Curran
     lot.json?versionId=free-pro-team%40latest&productId=copilot                                   Associates, Inc.
 [9] Anjana Gosain and Ganga Sharma. 2015. Static Analysis: A Survey of Tech-                 [33] Guanzhi Wang, Yuqi Xie, Yunfan Jiang, Ajay Mandlekar, Chaowei Xiao, Yuke
     niques and Tools. In Intelligent Computing and Applications (Advances in Intelli-             Zhu, Linxi Fan, and Anima Anandkumar. 2023. Voyager: An Open-Ended Em-
     gent Systems and Computing), Durbadal Mandal, Rajib Kar, Swagatam Das, and                    bodied Agent with Large Language Models. http://arxiv.org/abs/2305.16291
     Bijaya Ketan Panigrahi (Eds.). Springer India, New Delhi, 581–591.                            arXiv:2305.16291 [cs].
[10] Jiaxin Huang, Shixiang Shane Gu, Le Hou, Yuexin Wu, Xuezhi Wang, Hongkun                 [34] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Brian Ichter, Fei
     Yu, and Jiawei Han. 2022. Large Language Models Can Self-Improve. http:                       Xia, Ed Chi, Quoc Le, and Denny Zhou. 2023. Chain-of-Thought Prompting
     //arxiv.org/abs/2210.11610 arXiv:2210.11610 [cs].                                             Elicits Reasoning in Large Language Models. http://arxiv.org/abs/2201.11903
[11] Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii,                arXiv:2201.11903 [cs].
     Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023. Survey of Hallucination             [35] Lilian Weng. 2023. LLM-powered Autonomous Agents. lilianweng.github.io (Jun
     in Natural Language Generation. Comput. Surveys 55, 12 (Dec. 2023), 1–38.                     2023). https://lilianweng.github.io/posts/2023-06-23-agent
     https://doi.org/10.1145/3571730                                                          [36] Chunqiu Steven Xia and Lingming Zhang. 2023. Keep the Conversation Going:
[12] Jack Krawczyk and Amarnag Subramanya. 2023. Bard’s latest update: more                        Fixing 162 out of 337 bugs for $0.42 each using ChatGPT. http://arxiv.org/abs/
     features, languages and countries. https://blog.google/products/bard/google-                  2304.00385
     bard-new-features-update-july-2023/                                                      [37] Frank F. Xu, Uri Alon, Graham Neubig, and Vincent Josua Hellendoorn. 2022. A
[13] LangChain (2023). 2023. Announcing LangSmith, a unified platform for de-                      systematic evaluation of large language models of code. In Proceedings of the 6th
     bugging, testing, evaluating, and monitoring your LLM applications. https:                    ACM SIGPLAN International Symposium on Machine Programming. ACM, San
     //blog.langchain.dev/announcing-langsmith/                                                    Diego CA USA, 1–10. https://doi.org/10.1145/3520312.3534862
[14] Caroline Lemieux, Jeevana Priya Inala, Shuvendu K Lahiri, and Siddhartha Sen.            [38] Shunyu Yao, Dian Yu, Jeffrey Zhao, Izhak Shafran, Thomas L. Griffiths, Yuan Cao,
     2023. CODAMOSA: Escaping Coverage Plateaus in Test Generation with Pre-                       and Karthik Narasimhan. 2023. Tree of Thoughts: Deliberate Problem Solving
     trained Large Language Models. (2023).                                                        with Large Language Models. http://arxiv.org/abs/2305.10601 arXiv:2305.10601
[15] Hao Liu, Carmelo Sferrazza, and Pieter Abbeel. 2023. Chain of Hindsight                       [cs].
     Aligns Language Models with Feedback. http://arxiv.org/abs/2302.02676                    [39] Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik Narasimhan,
     arXiv:2302.02676 [cs].                                                                        and Yuan Cao. 2023. ReAct: Synergizing Reasoning and Acting in Language
[16] Kangjie Lu and Hong Hu. 2019. Where Does It Go?: Refining Indirect-Call                       Models. International Conference on Learning Representations (ICLR) (2023).
     Targets with Multi-Layer Type Analysis. In Proceedings of the 2019 ACM SIGSAC            [40] Yizhuo Zhai, Yu Hao, Hang Zhang, Daimeng Wang, Chengyu Song, Zhiyun Qian,
     Conference on Computer and Communications Security. ACM, London United                        Mohsen Lesani, Srikanth V. Krishnamurthy, and Paul Yu. 2020. UBITect: A Precise
     Kingdom. https://doi.org/10.1145/3319535.3354244                                              and Scalable Method to Detect Use-before-Initialization Bugs in Linux Kernel.
[17] Wei Ma, Shangqing Liu, Wenhan Wang, Qiang Hu, Ye Liu, Cen Zhang, Liming                       In Proceedings of the 28th ACM Joint Meeting on European Software Engineering
     Nie, and Yang Liu. 2023. The Scope of ChatGPT in Software Engineering: A                      Conference and Symposium on the Foundations of Software Engineering (ESEC/FSE
     Thorough Investigation. http://arxiv.org/abs/2305.12138 arXiv:2305.12138 [cs].                2020).
[18] Bertrand Meyer. 1997. Object-Oriented Software Construction, 2nd Edition.                [41] Wayne Xin Zhao, Kun Zhou, Junyi Li, Tianyi Tang, Xiaolei Wang, Yupeng Hou,
     Prentice-Hall.                                                                                Yingqian Min, Beichen Zhang, Junjie Zhang, Zican Dong, Yifan Du, Chen Yang,
[19] OpenAI (2022). 2022. Introducing ChatGPT. https://openai.com/blog/chatgpt                     Yushuo Chen, Zhipeng Chen, Jinhao Jiang, Ruiyang Ren, Yifan Li, Xinyu Tang,
[20] OpenAI (2023). 2023. Function calling and other API updates. https://openai.c                 Zikang Liu, Peiyu Liu, Jian-Yun Nie, and Ji-Rong Wen. 2023. A Survey of Large
     om/blog/function-calling-and-other-api-updates                                                Language Models. arXiv:2303.18223 [cs.CL]
[21] OpenAI (2023). 2023. GPT-4 Technical Report. http://arxiv.org/abs/2303.08774             [42] Shen Zheng, Jie Huang, and Kevin Chen-Chuan Chang. 2023. Why Does ChatGPT
     arXiv:2303.08774 [cs].                                                                        Fall Short in Providing Truthful Answers? http://arxiv.org/abs/2304.10513
[22] Long Ouyang, Jeff Wu, Xu Jiang, Diogo Almeida, Carroll L. Wainwright, Pamela                  arXiv:2304.10513 [cs].
     Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, John
                                                                                         12
