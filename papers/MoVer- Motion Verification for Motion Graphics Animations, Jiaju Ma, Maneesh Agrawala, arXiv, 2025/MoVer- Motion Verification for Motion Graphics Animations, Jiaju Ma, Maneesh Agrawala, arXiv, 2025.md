                                         MoVer: Motion Verification for Motion Graphics Animations
                                         JIAJU MA, Stanford University, USA
                                         MANEESH AGRAWALA, Stanford University, USA
                                         Text prompt                                                                           Generated motion graphics animation
                                          <svg> ... </svg>
                                                                                                  frame 1-60: m1 translation by the circle
                                          Move the orange circle above the rectangular shape.
                                 frame 001             frame 020                    frame 040             frame 060
                                          In the meantime, rotate the letter H clockwise by 90 degrees.
                                         MoVer program
                                         o1 = ιo.clr(o,"orange")∧shp(o,"circle") # check for an orange circle 
                                         o2 = ιo.shp(o,"rectangle")              # check for a rectangle 
                                         o3 = ιo.id(o,"H")                       # check for the id "H" 
                                         # check for a translation by the circle to the top of the rectangle  
arXiv:2502.13372v2 [cs.GR] 17 May 2025




                                         m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,top(o1,o2)) 
                                         # check for a clockwise rotation of 90 degrees by "H"   
                                         m2 = ιm.type(m,"rot")∧agt(m,o3)∧dir(m,"cw")∧mag(m,90)                                                                   frame 61-120: m2 rotation by “H”
                                         # assert that the translation and the rotation overlap in time                        frame 061             frame 080                    frame 100             frame 120
                                         while(m1,m2)
                                         MoVer verification report
                                         m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,top(o1,o2))                       false

                                              top(o1,o2)                                                          false

                                              post(m,top(o1,o2))                                                  false

                                         m2 = ιm.type(m,"rot")∧agt(m,o3)∧dir(m,"cw")∧mag(m,90)                    true

                                         while(m1,m2)                                                             false


                                         Fig. 1. We present MoVer, a motion verification DSL, and apply it in an LLM-based motion graphics synthesis pipeline. Given a text prompt (top left) describing
                                         a desired animation (with a static SVG scene for context) our pipeline synthesizes both (1) an SVG motion graphics animation (right) and (2) a corresponding
                                         MoVer verification program (middle left) that captures spatio-temporal properties mentioned in the prompt as first-order logic predicates. Executing the
                                         MoVer program on the animation produces a verification report (bottom left) that specifies which motions and predicates the animation includes (marked
                                         true) and which it does not (marked false). Here, m1 is false because the circle motion does not end at the top of the rectangle. Motion m2 is true because the H
                                         correctly rotates 90 degrees counterclockwise. The while() predicate is false because m1 is invalid. Our pipeline can automatically feed the verification report
                                         back to the LLM-based animation synthesizer to iteratively correct the animation or users can examine the report to facilitate their debugging process.

                                         While large vision-language models can generate motion graphics anima-                            any iteration, this number raises to 93.6% with up to 50 correction iterations.
                                         tions from text prompts, they regularly fail to include all spatio-temporal                       Our code and dataset are at https://mover-dsl.github.io.
                                         properties described in the prompt. We introduce MoVer, a motion verifica-
                                         tion DSL based on first-order logic that can check spatio-temporal properties                     CCS Concepts: • Computing methodologies → Graphics systems and
                                         of a motion graphics animation. We identify a general set of such properties                      interfaces.
                                         that people commonly use to describe animations (e.g., the direction and
                                                                                                                                           Additional Key Words and Phrases: verification, iterative refinement, large
                                         timing of motions, the relative positioning of objects, etc.). We implement
                                                                                                                                           language models, motion graphics, visual programs, SVG
                                         these properties as predicates in MoVer and provide an execution engine
                                         that can apply a MoVer program to any input SVG-based motion graphics                             ACM Reference Format:
                                         animation. We then demonstrate how MoVer can be used in an LLM-based                              Jiaju Ma and Maneesh Agrawala. 2025. MoVer: Motion Verification for Mo-
                                         synthesis and verification pipeline for iteratively refining motion graphics                      tion Graphics Animations. ACM Trans. Graph. 44, 4 (August 2025), 17 pages.
                                         animations. Given a text prompt, our pipeline synthesizes a motion graphics                       https://doi.org/10.1145/3731209
                                         animation and a corresponding MoVer program. Executing the verification
                                         program on the animation yields a report of the predicates that failed and
                                         the report can be automatically fed back to LLM to iteratively correct the                        1    Introduction
                                         animation. To evaluate our pipeline, we build a synthetic dataset of 5600
                                                                                                                                           Advances in large vision-language models have yielded powerful
                                         text prompts paired with ground truth MoVer verification programs. We
                                         find that while our LLM-based pipeline is able to automatically generate a
                                                                                                                                           tools for visual content creation via program synthesis. These mod-
                                         correct motion graphics animation for 58.8% of the test prompts without                           els can take a natural language text prompt as input and gener-
                                                                                                                                           ate program code in a domain specific language (e.g., SVG, CAD,
                                         Authors’ Contact Information: Jiaju Ma, Stanford University, USA, jiajuma@cs.stanford.            etc.) that is then executed to produce visual output including im-
                                         edu; Maneesh Agrawala, Stanford University, USA, maneesh@cs.stanford.edu.
                                                                                                                                           ages [Gupta and Kembhavi 2023], vector graphics [Polaczek et al.
                                         Permission to make digital or hard copies of all or part of this work for personal or
                                                                                                                                           2025; Xing et al. 2024a], 3D scenes and CAD [Hu et al. 2025; Khan
                                         classroom use is granted without fee provided that copies are not made or distributed             et al. 2024; Zhang et al. 2024], and animation [Gal et al. 2024; Liu et al.
                                         for profit or commercial advantage and that copies bear this notice and the full citation         2025; Tseng et al. 2024]. Yet, automatically verifying that the result-
                                         on the first page. Copyrights for components of this work owned by others than the
                                         author(s) must be honored. Abstracting with credit is permitted. To copy otherwise, or            ing program produces correct visual output—output that matches
                                         republish, to post on servers or to redistribute to lists, requires prior specific permission     the specification given in the prompt—remains a challenging task.
                                         and/or a fee. Request permissions from permissions@acm.org.                                          In some visual domains like image generation, researchers have
                                         © 2025 Copyright held by the owner/author(s). Publication rights licensed to ACM.
                                         ACM 1557-7368/2025/8-ART                                                                          explored automatic verification via concept matching between the
                                         https://doi.org/10.1145/3731209                                                                   input prompt and the output image [Cho et al. 2024; Hessel et al.

                                                                                                                                                     ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
2 •    Ma and Agrawala


2021; Hu et al. 2023; Johnson et al. 2017; Lee et al. 2023]. This ap-         humans [Badler et al. 1999] or simulating car accidents [Åkerberg
proach relies on access to concept detectors for both the natural             et al. 2003], such methods typically require many special case rules
language prompt and for the output visual asset. More importantly,            to handle the ambiguity of general natural language.
the detected concepts must be relevant to the desired properties of              In the current era of large generative AI models, researchers have
the generated content. Verifying the prompt “A horse sitting on an            explored end-to-end methods for directly generating animation
astronaut" might require concept detectors for the entities “horse”           from text prompts without passing through a semantic representa-
and“astronaut” and the spatial relationship “sitting on”.                     tion [Chen et al. 2024; Gal et al. 2024; Guo et al. 2023a,b; Xing et al.
   Here we focus on such automated verification for 2D motion                 2024b]. While these end-to-end methods can generate impressive
graphics animations. We first present MoVer, a Motion Verification            animations, they regularly fail to capture all of the desired spatio-
DSL, that is based on first-order logic and can be used to check              temporal properties mentioned in the text prompt. In contrast, we
properties of the spatio-temporal trajectories of objects in an an-           focus on automatically verifying such properties in synthesized
imation. More specifically, in MoVer, checks are written as logic             motion graphics animations.
statements constructed from predicates that verify the presence of
                                                                              LLM-based program synthesis. Our work builds on recent tech-
specific spatio-temporal properties such as the direction, the magni-         niques that use LLMs for program synthesis via in-context learn-
tude, or the type (e.g., translation, rotation, scale) of motions of an       ing [Gupta and Kembhavi 2023; Surís et al. 2023]. These methods
object. We identify relevant spatio-temporal concepts based on prior          typically provide language documentation with code examples (pairs
work from cognitive psychology that has investigated how people               of text prompts with corresponding programs) as part of the system
think about relationships between objects and their motions in ani-           prompt context. The approach has been applied in a variety of visual
mation [Talmy 1975, 1983; Tversky and Lee 1998]. We show how to               synthesis domains including images [Gupta and Kembhavi 2023],
implement these concepts as MoVer predicates using Allen’s [1983]             vector graphics [Xing et al. 2024a], 3D scenes [Zhang et al. 2024],
temporal interval algebra and its 2D spatial counterpart, the rectan-         CAD [Jones et al. 2025], and human motion animation [Goel et al.
gle algebra [Balbiani et al. 1998; Navarrete et al. 2013].
                                                                              2024]. Closest to our work are Keyframer [Tseng et al. 2024] and
   We then demonstrate how MoVer can be applied in an LLM-based
                                                                              LogoMotion [Liu et al. 2025] which apply this LLM-based program
synthesis and verification pipeline to iteratively produce motion             synthesis approach to the problem of generating 2D vector anima-
graphics animation that accurately match an input text prompt.                tions. While all these methods generate a human-editable program
Given a text prompt specifying a desired animation (with a static             representation for the visual content, none of them provide auto-
SVG scene for context), we use in-context LLM-based program                   mated verification capable of checking that the resulting visuals
synthesis [Gupta and Kembhavi 2023; Surís et al. 2023] to produce             match the prompt specification. It remains up to the user to manu-
(1) a motion graphics animation (as an SVG motion program) and (2)            ally identify mismatches and fix the resulting program or to update
a corresponding MoVer verification program. Executing the MoVer               their prompt and try again. Our work aims to close this gap in the
program on the corresponding motion graphics animation results in             context of motion graphics by providing automated verification
a report pinpointing the spatio-temporal predicates the animation             and thereby allowing the LLM to iteratively correct the animation
successfully passes and fails (Figure 1). Users can use the report to
                                                                              without user intervention.
manually fix the animation program, or automatically feed it back
to our LLM-based pipeline for iterative correction.                           Visual verification. Our work is inspired by recent efforts that
   To evaluate our synthesis and verification pipeline, we build a            use visual question answering (VQA) models to check that proper-
synthetic text dataset of 5600 natural language text prompts describ-         ties mentioned in an input prompt appear in diffusion generated
ing motion graphics animations, paired with ground truth MoVer                images [Cho et al. 2024; Hu et al. 2023; Johnson et al. 2017]. For
verification programs. We find that our LLM-based pipeline can                example, these methods convert the image generation prompt “A
synthesize correct MoVer programs for 95.1% of the test prompts.              tree behind a motorcycle” into a series of natural language questions
We also find that using the automatic correction iteration capability         like “Does the image contain a tree?” and “Is the tree behind the
of our pipeline increases the number of correct animations from               motorcycle?” and use a VQA model to report the answer to each
58.8% (with no iterations) to 93.6% (up to 50 iterations). Our code           one. The answers can then be converted into a score or examined
and dataset are available at https://mover-dsl.github.io.                     individually by users. Design2Code [Si et al. 2024], on the other
                                                                              hand, proposes a set of automatic metrics for evaluating webpage
                                                                              generation quality. DreamSync [Sun et al. 2024] incorporates the
2     Related Work                                                            VQA-based review of visual outputs into an iterative optimization
Text-to-animation. Generating animations from a natural lan-                  loop where the output from VQA model is automatically fed back
guage prompt has been a long standing challenge in computer graph-            to the image generating model. SceneCraft [Hu et al. 2025] and
ics [Bouali and Cavalli-Sforza 2023]. Early text-to-animation meth-           LLMR [De La Torre et al. 2024] apply this optimization approach in
ods often used rule-based natural language processing techniques              the context of 3D and VR scene generation respectively, using LLM-
such as regular expression parsing, co-reference resolution, and sen-         based question answering. Our work similarly provides an iterative
tence simplification to map the prompt to a semantic representation           optimization loop for motion graphics animation, but, instead of a
(e.g. a scene graph) that is rendered into an animation [Åkerberg             VQA model, it uses an LLM to convert the prompt into a first-order
et al. 2003; Badler et al. 1999; Ma 2006; Marti et al. 2018; Zhang et al.     logic based verification language.
2019]. While effective for specialized domains such as posing virtual

ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                             MoVer: Motion Verification for Motion Graphics Animations • 3


Table 1. The MoVer language provides logic predicates that checks for the fulfillment of various spatio-temporal properties of objects and motions in an input
animation. Note that each object and motion attribute predicate has a corresponding accessor form (e.g. get_shp()) that returns the value of that attribute.

 Name                        Syntax                     Description
 variables                   o𝑖 , m 𝑗                   Variables that represent objects and motions in the animation scene
 Logical operators
 ∀, ∃                        exists(var, expr)          expr is a logical statement, and var is an object or motion. Returns true if there is an assignment of var that satisfies expr.
 𝜄                           iota(var, expr)            Returns an object or motion that satisfies expr and assign it to var.
 A                           all(var, expr)             Return all objects or motions that satisfy expr and assign it to var.
 ¬                           not expr                   Compute the negation of expr.
 ∧, ∨                        expr1 and expr2            Compute the conjunction or disjunction of expr1 and expr2
 Object attribute predicates
 shape                       shp(o𝑖 , shp_val)          Returns true if o𝑖 has the shape specified by shp_val, and false otherwise.
 color                       clr(o𝑖 , clr_val)          Returns true if o𝑖 has the color specified by clr_val, and false otherwise.
 id                          id(o𝑖 , id_val)            Returns true if o𝑖 has the id specified by id_val, and false otherwise.
 Atomic motion attribute predicates
 agent                       agt(m 𝑗 , o𝑖 )             Returns a vector 𝑉 of booleans (one per frame). If o𝑖 performs m 𝑗 at frame 𝑛 , then 𝑣𝑛 ∈ 𝑉 is true, and false otherwise.
 type                        type(m 𝑗 , type_val)       If m 𝑗 has motion type of type_val (either trn, rot, or scl) at frame 𝑛 , then 𝑣𝑛 ∈ 𝑉 is true, and false otherwise.
 direction                   dir(m 𝑗 , dir_val)         If m 𝑗 is in the direction dir_val at frame 𝑛 , then 𝑣𝑛 ∈ 𝑉 is true, and false otherwise.
 magnitude                   mag(m 𝑗 , mag_val)         If m 𝑗 reaches the magnitude mag_val over a sequence of frames 𝑚, ..., 𝑛 , then 𝑣𝑚 , ...., 𝑣𝑛 ∈ 𝑉 are true, and false otherwise.
 origin                      orig(m 𝑗 , orig_val)       If m 𝑗 is performed around the origin orig_val at frame 𝑛 , then 𝑣𝑛 ∈ 𝑉 is true, and false otherwise.
 duration                    dur(m 𝑗 , dur_val)         If m 𝑗 lasts the duration dur_val over the sequence of frames, 𝑚, ..., 𝑛 , then 𝑣𝑚 , ...., 𝑣𝑛 ∈ 𝑉 are true, and false otherwise.
 post                        post(m 𝑗 , expr)           If expr evaluates to true on the last frame of m 𝑗 , then 𝑣𝑛 ∈ 𝑉 is true for all frames of m 𝑗 , and false otherwise.
 Spatial and temporal relative predicates
 temporal relative           <tmp_rel>(m 𝑗 , m 𝑗 )      <tmp_rel> is one of the 13 Allen’s interval algebra predicates or aggregations of them (Figure 2 top). Returns true if the
                                                        time intervals of m 𝑗 and m 𝑗 satisfy <tmp_rel>. MoVer includes three aggregated temporal predicates: before(), while(),
                                                        and after().

    spatial relative       <spt_rel>(o𝑖 , o 𝑗 )         <spt_rel> is one of the 169 rectangle algebra predicates or aggregations of them (Figure 2 bottom). Returns true if the
                                                        spatial positions of o𝑖 and o 𝑗 satisfy <spt_rel>. MoVer implements ten aggregated predicates: top(), bottom(), left(),
                                                        right(), border(), intersect(), top_border(), bottom_border(), left_border(), and right_border().


Mapping language into formal logical specifications. One ap-                             all three occur simultaneously. People also commonly use relative
proach to representing the semantic meaning of natural language                          frames of reference rather than absolute frames, e.g. saying “Move
expressions is to map the expression into formal logical specifica-                      the circle above the square after rotating the triangle.” instead of
tions. For example, Artzi et al. [2013] show how to map English                          “Move the circle to (100,100) starting at second 5.0”.
language navigational phrases such as “move to the chair” to a                               In MoVer, spatio-temporal concepts are expressed as first-order
corresponding logical form 𝜆a.move(a)∧to(a,𝜄x.chair(x)). Re-                             logic predicates (boolean functions) over variables representing
searchers have explored this mapping approach in the context of                          objects o𝑖 ∈ O and their motions m 𝑗 ∈ M (Table 1). MoVer treats
instructing robotic manipulators [Wang et al. 2023], VQA [Hsu et al.                     seven attributes as atomic descriptions of a motion m 𝑗 :
2024] and guidance for text-to-image generation [Sueyoshi and Mat-                        (1) agt The agent object o𝑖 performing motion m 𝑗 .
subara 2024]. These methods often use specialized semantic parsing                        (2) type The motion type of m 𝑗 : “translation,” “rotation,” or “scale”.
techniques [Kamath and Das 2018] to convert natural language into                         (3) dir The direction of motion m 𝑗 .
the formal logic. While our MoVer verification language is also based                     (4) mag The magnitude or distance of motion m 𝑗 .
on formal, first-order logic, we use the program synthesis capabili-                      (5) orig The origin of motion m 𝑗 when type is rotation or scale.
ties of an LLM to map prompts to MoVer predicates. We show that                           (6) dur The duration of motion m 𝑗 .
our LLM-based approach handles a wider variety of inputs than a                           (7) post A postcondition the end state of motion m 𝑗 must satisfy.
rule-based semantic parser.                                                              MoVer includes predicates that can check the values for each of
                                                                                         these attributes. For example, the predicate dir(m 𝑗 , [1,0]) returns
3       MoVer: A Motion Verification DSL                                                 true for each frame where motion m 𝑗 is along the direction vector
MoVer is a domain specific language for verifying that certain spatio-                   [1, 0] (i.e., rightwards). We can combine individual predicates into a
temporal concepts appear in a motion graphics animation. We first                        complete logic statement to check whether an animation contains a
consider the design of the MoVer language (Section 3.1) and then                         motion m with a set of atomic properties as
describe how we execute a MoVer verification program (Section 3.2).
                                                                                             ∃m.type(m,"trn") ∧ dir(m,[0,1]) ∧ mag(m,100)
3.1       MoVer Language Design                                                                      ∧ agt(m,𝜄o.clr(o,"black") ∧ shp(o,"square")).                                    (1)
We designed MoVer based on prior work from cognitive psychol-                            This statement returns true for frames containing a motion where a
ogy that has analyzed how people think about and describe spatio-                        black square-shaped object is translating upwards by 100 px.
temporal properties and relationships in animated scenes [Talmy                             MoVer also includes predicates that can check relative spatio-
1975, 1983; Tversky and Lee 1998]. This work shows that linguistic                       temporal relationships between motions. These predicates are based
descriptions of animation schematize the information to emphasize                        on Allen’s [1983] temporal interval algebra and its 2D analog, the
only the most salient aspects of the motions of each object. People                      rectangle algebra [Balbiani et al. 1998; Navarrete et al. 2013]. These
break complex trajectories into basic motions; they individually de-                     algebras provide a formal representation for 13 temporally relative
scribe the translation, rotation, and scaling of an object even when                     relationships and 169 spatially relative relationships (Figure 2) and

                                                                                                     ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
4        •    Ma and Agrawala


                                                                                                                                                        each foreground object is represented as an SVG <shape> , <g>, or
Allen’s Interval Algebra Predicates

precedes       meets     overlaps finished
 contains         starts    equals        started
    during finishes overlapped
 met by preceded



                                                                                                                                                        <image> node with motion transforms specified per-frame. This
                                     by                                                by                            by                by

mi             mi         mi             mi        mi        mi            mi          mi         mi         mi          mi              mi        mi

         mj         mj        mj         mj        mj         mj           mj        mj           mj         mj        mj        mj           mj        SVG motion program representation is similar to that used by
                    before(mi , mj )                                                                              after(mi , mj )                       Zhang et al. [2023], and many high-level animation APIs, including
                                                                   while(mi , mj )
                                                                                                                                                        CSS [MozDevNet 2025], anime.js [Garnier 2025], and GSAP [Doyle
Rectangle Algebra Predicates
                                                                                                                                                        2025], support rendering an animation into this type of per-frame
    oi




                                                                                                             right(oi , oj )
                                                                                                                                                        SVG representation.
              top(oi, oj )
         oj




                                                                                                                                                           Given such an SVG motion program, our execution engine first
    oi




                                                                                                                                                        builds a 2D animation matrix data structure where each row repre-
         oj




                                   intersect(oi , oj )
                                                                                                                                                        sents an object and each column represents a frame of the animation.
    oi

         oj




                                                                                                                                                        In each cell (𝑖, 𝑗) of the animation matrix we store all atomic motion
                                                                                                                                                        attributes (Section 3.1), except post, for object o𝑖 at frame 𝑗. We
    oi

         oj




                                                                                                                                                        compute these motion attributes by first factoring the per-frame
    oi

         oj




                                                                                                                                                        transformation matrix of each object into a translation, rotation,
                                                                                                                                                        and scale [Thomas 1991] and then depending on the type of mo-
         oj
    oi




                                                                                                                                                        tion, computing a direction, magnitude, and origin. We separately
         oj
    oi




                                                                                                                                                        store static information for each object such as its color, shape, and
                                                                                                                                                        bounding box in object local coordinates.
         oj
    oi




                                                                                                                                                           With these data structures in place, we implement our DSL as fol-
         oj




                                                                                                                                                        lows. We execute each logical predicate in the verification program
    oi




              bottom(oi , oj )
                                                                                                                                                        on each cell of the animation matrix. We mark the cell as true if the
         oj
    oi




                                                                                                                                                        predicate is satisfied and false otherwise. Thus each predicate pro-
         oj




                                                                                                                                                        duces a boolean matrix with the same shape as the animation matrix.
    oi




                                                                                                                                                        For example, executing the predicate type(m,"rot") sets matrix
         oj
    oi




                                                                                                                                                        cell (𝑖, 𝑗) to true if object o𝑖 has a non-zero rotation angle in frame 𝑗.
         oj




                                                                                                                                                        Similarly, executing the predicate shp(o𝑖 ,"square") sets the entire
    oi




              oi         oi         oi        oi        oi            oi        oi          oi          oi     oi           oi           oi        oi   matrix row (𝑖, ∗) to true if object o𝑖 is square-shaped. A predicate
                                                                                                                                                        expression (i.e., expr) combines the results of multiple predicates by
                    oj        oj      oj       oj        oj           oj        oj          oj         oj     oj        oj          oj        oj



Fig. 2. (top) The 13 low-level temporally relative predicates in Allen’s in-                                                                            applying logical boolean operators (e.g., ∧, ∨, ¬) element-wise on
terval algebra and the three aggregated predicates (disjunctions of the                                                                                 the predicate matrices. We can check logical quantifiers (e.g., ∃, ∀)
low level predicates) in MoVer: before(), while(), and after(). (bottom)                                                                                by aggregating the boolean matrices. Finally, the 𝜄 operator returns
The 169 spatially relative predicates in the rectangle algebra and four of                                                                              an object 𝑜𝑖 or motion 𝑚 𝑗 for which a logical expression expr holds.
the aggregated predicates in MoVer. MoVer implements 10 spatially rela-                                                                                 We compute the expression on the animation matrix, identify a row
tive aggregated predicates: top(), bottom(), left(), right(), border(),
                                                                                                                                                        for which the expression holds for at least one frame, and return the
intersect(), top_border(), bottom_border(), left_border(), and
right_border() as sub-regions of this table.
                                                                                                                                                        row index (if an object is requested) or the row itself (if a motion is
                                                                                                                                                        requested).
MoVer includes predicates that can check for all of them. In addition,                                                                                     While many predicates primarily involve looking up information
MoVer aggregates certain relative predicates together with disjunc-                                                                                     in the animation and object data structures, temporal and spatial
tion to form higher-level relative predicates to better accommodate                                                                                     predicates based on the interval and rectangle algebras are more
for natural language’s inherent ambiguity. For example, the higher-                                                                                     complex. These require comparisons between the starting and end-
level aggregated temporal predicate while(m𝑖 , m 𝑗 ) (Figure 2 top)                                                                                     ing frames of the motions or between the relative positions and
returns true for each frame where both m𝑖 and m 𝑗 occur at the same                                                                                     overlaps of the bounding boxes of the objects (Figure 1). An interval
time and aggregates nine lower-level Allen algebra predicates. Simi-                                                                                    tree representation [Cormen et al. 2022] of the motions (2D intervals
larly, the aggregated spatial predicate top(o𝑖 ,o 𝑗 ) returns true as                                                                                   per-frame for spatial predicates, frame discretized 1D intervals for
long as the top edge of object o𝑖 is above the top edge of o 𝑗 and                                                                                      temporal predicates) enables efficient execution of these predicates.
aggregates 52 lower-level rectangle algebra predicates.
                                                                                                                                                        4    LLM-Based Motion Program Synthesis and Verification
3.2           MoVer Execution Engine                                                                                                                    We leverage MoVer within an motion graphics synthesis and ver-
We have implemented an execution engine for MoVer that can check                                                                                        ification pipeline. It takes as input a text prompt describing the
whether a motion graphics animation is consistent with a MoVer                                                                                           Text Prompt with 
   LLM Animation 

                                                                                                                                                                                                     Motion Graphics Animation
program. It computes the set of frames that evaluate to false with                                                                                        Static SVG Code       Synthesizer
respect to each logical statement and predicate in the verification
                                                                                                                                                         LLM MoVer
            MoVer
                MoVer
             Verification

program and outputs a verification report for each such expression                                                                                       Synthesizer          Program           Execution Engine          Report
(an example report is Figure 1 bottom left).
   The MoVer execution engine operates on a generic, frame-level                                                                                        desired animation along with a static SVG that sets the scene con-
SVG representation of motion graphics animations. Specifically,                                                                                         text for the prompt. It uses LLM-based program synthesis to pro-

ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                                                MoVer: Motion Verification for Motion Graphics Animations • 5


Text prompt                                                                                 Generated motion graphics animation
 <svg> ... </svg>
                                                                                                      frame 1-120: m1 translation by “Y” and m2 translation by “S”
 The letter Y slides until it touches the left side of the letter E. Following that, 
      frame 001                    frame 020                     frame 040                       frame 060
 the letter S moves to border E’s right side.
MoVer program
o1 = ιo.id(o,"Y") # check for an object with id "Y" 
o2 = ιo.id(o,"E") # check for an object with id "E" 
o3 = ιo.id(o,"S") # check for an object with id "S" 
# check for a translation by "Y" to border "E" on its left side  
m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,left_border(o1,o2)) 
# check for a translation by "S" to border "E" on its right side  
m2 = ιm.type(m,"trn")∧agt(m,o3)∧post(m,right_border(o3,o2))                                                             frame 1-120: m1 translation by “Y” and m2 translation by “S”
# assert that the translation and the rotation happen sequentially                          frame 061                    frame 080                     frame 100                       frame 120
before(m1,m2)
MoVer verification report
m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,left_border(o1,o2))                         false

     post(m,left_border(o1,o2))                                                    false
m2 = ιm.type(m,"trn")∧agt(m,o3)∧post(m,right_border(o3,o2))                        true
before(m1,m2)                                                                      false
Fig. 3. The input text prompt (top left) aims to move the Y and the S so that they touch the E on either side. The verification report (bottom left) shows that,
although the Y does border the left side of E on frame 80 and left_border() evaluates to true, it continues its rightward motion m1 until frame 120, and so
the post() predicate fails. Although m2 , the motion of S, successfully borders the right side of E, the before() predicate fails because m1 is false.

MoVer verification report of correction iteration 1                                         Correction iteration 1
m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,left_border(o1,o2))                         true
                                frame 1-120: m1 translation by “Y” and m2 translation by “S”
     post(m,left_border(o1,o2))                                                    true     frame 001                    frame 040                     frame 080                       frame 120
m2 = ιm.type(m,"trn")∧agt(m,o3)∧post(m,right_border(o3,o2))                        true
before(m1,m2)                                                                      false
MoVer verification report of correction iteration 2                                         Correction iteration 2
m1 = ιm.type(m,"trn")∧agt(m,o1)∧post(m,left_border(o1,o2))                         true
                frame 1-60: m1 translation by “Y”                          frame 61-120: m2 translation by “S”
     post(m,left_border(o1,o2))                                                    true     frame 001                    frame 060                     frame 061                       frame 120
m2 = ιm.type(m,"trn")∧agt(m,o3)∧post(m,right_border(o3,o2))                        true
before(m1,m2)                                                                      true

Fig. 4. Our pipeline automatically feeds the verification report (Figure 3) back to the LLM animation synthesizer to correct the animation. On the first iteration,
the motion of Y correctly ends adjacent to the left side of E at frame 120. But the motion incorrectly overlaps in time with the motion of S. On the second
correction iteration, the sequencing of the motions is correctly updated so that Y moves first (frames 1-60) before S (frames 61-120).


duce two programs; (1) the animation synthesizer produces a motion                                          or filter the feedback sent to the LLM. On each iteration, the LLM
graphics animation program written in a high-level animation API                                            animation synthesizer has access to all previous animations it has
(GSAP [Doyle 2025] in our implementation) and (2) the MoVer syn-                                            generated and the corresponding verification reports in its chat
thesizer generates a corresponding MoVer verification program. In                                           history to help it make corrections.
both cases we follow the LLM-based in-context learning approach
for program synthesis [Gupta and Kembhavi 2023; Surís et al. 2023],                                         5     Results
where we prompt GPT-4o [Hurst et al. 2024] with annotated API                                               Figures 1, 3, 5 and 6 show examples of motion graphics anima-
or DSL documentation and examples of text prompts paired with                                               tions generated with our synthesis and verification pipeline (more
corresponding output programs (Appendix A gives the prompts                                                 examples can be found at https://mover-dsl.github.io).
used in our implementation).                                                                                   In Figure 1, the prompt asks for an upward translation of the
   We render the resulting motion graphics animation into the                                               orange circle above the rectangle and a 90-degree rotation of the
generic per-frame SVG motion program representation (Section 3.2).                                          letter H with both motions overlapping in time. The intention is that
Then we execute the MoVer program on the SVG motion program                                                 the animation should end after the shapes form the word “Hi.” While
to check that spatio-temporal properties mentioned in the prompt                                            the LLM-generated MoVer program captures the spatio-temporal
appear in the animation. The output is a verification report spec-                                          properties described in the prompt, the LLM-generated animation
ifying which spatio-temporal properties appear in the animation                                             does not. As shown in the animation frames and found by the
and which do not. If the verification report indicates a failure, our                                       verification report, there is no valid motion m1 , where the circle
pipeline can automatically send the report back to the animation                                            translates to the top of the rectangle, and so both top() and post()
synthesizer and request it to update the motion graphics anima-                                             are false. A valid m2 is found as the letter H was rotated by 90 degrees
tion, thereby supporting iterative correction. Note that when the                                           clockwise. However, since m1 fails, the temporal predicate while()
feedback is automatically sent back to the LLM, we include the doc-                                         also fails since one of its input motions is invalid.
umentation of our MoVer DSL in the prompt so it can interpret the                                              In Figure 3, the prompt describes a series of motions that aim
error report (Appendix A.3). In addition, a human user can examine                                          to move the letters Y and S adjacent to the letter E. The MoVer
the verification report and either manually fix the motion program,                                         program captures these desired properties and the verification report

                                                                                                                         ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
6 •     Ma and Agrawala


Text prompt                                                                                                      nitia motion grap ic animation
 <svg> ... </svg>

                                                                                                             I       l               h    s

                                                                                                                                          frame 1 60 scale by H yellow
 Scale the yellow letter H from its top center in y to touch the top side of the red letter A. Then scale    frame 001
                                                                                                                                                    -


                                                                                                                                                frame 0 0
                                                                                                                                                            : m1               “   -           ”


                                                                                                                                                                                               frame 060
 yellow H back down to 1. As the H scales down, scale the red letter A up in y from its bottom center to                                                3



 touch the bottom side of the yellow letter H. Then scale the red A back down to 1. As the yellow letter
 H scales up, resize the pink letter H up in y from its bottom center to touch the bottom side of the blue
 letter A. Then scale the pink H back down to 1. As the pink H scales down, resize the blue letter A up in
 y from its top center to touch the top side of the pink letter H. Then scale the blue A back down to 1.
MoVer program
o1 = ιo.id(o,"H-yellow") # check for an object with id "H-yellow" 
o2 = ιo.id(o,"A-red") # check for an object with id "A-red" 
o3 = ιo.id(o,"H-pink") # check for an object with id "H-pink"

o4 = ιo.id(o,"A-blue") # check for an object with id "A-blue"                                                            frame 61 120 scale by H yellow and scale by by A red
# check for a scale by "H-yellow" from its top center to border "A-red" on its top                                               -       : m2               “   -          ”           m3              “   -   ”



m1 = ιm.type(m,"scl")∧agt(m,o1)∧orig(m,[50%,0%])∧post(m,top_border(o1,o2))                                   frame 061                          frame 0 0
                                                                                                                                                        9                                      frame 120
# check for a scale by "H-yellow" down to 1 in the y-axis  
m2 = ιm.type(m,"scl")∧agt(m,o1)∧dir(m,[0,-1])∧mag(m,[1,1])

# check for a scale by "A-red" from its bottom center to border "H-yellow" on its bottom  
m3 = ιm.type(m,"scl")∧agt(m,o2)∧orig(m,[50%,100%])∧post(m,bottom_border(o2,o1)) 
# check for a scale by "A-red" down to 1 in the y-axis  
m4 = ιm.type(m,"scl")∧agt(m,o2)∧dir(m,[0,-1])∧mag(m,[1,1]) 
before(m1,m2)            # assert that scales of "H-yellow" happen sequentially

while(m2,m3)             # assert that "H-yellow" downscale and "A-red" upscale overlap

before(m3,m4)            # assert that scales of "A-red" happen sequentially

...(statements of "H-pink" and "A-blue" omitted for clarity)                                                                              frame 121 180 scale by A red
                                                                                                                                                        -           : m4               “   -   ”



MoVer verification report                                                                                    frame 121                          frame 1 0
                                                                                                                                                        5                                      frame 180
m1 = ιm.type(m,"scl")∧agt(m,o1)∧orig(m,[50%,0%])∧post(m,top_border(o1,o2))      false

     post(m,top_border(o1,o2))                                                  false
m3 = ιm.type(m,"scl")∧agt(m,o2)∧orig(m,[50%,100%])∧post(m,bottom_border(o2,o1)) false

     post(m,bottom_border(o2,o1))                                               false
before(m1,m2)                                                                   false
while(m2,m3)                                                                    false
before(m3,m4)                                                                   false

MoVer verification report of correction iteration 1                                                          C   orrection iteration 1
m1 = ιm.type(m,"scl")∧agt(m,o1)∧orig(m,[50%,0%])∧post(m,top_border(o1,o2))      false
                       frame 060                          frame 120                                      frame 180
     post(m,top_border(o1,o2))                                                  false
m3 = ιm.type(m,"scl")∧agt(m,o2)∧orig(m,[50%,100%])∧post(m,bottom_border(o2,o1)) false

     post(m,bottom_border(o2,o1))                                               false
before(m1,m2)                                                                   false
while(m2,m3)                                                                    false
before(m3,m4)                                                                   false

...correction iteration 2-7 are identical to iteration 1...
MoVer verification report of correction iteration 8                                                          C   orrection iteration 8
m1 = ιm.type(m,"scl")∧agt(m,o1)∧orig(m,[50%,0%])∧post(m,top_border(o1,o2))                     true
         frame 060                          frame 120                                      frame 180
     post(m,top_border(o1,o2))                                                                 true
m3 = ιm.type(m,"scl")∧agt(m,o2)∧orig(m,[50%,100%])∧post(m,bottom_border(o2,o1))                false

     post(m,bottom_border(o2,o1))                                                              true
before(m1,m2)                                                                                  true
while(m2,m3)                                                                                   false
before(m3,m4)                                                                                  false
MoVer verification report of correction iteration 9                                                          C   orrection iteration 9
m1 = ιm.type(m,"scl")∧agt(m,o1)∧orig(m,[50%,0%])∧post(m,top_border(o1,o2))                     true
         frame 060                          frame 120                                      frame 180
     post(m,top_border(o1,o2))                                                                 true
m3 = ιm.type(m,"scl")∧agt(m,o2)∧orig(m,[50%,100%])∧post(m,bottom_border(o2,o1))                true

     post(m,bottom_border(o2,o1))                                                              true
before(m1,m2)                                                                                  true
while(m2,m3)                                                                                   true
before(m3,m4)                                                                                  true


Fig. 5. The input text prompt describes an animation in which the letter H and the letter A are asked to maintain contact as they scale up and down, as shown
in the frames under Correction Iteration 9 (please refer to https://mover-dsl.github.io for the animations in action). However, the initial animation produced by
the LLM animation synthesizer fails to satisfy any of the border() relations as indicated by the verification report. In the first correction iteration, the letters
H and A are stretched to border the bottom edges of the letters below them, instead of top edges (frame 60 and 120). From there, the synthesizer becomes
stuck in a loop, producing the same animation until the eighth correction iteration, where it has corrected the scaling of the yellow H and blue A. In the ninth
iteration, it eventually changes the sign of the scale factor of the two bottom letters, passing all verification checks.




ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                                        MoVer: Motion Verification for Motion Graphics Animations • 7


Text prompt                                                                                                      Initial motion graphics animation
 <svg> ... </svg>
                                                                                                                     frame 1-60: m1 scale by “H-yellow ”
 Rotate the first letter W around the pink circle by 180 degrees. Then rotate the second letter W the            frame 001                   frame 060                     frame 120
 same way. Finally, move the letter O down so that its bottom align with the rotated letter W
MoVer program
o1 = ιo.id(o,"W-1")                    # check for an object with id "W-1" 
o2 = ιo.id(o,"W-2")                    # check for an object with id "W-2" 
o3 = ιo.id(o,"O")                      # check for an object with id "O"

o4 = ιo.clr(o,"pink")∧shp(o,"circle") # check for a pink circle 
# check for a rotation by "W-1" by 180 around the pink circle 
m1 = ιm.type(m,"rot")∧agt(m,o1)∧mag(m,180)∧orig(m,get_pos(o4)) 
# check for a rotation by "W-2" by 180 around the pink circle 
m2 = ιm.type(m,"rot")∧agt(m,o2)∧mag(m,180)∧orig(m,get_pos(o4))

                                                                                                                                          frame 1-60: m1 scale by “H-yellow ”
# check for a translation by "O" to border "W-2" on its bottom side  
                                                                                                                 frame 121                   frame 150                     frame 180
m3 = ιm.type(m,"trn")∧agt(m,o3)∧dir(m,[0,-1])∧post(m,bottom_border(o3,o2)) 
before(m1,m2) # assert that the rotation by "W-1" happens before that by "W-2"

before(m2,m3) # assert that the rotation by "W-2" happens before the translation by "O"
MoVer verification report
m3 = ιm.type(m,"trn")∧agt(m,o3)∧dir(m,[0,-1])∧post(m,bottom_border(o3,o2))                    false  

     dir(m,[0,-1])                                                                            false

     post(m,bottom_border(o3,o2))                                                             false
before(m2,m3)                                                                                 false

MoVer verification report of correction iteration 1                                                              Correction iteration 1
m3 = ιm.type(m,"trn")∧agt(m,o3)∧dir(m,[0,-1])∧post(m,bottom_border(o3,o2))                    false       
      frame 121                   frame 150                     frame 180
     dir(m,[0,-1])                                                                            true

     post(m,bottom_border(o3,o2))                                                             false
before(m2,m3)                                                                                 false




MoVer verification report of correction iteration 2                                                              Correction iteration 2
m3 = ιm.type(m,"trn")∧agt(m,o3)∧dir(m,[0,-1])∧post(m,bottom_border(o3,o2))                    true  
            frame 121                   frame 150                     frame 180
     dir(m,[0,-1])                                                                            true

     post(m,bottom_border(o3,o2))                                                             true
before(m2,m3)                                                                                 true




Fig. 6. The input text prompt asks the two letter W’s to be rotated around the small pink circle and the letter O to be lowered so that the transformed letters
form the word “mom” (animations can be found at https://mover-dsl.github.io). In the initial animation, the W’s are rotated correctly, but the letter O does not
move at all, rendering both dir() and post() to false. Note that bottom_border() is true because the bottom edge of O aligns with those of the W’s at the
beginning of the animation (frame 1). In the first correction iteration, the O moves towards the bottom but does not do so enough to align with the W’s. In the
second iteration, the LLM synthesizer correctly computes the translation distance for O, producing an animation that says “wow mom” at the end (frame 180).

indicates that m1 , the motion of the letter Y, is false because post()                              6        Evaluation
failed, even though its input predicate left_border() evaluates to
true. This is because at frame 80, the letter Y does border E on its left                          Test dataset. To evaluate our LLM-based synthesis and verification
side. However, because the Y continues its translational motion m1                                 pipeline, we require a test dataset consisting of text prompts describ-
until frame 120, the post() predicate fails. Since m1 is invalid, the                              ing motion graphics animations and their corresponding ground
temporal predicate before() also fails. Figure 4 shows the next two                                truth MoVer programs. Since no such dataset is readily available,
automatic correction iterations of our pipeline for the example in                                 we synthetically build one using a template-based approach in com-
Figure 3. In correction iteration 1, the verifier reports that the letter                          bination with an LLM. Appendix B details our dataset construction.
Y now properly borders the letter E at the end of the translation                                  We divide the test dataset into four categories based on the types of
motion m1 . Although both m1 and m2 are valid, the temporal predicate                              MoVer predicates they exercise.
before() still fails because the motions do not occur sequentially.                                  (1) Single atomic motion. Each prompt describes one atomic mo-
In the second iteration, the animation synthesizer fixes this problem,                                   tion with up to seven of its attributes as in Table 1 (e.g., “Expand
and every statement and predicate in the MoVer program evaluates                                         the square by 2.”).
to true, confirming that the final animation correctly matches the                                   (2) Spatially relative motion. Each prompt describes one atomic
input prompt. Figures 5 and 6 similarly walk through examples that                                       motion that is relative to the spatial position of another object to
require multiple correction iterations. Please refer to their captions                                   exercise predicates from the rectangle algebra (Figure 2 bottom)
for more details.                                                                                        (e.g., “Move the square next to the circle.”).
                                                                                                     (3) Temporally relative motions. Each prompt describes multiple
                                                                                                         atomic motions with relative temporal sequencing relations to

                                                                                                                 ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
8 •    Ma and Agrawala


Table 2. Success rate for our LLM-based MoVer program synthesizer and a                 Table 3. Performance of our iterative LLM-based synthesis and verification
baseline semantic parser. We determine the success rate by first computing              pipeline (a) and two variations of which we remove (b) and simplify (c)
the string difference between the LLM synthesized MoVer program and                     the verification reports. For our dataset of 5600 prompts, we compute the
the corresponding ground truth program. We count a success only when                    number that requires 0 correction iterations (pass@0), the number that
there is no difference. We note that requiring a perfect string match is a              requires 1 to 49 iterations (pass@1+), and the number that fails after 49
stringent test for success as the underlying semantics of the two programs              iterations. We report the average number of iterations and their min-max
may match even without an exact string match.                                           ranges for the pass@1+ prompts. Note that failed prompts are excluded
                                                                                        from these metrics. The slight differences in pass@0 between pipelines are
MoVer program                                 Prompt Type                               the results of using a temperature of 1.0. We use a seed of 1 to mitigate the
synthesis method       Single    Spatially    Temporally    Spatio-
                                                                              Overall   inherent randomness of LLM generation.
                       atomic     relative      relative  temporally
Ours (LLM-based)       96.5%       97.1%         97.7%      90.9%             95.1%     (a) Our LLM-based pipeline
Semantic Parser         87.1%      86.3%         92.4%       76.8%            84.7%                                                  Prompt Type
                                                                                                            Single      Spatially      Temporally        Spatio-
                                                                                                                                                                       Overall
                                                                                                           atomic        relative        relative      temporally
                                                                                        pass@0        1060 (88.3%)    530 (37.9%)     1062 (88.5%)     640 (35.6%)    3292 (58.8%)
    exercise predicates from the Allen temporal interval algebra                        pass@1+        136 (11.3%)    718 (51.3%)      134 (11.2%)     962 (53.4%)    1950 (34.8%)
    (Figure 2 top). (e.g., “Move the square, while scaling the circle”).                fail              4 (0.3%)    152 (10.9%)          4 (0.3%)    198 (11.0%)      358 (6.4%)
(4) Spatio-temporally relative motions: Each prompt describes                           avg. iters.       1.1 (1-5)     6.2 (1-34)       1.8 (1-12)      6.7 (1-38)      5.8 (1-38)
    multiple atomic motions with both spatially and temporally
                                                                                        (b) No feedback pipeline
    relative relationships (e.g., “Move the circle next to the square,
                                                                                                                                     Prompt Type
    while it rotates”).                                                                                     Single      Spatially      Temporally        Spatio-
                                                                                                                                                                       Overall
Our test dataset includes a total of 5600 pairs of prompts and MoVer                                        atomic       relative        relative      temporally
                                                                                        pass@0        1062 (88.5%)    528 (37.7%)     1064 (88.7%)     646 (35.9%)    3300 (58.9%)
programs (1200 single atomic, 1400 spatially relative, 1200 tempo-
                                                                                        pass@1+          42 (3.5%)    314 (22.4%)       118 (9.8%)     200 (11.1%)     674 (12.1%)
rally relative, and 1800 spatio-temporally relative). We release this                   fail             96 (8.0%)    558 (39.9%)         18 (1.5%)    954 (53.0%)    1626 (29.0%)
dataset to promote further research at https://mover-dsl.github.io.                     avg. iters.      7.0 (1-32)     3.8 (1-35)       1.6 (1-10)      2.8 (1-38)      3.3 (1-38)

Accuracy of LLM-based MoVer synthesizer. Table 2 reports the
                                                                                        (c) Minimal feedback pipeline
success rate for our LLM-based MoVer synthesizer across our test
                                                                                                                                     Prompt Type
dataset. Overall we find that it generates correct MoVer programs                                           Single      Spatially      Temporally        Spatio-
for 95.1% of the test prompts. It is especially successful for prompts                                                                                                 Overall
                                                                                                            atomic       relative        relative      temporally
across the first three categories (above 96%), but less so for prompts                  pass@0        1061 (88.4%)    532 (38.0%)     1059 (88.3%)     636 (35.3%)    3288 (58.7%)
in the spatio-temporally relative category at 90.9%. Analyzing fail-                    pass@1+        129 (10.8%)    418 (29.9%)      133 (11.0%)     394 (21.9%)    1074 (19.2%)
                                                                                        fail             10 (0.8%)    450 (32.1%)          8 (0.7%)    770 (42.8%)    1238 (22.1%)
ure cases, we find that the LLM tends to confuse relative spatial and                   avg. iters.      2.6 (1-21)     3.6 (1-37)         1.6 (1-8)     6.7 (1-37)      4.4 (1-37)
temporal concepts. For example, with a prompt of the form “The
square translates. After that, the circle scales,” the LLM MoVer syn-
thesizer sometimes produces the predicate after(m1 ,m2 ) instead of
before(m1 ,m2 ). There are also cases where the LLM confuses rela-                      rule-based methods are brittle as it is difficult to cover all the cases
tive positioning with absolute directions. For the prompt “Move the                     that can occur in natural language.
square to the right of the circle,” the LLM can produce dir(m,[1,0])                       Yet, even though our LLM-based approach generalizes well to a
and right(o1 ,o2 ) instead of just the latter, confusing rightward                      wide variety of sentence structures and expressions, we find that it
motion with the right-side positioning. Nevertheless, the overall suc-                  can fail unexpectedly. For example, it can randomly fail to include a
cess rate of the LLM MoVer synthesizer suggests that it can produce                     mag() predicate explicitly mentioned in the prompt (e.g., “Rotate the
                                                                                        square by 90 degrees”). It might also output the wrong parameters
correct programs across a variety of prompts.
                                                                                        for predicates, such as flipping the sign of a directional parameter for
   To better understand the generalization capabilities of our LLM-
based MoVer synthesizer, we implemented a classical rule-based                          dir() or using [1,0] for an upward translation instead of [0,1].
semantic parser [Kamath and Das 2018] for converting a text prompt                      There is no clear pattern to such failures and we also find that many
into a MoVer program. This parser serves as a baseline. Appendix C                      similar prompts can produce correct results.
describes the parser in detail. Table 2 shows that, although the                        Effectiveness of LLM-based synthesis and verification pipeline.
semantic parser achieves a high overall success rate of 83.5%, it is not                Table 3a evaluates the effectiveness of our fully automatic LLM-
as strong as our LLM-based approach. Examining the unsuccessful                         based motion graphics synthesis and verification pipeline. It shows
prompts, we find that the semantic parser has trouble generalizing                      that with 0 correction iterations the LLM-based animation synthe-
to the variety of sentence structures found in our test set prompts.                    sizer produces a motion graphics animation that successfully passes
For example, to describe an upward motion of an object, a prompt                        all the checks in the ground-truth MoVer program for 58.8% of our
might say “add an upward translation to ...” or “propel the object                      test prompts (pass@0). It requires one or more correction itera-
to climb ...” The former embeds the motion type as a noun, while                        tions to successfully generate another 34.8% of the test prompts
the latter uses multiple verbs to express the same atomic motion.                       (pass@1+), and it fails to pass the ground-truth MoVer program
Our semantic parser does not contain the rules necessary to handle                      after 49 correction iterations for 6.4% of the test prompts (fail). We
the former case and produces two motions for the latter. In general,                    also see that for the pass@1+ test prompts, the average number of

ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                   MoVer: Motion Verification for Motion Graphics Animations • 9


Original prompt                   frame 01   frame 20     frame 40        frame 60            MoVer program
Rotate the blue square to                                                                     o1 = ιo.clr(o,"blue")∧shp(o,"square")     # check for a blue square
 
intersect with the black square
                                                                                              o2 = ιo.clr(o,"black")∧shp(o,"square") # check for a black square        
 
Revised prompt                    frame 01   frame 20     frame 40        frame 60

Rotate the blue square to                                                                     # check for a rotation by the blue square that brings it to 

intersect with the black                                                                      # intersect with the black square at the end 
square. Use rotation only                                                                     ∃m.type(m,"rot")∧agt(m,o1)∧post(m,intersect(o1,o2))


Fig. 7. MoVer can help user’s identify ambiguous prompts. Our pipeline correctly generates a MoVer program reflecting the user’s original prompt and it
generates a motion that successfully passes verification. However, the user’s intention was for the blue square to make an arcing motion rather than rotating
about its center and simultaneously translating. Understanding why the animation passed verification but did not meet their intentions, the user revised the
prompt to ask for a rotation-only motion and produced the desired result.

iterations is 5.8 with a (min-max) range of 1-38. These numbers sug-                 average iterations metrics decrease from 5.8 with our pipeline to 2.3
gest that the automatic verification and correction iterations in our                with no feedback and 4.4 with minimal feedback because we exclude
pipeline (pass@0 and pass@1+) significantly improves the number                      failed prompts from these numbers.
of correct animations produced, compared to using only a single                         While the numbers in Table 3 are based on assuming the pipeline
forward pass of LLM-based animation synthesis alone (pass@0).                        has access to ground truth MoVer programs, in practice our pipeline
   We observe that correction iterations are especially effective for                generates MoVer program using an LLM. As shown in Table 2, our
the spatially and spatio-temporally relative prompts, as the iter-                   pipeline generates incorrect MoVer programs for 272 (4.9%) test
ations fix 51.3% and 53.4% (pass@1+) of these cases respectively.                    prompts. Running these prompts through our full pipeline with
Examining the test prompts in these categories, we find that initially               incorrect MoVer programs, we find 70 (25.7%) pass@0, 20 (7.4%)
our LLM-based animation synthesizer often neglects the height or                     fail, 134 (49.3%) pass@1+ and these require an average of 6.7 (1-32)
width of objects when translating one to a position relative to an-                  iterations, while 48 (17.6%) generate MoVer programs that fail to
other, but such errors are often corrected within a couple of itera-                 execute. In other words, running our full pipeline on these prompts
tions. Examining the test prompts in these categories, we find that                  would falsely report that it produced correct animations for 204
initially the LLM-based animation synthesizer has trouble interpret-                 (75%) of the prompts and that it produced incorrect animations for
ing certain relative spatial concepts. For example, for the test prompt              the remaining 68 (25%) prompts.
“Translate the black square to touch the blue circle,” the synthesizer                  Finally, we have also run the evaluation in Table 3a with LLMs
might initially move the square to fully overlap the circle, rather                  other than GPT-4o (i.e. o3-mini, Gemini 2.0 Flash, Llama 3.1 8B and
than moving it to the border of the circle. Errors like these can often              Llama 3.3 70B). We find that our automatic verification and iterative
be corrected within a couple of iteration as the feedback from the                   corrections can increase the number of correct animations produced
verification report allows the LLM to fix the problem.                               by LLMs regardless of their number of parameters. Please refer to
   Test prompts that require more correction iterations often ask for                Appendix D and https://mover-dsl.github.io for more details.
a rotation or scale motion to position one object relative to another.               Discussion. Our experiment on the LLM-based MoVer synthesizer
For example, with the prompt “The blue circle is rotated to lie on the               (Table 2) shows that it is relatively good at converting natural lan-
top side of the black square”, the LLM-based animation synthesizer                   guage prompts of motions into MoVer verification programs (95.1%).
sometimes defaults to using translation despite the explicit specifi-
                                                                                     The high accuracy may be due to the fact that the concepts we
cation otherwise in the prompt. It insists on using a translation for
                                                                                     include in the MoVer DSL are based on prior work in cognitive psy-
a few iterations, but after the verification report marks the motion                 chology [Talmy 1975, 1983; Tversky and Lee 1998] which has shown
as failing, it eventually corrects the motion to use a rotation.                     that these are the concepts people commonly use when they think
   To better understand the role of the MoVer verification reports in                about and verbally describe motions. This has two consequences;
providing feedback for the correction iterations, we compare them                    first, natural language animation prompts are likely to use these con-
to two alternative forms of feedback: (1) a no feedback report where                 cepts, and, second, LLMs are likely to have encountered the concepts
we simply ask the LLM animation synthesizer to generate another                      in their training data. As a result, our LLM-based synthesizer can
animation without any feedback (Table 3b), and (2) a minimal feed-                   more accurately parse the natural language prompts into our MoVer
back report where we only indicate whether an animation program                      programs. When compared to a strong rule-based semantic parser
passes or fails verification as a whole and do not include which pred-               (84.7%), our LLM-based approach exhibits better generalizability
icates pass or fail (Table 3c). Overall, the results show that providing
                                                                                     across different prompt categories. While the rule-based approach
no or minimal feedback makes the LLM animation synthesizer less
                                                                                     has trouble against unseen patterns, the black-box LLM can parse a
effective at iterative correction, as it fixes fewer prompts (pass@1+                wider variety of natural language descriptions of motions, perhaps
decreases from 34.8% with our pipeline to 12.1% with no feedback and                 because it has been trained on extremely large datasets.
19.2% with minimal feedback) and increases the number of prompts                        Evaluations with our LLM-based synthesis and verification pipeline
that fail (fail increases from 6.4% with our pipeline to 29.0% with no               indicate that our automatic verification and correction iterations
feedback and 22.1% with minimal feedback) across all prompt types.                   help to produce more correct animations (Table 3a). Removing or
Spatially and spatio-temporally relative prompts produce the largest                 simplifying the predicate-level feedback from the verification re-
numbers of failures, with no feedback (39.9% and 53.0%) performing                   ports in the pipeline decreases the number of prompts that can be
worse than minimal feedback (32.1% and 42.8%). We note that the                      corrected and increases the number of failures (Table 3a, b, c). These

                                                                                             ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
10   •   Ma and Agrawala


results suggest that increasing the feedback to the predicate level in        Acknowledgments
the verification reports provides better in-context information for           We thank Jiayuan Mao for valuable discussions. Jiaju Ma was sup-
the LLM to correct animations.                                                ported by the Stanford Graduate Fellowship. This work was partially
   While we have focused on the automated correction iterations,              supported by the Brown Institute for Media Innovation at Stanford
one benefit of our approach is that the verification reports are human        University, NSF Award #2219864, and the HPI-HAI Program on
interpretable. Users can adapt their prompts based on the report              Artificial Intelligence (AI) and Human-Computer Interaction (HCI).
feedback. Figure 7 shows an example from a user in our lab who
gave the pipeline the prompt “Rotate the blue square to intersect
with the black square,” intending for the blue square to move in              References
an arcing motion about the black square. Our pipeline produced                Ola Åkerberg, Hans Svensson, Bastian Schulz, and Pierre Nugues. 2003. CarSim: an
an animation where the blue square only rotated around its own                    automatic 3D text-to-scene conversion system applied to road accident reports. In
                                                                                  Demonstrations.
center, but simultaneously translated on a straight path to intersect         James F. Allen. 1983. Maintaining knowledge about temporal intervals. Commun. ACM
the black square. It correctly passed the MoVer program and the                   26, 11 (Nov. 1983), 832–843. https://doi.org/10.1145/182.358434
user realized that the prompt was ambiguous. Several different                Yoav Artzi and Luke Zettlemoyer. 2013. Weakly Supervised Learning of Semantic
                                                                                  Parsers for Mapping Instructions to Actions. Transactions of the Association for
animations could be consistent with it. MoVer verification helped                 Computational Linguistics 1 (2013), 49–62. https://doi.org/10.1162/tacl_a_00209
the user adapt their prompt to be more precise and request “rotation-         Norman I. Badler, Martha S. Palmer, and Rama Bindiganavale. 1999. Animation control
only” motion and thereby debug the prompt.                                        for real-time virtual humans. Commun. ACM 42, 8 (Aug. 1999), 64–73. https:
                                                                                  //doi.org/10.1145/310930.310975
                                                                              Philippe Balbiani, Jean-François Condotta, and L Farinas Del Cerro. 1998. A model for
                                                                                  reasoning about bidimensional temporal relations. In PRINCIPLES OF KNOWLEDGE
                                                                                  REPRESENTATION AND REASONING-INTERNATIONAL CONFERENCE-. MORGAN
                                                                                  KAUFMANN PUBLISHERS, 124–130.
                                                                              Nacir Bouali and Violetta Cavalli-Sforza. 2023. A Review of Text-to-Animation Systems.
                                                                                  IEEE Access 11 (2023), 86071–86087. https://doi.org/10.1109/ACCESS.2023.3304903
7    Limitations and Future Work                                              Haoxin Chen, Yong Zhang, Xiaodong Cun, Menghan Xia, Xintao Wang, Chao Weng,
                                                                                  and Ying Shan. 2024. VideoCrafter2: Overcoming Data Limitations for High-Quality
While our method enables verification of motion graphics anima-                   Video Diffusion Models. arXiv:2401.09047 [cs.CV]
tions and thereby supports LLM-based automated synthesis with                 Jaemin Cho, Yushi Hu, Roopal Garg, Peter Anderson, Ranjay Krishna, Jason Baldridge,
                                                                                  Mohit Bansal, Jordi Pont-Tuset, and Su Wang. 2024. Davidsonian Scene Graph:
iterative correction, it has some limitations. First, because MoVer               Improving Reliability in Fine-Grained Evaluation for Text-to-Image Generation. In
represents motions in terms of low-level motion attributes, it re-                ICLR.
                                                                              Thomas H Cormen, Charles E Leiserson, Ronald L Rivest, and Clifford Stein. 2022.
quires a low-level description of the motion in the prompt. Prompts               Introduction to algorithms. MIT press.
that describe complex motion paths (e.g., “Move the triangle on a             Fernanda De La Torre, Cathy Mengying Fang, Han Huang, Andrzej Banburski-Fahey,
figure eight path,” “Make the rectangle dance.”) are challenging for              Judith Amores Fernandez, and Jaron Lanier. 2024. LLMR: Real-time Prompting of
                                                                                  Interactive Worlds using Large Language Models. In Proceedings of the 2024 CHI
the LLM to convert the prompt into the low-level MoVer predicates.                Conference on Human Factors in Computing Systems (Honolulu, HI, USA) (CHI ’24).
Such prompts are also ambiguous as it is unclear what set of low-                 Association for Computing Machinery, New York, NY, USA, Article 600, 22 pages.
level predicates would make sense to represent a “dance” motion.                  https://doi.org/10.1145/3613904.3642579
                                                                              Jack Doyle. 2025. Greensock Animation Platform v3. https://gsap.com/docs/v3/
A direction for future work is to design higher-level predicates to           Niklas Eén and Niklas Sörensson. 2003. An extensible SAT-solver. In International
accommodate such complex motion descriptions. Second, users can                   conference on theory and applications of satisfiability testing. Springer, 502–518.
                                                                              Rinon Gal, Yael Vinker, Yuval Alaluf, Amit Bermano, Daniel Cohen-Or, Ariel Shamir,
specify a self-contradictory prompt (e.g., “Move the triangle to the              and Gal Chechik. 2024. Breathing Life Into Sketches Using Text-to-Video Priors. In
right and simultaneously to the left.”). Such prompts can be con-                 Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition
verted into valid MoVer statements, but they will always resolve to               (CVPR). 4325–4336.
                                                                              Julien Garnier. 2025. anime.js · JavaScript animation engine. https://animejs.com/
false for any given input animation. Automatic detection of such              Purvi Goel, Kuan-Chieh Wang, C. Karen Liu, and Kayvon Fatahalian. 2024. Iterative Mo-
contradictory prompts may be possible using a SAT solver [Eén and                 tion Editing with Natural Language. In Special Interest Group on Computer Graphics
Sörensson 2003] and is an open direction for future work. Third,                  and Interactive Techniques Conference Conference Papers ’24 (SIGGRAPH ’24). ACM,
                                                                                  1–9. https://doi.org/10.1145/3641519.3657447
while natural language prompting is an accessible interface for creat-        Yuwei Guo, Ceyuan Yang, Anyi Rao, Maneesh Agrawala, Dahua Lin, and Bo Dai.
ing visual content, precisely describing spatio-temporal trajectories             2023a. SparseCtrl: Adding Sparse Controls to Text-to-Video Diffusion Models.
                                                                                  arXiv:2311.16933 [cs.CV]
in language can be difficult. Converting other modalities of user             Yuwei Guo, Ceyuan Yang, Anyi Rao, Zhengyang Liang, Yaohui Wang, Yu Qiao, Maneesh
controls (e.g. sketches, gestures, etc.) into motion graphics anima-              Agrawala, Dahua Lin, and Bo Dai. 2023b. AnimateDiff: Animate Your Personalized
tions and corresponding MoVer programs could further facilitate                   Text-to-Image Diffusion Models without Specific Tuning.
                                                                              Tanmay Gupta and Aniruddha Kembhavi. 2023. Visual Programming: Compositional
animation creation. The challenge is to map such user inputs into                 Visual Reasoning Without Training. In Proceedings of the IEEE/CVF Conference on
appropriate spatio-temporal motion constraints. Fourth, the MoVer                 Computer Vision and Pattern Recognition (CVPR). 14953–14962.
verification report is passive; it explains what went wrong, but does         Jack Hessel, Ari Holtzman, Maxwell Forbes, Ronan Le Bras, and Yejin Choi. 2021.
                                                                                  CLIPScore: A Reference-free Evaluation Metric for Image Captioning. ArXiv
not suggest fixes for the problems. A suggestive interface [Igarashi              abs/2104.08718 (2021). https://api.semanticscholar.org/CorpusID:233296711
and Hughes 2001] giving possible solutions as part of the report              Matthew Honnibal, Ines Montani, Sofie Van Landeghem, and Adriane Boyd. 2020.
                                                                                  spaCy: Industrial-strength Natural Language Processing in Python. (2020). https:
could further aid users in making their desired animations. Finally,              //doi.org/10.5281/zenodo.1212303
while we have developed verification for animation, it may be possi-          Joy Hsu, Jiayuan Mao, Joshua B. Tenenbaum, and Jiajun Wu. 2024. What’s Left?
ble to build verification languages for other visual content domains,             concept grounding with logic-enhanced foundation models. In Proceedings of the
                                                                                  37th International Conference on Neural Information Processing Systems (New Orleans,
such as CAD, video, and image generation to enable automated                      LA, USA) (NIPS ’23). Curran Associates Inc., Red Hook, NY, USA, Article 1684,
iterative optimization with LLMs.                                                 17 pages.


ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                                 MoVer: Motion Verification for Motion Graphics Animations •            11


Yushi Hu, Benlin Liu, Jungo Kasai, Yizhong Wang, Mari Ostendorf, Ranjay Krishna, and             Kota Sueyoshi and Takashi Matsubara. 2024. Predicated Diffusion: Predicate Logic-
   Noah A. Smith. 2023. TIFA: Accurate and Interpretable Text-to-Image Faithfulness                 Based Attention Guidance for Text-to-Image Diffusion Models. In Proceedings of the
   Evaluation with Question Answering. In Proceedings of the IEEE/CVF International                 IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR). 8651–8660.
   Conference on Computer Vision (ICCV). 20406–20417.                                            Jiao Sun, Yushi Hu, Deqing Fu, Royi Rassin, Sjoerd van Steenkiste, Dana Alon, Su
Ziniu Hu, Ahmet Iscen, Aashi Jain, Thomas Kipf, Yisong Yue, David A Ross, Cordelia                  Wang, Charles Herrmann, Ranjay Krishna, Da-Cheng Juan, and Cyrus Rashtchian.
   Schmid, and Alireza Fathi. 2025. SceneCraft: an LLM agent for synthesizing 3D                    2024. DreamSync: Aligning Text-to-Image Generation with Image Understanding
   scenes as blender code. In Proceedings of the 41st International Conference on Machine           Models. In Synthetic Data for Computer Vision Workshop @ CVPR 2024. https:
   Learning (Vienna, Austria) (ICML’24). JMLR.org, Article 776, 31 pages.                           //arxiv.org/abs/2311.17946
Aaron Hurst, Adam Lerer, Adam P Goucher, Adam Perelman, Aditya Ramesh, Aidan                     Dídac Surís, Sachit Menon, and Carl Vondrick. 2023. ViperGPT: Visual Inference via
   Clark, AJ Ostrow, Akila Welihinda, Alan Hayes, Alec Radford, et al. 2024. Gpt-4o                 Python Execution for Reasoning. Proceedings of IEEE International Conference on
   system card. arXiv preprint arXiv:2410.21276 (2024).                                             Computer Vision (ICCV) (2023).
Takeo Igarashi and John F. Hughes. 2001. A suggestive interface for 3D drawing.                  Leonard Talmy. 1975. Semantics and Syntax of Motion. Brill, Leiden, The Netherlands,
   In Proceedings of the 14th Annual ACM Symposium on User Interface Software and                   181 – 238. https://doi.org/10.1163/9789004368828_008
   Technology (Orlando, Florida) (UIST ’01). Association for Computing Machinery,                Leonard Talmy. 1983. How language structures space. In Spatial orientation: Theory,
   New York, NY, USA, 173–181. https://doi.org/10.1145/502348.502379                                research, and application. Springer, 225–282.
Justin Johnson, Bharath Hariharan, Laurens van der Maaten, Judy Hoffman, Li Fei-Fei,             Spencer W. Thomas. 1991. VII.1 - DECOMPOSING A MATRIX INTO SIMPLE TRANS-
   C. Lawrence Zitnick, and Ross Girshick. 2017. Inferring and Executing Programs for               FORMATIONS. In Graphics Gems II, JAMES ARVO (Ed.). Morgan Kaufmann, San
   Visual Reasoning. In Proceedings of the IEEE International Conference on Computer                Diego, 320–323. https://doi.org/10.1016/B978-0-08-050754-5.50069-4
   Vision (ICCV).                                                                                Tiffany Tseng, Ruijia Cheng, and Jeffrey Nichols. 2024. Keyframer: Empowering An-
Benjamin T Jones, Felix Hähnlein, Zihan Zhang, Maaz Ahmad, Vladimir Kim, and                        imation Design using Large Language Models. arXiv:2402.06071 [cs.HC] https:
   Adriana Schulz. 2025. A Solver-Aided Hierarchical Language for LLM-Driven CAD                    //arxiv.org/abs/2402.06071
   Design. arXiv preprint arXiv:2502.09819 (2025).                                               Lewis Tunstall, Nils Reimers, Unso Eun Seo Jo, Luke Bates, Daniel Korat, Moshe
Aishwarya Kamath and Rajarshi Das. 2018. A survey on semantic parsing. arXiv                        Wasserblat, and Oren Pereg. 2022. Efficient Few-Shot Learning Without Prompts.
   preprint arXiv:1812.00978 (2018).                                                                https://doi.org/10.48550/ARXIV.2209.11055
Mohammad Sadil Khan, Sankalp Sinha, Talha Uddin Sheikh, Didier Stricker, Sk Aziz                 Barbara Tversky and Paul U Lee. 1998. How space structures language. In Spatial cog-
   Ali, and Muhammad Zeshan Afzal. 2024. Text2CAD: Generating Sequential CAD                        nition: An interdisciplinary approach to representing and processing spatial knowledge.
   Models from Beginner-to-Expert Level Text Prompts. arXiv:2409.17106 [cs.CV]                      Springer, 157–175.
   https://arxiv.org/abs/2409.17106                                                              Renhao Wang, Jiayuan Mao, Joy Hsu, Hang Zhao, Jiajun Wu, and Yang Gao. 2023.
Guy Lapalme. 2024. pyrealb at the GEM‘24 Data-to-text Task: Symbolic English                        Programmatically Grounded, Compositionally Generalizable Robotic Manipulation.
   Text Generation from RDF Triples. In Proceedings of the 17th International Natural               In The Eleventh International Conference on Learning Representations.
   Language Generation Conference: Generation Challenges, Simon Mille and Miruna-                Jinbo Xing, Hanyuan Liu, Menghan Xia, Yong Zhang, Xintao Wang, Ying Shan, and Tien-
   Adriana Clinciu (Eds.). Association for Computational Linguistics, Tokyo, Japan,                 Tsin Wong. 2024b. Tooncrafter: Generative cartoon interpolation. ACM Transactions
   54–58. https://aclanthology.org/2024.inlg-genchal.5/                                             on Graphics (TOG) 43, 6 (2024), 1–11.
Tony Lee, Michihiro Yasunaga, Chenlin Meng, Yifan Mai, Joon Sung Park, Agrim                     Ximing Xing, Juncheng Hu, Guotao Liang, Jing Zhang, Dong Xu, and Qian Yu. 2024a.
   Gupta, Yunzhi Zhang, Deepak Narayanan, Hannah Benita Teufel, Marco Bellagente,                   Empowering LLMs to Understand and Generate Complex Vector Graphics. (2024).
   Minguk Kang, Taesung Park, Jure Leskovec, Jun-Yan Zhu, Li Fei-Fei, Jiajun Wu,                 Sharon Zhang, Jiaju Ma, Jiajun Wu, Daniel Ritchie, and Maneesh Agrawala. 2023.
   Stefano Ermon, and Percy Liang. 2023. Holistic Evaluation of Text-To-Image Models.               Editing Motion Graphics Video via Motion Vectorization and Transformation. ACM
   arXiv:2311.04287 [cs.CV] https://arxiv.org/abs/2311.04287                                        Trans. Graph., Article 229 (dec 2023), 13 pages. https://doi.org/10.1145/3618316
Vivian Liu, Rubaiat Habib Kazi, Li-Yi Wei, Matthew Fisher, Timothy Langlois, Seth                Yunzhi Zhang, Zizhang Li, Matt Zhou, Shangzhe Wu, and Jiajun Wu. 2024. The Scene
   Walker, and Lydia Chilton. 2025. LogoMotion: Visually-Grounded Code Synthesis for                Language: Representing Scenes with Programs, Words, and Embeddings. arXiv
   Creating and Editing Animation. In Proceedings of the 2025 CHI Conference on Human               preprint arXiv:2410.16770 (2024).
   Factors in Computing Systems (CHI ’25). Association for Computing Machinery, New              Yeyao Zhang, Eleftheria Tsipidi, Sasha Schriber, Mubbasir Kapadia, Markus Gross, and
   York, NY, USA, Article 157, 16 pages. https://doi.org/10.1145/3706598.3714155                    Ashutosh Modi. 2019. Generating Animations from Screenplays. In Proceedings of
Yinhan Liu, Myle Ott, Naman Goyal, Jingfei Du, Mandar Joshi, Danqi Chen, Omer Levy,                 the Eighth Joint Conference on Lexical and Computational Semantics (*SEM 2019),
   Mike Lewis, Luke Zettlemoyer, and Veselin Stoyanov. 2019. RoBERTa: A Robustly                    Rada Mihalcea, Ekaterina Shutova, Lun-Wei Ku, Kilian Evang, and Soujanya Poria
   Optimized BERT Pretraining Approach. arXiv preprint arXiv:1907.11692 (2019).                     (Eds.). Association for Computational Linguistics, Minneapolis, Minnesota, 292–307.
Minhua Ma. 2006. Automatic conversion of natural language to 3D animation. Ph. D.                   https://doi.org/10.18653/v1/S19-1032
   Dissertation. University of Ulster.
Marcel Marti, Jodok Vieli, Wojciech Witoń, Rushit Sanghrajka, Daniel Inversini, Diana
   Wotruba, Isabel Simo, Sasha Schriber, Mubbasir Kapadia, and Markus Gross. 2018.               A     LLM-based Generation Pipeline System Prompts
   CARDINAL: Computer Assisted Authoring of Movie Scripts. In Proceedings of the
   23rd International Conference on Intelligent User Interfaces (Tokyo, Japan) (IUI ’18).
                                                                                                 Our motion graphics synthesis and verification pipeline uses LLM-
   Association for Computing Machinery, New York, NY, USA, 509–519. https://doi.                 based in-context learning. Here we provide the system prompts for
   org/10.1145/3172944.3172972                                                                   (1) our LLM animation synthesizer, (2) our LLM MoVer synthesizer,
George A. Miller. 1994. WordNet: A Lexical Database for English. In Human Language
   Technology: Proceedings of a Workshop held at Plainsboro, New Jersey, March 8-11,             and (3) our correction iterations. In our implementation the system
   1994. https://aclanthology.org/H94-1111/                                                      prompts include complete documentation for an animation API
MozDevNet. 2025.         Using CSS animations - CSS: Cascading style sheets:                     (GSAP [Doyle 2025]) and our MoVer DSL, but due to the length of
   MDN. https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_animations/Using_
   CSS_animations                                                                                this documentation we have abbreviated those sections of these
Isabel Navarrete, Antonio Morales, Guido Sciavicco, and M Antonia Cardenas-Viedma.               prompts for clarity.
   2013. Spatial reasoning with rectangular cardinal relations: The convex tractable
   subalgebra. Annals of Mathematics and Artificial Intelligence 67 (2013), 31–70.
Shon Otmazgin, Arie Cattan, and Yoav Goldberg. 2022. F-coref: Fast, Accurate and Easy            A.1     LLM-based animation synthesizer
   to Use Coreference Resolution. In Proceedings of the 2nd Conference of the Asia-Pacific
   Chapter of the Association for Computational Linguistics and the 12th International
                                                                                                 This system prompt asks the LLM to generate a motion graphics
   Joint Conference on Natural Language Processing: System Demonstrations, Wray                  animation using GSAP [Doyle 2025] from the input text prompt.
   Buntine and Maria Liakata (Eds.). Association for Computational Linguistics, Taipei,
   Taiwan, 48–56. https://doi.org/10.18653/v1/2022.aacl-demo.6                               1   ### Overview
Sagi Polaczek, Yuval Alaluf, Elad Richardson, Yael Vinker, and Daniel Cohen-Or.              2   - You are an experienced programmer skilled in creating
   2025. NeuralSVG: An Implicit Representation for Text-to-Vector Generation.                         SVG animations using the API documentation provided
   arXiv:2501.03992 [cs.CV] https://arxiv.org/abs/2501.03992                                          below .
Chenglei Si, Yanzhe Zhang, Zhengyuan Yang, Ruibo Liu, and Diyi Yang. 2024. De-               3   - Please output JavaScript code based on the instruction .
   sign2code: How far are we from automating front-end engineering? arXiv e-prints           4   - Think step by step .
                                                                                             5
   (2024), arXiv–2403.
                                                                                             6   ### Restrictions
                                                                                             7   - Only use functions provided in the API documentation .


                                                                                                            ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
     12   •   Ma and Agrawala


8    - Avoid doing calculations yourself . Use the functions                       42    * @returns { void } - This function does not return
          provided in the API documentation to do the                                        anything .
          calculations whenever possible .                                         43    * @example
9    - Always use ` document . querySelector () ` to select SVG                    44    * // Translates the square element 25 pixels to the
          elements .                                                                         right and 25 pixels down over 1 second .
10   - Always create the timeline element with ` createTimeline                    45    * translate ( tl , square , 1 , 25 , 25 , 0) ;
          () `                                                                     46    *
11   - Always use ` getCenterPosition ( element )` to get the                      47    * // Translates the square element 25 pixels to the
          position of an element , and use ` getSize ( element )` to                         right and 25 pixels down over 1 second , starting at 2
           get the width and height of an element .                                           seconds into the timeline . The easing function used
12   - Only use ` getProperty () ` to obtain attributes other                                is power1 . out .
          than position and size of an element .                                   48    * translate ( tl , square , 1 , 25 , 25 , 2 , ' power1 . out ') ;
13   - Within the JavaScript code , annotate the lines of                          49    */
          animation code with exact phrases from the animation                     50   function translate ( timeline , element , duration , toX , toY ,
          prompt . Enclose each annotation with **.                                           startTime , easing = ' power1 . inOut ')
14                                                                                 51
15   ### SVG Setup                                                                 52   /**
16   - In the viewport , the x position increases as you move                      53    * This function adds a tween to the timeline to scale an
          from left to right , and y position increases as you                                 SVG element .
          move from top to bottom .                                                54    * @param { object } timeline - The timeline object to add
17   - In the SVG , the element listed first is rendered first ,                             the translation tween to .
           so the element listed later is rendered on top of                       55    * @param { object } element - The SVG element to be scaled
          the element listed earlier .                                                       .
18                                                                                 56    * @param { number } duration - The duration of the tween
19   ### Template                                                                            in seconds
20   The output JavaScript code should follow the following                        57    * @param { number } scaleX - The scale factor to apply to
           template :                                                                        the element along the x - axis . This value is absolute
21   ``` javascript                                                                          and not relative to the element 's current scaleX
22   // Select the SVG elements                                                              factor .
23   < code > </ code >                                                            58    * @param { number } scaleY - The scale factor to apply to
24   // Create a timeline object                                                             the element along the y - axis . This value is absolute
25   < code > </ code >                                                                      and not relative to the element 's current scaleY
26   // Compute necessary variables . Comment each line of code                              factor .
             with your reasoning                                                   59    * @param { number } startTime - Same as the startTime
27   < code > </ code >                                                                      parameter for the translate function .
28   // Create the animation step by step . Comment each line                      60    * @param { string } [ elementTransformOriginX = '50% '] - The
           of code with your reasoning                                                       x - axis transform origin from which the transformation
29   < code > </ code >                                                                        is applied . The origin is in the element 's
30   ```                                                                                     coordinate space and is relative to the top left
31                                                                                           corner of the element . The default value is 50% ,
32   ### API Documentation ( only partially shown below )                                    which means 50% of the element 's width from the left
33   /**                                                                                     edge of the element ( horizontal center of the element
34    * This function adds a tween to the timeline to                                        ).
          translates an SVG element .                                              61    * @param { string } [ elementTransformOriginY = '50% '] - The
35    * @param { object } timeline - The timeline object to add                              y - axis transform origin from which the transformation
          the translation tween to .                                                           is applied . The origin is in the element 's
36    * @param { object } element - The SVG element to be                                    coordinate space and is relative to the top left
          translated .                                                                       corner of the element . The default value is 50% ,
37    * @param { number } duration - The duration of the tween                               which means 50% of the element 's height from the top
          in seconds                                                                         edge of the element ( vertical center of the element ).
38    * @param { number } toX - The amount of pixels to                            62    * @param { string } [ absoluteTransformOriginX = null ] -
          translate the element along the x - axis from its                                  Similar to elementTransformOriginX , but the origin is
          current position . This value is a relative offset                                   in the absolute coordinate space of the SVG document
          from the element ' s current x value .                                               and should be specified as a pixel value . Specify
39    * @param { number } toY - The amount of pixels to                                      only elementTransformOriginX and
          translate the element along the y - axis from its                                  elementTransformOriginY or absoluteTransformOriginX
          current position . This value is a relative offset                                 and absoluteTransformOriginY , but not both . When both
          from the element ' s current y value .                                               are specified , elementTransformOriginX and
40    * @param { number } startTime - The absolute time in the                               elementTransformOriginY take precedence .
          global timeline at which the tween should start .                        63    * @param { string } [ absoluteTransformOriginY = null ] -
41    * @param { string } [ easing = ' none '] - The easing function                         Similar to elementTransformOriginY , but the origin is
          to use for the tween . The default value is linear                                   in the absolute coordinate space of the SVG document
          easing . The easing functions are : " power2 " , " power4 " ,                        and should be specified as a pixel value . Specify
           " expo ", and " sine ". Each function should be appended                          only elementTransformOriginX and
           with ". in ", ". out " , or ". inOut " to specify how the                         elementTransformOriginY or absoluteTransformOriginX
          rate of change should change over time . ". in " means a                           and absoluteTransformOriginY , but not both . When both
           slow start and speeds up later . ". out " means a fast                              are specified , elementTransformOriginX and
          start and slows down at the end . ". inOut " means both                            elementTransformOriginY take precedence .
          a slow start and a slow ending . For example , " power2 .                64    * @param { string } [ easing = ' none '] - Same as the easing
          in " specifies a quadratic easing in . Another easing                              parameter for the translate function .
          function is " slow (0.1 , 0.4) " , which slows down in the               65    * @returns { void } - This function does not return
           middle and speeds up at both the beginning and the                                anything .
          end . The first number (0 -1) is the porportion of the                   66    * @example
          tween that is slowed down , and the second number                        67    * // Scale the square element to double its size over 1
          (0 -1) is the easing strength .                                                    second from its center .
                                                                                   68    * scale ( tl , square , 1 , 2 , 2 , 0) ;



     ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                                   MoVer: Motion Verification for Motion Graphics Animations •        13


 69    *                                                                      104   function rotate ( timeline , element , duration , angle ,
 70    * // Scale the square element to double along x - axis and                        startTime , elementTransformOriginX = '50% ' ,
            triple along y - axis over 2 second from its center ,                        elementTransformOriginY = '50% ' ,
           starting at 2 seconds into the timeline . The easing                          absoluteTransformOriginX = null ,
           function used is power1 . out .                                               absoluteTransformOriginY = null , easing = ' power1 .
 71    * scale (tl , square , 1 , 2 , 3 , 2 , '50% ' , '50% ' , null , null              inOut ')
           , ' power1 . out ') ;
 72    *
 73    * // Scale the square element to be 4 times as large
           from its bottom right corner over 1 second .                             A.2   LLM-based MoVer synthesizer
 74    * scale (tl , square , 1 , 4 , 4 , 0 , '100% ' , '100% ') ;
 75    *                                                                            This system prompt asks the LLM to generate a MoVer verification
 76    * // Scale the square element to be 5 times as large                         program from the input text prompt.
           along the x - axis and 2 times as large along the y -
           axis from (100 px , 100 px ) in the SVG document over 2
           second .                                                             1   ### Instructions
 77    * scale (tl , square , 2 , 5 , 2 , 0 , null , null , 100 , 100) ;        2   - When a motion does not have any sequencing or timing
 78    */                                                                                constraints , simply use `exists ` to check for the
 79   function scale ( timeline , element , duration , scaleX ,                          existence of the motion .
           scaleY , startTime , elementTransformOriginX = '50% ' ,              3   - Name the object variables as `o_1 `, `o_2 `, etc . and the
           elementTransformOriginY = '50% ' ,                                             motion variables as `m_1 `, `m_2 `, etc .
           absoluteTransformOriginX = null ,                                    4   - List the object variables that are performing the
           absoluteTransformOriginY = null , easing = ' power1 .                         action first , followed by the object variables that
           inOut ')                                                                      being used as reference objects .
 80
                                                                                5   - When using `exists `, no need to assign it to a variable
 81   /**                                                                                , but do use a named variable in the lambda function .
 82    * This function adds a tween to the timeline to rotate                             Do not just use `m ` or `o `.
           an SVG element .                                                     6   - The " type " predicate for motion only includes three
 83    * @param { object } timeline - The timeline object to add                         values : " translate " , " rotate " , " scale ".
           the translation tween to .                                           7   - For integers , output them with one decimal point . For
 84    * @param { object } element - The SVG element to be                               example , 100 should be output as 100.0.
           rotated .                                                            8   - For floats , just output them as they are .
 85    * @param { number } duration - The duration of the tween                 9   - For predicates about timing ( t_before () , t_while () ,
           in seconds                                                                    t_after () ) , use the motion variables in sequential
 86    * @param { number } angle - The rotation angle in degree .                        order . For example , if m_1 should happen before m_2 ,
           This value is absolute and not relative to the                                use ` t_before ( m_1 , m_2 )` and not ` t_after ( m_2 , m_1 ) `.
           element ' s current rotation angle .                               10    - Always enclose the output with ```. Do not output any
 87    * @param { number } startTime - Same as the startTime                             other text .
           parameter for the translate function .                             11    - Order the object predicates as follows : color , shape .
 88    * @param { string } [ elementTransformOriginX = '50% '] - Same         12    - Order the motion predicates as follows : type , direction
            as the elementTransformOriginX parameter for the                             , magnitude , origin , post , duration , agent . This
           scale function .                                                              ordering has to be strictly followed .
                                                                              13
 89    * @param { string } [ elementTransformOriginY = '50% '] - Same
            as the elementTransformOriginY parameter for the                  14    ### Examples
           scale function .                                                   15    Input :
 90    * @param { string } [ absoluteTransformOriginX = null ] - Same         16    " Translate the blue circle upwards by 100 px . Then rotate
            as the absoluteTransformOriginX parameter for the                              it by 90 degrees clockwise around its bottom right
           scale function .                                                               corner ."
                                                                              17
 91    * @param { string } [ absoluteTransformOriginY = null ] - Same
            as the absoluteTransformOriginY parameter for the                 18    Output :
           scale function .                                                   19    ```
 92    * @param { string } [ easing = ' none '] - Same as the easing          20    o_1 = iota ( Object , lambda o : color (o , " blue ") and shape (o
           parameter for the translate function .                                        , " circle ") )
 93    * @returns { void } - This function does not return                    21    m_1 = iota ( Motion , lambda m : type (m , " translate ") and
           anything .                                                                    direction (m , [0.0 , 1.0]) and magnitude (m , 100.0) and
 94    * @example                                                                        agent (m , o_1 ) )
 95    * // Rotate the square element by 45 degrees ( clockwise )             22    m_2 = iota ( Motion , lambda m : type (m , " rotate ") and
            from its center over 1 second .                                              direction (m , " clockwise ") and magnitude (m , 90.0) and
 96    * rotate (tl , square , 1 , 45 , 0) ;                                             origin (m , ["100%" , "100%"]) and agent (m , o_1 ))
 97    *                                                                      23    t_before ( m_1 , m_2 )
 98    * // Rotate the square element by -90 degrees (                        24    ```
                                                                              25
           counterclockwise ) from its bottom right corner over 1
            second , starting at 1.5 seconds into the timeline .              26    Input :
           The easing function used is power1 . out .                         27    " Scale the black square up by 2 around its center for
 99    * rotate (tl , square , 1 , -90 , 1.5 , '100% ' , '100% ' , null ,                 0.25 seconds ."
                                                                              28
           null , ' power1 . out ') ;
100    *                                                                      29    Output :
101    * // Rotate the square element by 135 degrees ( clockwise              30    ```
           ) from (300 , 300) in the SVG document over 2 second .             31    o_1 = iota ( Object , lambda o : shape (o , " circle ") and color
102    * rotate (tl , square , 2 , 135 , 0 , null , null , 300 , 300) ;                  (o , " blue ") )
103    */                                                                     32    exists ( Motion , lambda m_1 : type ( m_1 , " scale ") and
                                                                                         direction ( m_1 , [1.0 , 1.0]) and magnitude ( m_1 , [2.0 ,
                                                                                         2.0]) and origin ( m_1 , ["50%" , "50%"]) and duration (
                                                                                         m_1 , 0.25) and agent ( m_1 , o_1 ) )
                                                                              33    ```
                                                                              34
                                                                              35    Input :


                                                                                              ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
     14   •   Ma and Agrawala


36   " The yellow circle is scaled up horizontally by 2.5 about                    84    Analyzes the magnitude of a specified motion variable
            its center over a period of 10 seconds ."                                          over a series of animation frames and determines
37                                                                                 85    if it matches the target magnitude within a specified
38   Output :                                                                                  tolerance .
39   ```                                                                           86    Args :
40   o_1 = iota ( Object , lambda o : color (o , " yellow ") and shape             87         motion_var ( Variable ) : The motion variable to analyze
          (o , " circle ") )                                                                   .
41   exists ( Motion , lambda m_1 : type ( m_1 , " scale ") and                    88         target_magnitude ( float or list of floats ) : The
          direction ( m_1 , [1.0 , 0.0]) and magnitude ( m_1 , [2.5 ,                          target magnitude to compare against .
          0.0]) and origin ( m_1 , ["50%" , "50%"]) and duration (                 89              If the motion type is " S " ( scale ) , this should be
          m_1 , 10.0) and agent ( m_1 , o_1 ) )                                                  a list of two floats representing
42   ```                                                                           90              the target scale factors for x and y axes . For
43                                                                                             scale , if a direction along a certain axis is
44   Input :                                                                       91              not specified , the target magnitude should be 0.
45   " Over a period of 0.5 seconds , the blue circle moves to                     92    Returns :
           be on the right of the black square ."                                  93         TensorValue : A tensor containing boolean values
46                                                                                             indicating whether the motion with the specified
47   Output :                                                                      94         magnitude occurs for each object over the animation
48   ```                                                                                       frames .
49   o_1 = iota ( Object , lambda o : color (o , " blue ") and shape (o            95    """
          , " circle ") )                                                          96
50   o_2 = iota ( Object , lambda o : color (o , " black ") and shape (            97
          o , " square ") )                                                        98    origin ( motion_var , target_origin )
51                                                                                 99    """
52   exists ( Motion , lambda m_1 : type ( m_1 , " translate ") and                100   Determines the frames during which objects in the scene
          post ( m_1 , s_right ( o_1 , o_2 ) ) and duration ( m_1 , 0.5)                       have a specific origin .
          and agent ( m_1 , o_1 ) )                                                101   Args :
53   ```                                                                           102        motion_var ( Variable ) : The motion variable associated
54                                                                                              with the scene .
55   ### Template                                                                  103        target_origin ( tuple ) : The target origin coordinates
56   ```                                                                                       to check for each object . % sign is used to indicate
57   < All object variables >                                                                  relative origin .
58   < All motion variables >                                                      104   Returns :
59   < All sequencing predicates >                                                 105        TensorValue : A tensor containing boolean values
60   ```                                                                                       indicating whether each object
61                                                                                 106                       has the target origin at each frame .
62   ### DSL Documentation ( only partially shown below )                          107
63   direction ( motion_var , target_direction )                                   108   Examples :
64   """                                                                           109       Note : always output numbers with one decimal points ,
65   Determines the frames in which a specified motion                                        even if they are integers .
           variable moves in a target direction for all objects                    110       Rotate around the point (400 , 200) : origin ( m_1 ,
           in the scene .                                                                     [400.0 , 200.0])
66   Args :                                                                        111       Scale around the center : origin ( m_1 , ["50%" , "50%"])
67        motion_var ( Variable ) : The motion variable to check .                 112       Scale around the top left corner : origin ( m_1 , ["0%" ,
68        target_direction ( str or list ) : The target direction                             "0%"])
           to check for . Can be a string for rotation ("                          113   """
           clockwise " or " counterclockwise ") or a 2 D vector for                114
           translation and scaling directions . For scaling , use                  115
           1.0 for increase and -1.0 for decrease , and 0.0 if                     116   post ( motion_var , spatial_concept )
           the direction along a certain axis is not specified .                   117   """
69   Returns :                                                                     118   Processes the motion data and checks if , at the end of
70        TensorValue : A tensor containing boolean values                                     the duration of " motion_var " ,
           indicating whether the motion variable moves in the                     119   the spatial relationship between two objects expressed in
           target direction for each object over the frames .                                    " spatial_concept " has been satisified .
71   Examples :                                                                    120   Args :
72        translate upward : direction ( m_1 , [0.0 , 1.0])                        121        motion_var ( Variable ) : The motion variable to check .
73        translate to the left : direction ( m_1 , [ -1.0 , 0.0])                 122        spatial_concept ( TensorValue ) : A tensor containing
74        rotate clockwise : direction ( m_1 , " clockwise ")                                  boolean values indicating whether two objects
75        scale down along the x - axis : direction ( m_1 , [ -1.0 ,                           maintained a certain spatial relationship at each
           0.0]) ## Do not use values other than -1.0 , 0.0 , 1.0                              frame of the animation .
           for scaling directions                                                  123   Returns :
76        scale up ( uniformly ) : direction ( m_1 , [1.0 , 1.0]) ##               124        TensorValue : A tensor containing boolean values
           Do not use values other than -1.0 , 0.0 , 1.0 for                                   indicating whether spatial_concept has been satisifed
           scaling directions                                                                    at the end of motion_var .
77        NOTE : Pay attention that , for scaling , the direction                  125   """
           is a 2D vector , where the first element is the x - axis                126
            direction and the second element is the y - axis                       127
           direction .                                                             128   duration ( motion_var , target_duration )
78        If the direction along only one axis is specified ,                      129   """
           the other axis should be 0.0.                                           130   Determines the frames during which a motion of a
79   """                                                                                       specified duration occurs for each object in the
80                                                                                             scene .
81                                                                                 131   Args :
82   magnitude ( motion_var , target_magnitude )                                   132        motion_var ( Variable ) : The motion variable to check .
83   """                                                                           133        target_duration ( float ) : The target duration to match
                                                                                                for the motion .



     ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                             MoVer: Motion Verification for Motion Graphics Animations •        15


134   Returns :                                                                active voice (e.g. “the blue circle translates”) or passive voice (e.g.
135       TensorValue : A tensor containing boolean values                     “the blue circle is translated”). For each atomic motion in our scene
           indicating the frames during which the motion occurs
           for each object .                                                   graph, we choose a sentence-level template and fill the template
136   """                                                                      parameters by mapping motion attributes and their values to nat-
137
138
                                                                               ural language phrases. For example, if the value of the direction
139   agent ( motion_var , obj_var )                                           attribute is [0, 1] and the motion type is “translation” we map the
140   """                                                                      direction to the concept “up”. To increase variation in the output
141   Determines if the motion is performed by the agents
            specified in the object variable .                                 prompts, we build a dictionary of synonymous expressions for each
142   Args :                                                                   such concept sourced from thesaurus.com, synonym.com, Word-
143        motion_var ( Variable ) : The motion variable containing            Net [Miller 1994], and GPT-4o [Hurst et al. 2024]. For example, for
             the name of the motion .
144        obj_var ( Variable ) : The object variable representing             the concept “up”, we obtain synonymous expressions like “upward”,
            the object (s) involved .                                          “northward”, “towards the top”, etc.
145   Returns :
146        TensorValue : A tensor value indicating the presence
                                                                                  To further increase prompt language variation, we vary the or-
            of motion for each object over the time steps .                    dering of the motion attributes in the general template. For example,
147   """                                                                      “The square translates for 0.5 seconds” can be reordered as “For 0.5
                                                                               seconds, the square translates” and “The square, for 0.5 seconds,
      A.3    Correction iteration                                              translates.” Our prompt generator includes all permutations of the
                                                                               motion attributes. To ensure that all the different prompt ordering
      This system prompt is fed to the LLM animation synthesizer with
                                                                               variations form grammatical English, we use pyrealb [Lapalme 2024]
      each automated correction iteration as context for interpreting the
                                                                               to handle details like subject-verb agreement and conjugation.
      MoVer verification report.
                                                                                  Finally, we add another class of prompt variations by taking one
      ### DSL Documentation
  1
  2   < same content as the DSL documentation shown in the
                                                                               of the template-based prompts and asking GPT-4o to rewrite it with
            system prompt of the LLM - based MoVer synthesizer >               as many variations as possible. These LLM-generated variations
  3                                                                            tend to be more diverse in sentence structure than the variations
  4   ### MoVer Program
  5   < the MoVer program for the current text prompt >                        produced by our template-based algorithm.
  6                                                                               To produce our final test dataset, we build a set of 56 animation
  7   ### MoVer Verification Report                                            scene graphs. 12 of these graphs are of type single atomic motions,
  8   < the verification report for the current animation >
  9                                                                            12 of type temporally relative, 14 of type spatially relative, and 18 of
 10   ### Instruction                                                          type spatio-temporally relative. From those, we generated 56 MoVer
      Please correct errors in the animation program as
 11
           indicated by the report
                                                                               verification programs as well as 5600 prompt variations. 80% of the
                                                                               prompt variations are based on synonyms and reordering, while the
                                                                               remaining 20% are from GPT-4o rewrites.
      B     Synthetic Test Data Generation
      We synthetically generated a test dataset consisting of text prompts
      describing an animation, paired with ground truth MoVer programs.        C    Semantic Parser Implementation
      We release our test dataset along with the scripts for generating it     We have implemented a semantic parser that can convert a text
      to encourage further research at https://mover-dsl.github.io.            prompt describing a desired animation into a MoVer motion veri-
         Our approach is to first define an animation using a scene graph      fication program. It uses a rule-based approach that involves five
      that explicitly represents each atomic motion using the seven atomic     main steps (Figure 8).
      motion attributes; agt, type, dir, mag, orig, dur and post (Ta-
                                                                               Step 1: Resolve object co-references. The first step identifies seg-
      ble 1). Each atomic motion may also include a reference object and
                                                                               ments of text that refer to the same objects. For example, in Figure 8
      a reference motion. From this animation scene graph, we generate
      a ground truth MoVer verification program by directly converting         we identify that “it” refers to “the black square.” To resolve such
      each object and atomic motion into MoVer predicates.                     co-references, we use the fastcoref model [Otmazgin et al. 2022],
         We also use the animation scene graph to generate multiple vari-      which is primarily designed to handle noun co-references.
      ations of a natural language text prompt. Our approach is to use         Step 2: Split prompt into atomic motion clauses. In step two we
      a set of templates that can describe an atomic motion or objects         break the prompt into clauses, each representing a single atomic
      in the scene in terms of their attributes. For example, a general        motion. Our approach uses a Roberta-based transformer model [Liu
      template for an atomic motion is <motion type verb> <agent               et al. 2019] trained as a dependency parser [Honnibal et al. 2020]
      object> <dir> <mag> <orig> <dur> <post>. In English sentences            to convert the input text prompt into a set of parse trees. Each
      verbs and objects are usually next to one another, but their ordering    resulting parse tree contains a verb at its root and represents a
      can be either verb-object or object-verb. Our sentence-level template    complete sentence. In English, a sentence may contain more than
      for verb-object ordering, uses three different variations on impera-     one verb, so we further split such trees at each such internal verb.
      tive sentences: (1) “translate the blue square”, (2) “animate the blue   For example, in Figure 8, we split “While it lifts, the blue square
      square to translate”, and (3) “make the blue square translate.” Our      rotates by 90 degrees” into individual clauses “While it lifts” and
      template for object-verb ordering, uses present tense with either        “the blue square rotates by 90 degrees.”

                                                                                        ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
16   •    Ma and Agrawala


Input                                                              The black square translates upwards. While it lifts, the blue square rotates by 90 degrees

Step 1
                                                           The black square translates upwards. While it lifts, the blue square rotates by 90 degrees
Resolve object coreferences
Step 2

Split prompt into 
                              1. The black square translates upwards.               2. While it lifts,             3. the blue square rotates by 90 degrees.
atomic motion clauses
                                                      translates[ROOT-VERB]                       lifts[ROOT-VERB]                        rotates[ROOT-VERB] 
                                   Dependency
        ├── square[nsubj-NOUN]                      ├── While[mark-SCONJ]                   ├── square[nsubj_NOUN] 
                                   parse trees        │   ├── The[det-DET]                        └── it[nsubj-PRON]                      │ ├── the[det_DET] 
                                                      │   └── black[amod-ADJ]                                                             │ └── blue[amod_ADJ] 
                                                      └── upwards[advmod-ADV]                                                             └── by[prep-ADP] 
Step 3
                                                                                                                                       └── degrees[pobj-NOUN] 
Map phrases to 
                                                                                                                                  └── 90[nummod-NUM]
MoVer predicates
                                                      shp(o,"square")
                            shp(o,"square")
                        shp(o,"square")

                                                      clr(o,"black")
                             clr(o,"black")
                         clr(o,"blue")

                                   predicates




                                                      agt(m,o)
                                   agt(m,o)
                               type(m,"rot")

                                   Mapped





                                                      type(m,"trn")
                              type(m,"trn")
                          agt(m,o)

                                                      dir(m,[0.0, 1.0])                           dir(m,[0.0, 1.0])
                      mag(m,90.0)
                                                                                                  while(m,n)

                                                      shp(o,"square")
                            shp(o,"square")
                        shp(o,"square")

Step 4
                                               clr(o,"black")
                             clr(o,"black")
                         clr(o,"blue")

Resolve motion coreferences                           agt(m,o)
                                   agt(m,o)
                               type(m,"rot")

                                                      type(m,"trn")
                              type(m,"trn")
                          agt(m,o)

                                                      dir(m,[0.0, 1.0])                           dir(m,[0.0, 1.0])
                      mag(m,90.0)

                                                                                                  while(m,n)                              orig(m,prop(o,"pos"))

                                                                                                                                          while(m,n)

Step 5
                                                                o1 = ιo.clr(o,"black")∧shp(o,"square") 
Compose MoVer
                                                         o2 = ιo.clr(o,"blue")∧shp(o,"square") 
verification program                                                   m1 = ιm.type(m,"trn")∧agt(m,o1)∧dir(m,[0.0, 1.0])                  
                                                                       m2 = ιm.type(m,"rot")∧agt(m,o2)∧mag(m,90)∧orig(m,prop(o2,"pos")) 
                                                                       while(m1,m2)


Fig. 8. Our rule-based semantic parser consists of five main steps and serves as a baseline alternative to our LLM-based approach (Section 4) for converting
natural language prompts into MoVer programs.


   Each original parse tree includes either a subject marked with the                                the classifier with them, it can classify natural language words and
dependency tag nsubj (nominal subject) or an object marked dobj                                      phrases that are synonyms of the concept of type(m,"rot").
(direct object). However, splitting a tree at internal verbs can result                                 We process the atomic parse tree in a top-down manner. For each
in a tree that does not contain a subject or object. In such cases, we                               node of the tree, we apply the finetuned classifier to check if there
look for the closest nsubj or dobj node in the original tree and attach                              is a correspondence between a MoVer predicate or operator and
it to the dangling tree. English also allows the use of an auxiliary                                 the word or phrase spanned by the subtree rooted at that node.
verb in addition to the main verb to introduce a motion, such as                                     Once a correspondence is found, we extract relevant parameters
“animate the square to rotate” and “make the square expand”. The                                     for the predicate by analyzing the content of the mapped subtree.
dependency trees for such constructions includes non-motion verbs                                    For example, we extract the number “90” from the subtree attached
(“animate” and “make”) as roots. We resolve these case by combining                                  to the verb node “rotates” after we map its content to the mag()
the main and auxiliary verbs into one node and reattaching their                                     predicate (Figure 8). As we process each node, we first check if the
original subtrees under the combined node.                                                           node is marked as a nsubj or dobj. If so, we limit the correspondence
Step 3: Map phrases to MoVer predicates. In this step, we map                                        match to the agt() predicate and object attribute predicates such
phrases in each atomic parse tree to a corresponding predicate or                                    as shp() and clr().
logic operator in MoVer. Our approach is to finetune a transformer-                                  Step 4: Resolve motion co-references There are cases where peo-
based text classifier with SetFit [Tunstall et al. 2022] to build this                               ple might use a subordinate clause to refer to a previous motion.
correspondence. More specifically, for each predicate and logic op-                                  For example in Figure 8, the “while” clause references an existing
erator in MoVer, we manually look-up a small set of corresponding                                    translational motion instead of introducing a new motion. However,
synonyms from WordNet [Miller 1994], thesaurus.com, and syn-                                         our earlier steps treat the “while” clause motion as a standalone
onym.com and use them for finetuning. For example, for the predi-                                    atomic motion. To resolve this motion co-reference, we compare
cate type(m,"rot") that checks for a rotational motion, we look                                      every atomic parse tree 𝑝𝑖 that comes from a subordinate clause to
up synonyms such as “spin”, “turn”, etc. and the after finetuning                                    all atomic trees that appear before it in the prompt. If they match
                                                                                                     in their type() and agt() predicates, we mark 𝑝𝑖 as a co-reference


ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
                                                                                          MoVer: Motion Verification for Motion Graphics Animations •           17


and remove its predicates. However, we retain its temporal sequenc-    Table 4. Performance of our LLM-based synthesis and verification pipeline
ing predicate (e.g., while()) and append it to the atomic motion       on our 5600 test prompts with four different LLMs other than GPT-4o.
                                                                       Similarly to Table 3a, we report pass@0 (the number of prompts that requires
described in the original main clause.
                                                                       0 correction iterations), pass@ 1 (the number that requires requires 1 to
Step 5: Compose MoVer verification program. We compose the             49 iterations), and the number that fails after 49 iterations. We report the
final MoVer program by traversing the tree top-down and outputting     average number of iterations and their min-max ranges for the pass@1+
the predicate or the logic operator that corresponds to each node as   prompts. We exclude failed prompts from these metrics.
identified in Step 3.                                                  (a) o3-mini
                                                                                                                      Prompt Type
D   Comparison with other LLMs                                                              Single       Spatially     Temporally       Spatio-
                                                                                                                                                      Overall
                                                                                            atomic        relative       relative     temporally
We have tested our LLM-based motion graphics synthesis and veri-       pass@0         1124 (93.7%)     712 (50.9%)    1079 (89.9%)    783 (43.5%)    3698 (66.0%)
fication pipeline with LLMs other than GPT-4o (i.e. o3-mini, Gemini    pass@1+           76 (6.3%)     668 (47.7%)      118 (9.8%)    960 (53.3%)    1822 (32.5%)
2.0 Flash, Llama 3.3 70B, Llama 3.1 8B) on our dataset with 5600       fail                0 (0.0%)      20 (1.4%)         3 (0.3%)     57 (3.2%)       80 (1.4%)
                                                                       avg. iters.       1.13 (1-2)      6.1 (1-38)      2.0 (1-32)     7.9 (1-38)      6.5 (1-38)
test prompts, using the same setup as Table 3a. We observe that
our pipelines are able to iteratively correct animations after ini-    (b) Gemini 2.0 Flash
tial failures regardless of the model size, reporting 32.5% pass@1+
                                                                                                                      Prompt Type
for the large model o3-mini, 29.9% for Gemini 2.0 Flash, 32.0% for                          Single       Spatially     Temporally       Spatio-
                                                                                                                                                      Overall
Llama 3.3 70B, and 16.1% for the smallest model Llama 3.1 8B. All                           atomic        relative       relative     temporally
LLMs seem to struggle with spatially and spatio-temporally rela-       pass@0         1101 (91.8%)     660 (47.1%)     827 (68.9%)    772 (42.9%)    3360 (60.0%)
                                                                       pass@1+           56 (4.7%)     586 (41.9%)     335 (27.9%)    698 (38.8%)    1675 (29.9%)
tive prompts, with each achieving the lowest pass@0 and highest
                                                                       fail              43 (3.6%)     154 (11.0%)        38 (3.2%)   330 (18.3%)     565 (10.1%)
fail in the spatio-temporally relative category. Single atomic and     avg. iters.       3.5 (1-35)      4.1 (1-46)      2.4 (1-21)     4.4 (1-48)      3.9 (1-48)
temporally relative prompts are easier to process, although we do
see a 23% drop in pass@0 for Gemini 2.0 Flash. Finally, stronger       (c) Llama 3.3 70B
models might use more iterations to generate more fully correct                                                       Prompt Type
animations; o3-mini takes the highest average number of iterations                           Single      Spatially     Temporally       Spatio-
                                                                                                                                                      Overall
                                                                                             atomic       relative       relative     temporally
(6.5) to produce animations for 98.6% of the 5600 prompts (1.4%
                                                                       pass@0           946 (78.8%)    700 (50.0%)     933 (77.8%)    768 (42.7%)    3347 (59.8%)
fail), and GPT-4o in Table 3a uses 5.8 average iterations for 93.6%    pass@1+          249 (20.8%)    577 (41.2%)     259 (21.6%)    702 (39.0%)    1787 (32.0%)
(6.4% fail). The other three models all have fewer average number      fail                 5 (0.4%)    123 (8.8%)         8 (0.7%)   330 (18.3%)      466 (8.3%)
of iterations but higher failure rates.                                avg. iters.        2.0 (1-12)     3.6 (1-44)      2.1 (1-21)     4.0 (1-37)      3.3 (1-37)

                                                                       (d) Llama 3.1 8B
                                                                                                                      Prompt Type
                                                                                             Single      Spatially     Temporally     Spatio-
                                                                                                                                                      Overall
                                                                                             atomic       relative       relative   temporally
                                                                       pass@0           452 (37.7%)    366 (26.1%)     344 (28.7%)  218 (12.1%)      1380 (24.6%)
                                                                       pass@1+          235 (19.6%)    333 (23.8%)     204 (17.0%)   129 (7.2%)       901 (16.1%)
                                                                       fail             513 (42.8%)    701 (50.1%)     652 (54.3%) 1453 (80.7%)      3319 (59.3%)
                                                                       avg. iters.        3.8 (1-44)     4.7 (1-48)      3.9 (1-20)   5.6 (1-48)        4.4 (1-48)




                                                                                     ACM Trans. Graph., Vol. 44, No. 4, Article . Publication date: August 2025.
