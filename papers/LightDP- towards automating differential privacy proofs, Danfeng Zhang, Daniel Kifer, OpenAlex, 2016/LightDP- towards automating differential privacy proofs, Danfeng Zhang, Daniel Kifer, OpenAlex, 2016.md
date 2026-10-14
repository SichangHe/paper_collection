                                                   LightDP: Towards Automating Differential Privacy Proofs

                                                                                                                                   Danfeng Zhang                     Daniel Kifer
                                                                                                                         Department of Computer Science and Engineering
                                                                                                                                      Penn State University
                                                                                                                                University Park, PA United States
                                                                                                                                {zhang,dkifer@cse.psu.edu}
arXiv:1607.08228v3 [cs.PL] 9 Dec 2016




                                        Abstract                                                                                                                    of attackers to infer individual-level sensitive information (Dwork
                                        The growing popularity and adoption of differential privacy in                                                              et al. 2006b; Kifer and Machanavajjhala 2014).
                                        academic and industrial settings has resulted in the development                                                                Since 2006, differential privacy has seen explosive growth in
                                        of increasingly sophisticated algorithms for releasing information                                                          many areas, including theoretical computer science, databases, ma-
                                        while preserving privacy. Accompanying this phenomenon is the                                                               chine learning, and statistics. This technology has been deployed in
                                        natural rise in the development and publication of incorrect al-                                                            practice, starting with the U.S. Census Bureau LEHD OnTheMap
                                        gorithms, thus demonstrating the necessity of formal verification                                                           tool (Machanavajjhala et al. 2008), the Google Chrome Browser
                                        tools. However, existing formal methods for differential privacy                                                            (Erlingsson et al. 2014), and Apple’s new data collection efforts
                                        face a dilemma: methods based on customized logics can verify                                                               (Greenberg 2016). However, the increase in popularity and usage
                                        sophisticated algorithms but come with a steep learning curve and                                                           of differential privacy has also been accompanied by a correspond-
                                        significant annotation burden on the programmers, while existing                                                            ing increase in the development and implementation of algorithms
                                        programming platforms lack expressive power for some sophisti-                                                              with flawed proofs of privacy; for example, Chen and Machanava-
                                        cated algorithms.                                                                                                           jjhala (2015) and Lyu et al. (2016) catalog some recent cases about
                                            In this paper, we present LightDP, a simple imperative language                                                         variations of the Sparse Vector method (Dwork and Roth 2014) .
                                        that strikes a better balance between expressive power and usability.                                                           Currently, there are two strategies for combating this trend. The
                                        The core of LightDP is a novel relational type system that separates                                                        first is the use of programming platforms (McSherry 2009; Mohan
                                        relational reasoning from privacy budget calculations. With depen-                                                          et al. 2012; Roy et al. 2010) that have privacy primitives that restrict
                                        dent types, the type system is powerful enough to verify sophis-                                                            the privacy-preserving algorithms that can be implemented and of-
                                        ticated algorithms where the composition theorem falls short. In                                                            ten add more noise than is necessary to the computation. The sec-
                                        addition, the inference engine of LightDP infers most of the proof                                                          ond strategy is the development of languages and formal verifica-
                                        details, and even searches for the proof with minimal privacy cost                                                          tion tools for differential privacy (Reed and Pierce 2010; Gaboardi
                                        bound when multiple proofs exist. We show that LightDP verifies                                                             et al. 2013; Barthe et al. 2012, 2014, 2016c,b). These languages en-
                                        sophisticated algorithms with little manual effort.                                                                         able the development of much more sophisticated algorithms that
                                                                                                                                                                    use less noise and hence provide more accurate outputs. However,
                                        Categories and Subject Descriptors D.3.1 [Programming Lan-                                                                  the increased power of the formal methods comes with a consider-
                                        guages]: Formal Definitions and Theory; D.2.4 [Software En-                                                                 able cost — a programmer has to heavily annotate code and gener-
                                        gineering]: Software/Program Verification; F.3.1 [Logics and                                                                ate proofs using complicated logics such as a customized relational
                                        Meanings of Programs]: Specifying and Verifying and Reasoning                                                               Hoare logic proposed by Barthe et al. (2012). Moreover, intricate
                                        about Programs.                                                                                                             proof details have to be provided by a programmer, which makes
                                                                                                                                                                    exploring variations of an algorithm difficult since small variations
                                        Keywords Differential privacy; dependent types; type inference;                                                             in code can cause significant changes to a proof.
                                                                                                                                                                        In this paper, we present LightDP, a language for developing
                                        1.       Introduction                                                                                                       provably privacy-preserving algorithms. The goal of LightDP is to
                                                                                                                                                                    minimize the burden on the programmer while retaining most of
                                        Companies, government agencies, and academics are interested in                                                             the capabilities of the state-of-the-art, such as verifying the Sparse
                                        analyzing and modeling datasets containing sensitive information                                                            Vector method (Dwork and Roth 2014) (an algorithm which, until
                                        about individuals (e.g., medical records, customer behavior, etc.).                                                         very recently (Barthe et al. 2016c,b), was beyond the capabilities
                                        Privacy concerns can often be mitigated if the algorithms used to                                                           of verification tools). For example, we show that the Sparse Vector
                                        manipulate the data, answer queries, and build statistical models                                                           method can be verified in LightDP with little manual effort: just
                                        satisfy differential privacy (Dwork et al. 2006b) — a set of restric-                                                       two lines of annotation from the programmer.
                                        tions on their probabilistic behavior that provably limit the ability                                                           LightDP is equipped with a novel light-weight relational type
                                                                                                                                                                    system that clearly separates relational reasoning from privacy bud-
                                                                                                                                                                    get calculation. In particular, it transforms the original probabilis-
                                                                                                                                                                    tic program into an equivalent nonprobabilistic program, where all
                                        Permission to make digital or hard copies of part or all of this work for personal or classroom use is granted without      privacy costs become explicit. With dependent types, the explic-
                                        fee provided that copies are not made or distributed for profit or commercial advantage and that copies bear this notice
                                        and the full citation on the first page. Copyrights for components of this work owned by others than ACM must be
                                                                                                                                                                    itly calculated privacy cost in the target language may depend on
                                        honored. Abstracting with credit is permitted. To copy otherwise, to republish, to post on servers, or to redistribute to   program states, hence enabling the verification of sophisticated al-
                                        lists, requires prior specific permission and/or a fee. Request permissions from permissions@acm.org or Publications
                                        Dept., ACM, Inc., fax +1 (212) 869-0481.                                                                                    gorithms (e.g., the Sparse Vector method) that are beyond the capa-
                                        POPL ’17, January 18-20, 2017, Paris, France                                                                                bility of many existing methods (Reed and Pierce 2010; Gaboardi
                                        Copyright c 2017 ACM 978-1-4503-4660-3/17/01. . . $15.00
                                        DOI: http://dx.doi.org/10.1145/3009837.3009884                                                                              et al. 2013; Barthe et al. 2012, 2014) based on the composition the-
orem (McSherry 2009). Moreover, the transformed nonprobabilis-                 function S PARSE V ECTOR (T, N,  : num0 ; q : list num∗ )
tic program is ready for off-the-shelf formal verification methods,
such as Hoare logic, to provide an upper bound of the privacy cost.                      returns (out : list bool0 )
    On the usability end, LightDP has an inference engine that re-                       precondition ∀i. −1 ≤ (bq [i]) ≤ 1
duces the already low annotation burden on the programmers. Al-
                                                                               c1, c2, i : num0 ; T̃ , η1 : num1 ; η2 : numq[i]+η2 ≥T̃ ?2:0
though the inference engine does not yet automate the privacy bud-
get calculation part of a proof, it does fill in missing details in the re-   1     η1 := Lap (2/);
lational reasoning part of a proof; furthermore, based on MaxSMT              2     T̃ := T + η1 ;
theory, it even searches for the optimal proof that minimizes privacy         3     c1 := 0; c2 := 0; i := 0;
cost with minimal human involvement. For example, with only one               4     while (c1 < N )
postcondition annotation and one loop invariant annotation from a             5        η2 := Lap (4N/);
programmer, LightDP confirms that the proof in (Dwork and Roth                 6       if (q[i] + η2 ≥ T̃ ) then
2014) indeed provides the minimal privacy cost.                                7         out:= true::out;
    To summarize, this paper makes the following contributions:                8         c1 := c1 + 1;
                                                                               9       else
1. LightDP, a new imperative language for verifying sophisticated             10         out:= false::out;
   privacy-preserving algorithms (Section 3.1),                               11         c2 := c2 + 1;
                                                                              12       i := i+1;
2. expressive static annotations incorporating dependent types, en-
   abling precise tracking of privacy costs (Section 3.3),
                                                                              Figure 1. The Sparse Vector method. Type annotations are shown
3. a formal proof that the LightDP type system soundly tracks                 in grey. The precondition specifies the adjacency assumption.
   differential privacy costs, and new proof techniques involved
   in the soundness proof (Section 4),
4. an inference engine that automatically fills in missing details            Definition 1 (Differential privacy). Let , δ ≥ 0. A probabilistic
   involved in the relational reasoning part of a proof, and further,         computation M : A → Dist(B) is (, δ)-differentially private
   minimizes provable privacy cost bound when multiple proofs                 with respect to an adjacency relation Ψ ⊆ A × A if for every pair
   exist, with little manual effort (Section 5),                              of inputs a1 , a2 ∈ A such that a1 Ψa2 , and every output subset
                                                                              E ⊆ B, we have
5. case studies on complex algorithms showing that formal veri-
   fication of privacy-preserving algorithms are viable with little                        P (M a1 ∈ E) ≤ exp()P (M a2 ∈ E) + δ
   programmer annotation burden (Section 6).                                      Intuitively, a probabilistic computation satisfies differential pri-
                                                                              vacy if it produces similar distributions for any pair of inputs related
2.    Preliminaries and Illustrating Example                                  by Ψ. In the most common applications of differential privacy, A is
                                                                              the set of possible databases and the adjacency relation Ψ is chosen
2.1   Distributions                                                           so that a1 Ψa2 whenever a1 can be obtained from a2 by adding or
We define the set of sub-distributions over a discrete set A, writ-           removing data belonging to a single individual.
ten Dist(A), as the set of functions µ : A → [0, 1], such that
P                                                                                 In this paper, we focus on the verification of algorithms that sat-
   a∈A µ P a ≤ 1. When applied to an event E ⊆ A, we define                   isfy pure differential privacy. An algorithm is -differentially pri-
                                                                              vate iff it is (, 0)-differentially private according to Definition 1.
                                                      P
µ(E) , e∈E µ(e). Notice that we do not require a∈A µ a =
1, a special case when µ is a distribution, since sub-distribution
gives rise to an elegant semantics for programs that may not termi-           2.3    The Sparse Vector Method
nate (Kozen 1981).                                                            The goal of formal methods for verifying -differential privacy is
    Given a distribution µ ∈ Dist(A), its support is defined as               to provide an upper bound on the privacy cost  of a program.
support(µ) , {a | µ(a) > 0}. We use 1a to represent the                       Typically, users will have a fixed privacy budget 0 and can only
degenerate distribution µ that µ(a) = 1 and µ(a0 ) = 0 if a0 6= a.            run programs whose provable privacy cost  does not exceed the
Moreover, sub-distributions can be given a structure of a monad.              budget:  ≤ 0 . For this reason, it is important that formal methods
Formally, we define the unit and bind functions as follows:                   are able to prove a tight upper bound on the privacy cost.
                                                                                  With the exception of (Barthe et al. 2016c,b), most existing for-
        unit : A → Dist(A) , λa. 1a                                           mal methods rely on the composition theorem (McSherry 2009).
        bind : Dist(A) → (A → Dist(B)) → Dist(B)                              That is, in the case of -differential privacy, those methods essen-
                            X                                                 tially treat a program as a series of modules, each with a provable
             , λµ. λf. (λb.   (f a b) × µ(a))                                 upper bound i on its privacy cost. Then by the compositionP    theo-
                                 a∈A
                                                                              rem (McSherry 2009), the total privacy cost is bounded by i i .
That is, unit takes an element in A and returns the Dirac distribu-           However, for sophisticated advanced algorithms, the composition
tion where all mass is assigned to a; bind takes µ, a distribution            theorem often falls short — it can provide upper bounds that are
on A, and f , a mapping from A to distributions on B (e.g., a con-            arbitrarily larger than the true privacy cost. Providing the tightest
ditional distribution of B given A), and returns the corresponding            privacy cost for intricate algorithms requires formal methods that
marginal distribution on B. This monadic view will avoid cluttered            are more powerful but avoid over-burdening the programmers with
definitions and proofs when probabilistic programs are involved               annotation requirements. To illustrate these challenges, we con-
(Section 3.2).                                                                sider the Sparse Vector method (Dwork and Roth 2014). It is a
                                                                              prime example of the need for formal methods because many of
2.2   Differential Privacy                                                    its published variants have been shown to be incorrect (Chen and
Differential privacy has two major variants: pure (Dwork et al.               Machanavajjhala 2015; Lyu et al. 2016).
2006b) (obtained by setting δ = 0 in the following definition) and                The Sparse Vector method also has many correct variants, one
approximate (Dwork et al. 2006a) (obtained by choosing a δ > 0).              of which is shown in Figure 1. For now, safely ignore the type an-
                                                                              notations in grey and the precondition. Here, the input list q repre-
                                                                                                      (2)      (1)        (2)      (1)
sents a sequence of results of counting queries q1 , q2 , q3 , . . . (e.g.,   ported false (i.e., β0 = β0 and β1 = β1 ) and adds 2 to the
how many patients in the data have cancer, how many patients con-                                                                  (2)     (1)
                                                                              noise of queries for which D1 reported true (i.e., β2 = β2 +2).
tracted an infection in the hospital, etc.) running on a database. The           In our running example, execution under D2 with this function
goal is to answer as accurately as possible the following question:           would result in the noisy threshold T̃ = 6 and noise query answers
which queries, when evaluated on the true database, return an an-                       (2)                (2)                (2)
                                                                              q[0] + β0 = 5, q[1] + β1 = 3, q[2] + β2 = 6. Hence, the
swer greater than the threshold T (a program input unrelated to the
                                                                              output once again is (false, false, true). In fact, it is easy to see
sensitive data)?
                                                                              that under this injective function, every execution under D1 would
    To achieve differential privacy, the algorithm adds appropriate
                                                                              result in an execution under D2 that produces the same answer.
Laplace noise to the threshold and to each query. Here, Lap (4N/)
draws one sample from the Laplace distribution with mean zero                 Counting privacy cost For each output ω, let f be the injective
and a scale factor (4N/). If the noisy query answer (q[i] + η2 )             function; let A be the set of random variable assignments that
is above the noisy threshold T̃ , it adds true to the output list out         cause execution under D1 to produce ω; let B be the possible
(in the slot reserved for that query) and otherwise, it adds false.           assignments we can get by applying f to A; and let C be the
The key to this algorithm is the deep observation that once noise             set of random variable assignments that are not in the range of f ,
has been added to the threshold, queries for which we output true             but nevertheless cause execution under D2 to produce the output
have a privacy cost (so we can answer at most N of them, where                ω as well1 . Then we can rewrite P (M (D1 ) = ω) = P (A) and
N is a parameter); however, outputting false for a query does                 P (M (D2 ) = ω) = P (B) + P (C).
not introduce any new privacy costs (Dwork and Roth 2014). The                    Once we have done the alignment of randomness as above, and
algorithm ensures that the total privacy cost is bounded by the input         recalling that N = 1 in our example, the proof finishes by showing:
, the parameter used in Figure 1. This remarkable property makes                                 X                    X
the Sparse Vector method ideal in situations where the vast majority                      P (A) =      P (a) ≤ e 2 e2 4N      P (f (a))
of query counts are expected to be below the threshold.                                              a∈A                        a∈A

                                                                                                  = e P (B) ≤ e (P (B) + P (C))
Failure of the composition theorem If we just use the composi-
                                                                                            
tion theorem, we would have a privacy cost of /4N for each loop              where the e 2 factor results from using a threshold value that is 1
                                                                                                    
iteration (i.e., every time Lap (4N/) noise is added to a query              larger, while the e2 4N factor results from adding 2 to the noise for
answer) due to the property of the Laplace distribution. Since the            query q[2]. Notice that no privacy cost is paid for queries q[0] and
number of iterations are not a priori bounded, the composition the-           q[1], since the same noise is added
orem could not prove that the algorithm satisfies 0 -differential pri-                                         P under D1 and D2 . Moreover,
                                                                              due to the injective assumption, a∈A P (f (a)) = P (B).
vacy for any finite 0 ; more advanced methods are needed.
                                                                              Challenges The Sparse Vector method is a prime example of the
Informal proof and sample runthrough Proofs of correctness                    need for formal methods, since paper-and-pencil proof is shown
(of this and other variants) can be found in (Dwork and Roth                  to be error-prone for its variants. The intricacy in its proof brings
2014; Chen and Machanavajjhala 2015; Lyu et al. 2016). Here we                major challenges for formal methods:
provide an informal correctness argument by example to illustrate
the subtleties involved both in proving it and inferring a tight bound        1. Precision: a crucial observation in the proof is that once noise
for the algorithm.                                                               has been added to the threshold, different privacy costs are only
    Suppose we set the parameters T = 4 (we want to know which                   paid for outputting true. Hence, the cost calculation needs to
queries have a value at least 4) and N = 1 (we stop the algorithm                consider program states.
after the first time it outputs true). Consider the following two             2. Aligning randomness: finding an injective function from the
databases D1 , D2 that differ on one record, and their corresponding             randomness under D1 to that under D2 such that outputting ω
query answers:                                                                   under D1 entails outputting ω under D2 is the most intriguing
              D1 :     q[0] = 2,     q[1] = 3,    q[2] = 5                       piece in the proof. However, coming up with a correct function,
                                                                                 as we described informally above, is non-trivial.
              D2 :     q[0] = 3,     q[1] = 3,    q[2] = 4
                                                                              3. Finding the tightest bound: in fact, an infinite number of proofs
Suppose in one execution on D1 , the noise added to T is α(1) = 1                exist for the Sparse Vector method, though with various prov-
                                            (1)     (1)     (1)
and the noise added to q[0], q[1], q[2] is β0 = 2, β1 = 0, β2 =                  able privacy costs2 . Since a tighter privacy cost bound allows a
0, respectively. Thus the noisy threshold is T̃ = 5 and the noisy                privacy-preserving algorithm to produce more accurate outputs,
                           (1)                (1)
query answers are q[0]+β0 = 4, q[1]+β1 = 3, q[2]+β2 = 5
                                                          (1)                    a formal method should produce the tightest one when possible.
and so the algorithm outputs the sequence: (false, false, true).                  Except the very recent work by Barthe et al. (2016c,b), existing
    According to Definition 1, for any output sequence ω, we                  formal methods (e.g., (Reed and Pierce 2010; Gaboardi et al. 2013;
need to show P (M (D1 ) = ω) ≤ e P (M (D2 ) = ω) for                         Barthe et al. 2012, 2014)) rely on the composition theorem, hence
all possible outputs ω and databases D1 , D2 that differ on one               fail to prove that the Sparse Vector method satisfies 0 -privacy for
record. For the databases D1 , D2 described above, we will show               any 0 . Recent work by Barthe et al. (2016c,b) verifies variants of
that P (M (D1 ) = (false, false, true)) ≤ e P (M (D2 ) =                     the Sparse Vector method, but its customized relational logic in-
(false, false, true)). We proceed in two steps.                               curs heavy annotation burden, including the randomness alignment.
                                                                              Moreover, those work cannot search for the tightest cost bound.
Aligning randomness We first create an injective (but not neces-
sarily bijective) function from the randomness in the execution un-           1 This is possible since we do not assume the function to be a bijection.
der D1 into the randomness in the execution under D2 , so that both
                                                                              2 For example, another injective function adds 2 to the threshold noise (i.e.,
executions generate the same output. For an execution under D2 , let
                                                      (2)   (2)
α(2) be the noise added to the threshold and let β0 , β1 , β2 be
                                                                 (2)          α(2) = α(1) + 2), keeps the noise of queries for which D1 reported false
                                                                                      (2)  (1)       (2)      (1)
the noise added to the queries q[0], q[1], q[2], respectively. Consider       (i.e., β0 = β0 and β1 = β1 ) and adds 3 to the noise of queries for
                                                                                                                (2)      (1)
an injective function candidate that adds 1 to the threshold noise            which D1 reported true (i.e., β2 = β2 + 3). It is easy to check that
(i.e., α(2) = α(1) + 1), keeps the noise of queries for which D1 re-          this mapping has the desired property, but the privacy cost is (7)/4.
2.4   Our Approach                                                           function TS PARSE V EC (T, N,  : num; q : list num; qb : list num)
To tackle the challenges above, we propose LightDP, an imperative                     returns (out : list bool)
language that enables verification and even inference of the tightest                 precondition ∀i. −1 ≤ (b q [i]) ≤ 1
privacy cost for sophisticated privacy-preserving algorithms. We             1    v := 0;
illustrate the key components of LightDP in this section, and detail         2    havoc η1 ; v := v + /2;
all components in the rest of this paper.
                                                                             3    T̃ := T + η1 ;
Relational reasoning The core of LightDP is a novel light-weight             4    c1 := 0; c2 := 0; i := 0;
dependent type system that explicitly captures the exact differ-             5    while (c1 < N)
ence of a variable’s values in two executions under two adjacent                                                           
                                                                                     Invariant : c1 ≤ N ∧ v = /2 + c1 × 2N
databases. Let v (1) (v (2) ) be the value of a variable x in an exe-
                                                                             6      havoc η2 ; v := v + (q[i] + η2 ≥ T̃ ?2 : 0) × /4N ;
cution under D1 (D2 ). The type τ for x in LightDP has the form
of Bd , meaning that x holds a value of basic type B (e.g., int,             7      if (q[i] + η2 ≥ T̃ ) then
                                                                             8        out:= true::out;
real, bool), and v (1) + d = v (2) . Required type annotations for
                                                                             9        c1 := c1+1;
the Sparse Vector method are shown in grey in Figure 1. Note that           10      else
for brevity, we write num for numeric base types (e.g., int, real).         11        out:= false::out;
Hereafter, we refer to the d counterpart as the distance.                   12        c2 := c2+1;
    In the simplest case, the distance is a constant. For example, the      13      i := i+1;
input threshold T has a type num0 , meaning that its value remains
the same in two executions (since T is a parameter unrelated to             Figure 2. The transformed program. The instrumented statements
private information about individuals). The distance of variable η1         are underlined. The loop invariant to prove the postcondition v ≤
captures one randomness alignment in the informal proof above:               is shown in grey.
we enforce a distance of 1 for η1 (i.e., we map noise v to v + 1 for
any value v sampled in the execution under D1 ).
    The distance may also depend on program states. Hence,                      Notice that for the second property (the problem of bounding
LightDP supports dependent types. For instance, consider the dis-           v ), any off-the-shelf verification tool for functional correctness
tance of η2 : q[i] + η2 ≥ T̃ ?2 : 0. This annotation specifies an           can be utilized. For instance, the program above with the desired
injective function that maps noise v to v + 2 when the value of             postcondition v ≤  can be verified by Hoare logic, with one loop
q[i] + η2 ≥ T̃ is true (i.e., the output is true) in an execution           invariant provided by a programmer (the grey box in Figure 2).
under D1 , and maps noise v to v otherwise. As we will see shortly,
dependent types allow a precise privacy cost to be calculated under         2.5    Type Inference
various program states, hence enabling bounding privacy cost in a           The mechanisms sketched so far provide a light-weight yet power-
tighter way than mechanisms based on the composition theorem.               ful formal method for differential privacy. The annotation burden
    Moreover, LightDP uses a distinguished distance ∗ as a short-           is much reduced compared with (Barthe et al. 2016c). However,
hand for the standard Sigma type (e.g., num∗ , Σx:num0 numx ). In           providing the correct and optimal type annotations (especially for
other words, each value of type num∗ (e.g., each query in the list q)       random variables η1 and η2 ) is still subtle for a programmer.
can be interpreted as a pair of the form (x : num0 , y : numx ), where          Although it is folklore that type inference in face of dependent
the first component specifies the distance of the second component.         types can be daunting, LightDP is equipped with an inference en-
Note that by language design, the first component is invisible in the       gine that, at least for many algorithms, not only infers correct an-
privacy-preserving algorithm; however, the type system may rea-             notations, but also enables finding annotations that minimize pri-
son about and manipulate it via a distinguished operationb. For             vacy cost when multiple annotations exist. For example, given the
instance, the precondition in the running example states the adja-          function signature in Figure 1, the inference algorithm in Section 5
cent assumption on databases: for each query answer q[i] in q, its          automatically infers types for all variables. The inferred types are
distance (bq [i]) is bounded by ±1. The star type is also useful for dis-   identical to the ones in Figure 1 except that T̃ , η1 are assigned
tances that cannot be easily captured at compile time (Section 3.1).        with a distance α and η2 is assigned with a distance expression
    With type annotations, a type system statically verifies that the       q[i]+η2 ≥ T̃ ?β : γ, where α, β, γ are variables to be inferred, sub-
distances are maintained as an invariant throughout the execution.          ject to constraints generated during type checking. For the Sparse
For example, the output out in Figure 1 has type list bool0 ,               Vector method, multiple correct type annotations exist. For exam-
meaning that each element in the list has type bool0 . Hence, the           ple, α = 1, β = 2, γ = 0 corresponds to the annotation in Figure 1.
invariant maintained by the type system ensures that two related            Moreover, α = 0, β = 2, γ = −2 and α = 2, β = 3, γ = 0 are
executions always generate the same output.                                 both correct annotations.
Calculating privacy cost When type-checking succeeds, the type                  Given type annotations with distance variables, the type-guided
system transforms the original program to a non-probabilistic, non-         transformation as sketched above generates target program where
relational program where privacy cost is explicitly calculated. The         variables to be inferred (i.e., α, β, γ) are used in the calculation of
transformed program for the Sparse Vector method is shown in                privacy cost. The difference is that v increments by (α)/2 at line
Figure 2.                                                                   2 and increments by (q[i] + η2 ≥ T̃ ?β : γ) × /4N at line 6 in
    The transformed program is almost identical to the original             Figure 2. By Hoare logic, we can easily bound the privacy cost to
one, except that: 1) the privacy cost is explicitly calculated via a        be α/2 + β/4 + c2 × γ/4N .
new variable v , and 2) probabilistic instructions are replaced by a           Putting it all together, finding the optimal proof is equivalent
new nondeterministic instruction havoc η, which semantically sets           to a MaxSMT problem: min (2α + β + c2 × γ/N ), given that
variable η to an arbitrary value upon execution.                            constraints generated in type checking are satisfiable. Using an
    The fundamental soundness theorem of the type system states             existing MaxSMT solver, µZ (Bjørner and Phan 2014; Bjørner
that, informally, if 1) the original program type-checks, and 2) v         et al. 2015), the optimal proof for the Sparse Vector method is
is always bounded by some constant 0 in the transformed program,           successfully inferred: α = 1, β = 2, γ = 0. This is exactly the
then the original program being verified is 0 -differentially private.     randomness alignment used in its proof (Dwork and Roth 2014).
 Reals       r ∈ R                                                             function PARTIAL S UM (, b, size : num0 ; q : list num∗ )
 Booleans    b ∈ {true, false}                                                          returns (out : num0 )
 Vars        x ∈ Var                                                                    precondition ∀i ≥ 0. qb[i] ≤ b∧
 Rand Vars η ∈ H                                                                        ∀i ≥ 0. qb[i] > 0 ⇒ (∀j > i. qb[j] = 0)
 Linear Ops ⊕ ::= + | −
 Other Ops ⊗ ::= × | /                                                         1     sum : num∗ ; i : num0 ; η : num−sum
                                                                                                                     c
 Comparators ::= <|>|=|≤|≥                                                     2     sum := 0; i := 0;
 Rand Exps g ::= Lap r                                                         3     while (i < size)
 Expressions e ::= r | b | x | η | e1 ⊕ e2 | e1 ⊗ e2 | e1 e2 |                 4       sum := sum+q[i];
                   ¬e | e1 :: e2 | e1 [e2 ] | e1 ?e2 : e3                      5       i := i+1;
                                                                               6     η = Lap b/;
 Commands c ::= skip | x := e | η := g | c1 ; c2 | return e |
                                                                               7     out := sum + η;
                   if e then c1 else c2 | while e do c
 Distances   d ::= r | x | η | d1 ⊕ d2 | d1 ⊗ d2 | d1 d2 ?d3 : d4
                                                                               Figure 4. An -differentially private algorithm for summing over
 Types       τ ::= numd | num∗ | bool | list τ | τ1 → τ2
                                                                               a query list.
               Figure 3. LightDP0 : language syntax.
                                                                                   Since non-numeric types bool, list τ and τ1 → τ2 cannot be
3.    LightDP: A Language for Algorithm Design                                 associated with any numeric distance, those types are syntactic sug-
                                                                               ars for bool0 , (list τ )0 and (τ1 → τ2 )0 respectively. Notice that
We first introduce a simple imperative language, LightDP0 , for de-            elements in a list of type (list τ )0 (e.g., parameter q in Figure 1)
signing and verifying privacy-preserving algorithms. This language             may still have different elements in two related executions, since
is equipped with a dependent type system that enables formal veri-             the difference of elements is specified by type τ . The subscript 0
fication of sophisticated algorithms where the composition theorem             here simply restricts the list size in two related executions.
falls short. In this section, we assume all type annotations are pro-
vided by a programmer. We will remove this restriction and enable              Star type LightDP0 also supports sum types, written as B∗ , a
type inference in Section 5.                                                   syntactic sugar of a Sigma type. More specifically, a variable x
                                                                               with type num∗ is desugared as x : Σ(bx:num0 ) numxb , where x    b is
3.1   Syntax                                                                   a distinguished variable invisible in the source code, but can be
The language syntax is given in Figure 3. LightDP0 is mostly a                 reasoned about and manipulated by the type system. Hiding the
standard imperative language except for the following features.                first component of a Sigma type simplifies verification (Section 4).
                                                                                   The parameter q in Figure 1 is one example where the star type
Random expressions Probabilistic reasoning is essential in privacy-            is useful. Moreover, the star type enables reasoning about depen-
preserving algorithms. We use g to represent a random expression.              dencies that cannot be captured otherwise by a distance expression.
Since LightDP0 follows a modular design where new randomness                   Consider the -differentially private Partial Sum algorithm in Fig-
expression can be added easily, we only consider the most inter-               ure 4. It implements an immediate solution to answering the sum
esting random expression, Lap r, for now. Semantically, Lap r                  of a query list in a privacy preserving manner3 : it aggregates the
draws one sample from the Laplace distribution, with mean zero                 accurate partial sum in a loop, and releases a noisy sum using the
and a scale factor r. We will discuss other random expressions in              Laplace mechanism. The precondition specifies the adjacency as-
Section 6.3.                                                                   sumption: at most one query answer may differ by at most b.
    Each random expression g can be assigned to a random vari-                     In this algorithm, the distance of variable sum changes in each it-
able η, written as η := g. We distinguish random variables (H)                 eration. Hence, the accurate type for sum is numPi qb[j] . However,
                                                                                                                                   j=0
from normal variables (Var) for technical reasons explained in Sec-            with the goal of keeping type system as light-weight as possible,
tion 3.3. Notice that although the syntax restricts the distribution           we assign sum to a star type. The type system will reason about and
scale parameters to be a constant, its mean can be an arbitrary ex-            manipulate distance component sd    um in a sound way (Section 3.3).
pression e, via the legit expression e + η, where η is sampled from
a distribution with mean zero.                                                 3.2    Semantics
List operations Sophisticated algorithms usually make multiple                 The denotational semantics of the probabilistic language is defined
queries to a database and produce multiple outputs during that                 as a mapping from initial memory to a distribution on (possible)
process. Rather than reasoning about the privacy cost associated               final outputs. Formally, let M be a set of memory states where each
with each query in isolation and total the privacy costs using the             memory state m ∈ M is an assignment of all (normal and random)
composition theorem, LightDP0 enables more precise reasoning                   variables (Var ∪ H) to values. First, an expression e of base type B
via built-in list type operations: e1 :: e2 appends the element e1 to a        is interpreted as a function JeK : m → JBK, where JBK represents
list e2 ; e1 [e2 ] gets the e2 -th element in list e1 , assuming e2 is bound   the set of values belonging to the base type B. We omit expression
by the length of e1 . We also assume a list variable is initialized to         semantics since it is mostly standard4 .
an empty list.                                                                     A random expression g is interpreted as a distribution on real
                                                                               values. Hence, JgK : Dist(JnumK). Moreover, a command c is in-
Types with distances Each type τ has the form of Bd . Here, B                  terpreted as a function JcK : M → Dist(M). For brevity, we
is a base type, such as num (numeric type), bool (Boolean), or an              write JeKm and JcKm instead of JeK(m) and JcK(m) hereafter. Fig-
application of a type constructor (e.g., list) to another type, or a           ure 5 provides the semantics of commands, where functions unit
function (τ1 → τ2 ). d is a numeric expression that (semantically)
specifies the exact distance of the values stored in a variable in             3 We use this trivial algorithm here for its simplicity. We will analyze a more
two related executions. In particular, a distance expression is a              sophisticated version in Section 6.
numeric expression in the language, as specified in Figure 3, where            4 The reals in LightDP only come from sampling (or, the havoc command,
d1 d2 ?d3 : d4 evaluates to d3 when the comparison evaluates to                which mimics sampling). We assume the sample space is either finite or
true, and d4 otherwise.                                                        countable.
                   JskipKm = unit m
                 Jx := eKm = unit (m{JeKm /x})
                                                                        Typing rules for expressions.
                 Jη := gKm = bind JgK (λv. unit m{v/η})
               Jc1 ; c2 Km = bind (Jc1 Km ) Jc2 K                                          (T-N UM )                           (T-B OOLEAN )
                             (                                              Γ ` r : num0                      Γ ` b : bool
                               Jc1 Km if JeKm = true
Jif e then c1 else c2 Km =                                                                    (T-VAR )                           (T-VAR S TAR )
                               Jc2 Km if JeKm = false                    Γ, x : Bd ` x : Bd                Γ, x : B∗ ` x : Bxb
          Jwhile e do cKm = w∗ m
                                                                                  Γ ` e1 : numd1 Γ ` e2 : numd2
                  where w∗ = f ix(λf. λm.if JeKm = true                               Γ ` e1 ⊕ e2 : numd1 ⊕d2
                                                                                                                (T-OP LUS )

                                  then (bind JcKm f ) else (unit m))
                                                                                   Γ ` e1 : num0 Γ ` e2 : num0
           Jc; return eKm = bind (JcKm ) (λm0 . unit JeKm0 )                                                   (T-OT IMES )
                                                                                        Γ ` e1 ⊗ e2 : num0
              Figure 5. LightDP0 : language semantics.
                                                                            Γ ` e1 : numd1        Ψ ⇒ (e1 e2
                                                                            Γ ` e2 : numd2    ⇔ (e1 +d1 ) (e2 +d2 ))
                                                                                                                     (T-OD OT )
and bind are defined in Section 2.1. This semantics corresponds                         Γ ` e1 e2 : bool
directly to a semantics given by Kozen (1981), which interprets
programs as continuous linear operators on measures.                     Γ ` e : bool                  Γ ` e1 : τ Γ ` e2 : list τ
                                                                                      (T-N EG )                                   (T-C ONS )
    Finally, we assume all programs have the form (c; return e)         Γ ` ¬e : bool                     Γ ` e1 :: e2 : list τ
where c does not contain return statements. A LightDP0 program
is interpreted as a function m → DistJBK, defined in Figure 5,                    Γ ` e1 : list τ Γ ` e2 : num0
where B is the type of expression returned (e).                                                                 (T-I NDEX )
                                                                                           Γ ` e1 [e2 ] : τ
3.3    Typing Rules and Target Language
                                                                              Γ ` e1 : bool Γ ` e2 : τ Γ ` e3 : τ
We assume a typing environment Γ that tracks the type of each                                                     (T-S ELECT )
                                                                                        Γ ` e1 ?e2 : e3 : τ
variable (including random variable). For now, we assume a type
annotation is provided for each variable (i.e., dom(Γ) = Var ∪ H),      Typing rules for commands
but we will remove this restriction in Section 5. The typing rules
are formalized in Figure 6. Since all typing rules share a global                                                 (T-S KIP )
invariant Ψ (e.g., the precondition in Figure 1), typing rules do not                      Γ ` skip * skip
propagate Ψ for brevity. We also write Γ(x) = d for ∃B. Γ(x) =
Bd when the context is clear.                                                      Γ ` e : τ Γ ` x : Bd τ = Bd
                                                                                                               (T-A SGN )
                                                                                        Γ ` x := e * x := e
Expressions For expressions, each rule has the form of Γ ` e : τ ,
meaning that the expression e has type τ under the environment Γ.                  Γ ` x : Bxb   Γ ` e : Bd
Rule (T-OP LUS ) precisely tracks the distance of linear operations                                           (T-A SGN S TAR )
(e.g., + and −), while rule (T-OT IMES ) makes a conservative as-                Γ ` x := e * x := e; x
                                                                                                      b := d;
sumption that other numerical operations take identical parameters.
It is completely possible to refine rule (T-OT IMES )) (e.g., by fol-                Γ ` c1 * c01 Γ ` c2 * c02
                                                                                                                 (T-S EQ )
lowing the sensitivity analysis proposed by Reed and Pierce (2010);                      Γ ` c1 ; c2 * c01 ; c02
Gaboardi et al. (2013)) to improve precision, however, we leave that
as future work since it is largely orthogonal.                                   Γ ` e : num0 or Γ ` e : bool0
    Rule (T-VAR S TAR ) applies when variable x has a star type.                                               (T-R ETURN )
                                                                                    Γ ` return e * return e
This rule unpacks the corresponding pair with Sigma type and
makes x b explicit in the type system.
    The most interesting and novel rule is (T-OD OT ). It type-checks         Γ ` e : bool Γ ` ci * c0i where i ∈ {1, 2}
                                                                                                                             (T-I F )
a comparison of two real expressions by generating a constraint:           Γ ` if e then c1 else c2 * if e then c01 else c02
              Ψ ⇒ (e1       e2 ⇔ (e1 +d1 )     (e2 +d2 ))                           Γ ` e : bool   Γ ` c * c0
                                                                                                                  (T-W HILE )
    Intuitively, this constraint requires that in two related execu-             Γ ` while e do c * while e do c0
tions, the Boolean value of e1       e2 must be identical since the
distances of e1 and e2 are specified by d1 and d2 respectively. For     Typing rules for random assignments
example, consider the branch condition q[i] + η2 ≥ T̃ in Figure 1.
Rule (T-OD OT ) first checks types for subexpressions:                                   Γ(η) = numd
                                                                                                                     (T-L APLACE )
                                                                          Γ ` η := Lap r * havoc η; v = v + |d|/r;
      Γ ` q[i] + η2 : numqb[i]+(q[i]+η2 ≥T̃ ?2:0) and Γ ` T̃ : num1
Then the following constraint is generated (free variables in the       Figure 6. Typing rules. Ψ is an invariant that holds throughout
generated constraint are universally quantified):                       program execution.
  ∀qi , qbi , η2 , T̃ ∈ R. (−1 ≤ qbi ≤ 1) ⇒
qi + η2 ≥ T̃ ⇔ qi + η2 + qbi + (qi + η2 ≥ T̃ ?2 : 0) ≥ T̃ + 1
 Vars       x ∈ Var ∪ H ∪ {v }                                             Informally, the transformation says that by paying a privacy cost,
 Statements c ::= skip | x := e | havoc x | c1 ; c2 | return e              η has a distance of −dsum in two related executions. Hence, we can
                  if e then c1 else c2 | while e do c                       cancel out the distance of sum in line 7.
Figure 7. Target language syntax. The omitted parts are identical           Dependent types and imperative programming Mutable states in
to the source language defined in Figure 3.                                 imperative programming brings subtleties that are not foreseen in
                                                                            the standard theory of dependent types (Martin-Löf 1984). Con-
                                                                            sider a variable x with type numy where y is initialized to zero. The
    This proof obligation captures a subtle yet important property          type of x establishes an invariant on its values v1 , v2 under two ex-
of the Sparse Vector method: given the randomness alignment as              ecutions: v (1) = v (2) . However, if we update the value of y to 1,
specified by Γ, two related executions must take the same branch            the invariant changes to v (1) + 1 = v (2) , but the values of x in two
(hence, produce the same output). This proof obligation can easily          executions remains unchanged. Hence, the type invariant is broken.
be discharged by an external SMT solver, such as Z3 (de Moura                   To address this issue, we assume the following assumptions
and Bjørner 2008).                                                          are checked before type checking. First, for each normal variable
Target language The typing rules for a command have the form                x ∈ Var such that Γ(x) = Bd , all free variables in d are immutable.
of Γ ` c * c0 , where c is the original program being verified,             For example, each normal variables in Figure 1 has a constant
and c0 is the transformed program in the target language defined            distance in its type. Note that by language syntax, this restriction
in Figure 7. The target language is mostly identical to the original        does not apply to variables with a star type. Second, a random
one, except for two significant differences: 1) the target language         variable η ∈ H may depend on mutable variables. However, we
involves a distinguished variables v to explicitly track the privacy       assume that it has only one use other than the definition, and the
cost in the original program; 2) the target language removes prob-          definition of η is adjacent to its use. Hence, each variable that η
abilistic expressions, and introduces a new nondeterministic com-           depends on appears immutable between η’s definition and use 5 .
mand (havoc x), which sets variable x to an arbitrary value upon
execution. Hence, the target language is nonprobabilistic.                  4.    Soundness
    Due to nondeterminism, the denotational semantics interprets a
command c in the target language as a function JcK : M → P(M).              The type system in Section 3.3 enforces a fundamental property: if
For example, the semantics of the havoc command is defined as               Γ ` c * c0 and v in c0 is bounded by some constant , then the
follows:                                                                    original program being verified is -differentially private.
                                                                               To formalize and prove this soundness property, we first notice
                  Jhavoc xKm = ∪r∈R {m{r/x}}                                that a typing environment Γ defines a relation on two memories,
Other commands have a standard semantics, hence their semantics             since Γ specifies the exact distance of each variable:
are included in the appendix. Note that for simplicity, we abuse the
notation JcK to denote the semantics of both the source language            Definition 2 (Γ-Relation). Two memories m1 and m2 are related
and target language. However, its meaning is unambiguous in the             by a typing environment Γ, written m1 Γ m2 , iff
context of a memory m: when v 6∈ dom(m), JcKm denotes a                         ∀x ∈ Var. m1 (x) + Jdx Km1 = m2 (x), where Γ ` x : Bdx
distribution; otherwise, JcKm denotes a set.
                                                                               Note that since Γ(x) might be a dependent type, the definition
Commands Informally, if Γ ` c * c0 , and the distinguished                  needs to evaluate the distance of x (dx ) under m1 .
variable v in c0 is bounded by some constant 0 in all possible               By the definition above, Γ is a function since for any memory
executions, then program c is 0 -differentially private. Here, we          m, the distance for each variable in the related memory of m is a
discuss important typing rules to enforce this property. We will            constant. Hence, we also write Γ(m) to represent the unique m0
formalize this soundness property and sketch a proof in Section 4.          such that m Γ m0 . Moreover, given a set of distinct memories
    For an assignment x := e, rule (T-A SGN ) synthesizes the               S ⊆ M, we define Γ S , {Γ(m) | m ∈ S}. Note that by
types of x and e, and checks that their types are equivalent (i.e.,         definition, Γ S is also a set of distinct memories (hence, not a
both the base type and distance are equivalent). However, rule (T-          multiset). Furthermore, we assume that Γ is an injective function.
A SGN S TAR ) instruments the original program so that the typing           We make this assumption explicit by the following definition.
invariant (i.e., the distance of x is exactly x
                                              b) is maintained after the
assignment. Consider line 4 in Figure 4. Rule (T-A SGN S TAR ) first        Definition 3 (Well-Formed Γ-relation). A typing environment Γ is
checks subexpressions: Γ ` sum + q[i] : sd       um + qb[i]. Hence, the     well-formed, written ` Γ, iff Γ is an injective function.
transformed program is (sum := sum + q[i]; sd       um := sd um + qb[i]),       Checking well-formedness of the Γ-relation is straightforward.
which correctly maintains the typing invariant after the assignment.        Intuitively, Γ is well-formed when there is no “circular” depen-
    (T-R ETURN ) checks that the returned value is indistinguishable        dency, while more careful analysis is needed for circular depen-
in two related executions. Both (T-I F ) and (T-W HILE ) check that         dencies. Consider the Sparse Vector method in Figure 1 and any
two related executions must follow the same control flow.                   m1 and m2 such that Γ m1 = Γ m2 = m for some m. For a
                                                                            variable y with a constant distance v (e.g., T̃ , η1 , qb[i]), we have
Laplace mechanism Intuitively, (T-L APLACE ) assigns a poly-
                                                                            m1 (y) = m(y) − v = m2 (y). So m1 and m2 must agree
morphic type to the random source Lap r. In other words, for any
                                                                            on those variables. Then for any variable z that depends on vari-
distance d of random variable η, we can instantiate the type of Lap r
                                                                            ables that m1 and m2 already agree on, the distance of z must be
to be numd , though with a privacy cost of |d|/r. Moreover, the trans-
                                                                            identical in m1 and m2 ; hence, m1 (z) = m2 (z). For the circu-
formed program sets η to a nondeterministic value (havoc η), since
                                                                            lar dependency on variable η2 (whose distance depends η2 ), con-
any real value can be sampled from the Laplace distribution.
    Consider line 1 in Figure 1. (T-L APLACE ) transforms this line         5 The one-use assumption may appear restrictive at first glance, but when
to (havoc η1 ; v := v +/2) since Γ(η1 ) = num1 . Informally, the         η’s type has no dependency on mutable variables, we can always store η to
transformation says that by paying a privacy cost of /2, Lap (2/)         a normal variable to circumvent this restriction. When η’s type depends on a
ensures that η1 has a distance of one in two related executions.            mutable variable and multiple uses of η are needed, we can store η’s value to
    Moreover, consider line 6 in Figure 4. (T-L APLACE ) transforms         a normal variable with star type, whose distance counterpart is manipulated
this line to (havoc η; v := v + |d sum|/b) since Γ(η) = −d     sum.      and reasoned about by the type system.
sider t = JT̃ − q[i]Km1 = JT̃ − q[i]Km2 . The mapping for η2 is          Distance Vars α, β, γ ∈ DVar
v 7→ v + 2 when v > t and v 7→ v otherwise. Since this mapping           Distances     d              ::= · · · | α
is strictly monotonic, it is injective.
    For differential privacy, we are interested in the relationship                Figure 8. LightDP: language syntax extension.
between two memory distributions. Given a typing environment Γ
and constant , we define the (Γ, ) distance, written ∆Γ , of two
                                                                        et al. 2013; Barthe et al. 2012, 2014)) have to (conservatively) pro-
memory distributions:
                                                                        vide an unique cost bound for all possible executions, rendering a
Definition 4 (Γ -distance). The Γ -distance of two distributions      cost of 2/N .
µ1 , µ2 ∈ Dist(M), written ∆Γ (µ1 , µ2 ), is defined as:                   The point-wise soundness lemma provides a precise privacy
                                                                        bound per initial and final memory. However, differential privacy
         ∆Γ (µ1 , µ2 ) , max (µ1 (S) − exp()µ2 (Γ S))                 by definition (Definition 1) bounds the worst-case cost. To close
                           S⊆M
                                                                        the gap, we define the worst-case cost of the transformed program.
    Note that when S = ∅, the distance is 0 by definition. So
∆Γ (µ1 , µ2 ) ≥ 0 for any , µ1 , µ2 .                                 Definition 7. For any program c in the target language, we say c’s
    The soundness theorem connects the “privacy cost” of the prob-      execution cost is bounded by some constants , written c , iff for
abilistic program to the distinguished variable v in the transformed   any m ] (0),
nonprobabilistic program. In order to formalize the connection, we                         m0 ] (0 ) ∈ JcKm](0) ⇒ 0 ≤ 
first extend memory in the source language to include v :
                                                                            Note that this safety property can be verified by an external
Definition 5. For any memory m and constant , there is an              mechanism such as Hoare logic and model checking. Off-the-shelf
extension of m, written m ] (), so that
                                                                        tools can be used to verify that c holds for some . For example,
                    ∀x ∈ dom(m). m ] ()(x) = m(x)                      we have formally proved that the transformed program in Figure 1
               ∧ m ] ()(v ) =                                        satisfies a postcondition v ≤  by providing one line of annotation
                                                                        (the grey line in Figure 1) using the Dafny tool (Leino 2010).
    Next, we introduce useful lemmas and theorems. First, we show
that the type-directed transformation Γ ` c * c0 is faithful. In        Theorem 1 (Soundness).
other words, for any initial memory m and program c, memory m0
                                                                             ∀c, c0 , m1 , m2 , Γ, . ` Γ∧Γ ` c * c0 ∧m1 Γ m2 ∧c0 , we have
is a possible final memory iff for initial extended memory m ] (0)
and c0 , one final memory is an extension of m0 .                                                                ∆Γ (JcKm1 , JcKm2 ) ≤ 0
Lemma 1 (Faithfulness).                                                 Proof. By definition, (max(c m
                                                                                                      m1 )) ≤  for all m, m1 . Hence by
                                                                        Lemma 2, ∀m. JcKm1 (m) ≤ exp()JcKm2 (Γ(m)). Hence,
  ∀m, m0 , c, c0 , Γ. Γ ` c * c0 ⇒
                      JcKm (m0 ) 6= 0 ⇔ ∃. m0 ] () ∈ Jc0 Km](0)                 max (JcKm1 (S) − exp()JcKm2 (Γ(S)))
                                                                                   S⊆M
                                                                                       X
Proof. By structural induction on c.                                            = max     (JcKm1 (m) − exp()JcKm2 (Γ(m))) ≤ 0
                                                                                   S⊆M
                                                                                         m∈S
                                                        0
   For a pair of initial and final memories m0 and m when exe-          We note that the equality in the proof above holds due to the
cuting the original program, we identify a set of possible v values,   injective assumption (` Γ), which allows us to derive the set-based
so that in the corresponding executions of c0 , the initial and final   privacy from the point-wise privacy (Lemma 2).
memories are extensions of m and m0 respectively:
Definition 6. Given a target program c0 , an initial memory m0                We now connect the soundness theorem to differential privacy:
and a final memory m0 , the consistent costs of executing c0 w.r.t.     Theorem 2 (Privacy).
                          0
m0 and m0 , written c0 m
                        m0 , is defined as follows
                0
                                                                             ∀Γ, c, c0 , x, . ` Γ∧Γ ` (c; return e) * (c0 ; return e) then
         0           0        0      0                0
        c    m
              m0 , { | m ] ( ) ∈ Jc Km0 ](0) ∧ m = m }
                                                                                                       c0 ⇒ c is -differentially private
                0                      0
where m = m iff ∀x ∈ dom(m). m (x) = m(x)
                                                                        Proof. Proof is available in the appendix.
   Since (c0 m
              m1 ) by definition is a set of values of v , we write
max(c0 m m1 ) for the maximum cost. The next lemma enables
precise reasoning of privacy cost w.r.t. a pair of initial and final    5.     Differential-Privacy Proof Inference
memories when Γ is injective:                                           We have so far presented an explicitly typed language LightDP0 .
                                                                        However, writing down types (especially those dependent types)
Lemma 2 (Point-Wise soundness).
                                                                        for variables is still a non-trivial task. Moreover, when multiple
  ∀c, c0 , m1 , m2 , m, Γ. ` Γ ∧ Γ ` c * c0 ∧ m1 Γ m2 , we have         proofs exist, writing down types accompanied with the minimum
                                                                        privacy cost is even more challenging. We extend LightDP0 to
                    JcKm1 (m) ≤ exp(max(c0 m
                                            m1 ))JcKm2 (Γ(m))           automatically infer a proof and even search for the optimal one.
    The full proof of Lemma 2 is available in the appendix. We
comment that this point-wise result enables precise reasoning of        5.1     Type Inference
privacy cost where the composition theorem falls short. Consider        Since each type has two orthogonal components (base type and dis-
the transformed Sparse Vector method in Figure 2. This point-wise       tance), inference is needed for both. The former is mostly standard
result allows various cost bounds to be provided for various memo-      (e.g., for Hindley/Milner system (Wand 1987; Aiken and Wimmers
ries: v increments by 2/N when the branch condition is true, but      1993; Zhang and Myers 2014)), hence omitted in this paper.
it remains the same otherwise. On the other hand, methods based             Next, we assume all base types are available, and focus on
on the composition theorem (e.g., (Reed and Pierce 2010; Gaboardi       the inference of the distance counterpart. For brevity, we write
Γ(x) = d instead of ∃B. Γ(x) = Bd . We use DefVars to represent          Refinement rules for expressions
the set of variables whose distances are given by the programmer.
    To enable type inference, we extend LightDP0 with distance                                            b ∈ {true, false}
variables such as α, β, γ (shown in Figure 8). Initially, the typing                    (R-N UM )                           (R-B OOLEAN )
                                                                          Γ; P n
                                                                               or:Γ                          Γ; P n
                                                                                                                  ob:Γ
environment associates each variable in DefVars with its annotated
distance. It associates each other variable with a distinguished                                                    P=∅
distance variable to be inferred.                                                            (R-VAR )                      (R-R AND )
    Following the idea of modeling type inference as constraint               Γ; P n
                                                                                   ox:Γ                          Γ; P n
                                                                                                                      oη:Γ
solving (e.g., (Wand 1987; Aiken and Wimmers 1993; Haack and
Wells 2004)), it is straightforward to interpret the typing rules in            P 6= ∅     αt , αf fresh variables
                                                                                                                   (R-R AND -R EFINE )
Figure 6 as a (naive) inference algorithm. To see how, consider two           Γ; P n
                                                                                   o η : refine(Γ, η, P?αt : αf )
assignments (x := 0; y := x), where Γ(x) = α, Γ(y) = β. With
distance variables, the typing rules now collect constraints (instead        Γ; P n
                                                                                  o e1 : Γ1 Γ1 ; P n
                                                                                                   o e2 : Γ2 op ∈ ⊕ ∪ ⊗
of checking their validity) during type checking. For example, two                                                      (R-O PS )
                                                                                          Γ; P n
                                                                                               o e1 op e2 : Γ2
constraints are collected for those two assignments: α = 0 and
β = α. Hence, inferring types is equivalent to finding a solution for    Γ; P ∧ (e1         o e1 : Γ1 Γ1 ; P ∧ (e1
                                                                                       e2 ) n                             e2 ) n
                                                                                                                               o e2 : Γ2
those two constraints (i.e., the satisfiability problem of ∃α, β. α =                                                                      (R-OD OT )
0 ∧ β = α). It is easy to check that α = 0 ∧ β = 0 is a solution.                           Γ; P no e1 e2 : Γ2
Hence, the inferred distances are Γ(x) = 0, Γ(y) = 0. However,
this naive inference algorithm falls short in face of dependent types.             Γ; P n
                                                                                        o e1 : Γ1 Γ1 ; P n  o e2 : Γ2
                                                                                                                      (R-C ONS )
Next, we first explore the main challenges in inferring dependent                        Γ; P no e1 :: e2 : Γ2
types, and then propose our inference algorithm.
Inferring star types Consider the example in Figure 4. If we                  o e : Γ0
                                                                         Γ; P n                        Γ; P n
                                                                                                            o e1 : Γ1 Γ1 ; P n  o e2 : Γ2
                                                                                        (R-N EG )                                         (R-I DX )
follow the naive inference algorithm above, two constraints are               o ¬e : Γ0
                                                                         Γ; P n                              Γ; P no e1 [e2 ] : Γ2
generated from lines 2 and 4: α = 0 and α = α + qb[i], where
α = Γ(sum). These constraints are unsatisfiable, since the value         Refinement rules for commands
of qb[i] is an arbitrary value between −1 and 1. Nevertheless, the                        (R-S KIP )                              (R-R ETURN )
powerful type system of LightDP0 still allows formal verification          Γn
                                                                            o skip : Γ                       Γn
                                                                                                              o return e : Γ
of this example by assigning sum to the star type, meaning that its
distance is dynamically tracked.                                           x 6∈ DefVars         o e : Γ0
                                                                                           Γ, ∅ n             Γ0 ` e : d
    We observe that starting from the initial typing environment, we                                                     (R-A SGN -R EF )
                                                                                  Γno x := e : refine(Γ0 , x, d)
can refine it by processing each assignment x := e in the following
way. We first synthesize the type of e from its subexpressions, in
the same fashion as the original typing rules in Figure 6. Then, if                   x ∈ DefVars Γ, ∅ no e : Γ0
                                                                                                                 (R-A SGN )
x ∈ DefVars (i.e., given by the programmer), there is nothing                              Γno x := e : Γ0
to be refined. Otherwise, we can refine the typing environment by
updating the type of x to a more precise one:                                           o c1 : Γ0 Γ0 n
                                                                                       Γn              o c2 : Γ00
                                                                                                                  (R-S EQ )
                                                                                             o c1 ; c2 : Γ00
                       
                       Γ{d/α}
                                    if Γ(x) = α ∈ DVar                                    Γn
 refine(Γ, x, d) , Γ                 if Γ(x) 6∈ DVar ∧ (Γ(x) = d)
                       Γ[x 7→ ∗] otherwise
                                                                               Γ; ∅ n
                                                                                     o e : Γ1 Γ1 n
                                                                                                 o c1 : Γ2 Γ2 n o c2 : Γ 3
                                                                                                                           (R-I F )
                                                                                      Γno if e then c1 else c2 : Γ3
Here, the auxiliary function refine takes an initial environment Γ,
a variable x and a distance expression d. This function replaces all          Γ; ∅ n
                                                                                   o e : Γ1    Γ1 ≤ Γ2       Γ2 n
                                                                                                                o c : Γ2
occurrences of α in Γ to d when Γ(x) is a variable to be inferred                                                        (R-W HILE )
                                                                                         Γno while e do c : Γ2
(α ∈ DVar). Otherwise, it statically checks whether the old and new
distance expressions are equivalent. When the equivalence cannot         Refinement for random assignments
be determined at static time, it assigns the ∗ type to x.
    Our inference algorithm refines the typing environment as it                                                  (R-L APLACE )
proceeds. Consider Figure 4 again. At line 4, sum’s distance is                         Γn
                                                                                         o η := Lap r : Γ
refined to 0. Then at line 6, its distance is refined to ∗, since we
cannot statically check that 0 = 0 + qb[i] is valid.                                   Figure 9. The refinement algorithm.
Inferring dependency on program state Consider Figure 1 where
only the type of η2 is to be inferred. The naive inference algorithm     from dependency on program states. Hence, our inference algo-
will generate one constraint for the branch condition in line 6:         rithm propagates the comparison result to its subexpressions, and
   ∀qi , qbi , η2 , T̃ . (−1 ≤ qbi ≤ 1) ⇒                                refine subexpressions (e.g., η2 ) for the needed dependency.
                 (qi + η2 ≥ T̃ ⇔ (qi + η2 + qbi + α ≥ T̃ + 1)
                                                                         Inference algorithm We now present our inference algorithm,
which is unsatisfiable, since there is no single value α that can hide   which is still based on the typing rules in Figure 6. However, to
the difference of qi in both directions. We need a more precise type     tackle the challenges above, we run a refinement algorithm before
for η2 (as provided in Figure 1) so that the “if” and “else” branches    type inference. The algorithm is shown in Figure 9.
can be aligned in different ways.                                           For expressions, the refinement algorithm propagates context
    To infer dependent types, our inference algorithm propagates         information P to subexpressions. Hence, each rule for expression
context information to subexpressions. In particular, we observe         has the form of Γ, P n o e : Γ0 , where P is a predicate that may
that only rule (T-OD OT ) generates a constraint that may benefit        appear in a dependent type, Γ is the typing environment to be re-
fined, and Γ0 is the refined environment. The context information P        function MS PARSE V EC (T, N : num; q : list num; qb : list num;
is used to refine distance of a random variable η in rule (R-R AND -       α, β, γ : num)
R EFINE ). Note that the refinement is not needed for a normal vari-                  returns out : list num
able x (rule (R-VAR )). Intuitively, the reason is that the “shape” of                precondition ∀i. −1 ≤ (b
                                                                                                             q [i]) ≤ 1
x is either provided or has been refined when x is initialized. How-
                                                                            1    v := 0;
ever, this is not true for a random variable: η can have any distance
                                                                            2    havoc η1 ; v := v + (α/2);
expression according to rule (T-L APLACE ).
    The refinement rules for commands have the form of Γ n    o c : Γ0 .    3    T̃ := T + η1 ;
As we described informally above, rule (R-A SGN -R EF ) refines             4    c1 := 0; c2 := 0; i := 0;
the distance of x using the refine function when its distance is            5    while (c1 < N)
not given. The rule (R-W HILE ) assumes that a fixed point exists.          6       Invariant : c1 ≤ N ∧ v = α        β
                                                                                                                 + c1 × 2N        γ
                                                                                                                           + c2 × 2N
                                                                                                              2
Based on the definition of the refine function, a fixed point can
be computed as follows. We define ≤ as the lifted relation based on         7      havoc η2 ; v := v + (q[i] + η2 ≥ T̃ ?β : γ) × /4c;
a point-wise lattice (for each variable) where: ∀α, β ∈ DVar. α ≤           8      if (q[i] + η2 ≥ T̃ ) then
β ∧ β ≤ α and α ≤ d ≤ ∗ if d is not a distance variable. We                 9        out:= true::out;
can compute a fixed point by Γ1 = Γ0 ` c : Γ1 , Γ1 ` c :                   10        c1 := c1+1;
                                                                           11      else
Γ2 , · · · until Γi ` c : Γi for some i. Based on the definition
                                                                           12        out:= false::out;
of the refine function, it is easy to check that Γi ≤ Γi+1 and             13        c2 := c2+1;
the computation terminates since whenever Γi 6= Γi+1 , either              14      i := i+1;
the number of distance variables is reduced by one, or one more
variable has a star type.                                                  Figure 10. The target program with unknown type variables. The
                                                                           instrumented statements are underlined.
Example We consider type inference for our running example in
Figure 1 where all local variables are to be inferred. We first run        problem, where M is a large number since c2 is not bounded:
the refinement algorithm. The first refinement happens at line 2,
where the distance of T̃ is refined to α, the distance variable of                      α  β
                                                                                 min(     + + M × γ) such that
η1 . At line 3, c1 , c2 and i are refined to distance 0. In the loop                    2  2
body, η2 is refined to q[i] + η2 ≥ T̃ ?β : γ at line 6, using                              ∀qi , qbi , η2 , T̃ ∈ R. (−1 ≤ qbi ≤ 1) ⇒
rule (R-R AND -R EFINE ). At line 8, refine(Γ, c1, 0) returns Γ                                                                                  
since 0 = 0 is always true. Similar for the “else” branch and line         qi + η2 ≥ T̃ ⇔ qi + qbi + η2 + (qi + η2 ≥ T̃ ?β : γ) ≥ T̃ + α
12. Hence, the environment after line 12 is already a fixed point          Using a MaxSMT solver µZ (Bjørner and Phan 2014; Bjørner
for the loop body. Hence, the typing environment after refinement          et al. 2015), we successfully find the optimal solution for the type
is: Γ(c1) = Γ(c2) = Γ(i) = 0, Γ(T̃ ) = Γ(η1 ) = α and                      variables: α = 1, β = 2, γ = 0. This is exactly the randomness
Γ(η2 ) = (q[i] + η2 ≥ T̃ )?β : γ.                                          alignment used in its formal proof (Dwork and Roth 2014).
                                                                               We note that the translation to the MaxSMT problem at this
                                                                           stage still requires programmer efforts (e.g., identifying the cost
Type checking with distance variables With type variables in the           bound involving type variables and converting the cost bound to an
refined environment Γ, the type system collects constraints during         equivalent formula suitable for a MaxSMT solver). However, this
type checking, and tries to solve the collected constraints where          example clearly demonstrates the potential benefits of explicitly
the type variables are existentially qualified. For example, with          calculating the privacy cost in the target language.
type refinement, type checking the partial sum example in Figure 4
yields a unique solution, which is identical to the type annotation        5.3    Proof Automation
in the figure. In general, collected constraint may have multiple          In general, a LightDP-based proof consists four steps involving
solutions. For example, type checking the Sparse Vector method             manual efforts: 1) writing down the program specification (i.e., the
generates only one (nontrivial) constraint from the rule (T-OD OT ):       function signature that specifies private and non-private parameters
                                                                           and return values), 2) writing down the type annotations for local
      ∀qi , qbi , η2 , T̃ ∈ R. (−1 ≤ qbi ≤ 1) ⇒                            variables, 3) verifying that the privacy cost in the transformed
                                                                          program is bounded by either a known budget, or (MaxSMT only) a
qi + η2 ≥ T̃ ⇔ qi + qbi + η2 + (qi + η2 ≥ T̃ ?β : γ) ≥ T̃ + α
                                                                           formula involving unsolved type variables, and 4) (MaxSMT only)
                                                                           solving the MaxSMT problem of “min(upper bound formula) such
    It is easy to check that the type annotation in Figure 1 (i.e.,
                                                                           that constraints from step 2 are satisfiable”.
α = 1, β = 2, γ = 0) is a solution of the constraint. But in fact,
                                                                               As most verification tools, LightDP requires a programmer to
other solutions exist. For example, α = 0, β = 2, γ = −2 and
                                                                           write down specification (step 1). For step 2, we find that the infer-
α = 2, β = 3, γ = 0 are both valid solutions. The type system
                                                                           ence algorithm in Section 5.1 is powerful enough to automatically
can either pick a solution, or defer the inference by transforming
                                                                           infer the types for the nontrivial algorithms considered in this pa-
the original program to a target program where type variables are
                                                                           per6 . For step 3 and step 4, LightDP relies on the automation in
treated as unknown program inputs (as shown in Figure 10).
                                                                           existing verification tools. We note that though LightDP currently
                                                                           adds no automation in step 3 and 4, separating relational reasoning
5.2    Minimizing Privacy Cost                                             from counting privacy cost and automating task 2 greatly simpli-
                                                                           fies those steps for all examples that we have seen so far. We leave
With type variables captured explicitly in the transformed program,        systematic research in automating the entire proof as future work.
we can verify that the postcondition v = α 2
                                               + β
                                                  2
                                                    +c2× 2Nγ
                                                              holds
by providing the loop invariant shown in grey. Hence, combined             6 The only exception is the algorithm in Section 6.3, since the algorithm
with the remaining unsolved constraints on those type variables,           uses a uniformly distributed random source which is currently absent in the
finding the optimal proof is equivalent to the following MaxSMT            inference algorithm.
 function N UM S PARSE V ECTOR (T, N,  : num0 ; q : list num∗ )                  of Figure 11. To finish the proof, according to Theorem 2, it is
                                                                                  sufficient to verify the postcondition that v ≤ . In fact, only one
            returns (out : list num0 )                                            annotation (shown in Figure 11) that is very close to the one in
            precondition ∀i. −1 ≤ (b
                                   q [i]) ≤ 1                                     Figure 2 is needed to finish the proof. Hence, we just proved the
                                                                                  numerical Sparse Vector variant for (almost) free using LightDP.
  c1, c2, i : num0 ; T̃ , η1 : num1 ; η2 : numq[i]+η2 ≥T̃ ?2:0 ; η3 : num−b
                                                                          q [i]
                                                                                  Incorrect variants The numerical variant is also historically in-
 1    η1 := Lap (3/);
                                                                                  teresting since it fixes a bug in a very influential set of lecture notes
 2 T̃ := T + η1 ;                                                                 (Roth 2011); these lecture notes inadverantly re-used the same
 3 c1 := 0; c2 := 0; i := 0;
                                                                                  noise used for the “if” test (Line 7) instead of drawing new noise
 4 while (c1 < N)
 5      η2 := Lap (6N/);                                                         when outputting the noisy query answer. In other words, Lines 5-8
                                                                                  in Figure 1 are replaced with:
 6      if (q[i] + η2 ≥ T̃ ) then
 7         η3 := Lap (3N/);                                                             η2 := Lap (2N/);
 8         out:= (q[i]+η3 )::out;                                                        q̃ = q[i] + η2
 9         c1 := c1 + 1;                                                                 if (q̃ ≥ T̃ ) then
10      else                                                                                out:= (q̃)::out;
11         out:= 0::out;
                                                                                  For this incorrect variant, the refinement algorithm refines the type
12         c2 := c2 + 1;
13      i := i+1;                                                                 of q̃ to be qb[i] + α when q̃ is defined, where Γ(η2 ) = α. Moreover,
                                                                                  during type checking, ((q̃) :: out) generates a constraint (b
                                                                                                                                              q [i]+α =
 The transformed program, where underlined commands are added by the
                                                                                  0) by rule (T-C ONS ). Hence, it must be true that Γ(q̃) = num0
 type system. Only one annotation (loop invariant) is needed from the pro-
 grammer to verify the postcondition v ≤ : c1 ≤ N ∧v = 3 +c1× 3N  2
                                                                         .
                                                                                  and Γ(η2 ) = num−bq[i] after type inference. Moreover, after type
                                                                                  checking, η2 := Lap (2N/) is transformed to
 1     v := 0;
 2     havoc η1 ; v := v + /3;                                                                 (havoc η2 ; v := v + |b
                                                                                                                          q[i]|(/2N))
 3     T̃ := T + η1 ;                                                             However, we cannot prove that the incorrect variant is 0 -private for
 4     c1 := 0; c2 := 0; i := 0;                                                  any 0 . The reason is that v in the transformed program is clearly
 5     while (c1 < N)                                                             not bounded by any constant 0 : v increments by /2N in the
 6        havoc η2 ; v := v + (q[i] + η2 ≥ T̃ ?2 : 0) × /6N ;                  worst case in each loop iteration, but the number of iterations is
 7       if (q[i] + η2 ≥ T̃ ) then                                                unbounded (when most iterations take the “else” branch).
 8         havoc η3 ; v := v + |b
                                  q [i]| × /3N ;                                     The failure of a formal proof of the incorrect variant also sheds
 9         out:= (q[i]+η3 )::out;                                                 lights on how to fix it. For example, if we bound the number of
10         c1 := c1 + 1;                                                          iterations to be N , then the incorrect variant is fixed (though with a
11       else                                                                     different privacy cost).
12         out:= 0::out;
13         c2 := c2 + 1;                                                          6.2   Smart Summation
14       i := i+1
                                                                                  We next study a smart summation algorithm verified previously
           Figure 11. The Numerical Sparse Vector method.                         (with heavy annotations) in (Barthe et al. 2012, 2014). The pseudo
                                                                                  code, shown in Figure 12, is adapted from (Barthe et al. 2014). The
                                                                                  goal of this smart sum algorithm is to take a finite sequence of bits
 6.     Case Studies                                                              q[0], q[1], . . . , q[T ] and output a noisy
                                                                                                                           PT version of their partial sum
                                                                                  sequence: q[0], q[0] + q[1], . . . ,        i=0 q[i]. One naive approach
 6.1    Sparse Vector with Numerical Answers                                      is to add Laplace noise to each partial sum (partial implementation
 We first study a numerical variant of the Sparse Vector method. The              is shown in Figure 4). An alternative naive algorithm is to compute
 previous version (Figure 1), produces only two types of outputs for              a noisy bit q̃[i]
                                                                                                 PT= q[i]+Lap(1/) for each i and output q̃[0], q̃[0]+
 each query: true, meaning the query answer is probably above                     q̃[1], . . . ,     i=0 q̃[i]. However, in both approaches, the noise will
 the threshold; and false, meaning that it is probably below. The                 swamp the true counts.
 numerical variant, shown in Figure 11, replaces the output true                       A much smarter approach was proposed by Chan et al. (2011).
 with a noisy query answer. It does this by drawing fresh Laplace                 Intuitively, their algorithm groups q into nonoverlapping blocks
 noise and adding it to the query (Line 8).                                       of size M . So block G1 = {q[0], q[1], . . . , q[M − 1]}, G2 =
                                                                                  {q[M ], q[M +1], q[M +2], . . . , q[2M −1]}, etc. Then it maintains
 Verification using LightDP LightDP can easily verify this nu-                    2 levels of noisy counts: (1) the noisy bits q̃[i]
 merical variant from scratch, in a very similar way as verifying                                                                  P= q[i]+Lap(1/) for
                                                                                  each i, and (2) the noisy block sums G̃j = i∈Gj q[i] + Lap(1/)
 the Sparse Vector method. However, here we focus on another
 interesting scenario of using LightDP: the programmer (or algo-                  for each block. The partial sums are computed from these noisy
 rithm designer) has already verified the Sparse Vector method using              P` in the following way. Consider the sum of the first `+1
                                                                                  counts
                                                                                                                                                  `+1
                                                                                                                                                       bits:
 LightDP, and she is now exploring its variations. This is a common                   i=0 q[i].  We   can  represent `+1  =  xM  +c  where  x = b  M
                                                                                                                                                      c and
 scenario for algorithm designers. We show that since LightDP au-                 c = ` + 1 mod M . Hence, the noisy partial sum can be computed
 tomatically fills in most proof details, exploring variations of an              from the noisy sum of the first x blocks plus the remaining c noisy
                                                                                                                   c−1
 algorithm requires little effort.                                                bits: G̃1 + G̃2 + · · · + G̃x +
                                                                                                                    P
                                                                                                                       q̃[xB + j]. This algorithm is shown
     In particular, we assume the programmer has already obtained                                               j=0
 the (optimal) types for all local variables except η3 , and the loop             in Figure 12. The “if” branch keeps track of block boundaries and is
 invariant shown in Figure 2 from the verification of the Sparse                  responsible for summing up the noisy blocks. The “else” branch is
 Vector method. Hence, the type inference engine only needs to infer              responsible for adding in the remaining loose noisy bits (once there
 a type for η3 , which is trivially solved to be num−bq[i] . Moreover,            are enough loose bits to form a new block Gj , we use its noisy sum
 LightDP transforms the original program to the one on the bottom                 G̃j rather than the sum of its noisy bits).
 function S MART S UM (, M, T: num0 ; q: list num∗ )                        function P RIV B ERNOULLI (t : num∗ )
           returns (out : list num0 )                                                   returns b : bool
           precondition ∀i. −1 ≤ (b   q [i]) ≤ 1 ∧                                      precondition 0 ≤ t ≤ 1 ∧ 0 ≤ t + b
                                                                                                                         t≤1
                      (∀i. qb[i] 6= 0 ⇒ (∀j 6= i. qb[j] = 0))
                                                                             1     η := Uniform[0,1] ;
  next, n, i : num0 ; sum : num∗ ; η1 : num−sum−b
                                            c q [i] ; η2 : num−b
                                                               q [i]         2     if (η ≤ t) then
                                                                             3        b := true;
 1   next:=0; n:=0; i:=0; sum := 0;                                          4     else
 2   while i ≤ T                                                             5        b := false;
 3     if (i + 1) mod M = 0 then
                                                                             The transformed program where underlined commands are added by the
 4       η1 := Lap 1/;
                                                                             type system:
 5       n := n + sum + q[i] + η1 ;
 6       next:= n;                                                           1 v :=0;
 7       sum := 0;                                                           2 havoc η; v = v − log(1 + (η ≤ t)?(b   t ≥ 0?0 : (b
                                                                                                                                  t/t))
 8       out := next::out;                                                                                              t ≤ 0?0 : (b
                                                                                                                     : (b          t/t)));
 9     else
10       η2 := Lap 1/;                                                      3     if (η ≤ t) then
11       next:= next + q[i] + η2 ;                                           4       b := true;
12       sum := sum + q[i];                                                  5     else
13       out := next::out;                                                   6       b := false;
14     i := i+1;
 The transformed program, where underlined commands are added by the                       Figure 13. The PrivBernoulli algorithm.
 type system. Only one annotation (loop invariant) is needed from the pro-
 grammer to verify the postcondition v ≤ 2: (v + sd  um > 0 ⇒ ∀j ≥
 i. qb[j] = 0) ∧ (d
                  sum > 0 ⇒ v ≤ ) ∧ (d   sum ≤ 1.0) ∧ (v ≤ 2)             um > 0 ⇒ ∀j ≥ i. qb[j] = 0)). Using the loop invariant, we
                                                                             sd
 1 v = 0;                                                                   formally verified the desired postcondition v ≤ 2 using Dafny.
 2 next:=0, n:=0, i:= 0, sum:=0;sum              d := 0;
 3 while i ≤ T                                                               6.3    Categorical Outputs
 4         if (i + 1) mod M = 0 then                                         Until now, we have used the Laplace mechanism, which gener-
 5              havoc η1 ; v := v + |dsum + qb[i]|;
                                                                             ates numerical outputs, as the primary randomization tool for en-
 6              n := n + sum + q[i] + η1 ;                                   suring differential privacy. It might seem that categorical attributes
 7              next:= n;
 8              sum := 0;
                                                                             would require completely different techniques, but indeed, they can
 9              d := 0;
                sum                                                          be cleanly incorporated into LightDP with a new typing rule. We
10              out := next::out;
                                                                             briefly show how this can be done by considering a simple mech-
11         else                                                              anism that takes a private-data-dependent probability t and outputs
12              havoc η2 ; v := v + |bq [i]|;                             true with probability t and false with probability 1 − t. The al-
13              next:= next + q[i] + η2 ;                                    gorithm shown in Figure 13.
14              sum := sum + q[i];                                               The standard trick of generating an output true with probability
15              sum    d + |b
                d := sum        q [i]|;                                      t can be done by generating an uniform [0,1] random variable x and
16              out := next::out;                                            returning true if x ≤ t, and false otherwise. This trick converts
17         i := i+1;                                                         numerical randomness into categorical randomness with a notion
                                                                             of distance that can be aligned between executions under related
                 Figure 12. The SmartSum algorithm.                          databases. Generalizations to a larger output domain are routine
                                                                             and, in this way, can allow some instantiations of the exponential
                                                                             mechanism (McSherry and Talwar 2007).
     Assume for two adjacent databases, at most one query answer                 To calculate the privacy cost of aligning the binary output, we
 differs, and for that query, its distance is at most one (this adja-        need to add a single typing rule to capture the property of uniform
 cency assumption is provided as the precondition in function signa-         [0,1] distribution:
 ture). Hence, for queries that generate the same answer on adjacent                         Γ(η) = numη·d      −1<d≤0
 databases, no privacy cost is paid. However, privacy cost is paid
 twice to hide the query answers that differ: when the noisy sum for             Γ ` η := Uniform[0,1] * havoc[0,1] η; v = v − log(d + 1)
 the block containing that query is computed, and when the noisy                This rule requires that the random sample is aligned by a dis-
 version of that query is used. Hence informally, the SmartSum al-           tance of η · d for some d (i.e., we map η to (d + 1)η in the ran-
 gorithm satisfies 2-privacy where  is a function parameter.               domness alignment). Easy to check this mapping is injective. By
 Verification using LightDP LightDP successfully infers the type             property of uniform distribution, the privacy cost of any such as-
 annotations shown in the box under function signature in Figure 12.         signment is − log(d + 1) where −1 ≤ d ≤ 0.
 Since all type variables are only involved in equality constraints,            To integrate this typing rule and uniform distribution into
 only one solution exists. The transformed program is shown at the           LightDP, we need to establish that: 1) the faithfulness of the trans-
 bottom of Figure 12.                                                        formation, and 2) the uniform distribution satisfies Lemma 2. The
     By Theorem 2, to prove SmartSum is 2-private, it is sufficient         former is easy to check, and we establish the latter in the appendix.
 to verify that the postcondition v ≤ 2 holds for the transformed             With this new typing rule for uniform distribution, we can
 program. We notice that this program maintains the loop invariant           precisely compute the privacy cost of the algorithm in Figure 13
 shown in Figure 12. One observation is that once the privacy cost or        by providing the following type for η: Γ(η) = η · d where
 the distance of variable sum gets positive, the query that generates                           d = (η ≤ t)?(b
                                                                                                             t ≥ 0?0 : (b
                                                                                                                        t/t))
 different answers must have been handled already. Hence, rest
 queries must have identical answers on adjacent databases ((v +                                          :(t ≤ 0?0 : (t/t))
                                                                                                             b          b
During type checking, rule (T-OD OT ) checks the following con-                   heavier annotation burden since both relational and functional (e.g.,
straint for the branch condition η ≤ t ⇔ η + η · d ≤ t + bt, which                bounding privacy cost) properties are reasoned about in the trans-
can be discharged by a SMT solver. Hence, the algorithm is trans-                 formed program, while the former is completely and automatically
formed to the program at the bottom of Figure 13. By the fact that                handled by the type system of LightDP.
the newly added random source and typing rules satisfies Lemma 2,                     The notion of aligning randomness has been used in the re-
the privacy cost of this subtle example is provably bounded by the                cent coupling method (Barthe et al. 2016c,b). While the coupling
transformed cost formula in the transformed program 7 .                           method is capable of proving (, δ) privacy and it does not require
                                                                                  the injective assumption on the alignment, the cost of doing so is
                                                                                  the steep learning curve and heavy annotation burden. Technically,
7.    Related Work                                                                the coupling method reasons about privacy for each possible output
Type systems for differential privacy Fuzz (Reed and Pierce                       (or a set of outputs), while the alignment-based theory used in this
2010) and its successor DFuzz (Gaboardi et al. 2013) reason about                 paper aligns two program executions that will produce the same re-
the sensitivity (i.e., how much does a function magnify distances                 sults. The theory in this paper gives a simple proof, a light-weight
between inputs) of a program. DFuzz combines linear indexed                       type system, and clear insight behind the type system.
types and lightweight dependent types to allow rich sensitivity                   Other language-based methods for differential privacy Several
analysis. However, those systems rely on (without verify) external                dynamic tools exist for enforcing differential privacy. PINQ (Mc-
mechanisms (e.g., Laplace mechanism, Sparse Vector method) as                     Sherry 2009) tracks (at runtime) the privacy budget consumption,
trusted black boxes to release final query answers, without veri-                 and terminates the computation when the privacy budget is ex-
fying those black boxes. LightDP, on the other hand, verifies so-                 hausted. Airavat (Roy et al. 2010) is a MapReduce-based system
phisticated privacy-preserving mechanisms that releases those final               with a runtime monitor that enforces privacy policies controlled
answers. Sensitivity inference (D’Antoni et al. 2013) was proposed                by data providers. Recent work by Ebadi et al. (2015) proposed
in the context of Fuzz. While sensitivity inference shares the same               Personalised Differential Privacy (PDP), where each individual has
goal of minimizing type annotation and it also uses SMT solvers,                  its own personal privacy level and a dynamic system that imple-
the very different type system in LightDP brings unique challenges                ments PDP. There are also methods based on computing bisimu-
(Section 5.1) that do not present in Fuzz.                                        lations families for probabilistic automata (Tschantz et al. 2011;
    HOARe2 (Barthe et al. 2015) and its extension PrivInfer (Barthe               Xu et al. 2014). However, none of these techniques has the expres-
et al. 2016a) have the ability to relate a pair of expressions via                sive power to provide a tight privacy cost bound for sophisticated
relational assertions that appear as refinements in types. Hence,                 privacy-preserving algorithms.
they can verify mechanisms that privately release final query an-
swers as well as private Bayesian inference algorithms. However,
HOARe2 and PrivInfer incur heavy annotation burden on program-                    8.   Conclusions and Future Work
mers. Moreover, they can not deal with privacy-preserving algo-                   The increased usage and deployment of differentially private al-
rithms that go beyond the composition theorem (e.g., the Sparse                   gorithms underscores the need for formal verification methods to
Vector method).                                                                   ensure that personal information is not leaked due to mistakes or
                                                                                  carelessness. The ability to verify subtle algorithms should be cou-
Program logic for differential privacy Probabilistic relational                   pled with the ability to infer most of the proofs of correctness to
program logic (Barthe et al. 2012, 2013; Barthe and Olmedo 2013;                  reduce the programmer burden during the development and subse-
Barthe et al. 2016c,b) use custom relational logics to verify dif-                quent maintenance of a privacy-preserving code base.
ferential privacy. These systems have successfully verified privacy                    In this paper, we present a language with a lightweight type
for many advanced examples. However, only the very recent work                    system that allows us to separate privacy computation from the
by Barthe et al. (2016c,b) can verify the Sparse Vector method.                   alignment of random variables in hypothetical executions under
While these logics are expressive enough to prove (, δ) privacy,                 related databases. Thus enabling inference and search for proofs
the main difficulty with these approaches is that they use custom                 with the minimal privacy costs.
and complex logics that incurs steep learning curve and heavy an-                      These techniques allow us to verify (with much fewer annota-
notation burden. Moreover, ad hoc rules for loops are needed for                  tions) algorithms that were out of reach of the state of the art un-
many advanced examples.                                                           til recently. However, additional extensions are possible. The first
    The work by Barthe et al. (2014) transforms a probabilistic re-               challenge is to extend these methods to algorithms that use hid-
lational program to a nondeterministic program, where standard                    den private state to reduce privacy costs. One example is the noisy
Hoare logic can be used to reason about privacy. However, the fun-                max algorithm that adds noise to each query and returns the index
damental difference between that work and LightDP is that the for-                of the query with the largest noisy answer (although all noisy an-
mer cannot verify sophisticated algorithms where the composition                  swers are used in this computation, the fact that their values are
theorem falls short, since it lacks the power to express subtle de-               kept secret allows more refined reasoning to replace the composi-
pendency between privacy cost and memory state. Moreover, be-                     tion theorem). The second challenge is verifying subtle algorithms
neath the surface, that work and LightDP are built on very different              such as PrivTree (Zhang et al. 2016), in which intermediate pri-
principals and proof techniques. Further, their approach requires                 vacy costs depend on the data (hence cannot be released) but their
                                                                                  sum can be bounded in a data-independent way. This is another
7 We note that without LightDP, the precise calculation of privacy cost
                                                                                  case where the composition theorem can fail since it requires data-
is very difficult and error-prone. To show that the randomness alignment          independent privacy costs. Lastly, LightDP currently only verifies
cancels out the difference in the private-data-dependent probability t, we        -privacy, which has a nice point-wise property. We leave extending
need to analyze four cases. When outputting true and b      t ≥ 0, the related    LightDP to (, δ)-privacy as future work.
execution must output true as well (η ≤ t ∧ b        t ≥ 0 ⇒ η ≤ t+b        t).
When outputting true and b    t < 0, this alignment maps η to η(d + 1) =
                                                                                  Acknowledgments
η((t + bt)/t). Hence, true is the output in the related execution (η ≤ t ⇒
      t)/t ≤ t + b
η(t + b            t). Similar reasoning applies to the case outputting false     We thank Adam Smith, our shepherd Marco Gaboardi and anony-
too. Moreover, connecting this alignment to -privacy require is even more        mous reviewers for their helpful suggestions. This work was sup-
daunting by a paper-and-pencil proof.                                             ported by NSF grants CNS-1228669 and CCF-1566411.
References                                                                         ACM SIGSAC Conference on Computer and Communications Security,
                                                                                   CCS ’14, 2014.
A. Aiken and E. L. Wimmers. Type inclusion constraints and type inference.
   In FPLCA, pages 31–41, 1993.                                                 M. Gaboardi, A. Haeberlen, J. Hsu, A. Narayan, and B. C. Pierce. Lin-
G. Barthe and F. Olmedo. Beyond differential privacy: Composition the-             ear dependent types for differential privacy. In Proceedings of the 40th
   orems and relational logic for f-divergences between probabilistic pro-         Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-
   grams. In ICALP, pages 49–60, 2013.                                             ming Languages, POPL ’13, pages 357–370, 2013.
                                                                                A. Greenberg. Apple’s ‘differential privacy’ is about collecting your data
G. Barthe, B. Köpf, F. Olmedo, and S. Zanella Béguelin. Probabilistic re-        – but not Your data. Wired, https://www.wired.com/2016/
   lational reasoning for differential privacy. In Proceedings of the 39th         06/apples-differential-privacy-collecting-data/,
   Annual ACM SIGPLAN-SIGACT Symposium on Principles of Program-                   2016.
   ming Languages, pages 97–110, 2012.
                                                                                C. Haack and J. B. Wells. Type error slicing in implicitly typed higher-order
G. Barthe, G. Danezis, B. Grégoire, C. Kunz, and S. Zanella-Béguelin. Ver-
                                                                                   languages. Science of Computer Programming, 50(1–3):189–224, 2004.
   ified computational differential privacy with applications to smart me-
   tering. In 2013 IEEE 26th Computer Security Foundations Symposium,           D. Kifer and A. Machanavajjhala. Pufferfish: A framework for mathemat-
   pages 287–301, 2013.                                                            ical privacy definitions. ACM Trans. Database Syst., 39(1):3:1–3:36,
                                                                                   2014.
G. Barthe, M. Gaboardi, E. J. G. Arias, J. Hsu, C. Kunz, and P. Y. Strub.
   Proving differential privacy in hoare logic. In 2014 IEEE 27th Computer      D. Kozen. Semantics of probabilistic programs. Journal of Computer and
   Security Foundations Symposium, pages 411–424, 2014.                            System Sciences, 22(3):328 – 350, 1981.
G. Barthe, M. Gaboardi, E. J. G. Arias, J. Hsu, A. Roth, and P. Strub.          K. R. M. Leino. Dafny: An automatic program verifier for functional
   Higher-order approximate relational refinement types for mechanism              correctness. In Proceedings of the 16th International Conference on
   design and differential privacy. In POPL, 2015.                                 Logic for Programming, Artificial Intelligence, and Reasoning, pages
                                                                                   348–370, 2010.
G. Barthe, G. P. Farina, M. Gaboardi, E. J. G. Arias, A. Gordon, J. Hsu, and
   P.-Y. Strub. Differentially private bayesian programming. In Proceed-        M. Lyu, D. Su, and N. Li. Understanding the sparse vector technique for
   ings of the 2016 ACM SIGSAC Conference on Computer and Communi-                 differential privacy. https://arxiv.org/abs/1603.01699, 2016.
   cations Security, pages 68–79, 2016a.                                        A. Machanavajjhala, D. Kifer, J. Abowd, J. Gehrke, and L. Vilhuber. Pri-
G. Barthe, N. Fong, M. Gaboardi, B. Grégoire, J. Hsu, and P.-Y. Strub. Ad-        vacy: From theory to practice on the map. In Proceedings of the IEEE
   vanced probabilistic couplings for differential privacy. In Proceedings of      International Conference on Data Engineering (ICDE), pages 277–286,
   the 2016 ACM SIGSAC Conference on Computer and Communications                   2008.
   Security, pages 55–67, 2016b.                                                P. Martin-Löf. Intuitionistic type theory. Naples: Bibliopolis, 76, 1984.
G. Barthe, M. Gaboardi, B. Gregoire, J. Hsu, and P.-Y. Strub. Proving           F. McSherry and K. Talwar. Mechanism design via differential privacy.
   differential privacy via probabilistic couplings. In IEEE Symposium on          In Proceedings of the 48th Annual IEEE Symposium on Foundations of
   Logic in Computer Science (LICS), 2016c. To apprear.                            Computer Science, pages 94–103, 2007.
N. Bjørner and A.-D. Phan. νZ — maximal satisfaction with Z3. In                F. D. McSherry. Privacy integrated queries: An extensible platform for
   T. Kutsia and A. Voronkov, editors, 6th International Symposium on               privacy-preserving data analysis. In Proceedings of the 2009 ACM
   Symbolic Computation in Software Science (SCSS), volume 30 of EPiC               SIGMOD International Conference on Management of Data, pages 19–
   Series in Computing, pages 1–9, 2014.                                            30, 2009.
N. Bjørner, A.-D. Phan, and L. Fleckenstein. νZ — An Optimizing SMT             P. Mohan, A. Thakurta, E. Shi, D. Song, and D. Culler. Gupt: Privacy pre-
   Solver, pages 194–199. 2015.                                                     serving data analysis made easy. In Proceedings of the ACM SIGMOD
H. Chan, E. Shi, and D. Song. Private and continual release of statistics.          International Conference on Management of Data, 2012.
   ACM Transactions on Information and System Security, 14(3), 2011.            J. Reed and B. C. Pierce. Distance makes the types grow stronger: A calcu-
Y. Chen and A. Machanavajjhala. On the privacy properties of variants on            lus for differential privacy. In Proceedings of the 15th ACM SIGPLAN
   the sparse vector technique. http://arxiv.org/abs/1508.07306, 2015.              International Conference on Functional Programming, ICFP ’10, pages
L. D’Antoni, M. Gaboardi, E. J. Gallego Arias, A. Haeberlen, and B. Pierce.         157–168, 2010.
   Sensitivity analysis using type-based constraints. In Proceedings of the     A. Roth. The sparse vector technique. http://www.cis.upenn.
   1st Annual Workshop on Functional Programming Concepts in Domain-                edu/˜aaroth/courses/slides/Lecture11.pdf, 2011.
   specific Languages, pages 43–50, 2013.                                       I. Roy, S. Setty, A. Kilzer, V. Shmatikov, and E. Witchel. Airavat: Security
L. M. de Moura and N. Bjørner. Z3: An efficient SMT solver. In Conf.                and privacy for MapReduce. In NSDI, 2010.
   on Tools and Algorithms for the Construction and Analysis of Systems         M. C. Tschantz, D. Kaynar, and A. Datta. Formal verification of differential
   (TACAS), 2008.                                                                   privacy for interactive systems (extended abstract). Electron. Notes
C. Dwork and A. Roth. The algorithmic foundations of differential privacy.          Theor. Comput. Sci., 276:61–79, Sept. 2011.
   Foundations and Trends in Theoretical Computer Science, 9(3–4):211–
                                                                                M. Wand. A simple algorithm and proof for type inference. Fundamenta
   407, 2014. ISSN 1551-305X. doi: 10.1561/0400000042.
                                                                                    Informaticae, 10:115–122, 1987.
C. Dwork, K. Kenthapadi, F. McSherry, I. Mironov, and M. Naor. Our data,
                                                                                L. Xu, K. Chatzikokolakis, and H. Lin. Metrics for Differential Privacy in
   ourselves: Privacy via distributed noise generation. In EUROCRYPT,
                                                                                    Concurrent Systems, pages 199–215. 2014.
   pages 486–503, 2006a.
                                                                                D. Zhang and A. C. Myers. Toward general diagnosis of static errors. In
C. Dwork, F. McSherry, K. Nissim, and A. Smith. Calibrating noise to
                                                                                    ACM Symposium on Principles of Programming Languages (POPL),
   sensitivity in private data analysis. In TCC, 2006b.
                                                                                    pages 569–581, Jan. 2014.
H. Ebadi, D. Sands, and G. Schneider. Differential privacy: Now it’s getting
                                                                                J. Zhang, X. Xiao, and X. Xie. Privtree: A differentially private algorithm
   personal. In POPL, 2015.
                                                                                    for hierarchical decompositions. In SIGMOD, 2016.
U. Erlingsson, V. Pihur, and A. Korolova. Rappor: Randomized aggregat-
   able privacy-preserving ordinal response. In Proceedings of the 2014
Appendix                                                                       When Γ(x) = B∗ , Γ ` x : Bxb . Hence, m01 (x) + m01 (b   x) =
                                                                               JeKm1 + JdKm1 , where Γ(e) = d, by the extended seman-
A.     Soundness Proof                                                         tics. By Lemma 4, this is identical to JeKm2 , which is m02 (x)
In the source language semantics (Figure 5), the variable that a               by the semantics.
star-typed variable depends on (e.g., sd  um in Figure 4) is invisible.     Second, we show m01 (y) + JdKm01 = m02 (y), where Γ ` y : d
We first extend the semantics to make the manipulation of such              for y ∈ dom(Γ) ∧ y 6= x. When y ∈ Var, its type cannot depend
invisible variables explicit, by the following rule for assignments:        on x, which is mutable. So the desired result is true. For η ∈ H,
                                   x}) when Γ(x) = num∗ ,
Jx := eKm = unit (m{JeKm /x}{JdKm /b                                        its type only depends on the memory state when η is used. So
                                                                            the desired result is true as well.
where Γ(e) = d.                                                           • Case if e then c1 else c2 : by typing rule, Γ ` e : bool0 . By
   It is straightforward to check that the extended semantics (pa-
                                                                            Lemma 4, JeKm1 = JeKm2 . Hence, the same branch is taken in
rameterized on the type system) is consistent with the original se-
                                                                            m1 and m2 . Desired result is true by induction hypothesis.
mantics in Figure 5, as it does not change the distribution on the
                                                                          • Case c1 ; c2 : For any m such that Jc1 ; c2 Km1 (m) 6= 0, there
variables that are visible in the source program. The extended se-
mantics is needed to close the gap between the source language and          exists some m0 such that
the one that formal reasoning is applied on.                                              Jc1 Km1 (m0 ) 6= 0 ∧ Jc2 Km0 (m) 6= 0
   Next, we prove a few auxiliary lemmas.
                                                                            By induction hypothesis, we have
Lemma 3.
                                                                                      Jc1 Km1 (m0 ) ≤ exp(1 )Jc1 KΓ(m1 ) (Γ(m0 ))
  ∀m1 , m2 , Γ s.t. m1 Γ m2 , we have
                        ∀m. unit m1 (m) = unit m2 (Γ(m))                                Jc2 Km0 (m) ≤ exp(2 )Jc2 KΓ(m0 ) (Γ(m))
                                                                                                     0
                                                                            where 1 = max(c01 m                     m
                                                                                                m1 ) and 2 = max(c2 m0 ). Hence,
Proof. By the fact that Γ is a function.
                                                                               Jc1 Km1 (m0 ) · Jc2 Km0 (m) ≤
Lemma 4 (Expression).
                                                                                    exp(1 + 2 )Jc1 KΓ(m1 ) (Γ(m0 )) · Jc2 KΓ(m0 ) (Γ(m))
  ∀e, m1 , m2 , Γ s.t. m1 Γ m2 ∧ Γ ` e : Bd , we have
                                                                            Notice that m0 ] (1 ) ∈ Jc1 Km1 ](0) and m ] (2 ) ∈ Jc2 Km0 ](0)
                                        JeKm1 + JdKm1 = JeKm2               since 1 and 2 maximize privacy costs among consistent exe-
                                                                            cutions by definition. Hence, m ] (1 + 2 ) ∈ Jc01 ; c02 Km1 ](0) .
Proof. Induction on the structure of e. Interesting cases are follows.      Therefore, 1 + 2 ≤ max(c1 ; c2 m  m1 ).
    When e is x or η, result is true by the definition of m1 Γ m2 .         So for any m,
    When e is e1 ⊕ e2 , let Jei Km1 = vi , Jei Km2 = vi0 and Γ ` ei :                          X
  i
Bdi for i ∈ {1, 2}. Then by typing rule, we have d = d1 + d2 . By           Jc1 ; c2 Km1 (m) =     Jc1 Km1 (m0 ) · Jc2 Km0 (m)
induction hypothesis, we have vi0 = vi + di , where di = Jdi Km1 .                              m0

Hence, JeKm2 = v10 ⊕ v20 = (v1 + d1 ) ⊕ (v2 + d2 ) = (v1 ⊕ v2 ) +
                                                                                                          X
                                                                                             ≤ exp(0 )    Jc1 KΓ(m1 ) (Γ(m0 )) · Jc2 KΓ(m0 ) (Γ(m))
(d1 ⊕ d2 ) = Je1 ⊕ e2 Km1 + Jd1 ⊕ d2 Km1 = JeKm1 + JdKm1 .                                                m0
    When e = e1         e2 , let Γ ` ei : Bdi i for i ∈ {1, 2}.                                           X
Then by induction hypothesis, we have Jei Km1 + Jdi Km1 =                                    ≤ exp(0 )    Jc1 KΓ(m1 ) (m0 ) · Jc2 Km0 (Γ(m))
                                                                                                          m0
Jei Km2 for i ∈ {1, 2}. By rule (T-OD OT ), for any memory m,
Je1 e2 Km = J(e1 + d1 ) (e2 + d2 )Km . Hence, Je1 e2 Km1 =                                   ≤ exp(0 )Jc1 ; c2 Km2 (Γ(m))
J(e1 + d1 ) (e2 + d2 )Km1 = Je1 + d1 Km1             Je2 + d2 Km1 =
Je1 Km2 Je2 Km2 = Je1 e2 Km2 .                                              where 0 = max(c1 ; c2 m   m1 ). Notice that the change of vari-
                                                                            able in the second to last inequality only holds when Γ is an
                                                                            injective (but not necessarily onto) mapping, which is true due
Proof of Lemma 2
                                                                            to the assumption ` Γ.
  ∀c, c0 , m1 , m2 , m, Γ. ` Γ ∧ Γ ` c * c0 ∧ m1 Γ m2 , we have           • Case while e do c: let W = while e do c. By typing rule,
                                                                            Γ ` e : bool0 . Hence, JeKm01 = JeKm02 for any m01 Γ m02 .
                 JcKm1 (m) ≤ exp(max(c0 m
                                         m1 ))JcKm2 (Γ(m))                  We proceed by by natural induction on the number of loop
                                                                            iterations (denoted by i) under m1 .
Proof. By structural induction on c.                                        When i = 0, JbKm1 = false. So JbKm2 = false since
 • Case skip: c0 = skip by typing rule. Hence, max(c0 m
                                                                            m1 Γ m2 . By semantics, JW Km1 = unit m1 and JW Km2 =
                                                       m1 ) =
                                                                            unit m2 , and max(W m      m1 ) = 0. Desired result is true by
     0. Desired result is true by Lemma 3 and the semantics of skip.
                                                                            Lemma 3.
 • Case x := e: by the transformation, we have max(c0 m
                                                       m1 ) = 0.            Consider i = j + 1. JbKm1 = true. So JbKm2 = true since
     Hence, by the semantics and Lemma 3, it is sufficient to show          m1 Γ m2 . By semantics, JW Kmi = Jc; W Kmi for i ∈ {1, 2},
     that the memories after the assignment are related by Γ.               and the latter W iterates for j times. By induction hypothesis
     We first show m01 (x) + JdKm01 = m02 (x).                              and a similar argument as the sequential case, JW Km1 (m) ≤
        When Γ(x) = Bd , we need to show that m01 Γ m02 where               exp(max(W m    m1 )JW Km2 (Γ(m)).
        m01 = m1 {JeKm1 /x} and m02 = m2 {JeKm2 /x} by the                • Case η := Lap r: let µr = Lap r. Since µr is the Laplace
        semantics. By typing rule, we have Γ ` e : Bd as well.              distribution with a scale factor of r, we have
        By Lemma 4, JeKm1 + JdKm1 = JeKm2 . Hence, we have
        m01 (x) + JdKm1 = m02 (x). Since d may only depend on im-                     ∀v, d ∈ R. µr (v) ≤ exp(|d| × r)µr (v + d)
        mutable variables in this case, JdKm1 = JdKm01 . So m01 (x)+        When @v. m = m1 {v/η} , Jη := Lap rKm1 (m) = 0 by the
        JdKm01 = m02 (x) as desired.                                        semantics. Hence, desired inequality is trivial.
     When m = m1 {v/η} for some constant v, we have for any              semantics of commands are formalized as follows.
     d ∈ R,                                                                               JskipKm = {m}
                          Jη := Lap rKm1 (m)                                             Jx := eKm = {m{JeKm /x}}
                        = µr (v)                                                       Jhavoc xKm = ∪r∈R {m{r/x}}
                        ≤ exp(|d| · r)µr (v + d)                                        Jc1 ; c2 Km = ∪m0 ∈Jc1 Km Jc2 Km0
     Let Γ(η) = numd and JdKm = d for some constant d. Since
                                                                                                      (
                                                                                                       Jc1 Km if JeKm = true
     m1 Γ m2 , m1 {v/η} Γ m2 {v + d/η}. That is, Γ(m) =                  Jif e then c1 else c2 Km =
     m2 {v + d/η}. By the semantics,                                                                   Jc2 Km if JeKm = false

      Jη := Lap rKm2 (Γ(m)) = Jη := Lap rKm2 (m2 {v + d/η})                       Jwhile e do cKm = w∗ m
                               = µr (v + d)                                              where w∗ = f ix(λf. λm.if JeKm = true

     Hence, we have                                                                                    then (∪m0 ∈JcKm f m0 ) else {m})
                                                                                    Jc; return eKm = ∪m0 ∈JcKm {JeKm0 }
      Jη := Lap rKm1 (m) ≤ exp(|d| · r)Jη := Lap rKm2 (Γ(m))
                                                                           Accordingly, the Hoare logic rules for the target language is
     when m = m1 {v/η} for some constant v too. By the typing            mostly standard, summarized in Figure 14.
     rule (T-L APLACE ), the transformed program is (havoc η; v :=
     v + |d| · r). Hence, max(c01 m
                                    m0 ) = J|d| · rKm = |JdKm | · r =
     |d| · r. Therefore, we showed that                                  C.     Uniform Distribution
                                                                         Lemma 5 (UniformDist). The following typing rule is sound w.r.t.
       Jη := Lap rKm1 (m) ≤                                              Lemma 2:
                      exp(max(c01 m
                                   m0 ))Jη := Lap rKm2 (Γ(m))                         Γ(η) = numη·d       −1<d≤0
                                                                          Γ ` η := Uniform[0,1] * havoc[0,1] η; v = v − log(d + 1)

                                                                         Proof. When @v. m = m1 {v/η} or m(η) < −1 or m(η) > 1,
Proof of Theorem 2                                                       Jη := Uniform[0,1] Km1 (m) = 0 by the semantics. Hence, desired
  ∀Γ, c, c0 , x, . ` Γ∧Γ ` (c; return e) * (c0 ; return e) then         inequality is trivial.
                                                                            When m = m1 {v/η} for some −1 ≤ v ≤ 1. Let µ =
                                            c0 ⇒ c is -private        Uniform[0,1] , d = JdKm . Notice that by typing rule d ≤ 0. So
                                                                         d ≤ 0. We have
Proof. By the soundness theorem (Theorem 1), we have for any in-
                                                                                           Jη := Uniform[0,1] Km1 (m)
jective Γ, m1 Γ m2 , ∀S ⊆ M, JcKm1 (S) ≤ exp()JcKm2 (Γ(S)).
For clarity, we stress that all sets are over distinct elements (as we                   = µ(v)
have assumed throughout this paper). Let P = (c; return e). By                             Z 1
typing rule (T-R ETURN ), the return type B must be either num or                        =      1{x≤v} dx
bool, and its distance must be zero. By semantics, for any value                             0
                                                                                           Z 1
set V ⊆ B,                                                                               =      1{(d+1)x≤(d+1)v} dx
         JP Km1 (V ) = JcKm1 ({m | JeKm ∈ V })                    (1)                        0
                                                                                           Z 1+d
                     ≤ exp()JcKm2 ({Γ(m) | JeKm ∈ V })           (2)                               1
                                                                                         =              1{x≤(d+1)v} dx
                                                                                             0    1+d
                      ≤ exp()JcKm2 ({m | JeKm ∈ V })             (3)                             Z 1
                                                                                              1
                      = exp()JP Km2 (V )                         (4)                    ≤            1{x≤(d+1)v} dx
                                                                                           1+d 0
where inequality (2) is true due to Theorem 1 (the application                           = exp(− log(d + 1))µ(v + v · d)
of which requires the injective assumption). For inequality (3),
consider any m0 ∈ {Γ(m) | JeKm ∈ V }. It must be true that                    Since m1 Γ m2 , we have m1 {v/η} Γ m2 {(v + v · d)/η}.Hence,
m0 = Γ(m) ∧ JeKm ∈ V for some m ∈ M. Due to Lemma 4,
JeKm = JeKΓ(m) (the distance of e must be 0). That is, JeKm =              Jη := Uniform[0,1] Km1 (m) ≤
v ⇔ JeKΓ(m) = v for any v. Hence,                                                   exp(− log(d + 1))Jη := Uniform[0,1] Km2 (Γ(m))
            m0 = Γ(m) ∧ JeKm ∈ V for some m ∈ M                             By the transformation, Uniform[0,1] * havoc[0,1] η; v =
                                                                         v − log(d + 1), where Γ(η) = η · d. Hence, max(c01 m
                                                                                                                              m0 ) =
is the same as                                                           J− log(d + 1)Km1 {v/η} = − log(d + 1). Therefore,
 m0 = m00 ∧ JeKm00 ∈ V for some m ∈ M, where m00 = Γ(m)
                                                                           Jη := Uniform[0,1] Km1 (m) ≤
Since m00 ∈ M, m0 ∈ {m | JeKm ∈ V }. Hence, the inequality (3)
holds. We note that (3) is not an equality in general since Γ might                   exp(max(c01 m
                                                                                                   m0 ))Jη := Uniform[0,1] Km2 (Γ(m))

not be a surjection.
   Therefore, by definition of differential privacy, c is -private.


B.     Formal Semantics for the Target Language
The denotational semantics interprets a command c in the target
language (Figure 7) as a function JcK : M → P(M). The
             (H-S KIP )                            (H-A SGN )
{Φ}skip{Φ}                  {Φ{e/x}}x := e{Φ}

                                     (H AVOC )
             {∀x. Φ}havoc (x){Φ}

           {Ψ}c1 {Φ0 } {Φ0 }c2 {Φ}
                                   (H-S EQ )
               {Ψ}c1 ; c2 {Φ}

                                 (H-R ETURN )
             {Φ}return e{Φ}

       {e ∧ Ψ}c1 {Φ}    {¬e ∧ Ψ}c2 {Φ}
                                       (H-I F )
          {Ψ}if e then c1 else c2 {Φ}

     Ψ⇒I    {I ∧ e}c{I}   I⇒Φ
                              (H-W HILE )
        {Ψ}while e do c{Φ}

   Figure 14. Hoare logic rules for the target language.
