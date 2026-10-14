                                            Proving Differential Privacy with Shadow Execution
                                                       Yuxin Wang                                  Zeyu Ding                            Guanhong Wang
                                               Pennsylvania State University              Pennsylvania State University            Pennsylvania State University
                                                 University Park, PA, USA                   University Park, PA, USA                 University Park, PA, USA
                                                    yxwang@psu.edu                              zyding@psu.edu                          gpw5092@psu.edu

                                                                             Daniel Kifer                          Danfeng Zhang
                                                                    Pennsylvania State University            Pennsylvania State University
                                                                      University Park, PA, USA                 University Park, PA, USA
                                                                        dkifer@cse.psu.edu                       zhang@cse.psu.edu

                                        Abstract                                                           expressiveness and usability by providing verification tools
arXiv:1903.12254v2 [cs.PL] 1 Jul 2019




                                        Recent work on formal verification of differential privacy         that infer most (if not all) of the proof of privacy. The bench-
                                        shows a trend toward usability and expressiveness – gener-         mark algorithms for this task were Sparse Vector [21, 30] and
                                        ating a correctness proof of sophisticated algorithm while         Report Noisy Max [21]. LightDP [42] was the first system
                                        minimizing the annotation burden on programmers. Some-             that could verify Sparse Vector with very few annotations,
                                        times, combining those two requires substantial changes to         but it could not verify tight privacy bounds on Report Noisy
                                        program logics: one recent paper is able to verify Report          Max [21]. It is believed that proofs using randomness align-
                                        Noisy Max automatically, but it involves a complex verifica-       ment, the proof technique that underpins LightDP, are often
                                        tion system using customized program logics and verifiers.         simpler, while approximate coupling, the proof technique that
                                           In this paper, we propose a new proof technique, called         underpins [6–10], seems to be more expressive [2]. Subse-
                                        shadow execution, and embed it into a language called Shad-        quently, Albarghouthi and Hsu [2] produced the first fully
                                        owDP. ShadowDP uses shadow execution to generate proofs            automated system that verifies both Sparse Vector and Re-
                                        of differential privacy with very few programmer annota-           port Noisy Max. Although this new system takes inspiration
                                        tions and without relying on customized logics and verifiers.      from randomness alignment to simplify approximate cou-
                                        In addition to verifying Report Noisy Max, we show that it         pling proofs, its verification system still involves challenging
                                        can verify a new variant of Sparse Vector that reports the gap     features such as first-order Horn clauses and probabilistic
                                        between some noisy query answers and the noisy threshold.          constraints; it takes minutes to verify simple algorithms. The
                                        Moreover, ShadowDP reduces the complexity of verification:         complex verification system also prevents it from reusing
                                        for all of the algorithms we have evaluated, type checking         off-the-shelf verification tools.
                                        and verification in total takes at most 3 seconds, while prior        In this paper, we present ShadowDP, a language for veri-
                                        work takes minutes on the same algorithms.                         fying differentially private algorithms. It is based on a new
                                                                                                           proof technique called “shadow execution”, which enables
                                        CCS Concepts • Software and its engineering → For-                 language-based proofs based on standard program logics.
                                        mal software verification.                                         Built on randomness alignment, it transforms a probabilistic
                                        Keywords Differential privacy; dependent types                     program into a program in which the privacy cost is explicit;
                                                                                                           so that the target program can be readily verified by off-
                                        1    Introduction                                                  the-shelf verification tools. However, unlike LightDP, it can
                                                                                                           verify more challenging algorithms such as Report Noisy
                                        Differential privacy is increasingly being used in industry
                                                                                                           Max and a novel variant of Sparse Vector called Difference
                                        [23, 28, 38] and government agencies [1] to provide statis-
                                                                                                           Sparse Vector. We show that with minimum annotations,
                                        tical information about groups of people without violating
                                                                                                           challenging algorithms that took minutes to verify by [2]
                                        their privacy. Due to the prevalence of errors in published
                                                                                                           (excluding proof synthesis time) now can be verified within
                                        algorithms and code [30], formal verification of differential
                                                                                                           3 seconds with an off-the-shelf model checker.
                                        privacy is critical to its success.
                                                                                                              One extra benefit of this approach based on randomness
                                           The initial line of work on formal verification for differ-
                                                                                                           alignment is that the transformed program can also be ana-
                                        ential privacy (e.g., [6–10]) was concerned with increasing
                                                                                                           lyzed by standard symbolic executors. This appears to be an
                                        expressiveness. A parallel line of work (e.g., [32, 34, 36, 43])
                                                                                                           important property in light of recent work on detecting coun-
                                        focuses more on usability – on developing platforms that
                                                                                                           terexamples for buggy programs [12, 18, 24, 25]. Producing
                                        keep track of the privacy cost of an algorithm while limiting
                                                                                                           a transformed program that can be used for verification of
                                        the types of algorithms that users can produce.
                                                                                                           correct programs and bug-finding for incorrect programs is
                                           A recent line of work (most notably LightDP [42] and
                                        Synthesizing Coupling Proofs [2]) has sought to combine
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

one aspect that is of independent interest (however, we leave                     Definition 1 (Pure Differential privacy). Let ϵ ≥ 0. A proba-
this application of transformed programs to future work).                         bilistic computation M : A → B is ϵ-differentially private with
   In summary, this paper makes the following contributions:                      respect to an adjacency relation Ψ if for every pair of inputs
 1. Shadow execution, a new proof technique for differential                      a 1 , a 2 ∈ A such that a 1 Ψa 2 , and every output subset E ⊆ B,
    privacy (Section 2.4).                                                                         P(M(a 1 ) ∈ E) ≤ e ϵ P(M(a 2 ) ∈ E).
 2. ShadowDP, a new imperative language (Section 3) with
                                                                                  2.2   Randomness Alignment
    a flow-sensitive type system (Section 4) for verifying
    sophisticated privacy-preserving algorithms.                                  Randomness Alignment [42] is a simple yet powerful tech-
 3. A formal proof that the verification of the transformed                       nique to prove differential privacy. Here, we illustrate the
    program by ShadowDP implies that the source code is                           key idea with a fundamental mechanism for satisfying dif-
    ϵ-differentially private (Section 5).                                         ferential privacy–the Laplace Mechanism [31].
 4. Case studies on sophisticated algorithms showing that                            Following the notations in Section 2.1, we consider an
    verifying privacy-preserving algorithms using ShadowDP                        arbitrary pair of query answers a 1 and a 2 that differ by at
    requires little programmer annotation burden and verifi-                      most 1, i.e., −1 ≤ a 1 − a 2 = c ≤ 1. The Laplace Mechanism
    cation time (Section 6).                                                      (denoted as M) simply releases a + η, where η is a random
 5. Verification of a variant of Sparse Vector Technique that                     noise sampled from the Laplace distribution of mean 0 and
    releases the difference between noisy query answers and                       scale 1/ϵ; we use p1/ϵ to denote its density function. The goal
    a noisy threshold at the same privacy level as the original                   of randomness alignment is to “align” the random noise in
    algorithm [21, 30]. To the best of our knowledge, this                        two executions M(a 1 ) and M(a 2 ), such that M(a 1 ) = M(a 2 ),
    variant has not been studied before.                                          with a corresponding privacy cost. To do so, we create an
                                                                                  injective function f : R → R that maps η to η + c. Obviously,
2     Preliminaries and Illustrating Example                                      f is an alignment since a 1 + η = a 2 + f (η) for any a 1 , a 2 .
                                                                                  Then for an arbitrary set of outputs E ⊆ R, we have:
2.1    Differential Privacy                                                                               Õ                    Õ
                                                                                      P(M(a 1 ) ∈ E) =           p1/ϵ (η) ≤           p1/ϵ (η)
Differential privacy is now considered a gold standard in
                                                                                                        η |a 1 +η ∈E                  η |a 2 +f (η)∈E
privacy protections after recent high profile adoptions [1,
                                                                                                           ϵ
                                                                                                                    Õ
23, 28, 38]. There are currently several popular variants of                                          ≤e                         p1/ϵ (f (η))
differential privacy [13, 19, 20, 33]. In this paper, we focus on                                              η |a 2 +f (η)∈E

                                                                                                      = eϵ                    p1/ϵ (η) = e ϵ P(M(a 2 ) ∈ E)
                                                                                                                  Õ
the verification of algorithms that satisfy pure differential
privacy [20], which has several key advantages – it is the                                                     η |a 2 +η ∈E
strongest one among them, the most popular one, and the
easiest to explain to non-technical end-users [35].                               The first inequality is by the definition of f : a 1 + η ∈ E =⇒
   Differential privacy requires an algorithm to inject care-                     a 2 + f (η) ∈ E. The e ϵ factor results from the fact that p1/ϵ (η +
                                                                                  c) p1/ϵ (η) ≤ e |c | ·ϵ ≤ e ϵ , when the Laplace distribution has
                                                                                     
fully calibrated random noise during its computation. The
purpose of the noise is to hide the effect of any person’s                        scale 1/ϵ. The second to last equality is by change of variable
record on the output of the algorithm. In order to present the                    from f (η) to η in the summation, using the injectivity of f .
formal definition, we first define the set of sub-distributions                       In general, let H ∈ Rn be the random noise vector that a
over a discrete set A, written Dist(A), as the set of functions                   mechanism M uses. A randomness alignment for a 1 Ψa 2 is a
                                                                                  function f : Rn → Rn such that:
                           Í
µ : A → [0, 1], such that a ∈A µ(a) ≤ 1. When applied to an
                                   Í
event E ⊆ A, we define µ(E) ≜ e ∈E µ(e). 1                                         1. M(a 2 ) with noise f (H ) outputs the same result as M(a 1 )
   Differential privacy relies on the notion of adjacent databases                    with noise H (hence the name Randomness Alignment).
(e.g., pairs of databases that differ on one record). Since                        2. f is injective (this is to allow change of variables).
differentially-private algorithms sometimes operate on query
results from databases, we abstract adjacent databases as an                      2.3   The Report Noisy Max Algorithm
adjacency relation Ψ ⊆ A × A on input query answers. For                          To illustrate the challenges in proving differential privacy,
differential privacy, the most commonly used relations are:                       we consider the Report Noisy Max algorithm [21], whose
(1) each query answer may differ by at most n (for some                           source code is shown on the top of Figure 1. It can be used
number n), and (2) at most one query answer may differ, and                       as a building block in algorithms that iteratively generate
that query answer differs by at most n. This is also known                        differentially private synthetic data by finding (with high
as sensitivity of the queries.                                                    probability) the identity of the query for which the synthetic
                                                                                  data currently has the largest error [26].
1 As is standard in this line of work (e.g., [8, 42]), we assume a sub-              The algorithm takes a list q of query answers, each of
distribution instead of a distribution, since sub-distribution gives rise to an   which differs by at most 1 if the underlying database is re-
elegant program semantics in face of non-terminating programs [29].               placed with an adjacent one. The goal is to return the index
Proving Differential Privacy with Shadow Execution                                     PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

function NoisyMax (ϵ, size : num ⟨0,0⟩ ; q : list num ⟨∗,∗⟩ )       Informal proof using randomness alignment Proofs of
          returns max : num ⟨0,∗⟩                                   correctness of Report Noisy Max can be found in [21]. We will
                                                                    start with an informal correctness argument, based on the
 precondition ∀i ≥ 0. − 1 ≤ b            q† [i] = b
                            q◦ [i] ≤ 1 ∧ b        q◦ [i]            randomness alignment technique (Section 2.2), to illustrate
                                                                    subtleties involved in the proof.
 1  i := 0; bq := 0; max := 0;
 2  while ( i < size )                                                 Consider the following two databases D 1 , D 2 that differ
                                                                    on one record, and their corresponding query answers:
3       η := Lap (2/ϵ) , Ω ? † : ◦ , Ω ? 2 : 0 ;
4       if ( q [ i ] + η > bq ∨ i = 0)                                             D1 :      q[0] = 1,       q[1] = 2,        q[2] = 2
5          max := i;
6          bq := q[i] + η;                                                         D2 :      q[0] = 2,       q[1] = 1,        q[2] = 2
7       i := i + 1;
                                                                    Suppose in one execution on D 1 , the noise added to q[0], q[1],
The transformed program (slightly simplified for readability),
where underlined commands are added by the type system:             q[2] is α 0(1) = 1, α 1(1) = 2, α 2(1) = 1, respectively. In this case,
1 vϵ := 0;                                                          the noisy query answers are q[0] + α 0(1) = 2, q[1] + α 1(1) = 4,
2 i := 0; bq := 0; max := 0;                                        q[2] + α 2(1) = 3 and so the algorithm returns 1, which is the
   c◦ := 0; bq
3 bq             c† := 0;                                           index of the maximum noise query answer of 4.
 4   while ( i < size )
 5      assert (i < size);                                          Aligning randomness As shown in Section 2.2, we need
 6      havoc η; vϵ := Ω ? (0 + ϵ) : (vϵ + 0);                      to create an injective function of random bits in D 1 to ran-
 7      if ( q [ i ] + η > bq ∨ i = 0)
                                                                    dom bits in D 2 to make the output the same. Recall that
                                                  †                 α 0(1) , α 1(1) , α 2(1) are the noise added to D 1 , now let α 0(2) , α 1(2) , α 2(2)
 8        assert (q[i] + bq◦ [i] + η + 2 > bq + c
                                                bq ∨ i = 0);
                                                                    be the noise added to the queries q[0], q[1], q[2] in D 2 , re-
 9         max := i;
                                                                    spectively. Consider the following injective function: for any
10        c† := bq + c
          bq
                           †
                         bq - (q[i] + η);                           query except for q[1], use the same noise as on D 1 ; add 2 to
11         bq := q[i] + η;                                          the noise used for q[1] (i.e., α 1(2) = α 1(1) + 2).
             ◦
12        bq := b
          c       q◦ [i] + 2;                                           In our running example, execution on D 2 with this align-
13      else
                                                      ◦
                                                                    ment function would result in noisy query answers q[0] +
14        assert (¬(q[i] + b  q◦ [i] + η + 0 > bq + c
                                                    bq ∨ i = 0));   α 0(2) = 3, q[1] + α 1(2) = 5, q[2] + α 2(2) = 3. Hence, the output
15      // shadow execution                                         once again is 1, the index of query answer 5.
                                         †
16                 q† [i] + η > bq + c
        if (q[i] + b                  bq ∨ i = 0)                       In fact, we can prove that under this alignment, every exe-
17
            †
                       q† [i] + η − bq;
          bq := q[i] + b
          c                                                         cution on D 1 where 1 is returned would result in an execution
                                                                    on D 2 that produces the same answer due to two facts:
18      i := i + 1;
                                                                     1. On D 1 , q[1] + α 1(1) has the maximum value.
Figure 1. Verifying Report Noisy Max with ShadowDP. Here,
q is a list of query answers from a database, and max is the         2. On D 2 , q[1] + α 1(2) is greater than q[1] + α 1(1) + 1 on D 1
query index of the maximum query with Laplace noise gener-              due to α 1(2) = α 1(1) + 2 and the adjacency assumption.
ated at line 3. To verify the algorithm on the top, a program-         Hence, q[1] + α 1(2) on D 2 is greater than q[i] + α i(1) + 1 on
mer provides function specification as well as annotation for       D 1 for any i. By the adjacency assumption, that is the same
sampling command (annotations are shown in gray, where
                                                                    as q[1] + α 1(2) is greater than any q[i] + α i(2) on D 2 . Hence,
Ω represents the branch condition). ShadowDP checks the
                                                                    based on the same argument in Section 2.2, we can prove
source code and generates the transformed code (at the bot-
                                                                    that the Report Noisy Max algorithm is ϵ-private.
tom), which can be verified with off-the-shelf verifiers.
                                                                    Challenges Unfortunately, the alignment function above
of the largest query answer (as accurately as possible subject      only applies to executions on D 1 where index 1 is returned.
to privacy constraints).                                            If there is one more query q[3] = 4 and the execution gets
   To achieve differential privacy, the algorithm adds appro-       noise α 3(1) = 1 for that query, the execution on D 1 will return
priate Laplace noise to each query. Here, Lap (2/ϵ) draws           index 3 instead of 1. To align randomness on D 2 , we need
one sample from the Laplace distribution with mean zero             to construct a different alignment function (following the
and a scale factor (2/ϵ). For privacy, the algorithm uses the       construction above) that adds noise in the following way:
noisy query answer (q[i] + η) rather than the true query an-        for any query except for q[3], use the same noise as on D 1 ;
swer (q[i]) to compute and return the index of the maximum          add 2 to the noise used for q[3] (i.e., α 3(2) = α 3(1) + 2). In other
(noisy) query answer. Note that the return value is listed          words, to carry out the proof, the alignment for each query
right below the function signature in the source code.              depends on the queries and noise yet to happen in the future.
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

         D1:      q[0]=1    q[1]=2      q[2]=2      q[3]=4            language, we propose ShadowDP. We illustrate the key com-
        noise     α0(1)=1   α1(1)=2      α2(1)=1     α3(1)=1          ponents of ShadowDP in this section, as shown in Figure 1,
         D2:      q[0]=2    q[1]=1      q[2]=2      q[3]=4            and detail all components in the rest of this paper.
       shadow                                                            Similar to LightDP [42], ShadowDP embeds randomness
      execution   α0(†)=1    α1(†)=2     α2(†)=1     α3(†)=1
                                                                      alignments into types. In particular, each numerical variable
      alignment   α0(2)=3   α1(2)=4      α2(2)=1     α3(2)=3          has a type in the form of num ⟨n◦, n† ⟩ , where n◦ and n† repre-
                                                                      sent the “difference” of its value in the aligned and shadow
      Figure 2. Selective alignment for Report Noisy Max              execution respectively. In Figure 1, non-private variables,
                                                                      such as ϵ, size, are annotated with distance 0. For private
                                                                      variables, the difference could be a constant or an expression.
   One approach of tackling this challenge, followed by ex-           For example, the type of q along with the precondition speci-
isting language-based proofs of Report Noisy Max [2, 8], is           fies the adjacency relation: each query answer’s difference is
to use the pointwise lifting argument: informally, if we can          specified by ∗, which is desugared to a special variable qb◦ [i]
show that for any value i, execution on D 1 returns value i           (details discussed in Section 4). The precondition in Figure 1
implies execution on D 2 returns value i (with a privacy cost         specifies that the difference of each query answer is bounded
bounded by ϵ), then a program is ϵ-differential private. How-         by 1 (i.e., query answers have sensitivity of 1).
ever, this argument does not apply to the randomness align-              ShadowDP reasons about the aligned and shadow execu-
ment technique. Moreover, doing so requires a customized              tions in isolation, with the exception of sampling commands.
program logic for proving differential privacy.                       A sampling command (e.g., line 3 in Figure 1) constructs the
                                                                      aligned execution by either using values from the aligned
2.4    Approach Overview                                              execution so far (symbol ◦), or switching to values from the
In this paper, we propose a new proof technique “shadow               shadow execution (symbol †). The construction may depend
execution”, which enables language-based proofs based on              on program state: in Figure 1, we switch to shadow values iff
standard program logics. The key insight is to track a shadow         q[i] +η is the max on D 1 . A sampling command also specifies
execution on D 2 where the same noise is always used as on D 1 .      the alignment for the generated random noise.
For our running example, we illustrate the shadow execution              With function specification and annotations for sampling
in Figure 2, with random noise α 0(†) , α 1(†) and so on. Note that   commands, the type system of ShadowDP automatically
the shadow execution uses α i(†) = α i(1) for all i.                  checks the source code. If successful, it generates a non-
   With the shadow execution, we can construct a random-              probabilistic program (as shown at the bottom of Figure 1)
ness alignment for each query i as follows:                           with a distinguished variable vϵ . The soundness of the type
                                                                      system ensures the following property: if vϵ is bounded by
Case 1: Whenever q[i] + α i(1) is the maximum value so far            some constant ϵ in the transformed program, then the origi-
        on D 1 (i.e., max is updated), we use the alignments          nal program being verified is ϵ-private.
        on shadow execution for all previous queries but a
        noise α i(1) + 2 for q[i] on D 2 .
                                                                      Benefits Compared with previous language-based proofs
Case 2: Whenever q[i] + α i(1) is smaller than or equal to any        of Report Noisy Max [2, 8] (both are based on the pointwise
        previous noise query answer (i.e., max is not up-             lifting argument), ShadowDP enjoys a unique benefit: the
        dated), we keep the previous alignments for previous          transformed code can be verified based on standard program
        queries and use noise α i(1) for q[i] on D 2 .                semantics. Hence, the transformed (non-probabilistic) pro-
   We illustrate this construction in Figure 2. After seeing          gram can be further analyzed by existing program verifiers
q[1] on D 1 (Case 1), the construction uses noise in the shadow       and other tools. For example, the transformed program in
execution for previous query answers, and uses α 1(1) + 2 = 4         Figure 1 is verified with an off-the-shelf tool CPAChecker[11]
as the noise for q[1] on D 2 . After seeing q[2] on D 1 (Case 2),     without any extra annotation within seconds. Although not
the construction reuses alignments constructed previously,            explored in this paper, the transformed program can also be
                                                                      analyzed by symbolic executors to identify counterexamples
and use α 2(1) = 1 as the noise for q[2]. When q[3] comes, the
                                                                      when the original program is incorrect. We note that doing
previous alignment is abandoned; the shadow execution is
                                                                      so will be more challenging in a customized logic.
used for q[0] to q[2]. It is easy to check that this construction
is correct for any subset of query answers seen so far, since
the resulting alignment is exactly the same as the informal
proof above, when the index of maximum value is known.
                                                                      3   ShadowDP: Syntax and Semantics
                                                                      In this section, we present the syntax and semantics of Shad-
Randomness alignment with shadow execution To in-                     owDP, a simple imperative language for designing and veri-
corporate the informal argument above to a programming                fying differentially private algorithms.
Proving Differential Privacy with Shadow Execution                                                  PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

 Reals                r     ∈ R                                                 likelihood of seeing each is bounded by some constant. Since
 Normal Vars          x     ∈ NVars                                             only numerical values have numeric distances, other data
 Random Vars          η     ∈ RVars                                             types (including bool, list τ and τ1 → τ2 ) are always asso-
 Linear Ops           ⊕    ::= + | −
 Other Ops            ⊗    ::= × | /                                            ciated with ⟨0, 0⟩, hence omitted in the syntax. Note that this
 Comparators          ⊙    ::= <|>|=|≤|≥                                        does not rule out numeric distances in nested types. For ex-
 Bool Exprs           b    ::= true | false | x | ¬b | n1 ⊙ n2                  ample, (list num ⟨1,1⟩ ) stores numbers that differ by exactly
 Num Exprs            n    ::= r | x | η | n1 ⊕ n2 |                            one in both aligned and shadow executions.
                               n1 ⊗ n2 | b? n1 : n2                                Distance d can either be a numeric expression (n) in the
 Expressions          e    ::= n | b | e 1 :: e 2 | e 1 [e 2 ]                  language or ∗. A variable x with type num ⟨∗,∗⟩ is desugared as
 Commands             c    ::= skip | x := e | η := д | c 1 ; c 2 |             x : Σ(⟨b                                                              b◦ , xb† are distin-
                                                                                                                                 x ◦, xb† ⟩ , where x
                                                                                       x ◦ :num ⟨0, 0⟩ , xb† :num ⟨0, 0⟩ ⟩) num ⟨b
                               return e | while e do (c) |
                                                                                guished variables invisible in the source code; hiding those
                               if e then (c 1 ) else (c 2 )
 Distances            d    ::= n | ∗                                            variables in a Σ-type simplifies the type system (Section 4).
 Types                τ    ::= num ⟨d◦, d† ⟩ | bool | list τ                       The star type is useful for two reasons. First, it specifies
 Var Versions         k     ∈ {◦, †}                                            the sensitivity of query answers in a precise way. Consider
 Selectors            S    ::= e ? S1 : S2 | k                                  the parameter q in Figure 1 with type list num ⟨∗,∗⟩ , along
 Rand Exps            д    ::= Lap r , S , nη                                   with the precondition ∀i ≥ 0. − 1 ≤ b                         q◦ [i] ≤ 1. This notation
            Figure 3. ShadowDP: language syntax.                                makes the assumption of the Report Noisy Max algorithm
                                                                                explicit: each query answer differs by at most 1. Second,
3.1    Syntax                                                                   star type serves as the last resort when the distance of a
The language syntax is given in Figure 3. Most parts of Shad-                   variable cannot be tracked precisely by a static type system.
owDP is standard; we introduce a few interesting features.                      For example, whenever ShadowDP merges two different
                                                                                distances (e.g., 3 and 4) of x from two branches, the result
Non-probabilistic variables and expressions ShadowDP                            distance is ∗; the type system instruments the source code
supports real numbers, booleans as well as standard oper-                       to maintain the correct values of xb◦ , xb† (Section 4).
ations on them. We use n and b to represent numeric and
boolean expressions respectively. A ternary numeric expres-                     Sampling with selectors Each sampling instruction is at-
sion b ? n1 : n2 evaluates to n1 when the comparison evalu-                     tached with a few annotations for proving differential pri-
ates to true, and n2 otherwise. Moreover, to model multiple                     vacy, in the form of (η := Lap r , S, nη ). Note that just like
queries to a database and produce multiple outputs during                       types, the annotations S, nη have no effects on the program
that process, ShadowDP supports lists: e 1 :: e 2 appends the                   semantics; they only show up in verification. Intuitively, a se-
element e 1 to a list e 2 ; e 1 [e 2 ] gets the e 2 -th element in list e 1 ,   lector S picks a version (k ∈ {◦, †}) for all program variables
assuming e 2 is bound by the length of e 1 .                                    (including the previously sampled variables) at the sampling
                                                                                instruction, as well as constructs randomness alignment for
Random variables and expressions To model probabilis-                           η, specified by nη (note that the distance cannot be ∗ by syn-
tic computation, which is essential in differentially private                   tactical restriction here). By definition, both S and nη may
algorithms, ShadowDP uses random variable η ∈ RVars to                          depend on the program state when the sampling happens.
store a sample drawn from a distribution. Random variables                         Return to the running example in Figure 1. As illustrated
are similar to normal variables (x ∈ NVars) except that they                    in Figure 2, the selective alignment is to
are the only ones who can get random values from random
                                                                                  • use shadow variables and align the new sample by 2
expressions, via a sampling command η := д.
                                                                                    whenever a new max is encountered,
   We follow the modular design of LightDP [42], where
                                                                                  • use aligned variables and the same sample otherwise.
randomness expressions can be added easily. In this paper,
we only consider the most interesting random expression,                           Hence, the sampling command in Figure 1 is annotated
Lap r . Semantically, η := Lap r draws one sample from the                      as (η := Lap (2/ϵ), Ω ? † : ◦, Ω ? 2 : 0), where Ω is q[i]+η >
Laplace distribution, with mean zero and a scale factor r , and                 bq ∨ i = 0, the condition when a new max is found.
assigns it to η. For verification purpose, a sampling command                   3.2     Semantics
also requires a few annotations, which we explain shortly.
                                                                                As standard, the denotational semantics of the probabilistic
Types Types in ShadowDP have the form of B ⟨d◦, d† ⟩ , where                    language is defined as a mapping from initial memory to a
B is the base type, and d◦ , d† represent the alignments for the                distribution on (possible) final outputs. Formally, let M be a
execution on adjacent database and shadow execution respec-                     set of memory states where each m ∈ M maps all (normal
tively. Base type is standard: it includes num (numeric type),                  and random) variables (NVars ∪ RVars) to their values.
bool (Boolean), or a list of elements with type τ (list τ ).                       The semantics of an expression e of base type B is inter-
   Distance d is the key for randomness alignment proof.                        preted as a function JeK : M → JBK, where JBK represents
Intuitively, it relates two program executions so that the                      the set of values belonging to the base type B. We omit
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

expression semantics since it is standard. A random expres-            4.3.1     Aligned Variables
sion д is interpreted as a distribution on real values. Hence,         The type system infers and checks the distances of both
JдK : Dist(JnumK). Moreover, a command c is interpreted as             aligned and shadow variables. Since most rules treat them
a function JcK : M → Dist(M). For brevity, we write JeKm               in the same way, we first explain the rules with respect to
and JcKm instead of JeK(m) and JcK(m) hereafter. Finally, all          aligned variables only, then we discuss shadow variables in
programs have the form (c; return e) where c contains no               Section 4.3.2. To simplify notation, we write Γ instead of Γ ◦
return statement. A program is interpreted as a function               for now since only aligned variables are discussed.
m → DistJBK where B is the return type (of e).
   The semantics of commands is available in the Appendix;             Flow-Sensitivity In each typing rule pc ⊢ Γ {c ⇀ c ′ } Γ ′,
the semantics directly follows a standard semantics in [29].           an important invariant is that if c runs on two memories that
                                                                       are aligned by Γ, then the final memories are aligned by Γ ′.
4     ShadowDP: Type System                                                Consider the assignment rule (T-Asgn). This rule com-
                                                                       putes the distance of e’s value, n◦ , and updates the distance
ShadowDP is equipped with a flow-sensitive type system. If
                                                                       of x’s value after assignment to n◦ .
successful, it generates a transformed program with needed
                                                                           More interesting are rules (T-If) and (T-While). In (T-If),
assertions to make the original program differentially private.
                                                                       we compute the typing environments after executing c 1 and
The transformed program is simple enough to be verified by
                                                                       c 2 as Γ1 and Γ2 respectively. Since each branch may update
off-the-shelf program verifiers.
                                                                       x’s distance in arbitrary way, Γ1 (x) and Γ2 (x) may differ. We
4.1   Notations                                                        note that numeric expressions and ∗ type naturally form a
                                                                       two level lattice, where ∗ is higher than any n. Hence, we
We denote by Γ the typing environment which tracks the                 use the following rule to merge two distances d1 and d2 :
type of each variable in a flow-sensitive way (i.e., the type                                       (
of each variable at each program point is traced separately).                                         d1 if d1 = d2
All typing rules are formalized in Figure 4. Typing rules                                d1 ⊔ d2 ≜
                                                                                                      ∗ otherwise
share a common global invariant Ψ, such as the sensitiv-
ity assumption annotated in the source code (e.g., the pre-            For example, (3 ⊔ 4 = ∗), (x + y ⊔ x + y = x + y), (x ⊔ 3 = ∗).
condition in Figure 1). We also write Γ(x) = ⟨d◦ , d† ⟩ for            Hence, (T-If) ends with Γ1 ⊔ Γ2 , defined as λx . Γ1 (x) ⊔ Γ2 (x).
∃ B. Γ(x) = B ⟨d◦, d† ⟩ when the base type B is irrelevant.               As an optimization, we also use branch conditions to sim-
                                                                       plify distances. Consider our running example (Figure 1): at
4.2   Expressions                                                      Line 4, η has (aligned) distance Ω ? 2 : 0, where Ω is the
Expression rules have the form of Γ ⊢ e : τ , which means              branch condition. Its distance is simplified to 2 in the true
that expression e has type τ under the environment Γ. Most             branch and 0 in the false branch.
rules are straightforward: they compute the distance for                  Rule (T-While) is similar, except that it requires a fixed
aligned and shadow executions separately. Rule (T-OTimes)              point Γf such that pc ⊢ Γ ⊔ Γf {c} Γf . In fact, this rule is de-
makes a conservative approach for nonlinear computations,              terministic since we can construct the fixed point as follows
following LightDP [42]. Rule (T-VAR) desugars star types               (the construction is similar to the one in [27]):
when needed. The most interesting rule is (T-ODot), which                             pc ⊢ Γi′ {c ⇀ c i′ } Γi′′ for all 0 ≤ i ≤ n
generates the following constraint:
                                                                       where Γ0′ = Γ, Γi+1 ′ = Γ ′′ ⊔ Γ, Γ ′
                                                                                                  i         n+1 = Γn .
                                                                                                                   ′

Ψ ⇒ (e 1 ⊙ e 2 ⇔ (e 1 +n1 ) ⊙ (e 2 +n3 ) ∧ (e 1 + n2 ) ⊙ (e 2 +n4 ))      It is easy to check that Γn = Γn+1 = Γn′′ ⊔ Γ and pc ′ ⊢
                                                                                                          ′      ′

                                                                       Γn {c ⇀ c i′ } Γn′′ by construction. Hence, Γn′′ is a fixed point:
                                                                        ′
   This constraint states that the boolean value of e 1 ⊙ e 2 is       pc ⊢ Γ ⊔ Γn′′ {c ⇀ c i′ } Γn′′. Moreover, the computation above
identical in both aligned and shadow executions. If the con-           always terminates since all typing rules are monotonic on
straint is discharged by an external solver (our type system           typing environments2 and the lattice has a height of 2.
uses Z3 [17]), we are assured that e 1 ⊙ e 2 has distances ⟨0, 0⟩.
                                                                       Maintaining dynamically tracked distances Each typ-
4.3   Commands                                                         ing rule pc ⊢ Γ {c ⇀ c ′ } Γ ′ also sets the value of xb◦ to
The flow-sensitive type system tracks and checks the dis-              maintain distance dynamically whenever Γ ′(x) = ∗. This is
tances of aligned and shadow executions at each program                achieved by the instrumented commands in c ′.
point. Typing rules for commands have the form of                         None of rules (T-Skip, T-Asgn, T-Seq, T-Ret) generate ∗
                                                                       type, hence they do not need any instrumentation. The merge
                       pc ⊢ Γ {c ⇀ c ′ } Γ ′                           operation in rule (T-If) generates ∗ type when Γ1 (x) , Γ2 (x).
meaning that starting from the previous typing environment             In this case, we use the auxiliary instrumentation rule in the
Γ, the new typing environment is Γ ′ after c. We will discuss          2 That is, ∀pc, c, Γ , Γ , Γ ′, Γ ′, c , c . pc ⊢ Γ {c ⇀ c ′ }Γ ′ i ∈ {1, 2} ∧ Γ ⊑
                                                                                           1 2 1 2 1 2                    i       i i                  1
the other components pc and c ′ shortly.                               Γ2 =⇒ Γ1′ ⊑ Γ2′ .
Proving Differential Privacy with Shadow Execution                                                                  PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

Typing rules for expressions                                                                                              ⋆
                                                                                                                          xb       if d⋆ = ∗
                                                                                        Γ(x) = B ⟨d◦, d† ⟩       n⋆ =                              ⋆ ∈ {◦, †}
                                                                                                                           d⋆      otherwise
                              (T-Num)                             (T-Boolean)                                                                                      (T-Var)
       Γ ⊢ r : num ⟨0,0⟩                     Γ ⊢ b : bool                                                          Γ ⊢ x : B ⟨n ◦ , n † ⟩

              Γ ⊢ e 1 : num ⟨n1, n2 ⟩ Γ ⊢ e 2 : num ⟨n3, n4 ⟩                                            Γ ⊢ e 1 : num ⟨0,0⟩ Γ ⊢ e 2 : num ⟨0,0⟩
                                                              (T-OPlus)                                                                          (T-OTimes)
                   Γ ⊢ e 1 ⊕ e 2 : num ⟨n1 ⊕n3, n2 ⊕n4 ⟩                                                         Γ ⊢ e 1 ⊗ e 2 : num ⟨0,0⟩

 Γ ⊢ e 1 : num ⟨n1, n2 ⟩         Ψ ⇒ (e 1 ⊙ e 2 ⇔ (e 1 +n1 ) ⊙ (e 2 +n3 ))
 Γ ⊢ e 2 : num ⟨n3, n4 ⟩              ∧(e 1 ⊙ e 2 ⇔ (e 1 +n2 ) ⊙ (e 2 +n4 ))                                    Γ ⊢ e 1 : bool Γ ⊢ e 2 : τ Γ ⊢ e 3 : τ
                                                                             (T-ODot)                                                                  (T-Ternary)
                               Γ ⊢ e 1 ⊙ e 2 : bool                                                                        Γ ⊢ e1 ? e2 : e3 : τ

       Γ ⊢ e : bool                               Γ ⊢ e 1 : τ Γ ⊢ e 2 : list τ                                    Γ ⊢ e 1 : list τ Γ ⊢ e 2 : num ⟨0,0⟩
                    (T-Neg)                                                    (T-Cons)                                                                (T-Index)
      Γ ⊢ ¬e : bool                                   Γ ⊢ e 1 :: e 2 : list τ                                                 Γ ⊢ e 1 [e 2 ] : τ
 Typing rules for commands
                                                                                                        ⟨Γ[x 7→ B ⟨n◦, n† ⟩ ], skip⟩, if pc = ⊥
                                                                                                    (
                                                       Γ ⊢ e : B ⟨n ◦ , n † ⟩       ⟨Γ ′, c † ⟩ =
                                                                                                        ⟨Γ[x 7→ B ⟨n◦,∗⟩ ], xb† := x + n† − e⟩, else
                                         (T-Skip)                                                                                                                       (T-Asgn)
   pc ⊢ Γ {skip ⇀ skip} Γ                                                                 pc ⊢ Γ {x := e ⇀ c † ; x := e} Γ ′

           pc ⊢ Γ {c 1 ⇀ c 1′ } Γ1              pc ⊢ Γ1 {c 2 ⇀ c 2′ } Γ2                                   Γ ⊢ e : num ⟨0, d ⟩ or Γ ⊢ e : bool
                                                                                  (T-Seq)                                                      (T-Return)
                           pc ⊢ Γ {c 1 ; c 2 ⇀ c 1′ ; c 2′ } Γ2                                            pc ⊢ Γ {return e ⇀ return e} Γ

                                                                               skip, if (pc = ⊤ ∨ pc ′ = ⊥)
                                                                             (
         pc ′ = updPC(pc, Γ, e)
         pc ⊢ Γ {c i ⇀ c i } Γi
             ′           ′       Γi , Γ  ⊔ Γ  , pc ′
                                                     ⇛ c ′′
                                                         i  i ∈ {1, 2} c †
                                                                           =
                                                                                Lif e then c 1 else c 2 , Γ1 ⊔ Γ2 M† , else
                                       1    2

                                                                                                                                      (T-If)
    pc ⊢ Γ if e then c 1 else c 2 ⇀ if e then (assert (Le, ΓM◦ ); c 1′ ; c 1′′) else (assert (¬Le, ΓM◦ ); c 2′ ; c 2′′) ; c † Γ1 ⊔ Γ2
                                                                                                                      


                                                                                       skip, if (pc = ⊤ ∨ pc ′ = ⊥)
                                                                                     (
                 pc ′ = updPC(pc, Γ, e)                  Γ, Γ ⊔ Γf , pc ′ ⇛ c s
                                                        Γf , Γ ⊔ Γf , pc ′ ⇛ c ′′ c = Lwhile e do c, Γ ⊔ Γf M† , else
                                                                                   †
               pc ′ ⊢ Γ ⊔ Γf {c ⇀ c ′ } Γf
                                                                                                                                                      (T-While)
                            pc ⊢ Γ {while e do c ⇀ c s ; (while e do (assert (Le, ΓM◦ ); c ′; c ′′)); c † } Γ ⊔ Γf
 Typing rules for random assignments

pc = ⊥       Γ ′ = λx . ⟨S(⟨n◦ , n† ⟩), n† ⟩ where Γ ⊢ x : B ⟨n◦, n† ⟩                      Ψ ⇒ ((η + nη ){η 1 /η} = (η + nη ){η 2 /η} ⇒ η 1 = η 2 )
                                                                                                                                                                    (T-Laplace)
                                  pc ⊢ Γ {η := Lap r ; S, nη ⇀ η := Lap r ; S, nη } Γ ′[η 7→ num ⟨nη ,0⟩ ]
 Instrumentation rule

                                      c ◦ = {b
                                             x ◦ := n | Γ1 (x) = num ⟨n, d1 ⟩ ∧ Γ2 (x) = num ⟨∗, d2 ⟩ }
                                                                                                                                               if pc = ⊥
                                                                                                                                    ◦ †
                                                                                                                                    c ;c
                      Γ1 ⊑ Γ2         c = {b
                                        †
                                             x † := n | Γ1 (x) = num ⟨d1, n ⟩ ∧ Γ2 (x) = num ⟨d2,∗⟩ }                       c′ =
                                                                                                                                    c◦         if pc = ⊤
                                                                                    Γ1 , Γ2 , pc ⇛ c ′
 Select function
              ◦(⟨e 1 , e 2 ⟩) = e 1                  † (⟨e 1 , e 2 ⟩) = e 2                  (e ? S1 : S2 )(⟨e 1 , e 2 ⟩) = e ? S1 (⟨e 1 , e 2 ⟩) : S2 (⟨e 1 , e 2 ⟩)
 PC update function
                                                                                  ⊥ , if pc = ⊥ ∧ Ψ ⇒ (e ⇔ Le, ΓM† )
                                                                              
                                                  updPC(pc, Γ, e) =
                                                                                  ⊤ , else
Figure 4. Typing rules and auxiliary rules. Ψ is an invariant that holds throughout program execution. In most rules, shadow
distances are handled in the same way as aligned distances, with exceptions highlighted in gray boxes.
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

form of Γ1 , Γ2 , pc ⇛ c ′, assuming Γ1 ⊑ Γ2 . In particular, for    max; however, execution on D 1 will update max, since the
each variable x whose distance is “upgraded” to ∗, the rule          noisy query value of 4 is greater than the previous max of 2.
sets xb◦ to the distance previously tracked by the type system          To capture the potential divergence of shadow execution,
(Γ1 (x)). Moreover, the instrumentation commands c 1′′, c 2′′ are    each typing rule is associated with a program counter pc with
inserted under their corresponding branches.                         two possible values ⊥ and ⊤ (introducing program counters
   Consider the following example:                                   in a type system is common in information flow control to
    if ( x > 1) x := y; else y := 1;                                 track implicit flows [37]). Here, ⊤ (resp. ⊥) means that the
                                                                     shadow execution might take a different branch (resp. must
staring with Γ0 : {x : 1, y : 0}. In the true branch, rule (T-
                                                                     take the same branch) as the original execution.
Asgn) updates x to the distance of y, resulting Γ1 : {x : 0, y :
                                                                        When pc = ⊥, the shadow execution is checked in the
0}. Similarly, we get Γ2 : {x : 1, y : 0} in the false branch.
                                                                     same way as aligned execution. When pc = ⊤, the shadow
Moreover, when we merge the typing environments Γ1 and Γ2
                                                                     distances are updated (as done in Rule (T-Asgn)) so that x +b  x†
at the end of branch, the typing environment becomes Γ3 =
                                                                     remains the same. The new value from the shadow execution
Γ1 ⊔ Γ2 = {x : ∗, y : 0}. Since Γ1 (x) , Γ2 (x), instrumentation
                                                                     will be maintained by the type system when pc transits from
rule is also applied, which instruments b    x◦ := 0 after x :=
        ◦                                                            ⊥ to ⊤ by code instrumentation for sub-commands in (T-If)
y and bx := 1 after y := 1.
                                                                     and (T-While), as we show next.
   Rule (T-While) may also generate ∗ types. Following the
                                                                        Take a branch (if e then c 1 else c 2 ) for example. The
same process in rule (T-If), it also uses the instrumentation
                                                                     transition happens when pc = ⊥ ∧ pc ′ = ⊤. In this case, we
rule to update corresponding dynamically tracked distance
                                                                     construct a shadow execution of c by an auxiliary function
variables. The instrumentation command c s is inserted before
                                                                     Lc, ΓM† . The shadow execution essentially replaces each vari-
loop and c ′′ after the commands in the loop body.
                                                                     able x with their correspondence (i.e., x + xb† ), as is standard
Well-Formedness Whenever an assignment x := e is exe-                in self-composition [4, 39]. The only difference is that Lc, ΓM†
cuted, no variable’s distance should depend on x. To see why,        is not applicable to sampling commands, since we are un-
consider x := 2 with initial Γ ◦ (y) = x and m(x) = 1. Since         able to align the sample variables when different amount of
this assignment does not modify the value of y, the aligned          samples are taken. The full definition of Lc, ΓM† is available
value of y (i.e., y + Γ ◦ (y)) should not change. However, Γ ◦ (y)   in the Appendix. Rule (T-While) is very similar in its way
changes from 1 to 2 after the assignment.                            of handling shadow variables.
   To avoid this issue, we check the following condition for
each assignment x := e: ∀y ∈ Vars. x < Vars(Γ(y)). In case
that the check fails for some y, we promote its distance to ∗,
and use the auxiliary instrumentation ⇛ to set yb◦ properly.
Hence, well-formedness is guaranteed: no variable’s distance
depends on x when x is updated.                                      4.3.3    Sampling Command
                                                                     Rule (T-Laplace) checks the only probabilistic command η :=
Aligned branches For differential privacy, we require the            Lap r , S , nη in ShadowDP. Here, the selector S and numeric
aligned execution to follow the same branch as the original          distance nη are annotations provided by a programmer to
execution. Due to dynamically tracked distances, statically          aid type checking. For the sample η, the aligned distance is
checking that in a type system could be imprecise. Hence,            specified by nη and the shadow distance is always 0 (since
we use assertions in rules (T-If) and (T-While) to ensure the        by definition, shadow execution use the same sample as the
aligned execution does not diverge. In those rules, Le, ΓM◦          original program). Hence, the type of η becomes num ⟨nη ,0⟩ .
simply computes the value of e in the aligned execution; its            Moreover, the selector constructs the aligned execution
full definition is in the Appendix.                                  from either the aligned (◦) or shadow (†) execution. Since
                                                                     the selector may depend on a condition e, we use the selector
4.3.2   Shadow Variables                                             function S(⟨e 1 , e 2 ⟩) in Figure 4 to do so.
In most typing rules, shadow variables are handled in the               Rule (T-Laplace) also checks that each η is generated in
same way as aligned ones, which is discussed above. The key          an injective way: the same aligned value of η implies the
difference is that the type system allows the shadow execu-          same value of η in the original execution.
tion to take a different branch from the original execution.            Consider the sampling command in Figure 1. The typing
   The extra permissiveness is the key ingredient of verifying       environments before and after the command is shown below
algorithms such as Report Noisy Max. To see why, consider            (we omit unrelated parts for brevity):
the example in Figure 2, where the shadow execution runs                 {bq : ⟨∗, ∗⟩, · · · }
on D 2 with same random noise as from the execution on                   η := Lap (2/ϵ) , Ω ? † : ◦ , Ω ? 2 : 0;
D 1 . Upon the second query, the shadow execution does not                               †      ◦    †
                                                                         {bq : ⟨Ω ? cbq : c   bq , c
                                                                                                   bq ⟩ , η : ⟨Ω ? 2 : 0, 0⟩ , · · · }
update max, since its noisy value 3 is the same as the previous
Proving Differential Privacy with Shadow Execution                                   PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA


 η := Lap r ; S, nη ⇒ havoc η; vϵ := S(⟨vϵ , 0⟩) + |nη |/r ;
                                                                      5    Soundness
                                                                      The type system performs a two-stage transformation:
           c ⇒ c, if c is not a sampling command                                   pc ⊢ Γ1 {c ⇀ c ′ } Γ2       and     c ′ ⇒ c ′′
                                                                         Here, both c and c ′ are probabilistic programs; the dif-
Figure 5. Transformation rules to the target language. Prob-          ference is that c executes on the original memory without
abilistic commands are reduced to non-deterministic ones.             any distance tracking variables; c ′ executes on the extended
                                                                      memory where distance tracking variables are visible. In
                                                                      the second stage, c ′ is transformed to a non-probabilistic
                                                                      program c ′′ where sampling instructions are replaced by
  In this example, S is Ω ? † : ◦. So the aligned distance of         havoc and the privacy cost vϵ is explicit. In this section, we
variable bq will be Ω ? c
                           †
                        bq : c
                                 ◦
                              bq , the shadow distance of vari-       use c, c ′, c ′′ to represent the source, transformed, and target
                 c† . The aligned distance of η is ⟨Ω ? 2 : 0, 0⟩,
able bq is still bq
                                                                      program respectively.
                                                                         Overall, the type system ensures ϵ-differential privacy
where the aligned part is specified in the annotation.
                                                                      (Theorem 2): if the value of vϵ in c ′′ is always bounded by a
                                                                      constant ϵ, then c is ϵ-differentially private. In this section,
4.4   Target Language                                                 we formalize the key properties of our type system and prove
One goal of ShadowDP is to enable verification of ϵ-differential      its soundness. Due to space constraints, the complete proofs
privacy using off-the-shelf verification tools. In the trans-         are available in the Appendix.
formed code so far, we assumed assert commands to verify
                                                                      Extended Memory Command c ′ is different from c since it
that certain condition holds. The only remaining challenging
                                                                      maintains and uses distance tracking variables. To close the
feature is the sampling commands, which requires proba-
                                                                      gap, we first extend memory m to include those variables,
bilistic reasoning. Motivated by LightDP [42], we note that                       d = ∪x ∈NVars {b
                                                                      denoted as Vars            x ◦ , xb† } and introduce a distance
for ϵ-differential privacy, we are only concerned with the
maximum privacy cost, not its likelihood. Hence, in the fi-           environment γ : Vars → R.
                                                                                        d
nal step, we simply replace the sampling command with a               Definition 2. Let γ : Vars
                                                                                             d → R. For any m ∈ M, there is an
non-deterministic command havoc η, which semantically                 extension of m,written m ⊎ (γ ), such that
sets the variable η to an arbitrary value upon execution, as                                      (
                                                                                                   m(x), x ∈ Vars
shown in Figure 5.                                                                  m ⊎ (γ )(x) =
   Note that a distinguished variable vϵ is added by the type                                      γ (x), x ∈ Vars
                                                                                                                 d
system to explicitly track the privacy cost of the original
                                                                        We use M ′ to denote the set of extended memory states
program. For Laplace distribution, aligning η by the distance
                                                                      and m 1′ , m 2′ to refer to concrete extended memory states. We
of nη is associated with a privacy cost of |nη |/r . The reason
                                                                      note that although the programs c and c ′ are probabilistic, the
is that the ratio of any two points that are |nη | apart in
                                                                      extra commands in c ′ are deterministic. Hence, c ′ preserves
the Laplace distribution with scaling factor r is bounded
                                                                      the semantics of c, as formalized by the following Lemma.
by exp(|nη |/r ). Since the shadow execution uses the same
sample, it has no privacy cost. This very fact allows us to           Lemma 1 (Consistency). Suppose pc ⊢ Γ1 {c ⇀ c ′ } Γ2 . Then
reset privacy cost when the shadow execution is used (i.e., S         for any initial and final memory m 1 , m 2 such that JcKm1 (m 2 ) ,
selects †): the rule sets privacy cost to 0 + |nη |/r in this case.   0, and any extension m 1′ of m 1 , there is a unique extension m 2′
   In Figure 1, vϵ is set to Ω ? 0 : vϵ + Ω ? ϵ : 0 which is the      of m 2 such that
same as Ω ? ϵ : vϵ . Intuitively, that implies that the privacy
                                                                                           Jc ′Km1′ (m 2′ ) = JcKm1 (m 2 )
cost of the entire algorithm is either ϵ (when a new max is
found) or the same as the previous value of vϵ .                      Proof. By structural induction on c. The only interesting
   The type system guarantees the following important prop-           case is the (probabilistic) sampling command, which does
erty: if the original program type checks and the privacy             not modify distance tracking variables.                 □
cost vϵ in the target language is bounded by some constant
                                                                         From now on, we will use m 2′ to denote the unique exten-
ϵ in all possible executions of the program, then the original
                                                                      sion of m 2 satisfying the property above.
program satisfies ϵ-differential privacy. We will provide a
soundness proof in the next section. Consider the running             Γ-Relation To formalize and prove the soundness property,
example in Figure 1. The transformed program in the target            we notice that a typing environment Γ along with distance
language is shown at the bottom. With a model checking tool           environment γ induces two binary relations on memories.
CPAChecker [11], we verified that vϵ ≤ ϵ in the transformed           We write m 1 ⊎ (γ ) Γ ◦ m 2 (resp. m 1 ⊎ (γ ) Γ † m 2 ) when m 1 , m 2
program within 2 seconds (Section 6.3). Hence, the Report             are related by Γ ◦ (resp. Γ † ) and γ . Intuitively, the initial γ
Noisy Max algorithm is verified to be ϵ-differentially private.       and Γ (given by the function signature) specify the adjacency
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

relation, and the relation is maintained by the type system                    The next lemma enables precise reasoning of privacy cost
throughout program execution. For example, the initial γ and                 w.r.t. a pair of initial and final memories:
Γ in Figure 1 specifies that two executions of the program is
                                                                             Lemma 3 (Pointwise Soundness). Let pc, c, c ′, c ′′, Γ1 , Γ2 be
related if non-private variables ϵ, size are identical, and each
                                                                             such that pc ⊢ Γ1 {c ⇀ c ′ }Γ2 ∧ c ′ ⇒ c ′′, then ∀m 1′ , m 2′ :
query answer in q[i] differs by at most one.
   To facilitate the proof, we simply write m 1′ Γ m 2 where m 1′            (i) the following holds:
is an extended memory in the form of m 1 ⊎ (γ ).                                        Jc ′Km1′ (m 2′ ) ≤ JcKΓ†m′ (Γ2†m 2′ ) when pc = ⊥                       (1)
                                                                                                               1   1
Definition 3 (Γ-Relations). Two memories m 1′ (in the form                   (ii) one of the following holds:
of m 1 ⊎ (γ )) and m 2 are related by Γ ◦ , written m 1′ Γ ◦ m 2 , if                                                      m′
∀x ∈ Vars ∪ RVars, we have                                                         Jc ′Km1′ (m 2′ ) ≤ exp(max(c ′′ ↾m2′ ))JcKΓ1◦m1′ (Γ2◦m 2′ )                 (2a)
                                                                                                                             1

           m 2 (x) = m 1′ (x) + m 1′ (d◦ ) if Γ ⊢ x : num ⟨d◦, d† ⟩                                                        m 2′
                                                                                   Jc ′Km1′ (m 2′ ) ≤ exp(max(c ′′ ↾ ))JcKΓ†m′ (Γ2◦m 2′ )                      (2b)
                                                                                                                           m 1′           1   1
We define the relation on non-numerical types and the Γ †
                                                                                The point-wise soundness lemma provides a precise pri-
relation in a similar way.
                                                                             vacy bound per initial and final memory. However, differen-
    By the definition above, Γ ◦ introduces a function from                  tial privacy by definition (Definition 1) bounds the worst-case
M ′ to M. Hence, we use Γ ◦m 1′ as the unique m 2 such that                  cost. To close the gap, we define the worst-case cost of the
m 1′ Γ ◦ m 2 . The Γ † counterparts are defined similarly.                   transformed program.
Injectivity For alignment-based proofs, given any γ , both                   Definition 6. For any program c ′′ in the target language, we
Γ ◦ and Γ † must be injective functions [42]. The injectivity of             say the execution cost of c ′′ is bounded by some constants ϵ,
Γ over the entire memory follows from the injectivity of Γ                   written c ′′⪯ϵ , iff for any m 1′ , m 2′ ,
over the random noises η ∈ RVars, which is checked as the
                                                                                                m 2′ ⊎ (ϵ ′) ∈ Jc ′′Km1′ ⊎(0) ⇒ ϵ ′ ≤ ϵ
following requirement in Rule (T-Laplace):
       Ψ ⇒ ((η + nη ){η 1 /η} = (η + nη ){η 2 /η} ⇒ η 1 = η 2 )                  Note that off-the-shelf tools can be used to verify that
                                                                             c ′′⪯ϵ holds for some ϵ.
where all variables are universally quantified. Intuitively, this
is true since the non-determinism of the program is purely                   Theorem 1 (Soundness). Given c, c ′, c ′′, m 1′ , Γ1 , Γ2 , ϵ such that
from that of η ∈ RVars.                                                      ⊥ ⊢ Γ1 {c ⇀c ′ }Γ2 ∧ c ′ ⇒c ′′ ∧ c ′′⪯ϵ , one of the following holds:

Lemma 2 (Injectivity). Given c, c ′, pc, m ′, m 1′ , m 2′ , Γ1 , Γ2 such                max (Jc ′Km1′ (S) − exp(ϵ)JcKΓ1◦m1′ (Γ2◦S)) ≤ 0,                       (3a)
                                                                                       S ⊆M ′
that pc ⊢ Γ1 {c ⇀ c ′ }Γ2 , Jc ′Km′m 1′ , 0 ∧ Jc ′Km′m 2′ , 0, ⋆ ∈
                                                                                        max (Jc ′Km1′ (S) − exp(ϵ)JcKΓ†m′ (Γ2◦S)) ≤ 0.                         (3b)
{◦, †}, then we have                                                                   S ⊆M ′                                     1   1

                    Γ2⋆m 1′ = Γ2⋆m 2′ =⇒ m 1′ = m 2′                                                                                                 m′
                                                                             Proof. By definition of c ′′⪯ϵ , we have max(c ′′ ↾m2′ ) ≤ ϵ for
                                                                                                                                 1
Soundness The soundness theorem connects the “privacy                        all m 2′ ∈ S. Thus, by Lemma 3, we have one of the two:
cost” of the probabilistic program to the distinguished vari-
                                                                                    Jc ′Km1′ (m 2′ ) ≤ exp(ϵ)JcKΓ1◦m1′ (Γ2◦m 2′ ),                ∀m 2′ ∈ S,
able vϵ in the target program c ′′. To formalize the connection,
we first extend memory one more time to include vϵ :                                Jc ′Km1′ (m 2′ ) ≤ exp(ϵ)JcKΓ†m′ (Γ2◦m 2′ ),                  ∀m 2′ ∈ S.
                                                                                                                       1   1

Definition 4. For any extended memory m ′ and constant ϵ,                    If the first inequality is true, then
there is an extension of m ′, written m ′ ⊎ (ϵ), so that                           max (Jc ′Km1′ (S) − exp(ϵ)JcKΓ1◦m1′ (Γ2◦S))
                                                                                    S ⊆M ′
m ⊎ (ϵ)(vϵ ) = ϵ, and m ⊎ (ϵ)(x) = m(x), ∀x ∈ dom(m ).
   ′                              ′                                   ′
                                                                                        Õ
                                                                                 = max′      (Jc ′Km1′ (m 2′ ) − exp(ϵ)JcKΓ1◦m1′ (Γ2◦m 2′ )) ≤ 0
   For a transformed program and a pair of initial and final                        S ⊆M
                                                                                             m 2′ ∈S
memories m 1′ and m 2′ , we identify a set of possible vϵ values,
so that in the corresponding executions of c ′′, the initial and             and therefore (3a) holds. Similarly, (3b) holds if the second
final memories are extensions of m 1′ and m 2′ respectively:                 inequality is true. Note that the equality above holds due to
                                                                             the injective assumption, which allows us to derive the set-
Definition 5. Given c ′ ⇒ c ′′, m 1′ and m 2′ , the consistent costs         based privacy from the point-wise privacy (Lemma 3). □
                                                         m′
of executing c ′′ w.r.t. m 1′ and m 2′ , written c ′′ ↾m2′ , is defined as
                                                           1                    We now prove the main theorem on differential privacy:
                     m′
               c ′′ ↾m2′ ≜ {ϵ | m 2′ ⊎ (ϵ) ∈ Jc ′′Km1′ ⊎(0) }                Theorem 2 (Privacy). Given Γ1 , Γ2 , c, c ′, c ′′, e, ϵ such that Γ1◦ =
                      1

                  m′                                                         Γ1† ∧ ⊥ ⊢ Γ1 {(c; return e) ⇀ (c ′; return e)}Γ2 ∧ c ′ ⇒ c ′′,
   Since (c ′′ ↾m2′ ) by definition is a set of values of vϵ , we            we have
                    1
                    m′
write max(c ′′ ↾m2′ ) for the maximum cost.                                                   c ′′⪯ϵ ⇒ c is ϵ-differentially private.
                        1
Proving Differential Privacy with Shadow Execution                                 PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

Proof. By the typing rule, we have ⊥ ⊢ Γ1 {c ⇀ c ′ }Γ2 . By the      capable of automatically verifying C program with a given
soundness theorem (Theorem 1) and the fact that Γ1◦ = Γ2† , we       configuration. In our implementation, predicate analysis is
have Jc ′Km1′ (S) ≤ exp(ϵ)JcKΓ1◦m1′ (Γ2◦S). For clarity, we stress   used. Also, CPAChecker has multiple solver backends such as
that all sets are over distinct elements (as we have assumed         MathSat [16], Z3 [17] and SMTInterpol [15]. For the best per-
throughout this paper).                                              formance, we concurrently use different solvers and return
  By rule (T-Return), Γ2 ⊢ e : num ⟨0, d ⟩ or Γ2 ⊢ e : bool. For     the results as soon as any one of them verifies the program.
any set of values V ⊆ JBK, let SV′ = {m ′ ∈ M ′ | JeKm′ ∈ V }           One limitation of CPAChecker and many other tools, is
and SV = {m ∈ M | JeKm ∈ V }, then we have Γ2◦SV′ ⊆ SV :             the limited support for non-linear arithmetics. For programs
                                                                     with non-linear arithmetics, we take two approaches. First,
          m ∈ Γ2◦SV′ ⇒ m = Γ2◦m ′ for some m ′ ∈ SV
                                                                     we verify the algorithm variants where ϵ is fixed (the ap-
                        ⇒ JeKm = JeKΓ2◦m′ = JeKm′ ∈ V                proach taken in [2]). In this case, all transformed code in
                        ⇒ m ∈ SV .                                   our evaluation is directly verified without any modification.
                                                                     Second, to verify the correctness of algorithms with arbitrary
The equality in second implication is due to the zero distance
                                                                     ϵ, we slightly rewrite the non-linear part in a linear way or
when Γ2 ⊢ e : num ⟨0, n ⟩ , and rule (T-ODot) when Γ2 ⊢ e : bool.
                                                                     provide loop invariants (see Section 6.2.2). We report the
We note that Γ2◦SV′ , SV in general since Γ2◦ might not be a
                                                                     results from both cases whenever we encounter this issue.
surjection. Let P ′ = (c ′; return e), then for any γ , we have
           JP ′Km1 ⊎(γ ) (V ) = Jc ′Km1 ⊎(γ ) (SV′ )                 6.2     Case Studies
                              ≤ exp(ϵ)Jc ′KΓ1◦m1 ⊎(γ ) (Γ2◦SV′ )     We investigate some interesting differentially private algo-
                              ≤ exp(ϵ)Jc ′KΓ1◦m1 ⊎(γ ) (SV )         rithms that are formally verified by ShadowDP. We only
                                                                     present the most interesting programs in this section; the
                              = exp(ϵ)JPKΓ1◦m1 ⊎(γ ) (V ).
                                                                     rest are provided in the Appendix.
Finally, due to Lemma 1, JPKm1 (V ) = JP ′Km1 ⊎(γ ) (V ). There-
fore, by definition of privacy c is ϵ-differentially private. □      6.2.1    Sparse Vector Technique
   Note that the shallow distances are only useful for proofs;       Sparse Vector Technique [21] is a powerful mechanism which
they are irrelevant to the differential privacy property being       has been proven to satisfy ϵ-differential privacy (its proof
obeyed by a program. Hence, initially, we have Γ1◦ = Γ1† (both       is notoriously tricky to write manually [30]). In this section
describing the adjacency requirement) in Theorem 2, as well          we show how ShadowDP verifies this algorithm and later
as in all of the examples formally verified by ShadowDP.             show how a novel variant is verified.
                                                                         Figure 6 shows the pseudo code of Sparse Vector Tech-
6     Implementation and Evaluation                                  nique [21]. It examines the input queries and reports whether
                                                                     each query is above or below a threshold T . To achieve dif-
6.1   Implementation
                                                                     ferential privacy, it first adds Laplace noise to the threshold
We have implemented ShadowDP into a trans-compiler3                  T , compares the noisy query answer q[i] + η 2 with the noisy
in Python. ShadowDP currently supports trans-compilation             threshold T̃ , and returns the result (true or false). The
from annotated C code to target C code. Its workflow includes        number of true’s the algorithm can output is bounded by
two phases: transformation and verification. The annotated           argument N . One key observation is that once the noise
source code will be checked and transformed by ShadowDP;             has been added to the threshold, outputting false pays no
the transformed code is further sent to a verifier.                  privacy cost [21]. As shown in Figure 6, programmers only
Transformation As explained in Section 4, ShadowDP                   have to provide two simple annotations: ◦ , 1 for η 1 and
tracks the typing environments in a flow-sensitive way, and          ◦ , Ω ? 2 : 0 for η 2 . Since the selectors in this example only
instruments corresponding statements when appropriate.               select aligned version of variables, the shadow execution is
Moreover, ShadowDP adds an assertion assert (vϵ ≤ ϵ)                 optimized away (controlled by pc in rule (T-If)). ShadowDP
before the return command. This assertion specifies the              successfully type checks and transforms this algorithm. How-
final goal of proving differential privacy. The implementation       ever, due to a nonlinear loop invariant that CPAChecker fails
follows the typing rules explained in Section 4.                     to infer, it fails to verify the program. With the loop invariant
                                                                     provided manually, the verification succeeds, proving this
Verification The goal of verification is to prove the asser-         algorithm satisfies ϵ-differential privacy (we also verified a
tion assert (vϵ ≤ ϵ) never fails for any possible inputs that        variant where ϵ is fixed to N to remove the non-linearity).
satisfy the precondition (i.e., the adjacency requirement). To
demonstrate the usefulness of the transformed programs, we           6.2.2    Gap Sparse Vector Technique
use a model checker CPAChecker [11] v1.8. CPAChecker is
                                                                     We now consider a novel variant of Sparse Vector Technique.
3 Publicly available at https://github.com/cmla-psu/shadowdp.        In this variant, whenever q[i] + η 2 ≥ T̃ , it outputs the value
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

                                        Table 1. Time spent on type checking and verification
                       Algorithm                         Type Check (s)   Verification by ShadowDP (s)      Verification by [2] (s)
                    Report Noisy Max                         0.465                     1.932                          22
             Sparse Vector Technique (N = 1)                 0.398                     1.856                          27
                                                                          Rewrite            Fix ϵ
                Sparse Vector Technique                          0.399     2.629             1.679                    580
        Numerical Sparse Vector Technique (N = 1)                0.418     1.783             1.788                      4
           Numerical Sparse Vector Technique                     0.421     2.584             1.662                      5
             Gap Sparse Vector Technique                         0.424     2.494             1.826                    N/A
                       Partial Sum                               0.445     1.922             1.897                     14
                       Prefix Sum                                0.449     1.903             1.825                     14
                       Smart Sum                                 0.603     2.603             2.455                    255


function SVT (ϵ, size, T, N : num ⟨0,0⟩ ; q : list num ⟨∗,∗⟩ )            satisfy differential privacy, as noted in [30]). For noisy query
                                                                          values below the noisy threshold, it only outputs false. We
           returns (out : list bool )
                                                                          call this algorithm GapSparseVector. More specifically, Line 6
 precondition ∀i ≥ 0. − 1 ≤ b            q† [i] = b
                            q◦ [i] ≤ 1 ∧ b        q◦ [i]                  in Figure 6 is changed from out := true::out; to the
 1 η 1 := Lap (2/ϵ) , ◦ , 1 ;                                             following: out := (q[i] + η 2 - T̃ )::out;. To the best of
                                                                          our knowledge, the correctness of this variant has not been
 2 T̃ := T + η 1 ; count := 0; i := 0;
 3  while ( count < N ∧ i < size )                                        noticed before. This variant can be easily verified with little
 4     η 2 := Lap (4N /ϵ) , ◦ , Ω ? 2 : 0 ;                               changes to the original annotation. One observation is that,
                                                                          to align the out variable, the gap appended to the list must
 5     if ( q [ i ] + η 2 ≥ T̃ ) then
 6         out := true :: out ;                                           have 0 aligned distance. Thus we change the distance of η 2
 7         count := count + 1;                                            from Ω ? 2 : 0 to Ω ? (1 − b  q◦ [i]) : 0, the other part of the
 8     else                                                               annotation remains the same.
 9         out := false :: out ;                                             ShadowDP successfully type checks and transforms the
10     i := i + 1;
                                                                          program. Due to the non-linear arithmetics issue, we rewrite
The transformed program (slightly simplified for readability),            the assignment command vϵ := vϵ + (1 − b      q◦ [i]) × ϵ/4N ; to
where underlined commands are added by the type system:
                                                                          assert (|1 − b q◦ [i]| ≤ 2); vϵ := vϵ + 2 × ϵ/4N ; and provide
 1 vϵ := 0;
 2 havoc η 1 ; vϵ := vϵ + ϵ/2;
                                                                          nonlinear loop invariants; then it is verified (we also verified
                                                                          a variant where ϵ is fixed to 1).
 3   T̃ := T + η 1 ; count := 0; i := 0;
 4    while ( count < N ∧ i < size )
 5      assert (count < N ∧ i < size);                                    6.3   Experiments
 6      havoc η 2 ; vϵ = Ω ? (vϵ + 2 × ϵ/4N ) : (vϵ + 0);
                                                                          ShadowDP is evaluated on Report Noisy Max algorithm (Fig-
 7      if ( q [ i ] + η 2 ≥ T̃ ) then
                                                                          ure 1) along with all the algorithms discussed in Section 6.2,
 8        assert (q[i] + b q◦ [i] + η 2 + 2 ≥ T̃ + 1);
                                                                          as well as Partial Sum, Prefix Sum and Smart Sum algorithms
 9        out := true :: out ;
10        count := count + 1;
                                                                          that are included in the Appendix. For comparison, all the
11      else                                                              algorithms verified in [2] are included in the experiments
12        assert (¬(q[i] + b  q◦ [i] + η 2 ≥ T̃ + 1));                    (where Sparse Vector Technique is called Above Threshold
13        out := false :: out ;                                           in [2]). One exception is ExpMech algorithm, since ShadowDP
14      i := i + 1;                                                       currently lacks a sampling command for Exponential noise.
                                                                          However, as shown in [42], it should be fairly easy to add a
                                                                          noise distribution without affecting the rest of a type system.
Figure 6. Verifying Sparse Vector Technique with Shad-                       Experiments are performed on a Dual Intel® Xeon® E5-
owDP (slightly simplified for readability). Annotations are               2620 v4@2.10GHz CPU machine with 64 GB memory. All
in gray where Ω represents the branch condition.                          algorithms are successfully checked and transformed by
                                                                          ShadowDP and verified by CPAChecker. For programs with
                                                                          non-linear arithmetics, we performed experiments on both
of the gap q[i] +η 2 −T̃ (how much larger the noisy answer is             solutions discussed in Section 6.2.2. Transformation and ver-
compared to the noisy threshold). Note that the noisy query               ification all finish within 3 seconds, as shown in Table 1,
value q[i] + η 2 is reused for both this check and the output             indicating the simplicity of analyzing the transformed pro-
(whereas other proposals either (1) draw fresh noise and                  gram, as well as the practicality of verifying ϵ-differentially
result in a larger ϵ [21], or (2) re-use the noise but do not             private algorithms with ShadowDP.
Proving Differential Privacy with Shadow Execution                                PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

6.4   Proof Automation                                            Also, instead of building the system on customized relational
ShadowDP requires two kinds of annotations: (1) function          logics to verify differential privacy [3, 5, 8–10], ShadowDP
specification and (2) annotation for sampling commands. As        bases itself on standard program logics, which makes the
most verification tools, (1) is required since it specifies the   transformed program re-usable by other program analyses.
property being verified. In all of our verified examples, (2)     Other language-based proofs Recent work such as Per-
is fairly simple and easy to write. To further improve the        sonalized Differential Privacy (PDP) [22] allows each individ-
usability of ShadowDP, we discuss some heuristics to auto-        ual to set its own different privacy level and PDP will satisfy
matically generate the annotations for sampling commands.         difference privacy regarding the level she sets. PINQ [32]
   Sampling commands requires two parts of annotation:            tracks privacy consumption dynamically on databases and
1. Selectors. The selector has two options: aligned (◦) or        terminate when the privacy budget is exhausted. However,
   shadow (†), with potential dependence. The heuristic is        along with other work such as computing bisimulations fam-
   to enumerate branch conditions. For Report Noisy Max,          ilies for probabilistic automata [40, 41], they fail to provide a
   there is only one branch condition Ω, giving us four           tight bound on the privacy cost of sophisticated algorithms.
   possibilities: ◦ / † / Ω ? ◦ : † / Ω ? † : ◦.
2. Alignments for the sample. It is often simple arith-           8    Conclusions and Future Work
   metic on a small integer such as 0, 1, 2 or the exact dif-     In this paper we presented ShadowDP, a new language for
   ference of query answers and other program variables.          the verification of differential privacy algorithms. ShadowDP
   For dependent types, we can also use the heuristic of          uses shadow execution to generate more flexible randomness
   using branch conditions. For Report Noisy Max, this will       alignments that allows it to verify more algorithms, such as
   discover the correct alignment Ω ? 2 : 0.                      Report Noisy Max, than previous work based on randomness
This enables the discovery of all the correct annotations for     alignments. We also used it to verify a novel variant of Sparse
the algorithm studied in this paper. We leave a systematic        Vector that reports the gap between noisy above-threshold
study of proof automation as future work.                         queries and the noisy threshold.
                                                                     Although ShadowDP only involves minimum annotations,
7     Related Work                                                one future work is to fully automate the verification using
Randomness alignment based proofs The most related                ShadowDP, as sketched in Section 6.4. Another natural next
work is LightDP [42]. ShadowDP is inspired by LightDP in          step is to extend ShadowDP to support more noise distribu-
a few aspects, but also with three significant differences.       tions, enabling it to verify more algorithms such as ExpMech
First, ShadowDP supports shadow execution, a key enabling         which uses Exponential noise. Furthermore, we plan to in-
technique for the verification of Report Noisy Max based on       vestigate other applications of the transformed program. For
standard program semantics. Second, while LightDP has a           instance, applying symbolic executors and bug finding tools
flow-insensitive type system, ShadowDP is equipped with           on the transformed program to construct counterexamples
a flow-sensitive one. The benefit is that the resulting type      when the original program is buggy.
system is both more expressive and more usable, since only
sampling command need annotations. Third, ShadowDP al-
                                                                  Acknowledgments
lows extra permissiveness of allowing two related executions      We thank our shepherd Dana Drachsler-Cohen and anony-
to take different branches, which is also crucial in verifying    mous PLDI reviewers for their helpful suggestions. This work
Report Noisy Max. In fact, ShadowDP is strictly more expres-      is funded by NSF awards #1228669, #1702760, #1816282 and
sive than LightDP: LightDP is a restricted form of ShadowDP       #1566411.
where the shadow execution is never used (i.e., when the
selector always picks the aligned execution).                     References
                                                                   [1] John M. Abowd. 2018. The U.S. Census Bureau Adopts Differential
Coupling based proofs The state-of-the-art verifier based              Privacy. In Proceedings of the 24th ACM SIGKDD International Confer-
on approximate coupling [2] is also able to verify the algo-           ence on Knowledge Discovery and Data Mining (KDD ’18). ACM, New
rithms we have discussed in this paper. Notably, it is able to         York, NY, USA, 2867–2867.
                                                                   [2] Aws Albarghouthi and Justin Hsu. 2017. Synthesizing Coupling Proofs
automatically verify proofs for algorithms including Report-           of Differential Privacy. Proceedings of ACM Programming Languages 2,
Noisy-Max and Sparse Vector. However, verifying the trans-             POPL, Article 58 (Dec. 2017), 30 pages.
formed program by ShadowDP is significantly easier than            [3] Gilles Barthe, George Danezis, Benjamin Gregoire, Cesar Kunz, and
verifying the first-order Horn clauses and probabilistic con-          Santiago Zanella-Beguelin. 2013. Verified Computational Differential
straints generated by their tool. In fact, ShadowDP verifies           Privacy with Applications to Smart Metering. In Proceedings of the
                                                                       2013 IEEE 26th Computer Security Foundations Symposium (CSF ’13).
all algorithms within 3 seconds while the coupling verifier            IEEE Computer Society, Washington, DC, USA, 287–301.
takes 255 seconds in verifying Smart Sum and 580 seconds           [4] Gilles Barthe, Pedro R. D’Argenio, and Tamara Rezk. 2004. Secure
in verifying Sparse Vector (excluding proof synthesis time).           Information Flow by Self-Composition. In Proceedings of the 17th IEEE
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

     Workshop on Computer Security Foundations (CSFW ’04). IEEE Com-           [18] Zeyu Ding, Yuxin Wang, Guanhong Wang, Danfeng Zhang, and Daniel
     puter Society, Washington, DC, USA, 100–.                                      Kifer. 2018. Detecting Violations of Differential Privacy. In Proceedings
 [5] Gilles Barthe, Noémie Fong, Marco Gaboardi, Benjamin Grégoire,                 of the 2018 ACM SIGSAC Conference on Computer and Communications
     Justin Hsu, and Pierre-Yves Strub. 2016. Advanced Probabilistic Cou-           Security (CCS ’18). ACM, New York, NY, USA, 475–489.
     plings for Differential Privacy. In Proceedings of the 2016 ACM SIGSAC    [19] Cynthia Dwork, Krishnaram Kenthapadi, Frank McSherry, Ilya
     Conference on Computer and Communications Security (CCS ’16). ACM,             Mironov, and Moni Naor. 2006. Our Data, Ourselves: Privacy via
     New York, NY, USA, 55–67.                                                      Distributed Noise Generation. In Proceedings of the 24th Annual Inter-
 [6] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu,         national Conference on The Theory and Applications of Cryptographic
     César Kunz, and Pierre-Yves Strub. 2014. Proving Differential Privacy          Techniques (EUROCRYPT’06). Springer-Verlag, Berlin, Heidelberg, 486–
     in Hoare Logic. In Proceedings of the 2014 IEEE 27th Computer Security         503.
     Foundations Symposium (CSF ’14). IEEE Computer Society, Washington,       [20] Cynthia Dwork, Frank McSherry, Kobbi Nissim, and Adam Smith. 2006.
     DC, USA, 411–424.                                                              Calibrating Noise to Sensitivity in Private Data Analysis. In Theory
 [7] Gilles Barthe, Marco Gaboardi, Emilio Jesús Gallego Arias, Justin Hsu,         of Cryptography, Shai Halevi and Tal Rabin (Eds.). Springer Berlin
     Aaron Roth, and Pierre-Yves Strub. 2015. Higher-Order Approximate              Heidelberg, Berlin, Heidelberg, 265–284.
     Relational Refinement Types for Mechanism Design and Differential         [21] Cynthia Dwork, Aaron Roth, et al. 2014. The algorithmic foundations
     Privacy. In Proceedings of the 42Nd Annual ACM SIGPLAN-SIGACT                  of differential privacy. Theoretical Computer Science 9, 3–4 (2014),
     Symposium on Principles of Programming Languages (POPL ’15). ACM,              211–407.
     New York, NY, USA, 55–68.                                                 [22] Hamid Ebadi, David Sands, and Gerardo Schneider. 2015. Differential
 [8] Gilles Barthe, Marco Gaboardi, Benjamin Grégoire, Justin Hsu, and              Privacy: Now It’s Getting Personal. In Proceedings of the 42Nd An-
     Pierre-Yves Strub. 2016. Proving Differential Privacy via Probabilistic        nual ACM SIGPLAN-SIGACT Symposium on Principles of Programming
     Couplings. In Proceedings of the 31st Annual ACM/IEEE Symposium                Languages (POPL ’15). ACM, New York, NY, USA, 69–81.
     on Logic in Computer Science (LICS ’16). ACM, New York, NY, USA,          [23] Úlfar Erlingsson, Vasyl Pihur, and Aleksandra Korolova. 2014. RAP-
     749–758.                                                                       POR: Randomized Aggregatable Privacy-Preserving Ordinal Response.
 [9] Gilles Barthe, Boris Köpf, Federico Olmedo, and Santiago                       In Proceedings of the 2014 ACM SIGSAC Conference on Computer and
     Zanella Béguelin. 2012. Probabilistic Relational Reasoning for                 Communications Security (CCS ’14). ACM, New York, NY, USA, 1054–
     Differential Privacy. In Proceedings of the 39th Annual ACM SIGPLAN-           1067.
     SIGACT Symposium on Principles of Programming Languages (POPL             [24] Gian Pietro Farina, Stephen Chong, and Marco Gaboardi. 2017. Rela-
     ’12). ACM, New York, NY, USA, 97–110.                                          tional Symbolic Execution. arXiv e-prints, Article arXiv:1711.08349
[10] Gilles Barthe and Federico Olmedo. 2013. Beyond Differential Privacy:          (Nov 2017).
     Composition Theorems and Relational Logic for f-divergences Be-           [25] Anna C. Gilbert and Audra McMillan. 2018. Property Testing For
     tween Probabilistic Programs. In Proceedings of the 40th International         Differential Privacy. 2018 56th Annual Allerton Conference on Commu-
     Conference on Automata, Languages, and Programming - Volume Part               nication, Control, and Computing (Allerton) (2018), 249–258.
     II (ICALP’13). Springer-Verlag, Berlin, Heidelberg, 49–60.                [26] Moritz Hardt, Katrina Ligett, and Frank McSherry. 2012. A Simple
[11] Dirk Beyer and M. Erkan Keremoglu. 2011. CPACHECKER: A Tool for                and Practical Algorithm for Differentially Private Data Release. In
     Configurable Software Verification. In Proceedings of the 23rd Interna-        Proceedings of the 25th International Conference on Neural Information
     tional Conference on Computer Aided Verification (CAV’11). Springer-           Processing Systems - Volume 2 (NIPS’12). Curran Associates Inc., USA,
     Verlag, Berlin, Heidelberg, 184–190.                                           2339–2347.
[12] Benjamin Bichsel, Timon Gehr, Dana Drachsler-Cohen, Petar Tsankov,        [27] Sebastian Hunt and David Sands. 2006. On Flow-sensitive Security
     and Martin Vechev. 2018. DP-Finder: Finding Differential Privacy               Types. In Conference Record of the 33rd ACM SIGPLAN-SIGACT Sympo-
     Violations by Sampling and Optimization. In Proceedings of the 2018            sium on Principles of Programming Languages (POPL ’06). ACM, New
     ACM SIGSAC Conference on Computer and Communications Security                  York, NY, USA, 79–90.
     (CCS ’18). ACM, New York, NY, USA, 508–524.                               [28] Noah Johnson, Joseph P Near, and Dawn Song. 2018. Towards prac-
[13] Mark Bun and Thomas Steinke. 2016. Concentrated Differential Pri-              tical differential privacy for SQL queries. Proceedings of the VLDB
     vacy: Simplifications, Extensions, and Lower Bounds. In Proceedings,           Endowment 11, 5 (2018), 526–539.
     Part I, of the 14th International Conference on Theory of Cryptography    [29] Dexter Kozen. 1981. Semantics of probabilistic programs. J. Comput.
     - Volume 9985. Springer-Verlag New York, Inc., New York, NY, USA,              System Sci. 22, 3 (1981), 328 – 350.
     635–658.                                                                  [30] Min Lyu, Dong Su, and Ninghui Li. 2017. Understanding the sparse
[14] T.-H. Hubert Chan, Elaine Shi, and Dawn Song. 2011. Private and                vector technique for differential privacy. Proceedings of the VLDB
     Continual Release of Statistics. ACM Trans. Inf. Syst. Secur. 14, 3,           Endowment 10, 6 (2017), 637–648.
     Article 26 (Nov. 2011), 24 pages.                                         [31] Frank McSherry and Kunal Talwar. 2007. Mechanism Design via
[15] Jürgen Christ, Jochen Hoenicke, and Alexander Nutz. 2012. SMTIn-               Differential Privacy. In Proceedings of the 48th Annual IEEE Symposium
     terpol: An Interpolating SMT Solver. In Proceedings of the 19th Inter-         on Foundations of Computer Science (FOCS ’07). IEEE Computer Society,
     national Conference on Model Checking Software (SPIN’12). Springer-            Washington, DC, USA, 94–103.
     Verlag, Berlin, Heidelberg, 248–254.                                      [32] Frank D. McSherry. 2009. Privacy Integrated Queries: An Extensible
[16] Alessandro Cimatti, Alberto Griggio, Bastiaan Joost Schaafsma, and             Platform for Privacy-preserving Data Analysis. In Proceedings of the
     Roberto Sebastiani. 2013. The MathSAT5 SMT Solver. In Proceedings              2009 ACM SIGMOD International Conference on Management of Data
     of the 19th International Conference on Tools and Algorithms for the           (SIGMOD ’09). ACM, New York, NY, USA, 19–30.
     Construction and Analysis of Systems (TACAS’13). Springer-Verlag,         [33] I. Mironov. 2017. Rényi Differential Privacy. In 2017 IEEE 30th Computer
     Berlin, Heidelberg, 93–107.                                                    Security Foundations Symposium (CSF). 263–275.
[17] Leonardo De Moura and Nikolaj Bjørner. 2008. Z3: An Efficient SMT         [34] Prashanth Mohan, Abhradeep Thakurta, Elaine Shi, Dawn Song, and
     Solver. In Proceedings of the Theory and Practice of Software, 14th In-        David Culler. 2012. GUPT: Privacy Preserving Data Analysis Made
     ternational Conference on Tools and Algorithms for the Construction            Easy. In Proceedings of the 2012 ACM SIGMOD International Conference
     and Analysis of Systems (TACAS’08/ETAPS’08). Springer-Verlag, Berlin,          on Management of Data (SIGMOD ’12). ACM, New York, NY, USA,
     Heidelberg, 337–340.                                                           349–360.
Proving Differential Privacy with Shadow Execution                                              PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

[35] Kobbi Nissim, Thomas Steinke, Alexandra Wood, Micah Altman, Aaron         [40] Michael Carl Tschantz, Dilsun Kaynar, and Anupam Datta. 2011. For-
     Bembenek, Mark Bun, Marco Gaboardi, David R O’Brien, and Salil Vad-            mal Verification of Differential Privacy for Interactive Systems (Ex-
     han. 2017. Differential privacy: A primer for a non-technical audience.        tended Abstract). Electronic Notes in Theoretical Computer Science 276
     In Privacy Law Scholars Conf.                                                  (Sept. 2011), 61–79.
[36] Indrajit Roy, Srinath T. V. Setty, Ann Kilzer, Vitaly Shmatikov, and      [41] Lili Xu, Konstantinos Chatzikokolakis, and Huimin Lin. 2014. Metrics
     Emmett Witchel. 2010. Airavat: Security and Privacy for MapReduce.             for Differential Privacy in Concurrent Systems. In Formal Techniques
     In Proceedings of the 7th USENIX Conference on Networked Systems               for Distributed Objects, Components, and Systems, Erika Ábrahám and
     Design and Implementation (NSDI’10). USENIX Association, Berkeley,             Catuscia Palamidessi (Eds.). Springer Berlin Heidelberg, Berlin, Hei-
     CA, USA, 20–20.                                                                delberg, 199–215.
[37] Andrei Sabelfeld and Andrew C Myers. 2003. Language-based                 [42] Danfeng Zhang and Daniel Kifer. 2017. LightDP: Towards Automating
     information-flow security. IEEE Journal on selected areas in communi-          Differential Privacy Proofs. In Proceedings of the 44th ACM SIGPLAN
     cations 21, 1 (2003), 5–19.                                                    Symposium on Principles of Programming Languages (POPL 2017). ACM,
[38] Apple Differential Privacy Team. 2017. Learning with Privacy at Scale.         New York, NY, USA, 888–901.
     Apple Machine Learning Journal 1, 8 (2017).                               [43] Dan Zhang, Ryan McKenna, Ios Kotsogiannis, Michael Hay, Ashwin
[39] Tachio Terauchi and Alex Aiken. 2005. Secure information flow as a             Machanavajjhala, and Gerome Miklau. 2018. EKTELO: A Framework
     safety problem. In International Static Analysis Symposium. Springer,          for Defining Differentially-Private Computations. In Proceedings of the
     352–367.                                                                       2018 International Conference on Management of Data (SIGMOD ’18).
                                                                                    ACM, New York, NY, USA, 115–130.
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

Appendix                                                              Lr , ΓM⋆ = r    Ltrue, ΓM⋆ = true Lfalse, ΓM⋆ = false
A ShadowDP Semantics
                                                                                     x + n⋆           , else if Γ ⊢ x : num ⟨n◦, n† ⟩
                                                                                    
                                                                                  ⋆
                                                                           Lx, ΓM =
                                                                                     x                , else
                 JskipKm = unit m
                Jx := eKm = unit (m{JeKm /x })                    Le 1 op e 2 , ΓM⋆ = Le 1 , ΓM⋆ op Le 2 , ΓM⋆ where op = ⊕ ∪ ⊗ ∪ ⊙
         Jη := д, S, nη Km = bind JдK (λv. unit m{v/η})                                             ⋆
                                                                                   e 1 [e 2 ] + eb1 [e 2 ]
                                                                                                                 , if Γ⋆ ⊢ e 1 : list num∗
                 Jc 1 ; c 2 Km = bind (Jc 1 Km ) Jc 2 K
                                                                                   
                                                                              ⋆                    ⋆
                                                                  Le 1 [e 2 ], ΓM = e 1 [e 2 ] + n                , else if Γ⋆ ⊢ e 1 : list numn⋆
                                                                                   

                                   Jc 1 Km if JeKm = true
                                                                                  e 1 [e 2 ]
                                                                                   
                                                                                                                  , else
 Jif e then c 1 else c 2 Km =                                                      
                                   Jc 2 Km if JeKm = false
         Jwhile e do cKm = w ∗ m                                   Le 1 :: e 2 , ΓM⋆ = Le 1 , ΓM⋆ :: Le 2 , ΓM⋆        L¬e, ΓM⋆ = ¬Le, ΓM⋆
                where w ∗ = f ix(λ f . λm.if JeKm = true                    Le 1 ? e 2 : e 3 , ΓM⋆ = Le 1 M⋆ ? Le 2 , ΓM⋆ : Le 3 , ΓM⋆
                   then (bind JcKm f ) else (unit m))
          Jc; return eKm = bind (JcKm ) (λm ′ . unit JeKm′ )      Figure 8. Transformation of numerical expressions for
                                                                  aligned and shadow execution, where ⋆ ∈ {◦, †}.
        Figure 7. ShadowDP: language semantics.
                                                                                                        Lc 1 ; ΓM† = c 1′      Lc 2 ; ΓM† = c 2′
   Given a distribution µ ∈ Dist(A), its support is defined             Lskip, ΓM† = skip
                                                                                                              Lc 1 ; c 2 , ΓM† = c 1′ ; c 2′
as support(µ) ≜ {a | µ(a) > 0}. We use 1a to represent
the degenerate distribution µ that µ(a) = 1 and µ(a ′) = 0                           Lx := e, ΓM† = (b
                                                                                                     x † := Le, ΓM† − x)
if a ′ , a. Moreover, we define monadic functions unit and
bind functions to formalize the semantics for commands:                                   Lc i , ΓM† = c i′ i ∈ {1, 2}
        unit : A → Dist(A) ≜ λa. 1a                                   Lif e then c 1 else c 2 , ΓM† = if Le, ΓM† then c 1′ else c 2′
        bind : Dist(A) → (A → Dist(B)) → Dist(B)
                              Õ                                                                   Lc, ΓM† = c ′
             ≜ λµ. λ f . (λb.   (f a b) × µ(a))
                              a ∈A                                             Lwhile e do c, ΓM† = while Le, ΓM† do c ′
That is, unit takes an element in A and returns the Dirac
distribution where all mass is assigned to a; bind takes µ,                 Figure 9. Shadow execution for commands.
a distribution on A, and f , a mapping from A to distribu-
tions on B (e.g., a conditional distribution of B given A), and
returns the corresponding marginal distribution on B. This             we update xb† to v − x instead of updating the shadow
monadic view avoids cluttered definitions and proofs when              value of x to some value v.
probabilistic programs are involved.
   Figure 7 provides the semantics of commands.                   C      Extra Case Studies
                                                                  In this section, we study extra differentially private algo-
B    Constructing Shadow Execution                                rithms to show the power of ShadowDP. As Section 6.2, the
Figure 8 shows the rule for generating shadow execution ex-       shadow execution part is optimized away when the selectors
pressions as well as aligned execution expressions. Figure 9      never use the shadow variables.
shows the rules for generating shadow execution commands.
The shadow execution essentially replaces each variables x        C.1     Numerical Sparse Vector Technique
with their correspondence (i.e., x + Γ(x)) in c, as standard in   Numerical Sparse Vector Technique [21] is an interesting
self-composition construction [4, 39]. Compared with stan-        variant of Sparse Vector Technique which outputs numerical
dard self-composition, the differences are:                       query answers when the query answer is large. To achieve
 1. Lc, ΓM† is not applicable to sampling commands, since if      differential privacy, like Sparse Vector Technique, it adds
    the original execution takes a sample while the shadow        noise to the threshold T and each query answer q[i]; it then
    execution does not, we are unable to align the sample         tests if the noisy query answer is above the noisy threshold
    variable due to different probabilities.                      or not. The difference is that Numerical Sparse Vector Tech-
 2. For convenience, we use x + n† where Γ ⊢ x : ⟨n◦ , n† ⟩       nique draws a fresh noise η 3 when the noisy query answer is
    whenever the shadow value of x is used; correspondingly,      above the noisy threshold, and then releases q[i]+η 3 instead
Proving Differential Privacy with Shadow Execution                                 PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

of simply releasing true. The pseudo code for this algorithm                  to               q◦ [i]| ≤ 1); vϵ = vϵ + ϵ/3;
                                                                                   assert (| − b
is shown in Figure 10.
                                                                       With manual loop invariants provided, CPAChecker suc-
   In this algorithm, ShadowDP needs an extra annotation for
                                                                     cessfully verified the rewritten program.
the new sampling command of η 3 . We use the same approach
in Gap Sparse Vector Technique for this new sampling com-
                                                                     C.2    Partial Sum
mand. Recall the observation that we want the final output
variable out to have distance ⟨0, −⟩, which implies that the         We now study an ϵ-differentially private algorithm Partial-
numerical query q[i]+η 3 should have distance ⟨0, −⟩. We can         Sum (Figure 11) which simply sums over a list of queries.
deduce that η 3 must have distance −b    q◦ [i] inside the branch,   To achieve differential privacy, it adds noise using Laplace
thus we write “◦, −b  ◦
                     q [i]” for η 3 . The rest of the annotations    mechanism to the final sum and output the noisy sum. One
remain the same as standard Sparse Vector Technique.                 difference from the examples in Section 6.2 is the adjacency
                                                                     assumption: at most one query answer may differ by 1 as
                                                                     specified in the precondition.
function NumSVT (ϵ, size, T, N, : num ⟨0,0⟩ ; q : list num ⟨∗,∗⟩ )
                                                                        In this example, since the noise is added to the final sum,
           returns (out : list num ⟨0,−⟩ )                           it makes no difference if we choose the aligned version or
                                                                     shadow version of normal variables (they are both identi-
 precondition ∀i ≥ 0. − 1 ≤ b            q† [i] = b
                            q◦ [i] ≤ 1 ∧ b        q◦ [i]
                                                                     cal to the original execution). To decide the distance of the
 1   η 1 := Lap (3/ϵ) , ◦ , 1 ;                                      random variable, we want the final output to have distance
 2   T̃ := T + η 1 ; count := 0; i := 0;                             ⟨0, −⟩, it is easy to deduce that the distance of η should be
 3    while ( count < N ∧ i < size )                                 −dsum◦ . Adding the annotation ◦, −dsum◦ to Line 5 in Figure 11,
 4      η 2 := Lap (6N /ϵ) , ◦ , Ω ? 2 : 0 ;                         ShadowDP successfully transforms and verifies the program.
 5       if ( q [ i ] + η 2 ≥ T̃ ) then                              Note that since the cost update command vϵ := vϵ + |d  sum| ×ϵ;
 6       η 3 := Lap (3N /ϵ) , ◦ , − bq◦ [i] ;
                                                                     contains non-linear arithmetic, we carefully rewrite this com-
 7        out := (q[i] + η 3 ):: out ;
                                                                     mand to assert (|d    sum| ≤ 1); vϵ := vϵ + ϵ;. ShadowDP is
 8        count := count + 1;                                        able to type check and verify this algorithm within seconds.
 9     else
10        out := 0:: out ;
11     i := i + 1;                                                   function PartialSum (ϵ, size : num ⟨0,0⟩ ; q : list num ⟨∗,∗⟩ )
The transformed program (slightly simplified for readability),                 returns (out : num ⟨0,−⟩ )
where underlined commands are added by the type system:
 1 vϵ := 0;                                                          precondition ∀i ≥ 0. − 1 ≤ b            q† [i] = b
                                                                                                q◦ [i] ≤ 1 ∧ b        q◦ [i] ∧
 2 havoc η 1 ; vϵ := vϵ + ϵ/3;                                                               q◦ [i] , 0 ⇒ (∀j > i. b
                                                                                             b                     q◦ [j] = 0)
 3   T̃ := T + η 1 ;
 4    count := 0; i := 0;                                            1     sum := 0; i := 0;
 5    while ( count < N ∧ i < size )                                 2     while (i < size )
 6       assert (count < N ∧ i < size);                              3       sum := sum + q[i ];
 7       havoc η 2 ; vϵ = Ω ? (vϵ + 2 × ϵ/6N ) : (vϵ + 0);           4       i := i + 1;
 8      if (q[i] + η 2 ≥ T̃ ) then                                   5   η = Lap (1/ϵ) , ◦ , − sd  um◦ ;
 9        assert (q[i] + b  q◦ [i] + η 2 + 2 ≥ T̃ + 1);              6   out := sum + η;
10                                  q◦ [i]| × ϵ/3N ;
          havoc η 3 ; vϵ = vϵ + | − b                                The transformed program, where underlined commands are added
                                                                     by the type system:
11        out := (q[i] + η 3 ):: out ;
12        count := count + 1;                                        1   sum := 0; i := 0;
13      else                                                         2 s dum◦ := 0;
14        assert (¬(q[i] + b q◦ [i] + η 2 ≥ T̃ + 1));                3   while (i < size )
15        out := 0:: out ;                                           4      assert (i < size);
16      i := i + 1;                                                  5       sum := sum + q[i ];
                                                                     6      sdum◦ := sdum◦ + b
                                                                                             q◦ [i];
                                                                     7       i := i + 1;
Figure 10. Verifying Numerical Sparse Vector Technique               8 havoc η; vϵ := vϵ + |d    sum◦ | × ϵ;
with ShadowDP. Annotations are in gray where Ω represents            9   out := sum + η;
the branch condition.

  For the non-linear issue of the verifier, we rewrite the           Figure 11. Verifying Partial Sum using ShadowDP. Annota-
privacy cost assignment from                                         tions are shown in gray.

                   vϵ = vϵ + | − b
                                 q◦ [i]| × ϵ/3;
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

C.3    Smart Sum and Prefix Sum                                    algorithm is successfully transformed by ShadowDP. How-
Another interesting algorithm SmartSum [14] has been pre-          ever, due to the non-linear issue described in Section 6.1, we
viously verified [6, 9] with heavy annotations. We illustrate      change the commands of Line 6 and Line 12 from
the power of our type system by showing that this algorithm                                       um◦ − b
                                                                                  vϵ := vϵ + | − sd     q◦ [i]| × ϵ;
can be verified with very little annotation burden for the
                                                                                  vϵ := vϵ + | − b
                                                                                                 q◦ [i]| × ϵ;
programmers.
                                                                   to
function SmartSum (ϵ, M, T : num ⟨0,0⟩ q : list num ⟨∗,∗⟩ )                      um◦ − b
                                                                        if (| − sd      q◦ [i]| > 0)
           returns (out : list num ⟨0,−⟩ )                                 assert (| − sdum◦ − b q◦ [i]| ≤ 1); vϵ := vϵ + ϵ ;
                                                                                q [i]| > 0)
                                                                        if (| − b◦
 precondition ∀i ≥ 0. − 1 ≤ b            q† [i] = b
                            q◦ [i] ≤ 1 ∧ b        q◦ [i] ∧                 assert (| − bq◦ [i]| ≤ 1); vϵ := vϵ + ϵ ;
                        q◦ [i] , 0 ⇒ (∀j > i. b
                        b                     q◦ [j] = 0)             Moreover, one difference of this algorithm is that it satis-
                                                                   fies 2ϵ-differential privacy [14] instead of ϵ-differential pri-
1     next := 0; i := 0; sum := 0;
2     while i ≤ T                                                  vacy, thus the last assertion added to the program is changed
3       if ( i + 1) mod M = 0 then                                 to assert (vϵ ≤ 2 × ϵ);. With this CPAChecker is able to
4                                   um◦ − b
          η 1 := Lap (1/ϵ) , ◦ , − sd     q◦ [i] ;                 verify this algorithm.
5         next := sum + q[i] + η 1 ;                                  We also verified a variant of Smart Sum, called Prefix Sum
6         sum := 0;                                                algorithm [2]. This algorithm is a simplified and less precise
7         out := next :: out ;                                     version of Smart Sum, where the else branch is always taken.
8       else                                                       More specifically, we can get Prefix Sum by removing Lines 3
9        η 2 := Lap (1/ϵ) , ◦ , − b  q◦ [i] ;                      - 8 from Figure 12. The annotation remains the same for η 2 ,
10         next := next + q[i] + η 2 ;                             type checking and transformation follows Smart Sum. Note
11         sum := sum + q[i ];                                     that Prefix Sum satisfies ϵ-differential privacy, so the last
12         out := next :: out ;                                    assertion remains unchanged. CPAChecker then verifies the
13     i := i + 1;                                                 transformed Prefix Sum within 2 seconds.
The transformed program:
 1  next :=0; n :=0; i :=0; sum := 0;                              D     Soundness Proof
 2 sdum◦ := 0;                                                     We first prove a couple of useful lemmas. Following the
 3  while ( i < size ∧ i ≤ T )
                                                                   same notations as in Section 5, we use m for original mem-
 4     assert (i < size ∧ i ≤ T);
                                                                   ory and m ′ for extended memory with aligned and shadow
 5     if ( i + 1) mod M = 0 then
                                      um◦ − b
                                            q◦ [i]| × ϵ;
 6        havoc η 1 ; vϵ = vϵ + | − sd
                                                                   variables but not the distinguished privacy tracking variable
 7         next := sum + q[i] + η 1 ;
                                                                   vϵ . Moreover, we assume that memory tracks the entire list
 8         sum := 0;                                               of sampled random values at each point.
           out := next :: out ;
 9
                                                                   Lemma 4 (Numerical Expression). ∀e, m ′, Γ, such that Γ ⊢
10        sdum◦ := 0;
                                                                   e : num ⟨n◦, n† ⟩ , we have
11     else
12                                  q◦ [i]| × ϵ;
          havoc η 2 ; vϵ = vϵ + | − b                                                  JeKm′ + Jn◦ Km′ = JeKΓ◦m′ ,
13         next := next + q[i] + η 2 ;
                                                                                      JeKm′ + Jn† Km′ = JeKΓ†m′ .
14         sum := sum + q[i ];
15         out := next :: out ;                                    Proof. Induction on the inference rules.
16        sdum◦ := sdum◦ + b
                           q◦ [i];
                                                                    • (T-Num): trivial.
17     i := i + 1;
                                                                    • (T-Var): If Γ ◦ (x) is ∗, n◦ is xb◦ . By Definition 3, Γ ◦m ′(x) =
                                                                      m ′(x) + m ′(bx ◦ ). If Γ ◦ (x) = d◦ , n◦ is d◦ . Again, we have
Figure 12. Verifying SmartSum algorithm with ShadowDP.                Γ m (x) = m ′(x) + Jd◦ Km′ by Definition 3. The case for
                                                                        ◦   ′

Annotations are shown in gray.                                        Γ † is similar.
                                                                    • (T-OPlus, T-OTimes, T-Ternary, T-Index): by the induc-
   This algorithm (Figure 12) is designed to continually re-          tion hypothesis (list is treated as a collection of variables
lease aggregate statistics in a privacy-preserving manner.            of the same type).
The annotations are only needed on Line 4 and 9 in Figure 12.                                                                          □
We use the same observation as stated in Section 6.2.2, in
order to make the aligned distance of the output variable          Lemma 5 (Boolean Expression). ∀e, m ′, Γ, such that Γ ⊢ e :
out 0. To do that, we assign distance −d    sum◦ − b
                                                   q◦ [i] to η 1   bool, we have
and −b ◦
      q [i] to η 2 , and use ◦ for both random variables. This                        JeKm′ = JeKΓ◦m′ = JeKΓ†m′ .
Proving Differential Privacy with Shadow Execution                                           PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

Proof. Induction on the inference rules.                                        case, it must be true that Γ2⋆m 1′ (η) , Γ2⋆m 2′ (η): otherwise,
 • (T-Boolean): trivial.                                                        m 1′ = m 2′ by the injectivity check in rule (T-Laplace).
 • (T-Var): the special case where d◦ = d† = 0. Result is                                                                                     □
   true by Definition 3.
 • (T-ODot): by Lemma 4 and induction hypothesis, we                        Proof of Lemma 2
   have Jei Km′ + Jni◦ Km′ = Jei KΓ◦m′ for i ∈ {1, 2}. By the               Proof. Direct implication of Lemma 6.                                    □
   assumption of (T-ODot), we have
  Je 1 ⊙ e 2 Km′ ⇔ J(e 1 + n◦1 ) ⊙ (e 2 + n◦2 )Km′ = Je 1 ⊙ e 2 KΓ◦m′       D.2    Instrumentation
   The case for Γ † is similar.                                             Next, we show a property offered by the auxiliary function
 • (T-Ternary, T-Index): by the induction hypothesis.                       Γ1 , Γ2 , pc ⇛ c ′ used in the typing rules. Intuitively, they allow
                                                                            us to freely switch from one typing environment to another
                                                                        □   by promoting some variables to star type.
D.1    Injectivity                                                          Lemma 7 (Instrumentation). ∀pc, Γ1 , Γ2 , c ′, if (Γ1 , Γ2 , pc) ⇛
We first prove that the type system maintains injectivity.                  c ′, then for any memory m 1′ , there is a unique m 2′ such that
                                                                            Jc ′Km1′ (m 2′ ) , 0 and
Lemma 6. ∀c, c ′, pc, m ′, m 1′ , m 2′ , Γ1 , Γ2 . pc ⊢ Γ1 {c ⇀ c ′ }Γ2 ∧
Jc ′Km′m 1′ , 0 ∧ Jc ′Km′m 2′ , 0, then we have
                                                                                       (
                                                                                           Γ1◦m 1′ = Γ2◦m 2′ ∧ Γ1†m 1′ = Γ2†m 2′ if pc = ⊥
      (m 1′ = m 2′ ) ∨ (∃η. Γ2⋆m 1′ (η) , Γ2⋆m 2′ (η)), ⋆ ∈ {◦, †}                         Γ1◦m 1′ = Γ2◦m 2′                     if pc = ⊤
Proof. By structural induction on c.                                        Proof. By construction, c ′ is deterministic. Hence, there is a
 • Case skip: trivial since it is non-probabilistic.                        unique m 2′ such that JcKm1′ (m 2′ ) , 0.
 • Case x := e: trivial since it is non-probabilistic.                          Consider any variable x ∈ Vars. By the construction of
 • Case c 1 ; c 2 : Let pc ⊢ Γ1 {c 1 ⇀ c 1′ }Γ, pc ⊢ Γ{c 2 ⇀ c 2′ }Γ2 .     c ′, we note that m 1′ (x) = m 2′ (x) and xb◦ differs in m 1′ and m 2′
   There exists some m 3′ and m 4′ such that                                only if Γ1◦ (x) = n and Γ2◦ (x) = ∗. In this case, Γ1◦m 1′ (x) =
                                                                            m 1′ (x) + JnKm1′ = m 2′ (x) + m 2′ (b x ◦ ) = Γ2◦m 2′ (x). Otherwise,
                                                                            Γ1 (x) = Γ2 (x) (since Γ1 ⊑ Γ2 ). When Γ1◦ (x) = Γ2◦ (x) = ∗,
                                                                              ◦          ◦
                Jc 1′ Km′ (m 3′ ) , 0 ∧ Jc 2′ Km3′ (m 1′ ) , 0
                                                                            Γ1◦m 1′ (x) = m 1′ (x) + m 1′ (b
                                                                                                           x ◦ ) = m 2′ (x) + m 2′ (b
                                                                                                                                    x ◦ ) = Γ2◦m 2′ (x).
                Jc 1′ Km′ (m 4′ ) , 0 ∧ Jc 2′ Km4′ (m 2′ ) , 0              When Γ1 (x) = Γ2 (x) = n for some n, Γ1 m 1 (x) = m 1′ (x) +
                                                                                       ◦         ◦                            ◦     ′

   If m 3′ = m 4′ , results is true by the induction hypothesis on          JnKm1′ = m 2′ (x) + JnKm2′ = Γ2◦m 2′ (x).
   c 2′ . Otherwise, we have ∃η. Γ2⋆m 3′ (η) , Γ2⋆m 4′ (η). Hence,              When pc = ⊥, the same argument applies to the case of
   Γ2⋆m 1′ (η) , Γ2⋆m 2′ (η); contradiction.                                Γ1†m 1′ = Γ2†m 2′ .                                                       □
 • Case if e then c 1 else c 2 : let pc ′ ⊢ Γ1 {c i ⇀ c i′ }Γi′. By
   typing rule, we have Γ1′ ⊔ Γ2′ = Γ2 . Given initial memory               D.3    Shadow Execution
   m ′, both executions take the same branch. Without loss                  Next, we show the main properties related to shadow execu-
   of generality assume c 1 is executed. Let Jc 1′ Km′m 3′ , 0,             tion.
   Jc 1′′Km3′ m 1′ , 0, Jc 1′ Km′m 4′ , 0 and Jc 1′′Km4′ m 1′ , 0. There
                                                                            Lemma 8. ∀e, Γ, m ′, if e is well-typed under Γ, we have
   are two cases:
    1. m 3′ = m 4′ : in this case, c 1′′ only changes the value of                                  JLe, ΓM† Km′ = JeKΓ†m′
          x ⋆ to n when Γ2 (x) = ∗ and Γ1′(x) = n. Moreover, we
          have m 1′ (x ⋆ ) = JnKm3′ = JnKm4′ = m 2′ (x ⋆ ) for those        Proof. By structural induction on the e.
          variables. Hence, m 1′ = m 2′ .                                    • e is r , true or false: trivial.
    2. m 3′ , m 4′ : by induction hypothesis, ∃η. m 3′ (η) , m 4′ (η).       • e is x: if Γ † (x) = ∗ (with base type of num), JLx, ΓM† Km′ =
          Hence, m 1′ , m 2′ , and m 1′ (η) , m 2′ (η) for the same η.         m ′(x) + m ′(b    x † ) = JxKΓ†m′ . When Γ(x) = num ⟨d, n† ⟩ , we
   When pc = ⊤, c ′ also includes c † . In this case, result still             have JLx, ΓM Km′ = Jx + n† Km′ = m ′(x)+Jn† Km′ = JxKΓ†m′
                                                                                                 †

   holds after c † since c † is deterministic by construction.                 (by Lemma 4). Otherwise, JLx, ΓM† Km′ = m ′(x) = Γ †m ′(x).
 • Case while e do c: let pc ′ ⊢ Γ ⊔ Γf {c ⇀ c ′ }Γf . We proceed            • e is e 1 op e 2 : by induction hypothesis.
   by induction on the number of iterations:                                 • e is e 1 [e 2 ]: By the typing rule (T-Index), Γ ⊢ e 2 : num ⟨0,0⟩ .
    1. c is not executed: m 1′ = m ′ = m 2′ .                                  Hence, Je 2 KΓ†m′ = Je 2 Km′ by Lemma 4.
    2. c is executed n + 1 times: similar to the c 1 ; c 2 case.               Let Γ ⊢ e 1 : list num ⟨d, d† ⟩ . When e 1 = q and d† = ∗,
   When pc = ⊤, c ′ also includes c † . In this case, result still             JLq[e 2 ], ΓM† Km′ = Jq[e 2 ] + qb† [e 2 ]Km′ = Jq[e 2 ]KΓ†m′ . When
   holds after c † since c † is deterministic by construction.                 d = ∗ and e 1 is not a variable, JLe 1 [e 2 ], ΓM† Km′ is defined
 • Case (η := Lap r ; S, nη ): if m 1′ , m 2′ , we know that                   as JLe 1 , ΓM† [e 2 ]Km′ . By induction hypothesis, this is the
   m 1′ (η) , m 2′ (η) since c ′ only modifies the value of η. In this         same as Je 1 KΓ†m′ J[e 2 ]Km′ = Je 1 [e 2 ]KΓ†m′ .
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

   When d = n† , JLe 1 [e 2 ], ΓM† Km′ is defined as Je 1 [e 2 ] + n† Km′ ,          Next, we show that when pc = ⊤ (i.e., when the shadow
   which is the same as Je 1 [e 2 ]KΓ†m′ (by Lemma 4).                             execution might diverge), the transformed code does not
   Otherwise, result is true by Lemma 5.                                           modify shadow variables and their distances.
 • e is e 1 :: e 2 and ¬e: by induction hypothesis.
                                                                                   Lemma 10 (High PC). ∀c, c ′, Γ1 , Γ2 . ⊤ ⊢ Γ1 {c ⇀ c ′ }Γ2 , then
 • e is e 1 ?e 2 :e 3 : by induction hypothesis, we have JLe 1 , ΓM† Km′ =
                                                                                   we have
   Je 1 KΓ†m′ . Hence, the same element is selected on both
   ends. Result is true by induction hypothesis.                                    1. (∀x ∈ Asgnd(c). Γ2† (x) = ∗) ∧ (Γ1† (x) = ∗ ⇒ Γ2† (x) = ∗)
                                                                                    2. ∀m 1′ , m 2′ . Jc ′Km1′ (m 2′ ) , 0 =⇒ Γ1†m 1′ = Γ2†m 2′
                                                                         □
                                                                                Proof. By structural induction on c.
   Next, we show that shadow execution simulates two exe-                        • c is skip: trivial.
cutions on Γ -related memories via two program executions.
                 †                                                               • c is x := e: When pc = ⊤, Γ2† (x) = ∗ by the typing rule.
                                                                                     (Γ1† (x) = ∗ ⇒ Γ2† (x) = ∗) since Γ2† (y) = Γ1† (y) for y , x.
Lemma 9 (Shadow Execution). ∀c, c † , Γ. (∀x ∈ Asgnd(c). Γ † (x) =                   In this case, c ′ is defined as (b             x † := x + n† − e; x := e)
∗) ∧ Lc, ΓM† = c † , we have                                                                      †
                                                                                    where Γ1 ⊢ x : n . By the semantics, we have m 2′ =
                                                                                                                   †

               ∀m 1′ , m 2′ . Jc † Km1′ (m 2′ ) = JcKΓ†m1′ (Γ †m 2′ ).              m 1′ {Jx + n† − eKm1′ /b        x † }{JeKm1′ /x }. Hence, Γ2m 2′ (x) = m 2′ (x)+
                                                                                     Jx + n† − eKm1′ = JeKm1′ + Jx + n† Km1′ − JeKm1′ = Γ1m 1 (x).
Proof. By structural induction on c. First, we note that the                         For any y , x, both its value and its shadow distance do
construction of shadow execution does not apply to sampling                          not change (due to the wellformedness check in rule (T-
instructions. Hence, c and c † fall into the deterministic por-                     Asgn)). Hence, Γ1†m 1′ (y) = Γ2†m 2′ (y).
tion of programs. Therefore, we write m 2 = JcKm1 when m 2                       • c is c 1 ; c 2 : by induction hypothesis.
is the unique memory such that JcKm1 (m 2 ) = 1, and likewise                    • c is if e then c 1 else c 2 : when pc = ⊤, we have c ′ =
      ′
for c . Then this lemma can be stated as                                             if e then (assert (e ◦ ); c 1′ ; c 1′′) else (assert (¬e ◦ ); c 2′ ; c 2′′).
                                                                                     By the induction hypothesis, we know that c 1′ and c 2′ does
                 m 2′ = Jc † Km1′ =⇒ Γ †m 2′ = JcKΓ†m1′ .                            not modify any shadow variable and their ending typing
                                                                                     environments, say Γ1′, Γ2′, satisfy condition 1. Hence, the
  • c is skip: we have m 1′ = m 2′ in this case. Hence, Γ †m 2′ =                    ending environment Γ1′ ⊔ Γ2′ satisfies condition 1 too.
    Γ †m 1′ = JskipKΓ†m1′ .                                                         To show (2), we assume c 1 is executed without losing
  • c is (c 1 ; c 2 ): let Lc 1 , ΓM† = c 1† and Lc 2 , ΓM† = c 2† and m ′ =         generality. Let m 3′ be the memory state between c 1′ and
        † ′
    Jc 1 Km1 . By induction hypothesis, we have Γ †m ′ = Jc 1 KΓ†m1′ .              c 1′′. By induction hypothesis, Γ1†m 1′ = (Γ1′)†m 3′ . By the
    By language semantics, m 2′ = Jc 2† Km′ . By induction hy-                       definition of Γi , Γ1 ⊔ Γ2 , ⊤ ⇛ c i′′, c 1′′ and c 2′′ only modifies
    pothesis, with Γ † as both the initial and final environ-                       xb◦ , x ∈ Vars. Hence, Γ2†m 2′ = (Γ1′)†m 3′ = Γ1†m 1′ .
    ments, we have Γ †m 2′ = Jc 2 KΓ†m′ = Jc 1 ; c 2 KΓ†m1′                      • c is while e do c ′: by the definition of ⊔ and induction
                                                                                     hypothesis, condition 1 holds.
  • c is x := e: we have c † = (b            x † := Le, ΓM† − x) in this case.
                                                                                     Moreover, by the definition of Γ, Γ ⊔ Γf , ⊤ ⇛ c s , c s only
    Moreover, m 2′ = m 1′ {JLe, ΓM† ) − xKm1′ /b           x † }. By Lemma 8,
                                                                                     modifies xb◦ , x ∈ Vars. Hence, Γ2†m 2′ = Γ1†m 1′ by induction
    we have JLe, ΓM† Km1′ = JeKΓ†m1′ .
                                                                                     on the number of iterations.
    For variable x, we know that Γ(x)† = ∗ by assumption. So                     •  c   is sampling instruction: does not apply since pc = ⊥ in
    Γ †m 2′ (x) = m 2′ (x) + m 2′ (b    x † ) = m 1′ (x) + JLe, Γ2 M† − xKm1′ =      the typing rule.
    JeKΓ†m1′ = Jx := eKΓ†m1′ (x). For a variable y other than
                                                                                                                                                              □
    x, the result is true since both c and c † do not modify
    y and y † , and y’s distances does not change due to the                    Lemma 11. ∀c, c ′, c † , Γ1 , Γ2 . (∀x ∈ Asgnd(c). Γ2† (x) = ∗) ∧
    well-formedness check in typing rule (T-Asgn).                              Lc, Γ2 M† = c † ∧ c ′ is deterministic, and (∀m 1′ , m 2′ . Jc ′Km1′ (m 2′ ) ,
  • c is if e then c 1 else c 2 : let Lc 1 , ΓM† = c 1′ and Lc 2 , ΓM† = c 2′ . 0 =⇒ Γ †m 1′ = Γ †m 2′ ), then we have
    In this case, c = if Le, ΓM then c 1 else c 2 . By Lemma 8,
                        †                  †          ′         ′
                                                                                              ∀m 1′ , m 2′ . Jc ′; c † Km1′ (m 2′ ) = JcKΓ†m′ (Γ2†m 2′ ).
    we have JLe, ΓM† Km1 = JeKΓ†m1 . Hence, both c and c † will                                                                           1 1
                                                                                                    ′
    take the same branch under Γ m 1 and m 1 respectively.
                                                   †   ′         ′              Proof. c and c are deterministic. Hence, this lemma can be
    The desired results follow from induction hypothesis on                     stated as
    c 1 or c 2 .                                                                          ∀m 1′ , m 2′ . m 2′ = Jc ′; c † Km1′ =⇒ Γ2†m 2′ = JcKΓ†m′
  • c is while e do c: again, since JLe, ΓM† Km1 = JeKΓ†m1 . The                                                                                        1 1

    desired result follows from induction on the number of                         Let m 3 = Jc Km1′ and m 2 = Jc Km3′ . By assumption, we
                                                                                            ′           ′                ′          †

    loop iterations.                                                            have Γ2†m 3′ = Γ1†m 1′ . Moreover, by Lemma 9, we have Γ2†m 2′ =
                                                                              □ JcKΓ†m′ . Hence, Γ2†m 2′ = JcKΓ†m′ = JcKΓ†m′ .
                                                                                        2   3                         2   3        1   1
Proving Differential Privacy with Shadow Execution                                                    PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

                                                                                                                                                                     m′
                                                                                         For (2a) and (2b), let ϵ1 = max(c 1′′ ↾m
                                                                                                                                                                 ′
                                                                            □                                                   m′
                                                                                                                                   ), ϵ2 = max(c 2′′ ↾m2′ )
                                                                                                                                                                 1
                                                                                                                        m′
D.4    Soundness                                                                            and ϵ = max(c 1′′; c 2′′ ↾m2′ ). Note that ϵ1 + ϵ2 ≤ ϵ due to
                                                                                                                               1

Finally, we prove the Pointwise Soundness Lemma.                                            the fact that m 2′ ⊎ (ϵ1 + ϵ2 ) ∈ Jc 1′′; c 2′′Km1′ ⊎(0) . By induction
                                                                                            hypothesis we have one of the following two cases.
Proof of Lemma 3                                                                             1. Jc 2′ Km′ (m 2′ ) ≤ exp(ϵ2 )Jc 2 KΓ†m′ (Γ2◦m 2′ ). We have
                                                                                                                 Õ
Proof. By structural induction on c. Note that the desired                           Jc 1′ ; c 2′ Km1′ (m 2′ ) =   Jc 1′ Km1′ (m ′) · Jc 2′ Km′ (m 2′ )
inequalities are trivially true if Jc ′Km1′ (m 2′ ) = 0. Hence, in the                                      m′
                                                                                                                       Õ
proof we assume that Jc ′Km1′ (m 2′ ) > 0.                                                              ≤ exp(ϵ2 )      Jc 1′ KΓ†m′ (Γ †m ′) · Jc 2′ KΓ†m′ (Γ2◦m 2′ )
                                                                                                                                         1           1
 • Case (skip): trivial.                                                                                                m′
                                                                                                                  Õ
                                                              m′                                        ≤ exp(ϵ2 ) Jc 1′ KΓ†m′ (m ′) · Jc 2′ Km′ (Γ2◦m 2′ )
 • Case (x := e): by (T-Asgn), we have max(c ′′ ↾m2′ ) = 0.                                                                              1           1
                                                                1
                                                                                                                        m′
   This command is deterministic in the sense that when
   Jc ′Km1′ (m 2′ ) , 0, we have Jc ′Km1′ (m 2′ ) = 1 and m 2′ =                                        ≤ exp(ϵ2 )Jc 1 ; c 2 KΓ†m′ (Γ2◦m 2′ )
                                                                                                                                     1           1

   m 1′ {JeKm1′ /x }. To prove (1) and (2a), it suffices to show                                        ≤ exp(ϵ)Jc 1 ; c 2 KΓ†m′ (Γ2◦m 2′ ).
                                                                                                                                 1           1
   that Γ2†m 2′ = Γ1†m 1′ {JeKΓ†m′ /x } and Γ2◦m 2′ = Γ1◦m 1′ {JeKΓ1◦m1′ /x }.
                               1 1                                                                The first inequality is by induction hypothesis. The
   We prove the latter one as the other (given pc = ⊥) can                                         change of variable in the third line is again due to
   be shown by a similar argument.                                                                 Lemma 2. The last line is because ϵ1 + ϵ2 ≤ ϵ.
   First, we show Γ2◦m 2′ (x) = Γ1◦m 1′ {JeKΓ1◦m1′ /x }(x). Let Γ1 ⊢                         2. Jc 2′ Km′ (m 2′ ) ≤ exp(ϵ2 )Jc 2 KΓ◦m′ (Γ2◦m 2′ ). By induction
   e : ⟨n◦ , n† ⟩. By the typing rule, we have Γ2◦ (x) = n◦ , and                                  hypothesis on c 1 , we have two more cases:
                                                                                                    a. Jc 1′ Km1′ (m ′) ≤ exp(ϵ1 )Jc 1 Km1◦ (m◦ ). In this case,
                 Γ2◦m 2′ (x) = m 2′ (x) + Jn◦ Km2′
                             = JeKm1′ + Jn◦ Km2′
                                                                                                                   Õ
                                                                                     Jc 1′ ; c 2′ Km1′ (m 2′ ) =      Jc 1′ Km1′ (m ′) · Jc 2′ Km′ (m 2′ )
                             = JeKm1′ + Jn◦ Km1′                                                            m′
                                                                                                                      Õ
                             = JeKΓ1◦m1′                                                                ≤ exp(ϵ)       Jc 1 KΓ1◦m1′ (Γ ◦m ′) · Jc 2 KΓ◦m′ (Γ2◦m 2′ )
                                                                                                                       m′
                             = Γ1◦m 1′ {JeKΓ1◦m1′ /x }(x).                                                      Õ
                                                                                                        ≤ exp(ϵ) Jc 1 KΓ1◦m1′ (m ′) · Jc 2 Km′ (Γ2◦m 2′ )
   The third equality is due to well-formedness, and the                                                               m′
   forth equality is due to Lemma 4.                                                                    ≤ exp(ϵ)Jc 1 ; c 2 KΓ1◦m1′ (Γ2◦m 2′ ).
   Second, we show that Γ2◦m 2′ (y) = Γ1◦m 1′ {JeKΓ1◦m1′ /x }(y) for
                                                                                                 The second line is by induction hypothesis and
   y , x. First, by Rule (T-Asgn), Γ2◦ (y) = Γ1◦ (y), m 1′ (y) =
                                                                                                 the fact that ϵ1 + ϵ2 ≤ ϵ. The change of variable
                      y ◦ ) = m 2′ (b
   m 2′ (y) and m 1′ (b             y ◦ ). If Γ2◦ (y) = Γ1◦ (y) = ∗, Γ2◦m 2′ (y) =
                                                                                                 in the third line is due to Lemma 2.
   m 2 (y) + m 2 (b
      ′          ′  y ) = m 1 (y) + m 1′ (b
                      ◦       ′                y ◦ ) = Γ1◦m 1′ (y). If Γ2◦ (y) =
                                                                                              b. Jc 1′ Km1′ (m ′) ≤ exp(ϵ1 )Jc 1 KΓ†m′ (Γ ◦m ′). We have
   Γ1 (y) = n, Γ2 m 2 (y) = m 2 (y) + JnKm2′ = m 1′ (y) + JnKm1′ =
     ◦              ◦   ′            ′
                                                                                                                                                         1   1

   Γ1◦m 1′ (y), where JnKm2′ = JnKm1′ due to well-formedness.                                   Jc 1′ ; c 2′ Km1′ (m 2′ ) ≤ exp(ϵ)Jc 1 ; c 2 KΓ†m′ (Γ2◦m 2′ )
 • Case (c 1 ; c 2 ): For any m 2′ such that Jc 1′ ; c 2′ Km1′ (m 2′ ) , 0,                                                                    1 1

   there exists some m ′ such that                                                              by a similar argument as above.
                                                                                      • Case (if e then c 1 else c 2 ): If Γ1 ⊢ e : bool, then by
                 Jc 1′ Km1′ (m ′) , 0 ∧ Jc 2′ Km′ (m 2′ ) , 0.                          Lemma 5 we have JeKm1′ = JeKΓ1◦m1′ = JeKΓ†m′ . Hence,
                                                                                                                                      1 1
    Let pc ⊢ Γ1 {c 1 ⇀ c 1′ }Γ, pc ⊢ Γ{c 2 ⇀ c 2′ }Γ2 For (1), we                       the same branch is taken in all related executions. By
    have                                                                                rule (T-If), the transformed program is
                                                                                     if e then (assert (LeM◦ ); c 1′ ; c 1′′) else (assert (¬LeM◦ ); c 2′ ; c 2′′)
                                Õ
    Jc 1′ ; c 2′ Km1′ (m 2′ ) =  Jc 1′ Km1′ (m ′) · Jc 2′ Km′ (m 2′ )
                            m′
                            Õ                                                            and Γ1 , Γ1 ⊔ Γ2 , ⊥ ⇛ c 1′′, Γ2 , Γ1 ⊔ Γ2 , ⊥ ⇛ c 2′′. Without
                        ≤        Jc 1 KΓ†m′ (Γ m ) · Jc 2 KΓ†m′ (Γ2†m 2 )
                                               †   ′
                                                                                         loss of generality, suppose that c 1 is executed in all related
                                        1 1
                            m′                                                           executions. By Lemma 7, there is a unique m ′ such that
                                                                                         Jc 1′ Km1′ (m ′) , 0. By induction hypothesis, we have
                            Õ
                        ≤        Jc 1 KΓ†m′ (m ′) · Jc 2 Km′ (Γ2†m 2′ )
                                       1   1
                            m′
                                                                                                         Jc 1′ Km1′ (m ′) ≤ Jc 1 KΓ†m1′ (Γ1†m ′)
                        = Jc 1 ; c 2 KΓ†m′ (Γ2†m 2′ ).
                                      1    1
                                                                                         Moreover, by Lemma 7, Γ1†m ′ = Γ1†m 2′ and
    Here the second line is by induction hypothesis. The
    change of variable in the third line is due to Lemma 2.                                              Jc 1′ ; c 1′′Km1′ (m 2′ ) = Jc 1′ Km1′ (m ′).
PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA Yuxin Wang, Zeyu Ding, Guanhong Wang, Daniel Kifer, and Danfeng Zhang

    Hence, we have                                                                    and ⊤ ⊢ Γ1 ⊔ Γf {c ⇀ c ′ } Γf , (Γ1 , Γ1 ⊔ Γf , ⊤) ⇛ c s and
       Jc 1′ ; c 1′′Km1′ m 2′ ≤ Jc 1 KΓ†m1′ (Γ1†m ′) = Jc 1 KΓ†m1′ (Γ1†m 2′ )         (Γf , Γ ⊔ Γf , ⊤) ⇛ c ′′. Since we do not have sampling
                                                                                      instructions in this case, the program is deterministic,
    (2a) or (2b) can be proved in a similar way.                                      thus max(W ′′ ↾m     m 1 ) = 0. Note that by rule (T-Asgn),
                                                                                                             2

    When Γ1 ̸⊢ e : bool, the aligned execution will still take                        ∀x ∈ Asgnd(c), Γf (x) = ∗. Hence, Γ2† (x) = ∗ for x ∈
                                                                                                             †
    the same branch due to the inserted assertions. Hence,
                                                                                      Asgnd(c). Morevoer, let m ′ be the unique memory such
    the argument above still holds for (2a) or (2b).
                                                                                      that Jc s Km1′ (m ′) , 0, we have Γ1†m 1′ = Γ2†m ′ by Lemma 7.
    For the shadow execution, we need to prove (1). By rule (T-
                                                                                      Therefore, by Lemmas 10 and 11, we have
    If), pc ′ = ⊤, and the transformed program is
if e then (assert (LeM◦ ); c 1′ ; c 1′′) else (assert (¬LeM◦ ); c 2′ ; c 2′′);    JW ′Km1′ (m 2′ ) = JW ′′Km′ (m 2′ ) = JW KΓ†m′ (Γ2†m 2′ ) = JW KΓ†m′ (Γ2†m 2′ )
Lif e then c 1 else c 2 , Γ1 ⊔ Γ2 M†
                                                                                                                                  2                    1   1



   By Lemma 10 and the definition of ⇛ under high pc,                              • Case (η := Lap r ; S, nη ): let µ r be the probability den-
   we have that ∀m 1′ , m 2′ . Jc ′Km1′ (m 2′ ) , 0 ⇒ Γ2†m 1′ = Γ1†m 1′ ,            sity (resp. mass) function of the Laplace (resp. discrete
   and Γ1 ⊔ Γ2 (x) = ∗ ∀x ∈ Asgnd(c 1 ; c 2 ). Furthermore, the                      Laplace) distribution with zero mean and scale r . Since
   program is deterministic since it type-checks under ⊤.                            µ r (v) ∝ exp(−|v |/r ) we have
   Therefore, max(W ′′ ↾m  m 1 ) = 0 and (1) holds by Lemma 11.
                              2

 • Case (while e do c): Let W = while e do c. If Γ1 ⊢ e :                                     ∀v, d ∈ R, µ r (v) ≤ exp(|d |/r )µ r (v + d).                    (4)
   bool, then JeKm1′ = JeKΓ2◦m1′ = JeKΓ†m′ . By rule (T-While)
                                               2 1
   we have pc ′ = ⊥, Γ2 = Γ ⊔ Γf and the transformed pro-                             When Jc ′Km1′ (m 2′ ) , 0, we have m 2′ = m 1′ {v/η} for some
   gram is                                                                            constant v, and Jc ′Km1′ (m 2′ ) = µ r (v).
          W ′ = c s ; while e do (assert (LeM◦ ); c ′; c ′′)                          We first consider the case S = ◦. By (T-Laplace), we have
                                                                                      Γ2 (x) = Γ1 (x) for x , η, and Γ2 (η) = ⟨nη , 0⟩. Therefore,
    where ⊥ ⊢ Γ1 ⊔ Γf {c ⇀ c ′ } Γf , (Γ1 , Γ1 ⊔ Γf , ⊥) ⇛ c s and                    for x , η, we have
    (Γf , Γ1 ⊔ Γf , ⊥) ⇛ c ′′. We proceed by natural induction
    on the number of loop iterations (denoted by i).
                                                                                                     Γ2†m 2′ (x) = m 2′ (x) + JΓ2† (x)Km2′
    When i = 0, we have JeKm1′ = false. By the semantics,
    we have JW ′Km1′ = unit (Jc s Km1′ ), JW KΓ1◦m1′ = unit (Γ1◦m 1′ ),                                          = m 1′ (x) + JΓ1† (x)Km2′
    and JW KΓ†m′ = unit (Γ1†m 1′ ). Furthermore, max(W ′′ ↾m    m1
                                                                   2
                                                                                                                 = m 1′ (x) + JΓ1† (x)Km1′
                 1   1
    ) = 0. By Lemma 7, (Γ1◦m 1′ ) = (Γ2◦ (Jc s Km1′ )) and (Γ1†m 1′ ) =                                          = Γ1†m 1′ (x).
    (Γ2† (Jc s Km1′ )). So desired result holds.
    When i = j + 1 > 0, we have JeKm1′ = true. By the                                 In the second equation, we have m 2′ (x) = m 1′ (x) because
    semantics, we have JW ′Km1′ = Jc s ; c ′; c ′′; c ′; c ′′Km1′ and                 m 2 = m 1 {v/η} and x , η. The third equation is due to the
                                                                                      well-formedness assumption. Also, Γ2†m 2′ (η) = m 2′ (η) = v
                                         |{z}
                                                            j
    JW KΓ1⋆m1′ = Jc s ; c ′; c ′′; c ′; c ′′KΓ1⋆m1′ , ⋆ ∈ {◦, †}. For any m ′         since Γ2† (η) = 0. Therefore, we have Γ2†m 2′ = Γ1†m 1′ {v/η}
                                                                                      and thus JcKΓ†m′ (Γ2†m 2′ ) = µ r (v) = Jc ′Km1′ (m 2′ ).
                        |{z}
                              j                                                                      1 1
    such that Jc s ; c ′; c ′′;Km1′ (m ′) = k 1 , 0 and Jc ′; c ′′Km′ (m 2′ ) =       Similarly, we can show that Γ2◦m 2′ = Γ1◦m 1′ {v + d/η} and
                     |{z}                                                             therefore JcKΓ1◦m1′ (Γ2◦m 2′ ) = µ r (v + d). Furthermore, since
                          j
    k 2 , 0, we know that J c KΓ1⋆m1′ (Γ2⋆m ′) = k 1 . More-                          vϵ := vϵ + |nη |/r , the set (c ′′ ↾m     m 1 ) contains a single
                                                                                                                                  2

                           |{z}                                                       element J|nη |/r Km2 = |d|/r , and thus max(c ′′ ↾m        m1 ) =
                                                                                                                                                   2

                                           j                                          |d|/r . Therefore, we have
    over, there is a unique m 3′ such that Jc ′Km′ (m 3′ ) = k 2 ∧
    Jc ′′Km3′ (m 2′ ) = 1 by Lemma 7. By structural induction on c,
                                                                          m′
                                                                                          Jc ′Km1′ (m 2′ ) = µ r (v)
    we have k 1 ≤ JcKΓ†m′ (Γf†m 3′ ) and either k 1 ≤ exp(max(c ′ ↾m2′
                           2                                               1                             ≤ exp(|d|/r )µ r (v + d)
                                                 m′
    ))JcKΓ2◦m′ (Γf◦m 3′ ) or k 1 ≤ exp(max(c ′′ ↾m2′ ))JcKΓ†m′ (Γf◦m 3′ ).                               = exp(max(c ′′ ↾m                  ◦
                                                                                                                         m 1 ))JcKΓ1◦ m 1 (Γ2 m 2 ).
                                                                                                                           2
                                                  1        2
    By Lemma 7, Γf⋆m 3′ = Γ2⋆m 2′ . Hence, we can replace Γf
    with Γ2 in the inequalities. Finally, the desired result holds                    The second inequality is due to (4). Thus (1) and (2a) hold.
    following the same argument as in the composition case.                           Next consider the case S = †. By the typing rule, we have
    Otherwise, by rule (T-While) we have pc ′ = ⊤, Γ2 = Γ⊔Γf                          Γ2◦ (x) = Γ2† (x) = Γ1† (x) for x , η, and Γ2 (η) = ⟨nη , 0⟩.
    and the transformed program is W ′ = c s ;W ′′ where                              By a similar argument we have Γ2†m 2′ = Γ1†m 1′ {v/η} and
W ′′ = while e do (assert (LeM◦ ); c ′; c ′′); Lwhile e do c, Γ2 M†                   Γ2◦m 2′ = Γ1†m 1′ {v + d/η}. Furthermore, since vϵ := 0 +
Proving Differential Privacy with Shadow Execution                                PLDI ’19, June 22–26, 2019, Phoenix, AZ, USA

                                  m′
   |nη |/r , we have max(c ′′ ↾m2′ ) = |d|/r . Therefore, we have   E    Formal Semantics for the Target
                                    1
                                                                         Language
      Jc ′Km1′ (m 2′ ) = µ r (v) = JcKΓ†m′ (Γ2†m 2′ )
                                        1   1                       The denotational semantics interprets a command c in the
                     ≤ exp(|d|/r )µ r (v + d)                       target language as a function JcK : M → P(M). The seman-
                                            m′                      tics of commands are formalized as follows.
                    = exp(max(c ′′ ↾m2′ ))JcKΓ†m′ (Γ2◦m 2′ ).
                                                1   1   1
                                                                                    JskipKm = {m}
   Thus (1) and (2b) hold.
   Finally, consider S = e ? S1 : S2 . For any m 1′ , we have                      Jx := eKm = {m{JeKm /x }}
   S = S1 if JeKm1′ = true and S = S2 if JeKm1′ = false. By                      Jhavoc xKm = ∪r ∈R {m{r /x }}
   induction, S evaluates to either ◦ or † under m 1′ . Thus                        Jc 1 ; c 2 Km = ∪m′ ∈Jc 1 Km Jc 2 Km′
   the proof follows from the the two base cases above.                                             (
                                                                                                      Jc 1 Km if JeKm = true
                                                            □       Jif e then c 1 else c 2 Km =
                                                                                                      Jc 2 Km if JeKm = false
                                                                            Jwhile e do cKm = w ∗ m
                                                                                   where w ∗ = f ix(λ f . λm.if JeKm = true
                                                                                                   then (∪m′ ∈Jc Km f m ′) else {m})
                                                                              Jc; return eKm = ∪m′ ∈Jc Km {JeKm′ }
