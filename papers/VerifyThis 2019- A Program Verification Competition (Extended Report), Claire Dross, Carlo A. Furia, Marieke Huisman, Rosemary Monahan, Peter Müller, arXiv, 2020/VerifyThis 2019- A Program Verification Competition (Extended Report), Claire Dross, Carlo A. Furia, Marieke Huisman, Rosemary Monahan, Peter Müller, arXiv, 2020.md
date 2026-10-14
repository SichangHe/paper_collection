                                         Noname manuscript No.
                                         (will be inserted by the editor)




                                         VerifyThis 2019: A Program Verification Competition
                                         Extended Report

                                         Claire Dross · Carlo A. Furia
                                         Marieke Huisman · Rosemary Monahan · Peter Müller
arXiv:2008.13610v3 [cs.LO] 18 May 2021




                                         Received: date / Accepted: date


                                         Abstract VerifyThis is a series of program verification com-      1 The VerifyThis 2019 Verification Competition
                                         petitions that emphasize the human aspect: participants
                                         tackle the verification of detailed behavioral properties—        VerifyThis is a series of program verification competitions
                                         something that lies beyond the capabilities of fully auto-        where participants prove expressive input/output properties
                                         matic verification, and requires instead human expertise to       of small programs with complex behavior. This report de-
                                         suitably encode programs, specifications, and invariants. This    scribes VerifyThis 2019, which took place on 6–7 April 2019
                                         paper describes the 8th edition of VerifyThis, which took         in Prague, Czech Republic, as a two-day event of the Euro-
                                         place at ETAPS 2019 in Prague. Thirteen teams entered the         pean Joint Conferences on Theory and Practice of Software
                                         competition, which consisted of three verification challenges     (ETAPS 2019). It was the eighth event in the series, after the
                                         and spanned two days of work. This report analyzes how            VerifyThis competitions held at FoVeOOS 2011, FM 2012,
                                         the participating teams fared on these challenges, reflects on    the Dagstuhl Seminar 14171 (in 2014), and ETAPS 2015–
                                         what makes a verification challenge more or less suitable for     2018. The organizers of VerifyThis 2019 were also the au-
                                         the typical VerifyThis participants, and outlines the difficul-   thors of this paper—henceforth referred to as “we”.
                                         ties of comparing the work of teams using wildly different            VerifyThis aims to bring together researchers and practi-
                                         verification approaches in a competition focused on the hu-       tioners interested in formal verification, providing them with
                                         man aspect.                                                       an opportunity for engaging, hands-on, and fun discussion.
                                                                                                           The results of the competition help the research community
                                         Keywords functional correctness · correctness proofs ·            evaluate progress and assess the usability of formal verifi-
                                         program verification · verification competition                   cation tools in a controlled environment—which still repre-
                                                                                                           sents, on a smaller scale, important practical aspects of the
                                                                                                           verification process.
                                                                                                               Unlike other verification competitions that belong to the
                                         Claire Dross                                                      same TOOLympics (Competitions in Formal Methods) track
                                         AdaCore, France                                                   of ETAPS, VerifyThis emphasizes verification problems that
                                         E-mail: dross@adacore.com
                                                                                                           go beyond what can be proved fully automatically, and re-
                                         Carlo A. Furia                                                    quire instead human experts “in the loop”. During a Ver-
                                         USI Università della Svizzera italiana, Switzerland
                                         E-mail: furiac@usi.ch
                                                                                                           ifyThis event, participating teams are given a number of
                                                                                                           verification challenges that they have to solve on-site dur-
                                         Marieke Huisman
                                         University of Twente, the Netherlands
                                                                                                           ing the time they have available using their favorite veri-
                                         E-mail: m.huisman@utwente.nl                                      fication tools. A challenge is typically given as a natural-
                                         Rosemary Monahan
                                                                                                           language description—possibly complemented with some
                                         Maynooth University, Ireland                                      pseudo-code or lightweight formalization—of an algorithm
                                         E-mail: Rosemary.Monahan@mu.ie                                    and its specification. Participants have to implement the al-
                                         Peter Müller                                                      gorithm in the input language of their tool of choice, for-
                                         ETH Zurich, Switzerland                                           malize the specification, and formally prove the correctness
                                         E-mail: Peter.Mueller@inf.ethz.ch                                 of the implementation against the specification. The chal-
lenge descriptions leave a lot of details open, so that partic-     for three problems; and one more problem proposal arrived
ipants can come up with the formalization that best fits the        later, close to the competition date.
capabilities of their verification tool of choice. Correctness           We combined these proposals with other ideas in order
proofs usually require participants to supply additional in-        to design three challenges suitable for the competition. Fol-
formation, such as invariants or interactive proof commands.        lowing our experience, and the suggestions of organizers
    Following a format that consolidated over the years, Ver-       of previous VerifyThis events, we looked for problems that
ifyThis 2019 proposed three verification challenges. During         were suitable for a 90-minute slot, and that were not too bi-
the first day of the competition, participants worked during        ased towards a certain kind of verification language or tool.
three 90-minute slots—one for each challenge. Judging of            A good challenge problem should be presented as a series of
the submitted solutions took place during the second day            specification and verification steps of increasing difficulty;
of the competition, when we assessed the level of correct-          even inexperienced participants should be able to approach
ness, completeness, and elegance of the submitted solutions.        the first steps, whereas the last steps are reserved for those
Based on this assessment, we awarded prizes to the best             with advanced experience in the problem’s domain, or that
teams in different categories (such as overall best team, and       find it particularly congenial to the tools they’re using. Typ-
best student teams) The awards were announced during the            ically, the first challenge involves an algorithm that operates
ETAPS lunch on Monday, 8 April 2019.                                on arrays or even simpler data types; the second challenge
                                                                    targets more complex data structures in the heap (such as
Outline. The rest of this report describes VerifyThis 2019 in       trees or linked lists); and the third challenge involves con-
detail, and discusses the lessons we learned about the state of     currency.
the art in verification technology. Section 1.1 outlines how             In the end, we used one suggestion collected through the
we prepared the challenges; Section 1.2 discusses the in-           “Call for Problems” as the basis of the first challenge, which
vited tutorial that opened VerifyThis; Section 1.3 presents         involves algorithms on arrays (see Section 2). Another prob-
the teams that took part in this year’s VerifyThis; and Section 1.4 lem suggestion was the basis of the second challenge, which
describes the judging process in some more detail.                  targets the construction of binary trees from a sequence of
    Then, Sections 2–4 each describe a verification chal-           integers (see Section 3). For the third challenge, we took a
lenge in detail: the content of the challenge, what aspects we      variant of the matrix multiplication problem (which was al-
weighed when designing it, how the teams fared on it, and a         ready used, in a different form, during VerifyThis 2016) that
postmortem assessment of what aspects made the challenge            lends itself to a parallel implementation (see Section 4).
easy or hard for teams.
    Finally, Section 5 presents the lessons learned from or-
ganizing this and previous competitions, focusing on the            1.2 Invited Tutorial
tools and tool features that emerged, on the characteristics
of the challenges that made them more or less difficult for         We invited Virgile Prevosto to open VerifyThis 2019 with a
participants, and on suggestions for further improvements           tutorial about Frama-C. Developed by teams at CEA LIST
to the competition format.                                          and INRIA Saclay in France, Frama-C1 is an extensible plat-
    The online archive of VerifyThis                                form for source-code analysis of software written in C.
                                                                         Frama-C works on C code annotated with specifications
                http://verifythis.ethz.ch
                                                                    and other directives for verification written as comments
includes the text of all verification challenges, and the so-       in the ACSL (pronounced “axel”) language. Each plug-in
lutions submitted by the teams (typically revised and im-           in Frama-C provides a different kind of analysis, including
proved after the competition). Reports about previous edi-          classic dataflow analyses, slicing, and also dynamic anal-
tions of VerifyThis are also available [6,12,3,15,18,19,17].        yses. The tutorial2 focused on the WP (Weakest Precon-
The motivation and initial experiences of organizing verifi-        dition) plugin, which supports deductive verification using
cation competitions in the style of VerifyThis are discussed        SMT solvers or interactive provers to discharge verification
elsewhere [22,16]; a recent publication [10] draws lessons          conditions.
from the history of VerifyThis competitions.                             The tutorial began with the simple example of a func-
                                                                    tion that swaps two pointers. Despite the simplicity of the
                                                                    implementation, a complete correctness proof is not entirely
1.1 Challenges
                                                                    trivial since it involves proving the absence of undefined
                                                                    behavior—a characteristic of C’s memory model. The tuto-
A few months before the competition, we sent out a public
                                                                    rial continued with examples of increasing complexity demon-
“Call for Problems” asking for suggestions of verification
challenges that could be used during the competition. Two             1 https://frama-c.com

people submitted by the recommended deadline proposals                2 https://frama.link/fc-tuto-2019-04




                                                                  2
strating other features of the WP plugin and of the ACSL an-          on the aspects that the participants found the most relevant
notation language, such as how to specify frame conditions            while still having basic information about all teams.
and memory separation, how to reason about termination,
                                                                          At the same time as judging was going on, participants
and how to define and use custom predicates for specifica-
                                                                      not being interviewed were giving short presentations of their
tion.                                                                 solutions to the other teams. This is another time-honored
    Frama-C has been used to analyze critical low-level code,         tradition of VerifyThis, which contributes more value to the
such as the Contiki embedded operating system and imple-
                                                                      event and makes it an effective forum to exchange ideas
mentations of critical communications protocols. Its focus
                                                                      about how to do verification in practice. We briefly consid-
and the rich palette of analyses it supports make it a tool           ered the option of merging interviews (with organizers) and
with an original approach to formal verification—one that             presentation (to other participants), but in the end we de-
VerifyThis participants found interesting and stimulating to          cided that having separate sessions makes judging more ef-
compare to the capabilities of their own tools.
                                                                      fective and lets participants discuss freely with others with-
                                                                      out the pressure of the competition—although the atmosphere
                                                                      was generally quite relaxed!
1.3 Participants
                                                                          Once the interviews were over, we discussed privately
Table 1 lists the thirteen teams that participated in Verify-         to choose the awardees. We structured our discussion around
This 2019. Four teams consisted of a single person, whereas           the      questionnaires’     information,     and    supple-
the majority of teams included two persons (the maximum               mented it with the notes taken during the interviews. Never-
allowed).                                                             theless, we did not use any fixed quantitative scoring, since
    As it is often the case during verification competitions,         VerifyThis’s judging requires us to compare very different
the majority of participants used a tool they know very well          approaches and solutions to the same problems. Even crite-
because they have contributed to its development. However,            ria that are objectively defined in principle may not be di-
four teams identified themselves as non-developers, as they           rectly comparable between teams; for example, correctness
did not directly contribute to the development of the verifi-         is relative to a specification, and hence, different ways of
cation tools they used during the competition.                        formalizing a specification drastically change the hardness
    Out of 21 participants, 11 were graduate students. Some           of establishing correctness. We tried to keep an open mind
participated with a senior colleague, while some others               towards solutions that pursued an approach very different
worked alone or with other students, making up a total of             from the one we had in mind when writing the challenges,
three all-student teams.                                              provided the final outcome was convincing. Still, inevitably,
                                                                      our background, knowledge, and expectations somewhat may
                                                                      have biased the judging process. In the end, we were pleased
1.4 Judging                                                           by all submissions, which showed a high level of effort, and
                                                                      results that were often impressive—especially considering
Judging took place on the competition’s second day. Each              the limited available time to prepare a solution.
team sat for a 20–30-minute interview with us, during which
they went through their solutions, pointing out what they did             We awarded six prizes in four categories:
and didn’t manage to verify, and which aspects they found
the most challenging.
                                                                       – Best Overall Team went to Team The Refiners
    Following the suggestions of previous organizers [10],
                                                                       – Best Student Teams went to Team Mergesort and
we asked teams to fill in a questionnaire about their sub-
                                                                         Team Sophie & Wytse
mitted solutions in preparation for the interview. The ques-
                                                                       – Most Distinguished Tool Feature went to Team Bashers —
tionnaire asked them to explain the most important features
                                                                         for a library to model concurrency in Isabelle, which
of the implementation, specification, and verification in their
                                                                         they developed specifically in preparation for the compe-
solutions, such as whether the implementation diverged from
                                                                         tition—and to Team VerCors T(w/o)o —for their usage
the pseudo-code given in the challenge description, whether
                                                                         of ghost method parameters to model sparse matrices
the specification included properties such as memory safety,
                                                                       – Tool Used by Most Teams went to Viper—used directly
and whether verification relied on any simplifying assump-
                                                                         or indirectly3 by three different teams—represented by
tions. The questionnaire also asked participants to reflect
                                                                         Alexander J. Summers.
on the process they followed (How much human effort was
involved? How long would it take to complete your solu-
tion?), and on the strengths and weaknesses of the tools they           3 VerCors uses Viper as back-end; hence, Team Viper used it di-
used. With the bulk of the information needed for judging             rectly, and Team VerCors T(w/o)o and Team Sophie & Wytse used it
available in the questionnaire, we could focus the interviews         indirectly.


                                                                  3
                              TEAM NAME                               MEMBERS                                   TOOL

                     1    Mergesort               Quentin Garchery                                      Why3            [13, 5]
                     2    VerCors T(w/o)o         Marieke Huisman, Sebastiaan Joosten                   VerCors          [4, 1]
                     3    Bashers                 Mohammad Abdulaziz, Maximilian P L Haslbeck           Isabelle          [26]
                     4    Jourdan-Mével           Jacques-Henri Jourdan, Glen Mével                     Coq             [2, 20]
                     5    OpenJML                 David Cok                                             OpenJML             [8]
                     6    YVeTTe                  Virgile Prevosto, Virgile Robles                      Frama-C           [21]
                     7    The Refiners            Peter Lammich, Simon Wimmer                           Isabelle       [26, 23]
                     8    KIV                     Stefan Bodenmüller, Gerhard Schellhorn                KIV               [11]
                     9    Sophie & Wytse          Sophie Lathouwers, Wytse Oortwijn                     VerCors             [4]
                    10    Coinductive Sorcery     Jasper Hugunin                                        Coq                 [2]
                    11    Heja mig                Christian Lidström                                    Frama-C           [21]
                    12    Eindhoven UoT           Jan Friso Groote, Thomas Neele                        mCRL2            [9, 7]
                    13    Viper                   Alexander J. Summers                                  Viper             [25]
Table 1 Teams participating in VerifyThis 2019, listed in order of registration. For each TEAM the table reports its NAME, its MEMBERS, and the
verification TOOL they used. A member names is in italic if the member is a student; and it is underlined if the member is also a developer of the
tool or of some extension used in the competition.



2 Challenge 1: Monotonic Segments and GHC Sort                                cut := [0] # singleton sequence with element 0
                                                                              x, y := 0, 1
The first challenge was based on the generic sorting algo-                    while y < n:   # n is the length of sequence s
rithm used in Haskell’s GHC compiler.4 The algorithm is a                        increasing := s[x] < s[y] # in increasing segment?
                                                                                 while y < n and (s[y-1] < s[y]) == increasing:
form of patience sorting.5                                                          y := y + 1
                                                                                 cut.extend(y) # extend cut by adding y to its end
                                                                                 x := y
2.1 Challenge Description                                                        y := x + 1
                                                                              if x < n:
Challenge 1 was in two parts—described in Section 2.1.1                          cut.extend(n)

and Section 2.1.2—each consisting of several different ver-
                                                                            Fig. 1 Algorithm to compute the maximal cutpoints cut of sequence s.
ification tasks. We did not expect participants to solve both
parts in the 90 minutes at their disposal, but suggested that
they pick the one that they found the most feasible given the                  Formally, given a sequence s as above, we call mono-
tool they were using and their preferences.                                 tonic cutpoints any integer sequence

2.1.1 Part A: Monotonic Segments                                            cut    =     c0 c1 . . . cm−1

Given a sequence s                                                          such that the following four properties hold:
s    =     s[0] s[1] . . . s[n − 1]      n≥0                                non-empty:     m>0
of elements over a totally sorted domain (for example, the                  begin-to-end: c0 = 0 and cm−1 = n
integers), we call monotonic cutpoints any indexes that cut                 within bounds: for every element ck ∈ cut: 0 ≤ ck ≤ n
s into segments that are monotonic: each segment’s elements                 monotonic:     for every pair of consecutive elements
are all increasing or all decreasing.6 Here are some examples                              ck , ck+1 ∈ cut, the segment s[ck ..ck+1 ) =
of sequences with monotonic cutpoints:                                                     s[ck ] s[ck + 1] . . . s[ck+1 − 1] of s, which
     SEQUENCE s    MONOTONIC CUTPOINTS      MONOTONIC SEGMENTS
                                                                                           starts at index ck included and ends at index
     123457                         06           123457
                                                                                           ck+1 excluded, is monotonic, that is: either
    1473359                       0357         147 | 33 | 59                               s[ck ] < s[ck + 1] < · · · < s[ck+1 − 1] or
    6342537                      02467         63 | 42 | 53 | 7
                                                                                           s[ck ] ≥ s[ck + 1] ≥ · · · ≥ s[ck+1 − 1]
In this challenge we focus on maximal monotonic cutpoints,
that is such that, if we extend any segment by one element,                 Given a sequence s, for example stored in an array, max-
the extended segment is not monotonic anymore.                          imal monotonic cutpoints can be computed by scanning s
                                                                        once while storing every index that corresponds to a change
  4 https://hackage.haskell.org/package/base-4.12.0.0/docs/src/Data.OldList.html#sort
  5 Named
                                                                        in monotonicity (from increasing to decreasing, or vice versa),
                 after        the       patience       card       game
https://en.wikipedia.org/wiki/Patience_sorting .
                                                                        as shown by the algorithm in Figure 1.
  6 More precisely, all strictly increasing, or nonincreasing (decreas-     To solve Challenge 1.A, we asked participants to carry
ing or equal).                                                          out the following tasks.

                                                                        4
     # merge ordered segments s and t                                    Implementation task: Implement GHC Sort in your pro-
     merged := []                                                           gramming language of choice.
     x, y := 0, 0                                                        Verification tasks:
     while x < length(s) and y < length(t):
                                                                             1. Write functional specifications of all procedures/func-
       if s[x] < t[y]:
         merged.extend(s[x])                                                    tions/main steps of your implementation.
         x := x + 1                                                          2. Verify that the implementation of merge returns a se-
       else:                                                                    quence merged that is sorted.
         merged.extend(t[y])
                                                                             3. Verify that the overall sorting algorithm returns an
         y := y + 1
     # append any remaining tail of s or t                                      output that is sorted.
     while x < length(s):                                                    4. Verify that the overall sorting algorithm returns an
       merged.extend(s[x])                                                      output that is a permutation of the input.
       x := x + 1
     while y < length(t):
       merged.extend(t[y])
       y := y + 1                                                        2.2 Designing the Challenge

                                                                 The starting point for designing this challenge was Nadia
Fig. 2 Algorithm to merge sorted sequences s and t into sorted se-
quence merged .                                                  Polikarpova’s suggestion to target GHC’s generic sorting
                                                                 method. Responding to VerifyThis’s Call for Problems, she
Implementation task: Implement the algorithm in Figure 1         submitted a concise high-level description of how the sort-
    to compute monotonic cutpoints of an input sequence.         ing algorithm works, and pointed us to an implementation in
Verification tasks:                                              Liquid Haskell7 that verifies sortedness of the output.
     1. Verify that the output sequence satisfies properties          In order to understand whether this algorithm could be
        non-empty, begin-to-end, and within bounds above.        turned  into a suitable verification challenge, we developed a
     2. Verify that the output sequence satisfies property mono- prototype   implementation of GHC Sort written in Python,
        tonic given above (without the maximality require-       complete with assertions of key correctness properties as
        ment).                                                   well as tests that exercised the implementation on different
     3. Strengthen the definition of monotonic cutpoints so      inputs. Tweaking this implementation was useful to quickly
        that it requires maximal monotonic cutpoints, and        explore different variants of the algorithm and their reper-
        prove that your algorithm implementation computes        cussions on correct program behavior.
        maximal cutpoints according to the strengthened def-          We also developed a verified Dafny implementation of
        inition.                                                 parts  of the algorithm, in order to get an idea of the kinds
                                                                 of invariants that are required for proving correctness and to
2.1.2 Part B: GHC Sort                                           anticipate possible pitfalls when trying to specify or verify
                                                                 the algorithm.
To sort a sequence s, GHC Sort works as follows:                      These attempts indicated that verifying the whole GHC
                                                                 Sort algorithm would have been a task too demanding for
 1. Split s into monotonic segments σ1 , σ2 , . . . , σm−1
                                                                 a 90-minute slot. Therefore, we split it into two conceptu-
 2. Reverse every segment that is decreasing
                                                                 ally separate parts: A) finding the monotonic segments of
 3. Merge the segments pairwise in a way that preserves the
                                                                 the input (Section 2.1.1); and B) the actual sorting procedure
    order
                                                                 (Section 2.1.2). We suggested to participants to focus their
 4. If all segments have been merged into one, that is an or-
                                                                 work on the parts of the algorithm that were more amenable
    dered copy of s; then terminate. Otherwise, go to step 3
                                                                 to analysis according to the capabilities of their verification
Merging in step 3 works like merging in Merge Sort, which        tool, while specifying the expected behavior of the other
follows the algorithm in Figure 2.                               parts without proving their correctness explicitly. In particu-
    For example, GHC Sort applied to the sequence s =            lar, to decouple the different parts of the challenge and give
3 2 8 9 3 4 5 goes through the following steps:                  more flexibility, we left participants working on part B free
 – monotonic segments: 3 2 | 8 9 | 3 4 5                         to add the reversal (step 2 of GHC Sort) to the same pass
 – reverse decreasing segments: 2 3 | 8 9 | 3 4 5                that constructs the monotonic segments in step 1.
 – merge segments pairwise: 2 3 8 9 | 3 4 5                           GHC Sort’s original implementation is in Haskell—a
 – merge segments pairwise again: 2 3 3 4 5 8 9, which is s      pure functional programming language, which offers abstract
    sorted                                                       lists as a native data type—bringing the risk of a verifica-
                                                                 tion challenge biased in favor of tools based on functional
    To solve Challenge 1.B, we asked participants to carry
out the following tasks.                                           7 https://github.com/ucsd-progsys/liquidhaskell/blob/develop/tests/pos/




                                                                     5
programming features. To mitigate this risk, we explicitly             Detailed Results
told participants they were free to choose any representa-
tion of input sequences and cutpoints sequences that was               The two teams using Isabelle followed very different ap-
manageable using their programming language of choice:                 proaches to representing cutpoints in challenge 1. While
arrays, mathematical sequences, dynamic lists, . . . . We also         Team The Refiners used functional lists of lists to repre-
presented the key algorithms (Figure 1 and Figure 2) using             sent monotonic segments explicitly, Team Bashers chose
iteration, but still left participants free to use recursion in-       to use an explicit representation of indexes corresponding
stead of looping to implement the general idea behind the              to cutpoints—which turned out not to be a good match for
algorithms.                                                            Isabelle’s functional programming features. Team The Re-
     One technical issue we discussed while preparing the              finers expressed challenge 1’s correctness properties recur-
challenge was the definition of monotonicity of a segment.             sively to be amenable to inductive proofs. With these adjust-
Definition monotonic on page 4 above is asymmetric since               ments, they could take full advantage of Isabelle’s verifica-
it distinguishes between strictly increasing and nonstrictly           tion capabilities: they specified all properties of part A and
decreasing (that is, nonincreasing) segments. While using              performed all verification tasks with the exception of com-
a symmetric definition—which would allow repeated equal                pleting the proof of maximality; and they even managed to
values to appear indifferently in increasing or decreasing             solve most of part B’s specification and verification tasks,
segments—seemed more elegant and perhaps more natural,                 completing all its proofs not long after the competition slot
the asymmetric definition (2.1.1) seemed simpler to imple-             was over.
ment, since it is enough to compare the first two elements of               Both teams using the Coq theorem prover encoded chal-
a segment to know whether the rest of the segment has to be            lenge 1-A in a purely functional setting, using lists and re-
increasing (strictly) or decreasing (nonstrictly). In turn, def-       cursion. Without the support of domain-specific libraries,
inition (2.1.1) seemed to require slightly simpler invariants          reasoning about the properties required by the challenge turn-
because the predicate for “decreasing” would be exactly the            ed out to be quite cumbersome and time-consuming. In par-
complement of the predicate for “increasing”. At the same              ticular, Coq’s constructive logic requires that every recursive
time, we were wary of how people used to different nota-               function definition be accompanied by a proof of termina-
tions and verification styles might still find the symmetric           tion (showing that recursion is well founded). This slowed
definition easier to work with. Therefore, we left participants        down the work of Team Jourdan-Mével and Team Coinduc-
free to change the definition of monotonic so that segments            tive Sorcery , who could submit only partial solutions in time
of equal values could be indifferently included in increasing          for the competition.
or in decreasing segments. If they choose to do so, we also                 Challenge 1—in particular, part A—was well-suited, in
pointed out that they may have had to change the algorithm             its original form using arrays, with OpenJML’s capabilities:
in Figure 1 to match their definition of monotonic segment.            Team OpenJML delivered an implementation of the algo-
     One final aspect that we tried to anticipate was the re-          rithms that was very close to the pseudo-code of Figure 1,
quirement of maximality of the monotonic segments. Prov-               and could express and prove properties that directly trans-
ing maximality seemed somewhat more complex than prov-                 lated all of the challenge’s verification tasks. As usual for
ing monotonicity alone; hence, we marked it as “optional               verifiers based on SMT solvers, a successful proofs depends
task (advanced)” and we did not provide any formal defini-             on being able to write specifications in a form amenable to
tion of maximality—so that participants were free to come              automated reasoning. Then, the required loop invariants had
up with the formal specification that best fitted their general        a fairly clear connection to the postconditions that had to be
solution.                                                              proved. To save time, Team OpenJML took some shortcuts
                                                                       in the implementation (for example, writing the result into
2.3 Submitted Solutions                                                a global variable instead of returning it explicitly) that do
                                                                       not affect its behavior but are somewhat inelegant; cleaning
Overall Results                                                        them up, however, should be straightforward.
                                                                            Both teams using VerCors progressed quite far in solv-
Team OpenJML and Team The Refiners submitted solutions                 ing part A of challenge 1, but could not complete the proof of
of challenge 1 that were complete and correct. Another team            maximality during the competition. Team Sophie & Wytse
got close but missed a few crucial invariants. Five teams              modified the implementation of the algorithm to compute
made substantial progress but introduced some simplifying              the cutpoints so that it stores in a separate array the mono-
assumptions or skipped verification of maximality. And an-             tonicity direction of each segment (that is whether each seg-
other five teams’ progress was more limited, often due to              ment is increasing or decreasing); this helped to simplify
a mismatch between their tools’ capabilities and what was              reasoning about maximality, since one can more easily re-
required by the challenge.                                             fer to the monotonicity of each segment independent of the

                                                                   6
others. Even without this trick, Team VerCors T(w/o)o pro-            could be analyzed. In practice, most of their analysis used
gressed further in the proof of maximality, as they only missed       lists of up to 4 elements (lists of up to 10 elements is close
a few key invariants. Both teams using VerCors used im-               to the maximum the tool can handle before the analysis al-
mutable sequences, instead of arrays, to store cutpoint se-           gorithm exhausts the available resources); and they did not
quences; this dispensed them with having to deal with per-            prove maximality (possibly because expressing the property
missions—extensively used for arrays by VerCors.                      in operational form would have been tedious).
     Team KIV also used immutable sequences as primary
data structure for challenge 1-A; KIV’s libraries recently in-
cluded a proof that sequences and arrays can simulate each            2.4 Postmortem Evaluation of the Challenge
other, and hence, it should be possible to rework the formal-
                                                                      Teams did not find the definition (2.1.1)of monotonicity hard
ization to work with arrays with limited changes. As it is
                                                                      to work with because it is asymmetric: as far as we could
customary in KIV, and in contrast to what most other ap-
                                                                      see, most of them encoded the property as we suggested and
proaches prefer to do, Team KIV expressed all correctness
                                                                      made it work effectively.
properties together using a single descriptive predicate. Ac-
                                                                          However, a couple of teams were confused by mistak-
cording to Team KIV ’s members, this helps scalability with
                                                                      enly assuming a property of monotonic segments: since the
their tool, but may hamper a partial yet faster progress when
                                                                      condition for “decreasing” is the complement of the condi-
limited time is available—as it was the case during the com-
                                                                      tion for “increasing”, they concluded that increasing and de-
petition, when they could not complete the proofs in time.
                                                                      creasing segments must strictly alternate (after a decreasing
     Team Viper implemented challenge 1-A’s algorithm us-
                                                                      segment comes an increasing one, and vice versa). This is
ing arrays; more precisely, they introduced a domain defi-
                                                                      not true in general, as shown by the example of sequence
nition that represents arrays as objects with certain proper-
                                                                      6 3 4 2 5 3 7, which is made of 4 monotonic segments
ties. Team Viper modified the algorithm in Figure 1 trying
                                                                      6 3 | 4 2 | 5 3 | 7, all of them decreasing.
to enforce the property that increasing and decreasing seg-
                                                                          While we did not give a formal definition of maximality,
ments strictly alternate—a property that the original algo-
                                                                      the teams that managed to deal with this advanced property
rithm does not possess. This turned out to be tricky to do
                                                                      did not have trouble formalizing it. Since “extending” a seg-
and complicated several aspects of the specification. In the
                                                                      ment can be generally done both on its right and on its left
end, Team Viper submitted a solution that included several
                                                                      endpoint, teams typically expressed maximality as two sep-
parts of the specification and invariants necessary to prove
                                                                      arate properties: to the right and to the left. While it may be
correctness but did not completely establish monotonicity
                                                                      possible to prove that one follows from the other (and the
and maximality.
                                                                      definition of monotonic cutpoints), explicitly dealing with
     Team YVeTTe solved challenge 1-A using Frama-C’s                 both variants was found to be preferable in practice since the
WP plugin, which provides automated deductive verification            invariants to prove one variant are clearly similar to those to
of C code using SMT solvers. Since Frama-C encodes low-               prove the other.
level aspects of the C memory model, correctness proofs of-
ten generate a large number of proof obligations that require
to establish safety and separation of different memory re-            3 Challenge 2: Cartesian Trees
gions. These low-level proof obligations may significantly
complicate the proof of higher-level functional properties—           The second challenge involved the notion of Cartesian trees8
such as those that are the main focus of VerifyThis’s chal-           of a sequence of integers and, in particular, dwelt on how
lenges. More practically, this interplay of user-defined pred-        such trees can be constructed in linear time from the se-
icates and low-level properties made Frama-C’s WP plugin              quence of all nearest smaller values9 of the input sequence.
generate proof obligations that were not automatically prov-
able by SMT solvers and would have required a lengthy
manual analysis using an interactive prover like Coq. Due             3.1 Challenge Description
to these hurdles, Team YVeTTe managed to get close to a
proof of monotonicity, but could not complete some invari-            This challenge was in two parts. The first part, presented in
ants and lemmas in time during the competition.                       Section 3.1.1, asked to compute the sequence of all nearest
                                                                      smaller values of an input sequence, while the second, in
     The only team using a model checker, Team Eindhoven
                                                                      Section 3.1.2, dealt with the construction of the sequence’s
UoT had to introduce restrictions and simplification to ex-
                                                                      actual Cartesian tree. We did not expect participants to com-
press the requirements of challenge 1-A within the finite-
                                                                      plete the whole challenge in an hour and a half; so they could
state expressiveness of their verification tool. In their so-
lution, the integers that make up a sequence range over a              8 https://en.wikipedia.org/wiki/Cartesian_tree

finite bound; and only input lists of a certain fixed length           9 hhttps://en.wikipedia.org/wiki/All_nearest_smaller_values




                                                                  7
 stack := [] # empty stack                                                          4      7      8      1      2      3      9      5   6
 for every index x in s:
     # pop values greater or equal to s[x]
     while not stack.is_empty                                                                            1
           and s[stack.top] >= s[x]:
                                                                                                                2
         stack.pop
                                                                                                                       3
      if stack.is_empty:
          # x doesn’t have a left neighbor                                          4
          left[x] := 0
      else:                                                                                                                          5
          left[x] := stack.top
                                                                                                                                         6
      stack.push (x)
                                                                                           7
Fig. 3 Algorithm to compute the sequence left of all left nearest                                 8
smaller values of input sequence s. The algorithm assumes that in-
dexes start from 1, and hence, it uses 0 to denote that an index has no                                                       9
left neighbor.
                                                                              Fig. 4 Cartesian tree of sequence 4 7 8 1 2 3 9 5 6.

choose the part that best fitted their language of choice. The
second part of the challenge used features described in the                   of s (value 1) is also 0, since 1 is the smallest value of the
first part, but participants did not need to actually implement               list.
and verify the algorithms of the first part to carry out the sec-                   To solve Challenge 2.A, we asked participants to carry
ond.                                                                          out the following tasks:

                                                                              Implementation task. Implement the algorithm to compute
3.1.1 Part A: All Nearest Smaller Values                                         the sequence of left neighbors from an input sequence.
                                                                              Verification tasks.
For each index in a sequence of values, we define the nearest                     1. Index: verify that, for each index i in the input se-
smaller value to the left, or left neighbor, as the last index                       quence s, the left neighbor of i in s is smaller than i,
among the previous indexes that contains a smaller value.                            that is left[i] < i.
More precisely, for each index x in an input sequence s, the                      2. Value: verify that, for each index i in the input se-
left neighbor of x in s is the index y such that:                                    quence s, if i has a left neighbor in s, then the value
                                                                                     stored in s at the index of the left neighbor is
 – y < x,
                                                                                     smaller than the value stored at index i, namely, if
 – the value stored at index y in s, written s[y], is smaller
                                                                                     left[i] is a valid index of s then s[left[i]] < s[i].
   than the value stored at index x in s,
                                                                                  3. Smallest: verify that, for each index i in the input
 – there are no other values smaller than s[x] between y
                                                                                     sequence s, there are no values smaller than s[i] be-
   and x.
                                                                                     tween left[i] + 1 and i (included).
There are indexes that do not have a left neighbor; for exam-
ple, the first value, or the smallest value in a sequence.                    3.1.2 Part B: Construction of a Cartesian Tree
     We consider here an algorithm that constructs the se-
quence of left neighbors of all values of a sequence s. It                    Given a sequence s of distinct numbers, its unique Cartesian
works using a stack. At the beginning, the stack is empty.                    tree CT (s) is the tree such that:
Then, for each index x in the sequence, pop indexes from the
                                                                              1. CT (s) contains exactly one node per value of s.
stack until a index y is found such that s[y] is smaller than
                                                                              2. When traversing CT (s) in-order—that is, using a sym-
s[x]. If such a index exists in the stack, it is the left neighbor
                                                                                 metric traversal: first visit the left subtree, then the node
of x; otherwise, x does not have a left neighbor. After pro-
                                                                                 itself, and finally the right subtree—elements are encoun-
cessing x, push x onto the stack and go to the next index in
                                                                                 tered in the same order as s.
s. This algorithm is given in pseudo-code in Figure 3.
                                                                              3. Tree CT (s) has the heap property—that is, each node in
     As an example, consider sequence s = 4 7 8 1 2 3 9 5 6.
                                                                                 the tree contains a value (not an index) bigger than its
The sequence of the left neighbors of s (using indexes that
                                                                                 parent’s.
start from 1) is: left = 0 1 2 0 4 5 6 6 8. The left neighbor of
the first value of s is 0 (denoting no valid index), since the                The Carthesian tree of sequence s = 4 7 8 1 2 3 9 5 6 is given
first value in a list has no values at its left. The fourth value             in Figure 4.

                                                                          8
     There are several algorithms to construct a Cartesian tree         as a challenge by itself. Completing the implementation and
in linear time from its input sequence. The one we consider             verification of the actual Cartesian tree construction algo-
here is based on the all nearest smaller values problem (part           rithm turned out to be decidedly more complicated: writ-
A of this challenge). Let’s consider a sequence of distinct             ing the algorithm itself was no big deal, but understanding
numbers s. First, we construct the sequence of left neighbors           how it works well enough to prove it correct was more chal-
for the value of s using the algorithm in Figure 3. Then, we            lenging. In particular, proving property traversal (in-order
construct the sequence of right neighbors using the same al-            traversal of a Cartesian tree gives the input sequence) took
gorithm, but starting from the end of the list. Thus, for every         nearly one day of work for a complete working solution in
index x in sequence s, the parent of x in CT (s) is either:             SPARK.
                                                                             Following these investigations, we considered the possi-
 – The left neighbor of x if x has no right neighbor.
                                                                        bility of simply dropping from the challenge the construc-
 – The right neighbor of x if x has no left neighbor.
                                                                        tion of Cartesian trees, and concentrating only on the con-
 – If x has both a left neighbor and a right neighbor, then
                                                                        struction of nearest smaller values. However, we decided
   x’s parent is the larger one.
                                                                        against that option, because we still wanted to give partic-
 – If x has no neighbors, then x is the root node.
                                                                        ipants who had the right background and tools a chance of
    To solve Challenge 2.B, we asked participants to carry              trying their hands at proving this challenging algorithm. To
out the following tasks:                                                make the overall challenge tractable, we split it in two parts.
                                                                             The first part, concerned only with nearest smaller val-
Implementation task. Implement the algorithm for the con-               ues, was explicitly presented as the simplest, and was de-
   struction of the Cartesian tree.                                     signed to be verifiable using a wide range of tools, at it only
Verification tasks.                                                     deals with sequences. Since the main algorithm (Figure 3) is
    1. Binary: verify that the algorithm returns a well                 imperative but uses stacks—which could make it a bit tricky
       formed binary tree, with one node per value (or per              to verify using only functional data structures—we let par-
       index) in the input sequence.                                    ticipants free to use an existing implementation of stacks or
    2. Heap: verify that the resulting tree has the heap prop-          even use sequences as models of stacks.
       erty, that is, each non-root node contains a value                    As for the second part, dealing with the Cartesian tree
       larger than its parent.                                          construction algorithm, we clearly split the verification job
    3. Traversal: verify that an in-order traversal of the tree         in three distinct tasks of different difficulties; and marked
       traverses values in the same order as in the input se-           the third task (property traversal) as “optional”, assuming
       quence.                                                          that it would be mostly useful as a further exercise to be
                                                                        done after the competition. We did not provide an algorithm
                                                                        in pseudo-code for this part, as writing an implementation
3.2 Designing the Challenge
                                                                        is straightforward from the textual description but also de-
                                                                        pends strongly on the data structures used to encode the tree.
The subject for the challenge was given to us by Gidon Ernst
                                                                        Instead, we presented an example of a Cartesian tree built
(one of the organizers of VerifyThis 2018) as an idea that
                                                                        from a sequence, so that participants could use it to test their
was considered but, in the end, not used for the 2018 verifi-
                                                                        implementation and to understand why it worked. We also
cation competition.
                                                                        remarked to the participants that they could implement trees
    After first reading about Cartesian trees, we were wary
                                                                        as they preferred, using for example a recursive data-type,
of the risk that using them as subject would lead to a chal-
                                                                        a pointer-based structure, or even just a bounded structure
lenge too much oriented toward functional programming—
                                                                        inside an array.
unfeasible using verification tools that cannot handle recur-
sive data structures such as trees and lists. To avoid this risk,
we focused the challenge on one specific imperative algo-               3.3 Submitted Solutions
rithm that constructs a Cartesian tree bottom-up, attaching
the nodes to their parents in the order in which they appear            Overall Results
in the input sequence.
    To better understand if we could make a challenge out               Two teams submitted solutions to challenge 2 that were both
of the this bottom-up Cartesian tree construction algorithm,            correct and complete: Team OpenJML worked on part A of
we tried to implement and verify it using the SPARK verifi-             the challenge, and Team VerCors T(w/o)o on part B. The
cation tool for Ada. We began by writing and annotating the             latter team even managed to verify a partial specification of
short loops that build the input sequence’s nearest smaller             part B’s task traversal—which was marked “optional”. An-
values to the left and to the right. This task was not compli-          other four teams completed the first two verification tasks
cated, but turned out to be time-consuming enough to serve              of part A, one of them coming close to finishing the proof

                                                                    9
of the third, with only a small part of the necessary invari-          left. In principle, this mistake in the implementation should
ant missing. Another team completed all three verification             not have invalidated their proofs of verification tasks 1 and 2,
tasks of part A but with simplifying assumptions (on the fi-           which were expressed as conditionals on any values that do
nite range of inputs). Another two teams completed part A’s            have smaller values to their left. Thus, once they noticed the
verification task 1 only. The remaining four teams didn’t go           error, they fixed the implementation and tried replaying the
further than implementing the algorithm of the same part               mechanized proofs of the first two properties. Even though
and writing partial specifications of the properties that were         they were using Sledgehammer to automate part of the rea-
to be verified.                                                        soning, only the first task could be verified without manually
                                                                       adjusting the interactive proofs—which required some dif-
                                                                       ferent proofs steps even though the overall proof logic was
Detailed Results
                                                                       unchanged.
Most teams attempted part A of challenge 2, as it was pre-                  Both teams using Coq, Team Jourdan-Mével and
sented as the more approachable of the two. Only two teams             Team Coinductive Sorcery , implemented a functional ver-
attempted part B: Team VerCors T(w/o)o , using VerCors,                sion of the pseudo-code in Figure 3 using two recursive func-
who focused entirely on part B, and Team The Refiners , us-            tions instead of loops—just like Team Bashers did in Is-
ing Isabelle, whose two members decided to work separately             abelle. This encoding proved tricky to get right: both teams
in parallel—one person on each part of the challenge—to                ended up with a slightly incorrect “off-by-one” version of
assess which was more feasible (and eventually decided to              the algorithm that also pops (instead of just inspecting it)
focus on part A).                                                      the first value y on the stack that satisfies s[y] < s[x] (exit
     Both teams working on part B represented trees using              condition of the inner loop in Figure 3) and thus is the left
a “parent” relation mapping an index in the input sequence             neighbor of current value x. This mistake does not affect
to the index of its parent node in the tree. Team The Re-              the verification of tasks 1 and 2 (index and value), and, in
finers encoded this relation as a function on indexes. They            fact, the Coq teams did not notice it and still managed to
managed to verify the second verification task (heap: the              specify (both teams) and prove (Team Jourdan-Mével ) these
tree is a heap), but then decided to continue to work on               two tasks. In contrast, the invariant needed to prove the third
part A of the challenge, since it seemed more suitable for             verification task (smallest) depends on all values previously
their tool’s capabilities. In contrast, Team VerCors T(w/o)o           processed during the computation, which means that it could
stored the parent of each value in the input sequence using            not have been expressed on the implementations written by
another sequence. They also defined two other arrays, stor-            the Coq teams but would have required additional informa-
ing the left and right child of each node. On tree structures          tion about processed values to be passed as part of the recur-
encoded using this combination of parent and child rela-               sive functions’ arguments.
tions, Team VerCors T(w/o)o managed to complete part B’s                    As presented in Figure 3, the algorithm for the construc-
verification tasks 1 and 2. They even verified a partial ver-          tion of the sequence of all nearest smaller values of an in-
sion of task 3’s property traversal—partial because it in-             teger sequence was more suited to an imperative implemen-
volved only a node’s immediate children instead of the whole           tation. The Java implementation produced by Team Open-
left and right subtrees.                                               JML was indeed very close to that pseudo-code algorithm.
     Even though they tackled the same problem, the two                It included a low-level stack implementation consisting of
submissions in Isabelle for part A of the challenge were               an array along with a separate variable storing the stack’s
very different. Team Bashers sticked to the usual functional           top value index. The three properties—corresponding to the
programming style most common in Isabelle. They imple-                 three verification tasks index, value, and smallest—were ex-
mented the algorithm using two recursive functions to rep-             pressed in a direct way, and all were verified automatically
resent the two loops in the pseudo-code of Figure 3. By con-           by OpenJML without manual input other than the suitable
trast, Team The Refiners —true to their name—deployed Is-              loop invariants. The loop invariant for the third verification
abelle’s refinement framework to encode the algorithm di-              task was by far the most complex, but, once it was expressed
rectly in an iterative fashion, so that their implementation           correctly, the automated prover Z3—used as the backend of
could closely match the pseudo-code in Figure 3. On top of             OpenJML—could handle it without difficulties in the auto-
this, they attempted refinement proofs to express part A’s             mated proofs.
three verification tasks. This worked well for the first two                Other teams using a language with support for impera-
tasks (index and value), but they could not carry out the third        tive programming features were also able to go quite far in
one (smallest) in time. While revising their solution after the        the implementation and the verification of the algorithm of
competition, they realized that they had not implemented the           challenge 2’s part A. These submitted solutions’ implemen-
algorithm correctly, because their encoding implied that no            tations closely matched the algorithm in Figure 3 with dif-
values in the input sequence can have a smaller value to its           ferences only in how stacks were represented. Team Merge-

                                                                  10
sort , using Why3, encoded stacks as lists with an interface              complete the other tasks in the time during the competition.
to query the first value (top) and retrieve the tail of the list          In particular, difficulties with formalizing aliasing among
(pop). The main limitation of this approach was the back-                 data structures used by the algorithm and proving absence
ground solver’s limited support for recursive lists. As a re-             of side effects—a result of C’s low-level memory model—
sult, some of the lemmas about stacks required to build the               slowed the teams down and hindered further progress.
algorithm’s overall correctness proofs couldn’t be verified                   Team Eindhoven UoT managed to verify part A entirely
automatically, and were left unproved in the submitted solu-              using the mCRL2 model checker, but had to introduce re-
tion. Despite this issue, Team Mergesort managed to verify                strictions on the cardinality of the input values due to the
the first two verification tasks, and made significant progress           nature of their verification tool. Their proofs assume lists of
on the third one. The invariants submitted for this task were             up to six values; and each value ranges over four possible
proved automatically and close to the required ones—even                  values. With these restrictions, they managed to complete
though they were not strong enough to complete the verifi-                all three verification tasks in less than an hour. In partic-
cation of task smallest.                                                  ular, the third verification task did not cause any particular
     Team Viper also came close to a complete solution of                 trouble as model checking does not need manually-provided
part A. The team’s implementation of the algorithm was                    invariants.
close to Figure 3’s, whereas the representation of stacks was
more original. Instead of using a concrete data structure,
Team Viper defined stacks in a pure logic fashion using un-
interpreted function symbols and axioms that postulate the
result of popping, pushing, and peeking on a stack.
                                                                          3.4 Postmortem Evaluation of the Challenge
Team Viper ’s submitted solution included specifications of
all three verification tasks, and complete proofs of the first
                                                                          We presented challenge 2 under the assumption that its part A
two. Since the axiomatic representation did not support ref-
                                                                          was somewhat easier and more widely feasible than part B.
erencing arbitrary values inside the stack, Team Viper re-
                                                                          The fact that most teams worked on part A may seem to con-
sorted to expressing the invariant for the third verification
                                                                          firm our assumption about its relatively lower difficulty.10 At
task using a recursive predicate. The invariant was nearly
                                                                          the same time, one out of only two teams who submitted a
complete, but the proofs could not be finished in time dur-
                                                                          complete and correct solution to challenge 2 tackled part B.
ing the competition.
                                                                          This may just be survival bias but another plausible explana-
     Team Sophie & Wytse submitted a direct implementa-
                                                                          tion is that the difficulties of the two parts are not so different
tion of Figure 3’s algorithm in VerCors. They represented
                                                                          (even though part B looks more involved).
stacks using VerCors’s mathematical sequences (an approach
that worked well because these are well supported by the                      Indeed, part A revealed some difficulties that were not
background prover). They wrote pop and peek functions to                  obvious when we designed it. First, the algorithm in Figure 3
manipulate sequences as stacks; and equipped them with                    follows an imperative style, and hence, it is not obvious how
contracts so that they could be used inside the main algo-                to encode it using functional style; various teams introduced
rithm (for lack of time, they did not provide an implemen-                subtle mistakes while trying to do so. Part B is easier in this
tation of pop). They progressed quite far in the verification             respect, as the Cartesian tree construction algorithm consists
activities, but were not able to complete the proof of part A’s           of a simple iteration over the input, which manipulates data
third task during the competition. While VerCors has no spe-              that can all be encoded indifferently using sequences, ar-
cific limitations that would have prevented them from com-                rays, or lists. Part A, in contrast, requires a stack data struc-
pleting the proof given more time (the invariant required for             ture with its operations. In the end, what really makes part B
verifying the third task is quite involved), the team’s par-              harder than part A is probably its third, optional, verifica-
ticipants remarked that invariant generation features would               tion task traversal. Specifying it is not overly complicated,
have been useful to speed up their work.                                  but proving it requires a complex “big” invariant, which was
                                                                          understandably not easy to devise in the limited time avail-
     Team YVeTTe and Team Heja mig implemented in C
                                                                          able during the competition.
the algorithm of part A, and annotated it using ACSL com-
ments. While Team YVeTTe implemented the algorithm as
described in the challenge, Team Heja mig wrote a sim-                      10 After the competition, Team VerCors T(w/o)o explained that they

pler, quadratic-time algorithm, which searches for the near-              missed our hint that part A was simpler, and chose part B only because
est smaller value to the left by iterating in reverse over the in-        it looked like a different kind of challenge (as opposed to part A, which
                                                                          they felt was similar in kind to challenge 1’s part A). In the heat of the
put sequence (that is, by literally following the definition of
                                                                          competition, participants may miss details of the challenges that may
left neighbor). Both teams managed to complete the first ver-             have helped them; this is another factor that should be considered when
ification task using Frama-C’s WP plugin, but they could not              designing a challenge.


                                                                     11
   y := (0, ..., 0)                                                                         – each process computes exactly one iteration of
   for every element (r, c, v) in m:                                                           the for loop;
      y (c) := y (c) + x (r) * v                                                            – there is a fixed number of processes, each taking
                                                                                               an equal share of the total number of for loop
Fig. 5 Algorithm to multiply an input vector x with a sparse matrix m                          iterations;
and store the result in the output vector y. Input matrix m is represented
in the COO format as a list of triplets.                                                    – work is assigned to processes dynamically (for
                                                                                               example using a work stealing algorithm).
                                                                                  Verification tasks.
4 Challenge 3: Sparse Matrix Multiplication                                           1. Verify that the sequential multiplication algorithm
                                                                                         indeed performs standard matrix multiplication (that
The third challenge targeted the parallelization of a basic                              is, it computes the output vector y with values yi =
algorithm to multiply sparse matrices (where most values                                 P
                                                                                            k xk × mk,i ).
are zero).                                                                            2. Verify that the concurrent algorithm does not exhibit
                                                                                         concurrency issues (data races, deadlocks, . . . ).
                                                                                      3. Verify that the concurrent algorithm still performs
4.1 Challenge Description                                                                the same computation as the sequential algorithm. If
                                                                                         time permits, you can also experiment with differ-
We represent sparse matrices using the coordinate list (COO)                             ent work allocation policies and verify that they all
format. In this format, nonzero values of a matrix are stored                            behave correctly.
in a sequence of triplets, each containing row, column, and
corresponding value. The sequence is sorted, first by row
index and then by column index, for faster lookup. For ex-                        4.2 Designing the Challenge
ample, the matrix:
                                                                                Since we designed challenge 3 last, after refining the de-
   0010                                                                           scription of the other two challenges, we ended up with sev-
5 8 0 0                                                                         eral desiderata for it.
         
0 0 0 0                                                                             We wanted challenge 3 to target a concurrent algorithm,
   0300                                                                           but in a way that the challenge remained feasible, at least
                                                                                  partly, also by participants using tools without explicit sup-
is encoded into the following sequence (using row and col-                        port for concurrency. Expecting widely different degrees of
umn indexes that start from 1):                                                   support for concurrency, we looked for a problem that was
                                                                                  not completely trivial for teams using model-checking tools,
(1, 3, 1) (2, 1, 5) (2, 2, 8) (4, 2, 3)
                                                                                  which typically have built-in notions of concurrent synchro-
    In this challenge, we consider an algorithm that com-                         nization and are fully automated. Finally, true to the house-
putes the multiplication of a vector of values (encoded as a                      hold style of VerifyThis competitions, we wanted a problem
sequence) with a sparse matrix. It iterates over the values                       that also involved behavioral (safety) input/output proper-
present inside the matrix, multiplies each of them by the ap-                     ties, as opposed to only pure concurrency properties like ab-
propriate element in the input vector, and stores the result at                   sence of deadlock and data races.
the appropriate index in the output vector. Figure 5 presents                         With the content of challenge 2 still fresh in our minds,
the algorithm in pseudo-code.                                                     we first briefly considered some parallel algorithms to con-
    To solve challenge 3, we asked participants to carry out                      struct Cartesian trees. It was soon clear that these would
the following tasks:                                                              have added more complexity on top of an already challeng-
                                                                                  ing problem, and would have strongly penalized teams who
Implementation tasks.                                                             found, for whatever reason, the Cartesian tree topic unpalat-
   1. Implement the algorithm to multiply a vector x with                         able.
      a sparse matrix m.                                                              Since even a modicum of concurrency significantly com-
   2. We want to execute this algorithm in parallel, so that                      plicates the behavior of an algorithm, we decided to start
      each computation is done by a different process,                            from a sequential algorithm that was straightforward to un-
      thread, or task. Add the necessary synchronization                          derstand. The first candidate was a trivial problem where dif-
      steps in your sequential program, using the synchro-                        ferent processes increment a shared variable. In a sequential
      nisation feature of your choice (lock, atomic block,                        setting, when processes execute one after another, the behav-
      . . . ).                                                                    ior is very simple to reason about. But if the processes are
      You can choose how to allocate work to processes.                           allowed to interleave (that is, they run in parallel), some in-
      For example:                                                                crements may be lost due to interference. The issue with this

                                                                             12
problem is that verifying its concurrent behavior requires             sence of concurrency issues (verification task 2). Some of
reasoning about the behavior of a program with races, but              these teams used tools with built-in support for the verifi-
most verification frameworks for concurrent programs are               cation of concurrent algorithms, while others added concur-
geared towards proving the absence of race conditions—so               rency to their mostly sequential tools via custom libraries.
that the input/output behavior of the overall program is inde-         Three teams out of the six that tackled task 2 completed the
pendent of an execution schedule. Therefore, being able to             verification task in time during the competition; all of them
reason about the behavior of a program with races seemed               happened to use a tool with built-in support for concurrency.
unsuitable.                                                            Finally, five teams attempted verification task 3 (proving
    Continuing from this observation in our search for a prob-         that the sequential and concurrent algorithms compute the
lem, we ended up considering the matrix multiplication prob-           same output). Two of them achieved substantial progress on
lem. To avoid requiring to represent bidimensional data struc-         the proofs of task 3: Team Eindhoven UoT used a model
tures we decided to target sparse matrices, whose nonzero              checker with native support for concurrency; Team The Re-
elements can be encoded with a list of triples.                        finers used Isabelle—a tool without built-in support for
    The standard sequential algorithm to multiply matrices             concurrency—and hence modeled the concurrent implemen-
is neither overly hard nor trivial, therefore it seemed a good         tation as a sequential algorithm that goes over the sparse ma-
basis for the challenge. Parallelizing it is not conceptually          trix’s elements in nondeterministic order.
difficult; however, we decided to give plenty of freedom
in how computations are assigned to concurrent units (pro-
                                                                       Detailed Results
cesses, threads, or tasks) both to accommodate different tools
and to allow participants using tools with advanced support            Only teams using tools without support for concurrency at-
for concurrency to come up with sophisticated paralleliza-             tempted the verification of the sequential algorithm. Their
tion strategies and proofs.                                            implementations were close to the simple algorithm in Figure 5—
    As a final sanity check, we worked out a solution of               in some cases using recursion instead of looping. Verifica-
this challenge using the model checker Spin. ProMeLa—                  tion task 1 (prove the correctness of the sequential matrix
Spin’s modeling language—offers primitives to model non-               multiplication algorithm) required to specify the expected
deterministic processes and to synchronize them, but also              output given by “standard matrix multiplication”. The ap-
has limitations such as support of only simple data types.             proaches to expressing this property were quite varied.
These features—typical of finite-state verification tools—
                                                                           Team Mergesort , using Why3, defined a sparse matrix as
made solving challenge 3 possible in a reasonable amount of
                                                                       a record containing two fields: a regular field (representing
time but certainly non-trivial. In particular, we had to encode
                                                                       the sparse matrix in COO format) and a ghost field, repre-
parts of the state model in C, and then to finesse the link be-
                                                                       senting the same matrix as a standard bidimensional array
tween these foreign-code parts and the core ProMeLa model
                                                                       (with explicit zero values). A type invariant links together
so that the size of the whole state-space would not blow up
                                                                       the two fields so that they represent the same matrix. The
during model checking.
                                                                       type invariant does not require uniqueness of indexes in the
    Finally, we revised the description of challenge 3 to make         COO representation; if the element at a certain row and col-
sure that it was not biased towards any particular approach            umn appears more than once in the input sequence, its value
to modeling or reasoning about concurrency, and that its se-           in the “standard” matrix is taken to be the sum of values
quential part was clearly accessible as a separate verification        in all such occurrences. Team YVeTTe , using Frama-C, in-
problem.                                                               troduced the “standard” matrix as an additional parameter
                                                                       of the multiplication function. The predicate linking the two
                                                                       representations was straightforward, stating that all elements
4.3 Submitted Solutions
                                                                       in the COO representation are in the matrix, and that any el-
                                                                       ements of the matrix not in COO representation are zero.
Overall Results
                                                                       Uniqueness of indexes in the input sequence follows by as-
No teams solved challenge 3 completely. Six teams, out of              suming that they are ordered. Team KIV followed a different
the 12 teams11 that took part in VerifyThis’s third and fi-            approach to ensure uniqueness of indexes: they represented
nal session, attempted the verification of the sequential al-          the input sparse matrix by means of a map instead of a list.
gorithm only—usually because their tools had little or no              For “standard” matrices, they went for arrays of arrays, as
support for concurrency; out of these six teams, one com-              KIV does not have support for multi-dimensional arrays.
pleted verification task 1. Another six teams introduced con-          Team Mergesort , Team YVeTTe and Team KIV achieved
                                                                       good results in producing accurate specifications, but they
currency in their implementation and tried to verify the ab-
                                                                       did not have enough time left to complete the verification
 11   That is, one team skipped the last session.                      task during the competition.

                                                                  13
     Several teams who used tools without built-in support            Team Jourdan-Mével , using Coq’s Iris, verified the safety
for concurrency still managed to model concurrent behavior        of a single arbitrary iteration of the concurrent loop in Figure 5.
indirectly by making the order in which input elements are        They encoded the concurrent algorithm using a deeply em-
processed nondeterministic. Team Viper defined axiomati-          bedded toy language named LambdaRust, which features
cally a summation function over sets, and used it to specify      compare-and-set instructions as synchronization primitives.
progress: at any time during the computation, a set variable      They ran out of time trying to extend the proof to all itera-
stores the elements of the input that have been processed so      tions of the loop.
far; the current value of the output is thus the sum involving         Both teams using VerCors followed the same strategy of
all the matrix elements in that set. This specification style     implementing the concurrent multiplication algorithm using
has the advantage of being independent of the order in which      parallel loops and an atomic block around the output up-
input elements are processed, and thus it encompasses both        date (the loop’s body) to avoid interference. Thanks to Ver-
the sequential and the concurrent algorithms. By the end of       Cors’s features, they had no major difficulties verifying that
the competition, Team Viper got close to completing the cor-      the code does not exhibit concurrency issues. Progress in
responding correctness proofs.                                    task 3—verifying the functional behavior of the algorithm—
     Following a somewhat similar idea, Team Coinductive          was more limited. A major stumbling block was that Ver-
Sorcery implemented two versions of the multiplication al-        Cors does not have support for summation over collections
gorithm: one operating directly on the COO list, and the          of elements; introducing and specifying this feature (required
other on a binary tree. The tree defines a specific order in      for task 3) was quite time-consuming. Team VerCors T(w/o)o
which elements are processed and combined to get the final        set up the algorithm’s functional specification by introduc-
result, corresponding to different execution schedules. Then,     ing a summation function without specifying it fully—which
Team Coinductive Sorcery proved a lemma stating that both         limited the extent of what could be proved. Their specifi-
versions of the algorithm compute the same output—with            cation used ghost variables to encode the input’s matrix in
some unproved assumptions about the associativity of vec-         “regular” form, as well as a mapping between this form and
tor addition.                                                     the COO input sequence in sparse form. The mapping ex-
     Team The Refiners used Isabelle’s refinement framework       plicitly defined an element in the COO sequence for every
to prove that the sequential algorithm for multiplication of      nonzero element of the full matrix, so that no existential
sparse matrices (Figure 5) was a refinement of the “stan-         quantification is needed.
dard” multiplication algorithm on regular matrices. Then,             Team Eindhoven UoT was the only team that completed
to lift their proofs to the concurrent setting, they modified     verification of task 3, albeit with the usual simplifying as-
the sequential algorithm so that it inputs a multiset instead     sumptions (on input size and on the number of processes)
of a list. Since the order in which a multiset’s elements are     that are required by the finite-state nature of model check-
processed is nondeterministic, the modified algorithm mod-        ers. They explicitly built the “standard” matrix equivalent of
els every possible concurrent execution. They also started        the input sparse matrix, and verified that the output was the
modeling a work assignment algorithm (as an implementa-           expected result for all possible finitely many interleavings
tion of a folding scheme over the multisets), but they did not    (which are exhaustively explored by the model checker). If
completely finish the proofs of this more advanced part.          they had had more time, they remarked that they would have
     In preparation for their participation in VerifyThis,        tried to validate their model: the proofs assert the equiva-
Team Bashers developed a library for verifying concurrent         lence of two implementations, but it would be best to per-
programs in Isabelle, which they could deploy to solve chal-      form a sanity check that they work as expected.
lenge 3. The library supported locking individual elements
of an array. Unfortunately, this granularity of locking turned
out to be too fine grained for challenge 3, and they struggled
to adapt it to model the algorithm of challenge 3 in a way
that worked well for verification.                                4.4 Postmortem Evaluation of the Challenge
     Among the tools used in VerifyThis 2019, three had built-
in support for concurrency: VerCors (using separation logic),     Regardless of whether their verification tools supported con-
Iris (a framework for higher-order concurrent separation logic    currency, all teams had plenty of work to do in challenge 3.
in Coq), and the model checker mCRL2. The four teams us-          We wanted a challenge that was approachable by everybody,
ing these tools—Team VerCors T(w/o)o , Team Sophie &              and it seems that challenge 3 achieved this goal.
Wytse , Team Jourdan-Mével , and Team Eindhoven UoT —                 On the other hand, the challenge turned out to be more
managed to encode the concurrent algorithm, and to verify,        time-consuming than we anticipated. The sequential and the
possibly under simplifying assumptions, that it does not ex-      concurrent part alone were enough to fill all 90 minutes of
hibit concurrency issues (verification task 2).                   the competition session, and no team could complete the

                                                             14
whole challenge.12 When we designed the challenge, we did                   code, added comments, and improved a few aspects of the
not realize how time-consuming it would be.                                 implementation or specification to make them more read-
    The multiplication algorithm is conceptually simple, but                able. Team YVeTTe thoroughly revised their solutions and
verifying it requires to fill in a lot of details, such as as-              filled in missing parts of specification and proofs, so as to
sociativity and commutativity properties of arithmetic oper-                complete parts A of challenges 1 and 2, and the sequential
ations, that are not central to the algorithm’s behavior but                part of challenge 3. Team KIV and Team Viper went further,
are necessary to complete the proofs. In most cases, it was                 as they also completed the concurrent part of challenge 3.
these details that prevented participants from completing the               So did Team VerCors T(w/o)o , Team Sophie & Wytse ,13
challenge. Another feature that is often missing from verifi-               and Team The Refiners who also provided partial solutions
cation tools but was required for challenge 3 is the ability                for part B of challenge 2. Team Mergesort submitted exten-
of expressing sums over sets and sequences; while this can                  sively revised solutions, including the only complete solu-
always be specified and verified, doing so takes time and                   tion to challenge 2’s part B—relying on a Coq proof of task
distracts from the main goal of the challenge.                              traversal14 —and the sequential part of challenge 3.
    In all, verification challenges involving concurrency are                    The process of revising and extending solutions after the
not only harder to verify but also to design! There are so                  competition is very different from that of developing them
many widely different concurrency models and verification                   from scratch during it. With virtually unlimited time at their
frameworks that calibrating a challenge so that it suits most               disposal, and the freedom to explore different approaches
of them is itself a challenge. A possible suggestion to come                even if they may not pan out in the end, every team could in
up with concurrency challenges in the future is to write prob-              principle come up with a complete and correct solution. At
lems with different parts that are suitable for different verifi-           the same time, comparing the post-competition work of dif-
cation approaches. This strategy worked to ensure that tools                ferent teams is not very meaningful since some may simply
without support for concurrency still had work to do in this                not have additional time to devote to improving solutions—
challenge, and it may be generalizable to encompass differ-                 after all, we made it clear that revising solutions was some-
ent styles of concurrent programming and reasoning.                         thing entirely optional that they did not commit to when they
                                                                            signed up for the competition.

5 Discussion
                                                                            5.2 Used Tools and Features
We organize the discussion around four themes. Section 5.1
outlines how teams revised their solutions for publication                  Undeniably, SMT solvers have been a boon to verification
in the months after the competition. Section 5.2 points out                 technology, but some of their limitations may be a source of
some tool features that emerged during VerifyThis 2019, and                 frustration even for users with lots of experience. Team Open-
briefly discusses how they relate to open challenges in veri-               JML reported the well-known problem of unresponsive proof
fication technology. Section 5.3 analyzes the features of the               attempts: when a proof attempt is taking a long time, the user
verification challenges offered over the years, and how they                has to decide whether to abort it or to wait longer—hoping to
affect the teams’ success rate. Section 5.4 mentions some                   get some counterexample information that may help debug
lessons we learned during this year’s VerifyThis, which we                  the failed verification attempt.
would like to pass on to future organizers.                                      Nowadays, SMT solvers are not limited to so-called auto-
                                                                            active [24] tools such as OpenJML but also boost the level
                                                                            of automation of interactive provers. The Isabelle proof as-
5.1 Revised Solutions                                                       sistant, for instance, extensively uses its Sledgehammer fea-
                                                                            ture to automate the most routine proof steps (which make
A couple of weeks after VerifyThis was over, we contacted                   up a very large percentage of a typical proof). Once an SMT
all participants again, asking them permission to publish their             solver manages to close the proof of some branch, Isabelle
solutions online. Teams who consented had the choice of ei-                 performs proof reconstruction in order to generate a verifi-
ther publishing the solutions they submitted during the com-                able certificate of the SMT proof so that it can be soundly
petition or supplying revised solutions—which they could                    integrated into the overall Isabelle proof. Team The Refin-
prepare with substantially more time and the benefit of hind-               ers , using the Isabelle theorem prover, found the proof re-
sight. Nine teams submitted revised solutions—from light                    construction step to be very time consuming in some cases,
revisions to significant extensions. Among the former,
                                                                             13 Team VerCors T(w/o)o and Team Sophie & Wytse worked to-
Team Jourdan-Mével and Team OpenJML cleaned up their
                                                                            gether to prepare one revised solution that merged both teams’ inde-
 12 Using a model checker, Team Eindhoven UoT covered all verifi-           pendent work during the competition.
cation tasks but relied on simplifying assumptions on input size and         14 The proof obligation was generated automatically by Why3, but

number of processes.                                                        the Coq proof steps were supplied manually.


                                                                       15
                                                                                                V ERIFY T HIS COMPETITION
which even prevented them from completely closing the proof
                                                                                         2011 2012 2015 2016 2017 2018 2019 BY TOOL
of some steps in time during the competition—even when
                                                                        AProVe              1      0    0    0    0     0   0     1
they were confident in the SMT solver’s results.                        AutoProof           0      0    1    0    0     0   0     1
     Using a high-level programming language (for exam-                 CBMC                0      0    1    0    0     0   0     1
                                                                        CIVL                0      0    0    1    1     1   0     3
ple, one with an expressive type system) lets users focus               Coq                 0      0    0    0    0     1   2     3
on verifying complex behavioral properties on top of basic              Dafny               1      2    3    5    1     1   0    13
                                                                        ESC/Java2           0      1    0    0    0     0   0     1
correctness properties (such as memory safety)—which are                F*                  0      0    1    0    0     0   0     1
guaranteed by the language’s semantics. In contrast, when               Frama-C             0      0    1    0    1     1   2     5
                                                                        GNATProve           0      1    0    0    0     0   0     1
using a lower-level programming language, a large fraction              Isabelle            0      0    0    0    0     1   2     3
of verification effort has to be devoted to establishing such           jStar               1      0    0    0    0     0   0     1
                                                                        KeY                 1      1    1    1    2     1   0     7
basic properties—a time-consuming activity which may sti-               KIV                 1      1    1    1    1     1   1     7
                                                                        mCRL2               0      0    1    1    0     0   1     3
fle progress towards more advanced verification goals. We               MoCHi               0      0    1    0    0     0   0     1
witnessed this phenomenon during the competition, when                  OpenJML             0      0    0    0    0     0   1     1
                                                                        PAT                 0      1    0    0    0     0   0     1
teams using C or other relatively low-level languages spent             VCC                 0      1    0    0    0     0   0     1
the majority of the time at their disposal verifying mem-               VerCors             0      0    1    1    1     2   2     7
                                                                        VeriFast            0      1    1    1    0     1   0     4
ory separation properties, while their colleagues using high-           Viper               0      0    0    1    0     1   1     3
level languages could just assume them and jump right to the            Why3                1      2    1    2    3     1   1    11

key input/output properties required by the problem state-              BY COMPETITION      6      9   12    9    7    11   9

ment.                                                              Table 2 Verification tools used in each VerifyThis competition. Num-
                                                                   ber n in row t and column y means that n teams used tool t during Ver-
     VerifyThis has included a challenge involving concur-
                                                                   ifyThis y . The rightmost column (BY TOOL) reports the total number
rency since its 2015 edition. While it is probably still true      of teams that used each tool; and the bottom row (BY COMPETITION )
that the majority of program verification tools focus on se-       reports how many different tools were used in each competition.
quential correctness, features to reason about concurrency
and parallelism are increasingly available. Despite this un-
deniable progress, verifying concurrent program remains for-       VerifyThis competitions to date. A team has used one sin-
midably difficult, and even participants using a tool expressly    gle tool in all cases except for a single-person team that
designed to reason about concurrency (such as VerCors and          used two tools (Dafny and KeY) during VerifyThis 2018.
Viper, both supporting a permission logic) spent a consider-       Teams winning the “best overall” award used one of three
able amount of time choosing what kind of synchronization          tools: Isabelle, VeriFast, and Why3—each tool used by two
primitive to use and how to model them in a formal way.            awardees. The tools used by winners of “best student team”
     Model checkers are in a league of their own, since they       include Dafny, KIV, mCRL2 (one winning team each), Ver-
are more similar to the tools used in fully-automated veri-        Cors (two winning teams), and Why3 (five winning teams).
fication competitions such as SV-COMP than to the auto-            Several tools were singled out for having a “distinguished
active or interactive tools that most participants to Verify-      feature” that deserved an award because it was apt to tackle
This prefer. A model checker performs proofs completely            some verification challenges: CIVL, GNATProve, Isabelle,
automatically (crucially, it does not require users to sup-        KIV, MoCHi, VerCors, Viper, and Why3.
ply invariants) and is very effective at finding errors when
they exist. Modeling concurrency is also typically straight-
forward, since the programming language of a model checker
                                                                   5.3 What Makes a Challenge Difficult?
is typically built around a transparent model of parallel pro-
cesses that communicate through shared memory, message             We used various criteria to classify the 21 challenges used
passing, or both. On the flip side, model checkers can only        at VerifyThis to date—three in each edition excluding Veri-
explore finite state spaces, and hence cannot normally per-        fyThis 2014, which was run a bit differently among partici-
form verification of algorithms on unbounded data struc-           pants to a Dagstuhl Seminar. We classified each challenge
tures. While these differences complicate judging teams us-        according to which VerifyThis competition it belongs to,
ing model checkers on par with others, we believe that hav-        whether it appeared first, second, or third in order of com-
ing teams using model checkers taking part in VerifyThis           petition, how much time was given to solve it, whether it
adds depth to the competition, and strengthens the connec-         targets a sequential or concurrent algorithm, what kind of
tions with other verification competitions while emphasiz-         input data it processes (array, tree, linked list, and so on),
ing its own peculiarity and focus.                                 whether the main algorithm’s output involves the same kind
                                                                   of data structure as the input, whether the challenge’s main
Trends in tool usage. Table 2 updates the data about tools         algorithm is iterative or recursive (or if the algorithm is only
used at VerifyThis [10]. A total of 23 tools were used in          outlined), and whether the input data structure is mutable

                                                              16
        PROBLEM                             COMPETITION ORDER TIME SEQUENTIAL INPUT        OUTPUT ALGORITHM MUTABLE          PARTIAL COMPLETE

        Maximum by elimination                VT11          1    60 sequential   array       simple iterative    immutable       83        67
        Tree maximum                          VT11          2    90 sequential   tree        simple outlined     immutable      100        17
        Find duplets in array                 VT11          3    90 sequential   array       simple find         immutable       83        50
        Longest common prefix                 VT12          1    45 sequential   array       simple iterative    immutable      100        73
        Prefix sum                            VT12          2    90 sequential   array       complex outlined    immutable       73         9
        Delete min node in binary search tree VT12          3    90 sequential   tree        same    recursive   mutable         18         0
        Relaxed prefix                        VT15          1    60 sequential   array       same    iterative   immutable       79         7
        Parallel GCD by subtraction           VT15          2    60 concurrent   scalar      same    iterative   mutable         79        14
        Doubly linked lists                   VT15          3    90 sequential   linked list same    outlined    mutable         71         7
        Matrix multiplication                 VT16          1    90 sequential   matrix      same    iterative   immutable       86        43
        Binary tree traversal                 VT16          2    90 sequential   tree        simple iterative    mutable         79         7
        Static tree barriers                  VT16          3    90 concurrent   tree        simple iterative    mutable         79         7
        Pair insertion sort                   VT17          1    90 sequential   array       same    iterative   mutable        100        10
        Odd-even transposition sort           VT17          3    90 concurrent   array       same    iterative   mutable         60         0
        Tree buffer                           VT17          4    90 sequential   tree        same    recursive   immutable       40        20
        Gap buffer                            VT18          1    60 sequential   array       same    iterative   mutable         91        36
        Count colored tiles                   VT18          2    90 sequential   array       same    recursive   immutable       55        18
        Array-based queue lock                VT18          3    90 concurrent   array       simple iterative    mutable         27         9
        Monotonic segments and GCG sort VT19                1    90 sequential   array       same    iterative   immutable       85        15
        Cartesian trees                       VT19          2    90 sequential   array       complex iterative   immutable       69        15
        Sparse matrix multiplication          VT19          3    90 concurrent   matrix      same    iterative   immutable       85         0

Table 3 For each challenge PROBLEM used at VerifyThis: the COMPETITION when it was used; the ORDER in which it appeared; how much TIME
(in minutes) was given to participants to solve it; whether the main algorithm is SEQUENTIAL or concurrent; the main INPUT data type; whether
the OUTPUT data type is of the same kind as the input, simpler, or more complex; when the ALGORITHM was given in pseudo-code, whether it
was iterative or recursive (if it was not given, whether it was outlined or participants had to find it based on the requirements); whether the input
is MUTABLE or immutable; and the percentages of participating teams that were able to submit a partial or COMPLETE solution.



or immutable. For each challenge, we also record what per-                    accessible one, and participants get tired as a competition
centage of participating teams managed to submit a partial                    stretches over several hours.
or complete correct solution. Table 3 shows the results of                        When a challenge’s main algorithm is only outlined, or
this classification.                                                          is given in pseudo-code but is recursive, and when the in-
     To help us understand which factors affect the complex-                  put is a mutable data structure, participants found it harder
ity of a verification problem, we fit a linear regression model               to complete a correct solution. While the difficulty of deal-
(with normal error function) that uses competition, order,                    ing with mutable input is well known—and a key challenge
time, sequential, input, output, algorithm, and mutable as                    of formal verification—different reasons may be behind the
predictors, and the percentage of complete solutions as out-                  impact of dealing with naturally recursive algorithms. One
come.15 Using standard practices [14], categorical predic-                    interpretation is that verification tools are still primarily
tors that can take n different values are encoded as n − 1 bi-                geared towards iterative algorithms; a different, but related,
nary indicator variables—each selecting a possible discrete                   interpretation is that VerifyThis organizers are better at gaug-
value for the predictor. Fitting a linear regression model pro-               ing the complexity of verifying iterative algorithms, as op-
vides, for each predictor, a regression coefficient estimate                  posed to that of recursive algorithms that may be easy to
and a standard error of the estimate; the value of the predic-                present but hard to prove correct.
tor has a definite effect on the outcome if the corresponding                     Sequential algorithms, as opposed to concurrent ones,
coefficient estimate differs from zero by at least two stan-                  are associated with harder problems. Since the association is
dard errors.                                                                  not very strong, it is possible that this is only a fluke of the
     Our analysis suggests that the competition challenges                    analysis: sequential algorithms are the vast majority (76%)
were somewhat simpler in the early editions compared to                       of challenges and thus span a wide range of difficulties; the
the recent editions (starting from VerifyThis 2015): the co-                  few challenges involving concurrent algorithms have often
efficients for indicator variables related to predictor compe-                been presented in a way that they offer a simpler, sequential
tition for the years 2015–2017 and 2019 are clearly nega-                     variant (see for example challenge 3 in Section 4)—which
tive, indicating that belonging to one of these editions tends                may be what most teams go for.
to decrease the number of correct solutions. Similarly, the                       The input data structure also correlates with the ease of
later a challenge problem appears in a competition the fewer                  verification. Unsurprisingly, when the algorithm’s input is a
teams manage to solve it correctly. This is to be expected, as                scalar more teams are successful; but, somewhat unexpect-
the first challenge is normally the simpler and more widely                   edly, success increases also when the input is a linked list
 15 We could also perform a similar analysis using the percentage
                                                                              or a tree. It is possible that the organizers are well aware of
                                                                              the difficulty of dealing with heap-allocated data structures,
of partial solutions as outcome. However, what counts as “partially
correct” is a matter of degree and depends on a more subjective               and hence stick to relatively simple algorithms when using
judgment—which would risk making the analysis invalid.                        them in a verification challenge. Another possibility is that

                                                                         17
linked lists and trees just featured a few times (compared             questionnaire was primarily made of open questions and col-
to the ubiquitous arrays), and hence their impact is more of           lected qualitative data, it may be interesting to complement
a statistical fluke. Input in matrix form is associated with           it with quantitative information about the challenges and the
harder problems too; this is probably because most verifi-             solutions—such as the size of specifications, implementa-
cation tools have no built-in matrix data types, and repre-            tion, and other tool-specific annotations. Collecting such in-
senting bidimensional data using arrays or lists is possible           formation consistently year after year could also pave the
in principle but may be cumbersome.                                    way for more insightful analyses of the trends in the evolu-
                                                                       tion of verification technology as seen through the lens of
                                                                       verification competitions (perhaps along the lines of what
5.4 Lessons Learned for Future Competitions
                                                                       we did in Section 5.3).
                                                                            We are always pleased to see how committed partici-
Most verification tools are somewhat specialized in the kinds
                                                                       pants are, and how much effort they put into their work dur-
of properties and programs they mainly target; such special-
                                                                       ing and after the competition. One sign of this commitment
ization normally comes with a cost in terms of less flexibility
                                                                       is that most teams (see Section 5.1 for details) were avail-
when tackling challenges outside their purview. VerifyThis
                                                                       able to substantially revise their solutions during the weeks
organizers try to select challenges that target different do-
                                                                       and months after the competition, so that we could publish
mains and properties, so that no participants will be exclu-
                                                                       a complete solution that shows the full extent of the capa-
sively advantaged. However, this may also indicate that it
                                                                       bilities of their tools. It may be interesting to find ways to
may be interesting to see the participation of teams using dif-
                                                                       give more visibility to such additional work—for example,
ferent approaches. While only one team has used two differ-
                                                                       publishing post proceedings where teams can describe in de-
ent verification tools in the history of VerifyThis, teams us-
                                                                       tail their work and how it was perfected. Since not all par-
ing verification frameworks that integrate different libraries
                                                                       ticipants may be able to commit to such an extra amount
and features effectively have at their disposal a variety of
                                                                       of work, this may be organized only occasionally, and con-
approaches. For instance, Team The Refiners used a refine-
                                                                       tributing to it should be on a voluntary basis.
ment library for Isabelle only in one challenge, whereas they
stuck to Isabelle’s mainstream features for the rest of the
competition. In order to promote eclectic approaches to ver-           Acknowledgements We thank Amazon Web Services for sponsoring
                                                                       travel grants and monetary prizes; Gidon Ernst, Nadia Polikarpova,
ification, organizers of future events may introduce a new             and Stephen F. Siegel for submitting ideas for competition problems;
award category that rewards the teams that displayed the               and Virgile Prevosto for accepting, on a short notice, our invitation to
widest variety of approaches during the competition.                   give a tutorial. The extensive support by local organizers of ETAPS
    VerifyThis challenges are made publicly available after            was fundamental for the practical success of VerifyThis. Being part of
                                                                       TOOLympics further enhanced the interest and variety of the partici-
the competition every year, and several team members took              pants’ experience, and made VerifyThis more widely visible. Finally,
part in more than one competition. Therefore, the most com-            our biggest “thank you” goes to the participants for their enthusias-
petitive and ambitious teams are aware of the kinds of prob-           tic participation, for their effort (often continued after the competition
lems that will be presented, and may be better prepared to             when preparing revised solutions), and for contributing to interesting
                                                                       discussions in an amiable atmosphere.
solve them in the limited time at their disposal. We have
evidence of at least one team that went one step further
preparing for the competition this year: Team Bashers cre-
                                                                       References
ated an Isabelle library to reason about concurrency, expect-
ing a challenge of the same flavor as those given in recent             1. Amighi, A., Blom, S., Huisman, M.: VerCors: A layered
years. These observations may give new ideas to organiz-                   approach to practical verification of concurrent software.
ers of future events to design verification challenges that                In: 24th Euromicro International Conference on Paral-
are interesting but also feasible. For example, they could an-             lel, Distributed, and Network-Based Processing (PDP),
                                                                           pp. 495–503. IEEE Computer Society (2016).           URL
nounce before the competition (in the call for participation)              https://ieeexplore.ieee.org/abstract/document/7445381
some topics that will appear in the verification challenges,            2. Bertot, Y., Castéran, P.: Interactive Theorem Proving and Program
or some program features that participants will be expected                Development. Springer (2004)
to deal with—but without mentioning specific algorithms or              3. Beyer, D., Huisman, M., Klebanov, V., Monahan, R.: Evaluat-
                                                                           ing Software Verification Systems: Benchmarks and Competitions
problems. Researchers and practitioners interested in partic-              (Dagstuhl Reports 14171). Dagstuhl Reports 4(4), 1–19 (2014)
ipating may then use this information to focus their prepara-           4. Blom, S., Darabi, S., Huisman, M., Oortwijn, W.: The VerCors
tion.                                                                      tool set: Verification of parallel and concurrent software. In: 13th
    Following the recurring suggestions of previous organiz-               International Conference on Integrated Formal Methods (IFM),
                                                                           Lecture Notes in Computer Science, vol. 10510, pp. 102–110.
ers, we used a questionnaire to help compare solutions and                 Springer (2017)
judge them. This was of great help and we hope future or-               5. Bobot, F., Filliâtre, J.C., Marché, C., Paskevich, A.:
ganizers can improve this practice even further. While our                 Why3: Shepherd your herd of provers.             In: Boogie 2011:


                                                                  18
    First International Workshop         on Intermediate Verifica-                  higher-order concurrent separation logic. J. Funct. Program. 28,
    tion Languages, pp. 53–64.           Wrocław, Poland (2011).                    e20 (2018)
    https://hal.inria.fr/hal-00790310                                           21. Kirchner, F., Kosmatov, N., Prevosto, V., Signoles, J.,
 6. Bormer, T., Brockschmidt, M., Distefano, D., Ernst, G., Filliâtre,              Yakobowski, B.: Frama-C: A software analysis perspective.
    J., Grigore, R., Huisman, M., Klebanov, V., Marché, C., Monahan,                Formal Asp. Comput. 27(3), 573–609 (2015)
    R., Mostowski, W., Polikarpova, N., Scheben, C., Schellhorn, G.,            22. Klebanov, V., Müller, P., Shankar, N., Leavens, G.T., Wüstholz,
    Tofan, B., Tschannen, J., Ulbrich, M.: The COST IC0701 verifica-                V., Alkassar, E., Arthan, R., Bronish, D., Chapman, R., Cohen,
    tion competition 2011. In: Formal Verification of Object-Oriented               E., Hillebrand, M.A., Jacobs, B., Leino, K.R.M., Monahan, R.,
    Software (FoVeOOS), Lecture Notes in Computer Science, vol.                     Piessens, F., Polikarpova, N., Ridge, T., Smans, J., Tobies, S.,
    7421, pp. 3–21. Springer (2012)                                                 Tuerk, T., Ulbrich, M., Weiß, B.: The 1st verified software com-
 7. Bunte, O., Groote, J.F., Keiren, J.J.A., Laveaux, M., Neele, T.,                petition: Experience report. In: FM 2011: Formal Methods, Lec-
    de Vink, E.P., Wesselink, W., Wijs, A., Willemse, T.A.C.: The                   ture Notes in Computer Science, vol. 6664, pp. 154–168. Springer
    mCRL2 toolset for analysing concurrent systems – improvements                   (2011)
    in expressivity and usability. In: Tools and Algorithms for the             23. Lammich, P.: Refinement to imperative HOL. J. Autom. Reason-
    Construction and Analysis of Systems (Part II), Lecture Notes in                ing 62(4), 481–503 (2019)
    Computer Science, vol. 11428, pp. 21–39. Springer (2019)                    24. Leino, K.R.M., Moskal, M.: Usable auto-active verification. In:
 8. Cok, D.R.: OpenJML: Software verification for Java 7 using JML,                 Usable Verification Workshop. http://fm.csl.sri.com/UV10/
    OpenJDK, and Eclipse. In: Proceedings 1st Workshop on Formal                    (2010)
    Integrated Development Environment (F-IDE), EPTCS, vol. 149,                25. Müller, P., Schwerhoff, M., Summers, A.J.: Viper: A verification
    pp. 79–92 (2014)                                                                infrastructure for permission-based reasoning. In: Verification,
 9. Cranen, S., Groote, J.F., Keiren, J.J.A., Stappers, F.P.M., de Vink,            Model Checking, and Abstract Interpretation (VMCAI), Lecture
    E.P., Wesselink, W., Willemse, T.A.C.: An overview of the                       Notes in Computer Science, vol. 9583, pp. 41–62. Springer-Verlag
    mCRL2 toolset and its recent advances. In: Tools and Algorithms                 (2016)
    for the Construction and Analysis of Systems, Lecture Notes in              26. Wenzel, M., Paulson, L.C., Nipkow, T.: The Isabelle framework.
    Computer Science, vol. 7795, pp. 199–213. Springer (2013)                       In: 21st International Conference on Theorem Proving in Higher
10. Ernst, G., Huisman, M., Mostowski, W., Ulbrich, M.: VerifyThis                  Order Logics (TPHOL), Lecture Notes in Computer Science, vol.
    – verification competition with a human factor. In: Tools and Al-               5170, pp. 33–38. Springer (2008)
    gorithms for the Construction and Analysis of Systems – 25 Years
    of TACAS: TOOLympics, Held as Part of ETAPS 2019, Lecture
    Notes in Computer Science, vol. 11429, pp. 176–195. Springer
    (2019)
11. Ernst, G., Pfähler, J., Schellhorn, G., Haneberg, D., Reif, W.: KIV:
    Overview and VerifyThis competition. STTT 17(6), 677–694
    (2015)
12. Filliâtre, J., Paskevich, A., Stump, A.: The 2nd verified software
    competition: Experience report. In: Proceedings of the 1st Interna-
    tional Workshop on Comparative Empirical Evaluation of Reason-
    ing Systems, CEUR Workshop Proceedings, vol. 873, pp. 36–49.
    CEUR-WS.org (2012)
13. Filliâtre, J.C., Paskevich, A.: Why3 — where programs meet
    provers. In: Proceedings of the 22nd European Symposium on
    Programming (ESOP), Lecture Notes in Computer Science, vol.
    7792, pp. 125–128. Springer (2013)
14. Gelman, A., Hill, J.: Data analysis using regression and multi-
    level/hierarchical models. Cambridge University Press (2007)
15. Huisman, M., Klebanov, V., , Monahan, R., Tautschnig, M.: Ver-
    ifyThis 2015 – a program verification competition. International
    Journal on Software Tools for Technology Transfer 19(6), 763–
    771 (2017)
16. Huisman, M., Klebanov, V., Monahan, R.: On the organisation
    of program verification competitions. In: Proceedings of the 1st
    International Workshop on Comparative Empirical Evaluation of
    Reasoning Systems, CEUR Workshop Proceedings, vol. 873, pp.
    50–59. CEUR-WS.org (2012)
17. Huisman, M., Monahan, R., Müller, P., Paskevich, A., Ernst,
    G.: VerifyThis 2018: A program verification competition.
    https://hal.inria.fr/hal-01981937/ (2018). HAL Id: hal-
    01981937, version 1
18. Huisman, M., Monahan, R., Müller, P., Poll, E.: Ver-
    ifyThis 2016:          A program         verification competition.
    http://hdl.handle.net/2066/161349 (2016).               CTIT tech-
    nical report 1381-3625
19. Huisman, M., Monahan, R., Müller, P., Mostowski, W., Ulbrich,
    M.: VerifyThis 2017: A program verification competition. Tech.
    Rep. 10, Karlsruher Institut für Technologie (KIT) (2017)
20. Jung, R., Krebbers, R., Jourdan, J., Bizjak, A., Birkedal, L.,
    Dreyer, D.: Iris from the ground up: A modular foundation for


                                                                           19
