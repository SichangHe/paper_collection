                                                                               Estimating verification time

                                                                                     Pablo González de Aledo
                                                                                     Universidad de Cantabria
arXiv:1402.6478v1 [cs.SE] 26 Feb 2014




                                           This essay is divided in four parts: In section (I) I ex-   method to derive execution time directly from the high-
                                        plain why I think detecting hot-spots in verification is       level description of the function under test.
                                        complicated and in particular, more complicated than de-          Also, in the particular case of verification, the function
                                        tection when developing crude software. In section (II) I      parameters, the structure of the code or the algorithmic
                                        introduce the factors I think mostly affect performance        complexity does not directly affect performance, but in-
                                        in verification. In section (III) I propose a method to        stead, affect it through hidden parameters like path diver-
                                        find functions that are most promising to be optimized.        sity and query complexity (Figure 1). The challenge in
                                        Finally, in section (IV) I draw some conclusions and dis-      this case is therefore twofold; first, we have to describe
                                        cuss pros/cons of the proposed solution.                       the effect of visible characteristics of the code into these
                                                                                                       hidden parameters and then, the effect of intermediate
                                        1     Why detecting hot spots in verification is               factors into performance.
                                              difficult
                                        A generic framework for automated program verifica-
                                                                                                       2     What affects performance in verification
                                        tion through symbolic execution comprises the following
                                        steps:                                                         Performance of symbolic execution is dominated by the
                                                                                                       following factors (in order of importance):
                                            1. The code is parsed and transformed into an interme-
                                               diate representation for instrumentation.                   • Paths to explore (path diversity), greatly affected by
                                                                                                             the number of loops with variable number of itera-
                                            2. This intermediate code is instrumented for verifica-          tions.
                                               tion and compiled again to make it executable.
                                                                                                           • Complexity of branch-conditions that are symbolic;
                                            3. While running, the program forks on every branch
                                                                                                             number of variables, depth and kind of query (linear
                                               instruction, and calls a solver that decides which
                                                                                                             or not).
                                               branches can be executed.

                                            4. The annotated code and the solver run over an op-           • Memory accesses.
                                               erating system, which schedules the different seg-
                                               ments of code, commonly over an SMP processor,              • Arithmetic operations.
                                               but sometimes over a distributed set of processing
                                               nodes, each of them with its own memory, sched-            When considering how particular factors affect veri-
                                               uler, branch-prediction and memory management           fication time, we have to take account of the compiler
                                               directives...                                           transformations, and measure the above factors over op-
                                                                                                       timized code. Among the things that the compiler can do
                                          Many of these transformations and processes –                to make code more amenable for verification, are : al-
                                        particularly the transformations of step ¬, the forking        gebraic simplifications, removal of redundant operations
                                        scheme and the constraint solver of step ®– are guided         and constant propagation; loop unrolling; discard CPU-
                                        by heuristics that have been tuned and optimized during        specific optimizations; aggressively inline functions...
                                        years, so it is impossible in practice to obtain a formal      ([1])
                           Figure 1: Hot-spot finding when programming and when verifying.


3     A method to find functions that are more                    • Estimating the contribution of each parameter to the
      promising to be optimized.                                    verification time.
                                                                  • Isolating errors inherent to measures.
As explained in the previous sections, it is difficult and
probably undecidable to derive verification time from a           • Obtaining confidence intervals for inputs and out-
set of factors that can be observed in the code. This is            puts.
why the best way to confront the problem is a macro-
                                                                  • Validating the model.
modelling approach [2]. In macro-modelling, we map a
piece of code to a model that relates some output depen-           In order to enable human intervention to help auto-
dent of this code with various parameters that can be ob-       mated methods, I have divided the methodology in 5
tained, observed or calculated easily from the high-level       stages:
description. Important aspects of this technique are the
selection of the formula (linear or non-linear), the selec-     3.1    Parameter identification
tion of input parameters, and the fitting process.
   In particular, I will follow a white-box analysis and        In the first step, we identify the essential set of factors
black-box measurement philosophy.                               that may be correlated with performance. This is ar-
                                                                guably the most difficult step in the process and the one
    • White-box analysis means that we have access to           that most affects both the accuracy and practicality of the
      the variables that affect verification time, we can       approach. In general, any field nested in the input struc-
      modify them with little constraints and devise ex-        tures of the function and any local variable inside the
      periments that illustrate the effects of these changes.   function under study can affect verification time. How-
                                                                ever, the number of fields in structures passed to stdlib
    • Black-box measurement means that we measure               functions generates a lot of potential parameter candi-
      the verification time at the end of the previously        dates, even for simple functions, and the design space
      commented chain, when all the transformation and          of all those variables is too big to be exhaustively ana-
      heuristics are considered. Black-box measurement          lyzed. Therefore, a good automated tool must include a
      enable the time models to be estimated with little        step to characterize which of these parameters are truly
      knowledge of the steps involved in optimization and       relevant for the problem, and which can be omitted. In
      constraints solving.                                      some cases, human insight can help selecting those pa-
                                                                rameters, but the effort of manually performing this task
  Challenges in the practical application of this ap-           often hinders the application of these methods in prac-
proach include:                                                 tice, so in order to keep the method practical, human
                                                                intervention should be allowed but reduced as much as
    • Identifying the parameters and the template func-         possible.
      tion of the macro-model will require significant             I have chosen the following parameters as candidates
      manual effort. To choose a correct set of parameters      for the next step:
      and still keep generality to handle the wide range of
      behaviors of C-standard library is quite challenging.      1. Cyclomatic complexity of the function.
                                                                 2. An array indicating for each symbolic loop inside
    • Designing a proper set of experiments to measure              the function, how many instructions are inside this
      the effect of parameters into verification perfor-            loop.
      mance.
                                                                 3. An array indicating for each symbolic branch inside
    • Developing an accurate model that relates verifica-           the function, if the query that is evaluated is linear
      tion performance with the code and input data.                or not.
 4. An array indicating for each parameter, if it is sym-      3.3     Macro-model fitting
    bolic or constant.
                                                               In the forth step, collected data are used to fit a macro-
                                                               model of the functions: once the instrumented source-
 5. The sizes of all arrays passed to the function, either     code has been run and data have been obtained from the
    directly, or through the use of pointers. This size        experiments, we can fit the model to the data. There ex-
    is particularly difficult to be obtained during run-       ists two main approaches for macro-model fitting: linear
    time, as array boundaries are not maintained when          models can be easily fitted by least squares, but do not
    an array is passed to a function. Serialization can be     effectively capture complex inter-dependences between
    used to obtain a sequential description of the array       parameters. Symbolic regression [2] relaxes the restric-
    [2], but requires manual annotation of the code. An-       tion of a linear model and therefore can construct general
    other option is to omit size of arrays in the approach,    models for functions with highly related parameter de-
    under the empirical observation that most functions        pendencies. However, it commonly uses a hill-climbing
    of the standard library use a separate parameter to        or genetic algorithm which can fall in local-optima, ob-
    identify this size.                                        taining sub-optimal models.

 6. The value of all scalar values passed to the function.
                                                               3.4     Accuracy assessment
   The objective of choosing this set of factors is to ap-     The last step of the methodology is to assess the accuracy
proximate the effect of code structure and function pa-        of the model: once we have obtained the macro-model it
rameters in path diversity and query complexity. The           is important to evaluate the error it produces. This er-
benefit of choosing them is that ¬ and ­ can be obtained       ror provides a confidence interval of the predicted value
statically from the code, and the others does only need        when the model is used in subsequent estimations. Even
a light instrumentation. We still need to call a solver to     when this confidence interval is statistical and does not
measure the verification time (step 2), but the use of tech-   consider corner-cases, it can be of practical use to justify
niques from experimental design can reduce the number          the applicability of the model. ”Experimental Design”
of measures we need to perform.                                also explains how to estimate the error of the model. We
                                                               must take special care of making the set of experiments
                                                               used to assess the model different than the one used to fit
3.2    Experimental design and data collec-                    the data.
       tion
Second step of the methodology is concerned with ob-
                                                               4     Conclusions
taining the data needed to fit the macro-model for the ver-
                                                               I have presented a possible method to estimate verifica-
ification time. When a minimum or close-to-minimum
                                                               tion time of functions in the C standard library that can
set of parameters have been identified, we need to define
                                                               be used to detect which of them are responsible for a
characterization experiments in order to isolate the ef-
                                                               large time in the programs we verify. The benefits of the
fects of variables obtained in step 1 in verification time.
                                                               approach are:
”Experimental design” is a vast field that can not be eas-
ily described in this essay (and that have been largely
                                                                   • It considers many of the heuristics involved in pro-
ignored by software developers). Although references
                                                                     gram transformation and verification.
are very old, and are hard to fully automate, [3] and [4]
explain ways to obtain the maximum amount of informa-              • Once the method is developed, adapting it to new
tion about performance running the minimum number of                 compilers and solvers is easy and straightforward.
experiments. The theory explained in these references
shows how to construct experiments able to estimate the            • Once the models are fitted, we do not need to actu-
effects of the different parameters on the verification time         ally verify the code under test, so estimating verifi-
as efficiently as possible.                                          cation time is fast.
   Once the experiments have been designed, we need to
instrument the code to obtain the data needed to fit the           • Statistical confidence intervals for the results can be
macro-models. In [2] authors propose a method drawn                  obtained.
from data-structure serialization as a novel technique to
perform data collection, which can be applied to the par-        The cons of the proposed approach are mostly related
ticular case of verification.                                  with the selection of input parameters to the model.
  • The use of dynamically created data structures and
    memory allocation complicates the identification of
    relevant macromodel parameters.
  • Manual selection of a function template to fit the
    macromodel often requires a profound understand-
    ing of the function, which may be very difficult in
    this scenario. Symbolic regression can help in this
    step, but some human intervention is still needed.

   Another important limitation of the method is that the
macro-model will only be applicable when the function
is called with parameters that follow the same statistical
distributions as the ones used to train the model, and this
depends on what we are interested in analysing. For ex-
ample, if we are just interested in obtaining a good cov-
erage for a function, we will not put much effort in train-
ing the model for particular corner-cases that are seldom
executed. On the other hand, in some scenarios of ver-
ification we are particularly interested in finding those
corner-cases, so the model will have poor accuracy for
these test-cases.

References
      [1] J.Wagner, V.Kuznetsov, G.Candea, “-OVERIFY: Optimiz-
          ing Programs for Fast Verification” HotOS’13 Proceedings
          of the 14th USENIX conference on Hot Topics in Operat-
          ing Systems
      [2] A. Muttreja, A. Raghunathan, S. Ravi, N. K. Jha, “Auto-
          mated Energy/Performance Macromodeling of Embedded
          Software” IEEE Transactions on Computer-Aided Design
          of Integrated Circuits and Systems, vol. 26, no. 3, March
          2007
      [3] R.Jain, “Art of Computer Systems Performance Analysis
          Techniques For Experimental Design”
      [4] M. Schatzoff, “Design of Experiments in Computer Perfor-
          mance” IBM Res.Develop.vol. 25 no. 6 November 1981
