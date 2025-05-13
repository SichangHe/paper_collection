# Examining the Accessibility of Generative AI Website Builder Tools for Blind and Low Vision Users: 21 Best Practices for Designers and Developers

Sushil K. Oswal *University of Washington* oswal@uw.edu

*Abstract - Generative artificial intelligence tools are capturing the attention of the public and business since the introduction of ChatGPT. While this technology offers many productivity tools, their accessibility to screen reader users is little studied. Most of the technical and professional communication research about these tools focuses on their applied potential. This paper reports the findings of a mixed methods study on the user interfaces of three websites on which GenAI tools reside and the accessibility of their web editors. Studying the accessibility of these firms' websites and their builder platforms is important because without accessibility features, blind customers cannot access these tools and create websites. This study found that none of the three builder websites, or the web editors for their tools, had WCAG 2.1 level AA accessibility. To improve these tools' accessibility and usability, these website builders will need to invest resources to develop accessibility knowhow on web development and AI. Involvement of disabled users as co-designers and testers is essential to ensure accessibility in this AI infrastructure. This paper contributes 21 best practices for designing accessible interfaces for generative AI tools.*

*Index Terms – Accessible generative AI, accessibility of web editors, AI website builders, best practices for generative AI tool design, documentation for large language models, web accessibility* 

# INTRODUCTION

Generative artificial intelligence (GenAI) tools promise substantive time savings and rapid prototyping capabilities for doing website design and development work; however, little is known about the accessibility of these firms' website interfaces and workflows for web developers and users with visual and hand-motor disabilities who depend

Hitender K. Oswal *University of Washington* hitender@uw.edu

on keyboard-only interactions. Since these users depend on adaptive technologies, such as, screen readers, braille arrays, voice input systems, and headpointers in their work to interact with digital interfaces, it is crucial that technical and professional communication (TPC) researchers study these websites and the builder platforms of these fastgrowing GenAI tools for their ability to effectively interact with these technologies. TPC research has addressed the accessibility issues for users with disabilities in digital communication technologies in a variety of contexts in the recent decades (See [1] for a wide-ranging review of this work). While a great deal of this scholarship focuses on the accessibility of pedagogy in the TPC classroom (See the two special issues—81.1 and 81.4—of Business and Professional Communication Quarterly), some of this research also concerns web accessibility issues in TPC [2, 3, 4]. Palmer and Oswal [5] is the only accessibilitycentered study on the outputs of GenAI tools at this time to the best of our knowledge. Our study differs from this earlier study in its focus on the user interfaces of Dorik.com, Relume.io, and Wix ADI websites on which their GenAI tools reside, and the accessibility of the web editors offered on these sites that users must employ to generate their own websites and their content. This study highlights the need for addressing the accessibility of GenAI platforms for blind and keyboard-only users because human-computer interactions in these website builders heavily depend on drag-and-drop interactions employing pointing devices which are inaccessible to these users. Another contribution of this study is in providing detailed accessibility data about the platforms of three website builders.

### *I. Rationale for this Study*

World-wide population of disabled people reached one billion more than a decade ago [6] and GenAI tools are bound to affect this population not only as consumers of

Authorized licensed use limited to: University of Southern California. Downloaded on April 03,2025 at 21:32:37 UTC from IEEE Xplore. Restrictions apply.

GenAI outputs but also as jobseekers in the workplace in the coming decade as these GenAI tools get adopted by small and large businesses. We realize that TPC needs to take a leadership role in identifying the accessibility challenges faced by this group of users, particularly the ones with visual and hand-motor disabilities before these GenAI tools become a fixture in our workplaces and lives. Besides, people with disabilities also need access to these AI tools for their businesses, professional presence, and personal websites. Section 508 of U.S. Rehabilitation Act mandates all federal purchases to be accessible, and the World Wide Web Consortium's (W3C) Web Content Accessibility Guidelines 2.1 and 2.2 (WCAG 2.1 & 2.2) exhort web developers to meet a minimum of Level AA for accessibility. Therefore, we were expecting the three website generating platforms to have the accessibility features listed under WCAG 2.1 Level AA.

Unless these artificial design intelligence (ADI) tools are born accessible, they will be hard to retrofit with accessibility due to the complex nature of the large language models (LLMs) powering these AI tools, and last but not least, usability without accessibility in these tools won't serve users as adequately because accessibility improves system usability in varying degrees for all [7].

GenAI tools by the dint of their arrival in the marketplace have raised new barriers for disabled users to function in their work and personal lives. The firms behind Dorik, Relume, and Wix market these tools as full-fledged website builders providing freedom to users without web development background to ideate, prototype, and generate websites. None of the three website builders mention accessibility or disability in their marketing. We wanted to scrutinize the accessibility of these firms' websites, including the specific affordances of their web editors for generating websites so that this user group's needs could be elevated. The focus on the accessibility of these firms' websites in themselves is important because without accessible web interfaces and platforms, blind customers cannot prototype or create websites using these GenAI tools, even when LLMs are not inherently inaccessible. For example, a keyboard-only user with a visual disability can enter a prompt into ChatGPT for generating web content, creating a web frame, or to describe an image like any other user and employ the results for building a website. Thus, GenAI tools can provide excellent opportunities to blind users for performing TPC work independently since the traditional web development software is ridden with numerous accessibility problems and historically this group of users have had difficulties in using these software programs without sighted support. While little regulation framework presently exists to govern GenAI platforms in U.S. and the courts in this country have taken ambiguous paths in adjudicating traditional web accessibility cases [8], European Union accessibility regulations however are expanding to bring these AI tools within the scope of digital accessibility [9].

# A BRIEF REVIEW OF AI-CENTERED RESEARCH

The GenAI research in TPC is emergent and researchers have thus far focused on the potential applications of these technologies [10, 11]. Sherrill [12] discussed the changing automation infrastructure in the workplace and Kong and Ding [13] studied the risks involved in AI-driven hiring. Markauskaite [14] examined the use of AI in learning spaces. Duin and Pedersen [15] studied augmentation and artificial technologies for their use in TPC while commenting on the ethical implications of introducing these technologies. An upcoming double special issue of the *Journal of Business and Technical Communication* edited by Stephen Carradini is the first major research collection focusing on GenAI and TPC that handles different aspects of applying the AI tools in the generative space.

### DETAILS ABOUT THE THREE WEBSITES UNDER STUDY

We chose these three website builders because they are marketed as ADI or AI tools. ADI tools are a subcategory of the larger group of GenAI tools built on LLM technologies and have been developed for more specific tasks, such as website creation, unlike OpenAI's ChatGPT or Google's Gemini which are general purpose chat bots. All the three selected tools promised to be easy to use, have plenty of options to customize the design of the website, and state that a website could be created in minutes. Each offered a free plan although we later discovered that Relume.io needed a paid subscription to test anything beyond the home page of the generated website. Both Dorik.com and Wix.com offer hosting options but Relume.io requires export of the generated website to a web hosting service. Because we were testing the accessibility of the websites and platforms to generate websites, we assumed that they will all have the basic accessibility features listed under WCAG 2.1 level A and will meet most of the requirements of AA. All the three websites promote their GenAI features with expressive, and sometimes flashy, slogans. Their websites promote their builders for their speed, cost savings, and the general message: build a website without knowing anything about coding. Dorik.com and Wix.com also stress how a simple prompt can generate a whole website.

To provide more specific examples of the marketing copy, Dorik.com promotes its services using these slogans: "Build Beautiful Websites in Minutes with AI", "Design Beautiful Websites from Just a Prompt", and "No Maintenance, More Freedom."

Relume.io's promotional copy claims: "Websites designed & built faster with AI" and "Experience the power of our AI site builder today. Build a website in under 5 minutes. Yes really."

Wix.com, the company behind Wix ADI, which also has a traditional web development business, and the most established of the three AI website builders evaluated in this study, advertises its GenAI tools with these statements: "Follow these 6 simple steps to create a website today", "Get a unique, business-ready website in no time with our powerful AI", and "Your ideas go in. Your site comes out."

Relume.io is the only firm that hedges its claims with a precaution, "Use AI as your design ally, not as a replacement" followed by the assertion, "Effortlessly generate sitemaps and wireframes for marketing websites in minutes" and "Ship faster" (the quoted phrase has an animation for visual effect when scrolling over). None of three website builders mention accessibility or disability in their marketing.

### METHODS

In this mixed method screen reader and automatic WAVE checker testing-based study, we specifically focused on examining the ability of the website builder tools' own workflows to meet the needs of blind users and the accessibility of their web editors to create website prototypes. Our study is limited 3 builders; therefore its claims cannot be generalized but it exemplifies the common accessibility problems we are observing in existing GenAI tools. During the systematic manual testing for web accessibility, we drew on the guidelines from Horton and Quesenbery [16] and WCAG 2.1. For web usability guidelines, we relied on Barnum [17] and Rubin & Chisnell [18].

### *I. Manual testing using qualitative techniques*

To evaluate the usability and accessibility of the chosen websites, we first employed cognitive walkthrough method to get a feel for the site both with and without JAWS (2024) screen reader. Since one of the authors has experience of testing websites with screen readers for more than a decade, we conducted this expert testing both through the cognitive walkthrough and later during the step-by-step testing process. We turned off the screen to solely depend on JAWS screen reader while the other author observed and took notes. To analyze this qualitative data, we coded all the notes to arrive at the key themes relating the accessibility problems [19]. Our cognitive walkthrough using screen reader revealed so many usability and accessibility problems that testing with users with disabilities unfamiliar with the technical side of web design would not have gone very far without sighted help.

Cognitive walkthrough methods with all their variations [20] are useful for identifying features of web environment to study its workings and how these web interfaces interact with users [21]. Expert testing methods to obtain screen reader data are also well established and recognized as a valid substitute in such circumstances.

### *II. Automated Testing with WAVE Tool*

Because our manual testing with a screen reader both in the preliminary stages of this project and our later more indepth testing of every button, link, and heading levels revealed a large number of accessibility and usability issues in these websites and their web editors for generating websites with AI, we conducted a machine test of each of these platforms to verify our results. The data from both the test modalities is presented in the results section below. After reviewing the WAVE test's results, we further verified the errors flagged in this report with manual screen reader testing to count out the possibility of false positives and negatives. In most cases, WAVE identified the same problems that our manual testing had recorded. Because all the three websites lacked even rudimentary accessibility, we focused on selective accessibility features, such as, an accurate heading structure for screen reader navigation, alternative text descriptions for images and icons, proper labeling of all links with text, skip links for avoiding lengthy menus, and color contrast issues for low-vision and color-blind users. WAVE categorizes serious accessibility violations as "errors" and less egregious accessibility problems as "alerts". As our results later show, WAVE can categorize certain problems as "alerts" when the context in which the problem occurs requires manual checking.

# RESULTS

We provide a quick overview of the results before presenting detailed information about the three website builders in the first two tables. Tables 3 and 4 focus on specific accessibility problems. Our data offers a mixed accessibility picture in these three AI website builders' sites although one appears to have paid some attention to providing accessibility information to the users of its website builder. The websites hosting these GenAI tools and their web editors lacked basic accessibility features, such as, correct order for headings, properly labeled buttons and links, skip links, and alternative text descriptions for icons and images.

Our cognitive walkthrough of the three websites of these AI builders revealed that Dorik.com has no reference to accessibility for disabled users, including its Help Center. Relume.io also has no reference to accessibility on its own website; however, it has a link to the Client-First documentation which includes a page on web accessibility. Client-First itself is a style system for Webflow.com, one of the visual website builders that Relume.com employs for its own website builder. The important point here to note is that the accessibility information provided on these thirdparty pages is rudimentary, descriptive instead of instructional, and would be of little use to a Relume.io customer without a web development background. Wix.com offers an automated accessibility checker called, Accessibility Wizard, which again is of little use to anyone without basic knowledge of web development. A quick search of Wix.com's Help Center brings up more than 1,200 articles on accessibility but none of them appear to focus on Wix ADI's generated websites and for users unfamiliar with basic web development. As websites, all of them possess the basic features of webpages although Relume.io lacked professionalism in their content because we noticed typos in their tutorials.

Before presenting the results of the manual testing with a screen reader and WAVE automatic checker data, Table 1 offers a quick cognitive walkthrough of the workflow any user would follow to create a website on the three web builder platforms. While the series of steps involved in generating the sections of a website are not complicated, the missing labels on buttons, undescribed links, and a lack of spoken callouts about the function of specific actions make the process inaccessible. These callouts about action steps are essential for blind users to make up for the contextual information sighted users get from the layout and design of the page. The presence of multiple unlabeled buttons for choosing various options made all the three websites' editors altogether unusable for those who depend on screen readers to listen to these elements.

Table 2 describes AI tools built into the workflow for generating websites. Again, unlabeled buttons and links, a lack of callouts, and missing descriptions of the AI tools, or missing descriptions in the pop-ups make them both unusable and inaccessible.

TABLE 1. THE WEBSITE CREATION PROCESS AND CUSTOMIZATION OPTIONS FOR EACH SELECTED WEBSITE BUILDER.

|                 | Dorik.com                  | Relume.io                     | Wix.com                                   |  |
|-----------------|----------------------------|-------------------------------|-------------------------------------------|--|
| Website         | Fill out information:      | 1. Click "New Project"        | Chat with AI:                             |  |
| generation      | 1. Name of your website    | button                        | 1. What do you want to call your site?    |  |
| process         | 2. Website/Business        | 2. Enter Sitemap prompt       | 2. Can you describe your services?        |  |
|                 | Description                | 3. Choose number of           | 3. Who is your target audience?           |  |
|                 | 3. Language (Optional)     | pages (In increments of       | 4. Do you have any specific goals for     |  |
|                 | 4. Click on "Generate      | 5)                            | reaching a target audience?               |  |
|                 | Your website               | 4. Choose language            | 5. Can you share your unique selling      |  |
|                 |                            | 5. Click "Generate            | point?                                    |  |
|                 |                            | Sitemap"                      | 6. What inspired you to start your        |  |
|                 |                            | 6. Click "Generate            | business?                                 |  |
|                 |                            | empty pages"                  | 7. What is the history of your business?  |  |
|                 |                            | 7. Click on "Wireframe"       | 8. Click on "Design your website"         |  |
|                 |                            | to generate a wireframe       | 9. Click on "Let Wix create a site for    |  |
|                 |                            | using the sitemap             | you"                                      |  |
| Customization   | -Change layout of content  | -Add and remove sections      | -Change layout of content                 |  |
| Allowed         | -Add and remove sections   | with option to automatically  | -Add and remove sections as well as       |  |
|                 | with templates             | fill sections with AI         | generate new sections with an AI prompt   |  |
|                 |                            | generated content             |                                           |  |
|                 |                            |                               |                                           |  |
| Customization   | -Does not automatically    | -Cannot change layout of      | -Does not automatically generate content  |  |
| Limitations     | generate content for added | templates                     | for added sections                        |  |
|                 | sections                   |                               |                                           |  |
| AI tools in     | 1. AI Quick Style:         | 1. Sitemap:                   | 1. AI Text Creator:                       |  |
| addition to the | Switch the color scheme    | Creates a site map and layout | Generates text based on the business      |  |
| site generator  | and typography of the      | for each page                 | information, the topic of the text, and a |  |
|                 | webpage                    | 2. Wireframe:                 | prompt                                    |  |
|                 | 2. Generate new pages:     | Generates a wireframe with    | 2. Create AI Image:                       |  |
|                 | Creates new pages from an  | content for the webpage from  | Generates an AI generated image using a   |  |
|                 | AI prompt                  | the sitemap                   | chosen style and prompt                   |  |
|                 | 3. Write with AI:          | 3. Ask AI:                    |                                           |  |
|                 | generates content from a   | Generates content from a      |                                           |  |
|                 | prompt or existing text    | prompt or existing text       |                                           |  |
|                 | 4. Generate with AI:       |                               |                                           |  |
|                 | Generate images from a     |                               |                                           |  |
|                 | prompt                     |                               |                                           |  |

Dorik.com and Relume.io's website building process starts with the completion of a form with basic details of the desired website whereas Wix.com has step-by-step prompts. Besides the accessibility issues listed in Table

2, the form for Dorik.com itself had redundant text labels.

Relume.io's form also had missing form labels, empty

buttons, and very low contrast errors.

TABLE 2. ACCESSIBILITY FEATURES OF THE WEBSITE BUILDER TOOLS USING SCREEN READER WALKTHROUGH.

|                            | Dorik.com            | Relume.io              | Wix.com              |
|----------------------------|----------------------|------------------------|----------------------|
| The accessibility of the   | Inaccessible         | Partially accessible   | Inaccessible         |
| interface and the tools it |                      |                        |                      |
| employs                    |                      |                        |                      |
| Accessibility of the       | Mostly accessible    | Mostly accessible      | Mostly accessible    |
| website content -          |                      |                        |                      |
| Textual                    |                      |                        |                      |
| Accessibility of the       | Partially accessible | Has filler images only | Partially accessible |
| website content - Visual   |                      |                        |                      |

Although different websites use different terminology for the outputs of their builders, all require the addition of content, structural features, and layout sections by the user. While blind users may possess the skills for performing the tasks, due to the linear nature of screen reading by their adaptive tools, they heavily use search features to locate their place during this work. None of the three firms' own websites have a search feature. Dorik.com and Relume.io's website builder editors have search option for locating elements during the addition of sections but they do not have search for settings or features. We also noticed that none of them have a search feature in the automatically generated website; however, Wix.com has an option for the addition of one. Since the three AI tools engaged in this study do offer additional affordances for manually adding features by the user with some web development knowledge, our expert testing also included these features;

however, it was not easy to follow through the complete process for adding these features because the basic website editors failed to function adequately with the screen reader for completing the expert testing. Many of the AI tools were also unreachable for keyboard-only users. For instance, both Dorik.com and Wix.com had issues opening dropdown menus without the use of a mouse and all three builders had menus that were not labeled. A screen reader would read items as "unlabeled" image or just "graphic". Although it is possible to generate a website using AI from a prompt with all three website builders, the only website builder that allows some editing of sections is Relume.io. When working on a project sitemap, Relume.io permits a keyboard only user to edit a section for adding or removing content however, it neither explains to a blind user that they have to use the enter key to perform this function, nor does it indicate the location of the focus.

| Company pages     | Unlabeled<br>buttons1 | Missing form<br>labels1 | Color contrast<br>errors | Missing/uninfor<br>mative page title | Language<br>missing/invalid |
|-------------------|-----------------------|-------------------------|--------------------------|--------------------------------------|-----------------------------|
|                   |                       |                         |                          |                                      |                             |
| Dorik.com Editor  | 12 (75%)              | 1 (100%)                | 0                        | 1                                    | 0                           |
| Relume.io Sitemap | 10 (45%)              | 0 (No forms)            | 5                        | 1                                    | 1                           |
| Relume.io         | 11 (48%)              | 0 (No forms)            | 4                        | 1                                    | 1                           |
| Wireframe         |                       |                         |                          |                                      |                             |
| Wix.com Editor    | 17 (74%)              | 0 (No forms)            | 0                        | 0                                    | 0                           |

TABLE 3. THE LIST OF ERRORS FLAGGED BY WAVE

<sup>1</sup> The percentages listed for missing labels on buttons and forms indicate the portion of total elements that were unlabeled.

Table 3 shows the large number of errors in each of the three website builder sites identified by WAVE. When we machine tested the wireframe builder in Relume.io, WAVE found a large number of diverse errors, contrast errors, and alerts. In addition to these identified errors, WAVE gave a large number of false positives for Relume.io. For example, when the site used placeholder images in the wireframe, they are coded with the alt text of "wf\_reserved\_inherit" which communicates no information either about the image or about the element.

TABLE 4. THE LIST OF ALERTS FLAGGED BY WAVE

| Company pages     | No heading<br>structure | Noscript<br>element | Very small text | Underlined text | Broken same<br>page link |
|-------------------|-------------------------|---------------------|-----------------|-----------------|--------------------------|
| Dorik.com Editor  | 1                       | 2                   | 0               | 0               | 1                        |
| Relume.io Sitemap | 1                       | 1                   | 0               | 0               | 0                        |

| Relume.io<br>Wireframe | 1 | 1 | 0 | 0 | 0 |
|------------------------|---|---|---|---|---|
| Wix.com Editor         | 1 | 0 | 2 | 1 | 0 |

Although WAVE considers alerts to be less serious problems, it listed a number of heading structure issues under this category. Because screen readers are linear text readers, blind users employ keyboard commands to navigate webpages without reading all of the content. It is the heading structure of the page that allows users to jump around on the page with keyboard commands. We also might point out that when a page structure is not coded for headings or the headings are not in the right order, blind users cannot form a mental picture of the page and move around without linearly reading everything. Some of the other items under the WAVE alerts are less serious from the perspective of simple access to the information; however, they do affect the user experience negatively. For example, underlined text on webpages in the past could result in garbled reading by JAWS screen reader but newer versions of JAWS simply ignore underlining unless the user prompts it to read the text formatting. When Wix.com displayed a potential domain name for our imaginary gym with an underline, we could visually see that Wix.com was drawing our attention to this domain; however, JAWS simply read the name of the website. In this case, the blind user will miss the purpose of the underline because the screen reader is avoiding it; however, the content creator and designer could have made a different choice to stress the availability of the domain that would be communicated by screen readers without fail. The broken same-page link alert flagged on Dorik.com site was in fact a false positive. However, this link had a problem with the presentation of information on the linked pop-up which opens in the same tab and breaks the reading flow of a large list of editor options. The system also does not give focus to the link for the screen reader cursor after the pop up is read. Last, WAVE test's "very small text" alert is a false positive because screen readers can read all sizes of normally displayed text. "Noscript element" is another alert which would affect a screen reader because these elements seem to be related to the tracking of incoming user traffic from other sites.

# DISCUSSION

Our study's contribution is in highlighting the need for addressing the accessibility of GenAI platforms for blind and keyboard-only users because human-computer interactions in these website builders heavily depend on drag-and-drop interactions employing pointing devices such as mouse and touchpads which are inaccessible to these users. At this time, these website builders are both unusable and inaccessible to this group of users because the basic features of their interfaces are dysfunctional with adaptive technologies, including keyboards. Even if the technical accessibility problems in these website builders were to be solved, it would not make them usable for screen reader users because the platforms lack structural design essential for usable and accessible interfaces. TPC and HCI research often overlooks this usability-accessibility nexus when discussing the accessibility of web interfaces [4, 7].

A widely accepted definition of accessibility alludes to the "extent to which products, systems, services, environments and facilities can be used by people from a population with the widest range of characteristics and capabilities to achieve a specified goal in a specified context of use" (ISO 26800; ISO/TR 9241-100; ISO/TR 22411) [22]. In the context of the three websites in this study, the functionality refers to the usability of the interfaces whereas the lack of specific accessibility implementations, such as, labeling of buttons and icons with text, and systematic ordering of heading levels to render the structure of the pages correctly readable by screen readers refers to the accessibility, or lack thereof. When a screen reader user has to come up with some workarounds to deal with the missing accessibility, the concept of user experience also comes into play because these users are obtaining the tool usability by doing extra lifting which does not bode well for the website infrastructure and its user experience. The overlap of usability and accessibility in the context of GenAI tools is more complicated than the current ISO accessibility standard covers [22]. The web editors for GenAI tools differ from the typical web tools and currently do not have established design conventions. We also want to note that some of the problems that WAVE checker listed as "alerts", were serious accessibility issues and should have been categorized under "errors". Our data underlines the need for manual testing with screen readers when developers are checking pages for accessibility for users with visual disabilities. It also points toward the necessity for a greater representation of totally blind developers in the bodies in charge of developing accessibility standards and guidelines, including the various committees of W3C, U.S. Access Board, and Section 508 because W3C guidelines only tell half the story about web accessibility issues [23].

Improving human interactions with GenAI tools will require long-term, iterative testing with blind users because the Human-computer interactions on these platforms are different from traditional web interactions due to their prompt-driven interfaces and WCAG 2.2 standards have not specifically address ADI tools. We also lack documentation about the datasets underlying these website builders to understand their affordances to implement web accessibility. We further need background information about the algorithms, design engines, and training parameters behind these tools to understand their generative scope and any structural issues in the web products of these platforms that might affect the functioning of adaptive user interfaces such as screen readers. Without a meaningful information sharing relationship between the designers of these GenAI tools and the developers of adaptive technologies, achieving accessibility for disabled users in this new realm will be elusive.

### CONCLUSION

Researchers in TPC and HCI have stressed the need for including disabled users during all stages of prototype development so that inclusive user centered solutions are ideated, prototyped, and developed to solve practical problems, create usable and accessible products, and provide meaningful user experiences to all [4, 24]. Since AI based tools will reshape work and personal environments, it's important that the developers of these tools also engage disabled users in their work both as codesigners and user testers. Considering all the already identified bias issues with large language models, on which these GenAI tools are built, this inclusive approach to design is even more important [25, 26, 27]. Participation of disabled designers, developers, and users in LLM development work can make these models less ableist, more robust, and offer better user experiences. Inferring from the findings of this study, we contribute a set of 21 best practices for designers and developers of GenAI tools. These best practices are an important step for making AI tools accessible because disabled and older adult users can benefit even more from the affordances of machine learning technologies.

Best Practices for Designing Inclusive and Screen Reader Accessible GenAI Tools:

- 1. Conceptualize AI tool users and use contexts inclusively and engage users with diverse disabilities in ideation, design, and development process.
- 2. Have blind users test prototypes and employ their feedback to shape the design during the development process.
- 3. Identify trouble spots in the GenAI user interface with an awareness of the blind users' adaptive technology and the difference in their contexts-of-use.
- 4. Instead of testing to ensure that the outcome matches the design plan, check if the plan was drawn inclusively in the first place.
- 5. Fit the designers and developers of GenAI tools and their interfaces with the practical know-how about adaptive user interfaces and how blind users interact in web environments.
- 6. Seek out developers with embodied differences, and give due consideration to their diverse perspectives that challenge normative and nondisabled perceptions.
- 7. Minimize user's memory burden by training models to create brief and to the point content.
- 8. Equip the GenAI tool with affordances of sound and touch that employ user senses beyond vision.
- 9. Situate the user for the novel GenAI interface by offering a description of the layout of the landing page.
- 10. Create an easy-to-follow hierarchy for screen reader users for navigating pages employing WCAG 2.2 heading structure just the way visual hierarchy of headings guides sighted users.
- 11. Arrange navigation menus and page content in a concise, logical, and well-organized layout to reduce cognitive overload.
- 12. Make user interface accessible for keyboard and voice input systems systematically.
- 13. Give meaningful text labels to buttons and links because screen readers cannot interpret graphics.
- 14. Give buttons and links distinct-sounding labels to prevent cognitive mix-ups.
- 15. Open pop-ups and other messages in a separate tab so that the reading flow of the original item is not disrupted by the screen reader.
- 16. Provide timely and contextually relevant audio feedback for user interaction.
- 17. Meet WCAG 2.2 standards on color contrast for low vision and color-blind users.
- 18. Offer sufficient customization options for improving the generated product.
- 19. Implement context-aware AI support throughout the builder platform.
- 20. Explore the possibilities of conversational LLMs for generating on-demand descriptions of visual interface layouts, flagging visual clues, and overall page glanceability.
- 21. Conduct accessible design impact surveys with disabled users for continuous quality improvement after the GenAI product is on the market.

### ACKNOWLEDGEMENTS

We thank the reviewers for their feedback. We also thank Keshreeyaji Jr. and Lohitvenkatesh for their research assistance.

### REFERENCES

[1] L. Heilig, "Critical Disability Studies in Technical Communication: A 25-Year History and the Future of Accessibility," in *The Palgrave Handbook of Disability and Communication,* Cham, Switzerland: Springer International Publishing, 2023, pp. 401-415.

[2] L. Melonçon, *Rhetorical accessability: At the intersection of technical communication and disability studies*, Amityville, NY: Baywood Publishing, 2014.

[3] S. K. Oswal, "Exploring accessibility as a potential area of research for technical communication: A modest proposal," *Communication Design Quarterly Review*, vol. 1, no. 4, pp. 50- 60, 2013.

[4] S. K. Oswal, "Breaking the exclusionary boundary between user experience and access: Steps toward making UX inclusive of users with disabilities," in *Proc. 37th ACM International Conf. on the Design of Communication*, Portland, OR, 2019, pp. 1-8.

[5] Z. B. Palmer and S. K. Oswal, "Constructing Websites with Generative AI: Workflows, Products, and Their Accessibility for Users with Disabilities," *J. of Business and Technical Communication,* forthcoming.

[6] World Health Organization, *World report on disability*, Geneva, Switzerland: WHO, 2011.

[7] S. Chandrashekar and R. Benedyk, "Accessibility vs. usability: Where is the dividing line," in *Proc. Ergonomics Society's Annu. Conf.,* San Francisco, CA, 2006, pp. 231-235.

[8] Z. B. Palmer and R. H. Palmer, "Legal and Ethical Implications of Website Accessibility," *Business and Professional Communication Quarterly*, vol. 81, no. 4, pp. 399- 420, 2018.

[9] European Accessibility Act (EUR-Lex), *EN 301 549*, European Union, 2025.

[10] P. W. Cardon et al., "Generative AI in the workplace: Employee perspectives of ChatGPT benefits and organizational policies," 2023, preprint.

[11] I. Pedersen, *Ready to wear: A rhetoric of wearable computers and reality-shifting media*, Anderson, SC: Parlor Press, 2013.

[12] J. T. Sherrill, "Makers: Technical communication in postindustrial participatory communities," M.A. Thesis, Purdue Univ., West Lafayette, IN, 2014.

[13] Y. Kong and H. Ding, "Tools, Potential, and Pitfalls of Social Media Screening: Social Profiling in the Era of AI-Assisted Recruiting," *J. of Business and Technical Communication*, vol. 38, no. 1, pp. 33-65, 2024.

[14] L. Markauskaite et al., "Rethinking the entwinement between artificial intelligence and human learning: What capabilities do learners need for a world with AI?," *Computers and Education: Artificial Intelligence*, vol. 3, pp. 1-16, 2022.

[15] A. H. Duin and I. Pedersen, *Augmentation Technologies and Artificial Intelligence in Technical Communication: Designing Ethical Futures*. New York, NY: Taylor & Francis, 2023.

[16] S. Horton and W. Quesenbery, *A web for everyone: Designing accessible user experiences.* Brooklyn, NY: Rosenfeld Media, 2014.

[17] C. M. Barnum, *Usability testing essentials: Ready, set... test!* Cambridge, MA: Morgan Kaufmann, 2020.

[18] J. Rubin and D. Chisnell, *Handbook of usability testing: How to plan, design, and conduct effective tests*, Indianapolis, IN: John Wiley & Sons, 2008.

[19] J. Saldana, *The Coding Manual for Qualitative Researchers*, 4th ed. Thousand Oaks, CA: Sage Publications, 2021.

[20] B. Light et al., "The walkthrough method: An approach to the study of apps," *New media & society*, vol. 20, no. 3, pp. 881- 900, 2018.

[21] J. Troeger and A. Bock, "The sociotechnical walkthrough–a methodological approach for platform studies," *Studies in Communication Sciences*, vol. 22, no. 1, pp. 43-52, 2022.

[22] *Guide for addressing accessibility in standards, ISO/IEC Guide 71:2014,* 2014.

[23] C. Power, et al. "Guidelines are only half of the story: accessibility problems encountered by blind users on the web." In *Proceedings of the SIGCHI conference on human factors in computing systems*, Austin, TX, 2012, pp. 433-442.

[24] J. P. Bigham et al., "Accessibility by demonstration: enabling end users to guide developers to web accessibility solutions," in *Proc. 12th International ACM SIGACCESS Conf. on Computers and Accessibility*, Orlando, FL, 2010, pp. 35-42.

[25] A. L. Hoffmann, "Where fairness fails: data, algorithms, and the limits of antidiscrimination discourse," *Information, Communication & Society*, vol. 22, no. 7, pp. 900-915, 2019.

[26] I. D. Raji and J. Buolamwini, "Actionable auditing: Investigating the impact of publicly naming biased performance results of commercial ai products," in *Proc. 2019 AAAI/ACM Conf. on AI, Ethics, and Society*, Honolulu, HI, 2019, pp. 429- 435.

[27] E. M. Bender et al. "On the Dangers of Stochastic Parrots: Can Language Models Be Too Big? ���������," in *Proc. 2021 ACM Conf. on Fairness, Accountability, and Transparency,* Virtual, Canada, 2021, pp. 610-623.

### ABOUT THE AUTHORS

**Sushil K. Oswal**, Ph.D., is a Professor of Human-Centered Design at the University of Washington. He is completing two ICT studies on the accessibility of healthcare and emergency preparedness for climate change.

**Hitender K. Oswal** studies computer science and biology at the University of Washington. He is presently conducting research on computer science education and multi-object manipulation in virtual reality at the UW Reality Lab. The concept for this project won the Best Developer Tool Award at the 2023 DubHacks Hackathon in Seattle.