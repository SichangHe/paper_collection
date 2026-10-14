                                           Compositional Verification of Procedural Programs
                                             using Horn Clauses over Integers and Arrays
                                                        Anvesh Komuravelli                                               Nikolaj Bjørner                                     Arie Gurfinkel              Kenneth L. McMillan
                                               Computer Science Department                                           Microsoft Research                               Software Engineering Institute      Microsoft Research
                                                Carnegie Mellon University                                           Redmond, WA, USA                                  Carnegie Mellon University         Redmond, WA, USA
                                                   Pittsburgh, PA, USA                                                                                                     Pittsburgh, PA, USA
arXiv:1508.01288v1 [cs.LO] 6 Aug 2015




                                           Abstract—We present a compositional SMT-based algorithm                                                                    memory into registers (e.g., [2], [15]). However, the inlining
                                        for safety of procedural C programs that takes the heap into                                                                  approach has many drawbacks. It can expand the program size
                                        consideration as well. Existing SMT-based approaches are either                                                               exponentially, it cannot handle recursion, and it is not always
                                        largely restricted to handling linear arithmetic operations and
                                        properties, or are non-compositional. We use Constrained Horn                                                                 feasible to eliminate heap and array accesses.
                                        Clauses (CHCs) to represent the verification conditions where the                                                                We address this issue here by considering the problem of
                                        memory operations are modeled using the extensional theory of                                                                 MBP for the extensional theory of arrays (ARR). We find that
                                        arrays (ARR). First, we describe an exponential time quantifier                                                               a finite MBP exists that can be computed in polynomial time
                                        elimination (QE) algorithm for ARR which can introduce new                                                                    when only array-valued variables are projected. Projecting
                                        quantifiers of the index and value sorts. Second, we adapt the
                                        QE algorithm to efficiently obtain under-approximations using                                                                 variables of index and value sorts is not always possible, since
                                        models, resulting in a polynomial time Model Based Projection                                                                 the quantifier-free fragments of the theory combinations are
                                        (MBP) algorithm. Third, we integrate the MBP algorithm into the                                                               not guaranteed to be closed under projection. We therefore take
                                        framework of compositional reasoning of procedural programs                                                                   a pragmatic approach to MBP that may not always converge
                                        using may and must summaries recently proposed by us. Our                                                                     to the exact projection. This allows us to handle, for example,
                                        solutions to the CHCs are currently restricted to quantifier-
                                        free formulas. Finally, we describe our practical experience over                                                             the combination of ARR and LIA.
                                        SV-COMP’15 benchmarks using an implementation in the tool                                                                        We test the effectiveness of this approach using the model
                                        S PACER.                                                                                                                      checking framework of S PACER [17]. This SMT-based frame-
                                                                                                                                                                      work makes use of MBP to produce proof sub-goals for
                                                                                  I. I NTRODUCTION                                                                    Hoare-style procedure-modular proofs of recursive programs.
                                            Under-approximating a projection (i.e., existential quan-                                                                 The ability to reason with ARR makes it possible to handle
                                        tification), for example in computing an image, is a key                                                                      heap-allocating programs without inlining procedures, as the
                                        aspect of many techniques of symbolic model checking. A                                                                       heap can be faithfully modeled using ARR [14]. This leads
                                        typical (though not ubiquitous) approach to this is what we                                                                   to significant improvements in scalability, when compared
                                        call Model-based Projection (MBP) [17]: we generalize a                                                                       to the use of LIA alone with inlining, as measured using
                                        particular point in the space of the image (obtained using                                                                    benchmark programs from the 2015 Software Verification
                                        a model) to a subset of the image that contains it. In some                                                                   Competition (SVCOMP 2015) [4]. Not inlining the programs
                                        cases, the purpose is to compute the exact image by a series                                                                  also has the advantage that we generate procedure-modular
                                        of under-approximations [12]. In other cases, such as IC3 [6],                                                                proofs (containing procedure summaries) that might be re-
                                        the purpose of MBP is to produce a relevant proof sub-goal.                                                                   usable in various ways (e.g., [11]).
                                        When the number of possible generalizations is finite, we say                                                                    In summary, we (a) describe an exponential rewriting pro-
                                        that we have a finite MBP which allows us to compute the                                                                      cedure for projecting array variables (Sec. III-A), (b) adapt
                                        exact image by iterative sampling, or to guarantee that the                                                                   this procedure to obtain a polynomial-time (per model) finite
                                        branching in our proof search is finite.                                                                                      MBP for projecting array variables (Sec. III-B), (c) integrate
                                            The feasibility of a finite MBP depends on the underlying                                                                 this with existing MBP procedures for Linear Arithmetic
                                        logical theory. Finite MBPs exist for propositional logic [12],                                                               (Sec. III-C) in the S PACER framework obtaining a new com-
                                        [16] and Linear Integer Arithmetic (LIA) with a divisibility                                                                  positional proof search algorithm (Sec. IV), and (d) evaluate
                                        predicate [17], and have been applied in both hardware and                                                                    the algorithm experimentally using SVCOMP benchmarks
                                        software model checking. LIA is often adequate for software                                                                   (Sec. V).
                                        verification, provided that heap and array accesses can be
                                                                                                                                                                                           II. P RELIMINARIES
                                        eliminated. This can be done by abstraction, or by inlining
                                        all procedures and performing compiler optimizations to lower                                                                    We consider a first-order language with equality whose
                                                                                                                                                                      signature S contains basic sorts (e.g., bool of Booleans, int
                                           This material is based upon work funded and supported by the Department of Defense under Contract No. FA8721-05-           of integers, etc.) and array sorts. An array sort arr(I, V ) is
                                        C-0003 with Carnegie Mellon University for the operation of the Software Engineering Institute, a federally funded research
                                        and development center. This material has been approved for public release and unlimited distribution. DM-0002442.            parameterized by a sort of indices I and a sort of values V .
We assume that I is always a basic sort. For every array sort          operator Proj is a finite MBP if its image is finite up to logical
arr(I, V ), the language has the usual function symbols rd :           equivalence (that is, over all models we obtain only finitely
arr(I, V )×I → V and wr : arr(I, V )×I×V → arr(I, V )                  many semantically distinct formulas).1 In this case, we obtain
for reading from and writing to the array. Intuitively, rd (a, i)      the exact projection as the disjunction of the image of Proj .
denotes the value stored in the array a at the index i and             We will refer to Proj (M ) as a generalization of M .
wr (a, i, v) denotes the array obtained from a by replacing the           In some cases, there is a trivial approach to MBP that we
value at the index i by v. We use the following axioms for             will call the substitution approach. We simply substitute for
the extensional theory of arrays (ARR):                                each variable x in ϕ a constant that is equal to x in the given
  Read-after-write                                                     model M (for example, a numeric literal). This approach was
  ∀a : arr(I, V ) ∀i, j : I ∀v : V                                     taken for propositional logic by Ganai et al. [12]. For theories
                                                                       that admit models of unbounded size (e.g., LIA), however,
           (i = j =⇒ rd (wr (a, i, v), j) = v) ∧                       this does not yield a finite MBP, as the number of distinct
           (i 6= j =⇒ rd (wr (a, i, v), j) = rd (a, j))                generalizations we obtain can be infinite.
                                                                          Instead, we can take the approach used for Linear Real
   Extensionality
                                                                       Arithmetic and LIA in our earlier work [17]. Suppose that for
   ∀a, b : arr(I, V ) · (∀i : I · rd(a, i) = rd (b, i)) =⇒ a = b
                                                                       the given theory we have a QE procedure that produces a for-
   Intuitively, the first schema says that after modifying an
                                                                       mula with an exponential (or higher) number of disjunctions.
array a at index i, a read results in the new value at index
                                                                       We can adapt this procedure to an MBP by always choosing
i and rd (a, j) at every other index j. The second schema
                                                                       just one disjunct that is true in the given model M . The result
says that if two arrays agree on the values at every index
                                                                       may be a procedure that is polynomial for any given model,
location, the arrays are equal. We use an over-bar to denote
                                                                       though the number of distinct generalizations is exponential.
a vector. We write x : S to denote that every term in vector
                                                                       We will show how to apply this idea for the projection of array-
x has sort S, x(k) to denote the kth component of x, and
                                                                       valued variables in the theory of arrays ARR. When combining
y ∈ x to denote that y is equal to some component of x, i.e.,
W|x|                                                                   this theory with LIA, we will find that some variables of index
  k=1 y = x(k). Let i : I and v : V be vectors of index and            and value sorts must be eliminated by the substitution method,
value terms of the same length m. We write wr (a, i, v) to
                                                                       which gives us a useful MBP but not necessarily a finite MBP.
denote wr (wr (. . . wr (a, i(0), v(0)) . . . ), i(m), v(m)). Unless
specified otherwise, S contains no other symbols.                      A. Quantifier elimination for ARR
   For arrays a and b of sort arr(I, V ), and a (possibly                 Consider an existentially quantified formula ∃a :
empty) vector of index terms i, we write          a =i b to denote    arr(I, V ) · ϕ where ϕ is quantifier-free. While we cannot
∀j : I· j 6∈ i =⇒ rd(a, j) = rd (b, j) and call such formulas          always obtain an equivalent quantifier-free formula, our ob-
partial equalities [20]. Using extensionality, one can easily          jective here is to obtain an equivalent existentially quantified
show the following                                                     formula where every quantifier (if any) is of the sort I or V .
            a =∅ b ≡ a = b                                      (1)    As a simplification, we restrict the interpretations of I, the
                                                                      index sort, to infinite domains. Handling finite index domains
                        j ∈ i ∧ a =i b ∨                               requires a slight adaptation of the algorithms as described in
   wr (a, j, v) =i b ≡                                        (2)
                         j 6∈ i ∧ a =i,j b ∧ rd (b, j) = v             Appendix A.
             a =i b ≡ ∃v : V · a = wr (b, i, v)                 (3)      A RRAY QE(∃a · ϕ)
                                                                       1     ϕ1 ← (E LIM W R∗ )(∃a · ϕ)
   We write ϕ(x) for a formula ϕ with free variables x, and we               ϕW2 ← (C ASE
                                                                                        S PLIT E Q ; FACTOR R D )(ϕ1 )
                                                                                                     ∗              ∗
                                                                       2
treat φ as a predicate over x. We also write ϕ[t] to to indicate       3
                                                                                 n
                                                                                     δ   ←  L IFT E Q D ISEQ R D(ϕ  )
                                                                                 k=1 k                            2
that a term or formula t occurs in ϕ at some syntactic position.       4     for k ∈ [1, n] do
   Given formulas ϕA (x, z) and ϕB (y, z) with x ∩ y = ∅ and           5          ψk ← (E LIM E Q; E LIM D ISEQ; ACKERMANN)(δk )
                                                                                     W
ϕA =⇒ ϕB , a Craig Interpolant [7], denoted I TP(ϕA , ϕB ),            6     return n  k=1 ψk
is a formula ϕI (z) such that ϕA =⇒ ϕI and ϕI =⇒ ϕB .                  Algorithm 1: QE for ∃a · ϕ, where a is an array variable.
         III. QE AND MBP FOR THE THEORY ARR
                                                                          Our algorithm is inspired by the decision procedure for the
  By projection of a variable we mean elimination of an                quantifier-free fragment of ARR by Stump et al. [20]. At a
existential quantifier. Consider a formula ϕ of the form               high level, the QE algorithm proceeds in 3 steps: (i) eliminate
∃x · ϕqf (x, y) where ϕqf is quantifier-free. The problem              write terms using the read-after-write axiom schema and par-
of quantifier elimination (QE) in ϕ is to find a logically             tial equalities over arrays, (ii) eliminate (partial) equalities and
equivalent quantifier-free formula ψ(y). In this case, we say          disequalities over arrays, and (iii) eliminate read terms over
that ψ is the result of projecting x in ϕqf .                          arrays. Alg. 1 shows the pseudo-code for our QE algorithm
  A model-based projection (MBP) for ϕ is an operator Proj             A RRAY QE using the rewrite rules in Fig. 1, 2, and 3. Each rule
that takes a model M of ϕqf and returns a quantifier-free
formula ψM (y) such that M |= ψM and ψM entails ϕ. The                     1 MBP as defined in [17] corresponds to finite MBP here.
                                                                                                              ϕ[wr (t1 , j, v) =i t2 ]
                                                                                    E LIM W R E Q                                 
                                   ϕ[rd (wr (t, i, v), j)]                                                  j ∈ i ∧ ϕ[t1 =i t2 ] ∨           
         E LIM W R R D                                                                               j 6∈ i ∧ ϕ[t1 =i,j t2 ∧ v = rd (t2 , j)]
                          (i = j ∧ ϕ[v]) ∨ (i 6= j ∧ ϕ[rd (t, j)])


                        ϕ[t1 = t2 ]                                                 ϕ[t =i t]                      ϕ[t1 =i t2 ] t2 is a write term
        PARTIAL E Q                  ti ’s have array sort              T RIV E Q                         S YMM
                        ϕ[t1 =∅ t2 ]                                                  ϕ[⊤]                         ϕ[t2 =i t1 ] but t1 is not


                                      E LIM W R = (E LIM W R R D | E LIM W R E Q | PARTIAL E Q | T RIV E Q | S YMM )

                      Fig. 1: Rewriting rules to eliminate write terms. E LIM W R denotes one of the rules chosen non-deterministically.


                                     ∃a · ϕ[a =i t]                                                    ∃a · ϕ[rd (a, t)]       s is fresh, t does not
  C ASE S PLIT E Q                                                               FACTOR R D
                     ∃a · ((a =i t ∧ ϕ[⊤]) ∨ (¬(a =i t) ∧ ϕ[⊥]))                                ∃a, s · (ϕ[s] ∧ s = rd (a, t)) contain array terms

                               Fig. 2: Rewriting rules to factor out equalities and read terms on the quantified array variable.



                                                                                    Line 2 of A RRAY QE rewrites the formula by case-splitting
                                ∃a · (a =i t ∧ ϕ)
                     E LIM E Q                                                   on partial equalities on the array quantifier a (via C ASE S-
                               ∃v · ϕ[wr (t, i, v)/a]                            PLIT E Q ) followed by factoring out read terms over a by

  where a does not appear in t and v denotes fresh variables                     introducing new quantifiers of sort V (via FACTOR R D). Note
                                                                                 that, as presented, these two rules are not terminating as
                                          m
                                                             !                   the partial equalities and read terms are preserved in the
                                          ^                                      conclusion of the rules. However, one can easily ensure that a
                           ∃a ·    ϕ∧          ¬(a =ik tk )
                                         k=1
                                                                                 given partial equality or read term is considered exactly once
           E LIM D ISEQ                                                          by first computing the set of all partial equalities and read
                                          ∃a · ϕ
                                                                                 terms in the formula and processing them in a sequential order.
              where m ∈ N, a does not appear in any tk , and                     The details are straightforward and are left to the reader.
                    a appears in ϕ only in read terms over a                        L IFT E Q D ISEQ R D on line 3 of A RRAY QE performs
                                                                !                Boolean rewriting and returns an equivalent disjunction such
                                         m
                                         ^                                       that in every disjunct, the partial equalities, array disequalities,
                           ∃a ·    ϕ∧          sk = rd (a, tk )                  and equalities over read terms appear at the end as conjuncts,
                                         k=1                                     in that order. For each disjunct, line 5 applies the rules in
     ACKERMANN                    ^
                       ϕ∧                (tk = tℓ =⇒ sk = sℓ )                   Fig. 3 to eliminate the array quantifier a. E LIM E Q obtains
                            1≤k<ℓ≤m                                              a substitution term for a using the equivalence in Eq. (3).
                                                                                 E LIM D ISEQ is applicable when the disjunct contains no partial
      where m ∈ N and a does not appear in ϕ, sk ’s, or tk ’s
                                                                                 equalities and given that the domain of interpretation of I is
               Fig. 3: Rewriting rules for QE of arrays.
                                                                                 infinite, one can always satisfy the disequalities and hence,
                                                                                 they can simply be dropped. ACKERMANN performs the
                                                                                 Ackermann reduction [1] to eliminate the read terms.
rewrites the formula above the line to the logically equivalent                     Note that while the rewrite rules are applicable to all array
formula below the line. We use regular expression notation                       terms and equalities in the original formula, in practice, we
to express sequences of rewrites. In particular, Kleene star                     only need to apply them to eliminate the relevant terms
applied to a rule denotes the rule’s application to a fixed point.               containing the array quantifier a. See Fig. 4 for an illustration
  Line 1 of A RRAY QE eliminates write terms using the                           of A RRAY QE on an example.
rewrite rules in Fig. 1. Here E LIM W R denotes a rule in Fig. 1                    Correctness and Complexity. We can show the following
chosen non-deterministically. E LIM W R R D rewrites terms us-                   properties of A RRAY QE (proof sketches in Appendix B).
ing the read-after-write axiom and E LIM W R E Q rewrites partial
equalities using Eq. (2). PARTIAL E Q converts equalities into                      Theorem 1: A RRAY QE(∃a : arr(I, V ) · ϕ) returns ∃v :
partial equalities using Eq. (1). T RIV E Q eliminates trivial                   V · ρ, where ρ is quantifier-free and ∃v · ρ ≡ ∃a · ϕ.
partial equalities with identical arguments and S YMM ensures                       Theorem 2: A RRAY QE(∃a · ϕ) terminates in time expo-
that write terms on the r.h.s. of equalities are also eliminated.                nential in the size of ϕ.
∃a · (b = wr (a, i1 , v1 ) ∨ (rd (wr (a, i2 , v2 ), i3 ) > 5 ∧ rd (a, i4 ) > 0))
              (i2 = i3 ∧ (b = wr (a, i1 , v1 ) ∨ (v2 > 5 ∧ rd (a, i4 ) > 0))) ∨
       ≡ ∃a ·                                                                                                                {E LIM W R R D}
              (i2 6= i3 ∧ (b = wr (a, i1 , v1 ) ∨ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)))
              (i2 = i3 ∧ ((a =i1 b ∧ rd (b, i1 ) = v1 ) ∨ (v2 > 5 ∧ rd (a, i4 ) > 0))) ∨
       ≡ ∃a ·                                                                                                    {PARTIAL E Q; E LIM W R E Q}
              (i2 6= i3 ∧ ((a =i1 b ∧ rd (b, i1 ) = v1 ) ∨ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)))
                                                                                                  
                             (i2 = i3 ∧ (rd (b, i1 ) = v1 ∨ (v2 > 5 ∧ rd (a, i4 ) > 0))) ∨
                a = i1 b ∧                                                                           ∨
                             (i2 6= i3 ∧ (rd (b, i1 ) = v1 ∨ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)))
       ≡ ∃a ·                                                                                                            {C ASE S PLIT E Q}
                                  (i2 = i3 ∧ (v2 > 5 ∧ rd (a, i4 ) > 0)) ∨
                ¬(a =i1 b) ∧
                                  (i2 6= i3 ∧ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0))
                                                                                              
                           
                                      (i2 = i3 ∧ (rd (b, i1 ) = v1 ∨ (v2 > 5 ∧ s4 > 0))) ∨
                                                                                           
                           a =i1 b ∧                                                       ∨
                                      (i2 6= i3 ∧ (rd (b, i1 ) = v1 ∨ (s3 > 5 ∧ s4 > 0))) 
                                      |                           {z                      }
                                                                       ϕ1
                                                                                   
       ≡ ∃a, s3 , s4 ·                                                                  !                                     {FACTOR R D}
                          
                                        (i2 = i3 ∧ (v2 > 5 ∧ s4 > 0)) ∨
                                                                        
                          ¬(a =i1 b) ∧                                 
                                        (i2 6= i3 ∧ (s3 > 5 ∧ s4 > 0)) 
                                        |                {z            }
                                                              ϕ2

                        ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 )
                        (ϕ1 ∧ a =i1 b ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 )) ∨
       ≡ ∃a, s3 , s4 ·                                                                                                  {L IFT E Q D ISEQ R D}
                        (ϕ2 ∧ ¬(a =i1 b) ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 ))
       ≡ ∃v, s3 , s4 · (ϕ1 ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 )) [wr (b, i1 , v)/a] ∨                                           {E LIM E Q}
         ∃a, s3 , s4 · (ϕ2 ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 ))                                                             {E LIM D ISEQ}
       ≡ ∃v, s3 , s4 · (ϕ1 ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 )) [wr (b, i1 , v)/a] ∨
         ∃s3 , s4 · (ϕ2 ∧ (i3 = i4 =⇒ s3 = s4 ))                                                                            {ACKERMANN}


                                                        Fig. 4: Illustrating A RRAY QE on an example.



B. Model Based Projection                                                          the following:
                                                                                      Theorem 3: For any quantifier-free formula ϕ in ARR,
   In this section, we will assume that for a satisfiable formula                  A RRAY MBP(∃a : arr(I, V ). ϕ) is a finite MBP.
we can obtain a finite representation of a model of the formula                       The fact that it is an MBP can be easily shown by induction
and that we can effectively evaluate the truth of any formula in                   on the number of rewrites applied. The fact that it is finite
this model. This is possible for ARR and its combinations with                     derives from the fact that there are only finitely many ways to
LIA and propositional logic. The ability to evaluate allows                        resolve the disjunctions in the QE result.
us to strengthen a formula in a way that preserves a given                            Moreover, assuming that the evaluation of a formula in
model. Suppose we have a formula ϕ[ψ1 ∨ ψ2 ] with model                            a model can be done in polynomial time, we can evaluate
M , where the sub-formula ψ1 ∨ ψ2 occurs positively (under                         A RRAY MBP(ϕ)(M ) in time that is polynomial in the size of
an even number of negations) in ϕ. If we also have M |= ψ1 ,                       M and the size of ϕ. This is because we can polynomially
then M |= ϕ[ψ1 ] and clearly, ϕ[ψ1 ] entails ϕ. This gives us a                    bound the number of times each rule RM applies, and each
way to eliminate a disjunction while preserving a given model                      rule can only expand the formula size by a constant amount.
and maintaining an under-approximation. If neither ψ1 nor ψ2                       Fig. 6 shows an example of applying A RRAY MBP.
is true in M , we can similarly replace ϕ with ϕ[⊥]. These
transformations are expressed as MBP rewrite rules in Fig. 5.                      C. MBP for ARR+LIA
   For each QE rule R, we can produce a corresponding under-                          We now consider the combination of the ARR and LIA
approximate rule RM that preserves model M . This rule can                         theories. Assume that the only basic sorts are bool and
be written R ; (M BP L EFT | M BP R IGHT | M BP VAC )∗ . In                        int. Furthermore, we only consider linear functions over int
practice, we can choose to only apply the MBP rules to                             along with a divisibility predicate (with constant divisors).
disjunctions introduced by the QE rules and not to those                           We developed a finite MBP for LIA in a previous work [17]
originally occurring in ϕ. Correspondingly, we can convert                         (call it L IA MBP). When the index sort I is int, one can
our QE algorithm A RRAY QE to A RRAY QE M by replac-                               obtain a more efficient MBP with a slight modification of
ing each rule R with RM . We can then obtain an MBP                                ACKERMANN M (for eliminating array read terms) that utilizes
A RRAY MBP(ϕ)(M ) = A RRAY QE M (ϕ) and we can show                                the predicate symbol <. Given a model M of the formula,
∃a · (b = wr (a, i1 , v1 ) ∨ (rd (wr (a, i2 , v2 ), i3 ) > 5 ∧ rd (a, i4 ) > 0))
        ⇐ ∃a · (i2 6= i3 ∧ (b = wr (a, i1 , v1 ) ∨ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)))                                {W R R DM , M |= i2 6= i3 }
        ⇐ ∃a · (i2 6= i3 ∧ ((a =i1 b ∧ rd (b, i1 ) = v1 ) ∨ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)))                        {PARTIAL E Q; W R E QM }
        ⇐ ∃a · ¬(a =i1 b) ∧ i2 6= i3 ∧ (rd (a, i3 ) > 5 ∧ rd (a, i4 ) > 0)                                            {C ASE E QM , M 6|= a =i1 b}
                                                                      
                                                                     
                            ¬(a =i1 b) ∧ i2 6= i3 ∧ (s3 > 5 ∧ s4 > 0)
        ⇐ ∃a, s3 , s4 ·                   |             {z           }                                                              {FACTOR R D}
                                                              ϕ2

                         ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 )
        ⇐ ∃a, s3 , s4 · (ϕ2 ∧ ¬(a =i1 b) ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 ))                                             {L IFT E Q D ISEQ R D}
        ⇐ ∃a, s3 , s4 · (ϕ2 ∧ s3 = rd (a, i3 ) ∧ s4 = rd (a, i4 ))                                                                {E LIM D ISEQ}
        ⇐ ∃s3 , s4 · (ϕ2 ∧ (i3 = i4 ∧ s3 = s4 ))                                                                          {ACKM , M |= i3 = i4 }


                                      Fig. 6: Illustrating A RRAY MBP on the example of Fig. 4 with a given model M .



                                                                                     IV. T HE C OMPOSITIONAL V ERIFICATION F RAMEWORK
                            ϕ[ψ1 ∨ ψ2 ]     M |= ϕ, ψ1
               M BP L EFT                                                             MBP plays a crucial role in enabling the search for compo-
                                       ϕ[ψ1 ]
                                                                                   sitional proofs. In this section, we will consider the role played
                                                                                   by MBP in a model checking framework called S PACER [17].
                             ϕ[ψ1 ∨ ψ2 ]     M |= ϕ, ψ2
              M BP R IGHT                                                          In this framework, MBP is used to create succinct localized
                                        ϕ[ψ2 ]                                     proof sub-goals that make it possible to reason about only
                                                                                   one procedure at a time. The proof goals take the form of
                  ϕ[ψ1 ∨ ψ2 ]          M |= ϕ          M 6|= ψ1 , ψ2               under-approximate summaries, either of the calling context of
      M BP VAC
                                        ϕ[⊥]                                       a procedure or of the procedure itself. Without some form
                                                                                   of projection, S PACER would not be compositional, as it
         Fig. 5: MBP rules for formulas in negation-normal form.                   would build up formulas of exponential size, in effect inlining
                                                                                   procedures to create bounded model checking formulas.
                                                                                   A. Modeling programs with CHCs
one can first partition the set of index terms tk ’s according
to their interpretations in M and choose a representative for                         S PACER checks safety of procedural programs by reducing
each equivalence class. Then, the conjunction in the result of                     the problem to SMT of a special kind of formulas known as
the rule is modified as follows: (a) for every equivalence class,                  Constrained Horn Clauses (CHCs) [5], [17], [14]. We augment
add the equality tk = tℓ for every non-representative tℓ , where                   the signature S with a set of fresh predicate symbols P. A
tk is the representative, (b) linearly order the representatives                   Constrained Horn Clause (CHC) is a formula of the form
and add the corresponding inequalities. The modified rule (and                                          m
                                                                                                        ^
hence, the resulting MBP) is linear in time and space.                                           ∀x ·         Pk (xk ) ∧ ϕ(x) =⇒ head
                                                                                                        k=1
   However, the combination of arrays and integers introduces                                           |        {z          }
terms over the combined signature which need to be handled                                                       body

as well. For example, there is no equivalent quantifier-free                       where for each k, Pk is a symbol in P, xk ⊆ x and |xk |
formula for ∃i : int · rd (a, i) > 0. This implies that there                      is equal to the arity of Pk . The constraint ϕ is a formula
does not exist a finite MBP for the combination of LIA and                         over S, and head is either an application of a predicate in
ARR. In the example, the only way to under-approximate the                         P or another formula over S. We use body to refer to the
quantification is to use the substitution method, replacing i                      antecedent of the CHC, as shown above. A CHC is called
with its interpretation in a model M |= rd (a, i) > 0 as a                         a query if head is a formula over S and otherwise, it is
numeric literal.                                                                   called a rule. If m ≤ 1 in the body, the CHC is linear and
   Based on the above observations, we obtain an MBP for                           is non-linear otherwise. Following the convention of logic
ARR+LIA as follows. First, we apply A RRAY MBP, using the                          programming literature, we also write the above CHC as
modified ACKERMANN M above, to eliminate array quantifiers.                        head ← P1 (x1 ), . . . , Pm (xm ), ϕ(x).
Then, we use L IA MBP to eliminate integer quantifiers that do                        Intuitively, each predicate symbol Pk represents an unknown
not appear in any array term. Finally, we use the substitution                     partial correctness specification of a procedure (that is, an
method to eliminate any remaining integer quantifiers. When                        over-approximate summary). A query defines a property to be
the last step of substitution method is not necessary, the                         proved, while each rule gives modular verification condition
resulting MBP will be finite.                                                      for one procedure. A satisfying assignment to the symbols Pk
is thus a certificate that the program satisfies its specification                  Alg. 2 gives a simplified description of S PACER as a solver
and corresponds to the annotations in a Floyd/Hoare style                        for CHCs in the form of (4) (though S PACER handles general
proof. In this work, we are interested in finding annotations                    CHCs). It is described using a set of rules that can be applied
that can be expressed in the quantifier-free fragment of our                     non-deterministically. Each rule is presented as a guarded
first-order language, to avoid the difficulty of reasoning with                  command “[ grd ] cmd”, where cmd can be executed only
quantifiers.                                                                     if grd holds.
   Any given set of CHCs encoding safety of procedural
programs can be transformed to an equisatisfiable set of just                      Input: Formulas init (x), tr(x, xo , x′ ), bad (x)
three CHCs with a single predicate symbol (encoding the                            Output: Inductive invariant (FO interpretation of Inv
program location using a variable). These CHCs have the                                    satisfying (4)) or U NSAFE
following form:
                                                                                   if (init ∧ bad ) satisfiable then return U NSAFE
            Inv (x) ← init (x)           ¬bad (x) ← Inv (x)                        // initialize data structures
                                                                          (4)
            Inv (x′ ) ← Inv (x), Inv (xo ), tr (x, xo , x′ )                       Q := ∅                            // set of pairs hϕ, ii, i ∈ N
   Intuitively, Inv is the program invariant, x denotes the pre-                   N := 0                       // max level, or recursion depth
state of a program transition, x′ denotes the post-state, and                      O0 = init , Oi = ⊤, ∀i > 0         // may summary sequence
xo denotes the summary of a procedure call (if one is made).                       U = init                                     // must summary
If there are no procedure calls, tr is independent of xo and                       forever non-deterministically do
Inv (xo ) can be dropped: in this case Inv denotes an inductive                         (Candidate) [ (ON ∧ bad ) satisfiable ]
                                                                                            Q := Q ∪ hϕ, N i, for some ϕ =⇒ ON ∧ bad
invariant of an ordinary transition system. In the sequel, we
                                                                                        (DecideMust) [ hϕ, i + 1i ∈ Q , M |= F (Oi , U) ∧ ϕ′ ]
restrict to this normal form and consider only quantifier-free
                                                                                            Q := Q ∪ hM BP (∃xo , x′ · F (Oi , U) ∧ ϕ′ , M ), ii
interpretations of the predicate Inv .
                                                                                        (DecideMay) [ (ϕ, i + 1) ∈ Q , M |= F (Oi ) ∧ ϕ′ ]
   It is useful to rewrite the above rules using a function F
                                                                                            Q := Q ∪ hM BP(∃x, x′ · F (Oi ) ∧ ϕ′ , M )[x/xo ], ii
that substitutes given predicates φA (x) and φB (x) for the
                                                                                        (Leaf) [ (ϕ, i) ∈ Q , F (Oi−1 ) =⇒ ¬ϕ′ , i < N ]
occurrences of Inv in the rule bodies. That is, let                                         Q := Q ∪ hϕ, i + 1i
        F (ϕA , ϕB ) ≡ (ϕA (x) ∧ ϕB (xo ) ∧ tr(x, xo , x′ ))                            (Successor) [ hϕ, i + 1i ∈ Q , M |= F (U) ∧ ϕ′ ]
                          ∨ init (x′ )                                                      U := U ∨ M BP(∃x, xo · F (U) ∧ ϕ′ , M )[x/x′ ]
                                                                                        (Conflict) [ hϕ, i + 1i ∈ Q , F (Oi ) =⇒ ¬ϕ′ ]
The rules are thus equivalent to F (Inv , Inv) ⇒ Inv(x).                                    Oj := Oj ∧ I TP(F (Oi ), ¬ϕ′ )[x/x′ ], ∀j ≤ i + 1
Abusing notation, we will also write F (ϕA ) for F (ϕA , ϕA ).                          (Induction) [ (ϕ ∨ ψ) ∈ Oi , F (ϕ ∧ Oi ) =⇒ ϕ′ ]
                                                                                            Oj := Oj ∧ ϕ, ∀j ≤ i + 1
B. The S PACER framework
                                                                                        (Unfold) [ ON =⇒ ¬bad ] N := N + 1
   S PACER is a general framework that can be instantiated for                          (Safe) [ Oi+1 =⇒ Oi ] return invariant Oi
a given logical theory T by supplying three elements: (a) a                             (Unsafe) [ (U ∧ bad ) satisfiable ] return U NSAFE
model-generating SMT solver for T , (b) an MBP procedure
                                                                                       Algorithm 2: Rule-based description of S PACER.
M BP for T and (c) in interpolation procedure I TP for T .
Compared to other SMT-based algorithms (e.g., [3], [13], [10],
[18]), the key distinguishing feature of S PACER is compo-                          As shown in Alg. 2, S PACER maintains a set of reachability
sitional reasoning. That is, instead of checking satisfiability                  queries Q , a sequence of may summaries {Oi }i∈N , and a
of large formulas generated by program unwinding, S PACER                        must summary U. Intuitively, a query hϕ, ii corresponds to
iteratively creates and checks local reachability queries for                    checking if ϕ is reachable for recursion depth i, Oi over-
individual procedures. In this way it is similar to IC3 [6], [9],                approximates the reachable states for recursion depth i, and U
a SAT-based algorithm for safety of finite-state transition sys-                 under-approximates the reachable states. N denotes the current
tems, and GPDR [16], its extension to Linear Real Arithmetic.                    bound on recursion depth. The sequence of may summaries
Like these methods, S PACER maintains a sequence of over-                        and N correspond to the trace of approximations and the
approximations of procedure behaviors, called may summaries,                     maximum level in IC3/PDR, respectively. For convenience,
corresponding to program unwindings. However, unlike other                       let O−1 be ⊥. M BP (ϕ, M ), for a formula ϕ = ∃v · ϕqf and
approaches, S PACER also maintains under-approximations of                       model M |= ϕqf , denotes the result of some MBP function
procedure behaviors, called must summaries, to avoid redun-                      associated with ϕ for the model M .
dant reachability queries. Another distinguishing feature of                        Alg. 2 initializes N to 0 and, O0 and U to init . Candidate
S PACER is the use of MBP for efficiently handling existentially                 initiates a backward search for a counterexample beginning
quantified formulas to create a new query or a must summary.                     with a set of states in bad . The potential counterexample is ex-
We note, however, that MBP is a general technique and can                        panded using either DecideMust or DecideMay. DecideMust
be exploited in IC3/PDR as well.2                                                jumps over the call Inv (xo ), in the last CHC of (4), utilizing
                                                                                 the must summary U. DecideMay, on the other hand, creates a
  2 Arguably sub-goal creation in IC3 is a simple MBP for propositional logic.   query for the call using the may summary of its calling context.
Successor updates U when a query is known to be reachable.           array terms a, b in ψ, we strengthen ψ with the array equality
The other rules are similar to IC3 [6] and GPDR [16] and             a = b or disequality a 6= b, depending on whether M |= a = b
we skip their explanation in the interest of space. S PACER is       holds or not. In the above example, the queries will now be
sound and if M BP utilizes finite MBP functions, S PACER also        of the form rd (a, k) < 0 ∧ rd (b, k) > 0 ∧ a 6= b. However,
terminates for a fixed N [17].                                       rd (a, k) = rd (b, k) continues to be an interpolant whereas
                                                                     the desired interpolant is a = b. To reduce the dependence on
C. Instantiation for ARR+LIA
                                                                     specific integer constants in the learned interpolants, and hence
   In instantiating this framework for ARR+LIA, the key              in the may summaries, we modify I TP as follows. Suppose we
ingredient is the MBP procedure of the previous section. An          are computing an interpolant for ψ =⇒ ¬ϕ′ (as occurs in
interpolation procedure I TP can be trivially obtained by using      Conflict). We let ϕ = ϕ1 ∧ϕ2 where ϕ2 contains all the literals
literal-dropping approach based on UNSAT cores, or a more            where an integer quantifier is substituted using its interpreta-
sophisticated approach can be taken (e.g., see [16], [18]).          tion in a model. Using a minimal unsatisfiable subset (MUS)
   Because we do not have a finite MBP, S PACER is not               algorithm, we can generalize ϕ2 to ϕ̂2 such that ψ∧(ϕ1 ∧ ϕ̂2 )′
guaranteed to terminate even for a fixed bound on the recursion                                                              ′
                                                                     is unsatisfiable and then obtain I TP(ψ, ¬ (ϕ1 ∧ ϕ̂2 ) ). In the
depth N . That is, it can generate an infinite sequence of           above example, for N = 0 we have ψ = (a = b),
queries and must summaries. Note that MBP is used in 3               ϕ1 = (a 6= b), and ϕ2 = rd (a, k) < 0 ∧ rd (b, k) > 0.
rules: DecideMay, DecideMust, and Successor. The elim-               One can show that ϕ̂2 is simply ⊤ and the only possible
ination of quantifiers in Successor is only an optimization          interpolant is a = b. In our implementation, we add such
and can be avoided. This is not the case with DecideMay              (dis-)equalities on-demand in a lazy fashion. Note that adding
or DecideMust without changing the structure of the queries,         such (dis-)equalities to the queries is only a heuristic and may
the considerations of which are outside the scope of this paper.     not always help with termination.
In the following, we identify restrictions on the CHCs where
termination is still guaranteed and for the other cases, we                              V. E XPERIMENTAL R ESULTS
propose some heuristic modifications to M BP and I TP to help            As noted in the introduction, the array theory allows us to
avoid divergence.                                                    model heap references accurately. This eliminates the need to
   1) Equality resolution in M BP: There are several cases           inline procedures so that heap-allocated objects are reduced to
where terms over combined signatures appear in conjunction           local variables. We hypothesize that the resulting increase in
with equality terms over the index quantifier, e.g., ∃i : int·i =    modularity will allow S PACER to more efficiently verify pro-
t ∧ rd (a, i) > 0 for a term t independent of i. In these cases,     cedural programs using A RRAY M BP, in spite of the potential
the quantifier can be eliminated using equality resolution, e.g.,    for divergence due to non-finiteness of the MBP.
rd (a, t) > 0 in the above example. Such cases seem to be
                                                                         We test this hypothesis using a prototype implementation
natural in the case of a single procedure, i.e., when tr in
                                                                     of S PACER with A RRAY M BP.3 To verify C programs, we
(4) is independent of xo . Consider a disjunct δ in a DNF
                                                                     use S EA H ORN [14], which uses the LLVM infrastructure to
representation of tr. Now, δ represents a path in the procedure
                                                                     compile and optimize the input program, then encodes the
and typically, index terms (in reads and writes) in δ can be
                                                                     verification conditions as CHCs in the SMT-LIB2 format.
ordered such that every index term is a function of the previous
                                                                     S EA H ORN can optionally inline procedure calls before encod-
index terms or the current-state variables x. This makes it
                                                                     ing, allowing us to test our hypothesis regarding modularity.
possible to eliminate any index variables in x′ using equality
                                                                         For reference, we also compare S PACER to the implemen-
resolution as mentioned above.
                                                                     tation of GPDR [16] in Z3 [8]. A key difference between
   2) Privileging array equalities: Here is a simple example
                                                                     S PACER and GPDR is that the latter does not use must
that exhibits non-termination:
                                                                     summaries. Z3 also uses MBP, but is limited to equality
       Inv (a, b) ← a = b                                            resolution and the substitution method. As a result Z3 GPDR
              ⊥ ← Inv(a, b), rd (a, j) < 0, rd(b, j) > 0             is effective only for inlined programs.
                                                                         We use benchmarks from the software verification compe-
Here, intuitively, Inv (a, b) denotes the summary of a proce-        tition SVCOMP’15 [4]. We considered the 215 benchmarks
dure which takes an array a as input and produces b as output        from the Device Drivers category where Z3 GPDR (with inlin-
and we are interested in checking if there is sign change in the     ing) needed more than a minute of runtime or did not terminate
value at an index j as a result of the procedure call. For this      within the resource limits of SVCOMP [15]. All experiments
example, DecideMay creates queries of the form rd(a, k) <            have been carried out using a 2.2 GHz AMD Opteron(TM)
0 ∧ rd(b, k) > 0 where k is a specific integer constant. If I TP     Processor 6174 and 516GB RAM, running Ubuntu Linux. Our
returns interpolants of the form rd (a, k) = rd (b, k), it is easy   resource limits are 30 minutes and 15GB for each verification
to see that S PACER would not terminate even for N = 0, even         task. In the scatter plots that follow, a diamond indicates a
though there is a trivial solution: a = b.                           time-out, a star indicates a mem-out, and a box indicates an
   To alleviate this problem, we modify M BP and I TP to             anomaly in the implementation.
promote the use of array equalities in interpolants. Let ψ be
the result of M BP for a given model M . For every pair of             3 https://bitbucket.org/spacer/code
                                       1800                                                            extensions to software model checking (e.g., [16]), although
   Spacer without inlining (secs)      1600                                                            S PACER is the first to use under-approximate summaries of
                                       1400                                                            procedures for avoiding redundant proof sub-goals. Model-
                                       1200                                                            based generalizations have also been used to obtain projections
                                       1000                                                            efficiently in decision procedures for quantified formulas [19].
                                        800
                                                                                                                  VII. C ONCLUSION AND F UTURE W ORK
                                        600
                                        400
                                                                                                          We have presented a procedure for existentially projecting
                                        200
                                                                                                       array variables from formulas over combined theories of
                                          0
                                                                                                       ARR, LIA, and propositional logic. We have adapted the
                                               0   200   400   600   800 1000 1200 1400 1600 1800      procedure to a finite MBP for array variables. While existential
                                                          Spacer with inlining (secs)
                                                                                                       projection is worst-case exponential, the corresponding MBP
                                       Fig. 7: Advantage of inter-procedural encoding using S PACER.   is polynomial. However, projecting arrays might introduce
                                       1800
                                                                                                       new existentially quantified variables (whose sort is the same
                                                                                                       as the index- or value-sort of the eliminated array). For
         Spacer with inlining (secs)




                                       1600
                                                                                                       projecting these variables, a finite MBP need not exist. We
                                       1400
                                                                                                       described heuristics for obtaining a practical (but not nec-
                                       1200
                                                                                                       essarily finite) MBP procedure, obtaining an instantiation of
                                       1000
                                                                                                       the S PACER framework for verification of safety of sequential
                                         800
                                                                                                       heap-manipulating programs. We show that the new variant of
                                         600
                                                                                                       S PACER is effective for constructing compositional proofs of
                                         400
                                                                                                       Linux Device Drivers. In the future, we plan to extend these
                                         200                                                           ideas for handling more complex heap-manipulating programs
                                           0                                                           that require universal quantifiers in the program invariants.
                                               0   200   400   600   800 1000 1200 1400 1600 1800
                                                           Z3-PDR with inlining (secs)                                              R EFERENCES
       Fig. 8: S PACER vs. Z3 on hard SVCOMP benchmarks with inlining.                                  [1] W. Ackermann, Solvable Cases of The Decision Problem.           North-
                                                                                                            Holland, Amsterdam, 1954.
                                                                                                        [2] A. Albarghouthi, A. Gurfinkel, and M. Chechik, “From Under-
   The scatter plot in Fig. 7 compares the combined run time                                                Approximations to Over-Approximations and Back,” in TACAS, 2012.
                                                                                                        [3] ——, “Whale: An Interpolation-Based Algorithm for Inter-procedural
for the CHC encoding and verification, when inlining is turned                                              Verification,” in VMCAI, 2012.
on and off. A clear advantage is seen in the non-inlining case.                                         [4] D. Beyer, “Software Verification and Verifiable Witnesses – (Report on
This shows that S PACER is able to effectively exploit the addi-                                            SV-COMP 2015),” in TACAS, 2015.
                                                                                                        [5] N. Bjørner, K. McMillan, and A. Rybalchenko, “Program Verification
tional modularity that is made possible by A RRAY MBP, and                                                  as Satisfiability Modulo Theories,” in SMT, 2012.
that this advantage outweighs any occurrences of divergence                                             [6] A. R. Bradley, “SAT-Based Model Checking without Unrolling,” in
due to non-finite MBP.4 We note that S PACER with only LIA                                                  VMCAI, 2011.
                                                                                                        [7] W. Craig, “Three uses of the Herbrand-Gentzen theorem in relating
is able to handle only a small fraction of the non-inlined                                                  model theory and proof theory,” Symbolic Logic, vol. 22(3), 1957.
benchmarks. This result confirms our hypothesis.                                                        [8] L. de Moura and N. Bjørner, “Z3: An Efficient SMT Solver,” in TACAS,
   For reference, we also compare to the performance of                                                     2008.
                                                                                                        [9] N. Eén, A. Mishchenko, and R. K. Brayton, “Efficient Implementation
Z3 GPDR. We observed that without A RRAY MBP, Z3 is                                                         of Property Directed Reachability,” in FMCAD, 2011.
very ineffective in the non-inlined case. We should mention,                                           [10] M. H. et al., “Ultimate Automizer with SMTInterpol - (Competition
however, that of the 7 unsafe programs verified by Z3, 5 could                                              Contribution),” in TACAS, 2013.
                                                                                                       [11] G. Fedyukovich, O. Sery, and N. Sharygina, “eVolCheck: Incremental
not be verified by S PACER. Fig. 8 compares S PACER and Z3                                                  Upgrade Checker for C,” in TACAS, 2013.
with inlining on. This shows an overwhelming advantage for                                             [12] M. K. Ganai, A. Gupta, and P. Ashar, “Efficient SAT-based Unbounded
S PACER, which is due to its more effective MBP approach.                                                   Symbolic Model Checking Using Circuit Cofactoring,” in ICCAD, 2004.
                                                                                                       [13] S. Grebenshchikov, N. P. Lopes, C. Popeea, and A. Rybalchenko,
                                                                                                            “Synthesizing Software Verifiers from Proof Rules,” in PLDI, 2012.
                                                         VI. R ELATED W ORK                            [14] A. Gurfinkel, T. Kahsai, A. Komuravelli, and J. Navas, “The SeaHorn
                                                                                                            Verification Framework,” in CAV, 2015.
   There are several SMT-based approaches for sequential                                               [15] A. Gurfinkel, T. Kahsai, and J. A. Navas, “SeaHorn: A Framework For
program verification that iteratively check satisfiability of                                               Verifying C Programs - (Competition Contribution),” in TACAS, 2015.
formulas corresponding to safety of various unwindings of the                                          [16] K. Hoder and N. Bjørner, “Generalized Property Directed Reachability,”
                                                                                                            in SAT, 2012.
program [3], [13], [10], [18]. However, these monolithic SMT                                           [17] A. Komuravelli, A. Gurfinkel, and S. Chaki, “SMT-Based Model Check-
formulas can grow exponentially. In contrast, the S PACER                                                   ing for Recursive Programs,” in CAV, 2014.
framework [17] we use allows us to do a compositional proof                                            [18] K. L. McMillan and A. Rybalchenko, “Solving Constrained Horn
                                                                                                            Clauses using Interpolation,” Tech. Rep. MSR-TR-2013-6, 2013.
search for safety. Such local proof search is also found in                                            [19] D. Monniaux, “Quantifier Elimination by Lazy Model Enumeration,” in
the IC3 algorithm for hardware model checking [6] and its                                                   CAV, 2010.
                                                                                                       [20] A. Stump, C. W. Barrett, D. L. Dill, and J. R. Levitt, “A Decision
  4 Unfortunately, we have no way to distinguish divergence from timeouts.                                  Procedure for an Extensional Theory of Arrays,” in LICS, 2001.
                                  ∃a · (¬(a =i t) ∧ ϕ)
 E LIM D ISEQ F INITE                                             
                        ∃a, j · rd(a, j) 6= rd (t, j) ∧ j 6∈ i ∧ ϕ
                                      where a does not appear in t
       Fig. 9: Modified version of E LIM D ISEQ for finite domains.



                 A PPENDIX A
 QE AND MBP FOR ARR OVER F INITE I NDEX D OMAINS
   When finite interpretations of I are allowed, E LIM D ISEQ is
no longer an equivalent transformation as there may not exist
an index where the arrays in the disequalities disagree on the
values. However, one can use extensionality to obtain another
equivalent transformation rule E LIM D ISEQ F INITE, as shown
in Fig. 9. As this rule introduces new read terms over a, we
need to apply FACTOR R D once again before ACKERMANN.
Also, note that the result of QE and MBP is now of the form
∃i : I, v : V · ψ.
                     A PPENDIX B
     P ROOFS OF STATEMENTS ABOUT A RRAY QE AND
                     A RRAY MBP
   Theorem 1: A RRAY QE(∃a : arr(I, V ) · ϕ) returns ∃v :
V · ρ, where ρ is quantifier-free and ∃v · ρ ≡ ∃a · ϕ.
     Proof: (Sketch) One can easily show that the rules in
Fig. 1, 2, and 3 are equivalence preserving. The theorem
follows immediately.
   Theorem 2: A RRAY QE(∃a · ϕ) terminates in time expo-
nential in the size of ϕ.
     Proof: (Sketch) Line 1 of A RRAY QE essentially elim-
inates write terms one by one and can be easily shown to
terminate. Line 2 can be easily made to terminate by iterating
over all partial equality and read terms. The remaining steps
of the algorithm clearly terminate as well.
   The complexity analysis is similar to that of the decision
procedure by Stump et al. [20]. Let N be the size of ϕ. The
number of disjuncts generated by any rewrite rule is bounded
by N (due to the disjunction j ∈ i on indices in E LIM W R E Q).
Disjunctions can be generated by the rules for every write term
or partial equality and their number is bounded by N . So,
the total number of disjunctions generated by the algorithm is
bounded by O(N N ) which is exponential in N . The size of
a disjunct generated by a rule can be shown to be bounded
by a polynomial in N . C ASE S PLIT E Q can be efficiently
implemented using an (N + 1)-way case analysis over all N
partial equalities at once avoiding a Boolean rewriting on line 3
of the algorithm. That is, one can obtain N + 1 disjuncts, one
each for the case of a partial equality being true and the last
one for the case of every partial equality being false. Thus,
the complexity of A RRAY QE is exponential in N .
