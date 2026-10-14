                                                                                                                                                                   1

                                        Template-based Program Synthesis using Stellensätze
                                        AMIR KAFSHDAR GOHARSHADY∗ , Hong Kong University of Science and Technology, Hong Kong
                                        S. HITARTH, Hong Kong University of Science and Technology, Hong Kong
                                        FATEMEH MOHAMMADI, KU Leuven, Belgium
                                        HARSHIT JITENDRA MOTWANI, Ghent University, Belgium
arXiv:2209.03602v1 [cs.PL] 8 Sep 2022




                                        Template-based synthesis, also known as sketching, is a localized approach to program synthesis in which the
                                        programmer provides not only a specification, but also a high-level “sketch” of the program. The sketch is
                                        basically a partial program that models the general intuition of the programmer, while leaving the low-level
                                        details as unimplemented “holes”. The role of the synthesis engine is then to fill in these holes such that the
                                        completed program satisfies the desired specification. In this work, we focus on template-based synthesis
                                        of polynomial imperative programs with real variables, i.e. imperative programs in which all expressions
                                        appearing in assignments, conditions and guards are polynomials over program variables. While this problem
                                        can be solved in a sound and complete manner by a reduction to the first-order theory of the reals, the resulting
                                        formulas will contain a quantifier alternation and are extremely hard for modern SMT solvers, even when
                                        considering toy programs with a handful of lines. Moreover, the classical algorithms for quantifier elimination
                                        are notoriously unscalable and not at all applicable to this use-case.
                                           In contrast, our main contribution is an algorithm, based on several well-known theorems in polyhedral and
                                        real algebraic geometry, namely Putinar’s Positivstellensatz, the Real Nullstellensatz, Handelman’s Theorem
                                        and Farkas’ Lemma, which sidesteps the quantifier elimination difficulty and reduces the problem directly to
                                        Quadratic Programming (QP). Alternatively, one can view our algorithm as an efficient way of eliminating
                                        quantifiers in the particular formulas that appear in the synthesis problem. The resulting QP instances can
                                        then be handled quite easily by SMT solvers. Notably, our reduction to QP is sound and semi-complete, i.e. it
                                        is complete if polynomials of a sufficiently high degree are used in the templates. Thus, we provide the first
                                        method for sketching-based synthesis of polynomial programs that does not sacrifice completeness, while
                                        being scalable enough to handle meaningful programs. Finally, we provide experimental results over a variety
                                        of examples from the literature.
                                        Additional Key Words and Phrases: program synthesis, sketching, syntax-guided synthesis

                                        1   INTRODUCTION
                                        Program Synthesis. Program synthesis is one of the most central research topics not only in the
                                        programming languages and verification communities, but in computer science as a whole [Pnueli
                                        and Rosner 1989]. It is often called the holy grail of computing [Gulwani et al. 2017]. Generally
                                        speaking, the goal in program synthesis is to automate the process of programming, i.e. given
                                        a specification, which is often a logical formula, automatically find a program (in a predefined
                                        language) that satisfies the specification.
                                        Short History. Various formulations of this problem have been studied since the 1950s (e.g. see
                                        [Church 1963] which was originally published in 1957). Similar problems were also considered in
                                        the context of constructive mathematics as far back as the 1930s [Kolmogoroff 1932; Troelstra 1977].
                                        ∗ Authors are ordered alphabetically.


                                        Authors’ addresses: Amir Kafshdar Goharshady, Department of Computer Science and Engineering, Department of Mathe-
                                        matics, Hong Kong University of Science and Technology, Clear Water Bay, Kowloon, Hong Kong, goharshady@cse.ust.hk;
                                        S. Hitarth, Department of Computer Science and Engineering, Hong Kong University of Science and Technology, Clear
                                        Water Bay, Kowloon, Hong Kong, hsinghab@connect.ust.hk; Fatemeh Mohammadi, Department of Mathematics and
                                        Department of Computer Science, KU Leuven, Belgium, KU Leuven, Leuven, Belgium, fatemeh.mohammadi@kuleuven.be;
                                        Harshit Jitendra Motwani, Department of Mathematics: Algebra and Geometry, Ghent University, Ghent, Belgium,
                                        harshitjitendra.motwani@ugent.be.

                                        2018. 2475-1421/2018/1-ART1 $15.00
                                        https://doi.org/


                                                                          Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:2                       Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


Today, there is a rich body of literature that uses widely different techniques for synthesis. Some
notable approaches to program synthesis include deductive synthesis using theorem provers [Green
1981; Manna and Waldinger 1971], counterexample-guided synthesis [Abate et al. 2018; Preiner et al.
2017; Reynolds et al. 2015], evolutionary algorithms [Koza 1994; Krawiec 2016; Sobania et al. 2022],
sketching/syntax-guided [Alur et al. 2013; Fedyukovich et al. 2019; Si et al. 2018; Solar-Lezama
2008, 2009], template-based/search-based [Alur et al. 2018; Srivastava et al. 2013], proof-theoretic
methods [Srivastava et al. 2010], constraint-solving [Gulwani et al. 2011; Polikarpova et al. 2016],
type-guided [Guo et al. 2019; Polikarpova et al. 2016], resource-guided [Knoth et al. 2019], and
synthesis based on examples (input-output pairs) [Gulwani 2011; Gulwani et al. 2012; Shaw et al.
1975; Smith 1975]. This is by no means a comprehensive list and there is no way we can do justice
to all the work in this area. Moreover, most approaches, including ours, utilize more than one of the
paradigms named above. Therefore, we refer to [Gulwani et al. 2017] for a more detailed discussion.
Search-based/Syntax-guided Synthesis. While the initial classical formulations of program syn-
thesis focused on automated generation of the whole program, given only a specification as a
logical/semantic-based formula, it was later realized that scaling this approach is quite challenging
and much efficiency can be gained by allowing the programmer to also provide syntactic templates
that limit the search space of possible implementations [Alur et al. 2018]. Intuitively speaking, this
would let the programmer focus on the high-level ideas behind the program, while relying on the
synthesis engine to fill in the low-level details.
   Various formalizations of similar ideas have appeared in the literature. For example, in [Alur
et al. 2013], the programmer has to specify a background theory, a correctness specification, which
is semantic in nature, and a grammar which is used to syntactically limit the search space of
possible implementations. In sketching [Solar-Lezama 2008], the programmer provides the high-
level structure or “sketch” of the implementation, while leaving low-level “holes” for the synthesis
engine to fill. In template-based approaches, such as [Srivastava et al. 2013], the programmer
additionally provides a template for each hole, e.g. specifying that the hole should be filled by a
linear/affine expression or that it should likely utilize a specific set of variables. These approaches
have all led to highly successful synthesis engines. In particular, the SyGuS competition [Alur et al.
2019] is a great showcase of the remarkable year-on-year progress in program synthesis.
Completeness. Given that most variants of program synthesis are undecidable, often due to Rice’s
theorem [Rice 1953], it is no surprise that the synthesis algorithms cannot be sound, complete and
terminating at the same time. The undecidability also applies to almost all cases of syntax-guided
synthesis, since they are more expressive than the verification of specific non-trivial semantic
properties. As such, most synthesis engines, including the ones mentioned above, choose to sacrifice
completeness and focus on efficient sound algorithms that can handle a wide variety of real-world
use-cases. Completeness can only be achieved in limited circumstances, such as template-based
synthesis of linear/affine programs with linear/affine invariants [Srivastava et al. 2013]. So, a natural
question is to explore and characterize families of programs for which we can find efficient, sound
and complete synthesis procedures. Of course, the difficulty lies in obtaining all three desired
properties at the same time and not compromising on any of them.
Our Setting. In this work, we consider template-based synthesis over polynomial programs, i.e. im-
perative programs with bounded real variables in which all expressions appearing in the assign-
ments, loop guards, conditionals, and invariants (pre and post-conditions) are polynomials over
program variables. See Section 2 for a more formal statement. Following the sketching/template-
based approach, we assume that the programmer provides a sketch of the program, together with
one or more holes. The holes can appear both in the program itself or in the invariants and will
be filled by polynomial expressions. The programmer can also provide a template for how each
hole should be filled by specifying the program variables that can appear in the hole and the

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                  1:3


                  1   @real: 𝑖, 𝑠, 𝑛;
                  2   @pre: 𝑛 ≥ 1;
                  3   𝑖 = 0;
                  4   𝑠 = 0;
                  5   @invariant: [ {𝑖, 𝑠 }, 2] ≥ 0 ∧ [ {𝑖, 𝑠 }, 2] ≥ 0 ∧ [ {𝑖, 𝑛 }, 1] ≥ 0
                  6   while( [ {𝑖, 𝑛 }, 1] )
                  7   {
                  8          𝑖 = 𝑖 + 1;
                  9          𝑠 = [ {𝑖, 𝑠 }, 1] ;
                 10   }
                 11   @post: (𝑛 − 1) · 𝑛/2 ≤ 𝑠 ≤ 𝑛 · (𝑛 + 1)/2;
                             Fig. 1. An example polynomial program with holes.

expected degree of the polynomial expression used for filling it. Note that this is without any loss
of generality, since, in the absence of such information, our algorithm can simply iterate over all
possible templates with a bounded degree.
    Example 1.1. As a simple example, consider the program in Figure 1, in which we have three
bounded real variables 𝑖, 𝑠, and 𝑛. The programmer has given us a sketch of the program, which
includes the desired specification as a precondition and a postcondition. However, it also includes
holes that should be filled by the synthesis engine. These holes are shown by dashed boxes. In this
case, the programmer asks us to synthesize an invariant and a guard for the while loop, as well as
an expression for the right-hand side of the assignment inside the while loop. Moreover, she has
provided us with a template for each hole, specifying the variables that she expects would need
to appear in that hole and the maximum degree of the polynomial that should be synthesized for
filling the hole. For example, the while guard must be an affine (degree 1) polynomial over the
variables 𝑖 and 𝑛. As we will see in the sequel, given this partial program as input, our approach
is able to synthesize the completed program in Figure 2, which basically sums up all the integers
from 1 to ⌊𝑛⌋.

                       1   @real: 𝑖, 𝑠, 𝑛;
                       2   @pre: 𝑛 ≥ 1;
                       3   𝑖 = 0;
                       4   𝑠 = 0;
                       5   @invariant: 𝑠 ≥ 𝑖 · (𝑖 + 1)/2 ∧ 𝑠 ≤ 𝑖 · (𝑖 + 1)/2 ∧ 𝑖 ≤ 𝑛
                       6   while(𝑖 ≤ 𝑛 − 1)
                       7   {
                       8           𝑖 = 𝑖 + 1;
                       9           𝑠 = 𝑠 + 𝑖;
                      10   }
                      11   @post: (𝑛 − 1) · 𝑛/2 ≤ 𝑠 ≤ 𝑛 · (𝑛 + 1)/2;
               Fig. 2. The synthesized (completed) version of the partial program in Figure 1.


Decidability and Hardness. Note that the synthesis problem we consider here can be reduced, in
polynomial time, to the decision problem of a formula in the first-order theory of the reals and is
hence decidable. See Section 4 for more details. However, the resulting formula is quite long and
has a quantifier alternation. Thus, it is beyond the reach of modern SMT solvers and quantifier
elimination methods, even for toy programs with three lines of code. In the same section, we also
show that the problem is (strongly) NP-hard, so no strictly PTIME algorithms can be expected
unless P=NP. The NP-hardness holds even in the special case of linear/affine programs.
Our Contributions. In this work, we consider the problem of template-based synthesis over
polynomial imperative programs with bounded real variables. Our contributions are as follows:

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:4                         Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


      • Complexity: We prove that the problem is decidable. This is achieved by a reduction to the
        first-order theory of the reals. We also provide a reduction showing that our problem is
        (strongly) NP-hard. Note that, as mentioned above, decision procedures for the first-order
        theory of the reals are notoriously slow and cannot handle even toy programs in practice.
      • Practical Algorithm: We use classical theorems from polyhedral and real algebraic geometry,
        including Farkas’ Lemma, Handelman’s Theorem, Putinar’s Positivstellensatz1 , and the Real
        Nullstellensatz2 to obtain a polynomial-time reduction to Quadratic Programming (QP).
        Since modern solvers, both SMT solvers and numerical ones, are quite efficient in handling
        real-world QP instances, this leads to a much more scalable approach to program synthesis
        in comparison to decision procedures for the first-order theory of the reals.
      • Completeness: Crucially, we prove that our approach is not only sound but also semi-complete,
        i.e. it is complete as long as polynomials of sufficiently high degree are used in the templates.
        So, our approach achieves both soundness and completeness, while not suffering from the
        unscalability of quantifier elimination and decision procedures for the first-order theory of
        the reals.
      • Experimental Results: We provide extensive experimental results, illustrating the efficiency of
        our approach and that it can successfully handle a variety of programs.
Novelty. The main novelty of our approach is that it can handle a wide family of programs,
i.e. polynomial imperative programs, without sacrificing completeness. It is quite rare in program
synthesis to achieve soundness, semi-completeness and practical efficiency at the same time. To
the best of our knowledge, our method of relying on theorems in real algebraic geometry is also
novel in program synthesis. Moreover, we combine these theorems in non-trivial ways and obtain
new mathematical results, which are of independent interest.
Limitations. The main limitation of our approach is that it can only handle polynomial programs.
This is to be expected, since we are using techniques from real algebraic geometry, which are highly
dependent on having polynomial expressions/inequalities over real variables. Another limitation is
that, although our approach is quite efficient in practice, its runtime is not polynomial in the size
of the program or the number of variables. This is a natural consequence of our NP-hardness result
and cannot be overcome unless P=NP.
Related Works. Several previous works use ideas that are similar in spirit to our approach:
   • Template-based Synthesis: The work [Srivastava et al. 2013] provides algorithms based on
     Farkas’ Lemma for template-based synthesis of linear/affine programs. Since our work can
     handle polynomial programs of arbitrary degree, [Srivastava et al. 2013]’s results on lin-
     ear/affine programs are subsumed by our approach. Moreover, while the use of Farkas’ Lemma
     is shared among the two approaches, we also use theorems from real algebraic geometry,
     e.g. Handelman and Putinar, as well as non-trivial combinations of them, which are not
     considered in [Srivastava et al. 2013]. So, we have a different methodology and handle a
     wider family of programs. To the best of our knowledge, our algebro-geometric approach is
     novel in program synthesis.
   • Invariant Generation: The work [Chatterjee et al. 2020b] provides template-based algorithms
     for automated generation of polynomial invariants over polynomial programs with real
     variables. Note that this is also a special case of our setting, in which the holes are limited
     to appear only in the invariants. Since we allow holes in both the program itself and the
     invariants, our setting is strictly more general. Moreover, while [Chatterjee et al. 2020b]
     also uses Positivstellensätze, it does not consider Nullstellensätze, and thus has a different
     mathematical basis. The work [Sankaranarayanan et al. 2004b] considers the same problem
1 Positivstellensatz is German for “positive locus theorem”. Its plural form is Positivstellensätze.
2 Nullstellensatz is German for “zero locus theorem”.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                    1:5


      as [Chatterjee et al. 2020b] and solves it using Gröbner basis computations. In comparison with
      both of these approaches, we handle a more general setting and have a different methodology.
      There are also template-based approaches for generation of linear loop invariants, such
      as [Colón et al. 2003; Liu et al. 2022; Sankaranarayanan et al. 2004a]. This is an even narrower
      special case of our setting. Finally, [Feng et al. 2017] considers invariant generation for
      probabilistic programs and uses a different Positivstellensatz, i.e. that of Stengle, to obtain an
      automated algorithm. This setting is incomparable to ours due to the presence of probabilistic
      behavior but absence of holes in the program itself.
    • Termination analysis: Template-based algorithms that utilize Farkas’ Lemma or Positivstel-
      lensätze have also been considered in the context of termination and reachability analy-
      sis [Agrawal et al. 2017; Asadi et al. 2021; Chatterjee et al. 2016, 2020a; Neumann et al. 2020;
      Takisaka et al. 2018]. However, this is a very different and orthogonal problem and, while there
      are clear similarities in the approaches, it is not possible to directly or experimentally compare
      them. Conceptually, the works in termination analysis assume that strong-enough invariants
      are given as part of the input3 and then reduce the problem of finding an affine/polynomial
      ranking function, or its probabilistic counterparts, to Linear Programming (LP). This is in
      contrast to our setting where the reduction is to Quadratic Programming (QP) and a reduction
      to LP is impossible due to the strong NP-hardness.
Organization. In Section 2, we formalize our problem and define the syntax and semantics of
our programs. Section 3 is the core of the paper in which we provide our synthesis algorithm and
prove that it is sound and semi-complete. We then study the complexity of the problem in Section 4,
proving that it is decidable and strongly NP-hard. Finally, Section 5 reports on an implementation
of our algorithm and provides experimental results.

2 TEMPLATE-BASED SYNTHESIS OF POLYNOMIAL PROGRAMS
In this work, we focus on imperative polynomial programs. Our programs can have real variables,
conditionals and loops. Moreover, they include specifications as pre and post-conditions, as well as
invariants for each loop, which are used to prove that the program satisfies the specification.
Variables and Valuations. We assume that our programs have a finite set V = {𝑣 1, . . . , 𝑣𝑘 } of
real-valued variables. A valuation is a function 𝑣𝑎𝑙 : V → R that assigns a real value to each
program variable.
Syntax. We consider programs that can be generated from the following grammar:
               𝑃 := (Φ, 𝐶, Φ)
               𝐶 := skip | 𝑣 ← Π | if (Φ) {𝐶} else {𝐶} | while (Φ, Φ) {𝐶} | 𝐶; 𝐶
               Φ := Π ≥ 0 | (Φ ∧ Φ) | ¬Φ
               𝑣∈V
               Π ∈ R[V]
   Intuitively, a program 𝑃 consists of a pre-condition, a sequence 𝐶 of commands, and a post-
condition. We have a special command skip that does not do anything. We also allow assignments,
conditionals and while loops. The header of each loop should include both a guard and a loop
invariant. Moreover, the right-hand-side of every assignment is a polynomial expression Π over
program variables, and the guards, invariants and pre and post-conditions are boolean combinations
Φ of polynomial inequalities over V. For simplicity, we often write the programs as in Figure 2
to make them more human-readable. We also use standard syntactic sugars, e.g. to allow other
boolean operators.
3 Such invariants can be generated by our approach or [Chatterjee et al. 2020b; Sankaranarayanan et al. 2004b].



                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:6                       Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani




         Fig. 3. The Polynomial Transition System (PTS) Corresponding to the Program in Figure 2.


Polynomial Assertions. A polynomial assertion over a set 𝑉 of variables is a boolean combination
of polynomial inequalities of the form 𝑝 ≥ 0 in which 𝑝 ∈ R[𝑉 ]. In the sequel, without loss of
generality, our algorithms assume that all polynomial assertions are in disjunctive normal form.
Polynomial Transition Systems. We define the semantics of our programs using transition
systems. A polynomial transition system (PTS) is a tuple (V, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I) that consists of:
    • A finite set V of program variables,
    • A finite set L of locations,
    • An initial location ℓ0 ∈ L,
    • An initial polynomial assertion 𝜃 0 ,
    • A final location 𝑙 𝑓 ∈ L,
    • A final polynomial assertion 𝜃 𝑓 ,
    • A finite set T of transitions. Each transition 𝜏 ∈ T is a tuple (ℓ, ℓ ′, 𝜌𝜏 ), where ℓ, ℓ ′ ∈ L are
       the pre and post locations, and 𝜌𝜏 , called the transition relation, is a polynomial assertion
       over V ∪ V′, where V represents variables in the pre location and its primed version V′
       represents the variables in the post location, i.e. after taking the transition. Specifically, we
       have V′ = {𝑣 ′ | 𝑣 ∈ V};
    • An invariant I that maps some of the locations ℓ ∈ L to a polynomial assertion I(ℓ). Moreover,
       we have I(ℓ0 ) = 𝜃 0 and I(ℓ𝑓 ) = 𝜃 𝑓 . The set of locations for which an invariant is provided
       must be a cutset (see further below for a formal definition).
   The translation from programs to transition systems is intuitive and straightforward. We can
have one location ℓ ∈ L for each line of the program, and let ℓ0 correspond to the initial line and ℓ𝑓
to the end of the program. Similarly, 𝜃 0 serves as the pre-condition and 𝜃 𝑓 as the post-condition.
Programs are more human-friendly and hence a nicer way to specify the input to the synthesis
problem. In contrast, it is easier to define the algorithms using the more formal notion of PTS.
As such, we will define our semantics based on a PTS instead of a program. Below, we fix a PTS
(V, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I).
  Example 2.1. Figure 3 shows the PTS modeling the program of Figure 2. We have L = {3, 4, 6, 8, 9, 11}
and each location corresponds to a line of code. The invariants are bracketed and shown in green.
Note that our algorithm works with polynomial inequalities, so 𝑎 = 𝑏 is syntactic sugar for
𝑎 − 𝑏 ≥ 0 ∧ 𝑏 − 𝑎 ≥ 0.

Control Flow Graphs (CFGs). The control flow graph (CFG) of our PTS is a directed graph 𝐺 =
(L, 𝐸) in which the locations serve as vertices and there is a directed edge from ℓ to ℓ ′ iff there is a
transition 𝜏 ∈ T of the form 𝜏 = (ℓ, ℓ ′, 𝜌𝜏 ).
Cutsets, Cutpoints and Basic Paths. A subset C ⊆ L of vertices of the CFG 𝐺 is called a cutset if

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                  1:7


   (1) ℓ0, ℓ𝑓 ∈ C; and
   (2) Every cycle in 𝐺, be it a simple cycle or not, intersects C.
Assuming we have fixed a cutset C, every location 𝑐 ∈ C is called a cutpoint. A basic path is a finite
                                  𝑚 = ⟨(ℓ , ℓ ′, 𝜌 )𝑚 ⟩ such that:
sequence of transitions 𝜋 = ⟨𝜏𝑖 ⟩𝑖=1       𝑖 𝑖 𝜏𝑖 𝑖=1
              ′
     • ℓ𝑖 = ℓ𝑖−1 for all 𝑖 > 1.
     • ℓ1 and ℓ𝑚′ are cutpoints, but no internal location ℓ𝑖 with 1 < 𝑖 ≤ 𝑚 is a cutpoint.
We define the transition relation 𝜌 𝜋 of the basic path 𝜋 as 𝜌𝜏𝑚 ◦ 𝜌𝜏𝑚−1 ◦ · · · ◦ 𝜌𝜏1 . Informally, 𝜌 𝜋
is the transition relation resulting from going through all the transitions of 𝜋 one-by-one and is
hence equal to the Ó sequential composition of 𝜌𝜏𝑖 ’s. If 𝜋 is the empty path, then we let 𝜌 𝜋 be the
identity relation 𝑣 ∈V 𝑣 = 𝑣 ′ .
   Example 2.2. In the PTS of Figure 3, the cutpoints shown in red form a cutset C = {3, 6, 11}. In
this example, our non-empty basic paths are ⟨𝜏1, 𝜏2 ⟩, ⟨𝜏4 ⟩, and ⟨𝜏3, 𝜏5, 𝜏6 ⟩.

Remark on Invariants. It is straightforward to see that it suffices to specify invariants in a cutset
only and that the invariants can then be inductively expanded to every other line [Colón et al.
2003]. In the sequel, we assume that a cutset C is fixed and that the invariant I assigns a polynomial
assertion I(ℓ) to every cutpoint ℓ ∈ C. This also fits our simple syntax above in which the invariant
is only provided for the while loops and the start and end of the program (in the form of pre and
post conditions). Nevertheless, our algorithmic approaches consider the PTS and can hence work
with any arbitrary cutset C.
States. A state of the PTS is a pair 𝜎 = (ℓ, 𝑣𝑎𝑙) in which ℓ ∈ L is a location and 𝑣𝑎𝑙 : V → R is a
valuation. Intuitively, a state specifies which line of the program we are in and what values are
taken by our program variables.
Runs. A run of our PTS is a sequence 𝑅 = ⟨𝜎𝑖 ⟩𝑖=0  𝑚 = ⟨(ℓ , 𝑣𝑎𝑙 )⟩𝑚 of states such that:
                                                             𝑖   𝑖 𝑖=0
  • 𝑣𝑎𝑙 0 |= 𝜃 0, i.e. the run starts with the initial location ℓ0 and an initial valuation that satisfies
    the precondition 𝜃 0 ;
  • For every 𝑖 < 𝑚, there exists a transition 𝜏𝑖 ∈ T that allows us to go from 𝜎𝑖 to 𝜎𝑖+1 . More
    formally:
    – 𝜏𝑖 = (ℓ𝑖 , ℓ𝑖+1, 𝜌𝜏𝑖 ); and
                   ′ ) |= 𝜌 , i.e. if we consider 𝑣𝑎𝑙 as a valuation on V and 𝑣𝑎𝑙
    – (𝑣𝑎𝑙𝑖 , 𝑣𝑎𝑙𝑖+1         𝜏𝑖                      𝑖                              𝑖+1 as a valuation on
       V′, then they jointly satisfy the transition condition 𝜌𝜏𝑖 .
Valid Runs. A run 𝑅 = ⟨𝜎𝑖 ⟩𝑖=0  𝑚 = ⟨(ℓ , 𝑣𝑎𝑙 )⟩𝑚 is called valid iff for every 𝑖 for which ℓ has an
                                          𝑖   𝑖 𝑖=0                                               𝑖
associated invariant I(ℓ𝑖 ), we have 𝑣𝑎𝑙𝑖 |= I(ℓ𝑖 ). Intuitively, a run is valid if it always satisfies the
invariant. Specifically, if ℓ𝑚 = ℓ𝑓 , then we must have 𝑣𝑎𝑙𝑚 |= 𝜃 𝑓 in order for the run to be valid.
Valid Transition Systems. A transition system (PTS) is called valid iff every run of the PTS is
valid.
Inductively Valid Transition System. A PTS is called inductively valid with respect to a cutset
C, iff it satisfies the following conditions for all cutpoints ℓ, ℓ ′ ∈ C and valuations (𝑣𝑎𝑙, 𝑣𝑎𝑙 ′) over
V ∪ V′:
    • Initiation: For every basic path 𝜋 from ℓ0 to ℓ, we have
                               𝑣𝑎𝑙 |= 𝜃 0 ∧ (𝑣𝑎𝑙, 𝑣𝑎𝑙 ′) |= 𝜌 𝜋 ⇒ 𝑣𝑎𝑙 ′ |= I(ℓ) ′ .
      Here, I(ℓ) ′ is the same as I(ℓ), except that every program variable 𝑣 ∈ V is replaced with its
      primed version 𝑣 ′ .
    • Consecution: For every basic path 𝜋 from ℓ to ℓ ′, we have
                             𝑣𝑎𝑙 |= I(ℓ) ∧ (𝑣𝑎𝑙, 𝑣𝑎𝑙 ′) |= 𝜌 𝜋 ⇒ 𝑣𝑎𝑙 ′ |= I(ℓ ′) ′ .

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:8                       Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


      • Finalization: For every basic path 𝜋 from ℓ to ℓ𝑓 , we have
                                 𝑣𝑎𝑙 |= I(ℓ) ∧ (𝑣𝑎𝑙, 𝑣𝑎𝑙 ′) |= 𝜌 𝜋 ⇒ 𝑣𝑎𝑙 ′ |= 𝜃 𝑓′ .

The intuition behind inductive validity is similar to that of inductive invariants [Colón et al. 2003].
Informally, a PTS is inductively valid if we can prove that it is valid by breaking each run into a
sequence of basic paths and then show its validity by an inductive argument. It is straightforward
to see that every inductively valid PTS is indeed valid [Chatterjee et al. 2020b; Colón et al. 2003].
Moreover, the finalization and initiation conditions above can be considered as special cases of
consecution. We are including them separately to emphasize the point that validity requires the
PTS to satisfy its specification (as specified by pre and post-conditions).
Non-determinism. Note that, in order to simplify the presentation, we did not include non-
determinism in the syntax of our programs. However, our transition systems have built-in support
for non-determinism since one can have several outgoing transitions from the same node or,
alternatively, a transition that does not uniquely specify the post-valuation 𝑣𝑎𝑙 ′ in terms of the
pre-valuation 𝑣𝑎𝑙 . Therefore, all the results in the sequel are trivially extensible to the case of
non-deterministic polynomial programs.
   Our goal is to synthesize a valid PTS, given a sketch that includes holes in it. To do this, we first
define variants of our programs and transition systems which can also include holes.
Sketches of Polynomial Programs. In this work, we assume that the programmer provides a
sketch of the implementation. The sketch is a partial program, i.e. a program with holes, which is
generated using the following grammar:
          𝑃 := (Φ, 𝐶, Φ)
          𝐶 := skip | 𝑣 ← Π | 𝑣 ← 𝐻 | if (Φ) {𝐶} else {𝐶} | while (Φ, Φ) {𝐶} | 𝐶; 𝐶
          Φ := Π ≥ 0 | 𝐻 ≥ 0 | (Φ ∧ Φ) | ¬Φ
          𝐻 := (V, 𝑑)
          𝑣∈V
          Π ∈ R[V]
          V⊆V
          𝑑∈N
The main difference between this grammar and the previous one is the introduction of a new
non-terminal 𝐻 which models a hole. Note that holes can appear in assignments or as part of the
assertions Φ, be it in guards of if/while or the invariants or even pre and post-conditions. For each
hole, the programmer specifies a set V of variables which she expects might need to appear in
filling the hole, as well as a maximum degree 𝑑 ∈ N, requiring that the hole should be filled by a
polynomial of degree at most 𝑑. As an example, see the sketch in Figure 1 in which the holes are
shown in boxes. As usual, we do not follow the grammar exactly in order to make the sketch more
human-readable. For example, we wrote the invariant outside the while loop, instead of having it
as the second parameter in the while header.
Template and Symbolic Polynomials and Assertions. Let V be our finite set of program variables
and T a separate finite set of template variables. We define a symbolic polynomial over (V, T) as
a polynomial over V whose every coefficient is itself a polynomial over T. More formally, every
symbolic polynomial over (V, T) is of the form 𝑝 ∈ (R[T]) [V]. We say a symbolic polynomial 𝑝
is a template if every coefficient of 𝑝, when considered as a polynomial over T, has degree 0 or 1.
Symbolic (resp. template) polynomial assertions are simply defined as boolean combinations of

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                  1:9




Fig. 4. The SPTS Corresponding to the Sketch Program of Figure 1. For brevity, we have not included equalities
of the form 𝑣 ′ = 𝑣 that ensure a variable 𝑣 does not change in a transition. See Figure 3 for details of these
equalities. The cutpoints are shown in red.


symbolic (resp. template) polynomial inequalities. As mentioned before, our algorithms assume
without loss of generality that all assertions are in disjunctive normal form.
Sketches of Polynomial Transition Systems. A sketch of a polynomial transition system (SPTS) is
tuple (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I) in which all parts serve the same purposes and are defined similarly
as in a PTS. The only differences are:
    • The assertions 𝜃 0, 𝜃 𝑓 and invariants I(ℓ) are now template polynomials over (V, T).
    • The transition relations 𝜌𝜏 are now template polynomials over (V ∪ V′, T).
Moreover, we always assume T ∩ V = ∅.
   Example 2.3. Figure 4 shows a sketch polynomial transition system (SPTS) corresponding to
the sketch program of Figure 1. To obtain this SPTS, we introduced 21 new template variables
T = {𝑡 0, . . . , 𝑡 20 } and replaced each hole with a template polynomial that corresponds to the
programmer’s desire for that hole. Note that the invariant of location 6 and the transition relations
for 𝜏3, 𝜏4 and 𝜏6 are now symbolic, i.e. they are polynomials over the program variables {𝑖, 𝑠, 𝑛}
in which every coefficient is itself a polynomial over T. In this case, all coefficients are simply
variables in T. Our goal is to find suitable concrete real values for each 𝑡𝑖 such that the SPTS of
Figure 4 becomes a valid PTS, e.g. that of Figure 3.
  We now have all the needed ingredients to formalize our Template-Based Synthesis problem over
Polynomial programs (TBSP):
TBSP. Given a sketch of a polynomial transition system Γ = (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I), find a
valuation 𝑣𝑎𝑙 T : T → R that assigns a real value to every template variable, such that Γ 𝑣𝑎𝑙T becomes
an inductively valid polynomial transition system. Here, Γ 𝑣𝑎𝑙T is the PTS obtained by taking the
sketch Γ and replacing every appearance of each template variable 𝑡 ∈ T by its corresponding value
𝑣𝑎𝑙 T (𝑡). Informally, our goal is to synthesize concrete values for each of the template variables so
that the resulting program/PTS satisfies the programmer’s desired specification.
Boundedness. For technical reasons which will become evident in Section 3.2, we assume that our
program variables V have bounded values. More specifically, we consider a bound 𝑀 ∈ (0, ∞) and
assume that no program variable ever takes a value larger than 𝑀 or smaller than −𝑀. We call
this the boundedness assumption. The boundedness assumption is necessary for our completeness

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:10                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


theorem (Theorem 3.16), but not for soundness. It is a merely theoretical assumption with no
significant practical effect. In practice, we do not assume boundedness in our implementation in
Section 5 and can successfully handle all the cases without this extra assumption.

3 OUR ALGORITHM FOR TBSP
In this section, we provide an automated, sound and semi-complete algorithm for the TBSP problem
as defined in Section 2. We assume that the input to our algorithm is either a sketch polynomial
transition system (SPTS) or a sketch of a polynomial program, containing holes. In the latter case, we
would first process the input and translate it to an SPTS. We start by providing a high-level overview
of our algorithm (Section 3.1) and an illustration over the example of Figure 1. Then, we present our
mathematical toolkit, i.e. Farkas’ Lemma, Handelman’s Theorem, Putinar’s Positivstellesatz and
the Real Nullstellensatz in Section 3.2 and manipulate them to be usable for our application. We
use this toolkit to fill in the details of our algorithm in Section 3.3. Finally, we provide soundness
and semi-completeness theorems in Section 3.4.

3.1 An Illustration and Overview of the Algorithm
Suppose that a sketch, i.e. a polynomial program with holes, is given as the input. As a running
example, let us take Figure 1. Our algorithm fills in the holes using the following four steps:
Step 1: Creating Templates and Translation to SPTS. For each hole in the sketch, the algorithm
generates a template polynomial in which it introduces new template variables. Concretely, let the
hole be of the form 𝐻 = (V, 𝑑). This corresponds to a case in which the programmer desires the hole
to be filled by a polynomial of degree at most 𝑑 over the set V ⊆ V. The algorithm first generates
all monomials 𝑚𝑖 of degree at most 𝑑 over V. It then
                                                  Í creates a template polynomial that includes
all of these monomials and is of the form 𝑝 𝐻 := 𝑖 𝑡𝑖 · 𝑚𝑖 , in which each 𝑡𝑖 is a newly generated
template variable. It replaces the hole 𝐻 by the template polynomial 𝑝 𝐻 and then translates the
program to an SPTS. The translation from programs to transition systems is a standard procedure,
i.e. a simple parsing exercise, and hence we skip it for brevity. At the end of this step, we have an
SPTS Γ = (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I).
    Example 3.1. Consider the sketch of Figure 1. The first hole in the invariant of line 5 should be
filled by a polynomial of degree at most 2 over the variables {𝑖, 𝑠}. Hence, the algorithm generates
the following template for this hole:
                               𝑝 1 := 𝑡 0 + 𝑡 1 · 𝑖 + 𝑡 2 · 𝑠 + 𝑡 3 · 𝑖 2 + 𝑡 4 · 𝑖 · 𝑠 + 𝑡 5 · 𝑠 2 .
Note that all the 𝑡𝑖 ’s are new template variables whose concrete values have to be synthesized later.
It then establishes a similar template for the second hole in line 5:
                              𝑝 2 := 𝑡 6 + 𝑡 7 · 𝑖 + 𝑡 8 · 𝑠 + 𝑡 9 · 𝑖 2 + 𝑡 10 · 𝑖 · 𝑠 + 𝑡 11 · 𝑠 2 .
The third hole in line 5 and the hole in line 6 should be affine expressions over {𝑖, 𝑛}, so the algorithm
generates:
                                        𝑝 3 := 𝑡 12 + 𝑡 13 · 𝑖 + 𝑡 14 · 𝑛,
                                        𝑝 4 := 𝑡 15 + 𝑡 16 · 𝑖 + 𝑡 17 · 𝑛.
Finally, the last hole (line 9) should be filled by an affine expression over {𝑖, 𝑠}. So, we have:
                                                𝑝 5 := 𝑡 18 + 𝑡 19 · 𝑖 + 𝑡 20 · 𝑠.
The algorithm first replaces each 𝑖-th hole with its corresponding template polynomial 𝑝𝑖 . It then
translates the program to a transition system, leading to the SPTS of Figure 4.

Step 2: Generating Entailment Constraints. Recall that our goal is to synthesize concrete real
values for the template variables 𝑡𝑖 ∈ T such that our SPTS becomes an inductively valid PTS. As

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                   1:11


such, it should satisfy the initiation, consecution and finalization constraints defined in Section 2.
In this step, the algorithm considers every possible basic path 𝜋 and symbolically computes its
transition relation and its corresponding initiation/consecution/finalization constraint. Then, the
algorithm translates the constraint into an equivalent system of constraints in the following standard
form:
                             𝑓1 ⊲⊳1 0 ∧ 𝑓2 ⊲⊳2 0 ∧ . . . ∧ 𝑓𝑟 ⊲⊳𝑟 0 ⇒ 𝑓 ⊲⊳ 0                        (1)
in which 𝑓 and each 𝑓𝑖 are symbolic polynomials over (V ∪ V′, T) and each operator ⊲⊳, ⊲⊳𝑖 is either
≥ or >.
  Example 3.2. Consider the SPTS and cutset of Figure 4. As discussed in Example 2.2, the basic
paths in this SPTS are 𝜋1 = ⟨𝜏1, 𝜏2 ⟩, 𝜋2 = ⟨𝜏4 ⟩, and 𝜋3 = ⟨𝜏3, 𝜏5, 𝜏6 ⟩. The algorithm symbolically
computes the transition relation of each basic path:
                                𝜌 𝜋1 = 𝜌𝜏2 ◦ 𝜌𝜏1 = [𝑛 ′ = 𝑛 ∧ 𝑖 ′ = 0 ∧ 𝑠 ′ = 0]
                   𝜌 𝜋2 = 𝜌𝜏4 = [𝑡 15 + 𝑡 16 · 𝑖 + 𝑡 17 · 𝑛 < 0 ∧ 𝑖 ′ = 𝑖 ∧ 𝑠 ′ = 𝑠 ∧ 𝑛 ′ = 𝑛]
𝜌 𝜋3 = 𝜌𝜏6 ◦𝜌𝜏5 ◦𝜌𝜏3 = [𝑡 15 + 𝑡 16 · 𝑖 + 𝑡 17 · 𝑛 ≥ 0 ∧ 𝑖 ′ = 𝑖 + 1 ∧ 𝑠 ′ = 𝑡 18 + 𝑡 19 · (𝑖 + 1) + 𝑡 20 · 𝑠 ∧ 𝑛 ′ = 𝑛]
It then has to symbolically compute the inductive validity constraints. For 𝜋 1 , we have the following
initiation constraint:
                             𝑣𝑎𝑙 |= 𝜃 0 ∧ (𝑣𝑎𝑙, 𝑣𝑎𝑙 ′) |= 𝜌 𝜋1 ⇒ 𝑣𝑎𝑙 ′ |= I(6) ′ .
The algorithm symbolically computes and expands this constraint and obtains:
                                     𝑛 ≥ 1 ∧ 𝑛′ = 𝑛 ∧ 𝑖 ′ = 0 ∧ 𝑠 ′ = 0 ⇒
                           𝑡 0 + 𝑡 1 · 𝑖 ′ + 𝑡 2 · 𝑠 ′ + 𝑡 3 · 𝑖 ′2 + 𝑡 4 · 𝑖 ′ · 𝑠 ′ + 𝑡 5 · 𝑠 ′2 ≥ 0 ∧
                          𝑡 6 + 𝑡 7 · 𝑖 ′ + 𝑡 8 · 𝑠 ′ + 𝑡 9 · 𝑖 ′2 + 𝑡 10 · 𝑖 ′ · 𝑠 ′ + 𝑡 11 · 𝑠 ′2 ≥ 0 ∧
                                                𝑡 12 + 𝑡 13 · 𝑖 ′ + 𝑡 14 · 𝑛 ′ ≥ 0
Note that this constraint should hold for any valuation of V ∪ V′ . At this point, since we know
𝑛 ′ = 𝑛 and 𝑖 ′ = 𝑠 ′ = 0, we can further simplify the constraint to
                                𝑛 ≥ 1 ⇒ 𝑡 0 ≥ 0 ∧ 𝑡 6 ≥ 0 ∧ 𝑡 12 + 𝑡 14 · 𝑛 ≥ 0,
hence eliminating several variables and obtaining a much simpler but equivalent constraint. Our
implementation in Section 5 applies such sound heuristics for simplifying the constraints. However,
the constraint is still not in the standard form of (1) since there are several inequalities on the
right-hand-side. The algorithm rewrites this constraint as the following equivalent set of constraints
of the standard form (1):
                                          𝑛 ≥ 1 ⇒ 𝑡 0 ≥ 0;
                                                     𝑛 ≥ 1 ⇒ 𝑡 6 ≥ 0;
                                               𝑛 ≥ 1 ⇒ 𝑡 12 + 𝑡 14 · 𝑛 ≥ 0.
Let us now consider 𝜋2 . We need to generate a finalization constraint in this case. The algorithm
symbolically computes
                                       I(6) ∧ 𝜌 𝜋2 ⇒ 𝜃 𝑓′
and then expands it and rewrites it as an equivalent set of standard constraints just as in the previous
case. Finally, for 𝜋3, which starts and ends at the cutpoint 6, the algorithm writes a consecution
constraint:
                                         I(6) ∧ 𝜌 𝜋3 ⇒ I(6) ′ .
As above, the constraint will be simplified and translated to an equivalent set of standard constraints.

                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:12                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


Step 3: Eliminating Program Variables and Reduction to QP. We start by providing some
intuition for this step. Let V = {𝑣 1, . . . , 𝑣𝑚 } be our program variables and T = {𝑡 1, . . . , 𝑡𝑚′ } the
template variables introduced in Step 1 above. By the end of the previous step, we have a set of
standard constraints of form (1). Let the constraints be 𝜅 1, 𝜅 2, . . . , 𝜅𝑢 . Our problem is now equivalent
to finding concrete real values 𝑡𝑖∗ ∈ R for each template variable 𝑡𝑖 ∈ T such that the following
formula is satisfied:
                              ∀𝑣 1, 𝑣 2, . . . , 𝑣𝑚 (𝜅 1 ∧ 𝜅 2 ∧ . . . ∧ 𝜅𝑢 )                             (2)
or more formally                                      Ó
                                                         𝑢
                                                                           ′
                                                                         ∗ 𝑚 ,
                             ∀𝑣𝑎𝑙 ∈ RV 𝑣𝑎𝑙 |=               𝜅
                                                         𝑗=1 𝑗 𝑖𝑡 ←    𝑡 𝑖 𝑖=1                            (3)
                   𝑚 ′
where 𝜅 𝑗 𝑡𝑖 ← 𝑡𝑖∗ 𝑖=1 is the formula 𝜅 𝑗 in which each 𝑡𝑖 is replaced by 𝑡𝑖∗ . This is not an easy
           
problem in general (See Section 4), but the fact that all 𝜅𝑖 constraints are in the standard form of (1)
can be exploited for a reduction to quadratic programming (QP). This step requires mathematical
details that will be presented in Section 3.2. At this point, we consider a simple sound algorithm
that captures the main intuition of this step and then fill in the details to make it semi-complete in
Section 3.3.
   Consider a standard constraint 𝜅𝑖 of the following form:
                                  𝑓1 ≥ 0 ∧ 𝑓2 ≥ 0 ∧ . . . ∧ 𝑓𝑟 ≥ 0 ⇒ 𝑓 ≥ 0
As mentioned above, this constraint should hold over all valuations. So, intuitively, we would like
to guarantee that whenever all polynomials 𝑓1, 𝑓2, . . . , 𝑓𝑟 are non-negative, then so is 𝑓 . A simple
sound solution is to try to write 𝑓 as a combination of the 𝑓𝑖 ’s in the following form:
                                                 Í
                                         𝑓 = 𝜆0 + 𝑟𝑖=1 𝜆𝑖 · 𝑓𝑖                                      (4)
where each 𝜆𝑖 is a new non-negative real variable. We write Λ as a shorthand for {𝜆0, . . . , 𝜆𝑟 }. This
is clearly sound, since whenever the 𝑓𝑖 ’s are non-negative at a given valuation, then so is every
combination of them with non-negative coefficients. Indeed, we can go one step further and let each
𝜆𝑖 be an always-non-negative polynomial, instead of a real constant, and the exact same argument
will go through. As we will see, this idea can lead to a semi-complete algorithm.
   We can now present Step 3 of the algorithm. In this step, the algorithm considers each standard
constraint 𝜅𝑖 and symbolically computes the equation (4) for it. Note that both sides of (4) are
symbolic polynomials over (V, T ∪ Λ). In particular, they are polynomials over V. However, two
polynomials are equal if and only if they have equal coefficients for every monomial. Hence, the
algorithm equates the corresponding coefficients on the left and right-hand sides of (4) and rewrites
it as a system of quadratic equalities over T ∪ Λ.
   Example 3.3. Consider the standard constraint 𝑛 − 1 ≥ 0 ⇒ 𝑡 12 + 𝑡 14 · 𝑛 ≥ 0 that was generated
in Step 2 above (Example 3.2). The algorithm symbolically computes (4) and obtains
                                         𝑡 12 + 𝑡 14 · 𝑛 = 𝜆0 + 𝜆1 · (𝑛 − 1).
Since both sides of this equality are polynomials over 𝑛, in order for the equality to hold, they
should have the same constant factor and the same coefficient for 𝑛, so the algorithm obtains the
following constraints:
                                          𝑡 12 = 𝜆0 − 𝜆1
                                                      𝑡 14 = 𝜆1
                                             𝜆0 , 𝜆1 ≥ 0
This is a quadratic programming (QP) instance in which none of the program variables, e.g. 𝑛,
appear. The algorithm translates other standard constraints to QP in a similar manner and combines
them conjunctively.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                 1:13


Step 4: Constraint Solving. The algorithm passes the QP instance generated in the previous step
to an SMT solver or a numerical solver. If the solver fails to find a solution, then the algorithm fails,
too. Otherwise, the solver provides values for all 𝑡𝑖 and 𝜆𝑖 variables. The algorithm plugs the values
found for 𝑡𝑖 ’s back into the templates of Step 1, which successfully leads to an inductively valid
PTS or equivalenty to a valid synthesized program that satisfies the desired specification.
   Example 3.4. Given the sketch of Figure 1 as input, the synthesized program of Figure 2 is obtained
as one of the solutions of the QP instance in Step 4. However, the solution is not necessarily unique,
and our algorithm might find a different solution based on the values found by the external solver.

3.2 Mathematical Toolkit
In Section 3.1 above, we provided an overview of our algorithm. However, the details of Step 3,
i.e. the reduction to QP, were not presented since they depend on certain mathematical prerequisites.
In this section, we provide the mathematical tools and theorems that are crucial for this step of
the algorithm. We first recall some notation and classical definitions. Then, we present several
theorems from polyhedral and real algebraic geometry. Finally, we obtain tailor-made versions of
these theorems in a format that can be used in Step 3 of our algorithm above. We refer to [Bochnak
et al. 2013; Hartshorne 2013] for a more detailed treatment of these theorems.
Sums of Squares. A polynomial ℎ ∈ R[𝑥 1, . . . , 𝑥𝑛 ] is a sum of squares (SOS) iff there exist 𝑘 ≥ 1
                                                                  Í
and polynomials 𝑔1, . . . , 𝑔𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ] such that ℎ = 𝑘𝑖=1 𝑔𝑖2 .
Strong Positivity. Given a set 𝑋 ⊆ R𝑛 and a polynomial 𝑔 ∈ R[𝑥 1, . . . , 𝑥𝑛 ], we say that 𝑔 is strongly
positive over X if inf 𝑥 ∈𝑋 𝑔(𝑥) > 0. We write this as 𝑋 |= 𝑔 ≫ 0.
Notation. Let Φ = {𝑔1 ⊲⊳1 0, . . . , 𝑔𝑘 ⊲⊳𝑘 0} be a set of polynomial inequalities where ⊲⊳𝑖 ∈ {≥, >}
and 𝑔𝑖 ∈ R[𝑥 1, . . . , 𝑥𝑛 ]. We define SAT(Φ) as the set of all real valuations 𝑣𝑎𝑙 over the variables
{𝑥 1, . . . , 𝑥𝑛 } that satisfy Φ. More formally, SAT(Φ) = {𝑣𝑎𝑙 ∈ R𝑛 | 𝑘𝑖=1 𝑣𝑎𝑙 |= (𝑔𝑖 ⊲⊳𝑖 0)}.
                                                                       Ó

Closure. Given a set 𝑋 ⊆ R𝑛 , we define 𝑋 to be the closure of 𝑋 with respect to the Euclidean
topology of R𝑛 . For a set Φ of polynomial inequalities, we define Φ as the system of polynomial
inequalities obtained from Φ by replacing every strict ineqaulity with its non-strict counterpart.
  We are now ready to present the main mathematical theorems that will be used in our work.
Our presentation follows that of [Goharshady 2020, Section 2.6], which also contains proofs of
corollaries that are not proven here.
  Theorem 3.5 (Farkas’ Lemma [Farkas 1902]). Consider a set 𝑉 = {𝑥 1, . . . , 𝑥𝑟 } of real-valued
variables and the following system Φ of equations over 𝑉 :
                                   
                                   
                                    𝑎 1,0 + 𝑎 1,1 · 𝑥 1 + . . . + 𝑎 1,𝑟 · 𝑥𝑟 ≥ 0
                                                             ..
                              Φ :=
                                   
                                   
                                                              .                     .
                                   
                                   
                                   𝑎 + 𝑎 · 𝑥 + . . . + 𝑎 · 𝑥 ≥ 0
                                    𝑚,0        𝑚,1      1             𝑚,𝑟    𝑟

When Φ is satisfiable, it entails a linear inequality
                                     𝜓 := 𝑐 0 + 𝑐 1 · 𝑥 1 + · · · + 𝑐𝑟 · 𝑥𝑟 ≥ 0
if and only if 𝜓 can be written as non-negative linear combination of the inequalities in Φ and the
trivial inequality 1 ≥ 0, i.e. if there exist non-negative real numbers 𝑦0, . . . , 𝑦𝑚 such that
                                                     Í
                                           𝑐 0 = 𝑦0 + 𝑘𝑖=1 𝑦𝑖 · 𝑎𝑖,0 ;
                                                   Í𝑘
                                              𝑐 1 = 𝑖=1 𝑦𝑖 · 𝑎𝑖,1 ;
                                                      ..
                                                       .
                                                   Í𝑘
                                              𝑐𝑟 = 𝑖=1 𝑦𝑖 · 𝑎𝑖,𝑟 .

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:14                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


Moreover, Φ is unsatisfiable if and only if −1 ≥ 0 can be derived as above.
    The importance of Farkas’ Lemma for us is that if we have a standard constraint of form (1) and
if the constraint includes only linear/affine inequalities, then we can use this lemma in Step 3 of our
algorithm to reduce the standard constraint to QP, just as we did in Section 3.1. Moreover, Farkas’
Lemma guarantees that this approach is not only sound but also complete. A corner case that we
have to consider is when Φ is itself unsatisfiable and thus Φ ⇒ 𝜓 holds vacuously. Fortunately,
Farkas’ Lemma also provides a criterion for unsatisfiability. In practice, we work with the following
corollary of Theorem 3.5 which can also handle strict inequalities.
   Corollary 3.6. Consider a set 𝑉 = {𝑥 1, . . . , 𝑥𝑟 } of real-valued variables and the following system
of equations over 𝑉 :
                              
                              
                               𝑎 1,0 + 𝑎 1,1 · 𝑥 1 + . . . + 𝑎 1,𝑟 · 𝑥𝑟 ⊲⊳1 0
                                                          ..
                        Φ :=
                              
                              
                                                          .
                              
                              𝑎 + 𝑎 · 𝑥 + . . . + 𝑎 · 𝑥 ⊲⊳ 0
                               𝑚,0        𝑚,1      1             𝑚,𝑟    𝑟 𝑚

where ⊲⊳𝑖 ∈ {>, ≥} for all 1 ≤ 𝑖 ≤ 𝑚. When Φ is satisfiable, it entails a linear inequality
                                       𝜓 := 𝑐 0 + 𝑐 1 · 𝑥 1 + · · · + 𝑐𝑟 · 𝑥𝑟 ⊲⊳ 0
with ⊲⊳∈ {>, ≥}, if and only if 𝜓 can be written as non-negative linear combination of inequalities in
Φ and the trivial inequality 1 > 0. Note that if 𝜓 is strict, then at least one of the strict inequalities
should appear with a non-zero coefficient in the linear combination. Moreover, Φ is unsatisfiable if and
only if either −1 ≥ 0 or 0 > 0 can be derived as above.
  We now consider extensions of Farkas’ Lemma which can help us handle non-linear standard
constraints in Step 3. The first extension is Handelman’s theorem, which can be applied when the
inequalities on the left hand side of (1) are linear/affine, but the right hand side is a polynomial of
arbitrary degree. To present the theorem, we first need the concept of monoids.
Monoid. Consider a set 𝑉 = {𝑥 1, . . . 𝑥𝑟 } of real-valued variables and the following system of linear
inequalities over 𝑉 :
                                            𝑎 1,0 + 𝑎 1,1 · 𝑥 1 + . . . + 𝑎 1,𝑟 · 𝑥𝑟 ⊲⊳1 0
                                            
                                            
                                                                       ..
                                     Φ :=
                                            
                                            
                                                                       .
                                            
                                            𝑎 + 𝑎 · 𝑥 + . . . + 𝑎 · 𝑥 ⊲⊳ 0
                                             𝑚,0         𝑚,1    1             𝑚,𝑟    𝑟 𝑚

where ⊲⊳𝑖 ∈ {>, ≥} for all 1 ≤ 𝑖 ≤ 𝑚. Let 𝑔𝑖 be the left hand side of the 𝑖-th inequality, i.e.
𝑔𝑖 (𝑥 1, . . . , 𝑥𝑟 ) := 𝑎𝑖,0 + 𝑎𝑖,1 · 𝑥 1 + . . . 𝑎𝑖,𝑟 · 𝑥𝑟 . The monoid of Φ is defined as:
                                                    nÎ                                        o
                                                         𝑚 𝑘𝑖
                               Monoid(Φ) :=              𝑖=1 𝑔𝑖 | 𝑚 ∈ N ∧ ∀𝑖 𝑘𝑖 ∈ N ∪ {0} .

In other words, the monoid contains all polynomials that can be obtained as a multiplication of the
𝑔𝑖 ’s. Note that 1 ∈ Monoid(Φ). We define Monoid𝑑 (Φ) as the subset of polynomials in Monoid(Φ)
of degree at most 𝑑.
   Theorem 3.7 (Handelman’s Theorem [Handelman 1988]). Consider a set 𝑉 = {𝑥 1, . . . , 𝑥𝑟 } of
real-valued variables and the following system of equations over 𝑉 :
                                     
                                     
                                      𝑎 1,0 + 𝑎 1,1 · 𝑥 1 + . . . + 𝑎 1,𝑟 · 𝑥𝑟 ≥ 0
                                                               ..
                                Φ :=
                                     
                                     
                                                                .                        .
                                     
                                     
                                     𝑎 + 𝑎 · 𝑥 + . . . + 𝑎 · 𝑥 ≥ 0
                                      𝑚,0        𝑚,1      1             𝑚,𝑟    𝑟


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                 1:15


If Φ is satisfiable, SAT(Φ) is compact, and Φ entails a polynomial inequality 𝑔(𝑥 1, . . . , 𝑥𝑟 ) > 0, then
there exist non-negative real numbers 𝑦1, . . . 𝑦𝑢 and polynomials ℎ 1, . . . , ℎ𝑢 ∈ Monoid(Φ) such that:
                                                  Í
                                           𝑔 = 𝑢𝑖=1 𝑦𝑖 · ℎ𝑖 .
   The intuition here is that if every inequality in Φ holds, then all the LHS expressions in Φ are
non-negative and hence any multiplication ℎ𝑖 of them is also non-negative. As in the case of Farkas’
Lemma, Handelman’s theorem shows that this approach is not only sound but also complete. We
also need a variant that can handle strict inequalities in Φ.
   Corollary 3.8. Consider a set 𝑉 = {𝑥 1, . . . , 𝑥𝑟 } of real-valued variables and the following system
of equations over 𝑉 :
                              
                              
                               𝑎 1,0 + 𝑎 1,1 · 𝑥 1 + . . . + 𝑎 1,𝑟 · 𝑥𝑟 ⊲⊳1 0
                                                          ..
                        Φ :=
                              
                              
                                                          .
                              
                              𝑎 + 𝑎 · 𝑥 + . . . + 𝑎 · 𝑥 ⊲⊳ 0
                               𝑚,0        𝑚,1      1             𝑚,𝑟    𝑟 𝑚
in which ⊲⊳𝑖 ∈ {>, ≥} for all 1 ≤ 𝑖 ≤ 𝑚. If Φ is satisfiable and SAT(Φ) is bounded, then Φ entails a strong
polynomial inequality 𝑔 ≫ 0 if and only if there exist constants 𝑦0 ∈ (0, ∞), and 𝑦1, . . . , 𝑦𝑢 ∈ [0, ∞),
and polynomials ℎ 1, . . . , ℎ𝑢 ∈ Monoid(Φ) such that:
                                                      Í
                                           𝑔 = 𝑦0 + 𝑢𝑖=1 𝑦𝑖 · ℎ𝑖 .
    Corollary 3.8 above can handle a wider family of standard constraints than Corollary 3.6. However,
it is also more expensive, since we now need to generate one new variable 𝑦𝑖 for every polynomial in
Monoid𝑑 (Φ) instead of Φ itself. Moreover, there is no bound 𝑑 in the theorem itself, so introducing 𝑑
would lead to semi-completeness instead of completeness, i.e. the approach would be complete only
if a large enough value of 𝑑 is used. As such, in cases where both sides of (1) are linear, Corollary 3.6
is preferable. We now consider a more expressive theorem that can handle polynomials on boths
sides of (1).
  Theorem 3.9 (Putinar’s Positivstellensatz [Putinar 1993]). Given a finite collection of
polynomials {𝑔, 𝑔1, . . . , 𝑔𝑘 } ∈ R[𝑥 1, . . . , 𝑥𝑛 ], let Φ be the set of inequalities defined as
                                          Φ : {𝑔1 ≥ 0, . . . , 𝑔𝑘 ≥ 0}.
If Φ entails the polynomial inequality 𝑔 > 0 and there exist some 𝑖 such that SAT(𝑔𝑖 ≥ 0) is compact,
then there exist polynomials ℎ 0, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ] such that
                                                         Í
                                              𝑔 = ℎ0 + 𝑚     𝑖=1 ℎ𝑖 · 𝑔𝑖
and every ℎ𝑖 is a sum of squares. Moreover, Φ is unsatisfiable if and only if −1 > 0 can be obtained as
above, i.e. with 𝑔 = −1.
   As in the cases of Farkas and Handelman, we need a variant of of Theorem 3.9 that can handle
strict inequalities in Φ.
  Corollary 3.10. Consider a finite collection of polynomials {𝑔, 𝑔1, . . . , 𝑔𝑘 } ∈ R[𝑥 1, . . . , 𝑥𝑛 ] and let
                                         Φ : {𝑔1 ⊲⊳1 0, . . . , 𝑔𝑘 ⊲⊳𝑘 0}
where ⊲⊳𝑖 ∈ {>, ≥} for all 1 ≤ 𝑖 ≤ 𝑘. Assume that there exist some 𝑖 such that SAT(𝑔𝑖 ≥ 0) is compact
or equivalently SAT(𝑔𝑖 ⊲⊳𝑖 0) is bounded. If Φ is satisfiable, then it entails the strong polynomial
inequality 𝑔 ≫ 0, iff there exists a constant 𝑦0 ∈ (0, ∞) and polynomials ℎ 0, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ]
such that
                                                     Í
                                       𝑔 = 𝑦0 + ℎ 0 + 𝑘𝑖=1 ℎ𝑖 · 𝑔𝑖 ,
and every ℎ𝑖 is a sum of squares.

                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:16                        Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


   Trying to use the corollary above for handling standard constraints of form (1) in Step 3 of our
algorithm leads to two problems: (i) we also need a criterion for unsatisfiability of Φ to handle the
cases where Φ ⇒ 𝜓 holds vacuously, and (ii) in our QP, we should somehow express the property
that every ℎ𝑖 is a sum of squares. We now show how each of these challenges can be handled. To
handle (i), we need another classical theorem from real algebraic geometry.
  Theorem 3.11 ([Bochnak et al. 2013, Corollary 4.1.8] the Real Nullstellensatz). Given
polynomials 𝑔, 𝑔1, . . . , 𝑔𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ], exactly one of the following two statements holds:
    • There exists 𝑥 ∈ R𝑛 , such that 𝑔1 (𝑥) = · · · = 𝑔𝑘 (𝑥) = 0, but 𝑔(𝑥) ≠ 0.
                                                                                              Í
    • There exists 𝛼 ∈ N ∪ {0} and polynomials ℎ 1, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ] such that 𝑘𝑖=1 ℎ𝑖 ·𝑔𝑖 −ℎ 0 =
      𝑔2·𝛼 and ℎ 0 is a sum of squares.
   We now combine the Real Nullstellensatz with Putinar’s Postivstellensatz to obtain a criterion
for unsatisfiability of Φ.
   Theorem 3.12. Consider a finite collection of polynomials {𝑔1, . . . , 𝑔𝑘 } ∈ R[𝑥 1, . . . , 𝑥𝑛 ] and the
following system of inequalities:
                                              Φ : {𝑔1 ⊲⊳1 0, . . . , 𝑔𝑘 ⊲⊳𝑘 0}
where ⊲⊳𝑖 ∈ {>, ≥} for all 1 ≤ 𝑖 ≤ 𝑘. Φ is unsatisfiable if and only if at least one of the following
statements holds:
    • There exist a constant 𝑦0 ∈ (0, ∞) and sum of square polynomials ℎ 0, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ]
      such that                                         Í
                                      − 1 = 𝑦0 + ℎ 0 + 𝑘𝑖=1 ℎ𝑖 · 𝑔𝑖 .                                           (5)
    • There exist 𝛼 ∈ N ∪ {0} and ℎ 0, ℎ 1, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ], such that for some
      1 ≤ 𝑗 ≤ 𝑚 with ⊲⊳ 𝑗 ∈ {>}, we have
                                           Í
                                  𝑤 4·𝛼
                                    𝑗    = 𝑚 𝑖=1 ℎ𝑖 · (𝑔𝑖 − 𝑤 𝑖 ) − ℎ 0 .
                                                              2                                                 (6)
       where ℎ 0 is a sum of squares in R[𝑥 1, . . . , 𝑥𝑛 ]. Note that 𝑤 1, . . . , 𝑤𝑘 are new variables.
     Proof. First we show that if any of the two equalities (5) or (6) holds then Φ is unsatisfiable.
Suppose Φ is satisfiable and pick 𝑣𝑎𝑙 ∈ SAT(Φ). Then, the RHS of (5) is positive at 𝑣𝑎𝑙, whereas the
LHS is negative. So, (5) cannot hold. Now define 𝑔˜𝑖 (𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ) := 𝑔𝑖 (𝑥 1, . . . , 𝑥𝑛 ) − 𝑤𝑖2 .
                                                                     Í
Using this definition, we can rewrite (6) as 𝑤 4.𝛼           𝑗    = 𝑚  𝑖=1 ℎ𝑖 · 𝑔˜𝑖 − ℎ 0 . Moreover, 𝑔 𝑗
                                                                                                        2·𝛼 = (𝑔˜ + 𝑤 2 ) 2·𝛼 .
                                                                                                                 𝑗    𝑗
Expanding the right hand side using the binomial theorem, we get 𝑔 𝑗 = 𝑤 𝑗 + ℎ ′𝑗 · 𝑔˜𝑗 for some
                                                                                             2·𝛼    4·𝛼

ℎ ′𝑗 ∈ R[𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ]. Now, substituting 𝑤 4·𝛼𝑗   (6), we get
                                                      Í
                                                     = 𝑚                        ′
                                                𝑔2·𝛼
                                                 𝑗       𝑖=1 ℎ𝑖 · 𝑔˜𝑖 − ℎ 0 + ℎ 𝑗 · 𝑔˜𝑗                                    (7)
Let us extend 𝑣𝑎𝑙, which is a valuation of {𝑣 1, . . . , 𝑣𝑛 } to a valuation 𝑣𝑎𝑙 ′ over {𝑣 1, . . . , 𝑣𝑛 , 𝑤 1, . . . , 𝑤𝑘 }
such that 𝑣𝑎𝑙 ′ |= 𝑔˜𝑖 (𝑣 1, . . . , 𝑣𝑛 , 𝑤 1, . . . , 𝑤𝑘 ) = 0 for all 1 ≤ 𝑖 ≤ 𝑘. Note that such an extension is
always possible. We get a contradiction by evaluating (7) on 𝑣𝑎𝑙 ′ as the LHS is positive, whereas
the RHS is negative.
   We now prove the other side. Suppose Φ is unsatisfiable. We have two possibilities: either Φ is also
unsatisfiable or Φ is satisfiable. Suppose Φ is unsatisfiable, then using Theorem 3.9, Φ entails −2 > 0
                                      Í
and we can write −2 = ℎ 0 + 𝑘𝑖=1 ℎ𝑖 · 𝑔𝑖 for sum of squares polynomials ℎ 0, . . . , ℎ𝑘 ∈ R[𝑥 1, . . . , 𝑥𝑛 ].
Therefore,                                                         Í
                                                   −1 = 1 + ℎ 0 + 𝑘𝑖=1 ℎ𝑖 · 𝑔𝑖
which fits into (5). Now we are left with the case when Φ is satisfiable but Φ is unsatisfiable. We
first reorder the inequalities in Φ such that the non-strict inequalities appear first in the order. Let 𝑗
be the smallest index for which Φ[1 . . . 𝑗], i.e. the set of first 𝑗 inequalities in Φ, is unsatisfiable. By
definition, Φ[1 . . . 𝑗 − 1] is satisfiable and hence SAT(Φ[1 . . . 𝑗 − 1]) = SAT(Φ[1 . . . 𝑗 − 1]). We can

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                            1:17


rewrite Φ[1 . . . 𝑗] = Φ[1 . . . 𝑗 −1] ∧ (𝑔 𝑗 > 0). As Φ[1 . . . 𝑗] is unsatisfiable, we know that Φ[1 . . . 𝑗 −1]
entails 𝑔 𝑗 ≤ 0. More precisely, this means SAT(Φ[1 . . . 𝑗 − 1]) ⊆ SAT(𝑔 𝑗 ≤ 0). On taking closures on
both sides we get SAT(Φ[1 . . . 𝑗 − 1]) ⊆ SAT(𝑔 𝑗 ≤ 0). This implies that Φ[1, . . . 𝑗 − 1] entails 𝑔 𝑗 ≤ 0
and hence Φ[1 . . . 𝑗] entails 𝑔 𝑗 = 0. As defined above, 𝑔˜𝑖 (𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ) = 𝑔𝑖 (𝑥 1, . . . , 𝑥𝑛 ) −𝑤𝑖2 .
Now, we will show that there is no valuation 𝑣𝑎𝑙 ∗ over the variables {𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 } such
that for all 1 ≤ 𝑖 ≤ 𝑗, 𝑔˜𝑖 (𝑣𝑎𝑙 ∗ ) = 0 but 𝑔 𝑗 (𝑣𝑎𝑙 ∗ ) ≠ 0. Suppose there exist such a valuation 𝑣𝑎𝑙 ∗ . Let
us define 𝑣𝑎𝑙 to be the restriction of 𝑣𝑎𝑙 ∗ to {𝑥 1, . . . , 𝑥𝑛 }. For each 1 ≤ 𝑖 ≤ 𝑗, we get 𝑔𝑖 (𝑣𝑎𝑙) ≥ 0 as
𝑔˜𝑗 (𝑣𝑎𝑙 ∗ ) = 0. We also get 𝑔 𝑗 (𝑣𝑎𝑙) = 𝑔 𝑗 (𝑣𝑎𝑙 ∗ ) ≠ 0. Hence, we get a contradiction with the previous
result that Φ[1 . . . 𝑗] entails 𝑔 𝑗 = 0. Applying the Real Nullstellensatz (Theorem 3.11) to 𝑔˜𝑖 ’s and 𝑔 𝑗 ,
we have                                                     Í𝑗 ˜
                                                    𝑔2·𝛼
                                                      𝑗   = 𝑖=1  ℎ𝑖 · 𝑔˜𝑖 − ℎ 0
where 𝛼 is a non-negative integer and ℎ˜𝑖 ’s and ℎ 0 are sums of sqaures in R[𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ].
Using the definition of 𝑔 𝑗 = 𝑔˜𝑗 + 𝑤 2𝑗 and the binomial theorem, we get 𝑔2·𝛼                              ′
                                                                                              𝑗       𝑗 + ℎ 𝑗 · 𝑔˜𝑗 for some
                                                                                                  = 𝑤 4·𝛼
ℎ ′𝑗 ∈ R[𝑥 1, . . . , 𝑥𝑛 , 𝑤 1, . . . , 𝑤𝑘 ]. Therefore, we finally get the following expression:
                                                    ℎ𝑖 · (𝑔𝑖 − 𝑤𝑖2 ) − ℎ ′𝑗 · (𝑔 𝑗 − 𝑤 2𝑗 ) − ℎ 0
                                                Í𝑗 ˜
                                        𝑤 4·𝛼
                                          𝑗   = 𝑖=1
which fits into the format of (6), hence completing the proof.                                                                □
   Finally, we provide the needed theorems to check that a certain polynomial ℎ is a sum of squares
using QP.
                                                                                                       
   Theorem 3.13 ([Blekherman et al. 2012, Theorem 3.39]). Let 𝑎® be the vector of all 𝑛+𝑑          𝑑      mono-
mials of degree less than or equal to 𝑑 over the variables {𝑥 1, . . . , 𝑥𝑛 }. A polynomial 𝑝 ∈ R[𝑥 1, . . . , 𝑥𝑛 ]
of degree 2 · 𝑑 is a sum of squares if and only if there exist a positive semidefinite matrix 𝑄 of order
 𝑛+𝑑 
  𝑑    such that 𝑝 = 𝑎𝑇 · 𝑄 · 𝑎.
  Theorem 3.14 (Cholesky decomposition [Watkins 2004]). A symmetric square matrix 𝑄 is
positive semidefinite if and only if it has a Cholesky decomposition of the form 𝑄 = 𝐿𝐿𝑇 where 𝐿 is a
lower-triangular matrix with non-negative diagonal entries.
   Based on Theorems 3.13 and 3.14, a polynomial 𝑝 of degree 2 · 𝑑 is a sum of squares if and
only if it can be written as 𝑝 = 𝑎𝑇 · 𝐿 · 𝐿𝑇 · 𝑎 such that diagonal entries of 𝐿 are non-negative.
This representation provides us with a simple approach to generate a sum-of-squares polynomial
of degree 2 · 𝑑 with symbolic coefficients and encoding them in QP. We first generate a lower
                                 
triangular matrix 𝐿 of order 𝑛+𝑑
                              𝑑    by creating one fresh variable for each entry in the lower triangle
and adding the extra condition that the entries on the diagonal must be non-negative. Then, we
symbolically compute 𝑎𝑇 · 𝐿 · 𝐿𝑇 · 𝑎.

3.3 Details of Step 3 of the Algorithm
We now have all the necessary ingredients to provide a variant of Step 3 of the algorithm that
preserves completeness. We assume a positive integer 𝑑 is given as part of the input. This 𝑑 serves
as an upper-bound on the degrees of polynomials/templates that we use in Handelman’s theorem
(the monoid) and the Stellensätze. Our approach is complete as long as a large enough 𝑑 is chosen.
Step 3: Eliminating Program Variables and Reduction to QP. Recall that at the end of Step 2,
we have a finite set of standard constraints of form (1). In this step, the algorithm handles each
standard constraint separately and reduces it to quadratic programming over template variables
and newly-introduced variables, hence effectively eliminating the program variables and the
quantification over them. Let 𝑓1 ⊲⊳1 0 ∧ 𝑓2 ⊲⊳2 0 ∧ . . . ∧ 𝑓𝑟 ⊲⊳𝑟 0 ⇒ 𝑓 ⊲⊳ 0 be one of the standard
constraints. The algorithm considers three cases: (i) if all the inequalities on both sides of the
constraint are affine, then it applies Farkas’ Lemma; (ii) if the LHS inequalities are affine but the

                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:18                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


RHS is a higher-degree polynomial, then the algorithm applies Handelman’s theorem; and (iii) if the
LHS contains higher-degree polynomials, the algorithm applies the Stellensätze and Theorem 3.12.
Below, we define Φ : {𝑓1 ⊲⊳1 0, 𝑓2 ⊲⊳2 0, . . . , 𝑓𝑟 ⊲⊳𝑟 0} and 𝜓 : 𝑓 ⊲⊳ 0.
Step 3.(i). Applying Farkas’ Lemma. Assuming all the constraints in Φ and 𝜓 are affine, we can
apply Corollary 3.6. Based on this corollary, we have to consider three cases disjunctively:
  (1) Φ is satisfiable and entails 𝜓 : The algorithm creates new template variables
                                                                                 Í 𝑦0, . . . , 𝑦𝑟 with the
      constraint 𝑦𝑖 ≥ 0 for every 𝑖. It then symbolically computes 𝑓 = 𝑦0 + 𝑟𝑖=1 𝑦𝑖 · 𝑓𝑖 . The latter is
      a polynomial equality over V. So, the algorithm equates the coefficients of corresponding
      monomials on both sides, hence reducingÍ     this case to QP. Additionally, if𝜓 is a strict inequality,
      the algorithm adds the extra constraint ⊲⊳𝑖 ∈ {> } 𝑦𝑖 > 0.
  (2) Φ is unsatisfiable and −1 ≥ 0 can Í be obtained: This is similar to the previous case, except that
      −1 should be written as 𝑦0 + 𝑟𝑖=1 𝑦𝑖 · 𝑓𝑖 .
  (3) Φ is unsatisfiable
                Í        and 0 >Í0 can be obtained: This is also similar to the last two cases. We have
      0 = 𝑦0 + 𝑟𝑖=1 𝑦𝑖 · 𝑓𝑖 and ⊲⊳𝑖 ∈ {> } 𝑦𝑖 > 0.
Note that the template variables 𝑦 are freshly generated in each case above. Also, we have to
consider cases (2) and (3) because Φ is unsatisfiable in these cases and hence the constraint Φ ⇒ 𝜓
always holds vacuously.
Step 3.(ii). Applying Handelman’s Theorem. Assuming all constraints in Φ are linear but 𝜓 is a
higher-degree polynomial inequality, the algorithm applies Corollaries 3.6 and 3.8. Again, we have
to consider the same three cases as in Step 3.(i):
   (1) Φ is satisfiable and entails𝜓 : We apply Corollary 3.8. The algorithm first symbolically computes
       Monoid𝑑 (Φ) = {ℎ 1, ℎ 2, . . . , ℎ𝑢 }. It then generates new template variables 𝑦0, 𝑦1, . . . , 𝑦𝑢 and
       constrains them by setting 𝑦0, 𝑦1, 𝑦2, . . . , 𝑦𝑢 ≥ 0. If 𝜓 is a strict inequality, it further adds the
       constraint 𝑦0 > 0. It then symbolically computes the equality
                                                        Í
                                               𝑓 = 𝑦0 + 𝑢𝑖=1 𝑦𝑖 · ℎ𝑖 .
       As usual, this is an equality whose both sides are polynomials over V. So, the algorithm
       equates the coefficients of corresponding monomials on the LHS and RHS, which reduces
       this case to QP.
   (2) Note that Φ consists of linear inequalities, so we can use Farkas’ Lemma to check if Φ is
       unsatisfiable. As such, this step is the same as case (2) of Step 3.(i).
   (3) This is the same as case (3) of Step 3.(i).
Step 3.(iii). Applying Stellensätze. If Φ includes polynomial inequalities of degree 2 or larger,
then we have to apply Corollary 3.10 and Theorem 3.12. The algorithm considers three cases and
combines them disjunctively:
  (1) Φ is satisfiable and entails 𝜓 : In this case, we apply Corollary 3.10. The algorithm generates
      template sum-of-squares polynomials ℎ 0, . . . , ℎ𝑟 of degree 𝑑 and adds QP constraints that
      ensure each ℎ𝑖 is a sum of squares (See the end of Section 3.2). It also generates a non-negative
      fresh variable 𝑦0 . If 𝜓 is strict, the algorithm adds the constraint 𝑦0 > 0. Finally, the algorithm
      symbolically computes
                                                         Í
                                           𝑓 = 𝑦0 + ℎ 0 + 𝑟𝑖=1 ℎ𝑖 · 𝑓𝑖 ;
       and equates the corresponding coefficients in the LHS and RHS to obtain QP constraints.
   (2) Φ is unsatisfiable due to the first condition of Theorem  Í 3.12: This case is handled similary to
       case (1) above, except that we have −1 = 𝑦0 + ℎ 0 + 𝑟𝑖=1 ℎ𝑖 · 𝑓𝑖 .
   (3) Φ is unsatisfiable due to the second condition of Theorem 3.12: The algorithm introduces 𝑟 new
       program variables 𝑤 1, . . . , 𝑤𝑟 . It then generates a sum-of-squares template polynomial ℎ over
       V and arbitrary template polynomials ℎ 1, . . . , ℎ𝑘 over V ∪ {𝑤 1, . . . , 𝑤𝑟 }. All ℎ𝑖 ’s are degree-𝑑

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                  1:19


       templates. Finally, for every index 𝑗 that corresponds to a strict inequality, i.e. ⊲⊳ 𝑗 ∈ {>}, the
       algorithm symbolically computes
                                        ′ Í
                                    𝑤 𝑑𝑗 = 𝑟𝑖=1 ℎ𝑖 · (𝑓𝑖 − 𝑤𝑖2 ) − ℎ 0,
     in which 𝑑 ′ is the largest multiple of 4 that does not exceed 𝑑. Note that this is an equal-
     ity between two polynomials over V ∪ {𝑤 1, . . . , 𝑤𝑟 }. As before, the algorithm equates the
     coefficients of corresponding monomials on both sides of the equality and reduces it to QP.
  After the algorithm runs Step 3 as above, all standard constraints generated in Step 2 will be
reduced to QP and can hence be passed to an external solver in Step 4, as illustrated in Section 3.1.
Degree bounds. We are using the same bound 𝑑 for the degree of the polynomials and templates
in all cases above. This is not a requirement. One can fix different degree bounds for each case.
Handling Boundedness. To achieve completeness, we need the boundedness assumption, i.e. that
for every variable 𝑣 ∈ V, we always have −𝑀 ≤ 𝑣 ≤ 𝑀. To model this in the algorithm, we can
add the boundedness inequalities to the left-hand side of every standard constraint. Additionally,
we can get a concrete value for 𝑀 as part of the input, or treat 𝑀 symbolically, i.e. as a template
variable, and let the QP solver synthesize a value for it.

3.4 Soundness and Completeness
We now prove that our algorithm is sound and semi-complete for TBSP. The soundness result
needs no extra assumptions and can be obtained directly. The completeness on the other hand
relies on several assumptions: (i) boundedness, (ii) having chosen a large enough degree bound 𝑑,
and (iii) having invariants and post-conditions that, when written in DNF form, consist only of
strongly positive polynomial inequalities of the form 𝑔 ≫ 0.
  Theorem 3.15 (Soundness). Given a sketch polynomial program or equivalently a sketch polyno-
mial transition system (SPTS) of the form (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I) together with a cutset C as input,
every concrete polynomial transition system (PTS) synthesized by the algorithm above is inductively
valid.
   Proof. The standard constraints of form (1) generated in Step 2 are equivalent to the initiation,
consecution and finalization constraints in the definition of inductive validity. The reduction from
standard constraints to QP in Step 3 is also sound since, in every case, it either writes the RHS of
the standard constraint as a combination of the LHS polynomials, hence proving that it holds, or
otherwise proves that the LHS is unsatisfiable and thus the standard constraint holds vacuously. □
   Theorem 3.16 (Semi-completeness). Consider a solvable sketch polynomial transition system
(SPTS) of the form (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I), together with a cutset C, that is given as input. Moreover,
assume that:
   (1) The boundedness assumption holds, i.e. there is a constant 𝑀 ∈ (0, ∞) such that for every 𝑣 ∈ V,
       we always have −𝑀 ≤ 𝑣 ≤ 𝑀.
   (2) Every invariant I(ℓ) and post-condition 𝜃 𝑓 , when written in disjunctive normal form, contains
       only strongly positive polynomial inequalities of the form 𝑔 ≫ 0.
Then, there exists a constant degree bound 𝑑 ∈ N, for which the algorithm above is guaranteed to
successfully synthesize an inductively valid polynomial transition system (PTS).
   Proof. Since our instance is solvable, there is a valuation 𝑣𝑎𝑙 T for the template variables that
yields an inductively valid PTS. We prove that for large enough 𝑑, the valuation 𝑣𝑎𝑙 T is obtained
by one of the solutions of the QP instance solved in Step 4 of the algorithm. The proof is pretty
straightforward since we just have to check that all steps of our algorithm are complete. Step 2 is
complete since it simply rewrites the inductive validity constraints as an equivalent set of standard
constraints. For Step 3, we prove completeness of each case separately. Step 3.(i) is complete due to

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:20                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


Farkas’ Lemma (Corollary 3.6). In Step 3.(ii), if Φ is unsatisfiable, then the algorithm is complete
based on Corollary 3.6. Otherwise, it is complete based on Corollary 3.8. However, since we are
using a degree bound 𝑑 for the monoid, the completeness only holds if the chosen 𝑑 is large enough.
Moreover, Corollary 3.8 requires strong positivity of 𝑔, which corresponds to invariants and post-
conditions in our use-case, and boundedness of SAT(Φ), which is a direct consequence of our
boundedness assumption. Finally, Step 3.(iii) is complete due to Corollary 3.10 and Theorem 3.12.
These depend on 𝑑, strong positivity and boundedness in the exact same manner as in the case of
Step 3.(ii).                                                                                      □

Limitations of Completeness. The main limitation in our completeness result is that it holds only
if the degree bound 𝑑 chosen for the template polynomials is large enough. This is why we call
it a semi-completeness theorem. In theory, it is possible to come up with adversarial instances in
which the required degree is exponentially high [Mai and Magron 2022]. In practice, we rarely,
if ever, need to use a higher degree than that of the polynomials that are already part of the
input SPTS. The second limitation is boundedness. This limitation cannot be lifted since both
Handelman’s Theorem and Putinar’s Positivstellensatz assume compactness, which is equivalent to
being closed and bounded in R𝑛 . Nevertheless, it does not have a significant practical effect and the
algorithm remains sound even without this assumption. It is also noteworthy that the treatment of
the linear/affine case using Farkas’ Lemma requires neither boundedness nor any specific value of
𝑑 and is always complete. Finally, strong positivity in the invariants and post-conditions is needed
because Putinar’s Positivstellensatz and Theorem 3.12 can only provide a sound and complete
characterization of strongly positive polynomials over a bounded semi-algebraic set 𝑋 ⊆ 𝑅𝑛 if we do
not assume that 𝑋 itself is closed. In terms of the synthesis problem, this means that our algorithm
is not guaranteed to be complete for inequalities of the form 𝑓 > 0 in the invariants/post-conditions
for which the value of 𝑓 in the runs of the program can get arbitrarily close to 0. However, this
limitation is also not significant in practice because (i) our soundness does not depend on it, and
(ii) 𝑓 + 𝜖 ≫ 0 holds for any constant 𝜖 > 0. So, a small change (by any value 𝜖 > 0) in the
invariants/postconditions leads to an instance over which our completeness holds.

4 DECIDABILITY AND NP-HARDNESS
In this section, we study the decision variant of TBSP, in which we are given an SPTS of the form
Γ = (V, T, L, ℓ0, 𝜃 0, ℓ𝑓 , 𝜃 𝑓 , T , I) and should decide whether there exists a valuation 𝑣𝑎𝑙 T : T → R for
the template variables under which Γ turns into an inductively valid PTS.
Reduction to the First-order Theory of the Reals. Suppose V = {𝑣 1, . . . , 𝑣𝑚 } and T = {𝑡 1, . . . , 𝑡𝑚′ }.
Recall that Step 2 of our algorithm is sound and complete and reduces all the constraints to the
form shown in Equation (2). However, in the synthesis algorithm, we are looking for a valuation
to the template variables T that ensures (2). Hence, in the decision variant, we are interested in
deciding the following first-order formula over the reals:
                          ∃𝑡 1, 𝑡 2, . . . , 𝑡𝑚′ ∀𝑣 1, 𝑣 2, . . . , 𝑣𝑚 (𝜅 1 ∧ 𝜅 2 ∧ . . . ∧ 𝜅𝑢 )              (8)
It is well-known that the first-order theory of the reals is decidable and hence so is our problem.
Specifically, one can apply Tarski’s quantifier elimination method [Tarski 1949] to (8). Note that
while this proves decidability in theory, decision procedures and quantifier elimination on the first-
order theory of the reals are notoriously unscalable and since (8) contains a quantifier alternation,
it is practically beyond the reach of all modern solvers, even for toy programs.
NP-hardness. We prove our problem is strongly NP-hard, even for linear/affine transition systems,
                                                                                Ó Ô3
by providing a reduction from 3SAT. Consider a 3SAT instance 𝑚                   𝑖=1   𝑗=1 𝑙𝑖,𝑗 over the boolean
variables {𝑥 1, . . . , 𝑥𝑛 }, i.e. each literal 𝑙𝑖,𝑗 is either an 𝑥𝑘 or a ¬𝑥𝑘 . We define the expression 𝑒 (𝑙𝑖,𝑗 )
as 𝑥𝑘 if 𝑙𝑖,𝑗 = 𝑥𝑘 and 1 − 𝑥𝑘 if 𝑙𝑖,𝑗 = ¬𝑥𝑘 . To reduce this 3SAT instance to our problem, we let

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                      1:21


V = {𝑥 1, . . . , 𝑥𝑛 } and T = {𝑡 1, . . . , 𝑡𝑛 }. We then consider the sketch transition system corresponding
to the following program:
        @real: 𝑥 1 , 𝑥 2 , . . . , 𝑥𝑛
        @pre: 𝑥 1 = 𝑡 1 ∧ 𝑥 2 = 𝑡 2 ∧ . . . ∧ 𝑥𝑛 = 𝑡𝑛 ;
        if (𝑥 1 > 0.5)
                𝑥 1 = 1;
        else
                𝑥 1 = 0;
                 ..
                  .
        if (𝑥𝑛 > 0.5)
                𝑥𝑛 = 1;
        else
                𝑥𝑛 = 0;
                Ó
        @post: 𝑚    𝑖=1 𝑒 (𝑙𝑖,1 ) + 𝑒 (𝑙𝑖,2 ) + 𝑒 (𝑙𝑖,3 ) > 0.5;

Note that the template variables are appearing in the pre-condition. It is easy to see that the
synthesis instance has a solution if and only if the 3SAT instance is satisfiable.

5 IMPLEMENTATION AND EXPERIMENTAL RESULTS
In this section, we report on a prototype implementation of our algorithm and our experimental
results.
Implementation. We implemented our approach in Python and used SymPy [Meurer et al. 2017]
for symbolic computations. We also used the Z3 SMT solver [Moura and Bjørner 2008] to handle
the final QP instances. In all cases, we used quadratic templates for the holes and set the technical
parameter (degree upper-bound) 𝑑 to 2.
Experimental Setting. All experimental results were obtained on an Intel i9-10980HK Processor
(8 cores, 16 threads, 5.3 GHz, 16 MB Cache) with 32 GB of RAM running Microsoft Windows 10.
Heuristics. We used the following simple heuristics to speed up the solution of the QP instance by
the SMT solver:
    • Simplifying Standard Constraints: We apply the simplification procedure illustrated in Exam-
      ple 3.2. Specifically, it is often the case that for some 𝑣 1, 𝑣 2 ∈ V ∪ V′, the standard constraint
      contains 𝑣 1 = 𝑣 2 on its left-hand side. In these cases, we merge 𝑣 1 and 𝑣 2 into a single variable.
      Similarly, if the left-hand side of a standard constraint has 𝑣 1 = 𝑐 for a real constant 𝑐, then
      we simply replace every occurrence of 𝑣 1 with 𝑐.
    • Strengthening the Constraints: Our algorithm introduces a large number of template variables,
      not only in Step 1, but also in Step 3, where each of the Stellensätze lead to the creation of new
      coefficient variables. Such new variables are created, for example, in the linear combinations
      appearing in Farkas/Handelman and the sum-of-squares template polynomials in Putinar. For
      most real-world cases, the vast majority of the template variables should be set to 0 in solutions
      to the QP. However, their inclusion makes the QP much larger and more complicated and can
      even lead to the failure of other heuristics used by the SMT solver. Hence, we use a process
      which is intuitively the opposite of abstraction-refinement. We start with a strengthened
      version of our QP instance and repeatedly make it weaker, but never weaker than the original
      instance, until the SMT solver finds a solution. Specifically, we first add additional constraints
      of the form 𝑡 = 0 for every template variable 𝑡. This strengthens the constraints but makes
      the problem easier for the SMT solver, since it can now simply plug in the 0 values and
      solve a lower-dimensional QP. Additionally, it would very likely lead to an unsatisfiable QP.
      However, Z3 can then provide us with an unsatisfiability core, i.e. a minimal subset of QP
      constraints that are unsatisfiable. If the core does not include any of our 𝑡 = 0 constraints,

                                    Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:22                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


                       @prog: ClosestCubeRoot
                       @real: 𝑎, 𝑥, 𝑠, 𝑟 ;
                       @pre: 𝑎 ≥ 0;
                       𝑥 = 𝑎;
                       𝑟 = 1;
                       s = 3.25;
                       @invariant: 𝑥 ≥ 0 ∧ −12 · 𝑟 2 + 4 · 𝑠 = 1 ∧ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 + 4 · 𝑥 − 4 · 𝑎 = 1
                       while (𝑥 − 𝑠 ≥ 0)
                       {
                              𝑥 = 𝑥 −𝑠 ;
                              𝑠 = 3+𝑠 +6 ·𝑟 ;
                              𝑟 = 𝑟 + 1;
                       }
                       @post: 4 · 𝑟 3 + 6 · 𝑟 2 + 3 · 𝑟 ≥ 4 · 𝑎 ≥ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 − 1



                                                           @prog: SquareRootFloor
          @prog: ClosestSquareRoot                         @real: 𝑎, 𝑠𝑢, 𝑡, 𝑛;
          @real: 𝑎, 𝑥, 𝑟 ;                                 @pre: 𝑛 ≥ 0;
          @pre: 𝑎 ≥ 1;                                     𝑎 = 0;
          𝑥 = 0.5 · 𝑎;                                     𝑠𝑢 = 1;
          𝑟 = 0;                                           𝑡 = 1;
          @invariant: 𝑎 = 2 · 𝑥 + 𝑟 2 − 𝑟 ∧ 𝑥 ≥ 0          @invariant: 𝑎 2 ≤ 𝑛 ∧ 𝑡 = 2 · 𝑎 + 1 ∧ 𝑠𝑢 = (𝑎 + 1) 2
          while (𝑥 ≥ 𝑟 )                                   while (𝑠𝑢 ≤ 𝑛)
          {                                                {
                   𝑥 = 𝑥 −𝑟 ;                                      𝑎 = 𝑎 + 1;
                   𝑟 = 𝑟 + 1;                                      𝑡 = 2+𝑡 ;
          }                                                        𝑠𝑢 = 𝑠𝑢 + 𝑡 ;
          @post: 𝑟 2 − 𝑟 ≥ 𝑎 − 2 · 𝑟 ∧ 𝑟 2 − 𝑟 ≤ 𝑎         }
                                                           @post((a * a) <= n);




       then we know that the original QP is also unsatisfiable. Otherwise, we simply remove all the
       𝑡 = 0 constraints in the core and repeat the same process.

Experimental Results. We now illustrate several programs that we synthesized using our imple-
mentation. In each case, we show the completed program, in which the synthesized parts are boxed.
Due to space limitations, some examples are relegated to Appendix A. Table 1 provides a summary
of the runtimes of our algorithm over these examples.
    • PositivityEnforcement: We are synthesizing an expression such that adding it to the given
      polynomial makes it positive for all possible inputs.
    • SquareCompletion: We are synthesizing a number such that adding it to the given polyno-
      mial makes it always positive.
    • SlidingBody: Consider the following Physics problem: An object is placed on an inclined
      plane of given length 𝑙. The inclination is given in terms of the sine and cosine of its angle.
      The coefficients of static and kinetic friction are also known. We want to find whether the
      body will slide and, if so, find the time it will take for it to reach the bottom of the plane.
      A physics student can easily write a program template as shown in the example for solving
      this problem using the principles and equations from classical mechanics. For example, the
      student can use an if block to decide if the body will move or not. Then, inside the block,
      they can use an equation of motion that holds for the various parameters involved in the
      problem. Now, to find the time it takes to slide down, they can leave a program hole in the
      template.

Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                    1:23


      @prog: SquareRootApproximation
                                                        @prog: ConsecutiveCubes
      @real: 𝑎, 𝑒𝑟𝑟, 𝑟, 𝑞, 𝑝;
                                                        @real: 𝑁 , 𝑛, 𝑥, 𝑦, 𝑧, 𝑠;
      @pre: 𝑎 ≥ 1 ∧ 𝑒𝑟𝑟 ≥ 0;
                                                        @pre: 1 ≥ 0;
      𝑟 = 𝑎 − 1;
                                                        𝑛 = 0;
      𝑞 = 1;
                                                        𝑥 = 0;
      𝑝 = 0.5;
                                                        𝑦 = 1;
      @invariant: 𝑝 ≥ 0 ∧ 𝑟 ≥ 0 ∧ 𝑎 = 𝑞 2 + 2 · 𝑟 · 𝑝
                                                        𝑧 = 6;
      while (2 · 𝑝 · 𝑟 ≥ 𝑒𝑟𝑟 )
                                                        𝑠 = 0;
      {
                                                        @invariant: 𝑧 = 6 · 𝑛 ∧ 𝑦 = 3 · 𝑛 2 + 3 · 𝑛 + 1 ∧ 𝑥 = 𝑛 3
               if (2 · 𝑟 − 2 · 𝑞 − 𝑝 ≥ 0)
                                                        while (𝑛 ≤ 𝑁 )
               {
                                                        {
                        𝑟 = 2 ·𝑟 −2 ·𝑞 −𝑝 ;
                                                               if (𝑥 = 𝑛 3 )
                        𝑞 =𝑝 + 𝑞;
                                                               {
                        𝑝 = 𝑝/2;
                                                                          𝑠 = 𝑠 + 𝑥;
               }
                                                               }
               else
                                                               𝑛 = 𝑛 + 1;
               {
                                                               𝑥 = 𝑦 +𝑥 ;
                        𝑟 = 2 ·𝑟 ;
                                                               𝑦 = 𝑦 +𝑧;
                        𝑝 = 𝑝 · 0.5;
                                                               𝑧 = 6+𝑧;
               }
                                                        }
      }
                                                        @post: 1 ≥ 0;
      @post:𝑞 2 ≥ 𝑎 − 𝑒𝑟𝑟 ∧ 𝑞 2 ≤ 𝑎


                            Example                       Step 2    Step 3   Step 4 (Z3)
                            ArchimedesPrinciple           0.10      0.27     0.22
                            ClosestCubeRoot               0.13      12.48    3.20
                            ClosestSquareRoot             0.09      2.21     1.31
                            ConsecutiveCubes              0.14      35.00    20.92
                            PolynomialApproximation       0.09      0.10     0.05
                            PositivityEnforcement         0.08      0.08     0.03
                            SlidingBody                   0.10      0.30     0.22
                            SquareCompletion              0.07      0.08     0.04
                            SquareRootApproximation       0.12      14.87    5.54
                            SquareRootFloor               0.11      8.09     2.31
                  Table 1. The runtimes of the different steps of our algorithm in seconds.



    • ArchimedesPrinciple: A cuboid with dimensions (𝑙, 𝑏, ℎ) of density 𝜌 is placed in a fluid
       of density 𝜌 ′. We want to determine whether the body will float, and if it floats, find the
       percentage of the volume of the body that will be outside the fluid.
    • ClosestCubeRoot[Rodríguez-Carbonell 2018]: Given a positive real number 𝑛, we need to
       synthesize a program that computes the closest integer cube root of 𝑛.
    • SquareRootFloor[Rodríguez-Carbonell 2018]: Given a positive real number 𝑛, we need to
       synthesize a program that computes the floor of the square root of 𝑛.
    • SquareRootApproximation[Rodríguez-Carbonell 2018]: Given a positive       √ real number 𝑛
       and an error threshold 𝜖, we need to synthesize a program that computes 𝑛.
    • ConsecutiveCubes[Rodríguez-Carbonell 2018]: We want to synthesize a program that
       computes the sum of first 𝑛 cubes.
   In summary, our algorithm is able to handle various polynomial synthesis problems, including
examples from physics and [Rodríguez-Carbonell 2018] in a few seconds. Hence, not only is the
algorithm semi-complete in theory, but it is also applicable in practice.

ACKNOWLEDGMENTS
This section was removed to preserve anonymity.

                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:24                        Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


REFERENCES
Alessandro Abate, Cristina David, Pascal Kesseli, Daniel Kroening, and Elizabeth Polgreen. 2018. Counterexample guided
   inductive synthesis modulo theories. In CAV. 270–288.
Sheshansh Agrawal, Krishnendu Chatterjee, and Petr Novotnỳ. 2017. Lexicographic ranking supermartingales: an efficient
   approach to termination of probabilistic programs. In POPL.
Rajeev Alur, Rastislav Bodik, Garvit Juniwal, Milo MK Martin, Mukund Raghothaman, Sanjit A Seshia, Rishabh Singh,
   Armando Solar-Lezama, Emina Torlak, and Abhishek Udupa. 2013. Syntax-Guided Synthesis. FMCAD (2013).
Rajeev Alur, Dana Fisman, Saswat Padhi, Andrew Reynolds, Rishabh Singh, and Abhishek Udupa. 2019. SyGuS-Comp:
   Syntax-guided Synthesis Competition. https://sygus.org/.
Rajeev Alur, Rishabh Singh, Dana Fisman, and Armando Solar-Lezama. 2018. Search-based program synthesis. Commun.
   ACM 61, 12 (2018), 84–93.
Ali Asadi, Krishnendu Chatterjee, Hongfei Fu, Amir Kafshdar Goharshady, and Mohammad Mahdavi. 2021. Polynomial
   reachability witnesses via Stellensätze. In PLDI. 772–787.
Grigoriy Blekherman, Pablo A Parrilo, and Rekha R Thomas. 2012. Semidefinite optimization and convex algebraic geometry.
   SIAM.
Jacek Bochnak, Michel Coste, and Marie-Françoise Roy. 2013. Real algebraic geometry. Vol. 36. Springer Science & Business
   Media.
Krishnendu Chatterjee, Hongfei Fu, and Amir Kafshdar Goharshady. 2016. Termination analysis of probabilistic programs
   through Positivstellensatz’s. In CAV. 3–22.
Krishnendu Chatterjee, Hongfei Fu, Amir Kafshdar Goharshady, and Ehsan Kafshdar Goharshady. 2020b. Polynomial
   invariant generation for non-deterministic recursive programs. In PLDI. 672–687.
Krishnendu Chatterjee, Hongfei Fu, and Petr Novotnỳ. 2020a. Termination analysis of probabilistic programs with martin-
   gales. Foundations of Probabilistic Programming (2020), 221–258.
Alonzo Church. 1963. Application of recursive arithmetic to the problem of circuit synthesis. Journal of Symbolic Logic 28, 4
   (1963).
Michael A Colón, Sriram Sankaranarayanan, and Henny B Sipma. 2003. Linear invariant generation using non-linear
   constraint solving. In CAV. 420–432.
Julius Farkas. 1902. Theory of simple inequalities. Journal for pure and applied mathematics (Crelles Journal) 1902, 124
   (1902), 1–27.
Grigory Fedyukovich, Sumanth Prabhu, Kumar Madhukar, and Aarti Gupta. 2019. Quantified invariants via syntax-guided
   synthesis. In CAV. 259–277.
Yijun Feng, Lijun Zhang, David N Jansen, Naijun Zhan, and Bican Xia. 2017. Finding polynomial loop invariants for
   probabilistic programs. In ATVA. 400–416.
Amir Goharshady. 2020. Parameterized and algebro-geometric advances in static program analysis. Ph.D. Dissertation.
   Institute of Science and Technology Austria.
Cordell Green. 1981. Application of theorem proving to problem solving. In Readings in Artificial Intelligence. 202–222.
Sumit Gulwani. 2011. Automating string processing in spreadsheets using input-output examples. In POPL. 317–330.
Sumit Gulwani, William R Harris, and Rishabh Singh. 2012. Spreadsheet data manipulation using examples. Commun. ACM
   55, 8 (2012), 97–105.
Sumit Gulwani, Susmit Jha, Ashish Tiwari, and Ramarathnam Venkatesan. 2011. Synthesis of loop-free programs. In PLDI.
   62–73.
Sumit Gulwani, Oleksandr Polozov, and Rishabh Singh. 2017. Program synthesis. Foundations and Trends in Programming
   Languages 4, 1-2 (2017), 1–119.
Zheng Guo, Michael James, David Justo, Jiaxiao Zhou, Ziteng Wang, Ranjit Jhala, and Nadia Polikarpova. 2019. Program
   synthesis by type-guided abstraction refinement. In POPL. 1–28.
David Handelman. 1988. Representing polynomials by positive linear functions on compact convex polyhedra. Pacific J.
   Math. 132, 1 (1988), 35–62.
Robin Hartshorne. 2013. Algebraic geometry. Vol. 52. Springer Science & Business Media.
Tristan Knoth, Di Wang, Nadia Polikarpova, and Jan Hoffmann. 2019. Resource-guided program synthesis. In PLDI. 253–268.
Andrej Kolmogoroff. 1932. Zur deutung der intuitionistischen logik. Mathematische Zeitschrift 35, 1 (1932), 58–65.
John R Koza. 1994. Genetic programming as a means for programming computers by natural selection. Statistics and
   computing 4, 2 (1994), 87–112.
Krzysztof Krawiec. 2016. Behavioral program synthesis with genetic programming. Vol. 618.
Hongming Liu, Hongfei Fu, Zhiyong Yu, Jiaxin Song, and Guoqiang Li. 2022. Location-by-Location Linear Invariant
   Generation with Farkas’ Lemma. In OOPSLA.
Ngoc Hoang Anh Mai and Victor Magron. 2022. On the complexity of Putinar–Vasilescu’s Positivstellensatz. Journal of
   Complexity (2022), 101663.
Zohar Manna and Richard J Waldinger. 1971. Toward automatic program synthesis. Commun. ACM 14, 3 (1971), 151–165.



Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                        1:25


Aaron Meurer, Christopher P Smith, Mateusz Paprocki, Ondřej Čertík, Sergey B Kirpichev, Matthew Rocklin, AMiT Kumar,
   Sergiu Ivanov, Jason K Moore, Sartaj Singh, et al. 2017. SymPy: symbolic computing in Python. PeerJ Computer Science 3
   (2017), e103.
Leonardo de Moura and Nikolaj Bjørner. 2008. Z3: An efficient SMT solver. In TACAS. 337–340.
Eike Neumann, Joël Ouaknine, and James Worrell. 2020. On ranking function synthesis and termination for polynomial
   programs. In CONCUR.
Amir Pnueli and Roni Rosner. 1989. On the synthesis of a reactive module. In POPL. 179–190.
Nadia Polikarpova, Ivan Kuraj, and Armando Solar-Lezama. 2016. Program synthesis from polymorphic refinement types.
   In PLDI. 522–538.
Mathias Preiner, Aina Niemetz, and Armin Biere. 2017. Counterexample-guided model synthesis. In TACAS. 264–280.
Mihai Putinar. 1993. Positive polynomials on compact semi-algebraic sets. Indiana University Mathematics Journal 42, 3
   (1993), 969–984.
Andrew Reynolds, Morgan Deters, Viktor Kuncak, Cesare Tinelli, and Clark Barrett. 2015. Counterexample-guided quantifier
   instantiation for synthesis in SMT. In CAV. 198–216.
Henry Gordon Rice. 1953. Classes of recursively enumerable sets and their decision problems. Transactions of the American
   Mathematical society 74, 2 (1953), 358–366.
Enric Rodríguez-Carbonell. 2018. Some programs that need polynomial invariants in order to be verified. https://www.cs.
   upc.edu/~erodri/webpage/polynomial_invariants/list.html.
Sriram Sankaranarayanan, Henny B Sipma, and Zohar Manna. 2004a. Constraint-based linear-relations analysis. In SAS.
   53–68.
Sriram Sankaranarayanan, Henny B Sipma, and Zohar Manna. 2004b. Non-linear loop invariant generation using Gröbner
   bases. In POPL. 318–329.
David E Shaw, William R Swartout, and C Cordell Green. 1975. Inferring LISP Programs From Examples. In IJCAI. 260–267.
Xujie Si, Woosuk Lee, Richard Zhang, Aws Albarghouthi, Paraschos Koutris, and Mayur Naik. 2018. Syntax-guided synthesis
   of datalog programs. In ESEC/FSE. 515–527.
David Canfield Smith. 1975. Pygmalion: a creative programming environment. Stanford University.
Dominik Sobania, Dirk Schweim, and Franz Rothlauf. 2022. A Comprehensive Survey on Program Synthesis with Evolu-
   tionary Algorithms. IEEE Transactions on Evolutionary Computation (2022).
Armando Solar-Lezama. 2008. Program synthesis by sketching. University of California, Berkeley.
Armando Solar-Lezama. 2009. The sketching approach to program synthesis. In APLAS. 4–13.
Saurabh Srivastava, Sumit Gulwani, and Jeffrey S Foster. 2010. From program verification to program synthesis. In POPL.
   313–326.
Saurabh Srivastava, Sumit Gulwani, and Jeffrey S Foster. 2013. Template-based program verification and program synthesis.
   International Journal on Software Tools for Technology Transfer 15, 5 (2013), 497–518.
Toru Takisaka, Yuichiro Oyabu, Natsuki Urabe, and Ichiro Hasuo. 2018. Ranking and repulsing supermartingales for
   reachability in probabilistic programs. In ATVA. 476–493.
Alfred Tarski. 1949. A Decision Method for Elementary Algebra and Geometry. Journal of Symbolic Logic 14, 3 (1949).
Anne S Troelstra. 1977. Aspects of constructive mathematics. In Studies in Logic and the Foundations of Mathematics. Vol. 90.
   973–1052.
David S Watkins. 2004. Fundamentals of matrix computations. Vol. 64. John Wiley & Sons.




                                  Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
                                                                                                            Benchmark               Our Approach             Sketch                    Rosette                  Direct
                                                                                                                                     Result Time         Result      Time          Result      Time         Result      Time               1:26
                                                                                                        ArchimedesPrinciple         Success 0.59         Unsat       0.33         Success      0.37        Success      0.25
                                                                                                          ClosestCubeRoot           Success 15.81       Wrong        0.46        Timed out >43200         Timed out >43200
                                                                                                         ClosestSquareRoot          Success 3.61         Failed     969.17        Success      0.15       Timed out >43200
                                                                                                         ConsecutiveCubes           Success 56.06        Failed     778.04       Timed out >43200         Timed out >43200
                                                                                                     PolynomialApproximation        Success 0.24        Wrong        0.45         Success      0.12        Success      0.14
                                                                                                       PositivityEnforcement        Success 0.19        Success      0.30        Timed out >43200          Success      0.09
                                                                                                            SlidingBody             Success 0.62         Failed      0.47          Failed     < 0.01       Success      0.13
                                                                                                         SquareCompletion           Success 0.19        Wrong        0.29         Success      0.10        Success      0.09
                                                                                                     SquareRootApproximation        Success 20.53       Wrong        0.39        Timed out >43200         Timed out >43200
                                                                                                              Cohendiv              Success 26.11       Wrong        6.297        Success      0.11        Success      0.29
                                                                                                          MannadivCarre             Success 4.07       Timed out >43200           Success      0.25        Success      316.5
                                                                                                           MannadivCube             Success 4.03        Wrong        0.33        Timed out >43200          Success      92.9
                                                                                                           MannadivInd              Success 5.25         Failed      0.408        Success      0.11        Success      0.18
                                                                                                              Wensley               Success 52.75       Wrong        0.44        Timed out >43200         Timed out >43200
                                                                                                              Euclidex2             Success 29.68      Timed out >43200           Success      0.34       Timed out >43200
                                                                                                                LCM1                Success 10.99      Timed out >43200          Timed out >43200          Success      87.29
                                                                                                               Fermat1              Success 17.95      Timed out >43200           Success      0.17        Success     117.14
                                                                                                               Fermat2              Success 9.30       Timed out >43200          Timed out >43200          Success      0.31
                                                                                                               Petter3              Success 2.51         Failed      0.493       Timed out >43200          Success     124.51
                                                                                                               Petter5              Success 1.84         Failed      2.72        Timed out >43200          Success     117.33
                                                                                                                    Table 2. Comparison of our approach with previous synthesis methods. All times are in seconds.




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
                                                                                         COMPARISON WITH ROSETTE AND SKETCH
                                                                                         Table 2 provides a comparison between our approach and the state-of-the-art synthesis tools Sketch and Rosette, as well as a direct encoding to
                                                                                         SMT that was passed to Z3. The rest of this document contains the details of programs output by these tools. All experiments were run on the
                                                                                         same machine as in our original submission with a time limit of 12 hours per instance. Note that Sketch is not sound for real variables and
                                                                                         wrong answers are expected. However, in most cases Sketch’s output is just setting everything to 0, which is wrong even for integer variables.
                                                                                                                                                                                                                                           Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani
Synthesis of Polynomial Programs                                                                                   1:27


A   MORE EXAMPLES FROM SECTION 5

                                                                                @prog: PolynomialApproximation
                                                                                @real 𝑡, 𝑥, 𝑒, 𝑔1 , 𝑔2 , 𝑛;
                                                                                @macro 𝑓1 = 𝑥 3 ;
                                                                                @macro 𝑓2 = 𝑥 3 + 𝑥;
                                                                                @macro 𝑓3 = 5 + 𝑥 + 𝑥 3 ;
                                                                                @pre: 1 ≥ 0;
      @prog: PositivityEnforcement           @prog: SquareCompletion            𝑡 = 0;
      @real: 𝑥, 𝑛;                           @real: 𝑥, 𝑛;                       𝑒 = 5;
      @pre: 𝑥 ≤ 100;                         @pre: 𝑥 ≤ 100;                     if (𝑥 ≤ 𝑡 )
      𝑥 = 𝑛 2 − 5 · 𝑛;                       𝑥 = 𝑛 2 − 5 · 𝑛;                   {
      𝑛 = 5 ·𝑛 +1;                           𝑛 = 25
                                                  4 ;                                   𝑔 1 = 𝑓3 − 𝑓1 ;
      𝑥 = 𝑥 + 𝑛;                             𝑥 = 𝑥 + 𝑛;                                 𝑛 = 𝑔1 ;
      @post: 𝑥 ≥ 0;                          @post: 𝑥 ≥ 0;                      }
                                                                                else
                                                                                {
                                                                                        𝑔 2 = 𝑓3 − 𝑓2 ;
                                                                                        𝑛 = 𝑔2 ;
                                                                                }
                                                                                @post: 𝑛 ≤ 𝑒;




                 @prog: SlidingBody
                 @real: 𝑚𝑜𝑣𝑒, 𝑒, 𝑡, 𝑔, 𝑛𝑢𝑠, 𝑛𝑢𝑘, 𝑠𝑖𝑛, 𝑐𝑜𝑠, 𝑙;            @prog: ArchimedesPrinciple
                 @pre: 𝑡 ≥ 0 ∧ 𝑛𝑢𝑠 ≥ 𝑛𝑢𝑘;                                @real: 𝑓 𝑙, 𝑚, 𝑙, 𝑏, ℎ, 𝜌, 𝑒, 𝑥;
                 𝑔 = 9.8;                                                @pre: 𝑥 ≥ 0 ∧ 𝑚 ≥ 0;
                 𝑛𝑢𝑘 = 0.2;                                              𝑙 = 10;
                 𝑛𝑢𝑠 = 0.3;                                              𝑏 = 5;
                 𝑠𝑖𝑛 = 0.5;                                              ℎ = 2;
                 𝑐𝑜𝑠 = 0.86;                                             𝜌 = 2;
                 𝑙 = 10;                                                 if ( 𝑚 ≤ 𝜌 · 𝑙 · 𝑏 · ℎ)
                 if (𝑠𝑖𝑛 ≥ 𝑛𝑢𝑠 · 𝑐𝑜𝑠)                                    {
                 {                                                               𝑓 𝑙 = 1;
                          𝑚𝑜𝑣𝑒 = 1;                                                    𝑓𝑙
                                                                                  𝑥 = 200 ;
                          𝑡 = 21
                               2 − 8.0056060865 · 𝑚𝑜𝑣𝑒 ;                          𝑒 = 𝑚 − 𝜌 · 𝑙 · 𝑏 · ℎ · 𝑥;
                          𝑒 = 𝑡 · 𝑡 · 𝑔 · 𝑠𝑖𝑛 − 𝑔 · 𝑛𝑢𝑘 · 𝑐𝑜𝑠 − 2 · 𝑙;   }
                 }                                                       else
                 else                                                    {
                 {                                                                𝑒 = 0;
                          𝑚𝑜𝑣𝑒 = 0;                                               𝑓 𝑙 = 0;
                          𝑒 = 0;                                                       𝑓𝑙
                                                                                  𝑥 = 200 ;
                          𝑡 = 21
                               2 − 8.0056060865 · 𝑚𝑜𝑣𝑒 ;                 }
                 }                                                       @post: 𝑒 = 0 ∧ 0 ≤ 𝑥 ≤ 1;
                 @post: 𝑒 = 0 ∧ 𝑡 ≥ 0;




                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:28                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


                                                                   @prog: MannadivCarre
                @prog: Cohendiv
                                                                   @real 𝑛, 𝑦, 𝑥, 𝑡 ;
                @real: 𝑥, 𝑦, 𝑞, 𝑟, 𝑑𝑑;
                                                                   @pre: 𝑛 ≥ 0;
                @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 1;
                                                                   𝑦 = 𝑛;
                𝑞 = 0;
                                                                   𝑥 = 0;
                𝑟 = 𝑥;
                                                                   𝑡 = 0;
                @invariant: 𝑥 = 𝑞 · 𝑦 + 𝑟 ∧ 𝑟 ≥ 0
                                                                   @invariant: 𝑥 2 + 2 · 𝑡 + 𝑦 − 𝑛 = 0
                while (𝑟 ≥ 𝑦)
                                                                   while(𝑦 · (𝑦 − 1) ≥ 0)
                {
                                                                   {
                       𝑑 = 1;
                                                                          if(𝑡 = 𝑥)
                       𝑑𝑑 = 𝑦;
                                                                          {
                       @invariant: 𝑑𝑑 = 𝑦 · 𝑑 ∧ 𝑥 = 𝑞 · 𝑦 + 𝑟
                                                                                      𝑦 = 𝑦 −1;
                       ∧𝑟 ≥ 0 ∧ 𝑟 ≥ 𝑦 · 𝑑
                                                                                      𝑡 = 0;
                       while(𝑟 ≥ 2 · 𝑑𝑑)
                                                                                      𝑥 = 𝑥 + 1;
                       {
                                                                          }
                                   𝑑 = 2 · 𝑑;
                                                                          else
                                   𝑑𝑑 = 2 · 𝑑𝑑 ;
                                                                          {
                       }
                                                                                      𝑦 = 𝑦 − 2;
                       𝑟 = 𝑟 − 𝑑𝑑;
                                                                                      𝑡 = 𝑡 + 1;
                       𝑞 = 𝑞 +𝑑 ;
                                                                          }
                }
                                                                   }
                @post: 1 ≥ 0;
                                                                   @post: 1 ≥ 0;




                     @prog: MannadivCube                    @prog: MannadivInd
                     @real 𝑛, 𝑦, 𝑥, 𝑡 ;                     @real 𝑥1, 𝑥2, 𝑦1, 𝑦2, 𝑦3;
                     @pre: 𝑛 ≥ 0;                           @pre: 𝑥1 ≥ 0 ∧ 𝑥2 ≥ 0;
                     𝑦 = 𝑛;                                 𝑦1 = 0;
                     𝑥 = 0;                                 𝑦2 = 0;
                     𝑡 = 0;                                 𝑦3 = 𝑥1;
                     @invariant: 𝑥 3 + 3 · 𝑡 + 𝑦 − 𝑛 = 0    @invariant: 𝑦1 · 𝑥2 + 𝑦2 + 𝑦3 = 𝑥1
                     while(𝑦 ≥ 0)                           while(𝑦3 ≥ 0)
                     {                                      {
                            if(𝑡 = 𝑥 ∗ 𝑥)                           if(𝑦2 + 1 = 𝑥2)
                            {                                       {
                                        𝑦 = 𝑦 −3 ·𝑥 −1;                      𝑦1 = 𝑦1 + 1;
                                        𝑡 = 0;                               𝑦2 = 0 ;
                                        𝑥 = 𝑥 + 1;                           𝑦3 = 𝑦3 − 1;
                            }                                       }
                            else                                    else
                            {                                       {
                                        𝑦 = 𝑦 − 3;                           𝑦2 = 𝑦2 + 1 ;
                                        𝑡 = 𝑡 + 1;                           𝑦3 = 𝑦3 − 1;
                            }                                       }
                     }                                      }
                     @post: 1 ≥ 0;                          @post: 1 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                    1:29


                                                       @prog: Euclidex2
            @prog: Wensley
                                                       @real 𝑎, 𝑏, 𝑝, 𝑞, 𝑟, 𝑠, 𝑥, 𝑦;
            @real: 𝑃, 𝑄, 𝐸, 𝑎, 𝑏, 𝑑, 𝑦;
                                                       @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 0;
            @pre: 𝑄 ≥ 𝑃 ∧ 𝑃 ≥ 0 ∧ 𝐸 ≥ 0;
                                                       𝑎 = 𝑥;
            𝑎 = 0;
                                                       𝑏 = 𝑦;
            𝑏 = 𝑄/2;
                                                       𝑝 = 1;
            𝑑 = 1;
                                                       𝑞 = 0;
            𝑦 = 0;
                                                       𝑟 = 0;
            @invariant: 𝑎 = 𝑄 · 𝑦 ∧ 𝑏 = 𝑄 · 𝑑/2
                                                       𝑠 = 1;
            ∧𝑃 − 𝑑 · 𝑄 ≤ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≤ 𝑃 ∧ 𝑄 ≥ 0
                                                       @invariant: 𝑎 = 𝑦 · 𝑟 + 𝑥 · 𝑝 ∧ 𝑏 = 𝑥 · 𝑞 + 𝑦 · 𝑠
            while (𝑑 ≥ 𝐸)
                                                       while(1 ≥ 0)
            {
                                                       {
                     if(𝑃 ≤ 𝑎 + 𝑏)
                                                              if(𝑎 ≥ 𝑏)
                     {
                                                              {
                             𝑏 = 𝑏/2 ;
                                                                          𝑎 = 𝑎 −𝑏 ;
                             𝑑 = 𝑑/2;
                                                                          𝑝 = 𝑝 −𝑞;
                     }
                                                                          𝑟 = 𝑟 − 𝑠;
                     else
                                                              }
                     {
                                                              else
                             𝑎 = 𝑎 + 𝑏;
                                                              {
                             𝑦 = 𝑦 + 𝑑/2 ;
                                                                          𝑏 = 𝑏 −𝑎;
                             𝑏 = 𝑏/2;
                                                                          𝑞 = 𝑞 − 𝑝;
                             𝑑 = 𝑑/2;
                                                                          𝑠 = 𝑠 −𝑟 ;
                     }
                                                              }
            }
                                                       }
            @post: 𝑃 ≥ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≥ 𝑃 − 𝐸 · 𝑄;
                                                       @post: 1 ≥ 0;




 @prog: LCM1
                                            @prog: Fermat1
 @real 𝑎, 𝑏, 𝑥, 𝑦, 𝑢, 𝑣;
                                            @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
 @pre: 𝑎 ≥ 0 ∧ 𝑏 ≥ 0;
                                            @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
 𝑥 = 𝑎;
                                            𝑢 = 2 · 𝑅 + 1;
 𝑦 = 𝑏;
                                            𝑣 = 1;
 𝑢 = 𝑏;
                                            𝑟 = 𝑅2 − 𝑁 ;
 𝑣 = 0;
                                            @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
 @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                            while(1 ≥ 0)
 while(1 ≥ 0)
                                            {
 {
                                                               @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                               while(1 ≥ 0)
        while(1 ≥ 0)
                                                               {
        {
                                                                      𝑟 = 𝑟 − 𝑣;
                    𝑥 = 𝑥 −𝑦;
                                                                      𝑣 = 𝑣 +2;
                    𝑣 = 𝑣 + 𝑢;
                                                               }
        }
                                                               @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                               while(1 ≥ 0)
        while(1 ≥ 0)
                                                               {
        {
                                                                      𝑟 = 𝑟 +𝑢 ;
                    𝑦 = 𝑦 − 𝑥;
                                                                      𝑢 = 𝑢 + 2;
                    𝑢 = 𝑢+𝑣;
                                                               }
        }
                                            }
 }
                                            @post: 1 ≥ 0;
 @post: 1 ≥ 0;




                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:30                          Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


       @prog: Fermat2
       @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
       @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
       𝑢 = 2 · 𝑅 + 1;
       𝑣 = 1;
                                                                        @prog: Petter3
       𝑟 = 𝑅2 − 𝑁 ;
                                                                        @real 𝑛, 𝑘, 𝑁 , 𝑠;
       @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
                                                                        @pre: 𝑁 ≥ 0;
       while(𝑟 ≥ 1)
                                                                        𝑠 = 0;
       {
                                                                        𝑛 = 0;
                          if(𝑟 ≥ 0)
                                                                        @invariant: 𝑠 = 0.25 · 𝑛 2 · (𝑛 + 1) 2 ∧ 𝑛 ≤ 𝑁 + 1
                          {
                                                                        while(𝑛 ≤ 𝑁 )
                                  𝑟 = 𝑟 − 𝑣;
                                                                        {
                                  𝑣 = 𝑣 + 2;
                                                                               𝑠 = 𝑠 + 𝑛ˆ3 ;
                          }
                                                                               𝑛 = 𝑛 + 1;
                          else
                                                                        }
                          {
                                                                        @post: 1 ≥ 0;
                                  𝑟 = 𝑟 +𝑢 ;
                                  𝑢 = 𝑢 + 2;
                          }
       }
       @post: 1 ≥ 0;




                                @prog: Petter5
                                @real 𝑛, 𝑘, 𝑁 , 𝑠;
                                @pre: 𝑁 ≥ 0;
                                𝑠 = 0;
                                𝑛 = 0;
                                @invariant: 𝑠 = 𝑛 6 ∧ 𝑛 ≤ 𝑁 + 1
                                while(𝑛 ≤ 𝑁 )
                                {
                                       𝑠 = 𝑠 + 6 · 𝑛 5 + 15 · 𝑛 4 + 20 · 𝑛 3 + 15 · 𝑛 2 + 6 · 𝑛 + 1 ;
                                       𝑛 = 𝑛 + 1;
                                }
                                @post: 1 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                       1:31


SYNTHESIS RESULTS USING SKETCH

                      @prog: ClosestCubeRoot
                      @real: 𝑎, 𝑥, 𝑠, 𝑟 ;
                      @pre: 𝑎 ≥ 0;
                      𝑥 = 𝑎;
                      𝑟 = 1;
                      s = 3.25;
                      @invariant: 𝑥 ≥ 0 ∧ −12 · 𝑟 2 + 4 · 𝑠 = 1 ∧ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 + 4 · 𝑥 − 4 · 𝑎 = 1
                      while (𝑥 − 𝑠 ≥ 0)
                      {
                             𝑥 = 0;
                             𝑠 = 0;
                             𝑟 = 𝑟 + 1;
                      }
                      @post: 4 · 𝑟 3 + 6 · 𝑟 2 + 3 · 𝑟 ≥ 4 · 𝑎 ≥ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 − 1




                                                         @prog: SquareRootFloor
           @prog: ClosestSquareRoot                      @real: 𝑎, 𝑠𝑢, 𝑡, 𝑛;
           @real: 𝑎, 𝑥, 𝑟 ;                              @pre: 𝑛 ≥ 0;
           @pre: 𝑎 ≥ 1;                                  𝑎 = 0;
           𝑥 = 0.5 · 𝑎;                                  𝑠𝑢 = 1;
           𝑟 = 0;                                        𝑡 = 1;
           @invariant: 𝑎 = Failed ∧ 𝑥 ≥ 0                @invariant: 𝑎 2 ≤ 𝑛 ∧ 𝑡 = 2 · 𝑎 + 1 ∧ 𝑠𝑢 = (𝑎 + 1) 2
           while (𝑥 ≥ 𝑟 )                                while (𝑠𝑢 ≤ 𝑛)
           {                                             {
                    𝑥 = Failed ;                                 𝑎 = 𝑎 + 1;
                    𝑟 = 𝑟 + 1;                                   𝑡 = 12 + 8 · 𝑡 ;
           }                                                     𝑠𝑢 = 2 · 𝑠𝑢 + 15 · 𝑡 + 8 ;
           @post: 𝑟 2 − 𝑟 ≥ 𝑎 − 2 · 𝑟 ∧ 𝑟 2 − 𝑟 ≤ 𝑎      }
                                                         @post(𝑎 2 ≤ 𝑛);


      @prog: SquareRootApproximation
                                                           @prog: ConsecutiveCubes
      @real: 𝑎, 𝑒𝑟𝑟, 𝑟, 𝑞, 𝑝;
                                                           @real: 𝑁 , 𝑛, 𝑥, 𝑦, 𝑧, 𝑠;
      @pre: 𝑎 ≥ 1 ∧ 𝑒𝑟𝑟 ≥ 0;
                                                           @pre: 1 ≥ 0;
      𝑟 = 𝑎 − 1;
                                                           𝑛 = 0;
      𝑞 = 1;
                                                           𝑥 = 0;
      𝑝 = 0.5;
                                                           𝑦 = 1;
      @invariant: 𝑝 ≥ 0 ∧ 𝑟 ≥ 0 ∧ 𝑎 = 𝑞 2 + 2 · 𝑟 · 𝑝
                                                           𝑧 = 6;
      while (2 · 𝑝 · 𝑟 ≥ 𝑒𝑟𝑟 )
                                                           𝑠 = 0;
      {
                                                           @invariant: 𝑧 = 6 · 𝑛 ∧ 𝑦 = 3 · 𝑛 2 + 3 · 𝑛 + 1 ∧ 𝑥 = 𝑛 3
               if (2 · 𝑟 − 2 · 𝑞 − 𝑝 ≥ 0)
                                                           while (𝑛 ≤ 𝑁 )
               {
                                                           {
                        𝑟 = 0;
                                                                  if (𝑥 = 𝑛 3 )
                        𝑞 = 𝑝 + 0;
                                                                  {
                        𝑝 = 𝑝/2;
                                                                             𝑠 = 𝑠 + 𝑥;
               }
                                                                  }
               else
                                                                  𝑛 = 𝑛 + 1;
               {
                                                                  𝑥 = Failed ;
                        𝑟 = 0;
                                                                  𝑦 = Failed ;
                        𝑝 = 𝑝 · 0.5;
                                                                  𝑧 = Failed ;
               }
                                                           }
      }
                                                           @post: 1 ≥ 0;
      @post:𝑞 2 ≥ 𝑎 − 𝑒𝑟𝑟 ∧ 𝑞 2 ≤ 𝑎


                                Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:32                       Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


                                                                                @prog: PolynomialApproximation
                                                                                @real 𝑡, 𝑥, 𝑒, 𝑔1 , 𝑔2 , 𝑛;
                                                                                @macro 𝑓1 = 𝑥 3 ;
                                                                                @macro 𝑓2 = 𝑥 3 + 𝑥;
                                                                                @macro 𝑓3 = 0 ;
                                                                                @pre: 1 ≥ 0;
       @prog: PositivityEnforcement           @prog: SquareCompletion           𝑡 = 0;
       @real: 𝑥, 𝑛;                           @real: 𝑥, 𝑛;                      𝑒 = 5;
       @pre: 𝑥 ≤ 100;                         @pre: 𝑥 ≤ 100;                    if (𝑥 ≤ 𝑡 )
       𝑥 = 𝑛 2 − 5 · 𝑛;                       𝑥 = 𝑛 2 − 5 · 𝑛;                  {
       𝑛 = 23 · 𝑛 + 23 ;                      𝑛 = 6;                                    𝑔 1 = 𝑓3 − 𝑓1 ;
       𝑥 = 𝑥 + 𝑛;                             𝑥 = 𝑥 + 𝑛;                                𝑛 = 𝑔1 ;
       @post: 𝑥 ≥ 0;                          @post: 𝑥 ≥ 0;                     }
                                                                                else
                                                                                {
                                                                                        𝑔 2 = 𝑓3 − 𝑓2 ;
                                                                                        𝑛 = 𝑔2 ;
                                                                                }
                                                                                @post: 𝑛 ≤ 𝑒;




                  @prog: SlidingBody
                  @real: 𝑚𝑜𝑣𝑒, 𝑒, 𝑡, 𝑔, 𝑛𝑢𝑠, 𝑛𝑢𝑘, 𝑠𝑖𝑛, 𝑐𝑜𝑠, 𝑙;            @prog: ArchimedesPrinciple
                  @pre: 𝑡 ≥ 0 ∧ 𝑛𝑢𝑠 ≥ 𝑛𝑢𝑘;                                @real: 𝑓 𝑙, 𝑚, 𝑙, 𝑏, ℎ, 𝜌, 𝑒, 𝑥;
                  𝑔 = 9.8;                                                @pre: 𝑥 ≥ 0 ∧ 𝑚 ≥ 0;
                  𝑛𝑢𝑘 = 0.2;                                              𝑙 = 10;
                  𝑛𝑢𝑠 = 0.3;                                              𝑏 = 5;
                  𝑠𝑖𝑛 = 0.5;                                              ℎ = 2;
                  𝑐𝑜𝑠 = 0.86;                                             𝜌 = 2;
                  𝑙 = 10;                                                 if ( 𝑚 ≤ 𝜌 · 𝑙 · 𝑏 · ℎ)
                  if (𝑠𝑖𝑛 ≥ 𝑛𝑢𝑠 · 𝑐𝑜𝑠)                                    {
                  {                                                               𝑓 𝑙 = 1;
                           𝑚𝑜𝑣𝑒 = 1;                                              𝑥 = Unsat ;
                           𝑡 = Failed ;                                           𝑒 = 𝑚 − 𝜌 · 𝑙 · 𝑏 · ℎ · 𝑥;
                           𝑒 = 𝑡 · 𝑡 · 𝑔 · 𝑠𝑖𝑛 − 𝑔 · 𝑛𝑢𝑘 · 𝑐𝑜𝑠 − 2 · 𝑙;   }
                  }                                                       else
                  else                                                    {
                  {                                                               𝑒 = 0;
                           𝑚𝑜𝑣𝑒 = 0;                                              𝑓 𝑙 = 0;
                           𝑒 = 0;                                                 𝑥 = Unsat ;
                           𝑡 = Failed ;                                   }
                  }                                                       @post: 𝑒 = 0 ∧ 0 ≤ 𝑥 ≤ 1;
                  @post: 𝑒 = 0 ∧ 𝑡 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                 1:33


                                                                 @prog: MannadivCarre
               @prog: Cohendiv
                                                                 @real 𝑛, 𝑦, 𝑥, 𝑡 ;
               @real: 𝑥, 𝑦, 𝑞, 𝑟, 𝑑𝑑;
                                                                 @pre: 𝑛 ≥ 0;
               @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 1;
                                                                 𝑦 = 𝑛;
               𝑞 = 0;
                                                                 𝑥 = 0;
               𝑟 = 𝑥;
                                                                 𝑡 = 0;
               @invariant: 𝑥 = 𝑞 · 𝑦 + 𝑟 ∧ 𝑟 ≥ 0
                                                                 @invariant: 𝑥 2 + 2 · 𝑡 + 𝑦 − 𝑛 = 0
               while (𝑟 ≥ 𝑦)
                                                                 while(𝑦 · (𝑦 − 1) ≥ 0)
               {
                                                                 {
                      𝑑 = 1;
                                                                        if(𝑡 = 𝑥)
                      𝑑𝑑 = 𝑦;
                                                                        {
                      @invariant: 𝑑𝑑 = 𝑦 · 𝑑 ∧ 𝑥 = 𝑞 · 𝑦 + 𝑟
                                                                                    𝑦 = Failed ;
                      ∧𝑟 ≥ 0 ∧ 𝑟 ≥ 𝑦 · 𝑑
                                                                                    𝑡 = 0;
                      while(𝑟 ≥ 2 · 𝑑𝑑)
                                                                                    𝑥 = 𝑥 + 1;
                      {
                                                                        }
                                  𝑑 = 2 · 𝑑;
                                                                        else
                                  𝑑𝑑 = 27 · 𝑑𝑑 + 16 ;
                                                                        {
                      }
                                                                                    𝑦 = 𝑦 − 2;
                      𝑟 = 𝑟 − 𝑑𝑑;
                                                                                    𝑡 = 𝑡 + 1;
                      𝑞 = 10 · +13 ;
                                                                        }
               }
                                                                 }
               @post: 1 ≥ 0;
                                                                 @post: 1 ≥ 0;




                    @prog: MannadivCube                   @prog: MannadivInd
                    @real 𝑛, 𝑦, 𝑥, 𝑡 ;                    @real 𝑥1, 𝑥2, 𝑦1, 𝑦2, 𝑦3;
                    @pre: 𝑛 ≥ 0;                          @pre: 𝑥1 ≥ 0 ∧ 𝑥2 ≥ 0;
                    𝑦 = 𝑛;                                𝑦1 = 0;
                    𝑥 = 0;                                𝑦2 = 0;
                    𝑡 = 0;                                𝑦3 = 𝑥1;
                    @invariant: 𝑥 3 + 3 · 𝑡 + 𝑦 − 𝑛 = 0   @invariant: 𝑦1 · 𝑥2 + 𝑦2 + 𝑦3 = 𝑥1
                    while(𝑦 ≥ 0)                          while(𝑦3 ≥ 0)
                    {                                     {
                           if(𝑡 = 𝑥 ∗ 𝑥)                          if(𝑦2 + 1 = 𝑥2)
                           {                                      {
                                       𝑦 = 0;                              𝑦1 = 𝑦1 + 1;
                                       𝑡 = 0;                              𝑦2 = Failed ;
                                       𝑥 = 𝑥 + 1;                          𝑦3 = 𝑦3 − 1;
                           }                                      }
                           else                                   else
                           {                                      {
                                       𝑦 = 𝑦 − 3;                          𝑦2 = Failed ;
                                       𝑡 = 𝑡 + 1;                          𝑦3 = 𝑦3 − 1;
                           }                                      }
                    }                                     }
                    @post: 1 ≥ 0;                         @post: 1 ≥ 0;




                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:34                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


                                                         @prog: Euclidex2
             @prog: Wensley
                                                         @real 𝑎, 𝑏, 𝑝, 𝑞, 𝑟, 𝑠, 𝑥, 𝑦;
             @real: 𝑃, 𝑄, 𝐸, 𝑎, 𝑏, 𝑑, 𝑦;
                                                         @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 0;
             @pre: 𝑄 ≥ 𝑃 ∧ 𝑃 ≥ 0 ∧ 𝐸 ≥ 0;
                                                         𝑎 = 𝑥;
             𝑎 = 0;
                                                         𝑏 = 𝑦;
             𝑏 = 𝑄/2;
                                                         𝑝 = 1;
             𝑑 = 1;
                                                         𝑞 = 0;
             𝑦 = 0;
                                                         𝑟 = 0;
             @invariant: 𝑎 = 𝑄 · 𝑦 ∧ 𝑏 = 𝑄 · 𝑑/2
                                                         𝑠 = 1;
             ∧𝑃 − 𝑑 · 𝑄 ≤ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≤ 𝑃 ∧ 𝑄 ≥ 0
                                                         @invariant: 𝑎 = 𝑦 · 𝑟 + 𝑥 · 𝑝 ∧ 𝑏 = 𝑥 · 𝑞 + 𝑦 · 𝑠
             while (𝑑 ≥ 𝐸)
                                                         while(1 ≥ 0)
             {
                                                         {
                      if(𝑃 ≤ 𝑎 + 𝑏)
                                                                if(𝑎 ≥ 𝑏)
                      {
                                                                {
                              𝑏 = Failed ;
                                                                            𝑎 = Failed ;
                              𝑑 = 𝑑/2;
                                                                            𝑝 = Failed ;
                      }
                                                                            𝑟 = 𝑟 − 𝑠;
                      else
                                                                }
                      {
                                                                else
                              𝑎 = 𝑎 + 𝑏;
                                                                {
                              𝑦 = Failed ;
                                                                            𝑏 = Failed ;
                              𝑏 = 𝑏/2;
                                                                            𝑞 = 𝑞 − 𝑝;
                              𝑑 = 𝑑/2;
                                                                            𝑠 = Failed ;
                      }
                                                                }
             }
                                                         }
             @post: 𝑃 ≥ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≥ 𝑃 − 𝐸 · 𝑄;
                                                         @post: 1 ≥ 0;




 @prog: LCM1
                                              @prog: Fermat1
 @real 𝑎, 𝑏, 𝑥, 𝑦, 𝑢, 𝑣;
                                              @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
 @pre: 𝑎 ≥ 0 ∧ 𝑏 ≥ 0;
                                              @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
 𝑥 = 𝑎;
                                              𝑢 = 2 · 𝑅 + 1;
 𝑦 = 𝑏;
                                              𝑣 = 1;
 𝑢 = 𝑏;
                                              𝑟 = 𝑅2 − 𝑁 ;
 𝑣 = 0;
                                              @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
 @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                              while(1 ≥ 0)
 while(1 ≥ 0)
                                              {
 {
                                                                 @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                                 while(1 ≥ 0)
        while(1 ≥ 0)
                                                                 {
        {
                                                                        𝑟 = 𝑟 − 𝑣;
                    𝑥 = Failed ;
                                                                        𝑣 = Failed ;
                    𝑣 = 𝑣 + 𝑢;
                                                                 }
        }
                                                                 @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                                 while(1 ≥ 0)
        while(1 ≥ 0)
                                                                 {
        {
                                                                        𝑟 = Failed ;
                    𝑦 = 𝑦 − 𝑥;
                                                                        𝑢 = 𝑢 + 2;
                    𝑢 = Failed ;
                                                                 }
        }
                                              }
 }
                                              @post: 1 ≥ 0;
 @post: 1 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                        1:35


    @prog: Fermat2
    @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
    @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
    𝑢 = 2 · 𝑅 + 1;
    𝑣 = 1;
                                                                   @prog: Petter3
    𝑟 = 𝑅2 − 𝑁 ;
                                                                   @real 𝑛, 𝑘, 𝑁 , 𝑠;
    @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
                                                                   @pre: 𝑁 ≥ 0;
    while(𝑟 ≥ 1)
                                                                   𝑠 = 0;
    {
                                                                   𝑛 = 0;
                       if(𝑟 ≥ 0)
                                                                   @invariant: 𝑠 = 0.25 · 𝑛 2 · (𝑛 + 1) 2 ∧ 𝑛 ≤ 𝑁 + 1
                       {
                                                                   while(𝑛 ≤ 𝑁 )
                               𝑟 = 𝑟 − 𝑣;
                                                                   {
                               𝑣 = 𝑣 + 2;
                                                                          𝑠 =𝑠+ ;
                       }
                                                                          𝑛 = 𝑛 + 1;
                       else
                                                                   }
                       {
                                                                   @post: 1 ≥ 0;
                               𝑟 = Failed ;
                               𝑢 = 𝑢 + 2;
                       }
    }
    @post: 1 ≥ 0;




                                           @prog: Petter5
                                           @real 𝑛, 𝑘, 𝑁 , 𝑠;
                                           @pre: 𝑁 ≥ 0;
                                           𝑠 = 0;
                                           𝑛 = 0;
                                           @invariant: 𝑠 = 𝑛 6 ∧ 𝑛 ≤ 𝑁 + 1
                                           while(𝑛 ≤ 𝑁 )
                                           {
                                                  𝑠 = 𝑠 + Failed ;
                                                  𝑛 = 𝑛 + 1;
                                           }
                                           @post: 1 ≥ 0;




                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:36                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


SYNTHESIS RESULTS USING ROSETTE

                       @prog: ClosestCubeRoot
                       @real: 𝑎, 𝑥, 𝑠, 𝑟 ;
                       @pre: 𝑎 ≥ 0;
                       𝑥 = 𝑎;
                       𝑟 = 1;
                       s = 3.25;
                       @invariant: 𝑥 ≥ 0 ∧ −12 · 𝑟 2 + 4 · 𝑠 = 1 ∧ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 + 4 · 𝑥 − 4 · 𝑎 = 1
                       while (𝑥 − 𝑠 ≥ 0)
                       {
                              𝑥 = Timed out ;
                              𝑠 = Timed out ;
                              𝑟 = 𝑟 + 1;
                       }
                       @post: 4 · 𝑟 3 + 6 · 𝑟 2 + 3 · 𝑟 ≥ 4 · 𝑎 ≥ 4 · 𝑟 3 − 6 · 𝑟 2 + 3 · 𝑟 − 1




                                                           @prog: SquareRootFloor
          @prog: ClosestSquareRoot                         @real: 𝑎, 𝑠𝑢, 𝑡, 𝑛;
          @real: 𝑎, 𝑥, 𝑟 ;                                 @pre: 𝑛 ≥ 0;
          @pre: 𝑎 ≥ 1;                                     𝑎 = 0;
          𝑥 = 0.5 · 𝑎;                                     𝑠𝑢 = 1;
          𝑟 = 0;                                           𝑡 = 1;
          @invariant: 𝑎 = 2 · 𝑥 + 𝑟 2 − 𝑟 ∧ 𝑥 ≥ 0          @invariant: 𝑎 2 ≤ 𝑛 ∧ 𝑡 = 2 · 𝑎 + 1 ∧ 𝑠𝑢 = (𝑎 + 1) 2
          while (𝑥 ≥ 𝑟 )                                   while (𝑠𝑢 ≤ 𝑛)
          {                                                {
                   𝑥 = 𝑥 −𝑟 ;                                      𝑎 = 𝑎 + 1;
                   𝑟 = 𝑟 + 1;                                      𝑡 = 2+𝑡 ;
          }                                                        𝑠𝑢 = 𝑠𝑢 + 𝑡 ;
          @post: 𝑟 2 − 𝑟 ≥ 𝑎 − 2 · 𝑟 ∧ 𝑟 2 − 𝑟 ≤ 𝑎         }
                                                           @post((a * a) <= n);


       @prog: SquareRootApproximation
                                                            @prog: ConsecutiveCubes
       @real: 𝑎, 𝑒𝑟𝑟, 𝑟, 𝑞, 𝑝;
                                                            @real: 𝑁 , 𝑛, 𝑥, 𝑦, 𝑧, 𝑠;
       @pre: 𝑎 ≥ 1 ∧ 𝑒𝑟𝑟 ≥ 0;
                                                            @pre: 1 ≥ 0;
       𝑟 = 𝑎 − 1;
                                                            𝑛 = 0;
       𝑞 = 1;
                                                            𝑥 = 0;
       𝑝 = 0.5;
                                                            𝑦 = 1;
       @invariant: 𝑝 ≥ 0 ∧ 𝑟 ≥ 0 ∧ 𝑎 = 𝑞 2 + 2 · 𝑟 · 𝑝
                                                            𝑧 = 6;
       while (2 · 𝑝 · 𝑟 ≥ 𝑒𝑟𝑟 )
                                                            𝑠 = 0;
       {
                                                            @invariant: 𝑧 = 6 · 𝑛 ∧ 𝑦 = 3 · 𝑛 2 + 3 · 𝑛 + 1 ∧ 𝑥 = 𝑛 3
                if (2 · 𝑟 − 2 · 𝑞 − 𝑝 ≥ 0)
                                                            while (𝑛 ≤ 𝑁 )
                {
                                                            {
                         𝑟 = Timed out ;
                                                                   if (𝑥 = 𝑛 3 )
                         𝑞 = 𝑝 + Timed out ;
                                                                   {
                         𝑝 = 𝑝/2;
                                                                              𝑠 = 𝑠 + 𝑥;
                }
                                                                   }
                else
                                                                   𝑛 = 𝑛 + 1;
                {
                                                                   𝑥 = Timed out ;
                         𝑟 = Timed out ;
                                                                   𝑦 = Timed out ;
                         𝑝 = 𝑝 · 0.5;
                                                                   𝑧 = Timed out ;
                }
                                                            }
       }
                                                            @post: 1 ≥ 0;
       @post:𝑞 2 ≥ 𝑎 − 𝑒𝑟𝑟 ∧ 𝑞 2 ≤ 𝑎


Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                             1:37


                                                                             @prog: PolynomialApproximation
                                                                             @real 𝑡, 𝑥, 𝑒, 𝑔1 , 𝑔2 , 𝑛;
                                                                             @macro 𝑓1 = 𝑥 3 ;
                                                                             @macro 𝑓2 = 𝑥 3 + 𝑥;
                                                                             @macro 𝑓3 = 𝑥 3 − 0.5 · 𝑥 2 − 0.5 · 𝑥 + 0.5 ;
                                                                             @pre: 1 ≥ 0;
    @prog: PositivityEnforcement           @prog: SquareCompletion           𝑡 = 0;
    @real: 𝑥, 𝑛;                           @real: 𝑥, 𝑛;                      𝑒 = 5;
    @pre: 𝑥 ≤ 100;                         @pre: 𝑥 ≤ 100;                    if (𝑥 ≤ 𝑡 )
    𝑥 = 𝑛 2 − 5 · 𝑛;                       𝑥 = 𝑛 2 − 5 · 𝑛;                  {
    𝑛 = Timed out ;                        𝑛 = 6.25 ;                                𝑔 1 = 𝑓3 − 𝑓1 ;
    𝑥 = 𝑥 + 𝑛;                             𝑥 = 𝑥 + 𝑛;                                𝑛 = 𝑔1 ;
    @post: 𝑥 ≥ 0;                          @post: 𝑥 ≥ 0;                     }
                                                                             else
                                                                             {
                                                                                     𝑔 2 = 𝑓3 − 𝑓2 ;
                                                                                     𝑛 = 𝑔2 ;
                                                                             }
                                                                             @post: 𝑛 ≤ 𝑒;




                 @prog: SlidingBody
                                                                         @prog: ArchimedesPrinciple
                 @real: 𝑚𝑜𝑣𝑒, 𝑒, 𝑡, 𝑔, 𝑛𝑢𝑠, 𝑛𝑢𝑘, 𝑠𝑖𝑛, 𝑐𝑜𝑠, 𝑙;
                                                                         @real: 𝑓 𝑙, 𝑚, 𝑙, 𝑏, ℎ, 𝜌, 𝑒, 𝑥;
                 @pre: 𝑡 ≥ 0 ∧ 𝑛𝑢𝑠 ≥ 𝑛𝑢𝑘;
                                                                         @pre: 𝑥 ≥ 0 ∧ 𝑚 ≥ 0;
                 𝑔 = 9.8;
                                                                         𝑙 = 10;
                 𝑛𝑢𝑘 = 0.2;
                                                                         𝑏 = 5;
                 𝑛𝑢𝑠 = 0.3;
                                                                         ℎ = 2;
                 𝑠𝑖𝑛 = 0.5;
                                                                         𝜌 = 2;
                 𝑐𝑜𝑠 = 0.86;
                                                                         if ( 𝑚 ≤ 𝜌 · 𝑙 · 𝑏 · ℎ)
                 𝑙 = 10;
                                                                         {
                 if (𝑠𝑖𝑛 ≥ 𝑛𝑢𝑠 · 𝑐𝑜𝑠)
                                                                                 𝑓 𝑙 = 1;
                 {
                                                                                       𝑓𝑙
                          𝑚𝑜𝑣𝑒 = 1;                                               𝑥 = 200 ;
                          𝑡 = Failed ;                                            𝑒 = 𝑚 − 𝜌 · 𝑙 · 𝑏 · ℎ · 𝑥;
                          𝑒 = 𝑡 · 𝑡 · 𝑔 · 𝑠𝑖𝑛 − 𝑔 · 𝑛𝑢𝑘 · 𝑐𝑜𝑠 − 2 · 𝑙;   }
                 }                                                       else
                 else                                                    {
                 {                                                                𝑒 = 0;
                          𝑚𝑜𝑣𝑒 = 0;                                               𝑓 𝑙 = 0;
                          𝑒 = 0;                                                       𝑓𝑙
                                                                                  𝑥 = 200 ;
                          𝑡 = Failed ;
                                                                         }
                 }
                                                                         @post: 𝑒 = 0 ∧ 0 ≤ 𝑥 ≤ 1;
                 @post: 𝑒 = 0 ∧ 𝑡 ≥ 0;




                                 Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:38                      Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


                                                                   @prog: MannadivCarre
                @prog: Cohendiv
                                                                   @real 𝑛, 𝑦, 𝑥, 𝑡 ;
                @real: 𝑥, 𝑦, 𝑞, 𝑟, 𝑑𝑑;
                                                                   @pre: 𝑛 ≥ 0;
                @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 1;
                                                                   𝑦 = 𝑛;
                𝑞 = 0;
                                                                   𝑥 = 0;
                𝑟 = 𝑥;
                                                                   𝑡 = 0;
                @invariant: 𝑥 = 𝑞 · 𝑦 + 𝑟 ∧ 𝑟 ≥ 0
                                                                   @invariant: 𝑥 2 + 2 · 𝑡 + 𝑦 − 𝑛 = 0
                while (𝑟 ≥ 𝑦)
                                                                   while(𝑦 · (𝑦 − 1) ≥ 0)
                {
                                                                   {
                       𝑑 = 1;
                                                                          if(𝑡 = 𝑥)
                       𝑑𝑑 = 𝑦;
                                                                          {
                       @invariant: 𝑑𝑑 = 𝑦 · 𝑑 ∧ 𝑥 = 𝑞 · 𝑦 + 𝑟
                                                                                      𝑦 = 𝑦 −1;
                       ∧𝑟 ≥ 0 ∧ 𝑟 ≥ 𝑦 · 𝑑
                                                                                      𝑡 = 0;
                       while(𝑟 ≥ 2 · 𝑑𝑑)
                                                                                      𝑥 = 𝑥 + 1;
                       {
                                                                          }
                                   𝑑 = 2 · 𝑑;
                                                                          else
                                   𝑑𝑑 = 2 · 𝑑𝑑 ;
                                                                          {
                       }
                                                                                      𝑦 = 𝑦 − 2;
                       𝑟 = 𝑟 − 𝑑𝑑;
                                                                                      𝑡 = 𝑡 + 1;
                       𝑞 = 𝑞 +𝑑 ;
                                                                          }
                }
                                                                   }
                @post: 1 ≥ 0;
                                                                   @post: 1 ≥ 0;




                      @prog: MannadivCube                   @prog: MannadivInd
                      @real 𝑛, 𝑦, 𝑥, 𝑡 ;                    @real 𝑥1, 𝑥2, 𝑦1, 𝑦2, 𝑦3;
                      @pre: 𝑛 ≥ 0;                          @pre: 𝑥1 ≥ 0 ∧ 𝑥2 ≥ 0;
                      𝑦 = 𝑛;                                𝑦1 = 0;
                      𝑥 = 0;                                𝑦2 = 0;
                      𝑡 = 0;                                𝑦3 = 𝑥1;
                      @invariant: 𝑥 3 + 3 · 𝑡 + 𝑦 − 𝑛 = 0   @invariant: 𝑦1 · 𝑥2 + 𝑦2 + 𝑦3 = 𝑥1
                      while(𝑦 ≥ 0)                          while(𝑦3 ≥ 0)
                      {                                     {
                             if(𝑡 = 𝑥 ∗ 𝑥)                          if(𝑦2 + 1 = 𝑥2)
                             {                                      {
                                         𝑦 = Failed ;                        𝑦1 = 𝑦1 + 1;
                                         𝑡 = 0;                              𝑦2 = 0 ;
                                         𝑥 = 𝑥 + 1;                          𝑦3 = 𝑦3 − 1;
                             }                                      }
                             else                                   else
                             {                                      {
                                         𝑦 = 𝑦 − 3;                          𝑦2 = 𝑦2 + 1 ;
                                         𝑡 = 𝑡 + 1;                          𝑦3 = 𝑦3 − 1;
                             }                                      }
                      }                                     }
                      @post: 1 ≥ 0;                         @post: 1 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
Synthesis of Polynomial Programs                                                                                    1:39


                                                       @prog: Euclidex2
            @prog: Wensley
                                                       @real 𝑎, 𝑏, 𝑝, 𝑞, 𝑟, 𝑠, 𝑥, 𝑦;
            @real: 𝑃, 𝑄, 𝐸, 𝑎, 𝑏, 𝑑, 𝑦;
                                                       @pre: 𝑥 ≥ 0 ∧ 𝑦 ≥ 0;
            @pre: 𝑄 ≥ 𝑃 ∧ 𝑃 ≥ 0 ∧ 𝐸 ≥ 0;
                                                       𝑎 = 𝑥;
            𝑎 = 0;
                                                       𝑏 = 𝑦;
            𝑏 = 𝑄/2;
                                                       𝑝 = 1;
            𝑑 = 1;
                                                       𝑞 = 0;
            𝑦 = 0;
                                                       𝑟 = 0;
            @invariant: 𝑎 = 𝑄 · 𝑦 ∧ 𝑏 = 𝑄 · 𝑑/2
                                                       𝑠 = 1;
            ∧𝑃 − 𝑑 · 𝑄 ≤ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≤ 𝑃 ∧ 𝑄 ≥ 0
                                                       @invariant: 𝑎 = 𝑦 · 𝑟 + 𝑥 · 𝑝 ∧ 𝑏 = 𝑥 · 𝑞 + 𝑦 · 𝑠
            while (𝑑 ≥ 𝐸)
                                                       while(1 ≥ 0)
            {
                                                       {
                     if(𝑃 ≤ 𝑎 + 𝑏)
                                                              if(𝑎 ≥ 𝑏)
                     {
                                                              {
                             𝑏 = Failed ;
                                                                          𝑎 = 𝑎 −𝑏 ;
                             𝑑 = 𝑑/2;
                                                                          𝑝 = 𝑝 −𝑞;
                     }
                                                                          𝑟 = 𝑟 − 𝑠;
                     else
                                                              }
                     {
                                                              else
                             𝑎 = 𝑎 + 𝑏;
                                                              {
                             𝑦 = Failed ;
                                                                          𝑏 = 𝑏 −𝑎;
                             𝑏 = 𝑏/2;
                                                                          𝑞 = 𝑞 − 𝑝;
                             𝑑 = 𝑑/2;
                                                                          𝑠 = 𝑠 −𝑟 ;
                     }
                                                              }
            }
                                                       }
            @post: 𝑃 ≥ 𝑦 · 𝑄 ∧ 𝑦 · 𝑄 ≥ 𝑃 − 𝐸 · 𝑄;
                                                       @post: 1 ≥ 0;




 @prog: LCM1
                                            @prog: Fermat1
 @real 𝑎, 𝑏, 𝑥, 𝑦, 𝑢, 𝑣;
                                            @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
 @pre: 𝑎 ≥ 0 ∧ 𝑏 ≥ 0;
                                            @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
 𝑥 = 𝑎;
                                            𝑢 = 2 · 𝑅 + 1;
 𝑦 = 𝑏;
                                            𝑣 = 1;
 𝑢 = 𝑏;
                                            𝑟 = 𝑅2 − 𝑁 ;
 𝑣 = 0;
                                            @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
 @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                            while(1 ≥ 0)
 while(1 ≥ 0)
                                            {
 {
                                                               @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                               while(1 ≥ 0)
        while(1 ≥ 0)
                                                               {
        {
                                                                      𝑟 = 𝑟 − 𝑣;
                    𝑥 = Failed ;
                                                                      𝑣 = 𝑣 +2;
                    𝑣 = 𝑣 + 𝑢;
                                                               }
        }
                                                               @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
        @invariant: 𝑥 · 𝑢 + 𝑦 · 𝑣 = 𝑎 · 𝑏
                                                               while(1 ≥ 0)
        while(1 ≥ 0)
                                                               {
        {
                                                                      𝑟 = 𝑟 +𝑢 ;
                    𝑦 = 𝑦 − 𝑥;
                                                                      𝑢 = 𝑢 + 2;
                    𝑢 = Failed ;
                                                               }
        }
                                            }
 }
                                            @post: 1 ≥ 0;
 @post: 1 ≥ 0;




                               Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
1:40                          Amir Kafshdar Goharshady, S. Hitarth, Fatemeh Mohammadi, and Harshit Jitendra Motwani


       @prog: Fermat2
       @real 𝑁 , 𝑅, 𝑢, 𝑣, 𝑟 ;
       @pre: 𝑁 ≥ 1 ∧ (𝑅 − 1) 2 ≤ 𝑁 − 1 ∧ 𝑁 ≤ 𝑅 2 ;
       𝑢 = 2 · 𝑅 + 1;
       𝑣 = 1;
                                                                      @prog: Petter3
       𝑟 = 𝑅2 − 𝑁 ;
                                                                      @real 𝑛, 𝑘, 𝑁 , 𝑠;
       @invariant: 𝑁 ≥ 1 ∧ 4 · (𝑁 + 𝑟 ) = 𝑢 2 − 𝑣 2 − 2 · 𝑢 + 2 · 𝑣
                                                                      @pre: 𝑁 ≥ 0;
       while(𝑟 ≥ 1)
                                                                      𝑠 = 0;
       {
                                                                      𝑛 = 0;
                          if(𝑟 ≥ 0)
                                                                      @invariant: 𝑠 = 0.25 · 𝑛 2 · (𝑛 + 1) 2 ∧ 𝑛 ≤ 𝑁 + 1
                          {
                                                                      while(𝑛 ≤ 𝑁 )
                                  𝑟 = 𝑟 − 𝑣;
                                                                      {
                                  𝑣 = 𝑣 + 2;
                                                                             𝑠 = 𝑠 + Failed ;
                          }
                                                                             𝑛 = 𝑛 + 1;
                          else
                                                                      }
                          {
                                                                      @post: 1 ≥ 0;
                                  𝑟 = Failed ;
                                  𝑢 = 𝑢 + 2;
                          }
       }
       @post: 1 ≥ 0;




                                              @prog: Petter5
                                              @real 𝑛, 𝑘, 𝑁 , 𝑠;
                                              @pre: 𝑁 ≥ 0;
                                              𝑠 = 0;
                                              𝑛 = 0;
                                              @invariant: 𝑠 = 𝑛 6 ∧ 𝑛 ≤ 𝑁 + 1
                                              while(𝑛 ≤ 𝑁 )
                                              {
                                                     𝑠 = 𝑠 + Failed ;
                                                     𝑛 = 𝑛 + 1;
                                              }
                                              @post: 1 ≥ 0;




Proc. ACM Program. Lang., Vol. 1, No. CONF, Article 1. Publication date: January 2018.
