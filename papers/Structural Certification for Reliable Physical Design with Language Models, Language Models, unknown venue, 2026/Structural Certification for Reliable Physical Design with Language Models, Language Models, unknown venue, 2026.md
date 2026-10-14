                                                Structural Certification for Reliable Physical Design with
                                                                     Language Models

                                                                            Nakul Vyas1* and Iliya D. Stoev1,2*
                                                1
                                                 Heysuvi Labs, LLC, US Operations & Research, 7345 W Sand Lake Rd, Ste 210,
                                                                         Orlando, 32819, FL, United States.
                                           2
                                             Institute of Biological and Chemical Systems - Functional Molecular Systems, Karlsruhe
                                              Institute of Technology, Hermann-von-Helmholtz-Platz 1, Eggenstein-Leopoldshafen,
arXiv:2606.30107v1 [cs.AI] 29 Jun 2026




                                                                       76344, Baden-Württemberg, Germany.


                                                    *Corresponding author(s). E-mail(s): nvyas@heysuvi.com; istoev@heysuvi.com;
                                                                                iliya.stoev@kit.edu;


                                                                                              Abstract
                                              An unreliable language model can be made to produce reliable physical designs if the authority to
                                              assert is moved out of the model: the model proposes, and a deterministic engine alone certifies,
                                              returning certified, impossible, or unknown. We introduce Physics-Anchored Certification (PHACT),
                                              a propose–certify loop spanning five scientific domains, and identify what makes such a certificate
                                              trustworthy. A checker that accepts a model-supplied value can be forged; deriving the certified
                                              quantity from fixed inputs instead makes forgery impossible by construction. Across eighty adversarial
                                              trials spanning two models, two decoding temperatures, and a deliberately faulted engine, this contract
                                              produced zero false certifications.

                                              Keywords: machine reasoning, physical law, formal verification, self-correction, deterministic systems,
                                              propose-certify loop




                                         Main                                                          A model that has memorized every textbook will
                                                                                                       still, pushed off its training distribution, produce a
                                         A language model can produce a physically invalid             confident wrong answer. The deficit is structural:
                                         answer with the same fluency and confidence as                the model is unable to decline. We take a different
                                         a valid one. In scientific and engineering settings,          route. We do not make the model more reliable; we
                                         where a wrong result carries real experimental or             remove its authority to assert. We place it inside
                                         computational cost, the problem is not only gen-              a loop with a deterministic physics engine (the
                                         eration but certification: validity must be decided           model proposes, the engine disposes) so that a
                                         by an external physical check the model cannot                proposed design becomes an answer only once the
                                         author.                                                       engine has computed, from first principles, that it
                                             The usual response is to improve the predic-              satisfies the governing law. On rejection the model
                                         tor: more parameters, more data, better align-                is told which law was violated and by how much,
                                         ment. This helps but cannot resolve the problem,              and it revises. If every genuine attempt fails for
                                         because the problem is not a deficit of knowledge.            the same physical reason, the model does what a


                                                                                                   1
bare model is never permitted to do: it reports           Contributions
that the goal is impossible.                              (i) We formulate physically grounded design as
    A design is reliable to the extent the certi-         a propose–certify loop in which a determinis-
fier can check it. We instantiate PHACT in five           tic engine, not the model, holds the authority
domains spanning aerodynamics, DNA thermody-              to assert, with a three-valued output (certified,
namics, astrophysics, analog electronics, and col-        impossible, unknown) in which declining is a
loidal drug formulation, to show the architecture         valid verdict, not a failure mode. (ii) We iden-
is not tied to a single physical system. The pro-         tify the condition under which a certificate can
poser may be a hosted model, but the certifier is         be forged, namely a validator that lets the model
ordinary deterministic code. The certification step       supply the quantity under test, and replace it
therefore runs on commodity hardware and can              with a structural contract that derives the certi-
screen a candidate design against the governing           fied quantity from bound inputs. In the archived
physics before experimental effort or an expensive        adversarial evaluation this eliminates forged cer-
HPC allocation is committed. We release the full          tificates wherever tested: zero false certifications
system to that end.                                       across 80 adversarial trials spanning two models,
    That openness matters only if the certificate         two sampling temperatures (greedy and stochas-
itself can be trusted. The central contribution of        tic decoding), all five domains, and an injected
this paper is identifying the structural condition        engine fault. (iii) We show the structural contract
a propose–certify loop must satisfy to make that          does not make the loop impractically conserva-
possible. It is not enough to put a checker after         tive: on feasible goals the same model certifies
the model. If the checker asks the model to sup-          substantially more valid designs under PHACT
ply the quantity being certified (“here are the           than without an engine, confirming that the safety
masses; confirm the chirp mass is 50 M⊙ ”), then          constraint and design utility are compatible. (iv)
on a goal that should be refused, the model can           We show the safety guarantee is independent of
quietly change a quantity the prompt declared             the proposer: across models spanning an order of
fixed, hand the checker a self-consistent but off-        magnitude in scale, capability governs whether the
goal design, and receive a certificate for correct        loop produces a verdict at all, but never whether
physics that does not answer the question asked.          a verdict, once produced, can be wrong. We sepa-
We show this forgery is common, not hypothetical.         rate the contribution of verification from the mere
The fix is structural: the checker must derive the        ability to decline and the contribution of the lan-
certified quantity from bound inputs rather than          guage model from that of a closed-form solver,
accept it from the model. We formalize this with          delimit when the form of the feedback matters,
a structural contract for each domain: a directed         and state precisely the boundary of the guaran-
dependency graph in which quantities fixed by the         tee: soundness is relative to the engine’s model
goal enter as bound input nodes, any free design          of the physics. (v) We release the engines, struc-
variables occupy separate writable nodes, and the         tural contracts, goal corpus, and analysis as an
certified quantity is a derived leaf the model can-       open archive that regenerates every result with-
not write. On a fixed-system verification goal,           out credentials, a network, or a language model,
the bound nodes are read from the goal and are            so the certification, the part on which reliabil-
not writable by the model, so the model cannot            ity rests, runs on commodity hardware and lets
substitute a new mass pair (for this astrophysics         any scientist screen a design against governing
example, a different m1 , m2 ) and ask the checker        physics before committing experimental effort or
to certify a different system. Under this contract        expensive compute resources (e.g., HPC).
the forgery is impossible by construction, and we
confirm it holds across models, decoding temper-
atures, and even when the surrounding engine is           The framework
deliberately faulted.
                                                          PHACT has two parts kept separate. The first is a
                                                          language model: creative, general, unreliable. The
                                                          second is a deterministic certifier: narrow in scope,
                                                          but exact within the equations it implements.


                                                      2
Here the certifier is a domain-specific physics             asks the proposer for the controllable param-
engine; the architecture does not require it to be.         eters (for example, a flight path and speed
The model generates candidate designs; the engine           in aerodynamics, or a base sequence in DNA
evaluates them against the governing equations              thermodynamics where the target temperature
of the domain. Neither does the other’s job: the            is fixed by the goal) and computes for itself
model is never asked to compute physics, and the            whether the design satisfies the law. An answer-
engine is never asked to be creative.                       submitting validator additionally asks the pro-
                                                            poser to supply the quantity under test, e.g.,
The loop                                                    check chirp mass(m1 , m2 , claimed Mc ). The sec-
A user supplies a goal in natural language. The             ond form is natural for a “compute X ” goal but,
model proposes a fully specified design and calls           as we show, it is forgeable on a “this fixed system
the physics engine on it. The engine computes the           has property X ” goal. We therefore express each
relevant quantities exactly and returns a verdict.          domain as a structural contract with two kinds of
If the design satisfies all constraints, it is certi-       source nodes: bound nodes, fixed by the goal and
fied and the loop ends. If it does not, the engine          read-only to the proposer, and free nodes, which
returns the specific violations (which law was bro-         the proposer may choose. Derived nodes are com-
ken, what value was required, what the design               puted from those sources, and the outcome node
produced) and the model revises and calls again.            is the certified quantity (Fig. 2). For the guarantee
The loop ends in one of three outcomes: certi-              studied here, the decisive mechanism is the separa-
fied; impossible, when genuinely distinct attempts          tion between goal-bound inputs, which the model
all fail for the same physical reason; or unknown,          cannot change, and derived certified outputs,
when the goal lies outside the engine’s competence          which the model cannot supply. Concretely: bind
(Fig. 1). The second and third outcomes are the             the goal-fixed quantities as immutable inputs, let
system’s ability to decline, which is what makes            the model write only the free design variables,
its certificates reliable.                                  compute the quantity under test from the result-
                                                            ing graph, and never let the model write the value
                                                            being certified. On a goal such as “this binary
The engine, and the scope of its guarantee
                                                            has fixed masses m1 = 36 M⊙ , m2 = 29 M⊙ ; ver-
The engine contains no machine learning. It                 ify Mc = 50 M⊙ ”, the checker reads those masses
is ordinary code implementing peer-reviewed                 from the bound nodes and derives Mc itself; there
equations: the SantaLucia nearest-neighbor                  is no call in which the model can resubmit alter-
model for DNA melting temperature[1, 2], the                native masses and ask the checker to certify a
post-Newtonian expressions for gravitational-               different system. The engine performs determin-
wave inspiral[3], the resistor–capacitor transfer           istic forward evaluation over the graph, and this
function[4], and Derjaguin–Landau–Verwey–                   dataflow direction, together with the immutability
Overbeek theory for colloidal stability[5]. A               of the bound inputs, is the whole of the sound-
certificate is a statement about the engine’s               ness guarantee: it is interface design, not statistical
equations, not about physical reality in full: a            inference. Separately, on failure the engine uses
design that satisfies DLVO theory may still fail in         the same graph to return a targeted correction
a lab where hydration forces matter, and a chirp            Xi ← x∗i , the minimal change to an input node
mass certified by the post-Newtonian expansion              that would carry the outcome across the thresh-
may degrade near merger. Widening the fidelity              old. When the offending node is bound by the
of the underlying equations is a separate axis of           goal, the correction explains why the goal must
improvement from the certification contract itself,         be refused; when it is free, it guides the next pro-
and is what the third outcome, unknown, exists              posal. The role of the structural correction, as
to signal.                                                  we show below (Table 5), is to accelerate conver-
                                                            gence where the corrective inverse is coupled, not
Certification as derivation, not acceptance                 to secure soundness.
The pivotal design choice concerns who sup-
plies the quantity being certified. A validator can
take one of two forms. A design-only validator


                                                        3
     Decision loop         propose                         evaluate
                                                                                                              Certified
         Design goal                 Language model                       Physics engine
       natural language                 proposer                 derives; certifies or declines
                                                                                                         Impossible / unknown

                                         feedback: violated law / target fix


     Structural contract

              bound inputs                         design variables                          certified quantity
                read-only                              writable                                    derived




     Instantiated across five domains


           Drone              DNA                  Astro                                      Drug
                                                                      Electrical           formulation



Fig. 1 PHACT separates proposal from certification. A language model proposes candidate designs, but a deter-
ministic physics engine alone has the authority to certify, refuse as impossible, or abstain as unknown. On failure, the engine
returns the violated law and a targeted correction on the root-cause input. The structural contract binds goal-fixed inputs
as read-only, restricts the model to free design variables, and derives the certified quantity inside the engine. The same
contract pattern is then instantiated across five domains.


Results                                                                   (52%, 95% confidence interval (CI) 39–65%). On
                                                                          the 25 impossible goals it cannot decline, and on
We evaluate PHACT on five domains span-                                   7 of them (28%) it produced a design the engine
ning very different physics: drone aerodynamics,                          accepts post hoc, a confident, checker-passing
DNA hydrogel thermodynamics, gravitational-                               design for a goal that admits none. We count as
wave astrophysics, analog electrical filters, and                         a “hallucination” here only a design that passes
nanoparticle drug formulation (Fig. 3). For each                          the checker despite the goal being impossible, not
domain we authored ten feasible design goals                              merely a failure to refuse, so this is a conservative
and five physically impossible ones, requests that                        count. We state where those seven cases occur,
look reasonable but violate a hard physical limit.                        because the distribution matters: five of five in
The essential feature of the design is that the                           astrophysics, one in electrical, one in drone aero-
bare model and PHACT use the same language                                dynamics, none in DNA thermodynamics or drug
model (Gemini 2.5 Flash, greedy decoding); the                            formulation. The hallucination is concentrated in
only variable is the engine, so any difference is                         astrophysics, the most formula-saturated domain,
attributable to the loop. One accounting conven-                          where fluent recall most readily yields a plausible
tion is used throughout: feasible certification rates                     but off-goal answer. This is the failure PHACT
are reported over all authored feasible goals, with                       must remove.
infrastructure timeouts shown explicitly. A feasi-
ble goal wrongly declared impossible counts as a
                                                                          PHACT certifies valid designs and
failure. A run that ends with no terminal verdict
is a loop-fail, a property of the proposer, reported                      refuses impossible ones
separately.                                                               With the loop, the same model certifies 44 of
                                                                          50 feasible goals (88%, Wilson 95% CI 76–94%),
The bare model is unreliable, and                                         against the bare 52% (95% CI 39–65%), non-
                                                                          overlapping intervals (Table 1). The twelve-point
confidently so                                                            gap is not a soundness failure: not one of the non-
Without the engine, the model produces a phys-                            certifications is a false certificate. Every one of
ically valid design on only 26 of 50 feasible goals                       them is the system declining to assert rather than


                                                                      4
           Fixed-system goal: m1 = 36 M⊙ , m2 = 29 M⊙ ; verify Mc = 50 M⊙




                    Bare validator                                       Structural contract
               proposer can change inputs                                goal-fixed inputs are locked

                                                                        READ-
                     Model submits                                      ONLY
                   a different mass pair                             m1 = 36 M⊙               Engine
                         and claims                                                           derives
                      Mc = 50 M⊙                                        READ-               Mc = 28.1 M⊙
                                                                        ONLY

                    Validator checks                                 m2 = 29 M⊙
                  submitted inputs only


                         False pass                                                        Rejects claim


              Bare validator                         Structural                           All struct.
               10 / 15 forged                         contract                            conditions
                                                    0 / 15 forged                        0 / 80 forged
Fig. 2 A bare validator can certify the wrong system; the structural contract cannot. On a fixed-system
verification goal, an answer-submitting validator can be satisfied by a model that quietly substitutes a different mass pair
and submits a self-consistent claimed chirp mass. The structural contract binds the goal-fixed masses as read-only inputs
and derives the certified quantity inside the engine, so the model can neither change the system under test nor author the
certified value. The astrophysics close-up shows the attack mechanism that appears most often in our experiments: the bare
validator is forged in 10 of 15 greedy trials, whereas the structural contract is forged in none.


asserting falsely: two are infrastructure timeouts,               Table 1 PHACT feasible certification (Gemini
                                                                  2.5 Flash, temperature 0). “Certified” is verified-
three are loop-fails in which the model produced a                valid output. “Loop-fail” counts runs ending without
design, read the rejection, and then stalled with-                a terminal verdict; “wrong verdict” counts a feasible
out a verdict, and one is a feasible goal the model               goal declared impossible; “timeout” counts infrastruc-
conservatively, and wrongly, declared impossible.                 ture faults. PHACT certifies 44/50 (88%) versus the bare
                                                                  model’s 52%.
That last is the only substantive miss, and it
errs in the safe direction, refusing a goal it could              Domain               Cert. Loop-fail Wrong Timeout
have certified rather than certifying one it should
                                                                  Drone                 8/10          0       0          2
have refused. The loop errs toward declining, not                 Biochem               8/10          2       0          0
toward asserting. This is by design and not a                     Astrophysics          9/10          1       0          0
defect to be optimized away: a system constrained                 Electrical           10/10          0       0          0
to certify every feasible goal would be a system                  Drug formulation      9/10          0       1          0
that must always answer, and a system that must                   Overall             44/50           3       1          2
always answer is exactly the bare model that hal-
lucinates. The rate that matters is the rate at
which a granted certificate is true, and that rate is
100%; the feasible certification rate is the recover-
able remainder. Correction is fast: across certified             median of one or two engine calls, so the loop is a
runs the model reaches a verified design in a                    short conversation, not a search.


                                                             5
                                                     DNA                                      Astrophysics
                Drone
                                                        ∆H                                           (m1 m2 )3/5
          T = CT ρn2 D4                         Tm =                                      Mc =
                                                     ∆S + R ln cT                                   (m1 +m2 )1/5
         Size rotors for tar-                      Design strand sta-                        Verify chirp mass
          get hover thrust                          ble at target Tm                          of fixed binary




                                 Electrical                          Drug formulation
                                        1                                      A
                                fc =                                 Vmin = −    + κ−1
                                      2πRC                                    6D
                               Size RC filter for                   Formulate colloid stable
                                cutoff frequency                      against aggregation


Fig. 3 PHACT spans five domains with very different governing physics. Each domain is instantiated as a
deterministic engine implementing a peer-reviewed equation. The engine receives a proposed design, evaluates it against
the governing law, and returns certified, impossible, or unknown. Goals range from feasible design (size a filter, design a
strand) to fixed-system verification (confirm a binary’s chirp mass), the latter being the category where a bare validator is
forgeable and the structural contract is not.


   On the impossible goals, PHACT refuses                            This forgery is not hypothetical, and not rare.
where the bare model hallucinates, but the man-                  We demonstrate the attack mechanism in astro-
ner of refusal is the subject of the next section,               physics, the domain where answer-submitting val-
because it exposes the paper’s central point: a                  idation is most natural (the goal fixes two masses
checker is only as trustworthy as the contract by                and asks to verify a derived quantity) and where
which it certifies.                                              the substitution is most tractable (the chirp-mass
                                                                 formula is closed-form, so the forging trajectory is
                                                                 short and deterministic); it is therefore the domain
                                                                 where the bare contract is most exposed and the
                                                                 structural fix most testable. On three adversarial
A certificate can be forged, unless                              astrophysics goals run five times each, an answer-
the checker derives it                                           submitting (“bare”) validator was forged on ten
Consider an impossible goal that fixes a system                  of fifteen trials under greedy decoding (Table 2,
and asks to verify a property: “a binary has fixed               row S1). We then stress-tested derived certifica-
masses m1 = 36 M⊙ , m2 = 29 M⊙ ; verify its                      tion in the archived structural conditions. At a
chirp mass is 50 M⊙ ” (the true value is 28.1 M⊙ ).              high decoding temperature, where the proposer
With an answer-submitting validator, the model                   explores far more trajectories, the bare validator
can satisfy the checker by quietly changing a                    is still forged (S2, 6/15) while the SCM-exclusive
supposedly-fixed mass to a pair that genuinely has               structural check yields zero false certifications (S3,
chirp mass 50 M⊙ ; the engine then certifies cor-                0/15). And when we deliberately reinstate a his-
rect physics for a design other than the one that                torical engine bug that latches a certificate on
was asked. The instruction “you may not change                   any passing intermediate check, a fault that lets
the mass” lives only in the prompt and is invisible              the bare contract forge even at greedy decoding
to the tool.

                                                             6
(S4a, 3/15), the derived checks still forge noth-             (6/15) (greedy decoding deterministically com-
ing, whether the structural tool is merely available          mits to the substituting trajectory, whereas sam-
(S4b, 0/15) or made exclusive (S4c, 0/15).                    pling sometimes diverts the model into stalling)
    The astrophysics cells are where we exhibit               though at this sample size the two intervals over-
the attack in close-up; the safety result itself              lap and we report the direction, not a significant
is broader. Across the full impossible-goal suite             difference. The point that survives is that the vul-
(all five domains, 25 goals), the bare answer-                nerability is acute exactly at the greedy decoding,
submitting validator forges two certificates for              with which models are usually run, not only in
Gemini and one for Llama 3.3 70B (rows E1),                   a high-temperature tail. Second, the structural
while the SCM-exclusive structural contract forges            contract sometimes pays for its safety in feasible
zero for both models across all five domains                  certification rate: when forced through the derived
(rows E2; Fig. 4). The vulnerability is therefore             check the proposer occasionally stalls without
not specific to astrophysics; astrophysics is merely          issuing a clean refusal (a loop-fail) rather than
where the closed-form substitution makes the forg-            certifying. It never forges, but it does not always
ing trajectory shortest and so where the bare                 answer. This is the right trade for a safety prop-
contract fails most often. The guarantee is a prop-           erty: silence is recoverable, a forged certificate is
erty of the interface, not of the domain: any goal            not.
that fixes inputs and asks to verify a derived                    The conclusion is the paper’s thesis made
quantity is forgeable under an answer-submitting              concrete. A tool that checks correctness can be
validator and non-forgeable once the quantity is              satisfied off-goal; a contract that fixes which quan-
derived, because the value that would be forged is            tities are inputs and which are derived cannot,
computed, not accepted. The empirical trials con-             because the value that would be forged is com-
firm this construction on the instances that most             puted, not accepted. Certification authority must
invite it; they do not establish it.                          not pass through the proposer.
    The contrast is one-sided. Pooled across the
three bare close-up cells (S1, S2, S4a), the answer-          The safety guarantee transfers across
submitting contract is forged on 19 of 45 adver-              model families; feasible certification
sarial trials; pooled across the three structural
close-up cells (S3, S4b, S4c), the derived contract
                                                              rate scales with proposer capability
is forged on none of 45. We report this contrast              To test whether these findings are an artifact of
descriptively rather than as a significance test,             one model, we repeat the full evaluation with
because the structural guarantee is a property of             Llama 3.3 70B, an unrelated open model from
the interface, not a statistically inferred difference:       a different family, served via the same Vertex
the certified quantity is computed and so cannot              AI at temperature 0. The central result trans-
be authored by the model, whatever the decoding               fers exactly: under a bare validator the contract is
or the sampler. The role of the structural trials             forged for Llama as it is for Gemini (1/25), and the
is therefore to check the implementation under                structural contract yields zero false certifications
adversarial conditions, not to estimate a forgery             for both (Table 3). The engine’s authority to assert
rate. Pooled across every SCM-exclusive condition             is independent of which model proposes. What
in this work, the two five-domain suites (Gemini,             scales with proposer capability is the feasible cer-
0/25; Llama, 0/25) together with the astrophysics             tification rate: Llama 3.3 70B certifies only 33 of
close-up at high temperature (0/15) and under                 50 feasible goals against Gemini’s 44. The gap is
the injected fault (0/15), the structural contract            almost entirely loop-fail : on multi-tool domains
yields zero forged certificates observed in 80                (astrophysics, electrical, drug formulation) Llama
adversarial trials (25 + 25 + 15 + 15).                       reads the engine’s correction and restates the right
    We report on two honest qualifications. First,            value in prose rather than resubmitting a tool call,
the bare contract appears to be forged more at                ending with no verdict. The degradation is uneven:
greedy decoding (10/15) than at high temperature              electrical collapses (5/10 feasible certified), while
                                                              drone and biochem match Gemini exactly; it is a
                                                              property of the proposer, not the engine. When
                                                              a weaker proposer stalls, the system goes silent


                                                          7
Table 2 The structural contract cannot be forged. “Bare” validators let the model supply the certified quantity;
SCM rows derive it from the fixed inputs. “False cert.” is a forged certificate, a physically impossible goal certified instead
of refused. Bare rows report Wilson 95% confidence intervals; structural rows are reported as implementation checks and
therefore show only whether any forged certificate was observed. Rows S1–S4c are the archived astrophysics close-up
ablation (three goals, five trials each, 15 per row, Gemini 2.5 Flash): S1, S2, and S4a are bare answer-submitting conditions;
S3 and S4c are SCM-exclusive conditions; S4b is an SCM-available variant under the latch fault. Rows E1/E2 are the
full impossible-goal suites (all five domains, 25 goals per model), with E1 the bare validator and E2 the SCM-exclusive
structural contract. The bare contract is forged in every bare row; every structural row yields zero false certifications.

  Row      Scope                                        Condition                  Contract      False cert. / implementation check
  S1       astro close-up                               temperature 0              bare                            10/15 [42–85%]
  S2       astro close-up                               temperature 1              bare                             6/15 [20–64%]
  S3       astro close-up                               temperature 1              SCM excl.                  0/15 (none observed)
  S4a      astro close-up                               temp. 0, latch fault       bare                              3/15 [7–45%]
  S4b      astro close-up                               temp. 0, latch fault       SCM avail.                 0/15 (none observed)
  S4c      astro close-up                               temp. 0, latch fault       SCM excl.                  0/15 (none observed)
  E1       5 domains (Gemini)                           temperature 0              bare                              2/25 [2–25%]
  E2       5 domains (Gemini)                           temperature 0              SCM excl.                  0/25 (none observed)
  E1       5 domains (Llama)                            temperature 0              bare                              1/25 [1–20%]
  E2       5 domains (Llama)                            temperature 0              SCM excl.                  0/25 (none observed)


                                              Bare validator            Structural contract
             False certification rate




                                        80%
                                               67%
                                        60%

                                                               40%
                                        40%

                                                                               20%
                                        20%
                                                                                                 8%
                                                                     0%                0%             0%        4% 0%
                                        0%
                                               Astro              Astro               Astro      5 domains       5 domains
                                              bare t0            temp. 1           latch fault   (Gemini)         (Llama)
Fig. 4 Archived adversarial conditions in the forgeability evaluation. Red bars are bare answer-submitting valida-
tors; green bars are derived structural checks. The leftmost bar is the greedy-decoding astrophysics close-up bare condition
(S1). The next pairs compare the archived high-temperature close-up rows (S2 vs. S3), the latch-fault close-up rows (S4a
vs. S4c), and the full five-domain suites for Gemini and Llama (E1 vs. E2). The SCM-available latch variant (S4b, 0/15) is
reported in Table 2. The structural rows are zero wherever tested; the bare rows are non-zero in every archived condition
shown.


rather than wrong. Silence is recoverable; a false                                 the proposer is an order of magnitude smaller,
certificate is not.                                                                does the system merely become less useful, or
                                                                                   does it become unsafe? To probe this we ran
                                                                                   Llama 3.1 8B, served locally on-device via Ollama,
A capability-floor probe: a weak                                                   on the adversarial impossible-goal suite (Table 4).
proposer is unusable but not unsafe                                                The result isolates the central asymmetry between
                                                                                   capability and safety. On usefulness, 8B is at the
The cross-model comparison above tests two capa-
                                                                                   floor: it never closes the loop on a single impossible
ble proposers. A separate question is what hap-
pens at the floor of the capability ladder: if


                                                                               8
  Table 3 Cross-model comparison: the safety                       Table 4 Capability-floor probe (Llama 3.1 8B, on-
  guarantee transfers between model families.                      device via Ollama). The adversarial impossible-goal
  Two proposers run end to end through both the                    suite (all five domains, five goals each, 25 total), run under
  bare and the structural contract. Rows compare                   the bare answer-submitting validator, the condition that
  bare feasible validity, PHACT feasible certification,            forges for the larger models. Every trial ends in loop-
  and false certifications on impossible goals under a             closure failure: the model never issues a terminal verdict,
  bare validator versus the structural contract (tem-              so it never certifies, never refuses, and never forges. Use-
  perature 0). Wilson 95% confidence intervals are                 fulness is at the floor; safety is intact for the trivial reason
  reported for the empirical-rate rows; the structural             that the model never acts. This isolates the asymmetry:
  zero rows are reported as implementation checks                  producing a verdict is a capability the proposer may lack,
  and therefore show only whether any forged cer-                  but forging one requires a verdict it never produces.
  tificate was observed. The key contrast is the two
  false-certification rows: a bare validator that accepts           Domain               Refused False cert. Loop-fail          n
  the model-supplied value is forged for both models;
  the structural contract, which derives the certified              Drone                        0            0            5    5
  quantity from the fixed inputs, yields zero false certi-          Biochem                      0            0            5    5
  fications for both. Feasible certification rows use all 50        Astrophysics                 0            0            5    5
  feasible goals in the denominator; false-certification            Electrical                   0            0            5    5
  rows use all 25 impossible goals. A capability-floor              Drug formulation             0            0            5    5
  probe (Llama 3.1 8B) is reported separately in                    Overall                      0        0/25           25 25
  Table 4.

   Metric                     Gemini 2.5        Llama 3.3
   Bare feasible valid       52% [39–65]     52% [39–65]
   PHACT feasible cert.      88% [76–94]     66% [52–78]           once produced, can be wrong, because the author-
   False cert., bare        2/25 [2–25%] 1/25 [1–20%]              ity to certify never passed through the proposer. A
   False cert., struct.     0/25 (none) 0/25 (none)                loop-closure supervisor (a model-agnostic compo-
                                                                   nent that detects a stalled turn after an unsatisfied
                                                                   rejection and re-prompts the tool call) would plau-
                                                                   sibly recover much of the lost feasible certification
                                                                   rate for weaker proposers without touching the
goal, and all 25 trials end without a terminal ver-                engine’s authority. We have not implemented or
dict, the model reading the engine’s exchange and                  evaluated it; it is a clearly bounded direction for
then stalling in prose. On safety, it is nonetheless               future work.
perfect: it forges zero certificates. But the reason
is the point. It does not forge because the contract
caught it; it forges nothing because it never issues               What the verification and the
a verdict at all. A model too weak to be useful is,
for exactly that reason, too weak to be dangerous:
                                                                   language model each contribute
the only way to forge a certificate is to act, and                 Two fairness baselines isolate where the value of
the floor model does not act. We report this as a                  the system actually lies, and both make the con-
probe of the boundary, not as a third safety data                  tribution of PHACT’s components more precise
point: 8B was run under the bare validator only,                   rather than larger.
the same condition that forges for the larger mod-                      The first asks whether PHACT’s safety advan-
els, so its zero is the strongest possible statement               tage is merely that PHACT is allowed to decline.
of the asymmetry; under the bare validator, the                    We therefore re-ran the bare model with a prompt
8B model yields no forged certificates even where                  that explicitly permits it to answer “impossible”
the larger models do.                                              when no valid design exists (no engine, otherwise
    Taken together with the cross-model result,                    identical). Permitting refusal does reduce false cer-
the capability ladder reads cleanly from top to                    tifications: the bare-but-permitted model falsely
bottom (Fig. 5): Gemini closes the loop reliably,                  certifies 2 of 25 impossible goals rather than 7
Llama 3.3 70B stalls on the harder multi-tool                      of 25 when forbidden. But it does not eliminate
domains, and Llama 3.1 8B never closes it at all,                  them. Under the structural contract, false certifi-
yet neither of the three ever forges a certificate.                cations drop to zero for every model tested. The
Capability governs whether the system produces                     prompt cannot supply what the contract provides:
a verdict; it has no bearing on whether a verdict,                 the permitted bare model has no way to verify


                                                               9
                                       (a) Feasible certification rate                                                       (b) Safety (bare validator)




                                                                          False certification rate (bare validator)
                                100%                                                                                  100%
                                                            88%
  Feasible certification rate



                                80%                                                                                   80%
                                                   66%
                                60%                                                                                   60%


                                40%                                                                                   40%


                                20%                                                                                   20%
                                                                                                                                                 8%
                                         n/a                                                                                  0%†      4%
                                 0%                                                                                    0%
                                        Llama     Llama   Gemini                                                             Llama     Llama   Gemini
                                        3.1 8B   3.3 70B 2.5 Flash                                                           3.1 8B   3.3 70B 2.5 Flash
Fig. 5 Capability governs feasible certification rate but not safety. (a) Feasible certification rate rises with
proposer capability: Llama 3.1 8B never closes the loop (n/a; not run on feasible goals), Llama 3.3 70B reaches 66%, and
Gemini 2.5 Flash reaches 88%. (b) False certification rate under the bare validator: 4% for Llama 3.3 70B and 8% for Gemini.
Llama 3.1 8B († ) shows 0% not because the contract caught it but because it never issues a verdict at all: every trial ends in
loop-closure failure. For Gemini and Llama 3.3 70B, the structural contract yields 0% false certifications. Capability scales
feasible certification rate; the structural contract, not the proposer, determines whether a verdict once issued can be wrong.


its own refusals, still falsely certifies goals it can-                                                using an unreliable proposer in the open-ended
not catch, and over-refuses four feasible goals it                                                     setting where no solver exists, with the closed-
should have designed. None of its answers are                                                          form domains serving as a control that confirms
checked. PHACT’s value is therefore not that it                                                        the engine, not the model, is the source of physical
can decline, which a prompt can approximate, but                                                       correctness.
that every certificate it issues is verified and, under
the structural contract, cannot be forged.
    The second baseline asks what the language                                                         When the form of the feedback
model contributes that a solver does not. For
                                                                                                       matters
the domains whose design is a direct inversion
of a closed-form law, the resistor–capacitor cut-                                                      The engine returns, on failure, a violation report
off R = 1/(2πfc C ) and the chirp mass Mc =                                                            and a targeted correction. Does a richer, struc-
(m1 m2 )3/5 /(m1 + m2 )1/5 , a thin deterministic                                                      tured correction help the model converge faster?
solver with no language model certifies every tar-                                                     We answer with a controlled ablation holding
get we tried (7 of 7 RC filters, 7 of 7 chirp masses).                                                 the model, goals, and physics fixed, varying only
Where a closed form exists, the physics needs no                                                       the feedback form (weak: violation magnitude
model, and a parser plus the engine would suffice.                                                     only; strong: closed-form correction; structural:
We state this plainly because it locates the lan-                                                      the root-input correction with the dependency
guage model’s actual marginal contribution: not                                                        path), across three domains (Table 5). The answer
the physics, which a solver computes exactly, but                                                      is conditional. On the RC filter, whose correc-
the natural-language front end and the general-                                                        tive inverse is closed-form (R = 1/(2πfc C )), all
ity of operating across five unrelated domains,                                                        three forms converge in one to one-and-a-half iter-
from DNA thermodynamics to colloidal stabil-                                                           ations, the model computes the fix itself and the
ity, without per-domain solver code. The value of                                                      feedback form is immaterial. On drug formulation,
PHACT is best understood as a method for safely                                                        whose feasible region is large, the first proposal
                                                                                                       usually certifies and again the form barely matters


                                                                         10
                                                                      Neurosymbolic systems and structured
Table 5 Feedback-form ablation (Gemini 2.5 Flash;                     verification
mean iterations to certify). Weak: violation magnitude
only. Strong: closed-form correction. Structural: root-input          Combining neural generation with symbolic rea-
correction with dependency path. Feedback form matters                soning is a long-standing approach[14, 15]. We
only for the coupled domain (DNA), where no closed-form
                                                                      take a known structural model of a physical mech-
inverse exists; for a closed-form inverse (RC) or a large fea-
sible region (drug) it is immaterial.                                 anism, express it as a directed dependency graph
                                                                      whose input/output structure makes certification
 Domain (correction structure)      Weak Strong Struct.               non-forgeable, and use that graph to generate
 RC filter (closed-form inv.)        1.00      1.50     1.10          targeted corrections when a design fails. The con-
 Drug form. (large region)           1.20      1.20     1.00          tribution is in how the graph is wired relative to
 DNA dual-constraint (coupled)       2.50      2.22     1.70          the proposer, not in inferring the graph from data;
                                                                      we take the physical laws as given and use their
                                                                      dependency structure as an interface contract.

(1.20 vs 1.00 iterations). Only on DNA dual-
                                                                      Hallucination, abstention, and
constraint design, where two coupled constraints
                                                                      physics-informed learning
share parents and no closed-form inverse exists,
does structural feedback meaningfully reduce iter-                    Models produce fluent false statements[16, 17],
ations, from 2.50 (weak) to 1.70, a roughly 30%                       motivating      calibrated    abstention[18,      19];
improvement, with strong feedback intermediate                        PHACT’s three-valued output is a hard form of
at 2.22. Structural feedback earns its complexity                     abstention grounded in an external check rather
precisely when the corrective inverse requires joint                  than self-estimated confidence. Physics-informed
optimization the model cannot perform unaided;                        neural networks fold the governing equations into
elsewhere, the choice is immaterial.                                  the training loss as a soft penalty[20–22]; there
                                                                      the law is internalized and can still be violated at
                                                                      inference, and the network always emits a value.
Related work                                                          PHACT keeps the law outside the model as a
                                                                      hard check at inference: the model’s only author-
Tool-augmented and program-aided models                               ity is to propose, never to certify. The distinction
Language models can call external tools or offload                    is not which approach knows more physics but
computation to a code interpreter[6–9]. These ver-                    where the law sits relative to the output: inside
ify the execution of code, not the physical admissi-                  the model as a training signal, or outside it as a
bility of a design; a program that runs cleanly can                   runtime gate. The two are complementary rather
still describe a device that violates physical law.                   than competing. A physics-informed surrogate
PHACT’s validators check the latter, and our cen-                     trained on a domain whose governing law has no
tral finding, that the validator must derive rather                   closed form could slot directly into PHACT as
than accept the certified quantity, is a constraint                   the engine[20], extending certification to regimes
on how such a tool must be wired, not merely that                     where ordinary code cannot compute the forward
one is present.                                                       model exactly. In that configuration it is still the
                                                                      certification contract, not the soft constraint, that
Self-correction and verification                                      removes the confident assertion of the impossible;
                                                                      the surrogate supplies the forward model, and the
A model can criticize and revise its own output[10,
                                                                      contract determines who may assert the result.
11], and external verifiers can score candidates[12].
Self-verification inherits the blind spots that pro-
duced the error[13]; PHACT’s verifier is a deter-                     Discussion
ministic engine with which the model cannot
argue. The forgery we identify is precisely a case                    The improvement we find most significant is not
where a naive external verifier is still defeated (not                its size but its source, and what it costs to make
by being wrong, but by being asked the wrong                          it sound. The bare model and PHACT are the
question) which is why the input/output contract                      same model; we trained nothing and collected no
matters.                                                              data. We added a loop in which the model may not


                                                                 11
assert a quantity until a deterministic engine has           the five domains here all have closed-form gov-
confirmed it. That single change moves the sys-              erning equations, which is why certification is fast
tem from one that is wrong roughly half the time,            and exact. The architecture places no constraint
and confidently designs the impossible, to one that          on this: any deterministic forward model, includ-
certifies the large majority of valid designs and            ing a physics-informed surrogate for a domain
refuses the rest.                                            whose law has no closed form, can serve as the
    But a certificate is only as good as the con-            engine. The unknown verdict is the system’s hon-
tract that issues it. The central finding is how that        est response when the engine’s competence runs
contract can be forged and what closes the hole.             out, and widening that competence is a sepa-
When the validator asks the proposer to supply               rate axis from the certification contract itself,
the quantity under test, the proposer can satisfy it         one that the community can pursue domain by
by changing a quantity the prompt declared fixed;            domain without changing the safety structure.
the engine then certifies correct physics for the            The one boundary that is not an evaluation limit
wrong design. We showed this occurs readily in the           but a property of any PHACT certificate is that
domains most susceptible to it, and that it is worst         soundness is relative to the engine’s model of the
under the greedy decoding with which models are              physics: the certificate says this design satisfies
usually run. The fix is structural and, once seen,           these equations, not that it satisfies physical real-
simple: derive the certified quantity from the fixed         ity in full. We regard this as the correct scope for
inputs so the proposer cannot write it. Under this           any computable certificate, and stating it explic-
contract, the forgery is impossible by construction,         itly is what makes the guarantee trustworthy.
and the empirical results bear it out across mod-                The certification path contains no machine
els, temperatures, and even a deliberately faulted           learning and no proprietary model: the engines are
engine, zero forged certificates in eighty adversar-         ordinary code, and the released archive regener-
ial trials. The guarantee is structural rather than          ates every result on commodity hardware without
statistical, which is why it does not depend on              credentials, a network, or a language model. A stu-
how the model is decoded: the authority to assert            dent or a working scientist can put a candidate
never passes through the sampler. This sharpens              design, a DNA sequence intended to be stable at
a familiar intuition. Reliability is not only a prop-        a target temperature, a filter sized for a cutoff, a
erty of how good the predictor is; it is a property          nanoparticle formulation meant to resist aggrega-
of what the predictor is allowed to assert without           tion, through the same governing physics we use
a check it cannot author.                                    here, and learn whether it is admissible, infea-
    The five domains and three proposers evalu-              sible, or outside the engine’s competence, before
ated here are not the limits of the architecture;            committing bench time or an HPC allocation to
they are a first instantiation of it with closed-            it. The system does not replace high-fidelity sim-
form engines. Each axis admits direct extension.             ulation; it screens against the first-principles law
On the proposer side, the experiments show that              cheaply, so that expensive resources are spent only
loop-closure is a meta-cognitive capacity sepa-              on designs that have already cleared it.
rable from physical knowledge: Llama 3.3 70B                     The separation of authority instantiated here,
correctly parses the engine’s correction and some-           a learned proposer paired with a deterministic
times restates the right value, yet fails to resubmit        arbiter the proposer cannot override, may gen-
it as a tool call, ending with no verdict. The               eralize beyond static physical design. We make
safety property is untouched by this failure mode,           no claim about real-time control or perception,
the model never forges, and it points to a con-              which this evaluation does not touch; but the same
crete next step that does not require a better               input/output contract that prevents forgery on a
model: a model-agnostic loop-closure supervisor              fixed-mass chirp-mass goal is the same contract
that detects a stalled natural-language turn after           one would want wherever a model’s output feeds
an unsatisfied rejection and re-prompts the tool             an external check it cannot author.
call. With capable proposers, the loop already                   Reliable physical reasoning is not a property
closes reliably; the supervisor is the path to mak-          of a better predictor; it is a property of a predic-
ing that hold for smaller, fully open models and             tor placed inside a loop whose verdict it cannot
to broadening access further. On the engine side,            author. PHACT is one way to build that loop.


                                                        12
Methods                                                    the certified quantity; the edges are the same
                                                           closed-form equations as the validator, verified to
Models and decoding                                        reproduce the bare-tool values exactly. For fixed-
The primary proposer, in both the bare and                 system verification goals, the bound quantities are
PHACT conditions, is Gemini 2.5 Flash via Ver-             read from the goal state and are not accepted
tex AI, decoded at temperature 0; the same model           as model arguments. The certification contract
is used for both conditions so that the engine             is selected by tool availability: a goal that fixes
is the only variable. The cross-model experiment           a system and asks to verify a derived property
uses Llama 3.3 70B via Vertex AI Model-as-a-               is certified only through the structural (derive-
Service, also at temperature 0; its bare baseline          from-inputs) check, with the answer-submitting
uses the same API. A capability-floor proposer,            validators removed and the fixed quantities bound
Llama 3.1 8B (an order of magnitude smaller),              outside the model’s control, so the proposer can-
was run on the impossible-goal suite served locally        not change the system under test or supply the
via Ollama, entirely on-device with no external            value under test. The forgeability ablation toggles
API. The high-temperature ablation repeats the             this single variable, answer-submitting validators
adversarial impossible suite at temperature 1. No          (“bare”) versus the structural check, on identical
model was fine-tuned. Determinism at tempera-              goals.
ture 0 was confirmed by byte-identical tool-call
trajectories on repeated runs. The proposer is             Goals and scoring
orchestrated with the Google Agent Develop-
                                                           For each domain we authored ten feasible and
ment Kit, which lets the model decide when to
                                                           five impossible goals; an impossible goal fixes an
invoke tools; non-Gemini models route through
                                                           over-constrained input set that admits no valid
the ADK’s LiteLLM backend. A run ending in
                                                           design. The goals, engines, and feasible/impossible
error is classified at source as an infrastructure
                                                           boundary are author-defined; there is no held-out
fault (rate limit, authentication, server 5xx, or
                                                           external goal set, so the evaluation is a closed-
stream timeout), which is retried and never scored,
                                                           world test of the architecture rather than a bench-
or a loop-closure failure (no terminal verdict),
                                                           mark against an independent standard, and the
which is a property of the proposer and is reported
                                                           rates should be read in that light. A bare answer
as such. We evaluate three models in total; broader
                                                           is scored by parsing its parameters and evaluat-
generality would be firmer with additional capable
                                                           ing them with the same engine. A PHACT run is
proposers run end to end.
                                                           scored by its returned outcome. For feasible goals,
                                                           success is certification, and feasible certification
The engine and the structural contract                     rates are reported over all 50 authored goals, with
                                                           timeouts shown explicitly rather than excluded.
Each domain engine is a deterministic imple-
                                                           For impossible goals, success is the verdict impos-
mentation of its governing equations, containing
                                                           sible. Infrastructure faults are retried and not
no machine learning, calibrated against published
                                                           scored; wrong verdicts and loop-fails are reported
values (DNA melting temperature within ±1 ◦ C
                                                           separately and never counted as successes; a false
of SantaLucia 1998; GW150914 chirp mass within
                                                           certification on an impossible goal is counted as a
±1 M⊙ of the LIGO/Virgo catalog) to confirm
                                                           failure to refuse, never excluded.
correct implementation, a method check, not a
performance result. We do not score the system
on famous published quantities, because a model            Statistics
trained on the reporting papers recalls rather than        Wilson score 95% confidence intervals are reported
computes them; all performance claims rest on              for the genuinely empirical-rate rows, where a rate
design and impossible goals where memorization             is being estimated from finite samples. We delib-
cannot help. For each domain we declare a struc-           erately report the central forgeability contrast
tural contract: a directed dependency graph with           descriptively rather than through a significance
two kinds of input nodes, goal-bound quantities            test. The structural contract’s zero forgery result
and proposer-controlled design variables, followed         is a property of the interface, the certified quan-
by derived quantities and an outcome node for              tity is computed and cannot be authored by the


                                                      13
model, not a difference inferred from sampling; a           Funding
p-value would mischaracterize a by-construction
guarantee as a statistical one. The structural zero         This work was funded entirely by Heysuvi Labs,
rows are therefore presented as implementation              LLC. No external grant funding was received.
checks under the archived adversarial conditions:
no forged certificate was observed. For the bare            Competing interests
contract, which is a genuine empirical rate, we
report the per-condition proportions and their              NV and IDS are employees of Heysuvi Labs, LLC,
intervals. Given the small per-cell sizes (n = 15 to        which funded this work. The authors declare no
50), we read the intervals, not point estimates, as         other competing interests.
the result, and we flag where two intervals overlap
(so a difference is directional rather than signifi-        Ethics approval and consent to
cant) rather than asserting a difference the data           participate
do not support.
                                                            Not applicable.

Reproducibility                                             Consent for publication
The complete framework is released as a pub-
                                                            Not applicable.
lic archive: the physics engines, the struc-
tural contracts (the input/output dependency
graphs), the full goal corpus, the experiment               Data and code availability
driver, the engine-calibration scripts, and a table-
                                                            The goal corpus, engine outputs, and all data
regeneration pipeline. The archive is the sound-
                                                            required to reproduce the tables and figures in
ness claim made checkable: every table in this
                                                            this paper are available at https://github.com/
paper regenerates from the archived model out-
                                                            nakulvyas21/phact-reproducibility. The physics
puts and the deterministic engines without creden-
                                                            engines, structural contracts, experiment driver,
tials, network, or a language model, so a reader
                                                            and table-regeneration pipeline are publicly
can reproduce the full analysis pipeline and verify
                                                            available at https://github.com/nakulvyas21/
the physics exactly, end to end, with no API key.
                                                            phact-reproducibility. A production user inter-
What the archive does not reproduce is the elic-
                                                            face based on the PHACT workflow is available
itation of model behavior, which depends on the
                                                            at https://heysuvi.com/ae210. Every result in
hosted models and provider-side non-determinism;
                                                            this paper regenerates from the archived outputs
the certificate-checking pipeline, which is where
                                                            and the deterministic engines without credentials,
soundness lives, is fully deterministic and fully
                                                            a network connection, or a language model.
reproduced.
                                                            Author contributions
Acknowledgements                                            NV conceived and designed the study, developed
                                                            the framework and physics engines, ran the exper-
NV and IDS thank the Karlsruhe Institute of                 iments, and wrote the manuscript. IDS provided
Technology (KIT) and the University of Stuttgart            scientific guidance, reviewed and approved the
for institutional support. IDS further acknowl-             final manuscript.
edges support from KIT’s Excellence Strategy via
the Young Investigator Group Preparation Pro-               References
gram. Heysuvi Labs, LLC operated in part under
a technology transfer initiative of the University           [1] SantaLucia, J.: A unified view of polymer,
of Stuttgart during the development of this work.                dumbbell, and oligonucleotide DNA nearest-
This work also benefited from consulting and                     neighbor thermodynamics. Proceedings of
in-kind support provided through the NVIDIA                      the National Academy of Sciences 95(4),
Inception and Google for Startups programs.                      1460–1465 (1998)


                                                       14
 [2] Owczarzy, R., You, Y., Moreira, B.G., Man-              [11] Shinn, N., Cassano, F., Gopinath, A.,
     they, J.A., Huang, L., Behlke, M.A., Walder,                 Narasimhan, K., Yao, S.: Reflexion: Language
     J.A.: Effects of sodium ions on DNA duplex                   agents with verbal reinforcement learning. In:
     oligomers: improved predictions of melting                   Advances in Neural Information Processing
     temperatures. Biochemistry 43(12), 3537–                     Systems, vol. 36 (2023)
     3554 (2004)
                                                             [12] Cobbe, K., Kosaraju, V., Bavarian, M., Chen,
 [3] Abbott, B.P., et al.: Observation of grav-                   M., Jun, H., Kaiser, L., Plappert, M., et
     itational waves from a binary black hole                     al.: Training verifiers to solve math word
     merger. Physical Review Letters 116(6),                      problems. arXiv preprint arXiv:2110.14168
     061102 (2016)                                                (2021)

 [4] Horowitz, P., Hill, W.: The Art of Electron-            [13] Huang, J., Chen, X., Mishra, S., Zheng, H.S.,
     ics, 3rd edn. Cambridge University Press,                    Yu, A.W., Song, X., Zhou, D.: Large lan-
     Cambridge, UK (2015)                                         guage models cannot self-correct reasoning
                                                                  yet. In: International Conference on Learning
 [5] Israelachvili, J.N.: Intermolecular and Sur-                 Representations (2024)
     face Forces, 3rd edn. Academic Press, Ams-
     terdam (2011)                                           [14] Garcez, A.d., Gori, M., Lamb, L.C., Ser-
                                                                  afini, L., Spranger, M., Tran, S.N.: Neural-
 [6] Schick, T., Dwivedi-Yu, J., Dessı̀, R.,                      symbolic computing: An effective method-
     Raileanu, R., Lomeli, M., Hambro, E., Zettle-                ology for principled integration of machine
     moyer, L., Cancedda, N., Scialom, T.: Tool-                  learning and reasoning. Journal of Applied
     former: Language models can teach them-                      Logics 6(4), 611–632 (2019)
     selves to use tools. In: Advances in Neu-
     ral Information Processing Systems, vol. 36             [15] Marcus, G.: The next decade in AI: Four
     (2023)                                                       steps towards robust artificial intelligence.
                                                                  arXiv preprint arXiv:2002.06177 (2020)
 [7] Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I.,
     Narasimhan, K., Cao, Y.: ReAct: Synergizing             [16] Ji, Z., Lee, N., Frieske, R., Yu, T., Su, D., Xu,
     reasoning and acting in language models. In:                 Y., Ishii, E., Bang, Y.J., Madotto, A., Fung,
     International Conference on Learning Repre-                  P.: Survey of hallucination in natural lan-
     sentations (2023)                                            guage generation. ACM Computing Surveys
                                                                  55(12), 1–38 (2023)
 [8] Gao, L., Madaan, A., Zhou, S., Alon, U., Liu,
     P., Yang, Y., Callan, J., Neubig, G.: PAL:              [17] Maynez, J., Narayan, S., Bohnet, B., McDon-
     Program-aided language models. In: Interna-                  ald, R.: On faithfulness and factuality in
     tional Conference on Machine Learning, pp.                   abstractive summarization. In: Proceedings
     10764–10799 (2023)                                           of the 58th Annual Meeting of the Asso-
                                                                  ciation for Computational Linguistics, pp.
 [9] Chen, W., Ma, X., Wang, X., Cohen, W.W.:                     1906–1919 (2020)
     Program of thoughts prompting: Disentan-
     gling computation from reasoning for numeri-            [18] Kadavath, S., Conerly, T., Askell, A.,
     cal reasoning tasks. Transactions on Machine                 Henighan, T., Drain, D., Perez, E., Schiefer,
     Learning Research (2023)                                     N., et al.: Language models (mostly)
                                                                  know what they know. arXiv preprint
[10] Madaan, A., Tandon, N., Gupta, P., Hallinan,                 arXiv:2207.05221 (2022)
     S., Gao, L., Wiegreffe, S., Alon, U., Dziri, N.,
     et al.: Self-refine: Iterative refinement with          [19] Ren, J., Luo, J., Zhao, Y., Krishna, K., Saleh,
     self-feedback. In: Advances in Neural Infor-                 M., Lakshminarayanan, B., Liu, P.J.: Out-
     mation Processing Systems, vol. 36 (2023)                    of-distribution detection and selective gen-
                                                                  eration for conditional language models. In:


                                                        15
    International Conference on Learning Repre-
    sentations (2023)

[20] Raissi, M., Perdikaris, P., Karniadakis, G.E.:
     Physics-informed neural networks: A deep
     learning framework for solving forward and
     inverse problems involving nonlinear partial
     differential equations. Journal of Computa-
     tional Physics 378, 686–707 (2019)

[21] Karniadakis, G.E., Kevrekidis, I.G., Lu, L.,
     Perdikaris, P., Wang, S., Yang, L.: Physics-
     informed machine learning. Nature Reviews
     Physics 3(6), 422–440 (2021)

[22] Sanchez-Gonzalez, A., Godwin, J., Pfaff,
     T., Ying, R., Leskovec, J., Battaglia, P.W.:
     Learning to simulate complex physics with
     graph networks. In: International Conference
     on Machine Learning, pp. 8459–8468 (2020)




                                                      16
