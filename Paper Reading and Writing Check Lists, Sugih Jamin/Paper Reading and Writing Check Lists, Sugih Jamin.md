Paper Reading and Writing Check Lists Sugih Jamin jamin@eecs.umich.edu November 2003

## Paper Reading Checklist:

Here's a list of questions to keep in mind when reading papers:
Context and Problem Statement:
What problems are the authors trying to solve? Are they important problems? Why or why not?

New Idea:
What new architecture, algorithm, mechanism, methodology, or perspective are the authors proposing? (How is the new idea different from all other ideas to solve the same problem?) Some people also put a lot of emphasis on the usefulness and practicality of the idea.

What to Evaluate?

What, according to the authors, need to be evaluated to confirm the worthiness of their new idea? Runtime? Throughput? Cache miss ratio? Utilization?

How to Evaluate?

How did the authors go about conducting the evaluation? Did they prove theorems? Did they run simulations? Did they build a system? Did they collect traces from existing systems?

Was the Evaluation Correct and Adequate?

How was their data collection done? Do you agree with their analysis of the data? Do you agree with their conclusions about the data? Do you have new interpretation of their data? Can you suggest new ways to evaluate their idea?

Assumptions, Drawbacks, Extensions:
Can you think of other aspects of their idea that need to be evaluated? Can you think of extensions or modifications to their idea to improve it? How would you evaluate your improvement? Can you apply their idea or method of evaluation to your own project? Do the authors make any assumptions that are not valid/realistic? Can you come up with a more general solution that does not rely on one or more of the assumptions the authors make?

## Paper Writing Checklist:

The check list for writing your paper is basically the same as above, with the following emphasis:
Context and Problem Statement:
Unless you are getting on a bandwagon, you need to establish why the problem you are studying is important. This is very difficult to do. It may take several face-to-face meetings, which is why you need to present your idea in workshops and not wait until your masterpiece is completed before revealing it.

## New Idea:

If you are getting on a bandwagon, you need to show how your idea is different from all the other ideas on the bandwagon. In all cases, you need to show that your idea is ``useful'' to the reader personally. If your idea is a long-term solution that requires wide-spread adoption to show off its full glory, it must have a migration path and **it must provide**
short-term incentives to entice adoption. The short-term incentives must be compellingly useful without full adoption of your idea.

You MUST establish the importance and relevance of the problem you're addressing and the novelty and usefulness of your idea in the Abstract and Introduction of your paper. Some people don't read beyond the Abstract and Introduction, unfortunately. You MUST make your case here.

Everett Rogers and others attribute the following characteristics to "innovation diffusion":
1. **Relative advantage: how is this a better solution?** 2. **Compatibility: is it backward compatible with current solutions?** 3. **Complexity: does it follow the KISS principle?**
Triability: is it easy and cheap for people to try it out without commitment (which is a function of compatibility and complexity and price)?

4. 5. **Observability: how obvious is the relative advantage?** 6. **Image: how cool is it?** 7. **Trust: who proposed it?**
For those pursuing a doctoral degree, it would also be useful to ascertain the importance and relevance of the problem you're addressing and the novelty and feasibility of your approach, before you invest three to six years of your life on it.

Evaluation:
Evaluation must be correct. A careful reader will check the correctness of your evaluation. A careful reader may even appreciate your systematic, methodological handling of data and the elegance of your model and analysis. Or your paper can be killed by its evaluation section if the reader doesn't like your problem statement, or your idea, or you.

## Data Presentation:

The evaluation section is NOT simply your lab journal. Don't just document the experiments done and the data collected. This will be very boring to read and not very useful. The main purpose of the evaluation section is to present insights about your idea. Start off the section with the questions you want to answer; that is, why did you do the experiments you did.

Along with the questions, present what you expect **the outcome of your experiments to be.**
Justify your expectations. Then for each question, present the data that either confirms or refutes your expectations. When presenting the data, explain how to read your graphs, if any. It is usually most exciting if your expectations are refuted, this is usually when you have new insights to contribute (assuming it is not just a bug in your implementation). One useful rule of thumb is to minimize the data you present. Remove as much as possible, leave only the essential data that helps you make your case. Somewhere in the Evaluation section you must document your experiment setup in enough details that others can repeat your experiments. This would be useful if your paper present such startling insights that people would want to repeat your experiments.

Algorithm, Protocol, APIs Presentation:
If your paper calls for a presentation of an algorithm, protocol, or APIs, the best way to present these is by giving a tutorial of their usages. Come up with an example scenario and walk the reader through the algorithm, protocol, or APIs as used in the scenario. Discuss the relevant details and subtleties of your algorithm, protocol, or APIs only as they come up in the context of the example scenario, put other details in a separate specification document and refer the reader to it.

If your paper makes you enemy, expect the consequences.

Pray hard if you are submitting your paper for publication.

If your paper doesn't get accepted despite having followed all the above guidelines, you need to pray harder and make less enemy.